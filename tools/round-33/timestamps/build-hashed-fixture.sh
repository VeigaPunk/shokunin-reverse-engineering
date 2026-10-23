#!/usr/bin/env bash
# Bounded clone fixture for the hash-bound allowance wrapper.
# Reproduces the base blame times for the five allowed lines, then derives:
#   clone-green     unchanged (allowance must apply, gate green)
#   clone-sameline  synthetic future utc_end inserted into the allowed echo line (wrapper must refuse)
#   clone-unlisted  an extra unlisted synthetic future timestamp (tool must stay red)
# Synthetic timeline: the four source commits replicate base blame times (2026) so the
# pinned lines reproduce base findings; the two derived control commits are dated 2000
# and their injected instants 2001-02-03T04:05:06Z. 2001 is historic wall-clock and
# future relative to its own 2000 introducing commit, so no literal in this fixture is
# future at report/commit time. The values are synthetic controls, not execution evidence.
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
BASE=${HASHED_FIXTURE_BASE:-$HERE/hashed-fixture}
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
SRC=.ufo/waves/round-32
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
rm -rf "$BASE"
mkdir -p "$BASE/src/$SRC/a2after"
git init -q "$BASE/src"

commit_at() {
  local repo=$1 when=$2 msg=$3
  git -C "$repo" add -A
  GIT_AUTHOR_NAME='Timestamp Fixture' GIT_AUTHOR_EMAIL='fixture@example.invalid' \
  GIT_COMMITTER_NAME='Timestamp Fixture' GIT_COMMITTER_EMAIL='fixture@example.invalid' \
  GIT_AUTHOR_DATE="$when" GIT_COMMITTER_DATE="$when" \
  git -C "$repo" commit -q -m "$msg"
}

blob() {
  git -C "$REPO" cat-file blob "428315a8:$SRC/$1"
}

blob a2audit-gate.json >"$BASE/src/$SRC/a2audit-gate.json"
commit_at "$BASE/src" '2026-10-23T06:56:11+00:00' 'fixture: a2audit dispatch plan'

blob a2audit-settle.json >"$BASE/src/$SRC/a2audit-settle.json"
blob a2residual-dispatch.json >"$BASE/src/$SRC/a2residual-dispatch.json"
commit_at "$BASE/src" '2026-10-23T07:14:24+00:00' 'fixture: a2audit settle + residual dispatch plan'

blob a2residual-settle.json >"$BASE/src/$SRC/a2residual-settle.json"
commit_at "$BASE/src" '2026-10-23T07:30:33+00:00' 'fixture: residual settle plan'

blob a2after/timestamps-strict-at-9ef97f08.txt >"$BASE/src/$SRC/a2after/timestamps-strict-at-9ef97f08.txt"
commit_at "$BASE/src" '2026-10-23T07:41:55+00:00' 'fixture: frozen run receipt echo'

for name in green sameline unlisted; do
  git clone -q --no-hardlinks "$BASE/src" "$BASE/clone-$name"
done

# Same-line control: insert a future execution instant into the allowed echo line.
python3 -I -B - "$BASE/clone-sameline/$SRC/a2after/timestamps-strict-at-9ef97f08.txt" <<'PY'
import sys
path = sys.argv[1]
with open(path, "rb") as stream:
    lines = stream.read().split(b"\n")
line = lines[2]
needle = b'{"allow":[]'
assert line.startswith(needle), line[:40]
lines[2] = b'{"utc_end":"2001-02-03T04:05:06Z",' + line[1:]
with open(path, "wb") as stream:
    stream.write(b"\n".join(lines))
PY
commit_at "$BASE/clone-sameline" '2000-01-01T00:00:00+00:00' 'fixture: insert synthetic utc_end into frozen echo line'

# Unlisted control: a future timestamp on a line no allowance names.
mkdir -p "$BASE/clone-unlisted/$SRC/a2extra"
printf '{"utc_end":"2001-02-03T04:05:06Z"}\n' >"$BASE/clone-unlisted/$SRC/a2extra/unlisted.json"
commit_at "$BASE/clone-unlisted" '2000-01-01T00:00:00+00:00' 'fixture: add unlisted synthetic timestamp'

for name in green sameline unlisted; do
  printf '%s %s\n' "$name" "$(git -C "$BASE/clone-$name" rev-parse HEAD)"
done
