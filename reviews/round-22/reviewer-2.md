# Round 22 — Reviewer 2 (physics, source fidelity, packaging)

Reviewer role: independent reviewer 2 of 3. Focus: physics, source fidelity,
packaging. Prior-round verdicts do not carry; this is a full independent pass
on the post-editorial tree.

Frozen snapshot: `.agent-runtime/review-snapshots/round-22`, SNAPSHOT_ID
`68f3859a2c3f4ccaf73443f26869b0b86d3bf9b87cb18657365013687f55985d`, 550 files.

## 1. Snapshot integrity

- `sha256(source-manifest.json)` == SNAPSHOT_ID. **MATCH.**
- Re-hashed all 550 manifest entries. **550 OK, 0 missing, 0 mismatch.**

The snapshot is internally self-consistent at the top level: every file the
frozen source manifest declares is present and hashes as declared.

## 2. Shipped artifacts the manuscript references

The manuscript (`main.tex`), the companion site, and the supplement archive
reference a set of evidence artifacts. I verified each against its *own*
declared digest.

### 2.1 `fe-evidence/manifest.json` — FAILS (85 stale digests)

The manifest declares 293 files across 53 run directories. 208 hash correctly;
**85 do not**, and all 85 are the pore-fabric runs and `conformal_probe_ref`:

- `fabric_probe_iso/a0/a45/a90`, `fabric_probe_conformal`,
  `fabric_probe_coup_a0/a45/a90`, `fabric_probe_softaxial`,
  `fabric_probe_stiffaxial`
- `fabric_mandel_iso`, `fabric_mandel_coup_a0/a45/a90`
- `conformal_probe_ref`

For these the declared `input.i`, `analysis.json`, `provenance.json`,
`run.log`, `solution.csv` and `solution_profile_*.csv` hashes all mismatch the
on-disk files. Example: `runs/fabric_probe_iso/solution.csv` is declared
`847bb77404…` but the on-disk file is `aac49316…`. The declared hashes for the
fabric `input.i` files are byte-identical across all angles (`00ca5c61…`),
which is itself a red flag: the shipped inputs differ per case but the manifest
records a single shared hash. The manifest is stale relative to the current
run tree.

### 2.2 `site/scientific-snapshot.json` — FAILS (5 stale digests)

41 files declared; 36 OK, **5 mismatch**:
`moose_app/include/utils/FabricLaw.h`,
`moose_app/src/materials/FabricMaterial.C`,
`examples/verify_fabric.py`,
`moose_app/inputs/fabric_probe.i`,
`moose_app/inputs/fabric_mandel.i`.

### 2.3 `site/evidence.json` — FAILS (8 stale digests)

Artifact list: 24 OK, **8 mismatch**, all fabric-related:
`fabric-law-source`, `fabric-material-source`, `fabric-verify-script`,
`fe-fabric-probe`, `fe-fabric-probe-data`, `fe-fabric-mandel`,
`fe-fabric-mandel-history`, `fe-fabric-mandel-peak`.

### 2.4 `site/reports/fabric-verification.json` — stale content

Its recorded "moose" field values match the *stale archive* run data, not the
on-disk runs. For `fabric_probe_iso`, `sigma22 = -0.0202258…` (archive) vs
`-0.0224758…` (on-disk). This report was not regenerated with the current law.

## 3. Supplement archive

### 3.1 PDF attachment == on-disk archive — MATCH

`build/main.pdf` embeds one attachment (`/Type/EmbeddedFile`, `application/zip`,
`Size 312480`). Decompressing the embedded stream yields SHA-256
`f24b3d01…`, identical to `build/anisotropic-biot-2026-09-20-v2.zip` on disk,
and its `CheckSum` field equals `md5` of the on-disk archive. Good.

### 3.2 Archive name — MATCH

`main.tex` (`\embedfile[filespec=anisotropic-biot-2026-09-20-v2.zip,…]`) and
`README.md` both reference `anisotropic-biot-2026-09-20-v2.zip`; that file
ships at `build/anisotropic-biot-2026-09-20-v2.zip`.

### 3.3 Archive internal manifest — self-consistent

The archive's own `manifest.json` declares 57 files; all 57 hash correctly
internally (`manifest.json` itself is the only unlisted entry). The archive is
internally coherent.

### 3.4 Archive content is STALE relative to the shipped source — FAILS

This is the core packaging defect. The archive ships an **older** version of the
pore-fabric law than the manuscript's current sources and figures:

| File | archive (stale) | on-disk (current) |
|---|---|---|
| `FabricLaw.h` | `e57f4bdf…` ("transversely isotropic", `NDIR=5`) | `2953669c…` ("axisymmetric", `NDIR=2`) |
| `FabricMaterial.C` | `fd343519…` (5 moduli: in-plane + shear params) | `9abcfab6…` (2 moduli) |
| `fabric_probe.i` | `00ca5c61…` (has `fabric_inplane_modulus`, `fabric_shear_modulus`) | `49ae9a76…` (removed) |
| `fabric_mandel.i` | `89be4736…` | `a1ae9148…` |
| `verify_fabric.py` | `d9194f7c…` (5-direction basis) | `d6265788…` (2-direction axisymmetric basis) |
| fabric `solution.csv` | old values | new values |

The archive also ships the **stale** `fe-evidence/runs/*/solution.csv` for the
fabric cases (e.g. `fabric_probe_iso/solution.csv` = `847bb774…`), so its
recorded run histories no longer match the source it ships alongside.

### 3.5 Documented regeneration from the archive — does NOT reproduce the shipped figures

I extracted the archive to a temp dir outside the checkout and ran its
documented commands (`verify_fabric.py`, then
`plot_fabric_results.py --runs fe-evidence/runs --output build/fabric-plots`).
Both exit 0 and emit a fabric probe figure and CSVs — but the emitted CSVs
**differ** from the shipped `figures/fe_fabric_probe.csv` and
`figures/fe_fabric_mandel_peak.csv`:

- Archive-regenerated `fe_fabric_probe.csv` has `energy=0.0001013…` and
  `sigma22=-0.0202258…` for the iso case, and for `coup_a45` gives
  `drained_c11=0.723372…, drained_c12=+0.123372…`.
- Shipped `figures/fe_fabric_probe.csv` has `energy=0.0001070…`,
  `sigma22=-0.0224758…`, and `coup_a45` gives `drained_c11=1.285872…,
  drained_c12=-0.214128…`.

Regenerating from the **on-disk** `fe-evidence/runs` reproduces the shipped
`fe_fabric_probe.csv` and `fe_fabric_mandel_peak.csv` byte-for-byte. So the
shipped figures are consistent with the on-disk run tree, but the supplement
archive — the artifact a reader would actually regenerate from — produces a
different, superseded result. **The supplement does not reproduce the
manuscript's figures.**

## 4. Physics and source fidelity

### 4.1 Manuscript text quotes numbers its own shipped figures contradict — FAILS

`finite_elements.tex` (sec:fe-fabric) states the rotated-fabric coupled runs
give peak center pressure
`6.28×10⁻⁵` (fabric axis along X₁), `5.10×10⁻⁵` at 45°, `3.95×10⁻⁵` along the
other in-plane axis, against `5.13×10⁻⁵` uncoupled.

These four numbers match the **stale archive** runs exactly
(`6.2803e-5, 5.1022e-5, 3.9461e-5, 5.1326e-5`) but **not** the shipped figure
data `figures/fe_fabric_mandel_peak.csv`, which records
`4.3761e-5 (0°), 4.9826e-5 (45°), 5.4979e-5 (90°), 3.6523e-5 (uncoupled)`.
The shipped figure shows peak pressure *increasing* with orientation, the text
claims it *decreases* (6.28 at X₁ → 3.95 at the in-plane axis). The text and
its own figure are inconsistent, and the qualitative trend is reversed.

### 4.2 Manuscript theory section contradicts the implemented law — FAILS

`pore_fabric.tex` (sec:fabric-biot) describes the implemented law as "the
five-modulus transversely isotropic 𝔻 … full rank on the volumetric, axial,
in-plane-deviatoric and the two shear directions it retains," while two
paragraphs later (sec:fabric-transverse) it says the directional coupling is
carried by "the two-parameter energy." The compiled `FabricLaw.h` is
`NDIR=2` (axisymmetric: volumetric + axial only, four modes frozen), matching
the *two-parameter* description, not the *five-modulus* one. The theory text
describing a five-modulus full-rank law is stale relative to the shipped code
and contradicts the shipped evidence.

## 5. Overclaim / comparability check

The manuscript and `site/evidence.json` are appropriately scoped here: they
explicitly label the rotated-anisotropy, partial-drainage and rotated-fabric
runs as "demonstrations, not quantitative verification," mark physical
validation "not_performed," and note the square-domain partial-drainage case is
"not comparable" to the slender Mandel reference. I found no overclaim in the
scoping language. The defects above are *fidelity* defects (stale archive,
stale manifests, text/figure disagreement), not overclaim.

## Summary

The physics is carefully scoped, and the frozen snapshot is top-level
self-consistent. But the fabric-law revision (five-modulus → two-parameter
axisymmetric) was only partially propagated: the shipped source, the on-disk
run tree, and the shipped figures were updated, while the supplement archive,
all three evidence manifests (`fe-evidence/manifest.json`,
`site/scientific-snapshot.json`, `site/evidence.json`), the fabric verification
report, and the manuscript's own peak-pressure figures and theory description
were left stale. The supplement a reader regenerates does not reproduce the
manuscript's figures, and the manuscript text quotes numbers its shipped figures
contradict. These are release-blocking packaging and source-fidelity failures.

---

VERDICT: MAJOR REVISION

## Required corrections

1. **Regenerate the supplement archive** (`build/anisotropic-biot-2026-09-20-v2.zip`)
   to ship the current axisymmetric (`NDIR=2`) `FabricLaw.h`, `FabricMaterial.C`,
   `fabric_probe.i`, `fabric_mandel.i`, `verify_fabric.py`, and the current
   fabric `solution.csv` run histories; re-embed the regenerated archive in the
   PDF so the attachment equals the on-disk archive and reproduces the shipped
   figures.

2. **Regenerate `fe-evidence/manifest.json`** so all 85 stale fabric-run digests
   (and `conformal_probe_ref`) match the on-disk files.

3. **Regenerate `site/scientific-snapshot.json`** so the 5 stale digests
   (`FabricLaw.h`, `FabricMaterial.C`, `verify_fabric.py`, `fabric_probe.i`,
   `fabric_mandel.i`) match the on-disk files.

4. **Regenerate `site/evidence.json`** so the 8 stale fabric artifact digests
   match the on-disk files.

5. **Regenerate `site/reports/fabric-verification.json`** (and any other
   fabric report) from the current on-disk runs so its recorded values match the
   shipped source and figures.

6. **Reconcile the manuscript text with the shipped figures.** Update the
   `finite_elements.tex` peak center pressures (currently `6.28/5.10/3.95/5.13
   ×10⁻⁵`) to the shipped figure values (`4.376/4.983/5.498/3.652 ×10⁻⁵`), or
   regenerate the figures to match the text. The current text and figure disagree
   and the anisotropy trend is reversed.

7. **Reconcile the theory description with the implemented law.** In
   `pore_fabric.tex`, replace or qualify the "five-modulus … full rank on the
   volumetric, axial, in-plane-deviatoric and the two shear directions"
   description so it matches the shipped two-parameter axisymmetric law
   (`NDIR=2`), eliminating the internal contradiction with the "two-parameter
   energy" sentence.

## Optional suggestions

- Add a packaging-time assertion that the supplement archive's regenerated
  figures/CSVs match the shipped `figures/` byte-for-byte (or within documented
  tolerance), so this class of drift is caught automatically.
- In the fabric manifests, record per-case input-deck digests rather than a
  single shared hash, so angle-dependent input edits cannot silently share a
  digest.
- Note the fabric-law revision explicitly in `README.md` (the "archived earlier
  formulation" note currently covers only `finite_pressure.py`, not the
  five-modulus → axisymmetric fabric change).
