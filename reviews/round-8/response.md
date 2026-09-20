# Response to independent simulated review — round 8

Snapshot reviewed: `5ca2dd88c8341509f3b74bdc7a68c481b04362184bd816364277c435f3183925`.
All three reports were collected before changes. Verdicts: ACCEPT, MINOR REVISION,
MINOR REVISION. These votes do not apply to the revised source.

| Comment | Disposition and evidence | Change and verification |
| --- | --- | --- |
| R1-01 / R2-01, root bracketing | Accepted. The fixed bracket missed admissible stable negative-pressure roots and a large positive-pressure root. | `examples/conformal_model.py` now brackets the increasing residual branch at negative pressure and the unique positive-pressure root using dimensionless shifted residuals. Eleven added checks compare the principal Lambert-W solution at p=-14,-13,800 and separately reject scalar branch loss and invalid phase volumes. All 186 checks pass, maximum constitutive error 2.455e-9. Figure generation still passes 1,051 states. No tolerance changed. |
| R1-02 / R3-01, curvature | Accepted. The quadratic is convex in logarithmic distention, not globally in its exponential. | `sections/stress_reconstruction.tex` now says positive curvature with respect to ln a. Equations and physical assumptions unchanged. Clean LuaLaTeX build checked. |
| R2-02, generation order | Accepted. The supplemental refinement plot requires verification output first. | README now runs conformal verification before experiments. Supplement README gives all standalone verification commands in order. Six figure PDFs and six CSVs are included. |
| R3-02, accessible evidence | Accepted. Reader access must travel with this uncommitted draft rather than imply unpublished sources already exist at a public commit. | Versioned ZIP supplement is embedded in the article PDF. It contains numerical sources, exact data, reports, figure PDFs, licenses, commands and SHA-256 manifest. `pdfdetach` extracted a byte-identical archive; every payload hash passed; 186 tests passed from the extracted archive. Companion bibliography now links the publicly accessible exact commit 223901199e33e40ae1b82a1ae437f4cf71683ba8; all three reference-source hashes match remotely retrieved files. No companion edits or public publication of the new draft. |
| R3-03, polar detail | Retained current figure, optional suggestion declined. | The zero-based polar scale faithfully shows the size of normal coupling, while adjacent tangential coupling and Cartesian shear-response figures resolve the smaller anisotropic differences. Adding an inset would duplicate these views and crowd a two-panel figure. The plotted quantities and scope remain unchanged. |

Verification is implementation and constitutive verification, not physical validation
or general stability. Fresh reviewers must assess the new frozen snapshot. Final
engineering and narrative audit remains mandatory after an accepted round.
