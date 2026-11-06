"""Independent driver: run the self-test argv each registry cell documents (25 of 26 no-count rows)."""
import json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

S = "/fast/scratch/hyaku/kaidoku-r100/ExecReproC2"
CLONE = os.path.join(S, "clone-a2")
REV = "cbd224ef9b9d2271f415d823bdc4d1e70a0d281c"
SEED = "31820472784284727546808acc31b3ea1e73919b"
CASES = [
    (11, "tools/round-41/gen-squashfs.py", ["--selftest"], "python3"),
    (12, "tools/round-41/heldout-gen-v3.py", ["--seed", SEED, "--selftest", "--scratch", "{W}/scratch"], "python3"),
    (16, "tools/round-41/sqfs-list.py", ["--selftest"], "python3"),
    (21, "tools/round-42/c2-counter.py", ["--selftest"], "python3"),
    (23, "tools/round-42/heldout-gen-v4.py", ["--seed", SEED, "--selftest"], "python3"),
    (27, "tools/round-42/sqfs3-oracle.py", ["--selftest", "--work", "{W}/work"], "python3"),
    (29, "tools/round-43/c1-counter.py", ["--selftest"], "python3"),
    (31, "tools/round-43/heldout-gen-v4r43.py", ["--selftest-tuple", "--scratch", "{W}/scratch"], "python3"),
    (35, "tools/round-44/c2-counter.py", ["--selftest"], "python3"),
    (42, "tools/round-46/registry.py", ["--selftest", "--root", ".", "--freeze", "0", "--rev", "0"], "python3"),
    (47, "tools/round-48/record2.py", ["--selftest"], "python3"),
    (49, "tools/round-49/c1-controls.py", ["--selftest"], "python3"),
    (50, "tools/round-49/c1-oracle.py", ["--selftest"], "python3"),
    (60, "tools/round-50-c3/sqfs-triage-v5.py", ["--selftest"], "python3"),
    (61, "tools/round-51/census3.py", ["--selftest"], "python3"),
    (64, "tools/round-53/r53-record.py", ["--selftest"], "python -X utf8"),
    (104, "tools/round-72/capsule-audit.py", ["--selftest"], "python3"),
    (141, "tools/round-81/strictness-battery.py", ["--selftest"], "python3"),
    (142, "tools/round-82/conjunction-gate.py", ["--cli-selftest", "--root", ".", "--rev", REV, "--work", "{W}/work", "--json-out", "{W}/receipt.json"], "python3"),
    (143, "tools/round-82/printed-command.py", ["--cli-selftest", "--root", ".", "--rev", REV, "--work", "{W}/work", "--json-out", "{W}/receipt.json"], "python3"),
    (144, "tools/round-82/cli-fixtures.py", ["--selftest", "--root", ".", "--rev", REV, "--work", "{W}/work", "--json-out", "{W}/receipt.json"], "python3"),
    (145, "tools/round-83/attribution-audit.py", ["--selftest", "--root", ".", "--rev", REV, "--freeze", "de4e58b2c22bf4376dc81bd32dfe0b9ac605e17e", "--work", "{W}/work", "--json-out", "{W}/receipt.json"], "python3"),
    (146, "tools/round-83/source-bind.py", ["--selftest", "--json-out", "{W}/receipt.json"], "python3"),
    (155, "tools/round-90/control-cheat-repack.py", ["--selftest"], "python3"),
    (184, "tools/round-97/depth-blocks-v4.py", ["--selftest"], "python3"),
]
CNT = re.compile(r"(\d+)\s*(?:selftest\s+)?cases\b|cases\s*[=:]\s*(\d+)|(\d+)\s*/\s*(\d+)|(\d+)\s+checks|(\d+)\s+arms|(\d+)\s+cases", re.I)

def run_one(case):
    line, tool, args, pref = case
    W = os.path.join(S, "runs", "row%d" % line)
    os.makedirs(os.path.join(W, "work"), exist_ok=True)
    os.makedirs(os.path.join(W, "scratch"), exist_ok=True)
    argv_t = [a.replace("{W}", W) for a in args]
    prefix = pref.split()
    full = prefix + (["-I", "-B"] if prefix[0] == "python" and "-I" not in prefix else []) + [tool] + argv_t
    if prefix == ["python", "-X", "utf8"]:
        full = ["python", "-X", "utf8", "-I", "-B", tool] + argv_t
    env = {"PATH": os.environ["PATH"], "HOME": os.environ["HOME"], "LANG": "C.UTF-8",
           "HYAKU_SCRATCH": W, "TMPDIR": W}
    try:
        pr = subprocess.run(full, cwd=CLONE, capture_output=True, text=True, timeout=300, env=env)
        rc, out, err = pr.returncode, pr.stdout, pr.stderr
    except subprocess.TimeoutExpired as e:
        rc, out, err = -9, (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), "TIMEOUT 300s"
    # --help probe (argparse acceptance of the documented flags is checked against the help text too)
    hp = subprocess.run(prefix + (["-I", "-B"] if prefix[0] == "python" and "-I" not in prefix else []) + [tool, "--help"] if prefix != ["python", "-X", "utf8"] else ["python", "-X", "utf8", "-I", "-B", tool, "--help"],
                        cwd=CLONE, capture_output=True, text=True, timeout=120, env=env)
    open(os.path.join(W, "stdout.txt"), "w").write(out)
    open(os.path.join(W, "stderr.txt"), "w").write(err)
    open(os.path.join(W, "rc"), "w").write(str(rc) + "\n")
    txt = (out + "\n" + err).strip()
    last = txt.splitlines()[-1] if txt else ""
    m = list(CNT.finditer(txt))
    count = None
    if m:
        g = [x for x in m[-1].groups() if x is not None]
        count = g[0] if g else None
    return {"line": line, "tool": tool, "argv": full[len(prefix):] if prefix[0]!="python" or len(prefix)>1 else full[1:],
            "command": " ".join(full), "rc": rc, "last_line": last[:300],
            "count_token": (m[-1].group(0) if m else None), "count_value": count,
            "help_rc": hp.returncode, "help_head": (hp.stdout + hp.stderr).strip().splitlines()[:2],
            "stderr_tail": err.strip().splitlines()[-2:] if err else []}

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as ex:
        res = list(ex.map(run_one, CASES))
    json.dump(res, open(os.path.join(S, "runs", "results.json"), "w"), indent=1, ensure_ascii=False)
    for r in res:
        print(r["line"], r["tool"], "rc=%d" % r["rc"], "help_rc=%d" % r["help_rc"], "count=%s" % r["count_token"], "|", r["last_line"][:140])
