# Round-13 Independent Review — Reviewer 2 (physics/source fidelity and packaging completeness)

Reviewer identity: independent reviewer 2 of 3. I did not author this material and
did not read any other reviewer's report or any prior-round file under `reviews/`.

## 1. Reviewed version, snapshot ID, integrity result

- Reviewed artifact: frozen snapshot
  `.agent-runtime/review-snapshots/round-13/` of
  `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`.
- Snapshot ID (`cat SNAPSHOT_ID`): `69a39ab45c1fbeed02118958391509d19d5c51fb2779cb278b366594ae38375c`
- `sha256sum source-manifest.json`:
  `69a39ab45c1fbeed02118958391509d19d5c51fb2779cb278b366594ae38375c  source-manifest.json`
  → matches the SNAPSHOT_ID value exactly.
- Manifest file-hash verification (every entry in `source-manifest.json` re-hashed):

```
$ sha256sum source-manifest.json
69a39ab45c1fbeed02118958391509d19d5c51fb2779cb278b366594ae38375c  source-manifest.json
$ python3 (hash every listed file)
listed/ok/mismatch/missing: 340 340 0 0
extra files not in manifest: 2
EXTRA SNAPSHOT_ID
EXTRA source-manifest.json
```

**Integrity result: PASS.** 340 listed / 340 ok / 0 mismatch / 0 missing. The only
files present but unlisted are `SNAPSHOT_ID` and `source-manifest.json` themselves,
which is expected. All review work was performed against this frozen snapshot;
scratch output was written only under `/tmp/r13r2` (`/tmp` copy of the tree was
made with `cp -r` and `chmod -R u+w`, never touching the read-only snapshot).

Review limitations (stated up front):
- No MOOSE binary or built application is present in the snapshot, so I could not
  re-run the finite-element decks. The FE runs were audited from their recorded
  `provenance.json` / `analysis.json` / `solution.csv` artifacts, plus independent
  reproduction of the Python constitutive, reference, and post-processing suites.
- The Git commit recorded in `site/evidence.json` (`source_revision`) cannot be
  verified because no `.git` history is inside the snapshot.
- PDF/plot byte-reproduction was not attempted (platform PDF metadata differs by
  design, per the supplement README).

## 2. Independent verification evidence (literal commands and outputs)

### 2.a Constitutive and coupling fidelity (charge a)

Read the implementation: `moose_app/include/utils/Con formalLaw.h`,
`moose_app/src/kernels/ReferenceBalance.C`,
`moose_app/src/materials/ConformalMaterial.C`, `moose_app/src/main.C`,
`moose_app/src/postprocessors/*.C`.

Key source lines (verified against the manuscript equations):

- Total Cauchy stress (eq. `total-stress-phase-energy`,
  `σ = (φ_s0/J) τ̄_s − (1−φ_s) p I`) :
  `s.sigma=phi/s.J*tau-I*((1-s.solid)*p);`
- Total first Piola (eq. `fe-total-first-piola`, `P = J σ F^{-T}`) and the
  momentum kernel using it directly, with no drained/pB correction:
  `s.P=s.J*s.sigma*F.inverse().transpose();`
  `ReferenceMomentum::computeQpResidual(){ADReal r=0;for(unsigned j=0;j<3;++j)r+=_grad_test[_i][_qp](j)*_P[_qp](_component,j);return r;}`
- Fluid EOS (eq. `fe-fluid-eos`, `ρ̄_f = ρ̄_f0 exp(p/K_f)`):
  `ADReal rho=rho0*exp(p/Kf);`
- Reference fluid mass (eq. `fe-reference-fluid-mass`, `m_f = ρ̄_f (J − φ_s0 J̄)`):
  `s.mass=rho*(s.J-phi*s.y);`
- Darcy law (eq. `fe-reference-darcy-law`,
  `Q_f = −(J ρ̄_f k/μ_f) F^{-1}F^{-T} Grad p`, `mobility = k/μ_f`):
  `s.flux=-mobility*s.J*rho*(invF*invF.transpose())*gradp;`
- Mineral EOS (eq. `anisotropic-mineral-eos`). Code residual
  `Ks*(q0-target)+alpha*p*y0` with
  `target=K/(phi*Ks)*log(s.J)-alpha/(3*Ks)*stiffness(cs,dev).trace()`,
  `alpha=1-K/(phi*Ks)`, `q0=ln J̄`. Expanding gives exactly
  `K_s ln J̄ + (1−K/(φ_s0K_s)) p J̄ − (K/φ_s0) ln J + (1/3)(1−K/(φ_s0K_s)) I:C_s:dev ε = 0`.
- Stored energy (eq. `equivalent-anisotropic-energy`):
  `s.energy=K/(2*alpha)*pow(log(s.J)-q,2)+phi*.5*contract(em,T);`
- Solid fraction (eq. `distention`, `φ_s = φ_s0 J̄/J`) and stability domain
  (eq. `trace-mineral-stability-domain`, `K_s + α p J̄ > 0`):
  `s.solid=phi*s.y/s.J;` `s.stability=Ks+alpha*p*s.y;`
- Biot tensor (eq. `anisotropic-biot-explicit`):
  `s.B=I-s.y/(s.J*s.stability)*(K*I-phi*alpha/3*F*LB*F.transpose());`
  with `LB = ∫ (I+Dx)^{-1} dev(C_s:I) (I+Dx)^{-1} dx` = `∂log C/∂C : dev(C_s:I)`
  and `devCsI = stiffness(cs,I) - I*(3*Ks)` (since `tr(C_s:I)=9K_s`). Matches the
  manuscript term `−(φ_s0/3)(1−K/(φ_s0K_s)) F[∂logC/∂C:dev(C_s:I)]F^T`.
- Reference Biot (eq. `reference-biot-compatibility`), linear mode:
  `tensorRowCdInverseCs() = phi*I - phi*alpha/(3*Ks)*stiffness(cs,I)`, i.e.
  `C_d:C_s^{-1}:I = φ I − (φ α/(3K_s)) C_s:I`, so `B_0 = I − φ I + (φ α/(3K_s)) C_s:I`.
  For the isotropic case this gives `B_0 = (1 − K/K_s) I`.
- Reference total storage in linear mode
  (eq. `fe-reference-total-storage`): `storage=(1-phi)/Kf+phi*alpha/Ks`
  = `(1−φ)/K_f + S_s`, `S_s=(φ/K_s)(1−K/(φK_s))`.
- Appendix log-Fréchet (`sections/logarithmic_derivative.tex`,
  eq. `log-frechet-spectral-form`): `(lnλ_i−lnλ_j)/(λ_i−λ_j)` with equal-eigenvalue
  limit `T_ij/λ_i`; it is self-adjoint and satisfies `tr τ = tr T`. The code's
  resolvent integral `∫ (I+Dx)^{-1} T (I+Dx)^{-1} dx` is the same operator.

Equation traceability (all labels resolve):

```
$ python3 (collect \label from main.tex + sections + provenance; compare to refs)
total labels: 106
map equation refs: ['eq:anisotropic-biot-explicit', 'eq:anisotropic-mineral-eos',
 'eq:constitutive-phase-stress-sum', 'eq:equivalent-anisotropic-energy',
 'eq:log-frechet-spectral-form', 'eq:trace-mineral-stability-domain']
UNRESOLVED equation refs in map: []
UNRESOLVED eqref/cref targets: []
```

Conclusion (a): every kernel/material traces to a stated equation; the momentum
residual uses the **total** first Piola stress (not drained `−pB`); the declared
exponential fluid EOS and the current-configuration isotropic Darcy law are
implemented as written; the mineral EOS signs and factors match the paper.

### 2.b Analytical reference reproduction (charge b)

```
$ cd /tmp/r13r2 && python3 \
  <snapshot>/validation/mandel_reference.py --self-check --output-dir /tmp/r13r2/mandel-ref
EXIT=0
category analytical-reference-only
passed True
n_checks 38
failed []
overshoot ratio 1.0546586069998425     (5.4659%)
overshoot time  0.015165352045764979
derived {'Ku': 2.6941176470588237, 'nu': 0.2, 'nu_u': 0.3726273726273726,
         'skempton': 1.0480349344978166, 'c': 3.8216560509554145,
         'root_ratio': 4.63425925925926, 'initial_pressure_per_load': 0.4795204795204795}
source_sha256 e5cf969c5c9714ea31aa8bd8a7ed4745a69b3984ae5ca9c096064368c44ebe7a
```

This **exactly** reproduces the stated values in `site/evidence.json`:
"The independent Mandel reference passes 38 self-checks (peak overshoot 5.4659%
at t = 0.01516535)." The tool must be run from a writable CWD because it writes
its report under its `--output-dir` (default `.agent-runtime/...`); the snapshot
root is read-only, which is expected.

I also verified the reference inputs are consistent with the paper's stated
material set (`sections/finite_elements.tex`): φ_s0=0.9, K_s=2.5, μ_s=5/6, K=1,
K_f=8, k/μ_f=1.5. Then G=φ_s0 μ_s=0.75, B_0=1−K/K_s=0.6,
S=(1−φ)/K_f+(φ/K_s)(1−K/(φK_s))=0.0125+0.2=0.2125=17/80 ⇒ M=80/17,
Ku=K+α²M=229/85. All match the reference's derived quantities and the paper's
stated values (G=0.75, Biot 0.6, storage 17/80).

### 2.c Independent reproduction of the published Python suites

In a `/tmp` copy of the tree (`/tmp/r13r2/tree`):

```
$ python3 examples/verify_conformal.py
checks_passed 186
legacy_identities_rechecked 67
max_constitutive_identity_error 2.4549890331732928e-09
observed_orders energy_stress [2.00039, 2.00010, 2.00002, 2.00001]

$ python3 examples/verify_fluid_coupling.py --output /tmp/r13r2/fluid
{"scope": "Fluid EOS and reference-mass derivatives; not FE verification",
 "count": 110, "passed": true, "maximum_scaled_error": 8.086725789002713e-09}

$ python3 examples/verify_tensor.py
"materials": 13, "states_per_material": 21, "total_states": 273

$ python3 examples/verify_reconstruction.py
"incompatible_pairs_rejected": 20, "materials": 20,
"minimum_drained_eigenvalue": 1.8415045063808817
```

Every number matches the snapshot's own reports
(`site/reports/conformal-verification.json`: `checks_passed 186`,
`max_constitutive_identity_error 2.4549890331732928e-09`;
`fluid-coupling-verification.json`: `count 110`,
`maximum_scaled_error 8.0867e-09`;
`tensor-verification.json`: 13 materials, 273 states) and the manuscript's stated
"186 named checks, including the 67 checks of rotation, virtual work, and volume
response" and "largest absolute error ... 2.5×10^{-9}" and "273 finite states
across 13 mineral stiffnesses".

MMS convergence claims (`site/evidence.json`, convergence category) reproduce from
`site/reports/mms-convergence.json`: spatial `ux 2.99/2.96`, `uy 3.00/2.96`,
`p 2.00/2.00` over nx=4,8,16; temporal nx=16 `ux 1.093, uy 0.978, p 1.015`; nx=64
`ux 1.40, p 1.25` (the finer-mesh values quoted as spatial-floor contaminated).

### 2.d Comparability honesty (charge c)

Per-run flags in `fe-evidence/runs/*/analysis.json`:

```
reference_comparable=true : isotropic, linear_coarse, linear_load_reference,
  linear_space_10/20/40, linear_time_0.001/0.002, anisotropic_0/30/30_coarse/
  30_fine/45/90, nonlinear_load_0.01/0.001/0.0001
reference_comparable=false (with reference_note): partial_0, partial_30,
  partial_30_coarse, partial_30_fine
no flag (no Mandel comparison claimed): mms_space_4/8/16, mms_time_*, one_element_*
```

For the four `reference_comparable=false` runs, the reference-normalized metrics
are genuinely absent (verified programmatically):

```
partial_0            ref_comparable=False normalized_metrics_present=NONE
partial_30           ref_comparable=False normalized_metrics_present=NONE
partial_30_coarse    ref_comparable=False normalized_metrics_present=NONE
partial_30_fine      ref_comparable=False normalized_metrics_present=NONE
```

The `finite_deformation` category in `site/evidence.json` is `"pending"`, states
"compared ... as demonstrations, not as verification", records the partial family
as "not comparable", and says "No finite-deformation quantitative verification
claim is made." The manuscript agrees (`sections/finite_elements.tex` "Scope of
these results", abstract, and conclusions: "no quantitative finite-deformation
verification and no experimental validation is claimed"). The `physical_validation`
category is `"not_performed"`. Non-comparable runs back no verification claim.

The anisotropic-family ranges quoted in `site/evidence.json` reproduce exactly:

```
RANGE pressure_max_normalized  0.7549 - 0.8575   (claimed 0.75-0.86)
RANGE platen_max_normalized    0.7320 - 0.7754   (claimed 0.73-0.78)
RANGE edge_ux_max_normalized   1.6114 - 1.7796   (claimed 1.61-1.78)
RANGE profile_max_normalized   0.7550 - 0.8750   (claimed 0.75-0.88)
```

### 2.e Physical checks (charge d)

- One-element undrained (`fe-evidence/runs/one_element_undrained/analysis.json`):
  `pass: true`, `absolute_error 3.8e-15`, `mass_change −1.0e-16` (fluid mass
  conserved to machine precision). I independently regenerated the expected values
  with the same independent Python model and `decks.initial_mandel`:
  `expected 0.002476998516454143, −0.0004156360113397226, 0.004783296459228801`
  — identical to the recorded expected and actual values.
- One-element drained (`one_element_drained/analysis.json`): `pass: true`,
  `absolute_error 1.55e-16`, `p = 0`. `mass_change −2.38e-4` (fluid expelled)
  is not a gate, which is appropriate for a drained test. Independent regeneration:
  `expected 0.0013271584736625449, −0.0005291067041957089, 0.0` — identical.
- Force equilibrium: `force_relative` = 8.999745393367675e-13 (q=0.01),
  1.3999218451132833e-12 (q=0.001), 1.547099986098574e-09 (q=1e-4) for the
  nonlinear small-load family; 2.14e-12 (anisotropic_30) and 2.05e-10 (partial_30).
  Matches the evidence claim of "order 1e-10 or smaller"; `platen_equality_absolute`
  ~1e-14–1e-17. Backed by the `DofReactionSum` postprocessor summing the top normal
  DOF reaction, which is the discrete plate resultant.
- Mass conservation: `discrete_mass_mobilized_relative` between ~1e-11 and 1.4e-8
  across runs, far below the pre-registered 1e-3 target in
  `validation/reference-data/verification-contract.md`. The `ReferenceFluidMass`
  kernel uses backward-Euler on the full reference mass and the same end-step flux
  quadrature, consistent with eq. `fe-conservative-time-step`.
- Load-limit behavior: `figures/fe_load_limit.csv` and
  `nonlinear_load_0.0001/analysis.json` give
  `pressure_max_normalized = 0.003220919735602341` (= 3.22e-3). This matches the
  evidence.json and manuscript claim that the normalized discrepancy "floors at
  about 3.2×10^{-3}" rather than decaying, and is reported as a demonstration, not
  a verified linear limit. The evidence honestly attributes this to a discretization
  floor at nx=20, dt=1e-3.

### 2.f Packaging completeness (charge e)

All declared SHA-256 values in the enumerated sources resolve to files present
inside the snapshot with matching hashes:

```
=== site/evidence.json artifacts ===
counts {'OK': 21}          # 21 declared, 21 present+match, all also in source-manifest.json
=== site/scientific-snapshot.json files ===
counts {'OK': 33}          # 33 declared, 33 present+match
=== site/reports/*.json artifacts blocks ===
mandel-reference.json: 2/2 OK (mandel-probes.csv, mandel-profiles.csv)
conformal-verification.json, fluid-coupling-verification.json, mms-convergence.json,
reconstruction-verification.json, tensor-verification.json: (no artifacts block)
counts {'OK': 2}
```

Manuscript figure and archive references resolve:

```
includegraphics targets: build/conformal/{pressure_response,shear_response,
  directional_response,rotation_response,constrained_layer}.pdf  -> all OK
embedfile: build/conformal-2026-09-20-v1.zip  -> OK
```

Supplement archive internal consistency (extracted to `/tmp/r13r2/zip`):

```
archive manifest: ok=33 mismatch=0 missing=0 total=33
present but not declared: []
```

`site/reports/*.json` non-artifact hash fields:
- `fluid-coupling-verification.json.source_sha256` uses repository-relative paths:
  `examples/conformal_model.py` and `examples/verify_fluid_coupling.py` → 2/2 match.
- `conformal-verification.json.source_sha256` uses bare basenames
  (`conformal_model.py`, `verify_conformal.py`) that do **not** resolve as written
  from the snapshot root (the files live under `examples/`). The hashes themselves
  do match `examples/conformal_model.py` and `examples/verify_conformal.py`.

**Dangling declarations found (charge e):**

1. `fe-evidence/plot-manifest.json` (a shipped, manifest-listed file) declares 66
   `output_sha256` figure/data files (`fe_*.pdf`, `fe_mms_orders.csv`,
   `fe_map_*_samples.csv`, `fe_map_*_pressure_dofs.csv`, `fe_map_*_connectivity.csv`, …)
   and its `figures[].files`/`figures[].data` arrays list the same names. Of these,
   **54 figure/data paths do not exist anywhere in the snapshot**
   (`figures/` contains only the 12 files referenced by `site/evidence.json`).
   Its `input_sha256` block (147 entries) also references the runtime directory
   `.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs/...`, absent from
   the snapshot.
2. `README.md` references `reviews/README.md`, `agent_local/skills/biot-*/`, and
   `references/notes/weighted-stress-reconsideration.md`; `AGENTS.md` references
   `agent_local/skills/`. None of `reviews/`, `agent_local/`, or `references/`
   exist inside the snapshot.

Note that the *published* evidence does not depend on these: all 7 published
figures and 5 published data files in `site/evidence.json` resolve, and the
manuscript's own `\includegraphics`/`\embedfile` targets resolve. The dangling
entries are internal generator/record and documentation references.

## 3. Findings with severity

**(a) Requirements affecting correctness/reproducibility — none found.**
No kernel/material mismatch, wrong sign/factor, wrong fluid EOS, wrong
permeability law, or misleading verification claim was found. The momentum
residual uses the total stress, not a drained `−pB` form. All equation
cross-references resolve.

**(b) Minor / editorial findings**

- M1 (minor, packaging): `fe-evidence/plot-manifest.json` declares 66 output
  artifact hashes and 147 input hashes that do not resolve inside the snapshot
  (54 figure/data paths absent; all inputs point at the runtime run directory).
  See 2.f.1.
- M2 (minor, packaging): `README.md` / `AGENTS.md` reference `reviews/`,
  `agent_local/skills/biot-*/`, and `references/notes/...`, none of which exist in
  the snapshot. See 2.f.2.
- M3 (minor, editorial): `site/reports/conformal-verification.json` records
  `source_sha256` under bare basenames (`conformal_model.py`,
  `verify_conformal.py`) while the sibling `fluid-coupling-verification.json` uses
  repository-relative paths (`examples/...`). The hashes are correct; only the
  path form is non-resolvable as written. Inconsistent with the pattern used
  elsewhere.
- M4 (minor, hygiene): `moose_app/src/main.x86_64-conda-linux-gnu.opt.lo.d` is a
  compiler dependency-tracking artifact shipped under `src/` and listed in the
  source manifest; `moose_app/anisotropic_biot.yaml` also lists `WASPAPP` under
  `registered_apps`. Neither affects results but both are build-workspace residue.

**(c) Optional suggestions**

- S1: Add the missing `site/reports/*.json` reports' provenance fields
  (e.g., input deck hashes) or explicitly state that these reports carry only
  source hashes, to make the evidence chain uniform.
- S2: `site/evidence.json` `provenance.source_revision` is a base commit described
  as predating the working revision; a note that the snapshot ID above is the
  authoritative frozen artifact would close the provenance loop for reviewers.
- S3: Consider dropping `plot-manifest.json` from the published snapshot or
  regenerating it against the shipped `figures/` set so the manifest and the
  shipped files agree.

## 4. Required corrections

None that affect correctness or reproducibility. I found no constitutive,
analytical-reference, comparability, or physical-check defect, and every hash
declared in `site/evidence.json`, `site/scientific-snapshot.json`, and the
`site/reports/*.json` artifacts blocks resolves inside the snapshot. The items in
section 3(b) are packaging/documentation hygiene and do not alter any numerical
result or verification claim; I recommend fixing them before publication but they
are not correctness-blocking.

## 5. Optional suggestions

See S1–S3 in section 3(c).

## 6. Verdict

This is a strong, honest verification package. The constitutive implementation is
faithful to the stated equations (total stress, exponential fluid EOS,
current-configuration isotropic Darcy law, mineral EOS with correct signs and
factors, explicit Biot tensor). The independent Mandel reference reproduces its
stated 38 checks and 5.4659% peak overshoot exactly, and I independently reproduced
the 186/110/273-check suites and their maximum errors. Comparability labeling is
accurate: partial-drainage runs are marked non-comparable with reference-normalized
metrics omitted, and no non-comparable run backs a verification claim. The one-element
drained/undrained, mass-conservation, force-equilibrium, and load-limit diagnostics
reproduce. Packaging hashes all resolve; the only defects are dangling internal
generator/documentation references (minor hygiene), not correctness issues.

VERDICT: MINOR REVISION
