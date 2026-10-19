#!/usr/bin/env bash
# RV-8 evidence script (v2, working procedure) — re-derive EX-30's claimed
# identities from the current EX-30 pair against the HEAD bases.
# Run:  bash ex30-apply-v2.sh [REPO] [EX30DIR]
set -u
REPO="${1:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}"
E="${2:-$REPO/.ufo/waves/arc3-loop1-round3/claims/c2/EX-30}"
W=/var/tmp/rv8/ex30-apply-v2
rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 1

# base files: SKILL.md from the worktree (unmodified at HEAD), README.md from git HEAD
cp "$REPO/SKILL.md" ./base-skill.md
git -C "$REPO" show HEAD:.ufo/gates/custody-pair/README.md > ./base-readme.md
echo "== bases"; sha256sum base-skill.md base-readme.md

awk '/^```diff/{on=1;next} /^```$/{if(on){exit}} on{print}' "$E/registry-row.patch.md" > registry-row.diff
awk '/^```diff/{on=1;next} /^```$/{if(on){exit}} on{print}' "$E/readme.patch.md" > readme.diff
echo "== diffs"; wc -l registry-row.diff readme.diff; sha256sum registry-row.diff readme.diff

mkdir -p b/.ufo/gates/custody-pair
cp base-skill.md b/SKILL.md
cp base-readme.md b/.ufo/gates/custody-pair/README.md
cd b || exit 1
patch -p1 < ../registry-row.diff && echo "registry-row apply rc=0"
patch -p1 < ../readme.diff && echo "readme apply rc=0"
cd .. || exit 1
echo "== patched outputs (EX-30 claims: SKILL 62de3922…/390, README a82d0071…/180)"
sha256sum b/SKILL.md b/.ufo/gates/custody-pair/README.md
wc -l b/SKILL.md b/.ufo/gates/custody-pair/README.md