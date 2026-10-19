#!/bin/bash
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=/var/tmp/ex14
run() {
  local label="$1" census="$2" root="$3"
  python3 "$census" --root "$root" > "$S/receipts-live-$label.out" 2>&1
  local ec=$?
  printf '%-30s exit=%d | %s | %s\n' "$label" "$ec" \
    "$(grep -m1 'G2 positive-assertion guard' "$S/receipts-live-$label.out" | sed 's/^ *//')" \
    "$(grep -m1 '^VERDICT' "$S/receipts-live-$label.out" | sed 's/^ *//')"
}
C="$S/census-live-v11.py"
run head "$C" "$REPO"
run atk-missing "$C" "$S/atk-missing"
run atk-nullskill "$C" "$S/atk-nullskill"
run atk-shrunk "$C" "$S/atk-shrunk"
run atk-blind-all "$S/census-live-v11-all-neutered.py" "$REPO"
