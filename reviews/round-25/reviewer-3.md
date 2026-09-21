# Round 25 — Independent Review 3 (prose / notation / significance)

Snapshot: `.agent-runtime/review-snapshots/round-25`
Declared SNAPSHOT_ID: `5035dd198266c12544140e47381da3e9390c7d1e68c00a06009e85ba6052f9dd`
Scope read: `main.tex` and `sections/*.tex` (frozen snapshot only; report written to the
working tree, nothing else touched).

## 1. Snapshot integrity

| Check | Result |
|-------|--------|
| Declared SNAPSHOT_ID | `5035dd198266c12544140e47381da3e9390c7d1e68c00a06009e85ba6052f9dd` |
| Recomputed sha256(`source-manifest.json`) | `5035dd198266c12544140e47381da3e9390c7d1e68c00a06009e85ba6052f9dd` → **MATCH** |
| Manifest entries | 591 |
| Re-hashed OK | **591** |
| MISSING | **0** |
| MISMATCH | **0** |

Digest and payload both verify; no integrity item is raised. All findings below are
manuscript-content findings read from the frozen files.

## 2. Verification of the R24-3-1 repair (requested)

`ln h` is **not** described anywhere as an "eigenvalue ratio" (the string does not occur
in `main.tex` or `sections/*.tex`), and both repaired sites describe it consistently with
`eq:fabric-transverse-h`:

- `sections/pore_fabric.tex` (sec:fabric-transverse): "the reported shape scalar is the
  logarithm of the unimodular transverse fabric eigenvalue \(h=\mathrm{e}^{\ln h}\)."
- `sections/finite_elements.tex` (`fig:fe-fabric-probe` caption): "(c) The reported shape
  scalar \(\ln h\) ... is exactly the logarithm of the unimodular transverse fabric
  eigenvalue \(h=\mathrm{e}^{\ln h}\) of \eqref{eq:fabric-transverse-h}."

Both match `H = h^{-2}\,m\otimes m + h(I-m\otimes m)`, whose eigenvalues are
\((h^{-2},h,h)\): `ln h` is the log of the double transverse eigenvalue, not the log
eigenvalue ratio (-3 ln h). **The R24-3-1 defect is closed.** The residual imprecision in
the sentence immediately preceding the first site is item R3-2 below.

## 3. Findings

### R3-1 — `\mathbf m` is used before it is defined (REQUIRED)

In `sections/pore_fabric.tex`, `\mathbf m` first appears in **sec:fabric-biot**, at the
definition of the axial basis direction,
\(\mathbf e_2=\sqrt{3/2}\,(\mathbf m\otimes\mathbf m-\mathbf I/3)\) (line 282), and again in
the same subsection as "the plane normal to \(\mathbf m\)" (line 287) and "transversely
isotropic about \(\mathbf m\)" (line 288). The symbol is only introduced a subsection
later, in **sec:fabric-transverse** (line 308): "Let the fabric be transversely isotropic
about a unit material axis \(\mathbf m\)." Nothing earlier in `main.tex`, `limits.tex`,
`stress_reconstruction.tex`, or `experiments.tex` defines it. The reader therefore meets
the fabric axis symbol before it exists. Required correction: define \(\mathbf m\) as the
unit material fabric axis at its first use in sec:fabric-biot (or move the definition
forward).

### R3-2 — the "exponential" claim attached to `eq:fabric-transverse-strain` is off by a factor of two (REQUIRED)

`sections/pore_fabric.tex` (sec:fabric-transverse) states the distention logarithmic
strain
\(\mathbf E_{\mathrm{dis}}=\tfrac{\ln a}{3}\mathbf I+\ln h\,(\tfrac12\mathbf I-\tfrac32
\mathbf m\otimes\mathbf m)\) "whose exponential reconstructs \eqref{eq:fabric-transverse-h}
with unimodular eigenvalues \(h^{-2},h,h\)."

This contradicts the paper's own definition of the same symbol three subsections earlier
(sec:fabric-energy): \(\mathbf E_{\mathrm{dis}}=\ln\mathbf G^{1/2}=\tfrac12\ln\mathbf G\).
With that definition, \(\exp(\mathbf E_{\mathrm{dis}})=\mathbf G^{1/2}\) has eigenvalues
\(a^{1/3}(h^{-1},h^{1/2},h^{1/2})\), i.e. its unimodular part is \(\mathbf H^{1/2}\), not
\(\mathbf H\); the quoted eigenvalues \(h^{-2},h,h\) are those of \(\mathbf H\), which is
reached only by \(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G=a^{2/3}\mathbf H\). The
sentence is therefore not verifiable against `eq:fabric-transverse-h` as written (the
missing factor of two, and the removal of the \(a^{2/3}\) factor, must be supplied by the
reader). Required correction: write the relation as the exponential of *twice* the
distention logarithmic strain (equivalently \(\mathbf G=a^{2/3}\mathbf H\), with
\(\mathbf H\) the unimodular part), so that the quoted eigenvalues follow from the stated
operation.

### R3-3 — dangling qualifier "not a projection of it" (OPTIONAL)

`sections/pore_fabric.tex`: "the reported shape scalar is the logarithm of the unimodular
transverse fabric eigenvalue \(h=\mathrm{e}^{\ln h}\), **not a projection of it**." The
antecedent of "it" is unrecoverable (the eigenvalue, or the shape scalar?), and nothing in
the section is described as a projection. The clause carries no content and invites the
question it is trying to close; deleting it (or naming what is *not* being claimed) would
be clearer. The substantive claim is correct and remains reconcilable, so this is not
treated as required.

### R3-4 — the asserted six-element basis \(\mathbf e_1,\dots,\mathbf e_6\) lists only four members (OPTIONAL)

`sections/pore_fabric.tex` (sec:fabric-biot) defines
\(\mathbf e_1=\mathbf I/\sqrt3\), \(\mathbf e_2=\sqrt{3/2}(\mathbf m\otimes\mathbf m-\mathbf I/3)\),
\(\mathbf e_3=(\mathbf p_1\otimes\mathbf p_1-\mathbf p_2\otimes\mathbf p_2)/\sqrt2\), and
\(\mathbf e_6=\sqrt2\operatorname{sym}(\mathbf p_1\otimes\mathbf p_2)\), then calls
"\(\mathbf e_1,\dots,\mathbf e_6\) ... this fabric-adapted orthonormal basis". Members
\(\mathbf e_4,\mathbf e_5\) are never written down. All *used* directions are defined, so
nothing is undefined at use; but the label range promises six and delivers four, and the
numbering (skipping to 6 while explicitly disclaiming the Mandel indices of
`eq:example-mineral-stiffness`) is apt to be misread. Recommend enumerating the full basis
or narrowing the label range.

### R3-5 — `G` carries two meanings in different sections (OPTIONAL)

\(\mathbf G\) is the distention right Cauchy–Green tensor throughout sec:pore-fabric,
while \(G\) is the drained shear modulus in `sections/finite_elements.tex`
(sec:fe-reference-problems: "The compliance restriction gives drained shear modulus
\(G=0.75\)"). The paper's convention statement distinguishes blackboard-bold fourth-order
tensors and upright-bold second-order tensors, so the two are typographically separable,
but the same letter is doing constitutive-tensor work in one section and moduli work in
another. Worth a name change (e.g. \(\mu^d\)) or an explicit note.

### R3-6 — `k` carries two meanings (OPTIONAL)

\(k\) is the isotropic current-configuration permeability in
`sections/finite_elements.tex` (sec:fe-fluid-closure), while \((k_v,k_a,k_c)\) are the
volumetric–axial distention stiffness moduli in `sections/pore_fabric.tex`
(sec:fabric-biot). Subscripts separate them, and the settings are different sections, but
"\(k\)" now denotes both a hydraulic coefficient and a stiffness block; a distinct symbol
for the fabric moduli would remove the ambiguity.

### R3-7 — the implementation-check caveat is stated twice in the same paragraph (OPTIONAL)

`sections/finite_elements.tex` (sec:fe-fabric) says "That agreement is an implementation
check, not an independent derivation: `examples/verify_fabric.py` ... shares their
modelling conventions with the compiled material---the distention basis, the equilibrium,
and the reported sign convention for \(\ln h\)." and then, after the volume-only-limit
sentence, "This is an implementation check: the script shares the section's basis and
reported-scalar sign conventions, so it verifies the compiled material against the
equations rather than re-deriving the conventions themselves." The two sentences make the
same point (shared basis/conventions), with the volume-only result sandwiched between
them. Merging them would tighten the paragraph without losing content.

### R3-8 — "independent ... re-implementation" versus "not an independent derivation" (OPTIONAL)

The same material is called "An independent NumPy re-implementation of the section
equations" and, one sentence later, "not an independent derivation" (also in the abstract:
"checked at the material point against an independent re-implementation"). The two senses
of "independent" (separate codebase vs. independent model derivation) are distinguishable,
but the adjacent uses read as self-contradictory on first pass. Suggest reserving
"independent" for the codebase and saying "a re-implementation that shares the section's
conventions" for the caveat.

### R3-9 — "eleven ... snapshots" vs "six recorded times" (OPTIONAL)

`sections/finite_elements.tex` (sec:fe-fabric) says the refined run records "eleven evenly
spaced field snapshots across the run", while the `fig:fe-fabric-diffusion` caption shows
"pore-pressure snapshots at six recorded times". These are consistent if the figure
selects six of the eleven, but the text does not say so, and the two counts sit close
together. One clause ("the figure shows six of the eleven") would pre-empt the question.

### Non-issues checked and cleared

- "transversely isotropic" is used consistently; no "transverse-isotropic" remains
  (`main.tex` conclusions included).
- The \(d\) (drained) / \(\mathrm{dis}\) (distention) distinction is stated explicitly in
  `main.tex` and honoured throughout; \(d\) is never used for distention.
- \(\mathbf p_1,\mathbf p_2\) (plane vectors) do not collide with the scalar pressure
  \(p\) or the first Piola stress \(\mathbf P\); \(\mathbf t_0\) (traction) does not
  collide with the time variable \(t\); \(\mathbf H\), \(h\), \(a\), \(\mathbf G\),
  \(\mathbb D\), \(\mathbb D^{+}\) are all defined at first use within their own sections.
- Quoted reference-state numbers are internally consistent (isotropic
  \(B_0=1-K/K_s=0.6\), total storage \((1-\phi_{s0})/K_f+S_s=17/80\), drained shear
  \(G=\phi_{s0}\mu_s=0.75\), \(5\times13=65\) per-state checks).
- Significance is honestly framed: the introduction's novelty paragraph ("we are not aware
  of a tensorial distention law ...") is properly hedged, the route is explicitly
  differentiated from the fabric-elasticity/fabric-poroelasticity constructions, and the
  abstract and conclusions both state the fabric extension as a modelling choice rather
  than a verified physical law. No claim is stated more strongly than its evidence.

## 4. Overall assessment

The snapshot is intact (591/591 files re-hash; digest matches), and the specific
R24-3-1 repair is genuinely closed: `ln h` is nowhere called an eigenvalue ratio, and both
`pore_fabric.tex` and the `fig:fe-fabric-probe` caption tie it consistently to the
transverse eigenvalue of `eq:fabric-transverse-h`. Two required items remain, both in the
new fabric material: the fabric-axis symbol \(\mathbf m\) is used in sec:fabric-biot before
it is defined in sec:fabric-transverse (R3-1), and the sentence linking
`eq:fabric-transverse-strain` to `eq:fabric-transverse-h` names the exponential of
\(\mathbf E_{\mathrm{dis}}\) where only the exponential of \(2\mathbf E_{\mathrm{dis}}\)
reproduces the stated eigenvalues (R3-2). Both are wording/definition defects with
one-line fixes; neither disturbs a displayed equation, a quoted number, a label, or a
citation. The remaining items are optional prose polish. The contribution is clearly and
honestly stated throughout, so these are presentation-level corrections rather than
scientific ones.

VERDICT: MINOR REVISION
