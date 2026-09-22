#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check compiled tensor/scalar stress and mass against a separate linear solve."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT/'fe-evidence/insight-probe'
ANISOTROPIC = '50 12 10 0 0 0 12 60 14 0 0 0 10 14 70 0 0 0 0 0 0 20 0 0 0 0 0 0 24 0 0 0 0 0 0 28'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--analyze-only', action='store_true')
    ap.add_argument('--run-only', action='store_true')
    args = ap.parse_args()
    if not args.analyze_only:
        for model in ('tensor', 'scalar', 'anisotropic_minus', 'anisotropic_plus'):
            folder = DEST/model
            folder.mkdir(parents=True, exist_ok=True)
            cmd = ['moose_app/anisotropic_biot-opt', '-i', 'moose_app/inputs/fabric_probe.i',
                   f'Outputs/file_base=fe-evidence/insight-probe/{model}/solution',
                   'Materials/law/fabric_volume_modulus=5.4', 'Materials/law/fabric_coupling=0.4',
                   'Materials/law/fabric_angle=45',
                   'Materials/law/scalar_coupling='+str(model=='scalar').lower()]
            if model.startswith('anisotropic'):
                pressure = .02 + (-1e-4 if model.endswith('minus') else 1e-4)
                cmd += ['Materials/law/mineral_stiffness='+ANISOTROPIC,
                        f'BCs/left_p/value={pressure}', f'BCs/right_p/value={pressure}']
            with (folder/'run.log').open('w') as f:
                proc = subprocess.run(cmd, cwd=ROOT, stdout=f, stderr=subprocess.STDOUT)
            record = dict(command=cmd, exit_code=proc.returncode,
                          binary_sha256=sha(ROOT/'moose_app/anisotropic_biot-opt'),
                          library_sha256=sha(ROOT/'moose_app/lib/libanisotropic_biot-opt.so.0.0.0'),
                          source_sha256={n:sha(ROOT/n) for n in ['moose_app/include/utils/FabricLaw.h',
                          'moose_app/include/materials/FabricMaterial.h', 'moose_app/src/materials/FabricMaterial.C',
                          'moose_app/inputs/fabric_probe.i', 'tools/verify_scalar_probe.py']})
            (folder/'provenance.json').write_text(json.dumps(record, indent=2)+'\n')
            if proc.returncode:
                raise SystemExit((folder/'run.log').read_text()[-3000:])
    if args.run_only:
        return
    import numpy as np
    sys.path.insert(0, str(ROOT/'examples'))
    from fabric_insight import coefficients, IV, PHI
    _, _, _, _, _, Cd, B, storage = coefficients(45.)
    strain = np.array([.01, -.005, 0., 0., 0., 0.])
    report, inputs = {}, {}
    for model in ('tensor', 'scalar'):
        folder = DEST/model
        for f in ('provenance.json', 'solution.csv'):
            inputs[str((folder/f).relative_to(ROOT))] = sha(folder/f)
        record = json.loads((folder/'provenance.json').read_text())
        assert record['exit_code'] == 0
        for name, digest in record['source_sha256'].items():
            assert sha(ROOT/name) == digest
        row = np.genfromtxt(folder/'solution.csv', delimiter=',', names=True)[-1]
        bv = B if model == 'tensor' else (B@IV)/3*IV
        stress = Cd@strain-.02*bv
        expected = dict(sigma11=stress[0], sigma22=stress[1],
                        mass=1-PHI+bv@strain+.02*storage,
                        drained_c11=Cd[0,0], drained_c12=Cd[0,1])
        errors = {k:abs(float(row[k])-float(v)) for k,v in expected.items()}
        assert max(errors.values()) < 1e-11, errors
        report[model] = dict(expected={k:float(v) for k,v in expected.items()},
                            recorded={k:float(row[k]) for k in expected}, errors=errors)
    from fabric_insight import basis
    cs = np.fromstring(ANISOTROPIC, sep=' ').reshape(6, 6)
    L = basis(45.)[2]
    operator = np.array([[5.4, .4], [.4, 1.]]) + PHI*L.T@cs@L
    expected_solid_storage = PHI**2*(IV@L)@np.linalg.solve(operator, L.T@IV)
    samples = []
    for model in ('anisotropic_minus', 'anisotropic_plus'):
        folder = DEST/model
        record = json.loads((folder/'provenance.json').read_text())
        assert record['exit_code'] == 0
        for name, digest in record['source_sha256'].items():
            assert sha(ROOT/name) == digest
        for name in ('provenance.json', 'solution.csv'):
            inputs[str((folder/name).relative_to(ROOT))] = sha(folder/name)
        samples.append(np.genfromtxt(folder/'solution.csv', delimiter=',', names=True)[-1])
    mineral_derivative = -PHI*(samples[1]['Jbar']-samples[0]['Jbar'])/2e-4
    mass_derivative = (samples[1]['mass']-samples[0]['mass'])/2e-4-(1-PHI)/8
    errors = [abs(mineral_derivative-expected_solid_storage),
              abs(mass_derivative-expected_solid_storage)]
    assert max(errors) < 1e-9, errors
    report['anisotropic_storage'] = dict(expected=float(expected_solid_storage),
        mineral_volume_derivative=float(mineral_derivative),
        mass_derivative_solid_part=float(mass_derivative), errors=errors)
    for p in [Path(__file__), ROOT/'examples/fabric_insight.py']:
        inputs[str(p.relative_to(ROOT))] = sha(p)
    out = ROOT/'build/insight/scalar_probe_verification.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(dict(category='compiled_reference_constitutive_check', cases=report,
                                   input_sha256=inputs), indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
