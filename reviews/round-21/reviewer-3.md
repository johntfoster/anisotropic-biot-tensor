# Independent peer review — Round 21, Reviewer 3

**Emphasis:** prose, notation, and significance.
**Snapshot under review:** `.agent-runtime/review-snapshots/round-21`
**Declared SNAPSHOT_ID:** `f4c43aeea1590c8e166d3ffab342e5da92094443e55b4df4d47b69bbad8c673f`
**Reviewer independence:** this review was prepared without reading any other reviewer's report, and without modifying any file in the snapshot.

---

## 1. Integrity verification

| Check | Result |
| --- | --- |
| `sha256(snapshot/source-manifest.json)` | `f4c43aeea1590c8e166d3ffab342e5da92094443e55b4df4d47b69bbad8c673f` — **equals the declared SNAPSHOT_ID** |
| Paths listed in manifest | 549 |
| Paths re-hashed and matching | 549 / 549 |
| Missing listed files | 0 |
| Hash mismatches | 0 |
| Files present on disk but unlisted | 2: `SNAPSHOT_ID`, `source-manifest.json` (the two snapshot bookkeeping files; expected, not defects) |

The snapshot is internally consistent and complete. All subsequent findings cite files inside this snapshot only. Numeric claims quoted below were checked against the snapshot's own data and reports.

---

## 2. Overall assessment

This is a carefully scoped manuscript. The distinctive contribution — separating mineral deformation from distention through a dilation-times-rotation (and later a symmetric positive-definite) distention gradient, then requiring the drained Hooke law to be reproduced — is stated precisely, and the manuscript is unusually disciplined about what it does *not* claim. The limitations language (synthetic parameters, local-only stability, demonstrations rather than quantitative verification, no experimental validation) is honest and appears consistently in the body, the companion evidence file, and the supplement README. Citation keys all resolve (`references.bib`, 36 cited keys, no undefined and no orphaned entries).

The problems I found are concentrated in two places: (i) a small number of genuine symbol collisions, chiefly the letter *d* and the symbol **t**, which bite hardest in the anisotropic fabric section; and (ii) a mismatch between the *advertised* finite-element verification and the *displayed* finite-element verification. None of these threatens the derivation. They are fixable without new science.

**Integrity-relevant side note (not a numbered item):** the manuscript's own data support every number I spot-checked — reference Biot components `0.7000, 0.7583, 0.7917` (`build/conformal/pressure_response.csv`, first anisotropic row); peak centre pressures `6.28e-5, 5.10e-5, 3.95e-5, 5.13e-5` (`figures/fe_fabric_mandel_peak.csv`); `186` named checks, `273` spherical-gauge states over `13` stiffnesses (`build/conformal/verification.json`, `build/weighted-stress/tensor-verification.json`); largest constitutive identity error `2.5e-9` (actual `2.455e-9`); figure sample counts (121 pressure states, 161 shear values, 361 one-degree directional samples, 121 rotation angles, 121 layer points) match the captions exactly. The isotropic-comparison construction, "the mean of the five deviatoric stiffness modes of `C_s`, divided by two", is also correct: the deviatoric eigenvalues are `{20, 24, 28, 42.967, 53.033}`, mean `33.6`, half `16.8`, matching `examples/conformal_model.py` and `build/conformal/experiments.json`.

---

## 3. REQUIRED changes

Every item below names a location inside the snapshot and the evidence that demonstrates the defect.

### R3-1 — The letter *d* carries two incompatible meanings; they co-occur inside one displayed equation

**Location:** `sections/stress_reconstruction.tex:26` and `:45` (`\mathbb{C}^d`, `W_{\mathrm{dr}}`, superscript/subscript **d = drained**); `sections/pore_fabric.tex:112`, `:117`, `:122`, `:128`, `:244` (`W_d`, `\bar{\mathbf S}_d`, `\mathbf S_d`, `\mathbf E_d`, **d = distention**); intersection at `sections/pore_fabric.tex:248–251`.

**Evidence.** The drained compliance is written `(\mathbb{C}^d)^{-1}` in `\eqref{eq:fabric-compliance-restriction}` (`sections/pore_fabric.tex:249`), while the same section, two lines earlier, defines `W_d` as the *distention* energy and `\mathbf E_d` as the distention strain (`sections/pore_fabric.tex:112`, `:128`). The two meanings appear in a single equation block:

```
(\mathbb{C}^d)^{-1} = (\phi_{s0}\mathbb{C}_s)^{-1} + \mathbb{D}^{-1}     (eq:fabric-compliance-restriction)
```

Here `\mathbb{C}^d` is drained (superscript) and `\mathbb{D}` is distention (different letter, same concept), so a reader tracking *d* has to switch meaning mid-equation. The abstract also exposes the collision, using "drained" in `main.tex:40` and the distention-based construction in `main.tex:58–63` within one paragraph.

**Required action.** Give drained and distention distinct labels throughout (for example, keep `\mathbb{C}^d` for drained and rename the distention quantities to a distinguishable tag such as `W_{\mathrm{dis}}`, `\mathbf E_{\mathrm{dis}}`, `\mathbf S_{\mathrm{dis}}`), or state the convention explicitly where the first distention subscript is introduced, and use a single convention for both. The symbol table concept is already present at `main.tex:207–219`; extend it to cover the drained/distention subscript pair.

---

### R3-2 — The symbol **t** denotes both a unit tangent vector and the reference traction

**Location:** `sections/experiments.tex:94–103` (`\mathbf t=(-\sin\theta,\cos\theta,0)^T`, "tangent"); `sections/finite_elements.tex:100` and `:105` (`\mathbf t_0`, "reference traction").

**Evidence.** Two adjacent sections of the same manuscript use upright bold **t** for two different physical objects. `sections/experiments.tex:103` evaluates `\mathbf t\cdot\mathbf B\mathbf n`; `sections/finite_elements.tex:105` integrates `\mathbf v\cdot\mathbf t_0`. The units and roles differ (dimensionless direction vs. traction), so no equation becomes wrong, but the collision is gratuitous because neither symbol is convention-bound.

**Required action.** Rename one of them (for example the tangent to `\mathbf e_t` or `\hat{\mathbf t}`), or rename the reference traction.

---

### R3-3 — Advertised finite-element verification has no in-manuscript display

**Location:** `main.tex:47–53` (abstract), `main.tex:550–562` (conclusions); `sections/finite_elements.tex:137–160` (reference problems and error measures), `:170–190` (manufactured solution).

**Evidence.** The manuscript contains exactly seven figures: five conformal material-point figures (`sections/experiments.tex:53, 84, 112, 137, 160`) and two pore-fabric figures (`sections/finite_elements.tex:236, 262`). A full `\includegraphics` inventory confirms no other figure exists. Yet the companion evidence file publishes nine finite-element figures (`site/evidence.json`, `figures` array): `fe-mandel-history`, `fe-mandel-profiles`, `fe-mandel-refinement`, `fe-mms-convergence`, `fe-load-limit`, `fe-map-anisotropic-30`, `fe-map-partial-0`, plus the two that do appear. Seven of the nine are therefore unreachable from the manuscript.

The consequence is concrete: the abstract asserts that the implementation "is verified against a manufactured solution for the constant reference tangent and, in the same limit, the constant-coefficient consolidation reference", and the conclusions quote spatial orders, a step-refinement ratio, and a load-limit error floor (`main.tex:552–562`) — none of which is shown in the paper. The prose in `sections/finite_elements.tex:137–160` also promises an error-measurement procedure ("We retain the maximum error over all positive output times and also compare profiles at common fixed positive times under separate spatial and temporal refinement") whose results appear nowhere in the manuscript. A reader of the article alone cannot assess the central numerical claim without leaving the paper for a repository path.

**Required action.** Add at least one convergence figure or table (manufactured-solution orders, and either the step-refinement or the load-limit floor) and one reference-comparison figure to the finite-element section, or, if figures cannot be added, cite the companion artifact identifiers explicitly at the point of each quantitative claim (e.g. "see artifact `mms-convergence`") so the claim is not left unanchored.

---

### R3-4 — The temporal-order range in the conclusions contradicts the companion evidence's own caveat

**Location:** `main.tex:561–562` ("the manufactured-solution temporal orders at \(nx=16/32/64\) are \(0.98\)--\(1.40\)"); companion: `site/evidence.json`, `categories.convergence.summary`.

**Evidence.** The companion states that these are "measured successive-difference orders … at fixed mesh", that they "include values above one (ux is about 1.4)", that they "are reported as measurements and no order above one is asserted", and that the departure from one is "a mesh-step cross term in the error balance". The manuscript reports the same numbers as "the manufactured-solution temporal orders", without the fixed-mesh/cross-term qualification and without the explicit refusal to assert an order above one. As written, the manuscript sentence invites the reader to conclude that the temporal scheme is better than first order, which the evidence file explicitly disclaims. The numeric values themselves are consistent (`1.397 → 1.40`; `0.978 → 0.98`); only the characterization differs.

**Required action.** Adopt the companion's wording, e.g. "the fixed-mesh successive-difference temporal orders at \(nx=16/32/64\) are \(0.98\)--\(1.40\), including values above one; these are measurements from a sequence that retains a mesh-step cross term, and no order above one is asserted."

---

### R3-5 — The paper's central novelty claim is stated as a literature fact without the qualification its own evidence file records

**Location:** `main.tex:131–141`, especially `main.tex:133–136`: "What they do not supply is a tensorial distention law, a constitutive relation stating how the shape and orientation of the pore space enter a finite-deformation poromechanical energy and the Biot tensor derived from it."

**Evidence.** This is the sentence that positions the paper against the pore-fabric and poroelasticity literature, and it is phrased as a fact about that literature. The repository's own supporting note, `references/notes/novelty-evidence.md`, records: "This is a targeted full-text support audit, not a complete priority search"; that Carroll (1979) is "candidate-unverified / not-verifiable" with only abstract-level access; and that the Foster–Xu full text was only inspected via a later author manuscript whose "title-page date is June 22, 2026" and which "is not asserted to be the 2025 publisher version of record". A scoped negative claim is defensible; an unqualified one is not supported by the recorded search.

**Required action.** Scope the sentence to the reviewer's own knowledge or to an explicitly bounded comparison set, e.g. "Among the fabric-elasticity and fabric-poroelasticity constructions surveyed here, we are not aware of a tensorial distention law that states how pore shape and orientation enter a finite-deformation poromechanical energy and the Biot tensor derived from it."

---

## 4. OPTIONAL notes

### O3-1 — The bar accent is formally declared to carry four meanings

`main.tex:209–216` defines a bar as: (a) mineral state (kinematic/energetic), (b) per-phase-volume intrinsic density, (c) mixture-frame stress representation, and (d) prescribed boundary datum (`\bar Q_f`, `sections/finite_elements.tex:109,115`). Each meaning is individually defined, so this is not a defect, but `\bar{\mathbf F}` (mineral deformation) and `\bar{\mathbf\sigma}_s` (mixture-frame stress) place the same accent on the same base letter for opposite reasons, and `\bar Q_f` imports the bar into a section that otherwise uses it for mineral state. Consider a compact notation table, or move the boundary-datum convention out of the bar and onto a distinct marker.

### O3-2 — Hat, bar, and tilde all describe mineral stresses

`sections/pore_fabric.tex:63–73` and `sections/pore_fabric.tex` `\eqref{eq:fabric-phase-work}` introduce `\widetilde{\mathbf\tau}=\mathbf R_A^T\mathbf\tau'\mathbf R_A` alongside `\bar{\mathbf\tau}_s` and `\widehat{\mathbf\tau}_s`. Three accents over the same base `\tau` in one section will be hard to track; one explicit sentence listing "true frame (hat), mixture frame (bar), intermediate frame rotated (tilde)" near the first use would help.

### O3-3 — "Full rank" and "zero eigenvalue" in the same sentence

`sections/pore_fabric.tex:258–266` states that a full-rank `\mathbb{D}` relaxes the restriction, then that the implemented five-modulus transversely isotropic `\mathbb{D}` "is full rank on the volumetric, axial, in-plane-deviatoric and the two shear directions it retains, but … leaves the in-plane shear `\operatorname{sym}(\mathbf p_1\otimes\mathbf p_2)` frozen … through the zero eigenvalue of the Moore–Penrose inverse". The qualified phrase "full rank on …" is technically consistent, but the sentence reads as self-contradictory. State the rank explicitly: "rank five on the six-dimensional symmetric space, with the in-plane shear mode left at the mineral compliance."

### O3-4 — Abstract claim about the relaxation is broader than the implemented case

`main.tex:58–63` says the tensorial distention "relaxes the rank-one drained-compliance restriction and yields an anisotropic Biot tensor driven by both mineral and pore-fabric anisotropy." Both clauses hold for a general `\mathbb{D}`; the only `\mathbb{D}` actually implemented and verified is rank-deficient on the in-plane shear mode (`sections/pore_fabric.tex:261–266`), and the demonstrated directional coupling specifically requires the volume–axial modulus (`sections/pore_fabric.tex:324–326`; `site/evidence.json`, last limitation). A half-sentence in the abstract noting that the demonstrated case uses a rank-five distention stiffness would remove the gap.

### O3-5 — Caption phrasing reads as residual review correspondence

`sections/finite_elements.tex:243–244`: "the plotted quantity is the paper's `\ln h`, not its negative." The negation is unexplained and references a convention the reader has not been offered a reason to doubt. Either drop the clause or state the convention positively once, at the definition of `h` (`sections/pore_fabric.tex:281–293`).

### O3-6 — Reaction significance is asserted for a model with no reaction

`main.tex:594–596`: "This is the mechanism by which a reaction-induced pore fabric enters the poromechanical response." The model is explicitly elastic and reaction-free (`sections/finite_elements.tex:6–7`); the reaction literature (`main.tex:120–129`) motivates the fabric but is never coupled. The claim is defensible as a conditional statement, but as written it reads as a result about reactive systems. Consider "would enter" or "this is the mechanism by which a reaction-induced pore fabric *would* enter the poromechanical response."

### O3-7 — Companion site is referenced by path only

`sections/experiments.tex:238–239` points the reader to `site/evidence.json` and to the GitHub URL, which satisfies the "linked" requirement in the manuscript sense. The companion site itself records no deployed URL (`site/evidence.json` `provenance` has only `source_revision` and a note), and `site/README.md` treats deployment as separately authorized. That is consistent, but a reader cannot reach the rendered site from the paper. If a rendered site exists at submission time, link it; otherwise the current path-based reference is the honest choice.

---

## 5. Notation audit summary (symbol by symbol)

Items flagged above are the ones with demonstrable ambiguity. The remainder were checked and found clean:

- `\mathbf A` (distention gradient), `a` (its determinant) vs. the fabric literature's fabric tensor: the manuscript deliberately uses `\mathbf H` for the fabric (`sections/pore_fabric.tex:90–95`), which avoids the collision with Cowin-style `A`-notation. Good.
- Fourth-order `\mathbb{}` vs. second-order upright bold: consistent throughout; `\mathbf C` (right Cauchy–Green) and `\mathbb{C}^d` (drained stiffness) are typographically distinct, but see R3-1 for the *d* collision.
- `\mathbf B` (Biot tensor) vs. `B_\parallel`, `B_\perp` (its components): consistent.
- `K`, `K_s`, `K_f`; `S_s` (scalar storage) vs. `\mathbf S_d`, `\bar{\mathbf S}_d` (distention stresses): distinct by font and role; no collision found.
- `G` (scalar drained shear modulus, `sections/finite_elements.tex:164`) vs. `\mathbf G` (distention right Cauchy–Green): italic vs. bold; low risk, no action needed.
- `h` (fabric shape parameter) is used with one meaning only (`sections/pore_fabric.tex:281–293`), and `\det\mathbf H=1` and the strain split `\mathbf E_d=\tfrac{\ln a}{3}\mathbf I+\ln h(\tfrac12\mathbf I-\tfrac32\mathbf m\otimes\mathbf m)` are algebraically correct (verified by hand).
- `\mathbf F`, `\bar{\mathbf F}`, `\bar J`, `\bar{\mathbf C}`, `\bar{\mathbf\varepsilon}`: internally consistent mineral-state notation.

---

## 6. Figure and caption audit

| Figure | Caption claim | Data check | Result |
| --- | --- | --- | --- |
| `fig:conformal-pressure` | "121 pressure states on \(0\le p/K_*\le6\)" | `build/conformal/pressure_response.csv`, 242 rows = 2 materials × 121 | match |
| `fig:conformal-shear` | "161 equally spaced values of \(\gamma\)" | `shear_response.csv`, 322 rows = 2 × 161 | match |
| `fig:conformal-directional` | "sampled at one-degree intervals" | `directional_response.csv`, 1083 rows = 3 states × 361 | match |
| `fig:conformal-rotation` | "121 angles span zero to \(180^\circ\)" | `rotation_response.csv`, 242 rows = 2 modes × 121 | match |
| `fig:conformal-layer` | "121 points on \(0\le p/K_*\le6\)" | `constrained_layer.csv`, 242 rows = 2 × 121 | match |
| `fig:fe-fabric-probe` | axial/transverse Biot, difference, `\ln h` | `figures/fe_fabric_probe.csv` matches plotted fields; `B_par = B_per = 0.88387` for the uncoupled probes (isotropic mineral), `0.85065 / 0.91027` for the coupled probes | match |
| `fig:fe-fabric-mandel` | peak centre pressures, uncoupled reference dashed | `figures/fe_fabric_mandel_peak.csv`: `6.2803e-5`, `5.1022e-5`, `3.9461e-5`, uncoupled `5.1326e-5` | match to quoted values |

Captions correctly identify which panels are demonstrations rather than verification. The one caption-language issue is O3-5.

**Missing displays:** see R3-3 — the finite-element verification (Mandel history/profiles/refinement, manufactured-solution convergence, load-limit floor, anisotropic and partial-drainage maps) is discussed in prose but never shown in the manuscript.

---

## 7. Companion-site and supplement consistency

- `site/evidence.json`: 32 artifacts, **all** SHA-256 digests match the files on disk; five required categories present; `physical_validation` correctly `not_performed`; six substantive limitations listed. Category statuses are consistent with the body text (analytical and implementation and convergence `passed`; `finite_deformation` `pending`; `physical_validation` `not_performed`).
- `site/scientific-snapshot.json`: 41 listed files, all hashes verified, none missing.
- Embedded supplement `build/anisotropic-biot-2026-09-20-v2.zip`: 58 entries; its `manifest.json` carries a `sha256` map whose payload digests all verify against the archive contents; its README's reproduction commands match `README.md` and `sections/experiments.tex:196–201`; it contains exactly the MOOSE files the manuscript claims (`moose_app/include/utils/FabricLaw.h`, `moose_app/include/materials/FabricMaterial.h`, `moose_app/src/materials/FabricMaterial.C`, `moose_app/inputs/{fabric_probe,conformal_probe,fabric_mandel}.i`) and does *not* claim to ship the rest of the FE application, which matches the manuscript's wording at `sections/experiments.tex:228–240`.
- `fe-evidence/runs/`: 53 case directories, every one complete (`input.i`, `provenance.json`, `analysis.json`, `run.log`, `solution.csv`), matching the manuscript's description at `sections/experiments.tex:234–236`.
- AI-use disclosure (`provenance/ai_use_statement.tex`) is present, specific, and consistent with the repository layout.

No integrity, linking, or consistency defect was found in the companion artifacts. The only companion-related problems are the *incompleteness of the in-manuscript display* (R3-3) and the *characterization mismatch* (R3-4).

---

## 8. Significance and honesty of stated restrictions

Positive findings, recorded because they bear on the verdict:

- The physical restrictions are stated honestly and repeatedly: elastic-only scope (`main.tex:145–147`), synthetic parameters and no calibration (`main.tex:611–616`), local-only stability (`sections/limits.tex:100–117`), admissible branch and positive phase volumes at negative pressure (`sections/experiments.tex:203–210`), and the explicit "no quantitative finite-deformation verification and no experimental validation are claimed" (`main.tex:52–54`).
- The model's own narrowness is disclosed rather than buried: "Mineral anisotropy alone need not give directional pressure coupling" and the cubic-symmetry vanishing case (`main.tex:481–484`); the conformal case giving an isotropic drained skeleton for an isotropic mineral (`main.tex:568–578`); the admission that the tensor-information re-implementation shares the section's conventions and is therefore an implementation check, not an independent derivation (`sections/finite_elements.tex:219–226`).
- The most significant interpretive claim not overreached: the paper does not present the fabric law as validated, and it separates the volume-only conformal result from the shape-changing extension (`main.tex:617–626`).

The residual significance concerns are R3-5 (unscoped priority claim) and O3-6 (reaction-language overreach), both addressable in a sentence each.

---

## 9. Verdict rationale

Integrity is exact (549/549). The derivation, the numbers, the figures, and the companion evidence are mutually consistent, and the limitations are stated with unusual care. The required items are (i) two real notation collisions, one of which co-occurs inside a single displayed equation, (ii) an advertised verification claim with no in-manuscript display, (iii) a characterization of temporal orders that contradicts the companion's own caveat, and (iv) an unscoped priority claim. None requires new derivation, computation, or rewriting of the science; all are correctable by notation edits, one added figure or table, and tightened sentences.

VERDICT: MINOR REVISION
