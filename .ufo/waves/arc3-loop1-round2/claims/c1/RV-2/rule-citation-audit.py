#!/usr/bin/env python3
"""Rule-citation audit (SEAT RV-2, wave arc3-loop1-round2, chain c1).

Reviews the queue-drain craft rule block in SKILL.md at a named revision:
  (1) RESOLVABILITY -- every `path:line` / `path:start-end` citation resolves at
      that revision (path exists as a Git object; 1 <= start <= end <= line count).
  (2) RULE-#11 FORM -- a citation whose target is rewritten in place
      (in-place-rewritten repo file, or an out-of-repo custody path) must not be
      a bare line number standing alone: the citing text must carry a content
      anchor (stanza key in brackets, or a path-keyed anchor) AND a capture
      stamp (a named receipt path or an ISO/clock stamp).

Targets are read as immutable Git objects (`git show REV:path`), never the
moving worktree. Out-of-repo custody paths are stat-only (read-only).

Usage:
  rule-citation-audit.py [--root DIR] [--rev REV] [--skill PATH]
                         [--class-table PATH] [--json OUT]
  rule-citation-audit.py --selftest

Exit codes: 0 = audit printed (verdicts are in the JSON: `dead` list and
`form_flags` list), 2 = could-not-evaluate (missing revision or unparsable
section).
"""
import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_SKILL = "SKILL.md"
SECTION_START = "## Queue-drain craft"
RULE_SPLIT = re.compile(r"(?m)^- \*\*")

# path (repo-relative, ~-rooted or /-rooted), optional :line or :start-end
CITE = re.compile(
    r"(?<![\w./-])"
    r"(?P<path>(?:~|\.\.)?/?(?:[\w.@+-]+/)*[\w.@+-]+"
    r"\.(?:md|py|json|txt|toml|sh|js|ts))"
    r"(?::(?P<start>\d+)(?:-(?P<end>\d+))?)?"
    r"(?![\w-])"
)

# write-cadence classes. in-place-rewritten targets drift under inserts above the
# target; append-only records keep their line numbers by construction.
CLASSES = {
    "in-place-rewritten": {
        "SKILL.md", "SCORECARD.md", "PROVINCE.md", "SHONEN.md", "README.md",
        "corpus/README.md", "corpus/QUALITY.md",
    },
    "append-only-record": set(),  # corpus/knowledge, corpus/lessons, LOG.md, wave artifacts, receipts
    "external-custody": {
        "~/.kimi-code/config.toml", "~/.omp/agent/mcp.json",
        "~/.config/devin/mcp_config.json", "~/.bashrc", "~/.profile",
    },
}

RECEIPT = re.compile(
    r"(?:\d{2}:\d{2}:\d{2}Z|\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z|"
    r"receipt(?:s)?\b|\.bak\b|#[0-9a-f]{6,})"
)
STANZA_KEY = re.compile(r"`\[[\w.\-]+\]`|\bargs\b\s*(?:key|keys)")
PATH_ANCHOR = re.compile(r"`~?[\w./-]+\.(?:toml|json|md|txt)`")


def classify(path):
    if path in CLASSES["external-custody"]:
        return "external-custody"
    if path in CLASSES["in-place-rewritten"]:
        return "in-place-rewritten"
    if path == "LOG.md" or path.startswith("corpus/knowledge/") or path.startswith("corpus/lessons/"):
        return "append-only-record"
    if path.startswith(".ufo/") or path.startswith("evidence/"):
        return "append-only-record"  # wave artifacts / receipts: write-once
    if path.startswith("~") or path.startswith("/"):
        return "external-other"
    if path.endswith(".md") and ("/reports/" in path or "/rounds/" in path):
        return "append-only-record"
    return "repo-other"


def git_show(root, rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], cwd=root,
                          capture_output=True, text=True)


def audit(root, rev, skill_path=DEFAULT_SKILL, block_text=None):
    if block_text is not None:
        # draft mode: the candidate rule block resolves against the tree at rev,
        # but its own text is not yet in the tree. Wrap it in the section header
        # so the same split/extract path runs.
        skill = SECTION_START + " (draft)\n\n" + block_text.rstrip("\n") + "\n"
    else:
        r = git_show(root, rev, skill_path)
        if r.returncode != 0:
            return {"error": "revision_unresolvable", "detail": r.stderr.strip()}
        skill = r.stdout
    lines = skill.splitlines()
    if SECTION_START not in skill:
        return {"error": "section_absent"}
    start = skill.index(SECTION_START)
    start_line = skill[:start].count("\n") + 1
    tail = skill[start:]
    nxt = re.search(r"(?m)^## ", tail[len(SECTION_START):])
    section = tail if nxt is None else tail[: len(SECTION_START) + nxt.start()]
    section_lines = lines[start_line - 1: start_line - 1 + section.count("\n")]

    # split rules, keeping the absolute line number of each rule's first line
    parts = []
    cur, cur_line = [], None
    for i, ln in enumerate(section_lines):
        if ln.startswith("- **"):
            if cur is not None:
                parts.append((cur_line, cur))
            cur, cur_line = [ln], start_line + i
        elif cur is not None:
            cur.append(ln)
    if cur is not None:
        parts.append((cur_line, cur))

    # line-count cache per target
    counts, missing = {}, set()
    rules_out, dead, form_flags, all_cites = [], [], [], []

    def line_count(path):
        if path in counts or path in missing:
            return counts.get(path, 0)
        rr = git_show(root, rev, path)
        if rr.returncode != 0:
            missing.add(path)
            counts[path] = 0
            return 0
        n = len(rr.stdout.splitlines())
        counts[path] = n
        return n

    for first_line, body in parts:
        text = "\n".join(body)
        title = body[0].split("**")[1] if "**" in body[0] else body[0]
        refs, seen = [], set()
        for m in CITE.finditer(text):
            path, s, e = m.group("path"), m.group("start"), m.group("end")
            if (path, s, e) in seen:
                continue
            seen.add((path, s, e))
            entry = {"path": path, "start": int(s) if s else None,
                     "end": int(e) if e else (int(s) if s else None),
                     "class": classify(path)}
            if entry["class"] in ("in-place-rewritten", "external-custody",
                                  "append-only-record", "external-other",
                                  "repo-other"):
                if not path.startswith(("~", "/")):
                    n = line_count(path)
                    if n == 0:
                        entry["resolvable"] = False
                        entry["why"] = "file_absent_at_rev"
                    elif entry["start"] is None:
                        entry["resolvable"] = True
                        entry["why"] = "path_only"
                    elif 1 <= entry["start"] <= (entry["end"] or entry["start"]) <= n:
                        entry["resolvable"] = True
                        entry["why"] = f"lines<={n}"
                    else:
                        entry["resolvable"] = False
                        entry["why"] = f"out_of_range (file has {n} lines)"
                else:
                    # out-of-repo target: READ-ONLY stat/line-count capture only
                    live = os.path.expanduser(path)
                    if os.path.isfile(live):
                        try:
                            with open(live, "rb") as fh:
                                n_live = fh.read().count(b"\n") + 1
                        except OSError:
                            n_live = None
                        entry["resolvable"] = None
                        entry["live_stat"] = "exists"
                        entry["live_lines"] = n_live
                        entry["why"] = "out_of_repo (live copy exists; stat-only)"
                    else:
                        entry["resolvable"] = None
                        entry["live_stat"] = "absent"
                        entry["why"] = "out_of_repo (live copy absent at read time)"
            refs.append(entry)
            all_cites.append({"rule_line": first_line, **entry})

        dead_here = [x for x in refs if x.get("resolvable") is False]
        for x in dead_here:
            dead.append({"rule_line": first_line, "rule": title[:60], **x})

        # rule-#11 form: a bare line number into an in-place-rewritten target is a
        # flag unless the same rule text carries a content anchor AND a stamp.
        has_stamp = bool(RECEIPT.search(text))
        has_key = bool(STANZA_KEY.search(text) or PATH_ANCHOR.search(text))
        flags_here = []
        for x in refs:
            if x["class"] in ("in-place-rewritten", "external-custody") and x["start"]:
                if not (has_stamp and has_key):
                    flags_here.append({**x, "why": "bare_line_into_in_place_target",
                                       "rule_has_stamp": has_stamp,
                                       "rule_has_content_anchor": has_key})
        form_flags.extend({"rule_line": first_line, "rule": title[:60], **x}
                          for x in flags_here)

        rules_out.append({
            "rule_line": first_line, "title": title[:80],
            "citations": len(refs), "dead": len(dead_here),
            "form_flags": len(flags_here),
            "has_stamp": has_stamp, "has_content_anchor": has_key,
        })

    return {
        "revision": rev, "skill": skill_path,
        "section_line": start_line, "rules": len(rules_out),
        "total_citations": len(all_cites),
        "resolved": sum(1 for c in all_cites if c.get("resolvable") is True),
        "dead": dead, "form_flags": form_flags,
        "per_rule": rules_out, "citations": all_cites,
    }


def selftest(root):
    """Mutate a scratch copy of SKILL.md and require the auditor to catch it."""
    import shutil
    import tempfile
    outcomes = []
    base = subprocess.run(["git", "show", "HEAD:SKILL.md"], cwd=root,
                          capture_output=True, text=True).stdout
    scratch = tempfile.mkdtemp(prefix="rv2-audit-", dir="/var/tmp")
    # build an isolated mini-repo so git objects are the fixture
    subprocess.run(["git", "init", "-q", scratch], check=True)
    subprocess.run(["git", "-C", scratch, "config", "user.email", "rv2@test"],
                   check=True)
    subprocess.run(["git", "-C", scratch, "config", "user.name", "rv2"], check=True)

    # seed every repo-relative path the section cites, so "clean" means clean
    seeded = set()
    for p in re.findall(r"(?<![\w./-])([\w][\w./-]*\.(?:md|py|json|txt|toml|sh|js|ts))", base):
        if p.startswith(("~", "/")):
            continue
        r = git_show(root, "HEAD", p)
        if r.returncode == 0:
            dst = os.path.join(scratch, p)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "w") as fh:
                fh.write(r.stdout)
            seeded.add(p)

    def commit(skill_text):
        with open(os.path.join(scratch, "SKILL.md"), "w") as fh:
            fh.write(skill_text)
        subprocess.run(["git", "-C", scratch, "add", "-A"], check=True)
        subprocess.run(["git", "-C", scratch, "commit", "-q", "-m", "fixture"],
                       check=True)
        return subprocess.run(["git", "-C", scratch, "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()

    rev = commit(base)
    clean = audit(scratch, rev)
    outcomes.append({"case": "clean", "rules": clean["rules"], "dead": len(clean["dead"]),
                     "form_flags": len(clean["form_flags"]),
                     "expect_dead": 0})
    # case: dead line number (rule 1's first corpus citation set past EOF)
    m = re.search(r"(corpus/knowledge/[\w.-]+\.md):(\d+)", base)
    mutated = base[:m.start(2)] + "99999" + base[m.end(2):]
    rev2 = commit(mutated)
    dead = audit(scratch, rev2)
    outcomes.append({"case": "dead_line", "dead": len(dead["dead"]),
                     "expect_dead": 1, "caught": len(dead["dead"]) >= 1})
    # case: bare line into an in-place target -> form flag
    anchor = "corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md"
    mutated2 = base.replace(
        f"`{anchor}:144-146`", f"`SCORECARD.md:59999` and `{anchor}:144-146`", 1)
    rev3 = commit(mutated2)
    flagged = audit(scratch, rev3)
    outcomes.append({"case": "bare_in_place_line",
                     "form_flags": len(flagged["form_flags"]),
                     "caught": len(flagged["form_flags"]) >= 1})
    shutil.rmtree(scratch, ignore_errors=True)
    return outcomes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--skill", default=DEFAULT_SKILL)
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--block", help="audit a not-yet-landed rule block (draft) "
                                    "against the tree at --rev")
    ap.add_argument("--summary", action="store_true",
                    help="print a compact summary instead of the full JSON")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    if a.selftest:
        out = selftest(root)
        print(json.dumps(out, indent=2))
        ok = all(o.get("caught", o.get("expect_dead") == 0) for o in out)
        print("SELFTEST", "PASS" if ok else "FAIL")
        sys.exit(0 if ok else 1)
    if a.rev == "HEAD":
        a.rev = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                               capture_output=True, text=True).stdout.strip()
    block = None
    if a.block:
        with open(a.block, encoding="utf-8") as fh:
            block = fh.read()
    res = audit(root, a.rev, a.skill, block_text=block)
    text = json.dumps(res, indent=2, sort_keys=True)
    if a.json_out:
        with open(a.json_out, "w") as fh:
            fh.write(text)
    if a.summary and "error" not in res:
        targets = {}
        for c in res["citations"]:
            key = (c["path"], c["class"])
            targets.setdefault(key, [0, 0])
            targets[key][0] += 1
            targets[key][1] += 1 if c.get("resolvable") is False else 0
        print("revision %s | rules %d | citations %d | resolved %d | dead %d | form_flags %d"
              % (res["revision"], res["rules"], res["total_citations"],
                 res["resolved"], len(res["dead"]), len(res["form_flags"])))
        for (p, k), (n, d) in sorted(targets.items()):
            print("  target %-70s class=%-20s cites=%d dead=%d" % (p, k, n, d))
        for x in res["dead"]:
            print("  DEAD  %s:%s-%s (%s) rule_line=%s"
                  % (x["path"], x["start"], x["end"], x["why"], x["rule_line"]))
        for x in res["form_flags"]:
            print("  FORM  %s:%s-%s (%s) rule_line=%s stamp=%s anchor=%s"
                  % (x["path"], x["start"], x["end"], x["why"], x["rule_line"],
                     x["rule_has_stamp"], x["rule_has_content_anchor"]))
    else:
        print(text)
    sys.exit(0 if "error" not in res else 2)


if __name__ == "__main__":
    main()
