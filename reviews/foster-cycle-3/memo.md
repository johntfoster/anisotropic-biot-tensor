# Foster engineering-review / editor memo — cycle 3 of 3 (final)

Manuscript: `An anisotropic Biot tensor from mineral stress and distention work`
Repository: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
Reviewed snapshot: `c621378778d49f8875679440cf874a74aef3caa5d9b04b8936ad319fb57f885f`
(round-16, `.agent-runtime/review-snapshots/round-16/source-manifest.json`).
Scope: prose only (wording in `main.tex` and `sections/*.tex`). No equation,
symbol, label, citation, number, table entry, or stated assumption is in scope.
Reviewer position: fresh independent read of the tree after cycles 1 and 2.
Line numbers below are those of the working tree entering this cycle (the
cycle-2 final state).

Priorities: **high** = blocks comprehension or misstates scope; **medium** =
local clarity, precision, or referent problem a reader notices; **low** =
polish.

---

## Findings authored in this cycle

**1 — main.tex:501–505 (Discussion and conclusions, paragraph 2) — medium — APPLIED.**
"A finite-element discretization …; at finite load the nonlinear solutions
approach the reference as the load decreases, but their normalized pressure
discrepancy floors at about \(3.2\times10^{-3}\) at \(nx=20\), \(dt=10^{-3}\)
rather than decaying to it, and the finite-load rotated-anisotropy and
partial-drainage calculations are reported as demonstrations…"
The closing sentence of the paragraph is ~110 words and carries three distinct
claims chained by a semicolon and a coordinate `and`: the verification result,
the finite-load flooring behavior, and the demonstrations-versus-verification
scope boundary. A reader parsing them from one sentence is likely to lose which
claim is bounded by which qualifier.
**Proposed revision.** End the flooring clause at "rather than decaying to it"
and begin the scope boundary as its own sentence.
**Disposition.** applied. Before:
`…\(dt=10^{-3}\) rather than decaying to it, and the finite-load
rotated-anisotropy…`
After:
`…\(dt=10^{-3}\) rather than decaying to it. The finite-load
rotated-anisotropy…`
Every number (\(3.2\times10^{-3}\), \(nx=20\), \(dt=10^{-3}\)) and every claim
is preserved verbatim; only the coordinate `and` becomes a sentence boundary.

## Examined and declined (no change)

**2 — main.tex §2 notation inventory, "a bar on a stress denotes …"** — the
three bar/hat conventions are dense but each clause is self-contained and the
inventory is necessary; splitting risks reordering the conventions. No change.

**3 — main.tex §3, "Substituting it into the first recovers …"** — "the first"
resolves to "the first line" established one sentence earlier ("The second line
uses pressure equilibrium"). Unambiguous; no change.

**4 — sections/logarithmic_derivative.tex:47, "For \(\mathbf T=\mathbf I\), it
maps the logarithmic stress to the same spatial identity."** — the pronoun
carries the subject "the derivative" from the preceding sentence and the
sentence states a trace-conservation property of the log-derivative; any
rewording would border on a scientific claim. No change.

**5 — sections/limits.tex:65–66, "The solid and mixture should then have the
same homogeneous stretch"** — "should" states the physical condition of the
unjacketed test; replacing it with a bare declarative would change claim
strength. No change.

## Carried forward (out of prose-only scope)

**C1** (cycle-1 #15 / cycle-2 F17) — reused rectangle semi-axes `a`, `b` in
`sections/finite_elements.tex` versus `a=\det\mathbf A` (distention ratio) and
`\mathbf b_0` (body force). Resolving changes displayed notation; deferred to a
technical/notation cycle.

**C2** (cycle-1 #14) — wording that defines the isotropic-comparison modulus
\(16.8K_*\). Rewording could alter the stated definition; out of scope.

---

## Concurrent modification observed (not authored by this cycle)

The working tree is live-synced (Syncthing, per the workspace configuration).
While this session was running, prose edits I did not author arrived in the
tree, and a second `reviews/foster-cycle-3/` deliverable set was written by a
concurrent run. Each arriving edit was checked and is prose-only (no
equation/symbol/label/citation/number change; the digit-literal multiset is
unchanged in every file). The arriving edits are:

- `main.tex` §2 notation inventory — the three bar/hat conventions were split
  from one semicolon-chained sentence into three sentences (`; a bar` →
  `. A bar`, twice).
- `main.tex` conclusion paragraph 2 — a second, complementary split at the
  earlier semicolon ("for that reference tangent; at finite load" →
  "for that reference tangent. At finite load"), so the paragraph's closing
  sentence is now three sentences total (this cycle's edit is the third).
- `sections/experiments.tex:204–205` — definite articles added for parallel
  structure ("distinguishes loss of that branch from violation of" →
  "distinguishes the loss of that branch from the violation of").

These are consistent with the editorial scope and are reported here so the
parent can reconcile the two runs; this memo's numbered findings are the ones
authored in this session.

## Assessment summary

After cycles 1 and 2 the manuscript was already in final technical-prose
condition. This closing pass found no hedging artifacts, no drafting-history
phrasing, no unsupported novelty claims, no dangling equation/citation
references, and no remaining agentive or pronoun-referent defect worth changing.
The single applied edit is a high-value readability split of an overlong
conclusion sentence; everything else was examined and declined rather than
churned.
