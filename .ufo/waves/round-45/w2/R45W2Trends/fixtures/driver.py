#!/usr/bin/env python3
"""R45W2Trends: attack the Round-45 trend verdicts with fixtures + lane counters (read-only)."""
import hashlib, json, os, shutil, subprocess, sys, datetime

S = "/fast/scratch/hyaku/kaidoku-r45/R45W2Trends"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
os.environ["TMPDIR"] = S
os.environ["HYAKU_SCRATCH"] = S
REC = os.path.join(S, "receipts")
os.makedirs(REC, exist_ok=True)

def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p

def record(tag, cmd, p, extra=None):
    out = p.stdout or ""
    rec = {
        "tag": tag, "utc": utc(), "cmd": cmd, "exit": p.returncode,
        "stdout_sha256": hashlib.sha256(out.encode()).hexdigest(),
        "stdout_head": out[:4000], "stderr_head": (p.stderr or "")[:1500],
    }
    if extra:
        rec.update(extra)
    with open(os.path.join(REC, tag + ".json"), "w") as fh:
        json.dump(rec, fh, indent=1)
    return rec

def git(d, *args, cwd=None):
    return run(["git", "-C", d, *args])

def init_fixture(d):
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    p = run(["git", "init", "-q", d]); assert p.returncode == 0, p.stderr
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    return d

def writef(d, rel, body):
    path = os.path.join(d, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(body)

def commit(d, msg):
    git(d, "add", "-A")
    p = run(["git", "-C", d, "-c", "user.email=w2@trends.invalid", "-c", "user.name=R45W2Trends",
             "commit", "-q", "--allow-empty", "-m", msg])
    assert p.returncode == 0, p.stderr
    return git(d, "rev-parse", "HEAD").stdout.strip()

MARKER = "<!-- freeze-integrity-table v1 -->"
PREFLIGHT = "tools/round-45/frozen-path-preflight.py"

# ---- C1 forgery: the counter's own good_block() shape, filler content ----------
HEADER = "| trigger | arm | exit | receipt |\n|---|---|---|---|\n"
ROW = "| post-freeze commit touches a frozen path | commit arm | 1 | `--json-out` receipt |\n"

def c1_fixture(d):
    init_fixture(d)
    lines = ["# SKILL", "", "## Queue-drain craft (trends fixture)", ""]
    for i in range(1, 22):
        lines.append("- **%d. filler rule** nothing here\n" % i)
    block = "- **22. Freeze integrity.** " + MARKER + " S140 " + PREFLIGHT + "\n\n"
    block += HEADER + ROW * 8
    block += "\n  Refs: corpus/lessons/round-44.md:38, plans/round-45-claims.md:1, " \
             "corpus/lessons/round-44-verifier-spotcheck.md:12, " \
             "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:9\n\n"
    lines.append(block)
    writef(d, "SKILL.md", "\n".join(lines))
    writef(d, "corpus/lessons/round-44.md", "\n".join("L%d" % i for i in range(1, 60)) + "\n")
    writef(d, "corpus/lessons/round-44-verifier-spotcheck.md", "\n".join("L%d" % i for i in range(1, 60)) + "\n")
    writef(d, "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md", "\n".join("L%d" % i for i in range(1, 60)) + "\n")
    writef(d, "plans/round-45-claims.md", "claims\n")
    writef(d, PREFLIGHT, "import sys\nprint('PREFLIGHT_SELFTEST: cases=11 failures=0')\nsys.exit(0)\n")
    c1 = commit(d, "fixture: forged block 22 + stub interpreter")
    c2 = commit(d, "fixture: empty second commit")
    return c1, c2

# ---- C2 forgery: six fenced rows anywhere, junk exit cell ---------------------
SCOPE = [
    "tools/round-44/c1-counter.py", "tools/round-44/c1-run.sh", "tools/round-44/c2-counter.py",
    "tools/round-45/frozen-path-preflight.py", "tools/round-45/c1-counter.py",
    "tools/round-45/c2-counter.py",
]

def c2_fixture(d):
    init_fixture(d)
    lines = ["# SKILL", "", "## Something else", "", "```"]
    for p in SCOPE:
        lines.append("| `%s` | junk | 0 rows, 1 column, 2 bytes | junk |" % p)
    lines += ["```", "", "no registry heading anywhere", ""]
    writef(d, "SKILL.md", "\n".join(lines))
    writef(d, "plans/round-45-claims.md", "claims\n")
    writef(d, "tools/round-45/registry-scope.json", json.dumps({"paths": SCOPE}, indent=1) + "\n")
    c1 = commit(d, "fixture: fenced junk registry rows (no real row)")
    c2 = commit(d, "fixture: empty second commit")
    return c1, c2

# ---- Preflight dirty false-clean fixture --------------------------------------
def dirty_fixture(d):
    init_fixture(d)
    writef(d, "frozen/a.txt", "a\n")
    writef(d, "other.txt", "o\n")
    c1 = commit(d, "fixture: base")
    writef(d, "frozen/b.txt", "b\n")
    commit(d, "fixture: touch frozen/b.txt")
    with open(os.path.join(d, "frozen/a.txt"), "a") as fh:
        fh.write("dirty\n")          # worktree-only dirty, uncommitted
    return c1

def preflight_copy(dst, body):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w") as fh:
        fh.write(body)

def main():
    results = {}
    py = sys.executable
    c1c = os.path.join(LANE, "tools/round-45/c1-counter.py")
    c2c = os.path.join(LANE, "tools/round-45/c2-counter.py")

    # E2: do-nothing control at the freeze (lane, read-only)
    p = run([py, "-I", "-B", c1c, "--root", LANE, "--freeze", "f762b727", "--rev", "f762b727",
             "--json-out", os.path.join(REC, "c1-freeze.json")])
    results["c1-freeze"] = record("c1-freeze", "c1-counter --root LANE --freeze f762b727 --rev f762b727", p)
    p = run([py, "-I", "-B", c2c, "--root", LANE, "--freeze", "f762b727", "--rev", "f762b727",
             "--json-out", os.path.join(REC, "c2-freeze.json")])
    results["c2-freeze"] = record("c2-freeze", "c2-counter --root LANE --freeze f762b727 --rev f762b727", p)

    # E3: forged block 22 -> does the depth proxy accept it?
    d1 = os.path.join(S, "fx-c1-forged")
    f1, r1 = c1_fixture(d1)
    p = run([py, "-I", "-B", c1c, "--root", d1, "--freeze", f1, "--rev", r1,
             "--json-out", os.path.join(REC, "c1-forged.json")])
    results["c1-forged"] = record("c1-forged", "c1-counter --root fx-c1-forged --freeze %s --rev %s" % (f1, r1), p)

    # E4: six fenced junk registry rows -> does the calibration proxy accept them?
    d2 = os.path.join(S, "fx-c2-forged")
    f2, r2 = c2_fixture(d2)
    p = run([py, "-I", "-B", c2c, "--root", d2, "--freeze", f2, "--rev", r2,
             "--json-out", os.path.join(REC, "c2-forged.json")])
    results["c2-forged"] = record("c2-forged", "c2-counter --root fx-c2-forged --freeze %s --rev %s" % (f2, r2), p)

    # E5: preflight selftest from A3 (lane bytes, read-only)
    pf = os.path.join(S, "preflight-A3.py")
    body = subprocess.check_output(["git", "-C", LANE, "show", "f59565b7:tools/round-45/frozen-path-preflight.py"], text=True)
    preflight_copy(pf, body)
    p = run([py, "-I", "-B", pf, "--selftest"], cwd=S)
    results["preflight-selftest-A3"] = record("preflight-selftest-A3", "preflight-A3.py --selftest", p)
    results["preflight-selftest-A3"]["tail"] = (p.stdout or "").strip().splitlines()[-1:]

    # E6: dirty arm red + --dirty-pathspec false-clean
    dd = os.path.join(S, "fx-dirty")
    base = dirty_fixture(dd)
    p = run(["git", "-C", dd, "status", "--porcelain", "-z"])
    record("dirty-fixture-state", "git -C fx-dirty status --porcelain -z", p)
    p = run([py, "-I", "-B", pf, "--root", dd, "--freeze", base, "--rev", base,
             "--pathspec", "frozen/", "--freeze-path", "frozen", "--check-dirty",
             "--json-out", os.path.join(REC, "preflight-dirty.json")])
    results["preflight-dirty"] = record("preflight-dirty", "preflight --check-dirty --pathspec frozen/", p)
    p = run([py, "-I", "-B", pf, "--root", dd, "--freeze", base, "--rev", base,
             "--pathspec", "frozen/", "--freeze-path", "frozen", "--check-dirty",
             "--dirty-pathspec", "other.txt", "--json-out", os.path.join(REC, "preflight-dirty-wrongscope.json")])
    results["preflight-dirty-wrongscope"] = record(
        "preflight-dirty-wrongscope", "preflight --check-dirty --pathspec frozen/ --dirty-pathspec other.txt", p)

    # E7: restored arm isolation — delete the restored classifier, rerun selftest
    mutated = body.replace('            restored.append(path)\n', '            pass  # restored arm removed\n')
    assert mutated != body, "restored.append not found"
    pf2 = os.path.join(S, "preflight-no-restored.py")
    preflight_copy(pf2, mutated)
    p = run([py, "-I", "-B", pf2, "--selftest"], cwd=S)
    results["preflight-no-restored"] = record("preflight-no-restored", "preflight-no-restored.py --selftest", p)
    results["preflight-no-restored"]["tail"] = (p.stdout or "").strip().splitlines()[-1:]

    with open(os.path.join(S, "summary.json"), "w") as fh:
        json.dump(results, fh, indent=1)
    for k, v in results.items():
        print(k, "exit=", v["exit"], "sha=", v["stdout_sha256"][:12], v.get("tail", ""))
    print("fixtures:", f1, r1, f2, r2, base)

main()
