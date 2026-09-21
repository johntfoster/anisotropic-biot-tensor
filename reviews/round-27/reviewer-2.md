# Round-27 Independent Review — Reviewer 2
## Emphasis: physics / source fidelity / packaging

Working copy: `/tmp/r27-rev2` (copied from the frozen snapshot; the snapshot and the
repository tree were not modified). Read-only except for this report.

---

## 1. Snapshot and integrity

1. **Snapshot identity.** `SNAPSHOT_ID` = `c5050c77dd04628f149ddc417cce99eb6b53c4315884974efc6331c3267eda5e`,
   and `sha256(source-manifest.json)` reproduces that value exactly. The declared
   snapshot id is therefore genuine.

2. **Manifest re-hash.** I re-hashed every one of the 591 entries in
   `source-manifest.json` myself:
   - **591 / 591 re-hashed OK**
   - missing: **0**
   - digest mismatch: **0**
   - extra files on disk not in the manifest (excluding `source-manifest.json` and
     `SNAPSHOT_ID`): **0**

   The snapshot is bit-exact and self-consistent.

3. **Nested evidence digests** (re-hashed independently, not trusted from prose):
   - `site/evidence.json` artifacts: **41/41** digests resolve, 0 mismatches.
   - `site/scientific-snapshot.json` files: **47/47** resolve, 0 mismatches.
   - `fe-evidence/manifest.json` files: **317/317** resolve with matching byte sizes;
     all **57** run directories under `fe-evidence/runs/` are registered, 0 unregistered.
   - Supplement archive `build/anisotropic-biot-2026-09-20-v2.zip` `manifest.json`
     `sha256` map: **68/68** resolve, 0 mismatches, 0 unlisted extras.

**Snapshot re-hashed clean: yes.**

---

## 2. Findings

No required defects were found. The itemized checks that support this are in
sections 3–5; the two non-blocking observations are recorded under OPTIONAL
corrections in section 6.

---

## 3. Source-fidelity spot checks

1. **Citation existence and characterization.** All 35 distinct keys cited in
   `main.tex` + `sections/*.tex` are present in `references.bib`; no undefined
   citations (`build/main.log` shows no undefined-reference warnings, and the
   rendered PDF contains no `??`). I verified 30 of the load-bearing DOIs against
   Crossref, confirming title, journal, volume, and pages:

   | key | Crossref result | matches bib |
   |---|---|---|
   | `fosterxu2025` | JMPS 204, 106263, 2025 | yes |
   | `cowin2004fabric` | Mech. Mater. 36, 665–677, 2004 | yes |
   | `cowin1985fabric` | Mech. Mater. 4, 137–147, 1985 | yes |
   | `gajo2010` | Proc. R. Soc. A 466, 3061–3087, 2010 | yes |
   | `drumheller2000` | Int. J. Eng. Sci. 38, 347–382, 2000 | yes |
   | `thompsonwillis1991` | J. Appl. Mech. 58, 612–616, 1991 | yes |
   | `hudson1981`, `turnercowin1987`, `cowinmehrabadi2007`, `moesencardosocowin2012`, `debuhan1998`, `walker2023poroelasticity`, `rudgekelemen2010`, `jons2017`, `uno2022`, `putnis2002`, `putnis2009`, `ruizagudo2014`, `geisler2007`, `altreewilliams2015`, `cheng1997`, `wong2017`, `braun2020`, `sviridov2017`, `makhnenkolabuz2016`, `zhaoborja2020`, `macminnetal2016`, `chaubazantsu2016`, `flory1961`, `zha1996forsterite`, `dehghanipentamerodio2019`, `dehghanizilian2021` | all confirmed real | yes |

   No fabricated or mischaracterized citation was found. The two fabric-poroelasticity
   references (`cowin2004fabric`, `cowinmehrabadi2007`) are correctly described as
   assigning fabric-dependent coefficients to the solid at small strain — the
   manuscript's differentiator (fabric entering the distention energy instead) is
   accurately stated.

2. **Novelty differentiation is bounded.** The Introduction says "we are not aware
   of a tensorial distention law …" and explicitly distinguishes its route from the
   fabric-elasticity constructions it surveys. This is an appropriately hedged
   negative claim, not an absolute priority assertion.

3. **Availability / reproducibility claims match the shipped archive.** The
   `\paragraph{Code and data availability}` text promises the archive ships
   `FabricLaw.h`, `FabricMaterial.h`, `FabricMaterial.C`, the `fabric_probe.i`,
   `conformal_probe.i`, `fabric_mandel.i` decks, and "the recorded run histories
   those scripts read", and states the remaining FE sources are *not* in the archive.
   Every one of those files is present in the zip; only the pore-fabric subset of
   `moose_app/` plus the fabric run histories are shipped, exactly as promised. The
   README reproduction commands correspond to scripts that exist in the archive, and
   the archive's own `README.md` states the self-contained scope consistently.

**Source fidelity: clean.**

---

## 4. Physics assessment

1. **Construction.** The multiplicative split `F = A F̄` with
   `A = a^{1/3} R_A` (`R_A` proper) is internally consistent: `C̄ = a^{-2/3} C` is
   independent of `R_A`, so with a volume-only distention energy the internal
   rotation drops out of the energy, the mineral-volume equation, and `B`. The
   manuscript states this specialization explicitly and repeatedly marks the
   conformal and tensorial steps as *modeling choices* rather than consequences of
   stress symmetry (Discussion; `site/evidence.json` limitations). This is physically
   sound and honestly framed.

2. **Reference Biot tensor, independently recomputed.** Using the manuscript's
   `C_s` (eq. example-mineral-stiffness) and the recorded `C^d`, I recomputed
   `B_0 = I − C^d : C_s^{-1} : I`:
   - recomputed `B_0 = [0.700000, 0.758333, 0.791667]`
   - manuscript states `0.7000, 0.7583, 0.7917` — **match**.
   The drained-stiffness restriction and the rank-one compliance restriction both
   reproduce to machine precision against the recorded `C^d`
   (max |Δ| = 1.8e-15 and 1.4e-17).

3. **Isotropic-comparison shear modulus.** The claim "16.8 K_*, the mean of the five
   deviatoric stiffness modes of C_s, divided by two" checks out: the five deviatoric
   Mandel modes of `C_s` are {20, 24, 28, d1, d2} with d1+d2 = 180−84 = 96, so the mean
   is 33.6 and half of it is 16.8. The comparison mineral is isotropic with
   `K_s = 28`, `μ = 16.8`.

4. **FE reference inputs.** `K = 1`, `K_s = 2.5`, `φ_s0 = 0.9`, `K_f = 8` give
   `B = 1 − K/K_s = 0.6`, drained shear `G = φ_s0 μ_s = 0.75`, and total storage
   `(1−φ_s0)/K_f + S_s = 0.0125 + 0.2 = 0.2125 = 17/80` — all match the stated values.

5. **Recorded probe evidence supports the anisotropy claim.**
   - Fabric probe (`figures/fe_fabric_probe.csv`): with an isotropic mineral and no
     volume–axial coupling, `B_par = B_per = 0.883871`, anisotropy `≈ 1.1e-16`.
     With coupling 0.4, `B_par = 0.850654`, `B_per = 0.910270`, anisotropy
     `= −0.059616`. The directionality is therefore genuinely supplied by the
     volume–axial modulus, exactly as the text says.
   - Coupled rotated-fabric consolidation (`figures/fe_fabric_mandel_peak.csv`,
     cross-checked against `fe-evidence/runs/fabric_mandel_*`): peak centre pressure
     `3.6164e-5` (no coupling), `4.3628e-5` (0°), `4.9901e-5` (45°), `5.5211e-5` (90°).
     The manuscript quotes `3.62 / 4.36 / 4.99 / 5.52 × 10^{-5}` — **match**, and in
     every case the peak equals the final recorded value (no unstated transient
     overshoot). The mineral is isotropic and unrotated, so the directional spread is
     correctly attributed to the pore fabric.
   - Refined 40×8 contour runs (`figures/fe_fabric_contours.csv`): `p_max =`
     `3.6062 / 4.3491 / 4.9737 / 5.5031 × 10^{-5}`; manuscript quotes
     `3.61 / 4.35 / 4.97 / 5.50 × 10^{-5}` — **match**; `p_max_x = 0` in every case,
     consistent with "maximum lies on the X1 = 0 symmetry line". Displacement peaks
     `5.1826 / 5.1372 / 2.3818 / 5.2587 × 10^{-5}` vs quoted `5.18 / 5.14 / 2.38 / 5.26`
     — **match**.

6. **Supporting numerical claims reproduced from the frozen artifacts.**
   - Conformal suite: `checks_passed = 186` and
     `max_constitutive_identity_error = 2.455e-9` (manuscript: 186 checks, 2.5e-9).
   - Spherical-gauge suite: `materials = 13`, `total_states = 273`
     (manuscript: "273 finite states across 13 mineral stiffnesses").
   - Fabric symmetry checks (`build/fabric/fabric-verification.json`):
     `D: e3 = 1.58e-16` (text 1.6e-16), `D: e6 = 0`, rotation invariance `2.50e-16`
     (text 2.5e-16), H-reconstruction diff `2.22e-16` (text 2.2e-16),
     det H − 1 `= −3.33e-16` (text −3.3e-16), worst probe abs diff `4.88e-15`
     (text 4.9e-15), conformal-limit cross-check max `1.87e-14` (text 1.9e-14).
   - MMS spatial naive orders: ux `2.99/2.96`, uy `3.00/2.96`, p `2.00/2.00`
     (text matches). Fixed-mesh successive-difference temporal orders span
     `0.98–1.40` across nx = 16/32/64 (matches the text's stated range, with the text
     explicitly declining to assert any order above one).
   - Linear step refinement: `3.658e-3` (dt=1e-3) vs `7.104e-3` (dt=2e-3),
     ratio `1.94` (text: 3.7e-3, 7.1e-3, ratio 1.94).
   - Finite-load floor: `nonlinear_load_0.0001` pressure `3.221e-3` (text ~3.2e-3).
   - Mandel reference: 38 self-checks passed, central overshoot ratio `1.054659` at
     `t = 0.01516535` (text: 5.4659% at t = 0.01516535).

7. **Overclaim audit.** Every finite-load coupled result is explicitly labeled a
   demonstration; the manuscript states "no quantitative finite-deformation
   verification and no experimental validation are claimed for those
   demonstrations", and that the fabric law is checked only at the material point
   against an implementation that shares the section's conventions. I found no
   statement that exceeds the recorded, bounded evidence.

**Physics: sound, and the anisotropy and coupling claims are supported by the
recorded probes.**

---

## 5. Packaging

1. **F1 repair is real and operates in the correct order.** I reproduced the state
   by running, in a scratch copy, `tools/populate_site_manifest.py` followed by
   `tools/register_fabric_evidence.py`. The resulting `site/evidence.json`,
   `site/scientific-snapshot.json`, and `fe-evidence/manifest.json` are **byte-identical**
   to the frozen versions (the only field that differs is
   `provenance.source_revision`, which is a git hash and necessarily differs in a
   fresh scratch repo; every other field matches exactly).
   - After `populate` alone: 23 artifacts, no pore-fabric artifacts,
     45 snapshot files (the base state).
   - After `populate` then `register`: 41 artifacts, 13 figures, 47 snapshot files —
     equal to frozen.
   - **Order matters and is verified**: running `register` then `populate`
     (reverse) collapses back to 23 artifacts / 45 snapshot files, dropping the
     pore-fabric registrations. The documented order is the working one.

2. **Pore-fabric registration is complete.** `site/evidence.json` registers the
   pore-fabric report (`fabric-verification`), the fabric figures
   (`fe-fabric-probe`, `fe-fabric-mandel`, `fe-fabric-contours`, `fe-fabric-diffusion`),
   their CSV data, the fabric source files (`FabricLaw.h`, `FabricMaterial.C`,
   `verify_fabric.py`, `plot_fabric_contours.py`), the new FE-verification figures
   (`fe-verification-convergence`, `fe-reference-comparison`), and the refined deck
   (`fabric_contour.i`). All reference the correct repository paths, all 41 digests
   resolve, and there are no dangling artifact ids in `figures`, `cases`, or category
   `evidence` lists.

3. **Manifest validation passes.** `tools/build_verification_site.py --validate-only`
   reports `{"manifest": "valid", "artifacts": 41, "scientific_checks_executed": false}`.

4. **Supplement archive is consistent with the availability text.**
   `build/anisotropic-biot-2026-09-20-v2.zip` has a 68-entry manifest whose digests
   all resolve and which lists every payload file (0 extras). It contains the
   promised fabric law/material/decks, the recorded fabric run histories and the
   refined contour Exodus files, and it correctly omits the rest of the FE
   application. The archive `README.md` reproduction commands match the shipped
   scripts.

5. **PDF packaging.** `build/main.pdf` is 33 pages, builds with no undefined
   references, and embeds exactly one attachment,
   `anisotropic-biot-2026-09-20-v2.zip`, matching the `\embedfile` entry and the
   "numerical supplement" text. Every figure path referenced by
   `sections/*.tex` exists under `figures/` or `build/conformal/`.

**Packaging: complete and reproducible.**

---

## 6. REQUIRED and OPTIONAL corrections

### REQUIRED corrections
**None.** The snapshot re-hashes clean, all digests resolve with 0 mismatches, the
F1 repair reproduces byte-for-byte in the documented order and fails in the reverse
order, the numerical claims I checked reproduce from the frozen artifacts under
their stated scope, the citations are real and correctly characterized, and the
availability/packaging claims match what the archive actually ships. ACCEPT is
withheld only when a required correction exists; none does.

### OPTIONAL corrections (not blocking, no evidence or physics impact)
1. **Snapshot curation drops one populate input.** `build/fluid-coupling/verification.json`
   exists in the repository but is not in the frozen snapshot, so running the F1
   pipeline *from the snapshot alone* (rather than from the repo) yields 40 artifacts
   instead of 41 because `populate_site_manifest.py` silently skips the missing
   source. From the repository (which has the file), the pipeline reproduces exactly.
   If snapshot-only rebuildability is desired, add that file to the snapshot's
   tracked build inputs.
2. **`braun2020` key/entry year mismatch (cosmetic).** The citation key says 2020
   while the entry year is 2021 (online 2020, issue 2021). Keys need not encode the
   year, so this is harmless; renaming to `braun2021` would remove the ambiguity.
3. **Stale local note (not in the manuscript).** `AGENTS.md` records `fosterxu2025`
   as JMPS 204:105259; the bibliography and Crossref both give 106263. The manuscript
   is correct; only the internal note is stale.

---

VERDICT: ACCEPT
