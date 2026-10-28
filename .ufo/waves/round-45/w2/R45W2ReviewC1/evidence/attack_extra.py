#!/usr/bin/env python3
"""Extra fixtures: split inflation, block-number identity, evil-merge escape."""
import hashlib, json, os, subprocess, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import attack as A

def case_a1d_fence_inflates_count():
    fence = "  ```text\n- **not a rule, a sample bullet**\n  ```\n"
    # 20 real plain blocks + one plain block carrying a fenced sample bullet + the marked block
    skill = A.CRAFT_HEAD + A.plain(19) + f"- **20. Plain rule 20.** body\n{fence}" + A.good_block()
    # human count of real rule blocks in the section: 21 (19 plain + 20 + 22)
    A.run("A1d-fence-inflates-block-count", "A1: block split / rule_blocks count", 0, skill)

def case_a1e_numbering():
    skill = A.CRAFT_HEAD + A.plain(20) + A.good_block(label="3") + "- **22. Unrelated rule.** body\n"
    A.run("A1e-marker-not-on-block-22", "A1: block-number identity", 0, skill)

def case_b1_evil_merge():
    d = tempfile.mkdtemp(dir=A.S, prefix="fx-merge-")
    files = {"SKILL.md": A.CRAFT_HEAD + A.plain(21) + A.good_block(),
             A.PREFLIGHT: A.STUB_OK}
    files.update(A.corpus())
    f = A.make_repo(d, files)
    A.git(d, "checkout", "-q", "-b", "side")
    with open(os.path.join(d, "SIDE.md"), "w") as fh:
        fh.write("side\n")
    A.git(d, "add", "-A"); A.git(d, "commit", "-q", "-m", "side work")
    A.git(d, "checkout", "-q", "master") if A.git(d, "rev-parse", "--verify", "master").returncode == 0 else A.git(d, "checkout", "-q", "main")
    A.git(d, "merge", "--no-commit", "--no-ff", "side")
    # evil merge: swap the frozen interpreter for a zero-test stub
    stub = ("#!/usr/bin/env python3\nimport sys\n"
            "print('PREFLIGHT_SELFTEST: cases=11 failures=0')\nsys.exit(0)\n")
    if stub == A.STUB_OK:
        stub = ("#!/usr/bin/env python3\nimport sys\n"
                "print('PREFLIGHT_SELFTEST: cases=11 failures=0')\n# arms deleted\nsys.exit(0)\n")
    with open(os.path.join(d, A.PREFLIGHT), "w") as fh:
        fh.write(stub)
    A.git(d, "add", "-A"); A.git(d, "commit", "-q", "-m", "merge side")
    rev = A.git(d, "rev-parse", "HEAD").stdout.strip()
    log = A.git(d, "log", "--name-only", "--format=", f"{f}..{rev}", "--",
                "plans/round-45-claims.md", "tools/round-45")
    logm = A.git(d, "log", "-m", "--name-only", "--format=", f"{f}..{rev}", "--",
                 "plans/round-45-claims.md", "tools/round-45")
    out = os.path.join(A.OUT, "B1-evil-merge.json")
    argv = [sys.executable, "-I", "-B", A.COUNTER, "--root", d, "--freeze", f,
            "--rev", rev, "--json-out", out]
    proc = subprocess.run(argv, capture_output=True, text=True,
                          env=dict(os.environ, TMPDIR=A.S, HYAKU_SCRATCH=A.S), cwd=d)
    try: recv = json.loads(proc.stdout)
    except Exception: recv = {}
    rec = {"case": "B1-evil-merge-escape", "attacks": "B1 bonus: frozen arm vs merge diffs",
           "expect": 2, "exit": proc.returncode, "ok": proc.returncode == 2,
           "met_target": recv.get("met_target"),
           "stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "argv": " ".join(argv),
           "git_log_name_only": [l for l in log.stdout.splitlines() if l.strip()],
           "git_log_m_name_only": [l for l in logm.stdout.splitlines() if l.strip()],
           "receipt_subset": {"preflight_selftest": recv.get("preflight_selftest")},
           "failing": recv.get("failing")}
    A.RESULTS.append(rec)
    print(json.dumps({"case": rec["case"], "exit": rec["exit"], "expect": 2}))

if __name__ == "__main__":
    case_a1d_fence_inflates_count()
    case_a1e_numbering()
    case_b1_evil_merge()
    with open(os.path.join(A.OUT, "results_extra.json"), "w") as fh:
        json.dump(A.RESULTS, fh, indent=1)
