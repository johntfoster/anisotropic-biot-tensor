# Foster reviewer/editor cycle 1 — memo (findings)

Manuscript: anisotropic Biot tensor from mineral stress and distention work
Repository: /home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor
Base snapshot: round-21 `f4c43aee…c673f` (3/3 ACCEPT, zero required corrections)

## What this cycle was

An editorial prose pass only. Round 21 was accepted with no required
corrections, so this cycle made a small number of high-value prose
improvements and otherwise left the text alone. No equation, symbol, label,
citation, number, or claim was changed.

## Findings

The manuscript prose is already clean and consistent. Targeted scans found:

- No repeated words (`the the`, `is is`, etc.), no stray double spaces.
- Consistent US spelling ("distention" throughout), consistent authorial
  "we" voice, correct use of "principal" vs "principle".
- The standing author decision (`sec:fabric-transverse` names the
  volume--axial distention modulus as the carrier of `B_par != B_per`) is
  respected verbatim. Abstract, conclusions, `sec:fe-fabric`, and the fabric
  figure caption all correctly state that an isotropic mineral keeps `B`
  spherical in the absence of volume--axial coupling. Nothing was reverted.

Three low-risk clarity edits were applied (see disposition.md):

1. Abstract: added a comma to disambiguate "divided by the reference solid
   fraction, plus a spherical, rank-one contribution".
2. Conclusions: removed the redundant "a discretization floor" echo
   ("The floor is a discretization floor attributable to…" → "The floor is
   attributable to…").
3. `sec:fabric-kinematics`: supplied the missing copula in the elliptical
   clause "its eigenvectors the fabric axes" → "its eigenvectors are the
   fabric axes".

## Deliberately left unchanged (declined, no churn)

- The duplicated "implementation check, not an independent derivation"
  caveat in `sec:fe-fabric` — the two statements scope different checks
  (the tensorial law vs. the conformal limit); condensing them would risk
  weakening an evidence caveat.
- The triple-"and" scope sentence in the abstract (manufactured solution,
  consolidation reference, demonstrations) — a precise, claim-bearing scope
  statement; rewriting it risks the claim boundary.
- `Figure~\ref{...}` vs `\Cref{...}` cross-reference style differences — any
  change would alter the `\ref`/`\cref` counts and touch reference commands.
- All elliptical parallelism of the form "X carries A and Y B" — valid
  stylistic parallelism, not an error.

## Verification performed

- sha256 of all seven manuscript sources matched the round-21 manifest
  (0/7 differ) before editing.
- `\label`, `\ref`, `\cref`, `\eqref`, `\cite`, `\begin{equation}`,
  `\begin{align}` counts unchanged after editing (checked per file against
  the round-21 snapshot).
- Digit-literal multiset unchanged per file (checked programmatically).
- `git diff --check` clean (whitespace) — see cycle-report.md.
- Full rebuild (see cycle-report.md for exit code, pages, undefined refs,
  overfull boxes).
