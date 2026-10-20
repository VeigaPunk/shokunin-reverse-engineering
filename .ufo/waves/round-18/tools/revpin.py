#!/usr/bin/env python3
"""revpin.py — jj-safe revision-pin resolution for colocated lanes (R18 C2).

Contract: .ufo/waves/round-18/contract.md, section "W18/tools/revpin.py".

A jj-colocated lane leaves git HEAD detached on the working-copy commit, so
a lane tool that pins "the revision under test" must never read bare HEAD:
it pins the branch tip (refs/heads/<branch>) and only *validates* HEAD and
the remote-tracking ref against it. This module is the single place that
performs those three resolutions plus the requirement checks.

resolve_source(lane, branch="main", require_pushed=True, require_head=True)
returns:

    {
      "branch":            <branch name>,
      "source":            <sha of refs/heads/<branch>^{commit}>,
      "head":              <sha of HEAD^{commit}> or null,
      "head_equals_source": <bool>,
      "remote":            <sha of refs/remotes/origin/<branch>^{commit}>
                           or null when the remote-tracking ref is absent,
      "pushed":            <bool — source is an ancestor of remote>,
    }

and raises RevPinError with a named finding when a required condition
fails: "branch_missing" (the branch ref does not resolve), or — when the
corresponding require_* flag is set — "head_not_branch_tip" or
"branch_not_pushed". The error carries .finding and .result (the
best-effort dict above) so callers can still emit the observation.

All git access is read-only (rev-parse, merge-base); this module never
runs jj and never writes the lane. Pushed means "every commit on
refs/heads/<branch> is contained in refs/remotes/origin/<branch>"
(merge-base --is-ancestor), which covers ahead, behind and diverged —
a strict equality check would mislabel a merely stale-but-pushed tip.

CLI:
    revpin.py --root DIR [--branch main] [--no-require-pushed]
              [--no-require-head] [--selftest]

Prints the dict as JSON (sort_keys=True, indent=2). Exit 0 ok, exit 2 on a
named finding (the JSON then carries "finding" plus the best-effort
result). --selftest builds fixture repos under tempfile.mkdtemp() —
outside the lane — and exercises every finding.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

FINDINGS = ("branch_missing", "head_not_branch_tip", "branch_not_pushed")


class RevPinError(RuntimeError):
    """A named pin-requirement failure carrying the best-effort result."""

    def __init__(self, finding: str, result: dict):
        super().__init__(finding)
        if finding not in FINDINGS:
            raise ValueError(f"unknown revpin finding: {finding}")
        self.finding = finding
        self.result = result


def _git(root: str, *args: str) -> subprocess.CompletedProcess:
    """Run one read-only git command in root; never raises on nonzero."""
    return subprocess.run(
        ["git", "-C", root, *args],
        capture_output=True, text=True, check=False,
    )


def _resolve(root: str, rev: str):
    """rev-parse --verify <rev> -> sha string, or None when unresolvable."""
    r = _git(root, "rev-parse", "--verify", "--quiet", rev)
    if r.returncode != 0:
        return None
    return r.stdout.strip().splitlines()[0] if r.stdout.strip() else None


def _is_ancestor(root: str, older: str, newer: str) -> bool:
    """True iff `older` is an ancestor of (or equal to) `newer`."""
    r = _git(root, "merge-base", "--is-ancestor", older, newer)
    return r.returncode == 0


def resolve_source(lane: str, branch: str = "main",
                   require_pushed: bool = True,
                   require_head: bool = True) -> dict:
    """Resolve the lane's pin source (branch tip) plus HEAD/remote checks."""
    lane = os.path.abspath(lane)
    source = _resolve(lane, f"refs/heads/{branch}^{{commit}}")
    if source is None:
        raise RevPinError("branch_missing", {
            "branch": branch,
            "source": None,
            "head": None,
            "head_equals_source": False,
            "remote": None,
            "pushed": False,
        })
    head = _resolve(lane, "HEAD^{commit}")
    remote = _resolve(lane, f"refs/remotes/origin/{branch}^{{commit}}")
    result = {
        "branch": branch,
        "source": source,
        "head": head,
        "head_equals_source": head == source,
        "remote": remote,
        "pushed": remote is not None and _is_ancestor(lane, source, remote),
    }
    if require_head and not result["head_equals_source"]:
        raise RevPinError("head_not_branch_tip", result)
    if require_pushed and not result["pushed"]:
        raise RevPinError("branch_not_pushed", result)
    return result


def _emit(obj) -> None:
    json.dump(obj, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")


def _selftest() -> int:
    """Build fixture repos under mkdtemp; every fixture is outside LANE."""
    here = os.path.abspath(__file__)
    failures = []
    cases = 0

    def check(ok: bool, label: str, detail: str) -> None:
        if not ok:
            failures.append(f"{label}: {detail}")

    def git(cwd: str, *args: str, want: int = 0) -> subprocess.CompletedProcess:
        r = subprocess.run(["git", "-C", cwd, *args],
                           capture_output=True, text=True, check=False)
        if want is not None and r.returncode != want:
            raise RuntimeError(
                f"git {' '.join(args)} -> {r.returncode}: {r.stderr.strip()}")
        return r

    def commit_file(cwd: str, name: str, text: str, msg: str) -> None:
        with open(os.path.join(cwd, name), "w", encoding="utf-8") as fh:
            fh.write(text)
        git(cwd, "add", name)
        git(cwd, "-c", "user.email=selftest@revpin",
            "-c", "user.name=revpin-selftest", "commit", "-q", "-m", msg)

    def run_cli(*argv: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-I", "-B", here, *argv],
            capture_output=True, text=True, check=False,
        )

    root = os.path.realpath(tempfile.mkdtemp(prefix="revpin-selftest-"))
    try:
        remote = os.path.join(root, "remote.git")
        work = os.path.join(root, "work")
        plain = os.path.join(root, "plain")
        os.makedirs(plain)
        git(root, "-c", "init.defaultBranch=main", "init", "-q",
            "--bare", remote)
        git(root, "-c", "init.defaultBranch=main", "init", "-q", work)
        git(work, "remote", "add", "origin", remote)
        commit_file(work, "a.txt", "one\n", "first")
        git(work, "push", "-q", "-u", "origin", "main")

        # C1 — clean fixture: tip == HEAD == origin/main -> green.
        cases += 1
        res = resolve_source(work)
        tip = git(work, "rev-parse", "refs/heads/main").stdout.strip()
        check(res["source"] == tip == res["head"] == res["remote"]
              and res["head_equals_source"] is True
              and res["pushed"] is True and res["branch"] == "main",
              "clean-api", f"got {res}")
        cases += 1
        r = run_cli("--root", work)
        doc = json.loads(r.stdout) if r.stdout.strip() else {}
        check(r.returncode == 0 and doc.get("pushed") is True,
              "clean-cli", f"rc={r.returncode} out={r.stdout!r}")

        # C2 — tip ahead of origin: red for the named reason
        # branch_not_pushed (HEAD still equals the tip).
        cases += 1
        commit_file(work, "a.txt", "two\n", "unpushed")
        try:
            resolve_source(work)
            check(False, "unpushed-api", "expected RevPinError")
        except RevPinError as e:
            check(e.finding == "branch_not_pushed"
                  and e.result["head_equals_source"] is True
                  and e.result["pushed"] is False,
                  "unpushed-api", f"finding={e.finding} result={e.result}")
        cases += 1
        r = run_cli("--root", work)
        doc = json.loads(r.stdout) if r.stdout.strip() else {}
        check(r.returncode == 2 and doc.get("finding") == "branch_not_pushed",
              "unpushed-cli", f"rc={r.returncode} out={r.stdout!r}")
        cases += 1
        r = run_cli("--root", work, "--no-require-pushed")
        check(r.returncode == 0 and
              json.loads(r.stdout).get("pushed") is False,
              "unpushed-waived-cli", f"rc={r.returncode} out={r.stdout!r}")

        # C3 — detached off-branch HEAD (the jj working-copy shape): red
        # for head_not_branch_tip. Restore tip == origin first so the
        # head finding, not pushed, is what fires.
        cases += 1
        pushed_sha = git(work, "rev-parse",
                         "refs/remotes/origin/main").stdout.strip()
        git(work, "update-ref", "refs/heads/main", pushed_sha)
        git(work, "checkout", "-q", "--detach", "HEAD")
        commit_file(work, "b.txt", "off\n", "off-branch")
        try:
            resolve_source(work)
            check(False, "offbranch-api", "expected RevPinError")
        except RevPinError as e:
            check(e.finding == "head_not_branch_tip"
                  and e.result["source"] == pushed_sha
                  and e.result["head"] != pushed_sha,
                  "offbranch-api", f"finding={e.finding} result={e.result}")
        cases += 1
        r = run_cli("--root", work)
        doc = json.loads(r.stdout) if r.stdout.strip() else {}
        check(r.returncode == 2
              and doc.get("finding") == "head_not_branch_tip",
              "offbranch-cli", f"rc={r.returncode} out={r.stdout!r}")
        cases += 1
        r = run_cli("--root", work, "--no-require-head")
        doc = json.loads(r.stdout) if r.stdout.strip() else {}
        check(r.returncode == 0
              and doc.get("head_equals_source") is False,
              "offbranch-waived-cli", f"rc={r.returncode} out={r.stdout!r}")

        # C4 — branch_missing: a directory that is not a repo, and a repo
        # whose branch ref is absent (unborn / wrong name).
        cases += 1
        try:
            resolve_source(plain)
            check(False, "missing-api", "expected RevPinError")
        except RevPinError as e:
            check(e.finding == "branch_missing" and e.result["source"] is None,
                  "missing-api", f"finding={e.finding}")
        empty = os.path.join(root, "empty")
        git(root, "-c", "init.defaultBranch=main", "init", "-q", empty)
        try:
            resolve_source(empty)
            check(False, "unborn-api", "expected RevPinError")
        except RevPinError as e:
            check(e.finding == "branch_missing",
                  "unborn-api", f"finding={e.finding}")
        cases += 1
        r = run_cli("--root", plain)
        doc = json.loads(r.stdout) if r.stdout.strip() else {}
        check(r.returncode == 2 and doc.get("finding") == "branch_missing",
              "missing-cli", f"rc={r.returncode} out={r.stdout!r}")

        # C5 — non-default branch name resolves through the same path.
        cases += 1
        git(work, "checkout", "-q", "-b", "side", "main")
        git(work, "push", "-q", "-u", "origin", "side")
        git(work, "checkout", "-q", "--detach", "main")
        res = resolve_source(work, branch="side")
        check(res["branch"] == "side" and res["source"] == res["remote"],
              "side-branch-api", f"got {res}")
        if failures:
            print("SELFTEST: FAILED " + "; ".join(failures))
            return 1
        print(f"red cases observed: head_not_branch_tip, "
              f"branch_not_pushed, branch_missing all raised and exit 2")
    except Exception as exc:  # fixture setup failure — report, still clean up
        print(f"SELFTEST: FAILED setup: {exc}")
        return 1
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print(f"SELFTEST: CLEAN cases={cases}")
    return 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    ap = argparse.ArgumentParser(
        description="Resolve a lane's jj-safe pin source: the branch tip, "
                    "validated against HEAD and origin (read-only git).")
    ap.add_argument("--root", help="lane repository root")
    ap.add_argument("--branch", default="main", help="branch name (main)")
    ap.add_argument("--no-require-pushed", action="store_true",
                    help="do not require the tip to be contained in origin")
    ap.add_argument("--no-require-head", action="store_true",
                    help="do not require HEAD to equal the branch tip")
    ap.add_argument("--selftest", action="store_true",
                    help="run fixture-based selftest outside the lane")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()
    if not args.root:
        ap.error("--root is required")

    try:
        result = resolve_source(
            args.root, branch=args.branch,
            require_pushed=not args.no_require_pushed,
            require_head=not args.no_require_head)
    except RevPinError as e:
        out = dict(e.result)
        out["finding"] = e.finding
        _emit(out)
        return 2
    _emit(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
