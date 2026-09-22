# Round 34 — launched (confirming round after the round-33 required fixes)

Snapshot: `.agent-runtime/review-snapshots/round-34`
SNAPSHOT_ID: `a2d99a3960d08ac9a8b1e9d333a0f77fb676a240b29e0ed528b9d1b308b3ea1e`
Files: 608 (`missing []`)
Working-tree HEAD at freeze: `caac406` (the round-33 revision commit)
Built artifact: `build/main.pdf`, 34 pages, 0 overfull boxes, 0 undefined
references or citations, 0 missing-character warnings, 1 benign underfull
bibliography box.

## Reviewer run IDs

| Round | Reviewer 1 | Reviewer 2 | Reviewer 3 |
| --- | --- | --- | --- |
| 32 | `f119d90f-ded8-4125-a806-3215be947ca8` | `3597d8f1-b664-4c8a-95e1-88853e097fd1` | `01dbd200-f2cc-4a1e-814a-d3995394e252` |
| 33 | `556f67bc-da72-470e-b18f-0f6ab6a7c90b` | `b8f63d39-96b0-4a49-a8bc-55dcfd9a3d5c` | `cd69d1c5-69d6-41e4-a862-a9010a024849` |
| 34 | `5c869571-0576-490e-af78-2b59e4eac478` | `896d1afd-10ae-446a-b305-b17c667d6d5b` | `45ce6dd1-26a3-44e7-8021-8347e27073d4` |

Foster cycles (all in round 32): 1 `394a4597-6131-4894-bcfd-ac7ce311fbee`,
2 `6545bc4f-0fed-4a7b-a6bc-263884f04fc5`,
3 `f7a13604-31c8-4d85-88d1-3e1ac7a5adec`.

## Why round 33 does not carry forward

Round 33 met the two-of-three gate (reviewer 1 ACCEPT, reviewer 2 ACCEPT, reviewer 3
MINOR REVISION on snapshot `7e75f419…`), but its third reviewer filed two required
items and this revision changed manuscript text, so acceptance does not carry across
the edit. Counting only exact ACCEPT verdicts on the round-34 snapshot; **>=2
required**.

## What changed since round 33

`reviews/round-33/` holds the reports; the dispositions are in the round-33 commit.
Both required items are fixed:

1. `sections/experiments.tex:191` — "spherical-gauge" was used once and defined
   nowhere in the manuscript. The sentence now names the suite by its function:
   "A separate tensor-verification suite checks 273 finite states across 13 mineral
   stiffnesses". The count is unchanged. Verified: the term now occurs 0 times in
   `main.tex` and every `sections/*.tex`.
2. `main.tex:228-229` — the bar rule introduced by the round-32 rewrite was a
   participial clause with no subordinator, reading as if the bar "is written on"
   the distention stress. It is now two sentences; the second opens "When the bar is
   written on the distention stress `S̄_dis` of (72) it instead marks…". The rule
   itself is unchanged.

Also applied, from the two accepting reviewers' completeness notes:

- `main.tex` after eq. (5): one sentence stating that an incompressible solid phase
  has constant intrinsic density, so `J̄ = ρ̄_s0/ρ̄_s = 1`, and that the present
  construction is the compressible generalization of that limit. The identity is a
  direct consequence of the displayed relation.
- `main.tex` notation paragraph: `W_A(a)` and `W_dis(G)` are now stated to be
  normalized per reference mixture volume.

Retained with reasons (recorded in the round-33 commit's process log): the
"kinematically frozen" wording (kept consistent across both uses), the large-axial-
modulus enforcement of the conformal limit (already reported honestly), the stale
read-only `derivation-scan.txt` record, and the unrecorded five deviatoric stiffness
modes.

**The notation paragraph has now been edited in three consecutive rounds.** Its
grammar and completeness are the primary focus of this round's exposition reviewer.

## Known facts a reviewer should not misread

- The Foster prose cycles (round 32) changed no equation, symbol, label, citation,
  number or claim; the claim surface differs from HEAD `8d83726` in exactly three
  reference arguments added by the round-32 response itself, and this round added
  one more (`eq:distention`, now referenced by the new incompressible sentence).
- The Exodus field arrays are bit-identical across regenerations; the raw file
  digest moves with the run wall clock because the framework header echoes
  `Current Time: …` into the information records. This is documented in the contour
  plot manifest's limitations and the supplement README. No declared digest is stale.
- `build/weighted-stress/derivation-scan.txt` is knowingly stale, shipped read-only
  as a historical triage record beside that revision's contact sheets.
- The 38 runtime run records carry `git_revision` as the revision whose *tree*
  contains exactly their recorded source digests, with a companion
  `git_revision_basis` stating that weaker claim.
- `site/evidence.json` records the revision at the moment the site manifests were
  regenerated, not the snapshot HEAD.
- Two ignored copies of `fe_reference_comparison.pdf` and
  `fe_verification_convergence.pdf` exist in the working repository root; they are
  not shipped and not in the snapshot.

## Rules for this round

- Reviewers read the immutable snapshot, never the working tree, and never edit the
  manuscript. Each reviewer writes only `reviews/round-34/reviewer-{1,2,3}.md`.
- **Do not open any file under `reviews/`.** Reading another reviewer's report
  invalidates that reviewer's vote; self-report any accidental exposure.
- Each reviewer confirms that `sha256(snapshot/source-manifest.json)` equals the
  declared SNAPSHOT_ID, re-hashes every listed file, and reports mismatches or
  missing files.
- Stable comment IDs with exact source locations; required changes separated from
  optional notes; exactly one verdict line.
- Held suites (`validation/`, `examples/verify_*.py`) are not run.
- SIMULATED AI PEER REVIEW, not journal acceptance.

## Complementary emphasis

1. Derivation and correctness.
2. Numerical verification and source fidelity.
3. Exposition, notation and claims — with explicit, sentence-by-sentence attention to
   the grammar and completeness of the thrice-revised notation paragraph.
