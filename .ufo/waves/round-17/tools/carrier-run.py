#!/usr/bin/env python3
"""Round-17 carrier runner: retained REA analyze + searches on a Go carrier.

Runs `npx -y rea-agents@V inspect-go-binary|analyze|search` on a Go carrier
binary while polling for REA's ephemeral `/tmp/rea-ghidra-*` session dirs and
retaining each dir's `ghidra.log`/`script.log` into --out-dir/logs/<dirname>/
(copy to `*.tmp` then `os.replace`). Each mid-run pin check additionally
retains its full pin map under --out-dir/pins/mid-<n>.json with a recorded
sha256 (R17-PINMAP forward fix, round 18).

Limitation: REA deletes its runtime root at close; this is a polling copy, so
lines written after the final poll before deletion can be missing.
pins.snapshot proves only "same bytes at two instants", never "unchanged
throughout".

Usage: python3 -I carrier-run.py --carrier PATH --label LABEL --out-dir DIR
       [--rea-version 6.5.0] [--timeout 1800] [--poll 0.5] [--search NAME]...
       [--selftest]
"""
import argparse
import fnmatch
import glob
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
import tempfile
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
PIN_CHECK_S = 30.0
PINS_PATH = os.path.join(HERE, "pins.py")
R16_SELECTION = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/selection.py"
LOG_NAMES = ("ghidra.log", "script.log")
SESSION_GLOB = "/tmp/rea-ghidra-*"
LOG_CAPTURE_LIMIT = (
    "polling copy; lines written after the final poll before REA deletes "
    "its runtime root can be missing"
)


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pins(path):
    spec = importlib.util.spec_from_file_location("r17_pins", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sanitize(name):
    return re.sub(r"[^A-Za-z0-9._-]", "_", name) or "unnamed"


def list_session_dirs(session_glob):
    return {
        p
        for p in glob.glob(session_glob)
        if os.path.isdir(p) and not os.path.islink(p)
    }


class _DoneProc:
    """Popen-shaped result for an already-finished fake command."""

    def __init__(self, returncode):
        self.returncode = returncode

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        return self.returncode

    def kill(self):
        return None


def _popen(argv, cwd, stdout_f, stderr_f):
    return subprocess.Popen(argv, cwd=cwd, stdout=stdout_f, stderr=stderr_f)


def _private_runner(child_env):
    """Round-17 L1 integration (w1 SentinelPollRace/SentinelCarrierSafety F1/F2/F5):
    each REA child gets a private TMPDIR so only this run's rea-ghidra-* roots are
    visible to the poller, and its own session so a timeout can stop the group."""
    def run_(argv, cwd, stdout_f, stderr_f):
        return subprocess.Popen(argv, cwd=cwd, stdout=stdout_f, stderr=stderr_f,
                                env=child_env, start_new_session=True)
    return run_


def _stop_group(proc):
    """SIGTERM the child's process group, wait 15 s (REA's own close allows ~10 s),
    then SIGKILL; plain proc.kill() for injected fakes without a group."""
    import signal
    try:
        os.killpg(proc.pid, signal.SIGTERM)
        try:
            proc.wait(timeout=15)
            return "sigterm"
        except Exception:
            os.killpg(proc.pid, signal.SIGKILL)
            return "sigkill"
    except Exception:
        proc.kill()
        return "kill"


def bind_session(session_dir, files, carrier_sha256, carrier_md5=None):
    """Bind a retained session to this carrier from the log's own records:
    ghidra.log names its own path ('Using log file: <dir>/ghidra.log', component
    LoggingInitialization), the imported copy ('IMPORTING: file://<dir>/target-
    <sha256[:12]>.bin', component HeadlessAnalyzer) and, when given, the loader's
    full target MD5. Lines are matched whole, never as substrings (w2 BindingFuzz)."""
    out = {"logfile_ok": False, "target_ok": False, "md5_ok": None}
    ent = files.get("ghidra.log")
    if not ent or not carrier_sha256 or os.path.islink(ent["path"]):
        return out
    try:
        text = open(ent["path"], "rb").read().decode("utf-8", "replace")
    except OSError:
        return out
    lines = [ln.rstrip("\r").rstrip() for ln in text.split("\n")]
    out["logfile_ok"] = any(re.fullmatch(
        r"\S+ \S+ INFO +\(LoggingInitialization\) Using log file: "
        + re.escape("%s/ghidra.log" % session_dir), ln) for ln in lines)
    out["target_ok"] = any(re.fullmatch(
        r"\S+ \S+ INFO +\(HeadlessAnalyzer\) IMPORTING: "
        + re.escape("file://%s/target-%s.bin" % (session_dir, carrier_sha256[:12])), ln)
        for ln in lines)
    if carrier_md5:
        out["md5_ok"] = any(ln.startswith("Loading file://%s/target-%s.bin?MD5=%s"
                                          % (session_dir, carrier_sha256[:12], carrier_md5))
                            for ln in lines)
        out["target_ok"] = out["target_ok"] and out["md5_ok"]
    return out


def run_step(argv, name, out_dir, cwd, timeout, runner):
    """Spawn argv via runner, stream stdout/stderr to files, return step record."""
    started = utcnow()
    stdout_path = os.path.join(out_dir, name + ".json")
    stderr_path = os.path.join(out_dir, name + ".stderr")
    rec = {
        "argv": argv,
        "cwd": cwd,
        "started_at_utc": started,
    }
    try:
        with open(stdout_path, "wb") as out_f, open(stderr_path, "wb") as err_f:
            proc = runner(argv, cwd, out_f, err_f)
            try:
                exit_code = proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                rec["stop"] = _stop_group(proc)
                try:
                    proc.wait(timeout=10)
                except Exception:
                    pass
                rec["ended_at_utc"] = utcnow()
                rec["exit"] = None
                rec["timeout"] = True
                rec["error"] = "timeout after %ss" % timeout
                _finish_step(rec, stdout_path, stderr_path)
                return rec
    except OSError as e:
        rec["ended_at_utc"] = utcnow()
        rec["exit"] = None
        rec["error"] = "could not start: %s" % e
        _finish_step(rec, stdout_path, stderr_path)
        return rec
    rec["ended_at_utc"] = utcnow()
    rec["exit"] = exit_code
    _finish_step(rec, stdout_path, stderr_path)
    return rec


def _finish_step(rec, stdout_path, stderr_path):
    rec["stdout_path"] = stdout_path
    rec["stderr_path"] = stderr_path
    rec["stdout_sha256"] = sha256_file(stdout_path) if os.path.exists(stdout_path) else None
    rec["stderr_sha256"] = sha256_file(stderr_path) if os.path.exists(stderr_path) else None


class LogPoller:
    """Tracks new session dirs (relative to a pre-run baseline) and copies their
    ghidra.log/script.log into out_dir/logs/<dirname>/ via .tmp + os.replace."""

    def __init__(self, out_dir, session_glob, baseline):
        self.out_dir = out_dir
        self.session_glob = session_glob
        self.baseline = baseline
        self.tracked = {}  # session_dir -> {files: {name: {path, bytes, sha256}}, polls}

    def scan(self):
        now = utcnow()
        current = list_session_dirs(self.session_glob)
        for d in sorted(current - self.baseline):
            ent = self.tracked.get(d)
            if ent is None:
                ent = {"files": {}, "polls": 0, "last_copy_utc": None}
                self.tracked[d] = ent
            ent["polls"] += 1
            for name in LOG_NAMES:
                src = os.path.join(d, name)
                try:
                    if not (os.path.isfile(src) and not os.path.islink(src)):
                        continue
                    data = open(src, "rb").read()
                except OSError:
                    continue
                logs_dir = os.path.join(self.out_dir, "logs", os.path.basename(d))
                os.makedirs(logs_dir, exist_ok=True)
                dst = os.path.join(logs_dir, name)
                tmp = dst + ".tmp"
                try:
                    with open(tmp, "wb") as f:
                        f.write(data)
                    os.replace(tmp, dst)
                except OSError:
                    continue
                ent["files"][name] = {
                    "path": dst,
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "bytes": len(data),
                }
                ent["last_copy_utc"] = now

    def retained(self):
        return [
            {
                "session_dir": d,
                "files": ent["files"],
                "polls": ent["polls"],
                "last_copy_utc": ent["last_copy_utc"],
            }
            for d, ent in sorted(self.tracked.items())
        ]




def parse_evidence_id(stdout_path):
    try:
        with open(stdout_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("evidence_id")
    except (OSError, ValueError, AttributeError):
        return None


ENV_ALLOW = ("PATH", "HOME", "LANG", "LC_ALL", "LC_CTYPE", "USER", "LOGNAME", "SHELL",
             "GHIDRA_INSTALL_DIR", "JAVA_HOME", "GHIDRA_MAXMEM", "GHIDRA_HEADLESS_MAXMEM",
             "REA_LOG_LEVEL", "NPM_CONFIG_CACHE", "npm_config_cache")


def child_environment(private_root):
    """Round-17 L1 integration (w2 SentinelEnvLeak F1/F3, SentinelSessionResidue F1):
    allowlisted environment instead of a full copy, so tokens and agent sockets do
    not reach npx/REA/Ghidra; Node's compile cache is disabled so the private
    session parent can be removed."""
    env = {k: v for k, v in os.environ.items()
           if k in ENV_ALLOW or k.startswith("REA_GHIDRA_")}
    env["TMPDIR"] = private_root
    env["NODE_DISABLE_COMPILE_CACHE"] = "1"
    return env


def run(carrier, label, out_dir, rea_version="6.5.0", timeout=1800.0,
        poll=0.5, searches=(), runner=None, session_glob=SESSION_GLOB,
        pins_path=PINS_PATH, pin_paths=None, extra_pins=()):
    """Run the carrier pipeline; returns (receipt_dict, exit_code)."""
    carrier = os.path.realpath(carrier)  # pins.py keys by realpath (w2 CriticCapabilityRow F3)
    private_root = None
    child_env_keys = None
    if runner is None:
        if not os.path.isfile(carrier):
            return {"label": label, "carrier": {"path": carrier},
                    "error": "carrier unreadable: %s" % carrier}, 2
        # Private session parent: no dot-prefixed element (GhidraSessionRoot.js:28-38
        # falls back to /tmp otherwise), so REA places rea-ghidra-* roots under it.
        private_root = tempfile.mkdtemp(prefix="kr17-rea-", dir="/tmp")
        child_env = child_environment(private_root)
        child_env_keys = sorted(child_env)
        runner = _private_runner(child_env)
        session_glob = os.path.join(private_root, "rea-ghidra-*")
    runner = runner or _popen
    receipt = {
        "label": label,
        "carrier": {"path": carrier},
        "python": sys.version,
        "orig_argv": getattr(sys, "orig_argv", None),
        "log_capture_limit": LOG_CAPTURE_LIMIT,
        "steps": {},
        "retained_logs": [],
    }
    try:
        pins = load_pins(pins_path)
    except Exception as e:
        receipt["error"] = "pins module unavailable: %s" % e
        return receipt, 2
    if pin_paths is None:
        pin_paths = [carrier, R16_SELECTION]
    pin_paths = list(pin_paths) + [p for p in extra_pins if p not in pin_paths]
    receipt["session_parent"] = private_root or os.path.dirname(session_glob)
    receipt["child_env_keys"] = child_env_keys
    receipt["rea_ghidra_env"] = {k: v for k, v in os.environ.items()
                                 if k.startswith("REA_GHIDRA_")}
    if not os.path.isfile(carrier):
        receipt["error"] = "carrier unreadable: %s" % carrier
        return receipt, 2
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as e:
        receipt["error"] = "out-dir not writable: %s" % e
        return receipt, 2
    cwd = os.getcwd()

    pins_pre = pins.snapshot(pin_paths)
    receipt["pins_pre"] = pins_pre
    if pins_pre["entries"].get(carrier, {}).get("sha256"):
        receipt["carrier"]["sha256_pre"] = pins_pre["entries"][carrier]["sha256"]
        _md5 = hashlib.md5()
        with open(carrier, "rb") as _f:
            for _chunk in iter(lambda: _f.read(1 << 20), b""):
                _md5.update(_chunk)
        receipt["carrier"]["md5_pre"] = _md5.hexdigest()
    for p, ent in pins_pre["entries"].items():
        if "error" in ent:
            receipt["error"] = "pin failed for %s: %s" % (p, ent["error"])
            return receipt, 2

    npx_base = ["npx", "-y", "rea-agents@%s" % rea_version]
    steps = {}

    # Step 2: inspect-go-binary (fast; no session-log polling).
    steps["inspect-go-binary"] = run_step(
        npx_base + ["inspect-go-binary", carrier, "--format", "json"],
        "inspect-go", out_dir, cwd, timeout, runner)
    if steps["inspect-go-binary"].get("exit") is None:
        receipt["error"] = "inspect-go-binary step could not evaluate"
        receipt["steps"] = steps
        return receipt, 2

    # Step 3: baseline of existing session dirs, then polled analyze + searches.
    baseline = list_session_dirs(session_glob)
    receipt["session_dir_baseline"] = sorted(baseline)
    poller = LogPoller(out_dir, session_glob, baseline)


    # wire pins_pre once (compare-during-run uses the same pre snapshot)
    # R17-PINMAP forward fix (round 18): every mid-run pin check writes its
    # full snapshot to out_dir/pins/mid-<n>.json (n global across steps, never
    # reused) so the map, not only the comparator verdict, is retained.
    mid_map_counter = [0]

    def run_polled(name, argv):
        return _run_polled(name, argv, out_dir, cwd, timeout, poll, runner,
                           poller, pins, pins_pre, mid_map_counter)

    steps["analyze"] = run_polled(
        "analyze", npx_base + ["analyze", carrier, "--format", "json"])
    steps["analyze"]["evidence_id"] = parse_evidence_id(
        steps["analyze"]["stdout_path"])

    for i, name in enumerate(searches):
        sname = "search-%d-%s" % (i, sanitize(name))
        steps["search:" + name] = run_polled(
            sname,
            npx_base + ["search", carrier, "--pattern=%s" % name,
                        "--kind", "procedures", "--format", "json"])

    pins_post = pins.snapshot(pin_paths)
    pins_cmp = pins.compare(pins_pre, pins_post)
    receipt["pins_post"] = pins_post
    receipt["pins_compare"] = pins_cmp
    if pins_post["entries"].get(carrier, {}).get("sha256"):
        receipt["carrier"]["sha256_post"] = pins_post["entries"][carrier]["sha256"]
    receipt["steps"] = steps
    retained = poller.retained()
    carrier_sha = receipt["carrier"].get("sha256_pre")
    for ent in retained:
        ent["binding"] = bind_session(ent["session_dir"], ent["files"], carrier_sha,
                                      receipt["carrier"].get("md5_pre"))
    receipt["retained_logs"] = retained
    bound = [e["session_dir"] for e in retained
             if e["binding"]["logfile_ok"] and e["binding"]["target_ok"]]
    receipt["bound_sessions"] = bound
    receipt["unbound_sessions"] = [e["session_dir"] for e in retained
                                   if e["session_dir"] not in bound]
    if private_root is not None:
        try:
            leftovers = sorted(os.listdir(private_root))
        except OSError:
            leftovers = None
        receipt["session_parent_leftovers"] = leftovers
        if leftovers == []:
            os.rmdir(private_root)
    mid_drift = [n for n, s in steps.items()
                 if s.get("pins_changed_during_run")
                 or any(not c.get("equal") for c in s.get("pin_checks") or [])]
    receipt["mid_run_drift_steps"] = mid_drift
    try:
        receipt_path = os.path.join(out_dir, "receipt.json")
        with open(receipt_path, "w", encoding="utf-8") as f:
            json.dump(receipt, f, sort_keys=True, indent=2)
        receipt["receipt_path"] = receipt_path
    except OSError as e:
        receipt["error"] = "receipt write failed: %s" % e
        return receipt, 2
    if not pins_cmp["equal"] or mid_drift:
        return receipt, 1
    if steps["analyze"].get("exit") not in (0,) or any(
            s.get("timeout") for s in steps.values()):
        return receipt, 2
    # Exactly one bound session per polled REA step (analyze + each search), and a
    # leaked session parent (e.g. a surviving rea-ghidra-* root with session.json)
    # is never a clean run (w2 SentinelSessionResidue F2).
    if private_root is not None and (len(bound) != 1 + len(list(searches))
                                     or receipt.get("session_parent_leftovers")):
        return receipt, 2
    return receipt, 0


def _run_polled(name, argv, out_dir, cwd, timeout, poll, runner, poller, pins,
                pins_pre, mid_map_counter=None):
    started = utcnow()
    stdout_path = os.path.join(out_dir, name + ".json")
    stderr_path = os.path.join(out_dir, name + ".stderr")
    rec = {"argv": argv, "cwd": cwd, "started_at_utc": started, "polls": 0}
    try:
        out_f = open(stdout_path, "wb")
        err_f = open(stderr_path, "wb")
    except OSError as e:
        rec["ended_at_utc"] = utcnow()
        rec["exit"] = None
        rec["error"] = "cannot open output files: %s" % e
        rec["retained_logs"] = []
        return rec
    try:
        try:
            proc = runner(argv, cwd, out_f, err_f)
        except OSError as e:
            rec["ended_at_utc"] = utcnow()
            rec["exit"] = None
            rec["error"] = "could not start: %s" % e
            _finish_step(rec, stdout_path, stderr_path)
            rec["retained_logs"] = []
            return rec
        deadline = time.monotonic() + timeout
        last_pin_check = 0.0
        pin_paths = list(pins_pre["entries"])
        while proc.poll() is None:
            poller.scan()
            rec["polls"] += 1
            if time.monotonic() > deadline:
                rec["stop"] = _stop_group(proc)
                rec["timeout"] = True
                rec["error"] = "timeout after %ss" % timeout
                break
            # Throttled mid-run pin check: rehashing the carrier every poll
            # would dominate I/O on large binaries; every PIN_CHECK_S seconds.
            # Every check is retained with its instant (QUALITY #19), not only drift.
            now = time.monotonic()
            if now - last_pin_check >= PIN_CHECK_S:
                last_pin_check = now
                mid = pins.snapshot(pin_paths)
                cmp_mid = pins.compare(pins_pre, mid)
                check = {
                    "taken_at_utc": mid["taken_at_utc"],
                    "equal": cmp_mid["equal"],
                    "entries": len(mid["entries"]),
                    "changed": cmp_mid["changed"],
                    "missing": cmp_mid["missing"],
                }
                # Retain the full mid-run map with its digest (R17-PINMAP:
                # QUALITY #19 and the knowledge entry claim the map is kept,
                # not only the verdict). Naming is global, never per-step, so
                # later steps can never overwrite an earlier step's map.
                if mid_map_counter is not None:
                    mid_map_counter[0] += 1
                    map_path = os.path.join(
                        out_dir, "pins", "mid-%d.json" % mid_map_counter[0])
                    try:
                        payload = json.dumps(
                            mid, sort_keys=True, indent=2).encode("utf-8")
                        os.makedirs(os.path.dirname(map_path), exist_ok=True)
                        with open(map_path, "wb") as mf:
                            mf.write(payload)
                            mf.write(b"\n")
                        check["map_path"] = map_path
                        check["map_sha256"] = hashlib.sha256(
                            payload + b"\n").hexdigest()
                    except OSError as e:
                        # An unretained map is recorded, never silent
                        # (receipt-validate flags map_error).
                        check["map_error"] = "mid map write failed: %s" % e
                rec.setdefault("pin_checks", []).append(check)
                if not cmp_mid["equal"]:
                    rec["pins_changed_during_run"] = {
                        "changed": cmp_mid["changed"],
                        "missing": cmp_mid["missing"],
                    }
            time.sleep(min(poll, max(0.0, deadline - time.monotonic())))
        try:
            exit_code = proc.wait(timeout=10)
        except Exception:
            exit_code = proc.returncode
        poller.scan()  # final best-effort catch before REA deletes the root
        rec["ended_at_utc"] = utcnow()
        rec["exit"] = exit_code
        _finish_step(rec, stdout_path, stderr_path)
        rec["retained_logs"] = poller.retained()
        return rec
    finally:
        out_f.close()
        err_f.close()


def _selftest():
    """Exercise run() with an injected fake runner and session root.

    No REA/npx subprocess is launched for the tracked steps except fake
    children the selftest itself spawns under sys.executable.
    """
    import textwrap

    root = tempfile.mkdtemp(prefix="carrier-run-selftest-")
    cases = 0
    failures = []
    try:
        tmp_sessions = os.path.join(root, "tmp")
        out_dir = os.path.join(root, "out")
        os.makedirs(tmp_sessions)
        carrier = os.path.join(root, "carrier.bin")
        with open(carrier, "wb") as f:
            f.write(b"\x7fELF-fake-carrier")
        pins_src = os.path.join(root, "pins.py")
        with open(pins_src, "w") as f:
            f.write(textwrap.dedent('''
                import hashlib, os
                from datetime import datetime, timezone
                def snapshot(paths):
                    return {"taken_at_utc": datetime.now(timezone.utc).isoformat(),
                            "monotonic_ns": 0,
                            "entries": {p: ({"sha256": hashlib.sha256(open(p,"rb").read()).hexdigest(),
                                            "size": os.path.getsize(p),
                                            "mtime_ns": os.stat(p).st_mtime_ns}
                                           if os.path.exists(p) else {"error": "missing"})
                                        for p in paths}}
                def compare(pre, post):
                    changed = [p for p in pre["entries"]
                               if pre["entries"][p] != post["entries"].get(p)]
                    missing = [p for p in post["entries"] if p not in pre["entries"]]
                    return {"equal": not changed and not missing
                            and not any("error" in e for e in post["entries"].values()),
                            "changed": changed, "missing": missing,
                            "pre_taken_at_utc": pre["taken_at_utc"],
                            "post_taken_at_utc": post["taken_at_utc"]}
            '''))
        glob_pat = os.path.join(tmp_sessions, "rea-ghidra-*")

        # A pre-existing session dir must never be copied (baseline exclusion).
        pre_existing = os.path.join(tmp_sessions, "rea-ghidra-AAAAAA")
        os.makedirs(pre_existing)
        with open(os.path.join(pre_existing, "ghidra.log"), "w") as f:
            f.write("pre-existing baseline dir\n")

        child_src = textwrap.dedent('''
            import json, os, shutil, sys, time
            root, name, lifespan = sys.argv[1], sys.argv[2], float(sys.argv[3])
            d = os.path.join(root, name)
            os.makedirs(d)
            with open(os.path.join(d, "ghidra.log"), "w") as f:
                f.write("line1\\n"); f.flush()
            time.sleep(lifespan / 2)
            with open(os.path.join(d, "script.log"), "w") as f:
                f.write("s1\\n")
            with open(os.path.join(d, "ghidra.log"), "a") as f:
                f.write("line2\\n")
            time.sleep(lifespan / 2)
            print(json.dumps({"evidence_id": "fake-ev", "normalized_result": {}}))
            shutil.rmtree(d, ignore_errors=True)
            sys.exit(int(sys.argv[4]))
        ''')
        child_py = os.path.join(root, "fake_child.py")
        with open(child_py, "w") as f:
            f.write(child_src)

        def fake_runner(argv, cwd, out_f, err_f):
            joined = " ".join(argv)
            if "inspect-go-binary" in joined:
                out_f.write(json.dumps(
                    {"evidence_id": "insp-fake",
                     "normalized_result": {"build_info": {"go_version": "go1.23.12"}}
                     }).encode())
                out_f.flush()
                return _DoneProc(0)
            if "analyze" in joined:
                return subprocess.Popen(
                    [sys.executable, child_py, tmp_sessions,
                     "rea-ghidra-FAKE01", "0.3", "0"],
                    cwd=cwd, stdout=out_f, stderr=err_f)
            if argv[3] == "search":
                out_f.write(b'{"evidence_id": "search-fake", "matches": []}')
                out_f.flush()
                return _DoneProc(0)
            err_f.write(b"unhandled argv")
            err_f.flush()
            return _DoneProc(127)

        # Case 1: happy path — logs retained from a deleted session dir.
        receipt, code = run(
            carrier=carrier, label="selftest", out_dir=out_dir,
            timeout=30.0, poll=0.03, searches=["main.main"],
            runner=fake_runner, session_glob=glob_pat, pins_path=pins_src,
            pin_paths=[carrier])
        cases += 1
        sess = os.path.join(tmp_sessions, "rea-ghidra-FAKE01")
        ok = (
            code == 0
            and not os.path.exists(sess)
            and os.path.isfile(os.path.join(out_dir, "logs", "rea-ghidra-FAKE01", "ghidra.log"))
            and "line1" in open(os.path.join(out_dir, "logs", "rea-ghidra-FAKE01", "ghidra.log")).read()
            and receipt["steps"]["analyze"]["evidence_id"] == "fake-ev"
            and receipt["steps"]["inspect-go-binary"]["exit"] == 0
            and "search:main.main" in receipt["steps"]
            and receipt["steps"]["search:main.main"]["exit"] == 0
            and receipt["pins_compare"]["equal"]
            and all(c.get("map_path") and os.path.isfile(c["map_path"])
                    and sha256_file(c["map_path"]) == c.get("map_sha256")
                    for s in receipt["steps"].values()
                    for c in s.get("pin_checks") or [])
            and not os.path.exists(os.path.join(out_dir, "logs", "rea-ghidra-AAAAAA"))
            and os.path.isfile(os.path.join(out_dir, "inspect-go.json"))
            and os.path.isfile(os.path.join(out_dir, "analyze.json"))
            and os.path.isfile(os.path.join(out_dir, "search-0-main.main.json"))
        )
        if not ok:
            failures.append("case1 happy path: code=%r receipt=%r" % (code, receipt))

        # Case 2: analyze exits nonzero -> run() must return 2, receipt records
        # the nonzero exit.
        def runner_fail(argv, cwd, out_f, err_f):
            if "analyze" in " ".join(argv):
                return subprocess.Popen(
                    [sys.executable, child_py, tmp_sessions,
                     "rea-ghidra-FAIL01", "0.1", "3"],
                    cwd=cwd, stdout=out_f, stderr=err_f)
            return fake_runner(argv, cwd, out_f, err_f)

        receipt2, code2 = run(
            carrier=carrier, label="selftest-fail", out_dir=os.path.join(root, "out2"),
            timeout=30.0, poll=0.03, searches=(),
            runner=runner_fail, session_glob=glob_pat, pins_path=pins_src,
            pin_paths=[carrier])
        cases += 1
        if not (code2 == 2 and receipt2["steps"]["analyze"]["exit"] == 3):
            failures.append("case2 nonzero analyze: code=%r" % code2)

        # Case 3: carrier bytes mutated before analyze starts -> the first
        # mid-run pin check records the drift and retains its full map under
        # out3/pins/, the run exits 1 (R17-PINMAP: the map itself is kept).
        out3 = os.path.join(root, "out3")

        def runner_mutate(argv, cwd, out_f, err_f):
            if "analyze" in " ".join(argv):
                with open(carrier, "wb") as f:
                    f.write(b"\x7fELF-mutated-mid-run")
                return subprocess.Popen(
                    [sys.executable, child_py, tmp_sessions,
                     "rea-ghidra-DRIFT1", "0.3", "0"],
                    cwd=cwd, stdout=out_f, stderr=err_f)
            return fake_runner(argv, cwd, out_f, err_f)

        receipt3, code3 = run(
            carrier=carrier, label="selftest-drift", out_dir=out3,
            timeout=30.0, poll=0.03, searches=(),
            runner=runner_mutate, session_glob=glob_pat, pins_path=pins_src,
            pin_paths=[carrier])
        cases += 1
        pchecks3 = receipt3["steps"]["analyze"].get("pin_checks") or []
        ok3 = (
            code3 == 1
            and receipt3.get("mid_run_drift_steps") == ["analyze"]
            and pchecks3
            and any(not c.get("equal") for c in pchecks3)
            and all(c.get("map_path")
                    and os.path.dirname(c["map_path"]) ==
                    os.path.join(out3, "pins")
                    and os.path.isfile(c["map_path"])
                    and sha256_file(c["map_path"]) == c.get("map_sha256")
                    for c in pchecks3)
        )
        if not ok3:
            failures.append("case3 mid-run drift map: code=%r" % code3)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    if failures:
        print("SELFTEST: FAILED %s" % "; ".join(failures))
        return 1
    print("SELFTEST: CLEAN cases=%d" % cases)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--carrier", help="Go carrier binary path (never executed)")
    ap.add_argument("--label", help="Run label recorded in the receipt")
    ap.add_argument("--out-dir", help="Directory for receipts, outputs, retained logs")
    ap.add_argument("--rea-version", default="6.5.0")
    ap.add_argument("--timeout", type=float, default=1800.0,
                    help="Per-step timeout seconds (default 1800)")
    ap.add_argument("--poll", type=float, default=0.5,
                    help="Session-dir poll interval seconds (default 0.5)")
    ap.add_argument("--search", action="append", default=[],
                    help="Procedure pattern to search after analyze (repeatable)")
    ap.add_argument("--pin", action="append", default=[],
                    help="Extra path pinned pre/mid/post (repeatable)")
    ap.add_argument("--selftest", action="store_true",
                    help="Run internal fixtures only; no REA invocation")
    args = ap.parse_args(argv)
    if args.selftest:
        return _selftest()
    if not (args.carrier and args.label and args.out_dir):
        ap.error("--carrier, --label and --out-dir are required")
    receipt, code = run(
        carrier=args.carrier, label=args.label, out_dir=args.out_dir,
        rea_version=args.rea_version, timeout=args.timeout, poll=args.poll,
        searches=args.search, extra_pins=[os.path.abspath(p) for p in args.pin])
    print(json.dumps(receipt, sort_keys=True, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
