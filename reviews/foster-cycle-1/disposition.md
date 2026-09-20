# Disposition — Foster editorial cycle 1 of 3

One row per memo item. Line numbers are those of the reviewed snapshot
`c621378778d49f8875679440cf874a74aef3caa5d9b04b8936ad319fb57f885f`.

| # | Location | Priority | Disposition | Reason |
| --- | --- | --- | --- | --- |
| 1 | `main.tex:49` | low | applied | "solution of the constant reference tangent" → "solution for …"; aligns the abstract with the introduction wording and names the correct object. |
| 2 | `main.tex:52` | low | applied | Coordinated negated subjects now take the plural verb ("are claimed"); scope claim unchanged. |
| 3 | `main.tex:98–99` | medium | applied | Replaced premature "normalized right stretch" with the physical statement "leaving the shape of the mineral unchanged"; the term is introduced where it is defined in Section 2. |
| 4 | `main.tex:162–164` | medium | applied | Removed the mass-flux bar clause from the Section 2 notation inventory; `\mathbf Q_f`, `\bar Q_f`, and `\mathbf Q_f\cdot\mathbf N=\bar Q_f` are defined locally in `sections/finite_elements.tex`. |
| 5 | `main.tex:167` | low | declined | Nearby forward reference to `\eqref{eq:rotated-mineral-cauchy}` is permitted by the author profile; equation follows in the same section. |
| 6 | `main.tex:484` | low | applied | Recast the bare product phrase as a clause ("Writing the distention as a dilation times a proper rotation makes …"). |
| 7 | `main.tex:495–496` | low | applied | Coordinated subject chain recast with "together with"; verb and meaning unchanged. |
| 8 | `main.tex:118` | low | declined | "No plastic deformation is considered." states an excluded mechanism, which the profile permits, and is the introduction's only elastic-scope statement. |
| 9 | `main.tex:436–437` | low | declined | The "so" is logically exact: a superposed spatial rotation leaves \(\mathbf C\), \(J\), and \(\bar J\) unchanged. |
| 10 | `sections/stress_reconstruction.tex:139–140` | medium | applied | Corrected the referent to "the right-hand side of \eqref{eq:anisotropic-mineral-eos}"; the display's literal left-hand side is \(0\). |
| 11 | `sections/stress_reconstruction.tex:194–196` | medium | applied | Named the two displays explicitly in place of "These equations"; no claim added. |
| 12 | `sections/stress_reconstruction.tex:81–83` | low | declined | The curvature assumption is stated immediately after the display it qualifies and is already labelled as an assumption. |
| 13 | `sections/experiments.tex:180–184` | low | applied | Split the verification-count sentence; every number (186, 65, five × thirteen, two) and every identity family preserved verbatim. |
| 14 | `sections/experiments.tex:30–31` | low | declined | The sentence defines how \(16.8K_*\) is obtained; rewording risks altering that definition, outside prose-only scope. |
| 15 | `sections/finite_elements.tex:152–153` | medium | declined | Reused symbols \(a,b\) for the reference rectangle; renaming would modify displayed notation and equations, outside this cycle's scope. Future technical cycle. |

**Totals.** 15 memo items — 9 applied, 6 declined. Applied items map to 10 edit
operations (item 13 is two sentence-boundary edits) across `main.tex`,
`sections/experiments.tex`, and `sections/stress_reconstruction.tex`.
