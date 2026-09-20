# Engineering-reviewer memo — Foster editorial cycle 1 of 3

**Manuscript:** *An anisotropic Biot tensor from mineral stress and distention work*
**Reviewed snapshot:** `c621378778d49f8875679440cf874a74aef3caa5d9b04b8936ad319fb57f885f`
(working tree matched the frozen snapshot byte-for-byte before this cycle's prose edits:
`main.tex` `d1c6056649ef…`, `sections/experiments.tex` `0932fb1012f5…`,
`finite_elements.tex` `94a92ef0e31d…`, `limits.tex` `d29e67fbea2f…`,
`logarithmic_derivative.tex` `f799ae9ee2df…`, `stress_reconstruction.tex` `1af18fc1744a…`).
**Scope:** authorial/editorial quality only. No mathematical claim, equation, number,
label, citation, or assumption is in scope for change. Line numbers below are those of the
reviewed snapshot.

**Read-only triage.** `python3 .agent/shared/tools/review_scan.py` on `main.tex` and each
`sections/*.tex` returned zero editorial findings. Its single flag,
`sections/logarithmic_derivative.tex:35` (`unnumbered-display`), is a false positive: the
excerpt is the `\\[5pt]` row-spacing token inside the `cases` environment of
`eq:log-frechet-spectral-form`, not a `\[ … \]` display. Treated as a candidate only, per
the skill; no action taken.

---

## 1. `main.tex:49` — abstract names the wrong object of the manufactured solution
**Issue.** "verified against a manufactured solution **of** the constant reference tangent".
**Rationale.** The manufactured solution belongs to the equations linearized about the constant
reference tangent; "of the tangent" reads as if the tangent itself were solved. The introduction
(`main.tex:116`) already states the same fact as "in the constant reference tangent", so the
abstract is both imprecise and internally inconsistent.
**Priority.** low
**Proposed revision.** "verified against a manufactured solution **for** the constant reference tangent".
**Disposition.** applied.

## 2. `main.tex:52` — coordinated scope negation takes a singular verb
**Issue.** "no quantitative finite-deformation verification and no experimental validation **is** claimed".
**Rationale.** Two coordinated negated subjects require the plural verb. The claim is a scope
boundary and must read cleanly.
**Priority.** low
**Proposed revision.** "…and no experimental validation **are** claimed for those demonstrations."
**Disposition.** applied.

## 3. `main.tex:98–99` — introduction uses undeclared notation ("normalized right stretch")
**Issue.** "This conformal distention changes pore volume while preserving the **normalized right
stretch** of the mineral."
**Rationale.** The polar decomposition, the right stretch \(\mathbf U\), and the normalized
mineral stretch \(\bar{\mathbf U}=a^{-1/3}\mathbf U\) are not introduced until Section 2 and
`stress_reconstruction.tex`; an uninitiated continuum-mechanics reader meets the term here with no
antecedent. The author profile requires the physical distinction before its formal representation
and just-in-time terminology.
**Priority.** medium
**Proposed revision.** "changes pore volume while **leaving the shape of the mineral unchanged**."
**Disposition.** applied. (Accurate: \eqref{eq:conformal-mineral-metric} gives
\(\bar{\mathbf C}=a^{-2/3}\mathbf C\), i.e. equal normalized right stretches, and makes no claim
about the orientation of the intermediate frame.)

## 4. `main.tex:162–164` — mass-flux bar convention introduced long before its first use
**Issue.** The notation inventory announces "a bar on a mass-flux boundary measure denotes its
referential normalization (the referential mass-flux vector itself is written \(\mathbf Q_f\), with
\(\mathbf Q_f\cdot\mathbf N=\bar Q_f\))".
**Rationale.** \(\mathbf Q_f\), \(\bar Q_f\), and \(\mathbf N\) first occur in
`sections/finite_elements.tex` (lines 49, 54, 101, 108–115), where both symbols are defined
locally and \(\mathbf Q_f\cdot\mathbf N=\bar Q_f\) is restated. Declaring the convention in
Section 2 collects notation "merely because it will be needed later", which the author profile
excludes; the clause is redundant with its FE definition and adds nothing at this point.
**Priority.** medium
**Proposed revision.** Delete the mass-flux clause from the Section 2 inventory; rely on the local
definition in `sections/finite_elements.tex`. The kinematic, density, and stress bar/hat
conventions stay.
**Disposition.** applied.

## 5. `main.tex:167` — forward reference to `\eqref{eq:rotated-mineral-cauchy}`
**Issue.** "The two stress representations differ by the rotation \eqref{eq:rotated-mineral-cauchy}."
appears before that equation is displayed.
**Rationale.** Considered as a candidate, but the author profile permits an anecdotal forward
reference when the cited display is nearby; \eqref{eq:rotated-mineral-cauchy} is fifteen lines
below in the same section and the intervening paragraph carries the physical motivation.
**Priority.** low
**Proposed revision.** none.
**Disposition.** declined (permitted by the profile; no reader-facing problem).

## 6. `main.tex:484` — sentence fragment masquerading as a clause
**Issue.** "Dilation times a proper rotation **makes** that change of variables explicit".
**Rationale.** The bare product phrase supplies no subject for the reader to attach to; the
sentence is grammatically strained and obscures the step it introduces.
**Priority.** low
**Proposed revision.** "**Writing the distention as** a dilation times a proper rotation makes that
change of variables explicit; the skew rotation variation performs no work against a symmetric
stress."
**Disposition.** applied.

## 7. `main.tex:495–496` — coordinate subject chain in the conclusion
**Issue.** "The reference stress and storage coefficients **and** the finite unjacketed path provide
additional checks."
**Rationale.** Two coordinated subject groups joined by a bare "and" read as a three-item list and
delay the verb. A subordinating transition marks the second group as an accompaniment.
**Priority.** low
**Proposed revision.** "The reference stress and storage coefficients, **together with** the finite
unjacketed path, provide additional checks."
**Disposition.** applied.

## 8. `main.tex:118` — "No plastic deformation is considered."
**Issue.** A standalone negated sentence closes the introduction's roadmap paragraph.
**Rationale.** Considered as a candidate under the "close constructively" and "avoid negation"
rules. It conveys an excluded physical mechanism, which the profile explicitly permits, and it is
the only statement of the model's elastic scope in the introduction.
**Priority.** low
**Proposed revision.** none.
**Disposition.** declined (necessary scope negation; already a complete sentence).

## 9. `main.tex:436–437` — "so" linking material strain to spatial rotation
**Issue.** "The energy depends on material strain, **so** a superposed spatial rotation \(\mathbf Q\)
leaves \(\bar J\) unchanged and rotates the tensor as \(\mathbf B(\mathbf Q\mathbf F,p)=\mathbf Q\mathbf B\mathbf F\mathbf Q^T\)."
**Rationale.** Examined as a candidate unsupported "so". The link is exact: a spatial rotation
\( \mathbf F\mapsto\mathbf Q\mathbf F\) leaves \(\mathbf C=\mathbf F^T\mathbf F\), \(J\), and
\(\bar J\) unchanged, so it cannot alter the energy or the mineral volume. The connective is sound.
**Priority.** low
**Proposed revision.** none.
**Disposition.** declined (logically supported).

## 10. `sections/stress_reconstruction.tex:139–140` — "the left-hand side" names the wrong side
**Issue.** "At fixed deformation and nonnegative pressure, **the left-hand side** increases strictly
from negative to positive infinity …"
**Rationale.** \eqref{eq:anisotropic-mineral-eos} is displayed as `0 &= …`, so its literal
left-hand side is the constant \(0\). The quantity that increases is the right-hand expression.
The uninitiated reader resolving "left-hand side" from the display is misdirected; this is a pure
referent error.
**Priority.** medium
**Proposed revision.** "**the right-hand side of \eqref{eq:anisotropic-mineral-eos}** increases
strictly from negative to positive infinity as \(\bar J\) ranges over positive values."
**Disposition.** applied.

## 11. `sections/stress_reconstruction.tex:194–196` — "These equations" has no clear antecedent
**Issue.** "…the additional deformation allowed by the dilation part of conformal distention.
**These equations** are necessary and sufficient within the present construction for the full
drained energy to equal the prescribed \(W_d\)."
**Rationale.** The paragraph has just displayed \eqref{eq:drained-compliance-restriction}, while
the stiffness form \eqref{eq:drained-stiffness-restriction} appears earlier on the same page.
"These equations" leaves the sufficiency claim attached to an unspecified set, which is exactly
where the reader must know the scope.
**Priority.** medium
**Proposed revision.** "**Together, \eqref{eq:drained-stiffness-restriction} and
\eqref{eq:drained-compliance-restriction} are** necessary and sufficient within the present
construction…".
**Disposition.** applied (adds no claim; only identifies the displays already on the page).

## 12. `sections/stress_reconstruction.tex:81–83` — timing of the curvature assumption
**Issue.** "We assume \(0<K<\phi_{s0}K_s\), so the distention energy has positive curvature with
respect to \(\ln a\)." follows \eqref{eq:distention-energy}, whose denominator already contains the
factor.
**Rationale.** Examined as a just-in-time candidate. The assumption is stated in the same sentence
pair that first needs it, immediately after the display it qualifies, and it is explicitly labelled
as an assumption rather than a derived result. No change improves it.
**Priority.** low
**Proposed revision.** none.
**Disposition.** declined (already just-in-time and correctly labelled).

## 13. `sections/experiments.tex:180–184` — verification inventory compressed into one sentence
**Issue.** A single sentence carries the suite size, the per-state count, the state/identity
factorization, the eight identity families, and the two reference relations.
**Rationale.** The counts are the evidence for the verification claim, and a reader parsing them
from one 60-word sentence is likely to lose which number attaches to which object. Splitting at the
first count preserves every figure and category verbatim.
**Priority.** low
**Proposed revision.** End the first sentence at "186 named checks."; begin "These include the
65 per-state identities …" and join the reference relations with "and the two reference Biot and
rank-one compliance relations…" in place of "plus the two …".
**Disposition.** applied.

## 14. `sections/experiments.tex:30–31` — parse ambiguity in the isotropic-comparison modulus
**Issue.** "Its mineral shear modulus is \(16.8K_*\), the mean of the five deviatoric stiffness
modes of \(\mathbb C_s\), divided by two."
**Rationale.** The comma before "divided by two" leaves it ambiguous whether the division applies
to the mean or to the whole clause, and the sentence describes how a reported number was obtained.
Reordering the words risks changing which quantity is halved, and the calculation is a settled
scientific result.
**Priority.** low
**Proposed revision.** none.
**Disposition.** declined (quantitative description; a wording change could alter the stated
definition of \(16.8K_*\), which is out of scope).

## 15. `sections/finite_elements.tex:152–153` — reused symbols `a`, `b` for the reference rectangle
**Issue.** "The full reference rectangle is \([-a,a]\times[-b,b]\), with \(a=1\) and \(b=0.1\)…",
while \(a=\det\mathbf A\) is the distention volume ratio of Section 2 and \(\mathbf b_0\) is the
body force.
**Rationale.** The two uses are locally scoped and separated by the whole constitutive and
verification development, and the reader is unlikely to confuse a rectangle half-length with a
distention determinant. Renaming the half-lengths would edit displayed notation, which this cycle
may not do.
**Priority.** medium
**Proposed revision.** Rename the half-lengths in a future technical cycle if the parent elects to
do so; not actionable as prose.
**Disposition.** declined (out of scope: renaming a symbol alters displayed notation and equations).

---

### Summary

| Priority | Items |
| --- | --- |
| medium | 3, 4, 10, 11, 15 |
| low | 1, 2, 5, 6, 7, 8, 9, 12, 13, 14 |

Applied: 9 items (1, 2, 3, 4, 6, 7, 10, 11, 13) — 10 edit operations across 3 files.
Declined: 6 items (5, 8, 9, 12, 14, 15).

No item required a change to an equation, label, `\ref`/`\eqref`/`\cref`, citation, number, or
assumption. Items 5, 8, 9, and 12 were declined after contextual assessment found the original
wording already conforms to the profile; items 14 and 15 were declined as out of the prose-only
scope of this cycle.
