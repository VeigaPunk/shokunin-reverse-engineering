#!/usr/bin/env bash
# ConnRouted receipts: one line per read-only command, with exit code, stdout sha256, UTC time.
set -u
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=/fast/scratch/hyaku/kaidoku-r47/ConnRouted
OUT="$LANE/.ufo/waves/round-47/w1/ConnRouted"
mkdir -p "$OUT"
: > "$OUT/receipts.jsonl"

r() {
  local label="$1"; shift
  local tmp="$S/.r.$$"
  local cmd; cmd=$(printf '%q ' "$@")
  ( cd "$LANE" && "$@" ) > "$tmp" 2>&1
  local code=$?
  local sha; sha=$(sha256sum "$tmp" | awk '{print $1}')
  python3 - "$label" "$code" "$sha" "$tmp" "$cmd" <<'PY' >> "$OUT/receipts.jsonl"
import json, sys, datetime
label, code, sha, path = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
cmd = sys.argv[5]
body = open(path).read()
print(json.dumps({"label": label, "exit": code, "stdout_sha256": sha,
                  "utc": datetime.datetime.now(datetime.timezone.utc)
                  .strftime("%Y-%m-%dT%H:%M:%SZ"),
                  "stdout_tail": body[-300:] if len(body) > 300 else body,
                  "cmd": cmd}, sort_keys=True))
PY
  rm -f "$tmp"
}

r freeze_series env LC_ALL=C git log --format='%h %ci %s' --reverse 5017e1f7299c3a812e87e7950148f54313dd279e..caafeffa330a15e59412bc037591f6942b51e5aa
r ancestry_landing_before_A2 git merge-base --is-ancestor e856beb552080c03ede6000b96f1b58bde44c421 62e33f7dd75c8e3285967b26419842c106f6c965
r block24_rows grep -n '^| R46-CL' SKILL.md
r block23_r45cl19_row grep -n 'R45-CL19' SKILL.md
r cl9_cl10_selftest_cases grep -n 'red-frozen-section-shrink-is-exit-2\|red-dirty-frozen-tool-is-exit-2' tools/round-46/attest.py
r window_332f_58eb_empty git log --name-status --format= 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md
r w2_dispatch_file_commit git log --format='%H %s' -1 -- .ufo/waves/round-46/w2-dispatch.json
r w2_tree_at_head git ls-tree -r --name-only HEAD .ufo/waves/round-46/w2
r ready_files_round46 bash -c "git ls-tree -r --name-only HEAD .ufo/waves/round-46 | grep ready"
r results_json_at_head bash -c "git ls-tree -r --name-only HEAD .ufo/waves/round-46 | grep -c results.json"
r porcelain_count bash -c "git status --porcelain | wc -l"
r porcelain_excluding_this_seat bash -c "git status --porcelain -- . ':(exclude).ufo/waves/round-47/w1/ConnRouted*' | wc -l"
r untracked_count bash -c "git ls-files --others --exclude-standard | wc -l"
r controls_at_head git ls-tree -r --name-only HEAD .ufo/waves/round-47/controls
r record_freeze_hits bash -c "grep -c freeze tools/round-47/record.py"
r corr_regex_line sed -n '50p' tools/round-47/record.py
r dead_axes_branch sed -n '292,298p' tools/round-47/record.py
r log_round46_waves sed -n '3363,3365p' LOG.md
r scorecard_round46_seats bash -c "grep -n 'Waves: 40 + 40' SCORECARD.md"
r registry_attest_row sed -n '1743p' SKILL.md
r registry_record_row sed -n '1749p' SKILL.md
r bare_selftest_record python3 -I -B tools/round-47/record.py --selftest
r bare_selftest_exact python3 -I -B tools/round-47/exact.py --selftest
r record_selftest_cases python3 -I -B tools/round-47/record.py --selftest --root . --rev caafeffa330a15e59412bc037591f6942b51e5aa
r exact_selftest_cases python3 -I -B tools/round-47/exact.py --selftest --root . --freeze 1e2c3102952dc636650095643c1963c833859019 --rev caafeffa330a15e59412bc037591f6942b51e5aa
r attest_case_registrations bash -c "grep -cE '^\\s*case\\(' tools/round-46/attest.py"
echo "receipts written: $(wc -l < "$OUT/receipts.jsonl")"
