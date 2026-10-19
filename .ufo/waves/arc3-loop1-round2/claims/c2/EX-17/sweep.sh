#!/bin/bash
# usage: sweep.sh <instrument.py> <tag>
# Runs the instrument against every fixture root; writes one verbatim log per
# root and prints a compact table (verdict + exit + declared-class lines).
inst="$1"; tag="$2"; L=/var/tmp/ex17r2
ROOTS="head:/home/vgpnk/Projects/shokunin/kaidoku-shokunin
present-all:$L/root-present-all
absent-skill:$L/root-absent-skill
empty-skill:$L/root-empty-skill
unreadable-skill:$L/root-unreadable-skill
truncated-skill:$L/root-truncated-skill
skill-is-dir:$L/root-skill-is-dir
dangling-skill:$L/root-dangling-skill
blank-skill:$L/root-blank-skill
all-absent:$L/root-all-absent"
printf '%s\n' "$ROOTS" | while IFS=: read -r name root; do
  out="$L/logs/${tag}-${name}.txt"
  { echo "\$ python3 $(basename "$inst") --root $root --quiet"
    python3 "$inst" --root "$root" --quiet 2>&1
    echo "exit=$?"
    echo "--- instrument sha256: $(sha256sum "$inst" | cut -d' ' -f1)"
  } > "$out"
  printf '%-17s | %-7s | %s | %s\n' "$name" "$(grep -oE 'exit=[0-9]+' "$out" | tail -1)" \
    "$(grep -oE 'VERDICT: [A-Z]+ +\(stale=[0-9]+ ambiguous=[0-9]+ undeclared=[0-9]+ unresolved=[0-9]+\)' "$out" | head -1)" \
    "$(grep -iE 'unreadable|missing|SCOPE-ERRORS' "$out" | tr '\n' ' ' | cut -c1-110)"
done
