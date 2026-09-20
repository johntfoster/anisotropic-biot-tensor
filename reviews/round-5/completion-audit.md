# Weighted-stress revision: completion audit

This revision responds to the September 19 user correction. It supersedes
the earlier assumed logarithmic spring model; prior review votes do not count.

| User requirement | Evidence and current assessment |
| --- | --- |
| Analyze companion instructions and skills first | Read companion AGENTS, author profile, canonical root/macros, and five pinned shared skills. Imported adapted guidance before manuscript rewriting; provenance/companion-guidance-transfer.md records scope and validation. |
| Bring relevant guidance here and update it | Root AGENTS and author_style_profile.md; five distinct biot- skills with original supporting scripts/checklist; focused profile routing and one-way harness links. No MOOSE/plasticity/website dependencies imported. |
| Follow volume-fraction-weighted stress | Main equations (5)–(9) start with current mineral/fluid stress weights; full tensor balance enters work cancellation. |
| Follow equivalent volumetric energy derivation | Main section 3 changes variables from skeleton/mineral volume to distention/true deformation; pressure work cancels. Section 4 integrates mineral work and calibrates distention from zero-pressure response. |
| Reconsider the anisotropic extension | Full mineral Hooke law plus spherical distention yields an explicit stiffness/compliance restriction. Arbitrary independent stiffness pairs are not represented. The full phase stress, rather than its trace alone, agrees with energy derivatives. |
| Minimize notation and use upright bold tensors | Removed the independent N, q coordinate, spring operators and reduced helper symbols from manuscript. All active tensor commands use mathbf, including Greek and fourth-order tensors. Unicode font rendering inspected. |
| Adopt author prose and avoid jargon | Whole article rewritten around physical purpose, equations, local definitions, and consequences. No draft-history narrative, spring terminology, or unexplained condensed operator terminology remains. Independent prose review requested. |
| Elasticity only | No plastic variables or evolution laws retained. Source plastic factors specialized to identity. |
| Durable goal and three-review loop | Active durable goal; three fresh reviewers assigned the identical round-5 source hashes with distinct scientific and author-rule scopes. Final verdicts must be assessed before completion. |
| Verification and PDF quality | Both current suites pass. 273 tensor states test full phase stress, energy/pressure/volume derivatives, rotations, and differing stress/strain directions. Additional random materials test work, compliance, reference limits, and finite unjacketed compression. Twelve-page PDF visually inspected; build has no unresolved references, missing glyphs, overfull/underfull warnings. |
| Source and citation evidence | Current companion files hashed; original Gajo 2010 equations inspected. Existing reference audit remains qualified by its documented full-text access limits. |
| Standalone and preserved user work | No companion modifications or commits. Existing shared-submodule and hook/configuration changes preserved. Complete build uses this repository only. Optional local LuaLaTeX package extraction repairs missing font support without global installation. |

The current model is restricted to spherical distention; the additional
compliance is spherical. Anisotropy due solely to pore shape in an isotropic
mineral requires a further deformation law. Synthetic tests are verification,
not material validation or a proof of global finite-strain stability.
