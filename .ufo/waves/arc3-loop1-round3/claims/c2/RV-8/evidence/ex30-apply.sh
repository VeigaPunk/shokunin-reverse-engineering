#!/usr/bin/env bash
# RV-8: apply EX-30's two patch texts to scratch copies of the base files and
# re-derive every identity they claim.
set -u
EX30=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c2/EX-30
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=/var/tmp/rv8/ex30-apply
rm -rf "$W"; mkdir -p "$W"
cd "$W" || exit 1

cp "$REPO/SKILL.md" ./SKILL.md
git -C "$REPO" show HEAD:.ufo/gates/custody-pair/README.md > ./README.md
echo "== base identities"
sha256sum SKILL.md README.md

# extract fenced diff blocks
awk '/^```diff/{on=1;next} /^```$/{if(on){exit}} on{print}' "$EX30/registry-row.patch.md" > registry-row.diff
awk '/^```diff/{on=1;next} /^```$/{if(on){exit}} on{print}' "$EX30/readme.patch.md" > readme.diff
echo "== diff identities"
wc -l registry-row.diff readme.diff
sha256sum registry-row.diff readme.diff

mkdir -p a b
cp SKILL.md a/SKILL.md; cp README.md a/README.md
cd a || exit 1
patch -p1 < ../registry-row.diff && echo "registry-row patch rc=0" || echo "registry-row patch FAILED"
patch -p1 < ../readme.diff && echo "readme patch rc=0" || echo "readme patch FAILED"
cd .. || exit 1
echo "== patched identities (claimed: SKILL fed49a68…, README 4884e895…)"
sha256sum a/SKILL.md a/README.md
wc -l a/SKILL.md a/README.md
echo "== apply-twice idempotence check (should FAIL on second apply)"
cd a && patch -p1 --dry-run < ../registry-row.diff >/dev/null 2>&1 && echo "WARNING: applies twice" || echo "second apply refused (expected)"