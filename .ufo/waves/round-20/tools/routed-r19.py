#!/usr/bin/env python3
"""routed-r19.py — revision-scoped C1 counter for the round-19 routed defects.

A defect is closed only when BOTH its append-only name appears in SCORECARD.md
and corpus/lessons/round-20.md at REV, and its behavioral/recomputed check passes
using REV's Git objects. Revision tools execute only through REV's revexec.py;
the counter never executes a tool blob directly. All fixtures and extraction
scratch are created under /tmp and removed on exit.

Usage:
  python3 -I -B routed-r19.py --root LANE --rev REV [--strict] [--live]
  python3 -I -B routed-r19.py --selftest

Exit: 0 for a usable measurement (or a clean strict measurement), 1 for
--strict with open items, 2 for unusable input.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

BASELINE = "14f0260ad319ecc26994381b2415d5a999003375"
W20 = ".ufo/waves/round-20"
ROUTED_TOOL = W20 + "/tools/routed-r19.py"
REVEXEC = W20 + "/tools/revexec.py"
SCORECARD = "SCORECARD.md"
LESSON = "corpus/lessons/round-20.md"
CUSTODY = ".ufo/gates/custody-pair/custody-pair.py"
TIMESTAMPS = W20 + "/tools/evidence-timestamps.py"
CARRIER_GUARD = W20 + "/tools/carrier-guard.py"
CARRIERS = W20 + "/predictions/carriers.tsv"
CARRIER_EVIDENCE = W20 + "/evidence/carrier-guard"
CENSUS = ".ufo/gates/c1-census-v10.py"
FINAL_CENSUS = W20 + "/verify/final-census.json"
HEAD_LINT = ".ufo/waves/round-18/tools/head-rev-lint.py"
CITATION_PROBE = ".ufo/gates/citation-drift/citation-drift-probe.py"
RECEIPT_VALIDATE = ".ufo/waves/round-17/tools/receipt-validate.py"
PINS = ".ufo/waves/round-17/tools/pins.py"
WAVE_OUTCOMES = ".ufo/waves/round-19/tools/wave-outcomes.py"
JJ_RED_BEFORE = ".ufo/waves/round-18/tools/jj-red-before.py"
REVPIN = ".ufo/waves/round-18/tools/revpin.py"
ITEMS = ("D1", "D2", "D3", "D4", "D5", "D6a", "D6b", "D6c", "D6d", "D6e", "D6f")
UTC_FIXTURE_DATE = "2000-01-01T00:00:00Z"


class CounterError(Exception):
    """Input or Git-object failure that makes the whole measurement unusable."""


def _clean_env(extra=None):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("GIT_", "JJ_")) and k != "TMPDIR"}
    env["TMPDIR"] = "/tmp"
    if extra:
        env.update(extra)
    return env


def _run_git(root, args, timeout=60, env=None):
    """Run Git only; this is never an extracted Python-tool launch."""
    argv = ["git", "--no-optional-locks", "-C", root, *args]
    try:
        proc = subprocess.run(argv, capture_output=True, env=_clean_env(env),
                              timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout if isinstance(exc.stdout, bytes) else b""
        err = exc.stderr if isinstance(exc.stderr, bytes) else b""
        return 124, out, err + b"git command timed out"
    except OSError as exc:
        return 127, b"", (str(exc)).encode("utf-8", "replace")


def _run_revexec(revexec_path, root, tool_rev, entry, args, extras=(), timeout=240):
    """Launch a tool only by asking the extracted REV revexec to run it."""
    argv = [sys.executable, "-I", "-B", revexec_path, "run",
            "--root", root, "--rev", tool_rev, "--entry", entry]
    for extra in extras:
        argv.extend(("--extra", extra))
    argv.extend(("--", *args))
    try:
        proc = subprocess.run(argv, capture_output=True, env=_clean_env(),
                              timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout if isinstance(exc.stdout, bytes) else b""
        err = exc.stderr if isinstance(exc.stderr, bytes) else b""
        return 124, out, err + b"revexec command timed out"
    except OSError as exc:
        return 127, b"", (str(exc)).encode("utf-8", "replace")


def _run_revexec_selftest(revexec_path, timeout=240):
    """Run the REV revexec tool's own selftest (the wrapper under test)."""
    argv = [sys.executable, "-I", "-B", revexec_path, "--selftest"]
    try:
        proc = subprocess.run(argv, capture_output=True, env=_clean_env(),
                              timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout if isinstance(exc.stdout, bytes) else b""
        err = exc.stderr if isinstance(exc.stderr, bytes) else b""
        return 124, out, err + b"revexec selftest timed out"
    except OSError as exc:
        return 127, b"", (str(exc)).encode("utf-8", "replace")


def _revexec_preflight(git, rev, tmp):
    source = git.blob(rev, ROUTED_TOOL)
    if source is None:
        git.revexec_ready = False
        git.revexec_why = "routed-r19.py absent at REV"
        return False, git.revexec_why
    ast_ok, ast_why = _subprocess_ast_ok(_text(source))
    if not ast_ok:
        git.revexec_ready = False
        git.revexec_why = ast_why
        return False, git.revexec_why
    blob = git.blob(rev, REVEXEC)
    if blob is None:
        git.revexec_ready = False
        git.revexec_why = "revexec.py absent at REV"
        return False, git.revexec_why
    stage = tempfile.mkdtemp(prefix="revexec-preflight-", dir=tmp)
    path = os.path.join(stage, "revexec.py")
    with open(path, "wb") as fh:
        fh.write(blob)
    rc, out, err = _run_revexec_selftest(path)
    text = _text(out) + "\n" + _text(err)
    ready = (rc == 0 and "SELFTEST: CLEAN" in text and
             "write_outside_refused" in text and "net_refused" in text)
    git.revexec_ready = ready
    git.revexec_why = ("revexec selftest CLEAN with write_outside_refused and net_refused"
                       if ready else "revexec sandbox selftest failed its clean/refusal gate")
    return ready, git.revexec_why


def _fixture_git(root, args, env=None, timeout=90):
    return _run_git(root, args, timeout=timeout, env=env)


def _text(data):
    return data.decode("utf-8", "replace") if isinstance(data, bytes) else str(data)


def _combined(result):
    if not result:
        return ""
    return _text(result.get("stdout", b"")) + "\n" + _text(result.get("stderr", b""))


class GitObjects:
    def __init__(self, root):
        self.root = os.path.abspath(root)

    def run(self, args, timeout=60):
        return _run_git(self.root, args, timeout=timeout)

    def resolve(self, rev):
        rc, out, err = self.run(["rev-parse", "--verify", "--end-of-options",
                                 "%s^{commit}" % rev])
        if rc != 0:
            raise CounterError("revision_unresolvable: %s" % _text(err).strip())
        value = _text(out).strip()
        if not re.fullmatch(r"[0-9a-fA-F]{40,64}", value):
            raise CounterError("revision_unresolvable: Git returned no commit id")
        return value

    def blob(self, rev, path):
        rc, out, _err = self.run(["show", "--no-ext-diff", "--no-textconv",
                                  "%s:%s" % (rev, path)])
        return out if rc == 0 else None

    def text(self, rev, path):
        raw = self.blob(rev, path)
        return None if raw is None else _text(raw)

    def files(self, rev):
        rc, out, err = self.run(["ls-tree", "-r", "--name-only", "-z", rev],
                                timeout=90)
        if rc != 0:
            raise CounterError("tree_unreadable: %s" % _text(err).strip())
        return [p.decode("utf-8", "surrogateescape") for p in out.split(b"\0") if p]


def _named(git, rev):
    scorecard = git.text(rev, SCORECARD)
    lesson = git.text(rev, LESSON)
    result = {}
    for item in ITEMS:
        marker = "- R19-%s:" % item
        score_ok = scorecard is not None and any(
            line.startswith(marker) for line in scorecard.splitlines())
        lesson_ok = lesson is not None and any(
            line.startswith(marker) for line in lesson.splitlines())
        result[item] = (score_ok and lesson_ok,
                        score_ok, lesson_ok)
    return result


def _tmp_root(root, prefix):
    path = tempfile.mkdtemp(prefix=prefix, dir="/tmp")
    real = os.path.realpath(path)
    if root:
        lane = os.path.realpath(root)
        if real == lane or real.startswith(lane + os.sep):
            shutil.rmtree(path, ignore_errors=True)
            raise CounterError("scratch_inside_lane: /tmp resolved into LANE")
    if _is_worktree_path(path):
        shutil.rmtree(path, ignore_errors=True)
        raise CounterError("scratch_inside_worktree: /tmp resolved into a Git worktree")
    return path


def _run_tool(git, root, tmp, harness_rev, tool_rev, entry, args,
              extras=(), timeout=240):
    """Stage the REV's revexec blob, then ask it to run an entry."""
    if not getattr(git, "revexec_ready", False):
        return None, getattr(git, "revexec_why", "revexec sandbox not preflighted")
    if git.blob(tool_rev, entry) is None:
        return None, "%s absent at REV" % entry
    wrapper_blob = git.blob(harness_rev, REVEXEC)

    if wrapper_blob is None:
        return None, "revexec.py absent at harness revision"
    for extra in extras:
        if git.blob(tool_rev, extra) is None:
            return None, "%s absent at tool revision" % extra
    stage = tempfile.mkdtemp(prefix="revexec-", dir=tmp)
    revexec_path = os.path.join(stage, "revexec.py")
    with open(revexec_path, "wb") as fh:
        fh.write(wrapper_blob)
    rc, out, err = _run_revexec(revexec_path, root, tool_rev, entry, args,
                                extras=extras, timeout=timeout)
    return {"returncode": rc, "stdout": out, "stderr": err}, None


def _json_bytes(data):
    try:
        return json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
        return None


def _has_code(value, wanted):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in ("code", "finding", "id") and child == wanted:
                return True
            if _has_code(child, wanted):
                return True
    elif isinstance(value, list):
        return any(_has_code(child, wanted) for child in value)
    return False

def _selftest_has_case(source, function_name, label):
    try:
        tree = ast.parse(source)
    except (SyntaxError, TypeError, ValueError):
        return False
    function = next((node for node in tree.body
                     if isinstance(node, ast.FunctionDef)
                     and node.name == function_name), None)
    if function is None:
        return False
    for node in ast.walk(function):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id not in ("check", "run_case"):
            continue
        if any(isinstance(arg, ast.Constant) and arg.value == label
               for arg in node.args):
            return True
    return False

def _future_dated_claim(data, output):
    for row in _walk_values(data):
        fields = " ".join(str(row.get(key, "")) for key in
                          ("finding", "code", "id", "type", "path", "file",
                           "line", "where"))
        if ("future_dated" in fields and "round-19" in fields and
                "claims.json" in fields and re.search(r"\b36\b", fields)):
            return True
    return ("future_dated" in output and "round-19" in output and
            "claims.json" in output and
            re.search(r'claims\.json(?::|[\s",]+)36\b', output) is not None)


def _is_worktree_path(path):
    current = os.path.realpath(path)
    while True:
        if os.path.lexists(os.path.join(current, ".git")):
            return True
        parent = os.path.dirname(current)
        if parent == current:
            return False
        current = parent




def _nested_git_under_ufo(root):
    ufo = os.path.join(root, ".ufo")
    if not os.path.isdir(ufo):
        return []
    found = []
    for base, dirs, files in os.walk(ufo, followlinks=False):
        if ".git" in dirs:
            found.append(os.path.relpath(os.path.join(base, ".git"), root))
            dirs.remove(".git")
        if ".git" in files:
            found.append(os.path.relpath(os.path.join(base, ".git"), root))
    return sorted(found)


def _live_custody_check(root):
    rc, out, err = _run_git(root, ["status", "--porcelain", "--ignored"], timeout=90)
    if rc != 0:
        return False, "live git status failed: %s" % _text(err).strip()
    nested = _nested_git_under_ufo(root)
    if nested:
        return False, "live .ufo contains nested .git: %s" % ", ".join(nested)
    return True, "live git status --porcelain --ignored exit 0; no nested .git under .ufo (%d status rows)" % sum(
        1 for line in _text(out).splitlines() if line)


def _s_d1(ctx):
    git, root, rev, tmp = ctx["git"], ctx["root"], ctx["rev"], ctx["tmp"]
    source = git.blob(rev, CUSTODY)
    if source is None:
        return False, "%s absent at REV" % CUSTODY
    source_text = _text(source)
    if (not _selftest_has_case(source_text, "cmd_selftest",
                               "scratch_in_worktree_refused") or
            not _selftest_has_case(source_text, "cmd_selftest",
                                   "cleanup_after_run")):
        return False, "custody-pair selftest lacks the worktree-refusal or cleanup fixture"
    inside, err = _run_tool(git, root, tmp, rev, rev, CUSTODY,
                            ["selftest", "--scratch", root])
    if err:
        return False, err
    inside_text = _combined(inside)
    if inside["returncode"] != 2 or "scratch_inside_worktree" not in inside_text:
        return False, "in-worktree scratch did not refuse exit 2 with scratch_inside_worktree"

    outside_run, err = _run_tool(git, root, tmp, rev, rev, CUSTODY,
                                 ["selftest", "--scratch", "."])
    if err:
        return False, err
    outside_text = _combined(outside_run)
    if outside_run["returncode"] != 0 or "SELFTEST: CLEAN" not in outside_text:
        return False, "outside-workdir scratch selftest was not CLEAN exit 0"
    if ctx["live"]:
        live_ok, live_why = _live_custody_check(root)
        if not live_ok:
            return False, live_why
        return True, "in-worktree refusal; cleanup_after_run selftest CLEAN; " + live_why
    return True, "in-worktree refusal; outside sandbox scratch and cleanup_after_run selftest CLEAN"


def _commit_fixture(repo, message, commit_date=None):
    rc, _out, err = _fixture_git(repo, ["add", "-A"])
    if rc != 0:
        raise CounterError("fixture_git_add: %s" % _text(err).strip())
    env = {}
    if commit_date:
        env = {"GIT_AUTHOR_DATE": commit_date,
               "GIT_COMMITTER_DATE": commit_date}
    rc, _out, err = _fixture_git(
        repo, ["-c", "user.name=RoutedR19 fixture",
               "-c", "user.email=routed-r19@example.invalid",
               "commit", "-qm", message], env=env)
    if rc != 0:
        raise CounterError("fixture_git_commit: %s" % _text(err).strip())
    g = GitObjects(repo)
    return g.resolve("HEAD")


def _s_d2(ctx):
    git, root, rev, tmp = ctx["git"], ctx["root"], ctx["rev"], ctx["tmp"]
    bad, err = _run_tool(
        git, root, tmp, rev, rev, TIMESTAMPS,
        ["--root", root, "--rev", BASELINE, "--path", ".ufo/waves/round-19",
         "--strict"])
    if err:
        return False, err
    bad_text = _combined(bad)
    bad_data = _json_bytes(bad["stdout"])
    if bad["returncode"] != 1 or not _future_dated_claim(bad_data, bad_text):
        return False, "baseline claims.json:36 was not reported future_dated (exit 1)"

    repo = os.path.join(tmp, "d2-clean-repo")
    os.makedirs(repo)
    rc, _out, stderr = _fixture_git(repo, ["init", "-q", "-b", "main"])
    if rc != 0:
        return False, "clean fixture init failed: %s" % _text(stderr).strip()
    clean_path = os.path.join(repo, ".ufo", "waves", "round-20", "evidence")
    os.makedirs(clean_path)
    with open(os.path.join(clean_path, "clean.txt"), "w", encoding="utf-8") as fh:
        fh.write("introduced and recorded at " + UTC_FIXTURE_DATE + "\n")
    clean_rev = _commit_fixture(repo, "clean timestamp fixture", UTC_FIXTURE_DATE)
    clean, err = _run_tool(
        git, root, tmp, rev, rev, TIMESTAMPS,
        ["--root", repo, "--rev", clean_rev,
         "--path", ".ufo/waves/round-20/evidence", "--strict"])
    if err:
        return False, err
    if clean["returncode"] != 0 or "future_dated" in _combined(clean):
        return False, "clean timestamp fixture did not pass strict mode"
    return True, "future_dated at baseline claims.json:36 and clean committed timestamp fixture passed"


def _manifest_paths(text, root):
    rows = list(csv.reader(io.StringIO(text), delimiter="\t"))
    rows = [row for row in rows if row and any(cell.strip() for cell in row)]
    if not rows:
        raise ValueError("carrier manifest has no rows")
    names = [cell.strip().lower() for cell in rows[0]]
    index = next((names.index(candidate) for candidate in
                  ("path", "carrier_path", "binary_path", "file", "binary", "carrier")
                  if candidate in names), None)
    data_rows = rows[1:] if index is not None else rows
    paths = []
    for row in data_rows:
        if index is not None:
            if index >= len(row) or not row[index].strip():
                raise ValueError("carrier manifest row has no path")
            value = row[index].strip()
        else:
            candidates = [cell.strip() for cell in row if "/" in cell.strip()]
            if len(candidates) != 1:
                raise ValueError("carrier manifest row has ambiguous path columns")
            value = candidates[0]
        paths.append(_carrier_key(value, root))
    if not paths or len(paths) != len(set(paths)):
        raise ValueError("carrier manifest path set is empty or duplicated")
    return set(paths)


def _carrier_key(value, root):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("carrier path is not a non-empty string")
    value = os.path.normpath(value.strip())
    return value if os.path.isabs(value) else os.path.normpath(os.path.join(root, value))


def _record_carriers(record, root):
    carriers = record.get("carriers") if isinstance(record, dict) else None
    if not isinstance(carriers, list) or not carriers:
        raise ValueError("carrier record has no non-empty carriers array")
    result = []
    for row in carriers:
        if not isinstance(row, dict) or "path" not in row:
            raise ValueError("carrier record row has no path")
        result.append(_carrier_key(row["path"], root))
    if len(result) != len(set(result)):
        raise ValueError("carrier record contains duplicate paths")
    return set(result)


def _s_d3(ctx):
    git, root, rev, tmp = ctx["git"], ctx["root"], ctx["rev"], ctx["tmp"]
    run, err = _run_tool(git, root, tmp, rev, rev, CARRIER_GUARD, ["--selftest"])
    if err:
        return False, err
    text = _combined(run)
    if run["returncode"] != 0 or "SELFTEST: CLEAN" not in text:
        return False, "carrier-guard selftest was not CLEAN exit 0"
    if "exec_refused" not in text or "mode_restored" not in text:
        return False, "carrier-guard selftest omitted exec_refused or mode_restored"

    files = git.files(rev)
    arm_path = CARRIER_EVIDENCE + "/arm.json"
    arm = _json_bytes(git.blob(rev, arm_path))
    if not isinstance(arm, dict):
        return False, "carrier-guard arm.json absent or invalid at REV"
    try:
        manifest_blob = git.blob(rev, CARRIERS)
        wanted = (_manifest_paths(_text(manifest_blob), root)
                  if manifest_blob is not None else None)
        check_paths = [path for path in files
                       if path.startswith(CARRIER_EVIDENCE + "/check-")
                       and path.endswith(".json")]
        passed = False
        for path in check_paths:
            record = _json_bytes(git.blob(rev, path))
            if not isinstance(record, dict) or type(record.get("exit")) is not int \
                    or record.get("exit") != 0:
                continue
            try:
                current = _record_carriers(record, root)
            except (ValueError, TypeError):
                continue
            if (current == wanted if wanted is not None else bool(current)):
                passed = True
                break
        if not passed:
            return False, "no exit-0 check record has the required carrier set"
    except (ValueError, TypeError, UnicodeDecodeError) as exc:
        return False, "carrier evidence invalid: %s" % exc
    return True, "clean exec_refused/mode_restored selftest; arm.json and matching exit-0 check record retained"


def _extract_archive(archive, dest):
    os.makedirs(dest, exist_ok=True)
    root = os.path.realpath(dest)

    def inside(path):
        real = os.path.realpath(path)
        return real == root or real.startswith(root + os.sep)

    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        for member in tar:
            if member.name.startswith("/") or "\0" in member.name:
                raise ValueError("archive member path is absolute or contains NUL")
            parts = [part for part in member.name.split("/") if part not in ("", ".")]
            if not parts or any(part == ".." for part in parts):
                raise ValueError("archive member path escapes export")
            target = os.path.join(dest, *parts)
            parent = os.path.dirname(target)
            if not inside(parent):
                raise ValueError("archive parent resolves outside export")
            os.makedirs(parent, exist_ok=True)
            if not inside(parent):
                raise ValueError("archive parent resolves outside export")
            if member.isdir():
                if os.path.lexists(target):
                    if os.path.islink(target) or not os.path.isdir(target):
                        raise ValueError("archive directory collides with non-directory")
                else:
                    os.mkdir(target)
            elif member.issym():
                if os.path.lexists(target):
                    raise ValueError("archive symlink collides with existing path")
                os.symlink(member.linkname, target)
            elif member.isfile():
                if os.path.lexists(target):
                    raise ValueError("archive file collides with existing path")
                source = tar.extractfile(member)
                if source is None:
                    raise ValueError("archive file has no payload")
                with source, open(target, "xb") as output:
                    shutil.copyfileobj(source, output)
                os.chmod(target, member.mode & 0o777)
            else:
                raise ValueError("unsupported archive member type")


def _s_d4(ctx):
    git, root, rev, tmp = ctx["git"], ctx["root"], ctx["rev"], ctx["tmp"]
    if git.blob(rev, CENSUS) is None:
        return False, "%s absent at REV" % CENSUS
    rc, archive, err = git.run(["archive", "--format=tar", rev], timeout=180)
    if rc != 0:
        return False, "git archive failed: %s" % _text(err).strip()
    export = os.path.join(tmp, "d4-archive-export")
    try:
        _extract_archive(archive, export)
    except (OSError, tarfile.TarError, ValueError) as exc:
        return False, "git archive extraction failed: %s" % exc
    result, err = _run_tool(git, root, tmp, rev, rev, CENSUS,
                            ["--root", export], timeout=300)
    if err:
        return False, err
    output = _combined(result)
    if result["returncode"] != 0 or "VERDICT: PASS" not in output:
        return False, "c1-census-v10 archive run did not print VERDICT: PASS exit 0"
    return True, "c1-census-v10.py from REV passed over a git archive export"


def _safe_relpath(value):
    if not isinstance(value, str) or not value or os.path.isabs(value) or "\\" in value:
        return False
    parts = value.split("/")
    return all(part not in ("", ".", "..") for part in parts)


def _s_d5(ctx):
    git, rev = ctx["git"], ctx["rev"]
    blob = git.blob(rev, FINAL_CENSUS)
    record = _json_bytes(blob)
    if not isinstance(record, dict):
        return False, "final-census.json absent or invalid at REV"
    target_rev = record.get("rev")
    stdout_path = record.get("stdout_path")
    stdout_sha = record.get("stdout_sha256")
    argv = record.get("argv")
    if type(record.get("exit")) is not int or record.get("exit") != 0:
        return False, "final census record exit is not integer 0"
    if not isinstance(argv, list) or not argv or not all(isinstance(x, str) for x in argv):
        return False, "final census record argv is absent or malformed"
    if not _safe_relpath(stdout_path):
        return False, "final census stdout_path is not a safe lane-relative path"
    if not isinstance(stdout_sha, str) or not re.fullmatch(r"[0-9a-f]{64}", stdout_sha):
        return False, "final census stdout_sha256 is absent or malformed"
    if not isinstance(target_rev, str) or not target_rev:
        return False, "final census record rev is absent"
    try:
        census_rev = git.resolve(target_rev)
    except CounterError as exc:
        return False, "final census record rev does not resolve: %s" % exc
    stdout = git.blob(census_rev, stdout_path)
    if stdout is None or hashlib.sha256(stdout).hexdigest() != stdout_sha:
        return False, "final census stdout is absent at named rev or its sha256 differs"
    rc, changed, err = git.run(["diff", "--no-renames", "--name-only", "-z",
                                rev, census_rev], timeout=90)
    if rc != 0:
        return False, "final census tree comparison failed: %s" % _text(err).strip()
    paths = {p.decode("utf-8", "surrogateescape") for p in changed.split(b"\0") if p}
    if paths != {FINAL_CENSUS, stdout_path}:
        return False, "named census tree differs outside record/stdout pair: %s" % sorted(paths)
    return True, "named revision differs only in final-census.json and stdout; exit and stdout sha256 match"


def _walk_values(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_values(child)


def _s_d6a(ctx):
    git, root, rev, tmp = ctx["git"], ctx["root"], ctx["rev"], ctx["tmp"]
    result, err = _run_tool(git, root, tmp, rev, rev, HEAD_LINT,
                            ["--root", root, "--rev", rev])
    if err:
        return False, err
    if result["returncode"] != 0:
        return False, "head-rev-lint exit was not 0"
    data = _json_bytes(result["stdout"])
    if data is None:
        return False, "head-rev-lint output was not JSON"
    found = set()
    labels = ("class", "context", "finding", "classification", "category",
              "kind", "type")

    def collect(value, nested=False):
        if isinstance(value, dict):
            is_nested = nested or any(
                isinstance(value.get(key), str) and value[key].lower() == "nested"
                for key in labels)
            path = value.get("path")
            if is_nested and isinstance(path, str):
                normalized = path.replace("\\", "/")
                if "round-17" in normalized:
                    if normalized.endswith("verify.py"):
                        found.add("verify.py")
                    if normalized.endswith("revpin.py"):
                        found.add("revpin.py")
            for key, child in value.items():
                collect(child, is_nested or str(key).lower() == "nested")
        elif isinstance(value, list):
            for child in value:
                collect(child, nested)
        elif isinstance(value, str) and nested:
            normalized = value.replace("\\", "/")
            if "round-17" in normalized:
                if normalized.endswith("verify.py"):
                    found.add("verify.py")
                if normalized.endswith("revpin.py"):
                    found.add("revpin.py")

    collect(data)
    if found != {"verify.py", "revpin.py"}:
        return False, "nested findings missing for round-17 verify.py and/or revpin.py"
    return True, "head-rev-lint reports both round-17 files as nested"


def _assignment_list(function, name="argv"):
    for node in ast.walk(function):
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == name
                for target in node.targets):
            if isinstance(node.value, ast.List):
                return node.value
    return None


def _subprocess_ast_ok(source):
    try:
        tree = ast.parse(source)
    except (SyntaxError, TypeError, ValueError):
        return False, "routed-r19.py does not parse as Python"

    calls = []
    forbidden = []

    class Scan(ast.NodeVisitor):
        def __init__(self):
            self.functions = []

        def visit_FunctionDef(self, node):
            self.functions.append(node.name)
            self.generic_visit(node)
            self.functions.pop()

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_Call(self, node):
            fn = node.func
            owner = self.functions[-1] if self.functions else "<module>"
            if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name) \
                    and fn.value.id == "subprocess":
                if fn.attr == "run":
                    calls.append((owner, node))
                else:
                    forbidden.append("subprocess.%s" % fn.attr)
            elif isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name) \
                    and fn.value.id == "os" and (fn.attr == "system" or fn.attr.startswith("exec")):
                forbidden.append("os.%s" % fn.attr)
            elif isinstance(fn, ast.Name) and fn.id in ("exec", "eval"):
                forbidden.append(fn.id)
            self.generic_visit(node)

    Scan().visit(tree)
    if forbidden:
        return False, "direct execution primitive found: %s" % ", ".join(sorted(set(forbidden)))
    allowed = {"_run_git", "_run_revexec", "_run_revexec_selftest"}
    if len(calls) != 3 or {owner for owner, _node in calls} != allowed:
        return False, "subprocess.run sites are not confined to Git and revexec wrappers"
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    git_list = _assignment_list(functions["_run_git"])
    if (git_list is None or not git_list.elts or
            not isinstance(git_list.elts[0], ast.Constant) or git_list.elts[0].value != "git"):
        return False, "Git wrapper does not launch a literal git command"
    for fname, required in (("_run_revexec", {"run", "--root", "--rev", "--entry"}),
                            ("_run_revexec_selftest", {"--selftest"})):
        argv = _assignment_list(functions[fname])
        if argv is None or len(argv.elts) < 4:
            return False, "%s does not construct a revexec-only command" % fname
        start = argv.elts[:4]
        if not (isinstance(start[0], ast.Attribute) and
                isinstance(start[0].value, ast.Name) and start[0].value.id == "sys" and
                start[0].attr == "executable" and
                isinstance(start[1], ast.Constant) and start[1].value == "-I" and
                isinstance(start[2], ast.Constant) and start[2].value == "-B" and
                isinstance(start[3], ast.Name) and start[3].id == "revexec_path"):
            return False, "%s does not invoke the extracted revexec.py" % fname
        literals = {node.value for node in ast.walk(ast.Module(body=[ast.Expr(value=argv)],
                                                               type_ignores=[]))
                    if isinstance(node, ast.Constant) and isinstance(node.value, str)}
        if not required.issubset(literals):
            return False, "%s command omits required revexec arguments" % fname
    for owner, node in calls:
        if not node.args or not isinstance(node.args[0], ast.Name) or node.args[0].id != "argv":
            return False, "%s subprocess.run does not execute its reviewed argv" % owner
    return True, "AST confines Python subprocess execution to revexec wrappers; other child is literal Git"


def _s_d6b(ctx):
    git, rev = ctx["git"], ctx["rev"]
    source = git.blob(rev, ROUTED_TOOL)
    if source is None:
        return False, "routed-r19.py absent at REV for AST self-check"
    ast_ok, ast_why = _subprocess_ast_ok(_text(source))
    if not ast_ok:
        return False, ast_why
    if not ctx["revexec_ready"]:
        return False, ctx["revexec_why"]
    return True, ast_why + "; " + ctx["revexec_why"]


def _citation_fixture(root, tmp, rev, slug, symlink_escape=False):
    base = os.path.join(tmp, "d6c-" + hashlib.sha256(slug.encode()).hexdigest()[:10])
    snapshots = os.path.join(base, "snapshots")
    os.makedirs(snapshots)
    digest_value = b"safe snapshot\n"
    if symlink_escape:
        outside = os.path.join(base, "outside.txt")
        with open(outside, "wb") as fh:
            fh.write(digest_value)
        os.symlink(outside, os.path.join(snapshots, slug))
    elif "/" not in slug and ".." not in slug:
        with open(os.path.join(snapshots, slug), "wb") as fh:
            fh.write(digest_value)
    table = {"entries": [{"id": "slug-fixture", "kind": "exact",
                           "file": "@" + slug, "line": 1,
                           "must_match": "safe snapshot"}]}
    table_bytes = (json.dumps(table, separators=(",", ":")) + "\n").encode()
    table_path = os.path.join(base, "table.json")
    expected_path = os.path.join(base, "expected.json")
    with open(table_path, "wb") as fh:
        fh.write(table_bytes)
    expected = {"pointer_table": {"sha256": hashlib.sha256(table_bytes).hexdigest()},
                "snapshots": {slug: hashlib.sha256(digest_value).hexdigest()}}
    with open(expected_path, "w", encoding="utf-8") as fh:
        json.dump(expected, fh)
    return ["--root", root, "--rev", rev, "--table", table_path,
            "--expected", expected_path, "--snapshot-dir", snapshots,
            "--strict"]


def _s_d6c(ctx):
    git, root, rev, tmp = ctx["git"], ctx["root"], ctx["rev"], ctx["tmp"]
    cases = (("../x", False), ("a/b", False), ("escape", True))
    for slug, symlink_escape in cases:
        args = _citation_fixture(root, tmp, rev, slug, symlink_escape)
        result, err = _run_tool(git, root, tmp, rev, rev, CITATION_PROBE, args)
        if err:
            return False, err
        text = _combined(result)
        if result["returncode"] != 2 or not re.search(r"\bslug_unsafe\b", text):
            return False, "citation slug %r did not refuse exit 2 with slug_unsafe" % slug
    return True, "slug_unsafe exit 2 for ../x, a/b, and symlink escape fixture"


def _s_d6d(ctx):
    git, root, rev, tmp = ctx["git"], ctx["root"], ctx["rev"], ctx["tmp"]
    receipt_path = os.path.join(tmp, "d6d-receipt.json")
    carrier_path = os.path.join(tmp, "carrier.bin")
    stdout_path = os.path.join(tmp, "stdout.log")
    stderr_path = os.path.join(tmp, "stderr.log")
    for path in (carrier_path, stdout_path, stderr_path):
        with open(path, "wb") as fh:
            fh.write(b"")
    empty_sha = hashlib.sha256(b"").hexdigest()
    receipt = {
        "label": "analyze-token-decoy",
        "carrier": {"path": carrier_path, "sha256": empty_sha, "size": 0},
        "steps": [{
            "step": "inspect-go-binary",
            "argv": ["npx", "-y", "rea-agents@6.5.0", "inspect-go-binary",
                     "--", "analyze"],
            "cwd": tmp, "exit": 0,
            "stdout_path": stdout_path, "stdout_sha256": empty_sha,
            "stderr_path": stderr_path, "stderr_sha256": empty_sha,
        }],
        "retained_logs": [], "bound_sessions": [],
        "pins_pre": {"entries": {}}, "pins_post": {"entries": {}},
        "pins_compare": {"equal": True, "changed": [], "missing": []},
    }
    with open(receipt_path, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh)
    result, err = _run_tool(git, root, tmp, rev, rev, RECEIPT_VALIDATE,
                            ["--require-mid-maps", receipt_path], extras=(PINS,))
    if err:
        return False, err
    text = _combined(result)
    data = _json_bytes(result["stdout"])
    if (result["returncode"] != 1 or
            not (_has_code(data, "analyze_step_unauthenticated") or
                 "analyze_step_unauthenticated" in text)):
        return False, "decoy analyze token was not rejected as analyze_step_unauthenticated"
    return True, "receipt validator rejected analyze outside the post-package argv position"


def _s_d6e(ctx):
    git, root, rev, tmp = ctx["git"], ctx["root"], ctx["rev"], ctx["tmp"]
    source = git.blob(rev, WAVE_OUTCOMES)
    if source is None:
        return False, "%s absent at REV" % WAVE_OUTCOMES
    if not _selftest_has_case(_text(source), "_selftest", "seat_named_causes"):
        return False, "wave-outcomes selftest lacks the seat_named_causes fixture"
    result, err = _run_tool(git, root, tmp, rev, rev, WAVE_OUTCOMES,
                            ["--selftest"])
    if err:
        return False, err
    text = _combined(result)
    if result["returncode"] != 0 or "SELFTEST: CLEAN" not in text:
        return False, "wave-outcomes selftest was not CLEAN exit 0"
    return True, "seat_named_causes selftest fixture passed"


def _case_ids(text):
    return set(re.findall(r"\bjj_[A-Za-z0-9][A-Za-z0-9_-]*\b", text))


def _s_d6f(ctx):
    git, root, rev, tmp = ctx["git"], ctx["root"], ctx["rev"], ctx["tmp"]
    extras = (REVPIN,)
    current, err = _run_tool(git, root, tmp, rev, rev, JJ_RED_BEFORE,
                             ["--selftest"], extras=extras, timeout=360)
    if err:
        return False, err
    current_text = _combined(current)
    if current["returncode"] != 0 or "SELFTEST: CLEAN" not in current_text:
        return False, "jj-red-before selftest at REV was not CLEAN exit 0"
    baseline, err = _run_tool(git, root, tmp, rev, BASELINE, JJ_RED_BEFORE,
                              ["--selftest"], extras=extras, timeout=360)
    if err:
        return False, err
    baseline_text = _combined(baseline)
    if baseline["returncode"] != 0 or "SELFTEST: CLEAN" not in baseline_text:
        return False, "jj-red-before baseline selftest was not CLEAN exit 0"
    current_ids, baseline_ids = _case_ids(current_text), _case_ids(baseline_text)
    if len(current_ids) < len(baseline_ids) + 2:
        return False, "jj_ case ids at REV=%d baseline=%d; need at least two more" % (
            len(current_ids), len(baseline_ids))
    return True, "jj-red-before selftest CLEAN; jj_ case ids %d at REV vs %d at baseline" % (
        len(current_ids), len(baseline_ids))


SUBSTANCE = {
    "D1": _s_d1,
    "D2": _s_d2,
    "D3": _s_d3,
    "D4": _s_d4,
    "D5": _s_d5,
    "D6a": _s_d6a,
    "D6b": _s_d6b,
    "D6c": _s_d6c,
    "D6d": _s_d6d,
    "D6e": _s_d6e,
    "D6f": _s_d6f,
}


def measure(root, rev, live=False):
    if not root or not os.path.isdir(root):
        raise CounterError("root_unreadable: --root must name a directory")
    git = GitObjects(root)
    resolved = git.resolve(rev)
    names = _named(git, resolved)
    tmp = _tmp_root(root, "routed-r19-")
    try:
        revexec_ready, revexec_why = _revexec_preflight(git, resolved, tmp)
        items = []
        ctx = {"git": git, "root": git.root, "rev": resolved,
               "tmp": tmp, "live": live, "revexec_ready": revexec_ready,
               "revexec_why": revexec_why}
        for item in ITEMS:
            named, score_ok, lesson_ok = names[item]
            try:
                substance, substance_why = SUBSTANCE[item](ctx)
            except Exception as exc:
                substance, substance_why = False, "check error: %s: %s" % (
                    type(exc).__name__, exc)
            why = []
            if not named:
                missing = []
                if not score_ok:
                    missing.append("SCORECARD.md name missing")
                if not lesson_ok:
                    missing.append("round-20 lesson name missing")
                why.extend(missing)
            if not substance:
                why.append(substance_why)
            if not why:
                why.append("both name and substance checks passed")
            items.append({"id": item, "named": bool(named),
                          "substance": bool(substance), "why": "; ".join(why)})
        named_open = sum(1 for item in items if not item["named"])
        substance_open = sum(1 for item in items if not item["substance"])
        open_count = sum(1 for item in items
                         if not (item["named"] and item["substance"]))
        return {"rev": resolved, "open_count": open_count,
                "named_open": named_open, "substance_open": substance_open,
                "items": items}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

def _exit_code(result, strict):
    return 1 if strict and result["open_count"] else 0


def _selftest():
    tmp = _tmp_root(None, "routed-r19-selftest-")
    cases = []
    try:
        repo = os.path.join(tmp, "fixture-lane")
        os.makedirs(repo)
        rc, _out, err = _fixture_git(repo, ["init", "-q", "-b", "main"])
        if rc != 0:
            raise CounterError("fixture_git_init: %s" % _text(err).strip())
        os.makedirs(os.path.join(repo, "corpus", "lessons"))
        os.makedirs(os.path.join(repo, ".ufo", "waves", "round-20", "evidence"))
        score = "# scorecard\n" + "".join(
            "- R19-%s: named token-only claim\n" % item for item in ITEMS)
        lesson = "# round 20\n" + "".join(
            "- R19-%s: named token-only claim\n" % item for item in ITEMS)
        Path(os.path.join(repo, SCORECARD)).write_text(score, encoding="utf-8")
        Path(os.path.join(repo, LESSON)).write_text(lesson, encoding="utf-8")
        Path(os.path.join(repo, W20, "evidence", "token-only.txt")).write_text(
            "SELFTEST: CLEAN future_dated exec_refused mode_restored "
            "VERDICT: PASS slug_unsafe analyze_step_unauthenticated "
            "seat_named_causes jj_added_case\n", encoding="utf-8")
        rev_all_named = _commit_fixture(repo, "all names plus token-only text")
        result = measure(repo, rev_all_named)
        case_ok = (result["open_count"] == len(ITEMS) and
                   result["named_open"] == 0 and
                   result["substance_open"] == len(ITEMS) and
                   all(not row["substance"] for row in result["items"]))
        cases.append(("token_only_closures_stay_open", case_ok))

        Path(os.path.join(repo, LESSON)).write_text(
            "# round 20\n" + "".join(
                "- R19-%s: named token-only claim\n" % item
                for item in ITEMS if item != "D6f"), encoding="utf-8")
        rev_missing_name = _commit_fixture(repo, "one named correction absent")
        missing = measure(repo, rev_missing_name)
        cases.append(("missing_name_counts_open",
                      missing["open_count"] == len(ITEMS) and
                      missing["named_open"] == 1 and
                      missing["substance_open"] == len(ITEMS) and
                      next(row for row in missing["items"] if row["id"] == "D6f")["named"] is False))
        strict_code = _exit_code(result, True)
        cases.append(("strict_open_exit", strict_code == 1))
        try:
            source = Path(__file__).read_text(encoding="utf-8")
            ast_ok, _why = _subprocess_ast_ok(source)
        except OSError:
            ast_ok = False
        cases.append(("ast_revexec_only", ast_ok))
    except Exception as exc:
        print("SELFTEST: FAILED setup %s: %s cases=%d fails=1" % (
            type(exc).__name__, exc, len(cases)))
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    failures = [name for name, ok in cases if not ok]
    for name, ok in cases:
        print("SELFTEST_CASE: %s case=%s" % ("CLEAN" if ok else "FAILED", name))
    if failures:
        print("SELFTEST: FAILED cases=%d fails=%d (%s)" % (
            len(cases), len(failures), ", ".join(failures)))
        return 1
    print("SELFTEST: CLEAN cases=%d" % len(cases))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Count round-19 routed defects at an immutable Git revision.")
    parser.add_argument("--root")
    parser.add_argument("--rev")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--live", action="store_true",
                        help="also inspect the current LANE/.ufo for nested .git residue")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return _selftest()
    if not args.root or not args.rev:
        print("REFUSED root_rev_required: --root and --rev are required", file=sys.stderr)
        return 2
    try:
        result = measure(args.root, args.rev, live=args.live)
    except CounterError as exc:
        print("REFUSED %s" % exc, file=sys.stderr)
        return 2
    except Exception as exc:
        print("REFUSED internal_error: %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return _exit_code(result, args.strict)


if __name__ == "__main__":
    sys.exit(main())
