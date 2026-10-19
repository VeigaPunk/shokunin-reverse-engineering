#!/bin/bash
# EX-25 raw shell transcript: the seat-line attack, `--paths X --out X` on scratch.
# Every X lives under /var/tmp/ex25/raw/<label>/ ; no real custody path is named.
set -u
run () {  # $1 = label, $2 = tool path
  L=$1; T=$2
  D=/var/tmp/ex25/raw/$L
  rm -rf "$D"; mkdir -p "$D"
  printf 'VICTIM-PAYLOAD-%s\n' "$L" > "$D/X"
  for i in $(seq 1 24); do printf 'VICTIM-PAYLOAD-%s\n' "$L" >> "$D/X"; done
  echo "--- [$L] tool sha256: $(sha256sum "$T" | cut -d' ' -f1)"
  echo "--- [$L] X before: $(sha256sum "$D/X" | cut -d' ' -f1)  inode=$(stat -c %i "$D/X") mtime_ns=$(stat -c %Y "$D/X") ctime=$(stat -c %Z "$D/X") size=$(stat -c %s "$D/X")"
  echo "--- [$L] \$ python3 $T capture --paths $D/X --out $D/X"
  python3 "$T" capture --paths "$D/X" --out "$D/X"; echo "--- [$L] exit=$?"
  echo "--- [$L] X after : $(sha256sum "$D/X" | cut -d' ' -f1)  inode=$(stat -c %i "$D/X") size=$(stat -c %s "$D/X")"
  echo "--- [$L] sidecars: $(ls "$D" | tr '\n' ' ')"
  echo
}
run before     /var/tmp/ex25/before/custody-pair.py
run candidate  /var/tmp/ex25/after/custody-pair.py
run landed     /var/tmp/ex25/landed/custody-pair.py
