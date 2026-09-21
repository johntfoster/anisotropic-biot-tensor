# Foster engineering review — cycle 1 of 3

Manuscript: `main.tex` (+ `sections/*.tex`, `provenance/ai_use_statement.tex`)
Working tree: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
Skills applied: `foster-engineering-reviewer`, `foster-technical-prose`
Scope of this cycle: **prose revision only** at conceptual bridges. No equation,
label, reference, citation, number, symbol, unit, assumption, scope statement or
claim was changed.

Triage: `python3 .agent/shared/tools/review_scan.py` over `main.tex`, `sections/*.tex`
and `provenance/ai_use_statement.tex`. Every file returned `"findings": []` except
`sections/logarithmic_derivative.tex`, which returned one candidate,
`unnumbered-display` at line 35 (`\[`). That candidate is the `\\[5pt]` row
separator inside the `cases` environment of `eq:log-frechet-spectral-form`,
i.e. equation content, which this contract forbids touching. It was assessed and
deliberately left unchanged.

---

## 1. Scope revised (file, section, passage)

| # | File | Section / anchor | Passage |
|---|------|------------------|---------|
| 1 | `main.tex` | Abstract, final paragraph | Closing sentence of the abstract |
| 2 | `main.tex` | §1 Introduction, "We consider an anisotropic mineral…" | Dilation/rotation distinction before the formal distention |
| 3 | `main.tex` | §3 Reversible work and the equivalent energy | Purpose sentence before the distention-energy assumption (`W_A(a)`) |
| 4 | `main.tex` | §3, after `eq:equivalent-volumetric-work` | Origin of the factor `φ_{s0}` |
| 5 | `sections/stress_reconstruction.tex` | §4, after `eq:prescribed-logarithmic-energies` | What "the first"/"the second" normalize |
| 6 | `sections/stress_reconstruction.tex` | §4, before `eq:anisotropic-energy-pressure-derivative` | Pressure equilibrium at fixed `F` |
| 7 | `sections/stress_reconstruction.tex` | §4, before `eq:drained-stiffness-restriction` | Role of the spherical drained path |
| 8 | `sections/logarithmic_derivative.tex` | Appendix, opening | Purpose/setup of the matrix derivative |
| 9 | `sections/logarithmic_derivative.tex` | Appendix, before `eq:logarithmic-stress-trace-expansion` | Self-adjointness and the `C → I` action |
| 10 | `sections/pore_fabric.tex` | §7.5 (`sec:fabric-biot`), before `eq:fabric-additive-strain` | Relaxation of the rank-one restriction |
| 11 | `sections/limits.tex` | §6.3 Equal confining pressure and pore pressure | Unjacketed setup and state selection |
| 12 | `sections/experiments.tex` | §9, plane-traction paragraph | Purpose of the Biot tensor for plane traction |

## 2. Explanatory changes made, and why

The profile sequence is *purpose → equation → definitions → implication → limiting
case*, with the physical distinction stated before its formal representation and
opaque nominalizations replaced by a physical subject and an active verb.

1. **Abstract (1).** The sentence previously ended on a scope negation ("…and no
   relative rotation of the fabric and the mineral matrix represented"). The
   *same* content was reordered so the qualifier precedes the positive result,
   and the sentence now closes on what the construction yields ("yields an
   anisotropic Biot tensor driven by both mineral and pore-fabric anisotropy").
   This follows the profile rule to close constructively and to avoid ending on a
   negation unless necessary. No claim was added or removed.
2. **Introduction (2).** "This conformal distention changes pore volume…" blended
   two distinct physical effects into one subject. The dilation (volume change,
   shape of the mineral held fixed) and the rotation (change of representation
   frame) are now named separately, and "it" became the unambiguous
   "that rotation". This is the physical-distinction-before-formal-representation
   move.
3. **§3 (3).** Added a one-sentence purpose for the distention energy ("The
   distention energy is the remaining constitutive input") immediately before the
   assumption, satisfying purpose-before-equation; the assumption wording itself
   is unchanged. The conversational "we now…" form was deliberately avoided.
4. **§3 (4).** "The distinction between reference mixture volume and reference
   mineral volume accounts for the factor `φ_{s0}`" named the cause but not the
   mechanism. It now states the mechanism (mineral energy normalized per
   reference mineral volume, skeleton work per reference mixture volume), which
   is exactly the distinction the profile asks to be made explicit.
5. **§4 (5).** "The first … the second …" left the referents implicit. Both
   energies are now named with the volume they are normalized by, giving
   definitions local to the equation.
6. **§4 (6).** Passive "Pressure equilibrium is enforced by differentiating…"
   became an active construction, and the terse "Both `J` and skeleton shape then
   remain fixed while distention changes…" now states the fixed variable (skeleton
   deformation) and that the distention changes *only* through the mineral volume.
7. **§4 (7).** "The spherical drained path fixed `W_A`" was a clipped,
   verbless nominalization. It now reads as a relation with a subject and verb
   ("determines the distention energy `W_A`") and states what the next step
   requires.
8. **Appendix (8).** The opening introduced `C = FᵀF` and `ε = ½ log C` as bare
   symbols. They are now identified as the right Cauchy–Green tensor and its
   logarithmic strain — terminology already used elsewhere in the manuscript —
   before they are used.
9. **Appendix (9).** "The derivative maps `C` to `I`" was an unlabelled jump. The
   object is now named ("the metric `C` … the identity `I`"), keeping the
   subsequent trace consequence as the stated implication.
10. **§7.5 (10).** "The rank-one structure of the conformal compliance restriction
    relaxes" was an opaque nominalization. It now gives the physical reason (the
    conformal distention energy depends only on volume), states that the retained
    subspace is wider, and keeps both `\eqref` targets exactly where they were.
11. **§6.3 (11).** The unjacketed preamble read "The solid and mixture should then
    have the same homogeneous stretch". It now reads "In that experiment the solid
    and the mixture reach the same homogeneous stretch", and state selection is
    stated as "We therefore choose a state satisfying" — a concrete experiment
    before the formal path definition.
12. **§9 (12).** "The tensor also gives the pressure sensitivity of traction on a
    plane" had an indefinite subject. It is now "The Biot tensor also determines
    how a pressure change alters the traction on a plane", a physical subject with
    an active verb.

## 3. Passages deliberately left unchanged, and why

- **`main.tex` §2 notation key (the bar/prime/`dis` paragraph).** This is a
  deliberate symbol inventory in which every clause carries a symbol, a
  reference, or a normalization convention. Rewriting it risks dropping a
  load-bearing symbol/normalization distinction for no reader benefit that a
  local edit can achieve; the profile also requires definitions to remain close
  to use, which the paragraph already enforces by pointing each marker at its
  first-use equation. Left as authored.
- **`main.tex` §1 literature survey.** Removing inventory-style citation runs
  would delete citations, which the hard contract forbids.
- **`sections/logarithmic_derivative.tex` line 35 (`\\[5pt]` in `cases`).** The
  only `review_scan.py` flag; it is equation content.
- **All displayed equations, `align` bodies, `\label`s, `\eqref`/`\cref`/`\Cref`
  targets, `\cite` keys, numeric literals, and every stated assumption, scope
  caveat, and verification/floor statement** (including the `3.2×10⁻³` floor,
  temporal orders `0.98`–`1.40`, `1.94` ratio, `186`/`273`/`65` check counts,
  and all material-point error magnitudes).
- **`sections/pore_fabric.tex` "Fixing the rotation has three consequences."**
  The paragraph is dense but every clause is a necessary scope statement, and
  the framing word "three" is part of the author's structure. Any restructure
  would either drop a scope statement (a claim change) or renumber the
  consequences; both are outside a prose-only contract. Left as authored.
- **`sections/finite_elements.tex`.** Reviewed in full; its conceptual bridges
  (purpose → equation → definitions → consequence, plus explicit limiting-case
  and scope paragraphs) already satisfy the profile, so no change was made.
  Editing for its own sake would risk the numeric claim surface.
- **`sections/experiments.tex` subsections other than (12).** Already in the
  profile's order (physical situation, equation, reading of the figure,
  limiting comparison); no non-cosmetic improvement was available.

## 4. Required proof — exact command output

### Step 1 — before extraction (labels, refs, cite keys, numeric literals)

Command: `python3 /tmp/extract_surface.py /tmp/foster1-before.txt`
(same extractor used before and after; walks `main.tex`, `sections/*.tex`,
`provenance/ai_use_statement.tex` in document order.)

```
/tmp/foster1-before.txt: sha256=241136945222d7e251c1a2c2e085526f28bb205aa9582c71c1af1a8f7288bdc8
/tmp/foster1-before.txt.sorted: sha256=efa5e961cf7cf0517eec056180eaa15100cc9b3a262be0d613d6342b9f68ece5
lines=1022
```

### Step 2 — after extraction and diff

```
/tmp/foster1-after.txt: sha256=241136945222d7e251c1a2c2e085526f28bb205aa9582c71c1af1a8f7288bdc8
/tmp/foster1-after.txt.sorted: sha256=efa5e961cf7cf0517eec056180eaa15100cc9b3a262be0d613d6342b9f68ece5
lines=1022
ordered diff exit: 0
sorted diff exit:  0
```

`diff /tmp/foster1-before.txt /tmp/foster1-after.txt` produced **no output**.
`diff` of the sorted extractions also produced **no output**.

**The claim-surface diff is empty.** The before/after sha256 of the ordered
extraction are identical (`241136945222d7e251c1a2c2e085526f28bb205aa9582c71c1af1a8f7288bdc8`),
and of the sorted extraction identical
(`efa5e961cf7cf0517eec056180eaa15100cc9b3a262be0d613d6342b9f68ece5`). Every
`\label` name, every `\ref`/`\eqref`/`\cref`/`\Cref` argument, every `\cite`/
`\citep`/`\citet` key, and every numeric literal in text and math is unchanged.

### Step 3 — rebuild

Command (exactly as specified):

```sh
latexmk -g -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

```
EXIT=0
Output written on main.pdf (33 pages, 2807257 bytes).

pages: 33
Overfull: 0
Underfull: 1
undefined ref/cite: 0
Missing character: 0
LaTeX Warning count: 0
```

The one Underfull line is `Underfull \hbox (badness 1137) in paragraph at
lines 33--40` in `build/main.log`; it is present identically in the baseline
build of the unmodified source (`/tmp/foster1-log-before.txt`) and is not
introduced by these edits. Exit code of the baseline build was also 0 (33 pages,
0 Overfull, 1 Underfull, 0 undefined, 0 missing character), so this cycle
changed no build diagnostic.

### Step 4 — rendered equation numbers did not move

Equation numbers were read from the `.aux` label table before
(`/tmp/foster1-aux-before.aux`, copied from the baseline build) and after
(`build/main.aux`).

```
eq-label sequence diff exit: 0
eq labels compared: 106
```

(Plus the full `eq:…` `\newlabel` set including `@cref` companions:
`diff /tmp/b.full /tmp/a.full` → `FULL DIFF exit=0`.)

Every one of the 106 equation labels maps to exactly the same rendered equation
number before and after, and the ordered equation-number sequence is identical.
No equation was added, removed, reordered, or renumbered.

## 5. Status

Files changed: `main.tex`, `sections/stress_reconstruction.tex`,
`sections/logarithmic_derivative.tex`, `sections/pore_fabric.tex`,
`sections/limits.tex`, `sections/experiments.tex`.
No other file was modified (in particular, not `figures/`, `fe-evidence/`,
`build/`, `tools/`, `site/`, `references.bib`, or any other file under
`reviews/`). Claim surface: **identical** (empty diff). Build: **pass**, 33
pages, no new diagnostics. This memo is
`reviews/round-32/foster-cycle-1.md`.

Not performed (recorded rather than asserted): the held suites under
`validation/` and `examples/verify_*.py` were not run, and no scientific claim
was re-derived; this cycle is prose-only by contract.
