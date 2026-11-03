"""Tools the agent may call. Each declares an argument schema and whether it has side effects."""
from __future__ import annotations

import ast
import json
import operator
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import numpy as np
from rank_bm25 import BM25Okapi

KB = json.loads((Path(__file__).parent / "resources" / "kb.json").read_text(encoding="utf-8"))


def tokenize(t: str) -> list[str]:
    return re.findall(r"[a-z0-9\-\.]+", t.lower())


@dataclass
class Tool:
    name: str
    description: str
    args: dict[str, type]
    fn: Callable[..., Any]
    side_effect: bool = False


class Manual:
    def __init__(self, passages=None):
        self.p = passages or KB["passages"]
        self.bm25 = BM25Okapi([tokenize(x["title"] + " " + x["text"]) for x in self.p])

    def search(self, query: str, k: int = 2) -> list[dict]:
        s = self.bm25.get_scores(tokenize(query))
        return [{"id": self.p[i]["id"], "text": self.p[i]["text"]} for i in np.argsort(-s)[:k] if s[i] > 0]


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos}


def safe_eval(expr: str) -> float:
    """Arithmetic only (+ - * / ** and parentheses). No names, calls or attributes."""
    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](ev(n.operand))
        raise ValueError("unsupported expression")
    if len(expr) > 100:
        raise ValueError("expression too long")
    return float(ev(ast.parse(expr, mode="eval")))


@dataclass
class Outbox:
    work_orders: list[dict] = field(default_factory=list)


def make_tools(outbox: Outbox | None = None, manual: Manual | None = None) -> dict[str, Tool]:
    outbox = outbox if outbox is not None else Outbox()
    manual = manual or Manual()

    def lookup_fault_code(code: str) -> dict:
        c = KB["fault_codes"].get(code.strip().upper())
        return {"code": code.upper(), **c} if c else {"code": code.upper(), "error": "unknown fault code"}

    def create_work_order(asset: str, priority: str, summary: str) -> dict:
        if priority not in ("P1", "P2", "P3"):
            raise ValueError("priority must be P1, P2 or P3")
        wo = {"id": f"WO-{len(outbox.work_orders) + 1:04d}", "asset": asset, "priority": priority, "summary": summary}
        outbox.work_orders.append(wo)
        return wo

    tools = [
        Tool("search_manual", "Search maintenance procedures. Args: query (str).", {"query": str}, lambda query: manual.search(query)),
        Tool("lookup_fault_code", "Look up a fault code like E102. Args: code (str).", {"code": str}, lookup_fault_code),
        Tool("calculator", "Evaluate arithmetic, e.g. '4000*3'. Args: expression (str).", {"expression": str},
             lambda expression: {"result": safe_eval(expression)}),
        Tool("create_work_order", "Create a maintenance work order (SIDE EFFECT, needs human approval). "
             "Args: asset (str), priority (P1|P2|P3), summary (str).", {"asset": str, "priority": str, "summary": str},
             create_work_order, side_effect=True),
    ]
    return {t.name: t for t in tools}
