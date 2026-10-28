#!/usr/bin/env bash
S=/fast/scratch/hyaku/kaidoku-r49/C1DocCheck; export TMPDIR=$S HYAKU_SCRATCH=/fast/scratch/hyaku
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49
n=$1; python3 $S/mut.py $n >/dev/null || exit 9
mkdir -p $S/w-$n
cd $S; $R/draft/run-ctl.sh $S/clone $S/w-$n --controls pos --doc-dir $S/doc-$n > $S/w-$n/run.out 2>&1
echo "$n exit=$?"
