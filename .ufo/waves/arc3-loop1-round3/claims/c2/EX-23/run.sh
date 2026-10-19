#!/usr/bin/env bash
# EX-23 after-state EACCES fixture harness. Transcripts: cwd=, $ argv, combined out, [exit-status].
S=/var/tmp/ex23-after
T=$S/tool/custody-pair.py
O=$S/out
run() {
  name=$1; shift
  { echo "# cwd=$S"; echo "\$ $*"; } > $O/$name.txt
  "$@" >> $O/$name.txt 2>&1
  rc=$?
  echo "[exit-status] $rc" >> $O/$name.txt
  echo "== $name rc=$rc"
}
cd $S
run a2-capture-eacces python3 $T capture --out $S/work/a/a-rec-A.txt --paths $S/work/a/noaccess/secret.conf
run a3-verify-live  python3 $T verify $S/work/a/a-rec-A.txt --live
run a4-capture-B    python3 $T capture --out $S/work/a/a-rec-B.txt --paths $S/work/a/noaccess/secret.conf
run a5-verify-pair  python3 $T verify $S/work/a/a-rec-A.txt $S/work/a/a-rec-B.txt
echo "== fixture restored"
chmod 755 $S/work/a/noaccess
stat -c 'name=%n inode=%i size=%s mtime=%Y' $S/work/a/noaccess/secret.conf >> $O/a7-post-stat.txt
sha256sum $S/work/a/noaccess/secret.conf >> $O/a7-post-sha256.txt
cat $O/a7-post-stat.txt; cat $O/a7-post-sha256.txt
