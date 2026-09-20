# Reviewer 3 — Round 18 (prose, notation, significance, claim discipline)

**Manuscript:** An anisotropic Biot tensor from mineral stress and distention work
**Snapshot:** round-18, SNAPSHOT_ID `810b503058701b0d3f43ef39cba2c6952e28a5e8b0728321849b0129a60e3625`
**Scope:** prose, notation, significance, claim discipline. Prior-round verdicts do not carry.

---

## 1. Snapshot integrity

- `sha256(source-manifest.json)` = `810b503058701b0d3f43ef39cba2c6952e28a5e8b0728321849b0129a60e3625`, equal to `SNAPSHOT_ID`. **Match.**
- Re-hashed all **438** listed files: **438 OK, 0 missing, 0 mismatch.**
- Reviewed only the frozen snapshot; no source, code, data, figure, or snapshot files were modified; nothing was committed or pushed.

## 2. Required correction: bar/hat convention (RESOLVED)

main.tex §2 now declares a complete convention, with four distinct rules:

1. *bar on a kinematic or energetic quantity* → mineral state reached by removing the distention (`\bar F`, `\bar J`, `\bar C`, `\bar U`, `\bar\varepsilon`, `\bar W_s`);
2. *bar on an intrinsic density* → per-phase-volume value `\bar\rho_\xi = \rho_\xi/\phi_\xi` (`\bar\rho_s`, `\bar\rho_{s0}`, `\bar\rho_f`, `\bar\rho_{f0}`);
3. *bar on a stress* → mixture-frame representation; *hat* → true frame (`\bar\sigma_s`, `\bar\tau_s` vs `\widehat\sigma_s`, `\widehat\tau_s`), with the rotation `\eqref{eq:rotated-mineral-cauchy}` called out as the difference;
4. *bar on a prescribed boundary datum* → its prescribed value on that boundary, e.g. the mass flux `\bar Q_f` of `\eqref{eq:fe-fluid-residual}`.

I enumerated every `\bar` and `\widehat` symbol in `main.tex` and all five `sections/*.tex` files and confirmed each one conforms to exactly one declared rule. The boundary-datum case is now explicitly covered (it was the previously required item) and the `\bar Q_f` vs `\mathbf Q_f` distinction (prescribed scalar datum vs referential mass-flux vector) is consistent with the weak balance in `\eqref{eq:fe-fluid-residual}` and the boundary statement `\mathbf Q_f\cdot\mathbf N = \bar Q_f`. No undeclared bar/hat usage survives.

## 3. Cross-reference and citation integrity

- **Labels:** 106 `\label` definitions; every referenced label (34 distinct tokens across `\ref`/`\eqref`/`\cref`, including `sec:`, `fig:`, `eq:` names) resolves. **0 dangling references.**
- **Citations:** 22 citation keys used; all 22 present in `references.bib`; **0 missing, 0 unused entries.** The `\cref{sec:logarithmic-derivative}` and `\eqref{...}` cross-references all point to defined targets.

## 4. Duplication check

A sentence-level exact-duplicate scan (threshold 60 chars) across `main.tex` + `sections/*.tex` found **0 duplicated sentences**. The abstract, introduction, and conclusion restate the verification scope in different wording, not as duplicated text.

## 5. Quantitative-claim discipline

Every quantitative claim was traced to a listed artifact:

| Claim in manuscript | Artifact | Value found | Match |
|---|---|---|---|
| "186 named checks" | `build/conformal/verification.json` | `checks_passed: 186` | ✓ |
| "65 per-state identities … five states × thirteen identities" + "two reference … relations" | same | `legacy_identities_rechecked: 67` (65+2) | ✓ |
| "largest absolute error … 2.5×10⁻⁹" | same | `max_constitutive_identity_error: 2.455×10⁻⁹` | ✓ |
| "second-order convergence" | same | `observed_orders.*` ≈ 2.00 (energy, pore volume, pressure) | ✓ |
| "273 finite states across 13 mineral stiffnesses" | `site/reports/tensor-verification.json` | `total_states: 273`, `materials: 13`, `states_per_material: 21` | ✓ |
| reference Biot components "0.7000, 0.7583, 0.7917" | `build/conformal/experiments.json` | `highlights.reference_B: [0.7, 0.758333…, 0.791666…]` | ✓ |
| mineral stiffness matrix (eq. `example-mineral-stiffness`) | same | `mineral_Mandel_stiffness` (50,12,10 / 12,60,14 / … shear 20,24,28) | ✓ |
| isotropic comparison μ=16.8K₊ | same | `isotropic_comparison.mu: 16.8` | ✓ |
| Mandel inputs φₛ₀=0.9, Kₛ=2.5, μₛ=5/6, K=1, K_f=8, k/μ_f=1.5 | `fe-evidence/runs/linear_load_reference/input.i` + `site/reports/mandel-reference.json` | `solid_fraction=0.9`, `drained_bulk=1`, `fluid_bulk=8`, `mobility=1.5`, mineral stiffness diagonal 3.6111/1.9444/shear 1.6667 ⇒ Kₛ=2.5, μₛ=5/6 | ✓ |
| drained shear G=0.75; reference Biot 0.6; total storage 17/80 | `mandel-reference.json` | `G: 0.75`, `alpha: 0.6`, `M: 4.70588… = 80/17` | ✓ |
| pressure discrepancy "floors at about 3.2×10⁻³ at nx=20, dt=10⁻³" | `fe-evidence/runs/nonlinear_load_0.0001/analysis.json` | `pressure_max_normalized: 3.2209×10⁻³`, config `nx=20, dt=0.001` | ✓ |
| ρ_f0=1 (fluid density default) | `moose_app/src/materials/ConformalMaterial.C` | `fluid_density` default 1 | ✓ |
| 121 / 161 / 121 sample counts in experiments | `build/conformal/experiments.json` `loading` | 121 / 161 / 121 / 121 | ✓ |

## 6. Significance and claim framing

The significance is stated honestly and in disciplined fashion. The abstract, the "Scope of these results" paragraph (`sections/finite_elements.tex`), and the conclusion all consistently bound the claims: manufactured-solution verification is asserted only for the **constant reference tangent**, the consolidation reference only in the **same limit**, and the rotated-anisotropy/partial-drainage runs are explicitly labeled **demonstrations**, not quantitative verification of the nonlinear law and not experimental validation. This matches `site/evidence.json` (`version: moose-fe-pending-…`, `limitations[]`) and `verification.json` `scope` ("no FE or physical validation"). No withdrawn statement survives in the snapshot.

## Minor observations (non-blocking)

- The bar carries two distinct meanings (mineral state for kinematics/energy vs mixture frame for stress) while the true-frame stress is hatted. This is a mild surface tension, but it is explicitly declared, motivated by `\eqref{eq:rotated-mineral-cauchy}`, and applied consistently; no correction is required.
- The conclusion's `3.2×10⁻³` floor sentence is worded precisely ("rather than decaying to it") and is backed by the artifact, so the honest framing is intact.

---

## VERDICT: ACCEPT

Required corrections:

1. *(none)*
