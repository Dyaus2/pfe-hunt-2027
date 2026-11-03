# PFE proposal B: Production RAG assistant for technical documentation, with evaluation and LLMOps
*Hazem Ilahi, ESPRIT (Data Science & AI). 6 months, Feb–Jul 2027.*

**Business problem.** Engineers and support teams lose time searching thousands of pages of manuals, procedures, test reports and tickets. Off-the-shelf chatbots hallucinate, can't cite sources, and nobody measures whether they actually find the right document.

**Value.** Faster answers with citations to the exact passage; less load on experts; a measurable quality bar (retrieval and faithfulness metrics) that the team can enforce at every release.

**Data needed.** Document corpus (PDF/Word/HTML; scanned pages are OK because OCR is in scope), metadata (product, version, language, confidentiality), 150–300 real questions with the correct passage (built with experts in month 1–2), and user feedback logs once piloted.

**Already built (starter repo, CPU, public data).** BM25 + dense + Reciprocal-Rank-Fusion hybrid retrieval, cross-encoder reranking, an evaluation bench (hit@k, MRR, p95 latency, SQuAD F1, groundedness proxy), an extractive or LLM answerer with citation filtering, and a FastAPI service. On a SQuAD v2 sample (621 passages, 600 questions): BM25 hit@1 0.81, hit@10 0.97. In a 100-question CPU smoke test, hybrid + cross-encoder reranking reached **hit@1 0.90 / MRR@10 0.92**. This builds on my Garage Augmenté work: 697k pages of manuals, BGE-M3 + BM25, reranking.

## 6-month plan
| Month | Milestone | Deliverable |
|---|---|---|
| Feb | Use cases, corpus inventory, access and confidentiality rules, gold-question protocol | Scope note, first 100 gold Q&A |
| Mar | Ingestion: parsing, OCR, chunking, metadata; hybrid index | Reproducible ingestion pipeline, index v1, retrieval bench v1 |
| Apr | Retrieval tuning (chunk size, hybrid weights, reranker, query expansion), multilingual FR/EN | Ablation report |
| May | Generation: prompt with mandatory citations, refusal when unsure, LLM-as-judge faithfulness | Answer-quality bench, guardrails |
| Jun | LLMOps: API, feedback capture, release gates on the bench, cost and latency monitoring | Pilot with 10–20 users |
| Jul | Pilot analysis, documentation, hand-over, defence | Final report, runbook |

**Architecture.** Sources → parser/OCR → chunker + metadata → BM25 index + vector DB (Qdrant) → hybrid retrieval + reranker → LLM (host-approved: on-prem open model or enterprise API) with citations → FastAPI → UI or Teams. An offline evaluation bench gates every change; online logging covers latency, feedback and query drift.

**Stack.** Python, Qdrant/FAISS, BGE-M3 (or host embedder), BM25, cross-encoders, PyMuPDF and Tesseract, FastAPI, Docker, MLflow or Langfuse-style tracing, pytest.

**KPIs.** hit@5 ≥ agreed target on the gold set; MRR; faithfulness (share of answers fully supported by cited passages); "I don't know" precision; p95 latency; cost per query; user thumbs-up rate.

**Risks and mitigations.** Confidential data: on-prem models, access-controlled index, no data leaves the host. Hallucinations: mandatory citations, refusal policy, faithfulness gate. Poor scans or tables: OCR quality checks, table-aware parsing. No gold set: build it with experts early, since it is the core of the evaluation.
