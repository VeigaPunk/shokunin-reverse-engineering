#!/usr/bin/env bash
# CANONICAL bounded probe for R51-C2 grounding (ScoutMksquashfs).
# One input dir -> two tiny squashfs images (one -nopad, one padded) + one padded
# determinism control.  Every step records: exact command, exit code, stdout sha256, UTC.
# Nothing is written outside $S.
set -u
S=/fast/scratch/hyaku/kaidoku-r51/w1-ScoutMksquashfs
P="$S/canonical"
rm -rf "$P"; mkdir -p "$P/src/sub" "$P/run/pad" "$P/run/nopad" "$P/run/pad2"
LOG="$P/steps.log"
: > "$LOG"

step() {  # step <name> <cmd...>
  local name="$1"; shift
  local out="$P/$name.stdout" utc rc sha
  utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  "$@" > "$out" 2>"$P/$name.stderr"; rc=$?
  sha=$(sha256sum "$out" | cut -d' ' -f1)
  printf '%s\t%s\trc=%s\tstdout_sha256=%s\t%s\n' "$name" "$*" "$rc" "$sha" "$utc" >> "$LOG"
  printf '%s\n' "$rc" > "$P/$name.rc"
  return 0
}

# --- input tree (fixed mtimes so only the superblock mkfs_time varies) ---
printf 'hello\n' > "$P/src/a.txt"
printf 'world\n' > "$P/src/sub/b.txt"
touch -d '2020-01-01T00:00:00Z' "$P/src" "$P/src/a.txt" "$P/src/sub" "$P/src/sub/b.txt"

cd "$P" || exit 2
step mk_padded  mksquashfs src padded.sqfs  -noappend -no-progress -all-root
step mk_nopad   mksquashfs src nopad.sqfs   -noappend -no-progress -all-root -nopad
step mk_padded2 mksquashfs src padded2.sqfs -noappend -no-progress -all-root
# the rejected spelling: proves -no-pad is NOT an option
mkdir -p "$P/rej" && printf 'x\n' > "$P/rej/f.txt"
step mk_nopad_hyphen mksquashfs rej rej.sqfs -noappend -no-progress -all-root -no-pad

# --- readers, each in its own cwd so no extraction collides ---
step unsq_pad    unsquashfs -s padded.sqfs
step unsq_nopad  unsquashfs -s nopad.sqfs
step sasq_pad    sasquatch -d out padded.sqfs
step sasq_nopad  sasquatch -d out nopad.sqfs
rm -rf "$P/out"; mkdir -p "$P/out"

# --- superblock parse (bytes_used @ offset 40..47, LE64 for LE images) ---
step superblock python3 - "$P" <<'PY'
import struct, pathlib, sys
P = pathlib.Path(sys.argv[1])
for name in ("padded", "nopad", "padded2"):
    b = (P / f"{name}.sqfs").read_bytes()
    magic = b[0:4]
    fmt = "<" if magic == b"hsqs" else ">"
    (ino, mkfs, bsz, frag) = struct.unpack(fmt + "IIII", b[4:20])
    (comp, blog, flags, nids, smaj, smin) = struct.unpack(fmt + "HHHHHH", b[20:32])
    (root, used) = struct.unpack(fmt + "QQ", b[32:48])
    print(f"{name}: magic={magic!r} endian={fmt} inodes={ino} mkfs_time={mkfs} "
          f"block_size={bsz} s_major={smaj} s_minor={smin} bytes_used={used} "
          f"file_size={len(b)} file_size_mod4096={len(b) % 4096} "
          f"tail_bytes={len(b) - used} file_size_eq_bytes_used={len(b) == used}")
PY

# --- padding shape: is the padded image the nopad bytes + zero tail? ---
step padshape python3 - "$P" <<'PY'
import pathlib, sys
P = pathlib.Path(sys.argv[1])
pad = (P / "padded.sqfs").read_bytes()
nop = (P / "nopad.sqfs").read_bytes()
pad2 = (P / "padded2.sqfs").read_bytes()
n = len(nop)
print("nopad_len", n)
print("padded_len", len(pad))
print("byte_len_difference", len(pad) - n)
print("nopad_is_prefix_of_padded", pad[:n] == nop)
tail = pad[n:]
print("padded_tail_len", len(tail))
print("padded_tail_all_zero", set(tail) == {0})
print("padded2_equals_padded", pad2 == pad)
print("padded_sha256", __import__("hashlib").sha256(pad).hexdigest())
print("nopad_sha256", __import__("hashlib").sha256(nop).hexdigest())
print("padded2_sha256", __import__("hashlib").sha256(pad2).hexdigest())
PY

# --- extracted trees identical? (readers see the same content) ---
step extract_cmp bash -c '
  cd "$0/run/pad"   && unsquashfs -d out "$0/padded.sqfs" >/dev/null 2>&1; echo "pad_unsquashfs_rc=$?"  > "$0/extract.txt"
  cd "$0/run/nopad" && unsquashfs -d out "$0/nopad.sqfs"  >/dev/null 2>&1; echo "nopad_unsquashfs_rc=$?" >> "$0/extract.txt"
  cd "$0/run/pad/out"   && find . -type f | sort | xargs sha256sum | sed "s|^|PAD |"   >> "$0/extract.txt"
  cd "$0/run/nopad/out" && find . -type f | sort | xargs sha256sum | sed "s|^|NOPAD |" >> "$0/extract.txt"
' "$P"

echo "=== STEPS ==="; cat "$LOG"
echo; echo "=== superblock stdout ==="; cat "$P/superblock.stdout"
echo "=== padshape stdout ==="; cat "$P/padshape.stdout"
echo "=== extract_cmp stdout ==="; cat "$P/extract_cmp.stdout"
echo "=== mk_nopad_hyphen stderr ==="; cat "$P/mk_nopad_hyphen.stderr" | head -3
echo "=== versions ==="
mksquashfs -version 2>&1 | head -1
unsquashfs -version 2>&1 | head -1
sasquatch --version 2>&1 | head -2
