# Foster reviewer/editor cycle 1 (round-24) — disposition (applied / declined)

## Applied

| # | File | Change | Reason |
|---|------|--------|--------|
| 1 | main.tex (conclusions) | "In the transverse-isotropic fabric case the Biot tensor…" → "In the **transversely isotropic** fabric case the Biot tensor…" | Terminology consistency: the manuscript uses the standard term "transversely isotropic" four times in `sec:pore-fabric`; "transverse-isotropic" was a lone non-standard hyphenation. No equation, symbol, label, citation, number, or claim changed. |

This single edit is prose/terminology only. Verified: counts and digit-literal
multisets unchanged (see counts-after.txt; `diff` of the counts/digit lines is
empty). `git diff --check` is clean.

## Declined (no churn)

| # | Location | Proposed change | Reason declined |
|---|----------|-----------------|-----------------|
| 1 | sections/finite_elements.tex | Normalize the US/UK spelling mix ("center-pressure"/"Center" vs "centre-pressure"/"Centre", "colour", "modelling" vs three "modeling" in `sec:pore-fabric`) | Purely cosmetic; the author style profile states no US/UK convention, and normalization would touch several unchanged lines. Recorded, not changed. |
| 2 | sections/finite_elements.tex `sec:fe-fabric` | Condense the twice-stated "implementation check, not independent derivation" caveat (tensorial law `4.9e-15`, conformal limit `1.9e-14`) | Settled in prior Foster cycles: the two statements scope different checks; condensing risks weakening an evidence caveat and touching numeric thresholds. |
| 3 | sections/pore_fabric.tex `sec:fabric-energy` | "its spherical part carries the volume response and its deviatoric part the shape response" → add "carries" to the second clause | Valid stylistic parallelism, not an error; settled in prior Foster cycles. |
| 4 | sections/pore_fabric.tex `sec:fabric-equilibrium` | "must be an isotropic scalar function of the fabric tensor, that is, depend only on…" → add a second "must" | Valid elliptical parallel governed by the earlier "must"; settled in prior Foster cycles. |
| 5 | main.tex (introduction) | Smooth the trailing "and at small strain" qualifier in the Cowin-poroelasticity sentence | Claim-scoping detail (the cited poroelastic fabric constructions are small-strain); rewriting risks the claim boundary. |

## Standing decision check (no action, confirmed)

`sec:fabric-transverse` names the volume--axial distention modulus as the
carrier of `B_par != B_per`; an isotropic mineral alone keeps `B` spherical.
Abstract, conclusions, `sec:fe-fabric`, and the fabric figure captions are all
consistent with this confirmed wording. Nothing was reverted or changed here.

## Integrity

- sha256 of all seven manuscript sources: matched the round-24 manifest before
  editing (0/7 differ). After editing, only `main.tex` changed:
  `4d2b75d1…63787af` → `70e2cf27…5ec52`.
- `\label`/`\ref`/`\cref`/`\eqref`/`\cite`/`\begin{equation}`/`\begin{align}`
  counts: unchanged (verified programmatically).
- Digit-literal multiset: unchanged per file (verified programmatically).
- `git diff --check`: clean.
