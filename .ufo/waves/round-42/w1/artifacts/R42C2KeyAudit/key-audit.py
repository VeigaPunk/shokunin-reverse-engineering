#!/usr/bin/env python3
"""key-audit.py — static generator->manifest->counter declared-tuple key audit.

Round-42 wave-1 seat R42C2KeyAudit.  Audits ONE contract, the one round-41
mistake M41-1 broke (R41-CL1): the counter's per-carrier declared-feature-tuple
resolution (`observed_features_match_declared`) must terminate in a key the
generator actually writes in EVERY per-carrier manifest-entry shape it emits.

Mechanics (stdlib ast, no third-party imports):

  Writer side (--gen FILE)
    Carrier-entry shapes = dict literals whose keys are all string constants
    and which carry the {id, sha256} fingerprint.  For each shape: every key,
    whether its value is statically None, and, when the value is itself a
    string-keyed dict literal, that dict's subkeys (with their None-ness).

  Reader side (--counter FILE)
    The function(s) whose source contains the binding marker
    "observed_features_match_declared" (fallback: any function whose source
    contains a 'declared' string literal).  Inside them, a two-pass dataflow
    pass collects dotted resolution paths: assignments of `.get()` /
    `['key']` chains bind var -> path, then every `.get()`/subscript chain is
    resolved against that environment.  Chains rooted at a manifest object
    (names `man`/`manifest`) and `for key in (...)" loops over string tuples
    consumed by `man.get(key)` / `man[key]` are reported as manifest-level
    candidate keys (class-map lookups).

  Verdict
    A per-carrier path resolves against a shape when its first segment is a
    key of the shape with a non-None value and, for a second segment, that
    key's statically visible subkeys contain it non-None.  A manifest-level
    candidate key resolves when the generator's top-level manifest literal
    (the {seed, carriers} dict) writes it non-None.  Every shape must have at
    least one resolving path (per-carrier or class-map); otherwise RED.

  Exit codes: 0 green, 1 red, 2 tooling error.  --json OUT dumps the audit.
  --selftest asserts green on an embedded fixed pair and red on an embedded
  broken pair (generator writes 'declared', counter reads 'declared_features')
  and needs no other files.

Documented limits: depth-2 path resolution (deeper nesting is opaque);
interior functions only (methods and lambdas are not scanned); a tuple-valued
or call-valued binding is opaque-non-null.  This is a static contract check,
not a semantic equivalence proof.
"""

import argparse
import ast
import json
import sys

MANIFEST_ROOTS = {'man', 'manifest'}
BINDING_MARKER = 'observed_features_match_declared'
INTEREST = ('feature', 'declared')  # path-interest filter (case-insensitive)


def _source_and_tree(path):
    with open(path, 'rb') as handle:
        src = handle.read()
    return src, ast.parse(src)


def _func_source(src, node):
    lines = src.decode('utf-8', 'replace').splitlines()
    return '\n'.join(lines[node.lineno - 1:node.end_lineno])


# ---------------------------------------------------------------- writer side

def writer_shapes(path):
    """[(shape-id, {key: {'null': bool, 'subkeys': {k: is_none}}}), ...]."""
    src, tree = _source_and_tree(path)
    parents = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[child] = node

    def enclosing(node):
        cur = parents.get(node)
        while cur is not None and not isinstance(
                cur, (ast.FunctionDef, ast.AsyncFunctionDef)):
            cur = parents.get(cur)
        return getattr(cur, 'name', '<module>')

    # top-level manifest literal: {seed, carriers} fingerprint
    manifest_keys = None
    shapes = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        if not node.keys or not all(
                isinstance(k, ast.Constant) and isinstance(k.value, str)
                for k in node.keys):
            continue
        keys = [k.value for k in node.keys]
        if 'id' in keys and 'sha256' in keys:
            entries = {}
            for k, v in zip(node.keys, node.values):
                sub = {}
                if isinstance(v, ast.Dict) and v.keys and all(
                        isinstance(kk, ast.Constant)
                        and isinstance(kk.value, str) for kk in v.keys):
                    sub = {kk.value: isinstance(vv, ast.Constant)
                           and vv.value is None
                           for kk, vv in zip(v.keys, v.values)}
                entries[k.value] = {
                    'null': isinstance(v, ast.Constant) and v.value is None,
                    'subkeys': sub}
            shapes.append({'shape': '%s:%d' % (enclosing(node), node.lineno),
                           'keys': entries})
        elif 'seed' in keys and 'carriers' in keys and manifest_keys is None:
            manifest_keys = {k.value: isinstance(v, ast.Constant)
                             and v.value is None
                             for k, v in zip(node.keys, node.values)}
    return shapes, manifest_keys


# ---------------------------------------------------------------- reader side

def _chain_path(node, env):
    """Dotted path for a receiver expression, or None when not static."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
            and node.func.attr == 'get':
        base = _chain_path(node.func.value, env)
        key = None
        if node.args and isinstance(node.args[0], ast.Constant) \
                and isinstance(node.args[0].value, str):
            key = node.args[0].value
        if key is None:
            return base
        return (base + '.' + key) if base else key
    if isinstance(node, ast.Attribute):
        base = _chain_path(node.value, env)
        return (base + '.' + node.attr) if base else node.attr
    if isinstance(node, ast.Name):
        return env.get(node.id)
    if isinstance(node, ast.Subscript):
        base = _chain_path(node.value, env)
        sl = node.slice
        if sl.__class__.__name__ == 'Index':  # py<3.9 compat
            sl = sl.value
        if isinstance(sl, ast.Constant) and isinstance(sl.value, str):
            return (base + '.' + sl.value) if base else sl.value
        return base
    return None


def reader_resolution(path):
    """(entry paths [(path, line)], manifest candidate keys [(key, line)])."""
    src, tree = _source_and_tree(path)
    lines = src.decode('utf-8', 'replace').splitlines()
    targets = [n for n in ast.walk(tree)
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
               and BINDING_MARKER in _func_source(src, n)]
    if not targets:
        targets = [n for n in ast.walk(tree)
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                   and ("'declared" in _func_source(src, n)
                        or '"declared' in _func_source(src, n))]

    entry_paths = []   # (dotted path, line)
    man_keys = []      # (key, line)
    for func in targets:
        env = {}          # var -> dotted path
        loop_tuples = {}  # for-var -> tuple of string constants
        seen_chains = set()

        def scan_expr(expr, line):
            for node in ast.walk(expr):
                if isinstance(node, ast.Call) and isinstance(
                        node.func, ast.Attribute) and node.func.attr == 'get':
                    root = node.func.value
                    rooted_man = isinstance(root, ast.Name) and \
                        root.id in MANIFEST_ROOTS
                    dynamic_key = not (node.args
                                       and isinstance(node.args[0], ast.Constant)
                                       and isinstance(node.args[0].value, str))
                    if rooted_man and dynamic_key and node.args \
                            and isinstance(node.args[0], ast.Name) \
                            and node.args[0].id in loop_tuples:
                        for k in loop_tuples[node.args[0].id]:
                            if (k, line) not in man_keys:
                                man_keys.append((k, line))
                        continue
                    p = _chain_path(node, env)
                    if p is None:
                        continue
                    if isinstance(root, ast.Name) and root.id in MANIFEST_ROOTS:
                        seg = p.split('.', 1)[-1] if '.' in p else p
                        if (seg, line) not in man_keys:
                            man_keys.append((seg, line))
                    elif p not in seen_chains:
                        seen_chains.add(p)
                        entry_paths.append((p, line))
                elif isinstance(node, ast.Subscript) and isinstance(
                        node.value, ast.Name) and \
                        node.value.id in MANIFEST_ROOTS:
                    sl = node.slice
                    if sl.__class__.__name__ == 'Index':
                        sl = sl.value
                    if isinstance(sl, ast.Constant) and \
                            isinstance(sl.value, str):
                        if (sl.value, line) not in man_keys:
                            man_keys.append((sl.value, line))
                    elif isinstance(sl, ast.Name) and sl.id in loop_tuples:
                        for k in loop_tuples[sl.id]:
                            if (k, line) not in man_keys:
                                man_keys.append((k, line))

        def scan_body(stmts):
            for stmt in stmts:
                for field in ('test', 'iter', 'value', 'exc'):
                    expr = getattr(stmt, field, None)
                    if isinstance(expr, ast.expr):
                        scan_expr(expr, getattr(stmt, 'lineno', 0))
                for expr in getattr(stmt, 'ifs', []) or []:
                    scan_expr(expr, getattr(stmt, 'lineno', 0))
                if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 \
                        and isinstance(stmt.targets[0], ast.Name):
                    p = _chain_path(stmt.value, env)
                    if p is not None:
                        env[stmt.targets[0].id] = p
                if isinstance(stmt, ast.For) and isinstance(
                        stmt.iter, (ast.Tuple, ast.List)) and all(
                        isinstance(e, ast.Constant)
                        and isinstance(e.value, str) for e in stmt.iter.elts) \
                        and isinstance(stmt.target, ast.Name):
                    loop_tuples[stmt.target.id] = [
                        e.value for e in stmt.iter.elts]
                for field in ('body', 'orelse', 'finalbody'):
                    block = getattr(stmt, field, None)
                    if block:
                        scan_body(block)
                if isinstance(stmt, (ast.If, ast.While)):
                    pass
            for stmt in stmts:
                if isinstance(stmt, ast.If):
                    scan_body(stmt.orelse or [])
                if isinstance(stmt, ast.Try):
                    scan_body(stmt.handlers and
                              [h for h in stmt.handlers] or [])
        # py<3.11: ast.Try has orelse/finalbody/handlers; walk generically
        scan_body(func.body)
        # second sweep for else/handler blocks missed above
        for node in ast.walk(func):
            if isinstance(node, ast.If):
                scan_body(node.orelse or [])
            elif node.__class__.__name__ == 'Try':
                for h in getattr(node, 'handlers', []) or []:
                    scan_body(h.body or [])
                scan_body(getattr(node, 'orelse', None) or [])
                scan_body(getattr(node, 'finalbody', None) or [])
    return entry_paths, man_keys


# ------------------------------------------------------------------- verdict

def resolves(entry_path, shape):
    """Does one dotted path resolve against one writer shape (depth 2)?"""
    segs = entry_path.split('.')
    key = shape['keys'].get(segs[0])
    if key is None or key['null']:
        return False
    if len(segs) >= 2:
        return segs[1] in key['subkeys'] and not key['subkeys'][segs[1]]
    return True


def audit(gen_path, counter_path):
    shapes, manifest_keys = writer_shapes(gen_path)
    entry_paths, man_keys = reader_resolution(counter_path)
    interesting = [(p, ln) for p, ln in entry_paths
                   if any(t in p.lower() for t in INTEREST)]
    shape_rows = []
    red = False
    for shape in shapes:
        hit = next(((p, ln) for p, ln in interesting if resolves(p, shape)),
                   None)
        ok = hit is not None
        red = red or not ok
        shape_rows.append({'shape': shape['shape'],
                           'written_keys': sorted(shape['keys']),
                           'resolves': ok,
                           'via': hit[0] if hit else None,
                           'via_line': hit[1] if hit else None})
    man_rows = []
    for key, ln in man_keys:
        ok = manifest_keys is not None and key in manifest_keys \
            and not manifest_keys[key]
        man_rows.append({'manifest_key': key, 'line': ln,
                         'generator_writes_it': bool(ok)})
    return {'gen': gen_path, 'counter': counter_path,
            'reader_paths': [{'path': p, 'line': ln} for p, ln in interesting],
            'shapes': shape_rows, 'manifest_candidates': man_rows,
            'verdict': 'RED' if red else 'GREEN'}


# ------------------------------------------------------------------ selftest

FIXED_GEN = '''
def build_class(seed, k):
    return {'id': 'H%02d' % k, 'sha256': 'x', 'arm': 'after',
            'declared_features': {'handler_set': [], 'gap_kinds': [],
                                  'gap_dependencies': [], 'be_argv': 'n/a',
                                  'symlink_removed': False,
                                  'published': 'nonzero'}}

def build_combo(seed, k):
    return {'id': 'C%02d' % k, 'sha256': 'y', 'arm': 'after',
            'class_expected': None,
            'declared_features': {'handler_set': [], 'gap_kinds': [],
                                  'gap_dependencies': [], 'be_argv': 'no',
                                  'symlink_removed': False,
                                  'published': 'zero'}}

def build_set(seed):
    manifest = {'seed': seed, 'carriers': [], 'classes': []}
    return manifest
'''

FIXED_COUNTER = '''
def measure(man, carriers, env_objs):
    res = {'bindings': {}}
    b = res['bindings']
    feat_missing = []
    for c in carriers:
        decl = c.get('declared_features')
        canon = dict(decl) if isinstance(decl, dict) else None
        if canon is None:
            feat_missing.append(c.get('id'))
            continue
    b['observed_features_match_declared'] = not feat_missing
    return res
'''

BROKEN_GEN = '''
def build_combo(seed, k):
    return {'id': 'C%02d' % k, 'sha256': 'y', 'arm': 'after',
            'class_expected': None,
            'declared': {'handler_set': [], 'gap_kinds': []}}
'''

BROKEN_COUNTER = FIXED_COUNTER


def selftest():
    import os
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as work:
        for tag, gen_src, counter_src, want in (
                ('fixed', FIXED_GEN, FIXED_COUNTER, 'GREEN'),
                ('broken', BROKEN_GEN, BROKEN_COUNTER, 'RED')):
            gp = os.path.join(work, 'gen-%s.py' % tag)
            cp = os.path.join(work, 'counter-%s.py' % tag)
            with open(gp, 'w') as fh:
                fh.write(gen_src)
            with open(cp, 'w') as fh:
                fh.write(counter_src)
            got = audit(gp, cp)['verdict']
            status = 'ok' if got == want else 'FAIL'
            ok = ok and got == want
            print('selftest %-6s want %s got %s [%s]' % (tag, want, got, status))
    if not ok:
        print('selftest FAILED', file=sys.stderr)
    return 0 if ok else 1


# ----------------------------------------------------------------------- cli

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--gen')
    ap.add_argument('--counter')
    ap.add_argument('--json', dest='json_out')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.gen and args.counter):
        ap.error('--gen and --counter are required (or --selftest)')
    try:
        result = audit(args.gen, args.counter)
    except (OSError, SyntaxError) as exc:
        print('key-audit: %s' % exc, file=sys.stderr)
        return 2
    if args.json_out:
        with open(args.json_out, 'w') as fh:
            json.dump(result, fh, indent=2)
            fh.write('\n')
    print('gen      %s' % result['gen'])
    print('counter  %s' % result['counter'])
    for row in result['shapes']:
        print('shape    %-28s %s%s' % (
            row['shape'], 'resolves' if row['resolves'] else 'UNRESOLVED',
            ' via %s (counter:%d)' % (row['via'], row['via_line'])
            if row['via'] else ''))
    for row in result['manifest_candidates']:
        print('man-key  %-24s generator writes it: %s (counter:%d)'
              % (row['manifest_key'], row['generator_writes_it'], row['line']))
    for row in result['reader_paths']:
        print('read     %-28s counter:%d' % (row['path'], row['line']))
    print('verdict  %s' % result['verdict'])
    return 0 if result['verdict'] == 'GREEN' else 1


if __name__ == '__main__':
    sys.exit(main())
