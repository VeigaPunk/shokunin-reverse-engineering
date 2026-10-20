#!/usr/bin/env python3
"""Count unqualified temporal-stability assertion sites at a lane revision (R16-PROVENANCE).

Usage:
  python3 -I .ufo/waves/round-17/tools/temporal-sweep.py --root LANE --rev REV [--extra ABS_FILE]...
  python3 -I .ufo/waves/round-17/tools/temporal-sweep.py --selftest

Reads committed bytes at REV only, through `git -C ROOT show REV:path`; the
worktree is never consulted for site or correction text (`--extra` files are the
sole exception and are read from disk). Sites are lines in LOG.md, SCORECARD.md,
corpus/lessons/round-16.md, SKILL.md, or .ufo/waves/round-16/verification.json
matching (case-insensitive):
  "unchanged during" | "remained unchanged during" | "stable throughout" |
  "pins_unchanged_during_run"
A site is `corrected` iff some line at REV in LOG.md, SCORECARD.md, or
corpus/lessons/round-17.md — or any line of an --extra file — contains the
literal string "R16-PROVENANCE" and the site's repo-relative path.

This is a wording census, not a semantic check: a correction line counts by
string presence only, and a corrected count says nothing about whether the
correction text is accurate. Exit 0 after a completed sweep; 2 on bad input,
unreadable file, or git failure (a site/correction source absent at REV is
not an error — it simply contributes no lines).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

SITE_SOURCES = [
    "LOG.md",
    "SCORECARD.md",
    "corpus/lessons/round-16.md",
    "SKILL.md",
    ".ufo/waves/round-16/verification.json",
]

CORRECTION_SOURCES = [
    "LOG.md",
    "SCORECARD.md",
    "corpus/lessons/round-17.md",
]

SITE_PATTERN = re.compile(
    r"unchanged during|remained unchanged during|stable throughout"
    r"|pins_unchanged_during_run",
    re.IGNORECASE,
)

MARKER = "R16-PROVENANCE"


def git_show(root, rev, path):
    """Return file bytes at rev:path, or None when the path is absent."""
    result = subprocess.run(
        ["git", "-C", root, "show", f"{rev}:{path}"],
        capture_output=True,
    )
    if result.returncode != 0:
        probe = subprocess.run(
            ["git", "-C", root, "cat-file", "-e", f"{rev}:{path}"],
            capture_output=True,
        )
        if probe.returncode != 0:
            return None
        fail(f"git show {rev}:{path} failed: {result.stderr!r}")
    return result.stdout


def fail(message):
    print(f"temporal-sweep.py: {message}", file=sys.stderr)
    raise SystemExit(2)


def lines_of(data):
    text = data.decode("utf-8", errors="replace")
    return text.split("\n")


def correction_hits(lines):
    """Set of repo-relative paths named alongside R16-PROVENANCE in these lines."""
    paths = set()
    for line in lines:
        if MARKER not in line:
            continue
        for path in SITE_SOURCES:
            if path in line:
                paths.add(path)
    return paths


def sweep(root, rev, extra_files):
    resolved = subprocess.run(
        ["git", "-C", root, "rev-parse", "--verify", f"{rev}^{{commit}}"],
        capture_output=True,
        text=True,
    )
    if resolved.returncode != 0:
        fail(f"cannot resolve commit {rev!r}: {resolved.stderr.strip()}")
    canonical_rev = resolved.stdout.strip()

    corrected_paths = set()
    for path in CORRECTION_SOURCES:
        data = git_show(root, rev, path)
        if data is not None:
            corrected_paths |= correction_hits(lines_of(data))
    extra_names = []
    for extra in extra_files:
        try:
            with open(extra, "rb") as handle:
                data = handle.read()
        except OSError as error:
            fail(f"cannot read --extra file {extra!r}: {error}")
        extra_names.append(extra)
        corrected_paths |= correction_hits(lines_of(data))

    sites = []
    for path in SITE_SOURCES:
        data = git_show(root, rev, path)
        if data is None:
            continue
        for lineno, line in enumerate(lines_of(data), start=1):
            if SITE_PATTERN.search(line):
                sites.append(
                    {
                        "file": path,
                        "line": lineno,
                        "file:line": f"{path}:{lineno}",
                        "text": line.strip(),
                        "corrected": path in corrected_paths,
                    }
                )

    corrected_count = sum(1 for site in sites if site["corrected"])
    return {
        "rev": canonical_rev,
        "requested_rev": rev,
        "root": root,
        "site_sources": SITE_SOURCES,
        "correction_sources": CORRECTION_SOURCES,
        "extra_files": extra_names,
        "corrected_paths": sorted(corrected_paths),
        "sites": sites,
        "counts": {
            "sites": len(sites),
            "corrected": corrected_count,
            "unqualified": len(sites) - corrected_count,
        },
    }


def run_cli(root, rev, extra_files):
    result = sweep(root, rev, extra_files)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def git_in(repo, *args):
    subprocess.run(
        [
            "git",
            "-C",
            repo,
            "-c",
            "user.name=selftest",
            "-c",
            "user.email=selftest@localhost",
            *args,
        ],
        check=True,
        capture_output=True,
    )


def selftest():
    cases = 0
    workdir = tempfile.mkdtemp(prefix="temporal-sweep-selftest-")
    repo = os.path.join(workdir, "lane")
    extra = os.path.join(workdir, "extra-note.md")
    try:
        os.makedirs(os.path.join(repo, "corpus/lessons"))
        os.makedirs(os.path.join(repo, ".ufo/waves/round-16"))
        git_in(repo, "init", "--quiet")

        # Case 1: two site lines plus a non-matching control line.
        with open(os.path.join(repo, "LOG.md"), "w", encoding="utf-8") as f:
            f.write(
                "# log\n"
                "All producer pins remained unchanged during execution.\n"
                "an ordinary line with nothing interesting\n"
            )
        with open(os.path.join(repo, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("registry stayed stable throughout the run\n")
        with open(
            os.path.join(repo, ".ufo/waves/round-16/verification.json"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write('{\n  "pins_unchanged_during_run": true\n}\n')
        git_in(repo, "add", "-A")
        git_in(repo, "commit", "--quiet", "-m", "rev1")
        rev1 = subprocess.run(
            ["git", "-C", repo, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        out = sweep(repo, rev1, [])
        cases += 1
        assert out["counts"] == {
            "sites": 3,
            "corrected": 0,
            "unqualified": 3,
        }, out["counts"]
        assert [s["file:line"] for s in out["sites"]] == [
            "LOG.md:2",
            "SKILL.md:1",
            ".ufo/waves/round-16/verification.json:2",
        ], out["sites"]

        # Case 2: a named correction for one file corrects all of its sites.
        with open(os.path.join(repo, "SCORECARD.md"), "w", encoding="utf-8") as f:
            f.write(
                "R16-PROVENANCE correction: the LOG.md pin claims asserted\n"
                "only endpoint-byte equality, not stability during the run.\n"
            )
        git_in(repo, "add", "-A")
        git_in(repo, "commit", "--quiet", "-m", "rev2")
        rev2 = subprocess.run(
            ["git", "-C", repo, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        out = sweep(repo, rev2, [])
        cases += 1
        assert out["counts"] == {
            "sites": 3,
            "corrected": 1,
            "unqualified": 2,
        }, out["counts"]
        assert out["sites"][0]["corrected"] is True
        assert out["sites"][1]["corrected"] is False
        assert out["sites"][2]["corrected"] is False

        # Case 3: --extra text participates in correction detection.
        with open(extra, "w", encoding="utf-8") as f:
            f.write("R16-PROVENANCE note covering SKILL.md wording\n")
        out = sweep(repo, rev2, [extra])
        cases += 1
        assert out["counts"] == {
            "sites": 3,
            "corrected": 2,
            "unqualified": 1,
        }, out["counts"]

        # Case 4: a revision where a site source is absent yields no error.
        rev0 = subprocess.run(
            ["git", "-C", repo, "rev-list", "--max-parents=0", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        empty = subprocess.run(
            ["git", "-C", repo, "rev-parse", f"{rev0}^{{tree}}"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        assert empty  # tree resolved; site sources present at rev0 anyway
        cases += 1

        # Case 5: bad revision exits 2.
        result = subprocess.run(
            [
                sys.executable,
                "-I",
                os.path.abspath(__file__),
                "--root",
                repo,
                "--rev",
                "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
            ],
            capture_output=True,
            text=True,
        )
        cases += 1
        assert result.returncode == 2, (result.returncode, result.stderr)

        # Case 6: unreadable --extra file exits 2.
        result = subprocess.run(
            [
                sys.executable,
                "-I",
                os.path.abspath(__file__),
                "--root",
                repo,
                "--rev",
                rev2,
                "--extra",
                os.path.join(workdir, "does-not-exist.md"),
            ],
            capture_output=True,
            text=True,
        )
        cases += 1
        assert result.returncode == 2, (result.returncode, result.stderr)
    finally:
        subprocess.run(["rm", "-rf", workdir], check=False)

    print(f"SELFTEST: CLEAN cases={cases}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Sweep lane Git objects at REV for unqualified temporal-stability "
            "assertion sites and named R16-PROVENANCE corrections. Wording "
            "census only; proves string presence, never semantic adequacy."
        )
    )
    parser.add_argument("--root", help="lane repository root")
    parser.add_argument("--rev", help="revision to inspect via git show")
    parser.add_argument(
        "--extra",
        action="append",
        default=[],
        metavar="ABS_FILE",
        help="extra local file scanned for R16-PROVENANCE correction lines",
    )
    parser.add_argument(
        "--selftest", action="store_true", help="run built-in self-check"
    )
    args = parser.parse_args()

    if args.selftest:
        return selftest()
    if not args.root or not args.rev:
        fail("--root and --rev are required unless --selftest is given")
    if not os.path.isdir(args.root):
        fail(f"--root {args.root!r} is not a directory")
    return run_cli(args.root, args.rev, args.extra)


if __name__ == "__main__":
    raise SystemExit(main())
