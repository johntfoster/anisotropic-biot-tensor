#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Run the refined pore-fabric contour decks and record the shipped evidence.

Runs the four coupled contour variants (isotropic, fabric axis 0/45/90 deg) of
``moose_app/inputs/fabric_contour.i`` on the 40 x 4 quarter-Mandel mesh and
records the deck, scalar history, solver log, the Exodus field file (kept so the
contour figures are reproducible from the recorded fields), and a provenance
record under ``fe-evidence/runs/fabric_contour_<case>/``.
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / 'moose_app/anisotropic_biot-opt'
LIB = ROOT / 'moose_app/lib/libanisotropic_biot-opt.so.0.0.0'
DEST = ROOT / 'fe-evidence/runs'
SOURCE = 'moose_app/include/utils/FabricLaw.h, moose_app/src/materials/FabricMaterial.C'
SOURCE_FILES = ('moose_app/include/utils/FabricLaw.h',
                'moose_app/include/materials/FabricMaterial.h',
                'moose_app/src/materials/FabricMaterial.C')
CONTOUR_DECK = 'moose_app/inputs/fabric_contour.i'
PLOT_SCRIPT = 'examples/plot_fabric_contours.py'
PLOT_MANIFEST = 'figures/fe_fabric_contours-plot-manifest.json'

# case -> command-line overrides (deck defaults: coupling 0.4, angle 0)
CASES = [
    ('fabric_contour_iso', ['Materials/law/fabric_coupling=0', 'Materials/law/fabric_angle=0']),
    ('fabric_contour_a0', ['Materials/law/fabric_angle=0']),
    ('fabric_contour_a45', ['Materials/law/fabric_angle=45']),
    ('fabric_contour_a90', ['Materials/law/fabric_angle=90']),
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def revision():
    return subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()


def run_case(case, overrides):
    # The deck runs inside the temporary directory with a *relative* output base.
    # MOOSE records the output base as the Exodus `title` attribute, so an
    # absolute temporary path would embed a fresh random directory name in every
    # regeneration and make the shipped bytes irreproducible. A relative base
    # keeps `title = solution.e` for every run, so identical inputs give
    # identical Exodus bytes.
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        deck = ROOT / CONTOUR_DECK
        command = [str(BIN), '-i', str(deck),
                   'Outputs/file_base=solution', '--n-threads=1'] + overrides
        start = dt.datetime.now(dt.timezone.utc)
        proc = subprocess.run(command, cwd=out, capture_output=True, text=True)
        end = dt.datetime.now(dt.timezone.utc)
        status = 'success' if proc.returncode == 0 else 'failed'
        if (DEST / case).exists():
            shutil.rmtree(DEST / case)
        (DEST / case).mkdir(parents=True, exist_ok=True)
        (DEST / case / 'run.log').write_text(proc.stdout + proc.stderr)
        provenance = dict(
            application='anisotropic_biot-opt (FabricMaterial)',
            application_sha256=sha(BIN),
            application_library_sha256=sha(LIB),
            binary_sha256=sha(BIN),
            git_revision=revision(),
            input_sha256=sha(ROOT / CONTOUR_DECK),
            source_sha256={path: sha(ROOT / path) for path in SOURCE_FILES},
            input_deck='fabric_contour.i',
            mesh='nx=40 ny=4 on [0,1] x [0,0.1] (QUAD9)',
            time_control='dt=0.0003, end_time=0.003 (implicit-euler; 11 field snapshots incl. initial)',
            command_overrides=overrides,
            command=['./moose_app/anisotropic_biot-opt', '-i', 'moose_app/inputs/fabric_contour.i',
                     'Outputs/file_base=solution'] + overrides,
            recorded_utc=end.isoformat(),
            exit_status=status,
            source=SOURCE,
        )
        (DEST / case / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
        if proc.returncode != 0:
            print((proc.stdout + proc.stderr)[-2000:])
            return status
        if not (out / 'solution.csv').is_file():
            (DEST / case / 'provenance.json').write_text(
                json.dumps(dict(provenance, exit_status='failed-no-history'), indent=2) + '\n')
            return 'failed-no-history'
        shutil.copy2(out / 'solution.csv', DEST / case / 'solution.csv')
        # Write the per-run analysis here rather than only under --analysis-only:
        # the case directory was just replaced, so leaving it to a later step
        # would ship an evidence set with analysis.json silently absent.
        (DEST / case / 'analysis.json').write_text(
            json.dumps(final_row(case), indent=2, sort_keys=True) + '\n')
        exodus = out / 'solution.e'
        if not exodus.is_file():
            (DEST / case / 'provenance.json').write_text(
                json.dumps(dict(provenance, exit_status='failed-no-exodus'), indent=2) + '\n')
            return 'failed-no-exodus'
        shutil.copy2(exodus, DEST / case / 'solution.e')
        shutil.copy2(ROOT / 'moose_app/inputs/fabric_contour.i', DEST / case / 'input.i')
    return status


def final_row(case):
    with open(DEST / case / 'solution.csv') as stream:
        row = list(csv.DictReader(stream))[-1]
    return {key: float(value) for key, value in row.items()}


def regenerate_analysis():
    for case, _ in CASES:
        (DEST / case / 'analysis.json').write_text(
            json.dumps(final_row(case), indent=2, sort_keys=True) + '\n')
    print('regenerated analysis.json for', len(CASES), 'contour cases')


def refresh_figures():
    """Regenerate the contour figure data and re-verify their declared digests.

    Order is the point: these decks rewrite the recorded Exodus files that the
    contour plot manifest hashes, so the figure data and the manifest must be
    rebuilt *after* the decks and then re-checked. Skipping the last step is
    what let a stale ``input_sha256`` ship in an earlier round.
    """
    subprocess.run(['python3', PLOT_SCRIPT, '--runs', 'fe-evidence/runs',
                    '--output', 'figures'], cwd=ROOT, check=True)
    subprocess.run(['python3', 'tools/check_figure_manifests.py', PLOT_MANIFEST],
                   cwd=ROOT, check=True)
    print('figure data and plot manifest regenerated, then re-verified')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--analysis-only', action='store_true',
                        help='regenerate analysis.json from the recorded histories')
    parser.add_argument('--no-figures', action='store_true',
                        help='skip regenerating the contour figures and plot manifest')
    args = parser.parse_args()
    if args.analysis_only:
        regenerate_analysis()
        return
    print('git', revision(), 'app', sha(BIN), 'library', sha(LIB))
    results = {}
    for case, overrides in CASES:
        results[case] = run_case(case, overrides)
        print(f'{case:26s} {results[case]}', flush=True)
    print(json.dumps(results, indent=2))
    if any(status != 'success' for status in results.values()):
        raise SystemExit('one or more contour decks failed')
    if not args.no_figures:
        refresh_figures()


if __name__ == '__main__':
    main()
