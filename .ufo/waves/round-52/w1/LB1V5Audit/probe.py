#!/usr/bin/env python3
import hashlib, importlib.util, json, pathlib, sys
src='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50-c3/sqfs-triage-v5.py'
corpus='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes'
spec=importlib.util.spec_from_file_location('v5',src); m=importlib.util.module_from_spec(spec); sys.modules['v5']=m; spec.loader.exec_module(m)
rules,_=m.parse_skill(m.SKELETON.format(block=m.V5_BLOCK))
viol=[]; total=0
for p in sorted(pathlib.Path(corpus).glob('*/envelope.json')):
    obj=json.loads(p.read_text()); feat=m.features(m.envelope_data(obj,str(p))); label,action=m.decision(m.classify(rules,feat)); total+=1
    if feat.get('OP')=='extract_firmware' and 'squashfs_v3_ddwrt' in feat.get('H',[]) and feat.get('G')==['extractor-failure'] and feat.get('P')==0 and label=='legacy-body-failure' and action=='cross-read-legacy':
        viol.append({'envelope':p.parent.name,'label':label,'action':action})
print(json.dumps({'total':total,'violations':viol},sort_keys=True,separators=(',',':')))
