# Foster reviewer/editor cycle 1 — disposition (applied / declined)

## Applied

| # | File | Change | Reason |
|---|------|--------|--------|
| 1 | main.tex (abstract) | "divided by the reference solid fraction plus a spherical, rank-one contribution" → "divided by the reference solid fraction, **plus** a spherical, rank-one contribution" (comma added) | Removes the misparse "divided by (fraction plus contribution)"; grouping is now unambiguous. No claim changed. |
| 2 | main.tex (conclusions) | "The floor is a discretization floor attributable to the fixed-step backward-Euler temporal error" → "The floor is attributable to the fixed-step backward-Euler temporal error" | Removes the "floor … floor" echo; "discretization" is fully recovered by "backward-Euler temporal error" and the following first-order-in-dt sentence. No claim changed. |
| 3 | sections/pore_fabric.tex (`sec:fabric-kinematics`) | "Its eigenvalues are the squared principal shape ratios of the distention and its eigenvectors the fabric axes." → "… of the distention, and its eigenvectors **are** the fabric axes." | Supplies the missing copula in the elliptical clause; grammatical, no content change. |

All three edits are prose/punctuation only. They touch no equation, symbol,
label, citation, number, or claim. Verified: counts and digit-literal
multisets unchanged (see counts-after.txt).

## Declined

| # | Location | Proposed change | Reason declined |
|---|----------|-----------------|-----------------|
| 1 | sections/finite_elements.tex `sec:fe-fabric` | Condense the twice-stated "implementation check, not independent derivation" caveat (first for the tensorial law at 4.9e-15, second for the conformal limit at 1.9e-14) | The two statements scope different checks; merging would risk weakening an evidence caveat and touch numeric thresholds. |
| 2 | main.tex (abstract) | Rewrite the triple-"and" scope sentence (manufactured solution / consolidation reference / demonstrations) | Claim-bearing scope statement; rewriting risks altering the verification boundary. No churn. |
| 3 | sections/experiments.tex | Convert `Figure~\ref{fig:…}` to `\Cref{fig:…}` for style consistency | Would change `\ref`/`\cref` counts and touch reference commands; out of scope. |
| 4 | sections/pore_fabric.tex `sec:fabric-energy` | Add "carries" to "its spherical part carries the volume response and its deviatoric part the shape response" | Valid stylistic parallelism, not an error. |
| 5 | main.tex (conclusions) | Further smooth the "discretization floor" passage beyond edit #2 | The remaining text is precise and carries specific numerics; further edits add risk without benefit. |

## Standing decision check (no action, confirmed)

`sec:fabric-transverse` names the volume--axial distention modulus as the
carrier of `B_par != B_per`; an isotropic mineral alone keeps `B` spherical.
Abstract, conclusions, `sec:fe-fabric`, and the fabric figure caption are all
consistent with this. Nothing was reverted or changed here.
