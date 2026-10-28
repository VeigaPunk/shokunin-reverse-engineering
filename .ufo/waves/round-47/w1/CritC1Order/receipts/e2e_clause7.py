#!/usr/bin/env python3
"""Clause-7 (flag order) falsification, end to end.

Forgeries that keep the literal `"-m", "--diff-merges=first-parent"` exactly once and the
reversed pair zero times, yet stop the merge arm from working:

  F1 comment-literal : the literal moves into a comment; the executed call drops the flags
  F2 no-format       : the call keeps the literal but loses `--format=`, so the parser sees
                       no (status, path) pairs and history_touched returns []
  F3 dead-call       : freeze_state stops calling history_touched at all
  F4 runtime-reorder : gate() rewrites argv, call-site text unchanged

Each is scored by the real `exact.score` (v3) and, for F1/F2/F3, by the real
`gate.freeze_state` against a merge-only add/delete tamper under a frozen path.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import exact  # noqa: E402
import gate as real_gate  # noqa: E402

SCRATCH = os.environ["HYAKU_SCRATCH"]
CLAIMS = open(os.path.join(LANE, "plans", "round-47-claims.md")).read()
EXACT_SRC = open(os.path.join(LANE, "tools", "round-47", "exact.py")).read()
GATE_SRC = open(os.path.join(LANE, "tools", "round-46", "gate.py")).read()

CALL = ('    r = git(root, "log", "-m", "--diff-merges=first-parent", "--name-status", "-z",\n'
        '            "--format=", f"{base}..{tip}", "--", *paths, binary=True)\n')


def g(root, *args, binary=False):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True,
                       text=not binary, check=True)
    return r


def commit(root, msg):
    g(root, "add", "-A")
    g(root, "commit", "-qm", msg)
    return g(root, "rev-parse", "HEAD").stdout.strip()


def write(root, p, text):
    full = os.path.join(root, p)
    os.makedirs(os.path.dirname(full) or root, exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def forged_gate(kind):
    if kind == "F1-comment-literal":
        assert CALL in GATE_SRC
        return GATE_SRC.replace(
            CALL,
            '    # canonical argv, kept for the record: "-m", "--diff-merges=first-parent"\n'
            '    r = git(root, "log", "--name-status", "-z",\n'
            '            "--format=", f"{base}..{tip}", "--", *paths, binary=True)\n')
    if kind == "F2-no-format":
        return GATE_SRC.replace('"--name-status", "-z",\n            "--format=",',
                                '"--name-status", "-z",')
    if kind == "F3-dead-call":
        old = "    touched, err = history_touched(root, base, tip, paths)"
        assert old in GATE_SRC
        return GATE_SRC.replace(old, "    touched, err = [], None")
    if kind == "F4-runtime-reorder":
        old = ('def git(root, *args, binary=False, timeout=120):\n'
               '    return subprocess.run(["git", "-C", root, *args], capture_output=True,\n'
               '                          text=not binary, timeout=timeout)\n')
        assert old in GATE_SRC
        new = ('def git(root, *args, binary=False, timeout=120):\n'
               '    args = list(args)\n'
               '    if "--diff-merges=first-parent" in args and "-m" in args:\n'
               '        args.remove("-m")\n'
               '        args.insert(args.index("--diff-merges=first-parent"), "-m")\n'
               '    return subprocess.run(["git", "-C", root, *args], capture_output=True,\n'
               '                          text=not binary, timeout=timeout)\n')
        return GATE_SRC.replace(old, new)
    if kind == "F5-decoy-function":
        old = "    touched, err = history_touched(root, base, tip, paths)"
        assert old in GATE_SRC
        decoy = ('def history_touched_quiet(root, base, tip, paths):\n'
                 '    if not paths:\n'
                 '        return [], None\n'
                 '    r = git(root, "log", "--name-status", "-z", "--format=",\n'
                 '            f"{base}..{tip}", "--", *paths, binary=True)\n'
                 '    return [], None\n\n\n')
        out = GATE_SRC.replace("def history_touched(", decoy + "def history_touched(", 1)
        return out.replace(old, "    touched, err = history_touched_quiet(root, base, tip, paths)")
    raise SystemExit("unknown kind")


def load_gate_from(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def clause7(kind, root):
    """Score the real block against the forged gate bytes through exact.score."""
    gtext = forged_gate(kind)
    pin = hashlib.sha256(EXACT_SRC.encode()).hexdigest()
    block = exact.good_block(pin=pin)
    skill = exact.skill_text(block)
    files = {"SKILL.md": skill, "plans/round-47-claims.md": CLAIMS,
             "corpus/lessons/round-46.md": "lesson line\n" * 240,
             "tools/round-47/exact.py": EXACT_SRC, "tools/round-46/gate.py": gtext}
    d, rev = exact._repo(files, root, prefix="c7-")
    try:
        code, rec = exact.score(files["SKILL.md"], lambda p: real_gate.show(d, rev, p),
                                "v3", rev, battery=None)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return {"kind": kind,
            "order_literal_count": gtext.count(exact.ORDER),
            "reversed_count": gtext.count(exact.REVERSED),
            "score_exit": code,
            "failing": rec.get("failing"),
            "gate_order_literal_receipt": rec.get("gate_order_literal"),
            "gate_order_reversed_receipt": rec.get("gate_order_reversed")}


def tamper_repo(root, gate_kind):
    """freeze..rev contains a merge-only add + merge-only delete under tools/round-47/."""
    g(root, "init", "-q")
    g(root, "config", "user.email", "fx@round47")
    g(root, "config", "user.name", "round47 fixture")
    assert g(root, "rev-parse", "--show-toplevel").stdout.strip() == root
    write(root, "SKILL.md", exact.skill_text(exact.good_block(
        pin=hashlib.sha256(EXACT_SRC.encode()).hexdigest())))
    write(root, "plans/round-47-claims.md", CLAIMS)
    write(root, "tools/round-47/exact.py", EXACT_SRC)
    write(root, "tools/round-46/gate.py", forged_gate(gate_kind) if gate_kind else GATE_SRC)
    write(root, "corpus/lessons/round-46.md", "lesson line\n" * 240)
    write(root, "tools/round-47/keep.py", "# kept\n")
    freeze = commit(root, "freeze")
    default = g(root, "symbolic-ref", "--short", "HEAD").stdout.strip()
    write(root, "note.txt", "1\n")
    commit(root, "ordinary work")
    g(root, "checkout", "-q", "-b", "side1")
    write(root, "side1.txt", "1\n")
    commit(root, "side1")
    g(root, "checkout", "-q", default)
    write(root, "main1.txt", "1\n")
    commit(root, "main1")
    r = subprocess.run(["git", "-C", root, "merge", "--no-ff", "--no-commit", "side1"],
                       capture_output=True)
    assert r.returncode == 0, r.stderr
    write(root, "tools/round-47/decoy.txt", "decoy\n")
    g(root, "add", "-A")
    g(root, "commit", "-qm", "merge side1 (adds frozen decoy)")
    g(root, "checkout", "-q", "-b", "side2")
    write(root, "side2.txt", "1\n")
    commit(root, "side2")
    g(root, "checkout", "-q", default)
    write(root, "main2.txt", "1\n")
    commit(root, "main2")
    r = subprocess.run(["git", "-C", root, "merge", "--no-ff", "--no-commit", "side2"],
                       capture_output=True)
    assert r.returncode == 0, r.stderr
    g(root, "rm", "-q", "tools/round-47/decoy.txt")
    g(root, "commit", "-qm", "merge side2 (deletes frozen decoy)")
    rev = g(root, "rev-parse", "HEAD").stdout.strip()
    return freeze, rev


def freeze_probe(root, gate_kind):
    freeze, rev = tamper_repo(root, gate_kind)
    net = g(root, "diff", "--name-status", freeze, rev, "--", "tools/round-47/").stdout.strip()
    if gate_kind is None:
        code, rec = real_gate.freeze_state(root, freeze, rev, "plans/round-47-claims.md")
    else:
        mod = load_gate_from(os.path.join(root, "tools", "round-46", "gate.py"),
                             "gate_" + gate_kind.replace("-", "_"))
        code, rec = mod.freeze_state(root, freeze, rev, "plans/round-47-claims.md")
    return {"kind": gate_kind or "genuine", "freeze": freeze, "rev": rev,
            "net_tree_diff": net.splitlines(),
            "freeze_state_exit": code,
            "reason": rec.get("reason"),
            "touched": rec.get("touched"),
            "frozen_path_changed": rec.get("frozen_path_changed")}


def main():
    root, err = real_gate.scratch("kaidoku-r47-critc1-")
    assert not err, err
    out = {"clause7_scores": [], "freeze_state": [],
           "exact_py_sha256": hashlib.sha256(EXACT_SRC.encode()).hexdigest(),
           "gate_py_sha256": hashlib.sha256(GATE_SRC.encode()).hexdigest()}
    try:
        for kind in ("F1-comment-literal", "F2-no-format", "F3-dead-call",
                     "F4-runtime-reorder", "F5-decoy-function"):
            out["clause7_scores"].append(clause7(kind, root))
        # control: the clause must fire on a reversed pair
        rev_gate = GATE_SRC.replace(exact.ORDER, exact.REVERSED, 1)
        pin = hashlib.sha256(EXACT_SRC.encode()).hexdigest()
        files = {"SKILL.md": exact.skill_text(exact.good_block(pin=pin)),
                 "plans/round-47-claims.md": CLAIMS,
                 "corpus/lessons/round-46.md": "lesson line\n" * 240,
                 "tools/round-47/exact.py": EXACT_SRC, "tools/round-46/gate.py": rev_gate}
        d, rev = exact._repo(files, root, prefix="ctl-")
        try:
            code, rec = exact.score(files["SKILL.md"], lambda p: real_gate.show(d, rev, p),
                                    "v3", rev, battery=None)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        out["clause7_scores"].append({"kind": "C0-reversed-control",
                                      "order_literal_count": rev_gate.count(exact.ORDER),
                                      "reversed_count": rev_gate.count(exact.REVERSED),
                                      "score_exit": code, "failing": rec.get("failing")})
        for kind in (None, "F1-comment-literal", "F2-no-format", "F3-dead-call", "F5-decoy-function"):
            d = tempfile.mkdtemp(dir=root, prefix="fz-")
            try:
                out["freeze_state"].append(freeze_probe(d, kind))
            finally:
                pass  # keep for CLI run below if needed
    finally:
        pass
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
