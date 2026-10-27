#!/usr/bin/env python3
"""receipt-wrap — write a QUALITY-18/21-shaped receipt around one tool run.

Round 43 wave 1, seat R43SentProv.  Stdlib only; no timestamp of its own
(QUALITY 23: a receipt that stamps 'now' risks landing a line later than the
commit that introduces it; the commit's %cI is the admissible instant).

What it retains, and why:

  tool_path / tool_sha256        the bytes that actually ran
  argv                           the exact argv, as executed (QUALITY 18)
  cwd                            the directory the argv was valid in
  revision_arg / revision        the revision given, and the full hash it
                                 resolves to at run time (`--rev` is otherwise
                                 only an echoed label — round-34 note)
  tool_digest_at_rev             sha256 of `<revision>:<tool_path>` from Git
                                 objects: the measured tool equals the one run
  exit_code                      the tool's exit, propagated as this wrapper's
  stdout_sha256 / stdout_bytes / stdout_text
  stderr_sha256 / stderr_bytes / stderr_text

QUALITY 21: the embedded stdout is the tool's own JSON, so the keys the tool
recomputes are in the receipt as values.  A verdict word (`resolved`, `ok`) in
that JSON is not the compared object; cite the recorded digests and lists.

Usage:
  receipt-wrap.py --out <receipt.json> --git-root <lane> --rev <REV>
                  --tool <path> -- <cmd> [args...]

`<cmd>` should be the tool under `--git-root` (pass a path relative to it, with
`--root .`), so the receipt re-runs unchanged from the lane root.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shlex
import subprocess
import sys

CAP = 64 * 1024


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "--no-optional-locks", "-C", root, *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--git-root", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--tool", required=True)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    args = ap.parse_args()

    cmd = args.cmd
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        ap.error("no command after --")

    root = os.path.abspath(args.git_root)
    tool_abs = args.tool if os.path.isabs(args.tool) else os.path.join(root, args.tool)
    try:
        with open(tool_abs, "rb") as fh:
            tool_bytes = fh.read()
    except OSError as exc:
        print("receipt-wrap: cannot read --tool: %s" % exc, file=sys.stderr)
        return 2

    resolved = git(root, "rev-parse", "--verify", args.rev + "^{commit}")
    revision = resolved.stdout.decode().strip() if resolved.returncode == 0 else None
    tool_at_rev = None
    if revision:
        tool_rel = os.path.relpath(tool_abs, root)
        blob = git(root, "cat-file", "blob", "%s:%s" % (revision, tool_rel))
        if blob.returncode == 0:
            tool_at_rev = sha256_bytes(blob.stdout)

    proc = subprocess.run(cmd, cwd=root, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)

    receipt = {
        "schema": "receipt-wrap-v1",
        "tool_path": os.path.relpath(tool_abs, root),
        "tool_sha256": sha256_bytes(tool_bytes),
        "tool_digest_at_rev": tool_at_rev,
        "argv": cmd,
        "argv_shell": shlex.join(cmd),
        "cwd": ".",
        "git_root": root,
        "revision_arg": args.rev,
        "revision": revision,
        "revision_is_ancestor_of_head": (
            git(root, "merge-base", "--is-ancestor", revision, "HEAD").returncode == 0
            if revision else None),
        "exit_code": proc.returncode,
        "stdout_sha256": sha256_bytes(proc.stdout),
        "stdout_bytes": len(proc.stdout),
        "stdout_text": proc.stdout[:CAP].decode("utf-8", "replace"),
        "stdout_truncated": len(proc.stdout) > CAP,
        "stderr_sha256": sha256_bytes(proc.stderr),
        "stderr_bytes": len(proc.stderr),
        "stderr_text": proc.stderr[:CAP].decode("utf-8", "replace"),
        "interpreter": {"python": platform.python_version(), "machine": platform.machine()},
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True)
        fh.write("\n")
    sys.stdout.write(proc.stdout.decode("utf-8", "replace"))
    sys.stderr.write(proc.stderr.decode("utf-8", "replace"))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
