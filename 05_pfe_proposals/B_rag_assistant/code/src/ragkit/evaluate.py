"""Retrieval metrics (hit@k, MRR@k), answer metrics (SQuAD EM/F1) and a cheap groundedness proxy."""
from __future__ import annotations

import re
import string
import time
from collections import Counter
from typing import Sequence

import numpy as np

from .data import Query


def hit_at_k(ranked: Sequence[str], gold: str, k: int) -> float:
    return float(gold in list(ranked)[:k])


def reciprocal_rank(ranked: Sequence[str], gold: str, k: int = 10) -> float:
    for i, pid in enumerate(list(ranked)[:k], start=1):
        if pid == gold:
            return 1.0 / i
    return 0.0


def evaluate_retriever(retriever, queries: Sequence[Query], ks=(1, 3, 5, 10)) -> dict:
    kmax = max(ks)
    hits = {k: [] for k in ks}
    rr, lat = [], []
    for q in queries:
        t0 = time.perf_counter()
        ranked = [pid for pid, _ in retriever.search(q.question, kmax)]
        lat.append(time.perf_counter() - t0)
        for k in ks:
            hits[k].append(hit_at_k(ranked, q.gold_pid, k))
        rr.append(reciprocal_rank(ranked, q.gold_pid, kmax))
    out = {f"hit@{k}": float(np.mean(v)) for k, v in hits.items()}
    out[f"mrr@{kmax}"] = float(np.mean(rr))
    out["p95_latency_ms"] = float(np.percentile(lat, 95) * 1000)
    out["n_queries"] = len(queries)
    return out


def _norm(s: str) -> str:
    s = s.lower()
    s = "".join(ch for ch in s if ch not in set(string.punctuation))
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    return " ".join(s.split())


def exact_match(pred: str, golds: Sequence[str]) -> float:
    return float(any(_norm(pred) == _norm(g) for g in golds))


def f1(pred: str, golds: Sequence[str]) -> float:
    best = 0.0
    p = _norm(pred).split()
    for g in golds:
        gt = _norm(g).split()
        common = Counter(p) & Counter(gt)
        same = sum(common.values())
        if same == 0:
            continue
        prec, rec = same / len(p), same / len(gt)
        best = max(best, 2 * prec * rec / (prec + rec))
    return best


def groundedness(answer: str, contexts: Sequence[str]) -> float:
    """Share of answer content tokens found in the retrieved contexts (proxy; use an LLM judge in the PFE)."""
    a = [t for t in _norm(answer).split() if len(t) > 2]
    if not a:
        return 1.0
    ctx = set(_norm(" ".join(contexts)).split())
    return sum(t in ctx for t in a) / len(a)
