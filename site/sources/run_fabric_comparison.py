#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Record coupled scalar/tensor consolidation and refinement on identical decks.

Run inside the repository's verified MOOSE environment. Every case starts at
rest, ramps the load over 0.01 time units and holds it to 0.75 for drainage.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT/'fe-evidence/insight'
BIN = ROOT/'moose_app/anisotropic_biot-opt'
SOURCES = ['moose_app/inputs/fabric_comparison.i',
           'moose_app/include/utils/FabricLaw.h',
           'moose_app/include/materials/FabricMaterial.h',
           'moose_app/src/materials/FabricMaterial.C',
           'moose_app/src/kernels/ReferenceBalance.C', 'tools/run_fabric_comparison.py']


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--angles', nargs='+', type=int, default=[0, 45, 90])
    ap.add_argument('--levels', nargs='+', default=['coarse', 'fine'])
    args = ap.parse_args()
    source_hashes = {s: sha(ROOT/s) for s in SOURCES}
    binary = {'executable': sha(BIN), 'library': sha(ROOT/'moose_app/lib/libanisotropic_biot-opt.so.0.0.0')}
    for level in args.levels:
        nx, ny, dt = {'coarse': (20, 4, .0025), 'fine': (40, 8, .00125),
                      'time': (40, 8, .0025), 'finer': (80, 16, .000625)}[level]
        for angle in args.angles:
            for model in ('tensor', 'scalar'):
                case = f'{model}_{angle}_{level}'
                dest = DEST/case
                dest.mkdir(parents=True, exist_ok=True)
                overrides = [f'Mesh/base/nx={nx}', f'Mesh/base/ny={ny}', f'Executioner/dt={dt}',
                             f'Materials/law/fabric_angle={angle}',
                             'Materials/law/scalar_coupling='+str(model == 'scalar').lower()]
                cmd = [str(BIN), '-i', 'moose_app/inputs/fabric_comparison.i',
                       f'Outputs/file_base={dest}/solution', '--n-threads=1', *overrides]
                start = time.monotonic()
                with (dest/'run.log').open('w') as log:
                    proc = subprocess.run(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
                record = dict(case=case, model=model, angle=angle, level=level, nx=nx, ny=ny, dt=dt,
                              command=['moose_app/anisotropic_biot-opt', '-i', SOURCES[0],
                                       f'Outputs/file_base=fe-evidence/insight/{case}/solution',
                                       '--n-threads=1', *overrides],
                              source_sha256=source_hashes, binary_sha256=binary,
                              exit_code=proc.returncode, wall_seconds=time.monotonic()-start)
                if (dest/'solution.csv').exists():
                    record['history_sha256'] = sha(dest/'solution.csv')
                (dest/'provenance.json').write_text(json.dumps(record, indent=2)+'\n')
                print(case, 'exit', proc.returncode, f'{record["wall_seconds"]:.1f}s', flush=True)
                if proc.returncode:
                    raise SystemExit((dest/'run.log').read_text()[-4000:])


if __name__ == '__main__':
    main()
