#!/usr/bin/env bash
# run-sweeps.sh <WORKDIR> -- sweeps behind the S126 host-local-evidence finding.
# Read-only: git objects, grep over tracked text, sha256sum over the sibling tree.
set -u
W=${1:?usage: run-sweeps.sh <WORKDIR>}
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
REV=49096c7e6f226af0c750c4b003be58883cb6049f
SRC=/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work

echo "## A. how many registry rows cite the sibling tree (corpus/SOURCES.md)"
echo "\$ git -C LANE grep -c shokuknow -- corpus"
git -C "$LANE" grep -c "shokuknow" -- corpus || true
echo
echo "## B. the same sweep outside corpus/ (plans, PROVINCE, SKILL, SCORECARD, SHONEN)"
echo "\$ git -C LANE grep -n shokuknow -- plans PROVINCE.md SKILL.md SCORECARD.md SHONEN.md"
git -C "$LANE" grep -n "shokuknow" -- plans PROVINCE.md SKILL.md SCORECARD.md SHONEN.md
echo "grep exit=$? (1 = no match anywhere on these surfaces)"
echo
echo "## C. no registry row cites a host scratch body (the only /tmp hits are paths INSIDE the vendor image)"
echo "\$ git -C LANE grep -o -n -e '/fast/scratch[^ ]*' -e '/tmp/[^ ]*' -- corpus/SOURCES.md"
git -C "$LANE" grep -o -n -e "/fast/scratch[^ ]*" -e "/tmp/[^ ]*" -- corpus/SOURCES.md
echo "note: those two are the member paths var/tmp/filesystem.image and var/tmp/x86/filesystem.image inside the vendor image (S125 row),"
echo "      not host scratch; the classifier anchors at ^/tmp, so they are not scored."
echo "scope: numbered 'source: SNNN' lineage lines only; free-form '- source:' bullets in older knowledge entries are out of scope"
echo "       (many name deleted /tmp scratch and declare it in their own '## Scratch' section)."
echo
echo "## D. the three S126 bodies still hash to the pins the row carries (integrity holds; reach does not)"
sha256sum "$SRC/lead1-avm-image.tsv" "$SRC/avm-be.squashfs" "$SRC/unblob.log"
echo "row pins: f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0 (tsv)"
echo "          c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32 (image)"
echo "          352e0d794143df9cc4fa6113d72ee5a620ea0aa201a930e00e91590518aed5d7 (log)"
echo
echo "## E. durability is partial: the bodies are committed in the SIBLING repo at an unpinned revision"
echo "\$ git -C /home/vgpnk/Projects/shokuknow log -1 --format='%H %cI'"
git -C /home/vgpnk/Projects/shokuknow log -1 --format='%H %cI' || true
for f in lead1-avm-image.tsv avm-be.squashfs unblob.log; do
  printf '%s ' "$f"
  git -C /home/vgpnk/Projects/shokuknow cat-file blob "HEAD:lanes/kaidoku/round11/work/$f" 2>/dev/null | sha256sum || echo "absent at sibling HEAD"
done
echo
echo "## F. a fresh checkout of the LANE cannot reach those bodies (clone of the base)"
FX="$W/fx.sweep"
rm -rf "$FX"; mkdir -p "$FX"
git clone -q --shared "$LANE" "$FX/lane" || exit 2
echo "\$ git -C $FX/lane ls-tree -r --name-only $REV | grep -i 'avm-be'"
git -C "$FX/lane" ls-tree -r --name-only "$REV" | grep -i "avm-be" || echo "(no carrier body in the lane tree at the base)"
echo "\$ ls $FX/lane/corpus/evidence/round-11"
ls "$FX/lane/corpus/evidence/round-11" 2>&1 || true
echo "note: corpus/evidence/round-40/c1/L1/carrier.sqsh is committed in the same lane (lane-built carrier, in-lane) --"
git -C "$FX/lane" cat-file -s "$REV:corpus/evidence/round-40/c1/L1/carrier.sqsh" || true
echo
echo "## G. the two surfaces the finding names, at the base revision"
echo "\$ git -C LANE show REV:corpus/SOURCES.md | awk 'NR==132' | cut -c1-160"
git -C "$LANE" show "$REV:corpus/SOURCES.md" | awk 'NR==132' | cut -c1-160
echo "\$ git -C LANE show REV:corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md | sed -n '5p' | cut -c1-160"
git -C "$LANE" show "$REV:corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md" | sed -n '5p' | cut -c1-160
echo
echo "## H. the closure already filed this, status-neutral"
echo "\$ git -C LANE show REV:corpus/lessons/round-40-verifier-spotcheck.md | sed -n '87p'"
git -C "$LANE" show "$REV:corpus/lessons/round-40-verifier-spotcheck.md" | sed -n '87p'
echo
echo "## I. two of the three cited bodies ARE in the lane already (as round-40 wave artifacts); the third is not"
for p in \
  .ufo/waves/round-40/w1/artifacts/R40C1Revenger/round11-avm-be.squashfs \
  .ufo/waves/round-40/w1/artifacts/R40Quarantine/avm-be-r11.squashfs \
  .ufo/waves/round-40/w1/artifacts/R40C1Counter/dev-avm-be-4096.squashfs \
  .ufo/waves/round-40/w1/artifacts/R40C1MarkerBoundary/fixtures/avm-be.squashfs \
  .ufo/waves/round-40/w1/artifacts/R40Quarantine/lead1-avm-image.tsv; do
  printf '%s ' "$p"
  git -C "$LANE" cat-file blob "$REV:$p" | sha256sum
done
echo "row pins: image c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32"
echo "          tsv   f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0"
echo
echo "tracked files named lead1-avm-image.tsv or unblob.log in the whole lane at REV:"
git -C "$LANE" ls-tree -r --name-only "$REV" | grep -E '(^|/)(lead1-avm-image\.tsv|unblob\.log)$' || echo "(none)"
echo
echo "## J. same basename, different body: the lane-root unblob.log is NOT the round-11 extraction log"
printf '%s ' "unblob.log (lane root, REV)"; git -C "$LANE" cat-file blob "$REV:unblob.log" | sha256sum
echo "row pin for the round-11 log: 352e0d794143df9cc4fa6113d72ee5a620ea0aa201a930e00e91590518aed5d7"
echo "the lane-root file shares M38-7's recorded prefix (2d651a4a) but not its tail (…9299 vs …f16299): attribution withheld."
echo "a repair that points S126 at 'unblob.log' substitutes a different observation either way."
echo
echo "and none of the in-lane copies is named by any registry row or knowledge entry:"
git -C "$LANE" grep -c "R40C1Revenger\|R40Quarantine/avm-be-r11\|dev-avm-be-4096\|R40C1MarkerBoundary/fixtures/avm-be\|R40Quarantine/lead1-avm-image" -- corpus/SOURCES.md corpus/knowledge || echo "grep exit=$? (1 = none)"
exit 0
