# SIMULATED AI PEER REVIEW — Reviewer 3

**Manuscript:** *An anisotropic Biot tensor from mineral stress and distention work*
**Repository:** `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
**Snapshot:** `.agent-runtime/review-snapshots/round-31` (declared `SNAPSHOT_ID` = `09a606a73d9f475ec624785b7b2a8483f989f2270eca7aeb405015205d113c84`)
**Emphasis:** exposition, notation and claims
**Round:** 31

## Scope and method

I read only the frozen snapshot. All manuscript, artifact, and PDF inspection was
performed either on the read-only snapshot tree or on a byte-identical temporary
copy under `/tmp/r3-snap-09a606a7`. No file in the working tree was used as
source material, and no file was written inside the snapshot. I did not run any
held numerical suite (`validation/`, `examples/verify_*.py`); every numerical
claim I checked was recomputed from the frozen CSV/JSON artifacts.

---

## MANDATORY FIRST CHECKS

### Check 1 — manifest digest equals the declared SNAPSHOT_ID

```
$ cd /home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor
$ sha256sum .agent-runtime/review-snapshots/round-31/source-manifest.json
09a606a73d9f475ec624785b7b2a8483f989f2270eca7aeb405015205d113c84  .agent-runtime/review-snapshots/round-31/source-manifest.json
```

**Result: PASS.** The recomputed digest is exactly the declared `SNAPSHOT_ID`
(`09a606a73d9f475ec624785b7b2a8483f989f2270eca7aeb405015205d113c84`). The
snapshot's own `SNAPSHOT_ID` file contains the same string.

### Check 2 — re-hash every listed file on a temporary copy

```
$ SNAP=.../round-31; TMP=/tmp/r3-snap-09a606a7
$ rm -rf "$TMP"; mkdir -p "$TMP"; cp -r "$SNAP"/. "$TMP"/; chmod -R u+w "$TMP"
$ python3 - "$TMP" <<'PY'   # hashes each manifest entry, then walks for unlisted files
... sha256 of every listed path, compared to the manifest value; os.walk for extras ...
PY
```

**Result: PASS.**

| Quantity | Value |
|---|---|
| Entries listed in `source-manifest.json` | 606 |
| Entries re-hashed | 606 |
| Hash mismatches | **0** |
| Listed files missing on disk | **0** |
| Files present but not listed | 2 — `SNAPSHOT_ID`, `source-manifest.json` |

The two unlisted files are the manifest itself and the `SNAPSHOT_ID` marker;
both are self-referential bookkeeping files that cannot hash themselves, so
their absence from the manifest is expected and not a defect. The snapshot copy
is 54 MB and contains no `.agent-runtime/` subtree, i.e. no nested snapshot.
`reviews/README.md` appears in the manifest and was hashed mechanically as a
required manifest entry; its contents were never opened, read, or rendered.

### Check 3 — independence declaration

I declare that I did **not** open any file under `reviews/` (not `README.md`,
not `LAUNCH-STATE.md`, not any other report or response), and that I did **not**
read any other `.agent-runtime/review-snapshots/round-*` directory. Every path
I opened lies under `round-31` (or its `/tmp` copy). I did not list, glob, or
`find` any sibling `round-*` directory. **No accidental exposure occurred, so
there is nothing to self-report.**

---

## Emphasis audit

### A1. The bar rule (general decomposition primary, conformal as specialization)

`main.tex:216-245` states the glossary. The bar rule is stated against the
**general** multiplicative decomposition and identifies the conformal factor as
the specialization:

> "a bar on a kinematic or energetic quantity denotes the mineral state reached
> by removing the distention in the general multiplicative decomposition
> \eqref{eq:true-mineral-jacobian}, of which the conformal factor
> \eqref{eq:spherical-distention} is the specialization." (`main.tex:218-221`)

Rendered, this is "(1) … of which the conformal factor (2) is the
specialization", and I verified the numbers against the PDF (page 3): (1) =
`eq:true-mineral-jacobian`, (2) = `eq:spherical-distention`. **Correct as
stated**, and correctly forward-compatible with §7, where the distention is
generalized to `A = R_A G^{1/2}` without changing the meaning of the bar.

I enumerated every barred symbol used anywhere in the sources and tested it
against the rule. All are covered:

| Symbol occurrences | Rule invoked | Verdict |
|---|---|---|
| `\bar{\mathbf F}`, `\bar{\mathbf C}`, `\bar{\mathbf U}`, `\bar J`, `\bar W_s` | mineral state (kinematic/energetic) | consistent |
| `\bar{\mathbf\varepsilon}` | mineral logarithmic strain | consistent |
| `\bar\rho_s`, `\bar\rho_{s0}`, `\bar\rho_f`, `\bar\rho_{f0}` | intrinsic density `\bar\rho_\xi=\rho_\xi/\phi_\xi` | consistent |
| `\bar{\mathbf\sigma}_s`, `\bar{\mathbf\tau}_s` | mixture frame | consistent |
| `\bar{\mathbf S}_{\mathrm{dis}}` | intermediate frame (explicitly excepted) | consistent |
| `\bar Q_f` | prescribed boundary datum (explicitly excepted) | consistent |
| `\widehat{\mathbf\sigma}_s`, `\widehat{\mathbf\tau}_s` | hat = true frame | consistent |

### A2. Normalization of each barred stress

Verified against the rendered equations (PDF pages 3–4 and 22):

- `\bar{\mathbf\sigma}_s` per **current** mineral volume — `main.tex:226`; the
  text at `main.tex:251-252` confirms "Both are stresses per current mineral
  volume", and eq (6) is the pure rotation.
- `\bar{\mathbf\tau}_s = \bar J \bar{\mathbf\sigma}_s` of eq **(10)** per
  **reference** mineral volume — `main.tex:227-228`. I confirmed (10) is
  `eq:kirchhoff-volume-conventions` in the PDF. Correct.
- `\bar{\mathbf S}_{\mathrm{dis}}` of eq **(72)** per **reference** mixture
  volume in the **intermediate** frame — `main.tex:229-231`. I confirmed (72)
  is `eq:fabric-distention-stress`, and its source caption
  (`sections/pore_fabric.tex`) states the same normalization. Correct.
- The two representations are attributed to the rotation of eq **(6)**
  (`main.tex:245`), which is `eq:rotated-mineral-cauchy`. Correct.

### A3. Single-prime and double-prime rules — **two mis-targeted cross-references**

The rule statements are right; the equation targets are not.

**(a) Single prime.** `main.tex:234-236` reads "A single prime denotes the
effective stress that carries the full pore-pressure term, as in
`\mathbf\sigma'` of `\eqref{eq:constitutive-kirchhoff-phase-stress}`". That
label is eq **(12)**, and eq (12) contains `\mathbf\tau'`, not
`\mathbf\sigma'`:

```
(12)  𝛕′ = 𝜙𝑠0(𝛕̄𝑠 + 𝑝𝐽̄𝐈)
```

`\mathbf\sigma'` is defined in eq **(8)** (`\mathbf\sigma'=\mathbf\sigma+p\mathbf I`,
`eq:total-cauchy-single-prime`) and repeated in (9). Corroboration: the label
`eq:total-cauchy-single-prime` is **defined but never referenced anywhere** in
the manuscript — the notation paragraph is evidently where it was meant to be
used.

**(b) Double prime.** `main.tex:236-238` reads "a double prime denotes the
fixed-pressure stress of `\eqref{eq:cauchy-pressure-tangent}`, so that
`\mathbf\sigma=\mathbf\sigma''-p\mathbf B`". That label is eq **(55)**,
verified in the PDF as

```
(55)  ∂𝛔/∂𝑝|_𝐅 = −𝐁
```

i.e. the pressure tangent, which contains neither `\mathbf\sigma''` nor the
displayed relation. The relation `\mathbf\sigma=\mathbf\sigma''-p\mathbf B` is
eq **(49)** (`eq:finite-biot-tensor`); the double-prime stress `\mathbf P''` is
first defined in eq **(46)** (`eq:fixed-pressure-stress`). The correct target is
(49) (or (46)).

These two are the only broken notation-paragraph pointers I found. Every other
parameter/datum pointer in that paragraph resolves to the right equation:
`\mathbb{C}^d` of **(40)** and `W^d` of **(29)** (verified against the PDF),
`\bar Q_f` of **(96)**, `\bar{\mathbf S}_{\mathrm{dis}}` of **(72)**,
`\mathbf\sigma'`-adjacent eq (6), (1), (2).

### A4. The d-versus-dis distinction

`main.tex:239-245` reserves superscript `d` for the drained skeleton
(`\mathbb{C}^d` (40), `W^d` (29)) and subscript `\mathrm{dis}` for distention
(`W_{\mathrm{dis}}`, `\mathbf E_{\mathrm{dis}}`, `\mathbf S_{\mathrm{dis}}`),
and asserts "`d` never means distention". I grepped every occurrence of a
superscript `d` and of the distention quantities across `main.tex` and all
`sections/*.tex`: the assertion holds. The distention stiffness is a distinct
blackboard-bold symbol `\mathbb{D}` (not a superscript `d`), which is consistent
with the paragraph's own rule that fourth-order tensors are blackboard bold;
no collision with `\mathbb{C}^d` is introduced, though the two are visually close
(see R3-O4).

### A5. `e_1..e_6` label set and the √2 normalization (`sections/pore_fabric.tex:301-320`)

I checked the six tensors symbolically for orthonormality, completeness, and the
stated normalization:

- `e_1 = I/√3` — unit norm (`I:I = 3`). ✔
- `e_2 = √(3/2)(m⊗m − I/3)` — trace-free, norm² = (3/2)(2/3) = 1. ✔
- `e_3 = (p1⊗p1 − p2⊗p2)/√2` — unit norm. ✔
- `e_6 = √2 sym(p1⊗p2)` — Frobenius norm² = 2·(1/2) = 1. ✔
- `e_4 = √2 sym(m⊗p1)`, `e_5 = √2 sym(m⊗p2)` — **the axial-shear √2 is present
  and correct**: each has norm² = 2·(1/2) = 1. ✔
- All cross-inner-products vanish (`e_1:e_2 = 0`, `e_2:e_3 = 0`, `e_3:e_6 = 0`,
  `e_3:e_4 = 0`), and trace-free symmetric tensors are 5-dimensional, so
  `{e_2..e_6}` ∪ `{e_1}` spans all six dimensions. The set is a complete
  orthonormal basis. ✔

The wording is also correct: `e_3`, `e_6` are the in-plane (⊥`m`) pair and
`e_4`, `e_5` are the axial-shear pair; `𝔻` has rank two on the six-dimensional
space and therefore a four-dimensional null space, matching "annihilates the
four complementary modes". The disclaimer at `pore_fabric.tex:318-321` that
"`e_1,…,e_6` denote this fabric-adapted orthonormal basis … not the Mandel
component indices of (83)" is accurate — (83) is `eq:example-mineral-stiffness`.
The numerically reported residuals corroborate this exact normalization
(`build/fabric/fabric-verification.json` → `D4_e3_norm = 1.582e-16`,
`D4_e6_norm = 0.0`, `rotation_invariance_norm = 2.497e-16`).

### A6. Retargeted minimization cross-reference

The cross-reference at `sections/pore_fabric.tex:207-209` —

> "The minimization is restricted to distentions whose logarithmic strain lies
> in the retained subspace `\operatorname{range}\mathbb{D}` of
> `\cref{sec:fabric-biot}`."

— **resolves correctly**: it points to §7.5 (`sec:fabric-biot`), which does
define `range 𝔻`, the Moore–Penrose inverse `𝔻⁺`, and positive definiteness on
the retained subspace (`pore_fabric.tex:272-290`). The reciprocal pointer in §7.5
to eq (75) (`\eqref{eq:fabric-equilibrium}` at line 277) also resolves, to the
equilibrium defined in §7.4. The pair is mutually consistent; the only issue is
ordering (see R3-O2).

### A7. Abstract / body / conclusion scope statements agree

I compared the three scope statements clause by clause. They agree, and all are
backed by frozen evidence:

| Claim | Abstract | Body | Conclusion | Evidence in snapshot |
|---|---|---|---|---|
| FE verified vs manufactured solution + constant-coefficient consolidation | `main.tex:50-53` | `finite_elements.tex:201-216`, scope ¶ at end | `main.tex:499-503` | `fe-evidence/mms-convergence.json`, `figures/fe_mandel_refinement.csv` |
| No quantitative FE verification / no experimental validation for demonstrations | `main.tex:53-56` | "not a quantitative verification … not experimental validation" | `main.tex:504-508` | scope strings in the JSON artifacts |
| Fabric law checked at material point vs a re-implementation **sharing modelling conventions** | `main.tex:56-60` | `finite_elements.tex:280-287` ("not an independent derivation") | `main.tex:505-508` | `build/fabric/fabric-verification.json` |
| Pore-fabric orientation is prescribed material data; no relative rotation represented | `main.tex:61-64` | `pore_fabric.tex:57-90` | `main.tex:527-530` | — (modelling statement) |

### A8. Rendered PDF inspection (`build/main.pdf`, 34 pages)

- **Unresolved references: none.** `build/main.log` contains zero
  `undefined`/`LaTeX Warning` reference or citation entries, and the extracted
  PDF text contains zero `??` tokens. I independently resolved all 64 distinct
  `\cref`/`\Cref`/`\eqref`/`\ref` targets against the 138 defined labels:
  **0 missing targets**.
- **Missing glyphs: none.** Zero `Missing character` entries in the log.
- **Overfull boxes: none** (0 `Overfull`). One `Underfull \hbox (badness 1137)`
  occurs in the generated bibliography (`main.bbl`, the *Rock Mechanics and Rock
  Engineering* entry, `main.log` line 852) — benign and outside the manuscript
  body.
- **Equation numbering consistent.** 106 numbered equations, strictly monotonic
  1→106, matching an independent reconstruction from the source input order
  (main body parts interleaved with `\input` files: 23 + 20 + 13 + 8 + 18 + 3 +
  15 + 6 = 106).
- **Figure placement.** Documented as R3-O1 below.

### A9. Numerical claims re-checked from frozen artifacts

All checked values reproduce:

| Claim (location) | Artifact | Verdict |
|---|---|---|
| 186 named checks | `build/conformal/verification.json:checks_passed` | ✔ 186 |
| 65 per-state identities (5 states × 13) | 5 `legacy_state{0..4}_*` groups × 13 | ✔ |
| largest constitutive-identity error 2.5×10⁻⁹ | `max_constitutive_identity_error` = 2.4550e-9 | ✔ |
| step refinement second order | `observed_orders` ≈ 2.000, 2.000, 1.999 | ✔ |
| 273 finite states / 13 mineral stiffnesses | `tensor-verification.json` 273, states_per_material 21 | ✔ |
| reference Biot 0.7000 / 0.7583 / 0.7917 | `experiments.json:highlights.reference_B` | ✔ (recomputed `I−ℂ^d:ℂ_s⁻¹:I` = 0.7 / 0.758333 / 0.791667) |
| *K*_s = 28*K*₍, *K* = 7*K*₍, φ_s0 = 0.6 | `experiments.json` | ✔ (recomputed) |
| isotropic μ = 16.8*K*₍ = mean of 5 deviatoric modes ÷ 2 | recomputed eigenvalues of the deviatoric projection of ℂ_s: {20, 24, 28, 42.967, 53.033}, mean 33.6 | ✔ (my first, naive reading gave 4.58; the projected-stiffness reading gives exactly 16.8 — the text is right) |
| drained shear = φ_s0 × mineral shear | `drained_Mandel_stiffness` diag {12, 14.4, 16.8} = 0.6·{20,24,28} | ✔ |
| fabric residuals 2.2e-16, −3.3e-16, 1.6e-16, 0.0, 2.5e-16, 4.9e-15, 1.9e-14 | `build/fabric/fabric-verification.json` → `tensor_checks`, `worst_probe_abs_diff`, `conformal_cross_check` | ✔ all |
| Mandel inputs φ_s0=0.9, *K*=1, *G*=0.75, α=0.6, storage 17/80 | `site/reports/mandel-reference.json` (+ recomputation of S_s and 1/M) | ✔ |
| MMS orders p 2.00/2.00, u_x 2.99/2.96, u_y 3.00/2.96 | `mms-convergence.json:space.orders.*.naive_orders` | ✔ |
| temporal orders 0.98–1.40 at nx=16/32/64 | all nine `difference_orders` ∈ [0.9783, 1.3969] | ✔ |
| linear step refinement 3.7e-3, 7.1e-3, ratio 1.94 | `fe_mandel_refinement.csv` (0.003658, 0.007104 → 1.942) | ✔ |
| pressure floor 3.2e-3 at nx=20, dt=1e-3 | `fe_load_limit.csv:nonlinear_load_0.0001` = 0.0032209 | ✔ |
| fabric peaks 3.62 / 4.36 / 4.99 / 5.52 ×10⁻⁵ | `fe_fabric_mandel_peak.csv` | ✔ |
| contour peaks 3.61 / 4.35 / 4.97 / 5.50 ×10⁻⁵; u_mag 5.18 / 5.14 / 2.38 / 5.26 ×10⁻⁵ | `fe_fabric_contours.csv` | ✔ |
| "eleven evenly spaced field snapshots" | `fabric_contour_a0/solution.e`: `time_step = 11`, `time_whole` = 0 … 0.003 step 0.0003 | ✔ |
| "six recorded times" (diffusion figure) | `fe_fabric_diffusion.csv`: 6 distinct times | ✔ |
| "refined 40×8 mesh of the 1×0.1 strip" | `fabric_mandel.i` is 4×1; `fabric_contour.i` is 40×8; both 0..1 × 0..0.1 | ✔ |
| Lambert-function checks | `verify_conformal.py` uses `scipy.special.lambertw`; three `branch_pressure_*_lambert_volume` checks at 1e-13 tolerance | ✔ |
| max pressure on the `X_1 = 0` symmetry line | `fe_fabric_contours.csv:p_max_x = 0.0` for all four columns | ✔ |

No numerical claim I could test outran its artifact.

---

## REQUIRED CHANGES

### R3-C1 — Notation paragraph: single-prime rule points at the wrong equation
**Location:** `main.tex:234-236`.
**Problem:** "A single prime denotes the effective stress that carries the
full pore-pressure term, as in `\mathbf\sigma'` of
`\eqref{eq:constitutive-kirchhoff-phase-stress}`." That label renders as eq
**(12)**, whose content is `𝛕′ = 𝜙𝑠0(𝛕̄𝑠 + 𝑝𝐽̄𝐈)` — the Kirchhoff effective
stress, not `\mathbf\sigma'`.
**Required:** retarget the reference to `eq:total-cauchy-single-prime` (renders
as (8)), or change the symbol to `\mathbf\tau'` if (12) is intended. This is the
only reference to `eq:total-cauchy-single-prime` anywhere in the manuscript, so
the label is currently dead.

### R3-C2 — Notation paragraph: double-prime rule points at the wrong equation
**Location:** `main.tex:236-238`.
**Problem:** "a double prime denotes the fixed-pressure stress of
`\eqref{eq:cauchy-pressure-tangent}`, so that
`\mathbf\sigma=\mathbf\sigma''-p\mathbf B`." That label renders as eq **(55)**,
`∂𝛔/∂𝑝|_𝐅 = −𝐁`, which contains no `\mathbf\sigma''` and not the displayed
relation.
**Required:** retarget to `eq:finite-biot-tensor` (renders as (49)), where
`\mathbf\sigma=\mathbf\sigma''-p\mathbf B` is stated; optionally also cite
`eq:fixed-pressure-stress` (46) for `\mathbf P''`.

*(Both items are confined to the notation paragraph that this review was asked
to audit; no body equation or result is affected.)*

---

## OPTIONAL NOTES

### R3-O1 — Six figures are displaced 2–4 pages from their first citation
**Location:** `sections/finite_elements.tex:201, 215, 288, 317, 323, 333`
(citations) vs. `finite_elements.tex:219, 238, 292, 338, 351, 365` (all
`\begin{figure}[t]`).

Measured in the rendered PDF:

| Figure | First cited (p.) | Caption (p.) | Lag |
|---|---|---|---|
| 1, 2 | 16 | 17 | 1 |
| 3 | 16 | 18 | 2 |
| 4, 5 | 18 | 19 | 1 |
| **6** | **23** | **25** | **2** |
| **7** | **23** | **26** | **3** |
| **8** | **24** | **26** | **2** |
| **9** | **24** | **27** | **3** |
| **10** | **24** | **27** | **3** |
| **11** | **24** | **28** | **4** |

All figures follow their citation (no forward-figure reference), but the six
`[t]` floats of §9 are queued behind the `\FloatBarrier` at the end of the
section, so figures 6–11 land 2–4 pages after the text that argues from them.
Consider `[htbp]`, a smaller figure block, or moving `\FloatBarrier` to allow
one or two figures to land nearer their discussion.

### R3-O2 — `𝔻` and the "quadratic distention potential" are used one subsection before definition
**Location:** use at `sections/pore_fabric.tex:208-215`; definitions at
`sections/pore_fabric.tex:272-283`.
§7.4 refers to "the retained subspace `range 𝔻`" and to "the quadratic
distention potential … strictly convex", but `𝔻` and the quadratic form
`W_dis = ½ E_dis:𝔻:E_dis` are introduced only in §7.5. The retargeted
cross-reference at line 209 does correctly tell the reader where to look, so
this is an ordering/clarity matter rather than an error; moving the sentence, or
forward-declaring `𝔻`, would remove the forward reference.

### R3-O3 — Uniqueness is asserted from the convexity of the distention potential alone
**Location:** `sections/pore_fabric.tex:213-215` and `281-283`.
"the quadratic distention potential is strictly convex … so the stationary point
of (75) is unique". The bracket in (75) is
`W_dis(G) + φ_s0 \bar W_s(\bar F) + φ_s0 p \bar J`; strict convexity of
`W_dis` alone does not by itself establish uniqueness of the minimizer of the
full bracket, because the mineral term is also curved in `G`. The statement is
true in the retained positive-definite model (`𝔻 + φ_s0ℂ_s ≻ 0` on the
subspace), but the stated justification omits the second term. One clause
covering the mineral term would remove the gap.

### R3-O4 — Frame vocabulary is not consolidated in the notation paragraph
**Location:** `main.tex:224-231` defines only "mixture frame" (bar) and "true
frame" (hat). The body additionally uses "intermediate frame"
(`main.tex:231` for `\bar{\mathbf S}_{\mathrm{dis}}`, and `main.tex:262-263`),
"true-deformation frame" (`sections/logarithmic_derivative.tex:25`), "material
frame" and "mineral frames" (`sections/pore_fabric.tex:57-90`), and "reference
axes". These are used consistently, but the reader has to assemble the
correspondence. One sentence in the notation paragraph naming the
mixture/true/intermediate/material frames would close the gap. (Relatedly,
`\mathbb{D}` the distention stiffness and `\mathbb{C}^d` the drained stiffness
are visually close; the stated `d`-vs-`dis` rule is satisfied, but a
half-sentence distinguishing them would help.)

### R3-O5 — Notation glossary forward-references (72) and (96) from §2
**Location:** `main.tex:229-233`. Because the paragraph is a glossary, pointing
at later equations is reasonable; I note it only so that the choice is
deliberate. `\eqref{eq:fabric-distention-stress}` (72) and
`\eqref{eq:fe-fluid-residual}` (96) both resolve correctly.

### R3-O6 — Three literature-specific claims are not verifiable from the snapshot
**Locations:** `main.tex:633` (Drumheller §8.9 symmetry argument),
`sections/limits.tex:51` (Gajo eqs (3.27), (3.32), (3.34)),
`sections/finite_elements.tex:152` (Walker et al. appendix D). Each is a
specific, falsifiable pointer into another work. I could not check them against
the frozen snapshot (the source PDFs are not included), so I record them as
unverified rather than incorrect; they are worth a pre-submission read of the
cited passages. The supporting reference keys (`drumheller2000`, `gajo2010`,
`walker2023poroelasticity`, `zha1996forsterite`, `foster2026poroplastic`) all
exist in `references.bib`, and `foster2026poroplastic` is correctly typed
`@unpublished`.

---

## Assessment

The exposition is disciplined and unusually well hedged: scope statements in the
abstract, body, and conclusion agree, every "demonstration" is labelled as such,
the uniqueness of the strong-form claims is bounded by explicit caveats, and
every numerical value I re-derived from the frozen artifacts reproduces to the
stated precision. The notation paragraph is a genuine asset — the
normalization-by-normalization treatment of `\bar{\mathbf\sigma}_s`,
`\bar{\mathbf\tau}_s`, and `\bar{\mathbf S}_{\mathrm{dis}}`, the bar/hat rule,
and the explicit `d`-versus-`dis` separation are all correct, and the `e_1..e_6`
fabric basis (including the axial-shear √2 normalization) is exactly right.

The only concrete defects are two mis-targeted equation references inside that
notation paragraph (R3-C1, R3-C2), which would send a careful reader to the
wrong display. They are localized, mechanical, and do not touch any derivation,
result, or claim. Everything else is presentational. The manuscript is close to
ready.

VERDICT: MINOR REVISION
