# PFE proposal D: Agentic AI assistant for industrial operations, with guardrails and an evaluation harness
*Hazem Ilahi, ESPRIT (Data Science & AI). 6 months, Feb–Jul 2027.*

**Why this topic (demand seen in Phase 3).** Several live 2027 internship postings ask for agentic and LLM workflows in industrial settings: Sanofi (multi-agent architectures from prototype to production in manufacturing and supply chain), Bosch (agentic AI harness and GenAI workflows), Safran Helicopter Engines (chatbot with LLMs and agentics for industrial applications), and an energy-sector client via Askills (agents with an evaluation framework).

**Business problem.** Operators and engineers repeat multi-step tasks across several systems: read a fault code, check the procedure, compute a limit, open a work order. LLM agents can automate this, but without guardrails and measurement they are risky (wrong actions, invented facts, uncontrolled side effects).

**Value.** Shorter time from alarm to correct action, consistent procedures, and side effects (tickets, orders) that always pass human approval and an audit log. A reusable agent template plus an evaluation harness the host can extend.

**Data and access needed.** Procedure documents (or the RAG index from proposal B), fault-code and asset tables, a sandbox API of the ticketing or CMMS system, 100+ real requests with expected outcomes (built with operators), and the approved LLM (on-prem or enterprise API).

**Already built (starter repo, CPU, synthetic plant data).** Four tools (manual search, fault-code lookup, safe calculator, work-order creation). Guardrails: allow-list, argument validation, step budget, mandatory human approval for side effects, tool errors returned as observations. A CPU rule planner (intent classifier + slot rules) and a ReAct-style LLM planner that works with any model. A 12-scenario harness. The rule baseline scores **12/12**. A 0.5B open model run on CPU as a smoke test scores **0/3** (it loops until the step budget runs out), which shows exactly why the harness and guardrails are needed.

## 6-month plan
| Month | Milestone | Deliverable |
|---|---|---|
| Feb | Pick 2–3 target workflows with operators; risk analysis of each tool | Scope note, 50 scenarios |
| Mar | Tool layer on sandbox APIs (read-only first), retrieval tool (RAG) | Tool SDK, unit tests |
| Apr | Planners: rule baseline vs LLM (open and hosted), prompt and tool schemas, structured outputs | Harness results v1 |
| May | Guardrails: approval UI, policy checks, audit log, red-team scenarios | Safety report |
| Jun | Pilot with a small operator group, latency and cost optimisation, monitoring | Pilot metrics |
| Jul | Evaluation, documentation, hand-over, defence | Final report, runbook |

**Architecture.** User → agent loop (planner ↔ tools) → guardrail layer (allow-list, schema validation, approvals, budget) → tools (RAG search, fault DB, CMMS sandbox, calculator) → audit log and evaluation harness (offline scenarios + online traces).

**Stack.** Python, scikit-learn, open LLMs via Hugging Face transformers (Qwen/Llama class on GPU) or the host's enterprise LLM, FastAPI, Qdrant (RAG), pytest, Docker, tracing (OpenTelemetry/Langfuse-style).

**KPIs.** Task success rate on the scenario suite; tool-call accuracy; guardrail violations (target 0 unapproved side effects); steps and latency per task; cost per task; operator satisfaction.

**Risks and mitigations.** Wrong actions: read-only first, approvals for every write, sandbox only. Hallucinated facts: answers must come from tool outputs, with source citations. Model or vendor lock-in: planner interface is model-agnostic, harness compares models. Small models underperform: keep a rule or RAG fallback, and route only well-handled intents to the LLM.
