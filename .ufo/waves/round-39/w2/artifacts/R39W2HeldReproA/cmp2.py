import json, re, sys
H='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-39/c2/heldout/'
S='/fast/scratch/hyaku/kaidoku-r39/R39W2HeldReproA/'
SCRATCH=re.compile(r'/fast/scratch/hyaku/kaidoku-r39/\S*?/(?:rea-firmware-[A-Za-z0-9]+|r39-heldout-[A-Za-z0-9]+/rea-[A-Za-z0-9]+/out)')
def norm(o, outdir):
    if isinstance(o,dict): return {k:norm(v,outdir) for k,v in o.items() if k not in ('provider_id','provider_blob_id')}
    if isinstance(o,list): return [norm(v,outdir) for v in o]
    if isinstance(o,str):
        s=o.replace(outdir,'$OUT') if outdir else o
        return SCRATCH.sub('$RUN',s)
    return o
def diff(a,b,p=''):
    d=[]
    if type(a) is not type(b): return [(p,'type',type(a).__name__,type(b).__name__)]
    if isinstance(a,dict):
        for k in sorted(set(a)|set(b)):
            if k not in a: d.append((p+'/'+k,'only-fresh',b[k]))
            elif k not in b: d.append((p+'/'+k,'only-committed',a[k]))
            else: d+=diff(a[k],b[k],p+'/'+k)
    elif isinstance(a,list):
        if len(a)!=len(b): d.append((p,'len',len(a),len(b)))
        for i in range(min(len(a),len(b))): d+=diff(a[i],b[i],'%s[%d]'%(p,i))
    elif a!=b: d.append((p,'value',a,b))
    return d
for i in sys.argv[1:]:
    c=json.load(open(H+i+'/envelope.json')); f=json.load(open(S+'fresh/%s-full.json'%i))
    d=diff(norm(c['normalized_result'],c['parameters']['output_directory']),
           norm(f['data']['normalized_result'],f['data']['parameters']['output_directory']))
    print(i,'semantic diffs (paths+blob ids normalized):',len(d))
    for x in d[:15]: print('  ',x)
