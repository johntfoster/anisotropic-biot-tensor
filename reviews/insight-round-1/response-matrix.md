# Round 1 response matrix

Simulated AI peer review of snapshot `a5289ef83d1b55941719abcd663ad6792debdf728698e833c9f99d998174d18f`.
The unchanged reports return two ACCEPTs and one MINOR REVISION. The demonstrated implementation defect requires a new scientific snapshot; those votes do not apply to the revised candidate.

| ID | Disposition and evidence | Verification |
|---|---|---|
| D1 | Corrected `FabricLaw.h` to use the general compliance contraction for solid storage, including anisotropic minerals. Added two compiled anisotropic pressure probes and independent retained-equilibrium calculation. | Expected solid storage 0.030090340364165323; pressure differentiation of mineral volume and mass agree within 1.5e-11. All coupled runs are regenerated with the corrected executable. |
| D2 | Confirmed finding; conformal phase-work derivation retained. | Independent reviewer checked normalization and full tensor balance. |
| D3 | Confirmed finding; commuting restriction retained explicitly. | No general noncoaxial finite-law claim introduced. |
| D4 | Confirmed finding; full spatial derivative and pressure checks retained. | Independent reviewer reproduced the finite checks with a separate tensor calculation. |
| D5 | Confirmed finding; reciprocal scalar substitution and scope retained. | Compiled scalar/tensor checks still agree within 3.2e-14. |
| N1 | Deferred optional shear-probe expansion. The source correction acts on every tensor entry; the current independent material and finite checks address full tensor response. A compiled prescribed-shear regression would add coverage, but no defect was demonstrated. | No claim that the compiled scalar probe checks shear has been added. |
| N2 | Extended the source comment to state that both internal fabric and energy diagnostics retain the parent law and are not scalar-model states or energy. | Reported comparison uses stress, mass, displacement and reaction, not these diagnostics. |
| N3 | Named the two figure-generating commands explicitly in the supplement README template. | Package regenerated from the corrected template. |
| E1 | Deferred manuscript-wide relocation of notation. The conventions are explicit and the reviewer found no correctness defect; moving this material would broaden the requested numerical revision. | Local new-study definitions remain close to use. |
| E2 | Darkened the third Figure 9 series and reaction bars to improve contrast. | Regenerated figure and PDF page inspected. |
| E3 | Added a local interpretation: pressure is more sensitive than settlement for these cases; common drained stiffness gives the same fully drained settlement within each pair. | Consistent with measured histories and the pressure-free limit of the two displayed laws. |

The next round reviews all revised sources, regenerated evidence, supplement and PDF together. Final command outcomes are recorded with the new snapshot.
