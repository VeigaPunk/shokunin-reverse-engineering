#!/bin/bash
# RV-12: run the full fragility battery on one pointer table.
# usage: rv12-run-all.sh <table.json> <prefix>
set -u
TABLE="$1"; PREFIX="$2"; D=/var/tmp/rv12
python3 $D/rv12-fragility.py --table "$TABLE" --out $D/$PREFIX-fragility.json >/dev/null 2>&1
python3 $D/rv12-churn.py --table "$TABLE" --out $D/$PREFIX-churn.json >/dev/null 2>&1
python3 $D/rv12-simrepo.py "$TABLE" >$D/$PREFIX-simrepo.log 2>&1
cp $D/scenarios.json $D/$PREFIX-scenarios.json
python3 $D/rv12-rename.py "$TABLE" >$D/$PREFIX-rename.log 2>&1
cp $D/rename-scenarios.json $D/$PREFIX-rename.json
echo "battery done: $PREFIX"
tail -4 $D/$PREFIX-simrepo.log
tail -6 $D/$PREFIX-rename.log