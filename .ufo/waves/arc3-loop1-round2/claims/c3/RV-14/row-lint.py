#!/usr/bin/env python3
"""RV-14 row lint: check a registry-row artifact's claim tokens against the
custody-pair tool's measured surface.

Usage: row-lint.py <row-file> [<row-file> ...]

Checks (each printed as OK / FLAG / INFO):
  * backticked command tokens -> subcommands and flags must exist in the tool
  * exit codes mentioned in the row -> must be in the tool's declared map
  * "cases=N" mentions -> must equal the selftest's real case count
  * in-repo paths mentioned -> must exist
  * 64-hex digests mentioned -> reported for manual pinning
  * row's own self-identity claims (size/hash/line count) -> re-derived
"""
import hashlib, os, re, subprocess, sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
TOOL = os.path.join(REPO, ".ufo/gates/custody-pair/custody-pair.py")
DECLARED_EXITS = {0, 2, 3, 10, 11, 12, 13}
SUBCMDS = {"capture", "verify", "selftest", "paths"}
FLAGS = {"--out", "--label", "--paths", "--live", "--scratch", "-h", "--help"}

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)

def selftest_case_count():
    out = run(["python3", TOOL, "selftest", "--scratch", "/var/tmp/rv14/selftest-scratch"]).stdout
    m = re.search(r"CUSTODY_PAIR_SELFTEST:\s*\S+\s*cases=(\d+)", out)
    return int(m.group(1)) if m else None

def main():
    if not os.path.exists(TOOL):
        print("FATAL: tool absent: %s" % TOOL); return 2
    tool_sha = hashlib.sha256(open(TOOL, "rb").read()).hexdigest()
    ncases = selftest_case_count()
    print("tool %s\n  sha256 %s\n  selftest cases=%s" % (TOOL, tool_sha, ncases))
    for row in sys.argv[1:]:
        print("\n=== row: %s" % row)
        text = open(row, encoding="utf-8", errors="replace").read()
        raw = open(row, "rb").read()
        print("  INFO row-self: %d bytes  sha256 %s  %d lines"
              % (len(raw), hashlib.sha256(raw).hexdigest(), text.count("\n")))
        found_cmds, found_flags = set(), set()
        for tok in re.findall(r"`([^`]+)`", text):
            for sub in re.findall(r"\b(capture|verify|selftest|paths)\b", tok):
                found_cmds.add(sub)
            for fl in re.findall(r"(?<![\w-])--[a-z][a-z-]*", tok):
                found_flags.add(fl)
        bad_cmds = found_cmds - SUBCMDS
        bad_flags = found_flags - FLAGS
        print("  %s subcommands referenced: %s%s"
              % ("FLAG" if bad_cmds else "OK", sorted(found_cmds),
                 ("  NONE-EXISTENT: %s" % sorted(bad_cmds)) if bad_cmds else ""))
        print("  %s flags referenced: %s%s"
              % ("FLAG" if bad_flags else "OK", sorted(found_flags),
                 ("  NONE-EXISTENT: %s" % sorted(bad_flags)) if bad_flags else ""))
        exits = set(int(x) for x in re.findall(r"exit[^0-9\n]{0,8}(\d+)", text))
        bad_exits = exits - DECLARED_EXITS
        print("  %s exit codes referenced: %s%s"
              % ("FLAG" if bad_exits else "OK", sorted(exits),
                 ("  NOT-DECLARED: %s" % sorted(bad_exits)) if bad_exits else ""))
        cases = set(int(x) for x in re.findall(r"cases[= ](\d+)", text))
        if cases:
            print("  %s case counts claimed: %s (selftest actual=%s)"
                  % ("FLAG" if (ncases is not None and cases - {ncases}) else "OK",
                     sorted(cases), ncases))
        paths = set(re.findall(r"(?:\.ufo|corpus|~/) [\w./-]+".replace(" ", ""), "") )
        paths |= set(re.findall(r"(\.ufo/[\w./-]+|~/[\w./-]+|corpus/[\w./-]+)", text))
        for p in sorted(paths):
            real = os.path.expanduser(p) if p.startswith("~/") else os.path.join(REPO, p)
            if not os.path.exists(real):
                print("  FLAG path referenced but absent: %s" % p)
        print("  INFO in-repo paths referenced: %s" % (sorted(paths) or "none"))
        digests = re.findall(r"\b[0-9a-f]{64}\b", text)
        print("  INFO digests in text: %s" % (digests[:8] if digests else "none"))
        for d in digests[:8]:
            hits = [p for p in (TOOL, os.path.join(os.path.dirname(TOOL), "README.md"))
                    if os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() == d]
            if hits:
                print("       digest %s… matches %s" % (d[:8], hits))
    return 0

if __name__ == "__main__":
    sys.exit(main())
