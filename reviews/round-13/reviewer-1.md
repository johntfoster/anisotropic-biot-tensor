# Round-13 Independent Review — Reviewer 1 (Mathematics and Correctness)

## 1. Reviewed version, snapshot ID, integrity result

- **Frozen snapshot:** `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/review-snapshots/round-13` (read-only, mode 444/555).
- **Snapshot ID (from `SNAPSHOT_ID`):** `69a39ab45c1fbeed02118958391509d19d5c51fb2779cb278b366594ae38375c`
- **Reviewer:** round-13 reviewer 1 of 3. No prior-round report and no other reviewer report was read. Only the frozen snapshot was used for all findings; the live tree was read twice solely to characterize a snapshot-packaging gap (noted in §4).
- **Documents audited:** `sections/finite_elements.tex`, `sections/experiments.tex` (FE-relevant parts), `sections/limits.tex`, `main.tex` (FE-relevant equations), `moose_app/**`, `fe-evidence/**`, `validation/**`, `figures/**`, `site/evidence.json`, `site/scientific-snapshot.json`.

### Integrity step (mandatory, first)

```
$ cd .../review-snapshots/round-13
$ sha256sum source-manifest.json
69a39ab45c1fbeed02118958391509d19d5c51fb2779cb278b366594ae38375c  source-manifest.json

$ cat SNAPSHOT_ID
69a39ab45c1fbeed02118958391509d19d5c51fb2779cb278b366594ae38375c
```

Manifest hash **equals** the SNAPSHOT_ID value. Every file listed in `source-manifest.json` was then hashed:

```
listed: 340 ok: 340 mismatch: 0 missing: 0
```

`find . -type f | wc -l` = 342; the two files not listed are `SNAPSHOT_ID` and `source-manifest.json` themselves.

**Integrity result: PASS — 340/340 listed files present and bit-exact; 0 mismatches, 0 missing.**

---

## 2. Independent recomputation evidence (literal commands and outputs)

All scratch work was written under `/tmp/r13r1/`. Nothing inside the snapshot was modified.

### 2.1 Manufactured-solution observed orders, recomputed from raw `analysis.json` norms

```
$ python3 - <<'EOF'
import json, math
from pathlib import Path
R=Path("fe-evidence/runs")
def an(n): return json.loads((R/n/"analysis.json").read_text())
VARS=("ux_l2","uy_l2","p_l2")
print("SPACE (dt=1e-4), naive order = log2(E_h / E_{h/2})")
sp=[an(f"mms_space_{n}") for n in (4,8,16)]
for v in VARS:
    e=[s[v] for s in sp]
    print(f"  {v}: E={e} orders={[round(math.log2(e[i]/e[i+1]),6) for i in range(2)]}")
...
EOF
SPACE (dt=1e-4), naive order = log2(E_h/E_h/2)
  ux_l2: E=[1.6422301738159e-07, 2.0646791097949e-08, 2.6562048828672e-09] orders=[2.991667, 2.958479]
  uy_l2: E=[1.6952249963971e-07, 2.1215866084525e-08, 2.7265675427702e-09] orders=[2.998261, 2.959986]
  p_l2:  E=[4.8587321289799e-06, 1.2175243786378e-06, 3.0421081743803e-07] orders=[1.996629, 2.000807]
TIME nx=16 dt=0.02/0.01/0.005
  ux_l2: diff_order=1.093195
  uy_l2: diff_order=0.978304
  p_l2:  diff_order=1.015177
TIME nx=32
  ux_l2: diff_order=1.396878
  uy_l2: diff_order=1.018346
  p_l2:  diff_order=1.125199
TIME nx=64
  ux_l2: diff_order=1.396366
  uy_l2: diff_order=1.076204
  p_l2:  diff_order=1.251931
```

These reproduce every order quoted in `site/evidence.json` ("ux 2.99/2.96, uy 3.00/2.96, p 2.00/2.00"; "nx=16 triple (ux 1.093, uy 0.978, p 1.015)"; "nx=64 ux 1.40, p 1.25"). The `mms-convergence.json` file (both `fe-evidence/` and `site/reports/` copies) is byte-consistent with these norms; the two copies are content-identical apart from the `runs_dir` string.

**Consistency with FE theory:** Q2 displacement gives L2 order 2.99≈3 and Q1 pressure gives 2.00; backward-Euler temporal order is bounded near 1. This is the expected pattern for the discrete spaces declared in `validation/equation_to_moose_map.yml` (ReferenceMomentum FE: Q2; ReferenceFluidMass FE: Q1) and in the deck (`order = SECOND` for `ux`,`uy`; `order = FIRST` for `p`).

### 2.2 Discrete mass / force / platen balances recomputed from raw `solution.csv`

I bypassed `analysis.json` and recomputed the diagnostics from the raw scalar histories using the same conventions as `moose_app/scripts/analyze_mandel.py`:

```
$ python3 - <<'EOF'
import numpy as np, json
from pathlib import Path
for case in ["anisotropic_30","anisotropic_0","anisotropic_45","anisotropic_90","partial_0","partial_30"]:
    p=Path("fe-evidence/runs")/case
    cfg=json.loads((p/"provenance.json").read_text())["configuration"]
    q=cfg["load"]; quarter = cfg.get("case")=="mandel"
    width = 1.0 if quarter else 2.0
    expected_force = -q*width
    ramp_time = 0.0 if quarter else 0.002
    d=np.genfromtxt(p/"solution.csv",names=True,delimiter=",")
    t=d["time"]
    ramp=np.ones_like(t) if quarter else np.minimum(t/ramp_time,1.0)
    applied=expected_force*ramp
    m=d["mass"]; reaction=d["mass_reaction"]; flux=-reaction
    budget=m-m[0]+np.r_[0,np.cumsum(np.diff(t)*flux[1:])]
    mobilized=np.maximum(abs(m-m[0]),np.r_[0,np.cumsum(np.diff(t)*abs(flux[1:]))])
    floor=max(abs(m[0])*1e-12,1e-16)
    out=dict(case=case,
        discrete_mass_absolute=float(np.max(abs(budget))),
        discrete_mass_mobilized_relative=float(np.max(abs(budget[1:])/np.maximum(mobilized[1:],floor))),
        force_relative=float(np.max(np.abs(d["top_reaction"][1:]-applied[1:]))/abs(expected_force)),
        platen_equality_absolute=float(np.max(abs(d["platen_min"]-d["platen_max"]))))
    ...
EOF
=== anisotropic_30 ===
  discrete_mass_absolute                   mine=5.944030e-14 json=5.944030e-14 OK
  discrete_mass_mobilized_relative         mine=1.237090e-11 json=1.237090e-11 OK
  force_relative                           mine=2.142889e-12 json=2.142889e-12 OK
  platen_equality_absolute                 mine=1.699162e-15 json=1.699162e-15 OK
=== anisotropic_0 ===        (all OK; force_relative 4.000134e-12)
=== anisotropic_45 ===       (all OK; force_relative 2.285632e-12)
=== anisotropic_90 ===       (all OK; force_relative 1.642971e-12)
=== partial_0 ===            (all OK; force_relative 5.857061e-12)
=== partial_30 ===           (all OK; force_relative 2.052143e-10)
```

All four diagnostics match the stored JSON to ≤1e-15 relative for all six runs. The signs are self-consistent: the mass budget `m(t) − m(0) + Σ Δt·flux` closes to ~1e-11 relative (a sign error would leave the full ~O(0.1) imbalance); `top_reaction` matches `−q·width` (with the `min(t/0.002,1)` load ramp for the non-quarter decks) to ≤2.1e-10 relative.

### 2.3 Independent re-derivation of the manufactured forcing (strong form)

I implemented the documented reference-tangent law from scratch (independent Mandel basis, independent active +30° rotation, independent `C^d` and `B_0`), then compared `b_i = −∂_j σ_ij` and `s = ∂_t m + ∂_j Q_j` (numeric differentiation, h=1e-6) against the deck's `ParsedFunction` expressions parsed from `fe-evidence/runs/mms_space_4/input.i`:

```
Ks= 28.0 alpha= 0.5833333333333334
B0=
 [[ 0.71458333 -0.02525907  0.        ]
  [-0.02525907  0.74375     0.        ]
  [ 0.          0.          0.79166667]]
B0 vs documented max abs diff: 1.1102230246251565e-16
Ss= 0.0125 S= 0.0625
point            b_x(indep)   b_x(deck)    b_y(indep)   b_y(deck)   s(indep)    s(deck)
(0.31,0.27,0.4)  9.86390507e-01 9.86390507e-01 2.04958686e-01 2.04958686e-01 5.98445869e-02 5.98445869e-02
(0.5,0.5,1.0)    2.65194343e+00 2.65194343e+00 -1.05287700e-01 -1.05287700e-01 4.28749991e-04 4.28749991e-04
(0.13,0.81,0.7)  2.55672796e-01 2.55672796e-01 1.83473610e+00 1.83473610e+00 -1.49522287e-01 -1.49522287e-01
(0.9,0.05,0.3)   2.40381215e-01 2.40381215e-01 1.82862331e-01 1.82862331e-01 -1.07107435e-01 -1.07107435e-01
MAX abs discrepancy deck vs independent strong form: 4.1994074884144084e-11
```

The 4.2e-11 residual is the finite-difference truncation of my own reference (h=1e-6); the deck forcing is analytically consistent with the documented strong form. `B_0` matches the value published in `validation/reference-data/mms-reference.md` to 1.1e-16.

### 2.4 Equation ↔ implementation cross-checks

| Manuscript equation | Source | Check |
|---|---|---|
| `eq:fe-total-first-piola` `P = JσF^{-T}` | `ConformalLaw.h` `s.P=s.J*s.sigma*F.inverse().transpose()` | match |
| `eq:fe-fluid-eos` `ρ̄_f = ρ̄_{f0} e^{p/K_f}` | `ADReal rho=rho0*exp(p/Kf)` | match |
| `eq:fe-reference-fluid-mass` `m_f = ρ̄_f(J−φ_{s0}J̄)` | `s.mass=rho*(s.J-phi*s.y)` | match |
| `eq:fe-reference-darcy-law` `Q_f = −(Jρ̄_f k/μ_f)F^{-1}F^{-T}∇p` | `s.flux=-mobility*s.J*rho*(invF*invF.transpose())*gradp` (`mobility = k/μ_f`) | match |
| `eq:fe-fluid-storage` | analytically `∂_p m_f = ρ̄_f[(J−φJ̄)/K_f − φ ∂_p J̄]` | match |
| `eq:fe-fluid-deformation-coupling` | `δm_f|_p = ρ̄_f(J−φJ̄)` ⇒ consistent with `eq:biot-pore-volume-variation` (`δ(J−φJ̄)/J = B:(δF F^{-1})`) | match |
| `eq:fe-reference-total-storage` | `(1−φ_{s0})/K_f + S_s`; code `(1-phi)/Kf + phi*alpha/Ks` with `S_s=φ α/K_s` | match |
| `eq:fe-momentum-residual` | `ReferenceMomentum::computeQpResidual` = `Σ_j grad_test_j · P_{comp,j}` | match |
| `eq:fe-fluid-residual` | `ReferenceFluidMass::computeQpResidual` = `test·(m−m_old)/dt − grad_test·flux` | match |
| `eq:fe-conservative-time-step` (backward Euler on full `m_f`) | full mass `m` and `MaterialPropertyOld<Real> _old` | match |
| `eq:drained-stiffness-restriction` `C^d = φC_s − φ/(9K_s)(1−K/(φK_s))(C_s:I)⊗(C_s:I)` | `cd[i][j]=phi*cs[i][j]-phi*alpha/(9*Ks)*ci*cj` | match |
| `eq:reference-biot-compatibility` `B_0 = I − C^d:C_s^{-1}:I` | `I - tensorRowCdInverseCs()` | algebraically identical (verified: the rank-one term maps `C_s^{-1}:I` to `3·(C_s:I)`), and equals the documented `B_0` to 1.1e-16 |

The implicit differentiation of the mineral root is implemented correctly: the residual is AD-valued and the update `q = q0 − (r(q0) − raw(r(q0)))/den` with `den = K_s + αp e^{q}` propagates derivatives of both `F` and `p`, so mechanical–hydraulic coupling is retained (as `finite_elements.tex` claims).

### 2.5 Supporting arithmetic and hash claims

```
$ python3  # Mandel reference parameter arithmetic
G=phi_s0*mu_s = 0.75 ;  alpha=1-K/Ks = 0.6
S_s= 0.2 ;  1/M= 0.21250000000000002 ;  17/80 = 0.2125
mu_average (mean deviatoric mode sum /10) = 16.8
```

- `finite_elements.tex`: `G=0.75`, `α=0.6`, total storage `17/80` — all confirmed.
- `experiments.tex`: mineral shear modulus `16.8 K_*` = (mean of five deviatoric modes)/2 — confirmed (`trace(dev-proj·C_s)=168`, mean 33.6, /2 = 16.8).
- `site/evidence.json` artifact hashes: **21 ok, 0 bad, 0 missing**.
- `site/scientific-snapshot.json` file hashes: **33 ok, 0 bad, 0 missing**.
- `one_element_drained`/`one_element_undrained`: `absolute_error 1.55e-16` / `3.80e-15`, both `pass: true`; undrained `mass_change −1.0e-16` (conservation).
- Load-limit floor: `nonlinear_load_0.0001` `pressure_max_normalized = 0.0032209` — matches the manuscript's "floors at about 3.2e-3".
- Isotropic Mandel spatial refinement at the finest level is non-monotone (`pressure_max_normalized` 10→20→40 = 2.08e-3, 4.58e-4, 6.36e-4) — matches the manuscript's stated non-monotonicity.

### 2.6 Evidence-script failure behaviour

- `fe-evidence/compute_mms_order.py` fails loudly (`sys.exit(2)`) if any required run is missing or lacks `analysis.json`; it refuses to emit a partial table. Verified by inspection.
- `examples/plot_fe_results.py` requires `provenance.json`+`analysis.json`+`solution.csv`, rejects non-zero exit codes and non-monotone/NaN histories (raises on hash change of inputs), and records absent families in a `missing` list rather than synthesizing curves. The `plot-manifest.json` `missing` list contains the three `jacobian_*` families and the two `one_element_*` families (correctly reported, not plotted).
- `moose_app/scripts/run_case.py` refuses to overwrite existing evidence (`raise RuntimeError`) and raises on a non-zero solver exit code.

---

## 3. Findings with severity

### 3.1 Required corrections (affect correctness/reproducibility)

**None.** Every number quoted in the finite-element section and in the machine-readable convergence/balance evidence was independently reproduced from the frozen snapshot. No equation/implementation mismatch was found; no factor, sign, or limit error was found in `sections/finite_elements.tex`.

### 3.2 Minor / editorial findings

- **M1 (evidence packaging).** Every run's `provenance.json` lists a `run.log` entry in its `outputs` map with a SHA-256, but no `run.log` exists in the snapshot and none is listed in `source-manifest.json`. Consequence: the assembled-Jacobian self-test (`moose_app/scripts/check_jacobian.py`, run with `-snes_test_jacobian`) has its only recorded result (`‖J−J_fd‖_F/‖J‖_F`) inside `run.log`, which is not shipped. The `plot-manifest.json` also reports the three `jacobian_*` families as "Completion provenance, analysis, or scalar history is absent." This does **not** affect any quoted result (the Jacobian test is not cited in the manuscript or in `site/evidence.json`), but the provenance records reference artifacts the snapshot does not contain.
- **M2 (evidence wording).** `site/evidence.json` attributes the nx=32/64 temporal orders (ux 1.40, p 1.25) to "residual spatial-floor contamination." Successive differences cancel a *dt-independent* mesh floor exactly (`D(Δt)=C Δt^q(1−2^{−q})`); the departure from order 1 therefore requires a cross term (`h^p·Δt`) or a Δt-dependent floor. The script's own comment ("cancels E_h to leading order") is correct; the evidence.json phrasing is loose. The numerical conclusion (order ≈1, "at most about 1.1" from the nx=16 triple) is defensible.
- **M3 (evidence wording).** `site/evidence.json` states the finite-deformation `force_relative` is "of order 1e-10 or smaller," but the recomputed maximum over the partial family is `2.052e-10` (slightly above 1e-10). Suggest "≤ ~2×10^-10."
- **M4 (bookkeeping).** `fe-evidence/plot-manifest.json` lists data files (e.g., `fe_mms_orders.csv`, ten `fe_map_*_*.csv`) that are not present in `figures/`; `figures/` ships 12 files (2 maps + the rest). `site/evidence.json`, which is what the companion publishes, is self-consistent and hash-complete, so this is an internal superset record only.

*(Note on M1: the live tree does contain the `run.log` files, so this is a snapshot-packaging gap rather than a fabrication; it is reported because it is inside the frozen artifact set and its provenance claims cannot be checked from the snapshot alone.)*

### 3.3 Optional suggestions

- Add the assembled-Jacobian self-test ratio as a small standalone JSON report so that this check is reproducible from the evidence package.
- In `sections/finite_elements.tex` §"Reference problems", state that the spatial convergence is measured at fixed `Δt=1e-4` and that a ~10% residual temporal contribution explains the 2.96 (rather than 3.00) finest displacement order.
- State explicitly that the difference-method temporal order is an upper estimate whenever a positive higher-order error term is present.

---

## 4. Required corrections (with "why required")

**None.** No finding meets the bar of affecting correctness or reproducibility of a quoted result:
- The one implementation-verification gap (M1, missing `run.log`) concerns a diagnostic that is *not* cited as evidence for any claim in `sections/finite_elements.tex` or `site/evidence.json`; all quoted FE numbers reproduce from files that *are* shipped.
- M2–M4 are wording/bookkeeping in the evidence package and do not alter any reported value.

I therefore record **no required corrections to the manuscript's finite-element mathematics.**

## 5. Optional suggestions

See §3.3.

## 6. Review limitations

- I could not execute the MOOSE application (the compiled `anisotropic_biot-opt` binary and the source-versions/build are not part of the reviewed snapshot), so I verified the recorded raw outputs and re-derived the reference law rather than re-running the solver. All convergence and balance numbers were reproduced from the raw `analysis.json`/`solution.csv` data that *is* shipped.
- The constitutive-only suites (`site/reports/conformal-verification.json`, `tensor-verification.json`, `reconstruction-verification.json`, `fluid-coupling-verification.json`) were inspected by inspection of their stored check lists, not independently re-executed; they are outside the core FE charge.
- The assembled-Jacobian ratio could not be verified from the snapshot (M1).

VERDICT: MINOR REVISION
