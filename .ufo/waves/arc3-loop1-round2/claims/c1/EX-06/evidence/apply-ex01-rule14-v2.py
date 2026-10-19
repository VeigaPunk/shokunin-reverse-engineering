#!/usr/bin/env python3
"""EX-06: extract EX-01's rule-#14 payload verbatim, verify its self-identity
claim (896 B / a47dc38d...), apply it per EX-01's anchor recipe to a scratch
tree, and verify the resulting SKILL.md identity (385 lines / 19057c13...).

Usage: apply-ex01-rule14.py <ex01-patch-md> <tree-dir>
Exit 0 + one provenance line on success; nonzero on any mismatch (a mismatch
means a stale self-identity in the artifact -- report, do not paper over).
"""
import hashlib
import pathlib
import sys

PIN_PAYLOAD_BYTES = 1071
PIN_PAYLOAD_SHA = "6cc388cb61a3023e8e62a0f63c0ff2e275665706373b184ad7d4801c3c91718f"
PIN_SKILL_LINES = 387
PIN_SKILL_SHA = "a8170b96450f871282027b9adbc89cde08611457deb3a506cae3567701cd7e28"
ANCHOR = "kernel-OOM-killed (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37`)."


def main(patchfile, tree):
    text = pathlib.Path(patchfile).read_text(encoding="utf-8")
    payload = text.split("<!-- payload-begin -->\n", 1)[1].split("<!-- payload-end -->", 1)[0]
    pb = payload.encode()
    got = hashlib.sha256(pb).hexdigest()
    ok = (len(pb) == PIN_PAYLOAD_BYTES and got == PIN_PAYLOAD_SHA)
    print("payload_bytes=%d payload_sha256=%s identity_claim=%s"
          % (len(pb), got, "MATCH" if ok else "STALE"))
    if not ok:
        return 2
    skill = pathlib.Path(tree) / "SKILL.md"
    s = skill.read_text(encoding="utf-8")
    if payload in s:
        print("ALREADY-APPLIED")
        return 3
    needle = ANCHOR + "\n"
    if s.count(needle) != 1:
        print("ANCHOR-COUNT=%d (need 1)" % s.count(needle))
        return 4
    skill.write_text(s.replace(needle, needle + payload + "\n", 1), encoding="utf-8")
    out = skill.read_text(encoding="utf-8")
    lines = out.count("\n")
    sha = hashlib.sha256(out.encode()).hexdigest()
    verdict = "MATCH" if (lines == PIN_SKILL_LINES and sha == PIN_SKILL_SHA) else "MISMATCH"
    print("skill_lines=%d skill_sha256=%s identity_claim=%s" % (lines, sha, verdict))
    return 0 if verdict == "MATCH" else 5


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
