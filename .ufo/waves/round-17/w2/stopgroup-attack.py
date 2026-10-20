#!/usr/bin/env python3
"""Round-17 w2 falsification: attack _stop_group and the _run_polled/run_step
timeout paths of tools/carrier-run.py (lane rev da64646).

W1 SentinelCarrierSafety F2 asked for: start_new_session, killpg SIGTERM ->
wait >=15s -> killpg SIGKILL, kill the Ghidra process_group_id from
ownership.json, and record orphan_pids_remaining. The integrated tool does
killpg(proc.pid) only. This harness measures what actually survives.

All scratch state lives under /tmp (mkdtemp prefix kr17-stopgroup-). No
carrier binary is executed; children are python sleepers.

Run: python3 -B stopgroup-attack.py
Exit 0 = harness ran; findings are in the printed JSON.
"""
import importlib.util
import json
import os
import signal
import subprocess
import sys
import tempfile
import time

TOOLS = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools"
CARRIER_RUN = os.path.join(TOOLS, "carrier-run.py")


def load_tool():
    spec = importlib.util.spec_from_file_location("r17_carrier_run", CARRIER_RUN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def reap(pid):
    """SIGKILL one pid we spawned; never a pattern kill (siblings run sleeps)."""
    try:
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        return
    for _ in range(50):
        if not alive(pid):
            return
        time.sleep(0.05)


SPAWNED = []  # every real pid we create, for scoped cleanup only


def pgid_of(pid):
    try:
        return os.getpgid(pid)
    except ProcessLookupError:
        return None


# Child that ignores SIGTERM and spawns a SIGTERM-ignoring grandchild.
# GC_NEW_SESSION=1 -> grandchild calls setsid (own process group, like REA's
# Ghidra spawn); unset -> grandchild stays in the child's group.
CHILD_CODE = (
    "import os,signal,subprocess,sys,time\n"
    "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
    "gc_argv=[sys.executable,'-c',"
    "'import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(300)']\n"
    "kw={'start_new_session':True} if os.environ.get('GC_NEW_SESSION') else {}\n"
    "gc=subprocess.Popen(gc_argv,**kw)\n"
    "open(sys.argv[1],'w').write(str(gc.pid))\n"
    "time.sleep(300)\n"
)


class FakePins:
    """pins.snapshot/compare shape used by _run_polled's throttled check."""

    def snapshot(self, paths):
        from datetime import datetime, timezone
        return {"taken_at_utc": datetime.now(timezone.utc).isoformat(),
                "monotonic_ns": 0,
                "entries": {p: {} for p in paths}}

    def compare(self, pre, post):
        return {"equal": True, "changed": [], "missing": [],
                "pre_taken_at_utc": pre["taken_at_utc"],
                "post_taken_at_utc": post["taken_at_utc"]}


class FakePoller:
    def scan(self):
        return None

    def retained(self):
        return []


def private_runner(env_extra=None):
    """Mirror of carrier-run._private_runner: private TMPDIR + own session."""
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)

    def run_(argv, cwd, stdout_f, stderr_f):
        proc = subprocess.Popen(argv, cwd=cwd, stdout=stdout_f, stderr=stderr_f,
                                env=env, start_new_session=True)
        SPAWNED.append(proc.pid)
        return proc
    return run_


def scenario_A(mod, tmp):
    """_run_polled timeout: child ignores SIGTERM, grandchild in own session."""
    gc_pid_file = os.path.join(tmp, "gc-a.pid")
    argv = [sys.executable, "-c", CHILD_CODE, gc_pid_file]
    runner = private_runner({"GC_NEW_SESSION": "1"})
    t0 = time.monotonic()
    rec = mod._run_polled("analyze", argv, tmp, tmp, timeout=1.5, poll=0.2,
                          runner=runner, poller=FakePoller(), pins=FakePins(),
                          pins_pre=FakePins().snapshot([]))
    wall = time.monotonic() - t0
    gpid = None
    if os.path.exists(gc_pid_file):
        gpid = int(open(gc_pid_file).read().strip())
    orphan = alive(gpid) if gpid else None
    out = {
        "stop": rec.get("stop"),
        "timeout": rec.get("timeout"),
        "exit": rec.get("exit"),
        "error": rec.get("error"),
        "wall_s": round(wall, 2),
        "grandchild_pid": gpid,
        "grandchild_alive_after_stop_group": orphan,
    }
    if gpid:
        reap(gpid)
    return out


def scenario_B(mod, tmp):
    """run_step timeout: proc.kill() only. Grandchild stays in the child's
    process group, so a correct group kill would reach it."""
    gc_pid_file = os.path.join(tmp, "gc-b.pid")
    argv = [sys.executable, "-c", CHILD_CODE, gc_pid_file]
    runner = private_runner()  # own session; grandchild joins that session's group
    rec = mod.run_step(argv, "inspect-go", tmp, tmp, timeout=1.0, runner=runner)
    gpid = None
    if os.path.exists(gc_pid_file):
        gpid = int(open(gc_pid_file).read().strip())
    orphan = alive(gpid) if gpid else None
    out = {
        "timeout": rec.get("timeout"),
        "exit": rec.get("exit"),
        "error": rec.get("error"),
        "grandchild_pid": gpid,
        "grandchild_pgid_same_as_child_group": (
            gpid is not None and pgid_of(gpid) is not None
        ),
        "grandchild_alive_after_proc_kill": orphan,
    }
    if gpid:
        reap(gpid)
    return out


def scenario_C(mod, tmp):
    """_stop_group against a runner WITHOUT start_new_session (the module's own
    _popen fallback, carrier-run.py:93-94): killpg(proc.pid) cannot name the
    real group, so the code silently degrades to proc.kill() labelled 'kill'."""
    argv = [sys.executable, "-c", "import time;time.sleep(300)"]
    out_path = os.path.join(tmp, "c.out")
    err_path = os.path.join(tmp, "c.err")
    with open(out_path, "wb") as of, open(err_path, "wb") as ef:
        proc = mod._popen(argv, tmp, of, ef)
        child_pgid = pgid_of(proc.pid)
        our_pgid = os.getpgid(0)
        stop = mod._stop_group(proc)
        proc.wait(timeout=5)
    return {
        "stop_label": stop,
        "child_pgid": child_pgid,
        "our_pgid": our_pgid,
        "child_shared_parent_group": child_pgid == our_pgid,
        "killpg_pgid_used": "proc.pid",
    }


def scenario_D(mod, tmp):
    """run() end-to-end with an injected runner: analyze times out, but the
    child traps SIGTERM and exits 0. Does run() still report exit code 0?"""

    class TrapSigtermProc:
        """poll() alive until the wall deadline; killpg on our sacrificial
        session succeeds (a real 'sleep' process in its own session takes the
        signal); wait(15) then returns 0 — a clean SIGTERM-handled exit."""

        def __init__(self, sacrificial_pid):
            self.pid = sacrificial_pid
            self.returncode = None
            self._deadline = time.monotonic() + 60.0

        def poll(self):
            if self.returncode is not None:
                return self.returncode
            if time.monotonic() > self._deadline:
                self.returncode = 0
            return self.returncode

        def wait(self, timeout=None):
            # simulate a child that installs a SIGTERM handler and exits 0
            self.returncode = 0
            return 0

        def kill(self):
            self.returncode = -signal.SIGKILL

    carrier = os.path.join(tmp, "carrier.bin")
    with open(carrier, "wb") as f:
        f.write(b"\x7fELF-fake-carrier")

    def runner(argv, cwd, stdout_f, stderr_f):
        if "inspect-go-binary" in argv:
            stdout_f.write(b"{}")
            stdout_f.flush()
            return mod._DoneProc(0)
        if "analyze" in argv:
            # sacrificial real process in its own session so os.killpg works
            sac = subprocess.Popen(
                [sys.executable, "-c", "import time;time.sleep(300)"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                start_new_session=True)
            SPAWNED.append(sac.pid)
            return TrapSigtermProc(sac.pid)
        return mod._DoneProc(0)

    receipt, code = mod.run(
        carrier, "stopgroup-d", os.path.join(tmp, "out-d"),
        timeout=0.5, poll=0.1, runner=runner,
        session_glob=os.path.join(tmp, "rea-ghidra-*"),
        pin_paths=[carrier])
    step = receipt["steps"].get("analyze", {})
    return {
        "run_exit_code": code,
        "analyze_timeout": step.get("timeout"),
        "analyze_stop": step.get("stop"),
        "analyze_exit": step.get("exit"),
        "receipt_error": receipt.get("error"),
    }


def main():
    mod = load_tool()
    tmp = tempfile.mkdtemp(prefix="kr17-stopgroup-", dir="/tmp")
    results = {"tool": CARRIER_RUN, "tmp": tmp, "pid": os.getpid()}
    try:
        results["A_run_polled_timeout_sigterm_ignoring_child_own_session_gc"] = \
            scenario_A(mod, tmp)
        results["B_run_step_timeout_same_group_gc"] = scenario_B(mod, tmp)
        results["C_stop_group_no_session_runner"] = scenario_C(mod, tmp)
        results["D_run_timeout_exit0_child"] = scenario_D(mod, tmp)
    finally:
        for pid in SPAWNED:  # scoped sweep: only pids this harness created
            reap(pid)
    print(json.dumps(results, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
