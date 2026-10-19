#!/usr/bin/env bash
# EX-21 external creep audit runner (arc3-loop1-round2).
# Usage: run-audit.sh <baseline-census.py> <landed-census.py> <repo-root> <outdir>
# Writes receipts into <outdir>; writes nothing inside the repo except <outdir>.
set -u
BASE="$1"; LANDED="$2"; REPO="$3"; OUT="$4"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT"

echo "== identities ==" | tee "$OUT/identities.txt"
sha256sum "$BASE" "$LANDED" | tee -a "$OUT/identities.txt"
wc -l -c "$BASE" "$LANDED" | tee -a "$OUT/identities.txt"
stat -c '%n ino=%i mtime=%Y ctime=%Z size=%s' "$BASE" "$LANDED" | tee -a "$OUT/identities.txt"

echo "== EX-21 scope-audit compare (SCOPE bytes) =="
python3 "$HERE/scope-audit.py" compare "$BASE" "$LANDED" > "$OUT/scope-audit-compare.out" 2>&1
echo "exit=$?" >> "$OUT/scope-audit-compare.out"

echo "== round-1 CR-5 scope-diff.py verbatim (second opinion) =="
python3 "$HERE/cr5-tool/scope-diff.py" "$BASE" "$LANDED" > "$OUT/cr5-scope-diff.out" 2>&1
echo "exit=$?" >> "$OUT/cr5-scope-diff.out"

echo "== diff-surface =="
python3 "$HERE/diff-surface.py" "$BASE" "$LANDED" --diff > "$OUT/diff-surface.out" 2>&1

echo "== run invariance (both instruments at repo HEAD) =="
python3 "$HERE/scope-audit.py" invariance "$BASE" "$LANDED" "$REPO" > "$OUT/invariance.out" 2>&1
echo "exit=$?" >> "$OUT/invariance.out"

echo "== H1 injection: absent-file classes (both instruments) =="
for victim in SKILL.md PROVINCE.md SCORECARD.md; do
  SCRATCH=$(mktemp -d /var/tmp/ex21/h1-XXXXXX)
  for f in PROVINCE.md SKILL.md SCORECARD.md; do
    [ "$f" = "$victim" ] && continue
    cp "$REPO/$f" "$SCRATCH/$f"
  done
  {
    echo "--- victim=$victim root=$SCRATCH ---"
    echo "[before instrument]"
    python3 "$BASE" --root "$SCRATCH" --quiet; echo "exit=$?"
    echo "[landed instrument]"
    python3 "$LANDED" --root "$SCRATCH" --quiet; echo "exit=$?"
  } >> "$OUT/h1-absent.out" 2>&1
  rm -rf "$SCRATCH"
done

echo "== H3 injection: neutered needles (blind instrument) =="
for src in "$BASE" "$LANDED"; do
  tag=$([ "$src" = "$BASE" ] && echo before || echo landed)
  BLIND="/var/tmp/ex21/blind-$tag.py"
  python3 - "$src" "$BLIND" <<'PY'
import re, sys
txt = open(sys.argv[1], encoding="utf-8").read()
for name in ("PIN", "VER", "PTR"):
    txt = re.sub(r"(?m)^%s = re\.compile\(.*\)$" % name,
                 '%s = re.compile(r"(?!x)x")' % name, txt, count=1)
open(sys.argv[2], "w", encoding="utf-8").write(txt)
PY
  grep -n '^PIN = \|^VER = \|^PTR = ' "$BLIND" > "$OUT/h3-blind-$tag.constants.txt"
  {
    echo "--- $tag instrument ($BLIND) run at repo HEAD ---"
    python3 "$BLIND" --root "$REPO" --quiet; echo "exit=$?"
  } >> "$OUT/h3-blind.out" 2>&1
done

echo "== W: declared-bound teeth (planted locus past the bound must UNDECLARED-FAIL) =="
{
  for src in "$BASE" "$LANDED"; do
    tag=$([ "$src" = "$BASE" ] && echo before || echo landed)
    WROOT=$(mktemp -d /var/tmp/ex21/w-XXXXXX)
    cp "$REPO/PROVINCE.md" "$REPO/SKILL.md" "$REPO/SCORECARD.md" "$WROOT/"
    printf 'planted probe line — rea-agents@6.3.0 lives here\n' >> "$WROOT/SCORECARD.md"
    echo "--- $tag instrument, planted locus appended to SCORECARD.md (now $(wc -l < "$WROOT/SCORECARD.md") lines) ---"
    python3 "$src" --root "$WROOT" --quiet; echo "exit=$?"
    rm -rf "$WROOT"
  done
} > "$OUT/bound-teeth.out" 2>&1

echo "== T: truncation below declared max end (new G19 class) =="
{
  cut() { python3 -c "import sys; L=open(sys.argv[1]).read().splitlines(); open(sys.argv[2],'w').write('\n'.join(L[:int(sys.argv[3])])+'\n')" "$1" "$2" "$3"; }
  for case in "PROVINCE.md 130" "SKILL.md 19" "SCORECARD.md 850"; do
    set -- $case; victim=$1; keep=$2
    for src in "$BASE" "$LANDED"; do
      tag=$([ "$src" = "$BASE" ] && echo before || echo landed)
      TROOT=$(mktemp -d /var/tmp/ex21/t-XXXXXX)
      for f in PROVINCE.md SKILL.md SCORECARD.md; do
        if [ "$f" = "$victim" ]; then cut "$REPO/$f" "$TROOT/$f" "$keep"; else cp "$REPO/$f" "$TROOT/$f"; fi
      done
      echo "--- victim=$victim truncated to $keep lines [$tag] ---"
      python3 "$src" --root "$TROOT" --quiet; echo "exit=$?"
      rm -rf "$TROOT"
    done
  done
} > "$OUT/truncation.out" 2>&1

echo "== ordinary run at HEAD on both instruments =="
{
  echo "[before]"; python3 "$BASE" --root "$REPO" --quiet; echo "exit=$?"
  echo "[landed]"; python3 "$LANDED" --root "$REPO" --quiet; echo "exit=$?"
} > "$OUT/head-runs.out" 2>&1

echo "== done: receipts in $OUT =="
ls -la "$OUT"
