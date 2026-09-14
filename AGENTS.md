# AGENTS.md

## Shared workflow dependency

- This paper repository is the primary context. Read
  `.agent/shared/AGENTS.shared.md`; local scientific instructions in this file
  override shared workflow defaults.
- The reusable core is pinned as the `.agent/shared` Git submodule. Route work
  with `tools/agentctl route "<task>"`; shared skills are canonical under
  `.agent/shared/skills/`, and paper-specific skills belong under
  `agent_local/skills/` with distinct names.
- Do not inspect sibling paper repositories unless John explicitly requests it
  or `research-dependencies.yml` declares the exact pinned source needed.

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
  `.agent/shared/skills/commit/SKILL.md`.
- Draft the commit body from recoverable session history before writing its
  header. Use the sections `Summary`, `What changed & why`, `Alternatives
  considered`, `Dead ends & backtracks`, `Open questions`, and `Next steps`.
- In `Summary`, record the AI model or models and sanitized, non-secret session
  identifier or identifiers that contributed to the commit. The hooks reject
  ordinary commits that omit either field or substitute an unknown placeholder.
- Install tracked hooks after every fresh clone or worktree with
  `tools/agentctl hooks install`.

## Agent skill registration

- Canonical shared skills live in `.agent/shared/skills/<name>/SKILL.md`.
- `agent-profile.json` maps each harness to its skill
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
- Do not describe a calibration as "matched." State the condition it enforces
  or the quantities it is calibrated to reproduce.
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
