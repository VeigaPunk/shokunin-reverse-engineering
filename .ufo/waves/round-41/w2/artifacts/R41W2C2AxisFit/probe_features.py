import json, sys, hashlib
ROOT='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
def _as_list(v):
    return v if isinstance(v, list) else []
def _tokens(v):
    if isinstance(v, str): return sorted(v.split())
    if isinstance(v, list): return sorted(str(x) for x in v)
    return []
def _tri(v):
    if isinstance(v, bool): return 'yes' if v else 'no'
    if v is None: return 'n/a'
    s = str(v).strip().lower()
    return 'yes' if s in ('yes','true','1','y') else ('no' if s in ('no','false','0','n') else 'n/a')
def _pub(v):
    if isinstance(v, (int, float)): return 'nonzero' if v > 0 else 'zero'
    if isinstance(v, str):
        s=v.strip().lower()
        if s in ('nonzero','>0','positive','non-zero'): return 'nonzero'
        if s in ('0','zero','none','empty','no','false'): return 'zero'
    return 'zero'
def observed_features(data):
    nr = data.get('normalized_result') if isinstance(data, dict) else None
    nr = nr if isinstance(nr, dict) else {}
    handlers=set(); failed=False
    for chunk in _as_list(nr.get('chunks')):
        if not isinstance(chunk, dict): continue
        h=chunk.get('handler')
        if isinstance(h,str) and h.startswith('squashfs'): handlers.add(h)
        if chunk.get('extraction_failed') is True: failed=True
    gap_kinds=set(); dependencies=set()
    for gap in _as_list(nr.get('extraction_gaps')):
        if not isinstance(gap,dict): continue
        k=gap.get('kind')
        if isinstance(k,str):
            gap_kinds.add(k)
            if k=='extractor-failure': failed=True
        for dep in _as_list(gap.get('dependencies')):
            if isinstance(dep,str): dependencies.add(dep)
    # BE from diagnostics report commands
    cmds=[]
    for diag in _as_list(nr.get('diagnostics')):
        rep = diag.get('report') if isinstance(diag,dict) else None
        if isinstance(rep,dict) and isinstance(rep.get('command'),str): cmds.append(rep['command'])
    be='n/a'
    if cmds:
        be='no'
        for c in cmds:
            if '-be' in c.split(): be='yes'; break
    symlink=False
    for diag in _as_list(nr.get('diagnostics')):
        rep = diag.get('report') if isinstance(diag,dict) else None
        if isinstance(rep,dict) and rep.get('__typename__')=='MaliciousSymlinkRemoved': symlink=True
    def scan(o):
        nonlocal symlink
        if isinstance(o,dict):
            if o.get('__typename__')=='MaliciousSymlinkRemoved': symlink=True
            for v in o.values(): scan(v)
        elif isinstance(o,list):
            for v in o: scan(v)
    scan(data.get('raw_result'))
    return {'handler_set': sorted(handlers), 'gap_kinds': sorted(gap_kinds),
            'gap_dependencies': sorted(dependencies), 'be_argv': be,
            'symlink_removed': symlink,
            'published': 'nonzero' if _as_list(nr.get('files')) else 'zero',
            'extraction_failed': failed}
def canon(obj):
    if not isinstance(obj,dict): return None
    out={}
    for k,v in obj.items():
        key=str(k).strip().lower()
        if key in ('handler_set','gap_kinds','gap_dependencies'): out[key]=_tokens(v)
        elif key=='be_argv': out[key]=_tri(v)
        elif key=='symlink_removed': out[key]=_tri(v)=='yes'
        elif key=='published': out[key]=_pub(v)
        elif key=='extraction_failed': out[key]=_tri(v)=='yes'
    return out or None
m=json.load(open(ROOT+'/corpus/evidence/round-41/c2/heldout/manifest.json'))
req={'handler_set','gap_kinds','gap_dependencies','be_argv','symlink_removed','published'}
missing=[]; bad=[]; n=0
for c in m['carriers']:
    cid=c['id']
    e=json.load(open(ROOT+'/corpus/evidence/round-41/c2/heldout/'+cid+'/envelope.json'))
    obs=observed_features(e)
    decl=canon(c.get('declared'))
    if decl is None or any(k not in decl for k in req):
        missing.append(cid); continue
    n+=1
    shared=[k for k in decl if k in obs]
    diff=[k for k in shared if decl[k]!=obs[k]]
    if diff: bad.append((cid,diff,decl,obs))
print('carriers checked:', n, 'missing:', len(missing), missing)
print('mismatches:', len(bad))
for cid,diff,decl,obs in bad[:6]:
    print(cid, diff)
    print('  declared:', json.dumps(decl))
    print('  observed:', json.dumps(obs))
