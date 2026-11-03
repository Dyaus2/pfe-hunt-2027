"""FastAPI service: POST /ask, GET /health. Logs latency per request (feed it to monitoring)."""
from __future__ import annotations

import logging
import time

from fastapi import FastAPI
from pydantic import BaseModel

log = logging.getLogger("ragkit")


class AskIn(BaseModel):
    question: str


def create_app(pipeline) -> FastAPI:
    app = FastAPI(title="RAG assistant")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/ask")
    def ask(body: AskIn):
        t0 = time.perf_counter()
        out = pipeline.ask(body.question)
        out["latency_ms"] = round((time.perf_counter() - t0) * 1000, 2)
        log.info("ask latency_ms=%s retrieved=%s", out["latency_ms"], out["retrieved"][:3])
        return out

    return app
