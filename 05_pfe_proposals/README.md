# Phase 4: Self-proposed PFE subjects (pitch EN + FR, literature, tested starter code)

| | Subject | Fits these targets (Phase 3) | Pitch | Code baseline (CPU, public data) |
|---|---|---|---|---|
| **A** | Predictive maintenance & anomaly detection on sensor data | Thales PdM, Airbus acoustic testing, ENGIE PdM, ABB time series, AFI KLM E&M, Safran | [EN](A_predictive_maintenance/pitch_EN.md) · [FR](A_predictive_maintenance/pitch_FR.md) · [refs](A_predictive_maintenance/literature.md) | [code](A_predictive_maintenance/code/) — C-MAPSS FD001 RMSE 15.3 |
| **B** | Production RAG assistant + evaluation + LLMOps | ATR knowledge extraction, Safran chatbot, Airbus Helicopters knowledge, Sanofi | [EN](B_rag_assistant/pitch_EN.md) · [FR](B_rag_assistant/pitch_FR.md) · [refs](B_rag_assistant/literature.md) | [code](B_rag_assistant/code/) — hybrid+rerank hit@1 0.90 |
| **C** | MLOps: drift monitoring + champion/challenger + rollback | Thales cloud ops AI, Bosch production data, any team with models in production | [EN](C_mlops_drift/pitch_EN.md) · [FR](C_mlops_drift/pitch_FR.md) · [refs](C_mlops_drift/literature.md) | [code](C_mlops_drift/code/) — Elec2 AUC 0.764 → 0.845 |
| **D** | Agentic AI assistant with guardrails + eval harness (demand seen in Sanofi/Bosch/Safran/Askills postings) | Sanofi, Bosch agentic AI, Safran, InstaDeep | [EN](D_agentic_assistant/pitch_EN.md) · [FR](D_agentic_assistant/pitch_FR.md) · [refs](D_agentic_assistant/literature.md) | [code](D_agentic_assistant/code/) — rule baseline 12/12 |

**How to use in an application:** attach the matching 1-page pitch PDF (export the .md) to a spontaneous application, and link the code folder once the repo (or a public showcase copy) is visible. Say in the email: *"I prepared a 6-month plan and a working baseline on public data."*

**Testing (2026-11-03, this workspace, CPU only):** every package has a green `pytest` suite, and every notebook was executed end to end with `tools/build_notebook.py` (outputs saved in the .ipynb). GPU cells ran as CPU smoke tests with small models.

**Make the repo public?** The notebooks are self-contained, so a recruiter can run them in Colab from a downloaded file. To share links, create a separate **public** showcase repo with only `05_pfe_proposals/` (your CV and target list stay private).
