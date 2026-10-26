#!/usr/bin/env python3
"""Two controls that skip the claimed work, scored by a round-41-shaped C1 counter.

`relabel` -- the freeze pins the round-40 carriers V1/V2/L1/L2 as V3/V4/L3/L4 (same
bytes, same oracle/non-regular tables), and the post-freeze commit copies the
round-40 after-receipts with `parameters.output_directory` rewritten into a
`/kaidoku-r41/` scratch segment and the evidence id re-minted with the frozen
tools/round-27/xpin-attribute.mjs. No REA run produces any of the four receipts.
The drafted predicate scores carriers_matched 4/4.

`carve` -- a fixture carrier whose squashfs chunk starts at offset 8192 (the shape
REA produces for any carved member). The c1-counter-exact-match.diff helper
`extract_rel` drops only the FIRST `<...>_extract` component, so the receipt paths
(`firmware.bin_extract/8192-<end>.squashfs_v4_be_extract/<rel>`) never equal the
oracle rows (relative to the chunk extract root). The drafted sentence "exact path
relative to the chunk's extract root" is not implemented by the named prototype.

Usage:
  attack-controls.py {relabel,carve} --lane LANE --base REV --work DIR [--cache DIR]
                     [--package PKG] [--diff FILE] [--keep]

Writes only under --work (and --cache). Honours TMPDIR. Exit 0 iff the control
scored exactly as this script predicts (relabel: 4/4; carve: L4 fails only the
path clauses).
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
PKG_DEFAULT = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
R40 = '.ufo/waves/round-40/c1/carriers.json'
DIFF_DEFAULT = (LANE + '/.ufo/waves/round-40/w2/artifacts/R40W2C1Refreeze/'
                'c1-counter-exact-match.diff')
MAP = {'V1': 'V3', 'V2': 'V4', 'L1': 'L3', 'L2': 'L4'}
COUNTER = 'tools/round-40/c1-counter.py'


def run(argv, cwd=None, env=None, check=True):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, env=env, text=True)
    if check and p.returncode != 0:
        sys.stderr.write('FAILED %r\n%s\n%s' % (argv, p.stdout[-2000:], p.stderr[-2000:]))
        raise SystemExit(3)
    return p


def sha(b):
    return hashlib.sha256(b).hexdigest()


def clone(lane, base, work):
    d = os.path.join(work, 'lane')
    if os.path.isdir(d):
        shutil.rmtree(d)
    run(['git', 'clone', '-q', '--shared', lane, d])
    top = run(['git', '-C', d, 'rev-parse', '--show-toplevel']).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise SystemExit('clone toplevel %r != %r' % (top, d))
    run(['git', '-C', d, 'checkout', '-q', base])
    return d


def commit(repo, msg):
    run(['git', '-C', repo, 'add', '-A'])
    run(['git', '-C', repo, '-c', 'user.name=fx', '-c', 'user.email=fx@fx',
         'commit', '-q', '-m', msg])
    return run(['git', '-C', repo, 'rev-parse', 'HEAD']).stdout.strip()


def patch_counter(repo, diff):
    run(['git', '-C', repo, 'apply', diff])
    p = os.path.join(repo, COUNTER)
    s = open(p).read()
    subs = [
        ("CARRIERS = '.ufo/waves/round-40/c1/carriers.json'",
         "CARRIERS = '.ufo/waves/round-41/c1/carriers.json'"),
        ("GAPRULE = '.ufo/waves/round-40/c1/gap-rule.json'",
         "GAPRULE = '.ufo/waves/round-41/c1/gap-rule.json'"),
        ("AFTERDIR = 'corpus/evidence/round-40/c1'",
         "AFTERDIR = 'corpus/evidence/round-41/c1'"),
        ("IDS = ('V1', 'V2', 'L1', 'L2')", "IDS = ('V3', 'V4', 'L3', 'L4')"),
        ("PROV_SEGMENT = '/kaidoku-r40/'", "PROV_SEGMENT = '/kaidoku-r41/'"),
    ]
    for a, b in subs:
        if s.count(a) != 1:
            raise SystemExit('counter constant not found once: %r' % (a,))
        s = s.replace(a, b)
    open(p, 'w').write(s)


def build_freeze(repo, lane, mode, work):
    spec0 = json.load(open(os.path.join(lane, R40)))
    os.makedirs(os.path.join(repo, '.ufo/waves/round-41/c1'), exist_ok=True)
    spec = {'claim': 'R41-C1', 'target': 4, 'projection': 'plus-extractor',
            'rea_parameters': {'max_depth': 1},
            'prior_pins': [c['sha256'] for c in spec0['carriers']],
            'carriers': []}
    l2 = os.path.join(lane, 'corpus/evidence/round-40/c1/L2/carrier.sqsh')
    for c in spec0['carriers']:
        nid = MAP[c['id']]
        d = 'corpus/evidence/round-41/c1/' + nid
        os.makedirs(os.path.join(repo, d), exist_ok=True)
        nc = {'id': nid, 'sha256': c['sha256'], 'kind': c.get('kind'),
              'oracle': d + '/oracle.tsv', 'nonregular': d + '/nonregular.tsv'}
        if 'external' in c:
            nc['external'] = dict(c['external'])
        else:
            p = d + '/carrier.sqsh'
            if mode == 'carve' and nid == 'L4':
                body = b'\0' * 8192 + open(l2, 'rb').read()
                open(os.path.join(repo, p), 'wb').write(body)
                nc['sha256'] = sha(body)
            else:
                shutil.copyfile(os.path.join(lane, c['path']),
                                os.path.join(repo, p))
            nc['path'] = p
        shutil.copyfile(os.path.join(lane, c['oracle']),
                        os.path.join(repo, nc['oracle']))
        shutil.copyfile(os.path.join(lane, c['nonregular']),
                        os.path.join(repo, nc['nonregular']))
        spec['carriers'].append(nc)
    json.dump(spec, open(os.path.join(
        repo, '.ufo/waves/round-41/c1/carriers.json'), 'w'), indent=1)
    shutil.copyfile(os.path.join(lane, '.ufo/waves/round-40/c1/gap-rule.json'),
                    os.path.join(repo, '.ufo/waves/round-41/c1/gap-rule.json'))
    return spec


def write_receipts(repo, lane, spec, mode, work, pkg, unblob):
    fz = run(['git', '-C', repo, 'rev-parse', 'HEAD']).stdout.strip()
    xpin = os.path.join(work, 'xpin.mjs')
    open(xpin, 'wb').write(run(['git', '-C', repo, 'show',
                                fz + ':tools/round-27/xpin-attribute.mjs']).stdout.encode())
    env = dict(os.environ)
    env['TMPDIR'] = work
    if unblob:
        env['REA_UNBLOB_COMMAND'] = unblob
    wrapped = []
    for c in spec['carriers']:
        cid = c['id']
        outdir = os.path.join(work, 'kaidoku-r41', mode, cid, 'extract')
        if mode == 'carve' and cid == 'L4':
            inp = os.path.join(work, 'carve-L4.bin')
            open(inp, 'wb').write(open(os.path.join(
                repo, c['path']), 'rb').read())
            os.makedirs(os.path.dirname(outdir), exist_ok=True)
            p = run(['npx', '-y', 'rea-agents@6.5.0', 'extract-firmware',
                     '--format', 'json', '--full-output', '--max-depth', '1',
                     inp, outdir], cwd=work, env=env)
            data = json.loads(p.stdout)['data']
        else:
            src = 'corpus/evidence/round-40/c1/%s/after.json' % {
                v: k for k, v in MAP.items()}[cid]
            data = json.load(open(os.path.join(lane, src)))
            data['parameters']['output_directory'] = outdir
        w = os.path.join(work, 'wrapped-%s.json' % cid)
        json.dump({'data': data}, open(w, 'w'))
        wrapped.append((cid, w))
    p = run(['node', xpin, '--pkg65', pkg, '--pkg67', pkg] +
            [w for _, w in wrapped], env=env)
    ids = {}
    for line in p.stdout.splitlines():
        f = line.split('\t')
        ids[os.path.basename(f[0])[8:-5]] = f[2]
    for cid, w in wrapped:
        data = json.load(open(w))['data']
        data['evidence_id'] = ids[cid]
        d = os.path.join(repo, 'corpus/evidence/round-41/c1', cid)
        os.makedirs(d, exist_ok=True)
        json.dump(data, open(os.path.join(d, 'after.json'), 'w'), indent=1)
    return fz


def score(repo, work, fz, pkg, cache):
    rev = run(['git', '-C', repo, 'rev-parse', 'HEAD']).stdout.strip()
    out = os.path.join(work, 'score.json')
    env = dict(os.environ)
    env['TMPDIR'] = work
    run([sys.executable, os.path.join(repo, COUNTER), '--root', repo,
         '--rev', rev, '--freeze', fz, '--pkg65', pkg,
         '--carrier-cache', cache, '--json-out', out], env=env, check=False)
    return json.load(open(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=('relabel', 'carve'))
    ap.add_argument('--lane', default=LANE)
    ap.add_argument('--base', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--cache', required=True)
    ap.add_argument('--package', default=PKG_DEFAULT)
    ap.add_argument('--diff', default=DIFF_DEFAULT)
    ap.add_argument('--keep', action='store_true')
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    os.makedirs(work, exist_ok=True)
    if not os.path.isdir(a.cache):
        os.makedirs(a.cache)
    repo = clone(a.lane, a.base, work)
    patch_counter(repo, a.diff)
    spec = build_freeze(repo, a.lane, a.mode, work)
    commit(repo, 'freeze: control carriers')
    if a.mode == 'relabel':
        env = dict(os.environ)
        env['TMPDIR'] = work
        run([sys.executable, os.path.join(repo, 'tools/round-40/fetch-vendor.py'),
             '--root', repo, '--rev', a.base, '--cache', a.cache],
            env=env)
    fz = write_receipts(repo, a.lane, spec, a.mode, work, a.package,
                        os.path.expanduser('~/.local/bin/unblob'))
    commit(repo, 'receipts: control')
    res = score(repo, work, fz, a.package, a.cache)
    per = {k: {c: v.get(c) for c in (
        'matched', 'carrier_pin_ok', 'layout_ok', 'oracle_hits', 'oracle_files',
        'published_files', 'oracle_hits_ok', 'gaps_ok',
        'nonregular_unpublished_ok', 'receipt_fresh', 'run_provenance_ok',
        'evidence_id_ok', 'projection_ok')}
        for k, v in res['carriers'].items()}
    print(json.dumps({'mode': a.mode, 'freeze': fz,
                      'revision': res.get('revision'),
                      'carriers_matched': res['carriers_matched'],
                      'target': res['target'], 'per_carrier': per},
                     indent=1, sort_keys=True))
    ok = (res['carriers_matched'] == 4) if a.mode == 'relabel' else (
        res['carriers_matched'] == 3
        and per['L4']['oracle_hits'] == 0
        and per['L4']['matched'] is False)
    print('CONTROL_AS_PREDICTED', ok)
    if not a.keep:
        shutil.rmtree(work, ignore_errors=True)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
