# Independent exposition, notation, and engineering-insight review

This is simulated AI peer review, not journal acceptance. I reviewed the immutable `insight-round-1` snapshot independently, without reading other reviews, prior reports, or acceptance counts. All source locations below are relative to that snapshot.

## Snapshot integrity

Declared snapshot ID: `a5289ef83d1b55941719abcd663ad6792debdf728698e833c9f99d998174d18f`.

The SHA-256 digest of `source-manifest.json` equals that ID and the contents of `SNAPSHOT_ID`. I re-hashed all **713** manifest-listed files: **0 missing files and 0 digest mismatches**. This includes `build/main.pdf` and the three replacement figure PDFs. I read the snapshot's `AGENTS.md`, shared policy, author style profile, `main.tex` including its macros, and the included derivation and numerical sections. I inspected the actual rendered manuscript PDF, including page 27 (Figure 8 and scalar/tensor constitutive equations), page 29 (Figure 9), and page 30 (Figure 10), rather than relying only on source captions. The snapshot does not contain an executable `tools/agentctl`, so its routing command could not run; this did not prevent the requested source, manifest, and PDF review.

## Assessment

The replacement figures serve three distinct physical questions, and their descriptions support the stated conclusions.

- **Figure 8: which mechanism produces a pressure-induced shear reaction?** `sections/fabric_studies.tex:4–36` isolates volume–shape coupling from shape compliance alone. The angular dependence in equation (102), its sign reversal, the zero responses at coordinate-aligned fabric axes, and the coincident uncoupled/conformal curves agree with the rendered plot. The stiffness sweep demonstrates that zero coupling, rather than simply a stiff shape mode, controls the disappearance of the shear reaction. The positive-definite parameter domain is stated. This is a useful mechanistic result behind an isotropic mineral.
- **Figure 9: what is lost by using the mean scalar coefficient?** `sections/fabric_studies.tex:54–110` states the calibration and substitutes the scalar consistently in stress and mass. Holding stiffness, storage, and mobility fixed within each pair makes the comparison interpretable. The geometry, load ramp, side constraints, drainage, sampling location, and settlement definition are explicit. `build/insight/comparison_summary.tex` specifies the history norm, measured errors, refinement sensitivity, and end-of-run drainage. The plot supports modest but resolved differences, greatest in pressure. Neither the text nor the caption inflates these synthetic results into a general necessity for tensor coupling at every engineering tolerance.
- **Figure 10: how does finite internal-volume equilibration depart from the reference law?** `sections/fabric_studies.tex:117–179` defines a finite isochoric pure stretch, distinguishes oblique spatial components from noncoaxial constitutive states, and explicitly states the commuting restriction. Comparing both laws on the same logarithmic strain is particularly helpful. Subtracting the zero-pressure response exposes the pressure-induced shear and shape changes; the pore-volume panel demonstrates that fixed total volume does not fix the phase volumes. The stress-error map supports the claim that the reference linearization loses accuracy as pressure rises. The verification paragraph limits internal-Hessian positivity and work consistency to their demonstrated scope.

The constitutive assumptions enter before the new results: retained subspace, fixed relative orientation, synthetic isotropic mineral, positive distention block, and commuting finite specialization. The reference implementation is consistently distinguished from the finite material benchmark. The abstract and conclusions (`main.tex`, abstract and discussion beginning at line 592) reflect the mechanisms shown by the figures and preserve the limits on nonlinear finite-element verification and experimental validation. I found no unsupported escalation of the new numerical evidence in those summaries.

The rendered equations retain readable upright tensor glyphs, blackboard fourth-order tensors, and distinguish scalar shape variables from tensors. Figure captions identify the plotted quantities and comparison conventions; no clipping or broken mathematical reference was evident on the inspected pages.

## Required changes

None identified within this review's exposition, notation, and engineering-claim scope. This assessment is not a claim that every cited source was independently re-audited or that the numerical studies were rerun.

## Optional notes

**E1 — Preserve the physical flow by moving distant notation explanations closer to use.** Location: `main.tex:211–281`. The long discussion of bars, primes, hats, tildes, boundary data, and future distention quantities interrupts the otherwise clear transition from kinematics to phase mass. These conventions are explicit and internally explained, so this is not a correctness objection. A future editorial pass could keep the immediate density/stress conventions here and explain fabric-work and boundary-data notation in their own sections, consistent with the author profile's just-in-time principle.

**E2 — Improve the contrast of the third orientation.** Location: `sections/fabric_studies.tex:100–110`; rendered Figure 9, `build/main.pdf`, page 29. The yellow 90-degree curves and yellow reaction bars are readable on screen but noticeably lighter than the other series. A darker third color would improve grayscale and printed reproduction. The caption already supplies the solid/dashed model distinction.

**E3 — Add one sentence of interpretation after the history errors.** Location: `build/insight/comparison_summary.tex` as included at `sections/fabric_studies.tex:98`. The quantitative comparison is already adequate. An optional sentence could emphasize that, for these parameters and constraints, pressure is more sensitive to scalarization than settlement, while the shared drained stiffness explains the common long-time settlement within each pair. This would turn the clear measurements into an even more immediate engineering reading without broadening the claim.

ACCEPT
