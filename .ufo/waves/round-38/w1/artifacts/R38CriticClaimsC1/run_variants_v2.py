#!/usr/bin/env python3
"""v2 (freeze-draft) extension: paired before/after fabricated receipts scored by the v2 draft counter."""
import copy, json, os, subprocess, sys
sys.path.insert(0, os.environ['S'])
import run_variants as rv

S = os.environ['S']
rv.F = os.path.join(S, 'fx2')
rv.RES = os.path.join(S, 'results-v2')
rv.COUNTER = os.path.join(S, 'v2/tools/round-38/c1-counter.py')
rv.ART = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-38/w1/artifacts/R38CriticClaimsC1'
os.makedirs(rv.RES, exist_ok=True)


def main():
    rv.FZVAR = rv.setup()
    FZ = rv.FZVAR
    after = rv.fake_receipts()
    before = {}
    for k, e in after.items():
        b = copy.deepcopy(e)
        b.pop('evidence_id', None)
        nr = b['normalized_result']
        nr['files'] = []
        nr['extraction_gaps'] = [{'kind': 'missing-extractor-dependency', 'handler': 'squashfs_v4_be',
                                 'dependencies': ['sasquatch-v4be']}]
        nr['coverage'] = 'partial'
        nr['published_bytes'] = 0
        before[k] = rv.mint(b)
    recs = {}
    for k in after:
        recs['corpus/evidence/round-38/c1/%s/before.json' % k] = json.dumps(before[k], indent=1)
        recs['corpus/evidence/round-38/c1/%s/after.json' % k] = json.dumps(after[k], indent=1)
    ENTRY, prov_ok = rv.ENTRY, rv.prov_with('round38')
    reg_ok = rv.add_reg(rv.git('show', 'HEAD:corpus/SOURCES.md'), rv.reg_row())
    readme_ok = rv.readme_with(rv.STEM)
    entry_ok = rv.entry_text('S112')
    surf = {ENTRY: entry_ok, 'PROVINCE.md': prov_ok, 'corpus/SOURCES.md': reg_ok, 'corpus/README.md': readme_ok}

    def var(**kw):
        d = dict(recs, **surf)
        d.update(kw)
        return d

    after_gap = copy.deepcopy(after)
    for k in after_gap:
        after_gap[k]['normalized_result']['extraction_gaps'] = [
            {'kind': 'missing-extractor-dependency', 'handler': 'squashfs_v4_be', 'dependencies': ['sasquatch-v4be']}]
        after_gap[k].pop('evidence_id', None)
        rv.mint(after_gap[k])
    before_nogap = {}
    for k, b in before.items():
        b = copy.deepcopy(b)
        b['normalized_result']['extraction_gaps'] = []
        b.pop('evidence_id', None)
        before_nogap[k] = rv.mint(b)
    prov_v = {}
    for k, e in after.items():
        e = copy.deepcopy(e)
        e['provider'] = {'id': 'unblob', 'name': 'NotUnblob at all', 'version': '0.0.1'}
        e.pop('evidence_id', None)
        prov_v[k] = rv.mint(e)

    variants = [
        ('v2-do-nothing', {}),
        ('v2-receipts-only', dict(recs)),
        ('v2-full', var()),
        ('v2-carrier-bytes-swapped', var(**{'corpus/evidence/round-37/c1/K1/carrier.sqsh': b'not a squashfs image\n',
                                            'corpus/evidence/round-37/c1/K3/carrier.bin': b''})),
        ('v2-readme-stem-prefix', var(**{'corpus/README.md': rv.readme_with(rv.STEM + '-draft')})),
        ('v2-row-decoy-duplicate-heading', var(**{'PROVINCE.md': rv.prov_with('dup')})),
        ('v2-reuse-existing-today-row', var(**{ENTRY: rv.entry_text('S110'),
                                               'corpus/SOURCES.md': rv.append_used_by(rv.git('show', 'HEAD:corpus/SOURCES.md'), 'S110', ENTRY)})),
        ('v2-entry-stub-no-claim-text', var(**{ENTRY: 'source: S112\n'})),
        ('v2-provider-version-unchecked', {**recs, **{k: json.dumps(v, indent=1) for k, v in
                                        (('corpus/evidence/round-38/c1/%s/after.json' % k, pv) for k, pv in prov_v.items())}, **surf}),
        ('v2-after-carries-gap', var(**{'corpus/evidence/round-38/c1/K1/after.json': json.dumps(after_gap['K1'], indent=1)})),
        ('v2-before-carries-no-gap', var(**{'corpus/evidence/round-38/c1/K1/before.json': json.dumps(before_nogap['K1'], indent=1)})),
    ]
    rows = []
    for name, edits in variants:
        code, res = rv.run_variant(name, edits)
        row = {'variant': name, 'exit': code, 'met_target': res.get('met_target'),
               'carriers_matched': res.get('carriers_matched'), 'bindings': res.get('bindings')}
        rows.append(row)
        print(json.dumps(row, sort_keys=True))
    json.dump({'counter': 'v2 draft sha256 122fb982309db9570c8127b0f618b05087e05fe013151587d259b77f9e469b95',
               'fixture_freeze': FZ, 'rows': rows}, open(os.path.join(rv.ART, 'v2-draft-falsifiers.json'), 'w'), indent=1, sort_keys=True)


if __name__ == '__main__':
    main()
