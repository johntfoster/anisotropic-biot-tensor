# Round-13 independent review — reviewer 3 (prose, notation, significance, claim-vs-artifact)

## 1. Reviewed version, snapshot ID, integrity

- Live repository (not modified): `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
- Immutable reviewed snapshot: `.agent-runtime/review-snapshots/round-13` (read-only, mode 444/555)
- Manifest name: `source-manifest.json`; snapshot ID in `SNAPSHOT_ID`

```
$ cd <snapshot> && cat SNAPSHOT_ID
69a39ab45c1fbeed02118958391509d19d5c51fb2779cb278b366594ae38375c
$ sha256sum source-manifest.json
69a39ab45c1fbeed02118958391509d19d5c51fb2779cb278b366594ae38375c  source-manifest.json
```

`SNAPSHOT_ID` equals the SHA-256 of `source-manifest.json`. Every file listed in the
manifest was then hashed and compared:

```
$ python3 - <<'PY'   # hashes each manifest entry, compares to listed digest
...
PY
listed=340 ok=340 mismatch=0 missing=0
```

**Integrity result: PASS.** Snapshot ID matches the manifest digest; 340 listed,
340 ok, 0 mismatch, 0 missing. All audit statements below were made against this
frozen snapshot; the live tree was read only (no writes, no execution of the
verification suites or MOOSE).

Independent corroboration that the published evidence digests are live, not stale:

```
$ python3 -c "...compare site/evidence.json artifacts to files..."
evidence.json artifacts: total=21 ok=21 mismatch=0 missing=0
$ python3 -c "...compare site/scientific-snapshot.json to source-manifest.json..."
scientific-snapshot files: 33 inconsistent-with-manifest: []
$ python3 -c "...re-hash embedded build/conformal-2026-09-20-v1.zip against its manifest.json..."
version: conformal-2026-09-20-v1 | n hashed: 33
payload files=34 hashed_listed=33 ok=33 mismatch=0 listed-not-in-zip=0 in-zip-not-listed=0
```

## 2. Audit evidence (commands and literal outputs)

### 2a. The load-limit claim versus the recorded floor (charge a)

```
$ python3 -c "...dump linear_load_reference, nonlinear_load_* analysis.json..."
linear_load_reference : load 1e-4, linear=true, nx=20, dt=1e-3, pressure_max_normalized 0.003195724156060447
nonlinear_load_0.0001  : load 1e-4, linear=false, nx=20, dt=1e-3, pressure_max_normalized 0.003220919735602341
nonlinear_load_0.001   : load 1e-3, linear=false, nx=20, dt=1e-3, pressure_max_normalized 0.0034478714099894837
nonlinear_load_0.01    : load 1e-2, linear=false, nx=20, dt=1e-3, pressure_max_normalized 0.00570599193043681
```

`main.tex` (conclusions) states the floor explicitly and does **not** claim the
finite-deformation solutions reproduce the reference as the load vanishes:

```
$ sed -n '491,500p' main.tex
... A finite-element discretization of the coupled deformation and fluid-transport
balances reproduces the constant-coefficient consolidation reference in the
constant-tangent limit and satisfies a manufactured-solution convergence test
for that reference tangent; at finite load the nonlinear solutions approach
the reference as the load decreases, but their normalized discrepancy floors
at about \(3.2\times10^{-3}\) rather than decaying to it ...
```

The figure caption agrees, and is the strongest statement in the package:

```
$ python3 -c "...print plot-manifest figure caption for fe_load_limit..."
fe_load_limit | cases: ['nonlinear_load_0.0001','nonlinear_load_0.001','nonlinear_load_0.01']
caption: ... does not decay to the linear reference; it floors at about 3.2e-3
(a discretization floor), so this panel is a finite-load demonstration, not a
verified limit toward the linear solution.
```

Order of magnitude and direction of the measured sequence (5.71e-3 -> 3.45e-3 ->
3.22e-3 as load decreases 1e-2 -> 1e-3 -> 1e-4) match "approach ... but floored at
about 3.2e-3"; the linear constant-tangent run at the same nx=20, dt=1e-3 gives
3.196e-3, i.e. the floor is a discretization floor, as stated.

```
$ grep -rni "vanish|tends to zero|as the load|reproduce|decay" main.tex sections/*.tex site/evidence.json
sections/finite_elements.tex:167: problem as \(q_L/K\) tends to zero; they need not reproduce its series at a finite load.
```

No sentence in `main.tex` or `sections/*.tex` asserts that the finite-deformation
coupled solutions reproduce the constant-coefficient consolidation reference as
the load vanishes. The only "as the load tends to zero" wording is in
`site/evidence.json`, case 1, whose status is `pending` with empty `artifacts`
and the qualifier "Tolerances under review". **No overstatement found on charge (a).**

### 2b. Published ranges/numbers versus per-run analyses (charge b)

Claim in `site/evidence.json` (`finite_deformation`):

```
over the six rotated-anisotropy runs, pressure_max 0.75-0.86, platen 0.73-0.78,
edge displacement 1.61-1.78, and profile max 0.75-0.88
```

The six runs are `anisotropic_0/30/30_coarse/30_fine/45/90`. Measured
`analysis.json` values:

```
pressure_max_normalized : 0.7548557839(90) .. 0.8575201529(30_fine)   -> 0.75-0.86  OK
platen_max_normalized   : 0.7319829899(45) .. 0.7754134832(0)         -> 0.73-0.78  OK
edge_ux_max_normalized  : 1.6113823380(30_coarse) .. 1.7796212164(30_fine) -> 1.61-1.78 OK
profile_max_normalized  : 0.7549744337(90) .. 0.8750219313(30_fine)   -> 0.75-0.88  OK
```

`force_relative`, all anisotropic and partial runs:

```
anisotropic_0 4.0001e-12 | 30 2.1429e-12 | 30_coarse 1.2764e-10 | 30_fine 4.0715e-12
45 2.2856e-12 | 90 1.6430e-12
partial_0 5.8571e-12 | partial_30 2.0521e-10 | partial_30_coarse 2.4071e-11 | partial_30_fine 3.6714e-11
expected_force = -1.4 for load 0.7  (convention -2*a*q_L, full domain, a=1)  OK
```

Claim "force_relative of order 1e-10 or smaller" — the largest measured values are
1.276e-10 and 2.052e-10, i.e. slightly above 1e-10. See finding M1.

Other published numbers checked and confirmed:

```
site/reports/conformal-verification.json : checks_passed 186 ; legacy_identities_rechecked 67 ;
                                           max_constitutive_identity_error 2.4549890331732928e-09
sections/experiments.tex                 : "186 named checks" / "67 checks" / "2.5e-9"          OK
site/reports/tensor-verification.json    : materials 13 ; total_states 273
sections/experiments.tex                 : "273 finite states across 13 mineral stiffnesses"     OK
site/reports/fluid-coupling-verification.json : count 110 ; maximum_scaled_error 8.086725789002713e-09
site/evidence.json                       : "110 checks, max scaled error 8.09e-09"              OK
site/reports/mandel-reference.json       : n_checks 38 ; all passed True ;
                                           central_overshoot.ratio 1.0546586069998425 ;
                                           central_overshoot.time 0.015165352045764979
site/evidence.json                       : "38 self-checks (peak overshoot 5.4659% at t = 0.01516535)" OK
```

MMS convergence (site/evidence.json `convergence` vs `fe-evidence/mms-convergence.json`):

```
space.nx=4,8,16 ux naive_orders 2.9916668663 / 2.9584792405  -> "2.99/2.96"  OK
                uy naive_orders 2.9982612864 / 2.9599857747  -> "3.00/2.96"  OK
                p  naive_orders 1.9966292363 / 2.0008072999  -> "2.00/2.00"  OK
space configs [4,4,1e-4,0.01],[8,8,1e-4,0.01],[16,16,1e-4,0.01] -> "at dt=1e-4"  OK
time.nx16 difference_orders ux 1.0931948217, uy 0.9783037977, p 1.0151767156  -> "ux 1.093, uy 0.978, p 1.015" OK
time.nx64 difference_orders ux 1.3963663098, p 1.2519312797                   -> "nx=64 ux 1.40, p 1.25" OK
```

Independent re-derivation of the manuscript's finite-element parameters and the
anisotropic reference Biot numbers (my own arithmetic, not the repository's):

```
$ python3 (Mandel 6x6 C_s from eq:example-mineral-stiffness, phi_s0=0.6, K=7)
K_s = 28.0                       (manuscript: K_s = 28 K_*)                 OK
B0 diagonal = [0.7  0.758333 0.791667]
   (experiments.tex: "reference Biot components are 0.7000, 0.7583, 0.7917") OK
five deviatoric eigenvalues = [20, 24, 28, 42.966777, 53.033223]; mean/2 = 16.8
   (experiments.tex: isotropic comparison mu_s = 16.8 K_*)                  OK
Mandel reference parameters (site/reports/mandel-reference.json): K=1.0, G=0.75, alpha=0.6,
mobility=1.5, a=1, b=0.1  vs  finite_elements.tex: phi_s0=0.9, K_s=2.5, mu_s=5/6, K=1,
K_f=8, rho_f0=1, k/mu_f=1.5, G=0.75, Biot 0.6, storage 17/80
   storage check: (1-0.9)/8 + (0.9/2.5)(1-1/(0.9*2.5)) = 0.0125 + 0.2 = 0.2125 = 17/80   OK
   M = 1/0.2125 = 4.70588 matches mandel-reference M                                     OK
```

### 2c. Code/data availability statement (charge c)

Manuscript statement (`sections/experiments.tex`):

```
... the coupled finite-element implementation of section~\ref{sec:finite-elements}
is not part of that archive: ... recorded separately in the document repository
\url{https://github.com/johntfoster/anisotropic-biot-tensor}: the application
sources under \nolinkurl{moose_app/}, the independent reference and validation
scripts under \nolinkurl{validation/}, the deck inputs and per-run analyses
under the implementation runtime directory, figure data under
\nolinkurl{figures/}, and the verification-evidence file at
\nolinkurl{site/evidence.json}, which records the inspected source revision.
```

Resolvability checks:

```
$ grep -rn "runs_dir" fe-evidence/mms-convergence.json
"runs_dir": ".../.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs"
$ grep -n "runs" examples/plot_fe_results.py | tail -2
373: ... default=ROOT / '.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs'
374: ... default=ROOT / '.agent-runtime/moose-fe-goal-2026-09-20/plots'
$ ls <live repo>/.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs | wc -l
38
```

The manifest's `provenance.source_revision` is resolvable, and the archive's claim
about its own manifest is accurate:

```
$ cat site/evidence.json | grep source_revision
"source_revision": "ecfe4a22a094d3b346ea89287f9a23e1917f017c"
$ cd <live repo> && git cat-file -t ecfe4a22a094d3b346ea89287f9a23e1917f017c
commit
$ python3 -c "...print zip README head..."
# Numerical supplement: conformal-2026-09-20-v1
Extract the archive, then run from its root ... python3 examples/verify_reconstruction.py ...
```

But the runtime location the statement alludes to is hidden and untracked, and the
other named roots are not tracked at the cited revision:

```
$ cat <live repo>/.gitignore
/build/
/.agent-runtime/
...
$ cd <live repo> && git ls-files | wc -l
85
$ for p in fe-evidence figures site moose_app validation .agent-runtime; do
    printf "%-16s tracked-count=" "$p"; git ls-files "$p" | wc -l; done
fe-evidence      tracked-count=0
figures          tracked-count=0
site             tracked-count=0
moose_app        tracked-count=0
validation       tracked-count=0
.agent-runtime   tracked-count=0
$ git status --short | head
 M main.tex
 M references.bib
 M sections/experiments.tex
?? figures/
?? moose_app/
...
```

Note (limitation): the live checkout may be ahead of the eventual commit that is
published; this check reflects the state I could inspect, and the frozen snapshot
itself does contain `moose_app/`, `validation/`, `figures/`, `site/` and the run
analyses under `fe-evidence/runs/`. The statement nevertheless never names
`fe-evidence/` and gives no repository-relative path for the run data.

### 2d. Notation (charge d)

```
$ grep -rn "widehat|\\\\hat" main.tex sections/*.tex
main.tex:176 \(\widehat{\mathbf\sigma}_s\) ... intrinsic mineral Cauchy stress
main.tex:181  =\mathbf R_A\widehat{\mathbf\sigma}_s\mathbf R_A^T.
main.tex:211  \widehat{\mathbf\tau}_s
main.tex:214  =\mathbf R_A\widehat{\mathbf\tau}_s\mathbf R_A^T.
main.tex:275  +\phi_{s0}\widehat{\mathbf\tau}_s:
sections/logarithmic_derivative.tex:24 ... \(\widehat{\mathbf\tau}_s\) in the true-deformation frame.
```

The hat is used only for the true-frame mineral stress, matching the stated
convention in `main.tex` lines 156-160. Using the independently checked relations
(`J phi_s = phi_{s0} \bar J`, `tau' = J sigma'`, `bar tau_s = bar J bar sigma_s`)
the mixed bar/hat convention in eqs. (constitutive-kirchhoff-phase-stress),
(rotated-mineral-kirchhoff) and (total-stress-phase-energy) is self-consistent.
One tension: the convention says a bar on an intrinsic-density quantity "denotes
the mineral state reached by removing the distention", yet `sections/finite_elements.tex`
writes the fluid intrinsic density as `\bar\rho_f` / `\bar\rho_{f0}`. See M4.
The reference-versus-current-volume convention is stated explicitly and correctly
(`sections/finite_elements.tex` lines 38-41; `sections/stress_reconstruction.tex`
line 48).

### 2e. Citations (charge e)

```
$ <python: extract all \cite... braces across main.tex, sections/*.tex> 
used 22 ; defined 22
USED-NOT-DEFINED: []
DEFINED-NOT-USED: []
total cite occurrences (incl duplicates): 27
```

Every `\cite`/`\citep`/`\citet` key resolves in `references.bib`, and there is no
uncited bibliography entry. (A first naive line-based grep missed the two-line
`\citep{dehghanipentamerodio2019,\n dehghanizilian2021}`; the balanced-brace
extraction above is authoritative.) All 50 `\eqref`/`\ref`/`\cref` targets resolve
to a defined `\label` (`REFS WITH NO LABEL: []`).

### 2f. Abstract/introduction/keywords/conclusions scope consistency (charge f)

- Abstract: "verified against a manufactured solution and exercised on
  rotated-anisotropy and partial-drainage demonstrations at finite load; no
  quantitative finite-deformation verification and no experimental validation is
  claimed" — matches the scope paragraph in `sections/finite_elements.tex`
  ("implementation verification ... demonstrations ... not a quantitative
  verification of the nonlinear finite-deformation law ... not experimental
  validation: all parameters are synthetic") and `site/evidence.json`
  (`finite_deformation: pending`, `physical_validation: not_performed`).
- Keywords include "finite-element verification", consistent with the MMS plus
  constant-tangent reference verification.
- The abstract omits the constant-tangent consolidation-reference verification
  that the introduction and conclusions claim (see M3).

## 3. Findings

| # | Severity | Finding |
|---|----------|---------|
| R1 | Required (correctness of published claim) | `site/evidence.json` `implementation` summary asserts "The C++ law matches the independent Python evaluation to about 6e-14 over 41 finite states." No listed evidence artifact records a 41-state C++-versus-Python comparison or a 6e-14 error. |
| R2 | Required (reproducibility) | The availability statement points readers to "the implementation runtime directory" for deck inputs and per-run analyses; no repository-relative path is given, and the resolvable location is the git-ignored `.agent-runtime/...` tree. The other named roots (`moose_app/`, `validation/`, `figures/`, `site/`) are untracked at the cited revision in the checkout I inspected. |
| M1 | Minor | "force_relative of order 1e-10 or smaller" is slightly exceeded (1.276e-10 and 2.052e-10). |
| M2 | Minor | "the six rotated-anisotropy runs" includes `anisotropic_0` (zero rotation). |
| M3 | Minor | Abstract omits the constant-tangent consolidation-reference check; the introduction's "in the constant-tangent limit, the constant-coefficient consolidation reference" is compressed and can be misread. |
| M4 | Minor | `\bar\rho_f` / `\bar\rho_{f0}` (fluid intrinsic density) is not covered by the stated bar convention (mineral-state bar). |
| M5 | Minor (non-published) | `site/README.md` still describes `site/evidence.json` as "the complete pending example" / "The initial manifest records pending work", which no longer matches the manifest's passed categories. `site/README.md` is not in the artifact allowlist, so it is not published on the built site. |

### Evidence for R1

```
$ grep -rn "6e-14|41 finite|finite states" site/ fe-evidence/ provenance/ tools/ (non-CSV)
site/evidence.json:21: ... "The C++ law matches the independent Python evaluation to about 6e-14 over 41 finite states.",
tools/populate_site_manifest.py:137: 'Python evaluation to about 6e-14 over 41 finite states.',
$ grep -rn "\b41\b" site/ tools/ moose_app/scripts/ examples/ validation/   # counts only
site/evidence.json:21  ...  (the only "41" as a count)
tools/populate_site_manifest.py:137
$ grep -rn "finite states" . (non-CSV)
site/evidence.json, sections/experiments.tex, examples/verify_conformal.py, tools/populate_site_manifest.py
$ sed -n '116,120p' examples/verify_conformal.py
finite_states = [(I, 0.), (1.1*I, 2.), (np.diag([1.1, 1.1, .9]), .5),
                 (np.diag([1.1, 1.1+1e-11, .9]), .5),
                 (shear_gradient(.65), 2.), (shear_gradient(-.8), 6.)]   # 6 states x 2 materials
```

The four evidence artifacts listed for the `implementation` category record
110 checks / 8.09e-09 (fluid), 186 checks / 2.45e-09 max identity error
(conformal), 273 states (tensor), and reconstruction errors (reconstruction).
None records "41 finite states" or a 6e-14 C++-versus-Python agreement. The string
is a hardcoded literal in the site-manifest builder, so the manifest cannot be
regenerated from the artifacts and the number cannot be traced.

### Evidence for R2

```
$ grep -rn "runs_dir" fe-evidence/mms-convergence.json
"runs_dir": ".../.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs"
$ cd <live repo> && grep -n agent-runtime .gitignore
/.agent-runtime/
$ cd <live repo> && git ls-files moose_app figures site validation fe-evidence | wc -l
0
```

## 4. Required corrections

**R1 — Remove or substantiate the "6e-14 over 41 finite states" claim in
`site/evidence.json` (`implementation` category; source string in
`tools/populate_site_manifest.py`).**
*Why required:* it is a published quantitative number whose supporting artifact is
not among the artifacts the same manifest cites (and does not exist anywhere in the
snapshot). A reader cannot reproduce or trace it, and the surrounding numbers
(110/8.09e-09, 186 checks/2.5e-9, 273 states) all trace to artifacts, so this one
undermines the auditability of the manifest. Either add the artifact that records
the comparison (with the correct state count and error) or delete the sentence.

**R2 — Make the code/data availability statement resolvable: replace "the
implementation runtime directory" with an explicit repository-relative path (or
publish the run decks and per-run analyses at a tracked path and name it), and
verify the named roots are actually present at the inspected revision.**
*Why required:* the statement's purpose is reproducibility of the coupled
finite-element results; as written it cannot be followed to the deck inputs and
per-run analyses (the only resolvable location is the git-ignored runtime tree),
and the other roots it names are not tracked at the revision recorded in
`site/evidence.json`. Callers told the evidence is "recorded separately" in the
public repository will not find it there.

## 5. Optional suggestions

1. Qualify "reproduces the constant-coefficient consolidation reference in the
   constant-tangent limit" with the recorded tolerance
   (`pressure_max_normalized` 3.2e-3; profile error 1.3e-2 after t>=0.01;
   best refined pressure error ~4.6e-4 at nx=20), e.g. "reproduces ... to within
   the recorded discretization error". The neighbouring clause already reports the
   3.2e-3 floor, so the bare verb "reproduces" reads stronger than the numbers.
2. `site/evidence.json` `convergence`: mention the nx=32 temporal value
   (ux 1.397) alongside "nx=64 ux 1.40"; nx=32 is equally a "finer mesh" value.
3. `site/evidence.json` `analytical` category cites only `mandel-reference`, while
   its summary also states a finite-load floor. Add the load-limit figure/data
   artifact IDs to that category's `evidence` so every published number is
   traceable to a listed artifact.
4. Reword "the six rotated-anisotropy runs" to name the orientation set
   (0/30/30-coarse/30-fine/45/90 degrees) for the zero-rotation entry.
5. Extend the bar/hat convention sentence to cover intrinsic *fluid* density, or
   use a distinct symbol for `\bar\rho_f`, so the convention has no exceptions.
6. Refresh `site/README.md`'s "pending example" description of
   `site/evidence.json`.

## 6. Verdict rationale

Reviewed against the frozen round-13 snapshot. Integrity is clean (340/340). I
independently reproduced: the load-limit floor narrative against the per-run
`analysis.json` files (no overstatement of the load-vanishing limit found); all
published ranges and order counts for the exact run sets named in
`site/evidence.json` (six anisotropic runs and four partial runs match exactly);
the MMS spatial and temporal orders; the Mandel reference self-check count, peak
overshoot and time; the constitutive-suite counts (186/67/2.5e-9, 273 states/13
materials, 110/8.09e-09); the finite-element parameter set and the storage value
17/80; and the anisotropic reference Biot components 0.7000/0.7583/0.7917 and the
isotropic comparison shear modulus 16.8 by direct computation. Citation and label
resolution are complete. The two required corrections are confined to the evidence
manifest's reproducibility/availability text; no numerical or constitutive error
was found in the checked claims.

Limitations: I could not and did not render the PDF or any figure (no LaTeX
rendering, no image inspection); I verified figure data by digest only. I did not
re-run MOOSE or the Python verification suites; all quantitative checks were
either read from the frozen evidence files or re-derived analytically.

VERDICT: MINOR REVISION
