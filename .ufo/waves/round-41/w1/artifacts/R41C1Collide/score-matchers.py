#!/usr/bin/env python3
"""Score real REA 6.5.0 after-receipts against a ground-truth oracle under three
path matchers: the round-40 suffix rule, the round-41 prototype's exact
first-root rule, and the carrier-chunk-anchored exact rule proposed here.

The two lane matchers are not retyped from memory.  They are copied verbatim
from their sources and this script asserts, by AST equality, that its copies are
identical to the lane text:

  same_rel              tools/round-40/c1-counter.py:606-607              (suffix)
  extract_rel           .ufo/waves/round-40/w2/artifacts/R40W2C1Refreeze/
  same_rel (prototype)    c1-counter-exact-match.diff, `+` lines             (exact)

`parse_oracle`, `parse_nonregular`, `published`, `gaps`, `oracle_hits`,
`nonregular_published` and `gap_check` are transcribed from
tools/round-40/c1-counter.py:331-382, 610-616 and 637-700 with exactly one
change: the hard-coded `same_rel(...)` call becomes the `m(...)` matcher
parameter, so the same check body runs under each rule.

Usage:
  score-matchers.py --lane LANE --carriers DIR [--receipts SPEC ...] [--json OUT]

`--carriers DIR` is the build-dev.py output (index.json + per-carrier
oracle.tsv, nonregular.tsv plus a sibling `rea-<id>.log` per run).
`--receipts RECEIPT=ORACLE=NONREG=LABEL` adds one more scored receipt.
Exit 0 when the extraction-identity assertion holds (the score table is data,
not a pass/fail), 1 when a copy is not identical to the lane text, 2 usage.
"""
import argparse
import ast
import json
import os
import sys

# ------------------------------------------------------------- verbatim -----
# tools/round-40/c1-counter.py:606-607


def same_rel(candidate, rel):
    return bool(candidate) and bool(rel) and (candidate == rel or candidate.endswith('/' + rel))


# .ufo/waves/round-40/w2/artifacts/R40W2C1Refreeze/c1-counter-exact-match.diff


def extract_rel(path):
    """A receipt path relative to its chunk extract root.

    unblob extracts a chunk into `<staged name>_extract/`, so a receipt path is
    `<chunk>_extract/<rel>` while the oracle and non-regular tables are relative
    to the extracted filesystem's root. The leading component is dropped only
    when it is that root; a nested extraction keeps the components after the
    first root (`a_extract/b_extract/x` -> `b_extract/x`), which no table row
    names. Null and non-string paths stay null."""
    if not isinstance(path, str):
        return None
    p = path
    while p.startswith('$output/'):
        p = p[len('$output/'):]
    parts = [x for x in p.split('/') if x not in ('', '.')]
    if parts and parts[0].endswith('_extract'):
        parts = parts[1:]
    return '/'.join(parts)


def same_rel_exact(candidate, rel):
    """Exact match of a receipt path against a filesystem-relative path.

    Round-40 wave 2 defect (L2, the counter scored 3/4 at 42c10a58): the former
    rule was `candidate == rel or candidate.endswith('/' + rel)`, so the regular
    file `firmware.bin_extract/usr/bin/busy` satisfied the symlink entry
    `bin/busy` and failed `nonregular_unpublished_ok` on a carrier whose
    extraction is faithful. A path suffix is not a path: the candidate is
    resolved against its chunk extract root and compared for equality, so a
    deeper file can neither publish a non-regular entry nor stand in for an
    oracle row."""
    return bool(rel) and bool(candidate) and extract_rel(candidate) == rel


# ---------------------------------------------------------- transcribed -----
# c1-counter.py:331-382 (parsers), :610-616 (accessors), :637-700 (checks);
# `same_rel(...)` -> `m(...)` throughout.


def parse_oracle(raw):
    if raw is None:
        return [], 'absent'
    rows = []
    for line in raw.decode(errors='replace').splitlines():
        if not line.strip():
            continue
        f = [c.rstrip('\r') for c in line.split('\t')]
        if len(f) < 2:
            return [], 'short row'
        rel, sha = f[0].strip(), f[1].strip().lower()
        if not rel or len(sha) != 64:
            return [], 'bad row %r' % (line,)
        rows.append((rel, sha))
    return (rows, None) if rows else ([], 'no rows')


def parse_nonregular(raw):
    if raw is None:
        return [], 'absent'
    rows = []
    for line in raw.decode(errors='replace').splitlines():
        if not line.strip():
            continue
        f = [c.rstrip('\r') for c in line.split('\t')]
        if len(f) < 2:
            return [], 'short row'
        rel, kind = f[0].strip(), f[1].strip().lower()
        if (rel, kind) == ('relative_path', 'kind'):
            continue
        if not rel or not kind:
            return [], 'empty field in %r' % (line,)
        rows.append((rel, kind))
    return rows, None


def published(env):
    nr = env.get('normalized_result') or {}
    out = []
    for f in (nr.get('files') or []):
        if isinstance(f, dict):
            out.append((f.get('relative_path') or '', f.get('sha256') or '',
                        f.get('size')))
    return out


def gaps(env):
    nr = env.get('normalized_result') or {}
    return list(nr.get('extraction_gaps') or [])


def oracle_hits(oracle, files, m):
    hits = 0
    for rel, sha in oracle:
        if any(sha == fs and m(fp, rel) for fp, fs, _ in files):
            hits += 1
    return hits


def nonregular_published(files, nonreg, m):
    hits = []
    for fp, _, _ in files:
        for rel, _kind in nonreg:
            if m(fp, rel):
                hits.append(fp)
    return hits


def gap_check(gaps_list, nonreg, model, m):
    allowed = model.get('allowed') or {}
    structural = model.get('structural') or {}
    required = model.get('required') or {}
    seen = {}
    struct_count = {}
    for g in gaps_list:
        if not isinstance(g, dict):
            return False, 'non-object gap'
        kind = g.get('kind')
        rp = g.get('relative_path')
        if rp is None:
            if kind not in structural:
                return False, 'gap kind %r has no path and no structural allowance' % (kind,)
            struct_count[kind] = struct_count.get(kind, 0) + 1
            continue
        if kind in structural:
            return False, 'structural gap kind %r carries a path %r' % (kind, rp)
        hits = [r for r, _ in nonreg if m(rp, r)]
        if len(hits) != 1:
            return False, 'gap path %r matches %d non-regular entries %r' % (
                rp, len(hits), hits)
        entry_kind = dict(nonreg)[hits[0]]
        if kind not in allowed.get(entry_kind, []):
            return False, 'gap kind %r not allowed for %r entry %r' % (
                kind, entry_kind, hits[0])
        seen.setdefault(hits[0], []).append(kind)
    over = {k: [n, structural[k]] for k, n in struct_count.items()
            if n > structural[k]}
    if over:
        return False, 'structural gaps over allowance %r' % (over,)
    missing = []
    for rel, kind in nonreg:
        need = required.get(kind, bool(allowed.get(kind)))
        if not need:
            continue
        if not seen.get(rel):
            missing.append(rel)
    if missing:
        return False, 'required gap absent on %r' % (sorted(missing),)
    return True, '%d gaps (%d structural) on %d non-regular entries' % (
        len(gaps_list), sum(struct_count.values()), len(nonreg))


# ------------------------------------------------- proposed correction ------
# The prototype strips the FIRST `_extract` component unconditionally.  That is
# right only while the carrier itself is the chunk at depth 0.  The correction
# reads the anchor out of the receipt instead: the depth-0 `squashfs_v4_*` chunk
# (input_path == '$input', i.e. the carrier file) whose extract root is the one
# leading component every published and gap path shares.  A receipt without that
# chunk (a wrapper carrier: the squashfs is a member, so the published
# filesystem is the member's, not the carrier's) is refused by name rather than
# scored against the wrong base.


def carrier_root(env):
    """(root, why) for the CARRIER's own squashfs chunk, or (None, why not)."""
    nr = env.get('normalized_result') or {}
    depth0 = False
    for c in (nr.get('chunks') or []):
        if not isinstance(c, dict):
            continue
        if (c.get('input_path') == '$input'
                and str(c.get('handler') or '').startswith('squashfs_v4')):
            depth0 = True
    if not depth0:
        return None, ('no squashfs_v4_* chunk at input_path $input '
                      '(wrapper carrier: the published filesystem is a member)')
    firsts = set()
    for f in (nr.get('files') or []):
        p = (f or {}).get('relative_path') or ''
        if p:
            firsts.add(p.split('/')[0])
    for g in (nr.get('extraction_gaps') or []):
        p = (g or {}).get('relative_path') or ''
        if p:
            firsts.add(p.split('/')[0])
    if len(firsts) != 1:
        return None, ('published/gap paths span %d leading components %r'
                      % (len(firsts), sorted(firsts)[:3]))
    root = firsts.pop()
    if not root.endswith('_extract'):
        return None, 'leading component %r is not an extract directory' % (root,)
    return root, None


def same_rel_anchored(env, candidate, rel):
    """Exact match scoped to the carrier chunk's extract root."""
    root, _why = carrier_root(env)
    if root is None or not isinstance(candidate, str) or not rel:
        return False
    p = candidate
    while p.startswith('$output/'):
        p = p[len('$output/'):]
    prefix = root + '/'
    if not p.startswith(prefix):
        return False
    return p[len(prefix):] == rel


# ------------------------------------------------------------------ scoring --


MATCHERS = (
    ('suffix(r40)', lambda env, p, r: same_rel(p, r)),
    ('exact-first-root(proto)', lambda env, p, r: same_rel_exact(p, r)),
    ('exact-carrier-root(fix)', lambda env, p, r: same_rel_anchored(env, p, r)),
)


def score(env, oracle, nonreg, rule):
    out = {}
    files = published(env)
    root, root_why = carrier_root(env)
    for name, matcher in MATCHERS:
        m = (lambda p, r, _mm=matcher, _e=env: _mm(_e, p, r))
        hits = oracle_hits(oracle, files, m)
        esc = nonregular_published(files, nonreg, m)
        ok, why = gap_check(gaps(env), nonreg, rule, m)
        scopable = not (name.startswith('exact-carrier-root') and root is None)
        out[name] = {
            'scopable': scopable,
            'scope_note': root_why,
            'oracle_hits': hits,
            'oracle_files': len(oracle),
            'oracle_hits_ok': scopable and hits == len(oracle),
            'escapes': esc,
            'nonregular_unpublished_ok': scopable and not esc,
            'gaps_ok': scopable and ok,
            'gaps_note': why,
            'matched': scopable and (hits == len(oracle)) and not esc and ok,
        }
    return out


# -------------------------------------------------- extraction identity check


def _fn_ast(src, name):
    """AST dump of a top-level function with its own name normalised.

    The copies keep a round-41 name where the lane text says `same_rel`, so the
    comparison is about the body, which is what the lane fixes."""
    tree = ast.parse(src)
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name == name:
            n.name = 'FN'
            return ast.dump(n, include_attributes=False)
    return None


def _hunk_new_sides(diff_text):
    """Per-hunk new-side source: context plus `+` lines, removals dropped."""
    hunks, cur = [], None
    for line in diff_text.splitlines():
        if line.startswith('@@'):
            if cur is not None:
                hunks.append(cur)
            cur = []
            continue
        if cur is None or line.startswith('\\ No newline'):
            continue
        if line[:1] in ('+', ' '):
            cur.append(line[1:])
    if cur is not None:
        hunks.append(cur)
    return ['\n'.join(h) for h in hunks]


def check_identity(lane, here):
    """The three copies above must be AST-identical to the lane text."""
    problems = []
    counter = open(os.path.join(lane, 'tools/round-40/c1-counter.py')).read()
    mine = open(os.path.abspath(__file__)).read()
    if _fn_ast(counter, 'same_rel') != _fn_ast(mine, 'same_rel'):
        problems.append('same_rel (suffix) copy differs from c1-counter.py')
    diff = open(os.path.join(
        lane, '.ufo/waves/round-40/w2/artifacts/R40W2C1Refreeze/'
              'c1-counter-exact-match.diff')).read()
    proto = None
    for body in _hunk_new_sides(diff):
        lines = body.splitlines()
        cut = [i for i, line in enumerate(lines)
               if line.startswith('def extract_rel')]
        if not cut:
            continue
        lines = lines[cut[0]:]
        for j, line in enumerate(lines[1:], 1):
            if line.startswith('def ') and not line.startswith(
                    ('def extract_rel', 'def same_rel')):
                lines = lines[:j]
                break
        try:
            tree = ast.parse('\n'.join(lines))
        except SyntaxError:
            continue
        names = {}
        for n in tree.body:
            if isinstance(n, ast.FunctionDef):
                key = n.name
                n.name = 'FN'
                names[key] = ast.dump(n, include_attributes=False)
        if 'extract_rel' in names and 'same_rel' in names:
            proto = names
            break
    if proto is None:
        problems.append('prototype hunk with extract_rel+same_rel not found')
    else:
        if proto['extract_rel'] != _fn_ast(mine, 'extract_rel'):
            problems.append('extract_rel copy differs from the prototype diff')
        if proto['same_rel'] != _fn_ast(mine, 'same_rel_exact'):
            problems.append('same_rel (exact) copy differs from the prototype diff')
    return problems


# --------------------------------------------------------------------- main --


def load_env(path):
    d = json.load(open(path))
    if isinstance(d, dict) and 'data' in d and 'normalized_result' not in d:
        return d['data']
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--carriers', required=True)
    ap.add_argument('--receipts', nargs='*', default=[],
                    help='RECEIPT=ORACLE=NONREG=LABEL')
    ap.add_argument('--json', default=None)
    a = ap.parse_args()

    problems = check_identity(a.lane, os.path.dirname(os.path.abspath(__file__)))
    if problems:
        for p in problems:
            print('IDENTITY FAIL', p, file=sys.stderr)
        return 1
    print('identity: same_rel + extract_rel + prototype same_rel are '
          'AST-identical to the lane text')

    rule = json.load(open(os.path.join(
        a.lane, '.ufo/waves/round-40/c1/gap-rule.json')))
    idx = json.load(open(os.path.join(a.carriers, 'index.json')))
    here = os.path.dirname(os.path.abspath(a.carriers))
    rows = []

    def run(label, env_path, oracle_path, nonreg_path, note=''):
        env = load_env(env_path)
        oracle, oerr = parse_oracle(open(oracle_path, 'rb').read())
        nonreg, nerr = parse_nonregular(open(nonreg_path, 'rb').read())
        if oerr or nerr:
            print('table error %s: %r %r' % (label, oerr, nerr), file=sys.stderr)
            return
        res = score(env, oracle, nonreg, rule)
        rows.append({'label': label, 'note': note, 'receipt': env_path,
                     'oracle': oracle_path, 'nonregular': nonreg_path,
                     'carrier_root': carrier_root(env)[0], 'scores': res})
        print('\n== %s  (%s)' % (label, os.path.basename(env_path)))
        print('   carrier_root=%r  oracle_rows=%d nonreg_rows=%d%s'
              % (carrier_root(env)[0], len(oracle), len(nonreg),
                 ('  note: ' + note) if note else ''))
        for name, _m in MATCHERS:
            s = res[name]
            print('   %-26s oracle %d/%d %-4s  nonreg %-4s %-30r  gaps %-4s %s%s'
                  % (name, s['oracle_hits'], s['oracle_files'],
                     'OK' if s['oracle_hits_ok'] else 'FAIL',
                     'OK' if s['nonregular_unpublished_ok'] else 'FAIL',
                     (s['escapes'][:1] if s['escapes'] else ''),
                     'OK' if s['gaps_ok'] else 'FAIL', s['gaps_note'],
                     '' if s['scopable'] else '  [NOT SCORABLE: %s]'
                     % s['scope_note']))

    for cid, meta in sorted(idx['carriers'].items()):
        path = os.path.join(here, 'rea-%s.log' % cid)
        if os.path.exists(path):
            run('%s/d1' % cid, path, meta['oracle'], meta['nonregular'],
                'fresh AVM-genuine carrier, REA --max-depth 1')

    for spec in a.receipts:
        rp, op, np_, label = spec.split('=', 3)
        run(label, rp, op, np_, 'extra')

    if a.json:
        with open(a.json, 'w') as fh:
            json.dump({'identity_ok': True, 'rule': rule, 'rows': rows},
                      fh, indent=1)
            fh.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
