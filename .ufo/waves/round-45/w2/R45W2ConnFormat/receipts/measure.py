import re,glob,json,collections,hashlib
LANE_ROOT='/home/vgpnk/Projects/shokunin'
PAT=re.compile(r'`(tools/[A-Za-z0-9._/-]+\.(?:py|sh))`')
BARE=re.compile(r'^`([A-Za-z0-9._-]+\.(?:py|sh))`$')
def cls(c):
    if PAT.search(c): return 'fullpath'
    if BARE.match(c): return 'bare'
    return 'name'
def tables(f):
    lines=open(f,encoding='utf-8',errors='replace').read().split('\n')
    heading=''; i=0; out=[]
    while i<len(lines):
        l=lines[i]
        if l.startswith('#'): heading=l
        s=l.strip()
        if s.startswith('|') and i+1<len(lines):
            nxt=lines[i+1].strip()
            has_sep=bool(re.match(r'^\|[\s:|-]+\|$',nxt))
            hdr=[c.strip() for c in s.strip('|').split('|')]
            rows=[]; j=i+2 if has_sep else i+1
            while j<len(lines) and lines[j].strip().startswith('|'):
                rows.append([c.strip() for c in lines[j].strip().strip('|').split('|')]); j+=1
            if 'registry' in heading.lower():
                out.append(dict(heading=heading.strip(),line=i+1,ncols=len(hdr),header=hdr,sep=has_sep,
                                nrows=len(rows),c0=dict(collections.Counter(cls(r[0]) for r in rows if r)),
                                hdrsize_sha=hashlib.sha256(s.encode()).hexdigest()))
            i=j if rows or has_sep else i+1
            continue
        i+=1
    return out
res={}
for f in sorted(glob.glob(LANE_ROOT+'/*/SKILL.md')):
    res[f.split('/')[-2].replace('-shokunin','')]=tables(f)
agg=dict(tables=0,by_ncols=collections.Counter(),eight_col_lanes=[],fullpath_lanes={},sep_missing=[],header_hashes=collections.Counter())
for lane,ts in res.items():
    agg['tables']+=len(ts)
    has8=False; fp=0
    for t in ts:
        agg['by_ncols'][t['ncols']]+=1
        if t['ncols']==8: has8=True
        fp+=t['c0'].get('fullpath',0)
        if not t['sep']: agg['sep_missing'].append(f"{lane}:{t['line']} ({t['ncols']} cols) {t['heading'][:50]}")
        if t['ncols']==7: agg['header_hashes'][t['hdrsize_sha']]+=1
    if has8: agg['eight_col_lanes'].append(lane)
    agg['fullpath_lanes'][lane]=fp
print(json.dumps({'by_ncols':dict(agg['by_ncols']),'tables':agg['tables'],
 'eight_col_lane_count':len(agg['eight_col_lanes']),'eight_col_lanes':agg['eight_col_lanes'],
 'fullpath_cell0_by_lane':{k:v for k,v in agg['fullpath_lanes'].items() if v},
 'sep_missing':agg['sep_missing'],
 'seven_col_header_variants':len(agg['header_hashes']),
 'kaidoku_tables':[{k:t[k] for k in ('line','ncols','sep','nrows','c0','heading')} for t in res['kaidoku']]},indent=1))
