#!/usr/bin/env python3
"""Round-47 C1 kill-rule fixtures: does the frozen counter fail the five blocks the
claims file's Kill rule says it must fail? Same harness as attack4.py."""
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
EXACT = os.path.join(LANE, "tools/round-47/exact.py")
S = os.environ["HYAKU_SCRATCH"]
FILES = ["plans/round-47-claims.md", "tools/round-47/exact.py",
         "tools/round-46/gate.py", "corpus/lessons/round-46.md",
         "corpus/lessons/round-45.md"]
SELF_SHA = "dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c"
MUTS = ["substring-arm", "duplicate-routed-id", "stale-mutations-digest",
        "flag-order-drift"]
ORDER = '"-m", "--diff-merges=first-parent"'
REVERSED = '"--diff-merges=first-parent", "-m"'


def git_show(rev, path):
    return subprocess.run(["git", "-C", LANE, "show", rev + ":" + path],
                          capture_output=True, text=True, check=True).stdout


def build_repo(files, name, env):
    d = subprocess.run(["mktemp", "-d", "-p", S, "fx-" + name + "-XXXX"],
                       capture_output=True, text=True, check=True).stdout.strip()
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "kill fixture")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise SystemExit("toplevel mismatch")
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fixture " + name], check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         capture_output=True, text=True, check=True).stdout.strip()
    return d, rev


def score(d, rev, profile, env):
    cmd = [sys.executable, "-I", "-B", EXACT, "--root", d, "--freeze", rev,
           "--rev", rev, "--no-battery", "--profile", profile]
    p = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, " ".join(cmd)


def main():
    env = dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S)
    base_skill = git_show("HEAD", "SKILL.md")
    bodies = {p: git_show("HEAD", p) for p in FILES}
    # block 24 is the last craft block: from its bullet to the next "## "
    m24 = base_skill.index("\n- **24. ") + 1
    tail = base_skill.index("\n## ", m24)
    block24 = base_skill[m24:tail]
    b23_start = base_skill.index("\n- **23. ") + 1
    block23 = base_skill[b23_start:base_skill.index("\n- **24. ")]
    assert block24.startswith("- **24. "), block24[:40]

    def swap(new_block24):
        return base_skill[:m24] + new_block24.rstrip("\n") + base_skill[tail:]

    cases = []

    def add(name, skill, gate_text=None, expect=1, why=""):
        cases.append({"name": name, "skill": skill, "gate": gate_text,
                      "expect": expect, "why": why})

    add("k0-genuine", base_skill, None, 0, "control: the landed bytes")
    add("k1-blobberish", swap(block24.replace("| `symbol` |", "| `blobberish` |")),
        None, 1, "arm cell `blobberish`: v2 passes, v3 must fail clause 5")
    add("k3-digest-of-three",
        swap(block24.replace(
            "19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112",
            hashlib.sha256("\n".join(MUTS[:3]).encode()).hexdigest())),
        None, 1, "mutations_sha256 over three of four names")
    add("k4-flag-reversed", base_skill,
        bodies["tools/round-46/gate.py"].replace(ORDER, REVERSED, 1), 1,
        "gate.py carries the reversed flag pair")
    relabelled = block23.replace("- **23. ", "- **24. ", 1)
    lines = relabelled.split("\n", 1)
    if "<!-- exactness-table v3 -->" not in lines[0]:
        lines[0] = lines[0] + " <!-- exactness-table v3 -->"
        relabelled = "\n".join(lines)
    add("k5-block23-relabelled", swap(relabelled), None, 1,
        "block 23's text relabelled 24. with the v3 marker")
    add("k1b-order-ish", swap(block24.replace("| `symbol` |", "| `order-ish` |")),
        None, 1, "arm cell `order-ish`: a superstring of a real token, v2 must pass it")
    add("k6-arm-case", swap(block24.replace("| `symbol` |", "| `Symbol` |")), None, 1,
        "arm cell `Symbol`: case is part of the equality")
    add("k7-arm-punct", swap(block24.replace("| `symbol` |", "| `symbol`. |")), None, 1,
        "arm cell with a trailing period")

    out = []
    for c in cases:
        files = dict(bodies)
        files["SKILL.md"] = c["skill"]
        if c["gate"] is not None:
            files["tools/round-46/gate.py"] = c["gate"]
        d, rev = build_repo(files, c["name"], env)
        v3, out3, cmd = score(d, rev, "v3", env)
        v2, _, _ = score(d, rev, "v2", env)
        rec = {"name": c["name"], "why": c["why"], "fixture": d, "rev": rev,
               "command": cmd, "v3_exit": v3, "v2_exit": v2,
               "v3_stdout_sha256": hashlib.sha256(out3.encode()).hexdigest(),
               "skill_sha256": hashlib.sha256(c["skill"].encode()).hexdigest(),
               "expect": c["expect"],
               "verdict": "AS-EXPECTED" if v3 == c["expect"] else "MISMATCH"}
        try:
            rec["v3_failing"] = json.loads(out3).get("failing")
        except Exception:
            rec["v3_raw"] = out3[:300]
        out.append(rec)
        print("%-24s v3=%d v2=%d expect=%d %s %s" % (
            c["name"], v3, v2, c["expect"], rec["verdict"],
            (rec.get("v3_failing") or [])[:1]))
    with open(os.path.join(S, "kill-results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("\nMISMATCHES:", [r["name"] for r in out if r["verdict"] == "MISMATCH"] or "none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
