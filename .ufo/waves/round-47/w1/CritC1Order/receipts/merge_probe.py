#!/usr/bin/env python3
"""Which argv variants actually change what gate.history_touched sees?

Fixture A: ordinary merge with a conflict resolution that differs from both parents.
Fixture B: a frozen path added in one merge commit and deleted in a second one, net
           tree clean, no ordinary commit touching the path (the R45-CL6 shape).
"""
import json
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-46")
import gate  # noqa: E402

STATUS = re.compile(r"^[ACDMRTUXB][0-9]*$")
SCRATCH = os.environ["HYAKU_SCRATCH"]

VARIANTS = {
    "v1_canonical": ["log", "-m", "--diff-merges=first-parent", "--name-status", "-z", "--format="],
    "v2_reversed": ["log", "--diff-merges=first-parent", "-m", "--name-status", "-z", "--format="],
    "v3_m_only": ["log", "-m", "--name-status", "-z", "--format="],
    "v4_fp_only": ["log", "--diff-merges=first-parent", "--name-status", "-z", "--format="],
    "v5_none": ["log", "--name-status", "-z", "--format="],
    "v6_pair_split": ["log", "-m", "--name-status", "--diff-merges=first-parent", "-z", "--format="],
    "v7_no_format": ["log", "-m", "--diff-merges=first-parent", "--name-status", "-z"],
    "v8_no_name_status": ["log", "-m", "--diff-merges=first-parent", "-z", "--format="],
    "v9_format_first": ["log", "--format=", "-m", "--diff-merges=first-parent", "--name-status", "-z"],
}


def g(root, *args, binary=False):
    return subprocess.run(["git", "-C", root, *args], capture_output=True,
                          text=not binary, check=True)


def parse(raw):
    tokens = raw.decode("utf-8", "surrogateescape").split("\0")
    touched, i = [], 0
    while i < len(tokens):
        if STATUS.match(tokens[i].strip()) and i + 1 < len(tokens):
            if tokens[i + 1]:
                touched.append(tokens[i + 1])
            i += 2
            continue
        i += 1
    return touched


def run_variants(root, base, tip, paths):
    out = {}
    for name, argv in VARIANTS.items():
        r = subprocess.run(["git", "-C", root, *argv, f"{base}..{tip}", "--", *paths],
                           capture_output=True)
        raw = r.stdout
        out[name] = {"exit": r.returncode,
                     "raw_sha": __import__("hashlib").sha256(raw).hexdigest()[:16],
                     "raw_bytes": len(raw),
                     "parsed_touched": parse(raw)}
    real, err = gate.history_touched(root, base, tip, paths)
    out["gate_history_touched"] = {"touched": real, "error": err}
    return out


def fixture_a(root):
    def write(p, text):
        full = os.path.join(root, p)
        os.makedirs(os.path.dirname(full) or root, exist_ok=True)
        open(full, "w").write(text)

    def commit(msg):
        g(root, "add", "-A")
        g(root, "commit", "-qm", msg)
        return g(root, "rev-parse", "HEAD").stdout.strip()

    g(root, "init", "-q")
    g(root, "config", "user.email", "fx@round47")
    g(root, "config", "user.name", "round47 fixture")
    assert g(root, "rev-parse", "--show-toplevel").stdout.strip() == root
    DEFAULT = g(root, "symbolic-ref", "--short", "HEAD").stdout.strip()
    write("frozen/x.txt", "base\n")
    write("other.txt", "keep\n")
    base = commit("base")
    g(root, "checkout", "-q", "-b", "feat")
    write("frozen/x.txt", "feat-side\n")
    feat = commit("featwork")
    g(root, "checkout", "-q", DEFAULT)
    write("frozen/x.txt", "main-side\n")
    commit("mainwork")
    r = subprocess.run(["git", "-C", root, "merge", "--no-ff", "-q", "feat",
                        "-m", "merge feat"], capture_output=True)
    assert r.returncode != 0, "expected a conflict"
    write("frozen/x.txt", "RESOLUTION-ONLY\n")
    g(root, "add", "-A")
    g(root, "commit", "-qm", "merge feat resolved")
    tip = g(root, "rev-parse", "HEAD").stdout.strip()
    return base, tip, feat


def fixture_b(root):
    def write(p, text):
        full = os.path.join(root, p)
        os.makedirs(os.path.dirname(full) or root, exist_ok=True)
        open(full, "w").write(text)

    def commit(msg):
        g(root, "add", "-A")
        g(root, "commit", "-qm", msg)
        return g(root, "rev-parse", "HEAD").stdout.strip()

    g(root, "init", "-q")
    g(root, "config", "user.email", "fx@round47")
    g(root, "config", "user.name", "round47 fixture")
    assert g(root, "rev-parse", "--show-toplevel").stdout.strip() == root
    DEFAULT = g(root, "symbolic-ref", "--short", "HEAD").stdout.strip()
    write("a.txt", "0\n")
    base = commit("base")
    # merge 1: the frozen decoy is added *inside* the merge commit
    g(root, "checkout", "-q", "-b", "side1")
    write("b.txt", "1\n")
    commit("side1")
    g(root, "checkout", "-q", DEFAULT)
    write("c.txt", "1\n")
    commit("main1")
    r = subprocess.run(["git", "-C", root, "merge", "--no-ff", "--no-commit", "side1"],
                       capture_output=True)
    assert r.returncode == 0, r.stderr
    write("frozen/novel.txt", "decoy\n")
    g(root, "add", "-A")
    g(root, "commit", "-qm", "merge side1 (adds frozen decoy)")
    m1 = g(root, "rev-parse", "HEAD").stdout.strip()
    # merge 2: the same path is deleted *inside* a second merge commit
    g(root, "checkout", "-q", "-b", "side2")
    write("d.txt", "1\n")
    commit("side2")
    g(root, "checkout", "-q", DEFAULT)
    write("e.txt", "1\n")
    commit("main2")
    r = subprocess.run(["git", "-C", root, "merge", "--no-ff", "--no-commit", "side2"],
                       capture_output=True)
    assert r.returncode == 0, r.stderr
    g(root, "rm", "-q", "frozen/novel.txt")
    g(root, "commit", "-qm", "merge side2 (deletes frozen decoy)")
    tip = g(root, "rev-parse", "HEAD").stdout.strip()
    return base, tip, m1


def main():
    out = {}
    for name, builder in (("A_conflict_resolution", fixture_a), ("B_merge_only_add_delete", fixture_b)):
        d = tempfile.mkdtemp(dir=SCRATCH, prefix="probe-%s-" % name[0])
        try:
            base, tip, mid = builder(d)
            ordinary = g(d, "log", "--format=%H", "--name-status", f"{base}..{tip}").stdout
            net = g(d, "diff", "--name-status", f"{base}", f"{tip}", "--", "frozen/").stdout
            res = run_variants(d, base, tip, ["frozen/"])
            out[name] = {"root": d, "base": base, "tip": tip, "mid": mid,
                         "net_frozen_diff": net.strip().splitlines(),
                         "ordinary_log_mentions_frozen": "frozen/" in ordinary,
                         "variants": res}
        finally:
            pass  # keep fixtures on disk for the gate-level probes
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
