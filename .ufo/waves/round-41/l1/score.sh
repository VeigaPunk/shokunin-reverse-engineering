set -u
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
export TMPDIR=/fast/scratch/hyaku/kaidoku-r41/L1
M=e9a24d07256d1606f01aa4d2d65f74e649c5f3d4; F=d764389e9cbe61b9d1b07538ff3bff02d50bb34f
PK=/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents; O=.ufo/waves/round-41/l1/scores; CA=/fast/scratch/hyaku/kaidoku-r41/cache
mkdir -p $O
python3 -I -B tools/round-41/c2-counter.py --root . --rev $M --freeze $F --json-out $O/c2-at-e9a24d07.json > $O/c2-at-e9a24d07.stdout 2>&1; echo "c2 exit=$?"
python3 -I -B tools/round-41/c1-counter.py --root . --rev $M --freeze $F --pkg65 $PK --carrier-cache $CA --json-out $O/c1-at-e9a24d07.json > $O/c1-at-e9a24d07.stdout 2>&1; echo "c1 exit=$?"
python3 -I -B tools/round-41/c1-extra.py --root . --rev $M --freeze $F --base 49096c7e6f226af0c750c4b003be58883cb6049f --carrier-cache $CA --json-out $O/c1-extra-at-e9a24d07.json > $O/c1-extra-at-e9a24d07.stdout 2>&1; echo "extra exit=$?"
