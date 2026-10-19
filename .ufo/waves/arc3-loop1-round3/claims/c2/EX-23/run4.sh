#!/usr/bin/env bash
# EX-23 run4: clean parser-arm live proof, file-mode-000 EACCES shape, identity + read-only attestation.
S=/var/tmp/ex23-after
TB=$S/tool/custody-pair.before.py
TA=$S/tool/custody-pair.py
MUT=$S/tool/custody-pair.mut-noparser.py
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

# --- A11c: parser-arm proof in LIVE mode, with the parent dir blocked again
chmod 000 $S/work/a/noaccess
run a11c-mut-noparser-verify-live-blocked python3 $MUT verify $S/work/a/a-rec-A.txt --live
run a11d-revised-verify-live-blocked      python3 $TA  verify $S/work/a/a-rec-A.txt --live
chmod 755 $S/work/a/noaccess

# --- B: file-mode-000 shape (dir traversable, lstat OK, sha256 read EACCES) = D2b
mkdir -p $S/work/b2
printf 'secret-bytes-B2\n' > $S/work/b2/perm.conf
chmod 000 $S/work/b2/perm.conf
stat -c 'name=%n inode=%i size=%s mode=%a' $S/work/b2/perm.conf > $O/b2-pre-stat.txt
run b2-capture-file000        python3 $TA capture --out $S/work/b2/b2-rec-A.txt --paths $S/work/b2/perm.conf
run b2-verify-live            python3 $TA verify $S/work/b2/b2-rec-A.txt --live
run b2-capture-file000-B      python3 $TA capture --out $S/work/b2/b2-rec-B.txt --paths $S/work/b2/perm.conf
run b2-verify-pair            python3 $TA verify $S/work/b2/b2-rec-A.txt $S/work/b2/b2-rec-B.txt
run b2-before-capture-file000 python3 $TB capture --out $S/work/b2/b2-before-rec.txt --paths $S/work/b2/perm.conf
run b2-before-verify-live     python3 $TB verify $S/work/b2/b2-before-rec.txt --live
chmod 644 $S/work/b2/perm.conf
run b2-post-capture-readable  python3 $TA capture --out $S/work/b2/b2-rec-clean.txt --paths $S/work/b2/perm.conf
run b2-blocked-vs-clean       python3 $TA verify $S/work/b2/b2-rec-A.txt $S/work/b2/b2-rec-clean.txt

# --- identity re-derivation (rule #14), post-run
{
  echo "# identity re-derivation — seat EX-23, after-state EACCES fixture"
  echo "\$ date -u +%Y-%m-%dT%H:%M:%SZ"; date -u +%Y-%m-%dT%H:%M:%SZ
  echo "\$ git rev-parse HEAD"; git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD
  echo "\$ sha256sum <repo tool> <repo README> <scratch after copy> <scratch before copy> <scratch mut copy>"
  sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py \
           /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/README.md \
           $TA $TB $MUT
  echo "\$ stat -c '%n size=%s mtime=%Y mode=%a' <repo tool> <repo README>"
  stat -c '%n size=%s mtime=%Y mode=%a' \
           /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py \
           /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/README.md
  echo "\$ git cat-file -p HEAD:.ufo/gates/custody-pair/custody-pair.py | sha256sum"
  git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -p HEAD:.ufo/gates/custody-pair/custody-pair.py | sha256sum
  echo "\$ git status --short .ufo/gates/custody-pair/"
  git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --short .ufo/gates/custody-pair/
  echo "\$ grep -n 'self-pinned tool sha' <after receipts>"
  grep -H '# tool:' $S/work/a/a-rec-A.txt $S/work/a/a-rec-B.txt $S/work/b2/b2-rec-A.txt
} > $O/identity-after.txt 2>&1
cat $O/identity-after.txt

# --- read-only attestation on the 5 canonical custody paths (capture only, to scratch)
run ro1-capture-pre  python3 $TA capture --out $S/work/ro-pre.txt  --label ex23-readonly-attestation-pre
run ro2-capture-post python3 $TA capture --out $S/work/ro-post.txt --label ex23-readonly-attestation-post
run ro3-verify-pair  python3 $TA verify $S/work/ro-pre.txt $S/work/ro-post.txt

# --- traceback sweep across every after-state transcript
echo "## traceback sweep (after-state, revised tool)" > $O/traceback-sweep.txt
for f in $O/*.txt; do n=$(grep -c 'Traceback' $f); echo "$n  $(basename $f)" >> $O/traceback-sweep.txt; done
sort -rn $O/traceback-sweep.txt | head -20
