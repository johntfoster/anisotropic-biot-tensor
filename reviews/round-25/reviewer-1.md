# Round 25 — Reviewer 1 (mathematics / correctness)

Independent manuscript-acceptance review of the frozen round-25 snapshot of the
anisotropic pore-fabric extension. Scope: `sections/pore_fabric.tex`,
`sections/finite_elements.tex`, `sections/limits.tex`,
`sections/stress_reconstruction.tex`, `sections/logarithmic_derivative.tex`,
`main.tex`, `moose_app/include/utils/FabricLaw.h` (+ `ConformalLaw.h`),
`examples/verify_fabric.py`, `fe-evidence/`, `validation/`.

Prior-round reports and the other round-25 reviewers' reports were not read.
The snapshot and working tree were not modified; every script below was run
from a temporary copy created with `mktemp -d` (`/tmp/r25rev1.UwwiJR`), and
`diff` confirms the in-scope working-tree files are byte-identical to the
snapshot.

---

## 1. Snapshot integrity

Two independent commands, run from the repository root:

```
sha256sum .agent-runtime/review-snapshots/round-25/source-manifest.json
python3 <inline script>   # re-hash every manifest entry against the snapshot
```

| Check | Result |
|---|---|
| `sha256(source-manifest.json)` | `5035dd198266c12544140e47381da3e9390c7d1e68c00a06009e85ba6052f9dd` |
| Declared `SNAPSHOT_ID` (file `.../round-25/SNAPSHOT_ID`) | `5035dd198266c12544140e47381da3e9390c7d1e68c00a06009e85ba6052f9dd` |
| Manifest digest vs declared ID | **MATCH** |
| Manifest entries | 591 |
| Re-hash OK / MISSING / MISMATCH | **591 / 0 / 0** |

Secondary evidence artifacts also re-hash clean:

| Check | Command | Result |
|---|---|---|
| `build/main.pdf` sha256 | `sha256sum build/main.pdf` (in snapshot) | `12fc90c4…1ad8ad` — matches the digest declared in `LAUNCH-STATE.md` |
| PDF page count / build log | `pdfinfo build/main.pdf`; `grep -c undefined build/main.log` | 33 pages; 0 undefined references or citations; 0 overfull boxes |
| `fe-evidence/manifest.json` digests | re-hash of all 317 shipped `files[]` entries (paths relative to `fe-evidence/`) | **317 OK / 0 MISSING / 0 MISMATCH** |

Integrity line: **SNAPSHOT_ID verified — 591/591 manifest files re-hash OK, 0 missing, 0 mismatched; no integrity defects.**

The two Foster-cycle edits are present and are prose-only:
`grep -rn "transverse-isotropic" main.tex sections/` returns nothing while
`transversely isotropic` appears in `main.tex` (conclusions) and
`sections/pore_fabric.tex`; `grep -rn "eigenvalue ratio" main.tex sections/`
returns nothing, and both places that describe the shape scalar now say it is
"the logarithm of the unimodular transverse fabric eigenvalue
\(h=\mathrm{e}^{\ln h}\)" consistent with `eq:fabric-transverse-h`. No
equation, symbol, label, citation, or number differs between the snapshot and
the previous content in any way I can detect (`\label`/`\ref` integrity: 138
labels, 21 distinct referenced labels, **0 missing references**).

---

## 2. Independent mathematical re-derivation

Every item below was recomputed from scratch (own scripts, not by importing
the shipped checker) or re-run from the frozen artifacts.

**(a) Tensorial distention kinematics.** `eq:fabric-distention-polar`,
`eq:fabric-volume-ratio`, `eq:fabric-multiplicative`,
`eq:fabric-mineral-metric` all verify algebraically; I re-checked
\(\bar{\mathbf C}=\mathbf F^T\mathbf R_A\mathbf G^{-1}\mathbf R_A^T\mathbf F\)
and the conformal specialization
\(\mathbf G=a^{2/3}\mathbf I\Rightarrow\bar{\mathbf C}=a^{-2/3}\mathbf C\).

**(b) Fabric tensor and the logarithmic-strain relation.** For 20 random
states \((a,h,\mathbf m)\),
\(\mathbf H=h^{-2}\mathbf m\otimes\mathbf m+h(\mathbf I-\mathbf m\otimes\mathbf m)\)
has \(\det\mathbf H-1\) and
\(\lVert\exp(2\mathbf E_{\mathrm{dis}})-\mathbf G\rVert\) both \(\le 6.7\times10^{-16}\),
with \(\mathbf E_{\mathrm{dis}}\) exactly as in `eq:fabric-transverse-strain`.
The reconstruction is exact, not a projection: the eigenvalues of \(\mathbf H\)
are \(h^{-2},h,h\). I also confirmed the sign/basis convention in
`FabricLaw.h` (`e2 = sqrt(3/2)(m⊗m - I/3)`, `ln_h = -x2/sqrt(1.5)`) reproduces
the same \(\mathbf H\), so the reported `ln_h` **is** the manuscript's
\(\ln h\).

**(c) Phase work and the contraction ordering.** I re-derived
`eq:fabric-virtual-deformation` and `eq:fabric-phase-work` from
\(\delta\mathbf F\mathbf F^{-1}\), and checked numerically (2000 random
states with **non-symmetric** \(\delta\bar{\mathbf F}\bar{\mathbf F}^{-1}\))
that the manuscript's second term
\(\phi_{s0}\,\mathbf G^{1/2}\hat{\boldsymbol\tau}_s\mathbf G^{-1/2}:(\delta\bar{\mathbf F}\bar{\mathbf F}^{-1})\)
is the correct ordering: worst deviation from the direct work expression
\(8.9\times10^{-15}\), whereas the reversed ordering
\(\mathbf G^{-1/2}\hat{\boldsymbol\tau}_s\mathbf G^{1/2}\) fails by
\(2.8\times10^{1}\). The ordering matters here and the manuscript has it right.

**(d) Draining restriction — both forms are equivalent and correct.** Using
an independent energy route (minimise \(W_A+\phi_{s0}\bar W_s+\phi_{s0}p\bar J\)
over \(\ln a\), then form \(\mathbb C^d\) exactly from the quadratic form), I
reproduced
`eq:drained-stiffness-restriction` and `eq:drained-compliance-restriction` to
\(\le 9\times10^{-16}\) for both an isotropic and a genuinely anisotropic
(tetragonal) mineral, and for \(K\in\{0.3,0.5,0.8\}\); the two displayed forms
are mutual inverses (Sherman–Morrison) and both agree with the energy. The
Moore–Penrose statements check out: for the rank-two axisymmetric
generalisation, \(\mathbb D\mathbb D^+\mathbb D=\mathbb D\),
\(\mathbb D^+\mathbb D\mathbb D^+=\mathbb D^+\), and

```
|| C^d_energy - [(phi_s0 C_s)^-1 + D^+]^-1 ||  <= 1.1e-15
```

for three independent \((k_v,k_a,k_c,\mathbf m)\) sets, confirming
`eq:fabric-compliance-restriction` on the retained subspace.

**(e) Equilibrium conditions.** The linear system solved in `FabricLaw.h`,
\((\mathbb D_d+\phi_{s0}G)x=\phi_{s0}(g+p\sqrt3\hat e_1)\), is the exact
stationary point of the manuscript potential: the residual gradient at the
code's solution is \(3.5\times10^{-18}\) for three fabric orientations. The
manuscript's mineral EOS (`eq:anisotropic-mineral-eos`) is algebraically
equivalent to that stationarity condition, and the p=0 reduction reproduces
`eq:drained-distention-volume-matching` and `eq:drained-anisotropic-distention`
exactly. The unique-root and stability-domain arguments
(`eq:trace-mineral-stability-domain`) are correct: the right-hand side is
strictly increasing in \(\ln\bar J\) for \(p\ge0\) with limits \(-\infty\) and
\(+\infty\).

**(f) Biot tensor.** \(\mathbf B=\mathbf I-\mathbb C^d:\mathbb C_s^{-1}:\mathbf I\)
was recomputed independently: it reduces exactly to \((1-K/K_s)\mathbf I\) for
an isotropic mineral, is transversely isotropic
(\(B_\parallel\mathbf m\otimes\mathbf m+B_\perp(\mathbf I-\mathbf m\otimes\mathbf m)\))
for a transversely isotropic fabric, and \(B_\parallel-B_\perp\to0\) when the
fabric is isotropic (`no_coupling` and `frozen_shape` limits:
anisotropy \(\le1.1\times10^{-16}\)). The reference components in
`sections/experiments.tex` reproduce exactly from the restriction:
\(K_s=28\), \(\mathbf B_0=(0.7000,0.7583,0.7917)\) (my values
0.700000, 0.758333, 0.791667).

**(g) Storage and the unjacketed path.** The manuscript's total storage
equals the classical Biot value
\(1/M=(1-\phi_{s0})/K_f+(\alpha-\phi_{f0})/K_s\) identically
(\(0.2125=17/80\) for the reference moduli), and
`eq:reference-solid-storage` follows from implicit differentiation of the
mineral EOS. The finite unjacketed state
(`eq:reconstructed-finite-unjacketed-path`) satisfies the mineral EOS to
\(<6\times10^{-17}\) **and** the phase balance for both an isotropic and the
anisotropic example mineral — the claim in `limits.tex` is correct, including
the anisotropic case where \(C_s^{-1}:\mathbf I\) is not spherical.

**(h) Logarithmic-derivative appendix.** The spectral Fréchet formula
(`eq:log-frechet-spectral-form`), its repeated-eigenvalue limit, self-adjointness,
the trace identity \(\operatorname{tr}\boldsymbol\tau=\operatorname{tr}\mathbf T\)
(`C :[\partial\log\mathbf C/\partial\mathbf C:\mathbf T]=\operatorname{tr}\mathbf T`,
verified to \(1.8\times10^{-15}\) over random states), and the statement that
\(\mathbf T=\mathbf I\) maps to the spatial identity, all verify.

**(i) Shipped code (`FabricLaw.h`, `ConformalLaw.h`).** The Mandel conventions,
\(\mathbb D^+\) assembly, `cdm = inv(inv(phi*cs)+Dp)`, `bvec = eI - cd:cs^-1:eI`,
`storage = (1-phi)/Kf + (phi/Ks)(1-Kd/(phi*Ks))`, and the equilibrium operator
are consistent with the manuscript. `ConformalLaw.h`'s
\(\mathbf C^d=\phi\mathbf C_s-(\phi\alpha/(9K_s))(\mathbf C_s:\mathbf I)\otimes(\mathbf C_s:\mathbf I)\)
and its `cd:cs^-1:I = phi I - phi alpha/(3 Ks) Cs:I` identity are the
manuscript's equations verbatim; its nonlinear mineral-root Newton lift and
the Gauss–Legendre evaluation of
\(\int_0^1(\mathbf I+x\mathbf D)^{-1}\mathbf T(\mathbf I+x\mathbf D)^{-1}\mathrm dx\)
reproduce the matrix-logarithm derivative correctly (the integrand's
\(i\ne j\) entry integrates to \((\ln\lambda_i-\ln\lambda_j)/(\lambda_i-\lambda_j)\)).

---

## 3. Reproduction of every quoted number

Re-run from a temporary copy (authoritative-source rule: these are files on
disk, and the commands below are exactly what produced each number).

| Manuscript value | Provenance | Command | Reproduced |
|---|---|---|---|
| reconstruct \(2.2\times10^{-16}\), \(\det\mathbf H-1=-3.3\times10^{-16}\), \(\lVert\mathbb D:\mathbf e_3\rVert=1.6\times10^{-16}\), \(\mathbb D:\mathbf e_6=0\), rotation \(2.5\times10^{-16}\), worst probe diff \(4.9\times10^{-15}\), conformal reduction \(1.9\times10^{-14}\) | `examples/verify_fabric.py` vs `fe-evidence/runs` | `python3 examples/verify_fabric.py --runs fe-evidence/runs` | 2.220e-16 / -3.331e-16 / 1.582e-16 / 0.0 / 2.497e-16 / 4.885e-15 / 1.874e-14 — all ✓ |
| shipped vs my re-run of that script | `build/fabric/fabric-verification.json` | element-wise diff of the two JSON files | 0 differences ✓ |
| MMS spatial orders 2.00/2.00, 2.99/2.96, 3.00/2.96 | `fe-evidence/mms-convergence.json` | `python3 fe-evidence/compute_mms_order.py --runs fe-evidence/runs --out …` then diff vs shipped | 1.9966/2.0008, 2.9917/2.9585, 2.9983/2.9600; **file identical** ✓ |
| temporal orders 0.98–1.40 | same JSON (`difference_orders`) | same command | min 0.9783, max 1.3969 ✓ |
| linear step ratio 1.94; 3.7e-3 and 7.1e-3 at dt=1e-3, 2e-3 | `runs/linear_time_0.001,0.002/analysis.json` | `pressure_max_normalized` 0.0036580 / 0.0071039 → ratio 1.9420 | ✓ |
| floor \(3.2\times10^{-3}\) at \(nx=20\), \(dt=10^{-3}\) | `runs/nonlinear_load_0.0001/analysis.json` (`nx=20 ny=2 dt=0.001` confirmed from `input.i`) | value 0.0032209 | ✓ |
| peak centre pressures 4.36 / 4.99 / 5.52 / 3.62 \(\times10^{-5}\) | `runs/fabric_mandel_coup_a0,a45,a90,iso/solution.csv` | `center_pressure` last row: 4.3628e-5 / 4.9901e-5 / 5.5211e-5 / 3.6164e-5 | ✓ |
| peaks are the final state, not overshoot | same files | last row is the column maximum in all four cases | ✓ |
| contour pressures 3.61 / 4.35 / 4.97 / 5.50 \(\times10^{-5}\) | `runs/fabric_contour_*/analysis.json` | 3.6062e-5 / 4.3491e-5 / 4.9727e-5 / 5.5031e-5 | ✓ |
| contour \(|\mathbf u|\) 5.18 / 5.14 / 2.38 / 5.26 \(\times10^{-5}\) | `runs/fabric_contour_*/solution.e` | `netCDF4`: \(\max\sqrt{u_x^2+u_y^2}\) on the last step = 5.1826e-5 / 5.1372e-5 / 2.3818e-5 / 5.2587e-5 | ✓ |
| "maximum lies on the \(X_1=0\) symmetry line" | same files | argmax of \(p\) at \(x=0.0000\) in all four | ✓ |
| \(40\times8\) mesh, eleven evenly spaced snapshots | `fabric_contour_*/input.i`, `solution.e` | `nx=40 ny=8 dt=0.0003 end_time=0.003`; Exodus has 11 time steps | ✓ |
| "same deck with the volume–axial coupling switched off" | `fabric_mandel_*/input.i` + `provenance.json` | decks byte-identical; override `Materials/law/fabric_coupling=0` | ✓ |
| "same boundary conditions, material …, time integration, but a smaller step" | `diff fabric_mandel_coup_a45/input.i fabric_contour_a45/input.i` | differs only in mesh, `dt`, comments, and removal of the line sampler | ✓ |
| reference coefficients \(\phi_{s0}=0.9, K_s=2.5, \mu_s=5/6, K=1, K_f=8, k/\mu_f=1.5\), \(G=0.75\), \(B_0=0.6\), storage \(17/80\) | `runs/*/input.i`; my own computation | \(G=\phi_{s0}\mu_s=0.75\); \(1-K/K_s=0.6\); \((1-\phi)/K_f+\phi\alpha/K_s=0.2125=17/80\) | ✓ |
| Mandel "independently evaluated series" | `validation/mandel_reference.py` re-run | `python3 mandel_reference.py --self-check` → all gates pass; re-evaluating the series at the recorded times reproduces `reference_comparison.csv` to \(1.4\times10^{-20}\) | ✓ |
| `eq:example-mineral-stiffness`, reference Biot 0.7000/0.7583/0.7917 | my own computation | as above | ✓ |
| MMS exact solution \(U=P_0=0.01\), 30° rotated stiffness, unit square, Dirichlet on all boundaries | `runs/mms_space_8/input.i` | ParsedFunctions match `eq:fe-mms-u1…pressure`; `angle = 30`; `[0,1]^2` QUAD9 | ✓ |
| `examples/verify_*.py`, `weighted_stress.py`, `validation/mms_reference.py` execute | temp copy | all exit 0 (`verify_reconstruction.py`: 20/20 incompatible pairs rejected, min drained eigenvalue 1.84; `verify_conformal.py`: observed orders ≈2.00) | ✓ |

No quoted number failed to reproduce. Nothing in the shipped evidence is
inconsistent with the text it supports.

---

## 4. Findings

**Finding 1 — OPTIONAL (prose precision).**
`sections/finite_elements.tex` (panel (b) description) says the temporal
orders "lie near one and include one above one", while the recorded
`difference_orders` are 0.978, 1.015, 1.018, 1.076, 1.093, 1.125, 1.252,
1.396, 1.397 — i.e. several exceed unity. The conclusions already say
"including values above one", and the operative claim ("no order above one is
asserted") is conservative and honest, so this is a wording nit only.

**Finding 2 — OPTIONAL (shipped-code consistency).**
`FabricLaw.h` reports `s.stability = Ks` (a constant \(2.5\)), whereas
`ConformalLaw.h` reports the pressure-dependent branch derivative
\(K_s+\alpha p\bar J\) of `eq:trace-mineral-stability-domain`. The fabric
material is documented (and enforced at run time) as the reference-state
linearization, and the manuscript never quotes the fabric material's
`stability` field as a claim, so no manuscript statement is affected; the two
materials simply expose the same auxiliary name with different content. Worth
a one-line comment in `FabricLaw.h` if the field is ever read as evidence.

**Finding 3 — OPTIONAL (implementation note).**
`FabricLaw.h` sets the first Piola stress equal to the small-strain stress
(`s.P = sig`) and refuses to evaluate unless `linear_reference = true`. This
is the correct small-strain total-Lagrangian convention for the reference
tangent the material implements (the same convention is recorded in
`validation/equation_to_moose_map.yml`), but it is not the general
\(\mathbf P=J\boldsymbol\sigma\mathbf F^{-T}\) of `eq:fe-total-first-piola`.
Since the fabric runs are all reference-state linearizations, no run is
affected; a short comment would prevent misreading.

No REQUIRED corrections were identified. I specifically looked for and could
not substantiate: a wrong sign or factor in the distention work, the
compliance/stiffness restriction or the Biot tensor; a failure of
\(\det\mathbf H=1\) or of the exactness of `eq:fabric-transverse-strain`; a
non-equivalence of the two displayed restriction equations; a failure of the
rank-two Moore–Penrose generalisation; a spurious "eigenvalue ratio" claim
(the R24-3-1 defect is genuinely closed); a number that does not reproduce.

---

## 5. Overall assessment

The mathematical content is correct and internally consistent. I re-derived
or independently re-checked every core claim in scope — the tensorial
distention construction, the unimodular fabric tensor
\(\mathbf H=h^{-2}\mathbf m\otimes\mathbf m+h(\mathbf I-\mathbf m\otimes\mathbf m)\),
the logarithmic-strain relation, the drained compliance restriction in both
its stiffness and compliance forms, the equilibrium conditions, the Biot
tensor and its isotropic/transverse-isotropic limits, and the storage and
unjacketed relations — and all agree to machine precision with the shipped
equations. The rank-two axisymmetric generalisation of the restriction
verifies exactly from the energy, and the code's contraction orderings are
the correct ones. The snapshot is intact (591/591), the two Foster-cycle
edits are present and prose-only, and every quoted numerical result
reproduces from the frozen `fe-evidence/` artifacts and the supplied
verification and validation scripts. The three findings above are optional
prose/comment-level clarifications and do not affect any equation, number, or
claim.

VERDICT: ACCEPT
