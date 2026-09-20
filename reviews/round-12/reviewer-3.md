# Round-12 Reviewer 3 — prose, notation, and significance

## 1. Reviewed version, snapshot ID, and integrity result

- Repository: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
- Reviewed snapshot (read-only, mode 444/555): `.agent-runtime/review-snapshots/round-12`
- Live HEAD: `ecfe4a22a094d3b346ea89287f9a23e1917f017c`
- SNAPSHOT_ID (sha256 of `source-manifest.json`): `1797085484aca549014a3b3c8685a37c3bb892461b9e165635c61774513e2a9e`

**Integrity: PASS.** `sha256sum source-manifest.json` inside the snapshot root returned
`1797085484aca549014a3b3c8685a37c3bb892461b9e165635c61774513e2a9e`, equal to SNAPSHOT_ID.
Hashing every listed entry against the manifest:

```
listed total: 338
ok: 338 mismatch: 0 missing: 0
```

All 338 listed files verified (338/338 match; none missing, none mismatched). No snapshot file was modified; scratch work was confined to `/tmp`.

---

## 2. Audit evidence (commands + outputs)

### 2.1 Control-mode wording ("force-controlled" vs "displacement-controlled")

```
$ grep -rn "displacement-controlled\|force-controlled" --include=*.tex --include=*.md --include=*.json .
./sections/finite_elements.tex:139: ... For force-controlled consolidation, the
./sections/finite_elements.tex:215: The rotated-anisotropy and partial-drainage runs are force-controlled
./sections/finite_elements.tex:217: reaction is an equilibrium residual rather than a prescribed displacement.
./site/evidence.json:38,284; fe-evidence/plot-manifest.json (all cases): "force-controlled ... kinematic rigid platen"
```

No occurrence of "displacement-controlled" anywhere. The FE section correctly describes the decks as
force-controlled with a kinematic platen, and explicitly distinguishes the plate reaction from a
prescribed displacement. The stale-wording check requested by the charge is clean.

### 2.2 Percentage-range wording

```
$ grep -rni "percent\|\\\\%" --include=*.tex --include=*.md .
(no output)
```

No "60–100 percent"-style ranges appear in the manuscript. Not an issue.

### 2.3 FE quantitative sentences vs backing artifacts

Parameters in `sections/finite_elements.tex` ("φ_s0=0.9, K_s=2.5, μ_s=5/6, K=1, K_f=8, ρ̄_f0=1, k/μ_f=1.5", "G=0.75", "Biot 0.6", "total storage 17/80", "a=1 and b=0.1"):

```
$ grep -n "solid_fraction\|drained_bulk\|fluid_bulk\|mobility\|mineral_stiffness" fe-evidence/runs/linear_space_40/input.i
173: mineral_stiffness = '3.6111... 1.9444... ... 1.6666...'
174: solid_fraction = 0.9
175: drained_bulk = 1
176: fluid_bulk = 8
177: mobility = 1.5
```
Isotropic mineral block (C11=K_s+4μ_s/3=3.6111, C12=K_s−2μ_s/3=1.9444, C44=2μ_s=1.6667) is exactly φ_s0=0.9, K_s=2.5, μ_s=5/6, K=1.

```
$ python3 -c "... site/reports/mandel-reference.json ..."
parameters K=1.0, G=0.75, alpha=0.6, a=1.0, b=0.1  (M=4.70588 → storage=17/80)
```
Reference Biot coefficient 0.6 = 1−K/K_s, total storage 17/80 = (1−0.9)/8 + S_s with S_s=0.9/2.5·(1−1/2.25)=0.2. Both reproduce the stated values. **Verified.**

MMS settings ("U=P_0=0.01", "30° about the third axis"):

```
$ grep -n "expression\|angle" fe-evidence/runs/mms_space_4/input.i
32: exact_ux = 0.01*sin(t)*sin(pi*x)*sin(pi*y)        # matches eq:fe-mms-u1
36: exact_uy = 0.01*sin(t)*sin(pi*y)*cos(pi*x)        # matches eq:fe-mms-u2
40: exact_p  = 0.01*sin(t)*cos(pi*x)*cos(pi*y)        # matches eq:fe-mms-pressure
185: angle = 30
```
**Verified.**

Constitutive-count sentences in `sections/experiments.tex` ("186 named checks", "67 checks …", "largest … 2.5×10⁻⁹", "273 finite states across 13 mineral stiffnesses"):

```
$ python3 -c "... site/reports/conformal-verification.json ..."
checks_passed = 186 ; legacy_identities_rechecked = 67 ; max_constitutive_identity_error = 2.4549890331732928e-09
$ python3 -c "... site/reports/tensor-verification.json ..."
materials = 13 ; total_states = 273
```
186, 67, 2.45e-9 (≈2.5e-9), 273 states, 13 materials all match. **Verified.**

Site claim "C++ law matches the independent Python evaluation to about 6e-14 over 41 finite states":

```
$ python3 -c "... .agent-runtime/moose-fe-goal-2026-09-20/implementation/constitutive/report.json ..."
states: 41 rejected: 3
value_absolute_error: 6.394884621840902e-14
```
**Verified** (6.39e-14 ≈ 6e-14, 41 states).

Site claim "peak overshoot 5.4659% at t = 0.01516535":

```
$ python3 -c "... site/reports/mandel-reference.json ..."
checks: 38, passed: 38 ; time 0.015165352045764979
```
**Verified.**

### 2.4 Demonstration ranges (site text vs measured analyses)

```
$ for d in anisotropic_*; do python3 -c "... $d/analysis.json ..."; done
anisotropic_0        pressure_max 0.76197  platen 0.77541  edge_ux 1.77163  profile_max 0.76209  force_relative 4.0e-12
anisotropic_30       pressure_max 0.75757  platen 0.74466  edge_ux 1.71859  profile_max 0.75770  force_relative 2.1e-12
anisotropic_30_coarse pressure_max 0.75682 platen 0.74467  edge_ux 1.61138  profile_max 0.75751  force_relative 1.3e-10
anisotropic_30_fine  pressure_max 0.85752  platen 0.75598  edge_ux 1.77962  profile_max 0.87502  force_relative 4.1e-12
anisotropic_45       pressure_max 0.75500  platen 0.73198  edge_ux 1.69705  profile_max 0.75514  force_relative 2.3e-12
anisotropic_90       pressure_max 0.75486  platen 0.75821  edge_ux 1.77175  profile_max 0.75497  force_relative 1.6e-12
```

Measured envelopes over the anisotropic family:
- pressure_max: **0.7549 – 0.8575** (site says 0.73–0.86) — lower bound does not match
- platen: 0.7320 – 0.7754 (site says 0.73–0.78) — matches
- edge displacement: 1.6114 – 1.7796 (site says 1.61–1.78) — matches
- profile max: **0.7550 – 0.8750** (site says 0.74–0.88) — lower bound does not match

The same string is produced by `tools/populate_site_manifest.py:148-149`.

### 2.5 Small-load consolidation: paper wording vs evidence

`fe_load_limit.csv` (nonlinear FE vs linear Mandel reference, nx=20, dt=1e-3):

```
load 0.0001  pressure_max_normalized 0.00322
load 0.001   pressure_max_normalized 0.00345
load 0.01    pressure_max_normalized 0.00571
```

`site/evidence.json` case "Small-load isotropic Mandel consolidation" has `status: pending`,
"Tolerances under review", and `site/evidence.json:38` states the finite-load comparison
"floors at about 3.2e-3 … rather than decaying to the linear reference as the load tends to 1e-4".
`examples/plot_fe_results.py` (load-limit caption) states the same: "does not decay to the linear
reference; it floors at about 3.2e-3 … a finite-load demonstration, not a verified limit."

By contrast `main.tex` §1 (roadmap) and §Discussion state the FE discretization "reproduces the
constant-coefficient consolidation reference as the load vanishes" and "verify the implementation
against … the constant-coefficient consolidation reference".

### 2.6 Notation, framing, availability, references

- Bar/hat paragraph (`main.tex`, §"Deformation and volume-fraction-weighted stress"): separates bar on
  kinematic/energetic/intrinsic-density quantities (mineral state), bar on stress (mixture frame), and hat
  (true frame). Checked against every use (`\bar J,\bar{\mathbf F},\bar{\mathbf C},\bar W_s`,
  `\bar{\boldsymbol\sigma}_s`, `\bar{\boldsymbol\tau}_s`, `\hat{\boldsymbol\sigma}_s`, `\hat{\boldsymbol\tau}_s`,
  `\bar\rho_s`, `\bar\rho_f`). Consistent.
- Reference-vs-current volume convention: stated in `sections/finite_elements.tex`
  ("All mass measures … per unit reference mixture volume, whereas the intrinsic densities and volume
  fractions of the preceding sections are current-configuration measures; the two conventions differ by
  the factor J"), and consistent: pore volume per reference mixture volume `J−φ_s0\bar J = J(1−φ_s)`;
  `m_f=ρ̄_f(J−φ_s0\bar J)`; storage reduces to `(1−φ_s0)/K_f+S_s = 17/80`.
- Citation resolution:
  ```
  $ python3 resolve script
  cited keys: 21 ; missing in bib: [] ; uncited in bib: []
  ```
  `walker2023poroelasticity` is cited with an optional argument
  (`\cite[appendix D]{walker2023poroelasticity}`). All introduction citations resolve.
- Site: 19/19 artifact hashes in `site/evidence.json` match the files; `checksums.json` 25/25 match;
  all 24 `href`/`src` targets in `.agent-runtime/site/index.html` resolve on disk; snapshot
  `site/evidence.json` is byte-identical (sha256 `5a057aaf…`) to the live `.agent-runtime/site/evidence.json`.
- Figure legibility was checked indirectly: this model cannot render PNG content, so axis/unit labels were
  read from `examples/plot_fe_results.py` (e.g. `p(0,t)/p_0`, `u_y/q [length/stress]`,
  `Time [time unit]`, `X/Y [length unit]`, `p [stress unit]`, `B12 [dimensionless]`) and captions from
  `fe-evidence/plot-manifest.json`. Qualitative pixel-level legibility is therefore **not independently confirmed** (stated as a review limitation).

---

## 3. Findings

**F1 — Overstated small-load claim in the abstract/intro/conclusion (severity: moderate).**
`main.tex` §Discussion says the FE discretization "reproduces the constant-coefficient consolidation
reference as the load vanishes", and §1 lists "the constant-coefficient consolidation reference" among the
things the implementation is *verified* against. The evidence says the opposite about decay: the
nonlinear-to-linear discrepancy **floors at ≈3.2×10⁻³** (`fe_load_limit.csv`, load 1e-4) and the site
records the small-load Mandel case as `pending`, "Tolerances under review". The manuscript's own FE section
(§5) is careful here ("they need not reproduce its series at a finite load"), so the conclusion/roadmap
contradicts both the FE section and the artifacts. This is exactly the "demonstration presented as
verification" failure mode.

**F2 — Site range lower bounds do not match measured data (severity: minor).**
The published site/evidence text (`site/evidence.json:38`, generated by `tools/populate_site_manifest.py`)
states `pressure_max 0.73-0.86` and `profile max 0.74-0.88`. The measured minima are 0.7549 and 0.7550.
The 0.73/0.74 lower bounds appear in no anisotropic run; measured data support 0.75–0.86 and 0.75–0.88.
The `platen 0.73-0.78` and `edge displacement 1.61-1.78` ranges are correct.

**F3 — Code-availability locator for the FE evidence is ambiguous (severity: minor).**
`sections/experiments.tex` "Code and data availability" states the coupled FE implementation "is not part
of that archive: its application sources, deck inputs, per-run analyses, figure data, and the
machine-readable verification-evidence file are recorded separately in the same repository." No resolvable
locator (URL, DOI, path, or commit) for that repository/evidence is given in the manuscript; the only
external pointer is `foster2026poroplastic`, which is the *companion* manuscript. "The same repository"
is ambiguous (the archive? the companion repo? this paper's repo?). The coupled-code evidence exists in the
repository and is internally hashed, but the statement does not let a reader reach it.

**F4 — Minor bibliography inconsistency (severity: cosmetic).**
`references.bib` key `braun2020` carries `year = {2021}`. Key/year mismatch only; the reference itself is
correct and cited.

**Verified, no finding:** abstract, introduction roadmap, keywords, and the FE scope paragraph all state
implementation verification + finite-load demonstrations and explicitly disclaim quantitative
finite-deformation verification and experimental validation. Keywords include "finite-element
verification", which is consistent with MMS + constant-tangent + analytical-reference verification.
Bar/hat notation and the reference/current-volume mass convention are stated and consistent between the two
halves of the paper. All introduction citations resolve; previously uncited applied/experimental references
(cheng1997, wong2017, braun2020, sviridov2017, makhnenkolabuz2016, zhaoborja2020, macminnetal2016,
chaubazantsu2016, flory1961, dehghanipentamerodio2019, dehghanizilian2021) are now cited, and
zha1996forsterite is cited in the discussion. FE parameter/geometry values, check counts, and error
magnitudes trace to artifacts.

---

## 4. Required corrections

1. **Fix the small-load consolidation wording (F1).** In `main.tex` §1 and §Discussion, replace
   "reproduces the constant-coefficient consolidation reference as the load vanishes" / "verify the
   implementation against … the constant-coefficient consolidation reference" with wording that matches the
   artifacts: the constant-tangent (linear) runs reproduce the analytical Mandel reference to the recorded
   tolerance, while the finite-deformation solutions **approach** that reference as the load decreases but
   their discrepancy **floors at ≈3.2×10⁻³** and does not decay to it; the small-load comparison is a
   demonstration. *Why required:* the current sentence asserts a load→0 reproduction that the published
   evidence (`fe_load_limit.csv`, `site/evidence.json`) contradicts, converting a demonstration into a
   verification claim.

2. **Correct the site range lower bounds (F2).** Change `pressure_max 0.73-0.86` → `0.75-0.86` and
   `profile max 0.74-0.88` → `0.75-0.88` in `site/evidence.json` and
   `tools/populate_site_manifest.py` (then regenerate the site). *Why required:* published quantitative
   ranges must match the measured `analysis.json` values; the stated lower bounds appear in no run.

3. **Make the FE code/evidence locator resolvable (F3).** In the availability paragraph, name the
   repository and give a stable locator (URL + commit/path) for the coupled FE application sources, deck
   inputs, per-run analyses, figure data, and the verification-evidence file, and disambiguate
   "the same repository". *Why required:* an availability statement that asserts the existence of evidence
   without a locator does not meet the reproducibility requirement the paper sets for the constitutive
   supplement.

---

## 5. Optional suggestions

- **O1.** In the bar/hat paragraph, note explicitly that a bar on an *intrinsic density* (`\bar\rho_s`,
  `\bar\rho_f`) means "per phase volume" and that the mineral-state gloss applies to kinematic/energetic
  quantities; the current single gloss ("the mineral state reached by removing the distention") reads oddly
  for the fluid density `\bar\rho_f`.
- **O2.** Fix the `braun2020` key/year mismatch (cosmetic).
- **O3.** Consider stating the load-limit error floor (≈3.2×10⁻³) directly in the FE section, not only in
  the site, so the scope paragraph is self-contained.
- **O4.** Confirm figure font sizes/label legibility in a rendered check; this review could not inspect
  raster content and relied on the plotting code and captions.

---

## 6. Verdict

VERDICT: MINOR REVISION

The FE prose, notation, framing, and significance statements are largely accurate and appropriately
hedged, and the quantitative claims trace to artifacts. The required corrections are confined to wording
and one published range/locator: no new analysis, derivation, or computation is needed. F1 is the only
substantive rhetoric issue (a demonstration described as producing a vanishing-error reproduction); F2 and
F3 are correctness/availability fixes.
