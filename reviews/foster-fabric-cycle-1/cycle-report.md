# Foster reviewer/editor cycle 1 — cycle report

Cycle: 1 of 3 (engineering reviewer / editor)
Manuscript: anisotropic Biot tensor from mineral stress and distention work
Repo: /home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor
Base snapshot: round-21 `f4c43aeea1590c8e166d3ffab342e5da92094443e55b4df4d47b69bbad8c673f`
Working tree: existing dirty tree (no history rewrite, no commit, no push).

## 1. Snapshot hash table

| File | round-21 manifest | pre-edit | differs (pre-edit) |
|------|-------------------|----------|--------------------|
| main.tex | 20faf47b…43343796 | 20faf47b…43343796 | no |
| sections/experiments.tex | a452cf5d…333b86 | a452cf5d…333b86 | no |
| sections/finite_elements.tex | ee24fa81…931c9f4 | ee24fa81…931c9f4 | no |
| sections/limits.tex | a8547e6d…91afd3 | a8547e6d…91afd3 | no |
| sections/logarithmic_derivative.tex | 9696e296…925f7b1 | 9696e296…925f7b1 | no |
| sections/stress_reconstruction.tex | ad50c93c…df593fe | ad50c93c…df593fe | no |
| sections/pore_fabric.tex | 2228a633…5cab546 | 2228a633…5cab546 | no |

Pre-edit result: **0 of 7 differ** (expected none).

Post-edit hashes (only the two edited files changed):
- main.tex → `c67c00b8a17aaf0ecaa314857f66fc99e95324996587804c1b87807254a5d334`
- sections/pore_fabric.tex → `31a5a9fc0b644fd698f7d49b17d08278a16122e1f3916c316dd29d7d24f4daf6`

## 2. Count integrity

| File | label | ref | cref | eqref | cite | begin{equation} | begin{align} |
|------|-------|-----|------|-------|------|-----------------|--------------|
| main.tex | 41 | 0 | 3 | 18 | 24 | 17 | 10 |
| sections/experiments.tex | 9 | 6 | 0 | 9 | 1 | 3 | 0 |
| sections/finite_elements.tex | 22 | 0 | 2 | 9 | 2 | 3 | 5 |
| sections/limits.tex | 9 | 0 | 0 | 4 | 1 | 5 | 1 |
| sections/logarithmic_derivative.tex | 7 | 0 | 0 | 1 | 0 | 2 | 2 |
| sections/stress_reconstruction.tex | 21 | 0 | 1 | 9 | 0 | 8 | 8 |
| sections/pore_fabric.tex | 25 | 0 | 5 | 28 | 2 | 16 | 2 |

Every column unchanged from counts-before.txt (verified programmatically).
Digit-literal multiset (all maximal digit runs) identical per file.

## 3. Edits applied (prose only)

1. main.tex abstract: comma added for grouping clarity
   ("fraction plus a" → "fraction, plus a").
2. main.tex conclusions: removed redundant "a discretization floor"
   ("The floor is a discretization floor attributable to…" → "The floor is
   attributable to…").
3. sections/pore_fabric.tex: supplied missing copula
   ("and its eigenvectors the fabric axes" → "and its eigenvectors are the
   fabric axes").

Full rationale in disposition.md and memo.md.

## 4. Explicit list of what was NOT changed

- No equation, symbol, label, `\ref`/`\cref`/`\eqref`/`\cite`, number, or claim
  changed anywhere.
- No change to any digit literal (verified per file).
- `sec:fabric-transverse` and all wording around the standing author decision
  (volume--axial distention modulus carries `B_par != B_per`; isotropic mineral
  alone keeps `B` spherical) left verbatim.
- No edits to the forbidden paths: moose_app/, validation/, figures/, site/,
  fe-evidence/, references.bib, tools/, or anything under .agent-runtime/
  (read-only).
- No edits to the duplicated "implementation check" caveat in `sec:fe-fabric`,
  the abstract triple-"and" scope sentence, `Figure~\ref{…}` vs `\Cref{…}`
  style, or any elliptical parallelism (see disposition.md reasons).
- No commit, no push, no history rewrite; single writer throughout.

## 5. Build

Command:
`latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex`
(log: reviews/foster-fabric-cycle-1/build.log)

- Exit code: **0**
- Pages: **28** (letter)
- Undefined references: **none**
- Undefined citations: **none**
- Overfull boxes: **0**
- `git diff --check`: clean

Page images rendered: reviews/foster-fabric-cycle-1/page-01.png … page-28.png
(pdftoppm -r 90 -png).
