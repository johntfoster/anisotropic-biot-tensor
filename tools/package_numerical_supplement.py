#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Package numerical sources and evidence for attachment to the article PDF."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = 'conformal-2026-09-20-v1'
DEST = ROOT / 'build' / (VERSION + '.zip')


def main():
    sources = ['conformal_model.py', 'conformal_experiments.py',
               'verify_conformal.py', 'verify_tensor.py',
               'verify_reconstruction.py', 'weighted_stress.py', 'requirements.txt']
    files = [ROOT / 'examples' / name for name in sources]
    files += [ROOT / 'LICENSE', ROOT / 'LICENSES.md']
    files += list((ROOT / 'licenses').glob('*'))
    for directory in ('conformal', 'weighted-stress'):
        files += [p for p in (ROOT / 'build' / directory).glob('*')
                  if p.suffix in ('.csv', '.dat', '.json', '.pdf', '.tex')]
    for required in ('verification.json', 'experiments.json', 'step_refinement.csv'):
        if not (ROOT / 'build/conformal' / required).is_file():
            raise SystemExit('Run verification and experiments before packaging: ' + required)
    for required in ('results.json', 'tensor-verification.json', 'reconstruction-verification.json'):
        if not (ROOT / 'build/weighted-stress' / required).is_file():
            raise SystemExit('Run the spherical-gauge suites before packaging: ' + required)
    contents = {str(p.relative_to(ROOT)): p.read_bytes() for p in files if p.is_file()}
    contents['README.md'] = f'''# Numerical supplement: {VERSION}

This archive accompanies "An anisotropic Biot tensor from mineral stress and
distention work". It contains the numerical sources, parameters, figure data, figures,
verification reports, and software versions that produce the article's
conformal constitutive results, as of the archived date and version.
The models are synthetic homogeneous constitutive calculations, not physical
validation or finite-element simulations. No companion checkout is required.

Extract the archive, then run from its root in a Python environment:

```sh
python3 -m pip install -r examples/requirements.txt
python3 examples/weighted_stress.py
python3 examples/verify_reconstruction.py
python3 examples/verify_tensor.py
python3 examples/verify_conformal.py
python3 examples/conformal_experiments.py
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
