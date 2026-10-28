#!/usr/bin/env bash
export TMPDIR=/fast/scratch/hyaku/kaidoku-r49/W2Plan HYAKU_SCRATCH=/fast/scratch/hyaku GIT_NO_REPLACE_OBJECTS=1
S=/fast/scratch/hyaku/kaidoku-r49/W2Plan; L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
R=29883d4ec35a31a8393c4ffb220888c44c0bb022; F=decc5697bfd4ec1e9de4a762ad199d9bd9c4230d
P=/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
cd $S
python3 -I -B frz/tools/round-49/c1-counter.py --root $L --rev $R --freeze $F --pkg65 $P --work $S/w-rev --json-out $S/arts/c1-rev.json > arts/c1-rev.stdout 2> arts/c1-rev.stderr; echo "c1-rev exit=$?" >> arts/exits.txt
python3 -I -B frz/tools/round-49/c1-counter.py --root $L --rev $F --freeze $F --pkg65 $P --work $S/w-frz --json-out $S/arts/c1-frz.json > arts/c1-frz.stdout 2> arts/c1-frz.stderr; echo "c1-frz exit=$?" >> arts/exits.txt
python3 -I -B frz/tools/round-49/c2-mismatch.py --root $L --rev $R --freeze $F --battery --json-out $S/arts/c2-rev-battery.json > arts/c2-rev-battery.stdout 2> arts/c2-rev-battery.stderr; echo "c2-rev-battery exit=$?" >> arts/exits.txt
python3 -I -B frz/tools/round-49/c2-mismatch.py --root $L --rev $R --freeze $F --json-out $S/arts/c2-rev.json > arts/c2-rev.stdout 2> arts/c2-rev.stderr; echo "c2-rev exit=$?" >> arts/exits.txt
python3 -I -B frz/tools/round-49/c2-mismatch.py --root $L --rev $F --freeze $F --json-out $S/arts/c2-frz.json > arts/c2-frz.stdout 2> arts/c2-frz.stderr; echo "c2-frz exit=$?" >> arts/exits.txt
echo ALLDONE >> arts/exits.txt
