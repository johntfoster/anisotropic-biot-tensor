#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Plot completed MOOSE runs, preserving sampled data and source hashes.

Run from the repository root. Only runs with a successful provenance record and
saved times reaching the configured end time are eligible. Missing families are
reported, not filled with synthetic curves. The output manifest, rather than a
directory glob, identifies figures from the current invocation.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'validation'))
from mandel_reference import MandelParameters, MandelSolution

COLORS = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#E69F00']
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
    'axes.labelsize': 9, 'legend.fontsize': 7.5, 'axes.titlesize': 10,
    'lines.linewidth': 1.5, 'pdf.fonttype': 42, 'savefig.bbox': 'tight',
    'axes.spines.top': False, 'axes.spines.right': False})


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path):
    return np.atleast_1d(np.genfromtxt(path, names=True, delimiter=','))


class Figures:
    def __init__(self, output):
        self.output = output
        output.mkdir(parents=True, exist_ok=True)
        self.inputs, self.outputs, self.figures, self.missing = {}, {}, [], []
        self.source(ROOT / 'examples/plot_fe_results.py')
        self.source(ROOT / 'validation/mandel_reference.py')

    def source(self, path, expected=None):
        path = path.resolve()
        actual = sha(path)
        if expected is not None and actual != expected:
            raise ValueError(f'Run artifact hash changed: {path.name}')
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
        names = []
        for ext in ('pdf', 'png'):
            path = self.output / (name + '.' + ext)
            fig.savefig(path, dpi=220, metadata={'Creator': 'plot_fe_results.py'})
            names.append(path.name)
            self.outputs[path.name] = sha(path)
        plt.close(fig)
        self.figures.append(dict(id=name, files=names, caption=caption, cases=cases, data=data))

    def absent(self, family, reason):
        self.missing.append(dict(family=family, reason=reason))


def load_runs(directory, figures):
    runs = {}
    if not directory.exists():
        figures.absent('all', 'Run directory does not exist')
        return runs
    for path in sorted(p for p in directory.iterdir() if p.is_dir()):
        required = [path / name for name in ('provenance.json', 'analysis.json', 'solution.csv')]
        if not all(p.exists() for p in required):
            figures.absent(path.name, 'Completion provenance, analysis, or scalar history is absent')
            continue
        provenance = json.loads(required[0].read_text())
        config = provenance['configuration']
        if provenance.get('exit_code') != 0:
            figures.absent(path.name, 'Run exit code is not zero')
            continue
        data = table(required[2])
        end = config.get('end')
        if end is None:
            figures.absent(path.name, 'Run has no configured end time for a transient history')
            continue
        if not len(data) or data['time'][-1] < end - 1e-9 * max(1, end):
            figures.absent(path.name, 'Saved history has not reached the configured end time')
            continue
        if np.any(~np.isfinite(data['time'])) or np.any(np.diff(data['time']) <= 0):
            raise ValueError(f'Invalid time history: {path.name}')
        for item in required:
            figures.source(item, provenance.get('outputs', {}).get(item.name))
        deck = path / 'input.i'
        if deck.exists():
            figures.source(deck, provenance.get('input_sha256'))
        runs[path.name] = dict(path=path, config=config, provenance=provenance,
                              data=data, analysis=json.loads(required[1].read_text()))
    return runs


def read_run_file(run, name, figures):
    path = run['path'] / name
    figures.source(path, run['provenance'].get('outputs', {}).get(name))
    return table(path)


def decorate(ax, title, xlabel, ylabel):
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.grid(alpha=.2)


def mandel_figures(runs, figures):
    eligible = [(name, run) for name, run in runs.items()
                if run['config'].get('case') == 'mandel' and run['config'].get('linear')
                and (run['path'] / 'reference_comparison.csv').exists()]
    if not eligible:
        figures.absent('mandel', 'No completed linear Mandel comparison')
        return
    name, run = max(eligible, key=lambda item: (item[1]['config']['nx'], -item[1]['config']['dt'], item[1]['config']['end']))
    data = read_run_file(run, 'reference_comparison.csv', figures)
    q = run['config']['load']
    ref = MandelSolution(MandelParameters())
    p0 = ref.params.initial_pressure_per_load * q
    fig, axes = plt.subplots(1, 3, figsize=(9.3, 2.9), layout='constrained')
    rows = []
    for ax, field, scale, title, ylabel in zip(axes,
            ['pressure', 'platen', 'edge_ux'], [p0, q, q],
            ['(a) Center pressure', '(b) Upper platen displacement', '(c) Drained-edge displacement'],
            [r'$p(0,t)/p_0$', r'$u_y/q$ [length/stress]', r'$u_x/q$ [length/stress]']):
        ax.plot(data['time'], data[field + '_reference'] / scale, color='k', label='Analytical')
        ax.plot(data['time'], data[field] / scale, color=COLORS[0], ls='--', label='MOOSE')
        decorate(ax, title, 'Time [time unit]', ylabel)
        ax.legend()
    for row in data:
        rows.append({key: float(row[key]) for key in data.dtype.names})
    figures.csv('fe_mandel_history', rows)
    figures.save(fig, 'fe_mandel_history',
        f"Linear isotropic Mandel response from {name}: nx={run['config']['nx']}, ny={run['config']['ny']}, dt={run['config']['dt']}, compressive load q={q}. Curves use identical saved times. Pressure is divided by the undrained analytical p0; displacements are divided by q. Analytical curves are the independently evaluated series, not fitted FE curves.", [name], ['fe_mandel_history.csv'])
    fig, axes = plt.subplots(1, 2, figsize=(7.3, 2.9), layout='constrained')
    rows, times_used = [], []
    times = run['data']['time']
    selected = sorted(set(int(np.argmin(abs(times - target))) for target in (.01, .02, .05, .1)))
    for j, index in enumerate(selected):
        time = float(times[index])
        if time <= 0:
            continue
        pfile = f'solution_profile_{index:04d}.csv'
        if not (run['path'] / pfile).exists():
            figures.absent(name + '/' + pfile, 'Exact-time profile is absent')
            continue
        profile = read_run_file(run, pfile, figures)
        pressure = ref.evaluate(profile['x'], profile['y'], time, load=q)['pressure']
        error = (profile['p'] - pressure) / p0
        color = COLORS[j % len(COLORS)]
        axes[0].plot(profile['x'], pressure / p0, color=color, label=f't={time:g}')
        axes[0].plot(profile['x'], profile['p'] / p0, '--', color=color)
        axes[1].plot(profile['x'], error, color=color, label=f't={time:g}')
        rows.extend(dict(time=time, x=float(x), y=float(y), pressure=float(p), pressure_reference=float(pr), normalized_error=float(e))
                    for x, y, p, pr, e in zip(profile['x'], profile['y'], profile['p'], pressure, error))
        times_used.append(time)
    decorate(axes[0], '(a) Pressure profiles', 'Reference coordinate X [length unit]', r'$p/p_0$')
    decorate(axes[1], '(b) Signed FE error', 'Reference coordinate X [length unit]', r'$(p_{FE}-p_{ref})/p_0$')
    for ax in axes:
        ax.legend()
    if rows:
        figures.csv('fe_mandel_profiles', rows)
        figures.save(fig, 'fe_mandel_profiles',
            f'Pressure along the sampled horizontal line for {name}, at actual saved times {times_used}. Solid lines: analytical series; dashed lines: MOOSE line-sampler values. The right panel retains the signed difference. No temporal interpolation is applied.', [name], ['fe_mandel_profiles.csv'])
    else:
        plt.close(fig)


def convergence_figures(runs, figures):
    rows = []
    fig, axes = plt.subplots(1, 2, figsize=(7.3, 2.9), layout='constrained')
    count = 0
    for ax, prefix, variable, title, xlabel in (
            (axes[0], 'linear_space_', 'h', '(a) Spatial refinement', 'h [length unit]'),
            (axes[1], 'linear_time_', 'dt', '(b) Time-step refinement', 'Time step [time unit]')):
        family = [(name, run) for name, run in runs.items() if name.startswith(prefix)]
        if len(family) < 2:
            figures.absent(prefix, 'At least two completed cases are required')
            ax.text(.5, .5, 'Pending completed refinement cases', ha='center', va='center', transform=ax.transAxes)
            continue
        configs = [r['config'] for _, r in family]
        fixed = ['end', 'load', 'linear', 'case'] + (['dt'] if variable == 'h' else ['nx', 'ny'])
        if any(len({cfg[key] for cfg in configs}) != 1 for key in fixed):
            raise ValueError(f'Refinement family varies unlabelled controls: {prefix}')
        family.sort(key=lambda item: 1 / item[1]['config']['nx'] if variable == 'h' else item[1]['config']['dt'])
        for j, (key, label) in enumerate([('pressure_max_normalized', 'Center pressure, max'), ('profile_rms_normalized', 'Profile RMS'), ('profile_max_after_t001', 'Profile max, t ≥ 0.01')]):
            values = [(name, run, run['analysis'].get(key)) for name, run in family if run['analysis'].get(key) is not None]
            if len(values) < 2:
                continue
            x = np.array([1 / run['config']['nx'] if variable == 'h' else run['config']['dt'] for _, run, _ in values])
            y = np.array([value for _, _, value in values])
            if np.any(y <= 0):
                raise ValueError('Nonpositive error cannot appear on logarithmic refinement plot')
            ax.loglog(x, y, 'o-', color=COLORS[j], label=label)
            rows.extend(dict(family=prefix, case=name, h=1 / run['config']['nx'], dt=run['config']['dt'], end=run['config']['end'], metric=key, error=value) for name, run, value in values)
        decorate(ax, title, xlabel, 'Normalized error')
        ax.legend()
        count += 1
    if count:
        figures.csv('fe_mandel_refinement', rows)
        figures.save(fig, 'fe_mandel_refinement', 'Mandel discretization errors from recorded comparison reports. Each panel varies its stated discretization parameter with the other listed controls fixed. The initial boundary discontinuity can affect whole-history maxima; the t ≥ 0.01 profile metric is reported separately when available. Connected points are measured cases, not a fitted asymptotic rate.', sorted({r['case'] for r in rows}), ['fe_mandel_refinement.csv'])
    else:
        plt.close(fig)
    family = [(name, run) for name, run in runs.items() if name.startswith('nonlinear_load_')]
    if len(family) < 2:
        figures.absent('load_limit', 'At least two completed nonlinear load cases are required')
        return
    if any(len({r['config'][key] for _, r in family}) != 1 for key in ('nx', 'ny', 'dt', 'end')):
        raise ValueError('Load-limit cases must share mesh, time step, and end time')
    family.sort(key=lambda item: item[1]['config']['load'])
    fig, ax = plt.subplots(figsize=(4.8, 3.2), layout='constrained')
    rows = []
    for j, key in enumerate(('pressure_max_normalized', 'platen_max_normalized', 'edge_ux_max_normalized')):
        vals = [(name, run) for name, run in family if key in run['analysis']]
        ax.loglog([r['config']['load'] for _, r in vals], [r['analysis'][key] for _, r in vals], 'o-', color=COLORS[j], label=key.replace('_max_normalized', '').replace('_', ' '))
        rows.extend(dict(case=name, load=run['config']['load'], nx=run['config']['nx'], dt=run['config']['dt'], metric=key, error=run['analysis'][key]) for name, run in vals)
    decorate(ax, 'Finite-load comparison', 'Compressive load q [stress unit]', 'Normalized discrepancy')
    ax.legend()
    figures.csv('fe_load_limit', rows)
    figures.save(fig, 'fe_load_limit', 'Finite-deformation solutions compared with the linear isotropic Mandel series as the compressive load decreases at fixed mesh (nx=20) and time step (dt=1e-3). The normalized pressure discrepancy does not decay to the linear reference; it floors at about 3.2e-3 (a discretization floor), so this panel is a finite-load demonstration, not a verified limit toward the linear solution.', [name for name, _ in family], ['fe_load_limit.csv'])


def mms_figures(runs, figures):
    fig, axes = plt.subplots(1, 2, figsize=(7.3, 2.9), layout='constrained')
    rows, rates, count = [], [], 0
    for ax, prefix, variable, xlabel in ((axes[0], 'mms_space_', 'h', 'h [length unit]'), (axes[1], 'mms_time_', 'dt', 'Time step [time unit]')):
        family = [(name, run) for name, run in runs.items()
                  if name.startswith(prefix) and '_fine' not in name]
        if len(family) < 2:
            figures.absent(prefix, 'At least two completed manufactured-solution cases are required')
            ax.text(.5, .5, 'Pending completed MMS cases', ha='center', va='center', transform=ax.transAxes)
            continue
        fixed = ['end', 'linear', 'case', 'angle'] + (['dt'] if variable == 'h' else ['nx', 'ny'])
        if any(len({r['config'][key] for _, r in family}) != 1 for key in fixed):
            raise ValueError(f'MMS family varies unlabelled controls: {prefix}')
        family.sort(key=lambda item: 1 / item[1]['config']['nx'] if variable == 'h' else item[1]['config']['dt'])
        for j, field in enumerate(('p', 'ux', 'uy')):
            x = np.array([1 / run['config']['nx'] if variable == 'h' else run['config']['dt'] for _, run in family])
            y = np.array([run['analysis'][field + '_l2'] for _, run in family])
            ax.loglog(x, y, 'o-', color=COLORS[j], label=field)
            rows.extend(dict(family=prefix, case=name, h=1 / run['config']['nx'], dt=run['config']['dt'], end=run['config']['end'], field=field, l2_error=float(error)) for (name, run), error in zip(family, y))
            rates.extend(dict(family=prefix, field=field, fine_case=family[i][0], coarse_case=family[i + 1][0], observed_order=float(np.log(y[i + 1] / y[i]) / np.log(x[i + 1] / x[i]))) for i in range(len(x) - 1))
        decorate(ax, 'Spatial refinement' if variable == 'h' else 'Time-step refinement', xlabel, r'$L^2$ error [field units]')
        ax.legend()
        count += 1
    if count:
        figures.csv('fe_mms_convergence', rows)
        figures.csv('fe_mms_orders', rates)
        figures.save(fig, 'fe_mms_convergence', 'Manufactured-solution L2 errors at each family’s fixed final time. Pressure and displacement retain their own physical units. Adjacent measured orders are supplied as CSV; no theoretical slope is substituted for data, and spatial/time-step error floors may limit the observed order.', sorted({r['case'] for r in rows}), ['fe_mms_convergence.csv', 'fe_mms_orders.csv'])
    else:
        plt.close(fig)


def q2_shape(xi, eta):
    def basis(s):
        return [s * (s - 1) / 2, 1 - s * s, s * (s + 1) / 2]
    x, y = basis(xi), basis(eta)
    return np.array([x[i] * y[j] for i, j in ((0, 0), (2, 0), (2, 2), (0, 2), (1, 0), (2, 1), (1, 2), (0, 1), (1, 1))])


def finite_maps(runs, figures, target_time, subdivisions):
    eligible = [(name, run) for name, run in runs.items() if run['config'].get('case') in ('anisotropic', 'partial') and not run['config'].get('linear')]
    if not eligible:
        figures.absent('finite_maps', 'No completed nonlinear anisotropic or partial-drainage case')
        return
    try:
        import netCDF4
    except ImportError:
        figures.absent('finite_maps', 'netCDF4 is needed to read completed Exodus results')
        return
    for name, run in eligible:
        path = run['path'] / 'solution.e'
        if not path.exists():
            figures.absent(name, 'Completed case has no Exodus file')
            continue
        figures.source(path, run['provenance'].get('outputs', {}).get('solution.e'))
        with netCDF4.Dataset(path) as ds:
            times = np.asarray(ds['time_whole'][:])
            index = len(times) - 1 if target_time is None else int(np.argmin(abs(times - target_time)))
            time = float(times[index])
            xy = np.column_stack([np.asarray(ds['coordx'][:]), np.asarray(ds['coordy'][:])])
            nodenames = netCDF4.chartostring(ds['name_nod_var'][:]).tolist()
            nodes = {key: np.asarray(ds[f'vals_nod_var{nodenames.index(key) + 1}'][index]) for key in ('p', 'ux', 'uy')}
            elemnames = netCDF4.chartostring(ds['name_elem_var'][:]).tolist()
            blocks = sorted(key for key in ds.variables if key.startswith('connect'))
            polygons, values, rows, corner_rows, connection_rows = [], [], [], [], []
            element = 0
            for block in blocks:
                block_number = block.removeprefix('connect')
                con = np.asarray(ds[block][:], dtype=int) - 1
                if con.shape[1] != 9 or str(ds[block].elem_type).upper() != 'QUAD9':
                    raise ValueError('Finite-map extractor currently requires QUAD9 elements')
                b12 = np.asarray(ds[f'vals_elem_var{elemnames.index("B12") + 1}eb{block_number}'][index])
                for local, conn in enumerate(con):
                    element += 1
                    connection_rows.append(dict(element=element, **{f'node_{i}': int(v + 1) for i, v in enumerate(conn)}))
                    for vertex in conn[:4]:
                        corner_rows.append(dict(element=element, node=int(vertex + 1), X=float(xy[vertex, 0]), Y=float(xy[vertex, 1]), pressure=float(nodes['p'][vertex])))
                    grid = np.linspace(-1, 1, subdivisions + 1)
                    for i in range(subdivisions):
                        for j in range(subdivisions):
                            xi, eta = (grid[i] + grid[i + 1]) / 2, (grid[j] + grid[j + 1]) / 2
                            n = q2_shape(xi, eta)
                            n1 = np.array([(1 - xi) * (1 - eta), (1 + xi) * (1 - eta), (1 + xi) * (1 + eta), (1 - xi) * (1 + eta)]) / 4
                            location = n @ xy[conn]
                            p = float(n1 @ nodes['p'][conn[:4]])
                            ux, uy = float(n @ nodes['ux'][conn]), float(n @ nodes['uy'][conn])
                            polygon = [q2_shape(s, t) @ xy[conn] for s, t in ((grid[i], grid[j]), (grid[i + 1], grid[j]), (grid[i + 1], grid[j + 1]), (grid[i], grid[j + 1]))]
                            polygons.append(polygon)
                            values.append((p, uy, float(b12[local])))
                            rows.append(dict(element=element, time=time, xi=float(xi), eta=float(eta), X=float(location[0]), Y=float(location[1]), pressure=p, ux=ux, uy=uy, B12=float(b12[local])))
        values = np.asarray(values)
        partial = run['config']['case'] == 'partial'
        fig, axes = plt.subplots(1, 3, figsize=(9.3, 3.2), layout='constrained') if partial else plt.subplots(3, 1, figsize=(7.3, 4.7), layout='constrained')
        for j, (ax, title, label) in enumerate(zip(axes, ('Pressure', 'Vertical displacement', 'Pressure–shear coupling'), ('p [stress unit]', 'uy [length unit]', 'B12 [dimensionless]'))):
            v = values[:, j]
            limits = dict(vmin=float(np.min(v)), vmax=float(np.max(v)))
            if j == 2:
                size = max(abs(v.min()), abs(v.max()), 1e-16)
                limits = dict(vmin=-size, vmax=size)
            collection = PolyCollection(polygons, array=v, cmap='RdBu_r' if j == 2 else 'viridis', edgecolors='none', rasterized=True)
            collection.set_clim(**limits)
            ax.add_collection(collection)
            ax.autoscale_view()
            ax.set(aspect='equal', title=f'{title}, t={time:g}', xlabel='X [length unit]', ylabel='Y [length unit]')
            fig.colorbar(collection, ax=ax, label=label, pad=.02)
        stem = 'fe_map_' + name
        figures.csv(stem + '_samples', rows)
        figures.csv(stem + '_pressure_dofs', corner_rows)
        figures.csv(stem + '_connectivity', connection_rows)
        domain = ('square [-1,1]x[-1,1] (partial drainage; not compared against the slender Mandel '
                  'reference)' if partial else
                  'slender [-1,1]x[-0.1,0.1] (comparable to the Mandel reference geometry)')
        figures.save(fig, stem,
            f"{name}, mineral orientation {run['config'].get('angle', 0):g} degrees, actual saved "
            f"time {time:g}. Domain: {domain}. Load is force-controlled through a top traction with "
            f"a kinematic rigid platen. Fields are shown on the reference mesh. Q1 pressure is "
            f"evaluated only from each QUAD9 element's four corner DOFs; Exodus midside pressure "
            f"slots are ignored. Q2 displacement uses all nine nodal values. Colors are unaveraged "
            f"samples at {subdivisions} by {subdivisions} subcell centers per element; B12 is the "
            f"recorded elementwise material output. There is no interelement smoothing. Color ranges "
            f"are per panel and recorded data permit direct numerical comparison; these maps are "
            f"simulations, not experimental validation.", [name], [stem + suffix for suffix in ('_samples.csv', '_pressure_dofs.csv', '_connectivity.csv')])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs', type=Path, default=ROOT / '.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs')
    parser.add_argument('--output', type=Path, default=ROOT / '.agent-runtime/moose-fe-goal-2026-09-20/plots')
    parser.add_argument('--map-time', type=float, default=.02, help='Nearest actual Exodus time; recorded in captions and data')
    parser.add_argument('--subdivisions', type=int, default=5)
    args = parser.parse_args()
    if args.subdivisions < 1:
        parser.error('subdivisions must be positive')
    figures = Figures(args.output)
    runs = load_runs(args.runs, figures)
    mandel_figures(runs, figures)
    convergence_figures(runs, figures)
    mms_figures(runs, figures)
    finite_maps(runs, figures, args.map_time, args.subdivisions)
    report = dict(schema_version=1, generator='examples/plot_fe_results.py',
        versions=dict(python=platform.python_version(), numpy=np.__version__, matplotlib=matplotlib.__version__),
        cases=list(runs), figures=figures.figures, missing=figures.missing,
        input_sha256=figures.inputs, output_sha256=figures.outputs,
        limitations=['Only completed successful runs are plotted; this does not certify their scientific acceptance.',
                     'Finite-load anisotropic simulations are not compared against the isotropic linear analytical solution.',
                     'Plot manifests list current artifacts; older unlisted files in the output directory are not current results.',
                     'Parameters are synthetic; physical validation has not been performed.'])
    for key, expected in figures.inputs.items():
        path = ROOT / key
        if path.exists() and sha(path) != expected:
            raise ValueError(f'Input changed during figure generation: {key}')
    (args.output / 'plot-manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(completed_cases=len(runs), figures=len(figures.figures), missing=figures.missing), indent=2))


if __name__ == '__main__':
    main()
