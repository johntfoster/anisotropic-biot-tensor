# Foster reviewer/editor cycle 3 (final, round-27 tree) — memo (findings)

Manuscript: anisotropic Biot tensor from mineral stress and distention work
Repository: /home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor
Base snapshot: round-27 `c5050c77dd04628f149ddc417cce99eb6b53c4315884974efc6331c3267eda5e`
(3/3 exact ACCEPT, zero required corrections; 591-file manifest)
Working tree: existing dirty tree (no history rewrite, no commit, no push).
Single writer throughout (`pgrep -af 'opencode run'` returned no writer at start).

## What this cycle was

The final editorial prose pass, run against the CURRENT tree rather than the
superseded round-24 tree the two earlier `foster-r24-cycle-{1,2}` records
targeted. The tree advanced through rounds 25/26/27 (the `ln h` description
fix, the fabric-axis symbol definition, the `exp(2E_dis)` reconstruction, and
the companion-site registration repair), so this cycle re-reads the seven
manuscript sources cold on the round-27 content.

## Concurrent-writer check (passed)

`pgrep -af 'opencode run'` (and `pgrep -af opencode`) returned no writer
process at start, so this cycle is the single writer. No second writer
appeared during the cycle (file mtimes were checked before and after the
read/build; no source changed except by this cycle's none).

## Snapshot integrity (pre-edit)

The seven manuscript sources are byte-identical to the round-27 manifest
(0/7 differ) — see snapshot-hash-table.txt. This confirms the working tree
holds exactly the accepted round-27 text, with the cycle-1 edit
("transversely isotropic") and the round-25 `ln h`/fabric-axis fixes already
present. Notably `sections/pore_fabric.tex` differs from the round-24 cycle
records (`7c35f667…` vs `98184b99…`) and `sections/finite_elements.tex` from
its round-24 pre-edit form (`f254a8c2…` vs `2b111db8…`), exactly the expected
round-25/26/27 revisions.

## Prose findings (read cold, zero edits)

A fresh independent read of all seven sources found no high-value
authorial/editorial improvement that was not already settled by the earlier
cycles or that would not constitute churn. Confirmed clean:

- No repeated words, no filler phrases ("in order to", "the fact that", "it
  should be noted", "due to the fact", "note that"), no `its`/`it's` misuse
  (all occurrences are the possessive "its"), no "principal"/"principle"
  error, uniform "distention" (no "distension").
- No development-note markers (TODO/FIXME/XXX/NOTE/placeholder), no
  unresolved `??` reference markers in source.
- Consistent authorial "we/our" voice throughout; no "I"/"my" drift.
- The cycle-1 terminology edit is retained: "transversely isotropic" appears
  five times (once in conclusions, four in `sec:pore-fabric`), and the
  non-standard "transverse-isotropic" is absent.
- The round-25 `ln h` description fix is present and correct: the reported
  shape scalar is the logarithm of the unimodular transverse fabric
  eigenvalue `\(h=\mathrm{e}^{\ln h}\)`, and the phrase "eigenvalue ratio"
  no longer occurs. The `exp(2E_dis)` reconstruction
  `\(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G=a^{2/3}\mathbf H\)` with
  unimodular eigenvalues `\(h^{-2},h,h\)` is present and consistent.
- The fabric-axis symbol `\(\mathbf m\)` is defined as the unit material
  fabric axis in `sec:fabric-biot` and re-stated in `sec:fabric-transverse`.
- The standing author decision (`sec:fabric-transverse`: the volume--axial
  distention modulus carries `B_par != B_per`; an isotropic mineral alone
  keeps `B` spherical) is intact and not reverted.

One alignment-whitespace run inside a math `cases` block
(`sections/logarithmic_derivative.tex:36`, column-aligned `&`) is not a
prose defect; prior cycles declined trailing-whitespace normalization as
churn, and this instance is inside a display, not prose. Left untouched.

## Deliberately left unchanged (settled, not revisited)

- US/UK spelling mix (`center`/`centre`, `colour`, `modelling`) — declined
  in cycle 1, record only.
- Twice-stated "implementation check, not independent derivation" caveat in
  `sec:fe-fabric` — declined in cycle 1, record only.
- Elliptical parallelism in `sec:fabric-energy` ("…carries the volume
  response and its deviatoric part the shape response") and
  `sec:fabric-equilibrium` ("…that is, depend only on…") — declined, record only.
- The "and at small strain" qualifier and the triple-"and" scope sentence —
  declined, claim-bearing, record only.
- `Figure~\ref` → `\Cref` normalization in `sec:experiments` — declined
  (would change `\ref`/`\cref` counts), record only.

## Verification performed

- sha256 of all seven sources matched the round-27 manifest (0/7 differ)
  before editing — see snapshot-hash-table.txt.
- Counts and digit-literal multisets unchanged before vs after (re-run
  verify_integrity.py; `diff` of the before/after verifier output is empty)
  — see counts-before.txt, counts-after.txt, cycle-report.md.
- Build: exit code, pages, undefined refs/citations, overfull boxes — see
  cycle-report.md and build.log.
