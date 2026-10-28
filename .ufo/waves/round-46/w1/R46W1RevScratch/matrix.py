#!/usr/bin/env python3
"""R46W1RevScratch: attack the R45-CL20 scratch policy of tools/round-46/gate.py.

Runs both counters (attest.py = C1, registry.py = C2) at pairs where the artefact is
structurally green, so `gate.scratch()` is actually consulted, under each scratch-root
environment.  Records for every run: the exact command, exit code, stdout sha256, UTC
time, and what appeared under /tmp, /var/tmp and /dev/shm during the window.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r46/R46W1RevScratch"
PY = sys.executable
C1 = ("6e018068aaf9beb3c66ed270aeee08b300531976",
      "6e018068aaf9beb3c66ed270aeee08b300531976")   # structural green, battery runs
C2 = ("781e19ae674225b6be0b5de56ee8574679bac0b6",
      "781e19ae674225b6be0b5de56ee8574679bac0b6")
TMP_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
OUR_MARKERS = ("kaidoku", "fx-", "self-", "battery", "regsrc", "r46")


def utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def new_under(root, since_epoch):
    """Entries under root whose mtime is newer than since_epoch (wall clock)."""
    p = subprocess.run(["find", root, "-xdev", "-mindepth", "1", "-maxdepth", "3",
                        "-newermt", "@%d" % int(since_epoch), "-printf", "%p\t%T@\n"],
                       capture_output=True, text=True)
    return [ln.split("\t")[0] for ln in p.stdout.splitlines() if ln]


def listdir_safe(path):
    try:
        return sorted(os.listdir(path))
    except OSError as exc:
        return ["<%s: %s>" % (type(exc).__name__, exc.strerror)]


def run(counter, freeze, rev, env, cwd, extra=()):
    script = os.path.join(LANE, "tools", "round-46", counter)
    cmd = [PY, "-I", "-B", script, "--root", LANE, "--freeze", freeze, "--rev", rev,
           *extra]
    t0 = time.time()
    started = utc()
    p = subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, text=True,
                       timeout=600)
    return {
        "counter": counter, "cmd": " ".join(cmd), "cwd": cwd,
        "started_utc": started, "seconds": round(time.time() - t0, 2),
        "exit": p.returncode, "stdout_sha256": sha(p.stdout),
        "stderr_sha256": sha(p.stderr),
        "stderr_tail": p.stderr[-400:],
        "_stdout": p.stdout,
    }, t0


def summarize(stdout):
    try:
        d = json.loads(stdout)
    except Exception:
        return {"parse": "failed"}
    out = {}
    for k in ("met_target", "reason", "failing", "block_present", "rows",
              "unregistered", "thin", "absent_at_rev", "frozen_path_changed"):
        if k in d:
            out[k] = d[k] if not isinstance(d[k], list) else d[k][:6]
    b = d.get("battery") or {}
    if b:
        out["battery"] = {k: b.get(k) for k in
                          ("forgeries_total", "v1_green", "v2_green", "v2_crash",
                           "genuine_green", "skipped")}
        if "fixtures" in b:
            out["battery"]["fixtures"] = len(b["fixtures"])
    if "met_target" not in out:
        out["raw_head"] = stdout[:200]
    return out


CASES = [
    # name, env overrides (None = unset), cwd, expected exit per policy, why
    ("unset_both", {"HYAKU_SCRATCH": None, "TMPDIR": None}, LANE, 2,
     "no root set: refuse, never degrade to /tmp"),
    ("hk_tmp", {"HYAKU_SCRATCH": "/tmp"}, LANE, 2, "bare /tmp refused"),
    ("hk_tmp_trailing", {"HYAKU_SCRATCH": "/tmp/"}, LANE, 2, "trailing slash still /tmp"),
    ("hk_double_slash", {"HYAKU_SCRATCH": "//tmp"}, LANE, 2, "//tmp is /tmp on Linux"),
    ("hk_dotdot", {"HYAKU_SCRATCH": "/fast/scratch/../../tmp"}, LANE, 2,
     "path through .. resolves to /tmp"),
    ("hk_symlink_tmp", {"HYAKU_SCRATCH": S + "/linktmp"}, LANE, 2,
     "symlink resolving to /tmp refused"),
    ("hk_empty", {"HYAKU_SCRATCH": "", "TMPDIR": None}, LANE, 2,
     "empty HYAKU_SCRATCH with no TMPDIR"),
    ("tmpdir_tmp", {"HYAKU_SCRATCH": None, "TMPDIR": "/tmp/r46revtmp"}, LANE, 2,
     "TMPDIR under /tmp refused"),
    ("hk_vartmp", {"HYAKU_SCRATCH": "/var/tmp"}, LANE, 2, "/var/tmp refused"),
    ("hk_tmp_fast_tmpdir", {"HYAKU_SCRATCH": "/tmp", "TMPDIR": S + "/tmproot"}, LANE,
     2, "a bad HYAKU_SCRATCH must not silently fall through to a good TMPDIR"),
    ("tmpdir_fast", {"HYAKU_SCRATCH": None, "TMPDIR": S + "/tmproot2"}, LANE, 0,
     "documented fallback: TMPDIR on a real partition accepted"),
    ("hk_fast", {"HYAKU_SCRATCH": S + "/root"}, LANE, 0, "real fast path accepted"),
    ("hk_deep_new", {"HYAKU_SCRATCH": S + "/a/b/c"}, LANE, 0,
     "non-existent chain is created by makedirs"),
    ("hk_relative_fastcwd", {"HYAKU_SCRATCH": "relroot"}, S + "/relcwd", 0,
     "relative root is resolved against the process CWD"),
    ("hk_relative_repo", {"HYAKU_SCRATCH": "relroot"}, S + "/fixture-repo", 0,
     "relative root inside a git repo writes into that repo"),
    ("hk_shm", {"HYAKU_SCRATCH": "/dev/shm/r46scratch"}, LANE, 2,
     "/dev/shm is RAM, wiped at reboot: not citable evidence"),
    ("hk_runtime", {"HYAKU_SCRATCH": "/run/user/1000/r46scratch"}, LANE, 2,
     "XDG runtime tmpfs, wiped at logout"),
    ("hk_readonly", {"HYAKU_SCRATCH": S + "/ro"}, LANE, 2, "read-only root unusable"),
    ("hk_unreadable", {"HYAKU_SCRATCH": S + "/noread"}, LANE, 2,
     "mode-000 root unusable"),
    ("hk_file", {"HYAKU_SCRATCH": S + "/afile"}, LANE, 2, "root is a regular file"),
    ("hk_file_nested", {"HYAKU_SCRATCH": S + "/afile/sub"}, LANE, 2,
     "parent of the root is a regular file"),
]


def setup():
    for d in ("root", "tmproot", "tmproot2", "relcwd"):
        os.makedirs(os.path.join(S, d), exist_ok=True)
    for d in ("ro", "noread"):
        p = os.path.join(S, d)
        os.makedirs(p, exist_ok=True)
    os.chmod(os.path.join(S, "ro"), 0o555)
    os.chmod(os.path.join(S, "noread"), 0o000)
    link = os.path.join(S, "linktmp")
    if not os.path.islink(link):
        os.symlink("/tmp/r46-symlink-target", link)
    open(os.path.join(S, "afile"), "w").write("x\n")
    os.makedirs("/tmp/r46relcwd", exist_ok=True)
    # a real one-commit fixture repo whose CWD is the measured-repo stand-in
    repo = os.path.join(S, "fixture-repo")
    if not os.path.isdir(os.path.join(repo, ".git")):
        subprocess.run(["git", "init", "-q", repo], check=True)
        for k, v in (("user.email", "rev@round46"), ("user.name", "r46 rev")):
            subprocess.run(["git", "-C", repo, "config", k, v], check=True)
        open(os.path.join(repo, "README"), "w").write("fixture\n")
        subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-q", "-m", "fixture"],
                       check=True)
    top = subprocess.run(["git", "-C", repo, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert top == repo, (top, repo)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    setup()
    top = subprocess.run(["git", "-C", os.path.join(S, "fixture-repo"), "rev-parse",
                          "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    results = {"seat": "R46W1RevScratch", "utc_start": utc(), "python": sys.version.split()[0],
               "driver_sha256": sha(open(os.path.join(LANE, "tools/round-46/attest.py")).read()),
               "gate_sha256": sha(open(os.path.join(LANE, "tools/round-46/gate.py")).read()),
               "registry_sha256": sha(open(os.path.join(LANE, "tools/round-46/registry.py")).read()),
               "pairs": {"c1": C1, "c2": C2},
               "fixture_toplevel_assert": top == os.path.join(S, "fixture-repo"),
               "tmp_roots": list(TMP_ROOTS), "cases": []}
    base_env = dict(os.environ)
    for name, over, cwd, expect, why in CASES:
        if only and name not in only.split(","):
            continue
        env = dict(base_env)
        for k, v in over.items():
            if v is None:
                env.pop(k, None)
            else:
                env[k] = v
        rec = {"case": name, "env": {k: over.get(k, "<unset>") for k in
                                     ("HYAKU_SCRATCH", "TMPDIR")},
               "cwd": cwd, "expected_exit": expect, "why": why,
               "utc": utc(), "runs": [], "created": {},
               "base_before": {}, "base_after": {}}
        for key in ("root", "tmproot", "tmproot2", "relcwd"):
            rec["base_before"][key] = listdir_safe(os.path.join(S, key))
        t_start = time.time()
        for (freeze, rev) in (C1, C2):
            counter = "attest.py" if (freeze, rev) == C1 else "registry.py"
            r, _ = run(counter, freeze, rev, env, cwd)
            r["summary"] = summarize(r.pop("_stdout"))
            rec["runs"].append(r)
        for root in TMP_ROOTS:
            rec["created"][root] = new_under(root, t_start)
        for key in ("root", "tmproot", "tmproot2", "relcwd"):
            rec["base_after"][key] = listdir_safe(os.path.join(S, key))
        rec["relroot_created"] = {}
        for d in (S + "/relcwd", S + "/fixture-repo"):
            rel = os.path.join(d, "relroot")
            rec["relroot_created"][d] = os.path.isdir(rel)
        rec["fixture_repo_status"] = subprocess.run(
            ["git", "-C", os.path.join(S, "fixture-repo"), "status", "--porcelain"],
            capture_output=True, text=True).stdout.splitlines()
        rec["observed_exit"] = [r["exit"] for r in rec["runs"]]
        rec["matches_policy"] = rec["observed_exit"] == [expect, expect]
        results["cases"].append(rec)
    results["utc_end"] = utc()
    out = os.path.join(S, "results-%s.json" % (only.replace(",", "_") or "all"))
    with open(out, "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    print(out)
    for c in results["cases"]:
        print("%-22s exp=%s got=%s match=%s created_tmp=%d created_shm=%d" % (
            c["case"], c["expected_exit"], c["observed_exit"],
            c["matches_policy"],
            len([p for p in c["created"]["/tmp"] if any(m in p for m in OUR_MARKERS)]),
            len(c["created"]["/dev/shm"])))


if __name__ == "__main__":
    sys.exit(main())
