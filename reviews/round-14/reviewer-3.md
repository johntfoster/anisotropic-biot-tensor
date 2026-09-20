# Round-14 Review — Reviewer 3
## Prose, notation, significance, and claim-versus-artifact consistency

---

## 1. Reviewed version, snapshot ID, integrity result

- Repository: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
- Frozen snapshot: `.agent-runtime/review-snapshots/round-14` (read-only, modes 444/555)
- SNAPSHOT_ID (expected): `061a92feee93641668978ab0ecec033d0b9fe0d20ad74efbcb9ec0bf1a60ea69`
- `sha256sum <snapshot>/source-manifest.json`:
  `061a92feee93641668978ab0ecec033d0b9fe0d20ad74efbcb9ec0bf1a60ea69` → **matches SNAPSHOT_ID: PASS**
- Full manifest re-hash result: **listed=441, ok=441, mismatch=0, missing=0 → INTEGRITY PASS**
- All audit work was performed on a `/tmp` copy (`cp -r` + `chmod -R u+w`); the snapshot was not modified.

Subsidiary integrity checks performed (all PASS):
- `fe-evidence/manifest.json`: listed=206, ok=206 (sha256 + byte length), mismatch=0, missing=0.
- `site/evidence.json` `artifacts[]`: 22/22 paths exist and 22/22 sha256 match.
- Embedded supplement `build/conformal-2026-09-20-v1.zip` → `manifest.json`: 33/33 listed payload hashes match, no unlisted entries.
- `site/scientific-snapshot.json`: 33/33 listed hashes match.

---

## 2. Audit evidence (literal commands and outputs)

All commands run from a writable copy: `cp -r <snapshot> /tmp/r14r3/snap && chmod -R u+w /tmp/r14r3/snap`.

**2.1 Snapshot integrity**

```
$ sha256sum .agent-runtime/review-snapshots/round-14/source-manifest.json
061a92feee93641668978ab0ecec033d0b9fe0d20ad74efbcb9ec0bf1a60ea69  .../source-manifest.json
$ python3  # hash every manifest-listed file
listed=441 ok=441 mismatch=0 missing=0
```

**2.2 Evidence-manifest artifact resolution and hashes**

```
$ python3  # for each site/evidence.json artifacts[] entry: exists + sha256
OK fe-mandel-history ... OK scientific-snapshot
bad: 0
=== evidence ids referenced by categories ===
analytical: mandel-reference -> RESOLVES
analytical: fe-load-limit-data -> RESOLVES
implementation: fluid-coupling-verification -> RESOLVES
implementation: conformal-verification -> RESOLVES
implementation: tensor-verification -> RESOLVES
implementation: reconstruction-verification -> RESOLVES
implementation: cpp-python-constitutive -> RESOLVES
convergence: mms-convergence -> RESOLVES
```
Note: `finite_deformation` and `physical_validation` reference no evidence ids; all three `cases[].artifacts` arrays are empty (see §3, F4).

**2.3 Recomputation of every quantitative claim in `site/evidence.json`**

`analytical`:
```
$ python3 -c "import json;d=json.load(open('site/reports/mandel-reference.json'));
              print(len(d['verification']['checks']), d['verification']['checks']['central_overshoot'])"
38 {'ratio': 1.0546586069998425, 'time': 0.015165352045764979, 'passed': True}
```
→ "38 self-checks", "peak overshoot 5.4659%", "t = 0.01516535" all reproduced (ratio−1 = 5.4659 %).

```
$ cat figures/fe_load_limit.csv
nonlinear_load_0.0001,0.0001,20,0.001,pressure_max_normalized,0.003220919735602341
nonlinear_load_0.001,0.001,20,0.001,pressure_max_normalized,0.0034478714099894837
nonlinear_load_0.01,0.01,20,0.001,pressure_max_normalized,0.00570599193043681
$ python3 ... site/reports/... # linear_load_reference/analysis.json
pressure_max_normalized = 0.003195724156060447
```
→ "normalized pressure discrepancy floors at about 3.2e-3 (a discretization floor at nx=20, dt=1e-3) rather than decaying to the linear reference as the load tends to 1e-4": the sweep spans load = 0.01, 0.001, 0.0001 at nx=20, dt=1e-3; the 1e-4 case is 3.2209e-3 and the linear reference itself is 3.1957e-3 → **verified**.

`implementation`:
```
$ python3 -c "...fluid-coupling-verification.json..."
count = 110   maximum_scaled_error = 8.086725789002713e-09
$ python3 -c "...cpp-python-constitutive.json..."
states = 41   value_absolute_error = 6.394884621840902e-14
$ python3 -c "...conformal-verification.json..."
checks_passed = 186   legacy_identities_rechecked = 67   max_constitutive_identity_error = 2.4549890331732928e-09
$ python3 -c "...tensor-verification.json..."
total_states = 273   materials = 13
```
→ "110 checks, max scaled error 8.09e-09", "6.4e-14 over 41 finite states", "186 named checks, including the 67 checks", "largest absolute error … 2.5×10⁻⁹", "273 finite states across 13 mineral stiffnesses" all reproduced.

`convergence` (recomputed independently from `fe-evidence/runs/*/analysis.json`):

```
spatial nx=4,8,16 at dt=1e-4
  ux 2.9917/2.9585  -> paper "2.99/2.96"   OK
  uy 2.9983/2.9600  -> paper "3.00/2.96"   OK
  p  1.9966/2.0008  -> paper "2.00/2.00"   OK
temporal (successive differences of L2 norms, fixed mesh)
  nx=16: ux 1.0932, uy 0.9783, p 1.0152  -> "1.093, 0.978, 1.015"   OK
  nx=32: ux 1.3969, uy 1.0183, p 1.1252  -> "1.397, 1.018, 1.125"   OK
  nx=64: ux 1.3964, uy 1.0762, p 1.2519  -> "1.396, 1.076, 1.252"   OK
```
→ all 15 reported orders reproduce to the printed precision; `diff fe-evidence/mms-convergence.json site/reports/mms-convergence.json` → IDENTICAL.

`finite_deformation` (recomputed ranges over the six anisotropic runs):
```
pressure_max_normalized : 0.75486 … 0.85752   -> "0.75-0.86"   OK
platen_max_normalized   : 0.73198 … 0.77541   -> "0.73-0.78"   OK
edge_ux_max_normalized  : 1.61138 … 1.77962   -> "1.61-1.78"   OK
profile_max_normalized  : 0.75497 … 0.87502   -> "0.75-0.88"   OK
max force_relative over demonstration runs = 2.0521425828487087e-10 (partial_30) -> "at most about 2.1e-10 … largest measured 2.052e-10, partial_30"  OK
```
Geometry claims checked in the decks:
```
$ grep -A8 '\[base\]' fe-evidence/runs/anisotropic_0/input.i
nx=16 ny=4 xmin=-1 xmax=1 ymin=-0.1 ymax=0.1   -> "slender domain [-1,1]x[-0.1,0.1]"  OK
$ grep -A8 '\[base\]' fe-evidence/runs/partial_0/input.i
nx=12 ny=12 xmin=-1 xmax=1 ymin=-1 ymax=1       -> "square domain [-1,1]x[-1,1]"       OK
$ python3 -c "...partial_0/analysis.json..." -> reference_comparable = false  OK
```

**2.4 Manuscript numeric claims traced**

```
build/conformal/experiments.json:
  phi_s0=0.6, K=7.0, Ks=28.0, isotropic_comparison/mu=16.8
  highlights/reference_B = [0.7, 0.7583333333333333, 0.7916666666666667]
  loading: pressure 121 pts; shear 161 pts; directional 1-deg; rotation 121 pts 0..180 deg; layer 121 pts
  solid_fraction_range = [0.4343, 0.6]
  check of "mean of the five deviatoric stiffness modes / 2":
     dev projector on C_s gives eigenvalues {20,24,28} + two normal modes summing to
     trace(N) - (1/3) m:N m = 180 - 252/3 = 96  -> (96+72)/5 = 33.6 -> /2 = 16.8   OK
  K_s = (50+60+70+2*(12+10+14))/9 = 252/9 = 28                               OK
mandel-reference.json: K=1.0, G=0.75, alpha=0.6, mobility=1.5, a=1.0, b=0.1
  -> FE section "phi_s0=0.9, K_s=2.5, mu_s=5/6, K=1, K_f=8, k/mu_f=1.5, G=0.75, alpha=0.6"
  total storage (1-phi)/K_f + S_s = 0.1/8 + 0.9/2.5*(1-1/2.25) = 0.2125 = 17/80   OK
fe-evidence/runs/mms_space_4/input.i: angle=30, U=P0=0.01, dt=1e-4, end=0.01        OK
build/conformal/*.csv row counts: 242 = 2x121; 322 = 2x161; 1083 = 3x361; 242; 242; 5  OK
```

**2.5 Citation and cross-reference resolution**

```
cited keys: 22 ; CITED-NOT-IN-BIB: [] ; IN-BIB-NOT-CITED: []
labels: 106 ; refs: 33 ; REFS-WITHOUT-LABEL: []
includegraphics: all 5 build/conformal/*.pdf EXIST
\input: sections/{stress_reconstruction,limits,experiments,finite_elements,logarithmic_derivative}
        and provenance/ai_use_statement.tex all EXIST
```
The companion reference resolves as an `@unpublished` entry carrying both the public URL
(`github.com/johntfoster/finite-strain-biot-poromechanics`) and the inspected commit `223901199e33`,
matching the prose claim in the availability paragraph. Repository remote is
`git@github.com:johntfoster/anisotropic-biot-tensor.git` and HEAD is `ecfe4a2`, matching the
`source_revision` `ecfe4a22a094d3b346ea89287f9a23e1917f017c` recorded in `site/evidence.json`.

**2.6 Notation scan**

```
$ python3  # every \bar{...} argument in main.tex + sections/*.tex
 23 \mathbf F   9 \mathbf\tau   9 \mathbf\varepsilon   5 \mathbf\sigma
  3 \mathbf U   2 \mathbf C     (all mineral-state) ; \bar J (mineral volume)
 16 \bar\rho (intrinsic densities) ; \bar W_s (mineral energy) ; 3 \bar Q_f
```
`\widehat{...}` appears only as the true-frame stress `\widehat{\mathbf\sigma}_s`, `\widehat{\mathbf\tau}_s` — consistent with the stated convention.

**2.7 Scope wording**

`site/evidence.json` statuses: analytical `passed`, implementation `passed`, convergence `passed`,
finite_deformation `pending`, physical_validation `not_performed`. The manuscript matches this
grading: abstract "...at finite load; no quantitative finite-deformation verification and no
experimental validation is claimed for those demonstrations"; FE scope paragraph "implementation
verification ... and ... demonstrations ... not a quantitative verification of the nonlinear
finite-deformation law, and ... not experimental validation".

---

## 3. Findings with severity

**F1 — Availability paragraph overstates per-case directory contents. Severity: MEDIUM-LOW (prose vs artifact).**
`sections/experiments.tex` (availability paragraph) states: "the deck inputs and per-run analyses
under `fe-evidence/runs/` (each case directory holds its input deck, run provenance, per-run
analysis, and scalar history)". Three directories listed as cases in `fe-evidence/manifest.json`
(`jacobian_0.0001`, `jacobian_1e-05`, `jacobian_1e-06`) contain only `input.i`,
`provenance.json`, `run.log`, `solution.csv` — there is **no `analysis.json`**.
```
$ ls -1 fe-evidence/runs/jacobian_0.0001
input.i
provenance.json
run.log
solution.csv
```
The same overstatement is repeated in `fe-evidence/README.md` ("Each `runs/<case>/` holds the deck
(`input.i`), the recorded provenance (`provenance.json`), the per-run analysis (`analysis.json`),
the scalar history (`solution.csv`), …").

**F2 — Bar notation used outside its stated convention. Severity: LOW (notation).**
Section 2 defines: "a bar on a kinematic, energetic, or intrinsic-density quantity denotes the
mineral state …; a bar on a stress denotes its representation in the mixture frame". The FE section
then uses `\bar Q_f` (3 occurrences) for the **prescribed outward referential mass flux** on
`Γ_Q` and `\bar\rho_f`, `\bar\rho_{f0}` for the **fluid** intrinsic density. Neither is a mineral
state nor a stress representation; `\bar Q_f` is not covered by the convention at all.

**F3 — Roadmap/abstract omit the constant-tangent restriction on the manufactured-solution check. Severity: LOW (scope wording).**
`sections/finite_elements.tex` states the manufactured solution "checks off-axis coupling in the
constant reference tangent. … it does not by itself verify the nonlinear constitutive law", and the
scope paragraph calls the coupled work "an implementation verification of the weak balances and of
the constant reference tangent". The introduction nevertheless reads "verify the implementation
against a manufactured solution and, in the constant-tangent limit, the constant-coefficient
consolidation reference", attaching the restriction only to the second item; the abstract likewise
says the implementation "is verified against a manufactured solution" without the tangent qualifier.
The conclusions are precise ("... satisfies a manufactured-solution convergence test **for that
reference tangent**").

**F4 — The evidence manifest contains quantitative claims in categories/cases with no listed artifact. Severity: LOW (traceability).**
`site/evidence.json` `categories.finite_deformation` quotes numeric ranges (pressure_max 0.75–0.86,
platen 0.73–0.78, edge displacement 1.61–1.78, profile max 0.75–0.88, force_relative ≤ 2.052e-10)
but supplies `"evidence": []`, and all three `cases[]` entries have `"artifacts": []`. The numbers
are reproducible from `fe-evidence/runs/*/analysis.json` (hashed inside `fe-evidence/manifest.json`),
but `site/evidence.json` names no artifact for them, so the manifest's own artifact→claim chain is
broken for that category.

**F5 — Characterization of the 67 checks is slightly over-inclusive. Severity: LOW (characterization).**
`sections/experiments.tex`: "the 67 checks of rotation, virtual work, and volume response used to
establish the specialization". The 67 `legacy_*` checks are 5 states × 13 per-state identities,
plus `legacy_reference_biot` and `legacy_reference_rank_one_compliance_identity`, which are
reference relations rather than rotation/virtual-work/volume-response checks.

**F6 — The 3.2e-3 floor is quoted without naming the metric. Severity: OPTIONAL (precision).**
Conclusions: "their normalized discrepancy floors at about 3.2×10⁻³". `site/evidence.json` names it
precisely ("its normalized **pressure** discrepancy … at nx=20, dt=1e-3"); the manuscript does not.

No finding contradicts a shipped number: every quantitative claim audited (38/5.4659 %/0.01516535;
110/8.09e-9; 41/6.4e-14; 186/67/2.5e-9; 273/13; all 15 MMS orders; 0.7000/0.7583/0.7917; K_s=28;
μ_s=16.8; 121/161/121/361 samples; 17/80; 3.2e-3; 2.052e-10; the anisotropic and partial ranges)
was independently recomputed and matches its listed artifact.

---

## 4. Required corrections

1. **(F1)** Amend the availability sentence so it is true of the shipped tree, e.g. "each
   coupled-analysis case directory holds its input deck, run provenance, per-run analysis, and
   scalar history (the Jacobian-check decks carry only their input deck, provenance, solver log,
   and scalar history)", and align `fe-evidence/README.md`. *Why required:* the present wording is a
   published, checkable statement that is false for 3 of the 38 case directories listed in
   `fe-evidence/manifest.json`; a reader verifying the availability claim will hit a
   contract-versus-artifact mismatch.
2. **(F2)** Extend the notation convention in Section 2 to cover the referential mass-flux bar
   (e.g. "a bar on a mass-flux measure denotes its referential normalization; on an intrinsic
   density it denotes the per-phase-volume value"), or rename `\bar Q_f`. *Why required:* Section 2
   presents the bar/hat convention as exhaustive ("Throughout, …"), and `\bar Q_f` is an
   unexplained exception in the same manuscript, which invites misreading of the fluid-flux
   normalization.
3. **(F3)** Add the constant-tangent qualifier to the manufactured-solution check in the
   introduction roadmap (and, preferably, the abstract), as the conclusions already do. *Why
   required:* the paper's own FE section restricts the manufactured-solution test to the constant
   reference tangent and explicitly denies that it verifies the nonlinear constitutive law; the
   roadmap as written implies a broader implementation-verification scope than the artifact
   supports.
4. **(F4)** List the finite-deformation evidence in `site/evidence.json` — at minimum add
   `fe-evidence/manifest.json` (or the individual `fe-evidence/runs/<case>/analysis.json` files)
   to `artifacts[]` and reference it from `categories.finite_deformation.evidence` and the three
   `cases[].artifacts`. *Why required:* the manifest states quantitative ranges that the audit
   charge requires to be traceable to a listed artifact with a resolvable hash; as shipped, the
   `finite_deformation` category and its cases point at no artifact.

---

## 5. Optional suggestions

- **(F5)** Rephrase to "the 67 per-state identities, two of which are the reference Biot and
  rank-one compliance relations", or state 65 rotation/virtual-work/volume checks plus 2 reference
  checks, so the count characterization matches the check names.
- **(F6)** Name the metric and mesh in the conclusions, e.g. "the maximum normalized pressure
  discrepancy floors at about 3.2×10⁻³ at nx=20, dt=10⁻³".
- The site title `"An anisotropic Biot tensor: finite-element verification"` and the keyword
  "finite-element verification" are broader than the verified scope (constant-reference-tangent
  implementation verification plus finite-load demonstrations); consider "finite-element
  implementation verification" in both.
- `site/evidence.json` `analytical` carries status `passed` while `cases[0]` ("Small-load isotropic
  Mandel consolidation") is `pending` with "Tolerances under review"; consider stating in the
  `analytical` summary that the category passes while the finite-load case remains a demonstration,
  so the two statuses read consistently.
- `\bar\rho_f` / `\bar\rho_{f0}` for the fluid are defensible under an "intrinsic density" reading
  but sit next to the mineral-specific wording; a one-clause clarification (as in the F2 fix) would
  remove the ambiguity.

---

## 6. Verdict rationale

Integrity passed end-to-end: the frozen manifest hash equals SNAPSHOT_ID, all 441 listed files
re-hash correctly, and the subsidiary manifests (`fe-evidence/manifest.json` 206/206,
`site/evidence.json` 22/22, archive 33/33, `site/scientific-snapshot.json` 33/33) all verify.

On the charge, the package is in strong shape: every published number I could recompute matches a
listed artifact (constitutive suite, fluid-coupling suite, spherical-gauge and reconstruction
suites, all 15 manufactured-solution orders, the Mandel reference statistics, the Biot components,
the anisotropic/partial demonstration ranges, and the equilibrium residuals). Citations and
cross-references all resolve; the availability paragraph's named paths all exist; the scope grading
(implementation verification vs finite-load demonstrations vs physical validation) is consistent
between the abstract, the FE section, the conclusions, and `site/evidence.json`.

The corrections I require are real but bounded and non-scientific: one availability sentence that
is false for three case directories (F1), one unexplained notation exception to an explicitly
"throughout" convention (F2), one scope qualifier present in the FE section and conclusions but
absent from the roadmap/abstract (F3), and one evidence category whose quantitative ranges are not
attached to any listed artifact (F4). None of these changes a physical claim, an equation, or a
verified number; all are prose/notation/traceability defects of the kind this review is charged to
find. Because at least one required correction exists, ACCEPT is not available; because no
numerical claim, derivation, or scope claim is overstated at the level of the method or results,
REJECT and MAJOR REVISION are not warranted.

VERDICT: MINOR REVISION
