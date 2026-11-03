import pytest

from ragkit.data import Passage, Query, chunk_text
from ragkit.evaluate import evaluate_retriever, exact_match, f1, groundedness, hit_at_k, reciprocal_rank
from ragkit.generate import ExtractiveAnswerer, LLMAnswerer, RAGPipeline
from ragkit.retrieval import BM25Retriever, DenseRetriever, HybridRetriever, LsaEncoder, rrf_fuse

DOCS = [
    Passage("p1", "Brakes", "Replace the brake pads when the thickness is below 3 mm. Brake fluid must be changed every two years."),
    Passage("p2", "Engine oil", "Engine oil should be changed every 15000 km or once a year. Use 5W-30 synthetic oil."),
    Passage("p3", "Battery", "A battery voltage under 12.2 volts indicates a weak battery. Check the alternator output."),
    Passage("p4", "Tyres", "Tyre pressure must be checked monthly. Rotate the tyres every 10000 km."),
    Passage("p5", "Fault codes", "Fault code P0300 means random or multiple cylinder misfire detected."),
] * 1  # keep tiny
QS = [Query("q1", "When should brake fluid be changed?", "p1", ("every two years",)),
      Query("q2", "What does P0300 mean?", "p5", ("random or multiple cylinder misfire",)),
      Query("q3", "Which oil grade should I use?", "p2", ("5W-30",))]


def test_metrics_math():
    assert hit_at_k(["a", "b"], "b", 1) == 0.0 and hit_at_k(["a", "b"], "b", 2) == 1.0
    assert reciprocal_rank(["a", "b", "c"], "c") == pytest.approx(1 / 3)
    assert exact_match("The 5W-30", ["5W-30"]) == 1.0
    assert f1("every two years", ["every 2 years"]) == pytest.approx(2 * (2 / 3) * (2 / 3) / (4 / 3))
    assert groundedness("brake fluid two years", ["Brake fluid must be changed every two years."]) == 1.0


def test_rrf_prefers_consensus():
    fused = rrf_fuse([[("a", 9), ("b", 8)], [("b", 0.9), ("c", 0.8)]], k=60, top=3)
    assert fused[0][0] == "b"


def test_bm25_finds_gold():
    r = BM25Retriever(DOCS)
    res = evaluate_retriever(r, QS, ks=(1, 3))
    assert res["hit@1"] == 1.0 and res["mrr@3"] == 1.0


def test_hybrid_not_worse_than_bm25_at_3():
    dense = DenseRetriever(DOCS, LsaEncoder(dim=4))
    hyb = HybridRetriever([BM25Retriever(DOCS), dense], depth=5)
    assert evaluate_retriever(hyb, QS, ks=(3,))["hit@3"] == 1.0


def test_pipeline_and_llm_citation_filter():
    pipe = RAGPipeline(BM25Retriever(DOCS), DOCS, k=2)
    out = pipe.ask("What does fault code P0300 mean?")
    assert "misfire" in out["answer"] and out["cited"] == ["p5"]
    fake_llm = lambda prompt: "Random misfire [p5] [p99]"  # p99 is not in context → must be dropped
    a = LLMAnswerer(fake_llm)("q", [("p5", "x")])
    assert a.cited == ["p5"]
    assert ExtractiveAnswerer()("anything", []).text == "I don't know."


def test_chunker_overlap():
    text = " ".join(f"Sentence number {i} is here." for i in range(100))
    ch = chunk_text(text, max_words=50, overlap=10)
    assert len(ch) > 1 and all(len(c.split()) <= 60 for c in ch)


def test_service():
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient
    from ragkit.service import create_app
    c = TestClient(create_app(RAGPipeline(BM25Retriever(DOCS), DOCS, k=2)))
    assert c.get("/health").json() == {"status": "ok"}
    r = c.post("/ask", json={"question": "battery voltage weak?"}).json()
    assert r["retrieved"][0] == "p3" and "latency_ms" in r
