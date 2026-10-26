#!/usr/bin/env python3
"""R42-C1 gate cross-check: run the ROUND-41 gate's own matchers on the round-42 drafts.

Why: `check-draft.py` re-implements the text bindings, which proves the draft is consistent with my
reading of the gate, not with the gate. This script loads `tools/round-41/c1-counter.py` and
`tools/round-41/c1-extra.py` from the base commit verbatim, patches ONLY the constants a round-42 port
must change, and asks their own functions what they think of the drafts. No lane write, no freeze, no REA.

Bindings (names follow the round-41 gate):
  province_section   counter.section(prov, CORE_HEADING)
  province_row       counter.HANDLER_RE on cells(row)[0] + <format regex> + ENTRY in row
  counter_frontier   any(FRONTIER_MARK in l and STEM in l and <format regex> on l)
  extra_frontier     extra.note_verdict(l)['ok']  (heading + stem + supersede + old-record phrase)
  entry_sids         counter.sid_tokens over the entry's `source:` lines
  sourced_new        an id absent at --base and present in the SOURCES draft with the entry in used-by
  sources_row        extra.sids() over the SOURCES draft -> 11 cells, opened, used-by
  coverage_row       counter.section(readme, '## Coverage map') maps the stem

Usage: gate-crosscheck.py --dir ART --lane LANE [--base REV] [--work DIR] [--json-out F]
       gate-crosscheck.py --selftest
Exit 0 every binding true; 1 any false; 2 unevaluable.
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

ENTRY = 'corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md'
STEM = '2026-10-26-r42-squashfs-v3-core'
CORE_HEADING = '## Round-42 additions to Core'
FRONTIER_MARK = 'Round-42 frontier note'
HANDLER = 'squashfs_v3'
FORMAT_RE = re.compile(r'little-endian SquashFS v3|squashfs_v3 family|v3 family|SquashFS v3',
                       re.IGNORECASE)
OLD_RECORD = re.compile(r'coverage claim only')
OPENED = '2026-10-26'
SID_ROW = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
TOKEN_RE = re.compile(r'<<L1:[^>]*>>')


class Unevaluable(Exception):
    pass


def sh(cwd, *args):
    p = subprocess.run(args, cwd=cwd, capture_output=True)
    return p.returncode, p.stdout


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fences(text):
    out, body, last = [], None, ''
    for line in text.splitlines():
        if line.startswith('```'):
            if body is None:
                body = []
            else:
                out.append((last, '\n'.join(body)))
                body = None
            continue
        if body is not None:
            body.append(line)
        elif line.strip():
            last = line
    return out


def pick(fl, needle):
    for _, block in fl:
        if needle in block:
            return block
    raise Unevaluable('no fenced block with %r' % needle)


def insert_after_last(lines, startswith, new):
    idx = [i for i, l in enumerate(lines) if l.startswith(startswith)]
    if not idx:
        raise Unevaluable('no line starts %r' % startswith)
    at = idx[-1] + 1
    return lines[:at] + list(new) + lines[at:]


def synthesize(counter, base_prov, base_readme, prov_block, cov_row, idx_row, fr_line):
    prov = base_prov.rstrip('\n') + '\n\n' + prov_block.strip('\n') + '\n'
    sec = counter.section(base_readme, '## Coverage map')
    if sec is None:
        raise Unevaluable('base README lacks ## Coverage map')
    last = [l for l in sec if l.lstrip().startswith('|')][-1]
    lines = insert_after_last(base_readme.splitlines(), last, [cov_row.strip()])
    readme = '\n'.join(lines) + '\n'
    k = counter.section(readme, '## Knowledge')
    if k is not None:
        krow = [l for l in k if l.lstrip().startswith('|')][-1]
        readme = '\n'.join(insert_after_last(readme.splitlines(), krow, [idx_row.strip()])) + '\n'
    readme = '\n'.join(insert_after_last(readme.splitlines(), '- sasquatch-v4be', [fr_line.strip()])) + '\n'
    return prov, readme


def run(dirpath, lane, base, work):
    rc, out = sh(lane, 'git', 'show', '%s:tools/round-41/c1-counter.py' % base)
    if rc != 0:
        raise Unevaluable('counter absent at %s' % base)
    rc2, out2 = sh(lane, 'git', 'show', '%s:tools/round-41/c1-extra.py' % base)
    if rc2 != 0:
        raise Unevaluable('extra absent at %s' % base)
    cp = os.path.join(work, 'c1_counter.py')
    ep = os.path.join(work, 'c1_extra.py')
    open(cp, 'wb').write(out)
    open(ep, 'wb').write(out2)
    counter, extra = load(cp, 'c1_counter_r41'), load(ep, 'c1_extra_r41')

    # ---- the only constants a round-42 port changes (everything else stays the round-41 code)
    counter.ENTRY, counter.STEM = ENTRY, STEM
    counter.CORE_HEADING, counter.FRONTIER_MARK = CORE_HEADING, FRONTIER_MARK
    counter.HANDLER = HANDLER
    counter.HANDLER_RE = re.compile(r'(?<![A-Za-z0-9_-])' + HANDLER + r'(?![A-Za-z0-9_-])')
    counter.AVM_LAYOUT_RE = FORMAT_RE
    counter.OPENED = OPENED
    extra.ENTRY, extra.STEM, extra.HEADING = ENTRY, STEM, CORE_HEADING
    extra.NOTE, extra.R40_RECORD = FRONTIER_MARK, OLD_RECORD

    base_prov = subprocess.run(['git', '-C', lane, 'show', '%s:PROVINCE.md' % base],
                               capture_output=True).stdout.decode()
    base_readme = subprocess.run(['git', '-C', lane, 'show', '%s:corpus/README.md' % base],
                                 capture_output=True).stdout.decode()
    base_sources = subprocess.run(['git', '-C', lane, 'show', '%s:corpus/SOURCES.md' % base],
                                  capture_output=True).stdout.decode()

    prov_txt = open(os.path.join(dirpath, 'province-round42-additions.md')).read()
    readme_txt = open(os.path.join(dirpath, 'readme-r42-rows.md')).read()
    src_txt = open(os.path.join(dirpath, 'sources-r42-rows.md')).read()
    entry_txt = open(os.path.join(dirpath, 'entry-' + ENTRY.replace('/', '-'))).read()

    prov_block = pick(fences(prov_txt), CORE_HEADING)
    cov = pick(fences(readme_txt), '| SquashFS v3 handler family through REA (round 42)')
    idx = pick(fences(readme_txt), '| `' + STEM + '` |')
    fr = pick(fences(readme_txt), '- sasquatch — 2026-10-26 round 42')
    prov, readme = synthesize(counter, base_prov, base_readme, prov_block, cov, idx, fr)

    b = {}
    sec = counter.section(prov, counter.CORE_HEADING)
    b['province_section'] = sec is not None
    rows = [l for l in (sec or []) if l.lstrip().startswith('|')]
    b['province_row'] = any(
        counter.HANDLER_RE.search(counter.cells(r)[0]) and counter.AVM_LAYOUT_RE.search(r)
        and counter.ENTRY in r for r in rows)
    b['counter_frontier'] = any(
        counter.FRONTIER_MARK in l and counter.STEM in l and counter.AVM_LAYOUT_RE.search(l)
        for l in prov.splitlines())
    lines = [l for l in prov.splitlines() if counter.FRONTIER_MARK in l]
    b['extra_frontier'] = bool(lines) and all(extra.note_verdict(l)['ok'] for l in lines)
    b['extra_frontier_detail'] = [extra.note_verdict(l) for l in lines[:2]]

    cited = set()
    for line in entry_txt.splitlines():
        if line.startswith('source:'):
            cited |= counter.sid_tokens(line)
    b['entry_sids'] = sorted(cited)
    at_base = set(extra.sids(base_sources.encode()))
    draft = extra.sids(pick(fences(src_txt), '| S130').encode())
    b['sourced_new'] = any(s not in at_base and s in draft and ENTRY in draft[s] for s in cited)
    b['sources_row'] = all(len(counter.cells(r)) == 11 and counter.cells(r)[8] == OPENED
                           and (ENTRY in counter.cells(r)[10] or STEM in counter.cells(r)[10])
                           for r in draft.values())
    b['sources_ids'] = sorted(draft)
    cm = counter.section(readme, '## Coverage map')
    b['coverage_row'] = bool(cm) and any(STEM in l for l in cm if l.lstrip().startswith('|'))
    names = ('province_section', 'province_row', 'counter_frontier', 'extra_frontier',
             'sourced_new', 'sources_row', 'coverage_row')
    return {'bindings': b, 'order': list(names),
            'met': all(b.get(n) is True for n in names) and bool(b['entry_sids'])}


def selftest():
    """Two plantings on the base text: the gate must go red when the round-41 constants are restored."""
    ok = True
    out = []
    lane = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
    base = 'c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c'
    rc, out_b = sh(lane, 'git', 'show', '%s:tools/round-41/c1-counter.py' % base)
    if rc != 0:
        return {'selftest_ok': False, 'error': 'counter absent'}
    work = tempfile.mkdtemp(prefix='r42-xs-', dir=os.environ.get('TMPDIR'))
    cp = os.path.join(work, 'c.py')
    open(cp, 'wb').write(out_b)
    counter = load(cp, 'c1_counter_st')
    # round-41 constants must NOT match round-42 text
    prov = ('## Round-42 additions to Core\n\n| Surface | a |\n|---|---|\n| little-endian SquashFS v3 — '
            'the v3 family, squashfs_v3 family (`squashfs_v3`) | %s |\n\n'
            'Round-42 frontier note, 2026-10-26: superseded; coverage claim only; %s; little-endian '
            'SquashFS v3, v3 family, squashfs_v3 family.\n' % (ENTRY, STEM))
    out.append({'case': 'round-41 heading finds nothing in round-42 text',
                'pass': counter.section(prov, '## Round-41 additions to Core') is None})
    out.append({'case': 'round-41 handler token does not match the round-42 row',
                'pass': not counter.HANDLER_RE.search('the v3 family (`squashfs_v3`)')})
    ok = ok and all(c['pass'] for c in out)
    return {'selftest_ok': ok, 'cases': out, 'work': work}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir')
    ap.add_argument('--lane', default='/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
    ap.add_argument('--base', default='c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c')
    ap.add_argument('--work')
    ap.add_argument('--json-out')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        res = selftest()
        code = 0 if res.get('selftest_ok') else 1
        res.pop('work', None)
    else:
        if not a.dir:
            ap.error('--dir is required')
        work = tempfile.mkdtemp(prefix='r42-xs-', dir=a.work or os.environ.get('TMPDIR'))
        try:
            res, code = run(a.dir, a.lane, a.base, work), None
            code = 0 if res['met'] else 1
        except Unevaluable as e:
            res, code = {'error': str(e)}, 2
    txt = json.dumps(res, indent=1, sort_keys=True)
    if a.json_out:
        open(a.json_out, 'w').write(txt + '\n')
    print(txt)
    return code


if __name__ == '__main__':
    sys.exit(main())
