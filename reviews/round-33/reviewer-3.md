# SIMULATED AI PEER REVIEW — Reviewer 3 (exposition, notation and claims)

This is a simulated AI peer review of a frozen manuscript snapshot. It is not
journal peer review and confers no acceptance.

- Repository (report written here): `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
- Immutable snapshot reviewed: `.agent-runtime/review-snapshots/round-33`
- Declared `SNAPSHOT_ID`: `7e75f419a105318fb1bec98caa19469a63f34efd25d41b79fb8ae055f37e3e53`
- Emphasis: exposition, notation and claims.
- All reading was done from the frozen snapshot only. The snapshot was treated
  as read-only; equation labels were resolved from `build/main.pdf` (via
  `pdftotext -layout`) and `build/main.log`, and from the snapshot source text.

---

## 1. Mandatory first checks

### 1.1 Manifest hash vs declared SNAPSHOT_ID

Command:

```
cd <snapshot>
cat SNAPSHOT_ID
sha256sum source-manifest.json
```

Result:

```
7e75f419a105318fb1bec98caa19469a63f34efd25d41b79fb8ae055f37e3e53   (SNAPSHOT_ID file)
7e75f419a105318fb1bec98caa19469a63f34efd25d41b79fb8ae055f37e3e53   (sha256 of source-manifest.json)
```

PASS. The `sha256` of `source-manifest.json` equals the declared `SNAPSHOT_ID`
exactly, and the `SNAPSHOT_ID` file holds the identical string.

### 1.2 Re-hash of every manifest entry plus a tree walk

Command (Python, run in the snapshot root): load `source-manifest.json`,
`sha256` every listed file and compare, then `os.walk` the tree and diff the
present set against the listed set (excluding `source-manifest.json` and
`SNAPSHOT_ID`, which cannot list themselves).

Result:

```
entry count                        608
entries re-hashed                  608
hash mismatches                    0
listed files missing on disk       0
files present but unlisted         0
```

PASS. 608/608 entries re-hashed and matched; no listed file is missing; no file
present in the tree is unlisted.

### 1.3 Independence declaration

I did not open any file under `reviews/` — including `reviews/README.md` — and
I did not read, list, glob or `find` any other
`.agent-runtime/review-snapshots/round-*` directory, any other reviewer's
report, or any verdict/acceptance count. I did not consult the working tree for
manuscript content; the only directory I created under `reviews/` is the one
holding this report. I self-report **no accidental exposure** to another
reviewer's report or to any verdict tally.

---

## 2. Scope: exposition, notation and claims against the rendered document

Resolved from `build/main.pdf` (33 pages, per `build/main.log`). Equation
numbers below are the *rendered* numbers. All source line numbers are lines in
the frozen snapshot files.

### 2.1 Every cross-reference in the notation paragraph lands correctly

The notation paragraph is `main.tex:222–258`. Each pointer resolves as follows
(snapshot label → rendered display → intended display?):

| Source pointer | Renders as | Display content | Intended? |
|---|---|---|---|
| `eq:true-mineral-jacobian` | (1) | `F = A F̄, J = a J̄, a = det A, J̄ = det F̄` | yes |
| `eq:rotated-mineral-cauchy` ("the rotation (6)") | (6) | `σ̄_s = R_A σ̂_s R_Aᵀ` | yes |
| `eq:kirchhoff-volume-conventions` | (10) | `τ' = J σ', τ̄_s = J̄ σ̄_s` | yes |
| `eq:fabric-distention-stress` | (72) | `S̄_dis = 2 ∂W_dis/∂G`, `δW_dis = ½ S̄_dis : δG` | yes |
| `eq:single-prime` (`eq:total-cauchy-single-prime`) | (8) | `σ' = σ + p I` | yes |
| `eq:fixed-pressure-stress` | (46) | `P'' = ∂W''/∂F|_p` | yes |
| `eq:finite-biot-tensor` | (49) | `σ = σ'' − p B`, `B = I − …Fᵀ` | yes |
| `eq:reduced-energy` | (44) | `W''(F,p) = W_s(F, J̄(F,p))` | yes |
| `eq:legendre-energy` | (45) | `W'(F,p) = W'' + φ_s0 p J̄` | yes |
| `eq:drained-stiffness-restriction` | (40) | `C^d = φ_s0 C_s − …` | yes |
| `eq:prescribed-logarithmic-energies` | (29) | `W̄_s = ½ ε̄:C_s:ε̄`, `W^d = ½ ε:C^d:ε` | yes |
| `eq:fe-fluid-residual` | (96) | fluid residual containing `Q̄_f` | yes |
| `sec:finite-biot` | section 5 | "Pressure coupling at finite deformation" | yes |
| `sec:work-equivalence` (`W_A(a)`) | section 3 | "Reversible work and the equivalent energy" | yes |
| `sec:pore-fabric` | section 7 | "Pore fabric and shape-changing distention" | yes |

**No pointer lands on the wrong display.** Every rendered number in the notation
paragraph matches the equation it is meant to name. In particular the three
pointers most at risk — the distention-stress definition (72), the boundary
flux (96), and the rotation (6) — are all correct.

The companion in-text pointer at `sections/pore_fabric.tex:701`
(`\eqref{eq:energy-returned-pressure-balance} → (22)`, "equivalently, the trace
of `\eqref{eq:constitutive-kirchhoff-phase-stress} → (12)`") also resolves to
the intended displays.

### 2.2 Labels defined but never referenced

Across `main.tex` and `sections/*.tex`: 138 labels defined, 68 distinct labels
referenced, **0 references to undefined labels**. 70 labels are defined but
never cross-referenced (67 equation labels and 3 section labels:
`sec:conclusion`, `sec:compatibility`, `sec:stress-reconstruction`, plus the
fabric/finite-element subsection labels). This is normal for a manuscript of
this length and is **not** a defect; recorded here per the review scope
(R3-O6).

### 2.3 Completeness of the notation rules

The marks actually used across the manuscript are: bar (on `F, C, U, ε, W_s,
σ_s, τ_s, S_dis, ρ_s, ρ_f, Q_f`), hat (`σ_s, τ_s`), tilde (`τ`), single prime
(`σ', τ', P', W'`), double prime (`σ'', P'', W''`), superscript `d`
(`C^d, W^d`), superscript `+` (`D^+`), and subscript `dis`.

Checked against the stated rules:

- **Barred kinematic/energetic quantities** (`F, C, U, ε, W_s`) — covered by the
  first bar rule (`main.tex:222–226`). OK.
- **Barred intrinsic densities** (`ρ̄_s, ρ̄_f, ρ̄_{s0}, ρ̄_{f0}`) — covered by
  "A bar on an intrinsic density denotes the per-phase-volume value
  `ρ̄_ξ = ρ_ξ/φ_ξ`". OK.
- **Barred stresses and their normalizations** (`σ̄_s` per current mineral
  volume, `τ̄_s` per reference mineral volume) — covered, and the two volumes are
  correctly distinguished (`J̄` vs current mineral volume). OK.
- **`S̄_dis` vs `S_dis`** — the stated rule
  (`main.tex:228–234`) says the bar marks "the member of the work-conjugate pair
  that is conjugate to the distention tensor `G`, per reference mixture volume
  in the intermediate frame, its unbarred partner `S_dis` being conjugate to the
  distention logarithmic strain `E_dis` in that same frame and normalization."
  I re-derived the definitions (`sections/pore_fabric.tex:695–702`):
  `S̄_dis = 2 ∂W_dis/∂G` with `δW_dis = ½ S̄_dis : δG` (conjugate to `G`), and
  `S_dis = ∂W_dis/∂E_dis` with `δW_dis = S_dis : δE_dis` (conjugate to
  `E_dis`). **The stated rule describes exactly what the definitions differ by**
  (conjugate variable and the factor ½ absorbed in the `2 ∂/∂G` convention), and
  both are per reference mixture volume in the intermediate frame. Confirmed
  consistent.
- **Hat = true frame** (`σ̂_s, τ̂_s`) — covered and used only on those two
  symbols. OK.
- **Primes / double primes** — the paragraph correctly assigns single prime to
  the effective stress carrying the full pore-pressure term (`σ', τ', P'`) and
  double prime to the fixed-pressure stress (`σ'', P''`), then states that the
  *same two marks* name the reduced energies `W''` of (44) and `W'` of (45).
  Both are used correctly in the body. OK.
- **`d` (drained) vs `dis` (distention)** — explicitly separated, with the
  sentence "The two labels are kept distinct throughout, so `d` never means
  distention." I verified no counter-example exists in the source. OK.
- **`W_A(a)`** — correctly identified as the scalar volume-only distention energy
  of section 3 and as the volume-only specialization of `W_dis`. OK.

Two marks are used in the manuscript but are **not** enumerated in the notation
paragraph, although both are defined at their point of use:

- the **tilde** in `τ̃ = R_Aᵀ τ' R_A` (`sections/pore_fabric.tex:172,178`);
- the **superscript `+`** in `D^+` (Moore–Penrose inverse,
  `sections/pore_fabric.tex:783–786`).

Both are introduced inline, so no reader is stranded. Recorded as R3-O1.

### 2.4 Abstract, body and conclusion scope statements

Compared clause by clause; the scope disclaimers agree and each is supported by
the frozen evidence.

- Abstract FE clause ("verified against a manufactured solution for the constant
  reference tangent and, in the same limit, the constant-coefficient
  consolidation reference, and exercised on rotated-anisotropy and
  partial-drainage demonstrations at finite load; no quantitative
  finite-deformation verification and no experimental validation are claimed")
  matches `main.tex:45–56`, `sections/finite_elements.tex:201–215`,
  `sections/finite_elements.tex:379–397`, and the conclusion
  (`main.tex:594–610`). Evidence exists for exactly those claims
  (`fe-evidence/mms-convergence.json`; `figures/fe_mandel_refinement.csv`;
  `fe-evidence/runs/{anisotropic_*,partial_*}`).
- Abstract fabric clause ("implemented in its reference-state linearization and
  checked at the material point against a separate re-implementation … that
  shares the same modelling conventions") matches
  `sections/finite_elements.tex:267–284`, including the explicit disclaimer that
  the check "is an implementation check, not an independent derivation". Good
  self-limitation.
- The conclusion's added clause "At finite load … floors at about
  `3.2×10⁻³` … ratio `1.94` … temporal orders at `nx=16/32/64` are `0.98–1.40`
  … no order above one is asserted" (`main.tex:598–605`) is fully supported (see
  §2.5). No clause in the abstract is stronger than the body or the evidence.

### 2.5 Claim-strength audit ("verify / verified / demonstrate / unique / exact / independent")

Every such claim was recomputed from the frozen artifacts:

| Claim (source) | Artifact | Verdict |
|---|---|---|
| "186 named checks" (`experiments.tex:181`) | `build/conformal/verification.json` `checks_passed=186`; my count of the `checks` object = 67 legacy + 12 analytical + 48 anisotropic + 54 isotropic + 1 + 1 + 3 = 186 | exact match |
| "65 per-state identities (five states × thirteen identities)" | 5 `legacy_state0..4` × 13 identity keys = 65 | exact match |
| "the two reference Biot and rank-one compliance relations" | `legacy_reference_biot`, `legacy_reference_rank_one_compliance_identity` (67 − 65 = 2) | exact match |
| "largest absolute error … 2.5×10⁻⁹" | `max_constitutive_identity_error = 2.4549890331732928e-09` | match |
| "second-order convergence" of energy/pore-volume/pressure step refinement | `observed_orders` all ≈ 2.00 (last pressure 1.989) | match |
| "273 finite states across 13 mineral stiffnesses" | `site/reports/tensor-verification.json` `total_states=273`, `materials=13`, `states_per_material=21` | exact match |
| MMS spatial orders "pressure 2.00 and 2.00, ux 2.99 and 2.96, uy 3.00 and 2.96" | `mms-convergence.json` `naive_orders`: p 1.9966/2.0008; ux 2.9917/2.9585; uy 2.9983/2.9600 | match |
| temporal "0.98–1.40, including values above one" | `difference_orders` set = {0.978, 1.015, 1.025…} to 1.397 | match (range 0.978–1.397) |
| "linear step refinement … ratio 1.94" | `fe_mandel_refinement.csv`: 0.0071039215708695895 / 0.003657958974355574 = 1.942 | match |
| floor "3.2×10⁻³"; step errors "3.7×10⁻³ and 7.1×10⁻³" | `fe_load_limit.csv` 0.0032209; `fe_mandel_refinement.csv` 0.0036579 / 0.0071039 | match |
| fabric reconstruction "2.2×10⁻¹⁶", "det H − 1 = −3.3×10⁻¹⁶", "‖D:e₃‖ = 1.6×10⁻¹⁶", "D:e₆ = 0", rotation invariance "2.5×10⁻¹⁶", NumPy worst "4.9×10⁻¹⁵", conformal limit "1.9×10⁻¹⁴" | `build/fabric/fabric-verification.json` `tensor_checks` and `conformal_cross_check` (2.220e-16, −3.331e-16, 1.582e-16, 0.0, 2.497e-16, 4.885e-15, 1.874e-14) | all match |
| coupled peaks "4.36, 4.99, 5.52, 3.62 ×10⁻⁵" | `figures/fe_fabric_mandel_peak.csv` | match |
| refined peaks "3.61, 4.35, 4.97, 5.50 ×10⁻⁵" and displacement peaks "5.18, 5.14, 2.38, 5.26 ×10⁻⁵" | `figures/fe_fabric_contours.csv` (3.6062, 4.3491, 4.9737, 5.5031; 5.1826, 5.1372, 2.3818, 5.2587 ×10⁻⁵) | match |
| "reference Biot components are 0.7000, 0.7583, 0.7917" | `build/conformal/experiments.json` `reference_B` | match |
| isotropic comparison shear modulus "16.8 K_*, the mean of the five deviatoric stiffness modes divided by two" | computed deviatoric eigenvalues of `C_s` = {20, 24, 28, 42.9668, 53.0332}, mean 33.6, /2 = 16.8 | exact match |
| FE reference "G = 0.75", "Biot coefficient 0.6", "total storage 17/80" | `φ_s0 μ_s = 0.9 × 5/6 = 0.75`; `1 − K/K_s = 1 − 1/2.5 = 0.6`; `(1−φ_s0)/K_f + S_s = 0.0125 + 0.2 = 0.2125 = 17/80` | all match |
| "noncoaxial states and repeated stretches" | `noncoaxial_commutator = 0.1816 (>0)`; `exact_repeated_eigenvalue_log_derivative` check present | supported |

**Uniqueness and convergence claims are appropriately scoped.** The uniqueness
statements are confined to the reference quadratic model
(`sections/pore_fabric.tex:216` "the stationary point exists and is unique in
the reference quadratic model of §7.5"; `:286` "the condition for the unique
stationary point … on that subspace"). No global-uniqueness or global-stability
claim is made, and the paper explicitly states that "local scalar stability does
not establish stability against all deformation modes"
(`sections/experiments.tex:196`). The temporal-order claim is measured and
explicitly refuses to assert an order above one. I found **no inflated claim**.

### 2.6 Prose quality and consistency

- **Voice**: the revised prose reads as one voice; I found no verbatim duplicate
  prose lines across `main.tex` and `sections/*.tex` (the only repeated source
  lines are equation lines, which is expected).
- **Terms used before definition**: I checked the marked-symbol vocabulary (§2.3)
  and the running terms. The one real exception is **"spherical-gauge"**, used
  once at `sections/experiments.tex:191` and defined nowhere in the manuscript
  (see R3-C1). `unjacketed` is defined at first use (`limits.tex:74–78`);
  `Mandel basis` is defined at first use (`experiments.tex:9–22`).
- **Explanatory sequence (purpose → relation → variables → consequences)**: holds
  throughout the derivations in sections 2–7; the results sections follow the
  pattern claim → figure → caveat consistently.
- **Recently revised passages**: the finite-element scope paragraph and the
  conclusion read as *more* cautious than the headline claims, not less; no
  passage was found that inflates a claim relative to §2.5.

### 2.7 Float placement

From `build/main.pdf` (first *citation* page vs *caption* page, in PDF pages):

| Figure | First citation | Caption |
|---|---|---|
| 1 | 16 | 17 |
| 2 | 16 | 17 |
| 3 | 18 | 18 |
| 4 | 18 | 19 |
| 5 | 19 | 19 |
| 6 | 23 | 24 |
| 7 | 23 | 25 |
| 8 | 25 | 26 |
| 9 | 25 | 26 |
| 10 | 25 | 27 |
| 11 | 25 | 27 |

Every figure is cited on or before its caption page (never cited after
appearing). "References" begins on page 31; **no figure caption appears after
the References** (last caption page 27). PASS.

### 2.8 Rendered-PDF hygiene

- **Undefined references/citations**: none. `build/main.log` contains no
  "Reference … undefined" or "Citation … undefined" warning, no "multiply
  defined labels", and no "Label(s) may have changed".
- **Citations resolve**: all 36 cite keys used in `main.tex`/`sections/*.tex`
  have entries in `references.bib`, and every bib entry is cited (including
  `walker2023poroelasticity` via `\cite[appendix D]{…}`).
- **Missing glyphs**: no "Missing character" warning.
- **Overfull/underfull boxes**: exactly one — `Underfull \hbox (badness 1137) in
  paragraph at lines 33--40` (`main.tex`, inside the abstract). No overfull
  boxes. Cosmetic only (R3-O7).
- **Equation-numbering continuity**: displayed equations run (1)–(106) with no
  gaps and no duplicates.
- **Embedded supplement**: `pdfdetach -list` reports one embedded file
  (`anisotropic-biot-2026-09-20-v2.zip`); its extracted `sha256`
  (`ab993ee7…4d04`) is byte-identical to `build/anisotropic-biot-2026-09-20-v2.zip`.
- **Duplicated/tautological text**: see R3-O2 and R3-O3.

---

## 3. REQUIRED changes

### R3-C1 — `sections/experiments.tex:191` — undefined technical term "spherical-gauge"

Text: "The **spherical-gauge** suite separately checks 273 finite states across
13 mineral stiffnesses". The modifier "spherical-gauge" appears exactly once in
the manuscript and is defined nowhere in `main.tex` or any `sections/*.tex`
(the term originates in repository tooling, e.g. `tools/populate_site_manifest.py`
and `README.md`). A reader of the manuscript cannot tell what property is
"gauged" or why the gauge is spherical.

Required: either define the term at first use (one clause stating what quantity
is fixed/gauged in that suite) or replace the modifier with a self-explanatory
description. This is a text-only change; the underlying count of 273 states
across 13 stiffnesses is correct and needs no change.

### R3-C2 — `main.tex:228–229` — broken clause in the notation paragraph

Text: "… is per reference mineral volume, **and written on the distention stress
`S̄_dis` of (72), a bar instead marks** the member of the work-conjugate
pair …".

The participial clause has no subordinator, so the sentence reads as if the bar
"is written on" the distention stress; the intended meaning is "and, *when*
written on the distention stress `S̄_dis` of (72), a bar *instead* marks …".
This is the single hardest sentence to parse in the notation paragraph, which is
otherwise precise.

Required: repair the grammar (e.g. insert "when" and a comma, or split into two
sentences) without changing the rule, which §2.3 confirms is correct.

---

## 4. OPTIONAL notes

- **R3-O1** (`main.tex:222–258`; `sections/pore_fabric.tex:172,178,783–786`):
  the tilde on `τ̃ = R_Aᵀ τ' R_A` and the superscript `+` on the Moore–Penrose
  inverse `D^+` are not enumerated among the marks in the notation paragraph.
  Both are defined at their point of use, so this is optional; adding two short
  clauses would make the enumeration exhaustive.
- **R3-O2** (`sections/finite_elements.tex:361` and `:375`): the captions of
  Figures 10 and 11 end with the identical clause "… Values are read from the
  recorded Exodus fields; the runs are finite-load demonstrations on synthetic
  parameters, not a mesh-convergence study." Adjacent identical sentences are
  mildly tautological; one could be varied.
- **R3-O3** (`main.tex:594–610`): the conclusion restates the finite-element
  floor, step-refinement ratio, and temporal-order range in the same numerical
  detail as `sections/finite_elements.tex:201–215`. It is defensible in a
  conclusion, but the duplication of specific digits is heavier than usual.
- **R3-O4** (`sections/finite_elements.tex:331–332`): the reported 45°-fabric
  displacement-magnitude peak (`2.38×10⁻⁵`) is roughly half the other three
  (`5.18`, `5.14`, `5.26 ×10⁻⁵`). The value matches the artifact
  (`figures/fe_fabric_contours.csv`) exactly, so the claim is supported, but the
  paper reports it with no comment. A one-clause remark (or a note that the peak
  location differs) would prevent a reader from reading it as anomalous.
- **R3-O5** (`sections/experiments.tex:181–185`): "the two reference Biot and
  rank-one compliance relations **used to establish** the specialization" — these
  relations verify rather than establish the specialization; "used to verify" or
  "characteristic of" would be more precise.
- **R3-O6**: 70 labels (67 equations, 3 sections/subsections) are defined but
  never cross-referenced. Normal for this length; listed only because the review
  scope requested it. No action implied.
- **R3-O7** (`main.tex:33–40`): one underfull `\hbox` (badness 1137) inside the
  abstract. Cosmetic.

---

## 5. Assessment

All three mandatory checks pass exactly. The notation paragraph's every
cross-reference resolves to the intended display, and the distention-stress
pair, the reduced energies, the `d`/`dis` distinction, and the stress
normalizations are all stated correctly. Every numerical claim I checked —
constitutive-suite counts, MMS and temporal orders, step-refinement ratio, the
load floor, the fabric reconstruction residuals, the coupled and refined peaks,
the isotropic-comparison modulus, and the finite-element reference coefficients
— is reproduced by the frozen artifacts. The build is clean (no undefined
references, no missing glyphs, no overfull boxes, continuous equation
numbering), the embedded supplement is byte-identical to the shipped archive,
and no float is displaced after the References. The scope statements in the
abstract, body and conclusion agree clause by clause, and the uniqueness and
convergence claims are properly scoped.

The manuscript is in substance ready; the two required items are local,
text-only exposition repairs (one undefined modifier, one ungrammatical clause)
and neither touches a derivation, a claim, or an artifact.

VERDICT: MINOR REVISION
