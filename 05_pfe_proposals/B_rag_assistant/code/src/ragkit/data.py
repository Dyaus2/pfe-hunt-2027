"""Public stand-in corpus for development: SQuAD v2.0 dev set (Wikipedia paragraphs + questions).

In the PFE, replace it with the host's technical documentation; keep the same Passage/Query schema.
SQuAD: Rajpurkar et al. — https://rajpurkar.github.io/SQuAD-explorer/ (CC BY-SA 4.0).
"""
from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path

SQUAD_DEV_URL = "https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json"


@dataclass(frozen=True)
class Passage:
    pid: str
    title: str
    text: str


@dataclass(frozen=True)
class Query:
    qid: str
    question: str
    gold_pid: str
    answers: tuple[str, ...]


def download_squad(dest: str | Path = "data/squad_dev_v2.json", url: str = SQUAD_DEV_URL) -> Path:
    dest = Path(dest)
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url, timeout=120) as r:
            dest.write_bytes(r.read())
    return dest


def load_squad(path: str | Path, max_articles: int | None = None) -> tuple[list[Passage], list[Query]]:
    """Each paragraph → Passage; each answerable question → Query whose gold is its paragraph."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))["data"]
    passages, queries = [], []
    for a_i, art in enumerate(raw[:max_articles] if max_articles else raw):
        for p_i, para in enumerate(art["paragraphs"]):
            pid = f"{a_i}-{p_i}"
            passages.append(Passage(pid, art["title"].replace("_", " "), para["context"]))
            for qa in para["qas"]:
                if qa.get("is_impossible"):
                    continue
                answers = tuple(dict.fromkeys(a["text"] for a in qa["answers"]))
                queries.append(Query(qa["id"], qa["question"], pid, answers))
    return passages, queries


def chunk_text(text: str, max_words: int = 180, overlap: int = 40) -> list[str]:
    """Word-window chunker with overlap, sentence-aligned when possible (for long manuals)."""
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks, cur = [], []
    for s in sents:
        w = s.split()
        if cur and len(cur) + len(w) > max_words:
            chunks.append(" ".join(cur))
            cur = cur[-overlap:] if overlap else []
        cur.extend(w)
    if cur:
        chunks.append(" ".join(cur))
    return chunks
