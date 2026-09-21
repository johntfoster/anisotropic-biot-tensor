# SIMULATED AI PEER REVIEW — Reviewer 1 (Derivation and Correctness)

Manuscript: *An anisotropic Biot tensor from mineral stress and distention work*
Snapshot reviewed (frozen): `.agent-runtime/review-snapshots/round-30`
Declared SNAPSHOT_ID: `ade4ec319cd757abad15546bd307efe2d9f85b2df21aa075bd74fb9ba4f0658b`

## Verification of the frozen snapshot (mandatory first checks)

1. `sha256sum .agent-runtime/review-snapshots/round-30/source-manifest.json`
   = `ade4ec319cd757abad15546bd307efe2d9f85b2df21aa075bd74fb9ba4f0658b` — **matches the declared SNAPSHOT_ID**.
2. Re-hash of every listed file against `source-manifest.json`, performed on a temporary copy
   (`cp -r` into `/tmp`; nothing written inside the snapshot):
   - **Total entries checked: 592** (manifest lists 592 paths).
   - **Hash mismatches: 0.**
   - **Listed files missing on disk: 0.**
   - **Present files not listed: 2** — `source-manifest.json` and `SNAPSHOT_ID`, i.e. the two
     self-referential meta files. Both are expected and are not source entries.
   Result: **hash check clean.**

Build cross-checks used in this review: `build/main.log` records
`Output written on main.pdf (34 pages, 2804538 bytes)`, with no LaTeX errors, no undefined
references, and no overfull boxes. `build/main.pdf` renders the equations as written in the
sources. `provenance/ai_use_statement.tex` is input by `main.tex`.

Declarations of independence: I did not open any file under `reviews/` (including
`reviews/README.md`, any LAUNCH-STATE, any report, or any response), and I did not read any
`round-*` snapshot other than `round-30`. I ran none of the held numerical suites
(`validation/`, `examples/verify_*.py`); all numerical cross-checks below were recomputed by me
from the frozen CSV/JSON artifacts in the temporary copy, or verified algebraically.

Method: I re-derived every step from its stated starting point (reference configuration,
pull-backs/push-forwards, the conformal distention decomposition, the volume-fraction-weighted
phase stress, the volumetric energy, the pressure-coupling tensor, the drained compliance, and
the isotropic and isotropic-mineral reductions), checked index/factor/rank/symmetry/objectivity
and each asserted limiting case, and cross-checked all quoted values against the frozen
artifacts. Symbols were checked for consistent definition and use; trace vs full-tensor claims
were checked separately.

---

## REQUIRED CHANGES

### R1-C1 — False statement about the potential in the fabric-equilibrium justification
**Location:** `sections/pore_fabric.tex`, lines 205–209 (Section 7.4, text around
`eq:fabric-equilibrium`, rendered eq. (75)).
**Quoted text:**
> "The minimization is restricted to distentions whose logarithmic strain lies in the retained
> subspace \(\operatorname{range}\mathbb{D}\) of \cref{sec:fabric-biot}: on the complement
> \(\mathbb{D}\) vanishes, **the potential does not depend on the complementary modes**, and those
> modes are frozen to the mineral rather than equilibrated."

**Defect (incorrect mathematics as written).** The clause is asserted of "the potential", but the
potential being minimized is
\(\Phi(\mathbf G)=W_{\mathrm{dis}}(\mathbf G)+\phi_{s0}\bar W_s(\bar{\mathbf F}(\mathbf G))+\phi_{s0}p\bar J(\mathbf G)\)
(eq. 75 / `eq:fabric-equilibrium`), and the *mineral* term does depend on the complementary modes.
With \(\mathbf R_A=\mathbf I\) and \(\bar{\mathbf F}=\mathbf G^{-1/2}\mathbf F\), a complementary
distention increment (e.g. \(\mathbf E_{\mathrm{dis}}=t\,\mathbf e_3\)) changes \(\bar{\mathbf F}\)
at first order in \(t\) for any \(\mathbf F\neq\mathbf I\), hence changes
\(\phi_{s0}\bar W_s(\bar{\mathbf F})\); only the distention term \(W_{\mathrm{dis}}\) is annihilated
by \(\mathbb D\). The "frozen to the mineral" restriction is a modeling choice, and the very next
sentence ("read on that subspace") already makes the restriction explicit; but the intermediate
justification as printed is not correct for the full potential.
**Required fix:** restrict the claim to the distention energy (e.g. "the distention energy does not
depend on the complementary modes") or state the restriction directly ("those modes are dropped
from the minimization by construction"). This is a local wording correction and changes no derived
result.

---

## OPTIONAL NOTES

### R1-O1 — "equivalently" is not an equivalence
**Location:** `sections/pore_fabric.tex`, lines 306–309 (Section 7.5).
**Quoted text:** "That reduced \(\mathbb{D}\) is transversely isotropic about \(\mathbf m\) because
\(\mathbf e_1\) and \(\mathbf e_2\) are invariant under rotations about \(\mathbf m\);
**equivalently**, it annihilates the four complementary modes of this basis…".
The two conditions are not equivalent in general: annihilating the four complementary modes
constrains \(\mathbb D\) to a block on \(\operatorname{span}(\mathbf e_1,\mathbf e_2)\), whereas
the invariance of \(\mathbf e_1,\mathbf e_2\) is what actually delivers transverse isotropy (I
verified the conclusion is correct: \(\mathbf e_1=\mathbf I/\sqrt3\) is fully isotropic and
\(\mathbf e_2=\sqrt{3/2}\,(\mathbf m\otimes\mathbf m-\mathbf I/3)\) is invariant under rotations
about \(\mathbf m\), so any symmetric \(2\times2\) block \((k_v,k_a,k_c)\) on that span is
transversely isotropic). Suggest replacing "equivalently" with "and, concretely,".

### R1-O2 — Citation of (22) for \(\partial W_A/\partial\ln a=\tfrac13\tr\mathbf\tau'\)
**Location:** `sections/pore_fabric.tex`, lines 147–149.
**Quoted text:** "The scalar driving term
\(\partial W_A/\partial\ln a=\tfrac13\tr\mathbf\tau'\) of
\eqref{eq:energy-returned-pressure-balance} is replaced by this tensor…".
`eq:energy-returned-pressure-balance` (rendered eq. 22) states
\(\partial W_A/\partial\ln a=\tfrac{\phi_{s0}}3\tr\bar{\mathbf\tau}_s+\phi_{s0}p\bar J\), not
\(\tfrac13\tr\mathbf\tau'\). The two are equal because \(\tr\mathbf\tau'=\phi_{s0}(\tr\bar{\mathbf\tau}_s+3p\bar J)\)
(eq. 12), but the identity as attributed to (22) is not literally what (22) contains. Either cite
the relation that actually states \(\tfrac13\tr\mathbf\tau'\), or add "(equivalently, via the trace
of (12))".

### R1-O3 — (22)–(23) is a consistency check, not an independent derivation
**Location:** `main.tex`, lines 400–402 (Section 3, after `eq:energy-returned-pressure-balance`).
**Quoted text:** "The second line uses pressure equilibrium. Substituting it into the first
recovers \eqref{eq:constitutive-kirchhoff-phase-stress}, including all shear components."
This is correct, but note the logical direction: eq. (22) is obtained from energy differentiation
at fixed \(\bar J\), while eq. (23) is obtained from the *trace* of eq. (12). Substituting (23)
into (22) to recover (12) is therefore a consistency check that presupposes (12) for one of its two
ingredients. The word "check" is already used two sentences later; a single word noting that (23)
uses the trace of (12) would remove any appearance of circularity. No result is affected.

### R1-O4 — Optional: state the pressure interval for eq. (55)
**Location:** `main.tex` eq. (37) (`eq:cauchy-pressure-tangent`) and the surrounding text
(NEW, Section 5).
The relation \(\partial\mathbf\sigma/\partial p|_{\mathbf F}=-\mathbf B\) and the integrated form
(eq. 38) are correct (I verified \(\partial\mathbf\sigma/\partial p=-\mathbf B\) from
\(\mathbf\sigma=J^{-1}\mathbf P'\mathbf F^{T}-p\mathbf I\) using the mixed derivative
\(\partial_p\partial_{\mathbf F}W'=\partial_{\mathbf F}(\phi_{s0}\bar J)\)). The text already
qualifies the integration as holding "on an admissible pressure interval containing zero"; making
explicit that the interval is the one on which the mineral root of eq. (37) exists (condition 38)
would tie the two statements together, but the current wording is acceptable.

---

## Assessment of derivation and correctness quality

I verified the derivations end-to-end and found **no mathematical errors** in the derivations
themselves and **no unsupported numerical claims**. Specific confirmations:

- **Kinematics and phase stress.** \(\mathbf F=\mathbf A\bar{\mathbf F}\) with
  \(\mathbf A=a^{1/3}\mathbf R_A\) gives \(\bar{\mathbf F}=a^{-1/3}\mathbf R_A^{T}\mathbf F\) and
  \(\bar{\mathbf C}=a^{-2/3}\mathbf C\) exactly. The phase sum
  \(\mathbf\sigma=\phi_s\bar{\mathbf\sigma}_s-(1-\phi_s)p\mathbf I\), the single-prime stress, and
  the Kirchhoff form \(\mathbf\tau'=\phi_{s0}(\bar{\mathbf\tau}_s+p\bar J\mathbf I)\) (eq. 12) are
  all algebraically correct, including the two definitions of \(\bar{\mathbf\tau}_s\)
  (\(=\bar J\bar{\mathbf\sigma}_s\) and \(=\mathbf R_A\hat{\mathbf\tau}_s\mathbf R_A^{T}\)), which
  coincide.
- **Work decomposition.** Eq. (15) for \(\delta\mathbf F\mathbf F^{-1}\), the cancellation of the
  skew rotation increment against symmetric \(\mathbf\tau'\), and the reduction to eq. (18) all
  check out; I re-derived \(\mathbf R_A^{T}\mathbf\tau'\mathbf R_A-\phi_{s0}p\bar J\mathbf I=\phi_{s0}\hat{\mathbf\tau}_s\)
  from eq. (12). Objectivity eq. (19) follows correctly from left-rotation invariance of
  \(\bar W_s\), and holds for anisotropic minerals because a left rotation leaves the material
  metric unchanged.
- **Energy-returned stress.** Eq. (22) (\(\mathbf\tau'=\partial W_A/\partial\ln a\,\mathbf I+\phi_{s0}\dev\bar{\mathbf\tau}_s\))
  and eq. (23) are mutually consistent and recover eq. (12) including all shear components; the
  trace identities \(\tr\mathbf\tau'=3\partial W_A/\partial\ln a\) were checked independently.
- **Pressure coupling.** Eq. (29)–(31), the implicit differentiation (32), and the explicit Biot
  tensor (33) are factor- and index-correct; I confirmed the last factor
  \(\partial_{\mathbf F}[\mathbf I:\mathbb C_s:\dev\boldsymbol\varepsilon]\mathbf F^{T}=\mathbf F[\partial\log\mathbf C/\partial\mathbf C:\dev(\mathbb C_s:\mathbf I)]\mathbf F^{T}\)
  and the coefficient \(\phi_{s0}/3\) inside the braces. The claim that
  \(\dev(\mathbb C_s:\mathbf I)=\mathbf 0\) (cubic symmetry) makes \(\mathbf B\) spherical is
  correct. Eq. (36)–(38) (\(\partial_p W'|_{\mathbf F}=\phi_{s0}\bar J\),
  \(\partial_p\mathbf\sigma|_{\mathbf F}=-\mathbf B\), and the integrated response) are correct.
- **Drained response.** The spherical-path relations (44)–(46), the distention energy (47), the
  anisotropic EOS (48), the stability domain (49), the drained stiffness (52), and the compliance
  restriction (56)–(57) are mutually consistent; I verified both that (52) and (57) are exact
  inverses and that (57) holds numerically. The reference relations
  \(\mathbf B_0=\mathbf I-\mathbb C^d:\mathbb C_s^{-1}:\mathbf I\) and
  \(S_s=\phi_{s0}\mathbf I:\mathbb C_s^{-1}:\mathbf I-\mathbf I:\mathbb C_s^{-1}:\mathbb C^d:\mathbb C_s^{-1}:\mathbf I\)
  are correct (I recomputed \(S_s=0.0125\) from the frozen matrices). The unjacketed check
  (eqs. 58–59) is consistent: I verified
  \(\mathbf F\mathbf C^{-1}\mathbf F^{T}=\mathbf I\) and that the mineral-volume equation and phase
  balance are both satisfied.
- **Pore fabric.** The polar decomposition (63), the multiplicative split (65)–(66), the
  unimodular fabric \(\mathbf H=a^{-2/3}\mathbf G\) (67), the conjugate pair (70), the virtual
  deformation (71), and the phase work (72) are correct (I re-derived (72) via the full contraction
  \(\mathbf G^{1/2}\tilde{\mathbf\tau}\mathbf G^{-1/2}\)), and (72) reduces exactly to (18) in the
  conformal limit. The equilibrium (73), the additive strain split (76) (verified by linearizing
  \(\bar{\mathbf C}=\bar{\mathbf F}^{T}\bar{\mathbf F}\)), the Moore–Penrose compliance (78)
  (verified to reduce to the rank-one (43) in the conformal limit, with the correct coefficient
  \((1-c)/(9K)\)), and the fabric Biot tensor (84) are correct. The transverse-isotropy argument is
  sound (see R1-O1 for a wording quibble), and the "spherical \(\mathbf B\) when the volume–axial
  modulus vanishes" claim is correct: for isotropic \(\mathbb C_s\) and \(k_c=0\),
  \(\mathbb C^d:\mathbf I=c_v\mathbf I\), so \(\mathbf B_0\) is spherical, whereas \(k_c\neq0\)
  makes it directionally anisotropic.
- **Logarithmic-strain appendix.** The Fréchet derivative (A2), its self-adjointness, the trace
  identity \(\tr\mathbf\tau=\tr\mathbf T\), and \(\partial\log\mathbf C/\partial\mathbf C:\mathbf C=\mathbf I\)
  are all correct, and the repeated-eigenvalue branch is the correct continuous limit.
- **FE implementation vs continuum.** \(\mathbf P=J\mathbf\sigma\mathbf F^{-T}\),
  \(m_f=\bar\rho_f(J-\phi_{s0}\bar J)\), the Darcy closure \(\mathbf Q_f=-\tfrac{J\bar\rho_f k}{\mu_f}\mathbf F^{-1}\mathbf F^{-T}\operatorname{Grad}p\),
  the storage identities (92)–(94), and the weak balances (95)–(96) are consistent with the
  continuum equations they claim to implement, including the stated convention shift by the factor
  \(J\).
- **Quoted numerical evidence — all reproduced from the frozen artifacts.**
  Reference Biot components \(0.7000,0.7583,0.7917\) (matches `build/conformal/pressure_response.csv`
  p=0 and my recomputation); isotropic mineral shear modulus \(16.8K_*\) and \(K_s=28K_*\)
  (matches `experiments.json` and my deviatoric-eigenvalue computation); FE reference
  \(G=0.75\), Biot \(0.6\), total storage \(17/80\); MMS space orders 2.00/2.00, 2.99/2.96,
  3.00/2.96 (`fe-evidence/mms-convergence.json`); temporal successive-difference orders spanning
  \(0.978\)–\(1.397\) (text "\(0.98\)–\(1.40\)"); step-refinement errors \(3.66\times10^{-3}\) and
  \(7.10\times10^{-3}\) with ratio \(1.94\); the finite-load pressure floor \(3.22\times10^{-3}\)
  (`nonlinear_load_0.0001/analysis.json`); fabric reconstruction \(2.2\times10^{-16}\),
  \(\det\mathbf H-1=-3.3\times10^{-16}\), \(\lVert\mathbb D:\mathbf e_3\rVert=1.6\times10^{-16}\),
  \(\mathbb D:\mathbf e_6=0\), rotation invariance \(2.5\times10^{-16}\), worst probe difference
  \(4.9\times10^{-15}\), volume-only cross-check \(1.9\times10^{-14}\)
  (`build/fabric/fabric-verification.json`); 186 named checks with largest constitutive-identity
  error \(2.5\times10^{-9}\) and 273 states over 13 mineral stiffnesses
  (`build/conformal/verification.json`, `build/weighted-stress/tensor-verification.json`); the
  coupled peak centre pressures \(4.36,4.99,5.52\times10^{-5}\) against \(3.62\times10^{-5}\)
  uncoupled; the refined contour peaks \(3.61,4.35,4.97,5.50\times10^{-5}\) and displacement
  maxima \(5.18,5.14,2.38,5.26\times10^{-5}\) (`figures/fe_fabric_contours.csv`,
  `figures/fe_fabric_mandel_peak.csv`). No quoted value disagreed with its artifact, and no
  claimed order exceeds what the artifacts measure.

The manuscript is unusually careful about the boundary between what is derived and what is
assumed, and it labels the finite-load coupled runs and the shared-convention script checks
honestly. The single item I would require be changed (R1-C1) is an incorrect justification
clause; it does not propagate to any equation or result. The remaining notes are presentational.
On derivation and correctness grounds the paper is otherwise in good shape.

VERDICT: MINOR REVISION
