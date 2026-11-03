"""Minimal file-based model registry with champion promotion and rollback (swap for MLflow in the PFE)."""
from __future__ import annotations

import json
import time
from pathlib import Path

import joblib


class ModelRegistry:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.meta_path = self.root / "registry.json"
        self.meta = json.loads(self.meta_path.read_text()) if self.meta_path.exists() else {"versions": [], "champion": None, "history": []}

    def _save(self):
        self.meta_path.write_text(json.dumps(self.meta, indent=2))

    def register(self, model, metrics: dict, tags: dict | None = None) -> int:
        v = len(self.meta["versions"]) + 1
        joblib.dump(model, self.root / f"model_v{v}.joblib")
        self.meta["versions"].append({"version": v, "metrics": metrics, "tags": tags or {}, "created": time.time()})
        self._save()
        return v

    def load(self, version: int):
        return joblib.load(self.root / f"model_v{version}.joblib")

    @property
    def champion(self) -> int | None:
        return self.meta["champion"]

    def promote(self, version: int, reason: str = "") -> None:
        self.meta["history"].append({"from": self.meta["champion"], "to": version, "reason": reason, "t": time.time()})
        self.meta["champion"] = version
        self._save()

    def rollback(self, reason: str = "") -> int | None:
        """Restore the champion that preceded the current one."""
        for h in reversed(self.meta["history"]):
            if h["to"] == self.meta["champion"] and h["from"] is not None:
                self.promote(h["from"], reason=f"rollback: {reason}")
                return h["from"]
        return None
