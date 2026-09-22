# Independent simulated AI peer review: numerical evidence and source fidelity

Candidate: `insight-round-2`.
Snapshot: `8510407b6e10e12baf9d9695d639ca887f63513a2dfa097851d2f1cbcd072f36`.

This is simulated AI peer review, not journal acceptance. I reviewed this frozen candidate independently without reading earlier reports or acceptance counts. Scientific sources were read from the frozen candidate; numerical reproduction used a separate writable extraction of its embedded supplement. No scientific source was edited.

## Integrity and scope

The SHA-256 digest of `source-manifest.json`, the declared identifier, and `SNAPSHOT_ID` agree exactly. I independently rehashed **all 718 listed files**: no missing files or mismatches. I extracted the ZIP attachment directly from `build/main.pdf` using `pdfdetach`, unpacked it into `.agent-runtime/insight-r2-numerics/payload`, and independently checked **all 133 payload-manifest entries** before executing any scripts: no mismatches.

I read the main manuscript macros and relevant constitutive and numerical sections, the author profile and acceptance-cycle requirements, the finite material driver, reference fabric implementation, scalar-substitution implementation, comparison input and run/analysis scripts, and archived probe provenance. I rendered the actual manuscript PDF and visually inspected Figures 8, 9 and 10 on pages 27, 29 and 30. Their panels, units, legends and captions are legible and consistent with the plotted data and stated scope.

I reran the following from the extracted archive, using Python 3.10.12, NumPy 2.2.6, SciPy 1.15.3 and Matplotlib 3.10.8. Every command returned exit status zero:

- `python3 examples/weighted_stress.py`
- `python3 examples/verify_reconstruction.py`
- `python3 examples/verify_tensor.py`
- `python3 examples/verify_conformal.py`
- `python3 examples/conformal_experiments.py`
- `python3 examples/verify_fabric.py`
- `python3 examples/fabric_insight.py`
- `python3 examples/plot_fabric_comparison.py`
- `python3 tools/verify_scalar_probe.py --analyze-only`

Logs and regenerated artifacts remain in the isolated scratch directory. I did not rebuild MOOSE or rerun its coupled solves. Consequently the material Python calculations are fresh calculations; compiled constitutive probes and coupled histories are independent reanalyses of the archived runs, including their source/hash checks. I did not perform a full external-literature audit or establish experimental validity.

## Required changes

None.

## Findings and optional notes

**N1 — Verified: reciprocal scalar comparison and anisotropic storage.** Locations: `sections/fabric_studies.tex`, subsection “Consolidation with tensor and scalar pressure coupling”; `moose_app/src/materials/FabricMaterial.C::computeQpProperties`; `moose_app/include/utils/FabricLaw.h`; `tools/verify_scalar_probe.py`. The scalar replacement changes both stress and fluid mass with consistent signs. The storage expression uses the full mineral compliance, and its independent retained-subspace expression agrees with pressure differences of archived compiled mineral volume and fluid mass for the anisotropic stiffness case. The expected solid storage is 0.030090340364165323; the two independent archived derivatives are 0.030090340349397948 and 0.030090340350034953. Their absolute errors are below 1.5e-11. Tensor/scalar probe comparisons reproduce stress, mass and selected drained stiffness entries to a maximum absolute discrepancy of 3.18e-14. The regenerated probe report is byte-identical to the frozen report. The manuscript correctly excludes phenomenological scalar internal variables from mineral-volume interpretation. No change requested.

**N2 — Verified: coupled comparison claims and evidence category.** Locations: Figure 9; `build/insight/comparison_summary.tex`; `examples/plot_fabric_comparison.py`; `fe-evidence/insight/*/provenance.json`. The reanalysis verifies source/history hashes for the twelve archived runs and independently reconstructs the time-integrated error and conservation quantities. Pressure, settlement and reaction errors reproduce the reported 1.13–3.20%, 0.26–0.88% and 0.65–0.98% ranges. Joint space/time sensitivity, drainage completion and the 2.3e-11 conservation discrepancy reproduce exactly. The regenerated verification JSON, summary TeX and error CSV are byte-identical to the frozen artifacts. The text explicitly calls the two-level comparison a sensitivity measurement rather than an asymptotic convergence result. The error separation supports the stated comparison for these parameters, without establishing an unknown exact coupled solution. No change requested.

**N3 — Verified: finite commuting benchmark and physical limits.** Locations: Figure 10; `sections/fabric_studies.tex`, final subsection; `examples/fabric_insight.py::finite`, `candidate_energy`, `verify`. The finite calculation solves both retained internal strains with exact exponential mineral volume. Its independent spectral-energy differences perturb all nine deformation-gradient components at commuting base states, while pressure increments re-solve the internal equilibrium. These checks reproduce the reported maximum spatial-stress error 1.0381e-8, pressure-tangent error 1.2532e-11, minimization state error 1.0581e-8, and reference-limit orders 1.9989–1.9997. The generated finite CSVs and verification report are byte-identical to the frozen versions. The plotted domain has positive phase volumes and positive internal Hessians. The text properly limits this evidence to internal equilibrium and work consistency on the commuting family; it does not extrapolate the spectral candidate's derivative check into a verified noncoaxial finite constitutive theory. No change requested.

**N4 — Verified: pressure-induced shear mechanism.** Locations: Figure 8; `sections/fabric_studies.tex`, first subsection; `examples/fabric_insight.py::coefficients`. The eliminated-strain reaction check agrees with the Biot expression, and the modulus sweep enforces positive definiteness. Angle reversal, the maximum at 45 degrees and vanishing shear for zero volume–shape coupling are visible in the actual PDF and reproduced by the archive. The uncoupled and conformal curves coincide as the caption states. Both angular and modulus-sweep CSVs reproduce byte-for-byte. No change requested.

**N5 — Optional documentation clarity.** Location: embedded supplement `README.md`, opening paragraph. Its opening description still emphasizes “conformal constitutive results” and says the models are “not ... finite-element simulations,” before immediately explaining that finite-element histories are also bundled. The subsequent instructions accurately distinguish Python calculations, archived coupled results and fresh MOOSE reproduction, so reproduction is not blocked. An optional future cleanup could describe the three evidence categories together in the opening paragraph. This is editorial and does not affect the numerical findings or verdict.

The numerical evidence supports the manuscript's bounded claims, and the embedded supplement reproduces the inspected numerical artifacts without the source checkout. Remaining limitations are stated in the manuscript and above.

ACCEPT
