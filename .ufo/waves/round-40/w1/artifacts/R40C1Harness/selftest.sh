#!/usr/bin/env bash
# R40-C1 harness selftest: exercises c1-run.sh (after|oracle) and
# mk-carriers.py.
#
# Inputs are DEVELOPMENT only: round-37 K1/K4 copies (standard BE), the
# retained genuine AVM-BE fixture round11/work/avm-be.squashfs (read-only,
# copied), the round13 LE fixture (negative), and lane-built genuine AVM-layout
# images generated here with the round-40 writer (--endian avm-genuine).
# REA/ unblob are run on those copies only; no C1 carrier and no C2 held-out
# envelope is built or run. Scratch lives under $HYAKU_SCRATCH/kaidoku-r40 and
# is removed on exit unless SELFTEST_KEEP=1.
#
#   ./selftest.sh                       one JSON tally on stdout
#   SELFTEST_KEEP=1 ./selftest.sh       keep the scratch tree (receipts)
#   GEN=/path/gen-squashfs.py ./selftest.sh
#
# Exit: 0 all cases pass, 1 any case failed, 2 environment problem.
set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
LANE=${LANE:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
HY=${HYAKU_SCRATCH:-/fast/scratch/hyaku}
S=${SELFTEST_SCRATCH:-$HY/kaidoku-r40/c1-selftest.$$}
mkdir -p "$S" || { echo "selftest: cannot create scratch $S" >&2; exit 2; }
S=$(realpath -- "$S")
cleanup() {
  [[ ${SELFTEST_KEEP:-0} == 1 ]] || rm -rf -- "$S"
}
trap cleanup EXIT
export HYAKU_SCRATCH=$S/hy
mkdir -p "$HYAKU_SCRATCH"
export TMPDIR=$S

CR=$HERE/c1-run.sh
MK=$HERE/mk-carriers.py
TD=$HERE/test-double-sqfs-list.py
READER=${READER:-}
if [[ -z $READER ]]; then
  for cand in "$LANE/tools/round-40/sqfs-list.py" \
              "$LANE/.ufo/waves/round-40/w1/artifacts/R40C1Reader/sqfs-list.py"; do
    [[ -f $cand ]] && { READER=$cand; break; }
  done
fi
[[ -n $READER ]] || READER=$TD
for f in "$CR" "$MK" "$TD" "$READER"; do
  [[ -x $f ]] || { echo "selftest: missing $f" >&2; exit 2; }
done
command -v jq >/dev/null || { echo "selftest: jq missing" >&2; exit 2; }
command -v sasquatch-v4be >/dev/null || { echo "selftest: sasquatch-v4be missing" >&2; exit 2; }
command -v npx >/dev/null || { echo "selftest: npx missing" >&2; exit 2; }
command -v unblob >/dev/null || { echo "selftest: unblob missing" >&2; exit 2; }

R37=$LANE/corpus/evidence/round-37/c1
GEN=${GEN:-}
if [[ -z $GEN ]]; then
  for cand in "$LANE/tools/round-40/gen-squashfs.py" \
              "$LANE/.ufo/waves/round-40/w1/artifacts/R40C1AvmWriter/gen-squashfs.py"; do
    [[ -f $cand ]] && { GEN=$cand; break; }
  done
fi
[[ -n $GEN && -f $GEN ]] || { echo "selftest: round-40 gen-squashfs.py not found (set GEN)" >&2; exit 2; }
AVM_BE_FIXTURE=${AVM_BE_FIXTURE:-/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/avm-be.squashfs}
LE_FIXTURE=${LE_FIXTURE:-/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/avm-le-genuine.squashfs}
for f in "$R37/K1/carrier.sqsh" "$R37/K4/carrier.bin" "$AVM_BE_FIXTURE" "$LE_FIXTURE"; do
  [[ -f $f ]] || { echo "selftest: fixture missing: $f" >&2; exit 2; }
done

mkdir -p "$S/fx" "$S/out" "$S/fakes"
cp -f "$R37/K1/carrier.sqsh" "$S/fx/K1.sqsh"
cp -f "$R37/K4/carrier.bin" "$S/fx/K4.bin"
cp -f "$AVM_BE_FIXTURE" "$S/fx/avm-dev.squashfs"
cp -f "$LE_FIXTURE" "$S/fx/le-dev.squashfs"

# Development trees + lane-built genuine AVM-layout images (LE block-length
# headers, BE fields, marker) for the oracle arm.
mkdir -p "$S/tree1/bin" "$S/tree1/etc" "$S/tree1/docs/deep"
printf '#!/bin/sh\necho run\n' > "$S/tree1/bin/run"
printf 'alpha\n' > "$S/tree1/etc/a.txt"
printf 'beta\n' > "$S/tree1/etc/b.txt"
ln -s ../etc/a.txt "$S/tree1/docs/deep/link-in"
ln -s ../../../etc/passwd "$S/tree1/docs/deep/link-out"
python3 - "$S/tree2" <<'PY'
import os, sys
root = sys.argv[1]
os.makedirs(os.path.join(root, 'bulk'), exist_ok=True)
with open(os.path.join(root, 'bulk', 'blob.bin'), 'wb') as fh:
    fh.write(bytes((i * 37) & 0xFF for i in range(20000)))
PY
gen() { python3 -I -- "$GEN" --endian avm-genuine --comp "$2" "$1" "$3" >/dev/null; }
gen "$S/tree1" gzip "$S/fx/avm-gzip.sqsh"
gen "$S/tree1" xz "$S/fx/avm-xz.sqsh"
gen "$S/tree2" gzip "$S/fx/avm-multi-gzip.sqsh"

# Fake readers: isolate harness clauses that the double cannot fail.
cat > "$S/fakes/bad-tables.py" <<'PY'
#!/usr/bin/env python3
import argparse, sys
ap = argparse.ArgumentParser()
ap.add_argument('--layout'); ap.add_argument('--files'); ap.add_argument('--nonregular')
ap.add_argument('--inspect', action='store_true'); ap.add_argument('image')
a = ap.parse_args()
open(a.files, 'w').write('z.txt\tNOTHEX\t1\n')
open(a.nonregular, 'w').write('')
print('{}')
PY
cat > "$S/fakes/no-oracle.py" <<'PY'
#!/usr/bin/env python3
import argparse
ap = argparse.ArgumentParser()
ap.add_argument('--layout'); ap.add_argument('--files'); ap.add_argument('--nonregular')
ap.add_argument('--inspect', action='store_true'); ap.add_argument('image')
a = ap.parse_args()
open(a.nonregular, 'w').write('')
print('{}')
PY
cat > "$S/fakes/exit1.py" <<'PY'
#!/usr/bin/env python3
import argparse, sys
ap = argparse.ArgumentParser()
ap.add_argument('--layout'); ap.add_argument('--files'); ap.add_argument('--nonregular')
ap.add_argument('--inspect', action='store_true'); ap.add_argument('image')
ap.parse_args()
sys.stderr.write('fake reader: cannot decode\n')
sys.exit(1)
PY
cat > "$S/fakes/offset-reader.py" <<'PY'
#!/usr/bin/env python3
"""Test double for an image with leading bytes: strips them and delegates."""
import argparse, json, os, shutil, subprocess, sys, tempfile
ap = argparse.ArgumentParser(description='offset double; --layout --files --nonregular --inspect')
ap.add_argument('--layout'); ap.add_argument('--files'); ap.add_argument('--nonregular')
ap.add_argument('--inspect', action='store_true'); ap.add_argument('image')
a = ap.parse_args()
raw = open(a.image, 'rb').read()
off = raw.find(b'sqsh')
if off < 0:
    sys.exit(2)
tmp = tempfile.mkdtemp(prefix='td-offset.')
try:
    stripped = os.path.join(tmp, 'img.sqsh')
    open(stripped, 'wb').write(raw[off:])
    r = subprocess.run([sys.executable, '-I', os.environ['OFFSET_TD'], '--layout', 'avm',
                        '--files', a.files, '--nonregular', a.nonregular,
                        '--inspect', stripped], stdout=subprocess.PIPE)
    if r.returncode != 0:
        sys.exit(r.returncode)
    if a.inspect:
        data = json.loads(r.stdout.decode() or '{}')
        data['offset'] = off
        print(json.dumps(data))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
PY
cat > "$S/fakes/bad-inspect.py" <<'PY'
#!/usr/bin/env python3
import argparse, os, shutil
ap = argparse.ArgumentParser()
ap.add_argument('--layout'); ap.add_argument('--files'); ap.add_argument('--nonregular')
ap.add_argument('--inspect', action='store_true'); ap.add_argument('image')
a = ap.parse_args()
shutil.copy(os.environ['GOOD_ORACLE'], a.files)
open(a.nonregular, 'w').write('')
print('this is not json')
PY
cat > "$S/fakes/wrong-sha.py" <<'PY'
#!/usr/bin/env python3
import argparse, os
ap = argparse.ArgumentParser()
ap.add_argument('--layout'); ap.add_argument('--files'); ap.add_argument('--nonregular')
ap.add_argument('--inspect', action='store_true'); ap.add_argument('image')
a = ap.parse_args()
rows = open(os.environ['GOOD_ORACLE']).read().splitlines()
rel, sha, size = rows[0].split('\t')
sha = ('0' if sha[0] != '0' else '1') + sha[1:]
rows[0] = '\t'.join((rel, sha, size))
open(a.files, 'w').write('\n'.join(rows) + '\n')
open(a.nonregular, 'w').write('')
print('{}')
PY
cat > "$S/fakes/no-flags.py" <<'PY'
#!/usr/bin/env python3
import sys
print('this --help advertises nothing useful')
sys.exit(0)
PY
chmod +x "$S"/fakes/*.py

results=$S/results.jsonl
: > "$results"
fails=0
record() { # name want got
  jq -nc --arg n "$1" --arg w "$2" --arg g "$3" \
    '{name: $n, want: $w, got: $g, ok: ($w == $g)}' >> "$results"
  [[ $2 == "$3" ]] || { fails=$((fails + 1)); printf 'FAIL %s want=%s got=%s\n' "$1" "$2" "$3" >&2; }
}
run_case() { # name want-exit command...
  local name=$1 want=$2 rc
  shift 2
  set +e
  "$@" >"$S/last.out" 2>"$S/last.err"
  rc=$?
  set -e
  record "$name" "$want" "$rc"
  if [[ $rc != "$want" ]]; then
    sed -n '1,3p' "$S/last.err" | cut -c1-240 >&2
  fi
}
jget() { jq -r "$1" "$2" 2>/dev/null || true; }
jcase() { # name jq-file expr want-string
  local got
  got=$(jget "$3" "$2")
  record "$1" "$4" "$got"
}

# ---------------------------------------------------------------- usage/env
run_case usage-no-args 2 "$CR"
run_case usage-bad-mode 2 "$CR" bridge "$S/fx/K1.sqsh" "$S/out/x"
run_case usage-two-args 2 "$CR" after "$S/fx/K1.sqsh"
run_case usage-five-args 2 "$CR" after "$S/fx/K1.sqsh" "$S/out/x" "$S/a" extra
run_case usage-missing-carrier 2 "$CR" oracle "$S/fx/nope.sqsh" "$S/out/x"
chmod 000 "$S/fx/K1.sqsh"
run_case usage-unreadable-carrier 2 "$CR" oracle "$S/fx/K1.sqsh" "$S/out/x"
chmod 644 "$S/fx/K1.sqsh"
run_case usage-foreign-scratch 2 env C1_READER="$READER" "$CR" oracle "$S/fx/avm-dev.squashfs" "$S/out/x" /tmp/r40h-foreign.$$
run_case usage-oracle-missing-reader 2 env C1_READER="$S/fx/nope.py" "$CR" oracle "$S/fx/avm-dev.squashfs" "$S/out/x"
run_case usage-oracle-no-flags 2 env C1_READER="$S/fakes/no-flags.py" "$CR" oracle "$S/fx/avm-dev.squashfs" "$S/out/x"
run_case usage-oracle-le-carrier 2 env C1_READER="$READER" "$CR" oracle "$S/fx/le-dev.squashfs" "$S/out/x"
printf 'not a filesystem\n' > "$S/fx/garbage.bin"
run_case usage-oracle-no-magic 2 env C1_READER="$READER" "$CR" oracle "$S/fx/garbage.bin" "$S/out/x"
run_case usage-after-no-sasquatch 2 env \
  PATH=$(printf '%s' "$PATH" | tr ':' '\n' | grep -v "^$HOME/.local/bin$" | paste -sd:) \
  REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob "$CR" after "$S/fx/K1.sqsh" "$S/out/x"
run_case usage-after-missing-unblob 2 env REA_UNBLOB_COMMAND=/nonexistent/unblob "$CR" after "$S/fx/K1.sqsh" "$S/out/x"

# ------------------------------------------------------------- oracle arm
export C1_READER=$READER
run_case oracle-avm-dev 0 "$CR" oracle "$S/fx/avm-dev.squashfs" "$S/out/oracle-avm-dev"
jcase oracle-avm-dev-schema "$S/out/oracle-avm-dev/oracle-run.json" '.schema' kaidoku-r40-c1-run-v1
jcase oracle-avm-dev-mode "$S/out/oracle-avm-dev/oracle-run.json" '.mode' oracle
jcase oracle-avm-dev-claim "$S/out/oracle-avm-dev/oracle-run.json" '.claim' R40-C1
jcase oracle-avm-dev-layout "$S/out/oracle-avm-dev/oracle-run.json" '.layout' avm
jcase oracle-avm-dev-magic "$S/out/oracle-avm-dev/oracle-run.json" '.magic' sqsh
jcase oracle-avm-dev-offset "$S/out/oracle-avm-dev/oracle-run.json" '.squashfs_offset' 0
jcase oracle-avm-dev-files "$S/out/oracle-avm-dev/oracle-run.json" '.tables.oracle_files' 4
jcase oracle-avm-dev-cross-equal "$S/out/oracle-avm-dev/oracle-run.json" '.crosscheck.files_equal' true
jcase oracle-avm-dev-cross-zero "$S/out/oracle-avm-dev/oracle-run.json" '.crosscheck.mismatch_count' 0
jcase oracle-avm-dev-sq-exit "$S/out/oracle-avm-dev/oracle-run.json" '.sasquatch_v4be.exit' 0
jcase oracle-avm-dev-no-be-flag "$S/out/oracle-avm-dev/oracle-run.json" '[.sasquatch_v4be.argv[] | select(. == "-be")] | length' 0
jcase oracle-avm-dev-reader-exit "$S/out/oracle-avm-dev/oracle-run.json" '.reader.exit' 0
jcase oracle-avm-dev-bytes "$S/out/oracle-avm-dev/oracle-run.json" '.outputs.oracle_tsv.bytes' 312

run_case oracle-avm-gzip 0 "$CR" oracle "$S/fx/avm-gzip.sqsh" "$S/out/oracle-avm-gzip"
jcase oracle-avm-gzip-files "$S/out/oracle-avm-gzip/oracle-run.json" '.tables.oracle_files' 3
jcase oracle-avm-gzip-nonreg "$S/out/oracle-avm-gzip/oracle-run.json" '.tables.nonregular_entries' 6
jcase oracle-avm-gzip-symlinks "$S/out/oracle-avm-gzip/oracle-run.json" '.tables.nonregular_by_kind.symlink' 2
jcase oracle-avm-gzip-cross "$S/out/oracle-avm-gzip/oracle-run.json" '.crosscheck.files_equal' true
run_case oracle-avm-xz 0 "$CR" oracle "$S/fx/avm-xz.sqsh" "$S/out/oracle-avm-xz"
run_case oracle-avm-multiblock 0 "$CR" oracle "$S/fx/avm-multi-gzip.sqsh" "$S/out/oracle-avm-multi"
jcase oracle-avm-multi-files "$S/out/oracle-avm-multi/oracle-run.json" '.tables.oracle_files' 1

# offset carrier: 4 leading bytes must be found, -o passed to sasquatch
python3 - "$S/fx/avm-gzip.sqsh" "$S/fx/avm-gzip-offset.bin" <<'PY'
import sys
data = open(sys.argv[1], 'rb').read()
open(sys.argv[2], 'wb').write(b'\x00\x01\x02\x03' + data)
PY
export OFFSET_TD=$READER
run_case oracle-offset 0 env C1_READER="$S/fakes/offset-reader.py" \
  "$CR" oracle "$S/fx/avm-gzip-offset.bin" "$S/out/oracle-offset"
jcase oracle-offset-found "$S/out/oracle-offset/oracle-run.json" '.squashfs_offset' 4
jcase oracle-offset-o-flag "$S/out/oracle-offset/oracle-run.json" '[.sasquatch_v4be.argv[] | select(. == "-o")] | length' 1

# standard BE and marker-only BE are not AVM layout: the extractor refuses them
run_case oracle-standard-be-K1 3 "$CR" oracle "$S/fx/K1.sqsh" "$S/out/oracle-K1"
jcase oracle-standard-be-K1-files "$S/out/oracle-K1/oracle-run.json" '.tables' null
python3 -I -- "$GEN" --endian avm --comp gzip "$S/tree1" "$S/fx/marker-only.sqsh" >/dev/null
run_case oracle-marker-only 3 "$CR" oracle "$S/fx/marker-only.sqsh" "$S/out/oracle-marker-only"

# hostile readers
run_case oracle-reader-exit1 3 env C1_READER="$S/fakes/exit1.py" "$CR" oracle "$S/fx/avm-dev.squashfs" "$S/out/x-reader1"
jcase oracle-reader-exit1-error "$S/out/x-reader1/oracle-run.json" '.error' reader_failed
run_case oracle-bad-tables 3 env C1_READER="$S/fakes/bad-tables.py" "$CR" oracle "$S/fx/avm-dev.squashfs" "$S/out/x-badtables"
run_case oracle-no-oracle 3 env C1_READER="$S/fakes/no-oracle.py" "$CR" oracle "$S/fx/avm-dev.squashfs" "$S/out/x-nooracle"
GOOD_ORACLE=$S/out/oracle-avm-dev/oracle.tsv
export GOOD_ORACLE
run_case oracle-bad-inspect 3 env C1_READER="$S/fakes/bad-inspect.py" "$CR" oracle "$S/fx/avm-dev.squashfs" "$S/out/x-badinspect"
run_case oracle-wrong-sha 3 env C1_READER="$S/fakes/wrong-sha.py" "$CR" oracle "$S/fx/avm-dev.squashfs" "$S/out/x-wrongsha"
jcase oracle-wrong-sha-count "$S/out/x-wrongsha/oracle-run.json" '.crosscheck.mismatch_count' 1

# foreign scratch allowed on request (dev only), provenance flag false
run_case oracle-foreign-allowed 0 env C1_ALLOW_FOREIGN_SCRATCH=1 \
  "$CR" oracle "$S/fx/avm-dev.squashfs" "$S/out/x-foreign" /tmp/r40h-foreign-ok.$$
jcase oracle-foreign-flag "$S/out/x-foreign/oracle-run.json" '.run_provenance_segment_ok' false
rm -rf -- /tmp/r40h-foreign.$$ /tmp/r40h-foreign-ok.$$

# default scratch is under the /kaidoku-r40/ segment
unset C1_READER
run_case oracle-default-scratch 0 env C1_READER="$READER" "$CR" oracle "$S/fx/avm-dev.squashfs" "$S/out/oracle-default"
jcase oracle-default-segment "$S/out/oracle-default/oracle-run.json" '.run_provenance_segment_ok' true

# -------------------------------------------------------------- after arm
export REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob
run_case after-avm-dev 0 "$CR" after "$S/fx/avm-dev.squashfs" "$S/out/after-avm"
jcase after-avm-schema "$S/out/after-avm/run.json" '.schema' kaidoku-r40-c1-run-v1
jcase after-avm-claim "$S/out/after-avm/run.json" '.claim' R40-C1
jcase after-avm-exit "$S/out/after-avm/run.json" '.exit' 0
jcase after-avm-receipt "$S/out/after-avm/run.json" '.receipt_written' true
jcase after-avm-handler "$S/out/after-avm/run.json" '.receipt.handlers[0]' squashfs_v4_be
jcase after-avm-files "$S/out/after-avm/run.json" '.receipt.files' 4
jcase after-avm-gaps "$S/out/after-avm/run.json" '.receipt.gaps' 0
jcase after-avm-marker "$S/out/after-avm/run.json" '.carrier.superblock.avm_marker' true
jcase after-avm-subject "$S/out/after-avm/run.json" '.receipt.subject_sha256' c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32
jcase after-avm-rea "$S/out/after-avm/run.json" '.rea.pin' rea-agents@6.5.0
jcase after-avm-sqver "$S/out/after-avm/run.json" '.sasquatch_v4be.version' 4.5.1
jcase after-avm-segment "$S/out/after-avm/run.json" '.run_provenance_segment_ok' true
jcase after-avm-outdir-seg "$S/out/after-avm/run.json" '.receipt.output_directory | test("/kaidoku-r40/")' true
jcase after-avm-envelope-error "$S/out/after-avm/run.json" '.envelope.error' null
run_case after-K1 0 "$CR" after "$S/fx/K1.sqsh" "$S/out/after-K1"
jcase after-K1-files "$S/out/after-K1/run.json" '.receipt.files' 5
jcase after-K1-marker "$S/out/after-K1/run.json" '.carrier.superblock.avm_marker' false
run_case after-keep-envelope 0 env C1_KEEP_ENVELOPE=1 "$CR" after "$S/fx/avm-gzip.sqsh" "$S/out/after-envelope"
v=1; [[ -f $S/out/after-envelope/after.envelope.json ]] && v=0
record after-envelope-file 0 "$v"
v=1; jq -e 'type == "object"' "$S/out/after-envelope/after.envelope.json" >/dev/null 2>&1 && v=0
record after-envelope-valid 0 "$v"

# ----------------------------------------------------------- mk-carriers.py
OA=$S/out/oracle-avm-dev/oracle.tsv
ON=$S/out/oracle-avm-dev/nonregular.tsv
run_case mk-reader-mode 0 "$MK" --root "$S" --out "$S/out/m-reader.json" --allow-any-ids \
  --reader "$READER" V1 fx/avm-dev.squashfs out/oracle-avm-dev/oracle.tsv out/oracle-avm-dev/nonregular.tsv
jcase mk-schema "$S/out/m-reader.json" '.schema' kaidoku-r40-c1-carriers-v1
jcase mk-claim "$S/out/m-reader.json" '.claim' R40-C1
jcase mk-layout "$S/out/m-reader.json" '.layout' avm
jcase mk-id "$S/out/m-reader.json" '.carriers[0].id' V1
jcase mk-pin "$S/out/m-reader.json" '.carriers[0].sha256' c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32
jcase mk-oracle-pin "$S/out/m-reader.json" '.carriers[0].oracle_sha256' 6e5880c972d203bcc232e598df6e382a85ff25d4e96615ab5f10b9989988b6ad
jcase mk-receipt "$S/out/m-reader.json" '.carriers[0].receipt' corpus/evidence/round-40/c1/V1/after.json
jcase mk-marker "$S/out/m-reader.json" '.carriers[0].avm_marker' true
run_case mk-off-mode 0 "$MK" --root "$S" --out "$S/out/m-off.json" --layout-check off --allow-any-ids \
  V1 fx/avm-dev.squashfs out/oracle-avm-dev/oracle.tsv out/oracle-avm-dev/nonregular.tsv
v=1; cmp -s "$S/out/m-reader.json" "$S/out/m-off.json" && v=0
record mk-reader-equals-off 0 "$v"
run_case mk-refuse-markerless 2 "$MK" --root "$S" --out "$S/out/m-nomark.json" --layout-check off --allow-any-ids \
  K1 fx/K1.sqsh out/oracle-avm-dev/oracle.tsv out/oracle-avm-dev/nonregular.tsv
run_case mk-allow-markerless 0 "$MK" --root "$S" --out "$S/out/m-allow.json" --layout-check off --allow-any-ids \
  --no-require-marker K1 fx/K1.sqsh out/oracle-avm-dev/oracle.tsv out/oracle-avm-dev/nonregular.tsv
run_case mk-refuse-le 2 "$MK" --root "$S" --out "$S/out/m-le.json" --layout-check off --allow-any-ids \
  L1 fx/le-dev.squashfs out/oracle-avm-dev/oracle.tsv out/oracle-avm-dev/nonregular.tsv
run_case mk-duplicate-id 2 "$MK" --root "$S" --out "$S/out/m-dup.json" --layout-check off --allow-any-ids \
  V1 fx/avm-dev.squashfs "$OA" "$ON" V1 fx/avm-dev.squashfs "$OA" "$ON"
run_case mk-duplicate-path 2 "$MK" --root "$S" --out "$S/out/m-duppath.json" --layout-check off --allow-any-ids \
  V1 fx/avm-dev.squashfs "$OA" "$ON" V2 fx/avm-dev.squashfs "$OA" "$ON"
run_case mk-no-carriers 2 "$MK" --root "$S" --out "$S/out/m-none.json" --layout-check off
run_case mk-missing-oracle 2 "$MK" --root "$S" --out "$S/out/m-noo.json" --layout-check off --allow-any-ids \
  V1 fx/avm-dev.squashfs fx/nope.tsv "$ON"
run_case mk-path-outside-root 2 "$MK" --root "$S" --out "$S/out/m-out.json" --layout-check off --allow-any-ids \
  V1 /etc/hostname "$OA" "$ON"
printf 'a\tb\n' > "$S/fakes/two-fields.tsv"
run_case mk-oracle-two-fields 2 "$MK" --root "$S" --out "$S/out/m-two.json" --layout-check off --allow-any-ids \
  V1 fx/avm-dev.squashfs "$S/fakes/two-fields.tsv" "$ON"
printf 'b\t303980bcb9e9e6cdec515230791af8b0ab1aaa244b58a8d99152673aa22197d0\t6\na\t5a81483d96b0bc15ad19af7f5a662e14b275729fbc05579b18513e7f550016b1\t7\n' > "$S/fakes/unsorted.tsv"
run_case mk-oracle-unsorted 2 "$MK" --root "$S" --out "$S/out/m-unsorted.json" --layout-check off --allow-any-ids \
  V1 fx/avm-dev.squashfs "$S/fakes/unsorted.tsv" "$ON"
printf 'a\tXYZ\t6\n' > "$S/fakes/badsha.tsv"
run_case mk-oracle-bad-sha 2 "$MK" --root "$S" --out "$S/out/m-badsha.json" --layout-check off --allow-any-ids \
  V1 fx/avm-dev.squashfs "$S/fakes/badsha.tsv" "$ON"
printf 'docs\tlink\n' > "$S/fakes/badkind.tsv"
run_case mk-nonregular-bad-kind 2 "$MK" --root "$S" --out "$S/out/m-badkind.json" --layout-check off --allow-any-ids \
  V1 fx/avm-dev.squashfs "$OA" "$S/fakes/badkind.tsv"
printf 'docs\tsymlink\t\n' > "$S/fakes/emptytarget.tsv"
run_case mk-nonregular-empty-target 2 "$MK" --root "$S" --out "$S/out/m-emptytarget.json" --layout-check off --allow-any-ids \
  V1 fx/avm-dev.squashfs "$OA" "$S/fakes/emptytarget.tsv"
printf 'apple1.txt\tdir\t\n' > "$S/fakes/clash.tsv"
run_case mk-nonregular-clash 2 "$MK" --root "$S" --out "$S/out/m-clash.json" --layout-check off --allow-any-ids \
  V1 fx/avm-dev.squashfs "$OA" "$S/fakes/clash.tsv"
run_case mk-frozen-tables-mismatch 2 "$MK" --root "$S" --out "$S/out/m-mismatch.json" --allow-any-ids \
  --reader "$READER" V1 fx/avm-dev.squashfs "$S/fakes/unsorted.tsv" "$ON"
printf 'V1\tfx/avm-dev.squashfs\tout/oracle-avm-dev/oracle.tsv\tout/oracle-avm-dev/nonregular.tsv\n' > "$S/fakes/spec.tsv"
run_case mk-spec-file 0 "$MK" --root "$S" --out "$S/out/m-spec.json" --layout-check off --allow-any-ids --spec "$S/fakes/spec.tsv"
printf 'V1\tfx/avm-dev.squashfs\tout/oracle-avm-dev/oracle.tsv\n' > "$S/fakes/spec-bad.tsv"
run_case mk-spec-bad 2 "$MK" --root "$S" --out "$S/out/m-specbad.json" --layout-check off --allow-any-ids --spec "$S/fakes/spec-bad.tsv"
# two carriers: genuine gzip + multiblock, ids out of order -> sorted V1,V2
run_case mk-two-carriers 0 "$MK" --root "$S" --out "$S/out/m-two-carriers.json" --layout-check off --allow-any-ids \
  V2 fx/avm-gzip.sqsh "$S/out/oracle-avm-gzip/oracle.tsv" "$S/out/oracle-avm-gzip/nonregular.tsv" \
  V1 fx/avm-dev.squashfs "$OA" "$ON"
jcase mk-sorted-ids "$S/out/m-two-carriers.json" '[.carriers[].id] | join(",")' V1,V2
jcase mk-two-count "$S/out/m-two-carriers.json" '.carriers | length' 2
run_case mk-canonical-ids 0 "$MK" --root "$S" --out "$S/out/m-canonical.json" --reader "$READER" \
  V1 fx/avm-dev.squashfs out/oracle-avm-dev/oracle.tsv out/oracle-avm-dev/nonregular.tsv \
  V2 fx/avm-gzip.sqsh out/oracle-avm-gzip/oracle.tsv out/oracle-avm-gzip/nonregular.tsv \
  L1 fx/avm-xz.sqsh out/oracle-avm-xz/oracle.tsv out/oracle-avm-xz/nonregular.tsv \
  L2 fx/avm-multi-gzip.sqsh out/oracle-avm-multi/oracle.tsv out/oracle-avm-multi/nonregular.tsv
jcase mk-canonical-ids-set "$S/out/m-canonical.json" '[.carriers[].id] | join(",")' V1,V2,L1,L2
jcase mk-canonical-count "$S/out/m-canonical.json" '.carriers | length' 4
run_case mk-wrong-id-set 2 "$MK" --root "$S" --out "$S/out/m-wrongids.json" --layout-check off \
  V1 fx/avm-dev.squashfs out/oracle-avm-dev/oracle.tsv out/oracle-avm-dev/nonregular.tsv \
  V2 fx/avm-gzip.sqsh out/oracle-avm-gzip/oracle.tsv out/oracle-avm-gzip/nonregular.tsv \
  L1 fx/avm-xz.sqsh out/oracle-avm-xz/oracle.tsv out/oracle-avm-xz/nonregular.tsv \
  L3 fx/avm-multi-gzip.sqsh out/oracle-avm-multi/oracle.tsv out/oracle-avm-multi/nonregular.tsv
run_case mk-missing-id 2 "$MK" --root "$S" --out "$S/out/m-missingid.json" --layout-check off \
  V1 fx/avm-dev.squashfs out/oracle-avm-dev/oracle.tsv out/oracle-avm-dev/nonregular.tsv \
  V2 fx/avm-gzip.sqsh out/oracle-avm-gzip/oracle.tsv out/oracle-avm-gzip/nonregular.tsv \
  L1 fx/avm-xz.sqsh out/oracle-avm-xz/oracle.tsv out/oracle-avm-xz/nonregular.tsv
run_case mk-deterministic 0 "$MK" --root "$S" --out "$S/out/m-two-carriers-2.json" --layout-check off --allow-any-ids \
  V2 fx/avm-gzip.sqsh "$S/out/oracle-avm-gzip/oracle.tsv" "$S/out/oracle-avm-gzip/nonregular.tsv" \
  V1 fx/avm-dev.squashfs "$OA" "$ON"
v=1; cmp -s "$S/out/m-two-carriers.json" "$S/out/m-two-carriers-2.json" && v=0
record mk-deterministic-bytes 0 "$v"

# ------------------------------------------------------------------- tally
jq -s --arg scratch "$S" --arg reader "$READER" --arg double "$TD" '
  {schema: "kaidoku-r40-c1-selftest-v1", scratch: $scratch,
   reader: $reader, reader_is_test_double: ($reader == $double),
   cases: length,
   passed: (map(select(.ok)) | length),
   failed: (map(select(.ok | not)) | length),
   failed_names: [ .[] | select(.ok | not) | .name ],
   results: .}' "$results"
[[ $fails -eq 0 ]] || exit 1
exit 0
