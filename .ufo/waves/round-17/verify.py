#!/usr/bin/env python3
"""Round-17 single post-integration execution pass (L1).

Runs every command below once, without a shell, from the lane root, and
retains argv, cwd, env overrides, UTC start/end, exit, and stdout/stderr
(files under verify/ with SHA-256). Producer/tool/prediction bytes are pinned
with tools/pins.py before and after the pass: equal maps show identical bytes
at those two instants, not continuity between them (QUALITY #19).

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
W = LANE + "/.ufo/waves/round-17"
T = W + "/tools"
OUT = W + "/verify"
GODATA = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang"
PY = ["python3", "-I", "-B"]
LABELS = ["calib-shfmt", "calib-esbuild-0.25.12", "pro-notesmd-cli", "pro-aether",
          "pro-esbuild-0.21.5", "pro-containerd-shim", "pro-esbuild-0.27.7", "pro-op"]


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pins():
    spec = importlib.util.spec_from_file_location("r17_pins", T + "/pins.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(*args):
    return subprocess.check_output(["git", "-C", LANE, *args], text=True).strip()


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    base = git("rev-parse", "--verify", sys.argv[1] + "^{commit}")
    source = git("rev-parse", "HEAD")
    dirty = git("status", "--porcelain")
    os.makedirs(OUT, exist_ok=True)
    pins = load_pins()
    pin_paths = sorted(
        [os.path.join(T, n) for n in os.listdir(T) if n.endswith(".py")]
        + [W + "/run-carriers.sh", W + "/measure.py", W + "/controls.py", __file__]
        + [os.path.join(W, "predictions", n) for n in os.listdir(W + "/predictions")])
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

    for tool in ["pins", "retain", "carrier-run", "log-extract", "predict", "compare",
                 "receipt-validate", "temporal-sweep", "invocation-audit",
                 "buildinfo-probe", "carrier-census"]:
        run("selftest-" + tool, PY + [f"{T}/{tool}.py", "--selftest"], 0)
    run("selftest-measure", PY + [f"{W}/measure.py", "--selftest"], 0)
    run("selftest-controls", PY + [f"{W}/controls.py", "--selftest"], 0)

    for lab in LABELS:
        rd = f"{W}/runs/{lab}"
        run("receipt-validate-" + lab, PY + [f"{T}/receipt-validate.py", f"{rd}/receipt.json"], 0)
        bound = json.load(open(f"{rd}/receipt.json"))["bound_sessions"][0]
        log = f"{rd}/logs/{os.path.basename(bound)}/ghidra.log"
        obs = run("log-extract-" + lab, PY + [f"{T}/log-extract.py", "--log", log], 0)
        run("compare-" + lab, PY + [f"{T}/compare.py", "--prediction",
                                     f"{W}/predictions/{lab}.prediction.json",
                                     "--observation", obs], 0)
        gv = json.load(open(f"{W}/predictions/{lab}.inspect-go.json"))
        gv = ((gv.get("normalized_result") or {}).get("build_info") or {}).get("go_version") or ""
        run("predict-" + lab, PY + [f"{T}/predict.py", "--go-version", gv,
                                     "--golang-root", GODATA], 2 if gv == "" else 0)
        carrier = json.load(open(f"{rd}/receipt.json"))["carrier"]["path"]
        run("buildinfo-probe-" + lab, PY + [f"{T}/buildinfo-probe.py", carrier], 0)
        # Official Go toolchain reader (S024; reads the file, never runs it).
        run("go-version-m-" + lab, ["/home/vgpnk/.local/opt/go-1.27.3/bin/go", "version", "-m",
                                    carrier], 1 if gv == "" else 0)

    # Red demonstration for the route fields (Mistakes row 6): force the notesmd-cli
    # prediction's route to `info`; compare must fail. The contract's three fields alone pass.
    pred = json.load(open(f"{W}/predictions/pro-notesmd-cli.prediction.json"))
    red = json.loads(json.dumps(pred)); red["expected"]["snapshot_route"] = "info"
    red["expected"]["fallback_to"] = None
    three = json.loads(json.dumps(pred))
    for k in ("snapshot_route", "fallback_to"):
        three["expected"].pop(k)
    for name, obj in (("route-red", red), ("route-three-fields", three)):
        with open(f"{OUT}/{name}.prediction.json", "w") as f:
            json.dump(obj, f, sort_keys=True, indent=2)
    obs = f"{OUT}/log-extract-pro-notesmd-cli.stdout"
    run("compare-route-red", PY + [f"{T}/compare.py", "--prediction",
                                   f"{OUT}/route-red.prediction.json", "--observation", obs], 1)
    run("compare-three-fields", PY + [f"{T}/compare.py", "--prediction",
                                      f"{OUT}/route-three-fields.prediction.json",
                                      "--observation", obs], 0)

    run("temporal-sweep-baseline", PY + [f"{T}/temporal-sweep.py", "--root", LANE,
                                         "--rev", base, "--sites-rev", base], 0)
    run("temporal-sweep-source", PY + [f"{T}/temporal-sweep.py", "--root", LANE,
                                       "--rev", source, "--sites-rev", base], 0)
    run("invocation-audit-baseline", PY + [f"{T}/invocation-audit.py", "--root", LANE,
                                           "--rev", base], 0)
    run("controls", PY + [f"{W}/controls.py", base, source], 0)
    run("measure-baseline", PY + [f"{W}/measure.py", base], 0)
    run("measure-source", PY + [f"{W}/measure.py", source], 0)

    run("citation-strict", ["python3", "-I", f"{LANE}/.ufo/gates/citation-drift/citation-drift-probe.py",
                            "--root", LANE, "--rev", source, "--table",
                            f"{LANE}/.ufo/gates/citation-drift/pointer-table.json",
                            "--expected", f"{LANE}/.ufo/gates/citation-drift/expected.json",
                            "--strict"], 0)
    os.makedirs(W + "/custody", exist_ok=True)
    run("custody-capture", ["python3", "-I", f"{LANE}/.ufo/gates/custody-pair/custody-pair.py",
                            "capture", "--out", f"{W}/custody/custody-r17.v2.txt",
                            "--label", "round-17"])
    run("quote-selftest", ["python3", "-I", f"{LANE}/.ufo/waves/round-14/tools/quote-fidelity.py",
                           "--selftest"], 0)
    run("quote-original-frozen", ["python3", "-I", f"{LANE}/.ufo/waves/round-14/tools/quote-fidelity.py",
                                  "--frozen", f"{LANE}/.ufo/waves/round-14/fixtures/expected.json"], 0)
    run("quote-supplement-frozen", ["python3", "-I", f"{LANE}/.ufo/waves/round-14/tools/quote-fidelity.py",
                                    "--frozen", f"{LANE}/.ufo/waves/round-15/boundary-fixtures/expected.json"], 0)
    run("sources-census", ["/home/vgpnk/Projects/shokunin/scripts/sources-census.sh", "validate",
                           "--root", "/home/vgpnk/Projects/shokunin", "kaidoku"], 0)

    # pins CLI exercised on two snapshots of the tool directory taken around a replicate run.
    tools = sorted(os.path.join(T, n) for n in os.listdir(T) if n.endswith(".py"))
    run("pins-snapshot-pre", PY + [f"{T}/pins.py", "snapshot", "--out", f"{OUT}/tools-pre.json"] + tools, 0)
    run("go-carrier-run-replicate", ["bash", f"{W}/run-carriers.sh", "calib-shfmt"], 0,
        env={"RUNS_DIR": "verify/replicate"})
    run("pins-snapshot-post", PY + [f"{T}/pins.py", "snapshot", "--out", f"{OUT}/tools-post.json"] + tools, 0)
    run("pins-compare", PY + [f"{T}/pins.py", "compare", f"{OUT}/tools-pre.json",
                              f"{OUT}/tools-post.json"], 0)

    pins_post = pins.snapshot(pin_paths)
    pycache = subprocess.run(["find", LANE + "/.ufo", "-name", "__pycache__"],
                             capture_output=True, text=True).stdout.split()
    record = {
        "producer": __file__, "python": sys.version, "orig_argv": sys.orig_argv,
        "baseline_revision": base, "source_revision": source,
        "worktree_dirty_at_start": dirty.splitlines(),
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
                      "source_revision": source}, indent=2))
    return 0 if (not record["unexpected_exits"] and record["pins_compare"]["equal"]
                 and not pycache) else 1


if __name__ == "__main__":
    sys.exit(main())
