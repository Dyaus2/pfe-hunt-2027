"""Agent loop with guardrails: tool allow-list, argument validation, step budget, human approval for side effects."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from .tools import Tool


@dataclass
class Action:
    tool: str
    args: dict


@dataclass
class Final:
    answer: str
    sources: list[str] = field(default_factory=list)


@dataclass
class Step:
    action: Action
    observation: Any
    ok: bool


@dataclass
class Trace:
    query: str
    steps: list[Step] = field(default_factory=list)
    answer: str = ""
    sources: list[str] = field(default_factory=list)
    violations: list[str] = field(default_factory=list)

    @property
    def tools_called(self) -> list[str]:
        return [s.action.tool for s in self.steps]


class Agent:
    def __init__(self, planner, tools: dict[str, Tool], max_steps: int = 5,
                 approve: Callable[[str, dict], bool] = lambda tool, args: False):
        self.planner, self.tools, self.max_steps, self.approve = planner, tools, max_steps, approve

    def _validate(self, a: Action) -> str | None:
        if a.tool not in self.tools:
            return f"tool '{a.tool}' not allowed"
        spec = self.tools[a.tool].args
        missing = [k for k in spec if k not in a.args]
        extra = [k for k in a.args if k not in spec]
        bad = [k for k, t in spec.items() if k in a.args and not isinstance(a.args[k], t)]
        if missing or extra or bad:
            return f"invalid args for {a.tool}: missing={missing} extra={extra} wrong_type={bad}"
        return None

    def run(self, query: str) -> Trace:
        tr = Trace(query)
        for _ in range(self.max_steps):
            nxt = self.planner.next(query, tr)
            if isinstance(nxt, Final):
                tr.answer, tr.sources = nxt.answer, nxt.sources
                return tr
            err = self._validate(nxt)
            if err:
                tr.violations.append(err)
                tr.steps.append(Step(nxt, {"error": err}, False))
                continue
            tool = self.tools[nxt.tool]
            if tool.side_effect and not self.approve(tool.name, nxt.args):
                tr.violations.append(f"{tool.name} blocked: human approval missing")
                tr.steps.append(Step(nxt, {"error": "blocked: approval required"}, False))
                continue
            try:
                tr.steps.append(Step(nxt, tool.fn(**nxt.args), True))
            except Exception as e:  # tool errors become observations, never crashes
                tr.steps.append(Step(nxt, {"error": str(e)}, False))
        tr.answer = tr.answer or "Stopped: step budget exhausted."
        tr.violations.append("max_steps reached")
        return tr
