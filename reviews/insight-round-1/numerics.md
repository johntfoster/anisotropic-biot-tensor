# Independent numerical and reproducibility review

This is simulated AI peer review, not journal acceptance. The review is confined to the immutable `insight-round-1` snapshot; locations below are relative to its root. No other review or earlier acceptance result was consulted.

## Snapshot identity and scope

Declared snapshot: `a5289ef83d1b55941719abcd663ad6792debdf728698e833c9f99d998174d18f`.

The SHA-256 digest of `source-manifest.json` equals both that identifier and `SNAPSHOT_ID`. I re-hashed all **713** listed files: **zero missing files and zero mismatches**. I read `AGENTS.md`, the shared instructions, `author_style_profile.md`, the manuscript root and numerical sections, relevant constitutive/FE sources, and the acceptance-cycle instructions. I inspected the rendered new figures and adjacent text on PDF pages 27, 29, and 30.

I extracted the PDF's embedded `anisotropic-biot-2026-09-22-v3.zip` using `pdfdetach`. All **129** payload entries in its manifest have the stated hashes. Reproduction was performed only in a writable scratch extraction, using NumPy 2.2.6 and SciPy 1.15.3. The snapshot was not modified.

## Numerical assessment

The following commands completed successfully from the extracted supplement:

- `python3 examples/weighted_stress.py`
- `python3 examples/verify_reconstruction.py`
- `python3 examples/verify_tensor.py`
- `python3 examples/verify_conformal.py`
- `python3 examples/verify_fabric.py`
- `python3 examples/fabric_insight.py`
- `python3 examples/plot_fabric_comparison.py`
- `python3 tools/verify_scalar_probe.py --analyze-only`

The conformal verification reproduces 186 checks and a maximum constitutive identity error of `2.4549890331732928e-9`; the separate tensor suite reproduces 273 states. These support the corresponding statements in `sections/experiments.tex`.

For the new commuting finite benchmark, `examples/fabric_insight.py:125–181` differentiates the unreduced spectral energy in every deformation-gradient entry and pushes the resulting Piola tensor to spatial stress. It therefore checks the complete spatial tensor, rather than merely the mineral-volume equation or stress trace. The reproduced maximum stress discrepancy is `1.0380576488107994e-8`, the pressure-tangent discrepancy `1.2532076199130091e-11`, and the independently minimized internal-state discrepancy `1.0580925826936963e-8`. Joint pressure/deformation reduction produces orders `1.998944855`, `1.999472044`, and `1.999735926`. These agree with the rounded manuscript claims. The off-diagonal stress is nonzero in the oblique coordinate frame. This is still a commuting-family check: evaluating the candidate energy in neighboring perturbations does not establish a general noncoaxial physical law. The manuscript makes this restriction explicit, including the retained internal subspace and the distinction between internal Hessian positivity and full deformation stability.

For consolidation, the deck and overrides agree with the stated strip geometry, zero initial state, traction ramp, drainage boundary, two mesh/time levels, material parameters, and orientation pairs. In `moose_app/src/materials/FabricMaterial.C:95–106`, the scalar replacement is applied consistently to stress and fluid mass. The drained stiffness, storage, and mobility are preserved. The independent recorded probe agrees within `3.18e-14` over its reported stress, mass, and stiffness outputs.

The reproduced relative history errors are 1.1264–3.2031% for pressure, 0.2593–0.8764% for settlement, and 0.6498–0.9813% for lateral reaction. The maximum joint-refinement differences are 0.3669%, 0.0515%, and 0.1146%, respectively. The manuscript's rounding and norm definitions are accurate. The two-level comparison is expressly a combined spatial/temporal sensitivity measurement, not an order estimate or independent error bound. No stronger convergence claim is needed for the stated comparison.

The end-step accumulation of the boundary pressure residual reproduces maximum relative mass discrepancy `2.2837915118209887e-11`. This is algebraic discrete conservation, not independent verification of the boundary gradient flux; the manuscript distinguishes those quantities. Maximum final-to-peak pressure is `0.003479553`, consistent with the quoted 0.35%. The recorded source and history hashes pass the analysis driver. I did not rebuild MOOSE or rerun its transient suite, so my compiled-result assessment is based on the archived runs, independent Python recomputation, and source inspection.

The three new figures are legible, have correctly described quantities and units, and agree with the regenerated data. Their captions preserve the material-point/reference-FE distinction and synthetic-parameter scope.

## Required corrections

None identified within this numerical/source-fidelity review.

## Optional notes

**N1 — Broaden the compiled scalar probe.** `tools/verify_scalar_probe.py:49–65` checks two normal stresses and mass but does not compare the shear stress or use a nonzero imposed shear strain. Adding those outputs and a shear state would make this regression particularly sensitive to an omitted off-diagonal scalar substitution. The present implementation applies the complete tensor correction, so this is additional test coverage rather than a demonstrated scientific error.

**N2 — Clarify diagnostic energy in the scalar branch.** `moose_app/src/materials/FabricMaterial.C:95–114` changes stress and mass while retaining the parent law's `energy` output. The source already disclaims interpreting internal fabric outputs as scalar-model microstructure. Extending that diagnostic disclaimer to energy, or exporting the scalar comparison's own potential, would prevent future consumers from treating this unused diagnostic as the scalar model's thermodynamic energy. The reported plots and conservation calculations do not use that output.

**N3 — Correct the supplement command-count sentence.** `tools/package_numerical_supplement.py:117` generates the README sentence saying the three new studies are regenerated by the “last two commands.” The figure-producing commands are `fabric_insight.py` and `plot_fabric_comparison.py`; `verify_scalar_probe.py --analyze-only` follows them. Name the commands directly. The complete command list is present and worked as written, so this wording did not block reproduction.

ACCEPT
