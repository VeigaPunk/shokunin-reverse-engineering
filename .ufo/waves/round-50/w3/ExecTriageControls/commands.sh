#!/bin/sh
# R50-C3 control fixtures — every command this seat ran, and the post-freeze scoring
# commands the L1 runs once the v5 instrument is frozen.
#
# Everything is offline: no REA, no network.  Lane root is absolute; the seat writes
# only inside .ufo/waves/round-50/w3/ExecTriageControls/.
#
# Exit codes are semantic: 0 met/clean, 1 not met/violation, 2 could-not-evaluate.

set -eu
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
BASE=f890bbead20ca2c549487167f56876ae47f1e1a4
SEAT="$LANE/.ufo/waves/round-50/w3/ExecTriageControls"
ENVREL=.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes

# ---------------------------------------------------------------- 1. provenance
git -C "$LANE" show "$BASE":SKILL.md
git -C "$LANE" rev-parse "$BASE^{commit}"
git -C "$LANE" ls-tree -r --name-only "$BASE" -- "$ENVREL"
git -C "$LANE" ls-tree -r "$BASE" -- "$ENVREL"

# ---------------------------------------------------------------- 2. rebuild (deterministic)
#   SCRATCH=/fast/scratch/hyaku/kaidoku-r50/w3-ExecTriageControls
#   export TMPDIR="$SCRATCH"; mkdir -p "$SCRATCH"
#   python3 "$SEAT/build_controls.py"          # rewrites every artefact in $SEAT
#
# The generator reads only committed lane bytes and the 126 committed envelopes.

# ---------------------------------------------------------------- 3. table side, measured
# The lane's own evaluator, run offline on the committed envelopes with each control
# document as --skill.  Exit 2 on the junk control (duplicate labels refused).
python3 -I -B "$LANE/tools/round-42/sqfs-triage-v4.py" --skill "$SEAT/ctl-do-nothing.skill.md" \
  --table-only
python3 -I -B "$LANE/tools/round-42/sqfs-triage-v4.py" --skill "$SEAT/ctl-junk.skill.md" \
  --table-only
python3 -I -B "$LANE/tools/round-42/sqfs-triage-v4.py" --skill "$SEAT/ctl-guard-deleted.skill.md" \
  --table-only
python3 -I -B "$LANE/tools/round-42/sqfs-triage-v4.py" --skill "$SEAT/ctl-action-swapped.skill.md" \
  --table-only

# ---------------------------------------------------------------- 4. post-freeze scoring (L1)
# The frozen instrument must be able to score a table that is not SKILL.md at --rev,
# so --skill (or an equivalent) is required; see README.md "Instrument requirements".
#
# for CTL in ctl-do-nothing ctl-junk ctl-guard-deleted ctl-action-swapped; do
#   python3 -I -B "$LANE/tools/round-50/sqfs-triage-v5.py" \
#     --root "$LANE" --rev <REV> --freeze <FREEZE> \
#     --envelopes "$ENVREL" \
#     --skill "$SEAT/$CTL.skill.md" \
#     --json-out "$SEAT/scores/$CTL.json"
# done
#
# Each must exit 1 with pair_mismatches equal to the count in
# "$SEAT/$CTL.expected-red.json" for the family-set reading the instrument implements.
# A control that exits 0 stops C3 (attempt-2 claims, R50-C3 kill rule).
