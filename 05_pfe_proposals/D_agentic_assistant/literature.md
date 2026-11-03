# State of practice: LLM agents, tool use and agent evaluation
All references were verified on 2026-11-03 via the arXiv API or the publisher page.

| # | Reference | Why it matters here |
|---|---|---|
| 1 | Yao et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. [arXiv:2210.03629](https://arxiv.org/abs/2210.03629) | The reason–act–observe loop implemented by `LLMPlanner`. |
| 2 | Schick et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. [arXiv:2302.04761](https://arxiv.org/abs/2302.04761) | Tool calls as a learnable API: motivates explicit tool schemas. |
| 3 | Shinn et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. [arXiv:2303.11366](https://arxiv.org/abs/2303.11366) | Self-correction from feedback: a candidate extension after the baseline. |
| 4 | Wang et al. (2023). *A Survey on Large Language Model based Autonomous Agents*. [arXiv:2308.11432](https://arxiv.org/abs/2308.11432) | Taxonomy (profile, memory, planning, action) for the design document. |
| 5 | Liu et al. (2023). *AgentBench: Evaluating LLMs as Agents*. [arXiv:2308.03688](https://arxiv.org/abs/2308.03688) | Scenario-based evaluation: inspiration for the harness and its metrics. |
| 6 | Zheng et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. [arXiv:2306.05685](https://arxiv.org/abs/2306.05685) | When LLM judges are reliable or biased; needed if answers are graded automatically. |
| 7 | Anthropic (2024). *Building effective agents* (engineering blog). [anthropic.com/research/building-effective-agents](https://www.anthropic.com/research/building-effective-agents) | Practitioner guidance: prefer simple, composable workflows, add autonomy only when measured to help. |

**Takeaways for the PFE.** Start with deterministic workflows plus an LLM only where it adds value. Every tool gets a schema, validation and a risk level. Measure everything on a scenario suite before and after each change.
