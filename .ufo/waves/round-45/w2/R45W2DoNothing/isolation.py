#!/usr/bin/env python3
"""Isolate whether c1-counter's selftest case `red-relabelled-21-block` is red because of
the relabel or because of the block COUNT. Reproduce with:
  S=<scratch> TMPDIR=$S/tmp HYAKU_SCRATCH=$S/tmp python3 isolation.py <S> <lane-root>
Builds two fixtures that differ only in the number of plain blocks (20 vs 21); both
rename the block's ordinal from "22." to "20.".

Result recorded in ../isolation.json / receipts/iso-relabel-*.{json,stdout}:
  20 plain -> rule_blocks 21 -> exit 1, failing == ["rule_blocks 21 != 22"]
  21 plain -> rule_blocks 22 -> exit 0, met_target true
So the relabel is never exercised; the count is the whole reason.
"""
import json, os, subprocess, sys, tempfile

S, L = sys.argv[1], sys.argv[2]
FREEZE = "f762b7273e3f6ca3c710bb37d5de92a4a4417aec"


def show(p, rev=FREEZE):
    r = subprocess.run(["git", "-C", L, "show", f"{rev}:{p}"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout


def git(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


MARK = "<!-- freeze-integrity-table v1 -->"
GOOD_ROW = "| post-freeze commit touches a frozen path | commit arm | 1 | `--json-out` receipt |\n"
HDR = "| trigger | arm | exit | receipt |\n|---|---|---|---|\n"
REFS = ["corpus/lessons/round-44.md:1", "corpus/lessons/round-44-verifier-spotcheck.md:1",
        "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:1", "plans/round-45-claims.md:1"]


def build(label, n_plain, block_label):
    d = tempfile.mkdtemp(dir=os.path.join(S, "fx"), prefix=label + "-")
    git(d, "init", "-q"); git(d, "config", "user.email", "x@y"); git(d, "config", "user.name", "x")
    assert os.path.realpath(git(d, "rev-parse", "--show-toplevel").stdout.strip()) == os.path.realpath(d)
    block = (f"- **{block_label}. Freeze integrity.** {MARK} S140 tools/round-45/frozen-path-preflight.py\n\n  "
             + HDR.replace("\n", "\n  ") + ("  " + GOOD_ROW) * 8
             + "\n  Refs: " + ", ".join(REFS) + "\n\n")
    plain = "".join(f"- **{i}. Plain {i}.** body\n\n" for i in range(1, n_plain + 1))
    paths = {"SKILL.md": "# SKILL\n\n## Queue-drain craft (fixture)\n\n" + plain + block,
             "tools/round-45/frozen-path-preflight.py": show("tools/round-45/frozen-path-preflight.py"),
             "plans/round-45-claims.md": show("plans/round-45-claims.md")}
    for p in ("corpus/lessons/round-44.md", "corpus/lessons/round-44-verifier-spotcheck.md",
              "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md"):
        paths[p] = show(p)
    for p, t in paths.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        open(full, "w").write(t)
    git(d, "add", "-A"); git(d, "commit", "-q", "-m", "x")
    rev = git(d, "rev-parse", "HEAD").stdout.strip()
    out = os.path.join(S, label + ".json")
    p = subprocess.run([sys.executable, "-I", "-B", os.path.join(L, "tools/round-45/c1-counter.py"),
                        "--root", d, "--freeze", rev, "--rev", rev, "--json-out", out],
                       capture_output=True, text=True, env=dict(os.environ))
    rec = json.load(open(out))
    return dict(label=label, n_plain=n_plain, block_label=block_label, exit=p.returncode,
                rule_blocks=rec.get("rule_blocks"), failing=rec.get("failing"),
                met=rec.get("met_target"), fx=d)


if __name__ == "__main__":
    os.makedirs(os.path.join(S, "fx"), exist_ok=True)
    rows = [build("iso-selftest-relabel-20plain", 20, "20"),
            build("iso-relabel-21plain", 21, "20")]
    json.dump(rows, open(os.path.join(S, "isolation.json"), "w"), indent=1)
    print(json.dumps(rows, indent=1))
