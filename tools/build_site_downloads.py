#!/usr/bin/env python3
"""Build PDF downloads from source and write a manifest for this site build."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    for variable, directory in (
        ('TEXMFCACHE', '.agent-runtime/tex-cache/var'),
        ('LUOTFLOAD_CACHE', '.agent-runtime/tex-cache/cache'),
        ('MPLCONFIGDIR', '.agent-runtime/matplotlib'),
    ):
        path = ROOT / directory
        path.mkdir(parents=True, exist_ok=True)
        os.environ[variable] = str(path)
    # These drivers use shipped finite-element histories; no MOOSE solve is needed.
    for driver in (
        'examples/weighted_stress.py', 'examples/verify_tensor.py',
        'examples/verify_reconstruction.py', 'examples/verify_conformal.py',
        'examples/conformal_experiments.py', 'examples/verify_fabric.py',
        'examples/fabric_insight.py', 'examples/plot_fabric_comparison.py',
        'tools/package_numerical_supplement.py',
    ):
        subprocess.run([sys.executable, driver], cwd=ROOT, check=True)
    subprocess.run([
        'latexmk', '-lualatex', '-interaction=nonstopmode', '-halt-on-error',
        '-outdir=build', 'main.tex',
    ], cwd=ROOT, check=True)
    manifest = json.loads((ROOT / 'site/evidence.json').read_text())
    # Only the two newly built downloads receive build-specific hashes.
    # Recorded scientific evidence and source hashes remain independently checked.
    generated = {'build/main.pdf', 'build/anisotropic-biot-2026-09-22-v3.zip'}
    for artifact in manifest['artifacts']:
        if artifact['path'] in generated:
            artifact['sha256'] = hashlib.sha256((ROOT / artifact['path']).read_bytes()).hexdigest()
    output = ROOT / '.agent-runtime/site-build-evidence.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    main()
