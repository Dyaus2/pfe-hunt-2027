import pytest

from agentkit.agent import Action, Agent, Final
from agentkit.evaluate import run_suite, summarize
from agentkit.planners import LLMPlanner, RulePlanner
from agentkit.tools import Outbox, make_tools, safe_eval


def test_safe_eval():
    assert safe_eval("2*(3+4)") == 14
    for bad in ["__import__('os').system('ls')", "a+1", "(1).real", "9**9**9**9" * 20]:
        with pytest.raises(Exception):
            safe_eval(bad)


def test_rule_planner_passes_full_suite():
    planner = RulePlanner()
    s = summarize(run_suite(lambda tools: planner))
    assert s["task_success"] == 1.0 and s["n"] == 12


class Scripted:
    """Fake LLM returning canned replies (lets us test parsing + guardrails without a model)."""
    def __init__(self, replies): self.replies = list(replies)
    def __call__(self, prompt): return self.replies.pop(0)


def test_llm_planner_tool_then_final():
    tools = make_tools(Outbox())
    llm = Scripted(['Thought... {"tool": "lookup_fault_code", "args": {"code": "E101"}}',
                    '{"final": "Suction pressure low on P-200", "sources": ["FAULT:E101"]}'])
    tr = Agent(LLMPlanner(llm, tools), tools).run("what is E101?")
    assert tr.tools_called == ["lookup_fault_code"] and "Suction" in tr.answer and not tr.violations


def test_guardrails_block_bad_calls_and_side_effects():
    out = Outbox(); tools = make_tools(out)
    llm = Scripted(['not json at all',
                    '{"tool": "rm_rf", "args": {}}',
                    '{"tool": "calculator", "args": {"expression": 5}}',
                    '{"tool": "create_work_order", "args": {"asset": "P-200", "priority": "P1", "summary": "x"}}',
                    '{"final": "done"}'])
    tr = Agent(LLMPlanner(llm, tools), tools, approve=lambda t, a: False).run("q")
    assert len(tr.violations) == 4 and out.work_orders == [] and tr.answer == "done"


def test_step_budget():
    class Loop:
        def next(self, q, tr): return Action("calculator", {"expression": "1+1"})
    tools = make_tools()
    tr = Agent(Loop(), tools, max_steps=3).run("q")
    assert len(tr.steps) == 3 and "max_steps reached" in tr.violations
