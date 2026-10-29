#!/usr/bin/env python3
"""What-if: the effect of moving squashfs_v3_ddwrt into the no-reader set.

The claim (plans/round-50-attempt2-claims.md R50-C3) routes the ddwrt family as
reader-backed, citing the round-49 entry's reader census.  That census is
FIXTURE-level and it says (entry :104) that "squashfs_v3_nonstandard and
squashfs_v3_ddwrt's no-pad fixture: both readers refuse".  Re-measuring the
round-42 fixture bytes shows 6 of the 7 ddwrt fixtures have NO reader at all.

This script measures, on the frozen held-out corpus, the claim's rule as written
and the fixture-correct variant, changing BOTH the table cells and the evaluator
constants together (the two must agree, or the comparison is meaningless).  It
changes nothing on disk; it is a decision aid for the L1.
"""
import importlib.util, json, os, sys

INST, E = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('v5', INST)
v5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v5)


def table_labels(no_reader, reader_backed):
    rows = []
    for row in v5.V5_ROWS:
        row = list(row)
        if row[0] == 'legacy-body-failure':
            row[4] = ','.join(reader_backed)
        if row[0] in ('clean-unverified', 'no-reader-failure'):
            row[3] = ','.join(no_reader)
            if row[0] == 'no-reader-failure':
                row[4] = ','.join(no_reader)
        rows.append(row)
    block = v5.render_table(rows)
    rules, _info = v5.parse_skill(v5.SKELETON.format(block=block))
    out = {}
    for name in sorted(os.listdir(E)):
        p = os.path.join(E, name, 'envelope.json')
        if not os.path.isfile(p):
            continue
        feat = v5.load_envelope(p)
        rule = v5.classify(rules, feat)
        out[name] = v5.decision(rule)
    return out


def evaluator_labels(no_reader, reader_backed):
    v5.NO_READER_SET = frozenset(no_reader)
    v5.READER_BACKED_SET = frozenset(reader_backed)
    out = {}
    for name in sorted(os.listdir(E)):
        p = os.path.join(E, name, 'envelope.json')
        if not os.path.isfile(p):
            continue
        out[name] = v5.evaluate(v5.load_envelope(p))[:2]
    return out


NR = list(v5.NO_READER_FAMILIES)
RB = list(v5.READER_BACKED_V1V3)
claim_table = table_labels(NR, RB)
claim_eval = evaluator_labels(NR, RB)
nr2 = NR + ['squashfs_v3_ddwrt']
rb2 = [h for h in RB if h != 'squashfs_v3_ddwrt']
fix_table = table_labels(nr2, rb2)
fix_eval = evaluator_labels(nr2, rb2)

claim_mismatch = {k for k in claim_table if claim_table[k] != claim_eval[k]}
fix_mismatch = {k for k in fix_table if fix_table[k] != fix_eval[k]}
moved = {k: (claim_table[k], fix_table[k]) for k in claim_table
         if claim_table[k] != fix_table[k]}

print('envelopes: %d' % len(claim_table))
print('CLAIM rule (ddwrt reader-backed): pair mismatches = %d' % len(claim_mismatch))
print('FIXTURE-correct rule (ddwrt no-reader): pair mismatches = %d' % len(fix_mismatch))
print('labels that MOVE: %d' % len(moved))
for k in sorted(moved):
    print('  %-52s claim %-34s -> fixture %s' % (k, str(moved[k][0]), str(moved[k][1])))
print()
print('the ddwrt FAILURE envelope under each rule:')
for k in ('dmg_Z3_v3ddwrt_inode_table',):
    print('  %-52s claim %-34s -> fixture %s' % (k, str(claim_table.get(k)), str(fix_table.get(k))))
