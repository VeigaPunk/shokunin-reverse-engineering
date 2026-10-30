#!/usr/bin/env bash
# SentCreds scan driver - all read-only. Writes receipts into $OUT.
set -u
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
OUT="$1"
: > "$OUT"
log(){ printf '%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$1" "$2" "$3" >> "$OUT"; }
run(){
  local name="$1" cmd="$2"
  local sout=$(mktemp) serr=$(mktemp)
  eval "$cmd" >"$sout" 2>"$serr"; local rc=$?
  local sh=$(sha256sum "$sout" | cut -d' ' -f1)
  local eh=$(sha256sum "$serr" | cut -d' ' -f1)
  log "$name" "$rc" "$sh" "$cmd"
  log "$name.stderr" "$rc" "$eh" "(stderr bytes: $(wc -c <"$serr"))"
  rm -f "$sout" "$serr"
}
run A1-cred-scan-claims "grep -n -iE 'set-cookie|cookie:|session[_-]?id|bearer|authorization:|api[_-]?key|private key|op://|ghp_|github_pat_|AKIA[0-9A-Z]{16}|xox[baprs]-' $LANE/plans/round-52-claims.md"
run A2-cred-scan-wavedir "grep -rn -iE 'set-cookie|cookie:|session[_-]?id|bearer|authorization:|api[_-]?key|private key|op://|ghp_|github_pat_|AKIA[0-9A-Z]{16}|xox[baprs]-' $LANE/.ufo/waves/round-52/"
run A3-url-credentials "grep -rn -E 'https?://[^/[:space:]@]+:[^/[:space:]@]+@' $LANE/plans/round-52-claims.md $LANE/.ufo/waves/round-52/ $LANE/tools/round-50/carriers.json"
run A4-private-key-blocks "grep -rn -E 'BEGIN (RSA |EC |OPENSSH |PGP |DSA )?PRIVATE KEY' $LANE/plans/round-52-claims.md $LANE/.ufo/waves/round-52/"
run A5-op-vault-refs "grep -rn 'op://' $LANE/plans/round-52-claims.md $LANE/.ufo/waves/round-52/"
run A6-round50-c1-files-over-1MiB "git -C $LANE ls-tree -r -l ab0eafedc41402b43b41a4362084119578dfe7ce -- corpus/evidence/round-50/c1/ | awk '\$4>1048576'"
run A7-round50-c1-file-types "file -b $LANE/corpus/evidence/round-50/c1/*/after.json $LANE/corpus/evidence/round-50/c1/*/run.json"
run A8-lane-files-over-1MiB "git -C $LANE ls-tree -r -l ab0eafedc41402b43b41a4362084119578dfe7ce | awk '\$4>1048576 {print \$4\"\\t\"\$5}' | sort -rn"
run A9-vendor-sha-pins-in-tree "python3 - <<'PYEOF'
import subprocess,hashlib
known={'42f1dea02e80cd8543250e08c23498b77a7ba3e445d71b62f2e280e93db6b779':'image g7581','468f8f4a61e542986bb8e361837efc763dd7c3ba03bb52ebbc42739221bc6659':'image g7582','f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d':'image c6490','52e3687d7363301453aa4fe0c712126874c90d3c138dee0792213dab11f5d815':'image c6430','f4437608dc0c3d1b0d910208bcbd4483346596821b700586c435fd63cd2427f5':'member g7581','556ef5a52aee449f40ac34c3445c51dfe994b90de081b2ca56415d8c8b8f6d4b':'member g7582','7ea4c628def17c25dc05f6103f8563884022dd1a5baf0c4fba38a85b546a0419':'member c6490','25194a87e54f98d868c614cef4ef8509c3e8f34bd6498bc03cdc3e7dcdd4934c':'member c6430','968d997d5401a483a9250ab0e4e34bd632a40bee000af3419a2b8d0e29fa6845':'carrier g7581','a119b64428e7128e376317472c504605f17f81a2b802439e32194431d94a5bd0':'carrier g7582','880370e7f7e15d70b165a96ae3e6efef0cb8dc3e9a6b27b0b925c7fa62caf2d7':'carrier c6490','da1c804940f49fcfb3727efbd4f79a4788f86c5819ddda23b5a8221fb898b46f':'carrier c6430'}
p=subprocess.run(['git','-C','$LANE','cat-file','--batch-all-objects','--batch-check=%(objectname) %(objecttype) %(objectsize)'],capture_output=True,text=True)
blobs=[l.split() for l in p.stdout.splitlines() if l.endswith('blob')]
hits=[];n=0
for r in blobs:
    sha,size=r[0],int(r[2])
    if size==0: continue
    d=subprocess.run(['git','-C','$LANE','cat-file','blob',sha],capture_output=True).stdout
    n+=1
    h=hashlib.sha256(d).hexdigest()
    if h in known: hits.append((sha,size,known[h]))
print('blobs_hashed',n,'hits',len(hits))
for x in hits: print('HIT',x)
PYEOF"
run A10-vendor-sha-pins-worktree "python3 - <<'PYEOF'
import os,hashlib
known={'42f1dea02e80cd8543250e08c23498b77a7ba3e445d71b62f2e280e93db6b779':'image g7581','468f8f4a61e542986bb8e361837efc763dd7c3ba03bb52ebbc42739221bc6659':'image g7582','f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d':'image c6490','52e3687d7363301453aa4fe0c712126874c90d3c138dee0792213dab11f5d815':'image c6430','f4437608dc0c3d1b0d910208bcbd4483346596821b700586c435fd63cd2427f5':'member g7581','556ef5a52aee449f40ac34c3445c51dfe994b90de081b2ca56415d8c8b8f6d4b':'member g7582','7ea4c628def17c25dc05f6103f8563884022dd1a5baf0c4fba38a85b546a0419':'member c6490','25194a87e54f98d868c614cef4ef8509c3e8f34bd6498bc03cdc3e7dcdd4934c':'member c6430','968d997d5401a483a9250ab0e4e34bd632a40bee000af3419a2b8d0e29fa6845':'carrier g7581','a119b64428e7128e376317472c504605f17f81a2b802439e32194431d94a5bd0':'carrier g7582','880370e7f7e15d70b165a96ae3e6efef0cb8dc3e9a6b27b0b925c7fa62caf2d7':'carrier c6490','da1c804940f49fcfb3727efbd4f79a4788f86c5819ddda23b5a8221fb898b46f':'carrier c6430'}
hits=[];n=0
for root,dirs,files in os.walk('$LANE'):
    dirs[:]=[d for d in dirs if d not in ('.git','.jj')]
    for f in files:
        p=os.path.join(root,f)
        try: st=os.stat(p)
        except OSError: continue
        if st.st_size>200*1024*1024: continue
        try:
            h=hashlib.sha256()
            with open(p,'rb') as fh:
                for c in iter(lambda: fh.read(1<<20), b''): h.update(c)
            d=h.hexdigest()
        except OSError: continue
        n+=1
        if d in known: hits.append((p,st.st_size,known[d]))
print('files_hashed',n,'hits',len(hits))
for x in hits: print('HIT',x)
PYEOF"
run A11-history-unredacted-cookies "python3 - <<'PYEOF'
import subprocess,re
pat=re.compile(rb'set-cookie:\s*([A-Za-z0-9_]+)=([^;\r\n]{8,})')
p=subprocess.run(['git','-C','$LANE','cat-file','--batch-all-objects','--batch-check=%(objectname) %(objecttype)'],capture_output=True,text=True)
blobs=[l.split()[0] for l in p.stdout.splitlines() if l.endswith('blob')]
hits=[]
for b in blobs:
    d=subprocess.run(['git','-C','$LANE','cat-file','blob',b],capture_output=True).stdout
    for m in pat.finditer(d):
        v=m.group(2)
        if b'redact' in v.lower(): continue
        hits.append((b,m.group(1).decode(),len(v)))
seen=set()
for h in hits:
    if h[0] in seen: continue
    seen.add(h[0]); print('BLOB',h[0],h[1],'len',h[2])
print('total_hits',len(hits),'distinct_blobs',len(seen))
PYEOF"
run A12-origin-main-cookie-tip "git -C $LANE show origin/main:.ufo/waves/round-49/w1/C1CarrierPins/receipts/tree.hdr | grep -c 'redacted'"
run A13-lane-guard-in-fetcher "grep -n 'is inside the lane' $LANE/tools/round-50/fetch-vendor.py $LANE/.ufo/waves/round-52/w1/ExecFetchVendor/fetch-vendor.py"
run A14-carrier-cache-absent "ls /fast/scratch/hyaku/kaidoku-r50/carrier-cache/"
