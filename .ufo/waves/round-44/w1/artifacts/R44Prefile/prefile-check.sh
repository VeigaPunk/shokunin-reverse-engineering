#!/bin/sh
# prefile-check.sh — kaidoku round-N pre-file gate (file-only-after-WAVE-DONE).
#
# Re-runs the lane's pre-file gate machinery in the shape round 41 closure D1
# and QUALITY #47 require, and that the round-44 prompt restates as
# "File only after WAVE-DONE" (run-9 lesson, 9 incidents): the round report
# may be filed only after every launched wave has settled.
#
# Three binding conditions:
#
#   (a) every launched wave carries its WAVE-DONE signal — the
#       `<wave>-results.json` handoff ledger beside the dispatch file, named by
#       the wave id and committed at the measured revision. A wave is
#       "launched" when `<lane>/.ufo/waves/round-N/<wave>.ready` exists.
#   (b) the report path `.ufo/reports/round-N/kaidoku.md` exists only after all
#       launched waves are done: when the report is committed, every launched
#       wave's ledger must be committed, and the report's FIRST filing commit
#       must not predate any wave's ledger commit (round-41 closure D1:
#       the report was filed at 18:29:41, wave 2 settled at 18:44:28).
#   (c) the claims file's frozen-paths list is non-empty — the
#       `## Frozen paths` section of `plans/round-N-claims.md` names at least
#       one path.
#
# Read-only: no git write, no file creation except --json-out and the
# selftest's TMPDIR fixtures. GIT_OPTIONAL_LOCKS=0 keeps `git status` from
# refreshing the index.
#
# Exit codes are semantic: 0 met/clean · 1 failed · 2 could-not-evaluate
# (usage error, missing tree, unreadable git). A 2 never counts toward the
# target.
#
# usage:
#   prefile-check.sh --lane LANE_ROOT [--fleet FLEET_ROOT] [--round N]
#                     [--report-path RELPATH] [--rev REV] [--json-out FILE]
#   prefile-check.sh --selftest [--work DIR]
#
# The measured revision defaults to the LANE BRANCH TIP (`refs/heads/main`),
# never bare HEAD (the lane's HEAD is detached after the first helper commit);
# --rev overrides it. The fleet tip is read the same way.

set -u

PROG=prefile-check.sh
LANE=""
FLEET=""
ROUND=44
REPORT_REL=""
REV=""
JSON_OUT=""
SELFTEST=0
WORK=""

TMPBASE=${TMPDIR:-/tmp}
[ -d "$TMPBASE" ] || TMPBASE=/tmp

# ---------------------------------------------------------------- findings --

FIND_SEV=""
FIND_KEY=""
FIND_MSG=""

say() { printf '%s\n' "$*"; }

add_finding() { # severity key message
    FIND_SEV="$1"
    FIND_KEY="$2"
    FIND_MSG="$3"
    printf '%s\t%s\t%s\n' "$FIND_SEV" "$FIND_KEY" "$FIND_MSG" >>"$FINDINGS_FILE"
    case "$FIND_SEV" in
        FAIL) say "FAIL $FIND_KEY: $FIND_MSG" ;;
        WARN) say "WARN $FIND_KEY: $FIND_MSG" ;;
        *)    say "PASS $FIND_KEY: $FIND_MSG" ;;
    esac
}

usage() {
    cat >&2 <<EOF
usage: $PROG --lane LANE_ROOT [--fleet FLEET_ROOT] [--round N]
       $PROG --selftest [--work DIR]

  --lane LANE_ROOT    lane repo to inspect (default: derived from \$0's repo)
  --fleet FLEET_ROOT  fleet repo holding .ufo/reports/round-N/ (default: the
                      lane root's parent)
  --round N           round number (default: 44)
  --report-path REL   report path relative to a repo root
                      (default: .ufo/reports/round-N/kaidoku.md)
  --rev REV           measured revision (default: the lane branch tip)
  --json-out FILE     write a JSON receipt to FILE
  --selftest          run the sandbox fixtures (no lane needed)
  --work DIR          directory for selftest fixtures (default: TMPDIR)
EOF
    exit 2
}

# ------------------------------------------------------------------- args --

while [ $# -gt 0 ]; do
    case "$1" in
        --lane)        LANE=${2:-}; shift 2 || usage ;;
        --fleet)       FLEET=${2:-}; shift 2 || usage ;;
        --round)       ROUND=${2:-}; shift 2 || usage ;;
        --report-path) REPORT_REL=${2:-}; shift 2 || usage ;;
        --rev)         REV=${2:-}; shift 2 || usage ;;
        --json-out)    JSON_OUT=${2:-}; shift 2 || usage ;;
        --work)        WORK=${2:-}; shift 2 || usage ;;
        --selftest)    SELFTEST=1; shift ;;
        -h|--help)     usage ;;
        *)             say "$PROG: unknown argument: $1" >&2; usage ;;
    esac
done

# ----------------------------------------------------------------- selftest --

if [ "$SELFTEST" -eq 1 ]; then
    SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
    SELF="$SELF_DIR/$(basename -- "$0")"
    [ -f "$SELF" ] || SELF=$0

    fx_root() { # name -> creates and prints a fixture dir
        _d=$(mktemp -d "${WORK:-$TMPBASE}/$1.XXXXXX") || return 1
        mkdir -p "$_d"
        printf '%s\n' "$_d"
    }

    fx_init() { # dir  (git init + identity; asserts the toplevel is the fixture)
        _d=$1
        git -C "$_d" init -q -b main 2>/dev/null || return 1
        _top=$(git -C "$_d" rev-parse --show-toplevel 2>/dev/null) || return 1
        _top=$(CDPATH= cd -- "$_top" && pwd -P)
        _here=$(CDPATH= cd -- "$_d" && pwd -P)
        [ "$_top" = "$_here" ] || {
            echo "fixture toplevel mismatch: $_top != $_here" >&2
            return 1
        }
        git -C "$_d" config user.name fx
        git -C "$_d" config user.email fx@fx
        git -C "$_d" config commit.gpgsign false
        return 0
    }

    fx_commit() { # dir date message
        _d=$1; _dt=$2; _msg=$3
        git -C "$_d" add -A >/dev/null 2>&1
        GIT_AUTHOR_DATE="$_dt" GIT_COMMITTER_DATE="$_dt" \
            git -C "$_d" commit -q --allow-empty -m "$_msg" >/dev/null 2>&1 \
            || return 1
        return 0
    }

    fx_lane() { # dir  — a lane repo with a settled wave and a claims file
        _d=$1
        mkdir -p "$_d/.ufo/waves/round-44"
        mkdir -p "$_d/plans"
        cat >"$_d/.ufo/waves/round-44/w1.ready" <<'EOF'
{"lane": "kaidoku", "round": 44, "wave": "r44-w1", "dispatch": "/tmp/w1-dispatch.json", "l1": "KaidokuR44"}
EOF
        : >"$_d/.ufo/waves/round-44/w1.ready.dispatched"
        cat >"$_d/.ufo/waves/round-44/r44-w1-results.json" <<'EOF'
{"lane": "kaidoku", "round": 44, "wave": "r44-w1", "seats": 1, "results": [{"name": "S1", "agent": "executor", "output": "ok", "note": null}]}
EOF
        cat >"$_d/plans/round-44-claims.md" <<'EOF'
# kaidoku round 44 — frozen claims

## Frozen paths

This file; `tools/round-44/*`; `plans/round-44-claims.md`; `corpus/SOURCES.md`.
EOF
    }

    fx_lane_no_ledger() { # dir — same, but the wave never settled
        _d=$1
        mkdir -p "$_d/.ufo/waves/round-44" "$_d/plans"
        cat >"$_d/.ufo/waves/round-44/w1.ready" <<'EOF'
{"lane": "kaidoku", "round": 44, "wave": "r44-w1", "dispatch": "/tmp/w1-dispatch.json", "l1": "KaidokuR44"}
EOF
        : >"$_d/.ufo/waves/round-44/w1.ready.dispatched"
        cat >"$_d/plans/round-44-claims.md" <<'EOF'
# kaidoku round 44 — frozen claims

## Frozen paths

This file; `tools/round-44/*`.
EOF
    }

    fx_lane_empty_frozen() { # dir — claims file with an empty frozen-paths list
        _d=$1
        fx_lane "$_d"
        cat >"$_d/plans/round-44-claims.md" <<'EOF'
# kaidoku round 44 — frozen claims

## Frozen paths

Nothing is frozen yet.
EOF
    }

    selftest_pass=0
    selftest_fail=0

    st_case() { # name expect_exit lane fleet
        _name=$1; _exp=$2; _ln=$3; _fl=$4
        out=$(sh "$SELF" --lane "$_ln" --fleet "$_fl" --round 44 2>&1)
        rc=$?
        if [ "$rc" -eq "$_exp" ]; then
            printf 'SELFTEST PASS %-42s expect=%s got=%s\n' "$_name" "$_exp" "$rc"
            selftest_pass=$((selftest_pass + 1))
        else
            printf 'SELFTEST FAIL %-42s expect=%s got=%s\n' "$_name" "$_exp" "$rc"
            printf '%s\n' "$out" | sed 's/^/    /'
            selftest_fail=$((selftest_fail + 1))
        fi
    }

    T1=$(fx_root "prefile-green") || exit 2
    T2=$(fx_root "prefile-noledger") || exit 2
    T3=$(fx_root "prefile-order") || exit 2
    T4=$(fx_root "prefile-emptyfrozen") || exit 2
    T5=$(fx_root "prefile-usage") || exit 2

    for d in "$T1" "$T2" "$T3" "$T4"; do fx_init "$d" || exit 2; done
    fx_init "$T5" || exit 2

    # green: wave settled, no report filed yet
    fx_lane "$T1"
    fx_commit "$T1" "2026-10-28T10:00:00+00:00" "wave 1 settled" || exit 2
    mkdir -p "$T1/fleet"; fx_init "$T1/fleet" || exit 2
    fx_commit "$T1/fleet" "2026-10-28T10:00:00+00:00" "fleet base" || exit 2

    # red: a launched wave never settled
    fx_lane_no_ledger "$T2"
    fx_commit "$T2" "2026-10-28T10:00:00+00:00" "wave 1 launched" || exit 2
    mkdir -p "$T2/fleet"; fx_init "$T2/fleet" || exit 2
    fx_commit "$T2/fleet" "2026-10-28T10:00:00+00:00" "fleet base" || exit 2

    # red: the report was committed BEFORE the wave ledger settled (D1 shape)
    fx_lane "$T3"
    # the lane's first commit carries the ready file but not the ledger
    rm -f "$T3/.ufo/waves/round-44/r44-w1-results.json"
    fx_commit "$T3" "2026-10-28T12:00:00+00:00" "lane: wave 1 launched" || exit 2
    mkdir -p "$T3/fleet/.ufo/reports/round-44"
    fx_init "$T3/fleet" || exit 2
    cat >"$T3/fleet/.ufo/reports/round-44/kaidoku.md" <<'EOF'
# kaidoku — round 44
EOF
    fx_commit "$T3/fleet" "2026-10-28T12:15:00+00:00" "round-44: kaidoku report" || exit 2
    # the wave ledger lands AFTER the report was filed
    cat >"$T3/.ufo/waves/round-44/r44-w1-results.json" <<'EOF'
{"lane": "kaidoku", "round": 44, "wave": "r44-w1", "seats": 1, "results": [{"name": "S1", "agent": "executor", "output": "ok", "note": null}]}
EOF
    fx_commit "$T3" "2026-10-28T12:30:00+00:00" "lane: wave 1 settled" || exit 2

    # red: the claims file has an empty frozen-paths list
    fx_lane_empty_frozen "$T4"
    fx_commit "$T4" "2026-10-28T10:00:00+00:00" "wave 1 settled" || exit 2
    mkdir -p "$T4/fleet"; fx_init "$T4/fleet" || exit 2
    fx_commit "$T4/fleet" "2026-10-28T10:00:00+00:00" "fleet base" || exit 2

    st_case green-wave-settled-no-report 0 "$T1" "$T1/fleet"
    st_case red-wave-never-settled 1 "$T2" "$T2/fleet"
    st_case red-report-filed-before-wave-done 1 "$T3" "$T3/fleet"
    st_case red-empty-frozen-paths 1 "$T4" "$T4/fleet"

    # usage: a lane root that is not a git work tree -> could-not-evaluate
    out=$(sh "$SELF" --lane "$T5/not-a-repo" --fleet "$T5" --round 44 2>&1)
    rc=$?
    if [ "$rc" -eq 2 ]; then
        printf 'SELFTEST PASS %-42s expect=2 got=2\n' "red-unusable-lane-root"
        selftest_pass=$((selftest_pass + 1))
    else
        printf 'SELFTEST FAIL %-42s expect=2 got=%s\n' "red-unusable-lane-root" "$rc"
        selftest_fail=$((selftest_fail + 1))
    fi

    rm -rf "$T1" "$T2" "$T3" "$T4" "$T5"

    printf 'SELFTEST cases=%s pass=%s fail=%s\n' \
        "$((selftest_pass + selftest_fail))" "$selftest_pass" "$selftest_fail"
    [ "$selftest_fail" -eq 0 ] || exit 1
    exit 0
fi

# ------------------------------------------------------------------- main --

if [ -z "$LANE" ]; then
    cand=$(CDPATH= cd -- "$(dirname -- "$0")/../.." 2>/dev/null && pwd -P) || cand=""
    if [ -n "$cand" ] && [ -d "$cand/.git" ]; then
        LANE=$cand
    elif [ -d "$PWD/.git" ]; then
        LANE=$PWD
    else
        say "$PROG: --lane is required (or run from a git work tree)" >&2
        usage
    fi
fi
[ -d "$LANE" ] || { say "$PROG: lane root not found: $LANE" >&2; exit 2; }
[ -n "$FLEET" ] || FLEET=$(CDPATH= cd -- "$LANE/.." && pwd -P)
[ -d "$FLEET" ] || { say "$PROG: fleet root not found: $FLEET" >&2; exit 2; }
[ -n "$REPORT_REL" ] || REPORT_REL=".ufo/reports/round-$ROUND/kaidoku.md"

export GIT_OPTIONAL_LOCKS=0
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE

git_ok() { git -C "$1" rev-parse --git-dir >/dev/null 2>&1; }

if ! git_ok "$LANE"; then
    say "$PROG: lane root is not a git work tree: $LANE" >&2
    exit 2
fi
if ! git_ok "$FLEET"; then
    say "$PROG: fleet root is not a git work tree: $FLEET" >&2
    exit 2
fi

# The lane tip is the branch tip, never bare HEAD (detached after the first
# helper commit). Fall back to HEAD only when the branch does not exist.
lane_tip() {
    _t=$(git -C "$LANE" rev-parse --verify --quiet refs/heads/main 2>/dev/null) || _t=""
    [ -n "$_t" ] || _t=$(git -C "$LANE" rev-parse --verify --quiet HEAD 2>/dev/null) || _t=""
    printf '%s\n' "$_t"
}
fleet_tip() {
    _t=$(git -C "$FLEET" rev-parse --verify --quiet refs/heads/main 2>/dev/null) || _t=""
    [ -n "$_t" ] || _t=$(git -C "$FLEET" rev-parse --verify --quiet HEAD 2>/dev/null) || _t=""
    printf '%s\n' "$_t"
}

if [ -z "$REV" ]; then
    REV=$(lane_tip)
else
    git -C "$LANE" cat-file -e "$REV^{commit}" 2>/dev/null || {
        say "$PROG: --rev is not a commit in the lane: $REV" >&2
        exit 2
    }
fi
[ -n "$REV" ] || { say "$PROG: cannot resolve the lane tip" >&2; exit 2; }
FLEET_REV=$(fleet_tip)
[ -n "$FLEET_REV" ] || { say "$PROG: cannot resolve the fleet tip" >&2; exit 2; }

WORKTREE_REV=$(git -C "$LANE" rev-parse --verify --quiet HEAD 2>/dev/null) || WORKTREE_REV=""
if [ -n "$WORKTREE_REV" ] && [ "$WORKTREE_REV" != "$REV" ]; then
    say "WARN branch_tip_lags_worktree: measuring $REV, HEAD is $WORKTREE_REV"
fi

WAVE_DIR_REL=".ufo/waves/round-$ROUND"
WAVE_DIR="$LANE/$WAVE_DIR_REL"

FINDINGS_FILE=$(mktemp "${TMPBASE}/prefile-findings.XXXXXX") || exit 2
trap 'rm -f "$FINDINGS_FILE"' EXIT INT TERM

say "prefile: lane=$LANE fleet=$FLEET round=$ROUND rev=$REV fleet_rev=$FLEET_REV"

# ------------------------------------------------------------- condition (a) --

WAVE_COUNT=0
SETTLED=0
UNSETTLED_KEYS=""

if [ ! -d "$WAVE_DIR" ]; then
    add_finding FAIL wave_dir_missing "no $WAVE_DIR_REL directory in the lane"
else
    for ready in "$WAVE_DIR"/*.ready; do
        [ -f "$ready" ] || continue
        base=$(basename "$ready" .ready)
        WAVE_COUNT=$((WAVE_COUNT + 1))
        wave_id=$(sed -n 's/.*"wave"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$ready" | head -n1)
        if [ -z "$wave_id" ]; then
            add_finding FAIL malformed_ready_file \
                "$base.ready does not name a wave id (WAVE-DONE signal undecidable)"
            UNSETTLED_KEYS="$UNSETTLED_KEYS $base"
            continue
        fi
        if [ ! -e "$WAVE_DIR/$base.ready.dispatched" ]; then
            add_finding WARN wave_not_dispatched \
                "$wave_id has a ready file but no $base.ready.dispatched marker"
        fi
        ledger=""
        for cand in "$WAVE_DIR/$wave_id-results.json" "$WAVE_DIR/$base-results.json"; do
            if [ -f "$cand" ]; then ledger="$cand"; break; fi
        done
        if [ -z "$ledger" ]; then
            add_finding FAIL no_wave_done_ledger \
                "$wave_id has no WAVE-DONE results ledger in $WAVE_DIR_REL"
            UNSETTLED_KEYS="$UNSETTLED_KEYS $base"
            continue
        fi
        ledger_rel="$WAVE_DIR_REL/$(basename "$ledger")"
        if ! git -C "$LANE" cat-file -e "$REV:$ledger_rel" 2>/dev/null; then
            if git -C "$LANE" cat-file -e "HEAD:$ledger_rel" 2>/dev/null; then
                add_finding FAIL results_not_at_branch_tip \
                    "$wave_id ledger $ledger_rel is committed but not at the measured rev $REV"
            else
                add_finding FAIL results_not_committed \
                    "$wave_id ledger $ledger_rel is not committed in the lane"
            fi
            UNSETTLED_KEYS="$UNSETTLED_KEYS $base"
            continue
        fi
        if ! grep -q "\"$wave_id\"" "$ledger"; then
            add_finding FAIL ledger_wave_mismatch \
                "$ledger_rel does not name wave $wave_id"
            UNSETTLED_KEYS="$UNSETTLED_KEYS $base"
            continue
        fi
        seats=$(sed -n 's/.*"seats"[[:space:]]*:[[:space:]]*\([0-9][0-9]*\).*/\1/p' "$ledger" | head -n1)
        names=$(grep -o '"name"' "$ledger" | wc -l | tr -d ' ')
        if [ -n "$seats" ] && [ "$seats" -gt 0 ] && [ "$seats" != "$names" ]; then
            add_finding WARN ledger_seat_count_mismatch \
                "$ledger_rel declares seats=$seats but lists $names seat entries"
        fi
        SETTLED=$((SETTLED + 1))
    done
    if [ "$WAVE_COUNT" -eq 0 ]; then
        add_finding FAIL no_launched_wave "no <wave>.ready file in $WAVE_DIR_REL"
    elif [ "$SETTLED" -eq "$WAVE_COUNT" ]; then
        add_finding PASS waves_settled "$SETTLED/$WAVE_COUNT launched waves carry a committed WAVE-DONE ledger"
    else
        add_finding FAIL waves_settled "$SETTLED/$WAVE_COUNT launched waves carry a committed WAVE-DONE ledger"
    fi
fi

# ------------------------------------------------------------- condition (b) --

REPORT_STATE=absent
REPORT_ROOT=""
REPORT_CT=""

# The report lands on the fleet repo (.ufo/reports/round-N/<lane>.md); the lane
# is checked too so a lane-side copy cannot hide an early filing.
for spec in "$FLEET:$FLEET_REV" "$LANE:$REV"; do
    cand_root=${spec%%:*}
    cand_rev=${spec#*:}
    if git -C "$cand_root" cat-file -e "$cand_rev:$REPORT_REL" 2>/dev/null; then
        REPORT_STATE=committed
        REPORT_ROOT=$cand_root
        REPORT_CT=$(git -C "$cand_root" log --full-history --diff-filter=A --format=%ct -- "$REPORT_REL" 2>/dev/null | tail -n1)
        break
    fi
    if [ -f "$cand_root/$REPORT_REL" ] && [ "$REPORT_STATE" = "absent" ]; then
        REPORT_STATE=worktree
        REPORT_ROOT=$cand_root
    fi
done

if [ "$REPORT_STATE" = "absent" ]; then
    if [ -n "$UNSETTLED_KEYS" ]; then
        add_finding WARN report_not_filed_but_wave_unsettled \
            "$REPORT_REL is not present, but launched wave(s)$UNSETTLED_KEYS still lack a WAVE-DONE ledger (filing is blocked by no_wave_done_ledger)"
    else
        add_finding PASS report_not_filed_yet \
            "$REPORT_REL is not present and every launched wave settled; filing is permitted"
    fi
elif [ "$REPORT_STATE" = "worktree" ]; then
    add_finding WARN report_uncommitted \
        "$REPORT_REL exists in $REPORT_ROOT but is not committed; ordering is not yet decidable"
else
    add_finding PASS report_committed "$REPORT_REL is committed in $REPORT_ROOT (first filing ct=$REPORT_CT)"
    if [ -n "$UNSETTLED_KEYS" ]; then
        add_finding FAIL report_exists_but_wave_unsettled \
            "$REPORT_REL is committed while launched wave(s)$UNSETTLED_KEYS have no WAVE-DONE ledger"
    fi
    for ready in "$WAVE_DIR"/*.ready; do
        [ -f "$ready" ] || continue
        base=$(basename "$ready" .ready)
        wave_id=$(sed -n 's/.*"wave"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$ready" | head -n1)
        [ -n "$wave_id" ] || continue
        ledger_rel=""
        for cand in "$WAVE_DIR_REL/$wave_id-results.json" "$WAVE_DIR_REL/$base-results.json"; do
            if git -C "$LANE" cat-file -e "$REV:$cand" 2>/dev/null; then ledger_rel=$cand; break; fi
        done
        [ -n "$ledger_rel" ] || continue
        ledger_ct=$(git -C "$LANE" log --full-history --diff-filter=A --format=%ct -- "$ledger_rel" 2>/dev/null | tail -n1)
        [ -n "$ledger_ct" ] || continue
        if [ -n "$REPORT_CT" ] && [ "$REPORT_CT" -lt "$ledger_ct" ]; then
            add_finding FAIL report_filed_before_wave_done \
                "$REPORT_REL was first filed at ct=$REPORT_CT, before $wave_id settled at ct=$ledger_ct"
        else
            add_finding PASS report_after_wave_done \
                "$wave_id settled at ct=$ledger_ct, report first filed at ct=$REPORT_CT"
        fi
    done
fi

# ------------------------------------------------------------- condition (c) --

CLAIMS_REL="plans/round-$ROUND-claims.md"
CLAIMS_SRC=""
if git -C "$LANE" cat-file -e "$REV:$CLAIMS_REL" 2>/dev/null; then
    CLAIMS_SRC=$REV
elif [ -f "$LANE/$CLAIMS_REL" ]; then
    CLAIMS_SRC=worktree
else
    CLAIMS_SRC=""
fi

if [ -z "$CLAIMS_SRC" ]; then
    add_finding FAIL claims_file_absent "$CLAIMS_REL is absent from the lane"
else
    if [ "$CLAIMS_SRC" = "worktree" ]; then
        add_finding WARN claims_not_committed "$CLAIMS_REL is not committed at $REV; reading the worktree copy"
    fi
    if [ "$CLAIMS_SRC" = "$REV" ]; then
        claims_text=$(git -C "$LANE" show "$REV:$CLAIMS_REL" 2>/dev/null)
    else
        claims_text=$(cat "$LANE/$CLAIMS_REL" 2>/dev/null)
    fi
    frozen_paths=$(printf '%s\n' "$claims_text" | awk '
        /^## .*[Ff]rozen path/ { insec = 1; next }
        insec && /^## / { insec = 0 }
        insec { print }
    ' | grep -o '`[^`]*`' | tr -d '`' | grep -v ' ' | grep -E '/|\.(md|py|json|sh|tsv|txt|bin|csv|ya?ml)$' | sort -u)
    n_frozen=$(printf '%s\n' "$frozen_paths" | grep -c . )
    if [ "$n_frozen" -eq 0 ]; then
        add_finding FAIL frozen_paths_empty \
            "$CLAIMS_REL has no path in its '## Frozen paths' section"
    else
        add_finding PASS frozen_paths_nonempty \
            "$CLAIMS_REL names $n_frozen frozen path(s)"
        resolved=0
        for p in $frozen_paths; do
            n=$(git -C "$LANE" ls-tree -r --name-only "$REV" -- "$p" 2>/dev/null | grep -c .)
            [ "$n" -gt 0 ] && resolved=$((resolved + 1))
        done
        if [ "$resolved" -eq 0 ]; then
            add_finding WARN frozen_paths_resolution \
                "none of the $n_frozen frozen path(s) in $CLAIMS_REL resolves at $REV (advisory)"
        else
            add_finding WARN frozen_paths_resolution \
                "$resolved/$n_frozen frozen path(s) resolve at $REV (advisory; a directory or glob pathspec counts as resolved)"
        fi
    fi
fi

# ------------------------------------------------------------------ verdict --

FAILED_KEYS=$(cut -f1,2 "$FINDINGS_FILE" | awk -F'\t' '$1 == "FAIL" { print $2 }' | tr '\n' ' ')
N_FAIL=$(cut -f1 "$FINDINGS_FILE" | grep -c '^FAIL$' || true)
N_WARN=$(cut -f1 "$FINDINGS_FILE" | grep -c '^WARN$' || true)

if [ "$N_FAIL" -gt 0 ]; then
    VERDICT=RED
    RC=1
else
    VERDICT=GREEN
    RC=0
fi

say "prefile: waves_launched=$WAVE_COUNT waves_settled=$SETTLED report_state=$REPORT_STATE"
say "prefile: findings: $N_FAIL FAIL, $N_WARN WARN"
say "prefile: verdict=$VERDICT"

if [ -n "$JSON_OUT" ]; then
    json_escape() { printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'; }
    {
        printf '{\n'
        printf '  "tool": "%s",\n' "$PROG"
        printf '  "lane": "%s",\n' "$(json_escape "$LANE")"
        printf '  "fleet": "%s",\n' "$(json_escape "$FLEET")"
        printf '  "round": %s,\n' "$ROUND"
        printf '  "rev": "%s",\n' "$REV"
        printf '  "fleet_rev": "%s",\n' "$FLEET_REV"
        printf '  "report_path": "%s",\n' "$(json_escape "$REPORT_REL")"
        printf '  "report_state": "%s",\n' "$REPORT_STATE"
        printf '  "waves_launched": %s,\n' "$WAVE_COUNT"
        printf '  "waves_settled": %s,\n' "$SETTLED"
        printf '  "findings": [\n'
        first=1
        while IFS=$(printf '\t') read -r sev key msg; do
            [ -n "$sev" ] || continue
            [ "$first" -eq 1 ] || printf ',\n'
            first=0
            printf '    {"severity": "%s", "key": "%s", "message": "%s"}' \
                "$sev" "$(json_escape "$key")" "$(json_escape "$msg")"
        done <"$FINDINGS_FILE"
        printf '\n  ],\n'
        printf '  "failed_keys": "%s",\n' "$(json_escape "$(printf '%s' "$FAILED_KEYS" | sed 's/ *$//')")"
        printf '  "verdict": "%s",\n' "$VERDICT"
        printf '  "exit_code": %s\n' "$RC"
        printf '}\n'
    } >"$JSON_OUT" || { say "$PROG: cannot write $JSON_OUT" >&2; exit 2; }
    say "prefile: json receipt -> $JSON_OUT"
fi

exit "$RC"
