#!/usr/bin/env python3
"""Scratch prototype: measure what each v6 mutation flips.

Ports the v5 table/evaluator from tools/round-50-c3/sqfs-triage-v5.py (read-only),
adds the v6 row + audit + census clause, and measures every candidate mutation
against the frozen 126-envelope corpus and a synthetic fixture set.
"""
import importlib.util, os, sys, json, hashlib, datetime

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec = importlib.util.spec_from_file_location('v5', LANE + '/tools/round-50-c3/sqfs-triage-v5.py')
v5 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v5)

# ---- census (frozen reader census, per family, from the round-49 entry) ----
# families whose readers ALL refuse on every measured variant -> no cross-read executable
NO_VALIDATED_READER = ('squashfs_v2_nonstandard', 'squashfs_v3_nonstandard',
                       'squashfs_v3_ddwrt')
# broadcom has a PARTIAL reader (7-Zip lists it) -> cross-read is executable, no violation
PARTIAL_READER = ('squashfs_v3_broadcom',)
CROSS_READ_ACTIONS = ('cross-read-legacy',)

# ---- the v6 table draft: v5 rows, legacy cell narrowed, new row inserted ----
def _v6_rows():
    rows = [list(r) for r in v5.V5_ROWS]
    i = v5._row_index(rows, 'legacy-body-failure')
    rows[i][4] = 'squashfs_v1,squashfs_v2,squashfs_v3'          # ddwrt removed
    new = ['legacy-body-unreadable', 'extract_firmware', 'unblob', 'squashfs_*',
           'squashfs_v3_ddwrt', 'extractor-failure+', '*', '*', '*', '0',
           'preserve-unresolved',
           'the failing chunk is a reader-backed-family body whose readers all refuse '
           '-> no cross-read is executable; keep the failure unresolved',
           'R52-C2; round-49 W2Skill.md F1; round-52 plans/round-52-claims.md R52-C2']
    rows.insert(i + 1, new)                                       # BELOW legacy-body-failure
    return rows

V6_ROWS = _v6_rows()
V6_ACTIONS = v5.V5_ACTIONS  # vocabulary unchanged: preserve-unresolved already present

# ---- the v6 evaluator (fixed, independent of the table) ----
def evaluate_v6(feat):
    op, pv = feat['OP'], feat['PV']
    f, g, d = feat['F'], set(feat['G']), set(feat['D'])
    be, sr, p, hf = feat['BE'], feat['SR'] == 'yes', feat['P'], feat['HF']
    if op != v5.OPERATION_TOKEN or pv != 'unblob':
        return v5.DEFAULT_LABEL, v5.DEFAULT_ACTION, 1
    if not f and 'depth-limited' in g:
        return 'container-depth-limited', 'raise-depth', 2
    if not f:
        return 'no-squashfs-chunk', 'inspect-input', 3
    if 'missing-extractor-dependency' in g:
        if 'sasquatch-v4be' in d:
            return 'dep-missing-be', 'install-extractor-be', 4
        if 'sasquatch' in d:
            return 'dep-missing-le', 'install-extractor-le', 4
    if v5.FAILURE_KIND in g and p > 0:
        return 'partial-body-failure', 'salvage-partial', 5
    if v5.FAILURE_KIND in g and p == 0 and be == 'no' and 'squashfs_v4_be' in hf:
        return 'avm-marker-be-dropped', 'wrap-extractor-be', 6
    if v5.FAILURE_KIND in g and p == 0 and v5._meets(hf, ('squashfs_v3_ddwrt',)):
        return 'legacy-body-unreadable', 'preserve-unresolved', 7
    if v5.FAILURE_KIND in g and p == 0 and v5._meets(hf, v5.READER_BACKED_SET):
        return 'legacy-body-failure', 'cross-read-legacy', 7
    if v5.FAILURE_KIND in g and p == 0 and v5._meets(hf, v5.NO_READER_SET):
        return 'no-reader-failure', 'preserve-unresolved', 8
    if v5.FAILURE_KIND in g and p == 0:
        return 'body-extractor-failure', 'preserve-failure', 9
    if 'unknown-chunk-handler' in g:
        return 'unknown-residue', 'isolate-residue', 10
    if 'depth-limited' in g:
        return 'depth-limited', 'raise-depth', 11
    if sr and 'unpublished-entry' in g:
        return 'mixed-symlinks', 'audit-symlinks', 12
    if sr and not g:
        return 'escaping-symlink-removed', 'expect-link-absent', 13
    if g == {'unpublished-entry'}:
        return 'in-tree-symlink-metadata', 'count-gap', 14
    if not g:
        if p > 0:
            if v5._meets(f, v5.NO_READER_SET):
                return 'clean-unverified', 'record-unverified', 15
            return 'clean', 'none', 16
        return 'clean-empty', 'confirm-empty', 16
    return v5.DEFAULT_LABEL, v5.DEFAULT_ACTION, 17

# ---- the executability audit (new, frozen) ----
def audit_executability(rules, scope):
    """Every FAILED-body envelope's prescribed action vs the family's reader census."""
    findings = []
    for eid, path, feat in scope:
        if 'extractor-failure' not in feat['G'] or feat['P'] != 0:
            continue
        families = set(feat['HF'])
        unreadable = sorted(families & set(NO_VALIDATED_READER))
        if not unreadable:
            continue
        rule = v5.classify(rules, feat)
        label, action = v5.decision(rule)
        if action in CROSS_READ_ACTIONS:
            findings.append({'envelope': eid, 'label': label, 'action': action,
                             'families': unreadable})
    return findings

def census_outside(registry_paths, census_paths):
    return sorted(set(registry_paths) - set(census_paths))

# ---- corpus + fixtures ----
CORPUS = LANE + '/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes'
def load_corpus():
    out = []
    for eid, path in v5.envelope_entries(CORPUS):
        out.append((eid, path, v5.load_envelope(path)))
    return out

def v6_fixtures():
    """v5 fixtures + the ddwrt FAILED-body pair the v6 change owns."""
    rows = []
    for name, env, want in v5.FIXTURES:
        rows.append((name, env, want))
    rows.append(('v3ddwrt-failed', v5._env(handler='squashfs_v3_ddwrt',
                                           gaps=['extractor-failure'], be='-be', files=0),
                  ('legacy-body-unreadable', 'preserve-unresolved')))
    return rows

def parse(rows, actions=V6_ACTIONS, marker=None):
    # the v5 parser only reads the v5/v4 markers; v6 would add its own marker and
    # prefer it, falling back to v5 for the before-arm.  For the prototype we render
    # at the v5 marker so the frozen v5 parser can be reused verbatim.
    block = v5._render(rows, actions, marker or v5.MARKER_V5)
    rules, info = v5.parse_skill(v5.SKELETON.format(block=block))
    return rules, info

def pairs(rules, fixtures):
    out = {}
    for name, env, _w in fixtures:
        feat = v5.features(env)
        label, action = v5.decision(v5.classify(rules, feat))
        out[name] = (label, action)
    return out

def score(rules, scope, fixtures):
    """(pair mismatches, audit findings) of a table against the v6 evaluator."""
    mism = []
    for eid, path, feat in scope:
        label, action = v5.decision(v5.classify(rules, feat))
        ev = evaluate_v6(feat)[:2]
        if (label, action) != ev:
            mism.append({'envelope': eid, 'table': [label, action], 'evaluator': list(ev)})
    audit = audit_executability(rules, scope)
    return mism, audit
