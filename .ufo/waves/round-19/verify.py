#!/usr/bin/env python3
"""Round-19 single post-integration execution pass (L1).

Runs every command in the plan below once, without a shell, from the lane
root, and retains argv, cwd, env overrides, UTC start/end, exit, and
stdout/stderr (files under `.ufo/waves/round-19/verify/` with SHA-256) in
`.ufo/waves/round-19/verification.json`. Every command's expected exit comes
from EXPECTED_EXITS below; an actual exit that differs is recorded in
`unexpected_exits` and fails the pass.

`source` is the lane's branch tip (`refs/heads/main`), never HEAD: the pass
extracts `.ufo/waves/round-18/tools/revpin.py` from the source blob, loads it
from a tempfile.mkdtemp() copy, and calls `resolve_source(LANE)` (require_head
and require_pushed). Any RevPinError finding (branch_missing,
head_not_branch_tip, branch_not_pushed) refuses the pass with exit 2 before a
single command runs. The revision passed on the command line is the baseline
(the claims' red state); the source revision is resolved, not supplied.

Scope of "at REV": tools, predictions, the SOURCES census and the retained
c1-census-v10 baseline receipt are read at the source revision (Git objects;
`git show REV:path`, `git ls-tree`), and every lane tool the pass executes
must have worktree bytes equal to its source blob (`tool_integrity`; a
mismatch fails the pass). C3 run receipts and observations are read from
`W19/runs/<label>/` as the run wrote them: they are runtime evidence, not
committed bytes, and round-17's remap lesson shows that relocating a receipt
breaks its path bindings. predictions are materialized from the source blob
into `verify/scratch-predictions/` so `compare.py` judges the frozen bytes.

The plan covers: every round-19 Python tool selftest, the round-19-edited
round-18 tools and gates, the counting commands (`routed-r18.py`,
`province-pins.py`, `measure.py`) at the baseline and at the source revision,
per-carrier `receipt-validate.py --require-mid-maps` and `compare.py` for the
labels frozen in the source `predictions/carriers.tsv`, the fleet SOURCES
census (counts and validate), and `c1-census-v10.py`.

Usage: python3 -I -B verify.py BASELINE_REV   (full pass; writes verification.json)
       python3 -I -B verify.py --selftest      (2-command dry fixture, mkdtemp only)

`--selftest` is the dry fixture that proves the runner mechanics without
touching the lane: two commands (one expected exit 0, one deliberately
unexpected exit 7) exercise argv/exit/stdout-SHA-256 recording, expected-exit
accounting, and the verification.json round trip.

Limits: one pass, one host, one read of each input. A pin pair proves identical
bytes at the two recorded instants only (QUALITY #19), never continuity
between them. `compare.py` exit 0 means the retained prediction matched the
retained observation; it is not a claim that the analyzer was correct. No
carrier binary is executed here; the C3 commands read retained logs only.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True

LANE = str(Path(__file__).resolve().parents[3])
W = LANE + "/.ufo/waves/round-19"
T19 = W + "/tools"
T18 = LANE + "/.ufo/waves/round-18/tools"
T17 = LANE + "/.ufo/waves/round-17/tools"
GATES = LANE + "/.ufo/gates"
OUT = W + "/verify"
RUNS = W + "/runs"
PRED = W + "/predictions"
FLEET = "/home/vgpnk/Projects/shokunin"
CENSUS = FLEET + "/scripts/sources-census.sh"
PY = ["python3", "-I", "-B"]
REVPIN_REL = ".ufo/waves/round-18/tools/revpin.py"
VERIFY_REL = ".ufo/waves/round-19/verify.py"
BEFORE_REL = ".ufo/waves/round-19/evidence/c1-census-v10-before.txt"

# Required round-19 tools: a missing one is a skip record (unexpected exit),
# not a silently absent selftest.
REQUIRED_TOOLS = ["routed-r18.py", "province-pins.py", "wave-outcomes.py"]

# The expected-exit table for every command the pass can run. Labels not listed
# exactly must match a "-" suffix key; an unplanned label refuses the pass.
EXPECTED_EXITS = {
    # selftests: every round-19 tool, the round-19-edited round-18 tools and
    # gates, and the round-17 tools this pass invokes.
    "selftest-": 0,
    # C1 counting command (routed-r18.py): 7 defects open at the baseline,
    # 0 at the source revision.
    "routed-r18-baseline": 0,
    "routed-r18-baseline-strict": 1,
    "routed-r18-source": 0,
    "routed-r18-source-strict": 0,
    # C2 counting command (province-pins.py): stale client pins at the
    # baseline, none at the source revision.
    "province-pins-baseline": 0,
    "province-pins-baseline-strict": 1,
    "province-pins-source": 0,
    "province-pins-source-strict": 0,
    # Counting aggregates at both revisions (measure.py reports null+reason
    # for tools absent at the baseline revision).
    "measure-baseline": 0,
    "measure-source": 0,
    # C3 retained-run checks.
    "receipt-validate-": 0,
    "log-extract-": 0,
    "compare-": 0,
    # Freshness gate and fleet census.
    "c1-census-v10": 0,
    "sources-census-counts": 0,
    "sources-census": 0,
    # Registered revpin form and pin bookkeeping.
    "revpin-lane": 0,
    "pins-snapshot-pre": 0,
    "pins-snapshot-post": 0,
    "pins-compare": 0,
}

USAGE = (
    "usage: python3 -I -B verify.py BASELINE_REV\n"
    "       python3 -I -B verify.py --selftest\n"
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_try(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", LANE, "--no-optional-locks", *args],
        capture_output=True, text=True, check=False,
    )


def git_out(*args: str) -> str:
    r = git_try(*args)
    if r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def source_bytes(rev: str, rel: str):
    """Bytes of one lane-relative path at rev, or None when absent there."""
    r = subprocess.run(
        ["git", "-C", LANE, "--no-optional-locks", "show", "%s:%s" % (rev, rel)],
        capture_output=True, check=False,
    )
    return r.stdout if r.returncode == 0 else None


def expected_for(label: str) -> int:
    """Expected exit for one command label, from the table above."""
    if label in EXPECTED_EXITS:
        return EXPECTED_EXITS[label]
    for key in sorted(EXPECTED_EXITS, key=len, reverse=True):
        if key.endswith("-") and label.startswith(key):
            return EXPECTED_EXITS[key]
    raise KeyError("unplanned command label: " + label)


def write_json(path: str, obj) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, sort_keys=True, indent=2)
        f.write("\n")
    os.replace(tmp, path)


class Pass:
    """One execution plan: every command is recorded, expected or skipped."""

    def __init__(self, out_dir: str, cwd: str):
        self.out_dir = out_dir
        self.cwd = cwd
        self.commands = []
        self._labels = set()
        os.makedirs(out_dir, exist_ok=True)

    def _claim(self, label: str) -> None:
        if label in self._labels:
            raise RuntimeError("duplicate command label: " + label)
        self._labels.add(label)

    def run(self, label: str, argv, expect: int, env=None) -> str:
        self._claim(label)
        rec = {
            "label": label,
            "argv": list(argv),
            "cwd": self.cwd,
            "env_overrides": env or {},
            "started_at_utc": now(),
            "expected_exit": expect,
        }
        so = os.path.join(self.out_dir, label + ".stdout")
        se = os.path.join(self.out_dir, label + ".stderr")
        with open(so, "wb") as fo, open(se, "wb") as fe:
            p = subprocess.run(
                list(argv), cwd=self.cwd, stdout=fo, stderr=fe,
                env={**os.environ, **(env or {})},
            )
        rec.update({
            "ended_at_utc": now(),
            "exit": p.returncode,
            "stdout_path": so,
            "stdout_sha256": sha(so),
            "stderr_path": se,
            "stderr_sha256": sha(se),
        })
        rec["exit_as_expected"] = p.returncode == expect
        self.commands.append(rec)
        return so

    def skip(self, label: str, argv, expect: int, reason: str) -> None:
        """Record a command that could not run as an unevaluable unexpected
        exit instead of crashing the pass."""
        self._claim(label)
        rec = {
            "label": label,
            "argv": list(argv),
            "cwd": self.cwd,
            "env_overrides": {},
            "started_at_utc": now(),
            "ended_at_utc": now(),
            "expected_exit": expect,
            "exit": 2,
            "skipped_reason": reason,
        }
        so = os.path.join(self.out_dir, label + ".stdout")
        se = os.path.join(self.out_dir, label + ".stderr")
        with open(so, "wb") as fo:
            fo.write(b"")
        with open(se, "wb") as fe:
            fe.write(("SKIPPED: " + reason + "\n").encode())
        rec.update({
            "stdout_path": so,
            "stdout_sha256": sha(so),
            "stderr_path": se,
            "stderr_sha256": sha(se),
            "exit_as_expected": False,
        })
        self.commands.append(rec)

    def unexpected(self):
        return [c["label"] for c in self.commands if not c["exit_as_expected"]]


def selftest() -> int:
    """2-command dry fixture: prove argv/exit/stdout-SHA recording, the
    expected-exit table comparison, and the verification.json round trip.
    Everything lives under tempfile.mkdtemp() and is removed after."""
    fails = []
    cases = 2
    root = tempfile.mkdtemp(prefix="kr19-verify-selftest.")
    try:
        out = os.path.join(root, "verify")
        p = Pass(out, root)
        p.run("fixture-ok", PY + ["-c", "print('alpha')"], 0)
        # Deliberately unexpected: expected 0, exits 7. The runner must record
        # the mismatch, not assume the table.
        p.run("fixture-detects", PY + ["-c", "import sys; print('beta'); sys.exit(7)"], 0)

        def check(ok: bool, detail: str) -> None:
            if not ok:
                fails.append(detail)

        check(len(p.commands) == cases,
              "recorded %d commands, want %d" % (len(p.commands), cases))
        if len(p.commands) == cases:
            a, b = p.commands
            check(a["exit"] == 0 and a["exit_as_expected"] is True,
                  "fixture-ok exit/expected not recorded as 0/0")
            check(b["exit"] == 7 and b["exit_as_expected"] is False,
                  "fixture-detects exit 7 was not recorded as unexpected")
            check(a["stdout_sha256"] == sha_bytes(b"alpha\n"),
                  "fixture-ok stdout sha256 does not match its bytes")
            check(b["stdout_sha256"] == sha_bytes(b"beta\n"),
                  "fixture-detects stdout sha256 does not match its bytes")
            check(a["argv"] == PY + ["-c", "print('alpha')"],
                  "fixture-ok argv was not recorded verbatim")
            check(a["cwd"] == root, "cwd was not recorded")
            check(a["started_at_utc"] and a["ended_at_utc"],
                  "UTC instants missing")
        check(p.unexpected() == ["fixture-detects"],
              "unexpected_exits is %r, want ['fixture-detects']" % (p.unexpected(),))

        record = {"commands": p.commands, "unexpected_exits": p.unexpected()}
        path = os.path.join(out, "verification.json")
        write_json(path, record)
        again = json.load(open(path))
        check(len(again["commands"]) == cases,
              "verification.json round trip lost commands")
        check(again["unexpected_exits"] == ["fixture-detects"],
              "verification.json round trip lost unexpected_exits")
        check(again["commands"][0]["argv"] == PY + ["-c", "print('alpha')"],
              "verification.json round trip lost argv")

        # The table itself: exact keys, prefix keys, and one non-default entry.
        check(expected_for("selftest-routed-r18") == 0,
              "table: selftest prefix did not resolve to 0")
        check(expected_for("compare-t1250-go") == 0,
              "table: compare prefix did not resolve to 0")
        check(expected_for("routed-r18-baseline-strict") == 1,
              "table: routed-r18-baseline-strict did not resolve to 1")
        try:
            expected_for("no-such-label")
            fails.append("table: an unplanned label was accepted")
        except KeyError:
            pass
    finally:
        shutil.rmtree(root, ignore_errors=True)

    if fails:
        print("SELFTEST: FAILED cases=%d fails=%d: %s"
              % (cases, len(fails), "; ".join(fails)))
        return 1
    print("SELFTEST: CLEAN cases=%d" % cases)
    return 0


def resolve_commit(rev: str):
    r = git_try("rev-parse", "--verify", rev + "^{commit}")
    if r.returncode != 0:
        return None
    return r.stdout.strip() or None


def load_source_revpin(source: str):
    """Load revpin.py as committed at source (never the worktree copy)."""
    data = source_bytes(source, REVPIN_REL)
    if data is None:
        raise RuntimeError("revpin absent at source: " + REVPIN_REL)
    tmp = tempfile.mkdtemp(prefix="kr19-verify-revpin.")
    path = os.path.join(tmp, "revpin.py")
    try:
        with open(path, "wb") as f:
            f.write(data)
        spec = importlib.util.spec_from_file_location("r19_source_revpin", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return mod, sha_bytes(data)


def source_paths(source: str):
    listing = git_out("ls-tree", "-r", "--name-only", source)
    return set(line for line in listing.splitlines() if line)


def source_tools(source: str):
    """Every *.py directly under W19/tools at source, sorted."""
    try:
        listing = git_out("ls-tree", "--name-only", source,
                          ".ufo/waves/round-19/tools/")
    except RuntimeError:
        return []
    names = [os.path.basename(line.strip()) for line in listing.splitlines()
             if line.strip().endswith(".py")]
    return sorted(set(names))


def labels_at(source: str):
    rel = ".ufo/waves/round-19/predictions/carriers.tsv"
    data = source_bytes(source, rel)
    if data is not None:
        labels = []
        for line in data.decode("utf-8", "replace").splitlines():
            parts = line.split("\t")
            if parts and parts[0].strip():
                labels.append(parts[0].strip())
        labels = list(dict.fromkeys(labels))
        if labels:
            return labels, "source:" + rel
    if os.path.isdir(RUNS):
        labs = sorted(d for d in os.listdir(RUNS)
                      if os.path.isdir(os.path.join(RUNS, d)))
        return labs, "worktree:" + RUNS
    return [], "none"


def full_pass(arg: str) -> int:
    base = resolve_commit(arg)
    if base is None:
        print(json.dumps({"refused": True,
                          "cause": "baseline_unresolvable",
                          "baseline": arg}, sort_keys=True, indent=2))
        return 2
    tip = resolve_commit("refs/heads/main")
    if tip is None:
        print(json.dumps({"refused": True,
                          "cause": "branch_missing: refs/heads/main",
                          "baseline_revision": base}, sort_keys=True, indent=2))
        return 2
    try:
        revpin, revpin_sha = load_source_revpin(tip)
    except Exception as exc:  # unloadable source revpin is a finding, not a crash
        print(json.dumps({"refused": True,
                          "cause": "source_revpin_unloadable: %s: %s"
                                   % (type(exc).__name__, exc),
                          "baseline_revision": base,
                          "branch_tip": tip}, sort_keys=True, indent=2))
        return 2
    try:
        pin = revpin.resolve_source(LANE)
    except revpin.RevPinError as exc:
        print(json.dumps({
            "refused": True,
            "revpin_finding": exc.finding,
            "revpin_result": exc.result,
            "baseline_revision": base,
            "source": "unresolved: revpin.resolve_source refused before any command ran",
        }, sort_keys=True, indent=2))
        return 2
    source = pin["source"]
    if source != tip:
        print(json.dumps({
            "refused": True,
            "cause": "source_moved_during_resolution",
            "branch_tip_at_extraction": tip,
            "source_at_resolution": source,
            "baseline_revision": base,
        }, sort_keys=True, indent=2))
        return 2

    dirty = git_out("status", "--porcelain", "--untracked-files=no").splitlines()
    all_paths = source_paths(source)

    os.makedirs(OUT, exist_ok=True)
    if not os.path.isfile(T17 + "/pins.py"):
        print(json.dumps({"refused": True,
                          "cause": "pins_tool_missing: " + T17 + "/pins.py",
                          "baseline_revision": base,
                          "source_revision": source}, sort_keys=True, indent=2))
        return 2
    pins_spec = importlib.util.spec_from_file_location("r19_pins", T17 + "/pins.py")
    pins = importlib.util.module_from_spec(pins_spec)
    pins_spec.loader.exec_module(pins)

    executed_tools = set()

    def A(rel: str) -> str:
        return LANE + "/" + rel

    pin_set = {A(VERIFY_REL)}
    if os.path.isdir(T19):
        pin_set |= {os.path.join(T19, n) for n in os.listdir(T19)
                    if n.endswith(".py")}
    pin_paths = sorted(pin_set)
    for rel in [".ufo/waves/round-19/measure.py",
                ".ufo/waves/round-19/gen-predictions.py",
                ".ufo/waves/round-19/run-carriers.sh",
                ".ufo/waves/round-18/tools/revpin.py",
                ".ufo/waves/round-18/tools/head-rev-lint.py",
                ".ufo/waves/round-18/tools/jj-red-before.py",
                ".ufo/gates/citation-drift/citation-drift-probe.py",
                ".ufo/gates/custody-pair/custody-pair.py",
                ".ufo/waves/round-17/tools/receipt-validate.py",
                ".ufo/waves/round-17/tools/compare.py",
                ".ufo/waves/round-17/tools/log-extract.py",
                ".ufo/waves/round-17/tools/pins.py"]:
        if os.path.isfile(A(rel)):
            pin_paths.append(A(rel))
    if os.path.isdir(PRED):
        pin_paths.extend(sorted(os.path.join(PRED, n) for n in os.listdir(PRED)
                                if os.path.isfile(os.path.join(PRED, n))))
    pin_paths = sorted(set(pin_paths))

    pins_pre = pins.snapshot(pin_paths)
    p = Pass(OUT, LANE)

    def run_tool(label: str, rel: str, extra, expect: int,
                 prefix=None, present_at_source=True) -> None:
        argv = list(prefix or PY) + [A(rel)] + list(extra)
        if present_at_source and rel not in all_paths:
            p.skip(label, argv, expect, "absent_at_source: " + rel)
            return
        if not os.path.isfile(A(rel)):
            p.skip(label, argv, expect, "missing_worktree: " + rel)
            return
        executed_tools.add(rel)
        p.run(label, argv, expect)

    p.run("pins-snapshot-pre", PY + [A(".ufo/waves/round-17/tools/pins.py"),
                                     "snapshot", "--out", OUT + "/tools-pre.json"]
          + pin_paths, 0)

    # Round-19 tool selftests: every *.py under W19/tools at source, the
    # required three even when the source tree is incomplete, plus the
    # top-level runners.
    tool_names = sorted(set(source_tools(source)) | set(REQUIRED_TOOLS))
    for name in tool_names:
        stem = name[:-3]
        run_tool("selftest-" + stem, ".ufo/waves/round-19/tools/" + name,
                 ["--selftest"], 0)
    run_tool("selftest-measure", ".ufo/waves/round-19/measure.py",
             ["--selftest"], 0)
    run_tool("selftest-gen-predictions", ".ufo/waves/round-19/gen-predictions.py",
             ["--selftest"], 0)
    run_tool("selftest-run-carriers", ".ufo/waves/round-19/run-carriers.sh",
             ["--selftest"], 0, prefix=["bash"])

    # Round-19-edited round-18 tools and gates.
    run_tool("selftest-w18-revpin", ".ufo/waves/round-18/tools/revpin.py",
             ["--selftest"], 0)
    run_tool("selftest-w18-head-rev-lint",
             ".ufo/waves/round-18/tools/head-rev-lint.py", ["--selftest"], 0)
    run_tool("selftest-w18-jj-red-before",
             ".ufo/waves/round-18/tools/jj-red-before.py", ["--selftest"], 0)
    run_tool("selftest-citation-drift-probe",
             ".ufo/gates/citation-drift/citation-drift-probe.py",
             ["--selftest"], 0)
    os.makedirs(OUT + "/scratch-custody", exist_ok=True)
    run_tool("selftest-custody-pair", ".ufo/gates/custody-pair/custody-pair.py",
             ["selftest", "--scratch", OUT + "/scratch-custody"], 0)

    # Round-17 tools the pass invokes.
    for name in ("receipt-validate", "compare", "log-extract", "pins"):
        run_tool("selftest-w17-" + name, ".ufo/waves/round-17/tools/" + name + ".py",
                 ["--selftest"], 0)

    # Counting commands at the baseline and at the source revision.
    routed = ".ufo/waves/round-19/tools/routed-r18.py"
    run_tool("routed-r18-baseline", routed, ["--root", LANE, "--rev", base], 0)
    run_tool("routed-r18-baseline-strict", routed,
             ["--root", LANE, "--rev", base, "--strict"], 1)
    run_tool("routed-r18-source", routed, ["--root", LANE, "--rev", source], 0)
    run_tool("routed-r18-source-strict", routed,
             ["--root", LANE, "--rev", source, "--strict"], 0)

    province = ".ufo/waves/round-19/tools/province-pins.py"
    run_tool("province-pins-baseline", province,
             ["--root", LANE, "--rev", base], 0)
    run_tool("province-pins-baseline-strict", province,
             ["--root", LANE, "--rev", base, "--strict"], 1)
    run_tool("province-pins-source", province,
             ["--root", LANE, "--rev", source], 0)
    run_tool("province-pins-source-strict", province,
             ["--root", LANE, "--rev", source, "--strict"], 0)

    run_tool("measure-baseline", ".ufo/waves/round-19/measure.py", [base], 0)
    run_tool("measure-source", ".ufo/waves/round-19/measure.py", [source], 0)

    # C3 retained runs: prediction bytes come from the source blob; receipt
    # and observation stay where the run wrote them.
    labels, labels_source = labels_at(source)
    scratch_pred = OUT + "/scratch-predictions"
    os.makedirs(scratch_pred, exist_ok=True)
    for lab in labels:
        rd = os.path.join(RUNS, lab)
        receipt = os.path.join(rd, "receipt.json")
        pred_rel = ".ufo/waves/round-19/predictions/" + lab + ".prediction.json"
        if os.path.isfile(receipt):
            run_tool("receipt-validate-" + lab,
                     ".ufo/waves/round-17/tools/receipt-validate.py",
                     ["--require-mid-maps", receipt], 0)
        else:
            argv = PY + [A(".ufo/waves/round-17/tools/receipt-validate.py"),
                         "--require-mid-maps", receipt]
            p.skip("receipt-validate-" + lab, argv, 0,
                   "no receipt.json in " + rd)
        obs = os.path.join(rd, "observation.json")
        if not os.path.isfile(obs):
            obs = None
            log = None
            if os.path.isfile(receipt):
                try:
                    bound = json.load(open(receipt)).get("bound_sessions") or []
                    if bound:
                        log = os.path.join(rd, "logs",
                                           os.path.basename(bound[0]), "ghidra.log")
                except (OSError, ValueError):
                    log = None
            if log and os.path.isfile(log) and os.path.isfile(
                    A(".ufo/waves/round-17/tools/log-extract.py")):
                obs = p.run("log-extract-" + lab,
                            PY + [A(".ufo/waves/round-17/tools/log-extract.py"),
                                  "--log", log], 0)
                executed_tools.add(".ufo/waves/round-17/tools/log-extract.py")
        if pred_rel not in all_paths:
            p.skip("compare-" + lab,
                   PY + [A(".ufo/waves/round-17/tools/compare.py"),
                         "--prediction", A(pred_rel),
                         "--observation", str(obs)], 0,
                   "prediction absent at source: " + pred_rel)
        elif obs is None:
            p.skip("compare-" + lab,
                   PY + [A(".ufo/waves/round-17/tools/compare.py"),
                         "--prediction", A(pred_rel),
                         "--observation", "(none)"], 0,
                   "no retained observation.json and no bound ghidra.log in " + rd)
        else:
            data = source_bytes(source, pred_rel)
            pred_path = os.path.join(scratch_pred, lab + ".prediction.json")
            with open(pred_path, "wb") as f:
                f.write(data)
            run_tool("compare-" + lab,
                     ".ufo/waves/round-17/tools/compare.py",
                     ["--prediction", pred_path, "--observation", obs], 0)

    # Freshness gate and fleet census.
    run_tool("c1-census-v10", ".ufo/gates/c1-census-v10.py", ["--root", LANE], 0)
    p.run("sources-census-counts",
          [CENSUS, "census", "--root", FLEET, "kaidoku"], 0)
    p.run("sources-census",
          [CENSUS, "validate", "--root", FLEET, "kaidoku"], 0)

    # Registered revpin form plus pin bookkeeping across the pass.
    run_tool("revpin-lane", ".ufo/waves/round-18/tools/revpin.py",
             ["--root", LANE], 0)
    p.run("pins-snapshot-post", PY + [A(".ufo/waves/round-17/tools/pins.py"),
                                      "snapshot", "--out", OUT + "/tools-post.json"]
          + pin_paths, 0)
    p.run("pins-compare", PY + [A(".ufo/waves/round-17/tools/pins.py"),
                                "compare", OUT + "/tools-pre.json",
                                OUT + "/tools-post.json"], 0)
    executed_tools.add(VERIFY_REL)

    pins_post = pins.snapshot(pin_paths)
    pin_compare = pins.compare(pins_pre, pins_post)
    pycache = subprocess.run(["find", LANE + "/.ufo", "-name", "__pycache__"],
                             capture_output=True, text=True).stdout.split()

    # Tool bytes: every executed lane tool must equal its source blob.
    integrity = []
    for rel in sorted(executed_tools):
        sb = source_bytes(source, rel)
        wt = sha(A(rel)) if os.path.isfile(A(rel)) else None
        ss = sha_bytes(sb) if sb is not None else None
        integrity.append({"path": rel, "source_sha256": ss,
                          "worktree_sha256": wt,
                          "match": ss is not None and ss == wt})
    integrity_mismatches = [e["path"] for e in integrity if not e["match"]]

    # Baseline red-state receipt retained for the freshness claim.
    before = source_bytes(source, BEFORE_REL)
    before_info = {"path": BEFORE_REL,
                   "sha256": sha_bytes(before) if before is not None else None,
                   "present_at_source": before is not None,
                   "verdict_fail": False}
    if before is not None:
        text = before.decode("utf-8", "replace")
        before_info["verdict_fail"] = "VERDICT: FAIL" in text
        tail = [line for line in text.splitlines()
                if line.startswith("VERDICT") or line.startswith("exit=")]
        before_info["verdict_lines"] = tail[-2:]

    checks = {
        "c1_census_before_present": before_info["present_at_source"],
        "c1_census_before_verdict_fail": before_info["verdict_fail"],
        "baseline_differs_from_source": base != source,
    }
    failed_checks = [name for name, ok in sorted(checks.items()) if not ok]

    external = []
    for path in (CENSUS,):
        if os.path.isfile(path):
            st = os.stat(path)
            external.append({"path": path, "sha256": sha(path),
                             "size": st.st_size, "mtime_ns": st.st_mtime_ns})

    record = {
        "producer": os.path.abspath(__file__),
        "python": sys.version,
        "orig_argv": getattr(sys, "orig_argv", sys.argv),
        "lane": LANE,
        "baseline_revision": base,
        "source_revision": source,
        "source_branch": pin.get("branch"),
        "source_remote": pin.get("remote"),
        "source_pushed": pin.get("pushed"),
        "head_revision": pin.get("head"),
        "head_equals_source": pin.get("head_equals_source"),
        "source_revpin_sha256": revpin_sha,
        "worktree_dirty_tracked_at_start": dirty,
        "expected_exits_table": dict(EXPECTED_EXITS),
        "labels_source": labels_source,
        "c3_evidence_scope": "receipts/observations read from W19/runs as written; "
                             "predictions read from the source blob",
        "c1_census_before": before_info,
        "tool_integrity": integrity,
        "tool_integrity_mismatches": integrity_mismatches,
        "external_tools": external,
        "commands": p.commands,
        "pins_pre": pins_pre,
        "pins_post": pins_post,
        "pins_compare": pin_compare,
        "pins_scope_note": "identical bytes at the two recorded instants only "
                           "(QUALITY #19)",
        "pycache_dirs_after_pass": pycache,
        "unexpected_exits": p.unexpected(),
        "checks": checks,
        "failed_checks": failed_checks,
    }
    write_json(W + "/verification.json", record)

    failures = []
    if record["unexpected_exits"]:
        failures.append("unexpected_exits: " + ", ".join(record["unexpected_exits"]))
    if not pin_compare["equal"]:
        failures.append("pins_changed: %r" % (pin_compare,))
    if pycache:
        failures.append("pycache_dirs: " + ", ".join(pycache))
    if integrity_mismatches:
        failures.append("tool_byte_mismatch: " + ", ".join(integrity_mismatches))
    failures.extend("check_failed: " + name for name in failed_checks)
    print(json.dumps({
        "commands": len(p.commands),
        "unexpected_exits": record["unexpected_exits"],
        "pins_equal": pin_compare["equal"],
        "source_revision": source,
        "source_branch": pin.get("branch"),
        "failed_checks": failed_checks,
        "tool_integrity_mismatches": integrity_mismatches,
        "failures": failures,
    }, indent=2))
    return 0 if not failures else 1


def main(argv=None) -> int:
    argv = list(sys.argv if argv is None else argv)
    if argv[1:] == ["--selftest"]:
        return selftest()
    if len(argv) != 2 or argv[1].startswith("-"):
        sys.stderr.write(USAGE)
        return 2
    return full_pass(argv[1])


if __name__ == "__main__":
    sys.exit(main())
