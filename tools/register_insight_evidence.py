#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Register the three discriminating fabric studies and refresh publication hashes.

Run after both generators, supplement packaging, and the manuscript build.
This records existing evidence; it does not change scientific gate outcomes.
"""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    generated = ROOT/'build/insight'
    manifests = [json.loads((generated/name).read_text()) for name in ('manifest.json', 'comparison_manifest.json')]
    inputs, outputs = {}, {}
    for manifest in manifests:
        for name, digest in manifest['input_sha256'].items():
            assert sha(ROOT/name) == digest, name
            inputs[name] = digest
        for name, digest in manifest['output_sha256'].items():
            p = generated/name
            assert sha(p) == digest, name
            if p.suffix in ('.png', '.csv', '.json', '.tex'):
                dst = ROOT/'figures'/('insight_'+name)
                shutil.copyfile(p, dst)
                outputs[dst.name] = sha(dst)
    probe = generated/'scalar_probe_verification.json'
    proof = json.loads(probe.read_text())
    for name, digest in proof['input_sha256'].items():
        assert sha(ROOT/name) == digest, name
        inputs[name] = digest
    shutil.copyfile(probe, ROOT/'figures/insight_scalar_probe_verification.json')
    outputs['insight_scalar_probe_verification.json'] = sha(probe)
    manifest_path = ROOT/'figures/insight-plot-manifest.json'
    manifest_path.write_text(json.dumps(dict(input_sha256=inputs, output_sha256=outputs), indent=2)+'\n')
    runs = sorted((ROOT/'fe-evidence/insight').glob('*/*')) + sorted((ROOT/'fe-evidence/insight-probe').glob('*/*'))
    files = {str(p.relative_to(ROOT/'fe-evidence')): sha(p) for p in runs if p.is_file()}
    (ROOT/'fe-evidence/insight-manifest.json').write_text(json.dumps(dict(files=files,
        scope='Reference-state coupled scalar/tensor comparison; run records identify source and compiled binaries.'), indent=2)+'\n')

    path = ROOT/'site/evidence.json'
    site = json.loads(path.read_text())
    artifacts = {a['id']: a for a in site['artifacts']}
    def add(ident, name, kind, label):
        if name.startswith('tools/'):
            copy = ROOT/'site/sources'/Path(name).name
            copy.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT/name, copy)
            name = str(copy.relative_to(ROOT))
        artifacts[ident] = dict(id=ident, path=name, destination=Path(name).name,
                               kind=kind, label=label, sha256=sha(ROOT/name))
    add('current-paper', 'build/main.pdf', 'paper', 'Current manuscript PDF with numerical supplement')
    add('numerical-supplement', 'build/anisotropic-biot-2026-09-22-v3.zip', 'supplement', 'Versioned numerical sources, recorded histories and verification reports')
    figures = [
        ('fabric-pressure-shear', 'fabric_pressure_shear', 'Pressure-induced shear reactions with isotropic mineral and oblique fabric; reference linear law.'),
        ('fabric-scalar-comparison', 'fabric_comparison', 'Scalar-versus-tensor coupled consolidation with fixed drained stiffness, storage and isotropic mobility; loading and drainage histories.'),
        ('fabric-finite-benchmark', 'fabric_finite', 'Finite commuting pure shear: pressure-induced stress, pore volume, shape change and reference-linearization error.')]
    for ident, name, caption in figures:
        add(ident, f'figures/insight_{name}.png', 'figure', caption)
        site['figures'] = [x for x in site['figures'] if x['artifact'] != ident]
        site['figures'].append(dict(artifact=ident, caption=caption, alt=caption))
    # Retain legacy artifacts as downloadable supplementary evidence; replace
    # their main gallery panels with the three physical studies.
    legacy = {'fe-fabric-probe', 'fe-fabric-mandel', 'fe-fabric-contours', 'fe-fabric-diffusion'}
    site['figures'] = [x for x in site['figures'] if x['artifact'] not in legacy]
    add('fabric-finite-checks', 'figures/insight_verification.json', 'report',
        'Full spatial stress, pressure tangent and reference limit on commuting finite states')
    add('fabric-comparison-checks', 'figures/insight_comparison_verification.json', 'report',
        'Coupled histories: model errors, conservation and joint refinement sensitivity')
    add('fabric-scalar-probe-checks', 'figures/insight_scalar_probe_verification.json', 'report',
        'Compiled scalar/tensor stress, storage and drained stiffness checked against a separate linear solve')
    for name in ['pressure_shear.csv', 'pressure_shear_moduli.csv', 'finite_fabric.csv', 'finite_error.csv', 'comparison_errors.csv']:
        add('insight-'+name.replace('_', '-').replace('.csv', ''), 'figures/insight_'+name, 'data', name)
    for name in ['examples/fabric_insight.py', 'examples/plot_fabric_comparison.py',
                 'tools/run_fabric_comparison.py', 'moose_app/inputs/fabric_comparison.i']:
        add('insight-'+Path(name).stem.replace('_', '-'), name,
            'deck' if name.endswith('.i') else 'source', 'Reproduction source: '+Path(name).name)
    finite = site['categories']['finite_deformation']
    finite['summary'] = ('A material-point benchmark verifies full spatial stress and pressure derivatives, '
        'independent equilibrium minimization, and the reference limit for an isotropic mineral with '
        'commuting finite distention and stress. A general noncoaxial fabric law and quantitative '
        'finite-deformation coupled verification remain pending. Historical coupled finite-load '
        'calculations are demonstrations, as recorded in finite-deformation-summary.json.')
    finite['evidence'] = sorted(set(finite['evidence']) | {'fabric-finite-checks'})
    site['categories']['implementation']['evidence'] = sorted(set(site['categories']['implementation']['evidence']) | {'fabric-comparison-checks', 'fabric-scalar-probe-checks'})
    site['limitations'] = [s for s in site['limitations'] if not s.startswith('The pore-fabric extension relaxes')]
    site['limitations'].append('The fabric extension supplies a reference quadratic law and a finite commuting specialization. '
        'Full phase-work equivalence at finite deformation requires commuting distention and mineral stress. '
        'The scalar comparison is phenomenological and does not supply mineral-volume predictions.')
    site['reproduction'] = [r for r in site['reproduction'] if r['title'] != 'Discriminating fabric studies']
    site['reproduction'].append(dict(title='Discriminating fabric studies',
        description='Generate the finite material benchmark and compare the recorded coupled histories. Recompute the MOOSE histories with tools/run_fabric_comparison.py in the verified environment.',
        command='python3 examples/fabric_insight.py\npython3 examples/plot_fabric_comparison.py'))
    site['version'] = '2026-09-22-insight-studies'
    for a in artifacts.values():
        if a['path'].endswith('anisotropic-biot-2026-09-20-v2.zip'):
            a['path'] = a['path'].replace('2026-09-20-v2', '2026-09-22-v3')
            a['destination'] = a['destination'].replace('2026-09-20-v2', '2026-09-22-v3')
    # Snapshot hashes describe current sources, independently of the base commit.
    sp = ROOT/'site/scientific-snapshot.json'
    snapshot = json.loads(sp.read_text())
    names = {e['path'] for e in snapshot['files']}
    names.update(['main.tex', 'sections/pore_fabric.tex', 'sections/finite_elements.tex',
                  'sections/fabric_studies.tex', 'examples/fabric_insight.py',
                  'examples/plot_fabric_comparison.py', 'tools/run_fabric_comparison.py',
                  'tools/register_insight_evidence.py', 'tools/verify_scalar_probe.py', 'moose_app/inputs/fabric_comparison.i',
                  'moose_app/src/materials/FabricMaterial.C', 'moose_app/include/materials/FabricMaterial.h'])
    snapshot['files'] = [dict(path=n, sha256=sha(ROOT/n)) for n in sorted(names)]
    sp.write_text(json.dumps(snapshot, indent=2)+'\n')
    for a in artifacts.values():
        a['sha256'] = sha(ROOT/a['path'])
    site['artifacts'] = sorted(artifacts.values(), key=lambda a: a['id'])
    path.write_text(json.dumps(site, indent=2)+'\n')
    print('Registered three studies,', len(files), 'run artifacts and', len(outputs), 'publication outputs.')


if __name__ == '__main__':
    main()
