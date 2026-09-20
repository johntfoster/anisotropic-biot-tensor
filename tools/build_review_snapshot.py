#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Freeze an immutable review snapshot of the repository.

Copies the scientific sources, evidence, documents, and docs referenced by
`README.md`/`AGENTS.md` into a read-only directory, writes a SHA-256 manifest,
and records the manifest digest as the snapshot ID. Reviewers verify
`sha256(source-manifest.json)` against `SNAPSHOT_ID` and re-hash every listed
file. Only recorded artifacts are copied; no check is run here.
"""
import hashlib
import json
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROUND = sys.argv[1] if len(sys.argv) > 1 else 'round-14'
DEST = os.path.join(REPO, '.agent-runtime/review-snapshots', ROUND)

SKIP_SUFFIX = ('.o', '.so', '.a', '.lo', '.la', '.lo.d', '.mod', '.pyc')
SKIP_NAMES = ('anisotropic_biot-opt',)


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def walk(root, repo_rel, out, skip_dirs=()):
    for base, dirs, names in os.walk(os.path.join(REPO, root)):
        dirs[:] = [d for d in dirs if d not in skip_dirs and d != '__pycache__' and d != '.git']
        for name in sorted(names):
            if name.startswith('.') or name in SKIP_NAMES or name.endswith(SKIP_SUFFIX):
                continue
            out.add(os.path.relpath(os.path.join(base, name), REPO))


def main():
    files = set()
    for name in ('AGENTS.md', 'README.md', 'VISION.md', 'LICENSES.md', 'LICENSE',
                 'author_style_profile.md', 'main.tex', 'references.bib'):
        files.add(name)
    for directory in ('sections', 'provenance', 'licenses', 'site', 'validation',
                      'figures', 'fe-evidence', 'agent_local'):
        walk(directory, directory, files, skip_dirs=())
    walk('references/notes', 'references/notes', files)
    # Reviewers must not read other reviewers' reports or prior-round votes, so
    # the snapshot carries the review policy document but no round directories.
    files.add('reviews/README.md')
    files.add('.agent/shared/AGENTS.shared.md')
    walk('.agent/shared/skills', '.agent/shared/skills', files)
    for name in sorted(os.listdir(os.path.join(REPO, 'examples'))):
        if name.endswith(('.py', '.txt', '.md')):
            files.add(os.path.join('examples', name))
    for name in sorted(os.listdir(os.path.join(REPO, 'tools'))):
        if name.endswith('.py'):
            files.add(os.path.join('tools', name))
    files.update(('build/main.pdf', 'build/main.log', 'build/conformal-2026-09-20-v1.zip'))
    for sub in ('conformal', 'weighted-stress'):
        walk(os.path.join('build', sub), os.path.join('build', sub), files)
    walk('moose_app', 'moose_app', files, skip_dirs=('build', 'lib', '.libs'))

    if os.path.isdir(DEST):
        shutil.rmtree(DEST)
    os.makedirs(DEST)
    manifest, missing = {}, []
    for rel in sorted(files):
        src = os.path.join(REPO, rel)
        if not os.path.isfile(src):
            missing.append(rel)
            continue
        dst = os.path.join(DEST, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        manifest[rel] = sha(src)
    manifest_path = os.path.join(DEST, 'source-manifest.json')
    with open(manifest_path, 'w') as stream:
        json.dump(manifest, stream, indent=2, sort_keys=True)
        stream.write('\n')
    snapshot_id = sha(manifest_path)
    with open(os.path.join(DEST, 'SNAPSHOT_ID'), 'w') as stream:
        stream.write(snapshot_id + '\n')
    for base, dirs, names in os.walk(DEST):
        for name in names:
            os.chmod(os.path.join(base, name), 0o444)
        os.chmod(base, 0o555)
    print('SNAPSHOT_ID', snapshot_id)
    print('files', len(manifest))
    print('missing', missing)


if __name__ == '__main__':
    main()
