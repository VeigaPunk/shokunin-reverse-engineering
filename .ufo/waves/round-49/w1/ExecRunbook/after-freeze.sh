#!/usr/bin/env bash
# after-freeze.sh - kaidoku round 49, L1 runbook for everything AFTER the single freeze commit.
# Author: seat ExecRunbook (wave 1, pre-freeze). Written against the DRAFT tools; re-verify the
# resolved argv with `--dry-run` once the freeze is committed (the argv below is the plan's
# counting command verbatim, plan R49-C1 "Counting command" / R49-C2 "Counting command").
#
# USAGE
#   FREEZE=<40-hex freeze commit> after-freeze.sh [--dry-run] [--rev REV] PHASE...
#
# PHASES, in the order the L1 runs them (each is idempotent except `data` and `land-evidence`):
#   pre            read-only gates: jj-lane state, FREEZE is an ancestor of HEAD/main, frozen blobs at
#                  FREEZE == HEAD == worktree, tool + REA prerequisites, evidence root absent, controls
#                  summary; then takes the BEFORE snapshots (census before, misroot before).
#   score-before   C1 and C2 counted at --rev FREEZE (expected exit 1: carriers_matched 0 / mismatches 9).
#   data           tools/round-49/c1-run.sh --data-run  (the ONLY step that writes the lane evidence root).
#   land-evidence  (needs --yes) jj-lane.sh commit of corpus/evidence/round-49/c1 ONLY. Docs, entry,
#                  PROVINCE, README, SOURCES rows, lessons, SCORECARD, LOG corrections are landed by the L1
#                  by hand (jj-lane.sh commit, pathspec-limited) BEFORE `post`.
#   post           landed-state gates, score-after (C1 exit 0 / C2 exit 0), census after, misroot after.
#   before-landing = pre score-before data          after-landing = post
# Individual post steps: gate-landed score-after census-after misroot-after verdict.
#
# FLAGS / ENV
#   --dry-run   prints every resolved argv; executes only read-only gates; creates/writes NOTHING
#               (c1-run.sh is invoked with its own --dry-run so its resolved plan is shown).
#   --rev REV   measured revision for `post` (default: tip of refs/heads/main; must equal HEAD).
#   --yes       allow `land-evidence` to commit.
#   LANE FLEET BASE PKG SCRATCH LANE_ID  overridable (defaults below).
#   REHEARSAL=1 LANE=<scratch clone from mkclone.sh>: evidence root, receipts and scores move into
#               SCRATCH, c1-run.sh is NOT given --data-run (it gets --evidence-root instead), and
#               land-evidence commits inside the clone. Used only to verify this script.
#
# EXIT: 0 every gate clean and every score as expected; 1 a gate or score deviated (the receipt
# says which); 2 could not evaluate (bad args, missing FREEZE). A 2 never counts toward a target.
#
# WRITE SCOPE (guard_write refuses anything else): the lane evidence root
# $LANE/corpus/evidence/round-49/c1 (data + land-evidence only), $WAVE/l1/** (receipts, scores,
# census, misroot), and $SCRATCH/** (= /fast/scratch/hyaku/kaidoku-r49/l1). Known writes the guard
# cannot see (outside those three; measured by strace in the rehearsal, see ExecRunbook.md F12):
# `npx` appends ~/.npm/_logs/*-debug-0.log and talks to registry.npmjs.org:443 on every REA call.
set -u

PROG=after-freeze.sh
LANE=${LANE:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
FLEET=${FLEET:-/home/vgpnk/Projects/shokunin}
BASE=${BASE:-e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9}
PKG=${PKG:-/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents}
SCRATCH=${SCRATCH:-/fast/scratch/hyaku/kaidoku-r49/l1}
LANE_ID=${LANE_ID:-kaidoku}
REHEARSAL=${REHEARSAL:-0}
FREEZE=${FREEZE:-}
REV=""
DRY=0
YES=0
JJLANE=$FLEET/scripts/hyaku/jj-lane.sh
CENSUS_SH=$FLEET/scripts/sources-census.sh
DISK_GUARD=$FLEET/scripts/hyaku/disk-guard.sh
FIXED_PATH="/usr/local/bin:/usr/bin:/bin:$HOME/.local/bin:$HOME/.local/share/fnm/node-versions/v24.21.0/installation/bin"
export GIT_OPTIONAL_LOCKS=0

PHASES=()
while [ $# -gt 0 ]; do
  case $1 in
    --dry-run) DRY=1 ;;
    --yes) YES=1 ;;
    --rev) REV=${2:-}; shift ;;
    --freeze) FREEZE=${2:-}; shift ;;
    -h|--help) sed -n '2,41p' "$0"; exit 0 ;;
    pre|score-before|data|land-evidence|post|gate-landed|score-after|census-after|misroot-after|verdict) PHASES+=("$1") ;;
    before-landing) PHASES+=(pre score-before data) ;;
    after-landing) PHASES+=(post) ;;
    *) echo "$PROG: unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done
[ ${#PHASES[@]} -gt 0 ] || { sed -n '2,41p' "$0"; exit 2; }
if [ -z "$FREEZE" ]; then
  [ $DRY -eq 1 ] && FREEZE='<FREEZE>' || { echo "$PROG: FREEZE (40-hex) required: FREEZE=<hash> or --freeze" >&2; exit 2; }
fi

if [ "$REHEARSAL" = 1 ]; then
  WAVE=$SCRATCH/rehearsal-wave
  EVROOT=$SCRATCH/rehearsal-evidence/c1
  MAINREF=HEAD
else
  WAVE=$LANE/.ufo/waves/round-49
  EVROOT=$LANE/corpus/evidence/round-49/c1
  MAINREF=refs/heads/main
fi
L1=$WAVE/l1
OUT=$L1/after-freeze          # per-step receipts: <step>.json/.stdout/.stderr
SCORES=$L1/scores             # --json-out of the four counting commands
CENSUS=$L1/census
MISROOT=$L1/misroot
FAILS=()
fail() { FAILS+=("$1"); echo "FAIL  $1"; }
ok() { echo "ok    $1"; }
now() { date -u +%Y-%m-%dT%H:%M:%SZ; }

# ---- write-scope guard -------------------------------------------------------------------------
ALLOWED=("$SCRATCH" "$L1" "$EVROOT")
guard_write() { # <path>... : abort (exit 2) when a write target is outside the three roots
  local p r rp okp
  for p in "$@"; do
    rp=$(realpath -m -- "$p"); okp=0
    for r in "${ALLOWED[@]}"; do
      r=$(realpath -m -- "$r")
      case $rp in "$r"|"$r"/*) okp=1 ;; esac
    done
    [ $okp -eq 1 ] || { echo "$PROG: REFUSING write outside lane evidence root / wave l1 / scratch: $rp" >&2; exit 2; }
  done
}
mk() { [ $DRY -eq 1 ] && return 0; guard_write "$@"; mkdir -p -- "$@"; }

# ---- step runner: argv + exit + stdout sha256 + UTC time -> $OUT/<name>.json ----------------------
STEP_RC=0
step() { # step NAME EXPECT_EXIT CMD...   (runs in the current directory)
  local name=$1 expect=$2; shift 2
  echo "STEP  $name (expect exit $expect): ${*@Q}"
  if [ $DRY -eq 1 ]; then STEP_RC=$expect; echo "      [dry-run] not executed"; return 0; fi
  guard_write "$OUT"; mkdir -p "$OUT"
  local t0 t1 sha
  local cwd=${STEP_CWD:-$PWD}
  t0=$(now); ( cd "$cwd" && "$@" ) >"$OUT/$name.stdout" 2>"$OUT/$name.stderr"; STEP_RC=$?; t1=$(now)
  sha=$(sha256sum <"$OUT/$name.stdout" | cut -d' ' -f1)
  python3 -I - "$OUT/$name.json" "$name" "$expect" "$STEP_RC" "$sha" "$t0" "$t1" "$cwd" "$@" <<'PY'
import json, sys
p, name, expect, rc, sha, t0, t1, cwd, *argv = sys.argv[1:]
json.dump({"step": name, "argv": argv, "cwd": cwd, "exit_code": int(rc), "expected_exit": int(expect),
           "stdout_sha256": sha, "utc_start": t0, "utc_end": t1}, open(p, "w"), indent=1, sort_keys=True)
open(p, "a").write("\n")
PY
  echo "      exit $STEP_RC stdout_sha256 $sha"
  [ "$STEP_RC" = "$expect" ] || fail "step $name exit $STEP_RC != expected $expect (see $OUT/$name.stderr)"
}
jcheck() { # jcheck LABEL FILE 'python expr over d' : the receipt content, not just the exit code
  local label=$1 file=$2 expr=$3
  if [ $DRY -eq 1 ]; then echo "CHECK $label: [dry-run] $expr"; return 0; fi
  if python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if eval(sys.argv[2]) else 1)' "$file" "$expr" 2>/dev/null
  then ok "$label"; else fail "$label ($expr on $file)"; fi
}
G() { git -C "$LANE" "$@"; }
REV_RESOLVED() { G rev-parse --verify -q "$MAINREF^{commit}"; }

# the frozen set: the plan's byte-frozen paths + the counter's own FROZEN_PATHS/FROZEN_PREFIXES
FROZEN_SPECS=(tools/round-49 plans/round-49-claims.md tools/round-42/fixtures.json tools/round-42/c1-counter.py
  tools/round-42/prior-pins.json tools/round-42/rea-pkg.json tools/round-39/gen-squashfs.py
  tools/round-27/xpin-attribute.mjs corpus/evidence/round-44/oracle)

# (a3) frozen blobs unchanged: FREEZE tree == <rev> tree == worktree, log walk empty, no stray files
frozen_gate() { # <rev>
  local r=$1
  if diff <(G ls-tree -r "$FREEZE" -- "${FROZEN_SPECS[@]}") <(G ls-tree -r "$r" -- "${FROZEN_SPECS[@]}") >/dev/null
  then ok "frozen blobs at FREEZE == ${r:0:12} ($(G ls-tree -r "$FREEZE" -- "${FROZEN_SPECS[@]}" | wc -l) entries)"; else fail "frozen blobs differ between FREEZE and $r (a later restore does not un-block: counter exit 2 frozen_path_changed)"; fi
  [ -z "$(G diff --name-only "$FREEZE" -- "${FROZEN_SPECS[@]}")" ] && ok "worktree == FREEZE for the frozen set" || fail "worktree differs from FREEZE in the frozen set"
  [ -z "$(G ls-files --others -- tools/round-49 plans)" ] && ok "no untracked file under tools/round-49 or plans/ (no __pycache__)" || fail "untracked file(s) under tools/round-49 or plans/: $(G ls-files --others -- tools/round-49 plans | tr '\n' ' ')"
  [ -z "$(G log -m --diff-merges=first-parent --name-status --pretty=format: "$FREEZE..$r" -- "${FROZEN_SPECS[@]}" | tr -d '\n')" ] \
    && ok "no commit in FREEZE..${r:0:12} touches a frozen path (merge-aware walk over the whole frozen set)" || fail "a commit in FREEZE..$r touched a frozen path"
}

ambient_env() { env | grep -E '^(REA_|npm_config_|C1_|KAIDOKU_|PYTHON|NODE_)' | grep -viE '^[^=]*(token|auth|secret|passw|_key)' | sort; }

# ================================================================================================
phase_pre() {
  echo "== pre: read-only gates =="
  [ "$FREEZE" != '<FREEZE>' ] && { [[ $FREEZE =~ ^[0-9a-f]{40}$ ]] || { echo "$PROG: FREEZE is not 40-hex" >&2; exit 2; }; }
  # (a1) lane state
  if [ "$REHEARSAL" = 1 ]; then
    [ "$(G rev-parse --show-toplevel)" = "$LANE" ] && ok "rehearsal clone toplevel == $LANE" || fail "rehearsal LANE is not a repo toplevel"
  else
    local st; st=$("$JJLANE" state "$LANE" 2>&1); local rc=$?
    echo "      jj-lane.sh state $LANE -> exit $rc: $st"
    [ $rc -eq 0 ] && ok "jj-lane state exit 0" || fail "jj-lane state exit $rc"
    case $st in *' behind=0 '*) ok "behind=0" ;; *) fail "lane is behind origin: $st" ;; esac
    case $st in *' tracked=0 '*) ok "no tracked-file change in the lane worktree" ;; *) fail "tracked changes in the lane worktree (commit or revert before the data run): $st" ;; esac
    local lh; lh=$(sed -n 's/.* local=\([0-9a-f]*\) .*/\1/p' <<<"$st")
    [ "$lh" = "$(G rev-parse HEAD)" ] && ok "main tip == HEAD ($lh)" || fail "main tip $lh != HEAD $(G rev-parse HEAD) (colocated jj head moved?)"
  fi
  [ "$FREEZE" = '<FREEZE>' ] && { echo "      [dry-run] FREEZE unset; ancestry / blob gates skipped"; snapshot_census before; snapshot_misroot before; return 0; }
  # (a2) freeze identity and ancestry
  G cat-file -e "$FREEZE^{commit}" 2>/dev/null && ok "FREEZE is a commit" || { fail "FREEZE $FREEZE is not a commit"; return; }
  G merge-base --is-ancestor "$BASE" "$FREEZE" && ok "BASE is an ancestor of FREEZE" || fail "BASE not an ancestor of FREEZE"
  [ "$FREEZE" != "$BASE" ] && ok "FREEZE != BASE" || fail "FREEZE == BASE (nothing frozen)"
  G merge-base --is-ancestor "$FREEZE" "$MAINREF" && ok "FREEZE is an ancestor of $MAINREF" || fail "FREEZE is not an ancestor of $MAINREF"
  G merge-base --is-ancestor "$FREEZE" HEAD && ok "FREEZE is an ancestor of HEAD" || fail "FREEZE is not an ancestor of HEAD"
  # what the freeze commit(s) touched: only the plan, tools/round-49, and round-49 wave evidence
  local odd; odd=$(G diff --name-only "$BASE" "$FREEZE" | grep -vE '^(tools/round-49/|plans/round-49-claims\.md$|\.ufo/waves/round-49/)' || true)
  [ -z "$odd" ] && ok "BASE..FREEZE touches only tools/round-49, the plan, .ufo/waves/round-49" || fail "BASE..FREEZE touches other paths: $(echo "$odd" | tr '\n' ' ')"
  for f in tools/round-49/c1-counter.py tools/round-49/c1-run.sh tools/round-49/c1-run.py tools/round-49/c1-controls.py \
           tools/round-49/c1-oracle.py tools/round-49/carriers.json tools/round-49/c2-mismatch.py plans/round-49-claims.md; do
    G cat-file -e "$FREEZE:$f" 2>/dev/null && ok "frozen file at FREEZE: $f" || fail "missing at FREEZE: $f"
  done
  local nfix; nfix=$(G ls-tree -r --name-only "$FREEZE" -- tools/round-49/control-fixtures | wc -l)
  [ "$nfix" -gt 0 ] && ok "control-fixtures committed in FREEZE ($nfix files)" || fail "tools/round-49/control-fixtures absent at FREEZE (plan: every control fixture exists in the freeze)"
  frozen_gate "$MAINREF"
  # (a3b) environment that would silently redirect the data run or drop the unblob log tee
  local v
  for v in C1_RUN_PY C1_REAL_UNBLOB C1_LOG_COPY KAIDOKU_C1_DATA_RUN PYTHONPATH; do
    [ -z "${!v:-}" ] && ok "env $v unset" || fail "env $v is set (${!v}): it would redirect the runner or the counters"
  done
  case ${REA_UNBLOB_COMMAND:-} in
    ''|"$HOME/.local/bin/unblob") ok "env REA_UNBLOB_COMMAND ${REA_UNBLOB_COMMAND:-unset} (runner and counter override it with the same binary)" ;;
    *) fail "env REA_UNBLOB_COMMAND=$REA_UNBLOB_COMMAND is not \$HOME/.local/bin/unblob" ;;
  esac
  [ "${C1_UNBLOB_LOG_TEE:-1}" = 1 ] && ok "env C1_UNBLOB_LOG_TEE is 1/unset (log tee on)" || fail "C1_UNBLOB_LOG_TEE=${C1_UNBLOB_LOG_TEE} drops the extract command line from extract-env.json"
  # (a4) tools and REA prerequisites on the child PATH (identical to c1-run.sh FIXED_PATH)
  local t
  for t in unblob sasquatch npx node; do
    PATH=$FIXED_PATH command -v "$t" >/dev/null && ok "child PATH resolves $t -> $(PATH=$FIXED_PATH command -v $t)" || fail "child PATH lacks $t"
  done
  local uv; uv=$(PATH=$FIXED_PATH unblob --version 2>&1 | head -1); [ "$uv" = 26.6.4 ] && ok "unblob 26.6.4" || fail "unblob version '$uv' != 26.6.4"
  local sq; sq=$(PATH=$FIXED_PATH sasquatch -version 2>&1 | head -1); case $sq in *' 4.5.1 '*) ok "sasquatch 4.5.1" ;; *) fail "sasquatch version line '$sq'" ;; esac
  grep -q '"version": "6.5.0"' "$PKG/package.json" 2>/dev/null && ok "REA package root $PKG is 6.5.0" || fail "REA package root $PKG is not 6.5.0"
  # (a5) evidence root must not exist (REA refuses an existing root; never --force), controls summary
  if [ -e "$EVROOT" ]; then fail "evidence root already exists: $EVROOT (REA refuses an existing root; a re-run needs a decision, not --force)"; else ok "evidence root absent: $EVROOT"; fi
  if [ "$REHEARSAL" != 1 ]; then
    local cs=$WAVE/controls/summary.json
    if [ -f "$cs" ]; then jcheck "controls summary kill_rule_fires false" "$cs" "d.get('kill_rule_fires') is False"; else fail "controls summary missing: $cs"; fi
  fi
  # (a6) disk
  # `disk-guard.sh status` walks every scratch tree: measured 67 s wall / 7 CPU-min (F11); use df.
  local av; av=$(df -B1G --output=avail "$(dirname "$SCRATCH")" 2>/dev/null | tail -1 | tr -d ' G')
  [ "${av:-0}" -ge 20 ] && ok "scratch filesystem has ${av} GiB free (>= 20)" || fail "scratch filesystem free space ${av:-?} GiB < 20"
  # snapshots (BEFORE): written only when not --dry-run
  snapshot_census before
  snapshot_misroot before
  # The runner and the counter both pass os.environ through to REA (they override only PATH, TMPDIR
  # and REA_UNBLOB_COMMAND), so the ambient REA_*_COMMAND / npm_config_* variables are an input of the
  # receipt and of the counter-time rerun. Record them now, compare them in `post`.
  if [ $DRY -eq 1 ]; then echo "STEP  env-pre: ambient_env (REA_*/npm_config_*/C1_*/KAIDOKU_*/PYTHON*/NODE_* minus secret-shaped names) > $L1/env-pre.txt"
  else guard_write "$L1"; mkdir -p "$L1"; ambient_env >"$L1/env-pre.txt"; echo "      ambient env recorded: $(wc -l <"$L1/env-pre.txt") vars, sha256 $(sha256sum <"$L1/env-pre.txt" | cut -c1-16)"; fi
}

# ---- (d) census: SOURCES.md registry census before / after ---------------------------------------
# before = the round-start validate capture at $L1/sources-census-start.txt (exists) + a census taken
# now, + the BASE blob's row count (deterministic; independent of when the census is taken).
snapshot_census() { # before|after
  local tag=$1 d=$CENSUS
  echo "== census $tag =="
  if [ $DRY -eq 1 ]; then
    echo "STEP  census-$tag-validate (expect exit 0): $CENSUS_SH validate --root $FLEET kaidoku"
    echo "STEP  census-$tag-counts   (expect exit 0): $CENSUS_SH census --root $FLEET kaidoku"
    echo "STEP  census-$tag-rowcount: git show $([ "$tag" = before ] && echo "$BASE" || echo "<REV>"):corpus/SOURCES.md | grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|'"
    [ "$tag" = after ] && echo "STEP  census-after-immutable (expect exit 0): bash tools/round-38/registry-immutable.sh $LANE $BASE <REV>"
    return 0
  fi
  guard_write "$d"; mkdir -p "$d"
  local save=$OUT; OUT=$d
  STEP_CWD=$FLEET step "census-$tag-validate" 0 "$CENSUS_SH" validate --root "$FLEET" kaidoku
  STEP_CWD=$FLEET step "census-$tag-counts" 0 "$CENSUS_SH" census --root "$FLEET" kaidoku
  OUT=$save
  local rev=$BASE; [ "$tag" = after ] && rev=${REV:-$(REV_RESOLVED)}
  local rc; rc=$(G show "$rev:corpus/SOURCES.md" | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|')
  echo "$rc" >"$d/census-$tag-rowcount.txt"; echo "      registry rows at $rev: $rc"
  if [ "$tag" = before ] && [ -f "$L1/sources-census-start.txt" ]; then
    # the round-start capture: validate lines + `exit=N`; the live validate must reproduce its lines
    if diff <(sed '/^exit=/d' "$L1/sources-census-start.txt") "$d/census-before-validate.stdout" >/dev/null
    then ok "live validate == round-start capture sources-census-start.txt (lines); start exit line: $(grep '^exit=' "$L1/sources-census-start.txt")"
    else echo "WARN  live validate differs from round-start capture (the registry moved since round start; diff in $d/census-before.diff)"; diff <(sed '/^exit=/d' "$L1/sources-census-start.txt") "$d/census-before-validate.stdout" >"$d/census-before.diff"; fi
  fi
  if [ "$tag" = after ]; then
    # delta: ids added BASE->REV, and the append-only registry rule (only status/recheck/used-by may change)
    comm -13 <(G show "$BASE:corpus/SOURCES.md" | grep -oE '^\|[[:space:]]*S[0-9]{3,}' | tr -d '| ' | sort) \
             <(G show "$rev:corpus/SOURCES.md"  | grep -oE '^\|[[:space:]]*S[0-9]{3,}' | tr -d '| ' | sort) >"$d/census-after-added-ids.txt"
    echo "      ids added BASE..REV: $(tr '\n' ' ' <"$d/census-after-added-ids.txt")"
    local save2=$OUT; OUT=$d
    STEP_CWD=$LANE step census-after-immutable 0 bash tools/round-38/registry-immutable.sh "$LANE" "$BASE" "$rev"
    OUT=$save2
    # the plan's A8 registry arithmetic: rows B -> A must equal the before/after counts above
    echo "      A8 arithmetic: rows $(cat "$d/census-before-rowcount.txt" 2>/dev/null || echo '?') -> $rc (compare with the search-log entry for round 49)"
    [ -f "$d/census-after-validate.stdout" ] && tail -1 "$d/census-after-validate.stdout" | sed 's/^/      validate final line: /'
  fi
}

# ---- (e) misroot sweep ------------------------------------------------------------------------------
# Seats run with cwd = the FLEET root; tools write ./unblob.log and strays relative to cwd. The sweep
# diffs the fleet and lane statuses before/after and probes the known misroot shapes (M18/M26/M34/M38/M39).
# ABSOLUTE check (a delta against `before` would baseline an already-present misroot away): the fleet
# status must not show a path naming this round or lane at all, and the fleet must hold no tools/round-49.
# Found in wave 1: the fleet root already carries 23 untracked files under tools/round-49/control-fixtures/
# (c1, c4, c5; 17:55 UTC-3), written by c1-controls.py run with cwd = fleet root (FIXTURES is relative).
misroot_absolute() { # before|after
  local tag=$1 hits
  hits=$(git -C "$FLEET" status --porcelain -uall 2>/dev/null | grep -Ei 'kaidoku|round-49|r49|tools/round-49|squashfs' || true)
  if [ -n "$hits" ]; then fail "[$tag] fleet status names this round/lane NOW ($(echo "$hits" | wc -l) path(s); first: $(echo "$hits" | head -2 | tr '\n' ';')) - judge and remove BEFORE the freeze (never in a seat)"; else ok "[$tag] no fleet status path names kaidoku/round-49/r49/tools/round-49/squashfs (absolute)"; fi
  [ -e "$FLEET/tools/round-49" ] && fail "[$tag] $FLEET/tools/round-49 exists at the fleet root ($(find "$FLEET/tools/round-49" -type f | wc -l) files)" || ok "[$tag] no $FLEET/tools/round-49"
}

snapshot_misroot() { # before|after
  local tag=$1 d=$MISROOT
  echo "== misroot $tag =="
  misroot_absolute "$tag"
  if [ $DRY -eq 1 ]; then
    echo "STEP  misroot-$tag: git -C $FLEET status --porcelain -uall > $d/fleet-$tag.txt ; git -C $LANE status --porcelain -uall -- . ':!.ufo' > $d/lane-$tag.txt"
    [ "$tag" = before ] && echo "STEP  marker: touch $SCRATCH/misroot.marker"
    return 0
  fi
  guard_write "$d" "$SCRATCH"; mkdir -p "$d" "$SCRATCH"
  [ "$tag" = before ] && touch "$SCRATCH/misroot.marker"
  git -C "$FLEET" status --porcelain -uall >"$d/fleet-$tag.txt" 2>"$d/fleet-$tag.err"; echo "      fleet status exit $? lines $(wc -l <"$d/fleet-$tag.txt") sha256 $(sha256sum <"$d/fleet-$tag.txt" | cut -c1-16)"
  G status --porcelain -uall -- . ':!.ufo' >"$d/lane-$tag.txt" 2>"$d/lane-$tag.err"; echo "      lane status (excluding .ufo) lines $(wc -l <"$d/lane-$tag.txt")"
  [ "$tag" = after ] && misroot_diff
}
misroot_diff() {
  local d=$MISROOT m=$SCRATCH/misroot.marker pat='kaidoku|round-49|r49|squashfs|unblob|R49|ExecRunbook'
  [ -f "$m" ] || { fail "misroot marker missing: run phase pre first"; return; }
  diff "$d/fleet-before.txt" "$d/fleet-after.txt" | grep '^>' >"$d/fleet-new-lines.txt"
  echo "      fleet status lines new since before: $(wc -l <"$d/fleet-new-lines.txt") (sibling lanes also write the fleet; judged by name+content below)"
  # (1) a new fleet path whose NAME is ours
  if grep -Ei "$pat" "$d/fleet-new-lines.txt" >"$d/fleet-name-hits.txt"; then fail "new fleet-root path(s) naming this round: $(tr '\n' ';' <"$d/fleet-name-hits.txt")"; else ok "no new fleet status path names kaidoku/round-49/r49/squashfs/unblob"; fi
  # (2) content naming kaidoku-r49/round-49 inside NEW untracked fleet files (<= 1 MiB, text)
  : >"$d/fleet-content-hits.txt"
  while IFS= read -r l; do
    p=${l#> ?? }
    f=$FLEET/${p# }; [ -f "$f" ] && [ "$(stat -c %s "$f")" -le 1048576 ] && grep -IlE 'kaidoku-r49|round-49|kaidoku-shokunin' "$f" >>"$d/fleet-content-hits.txt"
  done < <(grep -E '^> \?\?' "$d/fleet-new-lines.txt")
  [ -s "$d/fleet-content-hits.txt" ] && fail "new untracked fleet file(s) whose content names this lane/round: $(tr '\n' ';' <"$d/fleet-content-hits.txt")" || ok "no new untracked fleet file names kaidoku-r49/round-49/kaidoku-shokunin in its content"
  # (3) known shapes: ./unblob.log or r49 files at fleet root / lane root, wave dirs at the fleet, /tmp leaks
  find "$FLEET" -maxdepth 1 -newer "$m" \( -type f -o -type d \) \( -iname 'unblob.log' -o -iname '*r49*' -o -iname '*round-49*' -o -iname '*squashfs*' -o -iname '*.bin' \) >"$d/fleet-root-newer.txt" 2>/dev/null
  [ -s "$d/fleet-root-newer.txt" ] && fail "fleet-root entries newer than the marker: $(tr '\n' ';' <"$d/fleet-root-newer.txt")" || ok "no unblob.log / *r49* / *.bin newer than the marker at the fleet root"
  find "$LANE" -maxdepth 1 -newer "$m" ! -name . ! -name .git ! -name .jj ! -name .ufo ! -name tools ! -name plans ! -name corpus >"$d/lane-root-newer.txt" 2>/dev/null
  [ -s "$d/lane-root-newer.txt" ] && fail "lane-root entries newer than the marker outside tools/plans/corpus/.ufo: $(tr '\n' ';' <"$d/lane-root-newer.txt") (lane unblob.log and glibc-tag-object.json are TRACKED strays from earlier rounds; a change shows here)" || ok "no new lane-root stray (unblob.log, *.json, dirs) since the marker"
  G diff --quiet -- unblob.log glibc-tag-object.json && ok "tracked lane-root strays unblob.log / glibc-tag-object.json unmodified" || fail "tracked lane-root stray modified (a run wrote ./unblob.log in the lane root?)"
  find "$FLEET/.ufo/waves" -maxdepth 1 -name 'round-49*' 2>/dev/null | grep . >"$d/fleet-wave-dir.txt" && fail "fleet has .ufo/waves/round-49*: $(cat "$d/fleet-wave-dir.txt")" || ok "no .ufo/waves/round-49* at the fleet root (the lane's wave dir is $WAVE)"
  find /tmp -maxdepth 2 -newer "$m" \( -name 'rea-firmware-*' -o -name 'c1-*' -o -name '*kaidoku*' -o -name '*unblob*' -o -name 'probe-R49*' \) >"$d/tmp-leaks.txt" 2>/dev/null
  [ -s "$d/tmp-leaks.txt" ] && fail "/tmp leaks (TMPDIR not honoured): $(tr '\n' ';' <"$d/tmp-leaks.txt")" || ok "no rea-firmware-*/c1-*/unblob* under /tmp newer than the marker"
  # lane: untracked files outside the expected landing set
  local stray; stray=$(grep -vE '^.. (corpus/(evidence/round-49|knowledge|lessons)/|corpus/README\.md|corpus/SOURCES\.md|PROVINCE\.md|SCORECARD\.md|LOG\.md|SKILL\.md)' "$d/lane-after.txt" || true)
  [ -z "$stray" ] && ok "lane status (excluding .ufo) shows only landing-set paths or nothing" || fail "lane status has paths outside the landing set: $(echo "$stray" | tr '\n' ';')"
}

# ================================================================================================
phase_score_before() {
  echo "== score-before (counted at --rev FREEZE) =="
  [ $DRY -eq 0 ] && { guard_write "$SCORES"; mkdir -p "$SCORES" "$SCRATCH"; }
  STEP_CWD=$LANE
  # (c) C1 before: exits 1, carriers_matched 0, every documentation binding false
  step c1-before 1 python3 -I -B tools/round-49/c1-counter.py --root "$LANE" --rev "$FREEZE" --freeze "$FREEZE" \
       --pkg65 "$PKG" --work "$SCRATCH/counter-c1-before" --json-out "$SCORES/c1-before.json"
  jcheck "C1 before: carriers_matched 0" "$SCORES/c1-before.json" "d['carriers_matched']==0 and d['exit_code']==1"
  jcheck "C1 before: all six documentation bindings false" "$SCORES/c1-before.json" \
    "all(b in d['bindings_false'] for b in ('province_core_section','province_core_row','frontier_note','entry_present','sourced','coverage_map_row'))"
  # C2 before: mismatches 9 (no --battery, the plan's FREEZE statement)
  step c2-before 1 python3 -I -B tools/round-49/c2-mismatch.py --root "$LANE" --rev "$FREEZE" --freeze "$FREEZE" \
       --json-out "$SCORES/c2-before.json"
  jcheck "C2 before: atoms_total 9 mismatches 9" "$SCORES/c2-before.json" "d['atoms_total']==9 and d['mismatches']==9 and d['exit_code']==1"
}

phase_data() {
  echo "== data: c1-run.sh (the only writer of the lane evidence root) =="
  mk "$SCRATCH" "$SCRATCH/tmp"
  guard_write "$EVROOT"
  if [ "$REHEARSAL" = 1 ]; then
    # the guard must refuse the committed evidence root without --data-run (plan: seats never run data)
    STEP_CWD=$SCRATCH step c1-run-guard 2 "$LANE/tools/round-49/c1-run.sh" --lane-root "$LANE" --scratch "$SCRATCH" --freeze "$FREEZE"
    STEP_CWD=$SCRATCH step c1-run-data 0 env "TMPDIR=$SCRATCH/tmp" "$LANE/tools/round-49/c1-run.sh" --lane-root "$LANE" --evidence-root "$EVROOT" \
        --scratch "$SCRATCH" --freeze "$FREEZE" --timeout 900
  else
    # resolved plan first (writes nothing), then the run; cwd = scratch so a stray ./unblob.log lands there
    if [ $DRY -eq 1 ]; then
      echo "STEP  c1-run-plan (live --dry-run of the runner; writes nothing)"
      [ -x "$LANE/tools/round-49/c1-run.sh" ] && (cd "$SCRATCH" 2>/dev/null || cd /; "$LANE/tools/round-49/c1-run.sh" --dry-run --lane-root "$LANE" --scratch "$SCRATCH" --freeze "$FREEZE") || echo "      tools/round-49/c1-run.sh not present in $LANE yet (pre-freeze)"
    else
      STEP_CWD=$SCRATCH step c1-run-plan 0 "$LANE/tools/round-49/c1-run.sh" --dry-run --lane-root "$LANE" --scratch "$SCRATCH" --freeze "$FREEZE"
    fi
    if [ $DRY -eq 1 ]; then
      echo "STEP  c1-run-data (expect exit 0): cd $SCRATCH && TMPDIR=$SCRATCH/tmp $LANE/tools/round-49/c1-run.sh --lane-root $LANE --scratch $SCRATCH --freeze $FREEZE --data-run --timeout 900"
      return 0
    fi
    STEP_CWD=$SCRATCH step c1-run-data 0 env "TMPDIR=$SCRATCH/tmp" "$LANE/tools/round-49/c1-run.sh" --lane-root "$LANE" --scratch "$SCRATCH" \
        --freeze "$FREEZE" --data-run --timeout 900
  fi
  [ $DRY -eq 1 ] && return 0
  local m=$EVROOT/manifest.json
  jcheck "manifest: 4 carriers ok, none failed" "$m" "d['summary']['ok']==4 and d['summary']['failed']==[]"
  jcheck "every carrier exit 0, receipt written, output_directory in /kaidoku-r49/ scratch" "$m" \
    "all(c['exit_code']==0 and c['receipt_written'] and '/kaidoku-r49/' in c['output_directory'] and '..' not in c['output_directory'].split('/') for c in d['carriers'].values())"
  jcheck "manifest names exactly v1le v1be v2le v2be" "$m" "sorted(d['carriers'])==['v1be','v1le','v2be','v2le']"
  local id; for id in v1le v1be v2le v2be; do
    jcheck "$id provenance.json binds the scratch output_directory" "$EVROOT/$id/provenance.json" "'/kaidoku-r49/' in d['rea_output_directory'] and d['rewritten'] is False"
    [ -f "$EVROOT/$id/after.json" ] && ok "$id/after.json present" || fail "$id/after.json missing"
  done
  [ -z "$(find "$EVROOT" -type l)" ] && ok "no symlink in the evidence tree" || fail "symlink in the evidence tree: $(find "$EVROOT" -type l | head -3)"
  [ -z "$(find "$EVROOT" -type f -size +10M)" ] && ok "no evidence file > 10 MiB" || fail "evidence file > 10 MiB (jj-lane needs --allow-large)"
  [ -z "$(G status --porcelain -uall -- tools plans | head -1)" ] && ok "the data run left tools/ and plans/ untouched (no __pycache__)" || fail "the data run dirtied tools/ or plans/: $(G status --porcelain -uall -- tools plans | head -3)"
  echo "      evidence tree: $(find "$EVROOT" -type f | wc -l) files, $(du -sk "$EVROOT" | cut -f1) KiB"
}

phase_land_evidence() {
  echo "== land-evidence: commit corpus/evidence/round-49/c1 only =="
  if [ "$REHEARSAL" = 1 ]; then
    [ $DRY -eq 1 ] && { echo "STEP  land-evidence [rehearsal]: cp -a $EVROOT -> $LANE/corpus/evidence/round-49/c1 ; git -C $LANE add/commit (clone only)"; return 0; }
    [ "$(G rev-parse --show-toplevel)" = "$LANE" ] || { echo "toplevel mismatch" >&2; exit 2; }
    mkdir -p "$LANE/corpus/evidence/round-49" && cp -a "$EVROOT" "$LANE/corpus/evidence/round-49/c1"
    G add -- corpus/evidence/round-49/c1 && G -c user.name=r49-dev -c user.email=r49@dev.invalid commit -q -m "rehearsal: evidence" && ok "rehearsal evidence committed in the clone: $(G rev-parse HEAD)"
    return
  fi
  local msg='round-49: R49-C1 REA 6.5.0 extract-firmware after-receipts for the four frozen SquashFS v1/v2 carriers (runner output verbatim)'
  echo "STEP  land-evidence: $JJLANE commit $LANE --as $LANE_ID -m '...' -- corpus/evidence/round-49/c1"
  if [ $DRY -eq 1 ]; then return 0; fi
  [ $YES -eq 1 ] || { echo "$PROG: land-evidence needs --yes (it mutates the lane history)" >&2; exit 2; }
  [ -d "$EVROOT" ] || { echo "$PROG: no evidence root to commit: run phase data first" >&2; exit 2; }
  "$JJLANE" commit "$LANE" --as "$LANE_ID" -m "$msg" -- corpus/evidence/round-49/c1 | tee "$L1/land-evidence.out"; echo "      jj-lane exit ${PIPESTATUS[0]}; the citable hash is the line starting 'landed'"
  echo "      NEXT (L1, by hand, pathspec-limited jj-lane.sh commit): knowledge entry, PROVINCE.md, corpus/README.md, SOURCES rows (S138/S139 used-by, S147/S148, search log), lessons, SCORECARD, LOG. Then: after-freeze.sh post"
}

phase_gate_landed() {
  echo "== gate-landed =="
  [ -n "$REV" ] || REV=$(REV_RESOLVED)
  [[ $REV =~ ^[0-9a-f]{40}$ ]] || { echo "$PROG: REV not resolvable" >&2; exit 2; }
  echo "      REV = $REV"
  if [ $DRY -eq 0 ]; then
    ambient_env >"$L1/env-post.txt"
    if [ -f "$L1/env-pre.txt" ] && diff "$L1/env-pre.txt" "$L1/env-post.txt" >/dev/null; then ok "ambient REA_*/npm_config_* env identical to the pre snapshot (data run and counters saw the same env)"; else fail "ambient env differs between pre and post (or pre snapshot missing): diff $L1/env-pre.txt $L1/env-post.txt"; fi
  fi
  [ "$REV" = "$(G rev-parse HEAD)" ] && ok "REV == HEAD" || fail "REV $REV != HEAD $(G rev-parse HEAD): the counter would measure a commit the worktree is not at"
  G merge-base --is-ancestor "$FREEZE" "$REV" && ok "FREEZE is an ancestor of REV" || fail "FREEZE is not an ancestor of REV"
  frozen_gate "$REV"
  [ -z "$(G status --porcelain --untracked-files=no -- . ':!.ufo' | head -1)" ] && ok "no tracked change outside .ufo (REV == worktree for the counters' file reads)" || fail "tracked worktree changes outside .ufo: the counters read git objects at REV and would not see them"
  [ -z "$(G ls-files --others --exclude-standard -- corpus tools plans PROVINCE.md | head -1)" ] && ok "no uncommitted new file under corpus/tools/plans (every landing file is at REV)" || fail "uncommitted new files: $(G ls-files --others --exclude-standard -- corpus tools plans | head -5 | tr '\n' ' ')"
  local id fa
  for id in v1le v1be v2le v2be; do
    fa=$(G log --diff-filter=A --format=%H "$REV" -- "corpus/evidence/round-49/c1/$id/after.json" | tail -1)
    if [ -n "$fa" ] && [ "$fa" != "$FREEZE" ] && G merge-base --is-ancestor "$FREEZE" "$fa"; then ok "$id after.json first added in $fa (a strict descendant of FREEZE)"; else fail "$id after.json first-add '$fa' is not a strict descendant of FREEZE"; fi
  done
  for f in corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md corpus/lessons/round-49.md; do
    G cat-file -e "$REV:$f" 2>/dev/null && ok "present at REV: $f" || fail "absent at REV: $f"
  done
  G show "$REV:PROVINCE.md" | grep -q '^## Round-49 additions to Core' && ok "PROVINCE.md has '## Round-49 additions to Core'" || fail "PROVINCE.md lacks the round-49 Core heading"
  G show "$REV:SCORECARD.md" | grep -q '^## Record corrections — round 49' && ok "SCORECARD.md has '## Record corrections — round 49'" || fail "SCORECARD.md lacks '## Record corrections — round 49'"
  G show "$REV:corpus/SOURCES.md" | grep -qE '^\|[[:space:]]*S148[[:space:]]*\|' && ok "SOURCES has S148" || fail "SOURCES lacks S148"
  for f in corpus/evidence/round-49/c2/popper.html corpus/evidence/round-49/c2/sysexits.html; do
    G cat-file -e "$REV:$f" 2>/dev/null && ok "snapshot at REV: $f" || fail "snapshot absent at REV: $f"
  done
}

phase_score_after() {
  echo "== score-after (counted at --rev REV) =="
  [ -n "$REV" ] || REV=$(REV_RESOLVED)
  [ $DRY -eq 0 ] && { guard_write "$SCORES"; mkdir -p "$SCORES" "$SCRATCH"; }
  [ $DRY -eq 1 ] && [ -z "$REV" ] && REV='<REV>'
  STEP_CWD=$LANE
  step c1-after 0 python3 -I -B tools/round-49/c1-counter.py --root "$LANE" --rev "$REV" --freeze "$FREEZE" \
       --pkg65 "$PKG" --work "$SCRATCH/counter-c1-after" --json-out "$SCORES/c1-after.json"
  jcheck "C1 after: carriers_matched 4, no false binding, frozen_path_changed [], met_target" "$SCORES/c1-after.json" \
    "d['carriers_matched']==4 and d['bindings_false']==[] and d['frozen_path_changed']==[] and d['met_target'] is True and d['exit_code']==0 and d['failing']==[]"
  step c1-after-verify-receipt 0 python3 -I -B tools/round-49/c1-counter.py --verify-receipt "$SCORES/c1-after.json"
  step c2-after 0 python3 -I -B tools/round-49/c2-mismatch.py --root "$LANE" --rev "$REV" --freeze "$FREEZE" --battery \
       --json-out "$SCORES/c2-after.json"
  jcheck "C2 after: atoms_total 9, mismatches 0, battery.failing [], eleven mutations ok, do-nothing red x9" "$SCORES/c2-after.json" \
    "d['atoms_total']==9 and d['mismatches']==0 and d['battery']['failing']==[] and len(d['battery']['mutations'])==11 and all(m['ok'] for m in d['battery']['mutations']) and len(d['battery']['do_nothing_red'])==9 and d['exit_code']==0"
  step c2-after-nobattery 0 python3 -I -B tools/round-49/c2-mismatch.py --root "$LANE" --rev "$REV" --freeze "$FREEZE" \
       --json-out "$SCORES/c2-after-nobattery.json"
}

phase_verdict() {
  echo "== verdict =="
  if [ ${#FAILS[@]} -eq 0 ]; then echo "VERDICT clean: every executed gate and score matched its expectation ($(now))"; return 0; fi
  echo "VERDICT $(( ${#FAILS[@]} )) deviation(s):"; printf '  - %s\n' "${FAILS[@]}"; return 1
}

# ================================================================================================
if [ $DRY -eq 1 ]; then echo "$PROG: DRY RUN - read-only gates execute, nothing is written; FREEZE=$FREEZE LANE=$LANE SCRATCH=$SCRATCH"; fi
for ph in "${PHASES[@]}"; do
  case $ph in
    pre) phase_pre ;;
    score-before) phase_score_before ;;
    data) phase_data ;;
    land-evidence) phase_land_evidence ;;
    gate-landed) phase_gate_landed ;;
    score-after) phase_score_after ;;
    census-after) [ -n "$REV" ] || REV=$(REV_RESOLVED); snapshot_census after ;;
    misroot-after) snapshot_misroot after ;;
    verdict) phase_verdict ;;
    post) phase_gate_landed; phase_score_after; snapshot_census after; snapshot_misroot after ;;
  esac
done
phase_verdict
exit $?
