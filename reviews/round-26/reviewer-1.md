# Round 26 — Independent reviewer 1 (mathematics / correctness)

Scope reviewed: `sections/pore_fabric.tex`, `sections/finite_elements.tex`,
`sections/limits.tex`, `sections/stress_reconstruction.tex`,
`sections/logarithmic_derivative.tex`, `main.tex`,
`moose_app/include/utils/FabricLaw.h`, `moose_app/include/utils/ConformalLaw.h`,
`examples/verify_fabric.py`, `fe-evidence/`, `validation/`.

All numerical work was done from a temporary copy
(`TMP=$(mktemp -d); cp -r .agent-runtime/review-snapshots/round-26/. "$TMP"/`),
never in place. I did not read `reviewer-2.md`, `reviewer-3.md`, or any earlier
round's report.

---

## 1. Snapshot integrity

| Check | Command | Result |
|-------|---------|--------|
| Manifest hash vs declared SNAPSHOT_ID | `cd .agent-runtime/review-snapshots/round-26 && sha256sum source-manifest.json` | `6e1afd9363639bdedf68ad4c42169710b7e74830e7d5fa83af91d3387c142907` — **identical** to the declared SNAPSHOT_ID |
| Entry count | `json.load(source-manifest.json)` | 591 entries (matches LAUNCH-STATE "Files: 591") |
| Re-hash every entry | Python loop over manifest: `hashlib.sha256(open(p,'rb').read()).hexdigest() == expected` | **OK = 591, MISSING = 0, MISMATCH = 0** |
| Internal FE evidence manifest | `fe-evidence/manifest.json` (317 files) re-hashed | **0 missing, 0 digest mismatches, 0 byte-length mismatches** |
| `SNAPSHOT_ID` file | `cat .agent-runtime/review-snapshots/round-26/SNAPSHOT_ID` | `6e1afd93…2907` (same) |

**No integrity item is required.** The snapshot re-hashes clean.

Round-25 required fixes verified present and prose/documentation-only:

* **R25-2-1** — `grep -rn "eigenvalue ratio"` over the *whole snapshot* returns
  no file; `grep -c "eigenvalue ratio" site/evidence.json
  site/scientific-snapshot.json` returns `0` and `0`. Absent from the manuscript
  and from the shipped site data, as required.
* **R25-3-1** — `sections/pore_fabric.tex` `sec:fabric-biot` now reads
  "…and the axial (degree-two) direction \(\mathbf e_2=\sqrt{3/2}(\mathbf m\otimes\mathbf m-\mathbf I/3)\),
  where \(\mathbf m\) is the unit material fabric axis". Definition at first use
  is present.
* **R25-3-2** — the clause attached to `eq:fabric-transverse-strain` now reads
  "twice whose exponential, \(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G=a^{2/3}\mathbf H\),
  reconstructs \eqref{eq:fabric-transverse-h}, whose unimodular eigenvalues are
  \(h^{-2},h,h\)." I re-derived this identity analytically (see finding M2) and
  confirmed it numerically; the replacement claim is correct and no equation,
  number, or downstream claim changed.

---

## 2. Independent mathematical review

### 2.1 Identities re-derived by hand and confirmed numerically

I re-derived each of the following from the manuscript's own definitions and
then re-checked it numerically with code I wrote myself (not the repository's
helpers), in `/tmp/rev1_indep/`.

**M1 — Fabric tensor.** With
\(\mathbf H=h^{-2}\mathbf m\otimes\mathbf m+h(\mathbf I-\mathbf m\otimes\mathbf m)\)
the eigenvalues are \(h^{-2}\) (axis \(\mathbf m\), multiplicity 1) and \(h\)
(multiplicity 2), so \(\det\mathbf H=h^{-2}\cdot h\cdot h=1\). Correct.
`examples/verify_fabric.py` independently reports `H_det_minus_one =
-3.33e-16` and eigenvalues `[0.999286354, 1.000357014, 1.000357014]` matching
`[h^-2,h,h]`.

**M2 — Distention strain ↔ \(\mathbf G\).** From
\(\mathbf E_{\mathrm{dis}}=\tfrac12\ln\mathbf G\), \(\ln\mathbf G=\tfrac23\ln a\,\mathbf I+\ln\mathbf H\)
and \(\ln\mathbf H=\ln h\,(\mathbf I-3\mathbf m\otimes\mathbf m)\), so
\[
\mathbf E_{\mathrm{dis}}=\frac{\ln a}{3}\mathbf I+\ln h\Big(\tfrac12\mathbf I-\tfrac32\mathbf m\otimes\mathbf m\Big),
\]
which is exactly `eq:fabric-transverse-strain`. Conversely
\(2\mathbf E_{\mathrm{dis}}=\tfrac23\ln a\,\mathbf I-3\ln h\,\mathbf m\otimes\mathbf m\),
so \(\exp(2\mathbf E_{\mathrm{dis}})=a^{2/3}\big(h^{-2}\mathbf m\otimes\mathbf m+h(\mathbf I-\mathbf m\otimes\mathbf m)\big)=a^{2/3}\mathbf H\).
Confirmed to \(2.22\times10^{-16}\) by `verify_fabric.py`
(`H_reconstruction_max_abs_diff`) and to machine precision in my own script.
The basis identities \(\mathbf e_1=\mathbf I/\sqrt3\) (unit), \(\mathbf e_2=\sqrt{3/2}(\mathbf m\otimes\mathbf m-\mathbf I/3)\)
(unit, and \(\tfrac12\mathbf I-\tfrac32\mathbf m\otimes\mathbf m=-\sqrt{3/2}\,\mathbf e_2\),
hence the reported \(\ln h=-x_2/\sqrt{1.5}\)) are all exact.

**M3 — Drained compliance restriction.** I inverted
\(\mathbb C^d=\phi_{s0}\mathbb C_s-\frac{\phi_{s0}}{9K_s}(1-\frac K{\phi_{s0}K_s})(\mathbb C_s:\mathbf I)\otimes(\mathbb C_s:\mathbf I)\)
with the Sherman–Morrison identity (\(\mathbf A=\phi_{s0}\mathbb C_s\),
\(\mathbf u=\mathbb C_s:\mathbf I\), \(\mathbf A^{-1}\mathbf u=\mathbf I/\phi_{s0}\),
\(\mathbf u:\mathbf A^{-1}:\mathbf u=9K_s/\phi_{s0}\)) and obtained exactly
\((\mathbb C^d)^{-1}=(\phi_{s0}\mathbb C_s)^{-1}+\frac{1-K/(\phi_{s0}K_s)}{9K}\mathbf I\otimes\mathbf I\),
i.e. `eq:drained-stiffness-restriction` and `eq:drained-compliance-restriction`
are mutually consistent. Cross-checked with a random-anisotropic test
(60 random SPD minerals, random retained subspaces, random \(K\)):
`worst |(Cd)^-1-(phi Cs)^-1 - alpha/(9K) I⊗I| = 2.7e-15`, and the equality
\(\mathbb C^d:\boldsymbol\varepsilon=\phi_{s0}\mathbb C_s:\bar{\boldsymbol\varepsilon}\)
at \(p=0\) holds to `4.3e-16`. The inverse of the conformal relation is the
spherical rank-one contribution with \(\mathbb D^{+}=\frac{\alpha}{9K}\mathbf I\otimes\mathbf I\),
matching the \(k_v=3K/\alpha\) normalization used by the implementation.

**M4 — Equilibrium.** I verified that the manuscript's stationarity condition
`eq:fabric-equilibrium` reduces along \(\mathbf G=a^{2/3}\mathbf I\) to
\(\partial W_A/\partial\ln a=(\phi_{s0}/3)\operatorname{tr}\bar{\boldsymbol\tau}_s+\phi_{s0}p\bar J\)
(`eq:energy-returned-pressure-balance`): the distention term contributes
\(\partial W_A/\partial\ln a\), the mineral-energy term \(-\tfrac13\operatorname{tr}\bar{\boldsymbol\tau}_s\),
and the pressure term \(-\phi_{s0}p\bar J\). I also confirmed numerically that
the implementation's linear system
\((\mathbb D+\phi_{s0}\mathbb G)\mathbf x=\phi_{s0}(\mathbf g+p\sqrt3\,\hat{\mathbf e}_1)\)
is the exact stationarity point of
\(\Pi=\tfrac12\mathbf x^\top\mathbb D\mathbf x+\tfrac{\phi_{s0}}2\bar{\boldsymbol\varepsilon}:\mathbb C_s:\bar{\boldsymbol\varepsilon}+\phi_{s0}p\operatorname{tr}\bar{\boldsymbol\varepsilon}\)
(finite-difference \(|\mathrm d\Pi/\mathrm dx|=8.7\times10^{-12}\)). The \(p\)-coupling
enters only the volumetric direction because \(\operatorname{tr}\mathbf e_1=\sqrt3\),
\(\operatorname{tr}\mathbf e_2=0\).

**M5 — Tensorial phase work.** `eq:fabric-virtual-deformation` follows from
\(\mathbf F=\mathbf R_A\mathbf G^{1/2}\bar{\mathbf F}\) by direct differentiation;
the skew term vanishes against symmetric \(\boldsymbol\tau'\); and using the phase
balance \(\boldsymbol\tau'=\phi_{s0}(\bar{\boldsymbol\tau}_s+p\bar J\mathbf I)\)
the pressure terms cancel to give `eq:fabric-phase-work`. In the conformal limit
\(\mathbf G^{1/2}=a^{1/3}\mathbf I\) this reduces to
\(\tfrac13\operatorname{tr}\boldsymbol\tau'\,\delta\ln a+\phi_{s0}\hat{\boldsymbol\tau}_s:(\delta\bar{\mathbf F}\bar{\mathbf F}^{-1})\),
i.e. `eq:distention-mineral-energy-work`. Correct.

**M6 — Finite Biot tensor.** Differentiating `eq:anisotropic-mineral-eos` at fixed
\(p\) gives `eq:mineral-fixed-pressure-derivative` with coefficient \(K/\phi_{s0}\)
on \(\mathbf F^{-T}\). Substituting into
\(\mathbf B=\mathbf I-\frac{\phi_{s0}}J\partial_{\mathbf F}\bar J\,\mathbf F^T\)
with \(\partial_{\mathbf F}\bar J=\bar J\,\partial_{\mathbf F}\ln\bar J\)
yields `eq:anisotropic-biot-explicit` **exactly, including the \(K\) (not \(K/\phi_{s0}\))
prefactor and the \(\phi_{s0}/3\) prefactor on the shape term**. For isotropic
\(\mathbb C_s\), \(\operatorname{dev}(\mathbb C_s:\mathbf I)=\mathbf 0\) and the
tensor collapses to the scalar form `eq:reconstructed-isotropic-source-biot`.
The matrix-logarithm facts used (spectral form `eq:log-frechet-spectral-form`,
self-adjointness, and \(\operatorname{tr}\boldsymbol\tau=\operatorname{tr}\mathbf T\)
because \(c_{ii}=1/\lambda_i\)) are all correct.

**M7 — Reference Biot and storage.** \(\mathbb C^d:\mathbb C_s^{-1}:\mathbf I=\phi_{s0}\mathbf I-\frac{\phi_{s0}\alpha}{3K_s}\mathbb C_s:\mathbf I\)
(verified to `5.0e-16` for random anisotropic minerals). Hence
\(\mathbf B_0=\mathbf I-\mathbb C^d:\mathbb C_s^{-1}:\mathbf I\) agrees with the
implementation. The isotropic reference gives \(B_0=1-K_d/K_s=1-1/2.5=0.6\),
and for the paper's example mineral \(K_s=28K_*\), \(\phi_{s0}=0.6\), \(K=7K_*\)
the three reference components reproduce as \(0.7000,0.7583,0.7917\). The storage
definitions `eq:reference-solid-storage` and `eq:reference-storage-compatibility`
agree, and both equal \((\phi_{s0}/K_s)(1-K/(\phi_{s0}K_s))\) (verified to
`2.2e-16` for random anisotropic minerals). The finite-element deck values give
\(S_s=0.2\), total storage \((1-0.9)/8+0.2=17/80\). Correct.

### 2.2 Reported finite-element numbers — all reproduce

Recomputing from the frozen artifacts:

* MMS orders (panel a): `python3 fe-evidence/compute_mms_order.py --runs fe-evidence/runs`
  reproduces `fe-evidence/mms-convergence.json` **byte-for-byte** (`diff` clean).
  `p_l2` naive orders `1.9966, 2.0008` → 2.00, 2.00; `ux_l2` `2.9917, 2.9585`
  → 2.99, 2.96; `uy_l2` `2.9983, 2.9600` → 3.00, 2.96. Matches the caption.
* Step-refinement ratio (panel c): from `figures/fe_mandel_refinement.csv`,
  `linear_time_0.002 / linear_time_0.001` = `7.1039215708695895e-3 /
  3.657958974355574e-3 = 1.942` → **1.94**.
* Finite-load floor (panel d): `figures/fe_load_limit.csv`,
  `nonlinear_load_0.0001` `pressure_max_normalized = 3.220919735602341e-3`
  → **3.2e-3**.
* Pore-fabric probes: my own from-scratch re-implementation reproduces every
  recorded `figures/fe_fabric_probe.csv` field (`B_par`, `B_per`, `ln_a`, `ln_h`,
  `J`, `Jbar`, `sigma11`, `sigma22`) with worst absolute difference
  **4.55e-15**.
* `examples/verify_fabric.py` (run from the temp copy): worst probe-field
  difference **4.885e-15** (paper: 4.9e-15); `H` reconstruction **2.220e-16**
  (paper: 2.2e-16); `det H - 1 = -3.331e-16` (paper: -3.3e-16);
  `||D:e3|| = 1.582e-16` and `D:e6 = 0` (paper: 1.6e-16, 0);
  rotation invariance **2.497e-16** (paper: 2.5e-16); conformal limit worst diff
  **1.874e-14** (paper: 1.9e-14).
* Coupled peak pressures: `figures/fe_fabric_mandel_peak.csv` gives 3.616e-5
  (uncoupled), 4.363e-5, 4.990e-5, 5.521e-5 → paper 3.62, 4.36, 4.99, 5.52
  (×10⁻⁵); each `peak_center_pressure == final_center_pressure` at
  `final_time = 0.003`, so "each peak coincides with the final recorded state"
  is correct.
* Refined 40×8 contours: `figures/fe_fabric_contours.csv` `p_max` 3.606e-5,
  4.349e-5, 4.974e-5, 5.503e-5 → paper 3.61, 4.35, 4.97, 5.50 (×10⁻⁵);
  `u_mag_max` 5.183e-5, 5.137e-5, 2.382e-5, 5.259e-5 → paper 5.18, 5.14, 2.38,
  5.26 (×10⁻⁵). `p_max_x = 0.0` and `p_min ≈ 0` in every case, confirming the
  maximum lies on the \(X_1=0\) symmetry line and the pressure falls to zero at
  \(X_1=1\).
* Reference-problem parameters: `fe-evidence/runs/linear_coarse/input.i` uses
  `solid_fraction=0.9, drained_bulk=1, fluid_bulk=8, mobility=1.5` with the
  mineral-stiffness entries `3.6111…, 1.9444…, 1.6667…` that give \(K_s=2.5\),
  \(\mu_s=5/6\); the deck therefore matches the manuscript's stated reference
  inputs, and the derived \(G=0.75\), \(B_0=0.6\), \(17/80\) are consistent.
* `examples/verify_reconstruction.py`, `verify_tensor.py`, `verify_conformal.py`,
  `verify_fluid_coupling.py` all run clean from the temp copy; their reported
  errors are at or below the manuscript's claims.

### 2.3 Findings

**Finding 1 — `fe-evidence`/`validation` cross-checks — OPTIONAL.**
`validation/mandel_reference.py` (referenced by the traceability map) uses the
same `C_s`/rotation as `validation/mms_reference.py`; the MMS deck's exact fields
(`fe-evidence/runs/mms_space_16/input.i`) match `eq:fe-mms-u1..-pressure`
(\(U=P_0=0.01\)) exactly. No discrepancy found; recorded for completeness only.

**Finding 2 — panel (b) prose vs. the recorded temporal orders — OPTIONAL.**
`sections/finite_elements.tex` states of the fixed-mesh successive-difference
orders: "the values lie near one and include one above one"; the
`fig:fe-verification` caption says "the values include one above unity".
From the frozen `fe-evidence/mms-convergence.json` (the same file
`compute_mms_order.py` regenerates exactly), the nine `difference_orders` are
`nx16: 1.0932, 0.9783, 1.0152`; `nx32: 1.3969, 1.0183, 1.1252`;
`nx64: 1.3964, 1.0762, 1.2519` — i.e. **eight** of nine exceed unity, with a
range of 0.98–1.40 rather than "near one with one above one". The
`sec:conclusion` statement of the same data is accurate ("0.98–1.40, including
values above one"), and the substantive hedge ("no order above one is asserted")
is correct everywhere, so this is a wording/count imprecision in one place
rather than a false convergence claim. Optional: align the section text and the
caption with the count and range already given in the conclusions.

**Finding 3 — justification of the retained subspace — OPTIONAL.**
`sec:fabric-equilibrium` justifies the restriction by "on the complement \(\mathbb D\)
vanishes, the potential does not depend on the complementary modes, and those
modes are frozen to the mineral rather than equilibrated". Taken about the
bracketed potential of `eq:fabric-equilibrium`
(\(W_{\mathrm{dis}}+\phi_{s0}\bar W_s+\phi_{s0}p\bar J\)), the flatness claim is
not literally true: \(W_{\mathrm{dis}}\) has no stiffness on the complement, but
\(\bar W_s(\bar{\boldsymbol\varepsilon})\) and \(p\bar J\) both depend on
\(\mathbf E_{\mathrm{dis}}\) through \(\bar{\boldsymbol\varepsilon}=\boldsymbol\varepsilon-\mathbf E_{\mathrm{dis}}\)
in *every* direction, so an unrestricted complementary mode would equilibrate
rather than be frozen. The manuscript states the correct reason elsewhere
(`sec:fabric-biot`: "the complementary modes are kinematically frozen to the
mineral, which carries them at its own compliance", presented explicitly as a
modeling choice), and the restriction is applied consistently in
`eq:fabric-equilibrium`, `eq:fabric-compliance-restriction`, and
`FabricLaw.h`, so no equation, number, or conclusion is affected. Optional:
phrase the sentence as a modeling choice rather than a consequence of the
vanishing distention stiffness.

No wrong signs, factor errors, or non-reproducing numbers were found. The
implementation's own guards (SPD checks on the mineral and distention
stiffnesses, orthonormality of the retained basis, stability-domain check
`eq:trace-mineral-stability-domain`) are consistent with the stated
assumptions.

---

## 3. Overall assessment

The snapshot is intact: `sha256(source-manifest.json)` equals the declared
SNAPSHOT_ID, and all 591 manifest entries (plus the 317 internal FE-evidence
entries) re-hash without a single missing or mismatched file. The three
round-25 required fixes are present, and all three are prose/documentation-only;
no equation, number, or claim attached to them changed, and the rephrased
`exp(2E_dis)=G` statement is correct.

I independently re-derived the tensorial distention construction, the
\(\mathbf H\) spectrum and unimodularity, the distention strain and its
exponential, the drained compliance restriction and its rank-one conformal
reduction, the equilibrium and its conformal reduction, the tensorial phase
work, the finite Biot tensor, the logarithmic-derivative identities, and the
reference Biot/storage relations. All hold analytically, and all agree with the
compiled materials and the recorded artifacts at or below \(10^{-14}\). Every
number quoted in the reviewed sections — MMS orders, the 1.94 step ratio,
the \(3.2\times10^{-3}\) floor, the probe tolerances, and all pore-fabric peak
pressures and displacement magnitudes — reproduces from the frozen artifacts
under the exact commands cited above.

The only observations are two optional prose-precision points (a
count/range wording in the panel (b) description, and one justification
sentence about the frozen complementary modes) plus one cross-check note.

VERDICT: ACCEPT
