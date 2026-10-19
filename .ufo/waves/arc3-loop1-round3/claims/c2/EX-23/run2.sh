#!/usr/bin/env bash
# EX-23 differential harness: before-rev on the identical fixture + cross-revision + attacks.
S=/var/tmp/ex23-after
TB=$S/tool/custody-pair.before.py
TA=$S/tool/custody-pair.py
O=$S/out
run() {
  name=$1; shift
  { echo "# cwd=$S"; echo "\$ $*"; } > $O/$name.txt
  "$@" >> $O/$name.txt 2>&1
  rc=$?
  echo "[exit-status] $rc" >> $O/$name.txt
  echo "== $name rc=$rc"
}

# --- differential: BEFORE rev, identical fixture shape, blocked parent dir
cd $S
mkdir -p $S/work/d/noaccess && printf 'secret-bytes-D\n' > $S/work/d/noaccess/secret.conf
chmod 000 $S/work/d/noaccess
run d-before-capture python3 $TB capture --out $S/work/d/d-rec-A.txt --paths $S/work/d/noaccess/secret.conf
run d-before-verify-live python3 $TB verify $S/work/d/d-rec-A.txt --live
run d-before-capture-B python3 $TB capture --out $S/work/d/d-rec-B.txt --paths $S/work/d/noaccess/secret.conf
run d-before-verify-pair python3 $TB verify $S/work/d/d-rec-A.txt $S/work/d/d-rec-B.txt
chmod 755 $S/work/d/noaccess

# --- cross-revision: EX-22's before-state artifact receipt fed to the REVISED tool
E=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c2/EX-22/transcripts/artifact-a-rec-A-receipt.txt
run x1-revised-verify-ex22artifact python3 $TA verify $E --live
run x1-revised-verify-ex22artifact-pair python3 $TA verify $E $E
run x1-before-verify-ex22artifact python3 $TB verify $E --live
