#!/bin/sh
# R45W2Src141 real-repo checks. Read-only: git log/show/rev-parse/ls-tree/status.
# Run from the lane root. Emits UTC + exit code per check.
set -u
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
GATE=/fast/scratch/hyaku/kaidoku-r45/R45W2Src141/preflight.py
PAGE=/fast/scratch/hyaku/kaidoku-r45/R45W2Src141/s141.html
W1=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-45/w1/R45W1SrcGitDiffTree/s141-git-diff-tree.html
F=f762b7273e3f6ca3c710bb37d5de92a4a4417aec
A1=1f4b27f82353d6544dc0c8048b3cfdadd8525d12
Q='When --raw, --numstat, --name-only or --name-status has been given, do not munge pathnames and use NULs as output field terminators.'

echo "UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo
echo "## quote word count (printf | wc -w)"
printf '%s' "$Q" | wc -w
echo "exit=$?"
echo
echo "## page identity (this seat's fetch)"
sha256sum "$PAGE"; wc -c < "$PAGE"
echo
echo "## byte-compare this seat's fetch with wave-1's saved copy"
cmp "$PAGE" "$W1"; echo "cmp_exit=$?"
echo
echo "## lesson Gate word-count token by revision"
for r in e715263cb51b713c342ab992d527fe9d61d6f8ff "$A1" HEAD; do
    printf '%s -> ' "$r"
    git -C "$LANE" show "$r:corpus/lessons/round-45.md" | grep -o 'terminators." ([0-9]* words)' | head -1
done
echo
echo "## frozen blob ids (tools/round-45/frozen-path-preflight.py, plans/round-45-claims.md)"
for r in "$F" "$A1" HEAD; do
    printf '%s ' "$r"
    git -C "$LANE" rev-parse "$r:tools/round-45/frozen-path-preflight.py" "$r:plans/round-45-claims.md" | tr '\n' ' '
    echo
done
echo
echo "## commits in FREEZE..HEAD touching a frozen path (commit arm on the real repo)"
git -C "$LANE" log --name-status --format='%H %s' "$F..HEAD" -- tools/round-45/ plans/round-45-claims.md
echo "log_exit=$?"
echo
echo "## frozen paths at FREEZE, non-ASCII scan (LC_ALL=C, '[^ -~]')"
git -C "$LANE" ls-tree -r --name-only "$F" -- tools/round-45/ plans/round-45-claims.md | tee /tmp/../dev/null | LC_ALL=C grep -c '[^ -~]'
echo "grep_nonascii_exit=$? (1 = none)"
git -C "$LANE" ls-tree -r --name-only "$F" -- tools/round-45/ plans/round-45-claims.md | wc -l
echo
echo "## gate at the brief's measured revision A1"
python3 "$GATE" --root "$LANE" --freeze "$F" --rev "$A1" \
    --pathspec tools/round-45/ --pathspec plans/round-45-claims.md \
    --freeze-path tools/round-45 --freeze-path plans/round-45-claims.md --check-dirty
echo "exit=$?"
echo
echo "## gate at HEAD"
python3 "$GATE" --root "$LANE" --freeze "$F" --rev HEAD \
    --pathspec tools/round-45/ --pathspec plans/round-45-claims.md \
    --freeze-path tools/round-45 --freeze-path plans/round-45-claims.md --check-dirty
echo "exit=$?"
echo
echo "## worktree status under the frozen pathspec"
git -C "$LANE" status --porcelain -- tools/round-45/ plans/round-45-claims.md
echo "status_exit=$?"
echo
echo "## L1 published receipt revs"
for f in .ufo/waves/round-45/l1/preflight-round45-frozen-both.json .ufo/waves/round-45/l1/preflight-round45-frozen.json; do
    printf '%s -> ' "$f"
    python3 -c "import json;d=json.load(open('$LANE/$f'));print(d['rev'],d['verdict'])" 2>/dev/null || echo unreadable
done
