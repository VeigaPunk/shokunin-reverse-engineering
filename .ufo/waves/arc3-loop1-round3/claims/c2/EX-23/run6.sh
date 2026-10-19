#!/usr/bin/env bash
# EX-23 run6: stripped-marker attacks — can a receipt without the error marker still fail open?
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
mkdir -p $S/work/strip
# t1: strip the STAT-ERROR line from a blocked receipt -> what does verify say against LIVE (still blocked)?
sed '/^STAT-ERROR:/d' $S/work/a/a-rec-A.txt > $S/work/strip/stripped-A.txt
echo "## stripped receipt stanza:"; tail -3 $S/work/strip/stripped-A.txt
chmod 000 $S/work/a/noaccess
run t1-stripped-vs-live-blocked python3 $TA verify $S/work/strip/stripped-A.txt --live
run t2-stripped-vs-stripped     python3 $TA verify $S/work/strip/stripped-A.txt $S/work/strip/stripped-A.txt
chmod 755 $S/work/a/noaccess
# t3: blocked receipt vs genuinely-absent live path (ref unevaluable, cand ENOENT)
run t3-blocked-vs-absent-live   python3 $TA verify $S/work/a/a-rec-A.txt --live
# t4: stripped receipt vs genuinely-absent live path -> both read "absent", no marker anywhere
mkdir -p $S/work/strip/empty
printf 'PATH: %s\nEXISTS: no\n' "$S/work/strip/empty/gone.conf" > $S/work/strip/absent-hand.txt
run t4-handabsent-vs-live       python3 $TA verify $S/work/strip/absent-hand.txt --live
