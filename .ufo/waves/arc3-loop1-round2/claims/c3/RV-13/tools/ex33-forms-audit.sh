#!/usr/bin/env bash
# RV-13 audit of EX-33's attack matrix: recompute the COMPLETE moved-field set for
# each rewrite form with an independent capturer, next to the tool's own reported
# moved= list.  All fixtures under /var/tmp; real tool is read/exec only.
set -u
TOOL=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py
PROTO=/var/tmp/rv13/custody_v2_proto.py
R=/var/tmp/rv13/ex33-audit
OUT=$R/audit-table.txt
rm -rf "$R"; mkdir -p "$R"; : > "$OUT"
TOOLSHA=$(sha256sum "$TOOL" | cut -d' ' -f1)
echo "# RV-13 audit of EX-33 rewrite forms — tool sha256=$TOOLSHA" >> "$OUT"
echo "# date: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> "$OUT"
echo "# 'complete' = full field diff from the independent capturer (ALL moved fields)" >> "$OUT"
echo "# 'tool'     = what custody-pair verify printed as moved= (first-matching branch)" >> "$OUT"
echo >> "$OUT"

form() {  # $1 = label, $2 = mutation shell snippet (uses $F)
  local L="$1" MUT="$2" D="$R/$1" F
  mkdir -p "$D"; F="$D/victim.conf"
  printf 'attack fixture body\n' > "$F"; touch -d @1700000000 "$F"
  # pre captures (tool + independent)
  python3 "$TOOL"  capture --out "$D/pre.tool.txt" --paths "$F" --label "$L" >/dev/null 2>&1
  python3 "$PROTO" emit "$F" > "$D/pre.proto.txt"
  ( F="$F"; eval "$MUT" ) > "$D/mutation.txt" 2>&1
  python3 "$TOOL" verify "$D/pre.tool.txt" --live > "$D/verify.out" 2>&1; local rc=$?
  local tmove; tmove=$(grep -o 'moved=[a-z0-9_,]*' "$D/verify.out" | head -1 | cut -d= -f2)
  local tcls; tcls=$(grep -oP 'PATH \S+: \K[A-Z-]+' "$D/verify.out" | head -1)
  # complete diff from the independent capturer
  local rec; rec=$(python3 - "$D/pre.proto.txt" "$F" <<'PY'
import importlib.util,sys
spec=importlib.util.spec_from_file_location("p","/var/tmp/rv13/custody_v2_proto.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
pre=m.parse(open(sys.argv[1]).read()); path=list(pre)[0]
now=m.capture(path)
moved=[f for f in m.FIELD_ORDER if str(pre[path].get(f.upper(),pre[path].get(f)))!=str(now[f])]
print(",".join(moved) or "-")
PY
)
  printf '%-26s | tool: %-14s exit=%-3s moved=%-24s | complete: %s\n' \
    "$L" "$tcls" "$rc" "${tmove:-none}" "$rec" >> "$OUT"
}

form "F-b-inplace"        'python3 /var/tmp/rv13/mut-inplace.py "$F"'
form "F-b2-inplace-forged" 'python3 /var/tmp/rv13/mut-inplace-forged.py "$F"'
form "F-c-rename-forged"   'cp -p "$F" "$F.new"; touch -d @1700000000 "$F.new"; mv -f "$F.new" "$F"'
form "F-c2-hardlink-swap"  'cp -p "$F" "$F.other"; touch -d @1700000000 "$F.other"; ln -f "$F.other" "$F"'
form "F-e-delete-recreate" 'rm -f "$F"; printf "attack fixture body\n" > "$F"; touch -d @1700000000 "$F"'
form "F-g-content-change"  'printf "x" >> "$F"'
form "F-k-chmod-only"      'chmod 600 "$F"'

# F-d same-second: capture and rewrite provably within one whole second
D="$R/F-d-same-second"; mkdir -p "$D"; F="$D/victim.conf"
python3 - "$TOOL" "$PROTO" "$D" <<'PY'
import importlib.util,os,subprocess,sys,time
tool,proto,d=sys.argv[1],sys.argv[2],sys.argv[3]
f=os.path.join(d,'victim.conf')
open(f,'wb').write(b'attack fixture body\n'); os.utime(f,(1700000000,1700000000))
# wait for a fresh second, then capture + rewrite inside it
now=time.time(); time.sleep(max(0.0, int(now)+1-time.time())+0.01)
subprocess.run(['python3',tool,'capture','--out',os.path.join(d,'pre.tool.txt'),'--paths',f],check=True,capture_output=True)
spec=importlib.util.spec_from_file_location('p',proto); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
pre=m.capture(f)
open(os.path.join(d,'pre.proto.txt'),'w').write(open(proto).read()[:0])  # placeholder
import json; json.dump(pre, open(os.path.join(d,'pre.proto.json'),'w'))
st=os.stat(f); data=open(f,'rb').read()
open(f,'r+b').write(data); os.utime(f,ns=(st.st_atime_ns,st.st_mtime_ns))
post=m.capture(f)
moved=[k for k in m.FIELD_ORDER if str(pre.get(k))!=str(post.get(k))]
print('SAME-SECOND pre_ctime_epoch=%d post_ctime_epoch=%d same=%s complete_moved=%s' % (
    pre['ctime_epoch'], post['ctime_epoch'], pre['ctime_epoch']==post['ctime_epoch'], ','.join(moved) or '-'))
PY
python3 "$TOOL" verify "$D/pre.tool.txt" --live > "$D/verify.out" 2>&1; rc=$?
tmove=$(grep -o 'moved=[a-z0-9_,]*' "$D/verify.out" | head -1 | cut -d= -f2)
tcls=$(grep -oP 'PATH \S+: \K[A-Z-]+' "$D/verify.out" | head -1)
{ printf '%-26s | tool: %-14s exit=%-3s moved=%-24s | complete: (see verify.out; see pre.proto.json)\n' \
   "F-d-same-second" "$tcls" "$rc" "${tmove:-none}"; } >> "$OUT"

cat "$OUT"
