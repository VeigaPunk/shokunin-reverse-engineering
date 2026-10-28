#!/usr/bin/env python3
"""Independent re-derivation of C2 atoms A1-A3 from base git objects (read-only). No counter import."""
import re, subprocess, json, hashlib, sys
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
B='e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9'
def g(*a, check=False):
    return subprocess.run(['git','-C',L]+list(a),capture_output=True)
def show(p): 
    r=g('show',f'{B}:{p}'); assert r.returncode==0,p; return r.stdout.decode('utf8')
out={}
# A1
sc=show('SCORECARD.md').split('\n')
i=[k for k,x in enumerate(sc) if re.match(r'^## Round 48\b',x)]
assert len(i)==1; start=i[0]
end=next((k for k in range(start+1,len(sc)) if sc[k].startswith('## ')),len(sc))
sec='\n'.join(sc[start:end])
dec=re.findall(r'\*\*Declared freeze:\*\*\s*`([0-9a-f]{40})`',sec)
out['A1_scorecard_declared']=dec
les=show('corpus/lessons/round-48.md')
hdr=[ (n+1,x) for n,x in enumerate(les.split('\n')[:6])]
m=re.findall(r'Declared freeze\s+`([0-9a-f]{40})`',les)
out['A1_lesson_header_hashes']=m
rows=re.findall(r'^\| (A\d) \|',les,re.M)
out['A1_lesson_rows']=rows
out['A1_lesson_series_claim']=re.findall(r'series (A\d–A\d)',les)
# which A-row's amendment hash is which, from SCORECARD
amend=re.findall(r'(A\d) `([0-9a-f]{8})`',sec)
out['A1_amendment_map']=amend
for nm,h in (('declared',dec[0]),('stale',m[0])):
    out[f'A1_{nm}_is_commit']=g('cat-file','-t',h).stdout.decode().strip()
out['A1_declared_amend']=[a for a,h in amend if dec[0].startswith(h)]
out['A1_stale_amend']=[a for a,h in amend if m[0].startswith(h)]
out['A1_stale_ancestor_of_declared']=g('merge-base','--is-ancestor',m[0],dec[0]).returncode
# A2
dead='663f30ee7516942a0120e7de68fe88356e680822'
out['A2_dead_type']=g('cat-file','-t',dead).stdout.decode().strip() or 'MISSING(rc=%d)'%g('cat-file','-t',dead).returncode
cands=[x for x in g('rev-list','--all').stdout.decode().split() if x.startswith('663f30ee')]
out['A2_prefix_commits_all']=cands
cb=[x for x in g('rev-list',B).stdout.decode().split() if x.startswith('663f30ee')]
out['A2_prefix_commits_base']=cb
out['A2_common_prefix_len']=len(__import__('os').path.commonprefix([dead,cands[0]]))
out['A2_actual_ancestor_of_base']=g('merge-base','--is-ancestor',cands[0],B).returncode
out['A2_actual_type']=g('cat-file','-t',cands[0]).stdout.decode().strip()
# A3
log=show('LOG.md').split('\n')
for h in ('2e785632','33f65a91','577a02a5','8847042a'):
    out['A3_'+h]=[n+1 for n,x in enumerate(log) if h in x.lower()]
    out['A3_'+h+'_commit']=g('cat-file','-t',h).stdout.decode().strip()
    out['A3_'+h+'_full']=g('rev-parse','--verify','-q',h+'^{commit}').stdout.decode().strip()
out['LOG_lines_total']=len(log)
out['LOG_sha256']=hashlib.sha256(show('LOG.md').encode()).hexdigest()
print(json.dumps(out,indent=1))
