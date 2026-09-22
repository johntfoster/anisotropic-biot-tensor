# Round 36 — CLOSE-OUT: the gate was not met, and the cycle ends here

## Verdict ledger (exact ACCEPT only; MINOR REVISION never counts)

| Round | Snapshot | Reviewer 1 | Reviewer 2 | Reviewer 3 | Exact ACCEPTs | Gate (>=2) |
| --- | --- | --- | --- | --- | --- | --- |
| 32 | `2231ed2b…` | ACCEPT | ACCEPT | MINOR REVISION | 2 | **MET** |
| 33 | `7e75f419…` | ACCEPT | ACCEPT | MINOR REVISION | 2 | **MET** |
| 34 | `a2d99a39…` | *no report* | ACCEPT | MINOR REVISION | 1 | not met (incomplete) |
| 35 | `3e56fad6…` | MINOR REVISION | MINOR REVISION | MINOR REVISION | 0 | not met |
| 36 | `c1f6210d…` | ACCEPT (recovered seat) | MINOR REVISION | MINOR REVISION | 1 | **not met** |

**The current tree did not reach two accepts.** Round 36 returned one exact ACCEPT and two
MINOR REVISION verdicts on its one immutable snapshot. Per the owner's bound this is the last
round; no round 37 was opened.

## Reviewer run IDs and report paths

| Seat | Run ID | Session key | Report |
| --- | --- | --- | --- |
| Reviewer 1 (first run — **no report written**) | `c33599cf-86dd-416c-8d3d-6b31b77bbeac` | `agent:react:subagent:494d34ce-c2c8-4d3a-9669-b85566672c72` | *(none)* |
| Reviewer 1 (recovery run — wrote the report) | `b1a35f77-b1f4-4baf-bd98-7a0c97b3b42a` | `agent:react:subagent:cec6a95e-2f67-484f-96e7-f6489d3d2ce6` | `reviews/round-36/reviewer-1.md` |
| Reviewer 2 | `f38fd32f-320b-4b82-b111-41b97c45c878` | `agent:react:subagent:8b9c30a0-cd30-4d66-9e85-83cc76fabf82` | `reviews/round-36/reviewer-2.md` |
| Reviewer 3 | `3629ad49-a04a-40c0-831e-95f2ef129e09` | `agent:react:subagent:b1a50c6f-6c85-4686-ab9f-3c5e87f77829` | `reviews/round-36/reviewer-3.md` |

Reviewer 1's first run settled with status ok after reporting "All derivations and recorded
numbers check out. Writing the report now." but wrote no file. Its seat was recovered in a
second isolated run; under the skill's rule a recovered review is not counted as acceptance,
so even its ACCEPT could not lift the gate — and, independently, one ACCEPT is below the
two-of-three bar.

## Snapshot integrity

`.agent-runtime/review-snapshots/round-36`, `SNAPSHOT_ID`
`c1f6210d5e2649986693d3dc0c26dccc072434c166148bbdc89e3f874ce4644d`, 608 files. All three
reviewers independently confirmed `sha256(source-manifest.json)` equals the declared
SNAPSHOT_ID and re-hashed every listed file: 608/608, 0 mismatches, 0 listed-but-missing, 0
present-but-unlisted (excluding the two self-referential metadata files).

## The four round-35 required items — disposition and verification

| Item | Location | Disposition |
| --- | --- | --- |
| R1-C1 / R3-C1 (tilde rule names the wrong input frame) | `main.tex:257-260` | **Fixed.** The rule now reads "the representation of a mixture-frame quantity in the true (mineral) frame, obtained by the inverse rotation `R_A^T`", matching eq. (74) and eq. (6) and inverting the bar rule. |
| R3-C2 (`xi` used once, never introduced) | `main.tex:221-223` | **Fixed.** Replaced by the explicit per-phase forms `rho_bar_s = rho_s/phi_s` (the mineral state) and `rho_bar_f = rho_f/phi_f`. |
| R1-C2 (`FabricMaterial.produces` lists `distention_stress`) | `validation/equation_to_moose_map.yml:15` | **Fixed by dropping the entry**, because the compiled material declares no such property (`moose_app/src/materials/FabricMaterial.C:50-69`) and `FabricLaw.h` computes no `S_bar_dis`. The material was not changed. |
| R2-C1 (manifest note over-states what is unshipped) | `fe-evidence/manifest.json` `notes[0]`, generator `tools/materialize_fe_evidence.py` | **Fixed at the pipeline root** and the shipped record re-synchronised from the generator's literal; only `notes[0]` changed — `cases`, `files`, `not_applicable` and `runs` are byte-identical, and no digest moved. |

## Round-36 required items, with both sides

### R2-C1 — `site/evidence.json:25` cites an evidence id that resolves to no artifact; the shipped record fails its own validator
**Location:** `site/evidence.json:25` (`categories.implementation.evidence`), built by
`tools/build_verification_site.py:108-110`.
**Reviewer's side:** the implementation category lists id `fluid-coupling-verification`, but no
artifact carries that id and no artifact path contains "fluid"; the shipped
`site/reports/fluid-coupling-verification.json` is therefore unregistered; and
`python3 tools/build_verification_site.py --validate-only` fails with
`Site build failed: Unknown evidence artifact: implementation` (exit 1). I reproduced this
independently: the validator exits 1, the 40 declared artifact ids contain none matching
"fluid", and removing that one id in a `/tmp` copy makes the manifest valid.
**Counter-consideration:** no manuscript number and no declared digest is affected; the
fluid-coupling report itself is present, is listed in the snapshot manifest, and its contents
(110 checks, 8.09e-09) match the site text. The defect is a registration/bookkeeping error in
a shipped site manifest, pre-existing (this pass did not touch `site/evidence.json`) and
documentary rather than scientific.

### R3-C1 — hat and tilde are both defined as "the true frame", with no criterion to choose between them
**Location:** `main.tex:224` (hat rule) versus `main.tex:258-261` (tilde rule), with the
instances `main.tex:281-286`, `main.tex:312-320` and eq. (74) in `sections/pore_fabric.tex`.
**Reviewer's side:** after this pass's own fix, both decorations map into the true frame;
eq. (74) places a hat and a tilde side by side in one expression, and
`~overline{tau_s} = hat{tau_s}` through eq. (6); the only thing separating the symbols is a
normalization the paragraph never states for this pair, so a reader cannot tell which
decoration a given true-frame object should carry.
**Counter-consideration:** the marks are decidable in context — a hat carries the intrinsic
mineral normalization, a tilde the mixture normalization rotated into the mineral frame — and
this item is the direct consequence of the round-35-mandated tilde fix, i.e. the same churn
structure the round-35 close-out identified: one round's repair became the next round's
required item.

### R3-C2 — "fixed-pressure" names both a double-primed stress and a single-primed energy
**Location:** `main.tex:237-243`, against `main.tex:461-476`.
**Reviewer's side:** the rule attaches "fixed-pressure" to the stress `P''` and simultaneously
to the energy `W'`, while the energy `W''` is called "reduced"; one word names two members
carrying opposite marks, so the verbal rule contradicts its own instances.
**Counter-consideration:** the marks themselves pair correctly — `(W'', P'', sigma'')` and
`(W', P', sigma')` — so nothing computational is affected; the defect is a verbal epithet. The
same substance was filed as an **optional** note in round 35 (R1-O2, "fixed-pressure qualifier
split across W' and P''") and has now been escalated to a required item.

## What is banked

- Three independent confirmations of the snapshot digest and a full 608/608 manifest re-hash.
- Reviewer 1 re-derived the whole development — the decomposition and conformal
  specialization, the phase balance and conjugacy, the reduced energies and the
  finite-deformation Biot tensor (verified numerically against implicit differentiation of the
  EOS to ~1e-11), the drained stiffness and compliance restriction including the
  Moore-Penrose limit, the reference/isotropic/unjacketed limits, the pore-fabric kinematics
  and work-conjugate pair, and the logarithmic-derivative conversions — and found **no
  incorrect derivation, no inconsistent normalization and no index or frame error** (no
  required items).
- Reviewer 2 verified every declared digest surface byte-for-byte (source manifest, FE
  evidence manifest 317/317, 57 provenance records, 40 site artifacts, 47 scientific-snapshot
  entries, the supplement archive's 68-entry internal manifest, three figure plot manifests)
  and located every quoted number in a frozen artifact, independently recomputing the key
  constitutive scalars.
- Reviewer 3 reproduced all 106 equation numbers, found 0 unresolved cross-references, 0
  overfull boxes and 0 missing glyphs, and confirmed claim strength matches the evidence.

## Final build status

- Working-tree HEAD `f163561` ("Fix the four round-35 required items in one bounded pass, then
  freeze round 36"); working tree clean apart from the untracked workspace file and this
  round's review artifacts.
- `build/main.pdf` — **34 pages**, sha256
  `980162471b9f0a118654eb7cda9ddbfe463887c294cac91160c460972f50c719`; 0 overfull boxes, 0
  undefined references or citations, 0 missing-character warnings, 1 benign underfull
  bibliography box.
- `tools/check_figure_manifests.py` verifies 3 manifests; `research_project.py check` errors
  `[]`; `agentctl check` passes. The held numerical suites were not run, as scoped.

## Recommendation

None is offered: the bound closes the cycle and forbids round 37. If a future pass is ever
authorized, the three outstanding items are all local and claim-neutral — register the
fluid-coupling artifact (or correct the id) and re-run `--validate-only`; state the hat-versus-
tilde criterion in the notation paragraph; make the "fixed-pressure" epithet follow the mark.
