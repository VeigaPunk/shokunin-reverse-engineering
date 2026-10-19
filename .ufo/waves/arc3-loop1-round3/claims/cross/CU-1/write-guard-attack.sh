#!/usr/bin/env bash
# CU-1 (arc3-loop1-round3) independent write-guard attack battery.
# Fake HOME so that "custody paths" resolve inside scratch: the real custody
# paths can never be at risk from this script.
set -u
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
TOOL=.ufo/gates/custody-pair/custody-pair.py
FH=/var/tmp/cu1-r3/fakehome
FX=/var/tmp/cu1-r3/fx
rm -rf "$FH" "$FX"; mkdir -p "$FH/.config/devin" "$FH/.omp/agent" "$FH/.kimi-code" "$FX"
printf '{"mcp":1}\n' > "$FH/.config/devin/mcp_config.json"
printf '{"mcp":2}\n' > "$FH/.omp/agent/mcp.json"
printf 'key = "v"\n'  > "$FH/.kimi-code/config.toml"
printf '# bashrc\n'   > "$FH/.bashrc"
printf 'export X=1\n' > "$FH/.profile"
printf '{"scoped":true}\n' > "$FX/scope.json"
printf '{"scoped":2}\n'    > "$FX/scope2.json"

echo "TOOL-SHA-BEFORE $(sha256sum $TOOL | cut -d' ' -f1)"
run() { echo "--- $1"; shift; "$@" ; echo "exit=$?"; }

echo "=== A: --out over a canonical custody path (fake HOME) ==="
before=$(sha256sum "$FH/.bashrc" | cut -d' ' -f1)
HOME="$FH" run "A: capture --out \$FH/.bashrc" python3 $TOOL capture --out "$FH/.bashrc"
after=$(sha256sum "$FH/.bashrc" | cut -d' ' -f1)
echo "A-UNCHANGED: $([ "$before" = "$after" ] && echo yes || echo NO) (sha $before)"

echo "=== B: VZ-4 replay — --paths X --out X (both scratch) ==="
before=$(sha256sum "$FX/scope.json" | cut -d' ' -f1)
HOME="$FH" run "B: capture --paths \$FX/scope.json --out \$FX/scope.json" python3 $TOOL capture --paths "$FX/scope.json" --out "$FX/scope.json"
after=$(sha256sum "$FX/scope.json" | cut -d' ' -f1)
echo "B-UNCHANGED: $([ "$before" = "$after" ] && echo yes || echo NO)"

echo "=== C: --paths over a fake-custody path, --out same path ==="
before=$(sha256sum "$FH/.profile" | cut -d' ' -f1)
HOME="$FH" run "C: capture --paths \$FH/.profile --out \$FH/.profile" python3 $TOOL capture --paths "$FH/.profile" --out "$FH/.profile"
after=$(sha256sum "$FH/.profile" | cut -d' ' -f1)
echo "C-UNCHANGED: $([ "$before" = "$after" ] && echo yes || echo NO)"

echo "=== D: control — ordinary capture (scoped file + separate out) ==="
before=$(sha256sum "$FX/scope2.json" | cut -d' ' -f1)
HOME="$FH" run "D: capture --paths \$FX/scope2.json --out \$FX/out.txt" python3 $TOOL capture --paths "$FX/scope2.json" --out "$FX/out.txt"
after=$(sha256sum "$FX/scope2.json" | cut -d' ' -f1)
echo "D-SOURCE-UNCHANGED: $([ "$before" = "$after" ] && echo yes || echo NO)"
head -8 "$FX/out.txt" 2>/dev/null | tail -4

echo "=== E: 1-of-5 receipt under verify --live (D3) ==="
HOME="$FH" python3 $TOOL capture --paths "$FH/.bashrc" --label "1of5" --out "$FX/one-of-five.txt" >/dev/null 2>&1; echo "capture-1of5 exit=$?"
HOME="$FH" run "E1: verify one-of-five --live" python3 $TOOL verify "$FX/one-of-five.txt" --live
HOME="$FH" run "E2: verify one-of-five --live --require-paths 5" python3 $TOOL verify "$FX/one-of-five.txt" --live --require-paths 5

echo "TOOL-SHA-AFTER  $(sha256sum $TOOL | cut -d' ' -f1)"