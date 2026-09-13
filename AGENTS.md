# AGENTS.md

## Portable agent environment

- Treat this file as the sole universal entry point for agent work.
- Resolve every operational path from this repository root. Do not record user
  home directories, sibling-repository paths, or machine-specific locations in
  tracked files.
- At the first relevant query, run `tools/agentctl route "<query>"` and use
  the smallest applicable skill and dependency profile.
- Keep generated environments, LaTeX output, caches, and run data in ignored
  runtime directories. Commit source, references, instructions, and intended
  publication artifacts only.

## Commit messages as process logs

- For every request to create a commit, use
  `agent_environment/skills/commit/SKILL.md`.
- Draft the commit body from recoverable session history before writing its
  header. Use the sections `Summary`, `What changed & why`, `Alternatives
  considered`, `Dead ends & backtracks`, `Open questions`, and `Next steps`.
- Install tracked hooks after every fresh clone or worktree with
  `tools/agentctl hooks install`.

## Agent skill registration

- Canonical skills live in `agent_environment/skills/<name>/SKILL.md`.
- `agent_environment/dependencies.json` maps each harness to its skill
  discovery directory. Re-register the one-way skill links after a fresh clone
  or when switching harnesses.

## Project scope

- Read `VISION.md` and check `git status --short` before editing.
- This repository owns a self-contained theoretical paper on an anisotropic
  finite-deformation Biot tensor for one deformable solid and one fluid.
- The canonical manuscript root is `main.tex`; `references.bib` is its sole
  bibliography. There is no dependency on the parent nonlinear-Biot repository.

## Manuscript editing and build

- Preserve TeX semantics, equation labels, citations, and the distinction
  between finite-deformation kinematics and the small-strain stiffness-tensor
  specialization.
- Number and descriptively label every displayed equation introduced by an
  agent. Use `align` for multi-step derivations.
- Verify citation-backed claims against the cited full text. Keep PDFs under
  `references/pdfs/`, notes under `references/notes/`, and retrieval state in
  `.agent-runtime/research/`.
- After every source edit, run

  ```sh
  latexmk -lualatex -interaction=nonstopmode -halt-on-error \
    -outdir=build main.tex
  ```

- Inspect warnings and affected pages. Generated output belongs only in
  `build/` and is never committed.
- Run `tools/agentctl check --profile manuscript` for manuscript tooling and
  the smallest focused validation appropriate to the change.
