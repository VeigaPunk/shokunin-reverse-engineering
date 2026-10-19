#!/usr/bin/env bash
# EX-33 round 2 — same-content-rewrite attack against the REAL v2 tool.
# Tool: .ufo/gates/custody-pair/custody-pair.py (EX-31's committed target; read/exec only).
# All fixtures scratch under /var/tmp. No custody path touched.
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
T=$REPO/.ufo/gates/custody-pair/custody-pair.py
S=/var/tmp/arc3-l1r2-EX-33
A=$S/real; rm -rf "$A"; mkdir -p "$A"
PAYLOAD="CUSTODY-PAYLOAD-v2-test"; FIXED_MTIME=1792000000
run(){ echo; echo "### $*"; }
sha(){ sha256sum "$1" | cut -d' ' -f1; }
stt(){ stat -c 'inode=%i size=%s mtime=%s ctime=%s' "$1"; }
cap(){ python3 "$T" capture --out "$2" --label "$3" --paths "$1"; }

run "R-A control: capture + verify --live (expect MATCH exit 0)"
mkdir -p "$A/A"; printf '%s\n' "$PAYLOAD" > "$A/A/a.bin"; touch -d @$FIXED_MTIME "$A/A/a.bin"
cap "$A/A/a.bin" "$A/A/a.v2.json" ex33-A | tail -1
python3 "$T" verify "$A/A/a.v2.json" --live | tee "$A/A/verify.txt" | tail -3; echo "exit=${PIPESTATUS[0]}"

run "R-B in-place identical rewrite (same inode; sha unchanged)"
mkdir -p "$A/B"; printf '%s\n' "$PAYLOAD" > "$A/B/b.bin"; touch -d @$FIXED_MTIME "$A/B/b.bin"
cap "$A/B/b.bin" "$A/B/b.v2.json" ex33-B | tail -1
b_sha1=$(sha "$A/B/b.bin"); stt "$A/B/b.bin" > "$A/B/stat-before"
python3 - "$A/B/b.bin" "$PAYLOAD" <<'PY'
import sys; open(sys.argv[1], "wb").write((sys.argv[2] + "\n").encode())
PY
b_sha2=$(sha "$A/B/b.bin"); stt "$A/B/b.bin" > "$A/B/stat-after"
echo "sha-before=$b_sha1"; echo "sha-after =$b_sha2  sha256-alone=$([ "$b_sha1" = "$b_sha2" ] && echo silent || echo DRIFT)"
diff -u "$A/B/stat-before" "$A/B/stat-after" || true
python3 "$T" verify "$A/B/b.v2.json" --live | tee "$A/B/verify.txt" | tail -3; echo "exit=${PIPESTATUS[0]}"

run "R-B2 in-place identical rewrite + forged mtime back"
mkdir -p "$A/B2"; printf '%s\n' "$PAYLOAD" > "$A/B2/b2.bin"; touch -d @$FIXED_MTIME "$A/B2/b2.bin"
cap "$A/B2/b2.bin" "$A/B2/b2.v2.json" ex33-B2 | tail -1
python3 - "$A/B2/b2.bin" "$PAYLOAD" <<'PY'
import sys; open(sys.argv[1], "wb").write((sys.argv[2] + "\n").encode())
PY
touch -d @$FIXED_MTIME "$A/B2/b2.bin"
stt "$A/B2/b2.bin"
python3 "$T" verify "$A/B2/b2.v2.json" --live | tee "$A/B2/verify.txt" | tail -3; echo "exit=${PIPESTATUS[0]}"

run "R-C rename-over identical bytes + forged mtime (new inode)"
mkdir -p "$A/C"; printf '%s\n' "$PAYLOAD" > "$A/C/c.bin"; touch -d @$FIXED_MTIME "$A/C/c.bin"
cap "$A/C/c.bin" "$A/C/c.v2.json" ex33-C | tail -1
printf '%s\n' "$PAYLOAD" > "$A/C/c.new"; touch -d @$FIXED_MTIME "$A/C/c.new"
mv -f "$A/C/c.new" "$A/C/c.bin"
stt "$A/C/c.bin"
python3 "$T" verify "$A/C/c.v2.json" --live | tee "$A/C/verify.txt" | tail -3; echo "exit=${PIPESTATUS[0]}"

run "R-C2 hardlink force (ln -f) of identical-content file"
mkdir -p "$A/C2"; printf '%s\n' "$PAYLOAD" > "$A/C2/c2.bin"; touch -d @$FIXED_MTIME "$A/C2/c2.bin"
cap "$A/C2/c2.bin" "$A/C2/c2.v2.json" ex33-C2 | tail -1
printf '%s\n' "$PAYLOAD" > "$A/C2/other.bin"; touch -d @$FIXED_MTIME "$A/C2/other.bin"
ln -f "$A/C2/other.bin" "$A/C2/c2.bin"
echo "inode=$(stat -c '%i' "$A/C2/c2.bin") links=$(stat -c '%h' "$A/C2/c2.bin")"
python3 "$T" verify "$A/C2/c2.v2.json" --live | tee "$A/C2/verify.txt" | tail -3; echo "exit=${PIPESTATUS[0]}"

run "R-E delete + recreate identical bytes + forged mtime"
mkdir -p "$A/E"; printf '%s\n' "$PAYLOAD" > "$A/E/e.bin"; touch -d @$FIXED_MTIME "$A/E/e.bin"
cap "$A/E/e.bin" "$A/E/e.v2.json" ex33-E | tail -1
rm -f "$A/E/e.bin"
printf '%s\n' "$PAYLOAD" > "$A/E/e.bin"; touch -d @$FIXED_MTIME "$A/E/e.bin"
stt "$A/E/e.bin"
python3 "$T" verify "$A/E/e.v2.json" --live | tee "$A/E/verify.txt" | tail -3; echo "exit=${PIPESTATUS[0]}"

run "R-G different-bytes rewrite (sha256 must fire)"
mkdir -p "$A/G"; printf '%s\n' "$PAYLOAD" > "$A/G/g.bin"; touch -d @$FIXED_MTIME "$A/G/g.bin"
cap "$A/G/g.bin" "$A/G/g.v2.json" ex33-G | tail -1
printf 'TAMPERED\n' > "$A/G/g.bin"; touch -d @$FIXED_MTIME "$A/G/g.bin"
python3 "$T" verify "$A/G/g.v2.json" --live | tee "$A/G/verify.txt" | tail -3; echo "exit=${PIPESTATUS[0]}"

run "R-H receipt-to-receipt: pre/post pair over an identical rewrite"
mkdir -p "$A/H"; printf '%s\n' "$PAYLOAD" > "$A/H/h.bin"; touch -d @$FIXED_MTIME "$A/H/h.bin"
cap "$A/H/h.bin" "$A/H/h-pre.v2.json" ex33-H-pre | tail -1
python3 - "$A/H/h.bin" "$PAYLOAD" <<'PY'
import sys; open(sys.argv[1], "wb").write((sys.argv[2] + "\n").encode())
PY
touch -d @$FIXED_MTIME "$A/H/h.bin"
cap "$A/H/h.bin" "$A/H/h-post.v2.json" ex33-H-post | tail -1
python3 "$T" verify "$A/H/h-pre.v2.json" "$A/H/h-post.v2.json" | tee "$A/H/verify.txt" | tail -3; echo "exit=${PIPESTATUS[0]}"

run "R-I absent path (delete after capture) — expect ABSENT exit 13"
mkdir -p "$A/I"; printf '%s\n' "$PAYLOAD" > "$A/I/i.bin"
cap "$A/I/i.bin" "$A/I/i.v2.json" ex33-I | tail -1
rm -f "$A/I/i.bin"
python3 "$T" verify "$A/I/i.v2.json" --live | tee "$A/I/verify.txt" | tail -3; echo "exit=${PIPESTATUS[0]}"

run "R-D same-second in-place rewrite + forged mtime (ns-precision probe)"
python3 "$S/same_second_real.py"; echo "exit=$?"

echo; echo "### real-tool ladder complete $(date -u +%FT%TZ)"
