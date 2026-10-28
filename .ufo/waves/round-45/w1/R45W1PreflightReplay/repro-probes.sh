#!/bin/sh
# Reproducer for the two false greens in tools/round-45/frozen-path-preflight.py
# (frozen at f762b7273e3f6ca3c710bb37d5de92a4a4417aec).
# Read-only on the lane tree: every git call is -C "$D" on a throwaway fixture under
# $TMPDIR (never /tmp). Usage: S=$(mktemp -d -p /fast/scratch) TMPDIR=$S sh repro-probes.sh
set -u
S=${TMPDIR:-$(mktemp -d -p /fast/scratch)}
LANE=${LANE:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
TOOL="$S/preflight-copy.py"
cp "$LANE/tools/round-45/frozen-path-preflight.py" "$TOOL" || exit 1

mk() { D=$(mktemp -d -p "$S" fx.XXXXXX); git -C "$D" init -q; \
       git -C "$D" config user.email p@f; git -C "$D" config user.name p; }
cm() { git -C "$D" add -A && git -C "$D" commit -q -m "$1" && git -C "$D" rev-parse HEAD; }
gate() { want=$1; shift; python3 -I -B "$TOOL" --root "$D" "$@" >/dev/null; rc=$?; echo "  -> exit $rc  (want $want)"; }

echo "== P1: frozen FILE f.md touched-then-restored; only the frozen DIR is the pathspec (want 0 = false green)"
mk; echo v1 > "$D/f.md"; mkdir "$D/d"; echo x > "$D/d/x.txt"; F=$(cm freeze)
echo tampered > "$D/f.md"; cm tamper; echo v1 > "$D/f.md"; R=$(cm restore)
gate 0 --freeze "$F" --rev "$R" --pathspec d/ --freeze-path f.md --freeze-path d --require-pathspec
echo "== P2 control: same repo, same revs, f.md in the pathspec (want 1 = red)"
gate 1 --freeze "$F" --rev "$R" --pathspec d/ --pathspec f.md --freeze-path f.md --freeze-path d --require-pathspec

echo "== P13: frozen FILE f.md dirty in the worktree, out of the pathspec (want 0 = false green)"
mk; echo v1 > "$D/f.md"; mkdir "$D/d"; echo x > "$D/d/x.txt"; F=$(cm freeze)
echo dirty > "$D/f.md"
gate 0 --freeze "$F" --rev "$F" --pathspec d/ --freeze-path f.md --freeze-path d --require-pathspec --check-dirty
echo "== P14 control: same dirty tree, no pathspec (want 1 = red)"
gate 1 --freeze "$F" --rev "$F" --freeze-path f.md --freeze-path d --check-dirty

echo "== P17: pathspec NARROWER than the frozen dir; d/b.txt touched-then-restored (want 0 = false green)"
mk; mkdir "$D/d"; echo a > "$D/d/a.txt"; echo b > "$D/d/b.txt"; F=$(cm freeze)
echo tampered > "$D/d/b.txt"; cm tamper; echo b > "$D/d/b.txt"; R=$(cm restore)
gate 0 --freeze "$F" --rev "$R" --pathspec d/a.txt --freeze-path d --require-pathspec
echo "== P17 control: same repo/revs, pathspec equal to the dir (want 1 = red)"
gate 1 --freeze "$F" --rev "$R" --pathspec d/ --freeze-path d --require-pathspec

echo "== P18: same narrow pathspec, d/b.txt dirty (want 0 = false green)"
echo dirty > "$D/d/b.txt"
gate 0 --freeze "$R" --rev "$R" --pathspec d/a.txt --freeze-path d --require-pathspec --check-dirty
echo "== P18 control: pathspec equal to the dir (want 1 = red)"
gate 1 --freeze "$R" --rev "$R" --pathspec d/ --freeze-path d --require-pathspec --check-dirty

echo "== P15: real-lane reversed pair must be could-not-evaluate (want 2)"
D=$LANE python3 -I -B "$TOOL" --root "$LANE" --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec \
  --rev c86ea508 --pathspec tools/round-45/ --freeze-path tools/round-45 --require-pathspec
echo "  -> exit $?  (want 2)"
