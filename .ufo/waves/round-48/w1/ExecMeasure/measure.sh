#!/usr/bin/env bash
# Round-48 measurement harness — ExecMeasure seat (kaidoku lane).
#
# Usage:
#   ./measure.sh [REV [FREEZE]]
#     REV     revision to grade; default = the declared freeze (tip, ac02a79f...)
#             which is the correct "after" until a landing commit exists.
#     FREEZE  declared freeze commit; default = ac02a79f... (the commit the
#             claims file itself declares after amendment A2).
#
# After the L1 lands:  ./measure.sh <landing_rev>
#
# Emits, per invocation, into $OUT/receipts/:
#   <name>.counter.json  — the counter's own receipt (--json-out), verbatim
#   <name>.stdout        — the counter's stdout stream, verbatim
#   <name>.json          — wrapped receipt: command, exit code, utc,
#                          stdout_sha256, plus the graded fields
#                          (met_target, failing, meaning_rows_failed, floor,
#                          quotes_bad, battery, freeze/frozen_* keys)
# Plus manifest.json summarising every invocation.
#
# Read-only on the lane tree: counters grade committed bytes via `git show`;
# PYTHONDONTWRITEBYTECODE keeps __pycache__ out of the worktree.
set -u

LANE="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
OUT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRATCH="${HYAKU_SCRATCH:-/fast/scratch/hyaku/kaidoku-r48/ExecMeasure}"

BASE="61b87d742032e65fca9c38267d7d6ed7e555edad"
FREEZE_A1="dc73587a8b9c1a23ba5a91dc7707ac7381a8b873"   # stale prompt freeze (A1)
FREEZE_A2="ac02a79ff84133220d01ce3b59a4789b7004dbc5"   # A2 (superseded)
FREEZE_DECL="0f06251bf6a3a6964c715f67243d4df12e854258" # declared freeze per claims file (A4)
FREEZE="${2:-$FREEZE_DECL}"
REV="${1:-$FREEZE_DECL}"
REV8="${REV:0:8}"

export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$SCRATCH" HYAKU_SCRATCH="$SCRATCH"
mkdir -p "$OUT/receipts/raw" "$SCRATCH"
cd "$LANE"

run() {
  # run <name> <counter> [extra args...]
  local name="$1" counter="$2"; shift 2
  local raw="$OUT/receipts/raw/$name.counter.json"
  local stdout="$OUT/receipts/raw/$name.stdout"
  local utc rc sha
  utc="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  python3 "tools/round-48/$counter" --root "$LANE" "$@" --json-out "$raw" >"$stdout" 2>&1
  rc=$?
  sha="$(sha256sum "$stdout" | cut -d' ' -f1)"
  python3 "$OUT/wrap.py" "$name" "$counter" "$rc" "$utc" "$sha" \
      "$raw" "$stdout" "$OUT/receipts/$name.json" -- "tools/round-48/$counter" --root "$LANE" "$@"
}

# ---- C1: meanings.py --------------------------------------------------------
run "c1-before-base"            meanings.py --freeze "$FREEZE"     --rev "$BASE"        --profile v3
run "c1-before-base-freezebase" meanings.py --freeze "$BASE"       --rev "$BASE"        --profile v3
run "c1-after-${REV8}"          meanings.py --freeze "$FREEZE"     --rev "$REV"         --profile v3
run "c1-after-${REV8}-v2"       meanings.py --freeze "$FREEZE"     --rev "$REV"         --profile v2
run "c1-stalefreeze-tip"        meanings.py --freeze "$FREEZE_A1"  --rev "$FREEZE_DECL" --profile v3
run "c1-stalefreeze-a2"         meanings.py --freeze "$FREEZE_A2"  --rev "$FREEZE_DECL" --profile v3
run "c1-control-a1-self"        meanings.py --freeze "$FREEZE_A1"  --rev "$FREEZE_A1"   --profile v3
run "c1-selftest"               meanings.py --selftest --freeze "$FREEZE" --rev "$REV"

# ---- C2: record2.py ---------------------------------------------------------
run "c2-before-base"            record2.py --freeze "$FREEZE"      --rev "$BASE"        --profile v3
run "c2-before-base-freezebase" record2.py --freeze "$BASE"        --rev "$BASE"        --profile v3
run "c2-after-${REV8}"          record2.py --freeze "$FREEZE"      --rev "$REV"         --profile v3
run "c2-after-${REV8}-v2"       record2.py --freeze "$FREEZE"      --rev "$REV"         --profile v2
run "c2-stalefreeze-tip"        record2.py --freeze "$FREEZE_A1"   --rev "$FREEZE_DECL" --profile v3
run "c2-stalefreeze-a2"         record2.py --freeze "$FREEZE_A2"   --rev "$FREEZE_DECL" --profile v3
run "c2-control-a1-self"        record2.py --freeze "$FREEZE_A1"   --rev "$FREEZE_A1"   --profile v3
run "c2-selftest"               record2.py --selftest --freeze "$FREEZE" --rev "$REV"

python3 "$OUT/manifest.py" "$OUT" "$REV" "$FREEZE" "$BASE" "$FREEZE_A1" "$FREEZE_DECL"
