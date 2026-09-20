# Requirement-by-requirement final audit

This audit concerns the stress-reconstruction revision, not the obsolete
round-2 acceptance. Source identities are in `source-sha256.txt`.

| Requirement | Current authoritative evidence | Assessment |
| --- | --- | --- |
| Use the companion stress-based derivation | Source elastic derivation inspected and hashed in `references/notes/stress-reconstruction-progress.md`; companion manuscript cited as `foster2026poroplastic`; scalar equations `eq:reconstructed-isotropic-source-eos` and `eq:reconstructed-isotropic-source-biot` independently tested | Satisfied for the scalar elastic volumetric construction; the source's separate neo-Hookean shear law is not claimed recovered |
| Reconstruct a compatible anisotropic tensor from logarithmic skeleton/mineral Hooke laws | `sections/stress_reconstruction.tex`: prescribed stress laws, explicit series assumption, compliance-difference stiffness, mineral shape relaxation, scalar condensation, objective tensor and total stress | Satisfied as a specified objective internal-strain elastic construction; not a unique localization theorem from two moduli alone |
| Elasticity only | No plastic state or flow law in reconstructed energy/equilibrium; source plastic material excluded; limitations distinguish possible future inelasticity | Satisfied |
| Compatibility and finite/reference distinction | Exact drained generalized Hooke law, full tensor modulus ordering, finite homogeneous unjacketed path, classical reference stress/storage, noncoaxial logarithmic push-forward, phase-average vs internal stress distinction | Satisfied within explicitly stated series assumption and admissible branch |
| Review all new source references | Original 23-key inventory in runtime research cache; every key accounted for in `references/notes/new-source-references-2026-09-18.md`; verified new citations and disclosed exclusions/access limits | Every entry reviewed at its stated evidence level; original full-text access is incomplete and exhaustive priority verification is not claimed |
| Revise paper with new results | New central reconstruction section, rewritten abstract and narrative, examples tied to reconstruction, restricted earlier model identified as comparison, updated README/VISION | Satisfied |
| Launch three JMPS reviewer agents and improve in a loop | Round 3 reports: ACCEPT / MINOR REVISION / MINOR REVISION; all required corrections and one optional mathematical clarification implemented; round-3 response describes evidence | Satisfied |
| At least two ACCEPT verdicts on current version | Round 4 reports, matched to current hashes, with reviewer-specific findings retained | Satisfied: all three independently returned ACCEPT; all reports assessed and all ten source hashes verified; no mandatory revisions remain |
| Build after edits and inspect affected pages | Required LuaLaTeX latexmk command passes; all 24 pages rendered and contact sheets inspected; new derivation and changed example/conclusion pages also inspected at readable resolution | Satisfied; four benign underfull warnings, no overfull boxes, undefined citations, or broken references |
| Focused numerical verification | Both `verify_reconstruction.py` and `verify_tensor.py` pass; reconstruction includes independent full six-coordinate minimization and noncommuting elastic tensors | Satisfied; sampled tests do not prove global ellipticity |
| Labels/citations and clean source formatting | 135 unique labels; internal references resolve; 16 citation keys resolve; new displays numbered; `git diff --check` passes | Satisfied |
| Repository tooling check | `tools/agentctl route` and `tools/agentctl check --profile manuscript` attempted but unavailable due to pre-existing missing shared submodule target; direct `tools/check_dependency_profile.py manuscript` passes | Scientific checks completed via direct commands; shared-workflow infrastructure remains unavailable and is disclosed |
| Preserve user work and standalone build | No source sibling edits, no commits, no changes to pre-existing hook/submodule/configuration edits; build uses only this repository; generated outputs in ignored build/runtime directories | Satisfied |

The reference access limits and phase-average localization limitation are
material qualifications of the result, not hidden assertions of work completed
without evidence. No actual journal acceptance, experimental validation, or
full noncoaxial microscopic phase localization is claimed.
