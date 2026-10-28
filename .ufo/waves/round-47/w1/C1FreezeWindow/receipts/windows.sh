#!/bin/sh
# C1FreezeWindow: the two frozen-window probes on the real lane, with argv/rc/bytes/sha256.
set -u
S=/fast/scratch/hyaku/kaidoku-r47/C1FreezeWindow
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
F=5017e1f7299c3a812e87e7950148f54313dd279e
T=$(git -C "$L" rev-parse HEAD)
PATHS="tools/round-47 plans/round-47-claims.md"
cd "$S" || exit 9

emit() {  # emit <label> <base> <tip> <flagorder...>
  label=$1; base=$2; tip=$3; shift 3
  out="$S/win-$label.out"
  # shellcheck disable=SC2086
  git -C "$L" log "$@" "$base..$tip" -- $PATHS > "$out" 2>"$S/win-$label.err"
  rc=$?
  echo "label=$label"
  echo "  argv=git -C $L log $* $base..$tip -- $PATHS"
  echo "  flag-order=$*"
  echo "  rc=$rc bytes=$(wc -c < "$out") stdout_sha256=$(sha256sum < "$out" | cut -d' ' -f1) stderr_bytes=$(wc -c < "$S/win-$label.err")"
  echo "  stdout: $(cat "$out" | tr '\n' ' ')"
}

echo "tip=$T"
echo "freeze=$F"
echo "utc_start=$(date -u +%FT%TZ)"
# frozen order: -m BEFORE --diff-merges=first-parent (matches gate.py line 99)
emit c1-freeze-to-freeze  "$F" "$F" --name-status --format= -m --diff-merges=first-parent
emit c2-freeze-to-tip      "$F" "$T" --name-status --format= -m --diff-merges=first-parent
# same windows, flags REORDERED (R46-CL6's defect direction)
emit c3-freeze-to-freeze-reversed "$F" "$F" --name-status --format= --diff-merges=first-parent -m
emit c4-freeze-to-tip-reversed     "$F" "$T" --name-status --format= --diff-merges=first-parent -m
echo "utc_end=$(date -u +%FT%TZ)"

echo "--- supplementary arms (same window, independent of flag order) ---"
echo "net_diff_paths=$(git -C "$L" diff --name-status "$F" "$T" -- $PATHS | wc -l)"
echo "tree_oid_freeze=$(git -C "$L" rev-parse "$F:tools/round-47")"
echo "tree_oid_tip=$(git -C "$L" rev-parse "$T:tools/round-47")"
echo "claims_blob_freeze=$(git -C "$L" rev-parse "$F:plans/round-47-claims.md")"
echo "claims_blob_tip=$(git -C "$L" rev-parse "$T:plans/round-47-claims.md")"
echo "worktree_dirty_frozen_paths=$(git -C "$L" status --porcelain -- tools/round-47/ plans/round-47-claims.md | wc -l)"
echo "merges_in_window=$(git -C "$L" rev-list --merges "$F..$T" | wc -l)"
echo "commits_in_window=$(git -C "$L" rev-list "$F..$T" | wc -l)"
echo "derived_freeze=$(git -C "$L" log --format=%H -1 -- plans/round-47-claims.md)"
echo "sha_exact_py_freeze=$(git -C "$L" cat-file blob "$F:tools/round-47/exact.py" | sha256sum | cut -d' ' -f1)"
echo "sha_exact_py_tip=$(git -C "$L" cat-file blob "$T:tools/round-47/exact.py" | sha256sum | cut -d' ' -f1)"
echo "sha_exact_py_worktree=$(sha256sum "$L/tools/round-47/exact.py" | cut -d' ' -f1)"
