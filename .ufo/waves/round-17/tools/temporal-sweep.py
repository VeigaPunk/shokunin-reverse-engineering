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

# Round-17 L1 integration (w1 ScoutTemporalWording, CriticC1Vacuity, ReviewContract F5,
# DraftLogEntry): the contract's site list missed the r16 knowledge entry and its regex
# missed "unchanged across execution" (LOG.md:2012); a path-only marker line could mark
# every site corrected; sites read at the measured revision could be deleted to vanish.
SITE_SOURCES = [
    "LOG.md",
    "SCORECARD.md",
    "corpus/lessons/round-16.md",
    "SKILL.md",
    ".ufo/waves/round-16/verification.json",
]
SITE_DIRS = ["corpus/knowledge/", "corpus/lessons/"]
# Non-author outside-verifier files quote the defect they route; they are not lane
# assertions (w2 CriticC1Admission F5 asked for lessons coverage).
SITE_EXCLUDE_SUFFIX = ("-verifier-spotcheck.md",)

CORRECTION_SOURCES = [
    "LOG.md",
    "SCORECARD.md",
    "corpus/lessons/round-17.md",
]

# Temporal claims about a run/execution only: "unchanged across the fix" (a two-state
# before/after comparison, corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md:16)
# is not a during-run claim and is excluded by requiring run|execution.
SITE_PATTERN = re.compile(
    r"unchanged (during|across|throughout) (the )?(run|execution)|stable throughout"
    r"|pins_unchanged_during_run",
    re.IGNORECASE,
)

MARKER = "R16-PROVENANCE"
REQUIRED_PHRASE = "temporal stability not evidenced"


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


def resolve(root, rev):
    resolved = subprocess.run(
        ["git", "-C", root, "rev-parse", "--verify", f"{rev}^{{commit}}"],
        capture_output=True,
        text=True,
    )
    if resolved.returncode != 0:
        fail(f"cannot resolve commit {rev!r}: {resolved.stderr.strip()}")
    return resolved.stdout.strip()


def site_files(root, rev):
    files = list(SITE_SOURCES)
    listing = subprocess.run(
        ["git", "-C", root, "ls-tree", "-r", "--name-only", rev, "--"] + SITE_DIRS,
        capture_output=True,
        text=True,
    )
    if listing.returncode != 0:
        fail(f"git ls-tree failed: {listing.stderr.strip()}")
    seen = set(files)
    files += sorted(p for p in listing.stdout.splitlines()
                    if p.endswith(".md") and p not in seen
                    and not p.endswith(SITE_EXCLUDE_SUFFIX))
    return files


def find_sites(root, rev):
    """A site is attributed to the line where the match starts; the next line is
    joined so hard-wrapped prose ("unchanged during\\nthe run",
    corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95-96) is still found."""
    sites = []
    for path in site_files(root, rev):
        data = git_show(root, rev, path)
        if data is None:
            continue
        lines = lines_of(data)
        for lineno, line in enumerate(lines, start=1):
            # A marker line is exempt only when it is itself a qualified correction.
            if MARKER in line and REQUIRED_PHRASE in line.lower():
                continue
            nxt = lines[lineno].strip() if lineno < len(lines) else ""
            joined = line.rstrip() + " " + nxt
            m = SITE_PATTERN.search(joined)
            if m and m.start() < len(line.rstrip()):
                sites.append({"file": path, "line": lineno,
                              "file:line": f"{path}:{lineno}", "text": line.strip()})
    return sites


def correction_lines(root, rev, extra_files):
    out = []
    for path in CORRECTION_SOURCES:
        data = git_show(root, rev, path)
        if data is not None:
            out += [(path, i, l) for i, l in enumerate(lines_of(data), start=1)
                    if MARKER in l]
    for extra in extra_files:
        try:
            with open(extra, "rb") as handle:
                data = handle.read()
        except OSError as error:
            fail(f"cannot read --extra file {extra!r}: {error}")
        out += [(extra, i, l) for i, l in enumerate(lines_of(data), start=1)
                if MARKER in l]
    return out


def sweep(root, rev, extra_files, sites_rev=None):
    """Sites are read at sites_rev (default rev) so deleting a site cannot hide it;
    a site is corrected only by one line at rev carrying the marker, the site's exact
    `file:line`, and the required phrase."""
    canonical_rev = resolve(root, rev)
    canonical_sites_rev = resolve(root, sites_rev or rev)
    corr = correction_lines(root, canonical_rev, extra_files)
    sites = find_sites(root, canonical_sites_rev)
    for site in sites:
        hit = None
        for path, i, line in corr:
            token = site["file:line"]
            if (re.search(re.escape(token) + r"(?!\d)", line)
                    and REQUIRED_PHRASE in line.lower()):
                hit = f"{path}:{i}"
                break
        site["corrected"] = hit is not None
        site["corrected_by"] = hit
    new_sites = []
    if canonical_sites_rev != canonical_rev:
        known = {(s["file"], s["text"]) for s in sites}
        new_sites = [s for s in find_sites(root, canonical_rev)
                     if (s["file"], s["text"]) not in known]
    corrected_count = sum(1 for site in sites if site["corrected"])
    return {
        "rev": canonical_rev,
        "sites_rev": canonical_sites_rev,
        "requested_rev": rev,
        "root": root,
        "site_sources": SITE_SOURCES,
        "site_dirs": SITE_DIRS,
        "site_pattern": SITE_PATTERN.pattern,
        "correction_sources": CORRECTION_SOURCES,
        "correction_rule": f"one line: {MARKER} + exact file:line + '{REQUIRED_PHRASE}'",
        "extra_files": list(extra_files),
        "extra_used": bool(extra_files),
        "sites": sites,
        "new_sites_at_rev": new_sites,
        "counts": {
            "sites": len(sites),
            "corrected": corrected_count,
            "unqualified": len(sites) - corrected_count,
            "new_unqualified_at_rev": len(new_sites),
        },
    }


def run_cli(root, rev, extra_files, sites_rev=None):
    result = sweep(root, rev, extra_files, sites_rev)
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
        c = dict(out["counts"]); c.pop("new_unqualified_at_rev")
        assert c == {"sites": 3, "corrected": 0, "unqualified": 3}, out["counts"]
        assert [s["file:line"] for s in out["sites"]] == [
            "LOG.md:2",
            "SKILL.md:1",
            ".ufo/waves/round-16/verification.json:2",
        ], out["sites"]

        # Case 2 (red): a marker line naming only the path, or the file:line without
        # the required phrase, corrects nothing; a full line corrects exactly its site.
        with open(os.path.join(repo, "SCORECARD.md"), "w", encoding="utf-8") as f:
            f.write(
                "R16-PROVENANCE correction: LOG.md and SKILL.md pin claims\n"
                "R16-PROVENANCE: SKILL.md:1 was overstated\n"
                "R16-PROVENANCE: LOG.md:2 map matches committed blobs; "
                "temporal stability not evidenced.\n"
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
        assert out["counts"]["corrected"] == 1, out["counts"]
        assert out["sites"][0]["corrected"] is True
        assert out["sites"][1]["corrected"] is False
        assert out["sites"][2]["corrected"] is False

        # Case 3 (red): deleting a site at rev cannot hide it when sites_rev=rev1.
        with open(os.path.join(repo, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("registry row\n")
        git_in(repo, "add", "-A")
        git_in(repo, "commit", "--quiet", "-m", "rev3")
        rev3 = subprocess.run(
            ["git", "-C", repo, "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        out = sweep(repo, rev3, [], sites_rev=rev1)
        cases += 1
        assert out["counts"]["sites"] == 3 and out["counts"]["unqualified"] == 2, out["counts"]
        # --extra text participates (and is flagged as used).
        with open(extra, "w", encoding="utf-8") as f:
            f.write("R16-PROVENANCE SKILL.md:1 temporal stability not evidenced\n")
        out = sweep(repo, rev3, [extra], sites_rev=rev1)
        assert out["counts"]["unqualified"] == 1 and out["extra_used"] is True, out

        # Case 3b (w2 MutateTemporalSweep survivors): a hard-wrapped
        # "unchanged across\nexecution" site in a lesson is found; a correction
        # naming LOG.md:20 must not correct site LOG.md:2 (prefix collision);
        # a marker line without the phrase stays a site.
        os.makedirs(os.path.join(repo, "corpus/lessons"), exist_ok=True)
        with open(os.path.join(repo, "corpus/lessons/round-9.md"), "w", encoding="utf-8") as f:
            f.write("intro\nhashes remain unchanged across\nexecution.\n"
                    "R16-PROVENANCE pins unchanged during the run\n")
        with open(os.path.join(repo, "SCORECARD.md"), "w", encoding="utf-8") as f:
            f.write("R16-PROVENANCE: LOG.md:20 temporal stability not evidenced\n")
        git_in(repo, "add", "-A")
        git_in(repo, "commit", "--quiet", "-m", "rev4")
        rev4 = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
        out = sweep(repo, rev4, [])
        cases += 1
        lines = [s["file:line"] for s in out["sites"]]
        assert "corpus/lessons/round-9.md:2" in lines, lines
        assert "corpus/lessons/round-9.md:4" in lines, lines
        assert not [s for s in out["sites"] if s["file:line"] == "LOG.md:2" and s["corrected"]], out

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
        "--sites-rev",
        help="revision whose site lines are audited (default: --rev); use the "
        "baseline so deleted sites stay counted",
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
    return run_cli(args.root, args.rev, args.extra, args.sites_rev)


if __name__ == "__main__":
    raise SystemExit(main())
