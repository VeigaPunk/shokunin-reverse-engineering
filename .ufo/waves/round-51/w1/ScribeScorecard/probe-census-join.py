import json,re
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
cen=open(LANE+'/.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt').read()
rows={}
for line in cen.splitlines():
    m=re.match(r'^(squashfs_v3\w*)\s+(\S+)\s+([0-9a-f]{12})\s+(\d)\s+(\d)\s+(.*)$',line)
    if m: rows[(m.group(1),m.group(2))]=dict(digest=m.group(3),unq=m.group(4),z=m.group(5),verdict=m.group(6))
by_digest={}
for (fam,fx),v in rows.items(): by_digest.setdefault(v['digest'],[]).append((fam,fx,v['verdict']))
man={e['run']:e.get('input') for e in json.load(open(LANE+'/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/manifest.json'))['entries']}
d=json.load(open(LANE+'/.ufo/waves/round-50/c3/c3-after.json'))
print('census rows:',len(rows),' distinct fixtures:',len({fx for _,fx in rows}))
amb=[(dg,v) for dg,v in by_digest.items() if len(v)>1]
print('digests shared by >1 family (ambiguous by digest alone):',len(amb))
for dg,v in amb[:4]: print('   ',dg,v)
print()
print(f"{'FAILED envelope':<36} {'own digest':<14} {'own in census':<14} {'parent fixture':<30} {'family+parent row':<20}")
for e in d['envelopes']:
    f=e.get('features',{})
    if 'extractor-failure' not in (f.get('G') or []): continue
    env=e['envelope']
    own=json.load(open(f"{LANE}/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/{env}/envelope.json"))['data']['subject']['digest']['sha256'][:12]
    inp=man.get(env) or {}
    parent=(inp.get('parent') or '')
    base=re.sub(r'\s*\(.*\)\s*$','',parent).strip()
    fam=(f.get('F') or [None])[0]
    row=rows.get((fam,base))
    print(f"{env:<36} {own:<14} {str(own in by_digest):<14} {base:<30} {(row['verdict'][:18] if row else 'NO ROW'):<20}")
