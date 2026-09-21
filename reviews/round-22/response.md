# Round-22 response — single-writer revision pass

**Manuscript:** "An anisotropic Biot tensor from mineral stress and distention work"
**Repository:** `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
**Reviewed freeze:** `.agent-runtime/review-snapshots/round-21`
(SNAPSHOT_ID `f4c43aeea1590c8e166d3ffab342e5da92094443e55b4df4d47b69bbad8c673f`, 549 files)
**Source of items:** `reviews/round-21/reviewer-1.md` (MAJOR REVISION), `reviews/round-21/reviewer-3.md` (MINOR REVISION), `reviews/round-21/reviewer-2.md` (ACCEPT)

> Status note: this file contains only what was **actually executed in this session**;
> every number is the observed output of the command named beside it. Nothing under
> `.agent-runtime/review-snapshots/`, `reviews/round-19`, `reviews/round-20`, or
> `reviews/round-21` was modified. Three retained Foster prose edits in the working tree
> (abstract comma, conclusions "a discretization floor" removal, `sections/pore_fabric.tex`
> missing copula) were preserved.

---

## Path taken: REDUCTION (not restatement)

**Decision: reduce.** The implemented distention was cut to the axisymmetric subspace the
section actually states, rather than restating the section around a five-direction law.

Reason (all four defects close exactly at once, each numerically demonstrable):

| Property | Before (5 directions) | After (retained span(e1,e2)) |
| --- | --- | --- |
| `D:e3` (in-plane deviatoric) | `k_ip ≠ 0` | `1.58e-16` (zero) |
| `D:e6` (`sym(p1⊗p2)`) | `0` | `0` |
| Rotation invariance `‖R D Rᵀ − D‖`, 30° about `m` | `4.33e-1` (reviewer-1) | `2.50e-16` |
| `H` vs `h⁻²m⊗m + h(I−m⊗m)` | not of that form | `2.22e-16`, `det H − 1 = −3.3e-16` |
| eigenvalues of `H` | in-plane pair split | `{h⁻², h, h}` exactly |
| reported `ln_h` | an `e2` projection | exactly the unimodular eigenvalue ratio |
| rank of `D` on 6-D symmetric space | 5 (ill-posed along the omitted mode) | 2 on `span(e1,e2)`, frozen complement |

Fallback (keep the 5-direction law and rewrite the section) was **not** needed: the reduction
made every symmetry claim in the section true exactly, produced machine-precision evidence,
and left the headline Biot values (which are insensitive to the removed modes) unchanged.

---

## REQUIRED items

### MAT-1 — non-transverse-isotropic `D` described as "the five-modulus transversely isotropic D"

**Locations fixed.** `sections/pore_fabric.tex` (former lines 260–266, 308);
`moose_app/include/utils/FabricLaw.h` (basis + `dd` block);
`validation/equation_to_moose_map.yml` (`FabricMaterial`).

**Change.** `NDIR` reduced from 5 to 2. The distention stiffness is now the positive definite
`2×2` block `(k_v, k_a, k_c)` on `span(e1,e2)` and vanishes on the four complementary modes.
`fabric_inplane_modulus` and `fabric_shear_modulus` were removed from the law, from
`FabricMaterial`, and from both decks. The section now states that the retained `D` annihilates
*both* members of the coupled in-plane pair `e3`, `e6`, so it commutes with rotations about `m`,
and it drops every "five-modulus"/"frozen in-plane shear artifact" claim.

**Evidence (reproducible).** `python3 examples/verify_fabric.py` →
`D4_e3_norm = 1.58e-16`, `D4_e6_norm = 0.0`,
`rotation_invariance_norm = 2.50e-16` (30° about `m`). A zero at machine precision is the
transverse-isotropy condition `D:e3 = D:e6` that reviewer-1 showed was violated.

### MAT-2 — the transverse-isotropic special case and the reported `ln_h`

**Locations fixed.** `sections/pore_fabric.tex` (`eq:fabric-transverse-h`,
`eq:fabric-transverse-strain`, the former "two-parameter energy" sentence);
`sections/finite_elements.tex` (`fig:fe-fabric-probe` caption);
`FabricLaw.h` (basis and equilibrium).

**Change.** `E_dis` is now restricted to `span(e1,e2)` in the law, so
`H = exp(2(E_dis − (ln a/3)I))` is exactly `h⁻²m⊗m + h(I−m⊗m)`. The caption no longer claims
a negative-convention caveat; it states that the plotted scalar *is* the unimodular fabric
eigenvalue ratio. "two-parameter" was replaced by "retained volumetric--axial energy", and the
deck moduli are now three entries on two degrees of freedom (not five nominally independent ones).

**Evidence.** `python3 examples/verify_fabric.py` →
`H_reconstruction_max_abs_diff = 2.22e-16`, `H_det_minus_one = -3.33e-16`,
`H_eigenvalues = [0.999286354, 1.000357014, 1.000357014]` versus
`H_eigenvalue_ratio_expected = [0.999286354, 1.000357014, 1.000357014]`.
The three uncoupled probes now have **three different** `ln_h` (`−0.005`, `−0.0005`, `+0.004`)
and three correspondingly different `H` eigenvalue triples — the reported scalar is no longer
orientation-dependent while `H` is fixed.

### MAT-3 — unrestricted minimization with a rank-deficient `D`

**Locations fixed.** `sections/pore_fabric.tex` (former lines 243–266, and
`eq:fabric-equilibrium` paragraph).

**Change.** The text now states explicitly that `D` is symmetric and positive **semidefinite**
(positive definite on `range(D)`, zero on the complement), that the minimization in
`eq:fabric-equivalent-energy` is over `E_dis ∈ range(D)`, that the complementary modes are
kinematically frozen to the mineral, and that `eq:fabric-equilibrium` is read on that subspace.
`D⁻¹` was replaced throughout by the Moore–Penrose `D⁺`. The former blanket claim "`D` is the
positive definite distention stiffness tensor" is gone.

**Evidence.** `sections/pore_fabric.tex` `eq:fabric-compliance-restriction` now reads
`(C^d)^{-1} = (phi_s0 C_s)^{-1} + D⁺`; `python3 examples/verify_fabric.py` reproduces every
recorded probe field with the reduced (constrained) solve to `4.885e-15`, and the
conformal reduction `D ∝ I⊗I` is recovered to `1.874e-14` against the reviewed
`ConformalMaterial`.

### R3-1 — `d` meant both drained and distention, including inside one displayed equation

**Change.** All distention quantities were renamed in the manuscript: `W_dis`, `S_dis`,
`\bar S_dis`, `E_dis` (21 symbols across `sections/pore_fabric.tex`; 1 in `main.tex`).
`\mathbb C^d` stays drained. The symbol table in `main.tex` now states the convention
explicitly: a superscript `d` is the drained skeleton, the distention quantities carry the
subscript `dis`, and "the two labels are kept distinct throughout, so `d` never means
distention".

**Evidence.** `grep -n 'W_d\|E_d\|S_d\|_d\b' sections/pore_fabric.tex` returns no distention
symbol (only `\mathbb C^d` remains, once, in `eq:fabric-compliance-restriction`);
`grep -c '\mathrm{dis}' sections/pore_fabric.tex` = 21.

### R3-2 — `\mathbf t` was both a unit tangent and the reference traction

**Change.** `sections/experiments.tex`: the unit tangent is now `\mathbf e_t`
(equation `eq:experiment-plane-directions` and the following sentence, 3 occurrences).
`sections/finite_elements.tex` keeps `\mathbf t_0` for the reference traction.

**Evidence.** `grep -n 'mathbf t' sections/experiments.tex` → no match;
`grep -n 'mathbf t' sections/finite_elements.tex` → only `\mathbf t_0`.

### R3-3 — advertised FE verification with no in-manuscript display

**Change (displays added, preferred option).** Two new figures, built only from recorded
artifacts, are now in `sections/finite_elements.tex` and referenced from the conclusions:

* `fig:fe-verification` — four panels: (a) manufactured-solution spatial `L²` errors with the
  measured adjacent orders, (b) the fixed-mesh successive-difference temporal orders
  `nx=16/32/64`, (c) the linear step-refinement ratio, (d) the finite-load pressure floor.
* `fig:fe-reference-comparison` — (a) center-pressure history and (b) pressure profiles against
  the independently evaluated Mandel series at identical saved times.

Both are generated by a new script `examples/plot_fe_verification.py` (source hash recorded in
the scientific snapshot) from `figures/fe_mms_convergence.csv`,
`fe-evidence/mms-convergence.json`, `figures/fe_mandel_refinement.csv`,
`figures/fe_load_limit.csv`, `figures/fe_mandel_history.csv`, `figures/fe_mandel_profiles.csv`.
The two displays are registered in `site/evidence.json` (ids `fe-verification-convergence`,
`fe-reference-comparison`) and attached to the `convergence` category.

**Evidence.** `python3 examples/plot_fe_verification.py` → `{"figures": 2, "missing": []}`;
`figures/fe_verification_convergence.pdf` sha256 `12cdde8e…`, `figures/fe_reference_comparison.pdf`
sha256 `4d5a499c…`; `python3 tools/build_verification_site.py --validate-only` →
`{"manifest": "valid", "artifacts": 35}` and the full build reports `"link_check": "passed"`.

### R3-4 — temporal-order range without the companion's caveat

**Change.** `main.tex` conclusions now read: "the fixed-mesh successive-difference temporal
orders at `nx=16/32/64` are `0.98`–`1.40`, including values above one; these are measurements
from a sequence that retains a mesh-step cross term, and no order above one is asserted."
The values themselves are unchanged and reproduce `fe-evidence/mms-convergence.json`
(`difference_orders` span `0.978`–`1.397`).

### R3-5 — unscoped novelty claim

**Change.** `main.tex` now reads: "Among the fabric-elasticity and fabric-poroelasticity
constructions surveyed here, we are not aware of a tensorial distention law, a constitutive
relation stating how the shape and orientation of the pore space enter a finite-deformation
poromechanical energy and the Biot tensor derived from it."

---

## OPTIONAL items

### Applied

| ID | Source | Change |
| --- | --- | --- |
| OPT-1 | reviewer-1 | `validation/theory_traceability.yml` gained a `fabric_distention` block (equations, retained subspace, restriction, Biot form, verification numbers); `grep -c fabric` was `0`, now the block exists. |
| OPT-2 | reviewer-1 | Abstract now says the law "is implemented in its reference-state linearization and checked at the material point". |
| OPT-3 | reviewer-1 | Resolved by construction: `e4`/`e5` no longer exist in `FabricLaw.h`; the header documents only `e1`/`e2`, and the in-plane shear naming issue is gone. |
| O3-4 | reviewer-3 | Abstract now says the relaxation is "to a fabric-symmetric compliance supported on the retained volumetric--axial distention subspace". |
| O3-5 | reviewer-3 | The "not its negative" clause was dropped from the `fig:fe-fabric-probe` caption and replaced by the positive statement that the scalar is the unimodular eigenvalue ratio. |
| O3-6 | reviewer-3 | Conclusions: "a reaction-induced pore fabric **would** enter the poromechanical response". |
| OPT-3 (R2) | reviewer-2 | `section~experiments.tex` availability statement: "Those decks are inputs, not a runnable build: reproducing them requires the repository application build, whose remaining sources the archive does not ship." |
| OPT-1 (R2) | reviewer-2 | Supplement README: "The models are synthetic constitutive calculations, not physical validation or finite-element simulations. The archive additionally ships recorded finite-element run histories … those runs are demonstrations … not physical validation." |

### Deliberately skipped

| ID | Source | Reason |
| --- | --- | --- |
| O3-1 | reviewer-3 | Bar-accent overload. Each meaning is individually defined and reviewer-3 recorded it as "not a defect"; a notation table would be a larger restructure than this pass allows. |
| O3-2 | reviewer-3 | Three accents over `τ` in one section. The three frames are already defined at first use; I added no new accent use in this pass. Deferred as editorial. |
| O3-3 | reviewer-3 | The "full rank / zero eigenvalue" contradiction is removed by the reduction (explicit rank two on a retained subspace); no separate wording fix is needed. |
| O3-7 | reviewer-3 | Companion-site deployment URL. No rendered site is deployed in this checkout, so the path-based reference remains the honest choice. |
| OPT-2 (R2) | reviewer-2 | Deck runnability note. Applied instead via `experiments.tex` (see above), where the reader meets the claim. |
| OPT-3 (R2) | reviewer-2 | "verified" vs "checked against" in the abstract. The abstract's verification claim is now backed by `fig:fe-verification`, which states the `3.2e-3` floor explicitly; reviewer-2 flagged this as "editorial only". Left unchanged to avoid weakening a claim that is now demonstrated. |
| OPT-4 (R2) | reviewer-2 | Provenance pin wording. `site/evidence.json` already records the base revision and the note that it predates the working revision; unchanged in this pass. |

---

## Residual uncertainty for a fresh reviewer

1. **Reduction changes the coupled demonstration numbers, including their sign of trend.**
   The Mandel peak centre pressures changed from `6.28e-5 / 5.10e-5 / 3.95e-5` (0°/45°/90°,
   uncoupled reference `5.13e-5`) to `4.38e-5 / 4.98e-5 / 5.50e-5` (uncoupled reference
   `3.65e-5`). The ordering across orientations also reversed: the previous law peaked at 0°,
   the reduced law increases monotonically with the fabric angle. This is a real model change,
   not a numerical artifact, and it should be re-checked by an independent reviewer against the
   reduced constitutive law. The reference Biot components (`0.88387` uncoupled;
   `0.850654`/`0.910270` coupled) are unchanged, showing the removed modes did not affect the
   reference tensors.
2. **The retained subspace is a modeling choice**, not derived. The section now says so, but a
   reviewer may wish to argue for the four frozen modes or for a full-rank `D`.
3. **Only the reference-state linearization is implemented.** `FabricLaw::evaluate` still throws
   unless `linear_reference = true`; the general finite-deformation fabric equilibrium remains
   out of scope, as the abstract and `validation/equation_to_moose_map.yml` state.
4. **Figures were not visually inspected** (no vision model was reachable in this session); they
   were verified numerically (inputs, ranges, absent-signal lists) and the plotted source CSVs
   are registered artifacts.
5. **The supplement archive name was kept at `anisotropic-biot-2026-09-20-v2.zip`.** The contents
   changed with this revision but the paper version label did not, matching the practice of the
   preceding rounds; if a version bump is required, `main.tex` `\embedfile`, the packaging tool,
   and the README must be changed together.
