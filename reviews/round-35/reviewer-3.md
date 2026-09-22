# SIMULATED AI PEER REVIEW — Reviewer 3 of 3

**This is not journal peer review and confers no acceptance.**

- Snapshot reviewed (read-only): `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/review-snapshots/round-35`
- Declared SNAPSHOT_ID: `3e56fad609d38c3a6dd65c10e6aff3959ec7deaff3c21ba2b86448074ad1d886`
- Emphasis: exposition, notation, and claims. Equation numbers resolved from `build/main.pdf` (pdftotext) and `build/main.log`; `build/main.aux` is not shipped.
- Scope boundaries honoured: I did **not** run any held numerical suite (`validation/`, `examples/verify_*.py`). All numbers below are read from frozen artifacts or recomputed independently in a scratch interpreter.

---

## 1. Mandatory first checks

### Check 1 — manifest hash vs declared SNAPSHOT_ID

Command:

```
cd <snapshot> && sha256sum source-manifest.json && cat SNAPSHOT_ID
```

Result:

```
3e56fad609d38c3a6dd65c10e6aff3959ec7deaff3c21ba2b86448074ad1d886  source-manifest.json
3e56fad609d38c3a6dd65c10e6aff3959ec7deaff3c21ba2b86448074ad1d886
```

- sha256(`source-manifest.json`) equals the declared SNAPSHOT_ID **exactly**. PASS
- The `SNAPSHOT_ID` file holds the identical string `3e56fad609d38c3a6dd65c10e6aff3959ec7deaff3c21ba2b86448074ad1d886`. PASS
- (`sha256sum SNAPSHOT_ID` itself is `98196c98…`; that is the digest of the one-line file, not the declared id, and is expected to differ.)

### Check 2 — re-hash every manifest entry and walk the tree

Command: Python re-hash of `source-manifest.json` (a flat `path -> sha256` mapping, 608 entries) plus an `os.walk` of the snapshot.

Result:

```
entries listed:                    608
entries re-hashed OK (file existed): 608
hash mismatches:                   0
listed files missing on disk:      0
files present but unlisted:        0
total files on disk:               610
```

610 = 608 listed + `source-manifest.json` + `SNAPSHOT_ID`, which cannot list themselves. **PASS — no mismatches, no missing files, no unlisted files.**

### Check 3 — independence declaration

I declare that I did **not** open any file under `reviews/` (including `reviews/README.md`); I did **not** read, list, glob, or `find` any other `.agent-runtime/review-snapshots/round-*` directory, any other reviewer's report, or any verdict/acceptance count.

Self-reported exposure: my in-snapshot tree walk (`find . -type f`, inside round-35 only) printed the path string `./reviews/README.md` in its output. No file under `reviews/` was opened, read, or hashed. No other exposure occurred.

---

## 2. Notation paragraph — every cross-reference resolved against the rendered PDF

The notation paragraph is `main.tex` lines 216–262 (renders pp. 3–4). I resolved every label in it to its rendered equation number from `build/main.pdf`. Equation numbering is continuous **1–106** with no gap (`build/main.log` shows no undefined reference, no multiply-defined label, no rerun warning).

| Cited in the notation paragraph | Label | Renders as | Intended display? |
|---|---|---|---|
| distention gradient **A** | `eq:true-mineral-jacobian` | (1) | yes |
| conformal factor | `eq:spherical-distention` | (2) | yes |
| τ̄_s = J̄σ̄_s | `eq:kirchhoff-volume-conventions` | (10) | yes |
| S̄_dis | `eq:fabric-distention-stress` | (72) | yes |
| Q̄_f | `eq:fe-fluid-residual` | (96) | yes |
| σ′ | `eq:total-cauchy-single-prime` | (8) | yes |
| **P**″ | `eq:fixed-pressure-stress` | (46) | yes |
| σ = σ″ − p**B** | `eq:finite-biot-tensor` | (49) | yes |
| W″ | `eq:reduced-energy` | (44) | yes |
| W′ | `eq:legendre-energy` | (45) | yes |
| ℂ^d | `eq:drained-stiffness-restriction` | (40) | yes |
| W^d | `eq:prescribed-logarithmic-energies` | (29) | yes |
| τ̃ | `eq:fabric-phase-work` | (74) | yes |
| rotation between frames | `eq:rotated-mineral-cauchy` | (6) | yes |

**All twelve cross-references resolve to the intended equations.** No dangling reference. Section cross-references also resolve: `sec:work-equivalence`→3, `sec:finite-biot`→5, `sec:pore-fabric`→7, `sec:finite-elements`→9; the raw `\ref{sec:experiments}` in the Data-availability statement renders as a number, not `??`.

---

## REQUIRED ITEMS

### R3-C1 — the "wide tilde" rule does not match its only instance, and is self-contradictory

**Location:** `main.tex` lines 257–259 (renders p. 4):
> "A wide tilde denotes the representation of a true-frame quantity in the intermediate mineral frame, obtained by the rotation **R**_A, as in τ̃ = **R**_A^T τ′ **R**_A of (74)."

**Problem.** Read against the paragraph's own definitions four sentences earlier — "A bar on a stress denotes its representation in the mixture frame, whereas a hat denotes the true frame" — and against §2 ("Let σ̂_s denote the intrinsic mineral Cauchy stress **in the frame reached by F̄**"), the *true frame* and the *intermediate mineral frame* are the same frame. On that reading this sentence says the tilde denotes "the representation of a [true-frame] quantity in the [true] frame", i.e. an identity, which is plainly not what (74) does.

What (74) actually does: τ′ is the **mixture-frame** skeleton effective stress (defined at (8) as σ′ = σ + p**I**, and (12) τ′ = φ_s0(τ̄_s + pJ̄**I**)); **R**_A rotates true→mixture by (6); therefore **R**_A^T τ′ **R**_A = φ_s0(τ̂_s + pJ̄**I**) is the **true/mineral-frame** representation of a mixture-frame quantity. So the input is mislabelled ("true-frame" should be "mixture-frame"), and/or the output frame is mislabelled ("intermediate mineral frame" is the same frame as the "true frame" the rule claims as input). The decoration is used exactly once in the manuscript, so there is no other instance to disambiguate it.

**Effect.** A reader following the notation will rotate the wrong quantity or the wrong way; the sentence cannot be parsed consistently on a first reading. This is the one stated rule in the audited paragraph that does not match the definition it governs.

**Fix.** Rewrite as, e.g.: "A wide tilde denotes the true-frame (mineral-frame) representation of a mixture-frame quantity, obtained by the rotation **R**_A, as in τ̃ = **R**_A^T τ′ **R**_A of (74)."

### R3-C2 — `ξ` is used once and never defined

**Location:** `main.tex` line 222 (renders p. 3):
> "A bar on an intrinsic density denotes the per-phase-volume value ρ̄_ξ = ρ_ξ/φ_ξ, which is the mineral state for the solid."

`ξ` occurs exactly once in the whole manuscript (`grep -n 'xi' main.tex sections/*.tex` returns only line 222 as a symbol use) and is nowhere introduced as a phase index, nor is `φ_ξ`/`ρ_ξ` ever used again. The reader must infer that ξ ranges over phases, in a sentence whose stated purpose is to fix notation. The manuscript uses `s` and `f` subscripts everywhere else, so the generic index is dropped immediately after being introduced.

**Fix.** One clause: "…denotes the per-phase-volume value ρ̄_ξ = ρ_ξ/φ_ξ for a phase ξ (ξ = s, f), which is the mineral state for the solid." Or drop the indexed form and write ρ̄_s = ρ_s/φ_s.

---

## OPTIONAL ITEMS

### R3-O1 — orthography is not one voice (two variants of the same word in one manuscript)

- `modelling`: `main.tex:58` (abstract), `main.tex:621` (Discussion), `sections/finite_elements.tex:283`.
- `modeling`: `sections/pore_fabric.tex:14`, `:68`, `:228`.

Both spellings of the same word appear, including inside the same sentence family ("shares … modelling conventions" / "a new modeling choice"). Additionally `colour` appears twice (`sections/finite_elements.tex:335`, `:370`) in a manuscript otherwise using US spelling (`normalize` at `:177`, `:250`; `color` = 0 occurrences). Harmless to the science, but it is the clearest "one voice" defect I found. A single pass with a consistent locale fixes it.

### R3-O2 — near-verbatim repetition between adjacent floats and one numeric fact asserted three times

1. The captions of the two adjacent refined-run floats are near-verbatim:
   - Fig. 10 (`sections/finite_elements.tex:362`): "Values are read from the recorded Exodus fields; the runs are finite-load demonstrations on synthetic parameters, not a mesh-convergence study."
   - Fig. 11 (`sections/finite_elements.tex:377`): "As in Figure 10, values are read from the recorded Exodus fields and the refined run is a finite-load demonstration, not a mesh-convergence study."
   The back-reference "As in Figure 10" is already there, so the repeated clause can be cut.
2. The pressure floor `3.2×10⁻³` is asserted three times within a few pages: §9.3 body (`:206`), the panel-(d) text of the Fig. 6 caption (`:231`), and the Discussion (`main.tex:600`). The first two are body/caption duplication of the same sentence.
3. `the four complementary modes are frozen to the mineral` recurs in `sections/pore_fabric.tex:249` and `sections/finite_elements.tex:266`, and `directionally asymmetric pressure coupling even when the mineral itself is isotropic` recurs in `sections/pore_fabric.tex:392` and `main.tex:652`. Both are conclusion-style restatements; acceptable, but tightening the second occurrence would reduce the echo.

### R3-O3 — float citation-to-caption page gaps

Captions and first citations (from the rendered PDF):

| Float | First cited | Caption | Gap |
|---|---|---|---|
| Fig. 1 | p. 16 | p. 17 | +1 |
| Fig. 2 | p. 18 | p. 18 | 0 |
| Fig. 3 | p. 18 | p. 19 | +1 |
| Fig. 4 | p. 18 | p. 19 | +1 |
| Fig. 5 | p. 20 | p. 20 | 0 |
| Fig. 6 | p. 24 | p. 25 | +1 |
| Fig. 7 | p. 24 | p. 26 | **+2** |
| Fig. 8 | p. 24 | p. 26 | **+2** |
| Fig. 9 | p. 24 | p. 27 | **+3** |
| Fig. 10 | p. 27 | p. 28 | +1 |
| Fig. 11 | p. 27 | p. 28 | +1 |

Figures 7–9 are all first cited from one summary paragraph on p. 24 but float to pp. 26–27. No figure appears after the References (References begin p. 32; last float p. 28), and there is no undefined reference or citation. This is a placement-tightening opportunity, not a correctness problem.

### R3-O4 — one underfull box in the abstract

`build/main.log:849`: `Underfull \hbox (badness 1137) in paragraph at lines 33--40`, i.e. the first abstract paragraph. The log contains **no** Overfull box, **no** undefined citation/reference, **no** missing-character glyph warning, and **no** `Font shape ... undefined`. A trivial `\looseness`/rewording fix in the abstract clears the only box warning in the document.

---

## 3. Claim-strength audit (every "verify/demonstrate/unique/exact/independent")

I recomputed or re-read each numeric and modal claim against the frozen artifacts. All of the following **match the artifacts**:

- Abstract "Independent energy and pressure derivatives verify the complete spatial phase-stress balance and its invariance under changes of the internal rotation" — supported: `build/conformal/verification.json` has `checks_passed = 186`; the rotation-invariance checks (`energy_rotation_independence`, `mixture_stress_rotation_independence`, `pressure_dependent_rotation_cancels`) are present. The wording "independent" is consistent with the manuscript's own careful distinction elsewhere ("that agreement is an implementation check, not an independent derivation", `sections/finite_elements.tex:281-283`); I read "independent" as "separate numerical route", which the artifact categories (`implementation`/`analytical`) support. No overstatement.
- "186 named checks … the 65 per-state identities (five states times thirteen identities …)" — verified: 5 states × 13 distinct identity names = 65, and the 186 count is the file's own `checks_passed`.
- "largest absolute error among its constitutive identities is 2.5×10⁻⁹" — `max_constitutive_identity_error = 2.4549890331732928e-09` → 2.5×10⁻⁹. Rounding is honest.
- "273 finite states across 13 mineral stiffnesses" — `site/reports/tensor-verification.json`: `materials 13`, `total_states 273`. Also `maximum_stress_strain_commutator = 2.61`, supporting "including noncoaxial states".
- "second-order convergence" of the constitutive step refinement — `observed_orders` ≈ 2.0004 (energy_stress), 2.0002 (pore_volume), ~2.0 (pressure).
- MMS spatial orders "pressure 2.00 and 2.00, u_x 2.99 and 2.96, u_y 3.00 and 2.96" — `fe-evidence/mms-convergence.json`: p naive_orders 1.9966/2.0008, ux 2.9917/2.9585, uy 2.9983/2.9600. Match.
- Temporal "0.98–1.40", "entries above unity", "no order above one is asserted" — the nine successive-difference orders at nx = 16/32/64 span 0.978–1.397. The hedge is exactly right.
- "linear step refinement … 3.7×10⁻³ and 7.1×10⁻³ at dt = 10⁻³ and 2×10⁻³ (ratio 1.94)" — `figures/fe_mandel_refinement.csv`: 0.003657958974355574 and 0.0071039215708695895; ratio 1.9421. Match.
- "floors at about 3.2×10⁻³ … rather than decaying as the load tends to 10⁻⁴" — `figures/fe_load_limit.csv`: `pressure_max_normalized = 0.0032209…` at load 1e-4, nx=20, dt=1e-3. Match, and the claim is correctly labelled a *floor*, not a limit.
- Fabric implementation numbers — all six match `build/fabric/fabric-verification.json` `tensor_checks`/`worst_probe_abs_diff`/`conformal_cross_check` exactly: reconstruction 2.22×10⁻¹⁶ ("2.2×10⁻¹⁶"), det **H**−1 = −3.33×10⁻¹⁶ ("−3.3×10⁻¹⁶"), ‖𝔻:**e**_3‖ = 1.58×10⁻¹⁶ ("1.6×10⁻¹⁶"), 𝔻:**e**_6 = 0, rotation invariance 2.50×10⁻¹⁶ ("2.5×10⁻¹⁶"), worst probe difference 4.88×10⁻¹⁵ ("4.9×10⁻¹⁵"), volume-only cross-check 1.87×10⁻¹⁴ ("1.9×10⁻¹⁴").
- Coupled peak pressures "4.36/4.99/5.52 ×10⁻⁵ … 3.62×10⁻⁵ uncoupled" — `figures/fe_fabric_mandel_peak.csv`: 4.3628/4.9901/5.5211/3.6164 ×10⁻⁵. Match, and "peak coincides with the final recorded state" is correct (`peak = final` in every row).
- Refined contours "3.61×10⁻⁵ isotropic; 4.35, 4.97, 5.50×10⁻⁵" and displacement "5.18/5.14/2.38/5.26×10⁻⁵" — `fe-evidence/runs/fabric_contour_*/analysis.json` and `figures/fe_fabric_contours.csv` (`u_mag_max` 5.1826/5.1372/2.3818/5.2587×10⁻⁵). Match. "the maximum lies on the X₁ = 0 symmetry line" — `p_max_x = 0.0` in every row. Match.
- Reference moduli: "K_s = 28K_*", "drained spherical-strain modulus K = 7K_*", "reference Biot components 0.7000, 0.7583, 0.7917", "G = 0.75", "reference Biot coefficient 0.6", "total storage 17/80", "isotropic mineral shear modulus 16.8K_*" — I recomputed all of these independently from the printed matrices and parameters in a scratch interpreter: K_s = 252/9 = 28; **B**₀ = (0.7, 0.75833, 0.79167); G = φ_s0 μ_s = 0.9·(5/6) = 0.75; B₀ = 1 − K/K_s = 0.6; (1−φ_s0)/K_f + S_s = 0.0125 + 0.2 = 0.2125 = 17/80; and μ_average = tr((I₆ − 𝟏⊗𝟏/3)ℂ_s)/10 = 168/10 = 16.8, which is exactly "the mean of the five deviatoric stiffness modes of ℂ_s, divided by two" under the manuscript's own Mandel convention (the rule correctly returns μ for an isotropic ℂ_s). Every one matches; the isotropic deck's `isotropic_stiffness(28,16.8)` reproduces 50.4/16.8/33.6 as expected.
- Uniqueness/existence claims — the "one positive root" argument at (37) is sound (RHS strictly increasing from −∞ to +∞ on J̄ > 0 for p ≥ 0 given 0 < K < φ_s0K_s), and "unique stationary point" on `range 𝔻` is sound (𝔻 + φ_s0ℂ_s positive definite on that subspace). The manuscript restricts both explicitly ("at negative pressure … need not be global", "no order above one is asserted"), so neither is overstated.
- "exact" claims (§7.6 "the inverse relation is exact", §9.4 "the reconstructed fabric is exactly (79)") — exact-by-construction, and the artifacts confirm at 10⁻¹⁶. Supported.
- Scope statements agree clause by clause across abstract / §9.4 "Scope of these results" / Discussion: the manufactured solution and the constant-coefficient consolidation reference are always tagged to the **constant reference tangent**, the rotated-anisotropy and partial-drainage runs are always "demonstrations, not verification", the fabric law is always an implementation check that **shares the section's modelling conventions**, and "no quantitative finite-deformation verification and no experimental validation" is claimed consistently in all three places. I checked this against §9.4's explicit partial-drainage exclusion ("their comparison with the slender Mandel reference geometry is therefore reported as not comparable and is excluded from the verification claims") and it is honoured: `site/reports/finite-deformation-summary.json` emits no reference-normalized field for the partial family. No unsupported claim found.

**Undefined-at-first-use terms:** no other term was found that appears only in a caption or a single sentence without introduction; `unjacketed`, `Mandel basis`, `drained`, `platen`, `solid storage`, and the overdot are all introduced at or before first substantive use. The only gaps are `ξ` (R3-C2) and the mislabelled tilde input (R3-C1).

---

## 4. Summary of the review

Two required items, both confined to the notation paragraph and both fixable in one clause each: one mis-stated decoration rule (R3-C1) and one never-defined index (`ξ`, R3-C2). Four optional polish items (orthography, float repetition, float placement, an underfull box). Nothing else: the snapshot is hash-clean, the equation numbering is continuous and complete, every cross-reference in the audited paragraph resolves to the intended equation, the log is free of undefined references/citations/overfull boxes/missing glyphs, and every quantitative claim I could check — including a full independent recomputation of the moduli and reference Biot components — matches the frozen artifacts, with claim strength appropriately hedged throughout.

VERDICT: MINOR REVISION
