#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Materialize the finite-element run evidence at a repository-relative path.

The coupled runs are produced under the ignored runtime directory
(``.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs``). The
manuscript's code-and-data availability statement and the published evidence
must point at a path that exists in the repository, so this tool copies the
deck input, provenance record, per-run analysis, scalar history, and solver log
of every recorded run into ``fe-evidence/runs/<case>/`` together with the
convergence analysis, and writes ``fe-evidence/README.md``.

It copies recorded artifacts only; it runs no solver and certifies no result.
"""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.agent-runtime/moose-fe-goal-2026-09-20'
RUNS = RUNTIME / 'implementation' / 'runs'
DEST = ROOT / 'fe-evidence'

# Per-run artifacts that make a run reproducible and checkable.
RUN_FILES = ('input.i', 'provenance.json', 'analysis.json', 'solution.csv',
             'reference_comparison.csv', 'run.log')


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not RUNS.is_dir():
        raise SystemExit('no runtime run directory: ' + str(RUNS))
    cases = sorted(p.name for p in RUNS.iterdir() if p.is_dir())
    if not cases:
        raise SystemExit('no recorded runs in ' + str(RUNS))

    if DEST.exists():
        shutil.rmtree(DEST)
    (DEST / 'runs').mkdir(parents=True)

    entries, missing = [], []
    for case in cases:
        src_dir = RUNS / case
        for name in RUN_FILES:
            src = src_dir / name
            if not src.is_file():
                missing.append(f'{case}/{name}')
                continue
            dst = DEST / 'runs' / case / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            entries.append(dict(path=f'runs/{case}/{name}', sha256=sha(dst), bytes=dst.stat().st_size))

    for src, rel in ((RUNTIME / 'parent-analysis' / 'mms-convergence.json', 'mms-convergence.json'),
                     (RUNTIME / 'parent-analysis' / 'compute_mms_order.py', 'compute_mms_order.py')):
        if not src.is_file():
            raise SystemExit('missing convergence artifact: ' + str(src))
        shutil.copy2(src, DEST / rel)
        entries.append(dict(path=rel, sha256=sha(DEST / rel), bytes=(DEST / rel).stat().st_size))

    # Every run provenance that declares a run.log must ship it, so the declared
    # digest resolves inside the evidence directory. The recorded source hashes
    # must also match the shipped sources, otherwise the run was produced by a
    # superseded revision and cannot be reproduced from this evidence set.
    case_records = []
    for case in cases:
        prov = DEST / 'runs' / case / 'provenance.json'
        if not prov.is_file():
            continue
        record = json.loads(prov.read_text())
        declared = record.get('outputs', {}).get('run.log')
        log = DEST / 'runs' / case / 'run.log'
        if declared and (not log.is_file() or sha(log) != declared):
            raise SystemExit(f'run.log digest does not resolve for {case}')
        mismatched = []
        for rel, want in sorted(record.get('source_sha256', {}).items()):
            src = ROOT / rel
            if not src.is_file() or sha(src) != want:
                mismatched.append(rel)
        if mismatched:
            raise SystemExit('recorded source digests do not match the shipped sources for '
                             + case + ': ' + ', '.join(mismatched))
        outputs = record.get('outputs', {})
        unshipped = [name for name in sorted(outputs)
                     if not (DEST / 'runs' / case / name).is_file()]
        case_records.append(dict(
            case=case,
            analysis_present=bool((DEST / 'runs' / case / 'analysis.json').is_file()),
            reference_comparison_present=bool((DEST / 'runs' / case / 'reference_comparison.csv').is_file()),
            provenance_outputs_total=len(outputs),
            provenance_outputs_unshipped=unshipped,
            binary_sha256=record.get('binary_sha256'),
        ))

    (DEST / 'manifest.json').write_text(json.dumps(
        dict(cases=cases, files=entries, not_applicable=missing,
             runs=case_records,
             notes=[
                 'Each runs/<case>/provenance.json enumerates the complete output set of the '
                 'source run. Only the curated subset listed in files[] ships. For the source '
                 'runs the large Exodus solution.e and the per-step solution_profile_*.csv '
                 'dumps are intentionally not shipped because of size, and '
                 'provenance_outputs_unshipped records the difference per case; the four '
                 'refined fabric_contour_* field files and the sixteen fabric_mandel_* '
                 'profile dumps are the exceptions that do ship.',
                 'not_applicable lists recorded run files that are deliberately not shipped '
                 '(the non-comparable demonstration/Jacobian/MMS/one-element decks do not solve '
                 'the reference-modulus Mandel problem, so they carry no reference_comparison.csv).',
                 'provenance.json binary_sha256 is the digest of the compiled application that '
                 'produced the run. The binary is not shipped; every recorded source_sha256 '
                 'digest is verified against the shipped sources by '
                 'tools/materialize_fe_evidence.py, which fails if any does not match.',
                 'The assembled-Jacobian decks ship analysis.json with the recorded '
                 '||J - Jfd||_F/||J||_F values; the Jacobian decks do not emit a per-run '
                 'reference_comparison.csv.',
             ]), indent=2) + '\n')
    (DEST / 'README.md').write_text(
        '# Finite-element run evidence\n\n'
        'Copied from the MOOSE run runtime by `tools/materialize_fe_evidence.py`.\n'
        'Each `runs/<case>/` holds the deck (`input.i`), the recorded provenance\n'
        '(`provenance.json`), the per-run analysis where one was produced\n'
        '(`analysis.json`), the scalar history (`solution.csv`), the solver log\n'
        '(`run.log`), and the reference comparison (`reference_comparison.csv`) only\n'
        'for the cases whose deck solves the same reference-modulus quarter-domain\n'
        'Mandel problem. `manifest.json` records per case whether `analysis.json` and\n'
        '`reference_comparison.csv` are present and lists the intentionally unshipped\n'
        'source-run outputs (`provenance_outputs_unshipped`); a `reference_note` in\n'
        'each non-comparable `analysis.json` states why no Mandel-normalized metric is\n'
        'reported.\n\n'
        '`mms-convergence.json` is the manufactured-solution convergence analysis and\n'
        '`compute_mms_order.py` recomputes it. `manifest.json` lists SHA-256 digests.\n'
        'These are force-controlled finite-load and manufactured-solution runs; the\n'
        'rotated-anisotropy and partial-drainage cases are demonstrations, not\n'
        'quantitative finite-deformation verification.\n')
    print(json.dumps(dict(cases=len(cases), files=len(entries), not_applicable=missing), indent=2))


if __name__ == '__main__':
    main()
