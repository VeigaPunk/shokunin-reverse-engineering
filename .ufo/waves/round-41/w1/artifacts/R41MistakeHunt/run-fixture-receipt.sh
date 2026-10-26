#!/usr/bin/env bash
# run-fixture-receipt.sh <WORKDIR> -- reproducible receipt for the S126 repair check.
# Clones the lane (read-only, --shared), runs registry-body-reach.py on the base state, applies
# fixture-repair.py, and proves the check is able to fail on the repaired state (stub) and
# returns to clean only with the byte-exact body.  Never touches the lane; every git call names
# -C and uses fixture identity -c user.name=fx -c user.email=fx@fx.
set -u
W=${1:?usage: run-fixture-receipt.sh <WORKDIR>}
ART=$(cd "$(dirname "$0")" && pwd)
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
SRC=/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work
FX="$W/fx.receipt"
rm -rf "$FX"
mkdir -p "$FX"
git clone -q --shared "$LANE" "$FX/lane" || exit 2
TOP=$(git -C "$FX/lane" rev-parse --show-toplevel) || exit 2
[ "$TOP" = "$FX/lane" ] || { echo "toplevel mismatch: $TOP"; exit 2; }
echo "# fixture clone: $TOP"
echo "# base: $(git -C "$FX/lane" rev-parse HEAD)"
echo
echo "## 1. base state (unmodified lane at the round-41 base)"
python3 -I -B "$ART/registry-body-reach.py" --root "$FX/lane" --rev HEAD
echo "exit=$?"
echo
echo "## 2. repair: three own-work bodies into corpus/evidence/round-11/avm-be/, row and knowledge lineage repointed"
python3 -I -B "$ART/fixture-repair.py" --lane "$FX/lane" --source "$SRC"
echo "exit=$?"
git -C "$FX/lane" -c user.name=fx -c user.email=fx@fx add -A
git -C "$FX/lane" -c user.name=fx -c user.email=fx@fx commit -q -m "fixture: S126 bodies in lane"
echo "repair commit: $(git -C "$FX/lane" rev-parse HEAD)"
python3 -I -B "$ART/registry-body-reach.py" --root "$FX/lane" --rev HEAD
echo "exit=$?"
echo
echo "## 3. control: same name, wrong bytes (4096 zero bytes at the repaired path)"
python3 -c "open('$FX/lane/corpus/evidence/round-11/avm-be/avm-be.squashfs','wb').write(b'\0'*4096)"
git -C "$FX/lane" -c user.name=fx -c user.email=fx@fx commit -qam "fixture control: stub"
python3 -I -B "$ART/registry-body-reach.py" --root "$FX/lane" --rev HEAD
echo "exit=$?"
cp "$SRC/avm-be.squashfs" "$FX/lane/corpus/evidence/round-11/avm-be/avm-be.squashfs"
git -C "$FX/lane" -c user.name=fx -c user.email=fx@fx commit -qam "fixture control: restore image"
echo "restored image; check:"
python3 -I -B "$ART/registry-body-reach.py" --root "$FX/lane" --rev HEAD
echo "exit=$?"
echo
echo "## 3b. control: the lane-root unblob.log (a different body, same basename) substituted for the round-11 log"
cp "$LANE/unblob.log" "$FX/lane/corpus/evidence/round-11/avm-be/unblob.log"
git -C "$FX/lane" -c user.name=fx -c user.email=fx@fx commit -qam "fixture control: same basename, other body"
echo "substituted bytes: $(sha256sum "$FX/lane/corpus/evidence/round-11/avm-be/unblob.log" | cut -d' ' -f1)"
echo "row pin:           352e0d794143df9cc4fa6113d72ee5a620ea0aa201a930e00e91590518aed5d7"
python3 -I -B "$ART/registry-body-reach.py" --root "$FX/lane" --rev HEAD
echo "exit=$?"
cp "$SRC/unblob.log" "$FX/lane/corpus/evidence/round-11/avm-be/unblob.log"
git -C "$FX/lane" -c user.name=fx -c user.email=fx@fx commit -qam "fixture control: restore log"
echo "restored log; check:"
python3 -I -B "$ART/registry-body-reach.py" --root "$FX/lane" --rev HEAD
echo "exit=$?"
echo
echo "## 4. final state of the repaired fixture"
git -C "$FX/lane" rev-parse HEAD
python3 -I -B "$ART/registry-body-reach.py" --root "$FX/lane" --rev HEAD
echo "exit=$?"
echo
echo "## 5. selftest of the check"
python3 -I -B "$ART/registry-body-reach.py" --selftest
echo "exit=$?"
echo
echo "## 6. the repair commit itself"
REPC=$(git -C "$FX/lane" log --format=%H --grep='fixture: S126 bodies in lane' -1)
git -C "$FX/lane" show --stat --format='commit %h %s' "$REPC"
echo "-- changed lines (SOURCES.md, knowledge doc):"
git -C "$FX/lane" show --format= --unified=0 "$REPC" -- corpus/SOURCES.md corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md | grep -E '^[-+][^-+]'
echo
echo "## 7. production run against the lane itself (read-only, git objects)"
python3 -I -B "$ART/registry-body-reach.py" --root "$LANE" --rev 49096c7e6f226af0c750c4b003be58883cb6049f
echo "exit=$?"
exit 0
