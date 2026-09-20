# Foster engineering-review / editor memo — cycle 2

Manuscript: `An anisotropic Biot tensor from mineral stress and distention work`
Repository: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
Scope: prose only (wording in `main.tex` and `sections/*.tex`).
Reviewer position: fresh independent read of the current tree after cycle 1.

Priorities: **high** = blocks comprehension or misstates scope; **medium** =
local clarity, precision, or referent problem that a reader notices; **low** =
polish.

---

## Findings

**F1 — main.tex:153 (§2, after eq. (4)) — medium — APPLIED.**
"An arbitrary determinant-one distention factor would also allow shear and would
describe a different deformation mechanism." Two stacked modals and a scope-less
"also" (also relative to what?). The physical point is that adding shear to the
distention factor changes the mechanism. *Revised* to "A general determinant-one
distention factor would additionally allow shear and describe a different
deformation mechanism."

**F2 — main.tex:362 (§4, "Pressure coupling at finite deformation") — medium — APPLIED.**
"The double-prime stress differentiates \(W''\) at fixed pressure." The subject
is a stress, but the sentence means the stress *results from* differentiating
the energy. *Revised* to "The double-prime stress is obtained by differentiating
\(W''\) at fixed pressure."

**F3 — main.tex:393–394 (§4) — medium — APPLIED.**
"To evaluate this derivative, differentiate the mineral equation at fixed
pressure. It gives" — the pronoun "It" has no nominal antecedent (the preceding
clause is imperative). *Revised* to "...at fixed pressure, which gives".

**F4 — main.tex:469–471 (§4, after eq. (25)) — medium — APPLIED.**
"The instantaneous tensor cannot generally multiply the entire pressure change
relative to the drained stress." A bare negation leaves the reader to infer the
operative rule. *Revised* to state it affirmatively: "The instantaneous coupling
tensor therefore applies to an infinitesimal pressure increment; a finite change
from the drained stress requires the integral in \eqref{eq:integrated-pressure-response}."
(Refers to an existing label; no new label introduced.)

**F5 — main.tex:117–118 (close of Introduction) — low — APPLIED.**
"No plastic deformation is considered." A lone negative sentence closing the
scope paragraph. *Revised* to state the scope affirmatively: "We restrict
attention to elastic deformation." (Meaning preserved: elastic response only.)

**F6 — sections/finite_elements.tex:9–10 (§1 opening) — medium — APPLIED.**
"All balance equations are integrated over the reference mixture domain
\(\Omega_0\), and \(\mathbf F=\mathbf I+\operatorname{Grad}\mathbf u\)." The
second clause is a fragment, not parallel to "are integrated." *Revised* to
"...domain \(\Omega_0\), with \(\mathbf F=\mathbf I+\operatorname{Grad}\mathbf u\)."

**F7 — sections/finite_elements.tex:117 (§2, weak balances) — medium — APPLIED.**
"The overdot follows a material point of the skeleton." An overdot does not
follow anything; the sentence intends the material time derivative. *Revised* to
"The overdot denotes a time derivative following a material point of the
skeleton."

**F8 — sections/experiments.tex:203–204 (§5 verification) — medium — APPLIED.**
"At negative pressure, the solver brackets the increasing branch ... It
distinguishes loss of that branch from violation of positive phase volumes."
"It" is ambiguous between the solver and the bracket. *Revised* to "The solver
distinguishes loss of that branch from violation of positive phase volumes."

**F9 — sections/experiments.tex:150–151 (§4, constrained layer) — low — APPLIED.**
"This scalar boundary-condition solve is coupled to the mineral-volume equation."
"Solve" as a bare noun is informal. *Revised* to "This scalar boundary-condition
problem is coupled to the mineral-volume equation."

**F10 — sections/logarithmic_derivative.tex:42 (appendix) — medium — APPLIED.**
"The coefficient is symmetric in \(i,j\), which makes the derivative self-adjoint.
It maps \(\mathbf C\) to \(\mathbf I\)." "It" can attach to the coefficient or
the derivative. *Revised* to "The derivative maps \(\mathbf C\) to \(\mathbf I\)."

**F11 — sections/limits.tex:50–52 (§2, isotropic mineral) — low — APPLIED.**
Two "also"s in adjacent sentences ("also gives ... also require"). The second
adds nothing. *Revised* to drop the second: "Here the full Hooke law and
volume-only conformal distention require the drained shear stiffness ...".

**F12 — sections/stress_reconstruction.tex:117 (§3, pressure equilibrium) — low — APPLIED.**
"Pressure equilibrium differentiates this energy at fixed \(\mathbf F\)." Same
agentive mismatch as F2: the condition is imposed *by* differentiating the
energy. *Revised* to "Pressure equilibrium is enforced by differentiating this
energy at fixed \(\mathbf F\)."

**F13 — sections/stress_reconstruction.tex:83 (§3, distention energy) — low — APPLIED.**
"Because \(W_A\) depends on \(a\) alone, its values determined on this path also
apply ..." — "its values" is an awkward possessive referent for the values of
\(W_A\). *Revised* to "the values determined on this path also apply ...".

**F14 — main.tex:160–164 (§2, bar convention) — low — DECLINED.**
After cycle 1 the convention sentence no longer covers the referential
mass-flux quantity \(\bar Q_f\) used in `sections/finite_elements.tex`. It is
defined at its point of use ("outward mass flux \(\bar Q_f\)" with
\(\mathbf Q_f\cdot\mathbf N=\bar Q_f\)), so no reader is stranded, and re-adding
the clause would undo cycle 1's deliberate deletion.

**F15 — main.tex:159–160 (§2) — low — DECLINED.**
"Let \(\bar\rho_s\) be solid intrinsic density" omits articles. This is the
repo's established terse math-prose convention ("Let \(X\) be Y"); per-item
fixing would be stylistic churn without a comprehension gain.

**F16 — sections/logarithmic_derivative.tex:35 — low — DECLINED (false positive).**
`.agent/shared/tools/review_scan.py` flagged an "unnumbered-display" `\[`. The
token is the row separator `\\[5pt]` inside the `cases` environment, not a
display. No action.

**F17 — symbol reuse in displayed notation — low — OUT OF SCOPE / DEFERRED.**
`finite_elements.tex` uses the reference-rectangle semi-axes \(a=1\), \(b=0.1\)
(`\([-a,a]\times[-b,b]\)`), while `main.tex` §2 uses \(a=\det\mathbf A\) for the
distention volume ratio and \(\mathbf b_0\) for mechanical body force. This is a
genuine cross-section notation collision, but resolving it would change displayed
symbols/equations, which the prose-only scope forbids. Recorded here for the
parent to schedule as a technical/notation change.

---

## Assessment summary

The manuscript is in good technical-prose condition: no hedging artifacts, no
drafting-history phrasing, no unsupported novelty claims, and no
equation/citation defects were found. Cycle-2 findings are localized
sentence-level issues (agentive mismatches, ambiguous pronouns, one fragment,
one bare negation). Nothing in the derivation, the displayed equations, the
symbol definitions, the numeric values, or the stated assumptions required
change.
