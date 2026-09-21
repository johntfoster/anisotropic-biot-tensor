# Foster reviewer/editor cycle 3 (final, round-27 tree) — disposition (applied / declined)

## Applied

None. This is the final editorial cycle, run against the current (round-27)
tree. A fresh cold read found no high-value authorial/editorial improvement
that was not already settled by the earlier cycles or that would not
constitute churn. A zero-edit outcome is legitimate and recorded as such.

## Declined (no churn; settled decisions not revisited)

| # | Location | Item | Reason declined |
|---|----------|------|-----------------|
| 1 | sections/finite_elements.tex | US/UK spelling mix (`center-pressure`/`Center` vs `centre-pressure`/`Centre`, `colour`, `modelling` vs `modeling`) | Settled in cycle 1; purely cosmetic, no author US/UK convention. Not revisited. |
| 2 | sections/finite_elements.tex `sec:fe-fabric` | Condense the twice-stated "implementation check, not an independent derivation" caveat | Settled in cycle 1; the two statements scope different checks and touch numeric thresholds. Not revisited. |
| 3 | sections/pore_fabric.tex `sec:fabric-energy` | "its spherical part carries the volume response and its deviatoric part the shape response" → add "carries" | Settled (cycle 1 #4); valid stylistic parallelism. Not revisited. |
| 4 | sections/pore_fabric.tex `sec:fabric-equilibrium` | "…that is, depend only on…" → add a second "must" | Settled (cycle 2); valid elliptical parallel. Not revisited. |
| 5 | main.tex (introduction) | Smooth the trailing "and at small strain" qualifier | Settled (cycle 1); claim-scoping. Not revisited. |
| 6 | main.tex (abstract) | Rewrite the triple-"and" scope sentence | Settled (cycle 1); claim-bearing scope statement. Not revisited. |
| 7 | sections/experiments.tex | Convert `Figure~\ref{…}` to `\Cref{…}` | Settled (cycle 1); would change `\ref`/`\cref` counts. Not revisited. |
| 8 | all seven sources | Strip pre-existing trailing/alignment whitespace | Settled; pure churn. The single non-leading double-space is column alignment inside a math `cases` block, not prose. |

## Standing decision check (no action, confirmed)

`sec:fabric-transverse` names the volume--axial distention modulus as the
carrier of `B_par != B_per`; an isotropic mineral alone keeps `B` spherical.
Abstract, conclusions, `sec:fe-fabric`, and the fabric figure captions are all
consistent with this confirmed wording. Nothing was reverted or changed.

## Round-25/26/27 fixes confirmed present (not reversed)

- The `ln h` description now reads "logarithm of the unimodular transverse
  fabric eigenvalue \(h=\mathrm{e}^{\ln h}\)"; "eigenvalue ratio" is absent.
- The fabric-axis symbol \(\mathbf m\) is defined as the unit material
  fabric axis in `sec:fabric-biot` and re-stated in `sec:fabric-transverse`.
- The `\(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G=a^{2/3}\mathbf H\)`
  reconstruction with unimodular eigenvalues \(h^{-2},h,h\) is present.
- Cycle-1's "transversely isotropic" edit is retained (five occurrences;
  "transverse-isotropic" absent).

## Integrity

- sha256 of all seven manuscript sources: identical before and after this
  cycle (0/7 differ), and identical to the round-27 manifest.
- `\label`/`\ref`/`\cref`/`\eqref`/`\cite`/`\begin{equation}`/`\begin{align}`
  counts: unchanged (re-run verify_integrity.py; `diff` empty).
- Digit-literal multiset: unchanged per file (re-run verify_integrity.py;
  `diff` empty).
- `git diff --check`: clean.
