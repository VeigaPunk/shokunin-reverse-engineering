#!/usr/bin/env bash
# CR-2 scratch-verify pipeline — wave arc3-loop1-round4, chain c2, seat CR-2.
#
# Applies ONE patch text (unified diff or prose .patch.md) to a fresh scratch
# clone, then runs the full gate set the claim must satisfy:
#   1. overreach-check.py  (class 1/2/3 + pinned invariants)
#   2. census v10          (PASS, 0 new gated locus via census-diff)
#   3. citation-drift probe at the candidate commit (findings=0)
#   4. PROVINCE line count / sha256 before->after
# Scratch only: the real repo is read, never written.  Git commits happen ONLY
# inside the scratch clone (r3 VZ-2 precedent; the probe reads via `git show`).
#
# Usage: scratch-verify.sh <PATCH-FILE> <LABEL> [STRIP]
# Exit: 0 all gates green; 1 any gate red; 2 usage.
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
WORK=/var/tmp/cr2
PATCH=${1:-}; LABEL=${2:-}; STRIP=${3:-0}
[ -n "$PATCH" ] && [ -n "$LABEL" ] || { echo "usage: scratch-verify.sh <PATCH> <LABEL> [STRIP]" >&2; exit 2; }

DIR=$WORK/verify-$LABEL
LOG=$DIR/run.log
rm -rf "$DIR"; mkdir -p "$DIR"
say() { printf '%s\n' "$*" | tee -a "$LOG"; }

say "== CR-2 scratch-verify =="
say "patch : $PATCH"
say "label : $LABEL"
say "date  : $(date -Iseconds)"

# --- fresh scratch clone (shared object store; cheap) ------------------------
git clone -q --shared "$REPO" "$DIR/tree" 2>>"$LOG" || { say "clone failed"; exit 1; }
cd "$DIR/tree" || exit 1
say "clone HEAD: $(git rev-parse HEAD)"

# --- baseline census JSON (from the REAL tree, read-only) --------------------
python3 "$REPO/.ufo/gates/c1-census-v10.py" --root "$REPO" --json > "$DIR/census-base.json" 2>&1
say "baseline census exit=$? -> $DIR/census-base.json"

# --- apply ------------------------------------------------------------------
say ""
say "== apply =="
APPLIED=0
case "$PATCH" in
  *.diff|*.patch)
    if patch -p"$STRIP" --no-backup-if-mismatch < "$PATCH" >>"$LOG" 2>&1; then APPLIED=1; say "unified diff applied (-p$STRIP)"; fi ;;
  *)
    if python3 "$REPO/.ufo/waves/arc3-loop1-round4/claims/c2/RV-4/prose-apply.py" "$PATCH" "$DIR/tree" >>"$LOG" 2>&1; then APPLIED=1; say "prose patch applied"; fi ;;
esac
if [ "$APPLIED" -ne 1 ]; then
  say "RESULT: UNAPPLIED — no verdict."
  exit 1
fi

# --- identities + line counts -----------------------------------------------
say ""
say "== PROVINCE identities =="
say "baseline : $(sha256sum "$REPO/PROVINCE.md" | cut -d' ' -f1) $(wc -l < "$REPO/PROVINCE.md") lines"
say "candidate: $(sha256sum PROVINCE.md | cut -d' ' -f1) $(wc -l < PROVINCE.md) lines"

# --- gate 1: overreach ------------------------------------------------------
say ""
say "== gate 1: overreach-check =="
python3 "$WORK/overreach-check.py" "$REPO/PROVINCE.md" PROVINCE.md > "$DIR/overreach.out" 2>&1
ORC=$?
tee -a "$LOG" < "$DIR/overreach.out" | tail -20
say "overreach exit=$ORC"

# --- gate 2: census on the patched tree -------------------------------------
say ""
say "== gate 2: census =="
python3 .ufo/gates/c1-census-v10.py --root . --json > "$DIR/census-after.json" 2>&1
CRC=$?
python3 .ufo/gates/c1-census-v10.py --root . --quiet > "$DIR/census-after.txt" 2>&1
tail -4 "$DIR/census-after.txt" | tee -a "$LOG"
say "census exit=$CRC"
python3 "$REPO/.ufo/waves/arc3-loop1-round4/claims/c2/RV-4/census-diff.py" \
  "$DIR/census-base.json" "$DIR/census-after.json" > "$DIR/census-diff.out" 2>&1
DRC=$?
tail -6 "$DIR/census-diff.out" | tee -a "$LOG"
say "census-diff exit=$DRC"

# --- gate 3: citation-drift probe at a scratch commit -----------------------
say ""
say "== gate 3: citation-drift probe (scratch commit) =="
git -c user.email=cr2@scratch -c user.name=cr2 add PROVINCE.md SKILL.md SCORECARD.md SHONEN.md 2>>"$LOG"
git -c user.email=cr2@scratch -c user.name=cr2 commit -q -m "CR-2 scratch candidate: $LABEL" >>"$LOG" 2>&1
say "scratch candidate commit: $(git rev-parse HEAD)"
timeout 300 python3 .ufo/gates/citation-drift/citation-drift-probe.py --root "$DIR/tree" --rev HEAD \
  > "$DIR/probe.out" 2>&1
PRC=$?
grep -E "CITATION_DRIFT_VERDICT|findings=|citation_" "$DIR/probe.out" | head -20 | tee -a "$LOG"
say "probe exit=$PRC"

# --- verdict -----------------------------------------------------------------
say ""
GATES=0
[ "$ORC" -eq 0 ] && [ "$CRC" -eq 0 ] && [ "$DRC" -eq 0 ] && [ "$PRC" -eq 0 ] && GATES=1
if [ "$GATES" -eq 1 ]; then
  say "RESULT: ALL GATES GREEN (overreach=0 census=0 diff=0 probe=0)"
  exit 0
fi
say "RESULT: GATE RED — overreach=$ORC census=$CRC diff=$DRC probe=$PRC"
exit 1
