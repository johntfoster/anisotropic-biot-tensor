# Stress-based reconstruction: current evidence and remaining work

> Historical record of the September 18 draft. The user rejected that
> reconstruction on September 19. It has been replaced by the weighted-stress
> derivation recorded in `weighted-stress-reconsideration.md`; current review
> status is in `reviews/README.md`. The earlier acceptance is not evidence
> for the replacement.

Updated 2026-09-18. See the final revision status and round-4 records below.

## Authoritative source inspected

The user-authorized nonlinear Biot implementation manuscript supplies the
scalar stress-based derivation. Its source file
`paper/sections/finite_deformation_biot.tex` has SHA-256
`89d0a307970c88d01bcdb25ba547d3f908a43a5c6240a034d6dc9bb1a4c949c2`.
Its bibliography `all.bib` has SHA-256
`47954bac64165fffec0ee9f23dcb8dddef25a542f91b3bf02f9948f85cb1fb90`.
These are provenance identifiers in the source repository; the present paper
has no build dependency on that repository. No source repository was edited.

Read the full elastic derivation, especially the drained/mineral logarithmic
stress laws, phase-stress trace, integration in distention and mineral volume,
scalar EOS, implicit Biot derivative, and finite unjacketed solution. Plastic
flow was excluded. The source's constitutive reevaluation and subsequent
mixture-reduction reconciliation notes were read in sequence; the latter
supersedes the earlier unresolved reduction.

## New reconstruction

`sections/stress_reconstruction.tex` prescribes drained and isolated-mineral
Hooke laws in material logarithmic strain. An explicit elastic series
assumption gives L = [Cd^-1 - (phi Hbar)^-1]^-1, provided phi Hbar - Cd is
positive definite. The internal mineral strain has six components; its shape
is not forced to follow the skeleton. Full mineral stationarity reduces to
q + phi s p exp(q) - r:E = 0. Here r = Cd:Hbar^-1:I/phi and
s = [phi tr(a) - a:Cd:a]/phi^2, a = Hbar^-1:I. The reduced energy is
E:Cd:E/2 + (q-r:E)^2/(2s). This gives the previous compatible scalar energy
from both prescribed stress laws under a stated localization assumption.

The derivation includes the noncoaxial matrix-log derivative, objective Biot
pressure tangent, reference stress/storage, exact finite unjacketed path,
and scalar source-law recovery. A critical limitation is explicit: equality
of logarithmic conjugate stresses is not equality of spatial Kirchhoff
stresses at general noncommuting states. The full phase-stress sum is proved
only in the stated commuting setting. The model is an objective internal-
strain elastic construction, not a microscopic localization theorem.
Assess this limitation in the fresh JMPS reviews; do not silently discard it
or claim a full spatial constituent law outside its demonstrated scope.

The abstract/introduction/conclusion now foreground reconstruction. Earlier
isotropic-distention daughter calculations remain as a diagnostic comparison.
The alternative volume-penalty energy is explicitly outside the reconstructed
series family. It preserves reference data but not the complete series and
mineral laws. The old independent reviews do not validate this revision.

## Verification performed

- `latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex`
  passes. No undefined references or overfull boxes remain. Four underfull
  table/paragraph warnings remain; no clipped text was seen on new pages.
- Rendered and visually inspected PDF pages 6–9 containing the new section.
  Final abstract/example/conclusion visual QA was subsequently completed.
- `examples/verify_reconstruction.py` passes using the numerics environment.
  Twenty seeded random anisotropic material pairs exercise noncommuting
  operators and six-component independent mineral minimization.
  Operator error 1.78e-14; energy error 8.36e-15; mineral-state/residual
  error 2.29e-9; pressure derivative error 2.18e-9; finite unjacketed error
  4.47e-14; isotropic source error 1.39e-13.
- The noncoaxial phase-sum discrepancy is deliberately exercised (maximum
  7.85e-4 in test units), supporting the explicit limitation rather than
  falsely claiming spatial equivalence.
- Existing `examples/verify_tensor.py` passes, including both finite-pressure
  energies, reference compatibility, objectivity, and sampled acoustic tests.
- `tools/agentctl route` and `tools/agentctl check --profile manuscript` were
  attempted. They cannot execute: the tracked symlink targets a missing
  shared submodule file. `.agent/shared/AGENTS.shared.md` is also absent.
  Direct `python3 tools/check_dependency_profile.py manuscript` passes.
  Do not change unrelated checkout/submodule edits merely to conceal this gap.

## Final revision status

The reference review is now recorded in
`references/notes/new-source-references-2026-09-18.md`. All 23 original new
keys are accounted for, with evidence levels, relevance, and explicit
full-text access gaps. Four verified background references and the explicitly
unpublished companion manuscript were added to the bibliography.

All example materials now pass the full tensor ordering check. README and
VISION describe the reconstructed model and the verification commands.
The phase-average/internal mineral stress distinction is explicit, and
trace preservation is proved and independently checked (error below 1.1e-13).

Three reviewer agents completed round 3 (ACCEPT, MINOR REVISION, MINOR
REVISION). Their requests were implemented and all three were asked to
review the current round-4 snapshot independently. All three returned ACCEPT,
with no mandatory revisions remaining. The authoritative final
verdicts are in `reviews/round-4/`; do not count old round-2 votes.
The source hashes, author response, and requirement-by-requirement audit
there supersede this progress note for final completion status.

The 24-page PDF has been rendered and visually inspected as a whole, with
changed derivation/example/conclusion pages additionally inspected at readable
resolution. No overfull boxes, undefined references, or clipping remain.
Both numerical suites and the direct manuscript dependency check pass.
The pre-existing unavailable shared agentctl remains a tooling limitation;
no user changes to submodule/hooks/configuration were overwritten.
