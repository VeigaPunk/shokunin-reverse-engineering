#!/bin/bash
# VZ-4 revision watcher — 20 s cadence, 90 samples (~30 min). Logs the identity
# of every real target under integration plus the C1 patch-side counters, so the
# wave summary can state revision finality with timestamps rather than a pin.
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
OUT=$R/.ufo/waves/arc3-loop1-round3/claims/cross/VZ-4/revisions.log
: > "$OUT"
for i in $(seq 1 90); do
  ts=$(date -u +%FT%TZ)
  c2=$(sha256sum "$R/.ufo/gates/custody-pair/custody-pair.py" 2>/dev/null | cut -c1-16)
  c2l=$(wc -l < "$R/.ufo/gates/custody-pair/custody-pair.py" 2>/dev/null)
  c2r=$(sha256sum "$R/.ufo/gates/custody-pair/README.md" 2>/dev/null | cut -c1-16)
  c3t=$(sha256sum "$R/.ufo/gates/citation-drift/pointer-table.json" 2>/dev/null | cut -c1-16)
  c3e=$(sha256sum "$R/.ufo/gates/citation-drift/expected.json" 2>/dev/null | cut -c1-16)
  c3n=$(python3 -c "import json;print(len(json.load(open('$R/.ufo/gates/citation-drift/pointer-table.json'))['entries']))" 2>/dev/null)
  kn=$(ls "$R/corpus/knowledge" 2>/dev/null | wc -l)
  seats=$(ls "$R/.ufo/waves/arc3-loop1-round3/seats" 2>/dev/null | grep -c '\.md$')
  printf '%s r%02d c2=%s/%sL readme=%s c3tab=%s entries=%s expected=%s knowledge=%s seats=%s\n' \
    "$ts" "$i" "$c2" "$c2l" "$c2r" "$c3t" "$c3n" "$c3e" "$kn" "$seats" >>"$OUT"
  sleep 20
done
echo "$(date -u +%FT%TZ) revwatch=done" >> "$OUT"