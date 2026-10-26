#!/usr/bin/env bash
# decoy-A2: duplicate 'REA MCP server' row (shadow-row mechanism isolated from
# the R3 range shift by compensating blank-line removal above '## Frontier').
set -euo pipefail
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=/fast/scratch/hyaku/kaidoku-r38/R38ReviewerPredicateIdentity
D="$S/fx-c2"
ART="$LANE/.ufo/waves/round-38/w1/artifacts/R38ReviewerPredicateIdentity"
BASEREV=$(git -C "$D" rev-parse decoyA^ 2>/dev/null || git -C "$D" rev-parse master 2>/dev/null || git -C "$D" rev-parse HEAD)
# base snapshot is the root commit of fx-c2
BASEREV=$(git -C "$D" rev-list --max-parents=0 HEAD)
git -C "$D" checkout -q -b decoyA2 "$BASEREV"
python3 -c "
p='$D/PROVINCE.md'
lines=open(p).read().splitlines()
i=[n for n,l in enumerate(lines) if 'REA MCP server' in l and l.lstrip().startswith('|')][0]
dup=lines[i].replace('\`evidence/doctor/\`','\`.ufo/waves/round-19/evidence/doctor/\`')
lines.insert(i+1,dup)
f=lines.index('## Frontier')
assert lines[f-1].strip()=='' , 'expected blank line before ## Frontier'
del lines[f-1]
open(p,'w').write('\n'.join(lines)+'\n')
print('inserted dup after line',i,'removed blank before Frontier')
"
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@invalid
git -C "$D" add -A && git -C "$D" commit -qm 'decoyA2: shadow duplicate row, Adjacent range compensated'
set +e
python3 -I -B "$LANE/tools/round-38/c2-counter.py" --root "$D" --rev "$(git -C "$D" rev-parse HEAD)" --base "$BASEREV" \
  --json-out "$ART/c2-decoy-A2.json" > "$ART/c2-decoy-A2.stdout" 2>&1
rc=$?
set -e
echo "decoy-A2 counter-exit=$rc"
