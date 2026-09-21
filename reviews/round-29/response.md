# Round 29 — author response

Snapshot `8aff33630cf27ac2727729471b38529c10f23edb1d6a5f90f2553c5b7f8726d7`
(592 files), HEAD `97e862b`, 34-page build.
Reviews: `reviews/round-29/reviewer-{1,2,3}.md`. SIMULATED AI PEER REVIEW.

## Verdict tally on the round-29 snapshot

| Reviewer | Emphasis | Verdict |
| --- | --- | --- |
| 1 | derivation and correctness | MINOR REVISION |
| 2 | numerical verification and source fidelity | MINOR REVISION |
| 3 | exposition, notation and claims | MINOR REVISION |

**0 exact ACCEPT.** The round does not satisfy the >=2 criterion; a revision round is required.

### Independence incident (recorded)

Reviewer 1 self-reported that, while establishing its report format, it opened
`reviews/round-29/reviewer-3.md` and read roughly its first 70 lines before stopping,
and that it did not open `reviewer-2.md` or any prior-round report. Reviewer 1's return is
therefore **not counted as an independent vote**, and a **fresh reviewer 1** is spawned for the
next round. Because reviewer 1 returned MINOR REVISION rather than ACCEPT, the exposure did not
manufacture an acceptance. Reviewer 1's required item R1-C1 was independently re-verified by the
author below before any edit. Reviewers 2 and 3 reported no exposure.

## Response matrix

Every substantive comment, its evidence, disposition, the change made or the reasoned rebuttal,
and how the change was verified.

### Required changes — all resolved

| ID | Comment | Evidence checked | Disposition | Verification |
| --- | --- | --- | --- | --- |
| R1-C1 | `sections/pore_fabric.tex` (sec:fabric-biot), the clause "it annihilates ... `e_3` and `e_6`, **so it commutes with rotations about `m`**" states an invalid inference. | Annihilation of `e_3`, `e_6` only puts them in `ker D`; a tensor `D + s_1⊗s_1` with `s_1 = sym(m⊗p_1)` annihilates both yet is not invariant under rotations about `m`, which mix `s_1` and `s_2`. Transverse isotropy of `D` is what the paper relies on elsewhere. | **FIXED.** Rewritten to give the true reason (both `e_1 = I/√3` and `e_2 = √(3/2)(m⊗m − I/3)` are invariant under rotations about `m`), with annihilation of the four complementary modes as a consequence, now naming the two axial-shear modes as well. | Rebuilt; the section still supports eq. `fabric-transverse-biot`; no new symbol introduced; `latexmk` exit 0. |
| R2-C1 | `figures/fe-verification-plot-manifest.json` declared `input_sha256["fe-evidence/mms-convergence.json"] = 87e1d95b…`, which does not resolve; the actual shipped digest is `de2ca677…`. | Confirmed: the only difference between the digest the manifest recorded and the shipped file is `runs_dir` (absolute → `fe-evidence/runs`, commit `6385889`), a string the plot does not read. `fe-evidence/manifest.json` already declared `de2ca677…`. | **FIXED** by regeneration (the reviewer's first-listed remedy). `python3 examples/plot_fe_verification.py` re-run; the manifest now records every input and output digest of the shipped tree, and its `versions` block (`python 3.10.12 / numpy 2.2.6 / matplotlib 3.10.8`) now matches the other two figure manifests. | All 6 input and all 4 output digests re-verified to resolve; figure data unchanged; regenerated panels inspected and render correctly; figure pixel difference vs the superseded rendering is <1% of pixels (text rasterisation only). |
| R3-C1 | A superscript `d` was declared for the drained skeleton (`C^d`) while the drained energy was written `W_dr`, though the text says "the two labels are kept distinct throughout". | Confirmed in `main.tex` (notation paragraph) and `sections/stress_reconstruction.tex` lines 34, 45, 49, 201. | **FIXED** by the reviewer's first-listed option: the drained energy is renamed `W_dr → W^d` at all four occurrences, and the notation paragraph now names both `C^d` and `W^d` under the superscript-`d` convention. | Rebuilt; `W_{\mathrm{dr}}` no longer occurs in the sources; no equation content changed (a symbol rename only). |
| R3-C2 | `\bar S_dis` was described as an intermediate-frame stress per reference mixture volume, but the declared bar convention assigned a bar on a stress only the mixture-frame meaning. | Confirmed: the convention listed four bar meanings; the distention stress is a fifth use. | **FIXED** by extending the stated convention (the reviewer's first option): the notation paragraph now records that a bar written on the distention stress of eq. `fabric-distention-stress` denotes that stress in the intermediate frame, normalised per reference mixture volume. | Rebuilt; the local sentence in `sections/pore_fabric.tex` is now consistent with the convention. |
| R3-C3 | The abstract presents the fabric-driven anisotropic Biot tensor without the fixed-orientation restriction the fabric model imposes. | Confirmed against `sections/pore_fabric.tex` §7.1: "which amounts to fixing `R_A = I` … This is a modeling choice"; "carries no rotational fabric variable". | **FIXED.** The abstract now states that the pore-fabric orientation is prescribed material data and that no relative rotation of the fabric and the mineral matrix is represented. | Rebuilt; abstract and body now agree on the scope of the fabric result. |
| R3-C4 | The abstract and the concluding sentence said "independent re-implementation", dropping the limitation the body states twice. | Confirmed against `sections/finite_elements.tex` lines 280–288: "an implementation check, not an independent derivation"; "shares the section's basis and reported-scalar sign conventions". | **FIXED.** Both the abstract and `main.tex` (discussion) now say "separate re-implementation … that shares their modelling conventions". | Rebuilt; abstract, discussion and body now state the same scope. |

### Optional notes

| ID | Note | Disposition |
| --- | --- | --- |
| R1-N1 | Name all four annihilated modes. | **APPLIED** — folded into the R1-C1 rewrite (the two axial-shear modes are now named). |
| R1-N2 | State that the transient fabric runs use the reference-state material. | **RETAINED.** The paragraph already discloses that the material "evaluates the reference-state drained stiffness, the Biot tensor, and the distention strains", and `sections/finite_elements.tex` already states no mesh-convergence claim is made. No correction required; avoids re-opening settled prose. |
| R1-N3 | Cite the `fabric_probe_conformal` cross-check number in sec:fe-fabric. | **RETAINED.** The number is already reported with its material-point check; adding a second citation of the same quantity is redundancy, not correction. |
| R2-N1 | Figure caption understates how many temporal orders exceed unity. | **APPLIED.** Demonstrated inaccuracy (8 of 9 exceed unity). The caption and the plot manifest caption now read "the values include entries above unity", matching `main.tex`. No number changed. |
| R2-N2 | Rename `tensor_checks.fabric_angle_deg`. | **RETAINED.** A machine-readable field name not quoted in the manuscript; renaming it would change the recorded JSON for no scientific gain. Recorded here for a future pass. |
| R2-N3 | Point `fe-evidence/README.md` from `input.i` to `command_overrides`. | **RETAINED.** The override record is already documented and correct in `provenance.json` and `tools/rerun_fabric_decks.py`. |
| R2-N4 | Unify `source_sha256` path conventions. | **RETAINED.** Both conventions resolve and match; no defect. |
| R2-N5 | `site/evidence.json` names the scientific snapshot without a resolvable reference. | **RETAINED.** A label, not a broken path; the sibling artifact entries carry resolving path+digest. |
| R3-C5…R3-C14 | Prime overload signposting; `C` letter collision; bar-accent collisions; compressed isotropic-modulus definition; unnamed suites; uninterpreted 45° outlier; circular `h = e^{ln h}` phrasing; compressed Biot step; figure font/float/underfull cosmetics; novelty-search scope. | **RETAINED.** None is a correctness defect; each is a readability or presentation preference. Applying all of them would churn settled prose across three sections in a round convened to resolve six specific defects. Recorded here so they are not lost. |

## Verification performed in this revision round

```
python3 examples/plot_fe_verification.py
latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
python3 tools/package_numerical_supplement.py
python3 tools/populate_site_manifest.py
python3 tools/register_fabric_evidence.py
python3 tools/build_verification_site.py
python3 .agent/shared/tools/research_project.py check      # errors: []
python3 .agent/shared/tools/research_project.py links site # {"errors": []}
python3 tools/agentctl check                               # passed
python3 tools/manuscript_release.py audit                  # rc=0
```

Outcomes: PDF rebuilt, 34 pages, 0 overfull boxes, 0 undefined references or citations;
supplement archive rebuilt, 69 files (byte-identical, `fa8c07a2…`, because
`examples/plot_fe_verification.py` is not archived); site manifests rebuilt in the documented order
(41 artifacts / 13 figures / 5 cases; 47 snapshot files; link check passed).

The held numerical suites (`validation/`, `examples/verify_*.py`) were not run, as scoped.

Because scientific content changed, no round-29 verdict carries forward; a new snapshot and a
fresh independent round are required.
