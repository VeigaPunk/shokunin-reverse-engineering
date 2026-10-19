#!/usr/bin/env python3
"""EX-33 self-pin audit — independent re-derivation of a receipt's embedded tool sha.

Independent means: this script hashes the tool file itself (hashlib, its own code
path) and extracts the receipt's `# tool:` pin with its own regex; it never
imports custody-pair.py and never trusts the tool's own self-report.

Usage:
  selfpin-audit.py --tool <tool.py> --receipt <receipt> [--expect-not <sha>]
                   [--expect <sha>] [--label <tag>]

Checks (each prints PASS/FAIL):
  C1 pin-present          the receipt carries a `# tool: <name>  sha256 <hex>` line
  C2 pin==tool-bytes      pin equals sha256(current tool file)   [independent hash]
  C3 pin!=old             pin differs from the superseded 112d01dc…   (only with --expect-not)
  C4 pin==expect          pin equals --expect                        (only with --expect)
  C5 tool-stable          tool file sha unchanged across this audit
  C6 sidecar-matches      receipt.sha256 sidecar (if present) matches receipt bytes
Exit 0 iff every performed check passed.
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

PIN_RE = re.compile(r"^# tool: (\S+)\s+sha256 ([0-9a-fA-F]{64})\s*$", re.M)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--expect-not", default=None)
    ap.add_argument("--expect", default=None)
    ap.add_argument("--label", default="")
    a = ap.parse_args()

    tool = Path(a.tool)
    receipt = Path(a.receipt)
    rows = []

    tool_sha_pre = sha256_file(tool)
    text = receipt.read_text(encoding="utf-8", errors="replace")
    m = PIN_RE.search(text)

    rows.append(("C1 pin-present", bool(m), m.group(2) if m else "no `# tool:` pin line found"))
    if m:
        pin_name, pin = m.group(1), m.group(2).lower()
        rows.append(("C2 pin==tool-bytes", pin == tool_sha_pre,
                     "pin=%s tool=%s" % (pin, tool_sha_pre)))
        if a.expect_not:
            rows.append(("C3 pin!=old", pin != a.expect_not.lower(),
                         "pin=%s forbidden=%s" % (pin, a.expect_not.lower())))
        if a.expect:
            rows.append(("C4 pin==expect", pin == a.expect.lower(),
                         "pin=%s expect=%s" % (pin, a.expect.lower())))
        name_ok = pin_name == tool.name
        rows.append(("C5 pin-name==tool-basename", name_ok,
                     "pin-name=%s tool-name=%s" % (pin_name, tool.name)))

    sidecar = receipt.with_name(receipt.name + ".sha256")
    if sidecar.exists():
        want = sidecar.read_text().split()[0].lower()
        got = sha256_file(receipt)
        rows.append(("C6 sidecar-matches", want == got, "sidecar=%s receipt=%s" % (want, got)))
    else:
        rows.append(("C6 sidecar-matches", False, "no sidecar at %s" % sidecar))

    tool_sha_post = sha256_file(tool)
    rows.append(("C7 tool-stable-during-audit", tool_sha_pre == tool_sha_post,
                 "pre=%s post=%s" % (tool_sha_pre, tool_sha_post)))

    print("SELFPIN-AUDIT %s tool=%s receipt=%s" % (a.label or "(unlabeled)", tool, receipt))
    ok_all = True
    for name, ok, detail in rows:
        ok_all &= ok
        print("  %-32s %s  %s" % (name, "PASS" if ok else "FAIL", detail))
    print("SELFPIN-AUDIT-RESULT: %s checks=%d failed=%d" %
          ("PASS" if ok_all else "FAIL", len(rows), sum(1 for _, ok, _ in rows if not ok)))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())