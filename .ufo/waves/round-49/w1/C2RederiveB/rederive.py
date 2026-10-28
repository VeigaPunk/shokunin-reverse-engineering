#!/usr/bin/env python3
"""Independent re-derivation of C2 atoms A4-A6 (no import of c2-mismatch.py). Read-only."""
import json,subprocess,hashlib,re,html,sys
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'; B='e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9'
def g(*a): return subprocess.run(['git','-C',L]+list(a),capture_output=True).stdout
sha=lambda b:hashlib.sha256(b).hexdigest()
out={}
# A4
res=json.loads(g('show',B+':.ufo/waves/round-48/r48-w1-results.json'))
names=[x['name'] for x in res['results']]
tree=[p for p in g('ls-tree','-r','--name-only',B,'.ufo/waves/round-48/w1/').decode().split('\n') if p]
pre='.ufo/waves/round-48/w1/'
def has(n): return (pre+n+'.md') in tree or any(p.startswith(pre+n+'/') and p.endswith('.md') for p in tree)
def has_strict(n): return (pre+n+'.md') in tree or any(p.startswith(pre+n+'/') and p.endswith('.md') and p.count('/')==pre.count('/')+1 for p in tree)
miss=[n for n in names if not has(n)]; miss_s=[n for n in names if not has_strict(n)]
out['A4']=dict(declared_seats=res['seats'],derived_seats=len(names),unique=len(set(names)),reports=len(names)-len(miss),missing=sorted(miss),strict_depth1_missing=sorted(miss_s),tree_files=len(tree))
# A5
for k in('c1','c2'):
    p='.ufo/waves/round-48/l1/scores/%s-final-33f65a91.json'%k; b=g('show',B+':'+p)
    out['A5_'+k]=dict(raw=sha(b),stripped=sha(b[:-1] if b.endswith(b'\n') else b),size=len(b),ends_nl=b.endswith(b'\n'))
rep=open('/home/vgpnk/Projects/shokunin/.ufo/reports/round-48/kaidoku.md',encoding='utf8').read()
for k in('c1','c2'):
    d=out['A5_'+k]; d['report_quotes_stripped_full']=d['stripped'] in rep; d['report_quotes_raw_full']=d['raw'] in rep
# A6
b=open('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/snapshots/popper.html','rb').read()
t=b.decode(); q="falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific"
tn=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',t)))
pat=r'\s*(?:<[^>]*>)?\s*'.join(map(re.escape,q.split()))
ms=list(re.finditer(pat,t,re.S)); i=ms[0].start()
hs=[(m.start(),m.group(1),html.unescape(re.sub(r'<[^>]+>','',re.sub(r'\s+',' ',m.group(3))))) for m in re.finditer(r'<h([1-6])\b([^>]*)>(.*?)</h\1>',t[:i],re.S)]
nx=re.search(r'<h([1-6])\b([^>]*)>(.*?)</h\1>',t[i:],re.S)
out['A6']=dict(snapshot_sha256=sha(b),bytes=len(b),quote_words=len(q.split()),occurrences_text=len(re.findall(re.escape(q),tn)),occurrences_rawtags=len(ms),raw_offset=i,
 headings_above_last3=hs[-3:],h3_between_quote_and_h2=[h for h in hs if h[1]=='3'],next_heading=html.unescape(re.sub(r'<[^>]+>','',nx.group(3))),next_offset=i+nx.start(),
 h2_id=re.search(r'id="([^"]+)"',[m for m in re.finditer(r'<h2([^>]*)>',t[:i])][-1].group(1)).group(1))
print(json.dumps(out,indent=1,ensure_ascii=False,default=str))
