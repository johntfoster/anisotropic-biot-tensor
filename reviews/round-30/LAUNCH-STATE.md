# Round 30 — launched (fresh independent round after the round-29 revision)

Snapshot: `.agent-runtime/review-snapshots/round-30`
SNAPSHOT_ID: `ade4ec319cd757abad15546bd307efe2d9f85b2df21aa075bd74fb9ba4f0658b`
Files: 592 (`missing []`)
Working-tree HEAD at freeze: `b6d72721414a0c09aa6492465acd3a4c8d07e31b`
Built artifact: `build/main.pdf`, 34 pages, 0 overfull boxes, 0 undefined references or citations
Supplement: `build/anisotropic-biot-2026-09-20-v2.zip`, 69 files, sha256 `fa8c07a25f853dd96a6ef8f101ee8d5ef25650e2d746aaedd9b5b78bfad0146c`

## Why round 29 does not carry forward

Round 29 returned three MINOR REVISION verdicts and **0 exact ACCEPT**, so it did not meet the
>=2 criterion, and the revision changed scientific and notation content. No round-29 verdict is
counted here. Counting only exact ACCEPT verdicts on the round-30 snapshot; **>=2 required**.

Round 29 also recorded an independence incident: reviewer 1 self-reported reading roughly the
first 70 lines of `reviews/round-29/reviewer-3.md`. Its return was not counted as an independent
vote, and round 30 uses a fresh reviewer 1.

## What changed since round 29

Six required corrections, all recorded in `reviews/round-29/response.md`:

1. `sections/pore_fabric.tex` — the transverse-isotropy sentence no longer claims the two
   annihilated modes imply invariance under rotations about the fabric axis; it gives the true
   reason (`e_1` and `e_2` are invariant) and names all four annihilated complementary modes.
2. `figures/fe-verification-plot-manifest.json` — regenerated with
   `python3 examples/plot_fe_verification.py`, so every declared input and output digest resolves
   and the `versions` block matches the other two figure manifests.
3. `main.tex` and `sections/stress_reconstruction.tex` — the drained energy is renamed `W^d`
   (was `W_dr`), one drained token throughout.
4. `main.tex` — the bar convention now records the intermediate-frame, reference-mixture-volume
   meaning of the distention stress.
5. `main.tex` abstract — now states that the pore-fabric orientation is prescribed material data
   and that no relative fabric–mineral rotation is represented.
6. `main.tex` abstract and discussion — "separate re-implementation … that shares their modelling
   conventions" replaces "independent re-implementation".

Also applied: the figure caption now reads "entries above unity" (demonstrated understatement).
Eleven optional readability notes were retained unapplied, with reasons, in the round-29 response.

## Known facts a reviewer should not misread

- `site/evidence.json` records `source_revision` `97e862b…`, the HEAD at the moment the site
  manifests were regenerated; the current HEAD is `b6d7272…`. The manifest's own note says the base
  commit predates the working revision. The FE runs carry their own recorded `git_revision`
  `ab46ebe…`, which is when those runs were executed.
- The two regenerated figure images differ from the superseded rendering in under one percent of
  pixels, all in text rasterisation; the plotted data, axes and annotations are unchanged.

## Rules for this round

- Reviewers read the immutable snapshot, never the working tree, and never edit the manuscript.
  Each reviewer writes only `reviews/round-30/reviewer-{1,2,3}.md`.
- **Do not open any file under `reviews/`.** The round rules are in each reviewer's own task.
  Reading another reviewer's report invalidates that reviewer's vote; self-report any accidental
  exposure.
- Each reviewer confirms that `sha256(snapshot/source-manifest.json)` equals the declared
  SNAPSHOT_ID, re-hashes every listed file, and reports mismatches or missing files.
- Stable comment IDs with exact source locations; required changes separated from optional notes;
  exactly one verdict line.
- Held suites (`validation/`, `examples/verify_*.py`) are not run.
- SIMULATED AI PEER REVIEW, not journal acceptance.

## Complementary emphasis

1. Derivation and correctness.
2. Numerical verification and source fidelity.
3. Exposition, notation and claims.
