# Round 32 — launched (fresh independent round after the round-31 revision)

Snapshot: `.agent-runtime/review-snapshots/round-32`
SNAPSHOT_ID: `2231ed2b9825fef48f1015be1b9b2a230c09bec424ad18a9ca8f32c5d0e8fa44`
Files: 608 (`missing []`)
Working-tree HEAD at freeze: `8d83726` (the round-31 revision commit)
Built artifact: `build/main.pdf`, 33 pages, 0 overfull boxes, 0 undefined references or
citations, 0 missing-character warnings. Supplement:
`build/anisotropic-biot-2026-09-20-v2.zip`, 69 files,
sha256 `ab993ee75fd3e087e19114fed9d3cc50996b587b908472e5ac96bcfdb5ee4d04`.

## Why round 31 does not carry forward

Round 31 returned one exact ACCEPT and two MINOR REVISION on snapshot
`09a606a7…`, so it did not meet the two-of-three criterion. The round-31 revision
changed scientific content (two notation cross-references, a uniqueness
justification, a float-placement change, regenerated contour evidence and completed
run provenance), so no round-31 verdict is counted here. Counting only exact ACCEPT
verdicts on the round-32 snapshot; **>=2 required**.

## What changed since round 31

`reviews/round-31/response.md` records every disposition. Summary of the
required items:

1. `figures/fe_fabric_contours-plot-manifest.json` recorded stale `input_sha256`
   values for the four contour Exodus files. Fixed at the process root:
   `tools/rerun_fabric_contours.py` now runs the decks with a relative output base
   (so the Exodus `title` is the stable string `solution.e`, not a temporary host
   path), regenerates the figure data and the plot manifest *after* the decks, and
   re-verifies them; the new `tools/check_figure_manifests.py` re-hashes every
   declared digest in every `figures/*-plot-manifest.json` from disk.
2. `main.tex` notation paragraph: the single-prime rule retargeted from
   `eq:constitutive-kirchhoff-phase-stress` (renders (12)) to
   `eq:total-cauchy-single-prime` (renders (8)); the double-prime rule retargeted
   from `eq:cauchy-pressure-tangent` (renders (55)) to
   `eq:fixed-pressure-stress` (renders (46)) and `eq:finite-biot-tensor`
   (renders (49)).
3. `sections/pore_fabric.tex`: the uniqueness argument now covers the mineral term
   in addition to the distention potential, in both §7.4 and §7.5.

Also applied: the six §9 figures changed from `[t]` to `[htbp]` (citation-to-caption
lag falls from 2–4 pages to 1–2; page count 34 → 33); the 38 runtime provenance
records now carry `git_revision` plus an explicit `git_revision_basis`, so all 57
run records carry revision + source + binary digests; `README.md`/`Makefile` document
the reproduction order (`make figures`).

## Known facts a reviewer should not misread

- The Exodus **field arrays** are bit-identical across regenerations, but the raw
  file digest still moves with the run wall clock, because the MOOSE framework
  header (`Current Time: …`) is unconditionally echoed into the Exodus information
  records and cannot be suppressed from the deck or the command line. The manifest is
  regenerated from the produced artifacts in the same ordered step and re-verified, so
  this does not make any declared digest stale. `README.md` states this.
- `tools/record_run_revisions.py` writes `git_revision` for the 38 runtime records as
  the revision whose *tree* contains exactly the recorded `source_sha256` digests,
  verified through the git object database. The companion `git_revision_basis` field
  states that this is the revision whose sources match, **not** necessarily the
  revision the run was made from. That weaker claim is deliberate and disclosed.
- Two ignored copies of `fe_reference_comparison.pdf` and
  `fe_verification_convergence.pdf` exist in the working repository root. They are not
  part of the snapshot and are not shipped artifacts. The figure plot manifests resolve
  bare figure basenames against `figures/`, which is where the shipped figures are.
- `site/evidence.json` records the `source_revision` at the moment the site manifests
  were regenerated, which is the revision recorded there, not necessarily the frozen
  snapshot's HEAD. The manifest's own note says so.
- Every quoted finite-element number is unchanged from the round-31 snapshot.

## Rules for this round

- Reviewers read the immutable snapshot, never the working tree, and never edit the
  manuscript. Each reviewer writes only `reviews/round-32/reviewer-{1,2,3}.md`.
- **Do not open any file under `reviews/`.** Reading another reviewer's report
  invalidates that reviewer's vote; self-report any accidental exposure.
- Each reviewer confirms that `sha256(snapshot/source-manifest.json)` equals the
  declared SNAPSHOT_ID, re-hashes every listed file, and reports mismatches or
  missing files.
- Stable comment IDs with exact source locations; required changes separated from
  optional notes; exactly one verdict line.
- Held suites (`validation/`, `examples/verify_*.py`) are not run; the contour decks
  were re-run only as part of the evidence regeneration, not as a scope exercise.
- SIMULATED AI PEER REVIEW, not journal acceptance.

## Complementary emphasis

1. Derivation and correctness.
2. Numerical verification and source fidelity.
3. Exposition, notation and claims.
