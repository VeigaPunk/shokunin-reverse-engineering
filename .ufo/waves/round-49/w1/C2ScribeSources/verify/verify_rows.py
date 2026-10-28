#!/usr/bin/env python3
"""Verify draft rows S147/S148 and their snapshots against the draft counter's atoms A6 and A7.

Read-only: the lane repository is read through `git show` only; every candidate registry, snapshot
and lesson is an in-memory overlay on a sentinel revision that does not exist in git. Nothing is
written under the lane. The counter module is loaded from the draft path with bytecode writing
disabled, so no __pycache__ appears in the draft tree.
"""
import importlib.util
import json
import os
import sys

sys.dont_write_bytecode = True

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # .../w1/C2ScribeSources
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
COUNTER = LANE + '/.ufo/waves/round-49/draft/tools/round-49/c2-mismatch.py'
SNAP = W + '/staged/corpus/evidence/round-49/c2/'
REV = 'REVX-sentinel-not-in-git'

spec = importlib.util.spec_from_file_location('c2m', COUNTER)
c2m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2m)

git = c2m.Git(LANE)
base_sources = git.show(c2m.LANE_BASE, 'corpus/SOURCES.md')
assert base_sources is not None, 'lane base SOURCES.md unreadable'
rows = open(W + '/rows.md', 'rb').read()
lines = base_sources.split(b'\n')
idx = max(i for i, l in enumerate(lines) if l.startswith(b'| S146 '))
new_sources = b'\n'.join(lines[:idx + 1] + rows.rstrip(b'\n').split(b'\n') + lines[idx + 1:])
popper = open(SNAP + 'popper.html', 'rb').read()
sysx = open(SNAP + 'sysexits.html', 'rb').read()
lesson = open(W + '/gate.md', 'rb').read()
L = {'A6': {'row': 'S147'}, 'A7': {'row': 'S148'}}


def overlay(sources=None, pop=None, sx=None, les=None):
    over = {
        'corpus/SOURCES.md': sources if sources is not None else new_sources,
        'corpus/evidence/round-49/c2/popper.html': pop if pop is not None else popper,
        'corpus/evidence/round-49/c2/sysexits.html': sx if sx is not None else sysx,
        'corpus/lessons/round-49.md': les if les is not None else lesson,
    }
    return c2m.Overlay(git, REV, over)


def run(label, ov):
    a6 = c2m.a6(ov, REV, L)
    a7 = c2m.a7(ov, REV, L)
    return {'label': label, 'A6_red_reasons': a6, 'A7_red_reasons': a7,
            'A6': 'green' if not a6 else 'red', 'A7': 'green' if not a7 else 'red'}


def sub(b, a, c):
    assert a in b, 'pattern absent: %r' % a[:40]
    return b.replace(a, c, 1)


def with_row(sid, fn):
    out = []
    for l in new_sources.split(b'\n'):
        if l.startswith(('| %s ' % sid).encode()):
            l = fn(l)
        out.append(l)
    return b'\n'.join(out)


res = []
# 1. genuine drafts: both atoms must be green
res.append(run('genuine drafts', overlay()))
# 2. battery-equivalent counterfactuals the counter itself uses
res.append(run('mut A6 snapshot byte edit (empirical->empirica1)',
               overlay(pop=popper.replace(b'empirical', b'empirica1'))))
res.append(run('mut A6 anchor names wrong section only',
               overlay(sources=sub(new_sources, '`2. Backdrop to Popper’s Thought`'.encode('utf-8'),
                                   '`3. The Problem of Demarcation; Popper’s Thought`'.encode('utf-8')))))
res.append(run('mut A7 sysexits snapshot byte edit (EX_USAGE->EX_USAGF)',
               overlay(sx=sysx.replace(b'EX_USAGE', b'EX_USAGF'))))
res.append(run('mut A7 teaches EX_USAGE is 64 -> is 2',
               overlay(sources=sub(new_sources, b'EX_USAGE is 64', b'EX_USAGE is 2'))))
# 3. vacuity probes: claims the counter should refuse but may accept
res.append(run('PROBE A6 anchor names the WRONG S145 heading AND the right one (counter checks containment only)',
               overlay(sources=with_row('S147', lambda l: l.replace(
                   '`2. Backdrop to Popper’s Thought`'.encode('utf-8'),
                   '`2. The Problem of Demarcation`; `2. Backdrop to Popper’s Thought`'.encode('utf-8'), 1)))))
res.append(run('PROBE A6 anchor names ONLY the wrong S145 heading (should be red)',
               overlay(sources=with_row('S147', lambda l: l.replace(
                   '`2. Backdrop to Popper’s Thought`'.encode('utf-8'),
                   '`2. The Problem of Demarcation`'.encode('utf-8'), 1)))))
res.append(run('PROBE A7 teaches says EX_USAGE is 2 and EX__BASE is 64 (wrong claim, should be red)',
               overlay(sources=with_row('S148', lambda l: l.replace(
                   b'EX_USAGE is 64', b'EX_USAGE is 2; EX__BASE is 64', 1)))))
res.append(run('PROBE A7 teaches drops the lane-convention statement (should be red per the S148 contract)',
               overlay(sources=with_row('S148', lambda l: l.replace(
                   b'; the lane\'s 0/1/2 exit meanings are its own convention, so no sysexits value grounds exit 2',
                   b'', 1)))))
res.append(run('PROBE A6 quote case-changed (should be red)',
               overlay(sources=with_row('S147', lambda l: l.replace(b'"if a theory', b'"If a theory', 1)))))
res.append(run('PROBE A6 pin removed (should be red)',
               overlay(sources=with_row('S147', lambda l: l.replace(
                   b'2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207', b'0' * 64, 1)))))
res.append(run('PROBE A7 S148 status queued (should be red)',
               overlay(sources=with_row('S148', lambda l: l.replace(b'| mined | 2026-10-28 | 365d',
                                                                  b'| queued | 2026-10-28 | 365d', 1)))))
res.append(run('PROBE A6 S145 line edited (should be red: append-only)',
               overlay(sources=sub(new_sources, b'`2. The Problem of Demarcation`; "if a theory',
                                   b'`2. The Problem of Demarcation`; "If a theory'))))

out = {'counter': COUNTER, 'counter_sha256': c2m.sha(open(COUNTER, 'rb').read()),
       'lane_base': c2m.LANE_BASE, 'results': res}
print(json.dumps(out, indent=1, ensure_ascii=False))
