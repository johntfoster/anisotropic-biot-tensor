# Foster reviewer/editor cycle 3 — disposition (applied / declined)

## Applied

None. Cycle 3 made **zero** prose edits. This is the third and final cycle;
the manuscript prose was found clean after a fresh independent read, and no
high-value authorial/editorial change remained that was not already settled by
cycle 1 or cycle 2 or that would not constitute churn.

## Declined (no churn)

| # | Location | Proposed change | Reason declined |
|---|----------|-----------------|-----------------|
| 1 | sections/pore_fabric.tex `sec:fabric-equilibrium` | "…must be an isotropic scalar function of the fabric tensor, that is, depend only on…" → add a second "must" | Already declined in cycle 2; valid elliptical parallel governed by the earlier "must". Settled — not revisited. |
| 2 | sections/pore_fabric.tex `sec:fabric-energy` | "its spherical part carries the volume response and its deviatoric part the shape response" → add "carries" | Already declined in cycle 1 (disposition #4); valid stylistic parallelism. Settled — not revisited. |
| 3 | sections/finite_elements.tex `sec:fe-fabric` | Condense the twice-stated "implementation check, not independent derivation" caveat | Already declined in cycle 1 (disposition #1); the two statements scope different checks. Settled — not revisited. |
| 4 | main.tex (abstract) | Rewrite the triple-"and" scope sentence | Already declined in cycle 1 (disposition #2); claim-bearing scope statement. Settled — not revisited. |
| 5 | sections/experiments.tex | Convert `Figure~\ref{fig:…}` to `\Cref{fig:…}` for style consistency | Already declined in cycle 1 (disposition #3); would change `\ref`/`\cref` counts. Settled — not revisited. |
| 6 | all seven sources | Strip pre-existing trailing whitespace on wrap-indented lines | Out of scope; pure churn; would touch unchanged lines. |

## Standing decision check (no action, confirmed)

`sec:fabric-transverse` names the volume--axial distention modulus as the
carrier of `B_par != B_per`; an isotropic mineral alone keeps `B` spherical.
Abstract, conclusions, `sec:fe-fabric`, and the fabric figure captions are all
consistent with this confirmed wording. Nothing was reverted or changed.

## Integrity

- sha256 of all seven manuscript sources: **byte-identical** before and after
  this cycle (0/7 differ) — see snapshot-hash-table.txt.
- `\label`/`\ref`/`\cref`/`\eqref`/`\cite`/`\begin{equation}`/`\begin{align}`
  counts: unchanged (no edits made).
- Digit-literal multiset: unchanged per file (no edits made).
