# Foster reviewer/editor cycle 2 — memo (findings)

Manuscript: anisotropic Biot tensor from mineral stress and distention work
Repository: /home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor
Base snapshot: round-21 `f4c43aeea1590c8e166d3ffab342e5da92094443e55b4df4d47b69bbad8c673f`
Cycle 1 (complete): applied 3 conservative prose edits (abstract comma;
conclusions "floor … floor" echo; a missing copula in `sec:fabric-kinematics`).

## What this cycle was

An authorial/editorial prose pass only, the second of three. Round 21 was
accepted 3/3 with zero required corrections, and cycle 1 already made the
small number of high-value prose improvements that existed. This cycle was a
fresh independent prose read of all seven manuscript sources to determine
whether any additional high-value prose edit remains.

## Conclusion

**Zero prose edits are warranted.** The manuscript prose is clean. A
targeted scan and a sentence-level read found no repeated words, no stray
double spaces in prose, no homophone or usage errors, consistent US spelling,
a consistent authorial "we" voice, correct "principal"/"principle" and
"affect"/"effect" usage, and no negative-positioning, drafting-history,
unsupported-rhetoric, or chat-local phrasing. Every remaining candidate was
either (a) already settled by cycle 1, (b) a claim-bearing or scope-bearing
sentence whose rewriting would risk the claim boundary, or (c) a marginal
stylistic preference that would constitute churn.

## Findings (all clean)

- `python3 .agent/shared/tools/review_scan.py` returned zero flags for all
  seven sources (no negative-positioning, drafting-history,
  unsupported-rhetoric, manual-delimiter, or unnumbered-display matches).
- Repeated-word scan (including across source line breaks): none.
- Double-space scan of prose (excluding math-alignment rows): none.
- Homophone/usage scan: "principal" vs "principle" correct; "affects" (verb)
  and "effects" (noun) each used correctly; no "it's"/"its" confusion.
- Voice: first-person plural "we" throughout; no first-person singular.
- No "that is,", "i.e.", or "e.g." construction is misused or mispunctuated.

## Candidates considered and declined (no churn)

1. `sections/pore_fabric.tex` `sec:fabric-equilibrium` — "\(W_d\) must be an
   isotropic scalar function of the fabric tensor, that is, depend only on
   the three invariants…". The bare "depend" is a valid elliptical parallel
   governed by the earlier "must"; adding a second "must" ("…that is, must
   depend only on…") would be clunky and add no clarity. Declined.

2. `sections/pore_fabric.tex` `sec:fabric-energy` — "its spherical part
   carries the volume response and its deviatoric part the shape response".
   This elliptical parallelism was already declined in cycle 1 (disposition
   #4). Not revisited; settled.

3. `sections/finite_elements.tex` `sec:fe-fabric` — the twice-stated
   "implementation check, not an independent derivation" caveat. Already
   declined in cycle 1 (disposition #1); the two statements scope different
   checks. Not revisited; settled.

4. Abstract triple-"and" scope sentence and `Figure~\ref{…}` vs `\Cref{…}`
   cross-reference style. Already declined in cycle 1 (disposition #2, #3).
   Not revisited; settled.

5. Any whitespace normalization (the sources contain pre-existing trailing
   whitespace on wrap-indented lines). This is out of scope and would be pure
   churn; not touched.

## Standing author decision (verified, no action)

`sec:fabric-transverse` names the volume--axial distention modulus as the
carrier of `B_par != B_per`; an isotropic mineral alone keeps `B` spherical.
Abstract, conclusions, `sec:fe-fabric`, and the fabric figure captions are all
consistent with this confirmed wording. Nothing was reverted or changed.

## Verification performed

- sha256 of all seven manuscript sources matched the cycle-1 post-edit state
  (0/7 differ) before and after this cycle (see snapshot-hash-table.txt and
  verify_integrity.py output).
- `\label`, `\ref`, `\cref`, `\eqref`, `\cite`, `\begin{equation}`,
  `\begin{align}` counts identical before/after (no edits made).
- Digit-literal multiset identical per file (no edits made; byte-identical
  sources).
- Full rebuild performed (see cycle-report.md for exit code, pages,
  undefined refs/citations, overfull boxes).
