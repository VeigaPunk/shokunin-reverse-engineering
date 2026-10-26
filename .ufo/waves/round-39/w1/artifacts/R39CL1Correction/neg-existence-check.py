#!/usr/bin/env python3
"""QUALITY-82 gate: a negative existence claim must root its sweep at the base
its cited relative path is relative to, must not dress a subtree sweep as a
host-wide claim, and the negative must still hold when the sweep is re-run.

Claim record (JSONL, one per line):
  id            stable identifier
  claim_text    the sentence that makes the negative claim
  find_root     root handed to `find` for the claim
  find_name     -name operand of that `find`
  staged_path   the relative path the claim is about
  base          key into bases.json naming the root that path is relative to

Verdict per claim: ok | host-claim-subtree-root | misrooted | negative-refuted.
Exit 0 iff every claim is ok. Exit 2 on unreadable input.
"""
import json
import os
import subprocess
import sys

HOST_PATTERNS = ("on this host", "on the host", "anywhere on this host")
HOST_ROOTS = ("/",)


def load_bases(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def is_within(root, base):
    root, base = os.path.realpath(root), os.path.realpath(base)
    return base == root or base.startswith(root.rstrip("/") + "/")


def main(argv):
    if len(argv) != 3:
        print("usage: neg-existence-check.py CLAIMS.jsonl BASES.json", file=sys.stderr)
        return 2
    claims_path, bases_path = argv[1], argv[2]
    bases = load_bases(bases_path)
    rows, failed = [], 0
    with open(claims_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            c = json.loads(line)
            reasons = []
            text = c["claim_text"].lower()
            root = c["find_root"]
            base = bases[c["base"]]
            if any(p in text for p in HOST_PATTERNS):
                if os.path.realpath(root) not in {os.path.realpath(h) for h in HOST_ROOTS}:
                    reasons.append("host-claim-subtree-root")
            if not is_within(root, base):
                reasons.append("misrooted")
            found = ""
            if os.path.isdir(root):
                proc = subprocess.run(
                    ["find", root, "-name", c["find_name"], "-print"],
                    capture_output=True, text=True, timeout=120,
                )
                found = proc.stdout.strip()
            if found:
                reasons.append("negative-refuted")
            verdict = "ok" if not reasons else "+".join(reasons)
            if reasons:
                failed += 1
            rows.append({
                "id": c["id"], "verdict": verdict, "find_root": root,
                "base": base, "staged_path": c["staged_path"],
                "found": found.splitlines(),
            })
    print(json.dumps({"claims": rows, "failed": failed}, indent=2))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
