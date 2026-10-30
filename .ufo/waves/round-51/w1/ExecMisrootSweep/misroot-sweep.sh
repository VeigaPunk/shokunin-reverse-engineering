#!/usr/bin/env bash
set -euo pipefail

usage() { printf 'usage: %s [--apply | --selftest] <fleet> <lane>\n' "$0" >&2; exit 2; }

classify() {
  local path=$1 content=$2
  case "$path" in .ufo/state/*|.scratch/*|*/.ufo/state/*|*/.scratch/*) printf 'protected\n'; return ;; esac
  if [[ "$path" == *kaidoku* || "$path" == *round-51* || "$content" == *kaidoku* || "$content" == *round-51* ]]; then
    printf 'lane\n'
  else
    printf 'foreign\n'
  fi
}

classify_file() { classify "$1" "$(cat -- "$2")"; }

copy_file() {
  local source=$1 target=$2
  [[ ! -e "$target" ]] || { printf 'refusing to overwrite: %s\n' "$target" >&2; return 2; }
  mkdir -p "$(dirname "$target")"
  cp -- "$source" "$target"
  if ! cmp -- "$source" "$target"; then rm -f -- "$target"; return 2; fi
  rm -- "$source"
}

run() {
  local mode=$1 fleet=$2 lane=$3
  [[ -d "$fleet/.git" || -f "$fleet/.git" ]] || { printf 'not a git repository: %s\n' "$fleet" >&2; return 2; }
  [[ -d "$lane" ]] || { printf 'lane directory missing: %s\n' "$lane" >&2; return 2; }
  local line status path kind target
  local -a files=() kinds=() targets=()
  while IFS= read -r -d '' line; do
    status=${line:0:2}; path=${line:3}
    [[ "$status" == '??' ]] || continue
    kind=$(classify_file "$path" "$fleet/$path")
    target="$lane/$path"
    files+=("$path"); kinds+=("$kind"); targets+=("$target")
    printf '%-8s %s\n' "$kind" "$path"
  done < <(git -C "$fleet" status --porcelain --untracked-files=all -z)
  if [[ "$mode" != apply ]]; then return 0; fi
  printf 'Proposed actions (only lane-classified paths):\n'
  local i
  for i in "${!files[@]}"; do
    [[ "${kinds[$i]}" == lane ]] && printf 'copy %q -> %q; cmp; unlink source\n' "$fleet/${files[$i]}" "${targets[$i]}"
  done
  for i in "${!files[@]}"; do
    [[ "${kinds[$i]}" == lane ]] || continue
    copy_file "$fleet/${files[$i]}" "${targets[$i]}"
  done
}

selftest() {
  local root fleet lane lane_file foreign_file protected_file
  root=$(mktemp -d "${TMPDIR:-/tmp}/misroot-sweep.XXXXXX")
  trap 'rm -rf "$root"' RETURN
  fleet="$root/fleet"; lane="$root/lane"
  mkdir -p "$fleet" "$lane" "$fleet/.ufo/state"
  git -C "$fleet" init -q
  [[ "$(git -C "$fleet" rev-parse --show-toplevel)" == "$fleet" ]] || return 2
  git -C "$fleet" config user.name 'Fixture Only'
  git -C "$fleet" config user.email 'fixture@example.invalid'
  printf 'tracked\n' > "$fleet/tracked"
  git -C "$fleet" add tracked
  git -C "$fleet" commit -qm fixture
  lane_file="$fleet/random-note.txt"; foreign_file="$fleet/foreign.txt"
  protected_file="$fleet/.ufo/state/round-51.txt"
  printf 'mentions round-51 lane context\n' > "$lane_file"
  printf 'foreign stray\n' > "$foreign_file"
  printf 'protected stray\n' > "$protected_file"
  printf 'SELFTEST: content classification\n'
  [[ "$(classify_file random-note.txt "$lane_file")" == lane ]]
  [[ "$(classify_file foreign.txt "$foreign_file")" == foreign ]]
  [[ "$(classify .ufo/state/round-51.txt round-51)" == protected ]]
  printf 'SELFTEST: apply\n'
  run apply "$fleet" "$lane"
  [[ -f "$lane/random-note.txt" && ! -e "$lane_file" ]]
  cmp "$lane/random-note.txt" <(printf 'mentions round-51 lane context\n')
  [[ -f "$foreign_file" && -f "$protected_file" ]]
  printf 'SELFTEST PASS: content-classified stray copied byte-exact then removed; foreign and protected untouched\n'
}

if [[ "${1:-}" == --selftest ]]; then selftest; exit $?; fi
mode=report
if [[ "${1:-}" == --apply ]]; then mode=apply; shift; fi
[[ $# == 2 ]] || usage
run "$mode" "$1" "$2"
