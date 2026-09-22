# Simulated AI Peer Review — Reviewer 3 of 3

**Seat:** exposition, notation and claims
**Repository:** `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
**Snapshot (read-only):** `.agent-runtime/review-snapshots/round-37`
**Declared SNAPSHOT_ID:** `0d75448ba758ff51c9f4e43423c120ffba6eaa1088442206436692c957fd2189`

This is a simulated AI peer review of a manuscript. It confers no journal acceptance.
All paths below are relative to the snapshot.

---

## 1. Mandatory integrity checks

### 1.1 Manifest digest

```
sha256(snapshot/source-manifest.json)
  = 0d75448ba758ff51c9f4e43423c120ffba6eaa1088442206436692c957fd2189
```

**PASS** — equals the declared SNAPSHOT_ID exactly.

### 1.2 Path-by-path re-hash

| Result | Count |
|---|---|
| Paths listed in `source-manifest.json` | 608 |
| Hash matches on disk | **608** |
| Hash mismatches | **0** |
| Listed-but-missing | **0** |
| Present-but-unlisted | **0** |

The two self-referential metadata files (`SNAPSHOT_ID`, `source-manifest.json`) are correctly unlisted;
no other file on disk is unlisted. `reviews/README.md` is present in the manifest and its digest matches
(verified by hashing only; **its content was never displayed**, per the isolation rules). The `reviews/`
subtree was excluded from my directory enumeration so that no file under it was listed.

### 1.3 Isolation self-report

**One accidental partial exposure, self-reported.** My very first orientation command ran a top-level
`ls -la` of the **working tree** (not the snapshot) before I had fully internalized the directory rule.
That listing printed the **names** of the entries in the working-tree `reviews/` directory (round/foster-cycle
directory names such as `round-1` … `round-18`, `foster-cycle-1`, etc.).

- No report file was opened, listed, globbed, or read.
- **No reviewer report content, verdict, or acceptance count was displayed.**
- The snapshot's `reviews/` directory was subsequently excluded from all enumeration.
- I did not touch sibling paper repositories, and I did not run any held suite (`validation/`, `examples/verify_*.py`).

---

## 2. Build audit

| Check | Result |
|---|---|
| Engine / driver | LuaHBTeX 1.14.0 via `latexmk -lualatex` (`.latexmkrc`, `Makefile:paper`) |
| Exit status | 0 |
| Pages | 33 |
| `!` errors in log | none |
| Undefined references / citations | none (`grep` for `LaTeX Warning`, `undefined`, `Rerun` → clean) |
| Missing glyphs / characters | none |
| Overfull boxes | none |
| Box warnings | **one** `Underfull \hbox (badness 1137)` — in the **bibliography** (`build/main.bbl`, output page 30), not the abstract |
| Rendered `??` / `[?]` | none in `pdftotext` output |

### 2.1 Equation-number reproducibility

I rebuilt the manuscript from the read-only snapshot into a scratch directory
(`latexmk -outdir=/tmp/r37build`). The rebuild reproduces the snapshot artifact exactly:

- 33 pages, identical byte size (2 809 899 bytes);
- **byte-identical extracted text** (`pdftotext` + whitespace-normalized `diff` → no differences);
- only the PDF `/ID` and `/CreationDate` fields differ, which are non-deterministic producer metadata.

Equation numbering and every `\eqref`/`\cref` resolution are therefore reproducible. The log
(`build/main.log`, 19:35) postdates `main.tex` (19:34) and `sections/*.tex` (19:03), so it corresponds
to the frozen source.

### 2.2 Cross-reference integrity

| Check | Count |
|---|---|
| `\label{}` in manuscript | 138, **all unique** (no duplicates) |
| Reference calls (`\cref/\Cref/\eqref/\ref`) | 142, **all resolve** |
| `\includegraphics` targets | 11, **all present** |
| Figure labels / figure refs | 11 / 11, no dangling, no orphan |
| Section refs | all resolve |
| Bib keys | 36; 36 cited; **0 missing, 0 orphans** |

---

## 3. Notation and decoration audit

Every stated rule in the notation paragraph (`main.tex:215–280`) was tested against **every** occurrence in
`main.tex` and `sections/*.tex`.

### 3.1 Counts of each decoration

| Decoration | Stated rule | Occurrences | Verdict |
|---|---|---|---|
| `\bar` (all payloads) | kinematic/energetic → mineral state; density → per-phase-volume; stress → mixture frame; `\bar S_dis` → conjugate to `G`; datum → prescribed value | **199** (22 distinct payloads: `\bar J` 81, `\bar{\mathbf F}` 38, `\bar W_s` 12, `\bar{\mathbf\tau}` 12, `\bar{\mathbf\varepsilon}` 10, `\bar{\mathbf\sigma}` 7, `\bar{\mathbf C}` 5, `\bar Q_f` 4, `\bar{\mathbf S}` 3, `\bar{\mathbf U}` 3, `\bar\rho_*` 16, …) | **consistent** |
| `\widehat` | true frame, mineral-normalized | **11** (`\widehat{\mathbf\tau}_s` 8, `\widehat{\mathbf\sigma}_s` 3) | consistent |
| `\widetilde` | true frame, mixture-normalized | **4** (all `\widetilde{\mathbf\tau}`) | consistent |
| superscript `d` | drained skeleton; **never** distention | **23** (all `\mathbb{C}^d`, `W^d`) | consistent |
| subscript `dis` | distention quantities | **39** | consistent (`W_A` is an explicitly stated exception, `main.tex:256–259`) |
| superscript `n` | discrete time level | **6** (`\dot m_f^{\,n}`, `\mathbf F^n`, `p^n`, `\mathbf F^{n-1}`, `p^{n-1}`) | consistent |
| subscript `0` | reference configuration | **124** decorations (`\phi_{s0}` 92, `\bar\rho_{s0}` 6, `\bar\rho_{f0}` 4, `\Omega_0` 6, `V_0` 5, `B_0` 3, `b_0` 2, `t_0` 2, `A_0` 2, **`P_0` 2**) | **2 exceptions — see R3-C1** |
| `\mathbb` | fourth-order tensors | 60 occurrences; emitted for `\mathbb{C}_s`, `\mathbb{C}^d`, `\mathbb{D}`, `\mathbb{D}^{+}` only | consistent (no second-order tensor in `\mathbb`, no fourth-order in `\mathbf`) |

The `\mathbb`/`\mathbf` split, the `^d`-never-distention claim, and the four-way bar/hat/tilde/prime scheme all
hold. The math of the two distention gradients is internally consistent across the conformal and fabric
sections (e.g. `\mathbf A=a^{1/3}\mathbf R_A` vs `\mathbf A=\mathbf R_A\mathbf G^{1/2}` agree at
`\mathbf G=a^{2/3}\mathbf I`; `\bar{\mathbf C}` agrees in both).

---

## 4. Claim-vs-evidence audit

Every quantitative claim I could locate was checked against the recorded artifacts.

| Manuscript claim | Location | Evidence | Verdict |
|---|---|---|---|
| conformal suite = 186 named checks | `experiments.tex:181` | `site/reports/conformal-verification.json` `checks_passed=186`, `len(checks)=186` | match |
| 65 per-state identities (5 states × 13) | `experiments.tex:182` | 5 state groups × 13 identities = 65 (`legacy_state*`) | match |
| + two reference Biot/rank-one relations | `experiments.tex:183` | `legacy_identities_rechecked=67` = 65+2 | match |
| largest constitutive identity error 2.5×10⁻⁹ | `experiments.tex:187` | `max_constitutive_identity_error = 2.4549890e-09` | match |
| second-order step refinement | `experiments.tex:187–190` | `observed_orders`: energy 2.0004…, pore 2.0002…, pressure 2.000 | match |
| 273 states across 13 stiffnesses | `experiments.tex:191` | `site/reports/tensor-verification.json`: 13 × 21 = 273 | match |
| MMS spatial orders p 2.00/2.00, uₓ 2.99/2.96, u_y 3.00/2.96 | `finite_elements.tex:196–199` | `mms-convergence.json` naive_orders | match to 2 d.p. |
| temporal orders 0.98–1.40, some >1 | `finite_elements.tex:200–204`; `main.tex:~630` | `difference_orders` min 0.97830, max 1.39688 | match |
| step-refinement ratio 1.94; 3.7×10⁻³ and 7.1×10⁻³ | `main.tex:~628` | `figures/fe_mandel_refinement.csv` 3.6579e-3, 7.1039e-3 → 1.942 | match |
| pressure floor ≈3.2×10⁻³ at nx=20, dt=10⁻³ | `main.tex:~626` | `figures/fe_load_limit.csv` 3.22092e-3 | match |
| reference inputs G=0.75, B=0.6, storage 17/80 | `finite_elements.tex:160–166` | recomputed: φ_s0μ_s=0.75; 1−K/K_s=0.6; (1−φ_s0)/K_f+S_s=0.2125 | match |
| example K_s=28K_*, μ_s=16.8K_*, B₀=(0.7000,0.7583,0.7917) | `experiments.tex:20–35` | I:C_s:I/9=28.0; trace-free modes {20,24,28,42.967,53.033}, mean/2=16.8; `build/weighted-stress/states.tex` row 1 = .7000/.7583/.7917 | match |
| fabric reconstruction 2.2e-16, det H−1 = −3.3e-16, ‖D:e₃‖=1.6e-16, D:e₆=0, rotation 2.5e-16 | `finite_elements.tex:280–288` | `site/reports/fabric-verification.json`: 2.2204e-16, −3.3307e-16, 1.5823e-16, 0.0, 2.4965e-16 | match |
| NumPy re-implementation worst diff 4.9e-15 | `finite_elements.tex:288–292` | `worst_probe_abs_diff = 4.8850e-15` | match |
| conformal-limit reproduction 1.9e-14 | `finite_elements.tex:293–295` | `conformal_cross_check` max abs diff 1.8742e-14 | match |
| peak centre pressures 4.36/4.99/5.52/3.62 ×10⁻⁵ | `finite_elements.tex:307–311` | `figures/fe_fabric_mandel_peak.csv` 4.3628/4.9901/5.5211/3.6164e-5 | match |
| refined peaks 3.61/4.35/4.97/5.50 ×10⁻⁵; maxima on X₁=0; zero at X₁=1 | `finite_elements.tex:326–330` | `figures/fe_fabric_contours.csv`: p_max 3.6062/4.3491/4.9737/5.5031e-5, p_max_x=0.0, p_min≈1e-127 | match |
| displacement peaks 5.18/5.14/2.38/5.26 ×10⁻⁵ | `finite_elements.tex:330–333` | same CSV `u_mag_max` | match |
| eleven evenly spaced Exodus snapshots | `finite_elements.tex:322` | `fe-evidence/runs/fabric_contour_a0/run.log`: Time Step 0…10, dt=0.0003 | match |
| peaks coincide with final state (no overshoot) | `finite_elements.tex:310` | peak = final in every peak row | match |
| Lambert / negative-pressure / large-positive checks | `experiments.tex:200–203` | `branch_pressure_-13/-14/800` Lambert + residual + stability checks present | match |

### 4.1 Hedge placement

Hedging is placed where the evidence stops and is, in my reading, **correct throughout**:

- Abstract: "no quantitative finite-deformation verification and no experimental validation are claimed for those demonstrations" (`main.tex:53–54`).
- `finite_elements.tex:381–399` ("Scope of these results") distinguishes implementation verification, finite-load demonstration, and validation, and states the fabric re-implementation "shares their modelling conventions".
- `finite_elements.tex:186–190`: the finite-deformation equations "need not reproduce its series at a finite load".
- `experiments.tex:194–196`: "Numerical differentiation supports implementation verification, not experimental validation or a proof of global stability"; "Local scalar stability does not establish stability against all deformation modes."
- `main.tex:~629`: "no order above one is asserted" for the scattered temporal orders.

I found **no claim asserted above the strength of its recorded evidence**, and no unhedged claim that the evidence contradicts.

---

## 5. REQUIRED items

### R3-C1 — `\(P_0\)` violates the stated subscript-0 rule

**Location:** `sections/finite_elements.tex:188` and `sections/finite_elements.tex:191`

The notation paragraph states (`main.tex:261–262`): "a subscript \(0\) marks a quantity of the reference
configuration, as in \(\phi_{s0}\) and \(\bar\rho_{s0}\)." I found **124** subscript-0 decorations; 122 are
reference-configuration quantities, and **2 are not**:

```
p&=P_0\cos(\pi X_1)\cos(\pi X_2)\sin t,      % finite_elements.tex:188
with \(U=P_0=0.01\).                          % finite_elements.tex:191
```

\(P_0\) is the manufactured-solution pressure **amplitude**, not a reference-configuration quantity.
A careful reader applying the stated rule would read \(P_0\) as a reference-state pressure and be misled.
(\(U\) at lines 184, 186, 191 is a scalar displacement amplitude.)

**Fix (either):** rename the amplitude (e.g. \(p_m\), \(\alpha_p\)) or \(\hat P\); or amend the notation
paragraph to except named amplitude constants introduced locally in the manufactured solution.

*Counts for the record:* subscript-0 = `\phi_{s0}` 92, `\bar\rho_{s0}` 6, `\bar\rho_{f0}` 4, `\Omega_0` 6,
`V_0` 5, `B_0` 3, `b_0` 2, `t_0` 2, `A_0` 2, **`P_0` 2** (plus one `\int_0`, which is an integral limit).

---

## 6. OPTIONAL notes

**R3-O1 — Mixed cross-reference styles.** `sections/experiments.tex:45, 75, 105, 129, 152` use
`Figure~\ref{fig:...}` and `main.tex:717` uses `section~\ref{sec:experiments}`, while the rest of the
manuscript uses `\cref`/`\Cref` (which is loaded with `nameinlink,noabbrev`). Consider uniform `\cref` for
consistent rendering of the reference name.

**R3-O2 — Dead macro.** `main.tex:11` defines `\let\tablerows\@@input`, but the manuscript contains no
`table`/`tabular` environment and never invokes `\tablerows`. The definition can be removed.

**R3-O3 — Underfull box in the bibliography.** The single box warning
(`Underfull \hbox (badness 1137)`, output page 30) is in `build/main.bbl`, not the body. Cosmetic only.

**R3-O4 — `\(U\)` vs `\(\mathbf U\)`.** The scalar MMS amplitude \(U\) (`finite_elements.tex:184, 186, 191`)
differs from the skeleton/mineral right stretches \(\mathbf U\), \(\bar{\mathbf U}\)
(`stress_reconstruction.tex:15–21`) by typeface alone. Distinguishable under the stated bold convention, but
an amplitude symbol such as \(a_u\) would remove the risk of misreading in the MMS equations.

**R3-O5 — Notation paragraph density.** `main.tex:215–280` encodes five distinct meanings of the bar, plus
the hat/tilde/prime scheme and the `d`/`dis`/`n`/`0` superscript-subscript rules, as ~66 lines of continuous
prose. The scheme is internally consistent, but a short lookup table (symbol → frame, normalization, rule)
would make it auditable at a glance, especially now that §`pore_fabric` adds `\bar{\mathbf S}_{\mathrm{dis}}`
whose bar follows the *work-conjugate-pair* clause rather than the frame clause.

**R3-O6 — Pointer to a sentence, not an equation.** `main.tex:263–265` cites
`\eqref{eq:fabric-phase-work}` for the identity
\(\widetilde{\mathbf\tau}=\mathbf R_A^T\mathbf\tau'\mathbf R_A\), but that identity appears in the prose sentence
preceding the labelled equation (`pore_fabric.tex:171–172`), not inside the numbered display. Either move the
identity into the display or adjust the pointer.

**R3-O7 — `\(n\)` overloaded.** The discrete time-level superscript \(n\) (`finite_elements.tex:120–122`)
and the unit normal \(\mathbf n\) (`experiments.tex:97–99`) share a letter (distinguished by typeface).

**R3-O8 — `\(K_*\)` not covered by the stated rules.** The reference stress unit \(K_*\) is introduced in
`experiments.tex:5` and used throughout, but the `*` subscript is not among the decorations defined in the
notation paragraph. A one-clause addition would close the gap.

---

## 7. Summary

- Integrity checks pass exactly (608/608, digest match); no listed file is missing or altered; no
  unexpected unlisted file is present.
- The build is clean and reproducible: no unresolved references or citations, no missing glyphs, no
  overfull boxes; the single underfull box is in the bibliography. A from-scratch rebuild reproduces the
  PDF's text byte-for-byte, differing only in producer metadata.
- The notation scheme is internally consistent and I verified it against all 199 `\bar`, 11 `\widehat`,
  4 `\widetilde`, 23 `^d`, 39 `_dis`, 6 `^n` and 124 subscript-0 occurrences. It has exactly one stated-rule
  exception (R3-C1).
- Every numerical claim I could test matched its recorded artifact exactly, including numbers that require
  nontrivial recomputation (μ_s = 16.8K_*, B = 0.6, storage 17/80, the 1.94 ratio, the 3.2×10⁻³ floor).
- Hedges are placed where the evidence stops, and I found no over-claim.

The required item is a small, local notation fix; nothing in the build, cross-referencing, or evidence
support blocks acceptance.

VERDICT: MINOR REVISION
