#!/bin/bash
# The five REA 6.5.0 runs behind env-*.json. Run from a scratch dir: unblob.log lands in cwd.
# REA refuses a pre-existing output dir; every run below uses a fresh one.
set -uo pipefail
S=${1:?usage: probe.sh <scratch dir>}
FIX=$(cd "$(dirname "$0")/fixtures" && pwd)
mkdir -p "$S"; cd "$S"

rea () {  # rea <outdir> <logname> <extra args...>
  local out=$1 log=$2; shift 2
  REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
    npx -y rea-agents@6.5.0 extract-firmware --format json --full-output "$@" >"$log" 2>"$log.err"
  echo "$log exit=$?"
}

# E1 depth-limited: ceiling 1, published file beside the gap -> env-depth1.json
rea "$S/out-d1" rea-d1.json --max-depth 1 "$FIX/outer.sqfs" "$S/out-d1"
# E2 control: default ceiling 3 descends, no gap, coverage complete -> env-depth3.json
rea "$S/out-d3" rea-d3.json --max-depth 3 "$FIX/outer.sqfs" "$S/out-d3"
# E3 missing dependency, LE branch: strip ~/.local/bin so sasquatch is unreachable -> env-nodep-le.json
PATH=$(echo "$PATH" | tr ':' '\n' | grep -v "^$HOME/.local/bin$" | paste -sd:) \
  rea "$S/out-nosq" rea-nosq.json --max-depth 2 "$FIX/outer.sqfs" "$S/out-nosq"
# E4 missing dependency, BE branch of a genuine AVM image -> env-nodep-avmbe.json
PATH=$(echo "$PATH" | tr ':' '\n' | grep -v "^$HOME/.local/bin$" | paste -sd:) \
  rea "$S/out-avmnodep" rea-avmnodep.json --max-depth 2 "$FIX/avm-pad.sqfs" "$S/out-avmnodep"
# E5 fatal body failure (sasquatch exit 1, files 0) -> env-fatal.json
rea "$S/out-fatal" rea-fatal.json --max-depth 2 "$FIX/lebig-corrupt2.sqfs" "$S/out-fatal"

# Reduction used for every env-*.json in this directory:
#   python3 -c 'import json,sys;d=json.load(open(sys.argv[1]))["data"];json.dump({k:d[k] for k in ("parameters","subject","provider","evidence_id")}|{"normalized_result":d["normalized_result"]},open(sys.argv[2],"w"),indent=1)' <log> <env.json>
