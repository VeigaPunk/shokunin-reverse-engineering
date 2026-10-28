import json, subprocess, hashlib, os, sys, datetime
S = "/fast/scratch/hyaku/kaidoku-r47/MutExitCodes"
env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
def run(name, cmd, expect=2):
    t = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=S, timeout=900)
    h = hashlib.sha256(r.stdout.encode()).hexdigest()
    rec = {"probe": name, "utc": t, "exit": r.returncode, "expect": expect,
           "ok": r.returncode == expect, "stdout_sha256": h,
           "stdout_head": r.stdout[:400].replace("\n", " "),
           "stderr_head": r.stderr[:300].replace("\n", " "),
           "cmd": " ".join(cmd)}
    print(json.dumps(rec))
    return rec
