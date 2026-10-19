#!/usr/bin/env bash
# EX-14 discovery: find every round-4 patch text that targets a census-scoped
# file (PROVINCE.md / SKILL.md / SCORECARD.md), print it with its identity and
# a one-line "targets" summary.  Read-only over the repo.
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
R=$REPO/.ufo/waves/arc3-loop1-round4
echo "== round-4 candidate patch texts (targeting a scoped file) =="
find "$R" -type f \( -name "*.patch.md" -o -name "*.patch" -o -name "*.diff" -o -name "*.patch.txt" \) 2>/dev/null | sort | while read -r p; do
  tgt=$(grep -oE "(PROVINCE|SKILL|SCORECARD)\.md" "$p" 2>/dev/null | sort -u | tr '\n' ',' | sed 's/,$//')
  if [ -n "$tgt" ]; then
    printf '%s\n    targets=%s  sha256=%s\n' "${p#$R/}" "$tgt" "$(sha256sum "$p" | cut -c1-16)"
  fi
done
echo
echo "== any file mentioning a PROVINCE Frontier repair =="
grep -rl "Frontier" "$R/claims" 2>/dev/null | grep -v "\.out$\|\.log$" | sort | head -20
echo
echo "== seats landed =="
ls "$R/seats/" 2>/dev/null | tr '\n' ' '; echo