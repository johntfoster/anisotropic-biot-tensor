# Round-14 independent review — Reviewer 1 (mathematics and correctness)

## 1. Reviewed version, snapshot ID, integrity result

- Repository: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
- Frozen snapshot reviewed (read-only): `.agent-runtime/review-snapshots/round-14`
- SNAPSHOT_ID: `061a92feee93641668978ab0ecec033d0b9fe0d20ad74efbcb9ec0bf1a60ea69`
- Integrity: **PASS**.

Literal commands and outputs:

```
$ sha256sum .agent-runtime/review-snapshots/round-14/source-manifest.json
061a92feee93641668978ab0ecec033d0b9fe0d20ad74efbcb9ec0bf1a60ea69  .../round-14/source-manifest.json
```

```
$ (hash every path listed in source-manifest.json)
listed 441 ok 441 mismatch 0 missing 0
```

The manifest digest equals SNAPSHOT_ID exactly, and all 441 listed files hash
to their recorded digests. Integrity therefore holds and the audit proceeded
against the frozen snapshot only. Scratch copy was made with
`cp -r <snapshot> /tmp/r14 && chmod -R u+w /tmp/r14`; the snapshot itself was
not written to. A MOOSE binary is not shipped in the snapshot, so all coupled
solver results were audited by **re-deriving independently from the recorded
raw outputs** rather than re-running the solver (see §6).

## 2. Independent recomputation evidence

All commands below were run in `/tmp/r14` (the writable copy). Every result is
my own recomputation from the shipped raw data / paper equations, not a re-read
of a recorded verdict.

### 2.1 MMS forcing re-derived from scratch, compared to the shipped deck

I independently built the constant-reference-tangent model
(phi=0.6, K=7, Kf=8, rho0=1, mobility=1.5, 30-deg-rotated Cs), derived
`b_i = -d_j sigma_ij` with `sigma = Cd:e - B0 p` and
`s = d_t m + d_j Q_j`, and emitted the decimal ParsedFunctions. Result: an
**exact character-for-character match** to `fe-evidence/runs/mms_space_4/input.i`:

```
body_x= 3.1515565942422978*sin(t)*sin(3.1415926535897932*x)*sin(3.1415926535897932*y) + ...
body_y= -0.12512338688923574*sin(t)*sin(...)*sin(...) - ...
mass_source= 0.29608813203268076*sin(t)*cos(...)*cos(...) + 0.00079353722185247031*sin(...)*sin(...)*cos(t) + ...
```

The deck strings are identical. Derived constants confirmed independently:
`B0 = [[0.7145833333333333, -0.02525907, 0],[..., 0.74375, 0],[0,0,0.7916666667]]`,
`S_s = 0.0125`, `S = 0.0625`, `min eig(Cd) = 12.0`.

### 2.2 MMS observed orders recomputed from `analysis.json`

```
$ python3  # load fe-evidence/runs/mms_*/analysis.json, recompute orders
== SPACE (dt=1e-4, end=0.01) ==
ux_l2 norms [1.6422301738159e-07, 2.0646791097949e-08, 2.6562048828672e-09]  naive [2.9917, 2.9585]
uy_l2 norms [1.6952249963971e-07, 2.1215866084525e-08, 2.7265675427702e-09]  naive [2.9983, 2.9600]
p_l2  norms [4.8587321289799e-06, 1.2175243786378e-06, 3.0421081743803e-07]  naive [1.9966, 2.0008]
== TIME nx=16 ==  ux difforder [1.0932]  uy [0.9783]  p [1.0152]
== TIME nx=32 ==  ux [1.3969]  uy [1.0183]  p [1.1252]
== TIME nx=64 ==  ux [1.3964]  uy [1.0762]  p [1.2519]
```

These reproduce `fe-evidence/mms-convergence.json` and the `site/evidence.json`
summary verbatim. The final-time norm in each `analysis.json` equals the last
data row of the corresponding `solution.csv`
(e.g. `mms_space_4`: `0.01,4.8587321289799e-06,1.6422301738159e-07,1.6952249963971e-07`).

### 2.3 Constitutive reference law re-derived three independent ways

```
max|cdA-cdB| = 0.0            # software rank-one form vs tensor form Cs:I
max|cdB-cdC| = 3.55e-15       # tensor form vs inverted compliance restriction
B0 normal comps = [0.7145833, 0.74375, 0.7916667]   (= 343/480, 119/160, 19/24)
off-diagonal B12 = -7*sqrt(3)/480 = -0.0252591
S_s = 0.0125 = phi/Ks*(1-K/(phi*Ks));  min eig(Cd) = 12
```

`eq:anisotropic-mineral-eos` was re-derived from the energy
`W_s = K/(2(1-K/(phi Ks)))[ln(J/Jbar)]^2 + (phi/2) epsbar:Cs:epsbar` by
differentiating at fixed F and collecting terms; the resulting equation is
identical to the paper's, and to `ConformalLaw.h`
(`Ks*(q0-target)+alpha*p*y0`, `target = K/(phi*Ks)*logJ - alpha/(3Ks)*tr(Cs:dev)`).
The explicit Biot formula `eq:anisotropic-biot-explicit` at F=I,p=0 gives the
same tensor as the compliance relation `I - Cd:Cs^-1:I`.

### 2.4 Isotropic reduction and pressure-tangent identity

```
p=+0.00  -dσ/dp diag=[0.59979986 ...]  B diag=[0.59979986 ...]  max|diff|=5.9e-12
p=+0.50  -dσ/dp diag=[0.67108741 ...]  B diag=[0.67108741 ...]  max|diff|=1.8e-10
```

i.e. `d sigma/dp|_F = -B` for the isotropic nonlinear branch with
`B = [1 - K*Jbar/(J[Ks+(1-K/(phi Ks))p Jbar])] I` (paper
`eq:reconstructed-isotropic-source-biot`). Confirmed with an independently
written state solver (brentq on the mineral EOS) that imports none of the
repository code.

### 2.5 One-element expected values re-derived from scratch

```
drained  solved ex,ey = [0.00132716, -0.00529107]   resid 8.3e-17
undrained solved ex,ey,p = [0.002477, -0.00415636, 0.0047833]  resid 1.1e-16
```

vs shipped `analysis.json`: drained `edge_ux=0.0013271584736625449`,
`platen=-0.0005291067041957089`; undrained `edge_ux=0.002476998516454143`,
`platen=-0.0004156360113397226`, `p=0.004783296459228801`. Agreement to
~1e-13 in the last digits (my values differ only in the final 2-3 digits).

### 2.6 Discrete balances recomputed from raw `solution.csv`

```
$ (recompute budget = m-m0 + cumsum(dt*(-mass_reaction)) for anisotropic_30)
discrete_mass_absolute              = 5.94402999043453e-14
discrete_mass_mobilized_relative    = 1.2370904397879597e-11
force_relative                      = 2.1428890408157844e-12   (expected_force = -1.4)
platen_equality_absolute            = 1.6991616447192825e-15
peak_pressure                       = 0.20675184523297   peak_time = 0.003
```

Exact match to `anisotropic_30/analysis.json` and to the `analyze_mandel.py`
convention (`flux = -mass_reaction`, ramp `min(t/0.002,1)`, width 2a=2 for the
full domain).

### 2.7 Verification-suite counts and extrema re-derived

```
fluid-coupling checks = 110   max error = 8.0867e-09   (claim 8.09e-09, 110 checks)
tensor:    13 materials x 21 states = 273 states
reconstruction: 20 materials, 20 incompatible pairs rejected
conformal: 186 checks passed, 67 legacy identities; max_constitutive_identity_error = 2.455e-9
Cd min eigenvalue = 12.0 ; Mandel reference overshoot = 5.4657% at t = 0.015256
site/evidence.json artifacts: 22 checked, 0 missing, 0 hash mismatch
```

All match the shipped reports (`conformal-verification.json`,
`fluid-coupling-verification.json`, `tensor-verification.json`,
`reconstruction-verification.json`, `mandel-reference.json`, `cpp-python-constitutive.json`).

### 2.8 Cross-reference / citation integrity

```
total labels: 106 ; total refs: 33 ; UNRESOLVED refs: [] ; missing in bib: []
```

Also verified: `figures/fe_mandel_history.csv` last row reproduces
`linear_space_40/solution.csv` last row exactly (correct figure provenance);
`directional_response.csv` F=I theta=0/90 equals `pressure_response.csv`
B11/B22 at p=2 exactly; the embedded `conformal-2026-09-20-v1.zip` contains
`manifest.json` and 34 payload files.

## 3. Findings with severity

**F1 — LOW (evidence hygiene).** The three Jacobian-verification runs
(`fe-evidence/runs/jacobian_0.0001`, `jacobian_1e-05`, `jacobian_1e-06`) are
byte-identical in both `run.log` and `solution.csv`:

```
$ for d in jacobian_*; do md5sum $d/solution.csv; done
3d3d7364e7eec40dff745b12901c69a9  jacobian_0.0001/solution.csv
3d3d7364e7eec40dff745b12901c69a9  jacobian_1e-05/solution.csv
3d3d7364e7eec40dff745b12901c69a9  jacobian_1e-06/solution.csv
$ tail jacobian_0.0001/run.log
Option left: name:-MAT_FD_COLORING_ERR value: 0.0001 source: code
```

`check_jacobian.py` varies `-mat_fd_coloring_err` (`-1e-4/-1e-5/-1e-6`), but
PETSc reports that option as **unused**, so the intended step-refinement study
was not actually performed. The recorded Jacobian test itself is fine and
passes the contract target
(`||J-Jfd||_F/||J||_F ≈ 2.1e-7 to 2.4e-7 < 1e-6`), and no manuscript claim
cites these three runs, so this is evidence hygiene, not a wrong result.

**F2 — LOW/MEDIUM (misleading metadata in a published artifact).**
`analyze_mandel.py` sets `reference_comparable = (case != 'partial')`, so the
slender-domain `anisotropic_*` and full-domain `isotropic` runs are flagged
comparable and are normalized against the `MandelParameters()` series
(K=1, G=0.75, alpha=0.6, M=80/17). But those runs use a different material
(`decks.py`: `DEFAULT_CS`, phi=0.6, K=7, so G = phi*mu ~ 10.08, alpha = 0.75,
M ~ 16; the isotropic contrast uses `isotropic_stiffness(28, 16.8)`). The
material mismatch shows up as the large normalized errors already in the file
(`anisotropic_30 pressure_max_normalized = 0.758`,
`profile_max_normalized = 0.758`, `isotropic = 0.729`), versus ~0.003-0.005 for
the genuinely matching quarter-domain `linear_*` runs. The boolean
`reference_comparable` and the derived `*_normalized` fields for these cases
are therefore not physically meaningful. The manuscript text does label these
runs as demonstrations, so no manuscript claim is invalidated, but the
machine-readable evidence file (`site/evidence.json`, published as the
verification-evidence file) carries a flag that contradicts its own data.

**F3 — LOW (wording, disclosed data).** `site/evidence.json` convergence
summary lists `ux 1.397` (nx=32) and `ux 1.396` (nx=64) and then states "still
near one and never quoted as an order above one". Those measured difference
orders are above one (~1.4, reproducible and stable across two meshes). The
following sentence clarifies that no order above one is *claimed* for the
scheme, so the intent is defensible, but the phrase as written is
self-inconsistent on first read. No numeric error: all listed values match my
recomputation exactly.

**No finding:** I found no wrong factor, no sign error, no unreproducible
number, and no overstatement of a spatial/factor order. Every quantity I could
independently recompute matched (MMS forcing, MMS orders, one-element states,
reference coefficients, discrete balances, suite counts, figure provenance).

## 4. Required corrections

1. **Fix or remove the Jacobian step-refinement evidence (F1).** Required
   because `validation/reference-data/verification-contract.md` §1 explicitly
   requires recording a Jacobian *step-refinement* study, and the current
   three-run set does not demonstrate one (the varied option is unused, and
   the outputs are identical). Either re-run with a recognized FD-perturbation
   control (`-snes_test_jacobian` already reports
   `||J-Jfd||_F/||J||_F`; vary a supported option or record the reported
   values into a machine-readable `analysis.json`), or drop the three runs and
   state the single measured 2.4e-7 result. This is required for the evidence
   set to support the contract it is listed under.

2. **Correct `reference_comparable` / the reference-normalized fields for the
   anisotropic and isotropic full-domain runs (F2).** Required because the
   artifact asserts comparability that is false on the material (K=7, phi=0.6,
   G~10.08 vs the reference K=1, phi=0.9, G=0.75), and the emitted
   `reference_comparison.csv` / `*_normalized` numbers are then meaningless.
   Set the flag false (and stop emitting the Mandel-normalized fields) for any
   case whose moduli differ from `MandelParameters()`, or supply the matching
   reference. This is required so that `site/evidence.json`, advertised as the
   pinned verification-evidence file, does not misrepresent these runs.

## 5. Optional suggestions

- Reword the `site/evidence.json` convergence sentence (F3) to e.g. "measured
  successive-difference orders, including ux ≈ 1.4, are not claimed as the
  scheme's order; no order above one is asserted."
- `fe-evidence/manifest.json` lists several `*/reference_comparison.csv` and
  the `jacobian_*` files under `missing`; consider documenting that these are
  intentionally absent so the "missing" list is not read as a defect.
- Consider shipping the finite-map sample CSVs (`fe_map_*_samples.csv`) that
  `plot_fe_results.py` generates, so the map figures are backed by data in
  `figures/` like the other figures.

## 6. Review limitations

- No MOOSE binary is present in the snapshot. All coupled results were audited
  by re-deriving from the recorded `solution.csv` / `analysis.json` /
  `run.log` and from the paper equations; I did not re-run the solver, so a
  discrepancy between the shipped binary and the shipped sources cannot be
  ruled out by execution (source hashes in each `provenance.json` are however
  internally consistent with the snapshot's `moose_app/` hashes).
- The Exodus `.e` fields themselves are not in the snapshot, so the finite-map
  images (`fe_map_*.png`) were not re-derived, only their captions/inputs
  checked.
- The Mandel analytical series (`validation/mandel_reference.py`) was checked
  for internal consistency (Biot 0.6, storage 17/80, G=0.75, root ratio,
  Skempton B, overshoot 5.47% at t≈0.0152) rather than re-implemented from
  Cheng-Detournay ab initio.
- My independent constitutive re-derivations use the same plane-strain,
  total-Lagrangian conventions stated in the paper; I did not test the
  three-dimensional kernel path beyond the plane-strain reduction.

VERDICT: MINOR REVISION
