# SIMULATED AI PEER REVIEW — Reviewer 3 (Exposition, Notation and Claims)

**This is a simulated AI peer review of a theoretical mechanics manuscript. It is not a journal submission and the verdict below is not a journal decision.**

- **Snapshot identifier (declared):** `ade4ec319cd757abad15546bd307efe2d9f85b2df21aa075bd74fb9ba4f0658b`
- **Snapshot reviewed:** `.agent-runtime/review-snapshots/round-30` (frozen snapshot only; all work done from a temporary copy in `/tmp`)
- **Manifest self-hash check:** `sha256sum .agent-runtime/review-snapshots/round-30/source-manifest.json` = `ade4ec319cd757abad15546bd307efe2d9f85b2df21aa075bd74fb9ba4f0658b` — **matches the declared SNAPSHOT_ID**.
- **Per-file hash re-check:** **592 entries checked; 592 match; 0 hash mismatches; 0 missing listed files.**
- **Present-but-unlisted files:** 2 — `SNAPSHOT_ID` and `source-manifest.json` (the snapshot's own self-referential metadata; expected, no action).
- **Independence:** No file under `reviews/` was opened (only directory entry names were listed). No other `review-snapshots/round-*` directory was read.

---

## REQUIRED CHANGES

### R3-C1 — Figures 6–11 are deferred past the References section (float deferral / orphaned figures)

**Location:** `sections/finite_elements.tex` lines 218, 237, 294, 340, 353, 367 —
`\begin{figure}[t]` for `fig:fe-verification`, `fig:fe-reference-comparison`,
`fig:fe-fabric-probe`, `fig:fe-fabric-mandel`, `fig:fe-fabric-contours`,
`fig:fe-fabric-diffusion`.

All six §9 floats are declared `[t]` and the section carries no `\clearpage` before
`\appendix` / the bibliography. As a result LaTeX defers them to the end of the
document. Measured page mapping from the rendered `build/main.pdf` (34 pages):

| caption | page | first reference in text |
|---|---|---|
| Figure 1–5 (`build/conformal/*.pdf`) | 16–19 | §8.1–§8.4 (pp. 15–19) — fine |
| Figure 6 `fig:fe-verification` | **31** | §9.3, p. 21 |
| Figure 7 `fig:fe-reference-comparison` | **32** | §9.3, p. 21 |
| Figure 8 `fig:fe-fabric-probe` | **32** | §9.4, p. 23 |
| Figure 9 `fig:fe-fabric-mandel` | **33** | §9.4, p. 23 |
| Figure 10 `fig:fe-fabric-contours` | **33** | §9.4, p. 24 |
| Figure 11 `fig:fe-fabric-diffusion` | **34** | §9.4, p. 24 |

The References run on pp. 28–30 and the CRediT statement on p. 27, so **all six
§9 figures appear after the reference list**, 7–10 pages from the text that
discusses them (e.g. the conclusion on p. 25 refers to "Figure 6" and "figure 7",
which are printed on pp. 31–32). Page 30 contains only references [35]–[36] and a
large blank area, and pp. 31–34 are float-only pages. This is a production/layout
defect, not a content defect: the evidence in the figures is present but the reader
cannot follow §9.3–§9.4 and the conclusion without leafing to the end.

**Requested change:** bound the float placement (e.g. a `\clearpage` before
`\appendix`/the bibliography, `[htbp]` or `[!t]`, or `\usepackage{placeins}` /
`\FloatBarrier` at the end of §9) so that Figures 6–11 land near §9.3–§9.4, and
eliminate the near-blank p. 30.

### R3-C2 — The bar convention in §2 is anchored to the conformal distention only, but §7 applies bars to the general distention

**Location:** `main.tex` lines 216–217, §2:

> "Throughout, a bar on a kinematic or energetic quantity denotes the mineral state reached by removing the distention in \eqref{eq:spherical-distention}."

`eq:spherical-distention` is the **conformal** specialization
`\mathbf A=a^{1/3}\mathbf R_A`. In §7 the distention is generalized to
`\mathbf A=\mathbf R_A\mathbf G^{1/2}` (`eq:fabric-distention-polar`,
`sections/pore_fabric.tex`), and the barred quantities are then defined by removing
the *general* distention, e.g. `\bar{\mathbf F}=\mathbf G^{-1/2}\mathbf R_A^T\mathbf F`
(`eq:fabric-multiplicative`) and
`\bar{\mathbf C}=\mathbf F^T\mathbf R_A\mathbf G^{-1}\mathbf R_A^T\mathbf F`
(`eq:fabric-mineral-metric`). Under the convention exactly as written, the barred
symbols of §7 are read against the wrong (volume-only) decomposition, so the
declared rule does not cover the majority of its later uses.

**Requested change:** state the bar rule against the general multiplicative
decomposition, with the conformal case noted as the specialization.

### R3-C3 — The bar-on-stress rule states only the frame change, not the differing normalizations of barred stresses

**Location:** `main.tex` lines 220–223:

> "A bar on a stress denotes its representation in the mixture frame, whereas a hat denotes the true frame; written on the distention stress \(\bar{\mathbf S}_{\mathrm{dis}}\) of \eqref{eq:fabric-distention-stress}, a bar instead denotes that stress in the intermediate frame, normalized per reference mixture volume."

The declared rule deals entirely with the *frame*. But across the barred stresses the
*normalization* also changes, and only the `\bar{\mathbf S}_{\mathrm{dis}}` case
flags it. Specifically, `\bar{\mathbf\sigma}_s` is per **current mineral volume**
("Both are stresses per current mineral volume", §2), whereas
`\bar{\mathbf\tau}_s=\bar J\bar{\mathbf\sigma}_s` (`eq:kirchhoff-volume-conventions`)
is per **reference mineral volume**, and `\bar{\mathbf S}_{\mathrm{dis}}` is per
**reference mixture volume**. A reader applying "a bar on a stress = mixture frame"
will mis-scale `\bar{\mathbf\tau}_s` and `\bar{\mathbf S}_{\mathrm{dis}}` relative to
`\bar{\mathbf\sigma}_s`.

**Requested change:** add the normalization of each barred stress to the notation
paragraph (current mineral volume for `\bar{\mathbf\sigma}_s`, reference mineral
volume for `\bar{\mathbf\tau}_s`, reference mixture volume for
`\bar{\mathbf S}_{\mathrm{dis}}`).

### R3-C4 — The `\mathbf e_1,\dots,\mathbf e_6` basis is declared orthonormal but is incompletely labelled and its axial-shear members are unnormalized

**Location:** `sections/pore_fabric.tex` lines 296–319, §7.5. Quoting the tail of the
passage:

> "…it annihilates the four complementary modes of this basis, the coupled in-plane pair \(\mathbf e_3=(\mathbf p_1\otimes\mathbf p_1-\mathbf p_2\otimes\mathbf p_2)/\sqrt2\) and \(\mathbf e_6=\sqrt2\operatorname{sym}(\mathbf p_1\otimes\mathbf p_2)\) together with the two axial-shear modes \(\operatorname{sym}(\mathbf m\otimes\mathbf p_1)\) and \(\operatorname{sym}(\mathbf m\otimes\mathbf p_2)\). The labels \(\mathbf e_1,\dots,\mathbf e_6\) denote this fabric-adapted orthonormal basis of symmetric tensors…"

Two defects:

1. **Labelling.** The sentence promises the labels `\mathbf e_1,\dots,\mathbf e_6`, but
   only `\mathbf e_1`, `\mathbf e_2`, `\mathbf e_3`, `\mathbf e_6` are given; the two
   axial-shear modes are never assigned `\mathbf e_4` and `\mathbf e_5`.
2. **Normalization.** `\mathbf e_1`, `\mathbf e_2`, `\mathbf e_3`, `\mathbf e_6` are
   each unit-norm as written (I verified
   `|\mathbf e_1|^2=|\mathbf e_2|^2=|\mathbf e_3|^2=|\mathbf e_6|^2=1` and mutual
   orthogonality), but the two axial-shear members are written *without* the
   `\sqrt2` that `\mathbf e_6` carries; as written
   `|\operatorname{sym}(\mathbf m\otimes\mathbf p_i)|^2=\tfrac12\ne1`. Under the declared
   "orthonormal basis" they must be `\sqrt2\operatorname{sym}(\mathbf m\otimes\mathbf p_i)`.

**Requested change:** label the axial-shear modes `\mathbf e_4`, `\mathbf e_5` and
include the `\sqrt2` normalization.

### R3-C5 — Misdirected cross-reference for the fabric minimization

**Location:** `sections/pore_fabric.tex` lines 273–275, §7.5:

> "The minimization in \eqref{eq:fabric-equivalent-energy} is therefore over \(\mathbf E_{\mathrm{dis}}\in\operatorname{range}\mathbb{D}\), not over all symmetric tensors…"

`eq:fabric-equivalent-energy` is the *definition of the energy*
`W_s(\mathbf F,\mathbf G)=W_{\mathrm{dis}}(\mathbf G)+\phi_{s0}\bar W_s(\bar{\mathbf F})`.
The minimization is prescribed by `eq:fabric-equilibrium` (the potential
`W_{\mathrm{dis}}+\phi_{s0}\bar W_s+\phi_{s0}p\bar J`, §7.4), which the same paragraph
correctly invokes two sentences later ("the stationary point of \eqref{eq:fabric-equilibrium}…").
As written, the reference points the reader at the wrong display.

**Requested change:** retarget the reference to `eq:fabric-equilibrium` (or rephrase as
"the potential of \eqref{eq:fabric-equilibrium}").

---

## OPTIONAL NOTES

### R3-C6 — Prime / double-prime conventions are absent from the notation paragraph

The notation paragraph (`main.tex` lines 216–236) collects the bar, hat, superscript
`d`, and subscript `dis` rules and explicitly guards `d` against distention, but never
defines the prime (and double-prime) accents, which carry distinct meanings:
`\mathbf\sigma'` is the single-prime effective stress (containing the full
pore-pressure term, §2), while `\mathbf\sigma''` is the fixed-pressure stress of §5
(`\mathbf\sigma=\mathbf\sigma''-p\mathbf B`). The superficially parallel `'`/`''`
pair denotes unrelated objects. Adding a one-line prime rule to the notation paragraph
would remove the ambiguity.

### R3-C7 — Duplicated caveat in §9.4, and "independent" used for a non-independent check

**Location:** `sections/finite_elements.tex` lines 274–289. The same limitation is
stated twice almost verbatim: "…the verification script re-derives the section
equations but shares their modelling conventions with the compiled material—the
distention basis, the equilibrium, and the reported sign convention for `\ln h`."
and again "…the script shares the section's basis and reported-scalar sign
conventions, so it verifies the compiled material against the equations rather than
re-deriving the conventions themselves." In the same passage the script is called "An
independent NumPy re-implementation" and "An independent script" while the text
simultaneously establishes that it is *not* independently derived. Retain one caveat
sentence, and reserve "independent" for the parts (energy/pressure differentiation)
that are genuinely independent.

### R3-C8 — Conclusion's temporal-order range reads stronger than "near one"

`sections/finite_elements.tex` line 205 states the successive-difference temporal
orders at `nx=16,32,64` "lie near one and include one above one", while the conclusion
(`main.tex` line 578) reports "are \(0.98\)--\(1.40\)". An upper value of 1.40 is not
comfortably "near one"; state the range in §9.3 as well so the characterisation is
consistent across abstract/body/conclusion. (The surrounding hedging — "no order above
one is asserted" — is otherwise well handled.)

### R3-C9 — Tautological restatement of the fabric scalar

**Location:** `sections/pore_fabric.tex` lines 353–355:

> "…the reported shape scalar is the logarithm of the unimodular transverse fabric eigenvalue \(h=\mathrm{e}^{\ln h}\), not a projection of it."

`h=\mathrm{e}^{\ln h}` is an identity and adds no information; it reads as an
unresolved draft artifact. State the intended claim directly (the reported scalar is
`\ln h` exactly, not a projection of it).

### R3-C10 — "distention" is used in §1 before it is defined in §2

`main.tex` §1: "allow the distention gradient to contain both a dilation and a proper
rotation. This conformal distention changes pore volume…". The symbol `\mathbf A` and
the term "distention" are only attached to the decomposition in §2
(`eq:true-mineral-jacobian`). A one-clause forward pointer in §1 (distention `\mathbf A`
with `J=a\bar J`) would let a non-initiated reader track the introduction.

### R3-C11 — Near-colliding glyph pairs

`\mathbb{C}` (fourth-order stiffness, 48 uses) versus `\mathbf{C}` (right
Cauchy–Green tensor) differ only by blackboard-bold vs bold and are visually close at
11 pt; likewise `\mathbb{D}` (distention stiffness, §7.5) sits next to the declared
statement "so \(d\) never means distention". Neither violates the declared typography
rule (fourth-order in blackboard bold, second-order in upright bold was checked and
holds throughout), but a reader-safety note or distinct symbol for the right
Cauchy–Green tensor would help.

### R3-C12 — The notation paragraph resolves its rules through far-forward equations

The §2 notation paragraph defines the conventions by pointing at
`eq:fabric-distention-stress` (§7.5), `eq:fe-fluid-residual` (§9.2),
`eq:drained-stiffness-restriction` (§4) and `eq:prescribed-logarithmic-energies` (§4).
The rules are correct, but the reader meets them 2–7 sections before the referenced
displays. Consider restating the two conventions that matter early (bar = mineral
state; `d` = drained) in words, leaving the cross-references as pointers.

### R3-C13 — Abstract antecedents

`main.tex` line 57: "a separate re-implementation of the section equations that shares
their modelling conventions" — the antecedent of "their" is the *equations*. Line 61:
"The construction isolates anisotropy inherited from the mineral." — "The construction"
is the conformal construction of §2–§6, which the preceding abstract sentences have not
yet named. Both are minor, but the abstract is otherwise scrupulous about scope and
should match that standard.

### R3-C14 — AI-use disclosure wording

`provenance/ai_use_statement.tex` states the author used several AI assistants, and
includes "simulated peer review" among the assisted activities. This is an appropriate
disclosure and is **not** a leaked reviewer response or drafting history — I confirmed
that no drafting history, reviewer response, or note-to-author text appears anywhere in
`main.tex`, `sections/*.tex`, or the appendix. I flag only the phrasing: naming
"simulated peer review" inside the manuscript may invite confusion with the journal
process; a neutral phrase such as "AI-assisted internal review" would read more safely.

---

## Assessment of exposition, notation and claims quality

**Exposition.** The manuscript is well organized for its intended audience: each major
equation is introduced by a stated purpose ("To separate mineral work from distention
work, vary…", "To exhibit the volume contribution, expand the mineral term…"), the
energy ↔ stress round-trip is explicitly re-derived as a check, and §7 is careful to
label which steps are *new modelling choices* rather than consequences of the conformal
model. Jargon is mostly standard for continuum poromechanics. The main exposition
weaknesses are the incompletely defined `\mathbf e_1,\dots,\mathbf e_6` basis
(R3-C4), the one wrong cross-reference (R3-C5), and the late formal introduction of
"distention" (R3-C10).

**Notation.** I audited every occurrence of the four declared conventions. The
superscript `d` is used exclusively for the drained skeleton (verified across
`limits.tex`, `pore_fabric.tex`, `stress_reconstruction.tex`), and the claim "so \(d\)
never means distention" holds. The subscript `dis` is used consistently for
`W_{\mathrm{dis}}`, `\mathbf E_{\mathrm{dis}}`, `\mathbf S_{\mathrm{dis}}`. The hat is
used only for true-frame stresses. The bar is the weak point: the declared bar rule is
anchored to the conformal distention and omits the normalization difference among
barred stresses (R3-C2, R3-C3). Fourth-order vs second-order typography is correct
throughout — every `\mathbb{C}`, `\mathbb{D}`, `\mathbb{D}^{+}` is fourth-order and all
second-order tensors are upright bold, consistent with
`\unimathsetup{bold-style=upright}`.

**Greek glyph rendering.** Clean. `build/main.log` contains **0** "Missing character"
warnings, the PDF has **0** unresolved references (`??`), and rendered inspection of
the notation, appendix, and figure pages shows correct `\phi, \sigma, \tau, \rho,
\varepsilon, \gamma, \theta, \pi, \mu, \Omega, \Gamma, \mathbb{C}, \mathbb{D}`
accents (no tofu, correctly placed bars/hats).

**Claim discipline.** Strong. Scope statements in the abstract are matched by the body:
the pore-fabric orientation restriction is stated in both ("with the pore-fabric
orientation prescribed as material data and no relative rotation of the fabric and the
mineral matrix represented", abstract, `main.tex` 68–69; §7.1); the material-point
cross-check is explicitly limited ("shares their modelling conventions", abstract,
`main.tex` 57; §9.4); the finite-load demonstrations are denied quantitative
verification and experimental validation in abstract, §9.4, and the conclusion; and the
temporal-order discussion itself refuses to assert an order above one. The novelty
claim is properly hedged ("we are not aware of a tensorial distention law…"). I
independently re-derived the reference coefficients quoted in §9.3 from the stated
parameters (`\phi_{s0}=0.9, K_s=2.5, \mu_s=5/6, K=1, K_f=8`): reference Biot `0.6`,
drained bulk `K_d=1`, drained shear `G=0.75`, and total storage `17/80 = 0.2125` all
reproduce exactly, and the isotropic reference relation `B_0=1-K/(\phi_{s0}K_s)=0.6`
agrees with `eq:reconstructed-isotropic-source-biot` at `p=0`. Claims about the
distention work-conjugate algebra (`eq:phase-work-substitution` →
`eq:distention-mineral-energy-work`, `eq:energy-returned-effective-stress`, and the
explicit `\mathbf B` of `eq:anisotropic-biot-explicit`) are internally consistent; I
did not execute the held numerical suites.

**Layout.** One underfull hbox only, in the bibliography (`main.log`, `main.bbl`
lines 33–40); no overfull boxes and no broken displays. The single serious layout
defect is the deferral of Figures 6–11 past the References (R3-C1).

**Summary.** The science-facing exposition, notation, and claim discipline are in good
shape; the required changes are presentation-level (float placement, two notation gaps,
one basis definition, one cross-reference). No unsupported novelty, generality,
verification, or validation claim was found.

VERDICT: MINOR REVISION
