#!/usr/bin/env python3
"""Seat-local differential check (not a counter instrument): applies the receipt-side
clause functions of the round-50 port and of the round-41 counter to the REAL
round-41 after-receipts (corpus/evidence/round-41/c1/<id>/, read-only) and compares
them. The port's HANDLER is patched to `squashfs_v4_be` for this check only (the
real receipts are the BE ones), and the port's frozen layout/provenance clauses are
NOT applied (they are LE/r50-specific); what is compared is the shared machinery:
extract root, oracle hits, gap/removal disposition, nonregular-published, and the
projection of a receipt against itself and against a rehosted copy.

usage: python3 -I -B differential-check.py R50_COUNTER R41_COUNTER LANE
"""
import importlib.util, json, os, sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


n50 = load(sys.argv[1], 'c50')
n41 = load(sys.argv[2], 'c41')
lane = sys.argv[3]
n50.HANDLER = 'squashfs_v4_be'          # the real receipts are the BE ones
rule = json.load(open(os.path.join(lane, '.ufo/waves/round-41/c1/gap-rule.json')))
rule50 = dict(rule, claim='R50-C1')
m41, _ = n41.gap_rule_model(json.dumps(rule).encode())
m50, _ = n50.gap_rule_model(json.dumps(rule50).encode())
out = {}
for cid in ('V3', 'V4', 'L3', 'L4'):
    d = os.path.join(lane, 'corpus/evidence/round-41/c1', cid)
    env = json.load(open(os.path.join(d, 'after.json')))
    o41, e1 = n41.parse_oracle(open(os.path.join(d, 'oracle.tsv'), 'rb').read())
    o50, e2 = n50.parse_oracle(open(os.path.join(d, 'oracle.tsv'), 'rb').read())
    nr41, _ = n41.parse_nonregular(open(os.path.join(d, 'nonregular.tsv'), 'rb').read())
    nr50, _ = n50.parse_nonregular(open(os.path.join(d, 'nonregular.tsv'), 'rb').read())
    r41, _ = n41.subject_root(env)
    r50, _ = n50.subject_root(env)
    f41, f50 = n41.published(env), n50.published(env)
    od = (env.get('parameters') or {}).get('output_directory')
    g41 = n41.disposition_check(n41.gaps(env), n41.diagnostics(env), nr41, m41, r41)
    g50 = n50.disposition_check(n50.gaps(env), n50.diagnostics(env), nr50, m50, r50, od)
    nested = n50.nested_roots(env, r50)
    extra = n50.extra_published(o50, f50, r50, nested)
    row = {
        'oracle_parse': [e1, e2], 'oracle_rows': [len(o41), len(o50)],
        'root': [r41, r50],
        'oracle_hits': [n41.oracle_hits([(a, b) for a, b, *_ in o41], f41, r41),
                        n50.oracle_hits(o50, f50, r50, nested)],
        'published_files': len(f50),
        'disposition': [g41[0], g50[0]],
        'disposition_note_equal': g41[1] == g50[1],
        'disposition_note_50': g50[1],
        'nonregular_published': [len(n41.nonregular_published(f41, nr41, r41)),
                                 len(n50.nonregular_published(f50, nr50, r50))],
        'extra_published_r50': len(extra), 'extra_sample': extra[:3],
        'path_shape_ok': n50.path_shape_ok(env),
        'parameters': {k: (env.get('parameters') or {}).get(k)
                       for k in ('max_depth', 'max_output_bytes', 'max_output_files')},
        'output_directory': od,
        'provenance_r41_rule': n41.provenance_ok(od),
        'provenance_r50_rule': n50.provenance_ok(od),
        'projection_equal_41_50': (n41.projection(env, 'plus-extractor')
                                   == n50.projection(env, 'plus-extractor')),
        'removal_diagnostics': sum(1 for x in n50.diagnostics(env)
                                   if n50.diagnostic_typename(x) == 'MaliciousSymlinkRemoved'),
        'removals_resolved_r41': sum(1 for x in n41.diagnostics(env)
                                     if n41.diagnostic_rel(x, r41) is not None),
        'removals_resolved_r50_trusted_root': sum(
            1 for x in n50.diagnostics(env) if n50.diagnostic_rel(x, r50, od) is not None),
    }
    out[cid] = row
print(json.dumps(out, indent=1, sort_keys=True))
