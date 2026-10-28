#!/usr/bin/env python3
"""R45 W2 seat R45W2MutC1Landing: mutate the LANDING (SKILL.md block 22 at f59565b7)
and score each mutant with the frozen c1-counter. Read-only on the lane: every
mutation is applied to a copy under this seat's scratch.

Shape per mutant:
  fx/<name>/            full tree of the lane at f59565b7 (git archive), git-init'd
  commit "freeze"       F0  (pristine, or carrying a broken interpreter for m6)
  commit "mutant"       R   (mutated SKILL.md, or absent when rev==freeze)
  c1-counter.py --root fx/<name> --freeze F0 --rev R
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "f59565b782c18b0eb691bec12f52d2f80d9f5032"
COUNTER = os.path.join(LANE, "tools/round-45/c1-counter.py")
S = "/fast/scratch/hyaku/kaidoku-r45/R45W2MutC1Landing"
REPORT = os.path.join(LANE, ".ufo/waves/round-45/w2/R45W2MutC1Landing")
MARKER = "<!-- freeze-integrity-table v1 -->"
PRE = "tools/round-45/frozen-path-preflight.py"


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


NEEDED = [
    "SKILL.md",
    PRE,
    "plans/round-45-claims.md",
    "corpus/lessons/round-44.md",
    "corpus/lessons/round-44-verifier-spotcheck.md",
    "corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md",
    "corpus/lessons/round-45.md",
]


def base_tree():
    """Real bytes at REV for every path the counter reads: SKILL.md, the interpreter,
    the claims file, and the four files block 22 cites (so line counts are the
    landing's). Nothing else: the fixture is the counter's own make_repo shape."""
    d = os.path.join(S, "base")
    if not os.path.isdir(d):
        for p in NEEDED:
            full = os.path.join(d, p)
            os.makedirs(os.path.dirname(full) or d, exist_ok=True)
            with open(full, "wb") as fh:
                r = subprocess.run(["git", "-C", LANE, "show", f"{REV}:{p}"], stdout=fh)
                assert r.returncode == 0, p
    return d


def new_fixture(name):
    d = os.path.join(S, "fixtures", name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    shutil.copytree(base_tree(), d, symlinks=True)
    return d


def git_init(d):
    sh(["git", "-C", d, "init", "-q"])
    sh(["git", "-C", d, "config", "user.email", "mut@r45"])
    sh(["git", "-C", d, "config", "user.name", "r45 mutant"])
    top = sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)


FIXED_DATE = "2026-10-28T16:00:00+0000"


def commit(d, msg):
    """Deterministic commit ids so a re-run reproduces the same receipt bytes."""
    env = dict(os.environ, GIT_AUTHOR_DATE=FIXED_DATE, GIT_COMMITTER_DATE=FIXED_DATE)
    sh(["git", "-C", d, "add", "-A"])
    r = sh(["git", "-C", d, "commit", "-q", "-m", msg], env=env)
    assert r.returncode == 0, r.stderr
    return sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()


# --- mutations on SKILL.md (block 22 lives inside it) -----------------------

def rd(d, path):
    with open(os.path.join(d, path)) as fh:
        return fh.read()


def wr(d, path, text):
    with open(os.path.join(d, path), "w") as fh:
        fh.write(text)


def m1(skill):                       # delete the marker LINE and nothing else
    lines = skill.splitlines(keepends=True)
    hits = [i for i, l in enumerate(lines) if MARKER in l]
    assert len(hits) == 1 and lines[hits[0]].strip() == MARKER
    del lines[hits[0]]
    return "".join(lines)


def table_rows(skill):
    """Line indices of the block-22 table only: header row onward, contiguous."""
    lines = skill.splitlines(keepends=True)
    start = next(i for i, l in enumerate(lines)
                 if l.strip() == "| trigger | arm | exit | receipt |")
    idx = []
    for i in range(start, len(lines)):
        if not lines[i].strip().startswith("|"):
            break
        idx.append(i)
    return idx


def m2(skill):                       # 10 data rows -> 7 (drop the last three)
    lines = skill.splitlines(keepends=True)
    idx = table_rows(skill)[2:]      # skip header + separator
    assert len(idx) == 10, len(idx)
    for i in sorted(idx[-3:], reverse=True):
        del lines[i]
    return "".join(lines)


def m3(skill):                       # one exit cell -> 3
    lines = skill.splitlines(keepends=True)
    for i, l in enumerate(lines):
        if l.strip().startswith("|") and "uncovered_frozen_dirs" in l:
            cells = l.split("|")
            assert cells[3].strip() == "2", cells
            cells[3] = " 3 "
            lines[i] = "|".join(cells)
            return "".join(lines)
    raise AssertionError("pathspec row not found")


def m3b(skill):                      # one exit cell -> another LEGAL value (2 where the arm returns 1)
    lines = skill.splitlines(keepends=True)
    for i, l in enumerate(lines):
        if l.strip().startswith("|") and "one record per path with commit and status" in l:
            cells = l.split("|")
            assert cells[3].strip() == "1", cells
            cells[3] = " 2 "
            lines[i] = "|".join(cells)
            return "".join(lines)
    raise AssertionError("touched row not found")


def m4(skill):                       # one citation one line PAST the file's end
    old = "corpus/lessons/round-45.md:12-17"
    lines = len(rd(os.path.join(S, "base"), "corpus/lessons/round-45.md").splitlines())
    assert old in skill
    return skill.replace(old, f"corpus/lessons/round-45.md:12-{lines + 1}")


def m4b(skill):                      # one citation past end of a file OUTSIDE the validated path set
    old = "`corpus/lessons/round-45.md:12-17`"
    assert old in skill
    return skill.replace(old, "`LOG.md:99999`")


def block22_span(skill):
    """(start, end) of the whole `- **22.` block, which is what the counter reads."""
    mk = skill.index(MARKER)
    start = skill.rindex("\n- **", 0, mk) + 1
    cands = [x for x in (skill.find("\n- **", mk), skill.find("\n## ", mk)) if x != -1]
    return start, min(cands)


def m5(skill):                       # remove the S140 token from block 22
    a, b = block22_span(skill)
    block = skill[a:b]
    assert block.count("S140") == 2, block.count("S140")
    return skill[:a] + block.replace("S140", "") + skill[b:]


def m7(skill):                       # keep 10 rows, but make them structurally valid junk
    lines = skill.splitlines(keepends=True)
    idx = table_rows(skill)[2:]
    junk = "| zzz | yyy | 1 | www |\n"
    for i in sorted(idx, reverse=True):
        lines[i] = junk
    return "".join(lines)





def m1b(skill):                      # a SECOND marker inside block 21 (clause 2 from above)
    sec = skill.index("## Queue-drain craft ")
    pos = [i for i in range(sec, len(skill)) if skill.startswith("\n- **", i)]
    start = pos[20] + 1              # 21st block bullet
    nl = skill.index("\n", start) + 1
    return skill[:nl] + "  " + MARKER + "\n" + skill[nl:]


def m4c(skill):                      # in-range citation moved to a file that does not support it
    old = "corpus/lessons/round-44.md:18-19"
    a, b = block22_span(skill)
    assert skill[a:b].count(old) == 1
    return skill[:a] + skill[a:b].replace(old, "corpus/lessons/round-45.md:1-2") + skill[b:]


def m8(skill):                       # a 23rd rule block in the section (clause 1 from above)
    sec = skill.index("## Queue-drain craft ")
    end = skill.index("\n## ", sec)
    return skill[:end] + "\n- **23. Extra rule.** body\n" + skill[end:]


def run_counter(d, freeze, rev, tag):
    out = os.path.join(REPORT, f"counter-{tag}.json")
    env = dict(os.environ, TMPDIR=os.path.join(S, "tmp"), HYAKU_SCRATCH=os.path.join(S, "tmp"))
    os.makedirs(env["TMPDIR"], exist_ok=True)
    t = utc()
    p = subprocess.run([sys.executable, "-I", "-B", COUNTER, "--root", d,
                        "--freeze", freeze, "--rev", rev, "--json-out", out],
                       capture_output=True, text=True, env=env, timeout=600)
    rec = {"tag": tag, "utc": t, "cmd": f"python3 -I -B {COUNTER} --root {d} "
           f"--freeze {freeze} --rev {rev} --json-out {out}",
           "exit": p.returncode, "stdout_sha256": sha(p.stdout),
           "stdout_head": p.stdout[:1200], "stderr": p.stderr[-500:]}
    try:
        rec["receipt"] = json.loads(p.stdout)
    except Exception:
        rec["receipt"] = None
    return rec


def lane_baseline():
    rec = run_counter(LANE, "f762b7273e3f6ca3c710bb37d5de92a4a4417aec", REV, "baseline-lane")
    return rec


MUTATIONS = {"m1": m1, "m1b": m1b, "m2": m2, "m3": m3, "m3b": m3b, "m4": m4,
             "m4b": m4b, "m4c": m4c, "m5": m5, "m7": m7, "m8": m8}


def main():
    os.makedirs(REPORT, exist_ok=True)
    recs = [lane_baseline()]
    for name, fn in MUTATIONS.items():
        d = new_fixture(name)
        git_init(d)
        f0 = commit(d, "freeze")
        before = rd(d, "SKILL.md")
        after = fn(before)
        assert after != before, name
        wr(d, "SKILL.md", after)
        r = commit(d, "mutant")
        rec = run_counter(d, f0, r, name)
        rec.update({"file": "SKILL.md", "sha_before": sha(before), "sha_after": sha(after),
                    "fixture_bytes": len(after)})
        recs.append(rec)
        print(name, rec["exit"], (rec["receipt"] or {}).get("failing"))

    # --- m6 family: the interpreter, not SKILL.md ---------------------------
    pre = rd(os.path.join(S, "base"), PRE)
    dirty_arm = """    dirty = []
    if check_dirty:
        scope_paths = dirty_pathspecs or pathspecs
        dscope = ["--"] + scope_paths if scope_paths else []
        st = git(root, "status", "--porcelain", "-z", *dscope)
        if st.returncode != 0:
            return 2, {"reason": "git status failed"}
        dirty = [e for e in st.stdout.split("\\x00") if e.strip()]
"""
    broken = pre.replace(dirty_arm, "    dirty = []\n")
    assert broken != pre and broken.count("dirty = []") == 1
    stub = ("#!/usr/bin/env python3\nimport sys\n"
            "print('PREFLIGHT_SELFTEST: cases=11 failures=0')\nsys.exit(0)\n")
    for tag, body, placement in (("m6a-freeze-broken-arm", broken, "freeze"),
                                 ("m6b-postfreeze-touch", broken, "rev"),
                                 ("m6c-stub-interpreter", stub, "freeze")):
        d = new_fixture(tag)
        git_init(d)
        if placement == "freeze":
            w = body
        else:
            w = pre
        wr(d, PRE, w)
        f0 = commit(d, "freeze")
        if placement == "rev":
            wr(d, PRE, body)
            r = commit(d, "mutant: interpreter broken after freeze")
        else:
            r = f0
        rec = run_counter(d, f0, r, tag)
        rec.update({"file": PRE, "sha_before": sha(pre), "sha_after": sha(body),
                    "placement": placement})
        recs.append(rec)
        print(tag, rec["exit"], (rec["receipt"] or {}).get("failing"),
              (rec["receipt"] or {}).get("reason"))

    with open(os.path.join(REPORT, "receipts.json"), "w") as fh:
        json.dump(recs, fh, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
