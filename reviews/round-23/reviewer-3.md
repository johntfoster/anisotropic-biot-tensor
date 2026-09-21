# Round 23 — Reviewer 3

Independent review of the frozen snapshot only:
`.agent-runtime/review-snapshots/round-23`
SNAPSHOT_ID `53af8afca869198eb1560733c6b9f0377accc0570d36b9dcbeddecc36142ddc5` (556 files).

Scope: prose, notation, significance, claim discipline. All statements below were
checked against the snapshot artifacts themselves (`main.tex`, `sections/*.tex`,
`references.bib`, `site/evidence.json`, `figures/*.csv`, `build/`, `fe-evidence/`,
`validation/`, `examples/`), not against any prior review or summary.

## Step 1 — integrity

- `sha256(source-manifest.json)` = `53af8afca869198eb1560733c6b9f0377accc0570d36b9dcbeddecc36142ddc5`
  = declared SNAPSHOT_ID. **Match.**
- Re-hashed every one of the 556 listed files: **556 OK, 0 missing, 0 mismatch.**
- Integrity: **OK.** Proceeded to the manuscript review.

## Verified positively (no action)

- **Citation keys.** Every `\cite`/`\citep`/`\citet` key resolves to a `references.bib`
  entry, including keys hidden behind optional arguments
  (`walker2023poroelasticity` `sections/finite_elements.tex:158`, `drumheller2000`
  `main.tex:604`, `gajo2010` `sections/limits.tex:40`). No dangling key, no uncited
  bib entry, no undefined `\ref`/`\cref`/`\eqref`. All nine `\includegraphics`
  targets exist (`build/conformal/*.pdf`, `figures/fe_*.pdf`); all nine figure labels
  are cited from the text; `build/main.log` has no unresolved-reference or
  multiply-defined warnings and reports 32 pages written.
- **`d` vs `dis`.** The disambiguation is explicit and hold throughout:
  superscript \(d\) is drained only (`main.tex:222`, used as \(\mathbb{C}^d\);
  \(\mathbb{C}^d\) appears only as "drained" at `sections/stress_reconstruction.tex:26`,
  `sections/limits.tex:10,25`, `sections/pore_fabric.tex:265,295,297`), and the
  distention quantities carry the subscript \(\mathrm{dis}\)
  (\(W_{\mathrm{dis}},\mathbf E_{\mathrm{dis}},\mathbf S_{\mathrm{dis}}\),
  `main.tex:223-225`, `sections/pore_fabric.tex:112-129,249-253`). No occurrence of
  \(d\) meaning distention.
- **Unit tangent vs reference traction are distinct.** The current unit tangent is
  \(\mathbf e_t\) (`sections/experiments.tex:94-97`); the reference traction is
  \(\mathbf t_0\) (`sections/finite_elements.tex:100,105`). No collision between them.
- **No "five-modulus"/"full rank" contradiction remains.** Neither phrase occurs
  anywhere in the manuscript (or in `site/`, `README.md`). The retained law is
  described consistently as the **rank-two** axisymmetric block
  `(k_v,k_a,k_c)` on the volumetric–axial subspace with four frozen complementary
  modes (`sections/pore_fabric.tex:277-291`, `sections/finite_elements.tex:262-267`).
- **Standing author decision is respected.** `sec:fabric-transverse`
  (`sections/pore_fabric.tex:359-361`) names the volume–axial distention coupling
  modulus as the carrier of \(B_\parallel\neq B_\perp\); the probe data confirm it
  (`figures/fe_fabric_probe.csv`: with coupling \(=0\) or "soft axial", \(B_\parallel=B_\perp\);
  with coupling \(=0.4\), \(B_\parallel=0.85065\), \(B_\perp=0.91027\)).
- **Conclusions' temporal-order caveat matches the companion site.**
  `main.tex:564-573` and `sections/finite_elements.tex:202-232` state the same
  caveat as `site/evidence.json` (convergence summary): the fixed-mesh
  successive-difference orders are *measurements* that include values above one and
  arise from a retained mesh–step cross term, and **no order above one is asserted**.
  No divergence between manuscript and site.
- **Novelty claim is scoped, not an unqualified priority claim.** `main.tex:141-143`
  reads "Among the fabric-elasticity and fabric-poroelasticity constructions surveyed
  here, we are not aware of a tensorial distention law…". This is a survey-scoped
  statement, not a "first" claim.
- **Headline numbers trace to snapshot artifacts.** All of the following were
  re-derived from recorded files: pressure floor \(3.2\times10^{-3}\)
  (`figures/fe_load_limit.csv` → `3.2209e-3` at load `1e-4`); linear step refinement
  \(3.66\times10^{-3}\) and \(7.10\times10^{-3}\), ratio \(1.94\)
  (`figures/fe_mandel_refinement.csv`); temporal orders \(0.98\)–\(1.40\)
  (`fe-evidence/mms-convergence.json`); MMS spatial orders p \(2.00/2.00\), \(u_x\)
  \(2.99/2.96\), \(u_y\) \(3.00/2.96\) (`figures/fe_mms_convergence.csv`); 186 checks
  with largest constitutive identity error \(2.45\times10^{-9}\)
  (`build/conformal/verification.json`); 273 states across 13 mineral stiffnesses
  (`build/weighted-stress/tensor-verification.json`); reference Biot components
  \(0.7000/0.7583/0.7917\) (`build/conformal/pressure_response.csv`,
  `build/weighted-stress/pressure.dat`); fabric-coupled peak centre pressures
  \(4.38/4.98/5.50\times10^{-5}\) vs \(3.65\times10^{-5}\) uncoupled
  (`figures/fe_fabric_mandel_peak.csv`, peaks equal final values as claimed).
- **Significance claim is earned and disciplined.** Every finite-load result is
  labeled a demonstration, not quantitative verification, and no experimental
  validation is claimed (`main.tex:44-53,564-580`, `sections/finite_elements.tex:333-352`).

## REQUIRED items

1. **Undefined symbols \(\mathbf p_1,\mathbf p_2\).**
   `sections/pore_fabric.tex:289-290` defines
   \(\mathbf e_3=(\mathbf p_1\otimes\mathbf p_1-\mathbf p_2\otimes\mathbf p_2)/\sqrt2\)
   and \(\mathbf e_6=\sqrt2\,\operatorname{sym}(\mathbf p_1\otimes\mathbf p_2)\), but
   \(\mathbf p_1,\mathbf p_2\) are never introduced anywhere in the manuscript (their
   only occurrences in the whole source are these two lines). Define them at first use
   (e.g., "let \(\mathbf p_1,\mathbf p_2\) be orthonormal vectors spanning the plane
   normal to \(\mathbf m\)") or rewrite \(\mathbf e_3,\mathbf e_6\) explicitly in terms
   of \(\mathbf m\) and an in-plane direction. This is a reader-blocking omission in the
   notation section the paper leans on for its central claim.

2. **Overloaded \(\mathbf e_\bullet\) family and Mandel-index collision.**
   The same `\mathbf e` prefix denotes three different objects:
   (i) the unit tangent \(\mathbf e_t\) (`sections/experiments.tex:94-97,103`);
   (ii) the retained subspace basis \(\mathbf e_1,\mathbf e_2\)
   (`sections/pore_fabric.tex:305`); and (iii) the in-plane modes
   \(\mathbf e_3,\mathbf e_6\) (`sections/pore_fabric.tex:289-290`, reused at
   `sections/finite_elements.tex:272-273`). Worse, the numeric labels \(\mathbf e_3,
   \mathbf e_6\) collide conceptually with the Mandel basis ordering
   "\(11,22,33,23,13,12\)" stated at `sections/experiments.tex:9`, where component 3 is
   the "33" normal component and component 6 the "12" shear — whereas here
   \(\mathbf e_3\) is the \((11-22)/\sqrt2\) deviatoric in-plane mode. Introduce a single
   definition of \(\mathbf e_1,\dots,\mathbf e_6\) (or relabel the fabric modes) and add a
   one-line note that these labels are **not** the Mandel component indices of
   `eq:example-mineral-stiffness`.

## Optional notes

1. **Drained shear modulus vs distention tensor.** \(G=0.75\)
   (`sections/finite_elements.tex:164`) uses the same letter as the distention tensor
   \(\mathbf G\), introduced at `sections/pore_fabric.tex:23` and used ~59 times. Bold
   vs italic distinguishes them, but the two are close enough (and \(\mathbf G\) central
   enough) that a distinct symbol (e.g., \(\mu_d\) or \(G_d\)) would read more safely.

2. **Time-step symbol inconsistency.** The conclusion uses italic \(dt\)
   (`main.tex:565,569`) while the accompanying section uses \(\Delta t\)
   (`sections/finite_elements.tex:210`). Unify on one symbol (and note the manuscript
   already defines the `\dd` differential macro at `main.tex:20`).

3. **"as the load tends to \(10^{-4}\)"** (`main.tex:566-567`) is imprecise: the
   smallest sampled normalized load is \(q_L/K=10^{-4}\)
   (`figures/fe_load_limit.csv`), and `sections/finite_elements.tex:168` phrases the
   same statement as "\(q_L/K\) tends to zero". Reword to something like "remains at
   about \(3.2\times10^{-3}\) at the smallest sampled load \(q_L/K=10^{-4}\)".

4. **Long sentence in the conclusion** (`main.tex:564-573`): one sentence carries the
   load limit, the floor value, the backward-Euler attribution, the step-refinement
   numbers, the successive-difference orders, and the caveat. Splitting it into two or
   three sentences would improve readability without changing content.

5. **Long final abstract sentence** (`main.tex:57-68`) similarly packs the fabric law,
   the relaxation of the rank-one restriction, and the two anisotropy sources into one
   sentence; a split would help.

6. **`braun2020` key vs year.** `references.bib:87,91` keys the entry `braun2020` but
   gives `year = {2021}`. Harmless, but the key/year mismatch invites confusion in a
   future cross-reference; rename to `braun2021` (and update the one citation at
   `main.tex:107`).

7. **Duplicate limitation in the companion manifest.** `site/evidence.json:482` and
   `:483` state the same pore-fabric limitation, the second a superset of the first.
   Not part of the manuscript, but the companion should carry it once.

VERDICT: MINOR REVISION
