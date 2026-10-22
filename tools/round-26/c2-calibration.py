#!/usr/bin/env python3
"""Round 26 C2 calibration counting instrument.

Counts mismatches between six fixed self-assessment items (K1-K6) and the
observed repository state at one revision.  The frozen rules live in
.ufo/waves/round-26/claims.json (R26-C2 -> rules); this script implements them
and re-defines nothing.

  K1  depth row: the first N/M token in the observable cell has
      N == M == command A rule_blocks == citation_resolved_rules at REV.
  K2  depth row: the evidence cell contains the string SKILL.md:H-L for the
      craft span at REV (H = line of '## Queue-drain craft', L = last non-blank
      line before the next line starting with '## ').
  K3  depth row: the first 7-40 hex revision following the word 'measured' in
      the evidence cell resolves, and command A at that revision gives
      rule_blocks == citation_resolved_rules == the K1 N.
  K4  coverage row: the first N/M token in the observable cell has
      N == M == command A mapped == knowledge_files at REV, and the first
      7-40 hex revision following 'measured' in the evidence cell resolves and
      gives the same N/M under command A.
  K5  calibration row: the first 7-40 hex revision following 'measured' in the
      evidence cell is a prefix of measured_revision in
      evidence/round-1-2026-10-15/result.json at REV.
  K6  SHONEN.md: the line after the box line '- [~] No cross-domain bleed'
      (or '- [x] ...') does not contain the word 'contested', and every
      PROVINCE.md:A-B or PROVINCE.md:A pointer in it is inside PROVINCE.md's
      line count at REV.

Row scope: only lines starting with '| depth |', '| coverage |' or
'| calibration |' inside the SCORECARD.md section that begins at the heading
'## Owned axes' and ends before the next line starting with '## '.  Cells split
on ' | '; column 3 is the observable cell, column 4 the evidence cell.

Command A is the SCORECARD.md '## Measurement recipes' recipe A, ported to read
Git objects of the named revision through --root instead of the working tree.

Usage:
  python3 -I -B c2-calibration.py --root <LANE> --rev <REV>
  python3 -I -B c2-calibration.py --selftest

Exit: 0 iff mismatches == 0, 1 when any item mismatches, 2 on input error.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

INSTRUMENT = "tools/round-26/c2-calibration.py"
RESULT_JSON = "evidence/round-1-2026-10-15/result.json"
AXES = ("depth", "coverage", "calibration")
HEXRUN = re.compile(r"[0-9a-fA-F]+")
NM = re.compile(r"(\d+)\s*/\s*(\d+)")
MEASURED = re.compile(r"\bmeasured\b")
PROVINCE_PTR = re.compile(r"PROVINCE\.md:(\d+)(?:-(\d+))?")


class InputError(Exception):
    """A required Git object or revision could not be read."""


# ---------------------------------------------------------------- git access

def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["LC_ALL"] = "C"
    return env


def git(root, *args):
    return subprocess.run(["git", "-C", root, "--no-replace-objects", *args],
                          capture_output=True, text=True, env=git_env())


def git_ok(root, *args):
    p = git(root, *args)
    if p.returncode != 0:
        raise InputError("git %s failed: %s" % (" ".join(args), p.stderr.strip()))
    return p.stdout


def resolve_rev(root, rev):
    p = git(root, "rev-parse", "--verify", "%s^{commit}" % rev)
    if p.returncode != 0:
        raise InputError("bad_rev")
    return p.stdout.strip()


def blob(root, rev, path):
    p = git(root, "cat-file", "blob", "%s:%s" % (rev, path))
    if p.returncode != 0:
        raise InputError("missing_blob:%s" % path)
    return p.stdout


def blob_lines(root, rev, path):
    return blob(root, rev, path).splitlines()


# ---------------------------------------------------------------- command A

def command_a(root, rev):
    """Port of SCORECARD.md '## Measurement recipes' recipe A on Git objects."""
    paths = git_ok(root, "ls-tree", "-r", "--name-only", rev, "--",
                   "corpus/knowledge").splitlines()
    files = set()
    for p in paths:
        if p.endswith(".md"):
            files.add(p.rsplit("/", 1)[-1][:-3])  # PurePosixPath(p).stem
    readme = blob(root, rev, "corpus/README.md")
    if "## Coverage map\n" not in readme:
        raise InputError("no_coverage_map:corpus/README.md")
    section = readme.split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
    mapped = set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+", section))
    skill = blob(root, rev, "SKILL.md")
    if "## Queue-drain craft " not in skill:
        raise InputError("no_craft_section:SKILL.md")
    craft = skill.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    rules = re.split(r"(?m)^- \*\*", craft)[1:]
    pattern = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
    resolved = 0
    for rule in rules:
        refs = re.findall(pattern, rule)
        valid = bool(refs)
        for name, first, last in refs:
            try:
                count = len(blob_lines(root, rev, "corpus/knowledge/" + name))
            except InputError:
                valid = False
                continue
            start = int(first or 1)
            end = int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        resolved += 1 if valid else 0
    return {
        "revision": rev,
        "mapped": len(files & mapped),
        "knowledge_files": len(files),
        "missing": sorted(files - mapped),
        "dangling": sorted(mapped - files),
        "citation_resolved_rules": resolved,
        "rule_blocks": len(rules),
        "coverage_score": round(10 * len(files & mapped) / len(files), 2) if files else 0.0,
        "depth_score": round(10 * resolved / len(rules), 2) if rules else 0.0,
    }


# ---------------------------------------------------------------- card parsing

def owned_axes_rows(scorecard_text):
    """Return {axis: {'observable': str, 'evidence': str}} for the rows that
    live inside the '## Owned axes' section only."""
    lines = scorecard_text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith("## Owned axes"):
            start = i
            break
    if start is None:
        return {}
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    rows = {}
    for ln in lines[start + 1:end]:
        for axis in AXES:
            if ln.startswith("| %s |" % axis):
                cells = ln.split(" | ")
                rows.setdefault(axis, []).append({
                    "line": ln,
                    "cells": cells,
                    "observable": cells[2] if len(cells) > 2 else "",
                    "evidence": cells[3] if len(cells) > 3 else "",
                })
    return rows


def unique_row(rows, axis):
    """Return (row, problem).

    The frozen rule speaks of 'the row' for each axis, so exactly one row per
    axis inside '## Owned axes' is expected.  Zero rows or several rows leave
    the item undecidable and are reported as a mismatch instead of a silent
    first-row or last-row choice.
    """
    found = rows.get(axis, [])
    if not found:
        return None, "no '| %s |' row inside ## Owned axes" % axis
    if len(found) > 1:
        return None, "%d '| %s |' rows inside ## Owned axes; the row is not unique" % (len(found), axis)
    return found[0], None


def first_nm(text):
    m = NM.search(text or "")
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)))


def first_hex_after_measured(text):
    """First maximal hex run of length 7..40 that follows the word 'measured'."""
    for m in MEASURED.finditer(text or ""):
        for hm in HEXRUN.finditer(text[m.end():]):
            run = hm.group(0)
            if 7 <= len(run) <= 40:
                return run.lower()
    return None


def craft_span(skill_text):
    """H = line of the '## Queue-drain craft' heading; L = last non-blank line
    before the next line starting with '## '."""
    lines = skill_text.splitlines()
    h = None
    for i, ln in enumerate(lines):
        if ln.startswith("## Queue-drain craft"):
            h = i + 1
            break
    if h is None:
        raise InputError("no_craft_heading:SKILL.md")
    last = len(lines)
    for i in range(h, len(lines)):
        if lines[i].startswith("## "):
            last = i
            break
    line_no = last
    while line_no > h and not lines[line_no - 1].strip():
        line_no -= 1
    if line_no < h:
        line_no = h
    return h, line_no


# ---------------------------------------------------------------- the items

def measure(root, rev):
    scorecard = blob(root, rev, "SCORECARD.md")
    shonen = blob(root, rev, "SHONEN.md")
    province = blob(root, rev, "PROVINCE.md")
    result_text = blob(root, rev, RESULT_JSON)
    try:
        result_obj = json.loads(result_text)
    except ValueError:
        raise InputError("bad_json:%s" % RESULT_JSON)
    if not isinstance(result_obj, dict) or "measured_revision" not in result_obj:
        raise InputError("no_measured_revision:%s" % RESULT_JSON)

    rows = owned_axes_rows(scorecard)
    a_rev = command_a(root, rev)
    h, l = craft_span(blob(root, rev, "SKILL.md"))
    province_lines = len(province.splitlines())

    depth, depth_problem = unique_row(rows, "depth")
    coverage, coverage_problem = unique_row(rows, "coverage")
    calibration, calibration_problem = unique_row(rows, "calibration")

    items = []

    # ---- K1 -------------------------------------------------------------
    depth_nm = first_nm(depth["observable"]) if depth else None
    k1_stated = {"row_nm": depth_nm,
                 "command_a_rule_blocks": a_rev["rule_blocks"],
                 "command_a_citation_resolved_rules": a_rev["citation_resolved_rules"]}
    if depth is None:
        k1_ok = False
        k1_note = depth_problem
    elif depth_nm is None:
        k1_ok = False
        k1_note = "no N/M token in the depth observable cell"
    elif depth_nm[0] == depth_nm[1] == a_rev["rule_blocks"] == a_rev["citation_resolved_rules"]:
        k1_ok = True
        k1_note = "depth row N/M equals command A rule_blocks and citation_resolved_rules"
    else:
        k1_ok = False
        k1_note = "depth row N/M != command A rule_blocks/citation_resolved_rules"
    items.append({"id": "K1",
                  "what": "depth row: first N/M token in the observable cell has N == M == command A rule_blocks == citation_resolved_rules at REV",
                  "result": "pass" if k1_ok else "mismatch",
                  "stated": k1_stated, "observed": k1_stated, "note": k1_note})

    # ---- K2 -------------------------------------------------------------
    span = "SKILL.md:%d-%d" % (h, l)
    k2_evidence = depth["evidence"] if depth else ""
    k2_ok = depth is not None and span in k2_evidence
    k2_note = ("craft span at REV is %d-%d" % (h, l)) if depth is not None else depth_problem
    if depth is not None and span not in k2_evidence:
        k2_note = ("the depth evidence cell does not contain %s (craft span at REV is %d-%d)"
                   % (span, h, l))
    items.append({"id": "K2",
                  "what": "depth row: the evidence cell contains the string SKILL.md:H-L for the craft span at REV",
                  "result": "pass" if k2_ok else "mismatch",
                  "stated": {"craft_span": span, "in_evidence_cell": span in k2_evidence},
                  "observed": {"craft_span": span, "in_evidence_cell": span in k2_evidence},
                  "note": k2_note})

    # ---- K3 -------------------------------------------------------------
    k3_rev = first_hex_after_measured(depth["evidence"]) if depth else None
    k3_state = {"hex_after_measured": k3_rev}
    if depth is None or k3_rev is None:
        k3_ok = False
        k3_state.update({"resolves": False,
                         "reason": depth_problem if depth is None
                         else "no 7-40 hex revision after 'measured'"})
    else:
        p = git(root, "rev-parse", "--verify", "%s^{commit}" % k3_rev)
        resolves = p.returncode == 0
        k3_state["resolves"] = resolves
        if not resolves:
            k3_ok = False
            k3_state["reason"] = "revision does not resolve to a commit"
        elif depth_nm is None:
            k3_ok = False
            k3_state["reason"] = "no N/M token in the depth observable cell"
        else:
            a_at = command_a(root, k3_rev)
            k3_state["command_a_at_measured_revision"] = {
                "rule_blocks": a_at["rule_blocks"],
                "citation_resolved_rules": a_at["citation_resolved_rules"]}
            k3_state["k1_n"] = depth_nm[0]
            k3_ok = (a_at["rule_blocks"] == a_at["citation_resolved_rules"] == depth_nm[0])
            if not k3_ok:
                k3_state["reason"] = "command A at the measured revision does not give the K1 N"
    items.append({"id": "K3",
                  "what": "depth row: the first 7-40 hex revision following 'measured' in the evidence cell resolves, and command A at that revision gives rule_blocks == citation_resolved_rules == the K1 N",
                  "result": "pass" if k3_ok else "mismatch",
                  "stated": k3_state, "observed": k3_state,
                  "note": k3_state.get("reason", "measured revision agrees with the K1 N")})

    # ---- K4 -------------------------------------------------------------
    cov_nm = first_nm(coverage["observable"]) if coverage else None
    k4_state = {"row_nm": cov_nm,
                "command_a_mapped": a_rev["mapped"],
                "command_a_knowledge_files": a_rev["knowledge_files"]}
    if coverage is None or cov_nm is None:
        k4_ok = False
        k4_state["reason"] = (coverage_problem if coverage is None
                               else "no N/M token in the coverage observable cell")
    else:
        k4_state["headline_ok"] = (cov_nm[0] == cov_nm[1] == a_rev["mapped"] == a_rev["knowledge_files"])
        k4_rev = first_hex_after_measured(coverage["evidence"])
        k4_state["hex_after_measured"] = k4_rev
        if k4_rev is None:
            k4_ok = False
            k4_state["measured_revision_ok"] = False
            k4_state["reason"] = "no 7-40 hex revision after 'measured'"
        else:
            p = git(root, "rev-parse", "--verify", "%s^{commit}" % k4_rev)
            if p.returncode != 0:
                k4_ok = False
                k4_state["measured_revision_ok"] = False
                k4_state["reason"] = "measured revision does not resolve to a commit"
            else:
                a_at = command_a(root, k4_rev)
                same = (a_at["mapped"] == cov_nm[0] and a_at["knowledge_files"] == cov_nm[1])
                k4_state["measured_revision_ok"] = same
                k4_state["command_a_at_measured_revision"] = {
                    "mapped": a_at["mapped"], "knowledge_files": a_at["knowledge_files"]}
                k4_ok = bool(k4_state["headline_ok"]) and same
                if not k4_ok:
                    k4_state["reason"] = "coverage row N/M does not match command A at REV and at the measured revision"
    items.append({"id": "K4",
                  "what": "coverage row: the first N/M token in the observable cell has N == M == command A mapped == knowledge_files at REV, and the first 7-40 hex revision following 'measured' in the evidence cell resolves and gives the same N/M under command A",
                  "result": "pass" if k4_ok else "mismatch",
                  "stated": k4_state, "observed": k4_state,
                  "note": k4_state.get("reason", "coverage row agrees with command A at REV and at the measured revision")})

    # ---- K5 -------------------------------------------------------------
    calib_rev = first_hex_after_measured(calibration["evidence"]) if calibration else None
    measured_revision = str(result_obj.get("measured_revision", ""))
    k5_state = {"hex_after_measured": calib_rev,
                "measured_revision": measured_revision}
    if calibration is None or calib_rev is None:
        k5_ok = False
        k5_state["reason"] = (calibration_problem if calibration is None
                               else "no 7-40 hex revision after 'measured' in the calibration evidence cell")
    else:
        k5_ok = measured_revision.lower().startswith(calib_rev.lower())
        k5_state["prefix_ok"] = k5_ok
        if not k5_ok:
            k5_state["reason"] = "the measured revision in the calibration row is not a prefix of measured_revision"
    items.append({"id": "K5",
                  "what": "calibration row: the first 7-40 hex revision following 'measured' in the evidence cell is a prefix of measured_revision in evidence/round-1-2026-10-15/result.json at REV",
                  "result": "pass" if k5_ok else "mismatch",
                  "stated": k5_state, "observed": k5_state,
                  "note": k5_state.get("reason", "calibration measured revision prefixes measured_revision")})

    # ---- K6 -------------------------------------------------------------
    shonen_lines = shonen.splitlines()
    box = None
    for i, ln in enumerate(shonen_lines):
        if ln.startswith("- [~] No cross-domain bleed") or ln.startswith("- [x] No cross-domain bleed"):
            box = i
            break
    if box is None:
        k6_ok = False
        k6_state = {"box_line": None, "reason": "no '- [~] No cross-domain bleed' box line in SHONEN.md"}
    else:
        after = shonen_lines[box + 1] if box + 1 < len(shonen_lines) else ""
        contested = "contested" in after
        pointers = []
        for m in PROVINCE_PTR.finditer(after):
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else start
            pointers.append({"pointer": m.group(0), "start": start, "end": end,
                             "inside_line_count": 1 <= start <= end <= province_lines})
        k6_state = {"box_line": box + 1, "line_after_box": after,
                    "contains_contested": contested,
                    "province_line_count": province_lines,
                    "pointers": pointers}
        k6_ok = (not contested) and bool(pointers) and all(p["inside_line_count"] for p in pointers)
        if not pointers:
            k6_state["reason"] = "no PROVINCE.md pointer on the line after the box line"
        elif contested:
            k6_state["reason"] = "the line after the box line contains the word 'contested'"
        elif not all(p["inside_line_count"] for p in pointers):
            k6_state["reason"] = "a PROVINCE.md pointer is outside PROVINCE.md's line count"
    items.append({"id": "K6",
                  "what": "SHONEN.md: the line after the box line '- [~] No cross-domain bleed' does not contain the word 'contested', and every PROVINCE.md:A-B or PROVINCE.md:A pointer in it is inside PROVINCE.md's line count at REV",
                  "result": "pass" if k6_ok else "mismatch",
                  "stated": k6_state, "observed": k6_state,
                  "note": k6_state.get("reason", "the asserted boundary line is clean and inside PROVINCE.md")})

    mismatches = sum(1 for i in items if i["result"] != "pass")
    return {"instrument": INSTRUMENT, "root": os.path.abspath(root), "rev": rev,
            "items": len(items), "mismatches": mismatches,
            "command_a_at_rev": a_rev, "detail": items}


# ---------------------------------------------------------------- selftest

FIX_ALPHA = "alpha line one\nalpha line two\n"
FIX_BETA = "beta line one\n"
FIX_RESULT_MEASURED = "deadbeef" + "0" * 32
FIX_PROVINCE = "# Fixture PROVINCE\n\nline three\nline four\nline five\n"
FIX_README = ("# Fixture corpus\n\n## Coverage map\n\n"
              "- 2026-10-20-alpha - fixture entry\n"
              "- 2026-10-21-beta - fixture entry\n\n"
              "## Other section\n\nnot the map\n")


def fix_skill(rule_count):
    body = ["# Fixture SKILL", "", "## Queue-drain craft (fixture)", ""]
    for i in range(rule_count):
        if i:
            body.append("")
        if i == 0:
            body.append("- **Rule one.** cites `corpus/knowledge/2026-10-20-alpha.md:1-2`.")
        elif i == 1:
            body.append("- **Rule two.** cites `corpus/knowledge/2026-10-21-beta.md:1`.")
        else:
            body.append("- **Rule %d.** cites `corpus/knowledge/2026-10-20-alpha.md:1`." % (i + 1))
    body += ["", "## Next section", "", "Body.", ""]
    return "\n".join(body)


def fix_scorecard(depth_nm="2/2", depth_span="SKILL.md:3-7", depth_rev=None,
                  cov_nm="2/2", cov_rev=None, calib_rev="deadbeef",
                  decoy_before=False, decoy_after=True, dup_inside=False):
    depth_rev = depth_rev or "HASH1"
    cov_rev = cov_rev or "HASH1"
    head = ["# Fixture scorecard", ""]
    if decoy_before:
        head += ["| coverage | 9.72 -> 10.0 | 99/99 knowledge files mapped; decoy row before ## Owned axes | decoy | decoy |", ""]
    head += [
        "## Owned axes", "",
        "| Axis | Baseline -> current score, 0-10 | Observable and limitation | Evidence / counting command | Last-change round |",
        "|---|---|---|---|---|",
        "| coverage | 9.72 -> 10.0 | %s knowledge files mapped; index integrity only | `corpus/README.md` `## Coverage map`; command A; measured `%s` | fixture |" % (cov_nm, cov_rev),
        "| depth | 10 -> 10 | %s queue-drain rule blocks have resolvable file/range citations | `%s` at fixture; command A; measured `%s` | fixture |" % (depth_nm, depth_span, depth_rev),
        "| calibration | 0 -> 10 | 2/2 preselected reconciliation obligations aligned | command B; measured at `%s` | fixture |" % calib_rev,
        "",
    ]
    if dup_inside:
        head.insert(head.index("| depth | 10 -> 10 | 2/2 queue-drain rule blocks have resolvable file/range citations | `SKILL.md:3-7` at fixture; command A; measured `HASH1` | fixture |"),
                    "| coverage | 9.72 -> 10.0 | 9/9 knowledge files mapped; second coverage row inside ## Owned axes | decoy | decoy |")
    if decoy_after:
        head += [
            "## Later notes", "",
            "| coverage | 9.72 -> 10.0 | 9/9 knowledge files mapped; decoy row outside ## Owned axes | decoy | decoy |",
            "",
        ]
    return "\n".join(head)


def fix_shonen(asserted=None, box="- [~]"):
    asserted = asserted or ("  asserted boundary only: `PROVINCE.md:2-3`; "
                             "no promotion or complete accuracy claimed.")
    return "\n".join([
        "# Fixture promotion checklist", "",
        "%s No cross-domain bleed (PROVINCE.md still accurate)" % box,
        asserted, "",
    ])


def git_fixture(repo, *args):
    env = git_env()
    env.update({"GIT_AUTHOR_NAME": "c2 selftest", "GIT_AUTHOR_EMAIL": "c2@example.invalid",
                "GIT_COMMITTER_NAME": "c2 selftest", "GIT_COMMITTER_EMAIL": "c2@example.invalid"})
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, env=env)
    if p.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), p.stderr))
    return p.stdout


def write_files(repo, files):
    for path, text in files.items():
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(text)


def build_fixture(base, name, *, base_rules=2, rev_rules=2, scorecard=None,
                  shonen=None, province=None, readme=None):
    """Build a temporary Git repo holding one fixture state.

    commit 1: base content (base_rules craft rules)
    commit 2: the state under test (rev_rules craft rules + SCORECARD/SHONEN)
    """
    repo = os.path.join(base, name)
    os.makedirs(repo, exist_ok=True)
    git_fixture(repo, "init", "-q")
    write_files(repo, {
        "SKILL.md": fix_skill(base_rules),
        "corpus/README.md": readme if readme is not None else FIX_README,
        "corpus/knowledge/2026-10-20-alpha.md": FIX_ALPHA,
        "corpus/knowledge/2026-10-21-beta.md": FIX_BETA,
        "PROVINCE.md": province if province is not None else FIX_PROVINCE,
        "SHONEN.md": fix_shonen(),
        "evidence/round-1-2026-10-15/result.json": json.dumps(
            {"measured_revision": FIX_RESULT_MEASURED}, indent=1) + "\n",
        "SCORECARD.md": "# Fixture scorecard\n\n## Owned axes\n\n(no rows yet)\n",
    })
    git_fixture(repo, "add", "-A")
    git_fixture(repo, "commit", "-q", "-m", "fixture base")
    h1 = git_fixture(repo, "rev-parse", "HEAD").strip()

    score = scorecard if scorecard is not None else fix_scorecard()
    score = score.replace("HASH1", h1[:8])
    write_files(repo, {
        "SKILL.md": fix_skill(rev_rules),
        "SCORECARD.md": score,
    })
    if shonen is not None:
        write_files(repo, {"SHONEN.md": shonen})
    if province is not None:
        write_files(repo, {"PROVINCE.md": province})
    git_fixture(repo, "add", "-A")
    git_fixture(repo, "commit", "-q", "-m", "fixture under test")
    h2 = git_fixture(repo, "rev-parse", "HEAD").strip()
    return repo, h2


def run_instrument(root, rev):
    script = os.path.abspath(__file__)
    p = subprocess.run([sys.executable, "-I", "-B", script, "--root", root, "--rev", rev],
                       capture_output=True, text=True)
    try:
        payload = json.loads(p.stdout)
    except ValueError:
        payload = {"parse_error": p.stdout, "stderr": p.stderr}
    return p.returncode, payload


def selftest():
    results = []
    failures = 0
    base = tempfile.mkdtemp(prefix="c2-calibration-selftest-")
    try:
        cases = []

        # green: every item holds; the decoy '| coverage |' row lives outside
        # '## Owned axes' and must not be read.
        cases.append(("green", {}, 0, set()))
        # K1 red: the depth row's N/M no longer agrees with command A.
        cases.append(("k1-red", {"scorecard": fix_scorecard(depth_nm="2/3")}, 1, {"K1"}))
        # K2 red: the depth evidence cell names the wrong craft span.
        cases.append(("k2-red", {"scorecard": fix_scorecard(depth_span="SKILL.md:3-8")}, 1, {"K2"}))
        # K3 red: the measured revision resolves but command A there gives 3 rule
        # blocks while the depth row states 2/2.
        cases.append(("k3-red", {"base_rules": 3, "rev_rules": 2}, 1, {"K3"}))
        # K4 red: the coverage row states 3/3 while command A maps 2/2.
        cases.append(("k4-red", {"scorecard": fix_scorecard(cov_nm="3/3")}, 1, {"K4"}))
        # K5 red: the calibration row's measured revision is not a prefix of
        # measured_revision in result.json.
        cases.append(("k5-red", {"scorecard": fix_scorecard(calib_rev="abcdef01")}, 1, {"K5"}))
        # K6 red: a PROVINCE.md pointer outside PROVINCE.md's line count.
        cases.append(("k6-red", {"shonen": fix_shonen(
            "  asserted boundary only: `PROVINCE.md:2-9`; no promotion claimed.")}, 1, {"K6"}))
        # K6 red: the asserted line still carries the word 'contested'.
        cases.append(("k6-contested-red", {"shonen": fix_shonen(
            "  asserted boundary only: `PROVINCE.md:2-3`; province-version alignment is contested.")}, 1, {"K6"}))
        # Decoy guard: the green fixture keeps a '| coverage |' row outside
        # '## Owned axes' that claims 9/9; reading it would break K4.
        cases.append(("decoy-outside-owned-axes", {}, 0, set()))

        # A second '| coverage |' row inside '## Owned axes' leaves the row
        # undecidable, so K4 must not pass silently.
        cases.append(("k4-duplicate-row-inside-owned-axes", {
            "scorecard": fix_scorecard(dup_inside=True)}, 1, {"K4"}))
        # Mutations derived from seat KaidokuR26.MutR25Calib's round-25
        # fixtures (routed defect 3), rebuilt here so the shipped selftest
        # depends on nothing outside this file.
        # M1: a decoy '| coverage |' row before '## Owned axes' plus a wrong
        # owned-axes coverage row.  The decoy must not be read and the
        # owned-axes row must be, so K4 has to fail.
        cases.append(("m1-decoy-row-before-owned-axes", {
            "scorecard": fix_scorecard(cov_nm="99/99", decoy_before=True)}, 1, {"K4"}))
        # M5: the README '## Coverage map' drops one knowledge stem while the
        # coverage row still claims 2/2; command A then maps 1 of 2 files.
        cases.append(("m5-readme-map-stem-removed", {
            "scorecard": fix_scorecard(),
            "readme": ("# Fixture corpus\n\n## Coverage map\n\n"
                       "- 2026-10-20-alpha - fixture entry\n\n"
                       "## Other section\n\nnot the map\n")}, 1, {"K4"}))
        # M8 control: a wrong owned-axes coverage row and no decoy.
        cases.append(("m8-control-wrong-owned-axes-coverage-row", {
            "scorecard": fix_scorecard(cov_nm="99/99", decoy_after=False)}, 1, {"K4"}))
        # M6: the box mark becomes '- [x]' while the 'contested' clause stays.
        cases.append(("m6-shonen-box-promoted-to-checked", {
            "shonen": fix_shonen(
                "  asserted boundary only: `PROVINCE.md:2-3`; province-version alignment is contested.",
                box="- [x]")}, 1, {"K6"}))
        # M9 (disclosed limit of the frozen rule): a checked box with the
        # 'contested' clause rewritten as 'settled' is not observable to K1-K6;
        # the frozen rule reads the box line, not its mark.
        cases.append(("m9-shonen-box-checked-contested-settled", {
            "shonen": fix_shonen(
                "  asserted boundary only: `PROVINCE.md:2-3`; province-version alignment is settled by the observations.",
                box="- [x]")}, 0, set()))
        # M2 (disclosed limit of the frozen rule): a PROVINCE.md pointer inside
        # PROVINCE.md's line count but outside the refusal list is not
        # observable to K6, which bounds pointers by the line count only.
        cases.append(("m2-shonen-pointer-inside-province-line-count", {
            "province": ("# Fixture PROVINCE\n\n## Refusals\n\nline four\nline five\n\n"
                         "## Core tables\n\n" + "row\n" * 10),
            "shonen": fix_shonen(
                "  asserted boundary only: `PROVINCE.md:9-12`; no promotion claimed.")}, 0, set()))

        for name, kwargs, want_exit, want_fail in cases:
            repo, rev = build_fixture(base, name, **kwargs)
            code, payload = run_instrument(repo, rev)
            failing = set()
            if isinstance(payload, dict) and isinstance(payload.get("detail"), list):
                failing = set(d["id"] for d in payload["detail"] if d.get("result") != "pass")
            ok = (code == want_exit and failing == want_fail
                  and payload.get("mismatches") == len(want_fail))
            failures += 0 if ok else 1
            results.append({"case": name, "exit": code,
                            "expected_exit": want_exit,
                            "mismatches": payload.get("mismatches"),
                            "expected_mismatches": len(want_fail),
                            "failing_items": sorted(failing),
                            "expected_failing_items": sorted(want_fail),
                            "ok": ok})
        # The decoy row must exist in the green fixture and must sit outside
        # '## Owned axes', otherwise the green case would not prove anything.
        repo, rev = build_fixture(base, "decoy-check")
        with open(os.path.join(repo, "SCORECARD.md"), encoding="utf-8") as fh:
            text = fh.read()
        owned = text.split("## Owned axes", 1)[1].split("\n## ", 1)[0]
        decoy_lines = [ln for ln in text.splitlines()
                       if ln.startswith("| coverage |") and "decoy" in ln]
        decoy_present = (len(decoy_lines) == 1
                         and decoy_lines[0] not in owned.splitlines()
                         and any(ln.startswith("| coverage |") for ln in owned.splitlines()))
        failures += 0 if decoy_present else 1
        results.append({"case": "decoy-row-is-outside-owned-axes",
                        "decoy_rows_found": len(decoy_lines),
                        "decoy_present_outside_owned_axes": decoy_present,
                        "ok": decoy_present})
        # A bad revision is an input error (exit 2).
        code, payload = run_instrument(repo, "0" * 40)
        ok = code == 2
        failures += 0 if ok else 1
        results.append({"case": "bad-revision-is-input-error", "exit": code,
                        "expected_exit": 2, "ok": ok})
    finally:
        shutil.rmtree(base, ignore_errors=True)
    print(json.dumps({"selftest": "c2-calibration", "cases": len(results),
                      "failures": failures, "detail": results}, indent=1))
    return 0 if failures == 0 else 1


# ---------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(description="R26-C2 calibration counting instrument")
    ap.add_argument("--root", help="lane repository path (read-only, Git objects only)")
    ap.add_argument("--rev", help="revision to measure")
    ap.add_argument("--selftest", action="store_true",
                    help="run the built-in red-fixture selftest and exit")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.root or not a.rev:
        print(json.dumps({"error": "usage", "instrument": INSTRUMENT}))
        return 2
    try:
        rev = resolve_rev(a.root, a.rev)
        out = measure(a.root, rev)
    except InputError as e:
        print(json.dumps({"error": str(e), "instrument": INSTRUMENT, "rev": a.rev}, indent=1))
        return 2
    print(json.dumps(out, indent=1))
    return 0 if out["mismatches"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
