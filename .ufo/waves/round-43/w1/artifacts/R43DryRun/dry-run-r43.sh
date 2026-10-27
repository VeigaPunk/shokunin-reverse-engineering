#!/usr/bin/env bash
# dry-run-r43.sh -- QUALITY 84 pre-freeze dry run for kaidoku round 43 (claim R43-C1).
#
# WHAT THIS IS
#   The gate the L1 runs AFTER installing the seat-drafted round-43 tools into the
#   lane (tools/round-43/heldout-gen-v4r43.py, tools/round-43/c1-counter.py) and
#   BEFORE the round-43 freeze commit.  It proves, on the pre-freeze tree, that the
#   frozen generator and the frozen counter work end to end on data the frozen
#   generator produced in a dev arm, that every counter binding was evaluated (and
#   printed), and that the round's new refusal guard really fires (exit 3) on a
#   manifest whose declared tuple the run did not observe.
#
# USAGE
#   dry-run-r43.sh LANE_ROOT WORK_DIR
#
#     LANE_ROOT  the lane checkout (read only: this script never writes it)
#     WORK_DIR   a scratch directory (created if absent).  All writes -- the clone,
#                the generator scratch, the receipts, the fixtures -- land here.
#                TMPDIR is set to $WORK_DIR/tmp and HYAKU_SCRATCH to $WORK_DIR so no
#                tool can fall back to /tmp.
#
#   Optional environment (defaults in brackets):
#     DRY_GEN=tools/round-43/heldout-gen-v4r43.py     generator, lane-relative
#     DRY_COUNTER=tools/round-43/c1-counter.py        counter, lane-relative
#     DRY_CLASSES=<six named classes>                 dev-arm named classes
#     DRY_COMBOS=4                                    combos, only if the generator
#                                                     advertises a combo-count knob
#     DRY_SEED=<40 hex>                               force the generator seed, replaying one
#                                                     specific combo draw (the receipt records
#                                                     generator_seed_forced; seed_matches_freeze
#                                                     then evaluates false, which is reported)
#     DRY_SWEEP=N                                     after the gates, run the generator (combo
#                                                     family only, --run) at N synthetic seeds and
#                                                     report which draws the tuple guard refuses.
#                                                     Reported (G8), never part of the exit code:
#                                                     the freeze seed is unknown until the freeze.
#     DRY_TIMEOUT=3600                                per generator / counter run (s)
#     DRY_KEEP_CLONE=1                                keep the scratch clone on success
#
# GATES (each is scored; the receipt lists every one with its observed value)
#   G1  clone of the lane at the pre-freeze tree + freeze-like commit F
#   G2  GREEN  the frozen generator writes a dev-arm manifest (exit 0)
#   G3  contract on that manifest: single-key declared tuple (R41-CL1) and the
#       generator's own generator.tuple_check block, every carrier equal:true
#   G4  region hash: the SKILL.md v4 table region at F equals the region at
#       d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b (the round-42 freeze)
#   G5  the frozen counter runs against the dev arm end to end and its receipt
#       carries EVERY declared binding with a boolean value; all values printed
#   G6  RED/GREEN of the refusal: a fixture manifest whose declared tuple the run
#       did not observe makes the generator exit 3 and write no manifest; the
#       untampered manifest does not refuse
#   G7  counter-level red: the same wrong declared tuple makes the frozen counter
#       report observed-vs-declared as false (the round-42 M42-2 defect is caught)
#
# EXIT
#   0 all gates pass   2 usage   10 preflight   11 clone/freeze   12 generator
#   13 manifest contract   14 region hash   15 counter coverage   16 refusal red
#   17 counter-level red
#
# DEV-ARM SUBSET (and why each new clause is covered)
#   named (6, the RECIPES prefix so dev-arm carrier ids line up with the full-set
#   regeneration the counter performs at the freeze):
#     clean-be ............... v4 BE handler, no gap, published>0   (baseline)
#     clean-le ............... v4 LE handler                        (endianness)
#     body-extractor-failure . gap extractor-failure, P=0, BE=yes   (rule-5 branch)
#     partial-body-failure ... gap extractor-failure, P>0           (rule-4 precedence)
#     depth-limited-mixed .... depth-limited + unpublished-entry + SR (precedence trap)
#     legacy-body-failure .... v1-v3 handler family, pinned fixture (legacy branch)
#   plus the generator's combo family (DRY_COMBOS when the generator exposes a
#   knob, else the family size of the port, 24).  Clause coverage:
#     region hash   -- lane-level: SKILL.md v4 region equals d1681696's (G4), and
#                      the counter binds it at the freeze-like commit (G5).
#     tuple_check   -- the generator's finalize step writes generator.tuple_check
#                      for these carriers (G3) and refuses a wrong declared tuple
#                      (G6); the counter binds the recorded check and the observed
#                      tuple (G5, G7).
#     single-key    -- every named and combo carrier carries the tuple under exactly
#                      one key, declared_features (G3); the counter reads only that
#                      key (R41-CL1).
#     lookup-combo  -- the combo family carries the exotic factor shapes (damage,
#                      dependency, depth ceiling, container wrap, residue, legacy
#                      base), so the frozen lookup control and combo_unseen_majority
#                      are scored on real combo envelopes (G5).
#
# This script reads git objects only (clone/show/ls-tree/rev-parse/merge-base) and
# never runs git add/commit in LANE_ROOT; the only commits are inside the scratch
# clone, with the fixture identity -c user.name=fx -c user.email=fx@fx.

set -uo pipefail
umask 022

PROG=$(basename "$0")
usage() { sed -n '2,80p' "$0" | sed 's/^# \{0,1\}//' >&2; exit 2; }

LANE=${1:-}
WORK=${2:-}
[[ -n $LANE && -n $WORK ]] || usage

GEN_REL=${DRY_GEN:-tools/round-43/heldout-gen-v4r43.py}
COUNTER_REL=${DRY_COUNTER:-tools/round-43/c1-counter.py}
# RECIPES-order prefix + the combo family: a prefix keeps the dev-arm carrier ids
# and bytes identical to the corresponding carriers of the full-set regeneration the
# counter performs at the freeze, so carriers_regenerated is a real green.
DEV_CLASSES=${DRY_CLASSES:-clean-be,clean-le,clean-empty,escaping-symlink-removed,in-tree-symlink-metadata,mixed-symlinks,combo}
WANT_COMBOS=${DRY_COMBOS:-4}
# Optional: force the generator seed.  The seed is normally the freeze-like commit
# hash; forcing it replays a specific combo draw (e.g. one a report cites).  The
# counter's seed_matches_freeze then evaluates false, which the receipt records.
FORCED_SEED=${DRY_SEED:-}
# DRY_SWEEP=N: after the gates, run the frozen generator (combo family only, --run)
# at N synthetic seeds and report which draws the tuple guard refuses.  Reported,
# never part of the exit code: it measures how often the predictor over/under-
# predicts, which one seed cannot tell you.
SWEEP=${DRY_SWEEP:-0}
RUN_TIMEOUT=${DRY_TIMEOUT:-3600}
KEEP_CLONE=${DRY_KEEP_CLONE:-0}

say()  { printf '%s: %s\n' "$PROG" "$*"; }
step() { printf '\n== %s\n' "$*"; }
ok()   { printf '  [ok]   %s\n' "$*"; }
bad()  { printf '  [FAIL] %s\n' "$*"; }
skip() { printf '  [skip] %s\n' "$*"; }

die() { local rc=$1; shift; bad "$*"; finish "$rc"; }

# ------------------------------------------------------------------- receipt
finish() {
  local rc=${1:-0}
  local verdict=FAIL
  [[ $rc -eq 0 ]] && verdict=PASS
  jq -n \
    --arg verdict "$verdict" --argjson rc "$rc" \
    --arg lane "$LANE" --arg lane_head "$LANE_HEAD" --arg work "$WORK" \
    --arg gen "$GEN_REL" --arg counter "$COUNTER_REL" --arg ev "$EV" \
    --arg classes "$DEV_CLASSES" --argjson combos "$WANT_COMBOS" \
    --argjson combos_flag "$([[ $COMBOS_FLAG == true ]] && echo true || echo false)" \
    --arg seed "${GEN_SEED:-}" --argjson seed_forced "$([[ -n $FORCED_SEED ]] && echo true || echo false)" \
    --arg F "$F" --arg R "$R" \
    --argjson gen_rc "$GEN_RC" --argjson manifest_written "$GEN_MANIFEST_WRITTEN" \
    --argjson n_carriers "$N_CARRIERS" \
    --argjson purged "$PURGED" \
    --argjson region_ok "$([[ $REGION_OK == true ]] && echo true || echo false)" \
    --slurpfile region "$WORK/receipts/region.json" \
    --argjson contract_ok "$([[ $MCHECK_OK == true ]] && echo true || echo false)" \
    --slurpfile mcheck "$WORK/receipts/manifest-check.json" \
    --argjson counter_rc "$([[ $CTR_RC == null ]] && echo 999 || echo "$CTR_RC")" \
    --argjson coverage_ok "$COVERAGE_OK" \
    --slurpfile coverage "$WORK/receipts/counter-coverage.json" \
    --argjson refusal_red "$REFUSAL_RED" --argjson refusal_green "$REFUSAL_GREEN" \
    --arg refusal_how "$REFUSAL_HOW" --rawfile ftries "$WORK/receipts/refusal-tries.txt" \
    --slurpfile rfix "$WORK/receipts/refusal-fixture.json" \
    --argjson counter_red "$COUNTER_RED" \
    --argjson sweep "${SWEEP_JSON:-null}" \
    '{
      schema: "kaidoku-r43-dry-run-v1", verdict: $verdict, exit_code: $rc,
      lane: $lane, lane_head: $lane_head, work_dir: $work,
      generator: $gen, counter: $counter, evidence_root: $ev,
      dev_arm: {named_classes: ($classes|split(",")|map(select(. != "combo"))),
                  requests_combo_family: ($classes|split(",")|index("combo") != null),
                  requested_combos: $combos, combos_flag_supported: $combos_flag,
                  carriers: $n_carriers},
      freeze_like: $F, rev: $R, evidence_root_purged_from_freeze_tree: $purged,
      generator_seed: $seed, generator_seed_forced: $seed_forced,
      gates: {
        G1_clone: ($F != ""),
        G2_generator_green: ($gen_rc == 0 and $manifest_written),
        G3_manifest_contract: $contract_ok,
        G4_region_hash: $region_ok,
        G5_counter_coverage: $coverage_ok,
        G6_refusal_red: ($refusal_red and $refusal_green),
        G7_counter_level_red: $counter_red
      },
      generator_exit: $gen_rc, manifest_written: $manifest_written,
      region: $region[0], manifest_contract: $mcheck[0],
      counter_exit: (if $counter_rc == 999 then null else $counter_rc end),
      counter_coverage: $coverage[0],
      refusal: {red: $refusal_red, green: $refusal_green, how: $refusal_how,
                tries: ($ftries|split("\n")|map(select(length>0))), fixture: $rfix[0]},
      counter_level_red: $counter_red,
      sweep: $sweep
    }' > "$WORK/receipts/dry-run-receipt.json" || \
    printf '{"schema":"kaidoku-r43-dry-run-v1","verdict":"%s","exit_code":%s,"note":"receipt serialisation failed; see logs"}\n' \
      "$verdict" "$rc" > "$WORK/receipts/dry-run-receipt.json"
  cp -f "$WORK/receipts/dry-run-receipt.json" "$WORK/dry-run-receipt.json"

  step "SUMMARY"
  jq -r '"  verdict=\(.verdict)  exit=\(.exit_code)", "  gates:", (.gates|to_entries[]|"    \(.key) = \(.value)")' \
    "$WORK/dry-run-receipt.json"
  say "receipt: $WORK/dry-run-receipt.json"
  say "logs:    $WORK/logs/"
  if [[ $KEEP_CLONE != 1 && $rc -eq 0 ]]; then rm -rf "$CLONE"; fi
  exit "$rc"
}

# state read by finish(); initialised before any die() can fire
F=""; R=""; GEN_RC=-1; CTR_RC=null; N_CARRIERS=0
GEN_MANIFEST_WRITTEN=false; PURGED=false
REGION_OK=null; MCHECK_OK=false; COVERAGE_OK=false
REFUSAL_RED=false; REFUSAL_GREEN=false; REFUSAL_HOW=""; REFUSAL_FLAG=""; REFUSAL_FORM=""; COUNTER_RED=false
COMBOS_FLAG=false
mkdir -p "$WORK/receipts" "$WORK/logs"
for f in region.json manifest-check.json counter-coverage.json refusal-fixture.json; do
  [[ -s $WORK/receipts/$f ]] || printf 'null\n' > "$WORK/receipts/$f"
done
: > "$WORK/receipts/refusal-tries.txt"

# ----------------------------------------------------------------- preflight
step "G0 preflight"
command -v git     >/dev/null || { bad "git not on PATH"; exit 10; }
command -v python3 >/dev/null || { bad "python3 not on PATH"; exit 10; }
command -v jq      >/dev/null || { bad "jq not on PATH"; exit 10; }
command -v npx     >/dev/null || { bad "npx not on PATH (the generator runs REA)"; exit 10; }
[[ -d $LANE ]] || { bad "lane root is not a directory: $LANE"; exit 10; }
git -C "$LANE" rev-parse --git-dir >/dev/null 2>&1 || { bad "not a git checkout: $LANE"; exit 10; }
LANE=$(cd "$LANE" && pwd -P)

mkdir -p "$WORK" || { bad "cannot create work dir: $WORK"; exit 10; }
WORK=$(cd "$WORK" && pwd -P)
export TMPDIR="$WORK/tmp"
export HYAKU_SCRATCH="$WORK/hyaku"
mkdir -p "$TMPDIR" "$HYAKU_SCRATCH" "$WORK/bin" "$WORK/logs" "$WORK/receipts"

# a tool may be given as an absolute path (e.g. a seat-authored artifact the L1 has
# not installed yet); it is copied into the scratch clone at tools/round-43/
GEN_IN=$LANE/$GEN_REL
COUNTER_IN=$LANE/$COUNTER_REL
[[ $GEN_REL == /* ]] && GEN_IN=$GEN_REL
[[ $COUNTER_REL == /* ]] && COUNTER_IN=$COUNTER_REL
[[ -f $GEN_IN ]] || { bad "round-43 generator not installed: $GEN_REL (the L1 integrates the seat-drafted tools first)"; exit 10; }
[[ -f $COUNTER_IN ]] || { bad "round-43 counter not installed: $COUNTER_REL"; exit 10; }
ok "lane $LANE"
ok "generator $GEN_REL $(sha256sum "$GEN_IN" | cut -d' ' -f1)"
ok "counter   $COUNTER_REL $(sha256sum "$COUNTER_IN" | cut -d' ' -f1)"

LANE_HEAD=$(git -C "$LANE" rev-parse HEAD)
ok "lane HEAD $LANE_HEAD"

# --- helper: module constants of a tool (literal assignments only)
cat > "$WORK/bin/consts.py" <<'PY'
import ast, json, sys
path = sys.argv[1]
out = {}
try:
    tree = ast.parse(open(path, encoding='utf-8').read())
except Exception as exc:
    print(json.dumps({'error': str(exc)})); raise SystemExit(0)
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        try:
            out[node.targets[0].id] = ast.literal_eval(node.value)
        except Exception:
            pass
    elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
        try:
            out[node.target.id] = ast.literal_eval(node.value)
        except Exception:
            pass
def safe(v):
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    if isinstance(v, (list, tuple)):
        return [safe(x) for x in v]
    if isinstance(v, dict):
        return {str(k): safe(x) for k, x in v.items()}
    return repr(v)
print(json.dumps({k: safe(v) for k, v in out.items()}))
PY

CONSTS_OUT=$WORK/receipts/tool-consts.json
python3 -I -B "$WORK/bin/consts.py" "$COUNTER_IN" > "$WORK/receipts/counter-consts.json"
python3 -I -B "$WORK/bin/consts.py" "$GEN_IN"     > "$WORK/receipts/generator-consts.json"
cp "$WORK/receipts/counter-consts.json" "$CONSTS_OUT"

EV=$(python3 - "$WORK/receipts/counter-consts.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
m = d.get('MANIFEST')
print(m if isinstance(m, str) else '')
PY
)
if [[ -z $EV ]]; then
  EV=corpus/evidence/round-43/c1/heldout/manifest.json
  say "counter source does not expose MANIFEST; assuming the plan's evidence root $EV"
fi
EV_DIR=${EV%/*}
ok "counter evidence root (probed from the counter source): $EV_DIR"
COUNTER_GEN=$(python3 - "$WORK/receipts/counter-consts.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
g = d.get('GEN')
print(g if isinstance(g, str) else '')
PY
)
[[ -n $COUNTER_GEN ]] && ok "counter regenerates with GEN=$COUNTER_GEN"
if [[ -n $COUNTER_GEN && ! -f $LANE/$COUNTER_GEN ]]; then
  say "WARN the counter's GEN path is absent from the lane: $COUNTER_GEN"
fi

# generator CLI surface (probe, never assume)
python3 -I -B "$GEN_IN" --help > "$WORK/logs/gen-help.txt" 2>&1
GEN_HELP_RC=$?
if [[ $GEN_HELP_RC -ne 0 ]]; then bad "generator --help failed (rc=$GEN_HELP_RC)"; cat "$WORK/logs/gen-help.txt" >&2; exit 10; fi
has_flag() { grep -q -- "$1" "$WORK/logs/gen-help.txt"; }
GEN_FLAGS=$(grep -oE -- '--[a-z0-9][a-z0-9-]*' "$WORK/logs/gen-help.txt" | sort -u | tr '\n' ' ')
ok "generator flags: $GEN_FLAGS"

# ------------------------------------------------------------------ G1 clone
step "G1 scratch clone + freeze-like commit"
CLONE=$WORK/clone
rm -rf "$CLONE"
git clone -q --shared "$LANE" "$CLONE" || die 11 "git clone failed"
TOP=$(git -C "$CLONE" rev-parse --show-toplevel)
[[ $TOP == "$CLONE" ]] || die 11 "clone toplevel is $TOP, expected $CLONE"
ok "clone $CLONE (toplevel verified)"

# materialise the pre-freeze tree: the lane working tree's version of every path
# that carries the round-43 freeze material.  Untracked lane files are copied too,
# because the L1 installs the seat-drafted tools before committing them.
copy_path() {
  local p=$1
  [[ -e $LANE/$p ]] || return 0
  mkdir -p "$CLONE/$(dirname "$p")"
  rm -rf "${CLONE:?}/$p"
  cp -a "$LANE/$p" "$CLONE/$p"
}
for p in SKILL.md plans/round-43-claims.md tools/round-43 corpus/evidence/round-43 .ufo/waves/round-43/controls; do
  copy_path "$p"
done
# The held-out set is produced AFTER the freeze; a stray copy would turn the
# dev-arm commit into a MODIFICATION of a frozen path.  Purge it from the
# freeze-like tree so F has exactly the shape the frozen tree will have.
PURGED=false
if [[ -e $CLONE/$EV_DIR ]]; then
  rm -rf "${CLONE:?}/$EV_DIR"
  PURGED=true
fi
install_abs() {   # $1 = clone dir, $2 = absolute tool path -> tools/round-43/<basename>
  local root=$1 src=$2 rel=tools/round-43/$(basename "$2")
  mkdir -p "$root/$(dirname "$rel")"
  cp -f "$src" "$root/$rel"
  printf '%s' "$rel"
}
GEN_IN_ABS=""; COUNTER_IN_ABS=""
[[ $GEN_REL == /* ]] && GEN_IN_ABS=$GEN_REL
[[ $COUNTER_REL == /* ]] && COUNTER_IN_ABS=$COUNTER_REL
if [[ $GEN_REL == /* ]]; then
  GEN_REL=$(install_abs "$CLONE" "$GEN_IN"); ok "generator installed into the clone at $GEN_REL"
fi
if [[ $COUNTER_REL == /* ]]; then
  COUNTER_REL=$(install_abs "$CLONE" "$COUNTER_IN"); ok "counter installed into the clone at $COUNTER_REL"
fi
ok "pre-freeze material copied; evidence root purged from the freeze-like tree: $PURGED"

# fixture inputs: the committed MIT copies the plan pins (never the network)
FX_DIR=""
if [[ -d $CLONE/corpus/evidence/round-43/c1/fixtures ]]; then FX_DIR=corpus/evidence/round-43/c1/fixtures
elif [[ -d $CLONE/corpus/evidence/round-42/c2/fixtures ]]; then FX_DIR=corpus/evidence/round-42/c2/fixtures; fi
PINS=""
if [[ -f $CLONE/tools/round-43/fixtures.json ]]; then PINS=tools/round-43/fixtures.json
elif [[ -f $CLONE/tools/round-42/fixtures.json ]]; then PINS=tools/round-42/fixtures.json; fi
ok "fixture copies: ${FX_DIR:-none}   pins: ${PINS:-none}"

git -C "$CLONE" add -A || die 11 "git add failed in the clone"
FIXTURE_DATE="2026-01-01T00:00:00 +0000"
export GIT_AUTHOR_DATE="$FIXTURE_DATE" GIT_COMMITTER_DATE="$FIXTURE_DATE"
git -C "$CLONE" -c user.name=fx -c user.email=fx@fx commit -q -m "fx dry-run freeze-like tree" \
  || die 11 "freeze-like commit failed"
F=$(git -C "$CLONE" rev-parse HEAD)
ok "freeze-like commit F=$F"
# the generator records sha256(__file__); it must be the blob at F
GEN_SHA_F=$(git -C "$CLONE" show "$F:$GEN_REL" 2>/dev/null | sha256sum | cut -d' ' -f1)
ok "generator blob at F sha256=${GEN_SHA_F:-absent}"

# --------------------------------------------------------------- G4 region hash
step "G4 region hash (SKILL.md v4 table region vs d1681696)"
cat > "$WORK/bin/region.py" <<'PY'
import json, subprocess, sys, hashlib
clone, marker = sys.argv[1], '<!-- sqfs-triage-table v4 -->'
def region(text):
    lines = text.splitlines()
    mi = next((i for i, l in enumerate(lines) if marker in l), None)
    if mi is None:
        return None
    ts = next((i for i in range(mi + 1, len(lines)) if lines[i].lstrip().startswith('|')), None)
    if ts is None:
        return None
    j = ts
    while j < len(lines) and lines[j].lstrip().startswith('|'):
        j += 1
    # "from the line containing the marker through the end of the first markdown
    # table after it"
    return '\n'.join(lines[mi:j]) + '\n'
def at(rev):
    p = subprocess.run(['git', '-C', clone, 'show', '%s:SKILL.md' % rev], capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None
cur = open('%s/SKILL.md' % clone, encoding='utf-8').read()
old = at('d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b')
rc, ro = region(cur), (region(old) if old else None)
print(json.dumps({
    'marker': marker,
    'region_present_worktree': rc is not None,
    'region_present_d1681696': ro is not None,
    'region_sha256_worktree': hashlib.sha256(rc.encode()).hexdigest() if rc else None,
    'region_sha256_d1681696': hashlib.sha256(ro.encode()).hexdigest() if ro else None,
    'equal': rc is not None and rc == ro,
    'region_bytes_worktree': len(rc.encode()) if rc else 0,
}))
PY
python3 -I -B "$WORK/bin/region.py" "$CLONE" > "$WORK/receipts/region.json"
REGION_OK=$(jq -r '.equal' "$WORK/receipts/region.json")
REGION_SHA=$(jq -r '.region_sha256_worktree' "$WORK/receipts/region.json")
if [[ $REGION_OK == true ]]; then
  ok "region sha256 $REGION_SHA equals the region at d1681696"
else
  bad "the SKILL.md v4 region differs from d1681696's: $(jq -c '{worktree:.region_sha256_worktree,frozen:.region_sha256_d1681696}' "$WORK/receipts/region.json")"
fi

# --------------------------------------------------------- G2 dev arm (GREEN)
step "G2 dev-arm generation (frozen generator, --run)"
mkdir -p "$WORK/gen-run" "$WORK/gen-scratch"
OUT_ABS=$CLONE/$EV_DIR
rm -rf "$OUT_ABS"
GEN_SEED=$F
[[ -n $FORCED_SEED ]] && GEN_SEED=$FORCED_SEED
GEN_ARGS=(--seed "$GEN_SEED" --out "$OUT_ABS" --run --classes "$DEV_CLASSES")
has_flag --scratch && GEN_ARGS+=(--scratch "$WORK/gen-scratch")
COMBOS_FLAG=false
has_flag --combos && { GEN_ARGS+=(--combos "$WANT_COMBOS"); COMBOS_FLAG=true; }
has_flag --gen && GEN_ARGS+=(--gen "$CLONE/tools/round-39/gen-squashfs.py")
has_flag --fixture-pins && [[ -n $PINS ]] && GEN_ARGS+=(--fixture-pins "$CLONE/$PINS")
has_flag --fixtures-dir && [[ -n $FX_DIR ]] && GEN_ARGS+=(--fixtures-dir "$CLONE/$FX_DIR")
GEN_ARGV=$(printf '%q ' "$GEN_IN" "${GEN_ARGS[@]}")
say "argv: (cd $WORK/gen-run && python3 -I -B $GEN_ARGV)"
GEN_START=$(date -u +%FT%TZ)
( cd "$WORK/gen-run" && timeout "$RUN_TIMEOUT" python3 -I -B "$CLONE/$GEN_REL" "${GEN_ARGS[@]}" ) \
  > "$WORK/logs/gen-devarm.log" 2>&1
GEN_RC=$?
GEN_END=$(date -u +%FT%TZ)
ok "generator exit $GEN_RC (log logs/gen-devarm.log)"
if [[ $GEN_RC -eq 3 ]]; then
  say "the generator REFUSED on the dev arm (exit 3).  Per-carrier diff list:"
  tail -40 "$WORK/logs/gen-devarm.log" >&2
  say "This is a real pre-freeze finding: the dev arm contains a shape whose declared tuple"
  say "the run did not observe.  The round's whole point is that the frozen generator"
  say "refuses instead of writing an unobserved manifest; the data run would stop here too."
fi
MAN=$OUT_ABS/manifest.json
GEN_MANIFEST_WRITTEN=false
[[ -f $MAN ]] && GEN_MANIFEST_WRITTEN=true
N_CARRIERS=0
[[ $GEN_MANIFEST_WRITTEN == true ]] && N_CARRIERS=$(jq '.carriers|length' "$MAN")

# ------------------------------------------------------- G3 manifest contract
step "G3 manifest contract: single-key + generator.tuple_check"
cat > "$WORK/bin/manifest_check.py" <<'PY'
import json, sys
man_path, gen_consts, counter_consts = sys.argv[1], sys.argv[2], sys.argv[3]
man = json.load(open(man_path))
gen = json.load(open(gen_consts))
cnt = json.load(open(counter_consts))
schema = man.get('declared_schema') if isinstance(man.get('declared_schema'), dict) else {}
fields = (gen.get('DECLARED_FIELDS') or gen.get('FIELDS')
          or schema.get('fields') or cnt.get('REQUIRED_FEATURES') or [])
fields = list(fields)
key = gen.get('DECLARED_KEY') or cnt.get('DECLARED_KEY') or 'declared_features'
stray_keys = {'declared', 'features'}
carriers = [c for c in (man.get('carriers') or []) if isinstance(c, dict)]
problems = []
for c in carriers:
    cid = c.get('id')
    t = c.get(key)
    if not isinstance(t, dict):
        problems.append('%s: no %s' % (cid, key)); continue
    if set(t) != set(fields):
        problems.append('%s: %s fields %s != %s' % (cid, key, sorted(t), sorted(fields)))
    for k in stray_keys:
        if k in c:
            problems.append('%s: stray key %r' % (cid, k))
    ce = c.get('class_expected')
    if isinstance(ce, dict) and 'features' in ce:
        problems.append('%s: class_expected.features present' % cid)
for k in stray_keys:
    if k in man:
        problems.append('manifest carries top-level %r' % k)
# the generator's own tuple check (QUALITY 85): a block under the generator record
tc = None
g = man.get('generator') if isinstance(man.get('generator'), dict) else {}
for k, v in g.items():
    if 'tuple' in str(k).lower() and isinstance(v, dict):
        tc = (k, v); break
if tc is None:
    tc_ok = None
    tc_key = None
    tc_rows = 0
    tc_unequal = []
else:
    tc_key, block = tc
    rows = block.get('carriers')
    if isinstance(rows, dict):
        rows = [dict(v, id=k) for k, v in rows.items() if isinstance(v, dict)]
    elif isinstance(rows, list):
        rows = [r for r in rows if isinstance(r, dict)]
    else:
        rows = []
    tc_rows = len(rows)
    tc_unequal = [r.get('id') for r in rows if r.get('equal') is not True]
    tc_all_equal = block.get('all_equal')
    tc_ok = tc_rows > 0 and not tc_unequal and tc_all_equal is not False
print(json.dumps({
    'key': key, 'fields': fields, 'carriers': len(carriers),
    'key_matches_counter': (gen.get('DECLARED_KEY') or key) == (cnt.get('DECLARED_KEY') or key),
    'fields_match_counter': (not cnt.get('REQUIRED_FEATURES')
                             or set(fields) == set(cnt.get('REQUIRED_FEATURES') or [])),
    'single_key_ok': not problems, 'single_key_problems': problems[:25],
    'tuple_check_key': tc_key, 'tuple_check_rows': tc_rows,
    'tuple_check_unaligned': tc_unequal[:25],
    'tuple_check_all_equal_flag': locals().get('tc_all_equal'),
    'tuple_check_ok': tc_ok,
}))
PY
MCHECK_OK=true
if [[ $GEN_MANIFEST_WRITTEN == true ]]; then
  python3 -I -B "$WORK/bin/manifest_check.py" "$MAN" "$WORK/receipts/generator-consts.json" "$WORK/receipts/counter-consts.json" \
    > "$WORK/receipts/manifest-check.json"
  jq -c . "$WORK/receipts/manifest-check.json" >&2
  [[ $(jq -r '.single_key_ok' "$WORK/receipts/manifest-check.json") == true ]] && ok "single-key contract holds (one declared key, no stray spellings)" \
    || { bad "single-key contract broken: $(jq -c '.single_key_problems' "$WORK/receipts/manifest-check.json")"; MCHECK_OK=false; }
  TC=$(jq -r '.tuple_check_ok' "$WORK/receipts/manifest-check.json")
  if [[ $TC == true ]]; then ok "generator.tuple_check present: $(jq -r '.tuple_check_rows' "$WORK/receipts/manifest-check.json") carriers, all equal"
  elif [[ $TC == null ]]; then bad "manifest carries no generator tuple-check block (the QUALITY 85 record the counter binds)"; MCHECK_OK=false
  else bad "generator.tuple_check has unequal carriers: $(jq -c '.tuple_check_unaligned' "$WORK/receipts/manifest-check.json")"; MCHECK_OK=false; fi
  [[ $(jq -r '.key_matches_counter' "$WORK/receipts/manifest-check.json") == true ]] || { bad "generator and counter disagree on the declared-tuple key (R41-CL1 seam)"; MCHECK_OK=false; }
  [[ $(jq -r '.fields_match_counter' "$WORK/receipts/manifest-check.json") == true ]] || { bad "generator DECLARED_FIELDS and counter REQUIRED_FEATURES differ"; MCHECK_OK=false; }
else
  bad "no manifest was written (generator exit $GEN_RC)"
  MCHECK_OK=false
fi

# -------------------------------------------------------------- G2 commit rev
step "G2b commit the dev arm as REV"
R=""
if [[ $GEN_MANIFEST_WRITTEN == true ]]; then
  git -C "$CLONE" add -A || die 11 "git add (dev arm) failed"
  git -C "$CLONE" -c user.name=fx -c user.email=fx@fx commit -q -m "fx dry-run dev-arm data" \
    || die 11 "dev-arm commit failed"
  R=$(git -C "$CLONE" rev-parse HEAD)
  ok "REV=$R (dev arm: $N_CARRIERS carriers; seed=$F)"
else
  say "no dev-arm commit: nothing to score"
fi

# ------------------------------------------------------ G5 counter end to end
step "G5 frozen counter against the dev arm"
CTR_RC=null; CTR_JSON=$WORK/receipts/counter-devarm.json
COVERAGE_OK=false
if [[ -n $R ]]; then
  say "argv: python3 -I -B $CLONE/$COUNTER_REL --root $CLONE --rev $R --freeze $F --json-out $CTR_JSON"
  ( cd "$WORK" && timeout "$RUN_TIMEOUT" python3 -I -B "$CLONE/$COUNTER_REL" \
      --root "$CLONE" --rev "$R" --freeze "$F" --json-out "$CTR_JSON" ) \
    > "$WORK/logs/counter-devarm.log" 2>&1
  CTR_RC=$?
  ok "counter exit $CTR_RC (log logs/counter-devarm.log)"
  [[ $CTR_RC -eq 2 ]] && say "exit 2 = UNEVALUABLE: see the receipt's 'unevaluable' field and the counter log"
  if [[ -s $CTR_JSON ]]; then
    cat > "$WORK/bin/coverage.py" <<'PY'
import json, sys
path = sys.argv[1]
d = json.load(open(path))
bindings = d.get('bindings') if isinstance(d.get('bindings'), dict) else {}
declared = list(d.get('claim_bindings') or []) + list(d.get('instrument_bindings') or [])
declared = list(dict.fromkeys(declared))
missing = [n for n in declared if n not in bindings]
nonbool = [n for n in bindings if not isinstance(bindings[n], bool)]
print(json.dumps({
    'unevaluable': d.get('unevaluable'),
    'exit_code': d.get('exit_code'),
    'n': d.get('n'), 'matched': d.get('matched'), 'met_target': d.get('met_target'),
    'declared_bindings': len(declared), 'evaluated': len(bindings),
    'missing': missing, 'nonbool': nonbool,
    'bindings_undeclared': d.get('bindings_undeclared'),
    'bindings_declared_unset': d.get('bindings_declared_unset'),
    'bindings_complete': (bindings.get('bindings_complete')
                          if isinstance(bindings.get('bindings_complete'), bool)
                          else (not missing and not (d.get('bindings_declared_unset') or [])
                                and not (d.get('bindings_undeclared') or []))),
    'bindings_false': sorted(k for k, v in bindings.items() if v is not True),
    'bindings': {k: bindings[k] for k in sorted(bindings)},
    'counter_sha256': d.get('counter_sha256'),
    'counter_sha256_at_freeze': d.get('counter_sha256_at_freeze'),
}))
PY
    python3 -I -B "$WORK/bin/coverage.py" "$CTR_JSON" > "$WORK/receipts/counter-coverage.json"
    if [[ $(jq -r '.unevaluable // "null"' "$WORK/receipts/counter-coverage.json") != null ]]; then
      bad "counter is UNEVALUABLE: $(jq -r '.unevaluable' "$WORK/receipts/counter-coverage.json")"
    elif [[ $(jq -r '.missing|length' "$WORK/receipts/counter-coverage.json") -gt 0 ]]; then
      bad "bindings declared but not evaluated: $(jq -c '.missing' "$WORK/receipts/counter-coverage.json")"
    elif [[ $(jq -r '.nonbool|length' "$WORK/receipts/counter-coverage.json") -gt 0 ]]; then
      bad "bindings without a boolean value: $(jq -c '.nonbool' "$WORK/receipts/counter-coverage.json")"
    elif [[ $(jq -r '.bindings_declared_unset|length' "$WORK/receipts/counter-coverage.json") -gt 0 ]]; then
      bad "bindings declared but unset: $(jq -c '.bindings_declared_unset' "$WORK/receipts/counter-coverage.json")"
    elif [[ $(jq -r '.bindings_undeclared|length' "$WORK/receipts/counter-coverage.json") -gt 0 ]]; then
      bad "bindings set but undeclared: $(jq -c '.bindings_undeclared' "$WORK/receipts/counter-coverage.json")"
    elif [[ $(jq -r '.bindings_complete' "$WORK/receipts/counter-coverage.json") != true ]]; then
      bad "receipt does not report bindings_complete"
    else
      COVERAGE_OK=true
      ok "every declared binding is evaluated: $(jq -r '.evaluated' "$WORK/receipts/counter-coverage.json") bindings"
    fi
    echo "  --- binding table (name = value) ---"
    jq -r '.bindings | to_entries[] | "  \(.key) = \(.value)"' "$WORK/receipts/counter-coverage.json"
    if jq -e '.bindings_false | index("manifest_after_freeze")' "$WORK/receipts/counter-coverage.json" >/dev/null 2>&1; then
      say "note: manifest_after_freeze is false when the evidence path already existed in the clone's history"
      say "      (a rehearsal on the round-42 tools).  On the fresh round-43 evidence path it must be true."
    fi
    echo "  --- false bindings on this dev arm (expected for a subset arm; each is still evaluated) ---"
    jq -c '.bindings_false' "$WORK/receipts/counter-coverage.json"
    echo "  --- target ---"
    jq -c '{n:.n, matched:.matched, met_target:.met_target}' "$WORK/receipts/counter-coverage.json"
  else
    bad "counter wrote no receipt at $CTR_JSON"
  fi
else
  bad "counter step skipped: no dev arm"
fi

# ------------------------------------------------------------ G6 refusal red
step "G6 refusal red (wrong declared tuple must make the generator exit 3)"
REFUSAL_RED=false; REFUSAL_GREEN=false; REFUSAL_HOW=""
FIX=$WORK/fixture-red; GREENFIX=$WORK/fixture-green
rm -rf "$FIX" "$GREENFIX"
if [[ $GEN_MANIFEST_WRITTEN == true ]]; then
  cp -a "$OUT_ABS" "$FIX"; cp -a "$OUT_ABS" "$GREENFIX"
  cat > "$WORK/bin/tamper.py" <<'PY'
import json, sys
src, dst = sys.argv[1], sys.argv[2]
man = json.load(open(src))
touched = []
for c in man.get('carriers') or []:
    t = c.get('declared_features')
    if not isinstance(t, dict):
        continue
    gaps = list(t.get('gap_kinds') or [])
    if gaps:
        t['gap_kinds'] = gaps[:-1]          # drop a kind the run DID observe
        touched.append({'id': c.get('id'), 'declared_gap_kinds': t['gap_kinds'], 'observed_dropped': gaps[-1]})
    else:
        t['gap_kinds'] = ['synthetic-unobserved-gap']   # add a kind the run did NOT observe
        touched.append({'id': c.get('id'), 'declared_gap_kinds': t['gap_kinds'], 'observed_dropped': None})
    break
json.dump(man, open(dst, 'w'), indent=1, sort_keys=True)
open(dst, 'a').write('\n')
print(json.dumps({'tampered': touched}))
PY
  python3 -I -B "$WORK/bin/tamper.py" "$OUT_ABS/manifest.json" "$FIX/manifest.json" > "$WORK/receipts/refusal-fixture.json"
  ok "fixture manifest with a deliberately wrong declared tuple: $(jq -c '.tampered' "$WORK/receipts/refusal-fixture.json")"

  # candidate manifest-check entry points, discovered from --help (then a fixed
  # fallback list), each attempted against the wrong fixture.  A candidate wins
  # when it exits 3 AND leaves the fixture manifest byte-identical.
  DENY=" --run --fetch --gen --seed --out --actions-file --actions-set --fixture-pins --fixtures-dir --scratch --ood-op --keep-extraction --gzip --classes --combos "
  CAND=$(grep -oE -- '--[a-z0-9][a-z0-9-]*' "$WORK/logs/gen-help.txt" | sort -u \
         | grep -Ei 'manifest|check|tuple|declared|final|refuse' | grep -vE "$DENY" || true)
  for extra in --check-manifest --verify-manifest --check-tuple --tuple-check --check --manifest-check --declared-check; do
    printf '%s\n' "$CAND" | grep -qx -- "$extra" || CAND="$CAND $extra"
  done
  say "candidate manifest-check flags: $(echo $CAND)"
  SHA_BEFORE=$(sha256sum "$FIX/manifest.json" | cut -d' ' -f1)
  tries=""
  for flag in $CAND; do
    for form in "flag-manifest" "flag-dir" "out-flag-manifest"; do
      case $form in
        flag-manifest)      argv=( "$flag" "$FIX/manifest.json" ) ;;
        flag-dir)           argv=( "$flag" "$FIX" ) ;;
        out-flag-manifest)  argv=( --out "$FIX" "$flag" "$FIX/manifest.json" ) ;;
      esac
      ( cd "$WORK" && timeout 600 python3 -I -B "$CLONE/$GEN_REL" "${argv[@]}" ) \
        > "$WORK/logs/refusal-try.log" 2>&1
      rc=$?
      sha_now=$(sha256sum "$FIX/manifest.json" | cut -d' ' -f1)
      tries="$tries $(printf '%s/%s/rc=%s/sha=%s' "$flag" "$form" "$rc" "$([[ $sha_now == "$SHA_BEFORE" ]] && echo same || echo changed)")"
      if [[ $rc -eq 3 && $sha_now == "$SHA_BEFORE" ]]; then
        REFUSAL_RED=true; REFUSAL_FLAG=$flag; REFUSAL_FORM=$form
        REFUSAL_HOW="python3 -I -B $GEN_REL $flag $([[ $form == flag-dir ]] && echo "$FIX" || echo "$FIX/manifest.json")"
        break 2
      fi
    done
  done
  # --verify over a directory that already holds a tampered manifest
  if [[ $REFUSAL_RED != true ]] && has_flag --verify; then
    ( cd "$WORK" && timeout 600 python3 -I -B "$CLONE/$GEN_REL" --out "$FIX" --verify ) \
      > "$WORK/logs/refusal-verify.log" 2>&1
    rc=$?
    sha_now=$(sha256sum "$FIX/manifest.json" | cut -d' ' -f1)
    tries="$tries --verify--out/rc=$rc/sha=$([[ $sha_now == "$SHA_BEFORE" ]] && echo same || echo changed)"
    [[ $rc -eq 3 && $sha_now == "$SHA_BEFORE" ]] && { REFUSAL_RED=true; REFUSAL_FLAG=--verify; REFUSAL_FORM=verify-out; REFUSAL_HOW="--out $FIX --verify"; }
  fi
  # selftest last (it can only corroborate; it does not take our fixture)
  SELFTEST_RC=null
  if [[ $REFUSAL_RED != true ]] && has_flag --selftest; then
    ( cd "$WORK" && timeout 900 python3 -I -B "$CLONE/$GEN_REL" --selftest ) \
      > "$WORK/logs/gen-selftest.log" 2>&1
    SELFTEST_RC=$?
    tries="$tries --selftest/rc=$SELFTEST_RC"
  fi
  python3 - "$WORK/receipts/refusal-tries.txt" "$tries" <<'PY'
import sys
open(sys.argv[1], 'w').write(sys.argv[2].strip() + '\n')
PY
  if [[ $REFUSAL_RED == true ]]; then
    ok "REFUSAL RED exercised: exit 3 and the fixture manifest was not rewritten ($REFUSAL_HOW)"
  else
    bad "the frozen generator exposes no reachable manifest-check entry point; a wrong declared tuple could not make it exit 3"
    say "tried:$tries"
    say "the generator must accept a manifest (or an out dir holding one) and exit 3 on a declared/observed mismatch:"
    say "that is the seam CTL-C1-2 and this QUALITY-84 gate both need.  Add e.g. --check-manifest PATH."
  fi
  # GREEN control: the same interface on the UNtampered manifest must not refuse
  if [[ $REFUSAL_RED == true ]]; then
    case ${REFUSAL_FORM:-} in
      flag-manifest) gargv=( "$REFUSAL_FLAG" "$GREENFIX/manifest.json" ) ;;
      flag-dir)      gargv=( "$REFUSAL_FLAG" "$GREENFIX" ) ;;
      out-flag-manifest) gargv=( --out "$GREENFIX" "$REFUSAL_FLAG" "$GREENFIX/manifest.json" ) ;;
      verify-out)    gargv=( --out "$GREENFIX" --verify ) ;;
      *)             gargv=( "$REFUSAL_FLAG" "$GREENFIX/manifest.json" ) ;;
    esac
    ( cd "$WORK" && timeout 600 python3 -I -B "$CLONE/$GEN_REL" "${gargv[@]}" ) \
      > "$WORK/logs/refusal-green.log" 2>&1
    grc=$?
    if [[ $grc -eq 3 ]]; then
      bad "GREEN control failed: the untampered manifest was refused too (exit 3) -- the refusal is not discriminating"
    else
      REFUSAL_GREEN=true
      ok "GREEN control: the untampered manifest is not refused (exit $grc)"
    fi
  fi
else
  bad "refusal red skipped: no dev-arm manifest to build the fixture from"
fi

# ----------------------------------------------------- G8 opt-in seed sweep
SWEEP_JSON='null'
if [[ ${SWEEP:-0} -gt 0 ]]; then
  step "G8 seed sweep ($SWEEP draws, combo family, reported only)"
  mkdir -p "$WORK/sweep"
  refused=(); accepted=(); rows=""
  for i in $(seq 1 "$SWEEP"); do
    sseed=$(printf 'dry-run-r43-sweep:%d' "$i" | sha256sum | cut -d' ' -f1)
    sout="$WORK/sweep/$i"
    rm -rf "$sout"
    ( cd "$WORK/sweep" && timeout "$RUN_TIMEOUT" python3 -I -B "$CLONE/$GEN_REL" \
        --seed "$sseed" --out "$sout" --classes combo --run --scratch "$WORK/gen-scratch" \
        $(has_flag --fixtures-dir && [[ -n $FX_DIR ]] && printf -- '--fixtures-dir %q ' "$CLONE/$FX_DIR") \
        $(has_flag --fixture-pins && [[ -n $PINS ]] && printf -- '--fixture-pins %q ' "$CLONE/$PINS") ) \
      > "$WORK/logs/sweep-$i.log" 2>&1
    src=$?
    if [[ $src -eq 3 ]]; then
      refused+=("$sseed")
      bad "draw $i (seed $sseed): the generator REFUSED (exit 3)"
      grep -E 'declared_tuple_unobserved|^  [A-Z][0-9]+' "$WORK/logs/sweep-$i.log" | head -4 | sed 's/^/         /'
    elif [[ $src -eq 0 ]]; then
      accepted+=("$sseed")
      ok "draw $i (seed $sseed): accepted (manifest written)"
    else
      bad "draw $i (seed $sseed): generator exit $src (not a refusal; see logs/sweep-$i.log)"
    fi
  done
  SWEEP_JSON=$(jq -n --argjson n "$SWEEP" --argjson refused "$(printf '%s\n' "${refused[@]:-}" | jq -R . | jq -s -c 'map(select(length>0))')" \
    --argjson accepted "$(printf '%s\n' "${accepted[@]:-}" | jq -R . | jq -s -c 'map(select(length>0))')" \
    '{draws: $n, refused: $refused, accepted: $accepted,
      refused_count: ($refused|length), accepted_count: ($accepted|length)}')
  say "sweep: $(echo "$SWEEP_JSON" | jq -c '{refused_count, accepted_count}') (reported only; the freeze seed is drawn at the freeze, so a refusal here is a predictor defect, not a harness failure)"
fi

# ------------------------------------------------- G7 counter-level refusal red
step "G7 counter-level red (the counter must catch the wrong declared tuple)"
COUNTER_RED=false
if [[ -n $R && $GEN_MANIFEST_WRITTEN == true ]]; then
  CLONE2=$WORK/clone2
  rm -rf "$CLONE2"
  if git clone -q --shared "$LANE" "$CLONE2"; then
    for p in SKILL.md plans/round-43-claims.md tools/round-43 corpus/evidence/round-43 .ufo/waves/round-43/controls; do
      [[ -e $LANE/$p ]] || continue
      mkdir -p "$CLONE2/$(dirname "$p")"; rm -rf "${CLONE2:?}/$p"; cp -a "$LANE/$p" "$CLONE2/$p"
    done
    rm -rf "${CLONE2:?}/$EV_DIR"
    [[ -n $GEN_IN_ABS ]] && install_abs "$CLONE2" "$GEN_IN_ABS" >/dev/null
    [[ -n $COUNTER_IN_ABS ]] && install_abs "$CLONE2" "$COUNTER_IN_ABS" >/dev/null
    git -C "$CLONE2" add -A
    git -C "$CLONE2" -c user.name=fx -c user.email=fx@fx commit -q -m "fx dry-run freeze-like tree (red)"
    F2=$(git -C "$CLONE2" rev-parse HEAD)
    mkdir -p "$CLONE2/$EV_DIR"
    cp -a "$FIX/." "$CLONE2/$EV_DIR/"
    git -C "$CLONE2" add -A
    git -C "$CLONE2" -c user.name=fx -c user.email=fx@fx commit -q -m "fx dry-run tampered dev arm"
    R2=$(git -C "$CLONE2" rev-parse HEAD)
    ( cd "$WORK" && timeout "$RUN_TIMEOUT" python3 -I -B "$CLONE2/$COUNTER_REL" \
        --root "$CLONE2" --rev "$R2" --freeze "$F2" --json-out "$WORK/receipts/counter-tampered.json" ) \
      > "$WORK/logs/counter-tampered.log" 2>&1
    TRC=$?
    ok "counter on the tampered manifest: exit $TRC"
    if [[ -s $WORK/receipts/counter-tampered.json ]]; then
      jq -r '.bindings | to_entries[] | select(.key|test("observed|tuple|declared";"i")) | "  \(.key) = \(.value)"' \
        "$WORK/receipts/counter-tampered.json"
      N_FALSE=$(jq -r '[.bindings | to_entries[] | select((.key|test("observed|tuple|declared";"i")) and .value==false)] | length' "$WORK/receipts/counter-tampered.json")
      if [[ $N_FALSE -ge 1 ]]; then
        COUNTER_RED=true
        ok "counter flags the wrong declared tuple ($N_FALSE binding(s) false)"
      else
        bad "counter did not flag the deliberately wrong declared tuple (its observed-vs-declared binding stayed true)"
      fi
    else
      if [[ $TRC -eq 2 ]]; then bad "counter went UNEVALUABLE on the tampered manifest (exit 2)"; else bad "counter wrote no receipt on the tampered manifest"; fi
    fi
    rm -rf "$CLONE2"
  else
    bad "could not clone for the counter-level red"
  fi
else
  bad "counter-level red skipped: no dev arm / no counter run"
fi


# ---------------------------------------------------------------- verdict
RC=0
if [[ $GEN_MANIFEST_WRITTEN != true || $GEN_RC -ne 0 ]]; then RC=12; fi
if [[ $RC -eq 0 && $MCHECK_OK != true ]]; then RC=13; fi
if [[ $RC -eq 0 && $REGION_OK != true ]]; then RC=14; fi
if [[ $RC -eq 0 && $COVERAGE_OK != true ]]; then RC=15; fi
if [[ $RC -eq 0 && ( $REFUSAL_RED != true || $REFUSAL_GREEN != true ) ]]; then RC=16; fi
if [[ $RC -eq 0 && $COUNTER_RED != true ]]; then RC=17; fi
finish "$RC"
