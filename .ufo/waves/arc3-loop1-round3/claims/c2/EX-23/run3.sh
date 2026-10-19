#!/usr/bin/env bash
# EX-23 attack battery: controls, parser-arm proof, mutation, identity.
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
cd $S

# --- A2 control: readable file on the same tool -> must be MATCH 0 (no over-refusal)
printf 'readable-control\n' > $S/work/ctl/readable.conf
run a8-capture-readable python3 $TA capture --out $S/work/ctl/ctl-rec.txt --paths $S/work/ctl/readable.conf
run a8b-verify-readable-live python3 $TA verify $S/work/ctl/ctl-rec.txt --live

# --- A3 control: genuinely absent path -> ABSENT 13, not swallowed by 14
run a9-capture-absent python3 $TA capture --out $S/work/ctl/abs-rec.txt --paths $S/work/ctl/does-not-exist.conf
run a9b-verify-absent-live python3 $TA verify $S/work/ctl/abs-rec.txt --live

# --- A4 parser-arm proof: fixture readable again, cross-pair blocked-vs-clean and clean-vs-blocked
printf 'secret-bytes-A\n' > $S/work/a/noaccess/secret.conf   # same bytes as the blocked receipt measured
run a10-capture-clean python3 $TA capture --out $S/work/a/a-rec-clean.txt --paths $S/work/a/noaccess/secret.conf
run a10b-blocked-vs-clean python3 $TA verify $S/work/a/a-rec-A.txt $S/work/a/a-rec-clean.txt
run a10c-clean-vs-blocked python3 $TA verify $S/work/a/a-rec-clean.txt $S/work/a/a-rec-A.txt
run a10d-before-blocked-vs-clean python3 $TB verify $S/work/a/a-rec-A.txt $S/work/a/a-rec-clean.txt

# --- A5 mutation: revert the parser arms in a scratch copy -> does the fail-open return?
python3 - <<'PY'
from pathlib import Path
src = Path('/var/tmp/ex23-after/tool/custody-pair.py').read_text()
mut = src.replace('''    "stat_error": re.compile(r"^STAT-ERROR:\\s*(.+?)\\s*$", re.M),
    "read_error": re.compile(r"^READ-ERROR:\\s*(.+?)\\s*$", re.M),''',
'''    "stat_error": re.compile(r"^ZZSTAT-ERROR:\\s*(.+?)\\s*$", re.M),
    "read_error": re.compile(r"^ZZREAD-ERROR:\\s*(.+?)\\s*$", re.M),''')
assert mut != src, "mutation did not apply"
Path('/var/tmp/ex23-after/tool/custody-pair.mut-noparser.py').write_text(mut)
print("mutation written")
PY
run a11-mut-noparser-verify-pair python3 $S/tool/custody-pair.mut-noparser.py verify $S/work/a/a-rec-A.txt $S/work/a/a-rec-B.txt
run a11b-mut-noparser-verify-live python3 $S/tool/custody-pair.mut-noparser.py verify $S/work/a/a-rec-A.txt --live
