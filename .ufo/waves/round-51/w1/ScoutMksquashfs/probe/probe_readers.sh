#!/usr/bin/env bash
# CANONICAL reader probe: each reader runs in its OWN cwd (probe_final.sh's sasquatch
# steps shared $P and collided on the "out" directory, giving rc=1 for the nopad case).
set -u
S=/fast/scratch/hyaku/kaidoku-r51/w1-ScoutMksquashfs
P="$S/canonical"
R="$P/readers"
rm -rf "$R"; mkdir -p "$R/pad" "$R/nopad" "$R/pad2"
LOG="$R/steps.log"; : > "$LOG"

step() {  # step <name> <cwd> <cmd...>
  local name="$1" cwd="$2"; shift 2
  local out="$R/$name.stdout" utc rc sha
  utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  ( cd "$cwd" && "$@" ) > "$out" 2>"$R/$name.stderr"; rc=$?
  sha=$(sha256sum "$out" | cut -d' ' -f1)
  printf '%s\t(%s) %s\trc=%s\tstdout_sha256=%s\t%s\n' "$name" "$(basename "$cwd")" "$*" "$rc" "$sha" "$utc" >> "$LOG"
  printf '%s\n' "$rc" > "$R/$name.rc"
}

step unsq_pad   "$R/pad"   unsquashfs -s "$P/padded.sqfs"
step unsq_nopad "$R/nopad" unsquashfs -s "$P/nopad.sqfs"
step sasq_pad   "$R/pad"   sasquatch -d out "$P/padded.sqfs"
step sasq_nopad "$R/nopad" sasquatch -d out "$P/nopad.sqfs"
step sasq_pad2  "$R/pad2"  sasquatch -d out "$P/padded2.sqfs"

# extracted trees: identical content?
{
  echo "--- PAD tree ---"
  ( cd "$R/pad/out" && find . | sort | while read -r f; do printf '%s  %s\n' "$(sha256sum "$f" 2>/dev/null | cut -d' ' -f1)" "$f"; done )
  echo "--- NOPAD tree ---"
  ( cd "$R/nopad/out" && find . | sort | while read -r f; do printf '%s  %s\n' "$(sha256sum "$f" 2>/dev/null | cut -d' ' -f1)" "$f"; done )
  echo "--- diff of the two trees (empty = identical) ---"
  diff <( cd "$R/pad/out" && find . | sort ) <( cd "$R/nopad/out" && find . | sort ) && echo "TREES_IDENTICAL=yes"
} > "$R/trees.txt" 2>&1

cat "$LOG"
echo; echo "=== trees ==="; cat "$R/trees.txt"
echo "=== sasq_nopad stderr (first 6) ==="; head -6 "$R/sasq_nopad.stderr"
echo "=== unsq_nopad stdout ==="; cat "$R/unsq_nopad.stdout"
