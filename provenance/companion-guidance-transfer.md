# Companion guidance transfer — 2026-09-19

John requested analysis and adaptation of the companion repository's agent
instructions and skills before reconsidering the derivation. The companion
AGENTS.md, canonical root and macros, and author profile were read directly.
Its shared checkout is empty, but the five relevant skill sources and their
supporting scripts/checklist were recovered read-only from local submodule
Git objects at commit `46b234fb6ad30d5620decd9d02ed7b9050a1088d`.

The local `biot-` skills adapt derivation auditing, notation propagation,
narrative review, display normalization, and manuscript recompilation.
Their source is `skills/<original-name>/` at that pinned commit. Paths and
local requirements were adapted; original shared files were not changed.
`author_style_profile.md` adapts the companion's 2026-07-27 profile (revised
July 28), omitting external sample paths and unrelated implementation rules.
The user's September 19 tensor-typography instruction overrides the Greek
bold-symbol convention still used by the companion source.

Root instructions now enforce minimal notation, upright bold tensors,
physical explanation, current-volume stress weighting, reference-volume
energy factors, and separate verification of the tensor balance and trace.
MOOSE synchronization, plasticity, website synchronization, and unrelated
commit workflows were not imported into this elasticity-only paper.

The shared submodule worktree and pre-existing hook/configuration changes
were preserved. `tools/agentctl` is still unavailable through its worktree
symlink. Adapted skills can be read directly and are linked in each configured
harness discovery directory. No companion files were edited.

## Validation

All five adapted skill directories pass the skill frontmatter validator.
Their derivation and display scanners ran on the current compilation graph.
Flagged equals signs occur in separate definitions or held-fixed state sets;
none is a compressed multistep derivation. The local author profile and
root instruction changes were applied before manuscript rewriting. The
current round-5 snapshot includes both guidance files for reviewer inspection.

The missing LuaLaTeX font support was supplied by unpacking the platform
`texlive-luatex` package into ignored runtime storage. No global package was
installed. A scoped provisioning helper and `.latexmkrc` fallback preserve
the standard manuscript build command. The dependency checker now verifies
LuaLaTeX support rather than only the availability of pdfLaTeX and BibTeX.
