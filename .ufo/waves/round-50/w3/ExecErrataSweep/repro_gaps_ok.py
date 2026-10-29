#!/usr/bin/env python3
"""Reproduction of the R50-C1 gaps_ok failure for g7581/g7582.

Read-only against the lane. Replays the FROZEN counter's own
`disposition_check` on the lane's own frozen tables and the lane's own
receipts (the L1's live data run under corpus/evidence/round-50/c1/, and
the committed POS control fixtures under tools/round-50/control-fixtures/pos/).

Exit codes (semantic): 0 = the claim's defect is reproduced (gaps_ok False
on g7581/g7582, True on c6490/c6430); 1 = the defect did NOT reproduce
(counter/rule changed under us); 2 = could-not-evaluate.

Usage:
  python3 -I -B repro_gaps_ok.py [--root LANE] [--json-out PATH]
"""

import argparse
import gzip
import importlib.util
import json
import os
import sys

DEFAULT_LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'


def load_counter(root):
    path = os.path.join(root, 'tools/round-50/c1-counter.py')
    spec = importlib.util.spec_from_file_location('r50_c1_counter', path)
    mod = importlib.util.module_from_spec(spec)
    argv = sys.argv
    sys.argv = [path]
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        pass
    finally:
        sys.argv = argv
    return mod, path


def sha256_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=DEFAULT_LANE)
    ap.add_argument('--json-out')
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    m, counter_path = load_counter(root)

    with open(os.path.join(root, 'tools/round-50/gap-rule.json'), 'rb') as fh:
        model, plan_probs = m.gap_rule_model(fh.read())
    with open(os.path.join(root, 'tools/round-50/carriers.json'), 'rb') as fh:
        carriers = {c['id']: c for c in json.load(fh)['carriers']}

    def check(env, cid):
        rows, err = m.parse_nonregular(
            open(os.path.join(root, carriers[cid]['nonregular']), 'rb').read())
        if err:
            return None, 'nonregular table unreadable: %s' % err
        diags = m.diagnostics(env)
        root_rel, how = m.subject_root(env, carriers[cid].get('oracle_root'))
        od = (env.get('parameters') or {}).get('output_directory')
        ok, why = m.disposition_check(m.gaps(env), diags, rows, model, root_rel, od)
        return ok, why

    def missing(env, cid):
        """The exact entries with no disposition (the rule's own accounting)."""
        rows, _ = m.parse_nonregular(
            open(os.path.join(root, carriers[cid]['nonregular']), 'rb').read())
        diags = m.diagnostics(env)
        root_rel, _ = m.subject_root(env, carriers[cid].get('oracle_root'))
        od = (env.get('parameters') or {}).get('output_directory')
        allowed = model.get('allowed') or {}
        required = model.get('required') or {}
        removed = model.get('removed') or {}
        rows_at = {}
        for r, _k, _d in rows:
            rows_at.setdefault(m.strip_rel(r), []).append(r)
        gapped = {}
        for g in m.gaps(env):
            if not isinstance(g, dict):
                continue
            rp = g.get('relative_path')
            if rp is None:
                continue
            rir = m.extract_rel(rp, root_rel)
            hits = rows_at.get(rir, []) if rir else []
            if len(hits) == 1:
                gapped.setdefault(hits[0], []).append(g.get('kind'))
        removed_rels = set()
        for d in diags:
            if m.diagnostic_typename(d) != removed.get('diagnostic'):
                continue
            rel = m.diagnostic_rel(d, root_rel, od)
            if rel:
                removed_rels.add(rel)
        out = []
        for rel, kind, detail in rows:
            if not required.get(kind, bool(allowed.get(kind))):
                continue
            if gapped.get(rel) or rel in removed_rels:
                continue
            ad = (removed.get('silent') or {}).get(kind)
            if ad and m.silent_detail_matches(detail, ad):
                continue
            out.append({'rel': rel, 'kind': kind, 'detail': detail})
        return out

    out = {'lane': root, 'counter': counter_path,
           'counter_sha256': sha256_file(counter_path),
           'gap_rule_sha256': sha256_file(os.path.join(root, 'tools/round-50/gap-rule.json')),
           'gap_rule_problems': plan_probs,
           'gap_rule_required_char_device': model.get('required', {}).get('char-device'),
           'gap_rule_silent_char_device': (model.get('removed', {}).get('silent') or {}).get('char-device'),
           'sources': {}}

    live = os.path.join(root, 'corpus/evidence/round-50/c1')
    for cid in ('g7581', 'g7582', 'c6490', 'c6430'):
        p = os.path.join(live, cid, 'after.json')
        if not os.path.isfile(p):
            out['sources']['live:' + cid] = {'present': False}
            continue
        env = json.load(open(p))
        ok, why = check(env, cid)
        out['sources']['live:' + cid] = {
            'present': True, 'path': p, 'sha256': sha256_file(p),
            'gaps_ok': ok, 'why': why,
            'missing_disposition': missing(env, cid)}

    for cid in ('g7581', 'g7582', 'c6490', 'c6430'):
        p = os.path.join(root, 'tools/round-50/control-fixtures/pos/files',
                         'corpus__evidence__round-50__c1__%s__after.json.gz' % cid)
        if not os.path.isfile(p):
            out['sources']['pos:' + cid] = {'present': False}
            continue
        env = json.loads(gzip.open(p, 'rb').read())
        ok, why = check(env, cid)
        out['sources']['pos:' + cid] = {
            'present': True, 'path': p, 'sha256': sha256_file(p),
            'gaps_ok': ok, 'why': why,
            'missing_disposition': missing(env, cid)}

    def g(ok):
        return out['sources'].get(ok, {}).get('gaps_ok')
    reproduced = (g('live:g7581') is False and g('live:g7582') is False
                  and g('live:c6490') is True and g('live:c6430') is True)
    out['defect_reproduced'] = reproduced
    out['conclusion'] = (
        'gaps_ok is False for g7581 and g7582 under the FROZEN gap rule: the rule '
        'requires a disposition for every char-device entry and admits only '
        '247:0 as silent, while the 7581/7582 non-regular tables carry 13 '
        'char-devices (dev/led 247:0, dev/pts/0..7 136:*, dev/tiatm 230:0, '
        'dev/ttyp0..2 3:*); the 12 non-247:0 devices carry no unpublished-entry '
        'gap and are not removals. carriers_matched therefore caps at 2 of 4.'
        if reproduced else
        'the defect did not reproduce; the frozen bytes changed under this seat.')

    if a.json_out:
        os.makedirs(os.path.dirname(os.path.abspath(a.json_out)), exist_ok=True)
        with open(a.json_out, 'w') as fh:
            json.dump(out, fh, indent=1, sort_keys=True)
            fh.write('\n')
    print(json.dumps({'defect_reproduced': reproduced,
                      'live': {k: v.get('gaps_ok') for k, v in out['sources'].items()
                               if k.startswith('live:')},
                      'pos': {k: v.get('gaps_ok') for k, v in out['sources'].items()
                              if k.startswith('pos:')}},
                     sort_keys=True))
    return 0 if reproduced else 1


if __name__ == '__main__':
    sys.exit(main())
