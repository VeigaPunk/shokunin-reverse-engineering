#!/usr/bin/env bash
# SC-3 guard-scope harness — write-guard scope, incl. the canonical-path direction
# under a SANDBOXED $HOME (so no real custody path can be written even if a
# revision regresses the canonical guard). Scratch-only for real paths.
# usage: guard-sandbox.sh <custody-pair.py> <out-root>
set -u
TOOL="$1"; OUT="$2"
WORK="$OUT/work"; H="$WORK/home"; S="$WORK/scope"
rm -rf "$OUT"; mkdir -p "$OUT" "$H/.config/devin" "$H/.omp/agent" "$H/.kimi-code" "$S"
printf 'sandbox bashrc\n'   > "$H/.bashrc"
printf 'sandbox profile\n'  > "$H/.profile"
printf '{sandbox}\n'        > "$H/.config/devin/mcp_config.json"
printf '{sandbox}\n'        > "$H/.omp/agent/mcp.json"
printf '[sandbox]\n'        > "$H/.kimi-code/config.toml"

echo "tool=$TOOL sha256=$(sha256sum "$TOOL" | cut -d' ' -f1) date=$(date -Is)" > "$OUT/guard.log"

t() { # t <name> <victim> <out> <paths...>
  local name="$1" victim="$2" out="$3"; shift 3
  local b a rc
  b=$(sha256sum "$victim" 2>/dev/null | cut -d' ' -f1)
  echo "### $name" >> "$OUT/guard.log"
  echo "\$ HOME=$H python3 $TOOL capture --out $out --paths $*" >> "$OUT/guard.log"
  HOME="$H" python3 "$TOOL" capture --out "$out" --paths "$@" --label "$name" >> "$OUT/guard.log" 2>&1
  rc=$?
  a=$(sha256sum "$victim" 2>/dev/null | cut -d' ' -f1)
  echo "exit=$rc victim=$victim" >> "$OUT/guard.log"
  echo "victim-sha before=$b after=$a" >> "$OUT/guard.log"
  if [ "$b" = "$a" ]; then echo "verdict=UNCHANGED" >> "$OUT/guard.log"; else echo "verdict=CLOBBERED" >> "$OUT/guard.log"; fi
  echo "---" >> "$OUT/guard.log"
}

printf 'victim G1\n' > "$S/guarded.conf"
t G1-scoped-as-out        "$S/guarded.conf" "$S/guarded.conf" "$S/guarded.conf"
t G2-canonical-bashrc-as-out "$H/.bashrc"  "$H/.bashrc"     "$S/guarded.conf"
printf 'victim G3\n' > "$S/g3.conf"
t G3-scope-includes-canonical "$H/.profile" "$H/.profile"   "$S/g3.conf" "$H/.profile"
# G4 (D7 adjacent): hardlink alias of the scoped path used as --out
printf 'victim G4\n' > "$S/guarded4.conf"
ln "$S/guarded4.conf" "$S/alias4.conf" 2>/dev/null || echo "note: hardlink fixture failed" >> "$OUT/guard.log"
t G4-hardlink-alias-as-out "$S/guarded4.conf" "$S/alias4.conf" "$S/guarded4.conf"
echo "done" >> "$OUT/guard.log"
cat "$OUT/guard.log"