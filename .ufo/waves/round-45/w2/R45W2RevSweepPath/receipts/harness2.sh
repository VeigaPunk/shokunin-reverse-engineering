#!/usr/bin/env bash
set -u
S=/fast/scratch/hyaku/kaidoku-r45/R45W2RevSweepPath
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
mkdir -p "$S/out"
rec(){ local label=$1; shift; local out rc ts sha
  out=$("$@" 2>&1); rc=$?
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  printf '%s\n' "$out" > "$S/out/$label.out"
  sha=$(printf '%s' "$out" | sha256sum | cut -d' ' -f1)
  printf '%s\t%s\t%s\t%s\t%s\n' "$label" "$ts" "$rc" "$sha" "$*" >> "$S/receipts.tsv"
  printf '%-42s rc=%-3s sha=%s\n' "$label" "$rc" "${sha:0:16}"; }
rec r35-jj-has-no-hooks   bash -c "echo \"help_hits=\$(jj help 2>/dev/null | grep -ci hook) config_hits=\$(jj config list --include-defaults 2>/dev/null | grep -ci hook)\""
rec r36-no-lane-commit-wrapper bash -c "grep -rn 'jj-lane.sh commit' $LANE/tools/ || echo NONE"
rec r37-preflight-invokers bash -c "grep -rln 'frozen-path-preflight' $LANE/tools/ | sort"
rec r38-c86-path-count  bash -c "git -C $LANE show --name-only --format= c86ea508 | grep -c ."
rec r39-c86-frozen-subset bash -c "git -C $LANE show --name-only --format= c86ea508 | grep -E '^tools/round-44/'"
rec r40-inline-sweep-pathspec bash -c "sed -n '155,162p' /home/vgpnk/Projects/shokunin/scripts/hyaku/inline.sh"
rec r41-fleet-commit-commitcode bash -c "sed -n '67,89p' /home/vgpnk/Projects/shokunin/scripts/hyaku/fleet-commit.sh"
rec r42-jjlane-commitscope bash -c "sed -n '545,560p;694,716p' /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh"
rec r43-census bash -c "python3 $S/census.py"
rec r44-script-perms bash -c "stat -c '%A %U:%G %n' /home/vgpnk/Projects/shokunin/scripts/hyaku/fleet-commit.sh /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh; id -un"
