#!/usr/bin/env python3
# P2b (replaces P2, which was a no-op: provenance.json has no top-level output_directory key).
# Run from the scratch seat dir after drive.py/drive2.py; scratch-only, never the lane.
import sys, json, hashlib
sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r49/C1RunMut/mut')
sys.argv = ['drive3']
import drive as D
D.CLONE_XPIN[0] = D.S + '/clone0/tools/round-27/xpin-attribute.mjs'
D.RESULTS.extend(json.load(open(D.S + '/results.json')))


def m_prov_rea_outdir_lie(d):
    doc = json.load(open(d + '/provenance.json'))
    doc['rea_output_directory'] = D.evpath(d)          # the committed evidence path
    doc['rea_output_directory_mode'] = 'evidence'
    json.dump(doc, open(d + '/provenance.json', 'w'), sort_keys=True, indent=2)


name = 'P2b_provenance_rea_outdir_lies_evidence'
srcs = D.fresh(name)
before = {k: hashlib.sha256(open(srcs[k] + '/provenance.json', 'rb').read()).hexdigest() for k in D.IDS}
for k in D.IDS:
    m_prov_rea_outdir_lie(srcs[k])
after = {k: hashlib.sha256(open(srcs[k] + '/provenance.json', 'rb').read()).hexdigest() for k in D.IDS}
print('provenance.json changed:', {k: before[k] != after[k] for k in D.IDS})
D.scenario(name, srcs)
