# Round 23 — launched

Independent review round on the anisotropic pore-fabric extension tree frozen
after the round-22 revision pass (reduction of the implemented distention to the
axisymmetric subspace `span(e1,e2)`, `NDIR` 5→2) and after this watcher
independently re-verified the tree.

Snapshot: `.agent-runtime/review-snapshots/round-23`
SNAPSHOT_ID: `53af8afca869198eb1560733c6b9f0377accc0570d36b9dcbeddecc36142ddc5`
Files: 556

## Why round-22 does not count

The round-22 snapshot (`.agent-runtime/review-snapshots/round-22`,
SNAPSHOT_ID `68f3859a2c3f4ccaf73443f26869b0b86d3bf9b87cb18657365013687f55985d`)
was frozen at 21:14 local while the single-writer revision pass (runId
`9f6ff21a-7bba-4ea4-8040-6260a60237cc`, 21:08–21:21) was still writing. It
therefore captured an intermediate state. Reviewer 2 of round 22 reported MAJOR
REVISION against that intermediate state, and reviewers 1 and 3 produced no
report at all. Round-22 is **void**; none of its verdicts carry forward.

Watcher re-verification of the **current** tree (2026-09-21 ~02:40Z), read-only:

- `fe-evidence/manifest.json`: 293/293 digests match on disk, 0 bad, 0 missing.
- `site/evidence.json`: 35/35 artifacts match.
- `site/scientific-snapshot.json`: 43/43 files match.
- `moose_app/include/utils/FabricLaw.h` on disk shows `NDIR = 2`; the copy inside
  `build/anisotropic-biot-2026-09-20-v2.zip` is byte-identical (`2953669c…`), and
  `examples/verify_fabric.py` inside the archive is byte-identical to the on-disk
  file (`d6265788…`).
- `pdfdetach -saveall build/main.pdf` yields a zip with SHA-256
  `bf99380c…`, identical to the on-disk archive.
- `sections/finite_elements.tex` quotes the regenerated peak pressures
  (`4.38 / 4.98 / 5.50 / 3.65 ×10⁻⁵`); no "five-modulus" / "full rank" /
  "two-parameter" wording remains in `sections/pore_fabric.tex`.
- `build/main.pdf`: 32 pages.

Every required correction listed in `reviews/round-22/reviewer-2.md` is therefore
already closed on the frozen round-23 tree.

## Rules for this round

Prior rounds (18–22) reviewed earlier snapshots and do not carry forward.
Counting only exact ACCEPT verdicts on the round-23 snapshot; >=2 required.

Reviewers: 3 fresh independent, complementary emphasis
(mathematics/correctness; physics/source fidelity/packaging; prose/notation/
significance). Reports: `reviews/round-23/reviewer-{1,2,3}.md`.

Reviewers must not read other reviewers' reports or prior-round verdicts.
