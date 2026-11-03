# Agentic assistant starter kit: tools + guardrails + evaluation harness
Tools (manual search, fault-code lookup, safe calculator, work order), guardrails (allow-list, arg validation, step budget, human approval for side effects), rule and ReAct-LLM planners, 12-scenario harness. Knowledge base is SYNTHETIC.

**Status:** starter skeleton for a PFE pitch, tested on CPU on 2026-11-03 (`pytest` green, notebook executed end to end).
**Measured baseline:** Rule planner 12/12 scenarios; Qwen2.5-0.5B-Instruct (CPU smoke, 3 scenarios) 0/3 — use the 1.5B+ model on a T4 and compare.

## Layout
```
src/agentkit/{tools,agent,planners,evaluate}.py, src/agentkit/resources/{kb.json,scenarios.jsonl}
tests/            pytest suite (synthetic data, runs offline in seconds)
notebooks/D_agentic_assistant_colab.ipynb   self-contained Colab notebook (embeds src/, executed outputs included)
notebooks/cells.py   notebook source; rebuild with: python ../../tools/build_notebook.py ../../D_agentic_assistant
requirements.txt
```

## Run
```bash
pip install -r requirements.txt
python -m pytest -q
python -c "import sys; sys.path.insert(0,'src'); from agentkit.evaluate import *; from agentkit.planners import RulePlanner; p=RulePlanner(); print(summarize(run_suite(lambda t: p)))"
```
**Colab:** upload `notebooks/D_agentic_assistant_colab.ipynb` (File → Upload notebook) and *Run all*; it writes the package itself, no clone needed. Cells marked **[GPU — Colab T4]** need Runtime → Change runtime type → T4 GPU (they also run as a slow CPU smoke test).

## My role
Designed and implemented by Hazem Ilahi as a PFE proposal starter; see `../pitch_EN.md`, `../pitch_FR.md`, `../literature.md`.
