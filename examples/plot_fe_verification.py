#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Assemble the finite-element verification displays from recorded artifacts.

The manuscript's finite-element section reports manufactured-solution orders, a
step-refinement ratio, and a finite-load error floor, but those results were
only published in the companion evidence file. This script turns the recorded
evidence already shipped in ``figures/`` and ``fe-evidence/`` into the two
in-manuscript displays:

``fe_verification_convergence``
    (a) manufactured-solution spatial L2 errors and their measured orders,
    (b) the fixed-mesh successive-difference temporal orders, and
    (c) the finite-load pressure discrepancy showing the discretization floor.

``fe_reference_comparison``
    (a) the linear constant-reference-tangent Mandel histories against the
    independently evaluated series, and (b) the pressure profiles at the saved
    exact comparison times.

Every value is read from a recorded CSV or JSON artifact; nothing is fitted,
interpolated, or synthesised, and a missing input is reported rather than
filled.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / 'figures'
from figure_style import COLORS, apply_style, publication_size
apply_style()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def table(path):
    return np.atleast_1d(np.genfromtxt(path, names=True, delimiter=',', dtype=None,
                                       encoding='utf-8'))


class Report:
    def __init__(self, output):
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=True)
        self.inputs, self.outputs, self.figures, self.missing = {}, {}, [], []

    def source(self, path):
        path = Path(path).resolve()
        key = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else path.name
        self.inputs[key] = sha(path)

    def save(self, fig, name, caption, sources):
        publication_size(fig)
        files = []
        for ext in ('pdf', 'png', 'pgf'):
            path = self.output / (name + '.' + ext)
            kwargs = dict(dpi=220)
            if ext != 'pgf':
                kwargs['metadata'] = {'Creator': 'plot_fe_verification.py',
                                      'CreationDate': None, 'ModDate': None}
            fig.savefig(path, **kwargs)
            files.append(path.name)
            self.outputs[path.name] = sha(path)
        plt.close(fig)
        self.figures.append(dict(id=name, files=files, caption=caption,
                                 sources=list(sources)))

    def absent(self, family, reason):
        self.missing.append(dict(family=family, reason=reason))


def convergence_figure(report):
    mms_csv = ROOT / 'figures/fe_mms_convergence.csv'
    mms_json = ROOT / 'fe-evidence/mms-convergence.json'
    refine_csv = ROOT / 'figures/fe_mandel_refinement.csv'
    load_csv = ROOT / 'figures/fe_load_limit.csv'
    for path in (mms_csv, mms_json, load_csv):
        if not path.is_file():
            report.absent(path.name, 'Recording is absent')
            return
    for path in (mms_csv, mms_json, refine_csv, load_csv):
        if path.is_file():
            report.source(path)

    mms = table(mms_csv)
    orders = json.loads(mms_json.read_text())
    load = table(load_csv)
    refine = table(refine_csv)

    fig, axes = plt.subplots(2, 2, figsize=(8.6, 6.0), layout='constrained')
    axes = axes.ravel()

    # (a) manufactured-solution spatial refinement.
    ax = axes[0]
    space = mms[mms['family'] == 'mms_space_']
    for j, field in enumerate(('p', 'ux', 'uy')):
        rows = sorted((r for r in space if r['field'] == field), key=lambda r: r['h'])
        x = np.array([r['h'] for r in rows])
        y = np.array([r['l2_error'] for r in rows])
        ax.loglog(x, y, 'o-', color=COLORS[j], label=field)
        observed = np.log(y[:-1] / y[1:]) / np.log(x[:-1] / x[1:])
        ax.annotate(', '.join(f'{v:.2f}' for v in observed), (x[0], y[0]),
                    textcoords='offset points', xytext=(4, 5 if j != 2 else 20), fontsize=7,
                    color=COLORS[j])
    ax.set(xlabel='$h$ [length unit]', ylabel=r'$L^2$ error',
           title='(a) Manufactured solution, spatial')
    ax.grid(alpha=.2, which='both')
    ax.legend()

    # (b) fixed-mesh successive-difference temporal orders.
    ax = axes[1]
    meshes = ['nx16', 'nx32', 'nx64']
    for j, field in enumerate(('p', 'ux', 'uy')):
        y = [orders['time'][mesh]['orders'][field + '_l2']['difference_orders'][0]
             for mesh in meshes]
        ax.plot([16, 32, 64], y, 'o-', color=COLORS[j], label=field)
    ax.axhline(1.0, color='k', ls='--', lw=.9, label='first order')
    ax.set(xlabel=r'$nx$ (fixed $h$ per curve)', ylabel='successive-difference order',
           xticks=[16, 32, 64], title='(b) Temporal order at fixed mesh')
    ax.grid(alpha=.2)
    ax.legend()

    # (c) linear step refinement of the constant-tangent comparison.
    ax = axes[2]
    time_family = [r for r in refine if r['family'] == 'linear_time_'
                   and r['metric'] == 'pressure_max_normalized']
    time_family.sort(key=lambda r: r['dt'])
    x = np.array([r['dt'] for r in time_family])
    y = np.array([r['error'] for r in time_family])
    ax.loglog(x, y, 'o-', color=COLORS[0], label='normalized pressure error')
    if len(y) > 1:
        ratio = y[-1] / y[0]
        ax.annotate(f'ratio {ratio:.2f}', (x[0], y[0]), textcoords='offset points',
                    xytext=(6, 6), fontsize=7.5, color=COLORS[0])
    ax.set(xlabel=r'time step $\Delta t$', ylabel='normalized discrepancy',
           title='(c) Linear step refinement')
    ax.set_xticks(x, [f'{value:g}' for value in x])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.grid(alpha=.2, which='both')
    ax.legend()

    # (d) finite-load floor.
    ax = axes[3]
    rows = sorted((r for r in load if r['metric'] == 'pressure_max_normalized'),
                  key=lambda r: r['load'])
    x = np.array([r['load'] for r in rows])
    y = np.array([r['error'] for r in rows])
    ax.loglog(x, y, 'o-', color=COLORS[0], label='normalized pressure error')
    ax.axhline(y[0], color='k', ls=':', lw=1.0,
               label=f'floor {y[0]:.3g}')
    ax.set(xlabel=r'compressive load $q$', ylabel='normalized discrepancy',
           title='(d) Finite-load comparison')
    ax.grid(alpha=.2, which='both')
    ax.legend()

    report.save(fig, 'fe_verification_convergence',
        'Finite-element verification displays, all read from recorded artifacts. '
        '(a) Manufactured-solution $L^2$ errors against mesh size at the fixed '
        'final time; the annotated numbers are the measured adjacent orders, not '
        'a fitted rate. (b) Temporal order measured by successive differences of '
        'the exact-solution error norms at fixed mesh for $nx=16,32,64$; the '
        'values include entries above unity, and no order above one is asserted. '
        '(c) Linear step refinement of the constant-tangent comparison: the '
        'normalized center-pressure error against the time step, with the measured '
        'coarse/fine ratio annotated. (d) The finite-deformation solutions compared '
        'with the linear Mandel series as the compressive load decreases at fixed '
        'mesh and time step; the pressure discrepancy floors rather than decaying to '
        'the linear reference, so this panel is a demonstration, not a verified limit.',
        ['figures/fe_mms_convergence.csv', 'fe-evidence/mms-convergence.json',
         'figures/fe_mandel_refinement.csv', 'figures/fe_load_limit.csv'])


def reference_figure(report):
    history_csv = ROOT / 'figures/fe_mandel_history.csv'
    profiles_csv = ROOT / 'figures/fe_mandel_profiles.csv'
    for path in (history_csv, profiles_csv):
        if not path.is_file():
            report.absent(path.name, 'Recording is absent')
            return
        report.source(path)
    history = table(history_csv)
    profiles = table(profiles_csv)

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0), layout='constrained')

    ax = axes[0]
    ax.plot(history['time'], history['pressure_reference'], color='k', label='analytical')
    ax.plot(history['time'], history['pressure'], 'o', markevery=max(1, len(history)//20), color=COLORS[0], label='MOOSE')
    ax.set(xlabel='time', ylabel=r'center pressure [stress unit]',
           title='(a) Center-pressure history')
    ax.grid(alpha=.2)
    ax.legend()

    ax = axes[1]
    times = sorted(set(profiles['time']))
    colors = plt.get_cmap('viridis')(np.linspace(0, 1, len(times)))
    for j, time in enumerate(times):
        rows = [r for r in profiles if r['time'] == time]
        x = np.array([r['x'] for r in rows])
        order = np.argsort(x)
        ax.plot(x[order], np.array([r['pressure'] for r in rows])[order], 'o', zorder=3, markevery=max(1, len(order)//20),
                color=colors[j], label=f'MOOSE t={time:g}')
        ax.plot(x[order], np.array([r['pressure_reference'] for r in rows])[order],
                '-', color=colors[j], lw=1.6,
                label='analytical' if j == 0 else None)
    ax.set(xlabel='reference coordinate $X$', ylabel='pressure [stress unit]',
           title='(b) Pressure profiles at saved times')
    ax.grid(alpha=.2)
    ax.legend()

    report.save(fig, 'fe_reference_comparison',
        'Linear constant-reference-tangent Mandel comparison from recorded runs. '
        '(a) Center pressure against time: solid curves show the independently evaluated '
        'series, hollow markers show the finite-element history at identical saved times. '
        '(b) Pressure along the sampled horizontal line at the saved comparison '
        'times. There is no temporal interpolation and no fitted coefficient in '
        'either panel.',
        ['figures/fe_mandel_history.csv', 'figures/fe_mandel_profiles.csv'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    report = Report(args.output)
    report.source(ROOT / 'examples/figure_style.py')
    report.source(Path(__file__))
    convergence_figure(report)
    reference_figure(report)
    manifest = dict(schema_version=1, generator='examples/plot_fe_verification.py',
                    versions=dict(python=platform.python_version(), numpy=np.__version__,
                                  matplotlib=matplotlib.__version__),
                    figures=report.figures, missing=report.missing,
                    input_sha256=report.inputs, output_sha256=report.outputs,
                    limitations=[
                        'Every curve is read from a recorded artifact; this does not certify its scientific acceptance.',
                        'The temporal orders are measurements at fixed mesh and include a mesh-step cross term; no order above one is claimed.',
                        'The finite-load panel is a demonstration, not a verified limit toward the linear solution.',
                    ])
    (args.output / 'fe-verification-plot-manifest.json').write_text(
        json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(dict(figures=len(report.figures), missing=report.missing,
                          files=sorted(report.outputs)), indent=2))


if __name__ == '__main__':
    main()
