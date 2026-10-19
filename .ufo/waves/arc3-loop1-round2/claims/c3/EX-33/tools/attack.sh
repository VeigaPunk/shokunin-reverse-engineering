#!/usr/bin/env bash
# EX-33 attack ladder — same-content rewrite vs sha256-only (v1-style) and v2 receipt.
# Scratch only (/var/tmp/arc3-l1r2-EX-33). No custody path touched.
set -u
S=/var/tmp/arc3-l1r2-EX-33
A=$S/attack
V=$S/v2ref.py
rm -rf "$A"; mkdir -p "$A"
PAYLOAD="CUSTODY-PAYLOAD-v2-test"; FIXED_MTIME=1792000000

say(){ echo; echo "### $*"; }
sha(){ sha256sum "$1" | cut -d' ' -f1; }
stt(){ stat -c 'inode=%i size=%s mtime=%Y(%y) ctime=%Z(%z)' "$1"; }

# ---------- A: control (no change) ----------
say "A. control: create + capture + verify, no rewrite"
mkdir -p "$A/A"; printf '%s\n' "$PAYLOAD" > "$A/A/a.bin"
touch -d @$FIXED_MTIME "$A/A/a.bin"
python3 "$V" capture "$A/A/a.v2rec" "$A/A/a.bin"
echo "sha-before=$(sha "$A/A/a.bin")"; stt "$A/A/a.bin"
python3 "$V" verify "$A/A/a.v2rec" "$A/A/a.bin"; echo "exit=$?"

# ---------- B: in-place identical rewrite (same inode) ----------
say "B. in-place identical rewrite (truncate+write, same inode)"
mkdir -p "$A/B"; printf '%s\n' "$PAYLOAD" > "$A/B/b.bin"
touch -d @$FIXED_MTIME "$A/B/b.bin"
python3 "$V" capture "$A/B/b.v2rec" "$A/B/b.bin"
sha_b=$(sha "$A/B/b.bin"); echo "sha-before=$sha_b"; stt "$A/B/b.bin" > "$A/B/b.stat-before"
python3 - "$A/B/b.bin" "$PAYLOAD" <<'PY'
import sys
open(sys.argv[1], "wb").write((sys.argv[2] + "\n").encode())
PY
sha_a=$(sha "$A/B/b.bin"); echo "sha-after=$sha_a  sha256-alone=$([ "$sha_b" = "$sha_a" ] && echo silent || echo DRIFT)"
stt "$A/B/b.bin" > "$A/B/b.stat-after"
diff -u "$A/B/b.stat-before" "$A/B/b.stat-after" || true
python3 "$V" verify "$A/B/b.v2rec" "$A/B/b.bin"; echo "exit=$?"

# ---------- B2: in-place rewrite + forged mtime back ----------
say "B2. in-place identical rewrite + forged mtime (touch -d @old) — ctime is the residue"
mkdir -p "$A/B2"; printf '%s\n' "$PAYLOAD" > "$A/B2/b2.bin"
touch -d @$FIXED_MTIME "$A/B2/b2.bin"
python3 "$V" capture "$A/B2/b2.v2rec" "$A/B2/b2.bin"
python3 - "$A/B2/b2.bin" "$PAYLOAD" <<'PY'
import sys
open(sys.argv[1], "wb").write((sys.argv[2] + "\n").encode())
PY
touch -d @$FIXED_MTIME "$A/B2/b2.bin"   # attacker forges mtime back
stt "$A/B2/b2.bin"
python3 "$V" verify "$A/B2/b2.v2rec" "$A/B2/b2.bin"; echo "exit=$?"

# ---------- C: rename-over (new inode) ----------
say "C. rename-over identical bytes, mtime forged to recorded value (new inode)"
mkdir -p "$A/C"; printf '%s\n' "$PAYLOAD" > "$A/C/c.bin"
touch -d @$FIXED_MTIME "$A/C/c.bin"
python3 "$V" capture "$A/C/c.v2rec" "$A/C/c.bin"
printf '%s\n' "$PAYLOAD" > "$A/C/c.new"
touch -d @$FIXED_MTIME "$A/C/c.new"
mv -f "$A/C/c.new" "$A/C/c.bin"
stt "$A/C/c.bin"
python3 "$V" verify "$A/C/c.v2rec" "$A/C/c.bin"; echo "exit=$?"

# ---------- C2: hardlink-force identical bytes (same-fs link swap) ----------
say "C2. ln -f of an identical-content file over the path"
mkdir -p "$A/C2"; printf '%s\n' "$PAYLOAD" > "$A/C2/c2.bin"
touch -d @$FIXED_MTIME "$A/C2/c2.bin"
python3 "$V" capture "$A/C2/c2.v2rec" "$A/C2/c2.bin"
printf '%s\n' "$PAYLOAD" > "$A/C2/other.bin"; touch -d @$FIXED_MTIME "$A/C2/other.bin"
ln -f "$A/C2/other.bin" "$A/C2/c2.bin"
echo "c2 now shares inode with other.bin: $(stat -c '%i' "$A/C2/c2.bin") / $(stat -c '%i' "$A/C2/other.bin")  links=$(stat -c '%h' "$A/C2/c2.bin")"
python3 "$V" verify "$A/C2/c2.v2rec" "$A/C2/c2.bin"; echo "exit=$?"

# ---------- E: delete + recreate (inode-reuse probe) ----------
say "E. delete+recreate identical bytes+mtime; inode-reuse probe (200 spawns)"
mkdir -p "$A/E"; printf '%s\n' "$PAYLOAD" > "$A/E/e.bin"
touch -d @$FIXED_MTIME "$A/E/e.bin"
python3 "$V" capture "$A/E/e.v2rec" "$A/E/e.bin"
i0=$(stat -c '%i' "$A/E/e.bin"); echo "inode-before=$i0"
rm -f "$A/E/e.bin"
printf '%s\n' "$PAYLOAD" > "$A/E/e.bin"; touch -d @$FIXED_MTIME "$A/E/e.bin"
i1=$(stat -c '%i' "$A/E/e.bin"); echo "inode-after=$i1 reused=$([ "$i0" = "$i1" ] && echo yes || echo no)"
: > "$A/E/reuse-scan.txt"
for n in $(seq 1 200); do printf 'x' > "$A/E/tmp$n"; stat -c '%i' "$A/E/tmp$n" >> "$A/E/reuse-scan.txt"; done
echo "reuse-scan hits for $i0: $(grep -cx "$i0" "$A/E/reuse-scan.txt") / 200 spawned inodes"
rm -f "$A/E"/tmp*
python3 "$V" verify "$A/E/e.v2rec" "$A/E/e.bin"; echo "exit=$?"

# ---------- D: same-second boundary (second-granularity vs nanosecond) ----------
say "D. same-second in-place rewrite, mtime forged: --sec receipt vs ns receipt"
python3 "$S/same_second.py"; echo "exit=$?"

# ---------- G: content change control (sha256 must fire) ----------
say "G. different-bytes rewrite (sha256 must fire too)"
mkdir -p "$A/G"; printf '%s\n' "$PAYLOAD" > "$A/G/g.bin"
touch -d @$FIXED_MTIME "$A/G/g.bin"
python3 "$V" capture "$A/G/g.v2rec" "$A/G/g.bin"
printf 'TAMPERED\n' > "$A/G/g.bin"; touch -d @$FIXED_MTIME "$A/G/g.bin"
python3 "$V" verify "$A/G/g.v2rec" "$A/G/g.bin"; echo "exit=$?"

echo; echo "### ladder complete $(date -u +%FT%TZ)"
