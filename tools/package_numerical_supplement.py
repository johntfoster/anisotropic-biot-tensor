#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Package numerical sources and evidence for attachment to the article PDF."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = 'anisotropic-biot-2026-09-20-v2'
DEST = ROOT / 'build' / (VERSION + '.zip')

MOOSE_SOURCES = ['include/utils/FabricLaw.h', 'include/materials/FabricMaterial.h',
                 'src/materials/FabricMaterial.C', 'inputs/fabric_probe.i',
                 'inputs/conformal_probe.i', 'inputs/fabric_mandel.i',
                 'inputs/fabric_contour.i']

# Recorded pore-fabric run inputs read by examples/verify_fabric.py and
# examples/plot_fabric_results.py. Shipping them keeps the documented commands
# working from the extracted archive, not only from the authoring checkout.
FABRIC_RUN_CASES = ['fabric_probe_iso', 'fabric_probe_coup_a0', 'fabric_probe_coup_a45',
                    'fabric_probe_coup_a90', 'fabric_probe_conformal',
                    'fabric_probe_stiffaxial', 'fabric_probe_softaxial',
                    'fabric_probe_a0', 'fabric_probe_a45', 'fabric_probe_a90',
                    'fabric_mandel_iso', 'fabric_mandel_coup_a0',
                    'fabric_mandel_coup_a45', 'fabric_mandel_coup_a90',
                    'conformal_probe_ref']

# Refined (40 x 8) contour runs ship both the scalar history and the Exodus
# field file so examples/plot_fabric_contours.py reproduces the contour figures
# from the extracted archive.
FABRIC_CONTOUR_CASES = ['fabric_contour_iso', 'fabric_contour_a0',
                        'fabric_contour_a45', 'fabric_contour_a90']


def main():
    sources = ['conformal_model.py', 'conformal_experiments.py',
               'verify_conformal.py', 'verify_tensor.py',
               'verify_reconstruction.py', 'verify_fabric.py',
               'plot_fabric_results.py', 'plot_fabric_contours.py',
               'weighted_stress.py', 'requirements.txt']
    files = [ROOT / 'examples' / name for name in sources]
    files += [ROOT / 'moose_app' / name for name in MOOSE_SOURCES]
    files += [ROOT / 'fe-evidence/runs' / case / 'solution.csv'
              for case in FABRIC_RUN_CASES]
    files += [ROOT / 'fe-evidence/runs' / case / 'solution.csv'
              for case in FABRIC_CONTOUR_CASES]
    files += [ROOT / 'fe-evidence/runs' / case / 'solution.e'
              for case in FABRIC_CONTOUR_CASES]
    files += [ROOT / 'tools/rerun_fabric_contours.py']
    files += [ROOT / 'LICENSE', ROOT / 'LICENSES.md']
    files += list((ROOT / 'licenses').glob('*'))
    for directory in ('conformal', 'weighted-stress', 'fabric'):
        files += [p for p in (ROOT / 'build' / directory).glob('*')
                  if p.suffix in ('.csv', '.dat', '.json', '.pdf', '.tex', '.txt')]
    for required in ('verification.json', 'experiments.json', 'step_refinement.csv'):
        if not (ROOT / 'build/conformal' / required).is_file():
            raise SystemExit('Run verification and experiments before packaging: ' + required)
    for required in ('fabric-verification.json',):
        if not (ROOT / 'build/fabric' / required).is_file():
            raise SystemExit('Run the pore-fabric verification before packaging: ' + required)
    for case in FABRIC_RUN_CASES:
        if not (ROOT / 'fe-evidence/runs' / case / 'solution.csv').is_file():
            raise SystemExit('Missing recorded pore-fabric run input: fe-evidence/runs/'
                             + case + '/solution.csv')
    for case in FABRIC_CONTOUR_CASES:
        for suffix in ('solution.csv', 'solution.e'):
            if not (ROOT / 'fe-evidence/runs' / case / suffix).is_file():
                raise SystemExit('Missing recorded contour run input: fe-evidence/runs/'
                                 + case + '/' + suffix)
    for required in ('results.json', 'tensor-verification.json', 'reconstruction-verification.json'):
        if not (ROOT / 'build/weighted-stress' / required).is_file():
            raise SystemExit('Run the spherical-gauge suites before packaging: ' + required)
    contents = {str(p.relative_to(ROOT)): p.read_bytes() for p in files if p.is_file()}
    contents['README.md'] = f'''# Numerical supplement: {VERSION}

This archive accompanies "An anisotropic Biot tensor from mineral stress and
distention work". It contains the numerical sources, parameters, figure data, figures,
verification reports, and software versions that produce the article's
conformal constitutive results, as of the archived date and version.
The models are synthetic
constitutive calculations, not physical validation or finite-element
simulations. The archive additionally ships recorded finite-element run
histories under `fe-evidence/runs` for the pore-fabric decks; those runs are
demonstrations of the coupled model, not physical validation. The recorded
Exodus field files carry a per-run wall-clock line in their information records,
so their raw bytes are not reproducible across runs; the recorded CSV histories
and the field arrays are. No companion
checkout is required.

Extract the archive, then run from its root in a Python environment:

```sh
python3 -m pip install -r examples/requirements.txt
python3 examples/weighted_stress.py
python3 examples/verify_reconstruction.py
python3 examples/verify_tensor.py
python3 examples/verify_conformal.py
python3 examples/conformal_experiments.py
python3 examples/verify_fabric.py
```

The pore-fabric verification re-implements the distention equations of the
manuscript independently of the compiled material. The recorded run histories
it reads ship in this archive under `fe-evidence/runs`, so it runs from the
extracted root without arguments. Its output can then be replotted from the
same recorded runs:

```sh
python3 examples/plot_fabric_results.py \
  --runs fe-evidence/runs --output build/fabric-plots
```

The refined (40 x 8) contour runs also ship their Exodus field files under
`fe-evidence/runs/fabric_contour_*`, so the contour and diffusion figures are
reproducible from the extracted archive:

```sh
python3 examples/plot_fabric_contours.py \
  --runs fe-evidence/runs --output figures
```

Verification precedes figure generation so the supplemental step-refinement
figure is also regenerated. Generated results are under build/. JSON files
record the actual versions used; requirements specify supported package ranges,
not a locked environment. Floating-point and PDF metadata differences between
platforms need not reproduce archive bytes. Verification tolerances remain in
the source and reports. The source/data SHA-256 manifest identifies this archive's
exact contents independently of any repository commit.

The article PDF embeds this ZIP in its attachments panel. Poppler users can
extract it with `pdfdetach -saveall article.pdf`. Some browser viewers do not
expose embedded files; download the PDF and use an attachment-capable viewer.
Code is Apache-2.0; the manuscript and original manuscript figures are
CC-BY-4.0, as detailed in LICENSES.md. Third-party rights are unchanged.
'''.encode()
    manifest = {name: hashlib.sha256(value).hexdigest() for name, value in sorted(contents.items())}
    contents['manifest.json'] = (json.dumps(dict(version=VERSION, sha256=manifest), indent=2)+'\n').encode()
    DEST.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DEST, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, value in sorted(contents.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 20, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, value)
    print(json.dumps(dict(archive=str(DEST.relative_to(ROOT)),
                         sha256=hashlib.sha256(DEST.read_bytes()).hexdigest(),
                         files=len(contents)), indent=2))


if __name__ == '__main__':
    main()
