#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Plot the recorded pore-fabric contour fields from the refined (40 x 8) runs.

Reads only the recorded Exodus field files under ``fe-evidence/runs`` (netCDF4)
and emits two figures plus CSV sidecars:

``fe_fabric_contours``
    Pore pressure ``p`` and displacement magnitude ``|u|`` at one common time,
    one column per fabric variant (isotropic, axis 0/45/90 deg), as filled
    contours with colourbars, equal aspect, a domain outline, and a fabric-axis
    indicator.

``fe_fabric_diffusion``
    Pore-pressure contour snapshots at several recorded times for the isotropic
    case and one coupled case, showing the Mandel-type drainage front.

``fe_fabric_contours.csv`` / ``fe_fabric_diffusion.csv``
    Per case and recorded time: the plotted extrema and the pressure-maximum
    location. Every number quoted downstream comes from these sidecars.

Nothing is fitted, interpolated in time, or synthesised: the fields are read
directly from the recorded Exodus files and the time samples are the recorded
time steps. These runs are finite-load demonstrations on synthetic parameters,
not mesh-convergence studies.
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
import netCDF4

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNS = ROOT / 'fe-evidence/runs'
DEFAULT_OUT = ROOT / 'figures'

NODAL = ['force_reaction', 'mass_reaction', 'p', 'ux', 'uy']
CASES = [
    ('fabric_contour_iso', 'isotropic', None),
    ('fabric_contour_a0', '$0^\\circ$', 0.0),
    ('fabric_contour_a45', '$45^\\circ$', 45.0),
    ('fabric_contour_a90', '$90^\\circ$', 90.0),
]
# Representative coupled case used for the diffusion row.
DIFFUSION_COUPLED = 'fabric_contour_a45'
# Recorded time indices for the diffusion figure (of the 11 snapshots).
DIFFUSION_TIME_IDX = [0, 2, 4, 6, 8, 10]

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8,
                     'axes.labelsize': 8, 'legend.fontsize': 7,
                     'axes.titlesize': 9, 'lines.linewidth': 1.2,
                     'pdf.fonttype': 42, 'savefig.bbox': 'tight',
                     'axes.spines.top': False, 'axes.spines.right': False})


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_exodus(case, runs):
    path = runs / case / 'solution.e'
    if not path.is_file():
        raise SystemExit('recorded Exodus field not found: ' + str(path))
    ds = netCDF4.Dataset(str(path))
    x = ds.variables['coordx'][:].astype(float)
    y = ds.variables['coordy'][:].astype(float)
    t = ds.variables['time_whole'][:].astype(float)

    def nodal(name):
        idx = NODAL.index(name) + 1
        return ds.variables[f'vals_nod_var{idx}'][:].astype(float)

    out = dict(x=x, y=y, t=t, p=nodal('p'), ux=nodal('ux'), uy=nodal('uy'))
    ds.close()
    out['u_mag'] = np.hypot(out['ux'], out['uy'])
    return out


def pressure_extrema(field, x, y):
    i = int(np.argmax(field))
    return dict(p_min=float(field.min()), p_max=float(field.max()),
                p_max_x=float(x[i]), p_max_y=float(y[i]))


def outline(ax):
    ax.plot([0, 1, 1, 0, 0], [0, 0, 0.1, 0.1, 0], color='k', lw=0.9, clip_on=False)


def fabric_indicator(ax, angle_deg):
    """Draw a fabric-axis arrow centred on the domain."""
    th = np.radians(angle_deg)
    cx, cy = 0.5, 0.05
    length = 0.045
    dx, dy = length * np.cos(th), length * np.sin(th)
    ax.annotate('', xy=(cx + dx, cy + dy), xytext=(cx - dx, cy - dy),
                arrowprops=dict(arrowstyle='-|>', color='#D55E00', lw=1.6,
                                mutation_scale=12))


def contours_figure(fields, out_dir, manifest):
    # One common time: the final recorded state (where the peak pressures are read).
    ti = len(fields['fabric_contour_iso']['t']) - 1
    t_common = float(fields['fabric_contour_iso']['t'][ti])

    fig, axes = plt.subplots(2, 4, figsize=(12.0, 4.4), layout='constrained')
    rows = [('p', r'pore pressure $p$'), ('u_mag', r'displacement $|\mathbf{u}|$')]
    csv_rows = []
    for j, (case, label, angle) in enumerate(CASES):
        f = fields[case]
        for r, (key, _) in enumerate(rows):
            ax = axes[r][j]
            field = f[key][ti]
            if key == 'p':
                vmax = float(field.max())
            else:
                vmax = float(field.max())
            levels = np.linspace(0.0, vmax, 21)
            cf = ax.tricontourf(f['x'], f['y'], field, levels=levels, cmap='viridis')
            fig.colorbar(cf, ax=ax, fraction=0.03, pad=0.02)
            ax.set_aspect('equal')
            outline(ax)
            if angle is not None:
                fabric_indicator(ax, angle)
            ax.set_xlim(-0.02, 1.02)
            ax.set_ylim(-0.012, 0.112)
            ax.set_xticks([])
            ax.set_yticks([])
            if r == 0:
                ax.set_title(f'{label}', fontsize=9)
            if j == 0:
                ax.set_ylabel(rows[r][1])
        # Record extrema and pressure-max location from the recorded fields.
        pfield = f['p'][ti]
        ext = pressure_extrema(pfield, f['x'], f['y'])
        umag = f['u_mag'][ti]
        iu = int(np.argmax(umag))
        csv_rows.append(dict(
            case=case, label=label, fabric_angle_deg=(angle if angle is not None else ''),
            time=t_common, p_min=ext['p_min'], p_max=ext['p_max'],
            p_max_x=ext['p_max_x'], p_max_y=ext['p_max_y'],
            u_mag_min=float(umag.min()), u_mag_max=float(umag.max()),
            u_mag_max_x=float(f['x'][iu]), u_mag_max_y=float(f['y'][iu])))

    manifest.csv('fe_fabric_contours', csv_rows)
    caption = ('Refined (40 x 8) coupled consolidation contours at the common '
               'recorded time t = %.6g. Top row: pore pressure. Bottom row: '
               'displacement magnitude. Columns: isotropic (uncoupled) fabric, '
               'then fabric axis 0, 45 and 90 deg behind an isotropic, unrotated '
               'mineral. The orange arrow marks the fabric axis; the isotropic '
               'column carries no arrow because its distention stiffness has no '
               'directional coupling. Equal aspect preserves the 1 x 0.1 domain. '
               'These are finite-load demonstrations on synthetic parameters, '
               'not a mesh-convergence study.' % t_common)
    manifest.save(fig, 'fe_fabric_contours', caption,
                  [c for c, _, _ in CASES], ['fe_fabric_contours.csv'])


def diffusion_figure(fields, out_dir, manifest):
    iso = fields['fabric_contour_iso']
    coup = fields[DIFFUSION_COUPLED]
    times = [iso['t'][i] for i in DIFFUSION_TIME_IDX]

    # Common colour scale across both rows and all times (honest contrast).
    vmax = max(float(iso['p'].max()), float(coup['p'].max()))
    levels = np.linspace(0.0, vmax, 21)

    rows = [('fabric_contour_iso', 'isotropic', iso),
            (DIFFUSION_COUPLED, 'coupled, $45^\\circ$', coup)]
    fig, axes = plt.subplots(2, len(DIFFUSION_TIME_IDX), figsize=(13.0, 3.6),
                             layout='constrained')
    csv_rows = []
    for r, (case, label, f) in enumerate(rows):
        for c, ti in enumerate(DIFFUSION_TIME_IDX):
            ax = axes[r][c]
            field = f['p'][ti]
            cf = ax.tricontourf(f['x'], f['y'], field, levels=levels, cmap='viridis')
            ax.set_aspect('equal')
            outline(ax)
            ax.set_xlim(-0.02, 1.02)
            ax.set_ylim(-0.012, 0.112)
            ax.set_xticks([])
            ax.set_yticks([])
            if r == 0:
                ax.set_title(f'$t={times[c]:.4g}$', fontsize=9)
            if c == 0:
                ax.set_ylabel(label)
            ext = pressure_extrema(field, f['x'], f['y'])
            csv_rows.append(dict(
                case=case, label=label,
                fabric_angle_deg=('' if case == 'fabric_contour_iso' else '45'),
                time=float(times[c]), p_min=ext['p_min'], p_max=ext['p_max'],
                p_max_x=ext['p_max_x'], p_max_y=ext['p_max_y']))
    # Shared colourbar spanning the grid.
    fig.colorbar(cf, ax=axes.ravel().tolist(), fraction=0.025, pad=0.01,
                 label='pore pressure $p$')

    manifest.csv('fe_fabric_diffusion', csv_rows)
    caption = ('Refined (40 x 8) coupled consolidation: pore-pressure snapshots at '
               'six recorded times, isotropic (uncoupled) row above and coupled '
               '$45^\\circ$ fabric row below on a shared colour scale. The drainage '
               'front starts at the drained right edge and propagates into the '
               'strip; the interior pressure is a genuine diffusion field, not a '
               'uniform or degenerate state. Equal aspect preserves the 1 x 0.1 '
               'domain. These are finite-load demonstrations on synthetic '
               'parameters, not a mesh-convergence study.')
    manifest.save(fig, 'fe_fabric_diffusion', caption,
                  ['fabric_contour_iso', DIFFUSION_COUPLED], ['fe_fabric_diffusion.csv'])


class Manifest:
    def __init__(self, output):
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=True)
        self.inputs, self.outputs, self.figures = {}, {}, []
        self.source(ROOT / 'examples/plot_fabric_contours.py')

    def source(self, path):
        path = Path(path).resolve()
        actual = sha(path)
        key = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else path.name
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
        files = []
        for ext in ('pdf', 'png'):
            path = self.output / (name + '.' + ext)
            fig.savefig(path, dpi=220,
                        metadata={'Creator': 'plot_fabric_contours.py',
                                  'CreationDate': None, 'ModDate': None})
            files.append(path.name)
            self.outputs[path.name] = sha(path)
        plt.close(fig)
        self.figures.append(dict(id=name, files=files, caption=caption,
                                 cases=list(cases), data=list(data)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs', type=Path, default=DEFAULT_RUNS)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    manifest = Manifest(args.output)
    fields = {}
    for case, _, _ in CASES:
        fields[case] = load_exodus(case, args.runs)
        manifest.source(args.runs / case / 'solution.e')

    contours_figure(fields, args.output, manifest)
    diffusion_figure(fields, args.output, manifest)

    report = dict(
        schema_version=1,
        generator='examples/plot_fabric_contours.py',
        versions=dict(python=platform.python_version(), numpy=np.__version__,
                      matplotlib=matplotlib.__version__, netCDF4=netCDF4.__version__),
        figures=manifest.figures,
        input_sha256=manifest.inputs,
        output_sha256=manifest.outputs,
        limitations=[
            'Fields are read from the recorded Exodus files only; no time interpolation.',
            'The refined runs are finite-load demonstrations on synthetic parameters, not a mesh-convergence study.',
            'The displacement magnitude is evaluated at the recorded nodal positions from ux and uy.',
            'Physical validation has not been performed.',
        ])
    (args.output / 'fe_fabric_contours-plot-manifest.json').write_text(
        json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(figures=len(manifest.figures),
                          files=sorted(manifest.outputs)), indent=2))


if __name__ == '__main__':
    main()
