#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check reference fluid-mass derivatives against solved-volume differences.

These material-point checks verify the added fluid closure, not a coupled FE
calculation. Outputs are generated under build/fluid-coupling by default.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from conformal_model import Model, I, isotropic_stiffness, shear_gradient


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('build/fluid-coupling'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    checks = []

    def check(name, error, tolerance=2e-8):
        error = float(error)
        checks.append(dict(name=name, error=error, tolerance=tolerance,
                           passed=bool(np.isfinite(error) and error <= tolerance)))
        if not checks[-1]['passed']:
            raise AssertionError(checks[-1])

    mineral = Model()
    isotropic = Model(isotropic_stiffness(mineral.ks, mineral.mu_average))
    rho0, kf = 1.2, 8.
    gradients = [I, np.diag([1.08, .96, 1.]), shear_gradient(.35)]
    direction = np.array([[.25, -.11, .03], [.07, -.18, .09], [.01, .04, .12]])
    for label, model in [('anisotropic', mineral), ('isotropic', isotropic)]:
        def mass(f, p):
            state = model.state(f, p)
            return rho0*np.exp(p/kf)*(state['J']-model.phi*state['y'])

        for i, f in enumerate(gradients):
            for p in (-1., 0., 2.):
                state = model.state(f, p)
                rho = rho0*np.exp(p/kf)
                expected_p = rho*((state['J']-model.phi*state['y'])/kf
                                 + state['storage'])
                expected_f = rho*state['J']*np.sum(
                    state['B']*(direction @ np.linalg.inv(f)))
                prefix = f'{label}_F{i}_p{p:g}'
                for h in (1e-3, 5e-4, 2.5e-4):
                    measured_p = (mass(f, p+h)-mass(f, p-h))/(2*h)
                    measured_f = (mass(f+h*direction, p)-mass(f-h*direction, p))/(2*h)
                    check(f'{prefix}_storage_h{h:g}',
                          abs(measured_p-expected_p)/max(1., abs(expected_p)))
                    check(f'{prefix}_deformation_h{h:g}',
                          abs(measured_f-expected_f)/max(1., abs(expected_f)))

    benchmark = Model(cs=isotropic_stiffness(2.5, 5/6), phi=.9, k=1.)
    state = benchmark.state(I, 0.)
    check('Mandel_reference_total_storage',
          abs((1-benchmark.phi)/8+state['storage']-17/80), 1e-14)
    check('Mandel_reference_Biot_tensor', np.linalg.norm(state['B']-.6*I), 1e-14)
    root = Path(__file__).resolve().parents[1]
    sources = ['examples/conformal_model.py', 'examples/verify_fluid_coupling.py']
    report = dict(category='implementation-material-point',
                  scope='Fluid EOS and reference-mass derivatives; not FE verification',
                  checks=checks, count=len(checks), passed=all(c['passed'] for c in checks),
                  maximum_scaled_error=max(c['error'] for c in checks),
                  fluid=dict(reference_density=rho0, bulk_modulus=kf),
                  source_sha256={p: hashlib.sha256((root/p).read_bytes()).hexdigest()
                                 for p in sources})
    (args.output/'verification.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('scope', 'count', 'passed',
                                           'maximum_scaled_error')}, indent=2))


if __name__ == '__main__':
    main()
