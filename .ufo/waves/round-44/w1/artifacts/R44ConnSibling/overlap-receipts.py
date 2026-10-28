#!/usr/bin/env python3
"""R44ConnSibling read-only overlap receipts.

Runs fixed read-only checks against the kaidoku lane and fleet siblings and
writes one JSON line per check: seat, command, exit code, stdout sha256,
stdout line count, wall time. Never writes outside the output file.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

SEAT = "R44ConnSibling"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
BASE = "c29360e3ba5381a5ab69e372d0d9577970f85018"
OUT = os.path.join(LANE, ".ufo/waves/round-44/w1", SEAT, "receipts.jsonl")

SIBLING_DOCS = [
    "revenger-shokunin/PROVINCE.md",
    "revenger-shokunin/SCORECARD.md",
    "revenger-shokunin/SKILL.md",
    "game-dev-3d-shokunin/SCORECARD.md",
    "game-dev-3d-shokunin/SKILL.md",
    "kengaku-shokunin/PROVINCE.md",
    "kumitate-shokunin/PROVINCE.md",
    "tsukuroi-shokunin/PROVINCE.md",
]

FROZEN_C2 = ["SCORECARD.md", "SHONEN.md", "corpus/README.md"]
FROZEN_C1 = [
    "PROVINCE.md",
    "corpus/SOURCES.md",
    "tools/round-42/fixtures.json",
    "tools/round-42/c1-counter.py",
    "tools/round-39/gen-squashfs.py",
    "corpus/evidence/round-42/c2/fixtures",
]

CHECKS = [
    ("sibling-squashfs-hits",
     ["grep", "-n", "-i", "-E", "squashfs|unblob|sasquatch|extract-firmware"] + [os.path.join(FLEET, p) for p in SIBLING_DOCS]),
    ("sibling-extract-firmware-verb",
     ["grep", "-rn", "-i", "extract-firmware", os.path.join(FLEET, "revenger-shokunin/PROVINCE.md"), os.path.join(FLEET, "revenger-shokunin/SKILL.md")]),
    ("kaidoku-contested-rule",
     ["grep", "-n", "-i", "contested", os.path.join(LANE, "PROVINCE.md")]),
    ("kaidoku-revenger-arbitration",
     ["grep", "-n", "-i", "-E", "arbitration|revenger", os.path.join(LANE, "PROVINCE.md")]),
    ("c2-surface-sibling-path-refs",
     ["grep", "-n", "-o", "-E", r"(\.\./|[a-z-]+-shokunin/)[A-Za-z0-9_./-]*"] + [os.path.join(LANE, p) for p in FROZEN_C2]),
    ("c1-surface-exists",
     ["bash", "-c", "cd '%s' && ls -l %s" % (LANE, " ".join(FROZEN_C1))]),
    ("c2-surface-exists",
     ["bash", "-c", "cd '%s' && ls -l %s" % (LANE, " ".join(FROZEN_C2))]),
    ("base-is-ancestor-of-head",
     ["git", "-C", LANE, "merge-base", "--is-ancestor", BASE, "HEAD"]),
    ("frozen-surface-changes-base-to-head",
     ["git", "-C", LANE, "diff", "--name-only", BASE, "HEAD", "--", "PROVINCE.md", "SCORECARD.md", "SHONEN.md", "corpus/README.md", "corpus/SOURCES.md", "tools/round-42", "tools/round-39/gen-squashfs.py", "corpus/evidence/round-42/c2/fixtures"]),
    ("oracle-package-owner",
     ["bash", "-c", "pacman -Q squashfs-tools; pacman -Qo /usr/bin/unsquashfs"]),
    ("oracle-binary-version",
     ["bash", "-c", "/usr/bin/unsquashfs -v | head -1"]),
]


def run(name, argv):
    t0 = time.time()
    proc = subprocess.run(argv, capture_output=True, text=True, cwd=FLEET)
    wall = time.time() - t0
    stdout = proc.stdout
    return {
        "seat": SEAT,
        "check": name,
        "command": " ".join(argv),
        "exit_code": proc.returncode,
        "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
        "stdout_lines": stdout.count("\n"),
        "stderr_first_line": (proc.stderr.splitlines() or [""])[0][:200],
        "wall_seconds": round(wall, 4),
        "stdout_head": stdout.splitlines()[:40],
    }


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        for name, argv in CHECKS:
            rec = run(name, argv)
            fh.write(json.dumps(rec) + "\n")
            print(name, rec["exit_code"], rec["stdout_lines"], rec["wall_seconds"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
