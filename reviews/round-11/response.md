# Author response — independent simulated review, round 11

All three reports were collected before this response. Round verdicts on the
immutable snapshot `b9fadd66e96794417a4bed1f674064928716ffb3f2cc30d09edc0a663586fe6a`
(286 files, manifest hash equal to the snapshot ID):

| Reviewer | Charge | Verdict |
| --- | --- | --- |
| 1 | mathematics and correctness | MAJOR REVISION |
| 2 | physics and source fidelity | MINOR REVISION |
| 3 | prose, notation, significance | MINOR REVISION |

No reviewer found a mathematical error, an unreproducible number, or a false
scientific pass; all three independently confirmed the snapshot hashes. The
required corrections concern claim-to-evidence linkage, packaging completeness,
and descriptive accuracy. Because source content changes, this round's verdicts
do not carry to the revised version; a new frozen snapshot will receive fresh
independent reviews.

## Substantiated findings and disposition

| Finding | Source | Disposition |
| --- | --- | --- |
| MAJOR-1: `site-evidence.json` cites report artifacts (`site/reports/*.json`, `site/scientific-snapshot.json`) and `validation/**` that are absent from the reviewed package, leaving the `analytical` pass unbacked inside it | R1; R2 m-5 | Accepted. The review snapshot now includes `site/**` and `validation/**`, and the supplement archive is hash-pinned; the site manifest is regenerated from the corrected runs. |
| MAJOR-2: shipped `compute_mms_order.py` resolves `RUNS` to a path that does not exist in the distributed layout, exits 0, and silently writes an empty evidence file | R1 | Accepted. The script resolves the run directory in the distributed layout and fails loudly instead of overwriting the evidence file with an empty document. |
| m-1 / MINOR-3: the `force_relative ≈ 1.0` explanation is wrong. Plate equilibrium actually holds to about 1e-12; the value arises because the analyzer divides by the traction `q` instead of the applied resultant `2a q_L` | R2; R1 | Accepted. The analyzer uses the correct per-deck resultant, all runs are re-analyzed from their existing `solution.csv`, and the metric is reported as an equilibrium residual. |
| m-2 / MINOR-3: "displacement-controlled demonstrations" mislabels the decks, which apply a traction load with a kinematically constrained rigid platen | R2 | Accepted. All descriptive text now says force-controlled with a kinematic platen. |
| m-3: the partial-drainage runs use a square domain while the comparison reference is the slender `a=1, b=0.1` Mandel geometry | R2 | Accepted. The partial family's reference comparison is marked not comparable and excluded from verification claims; its mass-balance, platen-equality and map results are retained. |
| m-4 / MINOR-1: "differences of 60–100 percent" understates the recorded displacement differences, which are about 170–180 percent | R2; R1 | Accepted. The measured per-metric ranges are stated from the artifacts. |
| MINOR-2: temporal orders above one (ux 1.40, p 1.25 at nx = 64) are quoted while asserting the order is "not higher" | R1 | Accepted. The fixed-mesh difference-method result is reported as bounding the temporal order near one, with the larger nx = 64 values identified as residual mesh-floor contamination. |
| MINOR-4 / o-2: the "finite-load limit toward the linear reference" framing is not demonstrated; the normalized error floors at about 3.2e-3 | R1; R2 | Accepted. The observed floor is stated and the framing is softened to a demonstration. |
| M1: the new coupled finite-element section is invisible to the abstract, the introduction roadmap, and the conclusions | R3 | Accepted. Abstract, roadmap, and conclusions now state what the coupled section does and does not establish; keyword list extended. |
| M2: the section lacks the scope qualifiers recorded in the project's own evidence file | R3 | Accepted. A "Scope of these results" paragraph states that the calculations are implementation verification plus finite-load demonstrations, that they are not quantitative verification of the nonlinear law and not experimental validation, and that the partial-drainage reference comparison is not comparable. |
| M3: the embedded supplement excludes finite-element simulations and the available-code paragraph gives no pointer to the coupled code | R3; R2 m-6 | Accepted. The supplement is hash-pinned in the reviewed package and the availability statement points to the coupled code and evidence. |
| M4: the overbar is overloaded and fourth-order typography is inconsistent | R3 | Accepted in part. A notation paragraph now separates mineral (bar on kinematics, energy, intrinsic density) from mixture-frame stress (bar) and true-frame stress (hat). |
| M5: current- versus reference-volume mass conventions alternate between the two halves of the paper | R3 | Accepted. The coupled section states its per-reference-volume convention and its relation to the current-configuration measures of the preceding sections. |
| M6: nine applied/experimental references are uncited and the engineering significance framing is thin | R3 | Accepted. The introduction now cites the measured anisotropic poroelasticity, soft-porous-material and poroelastic-fracture literature that the bibliography already contained. |

## Optional suggestions

Optional items (reference ordering, appendix pointer, AI-tool identifiers, the
two distinct material sets, conclusion wording, the analytical-versus-numerical
invariance attribution, gradient-flux reporting, kernel-to-equation inline
labels) are recorded and carried into the next revision where they cost nothing
and do not change scientific content.

This is simulated AI review, not journal acceptance or final author approval.
