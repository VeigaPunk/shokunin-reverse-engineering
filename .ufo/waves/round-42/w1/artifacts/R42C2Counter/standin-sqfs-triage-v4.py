#!/usr/bin/env python3
"""STAND-IN v4 triage interpreter — dry-run scaffold for `tools/round-42/sqfs-triage-v4.py`.

This file is NOT the frozen interpreter. The frozen one is owned by the
`R42C2Interp` seat; this stand-in exists so the round-42 C2 counter can be
dry-run end to end before the owning drafts land (QUALITY 84). It reads only
the `<!-- sqfs-triage-table v4 -->` rule block inside `## Queue-drain craft`
and decides one envelope at a time, first matching row wins.

Table grammar (v4)
  * marker line inside `## Queue-drain craft`: `<!-- sqfs-triage-table v4 -->`
  * the actions vocabulary on `<!-- sqfs-triage-actions: ... -->`
  * twelve columns as round 41; the counter needs
    label, operation, provider, handler, gap kinds, dependencies,
    `-be in child argv`, `symlink removed`, `published files`, action.

  cell grammar
    `*`                any (scalar) / any set
    `none`             the empty set, or the scalar value `none`
    `token`            set cell: the set is EXACTLY {token}
                       scalar cell: value == token
    `token+`           set cell: token is a MEMBER (contains form)
    `tok1,tok2`        alternatives (OR) inside one cell
    `squashfs_v[123]*` handler cell: fnmatch glob against a handler name

  handler-cell scope.  A row whose `gap kinds` cell names
  `extractor-failure` decides the FAILING chunk (`extraction_failed` true),
  so its handler cell is matched against the failing handlers only; every
  other row matches against all SquashFS handlers in H.  This is the
  stand-in's encoding of the precedence's "failing handler" wording and is
  the convention the dry run measures; the `R42C2Grammar` seat owns the
  frozen semantics.

  Fall-through (no row matches) is `unclassified` / `none` (round-41 rule).

Usage
  python3 -I -B sqfs-triage-v4.py --skill SKILL.md [--json] [--table-only] ENV...
  python3 -I -B sqfs-triage-v4.py --skill SKILL.md --envelopes DIR [--json]
Exit
  0  decided every envelope (including fall-through)
  2  table/skill refusal: no craft section, no v4 marker, a v3 marker where a
     v4 table is required, a malformed table, a duplicate label, an action
     outside the declared vocabulary
  3  an envelope is unreadable
"""
import argparse
import fnmatch
import json
import re
import shlex
import sys

MARKER = '<!-- sqfs-triage-table v4 -->'
MARKER_V3 = '<!-- sqfs-triage-table v3 -->'
ACTIONS_RE = re.compile(r'<!--\s*sqfs-triage-actions:\s*(.*?)\s*-->')
CRAFT = '## Queue-drain craft'
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'


class Refusal(Exception):
    pass


# ------------------------------------------------------------------ table
def craft_lines(text):
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines)
                  if l.lower().startswith(CRAFT.lower())), None)
    if start is None:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith('## '):
            end = i
            break
    return lines[start:end]


def table_block(text):
    lines = craft_lines(text)
    if lines is None:
        raise Refusal('no %r section' % CRAFT)
    mi = None
    for i, l in enumerate(lines):
        if l.strip().startswith(MARKER):
            mi = i
            break
    if mi is None:
        if any(MARKER_V3 in l for l in lines):
            raise Refusal("refused marker %r; this interpreter reads only %r"
                          % (MARKER_V3, MARKER))
        raise Refusal('no %r marker' % MARKER)
    stop = len(lines)
    for i in range(mi + 1, len(lines)):
        l = lines[i]
        if re.match(r'^#{1,4} ', l) or re.match(r'^\s*-\s+\*\*', l) \
                or l.strip().startswith('<!-- sqfs-triage-table'):
            stop = i
            break
    return lines[mi:stop]


def split_cell(cell):
    toks = []
    for raw in cell.replace('|', ' ').split(','):
        t = raw.strip().strip('`').strip()
        if t:
            toks.append(t)
    return toks


def parse_table(block):
    header = None
    rows = []
    for line in block:
        s = line.lstrip()
        if not s.startswith('|'):
            continue
        cells = [c.strip().strip('`').strip()
                 for c in s.strip().strip('|').split('|')]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if all(re.fullmatch(r'-{2,}|:?-+:?', c) for c in cells):
            continue
        rows.append(cells)
    if header is None or not rows:
        raise Refusal('v4 block carries no table rows')
    for need in ('label', 'action'):
        if need not in header:
            raise Refusal('v4 table has no %r column' % need)
    labels = [r[header.index('label')] for r in rows]
    if len(set(labels)) != len(labels):
        raise Refusal('duplicate label in the v4 table')
    return header, rows


def declared_actions(block):
    for line in block:
        m = ACTIONS_RE.search(line)
        if m:
            toks = [t.strip('`') for t in m.group(1).split()]
            return [t for t in toks if t]
    return None


# ------------------------------------------------------------------ features
def _as_list(v):
    return v if isinstance(v, list) else []


def _iter_dicts(obj):
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            yield cur
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)


def command_tokens(cmd):
    if isinstance(cmd, str):
        try:
            return shlex.split(cmd)
        except ValueError:
            return cmd.split()
    if isinstance(cmd, (list, tuple)):
        return [t for t in cmd if isinstance(t, str)]
    return None


def names_sasquatch(tokens):
    return any(t.rsplit('/', 1)[-1].startswith('sasquatch') for t in tokens)


def extractor_commands(data):
    cmds = []

    def take(cmd):
        toks = command_tokens(cmd)
        if toks and names_sasquatch(toks) and cmd not in cmds:
            cmds.append(cmd)

    nr = data.get('normalized_result')
    nr = nr if isinstance(nr, dict) else {}
    for source in (nr.get('diagnostics'), data.get('diagnostics')):
        for diag in _as_list(source):
            rep = diag.get('report') if isinstance(diag, dict) else None
            if isinstance(rep, dict) and 'command' in rep:
                take(rep['command'])
    for found in _iter_dicts(data.get('raw_result')):
        if 'command' in found:
            take(found['command'])
    return cmds


def envelope_features(data):
    nr = data.get('normalized_result')
    nr = nr if isinstance(nr, dict) else {}
    handlers = set()
    for chunk in _as_list(nr.get('chunks')):
        if not isinstance(chunk, dict):
            continue
        h = chunk.get('handler')
        if isinstance(h, str) and h:
            handlers.add(h)
    gaps, deps, hf = set(), set(), set()
    for gap in _as_list(nr.get('extraction_gaps')):
        if not isinstance(gap, dict):
            continue
        kind = gap.get('kind')
        if isinstance(kind, str):
            gaps.add(kind)
        gh = gap.get('handler')
        if isinstance(gh, str) and gh:
            handlers.add(gh)
            if kind == 'extractor-failure':
                hf.add(gh)
        for d in _as_list(gap.get('dependencies')):
            if isinstance(d, str):
                deps.add(d)
    squashfs = {h for h in handlers if h.startswith('squashfs_')}
    cmds = extractor_commands(data)
    be = 'n/a'
    if cmds:
        be = 'yes' if any('-be' in (command_tokens(c) or []) for c in cmds) else 'no'
    sr = False
    for diag in _as_list(nr.get('diagnostics')):
        rep = diag.get('report') if isinstance(diag, dict) else None
        if isinstance(rep, dict) and rep.get('__typename__') == SYMLINK_TYPENAME:
            sr = True
            break
    if not sr:
        for found in _iter_dicts(data.get('raw_result')):
            if found.get('__typename__') == SYMLINK_TYPENAME:
                sr = True
                break
    files = _as_list(nr.get('files'))
    op = data.get('operation')
    prov = data.get('provider')
    prov = prov.get('id') if isinstance(prov, dict) else prov
    return {'op': op if isinstance(op, str) else None,
            'pr': prov if isinstance(prov, str) else None,
            'handlers': handlers, 'squashfs': squashfs,
            'hf': hf or squashfs,
            'gaps': gaps, 'deps': deps, 'be': be, 'sr': sr,
            'files': len(files)}


# ------------------------------------------------------------------ matching
def scalar_match(cell, value):
    toks = split_cell(cell)
    if not toks or '*' in toks:
        return True
    if 'none' in toks:
        return value is None or value == 'none'
    return value in toks


def set_match(cell, values):
    toks = split_cell(cell)
    if not toks or '*' in toks:
        return True
    if 'none' in toks:
        return not values
    bare = [t for t in toks if not t.endswith('+')]
    plus = [t[:-1] for t in toks if t.endswith('+')]
    if bare and set(bare) != set(values):
        return False
    return all(p in values for p in plus)


def handler_match(cell, scope):
    toks = split_cell(cell)
    if not toks or '*' in toks:
        return True
    if 'none' in toks:
        return not scope
    return any(fnmatch.fnmatchcase(h, t) for t in toks for h in scope)


def row_matches(header, row, f):
    def cell(name):
        return row[header.index(name)] if name in header and header.index(name) < len(row) else '*'

    if not scalar_match(cell('operation'), f['op']):
        return False
    if not scalar_match(cell('provider'), f['pr']):
        return False
    scope = f['squashfs']
    if not handler_match(cell('handler'), scope):
        return False
    if not handler_match(cell('failing handler'), f['hf']):
        return False
    if not set_match(cell('gap kinds'), f['gaps']):
        return False
    if not set_match(cell('dependencies'), f['deps']):
        return False
    if not scalar_match(cell('-be in child argv'), f['be']):
        return False
    if not scalar_match(cell('symlink removed'), 'yes' if f['sr'] else 'no'):
        return False
    pub = '>0' if f['files'] else '0'
    if not scalar_match(cell('published files'), pub):
        return False
    return True


def decide(header, rows, data):
    f = envelope_features(data)
    for i, row in enumerate(rows):
        if row_matches(header, row, f):
            return {'label': row[header.index('label')],
                    'action': row[header.index('action')],
                    'rule': i, 'cells': row}
    return {'label': 'unclassified', 'action': 'none', 'rule': None, 'cells': None}


# ------------------------------------------------------------------ CLI
def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('--skill')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--table-only', action='store_true')
    ap.add_argument('--envelopes', dest='envelopes_dir')
    ap.add_argument('envs', nargs='*')
    a = ap.parse_args(argv)
    try:
        if not a.skill:
            raise Refusal('--skill is required')
        with open(a.skill) as fh:
            text = fh.read()
        block = table_block(text)
        header, rows = parse_table(block)
        actions = declared_actions(block)
        if not actions:
            raise Refusal('no `<!-- sqfs-triage-actions: ... -->` line in the v4 block')
        outside = sorted({r[header.index('action')] for r in rows} - set(actions))
        if outside:
            raise Refusal('actions outside the declared vocabulary: %s' % outside)
    except (OSError, Refusal) as e:
        sys.stderr.write('sqfs-triage-v4(standin): %s\n' % e)
        return 2

    if a.table_only:
        for i, row in enumerate(rows):
            print('%d. %s' % (i + 1, row[header.index('label')]))
        return 0

    paths = list(a.envs)
    if not paths and a.envelopes_dir:
        import os
        paths = [os.path.join(a.envelopes_dir, n)
                 for n in sorted(os.listdir(a.envelopes_dir)) if n.endswith('.json')]
    if not paths:
        sys.stderr.write('sqfs-triage-v4(standin): no envelopes\n')
        return 2
    results = []
    for p in paths:
        try:
            with open(p) as fh:
                obj = json.load(fh)
        except Exception as e:
            sys.stderr.write('sqfs-triage-v4(standin): unreadable %s: %s\n' % (p, e))
            return 3
        data = obj
        if isinstance(obj, dict) and 'subject' not in obj and isinstance(obj.get('data'), dict):
            data = obj['data']
        d = decide(header, rows, data)
        results.append({'path': p, 'label': d['label'], 'action': d['action'],
                        'rule': d['rule'], 'row': d['rule'],
                        'cells': d['cells']})
    if a.json:
        json.dump({'results': results}, sys.stdout, indent=1, sort_keys=True)
        sys.stdout.write('\n')
        return 0
    for r in results:
        print('%s\t%s\t%s\t%s' % (r['path'], r['label'], r['action'],
                                  '' if r['rule'] is None else r['rule']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
