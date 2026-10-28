#!/usr/bin/env bash
# R45W2C1Rerun attack E (self-contained): does the restored/commit arm see a frozen path
# named only by --freeze-path (the round-45 claims file) when the documented invocation
# passes --pathspec tools/round-45/ only?
#
# Repro of the sealed receipt d-repro.out (sha256 546fc57260241d33cadb480483cc2765769e48a4d358b9e24aebfd61b03e0f9b
# for the stdout of the recorded run). Fixture commit ids differ per run; the exit codes
# and receipt fields do not.
#
# preflight-at-A1.py in this directory is the interpreter extracted from
# 1f4b27f82353d6544dc0c8048b3cfdadd8525d12, sha256
# 633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
PF="$HERE/preflight-at-A1.py"
S=${S:-/fast/scratch/hyaku/kaidoku-r45/R45W2C1Rerun-repro}
mkdir -p "$S" || exit 89
export TMPDIR="$S" HYAKU_SCRATCH="$S"
D=$(mktemp -d -p "$S" d-fixture.XXXXXX) || exit 90
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t

git -C "$D" init -q || exit 91
TOP=$(git -C "$D" rev-parse --show-toplevel) || exit 92
[ "$TOP" = "$D" ] || { echo "TOPLEVEL MISMATCH: $TOP != $D" >&2; exit 93; }

mkdir -p "$D/plans" "$D/tools/round-45"
awk 'BEGIN{for(i=0;i<147;i++)print "claims line " i}' > "$D/plans/round-45-claims.md"
awk 'BEGIN{for(i=0;i<10;i++)print "c1 line " i}'     > "$D/tools/round-45/c1-counter.py"
awk 'BEGIN{for(i=0;i<10;i++)print "c2 line " i}'     > "$D/tools/round-45/c2-counter.py"
awk 'BEGIN{for(i=0;i<10;i++)print "pf line " i}'     > "$D/tools/round-45/frozen-path-preflight.py"
git -C "$D" add -A && git -C "$D" commit -q -m freeze || exit 94
F=$(git -C "$D" rev-parse HEAD)

# tamper the claims file, then restore it to the exact FREEZE bytes
awk 'BEGIN{for(i=0;i<147;i++)print "TAMPERED " i}' > "$D/plans/round-45-claims.md"
git -C "$D" add -A && git -C "$D" commit -q -m "tamper claims" || exit 95
awk 'BEGIN{for(i=0;i<147;i++)print "claims line " i}' > "$D/plans/round-45-claims.md"
git -C "$D" add -A && git -C "$D" commit -q -m "restore claims to freeze bytes" || exit 96
R=$(git -C "$D" rev-parse HEAD)

B_F=$(git -C "$D" rev-parse "$F:plans/round-45-claims.md")
B_R=$(git -C "$D" rev-parse "$R:plans/round-45-claims.md")
[ "$B_F" = "$B_R" ] || { echo "BLOB MISMATCH: $B_F != $B_R" >&2; exit 97; }

echo "fixture=$D freeze=$F rev=$R claims_blob_at_both=$B_F"
echo "--- counter's own frozen-path arm (unscoped, as tools/round-45/c1-counter.py runs it) ---"
git -C "$D" log --name-only --format= "$F..$R" -- plans/round-45-claims.md tools/round-45 | sed '/^$/d'

echo "--- gate with the documented invocation: --pathspec tools/round-45/ only ---"
python3 -I -B "$PF" --root "$D" --freeze "$F" --rev "$R" \
  --pathspec tools/round-45/ --freeze-path tools/round-45 \
  --freeze-path plans/round-45-claims.md --require-pathspec
echo "GATE_EXIT=$?"

echo "--- gate with the claims file also as a --pathspec (the L1's own both-paths receipt) ---"
python3 -I -B "$PF" --root "$D" --freeze "$F" --rev "$R" \
  --pathspec tools/round-45/ --pathspec plans/round-45-claims.md \
  --freeze-path tools/round-45 --freeze-path plans/round-45-claims.md --require-pathspec
echo "GATE_EXIT_BOTH=$?"
