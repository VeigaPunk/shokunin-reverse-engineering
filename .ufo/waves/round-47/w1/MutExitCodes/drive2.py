#!/usr/bin/env python3
"""Second probe batch: a green C2 fixture (control -> tamper), C1 ancestry in a fixture,
post-guard --json-out crashes, and a green-state C1 fixture for the same."""
import datetime
import hashlib
import json
import os
import subprocess
import sys
import tempfile

S = "/fast/scratch/hyaku/kaidoku-r47/MutExitCodes"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
ENV = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
C1 = os.path.join(LANE, "tools/round-47/exact.py")
C2 = os.path.join(LANE, "tools/round-47/record.py")
OUT = []


def sh(cmd, check=False):
    r = subprocess.run(cmd, capture_output=True, text=True, env=ENV, cwd=S)
    if check and r.returncode != 0:
        raise RuntimeError("%s -> %s" % (" ".join(cmd), r.stderr))
    return r


def lane_show(rev, path):
    r = sh(["git", "-C", LANE, "show", "%s:%s" % (rev, path)])
    return r.stdout if r.returncode == 0 else None


def repo(name, files, branch=None):
    d = tempfile.mkdtemp(dir=S, prefix=name + "-")
    sh(["git", "-C", d, "init", "-q"], check=True)
    if branch:
        sh(["git", "-C", d, "checkout", "-q", "-b", branch], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "r47 fixture")):
        sh(["git", "-C", d, "config", k, v], check=True)
    top = sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    put(d, files)
    return d


def put(d, files):
    for p, body in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        with open(full, "wb" if isinstance(body, bytes) else "w") as fh:
            fh.write(body)


def commit(d, msg, allow_empty=False):
    sh(["git", "-C", d, "add", "-A"], check=True)
    args = ["git", "-C", d, "commit", "-q", "-m", msg] + (["--allow-empty"] if allow_empty else [])
    sh(args, check=True)
    return sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()


def run(probe, cmd, expect, note=""):
    t = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=S, env=ENV, timeout=900)
    rec = {"probe": probe, "utc": t, "cmd": " ".join(cmd), "expect": expect,
           "exit": r.returncode,
           "verdict": "pass" if r.returncode == expect else ("info" if expect is None else "FAIL"),
           "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
           "stdout": r.stdout[:600].replace("\n", " "),
           "stderr": r.stderr[-300:].replace("\n", " "), "note": note}
    OUT.append(rec)
    print(json.dumps(rec))
    return rec


CRAFT_RULES = "".join(
    "- **%d. Rule %d.** body, see `corpus/lessons/round-46.md:1-5`.\n\n" % (i, i)
    for i in range(1, 4))


def card(base8, tip8, seats="Waves: 1 + 1 = 2 seats", window=None, corrections=True):
    window = window or "`git log %s..%s -- tools/x/` is empty" % (base8, base8)
    text = ("# card\n\n## Owned axes\n\n"
            "| Axis | Baseline -> current score, 0-10 | Observable | Evidence | Round |\n"
            "|---|---|---|---|---|\n"
            "| coverage | 9.72 -> 10.0 | 1/1 knowledge files mapped | x | r1 |\n"
            "| depth | 9.3 -> 10.0 | 3/3 craft blocks resolve | x | r1 |\n\n"
            "## Round 8\n\nAn earlier round with no atoms.\n\n"
            "## Round 9\n\nBase `%s`. %s. %s. See `.ufo/waves/round-9/w1-dispatch.json`.\n"
            % (tip8, seats, window))
    if corrections:
        text += ("\n## Record corrections \u2014 round 47\n\n"
                 "- corrects seats round-9: 2 waves, 2 seats total\n"
                 "- corrects window round-9: empty in %s..%s -- tools/x/\n" % (base8, base8))
    return text


def green_c2():
    """base -> landing; at landing record.py must exit 0."""
    d = repo("g2", {
        "tools/x/keep.md": "x\n",
        "SKILL.md": "# SKILL\n\n## Queue-drain craft (fixture) \n\n" + CRAFT_RULES +
                    "\n## Next\n\ntail\n",
        "corpus/lessons/round-46.md": "\n".join("line %d" % i for i in range(1, 40)) + "\n",
        "corpus/README.md": "# readme\n\n## Coverage map\n\n- 2026-10-01-x - x\n\n## Gaps\n\ntail\n",
        "corpus/knowledge/2026-10-01-x.md": "x\n",
        ".ufo/waves/round-9/w1-dispatch.json": json.dumps({"counts": {"spawn": 1}}),
        ".ufo/waves/round-9/w2-dispatch.json": json.dumps({"counts": {"spawn": 1}}),
        "plans/round-47-claims.md": ("# claims\n\n## Frozen paths (exact)\n\n"
                                     "- `plans/round-47-claims.md`\n- `tools/round-47/`\n"),
        "tools/round-46/gate.py": open(os.path.join(LANE, "tools/round-46/gate.py")).read(),
    })
    base = commit(d, "base")
    put(d, {"SCORECARD.md": card(base[:8], base[:8]),
            "tools/round-47/record.py": open(C2).read()})
    land = commit(d, "landing")
    return d, base, land


def main():
    d, base, land = green_c2()
    run("c2-green-control", ["python3", "-I", "-B", os.path.join(d, "tools/round-47/record.py"),
                             "--root", d, "--rev", land, "--no-battery"], 0,
        "green fixture control")

    # T1: the frozen counter itself is rewritten after the declared freeze
    d1 = tempfile.mkdtemp(dir=S, prefix="g2-t1-")
    sh(["git", "-C", d1, "clone", "-q", d, "."], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "r47 fixture")):
        sh(["git", "-C", d1, "config", k, v], check=True)
    body = open(os.path.join(d1, "tools/round-47/record.py")).read()
    assert body == open(C2).read()
    put(d1, {"tools/round-47/record.py": body + "\n# post-freeze tamper of a frozen path\n"})
    t1 = commit(d1, "tamper frozen counter")
    run("c2-frozen-counter-tampered", [
        "python3", "-I", "-B", os.path.join(d1, "tools/round-47/record.py"),
        "--root", d1, "--rev", t1, "--no-battery"], 2,
        "claims: 'a change [to tools/round-47/] makes both counters exit 2 frozen_path_changed'")

    # T2: the frozen claims file is rewritten after the declared freeze
    d2 = tempfile.mkdtemp(dir=S, prefix="g2-t2-")
    sh(["git", "-C", d2, "clone", "-q", d, "."], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "r47 fixture")):
        sh(["git", "-C", d2, "config", k, v], check=True)
    put(d2, {"plans/round-47-claims.md": "# claims\n\n## Frozen paths (exact)\n\n"
                                        "- `plans/round-47-claims.md`\n"})
    t2 = commit(d2, "tamper frozen claims")
    run("c2-frozen-claims-tampered", [
        "python3", "-I", "-B", os.path.join(d2, "tools/round-47/record.py"),
        "--root", d2, "--rev", t2, "--no-battery"], 2, "same claim, claims-file arm")

    # T3: --rev on a diverged side branch (C2 has no freeze and no ancestry binding)
    d3 = tempfile.mkdtemp(dir=S, prefix="g2-t3-")
    sh(["git", "-C", d3, "clone", "-q", d, "."], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "r47 fixture")):
        sh(["git", "-C", d3, "config", k, v], check=True)
    sh(["git", "-C", d3, "checkout", "-q", "-b", "side", base], check=True)
    put(d3, {"tools/x/keep.md": "x\nside\n"})
    side = commit(d3, "side branch")
    run("c2-rev-on-side-branch", [
        "python3", "-I", "-B", os.path.join(d3, "tools/round-47/record.py"),
        "--root", d3, "--rev", side, "--no-battery"], 2,
        "a rev that is not a descendant of the landing still scores")

    # T4: post-guard --json-out failures on the green C2 fixture
    for name, target in (("missing-parent", os.path.join(d, "no/such/x.json")),
                         ("is-a-directory", os.path.join(d, "logs")),
                         ("readonly-file", os.path.join(d, "ro.json"))):
        if name == "readonly-file":
            open(target, "w").write("{}\n")
            os.chmod(target, 0o444)
        run("c2-jsonout-" + name, [
            "python3", "-I", "-B", os.path.join(d, "tools/round-47/record.py"),
            "--root", d, "--rev", land, "--no-battery", "--json-out", target], 2,
            "a refused-to-open --json-out target")
        if name == "readonly-file":
            os.chmod(target, 0o644)
    run("c2-jsonout-good-control", [
        "python3", "-I", "-B", os.path.join(d, "tools/round-47/record.py"),
        "--root", d, "--rev", land, "--no-battery", "--json-out",
        os.path.join(d, "receipt.json")], 0, "control: writable target")

    # C1 fixture ancestry: freeze on a diverged branch
    files = {"SKILL.md": lane_show(land if False else "62e33f7d", "SKILL.md"),
             "plans/round-47-claims.md": lane_show("62e33f7d", "plans/round-47-claims.md"),
             "tools/round-47/exact.py": lane_show("62e33f7d", "tools/round-47/exact.py"),
             "tools/round-46/gate.py": lane_show("62e33f7d", "tools/round-46/gate.py")}
    for p in ("corpus/lessons/round-46.md", "corpus/lessons/round-45.md", "corpus/QUALITY.md",
              "corpus/knowledge/2026-10-01-x.md"):
        b = lane_show("62e33f7d", p)
        if b is not None:
            files[p] = b
    d4 = repo("g1", files)
    mainrev = commit(d4, "main")
    sh(["git", "-C", d4, "checkout", "-q", "-b", "side", mainrev], check=True)
    put(d4, {"SKILL.md": files["SKILL.md"] + "\n<!-- side -->\n"})
    siderev = commit(d4, "side")
    run("c1-green-control", ["python3", "-I", "-B", os.path.join(d4, "tools/round-47/exact.py"),
                             "--root", d4, "--freeze", mainrev, "--rev", mainrev,
                             "--no-battery"], None, "control: freeze == rev on the fixture")
    run("c1-freeze-side-branch", [
        "python3", "-I", "-B", os.path.join(d4, "tools/round-47/exact.py"), "--root", d4,
        "--freeze", siderev, "--rev", mainrev, "--no-battery"], 2,
        "freeze on a diverged branch is not an ancestor of rev")
    os.makedirs(os.path.join(d4, "logs", "keep"), exist_ok=True)
    open(os.path.join(d4, "logs", "keep", ".k"), "w").write("k\n")
    sh(["git", "-C", d4, "add", "-A"], check=True)
    commit(d4, "logs dir")
    for name, target in (("missing-parent", os.path.join(d4, "no/such/x.json")),
                         ("is-a-directory", os.path.join(d4, "logs"))):
        run("c1-jsonout-" + name, [
            "python3", "-I", "-B", os.path.join(d4, "tools/round-47/exact.py"), "--root", d4,
            "--freeze", mainrev, "--rev", mainrev, "--no-battery", "--json-out", target], 2,
            "post-guard emit() failure")

    # boundary: an import-time failure is outside main_guard
    d5 = repo("imp", {"tools/round-47/exact.py": open(C1).read(),
                      "tools/x/keep.md": "x\n"})
    r5 = commit(d5, "no gate.py")
    run("c1-import-failure", ["python3", "-I", "-B",
                              os.path.join(d5, "tools/round-47/exact.py"),
                              "--root", d5, "--freeze", r5, "--rev", r5, "--no-battery"],
        2, "boundary: gate.py absent, import fails before main_guard")
    d6 = repo("imp2", {"tools/round-47/record.py": open(C2).read(),
                       "tools/x/keep.md": "x\n"})
    r6 = commit(d6, "no gate.py")
    run("c2-import-failure", ["python3", "-I", "-B",
                              os.path.join(d6, "tools/round-47/record.py"),
                              "--root", d6, "--rev", r6, "--no-battery"],
        2, "boundary: gate.py absent, import fails before main_guard")

    with open(os.path.join(S, "receipts2.jsonl"), "w") as fh:
        for rec in OUT:
            fh.write(json.dumps(rec) + "\n")
    bad = [r for r in OUT if r["verdict"] == "FAIL"]
    print("\nPROBES=%d FAIL=%d" % (len(OUT), len(bad)), file=sys.stderr)
    for r in bad:
        print("FAIL %s exit=%s expect=%s | %s" % (r["probe"], r["exit"], r["expect"],
                                                  r["stdout"][:150]), file=sys.stderr)


if __name__ == "__main__":
    main()
