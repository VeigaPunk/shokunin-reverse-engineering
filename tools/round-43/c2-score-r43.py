#!/usr/bin/env python3
"""Score P43-C2 in a clean shared clone at one committed revision.

Runs the frozen local-source gate and the hardened content/provenance verifier,
then binds the registry delta, map digest, S126 preservation, and worktree
cleanliness into one receipt. All scratch and clone state must be supplied under
HYAKU_SCRATCH; the tool never uses /tmp deliberately and never mutates the lane.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

BASE_DEFAULT = "6b9e64fe7e0de202d9383baad5792fbfe039a743"
MAP = "corpus/evidence/local-sources.json"
SOURCES = "corpus/SOURCES.md"
S126 = "/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv"
MAP_SHA256 = "3158cdc982fc07d263198ab0eaeee2adb9ca9d8cf4ebb662ea640c1c0491148e"
EXPECTED_LINT_CHECKS = 136


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(argv: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    return run(["git", "--no-optional-locks", "-C", root, *args])


def blob(root: str, rev: str, path: str) -> bytes | None:
    proc = git(root, "show", "%s:%s" % (rev, path))
    return proc.stdout if proc.returncode == 0 else None


def receipt_wrapped(clone: str, rev: str, wrapper: str, tool: str,
                    command: list[str], out: str) -> tuple[int, dict]:
    argv = [sys.executable, "-I", "-B", wrapper, "--out", out,
            "--git-root", clone, "--rev", rev, "--tool", tool, "--"] + command
    proc = run(argv, cwd=clone)
    try:
        doc = json.loads(Path(out).read_text(encoding="utf-8"))
    except Exception as exc:
        return 2, {"wrapper_exit": proc.returncode,
                   "error": "receipt-unreadable: %s" % exc,
                   "stderr": proc.stderr.decode("utf-8", "replace")}
    return proc.returncode, doc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True, help="source lane repository")
    ap.add_argument("--rev", required=True, help="measured revision")
    ap.add_argument("--freeze", required=True, help="round freeze revision")
    ap.add_argument("--base", default=BASE_DEFAULT, help="round start revision")
    ap.add_argument("--scratch", required=True, help="dedicated scratch directory")
    ap.add_argument("--upstream-dir", required=True,
                    help="contains extracted go1.25.0/ and go1.24.6/ ABI trees")
    ap.add_argument("--tarball-67", required=True, help="pinned rea-agents-6.7.0.tgz")
    ap.add_argument("--tarball-65", required=True, help="pinned rea-agents-6.5.0.tgz")
    ap.add_argument("--json-out", required=True, help="committed result receipt")
    a = ap.parse_args(argv)

    root = os.path.abspath(a.root)
    scratch = os.path.abspath(a.scratch)
    os.makedirs(scratch, exist_ok=True)
    receipt: dict = {
        "schema": "kaidoku-c2-score-r43-v1",
        "argv": sys.argv,
        "root": root,
        "revision_arg": a.rev,
        "freeze_arg": a.freeze,
        "base_arg": a.base,
        "scratch": scratch,
        "clone_clean": False,
        "checks": {},
    }
    here = os.path.abspath(__file__)
    tool_rel = os.path.relpath(here, root)
    tool_bytes = Path(here).read_bytes()
    at_freeze = blob(root, a.freeze, tool_rel)
    at_rev = blob(root, a.rev, tool_rel)
    receipt["score_tool"] = {
        "path": tool_rel,
        "sha256": sha256(tool_bytes),
        "sha256_at_freeze": sha256(at_freeze) if at_freeze is not None else None,
        "sha256_at_rev": sha256(at_rev) if at_rev is not None else None,
        "frozen": bool(at_freeze and at_rev and tool_bytes == at_freeze == at_rev),
    }

    clone = os.path.join(scratch, "clone")
    if os.path.exists(clone):
        shutil.rmtree(clone)
    proc = run(["git", "clone", "-q", "--shared", root, clone])
    receipt["clone"] = {"exit": proc.returncode,
                        "stderr": proc.stderr.decode("utf-8", "replace")}
    if proc.returncode:
        receipt["exit_code"] = 2
        Path(a.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json_out).write_text(json.dumps(receipt, indent=2) + "\n")
        return 2
    checkout = git(clone, "checkout", "--quiet", "--detach", a.rev)
    status = git(clone, "status", "--porcelain")
    receipt["clone_clean"] = checkout.returncode == 0 and not status.stdout
    receipt["clone_status"] = status.stdout.decode("utf-8", "replace")
    receipt["revision"] = git(clone, "rev-parse", "HEAD").stdout.decode().strip()
    receipt["freeze_is_ancestor"] = git(clone, "merge-base", "--is-ancestor",
                                        a.freeze, a.rev).returncode == 0

    # The gate itself reads the map/copies from the clean worktree and SOURCES
    # from --rev. The receipt wrapper binds exact argv, tool bytes, and result.
    gate_path = "tools/round-41/local-source-gate.py"
    wrapper_path = "tools/round-43/receipt-wrap.py"
    gate_out = os.path.join(scratch, "gate-receipt.json")
    gate_argv = [sys.executable, "-I", "-B", gate_path, "--root", clone,
                 "--rev", a.rev, "--json"]
    gate_exit, gate_receipt = receipt_wrapped(
        clone, a.rev, wrapper_path, gate_path, gate_argv, gate_out)
    receipt["gate_receipt_path"] = gate_out
    receipt["gate_receipt_sha256"] = sha256(Path(gate_out).read_bytes()) if os.path.isfile(gate_out) else None
    receipt["gate"] = gate_receipt
    gate_doc = None
    try:
        gate_doc = json.loads(gate_receipt.get("stdout_text", ""))
    except Exception:
        pass
    receipt["gate_exit"] = gate_receipt.get("exit_code", gate_exit)
    receipt["rows_total"] = gate_doc.get("rows_total") if isinstance(gate_doc, dict) else None
    receipt["rows_checked"] = gate_doc.get("rows_checked") if isinstance(gate_doc, dict) else None
    receipt["rows_failed"] = gate_doc.get("rows_failed") if isinstance(gate_doc, dict) else None

    # The hardened verifier binds copy identity to row anchors, rejects
    # symlinks/aliases/duplicate map keys, and re-derives absent-host entries
    # from the pinned upstream substrates.
    lint_path = "tools/round-43/verify-copies-r43.py"
    lint_out = os.path.join(scratch, "copy-audit-receipt.json")
    lint_argv = [sys.executable, "-I", "-B", lint_path, "--root", clone,
                 "--rev", a.rev, "--freeze", a.freeze,
                 "--upstream-dir", os.path.abspath(a.upstream_dir),
                 "--tarball", os.path.abspath(a.tarball_67),
                 "--tarball-650", os.path.abspath(a.tarball_65)]
    lint_exit, lint_receipt = receipt_wrapped(
        clone, a.rev, wrapper_path, lint_path, lint_argv, lint_out)
    receipt["copy_audit_receipt_path"] = lint_out
    receipt["copy_audit_receipt_sha256"] = sha256(Path(lint_out).read_bytes()) if os.path.isfile(lint_out) else None
    receipt["copy_audit"] = lint_receipt
    lint_text = lint_receipt.get("stdout_text", "")
    match = re.search(r"checks:\s*(\d+),\s*failures:\s*(\d+)", lint_text)
    receipt["copy_audit_checks"] = int(match.group(1)) if match else None
    receipt["copy_audit_failures"] = int(match.group(2)) if match else None
    receipt["copy_audit_exit"] = lint_receipt.get("exit_code", lint_exit)

    # Registry and map bindings are independent of the worktree gate output.
    base_sources = blob(root, a.base, SOURCES)
    rev_sources = blob(root, a.rev, SOURCES)
    map_bytes = blob(root, a.rev, MAP)
    receipt["sources_sha256_at_rev"] = sha256(rev_sources) if rev_sources is not None else None
    receipt["map_sha256_at_rev"] = sha256(map_bytes) if map_bytes is not None else None
    diff = git(root, "diff", "--numstat", "%s..%s" % (a.base, a.rev), "--", SOURCES)
    receipt["sources_numstat"] = diff.stdout.decode("utf-8", "replace").strip()
    try:
        base_map = json.loads(blob(root, a.base, MAP).decode("utf-8"))
        rev_map = json.loads(map_bytes.decode("utf-8"))
        base_s126 = base_map["sources"][S126]
        rev_s126 = rev_map["sources"][S126]
        receipt["s126_preserved"] = base_s126 == rev_s126
    except Exception as exc:
        receipt["s126_preserved"] = False
        receipt["s126_error"] = repr(exc)

    checks = {
        "score_tool_frozen": receipt["score_tool"]["frozen"],
        "clone_at_rev_clean": receipt["clone_clean"],
        "freeze_ancestor": receipt["freeze_is_ancestor"],
        "gate_exit_zero": receipt["gate_exit"] == 0,
        "rows_total_137": receipt["rows_total"] == 137,
        "rows_checked_19": receipt["rows_checked"] == 19,
        "rows_failed_empty": receipt["rows_failed"] == [],
        "copy_audit_exit_zero": receipt["copy_audit_exit"] == 0,
        "copy_audit_136_checks": receipt["copy_audit_checks"] == EXPECTED_LINT_CHECKS,
        "copy_audit_no_failures": receipt["copy_audit_failures"] == 0,
        "map_digest_pinned": receipt["map_sha256_at_rev"] == MAP_SHA256,
        "sources_numstat_three_additions": receipt["sources_numstat"] == "3\t0\tcorpus/SOURCES.md",
        "s126_preserved": receipt["s126_preserved"],
    }
    receipt["checks"] = checks
    receipt["checks_ok"] = all(checks.values())
    receipt["exit_code"] = 0 if receipt["checks_ok"] else 1
    Path(a.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.json_out).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8")
    print(json.dumps({"checks": checks, "exit_code": receipt["exit_code"]}, sort_keys=True))
    return receipt["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
