#!/usr/bin/env bash
# Decisive probe: is the ddwrt reader refusal caused by the missing 4K pad, or by the
# non-standard magic?  Patch ONLY the 4 magic bytes of a copy (length and padding
# untouched) and re-run the readers.
set -u
S=/fast/scratch/hyaku/kaidoku-r51/w1-ScoutMksquashfs
M="$S/magicprobe"; rm -rf "$M"; mkdir -p "$M/run/orig" "$M/run/patched"
L="$M/steps.log"; : > "$L"

step() { local n="$1" cwd="$2"; shift 2
  local out="$M/$n.stdout" utc rc sha
  utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  ( cd "$cwd" && "$@" ) > "$out" 2>"$M/$n.stderr"; rc=$?
  sha=$(sha256sum "$out" | cut -d' ' -f1)
  printf '%s\t(%s) %s\trc=%s\tstdout_sha256=%s\t%s\n' "$n" "$(basename "$cwd")" "$*" "$rc" "$sha" "$utc" >> "$L"
}

SRC=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C1Oracle/fixtures/squashfs_v3_ddwrt/big_endian/__input__
cp "$SRC/squashfs_v3.be.nopad.bin" "$M/orig.bin"
cp "$SRC/squashfs_v3.be.4kpad.bin" "$M/pad4k.bin"

# patch ONLY byte 0: 't'(0x74) -> 's'(0x73), turning the non-standard magic
# 0x74717368 into the standard BE magic 0x73717368.  Length/padding untouched.
python3 - "$M" <<'PY'
import pathlib, sys, hashlib
M = pathlib.Path(sys.argv[1])
for src, dst in (("orig.bin", "orig-magicfixed.bin"), ("pad4k.bin", "pad4k-magicfixed.bin")):
    b = bytearray((M / src).read_bytes())
    print(f"{src}: len={len(b)} magic_before={bytes(b[:4])!r}", file=sys.stderr)
    assert b[0] == 0x74, b[0]
    b[0] = 0x73
    (M / dst).write_bytes(bytes(b))
    print(f"  -> {dst}: len={len(b)} magic_after={bytes(b[:4])!r} "
          f"sha256={hashlib.sha256(bytes(b)).hexdigest()}", file=sys.stderr)
PY

step unsq_orig        "$M/run/orig"    unsquashfs -s "$M/orig.bin"
step unsq_orig_fixed  "$M/run/orig"    unsquashfs -s "$M/orig-magicfixed.bin"
step unsq_4k          "$M/run/orig"    unsquashfs -s "$M/pad4k.bin"
step unsq_4k_fixed    "$M/run/orig"    unsquashfs -s "$M/pad4k-magicfixed.bin"
step sasq_orig        "$M/run/orig"    sasquatch -be "$M/orig.bin"
step sasq_orig_fixed  "$M/run/orig"    sasquatch -be "$M/orig-magicfixed.bin"
step sasq_4k          "$M/run/orig"    sasquatch -be "$M/pad4k.bin"
step sasq_4k_fixed    "$M/run/orig"    sasquatch -be "$M/pad4k-magicfixed.bin"

{
  echo "--- lengths / padding ---"
  for f in orig.bin orig-magicfixed.bin pad4k.bin pad4k-magicfixed.bin; do
    printf '%-26s bytes=%-6s mod4096=%-5s sha256=%s\n' "$f" "$(stat -c %s "$M/$f")" \
      "$(( $(stat -c %s "$M/$f") % 4096 ))" "$(sha256sum "$M/$f" | cut -d' ' -f1)"
  done
  echo "--- reader verdicts ---"
  for n in unsq_orig unsq_orig_fixed unsq_4k unsq_4k_fixed sasq_orig sasq_orig_fixed sasq_4k sasq_4k_fixed; do
    printf '%-18s rc=%s\n' "$n" "$(cat "$M/$n.rc" 2>/dev/null || echo '?')"
  done
} > "$M/summary.txt" 2>&1
# rc files
for n in unsq_orig unsq_orig_fixed unsq_4k unsq_4k_fixed sasq_orig sasq_orig_fixed sasq_4k sasq_4k_fixed; do :; done

cat "$L"
echo; cat "$M/summary.txt"
echo "--- unsq_orig_fixed stdout (head 3) ---"; head -3 "$M/unsq_orig_fixed.stdout"
echo "--- unsq_orig stderr (head 2) ---"; head -2 "$M/unsq_orig.stderr"
