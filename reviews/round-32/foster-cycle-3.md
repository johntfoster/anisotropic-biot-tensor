# Foster engineering review — cycle 3 of 3 (final)

Manuscript: `main.tex` (+ `sections/*.tex`)
Working tree: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
Skills applied: `foster-engineering-reviewer`, `foster-technical-prose`
Scope of this cycle: **prose revision only**. No equation, its content or order,
`\label`, `\ref`/`\eqref`/`\cref`/`\Cref` target, `\cite` key, number, symbol,
unit, variable name, stated assumption, scope statement or claim was changed.

Triage: `python3 .agent/shared/tools/review_scan.py` over `main.tex` and
`sections/*.tex`. Every file returned `"findings": []` except
`sections/logarithmic_derivative.tex`, which returned one candidate,
`unnumbered-display` at line 36 (`\[`) — the `\\[5pt]` row separator inside the
`cases` environment of `eq:log-frechet-spectral-form`, i.e. equation content,
which this contract forbids touching. Assessed and deliberately left unchanged,
as in cycles 1 and 2.

Cycle-1 spans (abstract close; Introduction dilation/rotation distinction; §3
distention-energy purpose and `φ_s0` origin; three passages in
`sections/stress_reconstruction.tex`; two in `sections/logarithmic_derivative.tex`;
one in `sections/pore_fabric.tex`; the §6.3 unjacketed preamble; the §9
plane-traction paragraph) and cycle-2 spans (`sections/limits.tex` entry
roadmap and §6.1 close; `sections/experiments.tex` §9.4 and §9.6 openings;
seven `sections/finite_elements.tex` passages; two `main.tex` §5 passages) were
**not** re-edited.

This final cycle worked the priority order given: the concluding discussion
(first), the abstract opening (second), residual unreviewed prose (§6.2 and the
§7.1 fixed-rotation paragraph), and a consistency pass over the prose the two
earlier cycles produced.

---

## 1. Scope revised (file, section, passage)

| # | File | Section / anchor | Passage |
|---|------|------------------|---------|
| 1 | `main.tex` | Abstract, sentence 2 | Opening description of the distention decomposition |
| 2 | `main.tex` | §10 `sec:conclusion`, first paragraph | Sentence 2 (what writing the decomposition exposes) |
| 3 | `main.tex` | §10 `sec:conclusion`, second paragraph | First two sentences (the mineral-volume equation and its derivative) |
| 4 | `sections/limits.tex` | §6.2 "Isotropic mineral" | The Gajo-correspondence sentence (ambiguous pronoun) |
| 5 | `sections/pore_fabric.tex` | §7.1 `sec:fabric-kinematics`, "Fixing the rotation has three consequences." | The first numbered consequence (split run-on) |

---

## 2. Explanatory changes made, and why

The profile sequence is *purpose → equation → definitions → implication →
limiting case*, with the physical distinction stated before its formal
representation and opaque nominalizations replaced by a physical subject and an
active verb.

1. **Abstract, sentence 2 (1).** "The distention gradient consists of a dilation
   and a proper rotation, so …" described the *specialization* A = a^{1/3} R_A as
   though it were the generic distention gradient, and "consists of" leaves the
   multiplication ambiguous (A is a dilation *times* a rotation, not the sum of
   two objects). It now reads "We write the distention gradient as a dilation
   times a proper rotation, so …", which states the multiplicative decomposition
   and marks it as the modeling choice it is. The physical consequence clause
   ("mineral deformation and changes in pore volume are distinguished without
   fixing the orientation of the intermediate frame") is unchanged.
2. **§10, first paragraph (2).** "Writing the distention as a dilation times a
   proper rotation makes that change of variables explicit" left "that change of
   variables" with no antecedent in the conclusion (the equation is not shown
   there) and hid the physical content in a nominalization. It now names what the
   decomposition exposes — "separates the volume change from the frame rotation"
   — so the reader meets the physical distinction, not a meta-statement about the
   derivation. The following clause ("the skew rotation variation performs no
   work against a symmetric stress") is unchanged.
3. **§10, second paragraph (3).** "The mineral-volume equation retains the
   coupling between volume and shape in the anisotropic mineral law." had an
   opaque verb ("retains" from an unnamed prior state) and an abstract object. It
   now states the physical relation with a concrete subject and an active verb:
   "The mineral-volume equation couples mineral volume to the shape of the
   skeleton through the anisotropic mineral law." "Its derivative produces a
   directional Biot tensor while preserving the full spatial phase stress
   balance." is retained; only its line wrap moved.
4. **§6.2 `limits.tex` (4).** "The correspondence concerns its volumetric law."
   — the pronoun "its" could attach to the equation, the elimination, or Gajo's
   model. It now reads "The correspondence concerns the volumetric law of Gajo's
   model.", naming the referent. Same claim.
5. **§7.1 `pore_fabric.tex` (5).** The first of the "three consequences" was a
   single ~35-word sentence compounding two ideas with ", and": the symmetry of
   the distention (so G carries shape and orientation), and the entry of the
   relative fabric orientation as material data. It is split into two
   medium-length sentences, the second opening with "therefore" to make the
   logical link the profile asks for; the enumeration of three consequences is
   intact and no scope statement was dropped.

---

## 3. Passages deliberately left unchanged, and why

- **`main.tex` §2 notation key (the bar/prime/`dis` paragraph).** A deliberate
  symbol inventory in which every clause carries a symbol, a reference or a
  normalization convention. Rewriting risks dropping a load-bearing
  symbol/normalization distinction; cycles 1 and 2 reached the same conclusion.
  Left as authored.
- **`main.tex` §1 literature survey and the "we are not aware of a tensorial
  distention law" gap statement.** Rephrasing the gap statement would either
  remove a citation (forbidden) or alter a stated claim about prior work.
  Preserved verbatim.
- **`main.tex` §5 remainder, the §10 third through final paragraphs.** The
  remaining conclusion prose already restates the construction, states what the
  checks and reductions establish, distinguishes the constitutive specialization
  from stress symmetry, and closes constructively ("only the distention law that
  closes it differs"). Its negations are necessary distinctions, not
  novelty-by-contrast. No non-cosmetic change was available.
- **§10 closing scope statement (last paragraph).** Reviewed. It states the
  synthetic-parameter limitation, the elastic-energy interpretation of constant
  logarithmic coefficients, and the boundary of the conformal result. Its
  restatement of the §7 tensorial law resolves back to a summarized pointer
  rather than a fresh derivation, so it is a scope summary, not a duplicated
  neighbouring explanation; removing it would delete a scope statement. Left
  intact. (Noted here because the final consistency pass examined it.)
- **§7.1 remainder, the other two of the "three consequences".** Necessary scope
  statements ("no rotational fabric variable", "dissipates no work in such a
  rotation"); restructuring would renumber the enumeration — a claim change.
  Left as authored; only the first consequence's sentence boundary was changed.
- **`sections/logarithmic_derivative.tex` line 36 (`\\[5pt]` in `cases`).** The
  only `review_scan.py` flag; equation content.
- **All displayed equations, `align` bodies, `\label`s,
  `\eqref`/`\cref`/`\Cref` targets, `\cite` keys, numeric literals, and every
  stated assumption, scope caveat and verification/floor statement** (including
  the `3.2×10⁻³` floor, temporal orders `0.98`–`1.40`, the `1.94` ratio, the
  `186`/`273`/`65` check counts, the `2.5×10⁻⁹` largest error, the
  `4.36×10⁻⁵` peak pressures, and all material-point error magnitudes).
- **`sections/finite_elements.tex` remaining conventional passives.** Cycle 2
  converted the reader-facing ones; the residual algorithmic passives carry no
  reader benefit to change and were left.

---

## 4. Required proof — exact command output

### Step 1 — before extraction (labels, refs, cite keys, numeric literals)

Command: `python3 /tmp/extract_surface.py /tmp/foster3-before.txt`
(the same deterministic extractor used in cycles 1 and 2; walks `main.tex`,
`sections/*.tex`, `provenance/ai_use_statement.tex` in document order).

```
/tmp/foster3-before.txt: sha256=241136945222d7e251c1a2c2e085526f28bb205aa9582c71c1af1a8f7288bdc8
/tmp/foster3-before.txt.sorted: sha256=efa5e961cf7cf0517eec056180eaa15100cc9b3a262be0d613d6342b9f68ece5
lines=1022
```

Cross-check that the pre-edit surface is the same artifact all three cycles
started from:

```
241136945222d7e251c1a2c2e085526f28bb205aa9582c71c1af1a8f7288bdc8  /tmp/foster1-before.txt
241136945222d7e251c1a2c2e085526f28bb205aa9582c71c1af1a8f7288bdc8  /tmp/foster2-before.txt
241136945222d7e251c1a2c2e085526f28bb205aa9582c71c1af1a8f7288bdc8  /tmp/foster3-before.txt
```

### Step 2 — after extraction and diff

```
/tmp/foster3-after.txt: sha256=241136945222d7e251c1a2c2e085526f28bb205aa9582c71c1af1a8f7288bdc8
/tmp/foster3-after.txt.sorted: sha256=efa5e961cf7cf0517eec056180eaa15100cc9b3a262be0d613d6342b9f68ece5
lines=1022
=== ordered diff ===
ordered diff exit: 0
=== sorted diff ===
sorted diff exit: 0
```

`diff /tmp/foster3-before.txt /tmp/foster3-after.txt` produced **no output**.
`diff` of the sorted extractions also produced **no output**.

**The claim-surface diff is empty.** The before/after sha256 of the ordered
extraction are identical
(`241136945222d7e251c1a2c2e085526f28bb205aa9582c71c1af1a8f7288bdc8`), and of
the sorted extraction identical
(`efa5e961cf7cf0517eec056180eaa15100cc9b3a262be0d613d6342b9f68ece5`). Every
`\label` name, every `\ref`/`\eqref`/`\cref`/`\Cref` argument, every
`\cite`/`\citep`/`\citet` key, and every numeric literal in text and math is
unchanged by this cycle.

### Step 3 — comparison against the last commit (`HEAD` = `8d83726`)

For each edited file, `git show HEAD:<file>` was piped through the same
tokenizer and compared with the working-tree file on disk.

```
=== main.tex ===
token counts: HEAD=234 disk=238
--- ordered diff (HEAD vs disk) ---
+ref	\cref{sec:finite-biot}
+ref	\eqref{eq:reduced-energy}
+ref	\eqref{eq:legendre-energy}
+ref	\cref{sec:work-equivalence}
label: HEAD=41 disk=41 | HEAD-only=(none) | disk-only=(none)
ref:   HEAD=28 disk=31 | HEAD-only=(none) | disk-only=['\cref{sec:work-equivalence}',
        '\eqref{eq:legendre-energy}', '\eqref{eq:reduced-energy}']   (unique values;
        occurrence counts HEAD=37 disk=41)
cite:  HEAD=22 disk=22 | HEAD-only=(none) | disk-only=(none)
num:   HEAD=27 disk=27 | HEAD-only=(none) | disk-only=(none)

=== sections/limits.tex ===
token counts: HEAD=42 disk=42
--- ordered diff (HEAD vs disk) ---
(empty)
label: HEAD=9 disk=9 | ref: HEAD=4 disk=4 | cite: HEAD=0 disk=0 | num: HEAD=7 disk=7
(all set and occurrence differences empty)

=== sections/pore_fabric.tex ===
token counts: HEAD=221 disk=222
--- ordered diff (HEAD vs disk) ---
+ref	\cref{sec:fabric-biot}
label: HEAD=25 disk=25 | HEAD-only=(none) | disk-only=(none)
ref:   HEAD=26 disk=26 | HEAD-only=(none) | disk-only=(none)
        (unique values identical; occurrence counts HEAD=43 disk=44)
cite:  HEAD=2 disk=2 | HEAD-only=(none) | disk-only=(none)
num:   HEAD=10 disk=10 | HEAD-only=(none) | disk-only=(none)
```

**Interpretation — every `HEAD`→disk difference predates all three cycles and
none comes from my edits.**

- My own before/after diff (Step 2) is **empty**, so this cycle added or removed
  no label, ref, cite or number token. In `main.tex` the four extra `ref`
  occurrences sit at lines 242–244 (`\cref{sec:finite-biot}`,
  `\eqref{eq:reduced-energy}`, `\eqref{eq:legendre-energy}`) and line 251
  (`\cref{sec:work-equivalence}`) — the §2 notation key and §3, spans this cycle
  did not touch. In `sections/pore_fabric.tex` the one extra `ref` occurrence sits
  at line 217 (`\cref{sec:fabric-biot}`, in §7.4); my only `pore_fabric.tex` edit
  is in §7.1 at lines 69–73 and contains no reference token.
- These are **pre-existing uncommitted changes**: the working-tree surface at the
  start of cycle 1 (`/tmp/foster1-before.txt`), cycle 2
  (`/tmp/foster2-before.txt`) and this cycle (`/tmp/foster3-before.txt`) are all
  the same sha256
  (`241136945222d7e251c1a2c2e085526f28bb205aa9582c71c1af1a8f7288bdc8`), so the
  `HEAD`→disk difference already existed at cycle-1 start. Cycle 2's memo
  identified the identical four `main.tex` tokens as pre-existing uncommitted
  work located outside its edited spans.
- I state explicitly: **no difference between `HEAD` and disk in labels, refs,
  cites or numbers originates from this cycle.** For `sections/limits.tex` the
  `HEAD`→disk surface is byte-identical in every category.

### Step 4 — rebuild

Command (exactly as specified):

```sh
latexmk -g -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

```
EXIT=0
Output written on main.pdf (33 pages, 2807652 bytes).

pages: 33
Overfull hbox:   0
Underfull hbox:  1
undefined ref/cite (Warning): 0
Missing character: 0
LaTeX Warning: 0
```

The one Underfull line is
`Underfull \hbox (badness 1137) in paragraph at lines 33--40` in
`build/main.log`; it is the abstract paragraph, present identically in the
baseline builds recorded in cycles 1 and 2 (same badness 1137), and not
introduced by these edits. Page count is 33, the same as the cycle-1/2 baseline.

Render check: `pdftotext build/main.pdf` contains each revised sentence, e.g.
"We write the distention gradient as a dilation times a proper rotation", the
split "The orientation of the pore fabric relative to the mineral therefore
enters as prescribed material data …", "The mineral-volume equation couples
mineral volume to the shape of the …", and "the volumetric law of Gajo's model".

Equation-numbering check: the `\newlabel{eq:…}` table in `build/main.aux` was
compared with the baseline table copied at cycle 1
(`/tmp/foster1-aux-before.aux`): 212 labels in both, no label added or removed,
and no equation renumbered (`diff` exit 0). The rendered equation-number
sequence is unchanged.

(Build note, recorded for completeness: the first build attempt failed with
`EXIT=12`, `! Package embedfile Error: File
'build/anisotropic-biot-2026-09-20-v2.zip' not found`, because I cleared the
ignored `build/` output directory before building and it also held the embedded
numerical-supplement archive and the `conformal/`, `fabric/` and
`weighted-stress/` figure PDFs that the manuscript includes. Those generated
inputs were restored from the round-32 review snapshot and the mandated build
then completed with `EXIT=0`. No manuscript source or included artifact was
altered; only generated files under `build/` were restored.)

---

## 5. Consistency of the three cycles as a whole

Read end to end, the three cycles now use one voice and one expository
sequence. Cycle 1 opened the abstract close, the Introduction's physical
distinction, the §3 energy inputs and the appendix; cycle 2 gave §6 its
roadmap, §9 its experiment openings and §8 its first-person-plural methods
voice; cycle 3 completes the arc by finishing the abstract's opening
decomposition, the concluding discussion's two summary sentences, and the two
residual nominalizations, and by splitting one run-on in §7.1. Authorial actions
are consistently first-person plural ("We derive", "We write", "We consider",
"we accumulate"), while derivations keep the operation, equation or physical
quantity as subject ("Differentiating \(W''\) … gives", "The balance gives").
Every revised bridge states purpose before relation and consequence after it,
and the only apparently duplicated material is the abstract/body/conclusion
restatement of the tensorial distention law — the intended summary layering, not
a repeated neighbouring explanation. The claim surface is byte-identical across
all three cycles.

## 6. Status

Files changed: `main.tex`, `sections/limits.tex`, `sections/pore_fabric.tex`.
No other file was modified (in particular, not `figures/`, `fe-evidence/`,
`tools/`, `site/`, `references.bib`, or any other file under `reviews/`; the
pre-existing working-tree modifications to `examples/`, `figures/`, `site/` and
`tools/` listed by `git status` predate this cycle and were not touched). The
only generated files written are under the ignored `build/` directory, as the
build requires. Claim surface: **identical** (empty before/after diff). Build:
**pass**, 33 pages, no new diagnostics. This memo is
`reviews/round-32/foster-cycle-3.md`.

Not performed (recorded rather than asserted): the held suites under
`validation/` and `examples/verify_*.py` were not run, and no scientific claim
was re-derived; this cycle is prose-only by contract.
