TITLE = """# PFE proposal B — Production RAG assistant: hybrid retrieval + evaluation bench + service
Public stand-in corpus: SQuAD v2.0 dev (Wikipedia paragraphs, CC BY-SA 4.0). In the PFE, swap in the host's manuals.
CPU path: BM25, LSA "dense" stand-in, RRF hybrid, extractive answers, metrics. **[GPU — Colab T4]** cells: BGE-M3 embeddings + cross-encoder reranking."""
PIP = "scikit-learn pandas numpy rank_bm25 fastapi httpx"

CELLS = [
("code", """from ragkit import data
from ragkit.retrieval import BM25Retriever, DenseRetriever, HybridRetriever, LsaEncoder
from ragkit.evaluate import evaluate_retriever
import random, pandas as pd
path = data.download_squad('data/squad_dev_v2.json')
passages, queries = data.load_squad(path, max_articles=20)   # CPU-sized sample; raise for full runs
random.Random(0).shuffle(queries); queries = queries[:600]
print(len(passages), 'passages |', len(queries), 'queries')"""),
("code", """bm25 = BM25Retriever(passages)
lsa = DenseRetriever(passages, LsaEncoder(dim=256))
hyb = HybridRetriever([bm25, lsa], depth=50)
table = pd.DataFrame({name: evaluate_retriever(r, queries) for name, r in
                      [('BM25', bm25), ('LSA (dense stand-in)', lsa), ('Hybrid RRF', hyb)]}).T
table.round(3)"""),
("code", """from ragkit.generate import RAGPipeline
from ragkit.evaluate import f1, groundedness
pipe = RAGPipeline(hyb, passages, k=5)
sample = queries[:100]
res = [pipe.ask(q.question) for q in sample]
ctx = lambda r: [pipe.by_id[p].text for p in r['retrieved']]
print('answer-sentence F1 vs gold (extractive baseline):', round(sum(f1(r['answer'], q.answers) for r, q in zip(res, sample)) / len(sample), 3))
print('groundedness proxy:', round(sum(groundedness(r['answer'], ctx(r)) for r in res) / len(res), 3))
pipe.ask(queries[0].question) | {'question': queries[0].question, 'gold': queries[0].answers}"""),
("code", """# Serve it (FastAPI). In Colab, test in-process with TestClient:
from fastapi.testclient import TestClient
from ragkit.service import create_app
client = TestClient(create_app(pipe))
client.post('/ask', json={'question': queries[1].question}).json()"""),
("md", """## [GPU — Colab T4] Neural dense retrieval (BGE-M3) + cross-encoder reranking
On CPU this cell uses small models on 100 queries as a smoke test. On a T4 it uses `BAAI/bge-m3` and `BAAI/bge-reranker-v2-m3`."""),
("code", """%pip install -q sentence-transformers
import torch
from ragkit.retrieval import SentenceTransformerEncoder, CrossEncoderReranker
gpu = torch.cuda.is_available()
EMB = 'BAAI/bge-m3' if gpu else 'sentence-transformers/all-MiniLM-L6-v2'
RER = 'BAAI/bge-reranker-v2-m3' if gpu else 'cross-encoder/ms-marco-MiniLM-L-6-v2'
qs = queries if gpu else queries[:100]
neural = DenseRetriever(passages, SentenceTransformerEncoder(EMB, batch_size=64 if gpu else 16))
hyb2 = HybridRetriever([bm25, neural], depth=50)
rerank = CrossEncoderReranker(hyb2, passages, RER, depth=20)
pd.DataFrame({n: evaluate_retriever(r, qs) for n, r in [(f'Dense {EMB.split("/")[-1]}', neural),
              ('Hybrid BM25+neural', hyb2), ('Hybrid + rerank', rerank)]}).T.round(3)"""),
("md", """## Next steps for the PFE
1. Ingest the host's documents (PDF → text/OCR → `chunk_text`), keep metadata filters (product, version, language).
2. Build a 150–300 question gold set with domain experts; track hit@k/MRR + answer faithfulness (LLM-judge, e.g. RAGAS) per release.
3. Gate every index/model change on the bench (no regression > 1 pt), log latency + feedback, monitor query drift."""),
]
