"""Sparse (BM25), dense (pluggable encoder) and hybrid retrieval fused with Reciprocal Rank Fusion.

BM25: Robertson & Zaragoza 2009, doi:10.1561/1500000019 · RRF: Cormack et al. 2009, doi:10.1145/1571941.1572114
"""
from __future__ import annotations

import re
import unicodedata
from typing import Protocol, Sequence

import numpy as np
from rank_bm25 import BM25Okapi
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

from .data import Passage

_STOP = set("a an the of to in on for and or is are was were be by with as at from that this it its which who what when where how why".split())


def tokenize(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return [t for t in re.findall(r"[a-z0-9]+", text) if t not in _STOP]


class Retriever(Protocol):
    def search(self, query: str, k: int = 10) -> list[tuple[str, float]]: ...


class BM25Retriever:
    def __init__(self, passages: Sequence[Passage], k1: float = 1.5, b: float = 0.75):
        self.ids = [p.pid for p in passages]
        self.bm25 = BM25Okapi([tokenize(f"{p.title} {p.text}") for p in passages], k1=k1, b=b)

    def search(self, query: str, k: int = 10) -> list[tuple[str, float]]:
        s = self.bm25.get_scores(tokenize(query))
        top = np.argsort(-s)[:k]
        return [(self.ids[i], float(s[i])) for i in top]


class Encoder(Protocol):
    def fit(self, texts: list[str]) -> "Encoder": ...
    def encode(self, texts: list[str]) -> np.ndarray: ...


class LsaEncoder:
    """CPU stand-in for a neural embedder: TF-IDF (word + char n-grams) → truncated SVD, L2-normalised."""

    def __init__(self, dim: int = 256, seed: int = 0):
        self.vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2, sublinear_tf=True)
        self.svd = TruncatedSVD(n_components=dim, random_state=seed)

    def fit(self, texts):
        self.svd.fit(self.vec.fit_transform(texts))
        return self

    def encode(self, texts):
        z = self.svd.transform(self.vec.transform(texts))
        return z / (np.linalg.norm(z, axis=1, keepdims=True) + 1e-12)


class SentenceTransformerEncoder:
    """[GPU recommended] e.g. 'BAAI/bge-m3' (Chen et al. 2024, arXiv:2402.03216). Needs sentence-transformers."""

    def __init__(self, name: str = "BAAI/bge-m3", device: str | None = None, batch_size: int = 32):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(name, device=device)
        self.bs = batch_size

    def fit(self, texts):
        return self

    def encode(self, texts):
        return np.asarray(self.model.encode(texts, batch_size=self.bs, normalize_embeddings=True, show_progress_bar=False))


class DenseRetriever:
    def __init__(self, passages: Sequence[Passage], encoder: Encoder):
        self.ids = [p.pid for p in passages]
        texts = [f"{p.title}. {p.text}" for p in passages]
        self.enc = encoder.fit(texts)
        self.mat = self.enc.encode(texts)

    def search(self, query: str, k: int = 10) -> list[tuple[str, float]]:
        s = self.mat @ self.enc.encode([query])[0]
        top = np.argsort(-s)[:k]
        return [(self.ids[i], float(s[i])) for i in top]


def rrf_fuse(rankings: Sequence[Sequence[tuple[str, float]]], k: int = 60, top: int = 10) -> list[tuple[str, float]]:
    """score(d) = Σ_r 1 / (k + rank_r(d)), rank starting at 1."""
    agg: dict[str, float] = {}
    for ranking in rankings:
        for rank, (pid, _) in enumerate(ranking, start=1):
            agg[pid] = agg.get(pid, 0.0) + 1.0 / (k + rank)
    return sorted(agg.items(), key=lambda x: -x[1])[:top]


class HybridRetriever:
    def __init__(self, retrievers: Sequence[Retriever], depth: int = 50, k_rrf: int = 60):
        self.retrievers, self.depth, self.k_rrf = list(retrievers), depth, k_rrf

    def search(self, query: str, k: int = 10) -> list[tuple[str, float]]:
        return rrf_fuse([r.search(query, self.depth) for r in self.retrievers], k=self.k_rrf, top=k)


class CrossEncoderReranker:
    """[GPU recommended] Re-score the top `depth` candidates of a base retriever with a cross-encoder
    (Nogueira & Cho 2019, arXiv:1901.04085). e.g. 'BAAI/bge-reranker-v2-m3' (GPU) or
    'cross-encoder/ms-marco-MiniLM-L-6-v2' (CPU smoke test)."""

    def __init__(self, base: Retriever, passages: Sequence[Passage], name: str, depth: int = 30, device: str | None = None):
        from sentence_transformers import CrossEncoder
        self.base, self.depth = base, depth
        self.text = {p.pid: f"{p.title}. {p.text}" for p in passages}
        self.model = CrossEncoder(name, device=device)

    def search(self, query: str, k: int = 10) -> list[tuple[str, float]]:
        cands = [pid for pid, _ in self.base.search(query, self.depth)]
        scores = self.model.predict([(query, self.text[pid]) for pid in cands], show_progress_bar=False)
        order = np.argsort(-np.asarray(scores))[:k]
        return [(cands[i], float(scores[i])) for i in order]
