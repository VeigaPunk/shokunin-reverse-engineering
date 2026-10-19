#!/usr/bin/env bash
# RV-13 replay v2 — one isolated case per directory, fresh receipt per case, so a
# tamper in one case cannot contaminate the next.  Every path is a /var/tmp
# stand-in; the 5 real custody paths are never passed to the tool.
set -u
TOOL=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py
R=/var/tmp/rv13/replay2
SUM=/var/tmp/rv13/replay2-summary.txt
rm -rf "$R"; mkdir -p "$R"
: > "$SUM"
echo "# RV-13 replay of the attack demo vs EX-31 instrument" >> "$SUM"
echo "# tool: $TOOL" >> "$SUM"
echo "# tool sha256 (this run): $(sha256sum "$TOOL" | cut -d' ' -f1)" >> "$SUM"
echo "# date: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> "$SUM"
echo "# columns: case | class | exit | moved-fields | sha256-equal" >> "$SUM"

mkcase() {  # $1 = case name -> prints dir
  local D="$R/$1"; mkdir -p "$D"
  printf 'stand\n' > "$D/subject.conf"; head -c 4100 /dev/urandom >> "$D/subject.conf"
  python3 "$TOOL" capture --out "$D/pre.receipt" --label "$1" --paths "$D/subject.conf" >/dev/null 2>&1
  echo "$D"
}

runcase() {  # $1 = case name, $2 = dir
  local D="$2"
  local out rc cls moved pre_sha post_sha
  out=$(python3 "$TOOL" verify "$D/pre.receipt" --live 2>&1); rc=$?
  cls=$(printf '%s' "$out" | grep -o 'PATH [^:]*: [A-Z-]*' | head -1 | awk '{print $3}')
  moved=$(printf '%s' "$out" | grep -o 'moved=[a-z_,]*' | head -1 || true)
  pre_sha=$(grep -m1 '^SHA256:' "$D/pre.receipt" | awk '{print $2}')
  post_sha=$(sha256sum "$D/subject.conf" | cut -d' ' -f1)
  printf '%s\n' "$out" > "$D/verify.out"
  printf '%-42s | %-15s | %-4s | %-28s | %s\n' "$1" "${cls:-none}" "$rc" "${moved:-none}" \
    "$([ "$pre_sha" = "$post_sha" ] && echo same || echo DIFFERENT)" | tee -a "$SUM"
}

# --- case 1: untouched control (must MATCH, exit 0)
D=$(mkcase c1-untouched);                    runcase c1-untouched "$D"

# --- case 2: in-place same-content rewrite, mtime restored ns-exact (attack 3)
D=$(mkcase c2-inplace-same-ct-restored)
python3 - "$D/subject.conf" <<'PY'
import os,sys
p=sys.argv[1]; st=os.stat(p); data=open(p,'rb').read()
open(p,'r+b').write(data); os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns))
PY
runcase c2-inplace-same-ct-restored "$D"

# --- case 3: read-only access (atime perturbation) on an UNTOUCHED file
D=$(mkcase c3-atime-only)
cat "$D/subject.conf" > /dev/null
runcase c3-atime-only "$D"

# --- case 4: no-op chmod (mode already 644)
D=$(mkcase c4-noop-chmod)
chmod 644 "$D/subject.conf"
runcase c4-noop-chmod "$D"

# --- case 5: replace by new file, same content, mtime restored (inode moves)
D=$(mkcase c5-replace-new-inode)
cp "$D/subject.conf" "$D/subject.new"; touch -r "$D/subject.conf" "$D/subject.new"
mv -f "$D/subject.new" "$D/subject.conf"
runcase c5-replace-new-inode "$D"

# --- case 6: content change (1 byte), mtime restored
D=$(mkcase c6-content-change)
PRE=$(stat -c %Y "$D/subject.conf"); printf 'X' >> "$D/subject.conf"; touch -d "@$PRE" "$D/subject.conf"
runcase c6-content-change "$D"

# --- case 7: same-second control — tamper the SAME second as the pre-receipt
#     (proves the tool's ns fields, not epoch fields, carry the detection)
D=$(mkcase c7-same-second)
python3 - "$D" <<'PY'
import os,subprocess,sys,time
d=sys.argv[1]; p=os.path.join(d,'subject.conf')
# recapture the receipt in the same second as the rewrite
st=os.stat(p); data=open(p,'rb').read()
subprocess.run(['python3','/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py',
                'capture','--out',os.path.join(d,'pre.receipt'),'--label','c7','--paths',p],
               check=True, capture_output=True)
pre_epoch=int(os.stat(p).st_ctime)
open(p,'r+b').write(data); os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns))
post_epoch=int(os.stat(p).st_ctime)
print("SAME-SECOND:", pre_epoch==post_epoch, "pre_ctime_epoch=%d post_ctime_epoch=%d"%(pre_epoch,post_epoch))
open(os.path.join(d,'same-second.txt'),'w').write("pre_ctime_epoch=%d post_ctime_epoch=%d same_second=%s\n"%(pre_epoch,post_epoch,pre_epoch==post_epoch))
PY
cat "$D/same-second.txt" | tee -a "$SUM"
runcase c7-same-second "$D"

echo >> "$SUM"
echo "# tool sha256 (post-run): $(sha256sum "$TOOL" | cut -d' ' -f1)" >> "$SUM"
tail -3 "$SUM"
