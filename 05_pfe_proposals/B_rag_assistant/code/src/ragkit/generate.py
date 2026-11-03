"""Answer generation. Default = extractive baseline (no LLM, CPU, deterministic).
Plug any LLM by passing a callable `llm(prompt: str) -> str` to LLMAnswerer."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, Sequence

from .retrieval import tokenize

PROMPT = """You are a maintenance assistant. Answer ONLY from the context passages below.
Cite the passage ids you used in square brackets, e.g. [3-1]. If the answer is not in the context, reply exactly: "I don't know."

Context:
{context}

Question: {question}
Answer:"""


@dataclass
class Answer:
    text: str
    cited: list[str] = field(default_factory=list)


class ExtractiveAnswerer:
    """Returns the context sentence with the highest token overlap with the question."""

    def __call__(self, question: str, contexts: Sequence[tuple[str, str]]) -> Answer:
        q = set(tokenize(question))
        best, best_pid, best_s = "", None, -1.0
        for pid, text in contexts:
            for sent in re.split(r"(?<=[.!?])\s+", text):
                toks = tokenize(sent)
                if not toks:
                    continue
                s = len(q & set(toks)) / (len(q) ** 0.5 * len(toks) ** 0.5 + 1e-9)
                if s > best_s:
                    best, best_pid, best_s = sent, pid, s
        return Answer(best or "I don't know.", [best_pid] if best_pid else [])


class LLMAnswerer:
    def __init__(self, llm: Callable[[str], str]):
        self.llm = llm

    def __call__(self, question: str, contexts: Sequence[tuple[str, str]]) -> Answer:
        ctx = "\n\n".join(f"[{pid}] {text}" for pid, text in contexts)
        out = self.llm(PROMPT.format(context=ctx, question=question)).strip()
        cited = sorted(set(re.findall(r"\[([^\]]+)\]", out)) & {pid for pid, _ in contexts})
        return Answer(out, cited)


class RAGPipeline:
    def __init__(self, retriever, passages, answerer=None, k: int = 5):
        self.retriever, self.k = retriever, k
        self.by_id = {p.pid: p for p in passages}
        self.answerer = answerer or ExtractiveAnswerer()

    def ask(self, question: str) -> dict:
        hits = self.retriever.search(question, self.k)
        ctx = [(pid, self.by_id[pid].text) for pid, _ in hits]
        ans = self.answerer(question, ctx)
        return {"answer": ans.text, "cited": ans.cited, "retrieved": [pid for pid, _ in hits]}
