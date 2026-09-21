# Round 27 — Reviewer 3 (prose / notation / significance)

Independent review of the frozen round-27 snapshot
`.agent-runtime/review-snapshots/round-27`, declared
`SNAPSHOT_ID = c5050c77dd04628f149ddc417cce99eb6b53c4315884974efc6331c3267eda5e`.
Read as a referee. I did not read reviewer-1.md, reviewer-2.md, or any pre-round-27
report. I did not modify the snapshot or the working tree; the only file I wrote is
this report.

---

## 1. Snapshot integrity (mandatory first step)

| Check | Result |
|---|---|
| Declared `SNAPSHOT_ID` | `c5050c77dd04628f149ddc417cce99eb6b53c4315884974efc6331c3267eda5e` |
| Re-computed `sha256(.agent-runtime/review-snapshots/round-27/source-manifest.json)` | `c5050c77dd04628f149ddc417cce99eb6b53c4315884974efc6331c3267eda5e` |
| Manifest ID vs declared ID | **MATCH** |
| Manifest entries | 591 |
| Re-hashed entries OK | **591** |
| MISSING | **0** |
| MISMATCH | **0** |

Every manifest entry was re-hashed from bytes on disk; the declared SNAPSHOT_ID
equals the recomputed manifest digest; no file is missing and none mismatches.
**No integrity defect.**

Supplementary registration checks on the companion site recorded in the snapshot
(the F1 subject), all reproduced from the frozen bytes:

* `site/evidence.json` — 41 artifacts / 13 figures / 5 cases (matches the launch
  state); every artifact `path`→`sha256` pair resolves (41/41 OK); all 13 figures
  reference a registered artifact id (0 dangling); the four fabric figure artifacts
  (`fe-fabric-probe`, `fe-fabric-mandel`, `fe-fabric-contours`, `fe-fabric-diffusion`)
  and `site/reports/fabric-verification.json` are registered.
* `site/scientific-snapshot.json` — 47 files, all 47 digests resolve
  (0 missing, 0 mismatch).
* `"eigenvalue ratio"` occurs **0** times in the manuscript sources, in the
  round-27 snapshot, and in the currently built site output. (The phrase survives
  only in stale `.agent-runtime/site.previous-*` builds, old review snapshots, and
  goal checkpoint records, none of which are the frozen snapshot.)

---

## 2. Findings

Each finding is marked REQUIRED or OPTIONAL. "REQUIRED" is reserved for a place
where a reader cannot reconcile the text with the paper's own equations or
evidence. Style preferences are OPTIONAL.

### REQUIRED

**None.** I found no statement, symbol, or claim in the manuscript that
contradicts the paper's own equations or its recorded evidence in the areas under
my emphasis (prose, notation, significance).

### Targeted checks requested for this round (all pass)

**F3-1. `ln h` is not described as an eigenvalue ratio — PASS.**
The string "eigenvalue ratio" does not occur in any manuscript source, and no
sentence anywhere in `main.tex` or `sections/*.tex` calls `ln h` a ratio. The two
places where the shape scalar is characterised say, correctly, that it is the
logarithm of the unimodular **transverse** eigenvalue:
`sections/pore_fabric.tex` (§fabric-transverse) — "the reported shape scalar is the
logarithm of the unimodular transverse fabric eigenvalue \(h=\mathrm{e}^{\ln h}\),
not a projection of it"; and the `fig:fe-fabric-probe` caption in
`sections/finite_elements.tex`. This is consistent with
\eqref{eq:fabric-transverse-h}, whose unimodular eigenvalues are \(h^{-2},h,h\)
(log eigenvalue ratio \(=-3\ln h\), of which \(\ln h\) is one third and
\(-2\ln h\) for the axial eigenvalue).

**F3-2. Distention-strain sentence is correct — PASS.**
`sections/pore_fabric.tex` writes \(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G
=a^{2/3}\mathbf H\) and reconstructs \eqref{eq:fabric-transverse-h}; it does not
claim a bare exponential. I verified the identity directly:
\(2\mathbf E_{\mathrm{dis}}=\tfrac{2}{3}\ln a\,\mathbf I+\ln h(\mathbf I-3\mathbf
m\otimes\mathbf m)\), so \(\exp(2\mathbf E_{\mathrm{dis}})=a^{2/3}[h^{-2}\mathbf
m\otimes\mathbf m+h(\mathbf I-\mathbf m\otimes\mathbf m)]=a^{2/3}\mathbf H=\mathbf G\).
The stored `H_eigenvalues`/`H_eigenvalue_ratio_expected`
(`[0.9992864, 1.0003570, 1.0003570]`) match \(h^{-2},h,h\) for
\(\ln h=0.00035695\). Consistent.

**F3-3. Distention / compliance algebra is mutually consistent — PASS.**
I re-derived the reduction claimed in §fabric-biot ("in the conformal case
\(\mathbb D\propto\mathbf I\otimes\mathbf I\) is rank one and
\eqref{eq:fabric-compliance-restriction} reduces to
\eqref{eq:drained-compliance-restriction}") using the paper's own conventions and
found it correct, including the factor in \(D^{+}\). With the recalled FE numbers
(\(\phi_{s0}=0.9,K_s=2.5,\mu_s=5/6,K=1\)) the energy
\(W_A=\tfrac{K}{2(1-K/(\phi_{s0}K_s))}(\ln a)^2\) fixes the volumetric component
\(k_v=3K/(1-K/(\phi_{s0}K_s))=5.4\) in the normalised basis
\(\mathbf e_1=\mathbf I/\sqrt3\), and the resulting
\(D^{+}=\big((1-K/(\phi_{s0}K_s))/(9K)\big)\mathbf I\otimes\mathbf I=0.061728\,
\mathbf I\otimes\mathbf I\) equals the independently constructed
\((\mathbb C^d)^{-1}-(\phi_{s0}\mathbb C_s)^{-1}\). So neither the distention
energy nor the compliance restriction carries a normalisation error, and the
reduction is exact rather than approximate.

### OPTIONAL (no reconciliation failure; recorded for an editorial pass)

**F3-4 (OPTIONAL). One symbol, two roles: `G`.** The distention tensor
\(\mathbf G\) is central throughout §fabric-* (~30 uses). In
`sections/finite_elements.tex` (line 164) the *scalar* \(G\) denotes the drained
shear modulus: "The compliance restriction gives drained shear modulus
\(G=0.75\)." The value is correct (I reproduced \(G=0.75\), \(B_0=0.6\), total
storage \(17/80\) from \(\phi_{s0}=0.9,K_s=2.5,\mu_s=5/6,K=1,K_f=8\)), and bold vs
upright distinguishes the two, but the paper elsewhere uses \(\mu_s\) for shear
moduli, so using \(G\) here re-uses the fabric symbol for a different quantity. A
reader can reconcile this from the equations; a one-word rename (e.g. \(G_d\) or
\(\mu^d\)) would remove the collision.

**F3-5 (OPTIONAL). Three distinct meanings of the overbar.** The notation
paragraph in `main.tex` (§kinematics) deliberately defines three: bar on a
kinematic/energetic quantity = mineral state, bar on a stress = mixture-frame
representation, bar on an intrinsic density = per-phase-volume value, and bar on a
prescribed boundary datum = the prescribed value. The last two co-occur in
`sections/finite_elements.tex`, where \(\bar\rho_f\) is an intrinsic density while
\(\bar Q_f\) is a prescribed boundary flux (and \(\mathbf Q_f\), no bar, is the
referential mass flux). All are stated, so this is an overloading burden rather
than an ambiguity; it is the price of the otherwise disciplined scheme.

**F3-6 (OPTIONAL). Lower-case `k` for both permeability and distention stiffness.**
\(k\) is the isotropic permeability in §fe-fluid-closure; \(k_v,k_a,k_c\) are the
volumetric–axial distention stiffness block in §fabric-biot. Different sections
and subscripts keep them apart, but the shared letter is avoidable.

**F3-7 (OPTIONAL). Duplicated caveat within three sentences.**
`sections/finite_elements.tex` (§fe-fabric) states the same limitation twice: "That
agreement is an implementation check, not an independent derivation: … shares
their modelling conventions … the distention basis, the equilibrium, and the
reported sign convention for \(\ln h\)." then, after the volume-only-limit
sentence, "This is an implementation check: the script shares the section's basis
and reported-scalar sign conventions, so it verifies the compiled material against
the equations rather than re-deriving the conventions themselves." The second restates
the first. Separately, the clause "not a mesh-convergence study"/"no
mesh-convergence claim" appears in all three fabric captions
(`fig:fe-fabric-mandel`, `fig:fe-fabric-contours`, `fig:fe-fabric-diffusion`) plus
the prose. Consolidating to one statement per idea would tighten the section
without changing any claim.

**F3-8 (OPTIONAL). Bold \(p\) vs pressure \(p\) vs first Piola \(\mathbf P\).**
§fabric-biot introduces orthonormal in-plane vectors \(\mathbf p_1,\mathbf p_2\);
the same letter family carries scalar pressure \(p\) and first Piola
\(\mathbf P'/\mathbf P''/\mathbf P\). Case and subscripts distinguish them and the
\(\mathbf p_i\) are used only locally, so this is cosmetic.

**F3-9 (OPTIONAL). "Independent re-implementation" in the abstract.** The abstract
says the tensorial law is "checked at the material point against an independent
re-implementation of the section equations." The body correctly qualifies that the
script "shares their modelling conventions with the compiled material", i.e. it is
an independent implementation but not an independent derivation. The body
qualification governs, so the abstract is not misleading; optional sharpening only.

---

## 3. Assessment

**Notation.** The fabric/distention symbol family the round asked about is
defined before use and single-valued in meaning: \(\mathbf m\) (unit material
fabric axis), \(\mathbf H\) eq. \eqref{eq:fabric-tensor}, \(h\)
eq. \eqref{eq:fabric-transverse-h}, \(a\) eq. \eqref{eq:true-mineral-jacobian},
\(\mathbf G\) eq. \eqref{eq:fabric-distention-polar}, \(\mathbb D\) and
\(\mathbb D^{+}\) §fabric-biot, the \(\mathbf e_1,\dots,\mathbf e_6\) fabric basis
explicitly disambiguated from the Mandel indices of
\eqref{eq:example-mineral-stiffness}, \(\mathbf t_0\) defined in
\eqref{eq:fe-momentum-residual}, and \(d\) (drained) vs \(\mathrm{dis}\)
(distention) explicitly separated in the `main.tex` notation paragraph
("\(d\) never means distention"). I found no symbol used before definition in a
way that blocks reconciliation, and no two-meaning collision that contradicts an
equation. The residual collisions (F3-4 to F3-8) are overloading, not error.

**Prose/precision.** The two items the round flagged are both clean, and I
verified F3-3 by independent algebra rather than by reading the text
sympathetically. Terminology is consistent: "distention" throughout (109 uses, no
"distension"); "transversely isotropic" throughout (5 uses, including the
conclusion) with the heading "Transverse isotropy of the pore fabric" — no
adjective/noun drift. No statement is stronger than its evidence: the finite-load
runs are labelled demonstrations in the abstract, the body, the captions, and the
scope paragraph; the temporal-order values above one are reported as measurements
with an explicit "no order above one is asserted"; the FE numbers I spot-checked
against the frozen artifacts all reproduce (fabric reconstruction
\(2.2\times10^{-16}\), \(\det\mathbf H-1=-3.3\times10^{-16}\),
\(\lVert\mathbb D:\mathbf e_3\rVert=1.6\times10^{-16}\),
\(\mathbb D:\mathbf e_6=0\), rotation invariance \(2.5\times10^{-16}\),
worst probe difference \(4.9\times10^{-15}\); peak centre pressures
\(4.36/4.99/5.52/3.62\times10^{-5}\) and refined
\(3.61/4.35/4.97/5.50\times10^{-5}\) with displacement peaks
\(5.18/5.14/2.38/5.26\times10^{-5}\); MMS spatial orders
\(2.00,2.00/2.99,2.96/3.00,2.96\); temporal orders \(0.98\)–\(1.40\); step-refinement
errors \(3.7\times10^{-3}\), \(7.1\times10^{-3}\), ratio \(1.94\)). The only prose
defects are local redundancy (F3-7).

**Significance.** The contribution is stated plainly and consistently in the
abstract, the introduction, and the conclusions: a finite-deformation anisotropic
Biot tensor obtained by (i) separating mineral deformation from distention,
(ii) deriving — not postulating — the drained-compliance restriction, and
(iii) extending the scalar dilation to a symmetric positive-definite distention
whose unimodular part is the pore fabric, which relaxes the rank-one restriction
to a fabric-symmetric compliance and yields a fabric-driven directional Biot
tensor. It is differentiated from prior work at the point of use: Cowin,
Turner–Cowin and Moesen–Cardoso–Cowin assign fabric-dependent coefficients to the
solid at small strain, whereas here the fabric enters the distention energy; Gajo
and the companion manuscript are identified as the isotropic volumetric limit, and
the Drumheller §8.9 similarity argument is used to explain, rather than assert, why
the conformal restriction is a constitutive specialization. The novelty claim is
scoped ("Among the fabric-elasticity and fabric-poroelasticity constructions
surveyed here, we are not aware of…") and the boundary of the claim (retained
volumetric–axial subspace; shape-changing distention otherwise a separate
mechanism) is stated in the abstract itself.

**Overall.** Integrity re-hashes clean (591/591). The round's three prose/notation
questions resolve in the paper's favour, and the one place where I expected a
hidden normalisation error (the conformal reduction of the fabric compliance) is
exactly consistent under the paper's own conventions. All findings are OPTIONAL
wording/overloading observations. Nothing in the manuscript, read against its own
equations and against the frozen artifacts, requires correction under my emphasis.

---

VERDICT: ACCEPT
