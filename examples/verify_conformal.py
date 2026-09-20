#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Constitutive verification, independent differences, and step refinement.

Run from the repository root: python3 examples/verify_conformal.py.
These are homogeneous material-point checks, not finite-element validation.
"""
import json
import hashlib
from pathlib import Path
import platform
import numpy as np
import scipy
from scipy.linalg import expm
from scipy.integrate import quad_vec
from scipy.special import lambertw
from conformal_model import (Model, I, ONE, vec, mat, log_symmetric,
                             log_frechet, isotropic_stiffness, shear_gradient)

DEST = Path(__file__).resolve().parents[1]/'build/conformal'


def derivative(fun, x, step=2e-5, order=4):
    x = np.asarray(x, dtype=float)
    columns = []
    for k in range(x.size):
        dx = np.zeros_like(x); dx.flat[k] = step
        if order == 4:
            value = (-np.asarray(fun(x+2*dx))+8*np.asarray(fun(x+dx))
                     -8*np.asarray(fun(x-dx))+np.asarray(fun(x-2*dx)))/(12*step)
        else:
            value = (np.asarray(fun(x+dx))-np.asarray(fun(x-dx)))/(2*step)
        columns.append(value.ravel())
    return np.array(columns).T


def main():
    checks = {}
    def check(name, value, tolerance=2e-7, category='implementation'):
        value = float(value)
        checks[name] = dict(error=value, tolerance=tolerance, category=category)
        assert np.isfinite(value) and value < tolerance, (name, value, tolerance)

    # Preserve the original five finite states and all 67 conformal identities.
    # Helpers and constitutive implementation are now wholly repository-owned.
    rng = np.random.default_rng(7178)
    x = rng.normal(size=(6, 6))
    cs = isotropic_stiffness(25, 16)+3*x.T@x
    ks = ONE@cs@ONE/9
    k = 1/(1/11+1/(.6*ks))
    model = Model(cs=cs, k=k)
    naive_errors, states = [], []
    for n in range(5):
        f = I+.12*rng.normal(size=(3, 3)); p = .4+.35*n
        z = rng.normal(size=(3, 3)); spin = (z-z.T)/2; r = expm(spin)
        st, zero = model.state(f, p, r), model.state(f, p)
        prefix = f'legacy_state{n}_'
        check(prefix+'rotation_orthogonality', np.linalg.norm(r.T@r-I))
        check(prefix+'true_metric', np.linalg.norm(st['Fbar'].T@st['Fbar']-st['a']**(-2/3)*f.T@f))
        check(prefix+'log_strain', np.linalg.norm(.5*log_symmetric(st['Fbar'].T@st['Fbar'])
                    -(.5*log_symmetric(f.T@f)-np.log(st['a'])/3*I)))
        check(prefix+'energy_rotation_independence', abs(st['W']-zero['W']))
        check(prefix+'rotated_mineral_stress', np.linalg.norm(st['tau_space']-zero['tau_space']))
        check(prefix+'mixture_stress_rotation_independence', np.linalg.norm(st['sigma']-zero['sigma']))
        check(prefix+'scalar_pressure_equilibrium', abs(model.ka*np.log(st['a'])
                    -model.phi*(np.trace(st['tau_true'])/3+p*st['y'])))
        grad = derivative(lambda ff: model.state(ff.reshape(3, 3), p, r)['potential'], f.ravel()).reshape(3, 3)
        check(prefix+'full_phase_balance_from_energy', np.linalg.norm(grad@f.T/st['J']-st['sigma']))
        dp = derivative(lambda pp: model.state(f, float(pp[0]), r)['sigma'], [p]).reshape(3, 3)
        check(prefix+'pressure_tangent', np.linalg.norm(dp+st['B']))
        dpv = derivative(lambda pp: model.state(f, float(pp[0]), expm(float(pp[0])*spin))['sigma'], [p]).reshape(3, 3)
        check(prefix+'pressure_dependent_rotation_cancels', np.linalg.norm(dpv+st['B']))
        dy = derivative(lambda ff: model.state(ff.reshape(3, 3), p, r)['y'], f.ravel()).reshape(3, 3)
        check(prefix+'pore_volume_derivative', np.linalg.norm(I-model.phi/st['J']*dy@f.T-st['B']))
        check(prefix+'zero_rotation_energy_derivative', np.linalg.norm(derivative(
            lambda tt: model.state(f, p, expm(tt[0]*spin)@r)['W'], [0.])))
        da = .7; z = rng.normal(size=(3, 3)); om = (z-z.T)/2; lb = rng.normal(size=(3, 3))
        l = da/3*I+om+r@lb@r.T
        tau = st['J']*(st['sigma']+p*I)
        work = np.sum(tau*l)-model.phi*p*st['y']*np.trace(lb)
        check(prefix+'full_virtual_work', abs(work-model.ka*np.log(st['a'])*da
                                             -model.phi*np.sum(st['tau_true']*lb)))
        naive_errors.append(float(model.phi/st['J']*np.linalg.norm(st['tau_true']-st['tau_space'])))
        states.append(dict(F=f.tolist(), p=p, R_A=r.tolist(), a=st['a'], B=st['B'].tolist()))
    compliance = np.linalg.inv(model.cd)-np.linalg.inv(model.phi*model.cs)
    check('legacy_reference_rank_one_compliance_identity', np.linalg.norm(
        compliance-model.alpha/(9*model.k)*np.outer(ONE, ONE)))
    check('legacy_reference_biot', np.linalg.norm(model.state(I, 0)['B']
        -(I-mat(model.cd@np.linalg.solve(model.cs, ONE)))))
    legacy_count = len(checks)
    assert legacy_count == 67
    check('compliance_rank', abs(np.linalg.matrix_rank(compliance, tol=1e-10)-1), 1e-12, 'analytical')
    assert min(naive_errors) > 1e-3, 'Missing-frame-rotation control must fail.'

    default = Model()
    # An independent Lambert-W solution checks stable branch selection well
    # outside the plotted paths, including two roots at negative pressure.
    for pressure in (-14., -13., 800.):
        st = default.state(I, pressure)
        beta = default.alpha*pressure/default.ks
        reference_q = -float(lambertw(beta, k=0).real)
        prefix = f'branch_pressure_{pressure:g}_'
        check(prefix+'lambert_volume', abs(st['y']-np.exp(reference_q)), 2e-13, 'analytical')
        check(prefix+'residual', abs(st['residual']), 2e-11, 'analytical')
        check(prefix+'positive_stability', float(st['stability'] <= 0), 1e-12, 'analytical')
    for name, pressure, message in (
            ('branch_termination', -18., 'No strictly stable scalar branch'),
            ('zero_fluid_volume', -16., 'positive solid and fluid volume fractions')):
        try:
            default.state(I, pressure)
        except ValueError as error:
            check(name, float(message not in str(error)), 1e-12, 'analytical')
        else:
            raise AssertionError(f'{name}: inadmissible state was accepted')
    iso = Model(isotropic_stiffness(default.ks, default.mu_average))
    finite_states = [(I, 0.), (1.1*I, 2.), (np.diag([1.1, 1.1, .9]), .5),
                     (np.diag([1.1, 1.1+1e-11, .9]), .5),
                     (shear_gradient(.65), 2.), (shear_gradient(-.8), 6.)]
    for label, material in [('anisotropic', default), ('isotropic', iso)]:
        for n, (f, p) in enumerate(finite_states):
            st = material.state(f, p); prefix = f'{label}_state{n}_'
            check(prefix+'residual', abs(st['residual']), 2e-11, 'analytical')
            check(prefix+'solid_mass', abs(st['J']*st['solid_fraction']/st['y']-material.phi), 1e-13, 'analytical')
            check(prefix+'symmetry', np.linalg.norm(st['B']-st['B'].T), 1e-12)
            energy_grad = derivative(lambda ff: material.state(ff.reshape(3,3), p)['potential'], f.ravel()).reshape(3,3)
            check(prefix+'energy_stress', np.linalg.norm(energy_grad@f.T/st['J']-st['sigma']))
            ds = derivative(lambda pp: material.state(f, pp[0])['sigma'], [p]).reshape(3,3)
            check(prefix+'pressure_tangent', np.linalg.norm(ds+st['B']))
            dv = derivative(lambda ff: material.state(ff.reshape(3,3), p)['y'], f.ravel()).reshape(3,3)
            check(prefix+'volume_gradient', np.linalg.norm(I-material.phi/st['J']*dv@f.T-st['B']))
            storage = -material.phi*derivative(lambda pp: material.state(f, pp[0])['y'], [p])[0,0]
            check(prefix+'storage', abs(storage-st['storage']))
            z = np.array([[0., -.6, .2], [.6, 0., .1], [-.2, -.1, 0.]])
            q = expm(z); rotated = material.state(q@f, p)
            check(prefix+'physical_rotation', max(np.linalg.norm(rotated['B']-q@st['B']@q.T),
                np.linalg.norm(rotated['sigma']-q@st['sigma']@q.T), abs(rotated['W']-st['W'])))
            if label == 'isotropic':
                scalar = 1-st['y']*material.k/(st['J']*(material.ks+material.alpha*p*st['y']))
                check(prefix+'scalar_limit', np.linalg.norm(st['B']-scalar*I), 1e-12, 'analytical')
    direction = np.array([[.4, .2, -.1], [.2, -.3, .6], [-.1, .6, .7]])
    check('exact_repeated_eigenvalue_log_derivative', np.linalg.norm(log_frechet(1.21*I, direction)-direction/1.21), 1e-13, 'analytical')
    f = shear_gradient(.65); p = 2.; st = default.state(f,p)
    mineral_log_stress = mat(default.cs@vec(.5*log_symmetric(st['Fbar'].T@st['Fbar'])))
    strain = .5*log_symmetric(f.T@f)
    commutator = float(np.linalg.norm(strain@mineral_log_stress-mineral_log_stress@strain))
    assert commutator > .1, 'Finite test must have different stress/strain axes.'
    integral, quadrature_error = quad_vec(lambda pp: default.state(f, pp)['B'], 0., 6., epsabs=1e-11)
    check('integrated_pressure_response', np.linalg.norm(default.state(f,6.)['sigma']
        -default.state(f,0.)['sigma']+integral), 1e-10, 'analytical')
    wrong = np.linalg.norm(default.state(f,6.)['sigma']-default.state(f,0.)['sigma']+6*default.state(f,6.)['B'])
    assert wrong > .01, 'Finite-pressure response must distinguish an integral from p*B(p).'
    # Meaningful second-order convergence before floating-point cancellation.
    refinement = []
    for step in (2e-2, 1e-2, 5e-3, 2.5e-3, 1.25e-3):
        grad = derivative(lambda ff: default.state(ff.reshape(3,3),p)['potential'], f.ravel(), step, 2).reshape(3,3)
        dv = derivative(lambda ff: default.state(ff.reshape(3,3),p)['y'], f.ravel(), step, 2).reshape(3,3)
        ds = derivative(lambda pp: default.state(f,pp[0])['sigma'], [p], step, 2).reshape(3,3)
        refinement.append(dict(step=step, energy_stress=float(np.linalg.norm(grad@f.T/st['J']-st['sigma'])),
            pore_volume=float(np.linalg.norm(I-default.phi/st['J']*dv@f.T-st['B'])),
            pressure=float(np.linalg.norm(ds+st['B']))))
    orders = {}
    for name in ('energy_stress', 'pore_volume', 'pressure'):
        values = [row[name] for row in refinement]
        orders[name] = [float(np.log2(a/b)) for a,b in zip(values[:-1], values[1:])]
        check('second_order_'+name, max(abs(order-2) for order in orders[name]), .06, 'convergence')
    result = dict(checks_passed=len(checks), legacy_identities_rechecked=legacy_count, checks=checks,
        max_constitutive_identity_error=max(v['error'] for v in checks.values() if v['category'] != 'convergence'),
        naive_unrotated_phase_stress_errors=naive_errors, legacy_states=states,
        refinement=refinement, observed_orders=orders, noncoaxial_commutator=commutator,
        instantaneous_times_pressure_error=float(wrong), quadrature_error=float(quadrature_error),
        versions=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__),
        source_sha256={'examples/'+name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
                       for name in ('conformal_model.py','verify_conformal.py')},
        scope='Homogeneous material-point implementation, analytical, convergence, and finite-deformation checks; no FE or physical validation.')
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ('checks_passed','legacy_identities_rechecked',
        'max_constitutive_identity_error','observed_orders','noncoaxial_commutator',
        'instantaneous_times_pressure_error','versions')}, indent=2))


if __name__ == '__main__':
    main()
