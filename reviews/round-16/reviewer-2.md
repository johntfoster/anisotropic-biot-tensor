# Round-16 independent review 2 of 3

## (1) Reviewed version, snapshot identity, integrity

- Task charge: physics/source fidelity and packaging completeness.
- Repository (read-only): `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
- Frozen snapshot reviewed: `.agent-runtime/review-snapshots/round-16`
- Declared `SNAPSHOT_ID`: `c621378778d49f8875679440cf874a74aef3caa5d9b04b8936ad319fb57f885f`
- `sha256(source-manifest.json)` = `c621378778d49f8875679440cf874a74aef3caa5d9b04b8936ad319fb57f885f` — **exact match** (verified before and after this review; the frozen snapshot was not modified).
- All work was performed on a writable copy at `/tmp/r16rev2`. No other round directory or prior-round verdict was read; only `reviews/README.md` was read for policy.
- Manifest re-hash of every listed path (sha256, byte-exact against `source-manifest.json`):
  `listed 438 ok 438 mismatch 0 missing 0`.
- All additional manifests resolved: `fe-evidence/manifest.json` `listed 202 ok 202 mismatch 0 missing 0` (38 declared cases, all present, no undeclared run directories); internal supplement `manifest.json` `listed 33 ok 33 mismatch 0 missing 0` (no extra payload files); `site/evidence.json` artifacts `listed 23 ok 23 mismatch 0 missing 0`; `site/scientific-snapshot.json` `listed 33 ok 33 mismatch 0 missing 0`.

## (2) Independent recomputation evidence

All recomputation used `conda activate moose` (note: that environment here is Python 3.14.0 / numpy 2.4.2 / scipy 1.17.1, deliberately newer than the environment recorded in the archived reports).

- **Supplement archive determinism.** Re-ran `python3 tools/package_numerical_supplement.py` from a fresh copy of the shipped originals: produced `build/conformal-2026-09-20-v1.zip` with SHA-256 `b635be7667231fc2077fa7542663ddec1eee126fcd7290c2309222768649f981`, byte-identical to the shipped archive.
- **PDF attachment claim.** `pdfdetach -list build/main.pdf` reports exactly `1: conformal-2026-09-20-v1.zip`; `pdfdetach -saveall` extracts a file whose SHA-256 equals the shipped `build/conformal-2026-09-20-v1.zip` (b635be76…). The `\embedfile` claim in `main.tex` and the README/archive README claims match the PDF as shipped.
- **Constitutive suites.** `examples/verify_tensor.py` reproduced the shipped error dictionary bit-for-bit (phase-energy 9.894327579473838e-10, pressure 1.77870529416424e-09, …, `materials` 13, `total_states` 273). `examples/verify_reconstruction.py` reproduced its shipped error dictionary bit-for-bit (work equivalence 5.040758921381894e-10, unjacketed 5.090372567906343e-14, 20 materials, 20 incompatible pairs rejected, minimum drained eigenvalue 1.8415045063808817).
- **Conformal suite.** `examples/verify_conformal.py` reproduced `checks_passed = 186`, `len(checks) = 186`, `max_constitutive_identity_error = 2.4549890331732928e-09`, `legacy_identities_rechecked = 67`; the regenerated `verification.json` equals the shipped file after excluding the recorded environment block (only `versions`/`source_sha256` differ). The 186 checks decompose as 65 per-state identities (5 states × 13) plus 2 legacy reference relations plus 48 anisotropic-state, 54 isotropic-state, 10 branch, and 7 other identities.
- **Figure data.** `examples/conformal_experiments.py` regenerated `pressure_response.csv`, `shear_response.csv`, `directional_response.csv`, `rotation_response.csv`, `constrained_layer.csv`, `step_refinement.csv` byte-identical to the shipped data; `experiments.json` differed only in the recorded environment versions block.
- **stdlib table data.** `examples/weighted_stress.py` regenerated `results.json`, `states.tex`, `layer.tex`, `pressure.dat` byte-identical to shipped.
- **Physics spot-checks against the shipped sources.** The drained stiffness restriction implemented in `examples/conformal_model.py` (`cd = φCs − φα/(9Ks)(Cs:I)⊗(Cs:I)`) and in `moose_app/include/utils/ConformalLaw.h` reproduces the reference Biot components stated in the manuscript: `B0 = [0.7000, 0.7583, 0.7917]` (from `I − C^d:C_s^{-1}:I`), and the isotropic comparison gives 0.75 (=1−K/Ks); the isotropic comparison shear modulus is 16.8 (= trace of the deviatoric projector contraction /10), matching `sections/experiments.tex`. The Mandel reference constants match `site/reports/mandel-reference.json` (K=1, G=0.75, α=0.6, 1/M=17/80) and `moose_app/scripts/decks.py` (φs0=0.9, Ks=2.5, μs=5/6, Kf=8, mobility 1.5). The recorded finite-load floor (0.0032209197 at nx=20, dt=1e-3) matches the manuscript's "about 3.2×10⁻³", and `site/reports/mandel-reference.json` passes all 38 of its checks.
- **Provenance digests.** Every `source_sha256` in all 38 `fe-evidence/runs/*/provenance.json`, every shipped `input.i` (vs `input_sha256`), every shipped `run.log` (vs `outputs`), the `source_sha256` blocks of `build/conformal/verification.json` and `experiments.json`, and the digests declared for `validation/mandel_reference.py` and `validation/mms_reference.py` all match the shipped sources. The only unshipped digests (binary, `solution.e`, `solution_profile_*.csv`) are the intentionally excluded outputs documented in `fe-evidence/manifest.json` notes.

## (3) Findings

**Observational — supplement records two different numpy versions.**
The archive is internally digest-consistent, but its two JSON reports record different NumPy versions for the same archive: `build/conformal/verification.json` records numpy `1.26.4` while `build/conformal/experiments.json` records numpy `2.2.6` (Python `3.10.12` and SciPy `1.15.3` agree; matplotlib `3.10.8`). The archive README states that JSON files record the actual versions used and that requirements are ranges, so this is self-consistent with the stated policy, but a reader comparing the two files sees an unexplained environment difference within one archived result set. No shipped number or digest is wrong.

**Observational — evidence JSON ships a non-resolving absolute locator.**
`fe-evidence/mms-convergence.json` and its byte-identical `site/reports/mms-convergence.json` record `"runs_dir": "/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs"`. This build-time directory is outside the snapshot (it is a recorded runtime path from `compute_mms_order.py`), so the locator does not resolve inside the artifact. All 12 `required_runs` listed in the same file do resolve under `fe-evidence/runs/`, and the convergence numbers reproduce, so this is a cosmetic provenance locator only.

**Optional — `provenance/manuscript-export.json` lists paths absent from the snapshot.**
The shipped export manifest enumerates 13 repository-relative paths, of which `.latexmkrc`, `.vscode`, `Makefile`, `agent_environment`, and `agent_workflows` do not resolve inside the snapshot; the first three do not exist in the full working tree either. Its own README describes the list as the paths "that belong to the public reproducibility repository", and `tools/manuscript_release.py audit` would flag the five as missing. This concerns a future export/freeze workflow, not the shipped scientific evidence; the manuscript, its evidence, and the supplement do not depend on these paths.

**Observational — no physics or source-fidelity defect found.**
The deck/material physics matches the manuscript: exponential fluid EOS `ρ̄f = ρ̄f0 exp(p/Kf)` with Kf=8 and constant isotropic spatial mobility `k/μf=1.5`; reference mass `m_f = ρ̄f (J − φs0 J̄)`; reference mass flux `Q_f = −J ρ̄f (k/μf) F⁻¹F⁻ᵀ Grad p`; kinematic rigid frictionless platen (EqualValueBoundaryConstraint) with force-controlled top traction; drainage Dirichlet p=0 on the drained boundary; quarter-domain `[0,1]×[0,0.1]` reference geometry (a=1, b=0.1 with reflection symmetry). The anisotropic, isotropic-comparison, and partial-drainage decks correctly use different parameters (φs0=0.6, K=7; partial adds the square domain) and are explicitly presented as demonstrations: `analysis.json` for each sets `reference_comparable: false` with a `reference_note`, `fe-evidence/manifest.json` lists `reference_comparison.csv` as `not_applicable` for them, `site/reports/finite-deformation-summary.json` reports no reference-normalized metric for them, and `sections/finite_elements.tex`, the abstract, the discussion, and `site/evidence.json` all state they are demonstrations rather than the reference-modulus Mandel comparison. `physical_validation` is `not_performed`; `finite_deformation` is `pending`. No overclaim was found.

## (4) Required corrections

No physics, source-fidelity, or numerical correction is required.

## (5) Optional suggestions

1. Unify or annotate the recorded environment blocks so the two supplement reports record a consistent NumPy version (or state that the constitutive verification and the experiments were produced under different supported environments).
2. Have `compute_mms_order.py` emit a snapshot-relative `runs_dir` (e.g. `fe-evidence/runs`) or add a note that the absolute path is a build-time runtime location.
3. Refresh `provenance/manuscript-export.json` so every listed path exists in the working tree, or narrow its description to a forward-looking export target list.

## (6) Review limitations

- Read-only review of the frozen snapshot; no MOOSE application compile/run was performed, so the C++ decks were checked against the manuscript and against the shipped Python law but were not re-executed. The recorded per-run logs, analyses, and provenance were instead re-hashed and cross-checked.
- The reference `sections/*.tex` derivation was spot-checked against the shipped implementations and reported reference values; it was not re-derived symbolically in full (charge was physics/source fidelity and packaging, not a complete mathematical proof).
- `site/reports/mandel-reference.json` and `mms-convergence.json` were inspected and their declared digests verified, but the Mandel series and MMS references were not independently re-implemented; their self-checks and the shipped convergence data were accepted as evidence after the shipped scripts' digests were confirmed.
- No access to any prior-round report, response, or verdict; earlier acceptance was not treated as evidence.
- Cross-platform floating-point and PDF metadata differences were not treated as defects, consistent with the supplement README.

VERDICT: ACCEPT
