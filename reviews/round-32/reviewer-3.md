# SIMULATED AI PEER REVIEW — Reviewer 3 of 3

This is a **simulated AI peer review** produced inside an automated acceptance
cycle. It is not journal peer review and confers no acceptance. Emphasis of
this review: **exposition, notation and claims**.

- Repository (write scope): `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
- Immutable snapshot reviewed: `.agent-runtime/review-snapshots/round-32`
- Declared `SNAPSHOT_ID`: `2231ed2b9825fef48f1015be1b9b2a230c09bec424ad18a9ca8f32c5d0e8fa44`
- Report written: `reviews/round-32/reviewer-3.md`
- All manuscript and evidence reads were taken **only** from the frozen
  snapshot (a writable copy was made at `/tmp/r32/snap`; the snapshot itself
  was not modified). `build/main.aux` is not shipped, so equation numbers and
  labels were resolved from `build/main.pdf` (pdftotext) and `build/main.log`,
  cross-checked against the source text.

---

## 1. Mandatory first checks

### 1.1 Manifest hash equals declared SNAPSHOT_ID

```
$ cd .agent-runtime/review-snapshots/round-32
$ sha256sum source-manifest.json
2231ed2b9825fef48f1015be1b9b2a230c09bec424ad18a9ca8f32c5d0e8fa44  source-manifest.json
$ cat SNAPSHOT_ID
2231ed2b9825fef48f1015be1b9b2a230c09bec424ad18a9ca8f32c5d0e8fa44
```

**Result: PASS.** `sha256(source-manifest.json)` equals the declared
`SNAPSHOT_ID` exactly, and the `SNAPSHOT_ID` file holds the same string.

### 1.2 Re-hash every manifest entry

`source-manifest.json` is a flat JSON object of `repository-relative path ->
sha256` with **608 entries**. Each entry was re-hashed and compared; the tree
was then walked for unlisted files.

```
manifest entries:                     608
entries re-hashed OK:                 608
hash mismatches:                        0
listed files missing on disk:           0
files present but unlisted:             2
  UNLISTED: SNAPSHOT_ID
  UNLISTED: source-manifest.json
```

**Result: PASS.** All 608 listed files are present and hash-identical. The only
two files present but unlisted are `SNAPSHOT_ID` and `source-manifest.json`
themselves, which the task states cannot list themselves. No other discrepancies.

### 1.3 Independence declaration

I did **not** open any file under `reviews/` (including `reviews/README.md`),
and I did **not** read, list, glob or `find` any `.agent-runtime/review-snapshots/round-*`
directory other than `round-32`, nor any other reviewer's report, nor any
verdict or acceptance count. All mandatory and evidence commands above were run
inside `round-32` only.

**Self-reported incidental exposure (filename only, no content).** While
locating my output path I ran `ls -la reviews/round-32` in the working
repository. That listing showed the directory entries `LAUNCH-STATE.md` and
`reviewer-2.md` (names and timestamps only). I did not open, read, or
otherwise inspect either file, and no report content, verdict, or acceptance
count was exposed to me. Reading another reviewer's report would invalidate
this vote; no such read occurred.

---

## 2. Notation paragraph — cross-reference resolution

The notation paragraph is `main.tex` lines 216–248. Every cross-reference in it
was resolved to its rendered equation/section number in `build/main.pdf`.

| Source reference (main.tex) | Renders as | Intended display | Correct? |
|---|---|---|---|
| `\eqref{eq:true-mineral-jacobian}` (L220) | (1) | `F = A F̄`, `J = a J̄` decomposition | yes |
| `\eqref{eq:spherical-distention}` (L221) | (2) | `A = a^{1/3} R_A` conformal factor | yes |
| `\eqref{eq:kirchhoff-volume-conventions}` (L228) | (10) | `τ̄_s = J̄ σ̄_s` normalization | yes |
| `\eqref{eq:fabric-distention-stress}` (L230) | (72) | `S̄_dis = 2 ∂W_dis/∂G` | yes |
| `\eqref{eq:fe-fluid-residual}` (L233) | (96) | fluid-mass residual with `Q̄_f` | yes |
| `\eqref{eq:total-cauchy-single-prime}` (L236) | (8) | `σ' = σ + p I` | yes |
| `\eqref{eq:fixed-pressure-stress}` (L237) | (46) | `P'' = ∂W''/∂F|_p` | yes |
| `\eqref{eq:finite-biot-tensor}` (L238) | (49) | `σ = σ'' − p B` | yes |
| `\eqref{eq:drained-stiffness-restriction}` (L241) | (40) | `C^d = φ_{s0} C_s − …` | yes |
| `\eqref{eq:prescribed-logarithmic-energies}` (L242) | (29) | `W̄_s`, `W^d` energies | yes |
| `\cref{sec:pore-fabric}` (L245) | section 7 | Pore fabric section | yes |
| `\eqref{eq:rotated-mineral-cauchy}` (L247) | (6) | `σ̄_s = R_A σ̂_s R_A^T` | yes |

**No pointer lands on the wrong display.** All 12 cross-references in the
notation paragraph resolve to the intended equations/section. No label used in
the notation paragraph is left undefined (`build/main.log` reports no undefined
references; the PDF text contains no `??`).

---

## 3. Bar / hat / prime / double-prime coverage and normalization

Every marked symbol used in `main.tex` and `sections/*.tex` was enumerated and
checked against the stated rules.

**Covered correctly:**
- Bar on kinematic/energetic quantities (`F̄`, `J̄`, `W̄_s`): mineral state —
  matches (1)/(19).
- Bar on intrinsic density (`ρ̄_s`, `ρ̄_ξ`, `ρ̄_f`, `ρ̄_{f0}`): per-phase-volume
  value — matches §2 and §9.1.
- Bar on stress (`σ̄_s`) mixture frame; hat (`σ̂_s`, `τ̂_s`) true frame — matches
  (6)/(11).
- Normalizations: `σ̄_s` per current mineral volume and `τ̄_s = J̄ σ̄_s` per
  reference mineral volume both match (10) and §2 prose.
- Bar on prescribed boundary datum (`Q̄_f`) — matches (96).
- Superscript `d` (drained: `C^d` (40), `W^d` (29)); subscript `dis`
  (`W_dis`, `E_dis`, `S_dis`), and the statement that `d` never means
  distention — consistent.
- Blackboard-bold fourth-order / upright-bold second-order convention holds
  (`𝓒`→`C`, `𝔻` all blackboard bold; all second-order tensors `\mathbf`).
- The closing statement "the two stress representations differ by the rotation
  (6)" matches (6).

**Gaps found** — see R3-C1 and R3-C2 below.

---

## 4. Claims checked against frozen artifacts

Every quantitative claim in the abstract, body and conclusion was recomputed
from the frozen CSV/JSON artifacts (no held numerical suite was run).

| Claim (location) | Artifact | Verdict |
|---|---|---|
| "conformal verification suite contains 186 named checks" | `build/conformal/verification.json` `checks_passed = 186`, 186 entries | supported |
| "65 per-state identities (five states × thirteen)" | 5 × `legacy_state{0..4}` blocks of 13 | supported |
| "the two reference Biot and rank-one compliance relations" | `legacy_reference_biot`, `legacy_reference_rank_one_compliance_identity` | supported |
| "largest absolute error … is 2.5×10⁻⁹" | `max_constitutive_identity_error = 2.4549890331732928e-09` | supported |
| "spherical-gauge suite … 273 finite states across 13 mineral stiffnesses" | `build/weighted-stress/tensor-verification.json`: `materials=13`, `states_per_material=21`, `total_states=273` | supported |
| "reconstruction suite checks work equivalence and finite unjacketed compression" | `reconstruction-verification.json`: `work_equivalence=5.04e-10`, `unjacketed=5.09e-14` | supported |
| "step refinement … second-order" | `observed_orders` energy/pore-volume/pressure ≈ 2.0000 | supported |
| "Lambert-function solutions check negative-pressure and a large positive state" | `branch_pressure_-14/-13/_800_lambert_volume` | supported |
| "all plotted states satisfy positive phase volumes and (38)" | `solid_fraction_range=[0.434,0.600]`, `min_scalar_stability=28.0` | supported |
| "reference Biot components 0.7000, 0.7583, 0.7917" | `experiments.json highlights.reference_B` | supported |
| "16.8 K_* mean deviatoric/2" (isotropic comparison) | recomputed: mean of five deviatoric eigenvalues = 33.6, /2 = 16.8 | supported |
| MMS orders "px 2.00/2.00, ux 2.99/2.96, uy 3.00/2.96" | `mms-convergence.json space.orders` | supported |
| Temporal orders "0.98–1.40" | nx16/32/64 `difference_orders` min 0.978, max 1.397 | supported |
| "3.7×10⁻³ and 7.1×10⁻³ … ratio 1.94" | `figures/fe_mandel_refinement.csv` 0.003658 / 0.007104 → 1.942 | supported |
| floor "about 3.2×10⁻³ at nx=20, dt=10⁻³" | `figures/fe_load_limit.csv` load 1e-4 → 0.0032209 | supported |
| fabric mandel peaks 4.36/4.99/5.52 vs 3.62 ×10⁻⁵ | `fe-evidence/runs/fabric_mandel_coup_*` centre_pressure | supported |
| refined peaks 3.61/4.35/4.97/5.50 ×10⁻⁵ | `figures/fe_fabric_contours.csv` `p_max` | supported |
| displacement-magnitude peaks 5.18/5.14/2.38/5.26 ×10⁻⁵ | `figures/fe_fabric_contours.csv` `u_mag_max` | supported |
| "maximum lies on X1=0 symmetry line" | `p_max_x = 0.0` for all four contour runs | supported |
| reconstruction 2.2e-16, det H−1 = −3.3e-16, ‖𝔻:e3‖ = 1.6e-16, 𝔻:e6=0, invariance 2.5e-16, worst diff 4.9e-15, volume-only 1.9e-14 | `build/fabric/fabric-verification.json` | supported |

**Claim strength.** The words *verify/verified/demonstrate/demonstration/
unique/exact/independent* are used with the qualifications the evidence
supports. The finite-load and pore-fabric FE runs are repeatedly and
explicitly labelled demonstrations (abstract L53–56; §9.4 scope paragraph
`finite_elements.tex` L379–396), the temporal orders disclaim any order above
one, and the material-point re-implementation is explicitly stated to share the
section's modelling conventions rather than being an independent derivation
(`finite_elements.tex` L281–284). I found **no** claim of uniqueness,
convergence or verification that exceeds what the artifacts establish. The
"unique stationary point" statements (`pore_fabric.tex` L216, L286) are
analytic consequences of the stated convexity/positive-definiteness on the
retained subspace, not numerical over-claims.

---

## 5. Float placement

First-citation page vs caption page in `build/main.pdf`:

| Figure | First cite | Caption | Placement |
|---|---|---|---|
| 1 `fig:conformal-pressure` | 16 | 17 | cite before caption |
| 2 `fig:conformal-shear` | 16 | 17 | cite before caption |
| 3 `fig:conformal-directional` | 16 | 18 | cite before caption |
| 4 `fig:conformal-rotation` | 18 | 19 | cite before caption |
| 5 `fig:conformal-layer` | 18 | 19 | cite before caption |
| 6 `fig:fe-verification` | 23 | 24 | cite before caption |
| 7 `fig:fe-reference-comparison` | 23 | 25 | cite before caption |
| 8 `fig:fe-fabric-probe` | 25 | 26 | cite before caption |
| 9 `fig:fe-fabric-mandel` | 25 | 26 | cite before caption |
| 10 `fig:fe-fabric-contours` | 25 | 27 | cite before caption |
| 11 `fig:fe-fabric-diffusion` | 25 | 27 | cite before caption |

References begin on page 31; every figure caption is on or before page 27.
**No figure is cited after its caption, and no figure appears after the
References.**

---

## 6. Rendered-PDF hygiene

- **Undefined references / citations:** none. `grep -i undefined build/main.log`
  returns nothing; the PDF text contains no `??`.
- **Bibliography:** 36 entries in `references.bib`, 36 distinct cited keys;
  no cited key missing and no uncited entry.
- **Missing glyphs:** none (`Missing character` absent from `build/main.log`).
- **Overfull boxes:** 0. **Underfull boxes:** 1 (bibliography entry,
  `main.log` L849–851) — cosmetic, see R3-O3.
- **Equation-numbering continuity:** numbers 1–106 appear exactly once each in
  the right-aligned display positions; no gaps, no duplicates, none beyond 106.
- **Duplicated / tautological text:** one near-verbatim passage repeated within
  section 7 — see R3-O2. Abstract/conclusion restatement is normal and expected.

---

## 7. Scope statements: abstract vs body vs conclusion

Checked clause by clause; the abstract (L31–72), the body disclaimers
(`finite_elements.tex` L379–396; `experiments.tex` L194–195) and the
conclusion (L568–661) agree:

- "derived from volume-fraction-weighted phase stresses and reversible work" —
  §§2–3 — agree.
- "internal rotation cancels for objective mineral energy + volume-only
  distention energy" — §3 (20) — agree.
- "mineral stress rotated into mixture frame" — §2 (6) — agree.
- "implicit mineral-volume equation + explicit pressure-coupling tensor" —
  §4 (61), §5 (52) — agree.
- "drained compliance = mineral compliance/φ_{s0} + spherical rank-one" —
  (43) — agree.
- FE "verified against a manufactured solution for the constant reference
  tangent and, in the same limit, the constant-coefficient consolidation
  reference"; "no quantitative finite-deformation verification and no
  experimental validation claimed" — §9 — agree with the conclusion.
- fabric law "checked at the material point against a separate
  re-implementation … shares the same modelling conventions" — §9.4 —
  agree.
- "pore-fabric orientation prescribed as material data and no relative
  rotation … represented" — §7.1 — agree.

Each clause is supported by the frozen evidence (section 4 above). One
phrasing tension in the abstract is noted as R3-O4.

Specialist vocabulary is defined close to first use in the body: "Moore–Penrose
inverse" (`pore_fabric.tex` L292–294), "Mandel basis" and the √2 shear
convention (`experiments.tex` L10–24), the logarithmic-strain conjugate-stress
transformation (`logarithmic_derivative.tex`). Two ordering issues are noted
(R3-O5, R3-O6).

---

## REQUIRED changes

### R3-C1 — Notation paragraph: the prime/double-prime rules omit the reduced energies `W'` and `W''`
**File:** `main.tex`, notation paragraph lines 234–239 (rules as stated) vs
lines 440–445 (first use).
**Problem.** The paragraph states: "A single prime denotes the effective stress
that carries the full pore-pressure term … and a double prime denotes the
fixed-pressure stress `P''` …". These rules are stated only for *stresses*.
Section 5 then introduces the reduced energies `W''(F,p)` (eq. 44) and
`W'(F,p)` (eq. 45) carrying the same marks. A reader who applies the glossary
literally has no rule for `W'`/`W''` (the single prime would be read as a
stress), even though these are the central quantities of the pressure-coupling
section.
**Required change.** Extend the prime sentence so it covers the potentials as
well as the stresses, e.g. state that the same single/double prime applied to
the energy denotes the fixed-pressure (Legendre) potential `W'` and the
energy `W''` differentiated at fixed pressure, alongside `σ'`, `τ'`, `P'` and
`σ''`, `P''`.

### R3-C2 — Notation paragraph: the bar on `S̄_dis` is attributed to the frame, but the unbarred `S_dis` is in the same frame
**File:** `main.tex` lines 229–231, against the definitions in
`sections/pore_fabric.tex` lines 139–146.
**Problem.** The paragraph says: "written on the distention stress
`S̄_dis` of (72), a bar instead denotes that stress in the intermediate frame,
normalized per reference mixture volume." But `pore_fabric.tex` L139–146
defines **both** `S̄_dis = 2 ∂W_dis/∂G` and the unbarred
`S_dis = ∂W_dis/∂E_dis` as stresses in the intermediate frame; they differ by
which strain they are conjugate to (`G` vs `E_dis = ½ ln G`), not by frame.
As written, the rule implies the bar signals the frame, which the unbarred
symbol contradicts.
**Required change.** Restate the rule so the bar's role for `S̄_dis` is stated
correctly — the bar distinguishes the work-conjugate pair (`S̄_dis` conjugate to
`G`, `S_dis` conjugate to `E_dis`) and marks the per-reference-mixture-volume
normalization — rather than attributing the intermediate frame to the bar.

---

## OPTIONAL notes

### R3-O1 — 72 labels are defined but never referenced
**Files:** `main.tex`, `sections/*.tex`.
63 equation labels and 9 section labels carry `\label{}` but are referenced
nowhere (e.g. `eq:solid-mass`, `eq:distention`, `eq:conformal-objective-energy`,
`eq:reduced-energy`, `eq:legendre-energy`, `eq:piola-transform-general`,
`eq:pressure-envelope`, `eq:fe-fluid-storage`, `eq:fe-mms-u1/u2/pressure`,
`eq:experiment-plane-directions`, `eq:logarithmic-conjugate-work`,
`eq:fabric-tensor`, `sec:conclusion`, `sec:compatibility`, `sec:fe-fluid-closure`).
No float label is unreferenced. This is LaTeX hygiene only and has **no**
effect on the rendered document; trimming the list would reduce clutter.

### R3-O2 — Near-duplicate passage inside section 7
**File:** `sections/pore_fabric.tex` lines 213–216 and 281–286.
The convexity/unique-stationary-point argument is stated twice in nearly
identical wording ("…strictly convex and the mineral term contributes a
positive-definite stiffness in the same strain, so the stationary point … is
unique"). Consider stating it once (in §7.4) and referring back from §7.5.

### R3-O3 — Underfull box in the bibliography
**File:** `build/main.log` lines 849–851 (entry "Rock Mechanics and Rock
Engineering"). Cosmetic; no action required.

### R3-O4 — Abstract relaxation clause blends the general fabric law with the implemented subspace
**File:** `main.tex` lines 62–67.
The abstract says the tensorial law "relaxes the rank-one drained-compliance
restriction to a fabric-symmetric compliance supported on the retained
volumetric–axial distention subspace". The relaxation in §7.5 eq. (78) is
general (`(C^d)^{-1} = (φ_{s0} C_s)^{-1} + 𝔻^{+}`); the volumetric–axial
subspace is the *implementation's* retained subspace (§7.5 tail; §9.4). Since
the abstract elsewhere separates law from implementation, consider wording this
clause to distinguish the general law from the retained subspace, to avoid
reading the implementation restriction as a property of the derivation.

### R3-O5 — "unimodular" used before gloss
**Files:** `main.tex` abstract (L~63) ; first gloss `sections/pore_fabric.tex`
§7.2 (`det H = 1`). The term is used in the abstract and only implicitly
defined later. A two-word parenthetical at first body use would help.

### R3-O6 — Forward reference to `𝔻` in §7.4
**File:** `sections/pore_fabric.tex` line 209 uses `range(𝔻)` and line 210 uses
`𝔻` before `𝔻` is defined in §7.5 (line ~272). The forward `\cref` makes this
recoverable, but introducing `𝔻` at that first use would read better.

### R3-O7 — Subscript `A` on `W_A` not covered by the notation paragraph
**File:** `main.tex` line ~371 (`W_A(a)`), cross-referenced from
`sections/stress_reconstruction.tex`. `W_A` is a distention quantity but is not
among the `dis`-subscripted symbols enumerated in the notation paragraph
(L243–245), and its subscript is not glossed. Adding one clause (the scalar
volume-only distention energy, `W_A(a)`, with `W_dis` its tensorial
generalization) would complete the glossary.

---

## Verdict

All 608 manifest entries verify; the notation paragraph's cross-references all
land on their intended displays; every quantitative claim I checked is
supported by the frozen artifacts; scope statements agree clause by clause;
float placement and equation numbering are clean. The two required items are
small, local edits to the notation paragraph (prime coverage for `W'`/`W''`,
and the `S̄_dis` bar rule); the remaining notes are optional hygiene.

VERDICT: MINOR REVISION
