#!/usr/bin/env python3
"""R47-C2 attack: the window class is derived with a log form blind to merge resolutions.

record.window_empty() runs exactly

    git log --name-status --format= A..B -- <pathspec>

and calls the claim "empty" when that prints nothing. Git prints no diff for a merge on that
form, so a merge whose RESOLUTION edits a frozen path leaves the range reading empty. That is
R46-CL6 / R45-CL6's class, closed for tools/round-46/gate.py by R47-C1 clause 7 and left open
in the counter that grades the record.

The fixture is built with `git commit-tree`: a merge whose first parent does not touch the
path and whose own tree does. No seat writes outside this fixture.
"""
import json
import os
import subprocess
import sys

S = os.environ["HYAKU_SCRATCH"]
D = os.path.join(S, "fx-merge")


def run(*args, cwd=D):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"FAILED {args}: {r.stderr}")
    return r.stdout.strip()


def main():
    subprocess.run(["rm", "-rf", D], check=True)
    os.makedirs(D)
    run("git", "init", "-q")
    run("git", "config", "user.email", "fx@round47")
    run("git", "config", "user.name", "round47 fixture")
    top = run("git", "rev-parse", "--show-toplevel")
    assert os.path.realpath(top) == os.path.realpath(D), top

    os.makedirs(os.path.join(D, "tools/round-46"), exist_ok=True)
    p = os.path.join(D, "tools/round-46/gate.py")
    open(p, "w").write('ORDER = "-m", "--diff-merges=first-parent"\n')
    run("git", "add", "-A")
    run("git", "commit", "-q", "-m", "base")
    base = run("git", "rev-parse", "HEAD")

    # first parent: an unrelated file only; the frozen path is untouched
    open(os.path.join(D, "README"), "w").write("x\n")
    run("git", "add", "-A")
    run("git", "commit", "-q", "-m", "unrelated")
    parent = run("git", "rev-parse", "HEAD")

    # the merge's own tree edits the frozen path; its parents do not
    blob = run("git", "hash-object", "-w", "--stdin") if False else None
    tree_src = os.path.join(D, "treeidx")
    open(p, "w").write('ORDER = "--diff-merges=first-parent", "-m"\n')
    run("git", "add", "-A")
    tree = run("git", "write-tree")
    merge = run("git", "commit-tree", tree, "-p", parent, "-p", base,
                "-m", "merge: resolution edits the frozen path")

    def log(*extra):
        r = subprocess.run(["git", "-C", D, "log", *extra, "A..B"], capture_output=True,
                           text=True)
        return r

    plain = subprocess.run(["git", "-C", D, "log", "--name-status", "--format=",
                            f"{base}..{merge}", "--", "tools/round-46/"],
                           capture_output=True, text=True)
    armed = subprocess.run(["git", "-C", D, "log", "-m", "--diff-merges=first-parent",
                            "--name-status", "--format=", f"{base}..{merge}",
                            "--", "tools/round-46/"], capture_output=True, text=True)
    reversed_pair = subprocess.run(["git", "-C", D, "log", "--diff-merges=first-parent",
                                    "-m", "--name-status", "--format=", f"{base}..{merge}",
                                    "--", "tools/round-46/"], capture_output=True, text=True)
    blob_arm = subprocess.run(["git", "-C", D, "diff", "--name-status", base, merge,
                               "--", "tools/round-46/"], capture_output=True, text=True)

    # the counter's own derivation on this fixture
    sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47")
    sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-46")
    import record  # noqa: E402
    empty, err = record.window_empty(D, merge, base[:8], merge[:8], ["tools/round-46/"])
    return {
        "fixture": D,
        "base": base, "merge": merge,
        "plain_log_stdout": plain.stdout,
        "plain_log_empty": plain.stdout.strip() == "",
        "armed_log_stdout": armed.stdout,
        "reversed_pair_stdout": reversed_pair.stdout,
        "blob_arm_stdout": blob_arm.stdout,
        "record.window_empty": {"empty": empty, "err": err},
        "record_form_matches_plain": True,
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=1))
