#!/usr/bin/env python3
"""R40-C1 supplementary bindings (L1-authored before the freeze; wave-1 R40C1Controls D3-D5).

The main counter (tools/round-40/c1-counter.py) scores receipts, reruns and doc presence.
This gate adds three bindings the wave-1 controls showed the counter does not enforce:

  oracle_rederived   for every carrier in carriers.json, the reader bytes AT THE FREEZE
                     (tools/round-40/sqfs-list.py, --layout avm) run on the carrier bytes
                     reproduce the frozen oracle.tsv and nonregular.tsv exactly (as row
                     sets); a trimmed or hand-edited oracle fails (R40C1Controls D5).
  sourced_new        the round-40 entry cites an S-id whose SOURCES.md row is ABSENT at
                     --base and present at --rev with the entry in its used-by cell; a
                     date string cannot satisfy it (R40C1Controls D3).
  frontier_content   PROVINCE.md at --rev holds a line starting `Round-40 frontier note`
                     that names the `## Round-40 additions to Core` heading, the entry stem,
                     and the word `supersede` (R40C1Controls D4: presence is not supersession).

Usage:
  c1-extra.py --root LANE --rev REV --freeze FREEZE --base BASE [--carrier-cache DIR] [--json-out F]
  c1-extra.py --selftest
Exit 0 all three true; 1 any false; 2 unevaluable (missing commit, carriers.json, reader).
Stdlib only; scratch under $HYAKU_SCRATCH/kaidoku-r40 (honours TMPDIR otherwise).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CARRIERS = '.ufo/waves/round-40/c1/carriers.json'
READER = 'tools/round-40/sqfs-list.py'
ENTRY = 'corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md'
STEM = '2026-10-26-r40-avm-be-squashfs-core'
HEADING = '## Round-40 additions to Core'
SID_ROW = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')


class Unevaluable(Exception):
    pass


def show(root, rev, path):
    p = subprocess.run(['git', '-C', root, 'show', f'{rev}:{path}'], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def rows(raw):
    return sorted(l for l in raw.decode('utf-8', 'replace').splitlines() if l.strip())


def scratch():
    base = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'kaidoku-r40')
    try:
        os.makedirs(base, exist_ok=True)
    except OSError:
        base = None
    return tempfile.mkdtemp(prefix='c1-extra.', dir=base)


def oracle_rederived(root, rev, freeze, cache, work):
    spec_raw = show(root, freeze, CARRIERS)
    reader = show(root, freeze, READER)
    if spec_raw is None or reader is None:
        raise Unevaluable('carriers.json or reader absent at freeze')
    rp = os.path.join(work, 'sqfs-list.py')
    open(rp, 'wb').write(reader)
    detail = {}
    for c in json.loads(spec_raw).get('carriers') or []:
        cid, pin = c.get('id'), (c.get('sha256') or '').lower()
        if c.get('path'):
            raw = show(root, rev, c['path'])
        else:
            fp = os.path.join(cache or '', pin + '.bin')
            raw = open(fp, 'rb').read() if cache and os.path.isfile(fp) else None
        if raw is None or hashlib.sha256(raw).hexdigest() != pin:
            detail[cid] = 'carrier bytes absent or pin mismatch'
            continue
        img = os.path.join(work, '%s.img' % cid)
        open(img, 'wb').write(raw)
        f, n = img + '.files', img + '.nonreg'
        p = subprocess.run([sys.executable, '-I', '-B', rp, img, '--layout', 'avm',
                            '--files', f, '--nonregular', n], capture_output=True)
        if p.returncode != 0:
            detail[cid] = 'reader exit %d' % p.returncode
            continue
        fo, no = show(root, rev, c.get('oracle', '')), show(root, rev, c.get('nonregular', ''))
        if fo is None or no is None:
            detail[cid] = 'oracle/nonregular absent at rev'
            continue
        ok_f = rows(open(f, 'rb').read()) == rows(fo)
        ok_n = rows(open(n, 'rb').read()) == rows(no)
        detail[cid] = 'ok' if ok_f and ok_n else 'mismatch files=%s nonregular=%s' % (ok_f, ok_n)
    good = bool(detail) and all(v == 'ok' for v in detail.values())
    return good, detail


def sids(raw):
    return {m.group(1): l for l in (raw or b'').decode('utf-8', 'replace').splitlines()
            for m in [SID_ROW.match(l)] if m}


def sourced_new(root, rev, base):
    entry = show(root, rev, ENTRY)
    if entry is None:
        return False, 'entry absent'
    cited = set(re.findall(r'\bS\d{3,}\b', '\n'.join(
        l for l in entry.decode('utf-8', 'replace').splitlines() if l.lower().startswith('source'))))
    at_base, at_rev = sids(show(root, base, 'corpus/SOURCES.md')), sids(show(root, rev, 'corpus/SOURCES.md'))
    new = sorted(s for s in cited if s not in at_base and s in at_rev
                 and (ENTRY in at_rev[s] or STEM in at_rev[s]))
    return bool(new), {'cited': sorted(cited), 'new_with_used_by': new}


def frontier_content(root, rev):
    prov = show(root, rev, 'PROVINCE.md')
    if prov is None:
        return False, 'PROVINCE.md absent'
    for l in prov.decode('utf-8', 'replace').splitlines():
        if l.startswith('Round-40 frontier note') and HEADING in l and STEM in l \
                and 'supersede' in l.lower():
            return True, l[:160]
    return False, 'no qualifying Round-40 frontier note line'


def measure(root, rev, freeze, base, cache):
    for r in (rev, freeze, base):
        if subprocess.run(['git', '-C', root, 'cat-file', '-e', f'{r}^{{commit}}'],
                          capture_output=True).returncode:
            raise Unevaluable('not a commit: %s' % r)
    work = scratch()
    try:
        o, od = oracle_rederived(root, rev, freeze, cache, work)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    s, sd = sourced_new(root, rev, base)
    f, fd = frontier_content(root, rev)
    res = {'revision': rev, 'freeze': freeze, 'base': base,
           'bindings': {'oracle_rederived': o, 'sourced_new': s, 'frontier_content': f},
           'detail': {'oracle_rederived': od, 'sourced_new': sd, 'frontier_content': fd}}
    res['met'] = o and s and f
    return res


def selftest():
    cases = []
    tmp = tempfile.mkdtemp(dir=os.environ.get('TMPDIR'))
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        gen = os.path.join(here, 'gen-squashfs.py')
        reader = os.path.join(here, 'sqfs-list.py')
        tree = os.path.join(tmp, 'tree')
        os.makedirs(os.path.join(tree, 'a'))
        open(os.path.join(tree, 'a', 'f'), 'wb').write(b'hello\n' * 50)
        open(os.path.join(tree, 'g'), 'wb').write(b'x' * 7000)
        os.symlink('../g', os.path.join(tree, 'a', 'l'))
        img = os.path.join(tmp, 'c.sqsh')
        subprocess.run([sys.executable, '-I', '-B', gen, tree, img, '--endian', 'avm-genuine',
                        '--comp', 'gzip'], check=True, capture_output=True)
        subprocess.run([sys.executable, '-I', '-B', reader, img, '--layout', 'avm', '--files',
                        img + '.f', '--nonregular', img + '.n'], check=True, capture_output=True)
        pin = hashlib.sha256(open(img, 'rb').read()).hexdigest()
        D = os.path.join(tmp, 'repo')
        os.makedirs(D)
        g = lambda *a: subprocess.run(['git', '-C', D, *a], check=True, capture_output=True,
                                      text=True).stdout.strip()
        g('init', '-q')
        assert os.path.realpath(g('rev-parse', '--show-toplevel')) == os.path.realpath(D)

        def put(rel, data):
            p = os.path.join(D, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, 'wb').write(data if isinstance(data, bytes) else data.encode())

        def commit(msg):
            g('add', '-A')
            g('-c', 'user.name=fx', '-c', 'user.email=fx@fx', 'commit', '-q', '-m', msg)
            return g('rev-parse', 'HEAD')

        put('corpus/SOURCES.md', '| id | x |\n|---|---|\n| S001 | old |\n')
        put('PROVINCE.md', '# p\n')
        base = commit('base')
        os.makedirs(os.path.join(D, 'tools', 'round-40'))
        shutil.copy(reader, os.path.join(D, READER))
        put('c/C.sqsh', open(img, 'rb').read())
        put('c/oracle.tsv', open(img + '.f', 'rb').read())
        put('c/nonregular.tsv', open(img + '.n', 'rb').read())
        put(CARRIERS, json.dumps({'carriers': [{'id': 'L1', 'path': 'c/C.sqsh', 'sha256': pin,
                                                'oracle': 'c/oracle.tsv',
                                                'nonregular': 'c/nonregular.tsv'}]}))
        freeze = commit('freeze')
        put(ENTRY, 'source: S002\n')
        put('corpus/SOURCES.md', '| id | x |\n|---|---|\n| S001 | old |\n| S002 | new %s |\n' % ENTRY)
        put('PROVINCE.md', '# p\n%s\nRound-40 frontier note: supersedes AVM; see %s, %s.\n'
            % (HEADING, HEADING, STEM))
        good = commit('landing')

        def case(name, rev, want, binding=None):
            r = measure(D, rev, freeze, base, None)
            got = r['met'] if binding is None else r['bindings'][binding]
            cases.append((name, got == want))

        case('green', good, True)
        case('base-has-nothing', freeze, False)
        put('c/oracle.tsv', b''.join(open(img + '.f', 'rb').read().splitlines(True)[:-1]))
        trimmed = commit('trim oracle')
        case('trimmed-oracle', trimmed, False, 'oracle_rederived')
        put('c/oracle.tsv', open(img + '.f', 'rb').read())
        put(ENTRY, 'source: S001\n')
        put('corpus/SOURCES.md', '| id | x |\n|---|---|\n| S001 | old %s |\n' % ENTRY)
        old = commit('old id re-used')
        case('old-sid-with-used-by', old, False, 'sourced_new')
        put(ENTRY, 'source: S002\n')
        put('corpus/SOURCES.md', '| id | x |\n|---|---|\n| S001 | old |\n| S002 | new no use |\n')
        nouse = commit('new id without used-by')
        case('new-sid-no-used-by', nouse, False, 'sourced_new')
        put('corpus/SOURCES.md', '| id | x |\n|---|---|\n| S001 | old |\n| S002 | new %s |\n' % ENTRY)
        put('PROVINCE.md', '# p\nRound-40 frontier note: AVM stays here; %s\n' % STEM)
        pres = commit('presence-only note')
        case('presence-only-frontier-note', pres, False, 'frontier_content')
        try:
            measure(D, 'deadbeef', freeze, base, None)
            cases.append(('bad-rev-unevaluable', False))
        except Unevaluable:
            cases.append(('bad-rev-unevaluable', True))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for name, ok in cases:
        print('%s\t%s' % ('PASS' if ok else 'FAIL', name))
    p = sum(1 for _, ok in cases if ok)
    print('SELFTEST cases=%d pass=%d fail=%d' % (len(cases), p, len(cases) - p))
    return 0 if p == len(cases) else 1


def main():
    ap = argparse.ArgumentParser()
    for k in ('--root', '--rev', '--freeze', '--base', '--carrier-cache', '--json-out'):
        ap.add_argument(k)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.root and a.rev and a.freeze and a.base):
        print('usage: --root --rev --freeze --base required', file=sys.stderr)
        return 2
    try:
        res = measure(a.root, a.rev, a.freeze, a.base, a.carrier_cache)
        res['exit_code'] = 0 if res['met'] else 1
    except Unevaluable as e:
        res = {'unevaluable': str(e), 'exit_code': 2}
    res['argv'] = sys.argv
    print(json.dumps(res, indent=1, sort_keys=True))
    if a.json_out:
        json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
    return res['exit_code']


if __name__ == '__main__':
    sys.exit(main())
