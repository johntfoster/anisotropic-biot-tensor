# Simulated AI peer review — Reviewer 3 of 3

**Seat:** exposition, notation and claims.
**Manuscript:** "An anisotropic Biot tensor from mineral stress and distention work."
**Snapshot under review (READ-ONLY):** `.agent-runtime/review-snapshots/round-36`, declared `SNAPSHOT_ID = c1f6210d5e2649986693d3dc0c26dccc072434c166148bbdc89e3f874ce4644d`.
All paths below are relative to the snapshot root. All reads came from the snapshot; scratch only under `/tmp`.

This is a simulated AI peer review of a manuscript. It is not journal peer review and confers no acceptance.

---

## 1. Mandatory first checks

### 1.1 Manifest hash and SNAPSHOT_ID

```
$ cd .agent-runtime/review-snapshots/round-36
$ sha256sum source-manifest.json
c1f6210d5e2649986693d3dc0c26dccc072434c166148bbdc89e3f874ce4644d  source-manifest.json
$ cat SNAPSHOT_ID
c1f6210d5e2649986693d3dc0c26dccc072434c166148bbdc89e3f874ce4644d
```

Both values equal the declared `SNAPSHOT_ID`. **PASS.**

### 1.2 Re-hash of every manifest entry, plus full tree walk

```
$ python3  # sha256 every value in source-manifest.json against the file on disk; os.walk the snapshot
LISTED: 608
RE-HASHED OK: 608
MISMATCHES: 0
LISTED-BUT-MISSING: 0
PRESENT-BUT-UNLISTED: 2
  UNLISTED SNAPSHOT_ID
  UNLISTED source-manifest.json
```

608 entries listed, 608 re-hashed and matching, no mismatches, no listed-but-missing files. The only two present-but-unlisted files are the snapshot's own metadata pair (`SNAPSHOT_ID`, `source-manifest.json`), which are the files the manifest cannot hash into itself. **PASS.**

### 1.3 Independence

I did not open, read, list, glob or find anything under the working tree's `reviews/` directory; I never touched it, and my report is the first thing I write there. I never opened any other `.agent-runtime/review-snapshots/round-*` directory, and I did not seek any other reviewer's report, verdict or acceptance count.

**Self-report (full disclosure):** the snapshot's own manifest lists exactly one `reviews/` path, `reviews/README.md`. Mandatory step 1.2 requires hashing *every* listed path, so my script read its bytes to compute a hash. I did not open, read, print, or otherwise display its content, and I did not enumerate the snapshot's `reviews/` directory (my tree listing was truncated with `head -100` and never reached it). The only listing I produced was of manifest *keys*.

---

## 2. Build log and cross-reference checks

```
$ pdftotext -layout build/main.pdf /tmp/r36.txt && grep -c "??" /tmp/r36.txt
0
$ grep -n -iE "undefined|Warning" build/main.log   # LaTeX Warning lines: none
$ grep -c Overfull build/main.log ; grep -c Underfull build/main.log
0
1
```

- No unresolved cross-reference or citation markers anywhere in the rendered PDF (`??` count 0); no `LaTeX Warning` of any kind; no overfull boxes; no missing glyphs; no undefined control sequences.
- The single box complaint is cosmetic: `build/main.log:849` `Underfull \hbox (badness 1137) in paragraph at lines 33--40` (bibliography) → R3-O1.

**Notation-paragraph cross-references.** I reproduced the equation numbers independently by counting every numbered equation from `main.tex` through the sectian files, then confirmed against the rendered text (PDF pages 3–4 render "of (3)", "(6)", "(8)", "(10)", "(29)", "(40)", "(44)", "(45)", "(46)", "(49)", "(72)", "(74)", "(96)"). Every equation cited in the notation paragraph and elsewhere resolves to the intended object: (3) `conformal-mineral-metric`, (6) `rotated-mineral-cauchy`, (8) `total-cauchy-single-prime`, (10) `kirchhoff-volume-conventions`, (12) `constitutive-kirchhoff-phase-stress`, (29) `prescribed-logarithmic-energies`, (40) `drained-stiffness-restriction`, (44) `reduced-energy`, (45) `legendre-energy`, (46) `fixed-pressure-stress`, (49) `finite-biot-tensor`, (72) `fabric-distention-stress`, (74) `fabric-phase-work`, (96) `fe-fluid-residual`. **No cross-reference defect found.**

---

## 3. Claim / evidence spot checks (all verified — no mismatch found)

I re-derived or re-read each numeric claim from the snapshot's own artifacts.

| Manuscript claim | Artifact | Result |
|---|---|---|
| Reference Biot components `0.7000, 0.7583, 0.7917` (`sections/experiments.tex`) | recomputed `B_0 = I − C^d:C_s^{-1}:I` from the Mandel `C_s` of eq (83), `φ_s0=0.6`, `K=7` | `[0.7000, 0.7583, 0.7917]` exact |
| Isotropic comparison shear `16.8K_*` = mean of the five deviatoric modes / 2 | deviatoric eigenvalues of the normal block `42.9668, 53.0332` + shears `20, 24, 28` | mean `33.6`, /2 = `16.8` exact |
| FE reference `G=0.75`, `B=0.6`, total storage `17/80` (`sections/finite_elements.tex`) | `G=φ_s0μ_s`, `1−K/K_s`, `(1−φ_s0)/K_f+S_s` | `0.75`, `0.6`, `0.2125=17/80` exact |
| "186 named checks", "65 per-state identities (five states times thirteen)", "two reference Biot and rank-one compliance relations" | `build/conformal/verification.json` | `checks_passed=186`, `len(checks)=186`, 13 identities/state, `legacy_identities_rechecked=67=65+2` |
| "largest absolute error among its constitutive identities is 2.5×10^{-9}" | `build/conformal/verification.json` | max non-convergence error `2.455e-9` ✓ (see R3-O2 for scope) |
| "273 finite states across 13 mineral stiffnesses" | `site/reports/tensor-verification.json` | `total_states=273`, `states_per_material=21` → 13 materials |
| MMS adjacent orders: pressure `2.00 and 2.00`, `u_x 2.99 and 2.96`, `u_y 3.00 and 2.96` | `fe-evidence/mms-convergence.json` | `1.9966/2.0008`, `2.9917/2.9585`, `2.9983/2.9600` ✓ |
| Temporal successive-difference orders "0.98–1.40" | same | min `0.978`, max `1.3965` ✓ |
| Linear step refinement `3.7e-3` and `7.1e-3`, ratio `1.94` | `fe-evidence/runs/linear_time_0.001,0.002/analysis.json` | `3.6580e-3`, `7.1039e-3`, ratio `1.9418` ✓ |
| Pressure floor "about `3.2×10^{-3}` at `nx=20`, `dt=10^{-3}`" | `fe-evidence/runs/nonlinear_load_0.0001/analysis.json` | `3.2209e-3` ✓ |
| Fabric checks `2.2e-16`, `det H−1=−3.3e-16`, `∥D:e_3∥=1.6e-16`, `D:e_6=0`, rotation `2.5e-16`, worst diff `4.9e-15`, conformal limit `1.9e-14` | `build/fabric/fabric-verification.json` | `2.220e-16`, `−3.331e-16`, `1.582e-16`, `0.0`, `2.497e-16`, `4.885e-15`, `1.874e-14` ✓ (eigenvalues `h^{-2},h,h` confirmed) |
| Coupled peaks `4.36/4.99/5.52e-5` vs `3.62e-5` uncoupled; refined `3.61/4.35/4.97/5.50e-5`; `|u|` peaks `5.18/5.14/2.38/5.26e-5` | `fe-evidence/runs/fabric_mandel_*, fabric_contour_*`, `figures/fe_fabric_contours.csv` | `4.3628, 4.9901, 5.5211, 3.6164e-5`; `3.6062, 4.3491, 4.9727, 5.5031e-5`; `5.1826, 5.1372, 2.3818, 5.2587e-5` ✓ |
| "Each peak coincides with the final recorded state rather than a transient overshoot" | `fe-evidence/runs/fabric_mandel_coup_a45/solution.csv` | centre pressure rises `4.890e-5 → 4.966e-5 → 4.990e-5`, last step = reported peak ✓ |

**Claim strength.** I also checked hedge/claim balance. The strong statements are matched by their evidence and the qualifications are placed where the evidence stops: the abstract's "no quantitative finite-deformation verification and no experimental validation are claimed for those demonstrations"; "no order above one is asserted"; "That agreement is an implementation check, not an independent derivation"; "the fabric law ... shares the section's modelling conventions"; "Not comparable and excluded from the verification claims" for the square-domain partial-drainage runs. I found no overstatement that the artifacts contradict, and no hedge so weak that it understates the evidence. One optional note on wording is R3-O5.

---

## REQUIRED ITEMS

### R3-C1 — Two decorations (hat and tilde) are both defined as "the true frame", with no stated criterion to choose between them

**Rule as stated (rule for the hat)** — `main.tex:224`:
> "A bar on a stress denotes its representation in the mixture frame, whereas a hat denotes the true frame."

**Rule as stated (rule for the tilde)** — `main.tex:258–261`:
> "A wide tilde denotes the representation of a mixture-frame quantity in the true (mineral) frame, obtained by the inverse rotation \(\mathbf R_A^T\), as in \(\widetilde{\mathbf\tau}=\mathbf R_A^T\mathbf\tau'\mathbf R_A\) of \eqref{eq:fabric-phase-work}."

**Instance it must match.** The hat is applied to \(\widehat{\mathbf\sigma}_s\), "the intrinsic mineral Cauchy stress in the frame reached by \(\bar{\mathbf F}\)" (`main.tex:281–286`) and to \(\widehat{\mathbf\tau}_s\), "the true-frame Kirchhoff stress" (`main.tex:312–320`, used again at `main.tex:380`). The tilde is applied at `main.tex:260` and `sections/pore_fabric.tex:172–184`. Both decorations therefore denote the same frame: by the second quoted rule \(\widetilde{\mathbf\tau}\) is the true-frame representation of the mixture-frame effective stress \(\mathbf\tau'\), and consequently \(\widetilde{\bar{\mathbf\tau}_s}=\widehat{\mathbf\tau}_s\) through \eqref{eq:rotated-mineral-kirchhoff} — a hat and a tilde are two spellings of one and the same frame. Equation (74) (`sections/pore_fabric.tex:172–184`) puts both decorations side by side: the first term contracts \(\widetilde{\mathbf\tau}\), the second \(\widehat{\mathbf\tau}_s\), so the reader meets a hat and a tilde in one line with no rule to say why. By the stated hat rule, the true-frame representation of \(\tau'\) would be expected to carry a hat.

The paragraph does state a normalization rule that separates the barred stresses (`main.tex:226–231`: \(\bar{\mathbf\sigma}_s\) per current mineral volume, \(\bar{\mathbf\tau}_s\) per reference mineral volume), but states no normalization for the hat/tilde pair. The two instances do in fact differ in normalization (\(\mathbf\tau'\) is per reference mixture volume; \(\widehat{\mathbf\tau}_s\) is per reference mineral volume), and that is the only thing distinguishing the symbols.

**Required fix.** State the criterion that selects hat versus tilde (for example: "a hat marks an intrinsic mineral quantity with its mineral normalization, a tilde marks a mixture-normalized quantity rotated into the mineral frame"), or reduce the two decorations to one. As it stands, a reader cannot determine from the notation paragraph which decoration a given true-frame object must carry.

### R3-C2 — The epithet "fixed-pressure" is attached to a double-primed object and to a single-primed object in the same rule

**Rule as stated** — `main.tex:237–243`:
> "A single prime denotes the effective stress that carries the full pore-pressure term, as in \(\mathbf\sigma'\) of \eqref{eq:total-cauchy-single-prime}, and a double prime denotes the fixed-pressure stress \(\mathbf P''\) of \eqref{eq:fixed-pressure-stress}, so that \(\mathbf\sigma=\mathbf\sigma''-p\mathbf B\) in \eqref{eq:finite-biot-tensor}. The same two marks name the reduced energies of \cref{sec:finite-biot} at the prescribed pressure: \(W''\) of \eqref{eq:reduced-energy} and its fixed-pressure companion \(W'\) of \eqref{eq:legendre-energy}."

**Instance it must match.** From `main.tex:461–476`: \(W''(\mathbf F,p)=W_s(\mathbf F,\bar J(\mathbf F,p))\) and \(W'(\mathbf F,p)=W''+\phi_{s0}p\bar J(\mathbf F,p)\); \(\mathbf P''=\partial W''/\partial\mathbf F|_p\) and \(\mathbf P'=\partial W'/\partial\mathbf F|_p=\mathbf P''+\phi_{s0}p\,\partial\bar J/\partial\mathbf F|_p\). The paired objects at a prescribed pressure are therefore \((W'',\mathbf P'')\) and \((W',\mathbf P')\). As written, the adjective "fixed-pressure" is given to the **double-primed stress** \(\mathbf P''\) and simultaneously to the **single-primed energy** \(W'\), while the double-primed energy \(W''\) is called "reduced". A reader applying the rule "double prime = fixed-pressure" is sent to \(W''\) for the energy and to \(\mathbf P''\) for the stress, i.e. one word names two members that carry opposite marks. (The discussion repeats the same collision: `main.tex` "The fixed-pressure effective stress \(\mathbf\sigma''\) itself depends on pressure.")

**Required fix.** Make the epithet follow the mark, for example "the reduced potential \(W''\) of (44), whose fixed-pressure derivative is the stress \(\mathbf P''\) of (46), and its single-primed Legendre companion \(W'\) of (45)"; or rename one member consistently throughout. No computational change is implied — the marks themselves pair correctly ((\(W'',\mathbf P'',\mathbf\sigma''\)) and (\(W',\mathbf P',\mathbf\sigma'\))) — the defect is that the stated verbal rule contradicts its own instances.

---

## OPTIONAL NOTES

**R3-O1 (cosmetic).** `build/main.log:849` — `Underfull \hbox (badness 1137) in paragraph at lines 33--40`, in the bibliography (`build/main.bbl`). There is no overfull box, no undefined reference/citation and no missing glyph anywhere in the build. A small hyphenation allowance in the bibliography would clear it.

**R3-O2 (claim scoping).** `sections/experiments.tex`, "The largest absolute error among its constitutive identities is \(2.5\times10^{-9}\)". The matching artifact `build/conformal/verification.json` also contains three larger values in a separate category — `second_order_pressure` `1.085e-2`, `second_order_energy_stress` `3.930e-4`, `second_order_pore_volume` `2.117e-4`, category `convergence`. The sentence is correct as scoped to "constitutive identities", but naming the excluded category in the same breath (they are refinement-fit residuals, i.e. convergence measures, not identities) would make the scope self-evident to a reader who opens the artifact.

**R3-O3 (notation completeness).** `main.tex:263` states "Fourth-order tensors are set in blackboard bold and second-order tensors in upright bold", but first-order tensors are also set in upright bold throughout (\(\mathbf m\), \(\mathbf n\), \(\mathbf e_t\), \(\mathbf q\), \(\mathbf u\), \(\mathbf v\), \(\mathbf p_1\), \(\mathbf p_2\) in `sections/pore_fabric.tex`, `sections/experiments.tex`, `sections/finite_elements.tex`) without a stated rule; adding "and vectors" costs nothing. Relatedly, the in-plane vectors \(\mathbf p_1,\mathbf p_2\) (`sections/pore_fabric.tex`) differ from the first Piola stress \(\mathbf P\) only in case; a half-sentence would remove any ambiguity.

**R3-O4 (brittle cross-references).** `main.tex:245–258` cites "section 5", "section 7", "section 3", "section 9" as literal numbers instead of `\cref`. They resolve correctly in this snapshot (verified against the rendered PDF: `sec:finite-biot` = 5, `sec:pore-fabric` = 7, `sec:work-equivalence` = 3, `sec:finite-elements` = 9), but they will break silently if sections are reordered. Replace with `\cref` for the same reason the rest of the manuscript uses it.

**R3-O5 (claim strength, mild).** `main.tex` (Introduction), "Together these observations establish two facts: fabric, not porosity alone, controls the effective poroelastic properties, and reactions create and orient pore structure." The cited literature supports both statements, and the immediately following novelty claim is properly hedged ("we are not aware of a tensorial distention law"). However "establish two facts" reads as a stronger warrant than a survey of cited work provides; "establish two points" or "support two conclusions" would match the evidence exactly. Not a defect, only a wording suggestion.

---

VERDICT: MINOR REVISION
