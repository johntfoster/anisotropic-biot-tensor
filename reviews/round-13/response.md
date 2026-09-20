# Round-13 author response

## Verdicts on the frozen round-13 snapshot

Snapshot ID: `69a39ab45c1fbeed02118958391509d19d5c51fb2779cb278b366594ae38375c`
(340 files; all three reports independently verified
`sha256(source-manifest.json)` against `SNAPSHOT_ID` and re-hashed 340/340 files,
0 mismatch, 0 missing.)

| Reviewer | Charge | Verdict | Required corrections |
| --- | --- | --- | --- |
| 1 | mathematics and correctness | MINOR REVISION | none |
| 2 | physics/source fidelity + packaging | MINOR REVISION | none |
| 3 | prose, notation, consistency | MINOR REVISION | R1, R2 |

Not at least two exact ACCEPT, so no Foster reviewer/editor cycle started and the
source was changed; verdicts do not carry to the revised version.

## Substantiated required corrections and dispositions

**R3-R1 (published number not traceable).** `site/evidence.json` asserted "the C++
law matches the independent Python evaluation to about 6e-14 over 41 finite states"
while no listed artifact recorded that comparison, and the sentence was a
hard-coded literal in `tools/populate_site_manifest.py`.
*Disposition:* substantiated rather than deleted. The comparison report
(`.agent-runtime/.../implementation/constitutive/report.json`, `states = 41`,
`value_absolute_error = 6.394884621840902e-14`) is now packaged as the artifact
`cpp-python-constitutive` (`site/reports/cpp-python-constitutive.json`), listed in
the `implementation` category evidence, and the published sentence is generated
from that artifact — the generator fails loudly if the report is missing or was
not packaged, so the number can no longer drift from its evidence.

**R3-R2 (availability locator not resolvable).** The code-and-data availability
paragraph pointed readers at "the implementation runtime directory", the only
resolvable location of which is the git-ignored `.agent-runtime/` tree.
*Disposition:* the run evidence is now materialized at a repository-relative path
by `tools/materialize_fe_evidence.py` (38 cases; deck, provenance, per-run
analysis, scalar history, solver log; plus the convergence analysis and the
`compute_mms_order.py` recompute script; 206 files with SHA-256 digests in
`fe-evidence/manifest.json`). The availability paragraph now names
`fe-evidence/runs/`, `fe-evidence/mms-convergence.json`, `moose_app/`,
`validation/`, `figures/` and `site/evidence.json`, and states that
`site/evidence.json` records the inspected revision and pins the SHA-256 hashes of
the implementation and evidence files it reports. `provenance.note` in the
manifest now names the same repository-relative roots.

## Minor findings addressed in the same pass

- "force_relative of order 1e-10 or smaller" (reviewers 1 and 3): now names the
  measured bound (at most about 2.1e-10; largest 2.052e-10, `partial_30`).
- "the six rotated-anisotropy runs" (reviewer 3): now names the orientation set
  (0, 30 coarse and fine, 45, 90 degrees).
- Temporal-order wording (reviewer 1): the difference method cancels a
  time-step-independent mesh floor exactly, so the departure from first order is a
  mesh-step cross term; the nx=32 values are now named alongside nx=64 and no
  order above one is claimed.
- `plot-manifest.json` declared 66 output and 149 input hashes that do not resolve
  (reviewers 1 and 2): the package no longer ships that internal generator record;
  it was cited by nothing in the manuscript or the published manifest.
- `run.log` declared with a SHA-256 in each `provenance.json` but absent from the
  package (reviewer 1): shipped, and `tools/materialize_fe_evidence.py` refuses to
  complete if any declared digest does not resolve.
- `conformal-verification.json` recorded `source_sha256` under bare basenames
  (reviewer 2): `examples/verify_conformal.py` now records repository-relative
  paths and the report was regenerated (186 checks / 67 legacy identities /
  2.4549890331732928e-09, values unchanged).
- Build residue `main.x86_64-conda-linux-gnu.opt.lo.d` (reviewer 2): excluded by
  the snapshot builder.
- `README.md`/`AGENTS.md` referenced `reviews/`, `agent_local/`,
  `references/notes/`, `.agent/shared/` (reviewer 2): the snapshot builder now
  carries `reviews/README.md` (policy only, never a round directory, so reviewers
  still cannot read prior reports or votes), `agent_local/**`,
  `references/notes/**`, `.agent/shared/AGENTS.shared.md` and
  `.agent/shared/skills/**`, so every reference in the shipped documents resolves.
- `site/README.md` still described `evidence.json` as "the complete pending
  example" (reviewer 3): reworded to describe the manifest's status semantics.
- `provenance.source_revision` (reviewer 2, optional): the note now states that the
  pinned review snapshot is the authoritative frozen artifact.

No numerical result, kernel, or verification claim changed: the changes are
packaging, availability wording, manifest traceability, and generator fixes.
Rebuilt `build/main.pdf` (22 pages, no undefined references) and regenerated the
site (22 artifacts, link check passed).

## Round-14

New frozen snapshot `061a92feee93641668978ab0ecec033d0b9fe0d20ad74efbcb9ec0bf1a60ea69`
(441 files, 0 missing, 0 mismatch). Three fresh independent reviewers were launched
on it; reports go to `reviews/round-14/reviewer-{1,2,3}.md`.
