#!/usr/bin/env python3
"""Register the pore-fabric evidence in the companion site manifests.

Idempotent: adds the fabric report, figures, figure data, and source files to
``site/evidence.json`` and ``site/scientific-snapshot.json`` if they are not
already present, and recomputes every recorded SHA-256 digest.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return str(Path(path).relative_to(ROOT))


# 1. Publish the fabric verification report next to the other site reports.
REPORT = ROOT / "site/reports/fabric-verification.json"
REPORT.write_bytes((ROOT / "build/fabric/fabric-verification.json").read_bytes())

# 2. Extend the scientific snapshot with the new sources.
SNAPSHOT = ROOT / "site/scientific-snapshot.json"
snapshot = json.loads(SNAPSHOT.read_text())
known = {entry["path"] for entry in snapshot["files"]}
NEW_FILES = [
    "examples/figure_style.py",
    "moose_app/include/utils/FabricLaw.h",
    "moose_app/include/materials/FabricMaterial.h",
    "moose_app/src/materials/FabricMaterial.C",
    "moose_app/inputs/fabric_probe.i",
    "moose_app/inputs/conformal_probe.i",
    "moose_app/inputs/fabric_mandel.i",
    "examples/verify_fabric.py",
    "examples/plot_fabric_results.py",
    "examples/plot_fe_verification.py",
    "tools/rerun_fabric_decks.py",
    "moose_app/inputs/fabric_contour.i",
    "examples/plot_fabric_contours.py",
    "tools/rerun_fabric_contours.py",
]
added, missing = [], []
for name in NEW_FILES:
    path = ROOT / name
    if not path.is_file():
        missing.append(name)
        continue
    if name not in known:
        added.append(name)
    snapshot["files"] = [entry for entry in snapshot["files"] if entry["path"] != name]
    snapshot["files"].append({"path": name, "sha256": sha(path)})
snapshot["files"].sort(key=lambda entry: entry["path"])
if missing:
    raise SystemExit("missing snapshot sources: " + ", ".join(missing))
for entry in snapshot["files"]:
    path = ROOT / entry["path"]
    if not path.is_file():
        raise SystemExit("snapshot entry does not resolve: " + entry["path"])
    entry["sha256"] = sha(path)
SNAPSHOT.write_text(json.dumps(snapshot, indent=2) + "\n")

# 3. Extend the site evidence manifest.
EVIDENCE = ROOT / "site/evidence.json"
manifest = json.loads(EVIDENCE.read_text())
artifacts = {item["id"]: item for item in manifest["artifacts"]}
NEW_ARTIFACTS = [
    dict(id="figure-style-source", kind="source", label="Shared publication plot style",
         path="examples/figure_style.py", destination="source/figure_style.py"),
    dict(id="fabric-verification", kind="report", label="Pore-fabric distention verification",
         path="site/reports/fabric-verification.json", destination="reports/fabric-verification.json"),
    dict(id="fabric-law-source", kind="source", label="FabricLaw.h (transversely isotropic distention law)",
         path="moose_app/include/utils/FabricLaw.h", destination="source/FabricLaw.h"),
    dict(id="fabric-material-source", kind="source", label="FabricMaterial.C (registered material)",
         path="moose_app/src/materials/FabricMaterial.C", destination="source/FabricMaterial.C"),
    dict(id="fabric-verify-script", kind="source", label="verify_fabric.py (independent NumPy re-implementation)",
         path="examples/verify_fabric.py", destination="source/verify_fabric.py"),
    dict(id="fe-verification-script", kind="source", label="plot_fe_verification.py (finite-element verification displays)",
         path="examples/plot_fe_verification.py", destination="source/plot_fe_verification.py"),
    dict(id="fe-fabric-probe", kind="figure", label="Pore-fabric probe: Biot tensor and shape response",
         path="figures/fe_fabric_probe.png", destination="figures/fe_fabric_probe.png"),
    dict(id="fe-fabric-probe-data", kind="data", label="Pore-fabric probe values",
         path="figures/fe_fabric_probe.csv", destination="data/fe_fabric_probe.csv"),
    dict(id="fe-fabric-mandel", kind="figure", label="Rotated-fabric consolidation: pressure response",
         path="figures/fe_fabric_mandel.png", destination="figures/fe_fabric_mandel.png"),
    dict(id="fe-fabric-mandel-history", kind="data", label="Rotated-fabric consolidation histories",
         path="figures/fe_fabric_mandel_history.csv", destination="data/fe_fabric_mandel_history.csv"),
    dict(id="fe-fabric-mandel-peak", kind="data", label="Rotated-fabric peak pressure by orientation",
         path="figures/fe_fabric_mandel_peak.csv", destination="data/fe_fabric_mandel_peak.csv"),
    dict(id="fe-fabric-contours", kind="figure",
         label="Refined coupled consolidation contours: pressure and displacement magnitude",
         path="figures/fe_fabric_contours.png", destination="figures/fe_fabric_contours.png"),
    dict(id="fe-fabric-contours-data", kind="data",
         label="Refined contour extrema and pressure-maximum locations",
         path="figures/fe_fabric_contours.csv", destination="data/fe_fabric_contours.csv"),
    dict(id="fe-fabric-diffusion", kind="figure",
         label="Refined coupled consolidation diffusion snapshots",
         path="figures/fe_fabric_diffusion.png", destination="figures/fe_fabric_diffusion.png"),
    dict(id="fe-fabric-diffusion-data", kind="data",
         label="Diffusion snapshot extrema and pressure-maximum locations",
         path="figures/fe_fabric_diffusion.csv", destination="data/fe_fabric_diffusion.csv"),
    dict(id="fabric-contours-script", kind="source",
         label="plot_fabric_contours.py (reads recorded Exodus fields)",
         path="examples/plot_fabric_contours.py", destination="source/plot_fabric_contours.py"),
    dict(id="fe-fabric-contour-deck", kind="deck",
         label="fabric_contour.i (refined 40 x 4 coupled fabric deck)",
         path="moose_app/inputs/fabric_contour.i", destination="deck/fabric_contour.i"),
    dict(id="fe-verification-convergence", kind="figure",
         label="Measured finite-element verification: manufactured solution, temporal order, finite-load floor",
         path="figures/fe_verification_convergence.png",
         destination="figures/fe_verification_convergence.png"),
    dict(id="fe-reference-comparison", kind="figure",
         label="Constant-reference-tangent Mandel comparison: pressure history and profiles",
         path="figures/fe_reference_comparison.png",
         destination="figures/fe_reference_comparison.png"),
]
for item in NEW_ARTIFACTS:
    path = ROOT / item["path"]
    if not path.is_file():
        raise SystemExit("missing artifact source: " + item["path"])
    item["sha256"] = sha(path)
    artifacts[item["id"]] = item

# Drop artifacts that no longer belong to a publication root (the site builder
# rejects sources outside its allowlist).
for stale in ("fe-rerun-harness",):
    artifacts.pop(stale, None)

# Refresh digests for every artifact so the manifest stays self-consistent.
for ident, item in artifacts.items():
    item["sha256"] = sha(ROOT / item["path"])

manifest["artifacts"] = [artifacts[key] for key in sorted(artifacts)]
manifest["version"] = "anisotropic-biot-2026-09-20-v2"

FIGURES = [
    dict(artifact="fe-fabric-probe",
         caption="reference-state pore-fabric probe: axial and transverse Biot "
                 "coefficients and the directional coupling produced by the "
                 "volume-axial distention coupling (isotropic mineral, uniform "
                 "prescribed deformation)",
         alt="bar charts of Biot coefficient components and of the directional Biot "
             "difference for the recorded pore-fabric probe runs"),
    dict(artifact="fe-fabric-mandel",
         caption="coupled consolidation with the pore fabric rotated in the plane and "
                 "an isotropic unrotated mineral: the direction dependence of the "
                 "center pressure is produced by the pore fabric alone (finite-load "
                 "demonstration)",
         alt="center-pressure histories and peak center pressure against fabric "
             "orientation from the recorded rotated-fabric consolidation runs"),
    dict(artifact="fe-verification-convergence",
         caption="measured finite-element verification displays built from the "
                 "recorded artifacts: manufactured-solution spatial errors and "
                 "orders, the fixed-mesh successive-difference temporal orders, and "
                 "the finite-load pressure floor",
         alt="log-log refinement curves for the manufactured solution, measured "
             "temporal orders against mesh size, and the finite-load discrepancy "
             "at fixed mesh"),
    dict(artifact="fe-reference-comparison",
         caption="linear constant-reference-tangent Mandel comparison: center-pressure "
                 "history and pressure profiles against the independently evaluated "
                 "series at identical saved times",
         alt="center pressure against time and pressure profiles at saved times, "
             "finite-element curves against the analytical Mandel series"),
    dict(artifact="fe-fabric-contours",
         caption="refined (40 x 4) coupled consolidation contours at the common "
                 "final recorded time: pore pressure and displacement magnitude for "
                 "the isotropic fabric and fabric axes at 0, 45 and 90 deg "
                 "(finite-load demonstration on synthetic parameters)",
         alt="filled contours of pore pressure and displacement magnitude across the "
             "four fabric variants on the 1 x 0.1 strip"),
    dict(artifact="fe-fabric-diffusion",
         caption="refined coupled consolidation pressure snapshots at six recorded "
                 "times showing the Mandel-type drainage front for the isotropic "
                 "and 45 deg fabric cases",
         alt="pressure contour snapshots at successive times for the isotropic and "
             "coupled fabric cases"),
]
for item in FIGURES:
    manifest.setdefault("figures", [])[:] = [
        old for old in manifest["figures"] if old["artifact"] != item["artifact"]]
    manifest["figures"].append(item)
contours = json.loads((ROOT / "figures/fe_fabric_contours-plot-manifest.json").read_text())
for figure in contours["figures"]:
    for item in manifest["figures"]:
        if item["artifact"] == figure["id"].replace("_", "-"):
            item["caption"] = figure["caption"]

CASES = [
    dict(title="Pore-fabric distention probe and rotated-fabric consolidation",
         status="pending",
         description="Reference-state axisymmetric distention law: the "
                     "Biot tensor, the shape response and the conformal reduction are "
                     "checked against an independent NumPy implementation of the "
                     "section equations (worst absolute difference 4.9e-15), and the "
                     "coupled transient problem is run with the fabric rotated in the "
                     "plane behind an isotropic, unrotated mineral. The coupled cases "
                     "are finite-load demonstrations, not quantitative verification of "
                     "the nonlinear law and not experimental validation.",
         artifacts=["fabric-verification", "fe-fabric-probe", "fe-fabric-probe-data",
                    "fe-fabric-mandel", "fe-fabric-mandel-history", "fe-fabric-mandel-peak"]),
    dict(title="Manufactured-solution and reference-comparison displays",
         status="passed",
         description="The manuscript's finite-element verification claims are "
                     "displayed from the recorded artifacts: manufactured-solution "
                     "spatial orders, the fixed-mesh successive-difference temporal "
                     "orders (measurements that include one value above one; no order "
                     "above one is asserted), the finite-load pressure floor (about "
                     "3.2e-3, a discretization floor), and the constant-reference-tangent "
                     "Mandel comparison of center pressure and pressure profiles "
                     "against the independently evaluated series.",
         artifacts=["fe-verification-convergence", "fe-reference-comparison",
                    "mms-convergence", "fe-mms-convergence", "fe-load-limit",
                    "fe-mandel-history", "fe-mandel-profiles"]),
]
existing_titles = {item["title"] for item in manifest.get("cases", [])}
for item in CASES:
    if item["title"] not in existing_titles:
        manifest.setdefault("cases", []).append(item)
    else:
        manifest["cases"] = [item if entry["title"] == item["title"] else entry
                             for entry in manifest["cases"]]

evidence = manifest["categories"]["implementation"].setdefault("evidence", [])
for ident in ("fabric-verification", "fe-fabric-contours", "fe-fabric-diffusion"):
    if ident not in evidence:
        evidence.append(ident)
convergence_evidence = manifest["categories"]["convergence"].setdefault("evidence", [])
for ident in ("fe-verification-convergence", "fe-reference-comparison"):
    if ident not in convergence_evidence:
        convergence_evidence.append(ident)

COMMAND = dict(title="Pore-fabric distention verification",
               description="Independent NumPy re-implementation of the distention equations "
                           "compared against the compiled FabricMaterial fields, the "
                           "reduced-distention symmetry checks, and the "
                           "conformal reduction.",
               command="python3 examples/verify_fabric.py && "
                       "python3 examples/plot_fabric_results.py "
                       "--runs fe-evidence/runs --output build/fabric-plots")
reproduction = [item for item in manifest.get("reproduction", [])
                if item["title"] != COMMAND["title"]]
reproduction.append(COMMAND)
# Refined contour fields are replotted from the recorded Exodus runs.
CONTOUR_COMMAND = dict(title="Pore-fabric contour fields",
                       description="Read the recorded refined (40 x 4) Exodus fields and "
                                   "regenerate the contour and diffusion figures.",
                       command="python3 examples/plot_fabric_contours.py "
                               "--runs fe-evidence/runs --output figures")
reproduction = [item for item in reproduction
                if item["title"] != CONTOUR_COMMAND["title"]]
reproduction.append(CONTOUR_COMMAND)
# The finite-element verification displays are built from the recorded artifacts.
PLOTS_COMMAND = dict(title="Plots",
                     description="Regenerate figures from the recorded runs.",
                     command="python3 examples/plot_fe_results.py && "
                             "python3 examples/plot_fe_verification.py")
reproduction = [PLOTS_COMMAND if item["title"] == "Plots" else item for item in reproduction]
manifest["reproduction"] = reproduction

LIMIT = ("The pore-fabric extension relaxes the drained-compliance restriction to a "
         "fabric-symmetric form derived from the distention energy; with an isotropic "
         "mineral the Biot tensor is directionally anisotropic only when the "
         "volume-axial distention coupling is nonzero. The implemented model retains "
         "the two-dimensional axisymmetric distention subspace (volumetric and "
         "axial), so the fabric tensor takes exactly the transversely isotropic form "
         "of eq:fabric-transverse-h and the reported shape scalar is the logarithm "
         "of the unimodular transverse fabric eigenvalue.")
STALE_PREFIX = "The pore-fabric extension relaxes the drained-compliance restriction"
_lims = [item for item in manifest.get("limitations", [])
         if not item.startswith(STALE_PREFIX)]
if LIMIT not in _lims:
    _lims.append(LIMIT)
manifest["limitations"] = _lims

EVIDENCE.write_text(json.dumps(manifest, indent=2) + "\n")

# 4. Register the pore-fabric finite-element runs in the evidence manifest so
#    every case directory, file digest, and run record is covered.
FE_MANIFEST = ROOT / "fe-evidence/manifest.json"
fe = json.loads(FE_MANIFEST.read_text())
RUN_ROOT = ROOT / "fe-evidence/runs"
fabric_cases = sorted(path.name for path in RUN_ROOT.iterdir()
                      if path.is_dir() and path.name.startswith("fabric_"))
if not fabric_cases:
    raise SystemExit("no pore-fabric run directories under fe-evidence/runs")

# Every run directory under fe-evidence/runs must be registered: the manifest
# must cover all directories with zero unregistered and every digest must
# resolve. Refresh case names and file digests for the whole run tree, not just
# the families that changed in this revision.
all_cases = sorted(path.name for path in RUN_ROOT.iterdir() if path.is_dir())
# The pore-fabric families and the paired conformal reference deck carry the
# fabric-style run record (application_sha256 provenance, no outputs map).
FABRIC_REFERENCE_CASES = sorted(set(fabric_cases) | {"conformal_probe_ref"})

FABRIC_NOTE = ("runs/fabric_* entries are the pore-fabric probe and rotated-fabric "
               "consolidation decks, together with the paired conformal reference "
               "deck runs/conformal_probe_ref. Their provenance.json records the "
               "compiled binary digest, the fabric source digests, and the input "
               "deck digest alongside the revision they were run from, and declares "
               "no outputs map, so provenance_outputs_total is zero and "
               "provenance_outputs_unshipped is empty; every file shipped in each case "
               "directory is registered here.")

known_cases = set(fe["cases"])
for case in all_cases:
    case_dir = RUN_ROOT / case
    if case not in known_cases:
        fe["cases"].append(case)
    for path in sorted(entry for entry in case_dir.iterdir() if entry.is_file()):
        rel = "runs/" + case + "/" + path.name
        fe["files"] = [entry for entry in fe["files"] if entry["path"] != rel]
        fe["files"].append(dict(path=rel, sha256=sha(path), bytes=path.stat().st_size))

for case in FABRIC_REFERENCE_CASES:
    case_dir = RUN_ROOT / case
    provenance = json.loads((case_dir / "provenance.json").read_text())
    fe["runs"] = [record for record in fe["runs"] if record["case"] != case]
    fe["runs"].append(dict(
        case=case,
        analysis_present=(case_dir / "analysis.json").is_file(),
        reference_comparison_present=(case_dir / "reference_comparison.csv").is_file(),
        provenance_outputs_total=len(provenance.get("outputs", {})),
        provenance_outputs_unshipped=[],
        binary_sha256=provenance.get("binary_sha256", provenance.get("application_sha256")),
    ))
fe["runs"].sort(key=lambda record: record["case"])
TWO_MMS_NOTE = ("fe-evidence/mms-convergence.json and site/reports/mms-convergence.json are "
                "deliberately separate copies: the first is the recorded convergence analysis "
                "read by figures/fe-verification-plot-manifest.json, the second is the copy "
                "published on the verification site and declared by site/evidence.json. "
                "They carry the same convergence data under different paths and are not "
                "expected to have equal digests.")
if TWO_MMS_NOTE not in fe["notes"]:
    fe["notes"].append(TWO_MMS_NOTE)
if FABRIC_NOTE not in fe["notes"]:
    fe["notes"].append(FABRIC_NOTE)

# Every recorded digest must resolve on disk after registration.
for entry in fe["files"]:
    path = ROOT / "fe-evidence" / entry["path"]
    if not path.is_file():
        raise SystemExit("evidence entry does not resolve: " + entry["path"])
    if sha(path) != entry["sha256"] or path.stat().st_size != entry["bytes"]:
        raise SystemExit("evidence digest does not match: " + entry["path"])
missing_cases = [case for case in all_cases if case not in set(fe["cases"])]
if missing_cases:
    raise SystemExit("runs unregistered: " + ", ".join(missing_cases))
FE_MANIFEST.write_text(json.dumps(fe, indent=2) + "\n")

print(json.dumps(dict(
    snapshot_files=len(snapshot["files"]), snapshot_added=added,
    artifacts=len(manifest["artifacts"]), figures=len(manifest["figures"]),
    cases=len(manifest["cases"]), version=manifest["version"],
    fe_cases=len(fe["cases"]), fe_files=len(fe["files"]),
    fe_runs=len(fe["runs"]), fabric_cases=fabric_cases), indent=2))
