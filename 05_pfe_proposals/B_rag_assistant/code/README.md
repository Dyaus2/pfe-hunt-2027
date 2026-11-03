# RAG starter kit: hybrid retrieval + evaluation bench + service
BM25 + dense (LSA on CPU / BGE-M3 on GPU) fused by RRF, cross-encoder reranker, hit@k/MRR/latency bench, extractive or LLM answerer with citation filter, FastAPI.

**Status:** starter skeleton for a PFE pitch, tested on CPU on 2026-11-03 (`pytest` green, notebook executed end to end).
**Measured baseline:** SQuAD v2 sample (621 passages / 600 q): BM25 hit@1 0.807, hit@10 0.965; hybrid hit@10 0.962. CPU smoke (100 q, MiniLM + ms-marco reranker): hybrid+rerank hit@1 0.90, MRR@10 0.924.

## Layout
```
src/ragkit/{data,retrieval,evaluate,generate,service}.py
tests/            pytest suite (synthetic data, runs offline in seconds)
notebooks/B_rag_assistant_colab.ipynb   self-contained Colab notebook (embeds src/, executed outputs included)
notebooks/cells.py   notebook source; rebuild with: python ../../tools/build_notebook.py ../../B_rag_assistant
requirements.txt
```

## Run
```bash
pip install -r requirements.txt
python -m pytest -q
python -c "import sys; sys.path.insert(0,'src'); from ragkit import data; print(data.download_squad())"
# then follow the notebook
```
**Colab:** upload `notebooks/B_rag_assistant_colab.ipynb` (File → Upload notebook) and *Run all*; it writes the package itself, no clone needed. Cells marked **[GPU — Colab T4]** need Runtime → Change runtime type → T4 GPU (they also run as a slow CPU smoke test).

## My role
Designed and implemented by Hazem Ilahi as a PFE proposal starter; see `../pitch_EN.md`, `../pitch_FR.md`, `../literature.md`.
