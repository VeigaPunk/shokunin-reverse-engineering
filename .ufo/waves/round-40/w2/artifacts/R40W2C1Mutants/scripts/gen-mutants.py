#!/usr/bin/env python3
"""Generate single-logic mutants of the frozen (42c10a58) C1 counters.

Each mutant replaces exactly one occurrence of one logic-bearing expression.
Every `old` string is asserted to occur exactly once in the pristine bytes, so
a mismatch between my reading and the rev bytes aborts the campaign loudly.
"""
import difflib
import hashlib
import json
import os
import sys

BASE = '/fast/scratch/hyaku/kaidoku-r40/R40W2C1Mutants/base'
OUT = '/fast/scratch/hyaku/kaidoku-r40/R40W2C1Mutants/mutants'
COUNTER = os.path.join(BASE, 'tools/round-40/c1-counter.py')
EXTRA = os.path.join(BASE, 'tools/round-40/c1-extra.py')

# id, file, clause, old, new
MUTANTS = [
    ('M01', 'counter', 'layout_ok: ambiguity guard dropped (both-plausible accepted as LE)',
     "if d['le_plausible'] and not d['be_plausible']:",
     "if d['le_plausible']:"),
    ('M02', 'counter', 'layout_ok: AVM marker inverted (mkfs_time != bytes_used)',
     "d['marker'] = d['mkfs_time'] == d['bytes_used']",
     "d['marker'] = d['mkfs_time'] != d['bytes_used']"),
    ('M03', 'counter', 'gaps_ok: structural allowance opened (path-less gaps never checked)',
     "if kind not in structural:",
     "if False:"),
    ('M04', 'counter', 'gaps_ok: structural allowance strictened (== allowance counts as over)',
     "if n > structural[k]}",
     "if n >= structural[k]}"),
    ('M05', 'counter', 'gaps_ok: required-default off (kinds not explicitly required never required)',
     "need = required.get(kind, bool(allowed.get(kind)))",
     "need = required.get(kind, False)"),
    ('M06', 'counter', 'same_rel: suffix matching dropped (exact path only)',
     "or candidate.endswith('/' + rel))",
     ")"),
    ('M07', 'counter', 'oracle_hits_ok: hit count vacuous (>= 0)',
     "and d['oracle_hits'] == d['oracle_files'])",
     "and d['oracle_hits'] >= 0)"),
    ('M08', 'counter', 'projection: rel_suffix keeps the chunk extract directory',
     "return '/'.join(parts[i + 1:])",
     "return '/'.join(parts[i:])"),
    ('M09', 'counter', 'projection_diff: comparison blinded (always equal)',
     "return not keys, keys, detail",
     "return True, keys, detail"),
    ('M10', 'counter', 'external-carrier load: cache key truncated to 32 hex',
     "fp = os.path.join(carrier_cache, pin + '.bin')",
     "fp = os.path.join(carrier_cache, pin[:32] + '.bin')"),
    ('M11', 'counter', 'frozen_drift: spec key list drops nonregular tables',
     "for key in ('path', 'oracle', 'nonregular'):",
     "for key in ('path', 'oracle'):"),
    ('M12', 'counter', 'receipt_fresh: added-at-freeze counts as fresh',
     "bool(add) and add != freeze and is_ancestor(root, freeze, add)",
     "bool(add) and is_ancestor(root, freeze, add)"),
    ('M13', 'counter', 'handler_ok: any handler satisfies',
     "d['handler_ok'] = HANDLER in chunk_handlers(env)",
     "d['handler_ok'] = bool(chunk_handlers(env))"),
    ('M14', 'counter', 'chunks_ok: failed flag inverted-to-none (failed chunks pass)',
     "return any(isinstance(c, dict) and c.get('extraction_failed')",
     "return any(isinstance(c, dict) and c.get('extraction_failed') is None"),
    ('M15', 'counter', 'sourced binding: opened-date check dropped',
     "if c[0] in src_ids and c[8] == OPENED and (ENTRY in used or STEM in used):",
     "if c[0] in src_ids and (ENTRY in used or STEM in used):"),
    ('M16', 'counter', 'met_target gate: carriers_matched == target dropped',
     "res['carriers_matched'] == target",
     "True"),
    ('E01', 'extra', 'oracle_rederived: row compare reduced to row counts',
     "ok_f = rows(open(f, 'rb').read()) == rows(fo)",
     "ok_f = len(rows(open(f, 'rb').read())) == len(rows(fo))"),
    ('E02', 'extra', 'sourced_new: base-absence check dropped (re-used S-id counts as new)',
     "if s not in at_base and s in at_rev",
     "if s in at_rev"),
    ('E03', 'extra', 'oracle_rederived: cache pin compare broken (upper-case pin)',
     "hexdigest() != pin:",
     "hexdigest() != pin.upper():"),
    ('E04', 'extra', 'frontier_content: supersede requirement dropped',
     "and 'supersede' in l.lower():",
     "and True:"),
]

manifest = []
for mid, which, clause, old, new in MUTANTS:
    src_path = COUNTER if which == 'counter' else EXTRA
    with open(src_path, 'rb') as fh:
        src = fh.read().decode('utf-8')
    n = src.count(old)
    if n != 1:
        print('ABORT %s: %d occurrences of %r' % (mid, n, old[:60]))
        sys.exit(1)
    mutated = src.replace(old, new, 1)
    name = '%s-%s.py' % (mid, which)
    with open(os.path.join(OUT, name), 'w') as fh:
        fh.write(mutated)
    diff = ''.join(difflib.unified_diff(
        src.splitlines(True), mutated.splitlines(True),
        fromfile='pristine/' + os.path.basename(src_path),
        tofile='mutant/' + name))
    with open(os.path.join(OUT, name.replace('.py', '.diff')), 'w') as fh:
        fh.write(diff)
    manifest.append({
        'id': mid, 'file': os.path.basename(src_path), 'clause': clause,
        'old': old, 'new': new,
        'sha256_mutant': hashlib.sha256(mutated.encode()).hexdigest(),
        'sha256_pristine': hashlib.sha256(src.encode()).hexdigest(),
    })

with open(os.path.join(OUT, 'manifest.json'), 'w') as fh:
    json.dump(manifest, fh, indent=1)
print('MUTANTS_OK %d' % len(manifest))
for m in manifest:
    print('%s\t%s\t%s' % (m['id'], m['file'], m['clause']))
