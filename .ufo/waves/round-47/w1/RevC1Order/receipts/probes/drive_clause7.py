#!/usr/bin/env python3
"""RevC1Order: does exact.py clause 7 survive gate.py reformatting / catch a reversed pair?

Scores the real frozen counter (imported read-only) against fixture repos whose only
difference is the layout of tools/round-46/gate.py. Nothing in the lane tree is written.
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
T47 = os.path.join(LANE, "tools", "round-47")
T46 = os.path.join(LANE, "tools", "round-46")
sys.path.insert(0, T47)
sys.path.insert(0, T46)
import gate          # noqa: E402
import exact         # noqa: E402

SCRATCH = sys.argv[1]
GATE_BODY = open(os.path.join(T46, "gate.py")).read()
EXACT_BODY = open(os.path.join(T47, "exact.py")).read()
ORIG_CALL = ('    r = git(root, "log", "-m", "--diff-merges=first-parent", "--name-status", "-z",\n'
             '            "--format=", f"{base}..{tip}", "--", *paths, binary=True)\n')
assert ORIG_CALL in GATE_BODY, "original call site not found verbatim"

REVERSED_ONE_LINE = ORIG_CALL.replace(
    '"-m", "--diff-merges=first-parent"',
    '"--diff-merges=first-parent", "-m"')

WRAPPED_FORWARD = ('    r = git(root, "log", "-m",\n'
                   '            "--diff-merges=first-parent", "--name-status", "-z",\n'
                   '            "--format=", f"{base}..{tip}", "--", *paths, binary=True)\n')
DOUBLE_SPACE = ORIG_CALL.replace('"-m", "--diff', '"-m",  "--diff')
SINGLE_QUOTES = ORIG_CALL.replace('"-m", "--diff-merges=first-parent"',
                                  "'-m', '--diff-merges=first-parent'")
KWARG = ('    r = git(root, "log", "--name-status", "-z",\n'
         '            "--format=", f"{base}..{tip}", "--", *paths, binary=True,\n'
         '            merges="first-parent")\n')
KWARG_SIG = ('def git(root, *args, binary=False, timeout=120, merges=None):\n'
             '    cmd = ["git", "-C", root, *args]\n'
             '    if merges:\n'
             '        cmd += ["-m", "--diff-merges=" + merges]\n'
             '    return subprocess.run(cmd, capture_output=True,\n'
             '                          text=not binary, timeout=timeout)\n')
ORIG_SIG = ('def git(root, *args, binary=False, timeout=120):\n'
            '    return subprocess.run(["git", "-C", root, *args], capture_output=True,\n'
            '                          text=not binary, timeout=timeout)\n')
REVERSED_WRAPPED_CALL = ('    r = git(root, "log",\n'
                         '            "--diff-merges=first-parent",\n'
                         '            "-m", "--name-status", "-z",\n'
                         '            "--format=", f"{base}..{tip}", "--", *paths, binary=True)\n')
COMMENT = ('# The shared history arm is evaluated in this order and the order is load-bearing:\n'
           '#   "-m", "--diff-merges=first-parent"\n')


def variant(body):
    return GATE_BODY.replace(ORIG_CALL, body)


def build(name, gate_text, comment=False):
    if comment:
        gate_text = gate_text.replace('TEMP_PARTITIONS = ("/tmp", "/var/tmp")\n',
                                      'TEMP_PARTITIONS = ("/tmp", "/var/tmp")\n' + COMMENT, 1)
    files = {
        "SKILL.md": exact.skill_text(exact.good_block()),
        "plans/round-47-claims.md": exact.CLAIMS_BODY,
        "corpus/lessons/round-46.md": "lesson line\n" * 240,
        exact.SELF: EXACT_BODY,
        exact.GATE46: gate_text,
        "plans/round-47-plain.md": "plain\n",
    }
    d, rev = exact._repo(files, SCRATCH, prefix="c7-")
    top = gate.git(d, "rev-parse", "--show-toplevel").stdout.strip()
    if top != d:
        raise RuntimeError("fixture toplevel mismatch: %r != %r" % (top, d))
    f = lambda p: gate.show(d, rev, p)  # noqa: E731
    try:
        c3, r3 = exact.score(files["SKILL.md"], f, "v3", rev, battery=None)
        c2, r2 = exact.score(files["SKILL.md"], f, "v2", rev, battery=None)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return {
        "name": name,
        "gate_sha256": hashlib.sha256(gate_text.encode()).hexdigest(),
        "literal_forward": gate_text.count(exact.ORDER),
        "literal_reversed": gate_text.count(exact.REVERSED),
        "v3_exit": c3,
        "v3_gate_literal": r3.get("gate_order_literal"),
        "v3_gate_reversed": r3.get("gate_order_reversed"),
        "v3_failing": [x for x in (r3.get("failing") or []) if "gate.py" in x or "sha256" in x],
        "v3_all_failing": r3.get("failing") or r3.get("reason"),
        "v2_exit": c2,
    }


def main():
    rows = []
    rows.append(build("v0-baseline-original", GATE_BODY))
    rows.append(build("v1-wrapped-forward-same-order", variant(WRAPPED_FORWARD)))
    rows.append(build("v2-double-space-forward-same-order", variant(DOUBLE_SPACE)))
    rows.append(build("v3-single-quotes-forward-same-order", variant(SINGLE_QUOTES)))
    rows.append(build("v4-helper-kwarg-order-built-at-runtime",
                      variant(KWARG).replace(ORIG_SIG, KWARG_SIG)))
    rows.append(build("v5-reversed-one-line", variant(REVERSED_ONE_LINE)))
    rows.append(build("v6-reversed-across-lines", variant(REVERSED_WRAPPED_CALL)))
    rows.append(build("v7-comment-keeps-literal-live-call-reversed-across-lines",
                      variant(REVERSED_WRAPPED_CALL), comment=True))
    rows.append(build("v8-comment-forward-live-call-reversed-one-line",
                      variant(REVERSED_ONE_LINE), comment=True))
    documented = GATE_BODY.replace(
        "def history_touched(root, base, tip, paths):\n",
        'def history_touched(root, base, tip, paths):\n'
        '    """Arm arguments, in this order: "-m", "--diff-merges=first-parent"."""\n', 1)
    assert documented != GATE_BODY
    rows.append(build("v9-forward-literal-in-docstring-plus-code", documented))
    print(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
