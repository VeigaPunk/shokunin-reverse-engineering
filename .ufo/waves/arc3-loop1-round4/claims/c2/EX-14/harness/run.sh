#!/usr/bin/env bash
# EX-14 run: fresh scratch root -> apply every patch -> census -> capture.
# usage: run.sh <label> [patch ...]
set -u
W=/var/tmp/arc3r4-ex14
LABEL="$1"; shift
ROOT="$W/run-$LABEL"
OUT="$W/out/$LABEL"
rm -rf "$ROOT" "$OUT"; mkdir -p "$ROOT" "$OUT"
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin

# baseline scoped files, taken from the repo (never written back)
cp "$REPO/PROVINCE.md" "$REPO/SKILL.md" "$REPO/SCORECARD.md" "$ROOT/"

{
  echo "# EX-14 run '$LABEL'  $(date -u +%FT%TZ)"
  echo "## scratch root: $ROOT"
  sha256sum "$ROOT"/*.md
} > "$OUT/before-sha256.txt"

echo "== APPLY ==" | tee "$OUT/apply.log"
APPLY_RC=0
if [ "$#" -gt 0 ]; then
  python3 "$W/harness/apply_patches.py" --root "$ROOT" \
      $(for p in "$@"; do printf -- '--patch %q ' "$p"; done) 2>&1 | tee -a "$OUT/apply.log"
  APPLY_RC=${PIPESTATUS[0]}
else
  echo "(no patches)" | tee -a "$OUT/apply.log"
fi

# Fail closed: a patch that did not apply must not be reported as a census
# verdict on "the patched tree" — that would read as a PASS over unpatched bytes.
if grep -qE "applied=0 failed=[1-9]|NO-APPLICABLE-BLOCK|HUNK-NOT-FOUND|^SKIP " "$OUT/apply.log"; then
  echo "APPLY-FAILED: a patch did not apply — no census verdict is issued." | tee -a "$OUT/apply.log"
  echo "APPLY-EXIT=$APPLY_RC"
  exit 1
fi

echo "== AFTER ==" | tee -a "$OUT/apply.log"
sha256sum "$ROOT"/*.md | tee "$OUT/after-sha256.txt"

echo "== CENSUS (--root $ROOT) ==" | tee "$OUT/census.log"
python3 "$REPO/.ufo/gates/c1-census-v10.py" --root "$ROOT" >> "$OUT/census.log" 2>&1
echo "CENSUS-EXIT=$?" >> "$OUT/census.log"
tail -1 "$OUT/census.log"
