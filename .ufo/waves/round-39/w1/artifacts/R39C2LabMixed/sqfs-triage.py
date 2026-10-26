#!/usr/bin/env python3
"""ADVISORY reference interpreter for the R39-C2 SquashFS triage table grammar.

This is a lab artifact, not the frozen tools/round-39/sqfs-triage.py.  It
implements the L1 contract verbatim so the grammar can be exercised against
development envelopes; the integration owner owns the frozen tool.

Grammar
  * Table = first markdown table after a line containing the marker
    `<!-- sqfs-triage-table v1 -->` inside SKILL.md's `## Queue-drain craft`
    section (heading line to the next `## ` heading).
  * Header row (exact cells, in order):
      label | handler | gap kinds | dependencies | -be in child argv |
      symlink removed | published files | cause -> action | source
  * Rules tried top to bottom; first row whose every condition cell matches
    gives the label; no match -> `unclassified`.
  * Condition cells (surrounding backticks/spaces stripped):
      handler            `none` (H empty) or an fnmatch pattern matching >=1
                         element of H
      gap kinds/deps     `none` (empty set) or `a+b` = exactly {a,b}
      -be/symlink removed  yes | no | n/a
      published files    0 | >0 | *
    `*` matches anything.  A malformed cell makes the table unevaluable
    (exit 2), never a silent non-match.
  * Envelope input: a bare REA `data` object or a full {ok,data,meta} CLI
    envelope.  Features:
      H  = {chunks[].handler | handler startswith 'squashfs'}
      G  = {extraction_gaps[].kind}
      D  = union(extraction_gaps[].dependencies)
      BE = yes if a diagnostics[].report `command` (string/argv list) naming
           sasquatch has a standalone `-be` token; no if such a command
           exists without it; n/a if no such command is recorded
      SR = yes if any diagnostics[].report.__typename__ ==
           MaliciousSymlinkRemoved (also accepted anywhere under
           raw_result.report)
      P  = len(normalized_result.files)

Usage:
  sqfs-triage.py --skill SKILL.md ENVELOPE.json [ENVELOPE.json ...]
  sqfs-triage.py --skill SKILL.md --table-only
Exit: 0 evaluated (labels printed as JSON), 2 unevaluable (table absent or
malformed, unreadable envelope).
"""
import argparse
import fnmatch
import json
import re
import shlex
import sys

HEADER = ['label', 'handler', 'gap kinds', 'dependencies',
          '-be in child argv', 'symlink removed', 'published files',
          'cause -> action', 'source']
COND = HEADER[1:7]
MARKER = '<!-- sqfs-triage-table v1 -->'
SECTION = '## Queue-drain craft'


class Unevaluable(Exception):
    pass


def table_lines(text):
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith(SECTION):
            start = i
            break
    if start is None:
        raise Unevaluable('no "## Queue-drain craft" heading')
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith('## '):
            end = j
            break
    marker = None
    for i in range(start, end):
        if MARKER in lines[i]:
            marker = i
            break
    if marker is None:
        raise Unevaluable('marker %r absent from craft section' % MARKER)
    i = marker + 1
    while i < end and not lines[i].lstrip().startswith('|'):
        i += 1
    if i >= end:
        raise Unevaluable('no markdown table after marker')
    tbl = []
    while i < end and lines[i].lstrip().startswith('|'):
        tbl.append(lines[i])
        i += 1
    return tbl


def cells(row):
    s = row.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c.strip().strip('`').strip() for c in s.split('|')]


def parse_table(text):
    rows = table_lines(text)
    if len(rows) < 3:
        raise Unevaluable('table needs header + separator + >=1 rule row')
    header = cells(rows[0])
    if header != HEADER:
        raise Unevaluable('header mismatch: %r' % (header,))
    sep = cells(rows[1])
    if len(sep) != len(HEADER) or not all(re.fullmatch(r':?-{2,}:?', c) for c in sep):
        raise Unevaluable('bad separator row: %r' % (sep,))
    rules = []
    for raw in rows[2:]:
        cs = cells(raw)
        if len(cs) != len(HEADER):
            raise Unevaluable('row has %d cells, want %d: %r'
                              % (len(cs), len(HEADER), raw))
        rule = {'label': cs[0], 'raw': raw}
        for name, cell in zip(COND, cs[1:7]):
            rule[name] = check_cell(name, cell)
        if not rule['label']:
            raise Unevaluable('empty label in row: %r' % (raw,))
        rules.append(rule)
    if not rules:
        raise Unevaluable('no rule rows')
    return rules


def check_cell(name, cell):
    if cell == '*':
        return '*'
    if name == 'handler':
        if cell == 'none':
            return ('none', None)
        if not cell:
            raise Unevaluable('empty handler cell')
        return ('pat', cell)
    if name in ('gap kinds', 'dependencies'):
        if cell == 'none':
            return ('exact', frozenset())
        parts = [p.strip() for p in cell.split('+')]
        if not all(parts):
            raise Unevaluable('bad %s cell %r' % (name, cell))
        return ('exact', frozenset(parts))
    if name in ('-be in child argv', 'symlink removed'):
        if cell not in ('yes', 'no', 'n/a'):
            raise Unevaluable('bad %s cell %r' % (name, cell))
        return ('lit', cell)
    if name == 'published files':
        if cell not in ('0', '>0'):
            raise Unevaluable('bad published files cell %r' % (cell,))
        return ('lit', cell)
    raise AssertionError(name)


def is_sasquatch_token(tok):
    base = tok.rsplit('/', 1)[-1]
    return base == 'sasquatch' or base.startswith('sasquatch-')


def commands_of(report):
    cmd = report.get('command') if isinstance(report, dict) else None
    if cmd is None:
        return []
    if isinstance(cmd, list):
        return [[str(x) for x in cmd]]
    return [shlex.split(cmd)]


def be_feature(diags):
    seen = False
    for dg in diags:
        rep = dg.get('report') if isinstance(dg, dict) else None
        if not isinstance(rep, dict):
            continue
        for argv in commands_of(rep):
            if not any(is_sasquatch_token(t) for t in argv):
                continue
            seen = True
            if '-be' in argv:
                return 'yes'
    return 'no' if seen else 'n/a'


def sr_feature(raw_report):
    def scan(o):
        if isinstance(o, dict):
            if o.get('__typename__') == 'MaliciousSymlinkRemoved':
                return True
            return any(scan(v) for v in o.values())
        if isinstance(o, list):
            return any(scan(v) for v in o)
        return False
    return 'yes' if scan(raw_report) else 'no'


def features(env):
    data = env.get('data') if isinstance(env, dict) and 'data' in env else env
    if not isinstance(data, dict) or 'normalized_result' not in data:
        raise Unevaluable('not a REA envelope (no normalized_result)')
    nr = data['normalized_result']
    H = {c.get('handler') for c in nr.get('chunks') or []
         if isinstance(c.get('handler'), str)
         and c['handler'].startswith('squashfs')}
    gaps = nr.get('extraction_gaps') or []
    G = {g.get('kind') for g in gaps if isinstance(g.get('kind'), str)}
    D = {dep for g in gaps for dep in (g.get('dependencies') or [])
         if isinstance(dep, str)}
    diags = nr.get('diagnostics') or []
    SR = 'yes' if any((isinstance(dg.get('report'), dict) and
                       dg['report'].get('__typename__') == 'MaliciousSymlinkRemoved')
                      for dg in diags) else 'no'
    if SR == 'no' and data.get('raw_result') is not None:
        SR = sr_feature(data['raw_result'].get('report'))
    return {'H': H, 'G': G, 'D': D, 'BE': be_feature(diags), 'SR': SR,
            'P': len(nr.get('files') or []),
            'coverage': nr.get('coverage'),
            'published_bytes': nr.get('published_bytes'),
            'ok': env.get('ok') if isinstance(env, dict) else None}


def matches(rule, f):
    h = rule['handler']
    if h != '*':
        kind, pat = h
        if kind == 'none':
            if f['H']:
                return False
        elif not any(fnmatch.fnmatchcase(x, pat) for x in f['H']):
            return False
    for name, key in (('gap kinds', 'G'), ('dependencies', 'D')):
        c = rule[name]
        if c != '*' and c[0] == 'exact' and f[key] != c[1]:
            return False
        if c != '*' and c[0] != 'exact':
            raise AssertionError(name)
    for name, key in (('-be in child argv', 'BE'), ('symlink removed', 'SR')):
        c = rule[name]
        if c != '*' and c[1] != f[key]:
            return False
    c = rule['published files']
    if c != '*':
        if c[1] == '0' and f['P'] != 0:
            return False
        if c[1] == '>0' and f['P'] <= 0:
            return False
    return True


def classify(rules, f):
    for rule in rules:
        if matches(rule, f):
            return rule['label']
    return 'unclassified'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skill', required=True)
    ap.add_argument('--table-only', action='store_true')
    ap.add_argument('envelopes', nargs='*')
    a = ap.parse_args()
    try:
        with open(a.skill, encoding='utf-8') as f:
            rules = parse_table(f.read())
        if a.table_only:
            print(json.dumps({'rules': [r['label'] for r in rules]}, indent=1))
            return 0
        out = []
        for path in a.envelopes:
            with open(path, encoding='utf-8') as f:
                env = json.load(f)
            f = features(env)
            out.append({'envelope': path, 'features': {
                'H': sorted(f['H']), 'G': sorted(f['G']), 'D': sorted(f['D']),
                'BE': f['BE'], 'SR': f['SR'], 'P': f['P'],
                'coverage': f['coverage'],
                'published_bytes': f['published_bytes'], 'ok': f['ok']},
                'label': classify(rules, f)})
        print(json.dumps(out, indent=1))
        return 0
    except Unevaluable as e:
        print(json.dumps({'unevaluable': str(e)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
