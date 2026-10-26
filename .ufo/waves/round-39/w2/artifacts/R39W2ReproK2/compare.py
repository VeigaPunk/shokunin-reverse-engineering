import json, re, sys
A=json.load(open('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-39/c1/K2/after.json'))
B=json.load(open('rea.json'))['data']
W=json.load(open('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-39/w1/artifacts/R39C1Harness/receipts/K2/after.json'))
def nstr(s):
    if not isinstance(s,str): return s
    s=re.sub(r'[^"\s]*/rea-firmware-[A-Za-z0-9]+','<READIR>',s)
    s=re.sub(r'/fast/scratch/hyaku/kaidoku-r39/[^/"]*?(?:/c1runs/[^/"]+)?/extract','<OUTDIR>',s)
    s=re.sub(r'/fast/scratch/hyaku/kaidoku-r39/[^/"]*?/out','<OUTDIR>',s)
    s=s.replace('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-37/c1/K2/carrier.sqsh','<CARRIER>')
    s=s.replace('/fast/scratch/hyaku/kaidoku-r39/R39W2ReproK2/carrier.sqsh','<CARRIER>')
    s=s.replace('/fast/scratch/hyaku/kaidoku-r39/R39C1Harness/carriers/K2/carrier.sqsh','<CARRIER>')
    s=re.sub(r'(?<![\w/])\d{6,8}:1','<BLOBID>',s)
    return s
def n(o):
    if isinstance(o,dict): return {k:n(v) for k,v in o.items()}
    if isinstance(o,list): return [n(x) for x in o]
    if isinstance(o,str): return nstr(o)
    return o
def sem(e):
    nr=e['normalized_result']
    return {
     'chunks':[(c['handler'],c['extraction_failed'],c['encrypted'],c['range'],c['root_file_range']) for c in nr['chunks']],
     'files':sorted((f['relative_path'],f['sha256']) for f in nr['files']),
     'gaps':[(g['kind'],g['relative_path'],g['continuation_id'],tuple(g['dependencies'])) for g in nr['extraction_gaps']],
     'unpub':[(u['relative_path'],u['link_target'],u['kind']) for u in nr['unpublished_entries']],
     'continuations':nr['extraction_continuations'],
     'diag':nr['diagnostics'],
     'diag_typenames':sorted({d.get('__typename__') for d in nr['diagnostics']}),
     'depth_limited':nr['depth_limited_paths'],
     'coverage':nr['coverage'],'published_bytes':nr['published_bytes'],
     'selection':nr['selection'],'engine':nr['engine'],'provider':e['provider'],
     'predicate_type':e['predicate_type'],'operation':e['operation'],
     'confidence':e['confidence'],'authority':e['authority'],
     'limitations':e['limitations'],'analysis_profile':e['analysis_profile'],
     'environment':e['environment'],'locations':e['locations'],'evidence_links':e['evidence_links'],
     'subject_digest':e['subject']['digest'],'subject_format':e['subject']['format'],
     'parameters':{k:v for k,v in e['parameters'].items() if k not in ('path','output_directory')},
    }
sa,sb,sw=sem(A),sem(B),sem(W)
out={
 'committed_vs_mine_semantic_equal': sa==sb,
 'committed_vs_w1_semantic_equal': sa==sw,
 'raw_result_committed_vs_mine_normalized': n(A['raw_result'])==n(B['raw_result']),
 'raw_result_committed_vs_w1_normalized': n(A['raw_result'])==n(W['raw_result']),
 'nonpath_field_differences_mine': [k for k in sa if sa[k]!=sb.get(k)],
 'nonpath_field_differences_w1': [k for k in sa if sa[k]!=sw.get(k)],
 'published_bytes_sum_check': sum([22,21,10240])==A['normalized_result']['published_bytes'],
}
if sa!=sb:
    for k in sa:
        if sa[k]!=sb.get(k): print("DIFF",k,'\n author=',json.dumps(sa[k])[:400],'\n mine  =',json.dumps(sb.get(k))[:400])
print(json.dumps(out,indent=1))
