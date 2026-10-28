#!/usr/bin/env bash
set -u
SEAT=R44Watchdog; OUT=out
rec() { local id="$1"; shift; local f="$OUT/$id.stdout.txt" e="$OUT/$id.stderr.txt" t0 t1 rc sha wall bytes
  t0=$(date +%s.%N); "$@" >"$f" 2>"$e"; rc=$?; t1=$(date +%s.%N)
  wall=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.3f", b-a}')
  sha=$(sha256sum "$f"|cut -d' ' -f1); bytes=$(stat -c%s "$f")
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$SEAT" "$id" "$rc" "$sha" "$wall" "$bytes" "$*" >> receipts.tsv
  echo "[$id] rc=$rc wall=${wall}s sha256=$sha bytes=$bytes"; return 0; }
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=$PWD/cmpchk; mkdir -p $W
python3 -c "open('$W/a','wb').write(b'A'*4096); open('$W/b','wb').write(b'A'*4095+b'B')"
rec W77-cmp-l-boundary   bash -c "cmp -l $W/a $W/b > $W/cmpL.out; echo rc=\$?; wc -c < $W/cmpL.out"
rec W78-cmp-s-boundary   bash -c "cmp -s $W/a $W/b; echo rc=\$?"
rec W79-cmp-plain        bash -c "cmp $W/a $W/b >/dev/null; echo rc=\$?"
rec W80-unsquashfs-dashver bash -c "/usr/bin/unsquashfs --version >/dev/null 2>&1; echo rc=\$?"
rec W81-unsquashfs-version-ok bash -c "/usr/bin/unsquashfs -version >/dev/null 2>&1; echo rc=\$?"
rec W82-caprefusal-seats bash -c "grep -oE 'w1.ready R44[A-Za-z0-9]+' /home/vgpnk/Projects/shokunin/.ufo/state/inline-dispatcher.log | awk '\$1==\"w1.ready\"{print \$2}' | sort | uniq -c"
