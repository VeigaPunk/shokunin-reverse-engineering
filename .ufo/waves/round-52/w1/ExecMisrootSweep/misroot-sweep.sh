#!/usr/bin/env bash
# Read-only fleet-root stray classifier. --apply copies lane artifacts byte-exactly
# into the designated lane seat before deleting the source stray.
set -euo pipefail
usage() { printf 'Usage: %s --fleet DIR --lane-seat DIR [--apply|--selftest]\n' "$0" >&2; exit 2; }
FLEET='' LANE_SEAT='' MODE=report
while (($#)); do case "$1" in
  --fleet) (($# >= 2)) || usage; FLEET=$2; shift 2;;
  --lane-seat) (($# >= 2)) || usage; LANE_SEAT=$2; shift 2;;
  --apply) MODE=apply; shift;; --selftest) MODE=selftest; shift;; *) usage;;
esac; done

# Never inspect or handle protected scratch/state/other-lane paths.
protected() {
  case "/$1/" in */.scratch/*|*/.ufo/state/*|*/.ufo/waves/*) return 0;; esac
  return 1
}
classify() {
  local file=$1
  if protected "$file"; then printf protected; return; fi
  if [[ -f $file ]] && [[ $(LC_ALL=C grep -aEic 'kaidoku|round-52' -- "$file" || :) -gt 0 ]]; then printf lane; else printf other; fi
}
report() {
  local fleet=$1 path full kind
  printf 'classification report (untracked paths; content match: kaidoku/round-52)\n'
  while IFS= read -r path; do
    [[ $path == '?? '* ]] || continue
    path=${path#\?\? }; path=${path%/}
    full=$fleet/$path
    kind=$(classify "$full")
    printf '%s\t%s\n' "$kind" "$path"
  done < <(git -C "$fleet" status --porcelain)
}
copy_apply() {
  local fleet=$1 seat=$2 path full dest kind
  while IFS= read -r path; do
    [[ $path == '?? '* ]] || continue
    path=${path#\?\? }; path=${path%/}; full=$fleet/$path
    kind=$(classify "$full"); [[ $kind == lane ]] || continue
    dest=$seat/$(basename -- "$path")
    printf 'would copy+cmp+delete: %s -> %s\n' "$full" "$dest"
    mkdir -p -- "$(dirname -- "$dest")"
    cp -- "$full" "$dest"
    cmp -- "$full" "$dest"
    rm -- "$full"
  done < <(git -C "$fleet" status --porcelain)
}
if [[ $MODE == selftest ]]; then
  [[ -n $FLEET && -n $LANE_SEAT ]] || usage
  # Fixture arguments are isolated repos supplied by the caller.
  [[ $(git -C "$FLEET" rev-parse --show-toplevel) == "$FLEET" ]] || { echo 'fixture root mismatch' >&2; exit 1; }
  mkdir -p "$LANE_SEAT"
  printf 'kaidoku round-52 planted fixture\n' > "$FLEET/planted-lane-stray.txt"
  printf 'unrelated content\n' > "$FLEET/non-lane-stray.txt"
  report "$FLEET"
  [[ $(classify "$FLEET/planted-lane-stray.txt") == lane ]]
  [[ $(classify "$FLEET/non-lane-stray.txt") == other ]]
  copy_apply "$FLEET" "$LANE_SEAT"
  cmp "$LANE_SEAT/planted-lane-stray.txt" "$LANE_SEAT/planted-lane-stray.txt"
  [[ ! -e $FLEET/planted-lane-stray.txt && -e $FLEET/non-lane-stray.txt ]]
  echo 'selftest: PASS'
  exit 0
fi
[[ -n $FLEET ]] || usage
report "$FLEET"
if [[ $MODE == apply ]]; then
  [[ -n $LANE_SEAT ]] || usage
  printf 'Apply plan shown above; performing lane-classified operations only.\n'
  copy_apply "$FLEET" "$LANE_SEAT"
fi
