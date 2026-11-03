# State of practice: retrieval-augmented generation in production
All references were verified on 2026-11-03 via Crossref (DOI) or the arXiv API.

| # | Reference | Why it matters here |
|---|---|---|
| 1 | Lewis et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401) | The original RAG formulation: ground generation in retrieved passages. |
| 2 | Gao et al. (2023). *Retrieval-Augmented Generation for Large Language Models: A Survey*. [arXiv:2312.10997](https://arxiv.org/abs/2312.10997) | Map of naive, advanced and modular RAG; checklist for chunking, retrieval, reranking and evaluation. |
| 3 | Robertson & Zaragoza (2009). *The Probabilistic Relevance Framework: BM25 and Beyond*. FnTIR. [doi:10.1561/1500000019](https://doi.org/10.1561/1500000019) | BM25, still a strong baseline on technical vocabulary (part numbers, fault codes). |
| 4 | Cormack, Clarke, Büttcher (2009). *Reciprocal rank fusion outperforms Condorcet and individual rank learning methods*. SIGIR. [doi:10.1145/1571941.1572114](https://doi.org/10.1145/1571941.1572114) | RRF: parameter-light fusion of sparse and dense rankings (`rrf_fuse`). |
| 5 | Chen et al. (2024). *M3-Embedding (BGE-M3): Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings*. [arXiv:2402.03216](https://arxiv.org/abs/2402.03216) | Multilingual dense retriever (FR/EN/AR), used in Garage Augmenté and in the [GPU] cell. |
| 6 | Nogueira & Cho (2019). *Passage Re-ranking with BERT*. [arXiv:1901.04085](https://arxiv.org/abs/1901.04085) | Cross-encoder reranking: the largest single gain in our smoke test (hit@1 0.80 → 0.90). |
| 7 | Es, James, Espinosa-Anke, Schockaert (2023). *RAGAS: Automated Evaluation of Retrieval Augmented Generation*. [arXiv:2309.15217](https://arxiv.org/abs/2309.15217) | Reference-free faithfulness and relevance metrics for the answer-quality gate. |

**Takeaways for the PFE.** Hybrid retrieval plus reranking is the robust default. The gold question set and the evaluation gate matter more than the choice of LLM. Citations and a refusal policy are what make RAG acceptable in industry.
