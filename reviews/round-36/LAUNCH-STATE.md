# Round 36 — launched (single confirmation round after the round-35 repairs)

Snapshot: `.agent-runtime/review-snapshots/round-36`
SNAPSHOT_ID: `c1f6210d5e2649986693d3dc0c26dccc072434c166148bbdc89e3f874ce4644d`
Files: 608 (`missing []`)
Working-tree HEAD at freeze: `f163561` (the round-35 required-item repair)
Built artifact: `build/main.pdf`, 34 pages, sha256
`980162471b9f0a118654eb7cda9ddbfe463887c294cac91160c460972f50c719`, 0 overfull
boxes, 0 undefined references or citations, 0 missing-character warnings, 1 benign
underfull bibliography box.

## What changed since round 35

All four required items of round 35, in one pass. No equation, symbol, label, citation,
number or claim changed; no other file's declared digest moved.

- `main.tex:257-260` — the wide-tilde rule now names its input a mixture-frame quantity and
  its output the true (mineral) frame, obtained by the inverse rotation `R_A^T`, matching its
  only instance `tau_tilde = R_A^T tau' R_A` (74) and eq. (6).
- `main.tex:221-223` — the undefined phase index is replaced by the explicit per-phase forms
  `rho_bar_s = rho_s/phi_s` (the mineral state) and `rho_bar_f = rho_f/phi_f`.
- `validation/equation_to_moose_map.yml:15` — `distention_stress` dropped from
  `FabricMaterial.produces`, because the compiled material declares no such property.
- `fe-evidence/manifest.json` `notes[0]`, edited at its generator
  (`tools/materialize_fe_evidence.py`) and re-synchronised from the generator's literal — the
  "intentionally not shipped" claim is now scoped to the source runs that omit those outputs,
  with the four `fabric_contour_*` Exodus files and sixteen `fabric_mandel_*` profile dumps
  named as the exceptions that do ship.

## Rules for this round

- Reviewers read the immutable snapshot, never the working tree, and never edit the
  manuscript. Each reviewer writes only `reviews/round-36/reviewer-{1,2,3}.md`, and must write
  it even if its budget runs short.
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
