#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Plot the recorded pore-fabric contour fields from the refined (40 x 4) runs.

Reads only the recorded Exodus field files under ``fe-evidence/runs`` (netCDF4)
and emits two figures plus CSV sidecars:

``fe_fabric_contours``
    Pore pressure ``p`` and displacement magnitude ``|u|`` at one common time,
    one column per fabric variant (isotropic, axis 0/45/90 deg), as filled
    contours with shared colourbars, displaced boundaries, and a fabric-axis
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

from figure_style import COLORS, apply_style, publication_size
apply_style()


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


# One displacement multiplier for every case and time in both figures.
DISPLACEMENT_SCALE = 500.0


def geometry(f, ti):
    return (f['x'] + DISPLACEMENT_SCALE * f['ux'][ti],
            f['y'] + DISPLACEMENT_SCALE * f['uy'][ti])


def panel(ax, f, ti, key, levels, angle=None):
    x, y = geometry(f, ti)
    cf = ax.tricontourf(x, y, f[key][ti], levels=levels, cmap='viridis')
    cf.set_zorder(-1)
    ax.set_rasterization_zorder(0)
    # Draw each boundary in reference-coordinate order, then displace its nodes.
    for coordinate, value, order in [('x', 0., 'y'), ('x', 1., 'y'),
                                     ('y', 0., 'x'), ('y', .1, 'x')]:
        indices = np.flatnonzero(np.isclose(f[coordinate], value))
        indices = indices[np.argsort(f[order][indices])]
        ax.plot(x[indices], y[indices], color='k', lw=.65)
    ax.plot([0, 1, 1, 0, 0], [0, 0, .1, .1, 0], '--', color='.55', lw=.6)
    if angle is not None:
        # The arrow denotes the reference fabric, in axes coordinates so its
        # direction is not distorted by the enlarged vertical display scale.
        th = np.radians(angle)
        dx, dy = .12*np.cos(th), .12*np.sin(th)/.38
        ax.annotate('', xy=(.5+dx, .5+dy), xytext=(.5-dx, .5-dy),
                    xycoords='axes fraction',
                    arrowprops=dict(arrowstyle='-|>', color='#D55E00', lw=1.1))
    ax.set_xlim(-.035, 1.045)
    ax.set_ylim(-.01, .11)
    ax.set_box_aspect(.38)
    ax.set_xticks([0, .5, 1])
    ax.set_yticks([0, .1])
    return cf


def contours_figure(fields, out_dir, manifest):
    ti = len(fields['fabric_contour_iso']['t']) - 1
    t_common = float(fields['fabric_contour_iso']['t'][ti])
    fig, axes = plt.subplots(2, 4, figsize=(6.35, 2.77), layout='constrained')
    rows = [('p', r'pore pressure $p$'), ('u_mag', r'displacement $|\mathbf{u}|$')]
    csv_rows = []
    for r, (key, label) in enumerate(rows):
        minimum = min(float(f[key][ti].min()) for f in fields.values())
        maximum = max(float(f[key][ti].max()) for f in fields.values())
        levels = np.linspace(minimum, maximum, 91)
        for j, (case, title, angle) in enumerate(CASES):
            cf = panel(axes[r,j], fields[case], ti, key, levels, angle)
            if r == 0:
                axes[r,j].set_title(title)
            if j:
                axes[r,j].set_yticklabels([])
        cb = fig.colorbar(cf, ax=list(axes[r]), fraction=.025, pad=.025, shrink=.55,
                         format='%.1e', label=label)
        cb.set_ticks(np.linspace(max(0., minimum), maximum, 3))
    for case, label, angle in CASES:
        f = fields[case]
        ext = pressure_extrema(f['p'][ti], f['x'], f['y'])
        umag = f['u_mag'][ti]
        iu = int(np.argmax(umag))
        csv_rows.append(dict(case=case, label=label,
            fabric_angle_deg=angle if angle is not None else '', time=t_common,
            **ext, u_mag_min=float(umag.min()), u_mag_max=float(umag.max()),
            u_mag_max_x=float(f['x'][iu]), u_mag_max_y=float(f['y'][iu])))
    fig.supxlabel(r'$X_1+500u_1$')
    fig.supylabel(r'$X_2+500u_2$')
    manifest.csv('fe_fabric_contours', csv_rows)
    caption = ('Coupled consolidation on the 40 x 4 mesh of the 1 x 0.1 domain '
               f'at t = {t_common:g}. Pressure above, displacement magnitude below; '
               'one colour scale and colourbar per quantity across all cases. '
               'Displacements are magnified 500 times, with dashed reference '
               'boundaries; the panel aspect ratio is 0.38. Orange arrows denote '
               'reference fabric directions. These are finite-load demonstrations '
               'on synthetic parameters, not a mesh-convergence study.')
    manifest.save(fig, 'fe_fabric_contours', caption,
                  [c for c, _, _ in CASES], ['fe_fabric_contours.csv'])


def diffusion_figure(fields, out_dir, manifest):
    iso = fields['fabric_contour_iso']
    selected = [fields['fabric_contour_iso'], fields[DIFFUSION_COUPLED]]
    minimum = min(float(f['p'][DIFFUSION_TIME_IDX].min()) for f in selected)
    maximum = max(float(f['p'][DIFFUSION_TIME_IDX].max()) for f in selected)
    levels = np.linspace(minimum, maximum, 91)
    fig, axes = plt.subplots(4, 3, figsize=(6.35, 5.6), layout='constrained')
    csv_rows = []
    for group, (case, label, f) in enumerate([
            ('fabric_contour_iso', 'isotropic', iso),
            (DIFFUSION_COUPLED, r'fabric $45^\circ$', selected[1])]):
        for c, ti in enumerate(DIFFUSION_TIME_IDX):
            ax = axes[2*group+c//3, c%3]
            cf = panel(ax, f, ti, 'p', levels)
            ax.set_title(f'{label}, $t={f["t"][ti]:.4g}$')
            if c%3:
                ax.set_yticklabels([])
            ext = pressure_extrema(f['p'][ti], f['x'], f['y'])
            csv_rows.append(dict(case=case, label=label,
                fabric_angle_deg='' if group == 0 else '45',
                time=float(f['t'][ti]), **ext))
    cb = fig.colorbar(cf, ax=axes.ravel().tolist(), fraction=.025, pad=.025,
                     label='pore pressure $p$', format='%.1e')
    cb.set_ticks(np.linspace(max(0., minimum), maximum, 5))
    fig.supxlabel(r'$X_1+500u_1$')
    fig.supylabel(r'$X_2+500u_2$')
    manifest.csv('fe_fabric_diffusion', csv_rows)
    caption = ('Coupled consolidation on the 40 x 4 mesh of the 1 x 0.1 domain: '
               'six recorded pressure snapshots for isotropic fabric (upper two '
               'rows) and coupled 45-degree fabric (lower two rows). All panes '
               'share one colour scale and colourbar. Displacements are magnified '
               '500 times, with dashed reference boundaries and panel aspect 0.38. '
               'These are finite-load demonstrations on synthetic parameters, '
               'not a mesh-convergence study.')
    manifest.save(fig, 'fe_fabric_diffusion', caption,
                  ['fabric_contour_iso', DIFFUSION_COUPLED], ['fe_fabric_diffusion.csv'])


class Manifest:
    def __init__(self, output):
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=True)
        self.inputs, self.outputs, self.figures = {}, {}, []
        self.source(ROOT / 'examples/plot_fabric_contours.py')
        self.source(ROOT / 'examples/figure_style.py')

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
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
        self.outputs[path.name] = sha(path)

    def save(self, fig, name, caption, cases, data):
        publication_size(fig)
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

    reference = fields['fabric_contour_iso']
    for case, f in fields.items():
        if not np.array_equal(f['t'], reference['t']):
            raise ValueError('Recorded times differ: ' + case)
        if not (np.isclose(f['x'].max(), 1.) and np.isclose(f['y'].max(), .1)):
            raise ValueError('Unexpected domain: ' + case)
        if len(np.unique(f['x'])) != 81 or len(np.unique(f['y'])) != 9:
            raise ValueError('Expected the 40 x 4 QUAD9 mesh: ' + case)
        if not all(np.isfinite(f[key]).all() for key in ('p', 'ux', 'uy')):
            raise ValueError('Nonfinite field: ' + case)
    contours_figure(fields, args.output, manifest)
    diffusion_figure(fields, args.output, manifest)

    report = dict(
        schema_version=1,
        generator='examples/plot_fabric_contours.py',
        versions=dict(python=platform.python_version(), numpy=np.__version__,
                      matplotlib=matplotlib.__version__, netCDF4=netCDF4.__version__),
        figures=manifest.figures,
        display=dict(displacement_scale=DISPLACEMENT_SCALE, panel_aspect=.38,
                     reference_domain=[1., .1], mesh=[40, 4]),
        input_sha256=manifest.inputs,
        output_sha256=manifest.outputs,
        limitations=[
            'Fields are read from the recorded Exodus files only; no time interpolation.',
            'The refined runs are finite-load demonstrations on synthetic parameters, not a mesh-convergence study.',
            'The displacement magnitude is evaluated at the recorded nodal positions from ux and uy.',
            'Physical validation has not been performed.',
            'The recorded Exodus files embed a per-run wall-clock line in their information records, so their raw bytes are not reproducible across runs; the recorded CSV histories and the field arrays are.',
        ])
    (args.output / 'fe_fabric_contours-plot-manifest.json').write_text(
        json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(figures=len(manifest.figures),
                          files=sorted(manifest.outputs)), indent=2))


if __name__ == '__main__':
    main()
