#!/usr/bin/env python3
"""Cycle-2 integrity verification: confirm zero edits preserved counts and
digit-literal multiset. Reads the seven manuscript sources and prints:
  - per-file sha256 (must equal snapshot-hash-table.txt pre-edit values)
  - per-file grep -oF counts for label/ref/cref/eqref/cite/begin{equation/begin{align
  - per-file sorted multiset of maximal digit runs (for manual cross-check)
No writes."""
import hashlib, re, sys
from pathlib import Path

FILES = [
    "main.tex",
    "sections/experiments.tex",
    "sections/finite_elements.tex",
    "sections/limits.tex",
    "sections/logarithmic_derivative.tex",
    "sections/stress_reconstruction.tex",
    "sections/pore_fabric.tex",
]

def counts(text):
    keys = ["\\label", "\\ref", "\\cref", "\\eqref", "\\cite",
            "\\begin{equation}", "\\begin{align}"]
    return [text.count(k) for k in keys]

def digit_multiset(text):
    return sorted(m.group() for m in re.finditer(r"\d+", text))

def main():
    for f in FILES:
        data = Path(f).read_bytes()
        text = data.decode()
        h = hashlib.sha256(data).hexdigest()
        c = counts(text)
        dm = digit_multiset(text)
        print(f"== {f}")
        print(f"  sha256={h}")
        print(f"  counts(label,ref,cref,eqref,cite,begin_eq,begin_align)={c}")
        print(f"  digit-run multiset hash={hashlib.sha256('|'.join(dm).encode()).hexdigest()}")
        print(f"  digit-run count={len(dm)}")

if __name__ == "__main__":
    main()
