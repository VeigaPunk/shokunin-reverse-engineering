#!/usr/bin/env python3
"""Exit-code-semantics probe matrix for tools/round-47/{exact,record}.py.

Every probe: exact command, exit, stdout sha256, UTC. Expected: 2 for every
could-not-evaluate input, and never 0.
"""
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

S = "/fast/scratch/hyaku/kaidoku-r47/MutExitCodes"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
ENV = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
OUT = []


def sh(cmd, cwd=None, check=False):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=ENV)
    if check and r.returncode != 0:
        raise RuntimeError("fixture step failed: %s\n%s" % (" ".join(cmd), r.stderr))
    return r


def lane_show(rev, path):
    r = sh(["git", "-C", LANE, "show", "%s:%s" % (rev, path)])
    return r.stdout if r.returncode == 0 else None


def repo(name, files, identity=("fx@round47", "round47 fixture")):
    d = tempfile.mkdtemp(dir=S, prefix=name + "-")
    sh(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", identity[0]), ("user.name", identity[1])):
        sh(["git", "-C", d, "config", k, v], check=True)
    top = sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise RuntimeError("fixture toplevel %r != %r" % (top, d))
    put(d, files)
    return d


def put(d, files):
    for p, body in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        if isinstance(body, bytes):
            with open(full, "wb") as fh:
                fh.write(body)
        else:
            with open(full, "w") as fh:
                fh.write(body)


def commit(d, msg):
    sh(["git", "-C", d, "add", "-A"], check=True)
    sh(["git", "-C", d, "commit", "-q", "-m", msg], check=True)
    return sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()


def run(probe, cmd, expect, note=""):
    t = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=S, env=ENV, timeout=900)
    h = hashlib.sha256(r.stdout.encode()).hexdigest()
    rec = {"probe": probe, "utc": t, "cmd": " ".join(cmd), "expect": expect,
           "exit": r.returncode, "verdict": ("pass" if r.returncode == expect else "FAIL"),
           "stdout_sha256": h,
           "stdout": r.stdout[:700].replace("\n", " "),
           "stderr": r.stderr[-400:].replace("\n", " "), "note": note}
    OUT.append(rec)
    print(json.dumps(rec))
    return rec


C1 = os.path.join(LANE, "tools/round-47/exact.py")
C2 = os.path.join(LANE, "tools/round-47/record.py")

CARD = """# card

## Owned axes

| Axis | Baseline -> current score, 0-10 | Observable | Evidence | Round |
|---|---|---|---|---|
| coverage | 9.72 -> 10.0 | 1/1 knowledge files mapped | x | r1 |
| depth | 9.0 -> 10.0 | 1/1 | x | r1 |

## Round 8

Earlier round, no atoms.

## Round 9

Base `%s`. Waves: 1 + 1 = 2 seats. `git log %s..%s -- tools/x/` is empty. See `.ufo/waves/round-9/w1-dispatch.json`.

## Record corrections - round 47

- corrects seats round-9: 2 waves, 2 seats total
- corrects window round-9: empty in %s..%s -- tools/x/
"""


def card_text(base, tip):
    return CARD % (tip[:8], base[:8], base[:8], base[:8], base[:8])


def c2_fixture():
    """Base -> landing -> frozen-counter-tampered, with a claims file naming the freeze."""
    files = {
        ".ufo/waves/round-9/w1-dispatch.json": json.dumps({"counts": {"spawn": 1}}),
        ".ufo/waves/round-9/w2-dispatch.json": json.dumps({"counts": {"spawn": 1}}),
        "tools/x/keep.md": "x\n",
        "corpus/README.md": "# readme\n\n## Coverage map\n\n- 2026-10-01-x - x\n\n## Gaps\n\ntail\n",
        "corpus/knowledge/2026-10-01-x.md": "x\n",
        "plans/round-47-claims.md": ("# claims\n\n## Frozen paths (exact)\n\n"
                                     "- `plans/round-47-claims.md`\n- `tools/round-47/`\n"),
    }
    d = repo("c2fx", files)
    base = commit(d, "base")
    put(d, {"SCORECARD.md": card_text(base, base),
            "tools/round-47/record.py": open(C2).read()})
    land = commit(d, "landing")
    return d, base, land


def main():
    which = sys.argv[1:] or ["lane", "claims", "crash", "card", "root"]
    FZ = os.environ.get("FZ", "62e33f7dd75c8e3285967b26419842c106f6c965")
    HEAD = sh(["git", "-C", LANE, "rev-parse", "--short", "HEAD"]).stdout.strip()

    if "lane" in which:
        run("c1-lane-declared-freeze-A2-at-head", [
            "python3", "-I", "-B", C1, "--root", LANE, "--freeze", FZ,
            "--rev", HEAD, "--no-battery"], 2,
            "the claims' declared freeze (A2) against a rev whose tools/round-47/ moved")
        run("c1-lane-freeze-eq-rev", [
            "python3", "-I", "-B", C1, "--root", LANE, "--freeze", FZ,
            "--rev", FZ, "--no-battery"], None, "control: freeze == rev")
        run("c2-lane-head", [
            "python3", "-I", "-B", C2, "--root", LANE, "--rev", HEAD, "--no-battery"],
            None, "C2 has no freeze argument at all")

    if "claims" in which:
        base_files = {"SKILL.md": lane_show(HEAD, "SKILL.md"),
                      "tools/round-47/exact.py": lane_show(HEAD, "tools/round-47/exact.py"),
                      "tools/round-46/gate.py": lane_show(HEAD, "tools/round-46/gate.py"),
                      "corpus/lessons/round-46.md": lane_show(HEAD, "corpus/lessons/round-46.md"),
                      "corpus/lessons/round-45.md": lane_show(HEAD, "corpus/lessons/round-45.md")}
        variants = {
            "absent": None,
            "no-frozen-heading": "# claims\n\n## Non-goals\n\nnone\n",
            "frozen-empty": "# claims\n\n## Frozen paths (exact)\n\nnothing here\n",
            "binary": b"\xff\xfe\x00claims\x00\n",
            "frozen-after-other-heading": ("# claims\n\n## Frozen paths (exact)\n\n"
                                           "- `plans/round-47-claims.md`\n- `tools/round-47/`\n\n"
                                           "## After\n\ntail\n"),
        }
        for name, body in variants.items():
            files = dict(base_files)
            if body is not None:
                files["plans/round-47-claims.md"] = body
            d = repo("cl-" + name, files)
            rev = commit(d, "claims " + name)
            run("c1-claims-%s" % name, [
                "python3", "-I", "-B", os.path.join(d, "tools/round-47/exact.py"),
                "--root", d, "--freeze", rev, "--rev", rev, "--no-battery"], 2,
                "malformed claims at BOTH ends: no frozen-path change, only the parse can fail")
            if name in ("absent", "no-frozen-heading", "binary"):
                continue
        # control: the valid claims shape at freeze == rev must NOT be 2
        d = repo("cl-valid", dict(base_files, **{
            "plans/round-47-claims.md": ("# claims\n\n## Frozen paths (exact)\n\n"
                                         "- `plans/round-47-claims.md`\n- `tools/round-47/`\n")}))
        rev = commit(d, "claims valid")
        run("c1-claims-valid-control", [
            "python3", "-I", "-B", os.path.join(d, "tools/round-47/exact.py"),
            "--root", d, "--freeze", rev, "--rev", rev, "--no-battery"], None,
            "control: valid claims, freeze == rev")

    if "crash" in which:
        body = lane_show(HEAD, "tools/round-47/exact.py")
        skill = lane_show(HEAD, "SKILL.md")
        claims = lane_show(HEAD, "plans/round-47-claims.md")
        gate_body = lane_show(HEAD, "tools/round-46/gate.py")
        common = {"SKILL.md": skill, "plans/round-47-claims.md": claims,
                  "tools/round-46/gate.py": gate_body,
                  "corpus/lessons/round-46.md": lane_show(HEAD, "corpus/lessons/round-46.md"),
                  "corpus/lessons/round-45.md": lane_show(HEAD, "corpus/lessons/round-45.md")}

        def c1_variant(name, needle, repl, expect, at="score"):
            files = dict(common)
            files["tools/round-47/exact.py"] = body.replace(needle, repl, 1)
            d = repo("cr-" + name, files)
            rev = commit(d, name)
            run("c1-crash-%s" % name, [
                "python3", "-I", "-B", os.path.join(d, "tools/round-47/exact.py"),
                "--root", d, "--freeze", rev, "--rev", rev, "--no-battery"], expect,
                "crash injected at %s in a scratch copy" % at)

        def_score = "def score(skill, files, profile, rev, battery=None):\n"
        # control first: unmutated copy of the same fixture
        d = repo("cr-control", dict(common, **{"tools/round-47/exact.py": body}))
        rev = commit(d, "control")
        run("c1-crash-control-unmutated", [
            "python3", "-I", "-B", os.path.join(d, "tools/round-47/exact.py"),
            "--root", d, "--freeze", rev, "--rev", rev, "--no-battery"], None,
            "control: identical fixture, no injected crash")
        c1_variant("score", def_score,
                   def_score + '    raise RuntimeError("injected-crash-in-score")\n', 2)
        c1_variant("keyboardinterrupt", def_score,
                   def_score + '    raise KeyboardInterrupt("injected")\n', None,
                   at="score (BaseException, not Exception)")
        c1_variant("memoryerror", def_score,
                   def_score + '    raise MemoryError("injected")\n', 2)

        c2body = open(C2).read()
        c2common = {"tools/round-46/gate.py": gate_body,
                    "SCORECARD.md": CARD % ("0000000", "0000000", "0000000", "0000000", "0000000"),
                    "tools/x/keep.md": "x\n",
                    ".ufo/waves/round-9/w1-dispatch.json": json.dumps({"counts": {"spawn": 1}}),
                    ".ufo/waves/round-9/w2-dispatch.json": json.dumps({"counts": {"spawn": 1}})}
        # valid card needs a real base..tip window; build base then tip
        d = repo("cr2", {"tools/x/keep.md": "x\n",
                         "SCORECARD.md": "# card\n\n## Round 8\n\nno atoms\n",
                         ".ufo/waves/round-9/w1-dispatch.json": json.dumps({"counts": {"spawn": 1}}),
                         ".ufo/waves/round-9/w2-dispatch.json": json.dumps({"counts": {"spawn": 1}})})
        b = commit(d, "base")
        put(d, {"SCORECARD.md": card_text(b, b),
                "tools/round-47/record.py": c2body})
        tip = commit(d, "tip")
        run("c2-crash-control-unmutated", [
            "python3", "-I", "-B", os.path.join(d, "tools/round-47/record.py"),
            "--root", d, "--rev", tip, "--no-battery"], None, "control")
        for name, needle, repl, expect, at in (
            ("evaluate-text", "def evaluate_text(card, files, root, rev, battery=None):\n",
             "def evaluate_text(card, files, root, rev, battery=None):\n"
             '    raise RuntimeError("injected")\n', 2, "evaluate_text"),
            ("post-guard-emit-payload",
             '    code, receipt = gate.main_guard(lambda: evaluate(args.root, args.rev,\n'
             '                                                     not args.no_battery))\n',
             '    code, receipt = gate.main_guard(lambda: evaluate(args.root, args.rev,\n'
             '                                                     not args.no_battery))\n'
             '    receipt["unserialisable"] = {1, 2}\n', 2,
             "receipt after the guard, crashes inside emit()"),
            ("keyboardinterrupt", "def evaluate_text(card, files, root, rev, battery=None):\n",
             "def evaluate_text(card, files, root, rev, battery=None):\n"
             '    raise KeyboardInterrupt("injected")\n', 2, "evaluate_text BaseException"),
        ):
            files = {"tools/x/keep.md": "x\n",
                     "tools/round-46/gate.py": gate_body,
                     "SCORECARD.md": card_text(b, b),
                     "tools/round-47/record.py": c2body.replace(needle, repl, 1),
                     ".ufo/waves/round-9/w1-dispatch.json": json.dumps({"counts": {"spawn": 1}}),
                     ".ufo/waves/round-9/w2-dispatch.json": json.dumps({"counts": {"spawn": 1}})}
            d2 = tempfile.mkdtemp(dir=S, prefix="cr2-" + name + "-")
            sh(["git", "-C", d2, "clone", "-q", d, "."], check=True)
            for k, v in (("user.email", "fx@round47"), ("user.name", "round47 fixture")):
                sh(["git", "-C", d2, "config", k, v], check=True)
            put(d2, files)
            rev2 = commit(d2, name)
            run("c2-crash-%s" % name, [
                "python3", "-I", "-B", os.path.join(d2, "tools/round-47/record.py"),
                "--root", d2, "--rev", rev2, "--no-battery"], expect, at)

    if "card" in which:
        # unreadable SCORECARD, four ways, on top of a valid C2 fixture
        d0, base, land = c2_fixture()
        run("c2-card-control", ["python3", "-I", "-B", C2, "--root", d0, "--rev", land,
                                "--no-battery"], None, "control on the C2 fixture")
        # 1. absent at rev
        d = repo("cd-absent", {"tools/x/keep.md": "x\n"})
        r1 = commit(d, "no card")
        run("c2-card-absent", ["python3", "-I", "-B", C2, "--root", d, "--rev", r1,
                               "--no-battery"], 2)
        # 2. invalid UTF-8 bytes
        d = repo("cd-binary", {"tools/x/keep.md": "x\n",
                               "SCORECARD.md": b"\xff\xfe# card\n\x00\x80\n"})
        r2 = commit(d, "binary card")
        run("c2-card-invalid-utf8", ["python3", "-I", "-B", C2, "--root", d, "--rev", r2,
                                     "--no-battery"], 2)
        # 3. card is a directory at rev
        d = repo("cd-dir", {"tools/x/keep.md": "x\n", "SCORECARD.md/part.md": "x\n"})
        r3 = commit(d, "card is a dir")
        run("c2-card-is-directory", ["python3", "-I", "-B", C2, "--root", d, "--rev", r3,
                                     "--no-battery"], 2)
        # 4. blob object removed from .git/objects (tree intact, object gone)
        d = repo("cd-corrupt", {"tools/x/keep.md": "x\n",
                                "SCORECARD.md": card_text("0000000", "0000000")})
        r4 = commit(d, "corrupt card")
        oid = sh(["git", "-C", d, "rev-parse", "HEAD:SCORECARD.md"]).stdout.strip()
        obj = os.path.join(d, ".git/objects", oid[:2], oid[2:])
        removed = os.path.exists(obj)
        if removed:
            os.chmod(obj, 0o600)
            os.remove(obj)
        run("c2-card-object-missing", ["python3", "-I", "-B", C2, "--root", d, "--rev", r4,
                                       "--no-battery"], 2,
            "loose object %s removed=%s (packed=%s)" % (oid, removed, not removed))
        # 5. worktree card unreadable (chmod 000) while the committed bytes are fine
        d = repo("cd-perm", {"tools/x/keep.md": "x\n",
                             "SCORECARD.md": card_text("0000000", "0000000")})
        r5 = commit(d, "perm card")
        os.chmod(os.path.join(d, "SCORECARD.md"), 0o000)
        run("c2-card-worktree-chmod000", ["python3", "-I", "-B", C2, "--root", d, "--rev", r5,
                                          "--no-battery"], None,
            "worktree unreadability is invisible to a git-object reader")

    if "root" in which:
        run("c1-root-not-a-repo", [
            "python3", "-I", "-B", C1, "--root", tempfile.mkdtemp(dir=S, prefix="nr-"),
            "--freeze", "HEAD", "--rev", "HEAD", "--no-battery"], 2)
        run("c1-root-missing", [
            "python3", "-I", "-B", C1, "--root", os.path.join(S, "does-not-exist"),
            "--freeze", "HEAD", "--rev", "HEAD", "--no-battery"], 2)
        run("c2-root-not-a-repo", [
            "python3", "-I", "-B", C2, "--root", tempfile.mkdtemp(dir=S, prefix="nr2-"),
            "--rev", "HEAD", "--no-battery"], 2)
        run("c1-argparse-missing-freeze", ["python3", "-I", "-B", C1, "--root", LANE,
                                           "--rev", "HEAD"], 2, "argparse usage error")
        run("c2-argparse-unknown-flag", ["python3", "-I", "-B", C2, "--root", LANE,
                                         "--rev", "HEAD", "--freeze", "x"], 2)

    with open(os.path.join(S, "receipts.jsonl"), "w") as fh:
        for rec in OUT:
            fh.write(json.dumps(rec) + "\n")
    bad = [r for r in OUT if r["verdict"] == "FAIL"]
    print("\nPROBES=%d FAIL=%d" % (len(OUT), len(bad)), file=sys.stderr)
    for r in bad:
        print("FAIL %s exit=%s expect=%s" % (r["probe"], r["exit"], r["expect"]), file=sys.stderr)


if __name__ == "__main__":
    main()
