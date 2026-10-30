#!/usr/bin/env python3
"""Independent scratch port of R50 disposition semantics for R52 controls."""
import json, pathlib
BASE = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
IDS = ('c6430','c6490','g7581','g7582')
OLD = json.loads((BASE/'tools/round-50/gap-rule.json').read_text())
NEW = json.loads(json.dumps(OLD))
NEW['claim'] = 'R52-C1'
NEW['allowed']['char-device'] = []
NEW['required']['char-device'] = False
NEW['removed'].get('silent',{}).pop('char-device',None)

def norm(p):
    return '/'.join(x for x in str(p).replace('\\','/').split('/') if x not in ('','.'))
def model_eval(env, rows, model):
    nr = env.get('normalized_result') or {}
    chunks = nr.get('chunks') or []
    roots = [norm(c.get('extract_path') or c.get('output_path') or c.get('path')) for c in chunks if isinstance(c,dict)]
    roots = [r for r in roots if r.endswith('_extract')]
    root = roots[0] if roots else 'firmware.bin_extract'
    def rel(p):
        p=norm(p)
        if p.startswith('$output/'): p=p[len('$output/'):]
        if p == root: return ''
        return p[len(root)+1:] if p.startswith(root+'/') else None
    byrel={norm(r):(k,d) for r,k,d in rows}
    at={}
    for r,k,d in rows: at.setdefault(norm(r),[]).append((norm(r),k,d))
    gap_by={}; structural={}
    for g in nr.get('extraction_gaps') or []:
        if not isinstance(g,dict): return False,'non-object gap'
        kind,rp=g.get('kind'),g.get('relative_path')
        if rp is None:
            if kind not in model.get('structural',{}): return False,f'pathless gap kind {kind!r} lacks structural allowance'
            structural[kind]=structural.get(kind,0)+1; continue
        if kind in model.get('structural',{}): return False,f'structural gap {kind!r} has a path'
        r=rel(rp); hits=at.get(r,[]) if r else []
        if len(hits)!=1: return False,f'gap path {rp!r} matched {len(hits)} rows'
        row=hits[0]; ek=row[1]
        if kind not in model.get('allowed',{}).get(ek,[]): return False,f'{kind!r} not allowed for {ek!r} {row[0]!r}'
        gap_by.setdefault(row[0],[]).append(kind)
    for kind,n in structural.items():
        if n>model['structural'][kind]: return False,f'{kind} structural overflow {n}'
    removed={}
    diagname=model.get('removed',{}).get('diagnostic')
    output=nr.get('output_directory')
    trusted=pathlib.PurePosixPath(output).parent if isinstance(output,str) and output.startswith('/') else None
    for d in nr.get('diagnostics') or []:
        report=d.get('report') or {}
        if report.get('__typename__') != diagname: continue
        link=report.get('link')
        if not isinstance(link,str) or trusted is None or not pathlib.PurePosixPath(link).is_relative_to(trusted): return False,'unresolvable removal link'
        parts=pathlib.PurePosixPath(link).parts; rootparts=pathlib.PurePosixPath(root).parts
        found=None
        for i in range(len(parts)-len(rootparts),len(trusted.parts)-1,-1):
            if parts[i:i+len(rootparts)]==rootparts: found='/'.join(parts[i+len(rootparts):]); break
        if found is None: return False,'removal link has no extract-root segment'
        hits=at.get(norm(found),[])
        if len(hits)!=1: return False,f'removal path {found!r} matched {len(hits)} rows'
        row=hits[0]
        if row[1] not in model.get('removed',{}).get('kinds',[]): return False,f'removal kind {row[1]!r} not allowed'
        if gap_by.get(row[0]): return False,f'{row[0]!r} both gap and removal'
        removed[row[0]]=removed.get(row[0],0)+1
    silent=[]; missing=[]
    for r,k,d in rows:
        need=model.get('required',{}).get(k,bool(model.get('allowed',{}).get(k)))
        if not need or gap_by.get(norm(r)) or removed.get(norm(r)): continue
        allows=model.get('removed',{}).get('silent',{}).get(k,[])
        if any((x=='empty-target' and d=='') or x==d for x in allows): silent.append(r)
        else: missing.append(r)
    if missing: return False, f'undisposed required entries: {len(missing)} (sample {missing[:4]})'
    return True,f'{sum(len(v) for v in gap_by.values())} path gaps; structural={structural}; removals={sum(removed.values())}; silent={len(silent)}; nonregular={len(rows)}'

def main():
    rows_out=[]
    for ident in IDS:
        env=json.loads((BASE/f'corpus/evidence/round-50/c1/{ident}/after.json').read_text())
        rows=[]
        for line in (BASE/f'tools/round-50/oracle/{ident}.nonregular.tsv').read_text().splitlines():
            cols=line.split('\t'); cols += ['']*(3-len(cols)); rows.append((cols[0],cols[1],cols[2]))
        old=model_eval(env,rows,OLD); new=model_eval(env,rows,NEW)
        rows_out.append({'carrier':ident,'round50':{'pass':old[0],'detail':old[1]},'r52_law':{'pass':new[0],'detail':new[1]}})
    print(json.dumps({'method':'independent implementation of path-resolved gap, structural gap, removal, required disposition and per-row silent allowance rules','expected_round50_passes':['c6430','c6490'],'expected_r52_passes':list(IDS),'results':rows_out,'round50_pass_count':sum(x['round50']['pass'] for x in rows_out),'r52_pass_count':sum(x['r52_law']['pass'] for x in rows_out)},sort_keys=True,indent=2))
if __name__=='__main__': main()
