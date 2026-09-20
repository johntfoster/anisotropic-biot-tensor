# Simulated peer-review record

These are independent AI-agent manuscript reviews, not actual JMPS submissions,
editorial decisions, or forecasts of acceptance. Reviewers are instructed to
assess correctness, novelty, significance and engineering relevance without
inferring a desired outcome.

The user requested successive rounds of three reviewers, revisions responding
to each report, and a stop criterion of at least two ACCEPT verdicts on the
same current manuscript version. MINOR REVISION is not counted as ACCEPT.
Optional editorial suggestions can accompany ACCEPT. Substantive valid findings
are addressed even when another reviewer accepts; source changes require a new
round for verdicts on the revised manuscript.

Each round records source SHA-256 hashes, three reports, and an author response.
Generated PDF, figures, data and diagnostic output remain under build/.

## Subsequent author-requested typography change

Fourth-order stiffness and compliance symbols now use `\mathbb{}`;
second-order tensors retain upright bold `\mathbf{}`. Only the two
stiffness font substitutions changed manuscript content. Reversing them
exactly reproduces the previous TeX source. Persistent notation guidance was
updated, and the manuscript rebuilt without warnings with rendered equations
inspected. The archived review hashes identify the earlier typography;
no new scientific review was requested for this formatting change.

## Completed weighted-stress reconsideration (2026-09-19)

The user rejected the preceding reconstruction's departure from the source
stress/work argument and its notation and prose. The manuscript was rebuilt
around volume-fraction-weighted spatial phase stress, spherical distention,
and equivalent volumetric energy. Its full drained stiffness restriction is
derived explicitly. Earlier acceptance votes did not count toward this work.

| Round | Mathematics | Physics and source fidelity | Prose, notation, significance | Action |
| --- | --- | --- | --- | --- |
| 5 | ACCEPT | ACCEPT | ACCEPT | Three fresh independent reviews. Added useful optional full spatial converse, direct compliance proof, precise pore-volume contraction, and numerical error summary. |
| 6 | ACCEPT | ACCEPT | ACCEPT | All additions independently reassessed. Final page reading identified one pronoun ambiguity. |
| 7 | ACCEPT | ACCEPT | ACCEPT | All three verified the exact wording correction and that every equation, assumption, and code file remained unchanged. Final stop criterion satisfied. |

All reports have been read and assessed. No required or optional correction
remains. The reviewed scientific snapshot is `round-7/source-sha256.txt`;
verification and the requirement audit are in `round-7/`.
The archived round-7 manuscript PDF (13 pages) builds without warnings; it is a
superseded snapshot and is not the current manuscript. Full tensor stress/energy,
pressure and volume derivatives, reference limits, and finite unjacketed
compression pass independent checks.

The model retains spherical distention and therefore requires a spherical
additional drained compliance. It does not represent arbitrary independent
anisotropic stiffness pairs or anisotropy caused solely by pore shape in an
isotropic mineral. These are stated physical restrictions of the result.

## Archived stress-reconstruction revision (2026-09-18)

The superseded manuscript contained a logarithmic spring reconstruction.
Three reviewers independently assessed the same round-4
snapshot after the round-3 corrections.

| Round | Reviewer 1 | Reviewer 2 | Reviewer 3 | Action |
| --- | --- | --- | --- | --- |
| 3 | ACCEPT | MINOR REVISION | MINOR REVISION | Clarified phase-average stress, proved trace preservation, checked full tensor ordering for every example, and updated reproduction instructions. |
| 4 | ACCEPT | ACCEPT | ACCEPT | All reports assessed; no mandatory revisions remain. Stop criterion satisfied on that archived snapshot only. |

See `round-4/source-sha256.txt`, the three reports, `round-4/response.md`,
and `round-4/completion-audit.md` for the final evidence. The reference audit
covers all 23 new entries at explicitly stated evidence levels; original
full-text access remains incomplete. The construction requires the stated
series assumption and does not establish general microscopic phase localization.

## Completed rounds for the earlier formulation

| Round | Reviewer 1 | Reviewer 2 | Reviewer 3 | Action |
| --- | --- | --- | --- | --- |
| 1 | ACCEPT | MAJOR REVISION | ACCEPT | Addressed all substantive requests and optional verification clarifications; re-reviewed changed source. |
| 2 | ACCEPT | ACCEPT | ACCEPT | Stop criterion satisfied on the archived round-2 snapshot only. |

The round-2 response includes final build checks and the version-aware
Foster–Xu local-author-manuscript evidence addendum.
