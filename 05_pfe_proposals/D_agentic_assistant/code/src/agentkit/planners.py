"""Planners decide the next tool call or the final answer.

RulePlanner: CPU baseline = intent classifier (TF-IDF + logistic regression) + slot extraction by regex.
LLMPlanner: ReAct-style (Yao et al. 2022, arXiv:2210.03629) JSON tool calls from any `llm(prompt) -> str`.
"""
from __future__ import annotations

import json
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

from .agent import Action, Final, Trace

INTENT_EXAMPLES = {
    "fault_code": ["what does fault E102 mean", "explain error code E205", "alarm E330 on the belt", "code E101 meaning",
                   "what is fault code E401", "E210 popped up what should I do"],
    "procedure": ["how do I start the pump", "what is the vibration limit", "how often change compressor oil",
                  "belt tension check procedure", "what is lockout tagout", "max bearing temperature",
                  "when to clean the heat exchanger", "what oil for the compressor"],
    "calculation": ["compute 4000*3", "what is 7.1 - 4.5", "calculate 2 percent of 1200 which is 0.02*1200", "how much is 85+10"],
    "work_order": ["create a work order for E102", "open a ticket for fault E205", "raise a work order for pump P-200 due to E101",
                   "log a maintenance job for E330", "please create work order E401"],
    "out_of_scope": ["what is the weather today", "tell me a joke", "who won the football match", "book me a flight to Paris"],
}
CODE = re.compile(r"\b(E\d{3})\b", re.I)
EXPR = re.compile(r"([0-9\.\s\+\-\*/\(\)]{3,})")


class RulePlanner:
    def __init__(self):
        X, y = zip(*[(t, k) for k, v in INTENT_EXAMPLES.items() for t in v])
        self.clf = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True),
                                 LogisticRegression(max_iter=2000, C=10.0)).fit(X, y)

    def intent(self, q: str) -> str:
        return self.clf.predict([q])[0]

    def next(self, query: str, tr: Trace):
        intent = self.intent(query)
        done = tr.tools_called
        obs = [s.observation for s in tr.steps if s.ok]
        code = CODE.search(query)
        if code and intent in ("calculation", "procedure", "out_of_scope"):
            intent = "fault_code"  # slot evidence (a fault-code pattern) overrides a weak classifier guess
        if intent == "out_of_scope":
            return Final("This assistant only answers plant-maintenance questions.")
        if intent in ("fault_code", "work_order") and code is None:
            return Final("Please give the fault code (e.g. E102).")
        if intent == "fault_code":
            if "lookup_fault_code" not in done:
                return Action("lookup_fault_code", {"code": code.group(1).upper()})
            f = obs[-1]
            if "error" in f:
                return Final(f"Unknown fault code {f['code']}.")
            return Final(f"{f['code']} on {f['asset']}: {f['description']} (severity {f['severity']}). Action: {f['action']}",
                         [f"FAULT:{f['code']}"])
        if intent == "work_order":
            if "lookup_fault_code" not in done:
                return Action("lookup_fault_code", {"code": code.group(1).upper()})
            f = next(o for o in obs if isinstance(o, dict) and "code" in o)
            if "error" in f:
                return Final(f"Unknown fault code {f['code']}; no work order created.")
            if "create_work_order" not in done:
                return Action("create_work_order", {"asset": f["asset"], "priority": f["severity"],
                                                    "summary": f"{f['code']}: {f['description']}"})
            last = tr.steps[-1]
            if not last.ok:
                return Final(f"Work order NOT created ({last.observation['error']}). Suggested: {f['severity']} on {f['asset']}.")
            wo = last.observation
            return Final(f"Created {wo['id']} ({wo['priority']}) for {wo['asset']}: {wo['summary']}", [f"FAULT:{f['code']}"])
        if intent == "calculation":
            m = EXPR.search(query)
            if "calculator" not in done and m:
                return Action("calculator", {"expression": m.group(1).strip()})
            if obs and "result" in obs[-1]:
                return Final(f"Result: {obs[-1]['result']:g}")
            return Final("I could not find an arithmetic expression.")
        # procedure
        if "search_manual" not in done:
            return Action("search_manual", {"query": query})
        hits = obs[-1] if obs else []
        if not hits:
            return Final("I don't know — nothing relevant in the procedures.")
        return Final(hits[0]["text"], [h["id"] for h in hits[:1]])


REACT_PROMPT = """You are a plant-maintenance assistant. Use tools; never invent facts.
Tools:
{tools}
Reply with ONE JSON object per turn, either
{{"tool": "<name>", "args": {{...}}}}  or  {{"final": "<answer>", "sources": ["<ids>"]}}

Question: {query}
{history}
Next JSON:"""


class LLMPlanner:
    def __init__(self, llm, tools):
        self.llm, self.tools = llm, tools

    def next(self, query: str, tr: Trace):
        hist = "\n".join(f"Called {s.action.tool}({json.dumps(s.action.args)}) -> {json.dumps(s.observation)[:400]}" for s in tr.steps)
        desc = "\n".join(f"- {t.name}: {t.description}" for t in self.tools.values())
        raw = self.llm(REACT_PROMPT.format(tools=desc, query=query, history=hist))
        m = re.search(r"\{.*\}", raw, re.S)
        try:
            obj = json.loads(m.group(0)) if m else None
        except json.JSONDecodeError:
            obj = None
        if not isinstance(obj, dict):
            return Action("__invalid__", {"raw": raw[:200]})  # rejected by the guardrails, recorded as violation
        if "final" in obj:
            return Final(str(obj["final"]), [str(s) for s in obj.get("sources", [])])
        return Action(str(obj.get("tool")), obj.get("args") if isinstance(obj.get("args"), dict) else {})
