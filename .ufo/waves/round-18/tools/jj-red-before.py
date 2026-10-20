#!/usr/bin/env python3
"""jj-red-before.py — throwaway jj-clone red/green probe for R18 C2.

Contract: .ufo/waves/round-18/contract.md, section "W18/tools/jj-red-before.py"
(lines 88-98), plus the L1 amendments of 2026-10-20 (sentinel/critic
findings): origin remote is removed right after clone and replaced by a fake
`refs/remotes/origin/main` ref, so nothing in sb can push to the lane; all
sandbox trees are mkdtemp(dir="/tmp") and are refused under the lane or the
fleet root; every git/jj child gets an explicit scrubbed env (`run()` takes a
mandatory env, `os.environ` is scrubbed before the in-process revpin import,
and `main()` scrubs the process env at entry), so no GIT_*/JJ_*/TMPDIR value
reaches a child; jj gets sandboxed HOME/XDG_CONFIG_HOME with `-R sb` on every
call after init; a pointer-table entry path or marker that resolves outside
the mkdtemp clone is refused with exit 2 and a named cause before any write;
the off-branch commit rewrites a pointer-table-cited line so the baseline red is
a real `citation_dead` finding, not just the printed rev; and a state-D0
pass (jj steady state, detached at the tip — the lane's current shape)
checks the fixed forms do not falsely refuse.

Sandbox (built under tempfile.mkdtemp(dir="/tmp"), removed unconditionally):

    git clone --no-local LANE sb
    git -C sb remote remove origin          # lane HEAD is detached; a push
    git -C sb remote                        # must print nothing (asserted)
    git -C sb update-ref refs/remotes/origin/main <tip>   # fake remote ref
    git -C sb checkout --quiet main         # ensure refs/heads/main exists
    jj --config user.name=... git init --colocate          # in sb
    (state D0: detached AT the branch tip — run no-refusal checks)
    rewrite one pointer-table-cited line + write a marker file
    jj --config ... -R sb commit -m off      # never moves `main`
    (state D1: HEAD is an off-branch commit — run the red/green matrix)

Steps (argv/exit/stdout/stderr retained verbatim in the receipt):

    d0-*                                 fixed forms + rev-parse + revpin at
                                         detached-at-tip: no false refusal
    baseline-citation-drift              `git show B:.../probe.py` to a temp
                                         file; run --root sb, no --rev, with
                                         --table/--expected pointed at sb's
                                         own gate files -> red: evaluates
                                         HEAD and reports the cited-line
                                         citation_dead finding
    baseline-citation-drift-finding      the cited-line finding is present in
                                         that run's findings
    baseline-citation-drift-control      same probe at --rev refs/heads/main:
                                         the cited-line finding is absent
    fixed-citation-drift                 LANE working-tree probe, no --rev:
                                         green iff rev_resolved == main tip
    fixed-citation-drift-rev-head        --rev HEAD: green iff exit 2 with
                                         head_not_branch_tip
    baseline-custody-capture             baseline custody-pair capture with
                                         cwd=sb -> red: repo-HEAD names the
                                         off-branch commit
    fixed-custody-capture                fixed custody-pair capture --repo sb
                                         -> green: repo-HEAD-is-branch-tip:
                                         no, repo-branch-tip == main tip
    baseline-rev-parse-head              `git -C sb rev-parse HEAD` -> red:
                                         the off-branch sha
    revpin-resolve-source                revpin.resolve_source(sb) in-process
                                         -> green iff RevPinError
                                         head_not_branch_tip
    lane-tip-unchanged                   lane refs/heads/main before == after
                                         (no lane write from the sandbox)

A fixed tool whose contract markers are not yet present in the LANE working
tree is reported not_runnable (held null) instead of executing a stale
pre-fix binary as if it were the fixed one. Exit 0 all held, 1 any runnable
step not held, 2 setup failure or every step blocked. Stdlib only.

`--selftest` builds a fixture lane and stub tools under mkdtemp(dir="/tmp"):
one all-green case, a regressed fixed citation-drift probe that resolves
HEAD like the baseline (must fail), a regressed fixed capture that omits the
is-branch-tip flag (must fail), an absent-fixed-tools case (must report
not_runnable, never held), and three red safety cases: a sentinel GIT_*/JJ_*
parent env observed through a shimmed git (no child may see it, the fixture
builder included), and pointer-table entries naming an absolute path, a `..`
walk and a symlink out of the clone (each must refuse exit 2 with a named
cause and leave the outside file byte-identical).
"""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE_DEFAULT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FLEET_ROOT = "/home/vgpnk/Projects/shokunin"
BASELINE_B = "9011581d84527ba34c675f9cf912e54d2e72d470"
CD_REL = ".ufo/gates/citation-drift/citation-drift-probe.py"
CP_REL = ".ufo/gates/custody-pair/custody-pair.py"
REVPIN_REL = ".ufo/waves/round-18/tools/revpin.py"
TABLE_REL = ".ufo/gates/citation-drift/pointer-table.json"
EXPECTED_REL = ".ufo/gates/citation-drift/expected.json"
MARKER_NAME = "JJ_RED_BEFORE_MARKER.txt"

CLEAN, FAILED, CNE = 0, 1, 2

# Fixed-tool readiness markers: bytes only the contract-fixed versions carry.
# Absence means the LANE file is still the pre-fix binary -> not_runnable.
CD_FIXED_MARKERS = (b"rev_resolved",)
CP_FIXED_MARKERS = (b"--repo", b"repo-HEAD-is-branch-tip")
REVPIN_MARKERS = (b"def resolve_source", b"RevPinError")


def _refuse_inside(path):
    """Absolute path must not live under the lane or the fleet root."""
    real = os.path.realpath(path)
    for forbidden in (LANE_DEFAULT, FLEET_ROOT):
        if real == forbidden or real.startswith(forbidden + os.sep):
            raise RuntimeError("refusing path inside %s: %s" % (forbidden, path))


def _dirty_key(key):
    """Environment keys that would redirect a git/jj child off the sandbox."""
    return key.startswith("GIT_") or key.startswith("JJ_") or key == "TMPDIR"


def _child_env(tmp, for_jj=False):
    """Scrubbed environment: no GIT_*/JJ_*/TMPDIR leakage into children."""
    env = {k: v for k, v in os.environ.items() if not _dirty_key(k)}
    if for_jj:
        home = os.path.join(tmp, "jj-home")
        xdg = os.path.join(tmp, "jj-xdg")
        os.makedirs(home, exist_ok=True)
        os.makedirs(xdg, exist_ok=True)
        env["HOME"] = home
        env["XDG_CONFIG_HOME"] = xdg
    return env


@contextlib.contextmanager
def _scrubbed_process_env():
    """Strip GIT_*/JJ_*/TMPDIR from os.environ for the duration of an
    in-process import whose own git children would otherwise inherit them."""
    saved = {k: os.environ.pop(k) for k in list(os.environ) if _dirty_key(k)}
    try:
        yield
    finally:
        os.environ.update(saved)


class SandboxRefusal(RuntimeError):
    """Named refusal: the probe would have to write outside its clone."""

    def __init__(self, cause, **detail):
        self.cause = cause
        self.detail = detail
        super().__init__("%s: %s" % (cause, json.dumps(detail, sort_keys=True)))


def _inside(sb, rel):
    """True iff rel names a path strictly inside sb (absolute and `..`
    escapes and symlinks that resolve outside are all rejected)."""
    if not isinstance(rel, str) or not rel or os.path.isabs(rel):
        return False
    base = os.path.realpath(sb)
    target = os.path.realpath(os.path.join(sb, rel))
    return target.startswith(base + os.sep)


def _guard_table_paths(sb, table):
    """Refuse any pointer-table entry that names a path outside the clone.

    Entries are lane-committed data; a `file` value is the only table field
    that steers a write, so it is checked before the entry can be selected,
    including entries the selection loop would never reach."""
    if not isinstance(table, dict):
        return
    for entry in table.get("entries", []):
        if not isinstance(entry, dict):
            continue
        rel = entry.get("file")
        if isinstance(rel, str) and rel and not rel.startswith("@") \
                and not _inside(sb, rel):
            raise SandboxRefusal("pointer_table_path_outside_sandbox",
                                 file=rel, sandbox=sb, entry=entry.get("id"))


def run(argv, cwd, env, timeout=300):
    """Run argv with an explicit cwd and a mandatory explicit child env;
    never raises. Retained step dict."""
    if env is None:
        raise TypeError("run() requires an explicit scrubbed env")
    rec = {"argv": list(argv), "cwd": cwd}
    try:
        p = subprocess.run(list(argv), cwd=cwd, env=env, capture_output=True,
                           text=True, timeout=timeout)
        rec["exit"] = p.returncode
        rec["stdout"] = p.stdout
        rec["stderr"] = p.stderr
    except Exception as exc:  # FileNotFoundError, TimeoutExpired, ...
        rec["exit"] = None
        rec["stdout"] = ""
        rec["stderr"] = "%s: %s" % (type(exc).__name__, exc)
    return rec


def run_expr(name, fn):
    """Retained record for an in-process expression (no subprocess). The
    expression runs under a scrubbed os.environ so any git child it spawns
    itself inherits no GIT_*/JJ_* value from the caller."""
    rec = {"argv": [name], "cwd": None, "exit": None,
           "stdout": "", "stderr": ""}
    try:
        with _scrubbed_process_env():
            rec["result"] = fn()
        rec["raised"] = None
    except Exception as exc:
        rec["result"] = None
        rec["raised"] = "%s: %s" % (type(exc).__name__, exc)
    return rec


def sha_of(root, rev, cwd, env):
    r = run(["git", "-C", root, "rev-parse", "--verify", "--quiet",
             rev + "^{commit}"], cwd=cwd, env=env)
    if r["exit"] != 0 or not r["stdout"].strip():
        return None
    return r["stdout"].strip().splitlines()[0]


def git_show(root, rev_path, cwd, env):
    r = run(["git", "-C", root, "show", rev_path], cwd=cwd, env=env)
    if r["exit"] != 0:
        return None, r
    return r["stdout"], r


def file_has_markers(path, markers):
    try:
        data = Path(path).read_bytes()
    except OSError:
        return False
    return all(m in data for m in markers)


def field_line(text, name):
    m = re.search(r"^#\s*%s:\s*(.*)$" % re.escape(name), text, re.M)
    return m.group(1).strip() if m else None


def probe_resolved_rev(stdout):
    """Pull the evaluated revision out of a citation-drift probe run."""
    try:
        obj = json.loads(stdout)
        if isinstance(obj, dict):
            return (obj.get("rev_resolved"), obj.get("rev_requested"),
                    obj.get("branch"))
    except (ValueError, TypeError):
        pass
    def _line(tag):
        m = re.search(r"^CITATION_DRIFT_%s:\s*(.*)$" % tag, stdout, re.M)
        return m.group(1).strip() if m else None
    # Baseline prints CITATION_DRIFT_REVISION (the --rev string it evaluated);
    # the fixed probe prints CITATION_DRIFT_REV_RESOLVED (the resolved sha).
    resolved = _line("REV_RESOLVED") or _line("REVISION")
    return resolved, _line("REV_REQUESTED"), _line("BRANCH")


def pick_cited_line(sb):
    """Choose (file, 1-based line, needle) the pointer table cites, so the
    off-branch commit can rewrite it and the baseline red lands in findings.
    Falls back to SCORECARD.md line 1 when the table has no usable entry."""
    try:
        table = json.loads(Path(sb, TABLE_REL).read_text())
    except (OSError, ValueError):
        table = {}
    if not isinstance(table, dict):
        table = {}
    _guard_table_paths(sb, table)
    for e in table.get("entries", []):
        if not isinstance(e, dict):
            continue
        if e.get("kind") in ("exact", "quoted") \
                and isinstance(e.get("line"), int) \
                and e.get("must_match") and e.get("file") \
                and Path(sb, e["file"]).is_file():
            return e["file"], e["line"], e.get("id", "?")
    return "SCORECARD.md", 1, "fallback-line-1"


# --------------------------------------------------------------------------
# sandbox construction (contract lines 89-91 + L1 amendments)
# --------------------------------------------------------------------------

def build_sandbox(lane, branch, jj):
    """Return (tmp, sb, main_sha, head_sha_D0, setup) or raise RuntimeError.

    The mkdtemp root is removed here when construction fails before the
    caller owns it, so a failed setup leaves nothing behind."""
    tmp = tempfile.mkdtemp(prefix="jj-red-before-", dir="/tmp")
    try:
        return _build_sandbox_in(tmp, lane, branch, jj)
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)
        raise


def _build_sandbox_in(tmp, lane, branch, jj):
    _refuse_inside(tmp)
    sb = os.path.join(tmp, "sb")
    env = _child_env(tmp)
    jjenv = _child_env(tmp, for_jj=True)
    setup = []

    setup.append(run(["git", "clone", "--no-local", lane, sb],
                     cwd=tmp, env=env))
    if setup[-1]["exit"] != 0:
        raise RuntimeError("git clone --no-local failed: "
                           + setup[-1]["stderr"][:200])

    # L1 amendment (1): the lane's HEAD is detached, so a push from sb could
    # move the lane's main. Remove origin entirely, assert no remotes, then
    # re-create a fake refs/remotes/origin/main so pushed checks have a
    # target that can never be written through.
    tip = sha_of(sb, "refs/remotes/origin/" + branch, tmp, env) \
        or sha_of(sb, "HEAD", tmp, env)  # head-rev-lint: red-before
    if tip is None:
        raise RuntimeError("clone exposes no tip for " + branch)
    setup.append(run(["git", "-C", sb, "remote", "remove", "origin"],
                     cwd=tmp, env=env))
    setup.append(run(["git", "-C", sb, "remote"], cwd=tmp, env=env))
    if setup[-1]["exit"] != 0 or setup[-1]["stdout"].strip():
        raise RuntimeError("remotes remain in sb after remote remove: %r"
                           % setup[-1]["stdout"])
    setup.append(run(["git", "-C", sb, "update-ref",
                      "refs/remotes/origin/" + branch, tip],
                     cwd=tmp, env=env))
    if setup[-1]["exit"] != 0:
        raise RuntimeError("fake origin ref update-ref failed")
    if sha_of(sb, "refs/heads/" + branch, tmp, env) is None:
        setup.append(run(["git", "-C", sb, "update-ref",
                          "refs/heads/" + branch, tip], cwd=tmp, env=env))
    setup.append(run(["git", "-C", sb, "checkout", "--quiet", branch],
                     cwd=tmp, env=env))

    cfg = ["--config", "user.name=JJ Red Before",
           "--config", "user.email=jj-red-before@example.invalid"]
    setup.append(run([jj, *cfg, "git", "init", "--colocate"],
                     cwd=sb, env=jjenv))
    if setup[-1]["exit"] != 0:
        raise RuntimeError("jj git init --colocate failed: "
                           + setup[-1]["stderr"][:200])

    main_sha = sha_of(sb, "refs/heads/" + branch, tmp, env)
    head_d0 = sha_of(sb, "HEAD", tmp, env)  # head-rev-lint: red-before
    if main_sha is None or head_d0 is None:
        raise RuntimeError("sandbox refs unresolvable after jj init")
    return tmp, sb, main_sha, head_d0, setup


def commit_off_branch(sb, main_sha, jj, tmp, setup):
    """Rewrite one pointer-table-cited line + a marker file; `jj commit -m
    off` lands it as the working-copy parent (off-branch HEAD). Returns
    (head_sha, mutation) where mutation records the cited file/line."""
    cited_file, cited_line, entry_id = pick_cited_line(sb)
    # Re-check at the write site: the fallback target and any symlink that
    # resolves out of the clone must refuse before a byte is written.
    if not _inside(sb, cited_file):
        raise SandboxRefusal("pointer_table_path_outside_sandbox",
                             file=cited_file, sandbox=sb)
    if os.path.islink(os.path.join(sb, cited_file)):
        raise SandboxRefusal("pointer_table_path_symlink",
                             file=cited_file, sandbox=sb)
    marker = Path(sb, MARKER_NAME)
    if not _inside(sb, MARKER_NAME) or os.path.islink(str(marker)):
        raise SandboxRefusal("marker_path_outside_sandbox",
                             file=MARKER_NAME, sandbox=sb)
    target = Path(sb, cited_file)
    lines = target.read_text().splitlines(keepends=True)
    if 1 <= cited_line <= len(lines):
        ending = "\n" if lines[cited_line - 1].endswith("\n") else ""
        lines[cited_line - 1] = ("OFF-BRANCH REWRITE by jj-red-before "
                                 "(was a pointer-table-cited line)" + ending)
        target.write_text("".join(lines))
        mutation = {"file": cited_file, "line": cited_line,
                    "entry_id": entry_id}
    else:
        mutation = {"file": None, "line": None, "entry_id": entry_id,
                    "note": "cited line out of range; marker only"}
    marker.write_text(
        "off-branch working-copy content; never committed to %s\n" % main_sha)

    cfg = ["--config", "user.name=JJ Red Before",
           "--config", "user.email=jj-red-before@example.invalid"]
    jjenv = _child_env(tmp, for_jj=True)
    setup.append(run([jj, *cfg, "-R", sb, "commit", "-m", "off"],
                     cwd=sb, env=jjenv))
    if setup[-1]["exit"] != 0:
        raise RuntimeError("jj commit -m off failed: "
                           + setup[-1]["stderr"][:200])
    head_sha = sha_of(sb, "HEAD", tmp, _child_env(tmp))  # head-rev-lint: red-before
    if head_sha is None:
        raise RuntimeError("sandbox HEAD unresolvable after jj commit")
    return head_sha, mutation


# --------------------------------------------------------------------------
# the probe matrix
# --------------------------------------------------------------------------

def evaluate(lane, baseline_rev, branch, jj, cd_fixed, cp_fixed, revpin_path):
    """Build the sandbox, run every step, return (receipt, exit_code)."""
    steps = []
    expectations = []
    baseline_extracts = []
    skipped = []
    env_tmp = None

    def step(name, rec, extra=None):
        rec = dict(rec)
        rec["step"] = name
        if extra:
            rec.update(extra)
        steps.append(rec)
        return rec

    def expect(name, expected, observed, held):
        expectations.append({"name": name, "expected": expected,
                             "observed": observed, "held": held})

    # Lane tip before any sandbox work; rechecked at the end to prove the
    # sandbox never wrote the lane (L1 amendment 6).
    pre_env = _child_env(tempfile.gettempdir())
    lane_tip_before = sha_of(lane, "refs/heads/" + branch,
                             tempfile.gettempdir(), pre_env)

    try:
        tmp, sb, main_sha, head_d0, setup = build_sandbox(lane, branch, jj)
    except Exception as exc:
        receipt = {"tool": "jj-red-before", "lane": lane, "branch": branch,
                   "baseline_rev": baseline_rev,
                   "setup_error": "%s: %s" % (type(exc).__name__, exc),
                   "steps": steps, "expectations": expectations,
                   "not_runnable": skipped, "all_held": False}
        return receipt, CNE
    env_tmp = tmp
    try:
        env = _child_env(tmp)
        cd_ok = file_has_markers(cd_fixed, CD_FIXED_MARKERS)
        cp_ok = file_has_markers(cp_fixed, CP_FIXED_MARKERS)
        revpin_ok = file_has_markers(revpin_path, REVPIN_MARKERS)
        table = os.path.join(sb, TABLE_REL)
        expected = os.path.join(sb, EXPECTED_REL)

        setup_ok = {"sb": sb, "branch": branch, "main_sha": main_sha,
                    "head_sha_d0": head_d0, "commands": setup}

        # ==================== state D0: detached AT the tip ==============
        # jj steady state (the lane's current shape): HEAD == main tip.
        rec = run(["git", "-C", sb, "rev-parse", "HEAD"], cwd=tmp,  # head-rev-lint: red-before
                  env=env)
        d0_head = rec["stdout"].strip()
        step("d0-rev-parse-head", rec,
             {"observed": {"head_sha": d0_head, "main_sha": main_sha}})
        expect("d0-rev-parse-head",
               "HEAD == %s tip %s (jj steady state, detached at tip)"
               % (branch, main_sha),
               {"head_sha": d0_head, "main_sha": main_sha},
               d0_head == main_sha)

        if cd_ok:
            rec = run([sys.executable, "-I", "-B", cd_fixed, "--root", sb,
                       "--rev", "HEAD",  # head-rev-lint: red-before
                       "--table", table, "--expected", expected],
                      cwd=tmp, env=env)
            blob = (rec["stdout"] or "") + (rec["stderr"] or "")
            refused = rec["exit"] == 2 and "head_not_branch_tip" in blob
            step("d0-fixed-citation-drift-rev-head", rec,
                 {"observed": {"exit": rec["exit"], "refused": refused}})
            expect("d0-fixed-citation-drift-rev-head",
                   "no false refusal at detached-at-tip: --rev HEAD exits 0",
                   {"exit": rec["exit"], "refused": refused},
                   rec["exit"] == 0 and refused is False)
        else:
            skipped.append("d0-fixed-citation-drift-rev-head")
            expect("d0-fixed-citation-drift-rev-head",
                   "no false refusal at detached-at-tip",
                   "not_runnable: %s lacks fixed markers" % cd_fixed, None)

        if cp_ok:
            rcp = os.path.join(tmp, "d0-custody-receipt.txt")
            rec = run([sys.executable, "-I", "-B", cp_fixed, "capture",
                       "--repo", sb, "--out", rcp,
                       "--label", "jj-red-before-d0",
                       "--paths", os.path.join(sb, "LOG.md"),
                       os.path.join(sb, "SCORECARD.md")],
                      cwd=tmp, env=env)
            text = ""
            try:
                text = Path(rcp).read_text()
            except OSError:
                pass
            obs = {"is_tip": field_line(text, "repo-HEAD-is-branch-tip"),
                   "repo_branch_tip": field_line(text, "repo-branch-tip")}
            step("d0-fixed-custody-capture", rec, {"observed": obs})
            expect("d0-fixed-custody-capture",
                   "at detached-at-tip: repo-HEAD-is-branch-tip: yes",
                   obs, obs["is_tip"] == "yes")
        else:
            skipped.append("d0-fixed-custody-capture")
            expect("d0-fixed-custody-capture",
                   "at detached-at-tip: repo-HEAD-is-branch-tip: yes",
                   "not_runnable: %s lacks fixed markers" % cp_fixed, None)

        if revpin_ok:
            def _resolve_d0():
                spec = importlib.util.spec_from_file_location(
                    "jj_red_before_revpin_d0", revpin_path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod.resolve_source(sb)
            rec = run_expr("revpin.resolve_source(%r) [D0]" % sb, _resolve_d0)
            res = rec["result"] or {}
            step("d0-revpin-resolve-source", rec,
                 {"observed": {"raised": rec["raised"], "result": res}})
            expect("d0-revpin-resolve-source",
                   "resolve_source returns clean at detached-at-tip "
                   "(head_equals_source, pushed)",
                   {"raised": rec["raised"],
                    "head_equals_source": res.get("head_equals_source"),
                    "pushed": res.get("pushed")},
                   rec["raised"] is None
                   and res.get("head_equals_source") is True
                   and res.get("pushed") is True)
        else:
            skipped.append("d0-revpin-resolve-source")
            expect("d0-revpin-resolve-source",
                   "resolve_source returns clean at detached-at-tip",
                   "not_runnable: %s lacks markers" % revpin_path, None)

        # ==================== transition to state D1 ======================
        try:
            head_sha, mutation = commit_off_branch(sb, main_sha, jj, tmp,
                                                 setup)
        except SandboxRefusal as exc:
            receipt = {"tool": "jj-red-before", "lane": lane,
                       "branch": branch, "baseline_rev": baseline_rev,
                       "setup": setup_ok, "refusal": exc.cause,
                       "refusal_detail": exc.detail,
                       "setup_error": "%s: %s" % (type(exc).__name__, exc),
                       "steps": steps, "expectations": expectations,
                       "not_runnable": skipped, "all_held": False}
            return receipt, CNE
        except Exception as exc:
            receipt = {"tool": "jj-red-before", "lane": lane,
                       "branch": branch, "baseline_rev": baseline_rev,
                       "setup": setup_ok,
                       "setup_error": "%s: %s" % (type(exc).__name__, exc),
                       "steps": steps, "expectations": expectations,
                       "not_runnable": skipped, "all_held": False}
            return receipt, CNE
        setup_ok["head_sha_d1"] = head_sha
        setup_ok["mutation"] = mutation
        off_branch = head_sha != main_sha
        if not off_branch:
            receipt = {"tool": "jj-red-before", "lane": lane,
                       "branch": branch, "baseline_rev": baseline_rev,
                       "setup": setup_ok,
                       "setup_error": "sandbox HEAD equals branch tip after "
                                      "jj commit -m off; no off-branch HEAD",
                       "steps": steps, "expectations": expectations,
                       "not_runnable": skipped, "all_held": False}
            return receipt, CNE

        # -- extraction steps: baseline tools out of Git objects at B ------
        cd_base_path = os.path.join(tmp, "baseline-citation-drift-probe.py")
        cp_base_path = os.path.join(tmp, "baseline-custody-pair.py")
        for rel, dest in ((CD_REL, cd_base_path), (CP_REL, cp_base_path)):
            text, rec = git_show(lane, "%s:%s" % (baseline_rev, rel),
                                 tmp, env)
            rec = dict(rec)
            rec["bytes"] = len(text.encode()) if text is not None else 0
            rec["extracted_to"] = dest
            if text is not None:
                Path(dest).write_text(text)
            baseline_extracts.append(step("extract-baseline:" + rel, rec))
            if text is None:
                skipped.append("extract-baseline:" + rel)

        needle = ("%s:%d" % (mutation["file"], mutation["line"])
                  if mutation["file"] else None)

        # == D1 step: baseline citation-drift, no --rev (red expected) =====
        if os.path.exists(cd_base_path):
            rec = run([sys.executable, "-I", "-B", cd_base_path, "--root", sb,
                       "--table", table, "--expected", expected],
                      cwd=tmp, env=env)
            resolved, _req, _br = probe_resolved_rev(rec["stdout"])
            finding_hit = bool(needle) and any(
                needle in l for l in rec["stdout"].splitlines()
                if l.startswith("CITATION_DRIFT:"))
            step("baseline-citation-drift", rec,
                 {"observed": {"reported_rev": resolved,
                               "head_sha": head_sha, "main_sha": main_sha,
                               "cited_finding": finding_hit}})
            expect("baseline-citation-drift",
                   "probe evaluates HEAD (the off-branch commit): red",
                   {"reported_rev": resolved, "head_sha": head_sha,
                    "head_is_off_branch": off_branch},
                   resolved == "HEAD" and off_branch)
            expect("baseline-citation-drift-finding",
                   "cited-line finding %s appears in findings (off-branch "
                   "content, not just the printed rev)" % needle,
                   {"needle": needle, "found": finding_hit},
                   finding_hit)

            rec = run([sys.executable, "-I", "-B", cd_base_path, "--root", sb,
                       "--rev", "refs/heads/" + branch,
                       "--table", table, "--expected", expected],
                      cwd=tmp, env=env)
            resolved, _req, _br = probe_resolved_rev(rec["stdout"])
            control_clean = not any(
                needle and needle in l for l in rec["stdout"].splitlines()
                if l.startswith("CITATION_DRIFT:"))
            step("baseline-citation-drift-control", rec,
                 {"observed": {"reported_rev": resolved,
                               "needle_absent": control_clean}})
            expect("baseline-citation-drift-control",
                   "at %s tip the cited-line finding %s is absent"
                   % (branch, needle),
                   {"reported_rev": resolved, "needle_absent": control_clean},
                   resolved == "refs/heads/" + branch and control_clean)
        else:
            skipped += ["baseline-citation-drift",
                        "baseline-citation-drift-finding",
                        "baseline-citation-drift-control"]
            for n in ("baseline-citation-drift",
                      "baseline-citation-drift-finding",
                      "baseline-citation-drift-control"):
                expect(n, "…", "not_runnable: baseline extract failed", None)

        # == D1 step: fixed citation-drift, no --rev (green expected) ======
        if cd_ok:
            rec = run([sys.executable, "-I", "-B", cd_fixed, "--root", sb,
                       "--table", table, "--expected", expected],
                      cwd=tmp, env=env)
            resolved, requested, fbranch = probe_resolved_rev(rec["stdout"])
            step("fixed-citation-drift", rec,
                 {"observed": {"rev_resolved": resolved,
                               "rev_requested": requested,
                               "branch": fbranch,
                               "main_sha": main_sha}})
            expect("fixed-citation-drift",
                   "no --rev resolves the %s tip %s" % (branch, main_sha),
                   {"rev_resolved": resolved, "exit": rec["exit"],
                    "branch": fbranch},
                   resolved == main_sha and rec["exit"] in (0, 1))
        else:
            skipped.append("fixed-citation-drift")
            expect("fixed-citation-drift",
                   "no --rev resolves the %s tip" % branch,
                   "not_runnable: %s lacks fixed markers %s or is absent"
                   % (cd_fixed, [m.decode() for m in CD_FIXED_MARKERS]),
                   None)

        # == D1 step: fixed citation-drift --rev HEAD (green: exit 2) ======
        if cd_ok:
            rec = run([sys.executable, "-I", "-B", cd_fixed, "--root", sb,
                       "--rev", "HEAD",  # head-rev-lint: red-before
                       "--table", table, "--expected", expected],
                      cwd=tmp, env=env)
            blob = (rec["stdout"] or "") + (rec["stderr"] or "")
            refused = rec["exit"] == 2 and "head_not_branch_tip" in blob
            step("fixed-citation-drift-rev-head", rec,
                 {"observed": {"exit": rec["exit"], "refused": refused}})
            expect("fixed-citation-drift-rev-head",
                   "--rev HEAD refused: exit 2 head_not_branch_tip",
                   {"exit": rec["exit"], "refused": refused}, refused)
        else:
            skipped.append("fixed-citation-drift-rev-head")
            expect("fixed-citation-drift-rev-head",
                   "--rev HEAD refused: exit 2 head_not_branch_tip",
                   "not_runnable: %s lacks fixed markers" % cd_fixed, None)

        # == D1 step: baseline custody-pair capture, cwd=sb (red) ==========
        measured = [p for p in (os.path.join(sb, "LOG.md"),
                              os.path.join(sb, "SCORECARD.md"))
                    if os.path.exists(p)] or \
            [os.path.join(sb, MARKER_NAME)]
        if os.path.exists(cp_base_path):
            rcp = os.path.join(tmp, "baseline-custody-receipt.txt")
            rec = run([sys.executable, "-I", "-B", cp_base_path, "capture",
                       "--out", rcp, "--label", "jj-red-before-baseline",
                       "--paths", *measured], cwd=sb, env=env)
            text = ""
            try:
                text = Path(rcp).read_text()
            except OSError:
                pass
            repo_head = field_line(text, "repo-HEAD")
            step("baseline-custody-capture", rec,
                 {"observed": {"repo_head": repo_head,
                               "head_sha": head_sha, "main_sha": main_sha}})
            expect("baseline-custody-capture",
                   "receipt repo-HEAD names the off-branch commit "
                   "(cwd-keyed): red",
                   {"repo_head": repo_head, "head_sha": head_sha,
                    "head_is_off_branch": off_branch},
                   repo_head == head_sha and off_branch)
        else:
            skipped.append("baseline-custody-capture")
            expect("baseline-custody-capture", "…",
                   "not_runnable: baseline extract failed", None)

        # == D1 step: fixed custody-pair capture --repo sb (green) =========
        if cp_ok:
            rcp = os.path.join(tmp, "fixed-custody-receipt.txt")
            rec = run([sys.executable, "-I", "-B", cp_fixed, "capture",
                       "--repo", sb, "--out", rcp,
                       "--label", "jj-red-before-fixed",
                       "--paths", *measured], cwd=tmp, env=env)
            text = ""
            try:
                text = Path(rcp).read_text()
            except OSError:
                pass
            obs = {
                "repo_root": field_line(text, "repo-root"),
                "repo_branch": field_line(text, "repo-branch"),
                "repo_branch_tip": field_line(text, "repo-branch-tip"),
                "repo_head": field_line(text, "repo-HEAD"),
                "is_tip": field_line(text, "repo-HEAD-is-branch-tip"),
            }
            step("fixed-custody-capture", rec, {"observed": obs})
            expect("fixed-custody-capture",
                   "receipt records repo-HEAD-is-branch-tip: no and "
                   "repo-branch-tip %s" % main_sha,
                   obs,
                   obs["is_tip"] == "no"
                   and obs["repo_branch_tip"] == main_sha
                   and obs["repo_branch"] == branch)
        else:
            skipped.append("fixed-custody-capture")
            expect("fixed-custody-capture",
                   "receipt records repo-HEAD-is-branch-tip: no",
                   "not_runnable: %s lacks fixed markers %s or is absent"
                   % (cp_fixed, [m.decode() for m in CP_FIXED_MARKERS]),
                   None)

        # == D1 step: baseline expression git rev-parse HEAD (red) =========
        rec = run(["git", "-C", sb, "rev-parse", "HEAD"], cwd=tmp,  # head-rev-lint: red-before
                  env=env)
        observed_head = rec["stdout"].strip()
        step("baseline-rev-parse-head", rec,
             {"observed": {"head_sha": observed_head,
                           "main_sha": main_sha}})
        expect("baseline-rev-parse-head",
               "rev-parse HEAD names the off-branch commit: red",
               {"head_sha": observed_head, "main_sha": main_sha,
                "head_is_off_branch": off_branch},
               observed_head == head_sha and off_branch)

        # == D1 step: revpin.resolve_source(sb) (green: raises) ============
        if revpin_ok:
            def _resolve_d1():
                spec = importlib.util.spec_from_file_location(
                    "jj_red_before_revpin_d1", revpin_path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod.resolve_source(sb)
            rec = run_expr("revpin.resolve_source(%r)" % sb, _resolve_d1)
            finding = None
            if rec["raised"] and "RevPinError" in rec["raised"]:
                finding = rec["raised"].split(":", 1)[-1].strip()
            step("revpin-resolve-source", rec,
                 {"observed": {"raised": rec["raised"],
                               "result": rec["result"]}})
            expect("revpin-resolve-source",
                   "resolve_source raises RevPinError head_not_branch_tip",
                   {"raised": rec["raised"], "finding": finding},
                   rec["raised"] is not None
                   and finding == "head_not_branch_tip")
        else:
            skipped.append("revpin-resolve-source")
            expect("revpin-resolve-source",
                   "resolve_source raises RevPinError head_not_branch_tip",
                   "not_runnable: %s lacks markers %s or is absent"
                   % (revpin_path, [m.decode() for m in REVPIN_MARKERS]),
                   None)

        # == L1 amendment (6): lane tip must be unchanged ==================
        lane_tip_after = sha_of(lane, "refs/heads/" + branch, tmp, env)
        expect("lane-tip-unchanged",
               "lane refs/heads/%s before == after (no lane write)" % branch,
               {"before": lane_tip_before, "after": lane_tip_after},
               lane_tip_before == lane_tip_after)

        runnable = [e for e in expectations if e["held"] is not None]
        all_held = bool(runnable) and all(e["held"] for e in runnable) \
            and not skipped
        receipt = {"tool": "jj-red-before", "lane": lane, "branch": branch,
                   "baseline_rev": baseline_rev,
                   "lane_tip": {"before": lane_tip_before,
                                "after": lane_tip_after},
                   "setup": setup_ok,
                   "baseline_extracts": baseline_extracts,
                   "steps": steps, "expectations": expectations,
                   "not_runnable": skipped, "all_held": all_held}
        if skipped:
            return receipt, CNE if not runnable else FAILED
        return receipt, CLEAN if all_held else FAILED
    finally:
        if env_tmp:
            shutil.rmtree(env_tmp, ignore_errors=True)


# --------------------------------------------------------------------------
# selftest fixtures (all under mkdtemp; nothing reads the real lane)
# --------------------------------------------------------------------------

FIXTURE_CD_BASELINE = """#!/usr/bin/env python3
import argparse, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--root", required=True)
ap.add_argument("--rev", default="HEAD")  # head-rev-lint: red-before (selftest fixture)
ap.add_argument("--table"); ap.add_argument("--expected")
a = ap.parse_args()
r = subprocess.run(["git", "-C", a.root, "rev-parse", "--verify", "--quiet",
                    a.rev + "^{commit}"], capture_output=True, text=True)
if r.returncode != 0:
    print("CITATION_DRIFT_VERDICT: could-not-evaluate exit=2"); sys.exit(2)
print("CITATION_DRIFT_REVISION: " + a.rev)
show = subprocess.run(["git", "-C", a.root, "show", a.rev + ":SCORECARD.md"],
                      capture_output=True, text=True)
line1 = (show.stdout.splitlines() or [""])[0]
if "fixture" not in line1:
    print("CITATION_DRIFT: citation_dead entry=fx-sc1 SCORECARD.md:1 lacks 'fixture'")
print("CITATION_DRIFT_VERDICT: reported findings=0 exit=0")
sys.exit(0)
"""

FIXTURE_CD_FIXED = """#!/usr/bin/env python3
# rev_resolved rev_requested branch head_not_branch_tip
import argparse, json, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--root", required=True)
ap.add_argument("--rev", default=None)
ap.add_argument("--table"); ap.add_argument("--expected")
a = ap.parse_args()
def sha(rev):
    r = subprocess.run(["git", "-C", a.root, "rev-parse", "--verify",
                        "--quiet", rev + "^{commit}"],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None
tip, head = sha("refs/heads/main"), sha("HEAD")  # head-rev-lint: red-before (selftest fixture)
if a.rev == "HEAD" and head != tip:  # head-rev-lint: red-before (selftest fixture)
    print("head_not_branch_tip: HEAD is not the branch tip", file=sys.stderr)
    sys.exit(2)
resolved = a.rev or tip
print(json.dumps({"rev_requested": a.rev, "rev_resolved": resolved,
                  "branch": "main"}, sort_keys=True, indent=2))
sys.exit(0)
"""

# Regressed "fixed" probe: markers present so the harness runs it, but it
# resolves HEAD like the baseline -> the green expectation must fail.
FIXTURE_CD_REGRESSED = FIXTURE_CD_FIXED.replace(
    "resolved = a.rev or tip", "resolved = a.rev or head")

FIXTURE_CP_BASELINE = """#!/usr/bin/env python3
import argparse, subprocess, sys
ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
c = sub.add_parser("capture")
c.add_argument("--out", required=True); c.add_argument("--label", default="")
c.add_argument("--paths", nargs="*", default=None)
a = ap.parse_args()
r = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,  # head-rev-lint: red-before (selftest fixture)
                   text=True)
head = r.stdout.strip() if r.returncode == 0 else "(none)"
text = "# custody-pair receipt v2\\n# repo-HEAD: %s\\n" % head
if a.out == "-":
    sys.stdout.write(text)
else:
    open(a.out, "w").write(text)
print("CUSTODY_PAIR_CAPTURE: OK exit=0")
sys.exit(0)
"""

FIXTURE_CP_FIXED = """#!/usr/bin/env python3
# --repo repo-HEAD-is-branch-tip repo-branch-tip
import argparse, os, subprocess, sys
ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
c = sub.add_parser("capture")
c.add_argument("--repo", default=None)
c.add_argument("--out", required=True); c.add_argument("--label", default="")
c.add_argument("--paths", nargs="*", default=None)
a = ap.parse_args()
repo = a.repo or os.getcwd()
def sha(rev):
    r = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", "--quiet",
                        rev + "^{commit}"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else "(none)"
head, tip = sha("HEAD"), sha("refs/heads/main")  # head-rev-lint: red-before (selftest fixture)
d = subprocess.run(["git", "-C", repo, "status", "--porcelain",
                    "--untracked-files=no"], capture_output=True, text=True)
text = ("# custody-pair receipt v3\\n"
        "# repo-HEAD: %s\\n"
        "# repo-root: %s\\n"
        "# repo-branch: main\\n"
        "# repo-branch-tip: %s\\n"
        "# repo-HEAD-is-branch-tip: %s\\n"
        "# repo-dirty: %s\\n"
        % (head, repo, tip, "yes" if head == tip else "no",
           "yes" if d.stdout.strip() else "no"))
if a.out == "-":
    sys.stdout.write(text)
else:
    open(a.out, "w").write(text)
print("CUSTODY_PAIR_CAPTURE: OK exit=0")
sys.exit(0)
"""

# Regressed "fixed" capture: markers present, branch-tip line present, but
# the is-branch-tip flag line is omitted -> the expectation must fail.
FIXTURE_CP_REGRESSED = FIXTURE_CP_FIXED.replace(
    '"# repo-HEAD-is-branch-tip: %s\\n"', '""')

FIXTURE_REVPIN = """#!/usr/bin/env python3
# def resolve_source RevPinError
import subprocess


class RevPinError(RuntimeError):
    def __init__(self, finding, result):
        super().__init__(finding)
        self.finding = finding
        self.result = result


def _sha(root, rev):
    r = subprocess.run(["git", "-C", root, "rev-parse", "--verify", "--quiet",
                        rev + "^{commit}"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def resolve_source(lane, branch="main", require_pushed=True,
                   require_head=True):
    source = _sha(lane, "refs/heads/" + branch)
    head = _sha(lane, "HEAD")  # head-rev-lint: red-before (selftest fixture)
    remote = _sha(lane, "refs/remotes/origin/" + branch)
    result = {"branch": branch, "source": source, "head": head,
              "head_equals_source": head == source, "remote": remote,
              "pushed": remote is not None}
    if require_head and not result["head_equals_source"]:
        raise RevPinError("head_not_branch_tip", result)
    return result
"""


def build_fixture_lane(root, name="fixture-lane", cd_text=None,
                       table_entries=None, symlinks=None):
    """A mini 'lane' git repo whose B commit carries the baseline stubs and a
    pointer-table entry citing SCORECARD.md:1 (needle 'fixture').

    `cd_text` overrides the committed citation-drift tool so a selftest case
    can make the *baseline* already resolve the tip (the red-before premise
    must then be reported as not held). `table_entries` replaces the default
    entry list and `symlinks` maps a lane-relative path to a link target;
    both exist for the pointer-table path-guard cases. Every git child here
    gets the same explicit scrubbed env as the probe's own children."""
    lane = os.path.join(root, name)
    os.makedirs(os.path.join(lane, os.path.dirname(CD_REL)))
    os.makedirs(os.path.join(lane, os.path.dirname(CP_REL)))
    Path(lane, CD_REL).write_text(cd_text or FIXTURE_CD_BASELINE)
    Path(lane, CP_REL).write_text(FIXTURE_CP_BASELINE)
    Path(lane, "LOG.md").write_text("# fixture log\n")
    Path(lane, "SCORECARD.md").write_text("# fixture scorecard\nrow\n")
    entries = table_entries if table_entries is not None else [
        {"id": "fx-sc1", "kind": "exact", "file": "SCORECARD.md",
         "line": 1, "must_match": "fixture"}]
    Path(lane, TABLE_REL).write_text(json.dumps({"entries": entries}))
    Path(lane, EXPECTED_REL).write_text("{}")
    for rel, target in (symlinks or {}).items():
        dest = os.path.join(lane, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if os.path.lexists(dest):
            os.unlink(dest)
        os.symlink(target, dest)
    env = _child_env(root)
    for argv in (["git", "init", "--quiet", "-b", "main", lane],
                 ["git", "-C", lane, "-c", "user.name=fx",
                  "-c", "user.email=fx@x", "add", "-A"],
                 ["git", "-C", lane, "-c", "user.name=fx",
                  "-c", "user.email=fx@x", "commit", "--quiet", "-m", "B"]):
        r = subprocess.run(list(argv), capture_output=True, text=True,
                           env=env)
        if r.returncode != 0:
            raise RuntimeError("fixture lane setup failed: %s %s"
                               % (argv, r.stderr))
    b = sha_of(lane, "refs/heads/main", root, env)
    return lane, b


def _install_git_shim(root):
    """A PATH-first `git` that logs its own child env, then execs real git.
    Only the selftest uses it: it turns 'the env was scrubbed' into an
    observation instead of a claim."""
    shim_dir = os.path.join(root, "git-shim")
    os.makedirs(shim_dir, exist_ok=True)
    log_path = os.path.join(root, "git-shim-env.log")
    real_git = shutil.which("git")
    script = ("#!/bin/sh\n"
              "{ printf '=== argv'; printf ' %%s' \"$@\"; printf '\\n'; "
              "env; } >> %s\n"
              "exec %s \"$@\"\n"
              % (shlex.quote(log_path), shlex.quote(real_git)))
    shim = os.path.join(shim_dir, "git")
    Path(shim).write_text(script)
    os.chmod(shim, 0o755)
    return shim_dir, log_path


def _shim_observations(log_path):
    """(git invocations logged, lines carrying a GIT_*/JJ_*/TMPDIR key)."""
    try:
        text = Path(log_path).read_text()
    except OSError:
        return 0, ["no shim log at %s" % log_path]
    calls, dirty = 0, []
    for line in text.splitlines():
        if line.startswith("=== "):
            calls += 1
            continue
        if _dirty_key(line.split("=", 1)[0]):
            dirty.append(line[:120])
    return calls, dirty


def selftest(jj):
    tmp = tempfile.mkdtemp(prefix="jj-red-before-selftest-", dir="/tmp")
    _refuse_inside(tmp)
    cases = 0
    failures = []
    try:
        lane, b = build_fixture_lane(tmp)
        tools = os.path.join(tmp, "fixed-tools")
        os.makedirs(tools)
        paths = {}
        for name, text in (("cd_fixed", FIXTURE_CD_FIXED),
                           ("cd_regressed", FIXTURE_CD_REGRESSED),
                           ("cp_fixed", FIXTURE_CP_FIXED),
                           ("cp_regressed", FIXTURE_CP_REGRESSED),
                           ("revpin", FIXTURE_REVPIN)):
            p = os.path.join(tools, name + ".py")
            Path(p).write_text(text)
            paths[name] = p

        def go(cd, cp, lane_=lane, b_=b):
            return evaluate(lane=lane_, baseline_rev=b_, branch="main",
                            jj=jj, cd_fixed=cd, cp_fixed=cp,
                            revpin_path=paths["revpin"])

        def not_held(receipt):
            return [e["name"] for e in receipt["expectations"]
                    if e["held"] is False]

        # case 1: all-fixed tools -> every expectation holds, exit 0
        cases += 1
        receipt, code = go(paths["cd_fixed"], paths["cp_fixed"])
        if not (code == 0 and receipt["all_held"] is True
                and not receipt["not_runnable"]):
            failures.append("green case: exit=%r all_held=%r not_held=%r"
                            % (code, receipt.get("all_held"),
                               not_held(receipt)))

        # case 2 (red): regressed cd probe resolves HEAD -> must fail
        cases += 1
        receipt, code = go(paths["cd_regressed"], paths["cp_fixed"])
        if not (code == 1 and "fixed-citation-drift" in not_held(receipt)):
            failures.append("red cd case: exit=%r not_held=%r"
                            % (code, not_held(receipt)))

        # case 3 (red): regressed cp omits is-branch-tip -> must fail
        cases += 1
        receipt, code = go(paths["cd_fixed"], paths["cp_regressed"])
        if not (code == 1 and "fixed-custody-capture" in not_held(receipt)):
            failures.append("red cp case: exit=%r not_held=%r"
                            % (code, not_held(receipt)))

        # case 4 (red): the *baseline* tool is already fixed -> the red-before
        # premise must be reported as not held (a green 'before' proves
        # nothing), exit 1 naming baseline-citation-drift.
        cases += 1
        lane2, b2 = build_fixture_lane(tmp, "fixture-lane-fixed-baseline",
                                       cd_text=FIXTURE_CD_FIXED)
        receipt, code = go(paths["cd_fixed"], paths["cp_fixed"], lane2, b2)
        bad = not_held(receipt)
        if not (code == 1 and "baseline-citation-drift" in bad
                and "baseline-citation-drift-finding" in bad):
            failures.append("green-baseline case: exit=%r not_held=%r"
                            % (code, bad))

        # case 5: fixed tools absent -> steps not_runnable, never held
        cases += 1
        receipt, code = go(os.path.join(tmp, "absent-cd.py"),
                           os.path.join(tmp, "absent-cp.py"))
        nr = sorted(receipt["not_runnable"])
        want = sorted(["d0-fixed-citation-drift-rev-head",
                       "d0-fixed-custody-capture",
                       "fixed-citation-drift",
                       "fixed-citation-drift-rev-head",
                       "fixed-custody-capture"])
        if not (code in (1, 2) and receipt["all_held"] is False
                and nr == want):
            failures.append("absent-tools case: exit=%r not_runnable=%r"
                            % (code, nr))

        # case 6 (red env): a sentinel GIT_*/JJ_* parent env must reach no
        # git child — the fixture builder, every evaluate child, and the
        # in-process revpin import (which spawns its own git) included. The
        # shimmed git turns "the env was scrubbed" into a logged observation.
        cases += 1
        shim_dir, shim_log = _install_git_shim(tmp)
        saved_path = os.environ.get("PATH", "")
        sentinels = {"GIT_DIR": os.path.join(tmp, "sentinel-git-dir"),
                     "GIT_WORK_TREE": os.path.join(tmp, "sentinel-wt"),
                     "GIT_INDEX_FILE": os.path.join(tmp, "sentinel-index"),
                     "JJ_OPERATION_ID": "sentinel-op"}
        os.environ.update(sentinels)
        os.environ["PATH"] = shim_dir + os.pathsep + saved_path
        env_obs = {}
        try:
            lane_env, b_env = build_fixture_lane(tmp, "fixture-lane-env")
            receipt, code = go(paths["cd_fixed"], paths["cp_fixed"],
                               lane_env, b_env)
            calls, dirty = _shim_observations(shim_log)
            env_obs = {"calls": calls, "dirty": dirty[:3], "exit": code,
                       "all_held": receipt.get("all_held")}
            ok_env = (code == 0 and receipt.get("all_held") is True
                      and calls > 0 and not dirty)
        except Exception as exc:
            ok_env = False
            env_obs = {"raised": "%s: %s" % (type(exc).__name__, exc)}
        finally:
            for key in sentinels:
                os.environ.pop(key, None)
            os.environ["PATH"] = saved_path
        if not ok_env:
            failures.append("env scrub case: %r" % (env_obs,))

        # cases 7-9 (red path): a pointer-table entry naming a path out of the
        # mkdtemp clone must refuse exit 2 with its named cause and leave the
        # outside victim byte-identical — absolute, `..` and symlink forms.
        def escape_case(label, entry_for, links_for=None):
            victim = os.path.join(tmp, "victim-" + label + ".md")
            Path(victim).write_text("# victim original\n")
            lane_g, b_g = build_fixture_lane(
                tmp, "fixture-lane-" + label,
                table_entries=[{"id": "fx-escape-" + label, "kind": "exact",
                                "file": entry_for(victim), "line": 1,
                                "must_match": "victim"}],
                symlinks=links_for(victim) if links_for else None)
            receipt, code = go(paths["cd_fixed"], paths["cp_fixed"],
                               lane_g, b_g)
            unchanged = Path(victim).read_text() == "# victim original\n"
            refused = (code == 2
                       and receipt.get("refusal")
                       == "pointer_table_path_outside_sandbox")
            if not (refused and unchanged):
                failures.append(
                    "%s case: exit=%r refusal=%r detail=%r unchanged=%r"
                    % (label, code, receipt.get("refusal"),
                       receipt.get("refusal_detail"), unchanged))

        cases += 1
        escape_case("abs", lambda victim: victim)
        cases += 1
        escape_case("rel", lambda victim: "../" + os.path.basename(victim))
        cases += 1
        escape_case("link", lambda victim: "linked.md",
                    links_for=lambda victim: {"linked.md": victim})
    except Exception as exc:
        return 2, "SELFTEST: FAILED setup %s: %s" % (type(exc).__name__, exc)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if failures:
        return 1, "SELFTEST: FAILED cases=%d (%s)" % (
            cases, "; ".join(failures))
    return 0, "SELFTEST: CLEAN cases=%d" % cases


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def emit(obj, out_path):
    text = json.dumps(obj, sort_keys=True, indent=2) + "\n"
    if out_path:
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    sys.stdout.write(text)


def main(argv=None):
    # Defence in depth: a GIT_*/JJ_* value in the invoking env must never
    # reach git/jj, including through a call site that forgets an env.
    for key in [k for k in os.environ if _dirty_key(k)]:
        del os.environ[key]
    ap = argparse.ArgumentParser(
        description="Red/green HEAD-vs-branch-tip probe inside a throwaway "
                    "jj-colocated clone (round-18 C2).")
    ap.add_argument("--root", default=LANE_DEFAULT, help="lane to clone")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--baseline-rev", default=BASELINE_B,
                    help="revision whose Git blobs are the baseline tools")
    ap.add_argument("--jj", default=shutil.which("jj") or
                    os.path.expanduser("~/.local/bin/jj"))
    ap.add_argument("--cd-probe", default=os.path.join(LANE_DEFAULT, CD_REL),
                    help="fixed citation-drift probe in the working tree")
    ap.add_argument("--custody-pair",
                    default=os.path.join(LANE_DEFAULT, CP_REL),
                    help="fixed custody-pair tool in the working tree")
    ap.add_argument("--revpin",
                    default=os.path.join(LANE_DEFAULT, REVPIN_REL),
                    help="revpin.py module under test")
    ap.add_argument("--out", default=None, help="receipt JSON path")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        code, line = selftest(args.jj)
        print(line)
        return code

    receipt, code = evaluate(
        lane=args.root, baseline_rev=args.baseline_rev, branch=args.branch,
        jj=args.jj, cd_fixed=args.cd_probe, cp_fixed=args.custody_pair,
        revpin_path=args.revpin)
    try:
        emit(receipt, args.out)
    except OSError as exc:
        print("USAGE: cannot write --out receipt (%s): %s"
              % (args.out, exc), file=sys.stderr)
        return CNE
    return code


if __name__ == "__main__":
    sys.exit(main())
