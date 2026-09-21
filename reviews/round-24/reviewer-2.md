# Round 24 — Reviewer 2 (physics / source fidelity / packaging)

Independent review of the anisotropic pore-fabric extension. I reviewed only the
frozen snapshot; I did not read reviewer-1, reviewer-3, or any prior-round
report. All scripts were run from copies under `mktemp -d`. Files on disk are
the evidence below.

## Snapshot and integrity

- Frozen snapshot: `<repo>/.agent-runtime/review-snapshots/round-24`
- Declared `SNAPSHOT_ID`: `1dea9e121e8d763dc0b4008d9b430026a17d600fbdd67d5f085a7d6f2617b423`
- `sha256(source-manifest.json)` = `1dea9e121e8d763dc0b4008d9b430026a17d600fbdd67d5f085a7d6f2617b423` → **matches the declared ID**.
- Manifest lists **591** files; re-hashed every one against the manifest:
  **591 OK, 0 missing, 0 mismatch**. (The tree holds 593 regular files; the two
  extras are `source-manifest.json` and `SNAPSHOT_ID`, which is expected.)

Integrity of the frozen artifact is clean.

## What I verified independently

### 1. Fabric law physics vs `sections/pore_fabric.tex` and `sec:fe-fabric`

I read `moose_app/include/utils/FabricLaw.h`, `ConformalLaw.h`,
`moose_app/src/materials/FabricMaterial.C`, `sections/pore_fabric.tex`,
`sections/finite_elements.tex` (sec:fe-fabric), and `sections/limits.tex`, and
checked the code against the stated equations line by line.

- **Kinematics / basis.** `e1 = I/√3`; `e2 = √(3/2)(m⊗m − I/3)` after unit
  normalisation in the Mandel metric — matches `sec:fabric-biot`. The retained
  directions are checked orthonormal at construction (throws otherwise).
- **Reported scalars.** Code sets `ln_a = √3·x1` and `ln_h = −x2/√1.5`. Using
  `E_dis = (ln a/3)I + ln h(½I − 3/2 m⊗m)` and `½I − 3/2 m⊗m = −√(3/2)e2`, this
  is exactly the paper's `ln a`, `ln h` (eq. `fabric-transverse-strain`), so the
  reported shape scalar is the unimodular eigenvalue ratio, not a projection —
  as claimed.
- **Restricted compliance.** Code builds `(C^d)^{-1} = (φ C_s)^{-1} + D4^+`,
  with `D4^+ = Σ dinv_ij e_i⊗e_j` (Moore–Penrose inverse on the retained
  2-D subspace, zero on the complement) — matches eq. `fabric-compliance-restriction`
  and the "two retained directions, four frozen modes" statement.
- **Biot tensor.** `bvec = eI − C^d : C_s^{-1} : I`, then
  `B_par = m·B·m`, `B_per = ½(tr B − B_par)`. This is the reference-state
  `B_0 = I − C^d:C_s^{-1}:I` of eq. `reference-biot-compatibility` with the
  generalised `C^d` — consistent with `sec:fabric-biot`.
- **Storage.** Code uses
  `storage = (1−φ)/K_f + (φ/K_s)(1 − K_d/(φ K_s))`, `K_d` read from the drained
  `C^d`. This is exactly eq. `reference-solid-storage` of `limits.tex`
  (`S_s = (φ_s0/K_s)(1 − K/(φ_s0 K_s))`) with `K→K_d`, and matches the published
  `ConformalMaterial` convention. The header comment states this correctly.
- **Physical narrative vs implementation.** `FabricLaw::evaluate` throws unless
  `linear_reference=true`; the material returns a *reference-state* first Piola
  stress, a *constant* Biot tensor, a linearised storage law, and a *constant*
  Darcy flux `−ρ0·mobility·∇p` (reference limit of eq. `fe-reference-darcy-law`,
  with `mobility = k/μ_f = 1.5`). This is a linearised reference-tangent
  implementation, and the manuscript says so repeatedly: abstract ("implemented
  in its reference-state linearization"), sec:fe-fabric ("evaluates the
  reference-state drained stiffness, the Biot tensor, and the distention
  strains"), and the figure captions ("finite-load demonstrations"). I found
  **no place where the physical claim is stronger than the implementation**. The
  finite-deformation law is *not* claimed to be verified; the MMS caveat ("does
  not by itself verify the nonlinear constitutive law") is explicit.

### 2. Recorded FE runs

- `fe-evidence/manifest.json`: **317/317 file digests match**, 0 missing,
  0 mismatch; 0 duplicate paths; 0 duplicate notes; all 57 run entries carry a
  `binary_sha256` equal to the `application_sha256` in the corresponding
  `provenance.json`.
- Naming note: there is **no `fe-evidence-index.json`** in the snapshot.
  `fe-evidence/manifest.json` (keys `cases`, `files`, `runs`, `not_applicable`,
  `notes`) is the index and is what I verified. See Optional note O2.
- The four refined contour decks `fe-evidence/runs/fabric_contour_{iso,a0,a45,a90}/`
  each retain `input.i`, `provenance.json`, `run.log`, `analysis.json`,
  `solution.csv`, and the **Exodus snapshot `solution.e`** (≈0.99 MB each).
  Provenance records mesh (`nx=40 ny=8`, QUAD9 on 0.1-strip), step
  (`dt=0.0003`, `end_time=0.003`), the exact overrides, git revision, and
  application/library digests.
- **Contour numbers reproduce from the Exodus files.** Reading `solution.e`
  directly (netCDF4) and taking the last step, I obtained exactly the values in
  `figures/fe_fabric_contours.csv`:

  | case | p_max (mine) | p_max (CSV) | u_mag_max (mine) | u_mag_max (CSV) |
  |---|---|---|---|---|
  | iso | 3.606194e-05 | 3.606194309585106e-05 | 5.182640e-05 | 5.1826395396202306e-05 |
  | a0  | 4.349137e-05 | 4.3491366180031454e-05 | 5.137155e-05 | 5.13715515334801e-05 |
  | a45 | 4.973659e-05 | 4.973659107895197e-05 | 2.381836e-05 | 2.381836351578327e-05 |
  | a90 | 5.503135e-05 | 5.503135423750668e-05 | 5.258692e-05 | 5.258692042529596e-05 |

  The pressure maximum lies on `X1 = 0` in every case, as the text states.
- **Manuscript numbers match the recorded data.** Coupled-transient peaks
  (`fe_fabric_mandel_peak.csv`): 4.36276e-5 (0°), 4.99008e-5 (45°), 5.52111e-5
  (90°), 3.61639e-5 (uncoupled) → the quoted 4.36, 4.99, 5.52, 3.62 (×10⁻⁵).
  Refined contour peaks 3.61 / 4.35 / 4.97 / 5.50 (×10⁻⁵) and displacement
  magnitudes 5.18 / 5.14 / 2.38 / 5.26 (×10⁻⁵) match the CSVs. The eleven-step
  Exodus output and the six diffusion snapshot times in `fe_fabric_diffusion.csv`
  match the text.
- **Fabric verification reproduces.** Running `examples/verify_fabric.py --runs
  fe-evidence/runs` reproduces the recorded `build/fabric/fabric-verification.json`
  exactly, including `worst probe-field absolute difference = 4.885e-15`,
  `H_reconstruction_max_abs_diff = 2.220e-16`, `H_det_minus_one = −3.331e-16`,
  `D4_e3_norm = 1.582e-16`, `D4_e6_norm = 0`, `rotation_invariance_norm =
  2.497e-16`, and the conformal cross-check `sigma11` diff 1.874e-14. Every one
  of the numbers quoted in `sec:fe-fabric` (2.2e-16, −3.3e-16, 1.6e-16, 2.5e-16,
  4.9e-15, 1.9e-14) is exactly these recorded values. I confirm the script's own
  caveat is correct: it shares the section's basis and sign conventions, so it is
  an implementation check, not an independent derivation — as the manuscript
  already states.

### 3. `site/evidence.json` and `site/scientific-snapshot.json`

- `evidence.json`: **41/41 artifact digests match** the files on disk; 13
  `figures[]` entries all reference existing artifact ids; every
  `categories[*].evidence` and `cases[*].artifacts` id resolves; **no duplicate
  artifact ids**; **6 limitations, no duplicates**; 5 notes, no duplicates.
- `scientific-snapshot.json`: **46/46 listed digests match**; the
  `scientific-snapshot` artifact's own sha256 in `evidence.json`
  (`47d175a3…`) equals the on-disk file hash.
- No machine-specific absolute paths (`/home/…`, `.agent-runtime`) appear in
  either `site/evidence.json` or `site/scientific-snapshot.json` (`grep` count 0).
- **Reported counts check out.** `mandel-reference.json` contains **38** checks,
  all passed, with central overshoot ratio 1.054659 at t = 0.015165352 (matches
  "38 self-checks (peak overshoot 5.4659% at t = 0.01516535)");
  `fluid-coupling-verification.json` has `count = 110`,
  `maximum_scaled_error = 8.0867e-09` (matches "110 checks, max scaled error
  8.09e-09"); `cpp-python-constitutive.json` has `states = 41`,
  `value_absolute_error = 6.395e-14` (matches "6.4e-14 over 41 finite states").

### 4. Supplement archive `build/anisotropic-biot-2026-09-20-v2.zip`

- Recorded sha256 in `source-manifest.json` =
  `46ef65aad77df01de64054108c5a0b0ec4a91718a73123f620f1793f6cba2c54`;
  recomputed on disk → **match**.
- Readable; 69 entries. Its internal `manifest.json` lists 68 files with
  sha256: **68/68 verified against the zip contents**, 0 mismatch, 0 absent.
  The single entry not self-listed is `manifest.json` itself, which is expected.
- **Byte-identity spot checks vs on-disk sources** (all IDENTICAL):
  `moose_app/include/utils/FabricLaw.h` (c83ae3e8…),
  `examples/verify_fabric.py` (e1abd2fe…),
  `moose_app/src/materials/FabricMaterial.C` (9abcfab6…),
  `moose_app/inputs/fabric_contour.i` (284f042c…).
  `main.tex` is **not** in the zip, but neither the zip README, the main.tex
  `\embedfile` description, nor the repo README claims it is; the archive ships
  the *numerical* supplement, and the manuscript PDF is the wrapper. No defect.
- The zip carries its **own** README (not the repo README) with correct
  instructions, and the claim "The article PDF embeds this ZIP" is true:
  `pdfdetach -list build/main.pdf` reports one embedded file,
  `anisotropic-biot-2026-09-20-v2.zip`, and the extracted attachment is
  byte-identical to the on-disk zip (both `46ef65aa…`).
- **End-to-end reproduction from the extracted archive.** I extracted the zip to
  a temp dir and ran the commands its README advertises from the extracted root:
  `python3 examples/verify_fabric.py` (no arguments) → `worst probe-field
  absolute difference = 4.885e-15`; and
  `python3 examples/plot_fabric_contours.py --runs fe-evidence/runs --output figures`
  → regenerated `fe_fabric_contours.{csv,pdf,png}` and
  `fe_fabric_diffusion.{csv,pdf,png}`. Run against the snapshot's own
  `fe-evidence/` + `figures/`, the regenerated
  `fe_fabric_contours.png` (a2ddeb8d…), `fe_fabric_contours.pdf` (d2dcc0c5…),
  `fe_fabric_contours.csv` (8a618ffc…), `fe_fabric_diffusion.png` (391c5a6b…)
  and `fe_fabric_diffusion.csv` (41a66a5d…) are **byte-identical** to the shipped
  files. This is a strong reproducibility result.

### 5. Citations

I resolved **all 35 DOIs** in `references.bib` against Crossref, and checked the
one non-DOI entry by hand.

- Every DOI resolves to the cited work, with the right first author, journal,
  volume, and page/article number. No fabricated, misattributed, or misdated
  entry found. Examples confirmed: Biot 1955 (JAP 26(2):182–185); Biot & Willis
  1957 (JAM 24(4):594–601); Cowin 1985 (Mech. Mater. 4(2):137–147); Turner &
  Cowin 1987 (J. Mater. Sci. 22(9):3178–3184); Walker et al. 2023 (GJI
  235(3):2442–2475); Foster & Xu 2025 (JMPS 204:106263 — the DOI/article number
  matches the journal record, and an independent online CV for the author lists
  the same article).
- `\cite` keys used in the manuscript all exist in the bib; `walker2023poroelasticity`
  is cited with an optional page argument (`\cite[appendix D]{…}`).
- Two real-but-trivial items are noted under Optional (O3).

### 6. Packaging/reproducibility numbers I quote

All numbers above are recomputed in this review: 591/591 snapshot files,
317/317 FE-manifest digests, 68/68 zip-internal digests, 41/41 artifact digests,
46/46 scientific-snapshot digests, 38 Mandel checks, 110 fluid checks,
41 cpp-python states, four contour Exodus decks, and the byte-identical
regenerated figures.

## REQUIRED items

**None.** I found no defect that genuinely blocks acceptance of the physics,
sources, or packaging as they stand. The implementation is honestly scoped as a
reference-state linearisation; every quoted number reproduces from the shipped
artifacts; the sources resolve; the frozen snapshot is integrity-clean and the
supplement reproduces end-to-end.

## Optional notes

- **O1 — Absolute machine paths in `fe-evidence/runs/*/provenance.json`.**
  38 of the 57 provenance records embed absolute, machine-specific paths such as
  `/home/jfoster/projects/…/.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs/…`
  in their `command` array. The two site JSONs named in the review brief are
  clean, and these files are not shipped inside the supplement zip, so this does
  not block anything. It is an inconsistency: the four refined `fabric_contour_*`
  provenance records (and the other fabric runs) use the sanitised
  `Outputs/file_base=...` form, while the earlier `materialize_fe_evidence`
  records keep raw absolute paths. Consider normalising the older records to the
  same repo-relative/redacted form if the evidence tree is ever shipped as-is.
- **O2 — No `fe-evidence-index.json`.** The brief refers to a file of that name;
  none exists. `fe-evidence/manifest.json` is the index and is internally
  consistent (see above). If an index file is expected by convention, its name
  should be reconciled.
- **O3 — Two minor bibliography items.** (a) `thompsonwillis1991` gives the title
  "A **Reformulation** of the Equations of Anisotropic Poroelasticity"; the
  published title (Crossref and ASME) is "A **Reformation** of the Equations of
  Anisotropic Poroelasticity". (b) `dehghanipentamerodio2019` and
  `dehghanizilian2021` appear in `references.bib` but are never cited in
  `main.tex` or `sections/*.tex`. Neither affects any claim.
- **O4 — Scope of `site/scientific-snapshot.json`.** It digests 46 files (all
  under `examples/`, `moose_app/`, `tools/`) and is labelled "exact FE source and
  evidence snapshot", but it does not cover the `fe-evidence/runs/**` run
  artifacts or the `figures/`, `site/reports/` outputs that `evidence.json`
  ships. `evidence.json`'s provenance note ("the scientific-snapshot artifact
  lists the exact files with SHA-256 hashes") is therefore slightly broader than
  the snapshot's actual coverage. The individual digests all check out via
  `evidence.json`; this is a wording/coverage clarity point only.

VERDICT: ACCEPT
