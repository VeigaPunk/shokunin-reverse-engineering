#!/usr/bin/env bash
# sources-census.sh — fleet-wide corpus/SOURCES.md census, validation, recheck queue.
# Conforms to SOURCES-CONTRACT-v1: one registry table, 11 columns => NF=13,
# statuses queued|mined|rejected ("watch" is NOT a status; recheck carries cadence),
# community is never tier A.
# Read-only: parses shokunin.conf LANES rows textually (never sources the conf),
# reads corpus/SOURCES.md, writes only stdout or --out; selftest uses cleaned temp files.
# Bash + coreutils + gawk.
#
#   sources-census.sh [mode] [lane-or-dir ...] [--root DIR] [--file PATH]
#                     [--today YYYY-MM-DD] [--out PATH] [--verbose]
#   modes:  census (default) | validate | overdue | shared | selftest
#   lanes:  lane ids from conf or root *-shokunin dirs, or explicit lane dirs
#   default targets: child repositories only; conf entries with repo "." are excluded.
#                     use --file or an explicit directory for a specific registry.
#   exit:   0 clean or warnings · 1 E/overdue findings (or census missing)
#           · 2 usage/env/missing registry · 3 selftest failure; W-codes and unlisted
#             lanes never change status (validate missing registry returns 2).
#
# Output: TSV on stdout — lane<TAB>metric|code<TAB>value…
#   census:   rows | tier.A|tier.B|tier.C|tier.invalid
#             | status.queued|status.mined|status.rejected|status.invalid
#             | missing | FLEET.rows | FLEET.tier.X | FLEET.status.X | FLEET.missing
#   validate: E01 malformed row (NF!=13)         E02 id not S[0-9]{3,}
#             E03 duplicate id                   E04 duplicate URL+scope (no supersedes)
#             E05 kind enum violation            E06 tier enum violation
#             E07 status enum violation          E08 opened not a past/present ISO date
#             E09 invalid recheck (ISO date, NNd, or symbolic cadence)
#             E10 community at tier A            E11 used-by path missing on disk
#             E12 row-shaped source outside the ## Registry section
#             W01 tier-C mined with non-— used-by   W02 rejected row, thin teaches
#             W03 mined row with used-by = — (warnings do not affect clean lanes)
#             W04 same URL across scopes (warnings do not affect clean lanes)
#   overdue:  overdue<SPC>id<SPC><days>d<SPC>recheck=<x><SPC>opened=<x> — ISO recheck
#             dates or NNd cadence (due = opened + N days); report on/after due date.
#             cadence<SPC>id<SPC>recheck=<x> — symbolic cadences (e.g. on-release)
#             are reported, never judged overdue.
#   shared:   url<TAB>shared<TAB>lane,lane,… — normalized URL present in >=2 lanes.

# Maintained parser accepts 0–3 leading ASCII spaces before Markdown rows/headings;
# 4 or more spaces are indented code and ignored. Frozen manual examples assume
# column-zero input.
set -u
MODE=census; OUT=""; FILE=""; ROOT=""; ROOT_SET=0; VERBOSE=0; TODAY=""
declare -a LANES_WANT=()

usage() { sed -n '2,38p' "$0"; }
die() { echo "ERROR: $*" >&2; exit 2; }
iso_epoch() {
  gawk -v input="$1" '
    function epoch(s,   a,y,m,d,t) {
      if (s !~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/) return -1e15
      split(s,a,"-"); y=a[1]+0; m=a[2]+0; d=a[3]+0
      if (y==0) return -1e15
      t=mktime(sprintf("%04d %02d %02d 00 00 00",y,m,d),1)
      if (strftime("%Y-%m-%d",t,1)!=s) return -1e15
      return t
    }
    BEGIN {
      t=epoch(input)
      if (t==-1e15) exit 1
      printf "%.0f\n",t
    }'
}

while [ $# -gt 0 ]; do
  case "$1" in
    census|validate|overdue|shared|selftest) MODE=$1; shift ;;
    --file)
      [ $# -ge 2 ] || die "--file needs a path"
      FILE=$2; shift 2 ;;
    --root)
      [ $# -ge 2 ] || die "--root needs a path"
      ROOT=$2; ROOT_SET=1; shift 2 ;;
    --today)
      [ $# -ge 2 ] || die "--today needs a date"
      TODAY=$2; shift 2 ;;
    --out)
      [ $# -ge 2 ] || die "--out needs a path"
      OUT=$2; shift 2 ;;
    --verbose) VERBOSE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "ERROR: unknown option $1" >&2; exit 2 ;;
    *)  LANES_WANT+=("$1"); shift ;;
  esac
done

[ -n "$ROOT" ] || ROOT=${SHOKUNIN_ROOT:-$(realpath -- "$(dirname -- "$0")/..")}
[ -d "$ROOT" ] || die "root not a directory: $ROOT"
TODAY=${TODAY:-$(date -u +%F)}
TODAY_S=$(iso_epoch "$TODAY") || die "--today not an ISO date: $TODAY"


emit() { if [ -n "$OUT" ]; then printf '%s\n' "$*" >> "$OUT"; else printf '%s\n' "$*"; fi; }
out_sink() { if [ -n "$OUT" ]; then cat >> "$OUT"; else cat; fi }

# ---------------------------------------------------------------- selftest ---
if [ "$MODE" = selftest ]; then
  FIX=$(realpath -- "$(dirname -- "$0")/fixtures/sources-census")
  [ -d "$FIX" ] || { echo "selftest: fixtures missing: $FIX" >&2; exit 3; }
  froot="$FIX/root"; fail=0
  check() { # <label> <cmd...> — stdout must contain the literal pattern
    local label=$1; local want=$2; shift 2
    if "$@" | grep -qF -- "$want"; then
      printf 'killed\t%s\n' "$label"
    else
      printf 'SURVIVED\t%s\n' "$label"; fail=1
    fi
  }
  checkx() { # <label> <expected-exit> <cmd...>
    local label=$1 want=$2; shift 2
    "$@" >/dev/null 2>&1; local rc=$?
    if [ "$rc" = "$want" ]; then printf 'killed\t%s\n' "$label"
    else printf 'SURVIVED\t%s (exit %s, want %s)\n' "$label" "$rc" "$want"; fail=1; fi
  }
  checkline() { # <label> <exact-line> <cmd...>
    local label=$1 expected=$2; shift 2
    local output
    output=$("$@" 2>/dev/null) || :
    if printf '%s\n' "$output" | grep -Fqx -- "$expected"; then
      printf 'killed\t%s\n' "$label"
    else
      printf 'SURVIVED\t%s\n' "$label"; fail=1
    fi
  }
  check "E01-malformed-row"    "E01" "$0" validate --today 2026-10-19 --root "$froot" a
  check "E02-malformed-id"     "E02" "$0" validate --today 2026-10-19 --root "$froot" a
  check "E03-duplicate-id"     "E03" "$0" validate --today 2026-10-19 --root "$froot" a
  check "E04-duplicate-url"    "E04" "$0" validate --today 2026-10-19 --root "$froot" a
  check "E05-bad-kind"         "E05" "$0" validate --today 2026-10-19 --root "$froot" a
  check "E06-bad-tier"         "E06" "$0" validate --today 2026-10-19 --root "$froot" a
  check "E07-bad-status"       "E07" "$0" validate --today 2026-10-19 --root "$froot" a
  check "E08-future-opened"    "E08" "$0" validate --today 2026-10-19 --root "$froot" a
  check "E09-bad-recheck"      "E09" "$0" validate --today 2026-10-19 --root "$froot" a
  check "E10-community-at-A"   "E10" "$0" validate --today 2026-10-19 --root "$froot" a
  check "E11-dangling-usedby"  "E11" "$0" validate --today 2026-10-19 --root "$froot" a
  check "W01-tierC-mined"      "W01" "$0" validate --today 2026-10-19 --root "$froot" a
  check "W02-thin-reject"      "W02" "$0" validate --today 2026-10-19 --root "$froot" a
  check "W03-mined-unused"     "W03" "$0" validate --today 2026-10-19 --root "$froot" a
  check "clean-lane-ok"        "ok" "$0" validate --today 2026-10-19 --root "$froot" c
  checkx "validate-findings-exit-1" 1 "$0" validate --today 2026-10-19 --root "$froot" a
  checkx "validate-clean-exit-0"    0 "$0" validate --today 2026-10-19 --root "$froot" c
  check "validate-missing-line" $'d\tmissing' "$0" validate --today 2026-10-19 --root "$froot" d
  checkx "validate-missing-exit-2" 2 "$0" validate --today 2026-10-19 --root "$froot" d
  checkx "overdue-exit-1" 1 "$0" overdue --root "$froot" --today 2026-10-19 a b c z
  check "overdue-finds-row" "S002" "$0" overdue --root "$froot" --today 2026-10-19 a b c z
  check "cadence-due-on-opened-plus-N" "S002 0d" "$0" overdue --root "$froot" --today 2026-08-30 a
  check "symbolic-on-release-reported" "S015 recheck=on-release" "$0" overdue --root "$froot" --today 2026-08-01 a
  check "symbolic-annual-reported" "S016 recheck=annual" "$0" overdue --root "$froot" --today 2026-08-01 a
  checkx "invalid-recheck-not-overdue" 0 "$0" overdue --root "$froot" --today 2026-03-10 a
  checkx "overdue-clean-exit-0" 0 "$0" overdue --root "$froot" --today 2026-08-01 a b c z
  check "shared-across-lanes" "a,b" "$0" shared --root "$froot"
  check "census-missing" "missing" "$0" census --root "$froot"
  checkx "census-missing-exit-1" 1 "$0" census --root "$froot"
  check "unlisted-directory-warning" $'z\tunlisted' "$0" census --root "$froot"
  check "unlisted-validation-warning" $'z\tunlisted' "$0" validate --today 2026-10-19 --root "$froot" z
  checkx "unlisted-warning-not-failure" 0 "$0" validate --today 2026-10-19 --root "$froot" z
  check "W-only-warning-reported" "W02" "$0" validate --today 2026-10-19 --root "$froot" z
  checkx "W-only-registry-exit-0" 0 "$0" validate --today 2026-10-19 --root "$froot" z
  check "UTC-date-in-Sao-Paulo" $'z\tok' env TZ=America/Sao_Paulo "$0" validate --root "$froot" --today 2026-10-19 z
  checkx "UTC-date-in-Sao-Paulo-exit-0" 0 env TZ=America/Sao_Paulo "$0" validate --root "$froot" --today 2026-10-19 z
  check "explicit-lane-dir" "E05" "$0" validate --today 2026-10-19 "$froot/a-shokunin"

  test_root=$(mktemp -d "${TMPDIR:-/tmp}/sources-census.XXXXXX") || {
    echo "selftest: unable to create temporary directory" >&2; exit 3;
  }
  trap 'rm -rf "$test_root"' EXIT
  fleet_root="$test_root/fleet-root"
  mkdir -p "$fleet_root/known-shokunin/corpus" || exit 3
  cat > "$fleet_root/shokunin.conf" <<'EOF'
LANES="
known|known-shokunin|known fixture
missing|missing-shokunin|missing fixture
"
EOF
  cat > "$fleet_root/known-shokunin/corpus/SOURCES.md" <<'EOF'
# Known census totals

## Registry
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S001 | Queue one | docs | B | q1 | p1 | queued evidence one | queued | 2026-10-01 | 90d | — |
| S002 | Queue two | docs | B | q2 | p2 | queued evidence two | queued | 2026-10-01 | 90d | — |
| S003 | Mined | docs | B | m | p3 | mined evidence | mined | 2026-10-01 | 90d | — |
| S004 | Rejected | docs | B | r | p4 | rejected evidence | rejected | 2026-10-01 | 90d | — |
| S005 | Invalid | docs | B | i | p5 | invalid evidence | watch | 2026-10-01 | 90d | — |
EOF
  checkline "FLEET-rows" $'FLEET\trows\t5' "$0" census --root "$fleet_root"
  checkline "FLEET-tier-A" $'FLEET\ttier.A\t0' "$0" census --root "$fleet_root"
  checkline "FLEET-tier-B" $'FLEET\ttier.B\t5' "$0" census --root "$fleet_root"
  checkline "FLEET-tier-C" $'FLEET\ttier.C\t0' "$0" census --root "$fleet_root"
  checkline "FLEET-tier-invalid" $'FLEET\ttier.invalid\t0' "$0" census --root "$fleet_root"
  checkline "FLEET-status-queued" $'FLEET\tstatus.queued\t2' "$0" census --root "$fleet_root"
  checkline "FLEET-status-mined" $'FLEET\tstatus.mined\t1' "$0" census --root "$fleet_root"
  checkline "FLEET-status-rejected" $'FLEET\tstatus.rejected\t1' "$0" census --root "$fleet_root"
  checkline "FLEET-status-invalid" $'FLEET\tstatus.invalid\t1' "$0" census --root "$fleet_root"
  checkline "FLEET-missing" $'FLEET\tmissing\t1' "$0" census --root "$fleet_root"

  base_census_out="$test_root/child-only-census.out"
  if "$0" census --root "$fleet_root" > "$base_census_out" 2>&1; then
    base_census_rc=0
  else
    base_census_rc=$?
  fi
  base_validate_out="$test_root/child-only-validate.out"
  if "$0" validate --root "$fleet_root" > "$base_validate_out" 2>&1; then
    base_validate_rc=0
  else
    base_validate_rc=$?
  fi
  conf_canary="$test_root/conf-was-sourced"
  cat > "$fleet_root/shokunin.conf" <<EOF
LANES="
protocol|.|main repo protocol lane
aggregator|.|main repo aggregator lane
known|known-shokunin|known fixture
missing|missing-shokunin|missing fixture
"
touch "$conf_canary"
EOF
  dot_census_out="$test_root/root-dot-census.out"
  if "$0" census --root "$fleet_root" > "$dot_census_out" 2>&1; then
    dot_census_rc=0
  else
    dot_census_rc=$?
  fi
  base_census_fleet=$(grep '^FLEET[[:space:]]' "$base_census_out")
  dot_census_fleet=$(grep '^FLEET[[:space:]]' "$dot_census_out")
  if [ "$base_census_rc" = "$dot_census_rc" ] &&
     [ "$base_census_fleet" = "$dot_census_fleet" ] &&
     ! grep -qE '^(protocol|aggregator)[[:space:]]' "$dot_census_out"; then
    printf 'killed\troot-dot-default-census-keeps-child-totals\n'
  else
    printf 'SURVIVED\troot-dot-default-census-keeps-child-totals\n'; fail=1
  fi
  dot_validate_out="$test_root/root-dot-validate.out"
  if "$0" validate --root "$fleet_root" > "$dot_validate_out" 2>&1; then
    dot_validate_rc=0
  else
    dot_validate_rc=$?
  fi
  if [ "$base_validate_rc" = "$dot_validate_rc" ] &&
     cmp -s "$base_validate_out" "$dot_validate_out" &&
     ! grep -qE '^(protocol|aggregator)[[:space:]]' "$dot_validate_out" &&
     [ ! -e "$conf_canary" ]; then
    printf 'killed\troot-dot-default-validate-and-text-conf-parsing\n'
  else
    printf 'SURVIVED\troot-dot-default-validate-and-text-conf-parsing\n'; fail=1
  fi

  root_only="$test_root/root-only-fleet"
  mkdir -p "$root_only" || exit 3
  cat > "$root_only/shokunin.conf" <<'EOF'
LANES="
protocol|.|main repo protocol lane
aggregator|.|main repo aggregator lane
:"
EOF
  if "$0" census --root "$root_only" > "$test_root/root-only-census.out" 2>&1; then
    root_only_rc=0
  else
    root_only_rc=$?
  fi
  if [ "$root_only_rc" = 2 ] &&
     grep -qF "no lanes parsed from $root_only/shokunin.conf" "$test_root/root-only-census.out"; then
    printf 'killed\troot-only-default-fails-closed\n'
  else
    printf 'SURVIVED\troot-only-default-fails-closed\n'; fail=1
  fi
  outside_dir="$test_root/outside-shokunin"
  mkdir -p "$outside_dir/corpus" || exit 3
  cat > "$outside_dir/corpus/SOURCES.md" <<'EOF'
# Outside registry fixture

## Registry
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
## Paths
| S900 | Outside source | docs | B | outside | p1 | outside row | queued | 2026-10-01 | 90d | — |
EOF
  checkline "E12-outside-registry-mutant" \
    $'outside-shokunin\tE12\tS900 row outside Registry section' \
    "$0" validate --today 2026-10-19 "$outside_dir"
  checkx "E12-row-outside-registry-exit-1" 1 \
    "$0" validate --today 2026-10-19 "$outside_dir"
  # Exercise the shared row parser at every supported indentation width.
  for indent_width in 0 1 2 3; do
    indent=$(printf '%*s' "$indent_width" '')
    valid_dir="$test_root/indent-valid-$indent_width-shokunin"
    invalid_dir="$test_root/indent-invalid-$indent_width-shokunin"
    outside_indent_dir="$test_root/indent-outside-$indent_width-shokunin"
    mkdir -p "$valid_dir/corpus" "$invalid_dir/corpus" "$outside_indent_dir/corpus" || exit 3
    valid_id="S92$indent_width"
    invalid_id="S93$indent_width"
    usedby_id="S95$indent_width"
    outside_id="S94$indent_width"

    printf '%s\n' \
      "${indent}## Registry" \
      '' \
      '    ## Paths' \
      '    | S999 | Code example — https://code.example/example | docs | Z | code | §1 | ignored code row | watch | 2026-10-01 | 90d | — |' \
      '' \
      "${indent}| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |" \
      "${indent}|---|---|---|---|---|---|---|---|---|---|---|" \
      "${indent}| $valid_id | Indented source — https://indent.example/shared | docs | B | width-$indent_width | §1 | valid indented row | queued | 2026-01-01 | 30d | — |" \
      > "$valid_dir/corpus/SOURCES.md"
    checkline "indented-valid-$indent_width-counted" \
      "$(printf '%s\trows\t1' "indent-valid-$indent_width-shokunin")" \
      "$0" census --root "$test_root" "$valid_dir"
    checkx "indented-valid-$indent_width-clean" 0 \
      "$0" validate --today 2026-10-19 "$valid_dir"
    check "indented-overdue-$indent_width-row" "$valid_id" \
      "$0" overdue --today 2026-10-19 "$valid_dir"
    checkx "indented-overdue-$indent_width-exit-1" 1 \
      "$0" overdue --today 2026-10-19 "$valid_dir"

    printf '%s\n' \
      "${indent}## Registry" \
      "${indent}| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |" \
      "${indent}|---|---|---|---|---|---|---|---|---|---|---|" \
      "${indent}| $invalid_id | Invalid tier — https://invalid-$indent_width.example/source | docs | Z | invalid-$indent_width | §1 | invalid indented row | queued | 2026-10-01 | 90d | — |" \
      "${indent}| $usedby_id | Missing used-by — https://usedby-$indent_width.example/source | docs | B | usedby-$indent_width | §1 | indented used-by row | mined | 2026-10-01 | 90d | corpus/knowledge/missing-$indent_width.md |" \
      > "$invalid_dir/corpus/SOURCES.md"
    checkline "indented-invalid-$indent_width-E06" \
      "$(printf '%s\tE06\t%s tier=Z' "indent-invalid-$indent_width-shokunin" "$invalid_id")" \
      "$0" validate --today 2026-10-19 "$invalid_dir"
    checkline "indented-invalid-$indent_width-E11" \
      "$(printf '%s\tE11\t%s missing used-by corpus/knowledge/missing-%s.md' "indent-invalid-$indent_width-shokunin" "$usedby_id" "$indent_width")" \
      "$0" validate --today 2026-10-19 "$invalid_dir"
    checkx "indented-invalid-$indent_width-exit-1" 1 \
      "$0" validate --today 2026-10-19 "$invalid_dir"

    printf '%s\n' \
      "${indent}## Registry" \
      "${indent}| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |" \
      "${indent}|---|---|---|---|---|---|---|---|---|---|---|" \
      "${indent}## Paths" \
      "${indent}| $outside_id | Outside source — https://outside-$indent_width.example/source | docs | B | outside-$indent_width | §1 | outside Registry | queued | 2026-10-01 | 90d | — |" \
      > "$outside_indent_dir/corpus/SOURCES.md"
    checkline "indented-outside-$indent_width-E12" \
      "$(printf '%s\tE12\t%s row outside Registry section' "indent-outside-$indent_width-shokunin" "$outside_id")" \
      "$0" validate --today 2026-10-19 "$outside_indent_dir"
    checkx "indented-outside-$indent_width-exit-1" 1 \
      "$0" validate --today 2026-10-19 "$outside_indent_dir"
  done
  checkline "indented-shared-across-lanes" \
    $'indent.example/shared\tshared\tindent-valid-0-shokunin,indent-valid-1-shokunin' \
    "$0" shared "$test_root/indent-valid-0-shokunin" "$test_root/indent-valid-1-shokunin"
  scope_dir="$test_root/scope-shokunin"
  mkdir -p "$scope_dir/corpus" || exit 3
  cat > "$scope_dir/corpus/SOURCES.md" <<'EOF'
# Scope-sensitive duplicate fixture

## Registry
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S901 | Scope one — https://DUP.example/source | docs | B | taxonomy | §1 | taxonomy evidence | queued | 2026-10-01 | 90d | — |
| S902 | Scope two — https://dup.example/source/ | docs | B | checker | §2 | checker evidence | queued | 2026-10-01 | 90d | — |
EOF
  checkline "W04-scope-sensitive-mutant" \
    $'scope-shokunin\tW04\tS902 duplicate url dup.example/source across scopes' \
    "$0" validate --today 2026-10-19 "$scope_dir"
  checkx "W04-does-not-fail-validation" 0 \
    "$0" validate --today 2026-10-19 "$scope_dir"
  rejected_dir="$test_root/rejected-duplicate-shokunin"
  mkdir -p "$rejected_dir/corpus" || exit 3
  cat > "$rejected_dir/corpus/SOURCES.md" <<'EOF'
# Rejected duplicate fixture

## Registry
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S017 | Initial finding — https://keep.example/evidence | docs | B | shared scope | §1 | initial evidence | queued | 2026-10-01 | 90d | — |
| S030 | Rejected duplicate — https://keep.example/evidence/ | docs | B | shared scope | §2 | retained rejection reason | rejected | 2026-10-01 | 90d | — |
| S031 | Rejected first — https://prior.example/evidence | docs | B | shared scope | §3 | retained prior rejection | rejected | 2026-10-01 | 90d | — |
| S032 | Later finding — https://prior.example/evidence/ | docs | B | shared scope | §4 | later evidence | queued | 2026-10-01 | 90d | — |
EOF
  check "E04-rejected-pair-exemption-mutant" "ok" \
    "$0" validate --today 2026-10-19 "$rejected_dir"
  checkx "E04-rejected-pair-exemption-exit-0" 0 \
    "$0" validate --today 2026-10-19 "$rejected_dir"
  printf 'preserve\n' > "$test_root/out-guard"
  if "$0" validate --root "$froot" --out "$test_root/out-guard" missing-lane > /dev/null 2>&1; then
    out_guard_rc=0
  else
    out_guard_rc=$?
  fi
  if [ "$out_guard_rc" = 2 ] && grep -Fqx "preserve" "$test_root/out-guard"; then
    printf 'killed\tout-not-truncated-before-target-resolution\n'
  else
    printf 'SURVIVED\tout-not-truncated-before-target-resolution\n'; fail=1
  fi
  canary="$test_root/CANARY"
  mkdir -p "$test_root/injection-shokunin/corpus" || exit 3
  sed "s|CANARY|$canary|g" "$FIX/injection-shokunin/corpus/SOURCES.md" \
    > "$test_root/injection-shokunin/corpus/SOURCES.md" || exit 3
  if "$0" validate "$test_root/injection-shokunin" > "$test_root/validate.out" 2>&1; then
    validate_rc=0
  else
    validate_rc=$?
  fi
  validate_safe=0
  [ ! -e "$canary" ] && validate_safe=1
  rm -f "$canary"
  if "$0" overdue "$test_root/injection-shokunin" --today 2026-10-19 > "$test_root/overdue.out" 2>&1; then
    overdue_rc=0
  else
    overdue_rc=$?
  fi
  overdue_safe=0
  [ ! -e "$canary" ] && overdue_safe=1
  rm -f "$canary"
  if "$0" shared "$test_root/injection-shokunin" > "$test_root/shared.out" 2>&1; then
    shared_rc=0
  else
    shared_rc=$?
  fi
  shared_safe=0
  [ ! -e "$canary" ] && shared_safe=1
  if [ "$validate_rc" = 1 ] &&
     grep -qF "E08" "$test_root/validate.out" &&
     grep -qF "E11" "$test_root/validate.out" &&
     [ "$validate_safe" = 1 ] &&
     [ "$overdue_rc" = 0 ] &&
     grep -qF "cadence" "$test_root/overdue.out" &&
     [ "$overdue_safe" = 1 ] &&
     [ "$shared_rc" = 0 ] &&
     [ "$shared_safe" = 1 ]; then
    printf 'killed\tH1-no-table-cell-execution\n'
  else
    printf 'SURVIVED\tH1-no-table-cell-execution\n'; fail=1
  fi
  if SOURCES_CENSUS_SELFTEST_BAD_GAWK=1 "$0" validate --root "$froot" c \
     > "$test_root/bad-awk.out" 2>&1; then
    bad_awk_rc=0
  else
    bad_awk_rc=$?
  fi
  if [ "$bad_awk_rc" = 2 ] &&
     grep -qF "ERROR: gawk failed" "$test_root/bad-awk.out" &&
     ! grep -q $'\tok\t' "$test_root/bad-awk.out"; then
    printf 'killed\tgawk-failure-is-error-not-ok\n'
  else
    printf 'SURVIVED\tgawk-failure-is-error-not-ok\n'; fail=1
  fi
  if [ "$fail" = 0 ]; then echo "selftest ok"; exit 0; else echo "selftest FAILED" >&2; exit 3; fi
fi

# ------------------------------------------------------- lane roster build ---
# Output: lines "lane<TAB>sources-file<TAB>lane-dir<TAB>unlisted-flag" on stdout.
build_roster() {
  local conf=$ROOT/shokunin.conf
  [ -f "$conf" ] || die "config not found: $conf"
  [ -r "$conf" ] || die "config not readable: $conf"
  local lane repo d rel flag listed
  local -a order=() conf_repos=()
  declare -A files=() dirs=() unlisted=()
  while IFS=$'\t' read -r lane repo; do
    [ -n "$lane" ] || continue
    while [[ "$repo" == *[[:space:]] ]]; do repo=${repo%?}; done
    if [ "$repo" = . ]; then
      # Main-repo lanes have no corpus; defaults enumerate child repositories only.
      continue
    fi
    [ -n "${files[$lane]+x}" ] || order+=("$lane")
    files[$lane]="$ROOT/${repo:+$repo/}corpus/SOURCES.md"
    dirs[$lane]="$ROOT${repo:+/$repo}"
    conf_repos+=("$repo")
  done < <(sed -n 's/^[[:space:]]*\([a-z0-9][a-z0-9-]*\)[[:space:]]*|[[:space:]]*\([^|[:space:]][^|]*\)|.*/\1\t\2/p' "$conf")

  for d in "$ROOT"/*-shokunin; do
    [ -d "$d" ] || continue
    rel=${d#"$ROOT"/}
    listed=0
    for repo in "${conf_repos[@]}"; do
      if [ "$repo" = "$rel" ]; then listed=1; break; fi
    done
    [ "$listed" = 1 ] && continue
    lane=${rel%-shokunin}
    [ -n "$lane" ] || continue
    [ -n "${files[$lane]+x}" ] || order+=("$lane")
    files[$lane]="$d/corpus/SOURCES.md"
    unlisted[$lane]=1
    dirs[$lane]="$d"
  done

  for lane in "${order[@]}"; do
    flag=""
    [ -n "${unlisted[$lane]+x}" ] && flag=unlisted
    printf '%s\t%s\t%s\t%s\n' "$lane" "${files[$lane]}" "${dirs[$lane]}" "$flag"
  done
}

resolve_targets() { # fills TSV: lane<TAB>file<TAB>dir<TAB>unlisted-flag
  TSV=""
  if [ -n "$FILE" ]; then
    [ -f "$FILE" ] || die "--file not found: $FILE"
    local file_abs dir_abs
    file_abs=$(realpath -- "$FILE")
    dir_abs=$(realpath -- "$(dirname -- "$file_abs")/..")
    TSV="file	$file_abs	$dir_abs	"
    return
  fi
  if [ ${#LANES_WANT[@]} -eq 0 ]; then
    TSV=$(build_roster)
    [ -n "$TSV" ] || die "no lanes parsed from $ROOT/shokunin.conf"
    return
  fi
  local roster="" roster_done=0 arg row d
  for arg in "${LANES_WANT[@]}"; do
    if { [[ "$arg" == */* ]] || { [ "$ROOT_SET" = 0 ] && [ -d "$arg" ]; }; } && [ -d "$arg" ]; then
      d=$(realpath -- "$arg")
      TSV=${TSV:+$TSV$'\n'}$(printf '%s\t%s\t%s\t' "${d##*/}" "$d/corpus/SOURCES.md" "$d")
      continue
    fi
    if [ "$roster_done" = 0 ]; then roster=$(build_roster); roster_done=1; fi
    row=$(printf '%s\n' "$roster" | awk -F'\t' -v l="$arg" '$1==l')
    if [ -n "$row" ]; then
      TSV=${TSV:+$TSV$'\n'}$row
    elif [ -d "$arg" ]; then
      d=$(realpath -- "$arg")
      TSV=${TSV:+$TSV$'\n'}$(printf '%s\t%s\t%s\t' "${d##*/}" "$d/corpus/SOURCES.md" "$d")
    else
      die "unknown lane (not a dir, not in conf or root): $arg"
    fi
  done
  [ -n "$TSV" ] || die "no lanes selected"
}

trim_cell() {
  local value=$1
  while [[ "$value" == [[:space:]]* ]]; do value=${value#?}; done
  while [[ "$value" == *[[:space:]] ]]; do value=${value%?}; done
  printf '%s' "$value"
}

usedby_findings() {
  local f=$1 dir=$2 lane=$3 line id status usedby path section in_registry=0
  local heading_re='^ {0,3}##[[:space:]]' top_heading_re='^ {0,3}#[[:space:]]'
  local table_re='^ {0,3}\|'
  local -a cells=() paths=()
  while IFS= read -r line; do
    if [[ "$line" =~ $heading_re ]]; then
      line="${line#"${line%%[! ]*}"}"
      section=$(trim_cell "${line:2}")
      [ "$section" = Registry ] && in_registry=1 || in_registry=0
      continue
    fi
    if [[ "$line" =~ $top_heading_re ]]; then in_registry=0; continue; fi
    [ "$in_registry" = 1 ] || continue
    [[ "$line" =~ $table_re ]] || continue
    line="${line#"${line%%[! ]*}"}"
    cells=()
    IFS='|' read -r -a cells <<< "$line"
    [ "${#cells[@]}" -ge 12 ] || continue
    id=$(trim_cell "${cells[1]}")
    status=$(trim_cell "${cells[8]}")
    [ "$status" = mined ] || continue
    usedby=$(trim_cell "${cells[11]}")
    paths=()
    IFS=',' read -r -a paths <<< "$usedby"
    for path in "${paths[@]}"; do
      path=$(trim_cell "$path")
      [ -n "$path" ] && [ "$path" != "—" ] || continue
      if [ ! -e "$dir/$path" ]; then
        printf '%s\tE11\t%s missing used-by %s\n' "$lane" "$id" "$path"
      fi
    done
  done < "$f"
}

# Runs one gawk program over Markdown table rows with 0-3 leading ASCII spaces.
row_pass() {
  local f=$1 lane=$3
  if [ "${SOURCES_CENSUS_SELFTEST_BAD_GAWK:-0}" = 1 ]; then
    gawk 'function !' >/dev/null 2>&1
    return $?
  fi
  gawk -F'|' -v lane="$lane" -v mode="$MODE" -v today_s="$TODAY_S" '
    function trim(s) { gsub(/^[ \t]+|[ \t]+$/,"",s); return s }
    function symbolic(s) { return s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/ }
    function epoch(s,   a,y,m,d,t) {
      if (s !~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/) return INVALID_EPOCH
      split(s,a,"-"); y=a[1]+0; m=a[2]+0; d=a[3]+0
      if (y==0) return INVALID_EPOCH
      t=mktime(sprintf("%04d %02d %02d 00 00 00",y,m,d),1)
      if (strftime("%Y-%m-%d",t,1)!=s) return INVALID_EPOCH
      return t
    }
    function separator_row(   i,c) {
      if (trim($2)=="id") return 1
      if (NF<3) return 0
      for (i=2;i<NF;i++) {
        c=trim($i)
        if (c !~ /^:?-+:?$/) return 0
      }
      return 1
    }
    function url_of(s,   u,n) {
      if (match(s,/https?:\/\/[^[:space:]|]+/)) { u=substr(s,RSTART,RLENGTH)
        sub(/#[^ ]*$/,"",u); sub(/\/$/,"",u); sub(/^[A-Za-z]+:\/\//,"",u)
        n=index(u,"/"); if(n) u=tolower(substr(u,1,n-1)) substr(u,n); else u=tolower(u)
        return u }
      return "" }
    BEGIN { INVALID_EPOCH=-1e15 }
    {
      line=$0
      if (line ~ /^ {0,3}##[ \t]/) {
        sub(/^ {0,3}/,"",line)
        in_registry=(trim(substr(line,3))=="Registry")
        next
      }
      if (line ~ /^ {0,3}#[ \t]/) { in_registry=0; next }
      if (line !~ /^ {0,3}\|/) next
      sub(/^ {0,3}/,"",line)
      $0=line
      if (!in_registry) {
        if (mode=="validate" && $0 ~ /^\|[ \t]*S[0-9]{3,}[ \t]*\|/) {
          id=trim($2)
          printf "%s\tE12\t%s row outside Registry section\n",lane,id
        }
        next
      }
      if (separator_row()) next
      id=trim($2); source=trim($3); kind=trim($4); tier=trim($5); scope=trim($6)
      anchor=trim($7); teaches=trim($8); status=trim($9); opened=trim($10)
      recheck=trim($11); usedby=trim($12)
      u=url_of(source)
      rows++
      tier_key=tier; if (tier !~ /^[ABC]$/) tier_key="invalid"
      status_key=status; if (status !~ /^(queued|mined|rejected)$/) status_key="invalid"
      tier_h[tier_key]++; status_h[status_key]++
      if (mode=="validate") {
        if (NF!=13) {
          printf "%s\tE01\t%s fields=%d\n",lane,id,NF-2
          if (id !~ /^S[0-9]{3,}$/) printf "%s\tE02\t%s\n",lane,id
          next
        }
        if (id !~ /^S[0-9]{3,}$/) printf "%s\tE02\t%s\n",lane,id
        else if (id in seen) printf "%s\tE03\t%s duplicate id\n",lane,id
        seen[id]=1
        scope_key=u SUBSEP scope
        if (u!="" && (u in url_seen) && !(scope_key in url_scopes))
          printf "%s\tW04\t%s duplicate url %s across scopes\n",lane,id,u
        if (u!="" && (scope_key in url_scopes) && status!="rejected" &&
            url_scope_nonrejected[scope_key] &&
            teaches !~ /supersedes S[0-9]{3}/)
          printf "%s\tE04\t%s duplicate url %s within scope %s\n",lane,id,u,scope
        if (u!="") {
          url_seen[u]=1
          url_scopes[scope_key]=1
          if (status!="rejected") url_scope_nonrejected[scope_key]=1
        }
        if (kind !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/)
          printf "%s\tE05\t%s kind=%s\n",lane,id,kind
        if (tier !~ /^[ABC]$/) printf "%s\tE06\t%s tier=%s\n",lane,id,tier
        if (status !~ /^(queued|mined|rejected)$/)
          printf "%s\tE07\t%s status=%s\n",lane,id,status
        opened_epoch=epoch(opened)
        if (opened_epoch==INVALID_EPOCH || opened_epoch>today_s)
          printf "%s\tE08\t%s opened=%s\n",lane,id,opened
        if (recheck ~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/) {
          if (epoch(recheck)==INVALID_EPOCH) printf "%s\tE09\t%s recheck=%s\n",lane,id,recheck
        } else if (recheck !~ /^[0-9]+d$/ && !symbolic(recheck)) {
          printf "%s\tE09\t%s recheck=%s\n",lane,id,recheck
        }
        if (tier=="A" && kind=="community") printf "%s\tE10\t%s community-at-A\n",lane,id
        if (tier=="C" && status=="mined" && usedby!="—")
          printf "%s\tW01\t%s tierC mined used-by=%s\n",lane,id,usedby
        if (status=="rejected" && length(teaches)<8)
          printf "%s\tW02\t%s thin reject reason\n",lane,id
        if (status=="mined" && usedby=="—")
          printf "%s\tW03\t%s mined but unused\n",lane,id
      } else if (mode=="overdue") {
        if (recheck ~ /^[0-9]+d$/ || symbolic(recheck))
          printf "%s\tcadence\t%s recheck=%s opened=%s\n",lane,id,recheck,opened
        if (recheck ~ /^[0-9]+d$/) {
          opened_epoch=epoch(opened)
          if (opened_epoch==INVALID_EPOCH) due=INVALID_EPOCH
          else due=opened_epoch+(substr(recheck,1,length(recheck)-1)+0)*86400
        } else if (symbolic(recheck)) due=INVALID_EPOCH
        else due=epoch(recheck)
        if (due!=INVALID_EPOCH && due<=today_s)
          printf "%s\toverdue\t%s %dd recheck=%s opened=%s\n",lane,id,int((today_s-due)/86400),recheck,opened
      } else if (mode=="shared") {
        if (u!="") printf "%s\turl\t%s\n",lane,u
      }
    }
    END { if (mode=="census") {
        printf "%s\trows\t%d\n",lane,rows+0
        for (t in tier_h)   printf "%s\ttier.%s\t%d\n",lane,t,tier_h[t]
        for (s in status_h) printf "%s\tstatus.%s\t%d\n",lane,s,status_h[s]
      } }' "$f"
}

# -------------------------------------------------------------------- main ---
resolve_targets
[ -n "$OUT" ] && : > "$OUT"
findings=0
missing=0
missing_error=0
declare -a OVERDUE_LINES=()
SHARED_ROWS=""
FLEET_ROWS=0; FLEET_MISSING=0
declare -A FTIER=() FSTATUS=()

while IFS=$'\t' read -r lane f dir roster_flag; do
  [ "$roster_flag" = unlisted ] && emit "$lane	unlisted	$dir"
  if [ ! -f "$f" ]; then
    emit "$lane	missing	$f"
    missing=$((missing+1)); FLEET_MISSING=$((FLEET_MISSING+1))
    [ "$MODE" = census ] || missing_error=1
    [ "$VERBOSE" = 1 ] && echo "census: $lane has no corpus/SOURCES.md" >&2
    continue
  fi
  if ! out=$(row_pass "$f" "$dir" "$lane"); then
    die "gawk failed while processing $f"
  fi
  if [ "$MODE" = validate ]; then
    usedby_out=$(usedby_findings "$f" "$dir" "$lane")
    [ -n "$usedby_out" ] && out=${out:+$out$'\n'}$usedby_out
  fi
  case "$MODE" in
    census)
      [ -n "$out" ] && printf '%s\n' "$out" | out_sink
      while IFS=$'\t' read -r _ m v; do
        case "$m" in
          rows) FLEET_ROWS=$((FLEET_ROWS+v)) ;;
          tier.*) k=${m#tier.}; [ -n "$k" ] && FTIER[$k]=$(( ${FTIER[$k]:-0}+v )) ;;
          status.*) k=${m#status.}; [ -n "$k" ] && FSTATUS[$k]=$(( ${FSTATUS[$k]:-0}+v )) ;;
        esac
      done <<EOFACC
$out
EOFACC
      ;;
    validate)
      lane_errors=0
      if printf '%s\n' "$out" | grep -qE '	E[0-9]+	'; then
        findings=1; lane_errors=1
      fi
      if printf '%s\n' "$out" | grep -qE '	[EW][0-9]+	'; then
        printf '%s\n' "$out" | grep -E '	[EW][0-9]+	' | out_sink
      fi
      [ "$lane_errors" = 1 ] || emit "$lane	ok	$f"
      ;;
    overdue)
      while IFS= read -r line; do
        [ -n "$line" ] || continue
        case "$line" in
          *$'\toverdue\t'*) OVERDUE_LINES+=("$line") ;;
          *) emit "$line" ;;
        esac
      done <<EOFOD
$out
EOFOD
      ;;
    shared)
      [ -n "$out" ] && SHARED_ROWS=${SHARED_ROWS:+$SHARED_ROWS$'\n'}$out
      ;;
  esac
done <<EOFTSV
$TSV
EOFTSV

case "$MODE" in
  census)
    emit "FLEET	rows	$FLEET_ROWS"
    for k in A B C invalid; do emit "FLEET	tier.$k	${FTIER[$k]:-0}"; done
    for k in queued mined rejected invalid; do emit "FLEET	status.$k	${FSTATUS[$k]:-0}"; done
    emit "FLEET	missing	$FLEET_MISSING"
    ;;
  overdue)
    if [ ${#OVERDUE_LINES[@]} -gt 0 ]; then
      findings=1
      printf '%s\n' "${OVERDUE_LINES[@]}" | sort -t' ' -k2 -rn | out_sink
    fi
    ;;
  shared)
    if ! shared_out=$(gawk -F'\t' '
      $2=="url" {
        url=$3; lane=$1
        if (!(url in url_seen)) { url_seen[url]=1; order[++n]=url }
        key=url SUBSEP lane
        if (!(key in seen)) {
          seen[key]=1
          lanes[url]=lanes[url] (lanes[url]=="" ? "" : ",") lane
          count[url]++
        }
      }
      END {
        for (i=1;i<=n;i++) {
          url=order[i]
          if (count[url]>=2) printf "%s\tshared\t%s\n",url,lanes[url]
        }
      }' <<< "$SHARED_ROWS"); then
      die "gawk failed while aggregating shared sources"
    fi
    [ -n "$shared_out" ] && printf '%s\n' "$shared_out" | out_sink
    ;;
esac

if [ "$MODE" = census ] && [ "$missing" -gt 0 ]; then exit 1; fi
[ "$missing_error" = 1 ] && exit 2
[ "$findings" = 1 ] && exit 1
exit 0
