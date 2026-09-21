# Round 32 — author response

Snapshot `2231ed2b9825fef48f1015be1b9b2a230c09bec424ad18a9ca8f32c5d0e8fa44`
(608 files), HEAD `8d83726`, 33-page build at the round-32 snapshot.
Reviews: `reviews/round-32/reviewer-{1,2,3}.md`. **SIMULATED AI PEER REVIEW.**

## Verdict tally

| Reviewer | Emphasis | Verdict | Required items |
| --- | --- | --- | --- |
| 1 | derivation and correctness | **ACCEPT** | 0 |
| 2 | numerical verification and source fidelity | **ACCEPT** | 0 |
| 3 | exposition, notation and claims | MINOR REVISION | 2 |

**Two exact ACCEPTs on one immutable snapshot — the gate is met.**

All three reviewers independently confirmed `sha256(snapshot/source-manifest.json)`
equals the declared SNAPSHOT_ID, reported 608/608 entries re-hashed with **0
mismatches, 0 missing**, and identified exactly two present-but-unlisted files
(`SNAPSHOT_ID`, `source-manifest.json` — the two that cannot list themselves).
None read another reviewer's report; each self-reported minor incidental exposure
of *filenames only* — reviewer 1 ran `ls reviews/` in the working tree and saw
directory names, reviewer 2 saw directory names and the filename
`LAUNCH-STATE.md`, reviewer 3 saw the filename `reviewer-2.md` in a listing of its
own output directory. No report content, verdict, or acceptance count was read.
All exposures and non-exposures are recorded in the reports' independence
declarations.

Because scientific and notation content changed in this response (two notation
rules, an added glossary clause, a uniqueness scope qualifier, regenerated
documentation), **no round-32 verdict carries forward**; a fresh snapshot and a
fresh independent round are required, as the cycle prescribes.

## Response matrix — reviewer 3 (the non-accepting reviewer)

| ID | Comment | Evidence checked before editing | Disposition | Verification |
| --- | --- | --- | --- | --- |
| **R3-C1** | The notation paragraph's prime rules covered only stresses, but §5 introduces the reduced energies `W''` (44) and `W'` (45) with the same marks, so a reader applying the glossary literally has no rule for them. | **Confirmed.** `main.tex` stated the rules for `σ'` and `P''` only; `\eqref{eq:reduced-energy}` = (44) and `\eqref{eq:legendre-energy}` = (45) in the rendered build were referenced nowhere in the glossary. This gap was introduced by my own round-31 rewrite of the prime sentence. | **FIXED.** The sentence now states that the same two marks name the reduced energies of the pressure-coupling section at the prescribed pressure: `W''` of `\eqref{eq:reduced-energy}` and its fixed-pressure companion `W'` of `\eqref{eq:legendre-energy}`. | Both labels resolve (`build/main.aux`: `eq:reduced-energy` → (44), `eq:legendre-energy` → (45)); each is now referenced where it is defined as well as in the glossary; the rendered page-3 text was read in the PDF. |
| **R3-C2** | The rule for the bar on `S̄_dis` said the bar "denotes that stress in the intermediate frame", but `pore_fabric.tex` defines **both** `S̄_dis = 2∂W_dis/∂G` and the unbarred `S_dis = ∂W_dis/∂E_dis` in the intermediate frame; they differ by their conjugate strain, not by frame. | **Confirmed.** `sections/pore_fabric.tex:139-146` defines both in the intermediate frame; the unbarred symbol contradicts the stated rule. | **FIXED.** The rule now says the bar marks the member of the work-conjugate pair that is conjugate to the distention tensor `G`, per reference mixture volume in the intermediate frame, with the unbarred `S_dis` its partner conjugate to `E_dis` in that same frame and normalization. | Re-read the definitions in each location; the corrected rule matches `pore_fabric.tex:139-146` verbatim in its attributions (frame and normalization identical for both symbols; the distinction is the conjugate measure). |
| R3-O1 | 72 labels are defined but never referenced. | Confirmed by inspection. | **RETAINED.** LaTeX hygiene only; the reviewer records that it has no effect on the rendered document, and trimming equation labels touches the derivation surface that the round-31 retargets stabilised. | Unchanged; all cross-references still resolve. |
| R3-O2 | Near-duplicate convexity/uniqueness passage in §7.4 and §7.5. | Confirmed. | **APPLIED.** §7.4 now states the argument once and scopes it to the reference quadratic model; §7.5 gives only the positive-definiteness condition `𝔻+φ_{s0}ℂ_s ≻ 0` and refers back, removing the repeated sentence. | Rebuilt; no diagnostic change; the condition and the claim are unchanged in content, only stated once. |
| R3-O3 | Underfull box in the bibliography. | Confirmed; reviewer records no action required. | **NO ACTION** (reviewer's own conclusion). | 1 underfull box remains, benign, in the generated bibliography. |
| R3-O4 | Abstract blends the general fabric law with the implementation's retained subspace. | Confirmed; reviewer records the abstract elsewhere separates law from implementation. | **RETAINED.** The abstract and §7.5 tail already name the retained subspace as the implementation's; the Foster cycles then revised the abstract opening and close for clarity without altering the claim. | Re-read the abstract after the Foster cycles; law and implementation remain separated. |
| R3-O5 | "unimodular" used before its gloss. | Confirmed. | **RETAINED.** The term appears in the abstract, where the glosses of the body do not fit; the first body use defines it (`det H = 1`). Recorded as a deliberate abstract-level choice. | Unchanged. |
| R3-O6 | Forward reference to `𝔻` in §7.4. | Confirmed; the forward `\cref` makes it recoverable. | **RETAINED.** Identical to the disposition accepted for R3-O2 in round 31: moving the sentence would restructure the derivation order the round-31 retarget stabilised. | Cross-reference re-verified as resolving to §7.5. |
| R3-O7 | Subscript `A` on `W_A` is not covered by the glossary. | Confirmed. | **APPLIED.** One clause added: the distention list now names the scalar volume-only distention energy `W_A(a)` of `\cref{sec:work-equivalence}`, of which `W_dis` is the tensorial generalization. | New reference resolves (`sec:work-equivalence` → §3); the wording matches `pore_fabric.tex:135`, which calls `W_A(a)` the volume-only energy. |

## Response matrix — reviewers 1 and 2 (both ACCEPT, zero required items)

| ID | Comment | Disposition | Verification |
| --- | --- | --- | --- |
| R1-O1 | `build/weighted-stress/derivation-scan.txt` is stale relative to the reviewed sources; it reports labels that no longer exist and omits two section files. | **Confirmed and RETAINED.** The reviewer is factually right: `tab:fixed-deformation`/`tab:layer` occur 0 times in `sections/experiments.tex` today. I regenerated both scans as a test and confirmed the current output (343 and 38 lines vs 112 and 18) covers `pore_fabric.tex` and `finite_elements.tex` and no longer reports the absent labels — but **did not install it**: `build/weighted-stress/` is a **read-only** shipped archive (`dr-xr-xr-x`, all files `r--r--r--`) alongside the revision's contact sheets, so the repository's own convention is that packaged evidence is immutable. Rewriting one file inside it would misrepresent a historical triage record. No manuscript claim depends on it. | Regeneration was run and its output compared, then discarded; the shipped file is byte-unchanged (`sha256` unchanged in `fe-evidence/manifest.json`). |
| R1-O2 | Uniqueness wording: the argument is valid for the implemented reference quadratic model, but the mineral term is not quadratic in `G` in general, so a one-clause qualifier would make the scope exact. | **APPLIED** — folded into the R3-O2 edit above: both statements are now scoped explicitly to the reference quadratic model. | Rebuilt; the qualifier is present in §7.4 and the condition restated in §7.5. |
| R1-O3 | The one-line minimization behind the drained-compliance result is not shown. | **RETAINED.** The result is stated and the reviewer notes the code path exists; showing the stationarity step is an exposition choice, and the Foster cycles are constrained to prose-only. Recorded as a deliberate choice. | Unchanged. |
| R1-O4 | It may help to state that `B` also depends on `p`. | **RETAINED.** The text already warns that `σ''` depends on `p`; adding a second caveat is prose, and the Foster cycles are claim-preserving. | Unchanged. |
| R1-O5 | The "independent" fabric check shares conventions with the compiled law. | **RETAINED** as recorded. The manuscript and `examples/verify_fabric.py` already disclose the shared conventions; the reviewer presents a convention-free numerical minimization as a strengthening, not a defect. | Unchanged; disclosure re-read and still present. |
| R2-O1 | "the five deviatoric stiffness modes" is correct but not reproducible from the shipped artifacts alone. | **RETAINED.** The value is confirmed correct by the reviewer from `experiments.json`. Recording the five modes would require regenerating `build/conformal/experiments.json` from a suite I am not authorized to re-run in this scope, and no manuscript number changes. Recorded as a pre-submission clarity item. | Value re-read as consistent; no artifact changed. |
| R2-O2 | The supplement README's reproducibility paragraph and the contour plot manifest's limitations omit the Exodus wall-clock caveat. | **APPLIED.** Both now carry the clause: the recorded Exodus files embed a per-run wall-clock line in their information records, so their raw bytes are not reproducible across runs, while the recorded CSV histories and the field arrays are. | Manifest regenerated and re-verified; the new limitation is present in `figures/fe_fabric_contours-plot-manifest.json`, and the supplement README clause is in the repackaged archive. |
| R2-O3 | No recorded norms for the complementary modes `e₄`/`e₅`. | **RETAINED.** The reviewer confirms no quoted number is unsupported and that transverse isotropy covers those modes; adding recorded norms would require re-running the fabric verification suite. | Unchanged. |

## Foster engineering-review cycles

Three Foster cycles were run on the accepted tree, each with a machine-checked
prose-only proof (claim-surface extraction of every `\label`, `\ref`/`\eqref`/
`\cref` argument, `\cite` key and numeric literal, hashed before and after):

| Cycle | Scope revised | Claim-surface diff | Memo |
| --- | --- | --- | --- |
| 1 | abstract close; Introduction dilation/rotation distinction; §3 distention-energy purpose and `φ_{s0}` origin; 3 passages in `stress_reconstruction.tex`; 2 in `logarithmic_derivative.tex`; 1 in `pore_fabric.tex` | **empty** | `reviews/round-32/foster-cycle-1.md` |
| 2 | `main.tex` §5 pressure coupling; `limits.tex` entry and close; `experiments.tex` (2); `finite_elements.tex` (7) | **empty** | `reviews/round-32/foster-cycle-2.md` |
| 3 | abstract opening; §10 conclusion (2 passages); residual §1–§2 prose; cross-cycle consistency pass | **empty** | `reviews/round-32/foster-cycle-3.md` |

The three cycles together revised 7 files. **Independently verified by me, not
only by the cycle memos**: the claim surface extracted from the working tree
differs from HEAD `8d83726` in **exactly three reference arguments — all of which
I added myself in this response** (`eq:reduced-energy`, `eq:legendre-energy`,
`sec:work-equivalence`). Zero label changes, zero citation changes, zero numeric
changes are attributable to any Foster cycle. The claim surface is unchanged by
the prose work.

## Verification performed in this revision round

```
python3 examples/plot_fabric_contours.py --runs fe-evidence/runs --output figures
python3 tools/check_figure_manifests.py         # 3 manifests, all inputs+outputs verify
python3 tools/register_fabric_evidence.py
python3 tools/package_numerical_supplement.py
python3 tools/populate_site_manifest.py
python3 tools/register_fabric_evidence.py       # re-run after populate (order matters)
python3 tools/build_verification_site.py
latexmk -g -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
python3 .agent/shared/tools/research_project.py check        # errors []
python3 .agent/shared/tools/research_project.py links site   # {"errors": []}
python3 tools/agentctl check                                 # passed
python3 tools/manuscript_release.py audit                    # 13 paths
```

Outcomes: 33-page build, 0 overfull boxes, 0 undefined references or citations,
0 missing-character warnings, 1 benign underfull bibliography box; supplement
repackaged; site manifests rebuilt with a passed link check; all three figure
plot manifests verify; claim-surface diff empty across all three Foster cycles.

The held numerical suites (`validation/`, `examples/verify_*.py`) were **not**
run, as scoped. Executing the pore-fabric decks and the contour plot script is
not one of them: the former regenerates the recorded evidence the plots consume,
the latter only re-reads it.
