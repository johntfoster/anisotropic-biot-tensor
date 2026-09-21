#!/usr/bin/env python3
"""Cycle-3 integrity verification.

Reads the seven manuscript sources and prints:
  - per-file sha256 (must equal snapshot-hash-table.txt pre-edit values)
  - per-file fixed-string counts for \\label/\\ref/\\cref/\\eqref/\\cite/
    \\begin{equation}/\\begin{align
  - per-file sorted multiset of maximal digit runs (hash + count)

Method is byte-for-byte identical to the cycle-2 verifier, so the cycle-3
before/after numbers can be compared directly against the cycle-2 report.

No writes."""
import hashlib, re
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
