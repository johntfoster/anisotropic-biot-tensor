# Round 25 — launched (step-8 fresh independent re-review)

Fresh independent re-review of the **revised post-Foster-cycle tree** for the
anisotropic pore-fabric extension.

Snapshot: `.agent-runtime/review-snapshots/round-25`
SNAPSHOT_ID: `5035dd198266c12544140e47381da3e9390c7d1e68c00a06009e85ba6052f9dd`
Files: 591

## Why round 24 does not count here

Round 24 (SNAPSHOT_ID `1dea9e12…b423`) returned 2 exact ACCEPT + 1 MINOR REVISION and
therefore met the step-6 acceptance threshold. After that round the tree changed under
the three Foster review/edit cycles (step 7), so no round-24 vote carries forward to the
revised tree. This round is the step-8 fresh independent re-review required by the
pipeline; counting only exact ACCEPT verdicts on the round-25 snapshot; >=2 required.

## What changed since round 24 (Foster cycles 1–3)

| Cycle | Edit |
|-------|------|
| 1 | `main.tex` conclusions: "transverse-isotropic" → "transversely isotropic" |
| 2 | `R24-3-1` repair, two places: the reported shape scalar is now described as the logarithm of the unimodular **transverse** fabric eigenvalue \(h=\mathrm{e}^{\ln h}\) — in `sections/pore_fabric.tex` (`sec:fabric-transverse`) and in the `fig:fe-fabric-probe` caption in `sections/finite_elements.tex`. The phrase "eigenvalue ratio" no longer occurs. |
| 3 | none (final read; prose clean) |

Prose/terminology only: no equation, symbol, label, citation, number, or claim changed;
per-file `\label`/`\ref`/`\cref`/`\eqref`/`\cite`/`\begin{equation}`/`\begin{align}`
counts and per-file digit-literal multisets preserved; `build/main.pdf` rebuilt at 33
pages with 0 undefined references/citations and 0 overfull boxes
(sha256 `12fc90c48010be3ebcc8462de0c2cdd374ac1cab7d7126890c8c4f93ac1ad8ad`).

## Watcher pre-launch verification (read-only)

- `sha256(source-manifest.json)` = `5035dd198266c12544140e47381da3e9390c7d1e68c00a06009e85ba6052f9dd`,
  identical to the declared SNAPSHOT_ID; 591 manifest entries; `missing []`.
- No writer process active in the repository at launch time (checked `ps`).
- Snapshot frozen immediately after Foster cycle 3, with zero writer activity between
  the cycle-3 build and the freeze.

## Rules for this round

- Prior rounds (18–24) reviewed earlier snapshots and do not carry forward.
- Counting only exact ACCEPT verdicts on the round-25 snapshot; >=2 required.
- Three fresh independent reviewers, complementary emphasis:
  (1) mathematics/correctness; (2) physics/source fidelity/packaging;
  (3) prose/notation/significance.
- Reviewers must not read other reviewers' reports or prior-round verdicts, and must not
  modify the snapshot or the working tree (work from a temporary copy).
- Reports: `reviews/round-25/reviewer-{1,2,3}.md`, each ending with a
  `VERDICT:` line.

## Specific focus for this round

Confirm independently that (a) the round-25 snapshot is self-consistent and every
manifest entry re-hashes; (b) the two Foster-cycle edits are present and are prose-only,
introducing no change to any equation, number, label, citation, or claim; (c) the
`R24-3-1` defect is genuinely closed — `ln h` is nowhere described as an eigenvalue
ratio, and the description is consistent with `eq:fabric-transverse-h`; (d) every
quoted number in the manuscript still reproduces from the frozen `fe-evidence/` artifacts
and the supplied verification scripts.
