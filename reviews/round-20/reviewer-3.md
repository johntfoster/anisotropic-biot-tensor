# Reviewer 3 — Round 20 (emphasis: prose, notation, significance)

Snapshot reviewed (read-only):
`/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/review-snapshots/round-20`

Declared `SNAPSHOT_ID` = `542eab1bb76847fbbe65596374191d99ffeb287b216651398c0ebfb37895aa0b`

I read only this snapshot. All scratch work was done in `/tmp/r20build` (a writable copy); no snapshot file was modified.

---

## 1. Snapshot identity and manifest

| Check | Result |
|---|---|
| `sha256(source-manifest.json)` vs declared `SNAPSHOT_ID` | **match** — `542eab1bb76847fbbe65596374191d99ffeb287b216651398c0ebfb37895aa0b` |
| `SNAPSHOT_ID` file contents vs declared id | **match** (single line, same hash) |
| Manifest entries re-hashed | 534 |
| Hash matches | **534 / 534** |
| Missing files | **0** |
| Hash mismatches | **0** |
| Files present but not in manifest | 2 — `source-manifest.json`, `SNAPSHOT_ID` (the manifest's own container files; expected) |

Method: read `source-manifest.json`, re-computed `sha256` of every listed path, and walked the tree for unlisted files. Integrity is complete: every listed artifact, including `main.tex`, all `sections/*.tex`, `references.bib`, the embedded `build/anisotropic-biot-2026-09-20-v2.zip`, `site/evidence.json`, and the `moose_app/` and `fe-evidence/` payloads, hashes as recorded.

---

## 2. Notation audit

### 2.1 Symbol collisions specifically tested

- **`W_d` (suspected double use: two different energies).** Not present. `W_d` appears only as the *distention energy* of the shape-changing model in `sections/pore_fabric.tex` (lines 112–123, 128–129, 182, 201–215, 243–254, 283–294, 313) and once in `main.tex:579`. The conformal volume-only distention energy is a *distinct symbol*, `W_A`, throughout `main.tex` (344–377) and `sections/stress_reconstruction.tex` (74–153). The replacement is explicitly flagged: `sections/pore_fabric.tex:117–118` — "The distention energy \(W_d(\mathbf G)\) now depends on the full symmetric tensor \(\mathbf G\), replacing the volume-only energy \(W_A(a)\)". **No collision.**

- **`a` (suspected reuse: distention volume ratio vs geometric half-width).** In the *manuscript* every occurrence of bare \(a\) in math is the distention volume ratio \(a=\det\mathbf A\) (`main.tex:245`, `main.tex:347`; `sections/pore_fabric.tex:32,74,98,101,118,132,167,189,215,255,280`; `sections/stress_reconstruction.tex:8,55,58,60,162`; `sections/limits.tex:62`). The reference geometry half-width is written \(L_x\) (`sections/finite_elements.tex:151–157`), never \(a\). So the collision does **not** occur in the manuscript. (For awareness only: the non-manuscript companion `site/evidence.json:15` prose writes the half-width as "\(a=1\)". That is outside the manuscript but reuses the letter \(a\) used by the paper for the distention ratio; see optional finding O-3.)

### 2.2 Symbol inventory completeness

I enumerated every displayed/inline symbol and confirmed each is defined before or at first use. No undefined symbols found. Verified definitions include: the multiplicative decomposition and its bar convention (`main.tex:238–260`), the explicit bar/hat/blackboard-bold inventory paragraph (`main.tex:211–218`), \(\mathbb C_s,\mathbb C^d\) (`stress_reconstruction.tex:40–43`), \(K,K_s\) (`stress_reconstruction.tex:53–54`), \(W_A\) (`stress_reconstruction.tex:78`), \(\mathbf B_0,S_s\) (`limits.tex:10,19–26`), \(K_*\) (`experiments.tex:29`), \(\mathbf G,\mathbf H,\mathbf E_d,\bar{\mathbf S}_d,\mathbf S_d,\mathbb D,h,\mathbf m,B_\parallel,B_\perp,\phi_{s0}\) (`pore_fabric.tex`), and the FE/transport set \(\bar\rho_f,\bar\rho_{f0},m_f,K_f,\mathbf q,\mathbf Q_f,\bar Q_f,\mathbf b_0,s_f,\mathbf t_0,\Gamma_t,\Gamma_Q,\Omega_0,q_L,L_x,L_y,U,P_0\) (`finite_elements.tex`). The appendix's generic conjugate stress \(\mathbf T\) is explicitly scoped to that appendix (`logarithmic_derivative.tex:22–24`).

### 2.3 Correctness of reuses

All reuses I checked are correct and mutually consistent across `main.tex` and `sections/*.tex`:

- Phase-stress algebras `\eqref{eq:constitutive-single-prime-phase-stress}` and `\eqref{eq:constitutive-kirchhoff-phase-stress}` are mutually consistent via \(J\phi_s=\phi_{s0}\bar J\).
- `\eqref{eq:energy-returned-effective-stress}` + `\eqref{eq:energy-returned-pressure-balance}` reproduce `\eqref{eq:constitutive-kirchhoff-phase-stress}`, as the text claims (`main.tex:395–400`).
- The conformal reduction \(\mathbf G=a^{2/3}\mathbf I\) in `pore_fabric.tex:49–55` is stated to and does reduce to `\eqref{eq:spherical-distention}`/`\eqref{eq:conformal-mineral-metric}`; `\eqref{eq:fabric-compliance-restriction}` reduces to `\eqref{eq:drained-compliance-restriction}` in that limit, as claimed.
- Cross-artifact symbols match too: `experiments.json` reference Biot `[0.7, 0.758333…, 0.791666…]` = "0.7000, 0.7583, 0.7917" (`experiments.tex:33`); \(K=7K_*\), \(K_s=28K_*\), \(\phi_{s0}=0.6\) all match.

**Residual (optional) notation items are listed in §5; none are required corrections.**

---

## 3. Prose and structure

**Figure coverage — all cited.** 7 figures, 7 `\includegraphics`, 7 in-text citations:

| Figure label | File | Cited at |
|---|---|---|
| `fig:conformal-pressure` | `build/conformal/pressure_response.pdf` | `experiments.tex:45` |
| `fig:conformal-shear` | `build/conformal/shear_response.pdf` | `experiments.tex:75` |
| `fig:conformal-directional` | `build/conformal/directional_response.pdf` | `experiments.tex:104` |
| `fig:conformal-rotation` | `build/conformal/rotation_response.pdf` | `experiments.tex:128` |
| `fig:conformal-layer` | `build/conformal/constrained_layer.pdf` | `experiments.tex:151` |
| `fig:fe-fabric-probe` | `figures/fe_fabric_probe.pdf` | `finite_elements.tex:222` |
| `fig:fe-fabric-mandel` | `figures/fe_fabric_mandel.pdf` | `finite_elements.tex:247` |

(The two FE figures are cited with `\Cref`; a `\ref`-only scan would miss them.) There are no tables in the manuscript and none are cited.

**Availability/scope statements are accurate.** I verified the availability paragraph (`experiments.tex:210–242`) against what actually ships:

- The embedded archive `build/anisotropic-biot-2026-09-20-v2.zip` exists, its `filespec` matches the `\embedfile` (`main.tex:33–35`), and it contains exactly the claimed `moose_app/` payload: `include/utils/FabricLaw.h`, `include/materials/FabricMaterial.h`, `src/materials/FabricMaterial.C`, `inputs/fabric_probe.i`, `inputs/conformal_probe.i`, `inputs/fabric_mandel.i`, plus the reported run histories under `fe-evidence/runs/`, `manifest.json`, and a README with reproduction commands. The claim that the *rest* of the FE implementation is not in the archive is correct (only 4 `moose_app` files ship).
- Every repository path named in the same paragraph exists in the snapshot: `moose_app/`, `validation/`, `fe-evidence/runs/`, `fe-evidence/mms-convergence.json`, `figures/`, `site/evidence.json`. A sampled case dir (`fe-evidence/runs/anisotropic_0/`) contains `input.i`, `provenance.json`, `analysis.json`, `solution.csv`, matching "input deck, run provenance, per-run analysis, and scalar history".
- `site/evidence.json` does record the inspected revision and SHA-256 pins, as stated.

**Scope/limitation language is honest and consistent end to end.** Abstract (`main.tex:44–49`), `finite_elements.tex:263–281`, and `site/evidence.json` all agree that the finite-load FE cases are demonstrations, that no quantitative finite-deformation verification or experimental validation is claimed, and that parameters are synthetic. The partial-drainage square-domain caveat in `finite_elements.tex:276–278` matches the evidence file.

**Numerical claims are backed by the shipped evidence** (spot-checked): 186 conformal checks (`build/conformal/verification.json: checks_passed=186`); 67 legacy identities = 65 per-state + 2 reference; max constitutive error \(2.45\times10^{-9}\) vs "\(2.5\times10^{-9}\)"; 273 states = 13 materials × 21 (`build/weighted-stress/tensor-verification.json`); second-order refinement orders ≈ 2.00 for energy/pore-volume/pressure; fabric worst diff `4.885e-15` = "\(4.9\times10^{-15}\)" and conformal cross-check max `1.87e-14` = "\(1.9\times10^{-14}\)"; peak centre pressures 6.280e-5 / 5.102e-5 / 3.946e-5 / 5.133e-5 = "\(6.28,5.10,3.95,5.13\times10^{-5}\)"; normalized pressure discrepancy `0.003221` = "\(3.2\times10^{-3}\)" at `nx=20, dt=10^{-3}`. Nothing overstated.

**Significance/novelty framing** is clear and well placed: `main.tex:88–116` states the gap ("What they do not supply is a tensorial distention law…") and `main.tex:117–140` states the distinct route (fabric enters the distention energy, not the stiffness). The conclusion's mechanism summary (`main.tex:566–600`) and the honest conformal-restriction caveat (`main.tex:601–620`) are appropriately scoped. No undefined terms encountered; heavy terms ("distention", "unjacketed", "manufactured solution") are defined at first use.

---

## 4. Build check

From a writable copy in `/tmp` (snapshot untouched):

```
rm -rf /tmp/r20build && cp -r <snapshot> /tmp/r20build && chmod -R u+w /tmp/r20build
cd /tmp/r20build
latexmk -lualatex -interaction=nonstopmode -halt-on-error main.tex
```

Observed result: **exit code 0**; LuaHBTeX; `Output written on main.pdf (28 pages, 648772 bytes)`; `main.bbl` produced from `references.bib` (36 entries) via plainnat; latexmk reported all targets up to date (converged).

- **Undefined references: 0.**
- **Undefined citations: 0.** (BibTeX run clean; no `Warning: Citation … undefined`.)
- **Overfull boxes: 0.**
- **Underfull boxes: 1** — `Underfull \hbox (badness 1137)` in `main.bbl` (a bibliography line-break, cosmetic, non-blocking).
- Missing-figure / missing-input errors: none (all 7 `\includegraphics` targets and all `\input` files resolved).

---

## 5. Findings

### Required corrections
**None found.** No hash/integrity defect, no undefined symbol, no uncited figure, no broken reference or citation, no build failure, no inaccurate availability/scope claim, and no numerical claim contradicted by the shipped evidence. There is no defect that must be fixed for acceptance.

### Optional (do not gate acceptance)

- **O-1 (notation clarity).** `main.tex:213` states a global rule — "A bar on a stress denotes its representation in the *mixture frame*". In `sections/pore_fabric.tex:119–123` the distention work conjugate is introduced as "the symmetric distention stress per reference mixture volume *in the intermediate frame*", written \(\bar{\mathbf S}_d\). That is a fifth, locally defined use of a bar on a stress and does not follow the stated stress rule. It is unambiguous at the point of use, but a short parenthetical (or a non-barred symbol) would remove the only notation wrinkle I found.
- **O-2 (style consistency).** Figure citations mix styles: `Figure~\ref{…}` in `sections/experiments.tex:45,75,104,128,151` versus `\Cref{…}` for sections and the two FE figures in `sections/finite_elements.tex:222,247`. Harmless; a single style would read more consistently.
- **O-3 (non-manuscript, cross-artifact).** `site/evidence.json:15` uses \(a=1\) for the domain half-width, while the manuscript reserves \(a\) for the distention volume ratio. Outside the manuscript's scope, but flagged because a reader following the availability pointer will meet both meanings.
- **O-4 (minor base-letter reuses, font/subscript-disambiguated).** \(\mathbf Q\) (superposed physical rotation, `main.tex:487`, `experiments.tex:127`, `pore_fabric.tex:202`) vs \(\mathbf Q_f\) (referential fluid mass flux, `finite_elements.tex:49–54`); \(\mathbf t\) (plane tangent, `experiments.tex:94–103`) vs \(\mathbf t_0\) (traction, `finite_elements.tex:100–105`); scalar \(G\) (drained shear modulus, `finite_elements.tex:164`) vs tensor \(\mathbf G\) (distention, `pore_fabric.tex`). All are distinguished by weight/subscript and are standard practice.
- **O-5 (abstract length).** The abstract (`main.tex:27–60`) is two dense paragraphs and will exceed typical 250-word limits; consider trimming for submission. Editorial only.

---

VERDICT: ACCEPT
