#!/usr/bin/env python3
"""Seat harness: 30 hand-written forgeries/edge cases against the GREEN fixture commit, scored
in-process with the draft counter's own `score` over an `Overlay` (nothing is written).
Each row: (label, overlay, expected red set).  Usage: attacks.py CLONE GREEN_REV WORKDIR"""
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('m', os.path.join(HERE, 'tools', 'round-50', 'c2-record.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

clone, rev, work = os.path.abspath(sys.argv[1]), sys.argv[2], os.path.abspath(sys.argv[3])
os.makedirs(work, exist_ok=True)
g = m.Git(clone)
rev = g.resolve(rev)
c0 = m.Ctx(g, rev, work, clone)
sc = m.text(g.show(rev, 'SCORECARD.md'))
soc = m.text(g.show(rev, 'corpus/SOURCES.md'))
sk = m.text(g.show(rev, 'SKILL.md'))
ln = {a: next(l for l in sc.split('\n') if l.startswith('- %s ' % a)) for a in ('B3', 'B4', 'B5', 'B10', 'B11')}
s150 = next(l for l in soc.split('\n') if l.startswith('| S150 '))
s151 = next(l for l in soc.split('\n') if l.startswith('| S151 '))
s152 = next(l for l in soc.split('\n') if l.startswith('| S152 '))
cal = next(l for l in sc.split('\n') if l.startswith('| calibration |'))
cov = next(l for l in sc.split('\n') if l.startswith('| coverage |'))
reg = next(l for l in sk.split('\n') if l.startswith('| `tools/round-49/c2-mismatch.py`'))
A = []


def add(label, over, red):
    A.append((label, over, sorted(red)))


def S(t):
    return {'SCORECARD.md': t.encode()}


def O(t):
    return {'corpus/SOURCES.md': t.encode()}


add('control: unmodified green', {}, [])
add('CRLF at the end of the B3 line still counts (renders the same)', S(sc.replace(ln['B3'], ln['B3'] + '\r')), [])
add('B3 line indented four spaces (indented code)', S(sc.replace(ln['B3'], '    ' + ln['B3'])), ['B3'])
add('B3 line in a block quote', S(sc.replace(ln['B3'], '> ' + ln['B3'])), ['B3'])
add('B3 line after a leading inline comment', S(sc.replace(ln['B3'], '<!-- x --> ' + ln['B3'])), ['B3'])
add('B3 line with a mid-line comment hiding a repeated key', S(sc.replace(ln['B3'], ln['B3'] + ' <!-- seats=9 -->')), ['B3'])
add('B3 line with an unknown extra key', S(sc.replace(ln['B3'], ln['B3'] + ' note=x')), ['B3'])
add('B3 line with a stray bare token', S(sc.replace(ln['B3'], ln['B3'] + ' fine')), ['B3'])
add('second heading `## Record corrections \u2014 round 50 (draft)`',
    S(sc.rstrip('\n') + '\n\n## Record corrections \u2014 round 50 (draft)\n\n- B3 seats=1\n'), ['B3', 'B4', 'B5', 'B10', 'B11'])
add('~~~ fence wrapping B4 with a longer closing fence', S(sc.replace(ln['B4'], '~~~\n' + ln['B4'] + '\n~~~~')), ['B4'])
add('tilde fence closed by a backtick fence does not close (hides the rest)',
    S(sc.replace(ln['B4'], '~~~\n' + ln['B4'] + '\n```')), ['B4', 'B5', 'B10', 'B11'])
add('coverage row duplicated', S(sc.replace(cov, cov + '\n' + cov)), ['B1'])
add('coverage row states the stale fraction first', S(sc.replace('140/140 knowledge', '138/138 knowledge')), ['B1'])
add('calibration row: 9 -> 1', S(sc.replace(cal, cal.replace('9 \u2192 0', '9 \u2192 1'))), ['B2'])
add('B5 receipt digest of c2 swapped for c1', S(sc.replace(ln['B5'], re.sub(r'c2_sha256=\w+', 'c2_sha256=' + re.search(r'c1_sha256=(\w+)', ln['B5']).group(1), ln['B5']))), ['B5'])
add('B4 discernment scope dropped', S(sc.replace('discernment_scope=decision-level-only ', '')), ['B4'])
add('B11 freeze file path changed', S(sc.replace('freeze_file=.ufo/waves/round-49/l1/FREEZE', 'freeze_file=FREEZE')), ['B11'])
add('S150 tier changed to A (kept status)', O(soc.replace(s150, s150.replace('| docs | C |', '| docs | A |'))), ['B6'])
add('S150 quote moved to the DESCRIPTION heading (anchor names DESCRIPTION only)',
    O(soc.replace(s150, s150.replace('`ERRORS`', '`DESCRIPTION`').replace('`ERRORS` heading', '`DESCRIPTION` heading'))), ['B6'])
add('S150 teaches opens "supersedes S149 -" with a hyphen',
    O(soc.replace(s150, s150.replace('supersedes S149 \u2014', 'supersedes S149 -'))), ['B6'])
add('second S149 correction row with a new id', O(soc.rstrip('\n') + '\n' + s150.replace('S150', 'S160') + '\n'), ['B6'])
add('S149 own row rewritten', O(soc.replace('| S149 |', '| S149 | (edited) ', 1)), ['B6'])
add('S151 teaches says tier A', O(soc.replace(s151, s151.replace('tier B per CORPUS', 'tier A per CORPUS'))), ['B7'])
add('S151 used-by loses the lesson', O(soc.replace(s151, s151.replace('`corpus/lessons/round-50.md`', '`corpus/lessons/round-49.md`'))), ['B7'])
add('S152 snapshot sha pin wrong', O(soc.replace(s152, re.sub(r'sha256 `[0-9a-f]{64}`', 'sha256 `' + '0' * 64 + '`', s152))), ['B8'])
add('S152 used-by empty', O(soc.replace(s152, re.sub(r'\| `corpus/lessons/round-50.md`, `[^|]*\|$', '| |', s152))), ['B8'])
add('registry markers doubled by a second visible region', {'SKILL.md': (sk + '\n' + m.REG_OPEN + '\n' + m.REG_CLOSE + '\n').encode()}, ['B9'])
add('registry row for c2-mismatch.py: self-test cell names another path',
    {'SKILL.md': sk.replace(reg, reg.replace('python3 -I -B tools/round-49/c2-mismatch.py --selftest', 'python3 -I -B tools/round-49/other.py --selftest')).encode()}, ['B9'])
add('registry row for c2-mismatch.py: verdict map `0=met` only',
    {'SKILL.md': sk.replace(reg, reg.replace('1=not met, a clause false; ', '').replace('0=met, every clause true;', '0=met;')).encode()}, ['B9'])
add('registry row with an extra cell', {'SKILL.md': sk.replace(reg, reg + ' extra |').encode()}, ['B9'])
add('selftest script deleted at REV', {m.SELFTEST_PATH: None}, ['B10'])
add('LOG.md truncated', {'LOG.md': g.show(rev, 'LOG.md')[:-200]}, ['B11'])

res, bad = [], 0
for label, over, red in A:
    cc = m.Ctx(m.Overlay(g, rev, over), rev, work, clone)
    cc.b10_cache = c0.b10_cache
    got = m.score(cc)
    r = sorted(k for k, v in got.items() if v)
    ok = r == red
    bad += not ok
    res.append({'label': label, 'expected_red': red, 'red': r, 'ok': ok,
                'why': {k: v[:2] for k, v in got.items() if v} if not ok else None})
print(json.dumps({'cases': len(res), 'deviations': bad, 'rows': res}, indent=1, ensure_ascii=False))
sys.exit(1 if bad else 0)
