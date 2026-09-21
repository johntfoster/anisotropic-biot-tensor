# Round 19 — Reviewer 3 (prose, notation, significance, claim discipline)

Reviewer role: independent Reviewer 3 — prose, notation, cross-reference/citation
integrity, claim discipline, and significance for a JMPS-style audience.
Reviewed artifact: the frozen read-only snapshot at
`.agent-runtime/review-snapshots/round-19`, and nothing else. Simulated AI peer
review, not a journal submission. No manuscript or snapshot file was modified;
scratch work was confined to `/tmp`.

---

## 1. Snapshot identity and manifest

**Identity — confirmed.**

| Item | Value |
|---|---|
| Snapshot root | `.agent-runtime/review-snapshots/round-19` |
| `SNAPSHOT_ID` file contents | `ceb3783ac7945cc3f8c31c4d6be514fae873d316a18f3c163dcb78fcb4b6d682` |
| `sha256sum source-manifest.json` | `ceb3783ac7945cc3f8c31c4d6be514fae873d316a18f3c163dcb78fcb4b6d682` |
| Declared SNAPSHOT_ID | `ceb3783ac7945cc3f8c31c4d6be514fae873d316a18f3c163dcb78fcb4b6d682` |

The hash of the manifest equals the declared snapshot ID, and the contents of
`SNAPSHOT_ID` agree. **Match confirmed.**

**Per-file re-hash — confirmed.**

- Manifest entries: **534**
- Present and hash-matching: **534**
- Missing files: **0**
- Hash mismatches: **0**
- Files present but not listed: **2** — `SNAPSHOT_ID` and
  `source-manifest.json`. Both are expected: a manifest cannot carry a hash of
  itself, and the ID file has to sit beside it. No unlisted manuscript,
  evidence, figure, or script payload was found.

The manifest covers the manuscript (`main.tex`, `references.bib`, six
`sections/*.tex`), the embedded archive, all figure/data files under
`build/`, `figures/`, `fe-evidence/`, `site/`, `validation/`, and `moose_app/`.
Snapshot integrity is clean and the review below was performed against it.

---

## 2. Notation

**What holds up.** The paper is unusually careful here, and most of the
reviewer risk in the new fabric material has been managed deliberately.

- The accent conventions are explicitly enumerated in `main.tex` (lines
  ~86–94): bar on a kinematic/energetic quantity = the mineral (distention
  removed) state; bar on an intrinsic density = per-phase-volume; bar on a
  stress = mixture-frame representation (hat = true frame); bar on a boundary
  datum = prescribed value. Four meanings, but each is stated once.
- Fourth-order tensors blackboard bold, second-order bold — stated and honoured
  throughout, including the new `\mathbb{D}`.
- New fabric symbols are all introduced at first use and in a sensible order:
  `\mathbf{A}` and `\mathbf{R}_A` (§2), `\mathbf{G}`, `\mathbf{H}`,
  `\mathbf{E}_d`, `\bar{\mathbf{S}}_d`, `\mathbf{S}_d`, `\mathbb{D}`,
  `\mathbf{m}`, `h` (§6).
- I re-derived the new algebra rather than accepting it. `\mathbf{H}` in
  eq. `fabric-transverse-h` does have unit determinant
  (`h^{-2}\cdot h\cdot h = 1`); eq. `fabric-transverse-strain`
  (`\mathbf{E}_d=\frac{\ln a}{3}\mathbf{I}+\ln h(\frac12\mathbf{I}-\frac32\mathbf{m}\otimes\mathbf{m})`)
  follows correctly from `\mathbf{E}_d=\frac12\ln\mathbf{G}` with
  `\mathbf{G}=a^{2/3}\mathbf{H}`; and eq. `fabric-mineral-metric` follows
  correctly from eq. `fabric-multiplicative`.
- I also checked the conformal reduction of the new compliance identity
  numerically (independent route: minimise
  `W_d(\mathbf{E}_d)+\frac{1}{2}\phi_{s0}(\boldsymbol\varepsilon-\mathbf{E}_d):\mathbb{C}_s:(\boldsymbol\varepsilon-\mathbf{E}_d)`).
  With `\mathbb{D}=\alpha\,\mathbf{I}\otimes\mathbf{I}` and
  `\alpha=K/(1-K/(\phi_{s0}K_s))`, eq. `fabric-compliance-restriction` and
  eq. `drained-compliance-restriction` agree exactly **and** the same `\alpha`
  reproduces `W_A(a)` of eq. `distention-energy` (`\frac{K}{2(1-K/(\phi_{s0}K_s))}(\ln a)^2`).
  There is no factor-of-three or convention error hiding in that reduction.

**Defects.**

### R3-01 — **required** — `W_d` denotes two different energies
`W_d` is the **drained skeleton energy** in §"Logarithmic Hooke laws and the
drained response", and the **distention energy** in §"Pore fabric and
shape-changing distention". Same symbol, two meanings, one manuscript.

- Drained meaning: `sections/stress_reconstruction.tex` lines 34
  (`\pder{W_d}{\boldsymbol\varepsilon}=\mathbb{C}^d:\boldsymbol\varepsilon`,
  eq. `prescribed-skeleton-log-hooke`), 45
  (`W_d=\frac12\boldsymbol\varepsilon:\mathbb{C}^d:\boldsymbol\varepsilon`,
  eq. `prescribed-logarithmic-energies`), 49 ("the coupled energy must recover
  `W_d`"), 201.
- Distention meaning: `sections/pore_fabric.tex` lines 112, 117, 122, 123,
  128, 129, 182, 201, 203, 207, 211, 244, 254, 283, 294, 313, and
  `main.tex` line 571 ("the fabric tensor a constitutive variable with its own
  energy `W_d(\mathbf G)`").
- Compounding it, the superscript `d` means *drained* in `\mathbb{C}^d`, while
  the subscript `d` means *distention* in `W_d`, `\mathbf{S}_d`,
  `\bar{\mathbf{S}}_d`, `\mathbf{E}_d`.
- Section 6 does carry one bridging sentence ("replacing the volume-only energy
  `W_A(a)`"), but it does not rename the symbol, so a reader who meets
  `W_d(\mathbf G)` in eq. `fabric-equivalent-energy` has a real chance of
  reading it as the drained skeleton energy introduced three sections earlier.
- Fix: rename one family (e.g. distention energy `\Phi_d(\mathbf G)` in §6 and
  the Discussion, or drained energy `\bar{W}^{\,\mathrm{dr}}` in §4).

### R3-02 — **required** — `a` is reused: distention volume ratio and Mandel half-width
`a = \det\mathbf{A}` is the distention volume ratio and is used continuously
from §2 through §6 and the Discussion. In §"Reference problems and error
measures" the same symbol is silently reassigned:
`sections/finite_elements.tex` line 153 — "The full reference rectangle is
`[-a,a]\times[-b,b]`, with `a=1` and `b=0.1`". Nothing marks the change of
meaning, and the section immediately before and after uses `a` in the
poromechanical sense via `\phi_s a=\phi_{s0}` from §6. Fix: use `L`/`w` (or
`a_R`) for the rectangle half-width.

### R3-03 — **optional** — residual overloads worth tightening
- `\mathbf{S}_d` (distention stress) and `S_s` (solid storage) are
  typographically close and both new-ish; `G` (drained shear modulus, §FE) vs
  `\mathbf{G}` (distention tensor, §6); `U` (MMS amplitude, §FE) vs
  `\mathbf U` (right stretch, §4); `t` (time) vs `\mathbf t` (tangent, §7).
  Each is disambiguated by case/weight, but in a paper this notation-dense the
  near-collisions cost the reader.
- The four-way overload of the bar accent is disclosed, but it is still heavy;
  if R3-01 is fixed, consider whether a dedicated glyph for the mineral energy
  (`\Psi_s`) would reduce the load further.

---

## 3. Cross-reference and citation integrity

**References.** 134 `\label`s, all unique (no duplicate-label risk). Every
`\ref`, `\eqref`, `\cref`, and `\Cref` target resolves: **0 unresolved
targets.** `build/main.log` (28-page LuaLaTeX build) contains no undefined
reference, no undefined citation, and no BibTeX warning; the only log hits for
"warning/error" are package-loading noise lines. The snapshot does not carry
`.aux`/`.bbl`, so resolution was established by static label↔reference
matching plus the clean log — two independent methods agreeing.

Cross-section pointers in the new material are correct
(`\cref{sec:kinematics,sec:work-equivalence}`, `\cref{sec:logarithmic-derivative}`,
`\cref{sec:fe-fabric}`, `\cref{sec:pore-fabric}` all point where the prose
says they point).

**Citations.** 36 bibliography entries, 36 distinct keys cited: **no
cited-but-missing entry, no dead entry, no duplicated DOI.** Every new
fabric/serpentinization/geoscience entry is used where the text claims it
supports the argument.

**Figures.** All seven `\includegraphics` targets exist on disk
(`build/conformal/{pressure,shear,directional,rotation,constrained_layer}_response.pdf`
or `..._layer.pdf`, `figures/fe_fabric_probe.pdf`, `figures/fe_fabric_mandel.pdf`).

### R3-04 — **required** — two new figures are never cited from the text
`fig:fe-fabric-probe` (`sections/finite_elements.tex` line 233) and
`fig:fe-fabric-mandel` (line 255) carry labels but no `Figure~\ref{...}` /
`\cref` anywhere in the manuscript. They are also the only two floats in the
paper with this defect. Both are load-bearing for the fabric contribution —
the probe figure is the only place `B_\parallel\ne B_\perp` is shown, and the
mandel figure is the only coupled fabric evidence — so they must be called out
in the prose ("Figure ... shows ...").

**Citation spot-checks (new literature).** I verified that each new entry
corresponds to a genuine publication, and that the cited work supports the
claim where checkable:

- `cowin1985fabric`, `turnercowin1987`, `moesencardosocowin2012`,
  `cowin2004fabric`, `cowinmehrabadi2007`, `hudson1981` — real; used exactly
  as the fabric/elasticity and fabric/poroelasticity literature claims require.
- `rudgekelemen2010`, `jons2017`, `uno2022`, `putnis2002`, `putnis2009`,
  `ruizagudo2014`, `geisler2007`, `altreewilliams2015` — real; the
  reaction-induced-cracking and mineral-replacement claims match these works.
- `walker2023poroelasticity` — confirmed real (GJI 235(3):2442, 2023) and the
  paper does treat Mandel's problem; the specific `[appendix D]` pointer could
  not be verified from the snapshot alone (see R3-08).
- `dehghanipentamerodio2019`, `dehghanizilian2021`, `zha1996forsterite`,
  `gaston2009moose`, `gajo2010`, `debuhan1998`, `macminnetal2016`,
  `zhaoborja2020`, `biot1955anisotropic`, `biotwillis1957`,
  `thompsonwillis1991`, `cheng1997`, `wong2017`, `sviridov2017`, `braun2020`,
  `makhnenkolabuz2016`, `chaubazantsu2016`, `flory1961`, `drumheller2000` —
  all consistent with genuine, properly identified publications.

---

## 4. Structure and duplication

**Arc.** The narrative arc holds: motivation (introduction: anisotropy in
shales/claystones/cracked rock, fabric lore, reaction-generated fabric) →
theory (kinematics, reversible work and energy equivalence, logarithmic Hooke
laws and the drained restriction, finite-deformation Biot tensor and limits)
→ new constitutive law (pore fabric) → implementation (coupled FE) →
verification → significance (discussion). Section ordering is coherent and the
equations needed downstream are all introduced upstream.

**Integration, not restatement.** The new fabric material is genuinely
integrated. `sections/pore_fabric.tex` derives from `\eqref{eq:coupled-energy-work}`,
`\eqref{eq:constitutive-kirchhoff-phase-stress}`, and
`\eqref{eq:spatial-distention}`-adjacent results rather than restating them,
recovers the conformal limit explicitly ("recovering
`\eqref{eq:distention-mineral-energy-work}` exactly"), and states which steps
are new modelling choices rather than consequences of the conformal model.
The Discussion then closes the loop by pointing forward to `\cref{sec:pore-fabric}`.
This is the right structure.

### R3-05 — **optional** — verification-scope disclaimer is stated four times
The same "demonstrations, not quantitative verification, not experimental
validation, synthetic parameters" caveat appears in (i) the abstract, (ii) the
end of `sec:experiments`, (iii) the `sec:fe-fabric` closing paragraph, and
(iv) the "Scope of these results" paragraph. This is honest and I would rather
have it than not, but four statements of the same limit is more than claim
discipline requires and dilutes the significance paragraph. One consolidated
scope statement in the FE section plus the abstract sentence would do.

### R3-06 — **optional** — abstract length and overlap with the conclusion
The abstract is **315 words** and reproduces much of the Discussion almost
step for step (work/energy route, rotation cancellation, rank-one compliance,
rotation of mineral stress, isotropic reduction, verification, fabric
extension). A 200–230-word abstract that keeps the two results (rank-one
drained restriction from conformal distention; tensorial distention law and
fabric-driven anisotropic Biot tensor) would read better and lose no content.

### R3-07 — **optional** — the numerical-supplement script list is incomplete
`sections/experiments.tex` names `examples/conformal_model.py`,
`examples/conformal_experiments.py`, and `examples/verify_conformal.py`, and
the "Code and data availability" paragraph describes the archive generically.
But `sec:fe-fabric` relies on a fabric verification whose scripts
(`examples/verify_fabric.py`, `examples/plot_fabric_results.py`) and
evidence file (`build/fabric/fabric-verification.json`) are never named
anywhere in the text, and are absent from the availability paragraph. Given
that the material-point fabric check is one of the paper's claimed
verification results, it should be named and its evidence file pointed to.

---

## 5. Quantitative-claim discipline

This is the strongest part of the manuscript. Every quantitative claim I could
test in prose matches its source data. Verified item by item:

| Claim (location) | Source data | Verdict |
|---|---|---|
| Reference Biot components `0.7000, 0.7583, 0.7917` (`sec:experiments`) | `build/conformal/experiments.json` → `highlights.reference_B = [0.7, 0.75833, 0.79167]` | match |
| Mineral shear modulus `16.8K_*` = mean of the five deviatoric modes of `\mathbb{C}_s`, halved | I computed the five deviatoric modes of eq. `example-mineral-stiffness`: `42.967, 53.033, 20, 24, 28` → mean `33.6` → half `16.8` | match (independent computation) |
| `K_s=28K_*`, `K=7K_*`, `0<K<\phi_{s0}K_s` | `experiments.json`; `(1/9)\mathbf I:\mathbb{C}_s:\mathbf I = 28.0`; `0.6\times28=16.8>7` | match |
| "conformal verification suite contains 186 named checks" | `build/conformal/verification.json` → `checks_passed = 186` | match |
| "the 65 per-state identities (five states times thirteen identities) and the two reference Biot and rank-one compliance relations" | I grouped the 186 checks: 5 `legacy_stateN_*` families × 13 identities = 65, plus `legacy_reference_biot` and `legacy_reference_rank_one_compliance_identity` = 67 | match, including the decomposition |
| "largest absolute error among its constitutive identities is `2.5\times10^{-9}`" | `max_constitutive_identity_error = 2.4549890331732928e-09` | match |
| "Step refinement ... gives second-order convergence" | `observed_orders` ≈ 2.000 for energy/stress, pore volume, pressure (last pressure order 1.989) | match, and the "before cancellation becomes significant" hedge is the right reading |
| "273 finite states across 13 mineral stiffnesses" | `build/weighted-stress/tensor-verification.json` → `materials 13`, `states_per_material 21`, `total_states 273` | match |
| reconstruction suite checks work equivalence and finite unjacketed compression | `reconstruction-verification.json` has `work_equivalence` and `unjacketed` entries; `incompatible_pairs_rejected = 20` backs "arbitrary independent choices generally do not satisfy this relation" | match |
| "worst absolute difference of `4.9\times10^{-15}`" over fabric fields | `build/fabric/fabric-verification.json` → `worst_probe_abs_diff = 4.884981308350689e-15` | match |
| volume-only limit reproduces the conformal material "to `1.9\times10^{-14}`" | `conformal_cross_check` max |Δ| = `1.87436871579294e-14` (`sigma11`) | match |
| peak centre pressure `6.28/5.10/3.95\times10^{-5}` by fabric orientation, `5.13\times10^{-5}` uncoupled | `figures/fe_fabric_mandel_peak.csv` → `6.28029e-05`, `5.10216e-05`, `3.94613e-05`, `5.13255e-05` | match |
| "normalized pressure discrepancy floors at about `3.2\times10^{-3}` at `nx=20`, `dt=10^{-3}`" (Discussion) | `fe-evidence/runs/nonlinear_load_0.0001/analysis.json` → `pressure_max_normalized = 0.003220919735602341` with `configuration {nx:20, dt:0.001, load:0.0001}`; `site/evidence.json` carries the same statement | match, including the grid/step identification |
| FE reference problem: `B=0.6`, total storage `17/80`, `G=0.75` | `1-1/2.5=0.6`; `(1-\phi_{s0})/K_f+S_s = 0.1/8+0.2 = 0.2125 = 17/80`; `\phi_{s0}\mu_s = 0.9\times5/6 = 0.75` | match |
| "Pressure errors are normalized by the initial interior pressure, and displacement errors by the corresponding final drained displacement. Neither normalization divides by a transient value approaching zero." | `moose_app/scripts/analyze_mandel.py` lines 84–91 divide by `p0`, `uy_drained`, `ux_drained` | match |
| "All plotted states satisfy positive phase volumes and the scalar stability condition" | `experiments.json` → `solid_fraction_range [0.4343, 0.6]`, `min_scalar_stability = 28.0` | match |
| On the fixed-`\mathbf F=\mathbf I` pressure path the two materials share mineral volume | Mineral EOS with `\dev\boldsymbol\varepsilon=\mathbf 0`: `\bar J` depends only on `J`, `p`, `K`, `\phi_{s0}K_s` — identical for both materials | match |

Claim *framing* is also disciplined throughout: the FE section repeatedly says
the solved mineral volume is the solution of the EOS "not an independent
porosity law", the constant-permeability choice is flagged as "a different
constitutive choice", and the partial-drainage runs are explicitly excluded
from verification claims because the square domain is "not comparable" to the
slender Mandel geometry. I found no overstated quantitative statement. Two
wording items:

### R3-08 — **optional** — "rather than a transient overshoot" is not supported by the recorded window
`sections/finite_elements.tex` line 242: "Each peak coincides with the final
recorded state rather than a transient overshoot." The recorded history
(`figures/fe_fabric_mandel_history.csv`) has only four time samples per case
(`t = 0, 0.001, 0.002, 0.003`), and the centre pressure is still rising
monotonically at the last sample (`5.0977e-5 → 5.1231e-5 → 5.1326e-5`). The
literal statement (peak = final recorded state) is true, but "rather than a
transient overshoot" asserts something the sampling cannot establish: the run
stops while the pressure is still increasing, so a later overshoot is neither
seen nor ruled out. Recommend either extending the recorded window or
rewording to "the pressure rises monotonically to the final recorded state".

### R3-09 — **optional** — one interpretative sentence claims more than was shown
`main.tex` lines ~576–578: "This is the mechanism by which a reaction-induced
pore fabric enters the poromechanical response." The manuscript models no
reaction and no fabric evolution; §6 is an elastic equilibrium of a prescribed
`W_d(\mathbf G)`, and §8's coupled demonstration prescribes a rotated fabric
directly. The defensible statement is "This is a mechanism by which a
reaction-induced pore fabric would enter the poromechanical response" (or
"provides a route for"). As written it implies the reaction→fabric→`\mathbf B`
chain was demonstrated.

---

## 6. Significance

**Novelty (my own judgement).** Two results are genuinely new and are not, so
far as I can see, contained in the cited literature: (i) the derivation that
conformal (volume-only) distention forces the extra drained compliance to be
the specific spherical rank-one tensor of eq. `drained-compliance-restriction`,
i.e. that the restriction is *derived* rather than postulated; and (ii) the
tensorial distention law, in which a symmetric positive-definite distention
whose unimodular part is a pore-fabric tensor gives a fabric-driven,
directionally anisotropic finite-deformation Biot tensor through the same
energy route. The second is the more significant contribution and is the one
the abstract foregrounds.

### R3-10 — **required** — the novelty claim is not differentiated from Cowin's fabric poroelasticity
The introduction states: "What they do not supply is a tensorial distention
law, a constitutive relation stating how the shape and orientation of the pore
space enter a finite-deformation poromechanical energy and the Biot tensor
derived from it." But the same paragraph cites `cowin2004fabric`
("Anisotropic poroelasticity: Fabric tensor formulation") and
`cowinmehrabadi2007`, which already deliver a fabric-determined anisotropic
Biot tensor — at small strain, ad hoc rather than from an energy. As written,
a JMPS referee who knows that literature can read the gap claim as too broad.
Required fix: state explicitly that the new element relative to Cowin-type
fabric poroelasticity is (a) finite deformation, (b) the distention *energy*
and its work conjugate, and (c) the equilibrium that determines the fabric —
rather than fabric-determined coefficients. This is a positioning fix, not a
result problem, but the paper's headline novelty claim rests on it.

**Significance for the readership.** For JMPS, the paper's assets are the
energy-based derivation, the exact restriction result, and a verification
discipline (independent re-implementation, manufactured solution,
consolidation reference, explicit refusal to overclaim) that is better than
typical. The limitations are equally clear: synthetic moduli only, no
calibration, no reaction, and the fabric law's coupled evidence is a single
demonstration whose directional effect is carried by one modulus
(the volume–axial one — a point the paper states honestly in §6 and in the
probe figure caption).

**Engineering relevance.** The introduction motivates the work with
serpentinization/carbonation, reaction-induced cracking, and measured shale /
claystone / cracked-rock anisotropy — and the acknowledgements name hydrogen
storage and seismic-safe H₂ production projects — but no example touches a
real material or a mechanism-adjacent application. I would not demand a
calibration study, but the Discussion would be much stronger with one
paragraph of concrete engineering outlook (e.g. what a fabric-driven
`B_\parallel \ne B_\perp` would change in a storage or seal-integrity
prediction) and one sentence on what experiment would test
`B_\parallel \ne B_\perp` behind an isotropic mineral. Without it, the
reaction/fabric motivation reads as context rather than as the paper's target.

**Readability.** Dense but disciplined. Sentences are long, but each carries
one claim, hedges are explicit ("need not", "is not", "as measured"), and the
cross-section pointers do real work. Two small readability items already filed
(R3-06 abstract length, R3-05 repeated disclaimers). Terminology is
consistent: "distention", "distention gradient", "intermediate frame",
"mineral state", "mixture frame" are each used with one meaning throughout.

---

## 7. Findings

| ID | Class | Location | Issue | Evidence |
|---|---|---|---|---|
| R3-01 | **required** | `sections/stress_reconstruction.tex` 34, 45, 49, 201 vs `sections/pore_fabric.tex` 112–313 and `main.tex` 571 | `W_d` denotes the drained skeleton energy in §4 and the distention energy in §6; the `d` suffix also means "drained" in `\mathbb{C}^d`. Ambiguous to a reader meeting `W_d(\mathbf G)` in `\eqref{eq:fabric-equivalent-energy}`. | Direct text comparison of both families of uses; 22 occurrences total; no rename in the bridging paragraph. |
| R3-02 | **required** | `sections/finite_elements.tex` 153 | `a` reused: distention volume ratio `\det\mathbf A` (§2–§6) vs Mandel rectangle half-width (`[-a,a]\times[-b,b]`, `a=1`). | Same symbol, both live in the same paper; no redefinition sentence. |
| R3-03 | optional | whole manuscript | Residual near-collisions: `\mathbf S_d` vs `S_s`; `G` vs `\mathbf G`; `U` vs `\mathbf U`; `t` vs `\mathbf t`; four-way overload of the bar accent. | Typographic inspection of the symbol set. |
| R3-04 | **required** | `sections/finite_elements.tex` 233, 255 | `fig:fe-fabric-probe` and `fig:fe-fabric-mandel` are never referenced in the text (the only two such floats). | Label/reference matching over all six source files: these two labels appear in no `\ref`/`\cref`. |
| R3-05 | optional | abstract; `sec:experiments` end; `sec:fe-fabric` end; "Scope of these results" | The verification-scope disclaimer is stated four times. | Text search for the disclaimer across the manuscript. |
| R3-06 | optional | `main.tex` abstract | Abstract is 315 words and duplicates the Discussion closely. | Word count of the abstract block. |
| R3-07 | optional | `sections/experiments.tex` (availability paragraph), `sections/finite_elements.tex` `sec:fe-fabric` | The fabric verification scripts (`examples/verify_fabric.py`, `examples/plot_fabric_results.py`) and its evidence file (`build/fabric/fabric-verification.json`) are never named in the manuscript, although the material-point fabric check is a claimed verification result. | File list of the snapshot vs the text of the availability and FE sections. |
| R3-08 | optional | `sections/finite_elements.tex` 242 | "Each peak coincides with the final recorded state rather than a transient overshoot" — only four time samples per case, with pressure still rising at the last one. | `figures/fe_fabric_mandel_history.csv`: 4 times per case; centre pressure monotone increasing to the last recorded value. |
| R3-09 | optional | `main.tex` 576–578 | "This is the mechanism by which a reaction-induced pore fabric enters the poromechanical response" — no reaction or fabric evolution is modelled. | `sec:pore-fabric` defines an elastic equilibrium for a prescribed `W_d`; §8 prescribes the fabric rotation directly. |
| R3-10 | **required** | `main.tex` introduction, gap paragraph | "What they do not supply is a tensorial distention law ..." is not differentiated from `cowin2004fabric`/`cowinmehrabadi2007`, which already give a fabric-determined anisotropic Biot tensor. | Cited works listed in the same paragraph; the distinguishing features (finite deformation, distention energy and work conjugate, fabric equilibrium) are not stated. |

**Availability-paragraph integrity, folded into the required list above as
R3-11 and R3-12** (split out here because both are checkable defects rather
than judgements):

| R3-11 | **required** | `sections/experiments.tex` 212 vs `main.tex` `\embedfile` line 26 | The text says the numerical supplement is embedded in the PDF as `conformal-2026-09-20-v1.zip`; the PDF actually embeds `build/anisotropic-biot-2026-09-20-v2.zip`. Wrong name **and** wrong version. | `\embedfile[filespec=anisotropic-biot-2026-09-20-v2.zip,...]` in `main.tex`; archive present in the manifest under `build/`. |
| R3-12 | **required** | `sections/experiments.tex` 221 | "The coupled finite-element implementation of section~\ref{sec:finite-elements} is not part of that archive" is contradicted by the archive contents, which include `moose_app/include/materials/FabricMaterial.h`, `moose_app/include/utils/FabricLaw.h`, `moose_app/src/materials/FabricMaterial.C`, and the coupled decks `moose_app/inputs/{fabric_mandel.i, fabric_probe.i, conformal_probe.i}`. | `unzip -l build/anisotropic-biot-2026-09-20-v2.zip` (43 files), listing above. |

**Two verification pointers that I could not substantiate from the snapshot**
(neither is a defect in the manuscript; both are unverifiable-from-snapshot
citations, so I record them at the lowest weight):

| R3-13 | optional | `sections/finite_elements.tex` 151 | `\cite[appendix D]{walker2023poroelasticity}` — the work is real and does treat Mandel's problem (verified externally), but the appendix-D pointer cannot be checked against the snapshot. | External check confirms publication and subject; appendix letter unverified. |
| R3-14 | optional | `main.tex` 588 | `\citet[section~8.9]{drumheller2000}` — reference work is real and correctly cited in the bibliography; the section pointer cannot be checked against the snapshot (no PDF present). | Bibliography entry verified; section number unverified. |

**One bibliography-metadata note.**

| R3-15 | optional | `references.bib` `braun2020` | Key says 2020; entry year is 2021 (`Rock Mech Rock Eng` 54(1):377–396). Cosmetic under `plainnat` (keys are not printed), but the key will mislead future cross-referencing. | Bib entry as written; key/year disagreement. Also, `fosterxu2025` is given as article 106263 which matches the publisher's indexed record, while a secondary listing (the author's own CV page) shows 105259/`10.1016/j.jmps.2025.105259`; worth a one-line confirmation by the author. |

---

## 8. Overall assessment

**Correctness.** I found no mathematical error in the new material. I
independently re-derived the fabric kinematics (`\mathbf H` unimodularity, the
transverse-isotropic `\mathbf{E}_d`, the mineral metric), the linearised
additive strain split, and the conformal reduction of the fabric compliance
identity — including a numeric cross-check that the same `\alpha` reproduces
both `W_A(a)` and eq. `drained-compliance-restriction` — and all were correct.
I also re-verified the deviatoric-average construction of the isotropic
comparison modulus (`16.8K_*`) from the mineral Mandel matrix. Nothing in §6
appears to be asserted without derivation.

**Verification.** Genuinely strong for the conformal model (186 checks, 273
states over 13 minerals, MMS, consolidation reference, independent
re-implementation, second-order refinement), and scoped with unusual honesty
for the fabric extension. Every quoted number I could trace matches its JSON/CSV
source, including the specific `3.2\times10^{-3}` floor with its `nx=20`,
`dt=10^{-3}` identification.

**Novelty and significance.** Real and, for a mechanics audience, worthwhile:
an energy-derived restriction on drained compliance plus a tensorial
distention law that makes pore fabric a constitutive variable of finite-
deformation poroelasticity. Its main vulnerabilities are positioning
(R3-10) and the absence of any realistic application or calibration, which
the paper currently answers by disclaimer rather than by evidence.

**Character of the required fixes.** All required items are local and
mechanical — one symbol rename (R3-01), one symbol rename (R3-02), two text
citations for existing figures (R3-04), one availability-paragraph correction
covering two factual errors (R3-11, R3-12), and one introduction paragraph
sharpening the novelty claim against Cowin's fabric poroelasticity (R3-10).
None requires new derivation, new computation, or new evidence, and none
undermines any result. That is the profile of a minor revision, not a major
one: the science stands; the notation and two accuracy statements need
repair.

VERDICT: MINOR REVISION
