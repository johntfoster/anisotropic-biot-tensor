# SIMULATED AI PEER REVIEW — Reviewer 1 (derivation and correctness)

This is a simulated AI peer review, not journal peer review, and it confers no
acceptance. Round-35 snapshot reviewed read-only.

- Snapshot: `.agent-runtime/review-snapshots/round-35` (repository
  `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`).
- Declared SNAPSHOT_ID: `3e56fad609d38c3a6dd65c10e6aff3959ec7deaff3c21ba2b86448074ad1d886`.
- Seat: derivation and correctness.

---

## 1. Mandatory first checks

### 1.1 Manifest hash vs declared SNAPSHOT_ID

Command:

```
cd <snapshot> && sha256sum source-manifest.json && cat SNAPSHOT_ID
```

Result:

```
3e56fad609d38c3a6dd65c10e6aff3959ec7deaff3c21ba2b86448074ad1d886  source-manifest.json
3e56fad609d38c3a6dd65c10e6aff3959ec7deaff3c21ba2b86448074ad1d886
```

Both equal the declared `SNAPSHOT_ID` exactly. **PASS.**

### 1.2 Re-hash every manifest entry (and walk the tree)

Command (Python, run inside the snapshot):

```
python3 - <<'EOF'
import json,hashlib,os
root=os.getcwd(); man=json.load(open('source-manifest.json'))
bad=[];missing=[];ok=0
for rel,h in man.items():
    p=os.path.join(root,rel)
    if not os.path.isfile(p): missing.append(rel); continue
    d=hashlib.sha256(open(p,'rb').read()).hexdigest()
    if d!=h: bad.append((rel,h,d))
    else: ok+=1
listed=set(man)|{'source-manifest.json','SNAPSHOT_ID'}
present={os.path.relpath(os.path.join(dp,f),root) for dp,_,fn in os.walk(root) for f in fn}
print(len(man),ok,len(bad),len(missing),sorted(present-listed),len(present))
EOF
```

Result:

```
608 608 0 0 [] 610
```

- Entries in `source-manifest.json`: **608**
- Entries re-hashed and matching: **608**
- Hash mismatches: **0**
- Listed files missing on disk: **0**
- Files present but unlisted: **0**
- Total files on disk: **610** (= 608 listed + `source-manifest.json` + `SNAPSHOT_ID`, neither of which lists itself). **PASS.**

### 1.3 Independence declaration

I did **not** open any file under `reviews/` (including `reviews/README.md`),
and I did **not** read, list, glob, or `find` any other
`.agent-runtime/review-snapshots/round-*` directory, any other reviewer's
report, or any verdict/acceptance count. All manuscript, evidence, and
implementation reads were from `round-35` only. I have **no accidental
exposure to self-report**. The only writes I made were a copy of extracted PDF
text and scratch scripts under `/tmp`, and this report.

---

## 2. What I re-derived / re-verified (context for the findings)

All checks below were computed from the frozen snapshot only (`main.tex`,
`sections/*.tex`, `build/main.pdf` text, `moose_app/`, `figures/*.csv`,
`fe-evidence/`, `site/reports/*.json`, `validation/*.yml`). Numerical
recomputation used NumPy/SciPy in `/tmp`; I did not run `validation/` or
`examples/verify_*.py`.

- **Equation numbering resolved from `build/main.pdf`** (and cross-checked
  against source order): e.g. `eq:constitutive-kirchhoff-phase-stress` = (12),
  `eq:finite-biot-tensor` = (49), `eq:anisotropic-biot-explicit` = (52),
  `eq:drained-compliance-restriction` = (43), `eq:fabric-compliance-restriction`
  = (78), `eq:fabric-transverse-biot` = (82), `build/main.log` carries no
  `\newlabel` records.
- **Distention energy chain (31)–(33)**: verified $K\ln J=\phi_{s0}K_s\ln\bar J$,
  $\ln a=(1-K/(\phi_{s0}K_s))\ln J$, and
  $W_A=\frac{K}{2(1-K/(\phi_{s0}K_s))}(\ln a)^2$ by direct integration. PASS.
- **Drained stiffness (40)**: reproduced
  $\mathbb C^d=\phi_{s0}\mathbb C_s-\frac{\phi_{s0}\alpha}{9K_s}(\mathbb C_s{:}\mathbf I)\otimes(\mathbb C_s{:}\mathbf I)$,
  $\alpha=1-K/(\phi_{s0}K_s)$, from the total derivative of the energy. PASS.
- **Compliance restriction (43)**: reproduced
  $(\mathbb C^d)^{-1}-(\phi_{s0}\mathbb C_s)^{-1}=\frac{\alpha}{9K}\mathbf I\otimes\mathbf I$
  by Sherman–Morrison, and the conformal limit of (78) with
  $\mathbb D\propto\mathbf I\otimes\mathbf I$: $\mathbb D^{+}=\frac{1}{9d}\mathbf I\otimes\mathbf I=\frac{\alpha}{9K}\mathbf I\otimes\mathbf I$.
  PASS (the two routes agree).
- **Reference Biot (57)**: numerically $B_0=(0.7000000,0.7583333,0.7916667)$
  for the example mineral (83), matching the manuscript text and `bvec` in
  `ConformalLaw.h`. Isotropic reduction $(1-K/K_s)\mathbf I$. PASS.
- **Eq (52) vs definition**: finite-difference of the mineral EOS (37) gives
  $\mathbf B=\mathbf I-\frac{\phi_{s0}}{J}\partial_{\mathbf F}\bar J\,\mathbf F^{T}$;
  agreement with (52) to $3.4\times10^{-10}$ (finite-difference level) over three
  random anisotropic states, and $\mathbf B$ symmetric to $6\times10^{-18}$. PASS.
- **Eq (54)/(55)**: $\partial W'/\partial p|_{\mathbf F}=\phi_{s0}\bar J$ and
  $\partial\boldsymbol\sigma/\partial p|_{\mathbf F}=-\mathbf B$ reproduced from
  $\boldsymbol\sigma=J^{-1}\mathbf P'\mathbf F^{T}-p\mathbf I$. PASS.
- **Reference storage (59)/(60)**: $S_s=\phi_{s0}\alpha/K_s$ matches both the
  direct form and $\phi_{s0}\mathbf I{:}\mathbb C_s^{-1}{:}\mathbf I-\mathbf I{:}\mathbb C_s^{-1}{:}\mathbb C^d{:}\mathbb C_s^{-1}{:}\mathbf I$;
  FE reference total $=0.1/8+0.2=17/80=0.2125$, $B_0=1-1/2.5=0.6$. PASS.
- **Unjacketed path (63)/(64)**: with $\mathbb C_s{:}\boldsymbol\varepsilon=-pJ\mathbf I$,
  $a=1$, $J=\bar J$, the mineral EOS (37) reduces to
  $[K_s-K/\phi_{s0}-\alpha K_s]\ln J=0$, which vanishes identically; hence
  $\boldsymbol\sigma=-p\mathbf I$, $\phi_s=\phi_{s0}$. PASS.
- **Fluid coupling (93)**: $\delta m_f|_p=\bar\rho_f J\mathbf B{:}(\delta\mathbf F\mathbf F^{-1})$
  reproduced via $\partial\bar J/\partial\mathbf F=(J/\phi_{s0})(\mathbf I-\mathbf B)\mathbf F^{-T}$. PASS.
- **Fabric basis $e_1..e_6$**: Gram matrix $=\mathbf I$ to $10^{-16}$;
  $\operatorname{tr}e_1=\sqrt3$, other traces $0$; $\mathbb D$ block structure
  gives $\mathbb D{:}e_3=\mathbb D{:}e_6=0$. PASS.
- **Transverse strain (80)**: $\exp(2\mathbf E_{\mathrm{dis}})=a^{2/3}\mathbf H$
  with $\mathbf H=h^{-2}\mathbf m\otimes\mathbf m+h(\mathbf I-\mathbf m\otimes\mathbf m)$
  reproduced to $1.1\times10^{-16}$, $\det\mathbf H-1\approx10^{-16}$,
  eigenvalues $(h^{-2},h,h)$. PASS.
- **Fabric phase work (74)** conformal-limit reduction to (18); the $p$ terms
  cancel. PASS.
- **Frozen artifacts reproduce the reported numbers**:
  `fe_mms_convergence.csv` → orders $p$ 2.00/2.00, $u_x$ 2.99/2.96, $u_y$
  3.00/2.96; `fe_mandel_refinement.csv` → ratio $7.10392/3.65796=1.9420$
  ("1.94"); `fe_load_limit.csv` → floor $3.2209\times10^{-3}$ ("3.2e-3");
  `mms-convergence.json` → fixed-mesh temporal orders 0.978–1.397 ("0.98–1.40");
  `fe_fabric_mandel_peak.csv` → 3.616, 4.363, 4.990, 5.521 ($\times10^{-5}$);
  `fe_fabric_contours.csv` → 3.606, 4.349, 4.974, 5.503 ($\times10^{-5}$) and
  $u$-magnitudes 5.18, 5.14, 2.38, 5.26 ($\times10^{-5}$);
  `site/reports/conformal-verification.json` → 186 checks, max identity error
  $2.455\times10^{-9}$ ("2.5e-9"); `fabric-verification.json` →
  worst probe diff $4.885\times10^{-15}$ ("4.9e-15"), $\mathbb D{:}e_3$
  $1.58\times10^{-16}$, rotation invariance $2.50\times10^{-16}$, $\mathbf H$
  reconstruction $2.22\times10^{-16}$, $\det\mathbf H-1=-3.33\times10^{-16}$,
  conformal cross-check max $1.87\times10^{-14}$ ("1.9e-14");
  `tensor-verification.json` → 273 states / 13 materials. All PASS.
- **Example moduli**: $K_s=28K_*$; isotropic comparison mineral shear
  $=$ mean of the five deviatoric modes $/2=33.6/2=16.8K_*$. PASS.
- Every `\cite*` key resolves in `references.bib` (35 cited keys, 0 missing).

I found **no error in the mathematical development**. The findings below are
notation/mapping defects in the prose and validation materials.

---

## 3. REQUIRED items

### R1-C1 — `main.tex:257–259`: the wide-tilde rule names the wrong source frame and contradicts the manuscript's own definition

Location: `main.tex` line 257–259 (`\(\bar\rho_{s0}\). A wide tilde denotes the
representation of a true-frame quantity in the intermediate mineral frame,
obtained by the rotation \(\mathbf R_A\), as in
\(\widetilde{\mathbf\tau}=\mathbf R_A^T\mathbf\tau'\mathbf R_A\) of
\eqref{eq:fabric-phase-work}.`), together with `main.tex:223–224`, `main.tex:261`,
`main.tex:312`, and `sections/pore_fabric.tex:172–173`.

The manuscript defines the "true frame" as the frame reached by
$\bar{\mathbf F}$: `main.tex:223–224` states "a hat denotes the true frame";
`main.tex:312` calls $\hat{\boldsymbol\tau}_s$ "the true-frame Kirchhoff
stress"; and `main.tex:261` contrasts "mixture-frame and true-frame stress
representations" via $\bar{\boldsymbol\sigma}_s=\mathbf R_A\hat{\boldsymbol\sigma}_s\mathbf R_A^{T}$
(`main.tex:285`). In the decomposition $\mathbf F=\mathbf A\bar{\mathbf F}$ the
frame reached by $\bar{\mathbf F}$ **is** the intermediate (mineral)
configuration, so the "true frame" and the "intermediate mineral frame" are the
same frame, and the rule as written ("representation of a true-frame quantity in
the intermediate mineral frame") is a no-op.

The cited example is not a no-op: $\widetilde{\boldsymbol\tau}=\mathbf R_A^{T}\boldsymbol\tau'\mathbf R_A$
(`sections/pore_fabric.tex:172`) maps the **mixture-frame** effective stress
$\boldsymbol\tau'$ into the mineral frame ($\mathbf R_A^{T}$ undoes the
true$\to$mixture rotation of (6)). Hence the stated rule contradicts the
definition it cites: the source object is a mixture-frame quantity, not a
true-frame one.

This matters because $\widetilde{\boldsymbol\tau}$ is the element on which the
tensorial distention work (74) is built, so the reader is given wrong decoding
instructions for a central symbol.

Fix (either): change "a true-frame quantity" to "a mixture-frame quantity"; or,
if the intent is "the true (current) configuration", drop the "frame" wording
and state explicitly that the tilde maps a spatial/mixture-frame tensor into the
mineral frame by the inverse rotation.

### R1-C2 — `validation/equation_to_moose_map.yml:15`: the FabricMaterial mapping declares an output the material does not produce

Location: `validation/equation_to_moose_map.yml:15`
(`produces: [first_piola, fluid_mass, J, Jbar, solid_fraction, B,
distention_strain, distention_stress]`).

For `ConformalMaterial` the `produces` list (`…:8`) enumerates exactly the
declared MOOSE properties. For `FabricMaterial` the list names
`distention_stress`, but `moose_app/src/materials/FabricMaterial.C:50–69`
declares no such property (it declares `first_piola`, `mass_flux`, `fluid_mass`,
`J`, `Jbar`, `solid_fraction`, `stability`, `energy`, `P22`, `B_par`, `B_per`,
`B_anisotropy`, `ln_a`, `ln_h`, `distention_a`, `distention_h`, `drained_c11`,
`drained_c12`, `sigma11`, `sigma22`), and `moose_app/include/utils/FabricLaw.h`
computes no $\bar{\mathbf S}_{\mathrm{dis}}$ or $\mathbf S_{\mathrm{dis}}$
output (grep for `distention_stress` / `S_dis` returns only this YAML line).
The map therefore claims a quantity that is not exposed.

Fix (either): declare and populate the distention-stress property in
`FabricMaterial`; or remove `distention_stress` from the mapped outputs (and, if
desired, replace it with the properties actually exported). The scientific
content is unaffected; this is a traceability-accuracy defect in a shipped
validation mapping, which the task scope requires me to flag.

---

## 4. OPTIONAL items

### R1-O1 — Notation paragraph does not cover every decoration actually applied

The paragraph (`main.tex:218–263`) enumerates bar, hat, tilde, single/double
prime, and superscript $d$/subscript $\mathrm{dis}$, superscript $n$,
subscript $0$. The manuscript additionally applies: superscript `+`
($\mathbb D^{+}$, `sections/pore_fabric.tex:293`), subscript `*` ($K_*$,
`sections/experiments.tex:6–7`), subscripts $\parallel/\perp$
(`sections/pore_fabric.tex:380–381`), and role subscripts $s,f,\xi,A,t$ (e.g.
$K_s$, $K_f$, $\bar\rho_\xi$, $R_A$, $t_n$, $\mathbf e_t$). Each is defined at
first use, so I do not think this misleads a careful reader; a one-line "role
subscripts follow their first definition" clause would close it.

### R1-O2 — "fixed-pressure" qualifier is split across W′ and P″

`main.tex:226–233` attaches "fixed-pressure stress" to $\mathbf P''$ (46) while
attaching "its fixed-pressure companion" to the energy $W'$ (45), so the same
qualifier labels objects on opposite sides of the prime pairing
($W''\!\leftrightarrow\!\mathbf P''$, $W'\!\leftrightarrow\!\mathbf P'$).
Consider naming $W'$ the Legendre/pressure-work companion explicitly.

### R1-O3 — The letter `e` is used for both a spatial tangent and the fabric basis

`sections/experiments.tex:96–99` uses $\mathbf e_t$ for a spatial unit tangent
(85), while `sections/pore_fabric.tex:305–322` reserves
$\mathbf e_1,\dots,\mathbf e_6$ for the symmetric-tensor fabric basis. The
manuscript already distinguishes the basis from the Mandel component indices
(83); it does not distinguish it from $\mathbf e_t$.

### R1-O4 — The floor attribution crosses meshes

The discussion attributes the $3.2\times10^{-3}$ floor (nonlinear load sweep at
$nx=20$, `figures/fe_load_limit.csv`) to backward-Euler temporal error using the
linear step-refinement ratio $1.94$ measured at $nx=40$
(`figures/fe_mandel_refinement.csv`, $h=0.025$). The attribution is hedged
("attributable to") and the supporting values are close ($3.66\times10^{-3}$ vs
$3.22\times10^{-3}$), but the two measurements are on different meshes.

### R1-O5 — Postprocessors are absent from the equation→object map

`moose_app/src/postprocessors/DofReactionSum.C` and
`.../ReferenceOutflow.C` implement, respectively, the summed platen reaction
(`sections/finite_elements.tex:139–145`) and the boundary mass-flux integral
$\int_{\Gamma_Q}w\bar Q_f\,\mathrm dA_0$ (96). They are postprocessors rather
than kernels/materials, hence outside the literal scope of my check, but
`validation/equation_to_moose_map.yml` does not record them.

---

## 5. Assessment

The scientific and mathematical development is internally consistent and
reproduces under independent symbolic and numerical recomputation: the
multiplicative decomposition and $a=\det\mathbf A$ relations, the
Coleman–Noll-type conjugacy and reduced energies $W''$, $W'$, the finite
deformation Biot tensor (49) and its explicit form (52), the stress/energy
normalizations, the logarithmic-derivative/spatial-stress conversion (101)–(106),
the drained compliance and Moore–Penrose restriction (43)/(78), and the
pore-fabric kinematics, basis, retained subspace, work-conjugate pair,
uniqueness argument (scope-limited to the reference quadratic model), and
conformal limit all verify. Every numerical claim I could recompute from the
frozen artifacts matches its recorded value. The manuscript's scope statements
are honest: the finite-load runs are labelled demonstrations, the fabric law is
labelled a shared-convention implementation check, and no experimental
validation is claimed.

The two required items are small in scope (a notation rule and a mapping entry),
but both are stated items that contradict the definitions/implementations they
refer to, so they should be corrected before the manuscript and its shipped
validation materials are considered final.

---

VERDICT: MINOR REVISION
