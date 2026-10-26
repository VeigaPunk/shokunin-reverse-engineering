#!/usr/bin/env bash
# R39-C1 harness selftest: exercises c1-run.sh (after|oracle) and
# mk-carriers.py on K1/K2 copies only (round-37 carriers already measured in
# round 38). Never builds or runs K5/K6, never calls REA on a held-out carrier,
# writes only under its own scratch (default
# $HYAKU_SCRATCH/kaidoku-r39/c1-selftest.<pid>, removed on exit).
#
#   ./selftest.sh              human table + JSON tally on stdout
#   SELFTEST_SCRATCH=DIR ./selftest.sh   reuse/keep a scratch dir (still removed)
#
# Output: one JSON object on stdout:
#   {cases, passed, failed, results:[{name, want, got, ok}], receipts:{...}}
# Exit: 0 all cases pass, 1 any case failed, 2 environment problem.
set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
LANE=${LANE:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
HY=${HYAKU_SCRATCH:-/fast/scratch/hyaku}
S=${SELFTEST_SCRATCH:-$HY/kaidoku-r39/c1-selftest.$$}
mkdir -p "$S" || { echo "selftest: cannot create scratch $S" >&2; exit 2; }
S=$(realpath "$S")
trap 'rm -rf -- "$S"' EXIT
export HYAKU_SCRATCH=$S/hy
mkdir -p "$HYAKU_SCRATCH"
export TMPDIR=$S

CR=$HERE/c1-run.sh
MK=$HERE/mk-carriers.py
CMP=$HERE/compare-after.py
for f in "$CR" "$MK" "$CMP"; do
  [[ -x $f ]] || { echo "selftest: missing $f" >&2; exit 2; }
done
R37=$LANE/corpus/evidence/round-37/c1
R38=$LANE/corpus/evidence/round-38/c1
for k in K1 K2 K3 K4; do
  [[ -f $R37/$k/oracle.tsv ]] || { echo "selftest: missing $R37/$k/oracle.tsv" >&2; exit 2; }
done
[[ -f $R38/K1/after.json && -f $R38/K2/after.json ]] || {
  echo "selftest: missing round-38 K1/K2 receipts" >&2; exit 2; }

results=$S/results.jsonl
: > "$results"
fails=0
record() { # name want got
  jq -nc --arg n "$1" --argjson w "$2" --argjson g "$3" \
    '{name: $n, want: $w, got: $g, ok: ($w == $g)}' >> "$results"
  if [[ $2 != "$3" ]]; then fails=$((fails + 1)); fi
}
run_case() { # name want-window command...
  local name=$1 want=$2 rc out
  shift 2
  set +e
  out=$("$@" 2>&1)
  rc=$?
  set -e
  record "$name" "$want" "$rc"
  if [[ $rc != "$want" ]]; then
    printf 'FAIL %s want exit %s got %s: %s\n' "$name" "$want" "$rc" \
      "$(printf '%s' "$out" | head -2 | tr '\n' ' ' | cut -c1-200)" >&2
  fi
}
jcheck() { # name jq-expr file
  local name=$1 expr=$2 file=$3 v=0
  if jq -e "$expr" "$file" >/dev/null 2>&1; then v=1; fi
  record "$name" 1 "$v"
  if [[ $v != 1 ]]; then printf 'FAIL %s: %s\n' "$name" "$expr" >&2; fi
}
jcheck_oracle() { # name after.json oracle.tsv -- every oracle row published (suffix + sha)
  local name=$1 after=$2 oracle=$3 v=0
  if jq -e --rawfile o "$oracle" '
      ($o | split("\n") | map(select(length > 0) | split("\t") | {rel: .[0], sha: .[1]})) as $oracle
      | (.normalized_result.files | map({rel: .relative_path, sha: .sha256})) as $files
      | all($oracle[]; . as $r | any($files[];
          .sha == $r.sha and (.rel == $r.rel or (.rel | endswith("/" + $r.rel)))))
    ' "$after" >/dev/null 2>&1; then v=1; fi
  record "$name" 1 "$v"
  if [[ $v != 1 ]]; then printf 'FAIL %s: oracle rows not all published\n' "$name" >&2; fi
}
fcheck() { # name command...
  local name=$1 v=0
  shift
  if "$@" >/dev/null 2>&1; then v=1; fi
  record "$name" 1 "$v"
  if [[ $v != 1 ]]; then printf 'FAIL %s: %s\n' "$name" "$*" >&2; fi
}

# ---------------------------------------------------------------- fixtures
mkdir -p "$S/carriers/K1" "$S/carriers/K2" "$S/carriers/K3" "$S/carriers/K4" "$S/fx/neg"
cp "$R37/K1/carrier.sqsh" "$S/carriers/K1/carrier.sqsh"
cp "$R37/K2/carrier.sqsh" "$S/carriers/K2/carrier.sqsh"
cp "$R37/K3/carrier.bin" "$S/carriers/K3/carrier.bin"
cp "$R37/K4/carrier.bin" "$S/carriers/K4/carrier.bin"
for k in K1 K2 K3 K4; do cp "$R37/$k/oracle.tsv" "$S/carriers/$k/oracle.tsv"; done
printf 'link-to-hello\t../hello.txt\tescaping\n' > "$S/carriers/K1/symlinks.tsv"
printf 'var/lib/run-link\t../../a/run.sh\tin-tree\n' > "$S/carriers/K2/symlinks.tsv"
: > "$S/carriers/K3/symlinks.tsv"   # test fixtures only (round-39 tables come from R39C1SymlinkK1K4)
: > "$S/carriers/K4/symlinks.tsv"
printf 'hsqs\x00\x00\x00\x04' > "$S/fx/neg/le.raw"
printf 'not a squashfs image at all\n' > "$S/fx/neg/junk.bin"
head -c 300 "$S/carriers/K1/carrier.sqsh" > "$S/fx/neg/truncated.sqsh"
printf 'hello.txt\tnot-a-sha\t29\n' > "$S/fx/neg/bad-sha.tsv"
printf 'hello.txt\t0da249108ff14fde04d11119e2d86dabc20aa18a95f0411164294674d62951ff\n' \
  > "$S/fx/neg/two-col.tsv"
printf 'link-to-hello\t../hello.txt\tintree\n' > "$S/fx/neg/bad-class.tsv"
printf 'hello.txt\t0da249108ff14fde04d11119e2d86dabc20aa18a95f0411164294674d62951ff\t29\nlink-to-hello\t%s\t1\n' \
  "$(printf 'a%.0s' {1..64})" > "$S/fx/neg/clash.tsv"
printf 'K1\tcarriers/K1/carrier.sqsh\tcarriers/K1/oracle.tsv\tcarriers/K1/symlinks.tsv\tfirst tree\n' \
  > "$S/fx/neg/spec.tsv"
printf 'link-to-hello\t../hello.txt\tescaping\n' > "$S/fx/expect-K1-symlinks.tsv"
printf 'var/lib/run-link\t../../a/run.sh\tin-tree\n' > "$S/fx/expect-K2-symlinks.tsv"

# ------------------------------------------------------------- mk-carriers
run_case "mk.green-4-carriers" 0 "$MK" --root "$S" --out "$S/fx/manifest.json" \
  K1 carriers/K1/carrier.sqsh carriers/K1/oracle.tsv carriers/K1/symlinks.tsv \
  K2 carriers/K2/carrier.sqsh carriers/K2/oracle.tsv carriers/K2/symlinks.tsv \
  K3 carriers/K3/carrier.bin carriers/K3/oracle.tsv carriers/K3/symlinks.tsv \
  K4 carriers/K4/carrier.bin carriers/K4/oracle.tsv carriers/K4/symlinks.tsv
run_case "mk.deterministic" 0 "$MK" --root "$S" --out "$S/fx/manifest.b.json" \
  K1 carriers/K1/carrier.sqsh carriers/K1/oracle.tsv carriers/K1/symlinks.tsv \
  K2 carriers/K2/carrier.sqsh carriers/K2/oracle.tsv carriers/K2/symlinks.tsv \
  K3 carriers/K3/carrier.bin carriers/K3/oracle.tsv carriers/K3/symlinks.tsv \
  K4 carriers/K4/carrier.bin carriers/K4/oracle.tsv carriers/K4/symlinks.tsv
fcheck "mk.byte-identical-regeneration" cmp -s "$S/fx/manifest.json" "$S/fx/manifest.b.json"
run_case "mk.spec-tsv" 0 "$MK" --root "$S" --out "$S/fx/spec.json" --spec "$S/fx/neg/spec.tsv"
jcheck "mk.spec-carries-kind" '.carriers[0].kind == "first tree"' "$S/fx/spec.json"
jcheck "mk.manifest-keys" '(.carriers | length) == 4 and
  all(.carriers[]; (["id","path","sha256","oracle","symlinks","receipt"] - keys) == []) and
  all(.carriers[]; .receipt == ("corpus/evidence/round-39/c1/" + .id + "/after.json")) and
  all(.carriers[]; (.path|startswith("/")|not) and (.path|contains("..")|not))' "$S/fx/manifest.json"
jcheck "mk.pins-match-carriers" '
  (.carriers[] | select(.id == "K1") | .sha256) == "1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e" and
  (.carriers[] | select(.id == "K2") | .sha256) == "403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154"' \
  "$S/fx/manifest.json"
run_case "mk.red.le-magic" 2 "$MK" --root "$S" --out "$S/fx/neg/x1.json" \
  K1 fx/neg/le.raw carriers/K1/oracle.tsv carriers/K1/symlinks.tsv
run_case "mk.endian-any-accepts-le" 0 "$MK" --root "$S" --out "$S/fx/neg/x2.json" \
  --endian any K1 fx/neg/le.raw carriers/K1/oracle.tsv carriers/K1/symlinks.tsv
run_case "mk.red.id-gap" 2 "$MK" --root "$S" --out "$S/fx/neg/x3.json" \
  K1 carriers/K1/carrier.sqsh carriers/K1/oracle.tsv carriers/K1/symlinks.tsv \
  K3 carriers/K3/carrier.bin carriers/K3/oracle.tsv carriers/K3/symlinks.tsv
run_case "mk.allow-gaps" 0 "$MK" --root "$S" --out "$S/fx/neg/x4.json" --allow-gaps \
  K1 carriers/K1/carrier.sqsh carriers/K1/oracle.tsv carriers/K1/symlinks.tsv \
  K3 carriers/K3/carrier.bin carriers/K3/oracle.tsv carriers/K3/symlinks.tsv
run_case "mk.red.duplicate-id" 2 "$MK" --root "$S" --out "$S/fx/neg/x5.json" \
  K1 carriers/K1/carrier.sqsh carriers/K1/oracle.tsv carriers/K1/symlinks.tsv \
  K1 carriers/K2/carrier.sqsh carriers/K2/oracle.tsv carriers/K2/symlinks.tsv
run_case "mk.red.duplicate-pin" 2 "$MK" --root "$S" --out "$S/fx/neg/x5b.json" \
  K1 carriers/K1/carrier.sqsh carriers/K1/oracle.tsv carriers/K1/symlinks.tsv \
  K2 carriers/K1/carrier.sqsh carriers/K2/oracle.tsv carriers/K2/symlinks.tsv
run_case "mk.red.oracle-symlink-clash" 2 "$MK" --root "$S" --out "$S/fx/neg/x6.json" \
  K1 carriers/K1/carrier.sqsh fx/neg/clash.tsv carriers/K1/symlinks.tsv
run_case "mk.red.bad-sha" 2 "$MK" --root "$S" --out "$S/fx/neg/x7.json" \
  K1 carriers/K1/carrier.sqsh fx/neg/bad-sha.tsv carriers/K1/symlinks.tsv
run_case "mk.red.two-column-oracle" 2 "$MK" --root "$S" --out "$S/fx/neg/x8.json" \
  K1 carriers/K1/carrier.sqsh fx/neg/two-col.tsv carriers/K1/symlinks.tsv
run_case "mk.red.bad-symlink-class" 2 "$MK" --root "$S" --out "$S/fx/neg/x9.json" \
  K1 carriers/K1/carrier.sqsh carriers/K1/oracle.tsv fx/neg/bad-class.tsv
run_case "mk.red.missing-carrier" 2 "$MK" --root "$S" --out "$S/fx/neg/x10.json" \
  K1 carriers/K1/nope.sqsh carriers/K1/oracle.tsv carriers/K1/symlinks.tsv
run_case "mk.red.escape-root" 2 "$MK" --root "$S/carriers" --out "$S/fx/neg/x11.json" \
  K1 ../../etc/hostname K1/oracle.tsv K1/symlinks.tsv
run_case "mk.red.no-carriers" 2 "$MK" --root "$S" --out "$S/fx/neg/x12.json"

# ------------------------------------------------------------- after arm
run_case "run.after.K1" 0 "$CR" after "$S/carriers/K1/carrier.sqsh" "$S/out/K1"
jcheck "run.after.K1.handler" '.receipt.handlers == ["squashfs_v4_be"]' "$S/out/K1/run.json"
jcheck "run.after.K1.receipt" '.receipt_written and .exit == 0 and .envelope.ok' "$S/out/K1/run.json"
jcheck "run.after.K1.pin" '.receipt.selection_sha256 == .carrier.sha256 and .receipt.subject_sha256 == .carrier.sha256' "$S/out/K1/run.json"
jcheck "run.after.K1.files-5" '.receipt.files == 5 and .receipt.gaps == 0' "$S/out/K1/run.json"
jcheck "run.after.K1.toolchain" '.rea.version == "6.5.0" and .unblob.version == "26.6.4" and
  .sasquatch_v4be.version == "4.5.1" and .unblob.sha256 == "0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09" and
  .sasquatch_v4be.path == "/home/vgpnk/.local/bin/sasquatch-v4be"' "$S/out/K1/run.json"
jcheck "run.after.K1.times" '.start_utc | test("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]{8}Z$")' "$S/out/K1/run.json"
fcheck "run.after.K1.scratch-removed" test -z "$(ls -A "$HYAKU_SCRATCH/kaidoku-r39" 2>/dev/null)"
jcheck_oracle "run.after.K1.oracle-published" "$S/out/K1/after.json" "$R37/K1/oracle.tsv"
jcheck "run.after.K1.run-provenance" '(.parameters.output_directory | test("/kaidoku-r39/"))' \
  "$S/out/K1/after.json"
fcheck "run.after.K1.matches-round-38" "$CMP" --json-out "$S/fx/compare-K1-r38.json" \
  "$S/out/K1/after.json" "$R38/K1/after.json"

run_case "run.after.K2" 0 "$CR" after "$S/carriers/K2/carrier.sqsh" "$S/out/K2"
jcheck "run.after.K2.files-3-gap-1" '.receipt.files == 3 and .receipt.gaps == 1 and
  .receipt.gaps_detail[0].kind == "unpublished-entry" and
  (.receipt.gaps_detail[0].relative_path | endswith("/var/lib/run-link"))' "$S/out/K2/run.json"
jcheck_oracle "run.after.K2.oracle-published" "$S/out/K2/after.json" "$R37/K2/oracle.tsv"
jcheck "run.after.K2.run-provenance" '(.parameters.output_directory | test("/kaidoku-r39/"))' \
  "$S/out/K2/after.json"
jcheck "run.after.K2.escaping-not-published" '
  all(.normalized_result.files[];
      ((.relative_path | endswith("/var/lib/run-link")) | not))' "$S/out/K2/after.json"
fcheck "run.after.K2.matches-round-38" "$CMP" --json-out "$S/fx/compare-K2-r38.json" \
  "$S/out/K2/after.json" "$R38/K2/after.json"
fcheck "run.after.K2.scratch-removed" test -z "$(ls -A "$HYAKU_SCRATCH/kaidoku-r39" 2>/dev/null)"

# keep-envelope + rerun bookkeeping
run_case "run.after.keep-envelope" 0 env C1_KEEP_ENVELOPE=1 \
  "$CR" after "$S/carriers/K1/carrier.sqsh" "$S/out/K1env"
fcheck "run.after.keep-envelope.file" test -s "$S/out/K1env/after.envelope.json"
jcheck "run.after.keep-envelope.shape" '.ok == true and (.data | type) == "object"' \
  "$S/out/K1env/after.envelope.json"
run_case "run.after.rerun-same-outdir" 0 "$CR" after "$S/carriers/K1/carrier.sqsh" "$S/out/K1"
jcheck "run.after.rerun-records-previous" '.previous_after_json_sha256 | type == "string"' \
  "$S/out/K1/run.json"

# explicit SCRATCH argument: created by the harness path, removed by its trap
run_case "run.after.explicit-scratch" 0 "$CR" after "$S/carriers/K1/carrier.sqsh" \
  "$S/out/K1s" "$S/myscratch"
fcheck "run.after.explicit-scratch.removed" test ! -e "$S/myscratch"
# a scratch outside a /kaidoku-r39/ segment would make the receipt uncountable
run_case "run.red.foreign-scratch" 2 "$CR" after "$S/carriers/K1/carrier.sqsh" \
  "$S/out/foreign" /tmp/r39-foreign-$$
run_case "run.after.foreign-scratch-allowed" 0 env C1_ALLOW_FOREIGN_SCRATCH=1 \
  "$CR" after "$S/carriers/K1/carrier.sqsh" "$S/out/foreign" /tmp/r39-foreign-$$
jcheck "run.after.foreign-scratch-recorded" '.run_provenance_segment_ok == false' \
  "$S/out/foreign/run.json"
fcheck "run.after.foreign-scratch.removed" test ! -e /tmp/r39-foreign-$$

# ------------------------------------------------------------- oracle arm
run_case "run.oracle.K1" 0 "$CR" oracle "$S/carriers/K1/carrier.sqsh" "$S/out/K1-oracle"
fcheck "run.oracle.K1.tsv-identical" cmp -s "$R37/K1/oracle.tsv" "$S/out/K1-oracle/oracle-check.tsv"
fcheck "run.oracle.K1.symlink-escaping" \
  cmp -s "$S/fx/expect-K1-symlinks.tsv" "$S/out/K1-oracle/oracle-symlinks-check.tsv"
jcheck "run.oracle.K1.counts" '.squashfs_offset == 0 and .counts.regular_files == 5 and
  .counts.symlinks_in_tree == 0 and .counts.symlinks_escaping == 1 and .exit == 0' \
  "$S/out/K1-oracle/oracle-run.json"
run_case "run.oracle.K2" 0 "$CR" oracle "$S/carriers/K2/carrier.sqsh" "$S/out/K2-oracle"
fcheck "run.oracle.K2.tsv-identical" cmp -s "$R37/K2/oracle.tsv" "$S/out/K2-oracle/oracle-check.tsv"
fcheck "run.oracle.K2.symlink-in-tree" \
  cmp -s "$S/fx/expect-K2-symlinks.tsv" "$S/out/K2-oracle/oracle-symlinks-check.tsv"

# ------------------------------------------------------------ error paths
run_case "run.red.no-args" 2 "$CR"
run_case "run.red.bad-mode" 2 "$CR" frobnicate "$S/carriers/K1/carrier.sqsh" "$S/out/x"
run_case "run.red.two-args" 2 "$CR" after "$S/carriers/K1/carrier.sqsh"
run_case "run.red.missing-carrier" 2 "$CR" after "$S/fx/neg/nope.sqsh" "$S/out/x"
run_case "run.red.oracle-no-magic" 2 "$CR" oracle "$S/fx/neg/junk.bin" "$S/out/junk"
run_case "run.red.oracle-truncated" 3 "$CR" oracle "$S/fx/neg/truncated.sqsh" "$S/out/trunc"
jcheck "run.red.oracle-truncated.not-pass" '.exit != 0 and .counts.regular_files == 0' \
  "$S/out/trunc/oracle-run.json"
stripped=$(printf '%s' "$PATH" | tr ':' '\n' | grep -v -x "$HOME/.local/bin" | paste -sd: || true)
[[ -n $stripped ]] || { echo "selftest: could not build a stripped PATH" >&2; exit 2; }
run_case "run.red.sasquatch-stripped" 2 env PATH="$stripped" \
  "$CR" after "$S/carriers/K1/carrier.sqsh" "$S/out/strip"
run_case "run.red.unblob-missing" 2 env REA_UNBLOB_COMMAND="$S/fx/neg/no-unblob" \
  "$CR" after "$S/carriers/K1/carrier.sqsh" "$S/out/noenv"
run_case "run.red.rea-failure" 3 env REA_UNBLOB_COMMAND=/bin/false \
  "$CR" after "$S/carriers/K1/carrier.sqsh" "$S/out/falseblob"
jcheck "run.red.rea-failure.no-receipt" '(.receipt_written | not) and (.envelope.ok | not)' \
  "$S/out/falseblob/run.json"
fcheck "run.red.rea-failure.no-after-json" test ! -e "$S/out/falseblob/after.json"

# ---------------------------------------------------------------- tally
jq -s --arg scratch "$S" --arg rea "$(npx -y rea-agents@6.5.0 --version 2>/dev/null | sed -n '$p')" \
  --arg unblob "$("$HOME/.local/bin/unblob" --version 2>&1 | sed -n 1p)" \
  --arg sasq "$("$HOME/.local/bin/sasquatch-v4be" -version 2>&1 | sed -n 1p)" \
  --arg lane "$LANE" \
  '{selftest: "r39-c1-harness", lane: $lane,
    toolchain: {rea: $rea, unblob: $unblob, sasquatch_v4be: $sasq},
    cases: length, passed: (map(select(.ok)) | length),
    failed: (map(select(.ok | not)) | length),
    results: map({name, want, got, ok})}' "$results" > "$S/tally.json"
cat "$S/tally.json"
if [[ -n ${SELFTEST_TALLY:-} ]]; then cp "$S/tally.json" "$SELFTEST_TALLY"; fi
if [[ $fails -ne 0 ]]; then
  echo "selftest: $fails case(s) failed" >&2
  exit 1
fi
exit 0
