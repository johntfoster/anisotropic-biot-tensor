# Foster engineering-review / editor disposition — cycle 2

One row per memo finding. Priority: high / medium / low.
Scope: prose only; no equation, label, citation, numeric value, table entry, or
stated assumption changed.

| # | Location | Priority | Disposition | Reason |
|---|----------|----------|-------------|--------|
| F1 | main.tex:153 (§2) | medium | APPLIED | Removed stacked modals and scope-less "also"; states the mechanism change directly. |
| F2 | main.tex:362 (§4) | medium | APPLIED | A stress cannot "differentiate" an energy; states the energy is differentiated. |
| F3 | main.tex:393–394 (§4) | medium | APPLIED | "It" had no nominal antecedent after an imperative clause. |
| F4 | main.tex:469–471 (§4) | medium | APPLIED | Bare negation replaced by an affirmative statement of the infinitesimal/finite role of B; references an existing label (\eqref only, no new label). |
| F5 | main.tex:117–118 (Intro close) | low | APPLIED | Scope stated affirmatively instead of a lone negative sentence. |
| F6 | finite_elements.tex:9–10 | medium | APPLIED | Coordinate clause was a fragment; joined with "with". |
| F7 | finite_elements.tex:117 | medium | APPLIED | An overdot denotes a derivative; it does not "follow" a material point. |
| F8 | experiments.tex:203–204 | medium | APPLIED | Ambiguous pronoun; named subject "The solver". |
| F9 | experiments.tex:150–151 | low | APPLIED | Replaced informal nominal "solve" with "problem". |
| F10 | logarithmic_derivative.tex:42 | medium | APPLIED | Ambiguous pronoun; named subject "The derivative". |
| F11 | limits.tex:50–52 | low | APPLIED | Removed the second of two adjacent "also"s (redundant). |
| F12 | stress_reconstruction.tex:117 | low | APPLIED | Agentive mismatch; pressure equilibrium is enforced by differentiating the energy. |
| F13 | stress_reconstruction.tex:83 | low | APPLIED | Awkward possessive referent; uses "the values determined on this path". |
| F14 | main.tex:160–164 (§2 bar convention) | low | DECLINED | \bar Q_f is defined at point of use in finite_elements.tex; re-adding the clause would undo cycle 1's deliberate deletion. |
| F15 | main.tex:159–160 (§2) | low | DECLINED | Article omission follows the repo's established terse "Let X be Y" math-prose convention; churn without comprehension gain. |
| F16 | logarithmic_derivative.tex:35 | low | DECLINED | review_scan "unnumbered-display" flag is a false positive: `\[` is the row separator inside `cases`. |
| F17 | finite_elements.tex vs main.tex (a, b reuse) | low | DEFERRED (out of scope) | Resolving the rectangle semi-axis / distention-ratio symbol collision would change displayed notation, forbidden in this prose-only pass. |

## Applied counts

- Applied: 13 (F1–F13)
- Declined: 3 (F14, F15, F16)
- Deferred / out of scope: 1 (F17)
- Total findings: 17

## Before / after for applied items

F1 main.tex:153
- before: `An arbitrary determinant-one distention factor would also allow shear and would describe a different deformation mechanism.`
- after:  `A general determinant-one distention factor would additionally allow shear and describe a different deformation mechanism.`

F2 main.tex:362
- before: `The double-prime stress differentiates \(W''\) at fixed pressure.`
- after:  `The double-prime stress is obtained by differentiating \(W''\) at fixed pressure.`

F3 main.tex:393–394
- before: `differentiate the mineral equation at fixed pressure. It gives`
- after:  `differentiate the mineral equation at fixed pressure, which gives`

F4 main.tex:469–471
- before: `The fixed-pressure effective stress \(\mathbf\sigma''\) itself depends on pressure. The instantaneous tensor cannot generally multiply the entire pressure change relative to the drained stress.`
- after:  `The fixed-pressure effective stress \(\mathbf\sigma''\) itself depends on pressure. The instantaneous coupling tensor therefore applies to an infinitesimal pressure increment; a finite change from the drained stress requires the integral in \eqref{eq:integrated-pressure-response}.`

F5 main.tex:117–118
- before: `and report finite-load demonstrations. No plastic deformation is considered.`
- after:  `and report finite-load demonstrations. We restrict attention to elastic deformation.`

F6 finite_elements.tex:9–10
- before: `integrated over the reference mixture domain \(\Omega_0\), and \(\mathbf F=\mathbf I+\operatorname{Grad}\mathbf u\).`
- after:  `integrated over the reference mixture domain \(\Omega_0\), with \(\mathbf F=\mathbf I+\operatorname{Grad}\mathbf u\).`

F7 finite_elements.tex:117
- before: `The overdot follows a material point of the skeleton.`
- after:  `The overdot denotes a time derivative following a material point of the skeleton.`

F8 experiments.tex:203–204
- before: `brackets the increasing branch of the mineral equation before its turning point. It distinguishes loss of that branch from violation of positive phase volumes.`
- after:  `brackets the increasing branch of the mineral equation before its turning point. The solver distinguishes loss of that branch from violation of positive phase volumes.`

F9 experiments.tex:150–151
- before: `This scalar boundary-condition solve is coupled to the mineral-volume equation.`
- after:  `This scalar boundary-condition problem is coupled to the mineral-volume equation.`

F10 logarithmic_derivative.tex:42
- before: `which makes the derivative self-adjoint. It maps \(\mathbf C\) to \(\mathbf I\).`
- after:  `which makes the derivative self-adjoint. The derivative maps \(\mathbf C\) to \(\mathbf I\).`

F11 limits.tex:50–52
- before: `Here the full Hooke law and volume-only conformal distention also require the drained shear stiffness`
- after:  `Here the full Hooke law and volume-only conformal distention require the drained shear stiffness`

F12 stress_reconstruction.tex:117
- before: `Pressure equilibrium differentiates this energy at fixed \(\mathbf F\).`
- after:  `Pressure equilibrium is enforced by differentiating this energy at fixed \(\mathbf F\).`

F13 stress_reconstruction.tex:83
- before: `Because \(W_A\) depends on \(a\) alone, its values determined on this path also apply when the mineral changes shape.`
- after:  `Because \(W_A\) depends on \(a\) alone, the values determined on this path also apply when the mineral changes shape.`
