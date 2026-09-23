#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Pressure reactions and a finite, commuting fabric benchmark.

The nonlinear calculation is restricted to an isotropic mineral and logarithmic
strains commuting with the prescribed fabric. No noncoaxial finite law is
inferred. The candidate three-dimensional energy is differentiated only at
these admissible states to check all nine spatial stress components.
"""
from pathlib import Path
import csv
import hashlib
import json
import sys
import scipy
import numpy as np
from scipy.linalg import expm
from scipy.optimize import root, minimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from figure_style import apply_style, COLORS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/insight'
PHI, KS, MU, KF = .9, 2.5, 5/6, 8.
KV, KA, KC = 5.4, 1., .4
I = np.eye(3)
IV = np.array([1., 1., 1., 0., 0., 0.])
CS = 2*MU*np.eye(6) + (KS-2*MU/3)*np.outer(IV, IV)


def mandel(a):
    return np.array([a[0, 0], a[1, 1], a[2, 2], np.sqrt(2)*a[1, 2],
                     np.sqrt(2)*a[0, 2], np.sqrt(2)*a[0, 1]])


def tensor(v):
    a = np.diag(v[:3]).astype(float)
    a[1, 2] = a[2, 1] = v[3]/np.sqrt(2)
    a[0, 2] = a[2, 0] = v[4]/np.sqrt(2)
    a[0, 1] = a[1, 0] = v[5]/np.sqrt(2)
    return a


def basis(angle=45., conformal=False):
    th = np.deg2rad(angle)
    m = np.array([np.cos(th), np.sin(th), 0.])
    n = np.array([-np.sin(th), np.cos(th), 0.])
    L = np.stack([mandel(I/np.sqrt(3)),
                  mandel(np.sqrt(1.5)*(np.outer(m, m)-I/3))], axis=1)
    return m, n, L[:, :1] if conformal else L


def coefficients(angle=45., coupling=KC, conformal=False, axial_modulus=KA):
    m, n, L = basis(angle, conformal)
    D = np.array([[KV]]) if conformal else np.array([[KV, coupling], [coupling, axial_modulus]])
    A = D + PHI*L.T@CS@L
    Cd = PHI*CS - PHI**2*CS@L@np.linalg.solve(A, L.T@CS)
    B = IV-Cd@np.linalg.solve(CS, IV)
    S = (1-PHI)/KF + PHI**2*(IV@L)@np.linalg.solve(A, L.T@IV)
    return m, n, L, D, A, Cd, B, S


def finite(E, p, angle=45., coupling=KC):
    m, n, L, D, A, Cd, B, S = coefficients(angle, coupling)
    e, t = mandel(E), L.T@IV
    if np.linalg.norm(E@tensor(L[:, 1])-tensor(L[:, 1])@E) > 1e-10:
        raise ValueError('The finite benchmark requires commuting strain and fabric')
    xlin = np.linalg.solve(A, PHI*(L.T@CS@e+p*t))
    def residual(x):
        y = np.exp(IV@e-t@x)
        return A@x-PHI*L.T@CS@e-PHI*p*y*t
    def hessian(x):
        return A+PHI*p*np.exp(IV@e-t@x)*np.outer(t, t)
    sol = root(residual, xlin, jac=hessian, tol=1e-11)
    x = sol.x
    if np.linalg.norm(residual(x)) > 2e-12:
        raise RuntimeError(sol.message)
    J, y = np.exp(IV@e), np.exp(IV@e-t@x)
    solid = PHI*y/J
    if not 0 < solid < 1:
        raise ValueError('Nonpositive phase volume')
    sigma = tensor(PHI*CS@(e-L@x)/J)-(1-solid)*p*I
    # Exact implicit derivative in the commuting family.
    dxde = np.linalg.solve(hessian(x), PHI*L.T@CS+PHI*p*y*np.outer(t, IV))
    bv = IV-PHI*y/J*(IV-t@dxde)
    return dict(x=x, J=J, y=y, solid=solid, sigma=sigma, B=tensor(bv),
                ln_h=-x[1]/np.sqrt(1.5), pore=J-PHI*y,
                residual=np.linalg.norm(residual(x)), hessian=hessian(x),
                F=expm(E), L=L, D=D)


def candidate_energy(F, x, p, L, D):
    """Unreduced potential; used for derivatives at commuting states only."""
    Ainv = expm(-tensor(L@x))
    Fbar = Ainv@F
    vals, V = np.linalg.eigh(Fbar.T@Fbar)
    eb = mandel((V*(.5*np.log(vals)))@V.T)
    y, J = np.linalg.det(Fbar), np.linalg.det(F)
    return .5*x@D@x+.5*PHI*eb@CS@eb+PHI*p*y-p*J


def linear(E, p):
    _, _, L, D, A, Cd, B, S = coefficients()
    e = mandel(E)
    x = np.linalg.solve(A, PHI*(L.T@CS@e+p*L.T@IV))
    return dict(sigma=tensor(Cd@e-B*p), pore=(1-PHI)+B@e+(S-(1-PHI)/KF)*p,
                ln_h=-x[1]/np.sqrt(1.5))


def save_csv(name, rows):
    with (OUT/name).open('w') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


def save_fig(fig, name):
    for ext in ('png', 'pdf'):
        fig.savefig(OUT/(name+'.'+ext), dpi=220, bbox_inches='tight',
                    metadata={'Creator': 'fabric_insight.py', 'CreationDate': None, 'ModDate': None} if ext == 'pdf' else None)
    plt.close(fig)


def verify():
    errors, balance, pressure, minima, stationarity = [], [], [], [], []
    m, n, *_ = coefficients()
    T = np.outer(m, m)-np.outer(n, n)
    for gamma in (-.4, 0., .45):
        for p in (0., .3, .8):
            E = gamma*T
            s = finite(E, p)
            minima.append(float(np.linalg.eigvalsh(s['hessian']).min()))
            stationarity.append(float(s['residual']))
            # Envelope derivative of the unreduced spectral energy, holding the
            # converged internal variable fixed. Every F entry is perturbed.
            errs = []
            for h in (2e-4, 1e-4, 5e-5):
                P = np.zeros((3, 3))
                for i in range(3):
                    for j in range(3):
                        d = np.zeros((3, 3)); d[i, j] = h
                        P[i, j] = (candidate_energy(s['F']+d, s['x'], p, s['L'], s['D'])-
                                   candidate_energy(s['F']-d, s['x'], p, s['L'], s['D']))/(2*h)
                errs.append(float(np.linalg.norm(P@s['F'].T/s['J']-s['sigma'])))
            balance.append(errs)
            h = 1e-5
            ds = (finite(E, p+h)['sigma']-finite(E, p-h)['sigma'])/(2*h)
            pressure.append(float(np.linalg.norm(ds+s['B'])))
            # Independent minimization of the spectral energy at the fixed F.
            opt = minimize(lambda x: candidate_energy(s['F'], x, p, s['L'], s['D']),
                           np.zeros(2), method='BFGS', options={'gtol': 1e-10})
            errors.append(float(np.linalg.norm(opt.x-s['x'])))
    ref = []
    for a in (.01, .005, .0025, .00125):
        E, p = a*T, .5*a
        ref.append(float(np.linalg.norm(finite(E, p)['sigma']-linear(E, p)['sigma'])))
    rates = np.log2(np.array(ref[:-1])/ref[1:])
    # Reference pressure reaction computed by eliminating internal strain;
    # compare with B transformed from its principal values.
    rotation_error = []
    for angle in np.linspace(-90, 90, 19):
        m, _, L, D, A, Cd, B, S = coefficients(angle)
        x = np.linalg.solve(A, PHI*.02*(L.T@IV))
        sig = -PHI*CS@L@x-(1-PHI)*.02*IV
        rotation_error.append(float(np.linalg.norm(sig+.02*B)))
    report = dict(category='finite_commuting_material_verification',
                  maximum_stationarity_residual=max(stationarity),
                  minimum_internal_hessian_eigenvalue=min(minima),
                  full_spatial_stress_fd_errors=balance,
                  full_spatial_stress_max_error=max(e[-1] for e in balance),
                  pressure_tangent_max_error=max(pressure),
                  independent_minimization_max_state_error=max(errors),
                  reference_limit_errors=ref, reference_limit_orders=rates.tolist(),
                  reference_reaction_max_error=max(rotation_error),
                  scope='Isotropic mineral; coaxial finite strain and distention. No general noncoaxial finite law or experimental validation.')
    assert report['full_spatial_stress_max_error'] < 2e-8
    assert report['pressure_tangent_max_error'] < 1e-8
    assert max(errors) < 2e-7
    assert min(rates) > 1.95
    assert max(rotation_error) < 1e-12
    (OUT/'verification.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    apply_style()
    report = verify()
    fig, axs = plt.subplots(1, 2, figsize=(6.35, 2.8), layout='constrained')
    rows = []
    for case, coupling, conformal, style in [('coupled', KC, False, '-'),
                      ('uncoupled', 0., False, '--'), ('conformal', 0., True, ':')]:
        yy = []
        for angle in np.linspace(-90, 90, 73):
            _, _, _, _, _, _, B, _ = coefficients(angle, coupling, conformal)
            yy.append(-tensor(B)[0, 1])
            rows.append(dict(case=case, angle=angle, shear_per_pressure=yy[-1],
                             normal11_per_pressure=-B[0], normal22_per_pressure=-B[1]))
        axs[0].plot(np.linspace(-90, 90, 73), yy, style, label=case)
    axs[0].set(xlabel='Fabric angle (degrees)', ylabel=r'$\Delta\sigma_{12}/\Delta p$',
               title='(a) Angular shear response')
    axs[0].legend(fontsize=7)
    ratios = np.geomspace(.02, 20., 61)
    couplings = np.linspace(-.9, .9, 73)
    sweep, sweeprows = [], []
    for ratio in ratios:
        line = []
        for normalized in couplings:
            ka = ratio*KV
            kc = normalized*np.sqrt(KV*ka)
            _, _, _, D, _, _, B, _ = coefficients(45., kc, False, ka)
            assert np.linalg.eigvalsh(D).min() > 0
            reaction = -tensor(B)[0, 1]
            line.append(reaction)
            sweeprows.append(dict(axial_over_volume=ratio, normalized_coupling=normalized,
                                 shear_per_pressure=reaction))
        sweep.append(line)
    im = axs[1].pcolormesh(couplings, ratios, sweep, shading='auto', cmap='coolwarm', rasterized=True,
                           vmin=-np.max(np.abs(sweep)), vmax=np.max(np.abs(sweep)))
    axs[1].set(yscale='log', xlabel=r'$k_c/\sqrt{k_vk_a}$', ylabel=r'$k_a/k_v$',
               title=r'(b) Shear reaction at $45^\circ$')
    axs[1].plot(KC/np.sqrt(KV*KA), KA/KV, 'ko', markerfacecolor='none', markersize=5)
    fig.colorbar(im, ax=axs[1], label=r'$\Delta\sigma_{12}/\Delta p$')
    save_csv('pressure_shear_moduli.csv', sweeprows)
    save_fig(fig, 'fabric_pressure_shear'); save_csv('pressure_shear.csv', rows)

    m, n, *_ = coefficients()
    T = np.outer(m, m)-np.outer(n, n)
    rows = []
    for gamma in np.linspace(-.6, .6, 81):
        s, lin = finite(gamma*T, .5), linear(gamma*T, .5)
        zero, linzero = finite(gamma*T, 0.), linear(gamma*T, 0.)
        rows.append(dict(gamma=gamma, p=.5, shear=s['sigma'][0, 1]-zero['sigma'][0, 1],
                         shear_linear=lin['sigma'][0, 1]-linzero['sigma'][0, 1], pore=s['pore'],
                         pore_linear=lin['pore'], ln_h=s['ln_h']-zero['ln_h'], ln_h_linear=lin['ln_h']-linzero['ln_h'],
                         J=s['J'], Jbar=s['y'], solid_fraction=s['solid']))
    save_csv('finite_fabric.csv', rows)
    fig, axs = plt.subplots(2, 2, figsize=(6.35, 5.1), layout='constrained')
    for ax, key, label, title in zip(axs.flat, ['shear', 'pore', 'ln_h'],
                [r'$[\sigma_{12}(p)-\sigma_{12}(0)]/K_*$', r'$J-\phi_{s0}\bar J$', r'$\ln h(p)-\ln h(0)$'],
                ['(a) Pressure-induced shear stress', '(b) Pore volume', '(c) Pressure-induced shape change']):
        ax.plot([r['gamma'] for r in rows], [r[key] for r in rows], label='finite')
        ax.plot([r['gamma'] for r in rows], [r[key+'_linear'] for r in rows], '--', label='reference linearization')
        ax.set(xlabel=r'Logarithmic shear $\gamma$', ylabel=label, title=title)
    axs[0, 0].legend(fontsize=7)
    grid, erows = [], []
    for p in np.linspace(0, 1., 41):
        line = []
        for gamma in np.linspace(-.6, .6, 49):
            s, lin = finite(gamma*T, p), linear(gamma*T, p)
            error = np.linalg.norm(s['sigma']-lin['sigma'])/KS
            line.append(error)
            erows.append(dict(gamma=gamma, p=p, stress_error_over_Ks=error,
                              pore=s['pore'], solid_fraction=s['solid'],
                              hessian_min=np.linalg.eigvalsh(s['hessian']).min()))
        grid.append(line)
    im = axs[1, 1].imshow(grid, origin='lower', extent=(-.6, .6, 0, 1), aspect='auto', cmap='viridis')
    axs[1, 1].set(xlabel=r'Logarithmic shear $\gamma$', ylabel=r'$p/K_*$', title='(d) Stress error of the linearization')
    fig.colorbar(im, ax=axs[1, 1], label=r'$\|\mathbf{\sigma}-\mathbf{\sigma}_{\rm lin}\|/K_s$')
    save_fig(fig, 'fabric_finite'); save_csv('finite_error.csv', erows)
    inputs = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in [Path(__file__), ROOT/'examples/figure_style.py']}
    params = dict(phi=PHI, Ks=KS, mu=MU, Kf=KF, kv=KV, ka=KA, kc=KC,
                  path='E=gamma(m outer m - n outer n); m at 45 degrees; n in-plane normal',
                  finite_linear_comparison='linear model evaluated on E, isolating constitutive truncation from engineering-strain substitution')
    manifest = dict(parameters=params, versions=dict(python=sys.version.split()[0], numpy=np.__version__, scipy=scipy.__version__, matplotlib=matplotlib.__version__), input_sha256=inputs,
                    output_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in [OUT/name for name in ('fabric_pressure_shear.png', 'fabric_pressure_shear.pdf', 'fabric_finite.png', 'fabric_finite.pdf', 'pressure_shear.csv', 'pressure_shear_moduli.csv', 'finite_fabric.csv', 'finite_error.csv', 'verification.json')]})
    (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
