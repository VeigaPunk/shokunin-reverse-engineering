#!/usr/bin/env bash
# EX-19 re-certification: run the H3 battery against the LIVE census instrument.
# Usage: bash certify.sh [REPO_ROOT]   (default /home/vgpnk/Projects/shokunin/kaidoku-shokunin)
# Prints the live sha, the ordinary-run verdict, and the injection matrix.
# Scratch goes to /var/tmp/ex19-cert (never /tmp).
set -u
REPO="${1:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}"
WORK=/var/tmp/ex19-cert
mkdir -p "$WORK/root"
cp -p "$REPO/.ufo/gates/c1-census-v10.py" "$WORK/live.py"
cp -p "$REPO/PROVINCE.md" "$REPO/SKILL.md" "$REPO/SCORECARD.md" "$WORK/root/"
echo "live gate sha256: $(sha256sum "$WORK/live.py" | cut -d' ' -f1)"
echo "root copies:      $(sha256sum "$WORK/root/"*.md | awk '{printf "%s:%s ", $2, substr($1,1,8)}')"
echo "--- ordinary run at HEAD ---"
python3 "$WORK/live.py" --root "$REPO" | grep -E "^(G2 |UNREADABLE|DECLARED|VERDICT)"; echo "ordinary exit=${PIPESTATUS[0]}"
echo "--- injection matrix (expect: full+pin+ver = FAIL BLIND-INSTRUMENT;"
echo "    pin,ptr,pin+ptr,ver+ptr,h-pin64 = residual PASS; pin/ver narrowing = see notes) ---"
python3 "$REPO/.ufo/waves/arc3-loop1-round2/claims/c2/EX-19/tools/neuter.py" \
  --src "$WORK/live.py" --tag recert --root "$WORK/root" --outdir "$WORK" \
  --spec full --spec pin --spec ver --spec ptr --spec pin+ver --spec pin+ptr \
  --spec ver+ptr --spec h-ver67 --spec h-ver65 --spec h-pin64 --spec h-all67
echo "matrix manifest: $WORK/recert.matrix.json"
