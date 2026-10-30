#!/usr/bin/env python3
"""CritTriV6 (r52-w1) read-only attack probe for R52-C2.

Reads the committed round-42 envelope corpus, the committed round-50 c3 receipt, the
round-50 reader-census receipt and the round-49 v3-readers receipt. Writes nothing into
the lane. Usage: python3 -I -B probe_v6_attack.py --lane LANE --out JSON
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys

ap = argparse.ArgumentParser()
ap.add_argument('--lane', required=True)
ap.add_argument('--out', required=True)
ns = ap.parse_args()
lane = os.path.abspath(ns.lane)
V5 = os.path.join(lane, 'tools/round-50-c3/sqfs-triage-v5.py')
ENV = os.path.join(lane, '.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes')
C3 = os.path.join(lane, '.ufo/waves/round-50/c3/c3-after.json')
CENSUS = os.path.join(lane, '.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt')
V3R = os.path.join(lane, '.ufo/waves/round-49/w1/C1ScribeEntry/v3-readers.out')

spec = importlib.util.spec_from_file_location('v5', V5)
v5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v5)

report = {'probe': 'CritTriV6-r52-w1', 'lane': lane, 'checks': {}}

# P1: which envelopes does a FAILED-only, P=0, ddwrt-in-HF row capture?
moved, failed = [], []
for d in sorted(os.listdir(ENV)):
    feat = v5.load_envelope(os.path.join(ENV, d, 'envelope.json'))
    lab, act, _ = v5.evaluate(feat)
    if 'extractor-failure' in feat['G']:
        failed.append({'envelope': d, 'F': feat['F'], 'P': feat['P'], 'v5_label': lab,
                       'v5_action': act})
    if 'extractor-failure' in feat['G'] and feat['P'] == 0 and \
            any(h == 'squashfs_v3_ddwrt' for h in feat['HF']):
        moved.append(d)
report['checks']['P1_moving_set_ddwrt_failed_P0'] = moved
report['checks']['P1_failed_envelopes_total'] = len(failed)
report['checks']['P1_failed_envelopes'] = failed

# P2: ddwrt-family clean envelopes and their reader verdict by subject digest
census_rows = {}
for line in open(CENSUS, encoding='utf-8'):
    parts = line.split()
    if len(parts) >= 6 and parts[0].startswith('squashfs_v3') and len(parts[2]) == 12:
        census_rows[parts[2]] = (parts[0], parts[1], parts[3], parts[4], ' '.join(parts[5:]))
c3 = json.load(open(C3, encoding='utf-8'))
residue = []
for e in c3['envelopes']:
    if 'squashfs_v3_ddwrt' in e['features']['F'] and e['table_label'] == 'clean':
        p = os.path.join(ENV, e['envelope'], 'envelope.json')
        dig = json.load(open(p, encoding='utf-8'))['data']['subject']['digest']['sha256']
        residue.append({'envelope': e['envelope'], 'label': e['table_label'],
                        'action': e['table_action'], 'subject_sha12': dig[:12],
                        'census_row': census_rows.get(dig[:12], 'NO CENSUS ROW')})
report['checks']['P2_ddwrt_clean_residue'] = residue
report['checks']['P2_ddwrt_clean_residue_count'] = len(residue)

# P3: does the round-50 reader census cover each FAILED-envelope family, and by digest?
fam_rows = {}
for line in open(CENSUS, encoding='utf-8'):
    parts = line.split()
    if len(parts) >= 6 and parts[0].startswith('squashfs_v') and len(parts[2]) == 12:
        fam_rows.setdefault(parts[0], []).append(parts[5:])
coverage = {}
for f in failed:
    fam = f['F'][0] if f['F'] else None
    dig = json.load(open(os.path.join(ENV, f['envelope'], 'envelope.json'),
                         encoding='utf-8'))['data']['subject']['digest']['sha256']
    coverage[f['envelope']] = {'family': fam, 'family_in_census': fam in fam_rows,
                               'subject_has_census_row': dig[:12] in census_rows}
report['checks']['P3_failed_coverage'] = coverage

# P4: nopad ddwrt bytes: independent readers vs sasquatch success (round-49 receipt)
v3r = open(V3R, encoding='utf-8').read()
block = v3r.split('== v3ddwrt-be--squashfs_v3.be.nopad.bin', 1)[1].split('== v3ns', 1)[0]
report['checks']['P4_round49_v3ddwrt_nopad_block'] = block.strip().splitlines()
report['checks']['P4_sasquatch_on_nopad_clean'] = [
    e['envelope'] for e in c3['envelopes']
    if e['envelope'].endswith('nopad_ddefault') or e['envelope'] == 'dep_A2_squashfs_v3.be.nopad']

# P5: are the two v6 new-row actions identical (swap mutant would be a no-op)?
rules, _ = v5.parse_skill(open(os.path.join(lane, 'SKILL.md'), encoding='utf-8').read())
acts = {r['label']: r['action'] for r in rules}
report['checks']['P5_actions'] = {k: acts.get(k) for k in
                                  ('clean-unverified', 'no-reader-failure', 'legacy-body-failure')}

report['sha256_self'] = hashlib.sha256(open(__file__, 'rb').read()).hexdigest()
text = json.dumps(report, indent=2, sort_keys=True)
with open(ns.out, 'w', encoding='utf-8') as fh:
    fh.write(text + '\n')
print(hashlib.sha256(text.encode()).hexdigest())
sys.exit(0)
