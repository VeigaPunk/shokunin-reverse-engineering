#!/usr/bin/env python3
"""R45W2CritC1Text: text-vs-instrument attacks on R45-C1, in scratch fixtures only."""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile

S = "/fast/scratch/hyaku/kaidoku-r45/R45W2CritC1Text"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
COUNTER = os.path.join(LANE, "tools/round-45/c1-counter.py")
PREFLIGHT = os.path.join(LANE, "tools/round-45/frozen-path-preflight.py")
WORK = os.path.join(S, "work")
os.makedirs(WORK, exist_ok=True)
ENV = dict(os.environ, TMPDIR=WORK, HYAKU_SCRATCH=WORK)
ENV.pop("GIT_DIR", None)

def git(d, *args):
    return subprocess.run(["git", "-C", d, *args], capture_output=True, text=True)

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

def base_tree():
    t = os.path.join(S, "tree")
    if os.path.isdir(t):
        shutil.rmtree(t)
    os.makedirs(t)
    arch = subprocess.run(["git", "-C", LANE, "archive", "HEAD"], capture_output=True)
    subprocess.run(["tar", "-x", "-C", t], input=arch.stdout, check=True)
    return t

def mkfix(name, tree, edit=None, pre_edit=None):
    d = os.path.join(S, "fix-" + name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    shutil.copytree(tree, d, symlinks=True)
    if pre_edit:
        pre_edit(d)
    git(d, "init", "-q")
    git(d, "config", "user.email", "w2@crit")
    git(d, "config", "user.name", "w2 crit")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "freeze")
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    f0 = git(d, "rev-parse", "HEAD").stdout.strip()
    f1 = f0
    if edit:
        edit(d)
        git(d, "add", "-A")
        git(d, "commit", "-q", "-m", "mutation")
        f1 = git(d, "rev-parse", "HEAD").stdout.strip()
    return d, f0, f1

def run_counter(d, freeze, rev, tag):
    out = os.path.join(S, "c1-%s.json" % tag)
    p = subprocess.run([sys.executable, "-I", "-B", COUNTER, "--root", d,
                        "--freeze", freeze, "--rev", rev, "--json-out", out],
                       capture_output=True, text=True, env=ENV, cwd=S)
    try:
        rec = json.load(open(out))
    except Exception:
        rec = {"unparsed_stdout": p.stdout, "stderr": p.stderr}
    return p.returncode, rec, sha(p.stdout)

def block_bounds(text):
    i = text.index("- **22.")
    j = text.index("\n## Config custody", i)
    return i, j

def edit_skill(d, fn):
    p = os.path.join(d, "SKILL.md")
    t = open(p).read()
    i, j = block_bounds(t)
    t = t[:i] + fn(t[i:j]) + t[j:]
    open(p, "w").write(t)

def t1_header_collapse(block):
    k = block.index("<!-- freeze-integrity-table v1 -->")
    head_end = block.index("\n\n", block.index("| --- |", k))
    new = ("<!-- freeze-integrity-table v1 -->\n"
           "  | trigger arm exit receipt |\n  | --- |\n"
           + "  | 1 |\n" * 10)
    return block[:k] + new + block[head_end:]

def t2_unlocated(block):
    return re.sub(r"(\.md):[0-9]+(-[0-9]+)?", r"\1", block)

def t3_extra_refs(block):
    return block + "\n  Unchecked refs: `corpus/SOURCES.md:99999`, `SKILL.md:99999`, `tools/round-44/c1-counter.py:9999`.\n"

def t5_bad_exit(block):
    return block.replace("| 1 |", "| 3 |", 1)

def t4_sources(d):
    p = os.path.join(d, "corpus/SOURCES.md")
    lines = open(p).read().splitlines(True)
    keep = [l for l in lines if "S140" not in l and "S141" not in l]
    open(p, "w").writelines(keep)

STUB_OK = ("#!/usr/bin/env python3\n"
           "import sys\n"
           "print('PREFLIGHT_SELFTEST: cases=11 failures=0')\n"
           "sys.exit(0)\n")

def t6_stub(d):
    open(os.path.join(d, "tools/round-45/frozen-path-preflight.py"), "w").write(STUB_OK)

def t7_touch_claims(d):
    with open(os.path.join(d, "plans/round-45-claims.md"), "a") as fh:
        fh.write("post-freeze edit\n")

def report(tag, code, rec, out_sha, note):
    keys = sorted(rec.keys()) if isinstance(rec, dict) else []
    sel = {k: rec.get(k) for k in ("rule_blocks", "block22_present", "block22_rows", "block22_refs",
                                   "block22_unresolved_citations", "block22_cites", "block22_header_ok",
                                   "preflight_selftest", "interpreter_present", "met_target", "failing",
                                   "verdict", "reason", "frozen_path_changed") if k in rec}
    print(json.dumps({"test": tag, "exit": code, "stdout_sha256": out_sha, "receipt_keys": keys,
                      "values": sel, "note": note}, sort_keys=True))

def main():
    tree = base_tree()
    print(json.dumps({"lane_head_tree_sha256":
                      sha(subprocess.run(["git", "-C", LANE, "rev-parse", "HEAD"],
                                         capture_output=True, text=True).stdout)}))
    tests = {}

    d, f0, f1 = mkfix("header", tree, lambda x: edit_skill(x, t1_header_collapse))
    tests["T1-header-single-cell"] = (run_counter(d, f0, f1, "T1"),
        "header collapsed to one cell carrying all four words; rows are | 1 |")

    d, f0, f1 = mkfix("unlocated", tree, lambda x: edit_skill(x, t2_unlocated))
    tests["T2-unlocated-refs"] = (run_counter(d, f0, f1, "T2"),
        "every :line dropped from the eight .md citations in block 22")

    d, f0, f1 = mkfix("extra", tree, lambda x: edit_skill(x, t3_extra_refs))
    tests["T3-out-of-domain-refs"] = (run_counter(d, f0, f1, "T3"),
        "block 22 gains corpus/SOURCES.md:99999, SKILL.md:99999, tools/round-44/c1-counter.py:9999")

    d, f0, f1 = mkfix("sources", tree, lambda x: edit_skill(x, t3_extra_refs), pre_edit=t4_sources)
    tests["T4-s140-row-absent"] = (run_counter(d, f0, f1, "T4"),
        "S140 and S141 rows deleted from corpus/SOURCES.md; block text unchanged")

    d, f0, f1 = mkfix("badexit", tree, lambda x: edit_skill(x, t5_bad_exit))
    tests["T5-bad-exit-cell"] = (run_counter(d, f0, f1, "T5"),
        "one table exit cell changed 1 -> 3")

    d, f0, f1 = mkfix("touch", tree, t7_touch_claims)
    tests["T6-post-freeze-touch"] = (run_counter(d, f0, f1, "T6"),
        "commit in FREEZE..REV appends to plans/round-45-claims.md")

    d, f0, f1 = mkfix("stub", tree, pre_edit=t6_stub)
    tests["T7-stub-interpreter"] = (run_counter(d, f0, f0, "T7"),
        "tools/round-45/frozen-path-preflight.py replaced by a 3-line stub printing cases=11 failures=0")

    for tag, ((code, rec, out_sha), note) in tests.items():
        report(tag, code, rec, out_sha, note)

    json.dump({t: {"exit": v[0][0], "sha256": v[0][2], "values": v[0][1]} for t, v in tests.items()},
              open(os.path.join(S, "attack-receipts.json"), "w"), indent=1, sort_keys=True)

if __name__ == "__main__":
    main()
