# Finite-element run evidence

Copied from the MOOSE run runtime by `tools/materialize_fe_evidence.py`.
Each `runs/<case>/` holds the deck (`input.i`), the recorded provenance
(`provenance.json`), the per-run analysis where one was produced
(`analysis.json`), the scalar history (`solution.csv`), the solver log
(`run.log`), and the reference comparison (`reference_comparison.csv`) only
for the cases whose deck solves the same reference-modulus quarter-domain
Mandel problem. `manifest.json` records per case whether `analysis.json` and
`reference_comparison.csv` are present and lists the intentionally unshipped
source-run outputs (`provenance_outputs_unshipped`); a `reference_note` in
each `analysis.json` whose analysis records `reference_comparable:false`
states why no Mandel-normalized metric is reported.

`mms-convergence.json` is the manufactured-solution convergence analysis and
`compute_mms_order.py` recomputes it. `manifest.json` lists SHA-256 digests.
These are force-controlled finite-load and manufactured-solution runs; the
rotated-anisotropy and partial-drainage cases are demonstrations, not
quantitative finite-deformation verification.
