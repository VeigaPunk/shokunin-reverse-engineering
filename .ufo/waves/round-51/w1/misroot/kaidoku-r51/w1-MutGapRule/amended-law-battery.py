#!/usr/bin/env python3
"""R51-C1 battery, AMENDED mutation set (wave-1 amendments F3/F4/F10) + `law_shape_ok`.

Seat: MutGapRule (kaidoku round 51, wave 1).  The L1 amended
`plans/round-51-claims.md` during wave 1 (amendment record F1-F11).  F3/F4 changed
the rule shape and renumbered the frozen mutation set, and F10 changed the claim
grammar.  This script re-derives the expected-verdict table for the AMENDED set
and adds the new `law_shape_ok` binding, which the amended counter declares in
its BINDINGS tuple but (measured) never assigns.

Everything is table math over the committed round-50 receipts and the frozen
oracle tables at the declared base revision.  No REA run, no network, no lane
write.

Two independent evaluations per cell:
  A. this file's own three-family disposition evaluator
  B. the lane's amended v2 counter `tools/round-51/c1-counter.py`, imported
     read-only (its `gap_rule_model` + `disposition_check` are byte-identical in
     disposition semantics to the round-50 counter; only the claim-label set and
     the new binding differ)

Exit codes: 0 every expectation met; 1 an expectation or a cross-check failed;
2 could not evaluate.
"""
import copy
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE = 'f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab'
IDS = ('c6430', 'c6490', 'g7581', 'g7582')
HANDLER = 'squashfs_v4_le'
DEVICE_KINDS = ('char-device', 'block-device', 'fifo', 'socket')
V1 = os.path.join(LANE, 'tools/round-50/c1-counter.py')
V2 = os.path.join(LANE, 'tools/round-51/c1-counter.py')
ALL13 = ['247:0', '230:0', '3:0', '3:1', '3:2'] + ['136:%d' % i for i in range(8)]
PTS8 = ['136:%d' % i for i in range(8)]


def git_show(rev, path):
    p = subprocess.run(['git', '-C', LANE, 'show', '%s:%s' % (rev, path)],
                       capture_output=True)
    if p.returncode != 0:
        raise SystemExit('git show %s:%s failed' % (rev, path))
    return p.stdout


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_nonregular(raw):
    rows = []
    for line in raw.decode(errors='replace').splitlines():
        if not line.strip():
            continue
        f = line.split('\t')
        if (f[0], f[1]) == ('relative_path', 'kind'):
            continue
        rows.append((f[0], f[1], f[2] if len(f) > 2 else None))
    return rows


def load_carrier(cid):
    env = json.loads(git_show(BASE, 'corpus/evidence/round-50/c1/%s/after.json' % cid))
    rows = parse_nonregular(git_show(BASE, 'tools/round-50/oracle/%s.nonregular.tsv' % cid))
    nr = env.get('normalized_result') or {}
    roots = []
    for d in (nr.get('derivations') or []):
        if isinstance(d, dict) and d.get('handler') == HANDLER:
            cp = d.get('child_path') or ''
            if cp.startswith('$output/'):
                cp = cp[len('$output/'):]
            if cp:
                roots.append(cp.rstrip('/'))
    params = env.get('parameters') or {}
    return {
        'id': cid,
        'gaps': [g for g in (nr.get('extraction_gaps') or []) if isinstance(g, dict)],
        'diags': [d for d in (nr.get('diagnostics') or []) if isinstance(d, dict)],
        'rows': rows,
        'root': roots[0] if len(roots) == 1 else None,
        'output_directory': params.get('output_directory'),
    }


# ------------------------------------------------------------- clause evaluators

def diag_typename(d):
    rep = d.get('report')
    return rep.get('__typename__') if isinstance(rep, dict) else None


def diag_link(d):
    rep = d.get('report')
    return rep.get('link') if isinstance(rep, dict) else None


def resolve_gap_path(rp, root):
    if not isinstance(rp, str) or not rp or root is None:
        return None
    if rp == root:
        return ''
    pre = root.rstrip('/') + '/'
    return rp[len(pre):] if rp.startswith(pre) else None


def resolve_diag_link(link, root, output_directory):
    if not isinstance(link, str) or not link:
        return None
    if not isinstance(output_directory, str) or not os.path.isabs(output_directory):
        return None
    if '..' in output_directory.split('/'):
        return None
    trusted = os.path.dirname(output_directory.rstrip('/'))
    if not trusted or trusted == '/':
        return None
    if not (link == trusted or link.startswith(trusted.rstrip('/') + '/')):
        return None
    segs = [x for x in link.split('/') if x not in ('', '.')]
    tsegs = [x for x in trusted.split('/') if x not in ('', '.')]
    if segs[:len(tsegs)] != tsegs:
        return None
    rsegs = [x for x in root.split('/') if x not in ('', '.')]
    for i in range(len(segs) - len(rsegs), len(tsegs) - 1, -1):
        if segs[i:i + len(rsegs)] == rsegs:
            return '/'.join(segs[i + len(rsegs):])
    return None


def silent_match(detail, allowed):
    if detail is None:
        return False
    for label in allowed:
        if label == 'empty-target':
            if detail == '':
                return True
        elif detail == label:
            return True
    return False


def evaluate(carrier, model):
    """The three-family disposition verdict: (ok, clause, note, unaccounted)."""
    rows = carrier['rows']
    root = carrier['root']
    if root is None:
        return False, 'no-root', 'no single %s derivation root' % HANDLER, []
    allowed = model.get('allowed') or {}
    structural = model.get('structural') or {}
    required = model.get('required') or {}
    removed = model.get('removed') or {}
    by_rel = {rel: (kind, detail) for rel, kind, detail in rows}
    rows_at = {}
    for rel, kind, _d in rows:
        rows_at.setdefault(strip_rel(rel), []).append(rel)
    gapped = {}
    struct_count = {}
    for g in carrier['gaps']:
        kind = g.get('kind')
        rp = g.get('relative_path')
        if rp is None:
            if kind not in structural:
                return False, 'structural-gap', 'gap kind %r has no path and no structural allowance' % kind, []
            struct_count[kind] = struct_count.get(kind, 0) + 1
            continue
        if kind in structural:
            return False, 'structural-gap', 'structural gap kind %r carries a path %r' % (kind, rp), []
        rel = resolve_gap_path(rp, root)
        hits = rows_at.get(rel, []) if rel is not None else []
        if len(hits) != 1:
            return False, 'path-resolved-gap', 'gap path %r matches %d non-regular entries' % (rp, len(hits)), []
        entry_kind = by_rel[hits[0]][0]
        if kind not in allowed.get(entry_kind, []):
            return False, 'path-resolved-gap', (
                'gap kind %r not allowed for %r entry %r (allowed %r)'
                % (kind, entry_kind, hits[0], allowed.get(entry_kind, []))), []
        gapped.setdefault(hits[0], []).append(kind)
    over = {k: [n, structural[k]] for k, n in struct_count.items() if n > structural[k]}
    if over:
        return False, 'structural-gap', 'structural gaps over allowance %r' % (over,), []
    removal_name = removed.get('diagnostic')
    removal_kinds = removed.get('kinds') or []
    removed_rels = {}
    if removal_name:
        for d in carrier['diags']:
            if diag_typename(d) != removal_name:
                continue
            rel = resolve_diag_link(diag_link(d), root, carrier['output_directory'])
            if rel is None:
                return False, 'removal', 'removal diagnostic without a resolvable path', []
            hits = rows_at.get(rel, [])
            if len(hits) != 1:
                return False, 'removal', 'removal resolves to %d non-regular entries at %r' % (len(hits), rel), []
            entry_kind = by_rel[hits[0]][0]
            if entry_kind not in removal_kinds:
                return False, 'removal', (
                    'removal at %r names a %r entry; removed.kinds is %r'
                    % (rel, entry_kind, removal_kinds)), []
            if gapped.get(hits[0]):
                return False, 'removal', 'entry %r is both gapped and removed' % hits[0], []
            removed_rels[hits[0]] = removed_rels.get(hits[0], 0) + 1
    missing = []
    for rel, kind, detail in rows:
        need = required.get(kind, bool(allowed.get(kind)))
        if not need:
            continue
        if gapped.get(rel) or removed_rels.get(rel):
            continue
        allowed_details = (removed.get('silent') or {}).get(kind)
        if allowed_details and silent_match(detail, allowed_details):
            continue
        missing.append(rel)
    if missing:
        return False, 'required-disposition', (
            'required entry with no disposition (no gap, no %s): %d row(s)'
            % (removal_name or 'removal', len(missing))), sorted(missing)
    return True, 'green', (
        '%d gaps, %d removals, on %d non-regular entries'
        % (len(carrier['gaps']), sum(removed_rels.values()), len(rows))), []


def strip_rel(rel):
    r = rel
    while r.startswith('./'):
        r = r[2:]
    return r.lstrip('/')


def law_shape_ok(model):
    """The F3/F4 `law_shape_ok` binding, implemented from its documented text.

    "allowed for the device kinds (char-device, block-device, fifo, socket) must
    be the EMPTY list and removed.silent must name no device detail and
    required[char-device] must be false."

    Returns (ok, reasons).
    """
    reasons = []
    allowed = model.get('allowed') or {}
    for kind in DEVICE_KINDS:
        if kind not in allowed:
            reasons.append('allowed has no %r entry' % kind)
        elif allowed[kind]:
            reasons.append('allowed[%r] is %r, not the empty list' % (kind, allowed[kind]))
    silent = (model.get('removed') or {}).get('silent') or {}
    for kind, details in silent.items():
        if kind in DEVICE_KINDS and details:
            reasons.append('removed.silent[%r] names %d device detail(s)' % (kind, len(details)))
    required = model.get('required') or {}
    if required.get('char-device') is not False:
        reasons.append('required[char-device] is %r, not false' % (required.get('char-device'),))
    return (not reasons), reasons


# ------------------------------------------------------------------ rule fixtures

def amended_law():
    """The F3 rule shape: device kinds admit NO gap kind, no device whitelist."""
    return {
        'claim': 'R51-C1',
        'allowed': {
            'symlink': ['unpublished-entry'],
            'char-device': [],
            'block-device': [],
            'fifo': [],
            'socket': [],
            'dir': [],
        },
        'required': {
            'symlink': True,
            'char-device': False,
            'block-device': False,
            'fifo': False,
            'socket': False,
            'dir': False,
        },
        'removed': {
            'diagnostic': 'MaliciousSymlinkRemoved',
            'kinds': ['symlink'],
            'disposition': 'exclusive',
            'silent': {},
        },
        'structural': {'depth-limited': 1, 'unknown-chunk-handler': 0},
    }


def deep_copy(doc):
    return json.loads(json.dumps(doc))


def amended_mutations():
    """The F4 frozen mutation set, restated as complete gap-rule.json documents."""
    out = []
    law = amended_law()

    m = deep_copy(law)
    m['required']['char-device'] = True
    m['removed']['silent'] = {'char-device': list(ALL13)}
    out.append(('F4-M1', 'all-thirteen whitelist (required.char-device=true, silent names all thirteen)', m))

    m = deep_copy(law)
    m['required']['char-device'] = True
    m['removed']['silent'] = {'char-device': ['247:0']}
    out.append(('F4-M3', "regression: required.char-device=true with only 247:0 silent (the round-50 miss)", m))

    m = deep_copy(law)
    m['required']['char-device'] = True
    m['removed']['silent'] = {'char-device': ['247:0'] + list(PTS8)}
    out.append(('F4-M4', 'regression: strict-subset whitelist (247:0 plus 136:0-136:7)', m))

    out.append(('F4-LAW', "the amended law itself (F3 shape)", deep_copy(law)))

    m = deep_copy(law)
    m['removed']['silent'] = {'char-device': list(ALL13)}
    out.append(('F4-WHITELIST-ONLY',
                'the all-thirteen whitelist WITHOUT required.char-device=true '
                '(the shape the claims call a per-detail whitelist)', m))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args(argv)

    v1 = load(V1, 'c1_v1')
    v2 = load(V2, 'c1_v2_lane')
    carriers = {cid: load_carrier(cid) for cid in IDS}

    res = {
        'seat': 'MutGapRule',
        'round': 51,
        'wave': 1,
        'scope': 'amended mutation set (wave-1 amendments F3/F4/F10) + law_shape_ok',
        'base_revision': BASE,
        'generated_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'v1_counter_sha256': hashlib.sha256(open(V1, 'rb').read()).hexdigest(),
        'v2_lane_counter_sha256': hashlib.sha256(open(V2, 'rb').read()).hexdigest(),
        'cells': [],
        'expectations': [],
        'cross_check': {'agreements': 0, 'disagreements': []},
        'findings': [],
    }

    def cell(rule_id, desc, raw, carrier):
        model_a, probs_a = v1.gap_rule_model(raw)
        model_b, probs_b = v2.gap_rule_model(raw)
        a_ok, a_clause, a_note, a_un = evaluate(carrier, model_a)
        b_ok, b_why = v2.disposition_check(
            carrier['gaps'], carrier['diags'], carrier['rows'], model_b,
            carrier['root'], carrier['output_directory'])
        agree = (a_ok == b_ok)
        if agree:
            res['cross_check']['agreements'] += 1
        else:
            res['cross_check']['disagreements'].append(
                {'rule': rule_id, 'carrier': carrier['id'],
                 'independent': [a_ok, a_clause, a_note], 'counter': [b_ok, b_why]})
        shape_ok, shape_reasons = law_shape_ok(model_a)
        return {
            'rule': rule_id, 'description': desc, 'carrier': carrier['id'],
            'verdict': 'green' if a_ok else 'red',
            'clause_fired': a_clause, 'note': a_note,
            'unaccounted_rows': a_un,
            'law_shape_ok': shape_ok, 'law_shape_reasons': shape_reasons,
            'v1_model_problems': probs_a, 'v2_model_problems': probs_b,
            'v2_counter_verdict': 'green' if b_ok else 'red',
            'agreement': agree,
        }

    # ---- the F2 "fourteenth device" fixture carrier (M2 of the amended set)
    def fourteenth_carrier(cid):
        c = copy.deepcopy(carriers[cid])
        c['rows'] = list(c['rows']) + [('dev/ttyS0', 'char-device', '4:64')]
        return c

    for rule_id, desc, rule in amended_mutations():
        raw = json.dumps(rule, indent=2, sort_keys=True).encode()
        for cid, car in carriers.items():
            res['cells'].append(cell(rule_id, desc, raw, car))
        # the fourteenth-device fixture carrier, under the law and under the whitelist
        if rule_id in ('F4-LAW', 'F4-WHITELIST-ONLY', 'F4-M1'):
            for cid in IDS:
                car = fourteenth_carrier(cid)
                res['cells'].append(cell(rule_id + '+14th', desc + ' [fourteenth-device fixture]',
                                        raw, car))

    def verdicts(rule_id, suffix=''):
        key = rule_id + suffix
        return {c['carrier']: c['verdict'] for c in res['cells'] if c['rule'] == key}

    def shape(rule_id, suffix=''):
        key = rule_id + suffix
        got = [c for c in res['cells'] if c['rule'] == key]
        return (got[0]['law_shape_ok'], got[0]['law_shape_reasons']) if got else (None, [])

    def unacc(rule_id, cid, suffix=''):
        for c in res['cells']:
            if c['rule'] == rule_id + suffix and c['carrier'] == cid:
                return c['unaccounted_rows']
        return []

    def want(name, got, want_val, why):
        res['expectations'].append({'expectation': name, 'observed': got,
                                     'required': want_val, 'met': got == want_val,
                                     'why': why})

    # F4-M1: the all-thirteen whitelist must be RED, and red by law_shape_ok
    v = verdicts('F4-M1')
    want('F4-M1 all-thirteen whitelist: the disposition clause alone is GREEN on all four '
         '(the law and the whitelist are extensionally identical over the measured data)',
         sorted(set(v.values())), ['green'],
         'this is why the amended set adds law_shape_ok: the three-family clause cannot '
         'separate the law from the whitelist over these four carriers')
    ok, reasons = shape('F4-M1')
    want('F4-M1 all-thirteen whitelist: law_shape_ok is FALSE', ok, False,
         'law_shape_ok must be the clause that reddens M1')
    want('F4-M1 law_shape_ok names the device silent whitelist',
         any('removed.silent' in r for r in reasons), True,
         'the reason list must show the whitelist as the offending shape')

    # F4-M3: the round-50 miss reproduction
    v = verdicts('F4-M3')
    want('F4-M3 (247:0-only whitelist) is red on the FRITZ!Box class',
         [v['g7581'], v['g7582']], ['red', 'red'],
         'reproduces the round-50 miss (the twelve non-247:0 char-devices)')
    want('F4-M3 is green on the Cable class',
         [v['c6430'], v['c6490']], ['green', 'green'],
         'the Cable census has exactly one char-device, 247:0')
    want('F4-M3 unaccounts exactly the twelve non-247:0 char-devices on the FRITZ!Box class',
         [len(unacc('F4-M3', 'g7581')), len(unacc('F4-M3', 'g7582'))], [12, 12],
         'the claims name twelve other char-devices')

    # F4-M4: the partial-widening trap
    v = verdicts('F4-M4')
    want('F4-M4 (strict-subset whitelist) is red on the FRITZ!Box class',
         [v['g7581'], v['g7582']], ['red', 'red'],
         'the M50 partial-widening trap')
    want('F4-M4 unaccounts exactly the four char-devices outside the subset',
         [len(unacc('F4-M4', 'g7581')), len(unacc('F4-M4', 'g7582'))], [4, 4],
         'dev/tiatm 230:0 and dev/ttyp0-2 3:0-3:2')

    # the amended law
    v = verdicts('F4-LAW')
    want('the amended law (F3 shape) is green on all four carriers',
         sorted(set(v.values())), ['green'],
         'device kinds admit no gap kind and are not required')
    ok, reasons = shape('F4-LAW')
    want('the amended law satisfies law_shape_ok', ok, True,
         'allowed device kinds are empty, no device silent detail, required.char-device false')

    # the fourteenth-device fixture: GREEN under the law, RED under any whitelist
    v = verdicts('F4-LAW', '+14th')
    want('the fourteenth-device fixture is GREEN under the law (all four carriers)',
         sorted(set(v.values())), ['green'],
         'the law admits any device census: an unlisted fourteenth device needs no disposition')
    v = verdicts('F4-M1', '+14th')
    want('the fourteenth-device fixture is RED under the all-thirteen whitelist',
         sorted(set(v.values())), ['red'],
         'the whitelist names thirteen details, so the fourteenth device has no disposition')
    v = verdicts('F4-WHITELIST-ONLY', '+14th')
    want('the fourteenth-device fixture is RED under the whitelist-only shape too',
         sorted(set(v.values())), ['red'],
         'same reason: the whitelist is a census, not a law')

    # the whitelist-only shape (required.char-device stays false)
    v = verdicts('F4-WHITELIST-ONLY')
    want('the whitelist-only shape is disposition-GREEN on the measured carriers',
         sorted(set(v.values())), ['green'],
         'with required.char-device=false the whitelist is inert for the disposition clause')
    ok, reasons = shape('F4-WHITELIST-ONLY')
    want('the whitelist-only shape still FAILS law_shape_ok', ok, False,
         'law_shape_ok is what distinguishes it')

    want('no cross-check disagreement between the independent evaluator and the lane counter',
         len(res['cross_check']['disagreements']), 0,
         'the two clause implementations must agree on every cell')

    # ---- the law_shape_ok binding is declared but never assigned in the lane counter
    src = open(V2).read()
    bind = re.search(r"^BINDINGS = \((.*?)\)", src, re.M | re.S).group(1)
    names = re.findall(r"'([a-z_]+)'", bind)
    assigned = set(re.findall(r"b\['([a-z_]+)'\]\s*=", src))
    never = [n for n in names if n not in assigned]
    res['binding_audit'] = {
        'counter': V2,
        'bindings': names,
        'assigned_in_measure': sorted(assigned),
        'declared_but_never_assigned': never,
    }
    if never:
        res['findings'].append({
            'id': 'law_shape_ok-never-assigned',
            'severity': 'critical',
            'finding': ("the lane v2 counter declares %r in its BINDINGS tuple but never "
                        "assigns b[%r]; the `met_target` line evaluates "
                        "`all(b[x] is True for x in BINDINGS)`, which raises KeyError on "
                        "the first missing key, so the predicate CRASHES instead of "
                        "returning exit 0 or 1" % (never, never[0])),
            'evidence': 'binding_audit.declared_but_never_assigned',
        })
    # and the --controls interface F2 promises
    flags = re.findall(r"add_argument\(\s*'(--[a-z0-9-]+)'", src)
    promised = ['--controls', '--gap-rule', '--receipts', '--provenance-base',
                '--receipt-fresh-base']
    missing_flags = [f for f in promised if f not in flags]
    res['cli_audit'] = {'counter': V2, 'implemented_flags': flags,
                         'promised_by_claims_F2_but_absent': missing_flags}
    if missing_flags:
        res['findings'].append({
            'id': 'controls-interface-absent',
            'severity': 'critical',
            'finding': ("the lane v2 counter's docstring promises the F2 offline mode but "
                        "none of %r is an argparse flag, so the pre-freeze control driver "
                        "cannot score any rule: every invocation exits 2 with "
                        "`unrecognized arguments`" % (missing_flags,)),
            'evidence': 'cli_audit.promised_by_claims_F2_but_absent',
        })

    res['failed_expectations'] = [e for e in res['expectations'] if not e['met']]
    res['exit_code'] = 1 if (res['failed_expectations'] or res['cross_check']['disagreements']) else 0
    with open(args.out, 'w') as fh:
        json.dump(res, fh, indent=2, sort_keys=True)
        fh.write('\n')
    return res['exit_code']


if __name__ == '__main__':
    sys.exit(main())
