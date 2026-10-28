#!/bin/sh
# mutants.sh — the prefile-check harness must be able to fail.
#
# Each mutant is a one-line semantic change to prefile-check.sh. A mutant is
# CAUGHT when at least one test case (the 5 sandbox selftest cases, or the four
# historical lane replays) yields an exit code that differs from the
# unmutated tool's exit code on the same case. A mutant that changes no exit
# code on any case is EQUIVALENT and is reported as such.
#
# Test cases and their expected (unmutated) exit codes:
#   selftest green-wave-settled-no-report        0
#   selftest red-wave-never-settled               1
#   selftest red-report-filed-before-wave-done    1
#   selftest red-empty-frozen-paths               1
#   selftest red-unusable-lane-root               2
#   replay round 41 (D1 defect filed early)       1
#   replay round 42 (filed after wave-1)          0
#   replay round 43 (filed after wave-2)          0
#   replay round 44 (wave-1 still running)        1
#
# usage: mutants.sh <tool-path> <lane-root> <fleet-root>
# exit 0 when every mutant is caught; 1 when a mutant survives; 2 on usage error.

set -u
TOOL=${1:-}
LANE=${2:-}
FLEET=${3:-}
[ -n "$TOOL" ] && [ -n "$LANE" ] && [ -n "$FLEET" ] || {
    echo "usage: $0 <tool> <lane> <fleet>" >&2
    exit 2
}
[ -f "$TOOL" ] || { echo "$0: no such tool: $TOOL" >&2; exit 2; }

WORKDIR=$(mktemp -d "${TMPDIR:-/tmp}/prefile-mutants.XXXXXX") || exit 2
trap 'rm -rf "$WORKDIR"' EXIT INT TERM

run_all() { # tool -> prints "case=exit" lines
    _t=$1
    _s=$("$_t" --selftest 2>&1)
    _rc=$?
    printf 'selftest_overall=%s\n' "$_rc"
    for r in 41 42 43 44; do
        _j="$WORKDIR/receipt-$r.json"
        rm -f "$_j"
        "$_t" --lane "$LANE" --fleet "$FLEET" --round "$r" --json-out "$_j" >/dev/null 2>&1
        printf 'replay_%s=%s\n' "$r" "$?"
        # the set of FAIL keys is part of the contract too: a mutant that
        # downgrades one binding finding must not be able to hide it
        _keys=$(tr '{' '\n' <"$_j" 2>/dev/null | sed -n 's/.*"severity": "FAIL", "key": "\([^"]*\)".*/\1/p' | tr '\n' ',')
        printf 'replay_%s_failkeys=%s\n' "$r" "$_keys"
    done
    # a lane with no wave directory at all: the gate must still FAIL, and name
    # the wave_dir_missing finding (a mutant that skips the missing-directory
    # arm would otherwise report no_launched_wave instead)
    _j="$WORKDIR/receipt-nowavedir.json"
    rm -f "$_j"
    "$_t" --lane "$WORKDIR/nowavedir" --fleet "$FLEET" --round 44 --json-out "$_j" >/dev/null 2>&1
    printf 'replay_nowavedir=%s\n' "$?"
    _keys=$(tr '{' '\n' <"$_j" 2>/dev/null | sed -n 's/.*"severity": "FAIL", "key": "\([^"]*\)".*/\1/p' | tr '\n' ',')
    printf 'replay_nowavedir_failkeys=%s\n' "$_keys"
}

CAUGHT=0
SURVIVED=0

# a lane fixture with no .ufo/waves/round-44 directory (created before the
# baseline so BASE and every mutant see the same tree)
mkdir -p "$WORKDIR/nowavedir"
git -C "$WORKDIR/nowavedir" init -q -b main >/dev/null 2>&1
git -C "$WORKDIR/nowavedir" config user.name fx
git -C "$WORKDIR/nowavedir" config user.email fx@fx
mkdir -p "$WORKDIR/nowavedir/plans"
printf '# claims\n\n## Frozen paths\n\n`plans/round-44-claims.md`\n' \
    >"$WORKDIR/nowavedir/plans/round-44-claims.md"
git -C "$WORKDIR/nowavedir" add -A >/dev/null 2>&1
git -C "$WORKDIR/nowavedir" commit -q -m "no wave dir" >/dev/null 2>&1

BASE=$(run_all "$TOOL")
printf '%s\n' "$BASE" | sed 's/^/BASE /'

mk_mutant() { # name sed-expr
    _name=$1; _expr=$2
    sed "$_expr" "$TOOL" >"$WORKDIR/$_name.sh" || return 1
    chmod +x "$WORKDIR/$_name.sh"
    return 0
}

check_mutant() { # name
    _name=$1
    _out=$(run_all "$WORKDIR/$_name.sh")
    _diffs=$(printf '%s\n' "$BASE" | while IFS= read -r line; do
        _k=${line%%=*}
        _b=${line#*=}
        _m=$(printf '%s\n' "$_out" | awk -F= -v k="$_k" '$1 == k { print $2 }')
        [ "$_b" != "$_m" ] && printf '%s:%s->%s ' "$_k" "$_b" "$_m"
    done)
    if [ -n "$_diffs" ]; then
        printf 'MUTANT %-28s CAUGHT   %s\n' "$_name" "$_diffs"
        CAUGHT=$((CAUGHT + 1))
    else
        printf 'MUTANT %-28s SURVIVED (equivalent on every case)\n' "$_name"
        SURVIVED=$((SURVIVED + 1))
    fi
}

mk_mutant m1_no_order_check \
    's/if \[ -n "$REPORT_CT" \] && \[ "$REPORT_CT" -lt "$ledger_ct" \]; then/if false; then/' || exit 2
mk_mutant m2_ledger_fail_to_warn \
    's/add_finding FAIL no_wave_done_ledger/add_finding WARN no_wave_done_ledger/' || exit 2
mk_mutant m3_frozen_fail_to_warn \
    's/add_finding FAIL frozen_paths_empty/add_finding WARN frozen_paths_empty/' || exit 2
mk_mutant m4_force_exit_zero \
    's/^    RC=1$/    RC=0/' || exit 2
mk_mutant m5_wave_dir_ignored \
    's|^if \[ ! -d "$WAVE_DIR" \]; then|if false; then|' || exit 2
mk_mutant m6_report_presence_ignored \
    's|^for spec in "$FLEET:$FLEET_REV" "$LANE:$REV"; do|for spec in ; do|' || exit 2

for m in m1_no_order_check m2_ledger_fail_to_warn m3_frozen_fail_to_warn \
         m4_force_exit_zero m5_wave_dir_ignored m6_report_presence_ignored; do
    check_mutant "$m"
done

printf 'MUTANTS caught=%s survived=%s\n' "$CAUGHT" "$SURVIVED"
[ "$SURVIVED" -eq 0 ] || exit 1
exit 0
