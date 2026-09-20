# Response to round 3

Round 3 reviewed the new stress-based reconstruction, not the older accepted
energy-only formulation. Verdicts: ACCEPT, MINOR REVISION, MINOR REVISION.
All reports are independent simulated reviews, not journal decisions.

## Reviewer 1

Accepted the mathematics. Implemented the optional branch clarification:
mineral minimization is stated globally for nonnegative pressure and locally
on the stable branch for negative pressure. The unconstrained negative-pressure
potential is not claimed globally bounded below.

## Reviewer 2

Clarified that N is an effective internal mineral strain. Added the distinct
actual phase-average stress inferred from mixture balance and the internal
mineral stress obtained by pushing forward the prescribed mineral Hooke law.
Their difference is explicitly a phase-average localization limitation, not
merely a question of uniform stress in individual grains. Added and proved
trace preservation of the logarithmic stress push-forward; the scalar
phase-stress trace therefore remains exact even when the full noncoaxial
phase-stress sum does not. The numerical trace discrepancy is below 1.1e-13.

## Reviewer 3

The tensor verification now checks positive definiteness of H - Cd for each
compatible anisotropic example. All three minimum eigenvalues equal 4 K_* to
rounding. The text explicitly connects those examples to the new tensor
series realization. README now documents verify_reconstruction.py next to
verify_tensor.py, and distinguishes build-time table generation from
independent tests. The optional axial/compliance symbol rename was not needed
for correctness; each is defined in its own context.

## Literature and scope

Completed an evidence-level review of all 23 new bibliography entries, recorded
in references/notes/new-source-references-2026-09-18.md. Retrieved four
additional full texts and copied the source library's available PDFs locally.
The revised introduction cites verified Hencky skeleton and microstructural
localization precedents. Conclusions distinguish mineral acoustic measurements
from a constant logarithmic energy Hessian. The scalar companion manuscript is
cited explicitly as an unpublished manuscript, not confused with Foster–Xu 2025.
No plastic constitutive law is imported.

Original full texts for several historical/comparison entries remain unavailable;
the audit identifies exactly which entries were screened only at abstract or
metadata level. No detailed equation or priority claim is based on those sources.
This completes the requested inventory review at the available evidence levels,
not an exhaustive priority certification or a claim of universal full-text access.

## Checks

Both numerical scripts pass. The reconstruction pressure error is 2.18e-9;
full mineral minimization discrepancy is 2.29e-9; scalar recovery is 1.39e-13;
finite unjacketed error is 4.47e-14. The noncoaxial spatial phase-sum discrepancy
is nonzero as disclosed, while its trace is negligible. Existing pressure,
energy, rotation, and sampled acoustic checks pass unchanged.

LuaLaTeX/latexmk build passes. Overfull boxes were corrected. Shared agentctl
remains unavailable due to the pre-existing missing submodule target; direct
manuscript dependency checking passes. The revised source requires round-4
reviews; round-3 verdicts are not carried forward automatically.
