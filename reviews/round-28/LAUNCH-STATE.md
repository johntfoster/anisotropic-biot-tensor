# Round 28 — launched (confirmation round after the FabricLaw.h documentation repair)

Snapshot: `.agent-runtime/review-snapshots/round-28`
SNAPSHOT_ID: `229ce2a5106738159e18a889f5c99fbce66f0d5f9dfbb3955df46797e19d3124`
Files: 591 (`missing []`)

## Why round 27 does not carry forward

Round 27 returned **2 exact ACCEPT + 1 MINOR REVISION** (reviewer-1 `ACCEPT`,
reviewer-2 `ACCEPT`, reviewer-3 `MINOR REVISION`), so the >=2 threshold was met, but
reviewer-1's single required item was a real, shipped documentation defect that earlier
prose sweeps had missed because the offending phrase was line-wrapped:

> `moose_app/include/utils/FabricLaw.h` lines 19–20 described the reported `ln_h` as
> "the unimodular fabric eigenvalue ratio" — false, and it contradicted both the
> corrected manuscript text and `site/evidence.json`. The file ships inside the
> PDF-embedded supplement archive.

That file changed, so the tree no longer matches the round-27 snapshot and no round-27
vote carries forward. Counting only exact ACCEPT verdicts on the round-28 snapshot;
>=2 required.

## What changed since round 27

**One required documentation repair plus one thrice-flagged naming item. No manuscript
body prose, no equation, no number, no figure, and no computed quantity changed.**

1. **REQUIRED (round-27 reviewer-1).** `moose_app/include/utils/FabricLaw.h`: the
   trailing sentence now reads "…with h = exp(ln h), so the reported ln_h IS the
   logarithm of the unimodular **transverse fabric eigenvalue h**", matching the
   manuscript and `site/evidence.json`. The string "eigenvalue ratio" now occurs **0**
   times anywhere in the shipped tree outside `reviews/` and `.agent-runtime/`.
2. **OPTIONAL (flagged by round-25/26 reviewer-2 and round-27 reviewer-3).**
   `examples/verify_fabric.py`: report key `H_eigenvalue_ratio_expected` →
   `H_eigenvalues_expected` (the value is the eigenvalue triple `[h^-2, h, h]`, not a
   ratio). `build/fabric/fabric-verification.json` regenerated; all values byte-for-byte
   identical apart from the key name.

### Rebuild verification

- The **executable** `moose_app/anisotropic_biot-opt` is **byte-identical** after the
  rebuild (sha256 `ff0272fc279fcf91f6acd0c4a2e0ce436e8b165ad68b15549c27e6845dfdd31e`),
  which is the artifact every recorded run executed, so all recorded FE results are
  unchanged and remain faithful to their provenance records.
- Observed and worth recording: the auxiliary `libanisotropic_biot-opt.so.0.0.0`
  digest is **not reproducible across rebuilds even with no source change** (three
  consecutive builds gave `9636d01a…`, `89714344…`, `cdd1ebf6…` with identical inputs;
  the recorded executable digest never moved). The library digest stored in
  `fe-evidence/runs/*/provenance.json` is therefore build-id noise, not a
  falsifiable claim; the library is not shipped in the archive and is not digest-pinned
  anywhere in `fe-evidence/manifest.json`.
- `build/fabric/fabric-verification.json` regenerated (`verify_fabric.py` exits 0; worst
  probe-field absolute difference 4.885e-15; reconstruction 2.2e-16).
- Supplement archive rebuilt: `build/anisotropic-biot-2026-09-20-v2.zip`, 69 files,
  sha256 `fa8c07a25f853dd96a6ef8f101ee8d5ef25650e2d746aaedd9b5b78bfad0146c`.
- Companion site regenerated in the documented order
  (`populate_site_manifest.py` → `register_fabric_evidence.py` → `build_verification_site.py`):
  `site/evidence.json` **41 artifacts / 13 figures / 5 cases**;
  `site/scientific-snapshot.json` **47 files**; **0 digest mismatches** in either;
  link check **passed**.
- Manuscript rebuilt: `latexmk -lualatex -g … -outdir=build main.tex`, exit 0,
  **33 pages**, **0 undefined references**, **0 undefined citations**, **0 overfull
  boxes**; `build/main.pdf` sha256
  `d1d84bac1ee6a4b17be7f87b44ad4f8cd65ac666fa51f41ba9cda08e15635265`; the embedded
  attachment re-extracts to the new archive digest `fa8c07a2…`.

## Rules for this round

- Prior rounds (18–27) reviewed earlier snapshots and do not carry forward.
- Counting only exact ACCEPT verdicts on the round-28 snapshot; >=2 required.
- Three fresh independent reviewers, complementary emphasis:
  (1) mathematics/correctness; (2) physics/source fidelity/packaging;
  (3) prose/notation/significance.
- Reviewers must not read other reviewers' reports or prior-round verdicts, and must not
  modify the snapshot or the working tree (work from a temporary copy).
- Reports: `reviews/round-28/reviewer-{1,2,3}.md`, each ending with a `VERDICT:` line.

## Specific focus for this round

Confirm independently that (a) the round-28 snapshot re-hashes clean, all 591 entries;
(b) the `FabricLaw.h` documentation repair is present and the phrase "eigenvalue ratio"
occurs nowhere in the shipped tree; (c) the header comment, the manuscript, and
`site/evidence.json` now agree on what `ln_h` is; (d) the executable `anisotropic_biot-opt`
is byte-identical to the round-27 tree, so every quoted number still reproduces; (e) the
rebuilt archive, site manifests, and PDF are internally consistent (embedded attachment
digest equals the on-disk archive digest).
