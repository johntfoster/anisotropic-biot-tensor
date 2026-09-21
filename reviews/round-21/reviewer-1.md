# Round-21 independent peer review — Reviewer 1

**Manuscript:** `main.tex`, "An anisotropic Biot tensor from mineral stress and distention work"
**Snapshot under review:** `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/review-snapshots/round-21`
**Declared SNAPSHOT_ID:** `f4c43aeea1590c8e166d3ffab342e5da92094443e55b4df4d47b69bbad8c673f`
**Emphasis:** mathematics and correctness. Independent re-derivation of the tensorial-distention
(tensorial Biot / pore-fabric) extension: the distention deformation gradient, the fabric-dependent
Biot tensor, the drained-stiffness restriction, and the transverse-isotropic special case; every
numbered equation in `sections/pore_fabric.tex`; the MOOSE law (`FabricLaw.h`, `FabricMaterial.C`)
including the `ln_h` sign convention; and the verification artifacts (`build/fabric/fabric-verification.json`,
`examples/verify_fabric.py`, `fe-evidence/runs/*`).

Comment IDs are stable and tied to a location (`file:line`, equation label). REQUIRED items each carry a
demonstrated defect with a location and a reproducible computation. Scratch work was done in `/tmp/r21rev1`
(a Python re-implementation of `FabricLaw.h` that reproduces the recorded material-point outputs to
machine precision, plus independent checks). Nothing in the snapshot was modified.

---

## 1. Snapshot integrity (INT-1)

| Check | Result |
|---|---|
| `sha256(snapshot/source-manifest.json)` vs declared SNAPSHOT_ID | **match** (`f4c43aee…c673f`) |
| Manifest entries re-hashed | **549 / 549 match**, 0 missing, 0 hash mismatches |
| Files on disk not listed in the manifest | 2 — `source-manifest.json` and `SNAPSHOT_ID` (self-referential; expected) |
| Unexplained / missing files | none |

The snapshot tree is read-only (directories `0555`, files `0444`). I read it only and wrote no file inside it.

## 2. Independent re-derivation: what is correct

I re-derived the extension from the stated postulates and reproduce the compiled law numerically. The
following are **confirmed correct**; I record them so the fixes below are not over-extended.

- **Kinematics.** `eq:fabric-distention-polar`, `eq:fabric-volume-ratio`, `eq:fabric-multiplicative`,
  `eq:fabric-mineral-metric` are correct for $\mathbf A=\mathbf R_A\mathbf G^{1/2}$: $\mathbf G=\mathbf A^T\mathbf A$,
  $a=\det\mathbf A=(\det\mathbf G)^{1/2}$, $\bar{\mathbf C}=\mathbf F^T\mathbf R_A\mathbf G^{-1}\mathbf R_A^T\mathbf F$,
  and the conformal specialization $\mathbf G=a^{2/3}\mathbf I$ gives $\bar{\mathbf C}=a^{-2/3}\mathbf C$.
- **Fabric tensor.** `eq:fabric-tensor`, $\mathbf H=(\det\mathbf G)^{-1/3}\mathbf G$, $\mathbf G=a^{2/3}\mathbf H$, is correct.
- **Distention work.** `eq:fabric-distention-stress` ($\bar{\mathbf S}_d=2\,\partial W_d/\partial\mathbf G$,
  $\delta W_d=\tfrac12\bar{\mathbf S}_d{:}\delta\mathbf G$) and its equivalence with
  $\mathbf E_d=\tfrac12\ln\mathbf G$ are consistent (the matrix-log derivative is self-adjoint in the trace metric).
- **Virtual work.** `eq:fabric-virtual-deformation` is exactly $\delta\mathbf F\mathbf F^{-1}$ for
  $\mathbf F=\mathbf R_A\mathbf G^{1/2}\bar{\mathbf F}$; the skew term drops against $\boldsymbol\tau'$, and
  `eq:fabric-phase-work` follows from the phase balance `eq:constitutive-kirchhoff-phase-stress`
  (I re-checked both contracted terms; the $G^{1/2}\widehat{\boldsymbol\tau}_sG^{-1/2}$ and
  $G^{-1/2}\widehat{\boldsymbol\tau}_sG^{1/2}$ forms are equal under the double contraction).
- **Transverse-isotropic strain.** `eq:fabric-transverse-strain`
  $\mathbf E_d=\tfrac{\ln a}{3}\mathbf I+\ln h\,(\tfrac12\mathbf I-\tfrac32\mathbf m\otimes\mathbf m)$ is correct
  for `eq:fabric-transverse-h`: $\ln\mathbf H=\ln h\,(\mathbf I-3\mathbf m\otimes\mathbf m)$.
- **`ln_h` sign convention.** With $\mathbf e_2=\sqrt{3/2}\,(\mathbf m\otimes\mathbf m-\mathbf I/3)$,
  $\tfrac12\mathbf I-\tfrac32\mathbf m\otimes\mathbf m=-\sqrt{3/2}\,\mathbf e_2$, so $x_2=-\sqrt{3/2}\,\ln h$, i.e.
  $\ln h=-x_2/\sqrt{1.5}$. `FabricLaw.h:607` (`s.ln_h = -xi/std::sqrt(1.5)`) **is** the manuscript's $\ln h$
  (not its negative) *when $\mathbf E_d\in\operatorname{span}(\mathbf e_1,\mathbf e_2)$*. The reported sign is right;
  see MAT-2 for the proviso.
- **Reference Biot tensor.** `eq:reference-biot-compatibility`, $\mathbf B_0=\mathbf I-\mathbb C^d{:}\mathbb C_s^{-1}{:}\mathbf I$,
  is what `FabricLaw.h` computes, and `eq:fabric-transverse-biot` holds **exactly** in the implementation: for the
  coupled probes I get $\lVert\mathbf B-(B_\parallel\mathbf m\otimes\mathbf m+B_\perp(\mathbf I-\mathbf m\otimes\mathbf m))\rVert=1.1\times10^{-16}$.
- **Reported numbers.** The abstract/conclusion values reproduce from the artifacts: material-point worst
  difference $4.885\times10^{-15}$ (claimed $4.9\times10^{-15}$); conformal reduction vs the independent
  `ConformalMaterial` worst $1.87\times10^{-14}$ (claimed $1.9\times10^{-14}$); coupled peak centre pressures
  $6.280\times10^{-5}/5.102\times10^{-5}/3.946\times10^{-5}/5.133\times10^{-5}$ (claimed
  $6.28/5.10/3.95/5.13\times10^{-5}$); constant-tangent pressure errors $3.658\times10^{-3}$ and $7.104\times10^{-3}$
  at $dt=10^{-3},2\times10^{-3}$ (ratio $1.94$); nonlinear load floor $3.221\times10^{-3}$ at load $10^{-4}$.

## 3. REQUIRED changes

### MAT-1 — The implemented distention stiffness is **not** transversely isotropic, contrary to `sections/pore_fabric.tex` and the traceability map

**Locations.** `sections/pore_fabric.tex:260-264` ("the five-modulus *transversely isotropic* $\mathbb D$ implemented
in `sec:fe-fabric` …"); `sections/pore_fabric.tex:308` ("The drained compliance `eq:fabric-compliance-restriction`
is then *transversely isotropic*"); `moose_app/include/utils/FabricLaw.h:469-474` (the `dd` block);
`validation/equation_to_moose_map.yml` (`FabricMaterial` lists `eq:fabric-transverse-h` … `eq:fabric-transverse-biot`).

**Defect.** Under rotations about the fabric axis $\mathbf m$, the Mandel directions
$\mathbf e_3=(\mathbf p_1\otimes\mathbf p_1-\mathbf p_2\otimes\mathbf p_2)/\sqrt2$ and
$\mathbf e_6=\sqrt2\,\operatorname{sym}(\mathbf p_1\otimes\mathbf p_2)$ transform into each other
($\mathbf e_3\mapsto\cos2\varphi\,\mathbf e_3+\sin2\varphi\,\mathbf e_6$, $\mathbf e_6\mapsto-\sin2\varphi\,\mathbf e_3+\cos2\varphi\,\mathbf e_6$):
they span a two-dimensional irreducible subspace. Transverse isotropy about $\mathbf m$ therefore **requires**
$\mathbb D{:}\mathbf e_3=\mathbb D{:}\mathbf e_6$ (a scalar on that pair). The constructor sets
`dd[2][2] = fabric_inplane_modulus` and assigns **no** entry on $\mathbf e_6$ (`FabricLaw.h:439-444, 469-474`), so
$\mathbb D{:}\mathbf e_6=\mathbf 0$ while $\mathbb D{:}\mathbf e_3=k_i\mathbf e_3$.

**Evidence (reproducible).** From my `/tmp` re-implementation of `FabricLaw.h`:
$\lVert\mathbb D_4-\mathbf R\mathbb D_4\mathbf R^{\!\top}\rVert=4.33\times10^{-1}$ for a $30^\circ$ rotation about
$\mathbf m$ (zero would be TI); $\mathbb D_4{:}\mathbf e_6=\mathbf 0$ while
$\mathbb D_4{:}\mathbf e_3=(0,0.707,-0.707,0,0,0)$; the recovered drained stiffness is equally non-TI,
$\lVert\mathbb C^d-\mathbf R\mathbb C^d\mathbf R^{\!\top}\rVert=3.90\times10^{-1}$ (the `drained_c11`/`drained_c12`
path). The implemented tensor has the lower symmetry of the fixed triad $\{\mathbf m,\mathbf p_1,\mathbf p_2\}$
(orthorhombic-like), not transverse isotropy, and calling it "the five-modulus transversely isotropic $\mathbb D$"
is therefore incorrect. The kernel sentence on `pore_fabric.tex:264` ("the in-plane shear
$\operatorname{sym}(\mathbf p_1\otimes\mathbf p_2)$ frozen to the mineral compliance") describes an artifact of this
non-TI construction, not a consequence of transverse isotropy.

**Required action.** Either (a) give $\mathbb D$ its transverse-isotropic form, i.e. let the $(\mathbf e_3,\mathbf e_6)$
block be $k_{\rm ip}\mathbf I_2$ (this makes $\mathbb D$ full rank and removes the "frozen mode" discussion, see MAT-3),
or (b) state the symmetry actually used and drop/qualify the "transversely isotropic $\mathbb D$" and "drained compliance
is then transversely isotropic" claims. If (a) is chosen, the coupled decks must be re-run, because the deformation
(fabric) response on in-plane-shear-dominated states changes (the reference Biot values do not: I verified $\mathbf B$ is
insensitive to the $\mathbf e_6$ modulus, since $\mathbb D^{+}{:}\mathbf I\in\operatorname{span}(\mathbf e_1,\mathbf e_2)$).

### MAT-2 — The transverse-isotropic special case does not describe the implemented model; the reported `ln_h` is not the unimodular fabric eigenvalue ratio

**Locations.** `sections/pore_fabric.tex:278-296` (`eq:fabric-transverse-h`, `eq:fabric-transverse-strain`);
`sections/pore_fabric.tex:324` ("In the two-parameter energy used in `sec:fe-fabric` …");
`sections/finite_elements.tex` fig. `fig:fe-fabric-probe` caption ("with $h$ the unimodular fabric eigenvalue ratio");
`moose_app/include/utils/FabricLaw.h` (the 5-direction basis and the equilibrium solve).

**Defect.** `eq:fabric-transverse-h`/`eq:fabric-transverse-strain` force
$\mathbf E_d=(\ln a/3)\mathbf I+\ln h(\tfrac12\mathbf I-\tfrac32\mathbf m\otimes\mathbf m)$, i.e.
$\mathbf E_d\in\operatorname{span}(\mathbf e_1,\mathbf e_2)$, so $\mathbf H$ has the two-fold in-plane eigenvalue.
The compiled law minimizes over $\operatorname{span}(\mathbf e_1,\dots,\mathbf e_5)$ (the 5$\times$5 block
`dd[i][j]+phi*g`, `FabricLaw.h`), so the equilibrium $\mathbf E_d$ generally lies outside
$\operatorname{span}(\mathbf e_1,\mathbf e_2)$. Consequently (i) the implemented $\mathbf H$ is not of the form
$h^{-2}\mathbf m\otimes\mathbf m+h(\mathbf I-\mathbf m\otimes\mathbf m)$, and (ii) the reported `ln_h` ($=-\!x_2/\sqrt{1.5}$,
the $\mathbf e_2$ coefficient only) is not the fabric eigenvalue ratio plotted/claimed.

**Evidence (reproducible).** For the recorded probe `fabric_probe_coup_a45` ($\boldsymbol\varepsilon=\operatorname{diag}(0.01,-0.005,0)$,
$p=0.02$; `fe-evidence/runs/fabric_probe_coup_a45/input.i`) my re-implementation returns the same `ln_a=0.0113616622`
and `ln_h=0.0003569502` as the artifact, with $\mathbf E_d$ coefficients
$(6.559659\times10^{-3},\,-4.37173\times10^{-4},\,1.060660\times10^{-3},\,-6.363961\times10^{-3},\,0)$ in
$(\mathbf e_1,\dots,\mathbf e_5)$: $|x_3|+|x_4|$ exceeds $|x_2|$ by more than an order of magnitude, so $\mathbf E_d\notin
\operatorname{span}(\mathbf e_1,\mathbf e_2)$. At `fabric_angle=0` the computed $\mathbf H$ is
$\operatorname{diag}(1.0100502,\,0.9920319,\,0.9980020)$ — the two in-plane entries differ, so $\mathbf H$ is not TI
about $\mathbf m$ even in the aligned case. For the three *uncoupled* probes `fabric_probe_a0/a45/a90` the eigenvalues of
$\mathbf H$ are **identical** ($0.9920319,0.9980020,1.0100502$) while the reported `ln_h` takes three different values
($-0.005$, $-0.0005$, $+0.004$); the plotted scalar therefore cannot be "the unimodular fabric eigenvalue ratio".
Finally, "the two-parameter energy used in `sec:fe-fabric`" is in fact five-parameter: every fabric deck sets
`fabric_volume_modulus`, `fabric_axial_modulus`, `fabric_coupling`, `fabric_inplane_modulus`, `fabric_shear_modulus`
(e.g. `fe-evidence/runs/fabric_mandel_coup_a45/input.i:161-166`: $5.4,1,0.4,1,1$).

**Required action.** Reconcile `sec:fabric-transverse` with what is implemented and verified. Either restrict the
implementation to the 2-d.o.f. fabric ($\mathbf E_d\in\operatorname{span}(\mathbf e_1,\mathbf e_2)$) and re-run the probes,
or state that the implemented distention has five degrees of freedom, that $\mathbf H$ is then not of `eq:fabric-transverse-h`'s
form, and that `ln_h` is the $\mathbf e_2$ (axial-deviatoric) coefficient, not the unimodular eigenvalue ratio. Fix the
figure caption and the "two-parameter" wording accordingly. If the 5-d.o.f. model is retained, the
`validation/equation_to_moose_map.yml` entry for `FabricMaterial` should not claim `eq:fabric-transverse-h`/`-strain`/`-biot`.

### MAT-3 — The drained-compliance derivation presupposes an invertible distention stiffness; the relation actually used needs an unstated constraint on $\mathbf E_d$

**Locations.** `sections/pore_fabric.tex:243-253` ("With a quadratic … where $\mathbb D$ is the positive definite
distention stiffness … minimizing `eq:fabric-equivalent-energy` over $\mathbf E_d$ at fixed $\boldsymbol\varepsilon$ gives the
drained compliance $(\mathbb C^d)^{-1}=(\phi_{s0}\mathbb C_s)^{-1}+\mathbb D^{-1}$"); `sections/pore_fabric.tex:260-266`
(the Moore–Penrose $\mathbb D^{+}$ sentence); `eq:fabric-equilibrium`.

**Defect.** For the rank-5 $\mathbb D$ actually used, the *unrestricted* minimization is ill-posed: $W_d$ is flat along the
omitted in-plane-shear direction, so $W_d+\phi_{s0}\bar W_s+\phi_{s0}p\bar J$ is unbounded below (the mineral shear strain can
be absorbed at zero distention cost) and `eq:fabric-equilibrium` has no stationary point along that direction. The identity
$(\mathbb C^d)^{-1}=(\phi_{s0}\mathbb C_s)^{-1}+\mathbb D^{+}$ is not the inverse of the *minimized* stiffness but of the
*constrained* stiffness obtained when $\mathbf E_d\in\operatorname{range}(\mathbb D)$ (equivalently, when the complementary
mode is carried by the mineral). That constraint is never stated in the manuscript; `pore_fabric.tex:245` instead asserts
$\mathbb D$ is positive definite.

**Evidence (reproducible).** Scalar analog ($\mathbb D=\operatorname{diag}(d,0)$, $\mathbb C_s=c\mathbf I$,
$\phi$): the minimized stiffness is $\phi c\,d/(d+\phi c)$ on $\operatorname{range}\mathbb D$ and **exactly $0$** on the
kernel, whereas $\big[(\phi\mathbb C_s)^{-1}+\mathbb D^{+}\big]^{-1}$ equals $\phi c$ on the kernel — the two disagree
unless the constraint is imposed. In the full 6-D code the same holds, and the code is self-consistent under the
constrained reading: my re-implementation gives $\mathbb C^d{:}\boldsymbol\varepsilon=\phi\mathbb C_s{:}\bar{\boldsymbol\varepsilon}$
to $3\times10^{-18}$ on the probe states, and $\mathbb C^d=\operatorname{inv}\!\big((\phi_{s0}\mathbb C_s)^{-1}+\mathbb D^{+}\big)$
reproduces the `drained_c11`/`drained_c12` outputs. So the *formula* is right for the constrained model; the *derivation sentence*
is not, and `eq:fabric-equilibrium` as written does not admit the implemented $\mathbb D$.

**Required action.** State explicitly that $\mathbf E_d$ is restricted to the fabric's retained invariant subspace
($\operatorname{range}\mathbb D$) and that the complementary mode is kinematically frozen to the mineral, or use a full-rank
(generally non-degenerate) $\mathbb D$ so that the plain inverse in `eq:fabric-compliance-restriction` is correct as written
(see MAT-1, option (a)). Whichever is chosen, make the inverse/pseudoinverse statement and `eq:fabric-equilibrium` mutually
consistent.

## 4. OPTIONAL notes

- **OPT-1 (traceability).** `validation/theory_traceability.yml` contains no fabric/`FabricMaterial` entries at all
  (`grep -c fabric` = 0), whereas `validation/equation_to_moose_map.yml` covers the fabric law. Adding the fabric
  constitutive relations to `theory_traceability.yml` would make the extension traceable in the same file as the rest.
- **OPT-2 (scope wording).** `equation_to_moose_map.yml` records for `FabricMaterial`:
  `derivatives: linearized_reference_state_stationarity`, `approximation: reference_state_linearized_distention_energy_and_reference_biot_limit; general_finite_deformation_fabric_equilibrium_out_of_scope`,
  and `FabricLaw::evaluate` throws unless `linear_reference = true`. The abstract's "The tensorial distention law is
  implemented and checked at the material-point level" is therefore best read as its reference-state linearization; say so
  in the abstract as well as in `sec:fe-fabric`.
- **OPT-3 (basis labels).** `FabricLaw.h` labels $\mathbf e_4$ "axial shear" and $\mathbf e_5$ "in-plane shear", but
  $\mathbf e_5=\operatorname{sym}(\mathbf p_2\otimes\mathbf m)$ is also an axial (transverse) shear; the true in-plane
  shear is the omitted $\operatorname{sym}(\mathbf p_1\otimes\mathbf p_2)$. The manuscript's usage ("in-plane shear
  $\operatorname{sym}(\mathbf p_1\otimes\mathbf p_2)$") is the correct one; align the code comments.
- **OPT-4 (figure interpretability).** Because the uncoupled probes have orientation-independent $\mathbf H$ eigenvalues
  but orientation-dependent reported `ln_h` (MAT-2), panel (c) of `fig:fe-fabric-probe` would be more informative if it
  plotted a quantity that is well defined for the implemented model (e.g. the full $\mathbf H$, or its three eigenvalues).

## 5. Assessment

The conformal core of the paper (kinematics, phase-stress/work equivalence, the implicit mineral-volume equation, the
spherical rank-one compliance restriction, `eq:anisotropic-biot-explicit`, the reference and unjacketed limits) is
mathematically sound, and I found no error in it. The new pore-fabric extension, however, is stated for a
transverse-isotropic distention while the implemented and verified law is not transverse isotropic (MAT-1), its reported
`ln_h` is not the quantity the text and figure caption say it is (MAT-2), and the central compliance relation is derived
from an unrestricted minimization that is ill-posed for the rank-deficient $\mathbb D$ actually used (MAT-3). These are
correctness defects in the section that carries the paper's main new claim, and they are not repairable by wording alone:
they require re-deriving/re-stating the anisotropic section and reconciling it with the implementation and the recorded
evidence (possibly re-running the coupled decks). Everything else I checked — including all the quoted error levels and
peak pressures — is internally consistent.

VERDICT: MAJOR REVISION
