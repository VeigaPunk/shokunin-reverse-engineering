#!/usr/bin/env bash
# RV-4 apply-and-census harness — wave arc3-loop1-round4, chain c2, seat RV-4.
#
# Applies a patch (unified diff, or a .patch.md prose patch whose fenced block
# carries "-" / "+" hunk lines) to a FRESH SCRATCH COPY of the repo tree, then
# runs the census instrument against that scratch tree and diffs the result
# against a baseline census JSON.  The real tree is only ever read.
#
# Usage:
#   apply-and-census.sh <PATCH-FILE> <LABEL> [PATCH-STRIP-LEVEL]
#
# Environment:
#   REPO   repo root (default /home/vgpnk/Projects/shokunin/kaidoku-shokunin)
#   WORK   scratch root (default /var/tmp/rv4-scratch)  -- NEVER /tmp
#   BASE   baseline census JSON (default $WORK/census-base.json)
#
# Exit: 0 census PASS with no new gated locus; 1 defect / apply failure; 2 usage.
set -u

REPO=${REPO:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
WORK=${WORK:-/var/tmp/rv4-scratch}
BASE=${BASE:-$WORK/census-base.json}
DIFFER=$REPO/.ufo/waves/arc3-loop1-round4/claims/c2/RV-4/census-diff.py

PATCH=${1:-}; LABEL=${2:-}; STRIP=${3:-0}
if [ -z "$PATCH" ] || [ -z "$LABEL" ]; then
  echo "usage: apply-and-census.sh <PATCH-FILE> <LABEL> [STRIP-LEVEL]" >&2
  exit 2
fi
# resolve the patch to an absolute path before the cwd moves to the scratch tree
case "$PATCH" in
  /*) : ;;
  *)  PATCH="$(cd "$(dirname "$PATCH")" 2>/dev/null && pwd)/$(basename "$PATCH")" ;;
esac
if [ ! -f "$PATCH" ]; then
  echo "apply-and-census.sh: patch file not found: $PATCH" >&2
  exit 2
fi

DIR=$WORK/apply-$LABEL
LOG=$DIR/run.log
mkdir -p "$DIR"
: > "$LOG"

say() { printf '%s\n' "$*" | tee -a "$LOG"; }

say "== RV-4 apply-and-census =="
say "patch  : $PATCH"
say "label  : $LABEL"
say "scratch: $DIR"
say "repo   : $REPO (read-only)"
say "date   : $(date -Iseconds)"

# --- fresh scratch copy of the census-scoped surfaces + instrument + gates ----
rm -rf "$DIR/tree"
mkdir -p "$DIR/tree/.ufo/gates"
for f in PROVINCE.md SKILL.md SCORECARD.md README.md LOG.md; do
  [ -f "$REPO/$f" ] && cp "$REPO/$f" "$DIR/tree/$f"
done
cp "$REPO/.ufo/gates/c1-census-v10.py" "$DIR/tree/.ufo/gates/"
if [ -d "$REPO/.ufo/gates/custody-pair" ]; then
  mkdir -p "$DIR/tree/.ufo/gates/custody-pair"
  cp "$REPO/.ufo/gates/custody-pair/"* "$DIR/tree/.ufo/gates/custody-pair/" 2>/dev/null
fi
if [ -d "$REPO/corpus" ]; then cp -r "$REPO/corpus" "$DIR/tree/corpus"; fi

# --- record pre-apply identities of every scoped file ------------------------
say ""
say "== pre-apply identities (scratch copies) =="
( cd "$DIR/tree" && sha256sum PROVINCE.md SKILL.md SCORECARD.md 2>/dev/null | tee -a "$LOG" )
( cd "$DIR/tree" && wc -l PROVINCE.md SKILL.md SCORECARD.md | tee -a "$LOG" )

# --- apply ------------------------------------------------------------------
say ""
say "== apply =="
APPLIED=0
cd "$DIR/tree" || exit 2
case "$PATCH" in
  *.diff|*.patch)
    if patch -p"$STRIP" --batch --forward --no-backup-if-mismatch < "$PATCH" >>"$LOG" 2>&1; then
      APPLIED=1; say "applied as unified diff (-p$STRIP): OK"
    else
      say "applied as unified diff (-p$STRIP): FAILED (see log)"
    fi
    ;;
  *)
    # prose patch: extract fenced blocks, honour "-" -> "+" hunks in order
    if python3 "$REPO/.ufo/waves/arc3-loop1-round4/claims/c2/RV-4/prose-apply.py" \
         "$PATCH" "$DIR/tree" >>"$LOG" 2>&1; then
      APPLIED=1; say "applied as prose patch (fenced -/+ hunks): OK"
    else
      say "applied as prose patch (fenced -/+ hunks): FAILED (see log)"
    fi
    ;;
esac

if [ "$APPLIED" -ne 1 ]; then
  say ""
  say "RESULT: UNAPPLIED — patch could not be applied to the scratch tree; no census verdict."
  exit 1
fi

say ""
say "== post-apply identities =="
( cd "$DIR/tree" && sha256sum PROVINCE.md SKILL.md SCORECARD.md 2>/dev/null | tee -a "$LOG" )
( cd "$DIR/tree" && wc -l PROVINCE.md SKILL.md SCORECARD.md | tee -a "$LOG" )

# --- census -----------------------------------------------------------------
say ""
say "== census on the patched scratch tree =="
( cd "$DIR/tree" && python3 .ufo/gates/c1-census-v10.py --root . --json ) \
  > "$DIR/census-after.json" 2>&1
CENSUS_RC=$?
say "census --json exit=$CENSUS_RC  -> $DIR/census-after.json"
( cd "$DIR/tree" && python3 .ufo/gates/c1-census-v10.py --root . --quiet ) \
  > "$DIR/census-after.txt" 2>&1
tail -8 "$DIR/census-after.txt" | tee -a "$LOG"

# --- differ -----------------------------------------------------------------
say ""
say "== differ vs baseline ($BASE) =="
python3 "$DIFFER" "$BASE" "$DIR/census-after.json" 2>&1 | tee -a "$LOG"
DIFF_RC=${PIPESTATUS[0]}

say ""
if [ "$DIFF_RC" -eq 0 ] && [ "$CENSUS_RC" -eq 0 ]; then
  say "RESULT: CONFORMANT — census PASS, no new gated locus."
  exit 0
fi
say "RESULT: DEFECT — census exit=$CENSUS_RC, differ exit=$DIFF_RC (see above)."
exit 1
