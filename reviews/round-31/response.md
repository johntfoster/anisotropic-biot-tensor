# Round 31 — author response

Snapshot `09a606a73d9f475ec624785b7b2a8483f989f2270eca7aeb405015205d113c84`
(606 files), HEAD `40a49ae`, 34-page build at the round-31 snapshot.
Reviews: `reviews/round-31/reviewer-{1,2,3}.md`. **SIMULATED AI PEER REVIEW.**

## Verdict tally on the round-31 snapshot

| Reviewer | Emphasis | Verdict |
| --- | --- | --- |
| 1 | derivation and correctness | **ACCEPT** |
| 2 | numerical verification and source fidelity | MINOR REVISION |
| 3 | exposition, notation and claims | MINOR REVISION |

**1 exact ACCEPT — the gate (two of three, one immutable snapshot) is not met.**
All three reviewers confirmed `sha256(snapshot/source-manifest.json)` equals the declared
SNAPSHOT_ID, re-hashed the listed files with zero mismatches and zero missing listed files,
declared no exposure to any other report, and used the held suites only as recorded
evidence. No independence incident was recorded. Because scientific content changes in this
response, no round-31 verdict carries forward; round 32 must be a fresh round on a fresh
snapshot.

## Loop guard — the round-31 required items are round-30 artifacts

Reviewer 2's required item (R2-C1) and reviewer 3's two required items (R3-C1, R3-C2) were
**caused by round 30's own fixes**: the round-30 revision re-ran the contour decks (which
rewrote the Exodus metadata) without regenerating the downstream plot manifest, and wrote
two notation cross-references against the wrong labels. That is exactly the pattern the
round is instructed to break rather than re-enter. The disposition below therefore fixes
the **generating process**, not just the two artifacts:

- the contour harness now regenerates the figure data and the plot manifest *after* the
  decks, and then re-verifies every declared digest, so the stale-digest class cannot
  recur (see R2-C1);
- every `\eqref` touched in the notation paragraph was resolved against its label and
  against the rendered equation number (see the R3-C1/R3-C2 verification column).

Neither required item is a bare recurrence of a round-29 item, so the guard is not
triggered for stopping; it is satisfied by breaking the cause.

## Response matrix — reviewer 2 (numerical verification and source fidelity)

| ID | Comment | Evidence checked before editing | Disposition | Verification |
| --- | --- | --- | --- | --- |
| **R2-C1** | `figures/fe_fabric_contours-plot-manifest.json` records a stale `input_sha256` for the four contour Exodus files. | **Confirmed** on the tree: declared `7b79a565…`, `8fba1339…`, `9dd70793…`, `f8f5f361…`; shipped bytes hash `0f281f7a…`, `ca9ad477…`, `36c8fb10…`, `604d9fcc…`, which is what `source-manifest.json` and the supplement manifest declare. Root cause reproduced: `git show 6385889:<build>` vs `40a49ae:<build>` differ in **2 bytes only**, the Exodus `title` attribute holding the run's temporary directory (`/tmp/tmp38vtwout/solution.e` → `/tmp/tmpzwc21mkj/solution.e`); every field array is bit-identical. Round 30 re-ran the decks and never regenerated the manifest that hashes them. | **FIXED at the process root**, not by re-stamping. (1) `tools/rerun_fabric_contours.py` now runs each deck **inside the temporary directory with a relative `Outputs/file_base=solution`**, so the recorded `title` is the stable string `solution.e` instead of a fresh random host path. (2) The harness now rebuilds the figure data and the plot manifest **after** the decks and then re-verifies them as its final step (`--no-figures` opts out). (3) `tools/check_figure_manifests.py` is new: it recomputes every declared `input_sha256`/`output_sha256` in every `figures/*-plot-manifest.json` from the file on disk and exits non-zero on a missing file or a mismatch. (4) `make figures` runs the ordered pair. | Manifest regenerated from the produced Exodus bytes and **all five inputs / six outputs now verify** (`OK figures/fe_fabric_contours-plot-manifest.json: 5 inputs, 6 outputs verified`). The checker was shown to *catch* the round-31 defect before the fix (4 stale entries reported, rc=1) and to pass after it (rc=0). The two independent regenerations of this round produced the same field arrays; the plot manifest and `fe-evidence/manifest.json` were regenerated with them and re-verified. |
| R2-O1 | The four shipped contour Exodus files embed a foreign absolute host path in the `title` attribute (`/tmp/tmpzwc21mkj/solution.e`, …). | Confirmed: all four carried a `/tmp/tmp*/solution.e` title. | **APPLIED** — this is the same defect as the R2-C1 root cause, so the relative-output-base fix removes it. | Re-read after regeneration: every contour Exodus now reports `title = 'solution.e'`; no `/tmp`, `/home`, or other host path remains in the four `title` attributes. |
| R2-O2 | `binary_sha256` cannot be byte-verified from the snapshot because the compiled binary is intentionally not shipped. | Confirmed: no `*-opt`/`.so` in the snapshot; `binary_sha256` equals `application_sha256` in all records. | **RETAINED**, with the schema completed — see the round-30 optional closure below, which now records `git_revision` for every run record so a reader can recover the toolchain revision independently. Shipping the binary would publish a host-specific artifact the evidence set deliberately excludes. | `fe-evidence/manifest.json` records the `binary_sha256` per case; `tools/record_run_revisions.py` now resolves and records the revision whose sources match each run's declared digests. |
| R2-O3 | `provenance/manuscript-export.json` declares 13 paths rather than the "four" in the review brief. | Confirmed: 13 declared, all resolve in the snapshot; reviewer 2 explicitly states no action is needed. | **NO ACTION** (reviewer's own conclusion). | Unchanged; all 13 paths still resolve. |

## Response matrix — reviewer 3 (exposition, notation and claims)

| ID | Comment | Evidence checked before editing | Disposition | Verification |
| --- | --- | --- | --- | --- |
| **R3-C1** | Notation paragraph: "a single prime denotes … as in \(\mathbf\sigma'\) of `eq:constitutive-kirchhoff-phase-stress`" points at eq (12), which contains \(\mathbf\tau'\), not \(\mathbf\sigma'\). | **Confirmed** from `build/main.aux`: `eq:constitutive-kirchhoff-phase-stress` → **(12)**; `eq:total-cauchy-single-prime` → **(8)**, whose first line is `\mathbf\sigma'=\mathbf\sigma+p\mathbf I`. Also confirmed the label (8) was defined but referenced nowhere else, i.e. the notation paragraph was its intended use. | **FIXED** by the reviewer's first option: retargeted to `\eqref{eq:total-cauchy-single-prime}`. | **Label resolved against the equation it lands on**: `build/main.aux` gives `\newlabel{eq:total-cauchy-single-prime}{{8}{4}{Deformation and volume-fraction-weighted stress}…}`, and the rendered page-3 text reads "\(\mathbf\sigma'\) of (8)"; the command in the source is the only change. `grep` confirms the label is now referenced (previously dead). |
| **R3-C2** | Notation paragraph: "a double prime denotes the fixed-pressure stress of `eq:cauchy-pressure-tangent`" points at eq (55) (`∂𝛔/∂𝑝 = −𝐁`), which contains neither \(\mathbf\sigma''\) nor the displayed relation. | **Confirmed** from `build/main.aux`: `eq:cauchy-pressure-tangent` → **(55)**; `eq:fixed-pressure-stress` → **(46)** (`\mathbf P''=\partial W''/\partial\mathbf F\|_p`); `eq:finite-biot-tensor` → **(49)** (`\mathbf\sigma=\mathbf\sigma''-p\mathbf B`). | **FIXED**, taking the reviewer's retarget *and* the offered optional: the rule now names \(\mathbf P''\) with `\eqref{eq:fixed-pressure-stress}` and states the relation with `\eqref{eq:finite-biot-tensor}`. | **Each label resolved against the equation it lands on**: aux gives `eq:fixed-pressure-stress → (46)` and `eq:finite-biot-tensor → (49)`; the rendered page-3 text reads "the fixed-pressure stress \(\mathbf P''\) of (46), so that \(\mathbf\sigma = \mathbf\sigma'' - p\mathbf B\) in (49)". No other `\eqref` in the paragraph was edited. |
| R3-O1 | Six §9 figures land 2–4 pages after the text that argues from them, queued behind the end-of-section `\FloatBarrier`. | Confirmed from the rendered PDF; the round-30 `\FloatBarrier` requirement (figures before References, inside §9) still holds. | **APPLIED** with the reviewer's first suggestion: the six `\begin{figure}[t]` in `sections/finite_elements.tex` become `[htbp]`, leaving `\FloatBarrier` in place. | Rebuilt: figure lag falls from 2–4 pages to 1–2 (Figure 6 cited p23/caption p24; Figure 11 cited p25/caption p27), page count 34 → **33**, and diagnostics stay at 0 overfull, 0 undefined references, 0 missing characters. |
| R3-O2 | §7.4 uses `range 𝔻` and the quadratic distention potential one subsection before their §7.5 definition. | Confirmed at `sections/pore_fabric.tex:207-215` vs `:272-283`. Reviewer states the retargeted cross-reference already tells the reader where to look and that this is ordering, not error. | **RETAINED.** The pointer resolves correctly, and moving the sentence or forward-declaring 𝔻 would restructure the derivation order that round-30's accepted R3-C5 retarget stabilised. Recorded as a deliberate choice. | Cross-reference re-verified: `\cref{sec:fabric-biot}` resolves to §7.5, which defines `range 𝔻` and `𝔻⁺`. |
| R3-O3 | Uniqueness is asserted from the strict convexity of the distention potential alone; the mineral term is also curved in `G`, so the stated justification omits it. | **Confirmed**: the bracket is `W_dis + φ_s0 W̄_s(F̄) + φ_s0 p J̄` and strict convexity of `W_dis` alone does not bound the mineral term; the reviewer's own positive-definiteness condition `𝔻 + φ_s0 ℂ_s ≻ 0` on the retained subspace is the correct statement. | **APPLIED** in both locations (`:213-215` and `:281-283`): each now states that the mineral term contributes a positive-definite stiffness in the same strain, and §7.5 records the explicit condition `𝔻+φ_s0ℂ_s` positive definite there. | Rebuilt; `ℂ_s` is introduced earlier (§6, `sections/stress_reconstruction.tex:26`, input before `pore_fabric`), so no forward-reference is added. The drained compliance `(\mathbb{C}^d)^{-1}=(\phi_{s0}\mathbb{C}_s)^{-1}+\mathbb{D}^{+}` is unchanged, and no symbol, label or number elsewhere moved. |
| R3-O4 | Frame vocabulary (mixture/true/intermediate/material frames) is not consolidated in the notation paragraph. | Confirmed; the reviewer states the terms are used consistently and asks for one consolidating sentence. | **RETAINED.** The paragraph already names the mixture and true frames and excepts the intermediate-frame distention stress explicitly; a consolidating sentence would restate §7's material-frame content that the round-29/30 notation restructuring deliberately kept out of §2 (the disposition round 30 recorded and reviewers accepted for R3-C12). | Reviewed the paragraph: every frame used in the body is either named there or its use is explicitly scoped at the point of use. |
| R3-O5 | The §2 glossary forward-references equations (72) and (96). | Confirmed both resolve correctly; reviewer records the choice as deliberate. | **NO ACTION** (reviewer's own conclusion). | Unchanged. |
| R3-O6 | Three literature-specific claims (Drumheller §8.9, Gajo (3.27)/(3.32)/(3.34), Walker et al. appendix D) cannot be checked from the snapshot, whose sources are not shipped. | Confirmed the cited keys exist in `references.bib` and `foster2026poroplastic` is typed `@unpublished`. | **RETAINED as recorded-unverified.** The cited works are not part of the frozen artifact by design; verifying them requires the external PDFs, which the snapshot deliberately excludes. Recorded here as a pre-submission manual check, not as an unresolved defect. | No source change; the claim pointers are unchanged. |

## Round-30 optional carried into this round

| ID | Note | Disposition | Verification |
| --- | --- | --- | --- |
| R2-C3 (round 30) | No run record carried both a revision and source digests; closed only for the 19 fabric-style records, leaving the 38 runtime records without `git_revision`. | **CLOSED.** `tools/record_run_revisions.py` resolves, for each record lacking a revision, the commit whose **tree** contains exactly the recorded `source_sha256` digests, verified through the git object database (not the working tree), and writes `git_revision` together with an explicit `git_revision_basis` field stating that this is the revision whose sources match rather than necessarily the revision the run was made from. | All **38** records resolved to `40a49ae…` with **12/12** source digests matching that commit's tree (456 digest comparisons, 0 mismatches) before writing. After writing, the schema is uniform: **57/57** records carry `git_revision`, `source_sha256` and `binary_sha256`. `--check` re-verifies without writing. The basis field is shipped so the weaker claim is not read as run-time provenance. |

## Additional defect found by the new checker

`tools/check_figure_manifests.py` was written to prove the R2-C1 fix and immediately
surfaced a **second stale-digest defect that neither reviewer reported**:
`figures/fe-verification-plot-manifest.json` declares `output_sha256` for
`fe_reference_comparison.pdf` and `fe_verification_convergence.pdf` that no longer match
the shipped figures at `6385889`/`b6d7272`… Investigating it exposed a **false positive in
the checker itself first**: two *ignored* copies of those figures were sitting in the
repository root and shadowed the real ones, so the checker initially resolved bare figure
basenames against the repository root. The resolver now resolves bare basenames against the
manifest's own directory and path-bearing keys against the repository root. After that
correction the two entries verify and the only genuine mismatches are the four R2-C1
entries. Nothing was changed in `figures/` for this: the defect was in the diagnosis, and
it is recorded here so the diagnostic path is not mistaken for a source change.

## Verification performed in this revision round

```
python3 tools/rerun_fabric_contours.py          # decks -> evidence -> figures -> manifest -> verify
python3 tools/check_figure_manifests.py         # re-hash every declared digest (3 manifests)
python3 tools/record_run_revisions.py --check   # 38 records resolved, no writes
python3 tools/record_run_revisions.py           # schema completed: 57/57
python3 tools/register_fabric_evidence.py
python3 tools/package_numerical_supplement.py
python3 tools/populate_site_manifest.py
python3 tools/register_fabric_evidence.py       # re-run after populate (order matters)
python3 tools/build_verification_site.py
latexmk -g -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
python3 .agent/shared/tools/research_project.py check        # errors: []
python3 .agent/shared/tools/research_project.py links site   # {"errors": []}
python3 tools/agentctl check                                 # agent environment checks passed
python3 tools/manuscript_release.py audit                    # export manifest covers 13 paths
```

Outcomes: PDF rebuilt, **33 pages**, 0 overfull boxes, 0 undefined references or citations,
0 missing-character warnings, 1 benign underfull box in the generated bibliography;
supplement archive rebuilt (69 files, `ab993ee7…`); site manifests rebuilt (23 artifacts /
7 figures / 45 snapshot files; link check passed); all three plot manifests verify.

Two consecutive regenerations of the contour evidence in this round were compared: the
Exodus **field arrays are bit-identical**; the raw file digest still moves with the run wall
clock, which is echoed into the Exodus information records by the framework header
(`Current Time: …`). That residual is documented in `README.md`, and it no longer matters
for manifest integrity because the manifest is regenerated from the produced artifacts and
re-verified as the last step of the same pipeline.

The held numerical suites (`validation/`, `examples/verify_*.py`) were **not** run. Executing
the pore-fabric decks is not one of the held suites; it regenerates the recorded evidence
that the plots consume.

Because scientific content changed (two notation cross-references, a uniqueness
justification, a float-placement change, regenerated contour evidence and completed run
provenance), no round-31 verdict carries forward; a new snapshot and a fresh independent
round are required.
