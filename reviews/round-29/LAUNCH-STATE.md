# Round 29 — launched (fresh independent acceptance round on the current tree)

Snapshot: `.agent-runtime/review-snapshots/round-29`
SNAPSHOT_ID: `8aff33630cf27ac2727729471b38529c10f23edb1d6a5f90f2553c5b7f8726d7`
Files: 592 (`missing []`)
Working-tree HEAD at freeze: `97e862b30e176b8fa1f223abef9adfef78d4cfc3`
Built artifact: `build/main.pdf`, 34 pages, sha256 `6b49ce77d137c0f41e27b910428f4c4dc24569fbfd90762eb6d3a696df7b68f5`
Supplement: `build/anisotropic-biot-2026-09-20-v2.zip`, 69 files, sha256 `fa8c07a25f853dd96a6ef8f101ee8d5ef25650e2d746aaedd9b5b78bfad0146c`

## Why earlier rounds do not carry forward

No verdict from round-28 or earlier applies to this snapshot. The tree changed after the
round-28 freeze (pore-fabric prose, CI pin alignment, the four text items in `main.tex` /
`sections/experiments.tex` / `sections/finite_elements.tex` / `provenance/`, and the
`.latexmkrc`/`Makefile` export-recipe restoration), and this round's snapshot was frozen
from the current working tree. Counting only exact ACCEPT verdicts returned by reviewers
1–3 on the round-29 snapshot; **>=2 required**.

## What this round reviews

The complete self-contained repository as frozen in the round-29 snapshot: the manuscript
root `main.tex` and its includes, `references.bib`, the FE evidence tree, the numerical
supplement, the companion-site manifests, the provenance records, and the packaging tools.

## Rules for this round

- Reviewers read the immutable snapshot, never the working tree, and never edit the
  manuscript. Each reviewer writes only its own report file:
  `reviews/round-29/reviewer-{1,2,3}.md`.
- Reviewers must not read other reviewers' reports, prior-round verdicts, or any
  acceptance count.
- Each reviewer must confirm that `sha256(snapshot/source-manifest.json)` equals the
  declared `SNAPSHOT_ID`, re-hash every listed file, and report mismatches or missing
  files.
- Each reviewer must use stable comment IDs with exact source locations, separate
  required changes from optional notes, and end with exactly one verdict line:
  `ACCEPT`, `MINOR REVISION`, `MAJOR REVISION`, or `REJECT`.
- Reviewers may inspect and recompute quoted values from the frozen artifacts in a
  temporary copy, but must not modify the snapshot or the working tree and must not run
  the repository's held numerical suites (`validation/`, `examples/verify_*.py`).
- Label this exercise SIMULATED AI PEER REVIEW, not journal acceptance.

## Complementary emphasis

1. Derivation and correctness.
2. Numerical verification and source fidelity.
3. Exposition, notation and claims.

## Specific focus for this round

Confirm independently that (a) the round-29 snapshot re-hashes clean (all 592 entries);
(b) the pore-fabric construction described in `sections/pore_fabric.tex` is internally
consistent and matches its equations and the FE evidence; (c) every quoted number still
reproduces from the frozen artifacts; (d) the manuscript, `site/evidence.json`, and the
supplement archive agree (embedded attachment digest equals the on-disk archive digest);
(e) the build recipe declared by the standalone export manifest is present and correct.
