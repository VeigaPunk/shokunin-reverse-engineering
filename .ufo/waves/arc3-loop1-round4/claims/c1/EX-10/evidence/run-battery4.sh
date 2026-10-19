#!/bin/bash
# EX-10 battery 4: path vs inode vs mtime as id inputs (all scratch-internal)
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
OUT=/var/tmp/ex10-r4/out
LOG=/var/tmp/ex10-r4/battery4-log.txt
T1=/var/tmp/ex10-r4/tmpdir
W=/var/tmp/ex10-r4/work
SRC=$REPO/.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex
: > "$LOG"
mkdir -p "$W/ino"
cp "$SRC" "$W/ino/a.hex"
ln "$W/ino/a.hex" "$W/ino/b.hex"
echo "inode check: a=$(stat -c %i "$W/ino/a.hex") b=$(stat -c %i "$W/ino/b.hex") nlink=$(stat -c %h "$W/ino/a.hex")" >> "$LOG"
run() { local leg="$1"; shift
  ( cd "$REPO" && TMPDIR="$T1" npx -y rea-agents@6.4.0 inspect-evm-interface "$@" ) > "$OUT/$leg.json" 2> "$OUT/$leg.err"
  local rc=$?; local eid; eid=$(python3 -c "import json;print(json.load(open('$OUT/$leg.json')).get('evidence_id',''))" 2>/dev/null)
  local sha; sha=$(sha256sum "$OUT/$leg.json"|cut -d' ' -f1)
  printf 'leg=%-14s exit=%s envelope=%s id=%s argv=%s\n' "$leg" "$rc" "${sha:0:16}" "$eid" "$1" >> "$LOG"
}
run ino-a "$W/ino/a.hex" hex --format json
run ino-b "$W/ino/b.hex" hex --format json
# recreate at the same path: new inode, same bytes
rm "$W/ino/b.hex"; rm "$W/ino/a.hex"; cp "$SRC" "$W/ino/a.hex"
echo "recreated inode=$(stat -c %i "$W/ino/a.hex")" >> "$LOG"
run recreate-a "$W/ino/a.hex" hex --format json
# mtime-only change at the same path
touch -d '2020-01-01 00:00:00' "$W/ino/a.hex"
echo "mtime now $(stat -c %y "$W/ino/a.hex")" >> "$LOG"
run mtime-a "$W/ino/a.hex" hex --format json
# content-mutation control at the same path (append 0x00)
printf '00' >> "$W/ino/a.hex"
run mutate-a "$W/ino/a.hex" hex --format json
echo "BATTERY4-DONE" >> "$LOG"
