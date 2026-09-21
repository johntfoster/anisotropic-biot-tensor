# Round-22 reviewer 3 — prose, notation, novelty positioning, claim discipline

**Manuscript:** "An anisotropic Biot tensor from mineral stress and distention work"
**Reviewed snapshot:** `.agent-runtime/review-snapshots/round-22`
(SNAPSHOT_ID `68f3859a2c3f4ccaf73443f26869b0b86d3bf9b87cb18657365013687f55985d`, 550 files)
**Scope:** prose, notation, novelty positioning, and claim discipline; full independent pass
on the post-editorial tree (prior-round verdicts not carried).

---

## 0. Snapshot integrity

- `sha256(source-manifest.json)` == SNAPSHOT_ID. **PASS.**
- Re-hashed all 550 manifest entries: **550 OK, 0 missing, 0 mismatch.**

---

## 1. Standing author decision (holds)

- **sec:fabric-transverse names the volume–axial distention modulus as the carrier of
  `B_par != B_per`.** Confirmed verbatim: `sections/pore_fabric.tex` closes the section with
  "that directional coupling is carried by the volume--axial modulus of the distention
  stiffness: with the other fabric moduli alone, the drained compliance is transversely
  isotropic while \(\mathbf B\) stays spherical." The coupled-demonstration prose and the
  `fig:fe-fabric-probe` caption state the same in matching terms. **PASS.**
- **Nothing claims an isotropic mineral alone yields a non-spherical Biot tensor.** The abstract
  says "whereas an isotropic mineral recovers the scalar nonlinear Biot coefficient"; the fabric
  section attributes the directional coupling to the *pore fabric* ("even when the mineral itself
  is isotropic"); the probe caption says "With an isotropic mineral the Biot tensor remains
  spherical when the distention stiffness carries no volume–axial coupling." **PASS.**

---

## 2. Symbol collisions

- **`a` as distention volume ratio only.** `a = det A = det G^{1/2}` throughout; no competing
  use of `a` (no half-width, lattice parameter, or other coefficient) in any section. **PASS.**
- **`W_d` vs `W_dis` vs `W_dr` — NOT fully resolved (one leftover).** The drained energy is
  `W_{\mathrm{dr}}` (`stress_reconstruction.tex`); the distention energy was renamed to
  `W_{\mathrm{dis}}` (`sections/pore_fabric.tex`, consistent throughout). But the conclusion in
  `main.tex:582` still writes the distention energy as `\(W_d(\mathbf G)\)` — a stale pre-rename
  symbol that collides with both `W_{\mathrm{dis}}` (the section's name) and `W_{\mathrm{dr}}`
  (the drained energy). See Required item R3.

---

## 3. Figures and citations

- **Both fabric figures are cited.** `\Cref{fig:fe-fabric-probe}` and
  `\Cref{fig:fe-fabric-mandel}` both appear in `sections/finite_elements.tex`. **PASS.**
- **Citations resolve.** 36 keys cited = 36 keys defined in `references.bib`; zero
  cited-but-undefined and zero defined-but-uncited. **PASS.**
- **No withdrawn statement survives.** The formerly listed reference-normalized numbers for the
  rotated-anisotropy / partial-drainage runs are gone; `evidence.json` records them as withdrawn
  and the manuscript states these are "demonstrations … not quantitative verification … not
  experimental validation." **PASS.**

---

## 4. Availability paragraph vs. what the archive ships — FAIL (stale)

The availability paragraph (`sections/experiments.tex`) claims the embedded archive ships "the
`FabricLaw.h` distention law, the `FabricMaterial.h` and `FabricMaterial.C` material, and the
`fabric_probe.i`, `conformal_probe.i`, and `fabric_mandel.i` decks," and that
`site/evidence.json` "pins the SHA-256 hashes of the implementation and evidence files it
reports."

The files exist in `build/anisotropic-biot-2026-09-20-v2.zip`, **but the shipped versions are the
pre-reduction (round-21) 5-direction law, not the reduced 2-direction law the manuscript now
describes.** Verified directly:

| file | archive (zip) | source tree | match? |
| --- | --- | --- | --- |
| `moose_app/include/utils/FabricLaw.h` | `e57f4bdf…` | `2953669c…` | **NO** |
| `moose_app/src/materials/FabricMaterial.C` | `fd343519…` | `9abcfab6…` | **NO** |
| `examples/verify_fabric.py` | `d9194f7c…` | `d6265788…` | **NO** |
| `build/fabric/fabric-verification.json` (zip) vs `build/fabric/…` (tree) | `7b2579a9…` | `66e3f5c4…` | **NO** |

The same staleness is baked into the evidence manifests: `site/evidence.json` pins **8** stale
artifact hashes and `site/scientific-snapshot.json` pins **5** stale file hashes (the same
`FabricLaw.h`, `FabricMaterial.C`, `verify_fabric.py`, the two fabric decks, and the regenerated
fabric figures/CSVs). None of these pins match the current source tree. A reader who extracts the
supplement and follows the reproduction commands would build the *rejected* 5-direction law, not
the law the paper states. See Required item R1.

---

## 5. Quantitative claims vs. shipped artifacts — FAIL (one stale claim)

Every quantitative claim was checked against a listed artifact. One fails:

- **`sections/finite_elements.tex` lines 251–255 (rotated-fabric Mandel peaks).** The prose
  states peak centre pressures `6.28×10⁻⁵` (fabric along `X₁`), `5.10×10⁻⁵` (45°),
  `3.95×10⁻⁵` (other in-plane axis), against `5.13×10⁻⁵` (uncoupled). The shipped figure data
  `figures/fe_fabric_mandel_peak.csv` and `fe-evidence/runs/fabric_mandel_*/analysis.json` record
  **`4.376×10⁻⁵`, `4.983×10⁻⁵`, `5.498×10⁻⁵`, `3.652×10⁻⁵`**. The values differ **and the
  ordering is reversed** (the reduced law increases monotonically with fabric angle; the prose
  implies the opposite). A search of the entire snapshot confirms `6.28e-5 / 5.10e-5 / 3.95e-5 /
  5.13e-5` appear nowhere as peak pressures in round-22. The prose was not updated to the
  regenerated data. See Required item R2.

All other numbers verified consistent (unchanged by this pass): worst probe-field difference
`4.9e-15` (= 4.885e-15), conformal reduction `1.9e-14` (= 1.874e-14), reference Biot components
`0.7000 / 0.7583 / 0.7917`, conclusions step-refinement `3.7e-3 / 7.1e-3` (ratio `1.94`), floor
`3.2e-3`, temporal orders `0.98–1.40`, conformal suite `186` checks / `273` states / `13`
stiffnesses / `2.5e-9`.

---

## VERDICT: MAJOR REVISION

### Required corrections

1. **R1 (reproducibility): regenerate and re-embed the numerical supplement and the evidence
   manifests.** Rebuild `build/anisotropic-biot-2026-09-20-v2.zip` and regenerate
   `site/evidence.json` and `site/scientific-snapshot.json` so that `FabricLaw.h`,
   `FabricMaterial.C`, `fabric_probe.i`, `fabric_mandel.i`, `verify_fabric.py`, and the
   `fabric-verification.json` report all hash-match the current source tree (the reduced
   2-direction distention law). The archive and evidence must not ship/pin the rejected
   5-direction law.

2. **R2 (claim discipline): update the rotated-fabric peak-pressure sentence.**
   `sections/finite_elements.tex` lines ~251–255 must report `4.38×10⁻⁵ / 4.98×10⁻⁵ / 5.50×10⁻⁵`
   (fabric along `X₁` / 45° / other axis, uncoupled reference `3.65×10⁻⁵`) and reverse the
   orientation-ordering statement to match `figures/fe_fabric_mandel_peak.csv` and the recorded
   run analyses.

3. **R3 (notation): fix the `W_d` collision.** `main.tex:582` writes the distention energy as
   `W_d(\mathbf G)`; change it to `W_{\mathrm{dis}}(\mathbf G)` to match `sec:pore-fabric` and to
   stay distinct from the drained `W_{\mathrm{dr}}`.

### Optional (not required)

- None. (The bar-accent and three-`τ`-accent items deferred in the author response are acceptable
  editorial choices; the "full-rank / zero-eigenvalue" tension is resolved by the explicit
  rank-two reduction.)
