#!/usr/bin/env python3
"""Minimal decisive probe: what decides `gaps_ok` on the LANDED receipts?

Imports the FROZEN counter's own functions (frozen bytes, never mutated) and
evaluates the ONE clause under test -- `disposition_check` -- against the
committed after-receipts at the landing rev, under three rule models:

  F   the frozen gap-rule.json (required.char-device = true,
      removed.silent.char-device = ["247:0"])
  M1  required.char-device = false          (the kind is not required)
  M2  any char-device detail admitted silently (the silent allowance widened)

No REA run, no git write: `git show` only. Exit 0 = every carrier's gaps_ok
holds under that model, 1 = at least one carrier fails, 2 = unevaluable.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FROZEN_COUNTER = '/fast/scratch/hyaku/kaidoku-r50/w4-MutC1Counter/c1-counter-frozen.py'
REV = '646d29c9df4ef77499248f95589cb9526c6dea19'
FREEZE = '435d41fd4ad9211d1579fc447936fb33d2b74467'
IDS = ('g7581', 'g7582', 'c6490', 'c6430')
AFTERDIR = 'corpus/evidence/round-50/c1'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git_show(rev, path):
    p = subprocess.run(['git', '-C', LANE, 'show', f'{rev}:{path}'],
                       capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout


def main():
    c = load(FROZEN_COUNTER, 'c1_frozen')
    rule_raw = git_show(FREEZE, c.GAPRULE)
    spec = json.loads(git_show(FREEZE, c.CARRIERS))

    models = {}
    base_model, probs = c.gap_rule_model(rule_raw)
    if probs:
        print('frozen rule does not parse:', probs)
        return 2
    models['F'] = base_model

    m1 = json.loads(json.dumps(base_model))
    m1['required']['char-device'] = False
    models['M1'] = m1

    m2 = json.loads(json.dumps(base_model))
    m2['removed'].setdefault('silent', {})['char-device'] = ['*']
    models['M2'] = m2

    # M2 needs the matcher to honour the '*' wildcard; the frozen matcher does
    # not, so for M2 the silent admission is applied by widening the model's
    # silent list with every char-device detail the oracle actually carries.
    detail_by_kind = {}
    for spec_c in spec['carriers']:
        rows, err = c.parse_nonregular(git_show(REV, spec_c['nonregular']))
        if err:
            print('nonregular parse error', spec_c['id'], err)
            return 2
        for rel, kind, detail in rows:
            if kind == 'char-device' and detail is not None:
                detail_by_kind.setdefault(kind, set()).add(detail)
    m2['removed']['silent']['char-device'] = sorted(detail_by_kind.get(
        'char-device', set()))

    out = {'rev': REV, 'freeze': FREEZE, 'counter_sha256': hashlib.sha256(
        open(FROZEN_COUNTER, 'rb').read()).hexdigest(),
        'models': {}, 'details_per_kind': {k: sorted(v)
                                           for k, v in detail_by_kind.items()}}
    for name, model in models.items():
        per = {}
        for spec_c in spec['carriers']:
            cid = spec_c['id']
            env = json.loads(git_show(REV, '%s/%s/after.json' % (AFTERDIR, cid)))
            rows, err = c.parse_nonregular(git_show(REV, spec_c['nonregular']))
            if err:
                print('nonregular parse error', cid, err)
                return 2
            root, how = c.subject_root(env)
            ok, why = c.disposition_check(c.gaps(env), c.diagnostics(env), rows,
                                          model, root,
                                          (env.get('parameters') or {}).get(
                                              'output_directory'))
            per[cid] = {'gaps_ok': ok, 'gaps_note': why, 'root': root,
                        'root_how': how, 'nonregular_rows': len(rows)}
        out['models'][name] = per

    # what the frozen model says is MISSING, per carrier, in full (the counter
    # truncates its note to the first 8 rows)
    full = {}
    for spec_c in spec['carriers']:
        cid = spec_c['id']
        env = json.loads(git_show(REV, '%s/%s/after.json' % (AFTERDIR, cid)))
        rows, _ = c.parse_nonregular(git_show(REV, spec_c['nonregular']))
        by_rel = {rel: (kind, detail) for rel, kind, detail in rows}
        root, _ = c.subject_root(env)
        gapped = {}
        for g in c.gaps(env):
            if not isinstance(g, dict):
                continue
            rp = g.get('relative_path')
            if rp is None:
                continue
            rel = c.extract_rel(rp, root)
            if rel is not None:
                gapped.setdefault(rel, []).append(g.get('kind'))
        removed_rels = set()
        od = (env.get('parameters') or {}).get('output_directory')
        for d in c.diagnostics(env):
            rel = c.diagnostic_rel(d, root, od)
            if rel is not None and c.diagnostic_typename(d) == 'MaliciousSymlinkRemoved':
                removed_rels.add(rel)
        missing = []
        for rel, kind, detail in rows:
            if kind != 'char-device':
                continue
            if gapped.get(rel) or rel in removed_rels:
                continue
            missing.append({'rel': rel, 'detail': detail,
                            'silent_admitted_by_frozen_rule':
                                detail == '247:0'})
        full[cid] = {'char_device_rows': sum(1 for r in rows if r[1] == 'char-device'),
                     'char_device_without_disposition': missing}
    out['missing_detail'] = full

    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'probe.json')
    with open(dest, 'w') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)

    print('%-6s %-8s %s' % ('model', 'gaps_ok', 'per-carrier gaps_ok'))
    for name, per in out['models'].items():
        print('%-6s %-8s %s' % (name,
                                all(v['gaps_ok'] for v in per.values()),
                                {k: v['gaps_ok'] for k, v in per.items()}))
        for cid, v in sorted(per.items()):
            print('        %s: %s' % (cid, v['gaps_note']))
    print()
    for cid, v in out['missing_detail'].items():
        print('%s: %d char-device rows, %d without a disposition: %s' % (
            cid, v['char_device_rows'], len(v['char_device_without_disposition']),
            [(m['rel'], m['detail']) for m in v['char_device_without_disposition']]))
    allok = all(all(v['gaps_ok'] for v in per.values())
                for per in out['models'].values())
    return 0 if allok else 1


if __name__ == '__main__':
    sys.exit(main())
