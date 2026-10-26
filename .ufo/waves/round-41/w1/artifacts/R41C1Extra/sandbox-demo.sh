#!/usr/bin/env bash
# R41C1Extra sandbox demo: a round-41-shaped landing in a throwaway clone, scored by the
# ported gate. DEV ONLY — the carrier is the round-40 lane-built L1 (a development input),
# not any reserved or round-41 carrier; this is a satisfiability demo of the gate, not a score.
# usage: sandbox-demo.sh CLONE GATE_PY WORKDIR
set -euo pipefail
clone=$1; gate=$2; work=$3
ENTRY=corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md
STEM=2026-10-26-r41-avm-be-squashfs-core
[[ $(git -C "$clone" rev-parse --show-toplevel) == "$clone" ]] || { echo "not a clone: $clone" >&2; exit 2; }
base=$(git -C "$clone" rev-parse HEAD)
mkdir -p "$clone/tools/round-41" "$clone/.ufo/waves/round-41/c1"
cp "$clone/tools/round-40/sqfs-list.py" "$clone/tools/round-41/sqfs-list.py"
pin=$(python3 -c "import json,sys;print([c['sha256'] for c in json.load(open(sys.argv[1]))['carriers'] if c['id']=='L1'][0])" \
  "$clone/.ufo/waves/round-40/c1/carriers.json")
cat > "$clone/.ufo/waves/round-41/c1/carriers.json" <<JSON
{
 "claim": "R41-C1",
 "target": 4,
 "projection": "plus-extractor",
 "rea_parameters": {"max_depth": 1},
 "carriers": [
  {"id": "L1dev", "kind": "dev-sandbox", "path": "corpus/evidence/round-40/c1/L1/carrier.sqsh",
   "sha256": "$pin", "oracle": "corpus/evidence/round-40/c1/L1/oracle.tsv",
   "nonregular": "corpus/evidence/round-40/c1/L1/nonregular.tsv"}
 ]
}
JSON
git -C "$clone" add -A
git -C "$clone" -c user.name=fx -c user.email=fx@fx commit -q -m 'sandbox freeze'
freeze=$(git -C "$clone" rev-parse HEAD)
printf '# Round-41 sandbox entry (dev)\n\nsource: S127 — sandbox demo row, dev only\n' > "$clone/$ENTRY"
python3 - "$clone/corpus/SOURCES.md" "$ENTRY" <<'PY'
import sys
path, entry = sys.argv[1], sys.argv[2]
lines = open(path).read().splitlines(True)
last = max(i for i, l in enumerate(lines) if l.startswith('|'))
lines.insert(last + 1, '| S127 | sandbox demo row (dev only) | own-work | A | gate satisfiability check | '
                       'row inserted by sandbox-demo.sh | the round-41-shape SOURCES binding only | '
                       'sandbox | 2026-10-26 | n/a | %s |\n' % entry)
open(path, 'w').write(''.join(lines))
PY
cat >> "$clone/PROVINCE.md" <<MD
## Round-41 additions to Core

| surface | row (sandbox demo, dev) | entry |
|---|---|---|
| AVM-layout BE SquashFS v4 sandbox | gate satisfiability demo | \`$STEM\` |

Round-41 frontier note, 2026-10-26: the round-40 \`measured, not promoted\` record (\`## Round-40 measured, not promoted (R40-C1 honest stop)\`) is superseded for AVM-layout BE v4 by \`## Round-41 additions to Core\` (\`$STEM\`). Sandbox demo only.
MD
git -C "$clone" add -A
git -C "$clone" -c user.name=fx -c user.email=fx@fx commit -q -m 'sandbox landing'
rev=$(git -C "$clone" rev-parse HEAD)
echo "base=$base freeze=$freeze rev=$rev"
python3 -I -B "$gate" --root "$clone" --rev "$rev" --freeze "$freeze" --base "$base" \
  --work "$work" --json-out "$work/gate-demo.json"
