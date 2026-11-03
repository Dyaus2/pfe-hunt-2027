TITLE = """# PFE proposal D — Agentic maintenance assistant: tools, guardrails, evaluation harness
A tool-using agent (manual search, fault-code lookup, calculator, work-order creation) with guardrails:
tool allow-list, argument validation, step budget, **human approval for side effects**. Evaluated on a scenario suite.
CPU baseline planner = intent classifier + slot rules. **[GPU — Colab T4]** cell: an open LLM as ReAct planner.
The knowledge base is a small **synthetic** plant (fictional ACME assets) — replace with the host's procedures."""
PIP = "scikit-learn pandas numpy rank_bm25"

CELLS = [
("code", """import pandas as pd
pd.set_option('display.max_colwidth', 90)
from agentkit.evaluate import run_suite, summarize
from agentkit.planners import RulePlanner
rule = RulePlanner()
df = run_suite(lambda tools: rule)
print(summarize(df))
df[['id', 'query', 'tools', 'answer', 'success']]"""),
("md", """### Guardrails in action (scripted LLM replies, no model needed)"""),
("code", """from agentkit.agent import Agent
from agentkit.planners import LLMPlanner
from agentkit.tools import Outbox, make_tools
class Scripted:
    def __init__(self, r): self.r = list(r)
    def __call__(self, prompt): return self.r.pop(0)
out = Outbox(); tools = make_tools(out)
llm = Scripted(['{"tool": "delete_database", "args": {}}',
                '{"tool": "create_work_order", "args": {"asset": "P-200", "priority": "P1", "summary": "vibration"}}',
                '{"final": "Work order needs supervisor approval.", "sources": []}'])
tr = Agent(LLMPlanner(llm, tools), tools, approve=lambda t, a: False).run('Create a WO for P-200 vibration')
print('violations:', tr.violations); print('work orders created:', out.work_orders); print('answer:', tr.answer)"""),
("md", """## [GPU — Colab T4] Open LLM as planner (ReAct-style JSON tool calls)
On a T4: `Qwen/Qwen2.5-1.5B-Instruct` on the full suite. On CPU: `Qwen/Qwen2.5-0.5B-Instruct` on 3 scenarios (smoke test, slow).
Expect a small model to score below the rule baseline — measuring that gap is exactly what the PFE evaluation harness is for."""),
("code", """import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from agentkit.evaluate import load_scenarios
gpu = torch.cuda.is_available()
NAME = 'Qwen/Qwen2.5-1.5B-Instruct' if gpu else 'Qwen/Qwen2.5-0.5B-Instruct'
tok = AutoTokenizer.from_pretrained(NAME)
model = AutoModelForCausalLM.from_pretrained(NAME, torch_dtype=torch.float16 if gpu else torch.float32).to('cuda' if gpu else 'cpu')
def hf_llm(prompt):
    msgs = [{'role': 'user', 'content': prompt}]
    enc = tok.apply_chat_template(msgs, add_generation_prompt=True, return_tensors='pt', return_dict=True).to(model.device)
    with torch.no_grad():
        outp = model.generate(**enc, max_new_tokens=96, do_sample=False)
    return tok.decode(outp[0, enc['input_ids'].shape[1]:], skip_special_tokens=True)
scen = load_scenarios() if gpu else [s for s in load_scenarios() if s['id'] in ('s01', 's04', 's11')]
llm_df = run_suite(lambda tools: LLMPlanner(hf_llm, tools), scen, max_steps=4)
print(NAME, summarize(llm_df))
llm_df[['id', 'tools', 'answer', 'success', 'violations']]"""),
("md", """## Next steps for the PFE
1. Connect real tools (CMMS/ticketing API in a sandbox, document search from proposal B) behind the same guardrails.
2. Grow the scenario suite with operators (100+ cases, incl. adversarial/unsafe requests); track success, tool accuracy, cost, latency per release.
3. Compare planners (rules, small open LLM, hosted LLM) on the same harness; add human-in-the-loop approval UI and audit log."""),
]
