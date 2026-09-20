# Reviewer 3 — exposition, physical interpretation, and scientific readiness

Snapshot: `5ca2dd88c8341509f3b74bdc7a68c481b04362184bd816364277c435f3183925`

## Assessment

The principal argument is scientifically convincing within its explicitly restricted constitutive class. The manuscript is self-contained in the important sense: the complete phase-stress equation leads through reversible work to the equivalent energy, mineral-volume equation, and pressure-coupling tensor without requiring the companion manuscript to supply a missing derivation. Intrinsic density, bulk solid density, phase fractions, and reference-volume normalizations remain consistent. The true-frame versus mixture-frame mineral stress distinction is correctly carried through the work calculation. The internal rotation is correctly interpreted as a representation choice for this objective, volume-only specialization, rather than a separately observable elastic mode.

The drained compliance restriction is derived rather than concealed in independent material inputs. Logarithmic conjugate stress is distinguished from spatial Kirchhoff stress, including noncoaxial states. The reference, isotropic, and unjacketed limits are plausible and mutually consistent. The fixed-deformation experimental interpretation of the Biot tensor is especially useful, and the pressure integral avoids confusing instantaneous sensitivity with a finite pressure increment. Synthetic examples are appropriately separated from physical validation and general stability. I found no substantive derivational defect requiring a major revision.

## Comments

### R3-01 — Minor; required: specify the variable in the curvature statement

**Location:** `sections/stress_reconstruction.tex:77–83`, Eq. (33), PDF p. 5.

The statement that the assumption `0 < K < phi_s0 K_s` makes the distention energy have “positive curvature” needs qualification. Equation (33) is quadratic and strictly convex in **logarithmic distention**, not globally convex in the stated argument `a`. Writing its positive coefficient as `c = K/(1-K/(phi_s0 K_s))`, direct differentiation gives `d²W_A/da² = c(1-ln a)/a²`, which becomes negative for `a > e`. This matters because the manuscript later carefully distinguishes scalar stability from stability against general deformation.

**Required change:** say “positive curvature with respect to ln a” or “a positive quadratic energy in logarithmic distention.” No constitutive change or new computation is needed.

### R3-02 — Minor; required for reader-facing reproducibility: identify where the accompanying code can be obtained

**Location:** `sections/experiments.tex:193–197`, PDF p. 14; companion reference [7], PDF p. 16.

The numerical section names repository-relative scripts and says that the repository records parameters and figure data, but the manuscript supplies no repository/archive URL or persistent identifier. Reference [7] likewise identifies an inspected companion version without an accessible location. The provided review snapshot makes the numerical evidence auditable to this reviewer, but a reader receiving the article alone cannot follow the reproducibility instructions.

**Required change:** add a code/data availability statement giving a resolvable repository or supplementary archive and an identifiable release/commit. Make the cited companion version accessible, or explicitly identify its unpublished status and access conditions. This is an accessibility correction, not a request for additional scientific validation.

### R3-03 — Low; optional: make directional differences easier to see

**Location:** Figure 3(a), PDF p. 12; `sections/experiments.tex:104–118`.

The normal-sensitivity polar curves nearly coincide at the displayed 0–1 radial scale, while the tangential panel clearly shows anisotropy. A small inset or a companion curve showing deviation from the angular mean would help readers see the normal directional effect without changing the honest zero-based polar plot. The present caption and plotted quantities are otherwise clear.

## Actual checks and limits of review

- Verified SHA-256 hashes of all 95 manifest entries, including the manuscript PDF; no mismatches. The manifest hash equals the supplied snapshot ID.
- Read `main.tex`, all four included sections, disclosure, author style profile, and the complete 17-page PDF text. Visually inspected rendered theory pages 3–5, 7, and 9, and all five figures on pages 11–13. No unresolved-reference or overfull/underfull-box warnings were found in the supplied build log.
- Independently traced the volume weights, rotation cancellation, energy-returned phase stress, fixed-pressure differentiation, and compliance restriction. Checked Gajo's cited Eqs. (3.27), (3.32), and (3.34) in the locally supplied primary-source PDF; their elimination supports the stated scalar volumetric correspondence, not equivalence of the full shear laws.
- Inspected the conformal constitutive and verification implementation and numerical JSON evidence. Reran `verify_conformal.py` with all output redirected to reviewer-owned `/tmp` scratch and bytecode writing disabled: all 175 checks passed, maximum constitutive-identity error `2.4535896960865923e-9`. Observed refinement orders were approximately 2.0000–2.0167. The rerun used Python 3.10.12, NumPy 1.26.4, and SciPy 1.15.3; the frozen evidence records NumPy 2.2.6. The reported results reproduced despite that environment difference.
- Checked the recorded 273-state/13-material tensor evidence and reconstruction evidence, but did not rerun those two separate suites. Did not assess every bibliographic claim against primary sources, perform physical validation, establish global ellipticity, or inspect other reviewer reports. No manuscript or snapshot files were modified.

MINOR REVISION
