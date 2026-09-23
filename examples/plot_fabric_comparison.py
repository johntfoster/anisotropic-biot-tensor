#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Compare recorded coupled histories, check conservation and quantify refinement."""
from pathlib import Path
import hashlib
import json
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from figure_style import apply_style, COLORS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'build/insight'
RUNS = ROOT/'fe-evidence/insight'
ANGLES = (0, 45, 90)
FIELDS = ('center_pressure', 'top_displacement', 'right_reaction')
COMPARISON_COLORS = (COLORS[0], COLORS[1], '#806000')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def norm(values, t):
    return np.sqrt(np.trapezoid(values**2, t))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    apply_style()
    data, checks, inputs = {}, {}, {}
    for angle in ANGLES:
        for level in ('coarse', 'fine'):
            for model in ('tensor', 'scalar'):
                case = f'{model}_{angle}_{level}'
                folder = RUNS/case
                p = folder/'provenance.json'
                record = json.loads(p.read_text())
                history = folder/'solution.csv'
                assert record['exit_code'] == 0 and sha(history) == record['history_sha256']
                for path, digest in record['source_sha256'].items():
                    assert sha(ROOT/path) == digest, ('stale source', path)
                for path in (p, history):
                    inputs[str(path.relative_to(ROOT))] = sha(path)
                d = np.genfromtxt(history, delimiter=',', names=True)
                t = d['time']
                assert np.all(np.diff(t) > 0) and abs(t[-1]-.75) < 1e-10
                change = d['mass']-d['mass'][0]
                integral = np.r_[0., np.cumsum(d['mass_reaction'][1:]*np.diff(t))]
                balance = np.max(np.abs(change-integral))/max(np.max(np.abs(change)), 1e-14)
                final_ratio = abs(d['center_pressure'][-1])/np.max(np.abs(d['center_pressure']))
                peak_time = t[np.argmax(d['center_pressure'])]
                assert balance < 2e-6, (case, balance)
                assert peak_time < .75 and final_ratio < .02, (case, peak_time, final_ratio)
                checks[case] = dict(mass_balance_relative=balance, final_to_peak_pressure=final_ratio,
                                    peak_time=peak_time, peak_pressure=float(d['center_pressure'].max()),
                                    mean_final_settlement=-float(d['top_displacement'][-1]))
                data[model, angle, level] = d
    rows, refinement = [], []
    for angle in ANGLES:
        dt = data['tensor', angle, 'fine']; ds = data['scalar', angle, 'fine']
        assert np.allclose(dt['time'], ds['time'], rtol=0, atol=1e-12)
        for field in FIELDS:
            error = norm(ds[field]-dt[field], dt['time'])/norm(dt[field], dt['time'])
            refs = []
            for model in ('tensor', 'scalar'):
                fine, coarse = data[model, angle, 'fine'], data[model, angle, 'coarse']
                # Compare saved times shared exactly by the two grids.
                ix = np.searchsorted(fine['time'], coarse['time']-1e-10)
                assert np.max(abs(fine['time'][ix]-coarse['time'])) < 1e-9
                difference = norm(coarse[field]-fine[field][ix], coarse['time'])/norm(fine[field][ix], coarse['time'])
                refs.append(difference)
                refinement.append(dict(model=model, angle=angle, field=field, relative_history_difference=difference))
            rows.append(dict(angle=angle, field=field, scalar_relative_L2_error=error,
                             maximum_relative_refinement_difference=max(refs)))
    report = dict(category='coupled_reference_law_comparison', checks=checks,
                  errors=rows, refinement=refinement,
                  norm='trapezoidal time L2 over [0,0.75], divided by tensor-history L2',
                  refinement_scope='20x4 dt=.0025 versus 40x8 dt=.00125; combined space/time sensitivity, not an asymptotic order estimate',
                  parameters=dict(phi=.9, Ks=2.5, mineral_shear=5/6, kv=5.4, ka=1., kc=.4,
                                  Kf=8., mobility=1.5, peak_traction=.0001, ramp_end=.01, end_time=.75))
    (OUT/'comparison_verification.json').write_text(json.dumps(report, indent=2)+'\n')
    with (OUT/'comparison_errors.csv').open('w') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    fig, axs = plt.subplots(2, 2, figsize=(6.35, 5.2), layout='constrained')
    for ax, field, factor, title, ylabel in zip(axs.flat, FIELDS, [1e4, -1e5, 1e5],
         ['(a) Pressure', '(b) Mean settlement', '(c) Lateral reaction'],
         [r'$p/10^{-4}K_*$', r'$-\langle u_2\rangle/10^{-5}$', r'$R_1/10^{-5}$']):
        for angle, color in zip(ANGLES, COMPARISON_COLORS):
            for model, style in [('tensor', '-'), ('scalar', '--')]:
                d = data[model, angle, 'fine']
                ax.plot(d['time'], factor*d[field], style, color=color,
                        label=f'{angle}°' if model == 'tensor' else None)
        ax.axvline(.01, color='.6', linewidth=.7, linestyle=':')
        ax.set(xlabel='Time', ylabel=ylabel, title=title)
    axs[0, 0].legend(title='Fabric angle', fontsize=7, title_fontsize=7)
    ax = axs[1, 1]
    for i, (field, label, color) in enumerate(zip(FIELDS, ['pressure', 'settlement', 'reaction'], COMPARISON_COLORS)):
        rr = [r for r in rows if r['field'] == field]
        ax.bar(np.arange(3)+(i-1)*.25, [100*r['scalar_relative_L2_error'] for r in rr],
               width=.24, label=label, color=color)
    ax.set(xticks=np.arange(3), xticklabels=['0°', '45°', '90°'], xlabel='Fabric angle',
           ylabel='Relative history error (%)', title='(d) Error of the scalar approximation')
    ax.legend(fontsize=7)
    for ext in ('png', 'pdf', 'pgf'):
        kwargs = dict(dpi=220, bbox_inches='tight')
        if ext == 'pdf':
            kwargs['metadata'] = {'CreationDate': None, 'ModDate': None}
        fig.savefig(OUT/('fabric_comparison.'+ext), **kwargs)
    plt.close(fig)
    maxrefs = [100*max(r['relative_history_difference'] for r in refinement if r['field']==field) for field in FIELDS]
    errorranges = {}
    for field in FIELDS:
        vals = [100*r['scalar_relative_L2_error'] for r in rows if r['field']==field]
        errorranges[field] = f'{min(vals):.2f}'+r'\text{--}'+f'{max(vals):.2f}'
    balance_mantissa, balance_exponent = f"{max(r['mass_balance_relative'] for r in checks.values()):.1e}".split('e')
    balance_tex = balance_mantissa + r'\times10^{' + str(int(balance_exponent)) + '}'
    summary = r'''\Cref{fig:fe-fabric-mandel} shows the complete histories on the
\(40\times8\) mesh with \(\Delta t=0.00125\). Relative errors use the
trapezoidal time \(L^2\) norm over \([0,0.75]\), divided by the corresponding
tensor-history norm. Across the three orientations, the scalar approximation
produces pressure errors of \(%s\,\%%\), settlement errors of
\(%s\,\%%\), and lateral-reaction errors of \(%s\,\%%\).
A joint refinement from \(20\times4\), \(\Delta t=0.0025\), changes these
pressure, settlement and reaction histories by at most
\(%.2f\,\%%\), \(%.2f\,\%%\), and \(%.2f\,\%%\), respectively,
in the same relative norm (using each model's own fine history). This is a measured sensitivity to combined
space and time refinement, not an asymptotic convergence-order claim.
The end-of-run pressure is below \(%.2f\,\%%\) of its maximum in every
run, so the observation interval resolves loading and substantial drainage.
The accumulated boundary pressure residual balances the fluid-mass change
to a maximum relative discrepancy of \(%s\).
''' % (errorranges[FIELDS[0]], errorranges[FIELDS[1]], errorranges[FIELDS[2]],
       *maxrefs, 100*max(r['final_to_peak_pressure'] for r in checks.values()),
       balance_tex)
    (OUT/'comparison_summary.tex').write_text(summary)
    inputs[str(Path(__file__).relative_to(ROOT))] = sha(Path(__file__))
    inputs['examples/figure_style.py'] = sha(ROOT/'examples/figure_style.py')
    (OUT/'comparison_manifest.json').write_text(json.dumps(dict(input_sha256=inputs,
         output_sha256={p.name:sha(p) for p in [OUT/'fabric_comparison.png', OUT/'fabric_comparison.pdf',
                   OUT/'comparison_verification.json', OUT/'comparison_errors.csv', OUT/'comparison_summary.tex']}), indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
