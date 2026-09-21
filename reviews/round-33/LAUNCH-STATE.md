# Round 33 — launched (final independent re-review of the post-Foster tree)

Snapshot: `.agent-runtime/review-snapshots/round-33`
SNAPSHOT_ID: `7e75f419a105318fb1bec98caa19469a63f34efd25d41b79fb8ae055f37e3e53`
Files: 608 (`missing []`)
Working-tree HEAD at freeze: `a0e268c` (the round-32 revision commit)
Built artifact: `build/main.pdf`, 33 pages, 0 overfull boxes, 0 undefined references
or citations, 0 missing-character warnings, 1 benign underfull bibliography box.

## Why round 32 does not carry forward

Round 32 met the gate (reviewer 1 ACCEPT, reviewer 2 ACCEPT, reviewer 3 MINOR
REVISION on snapshot `2231ed2b…`), but this is the **post-Foster** tree: three
Foster engineering-review cycles revised prose in seven files after acceptance.
Acceptance does not carry across editorial edits, so this round is a fresh
independent re-review on a new snapshot. Counting only exact ACCEPT verdicts on the
round-33 snapshot; **>=2 required**.

Round-32 run IDs: reviewer 1 `f119d90f-ded8-4125-a806-3215be947ca8`,
reviewer 2 `3597d8f1-b664-4c8a-95e1-88853e097fd1`,
reviewer 3 `01dbd200-f2cc-4a1e-814a-d3995394e252`.
Foster cycles: 1 `394a4597-6131-4894-bcfd-ac7ce311fbee`,
2 `6545bc4f-0fed-4a7b-a6bc-263884f04fc5`,
3 `f7a13604-31c8-4d85-88d1-3e1ac7a5adec`.

## What changed since round 32

`reviews/round-32/response.md` records every disposition. Two required items from
reviewer 3, both notation defects:

1. `main.tex` notation paragraph — the prime rules now cover the reduced energies
   `W''` (44) and `W'` (45) as well as the stresses; the rule for the bar on
   `S̄_dis` now says the bar marks the conjugate-`G` member of the work-conjugate
   pair (not the intermediate frame, which the unbarred `S_dis` shares); and the
   distention glossary now names the scalar volume-only energy `W_A(a)`.
2. `sections/pore_fabric.tex` — the uniqueness argument is now scoped to the
   reference quadratic model in §7.4 and stated once, with §7.5 giving only the
   positive-definiteness condition `𝔻+φ_{s0}ℂ_s ≻ 0`.

Also applied: the contour plot manifest's limitations and the supplement README now
document the Exodus wall-clock residual.

Then **three Foster prose cycles** revised prose in seven files
(`main.tex`, `sections/{experiments,finite_elements,limits,logarithmic_derivative,pore_fabric,stress_reconstruction}.tex`).
Each cycle carries a machine-checked prose-only proof, and I independently verified
against HEAD that the claim surface — every label, ref, cite and numeric literal —
differs in **exactly three reference arguments, all added by the round-32 response
itself** (`eq:reduced-energy`, `eq:legendre-energy`, `sec:work-equivalence`), with
**zero** changes from any Foster cycle.

## Known facts a reviewer should not misread

- The prose changed but no claim, equation, label, citation, number or symbol did.
  If you believe a prose edit changed a claim, that is a required finding.
- The Exodus field arrays are bit-identical across regenerations, but the raw file
  digest moves with the run wall clock: the MOOSE framework header
  (`Current Time: …`) is unconditionally echoed into the Exodus information records
  and cannot be suppressed. This is now documented in
  `figures/fe_fabric_contours-plot-manifest.json` and the supplement README. No
  declared digest is stale: the manifest is regenerated from the produced artifacts
  in the same ordered pipeline and re-verified by
  `tools/check_figure_manifests.py`.
- `build/weighted-stress/derivation-scan.txt` is knowingly stale and shipped as a
  read-only historical triage record beside that revision's contact sheets; it is
  not a claim about the current sources. Recorded as such in the round-32 response.
- The 38 runtime run records carry `git_revision` as the revision whose *tree*
  contains exactly their recorded source digests, with a companion
  `git_revision_basis` field stating that this is the revision whose sources match,
  not necessarily the revision the run was made from.
- Two ignored copies of `fe_reference_comparison.pdf` and
  `fe_verification_convergence.pdf` exist in the working repository root; they are
  not shipped and not in the snapshot.
- `site/evidence.json` records the revision at the moment the site manifests were
  regenerated, not the snapshot HEAD.

## Rules for this round

- Reviewers read the immutable snapshot, never the working tree, and never edit the
  manuscript. Each reviewer writes only `reviews/round-33/reviewer-{1,2,3}.md`.
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

1. Derivation and correctness — including whether the Foster prose edits preserved
   every claim.
2. Numerical verification and source fidelity.
3. Exposition, notation and claims — including whether the revised prose reads as
   one voice and whether the notation rules are now complete.
