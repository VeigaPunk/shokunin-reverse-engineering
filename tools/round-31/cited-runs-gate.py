#!/usr/bin/env python3
"""cited-runs-gate.py -- reject report lines that assert a gate or counter
result without a committed receipt.

Round-30 routed defect 1 (corpus/lessons/round-30-verifier-spotcheck.md:144):
the round-30 report asserted `settle-gate` PASS and `prefile: PASS` while
neither run was committed, and the only committed prefile run is red.

What counts as an assertion (per report line, independent of markdown context):
  * `PASS` (upper case, not part of a longer word),
  * `CLEAN` in a positive context (a preceding `NOT` -- e.g.
    `prefile: tree NOT CLEAN` -- does not count),
  * `exit 0` / `exit=0` / `exit_code=0`,
  * one or more counter pairs `key=<integer>` (e.g. `pass=16`, `matches=19`).

Every assertion line must cite at least one lane path under `.ufo/waves/` or
`corpus/evidence/` that exists as a blob at --rev and whose committed bytes
contain each asserted token.  A citation may be written in full or relative
to the report's round (`after/x.txt` -> `.ufo/waves/<round>/after/x.txt`).

stdout (findings only):
    UNCITED <line>: <excerpt>
    UNBACKED <line>: <path> lacks <token>
stderr: one `note:` line per unbacked citation resolution, then a summary.

Exit codes: 0 every assertion backed; 1 at least one finding; 2 usage error.

Stdlib only.  `--selftest` builds a throw-away git repo under the script's
directory and exercises the cases offline with GIT_DIR/GIT_WORK_TREE/
GIT_INDEX_FILE unset.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

SCRIPT = os.path.abspath(__file__)

ALLOWED_PREFIXES = (".ufo/waves/", "corpus/evidence/")

PASS_RE = re.compile(r"(?<![A-Za-z0-9_])PASS(?![A-Za-z0-9_])")
CLEAN_RE = re.compile(r"(?<![A-Za-z0-9_])CLEAN(?![A-Za-z0-9_])")
CLEAN_NEG_RE = re.compile(r"NOT[\s\-_]*$", re.IGNORECASE)
EXIT0_RE = re.compile(r"(?<![A-Za-z0-9_])exit(?:_code)?[ :=]+0(?![0-9])")
COUNTER_RE = re.compile(
    r"(?<![A-Za-z0-9_.\-])([a-z][a-z0-9]*(?:[_\-][a-z0-9]+)*)=([0-9]{1,6})(?![A-Za-z0-9_.])"
)
PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_.\-])"
    r"((?:\.ufo/waves|corpus/evidence)/[A-Za-z0-9._/\-]+"
    r"|[A-Za-z0-9_.\-]+/[A-Za-z0-9._/\-]+)"
)
ROUND_RE = re.compile(r"round-\d+")
EXIT_KEY_RE = {"exit", "exit_code"}
MAX_EXCERPT = 120


def sanitized_env():
    """Environment without git's location overrides."""
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def run_git(lane, args, timeout=120):
    try:
        return subprocess.run(
            ["git", "-C", lane, *args],
            capture_output=True,
            env=sanitized_env(),
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return subprocess.CompletedProcess(args, 127, b"", str(exc).encode())


def excerpt(line):
    text = line.strip()
    if len(text) > MAX_EXCERPT:
        text = text[: MAX_EXCERPT - 3] + "..."
    return text


def clean_is_positive(text):
    for match in CLEAN_RE.finditer(text):
        before = text[max(0, match.start() - 12): match.start()]
        if CLEAN_NEG_RE.search(before):
            continue
        return True
    return False


def strip_path_token(token):
    token = token.strip("`'\"(<[")
    token = token.rstrip(".,;:)]}>`'\"")
    return token


def asserted_tokens(line):
    """Ordered, deduplicated list of (label, matcher) asserted by one line."""
    tokens = []

    def add(label, matcher):
        if all(label != existing for existing, _ in tokens):
            tokens.append((label, matcher))

    if PASS_RE.search(line):
        add("PASS", lambda text: bool(PASS_RE.search(text)))
    if clean_is_positive(line):
        add("CLEAN", clean_is_positive)
    if EXIT0_RE.search(line):
        add("exit 0", lambda text: bool(EXIT0_RE.search(text)))
    for key, value in COUNTER_RE.findall(line):
        if key in EXIT_KEY_RE:
            continue
        label = "%s=%s" % (key, value)
        add(label, lambda text, want=label: want in text)
    return tokens


def citation_candidates(line, round_name):
    """Candidate lane-relative paths mentioned by a line, in citation order."""
    seen = set()
    candidates = []
    for raw in PATH_RE.findall(line):
        token = strip_path_token(raw)
        if not token or not token.strip("/"):
            continue
        if ".." in token.split("/"):
            continue
        attempts = []
        if token.startswith(ALLOWED_PREFIXES):
            attempts.append(token)
        if round_name:
            attempts.append(".ufo/waves/%s/%s" % (round_name, token))
            attempts.append("corpus/evidence/%s/%s" % (round_name, token))
        for attempt in attempts:
            if not attempt.startswith(ALLOWED_PREFIXES):
                continue
            if ".." in attempt.split("/"):
                continue
            if attempt in seen:
                continue
            seen.add(attempt)
            candidates.append((token, attempt))
    return candidates


class Gate:
    def __init__(self, lane, rev, report_path):
        self.lane = lane
        self.rev = rev
        self.report_path = report_path
        found = ROUND_RE.findall(os.path.abspath(report_path))
        self.round_name = found[-1] if found else None
        self.blob_cache = {}

    def blob_text(self, path):
        """Committed text of `path` at the gate rev, or None if not a blob."""
        if path in self.blob_cache:
            return self.blob_cache[path]
        kind = run_git(self.lane, ["cat-file", "-t", "%s:%s" % (self.rev, path)])
        if kind.returncode != 0 or kind.stdout.strip() != b"blob":
            self.blob_cache[path] = None
            return None
        shown = run_git(self.lane, ["show", "%s:%s" % (self.rev, path)])
        if shown.returncode != 0:
            self.blob_cache[path] = None
            return None
        text = shown.stdout.decode("utf-8", "replace")
        self.blob_cache[path] = text
        return text

    def check(self, lines):
        findings = []
        notes = []
        asserted = 0
        for lineno, line in enumerate(lines, 1):
            tokens = asserted_tokens(line)
            if not tokens:
                continue
            asserted += 1
            candidates = citation_candidates(line, self.round_name)
            resolved = []
            tried = []
            for written, path in candidates:
                text = self.blob_text(path)
                tried.append(path)
                if text is not None:
                    resolved.append((written, path, text))
            if not resolved:
                findings.append(("UNCITED", lineno, excerpt(line), None, None))
                if candidates:
                    notes.append(
                        "note: line %d cites no path that is a blob at %s; tried %s"
                        % (lineno, self.rev, ", ".join(tried))
                    )
                continue
            for label, matcher in tokens:
                if any(matcher(text) for _, _, text in resolved):
                    continue
                findings.append(
                    ("UNBACKED", lineno, excerpt(line), resolved[0][0], label)
                )
                notes.append(
                    "note: line %d asserts %r; cited %s lack(s) it at %s"
                    % (
                        lineno,
                        label,
                        ", ".join(path for _, path, _ in resolved),
                        self.rev,
                    )
                )
        return findings, notes, asserted


def read_lines(path):
    with open(path, "r", encoding="utf-8", errors="replace", newline=None) as handle:
        return handle.read().splitlines()


def report_findings(findings):
    for kind, lineno, text, path, token in findings:
        if kind == "UNCITED":
            print("UNCITED %d: %s" % (lineno, text))
        else:
            print("UNBACKED %d: %s lacks %s" % (lineno, path, token))


def usage_error(message):
    sys.stderr.write("cited-runs-gate: usage error: %s\n" % message)
    return 2


def main(argv):
    parser = argparse.ArgumentParser(
        prog="cited-runs-gate.py",
        description="Fail report lines that assert gate/counter results without committed receipts.",
    )
    parser.add_argument("--report", help="report markdown to inspect")
    parser.add_argument("--lane", help="lane repository root")
    parser.add_argument("--rev", help="commit the cited receipts must exist at")
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="run the offline self-test in a throw-away git repo",
    )
    parser.add_argument(
        "--keep-selftest",
        action="store_true",
        help="keep the self-test repository instead of removing it",
    )
    args = parser.parse_args(argv)

    if args.selftest:
        if args.report or args.lane or args.rev:
            return usage_error("--selftest takes no --report/--lane/--rev")
        return selftest(keep=args.keep_selftest)

    if not args.report or not args.lane or not args.rev:
        return usage_error("--report, --lane and --rev are all required")
    if not os.path.isfile(args.report):
        return usage_error("report is not a file: %s" % args.report)
    if not os.path.isdir(args.lane):
        return usage_error("lane is not a directory: %s" % args.lane)
    if not os.path.exists(os.path.join(args.lane, ".git")):
        return usage_error("lane is not a git repository: %s" % args.lane)
    verify = run_git(args.lane, ["rev-parse", "--verify", "--quiet", "%s^{commit}" % args.rev])
    if verify.returncode != 0 or not verify.stdout.strip():
        return usage_error("rev %r is not a commit in %s" % (args.rev, args.lane))
    sha = verify.stdout.decode().strip()

    try:
        lines = read_lines(args.report)
    except OSError as exc:
        return usage_error("cannot read report: %s" % exc)

    gate = Gate(args.lane, args.rev, args.report)
    findings, notes, asserted = gate.check(lines)

    for note in notes:
        sys.stderr.write(note + "\n")
    report_findings(findings)

    if findings:
        sys.stderr.write(
            "cited-runs-gate: FAIL findings=%d assertions=%d report=%s rev=%s\n"
            % (len(findings), asserted, args.report, sha)
        )
        return 1
    print(
        "cited-runs-gate: ok assertions=%d report=%s rev=%s"
        % (asserted, args.report, sha)
    )
    return 0


# --------------------------------------------------------------------------
# self-test
# --------------------------------------------------------------------------

SEED_FILES = {
    ".ufo/waves/round-30/green.txt": (
        "gate: PASS\n"
        "verdict=CLEAN\n"
        "exit=0\n"
        "carriers=16 pass=16 target=16\n"
        "mutants=19 matches=19 target=19 entry_ok=1 skill_ok=1\n"
    ),
    ".ufo/waves/round-30/red.txt": (
        "?? .ufo/waves/round-30/after/run.txt\n"
        "prefile: tree NOT CLEAN (3 paths)\n"
        "prefile: FAIL\n"
        "prefile_exit=1\n"
        "exit=1\n"
    ),
    ".ufo/waves/round-30/after/c1-run.txt": (
        "carriers=16 pass=16 target=16 entry_ok=1 (ok) province_ok=1 (ok)\n"
        "rev=deadbeef exit=0\n"
    ),
    ".ufo/waves/round-30/gone.txt": "gate: PASS\nexit=0\n",
    "corpus/evidence/round-30/c1/ok.txt": (
        "requests=23 matches=23 target=23 entry_ok=1 skill_ok=1\nexit=0\n"
    ),
    "tools/round-30/gate.py": "PASS CLEAN exit=0\n",
}


def sh(cmd, cwd):
    proc = subprocess.run(
        cmd, cwd=cwd, env=sanitized_env(), capture_output=True, text=True, timeout=120
    )
    if proc.returncode != 0:
        raise RuntimeError(
            "command failed (%d): %s\nstdout: %s\nstderr: %s"
            % (proc.returncode, " ".join(cmd), proc.stdout, proc.stderr)
        )
    return proc


def seed_repo(base):
    repo = tempfile.mkdtemp(prefix="cited-runs-gate-selftest-", dir=base)
    sh(["git", "init", "-q", "-b", "main", repo], base)
    for rel, content in SEED_FILES.items():
        target = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(content)
    os.makedirs(os.path.join(repo, ".ufo", "reports", "round-30"), exist_ok=True)

    def commit(message):
        sh(["git", "add", "-A"], repo)
        sh(
            [
                "git",
                "-c",
                "user.name=selftest",
                "-c",
                "user.email=selftest@local",
                "-c",
                "commit.gpgsign=false",
                "commit",
                "-q",
                "-m",
                message,
            ],
            repo,
        )

    commit("seed")
    base_rev = sh(["git", "rev-parse", "HEAD"], repo).stdout.strip()
    sh(["git", "rm", "-q", ".ufo/waves/round-30/gone.txt"], repo)
    commit("drop gone.txt at tip")
    tip_rev = sh(["git", "rev-parse", "HEAD"], repo).stdout.strip()
    return repo, base_rev, tip_rev


def invoke(report, repo, rev):
    return subprocess.run(
        [
            sys.executable,
            "-I",
            "-B",
            SCRIPT,
            "--report",
            report,
            "--lane",
            repo,
            "--rev",
            rev,
        ],
        capture_output=True,
        text=True,
        env=sanitized_env(),
        timeout=180,
    )


def selftest(keep=False):
    base = os.path.dirname(SCRIPT)
    repo = None
    cases = []
    try:
        repo, base_rev, tip_rev = seed_repo(base)

        def report(name, text):
            path = os.path.join(repo, ".ufo", "reports", "round-30", name + ".md")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
            return path

        def case(name, text, rev, code, has=(), lacks=(), err_has=()):
            path = report(name, text)
            proc = invoke(path, repo, rev)
            out = proc.stdout
            err = proc.stderr
            problems = []
            if proc.returncode != code:
                problems.append("exit %d != %d" % (proc.returncode, code))
            for pattern in has:
                if not re.search(pattern, out):
                    problems.append("stdout missing /%s/" % pattern)
            for pattern in lacks:
                if re.search(pattern, out):
                    problems.append("stdout unexpectedly has /%s/" % pattern)
            for pattern in err_has:
                if not re.search(pattern, err):
                    problems.append("stderr missing /%s/" % pattern)
            cases.append((name, problems, proc.returncode, out, err))

        # 1. backed PASS: green receipt cited in full, receipt holds PASS.
        case(
            "backed-pass",
            "- settle-gate PASS (`.ufo/waves/round-30/green.txt`)\n",
            tip_rev,
            0,
            has=[r"cited-runs-gate: ok assertions=1"],
        )
        # 2. uncited PASS: nothing under .ufo/waves or corpus/evidence cited.
        case(
            "uncited-pass",
            "- settle-gate PASS.\n",
            tip_rev,
            1,
            has=[r"^UNCITED 1: - settle-gate PASS\.$"],
        )
        # 3. cited path is not a blob at the gate rev (deleted at tip).
        case(
            "path-absent-at-rev",
            "- settle-gate PASS (`.ufo/waves/round-30/gone.txt`)\n",
            tip_rev,
            1,
            has=[r"^UNCITED 1:"],
            err_has=[r"not a blob|no path that is a blob"],
        )
        # 3b. same report passes at the rev where the receipt still exists.
        case(
            "path-present-at-base-rev",
            "- settle-gate PASS (`.ufo/waves/round-30/gone.txt`)\n",
            base_rev,
            0,
            has=[r"cited-runs-gate: ok assertions=1"],
        )
        # 4. path exists but its bytes never claim PASS (red receipt).
        case(
            "token-absent",
            "- prefile PASS (`.ufo/waves/round-30/red.txt`)\n",
            tip_rev,
            1,
            has=[r"^UNBACKED 1: \.ufo/waves/round-30/red\.txt lacks PASS$"],
        )
        # 5. red receipt for a CLEAN claim: `NOT CLEAN` must not back CLEAN.
        case(
            "red-receipt-clean",
            "- prefreeze-gate CLEAN (`.ufo/waves/round-30/red.txt`)\n",
            tip_rev,
            1,
            has=[r"^UNBACKED 1: \.ufo/waves/round-30/red\.txt lacks CLEAN$"],
        )
        # 6. counter target line backed by a committed receipt.
        case(
            "counter-backed",
            "- R30-C2 `mutants=19 matches=19 target=19 entry_ok=1 skill_ok=1` "
            "(`.ufo/waves/round-30/green.txt`)\n",
            tip_rev,
            0,
            has=[r"cited-runs-gate: ok assertions=1"],
        )
        # 7. one counter pair differs from the committed receipt.
        case(
            "counter-miscount",
            "- R30-C1 `carriers=15 pass=16 target=16` "
            "(`.ufo/waves/round-30/green.txt`)\n",
            tip_rev,
            1,
            has=[r"^UNBACKED 1: \.ufo/waves/round-30/green\.txt lacks carriers=15$"],
        )
        # 8. `exit 0` in the report backed by `exit=0` in the receipt.
        case(
            "exit0-equals-form",
            "- gate exit 0 (`.ufo/waves/round-30/after/c1-run.txt`)\n",
            tip_rev,
            0,
            has=[r"cited-runs-gate: ok assertions=1"],
        )
        # 9. `exit 0` against a receipt whose only exit code is 1.
        case(
            "exit0-red",
            "- gate exit 0 (`.ufo/waves/round-30/red.txt`)\n",
            tip_rev,
            1,
            has=[r"^UNBACKED 1: \.ufo/waves/round-30/red\.txt lacks exit 0$"],
        )
        # 10. relative shorthand resolves under the report's round.
        case(
            "shorthand-relative",
            "- R30-C1 `carriers=16 pass=16 target=16 entry_ok=1 province_ok=1`, "
            "exit 0 (`after/c1-run.txt`)\n",
            tip_rev,
            0,
            has=[r"cited-runs-gate: ok assertions=1"],
        )
        # 11. a citation outside the two evidence roots does not count.
        case(
            "outside-prefix",
            "- gate PASS (`tools/round-30/gate.py`)\n",
            tip_rev,
            1,
            has=[r"^UNCITED 1:"],
        )
        # 12. only the unbacked line of a mixed report is reported.
        case(
            "mixed-lines",
            "- settle-gate PASS (`.ufo/waves/round-30/green.txt`)\n"
            "- prefreeze-gate CLEAN.\n",
            tip_rev,
            1,
            has=[r"^UNCITED 2: - prefreeze-gate CLEAN\.$"],
            lacks=[r"UNCITED 1:"],
        )
        # 13. prose without an assertion is not a finding.
        case(
            "no-assertion",
            "- This line reports no gate result.\n",
            tip_rev,
            0,
            has=[r"cited-runs-gate: ok assertions=0"],
        )
        # 14-16. usage errors exit 2.
        no_args = subprocess.run(
            [sys.executable, "-I", "-B", SCRIPT],
            capture_output=True,
            text=True,
            env=sanitized_env(),
            timeout=120,
        )
        cases.append(
            (
                "usage-no-args",
                [] if no_args.returncode == 2 else ["exit %d != 2" % no_args.returncode],
                no_args.returncode,
                no_args.stdout,
                no_args.stderr,
            )
        )
        bad_rev = invoke(report("bad-rev", "- gate PASS\n"), repo, "0" * 40)
        cases.append(
            (
                "usage-bad-rev",
                [] if bad_rev.returncode == 2 else ["exit %d != 2" % bad_rev.returncode],
                bad_rev.returncode,
                bad_rev.stdout,
                bad_rev.stderr,
            )
        )
        missing_report = subprocess.run(
            [
                sys.executable,
                "-I",
                "-B",
                SCRIPT,
                "--report",
                os.path.join(repo, "no-such-report.md"),
                "--lane",
                repo,
                "--rev",
                tip_rev,
            ],
            capture_output=True,
            text=True,
            env=sanitized_env(),
            timeout=120,
        )
        cases.append(
            (
                "usage-missing-report",
                [] if missing_report.returncode == 2 else ["exit %d != 2" % missing_report.returncode],
                missing_report.returncode,
                missing_report.stdout,
                missing_report.stderr,
            )
        )
    finally:
        if repo and not keep:
            shutil.rmtree(repo, ignore_errors=True)

    failures = 0
    for name, problems, code, out, err in cases:
        if problems:
            failures += 1
            print("SELFTEST case %s: FAIL (%s)" % (name, "; ".join(problems)))
            if out.strip():
                print("  stdout: %s" % out.strip().replace("\n", " | "))
            if err.strip():
                print("  stderr: %s" % err.strip().replace("\n", " | "))
        else:
            print("SELFTEST case %s: PASS (exit %d)" % (name, code))
    print(
        "SELFTEST %s cases=%d passed=%d"
        % ("ok" if failures == 0 else "FAIL", len(cases), len(cases) - failures)
    )
    if repo:
        print("SELFTEST repo=%s%s" % (repo, " (kept)" if keep else " (removed)"))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(130)
