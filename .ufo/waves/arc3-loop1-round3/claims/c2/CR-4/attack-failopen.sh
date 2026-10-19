#!/usr/bin/env bash
# =============================================================================
# CR-4 follow-up probe — does the inode arm fail open when the SCOPED path side
# cannot be stat'ed? (assertion under test: guard refuses "a path it measures";
# measured shape: _same_file() catches OSError and returns False)
#
# Setup: the scoped file lives in a parent dir with mode 000 (no traversal), and
# a hardlink alias lives outside it. --out is the alias, --paths is the blocked
# path. Neither the resolve arm (names differ) nor the inode arm (os.stat on the
# blocked side raises EACCES) can see the alias.
#
# Scratch-only (/dev/shm), unprivileged, sandboxed HOME.
# usage: attack-failopen.sh <custody-pair.py> <label>
# =============================================================================
set -u
export PYTHONDONTWRITEBYTECODE=1
TOOL="$(readlink -f "$1")"; LABEL="${2:-unlabeled}"
TOOL_SHA=$(sha256sum "$TOOL" | cut -d' ' -f1)
SB=$(mktemp -d /dev/shm/cr4-failopen-XXXXXX) || exit 1
export TMPDIR="$SB"
H="$SB/home"; B="$SB/blocked"; S="$SB/outside"
mkdir -p "$H" "$B" "$S"
printf 'sandbox bashrc\n' > "$H/.bashrc"

echo "== CR-4 fail-open probe =="
echo "variant: $LABEL   tool sha256: $TOOL_SHA"
echo "sandbox: $SB"

printf 'scoped victim bytes\n' > "$B/watch.conf"
ln -f "$B/watch.conf" "$S/alias.conf"     # hardlink alias, outside the blocked dir
chmod 000 "$B"
before=$(sha256sum "$S/alias.conf" | cut -d' ' -f1)
echo "scoped path : $B/watch.conf  (parent mode 000 — untraversable)"
echo "alias path  : $S/alias.conf  (same inode; traversable)"
echo "alias sha256 before: $before"

HOME="$H" python3 "$TOOL" capture --out "$S/alias.conf" --paths "$B/watch.conf" \
    --label failopen-probe > "$SB/out.txt" 2> "$SB/err.txt"
rc=$?
chmod 700 "$B"
after=$(sha256sum "$S/alias.conf" | cut -d' ' -f1)
echo "exit=$rc"
echo "stdout: $(head -2 "$SB/out.txt" | tr '\n' '|')"
echo "stderr: $(head -2 "$SB/err.txt" | tr '\n' '|')"
echo "alias sha256 after : $after"
if [ "$after" = "$before" ]; then
  echo "verdict: REFUSED-or-missed / victim-UNCHANGED"
else
  echo "verdict: ALLOWED / victim-CLOBBERED through a blocked-side alias"
fi
echo "sandbox kept: $SB"