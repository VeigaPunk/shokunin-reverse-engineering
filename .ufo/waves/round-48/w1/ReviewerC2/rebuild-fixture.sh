#!/bin/sh
# Rebuilds the ReviewerC2 fixture: a clone of the lane at 663f30ee plus two
# commits that simulate the landing card (round-48 corrections + round section).
# Usage: S=/fast/scratch/hyaku/<seat> sh rebuild-fixture.sh
set -eu
S=${S:?set S to a scratch dir}
D="$S/fixture"
git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$D"
git -C "$D" rev-parse --show-toplevel   # must equal $D before any commit
cd "$D"
git checkout -q 663f30ee751694fb0970e7de68fe88356e680822
mkdir -p .ufo/waves/round-48/l1/scores
cat > .ufo/waves/round-48/w1-dispatch.json <<'EOF'
{"counts": {"spawn": 5, "resume": 0, "total": 5}}
EOF
cat > .ufo/waves/round-48/l1/scores/c2-at-landing.json <<'EOF'
{"atoms": 5, "verified": 5, "exempted": [], "mismatches": [], "corrections": 2, "met_target": true}
EOF
cat >> SCORECARD.md <<'EOF'

## Record corrections — round 48

Append-only repair of the self-assessment atoms `tools/round-48/record2.py` re-derives.

- corrects seats round-47: 1 waves, 75 seats total — `w1-dispatch.json` reports
  `counts.spawn 75`, and the round-47 section names no seats line at all.
- corrects quote round-47: exempted 1 — the cited receipt's own `exempted` list has
  one entry; the round-47 section quotes `exempted 2`.

## Round 48 — the meaning-bound registry counter and the record floor counter

Base `61b87d74`. The declared freeze is `0f06251b` (A4). Landings measured at
`61b87d74`. Waves: 5 + 0 = 5 seats.

| claim | axis / surface | before | after | counting command | measured at |
|---|---|---|---|---|---|
| R48-C1 | depth — craft rule block 25 and `tools/round-48/meanings.py` | exit 1 | exit 0 | `tools/round-48/meanings.py --root . --freeze 0f06251b --rev <REV>` | `61b87d74` |
| R48-C2 | calibration — `tools/round-48/record2.py` re-derives the card | exit 1 | exit 0 | `tools/round-48/record2.py --root . --freeze 0f06251b --rev <REV>` | `61b87d74` |

Seats were read off the dispatch files in `.ufo/waves/round-48/w1/` and
`.ufo/waves/round-48/w1-dispatch.json`. The counter receipt is
`.ufo/waves/round-48/l1/scores/c2-at-landing.json`. The round's window
`git log --name-status --format= dc73587a..dc73587a -- tools/round-48/ plans/round-48-claims.md` is empty.
EOF
git add SCORECARD.md .ufo/waves/round-48
GIT_AUTHOR_NAME=fix GIT_AUTHOR_EMAIL=f@f GIT_COMMITTER_NAME=fix GIT_COMMITTER_EMAIL=f@f \
  git commit -qm "simulated landing card"
mkdir -p .ufo/waves/round-48/w1/seat
echo evidence > .ufo/waves/round-48/w1/seat/report.md
git add .ufo/waves/round-48/w1
GIT_AUTHOR_NAME=fix GIT_AUTHOR_EMAIL=f@f GIT_COMMITTER_NAME=fix GIT_COMMITTER_EMAIL=f@f \
  git commit -qm "w1 dir"
git rev-parse HEAD
# Counter run (from the lane worktree; --root is the fixture):
#   cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
#   HYAKU_SCRATCH=$S python3 -I -B tools/round-48/record2.py \
#     --root $D --freeze 0f06251bf6a3a6964c715f67243d4df12e854258 --rev <HEAD above>
