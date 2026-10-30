#!/usr/bin/env python3
"""R51-C1 gap-rule mutation battery (table math, no REA, no counter run).

Seat: MutGapRule (kaidoku round 51, wave 1).  Scope: compute the three-family
disposition-clause verdict per carrier per RULE MUTATION, FROM THE DATA.

Inputs (all read-only, at the declared base revision):
  corpus/evidence/round-50/c1/<id>/after.json        the committed REA 6.5.0 receipt
  tools/round-50/oracle/<id>.nonregular.tsv          the frozen non-regular census
  tools/round-50/gap-rule.json                       the round-50 frozen rule (M0)

Two independent evaluations of the same clause math are run and cross-checked:
  A. this file's own three-family evaluator (independent re-implementation of
     the clause semantics documented at tools/round-50/c1-counter.py:1458-1569)
  B. the frozen counter's own `disposition_check` + `gap_rule_model`, imported
     read-only from the lane tree (no REA, no network, no writes)
A disagreement is a failure of this battery (exit 1).

Exit codes: 0 battery table computed and every cross-check held; 1 a
cross-check or an expectation failed; 2 could not evaluate.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE = 'f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab'
IDS = ('c6430', 'c6490', 'g7581', 'g7582')
HANDLER = 'squashfs_v4_le'

# --------------------------------------------------------------- frozen data IO

def git_show(rev, path):
    p = subprocess.run(['git', '-C', LANE, 'show', '%s:%s' % (rev, path)],
                       capture_output=True)
    if p.returncode != 0:
        raise SystemExit('git show %s:%s failed: %s'
                         % (rev, path, p.stderr.decode(errors='replace').strip()))
    return p.stdout


def parse_nonregular(raw):
    """[(rel, kind, detail)] from a `.nonregular.tsv` table."""
    rows = []
    for line in raw.decode(errors='replace').splitlines():
        if not line.strip():
            continue
        f = line.split('\t')
        if (f[0], f[1]) == ('relative_path', 'kind'):
            continue
        if len(f) < 2 or not f[0] or not f[1]:
            raise SystemExit('bad nonregular row: %r' % (line,))
        rows.append((f[0], f[1], f[2] if len(f) > 2 else None))
    return rows


def strip_rel(rel):
    r = rel
    while r.startswith('./'):
        r = r[2:]
    return r.lstrip('/')


def load_carrier(cid):
    env = json.loads(git_show(BASE, 'corpus/evidence/round-50/c1/%s/after.json' % cid))
    rows = parse_nonregular(git_show(BASE, 'tools/round-50/oracle/%s.nonregular.tsv' % cid))
    nr = env.get('normalized_result') or {}
    gaps = [g for g in (nr.get('extraction_gaps') or []) if isinstance(g, dict)]
    diags = [d for d in (nr.get('diagnostics') or []) if isinstance(d, dict)]
    roots = []
    for d in (nr.get('derivations') or []):
        if isinstance(d, dict) and d.get('handler') == HANDLER:
            cp = d.get('child_path')
            if isinstance(cp, str) and cp.startswith('$output/'):
                cp = cp[len('$output/'):]
            if cp:
                roots.append(cp.rstrip('/'))
    params = env.get('parameters') or {}
    return {
        'id': cid,
        'env': env,
        'rows': rows,
        'gaps': gaps,
        'diags': diags,
        'root': roots[0] if len(roots) == 1 else None,
        'roots': roots,
        'output_directory': params.get('output_directory'),
    }


# ------------------------------------------------- A: independent clause math

def diag_typename(d):
    rep = d.get('report')
    return rep.get('__typename__') if isinstance(rep, dict) else None


def diag_link(d):
    rep = d.get('report')
    return rep.get('link') if isinstance(rep, dict) else None


def resolve_gap_path(rp, root):
    """Gap `relative_path` -> oracle-relative path, segment-bounded."""
    if not isinstance(rp, str) or not rp or root is None:
        return None
    if rp == root:
        return ''
    pre = root.rstrip('/') + '/'
    if not rp.startswith(pre):
        return None
    return rp[len(pre):]


def resolve_diag_link(link, root, output_directory):
    """Removal diagnostic `link` -> oracle-relative path, under the run's trusted root."""
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
    """Three-family disposition verdict for one carrier under one rule model.

    Returns (ok, clause, note, unaccounted).  `clause` is the family that
    fired: path-resolved-gap / structural-gap / removal / required-disposition.
    """
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


# --------------------------------------------- B: the frozen counter's own math

def load_counter(path):
    spec = importlib.util.spec_from_file_location('r50_c1_counter', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def counter_verdict(counter, carrier, rule_bytes):
    model, probs = counter.gap_rule_model(rule_bytes)
    ok, why = counter.disposition_check(
        carrier['gaps'], carrier['diags'], carrier['rows'], model,
        carrier['root'], carrier['output_directory'])
    return ok, why, probs, model


# ----------------------------------------------------------------- the mutations

ALL13 = ['247:0', '230:0', '3:0', '3:1', '3:2',
         '136:0', '136:1', '136:2', '136:3', '136:4', '136:5', '136:6', '136:7']
PTS8 = ['136:%d' % i for i in range(8)]

LAW = {
    'claim': 'R51-C1',
    'allowed': {
        'symlink': ['unpublished-entry'],
        'char-device': ['unpublished-entry'],
        'block-device': [],
        'fifo': ['unpublished-entry'],
        'socket': ['unpublished-entry'],
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
    'structural': {
        'depth-limited': 1,
        'unknown-chunk-handler': 0,
    },
}


def deep_copy(doc):
    return json.loads(json.dumps(doc))


def mutations():
    out = []

    m = deep_copy(LAW)
    m['required']['char-device'] = True
    m['removed']['silent'] = {'char-device': ['247:0']}
    out.append(('M1', 'require char-device, silent whitelist 247:0 only (== the round-50 frozen rule)', m))

    m = deep_copy(LAW)
    m['required']['char-device'] = True
    m['removed']['silent'] = {'char-device': list(ALL13)}
    out.append(('M2', 'require char-device, silent whitelist of all thirteen details', m))

    m = deep_copy(LAW)
    m['required']['char-device'] = True
    m['removed']['silent'] = {'char-device': ['247:0'] + list(PTS8)}
    out.append(('M3', 'require char-device, silent whitelist = 247:0 plus 136:0-136:7 (strict subset)', m))

    m = deep_copy(LAW)
    m['required']['char-device'] = True
    m['removed']['silent'] = {'char-device': list(PTS8)}
    out.append(('M3b', 'require char-device, silent whitelist = 136:0-136:7 only (the other strict-subset reading)', m))

    m = deep_copy(LAW)
    m.pop('removed')
    out.append(('M4', 'drop the symlink-removal diagnostic clause entirely', m))

    m = deep_copy(LAW)
    m['removed']['kinds'] = ['char-device']
    out.append(('M5', 'require symlinks, but only the gap may discharge them (removed.kinds excludes symlink)', m))

    out.append(('M6', "the claims' law encoding (required.char-device=false, no device whitelist)", deep_copy(LAW)))

    m = deep_copy(LAW)
    for k in ('char-device', 'fifo', 'socket'):
        m['allowed'][k] = []
    out.append(('M6s', 'advisory: law with device kinds admitting NO gap kind (a device gap would be red)', m))
    return out


# ------------------------------------------------------------------------ main

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--counter', default=os.path.join(LANE, 'tools/round-50/c1-counter.py'))
    args = ap.parse_args(argv)

    counter = load_counter(args.counter)
    carriers = {cid: load_carrier(cid) for cid in IDS}

    result = {
        'seat': 'MutGapRule',
        'round': 51,
        'wave': 1,
        'base_revision': BASE,
        'generated_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'counter_path_used': args.counter,
        'counter_sha256': hashlib.sha256(open(args.counter, 'rb').read()).hexdigest(),
        'data': {},
        'mutations': [],
        'cross_check': {'agreements': 0, 'disagreements': []},
        '_agree_ids': [],
        'expectations': [],
    }

    # data census (per carrier, from the committed receipt + frozen table)
    for cid, c in carriers.items():
        kinds = {}
        for rel, kind, detail in c['rows']:
            kinds.setdefault(kind, []).append((strip_rel(rel), detail))
        result['data'][cid] = {
            'extract_root': c['root'],
            'derivation_roots': c['roots'],
            'nonregular_rows': len(c['rows']),
            'rows_by_kind': {k: len(v) for k, v in sorted(kinds.items())},
            'char_device_rows': sorted(kinds.get('char-device', [])),
            'gaps_total': len(c['gaps']),
            'gap_kinds': {},
            'diagnostics': [diag_typename(d) for d in c['diags']],
            'removal_targets': sorted(
                x for x in (resolve_diag_link(diag_link(d), c['root'], c['output_directory'])
                            for d in c['diags'])
                if x is not None),
            'output_directory': c['output_directory'],
        }
        gk = result['data'][cid]['gap_kinds']
        for g in c['gaps']:
            gk[g.get('kind')] = gk.get(g.get('kind'), 0) + 1

    # M0: the round-50 frozen rule as committed
    m0_bytes = git_show(BASE, 'tools/round-50/gap-rule.json')
    m0 = json.loads(m0_bytes)
    row = {'id': 'M0', 'description': 'the round-50 frozen rule (committed tools/round-50/gap-rule.json)',
           'rule_sha256': hashlib.sha256(m0_bytes).hexdigest(), 'carriers': {}}
    for cid, c in carriers.items():
        a_ok, a_clause, a_note, a_un = evaluate(c, counter.gap_rule_model(m0_bytes)[0])
        b_ok, b_why, probs, _m = counter_verdict(counter, c, m0_bytes)
        agree = (a_ok == b_ok)
        if agree:
            result['cross_check']['agreements'] += 1
        else:
            result['cross_check']['disagreements'].append(
                {'mutation': 'M0', 'carrier': cid,
                 'independent': [a_ok, a_clause, a_note],
                 'counter': [b_ok, b_why]})
        row['carriers'][cid] = {
            'verdict': 'green' if a_ok else 'red',
            'clause_fired': a_clause,
            'note': a_note,
            'unaccounted_rows': a_un,
            'counter_verdict': 'green' if b_ok else 'red',
            'counter_note': b_why,
            'rule_model_problems': probs,
            'agreement': agree,
        }
    result['mutations'].append(row)

    for mid, desc, rule in mutations():
        raw = json.dumps(rule, indent=2, sort_keys=True).encode()
        row = {'id': mid, 'description': desc,
               'rule_sha256': hashlib.sha256(raw).hexdigest(), 'carriers': {}}
        for cid, c in carriers.items():
            a_ok, a_clause, a_note, a_un = evaluate(c, counter.gap_rule_model(raw)[0])
            b_ok, b_why, probs, _m = counter_verdict(counter, c, raw)
            agree = (a_ok == b_ok)
            if agree:
                result['cross_check']['agreements'] += 1
            else:
                result['cross_check']['disagreements'].append(
                    {'mutation': mid, 'carrier': cid,
                     'independent': [a_ok, a_clause, a_note],
                     'counter': [b_ok, b_why]})
            row['carriers'][cid] = {
                'verdict': 'green' if a_ok else 'red',
                'clause_fired': a_clause,
                'note': a_note,
                'unaccounted_rows': a_un,
                'counter_verdict': 'green' if b_ok else 'red',
                'counter_note': b_why,
                'rule_model_problems': probs,
                'agreement': agree,
            }
        result['mutations'].append(row)

    # ------------------------------------------------------------ expectations
    def verdicts(mid):
        r = next(x for x in result['mutations'] if x['id'] == mid)
        return {cid: r['carriers'][cid]['verdict'] for cid in IDS}

    def clause(mid, cid):
        r = next(x for x in result['mutations'] if x['id'] == mid)
        return r['carriers'][cid]['clause_fired']

    def unacc(mid, cid):
        r = next(x for x in result['mutations'] if x['id'] == mid)
        return r['carriers'][cid]['unaccounted_rows']

    exp = []

    def want(name, got, want_val, why):
        exp.append({'expectation': name, 'observed': got, 'required': want_val,
                    'met': got == want_val, 'why': why})

    v = verdicts('M0')
    want('M0 reproduces the round-50 miss: Cable green, FRITZ!Box red',
         v, {'c6430': 'green', 'c6490': 'green', 'g7581': 'red', 'g7582': 'red'},
         'the committed round-50 counter reported carriers_matched 2')
    v = verdicts('M1')
    want('M1 (require char-device, 247:0-only whitelist) is red on the FRITZ!Box class',
         [v['g7581'], v['g7582']], ['red', 'red'],
         'the twelve non-247:0 char-devices have no disposition')
    want('M1 is green on the Cable class (247:0 silently admitted)',
         [v['c6430'], v['c6490']], ['green', 'green'],
         'the Cable census has exactly one char-device, 247:0')
    v = verdicts('M2')
    want('M2 (all-thirteen whitelist) is green on all four carriers',
         sorted(set(v.values())), ['green'],
         'a full detail whitelist discharges every char-device; the clause math cannot '
         'tell it from the law')
    v = verdicts('M3')
    want('M3 (strict-subset whitelist) is red on the FRITZ!Box class (F10 trap)',
         [v['g7581'], v['g7582']], ['red', 'red'],
         '230:0 and 3:0-3:2 fall outside the subset')
    v = verdicts('M4')
    want('M4 (removal clause dropped) is red on all four carriers',
         sorted(set(v.values())), ['red'],
         'the symlinks that only a removal diagnostic discharges are left unaccounted')
    v = verdicts('M5')
    want('M5 (only the gap may discharge a symlink) is red on all four carriers',
         sorted(set(v.values())), ['red'],
         'the removal diagnostic names a symlink entry that removed.kinds no longer covers')
    v = verdicts('M6')
    want('M6 (the law) is green on all four carriers',
         sorted(set(v.values())), ['green'],
         'char-devices are exempt from the required-disposition clause')
    want('the law fires no clause on any carrier',
         sorted({clause('M6', cid) for cid in IDS}), ['green'],
         'the law must not rely on any of the three families for the device census')
    want('M3 unaccounts exactly the four non-pts, non-led char-devices on the FRITZ!Box class',
         [len(unacc('M3', 'g7581')), len(unacc('M3', 'g7582'))], [4, 4],
         'dev/tiatm 230:0 and dev/ttyp0-2 3:0-3:2')
    want('M1 unaccounts exactly the twelve non-247:0 char-devices on the FRITZ!Box class',
         [len(unacc('M1', 'g7581')), len(unacc('M1', 'g7582'))], [12, 12],
         'the claims name twelve other char-devices')
    want('M4 unaccounts exactly the removal-discharged symlinks (1 Cable / 3 FRITZ!Box)',
         [len(unacc('M4', 'c6430')), len(unacc('M4', 'c6490')),
          len(unacc('M4', 'g7581')), len(unacc('M4', 'g7582'))], [1, 1, 3, 3],
         'the receipts carry 1/1/3/3 MaliciousSymlinkRemoved diagnostics')
    v = verdicts('M3b')
    want('M3b (136:0-136:7 only, no 247:0) is red on the Cable class too',
         [v['c6430'], v['c6490']], ['red', 'red'],
         'the Cable census has only 247:0, which the subset omits')
    want('M3b unaccounts exactly the five char-devices outside the 136:0-136:7 subset '
         '(247:0, 230:0, 3:0-3:2) on the FRITZ!Box class',
         [len(unacc('M3b', 'g7581')), len(unacc('M3b', 'g7582'))], [5, 5],
         'the subset admits eight of the thirteen details')
    want('M3b unaccounts exactly the one Cable char-device (247:0)',
         [len(unacc('M3b', 'c6430')), len(unacc('M3b', 'c6490'))], [1, 1],
         'the Cable census has only 247:0, which the subset omits')
    want('no cross-check disagreement between the independent evaluator and the frozen counter',
         len(result['cross_check']['disagreements']), 0,
         'the two clause implementations must agree on every (mutation, carrier) cell')

    result['expectations'] = exp
    failed = [e for e in exp if not e['met']]
    result['failed_expectations'] = failed
    result['exit_code'] = 0 if (not failed and not result['cross_check']['disagreements']) else 1

    with open(args.out, 'w') as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write('\n')
    return result['exit_code']


if __name__ == '__main__':
    sys.exit(main())
