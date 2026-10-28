#!/usr/bin/env bash
# SentScope / round-47 w1 — security & scope probe harness for the two frozen counters.
# Every check appends {check, exit, stdout_sha256, utc, cmd} to receipts.jsonl.
set -u
export S=/fast/scratch/hyaku/kaidoku-r47/SentScope
export HYAKU_SCRATCH="$S" TMPDIR="$S"
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
R="$L/.ufo/waves/round-47/w1/SentScope"
CAP="$S/cap"
FREEZE_DECL=62e33f7dd75c8e3285967b26419842c106f6c965
FREEZE_PROMPT=5017e1f7299c3a812e87e7950148f54313dd279e
FREEZE_A5=07d2894eabe88c326e9036262f20ad02662c860d
REV=a631bba01633d2b5353306a569be4ce2e683d364
C0="$S/c0"; CHL="$S/c-hl"; CGIT="$S/c-git"; CPY="$S/c-py"; CVAL="$S/c-val"
mkdir -p "$CAP" "$R"
: > "$CAP/receipts.jsonl"

rec() {
  local name=$1; shift
  local out="$CAP/$name.out" t0 rc sha
  t0=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  "$@" > "$out" 2>&1
  rc=$?
  sha=$(sha256sum "$out" | cut -d' ' -f1)
  python3 - "$name" "$rc" "$sha" "$t0" "$@" >> "$CAP/receipts.jsonl" <<'PY'
import json, sys
name, rc, sha, utc, *cmd = sys.argv[1:]
print(json.dumps({"check": name, "exit": int(rc), "stdout_sha256": sha,
                  "utc": utc, "cmd": cmd}))
PY
  printf '[%-28s] exit=%s sha=%s\n' "$name" "$rc" "${sha:0:12}"
}

for d in "$C0" "$CHL" "$CGIT" "$CPY" "$CVAL"; do rm -rf "$d"; done
git clone -q --no-hardlinks "$L" "$C0"
git clone -q --no-hardlinks "$L" "$CHL"
git clone -q --no-hardlinks "$L" "$CGIT"
git clone -q --no-hardlinks "$L" "$CPY"
git clone -q --no-hardlinks "$L" "$CVAL"

# --- 0. toplevel assertions for every fixture clone -------------------------
rec clone_toplevels bash -c "for d in $C0 $CHL $CGIT $CPY $CVAL; do t=\$(git -C \"\$d\" rev-parse --show-toplevel); [ \"\$t\" = \"\$d\" ] && echo \"OK \$t\" || echo \"MISMATCH \$t != \$d\"; done"

# --- 1. read-only: lane status before/after the two counters ----------------
rec lane_status_before git -C "$L" status --porcelain
rec c1_a5_freeze_lane python3 -I -B "$L/tools/round-47/exact.py" --root "$L" --freeze "$FREEZE_A5" --rev "$REV" --json-out "$R/c1-a5.json"
rec c1_declared_freeze_lane python3 -I -B "$L/tools/round-47/exact.py" --root "$L" --freeze "$FREEZE_DECL" --rev "$REV" --json-out "$R/c1-declared.json"
rec c1_prompt_freeze_lane python3 -I -B "$L/tools/round-47/exact.py" --root "$L" --freeze "$FREEZE_PROMPT" --rev "$REV" --json-out "$R/c1-prompt-freeze.json"
rec c2_lane python3 -I -B "$L/tools/round-47/record.py" --root "$L" --rev "$REV" --json-out "$R/c2.json"
rec lane_status_after git -C "$L" status --porcelain

# --- 2. --json-out: refusals -------------------------------------------------
rec jsonout_outside_lane python3 -I -B "$L/tools/round-47/exact.py" --root "$C0" --freeze "$FREEZE_A5" --rev "$REV" --no-battery --json-out "$S/escape.json"
rec jsonout_graded_file python3 -I -B "$L/tools/round-47/exact.py" --root "$C0" --freeze "$FREEZE_A5" --rev "$REV" --no-battery --json-out "$C0/SKILL.md"
rec jsonout_graded_dir python3 -I -B "$L/tools/round-47/exact.py" --root "$C0" --freeze "$FREEZE_A5" --rev "$REV" --no-battery --json-out "$C0/tools/round-47/inject.json"
rec jsonout_traversal python3 -I -B "$L/tools/round-47/exact.py" --root "$C0" --freeze "$FREEZE_A5" --rev "$REV" --no-battery --json-out "$C0/.ufo/../../../escape2.json"
rec jsonout_symlink_to_graded python3 -B "$S/probe1.py"

# --- 3. --json-out: accepted repo internals (clone only) ---------------------
rec jsonout_git_config bash -c "cd $CGIT && python3 -I -B $L/tools/round-47/exact.py --root $CGIT --freeze $FREEZE_A5 --rev $REV --no-battery --json-out $CGIT/.git/config; echo \"counter_exit=\$?\"; head -c 60 $CGIT/.git/config; echo; git -C $CGIT status --porcelain 2>&1 | head -2"

# --- 4. --json-out: hardlink bypass of the graded-surface guard --------------
rec jsonout_hardlink bash -c "ln $CHL/SKILL.md $CHL/.ufo/SKILL-mirror.json && echo \"before=\$(sha256sum $CHL/SKILL.md | cut -c1-16)\"; git -C $CHL status --porcelain -- SKILL.md; python3 -I -B $L/tools/round-47/exact.py --root $CHL --freeze $FREEZE_A5 --rev $REV --no-battery --json-out $CHL/.ufo/SKILL-mirror.json >/dev/null 2>&1; echo \"counter_exit=\$?\"; echo \"after=\$(sha256sum $CHL/SKILL.md | cut -c1-16)\"; head -1 $CHL/SKILL.md; git -C $CHL status --porcelain -- SKILL.md"

# --- 5. --json-out parent missing: exit-code contract -----------------------
rec jsonout_missing_parent bash -c "python3 -I -B $L/tools/round-47/exact.py --root $CVAL --freeze $FREEZE_A5 --rev $REV --no-battery --json-out $CVAL/.ufo/nodir/x.json 2>&1 | tail -2; echo \"exit=\${PIPESTATUS[0]}\""

# --- 6. scratch-root refusal ------------------------------------------------
rec scratch_no_env bash -c "env -u HYAKU_SCRATCH -u TMPDIR python3 -I -B $L/tools/round-47/exact.py --root $L --freeze $FREEZE_A5 --rev $REV --json-out $R/scratch-noenv.json; echo \"exit=\$?\""
rec scratch_tmp bash -c "env -u HYAKU_SCRATCH TMPDIR=/tmp python3 -I -B $L/tools/round-47/exact.py --root $L --freeze $FREEZE_A5 --rev $REV --json-out $R/scratch-tmp.json; echo \"exit=\$?\""
rec scratch_var_tmp bash -c "env HYAKU_SCRATCH=/var/tmp python3 -I -B $L/tools/round-47/exact.py --root $L --freeze $FREEZE_A5 --rev $REV --json-out $R/scratch-vartmp.json; echo \"exit=\$?\""
rec scratch_library python3 -B "$S/probe3.py"

# --- 7. bytecode write when -B is omitted ----------------------------------
rec pycache_without_B bash -c "rm -rf $CPY/tools/round-46/__pycache__; python3 $L/tools/round-47/exact.py --root $CPY --freeze $FREEZE_A5 --rev $REV --no-battery --json-out $CPY/.ufo/b.json >/dev/null 2>&1; echo \"exit=\$?\"; echo \"pycache: \$(ls $CPY/tools/round-46/__pycache__ 2>/dev/null | tr '\n' ' ')\"; echo \"git status (frozen paths): [\$(git -C $CPY status --porcelain -- tools/round-47 plans/round-47-claims.md)]\"; echo \"real lane pycache: \$(ls $L/tools/round-47/__pycache__ 2>/dev/null | tr '\n' ' ')\""

# --- 8. crafted SCORECARD / SKILL: no execution -----------------------------
rec crafted_inputs_no_exec python3 -B "$S/probe4.py"
rec symlink_blobs python3 -B "$S/probe2.py"
rec window_vacuity python3 -B "$S/probe5.py"

# --- 9. selftests ----------------------------------------------------------
rec exact_selftest_bare python3 -I -B "$L/tools/round-47/exact.py" --selftest
rec record_selftest_bare python3 -I -B "$L/tools/round-47/record.py" --selftest
rec exact_selftest_dummy python3 -I -B "$L/tools/round-47/exact.py" --root /nonexistent --freeze deadbeef --rev deadbeef --selftest
rec record_selftest_dummy python3 -I -B "$L/tools/round-47/record.py" --root /nonexistent --rev deadbeef --selftest

# --- 10. argv injection ----------------------------------------------------
rec argv_rev_help bash -c "python3 -I -B $L/tools/round-47/exact.py --root $C0 --freeze $FREEZE_A5 --rev=--help --no-battery; echo \"exit=\$?\""
rec argv_freeze_help bash -c "python3 -I -B $L/tools/round-47/exact.py --root $C0 --freeze=--help --rev $REV --no-battery; echo \"exit=\$?\""
rec argv_record_output bash -c "python3 -I -B $L/tools/round-47/record.py --root $C0 --rev=--output=x; echo \"exit=\$?\""

# --- 11. freeze chain facts ------------------------------------------------
rec freeze_chain git -C "$L" log --format="%H %s" "$FREEZE_DECL..$REV" -- plans/round-47-claims.md tools/round-47/
rec claims_unchanged_since_A2 git -C "$L" diff --stat "$FREEZE_DECL" "$REV" -- plans/round-47-claims.md
rec record_freeze_calls bash -c "grep -n 'freeze' $L/tools/round-47/record.py || echo 'NO OCCURRENCE OF freeze IN record.py'"
rec exact_pins sha256sum "$L/tools/round-47/exact.py"

echo
echo "receipts: $(wc -l < "$CAP/receipts.jsonl") lines"
