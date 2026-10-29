#!/usr/bin/env python3
"""Mutation battery for the frozen R50-C1 counter (scratch copies only).

Each mutation is a single-point text substitution applied to a COPY of the
frozen counter.  The copy is run with `--selftest`; the mutation is KILLED when
the selftest exits != 0 (it noticed the defect), SURVIVED when it exits 0.

Nothing in the lane tree is written: the copies live under this seat's scratch.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

S = '/fast/scratch/hyaku/kaidoku-r50/w3-MutPlan'
SRC = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/c1-counter.py'
XPIN = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-27/xpin-attribute.mjs'
LANE_SCRATCH = os.path.join(S, 'counter-mut')
REQS = os.path.join(S, 'counter-mut-results.json')


def results_path(argv):
    """One results file per invocation, so parallel groups never clobber."""
    tag = '-'.join(argv) if argv else 'all'
    safe = ''.join(c if c.isalnum() or c in '-_' else '_' for c in tag)[:120]
    return os.path.join(S, 'counter-mut-results-%s.json' % safe)

# (name, old, new, one-line description of the defect the mutant injects)
MUTATIONS = [
    ('handler-name-compare',
     "                    h == HANDLER for h in d['squashfs_handlers'])",
     "                    h.startswith('squashfs_v4') for h in d['squashfs_handlers'])",
     'handler_ok accepts any squashfs_v4* family, not exactly squashfs_v4_le'),
    ('handler-constant-widened',
     "HANDLER = 'squashfs_v4_le'",
     "HANDLER = 'squashfs_v4'",
     'the frozen handler constant itself is widened (self-consistent mutant)'),
    ('marker-equality',
     "    d['marker'] = d['mkfs_time'] == d['bytes_used']",
     "    d['marker'] = d['mkfs_time'] >= d['bytes_used']",
     'the AVM marker equality becomes an inequality (a real timestamp passes)'),
    ('bytes-used-lower-bound',
     "    d['bytes_used_sane'] = 0 < d['bytes_used'] <= len(raw)",
     "    d['bytes_used_sane'] = 0 <= d['bytes_used'] <= len(raw)",
     'bytes_used == 0 is accepted as sane'),
    ('evidence-id-recompute',
     "            d['evidence_id_ok'] = (key in ev and ev[key][0] == ev[key][1]\n"
     "                                   and ev[key][0].startswith('ev_'))",
     "            d['evidence_id_ok'] = (key in ev\n"
     "                                   and ev[key][0].startswith('ev_'))",
     'the stored evidence id is no longer compared with the recomputed one'),
    ('projection-files-key',
     "PROJECTION_KEYS = ('subject_sha256', 'files', 'chunks', 'extraction_gaps',\n"
     "                   'unpublished_entries', 'diagnostics')",
     "PROJECTION_KEYS = ('subject_sha256', 'chunks', 'extraction_gaps',\n"
     "                   'unpublished_entries', 'diagnostics')",
     'the published-file list is dropped from the projection comparison'),
    ('oracle-path-map-size',
     "        if any(s == sha and z == want_size for s, z in idx.get(strip_rel(rel), [])):",
     "        if any(s == sha for s, z in idx.get(strip_rel(rel), [])):",
     'an oracle hit ignores the published file size'),
    ('parameters-prefix-test',
     "                d['parameters_ok'] = (all(isinstance(v, int)\n"
     "                                          and not isinstance(v, bool)\n"
     "                                          for v in want_p.values())\n"
     "                                      and got_p == want_p)",
     "                d['parameters_ok'] = (all(isinstance(v, int)\n"
     "                                          and not isinstance(v, bool)\n"
     "                                          for v in want_p.values())\n"
     "                                      and got_p.get('max_depth')\n"
     "                                      == want_p.get('max_depth'))",
     'only max_depth of the frozen extraction parameters is compared'),
    ('target-constant',
     "TARGET = 4",
     "TARGET = 3",
     'the carrier target is 3 instead of the frozen 4'),
    ('receipt-first-add',
     "            d['receipt_fresh'] = bool(adds) and all(\n"
     "                a != freeze and is_ancestor(root, freeze, a) for a in adds)",
     "            d['receipt_fresh'] = bool(adds) and all(\n"
     "                is_ancestor(root, freeze, a) for a in adds)",
     'a receipt added AT the freeze commit counts as fresh'),
    ('full-history-flag',
     "    p = git(root, 'log', '-m', '--full-history', '--diff-filter=A', '--format=%H',",
     "    p = git(root, 'log', '-m', '--diff-filter=A', '--format=%H',",
     'the --full-history flag is dropped from the receipt-add scan'),
    ('unblob-version-pin',
     "    if ver != UNBLOB_VERSION:",
     "    if not ver.startswith('26.'):",
     'the unblob version pin accepts any 26.x'),
    ('sasquatch-presence-pin',
     "    sas = which_fixed('sasquatch')\n"
     "    if sas is None:\n"
     "        raise RerunEnvError('missing-extractor-dependency: sasquatch is not '\n"
     "                            'on the fixed child PATH %r' % (FIXED_PATH,))",
     "    sas = which_fixed('sasquatch')\n"
     "    if sas is None:\n"
     "        sas = '/nonexistent/sasquatch'",
     'a missing sasquatch on the fixed PATH no longer refuses the rerun'),
    ('minor-version-clause',
     "    d['version_v4'] = (d['major'], d['minor']) == (4, 0)",
     "    d['version_v4'] = d['major'] == 4",
     'the s_minor == 0 half of the frozen v4.0 clause is dropped'),
    ('score-receipt-shape',
     "                d['evidence_envelope_ok'] = not ({'counter_sha256', 'exit_code'}\n"
     "                                                 & set(env))",
     "                d['evidence_envelope_ok'] = not ({'counter_sha256'}\n"
     "                                                 & set(env))",
     'a committed receipt carrying a score exit_code is accepted as an after-receipt'),
    ('frozen-drift-rename-code',
     "            elif code in 'MDRTU':",
     "            elif code in 'MDTU':",
     'a rename (R) of a frozen path is not treated as freeze drift'),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def run_one(name, old, new, desc):
    root = os.path.join(LANE_SCRATCH, name)
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(os.path.join(root, 'tools', 'round-50'))
    os.makedirs(os.path.join(root, 'tools', 'round-27'))
    shutil.copy2(XPIN, os.path.join(root, 'tools', 'round-27', 'xpin-attribute.mjs'))
    with open(SRC, 'r', encoding='utf-8') as fh:
        base = fh.read()
    n = base.count(old)
    if n != 1:
        return {'name': name, 'status': 'anchor-error', 'anchor_count': n,
                'description': desc, 'old': old[:80]}
    mutated = base.replace(old, new)
    cpath = os.path.join(root, 'tools', 'round-50', 'c1-counter.py')
    with open(cpath, 'w', encoding='utf-8') as fh:
        fh.write(mutated)
    # syntax gate first: a mutant that does not parse is not a behaviour mutant
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
    t0 = time.time()
    started = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    proc = subprocess.run([sys.executable, '-I', '-B', 'tools/round-50/c1-counter.py',
                           '--selftest'], cwd=root, capture_output=True, text=True,
                          env=env, timeout=1800)
    dur = time.time() - t0
    out = proc.stdout or ''
    err = proc.stderr or ''
    try:
        summary = json.loads(out.strip().splitlines()[-1])
    except Exception:
        summary = None
    res = {
        'name': name,
        'status': 'ran',
        'description': desc,
        'command': 'python3 -I -B tools/round-50/c1-counter.py --selftest',
        'cwd': root,
        'exit_code': proc.returncode,
        'utc_started': started,
        'duration_s': round(dur, 1),
        'stdout_sha256': hashlib.sha256(out.encode()).hexdigest(),
        'stdout_bytes': len(out),
        'stderr_sha256': hashlib.sha256(err.encode()).hexdigest(),
        'stderr_tail': err[-600:],
        'mutant_sha256': sha256_file(cpath),
        'pristine_sha256': sha256_file(SRC),
        'verdict': 'killed' if proc.returncode != 0 else 'survived',
        'selftest_summary': summary,
    }
    return res


def main():
    only = sys.argv[1:] or None
    reqs = results_path(sys.argv[1:])
    os.makedirs(LANE_SCRATCH, exist_ok=True)
    results = []
    for name, old, new, desc in MUTATIONS:
        if only and name not in only:
            continue
        r = run_one(name, old, new, desc)
        results.append(r)
        print('%-28s %-14s exit=%s' % (r['name'], r['status'],
                                       r.get('exit_code')), flush=True)
        with open(reqs, 'w', encoding='utf-8') as fh:
            json.dump(results, fh, indent=1, sort_keys=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
