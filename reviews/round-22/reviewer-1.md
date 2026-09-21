# Round-22 independent peer review — Reviewer 1 (mathematics)

**Manuscript:** `main.tex`, "An anisotropic Biot tensor from mineral stress and distention work"
**Snapshot under review:** `.agent-runtime/review-snapshots/round-22`
**Declared SNAPSHOT_ID:** `68f3859a2c3f4ccaf73443f26869b0b86d3bf9b87cb18657365013687f55985d`
**Emphasis:** mathematics and correctness. Full independent pass over the tree as frozen after three
Foster editorial cycles. I re-derived the distention kinematics, the virtual-work reduction, the
energy-return relations, the drained stiffness/compliance restrictions, the fabric-coupled Biot
tensor, and the transverse-isotropy case, and recomputed every published number from raw data.

Nothing in the snapshot was modified. Scratch work in `/tmp` (a Python re-implementation of the
conformal constitutive model and of the reduced `FabricLaw` invariants, plus independent hashing).

---

## 1. Snapshot integrity (INT-1)

| Check | Result |
|---|---|
| `sha256(snapshot/source-manifest.json)` vs declared SNAPSHOT_ID | **match** (`68f3859a…585d`) |
| Manifest entries re-hashed | **550 / 550 match**, 0 missing, 0 hash mismatches |
| Files on disk not in the manifest | 2 — `source-manifest.json`, `SNAPSHOT_ID` (self-referential) |

The manifest is internally consistent: no listed file is missing and no hash differs.

## 2. Independent re-derivation: what is confirmed correct

I record these so the required corrections below are not over-extended. All were re-checked, not
inherited from the prior round.

- **Kinematics.** `eq:fabric-distention-polar` (`A=R_A G^{1/2}`, `G=A^T A`),
  `eq:fabric-volume-ratio` (`a=det A=(det G)^{1/2}`), `eq:fabric-multiplicative`
  (`F=R_A G^{1/2} F̄`, `F̄=G^{-1/2} R_A^T F`), `eq:fabric-mineral-metric`
  (`C̄=F^T R_A G^{-1} R_A^T F`) are correct. The conformal specialization `G=a^{2/3} I` reduces them
  **exactly** to `A=a^{1/3} R_A`, `F̄=a^{-1/3} R_A^T F`, `C̄=a^{-2/3} C`, matching the conformal
  section verbatim.
- **Virtual work.** `eq:fabric-virtual-deformation` is the exact `δF F^{-1}` for
  `F=R_A G^{1/2} F̄`; the skew `δR_A R_A^T` term vanishes against symmetric `τ′`, and
  `eq:fabric-phase-work` follows from `eq:constitutive-kirchhoff-phase-stress`. In the conformal limit
  the two terms reduce to `(1/3) tr τ′ δ ln a` and `φ_s0 τ̂_s : (δF̄ F̄^{-1})` — recovering
  `eq:distention-mineral-energy-work` exactly.
- **Energy-return relations.** `eq:energy-returned-effective-stress`
  (`τ′=(∂W_A/∂ ln a) I + φ_s0 dev τ̄_s`) and `eq:energy-returned-pressure-balance`
  (`∂W_A/∂ ln a=(φ_s0/3) tr τ̄_s + φ_s0 p J̄`) are mutually consistent: substituting the second into the
  first recovers the phase balance `τ′=φ_s0(τ̄_s+p J̄ I)` including all shear components.
- **Conformal drained response.** With the example stiffness
  (`φ_s0=0.6`, `K=7`, `C_s` as `eq:example-mineral-stiffness`):
  - `K_s = (1/9) I:C_s:I = 28`; `α = 1−K/(φ_s0 K_s) = 0.583333…`.
  - `eq:drained-stiffness-restriction` gives drained shear = `φ_s0 ×` mineral shear
    (`12.0, 14.4, 16.8` vs `20, 24, 28`).
  - `eq:drained-compliance-restriction` holds exactly:
    `(C^d)^{-1} − (φ_s0 C_s)^{-1} = 0.00925926… × I⊗I = (1−K/(φ_s0 K_s))/(9K)`.
- **Reference Biot components.** `eq:reference-biot-compatibility` `B_0 = I − C^d:C_s^{-1}:I` evaluates to
  `diag(0.7000000000, 0.7583333333, 0.7916666667)` — matching the published `0.7000, 0.7583, 0.7917`
  **exactly**.
- **`ln_h` convention.** With `e2 = sqrt(3/2)(m⊗m − I/3)` and
  `eq:fabric-transverse-strain` `E_dis=(ln a/3) I + ln h (I/2 − 3/2 m⊗m)`, the identity
  `I/2 − 3/2 m⊗m = −sqrt(3/2) e2` gives `x2 = −sqrt(1.5) ln h`, i.e. `ln h = −x2/sqrt(1.5)`. The
  compiled `FabricLaw.h` (`s.ln_h = −xi/std::sqrt(1.5)`) **is** the paper's `ln h`, not its negative.
- **Re-implementation agreement.** `build/fabric/fabric-verification.json`
  `worst_probe_abs_diff = 4.885×10^{-15}` — consistent with the published `4.9×10^{-15}`.
- **Conformal reduction.** The same report's `conformal_cross_check` gives worst `1.874×10^{-14}`
  (σ₁₁) — consistent with the published `1.9×10^{-14}`.

## 3. REQUIRED corrections

### NUM-1 — The published peak centre pressures in `sec:fe-fabric` do not match the recorded data (stale numbers, reversed ordering)

**Locations.** `sections/finite_elements.tex:252–254` (the sentence beginning "The peak centre
pressure is …"); the recorded data `figures/fe_fabric_mandel_peak.csv` and
`fe-evidence/runs/fabric_mandel_{iso,coup_a0,coup_a45,coup_a90}/solution.csv` in the same snapshot;
the figure `figures/fe_fabric_mandel.pdf` (regenerated from those runs).

**Defect.** The manuscript text states the peak centre pressure is
`6.28×10⁻⁵` for a fabric axis along `X₁`, `5.10×10⁻⁵` at `45°`, `3.95×10⁻⁵` along the other
in-plane axis, against `5.13×10⁻⁵` with the coupling off. The recorded data in the same snapshot
gives a **different set of values and a reversed ordering**:

| case (recorded) | fabric angle | recorded peak `center_pressure` |
|---|---|---|
| `fabric_mandel_iso` (no coupling) | — | `3.652325×10⁻⁵` |
| `fabric_mandel_coup_a0` | 0° (X₁) | `4.376073×10⁻⁵` |
| `fabric_mandel_coup_a45` | 45° | `4.982579×10⁻⁵` |
| `fabric_mandel_coup_a90` | 90° (other axis) | `5.497927×10⁻⁵` |

So the text's four numbers (`6.28/5.10/3.95` and the `5.13` uncoupled reference) appear nowhere in
the recorded data, and the **directional trend is inverted**: the text has X₁ largest
(`6.28`) and the perpendicular axis smallest (`3.95`), whereas the data has X₁ smallest
(`4.38`) and the perpendicular axis largest (`5.50`). The text's uncoupled reference (`5.13×10⁻⁵`)
also disagrees with the recorded uncoupled peak (`3.65×10⁻⁵`).

**Required action.** Reconcile `sections/finite_elements.tex:252–254` with
`figures/fe_fabric_mandel_peak.csv`. The correct values are `4.38×10⁻⁵` (X₁), `4.98×10⁻⁵` (45°),
`5.50×10⁻⁵` (perpendicular), against `3.65×10⁻⁵` (uncoupled), with the ordering stated the right way
round. (The working tree outside the snapshot already carries these corrected digits, but the frozen
snapshot under review does not; the review is of the snapshot.)

### NUM-2 — `sec:pore-fabric` describes a five-modulus, full-rank distention stiffness while the implemented and verified law is the reduced two-direction (`span(e1,e2)`) model

**Locations.** `sections/pore_fabric.tex:250` (`eq:fabric-compliance-restriction`, RHS `D^{-1}`),
`sections/pore_fabric.tex:260–266` ("the five-modulus transversely isotropic `D` … full rank on the
volumetric, axial, in-plane-deviatoric and the two shear directions"), `sections/pore_fabric.tex:193–194`
("The remaining five components of `eq:fabric-equilibrium` are new"); contrasted with
`moose_app/include/utils/FabricLaw.h:61` (`NDIR = 2`), `:437–450` (the `2×2` `dd` block
`{k_v,k_a,k_c}` on `span(e1,e2)`), and the deck `fe-evidence/runs/fabric_mandel_coup_a45/input.i:161–163`
(`fabric_volume_modulus=5.4`, `fabric_axial_modulus=1`, `fabric_coupling=0.4` — three moduli, no
in-plane/shear moduli).

**Defect.** The manuscript text states the drained compliance obeys
`(C^d)^{-1} = (φ_s0 C_s)^{-1} + D^{-1}` with `D` a "five-modulus transversely isotropic" stiffness
"full rank" on five directions, and that "the remaining five components" of the fabric equilibrium are
new. The compiled law in the same snapshot restricts the distention strain to the two-dimensional
axisymmetric subspace `span(e1,e2)` (volumetric + axial), with a positive-definite `2×2` block; the
four complementary modes carry no distention energy and are frozen to the mineral. Consequently:
(i) `D` is rank-two on the six-dimensional space of symmetric tensors, so its ordinary inverse in
`eq:fabric-compliance-restriction` does not exist — the relation actually used is the Moore–Penrose
inverse `D^{+}` (which the text itself invokes two sentences later at `:266`, in self-contradiction);
(ii) "five-modulus … full rank" and "the remaining five components" describe a model the code does not
implement; with `NDIR=2` there is one retained shape component and four frozen modes.

**Required action.** Bring `sec:fabric-biot` and `sec:fabric-equilibrium` into agreement with the
implemented law: state that `D` is positive-definite only on `span(e1,e2)` (zero on the complement),
that the minimization in `eq:fabric-equilibrium` is over `range D` with the complementary modes frozen
to the mineral, that `eq:fabric-compliance-restriction` therefore reads `… + D^{+}` (Moore–Penrose),
and that the retained model has the volumetric–axial `2×2` block `(k_v,k_a,k_c)` — not "five-modulus",
not "full rank on five directions", and not "the remaining five components". These are exactly the
reductions the code and regenerated evidence already reflect, but the manuscript text in the frozen
snapshot was not updated to match them.

## 4. OPTIONAL notes

- **OPT-1.** `eq:fabric-distention-stress` writes the work conjugate `S̄_d` while the same section later
  switches to `S_dis = ∂W_dis/∂E_dis`; the two are related by the self-adjoint matrix-logarithm
  derivative and the text says so, but the subscript change (`_d` vs `_dis`) is an unnecessary
  notational split that could be unified.
- **OPT-2.** The abstract's sentence "no quantitative finite-deformation verification and no
  experimental validation are claimed for those demonstrations" is accurate, but because `NUM-1`
  corrects the headline demonstration numbers, the abstract/`sec:fe-fabric` caveat ("Each peak
  coincides with the final recorded state rather than a transient overshoot") should be re-checked
  after the numbers are corrected so the caveat and the corrected values are consistent.

## 5. Assessment

The conformal core of the paper — kinematics, the phase-stress/work equivalence, the implicit
mineral-volume equation, the spherical rank-one compliance restriction, `eq:anisotropic-biot-explicit`,
the reference and unjacketed limits — is mathematically sound, and I found no error in it. The
reference Biot components (`0.7000/0.7583/0.7917`), the `4.9×10⁻¹⁵` re-implementation agreement, the
`1.9×10⁻¹⁴` conformal reduction, and the `ln_h = ln h` convention all reproduce from the raw data.

However, two correctness defects remain in the frozen snapshot. First (`NUM-1`), the manuscript text
reports peak centre pressures (`6.28/5.10/3.95` vs `5.13×10⁻⁵`) that contradict the recorded data and
figure in the same snapshot, with the directional ordering reversed. Second (`NUM-2`), the theory
section describes a five-modulus, full-rank, `D^{-1}` distention law while the implemented and verified
law is the reduced two-direction `span(e1,e2)` model with the Moore–Penrose `D^{+}`. Both are cases
where the code and regenerated evidence advanced to the reduced model but the manuscript text in the
frozen snapshot was not brought along. These are factual errors in the paper's headline quantitative
result and in its central new section, and they require correction before acceptance.

VERDICT: MAJOR REVISION

### Required corrections

1. **NUM-1** — Replace the peak centre pressures in `sections/finite_elements.tex:252–254` with the
   recorded values `4.38×10⁻⁵` (X₁), `4.98×10⁻⁵` (45°), `5.50×10⁻⁵` (perpendicular axis), against
   `3.65×10⁻⁵` (uncoupled), and state the orientation ordering in the correct direction.
2. **NUM-2** — Rewrite `sections/pore_fabric.tex` `eq:fabric-compliance-restriction` (RHS `D^{-1}` →
   `D^{+}`), the "five-modulus … full rank on five directions" sentence, and "the remaining five
   components" to describe the implemented `span(e1,e2)` volumetric–axial `2×2` model, stating that
   `D` is positive-definite only on the retained subspace and that the four complementary modes are
   frozen to the mineral.

### Optional

1. **OPT-1** — Unify the `S̄_d` / `S_dis` subscript convention in `eq:fabric-distention-stress` and its
   surrounding prose.
2. **OPT-2** — After `NUM-1`, re-check the "peak coincides with the final recorded state" caveat so it
   remains consistent with the corrected values.
