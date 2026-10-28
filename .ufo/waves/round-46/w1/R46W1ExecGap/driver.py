#!/usr/bin/env python3
"""R46W1ExecGap: measure the round-45 discrimination gap LIVE on committed bytes.

Builds a one-commit fixture repo holding the round-45 cheapest-green C1 forgery
(SKILL.md text from the committed reconstruction), then scores it with:
  A) the FROZEN round-45 counter (tools/round-45/c1-counter.py @ 3182047)
  B) tools/round-46/attest.py --spec r45 --profile v1, both at the freeze
     commit bytes (3182047) and at HEAD bytes
plus two freeze-identity probes on the real lane.  Every receipt carries the
exact command, exit code, stdout sha256 and UTC time.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import datetime

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r46/R46W1ExecGap"
FREEZE = "31820472784284727546808acc31b3ea1e73919b"
AUTHORITATIVE = "65678df0f1666e83cdeea7233bfb31ffe73ec709"
HEAD = subprocess.run(["git", "-C", LANE, "rev-parse", "HEAD"],
                      capture_output=True, text=True).stdout.strip()

os.environ["TMPDIR"] = S
os.environ["HYAKU_SCRATCH"] = S

RECEIPTS = []


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(cmd, cwd=None, timeout=600):
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout)
    rec = {
        "cmd": " ".join(cmd),
        "cwd": cwd,
        "exit": proc.returncode,
        "stdout_sha256": sha(proc.stdout.encode()),
        "stdout_head": proc.stdout[:1200],
        "stdout_tail": proc.stdout[-600:],
        "stderr_sha256": sha(proc.stderr.encode()),
        "stderr_tail": proc.stderr[-800:],
        "utc": utc(),
    }
    RECEIPTS.append(rec)
    return rec


def lane_show(ref, path):
    r = subprocess.run(["git", "-C", LANE, "show", f"{ref}:{path}"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"absent {ref}:{path}")
    return r.stdout


def build_fixture(name, preflight_bytes):
    """One-commit git repo: the a6 forgery SKILL plus the files its refs name."""
    d = tempfile.mkdtemp(dir=S, prefix=name + "-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    subprocess.run(["git", "-C", d, "config", "user.email", "gap@round46"], check=True)
    subprocess.run(["git", "-C", d, "config", "user.name", "round46 gap fixture"],
                   check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    files = {
        "SKILL.md": lane_show(HEAD, ".ufo/waves/round-45/w2/R45W2Lesson/fx-a6-SKILL.md"),
        "plans/round-45-claims.md": lane_show(HEAD, "plans/round-45-claims.md"),
        "tools/round-45/frozen-path-preflight.py": preflight_bytes,
        "corpus/lessons/round-44.md": lane_show(HEAD, "corpus/lessons/round-44.md"),
        "corpus/lessons/round-44-verifier-spotcheck.md":
            lane_show(HEAD, "corpus/lessons/round-44-verifier-spotcheck.md"),
        "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md":
            lane_show(HEAD, "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md"),
        # the frozen counter sits inside the frozen directory in the fixture
        "tools/round-45/c1-counter.py": lane_show(FREEZE, "tools/round-45/c1-counter.py"),
    }
    for p, body in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(body)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fixture: a6 forgery"],
                   check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return d, rev


def install_tool(dirname, ref):
    tgt = os.path.join(S, "bin", dirname)
    os.makedirs(tgt, exist_ok=True)
    for p in ("attest.py", "gate.py"):
        body = lane_show(ref, "tools/round-46/" + p)
        with open(os.path.join(tgt, p), "w") as fh:
            fh.write(body)
    return os.path.join(tgt, "attest.py")


def main():
    os.makedirs(os.path.join(S, "bin"), exist_ok=True)
    counter = os.path.join(S, "bin", "c1-counter.py")
    with open(counter, "w") as fh:
        fh.write(lane_show(FREEZE, "tools/round-45/c1-counter.py"))
    os.chmod(counter, 0o755)
    real_preflight = lane_show(HEAD, "tools/round-45/frozen-path-preflight.py")
    stub_preflight = lane_show(HEAD, ".ufo/waves/round-45/w2/R45W2Lesson/stub.py")
    attest_freeze = install_tool("r46-freeze", FREEZE)
    attest_head = install_tool("r46-head", HEAD)

    out = {"lane": LANE, "lane_head": HEAD, "freeze": FREEZE,
           "authoritative_freeze_claimed_by_commit": AUTHORITATIVE,
           "tool_sha256": {
               "c1-counter.py@freeze": sha(open(counter, "rb").read()),
               "attest.py@freeze": sha(open(os.path.join(S, "bin", "r46-freeze",
                                                         "attest.py"), "rb").read()),
               "attest.py@HEAD": sha(open(os.path.join(S, "bin", "r46-head",
                                                      "attest.py"), "rb").read()),
               "frozen-path-preflight.py@HEAD": sha(real_preflight.encode()),
               "stub.py@HEAD": sha(stub_preflight.encode()),
           },
           "fixtures": {}}

    for name, preflight in (("fx-a6-real", real_preflight),
                            ("fx-a6-stub", stub_preflight)):
        d, rev = build_fixture(name, preflight)
        try:
            entry = {"dir": d, "rev": rev, "skill_sha256":
                     sha(open(os.path.join(d, "SKILL.md"), "rb").read()),
                     "preflight_sha256": sha(preflight.encode())}
            entry["r45_counter"] = run(
                ["/usr/bin/python3", "-I", "-B", counter, "--root", d,
                 "--freeze", rev, "--rev", rev], cwd=d)
            json.loads(entry["r45_counter"]["stdout_head"])
            entry["v1_freeze_bytes_notrim"] = run(
                ["/usr/bin/python3", "-I", "-B", attest_freeze, "--root", d,
                 "--freeze", rev, "--rev", rev, "--spec", "r45", "--profile", "v1",
                 "--no-battery"], cwd=d)
            entry["v1_head_bytes_notrim"] = run(
                ["/usr/bin/python3", "-I", "-B", attest_head, "--root", d,
                 "--freeze", rev, "--rev", rev, "--spec", "r45", "--profile", "v1",
                 "--no-battery"], cwd=d)
            entry["v1_head_bytes_battery_on"] = run(
                ["/usr/bin/python3", "-I", "-B", attest_head, "--root", d,
                 "--freeze", rev, "--rev", rev, "--spec", "r45", "--profile", "v1"],
                cwd=d)
            entry["v2_head_bytes_notrim"] = run(
                ["/usr/bin/python3", "-I", "-B", attest_head, "--root", d,
                 "--freeze", rev, "--rev", rev, "--spec", "r45", "--profile", "v2",
                 "--no-battery"], cwd=d)
            out["fixtures"][name] = entry
        finally:
            shutil.rmtree(d, ignore_errors=True)

    # freeze identity: what the claims file's own re-derivation names vs what was scored
    out["freeze_identity"] = {
        "git_log_1_claims": run(["git", "-C", LANE, "log", "--format=%H", "-1",
                                 "--", "plans/round-46-claims.md"])["stdout_head"].strip(),
        "git_log_1_tools": run(["git", "-C", LANE, "log", "--format=%H", "-1",
                                "--", "tools/round-46/"])["stdout_head"].strip(),
    }
    out["freeze_identity"]["attest_head_byte_diff"] = run(
        ["git", "-C", LANE, "diff", "--stat", FREEZE + ".." + HEAD, "--",
         "plans/round-46-claims.md", "tools/round-46/"])["stdout_head"]

    d = tempfile.mkdtemp(dir=S, prefix="probe-")
    try:
        probe = {}
        probe["freeze_3182047_rev_HEAD"] = run(
            ["/usr/bin/python3", "-I", "-B", attest_head, "--root", LANE,
             "--freeze", FREEZE, "--rev", HEAD, "--no-battery"], cwd=S)
        probe["freeze_65678df0_rev_HEAD"] = run(
            ["/usr/bin/python3", "-I", "-B", attest_head, "--root", LANE,
             "--freeze", AUTHORITATIVE, "--rev", HEAD, "--no-battery"], cwd=S)
        out["lane_probes"] = probe
    finally:
        shutil.rmtree(d, ignore_errors=True)

    with open(os.path.join(S, "receipts.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "fixtures"}, indent=1)[:1500])
    for name, e in out["fixtures"].items():
        print(name, e["rev"])
        for k in ("r45_counter", "v1_freeze_bytes_notrim", "v1_head_bytes_notrim",
                  "v1_head_bytes_battery_on", "v2_head_bytes_notrim"):
            print("  ", k, "exit", e[k]["exit"], "sha", e[k]["stdout_sha256"][:12])


if __name__ == "__main__":
    main()
