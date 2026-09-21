# Foster reviewer/editor cycle 2 — disposition (applied / declined)

## Applied

None. Cycle 2 made **zero** prose edits. The manuscript prose was found to be
clean after a fresh independent read; no high-value authorial/editorial change
remained that was not already settled or that would not constitute churn.

## Declined (no churn)

| # | Location | Proposed change | Reason declined |
|---|----------|-----------------|-----------------|
| 1 | sections/pore_fabric.tex `sec:fabric-equilibrium` | "…must be an isotropic scalar function of the fabric tensor, that is, depend only on…" → add a second "must" ("…that is, must depend only on…") | Valid elliptical parallel governed by the earlier "must"; the addition is clunky and adds no clarity. |
| 2 | sections/pore_fabric.tex `sec:fabric-energy` | "its spherical part carries the volume response and its deviatoric part the shape response" → add "carries" to the second clause | Already declined in cycle 1 (disposition #4); valid stylistic parallelism, not an error. Settled — not revisited. |
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
