#!/usr/bin/env python3
"""Round-18 single post-integration execution pass (L1).

Runs every command below once, without a shell, from the lane root, and
retains argv, cwd, env overrides, UTC start/end, exit, and stdout/stderr
(files under verify/ with SHA-256). Producer/tool/prediction bytes are pinned
with round-17 tools/pins.py before and after the pass: equal maps show
identical bytes at those two instants, not continuity between them
(QUALITY #19).

`source` is resolved by round-18 tools/revpin.py `resolve_source(LANE)`
(refs/heads/main with require_pushed and require_head). Any RevPinError
finding (branch_missing, head_not_branch_tip, branch_not_pushed) refuses the
pass with exit 2 before a single command runs — jj-colocated lanes can leave
git HEAD on an off-branch commit, and HEAD is never used as a revision.

Usage: python3 -I -B verify.py BASELINE_REV   (writes verification.json + verify/)
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

sys.dont_write_bytecode = True
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
W17 = LANE + "/.ufo/waves/round-17"
W = LANE + "/.ufo/waves/round-18"
T = W + "/tools"
T17 = W17 + "/tools"
OUT = W + "/verify"
RUNS = W + "/runs"
PREDICTIONS = W + "/predictions"
PY = ["python3", "-I", "-B"]
GATES = LANE + "/.ufo/gates"
REVPIN = T + "/revpin.py"


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(*args):
    return subprocess.check_output(["git", "-C", LANE, *args], text=True).strip()


def run_labels():
    """Run labels: predictions/carriers.tsv column 1 when present, else the
    retained W18/runs/ directory names (sorted)."""
    tsv = os.path.join(PREDICTIONS, "carriers.tsv")
    labels = []
    if os.path.isfile(tsv):
        with open(tsv) as f:
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if parts and parts[0]:
                    labels.append(parts[0])
    if labels:
        return labels
    if os.path.isdir(RUNS):
        return sorted(d for d in os.listdir(RUNS)
                      if os.path.isdir(os.path.join(RUNS, d)))
    return []


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    base = git("rev-parse", "--verify", sys.argv[1] + "^{commit}")

    # jj-safe source pin: refuse before running anything on a finding.
    revpin = load_module("r18_revpin", REVPIN)
    try:
        pin = revpin.resolve_source(LANE)
    except revpin.RevPinError as exc:
        print(json.dumps({
            "refused": True,
            "revpin_finding": str(exc),
            "source": "unresolved: revpin.resolve_source refused before any command ran",
        }, sort_keys=True, indent=2))
        return 2
    source = pin["source"]
    dirty = git("status", "--porcelain", "--untracked-files=no")

    os.makedirs(OUT, exist_ok=True)
    pins = load_module("r17_pins", T17 + "/pins.py")
    pin_paths = sorted(
        [os.path.join(T, n) for n in os.listdir(T) if n.endswith(".py")]
        + [os.path.join(T17, n) for n in os.listdir(T17) if n.endswith(".py")]
        + [GATES + "/citation-drift/citation-drift-probe.py",
           GATES + "/custody-pair/custody-pair.py",
           W + "/run-carriers.sh", W + "/measure.py", W + "/controls.py",
           __file__]
        + [os.path.join(PREDICTIONS, n) for n in os.listdir(PREDICTIONS)
           if os.path.isfile(os.path.join(PREDICTIONS, n))])
    pins_pre = pins.snapshot(pin_paths)
    cmds = []

    def run(label, argv, expect=None, env=None):
        rec = {"label": label, "argv": argv, "cwd": LANE, "env_overrides": env or {},
               "started_at_utc": now(), "expected_exit": expect}
        so, se = os.path.join(OUT, label + ".stdout"), os.path.join(OUT, label + ".stderr")
        with open(so, "wb") as fo, open(se, "wb") as fe:
            p = subprocess.run(argv, cwd=LANE, stdout=fo, stderr=fe,
                               env={**os.environ, **(env or {})})
        rec.update({"ended_at_utc": now(), "exit": p.returncode,
                    "stdout_path": so, "stdout_sha256": sha(so),
                    "stderr_path": se, "stderr_sha256": sha(se)})
        rec["exit_as_expected"] = (expect is None) or (p.returncode == expect)
        cmds.append(rec)
        return so

    def skip(label, argv, expect, reason):
        """Record a command that could not run (missing prerequisite input)
        as an unevaluable unexpected exit instead of crashing the pass."""
        rec = {"label": label, "argv": argv, "cwd": LANE, "env_overrides": {},
               "started_at_utc": now(), "ended_at_utc": now(),
               "expected_exit": expect, "exit": 2,
               "skipped_reason": reason}
        so, se = os.path.join(OUT, label + ".stdout"), os.path.join(OUT, label + ".stderr")
        with open(so, "wb") as fo:
            fo.write(b"")
        with open(se, "wb") as fe:
            fe.write(("SKIPPED: " + reason + "\n").encode())
        rec.update({"stdout_path": so, "stdout_sha256": sha(so),
                    "stderr_path": se, "stderr_sha256": sha(se),
                    "exit_as_expected": False})
        cmds.append(rec)

    # pins CLI exercised on the W18 tool directory across the pass (pre-snapshot
    # here before the first command, post-snapshot at the end, then compare).
    tools_pre = sorted(os.path.join(T, n) for n in os.listdir(T) if n.endswith(".py"))
    run("pins-snapshot-pre", PY + [f"{T17}/pins.py", "snapshot",
                                   "--out", f"{OUT}/tools-pre.json"] + tools_pre, 0)

    # Selftests: every new/edited tool (all W18 tools, the four edited W17
    # tools plus the other r17 tools the pass invokes, the two edited gate
    # tools) plus measure.py/controls.py.
    for n in sorted(os.listdir(T)):
        if n.endswith(".py"):
            run("selftest-" + n[:-3], PY + [f"{T}/{n}", "--selftest"], 0)
    for tool in ["carrier-run", "compare", "invocation-audit", "log-extract",
                 "pins", "receipt-validate", "temporal-sweep"]:
        run("selftest-w17-" + tool, PY + [f"{T17}/{tool}.py", "--selftest"], 0)
    run("selftest-citation-drift-probe", PY + [
        f"{GATES}/citation-drift/citation-drift-probe.py", "--selftest"], 0)
    os.makedirs(OUT + "/scratch-custody", exist_ok=True)
    run("selftest-custody-pair", PY + [
        f"{GATES}/custody-pair/custody-pair.py", "selftest",
        "--scratch", f"{OUT}/scratch-custody"], 0)
    run("selftest-measure", PY + [f"{W}/measure.py", "--selftest"], 0)
    run("selftest-controls", PY + [f"{W}/controls.py", "--selftest"], 0)

    # C1: routed R17 defects at baseline and source (plain reporting; strict
    # would fail at baseline by design, so strict runs only at source).
    run("routed-defects-baseline", PY + [f"{T}/routed-defects.py", "--root", LANE,
                                         "--rev", base], 0)
    run("routed-defects-source", PY + [f"{T}/routed-defects.py", "--root", LANE,
                                       "--rev", source], 0)
    run("routed-defects-source-strict", PY + [f"{T}/routed-defects.py", "--root", LANE,
                                              "--rev", source, "--strict"], 0)

    # C2: live HEAD-as-revision sites; strict must fail at baseline, pass at
    # source.
    run("head-rev-lint-baseline-strict", PY + [f"{T}/head-rev-lint.py", "--root", LANE,
                                               "--rev", base, "--strict"], 1)
    run("head-rev-lint-source-strict", PY + [f"{T}/head-rev-lint.py", "--root", LANE,
                                             "--rev", source, "--strict"], 0)

    # C2 red-before: sandbox jj-colocated clone shows baseline forms fail and
    # fixed forms hold; writes its own retained receipt.
    run("jj-red-before", PY + [f"{T}/jj-red-before.py",
                               "--out", f"{OUT}/jj-red-before-receipt.json"], 0)

    # C3 / W18 runs: receipt validation and prediction-vs-observation compare
    # per retained run. Observation comes from the run's own observation.json
    # when retained, else a fresh log-extract over the bound Ghidra log.
    for lab in run_labels():
        rd = os.path.join(RUNS, lab)
        receipt = os.path.join(rd, "receipt.json")
        pred = os.path.join(PREDICTIONS, lab + ".prediction.json")
        if os.path.isfile(receipt):
            run("receipt-validate-" + lab, PY + [f"{T17}/receipt-validate.py", receipt], 0)
        else:
            skip("receipt-validate-" + lab, PY + [f"{T17}/receipt-validate.py", receipt],
                 0, "no receipt.json in " + rd)
        obs = os.path.join(rd, "observation.json")
        if not os.path.isfile(obs):
            obs = None
            log = None
            if os.path.isfile(receipt):
                try:
                    bound = json.load(open(receipt)).get("bound_sessions") or []
                    if bound:
                        log = os.path.join(rd, "logs", os.path.basename(bound[0]),
                                           "ghidra.log")
                except (OSError, ValueError):
                    log = None
            if log and os.path.isfile(log):
                obs = run("log-extract-" + lab, PY + [f"{T17}/log-extract.py",
                                                      "--log", log], 0)
        if not os.path.isfile(pred):
            skip("compare-" + lab,
                 PY + [f"{T17}/compare.py", "--prediction", pred,
                       "--observation", str(obs)],
                 0, "no prediction for label " + lab)
        elif obs is None:
            skip("compare-" + lab,
                 PY + [f"{T17}/compare.py", "--prediction", pred,
                       "--observation", "(none)"],
                 0, "no retained observation.json and no bound ghidra.log in " + rd)
        else:
            run("compare-" + lab, PY + [f"{T17}/compare.py", "--prediction", pred,
                                        "--observation", obs], 0)

    run("measure-baseline", PY + [f"{W}/measure.py", base], 0)
    run("measure-source", PY + [f"{W}/measure.py", source], 0)
    run("controls", PY + [f"{W}/controls.py", base, source], 0)

    run("citation-drift-strict", PY + [
        f"{GATES}/citation-drift/citation-drift-probe.py",
        "--root", LANE, "--rev", source,
        "--table", f"{GATES}/citation-drift/pointer-table.json",
        "--expected", f"{GATES}/citation-drift/expected.json",
        "--strict"], 0)

    run("temporal-sweep-source", PY + [f"{T17}/temporal-sweep.py", "--root", LANE,
                                       "--rev", source, "--sites-rev", base], 0)
    run("invocation-audit-source", PY + [f"{T17}/invocation-audit.py", "--root", LANE,
                                         "--rev", source], 0)

    run("sources-census", ["/home/vgpnk/Projects/shokunin/scripts/sources-census.sh",
                           "validate", "--root",
                           "/home/vgpnk/Projects/shokunin", "kaidoku"], 0)

    os.makedirs(W + "/custody", exist_ok=True)
    run("custody-capture", PY + [
        f"{GATES}/custody-pair/custody-pair.py", "capture",
        "--out", f"{W}/custody/custody-r18.v2.txt",
        "--label", "round-18"])

    # pins CLI exercised on the W18 tool directory across the pass: pre was
    # taken above before the first selftest, post here, then compare.
    tools = sorted(os.path.join(T, n) for n in os.listdir(T) if n.endswith(".py"))
    run("pins-snapshot-post", PY + [f"{T17}/pins.py", "snapshot",
                                    "--out", f"{OUT}/tools-post.json"] + tools, 0)
    run("pins-compare", PY + [f"{T17}/pins.py", "compare",
                              f"{OUT}/tools-pre.json", f"{OUT}/tools-post.json"], 0)

    pins_post = pins.snapshot(pin_paths)
    pycache = subprocess.run(["find", LANE + "/.ufo", "-name", "__pycache__"],
                             capture_output=True, text=True).stdout.split()
    record = {
        "producer": __file__, "python": sys.version, "orig_argv": sys.orig_argv,
        "baseline_revision": base,
        "source_revision": source,
        "source_branch": pin.get("branch"),
        "source_remote": pin.get("remote"),
        "source_pushed": pin.get("pushed"),
        "head_revision": pin.get("head"),
        "head_equals_source": pin.get("head_equals_source"),
        "worktree_dirty_tracked_at_start": dirty.splitlines(),
        "pycache_dirs_after_pass": pycache,
        "commands": cmds,
        "pins_pre": pins_pre, "pins_post": pins_post,
        "pins_compare": pins.compare(pins_pre, pins_post),
        "pins_scope_note": "identical bytes at the two recorded instants only (QUALITY #19)",
        "unexpected_exits": [c["label"] for c in cmds if not c["exit_as_expected"]],
    }
    with open(W + "/verification.json", "w") as f:
        json.dump(record, f, sort_keys=True, indent=2)
    print(json.dumps({"commands": len(cmds), "unexpected_exits": record["unexpected_exits"],
                      "pins_equal": record["pins_compare"]["equal"],
                      "source_revision": source,
                      "source_branch": pin.get("branch")}, indent=2))
    return 0 if (not record["unexpected_exits"] and record["pins_compare"]["equal"]
                 and not pycache) else 1


if __name__ == "__main__":
    sys.exit(main())
