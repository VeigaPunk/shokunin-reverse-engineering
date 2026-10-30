#!/usr/bin/env python3
"""R52 gap-rule mutation battery: clause math over the COMMITTED round-50 bytes.

Seat MutGapRule (kaidoku round 52, wave r52-w1). Scope: the gap-rule TEXT only.
No counter run, no REA, no carrier bytes. Inputs are the committed lane bytes:

  tools/round-50/gap-rule.json                      (the frozen round-50 rule)
  tools/round-50/oracle/<id>.nonregular.tsv          (committed non-regular census)
  corpus/evidence/round-50/c1/<id>/after.json        (committed REA envelope)
  .ufo/waves/round-50/l1/scores/c1-after-attempt2.json  (committed round-50 verdict)

The clause math below is a faithful re-implementation of the three-family
disposition check in tools/round-50/c1-counter.py (`disposition_check`,
`gap_rule_model`, `parse_nonregular`, `extract_rel`, `strip_rel`,
`diagnostic_rel`, `silent_detail_matches`), written so that it can be run over
an ARBITRARY rule text without the counter (no carrier bytes needed: the
envelopes and the oracle tables are the frozen data the counter itself uses).

ANCHOR: applied to the frozen round-50 rule this script must reproduce the
committed round-50 receipt's per-carrier `gaps_ok` (true, true, false, false)
and its failure note. If the anchor does not reproduce, the clause math is
wrong and every mutant verdict below is inconclusive.

Families (as in the counter's docstring, R41C1DevCore 7.1):
  F1 path-resolved gap  a gap with a relative_path resolves (exactly, segment
                        bound) to exactly one non-regular row, and its kind is
                        listed in allowed[<row kind>]
  F2 structural gap     a gap with relative_path null has its kind in
                        `structural` and does not exceed that kind's allowance
  F3 removal            every diagnostic whose __typename__ the rule names is a
                        removal: it resolves at its exact path to exactly one
                        non-regular row whose kind is in removed.kinds, and
                        that row carries no gap (exclusive)
  R  required rows      every row whose kind is required carries exactly one
                        disposition: an allowed gap, a removal, or nothing at
                        all when removed.silent lists that row's kind/detail

law_shape_ok is the round-52 rule-SHAPE clause (the claims' wording):
  no char-device/fifo/socket/block-device detail under removed.silent, and
  `allowed` for those kinds is the empty list.

Exit code: 0 when every computed verdict equals the independently derived
EXPECTED matrix (the derivation is in the report), 1 otherwise.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
IDS = ('c6430', 'c6490', 'g7581', 'g7582')
DEVICE_KINDS = ('char-device', 'fifo', 'socket', 'block-device')

RULE_R50 = os.path.join(LANE, 'tools/round-50/gap-rule.json')
R50_RECEIPT = os.path.join(LANE, '.ufo/waves/round-50/l1/scores/c1-after-attempt2.json')


# --------------------------------------------------------------- byte helpers

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def read_bytes(path):
    with open(path, 'rb') as fh:
        return fh.read()


# ------------------------------------------------------- frozen-clause helpers
# (ported verbatim in behaviour from tools/round-50/c1-counter.py)

def parse_nonregular(raw):
    """(rows[(rel, kind, detail)], error) for nonregular.tsv."""
    if raw is None:
        return [], 'absent'
    rows = []
    for line in raw.decode(errors='replace').splitlines():
        if not line.strip():
            continue
        f = [c.rstrip('\r') for c in line.split('\t')]
        if len(f) < 2:
            return [], 'row %r has %d fields, want >= 2' % (line, len(f))
        rel = f[0].strip()
        kind = f[1].strip().lower()
        if (rel, kind) == ('relative_path', 'kind'):
            continue
        if not rel or not kind:
            return [], 'empty path/kind in %r' % (line,)
        rows.append((rel, kind, f[2] if len(f) > 2 else None))
    seen = set()
    for row in rows:
        if (row[0], row[1]) in seen:
            return [], 'duplicate nonregular row %r' % (row[:2],)
        seen.add((row[0], row[1]))
    return rows, None


def strip_rel(rel):
    if not isinstance(rel, str):
        return rel
    r = rel
    while r.startswith('./'):
        r = r[2:]
    return r.lstrip('/')


def strip_output(path):
    if not isinstance(path, str):
        return path
    if path.startswith('$output/'):
        return path[len('$output/'):]
    return path


def path_parts(path):
    if not isinstance(path, str) or not path:
        return None
    p = path
    while p.startswith('$output/'):
        p = p[len('$output/'):]
    return [x for x in p.split('/') if x not in ('', '.')]


def under_root(path, root):
    if not isinstance(path, str) or not isinstance(root, str) or not root:
        return False
    p = strip_output(path)
    if p == root:
        return True
    return p.startswith(root.rstrip('/') + '/')


def extract_rel(path, root):
    if root is None or not isinstance(path, str) or not path:
        return None
    if not under_root(path, root):
        return None
    parts = path_parts(path)
    if parts is None:
        return None
    pret = root.split('/')
    if parts[:len(pret)] != pret:
        return None
    rest = parts[len(pret):]
    return '/'.join(rest) if rest else ''


def trusted_run_root(output_directory):
    if not isinstance(output_directory, str) or not os.path.isabs(output_directory):
        return None
    if '..' in output_directory.split('/'):
        return None
    parent = os.path.dirname(output_directory.rstrip('/'))
    if not parent or parent == '/':
        return None
    return parent


def diagnostic_typename(diagnostic):
    report = diagnostic.get('report')
    return report.get('__typename__') if isinstance(report, dict) else None


def diagnostic_rel(diagnostic, root, output_directory=None):
    if root is None or not isinstance(diagnostic, dict):
        return None
    report = diagnostic.get('report')
    link = report.get('link') if isinstance(report, dict) else None
    if not isinstance(link, str) or not link:
        return None
    trusted = trusted_run_root(output_directory)
    if trusted is None:
        return None
    if not under_root(link, trusted):
        return None
    segs = [x for x in link.split('/') if x not in ('', '.')]
    tsegs = [x for x in trusted.split('/') if x not in ('', '.')]
    if segs[:len(tsegs)] != tsegs:
        return None
    rsegs = root.split('/')
    start = len(tsegs)
    for i in range(len(segs) - len(rsegs), start - 1, -1):
        if segs[i:i + len(rsegs)] == rsegs:
            return '/'.join(segs[i + len(rsegs):])
    return None


def silent_detail_matches(detail, allowed):
    if detail is None:
        return False
    for label in allowed:
        if label == 'empty-target':
            if detail == '':
                return True
        elif detail == label:
            return True
    return False


def rule_model(raw):
    """(model, problems) for a gap-rule.json text (counter's gap_rule_model,
    with the round-50 hard-coded claim label widened: the round-52 counter's
    gap_rule_model accepts {R50-C1, R52-C1} per the claims' rule grammar)."""
    probs = []
    model = {'allowed': {}, 'required': {}, 'structural': {}, 'removed': {},
             'claim': None}
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as e:
        return model, ['not JSON: %s' % e]
    if not isinstance(doc, dict):
        return model, ['not a JSON object']
    model['claim'] = doc.get('claim')
    if model['claim'] not in (None, 'R50-C1', 'R52-C1'):
        probs.append('claim %r not in {R50-C1, R52-C1}' % (model['claim'],))
    structural = doc.get('structural')
    if structural is not None:
        if not isinstance(structural, dict):
            probs.append('`structural` must be an object')
        else:
            for kind, limit in structural.items():
                if not isinstance(kind, str) or not kind.strip():
                    probs.append('non-string structural gap kind %r' % (kind,))
                    continue
                if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
                    probs.append('structural[%r] must be a non-negative int' % (kind,))
                    continue
                model['structural'][kind.strip()] = limit
    allowed = doc.get('allowed')
    if not isinstance(allowed, dict) or not allowed:
        probs.append('`allowed` must be a non-empty object')
        allowed = allowed if isinstance(allowed, dict) else {}
    for kind, kinds in allowed.items():
        if not isinstance(kind, str) or not kind.strip():
            probs.append('non-string non-regular kind %r' % (kind,))
            continue
        if not isinstance(kinds, list) or not all(isinstance(k, str) and k for k in kinds):
            probs.append('allowed[%r] must be a list of gap kinds' % (kind,))
            continue
        if len(set(kinds)) != len(kinds):
            probs.append('allowed[%r] repeats a gap kind' % (kind,))
        model['allowed'][kind.strip().lower()] = [k.strip() for k in kinds]
    required = doc.get('required')
    if required is not None:
        if not isinstance(required, dict):
            probs.append('`required` must be an object')
        else:
            for kind, flag in required.items():
                key = kind.strip().lower() if isinstance(kind, str) else None
                if key not in model['allowed']:
                    probs.append('required[%r] names a kind absent from allowed' % (kind,))
                    continue
                if not isinstance(flag, bool):
                    probs.append('required[%r] must be a boolean' % (kind,))
                    continue
                model['required'][key] = flag
    removed = doc.get('removed')
    if removed is not None:
        if not isinstance(removed, dict):
            probs.append('`removed` must be an object')
        else:
            diag = removed.get('diagnostic')
            kinds = removed.get('kinds')
            disp = removed.get('disposition', 'exclusive')
            silent = removed.get('silent', {})
            if not (isinstance(diag, str) and diag.strip()):
                probs.append('removed.diagnostic must be a non-empty string')
                diag = None
            if not (isinstance(kinds, list) and kinds
                    and all(isinstance(k, str) and k for k in kinds)):
                probs.append('removed.kinds must be a non-empty list of kinds')
                kinds = []
            if disp != 'exclusive':
                probs.append('removed.disposition %r != "exclusive"' % (disp,))
            if not isinstance(silent, dict):
                probs.append('removed.silent must be an object')
                silent = {}
            for kind, details in silent.items():
                if not (isinstance(details, list)
                        and all(isinstance(x, str) for x in details)):
                    probs.append('removed.silent[%r] must be a list of details' % (kind,))
                    continue
            model['removed'] = {
                'diagnostic': diag.strip() if isinstance(diag, str) else None,
                'kinds': [k.strip().lower() for k in kinds],
                'disposition': disp,
                'silent': {str(k).strip().lower(): list(v)
                           for k, v in silent.items() if isinstance(v, list)},
            }
    return model, probs


def law_shape_ok(model):
    """(ok, why) -- the round-52 rule-SHAPE clause, the claims' wording verbatim.

    "the frozen rule lists no char-device/fifo/socket/block detail under
    `removed.silent` and `allowed` for those kinds is the empty list".
    """
    silent = (model.get('removed') or {}).get('silent') or {}
    allowed = model.get('allowed') or {}
    for kind in DEVICE_KINDS:
        details = silent.get(kind) or []
        if details:
            return False, 'removed.silent lists %s details %r' % (kind, details)
        if kind not in allowed:
            return False, 'allowed does not name the device kind %r' % (kind,)
        if allowed[kind]:
            return False, 'allowed[%r] is not the empty list: %r' % (kind, allowed[kind])
    return True, None


def law_shape_ok_strict(model):
    """(ok, why) -- the claims' shape clause PLUS required[device] is false.

    The claims' own wording of law_shape_ok does not mention `required`, so a
    rule with required['char-device']=true and NO silent allowance passes the
    claims' clause and is caught only by the disposition check. Reported
    separately so the L1 can decide the frozen grammar.
    """
    ok, why = law_shape_ok(model)
    if not ok:
        return False, why
    required = model.get('required') or {}
    for kind in DEVICE_KINDS:
        if required.get(kind) is not False:
            return False, 'required[%r] is %r, not false' % (kind, required.get(kind))
    return True, None


# -------------------------------------------------------- the disposition math

def disposition(gaps_list, diags, nonreg, model, root, output_directory=None):
    """(ok, why, families) -- the counter's three-family disposition check.

    `families` reports each family separately (the counter short-circuits; the
    battery needs to know WHICH clause killed each mutant):
      F1 path-resolved gap, F2 structural gap, F3 removal, R required rows.

    `why` reproduces the counter's note byte-for-byte: the counter RETURNS on
    the first failing clause it meets, in ITS order (the gap loop, then the
    structural over-allowance, then the removal loop, then the missing
    dispositions). The first failure in that order is recorded here, so the
    anchor against the committed round-50 receipt is exact, not merely
    "both red".
    """
    if root is None:
        return False, 'no extract root: paths cannot be resolved', {
            'F1': (False, 'no extract root'), 'F2': (False, 'no extract root'),
            'F3': (False, 'no extract root'), 'R': (False, 'no extract root')}
    allowed = model.get('allowed') or {}
    structural = model.get('structural') or {}
    required = model.get('required') or {}
    removed = model.get('removed') or {}
    by_rel = {rel: (kind, detail) for rel, kind, detail in nonreg}
    rows_at = {}
    for rel, _kind, _detail in nonreg:
        rows_at.setdefault(strip_rel(rel), []).append(rel)
    gapped = {}
    struct_count = {}
    flags = {'F1': True, 'F2': True, 'F3': True, 'R': True}
    notes = {}
    first_fail = [None]

    def fail(family, note):
        flags[family] = False
        notes.setdefault(family, note)
        if first_fail[0] is None:
            first_fail[0] = note

    for g in gaps_list:
        if not isinstance(g, dict):
            fail('F1', 'non-object gap')
            continue
        kind = g.get('kind')
        rp = g.get('relative_path')
        if rp is None:
            if kind not in structural:
                fail('F2', 'gap kind %r has no path and no structural allowance' % (kind,))
                continue
            struct_count[kind] = struct_count.get(kind, 0) + 1
            continue
        if kind in structural:
            fail('F1', 'structural gap kind %r carries a path %r' % (kind, rp))
            continue
        rel_in_root = extract_rel(rp, root)
        hits = rows_at.get(rel_in_root, []) if rel_in_root else []
        if len(hits) != 1:
            fail('F1', 'gap path %r matches %d non-regular entries' % (rp, len(hits)))
            continue
        entry_kind = by_rel[hits[0]][0]
        if kind not in allowed.get(entry_kind, []):
            fail('F1', 'gap kind %r not allowed for %r entry %r (allowed %r)' % (
                kind, entry_kind, hits[0], allowed.get(entry_kind, [])))
            continue
        gapped.setdefault(hits[0], []).append(kind)
    over = {k: [n, structural[k]] for k, n in struct_count.items() if n > structural[k]}
    if over:
        fail('F2', 'structural gaps over allowance %r' % (over,))

    removal_name = removed.get('diagnostic')
    removal_kinds = removed.get('kinds') or []
    removed_rels = {}
    if removal_name:
        for d in diags:
            if diagnostic_typename(d) != removal_name:
                continue
            rel = diagnostic_rel(d, root, output_directory)
            if rel is None:
                fail('F3', 'removal diagnostic without a path under the root: %r'
                     % (d.get('input_path'),))
                continue
            hits = rows_at.get(rel, [])
            if len(hits) != 1:
                fail('F3', 'removal resolves to %d non-regular entries at %r'
                     % (len(hits), rel))
                continue
            entry_kind = by_rel[hits[0]][0]
            if entry_kind not in removal_kinds:
                fail('F3', 'removal at %r names a %r entry; removed.kinds is %r'
                     % (rel, entry_kind, removal_kinds))
                continue
            if gapped.get(hits[0]):
                fail('F3', 'entry %r is both gapped and removed' % (hits[0],))
                continue
            removed_rels[hits[0]] = removed_rels.get(hits[0], 0) + 1

    missing = []
    silent_admitted = []
    for rel, kind, detail in nonreg:
        need = required.get(kind, bool(allowed.get(kind)))
        if not need:
            continue
        if gapped.get(rel) or removed_rels.get(rel):
            continue
        allowed_details = (removed.get('silent') or {}).get(kind)
        if allowed_details and silent_detail_matches(detail, allowed_details):
            silent_admitted.append(rel)
            continue
        missing.append(rel)
    if missing:
        fail('R', 'required entry with no disposition (no gap, no %s) on %r'
             % (removal_name or 'removal', sorted(missing)[:8]))

    families = {
        'F1': (flags['F1'], notes.get('F1', 'ok')),
        'F2': (flags['F2'], notes.get('F2', 'ok')),
        'F3': (flags['F3'], notes.get('F3', 'ok')),
        'R': (flags['R'], notes.get('R', 'ok')),
    }
    ok = all(flags.values())
    if ok:
        why = ('%d gaps (%d structural), %d removals, %d silent, on %d '
               'non-regular entries' % (
                   len(gaps_list), sum(struct_count.values()),
                   sum(removed_rels.values()), len(silent_admitted), len(nonreg)))
    else:
        why = first_fail[0]
    return ok, why, families


# ------------------------------------------------------------------- the data

def load_carrier(cid):
    env = json.loads(read_bytes(os.path.join(
        LANE, 'corpus/evidence/round-50/c1', cid, 'after.json')).decode())
    nr = env.get('normalized_result') or {}
    rows, err = parse_nonregular(read_bytes(os.path.join(
        LANE, 'tools/round-50/oracle', cid + '.nonregular.tsv')))
    if err:
        raise SystemExit('nonregular table %s: %s' % (cid, err))
    roots = []
    for d in nr.get('derivations') or []:
        if isinstance(d, dict) and d.get('handler') == 'squashfs_v4_le':
            child = strip_output(d.get('child_path'))
            if isinstance(child, str) and child:
                roots.append(child.rstrip('/'))
    roots = sorted(set(roots))
    if len(roots) != 1:
        raise SystemExit('%s: %d squashfs_v4_le roots %r' % (cid, len(roots), roots))
    od = (env.get('parameters') or {}).get('output_directory')
    return {
        'id': cid,
        'gaps': list(nr.get('extraction_gaps') or []),
        'diags': [d for d in (nr.get('diagnostics') or []) if isinstance(d, dict)],
        'nonreg': rows,
        'root': roots[0],
        'output_directory': od,
    }


# -------------------------------------------------------------- the rule texts

def base_law_rule():
    """The round-52 law rule (M6): the device-accounting law, no detail list."""
    return {
        'claim': 'R52-C1',
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


ALL_THIRTEEN = ['247:0', '136:0', '136:1', '136:2', '136:3', '136:4', '136:5',
                '136:6', '136:7', '230:0', '3:0', '3:1', '3:2']


def mutants():
    """name -> (rule dict, human description).

    The names follow the seat's brief: M1..M6. M6 is the round-52 law rule
    itself (the CTL-NEW arm); M1..M5 are the five mutants. R50-FROZEN is the
    committed round-50 rule (the CTL-OLD arm)."""
    out = {}

    law = base_law_rule()

    out['M6'] = (law, 'the round-52 device-accounting law rule (the CTL-NEW arm: '
                'required char-device=false, allowed device kinds empty, no '
                'device detail under removed.silent)')

    m1 = json.loads(json.dumps(law))
    m1['required']['char-device'] = True
    m1['removed']['silent'] = {'char-device': ['247:0']}
    out['M1'] = (m1, 'require char-device, silent detail 247:0 only '
                '(the round-50 rule\'s device clause on top of the law)')

    m1b = json.loads(json.dumps(law))
    m1b['required']['char-device'] = True
    out['M1b'] = (m1b, 'require char-device with NO silent allowance at all '
                 '(the claims\' F3 "required-true variant")')

    m2 = json.loads(json.dumps(law))
    m2['required']['char-device'] = True
    m2['removed']['silent'] = {'char-device': list(ALL_THIRTEEN)}
    out['M2'] = (m2, 'whitelist ALL THIRTEEN observed char-device details')

    m3 = json.loads(json.dumps(law))
    m3['required']['char-device'] = True
    m3['removed']['silent'] = {'char-device': ['247:0'] + ['136:%d' % i for i in range(8)]}
    out['M3'] = (m3, 'whitelist a STRICT SUBSET: 247:0 plus 136:0-136:7 only '
                '(the M50 partial-widening trap)')

    m3b = json.loads(json.dumps(law))
    m3b['required']['char-device'] = True
    m3b['removed']['silent'] = {'char-device': ['136:%d' % i for i in range(8)]}
    out['M3b'] = (m3b, 'variant of M3: 136:0-136:7 only, 247:0 dropped')

    m4 = json.loads(json.dumps(law))
    m4['removed'] = {
        'diagnostic': 'MaliciousSymlinkKept',
        'kinds': ['symlink'],
        'disposition': 'exclusive',
        'silent': {},
    }
    out['M4'] = (m4, 'DROP the symlink removal diagnostic (the rule no longer '
                'names MaliciousSymlinkRemoved)')

    m5 = json.loads(json.dumps(law))
    m5['removed']['kinds'] = ['dir']
    out['M5'] = (m5, 'require symlinks with ONLY THE GAP allowed '
                '(removed.kinds no longer admits a symlink)')

    m5b = json.loads(json.dumps(law))
    m5b['allowed']['symlink'] = []
    out['M5b'] = (m5b, 'variant of M5: no gap kind is allowed for a symlink row')

    # CTL-OLD arm: the COMMITTED round-50 rule, verbatim from the lane.
    out['R50-FROZEN'] = (json.loads(read_bytes(RULE_R50).decode()),
                         'the committed round-50 gap rule (the CTL-OLD arm: it '
                         'must yield 2 of 4 dispositions over the committed '
                         'round-50 envelopes, reproducing the round-50 miss)')

    return out


# ------------------------------------------- the independently derived matrix
# Derived by reading the frozen clause math and the committed census, NOT by
# running the script.  'verdict' is the per-carrier DISPOSITION verdict
# (green = gaps_ok); 'shape' is law_shape_ok; 'overall' is the rule-scoped
# verdict the counter would report (red if the shape clause fails or any
# carrier's disposition fails); 'clauses' are the clauses that make it red.
#
# Name map to the claims' own mutation labels (plans/round-52-claims.md, F4):
#   this M1  == claims M3 (required.char-device=true, silent 247:0 only)
#   this M1b == claims F3's "required-true variant" (no silent allowance)
#   this M2  == claims M1 (the all-thirteen whitelist)
#   this M3  == claims M4 (a strict-subset whitelist stays red)
#   claims M2 (a 14th, unlisted device) is the SYNTHETIC probe below: the
#   committed corpus has no fourteenth device, so it cannot be measured from
#   the committed census.
EXPECTED = {
    'R50-FROZEN': {'verdict': {'c6430': 'green', 'c6490': 'green',
                               'g7581': 'red', 'g7582': 'red'},
                   'shape': 'red', 'overall': 'red', 'clauses': ['R', 'shape']},
    'M6': {'verdict': {'c6430': 'green', 'c6490': 'green',
                       'g7581': 'green', 'g7582': 'green'},
           'shape': 'green', 'overall': 'green', 'clauses': []},
    'M1': {'verdict': {'c6430': 'green', 'c6490': 'green',
                       'g7581': 'red', 'g7582': 'red'},
           'shape': 'red', 'overall': 'red', 'clauses': ['R', 'shape']},
    'M1b': {'verdict': {'c6430': 'red', 'c6490': 'red',
                        'g7581': 'red', 'g7582': 'red'},
            'shape': 'green', 'overall': 'red', 'clauses': ['R']},
    'M2': {'verdict': {'c6430': 'green', 'c6490': 'green',
                       'g7581': 'green', 'g7582': 'green'},
           'shape': 'red', 'overall': 'red', 'clauses': ['shape']},
    'M3': {'verdict': {'c6430': 'green', 'c6490': 'green',
                       'g7581': 'red', 'g7582': 'red'},
           'shape': 'red', 'overall': 'red', 'clauses': ['R', 'shape']},
    'M3b': {'verdict': {'c6430': 'red', 'c6490': 'red',
                        'g7581': 'red', 'g7582': 'red'},
            'shape': 'red', 'overall': 'red', 'clauses': ['R', 'shape']},
    'M4': {'verdict': {'c6430': 'red', 'c6490': 'red',
                       'g7581': 'red', 'g7582': 'red'},
           'shape': 'green', 'overall': 'red', 'clauses': ['R']},
    # M5: removed.kinds no longer admits a symlink -> F3 fails (the removal
    # diagnostic names a symlink entry) AND that symlink row then carries
    # neither a gap nor a removal -> R fails too. M5b: no gap kind is allowed
    # for a symlink row -> F1 fails AND the row loses its disposition -> R.
    'M5': {'verdict': {'c6430': 'red', 'c6490': 'red',
                       'g7581': 'red', 'g7582': 'red'},
           'shape': 'green', 'overall': 'red', 'clauses': ['F3', 'R']},
    'M5b': {'verdict': {'c6430': 'red', 'c6490': 'red',
                        'g7581': 'red', 'g7582': 'red'},
            'shape': 'green', 'overall': 'red', 'clauses': ['F1', 'R']},
}


def cross_validate(carriers, rules):
    """Cross-validate the ported clause math against the FROZEN counter's own
    `disposition_check` (tools/round-50/c1-counter.py), imported as a module.

    The frozen counter's `gap_rule_model` hard-codes the claim label 'R50-C1',
    so the model is built with that label (the claim-label check is a separate
    finding, reported by the caller); everything else -- allowed, required,
    structural, removed -- is passed through unchanged. Both implementations
    must agree on (ok, why) for every rule x carrier."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'r50_c1_counter', os.path.join(LANE, 'tools/round-50/c1-counter.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rows = []
    agree = True
    for name, rule in rules.items():
        r = json.loads(json.dumps(rule))
        if r.get('claim') != 'R50-C1':
            r['claim'] = 'R50-C1'
        model, probs = mod.gap_rule_model(json.dumps(r).encode())
        for cid in IDS:
            c = carriers[cid]
            want_ok, want_why = mod.disposition_check(
                c['gaps'], c['diags'], c['nonreg'], model, c['root'],
                c['output_directory'])
            got_ok, got_why, _fam = disposition(
                c['gaps'], c['diags'], c['nonreg'], model, c['root'],
                c['output_directory'])
            same = (want_ok == got_ok) and (want_why == got_why)
            if not same:
                agree = False
            rows.append({'mutant': name, 'id': cid,
                         'counter_gaps_ok': want_ok, 'ported_gaps_ok': got_ok,
                         'agree': same,
                         'note_identical': want_why == got_why,
                         'counter_note': want_why, 'ported_note': got_why})
    return rows, agree


def input_hashes():
    """sha256 of every committed lane byte this battery reads (restoration
    evidence: the battery is READ-ONLY on the lane tree, so these must be
    identical before and after the run)."""
    out = {}
    out[os.path.relpath(RULE_R50, LANE)] = sha256_file(RULE_R50)
    out[os.path.relpath(R50_RECEIPT, LANE)] = sha256_file(R50_RECEIPT)
    for cid in IDS:
        out['corpus/evidence/round-50/c1/%s/after.json' % cid] = sha256_file(
            os.path.join(LANE, 'corpus/evidence/round-50/c1', cid, 'after.json'))
        out['tools/round-50/oracle/%s.nonregular.tsv' % cid] = sha256_file(
            os.path.join(LANE, 'tools/round-50/oracle', cid + '.nonregular.tsv'))
    out['tools/round-50/c1-counter.py'] = sha256_file(
        os.path.join(LANE, 'tools/round-50/c1-counter.py'))
    return out


def main():
    started = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    hashes_before = input_hashes()
    carriers = {cid: load_carrier(cid) for cid in IDS}

    # ---- ANCHOR: the frozen round-50 rule must reproduce the committed
    # round-50 verdict (per-carrier gaps_ok and the failure note).
    r50_raw = read_bytes(RULE_R50)
    r50_model, r50_probs = rule_model(r50_raw)
    committed = json.loads(read_bytes(R50_RECEIPT))
    ccar = committed.get('carriers') or {}
    anchor_rows = []
    anchor_ok = True
    for cid in IDS:
        c = carriers[cid]
        ok, why, fam = disposition(c['gaps'], c['diags'], c['nonreg'], r50_model,
                                   c['root'], c['output_directory'])
        want = (ccar.get(cid) or {}).get('gaps_ok')
        note = (ccar.get(cid) or {}).get('gaps_note')
        match = (ok == want) and (why == note)
        if not match:
            anchor_ok = False
        anchor_rows.append({'id': cid, 'computed_gaps_ok': ok,
                            'committed_gaps_ok': want, 'match': match,
                            'note_identical': why == note,
                            'computed_note': why, 'committed_note': note})
    shape50, shape50_why = law_shape_ok(r50_model)

    # ---- CROSS-VALIDATION: the ported clause math vs the frozen counter's own
    # disposition_check, over every mutant x carrier.
    xval_rules = {name: rule for name, (rule, _d) in mutants().items()}
    xval_rules['R50-FROZEN'] = json.loads(r50_raw.decode())
    xval_rows, xval_agree = cross_validate(carriers, xval_rules)
    if not xval_agree:
        failures.append('CROSS-VALIDATION')

    # ---- SYNTHETIC PROBE: the claims' mutation (M2) "a fixture carrier whose
    # non-regular census carries a FOURTEENTH, unlisted device (e.g.
    # dev/ttyS0 4:64) must be GREEN under the law rule and RED under any
    # detail whitelist". The committed corpus has no fourteenth device, so
    # this arm is measured on a SYNTHETIC census row added to the committed
    # g7581 table (no gap, no removal, no published path -> the law says such
    # a row carries no disposition and must not be required).
    # This is a fixture probe, not a claim about the measured carriers.
    probe_carrier = dict(carriers['g7581'])
    probe_carrier['nonreg'] = list(carriers['g7581']['nonreg']) + [
        ('dev/ttyS0', 'char-device', '4:64')]
    probe_rules = {
        'M6': mutants()['M6'][0],
        'M1': mutants()['M1'][0],
        'M1b': mutants()['M1b'][0],
        'M2': mutants()['M2'][0],
        'M3': mutants()['M3'][0],
    }
    probe = {}
    for name, rule in probe_rules.items():
        model, _probs = rule_model(json.dumps(rule).encode())
        ok, why, fam = disposition(probe_carrier['gaps'], probe_carrier['diags'],
                                   probe_carrier['nonreg'], model,
                                   probe_carrier['root'],
                                   probe_carrier['output_directory'])
        probe[name] = {'gaps_ok': ok, 'note': why,
                       'families': {k: {'ok': v[0], 'note': v[1]}
                                    for k, v in fam.items()}}
    probe_expected = {'M6': True, 'M1': False, 'M1b': False,
                      'M2': False, 'M3': False}
    probe_ok = all(probe[n]['gaps_ok'] == probe_expected[n] for n in probe)
    if not probe_ok:
        failures.append('PROBE-14th-device')

    # ---- PROBE-DEVICE-GAP: the law must FAIL CLOSED when a gap lands on a
    # device row ("a future extractor that starts emitting a device gap turns
    # the rule red"). Synthetic gap injected on the committed c6430 device row
    # dev/led; the round-50 rule (allowed['char-device'] = ['unpublished-entry'])
    # tolerates it, the round-52 law rule (allowed['char-device'] = []) must not.
    dev_gap = {'kind': 'unpublished-entry',
               'input_path': '$output/firmware.bin_extract/dev/led',
               'relative_path': 'firmware.bin_extract/dev/led',
               'dependencies': [], 'continuation_id': 'synthetic-device-gap'}
    c = carriers['c6430']
    gap_rows = {}
    for name, rule in (('M6', mutants()['M6'][0]),
                       ('R50-FROZEN', json.loads(r50_raw.decode()))):
        r = json.loads(json.dumps(rule))
        if r.get('claim') != 'R50-C1':
            r['claim'] = 'R50-C1'
        model, _p = rule_model(json.dumps(r).encode())
        ok, why, fam = disposition(list(c['gaps']) + [dev_gap], c['diags'],
                                   c['nonreg'], model, c['root'],
                                   c['output_directory'])
        gap_rows[name] = {'gaps_ok': ok, 'note': why,
                           'families': {k: {'ok': v[0], 'note': v[1]}
                                        for k, v in fam.items()}}
    # expected: the law rule is RED (fail closed); the round-50 rule tolerates
    # the device gap (its allowed['char-device'] lists unpublished-entry)
    devgap_expected = {'M6': False, 'R50-FROZEN': True}
    devgap_ok = all(gap_rows[n]['gaps_ok'] == devgap_expected[n] for n in gap_rows)
    if not devgap_ok:
        failures.append('PROBE-DEVICE-GAP')

    # ---- the battery
    rows = []
    failures = []
    for name, (rule, desc) in mutants().items():
        raw = json.dumps(rule, indent=1, sort_keys=True).encode()
        model, probs = rule_model(raw)
        shape, shape_why = law_shape_ok(model)
        shape_s, shape_s_why = law_shape_ok_strict(model)
        per = {}
        for cid in IDS:
            c = carriers[cid]
            ok, why, fam = disposition(c['gaps'], c['diags'], c['nonreg'], model,
                                       c['root'], c['output_directory'])
            per[cid] = {'gaps_ok': ok, 'note': why,
                        'families': {k: {'ok': v[0], 'note': v[1]}
                                     for k, v in fam.items()}}
        verdicts = {cid: ('green' if per[cid]['gaps_ok'] else 'red') for cid in IDS}
        # every clause that makes this rule red (shape + any failing family)
        clauses = []
        if not shape:
            clauses.append('shape')
        for cid in IDS:
            for k in ('F1', 'F2', 'F3', 'R'):
                if not per[cid]['families'][k]['ok'] and k not in clauses:
                    clauses.append(k)
        overall = 'red' if clauses else 'green'
        exp = EXPECTED.get(name)
        exp_ok = True
        if exp is None:
            exp_ok = False
        else:
            exp_ok = (verdicts == exp['verdict']
                      and ('green' if shape else 'red') == exp['shape']
                      and overall == exp['overall']
                      and sorted(clauses) == sorted(exp['clauses']))
            if not exp_ok:
                failures.append(name)
        rows.append({
            'mutant': name,
            'description': desc,
            'rule_problems': probs,
            'law_shape_ok': shape,
            'law_shape_note': shape_why,
            'law_shape_ok_strict': shape_s,
            'law_shape_note_strict': shape_s_why,
            'per_carrier': per,
            'verdict': verdicts,
            'carriers_green': sum(1 for v in verdicts.values() if v == 'green'),
            'overall': overall,
            'red_clauses': clauses,
            'expected': exp,
            'matches_expected': exp_ok,
        })

    hashes_after = input_hashes()
    restoration_ok = (hashes_before == hashes_after)
    if not restoration_ok:
        failures.append('RESTORATION')

    out = {
        'schema': 'kaidoku-r52-mutgaprule-battery-v1',
        'seat': 'MutGapRule',
        'started_utc': started,
        'finished_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'restoration': {
            'note': 'the battery reads committed lane bytes and writes nothing '
                    'into the lane tree; these hashes are taken before and after '
                    'the run and must be identical',
            'identical': restoration_ok,
            'input_sha256_before': hashes_before,
            'input_sha256_after': hashes_after,
        },
        'inputs': {
            'round-50 rule': {'path': os.path.relpath(RULE_R50, LANE),
                              'sha256': sha256_file(RULE_R50)},
            'round-50 receipt': {'path': os.path.relpath(R50_RECEIPT, LANE),
                                 'sha256': sha256_file(R50_RECEIPT)},
        },
        'carriers': {cid: {'nonregular_rows': len(carriers[cid]['nonreg']),
                           'gaps': len(carriers[cid]['gaps']),
                           'diagnostics': len(carriers[cid]['diags']),
                           'extract_root': carriers[cid]['root'],
                           'output_directory': carriers[cid]['output_directory']}
                     for cid in IDS},
        'anchor_round-50-rule': {
            'rule_problems': r50_probs,
            'law_shape_ok': shape50,
            'law_shape_note': shape50_why,
            'rows': anchor_rows,
            'anchor_reproduced': anchor_ok,
        },
        'cross_validation_vs_frozen_counter': {
            'note': 'ported clause math vs tools/round-50/c1-counter.py '
                    'disposition_check (the frozen counter\'s gap_rule_model is '
                    'given the claim label R50-C1 because it hard-codes it)',
            'agree': xval_agree,
            'rows': xval_rows,
        },
        'probe_device_gap_fail_closed': {
            'note': 'synthetic unpublished-entry gap injected on the committed '
                    'c6430 device row dev/led; the law rule (allowed[char-device] '
                    'empty) must go RED, the round-50 rule tolerates it',
            'expected': devgap_expected,
            'rows': gap_rows,
            'matches_expected': devgap_ok,
        },
        'probe_14th_device': {
            'carrier': 'g7581 census + synthetic row dev/ttyS0 4:64',
            'expected': probe_expected,
            'rows': probe,
            'matches_expected': probe_ok,
        },
        'matrix': rows,
        'failures': failures,
        'verdict': 'ok' if (anchor_ok and not failures) else 'MISMATCH',
    }
    json.dump(out, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')
    return 0 if (anchor_ok and not failures) else 1


if __name__ == '__main__':
    sys.exit(main())
