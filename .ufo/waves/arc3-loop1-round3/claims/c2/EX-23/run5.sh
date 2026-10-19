#!/usr/bin/env bash
# EX-23 run5: negative-space sweep — hunt for ANY revised-tool invocation that returns MATCH exit 0
# on the EACCES fixture. Any rc==0 found here is a counterexample to the claim.
S=/var/tmp/ex23-after
TA=$S/tool/custody-pair.py
O=$S/out
run() {
  name=$1; shift
  { echo "# cwd=$S"; echo "\$ $*"; } > $O/$name.txt
  "$@" >> $O/$name.txt 2>&1
  rc=$?
  echo "[exit-status] $rc" >> $O/$name.txt
  echo "rc=$rc  $name"
}
cd $S
chmod 000 $S/work/a/noaccess

run s01-verify-live                 python3 $TA verify $S/work/a/a-rec-A.txt --live
run s02-verify-live-require5        python3 $TA verify $S/work/a/a-rec-A.txt --live --require-paths 5
run s03-verify-live-require1        python3 $TA verify $S/work/a/a-rec-A.txt --live --require-paths 1
run s04-verify-pair-rev             python3 $TA verify $S/work/a/a-rec-B.txt $S/work/a/a-rec-A.txt
run s05-verify-self                 python3 $TA verify $S/work/a/a-rec-A.txt $S/work/a/a-rec-A.txt
run s06-verify-ex22artifact-pair    python3 $TA verify /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c2/EX-22/transcripts/artifact-a-rec-A-receipt.txt $S/work/a/a-rec-A.txt
run s07-capture-stdout              python3 $TA capture --out - --paths $S/work/a/noaccess/secret.conf
run s08-capture-ex22artifact-vs-new python3 $TA verify /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c2/EX-22/transcripts/artifact-a-rec-A-receipt.txt --live
chmod 755 $S/work/a/noaccess

echo "## NEGATIVE-SPACE SWEEP: any rc==0 is a counterexample" > $O/sweep-summary.txt
for f in $O/s0*.txt; do printf '%s  %s\n' "$(grep -o '^\[exit-status\] [0-9]*' $f | tail -1)" "$(basename $f)" >> $O/sweep-summary.txt; done
cat $O/sweep-summary.txt
echo "## MATCH verdicts found:"; grep -l 'VERDICT: MATCH' $O/s0*.txt || echo "(none)"
