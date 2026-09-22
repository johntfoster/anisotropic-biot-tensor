#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Compare rotated-anisotropy FE results in 2-D.

Reads the recorded Exodus results for the anisotropic consolidation cases and
produces:
  1. a panel of exaggerated deformed configurations coloured by the in-plane
     displacement magnitude, for each mineral orientation;
  2. quantitative curves showing how the orientation changes the surface
     settlement profile, the lateral edge displacement, and the peak pressure.

Every value comes from the recorded runs; nothing is synthesised.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from figure_style import COLORS, apply_style, publication_size
apply_style()
import netCDF4
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / '.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs'
OUT = ROOT / '.agent-runtime/moose-fe-goal-2026-09-20/plots'

CASES = [('anisotropic_0', 0), ('anisotropic_30', 30), ('anisotropic_45', 45), ('anisotropic_90', 90)]


def read_case(run_dir):
    path = run_dir / 'solution.e'
    ds = netCDF4.Dataset(path)
    names = [bytes(x).decode('utf-8', 'ignore').rstrip('\x00').strip() for x in ds.variables['name_nod_var'][:]]
    ntime = len(ds.dimensions['time_step'])
    last = ntime - 1
    vals = {}
    for i, name in enumerate(names, start=1):
        var = ds.variables.get(f'vals_nod_var{i}')
        if var is None:
            continue
        vals[name] = np.array(var[last, :], dtype=float)
    x = np.array(ds.variables['coordx'][:], dtype=float)
    y = np.array(ds.variables['coordy'][:], dtype=float)
    conn = np.array(ds.variables['connect1'][:], dtype=int) - 1
    time = np.array(ds.variables['time_whole'][:], dtype=float)
    ds.close()
    return dict(x=x, y=y, conn=conn, vals=vals, time=time, ntime=ntime, path=path, last=last)


def main():
    scalar = json.loads((ROOT / '.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs/anisotropic_0/provenance.json').read_text())['configuration']
    cases = {}
    for name, angle in CASES:
        d = RUNS / name
        if not (d / 'solution.e').is_file():
            print('missing', name, file=sys.stderr)
            continue
        cases[angle] = read_case(d)

    fig = plt.figure(figsize=(15.5, 8.2))
    gs = fig.add_gridspec(2, 4, hspace=.36, wspace=.34)

    # --- Row 1: deformed configurations, one panel per orientation ---
    for idx, (angle, d) in enumerate(sorted(cases.items())):
        ax = fig.add_subplot(gs[0, idx])
        ux, uy = d['vals']['ux'], d['vals']['uy']
        mag = np.hypot(ux, uy)
        scale = 0.15 / max(mag.max(), 1e-30)
        X, Y = d['x'] + scale * ux, d['y'] + scale * uy
        for row in d['conn']:
            loop = np.r_[row, row[0]]
            ax.plot(X[loop], Y[loop], '-', color='0.55', lw=.35, zorder=1)
        sc = ax.scatter(X, Y, c=mag, s=9, cmap='viridis', zorder=2)
        ax.plot(d['x'][[np.argmin(d['x'])] * 2], [d['y'].min(), d['y'].max()], 'k--', lw=.6, alpha=.4)
        ax.set_aspect('equal')
        ax.set_title(f'mineral orientation $\\theta$ = {angle}$^\\circ$', fontsize=10)
        ax.set_xlabel('$X_1$', fontsize=9)
        if idx == 0:
            ax.set_ylabel('$X_2$', fontsize=9)
        ax.tick_params(labelsize=8)
        plt.colorbar(sc, ax=ax, fraction=.046, pad=.03).set_label('$|\\mathbf{u}|$ (exaggerated $\\times$%.0f)' % (1 / scale if scale else 0), fontsize=8)

    # --- Row 2a: surface settlement (uy along the top edge) ---
    ax = fig.add_subplot(gs[1, 0:2])
    for angle, d in sorted(cases.items()):
        top = np.isclose(d['y'], d['y'].max())
        o = np.argsort(d['x'][top])
        ax.plot(d['x'][top][o], 1e3 * d['vals']['uy'][top][o], marker='o', ms=2.4, lw=1.2,
                label=f'{angle}$^\\circ$')
    ax.set_xlabel('$X_1$', fontsize=9)
    ax.set_ylabel('vertical displacement $u_2$ ($\\times10^{-3}$)', fontsize=9)
    ax.set_title('Top-surface settlement profile', fontsize=10)
    ax.grid(alpha=.25)
    ax.legend(fontsize=8, title='orientation', title_fontsize=8)

    # --- Row 2b: lateral edge displacement and peak pressure vs angle ---
    ax = fig.add_subplot(gs[1, 2])
    angles, edge_ux, peak_p = [], [], []
    for angle, d in sorted(cases.items()):
        right = np.isclose(d['x'], d['x'].max())
        angles.append(angle)
        edge_ux.append(d['vals']['ux'][right].mean())
        peak_p.append(d['vals']['p'].max())
    ax.plot(angles, 1e3 * np.array(edge_ux), 'o-', color=COLORS[0], label='mean $u_1$ on $X_1=+1$')
    ax.set_xlabel('mineral orientation $\\theta$ (degrees)', fontsize=9)
    ax.set_ylabel('$u_1$ ($\\times10^{-3}$)', fontsize=9)
    ax.grid(alpha=.25)
    ax2 = ax.twinx()
    ax2.plot(angles, peak_p, 's--', color=COLORS[1], label='peak $p$')
    ax2.set_ylabel('peak $p$', fontsize=9)
    ax.set_title('Orientation effect on lateral flow-driven deformation', fontsize=10)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=8, loc='best')

    # --- Row 2c: pressure field at the final state ---
    ax = fig.add_subplot(gs[1, 3])
    for angle, d in sorted(cases.items()):
        mid = np.isclose(d['y'], 0.0)
        o = np.argsort(d['x'][mid])
        ax.plot(d['x'][mid][o], 1e3 * d['vals']['p'][mid][o], lw=1.2, marker='.', ms=2,
                label=f'{angle}$^\\circ$')
    ax.set_xlabel('$X_1$', fontsize=9)
    ax.set_ylabel('pressure $p$ ($\\times10^{-3}$)', fontsize=9)
    ax.set_title('Mid-plane pressure, final state', fontsize=10)
    ax.grid(alpha=.25)
    ax.legend(fontsize=8)

    fig.suptitle('Rotated mineral anisotropy in the coupled FE model '
                 f'(load $q$ = {scalar["load"]}, modulus rotation in the $X_1$-$X_2$ plane)',
                 fontsize=11.5)
    OUT.mkdir(parents=True, exist_ok=True)
    publication_size(fig)
    fig.savefig(OUT / 'fe_anisotropy_2d.png', dpi=200, metadata={'Creator': 'plot_anisotropy_2d.py'})
    fig.savefig(OUT / 'fe_anisotropy_2d.pdf', metadata={'Creator': 'plot_anisotropy_2d.py'})

    summary = {}
    for angle, d in sorted(cases.items()):
        right = np.isclose(d['x'], d['x'].max())
        top = np.isclose(d['y'], d['y'].max())
        summary[angle] = dict(
            mean_edge_ux=float(d['vals']['ux'][right].mean()),
            max_abs_ux=float(np.abs(d['vals']['ux']).max()),
            mean_top_uy=float(d['vals']['uy'][top].mean()),
            peak_pressure=float(d['vals']['p'].max()),
            displacement_magnitude_max=float(np.hypot(d['vals']['ux'], d['vals']['uy']).max()),
            final_time=float(d['time'][d['last']]),
        )
    (OUT / 'fe_anisotropy_2d.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
