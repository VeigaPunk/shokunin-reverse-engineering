#!/usr/bin/env bash
# R45W2SweepAudit fixture: does a merge commit that edits a frozen path in its
# resolution escape (a) the round-45 counters' frozen arm and (b) a per-commit
# `git diff-tree --name-status -r` sweep?
# Read-only on the lane: the lane's blobs are copied in with `git show`.
set -u
S=/fast/scratch/hyaku/kaidoku-r45/R45W2SweepAudit
export TMPDIR="$S"
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
FREEZE=f762b7273e3f6ca3c710bb37d5de92a4a4417aec
D="$S/fixtures/merge-blindness"
rm -rf "$D"; mkdir -p "$D"

git -C "$D" init -q
TOP=$(git -C "$D" rev-parse --show-toplevel)
[ "$TOP" = "$D" ] || { echo "REFUSING: toplevel $TOP != $D"; exit 9; }

mkdir -p "$D/plans" "$D/tools/round-45"
git -C "$LANE" show "$FREEZE:plans/round-45-claims.md" > "$D/plans/round-45-claims.md"
for f in frozen-path-preflight.py c1-counter.py c2-counter.py registry-scope.json; do
  git -C "$LANE" show "$FREEZE:tools/round-45/$f" > "$D/tools/round-45/$f"
done

git -C "$D" add -A
git -C "$D" -c user.name=seat -c user.email=seat@local commit -qm "freeze"
F=$(git -C "$D" rev-parse HEAD)

# first-parent line
echo a > "$D/a.txt"; git -C "$D" add a.txt
git -C "$D" -c user.name=seat -c user.email=seat@local commit -qm "main work"
# side line
git -C "$D" checkout -q -b side "$F"
echo b > "$D/b.txt"; git -C "$D" add b.txt
git -C "$D" -c user.name=seat -c user.email=seat@local commit -qm "side work"
git -C "$D" checkout -q master 2>/dev/null || git -C "$D" checkout -q main

git -C "$D" -c user.name=seat -c user.email=seat@local merge -q --no-commit side
echo "" >> "$D/plans/round-45-claims.md"
echo "post-freeze edit smuggled into a merge resolution" >> "$D/plans/round-45-claims.md"
git -C "$D" add -A
git -C "$D" -c user.name=seat -c user.email=seat@local commit -qm "merge side (resolution edits the frozen claims file)"
M=$(git -C "$D" rev-parse HEAD)

echo "== fixture: F=$F merge=$M parents=$(git -C "$D" rev-list --parents -1 $M | wc -w) "
echo
echo "--- A. counter frozen arm query (c1-counter.py:53 form) ---"
git -C "$D" log --name-only --format= "$F..$M" -- plans/round-45-claims.md tools/round-45
echo "A exit=$?  (no path line above = arm sees nothing)"
echo
echo "--- B. per-commit name-status sweep (this seat's form) ---"
git -C "$D" diff-tree --no-commit-id --name-status -r "$M"
echo "B exit=$?  (empty above = sweep is blind to the resolution edit)"
echo
echo "--- C. the merge-visible form ---"
git -C "$D" diff-tree -m --first-parent --no-commit-id --name-status -r "$M"
echo "C exit=$?"
echo
echo "--- D. direct diff against first parent ---"
git -C "$D" diff "$M^1" "$M" -- plans/round-45-claims.md
echo "D exit=$?"
echo
echo "--- E. counter function called live ---"
python3 -I -B - "$D" "$F" "$M" "$LANE" <<'PY'
import importlib.util, subprocess, sys
d, f, m, lane = sys.argv[1:5]
spec = importlib.util.spec_from_file_location("c1", f"{lane}/tools/round-45/c1-counter.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
print("frozen_path_changed(fixture, F, MERGE) =", mod.frozen_path_changed(d, f, m))
alt = subprocess.run(["git","-C",d,"log","--name-only","--format=",
                      "--diff-merges=first-parent",f"{f}..{m}","--",
                      "plans/round-45-claims.md","tools/round-45/"],
                     capture_output=True, text=True).stdout
print("--diff-merges=first-parent variant =", [p for p in alt.splitlines() if p.strip()])
PY
echo "E exit=$?"
