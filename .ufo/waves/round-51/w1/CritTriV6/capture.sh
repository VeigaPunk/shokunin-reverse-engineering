#!/usr/bin/env bash
# CritTriV6 evidence capture — read-only against the lane; writes receipts into the seat dir.
set -u
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
SEAT="$LANE/.ufo/waves/round-51/w1/CritTriV6"
S=/fast/scratch/hyaku/kaidoku-r51/w1-CritTriV6
BASE=1aa273694f4409d3432fbcd73e83a33bee0dd8e9
DRAFT=f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab
mkdir -p "$SEAT/receipts"
rc=0
run() {  # run <name> <cmd...>
  local name="$1"; shift
  local out="$SEAT/receipts/$name.out"
  local meta="$SEAT/receipts/$name.meta"
  local utc; utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  ( "$@" ) >"$out" 2>"$SEAT/receipts/$name.err"
  local ec=$?
  local sha; sha=$(sha256sum "$out" | cut -d' ' -f1)
  printf 'command: %s\nexit_code: %s\nstdout_sha256: %s\nutc: %s\n' "$*" "$ec" "$sha" "$utc" >"$meta"
  echo "[$name] exit=$ec sha=$sha"
  [ "$ec" -ne 0 ] && rc=1
  return 0
}

run e1_registry_vs_census2 python3 - "$LANE" "$BASE" "$S" <<'EOF'
import json,re,subprocess,sys
LANE,BASE,S=sys.argv[1],sys.argv[2],sys.argv[3]
def show(p,rev=BASE):
    r=subprocess.run(['git','-C',LANE,'show',f'{rev}:{p}'],capture_output=True,text=True)
    return r.stdout if r.returncode==0 else None
sk=show('SKILL.md')
body=sk.split("<!-- instrument-registry v2 -->",1)[1].split("<!-- /instrument-registry -->",1)[0]
reg=[]
for line in body.splitlines():
    if re.match(r"^\|\s*`",line.strip()):
        cs=[c.strip() for c in line.strip().strip("|").split("|")]
        if len(cs)==7: reg.append(cs[0].strip("` "))
doc=json.loads(show('tools/round-48/census2.json'))
c=set(doc['paths'])
print('registry_rows',len(reg)); print('census2_paths',len(c))
extra=sorted(set(reg)-c); print('registry_outside_census2',len(extra))
for e in extra: print(' ',e)
print('census2_paths_without_registry_row',len(c-set(reg)))
EOF

run e2_label_moves python3 - "$LANE" "$S" <<'EOF'
import importlib.util,json,sys
LANE,S=sys.argv[1],sys.argv[2]
spec=importlib.util.spec_from_file_location('v5',S+'/v5.py')
v5=importlib.util.module_from_spec(spec); spec.loader.exec_module(v5)
ENV=LANE+'/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes'
rec=json.load(open(LANE+'/.ufo/waves/round-50/c3/c3-after.json'))
def labels(noreader):
    v5.NO_READER_FAMILIES=tuple(noreader); v5.NO_READER_SET=frozenset(noreader)
    out={}
    for eid,path in v5.envelope_entries(ENV):
        f=v5.load_envelope(path)
        try: lab,act,st=v5.evaluate(f)
        except Exception: lab,act,st=None,None,None
        out[eid]=(lab,act)
    return out
cur=labels(v5.NO_READER_FAMILIES)
print('reproduction_mismatches_vs_receipt',sum(1 for k in cur if cur[k][0]!=rec['evaluator_labels'][k]))
print('NO_READER_FAMILIES',v5.NO_READER_FAMILIES); print('READER_BACKED_V1V3',v5.READER_BACKED_V1V3)
moved=sorted(k for k in cur if cur[k][0]!=rec['evaluator_labels'][k])
print('=== v6 proposal A: family-level ddwrt -> no-reader (BOTH sets) ===')
v5.READER_BACKED_V1V3=('squashfs_v1','squashfs_v2','squashfs_v3')
full=labels(tuple(v5.NO_READER_FAMILIES)+('squashfs_v3_ddwrt',))
d=sorted(k for k in cur if cur[k][0]!=full[k][0])
print('labels_moved',len(d))
for k in d: print(' ',k,cur[k][0],'->',full[k][0],'|',cur[k][1],'->',full[k][1])
EOF

run e3_envelope_census_binding python3 - "$LANE" <<'EOF'
import json,os,sys
LANE=sys.argv[1]
C=LANE+'/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes'
cen={}
for line in open(LANE+'/.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt'):
    if line.startswith('squashfs_v3'):
        p=line.split()
        if len(p)>=6: cen[p[2]]=(p[0],p[1],p[3],p[4],p[5])
rows=[]
for n in sorted(os.listdir(C)):
    fp=os.path.join(C,n,'envelope.json')
    if not os.path.exists(fp): continue
    d=json.load(open(fp)); data=d.get('data',d)
    sha=((data.get('subject') or {}).get('digest') or {}).get('sha256','')
    s12=sha[:12]
    fam,verdict=cen.get(s12,(None,'(no census row)'))
    rows.append((n,fam or '-',s12,verdict))
print('=== corpus envelopes bound to a reader-census row (sha256[:12]) ===')
for n,f,s,v in rows:
    if v!='(no census row)': print('%-46s %-22s %s %s'%(n,f,s,v))
print()
print('=== NO-READER bodies that carry label clean/none (oracle match prescribed) ===')
rec=json.load(open(LANE+'/.ufo/waves/round-50/c3/c3-after.json'))
lab={e['envelope']:(e['evaluator_label'],e['evaluator_action']) for e in rec['envelopes']}
for n,f,s,v in rows:
    if v.startswith('NO-READER') and lab.get(n,('',''))[0]=='clean':
        print('%-46s %-14s %s %s'%(n,f,s,lab[n]))
EOF

run e4_census3_floor python3 - "$LANE" "$DRAFT" <<'EOF'
import re,subprocess,sys
LANE,DRAFT=sys.argv[1],sys.argv[2]
def show(p,rev=DRAFT):
    r=subprocess.run(['git','-C',LANE,'show',f'{rev}:{p}'],capture_output=True,text=True)
    return r.stdout if r.returncode==0 else None
TOOL=re.compile(r"tools/round-(?:4[1-9]|5[0-1])(?:-[a-z0-9]+)?/[A-Za-z0-9._/-]+\.(?:py|sh)")
named={}
for n in range(41,52):
    for cf in (f'plans/round-{n}-claims.md', f'plans/round-{n}-attempt2-claims.md'):
        b=show(cf)
        if b is None: continue
        for m in TOOL.finditer(b): named.setdefault(m.group(0),[]).append(cf)
present=sorted(p for p in named if show(p) is not None)
sk=show('SKILL.md')
body=sk.split("<!-- instrument-registry v2 -->",1)[1].split("<!-- /instrument-registry -->",1)[0]
reg=set()
for line in body.splitlines():
    if re.match(r"^\|\s*`",line.strip()):
        cs=[c.strip() for c in line.strip().strip("|").split("|")]
        if len(cs)==7: reg.add(cs[0].strip("` "))
print('claims_derived_census3_paths (rounds 41..51)',len(present))
print('registry_rows',len(reg))
extra=sorted(reg-set(present))
print('FLOOR registry_rows_outside_claims_derived_census3',len(extra))
for e in extra: print('  ',e,'| named_in:',named.get(e,'NOWHERE'))
print('census3_paths_without_registry_row',len(set(present)-reg), sorted(set(present)-reg))
EOF

run e5_marker_chain grep -n "MARKER_V5 = \|MARKER_V4 = \|REFUSED_MARKERS = \|marker_index = _find_marker(lines, MARKER_V5)\|marker_index = _find_marker(lines, MARKER_V4)\|raise TableError" "$LANE/tools/round-50-c3/sqfs-triage-v5.py"

run e6_freeze_ancestry git -C "$LANE" merge-base --is-ancestor 435d41fd4ad9211d1579fc447936fb33d2b74467 "$BASE"

run e7_skill_markers_at_base git -C "$LANE" show "$BASE:SKILL.md"

run e8_ddwrt_reader_census_rows grep "squashfs_v3_ddwrt" "$LANE/.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt"

run e9_registry_rows_at_draft python3 - "$LANE" "$DRAFT" <<'EOF'
import re,subprocess,sys
LANE,DRAFT=sys.argv[1],sys.argv[2]
r=subprocess.run(['git','-C',LANE,'show',f'{DRAFT}:SKILL.md'],capture_output=True,text=True)
sk=r.stdout
body=sk.split("<!-- instrument-registry v2 -->",1)[1].split("<!-- /instrument-registry -->",1)[0]
n=0
for line in body.splitlines():
    if re.match(r"^\|\s*`",line.strip()):
        cs=[c.strip() for c in line.strip().strip("|").split("|")]
        if len(cs)==7: n+=1
print('registry_rows_at_draft',n)
EOF

exit $rc
