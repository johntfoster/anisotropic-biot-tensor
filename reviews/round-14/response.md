# Round-14 author response

Snapshot `061a92feee93641668978ab0ecec033d0b9fe0d20ad74efbcb9ec0bf1a60ea69`
(441 files; all three reviewers independently verified
`SNAPSHOT_ID == sha256(source-manifest.json)` and re-hashed all 441 listed
files). Verdicts: reviewer-1 MINOR REVISION, reviewer-2 MINOR REVISION,
reviewer-3 MINOR REVISION — 0 ACCEPT, so a further round is required.

No reviewer reported a wrong factor, a sign error, an unreproducible number,
or a false scientific pass. Every required correction below was applied and
verified before refreezing.

## reviewer-1 (mathematics and correctness)

R1-F1 **Jacobian step-refinement evidence (required) — RESOLVED at the source.**
The three `jacobian_*` runs were genuinely byte-identical: the varied option
`-mat_fd_coloring_err` is reported unused, so no FD step study existed.
`moose_app/scripts/check_jacobian.py` now runs each step with
`-snes_test_jacobian -snes_mf_operator` and `-mat_mffd_err` = 1e-4, 1e-5, 1e-6,
which PETSc does consume, and each run writes a machine-readable
`analysis.json` recording `fd_perturbation`, the three reported
`||J - Jfd||_F/||J||_F` values, the maximum, the contract target, and the pass
flag. The three runs are no longer byte-identical (`solution.csv` and `run.log`
all differ). Recorded maxima: 2.38892e-07 (1e-4), 2.38797e-07 (1e-5),
2.39529e-07 (1e-6), all below the 1e-6 contract target. A wider sweep of the
perturbation from 1e-2 to 1e-10 held the reported difference inside
2.39e-7 +/- 4e-9 with no trend, which is recorded in each `analysis.json`; in
that range the measured difference is not limited by the difference step.

R1-F2 **`reference_comparable` and the normalized fields (required) — RESOLVED.**
`moose_app/scripts/analyze_mandel.py` now sets comparability from the deck
itself: only `case = 'mandel'` decks solve the reference-modulus quarter-domain
problem (`phi_s0=0.9`, `K=1`, `isotropic_stiffness(2.5,5/6)`). The
rotated-anisotropy (`DEFAULT_CS`, `phi_s0=0.6`, `K=7`), isotropic-comparison
(`isotropic_stiffness(28,16.8)`, `phi_s0=0.6`, `K=7`) and partial-drainage
(square domain) decks are now `reference_comparable = false`, emit no
Mandel-normalized field, delete any stale `reference_comparison.csv`, and carry
a `reference_note` naming the material/geometry mismatch.
`site/evidence.json` no longer publishes the withdrawn normalized ranges; the
`finite_deformation` category now publishes measured per-run diagnostics from
the new listed artifact `site/reports/finite-deformation-summary.json` and
points at it from `evidence` and from the two demonstration cases.

R1-F3 (optional) **Convergence wording — ADDRESSED.** The convergence summary
now states that the measured successive-difference orders, including ux about
1.4, belong to that mesh/step sequence and are not asserted as the scheme's
order.

## reviewer-2 (physics/source fidelity and packaging completeness)

R2-R1 (F2) **`linear_coarse` provenance (required) — RESOLVED at the source.**
The run was regenerated from the shipped application, so its recorded
`source_sha256` (including `moose_app/include/utils/ConformalLaw.h` =
`ca18175b...613c`) and `binary_sha256` (`ff0272fc...d31e`) now match the
shipped sources; the superseded copy is retained under
`.agent-runtime/moose-fe-goal-2026-09-20/superseded/`. `tools/materialize_fe_evidence.py`
now fails loudly if any recorded source digest does not match a shipped source.

R2-R2 (F1) **Declared-but-unshipped digests (required) — RESOLVED by
disclosure.** `fe-evidence/manifest.json` now carries `runs[]` with per case
`analysis_present`, `reference_comparison_present`, `provenance_outputs_total`,
`provenance_outputs_unshipped`, and `binary_sha256`, plus a `notes` block
recording that each `provenance.json` enumerates the complete output set of the
source run while only the curated subset ships (the Exodus `solution.e` and the
per-step `solution_profile_*.csv` dumps are intentionally unshipped because of
size), and that `binary_sha256` refers to the compiled application, which is not
shipped.

R2-R3 (F3) **README versus shipped tree (required) — RESOLVED.**
`fe-evidence/README.md` now qualifies the contents ("the per-run analysis where
one was produced"), documents the per-case presence flags and the unshipped
output list, and notes that a `reference_note` in each non-comparable
`analysis.json` explains the omitted metrics. All 38 case directories now ship
an `analysis.json`, including the three Jacobian decks.

F4 (informational, absolute runtime paths) — the paths remain provenance
references to the recorded command lines; the README and manifest now name the
runtime-relative origin of the evidence.

## reviewer-3 (prose, notation, significance, claim-versus-artifact)

R3-F1 **Availability sentence over per-case contents (required) — RESOLVED at
the source.** All 38 `fe-evidence/runs/<case>/` directories now contain
`analysis.json` (the three Jacobian decks included), so the shipped sentence
"each case directory holds its input deck, run provenance, per-run analysis, and
scalar history" is true of the shipped tree; `fe-evidence/README.md` and
`fe-evidence/manifest.json` record the per-case presence explicitly.

R3-F2 **Bar notation (required) — RESOLVED.** The Section 2 convention now
reads: a bar on a kinematic or energetic quantity denotes the mineral state; a
bar on an intrinsic density denotes the per-phase-volume value
`\bar\rho_\xi = \rho_\xi/\phi_\xi`, which is the mineral state for the solid; a
bar on a mass-flux measure denotes its referential normalization; a bar on a
stress denotes its mixture-frame representation, and a hat the true frame. This
covers `\bar Q_f` and `\bar\rho_f` explicitly.

R3-F3 **Constant-tangent qualifier in abstract/roadmap (required) — RESOLVED.**
The abstract now reads "verified against a manufactured solution of the constant
reference tangent", and the roadmap reads "verify the implementation against a
manufactured solution in the constant reference tangent and, in the same limit,
the constant-coefficient consolidation reference", matching the FE section and
the conclusions.

R3-F4 **Unbacked finite-deformation numbers (required) — RESOLVED.**
`site/reports/finite-deformation-summary.json` is generated from the recorded
per-run `analysis.json` files (it refuses to emit if any demonstration run still
carries a comparable flag), is listed in `artifacts[]`, and is referenced from
`categories.finite_deformation.evidence` and from the rotated-anisotropy and
partial-drainage cases. The category no longer quotes Mandel-normalized ranges.

R3-F5 (optional) — the suite description now reads "65 rotation, virtual-work,
and volume-response checks (five states times thirteen per-state identities)
plus the two reference Biot and rank-one compliance relations".

R3-F6 (optional) — the conclusions now name the metric and discretization:
"normalized pressure discrepancy floors at about 3.2e-3 at nx=20, dt=1e-3".

## Rebuild and verification

- Re-ran the three Jacobian decks and `linear_coarse` with the shipped
  application; re-analyzed all `case = 'mandel'`-family runs from the recorded
  `solution.csv` (no solver rerun for the others).
- Regenerated the seven FE figures from the recorded runs.
- Rebuilt `build/main.pdf`: 22 pages, 0 undefined references/citations.
- Rebuilt the site (`tools/build_verification_site.py`): 23 artifacts, link
  check passed; `site/test_builder.py` 12 passed.
- Froze round-15 snapshot and launched three fresh independent reviewers; prior
  verdicts do not carry.

No change to the constitutive law, the weak forms, the kernels, or any verified
number.
