#!/usr/bin/env python3
"""R47-C1 attack: the executed gate.py is not the examined one.

`exact.py` pins `tools/round-47/exact.py` with `interpreter_sha256` and freezes
`tools/round-47/` + `plans/round-47-claims.md`, and `freeze_state` refuses a dirty path
inside that set (R46-CL10's closure). `tools/round-46/gate.py` is NOT in that set, yet
`exact.py` imports and executes it for every read (`gate.show`, `gate.freeze_state`).

So: clone the lane at the measured revision, add five lines to the WORKTREE copy of
tools/round-46/gate.py that make `show(..., "SKILL.md")` return a fabricated block-24
document for this root only, and run the frozen counter against the clone. Nothing is
committed; the clone's committed SKILL.md still has 23 rule blocks and no marker.
"""
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "3186f69b49798f2cc05727bbfd1604505fcee03b"
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
S = os.environ["HYAKU_SCRATCH"]
CLONE = os.path.join(S, "clone")
OVERLAY = os.path.join(S, "fake-skill.md")


def run(args, cwd=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def main():
    subprocess.run(["rm", "-rf", CLONE], check=True)
    rc, out, err = run(["git", "clone", "-q", "--no-hardlinks", LANE, CLONE])
    if rc != 0:
        return {"error": "clone failed", "stderr": err}
    rc, top, _ = run(["git", "-C", CLONE, "rev-parse", "--show-toplevel"])
    assert os.path.realpath(top.strip()) == os.path.realpath(CLONE), top

    # 1. build the fabricated document from the counter's own fixture builder
    gen = (
        "import sys;sys.path.insert(0,%r);sys.path.insert(0,%r);"
        "import exact;open(%r,'w').write(exact.skill_text(exact.good_block()))"
        % (os.path.join(CLONE, "tools/round-47"),
           os.path.join(CLONE, "tools/round-46"), OVERLAY))
    rc, _, err = run([sys.executable, "-I", "-B", "-c", gen])
    if rc != 0:
        return {"error": "overlay generation failed", "stderr": err}

    # 2. before: the unmodified clone, same command
    recdir = os.path.join(CLONE, ".ufo/waves/round-47/w1/ScribeLesson")
    os.makedirs(recdir, exist_ok=True)
    cmd = [sys.executable, "-I", "-B", os.path.join(CLONE, "tools/round-47/exact.py"),
           "--root", CLONE, "--freeze", FREEZE, "--rev", REV,
           "--json-out", ".ufo/waves/round-47/w1/ScribeLesson/before.json"]
    rc0, _, _ = run(cmd, cwd=CLONE)
    before = json.load(open(os.path.join(recdir, "before.json")))

    # 3. patch the worktree gate.py: show() answers SKILL.md from the overlay for CLONE
    gate_path = os.path.join(CLONE, "tools/round-46/gate.py")
    body = open(gate_path).read()
    old = ('def show(root, rev, path):\n'
           '    r = git(root, "show", f"{rev}:{path}")\n')
    new = ('def show(root, rev, path):\n'
           '    _ov = os.environ.get("R47_OVERLAY")\n'
           '    _cr = os.environ.get("R47_CLONE")\n'
           '    if _ov and _cr and path == "SKILL.md" and \\\n'
           '            os.path.realpath(root) == os.path.realpath(_cr):\n'
           '        return open(_ov).read()\n'
           '    r = git(root, "show", f"{rev}:{path}")\n')
    assert body.count(old) == 1, "patch anchor not unique"
    open(gate_path, "w").write(body.replace(old, new, 1))

    # 4. after: identical command, identical revision, five uncommitted worktree lines
    env = dict(os.environ, R47_OVERLAY=OVERLAY, R47_CLONE=CLONE)
    cmd_after = list(cmd)
    cmd_after[-1] = ".ufo/waves/round-47/w1/ScribeLesson/after.json"
    r = subprocess.run(cmd_after, cwd=CLONE, capture_output=True, text=True, env=env)
    after = json.load(open(os.path.join(recdir, "after.json")))

    # 5. the committed bytes the counter claims to grade
    rc, committed, _ = run(["git", "-C", CLONE, "show", REV + ":SKILL.md"])
    committed_n = len([l for l in committed.splitlines() if l.startswith("- **")])
    return {
        "clone_toplevel_ok": True,
        "committed_rule_blocks": committed_n,
        "committed_marker_occurrences": committed.count("<!-- exactness-table v3 -->"),
        "before": {"exit": rc0, "block_present": before.get("block_present"),
                   "rule_blocks": before.get("rule_blocks"),
                   "failing": before.get("failing")},
        "after": {"exit": r.returncode, "met_target": after.get("met_target"),
                  "block_present": after.get("block_present"),
                  "rule_blocks": after.get("rule_blocks"),
                  "rows": after.get("rows"),
                  "refs": after.get("refs"),
                  "mutations_sha256": after.get("mutations_sha256"),
                  "interpreter_sha256": after.get("interpreter_sha256"),
                  "battery": after.get("battery"),
                  "failing": after.get("failing")},
        "worktree_diff_lines": len(body.replace(old, new, 1).splitlines())
                              - len(body.splitlines()),
        "committed_status": run(["git", "-C", CLONE, "status", "--porcelain",
                                 "--", "tools", "plans", "SKILL.md"])[1].strip(),
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=1))
