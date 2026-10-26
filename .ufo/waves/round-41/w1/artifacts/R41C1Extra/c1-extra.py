#!/usr/bin/env python3
"""R41-C1 supplementary bindings (round-41 port of tools/round-40/c1-extra.py at 49096c7e).

The main counter (tools/round-41/c1-counter.py) scores receipts, reruns and doc presence.
This gate adds the three bindings the wave-1 controls showed the counter does not enforce:

  oracle_rederived   for every carrier in .ufo/waves/round-41/c1/carriers.json, the reader
                     bytes AT THE FREEZE (tools/round-41/sqfs-list.py, --layout avm) run on
                     the carrier bytes reproduce the frozen oracle.tsv and nonregular.tsv
                     exactly (as row sets); a trimmed or hand-edited oracle fails.
  sourced_new        the round-41 entry cites an S-id whose corpus/SOURCES.md row is ABSENT
                     at --base and present at --rev with the entry in its used-by cell; a
                     date string cannot satisfy it, nor can an id that already exists at the
                     base (S126 is the highest row at 49096c7e).
  frontier_content   PROVINCE.md at --rev holds a line starting `Round-41 frontier note` that
                     names `## Round-41 additions to Core`, the round-41 entry stem, a
                     supersede verb, AND the round-40 `measured, not promoted` record phrase
                     (round-41 addition to the round-40 check: naming a heading is not
                     superseding the round-40 honest-stop record, and a `Round-40 frontier
                     note` line is not a round-41 note).

Usage:
  c1-extra.py --root LANE --rev REV --freeze FREEZE --base BASE [--carrier-cache DIR]
              [--json-out F] [--work DIR]
  c1-extra.py --selftest [--tools DIR] [--work DIR]
Exit 0 all three true; 1 any false; 2 unevaluable (missing commit, carriers.json, reader) or
bad selftest environment.
Stdlib only; scratch under $HYAKU_SCRATCH/kaidoku-r41 (honours TMPDIR / --work otherwise).
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

CARRIERS = '.ufo/waves/round-41/c1/carriers.json'
READER = 'tools/round-41/sqfs-list.py'
ENTRY = 'corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md'
STEM = '2026-10-26-r41-avm-be-squashfs-core'
HEADING = '## Round-41 additions to Core'
NOTE = 'Round-41 frontier note'
R40_RECORD = re.compile(r'measured[,\s-]+not[,\s-]+promoted')
SID_ROW = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')


class Unevaluable(Exception):
    pass


def show(root, rev, path):
    p = subprocess.run(['git', '-C', root, 'show', f'{rev}:{path}'], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def rows(raw):
    return sorted(l for l in raw.decode('utf-8', 'replace').splitlines() if l.strip())


def scratch(work):
    if work:
        os.makedirs(work, exist_ok=True)
        return tempfile.mkdtemp(prefix='c1-extra.', dir=work)
    base = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'kaidoku-r41')
    try:
        os.makedirs(base, exist_ok=True)
    except OSError:
        base = None
    return tempfile.mkdtemp(prefix='c1-extra.', dir=base)


def oracle_rederived(root, rev, freeze, cache, work):
    spec_raw = show(root, freeze, CARRIERS)
    reader = show(root, freeze, READER)
    if spec_raw is None or reader is None:
        missing = [p for p, r in ((CARRIERS, spec_raw), (READER, reader)) if r is None]
        raise Unevaluable('absent at freeze: %s' % ', '.join(missing))
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
        return False, {'error': 'entry absent'}
    cited = sorted(set(re.findall(r'\bS\d{3,}\b', '\n'.join(
        l for l in entry.decode('utf-8', 'replace').splitlines() if l.lower().startswith('source')))))
    at_base, at_rev = sids(show(root, base, 'corpus/SOURCES.md')), sids(show(root, rev, 'corpus/SOURCES.md'))
    new = [s for s in cited if s not in at_base and s in at_rev
           and (ENTRY in at_rev[s] or STEM in at_rev[s])]
    return bool(new), {'cited': cited, 'at_base': [s for s in cited if s in at_base],
                       'new_with_used_by': new}


def note_verdict(line):
    flat = line.replace('*', '').lower()
    v = {'line': line[:200],
         'names_heading': HEADING in line,
         'names_stem': STEM in line,
         'supersedes': 'supersede' in flat,
         'names_r40_record': bool(R40_RECORD.search(flat))}
    v['ok'] = all(v[k] for k in ('names_heading', 'names_stem', 'supersedes', 'names_r40_record'))
    return v


def frontier_content(root, rev):
    prov = show(root, rev, 'PROVINCE.md')
    if prov is None:
        return False, {'error': 'PROVINCE.md absent'}
    near = []
    for l in prov.decode('utf-8', 'replace').splitlines():
        if not l.startswith(NOTE):
            continue
        v = note_verdict(l)
        if v['ok']:
            return True, v
        near.append(v)
    return False, (near[0] if near else {'error': 'no line starting %r' % NOTE})


def measure(root, rev, freeze, base, cache, work=None):
    for r in (rev, freeze, base):
        if subprocess.run(['git', '-C', root, 'cat-file', '-e', f'{r}^{{commit}}'],
                          capture_output=True).returncode:
            raise Unevaluable('not a commit: %s' % r)
    w = scratch(work)
    try:
        o, od = oracle_rederived(root, rev, freeze, cache, w)
    finally:
        shutil.rmtree(w, ignore_errors=True)
    s, sd = sourced_new(root, rev, base)
    f, fd = frontier_content(root, rev)
    res = {'revision': rev, 'freeze': freeze, 'base': base,
           'bindings': {'oracle_rederived': o, 'sourced_new': s, 'frontier_content': f},
           'detail': {'oracle_rederived': od, 'sourced_new': sd, 'frontier_content': fd}}
    res['met'] = o and s and f
    return res


def tool_dir(explicit, root):
    cands = []
    if explicit:
        cands.append(explicit)
    cands.append(os.path.dirname(os.path.abspath(__file__)))
    if root:
        cands += [os.path.join(root, 'tools', 'round-41'), os.path.join(root, 'tools', 'round-40')]
    for c in cands:
        if os.path.isfile(os.path.join(c, 'gen-squashfs.py')) \
                and os.path.isfile(os.path.join(c, 'sqfs-list.py')):
            return c
    return None


def selftest(tools=None, root=None, work=None):
    tdir = tool_dir(tools, root)
    if tdir is None:
        print('SELFTEST tool_dir_missing: need --tools DIR holding gen-squashfs.py and sqfs-list.py',
              file=sys.stderr)
        return 2
    cases = []
    parent = work or os.environ.get('TMPDIR') or os.environ.get('HYAKU_SCRATCH')
    if parent:
        os.makedirs(parent, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix='c1-extra-selftest.', dir=parent)
    try:
        gen = os.path.join(tdir, 'gen-squashfs.py')
        reader = os.path.join(tdir, 'sqfs-list.py')
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

        # base mirrors 49096c7e: S126 is the highest row, PROVINCE has no round-41 heading.
        put('corpus/SOURCES.md', '| id | x |\n|---|---|\n| S001 | old |\n| S126 | highest at base |\n')
        put('PROVINCE.md', '# p\n')
        base = commit('base')
        put(READER, open(reader, 'rb').read())
        put('c/C.sqsh', open(img, 'rb').read())
        put('c/oracle.tsv', open(img + '.f', 'rb').read())
        put('c/nonregular.tsv', open(img + '.n', 'rb').read())
        put(CARRIERS, json.dumps({'carriers': [{'id': 'L3', 'path': 'c/C.sqsh', 'sha256': pin,
                                                'oracle': 'c/oracle.tsv',
                                                'nonregular': 'c/nonregular.tsv'}]}))
        freeze = commit('freeze')
        green_note = ('# p\n%s\nRound-41 frontier note, 2026-10-26: the round-40 `measured, not '
                      'promoted` record (`## Round-40 measured, not promoted (R40-C1 honest stop)`) '
                      'is superseded; AVM-BE is Core — see %s (`%s`).\n' % (HEADING, HEADING, STEM))
        put(ENTRY, 'source: S127\n')
        put('corpus/SOURCES.md', '| id | x |\n|---|---|\n| S001 | old |\n'
                                 '| S126 | highest at base |\n| S127 | new %s |\n' % ENTRY)
        put('PROVINCE.md', green_note)
        good = commit('landing')

        def case(name, rev, want, binding=None, fz=None, cache=None):
            r = measure(D, rev, fz or freeze, base, cache, work=tmp)
            got = r['met'] if binding is None else r['bindings'][binding]
            cases.append((name, got == want))

        case('green', good, True)
        case('base-has-nothing', freeze, False)
        put('c/oracle.tsv', b''.join(open(img + '.f', 'rb').read().splitlines(True)[:-1]))
        trimmed = commit('trim oracle')
        case('trimmed-oracle', trimmed, False, 'oracle_rederived')
        rows_f = open(img + '.f', 'rb').read().decode().splitlines()
        edited = list(rows_f)
        rel, sha, size = edited[0].split('\t')
        edited[0] = '\t'.join((rel, ('0' if sha[0] != '0' else '1') + sha[1:], size))
        put('c/oracle.tsv', '\n'.join(edited) + '\n')
        shabad = commit('oracle sha256 edited, row count kept')
        case('edited-oracle-same-count', shabad, False, 'oracle_rederived')
        put('c/oracle.tsv', open(img + '.f', 'rb').read())
        put('c/nonregular.tsv', open(img + '.n', 'rb').read()
            + b'fabricated/link\tsymlink\telsewhere\n')
        extra_nr = commit('fabricated nonregular row')
        case('extra-nonregular-row', extra_nr, False, 'oracle_rederived')
        put('c/nonregular.tsv', open(img + '.n', 'rb').read())
        # marker-only body (`--endian avm`): a genuine `sqsh` superblock with big-endian block
        # lengths. Only the `--layout avm` reader refuses it; `auto` reads it as standard BE.
        img2 = os.path.join(tmp, 'm.sqsh')
        subprocess.run([sys.executable, '-I', '-B', gen, tree, img2, '--endian', 'avm',
                        '--comp', 'gzip'], check=True, capture_output=True)
        subprocess.run([sys.executable, '-I', '-B', reader, img2, '--layout', 'auto', '--files',
                        img2 + '.f', '--nonregular', img2 + '.n'], check=True, capture_output=True)
        put('c2/M.sqsh', open(img2, 'rb').read())
        put('c2/oracle.tsv', open(img2 + '.f', 'rb').read())
        put('c2/nonregular.tsv', open(img2 + '.n', 'rb').read())
        put(CARRIERS, json.dumps({'carriers': [
            {'id': 'L3', 'path': 'c/C.sqsh', 'sha256': pin, 'oracle': 'c/oracle.tsv',
             'nonregular': 'c/nonregular.tsv'},
            {'id': 'M', 'path': 'c2/M.sqsh', 'sha256': hashlib.sha256(open(img2, 'rb').read()).hexdigest(),
             'oracle': 'c2/oracle.tsv', 'nonregular': 'c2/nonregular.tsv'}]}))
        marker_freeze = commit('marker-only carrier added')
        case('marker-only-body-refused', marker_freeze, False, 'oracle_rederived', fz=marker_freeze)
        # external carrier: bytes come from --carrier-cache and MUST hash to the pin. The cache
        # holds a different, well-formed image under the pinned name, with that image's own oracle.
        tree3 = os.path.join(tmp, 'tree3')
        os.makedirs(os.path.join(tree3, 'b'))
        open(os.path.join(tree3, 'b', 'z'), 'wb').write(b'other\n' * 300)
        img3 = os.path.join(tmp, 'o.sqsh')
        subprocess.run([sys.executable, '-I', '-B', gen, tree3, img3, '--endian', 'avm-genuine',
                        '--comp', 'xz'], check=True, capture_output=True)
        subprocess.run([sys.executable, '-I', '-B', reader, img3, '--layout', 'avm', '--files',
                        img3 + '.f', '--nonregular', img3 + '.n'], check=True, capture_output=True)
        put('c3/oracle.tsv', open(img3 + '.f', 'rb').read())
        put('c3/nonregular.tsv', open(img3 + '.n', 'rb').read())
        put(CARRIERS, json.dumps({'carriers': [
            {'id': 'X', 'sha256': pin, 'oracle': 'c3/oracle.tsv', 'nonregular': 'c3/nonregular.tsv'}]}))
        ext_freeze = commit('external carrier pinned to the L3 bytes')
        cache = os.path.join(tmp, 'cache')
        os.makedirs(cache, exist_ok=True)
        open(os.path.join(cache, pin + '.bin'), 'wb').write(open(img3, 'rb').read())
        case('external-carrier-pin-mismatch', ext_freeze, False, 'oracle_rederived', fz=ext_freeze,
             cache=cache)
        os.remove(os.path.join(cache, pin + '.bin'))
        case('external-carrier-missing-cache', ext_freeze, False, 'oracle_rederived', fz=ext_freeze,
             cache=cache)
        put(ENTRY, 'source: S001\n')
        put('corpus/SOURCES.md', '| id | x |\n|---|---|\n| S126 | highest at base |\n'
                                 '| S001 | old %s |\n| S127 | new %s |\n' % (ENTRY, ENTRY))
        old = commit('old id re-used')
        case('old-sid-with-used-by', old, False, 'sourced_new')
        put(ENTRY, 'source: S126\n')
        used = commit('base-highest-sid-reused')
        case('base-sid-s126-with-used-by', used, False, 'sourced_new')
        put(ENTRY, 'source: S127\n')
        put('corpus/SOURCES.md', '| id | x |\n|---|---|\n| S126 | highest at base |\n'
                                 '| S127 | new no use |\n')
        nouse = commit('new id without used-by')
        case('new-sid-no-used-by', nouse, False, 'sourced_new')
        put('corpus/SOURCES.md', '| id | x |\n|---|---|\n| S126 | highest at base |\n'
                                 '| S127 | new %s |\n' % ENTRY)
        put('PROVINCE.md', '# p\nRound-41 frontier note: the round-40 measured, not promoted '
                           'record stays; see %s, %s.\n' % (HEADING, STEM))
        pres = commit('presence-only note')
        case('presence-only-frontier-note', pres, False, 'frontier_content')
        put('PROVINCE.md', '# p\nRound-40 frontier note: the round-40 measured, not promoted '
                           'record is superseded; see %s, %s.\n' % (HEADING, STEM))
        r40 = commit('round-40 note only')
        case('round-40-note-names-r41-heading', r40, False, 'frontier_content')
        put('PROVINCE.md', '# p\nRound-41 frontier note: the round-40 measured, not promoted '
                           'record is superseded; see ## round-41 additions to core, %s.\n' % STEM)
        miscase = commit('miscased heading')
        case('note-miscases-heading', miscase, False, 'frontier_content')
        put('PROVINCE.md', '# p\nRound-41 frontier note: AVM-BE supersedes the round-39 AVM '
                           'sentence; see %s, %s.\n' % (HEADING, STEM))
        norec = commit('r41 note omits r40 record')
        case('r41-note-omits-r40-record', norec, False, 'frontier_content')
        put('PROVINCE.md', green_note)
        restored = commit('green note restored')
        case('green-after-restore', restored, True)
        try:
            measure(D, 'deadbeef', freeze, base, None, work=tmp)
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
    for k in ('--root', '--rev', '--freeze', '--base', '--carrier-cache', '--json-out',
              '--work', '--tools'):
        ap.add_argument(k)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.tools, a.root, a.work)
    if not (a.root and a.rev and a.freeze and a.base):
        print('usage: --root --rev --freeze --base required', file=sys.stderr)
        return 2
    try:
        res = measure(a.root, a.rev, a.freeze, a.base, a.carrier_cache, a.work)
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
