#!/bin/bash
# usage: measure.sh <tree-with-git> <base-tree> [diff-file]
set -u
T="$1"; B="$2"
echo "--- recipe A (tree)"; python3 /dev/shm/rv1/recipeA-tree.py "$T" | python3 -c "import json,sys;d=json.load(sys.stdin);print({k:v for k,v in d.items() if k!='rule_detail'});print('lastrule',d['rule_detail'][-1])"
echo "--- prior-13 byte-identity"; python3 - "$B/SKILL.md" "$T/SKILL.md" <<'PY'
import re,sys,hashlib
def rules(p):
    t=open(p,encoding='utf-8').read().split('## Queue-drain craft ',1)[1].split('\n## ',1)[0]
    return re.split(r'(?m)^- \*\*', t)[1:]
a,b=rules(sys.argv[1]),rules(sys.argv[2])
print('base_rules',len(a),'cand_rules',len(b))
print('prior13_byte_identical', all(x==y for x,y in zip(a,b[:13])))
print('sha_prior13_base', hashlib.sha256(''.join(a).encode()).hexdigest()[:16], 'sha_prior13_cand', hashlib.sha256(''.join(b[:13]).encode()).hexdigest()[:16])
PY
echo "--- census (HEAD v10)"; python3 /dev/shm/rv1/census-v10-head.py --root "$T" --quiet 2>&1 | tail -4; echo "census_exit=$?"
echo "--- citation-drift probe"; (cd "$T" && timeout 120 python3 "$T/.ufo/gates/citation-drift/citation-drift-probe.py" --root . --rev "$(git -C "$T" rev-parse HEAD)" --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json 2>&1 | tail -3); echo "probe_exit=$?"
