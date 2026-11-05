#!/bin/bash
# SentinelRepair probe A: --out path confinement (scratch only). Read-only on lane.
set -u
S=/fast/scratch/hyaku/kaidoku-r92/SentinelRepair
C=$S/clone/tools/round-91/upx-stop-boundary-repair.py
W=$S/work/a
PKG=$S/work/packed-xxd
mkdir -p "$W" "$S/work/outside" "$S/logs"
L=$S/logs/probe_a.log
run() { # run TOOL with pinned scratch env; echoes rc
  TMPDIR=$S/tmp HOME=$S/tmp python3 -I -B "$C" "$@" >"$W/last.stdout" 2>"$W/last.stderr"
  echo "rc=$?"
  echo "stdout: $(cat "$W/last.stdout")"
  [ -s "$W/last.stderr" ] && echo "stderr: $(cat "$W/last.stderr")"
  return 0
}
{
echo "== A0 baseline: intact packed carrier, plain --out inside work dir"
run --in "$PKG" --out "$W/base-out" --info "$W/base-info.json"
echo "wrote: $(ls -l "$W/base-out" 2>/dev/null | awk '{print $5, $9}')"

echo; echo "== A1 --out is a symlink to a file OUTSIDE the work dir"
printf 'VICTIM-ORIGINAL\n' > "$S/work/outside/victim.bin"
ln -s "$S/work/outside/victim.bin" "$W/out"
echo "before: $(ls -l "$W/out")"
run --in "$PKG" --out "$W/out"
echo "after-link: $(ls -l "$W/out")"
echo "victim sha/content: $(sha256sum "$S/work/outside/victim.bin" | cut -c1-16) $(cat "$S/work/outside/victim.bin")"
cmp -s "$W/out" "$PKG" && echo "out-is-regular-and-identical-to-input=true" || echo "out-is-regular-and-identical-to-input=false"
[ -L "$W/out" ] && echo "symlink-survives=true" || echo "symlink-survives=false"

echo; echo "== A2 --out parent is a symlink (final parent component)"
mkdir -p "$W/a2real"
ln -s a2real "$W/a2link"
run --in "$PKG" --out "$W/a2link/out"
echo "a2real entries after: $(ls -A "$W/a2real" | wc -l)"

echo; echo "== A3 intermediate symlink component escapes the work tree"
mkdir -p "$S/work/outside/escape"
ln -s "$S/work/outside/escape" "$W/esc"
mkdir -p "$W/esc/sub"   # mkdir follows the symlink: creates outside/escape/sub
run --in "$PKG" --out "$W/esc/sub/out"
echo "escape-dir now: $(ls -l "$S/work/outside/escape/sub" 2>/dev/null)"
cmp -s "$S/work/outside/escape/sub/out" "$PKG" && echo "file-landed-outside-worktree=true" || echo "file-landed-outside-worktree=false"

echo; echo "== A4 --out carries a '..' component (resolves inside work)"
mkdir -p "$W/sub"
run --in "$PKG" --out "$W/sub/../out4"

echo; echo "== A5 refused input: pre-existing --out must be untouched"
printf 'PRE-EXISTING\n' > "$W/out5"
printf 'not an elf at all' > "$W/bad-in"
run --in "$W/bad-in" --out "$W/out5"
echo "out5 content now: $(cat "$W/out5")"

echo; echo "== A6 --out is a symlink to a DIRECTORY"
mkdir -p "$W/dir-target"
ln -s "$W/dir-target" "$W/outdir"
run --in "$PKG" --out "$W/outdir"
echo "dir-target entries after: $(ls -A "$W/dir-target" | wc -l)"
} 2>&1 | tee "$L"
echo "LOG=$L"
