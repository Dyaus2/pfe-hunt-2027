"""Scenario-based evaluation: task success, exact tool-sequence accuracy, steps, guardrail events."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .agent import Agent
from .tools import Outbox, make_tools

SCENARIOS = Path(__file__).parent / "resources" / "scenarios.jsonl"


def load_scenarios(path: str | Path = SCENARIOS) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def run_suite(planner_factory, scenarios: list[dict] | None = None, max_steps: int = 5) -> pd.DataFrame:
    rows = []
    for sc in scenarios or load_scenarios():
        tools = make_tools(Outbox())
        agent = Agent(planner_factory(tools), tools, max_steps=max_steps,
                      approve=(lambda t, a: True) if sc["approve"] else (lambda t, a: False))
        tr = agent.run(sc["query"])
        contains = all(s.lower() in tr.answer.lower() for s in sc["must_contain"])
        tools_ok = tr.tools_called == sc["expected_tools"]
        rows.append({"id": sc["id"], "query": sc["query"], "success": contains and tools_ok, "answer_ok": contains,
                     "tools_ok": tools_ok, "steps": len(tr.steps), "violations": len(tr.violations),
                     "tools": tr.tools_called, "answer": tr.answer})
    return pd.DataFrame(rows)


def summarize(df: pd.DataFrame) -> dict:
    return {"task_success": float(df["success"].mean()), "answer_ok": float(df["answer_ok"].mean()),
            "tool_sequence_acc": float(df["tools_ok"].mean()), "avg_steps": float(df["steps"].mean()),
            "guardrail_events": int(df["violations"].sum()), "n": int(len(df))}
