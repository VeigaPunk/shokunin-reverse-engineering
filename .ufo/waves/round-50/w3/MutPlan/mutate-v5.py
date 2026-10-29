#!/usr/bin/env python3
"""Mutation battery against the sibling seat's C3 v5 draft (a SCRATCH COPY).

The draft is copied to scratch and never edited in the lane.  Each mutation is
a single-point substitution in the copy; the copy's own `--selftest` is run and
the mutation is KILLED when the selftest exits != 0.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

S = '/fast/scratch/hyaku/kaidoku-r50/w3-MutPlan'
SRC = os.path.join(S, 'v5-draft.py')
BASE = os.path.join(S, 'v5-mut')
REQS = os.path.join(S, 'v5-mut-results.json')

MUTATIONS = [
    ('no-reader-set-drops-broadcom',
     "NO_READER_FAMILIES = (\n    'squashfs_v2_nonstandard',\n"
     "    'squashfs_v3_broadcom',\n    'squashfs_v3_nonstandard',\n)",
     "NO_READER_FAMILIES = (\n    'squashfs_v2_nonstandard',\n"
     "    'squashfs_v3_nonstandard',\n)",
     'the no-reader family set loses squashfs_v3_broadcom'),
    ('no-reader-set-drops-v2ns',
     "NO_READER_FAMILIES = (\n    'squashfs_v2_nonstandard',\n"
     "    'squashfs_v3_broadcom',\n    'squashfs_v3_nonstandard',\n)",
     "NO_READER_FAMILIES = (\n    'squashfs_v3_broadcom',\n"
     "    'squashfs_v3_nonstandard',\n)",
     'the no-reader family set loses squashfs_v2_nonstandard'),
    ('reader-backed-set-drops-ddwrt',
     "    'squashfs_v3_ddwrt',\n)",
     ")",
     'the reader-backed legacy set loses squashfs_v3_ddwrt'),
    ('no-reader-failure-row-deleted-from-table',
     "    ['no-reader-failure', 'extract_firmware', 'unblob', 'squashfs_*', NO_READER_CELL,\n"
     "     'extractor-failure+', '*', '*', '*', '0', 'preserve-unresolved',",
     "    ['no-reader-failure-DELETED', 'extract_firmware', 'unblob', 'squashfs_*', NO_READER_CELL,\n"
     "     'extractor-failure+', '*', '*', '*', '0', 'preserve-unresolved',",
     'the table row that names no-reader-failure is renamed'),
    ('clean-unverified-row-files-cell-widened',
     "     'none', '*', '*', 'no', '>0', 'record-unverified',",
     "     'none', '*', '*', 'no', '*', 'record-unverified',",
     'the clean-unverified row fires on zero-file runs too'),
    ('clean-unverified-row-symlink-cell-widened',
     "     'none', '*', '*', 'no', '>0', 'record-unverified',",
     "     'none', '*', '*', '*', '>0', 'record-unverified',",
     'the clean-unverified row no longer excludes a removed-symlink run'),
    ('evaluator-no-reader-meets-all',
     "def _meets(names, wanted):\n"
     "    \"\"\"The table's positive subset test: any member of ``names`` is in ``wanted``.\"\"\"\n"
     "    for name in names:\n"
     "        if name in wanted:\n"
     "            return True\n"
     "    return False",
     "def _meets(names, wanted):\n"
     "    \"\"\"The table's positive subset test: any member of ``names`` is in ``wanted``.\"\"\"\n"
     "    if not names:\n"
     "        return False\n"
     "    for name in wanted:\n"
     "        if name not in names:\n"
     "            return False\n"
     "    return True",
     'the no-reader test becomes an ALL-match instead of ANY-match'),
    ('evaluator-clean-unverified-step-dropped',
     "        if p > 0:\n"
     "            if _meets(f, NO_READER_SET):\n"
     "                return 'clean-unverified', 'record-unverified', 15\n"
     "            return 'clean', 'none', 16",
     "        if p > 0:\n"
     "            return 'clean', 'none', 16",
     'the evaluator never returns clean-unverified'),
    ('evaluator-no-reader-failure-step-dropped',
     "    if FAILURE_KIND in g and p == 0 and _meets(hf, NO_READER_SET):\n"
     "        return 'no-reader-failure', 'preserve-unresolved', 8",
     "    if False:\n"
     "        return 'no-reader-failure', 'preserve-unresolved', 8",
     'the evaluator never returns no-reader-failure'),
    ('evaluator-legacy-step-widened-to-all',
     "    if FAILURE_KIND in g and p == 0 and _meets(hf, READER_BACKED_SET):\n"
     "        return 'legacy-body-failure', 'cross-read-legacy', 7",
     "    if FAILURE_KIND in g and p == 0:\n"
     "        return 'legacy-body-failure', 'cross-read-legacy', 7",
     'the evaluator sends every zero-file failure to cross-read-legacy'),
    ('table-legacy-row-keeps-the-wide-glob',
     "    ['legacy-body-failure', 'extract_firmware', 'unblob', 'squashfs_*', READER_BACKED_CELL,",
     "    ['legacy-body-failure', 'extract_firmware', 'unblob', 'squashfs_*', 'squashfs_v[123]*',",
     'the table keeps the v4 wide failing-handler glob'),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for c in iter(lambda: fh.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()


def run_one(name, old, new, desc):
    root = os.path.join(BASE, name)
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(root)
    with open(SRC, encoding='utf-8') as fh:
        base = fh.read()
    n = base.count(old)
    if n != 1:
        return {'name': name, 'status': 'anchor-error', 'anchor_count': n,
                'description': desc, 'old': old[:90]}
    mutated = base.replace(old, new)
    cpath = os.path.join(root, 'sqfs-triage-v5.py')
    with open(cpath, 'w', encoding='utf-8') as fh:
        fh.write(mutated)
    comp = subprocess.run([sys.executable, '-I', '-B', '-c',
                           'import ast,sys;ast.parse(open(sys.argv[1]).read())', cpath],
                          capture_output=True, text=True)
    if comp.returncode != 0:
        return {'name': name, 'status': 'syntax-error', 'description': desc,
                'stderr': comp.stderr[-400:]}
    env = dict(os.environ)
    env['TMPDIR'] = os.path.join(root, 'tmp')
    env['HYAKU_SCRATCH'] = os.path.join(root, 'hyaku')
    os.makedirs(env['TMPDIR'], exist_ok=True)
    started = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    p = subprocess.run([sys.executable, '-I', '-B', 'sqfs-triage-v5.py', '--selftest'],
                       cwd=root, capture_output=True, text=True, env=env, timeout=1200)
    out = p.stdout or ''
    tail = out.strip().splitlines()[-3:] if out.strip() else []
    return {
        'name': name, 'status': 'ran', 'description': desc,
        'command': 'python3 -I -B sqfs-triage-v5.py --selftest',
        'exit_code': p.returncode, 'utc_started': started,
        'stdout_sha256': hashlib.sha256(out.encode()).hexdigest(),
        'stdout_tail': tail,
        'stderr_sha256': hashlib.sha256((p.stderr or '').encode()).hexdigest(),
        'stderr_tail': (p.stderr or '')[-500:],
        'mutant_sha256': sha256_file(cpath),
        'pristine_sha256': sha256_file(SRC),
        'verdict': 'killed' if p.returncode != 0 else 'survived',
    }


def main():
    only = sys.argv[1:] or None
    os.makedirs(BASE, exist_ok=True)
    results = []
    for name, old, new, desc in MUTATIONS:
        if only and name not in only:
            continue
        r = run_one(name, old, new, desc)
        results.append(r)
        print('%-46s %-12s exit=%s' % (r['name'], r['status'], r.get('exit_code')),
              flush=True)
        json.dump(results, open(REQS, 'w'), indent=1, sort_keys=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
