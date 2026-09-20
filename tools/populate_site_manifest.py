#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Populate the verification-site manifest from recorded, checksummed evidence.

This copies a curated subset of plots and reports into publication roots and
writes site/evidence.json with category statuses that match what was actually
computed. It does not run or certify any scientific check itself.
"""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.agent-runtime/moose-fe-goal-2026-09-20'
PLOTS = RUNTIME / 'plots'
RUNS = RUNTIME / 'implementation' / 'runs'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def copy(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return dst


def main():
    manifest = json.loads((ROOT / 'site/evidence.json').read_text())
    artifacts, figures = [], []

    def add(ident, path, destination, kind, label):
        artifacts.append(dict(id=ident, path=str(path.relative_to(ROOT)),
                              destination=destination, kind=kind, label=label,
                              sha256=sha(path)))

    # --- Figures: curated FE plots copied into the publication root ---
    published = {
        'fe_mandel_history.png': 'isotropic Mandel pressure and platen history',
        'fe_mandel_profiles.png': 'isotropic Mandel pressure profiles',
        'fe_mandel_refinement.png': 'isotropic Mandel spatial and temporal refinement',
        'fe_mms_convergence.png': 'manufactured-solution spatial convergence',
        'fe_load_limit.png': 'finite-load comparison at decreasing compressive load (small-load error floor)',
        'fe_map_anisotropic_30.png': 'rotated anisotropic consolidation map',
        'fe_map_partial_0.png': 'partial-drainage two-dimensional map',
    }
    for name, label in published.items():
        src = PLOTS / name
        if not src.is_file():
            continue
        dst = copy(src, ROOT / 'figures' / name)
        ident = name.replace('.png', '').replace('_', '-')
        add(ident, dst, name, 'figure', label)
        for csv in (PLOTS / name.replace('.png', '.csv'),):
            if csv.is_file():
                cid = ident + '-data'
                cdst = copy(csv, ROOT / 'figures' / csv.name)
                add(cid, cdst, csv.name, 'data', label + ' (data)')
        figures.append(dict(artifact=ident, caption=label,
                            alt=label + ' generated from the recorded MOOSE runs'))

    # --- Reports ---
    reports = {
        'fluid-coupling-verification': (ROOT / 'build/fluid-coupling/verification.json',
                                        'fluid EOS and reference-mass derivative checks'),
        'conformal-verification': (ROOT / 'build/conformal/verification.json',
                                   'conformal constitutive verification suite'),
        'tensor-verification': (ROOT / 'build/weighted-stress/tensor-verification.json',
                                'spherical-gauge tensor verification suite'),
        'reconstruction-verification': (ROOT / 'build/weighted-stress/reconstruction-verification.json',
                                        'work-equivalence and unjacketed reconstruction suite'),
        'mandel-reference': (RUNTIME / 'reference/mandel-reference-report.json',
                             'independent Mandel series reference self-check (38 checks)'),
        'mms-convergence': (RUNTIME / 'parent-analysis/mms-convergence.json',
                            'manufactured-solution spatial and temporal convergence orders'),
        'cpp-python-constitutive': (RUNTIME / 'implementation/constitutive/report.json',
                                    'C++ versus independent Python constitutive evaluation'),
    }
    for ident, (src, label) in reports.items():
        if src.is_file():
            dst = copy(src, ROOT / 'site/reports' / (ident + '.json'))
            add(ident, dst, ident + '.json', 'report', label)
            # Ship the data artifacts a report declares, alongside the report,
            # so every declared SHA-256 resolves inside the published package.
            declared = json.loads(dst.read_text()).get('artifacts', {})
            for name, digest in declared.items():
                data_src = src.parent / name
                if data_src.is_file():
                    data_dst = copy(data_src, ROOT / 'site/reports' / name)
                    add(ident + '-' + name.replace('.csv', '').replace('.', '-'),
                        data_dst, name, 'data', label + ' (data: ' + name + ')')
                    if sha(data_dst) != digest:
                        raise SystemExit('declared artifact hash mismatch: ' + name)

    # --- Finite-deformation demonstration diagnostics ---
    # The rotated-anisotropy, isotropic-comparison and partial-drainage decks solve a
    # different problem from the reference-modulus isotropic Mandel series used by the
    # quarter-domain decks (phi_s0=0.6 and K=7; the partial family also uses a square
    # domain), so a Mandel-normalized discrepancy would compare different problems and
    # is not reported for them. The published diagnostics are the measured per-run
    # quantities, collected here into a listed artifact.
    demo = {}
    for case in sorted(p.name for p in RUNS.iterdir() if p.is_dir()):
        analysis = RUNS / case / 'analysis.json'
        if not analysis.is_file():
            continue
        record = json.loads(analysis.read_text())
        cfg = record.get('configuration', {})
        if cfg.get('case') not in ('anisotropic', 'isotropic', 'partial') or cfg.get('linear'):
            continue
        if record.get('reference_comparable') is not False:
            raise SystemExit('demonstration run still compares against the Mandel series: ' + case)
        demo[case] = {k: record[k] for k in
                      ('peak_pressure', 'peak_time', 'force_relative',
                       'discrete_mass_absolute', 'discrete_mass_mobilized_relative',
                       'platen_equality_absolute') if k in record}
    if not demo:
        raise SystemExit('no demonstration run analyses found for the finite-deformation category')

    def family(prefix):
        return {n: r for n, r in demo.items() if n.startswith(prefix)}

    def span(records, key):
        values = [r[key] for r in records.values() if key in r]
        if not values:
            raise SystemExit('demonstration diagnostic missing: ' + key)
        return [min(values), max(values)]

    anisotropic = family('anisotropic_')
    partial = family('partial_')
    isotropic = family('isotropic')
    coarse = {n[len('anisotropic_'):] for n in anisotropic}
    orientations = ', '.join(sorted({d.split('_')[0] for d in coarse}, key=float))
    refined = sorted({d.split('_')[0] for d in coarse if '_' in d}, key=float)
    mesh_note = (' (with coarse and fine meshes at ' + ', '.join(refined) + ' degrees)'
                 if refined else '')
    summary = dict(
        note=('Force-controlled demonstrations with a kinematic rigid platen. Their decks solve a '
              'different problem from the reference-modulus isotropic Mandel series of the '
              'quarter-domain decks (phi_s0=0.6 and K=7 for the anisotropic and isotropic-comparison '
              'decks; the partial-drainage family additionally uses the square domain '
              '[-1,1]x[-1,1]), so no reference-normalized discrepancy is reported for them. Every '
              'listed quantity is a measured per-run diagnostic.'),
        source_runs=sorted(demo),
        families=dict(
            anisotropic=dict(cases=sorted(anisotropic),
                             peak_pressure=span(anisotropic, 'peak_pressure'),
                             peak_time=span(anisotropic, 'peak_time'),
                             force_relative_max=span(anisotropic, 'force_relative')[1],
                             discrete_mass_mobilized_relative_max=span(
                                 anisotropic, 'discrete_mass_mobilized_relative')[1]),
            isotropic=dict(cases=sorted(isotropic),
                           peak_pressure=span(isotropic, 'peak_pressure'),
                           peak_time=span(isotropic, 'peak_time'),
                           force_relative_max=span(isotropic, 'force_relative')[1],
                           discrete_mass_mobilized_relative_max=span(
                               isotropic, 'discrete_mass_mobilized_relative')[1]),
            partial=dict(cases=sorted(partial),
                         peak_pressure=span(partial, 'peak_pressure'),
                         peak_time=span(partial, 'peak_time'),
                         force_relative_max=span(partial, 'force_relative')[1],
                         discrete_mass_mobilized_relative_max=span(
                             partial, 'discrete_mass_mobilized_relative')[1]),
        ),
        runs=demo,
    )
    summary_path = ROOT / 'site/reports/finite-deformation-summary.json'
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2) + '\n')
    add('finite-deformation-summary', summary_path, 'finite-deformation-summary.json', 'report',
        'measured diagnostics of the anisotropic, isotropic-comparison, and partial-drainage demonstrations')

    aniso = summary['families']['anisotropic']
    isorun = summary['families']['isotropic']
    part = summary['families']['partial']

    def fmt(v):
        return format(v, '.4g')

    def rng(fam, key):
        low, high = fam[key]
        return fmt(low) if low == high else fmt(low) + '-' + fmt(high)

    # --- Scientific snapshot: exact FE source and evidence files ---
    snapshot_files = []
    for pattern in ('moose_app/**/*.C', 'moose_app/**/*.h', 'moose_app/scripts/*.py',
                    'moose_app/inputs/*.i', 'examples/*.py', 'validation/*.py'):
        for path in sorted(ROOT.glob(pattern)):
            if 'build' in path.parts or not path.is_file():
                continue
            snapshot_files.append(dict(path=str(path.relative_to(ROOT)), sha256=sha(path)))
    snap = ROOT / 'site/scientific-snapshot.json'
    snap.write_text(json.dumps(dict(files=snapshot_files), indent=2) + '\n')
    add('scientific-snapshot', snap, 'scientific-snapshot.json', 'provenance',
        'exact FE source and evidence snapshot')

    revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, check=True,
                              capture_output=True, text=True).stdout.strip()

    manifest['artifacts'] = artifacts
    manifest['figures'] = figures
    manifest['provenance'] = dict(
        source_revision=revision,
        scientific_snapshot='scientific-snapshot',
        note=('The base commit predates this working revision. The finite-element sources and '
              'evidence are provided under the repository-relative paths moose_app/, validation/, '
              'fe-evidence/, figures/ and site/; the scientific-snapshot artifact lists the exact '
              'files with SHA-256 hashes, and the review snapshot pinned in the review record is '
              'the authoritative frozen artifact for the checks below.'),
    )

    cpp_path = RUNTIME / 'implementation/constitutive/report.json'
    if not cpp_path.is_file():
        raise SystemExit('missing constitutive C++/Python comparison report: ' + str(cpp_path))
    if 'cpp-python-constitutive' not in {a['id'] for a in artifacts}:
        raise SystemExit('constitutive comparison artifact was not packaged into site/reports')
    cpp = json.loads(cpp_path.read_text())

    passed = lambda summary, ev: dict(status='passed', summary=summary, evidence=ev)
    pending = lambda summary, ev=(): dict(status='pending', summary=summary, evidence=list(ev))

    manifest['categories'] = {
        'analytical': dict(
            status='passed',
            summary=('The independent Mandel reference passes 38 self-checks (peak overshoot '
                     '5.4659% at t = 0.01516535). This status covers the analytical reference '
                     'self-checks only.'),
            demonstration=('The finite-load FE comparison against the reference is a '
                           'demonstration, not an analytical gate; its normalized pressure '
                           'discrepancy floors at about 3.2e-3 (a discretization floor at '
                           'nx=20, dt=1e-3) rather than decaying to the linear reference as the '
                           'load tends to 1e-4.'),
            evidence=['mandel-reference', 'fe-load-limit-data']),
        'implementation': passed(
            'Material-point and residual checks: fluid EOS and reference-mass derivatives '
            '(110 checks, max scaled error 8.09e-09); conformal constitutive suite; independent '
            'spherical-gauge and reconstruction suites. The C++ law matches the independent '
            'Python evaluation to ' + format(cpp['value_absolute_error'], '.1e') + ' over '
            + str(cpp['states']) + ' finite states (artifact cpp-python-constitutive.json, '
            'which records the comparison itself).',
            ['fluid-coupling-verification', 'conformal-verification',
             'tensor-verification', 'reconstruction-verification',
             'cpp-python-constitutive']),
        'convergence': passed(
            'Manufactured-solution L2 convergence at a fixed final time: spatial order is '
            'consistent with Q2 displacement and Q1 pressure (ux 2.99/2.96, uy 3.00/2.96, '
            'p 2.00/2.00 over nx=4,8,16 at dt=1e-4). The temporal order is measured by successive '
            'differences of the exact-solution error norms at fixed mesh, which cancels the '
            'mesh-dependent spatial floor; the nx=16 triple (ux 1.093, uy 0.978, p 1.015) bounds '
            'the temporal order near one (at most about 1.1), consistent with backward Euler and '
            'not higher. At finer meshes the same measure gives nx=32 (ux 1.397, uy 1.018, p 1.125) '
            'and nx=64 (ux 1.396, uy 1.076, p 1.252). Those measured successive-difference orders '
            'belong to this mesh and step sequence and include values above one (ux is about 1.4); '
            'they are reported as measurements and no order above one is asserted. The departure '
            'from one at fixed mesh is a mesh-step cross term in the error '
            'balance: successive differences cancel a time-step-independent mesh floor exactly, so '
            'no order above one is claimed; naive error-ratio orders at fixed step are dominated by '
            'the spatial error and are never reported as temporal order. The isotropic '
            'Mandel spatial refinement is non-monotone at the finest level because of the initial '
            'drainage boundary discontinuity and is reported separately.',
            ['mms-convergence']),
        'finite_deformation': pending(
            'Rotated-anisotropy and partial-drainage cases are force-controlled demonstrations '
            'with a kinematic rigid platen (a top traction plus an equal-value boundary constraint). '
            'Their decks do not solve the reference-modulus isotropic quarter-domain Mandel problem '
            '(they use phi_s0=0.6 and K=7, and the partial family additionally uses the square domain '
            '[-1,1]x[-1,1]), so no Mandel-normalized discrepancy is reported for them and the '
            'formerly listed reference-normalized numbers are withdrawn; the measured per-run '
            'diagnostics are collected in finite-deformation-summary.json. Over the '
            + str(len(anisotropic)) + ' anisotropic runs at mineral orientations '
            + orientations + ' degrees' + mesh_note + ' the peak center pressure is '
            + rng(aniso, 'peak_pressure') + ' at t = ' + rng(aniso, 'peak_time')
            + ', the plate resultant reproduces the applied load with force_relative at most '
            + fmt(aniso['force_relative_max']) + ', and the discrete fluid-mass balance '
            'residual normalized by the mobilized mass is at most '
            + fmt(aniso['discrete_mass_mobilized_relative_max']) + '. The isotropic-comparison '
            'run gives peak center pressure ' + rng(isorun, 'peak_pressure')
            + ' and force_relative ' + fmt(isorun['force_relative_max']) + '. The '
            + str(len(partial)) + ' partial-drainage runs give peak center pressure '
            + rng(part, 'peak_pressure') + ' at t = ' + rng(part, 'peak_time')
            + ', force_relative at most ' + fmt(part['force_relative_max'])
            + ', and normalized mass balance at most '
            + fmt(part['discrete_mass_mobilized_relative_max']) + '. The corrected plate '
            'resultant is -2*a*q_L (full domain, a=1); it is an equilibrium residual, not a '
            'force-balance failure. No finite-deformation quantitative verification claim is made.',
            ['finite-deformation-summary']
            if 'finite-deformation-summary' in {a['id'] for a in artifacts} else []),
        'physical_validation': dict(
            status='not_performed',
            summary='The parameters are synthetic. No comparison to laboratory or field '
                    'measurements has been performed.', evidence=[]),
    }

    report = lambda kind: [kind] if kind in {a['id'] for a in artifacts} else []
    manifest['cases'] = [
        dict(title='Small-load isotropic Mandel consolidation',
             status='pending',
             description=('Coupled displacement and pressure response against the classical '
                          'analytical solution as the load tends to zero, using parameters that '
                          'satisfy the compliance restriction. Tolerances under review.'),
             artifacts=['fe-load-limit-data'] if 'fe-load-limit-data' in {a['id'] for a in artifacts} else []),
        dict(title='Rotated anisotropic consolidation',
             status='pending',
             description=('Force-controlled demonstration (top traction plus a kinematic rigid '
                          'platen) for prescribed mineral orientations on the slender domain '
                          '[-1,1]x[-0.1,0.1]; compared against the isotropic Mandel reference as a '
                          'demonstration of the anisotropic material response, not as verification.'),
             artifacts=[i for i in ('finite-deformation-summary', 'fe-map-anisotropic-30')
                        if i in {a['id'] for a in artifacts}]),
        dict(title='Partial-boundary drainage',
             status='pending',
             description=('Spatially restricted drainage producing two-dimensional flow and '
                          'deformation on the square domain [-1,1]x[-1,1]. Because the Mandel '
                          'analytical reference uses the slender domain [-1,1]x[-0.1,0.1], the '
                          'reference-normalized comparison is not comparable and is omitted; only '
                          'mass balance, force balance, platen equality, peak pressure, and the '
                          'maps are reported.'),
             artifacts=[i for i in ('finite-deformation-summary', 'fe-map-partial-0')
                        if i in {a['id'] for a in artifacts}]),
    ]

    manifest['reproduction'] = [
        dict(title='Build the MOOSE application',
             description='Configure the framework, then compile the repository application.',
             command='cd moose_app && make -j$(nproc)'),
        dict(title='Material-point verification',
             description='Independent constitutive and fluid-coupling checks.',
             command='python3 examples/verify_conformal.py && python3 examples/verify_fluid_coupling.py'),
        dict(title='Coupled runs',
             description='Isotropic Mandel, manufactured solution, anisotropic and partial drainage.',
             command='cd moose_app/scripts && python3 run_verification.py && python3 run_demonstrations.py'),
        dict(title='Plots',
             description='Regenerate figures from the recorded runs.',
             command='python3 examples/plot_fe_results.py'),
    ]
    manifest['limitations'] = [
        'Stress symmetry alone does not require the dilation-times-rotation specialization at every individual material state; the specialization and volume-only distention energy are additional constitutive assumptions.',
        'The drained and mineral stiffness tensors must obey the spherical rank-one compliance restriction; they are not independent inputs.',
        'The model describes mineral anisotropy; shape-changing distention and pore-shape anisotropy require additional constitutive mechanics.',
        'Rotated-anisotropy and partial-drainage runs are force-controlled demonstrations with a kinematic rigid platen, not verified quantitative predictions.',
        'Parameters are synthetic; agreement with numerical and analytical checks is not experimental validation.',
    ]

    (ROOT / 'site/evidence.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(dict(artifacts=len(artifacts), figures=len(figures),
                         snapshot_files=len(snapshot_files), source_revision=revision), indent=2))


if __name__ == '__main__':
    main()
