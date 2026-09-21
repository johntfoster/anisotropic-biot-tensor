# Round 30 — author response

Snapshot `ade4ec319cd757abad15546bd307efe2d9f85b2df21aa075bd74fb9ba4f0658b`
(592 files), HEAD `b6d7272`, 34-page build.
Reviews: `reviews/round-30/reviewer-{1,2,3}.md`. SIMULATED AI PEER REVIEW.

## Verdict tally on the round-30 snapshot

| Reviewer | Emphasis | Verdict |
| --- | --- | --- |
| 1 | derivation and correctness | MINOR REVISION |
| 2 | numerical verification and source fidelity | MINOR REVISION |
| 3 | exposition, notation and claims | MINOR REVISION |

**0 exact ACCEPT.** The round does not satisfy the >=2 criterion; a revision round is
required. All three reviewers confirmed `sha256(snapshot/source-manifest.json)` equals the
declared SNAPSHOT_ID, re-hashed all 592 listed files with zero mismatches and zero missing
listed files, reported no exposure to any other report, and used the held suites only as
recorded evidence. No independence incident was recorded in this round.

### Relationship to round 29 (loop guard)

None of the eight required items is a bare recurrence of a round-29 required item:

- R1-C1 is a different clause in `sections/pore_fabric.tex` from the round-29 R1-C1
  (that one was the "so it commutes with rotations about m" inference, already fixed).
- R3-C2 and R3-C3 extend the round-29 R3-C2, which fixed only the *frame* meaning of the
  distention stress; the new asks are the *anchor* of the whole bar rule and the
  *normalization* of each barred stress, neither of which the round-29 edit addressed.
- R3-C4 follows the round-29 R1-N1, which required the two axial-shear modes to be named;
  they were named but never labelled `e_4`, `e_5` and were written without the `sqrt2`.
  The normalization defect is new evidence.

Each carries new evidence or a new argument, so none is stopped under the loop guard.

## Response matrix

Every substantive comment, its evidence, disposition, the source change or reasoned
rebuttal, and how the change was verified.

### Required changes — all resolved

| ID | Comment | Evidence checked before editing | Disposition | Verification |
| --- | --- | --- | --- | --- |
| R1-C1 | `sections/pore_fabric.tex` §7.4 said of the equilibrium potential that "the potential does not depend on the complementary modes". | True of `W_dis` only. The minimized potential is `W_dis + phi_s0 W_s(Fbar) + phi_s0 p Jbar` and `Fbar = G^{-1/2} R_A^T F`, so a complementary distention increment changes `Fbar` and therefore `W_s`. Confirmed at lines 205–209. | **FIXED.** The clause now reads "the distention energy is independent of the complementary modes; those modes are dropped from the minimization by construction and frozen to the mineral rather than equilibrated", and the following sentence says the *distention* potential is strictly convex. | Rebuilt; the restriction, the strict convexity and the unique stationary point are unchanged; no symbol or equation touched. |
| R2-C1 | All 19 pore-fabric `provenance.json` records declared `git_revision ab46ebe…`, which cannot contain the fabric sources, and carried no `source_sha256`/`binary_sha256`. | Confirmed: `git cat-file -e ab46ebe:moose_app/src/materials/FabricMaterial.C` fails; the fabric files are added at `6385889`; 19/19 fabric-style records had `git_revision` only, while 38/38 runtime records had `source_sha256`+`binary_sha256`. The recorded `recorded_utc` (2026-09-21T02:56Z) precedes the fabric commit, so the runs were made from an uncommitted working tree. | **FIXED** by the reviewer's first-listed remedy. Both harnesses (`tools/rerun_fabric_decks.py`, `tools/rerun_fabric_contours.py`) now also record `binary_sha256`, `input_sha256`, and a three-file `source_sha256` map, and all 19 decks were re-run so the recorded `git_revision` is the current revision that does contain the fabric sources. | Deck outputs are byte-reproducible: `fabric_probe_iso/solution.csv` and `fabric_contour_iso/solution.csv` are byte-identical to the superseded runs, and every Exodus field array is bit-identical (only file metadata differs). Recorded `binary_sha256` `ff0272fc…` matches the shipped application digest; the three `source_sha256` values match `git show HEAD:<path>`. `fe-evidence/manifest.json` regenerated: 57 cases, 317 files, all digests resolve. The quoted 4.36/4.99/5.52/3.62e-5 and 3.61/4.35/4.97/5.50e-5 are unchanged. |
| R2-C2 | `build/weighted-stress/derivation-scan.json` and `display-scan.json` are declared `.json`, ship in the supplement, are not parseable JSON, and embed `/home/john/...` paths. | Confirmed: `file` reports ASCII text, `json.load` raises `JSONDecodeError`, and both begin with an absolute host path. | **FIXED.** Both are renamed to `.txt`, the absolute host prefix is rewritten to the repository-relative path (zero `/home/` occurrences remain), and `tools/package_numerical_supplement.py` now ships `.txt` alongside the other suffixes. | Supplement rebuilt: 69 files, `9643b64b…`; both `.txt` logs present, the superseded `.json` names absent. |
| R3-C1 | Figures 6–11 (`[t]` floats in §9) were deferred past the References to pp. 31–34. | Confirmed from the rendered PDF: six `\begin{figure}[t]` in `sections/finite_elements.tex`, no `\clearpage` before the bibliography. | **FIXED** with the reviewer's `placeins`/`\FloatBarrier` option: `\usepackage{placeins}` added and `\FloatBarrier` placed at the end of §9. | Rebuilt; Figures 6–11 now render on pp. 25–28, inside §9 and before the References; pages 20–28 carry §9 and its floats. |
| R3-C2 | The §2 bar rule was anchored to `eq:spherical-distention` (the conformal factor), but §7 uses bars against the general distention. | Confirmed at `main.tex` lines 216–217; §7 defines `Fbar = G^{-1/2} R_A^T F`. | **FIXED.** The rule is now stated against the general `eq:true-mineral-jacobian` decomposition, "of which the conformal factor `eq:spherical-distention` is the specialization". | Rebuilt; the §7 barred quantities now read against the general rule. |
| R3-C3 | The bar-on-stress rule gave only the frame change, not the differing normalizations of the barred stresses. | Confirmed: `barsigma_s` is per current mineral volume, `bartau_s = Jbar barsigma_s` per reference mineral volume, `barS_dis` per reference mixture volume. | **FIXED.** The notation paragraph now states each normalization explicitly. | Rebuilt; §7 and §2 agree on the three normalizations. |
| R3-C4 | The `e_1..e_6` basis was declared orthonormal but `e_4`, `e_5` were unlabelled and the axial-shear modes lacked `sqrt2`. | Confirmed: `|sym(m⊗p_i)|^2 = 1/2`, so the declared orthonormality fails as written; only four labels were given. | **FIXED.** The modes are labelled `e_4 = sqrt2 sym(m⊗p_1)` and `e_5 = sqrt2 sym(m⊗p_2)`. | Rebuilt; all six members are unit-norm and mutually orthogonal. |
| R3-C5 | "The minimization in `eq:fabric-equivalent-energy`" pointed at the energy definition, not the potential that prescribes the minimization. | Confirmed at `sections/pore_fabric.tex` lines 273–275; the same paragraph correctly cites `eq:fabric-equilibrium` two sentences later. | **FIXED.** The reference is retargeted to `eq:fabric-equilibrium`. | Rebuilt; `cleveref` resolves the new target. |

### Optional notes

| ID | Note | Disposition |
| --- | --- | --- |
| R1-O1 | "equivalently" is not an equivalence in the transverse-isotropy sentence. | **APPLIED.** Replaced by "and, concretely,". |
| R1-O2 | Eq. (22) does not literally contain `(1/3)tr tau'`. | **APPLIED.** The text now adds "— equivalently, the trace of `eq:constitutive-kirchhoff-phase-stress` —". |
| R1-O3 | (22)–(23) is a consistency check that presupposes (12). | **APPLIED.** The text now says the second line uses "pressure equilibrium, the trace form of `eq:constitutive-kirchhoff-phase-stress`". |
| R1-O4 | Tie eq. (37)'s pressure interval to condition (38). | **RETAINED.** The text already qualifies the integration as holding on an admissible interval containing zero; adding the root-existence condition is a restatement, not a correction. |
| R2-C3 | No run record carries both a revision and source digests. | **PARTIALLY APPLIED.** The 19 fabric-style records now carry revision + input + source + binary digests, so they satisfy the uniform schema. The 38 runtime records still carry no `git_revision`; adding it requires re-running them from the ignored runtime harness, which is outside this round. The residual asymmetry is recorded in `fe-evidence/manifest.json`. |
| R2-C4 | Two distinct copies of the manufactured-solution analysis. | **APPLIED.** A note in `fe-evidence/manifest.json` records that the `fe-evidence/` and `site/reports/` copies are deliberately separate and are not expected to share a digest. |
| R2-C5 | `provenance/manuscript-export.json` names four paths absent from the snapshot. | **APPLIED.** The manifest's own description already scopes it to the public paper repository; to remove the ambiguity the four present, tracked paths (`.latexmkrc`, `Makefile`, `agent_environment`, `agent_workflows`) are now included by `tools/build_review_snapshot.py`, so every declared path resolves in the snapshot. |
| R2-C6 | `braun2020` key with `year = 2021`. | **APPLIED.** The published year is 2021 (Rock Mech Rock Eng 54(1):377–396, confirmed against the publisher record), so the key is renamed `braun2021` and the citation in `main.tex` updated; the rendered reference is unchanged. |
| R2-C7 | `source_sha256` keys in the build reports are bare basenames. | **RETAINED.** Every digest resolves under `examples/`; the reports are generated by `examples/conformal_experiments.py`, and changing the key form would change recorded reports for no defect. |
| R3-C6 | Prime / double-prime conventions absent from the notation paragraph. | **APPLIED.** A one-line rule now defines the single prime (effective stress with the full pore-pressure term) and the double prime (fixed-pressure stress). |
| R3-C7 | Duplicated caveat in §9.4; "independent" used for a non-independent check. | **APPLIED.** The second caveat sentence is removed, leaving one; "An independent NumPy re-implementation" becomes "A separate NumPy re-implementation". |
| R3-C8 | Conclusion's temporal range reads stronger than §9.3's "near one". | **APPLIED.** §9.3 now states the range "between 0.98 and 1.40", matching the conclusion, with the no-order-above-one disclaimer retained. |
| R3-C9 | Tautological `h = e^{ln h}`. | **APPLIED.** Replaced by "exactly `ln h`, the logarithm of the unimodular transverse fabric eigenvalue, and not a projection of `h`". |
| R3-C10 | "distention" used in §1 before its definition. | **APPLIED.** §1 now names the distention gradient `A` with `J = a Jbar`, forward-referencing `eq:true-mineral-jacobian`. |
| R3-C11 | Near-colliding `mathbb{C}` and `mathbf{C}` glyphs. | **RETAINED.** The declared typography rule holds throughout; renaming the right Cauchy–Green tensor would touch every mechanical equation for a presentation preference. |
| R3-C12 | The notation paragraph resolves its rules through far-forward equations. | **RETAINED.** The rules are correct and the cross-references are the canonical statements; restating them in §2 would duplicate content the round-29 edit already restructured. |
| R3-C13 | Abstract antecedents. | **APPLIED.** "shares their modelling conventions" becomes "shares the same modelling conventions", and "The construction" becomes "The conformal construction". |
| R3-C14 | AI-use disclosure names "simulated peer review". | **RETAINED.** The disclosure names the activity accurately and the same paragraph already states that these reviews "do not constitute journal peer review"; relabelling it would weaken an accurate disclosure. |

## Verification performed in this revision round

```
python3 tools/rerun_fabric_decks.py
python3 tools/rerun_fabric_contours.py
python3 tools/register_fabric_evidence.py
python3 tools/package_numerical_supplement.py
python3 tools/populate_site_manifest.py
python3 tools/register_fabric_evidence.py          # re-run after populate (order matters)
python3 tools/build_verification_site.py
latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
python3 .agent/shared/tools/research_project.py check       # errors: []
python3 .agent/shared/tools/research_project.py links site  # {"errors": []}
python3 tools/agentctl check                                # passed
python3 tools/manuscript_release.py audit                   # rc=0
```

Outcomes: PDF rebuilt, 34 pages, 0 overfull boxes, 0 undefined references or citations,
0 missing-character warnings; Figures 6–11 moved into §9 (pp. 25–28); supplement archive
rebuilt, 69 files, `9643b64b…`; site manifests rebuilt (41 artifacts / 13 figures / 5 cases;
47 snapshot files; link check passed).

The held numerical suites (`validation/`, `examples/verify_*.py`) were not run, as scoped.
Executing the pore-fabric decks is not one of the held suites; it regenerates the recorded
evidence for the decks those suites consume.

Because scientific content changed (a corrected justification, a corrected notation rule,
a corrected basis definition, a citation-key correction, and regenerated run provenance),
no round-30 verdict carries forward; a new snapshot and a fresh independent round are
required.
