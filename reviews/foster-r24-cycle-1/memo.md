# Foster reviewer/editor cycle 1 (round-24) — memo (findings)

Manuscript: anisotropic Biot tensor from mineral stress and distention work
Repository: /home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor
Base snapshot: round-24 `1dea9e121e8d763dc0b4008d9b430026a17d600fbdd67d5f085a7d6f2617b423`
(3/3 ACCEPT, zero required corrections; 591-file manifest)

## What this cycle was

An editorial prose pass only, on a superseded tree relative to the earlier
`foster-fabric-cycle-{1,2,3}` records (those were written against the round-21
snapshot). Round 24 was accepted with no required corrections, so this cycle
made the smallest number of high-value prose improvements and otherwise left
the text alone. No equation, symbol, label, citation, number, or claim was
changed; the seven manuscript sources were byte-identical to the round-24
manifest before editing (0/7 differ).

## Findings

The manuscript prose is clean and consistent in the respects the prior Foster
cycles already established (no repeated words, no stray double spaces, correct
"principal"/"principle" usage, consistent "distention" spelling, consistent
authorial "we" voice). One terminology inconsistency remained that is not
present in the prior cycle records: the conclusions used the non-standard
hyphenation "transverse-isotropic" exactly once, while the rest of the
manuscript (four occurrences in `sec:pore-fabric`) uses the standard term
"transversely isotropic." This single edit was applied (see disposition.md).

## Deliberately left unchanged (declined, no churn)

- **US/UK spelling mix.** `sections/finite_elements.tex` mixes
  "center-pressure"/"Center" (two lines) with "centre-pressure"/"Centre"
  (four lines), uses "colour" (two lines), and writes "modelling conventions"
  once against three "modeling" spellings in `sec:pore-fabric`. The author
  style profile states no US/UK convention, and normalizing it would touch
  several unchanged lines for purely cosmetic benefit. Recorded, not changed.
- **The twice-stated "implementation check, not an independent derivation"
  caveat** in `sec:fe-fabric` (tensorial law at `4.9e-15`, conformal limit at
  `1.9e-14`). Settled in prior Foster cycles: the two statements scope
  different checks; condensing would risk weakening an evidence caveat.
- **Elliptical parallelism** of the form "its spherical part carries the
  volume response and its deviatoric part the shape response" and "must be an
  isotropic scalar function … that is, depend only on …." Settled in prior
  Foster cycles as valid stylistic parallelism, not an error.
- **The "and at small strain" trailing qualifier** in the introduction's
  Cowin-poroelasticity sentence. It scopes a claim (the cited poroelastic
  fabric constructions are small-strain); rewriting risks the claim boundary.

## Standing decision check (no action, confirmed)

`sec:fabric-transverse` names the volume--axial distention modulus as the
carrier of `B_par != B_per`; an isotropic mineral alone keeps `B` spherical.
Abstract, conclusions, `sec:fe-fabric`, and the fabric figure captions are all
consistent with this confirmed wording (verified in the text). Nothing was
reverted or changed here.

## Verification performed

- sha256 of all seven manuscript sources matched the round-24 manifest
  (0/7 differ) before editing — see snapshot-hash-table.txt.
- `\label`/`\ref`/`\cref`/`\eqref`/`\cite`/`\begin{equation}`/`\begin{align}`
  counts unchanged after editing (per file, verified programmatically with
  verify_integrity.py; `diff` on the counts/digit lines is empty).
- Digit-literal multiset unchanged per file (verified programmatically).
- `git diff --check` clean (whitespace) — see cycle-report.md.
- Full rebuild: exit code 0, 33 pages, no undefined references/citations,
  0 overfull boxes — see cycle-report.md and build.log.
