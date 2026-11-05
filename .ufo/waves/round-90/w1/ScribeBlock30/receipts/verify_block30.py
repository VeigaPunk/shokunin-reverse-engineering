#!/usr/bin/env python3
# ScribeBlock30 verification driver: scratch-only clone of the lane at base fc52cc9dc.
import json, os, re, shutil, subprocess, sys

S = "/fast/scratch/hyaku/kaidoku-r90/ScribeBlock30"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SEAT = f"{LANE}/.ufo/waves/round-90/w1/ScribeBlock30"
REC = f"{SEAT}/receipts"
BASE = "fc52cc9dc"
COUNTER = f"{LANE}/tools/round-89/depth-blocks-v2.py"
REPO = f"{S}/repo"
ID = ["-c", "user.name=scribe30", "-c", "user.email=scribe30@scratch.local"]

os.makedirs(REC, exist_ok=True)
summary = []


def run(args, cwd=None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def git(*a):
    rc, out, err = run(["git", "-C", REPO, *a])
    if rc != 0:
        raise SystemExit(f"git {a} rc={rc} {err}")
    return out


def gitv(*a):
    return git(*a).strip()


# 1. scratch clone of the lane (source is only read)
if os.path.exists(REPO):
    shutil.rmtree(REPO)
rc, _, err = run(["git", "clone", "-q", LANE, REPO])
assert rc == 0, err
top = gitv("rev-parse", "--show-toplevel")
assert top == REPO, f"toplevel {top} != {REPO}"
git("checkout", "-q", "--detach", BASE)
base_skill = git("show", f"{BASE}:SKILL.md")  # raw, keeps the final newline
block = open(f"{SEAT}/block-30.md", encoding="utf-8").read()
summary.append(f"clone toplevel {top}; detached at {BASE}")
open(os.path.join(S, "base-skill-raw-tail.txt"), "w").write(repr(base_skill[-40:]))

ANCHOR = "\n## Config custody for live-probe rounds"
assert base_skill.count(ANCHOR) == 1


def skill_with(new_block):
    idx = base_skill.index(ANCHOR)
    return base_skill[:idx] + "\n" + new_block + base_skill[idx:]


def commit(text, label):
    with open(f"{REPO}/SKILL.md", "w", encoding="utf-8") as fh:
        fh.write(text)
    git("add", "SKILL.md")
    git(*ID, "commit", "-q", "-m", f"scratch variant {label}")
    return gitv("rev-parse", "HEAD")


def count(rev, expect, label):
    out = f"{REC}/counter-{label}.json"
    rc, so, se = run(["python3", "-I", "-B", COUNTER, "--root", REPO, "--rev", rev,
                      "--expect-blocks", str(expect), "--json-out", out])
    line = so.strip() or se.strip()
    summary.append(f"[{label}] rev={rev[:12]} expect={expect}: {line} (process rc={rc})")
    return rc, line


# 2. candidate and base arms
cand_sha = commit(skill_with(block), "candidate-block30")
results = {}
results["base_expect29"] = count(BASE, 29, "base-expect29")
results["base_expect30"] = count(BASE, 30, "base-expect30")
results["cand_expect30"] = count(cand_sha, 30, "cand-expect30")
results["cand_expect29"] = count(cand_sha, 29, "cand-expect29")

# 3. selftest of the frozen counter (read-only use of the lane file)
rc, so, se = run(["python3", "-I", "-B", COUNTER, "--selftest"])
open(f"{REC}/counter-selftest.txt", "w").write(so + se)
summary.append(f"[selftest] {so.strip()} (rc={rc})")

# 4. red worlds: each must be refused by the counter or by the base-presence gate
def variant(label, text, expect=30):
    sha = commit(text, label)
    return count(sha, expect, label)


stub = "- **30. stub.** corpus/knowledge/2026-11-04-r89-binfo-field-value-class.md:59-61 `x`\n"
results["red_stub"] = variant("red-stub-as-block30", skill_with(stub))
absent = block.replace("QUALITY 157 |", "QUALITY 157; `corpus/knowledge/2026-11-04-r90-missing.md:1-3` |", 1)
results["red_absent_knowledge"] = variant("red-absent-knowledge", skill_with(absent))
rng = block.replace("QUALITY 171;", "QUALITY 171; `corpus/knowledge/2026-11-04-r89-binfo-field-value-class.md:900-910`;", 1)
results["red_range"] = variant("red-range", skill_with(rng))
# gap probes: the counter passes these, the base-presence gate must refuse them
lesson = block.replace("QUALITY 159 |", "QUALITY 159; `corpus/lessons/round-89.md` |", 1)
results["gap_lesson_citation"] = variant("gap-lesson-citation", skill_with(lesson))
r90 = block.replace("QUALITY 146 |", "QUALITY 146; `tools/round-90/upx-break-repair.py` |", 1)
results["gap_round90_path"] = variant("gap-round90-path", skill_with(r90))
q999 = block.replace("QUALITY 146 |", "QUALITY 999 |", 1)
results["gap_quality_999"] = variant("gap-quality-999", skill_with(q999))
# restore candidate as HEAD of the scratch clone
git("checkout", "-q", "--detach", cand_sha)
assert gitv("rev-parse", "HEAD") == cand_sha

# 5. base-presence gate, the check the counter does not perform
base_q = git("show", f"{BASE}:corpus/QUALITY.md")
row_nums = set(int(m) for m in re.findall(r"^- \*\*Row (\d+) \(", base_q, re.M))


def gate(text, label):
    blk = text[text.index("- **30. "):text.index("\n## Config custody")]
    paths = set()
    for m in re.findall(r"(?<![\w/.\-])((?:corpus|tools|plans|\.ufo)/[\w.\-/]+)", blk):
        paths.add(re.sub(r":\d+(-\d+)?$", "", m.rstrip(".,;)")))
    missing_paths = []
    for p in sorted(paths):
        rc, _, _ = run(["git", "-C", REPO, "cat-file", "-e", f"{BASE}:{p}"])
        if rc != 0:
            missing_paths.append(p)
    cited = set(int(n) for n in re.findall(r"QUALITY (\d+)", blk))
    for lo, hi in re.findall(r"QUALITY (\d+)-(\d+)", blk):
        cited |= set(range(int(lo), int(hi) + 1))
    for grp in re.findall(r"rows ([\d,\- ]+)\(base", blk):
        for part in grp.split(","):
            part = part.strip()
            if "-" in part:
                lo, hi = part.split("-")
                cited |= set(range(int(lo), int(hi) + 1))
            elif part.isdigit():
                cited.add(int(part))
    missing_rows = sorted(n for n in cited if n not in row_nums)
    words = len(blk.split())
    spans = len(re.findall(r"`[^`\n]+`", blk))
    ranges = []
    for name, a, b in re.findall(r"corpus/knowledge/([a-z0-9-]+\.md):(\d+)-(\d+)", blk):
        kp = f"corpus/knowledge/{name}"
        n = len(git("show", f"{BASE}:{kp}").splitlines())
        ok = 1 <= int(a) <= int(b) <= n
        ranges.append({"path": kp, "range": f"{a}-{b}", "lines_at_base": n, "in_range": ok})
    verdict = not missing_paths and not missing_rows and all(r["in_range"] for r in ranges)
    return {"label": label, "words": words, "spans": spans, "paths_checked": sorted(paths),
            "missing_paths_at_base": missing_paths, "quality_rows_cited": sorted(cited),
            "missing_quality_rows": missing_rows, "knowledge_ranges": ranges,
            "base_presence_pass": verdict}


gates = {"candidate": gate(skill_with(block), "candidate"),
         "gap_lesson_citation": gate(skill_with(lesson), "gap_lesson_citation"),
         "gap_round90_path": gate(skill_with(r90), "gap_round90_path"),
         "gap_quality_999": gate(skill_with(q999), "gap_quality_999")}
json.dump({"counter": {k: {"rc": v[0], "line": v[1]} for k, v in results.items()},
           "gate": gates}, open(f"{REC}/verify-block30.json", "w"), indent=1, sort_keys=True)
for k, g in gates.items():
    summary.append(f"[gate {k}] words={g['words']} spans={g['spans']} base_presence_pass={g['base_presence_pass']} "
                   f"missing_paths={g['missing_paths_at_base']} missing_rows={g['missing_quality_rows']}")
open(f"{REC}/verify-summary.txt", "w").write("\n".join(summary) + "\n")
print("\n".join(summary))
print("candidate sha", cand_sha)
