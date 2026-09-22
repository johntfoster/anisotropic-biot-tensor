#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Plot the recorded pore-fabric probe and coupled runs.

Every number is read from the recorded ``solution.csv`` histories under the
shipped provenance tree ``fe-evidence/runs`` (override with ``--runs``).
Nothing is fitted,
interpolated, or synthesised; a family whose runs are absent is reported in the
manifest instead of being drawn.

Two figures are produced:

``fe_fabric_probe``
    Reference-state Biot tensor components and the shape (deviatoric) response
    of the transversely isotropic distention law. The probe prescribes a uniform
    deformation, so this figure is a direct comparison against the section
    equations, not a boundary-value result.

``fe_fabric_mandel``
    The coupled transient consolidation problem with the fabric rotated in the
    plane. The mineral is isotropic and unrotated, so any directional pressure
    difference is produced by the pore fabric alone. These are finite-load
    demonstrations, not quantitative verification of the nonlinear law.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNS = ROOT / 'fe-evidence/runs'
DEFAULT_OUT = ROOT / 'build/fabric-plots'

from figure_style import COLORS, apply_style, publication_size
apply_style()

# Case -> (label, fabric angle in degrees, volume-axial coupling)
PROBE_CASES = [
    ('fabric_probe_iso', 'no coupling', None, 0.0),
    ('fabric_probe_coup_a0', 'coupling 0.4, $0^\\circ$', 0.0, 0.4),
    ('fabric_probe_coup_a45', 'coupling 0.4, $45^\\circ$', 45.0, 0.4),
    ('fabric_probe_coup_a90', 'coupling 0.4, $90^\\circ$', 90.0, 0.4),
    ('fabric_probe_stiffaxial', 'frozen shape', None, 0.0),
    ('fabric_probe_softaxial', 'soft axial', None, 0.0),
    ('fabric_probe_conformal', 'conformal limit', None, None),
]
SHAPE_CASES = [
    ('fabric_probe_a0', '$0^\\circ$', 0.0),
    ('fabric_probe_a45', '$45^\\circ$', 45.0),
    ('fabric_probe_a90', '$90^\\circ$', 90.0),
]
MANDEL_CASES = [
    ('fabric_mandel_iso', 'no coupling', None),
    ('fabric_mandel_coup_a0', 'coupling 0.4, $0^\\circ$', 0.0),
    ('fabric_mandel_coup_a45', 'coupling 0.4, $45^\\circ$', 45.0),
    ('fabric_mandel_coup_a90', 'coupling 0.4, $90^\\circ$', 90.0),
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def table(path):
    return np.atleast_1d(np.genfromtxt(path, names=True, delimiter=','))


def final_row(data):
    """Last recorded time; the probe decks reach a single prescribed state."""
    return {name: float(data[name][-1]) for name in data.dtype.names}


class Figures:
    def __init__(self, output):
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=True)
        self.inputs, self.outputs, self.figures, self.missing = {}, {}, [], []
        self.source(ROOT / 'examples/plot_fabric_results.py')

    def source(self, path):
        path = Path(path).resolve()
        actual = sha(path)
        key = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else path.name
        if key in self.inputs and self.inputs[key] != actual:
            raise ValueError(f'Input changed during plotting: {key}')
        self.inputs[key] = actual
        return actual

    def csv(self, name, rows):
        if not rows:
            return
        path = self.output / (name + '.csv')
        with path.open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        self.outputs[path.name] = sha(path)

    def save(self, fig, name, caption, cases, data):
        publication_size(fig)
        files = []
        for ext in ('pdf', 'png'):
            path = self.output / (name + '.' + ext)
            # Omit the PDF date metadata so the recorded figure is byte-stable
            # across reruns and platforms.
            fig.savefig(path, dpi=220,
                        metadata={'Creator': 'plot_fabric_results.py',
                                  'CreationDate': None, 'ModDate': None})
            files.append(path.name)
            self.outputs[path.name] = sha(path)
        plt.close(fig)
        self.figures.append(dict(id=name, files=files, caption=caption,
                                 cases=list(cases), data=list(data)))

    def absent(self, family, reason):
        self.missing.append(dict(family=family, reason=reason))


def load_probe(runs, case, figures):
    path = runs / case / 'solution.csv'
    if not path.is_file():
        figures.absent(case, 'Recorded scalar history is absent')
        return None
    figures.source(path)
    data = table(path)
    if len(data) < 2:
        figures.absent(case, 'Recorded history has no converged state')
        return None
    return data


def probe_figure(runs, figures):
    records, rows = {}, []
    for case, label, angle, coupling in PROBE_CASES:
        data = load_probe(runs, case, figures)
        if data is None:
            continue
        row = final_row(data)
        records[case] = dict(label=label, angle=angle, coupling=coupling, row=row)
        rows.append(dict(case=case, label=label, fabric_angle_deg=angle,
                         fabric_coupling=coupling, **row))
    shape, shape_rows = {}, []
    for case, label, angle in SHAPE_CASES:
        data = load_probe(runs, case, figures)
        if data is None:
            continue
        row = final_row(data)
        shape[case] = dict(label=label, angle=angle, row=row)
        shape_rows.append(dict(case=case, label=label, fabric_angle_deg=angle, **row))
    if not records and not shape:
        return

    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.0), layout='constrained')

    # (a) Biot components per probe case
    names = [r['label'] for r in records.values()]
    par = [r['row']['B_par'] for r in records.values()]
    per = [r['row']['B_per'] for r in records.values()]
    y = np.arange(len(names))
    ax = axes[0]
    ax.barh(y - .19, par, height=.36, color=COLORS[0], label=r'$B_\parallel$')
    ax.barh(y + .19, per, height=.36, color=COLORS[1], label=r'$B_\perp$')
    ax.set(yticks=y, yticklabels=names, xlabel=r'Biot coefficient', title='(a) Biot coefficients')
    ax.invert_yaxis()
    ax.legend(loc='lower right')
    ax.grid(alpha=.2, axis='x')

    # (b) anisotropy of B and its compliance origin
    ax = axes[1]
    aniso = [r['row']['B_anisotropy'] for r in records.values()]
    ax.barh(y, aniso, color='0.35')
    ax.set(yticks=y, yticklabels=[], xlabel=r'$B_\parallel - B_\perp$',
           title='(b) Directional difference')
    ax.invert_yaxis()
    ax.axvline(0, color='k', lw=.8)
    ax.grid(alpha=.2, axis='x')

    # (c) shape response: ln h against fabric orientation
    ax = axes[2]
    if shape:
        angles = [r['angle'] for r in shape.values()]
        lhs = [r['row']['ln_h'] for r in shape.values()]
        order = np.argsort(angles)
        ax.plot(np.array(angles)[order], np.array(lhs)[order], 'o-', color=COLORS[0])
        ax.set(xlabel='fabric angle (degrees)', ylabel=r'$\ln h$',
               title='(c) Shape response')
    else:
        ax.text(.5, .5, 'Shape-response probes absent', ha='center', va='center',
                transform=ax.transAxes)
    ax.grid(alpha=.2)

    figures.csv('fe_fabric_probe', rows + shape_rows)
    figures.save(fig, 'fe_fabric_probe',
        'Reference-state pore-fabric probes (uniform prescribed deformation, '
        'one QUAD4 element: eps11=0.01, eps22=-0.005, p=0.02). (a) Axial and '
        'transverse Biot coefficients from the recorded final state. The '
        'conformal-limit case reduces to the reviewed ConformalMaterial. (b) '
        'B_par - B_per: with an isotropic mineral the Biot tensor stays '
        'isotropic unless the volume-axial coupling of the distention stiffness '
        'is nonzero, so the coupling rows carry the directional coupling. '
        '(c) ln h, the fabric shape (deviatoric) distention, against fabric '
        'orientation for '
        'the uncoupled probes; the Biot tensor of those probes is isotropic and '
        'is plotted in (a,b) only for the coupled variants. Values are read from '
        'the recorded run histories with no fitting or interpolation.',
        [case for case in records] + [case for case in shape],
        ['fe_fabric_probe.csv'])


def mandel_figure(runs, figures):
    series, rows, peak = {}, [], []
    for case, label, angle in MANDEL_CASES:
        path = runs / case / 'solution.csv'
        if not path.is_file():
            figures.absent(case, 'Recorded scalar history is absent')
            continue
        figures.source(path)
        data = table(path)
        if not len(data):
            figures.absent(case, 'Recorded history is empty')
            continue
        series[case] = dict(label=label, angle=angle, data=data)
        rows.extend(dict(case=case, label=label, fabric_angle_deg=angle,
                         time=float(t), center_pressure=float(p),
                         edge_ux=float(u), platen_max=float(m))
                    for t, p, u, m in zip(data['time'], data['center_pressure'],
                                          data['edge_ux'], data['platen_max']))
        peak.append(dict(case=case, label=label, fabric_angle_deg=angle,
                         peak_center_pressure=float(np.max(data['center_pressure'])),
                         final_center_pressure=float(data['center_pressure'][-1]),
                         final_time=float(data['time'][-1]),
                         peak_stability=float(np.max(data['stability_max']))))
    if not series:
        return

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0), layout='constrained')
    ax = axes[0]
    for j, (case, item) in enumerate(series.items()):
        style = dict(color='k', ls='--') if item['angle'] is None else dict(color=COLORS[j % len(COLORS)])
        ax.plot(item['data']['time'], item['data']['center_pressure'], marker='o', markevery=max(1, len(item['data'])//20), **style, label=item['label'])
    ax.set(xlabel='time', ylabel='center pressure', title='(a) Center-pressure history')
    ax.grid(alpha=.2)
    ax.legend()

    ax = axes[1]
    oriented = [p for p in peak if p['fabric_angle_deg'] is not None]
    flat = [p for p in peak if p['fabric_angle_deg'] is None]
    if oriented:
        order = np.argsort([p['fabric_angle_deg'] for p in oriented])
        x = [oriented[i]['fabric_angle_deg'] for i in order]
        y = [oriented[i]['peak_center_pressure'] for i in order]
        ax.plot(x, y, 'o-', color=COLORS[0], label='fabric rotated')
        ax.set_xlabel('fabric orientation (degrees)')
    for item in flat:
        ax.axhline(item['peak_center_pressure'], color='k', ls='--', lw=1.2,
                   label=item['label'])
    ax.set(ylabel='peak center pressure', title='(b) Directional pressure response')
    ax.grid(alpha=.2)
    ax.legend()

    axes[0].xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
    figures.csv('fe_fabric_mandel_history', rows)
    figures.csv('fe_fabric_mandel_peak', peak)
    figures.save(fig, 'fe_fabric_mandel',
        'Coupled transient consolidation (quarter Mandel geometry, isotropic and '
        'unrotated mineral) with the pore fabric rotated in the plane. (a) Center '
        'pressure against recorded time for each fabric orientation. (b) Peak '
        'center pressure against fabric orientation, with the uncoupled fabric '
        'reference drawn as a dashed line. Because the mineral is isotropic and '
        'unrotated, the directional difference isolates the pore fabric. These '
        'are finite-load demonstrations of the coupled model, not quantitative '
        'verification of the nonlinear law and not experimental validation.',
        [case for case in series], ['fe_fabric_mandel_history.csv', 'fe_fabric_mandel_peak.csv'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs', type=Path, default=DEFAULT_RUNS)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    figures = Figures(args.output)
    figures.source(ROOT / 'examples/figure_style.py')
    probe_figure(args.runs, figures)
    mandel_figure(args.runs, figures)
    report = dict(
        schema_version=1,
        generator='examples/plot_fabric_results.py',
        versions=dict(python=platform.python_version(), numpy=np.__version__,
                      matplotlib=matplotlib.__version__),
        figures=figures.figures,
        missing=figures.missing,
        input_sha256=figures.inputs,
        output_sha256=figures.outputs,
        limitations=[
            'Only recorded successful runs are plotted; this does not certify their scientific acceptance.',
            'The probe figure is a uniform prescribed-deformation comparison, not a boundary-value verification.',
            'The coupled fabric runs are finite-load demonstrations, not quantitative verification and not experimental validation.',
            'Parameters are synthetic; physical validation has not been performed.',
        ])
    (args.output / 'fabric-plot-manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(figures=len(figures.figures),
                          missing=figures.missing,
                          files=sorted(figures.outputs)), indent=2))


if __name__ == '__main__':
    main()
