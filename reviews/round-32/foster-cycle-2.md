# Foster engineering review — cycle 2 of 3

Manuscript: `main.tex` (+ `sections/*.tex`)
Working tree: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
Skills applied: `foster-engineering-reviewer`, `foster-technical-prose`
Scope of this cycle: **prose revision only**. No equation, label, reference,
citation, number, symbol, unit, assumption, scope statement or claim was changed.

Triage: `python3 .agent/shared/tools/review_scan.py` over `main.tex` and
`sections/*.tex`. Every file returned `"findings": []` except
`sections/logarithmic_derivative.tex`, which returned one candidate,
`unnumbered-display` at line 36 (`\[`). That candidate is the `\\[5pt]` row
separator inside the `cases` environment of `eq:log-frechet-spectral-form`
(equation content, forbidden to touch). Assessed and deliberately left
unchanged, as in cycle 1.

Cycle-1 spans (abstract close; Introduction dilation/rotation distinction; §3
distention-energy purpose and `φ_s0` origin; three passages in
`sections/stress_reconstruction.tex`; two in `sections/logarithmic_derivative.tex`;
one in `sections/pore_fabric.tex`; the §6.3 unjacketed preamble; the §9
plane-traction paragraph) were **not** re-edited.

---

## 1. Scope revised (file, section, passage)

| # | File | Section / anchor | Passage |
|---|------|------------------|---------|
| 1 | `sections/limits.tex` | §6 `sec:compatibility`, section entry | Added a purpose/roadmap sentence before the first subsection |
| 2 | `sections/limits.tex` | §6.1, close of "Reference stress and solid storage" | The sentence naming the common origin of the stress and storage relations |
| 3 | `sections/experiments.tex` | §9.4 "Internal and physical rotations", opening | First sentence (two rotation experiments) |
| 4 | `sections/experiments.tex` | §9.6 "Independent verification and reproducibility", opening | Evaluation of the stress by energy differentiation |
| 5 | `sections/finite_elements.tex` | §8 opening, after `eq:fe-total-first-piola` | The effective-stress scope sentence |
| 6 | `sections/finite_elements.tex` | §8.3, end of the rigid-plate paragraph | The sentence distinguishing the loading condition |
| 7 | `sections/finite_elements.tex` | §8.3, mass-balance paragraph | Backward-Euler discharge accumulation and error normalization |
| 8 | `sections/finite_elements.tex` | §8.3, mass-balance paragraph | The reconstructed-flux sentence |
| 9 | `sections/finite_elements.tex` | §8.3, error measures | Normalization of pressure and displacement errors |
| 10 | `sections/finite_elements.tex` | §8.5 `sec:fe-fabric`, opening | Implementation of the tensorial distention law |
| 11 | `sections/finite_elements.tex` | §8.5, refined-rerun sentence | Rerun on the refined mesh |
| 12 | `main.tex` | §5 `sec:finite-biot`, after `eq:legendre-energy` | The double-prime stress sentence |
| 13 | `main.tex` | §5 `sec:finite-biot`, before the two stress checks | Opening of the two-checks paragraph |

`defs.tex` does not exist in this repository; its macros live inline in
`main.tex` (the `\newcommand`/`\providecommand` block) and contain no prose, so
the first priority item has no prose to revise.

## 2. Explanatory changes made, and why

The profile sequence is *purpose → equation → definitions → implication →
limiting case*, with the physical distinction stated before its formal
representation and opaque nominalizations replaced by a physical subject and an
active verb.

1. **§6 entry (1).** The section opened directly with
   `\subsection{Reference stress and solid storage}` and never stated its
   purpose or how it uses the immediately preceding result, contrary to the
   profile rule for section openings and the roadmap rule when several tasks
   follow. Added two sentences naming the reduction to the undeformed reference
   state and to the two limiting experiments, then listing the three subsection
   tasks in order. No equation, reference or number was introduced.
2. **§6.1 close (2).** "The stress and solid storage relations here come from
   the same energy and the same mineral-volume response." carried a deictic
   "here" and a compressed subject. It now names both relations as the subject
   ("The stress relation and the solid storage relation come from …"), keeping
   the same claim.
3. **§9.4 opening (3).** "There are two different rotation experiments." was an
   empty existential. It is now "We consider two different rotation
   experiments.", a paper-level action in the author's first-person plural.
4. **§9.6 opening (4).** "The stress is first evaluated by differentiating …"
   was a passive subjectless opening. It is now "We first evaluate the stress by
   differentiating …", matching the active "We evaluate the pressure and
   displacement series independently" already used in §8.
5. **§8 opening (5).** "No additional effective-stress correction is applied in
   the momentum residual." The necessary scope distinction is kept but given a
   concrete subject and an active verb: "The momentum residual applies no
   additional effective-stress correction."
6. **§8.3 plate paragraph (6).** "It is distinct from prescribing …" left the
   referent of "It" implicit. It is now "This condition is distinct from
   prescribing …".
7. **§8.3 mass balance (7).** "For a conservative backward-Euler solve, fluid
   discharge is accumulated … The balance error is normalized by …" were
   passives. They now read "we accumulate the fluid discharge …" and "We
   normalize the balance error by …", consistent with the section's first-person
   plural methods voice. No quantity or floor statement changed.
8. **§8.3 reconstructed flux (8).** "A flux reconstructed from boundary pressure
   gradients is evaluated separately because …" became "We evaluate a flux
   reconstructed from boundary pressure gradients separately because …". Same
   claim and caveat.
9. **§8.3 error measures (9).** "Pressure errors are normalized by …, and
   displacement errors by …" became "We normalize pressure errors by …, and
   displacement errors by …". The following "Neither normalization divides by a
   transient value approaching zero." is unchanged.
10. **§8.5 opening (10).** "The tensorial distention law of
    `\cref{sec:pore-fabric}` is implemented as a material that evaluates …"
    became "We implement the tensorial distention law of
    `\cref{sec:pore-fabric}` as a material that evaluates …". The existing
    `\cref` was retained unchanged in place.
11. **§8.5 rerun (11).** "the same coupled problem is rerun on a refined …"
    became "we rerun the same coupled problem on a refined …". Mesh, domain and
    snapshot counts are unchanged.
12. **§5 double-prime stress (12).** "The double-prime stress is obtained by
    differentiating \(W''\) at fixed pressure." became "Differentiating \(W''\)
    at fixed pressure gives the double-prime stress." — the operation is now the
    grammatical subject, in the profile's "the balance gives" pattern.
13. **§5 two checks (13).** "There are two useful checks on the stress
    interpretation. First, …" was an existential opening. It is now "The energy
    also provides two useful checks on the stress interpretation. First, …",
    naming the source of the checks and keeping the retained "useful" and the
    First/Second enumeration.

## 3. Passages deliberately left unchanged, and why

- **`defs.tex`.** Does not exist; the `main.tex` macro block carries no prose.
- **`main.tex` §2 notation key (the bar/prime/`dis` paragraph).** A deliberate
  symbol inventory in which every clause carries a symbol, a reference or a
  normalization convention. Rewriting risks dropping a load-bearing
  symbol/normalization distinction; cycle 1 reached the same conclusion.
- **`main.tex` §1 literature survey.** Removing inventory-style citation runs
  would delete citations, which the hard contract forbids.
- **`main.tex` §5 remainder and the concluding Discussion.** Reviewed in full.
  The remaining §5 prose already follows purpose → equation → local definitions
  → consequence (e.g. the pore-volume interpretation after
  `eq:biot-pore-volume-variation`, and the symmetry argument after
  `eq:anisotropic-biot-explicit`), and the Discussion already restates the
  construction, states what the checks and reductions establish, distinguishes
  the constitutive specialization from stress symmetry, and closes
  constructively ("only the distention law that closes it differs"). Its
  negations are necessary distinctions, not novelty-by-contrast. No non-cosmetic
  change was available.
- **`sections/stress_reconstruction.tex`, other than the three cycle-1 spans.**
  Re-read in full; the equation paragraphs already open with purpose, define
  symbols locally, and state the immediate consequence. Left as authored.
- **`sections/pore_fabric.tex` "Fixing the rotation has three consequences."**
  Dense but every clause is a necessary scope statement and the framing "three"
  is the author's structure. Restructuring would drop a scope statement or
  renumber the consequences — a claim change. Left as authored.
- **`sections/logarithmic_derivative.tex` line 36 (`\\[5pt]` in `cases`).** The
  only `review_scan.py` flag; equation content.
- **`sections/experiments.tex` subsections other than (3) and (4).** The
  pressure-change, shape-change, plane-traction, laterally-constrained-extension
  and verification/reproducibility passages already state the physical
  situation, give the equation, read the figure, and state the limiting
  comparison; they already distinguish derived results, synthetic parameters and
  scope. No non-cosmetic improvement was available.
- **`sections/finite_elements.tex` remaining methods sentences.** A few
  passives remain where the passive is the conventional register for an
  algorithmic description and no reader benefit was identified; forcing them
  active would have churned prose without changing the explanation.
- **All displayed equations, `align` bodies, `\label`s,
  `\eqref`/`\cref`/`\Cref` targets, `\cite` keys, numeric literals, and every
  stated assumption, scope caveat and verification/floor statement** (including
  the `3.2×10⁻³` floor, temporal orders `0.98`–`1.40`, the `1.94` ratio, the
  `186`/`273`/`65` check counts, the `2.5×10⁻⁹` largest error, the `4.36×10⁻⁵`
  peak pressures, and all material-point error magnitudes).

## 4. Required proof — exact command output

### Step 1 — before extraction (labels, refs, cite keys, numeric literals)

Command: `python3 /tmp/extract_surface.py /tmp/foster2-before.txt`
(walks `main.tex`, `sections/*.tex`, `provenance/ai_use_statement.tex` in
document order; same extractor used before and after).

```
/tmp/foster2-before.txt: sha256=241136945222d7e251c1a2c2e085526f28bb205aa9582c71c1af1a8f7288bdc8
/tmp/foster2-before.txt.sorted: sha256=efa5e961cf7cf0517eec056180eaa15100cc9b3a262be0d613d6342b9f68ece5
lines=1022
```

### Step 2 — after extraction and diff

```
/tmp/foster2-after.txt: sha256=241136945222d7e251c1a2c2e085526f28bb205aa9582c71c1af1a8f7288bdc8
/tmp/foster2-after.txt.sorted: sha256=efa5e961cf7cf0517eec056180eaa15100cc9b3a262be0d613d6342b9f68ece5
lines=1022
ordered diff exit: 0
sorted diff exit:  0
```

`diff /tmp/foster2-before.txt /tmp/foster2-after.txt` produced **no output**.
`diff` of the sorted extractions also produced **no output**.

**The claim-surface diff is empty.** The before and after sha256 of the ordered
extraction are identical
(`241136945222d7e251c1a2c2e085526f28bb205aa9582c71c1af1a8f7288bdc8`), and of
the sorted extraction identical
(`efa5e961cf7cf0517eec056180eaa15100cc9b3a262be0d613d6342b9f68ece5`). Every
`\label` name, every `\ref`/`\eqref`/`\cref`/`\Cref` argument, every
`\cite`/`\citep`/`\citet` key, and every numeric literal in text and math is
unchanged by this cycle.

### Step 3 — comparison against the last commit (`HEAD` = `8d83726`)

For each edited file, `git show HEAD:<file>` was piped through the same
tokenizer and diffed against the working-tree file on disk.

```
=== main.tex ===
--- ordered diff (HEAD vs disk) ---
63a64,66
> ref	\cref{sec:finite-biot}
> ref	\eqref{eq:reduced-energy}
> ref	\eqref{eq:legendre-energy}
66a70
> ref	\cref{sec:work-equivalence}
exit=1
label: HEAD=41 disk=41
ref:   HEAD=37 disk=41
cite:  HEAD=23 disk=23
num:   HEAD=133 disk=133

=== sections/limits.tex ===
--- ordered diff (HEAD vs disk) ---
exit=0
label: HEAD=9  disk=9
ref:   HEAD=4  disk=4
cite:  HEAD=0  disk=0
num:   HEAD=29 disk=29

=== sections/experiments.tex ===
--- ordered diff (HEAD vs disk) ---
exit=0
label: HEAD=9   disk=9
ref:   HEAD=15  disk=15
cite:  HEAD=1   disk=1
num:   HEAD=116 disk=116

=== sections/finite_elements.tex ===
--- ordered diff (HEAD vs disk) ---
exit=0
label: HEAD=26  disk=26
ref:   HEAD=20  disk=20
cite:  HEAD=1   disk=1
num:   HEAD=187 disk=187
```

Per-category **set** difference for `main.tex` (set, not sequence):

```
label  HEAD-only: (none)     disk-only: (none)
ref    HEAD-only: (none)     disk-only: \cref{sec:finite-biot}
                                        \cref{sec:work-equivalence}
                                        \eqref{eq:legendre-energy}
                                        \eqref{eq:reduced-energy}
cite   HEAD-only: (none)     disk-only: (none)
num    HEAD-only: (none)     disk-only: (none)
```

**Interpretation of the `main.tex` difference.** It is a **pre-existing**
difference that predates this cycle, not one I introduced. Proof:

- My own before/after diff (Step 2) is empty, so no token of any kind was added
  or removed by this cycle.
- Those four `ref` tokens were already present in the pre-edit working-tree
  surface: `grep -c` against `/tmp/foster2-before.txt` returns
  `sec:finite-biot -> 3`, `eq:reduced-energy -> 2`, `eq:legendre-energy -> 2`,
  `sec:work-equivalence -> 3`.
- The identical surface was recorded at the start of cycle 1:
  `sha256sum /tmp/foster1-before.txt` and `/tmp/foster2-before.txt` both give
  `241136945222d7e251c1a2c2e085526f28bb205aa9582c71c1af1a8f7288bdc8`.
- On disk the four additions sit at `main.tex` lines 242–244 (`\cref{sec:finite-biot}`,
  `\eqref{eq:reduced-energy}`, `\eqref{eq:legendre-energy}`) and line 251
  (`\cref{sec:work-equivalence}`) — the §2 notation key and §3, spans this cycle
  did not edit (my `main.tex` edits are in §5). They are uncommitted changes that
  were already in the working tree when cycle 1 began.

No difference between `HEAD` and disk in labels, refs, cites or numbers
originates from this cycle. The only files with a `HEAD`→disk claim-surface
difference are the ones with pre-existing uncommitted work; `limits.tex`,
`experiments.tex` and `finite_elements.tex` are byte-identical in claim surface
to `HEAD`.

### Step 4 — rebuild

Command (exactly as specified):

```sh
latexmk -g -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

```
EXIT=0
Output written on main.pdf (33 pages, 2807782 bytes).

pages: 33
Overfull: 0
Underfull: 1
undefined ref/cite: 0
Missing character: 0
LaTeX Warning count: 0
```

The one Underfull line is
`Underfull \hbox (badness 1137) in paragraph at lines 33--40` in
`build/main.log`; it is present identically in the baseline build of the
unmodified source and is not introduced by these edits. Page count is 33, the
same as the baseline recorded in cycle 1.

Render check: `pdftotext build/main.pdf` contains each new sentence, e.g.
"The energy also provides two useful checks on the stress interpretation.",
"We consider two different rotation experiments.",
"We first evaluate the stress by differentiating the mineral energy …",
"The momentum residual applies no additional effective-stress correction.",
"We implement the tensorial distention law …", and
"We evaluate a flux reconstructed from boundary pressure gradients separately
because its discretization error is not the algebraic mass-balance error."

Equation-numbering check: the `\newlabel{eq:…}` table in `build/main.aux` was
compared with the baseline table copied at cycle 1
(`/tmp/foster1-aux-before.aux`): 212 labels in both, no label added or removed,
and no equation renumbered.

## 5. Status

Files changed: `main.tex`, `sections/limits.tex`, `sections/experiments.tex`,
`sections/finite_elements.tex`. No other file was modified (in particular, not
`figures/`, `fe-evidence/`, `build/`, `tools/`, `site/`, `references.bib`, or any
other file under `reviews/`). Claim surface: **identical within this cycle**
(empty before/after diff). Build: **pass**, 33 pages, no new diagnostics. This
memo is `reviews/round-32/foster-cycle-2.md`.

Not performed (recorded rather than asserted): the held suites under
`validation/` and `examples/verify_*.py` were not run, and no scientific claim
was re-derived; this cycle is prose-only by contract.
