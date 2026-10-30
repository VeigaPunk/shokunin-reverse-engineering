#!/usr/bin/env python3
"""MutTriV6 probe - measure the v6 mutation battery's expectations OFFLINE.

Reads (read-only):
  * tools/round-50-c3/sqfs-triage-v5.py                    (the v5 instrument)
  * .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/  (126 envelopes)
  * .ufo/waves/round-50/w3/ExecTriageControls/ctl-*.skill.md    (round-50 control surfaces)
  * .ufo/waves/round-50/c3/ctl-junk.skill.md                   (the unique-label junk surface)

Writes: receipts into the seat dir only.  No REA, no network, no lane write.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
V5 = os.path.join(LANE, 'tools/round-50-c3/sqfs-triage-v5.py')
ENV = os.path.join(LANE, '.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes')
W3 = os.path.join(LANE, '.ufo/waves/round-50/w3/ExecTriageControls')
C3 = os.path.join(LANE, '.ufo/waves/round-50/c3')
OUTDIR = os.environ.get('PROBE_OUT', '/fast/scratch/hyaku/kaidoku-r51/w1-MutTriV6/out')

CROSS_READ_ACTIONS = ('cross-read-legacy',)
# The frozen reader census for FAILED bodies: the ddwrt no-pad body has NO reader
# (corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md:104 - unsquashfs exit 1,
# 7z exit 2, receipt v3-readers).  Every other FAILED body in the corpus is on a
# reader-backed family (v1/v2/v3).
NO_READER_FAILED_BODIES = ('dmg_Z3_v3ddwrt_inode_table',)


def load_v5():
    spec = importlib.util.spec_from_file_location('v5', V5)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_text(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()


def sha256_file(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


# ----------------------------------------------------------------- the v6 table

def v6_rows(v5):
    """The v6 table: legacy row loses ddwrt, the unreadable row is inserted after it."""
    rows = [list(r) for r in v5.V5_ROWS]
    i = [n for n, r in enumerate(rows) if r[0] == 'legacy-body-failure'][0]
    rows[i][4] = 'squashfs_v1,squashfs_v2,squashfs_v3'
    new = ['legacy-body-unreadable', 'extract_firmware', 'unblob', 'squashfs_*',
           'squashfs_v3_ddwrt', 'extractor-failure+', '*', '*', '*', '0',
           'preserve-unresolved',
           'the failing chunk is a reader-backed v1-v3 body whose readers ALL refuse -> '
           'no second reader exists, so prescribe no cross-read: keep the failure '
           'unresolved',
           'R51-C2; round-51 plans/round-51-claims.md R51-C2']
    rows.insert(i + 1, new)
    return rows


def v6_block(v5, rows=None):
    rows = rows if rows is not None else v6_rows(v5)
    return v5.render_table(rows, v5.V5_ACTIONS, v5.MARKER_V5)


# ----------------------------------------------------------------- the v6 evaluator

def make_evaluate_v6(v5):
    ddwrt = frozenset(('squashfs_v3_ddwrt',))
    base = v5.evaluate

    def evaluate_v6(feat):
        g = set(feat['G'])
        if ('extractor-failure' in g and feat['P'] == 0
                and v5._meets(set(feat['HF']), ddwrt)):
            return 'legacy-body-unreadable', 'preserve-unresolved', 7
        return base(feat)
    return evaluate_v6


# ----------------------------------------------------------------- the audit

def audit_violations(v5, entries, table_action):
    """Every FAILED-body envelope whose PRESCRIBED action is a cross-read while the
    frozen reader census says the body has no reader."""
    out = []
    for eid, _path in entries:
        feat = v5.load_envelope(_path)
        if 'extractor-failure' in set(feat['G']) and feat['P'] == 0:
            act = table_action.get(eid)
            if act in CROSS_READ_ACTIONS and eid in NO_READER_FAILED_BODIES:
                out.append({'envelope': eid, 'table_action': act,
                            'reader_census': 'no-reader'})
    return out


# ----------------------------------------------------------------- the comparison

def compare(v5, evaluator, rules, entries):
    mismatches = []
    table_action = {}
    for eid, path in entries:
        feat = v5.load_envelope(path)
        rule = v5.classify(rules, feat)
        t_label, t_action = v5.decision(rule)
        table_action[eid] = t_action
        e_label, e_action, _step = evaluator(feat)
        if t_label != e_label or t_action != e_action:
            mismatches.append({'envelope': eid, 'table_label': t_label,
                               'table_action': t_action,
                               'evaluator_label': e_label,
                               'evaluator_action': e_action})
    return mismatches, table_action


def surface(name, path):
    with open(path, 'r', encoding='utf-8') as fh:
        text = fh.read()
    return name, path, text


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    v5 = load_v5()
    evaluate_v6 = make_evaluate_v6(v5)
    entries = v5.envelope_entries(ENV)
    assert len(entries) == 126, len(entries)

    surfaces = [
        surface('ctl-do-nothing', os.path.join(W3, 'ctl-do-nothing.skill.md')),
        surface('ctl-guard-deleted', os.path.join(W3, 'ctl-guard-deleted.skill.md')),
        surface('ctl-action-swapped', os.path.join(W3, 'ctl-action-swapped.skill.md')),
        surface('ctl-junk', os.path.join(C3, 'ctl-junk.skill.md')),
    ]

    report = {'probe': 'MutTriV6 v6-battery expectation probe',
              'utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
              'v5_sha256': sha256_file(V5),
              'envelopes': len(entries),
              'reader_census_no_reader_failed_bodies': list(NO_READER_FAILED_BODIES),
              'surfaces': [], 'mutants': []}

    # ---- the four round-50 carryover surfaces, under the v5 evaluator (baseline)
    for name, path, text in surfaces:
        rules, info = v5.parse_skill(text)
        mm5, _ta = compare(v5, v5.evaluate, rules, entries)
        mm6, ta6 = compare(v5, evaluate_v6, rules, entries)
        av6 = audit_violations(v5, entries, ta6)
        report['surfaces'].append({
            'surface': name, 'path': path, 'sha256': sha256_file(path),
            'table_version': info['version'], 'rules': info['rules'],
            'v5_evaluator_pair_mismatches': len(mm5),
            'v6_evaluator_pair_mismatches': len(mm6),
            'v6_audit_violations': len(av6),
            'v6_audit_violation_ids': [v['envelope'] for v in av6],
            'v6_mismatch_detail': mm6[:40],
        })

    # ---- the v6 table and its mutants
    base_rows = v6_rows(v5)
    base_text = v6_block(v5, base_rows)

    def mutate_delete_unreadable(rows):
        out = [list(r) for r in rows]
        del out[[n for n, r in enumerate(out) if r[0] == 'legacy-body-unreadable'][0]]
        return out

    def mutate_swap_unreadable_action(rows):
        out = [list(r) for r in rows]
        out[[n for n, r in enumerate(out) if r[0] == 'legacy-body-unreadable'][0]][10] = \
            'cross-read-legacy'
        return out

    def mutate_broaden_legacy_glob(rows):
        out = [list(r) for r in rows]
        out[[n for n, r in enumerate(out) if r[0] == 'legacy-body-failure'][0]][4] = \
            'squashfs_v[123]*'
        return out

    def mutate_delete_legacy_row(rows):
        out = [list(r) for r in rows]
        del out[[n for n, r in enumerate(out) if r[0] == 'legacy-body-failure'][0]]
        return out

    def mutate_delete_clean_unverified(rows):
        out = [list(r) for r in rows]
        del out[[n for n, r in enumerate(out) if r[0] == 'clean-unverified'][0]]
        return out

    def mutate_swap_clean_action(rows):
        out = [list(r) for r in rows]
        out[[n for n, r in enumerate(out) if r[0] == 'clean'][0]][10] = 'inspect-input'
        return out

    def mutate_no_reader_family_to_clean(rows):
        out = [list(r) for r in rows]
        i = [n for n, r in enumerate(out) if r[0] == 'clean-unverified'][0]
        parts = [p for p in out[i][3].split(',') if p != 'squashfs_v3_broadcom']
        out[i][3] = ','.join(parts)
        return out

    def mutate_precedence_swapped(rows):
        out = [list(r) for r in rows]
        i = [n for n, r in enumerate(out) if r[0] == 'clean-unverified'][0]
        row = out.pop(i)
        j = [n for n, r in enumerate(out) if r[0] == 'clean'][0]
        out.insert(j + 1, row)
        return out

    def mutate_blank_cell(rows):
        out = [list(r) for r in rows]
        out[[n for n, r in enumerate(out) if r[0] == 'clean-unverified'][0]][3] = ''
        return out

    MUTANTS = [
        ('v6-pristine', base_rows),
        ('unreadable-row-deleted', mutate_delete_unreadable(base_rows)),
        ('unreadable-action-swapped-to-cross-read',
         mutate_swap_unreadable_action(base_rows)),
        ('legacy-glob-broadened-to-squashfs_v[123]*',
         mutate_broaden_legacy_glob(base_rows)),
        ('legacy-row-deleted', mutate_delete_legacy_row(base_rows)),
        ('clean-unverified-row-deleted', mutate_delete_clean_unverified(base_rows)),
        ('clean-row-action-swapped', mutate_swap_clean_action(base_rows)),
        ('no-reader-family-moved-to-clean', mutate_no_reader_family_to_clean(base_rows)),
        ('precedence-order-swapped', mutate_precedence_swapped(base_rows)),
        ('blanked-handler-cell', mutate_blank_cell(base_rows)),
    ]
    for mname, rows in MUTANTS:
        text = v6_block(v5, rows)
        try:
            rules, info = v5.parse_skill(text)
        except Exception as exc:            # a malformed table is a refusal
            report['mutants'].append({'mutant': mname, 'parse_error': str(exc)[:160]})
            continue
        mm, ta = compare(v5, evaluate_v6, rules, entries)
        av = audit_violations(v5, entries, ta)
        report['mutants'].append({
            'mutant': mname, 'rules': info['rules'],
            'pair_mismatches': len(mm),
            'mismatch_envelopes': [m['envelope'] for m in mm],
            'mismatch_detail': mm[:8],
            'audit_violations': len(av),
            'audit_violation_ids': [v['envelope'] for v in av],
        })

    out = os.path.join(OUTDIR, 'probe-v6-battery.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print(json.dumps({'surfaces': [{k: v for k, v in s.items()
                                    if k not in ('v6_mismatch_detail',)}
                                   for s in report['surfaces']],
                      'mutants': report['mutants']}, indent=1, sort_keys=True))
    print('json: %s' % out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
