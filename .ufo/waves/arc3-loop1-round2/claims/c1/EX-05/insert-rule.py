#!/usr/bin/env python3
"""EX-05 (c1, round 2) harness: insert a rule block into a scratch SKILL.md.

Inserts the block immediately before the "## Config custody for live-probe
rounds (SOP)" heading, i.e. at the end of the queue-drain craft section
(command A's rule-split region), so no pre-existing line in that region is
rewritten and the SKILL.md scope rows (10-16, 18-20) do not shift.

Usage: python3 insert-rule.py <root> <block-file>
Prints the sha256 of the scratch SKILL.md before and after.
"""
import hashlib
import pathlib
import sys

MARKER = "## Config custody for live-probe rounds (SOP)"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main(root, blockfile):
    skill = pathlib.Path(root) / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    block = pathlib.Path(blockfile).read_text(encoding="utf-8").rstrip("\n") + "\n"
    before = sha(skill)
    if MARKER not in text:
        print("MARKER-ABSENT: %r" % MARKER)
        return 2
    if block.strip() in text:
        print("ALREADY-APPLIED sha256=%s" % before)
        return 3
    head, tail = text.split(MARKER, 1)
    if not head.endswith("\n\n"):
        head = head.rstrip("\n") + "\n\n"
    new = head + block + "\n" + MARKER + tail
    skill.write_text(new, encoding="utf-8")
    print("before_sha256=%s after_sha256=%s added_lines=%d"
          % (before, sha(skill), new.count("\n") - text.count("\n")))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
