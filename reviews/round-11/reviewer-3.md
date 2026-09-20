# Round 11 — Independent Reviewer 3 (prose, notation, presentation, significance)

**Reviewed object:** immutable snapshot `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/review-snapshots/round-11`
**Snapshot ID (required):** `b9fadd66e96794417a4bed1f674064928716ffb3f2cc30d09edc0a663586fe6a`
**Manuscript:** *An anisotropic Biot tensor from mineral stress and distention work* (main.tex, 20-page build/main.pdf)
**Role:** independent Reviewer 3. I did not read any other reviewer report from this round, nor the `reviews/` directory, and I did not infer a desired outcome.

---

## 0. Integrity verification (MANDATORY FIRST STEP)

Command: `sha256sum source-manifest.json` in the snapshot root.

```
b9fadd66e96794417a4bed1f674064928716ffb3f2cc30d09edc0a663586fe6a  source-manifest.json
```

This **equals the required snapshot ID**. I then recomputed SHA-256 for every file listed in `source-manifest.json` (Python `hashlib`, relative paths resolved under the snapshot root):

```
total entries: 286
verified ok:   286
MISMATCHED:    0
MISSING:       0
```

**Result: integrity PASS.** No blocking integrity finding. The snapshot is internally consistent and matches its declared ID.

---

## 1. Scope of inspection

Read in full: `main.tex`; `sections/{stress_reconstruction,limits,experiments,finite_elements,logarithmic_derivative}.tex`; `references.bib`; `provenance/AI_USE.md`, `provenance/ai_use_statement.tex`, `provenance/ai-use.yml`; `fe-evidence/site-evidence.json`.

Rendered PDF (`build/main.pdf`, 20 pages, LuaTeX, 2026-09-20 15:13 CDT): I extracted the complete text layer with `pdftotext -layout` and read **every page**, including the text of all equations, figure captions, the Appendix A equations, the Acknowledgements, the AI declaration, and the reference list. Page map confirmed:

| Page(s) | Content |
|---|---|
| 1 | title, abstract, keywords, §1 Introduction start |
| 2 | §2 Deformation and volume-fraction-weighted stress |
| 3–4 | §3 Reversible work and the equivalent energy |
| 4–7 | §4 Logarithmic Hooke laws and the drained response |
| 7–8 | §5 Pressure coupling at finite deformation (Biot tensor, eqs. 36–39) |
| 8–9 | §6 Reference response and limiting cases |
| 10–13 | §7 Numerical examples and independent checks; **Figures 1–5**, eqs. 65–67 |
| 13–14 | §7.5 Independent verification; "Code and data availability" |
| **14–17** | **§8 Coupled deformation and fluid transport (new finite-element material), eqs. 68–82** |
| 17–18 | §9 Discussion and conclusions; Appendix A (eqs. 83–88) |
| 18 | Acknowledgements |
| 19 | Declaration of generative AI; references [1]–[10] |
| 20 | references [11]–[13] |

Programmatic checks performed: citation-key vs bib cross-check; unresolved-reference scan (`??` count = 0); equation-number cross-reference spot checks; figure-file hash verification; extraction and inspection of the embedded supplement `conformal-2026-09-20-v1.zip` via `pdfdetach`; review of `figures/fe_*.{png,csv}` and `fe-evidence/*.json`; and recomputation of several stated numbers (Section 4).

**Stated limitation of my inspection:** the model running this review cannot accept images, so I could **not** visually inspect rasterized PDF pages or the PNG figures. I compensated by reading the complete PDF text layer (all 20 pages), by `pdfimages`/`pdftoppm` rendering the relevant pages to confirm they exist and are populated, and by programmatic verification of the figure data files and evidence JSON. Any purely visual defect (e.g. illegible axes, overlapping curves) is outside what I can certify; everything I assert about the figures is text- or data-based.

---

## 2. What passes (checked, not accepted on assertion)

**P1. §8 does not claim quantitative finite-deformation verification.** `sections/finite_elements.tex` is a formulation/methods section (weak balances, fluid closure, plane strain, reference problems). Its only verification-adjacent statement is explicitly self-limiting, line 194:

> "This test exercises mixed derivatives and off-diagonal pressure coupling; **it does not by itself verify the nonlinear constitutive law.**"

No finite-deformation FE result, error table, or convergence figure appears in the manuscript. The section therefore does **not** imply quantitative finite-deformation verification. This specific check **passes**.

**P2. `force_relative ≈ 1.0` is correctly framed in the evidence.** The manuscript never mentions `force_relative`. The evidence file states it correctly (`fe-evidence/site-evidence.json`, `finite_deformation.summary`):

> "A force_relative value of approximately 1.0 reflects the kinematic platen constraint, not a force-balance failure."

I confirmed the underlying data: `fe-evidence/runs/anisotropic_30/analysis.json` gives `force_relative = 1.0000000000042857` with `platen_equality_absolute = 1.70e-15`; `partial_0` gives `force_relative = 1.0000000000035714` with `platen_equality_absolute = 3.10e-14`. The near-unity value is the platen-equality (kinematic) residual identity, exactly as labelled. **No mislabel in either the manuscript or the evidence.**

**P3. No experimental-validation overclaim in the manuscript.** §7 (experiments.tex line 35) states the calculations are "homogeneous constitutive calculations with synthetic parameters, rather than finite-element simulations or calibration to a measured material," and §9 (main.tex line 494) opens "The examples use synthetic elastic parameters." Nothing in the manuscript implies experimental validation. The evidence file's `physical_validation.status = "not_performed"` ("The parameters are synthetic. No comparison to laboratory or field measurements has been performed.") is consistent with the manuscript's stance.

**P4. Stated numbers that I independently recomputed agree.**
- Eq. (65) with diagonal 50/60/70: `K_s = (1/9) I:C_s:I = (72+86+94)/9 = 28` ✓ (manuscript: "K_s = 28K_*").
- Compliance restriction ⇒ `G = φ_s0 μ_s = 0.9 × 5/6 = 0.75` ✓ (§8.3 "drained shear modulus G = 0.75").
- Reference Biot `B0 = 1 − K/K_s = 1 − 1/2.5 = 0.6` ✓ (§8.3 "reference Biot coefficient is 0.6").
- Total storage `S_s + (1−φ_s0)/K_f = 0.9/2.5·(1−1/2.25) + 0.1/8 = 0.2 + 0.0125 = 17/80` ✓ (§8.3 "total storage is 17/80").
- `conformal/verification.json`: `checks_passed = 186`, `legacy_identities_rechecked = 67` ✓ (§7.5 "186 named checks, including the 67 checks").
- Max constitutive-identity error over all non-convergence checks = **2.455e-9** ✓ (§7.5 "largest absolute error among its constitutive identities is 2.5×10⁻⁹"; the larger 1.09e-2 entry is the `convergence/second_order_pressure` check, correctly excluded by the wording "constitutive identities").
- `tensor-verification.json`: 13 materials × 21 states = 273 ✓ (§7.5 "273 finite states across 13 mineral stiffnesses").
- All 13 citation keys used resolve in `references.bib`; unresolved-reference count in the PDF text is 0; reference list [1]–[13] on pp. 19–20 matches the bib entries.

These all check out. The manuscript is unusually careful about verification vs demonstration in §7 and §7.5, and its AI disclosure (below) is honest.

**P5. AI-use disclosure quality.** `provenance/AI_USE.md` and the rendered `provenance/ai_use_statement.tex` (PDF p. 19) state the tools, the scope of assistance, author responsibility, that AI output is not cited as a scholarly source, and — importantly — that "independent AI reviews ... do not constitute journal peer review or final author approval." The statement is generated from `ai-use.yml`, and the two artifacts agree verbatim with the yml `journal_statement`. This is a substantive, non-minimal disclosure. The `uses` list even includes "identifying candidate literature and bibliographic issues," which is consistent with §3 item M6 below (unused entries remain in the bib).

---

## 3. Findings

### BLOCKING
None. Integrity passes; no fabricated result, no false verification claim, no evidence/traceability failure detected.

### MAJOR
None. I looked specifically for a *systematic* pattern of overclaim or demonstration-as-verification and did not find one: §7 and §7.5 label their status explicitly and conservatively, and the abstract's "verify" language is bounded by the body (§7.5: "Numerical differentiation supports implementation verification, not experimental validation or a proof of global stability"). The defects below are localized and presentational rather than systemic, so I do not elevate them to MAJOR.

### MINOR

**M1 — The new §8 is absent from the abstract, the introduction roadmap, and the conclusions (framing/coherence).**
The paper's self-description stops at the constitutive result. Abstract (main.tex line 44):

> "Numerical experiments compare these responses under pressure, shear, and constrained extension."

and §1 roadmap (main.tex lines 96–97):

> "After deriving the compatible energy, we obtain the mineral-volume equation and the Biot tensor, examine their reference and isotropic limits, and verify the full phase stress balance numerically. No plastic deformation is considered."

Neither the abstract, the introduction, nor §9 (main.tex lines 460–509) mentions coupled deformation/fluid transport, the Darcy closure, the MOOSE implementation, or §8 at all, and the keyword list has no transport/flow term. A four-page section carrying sixteen numbered equations therefore appears with no announced role, no stated contribution, and no stated status. A reader cannot tell whether §8 is a formulation contribution, an implemented solver, or a work-in-progress. *Fix:* add one sentence to the abstract, one clause to the §1 roadmap, and one sentence to §9 stating what §8 contributes and its verification status.

**M2 — §8's scope/limitations do not agree with `fe-evidence/site-evidence.json`.**
The evidence file is explicit and cautious:

- `finite_deformation.status = "pending"`: "Rotated-anisotropy and partial-drainage cases have run and produced maps, but they are displacement-controlled demonstrations compared against the linear isotropic Mandel reference. Differences of 60-100 percent in pressure and displacement are expected and are presented as demonstrations, not error. ... **No finite-deformation quantitative verification claim is made.**"
- `physical_validation.status = "not_performed"`.
- `limitations` includes "Rotated-anisotropy and partial-drainage runs are displacement-controlled demonstrations, not verified quantitative predictions."

§8 contains none of this. Instead it uses the present tense of a completed study, e.g. (finite_elements.tex line 145) "The isotropic reference is Mandel consolidation between frictionless rigid plates. We evaluate the pressure and displacement series independently...", and (line 170):

> "We retain the maximum error over all positive output times and also compare profiles at common fixed positive times under separate spatial and temporal refinement."

and (line 155) "The compatible material inputs, in one consistent nondimensional system, are ...". No results follow, and no sentence says the finite-deformation runs are demonstrations or that quantitative FE verification is pending/not claimed. Because §8 sits immediately after §7 "Numerical examples and independent checks," a reader may reasonably conclude the coupled FE study *is* reported and verified here. This is a presentation mismatch with the paper's own evidence. Note the contrast in labeling discipline: §7 explicitly writes "rather than finite-element simulations" (experiments.tex line 35) and "Numerical differentiation supports implementation verification, not experimental validation" (lines 190–191); §8 has no corresponding qualifier. *Fix:* add an explicit status sentence to §8 (demonstrations; no quantitative finite-deformation verification claimed; parameters synthetic; physical validation not performed), mirroring `site-evidence.json`.

**M3 — The embedded reproducibility artifact excludes §8, and the "Code and data availability" statement does not say where the FE code/evidence live.**
I extracted the embedded attachment (`pdfdetach`) and inspected its `manifest.json` and `README.md`. The archive `conformal-2026-09-20-v1.zip` contains 34 files, all conformal/weighted-stress payloads — **no** FE/MOOSE sources, inputs, or evidence. Its README states:

> "The models are synthetic homogeneous constitutive calculations, not physical validation or finite-element simulations."

Yet the paper contains a finite-element section. The manuscript's own availability paragraph (experiments.tex lines 208–216) describes only the conformal supplement and concludes "This supplement is self-contained and does not require the companion repository." Nothing directs the reader to the MOOSE application or to `fe-evidence/` for §8. *Fix:* either include the FE material in the supplement or state in the availability paragraph where the §8 code and evidence are archived, and reconcile the supplement's "not ... finite-element simulations" wording with the presence of §8. Separately, the `conformal-2026-09-20-v1.zip` container itself is **not** in the snapshot manifest (the payloads are), so the embedded archive is not hash-pinned by `source-manifest.json`.

**M4 — Notation: the overbar is overloaded, and fourth-order tensor typography is inconsistent.**
*Overbar overload.* The overbar denotes "mineral/intrinsic" for density, deformation, energy, and strain: `\bar\rho_s` "solid intrinsic density" (main.tex line 138), `\bar J`, `\bar{\mathbf F}`, `\bar W_s`, `\bar{\mathbf C}`, `\bar{\mathbf U}`, `\bar{\mathbf\varepsilon}`. But for stress the overbar instead denotes the **mixture-frame representation**, paired against a hat for the true frame:

> (main.tex lines 152–157) "Let \(\widehat{\mathbf\sigma}_s\) denote the intrinsic mineral Cauchy stress in the frame reached by \(\bar{\mathbf F}\). Its representation in the mixture frame is \(\bar{\mathbf\sigma}_s=\mathbf R_A\widehat{\mathbf\sigma}_s\mathbf R_A^T\)."

So the mineral deformation `\bar{\mathbf F}` (overbar = mineral) pairs with the **hat** stress `\widehat{\mathbf\tau}_s`, while the **bar** stress `\bar{\mathbf\tau}_s` means something different (transported to the mixture frame). A reader tracking the accents can easily invert the two meanings. A short notation table (symbol, order, frame, normalization) would remove the ambiguity.

*Fourth-order typography.* Fourth-order tensors are blackboard bold (`\mathbb{C}_s`, `\mathbb{C}^d`), but two other fourth-order objects are not: the spherical tensor is written `\mathbf I\otimes\mathbf I` (stress_reconstruction.tex line 192) and the logarithmic derivative as `\partial\log\mathbf C/\partial\mathbf C`, both in the bold family used for second-order tensors. Since `\mathbf I\otimes\mathbf I` multiplies a fourth-order-inverse relation and acts on a symmetric second-order stress, reusing the bold-`I` family for the fourth-order object is a real, if small, inconsistency. *Fix:* adopt one typographic convention for fourth-order objects.

**M5 — Mass/volume normalizations are mixed between "current" and "reference" without a single statement of the convention.**
`\rho_s` is defined as "solid mass **per current mixture volume**" (main.tex line 138), and §5 likewise quotes pore-volume changes "per **current** mixture volume" (line 355) versus "per **reference** mixture volume" (line 361). But §8 defines `m_f` as "fluid mass **per reference mixture volume**" (finite_elements.tex line 26) and evaluates storage "per **reference** fluid density" (line 79). Both normalizations are internally correct, but the paper alternates between a current-volume solid mass measure and a reference-volume fluid mass measure across the two halves without consolidating the convention, and `m_f` is a mass while `\rho_s` is a density. *Fix:* one sentence in §8 (or a notation table entry) stating that solid densities are current-volume normalized and fluid storage is reference-volume normalized.

**M6 — Nine bibliography entries are never cited, and they are precisely the applied/experimental references; the significance for engineering practice is thin.**
`grep`-based cross-check: `references.bib` defines 22 keys, the manuscript cites 13. Never cited: `braun2020` (claystone VTI poroelasticity), `chaubazantsu2016` (hydraulic fracture in shale), `cheng1997` (anisotropic poroelastic coefficients), `flory1961`, `macminnetal2016` (large deformations of soft porous material), `makhnenkolabuz2016` (saturated rock deformation), `sviridov2017` (VTI shale experiment), `wong2017` (crack-induced anisotropy), `zhaoborja2020` (anisotropic elastoplastic porous media). That the entire applied/experimental set is uncited while remaining in the bib suggests an intended motivation/context paragraph that is missing. Correspondingly, the introduction and conclusion motivate the work only abstractly; §9's closest statement to engineering significance is a caveat (main.tex line 494: "Application to a material requires checking the measured stiffnesses against the assumed deformation mechanism and restricting strains to a range supported by data"). The significance for engineering practice is therefore not *unfairly* stated — but it is barely stated. *Fix:* either cite the applied references in a short motivation/context paragraph (introduction and/or §9) or remove them; and add a sentence naming the intended application domain.

### OPTIONAL

**O1.** Reference ordering anomaly: `[4]` is Dehghani & Zilian (2021) and `[5]` is Dehghani, Penta & Merodio (2019). `plainnat` sorts by author then year, which would place Penta (2019) before Zilian (2021); the printed order is reversed. This may be a `.bbl`/style artifact rather than an error. Worth verifying against the generated `.bbl` (which is not in the snapshot).

**O2.** §8.3 cites the Mandel series to "Walker et al. [12, appendix D]" (finite_elements.tex line 146). I could not verify offline that appendix D of Walker et al. (GJI 235:2442–2475, 2023) contains that series; a precise equation/table pointer would help.

**O3.** AI disclosure: the statement is appropriately detailed, but lists only vendor and model strings ("GPT-5.6 Terra", "GPT-6 Astra") with no provider-side tool identifiers, and `ai-use.yml` records `complete_prompt_history_available: false`. Consider adding the tooling/provenance identifiers a reader could cross-check.

**O4.** §8 uses two different material sets: the MMS rotates the stiffness of eq. (65) (which has `φ_s0=0.6, K_s=28K_*`), while the isotropic Mandel reference uses `φ_s0=0.9, K_s=2.5, K=1`. Both are stated, but a one-line remark that they are deliberately different would prevent confusion.

**O5.** §9 states unqualified (main.tex line 466) "Independent numerical differentiation **verifies** the phase stress, pressure derivative, and energy at finite anisotropic deformations." The body (§7.5) bounds this to implementation verification. Repeating the qualifier in the conclusion would be tighter.

**O6.** The abstract's verification sentence (main.tex lines 45–47) attributes "invariance under changes of the internal rotation" to the numerical checks; the invariance is also a derived analytical result (eq. 24). Minor, but the abstract could distinguish the two.

---

## 4. Independent recomputation performed

Beyond hash verification (§0), I independently recomputed: `K_s = 28K_*` from eq. (65); `G = 0.75` from the compliance restriction; reference Biot `= 0.6`; total storage `= 17/80 = 0.2125`; the conformal suite's 186 checks / 67 legacy checks and its maximum constitutive-identity error `2.455e-9` (vs the claimed `2.5e-9`); the tensor suite's 273 = 13 × 21 states; and the demonstration `force_relative` values (1.0000000000036–1.0 with platen residuals ~1e-15). I also verified the embedded supplement's payload hashes against its own `manifest.json` and confirmed the archive contains no FE payloads. All recomputations agreed with the manuscript or with the evidence files as described above.

---

## 5. Summary judgment

The manuscript is scientifically careful where it makes claims: §7/§7.5 explicitly bound numerical differentiation to implementation verification and disclaim experimental validation, the stated constitutive numbers are correct, the AI disclosure is substantive and honest, and the snapshot integrity is perfect. The specific hazards named in the charge are not realized: §8 does not claim quantitative finite-deformation verification, and `force_relative ≈ 1.0` is correctly labelled in the evidence as a kinematic platen constraint.

The problem is the opposite of overclaim: the new finite-element section is *unintegrated and unqualified*. It is invisible to the abstract, introduction, and conclusions (M1); it carries none of the "demonstration / pending / not validated" qualifications that the project's own `site-evidence.json` records (M2); it is unsupported by the embedded reproducibility artifact, which explicitly excludes finite-element simulations (M3); and its notation adds overbar/hat and fourth-order typography ambiguities (M4–M5). Combined with the uncited applied literature and thin engineering-significance framing (M6), these are real but localized presentation and scope defects. None are blocking, none are systemic, and none undermine a result the paper claims. They should, however, be fixed before submission.

**Verdict: MINOR REVISION**
