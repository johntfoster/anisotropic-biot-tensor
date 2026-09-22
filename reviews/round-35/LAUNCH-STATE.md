# Round 35 — launched (recovery round after the incomplete round 34)

Snapshot: `.agent-runtime/review-snapshots/round-35`
SNAPSHOT_ID: `3e56fad609d38c3a6dd65c10e6aff3959ec7deaff3c21ba2b86448074ad1d886`
Files: 608 (`missing []`)
Working-tree HEAD at freeze: `0120875` (the round-34 revision commit)
Built artifact: `build/main.pdf`, 34 pages, 0 overfull boxes, 0 undefined
references or citations, 0 missing-character warnings, 1 benign underfull
bibliography box.

## Reviewer run IDs

| Round | Reviewer 1 | Reviewer 2 | Reviewer 3 |
| --- | --- | --- | --- |
| 32 | `f119d90f-ded8-4125-a806-3215be947ca8` | `3597d8f1-b664-4c8a-95e1-88853e097fd1` | `01dbd200-f2cc-4a1e-814a-d3995394e252` |
| 33 | `556f67bc-da72-470e-b18f-0f6ab6a7c90b` | `b8f63d39-96b0-4a49-a8bc-55dcfd9a3d5c` | `cd69d1c5-69d6-41e4-a862-a9010a024849` |
| 34 | `5c869571-0576-490e-af78-2b59e4eac478` (NO REPORT) | `896d1afd-10ae-446a-b305-b17c667d6d5b` | `45ce6dd1-26a3-44e7-8021-8347e27073d4` |
| 35 | `2edd5888-8dad-4027-9427-7e138fccc392` | `440fd89c-6b20-44e9-a075-face12633e54` | `885de3b0-e2e8-43e9-a160-1e0b47fac637` |

Foster cycles (all in round 32): 1 `394a4597-6131-4894-bcfd-ac7ce311fbee`,
2 `6545bc4f-0fed-4a7b-a6bc-263884f04fc5`,
3 `f7a13604-31c8-4d85-88d1-3e1ac7a5adec`.

## Why round 34 does not carry forward, and why round 35 exists

**Round 34 is incomplete.** Reviewer 1 (`5c869571…`) settled with status ok but
produced **no report** — `reviews/round-34/reviewer-1.md` does not exist. The skill
treats a missing report as an incomplete round: it cannot be counted as acceptance and
must be recovered without being counted as acceptance. Its report path was checked
before any respawn, per the skill's stalled-child rule.

The two reports that exist are reviewer 2 **ACCEPT** (0 required) and reviewer 3
**MINOR REVISION** (3 required). All three required items are resolved in this round's
tree, and reviewer 3's report and reviewer 2's report are preserved unchanged in
`reviews/round-34/`.

Round 33 likewise met the gate but its fixes changed the tree, so no earlier verdict
carries forward. Counting only exact ACCEPT verdicts on the round-35 snapshot;
**>=2 required**. This round supplies the fresh derivation-and-correctness review that
round 34 failed to produce.

## What changed since round 34

- `main.tex` notation paragraph — completed as a class. It now states rules for the
  time-level superscript `n`, the reference-configuration subscript `0`, and the wide
  tilde (the true-frame quantity referred to the intermediate mineral frame by `R_A`,
  with the tilde relation of eq. (73) as the example). Fixed with it: the missing
  article before "solid intrinsic density", and the distant antecedent in "The two
  stress representations differ by the rotation" (now names the mixture-frame and
  true-frame representations).
- `sections/finite_elements.tex` — the two adjacent fabric figure captions no longer
  end in an identical sentence; the diffusion caption now refers to the contours
  figure instead of repeating the disclaimer verbatim.
- `sections/experiments.tex` — the duplicated listing of the reference Biot and
  rank-one compliance relations was removed from the second of two adjacent
  sentences, which now claims only the isotropic formula.

## Known facts a reviewer should not misread

- The Foster prose cycles changed no equation, symbol, label, citation, number or
  claim. The claim surface differs from HEAD `8d83726` only in reference arguments
  added by these revision rounds, never removed or retargeted.
- The Exodus field arrays are bit-identical across regenerations; the raw file digest
  moves with the run wall clock because the framework header echoes `Current Time: …`
  into the information records. Documented in the contour plot manifest's limitations
  and the supplement README. No declared digest is stale.
- `build/weighted-stress/derivation-scan.txt` is knowingly stale, shipped read-only as
  a historical triage record; it is not a claim about the current sources.
- The 38 runtime run records carry `git_revision` as the revision whose *tree* contains
  exactly their recorded source digests, with a companion `git_revision_basis` stating
  that weaker claim.
- `site/evidence.json` records the revision at the moment the site manifests were
  regenerated, not the snapshot HEAD.
- Two ignored copies of `fe_reference_comparison.pdf` and
  `fe_verification_convergence.pdf` exist in the working repository root; they are not
  shipped and not in the snapshot.

## Rules for this round

- Reviewers read the immutable snapshot, never the working tree, and never edit the
  manuscript. Each reviewer writes only `reviews/round-35/reviewer-{1,2,3}.md`, and
  must write it even if its budget runs short.
- **Do not open any file under `reviews/`.** Reading another reviewer's report
  invalidates that reviewer's vote; self-report any accidental exposure.
- Each reviewer confirms that `sha256(snapshot/source-manifest.json)` equals the
  declared SNAPSHOT_ID, re-hashes every listed file, and reports mismatches or missing
  files.
- Stable comment IDs with exact source locations; required changes separated from
  optional notes; exactly one verdict line.
- Held suites (`validation/`, `examples/verify_*.py`) are not run.
- SIMULATED AI PEER REVIEW, not journal acceptance.

## Complementary emphasis

1. Derivation and correctness (recovery of the missing round-34 seat).
2. Numerical verification and source fidelity.
3. Exposition, notation and claims — including whether the now class-complete notation
   rules leave any decoration uncovered or any clause unparseable.
