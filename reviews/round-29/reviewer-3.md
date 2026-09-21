# SIMULATED AI PEER REVIEW — Reviewer 3

**Emphasis:** exposition, notation and claims (not a journal decision).

**Snapshot reviewed (frozen, read-only):** `.agent-runtime/review-snapshots/round-29`
**Declared SNAPSHOT_ID:** `8aff33630cf27ac2727729471b38529c10f23edb1d6a5f90f2553c5b7f8726d7`

## Mandatory verification

1. **Manifest hash.** `sha256sum .agent-runtime/review-snapshots/round-29/source-manifest.json`
   = `8aff33630cf27ac2727729471b38529c10f23edb1d6a5f90f2553c5b7f8726d7`.
   This equals the declared SNAPSHOT_ID. **PASS.**
2. **Per-file hash re-check.** The snapshot was copied to `/tmp/r29-r3/snap` (no writes inside the
   snapshot). Every entry in `source-manifest.json` was re-hashed against the manifest:
   - total entries listed: **592**
   - entries checked (present and hashed): **592**
   - hash mismatches: **0**
   - missing files: **0**
   - files present but not listed: **2** (`SNAPSHOT_ID`, `source-manifest.json` — the manifest's
     own self-referential files, expected and benign)

   **Result: 592/592 verified, 0 mismatches, 0 missing. PASS.**

All findings below are made against the frozen snapshot only. I did not read `reviews/`, any other
reviewer's report, any prior-round verdict, or any other `round-*` snapshot, and I ran none of the
held numerical suites.

---

## REQUIRED CHANGES

### R3-C1 — Drained energy carries a subscript while the stated convention reserves a superscript for the drained state
**Location:** `main.tex` lines 221–222 (notation paragraph, §2); `sections/stress_reconstruction.tex`
lines 34, 45, 49, 201.
**Quoted text:** the convention reads "A superscript \(d\) denotes the drained skeleton, as in the
drained stiffness \(\mathbb{C}^d\)"; the drained energy is then written
"\(W_{\mathrm{dr}}=\frac12\mathbf\varepsilon:\mathbb{C}^d:\mathbf\varepsilon\)".
**Problem:** the drained *stiffness* uses superscript \(d\) (\(\mathbb{C}^d\)) while the drained
*energy* of the same construct uses subscript \(\mathrm{dr}\) (\(W_{\mathrm{dr}}\)), and a paragraph
above asserts "The two labels are kept distinct throughout." A reader who has internalized the
declared rule ("superscript \(d\) = drained") will parse \(W_{\mathrm{dr}}\) as a third, unrelated
label and may not connect it to \(\mathbb{C}^d\). The same section already uses \(\mathbb{C}^d\) and
\(W_{\mathrm{dr}}\) in adjacent equations, so the clash is visible on the page.
**Required:** either rename the drained energy consistently (e.g. \(W^d_{\mathrm{dr}}\to W^d\)) or
add an explicit exception sentence to the notation paragraph naming \(W_{\mathrm{dr}}\) as the drained
energy. Unify so that one drained token is used throughout.

### R3-C2 — Bar on the distention stress is described "in the intermediate frame", contradicting the declared bar convention
**Location:** `sections/pore_fabric.tex` lines 137–140; bar convention in `main.tex` lines 214–220.
**Quoted text:** "Its work conjugate is the symmetric distention stress per reference mixture volume
**in the intermediate frame**, \(\bar{\mathbf S}_{\mathrm{dis}}=2\pder{W_{\mathrm{dis}}}{\mathbf G}\)".
The convention paragraph states: "A bar on a stress denotes its representation in the **mixture
frame**, whereas a hat denotes the true frame."
**Problem:** the convention assigns exactly one frame meaning to a bar on a stress (mixture frame),
but \(\bar{\mathbf S}_{\mathrm{dis}}\) is defined as an intermediate-frame stress. The sentence also
introduces a further, unenumerated bar meaning — normalization "per reference mixture volume" — that
is not in the list of four bar meanings given in §2 (mineral state; intrinsic density; mixture-frame
stress; prescribed boundary datum). Because the paper leans on its notation convention as the main
disambiguator, an unflagged exception in the one variable that is *conjugate to the fabric* is a
genuine notation defect.
**Required:** either extend the stated bar convention to cover the intermediate-frame/reference-
volume normalization of \(\bar{\mathbf S}_{\mathrm{dis}}\), or relabel the quantity so its frame and
normalization follow the declared rule.

### R3-C3 — Abstract presents the fabric-driven Biot tensor without the fixed-orientation restriction the fabric model imposes
**Location:** `main.tex` abstract lines 33–34 and 55–66; `sections/pore_fabric.tex` §7.1
(the "This is a modeling choice …" paragraph).
**Quoted text:** the abstract states the conformal model distinguishes mineral deformation and pore
volume change "without fixing the orientation of the intermediate frame", and then that the fabric
extension "yields an anisotropic Biot tensor driven by both mineral and pore-fabric anisotropy".
The body states instead that "Throughout the remainder we express the fabric and the mineral
stiffness in a common material frame, which amounts to fixing \(\mathbf R_A=\mathbf I\) … This is a
modeling choice" and "The construction therefore carries no rotational fabric variable, it represents
no rotation of the pore fabric relative to the mineral matrix".
**Problem:** the "without fixing the orientation" property holds only for the volume-only conformal
specialization; the fabric model that delivers the headline anisotropic Biot tensor *fixes* the
fabric orientation as prescribed material data. The abstract juxtaposes the two in a way that lets a
reader attribute the frame-independence of the conformal model to the fabric result, hiding a real
limitation of the claimed anisotropic Biot tensor (no relative fabric–mineral rotation).
**Required:** state the fixed-orientation restriction in the abstract, in one clause, so the scope of
the fabric result matches the body.

### R3-C4 — Abstract's "independent re-implementation" omits the limitation the body states twice
**Location:** `main.tex` line 56 (abstract) and line 578 (conclusions); the body qualification is in
`sections/finite_elements.tex` lines 280–288.
**Quoted text:** abstract — "checked at the material point against an independent re-implementation
of the section equations"; body — "That agreement is an implementation check, not an independent
derivation: the verification script re-derives the section equations but shares their modelling
conventions with the compiled material"; and again "This is an implementation check: the script
shares the section's basis and reported-scalar sign conventions".
**Problem:** the body deliberately deems the "not an independent derivation / shares conventions"
caveat essential and repeats it; the abstract and the corresponding concluding sentence carry only
"independent re-implementation", which a reader of the abstract alone will read as independent
verification of the fabric law. This is the one place where a limitation that the body flags is
dropped from the abstract.
**Required:** add a short qualifier in the abstract and at `main.tex:578` (e.g. "which shares the
section's modelling conventions") or replace "independent" with "separate", so the abstract and body
agree on what was and was not independently established.

---

## OPTIONAL NOTES

### R3-C5 — Prime overload on the potentials \(W'\), \(W''\) is not signposted
**Location:** `main.tex` §5 (eqs. `eq:reduced-energy`, `eq:legendre-energy`) versus the effective-
stress primes \(P'\), \(\tau'\), \(\sigma'\) defined in §2–§3.
The notation paragraph disambiguates \(d\) vs \(\mathrm{dis}\) but never warns that a prime on a
*scalar potential* \(W'\), \(W''\) is a name, not a derivative, while the same prime on a stress
denotes the effective/fixed-mineral-state version. One clarifying clause would remove the
"is \(W'\) the derivative of \(W\)?" reading.

### R3-C6 — Same letter \(C\) for a second-order and fourth-order tensor, distinguished only by font
`\mathbf C = \mathbf F^T\mathbf F` (second-order) and \(\mathbb{C}_s,\ \mathbb{C}^d\) (fourth-order)
coexist throughout. The paper's own rule ("fourth-order tensors in blackboard bold, second-order in
upright bold") makes them technically distinct, but in dense expressions such as
`C:\mathbb{C}_s:\dev\mathbf\varepsilon` the distinction rests entirely on the typeface. Consider a
distinct base letter for one of them.

### R3-C7 — The bar accent carries four meanings in adjacent symbols
§2 enumerates four bar meanings, but they collide locally: \(\bar W_s\) (bar = mineral state) and
\(\bar{\mathbf\tau}_s\) (bar = mixture-frame representation) appear within a few lines of each other,
and \(\bar\rho_f\) (intrinsic density) sits beside \(\bar Q_f\) (prescribed boundary datum). The
enumeration is careful; a one-line reminder at the point of first collision would help the
non-initiated reader.

### R3-C8 — Compressed definition of the isotropic comparison modulus
`sections/experiments.tex` line 29: "Its mineral shear modulus is \(16.8K_*\), the mean of the five
deviatoric stiffness modes of \(\mathbb C_s\), divided by two." A reader without Mandel-basis
fluency cannot reproduce this. (The claim is correct — I confirmed the five deviatoric eigenvalues of
\(\mathbb C_s\) sum to \(168K_*\), mean \(33.6K_*\), half \(16.8K_*\).) Naming the five modes (two
deviatoric normal modes plus the three shear modes) and stating that the factor \(1/2\) converts a
Mandel eigenvalue to a shear modulus would make the comparison reproducible on its face.

### R3-C9 — Verification-suite names used without definition
`sections/experiments.tex` lines 190, 192: "The spherical-gauge suite" and "a reconstruction suite"
are named but not described. Since the surrounding paragraph enumerates check counts, one clause per
suite stating what it checks (and why "spherical-gauge") would let a reader map the counts to claims.

### R3-C10 — Outlier reported without comment
`sections/finite_elements.tex` line 334: the refined-mesh displacement-magnitude peaks are reported
as \(5.18\), \(5.14\), \(2.38\), and \(5.26\times10^{-5}\) for the isotropic, \(0^\circ\), \(45^\circ\),
and \(90^\circ\) cases. The \(45^\circ\) value is roughly half the others (confirmed in
`figures/fe_fabric_contours.csv`). Reported bare, a reader cannot tell whether this is a physical
consequence of the tensor coupling or a discretization artifact. One sentence of interpretation (or
an explicit "we do not interpret this") would prevent the reader from drawing an unintended
conclusion.

### R3-C11 — Circular phrasing for the shape scalar
`sections/finite_elements.tex` (pore-fabric demonstration) and `sections/pore_fabric.tex` §7.6 use
"the unimodular transverse fabric eigenvalue \(h=\mathrm{e}^{\ln h}\)". The identity is trivially
true and reads as circular; it would be clearer to say "\(h\) is the unimodular transverse
eigenvalue, so the reported scalar is \(\ln h\)".

### R3-C12 — Compressed step to the explicit Biot tensor
`main.tex` §5, from eq. `eq:mineral-fixed-pressure-derivative` to eq. `eq:anisotropic-biot-explicit`:
"Using its self-adjointness gives the explicit current Biot tensor". The elimination of
\(\partial\ln\bar J/\partial\mathbf F\) and insertion of the matrix-logarithm derivative is the
technical heart of the section; a single intermediate line (or a forward pointer with the one
substitution made explicit) would keep the non-initiated reader with the argument.

### R3-C13 — Presentation-level items
- **Figures 3–5:** legend and axis-label text is noticeably smaller than the caption text; consider a
  larger figure font (presentation only).
- **Bibliography underfull box:** `build/main.log:845` records a single `Underfull \hbox (badness
  1137)` in a bibliography entry ("Rock Mechanics and Rock Engineering, 54(1):377--396, 2021").
  Cosmetic.
- **Float pagination:** the closing figure pages carry several top-of-page floats with large
  inter-float white space; `[htbp]` or reordering the last two figures may tighten the end matter.
  (No overfull box is present anywhere: `build/main.log` records **0 overfull** boxes across the
  34-page build.)

### R3-C14 — Novelty claim could state its search scope
`main.tex` §1: "we are not aware of a tensorial distention law…". The claim is appropriately hedged,
but given that it is the paper's central novelty statement, naming the survey scope (fabric-elasticity
and fabric-poroelasticity literature) would make the negative claim auditable.

---

## Assessment of exposition, notation and claims quality

**Exposition.** The manuscript reads as a self-contained theoretical article and is unusually
well-structured for its density: the notation paragraph in §2 enumerates every accent and superscript,
each display is introduced by a purpose statement, and §7 is explicit about which assumptions are new
modeling choices rather than consequences of the conformal model. I found **no undefined symbol that
blocks comprehension** and no missing purpose statement before a display. The few exposition concerns
(R3-C5, R3-C8, R3-C9, R3-C12) are places where an expert reader must supply a convention that the text
leaves implicit; none prevents following the argument end to end.

**Notation.** No `\bm`/`\boldsymbol` appears; fourth-order tensors use blackboard bold and
second-order tensors/vectors use upright bold via `\mathbf` with `unimathsetup{mathbf=sym,
bold-style=upright}`; Greek and blackboard symbols render correctly in the PDF (embedded
Latin Modern Math; no missing-glyph warnings). The declared conventions are internally consistent
except for the two genuine exceptions in R3-C1 and R3-C2. The letter collision in R3-C6 and the bar
overload in R3-C7 are readability issues rather than errors.

**Claims.** Claim discipline is a strength. Novelty is hedged ("we are not aware"); the FE work is
scoped as verification of the *constant reference tangent* plus finite-load *demonstrations*, with the
nonlinear law explicitly **not** claimed as quantitatively verified and no experimental validation
claimed; the partial-drainage runs are excluded from the verification claims as not comparable to the
slender Mandel geometry; and the material-point cross-check is honestly labeled an implementation
check rather than an independent derivation, with the shared conventions named. I re-derived the
constitutive numbers independently and they agree with the text: reference Biot components
\(0.7000/0.7583/0.7917\) (isotropic \(0.75\)), the drained-compliance restriction giving \(G=0.75\),
storage \(17/80\) and Biot \(0.6\) in §9, the isotropic comparison modulus \(16.8K_*\), and the
verification tallies (\(186\) checks, \(67=65+2\) identities, \(273\) states, \(2.5\times10^{-9}\)
largest constitutive error, \(4.9\times10^{-15}\) worst re-implementation difference, the
\(3.2\times10^{-3}\) pressure floor, and the \(1.94\) step-refinement ratio). The only claim-level gaps
are the two abstract-vs-body scope omissions in R3-C3 and R3-C4.

**Drafting hygiene.** No drafting history, reviewer response, or note-to-author text appears in the
manuscript. The generative-AI declaration in `provenance/ai_use_statement.tex` is an appropriate
disclosure, not stray drafting material.

**Bottom line.** A rigorous, carefully hedged, notation-conscious manuscript. The required changes are
four small consistency/scope fixes in notation and in the abstract; none touches the derivations, the
numerics, or the FE evidence, all of which I checked and found sound.

VERDICT: MINOR REVISION
