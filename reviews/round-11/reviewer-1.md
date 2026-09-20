# Round-11 independent review — Reviewer 1 (mathematics and correctness)

## 1. Reviewed version and snapshot

- **Role:** independent reviewer 1 (mathematics / correctness). Not the author, not the
  editor; no outcome was assumed. I did not read any other reviewer's report or anything
  under `reviews/`.
- **Reviewed artifact (immutable snapshot):**
  `.agent-runtime/review-snapshots/round-11/`
- **Snapshot ID (sha256 of `source-manifest.json`):**
  `b9fadd66e96794417a4bed1f674064928716ffb3f2cc30d09edc0a663586fe6a`
- **Manuscript version metadata present in the snapshot:**
  - `fe-evidence/site-evidence.json` `version` = `moose-fe-pending-2026-09-20`
  - `site-evidence.json` `provenance.source_revision` = `ecfe4a22a094d3b346ea89287f9a23e1917f017c`
    (annotated "The base commit predates this working revision")
  - `main.tex` mtime 2026-09-20 14:22; `build/main.pdf` = 20 pages (confirmed with `pdfinfo`).

## 2. Integrity verification (mandatory first step)

Command run in the snapshot root:

```
sha256sum source-manifest.json
```

Result: `b9fadd66e96794417a4bed1f674064928716ffb3f2cc30d09edc0a663586fe6a`
→ **equals the SNAPSHOT ID. PASS.**

All listed files were then hashed and compared against the manifest (Python, streaming
read of each file):

```
total listed: 286
verified ok: 286
missing: 0
mismatched: 0
```

Re-verified at the end of the review (after all work was done in a `/tmp` copy):
`re-verify mismatches: 0`. **Integrity: PASS. No file in the snapshot was modified.**

I worked on a read-write copy at `/tmp/r11rev1/snap` and staged run data at
`/tmp/r11rev1/work`. The live repository was only read (and my single report file written).

## 3. What I inspected

- `main.tex` (full), `sections/stress_reconstruction.tex`, `sections/limits.tex`,
  `sections/experiments.tex`, `sections/finite_elements.tex`,
  `sections/logarithmic_derivative.tex`, `README.md`.
- `build/main.pdf` (20 pages, via `pdfinfo`), `build/main.log` (no undefined
  references/multiply-defined labels), `build/conformal/**`, `build/weighted-stress/**`.
- `fe-evidence/`: `site-evidence.json`, `mms-convergence.json`, `compute_mms_order.py`,
  `plot-manifest.json`, `runs/*/{analysis.json,input.i,provenance.json,reference_comparison.csv}`
  (all 38 run directories), and `figures/*.csv`.
- Implementation trace: `moose_app/scripts/{analyze_mandel.py,decks.py,run_demonstrations.py,verify_constitutive.py}`,
  `moose_app/src/postprocessors/DofReactionSum.C`, run `input.i` decks.
- Cited verification reports: `site/reports/*.json` and `site/scientific-snapshot.json`
  (read from the live repository — see finding **MAJOR-1** for why they are not in the snapshot).

## 4. Independent recomputation (commands and numbers)

All recomputation was done in `/tmp/r11rev1` against the snapshot copy and `/tmp`-staged
live run data. Note: `fe-evidence/runs/*/` in the snapshot contains only
`analysis.json`, `input.i`, `provenance.json` (and, for Mandel cases,
`reference_comparison.csv`); `solution.csv`/`solution.e` are **not** in the snapshot but are
present in the live repo at
`.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs/`, where I verified each
`solution.csv` matches the SHA-256 recorded in that run's `provenance.json`.

### (a) MMS orders re-derived from `analysis.json` (my own script, not the shipped one)

```
python3 - <<'PY'   # reads fe-evidence/runs/*/analysis.json, computes naive ratios and
...                # successive-deficit ("difference") orders
```

Results:

```
=== SPATIAL (fixed dt=1e-4, end=0.01), nx 4,8,16 ===
ux_l2: err=[1.6422e-07, 2.0647e-08, 2.6562e-09]  naive=[2.9917, 2.9585]  diff_order=[2.9965]
uy_l2: err=[1.6952e-07, 2.1216e-08, 2.7266e-09]  naive=[2.9983, 2.9600]  diff_order=[3.0038]
p_l2 : err=[4.8587e-06, 1.2175e-06, 3.0421e-07]  naive=[1.9966, 2.0008]  diff_order=[1.9952]

=== TEMPORAL ===
nx=16 (dt .02,.01,.005): ux diff_order=1.0932  uy=0.9783  p=1.0152
nx=32                   ux diff_order=1.3969  uy=1.0183  p=1.1252
nx=64                   ux diff_order=1.3964  uy=1.0762  p=1.2519
```

**Match to the brief:** nx16 `1.093/0.978/1.015` ✓; nx32 `1.397/1.018/1.125` ✓;
nx64 `1.396/1.076/1.252` ✓; spatial `2.99/2.96, 3.00/2.96, 2.00/2.00` ✓.
Every quoted number is reproduced.

### (b) The shipped evidence generator, run as-is

```
cd /tmp/r11rev1/snap/fe-evidence && python3 compute_mms_order.py
```

The script exited 0 but emitted **empty** `space`/`time` blocks and silently rewrote
`fe-evidence/mms-convergence.json` to an all-empty document. Cause: line 16,
`RUNS = Path(__file__).resolve().parents[1] / "implementation" / "runs"`, resolves to the
snapshot root, where there is no `implementation/` directory (see **MAJOR-2**).

With only that path corrected (`parents[0] / "runs"`, i.e. `fe-evidence/runs`), the script's
output is **exactly equal** to the committed `mms-convergence.json`:

```
EXACT-EQUAL: True      num diffs (tol 1e-12 rel): 0
```

So the *numbers* are fully reproducible; only the shipped path is wrong in the snapshot layout.

### (c) Recompute of `analysis.json` from its `solution.csv`

```
cd /tmp/r11rev1/work    # linear_space_20/ copied from the live runs dir
python3 - <<'PY' ... uses validation/mandel_reference.py ...
```

```
p0 = 4.795204795204795e-05
pressure_max_normalized  recomputed=0.0004576366802955016  claimed=0.0004576366802955016  match=True
force_relative           recomputed=8.115998650047584e-11  claimed=8.115998650047584e-11  match=True
```

### (d) Manuscript constitutive numbers re-derived from the tensor algebra

Rebuilt `C_s` from `eq (19)` in Mandel basis and evaluated the constitutive restrictions
(order of contraction of `C^d : C_s^{-1} : I` matters; verified in full tensor form):

```
K_s = 28.0
K_d = 7.000000000000002                       (abstract/section claim "K = 7K_*")
B0 normal components = [0.70, 0.75833333, 0.79166667]
                                              (claim "0.7000, 0.7583, 0.7917" ✓)
C_s positive definite (eigenvalues 20,24,28,41.98,51.79,86.23) ✓
0 < K < phi_s0*K_s  →  0 < 7 < 16.8  ✓
compliance restriction (C^d)^{-1}-(phi Cs)^{-1} = c I⊗I  max abs err = 8.673617379884035e-18 ✓
deviatoric stiffness modes of C_s: [20,24,28,42.9668,53.0332], mean/2 = 16.8 ✓
("isotropic mineral shear modulus 16.8K_*")
isotropic-comparison mineral → spherical B = 0.75 I  ✓
Mandel reference problem: K_d=1 → G=0.75, alpha=1-1/2.5=0.6, (1-phi_s0)/K_f+S_s = 0.0125+0.2 = 0.2125 = 17/80 ✓
```

### (e) Reported check counts / error magnitudes

| Manuscript / site claim | Artifact | Verified |
|---|---|---|
| conformal suite 186 checks; 67 rotation/work/volume | `build/conformal/verification.json` `checks_passed=186`, `legacy_identities_rechecked=67` | ✓ |
| largest constitutive identity error 2.5e-9 | same file `max_constitutive_identity_error=2.4549890331732928e-09` | ✓ |
| step refinement second order (energy/pore-volume/pressure) | `observed_orders` ≈ 2.0004 / 2.0002 / 2.00 | ✓ |
| 273 finite states across 13 mineral stiffnesses | `build/weighted-stress/tensor-verification.json` `total_states=273`, `materials=13` (21/material) | ✓ |
| fluid EOS/reference-mass 110 checks, max scaled error 8.09e-9 | `site/reports/fluid-coupling-verification.json` `count=110`, `maximum_scaled_error=8.0867e-09` | ✓ |
| C++ law matches NumPy oracle ~6e-14 over 41 finite states | `.agent-runtime/.../implementation/constitutive/report.json` `states=41`, `value_absolute_error=6.394884621840902e-14` | ✓ |
| Mandel reference 38 self-checks; overshoot 5.4659% at t=0.01516535 | `site/reports/mandel-reference.json` `central_overshoot.ratio=1.0546586069998425`, `time=0.015165352045764979`, 38 checks | ✓ |
| reconstruction suite work-equivalence/unjacketed | `build/weighted-stress/reconstruction-verification.json` errors all ≤ 2.8e-9 | ✓ |

### (f) Numerical-setup confirmation for the convergence claim

`fe-evidence/runs/mms_space_4/input.i`: `elem_type = QUAD9`; `ux`/`uy` `order = SECOND`;
`p` `order = FIRST`; `[Executioner] scheme = implicit-euler`. This independently confirms
the site text "consistent with Q2 displacement and Q1 pressure" and "consistent with
backward Euler". The MMS case sets `linear_reference = true` (constant reference tangent),
i.e. it tests the linearised operator, exactly as the manuscript states.

**Conclusion of recomputation: every quantitative claim I checked reproduces. No
unreproducible number was found.**

## 5. Findings

### BLOCKING

None. (See MAJOR-1 for a traceability defect that a strict reading of the
"passed without a supporting artifact" rule would elevate to blocking; I explain there why
I do not treat it as a false scientific pass.)

### MAJOR

**MAJOR-1 — The reviewed snapshot omits the report artifacts cited by
`fe-evidence/site-evidence.json`, so two "passed" categories are unsupported inside the
snapshot itself.**
`site-evidence.json` (in the snapshot) cites artifact paths under `site/reports/` and
`site/scientific-snapshot.json` (lines ~166–215), and the `analytical` category
(line 12–13, `"status": "passed"`) cites evidence id `mandel-reference` →
`site/reports/mandel-reference.json`, while the `implementation` category (line 19–20)
cites `fluid-coupling-verification` → `site/reports/fluid-coupling-verification.json`.
The snapshot manifest lists **no `site/` or `validation/` paths at all**; `site/reports/mandel-reference.json`,
`site/reports/fluid-coupling-verification.json` and `site/scientific-snapshot.json` are absent
from the snapshot and from `source-manifest.json`. An auditor restricted to the snapshot
cannot substantiate the `analytical` pass (and one of four `implementation` items).
Mitigation I verified: these files **do exist in the live repository** and their SHA-256
values match the hashes cited in `site-evidence.json`
(`mandel-reference 534c3a06…`, `fluid-coupling-verification 5842f2eb…`,
`scientific-snapshot 284aeeb2…`), and I read their contents (they do support the claims,
§4e). The other three cited reports resolve by hash to files that *are* in the snapshot
(`conformal-verification` → `build/conformal/verification.json`;
`tensor-verification` → `build/weighted-stress/tensor-verification.json`;
`reconstruction-verification` → `build/weighted-stress/reconstruction-verification.json`;
`mms-convergence` → `fe-evidence/mms-convergence.json`), but the `site-evidence.json`
`path` fields still point at the non-existent `site/reports/…` locations.
**Required correction:** include the cited report artifacts in the snapshot (or rewrite the
`path` fields to the in-snapshot locations and add them to the manifest).
*Strict reading:* because a category is marked `passed` while its cited artifact is absent
from the reviewed package, this is blocking under the review brief; I classify it MAJOR
only because the artifacts exist, hash-match, and substantiate the claims in the live
repository, so no false scientific pass is alleged.

**MAJOR-2 — `fe-evidence/compute_mms_order.py` (snapshot) cannot reproduce its own evidence
and silently destroys it.**
Line 16: `RUNS = Path(__file__).resolve().parents[1] / "implementation" / "runs"`.
In the snapshot, `parents[1]` is the snapshot root, which has no `implementation/`
directory, so `load()` returns `None` for every case and the script prints an all-empty
document and **overwrites `fe-evidence/mms-convergence.json` with empty `space`/`time`
objects** (exit code 0, no error). The script's home in the live repo is
`.agent-runtime/moose-fe-goal-2026-09-20/parent-analysis/compute_mms_order.py`, where
`parents[1]` is `moose-fe-goal-2026-09-20` and `implementation/runs` exists — so the defect
was introduced by the snapshot relocation, not by a wrong algorithm. With the path
corrected to `fe-evidence/runs`, output is byte-for-byte equal to the committed file (§4b).
**Required correction:** make `RUNS` resolve to the evidence directory in the shipped
layout, and fail loudly (non-zero exit) instead of writing an empty evidence file.

### MINOR

**MINOR-1 — `site-evidence.json` line 38 understates the demonstrated differences.**
It states "Differences of 60-100 percent in pressure and displacement". The recorded
metrics are larger for displacement: `edge_ux_max_normalized` is 1.7166 (anisotropic_30)
to 1.7717 (anisotropic_90), i.e. **170-178 %**, and `platen_max_normalized` up to 0.775.
The pressure metric (0.715-0.762) is consistent with "60-100 %". Recommendation: state the
displacement range as ~170 % (or report each metric separately).

**MINOR-2 — the convergence summary quotes temporal orders above first order while
asserting "not higher".**
`site-evidence.json` line 31: "temporal order … is first order (nx=64: ux 1.40, uy 1.08,
p 1.25), consistent with backward Euler and **not higher**". Quoting nx=64 ux = 1.40 and
p = 1.25 is inconsistent with "no order greater than first order may be quoted"; those
values are best explained by residual mesh-floor contamination at the finest level (the
deficits there are ~2-6×10⁻¹⁰ for ux). The cleaner fixed-mesh estimates are the nx=16
values (ux 1.09, uy 0.98, p 1.02). Recommendation: quote the nx=16 triple (or a stated
bound ≤ ~1.1) and note that the difference-of-norms estimator only bounds the order near
one. (The method itself is correctly described, and naive ratios are correctly excluded.)

**MINOR-3 — the `force_relative ≈ 1.0` explanation is qualitative and does not identify the
quantity that produces it.**
`site-evidence.json` line 38: "A force_relative value of approximately 1.0 reflects the
kinematic platen constraint, not a force-balance failure." From
`moose_app/scripts/analyze_mandel.py`, `force_relative = max|top_reaction − (−q)|/q`; the
recorded finite-deformation value is `1.000000000008` for the anisotropic cases and
`1.0` for `partial_30`, which requires `top_reaction ≈ 0` (to ~1e-12). The metric compares a
displacement-controlled run against a force-control reference (`expected_force = −q`), so it
is not a force-balance measure for these runs. Recommendation: state `top_reaction ≈ 0`
explicitly, and mark the metric as not applicable (or drop it) for the demonstration runs.
This does not affect the category status (see below).

**MINOR-4 — `figures/fe_load_limit.csv` / figure caption "finite-load limit toward the
linear reference" is not demonstrated by the data.**
Recorded `pressure_max_normalized` is 0.00322 (load 1e-4), 0.00345 (1e-3),
0.00571 (1e-2) — essentially flat (a ~0.3 % discretization floor at nx=20, dt=1e-3), not
decaying toward the reference as the load → 0. The site lists the case as `pending` and the
analytical summary says the tolerance "is still being finalized", so this is disclosed;
but the figure/caption framing should be softened to "finite-load comparison" until a
tolerance is stated.

### OPTIONAL

**OPT-1** — `fe-evidence/runs/*/` contains no `solution.csv`/`solution.e` even though
`provenance.json` records their SHA-256. Including at least the Mandel and MMS `solution.csv`
files (as the task anticipated) would let a reviewer recompute `analysis.json` without
reaching into the live repo.

**OPT-2** — manuscript §finite_elements could state the MMS orders it relies on (currently
the numbers appear only in `site-evidence.json`), and could state explicitly that the
difference-of-norms order is a bound near one, not an estimate of 1.4.

**OPT-3** — the appendix sentence "The coefficient is symmetric in i,j, which makes the
derivative self-adjoint" (sections/logarithmic_derivative.tex) is correct; adding the
one-line reason (`(lnλi−lnλj)/(λi−λj)` is symmetric under i↔j) would remove an ambiguity.

## 6. Mathematics assessment

I re-derived, independently of the manuscript's algebra, and found no error in:

- the change of variables `F = a^{1/3}R_A F̄` and `δF F^{-1}` split
  (`main.tex` eqs. 13-15), including the vanishing skew term;
- the phase-stress balance `τ' = φ_{s0}(τ̄_s + pJ̄ I)` (eq. 16) and its equivalence with the
  integrated energy (eqs. 17-18), which I reconfirmed by direct chain-rule differentiation
  including the `a`-dependence of `F̄` at fixed `J̄`;
- the objectivity argument that makes `W_s` independent of `R_A` (eqs. 19-20);
- the distention energy `W_A(a)` and the mineral-volume equation (eqs. 26, 31), which I
  reproduced term by term;
- the drained stiffness restriction (eq. 32) and its compliance form (eq. 37), verified
  numerically to 8.7e-18;
- the explicit anisotropic Biot tensor (eq. 23), whose isotropic limit (eq. 43) and
  reference limit `B_0 = I − C^d:C_s^{-1}:I` (eq. 42) both follow, and which I verified
  numerically against the manuscript's quoted 0.7000/0.7583/0.7917;
- the spectral matrix-logarithm derivative in the appendix (eqs. A.5-A.7).

Consistency checks that legitimately pass/fail as stated: `dev(C_s:I)=0` for cubic symmetry
→ spherical `B` even with anisotropic mineral shear (I confirmed this from the tensor
algebra); the example `C_s` is orthorhombic (not cubic), so `dev(C_s:I)≠0` and the reference
Biot tensor is correctly nonspherical; the unjacketed branch is verified at 5e-14 in the
reconstruction report.

Category-status judgement:
- `convergence = passed` — justified: `fe-evidence/mms-convergence.json` (in snapshot) is
  exactly reproducible (§4a/§4b); Q2/Q1 orders confirmed from `input.i`; the Mandel
  non-monotonicity is disclosed and its attribution to the initial drainage boundary
  discontinuity is consistent with the per-time errors in `linear_space_{10,20,40}` (at
  t=0.01 the errors are 0.00607/0.00246/0.00262 — non-monotone at the finest level; at
  t≥0.05 they decrease monotonically 0.00153/0.000475/0.000388).
- `analytical = passed` — substantiated by the `mandel-reference` report, but that report is
  not in the snapshot (MAJOR-1).
- `implementation = passed` — substantiated by four reports; three are present in-snapshot by
  hash, one (`fluid-coupling-verification`) is not (MAJOR-1).
- `finite_deformation = pending` — honest. The runs are demonstrations; recorded differences
  are 71-86 % (pressure/platen) and up to 178 % (edge displacement); `force_relative ≈ 1.0`
  reflects `top_reaction ≈ 0`. No quantitative verification is claimed. The only defect is
  the 60-100 % wording (MINOR-1) and the force_relative phrasing (MINOR-3).
- `physical_validation = not_performed` — honest; parameters are synthetic and no
  measurement comparison is made.

## 7. Verdict

The mathematics is sound and, with one narrow exception noted above, every numerical claim
in the manuscript and in `fe-evidence/site-evidence.json` is supported by a recorded
artifact that I independently reproduced. The required corrections are (i) snapshot
completeness/traceability for the artifacts cited by `site-evidence.json` (MAJOR-1),
(ii) the broken and silently-destructive path in `compute_mms_order.py` (MAJOR-2), and
(iii)-(vi) four short text/data-consistency corrections. No false scientific pass and no
mathematical error was found. This is not an ACCEPT because corrections to the
claim-to-evidence linkage in the reviewed package are required; it is not REJECT because no
claim failed reproduction.

**VERDICT: MAJOR REVISION**
