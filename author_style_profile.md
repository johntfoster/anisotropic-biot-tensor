# Author profile for repository edits

Date revised: 2026-07-28

## Use

Read this profile before every repository edit. Apply the prose rules to all
manuscript text, captions, tables, source comments, documentation, and
agent-workflow material. For an edit containing no prose, use the profile to
avoid unnecessary terminology, notation, commentary, and scope changes.

This is an editing profile, not a license to imitate defects in working drafts.
Project instructions, accepted notation, and the author's explicit directions
take precedence.

## Provenance and scope

Adapted on 2026-09-19 from the author profile supplied in the authorized
companion manuscript repository. Its authorial guidance is retained here;
external sample paths and implementation-specific directions are omitted.
This profile is self-contained and does not authorize access to other papers.

## Characteristic voice

- Begin with the physical system or mathematical task. In an article-level
  introduction, establish the application and governing difficulty first. In a
  derivation, begin directly with the body, mixture, motion, balance, or
  constitutive quantity under consideration.
- At the beginning of a long section or chapter, state its purpose and identify
  how it uses the result established immediately before it. Give a roadmap when
  several distinct tasks follow.
- State the central contribution early and positively. Typical paper-level
  constructions are “We develop...,” “We derive...,” and “The central
  contribution is....”
- Move from a familiar continuum-mechanics statement to the required
  extension. Give the physical reason for the extension before its detailed
  notation.
- Keep the derivation equation-forward. Introduce the operation, display the
  equation, define its symbols locally, and state the immediate consequence.
- Use concrete mathematical subjects and verbs: “the balance gives,” “the
  constraint yields,” “substitution produces,” “summing the phase equations
  gives,” and “the small-strain limit recovers....”
- Interpret a formal result physically after deriving it. When useful, follow
  that interpretation with a limiting case, benchmark, or experimentally
  observable consequence.
- Explain procedural choices by connecting them to the quantity being measured,
  derived, or validated. Include enough detail for the reader to understand why
  the chosen construction serves that purpose.
- Distinguish derived results, constitutive choices, specializations, and
  assumptions explicitly.
- Conclude by restating the construction, its principal physical consequence,
  the checks or reductions performed, and the next scientifically meaningful
  extension.
- For a long work, close major sections locally instead of postponing every
  interpretation to the final conclusion. Use the final conclusion to assemble
  those results into the overall contribution.

## Sentence and paragraph habits

- Use ordinary technical English and mostly moderate-length sentences.
  Technical paragraphs may be compact, but each should perform one recognizable
  task.
- Use first-person plural for paper-level actions and choices. Within a
  derivation, prefer the equation, balance, constraint, or physical quantity as
  the subject.
- Use short transitions such as “Here,” “Thus,” “Then,” “Substituting,”
  “Summing,” and “In this limit” when they identify a real mathematical step.
  Vary them rather than repeating the same transition in adjacent paragraphs.
- Place definitions immediately before or after first use. A reader should not
  have to search several paragraphs ahead to decode a symbol.
- Let equations remain grammatical parts of their sentences. The prose before
  a display should say why the equation is needed; the prose after it should
  say what follows.
- Prefer a paragraph that states a claim, supplies the mathematical or physical
  basis, and gives the implication over a paragraph that inventories features.
- Use a concrete example or analogy when it makes an unfamiliar formal
  distinction visible, but return promptly to the governing variables and
  equations.

## Just-in-time exposition

- Introduce notation only when the corresponding physical idea or derivational
  step becomes active.
- Do not collect symbols, constitutive quantities, or terminology in an early
  section merely because they will be needed later.
- Define a symbol within one or two paragraphs of its first substantive use.
  If a far-future closure must be mentioned, describe its role anecdotally
  without using its undeveloped notation.
- Refer to an appendix when a detailed prerequisite would interrupt the main
  argument. State the result needed in the body and leave the full derivation
  in the appendix.
- Use an appendix for supporting derivations, supplementary definitions, and
  validation details that are necessary for reproducibility but would obscure
  the main line of argument.
- In an equation paragraph, use this order when possible: physical purpose,
  equation, local definitions, consequence, and limiting interpretation.
- Do not introduce a named helper quantity when the existing primitive
  variables state the result clearly.

## Positioning prior work and the present contribution

- Describe affirmatively what a cited theory, experiment, or model establishes.
  Then state what the present paper derives or applies.
- Do not build novelty by listing what earlier work lacks, what the current
  model is not, or what inspected formulations fail to contain.
- Avoid constructions such as “unlike prior models,” “does not present,”
  “has not developed,” “not merely,” and “not ad hoc.”
- Use negation only when it conveys necessary scientific content: a
  mathematical condition, an operative assumption, a distinction between
  easily confused quantities, an excluded physical mechanism, or a limitation
  that prevents misinterpretation.
- Do not insert commentary from author-agent discussions, drafting history,
  prior versions, review strategy, or discarded formulations into the paper.

## Vocabulary and symbols for this manuscript

Use “solid intrinsic density,” “solid volume fraction,” “mineral volume,”
“distention,” and “fixed-pressure derivative” for those physical quantities.
Distinguish current mixture volume, reference mixture volume, and reference
mineral volume when expressing work or energy. Use the companion's physical
symbols wherever their meanings agree. Fourth-order tensor symbols use
`\mathbb{}`. Second-order tensors and vectors are upright bold using
`\mathbf{}`; do not use `\bm` or `\boldsymbol` for tensors. Use an upright Greek math setup if Greek tensor symbols
are retained, and inspect the rendered result. Do not rename a tensor only
to simplify typography. Introduce no helper symbols unless essential to the
result or explicitly approved by the author.

## Draft artifacts not to imitate

- Conversational work-note phrasing such as “we'll rewrite,” “we now fix,” “as
  requested,” “this repair,” or “for reasons that will be made clear.”
- Placeholder references, incomplete captions, compressed sentence fragments,
  and grammatical errors present in draft PDFs.
- Abrupt formalism before the reader knows the physical or mathematical
  question.
- Repeated “Thus,” “Hence,” or “Therefore” where the logical relation can be
  stated directly.
- Unsupported claims of novelty, generality, completeness, or experimental
  accessibility.
- Long literature inventories whose only purpose is to contrast the paper with
  absent features.
- Dissertation-era habits that weaken current prose, including excessive
  authorial qualification, informal judgments such as “obvious” or “very
  simple,” and repeated announcements that a result is novel.

## Technical preservation rules

- Preserve accepted equations, symbols, labels, citations, and constitutive
  distinctions unless the task explicitly changes them or a technical audit
  identifies an error.
- Preserve the distinction between intrinsic and bulk solid density and between
  the reference Biot tensor and its finite-deformation value.
- Preserve solid mass conservation and the mineral equation as solved equations
  in the numerical presentation.
- Improve the explanation adjacent to an equation before adding notation.

## Pre-edit and review checklist

Before editing:

1. What exact reader-facing problem does this edit solve?
2. Which symbols and concepts are already defined at this location?
3. Can the change use existing notation and terminology?
4. Does the proposed prose state what the theory does, without discussing what
   earlier drafts or other models do not do?

After editing:

1. Is every new symbol defined within one or two paragraphs of first
   substantive use?
2. Does each forward reference remain anecdotal unless the cited equation or
   definition is nearby?
3. Does each equation paragraph explain purpose, local notation, and immediate
   consequence?
4. Does the prose distinguish definitions, derived restrictions, constitutive
   closures, specializations, and validation needs?
5. Were accepted equations, labels, citations, and thermodynamic distinctions
   preserved?
6. Is all drafting-history and discussion-local commentary absent?
7. Does any sentence establish importance by saying what another formulation
   lacks or what the present model is not? If so, rewrite it affirmatively.
