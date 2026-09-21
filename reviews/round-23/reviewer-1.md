# Round-23 independent review — Reviewer 1 (mathematics / correctness)

Frozen snapshot: `.agent-runtime/review-snapshots/round-23`
Declared `SNAPSHOT_ID`: `53af8afca869198eb1560733c6b9f0377accc0570d36b9dcbeddecc36142ddc5` (556 files)
All paths below are relative to that snapshot.

## 0. Integrity

- `sha256(source-manifest.json)` = `53af8afca869198eb1560733c6b9f0377accc0570d36b9dcbeddecc36142ddc5`, identical to the declared SNAPSHOT_ID. OK.
- Re-hashed every one of the 556 listed files against the manifest: **556 OK, 0 missing, 0 mismatch.**
- Integrity passes; the review proceeds on the frozen bytes.

## 1. What I re-derived independently (not trusting the artifacts)

I re-derived each item from the manuscript equations and then checked it against the shipped code/scripts and the recorded runs. I ran `examples/verify_fabric.py` and `examples/verify_conformal.py` myself (from a writable copy against the snapshot's recorded `fe-evidence/runs`).

1. **Distention kinematics.** `A = R_A G^{1/2}`, `G = a^{2/3}H`, `det H = 1` (sections/pore_fabric.tex:15-23, 76-84 and eqs. `fabric-distention-polar`, `fabric-tensor`). Verified: `det G^{1/2} = a`, `F = A F̄`, `C̄ = a^{-2/3}C` reduces to `spherical-distention`/`conformal-mineral-metric`.
2. **Retained basis.** `e1 = I/√3`, `e2 = √(3/2)(m⊗m − I/3)` (pore_fabric.tex:290-294; FabricLaw.h:414-424). Verified by hand in the Mandel (= Frobenius) metric that `|e2| = 1` (`|m⊗m − I/3| = √(2/3)`) and that `{e1,e2}` is orthonormal; the constructor also enforces this (FabricLaw.h:426-431). Verified the identity `1/2 I − 3/2 m⊗m = −√(3/2) e2`, hence `E_dis = (ln a/3)I + ln h(1/2 I − 3/2 m⊗m)` (eq. `fabric-transverse-strain`, pore_fabric.tex:320-323) and `exp(2 E_dis) = a^{2/3}[h^{-2}m⊗m + h(I−m⊗m)] = G`, with `det H = h^{-2}·h·h = 1` and eigenvalues `{h^{-2},h,h}` (eq. `fabric-transverse-h`, pore_fabric.tex:307-309). Because `tr e2 = 0`, `ln a = √3 x1` is exact; and `ln h = −x2/√1.5` is the sign/basis convention of FabricLaw.h:559-571. So the reported `ln_h` **is** the unimodular eigenvalue ratio, not a projection.
3. **Equilibrium.** Minimising `W_dis(E_d) + (φ_s0/2)(ε−E_d):C_s:(ε−E_d) + φ_s0 p tr(ε−E_d)` over `span(e1,e2)` gives `(Dd + φ_s0 G) x = φ_s0 (g + p√3 ê1)` with `G_ij = e_i:C_s:e_j`, `g_i = e_i:C_s:ε` — the `√3` from `e1:I = √3` and the vanishing pressure source on `e2` because `e2` is traceless. This is exactly FabricLaw.h:481-499 with the operator built at FabricLaw.h:536-556, and matches the header comment (FabricLaw.h:36-40). The reduced system is linear in `(ε,p)`, so the AD derivatives are exact as claimed (FabricLaw.h:44-46, 557-561).
4. **Compliance restriction.** I re-derived `(C^d)^{-1} = (φ_s0 C_s)^{-1} + D^{+}` (eq. `fabric-compliance-restriction`, pore_fabric.tex:270-273) from stationarity: `σ = D:E_d ∈ range(D)` and `E_d = D^{+}σ`, so `(I + (φ C_s)D^{+})σ = (φ C_s)ε` and hence `(C^d)^{-1} = (φ C_s)^{-1} + D^{+}`; the Moore–Penrose inverse is required exactly as stated. Code: `A6 = inv(φC_s) + D^+`, `cdm = inv(A6)` (FabricLaw.h:465-476). The conformal rank-one case `D^{+} = (1−K/(φ_s0K_s))/(9K) I⊗I` (stress_reconstruction.tex:193-196) follows from `k_v = 3K/(1−K/(φ_s0K_s))`; the script's conformal probe uses `k_v = 5.4 = 3·1/(1−1/2.25)`. Verified numerically.
5. **Transverse isotropy / rotation invariance.** `D = Σ_{i,j≤2} Dd_ij e_i⊗e_j` is supported only on `span(e1,e2)`; it therefore annihilates the four complementary modes, including the coupled in-plane pair `e3 = (p1⊗p1−p2⊗p2)/√2` and `e6 = √2 sym(p1⊗p2)` (script basis, verify_fabric.py:236-247), and is invariant under rotations about `m`. Confirmed by running the script: `||D:e3|| = 1.5823e-16`, `D:e6 = 0.0`, rotation-invariance `2.4965e-16`.
6. **Numeric tolerances (all quotes reproduce).** `2.2e-16` (H reconstruction, 2.2204e-16), `det H − 1 = −3.3e-16` (−3.3307e-16), `||D:e3|| = 1.6e-16` (1.5823e-16), `D:e6 = 0`, rotation `2.5e-16` (2.4965e-16), worst probe field diff `4.9e-15` (4.8850e-15) over `B_par,B_per,ln_a,ln_h,J,J̄,σ11,σ22,φ_solid` (finite_elements.tex:269-279). Conformal cross-check max `1.874e-14` = the σ11 entry (finite_elements.tex:284-286 "1.9e-14"). Reference Biot values `B_par = 0.850654`, `B_per = 0.910270` (coupled) and `0.883871` (uncoupled) reproduce, as does the full-B TI form (`||B − (B_par m⊗m + B_per(I−m⊗m))|| ≈ 1e-16`).
7. **Companion conformal/constant-tangent numbers.** `G = φ_s0 μ_s = 0.9·(5/6) = 0.75`, `K = 1`, `B_0 = 1−K/K_s = 0.6`, total storage `(1−φ_s0)/K_f + S_s = 17/80 = 0.2125` (finite_elements.tex:158-166; S_s in limits.tex:22) all reproduce. experiments.tex:25 reference Biot components `0.7000, 0.7583, 0.7917` reproduce to 1e-12 from `eq:example-mineral-stiffness`. `examples/verify_conformal.py` runs: `checks_passed = 186`, `max_constitutive_identity_error = 2.4549890331732928e-09` (manuscript "2.5e-9", experiments.tex:183-186). Peak centre pressures `4.376e-5 / 4.983e-5 / 5.498e-5 / 3.652e-5` match finite_elements.tex:312-316. The recorded mineral `CS` is isotropic in the Mandel convention (`C11 = λ+2μ = 3.6111`, `C12 = λ = 1.9444`, `C44 = 2μ = 1.6667`, `K_s = 2.5`, `μ_s = 5/6`), consistent with the captions' "isotropic mineral".

The reduced (NDIR=2) claims are internally consistent and true, and the manuscript's "scope of these results" wording (finite_elements.tex:276-287, 335-352) does not overstate what is implemented: the law is explicitly the reference-state linearization, the script's conventions are disclosed, and the coupled runs are labelled demonstrations.

## REQUIRED

**R1. `FabricMaterial` uses a storage coefficient that disagrees with the manuscript's own storage definition (and with the published `ConformalMaterial`).**
`moose_app/include/utils/FabricLaw.h:506` defines `alpha_eff = (b_par + 2 b_per)/3`, which is the mean Biot coefficient `1 − K/K_s`, and `FabricLaw.h:507` then sets
`storage = (1 − φ)/K_f + φ·alpha_eff/K_s`.
The manuscript defines the reference total storage as `(1−φ_s0)/K_f + S_s` with `S_s = (φ_s0/K_s)(1 − K/(φ_s0K_s))` (sections/finite_elements.tex:84-91; sections/limits.tex:18-23, eq. `reference-solid-storage`). The consistent tangent of `m_f = ρ̄_f(J − φ_s0J̄)` at `F=I, p=0` is `∂m_f/∂p = (1−φ_s0)/K_f + 3φ_s0²·solve[0][0]`, and `3φ_s0²·solve[0][0] = (φ_s0/K_s)(1 − K/(φ_s0K_s))`; I confirmed both forms for every probe. The code's value is larger by `(1−φ)·K/K_s²`:
- conformal-limit probe (`k_v = 5.4`): correct `0.2125` (= 17/80) vs code `0.2285`;
- `fabric_probe_iso` (`k_v = k_a = 1`): correct `0.326048` vs code `0.330694`;
- `fabric_probe_coup_a*`: correct `0.328659` vs code `0.333043`.

The published conformal law uses the correct coefficient, `alpha = 1 − K/(φ·K_s)` (`moose_app/include/utils/ConformalLaw.h:73`, used at `:87`), which is what reproduces `17/80`. Because `verify_fabric.py:142-143` replicates `FabricLaw.h`'s expression, and `mass` is not in the compared field list (`verify_fabric.py:213`), the shipped verification cannot detect the difference. The affected output is the `fluid_mass` property (`FabricMaterial.C:70`; `FabricLaw.h:607`), which is consumed by `ReferenceFluidMass` in the coupled fabric decks (`fe-evidence/runs/fabric_mandel_*/input.i:203-204`), so the reported fabric-rotation demonstration pressures are computed with a storage that is ~1.4–7.5 % too large.
Fix: use the solid storage `(φ_s0/K_s)(1 − K/(φ_s0K_s))` (equivalently `3φ_s0²·solve[0][0]`) in `FabricLaw.h:507`, mirror it in `verify_fabric.py:143`, add `mass` to the compared fields, and regenerate the coupled fabric decks. If instead a different storage convention is intended for the fabric material, state it in `sec:fe-fabric` and reconcile it with `(fe-reference-total-storage)`.

## Optional notes

**N1.** `examples/verify_fabric.py:174` computes `mass`, but `mass` is absent from the compared `FIELDS` (verify_fabric.py:213), so the storage/`alpha_eff` error of R1 is outside the shipped check. After fixing R1, adding `mass` to `FIELDS` would make the material-point check guard the storage too.

**N2.** `examples/verify_fabric.py:236-273` (`symmetry_checks`) tests rotation invariance for a single 30° rotation about `m`, at the same 30° fabric angle used to build `D4` (verify_fabric.py:259-260). The result is correct, but a second angle (and ideally a general rotation that mixes `(e3,e6)` and `(e4,e5)`) would make the invariance check less dependent on that coincidence.

**N3.** finite_elements.tex:284-286 quotes the conformal cross-check as "1.9e-14", which is the σ11 entry (1.874e-14); the remaining compared entries are ≤ 2.2e-15. Writing "worst 1.9e-14" would match the script's presentation (`verify_fabric.py:337-343`) exactly.

**N4.** The fabric-probe mineral is isotropic only after reading the Mandel shear entry as `2μ` (`C44 = 1.6667 = 2·(5/6)`, FabricLaw.h:88-98, 100-107). The captions assert an isotropic mineral; one line in `sec:fe-fabric` giving the mineral constants (`K_s = 2.5`, `μ_s = 5/6`, `φ_s0 = 0.9`) would prevent a reader from misreading that entry as `μ_s`.

**N5.** The `B` returned by `FabricMaterial` is the reference-state, pressure- and deformation-independent tensor (`bvec` built once in the constructor, FabricLaw.h:477-483; assigned at FabricMaterial.C:70). The decks and text consistently say "reference-state"; keep that wording and avoid implying that the probe figures show the finite-deformation `B` of eq. `fabric-biot-tensor`.

VERDICT: MINOR REVISION
