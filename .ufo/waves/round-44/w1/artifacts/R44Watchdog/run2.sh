#!/usr/bin/env bash
set -u
SEAT=R44Watchdog; OUT=out
rec() { local id="$1"; shift; local f="$OUT/$id.stdout.txt" e="$OUT/$id.stderr.txt" t0 t1 rc sha wall bytes
  t0=$(date +%s.%N); "$@" >"$f" 2>"$e"; rc=$?; t1=$(date +%s.%N)
  wall=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.3f", b-a}')
  sha=$(sha256sum "$f" | cut -d' ' -f1); bytes=$(stat -c%s "$f")
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$SEAT" "$id" "$rc" "$sha" "$wall" "$bytes" "$*" >> receipts.tsv
  echo "[$id] rc=$rc wall=${wall}s sha256=$sha bytes=$bytes"; return 0; }
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
rec W15-claims-target-lines   grep -nE "carriers_matched|six carriers|These (four|six)" "$LANE/plans/round-44-claims.md"
rec W16-claims-carrier-rows   sed -n '/^| id | file | handler/,/^$/p' "$LANE/plans/round-44-claims.md"
rec W17-carriers-ids          python3 -c 'import json;d=json.load(open("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/carriers.json"));print(len(d["carriers"]));[print(c["id"],c["handler"],c["endian"],c["sha256"]) for c in d["carriers"]]'
rec W18-claims-sha            sha256sum "$LANE/plans/round-44-claims.md"
rec W19-claims-clean          git -C "$LANE" status --porcelain=v1 -- plans/round-44-claims.md
rec W20-inventory-snapshot    bash -c 'cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git status --porcelain=v1 -uall'
rec W21-tools44-head          git -C "$LANE" ls-tree -r --name-only HEAD -- tools/round-44/
rec W22-artifacts-dir         ls -la "$LANE/.ufo/waves/round-44/w1/artifacts"
rec W23-wave-md-count         bash -c 'ls /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w1/*.md | wc -l'
rec W24-spawncap-count        bash -c 'grep -cE "spawn-cap .*kaidoku-shokunin/.ufo/waves/round-44/w1.ready" /home/vgpnk/Projects/shokunin/.ufo/state/inline-dispatcher.log'
rec W25-unblob-versions       bash -c 'unblob --version; /usr/bin/unsquashfs -version | head -1; sasquatch -version | head -1'
