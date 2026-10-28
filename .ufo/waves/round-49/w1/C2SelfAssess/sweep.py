#!/usr/bin/env python3
"""Read-only round-48 self-assessment sweep. Writes only next to this file."""
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
OUT = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/w1/C2SelfAssess")
RECEIPTS = OUT / "receipts"
RECEIPTS.mkdir(parents=True, exist_ok=True)

records = []


def utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(label, argv, cwd=None):
    t = utc()
    p = subprocess.run(argv, cwd=cwd or str(LANE), capture_output=True)
    blob = p.stdout
    rec = {
        "label": label,
        "argv": argv,
        "cwd": str(cwd or LANE),
        "exit": p.returncode,
        "utc": t,
        "stdout_sha256": hashlib.sha256(blob).hexdigest(),
        "stderr_sha256": hashlib.sha256(p.stderr).hexdigest(),
        "stdout_bytes": len(blob),
        "stderr_bytes": len(p.stderr),
    }
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", label)[:80]
    (RECEIPTS / f"{safe}.stdout").write_bytes(blob)
    (RECEIPTS / f"{safe}.stderr").write_bytes(p.stderr)
    (RECEIPTS / f"{safe}.json").write_text(json.dumps(rec, indent=2) + "\n")
    records.append(rec)
    return p


def git(*args):
    return run("git " + " ".join(args[:6]), ["git", "-C", str(LANE), *args])


def show(rev, path):
    p = subprocess.run(["git", "-C", str(LANE), "show", f"{rev}:{path}"], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def main():
    facts = {}
    p = git("rev-parse", "HEAD")
    facts["HEAD"] = p.stdout.decode().strip()
    p = git("rev-parse", "--show-toplevel")
    facts["toplevel"] = p.stdout.decode().strip()
    p = git("status", "--porcelain", "--", "SCORECARD.md", "SHONEN.md", "LOG.md",
            "corpus/QUALITY.md", "corpus/lessons/round-48-verifier-spotcheck.md",
            "SKILL.md", "PROVINCE.md")
    facts["porcelain"] = p.stdout.decode()

    # command A recipe, SCORECARD.md lines 93-123, at three revs
    def command_a(rev):
        t = utc()
        code = r'''
import json, pathlib, re, subprocess, sys
rev = sys.argv[1]
def get(path):
    return subprocess.check_output(["git","-C",sys.argv[2],"show",f"{rev}:{path}"], text=True)
paths = subprocess.check_output(["git","-C",sys.argv[2],"ls-tree","-r","--name-only",rev,"--","corpus/knowledge"], text=True).splitlines()
files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith(".md")}
section = get("corpus/README.md").split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
mapped = set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+", section))
craft = get("SKILL.md").split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
rules = re.split(r"(?m)^- \*\*", craft)[1:]
pattern = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
resolved = 0
unresolved = []
for i, rule in enumerate(rules, 1):
    refs = re.findall(pattern, rule)
    valid = bool(refs)
    why = "no knowledge ref" if not refs else ""
    for name, first, last in refs:
        try:
            count = len(get("corpus/knowledge/" + name).splitlines())
            start, end = int(first or 1), int(last or first or 1)
            if not (1 <= start <= end <= count):
                valid = False
                why = f"{name}:{start}-{end} lines={count}"
        except subprocess.CalledProcessError:
            valid = False
            why = "missing " + name
    resolved += valid
    if not valid:
        title = rule.split("\n", 1)[0][:80]
        unresolved.append({"n": i, "why": why, "title": title})
craft_lines = craft.count("\n") + (0 if craft.endswith("\n") else 1)
print(json.dumps({"revision": rev, "mapped": len(files & mapped),
 "knowledge_files": len(files), "missing": sorted(files - mapped),
 "dangling": sorted(mapped - files), "citation_resolved_rules": resolved,
 "rule_blocks": len(rules), "unresolved": unresolved,
 "craft_chars": len(craft), "coverage_score": round(10*len(files & mapped)/len(files), 2) if files else None,
 "depth_score": round(10*resolved/len(rules), 2) if rules else None}, sort_keys=True))
'''
        argv = ["python3", "-I", "-c", code, rev, str(LANE)]
        p = run(f"command-A {rev[:12]}", argv)
        facts[f"command_a_{rev[:12]}"] = {
            "exit": p.returncode,
            "stdout": p.stdout.decode()[:4000],
        }

    for rev in (
        "e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9",
        "8847042a140b044dbf335210c965bf7b06b09b4f",
        "2e785632863f043a985f7953775b6aca191f1169",
        "52b0eb2907c704ed5f184c47b14c723208e5cbbc",
    ):
        command_a(rev)

    # blob identity of SKILL / SCORECARD / SHONEN / QUALITY / LOG across revs
    revs = ["61b87d742032e65fca9c38267d7d6ed7e555edad",
            "b6f7ca2a6391964dfdedd477cd560bd42159873a",
            "165d45d1",
            "2e785632863f043a985f7953775b6aca191f1169",
            "c093e798106eba7e5372f63108ec32748bdc115f",
            "33f65a913cfd21a4491a4f8b7ccc8f00069f058d",
            "8847042a140b044dbf335210c965bf7b06b09b4f",
            "e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9"]
    p = git("rev-parse", "--verify", *[f"{r}^{{commit}}" for r in (
        "165d45d1", "b6f7ca2a6391964dfdedd477cd560bd42159873a",
        "dc73587a8b9c1a23ba5a91dc7707ac7381a8b873",
        "2e785632863f043a985f7953775b6aca191f1169")])
    facts["rev_parse_selected"] = p.stdout.decode()

    p = git("log", "-1", "--format=%H %ci %s", "165d45d1")
    facts["log_165d45d1"] = p.stdout.decode()
    p = git("log", "-1", "--format=%H %ci %s", "b6f7ca2a6391964dfdedd477cd560bd42159873a")
    facts["log_A8"] = p.stdout.decode()
    p = git("log", "-1", "--format=%H %ci %s", "dc73587a8b9c1a23ba5a91dc7707ac7381a8b873")
    facts["log_A1"] = p.stdout.decode()
    p = git("merge-base", "--is-ancestor", "165d45d1", "b6f7ca2a6391964dfdedd477cd560bd42159873a")
    facts["165_ancestor_of_A8_exit"] = p.returncode
    p = git("merge-base", "--is-ancestor", "b6f7ca2a6391964dfdedd477cd560bd42159873a", "165d45d1")
    facts["A8_ancestor_of_165_exit"] = p.returncode
    p = git("merge-base", "--is-ancestor", "dc73587a8b9c1a23ba5a91dc7707ac7381a8b873", "165d45d1")
    facts["A1_ancestor_of_165_exit"] = p.returncode

    p = git("diff-tree", "--no-commit-id", "--name-only", "-r", "2e785632863f043a985f7953775b6aca191f1169")
    facts["names_2e785632"] = p.stdout.decode()
    p = git("diff-tree", "--no-commit-id", "--name-only", "-r", "c093e798106eba7e5372f63108ec32748bdc115f")
    facts["names_c093e798"] = p.stdout.decode()
    p = git("diff", "--stat", "61b87d742032e65fca9c38267d7d6ed7e555edad", "8847042a140b044dbf335210c965bf7b06b09b4f", "--", "SHONEN.md", "PROVINCE.md")
    facts["diff_shonen_province_r48"] = p.stdout.decode()

    p = git("grep", "-n", "-e", "Row 79 added after round 48", "-e", "^| 79 |", "61b87d742032e65fca9c38267d7d6ed7e555edad", "--", "corpus/QUALITY.md")
    facts["quality_row79_at_base_exit"] = p.returncode
    facts["quality_row79_at_base"] = p.stdout.decode()[:2000]
    p = git("grep", "-n", "score cell", "2e785632863f043a985f7953775b6aca191f1169", "--", "corpus/QUALITY.md")
    facts["quality_score_cell_at_2e78"] = {"exit": p.returncode, "stdout": p.stdout.decode()[:2000]}

    # citation_resolved_rules in the cited receipt dir
    p = run("grep citation_resolved scores", ["grep", "-R", "-n", "citation_resolved_rules",
            str(LANE / ".ufo/waves/round-48/l1/scores")])
    facts["citation_in_scores"] = {"exit": p.returncode, "stdout": p.stdout.decode()[:2000]}

    # axis score cells
    rec_path = LANE / ".ufo/waves/round-48/l1/scores/c2-final-33f65a91.json"
    d = json.loads(rec_path.read_text())
    facts["c2_axis_keys"] = sorted(d["axis_score_cells"])
    facts["c2_axes_atoms"] = d["axes_atoms"]
    facts["c2_bad"] = d["axis_score_bad"]
    c1 = json.loads((LANE / ".ufo/waves/round-48/l1/scores/c1-final-33f65a91.json").read_text())
    c1e = json.loads((LANE / ".ufo/waves/round-48/l1/scores/c1-at-2e785632.json").read_text())
    facts["c1_final_headline"] = {k: c1[k] for k in (
        "rule_blocks", "registry_rows", "census_paths", "meaning_rows_failed", "rows", "failing")}
    facts["c1_final_battery"] = {k: c1["battery"][k] for k in (
        "forgeries_total", "v2_green", "v3_green", "genuine_green", "crash")}
    facts["c1_2e78_headline"] = {k: c1e[k] for k in (
        "rule_blocks", "registry_rows", "census_paths", "meaning_rows_failed", "rows", "failing", "rev")}
    facts["c1_2e78_battery"] = {k: c1e["battery"][k] for k in (
        "forgeries_total", "v2_green", "v3_green", "genuine_green", "crash")}
    facts["c1_has_citation_resolved"] = "citation_resolved_rules" in c1

    # wave accounting
    results = json.loads((LANE / ".ufo/waves/round-48/r48-w1-results.json").read_text())
    names = [x["name"] for x in results["results"]]
    roles = {}
    for x in results["results"]:
        roles[x.get("agent")] = roles.get(x.get("agent"), 0) + 1
    tree = subprocess.run(["git", "-C", str(LANE), "ls-tree", "-r", "--name-only", "HEAD", "--",
                           ".ufo/waves/round-48/w1"], capture_output=True).stdout.decode().splitlines()
    missing = []
    present = []
    for n in names:
        has = (f".ufo/waves/round-48/w1/{n}.md" in tree) or any(
            p.startswith(f".ufo/waves/round-48/w1/{n}/") and p.endswith(".md") for p in tree)
        (present if has else missing).append(n)
    facts["wave"] = {
        "file_seats": results.get("seats"),
        "results_len": len(names),
        "dup_names": sorted({n for n in names if names.count(n) > 1}),
        "roles": roles,
        "role_sum": sum(roles.values()),
        "attack": roles.get("reviewer", 0) + roles.get("critic", 0) + roles.get("mutation-tester", 0),
        "missing_reports": missing,
        "report_count": len(present),
        "planner_in_roles": roles.get("planner", 0),
        "top_keys": sorted(results.keys()),
        "result_keys": sorted(results["results"][0].keys()),
    }
    # blocked / cancel / freeze hashes inside outputs
    freezes = {}
    blocked = []
    cancel_hits = []
    for x in results["results"]:
        text = x.get("output") or ""
        if '"status": "blocked"' in text or '"status":"blocked"' in text:
            blocked.append(x["name"])
        if re.search(r"cancel", text, re.I):
            cancel_hits.append(x["name"])
        for h in ("dc73587a", "ac02a79f", "f3a7afc4", "0f06251b", "04f9d4b7",
                  "24b4e5cb", "c8d7da55", "b6f7ca2a"):
            if h in text:
                freezes.setdefault(h, []).append(x["name"])
    facts["blocked_status"] = blocked
    facts["cancel_names"] = cancel_hits
    facts["freeze_prefix_seats"] = {k: v for k, v in freezes.items()}
    # C1Meaning / C2Floor / C1Battery / Scribe snippets
    want = {"C1Meaning", "C2Floor", "C1Battery", "ScribeReportNumbers", "C1Battery-2"}
    snippets = {}
    for x in results["results"]:
        if x["name"] in want:
            snippets[x["name"]] = (x.get("output") or "")[:500]
    facts["snippets"] = snippets
    facts["names_has_C1Battery-2"] = "C1Battery-2" in names

    dispatch = json.loads((LANE / ".ufo/waves/round-48/w1-dispatch.json").read_text())
    facts["dispatch_counts"] = dispatch.get("counts")
    facts["dispatch_wave"] = dispatch.get("wave")
    facts["dispatch_schema"] = dispatch.get("schema")
    droles = {}
    for name, mem in dispatch.get("registry", {}).get("members", {}).items():
        droles[mem.get("role")] = droles.get(mem.get("role"), 0) + 1
    facts["dispatch_roles"] = droles
    facts["dispatch_members"] = len(dispatch.get("registry", {}).get("members", {}))

    # other dispatch / w2
    p = run("glob round-48 dispatch and w2", ["bash", "-c",
            "ls -1 .ufo/waves/round-48 | sort"])
    facts["round48_top"] = p.stdout.decode()

    # line quotes
    needles = {
        "scorecard_quality": ("SCORECARD.md", "quality **improved on the instruments**, bounded by"),
        "scorecard_calib_cell": ("SCORECARD.md", "outside closures: round 24 rejected-honest-stop, round 25 admitted"),
        "scorecard_depth_25": ("SCORECARD.md", "citation_resolved_rules 25"),
        "scorecard_lastchange_depth": ("SCORECARD.md", "count refreshed rounds 25, 26, 39 and 40"),
        "scorecard_noclaim": ("SCORECARD.md", "No claim data had been scored before the amendments"),
        "scorecard_a1_only": ("SCORECARD.md", "those seats saw A1 bytes only"),
        "scorecard_waves": ("SCORECARD.md", "Waves: 75 + 0 = 75 seats"),
        "scorecard_calib_10": ("SCORECARD.md", "calibration `10 → 10`"),
        "log_dead": ("LOG.md", "0 dead seats, 0 residual calls"),
        "log_73": ("LOG.md", "73 seats produced reports"),
        "log_row79": ("LOG.md", "QUALITY row 79 records the rule"),
        "log_landed": ("LOG.md", "QUALITY row 79 and settled wave evidence"),
        "log_depth": ("LOG.md", "Owned-axes depth fraction is now 25/25"),
        "shonen_21": ("SHONEN.md", "command A stays 21/21"),
        "shonen_20": ("SHONEN.md", "20/20 rule blocks"),
        "closure_rej": ("corpus/lessons/round-48-verifier-spotcheck.md", "Admission: **rejected-harmed**"),
        "closure_cal": ("corpus/lessons/round-48-verifier-spotcheck.md", "| calibration | harmed |"),
        "closure_qual": ("corpus/lessons/round-48-verifier-spotcheck.md", "**quality — harmed.**"),
        "closure_dead": ("corpus/lessons/round-48-verifier-spotcheck.md", "0 dead seats"),
        "quality_table79": ("corpus/QUALITY.md", "| 79 | A claim's rule is the bytes of its **first** freeze commit."),
        "quality_prose79": ("corpus/QUALITY.md", "Row 79 added after round 48"),
        "record2_regex": ("tools/round-48/record2.py", "AXIS_SCORE = re.compile"),
    }
    lines = {}
    for key, (path, needle) in needles.items():
        text = (LANE / path).read_text(errors="replace").splitlines()
        hits = [i + 1 for i, line in enumerate(text) if needle in line]
        lines[key] = hits
    facts["lines"] = lines

    # round-47 section seat total
    sc = (LANE / "SCORECARD.md").read_text()
    r47 = sc.split("## Round 47", 1)[1].split("\n## Round 48", 1)[0]
    facts["r47_seat_lines"] = [ln for ln in r47.splitlines() if re.search(r"seat", ln, re.I)][:30]
    facts["r47_has_waves_formula"] = "Waves:" in r47

    # 50 atoms
    facts["line_3709"] = sc.splitlines()[3708]

    # SHONEN round-48 tokens
    sh = (LANE / "SHONEN.md").read_text()
    facts["shonen_lines"] = sh.count("\n") + 1
    facts["shonen_round48_hits"] = [i + 1 for i, ln in enumerate(sh.splitlines())
                                    if re.search(r"round 48|round-48|block 25|25/25|33f65a91", ln, re.I)]

    # PROVINCE cited lines
    prov = (LANE / "PROVINCE.md").read_text().splitlines()
    picks = [97, 110, 116, 119, 125, 157, 376, 378, 382, 384, 386, 394]
    facts["province_picks"] = {str(n): (prov[n - 1][:180] if n <= len(prov) else "OUT OF RANGE") for n in picks}
    facts["province_len"] = len(prov)

    # craft section end at HEAD: line of "## Config custody"
    skill = (LANE / "SKILL.md").read_text().splitlines()
    facts["skill_craft_heading"] = next(i + 1 for i, ln in enumerate(skill) if ln.startswith("## Queue-drain craft"))
    facts["skill_after_craft"] = next(i + 1 for i, ln in enumerate(skill) if ln.startswith("## ") and i > facts["skill_craft_heading"])
    # historical craft end at 52b0eb29
    old = show("52b0eb2907c704ed5f184c47b14c723208e5cbbc", "SKILL.md")
    if old:
        ol = old.decode().splitlines()
        h = next(i + 1 for i, ln in enumerate(ol) if ln.startswith("## Queue-drain craft"))
        a = next(i + 1 for i, ln in enumerate(ol) if ln.startswith("## ") and i + 1 > h)
        facts["skill_craft_at_52b0eb29"] = {"heading": h, "next_section": a, "last_craft_line": a - 1}

    # owned-axes depth row columns
    for i, ln in enumerate(sc.splitlines(), 1):
        if ln.startswith("| depth |") and "25/25" in ln:
            cells = [c.strip() for c in ln.strip().split("|")]
            facts["depth_row_line"] = i
            facts["depth_ncols"] = len(cells)
            facts["depth_score_cell"] = cells[2][:80] if len(cells) > 2 else ""
            facts["depth_last"] = cells[-2][:400] if len(cells) > 2 else ""
            facts["depth_evidence_tail"] = cells[4][-500:] if len(cells) > 5 else ""
            break
    for i, ln in enumerate(sc.splitlines(), 1):
        if ln.startswith("| calibration |") and "self-assessment mismatches" in ln:
            cells = [c.strip() for c in ln.strip().split("|")]
            facts["cal_row_line"] = i
            facts["cal_last"] = cells[-2][:500] if len(cells) > 2 else ""
            break
    for i, ln in enumerate(sc.splitlines(), 1):
        if ln.startswith("| coverage |") and "138/138" in ln:
            cells = [c.strip() for c in ln.strip().split("|")]
            facts["cov_row_line"] = i
            facts["cov_last"] = cells[-2][:400] if len(cells) > 2 else ""
            break

    # dead hash vs real, for context only (A2) — confirm not re-reported as new
    p = git("cat-file", "-e", "663f30ee7516942a0120e7de68fe88356e680822^{commit}")
    facts["dead_hash_exit"] = p.returncode
    p = git("cat-file", "-e", "663f30ee751694fb0970e7de68fe88356e680822^{commit}")
    facts["real_hash_exit"] = p.returncode

    # knowledge count at r48 tip and base
    for rev, tag in (("61b87d742032e65fca9c38267d7d6ed7e555edad", "base"),
                     ("8847042a140b044dbf335210c965bf7b06b09b4f", "tip")):
        p = git("ls-tree", "-r", "--name-only", rev, "--", "corpus/knowledge")
        n = sum(1 for ln in p.stdout.decode().splitlines() if ln.endswith(".md"))
        facts[f"knowledge_md_{tag}"] = n

    # does LOG name 577a02a5 / 8847042a (A3, exclusion)
    log = (LANE / "LOG.md").read_text()
    facts["log_names_577"] = "577a02a5" in log
    facts["log_names_8847"] = "8847042a" in log

    # c2-at-165 exit fields
    early = json.loads((LANE / ".ufo/waves/round-48/l1/scores/c2-at-165d45d1.json").read_text())
    facts["c2_165"] = {"failing": early.get("failing"), "met_target": early.get("met_target"),
                       "rev": early.get("rev")}
    early1 = json.loads((LANE / ".ufo/waves/round-48/l1/scores/c1-at-165d45d1.json").read_text())
    facts["c1_165"] = {"failing": early1.get("failing"), "met_target": early1.get("met_target"),
                       "rule_blocks": early1.get("rule_blocks"), "rev": early1.get("rev")}

    # when were the 165 receipts committed
    p = git("log", "-1", "--format=%H %ci %s", "--", ".ufo/waves/round-48/l1/scores/c1-at-165d45d1.json")
    facts["commit_of_165_receipt"] = p.stdout.decode()

    outp = OUT / "facts.json"
    outp.write_text(json.dumps({"facts": facts, "receipts": records}, indent=2) + "\n")
    print(outp)
    print("records", len(records))


if __name__ == "__main__":
    main()
