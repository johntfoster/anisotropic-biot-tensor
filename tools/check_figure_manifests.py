#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Re-hash every digest a figure plot manifest declares and report mismatches.

The plot manifests under ``figures/`` record the SHA-256 of each declared input
(the recorded evidence and the generator script) and of each produced figure
file. A stale ``input_sha256`` silently breaks provenance: the manifest claims
an input identity that the shipped bytes no longer have. This checker recomputes
every declared digest from the artifact on disk, so a stale entry is caught by a
check instead of by a reviewer.

Order matters. Any step that regenerates an input (running the MOOSE decks
rewrites the recorded Exodus files) must run *before* the figure data and the
plot manifest that hash it; run this checker as the last step of that sequence.
It computes digests from the produced artifacts and never trusts a stored
value.

Exit status is non-zero when any declared digest disagrees with the file on
disk, when a declared file is missing, or when a manifest is not parseable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GLOB = 'figures/*-plot-manifest.json'


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def resolve(key: str, manifest_path: Path) -> Path:
    """Resolve a manifest key the way its generator wrote it.

    Input keys are repository-relative paths (``fe-evidence/runs/...``); output
    keys are bare figure basenames that live beside the manifest in
    ``figures/``. Resolving a bare basename against the repository root would
    pick up an unrelated same-named file, so the split is on the presence of a
    path separator.
    """
    if '/' in key or os.sep in key:
        return ROOT / key
    return manifest_path.parent / key


def check_manifest(manifest_path: Path) -> list[str]:
    """Return a list of human-readable defects; empty means the manifest holds."""
    problems: list[str] = []
    try:
        report = json.loads(manifest_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return [f'{manifest_path}: not parseable JSON ({exc})']

    for section in ('input_sha256', 'output_sha256'):
        declared = report.get(section)
        if not isinstance(declared, dict):
            problems.append(f'{manifest_path}: missing or malformed "{section}"')
            continue
        if not declared:
            problems.append(f'{manifest_path}: "{section}" is empty')
        for key, expected in sorted(declared.items()):
            target = resolve(key, manifest_path)
            if not target.is_file():
                problems.append(f'{manifest_path}: declared file missing on disk: {key}')
                continue
            actual = sha(target)
            if actual != expected:
                problems.append(
                    f'{manifest_path}: stale {section} for {key}: '
                    f'declared {expected} but hashed {actual}')
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifests', nargs='*', type=Path,
                        help=f'plot manifests to check (default: {DEFAULT_GLOB})')
    args = parser.parse_args()

    manifests = args.manifests or sorted(ROOT.glob(DEFAULT_GLOB))
    if not manifests:
        raise SystemExit('no plot manifests found')

    problems: list[str] = []
    for manifest in manifests:
        defects = check_manifest(manifest)
        label = manifest.name if manifest.is_absolute() or manifest.parent == Path('.') else str(manifest)
        if defects:
            problems.extend(defects)
            print(f'FAIL {label}: {len(defects)} problem(s)')
        else:
            report = json.loads(manifest.read_text())
            print(f'OK   {label}: '
                  f'{len(report.get("input_sha256", {}))} inputs, '
                  f'{len(report.get("output_sha256", {}))} outputs verified')

    if problems:
        print('\n'.join(problems), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
