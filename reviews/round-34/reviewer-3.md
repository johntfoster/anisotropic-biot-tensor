# SIMULATED AI PEER REVIEW — Reviewer 3 of 3

**Manuscript:** *An anisotropic Biot tensor from mineral stress and distention work* (John T. Foster)
**Repository:** `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
**Immutable snapshot reviewed:** `.agent-runtime/review-snapshots/round-34`
**Declared SNAPSHOT_ID:** `a2d99a3960d08ac9a8b1e9d333a0f77fb676a240b29e0ed528b9d1b308b3ea1e`
**Emphasis:** exposition, notation and claims.
**Note:** This is a simulated AI peer review. It is not journal peer review and confers no acceptance. All readings, equation numbers and numbers below were taken only from the frozen snapshot; the working tree was used only to write this file.

---

## 1. Mandatory checks

### 1.1 Manifest hash equals declared SNAPSHOT_ID

```
cd /home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/review-snapshots/round-34
sha256sum source-manifest.json
cat SNAPSHOT_ID
```

Result:

```
a2d99a3960d08ac9a8b1e9d333a0f77fb676a240b29e0ed528b9d1b308b3ea1e  source-manifest.json
a2d99a3960d08ac9a8b1e9d333a0f77fb676a240b29e0ed528b9d1b308b3ea1e
```

**PASS.** `sha256(source-manifest.json)` equals the declared SNAPSHOT_ID exactly, and `SNAPSHOT_ID` holds the same 64-hex string.

### 1.2 Every listed file re-hashed

Re-hashed each `repository-relative path -> sha256` entry of `source-manifest.json` with `hashlib.sha256`, then walked the snapshot tree with `os.walk` for unlisted files.

| Quantity | Result |
|---|---|
| Manifest entry count | **608** |
| Entries re-hashed OK | **608** |
| Hash mismatches | **0** |
| Listed files missing on disk | **0** |
| Files present but unlisted (walk, excluding `source-manifest.json` and `SNAPSHOT_ID`) | **0** |
| Total files on disk | 610 (608 listed + the two non-self-listable files) |

**PASS.** As the task allows, `source-manifest.json` and `SNAPSHOT_ID` cannot list themselves; both are present, and the 608+2 = 610 total accounts for every file in the tree.

### 1.3 Independence declaration

I did **not** open any file under `reviews/`, including `reviews/README.md`. I did **not** read, list, glob or `find` any other `.agent-runtime/review-snapshots/round-*` directory, any other reviewer's report, or any verdict/acceptance count.

Self-reported accidental exposure: while orienting myself in the repository I ran a single `ls -la reviews/` in the **working tree** (not the snapshot) to confirm that `reviews/round-34/` did not yet exist. That listing printed only directory *names* (`foster-cycle-*`, `round-1` … `round-33`) and `README.md`; no report file was opened, no file content was read, no verdict or count was observed. I did not repeat or extend that listing. I believe my vote is untainted; I report the exposure for transparency.

---

## 2. Cross-reference audit of the notation paragraph (emphasis core)

The notation paragraph is `main.tex:215–256`. Equations were resolved from the rendered `build/main.pdf` (`pdftotext -layout`, then per-page extraction), not from `build/main.aux` (not shipped). Every cross-reference in the paragraph was located in the source, then matched to its rendered display.

| `main.tex` line | Source pointer | Renders as | Display it lands on | Intended? |
|---|---|---|---|---|
| 219 | `\eqref{eq:true-mineral-jacobian}` | (1) | `F = A F̄, J = aJ̄, a = det A, J̄ = det F̄` | yes |
| 220 | `\eqref{eq:spherical-distention}` | (2) | `A = a^{1/3}R_A, R_A^T R_A = I, det R_A = 1, F̄ = a^{-1/3}R_A^T F` | yes |
| 227 | `\eqref{eq:kirchhoff-volume-conventions}` | (10) | `τ' = Jσ', τ̄_s = J̄σ̄_s` | yes |
| 229 | `\eqref{eq:fabric-distention-stress}` | (72) | `S̄_dis = 2 ∂W_dis/∂G` | yes |
| 235 | `\eqref{eq:fe-fluid-residual}` | (96) | fluid mass residual carrying `Q̄_f` | yes |
| 238 | `\eqref{eq:total-cauchy-single-prime}` | (8) | `σ' = σ + pI` | yes |
| 239 | `\eqref{eq:fixed-pressure-stress}` | (46) | `P'' = ∂W''/∂F|_p` | yes |
| 241 | `\eqref{eq:finite-biot-tensor}` | (49) | `σ = σ'' − pB` | yes |
| 242 | `\cref{sec:finite-biot}` | Section 5 | Pressure coupling at finite deformation | yes |
| 243 | `\eqref{eq:reduced-energy}` | (44) | `W''(F,p) = W_s(F, J̄(F,p))` | yes |
| 244 | `\eqref{eq:legendre-energy}` | (45) | `W'(F,p) = W'' + φ_s0 p J̄` | yes |
| 246 | `\eqref{eq:drained-stiffness-restriction}` | (40) | drained stiffness restriction | yes |
| 247 | `\eqref{eq:prescribed-logarithmic-energies}` | (29) | `W̄_s` and `W^d` definitions | yes |
| 250 | `\cref{sec:pore-fabric}` | Section 7 | Pore fabric and shape-changing distention | yes |
| 251 | `\cref{sec:work-equivalence}` | Section 3 | Reversible work and the equivalent energy | yes |
| 255 | `\eqref{eq:rotated-mineral-cauchy}` | (6) | `σ̄_s = R_A σ̂_s R_A^T` | yes |

**Result: no pointer in the notation paragraph lands on a wrong display.** I found no mis-targeted cross-reference anywhere in `main.tex` or `sections/*.tex`; the build log contains no undefined-reference or multiply-defined-label warning (`grep -n "LaTeX Warning" build/main.log` → empty; `grep -in "undefined" build/main.log` → empty), and a source-side check of all 138 `\label{}` keys found **zero** references to undefined labels.

Labels defined but never referenced: **69** (60 `eq:*` and 9 `sec:*` — `sec:compatibility`, `sec:conclusion`, `sec:fabric-energy`, `sec:fabric-kinematics`, `sec:fabric-mass`, `sec:fabric-transverse`, `sec:fe-fluid-closure`, `sec:fe-weak-balances`, `sec:stress-reconstruction`). These are harmless numbering anchors; see R3-O5.

---

## 3. Notation-rule completeness

Every **barred** symbol used anywhere in `main.tex` and `sections/*.tex` is covered: `\bar C, \bar F, \bar J, \bar\sigma, \bar\tau, \bar U, \bar\varepsilon, \bar W_s` (kinematic/energetic bar, `main.tex:217–220`); `\bar\rho_\xi` (intrinsic-density bar, `main.tex:221–222`); `\bar\sigma_s, \bar\tau_s` with the two normalizations (stress bar + normalization, `main.tex:223–227`); `\bar S_dis` with its stated exception (distention-stress bar, `main.tex:228–233`); `\bar Q_f` (prescribed-boundary-datum bar, `main.tex:234–235`). **Hatted**: `\widehat\sigma_s, \widehat\tau_s` (true-frame rule, `main.tex:223–224`). **Primed/double-primed**: `σ', P', τ', σ'', P'', W'', W'` all covered (`main.tex:236–244`).

The five items the task asks about specifically are all now present and mutually consistent:

* `W''` of (44) and `W'` of (45) — stated, `main.tex:241–244`.
* the pair `S̄_dis` / `S_dis` with frame and normalization — stated, `main.tex:228–233`; consistent with `sections/pore_fabric.tex:210–215`.
* `W_A(a)` and the normalization of both `W_A` and `W_dis` — `main.tex:249–253` ("both energies are normalized per reference mixture volume"). Verified consistent with (19)/(34) and (71), where `W_s` is per reference mixture volume and `φ_s0 W̄_s` is per reference mineral volume.
* drained superscript `d` versus distention subscript `dis` — `main.tex:245–254`, including the explicit disambiguation "so `d` never means distention".
* stress normalizations — `main.tex:224–227` and the sentence after (6).

Uncovered decorations: the time-level superscript `n` in `m_f^{\,n}`, `F^n`, `p^n`, `t_n` (eq. (97), `sections/finite_elements.tex:120–123`) has no stated rule → **R3-C3**. The wide tilde `\widetilde\tau` of eq. (73) (`sections/pore_fabric.tex:172,178`) is defined at its point of use but is not covered by the notation paragraph → R3-O3. The reference subscript `0` (`φ_{s0}`, `\bar\rho_{s0}`, `B_0`, `\bar\rho_{f0}`) first appears in eqs. (4)–(5) with no stated rule → R3-O4. `^T` (transpose) and `\mathbb D^+` (Moore–Penrose, defined at use) are universal/local.

---

## 4. Grammar and parse-ability of the notation paragraph

Read sentence by sentence in the rendered form (`build/main.pdf`, pp. 3–4), the paragraph parses on a first reading. Three residual weaknesses:

1. `main.tex:215` — "Let \(\bar\rho_s\) be solid intrinsic density, \(\phi_s\) the current solid volume fraction, and \(\rho_s=\phi_s\bar\rho_s\) the solid mass per current mixture volume." The first member of the parallel triad drops the article carried by the other two ("**the** current solid volume fraction", "**the** solid mass"). Reads as a slip, not as an error. → R3-O1.
2. `main.tex:219–220` — "of which the conformal factor (2) is the specialization." Equation (2) is the conformal specialization of the *distention gradient* `A`, not a "factor"; elsewhere the manuscript says "the conformal specialization" (see `sections/pore_fabric.tex:50–57`). Slightly loose phrasing. → R3-O3b (folded into R3-O1 group).
3. `main.tex:255` — "The two stress representations differ by the rotation (6)." This sentence follows the `d`/`dis` discussion but resumes the bar/hat stress discussion from `main.tex:223–227`. "The two stress representations" therefore has a distant antecedent and is momentarily ambiguous against the immediately preceding sentence. Cohesion, not grammar. → R3-O2.

The long sentence at `main.tex:228–233` (44 words, semicolon-joined) parses, but the phrase "per reference mixture volume in the intermediate frame" attaches ambiguously to either "marks the member" or "conjugate to the distention tensor `G`". Not an error; noted for clarity.

---

## 5. Rendered-PDF hygiene

* `pdfinfo build/main.pdf`: 34 pages, letter, LuaTeX-1.14.0.
* `grep -n "LaTeX Warning" build/main.log` → **none**. `grep -in "undefined" build/main.log` → **none**. `grep -in "Missing character" build/main.log` → **none** (no missing glyphs).
* `grep -nE "Overfull|Underfull" build/main.log` → one entry only: `Underfull \hbox (badness 1137)` at log line 849, and the log context shows it is in the **bibliography** (`build/main.bbl`, the entry ending "Rock Mechanics and Rock Engineering, 54(1):377--396, 2021."), not in the manuscript body. No overfull boxes.
* Equation-numbering continuity: parsing every display number from `build/main.txt` gives 109 end-of-line matches covering **1 … 106 with no gap**. The three apparent "duplicates" (10, 12, 37) are inline references that happen to end a text line (`… of (10)`, `… Setting p = 0 in (37)`), not repeated displays. Numbering is continuous and monotone.
* No figure appears after the References. References heading is on **p. 32**; the last figure caption is on **p. 28**.

---

## 6. Float placement

`build/main.aux` is not shipped, so first-citation pages were resolved from the rendered text and compared with the caption pages.

| Figure | First citation page | Caption page | Δ |
|---|---|---|---|
| 1 `fig:conformal-pressure` | 16 | 17 | +1 |
| 2 `fig:conformal-shear` | 18 | 18 | 0 |
| 3 `fig:conformal-directional` | 18 | 19 | +1 |
| 4 `fig:conformal-rotation` | 18 | 19 | +1 |
| 5 `fig:conformal-layer` | 20 | 20 | 0 |
| 6 `fig:fe-verification` | 24 | 25 | +1 |
| 7 `fig:fe-reference-comparison` | 24 | 26 | +2 |
| 8 `fig:fe-fabric-probe` | 24 | 26 | +2 |
| 9 `fig:fe-fabric-mandel` | 24 | 27 | +3 |
| 10 `fig:fe-fabric-contours` | 27 | 28 | +1 |
| 11 `fig:fe-fabric-diffusion` | 27 | 28 | +1 |

No figure is captioned before its first citation, and none lands after the References. The drift for Figures 7–9 (+2/+2/+3) is the usual `[htbp]` deferral under a figure-dense section; see R3-O7.

---

## 7. Abstract / body / conclusion scope agreement and claim strength

I checked the abstract clause by clause against the body and the conclusion, and checked each claim-bearing number against the frozen artifacts (recomputed from CSVs/JSON; the held suites were **not** run).

| Claim | Artifact | Result |
|---|---|---|
| Reference Biot components 0.7000 / 0.7583 / 0.7917 (`sections/experiments.tex:27`) | recomputed from (40)+(57) with the stated `C_s`, `φ_s0=0.6`, `K=7K_*`, `K_s=28K_*` | 0.700000, 0.758333, 0.791667 — **match** |
| `K_s = 28 K_*`; isotropic shear `16.8 K_*` = mean of the five deviatoric Mandel modes ÷ 2 | Mandel eigenvalues 20, 24, 28, 41.98, 51.79, 86.23; `3K_s = 84`; (252−84)/5/2 = 16.8 | **match** |
| MMS spatial orders p 2.00/2.00, `u_x` 2.99/2.96, `u_y` 3.00/2.96 | `fe-evidence/mms-convergence.json` `space.orders.*.naive_orders` = 1.9966/2.0008, 2.9917/2.9585, 2.9983/2.9600 | **match** |
| Temporal orders "between 0.98 and 1.40" | `time.nx16/32/64` `difference_orders` min 0.9783, max 1.3969 | **match** |
| Linear step-refinement 3.7e-3 and 7.1e-3 at `dt=1e-3`/2e-3, ratio 1.94 | `figures/fe_mandel_refinement.csv` `linear_time_` 0.003658 / 0.007104; ratio 1.942 | **match** |
| Pressure discrepancy floors at ≈3.2e-3 | `figures/fe_load_limit.csv` `nonlinear_load_0.0001` `pressure_max_normalized` = 0.0032209 | **match** |
| Suite has 186 named checks; 65 = 5 states × 13 identities | `site/reports/conformal-verification.json` `checks_passed=186`; `legacy_state*` keys = 65 (13 per state) | **match** |
| Largest constitutive-identity error 2.5e-9 | `max_constitutive_identity_error` = 2.4549890331732928e-09 | **match** |
| Second-order step refinement of energy/pore-volume/pressure | `observed_orders` ≈ 2.0000/2.0002/2.0003 (and 1.989 for the last pressure level) | **match** |
| 273 finite states across 13 mineral stiffnesses | `site/reports/tensor-verification.json` `total_states=273`, `materials=13` | **match** |
| Fabric reconstruction 2.2e-16; `det H − 1 = −3.3e-16`; `‖D:e₃‖ = 1.6e-16`; `D:e₆ = 0`; rotation invariance 2.5e-16 | `site/reports/fabric-verification.json` `tensor_checks` = 2.220e-16, −3.331e-16, 1.582e-16, 0.0, 2.497e-16 | **match** |
| NumPy re-implementation worst difference 4.9e-15 | `worst_probe_abs_diff` = 4.88498e-15 (max over `analysis.json` cases = 4.885e-15) | **match** |
| Volume-only limit reproduces conformal material to 1.9e-14 | `conformal_cross_check` max abs diff = 1.874e-14 (σ11) | **match** |
| Peak centre pressures 4.36/4.99/5.52e-5 vs 3.62e-5 uncoupled | `figures/fe_fabric_mandel_peak.csv` 4.3628/4.9901/5.5211/3.6164e-5 | **match** |
| Refined-mesh peaks 3.61e-5 iso, 4.35/4.97/5.50e-5; `|u|` peaks 5.18/5.14/2.38/5.26e-5; `p_max` on `X₁=0`, zero at `X₁=1` | `figures/fe_fabric_contours.csv` | **match** |
| "Independent Lambert-function solutions check … negative-pressure states and a large positive-pressure state" | `site/reports/conformal-verification.json` `branch_pressure_-14/-13/800_*`; `scipy.special.lambertw` in `examples/verify_conformal.py` | **supported** |

Scope statements are consistent across abstract, body and conclusion, and each is hedged no more weakly than the evidence requires: the abstract's "exercised on rotated-anisotropy and partial-drainage demonstrations at finite load; no quantitative finite-deformation verification and no experimental validation are claimed for those demonstrations" agrees with the `sections/finite_elements.tex:379–397` scope paragraph and with `main.tex:610–618`; the "shares the same modelling conventions" caveat on the NumPy re-implementation appears identically in the abstract, in `sections/finite_elements.tex:276–282`, and in the conclusion. "Verified" is confined to the constant reference tangent (MMS and consolidation reference); the nonlinear finite-load runs are "demonstrations"; no convergence order above one is asserted for the temporal sequence; and the MMS spatial orders are labelled as measured adjacent orders, not fitted. I found **no claim that the artifacts do not support**.

Uniqueness claims are scoped and analytic: `sections/pore_fabric.tex:212–217` and `:284–287` claim existence and uniqueness only "in the reference quadratic model", where `D + φ_s0 C_s` is positive definite on `range D` — a valid argument, and the two occurrences are consistent. No convergence claim beyond the floors is made.

---

## 8. Prose voice, repetition, explanatory sequence

The manuscript reads as one voice (consistent `\cref` usage, consistent hedging vocabulary, first-person plural throughout). The explanatory sequence — purpose, relation, variables, consequences — holds in the revised sections I examined (Sections 3, 5, 6, 7, 9.4).

Repetition found:

* **A full sentence is duplicated verbatim in two adjacent figure captions.** "Values are read from the recorded Exodus fields; the runs are finite-load demonstrations on synthetic parameters, not a mesh-convergence study." appears in the caption of `fig:fe-fabric-contours` (`sections/finite_elements.tex:359–361`) and again in the caption of `fig:fe-fabric-diffusion` (`sections/finite_elements.tex:373–375`). → **R3-C1**.
* **The same two verification relations are enumerated twice in adjacent sentences** in `sections/experiments.tex`: "…and the two reference Biot and rank-one compliance relations used to establish the specialization" (lines 185–187) and then "Additional checks recover the isotropic formula, the reference Biot relation, and the rank-one compliance restriction" (lines 190–191). With `legacy_reference_biot` and `legacy_reference_rank_one_compliance_identity` being single checks, the reader cannot tell whether "additional checks" are new or the same ones re-listed. → **R3-C2**.
* The verbatim 10-gram overlap between `main.tex` (abstract) and `sections/pore_fabric.tex` ("directionally asymmetric pressure coupling even when the mineral itself is isotropic") is the normal abstract/body correspondence, not a defect.
* The "demonstration, not verification" disclaimer is repeated many times (abstract, `sections/finite_elements.tex:214`, `:231–234`, `:335–336`, three captions, `:379–397`, conclusion). The hedging is defensible for this paper, but it is dense enough to be trimmed → R3-O8.

---

## 9. Undefined / undefined-at-first-use technical terms

* **Exodus** — used at `sections/finite_elements.tex:322` ("the Exodus output records eleven evenly spaced field snapshots") and in the captions of `fig:fe-fabric-contours` and `fig:fe-fabric-diffusion` ("the recorded Exodus fields"). It is a MOOSE-specific file format and is nowhere defined or cited. A term whose first appearance is a body sentence and whose other appearances are figure captions. → R3-O6.
* **Lambert-function solutions** — a single sentence, `sections/experiments.tex:204`. Standard special function, undefined. → R3-O6.
* **unjacketed** is properly introduced in `sections/limits.tex:62` before its later uses in `main.tex:594` and `sections/experiments.tex:193`. **Mandel** is explained at first use (`sections/experiments.tex:8–14`) and labelled in `sections/pore_fabric.tex:324` as distinct from the fabric-adapted basis. **Moore–Penrose**, **pseudomorphic** and **platen** are adequately explained at or near first use. No other single-appearance undefined term was found.

---

## 10. REQUIRED changes

**R3-C1 — Verbatim duplicate sentence in two adjacent figure captions.**
`sections/finite_elements.tex:359–361` (caption of `fig:fe-fabric-contours`) and `sections/finite_elements.tex:373–375` (caption of `fig:fe-fabric-diffusion`) both end with the identical sentence: "Values are read from the recorded Exodus fields; the runs are finite-load demonstrations on synthetic parameters, not a mesh-convergence study." The same disclaimer is also in the body at line 336. Keep it in one place (or give each caption distinct wording) so the adjacent floats do not repeat each other verbatim.

**R3-C2 — The same two verification relations are claimed twice in adjacent sentences.**
`sections/experiments.tex:185–187` ("…the two reference Biot and rank-one compliance relations used to establish the specialization") and `sections/experiments.tex:190–191` ("Additional checks recover the isotropic formula, the reference Biot relation, and the rank-one compliance restriction"). Because `legacy_reference_biot` and `legacy_reference_rank_one_compliance_identity` are single checks, the second sentence reads as a re-listing of the first and leaves ambiguous whether the "additional checks" are distinct. State explicitly which checks are additional, or drop the duplicated items from the second sentence.

**R3-C3 — No stated notation rule for the time-level superscript `n`.**
The notation paragraph (`main.tex:215–256`) enumerates the decorations it governs but gives no rule for the superscript `n` used in eq. (97): `m_f^{\,n}`, `\mathbf F^n`, `p^n`, `t_n` (`sections/finite_elements.tex:120–123`), nor at its first appearance in eq. (97). Add one clause (e.g., "a superscript `n` denotes the discrete time level"), consistent with the paragraph's existing level of completeness.

---

## 11. OPTIONAL notes

**R3-O1 — Opening sentence of the notation paragraph drops an article.**
`main.tex:215`: "Let \(\bar\rho_s\) be solid intrinsic density, \(\phi_s\) the current solid volume fraction, and \(\rho_s=\phi_s\bar\rho_s\) the solid mass per current mixture volume." Add "the" before "solid intrinsic density" for parallelism with the other two members.

**R3-O2 — "The two stress representations" has a distant antecedent.**
`main.tex:255`: "The two stress representations differ by the rotation \eqref{eq:rotated-mineral-cauchy}." It follows the `d`/`dis` sentences but resumes the bar/hat discussion of `main.tex:223–227`. Name the two (e.g., "the mixture-frame and true-frame stress representations") or move the sentence next to the bar/hat rule.

**R3-O3 — Tilde decoration not covered; "conformal factor" is loose.**
`sections/pore_fabric.tex:172,178` introduce `\widetilde{\tau}=\mathbf R_A^T\tau'\mathbf R_A` without the notation paragraph covering the wide tilde. Also `main.tex:219–220` calls eq. (2) "the conformal factor", where the rest of the manuscript calls it the conformal (or volume-only) specialization of the distention gradient.

**R3-O4 — Reference subscript `0` has no stated rule.**
`φ_{s0}` and `\bar\rho_{s0}` are first used at eqs. (4)–(5) (`main.tex:258–263`) before any rule; `B_0` (eq. 57), `\bar\rho_{f0}` and `K_*` follow. Consider one clause in the notation paragraph.

**R3-O5 — Labels defined but never referenced: 69.**
60 equation labels and 9 section labels (listed in §2) carry no `\eqref`/`\cref`. Harmless numbering anchors, but the nine unused section labels in particular are dead weight.

**R3-O6 — Undefined technical term at first use.**
"Exodus" (`sections/finite_elements.tex:322` and two captions) and "Lambert-function" (`sections/experiments.tex:204`). One short gloss each, or attribute the file format to the MOOSE reference already cited.

**R3-O7 — Float drift for Figures 7–9.**
`fig:fe-reference-comparison`, `fig:fe-fabric-probe` and `fig:fe-fabric-mandel` are first cited on p. 24 but captioned on pp. 26, 26 and 27. All floats follow their citations and none passes the References, so this is presentational; moving Figures 7–8 earlier or citing them later would tighten the reader's path.

**R3-O8 — Hedging density.**
The "demonstration, not quantitative verification / not experimental validation" caveat recurs in the abstract, four body passages, three captions and the conclusion. The scoping is correct and should be kept, but one or two of the repeats can be trimmed without weakening it.

---

VERDICT: MINOR REVISION
