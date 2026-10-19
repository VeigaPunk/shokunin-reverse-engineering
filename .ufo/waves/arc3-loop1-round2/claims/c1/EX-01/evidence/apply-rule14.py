#!/usr/bin/env python3
"""Apply the rule #14 payload to a scratch SKILL.md (worktree form).

Insertion rule: the payload lines + one empty line go immediately after the
last line of rule #13, whose final line contains the anchor text
"kernel-OOM-killed (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37`)."
Nothing at or before that anchor line moves (rules #1-#13 byte-identical).
"""
import pathlib, sys

root = pathlib.Path(sys.argv[1])
payload = pathlib.Path(sys.argv[2]).read_text()
skill = root / "SKILL.md"
lines = skill.read_text().splitlines(keepends=True)

anchor = "kernel-OOM-killed (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37`)."
idx = [i for i, l in enumerate(lines) if anchor in l]
assert len(idx) == 1, "anchor not unique: %r" % idx
i = idx[0]
assert lines[i].startswith("  kernel-OOM-killed"), "anchor line unexpected"

payload_lines = payload.splitlines(keepends=True)
new = lines[:i + 1] + payload_lines + ["\n"] + lines[i + 1:]
skill.write_text("".join(new))
print("anchor_line=%d payload_lines=%d old_total=%d new_total=%d"
      % (i + 1, len(payload_lines), len(lines), len(new)))
