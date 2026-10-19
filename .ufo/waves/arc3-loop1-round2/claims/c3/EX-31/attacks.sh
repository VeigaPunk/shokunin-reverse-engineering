#!/usr/bin/env bash
# EX-31 attack harness — custody-pair v2 comparator (wave arc3-loop1-round2, chain c3).
#
# Every attack runs on SCRATCH FIXTURES under the given scratch dir. No custody
# path is read beyond hash/stat, and no custody path is written.
# usage: attacks.sh <tool-path> <scratch-dir>
set -u
TOOL="$1"
SCRATCH="$2"
mkdir -p "$SCRATCH"

FIX="$SCRATCH/victim.conf"
printf 'attack fixture body\n' > "$FIX"
touch -d @1700000000 "$FIX"

banner() { printf '\n===== %s =====\n' "$1"; }

banner "A1 same-content rewrite IN PLACE, mtime restored (round-1 attack 3, ctime pin)"
"$TOOL" capture --out "$SCRATCH/a1-pre.txt" --paths "$FIX" --label A1-pre >/dev/null
python3 - "$FIX" <<'PY'
import os, sys
p = sys.argv[1]
st = os.lstat(p)
data = open(p, "rb").read()
with open(p, "wb") as fh:
    fh.write(data)
os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns))
after = os.lstat(p)
print("rewrote %d bytes in place: inode %d->%d (same=%s) mtime_ns %d->%d (restored=%s) ctime_ns %d->%d (moved=%s)"
      % (len(data), st.st_ino, after.st_ino, st.st_ino == after.st_ino,
         st.st_mtime_ns, after.st_mtime_ns, st.st_mtime_ns == after.st_mtime_ns,
         st.st_ctime_ns, after.st_ctime_ns, st.st_ctime_ns != after.st_ctime_ns))
PY
"$TOOL" verify "$SCRATCH/a1-pre.txt" --live
echo "A1 exit=$?"

banner "A2 same-content rewrite via TEMP+RENAME (inode pin)"
"$TOOL" capture --out "$SCRATCH/a2-pre.txt" --paths "$FIX" --label A2-pre >/dev/null
TMP="$SCRATCH/victim.conf.new"
cp "$FIX" "$TMP" 2>/dev/null || printf 'attack fixture body\n' > "$TMP"
touch -d @1700000000 "$TMP"
mv -f "$TMP" "$FIX"
printf 'inode after rename: %s\n' "$(stat -c %i "$FIX")"
"$TOOL" verify "$SCRATCH/a2-pre.txt" --live
echo "A2 exit=$?"

banner "A3 content drift (one byte appended)"
printf 'x' >> "$FIX"
"$TOOL" verify "$SCRATCH/a2-pre.txt" --live
echo "A3 exit=$?"

banner "A4 absent path"
rm -f "$FIX"
"$TOOL" verify "$SCRATCH/a2-pre.txt" --live
echo "A4 exit=$?"

banner "A5 receipt mutation on a copy of the ROUND receipt (vacuous-comparator check)"
REAL="$3"
if [ -n "$REAL" ] && [ -f "$REAL" ]; then
  MUT="$SCRATCH/a5-mutated.txt"
  # flip the last hex digit of the first SHA256 field of a copy of the real receipt
  python3 - "$REAL" "$MUT" <<'PY'
import re, sys
src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
m = re.search(r"^SHA256:\s*([0-9a-f]{64})\s*$", text, re.M)
old = m.group(1)
new = old[:-1] + ("0" if old[-1] != "0" else "1")
open(dst, "w", encoding="utf-8").write(text.replace(old, new, 1))
print("mutated first SHA256 %s -> %s" % (old, new))
PY
  "$TOOL" verify "$MUT" --live
  echo "A5 exit=$?"
else
  echo "skipped: no receipt passed as argument 3"
fi

banner "A6 v1 sums receipt with one mutated digest (v1-compat vacuity check)"
SUM="$SCRATCH/a6-sums.txt"
python3 - "$SUM" <<'PY'
import hashlib, sys
path = sys.argv[1]
body = b"v1 fixture\n"
open("/dev/shm/.a6-fixture", "wb").write(body)
digest = hashlib.sha256(body).hexdigest()
bad = digest[:-1] + ("0" if digest[-1] != "0" else "1")
open(path, "w").write(bad + "  /dev/shm/.a6-fixture\n")
print("v1 sums entry: %s (mutated from %s)" % (bad, digest))
PY
"$TOOL" verify "$SUM" --live
echo "A6 exit=$?"

echo
echo "ATTACK-HARNESS: done (fixtures: $SCRATCH)"
