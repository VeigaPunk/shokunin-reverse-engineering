#!/usr/bin/env python3
"""R41C1Extra evidence: WHICH sub-check each NEW round-41 red case trips.

The selftest reports PASS/FAIL per case; this driver rebuilds the same fixture repo and
prints the binding detail, so the two new red classes (an S-id already present at the base,
and a frontier note that does not supersede the round-40 `measured, not promoted` record)
are shown failing for the intended reason rather than incidentally.

Usage: probe-red-cases.py TOOLS_DIR OUT.json    (run with TMPDIR inside the seat scratch)
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('c1x', os.path.join(here, 'c1-extra.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

tools, out = sys.argv[1], sys.argv[2]
tmp = tempfile.mkdtemp(prefix='red-cases.', dir=os.environ.get('TMPDIR'))
try:
    tree = os.path.join(tmp, 'tree')
    os.makedirs(os.path.join(tree, 'a'))
    open(os.path.join(tree, 'a', 'f'), 'wb').write(b'hello\n' * 50)
    open(os.path.join(tree, 'g'), 'wb').write(b'x' * 7000)
    os.symlink('../g', os.path.join(tree, 'a', 'l'))
    img = os.path.join(tmp, 'c.sqsh')
    subprocess.run([sys.executable, '-I', '-B', os.path.join(tools, 'gen-squashfs.py'), tree, img,
                    '--endian', 'avm-genuine', '--comp', 'gzip'], check=True, capture_output=True)
    subprocess.run([sys.executable, '-I', '-B', os.path.join(tools, 'sqfs-list.py'), img,
                    '--layout', 'avm', '--files', img + '.f', '--nonregular', img + '.n'],
                   check=True, capture_output=True)
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

    put('corpus/SOURCES.md', '| id | x |\n|---|---|\n| S001 | old |\n| S126 | highest at base |\n')
    put('PROVINCE.md', '# p\n')
    base = commit('base')
    put(m.READER, open(os.path.join(tools, 'sqfs-list.py'), 'rb').read())
    put('c/C.sqsh', open(img, 'rb').read())
    put('c/oracle.tsv', open(img + '.f', 'rb').read())
    put('c/nonregular.tsv', open(img + '.n', 'rb').read())
    put(m.CARRIERS, json.dumps({'carriers': [{'id': 'L3', 'path': 'c/C.sqsh', 'sha256': pin,
                                              'oracle': 'c/oracle.tsv',
                                              'nonregular': 'c/nonregular.tsv'}]}))
    freeze = commit('freeze')

    res = {'freeze': freeze, 'base': base,
           'constants': {'carriers': m.CARRIERS, 'reader': m.READER, 'entry': m.ENTRY,
                         'stem': m.STEM, 'heading': m.HEADING, 'note': m.NOTE,
                         'r40_record_re': m.R40_RECORD.pattern}}

    # red case 1: S126 exists at the base; a rev row with the entry in used-by does not make it new.
    put(m.ENTRY, 'source: S126\n')
    put('corpus/SOURCES.md', '| id | x |\n|---|---|\n| S126 | highest at base %s |\n' % m.ENTRY)
    rev = commit('cites base-highest S126')
    ok, det = m.sourced_new(D, rev, base)
    res['base_sid_s126'] = {'sourced_new': ok, 'detail': det}

    # red case 2: a Round-40 note line naming the round-41 heading/stem, supersede verb and record.
    put('PROVINCE.md', '# p\nRound-40 frontier note: the round-40 measured, not promoted record '
                       'is superseded; see %s, %s.\n' % (m.HEADING, m.STEM))
    rev = commit('round-40 note only')
    ok, det = m.frontier_content(D, rev)
    res['round_40_note_only'] = {'frontier_content': ok, 'detail': det}

    # red case 3: a Round-41 note with heading + stem + supersede verb that never names the record.
    put('PROVINCE.md', '# p\nRound-41 frontier note: AVM-BE supersedes the round-39 AVM '
                       'sentence; see %s, %s.\n' % (m.HEADING, m.STEM))
    rev = commit('r41 note omits r40 record')
    ok, det = m.frontier_content(D, rev)
    res['r41_note_omits_r40_record'] = {'frontier_content': ok, 'detail': det}

    # red case 4 (round-40 carry-over): heading + stem + record, no supersede verb.
    put('PROVINCE.md', '# p\nRound-41 frontier note: the round-40 measured, not promoted record '
                       'stays; see %s, %s.\n' % (m.HEADING, m.STEM))
    rev = commit('presence-only note')
    ok, det = m.frontier_content(D, rev)
    res['presence_only'] = {'frontier_content': ok, 'detail': det}

    # green control: all four sub-checks true.
    put('PROVINCE.md', '# p\n%s\nRound-41 frontier note, 2026-10-26: the round-40 `measured, not '
                       'promoted` record (`## Round-40 measured, not promoted (R40-C1 honest '
                       'stop)`) is superseded; see %s (`%s`).\n' % (m.HEADING, m.HEADING, m.STEM))
    rev = commit('green note')
    ok, det = m.frontier_content(D, rev)
    res['green'] = {'frontier_content': ok, 'detail': det}

    # final full measure on a state that satisfies all three bindings (S127 is absent at base).
    put(m.ENTRY, 'source: S127\n')
    put('corpus/SOURCES.md', '| id | x |\n|---|---|\n| S126 | highest at base |\n'
                             '| S127 | new %s |\n' % m.ENTRY)
    rev = commit('green state')
    total = m.measure(D, rev, freeze, base, None, work=tmp)
    res['measure_green'] = {'met': total['met'], 'bindings': total['bindings'],
                            'frontier_detail': total['detail']['frontier_content'],
                            'sourced_detail': total['detail']['sourced_new'],
                            'oracle_detail': total['detail']['oracle_rederived']}
finally:
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)

json.dump(res, open(out, 'w'), indent=1, sort_keys=True)
print(json.dumps(res, indent=1, sort_keys=True))
