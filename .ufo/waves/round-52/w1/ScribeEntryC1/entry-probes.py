#!/usr/bin/env python3
"""Read-only measurement probe for the R52-C1 knowledge-entry draft (ScribeEntryC1).

Every number the draft entry states is produced here, over COMMITTED bytes in the
lane, with no REA run, no download, no lane write and no vendor byte touched:

  * the per-carrier non-regular census (kinds and char-device counts),
  * the device-row disposition census over the committed round-50 envelopes
    (does a device row carry a gap, or a published path?),
  * the rule-scoped disposition verdict of each named gap rule over the
    committed round-50 envelopes (CTL-OLD / CTL-NEW / M1 / M3 / M4 / junk), on
    the measured 13-row census and on the synthetic 14-row census,
  * the fail-closed check (one synthetic device gap injected into the committed
    g7581 envelope),
  * the committed round-50 miss receipt's own fields,
  * the SOURCES opened-date / used-by state of the rows this entry cites.

The disposition semantics are the round-50 counter's OWN `gap_rule_model` /
`disposition_check` (imported from `tools/round-50/c1-counter.py`), so the
rule-scoped numbers are the counter's, not a re-implementation. The round-52
law rule is read from the wave-1 draft fixture
`.ufo/waves/round-52/w1/ExecRuleFixtures/gap-rule.json`; the path the L1 will
land is `tools/round-52/gap-rule.json`.

The v1 parser accepts only the claim label `R50-C1`; the round-52 rule carries
`"claim": "R52-C1"`. The label complaint is reported, not hidden: it is the
grammar defect the claims' F10 requires the v2 counter to repair.

Usage:  python3 -I -B entry-probes.py --lane <LANE> [--law-rule PATH]
Exit:   0 every probe ran, 1 a usage error, 2 an input could not be read.
"""
import argparse
import copy
import importlib.util
import json
import os
import sys

CARRIERS = ('c6430', 'c6490', 'g7581', 'g7582')
DEVICE_KINDS = ('char-device', 'block-device', 'fifo', 'socket')
THIRTEEN = ('247:0', '136:0', '136:1', '136:2', '136:3', '136:4', '136:5',
            '136:6', '136:7', '230:0', '3:0', '3:1', '3:2')


def load_counter(lane):
    path = os.path.join(lane, 'tools', 'round-50', 'c1-counter.py')
    spec = importlib.util.spec_from_file_location('r50ctr', path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['r50ctr'] = mod
    spec.loader.exec_module(mod)
    return mod


def nonreg_rows(path):
    rows = []
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            c = line.rstrip('\n').split('\t')
            if len(c) >= 2 and c[1]:
                rows.append((c[0], c[1], c[2] if len(c) > 2 else ''))
    return rows


def load_json(path):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def census(lane):
    print('## census: kinds and char-device rows per carrier')
    for cid in CARRIERS:
        rows = nonreg_rows(os.path.join(lane, 'tools', 'round-50', 'oracle',
                                        '%s.nonregular.tsv' % cid))
        kinds = {}
        for _rel, kind, _detail in rows:
            kinds[kind] = kinds.get(kind, 0) + 1
        devs = [(rel, d) for rel, kind, d in rows if kind == 'char-device']
        other = [(rel, d) for rel, d in devs if rel != 'dev/led']
        print('%s kinds=%s char-device=%d other-than-dev/led=%d'
              % (cid, json.dumps(kinds, sort_keys=True), len(devs), len(other)))
    print('## census: char-device rows of g7581')
    rows = nonreg_rows(os.path.join(lane, 'tools', 'round-50', 'oracle',
                                    'g7581.nonregular.tsv'))
    for rel, kind, detail in rows:
        if kind == 'char-device':
            print('  %s %s %s' % (rel, kind, detail))
    print('## census: kinds present across all four tables')
    seen = set()
    for cid in CARRIERS:
        for _rel, kind, _detail in nonreg_rows(
                os.path.join(lane, 'tools', 'round-50', 'oracle',
                             '%s.nonregular.tsv' % cid)):
            seen.add(kind)
    print('  kinds=%s device_kinds_present=%s'
          % (sorted(seen), sorted(k for k in DEVICE_KINDS if k in seen)))


def device_dispositions(lane):
    print('## law: device-row disposition census over the committed envelopes')
    total = 0
    with_gap = []
    published = []
    for cid in CARRIERS:
        env = load_json(os.path.join(lane, 'corpus', 'evidence', 'round-50', 'c1',
                                     cid, 'after.json'))
        devs = [(rel, d) for rel, kind, d in nonreg_rows(
            os.path.join(lane, 'tools', 'round-50', 'oracle',
                         '%s.nonregular.tsv' % cid)) if kind == 'char-device']
        nr = env['normalized_result']
        gaps = list(nr.get('unpublished_entries') or [])
        gap_paths = [g.get('relative_path') or '' for g in gaps]
        gap_kinds = sorted({g.get('kind') for g in gaps if g.get('kind')})
        pub_paths = [f.get('relative_path') or '' for f in nr.get('files') or []]

        def hits(rel, paths):
            return [p for p in paths if p == rel or p.endswith('/' + rel)]

        wg = [rel for rel, _d in devs if hits(rel, gap_paths)]
        pb = [rel for rel, _d in devs if hits(rel, pub_paths)]
        total += len(devs)
        with_gap += [(cid, r) for r in wg]
        published += [(cid, r) for r in pb]
        print('%s device_rows=%d gap_kinds=%r devices_with_gap=%r '
              'devices_published=%r gaps_total=%d files=%d'
              % (cid, len(devs), gap_kinds, wg, pb, len(gaps),
                 len(nr.get('files') or [])))
    print('LAW-TOTAL device_rows=%d rows_with_a_gap=%d rows_published=%d'
          % (total, len(with_gap), len(published)))


def rule_variants(lane, law_rule_path):
    ctr = load_counter(lane)
    base = load_json(os.path.join(lane, 'tools', 'round-50', 'gap-rule.json'))
    law = load_json(law_rule_path)
    out = {}
    out['CTL-OLD-R50-frozen'] = base
    out['CTL-NEW-R52-law'] = law

    m1 = copy.deepcopy(law)
    m1['required']['char-device'] = True
    m1['removed']['silent'] = {'char-device': list(THIRTEEN)}
    out['M1-all-thirteen'] = m1

    m3 = copy.deepcopy(law)
    m3['required']['char-device'] = True
    m3['removed']['silent'] = {'char-device': ['247:0']}
    out['M3-required-247-only'] = m3

    m4 = copy.deepcopy(law)
    m4['required']['char-device'] = True
    m4['removed']['silent'] = {'char-device': [d for d in THIRTEEN if d != '230:0']}
    out['M4-strict-subset'] = m4

    junk = load_json(os.path.join(lane, '.ufo', 'waves', 'round-52', 'w1',
                                  'ExecRuleFixtures', 'junk-rule.json'))
    out['CTL-JUNK'] = junk

    inputs = {}
    for cid in CARRIERS:
        env = load_json(os.path.join(lane, 'corpus', 'evidence', 'round-50', 'c1',
                                     cid, 'after.json'))
        rows = nonreg_rows(os.path.join(lane, 'tools', 'round-50', 'oracle',
                                        '%s.nonregular.tsv' % cid))
        inputs[cid] = (env, rows)

    # the M2 synthetic census: the g7581 census plus one unlisted device
    g_rows = inputs['g7581'][1] + [('dev/ttyS0', 'char-device', '4:64')]

    print('## rule-scoped disposition verdict over the committed envelopes')
    for name, doc in out.items():
        model, problems = ctr.gap_rule_model(json.dumps(doc))
        for census_name, override in (('measured-13-row', None),
                                      ('M2-synthetic-14-row', g_rows)):
            matched = 0
            per = []
            for cid in CARRIERS:
                env, rows = inputs[cid]
                if override is not None and cid == 'g7581':
                    rows = override
                gaps = ctr.gaps(env)
                diags = ctr.diagnostics(env)
                od = (env.get('parameters') or {}).get('output_directory')
                root, _how = ctr.subject_root(env)
                ok, why = ctr.disposition_check(gaps, diags, rows, model, root, od)
                matched += 1 if ok else 0
                per.append('%s=%s' % (cid, 'T' if ok else 'F'))
            print('%s | %s | %d/4 | %s | parser_problems=%r'
                  % (name, census_name, matched, ' '.join(per), problems))
            if name == 'CTL-OLD-R50-frozen' and census_name == 'measured-13-row':
                for cid in CARRIERS:
                    env, rows = inputs[cid]
                    gaps = ctr.gaps(env)
                    diags = ctr.diagnostics(env)
                    od = (env.get('parameters') or {}).get('output_directory')
                    root, _how = ctr.subject_root(env)
                    ok, why = ctr.disposition_check(gaps, diags, rows, model,
                                                    root, od)
                    if not ok:
                        print('   CTL-OLD %s false: %s' % (cid, why[:220]))

    print('## fail-closed: one synthetic device gap injected into the g7581 envelope')
    env = inputs['g7581'][0]
    rows = inputs['g7581'][1]
    od = (env.get('parameters') or {}).get('output_directory')
    root, _how = ctr.subject_root(env)
    gaps = ctr.gaps(env)
    diags = ctr.diagnostics(env)
    injected = copy.deepcopy(gaps)
    injected.append({
        'kind': 'unpublished-entry',
        'input_path': '$output/%s/dev/led' % root,
        'relative_path': '%s/dev/led' % root,
        'handler': None, 'provider_id': None, 'range': None,
        'root_file_range': None, 'dependencies': [],
        'continuation_id': '0' * 64,
    })
    for name, doc in (('CTL-OLD-R50-frozen', base), ('CTL-NEW-R52-law', law)):
        model, problems = ctr.gap_rule_model(json.dumps(doc))
        clean_ok, _cw = ctr.disposition_check(gaps, diags, rows, model, root, od)
        inj_ok, inj_why = ctr.disposition_check(injected, diags, rows, model,
                                                 root, od)
        print('%s | clean=%s | injected_device_gap=%s | %s'
              % (name, clean_ok, inj_ok, inj_why[:220]))


def miss_receipt(lane):
    print('## committed round-50 miss receipt')
    path = os.path.join(lane, '.ufo', 'waves', 'round-50', 'l1', 'scores',
                        'c1-after-attempt2.json')
    d = load_json(path)
    print('carriers_matched=%r target=%r exit_code=%r'
          % (d.get('carriers_matched'), d.get('target'), d.get('exit_code')))
    for cid, v in sorted((d.get('carriers') or {}).items()):
        print('%s gaps_ok=%r projection_ok=%r nonregular_unpublished_ok=%r note=%r'
              % (cid, v.get('gaps_ok'), v.get('projection_ok'),
                 v.get('nonregular_unpublished_ok'),
                 str(v.get('gaps_note'))[:200]))


def sources_state(lane):
    print('## SOURCES state of the rows this entry cites')
    wanted = ('S243', 'S244', 'S245', 'S249', 'S250', 'S251', 'S252')
    found = {}
    with open(os.path.join(lane, 'corpus', 'SOURCES.md'), encoding='utf-8') as fh:
        for line in fh:
            if not line.lstrip().startswith('| S'):
                continue
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if cells and cells[0] in wanted:
                found[cells[0]] = cells
    for sid in wanted:
        cells = found.get(sid)
        if not cells:
            print('%s ABSENT from corpus/SOURCES.md' % sid)
            continue
        print('%s opened=%r used_by=%r' % (sid, cells[8], cells[10][:220]))
    print('## lane counters')
    print('knowledge_files=%d'
          % sum(1 for n in os.listdir(os.path.join(lane, 'corpus', 'knowledge'))
                if n.endswith('.md')))
    with open(os.path.join(lane, 'corpus', 'SOURCES.md'), encoding='utf-8') as fh:
        rows = sum(1 for line in fh if line.lstrip().startswith('| S'))
    print('sources_rows=%d' % rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--law-rule', default=None)
    args = ap.parse_args()
    law_rule = args.law_rule or os.path.join(
        args.lane, '.ufo', 'waves', 'round-52', 'w1', 'ExecRuleFixtures',
        'gap-rule.json')
    try:
        census(args.lane)
        device_dispositions(args.lane)
        rule_variants(args.lane, law_rule)
        miss_receipt(args.lane)
        sources_state(args.lane)
    except Exception as exc:                                  # noqa: BLE001
        print('probe failed: %r' % (exc,), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
