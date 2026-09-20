# Foster engineering-review / editor disposition — cycle 3 of 3 (final)

One row per memo item. Priority: high / medium / low.
Scope: prose only; no equation, label, citation, numeric value, table entry, or
stated assumption changed.

| # | Location | Priority | Disposition | Reason |
|---|----------|----------|-------------|--------|
| 1 | main.tex:501–505 (§7 conclusion) | medium | APPLIED | Split the ~110-word closing sentence after "rather than decaying to it"; every number (3.2e-3, nx=20, dt=10^-3) and claim preserved verbatim. |
| 2 | main.tex §2 notation inventory | low | DECLINED | Each bar/hat clause is self-contained; splitting risks reordering the conventions. |
| 3 | main.tex §3 "Substituting it into the first" | low | DECLINED | "the first" resolves to "the first line" established one sentence earlier. |
| 4 | logarithmic_derivative.tex:47 "it maps …" | low | DECLINED | Pronoun carries "the derivative" from the prior sentence; rewording would border a scientific claim. |
| 5 | limits.tex:65–66 "should then have" | low | DECLINED | "should" states the unjacketed-test condition; a bare declarative would change claim strength. |
| C1 | finite_elements.tex vs main.tex (`a`, `b` reuse) | — | DEFERRED (out of scope) | Cycle-1 #15 / cycle-2 F17; resolving changes displayed notation, forbidden in prose-only. |
| C2 | experiments.tex:30–31 (16.8K_* definition) | — | DEFERRED (out of scope) | Cycle-1 #14; rewording could alter the stated definition. |

## Applied counts

- Applied: 1 (item 1)
- Declined: 4 (items 2–5)
- Deferred / out of scope (carried from cycles 1–2): 2 (C1, C2)
- Total findings authored this cycle: 5 (1 applied, 4 declined, 2 carried)

## Before / after for the applied item

Item 1 — main.tex:501–505 (conclusion paragraph 2)
- before: `…\(dt=10^{-3}\) rather than decaying to it, and the finite-load rotated-anisotropy and partial-drainage calculations are reported as demonstrations…`
- after:  `…\(dt=10^{-3}\) rather than decaying to it. The finite-load rotated-anisotropy and partial-drainage calculations are reported as demonstrations…`

## Concurrent edits observed (not authored by this cycle)

The tree is live-synced (Syncthing). Three prose edits arrived during the
session and are verified prose-only (digit-literal multiset unchanged):

- `main.tex` §2 notation inventory: two `; a bar` → `. A bar` sentence splits.
- `main.tex` conclusion: "…tangent; at finite load" → "…tangent. At finite load"
  (complementary to item 1; the paragraph's closing sentence is now three
  sentences).
- `sections/experiments.tex:204–205`: added definite articles
  ("the loss … from the violation").

These are listed here for reconciliation with the concurrent run; they are not
attributed to this session's numbered findings.
