# Round 37 — launched (final round of the extended acceptance cycle)

Repository: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
Starting HEAD: `6d47dfc`; repair commit: `3144a68`.
Snapshot: `.agent-runtime/review-snapshots/round-37`
SNAPSHOT_ID: `0d75448ba758ff51c9f4e43423c120ffba6eaa1088442206436692c957fd2189`
Files: 608 (`missing []`)
Built artifact: `build/main.pdf`, 33 pages, sha256
`795826c3ed141007d674e159b7b0056b9a67cf3cf3988ed63d470e873ce832fb`, 0 overfull
boxes, 0 undefined references or citations, 0 missing-character warnings, 1 benign
underfull bibliography box, 106 numbered equations.

## What changed since round 36

Round-36 items only; no equation, number, data, or claim changed.

- R2-C1 — `site/evidence.json` now registers `fluid-coupling-verification`
  (path `site/reports/fluid-coupling-verification.json`), fixed at the owning
  generator `tools/populate_site_manifest.py` and regenerated, not hand-edited.
  `python3 tools/build_verification_site.py --validate-only` -> `{"manifest":
  "valid", "artifacts": 41, ...}`, exit 0.
- R2-O1 — `fe-evidence/README.md` `reference_note` sentence scoped to the
  `reference_comparable:false` set, edited at `tools/materialize_fe_evidence.py`
  and re-synchronised.
- R3-C1 — `main.tex` notation paragraph: the hat and the wide tilde are now
  partitioned on normalization (hat = mineral-normalized; wide tilde =
  mixture-normalized rotated into the true frame), not on frame.
- R3-C2 — `main.tex`: the "fixed-pressure" epithet now follows the mark;
  single prime carries the full pore-pressure term, double prime the reduced
  counterpart.

## Rules for this round

- Reviewers read the immutable snapshot, never the working tree, and never edit the
  manuscript. Each reviewer writes only `reviews/round-37/reviewer-{1,2,3}.md`, and must
  write it even if its budget runs short.
- **Do not open any file under `reviews/`.** Reading another reviewer's report invalidates
  that reviewer's vote; self-report any accidental exposure.
- Each reviewer confirms that `sha256(snapshot/source-manifest.json)` equals the declared
  SNAPSHOT_ID, re-hashes every listed file, and reports mismatches or missing files.
- Stable comment IDs with exact source locations; required changes separated from optional
  notes; exactly one verdict line: ACCEPT, MINOR REVISION, MAJOR REVISION or REJECT.
- Only an exact ACCEPT counts toward the gate; MINOR REVISION never counts.
- Held suites (`validation/`, `examples/verify_*.py`) are not run.
- SIMULATED AI PEER REVIEW, not journal acceptance.

## Complementary emphasis

1. Derivation and correctness.
2. Numerical verification and source fidelity.
3. Exposition, notation and claims.
