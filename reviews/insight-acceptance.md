# Numerical-study revision: completion record

This is simulated AI peer review, not journal acceptance.

The revision replaces Figures 8–10 with pressure-induced shear and a modulus sweep, coupled scalar/tensor consolidation through drainage, and a finite commuting pure-shear material study. It corrects general anisotropic solid storage in the compiled fabric law and tests the correction against pressure derivatives of mineral volume and mass.

The accepted immutable snapshot is `8510407b6e10e12baf9d9695d639ca887f63513a2dfa097851d2f1cbcd072f36` (718 files). All three fresh reviewers independently verified its complete manifest and returned exactly ACCEPT:

- [Derivation](insight-round-2/derivation.md)
- [Numerics](insight-round-2/numerics.md)
- [Exposition](insight-round-2/exposition.md)
- [Comment dispositions](insight-round-2/response-matrix.md)

The first round and its resolved storage finding remain in `insight-round-1/`. Three subsequent Foster cycles assessed physical purpose, local definitions/figures, and abstract/conclusion integration. Their memos and structural audits are in `insight-foster/`. They made no source changes. Every accepted source, scientific artifact and PDF remains byte-identical; acceptance-cycle step 8 therefore preserves the fresh round-2 acceptance without another round.

Validation includes twelve successful corrected MOOSE consolidation runs, four compiled constitutive probes, independent finite spatial-stress/pressure checks, all figure manifests, the configured LuaLaTeX build and visual page inspection, and the local companion site's artifact-link check. The updated embedded supplement has 133 verified payload files. Its Python reproduction recreates all five new CSVs byte-for-byte. Independent numerical review also reproduced nine analysis commands. The finite fabric evidence remains restricted to commuting states; no general noncoaxial finite law or experimental validation is claimed.

Delivery target: the workspace artifact `build/main.pdf`, linked in the conversation. No commit, deployment or external message was requested or performed.

PDF SHA-256: `91971dade2d2096d3a705c720b375a1ca0ea32e611240aa9a4815fc87f8063e2`.
