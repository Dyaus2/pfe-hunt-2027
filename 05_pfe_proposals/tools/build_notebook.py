"""Build a self-contained Colab notebook from a proposal's src/ package and execute it on CPU.

Each src file is embedded as a %%writefile cell, so the notebook runs in Colab without cloning
this (private) repo and never drifts from the tested code.

Usage: python tools/build_notebook.py <proposal_dir> [--no-exec]
The proposal dir must contain code/src/<pkg>/ and code/notebooks/cells.py defining
TITLE, PIP, CELLS (list of ("md"|"code", source)).
"""
import importlib.util
import sys
import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def build(proposal: Path, execute: bool = True) -> Path:
    code = proposal / "code"
    spec = importlib.util.spec_from_file_location("cells", code / "notebooks" / "cells.py")
    cells_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cells_mod)

    nb = nbformat.v4.new_notebook()
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.metadata["accelerator"] = "GPU"
    add = nb.cells.append
    add(nbformat.v4.new_markdown_cell(cells_mod.TITLE))
    add(nbformat.v4.new_code_cell(f"# Setup (Colab or local). CPU is enough unless a cell says [GPU — Colab T4].\n"
                                  f"%pip install -q {cells_mod.PIP}"))
    pkg_dirs = sorted(p for p in (code / "src").iterdir() if p.is_dir() and not p.name.startswith("__"))
    mk = ["import os, sys", "os.makedirs('src', exist_ok=True)"]
    sub = sorted({f.parent for d in pkg_dirs for f in d.rglob("*") if f.is_file()} | set(pkg_dirs))
    mk += [f"os.makedirs('{x.relative_to(code).as_posix()}', exist_ok=True)" for x in sub if "__pycache__" not in x.parts]
    mk += ["sys.path.insert(0, os.path.abspath('src'))"]
    add(nbformat.v4.new_markdown_cell("## Package source (embedded from `code/src/`, identical to the tested files)"))
    add(nbformat.v4.new_code_cell("\n".join(mk)))
    for d in pkg_dirs:
        for f in sorted(d.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts and f.suffix in (".py", ".json", ".jsonl", ".md", ".txt"):
                rel = f.relative_to(code)
                add(nbformat.v4.new_code_cell(f"%%writefile {rel.as_posix()}\n{f.read_text(encoding='utf-8')}"))
    for kind, src in cells_mod.CELLS:
        add(nbformat.v4.new_markdown_cell(src) if kind == "md" else nbformat.v4.new_code_cell(src))

    out = code / "notebooks" / f"{proposal.name}_colab.ipynb"
    if execute:
        with tempfile.TemporaryDirectory() as tmp:
            NotebookClient(nb, timeout=1800, kernel_name="python3", resources={"metadata": {"path": tmp}}).execute()
    nbformat.write(nb, out)
    return out


if __name__ == "__main__":
    p = Path(sys.argv[1]).resolve()
    print("wrote", build(p, execute="--no-exec" not in sys.argv))
