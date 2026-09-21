# Round 26 — Independent reviewer 2 (physics / source fidelity / packaging)

Snapshot reviewed: `.agent-runtime/review-snapshots/round-26`
Declared SNAPSHOT_ID: `6e1afd9363639bdedf68ad4c42169710b7e74830e7d5fa83af91d3387c142907`

All work was read-only on the frozen snapshot; the only file written is this report. Every number below
is stated with the exact command that produced it. Chat/launch summaries were treated as claims to be
re-tested, not as evidence.

---

## 1. Snapshot integrity

| # | Check | Command | Result |
|---|-------|---------|--------|
| 1.1 | Manifest digest vs declared SNAPSHOT_ID | `sha256sum .agent-runtime/review-snapshots/round-26/source-manifest.json` | `6e1afd9363639bdedf68ad4c42169710b7e74830e7d5fa83af91d3387c142907` — **matches declared ID** |
| 1.2 | `SNAPSHOT_ID` file content | `cat .agent-runtime/review-snapshots/round-26/SNAPSHOT_ID` | same 64-hex string |
| 1.3 | Manifest entry count | `python3 -c "import json;print(len(json.load(open('source-manifest.json'))))"` | **591** |
| 1.4 | Re-hash every entry | `python3 - <<'EOF'` (walk manifest, `sha256(file)`) | **OK 591 / MISSING 0 / MISMATCH 0** |
| 1.5 | Files on disk not in manifest | same script, `os.walk` vs manifest keys | **0 extra** (excl. `source-manifest.json`, `SNAPSHOT_ID`) |
| 1.6 | Internal digests: `fe-evidence/manifest.json` | re-hash all 317 `files[]` entries | **317 OK / 0 missing / 0 mismatch** |
| 1.7 | Internal digests: `site/scientific-snapshot.json` | re-hash all 45 `files[]` entries | **45 OK / 0 missing / 0 mismatch** |
| 1.8 | Internal digests: `site/evidence.json` artefacts | re-hash all 23 `artifacts[]` digests | **23 OK / 0 missing / 0 mismatch** |
| 1.9 | Working tree vs snapshot drift | `sha256sum` of 9 key files (main.tex, sections, site manifests, tools, figures, fe-evidence, build/main.pdf) | **all SAME** — the tree has not moved since the freeze |

**Integrity verdict: CLEAN.** No required integrity item.

---

## 2. Physics and source fidelity — independent checks

### 2.1 Pore-fabric construction (independent re-derivation)

* `eq:fabric-tensor` sets \(\mathbf H=a^{-2/3}\mathbf G\), \(\det\mathbf H=1\) (since \(a^2=\det\mathbf G\)). Consistent.
* `eq:fabric-transverse-h` gives \(\mathbf H=h^{-2}\mathbf m\otimes\mathbf m+h(\mathbf I-\mathbf m\otimes\mathbf m)\); I recomputed its eigenvalues as \(h^{-2},h,h\) and \(\det\mathbf H=1\). Consistent, and consistent with the shipped check `H_eigenvalues` in `site/reports/fabric-verification.json`: `[0.9992863543052308, 1.000357013944851, 1.000357013944851]`, which are exactly \(h^{-2},h,h\) for \(\ln h=3.5695\times10^{-4}\) (`figures/fe_fabric_probe.csv`, case `fabric_probe_coup_a45`).
* `eq:fabric-transverse-strain`: \(\mathbf E_{\mathrm{dis}}=\tfrac{\ln a}{3}\mathbf I+\ln h(\tfrac12\mathbf I-\tfrac32\mathbf m\otimes\mathbf m)\). I verified \(\exp(2\mathbf E_{\mathrm{dis}})=a^{2/3}\mathbf H=\mathbf G\) symbolically. I also verified the strain lies in the retained subspace: with \(\mathbf e_2=\sqrt{3/2}(\mathbf m\otimes\mathbf m-\mathbf I/3)\) one has \(\tfrac12\mathbf I-\tfrac32\mathbf m\otimes\mathbf m=-\sqrt{3/2}\,\mathbf e_2\) and \(\mathbf I=\sqrt3\,\mathbf e_1\), so \(\mathbf E_{\mathrm{dis}}\in\operatorname{span}(\mathbf e_1,\mathbf e_2)\). This is exactly the condition the text claims makes the reduced model *exact*, so `sec:fe-fabric`'s "holds exactly in this subspace" and "\(h=\mathrm{e}^{\ln h}\), not a projection of it" are supported.
* \(\mathbf e_1=\mathbf I/\sqrt3\), \(\mathbf e_2=\sqrt{3/2}(\mathbf m\otimes\mathbf m-\mathbf I/3)\) are orthonormal under double contraction (I recomputed \(\lVert\mathbf e_2\rVert=1\), \(\mathbf e_1{:}\mathbf e_2=0\)). The R25-3-1 fix (\(\mathbf m\) defined at first use) is present at `sections/pore_fabric.tex:283`.

### 2.2 Does the volume–axial distention modulus really carry \(B_\parallel\neq B_\perp\)?

This is the paper's central physics claim, so I checked it two ways.

* **Analytically.** With an isotropic mineral, \((\phi_{s0}\mathbb C_s)^{-1}\) acts as \(\alpha\) on the volumetric direction \(\mathbf e_1\) and \(\beta\) on the other five modes; the retained \(\mathbb D\) is a \(2\times2\) block \((\alpha+k_v,\;k_c,\;k_a)\). If \(k_c=0\) the composite is diagonal, so \(\mathbb C^d{:}\mathbf I=\sqrt3\,(\mathbb C^d{:}\mathbf e_1)\) is purely volumetric and \(\mathbf B_0=\mathbf I-\tfrac{1}{3K_s}\mathbb C^d{:}\mathbf I\) is **spherical**, even though \(\mathbb C^d\) is genuinely transversely isotropic (\(\mathbb C^d\) still differs between \(\mathbf e_1\) and \(\mathbf e_2\)). If \(k_c\neq0\), \(\mathbb C^d{:}\mathbf e_1\) acquires an \(\mathbf e_2\) component, \(\mathbb C^d{:}\mathbf I\) becomes transversely isotropic and \(\mathbf B_0\) becomes \(B_\parallel\mathbf m\otimes\mathbf m+B_\perp(\mathbf I-\mathbf m\otimes\mathbf m)\) with \(B_\parallel\neq B_\perp\). **The claim is correct.**
* **Against the shipped evidence** (`site/reports/fabric-verification.json`, key `limits`):
  * `no_coupling_isotropic_biot` → anisotropy \(1.11\times10^{-16}\) (spherical),
  * `frozen_shape_isotropic_biot` → anisotropy \(-1.11\times10^{-16}\) (spherical),
  * `coupling_gives_anisotropy` → \(B_\parallel=0.8506544\), \(B_\perp=0.9102700\), anisotropy \(-0.0596156\).
* **A sharper check of the mechanism.** Case `fabric_probe_softaxial` (`figures/fe_fabric_probe.csv`) has a *non-zero* shape, \(\ln h=-0.0078125\), yet \(B_\parallel=B_\perp=0.88387097\) and `B_anisotropy = -1.11e-16`. So a non-trivial fabric shape alone leaves \(\mathbf B\) spherical; the directional Biot coupling is carried by the volume–axial modulus, exactly as `sec:fabric-transverse` and the `fig:fe-fabric-probe` caption state.

### 2.3 Undrained / drained limits and Mandel consistency

* All 38 analytical-reference checks pass: `python3 -c "import json;v=json.load(open('site/reports/mandel-reference.json'))['verification'];print(len(v['checks']), all(c['passed'] for c in v['checks'].values()))"` → `38 True`. The undrained and drained blocks (`undrained_fluid_content`, `undrained_vertical_stress`, `drained_pressure`, `drained_ux`, `drained_uy`, `drainage_*`, `rigid_platen_*`) are all within tolerance.
* I re-derived the Mandel parameters from `parameters` {K=1, G=0.75, α=0.6, M=4.7058824, a=1, b=0.1}: \(K_u=K+\alpha^2M=2.6941176\) (shipped 2.6941176470588237), Skempton \(B=\alpha M/K_u=1.04803\) (shipped 1.0480349344978166), \(\nu_u=0.372627\) (shipped 0.3726273726273726). Consistent.
* The central-pressure overshoot quoted in `site/evidence.json` ("peak overshoot 5.4659% at t = 0.01516535") reproduces from `site/reports/mandel-reference.json` → `central_overshoot` \(\{\)`ratio` \(=1.0546586069998425\), `time` \(=0.015165352045764979\}\). \(1.0546586-1=5.4659\%\). Consistent.
* The manuscript's FE peaks reproduce from `figures/fe_fabric_mandel_peak.csv` / `figures/fe_fabric_contours.csv`; see §2.4.

**Physics verdict: no physical-soundness defect found.** The construction, the limit reductions, the modulus-carries-coupling claim, and the Mandel/undrained/drained results are self-consistent.

### 2.4 Every quoted number reproduces from the shipped artifacts

Each row was checked by reading the named artifact directly.

| Quoted (source file, line) | Artifact | Value found | OK |
|---|---|---|---|
| reconstruction \(2.2\times10^{-16}\) (`finite_elements.tex:270`) | `site/reports/fabric-verification.json` `tensor_checks.H_reconstruction_max_abs_diff` | `2.220446049250313e-16` | ✓ |
| \(\det\mathbf H-1=-3.3\times10^{-16}\) (:270) | `tensor_checks.H_det_minus_one` | `-3.3306690738754696e-16` | ✓ |
| \(\lVert\mathbb D:\mathbf e_3\rVert=1.6\times10^{-16}\) (:272) | `tensor_checks.D4_e3_norm` | `1.5823112613210482e-16` | ✓ |
| \(\mathbb D:\mathbf e_6=\mathbf 0\) (:272) | `tensor_checks.D4_e6_norm` | `0.0` | ✓ |
| rotation invariance \(2.5\times10^{-16}\) (:274) | `tensor_checks.rotation_invariance_norm` | `2.4965357070272594e-16` | ✓ |
| worst NumPy diff \(4.9\times10^{-15}\) (:278) | `worst_probe_abs_diff` (max over cases) | `4.884981308350689e-15` | ✓ |
| conformal reduction \(1.9\times10^{-14}\) (:286) | `conformal_cross_check.sigma11.abs_diff` | `1.8741952434453424e-14` | ✓ |
| peaks \(4.36/4.99/5.52\times10^{-5}\), uncoupled \(3.62\times10^{-5}\) (:314–317) | `figures/fe_fabric_mandel_peak.csv` | `4.3627593400865e-05`, `4.9900848305106e-05`, `5.521105069019e-05`, `3.6163929824772e-05` | ✓ |
| contour peaks \(3.61/4.35/4.97/5.50\times10^{-5}\) (:328–330) | `figures/fe_fabric_contours.csv` | `3.606194309585106e-05`, `4.3491366180031454e-05`, `4.973659107895197e-05`, `5.503135423750668e-05` | ✓ |
| displacement maxima \(5.18/5.14/2.38/5.26\times10^{-5}\) (:333–334) | `figures/fe_fabric_contours.csv` `u_mag_max` | `5.1826e-05`, `5.1372e-05`, `2.3818e-05`, `5.2587e-05` | ✓ |
| "maximum lies on \(X_1=0\)", "falls to zero at \(X_1=1\)" (:330) | same, `p_max_x=0.0` for all four cases; `p_min≈-1e-127…-4e-167` | ✓ |
| "each peak coincides with the final recorded state" (:317) | peak CSV: `peak==final`, `peak_stability=2.5` | ✓ |
| floor \(3.2\times10^{-3}\) at nx=20, dt=\(10^{-3}\) (`main.tex:566`) | `figures/fe_load_limit.csv` `nonlinear_load_0.0001/pressure_max_normalized` | `0.003220919735602341` | ✓ |
| \(3.7\times10^{-3}\) and \(7.1\times10^{-3}\) at dt=\(10^{-3}\), \(2\times10^{-3}\), ratio 1.94 (`main.tex:568`) | `figures/fe_mandel_refinement.csv` `linear_time_0.001/0.002` | `0.003657958974355574`, `0.0071039215708695895`; ratio `1.9421` | ✓ |
| MMS spatial orders 2.99/2.96, 3.00/2.96, 2.00/2.00 (`site/evidence.json`) | `site/reports/mms-convergence.json` `space.orders` | `2.9917/2.9585`, `2.9983/2.9600`, `1.9966/2.0008` | ✓ |
| temporal 1.093/0.978/1.015; nx=32 1.397/1.018/1.125; nx=64 1.396/1.076/1.252; range 0.98–1.40 (`main.tex:570`) | `mms-convergence.json` `time.{nx16,nx32,nx64}` | `1.0932/0.9783/1.0152`, `1.3969/1.0183/1.1252`, `1.3964/1.0762/1.2519` | ✓ |
| "110 checks, max scaled error 8.09e-09" | `site/reports/fluid-coupling-verification.json` | `count=110`, `maximum_scaled_error=8.086725789002713e-09` | ✓ |
| "6.4e-14 over 41 finite states" | `site/reports/cpp-python-constitutive.json` | `value_absolute_error=6.394884621840902e-14`, `states=41` | ✓ |
| "186 named checks", "65 per-state identities", "273 finite states across 13 mineral stiffnesses", "2.5e-9" (`experiments.tex:180,191`) | `conformal-verification.json` (`checks_passed=186`, `legacy_identities_rechecked=67=65+2`), `tensor-verification.json` (`total_states=273`, `materials=13`), `max_constitutive_identity_error=2.4549890331732928e-09` | ✓ |
| "20 materials, 20 incompatible pairs rejected" | `reconstruction-verification.json` | `materials=20`, `incompatible_pairs_rejected=20` | ✓ |
| finite-deformation diagnostics (`site/evidence.json` `finite_deformation`) | `site/reports/finite-deformation-summary.json` | peaks `0.20618076–0.21577361` at t=0.002–0.004; `force_relative_max=1.2764e-10`; `…mobilized_relative_max=2.4699e-10`; isotropic `0.22382672`, `3.2144e-12`; partial `0.20051526–0.20162858`, `2.0521e-10`, `4.6363e-10` | ✓ |

**Nothing quoted in `main.tex` or `sections/*.tex` failed to reproduce.**

### 2.5 Figure / PDF / archive packaging

* Every `\includegraphics` target resolves (11/11): `grep -rhoE "includegraphics(\[[^]]*\])?\{[^}]*\}" main.tex sections/*.tex` → all 11 paths exist on disk.
* Each manuscript figure is reproducible from a shipped script: `examples/plot_fabric_results.py` (probe, mandel — `figures/fabric-plot-manifest.json` generator field), `examples/plot_fabric_contours.py` (contours, diffusion — `figures/fe_fabric_contours-plot-manifest.json`), `examples/plot_fe_verification.py` (convergence, reference comparison — `figures/fe-verification-plot-manifest.json`), `examples/conformal_experiments.py` (the five `build/conformal/*.pdf`). All four plot manifests report `"missing": []`.
* `build/main.pdf`: sha256 `db90490c04a7af322087e841dd01eac194de27f46a8baf49305859f5a57fe0c1` — identical to the ID declared in LAUNCH-STATE; `build/main.log` reports 33 pages; `grep -ci undefined build/main.log` → 0; `grep -c Overfull build/main.log` → 0.
* Embedded supplement: `pdfdetach -saveall build/main.pdf` extracts `anisotropic-biot-2026-09-20-v2.zip` with sha256 `46ef65aad77df01de64054108c5a0b0ec4a91718a73123f620f1793f6cba2c54`, **byte-identical to `build/anisotropic-biot-2026-09-20-v2.zip`** (69 entries). PDF and supplement are internally consistent.
* The supplement **does** contain the fabric evidence (`unzip -l … | grep -i fabric` → `FabricLaw.h`, `FabricMaterial.C`, `fabric_*.i`, `fe-evidence/runs/fabric_*`, `examples/verify_fabric.py`, `examples/plot_fabric*.py`, `tools/rerun_fabric_contours.py`). This matters for finding 1 below.

---

## 3. Findings

### Finding 1 — REQUIRED. The shipped companion-site manifests are not the output of the shipped registration tool; none of the pore-fabric evidence is registered, and the manifest cannot be regenerated from the shipped pipeline.

The repository ships `tools/register_fabric_evidence.py`, whose docstring is *"Register the pore-fabric evidence in the companion site manifests. Idempotent: adds the fabric report, figures, figure data, and source files to `site/evidence.json` and `site/scientific-snapshot.json`…"*. The LAUNCH-STATE also asserts, for the round-25 required fix R25-2-1, that `site/evidence.json` and `site/scientific-snapshot.json` were *regenerated*. On disk neither file is that regenerated artifact.

Commands and results:

```sh
# state of the shipped manifest
grep -ic fabric .agent-runtime/review-snapshots/round-26/site/evidence.json      # -> 0
python3 -c "import json;d=json.load(open('.../site/evidence.json'));print(len(d['artifacts']),len(d['figures']),len(d['cases']))"   # -> 23 7 3

# re-run the shipped tool on a writable copy of the frozen snapshot
cp -a .agent-runtime/review-snapshots/round-26/. /tmp/r26copy/ && cd /tmp/r26copy
python3 tools/register_fabric_evidence.py     # exit 0
grep -ic fabric site/evidence.json            # -> 78
python3 -c "import json;d=json.load(open('site/evidence.json'));print(len(d['artifacts']),len(d['figures']),len(d['cases']))"   # -> 41 13 5
```

The two manifests differ only by the fabric/verification content:

* artefact IDs present only in the tool output (18): `fabric-verification`, `fabric-law-source`, `fabric-material-source`, `fabric-verify-script`, `fe-verification-script`, `fe-fabric-probe`, `fe-fabric-probe-data`, `fe-fabric-mandel`, `fe-fabric-mandel-history`, `fe-fabric-mandel-peak`, `fe-fabric-contours`, `fe-fabric-contours-data`, `fe-fabric-diffusion`, `fe-fabric-diffusion-data`, `fabric-contours-script`, `fe-fabric-contour-deck`, `fe-verification-convergence`, `fe-reference-comparison`. Artefact IDs present only in the shipped file: **none**.
* figures registered: shipped 7 (conformal/isotropic only) vs tool 13 (adds `fe-fabric-probe`, `fe-fabric-mandel`, `fe-verification-convergence`, `fe-reference-comparison`, `fe-fabric-contours`, `fe-fabric-diffusion`).
* cases: shipped 3 vs tool 5.
* `site/scientific-snapshot.json`: shipped 45 files vs tool 47 (the tool adds `tools/rerun_fabric_decks.py`, `tools/rerun_fabric_contours.py`).

Consequences that bear on this review's remit:

1. **Unregistered published artifacts.** `site/README.md` states *"Add every public source, deck, plot, CSV, run report, PDF, supplement, and provenance file to `artifacts` … These entries are the publication allowlist."* Against that allowlist, 21 files under `figures/` and 1 report under `site/reports/` are unregistered:
   `figures/fe_fabric_probe.{csv,pdf,png}`, `fe_fabric_mandel.{pdf,png}`, `fe_fabric_mandel_history.csv`, `fe_fabric_mandel_peak.csv`, `fe_fabric_contours.{csv,pdf,png}`, `fe_fabric_diffusion.{csv,pdf,png}`, `fe_verification_convergence.{pdf,png}`, `fe_reference_comparison.{pdf,png}`, the three plot manifests, and `site/reports/fabric-verification.json`.
   (`python3 - <<'EOF'` comparing `os.walk('figures')` / `os.walk('site/reports')` against `evidence.json['artifacts']` paths.)
2. **The companion site does not publish the paper's headline evidence**, while the PDF-embedded supplement does (§2.5). Four of the six finite-element figures in the manuscript appear nowhere in the site gallery, and the companion site's `reproduction` block still lists only the conformal/isotropic commands.
3. **The site cannot be regenerated by the shipped pipeline**: the shipped `site/evidence.json`/`site/scientific-snapshot.json` are the output of `tools/populate_site_manifest.py`, which overwrites `artifacts`, `figures`, `cases`, `reproduction`, `limitations` and rewrites the scientific snapshot from its own globs — so if it runs after `register_fabric_evidence.py` it silently discards the fabric registration. The shipped manifest order therefore does not correspond to the documented tool chain.
4. Corroborating (runtime output, outside the frozen snapshot): the rebuilt site is also fabric-free — `grep -ic fabric .agent-runtime/site/evidence.json` → `0` and `grep -ic fabric .agent-runtime/site/index.html` → `0` (md5 `600d6971f246fc8fab7d3481c30347c0`, identical to the snapshot's `site/evidence.json`).

This does not alter any equation, number, or scientific claim, but it is a packaging/source-fidelity failure: a shipped tool does not reproduce the shipped artifact, published artifacts are unregistered, and the "regenerated" state asserted in the launch record is not present on disk.

**Required correction:** re-run the registration step so that `site/evidence.json` and `site/scientific-snapshot.json` match the output of the shipped `tools/register_fabric_evidence.py` (or otherwise reconcile the shipped manifests with the tool and with the manuscript), then rebuild the site and re-freeze.

### Finding 2 — OPTIONAL (documentation wording). A limitation in the shipped companion manifest is superseded by `sec:pore-fabric`.

`site/evidence.json` `limitations[2]` reads: *"The model describes mineral anisotropy; shape-changing distention and pore-shape anisotropy require additional constitutive mechanics."* The manuscript now **supplies** those mechanics in `sec:pore-fabric` / `sec:fe-fabric` (and the supplement ships them). As a companion statement for the same `…-v2` version that contains the fabric section, it reads as a contradiction with the paper. Note this string is also produced by `tools/register_fabric_evidence.py` (which *appends* its new limitation rather than replacing this one), so it is a wording issue independent of Finding 1: reword to scope it to the conformal specialization.

### Finding 3 — OPTIONAL (cosmetic). Legacy JSON key name in a shipped report.

`site/reports/fabric-verification.json` (and the identical `build/fabric/fabric-verification.json`) retains the key `H_eigenvalue_ratio_expected` under `tensor_checks`. Its *content* is correct (the expected \(h^{-2},h,h\) triple), and this round's stated requirement is satisfied: `grep -rin "eigenvalue ratio"` returns nothing anywhere in the repository, `grep -ic "eigenvalue ratio" site/evidence.json` → `0`, and `tools/register_fabric_evidence.py` no longer contains the phrase (its only "eigenvalue" occurrence, line 264, is the corrected *"…the logarithm of the unimodular transverse fabric eigenvalue."*). Renaming the key would remove the last trace of the retired wording.

### Checks that passed (recorded for completeness)

* R25-3-1 fix present: `sections/pore_fabric.tex` defines \(\mathbf m\) at first use in `sec:fabric-biot`.
* R25-3-2 fix present and correct: the claim attached to `eq:fabric-transverse-strain` reads "twice whose exponential, \(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G=a^{2/3}\mathbf H\), reconstructs \eqref{eq:fabric-transverse-h}, whose unimodular eigenvalues are \(h^{-2},h,h\)." — independently re-derived in §2.1.
* No statement about \(\ln h\), \(\mathbf H\), or the distention strain contradicts any equation; `validation/equation_to_moose_map.yml` and `validation/theory_traceability.yml` quote the same values (2.5e-16, 2.2e-16, 4.9e-15, 1.9e-14) as the report and the manuscript.
* No dangling references or citations; no overfull boxes; PDF/supplement byte-consistent.

---

## 4. Overall assessment

The science is in good shape. The snapshot re-hashes perfectly (591/591, declared ID confirmed), every quoted number in the manuscript reproduces from the frozen artifacts, the pore-fabric construction and its transverse-isotropic reduction are correct as written, the volume–axial distention modulus is genuinely the carrier of \(B_\parallel\neq B_\perp\) (with an isotropic mineral alone keeping \(\mathbf B\) spherical), the undrained/drained and Mandel results are self-consistent, and the PDF plus embedded supplement archive are internally consistent.

The blocking issue is packaging, not physics: the companion-site manifests shipped in this snapshot are not what the shipped registration tool produces, so the manuscript's new pore-fabric evidence is entirely unregistered in the publication allowlist, the site omits four of the paper's figures while the embedded supplement ships them, and the regeneration asserted for round 25 is not present on disk. That is a concrete, reproducible and correctable publication defect, so I cannot return an unconditional accept.

**Required corrections: 1** (Finding 1). Optional: 2.

VERDICT: MINOR REVISION
