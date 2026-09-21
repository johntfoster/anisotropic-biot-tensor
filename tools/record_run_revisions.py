#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Record the revision for run records that declare source digests but no revision.

The pore-fabric harnesses record ``git_revision`` directly, so their run records
carry both a revision and the source digests. The 38 coupled-runtime records were
produced by an ad-hoc harness that never recorded a revision; they carry
``source_sha256`` alone, which makes the schema asymmetric and leaves a reader
unable to say which sources the run used.

This tool closes that gap without inventing history. For each record that lacks
``git_revision`` it resolves a candidate revision whose *tree* contains exactly
the recorded source digests, verified byte-for-byte through the git object
database (never through the mutable working tree). It writes

    git_revision        the verified revision
    git_revision_basis  how that revision was established

so the claim is checkable and the basis is explicit: the field records a
revision whose sources match the run's declared digests, which is weaker than
"the run was made at this revision". Records that cannot be resolved are left
untouched and reported.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / 'fe-evidence/runs'
BASIS = ('recorded source_sha256 digests matched byte-for-byte against this '
         "commit's tree via the git object database; the run harness did not "
         'record a revision at run time, so this is the revision whose sources '
         'match, not necessarily the revision the run was made from')


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or 'git failed: ' + ' '.join(args))
    return result.stdout


def blob_digest(rev: str, path: str) -> str | None:
    result = subprocess.run(['git', 'show', f'{rev}:{path}'], cwd=ROOT,
                            capture_output=True)
    if result.returncode:
        return None
    return hashlib.sha256(result.stdout).hexdigest()


def resolve_revision(record: dict, candidates: list[str]) -> tuple[str | None, int]:
    """Return (revision, matched-count) for the first candidate whose tree matches."""
    sources = record.get('source_sha256') or {}
    if not sources:
        return None, 0
    for rev in candidates:
        matched = sum(1 for path, digest in sources.items()
                      if blob_digest(rev, path) == digest)
        if matched == len(sources):
            return rev, matched
    return None, 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', action='append', default=None,
                        help='candidate revision (default: HEAD, repeated for a range)')
    parser.add_argument('--check', action='store_true',
                        help='verify only; do not write')
    args = parser.parse_args()

    candidates = args.revision or [git('rev-parse', 'HEAD').strip()]
    if not args.revision:
        # Walk back a bounded window so a run made before later commits can
        # still be resolved when the sources it used are unchanged since.
        history = git('rev-list', '--max-count=60', 'HEAD').split()
        candidates = [git('rev-parse', 'HEAD').strip()] + history

    unresolved, written = [], 0
    for path in sorted(glob.glob(str(RUNS / '*' / 'provenance.json'))):
        record_path = Path(path)
        record = json.loads(record_path.read_text())
        if record.get('git_revision'):
            continue
        rev, matched = resolve_revision(record, candidates)
        if rev is None:
            unresolved.append(record_path.parent.name)
            continue
        if not args.check:
            record['git_revision'] = rev
            record['git_revision_basis'] = BASIS
            record_path.write_text(json.dumps(record, indent=2) + '\n')
        written += 1
        print(f'{record_path.parent.name:26s} {rev} ({matched} source digests matched)')

    if unresolved:
        print('unresolved (left untouched): ' + ', '.join(unresolved), file=sys.stderr)
    print(f'{written} record(s) {"verified" if args.check else "recorded"}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
