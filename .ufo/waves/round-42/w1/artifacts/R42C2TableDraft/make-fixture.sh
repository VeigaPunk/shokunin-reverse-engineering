#!/bin/sh
# make-fixture.sh — build the block-21 fixture SKILL.md from the lane base plus this
# directory's drafts.  Read-only against the lane; writes only $OUT.
#
#   ./make-fixture.sh LANE BASE_REV OUT
#
# LANE     /home/vgpnk/Projects/shokunin/kaidoku-shokunin
# BASE_REV c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c
# OUT      where to write the fixture SKILL.md (never inside the lane)
set -eu
LANE=${1:?lane}
BASE=${2:?base rev}
OUT=${3:?out}
HERE=$(cd "$(dirname "$0")" && pwd)

git -C "$LANE" show "$BASE:SKILL.md" > "$OUT.base"

python3 - "$OUT.base" "$HERE/block21.md" "$OUT" <<'PY'
import sys

base, block_path, out = sys.argv[1:4]
text = open(base, encoding='utf-8').read()
block = open(block_path, encoding='utf-8').read()

old_tail = '  stale second text behind.\n'
new_tail = ('  stale second text behind. Superseded for routing and for the action column\n'
            '  by rule block 21 (table v4, round 42): v4\'s handler cells cover the seven\n'
            '  v1\u2013v3 handler names this table\'s `squashfs_v4_*` cells cannot match, so a\n'
            '  legacy chunk is labelled instead of falling to `unclassified`, and v4 adds the\n'
            '  `legacy-body-failure` row, whose action is a cross-read rather than the `-be`\n'
            '  wrapper.\n')
assert text.count(old_tail) == 1, 'block-20 bullet tail not found exactly once'
text = text.replace(old_tail, new_tail)

anchor = '## Config custody for live-probe rounds (SOP)\n'
assert text.count(anchor) == 1, 'config-custody anchor not found exactly once'
text = text.replace(anchor, block + '\n' + anchor)
open(out, 'w', encoding='utf-8').write(text)
print('fixture written: %s (%d lines)' % (out, text.count('\n')))
PY
rm -f "$OUT.base"
