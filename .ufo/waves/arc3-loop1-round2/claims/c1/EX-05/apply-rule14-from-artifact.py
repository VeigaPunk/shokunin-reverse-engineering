#!/usr/bin/env python3
"""EX-05 (c1, round 2): apply EX-01's rule-#14 patch from the artifact.

Implements EX-01's anchor recipe (claims/c1/EX-01/rule14.patch.md §2): extract
the payload strictly between the payload-begin/payload-end markers, verify its
identity (896 B, sha256 a47dc38d...), then insert it plus one blank line
immediately after the SKILL.md line carrying

  kernel-OOM-killed (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37`).

and verify the resulting file identity (385 lines, sha256 19057c13...).

Usage: python3 apply-rule14-from-artifact.py <patch.md> <root>
"""
import hashlib
import pathlib
import re
import sys

B, E = "<!-- payload-begin -->", "<!-- payload-end -->"
PAY_SHA = "a47dc38d1e12856bb34b3f1310af7109d65c649f8eef17a5feb3c00781623b80"
SKILL_SHA = "19057c131038352ba1bee1aec007401de774cc88a9ef42cde2cc09dcbe6f4e90"
ANCHOR = re.compile(
    r"^\s*kernel-OOM-killed \(`corpus/knowledge/"
    r"2026-10-18-arc2-r7-pe-wall\.md:23-37`\)\.\s*$")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main(patchf, root, exp_payload=None, exp_skill=None):
    text = pathlib.Path(patchf).read_text(encoding="utf-8")
    body = text.split(B, 1)[1].split(E, 1)[0]
    payload = (body.strip("\n") + "\n").encode()
    print("payload_bytes=%d payload_sha256=%s" % (len(payload), sha(payload)))
    if exp_payload:
        assert sha(payload) == exp_payload, "payload identity mismatch"
    skill = pathlib.Path(root) / "SKILL.md"
    lines = skill.read_text(encoding="utf-8").splitlines(keepends=True)
    idx = [i for i, ln in enumerate(lines) if ANCHOR.match(ln.rstrip("\n"))]
    print("anchor_hits=%d anchor_line=%s" % (len(idx), [i + 1 for i in idx]))
    assert len(idx) == 1, "anchor not unique"
    at = idx[0] + 1
    new = lines[:at] + [payload.decode(), "\n"] + lines[at:]
    out = "".join(new).encode()
    skill.write_bytes(out)
    print("skill_lines=%d skill_sha256=%s" % (out.decode().count("\n"), sha(out)))
    if exp_skill:
        assert sha(out) == exp_skill, "patched SKILL.md identity mismatch"
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
