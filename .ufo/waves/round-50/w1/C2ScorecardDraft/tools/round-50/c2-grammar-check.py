#!/usr/bin/env python3
"""Draft check (C2ScorecardDraft, pre-freeze; not a frozen counter).

Reads the round-50 SCORECARD repair blocks from `landing-blocks.md` and tests them against the
regexes the round-47/48 counters really use (copied verbatim from the committed bytes:
`tools/round-48/record2.py` CORR / CORR_HEAD / AXIS_SCORE / FRAC, `tools/round-47/record.py`
CORR / CORR_SEATS). Reads only git objects at --rev; writes nothing into the lane.

  python3 -I -B c2-grammar-check.py --root LANE --rev REV --blocks landing-blocks.md

Exit: 0 every parsed line re-derives and no inert line is in the block; 1 otherwise; 2 unevaluable.
"""
import argparse
import json
import re
import subprocess
import sys

CORR_R48 = re.compile(r"^- corrects (seats|window|path|rev|axes|quote) (\S+):\s*(.+)$")
CORR_R47 = re.compile(r"^- corrects (seats|window|path|rev) (\S+):\s*(.+)$")
CORR_SEATS = re.compile(r"(\d+) waves?,\s*(\d+) seats total")
AXIS_SCORE = re.compile(r"(?m)^\|\s*(coverage|depth)\s*\|(.*)$")
SCORE_CELL = re.compile(r"(\d+(?:\.\d+)?)\s*(?:→|->)\s*(\d+(?:\.\d+)?)")
FRAC = re.compile(r"\b(\d+)/(\d+)\b")
A9_FORM = re.compile(r"^- (B\d+|A\d+) verdict=\S+")
HEAD = "## Record corrections \u2014 round 50"


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True)


def show(root, rev, path):
    p = git(root, "show", f"{rev}:{path}")
    return p.stdout.decode("utf-8", "replace") if p.returncode == 0 else None


def blocks_section(md):
    """The fenced block whose first line is HEAD (the paste text), up to its closing fence."""
    lines = md.split("\n")
    out, on, fence = [], False, False
    for l in lines:
        if l.startswith("```"):
            if on:
                break
            fence = True
            continue
        if fence and l == HEAD:
            on = True
        if on:
            out.append(l)
    return out


def dispatch_spawns(root, rev, rnd):
    spawns, i = [], 1
    while True:
        body = show(root, rev, f".ufo/waves/round-{rnd}/w{i}-dispatch.json")
        if body is None:
            break
        spawns.append(int(json.loads(body)["counts"]["spawn"]))
        i += 1
    return spawns


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--blocks", required=True)
    a = ap.parse_args(argv)
    try:
        md = open(a.blocks, encoding="utf-8").read()
    except OSError as e:
        print(json.dumps({"exit_code": 2, "error": str(e)}))
        return 2
    sec = blocks_section(md)
    if not sec or sec[0] != HEAD:
        print(json.dumps({"exit_code": 2, "error": "no round-50 section block found"}))
        return 2
    report = {"rev": a.rev, "lines": [], "failing": []}
    for l in sec:
        if not l.startswith("- "):
            continue
        rec = {"line": l[:110]}
        m8 = CORR_R48.match(l)
        m7 = CORR_R47.match(l)
        if m8 is None:
            rec["parsed_by_round48_grammar"] = False
            rec["parsed_by_round49_A_form"] = bool(A9_FORM.match(l))
            if not rec["parsed_by_round49_A_form"]:
                rec["status"] = "inert"
                report["failing"].append({"inert": l[:80]})
            else:
                rec["status"] = "A-form (needs a round-50 counter atom)"
            report["lines"].append(rec)
            continue
        cls, key, stmt = m8.group(1), m8.group(2), m8.group(3)
        rec.update({"class": cls, "key": key, "parsed_by_round48_grammar": True,
                    "parsed_by_round47_grammar": m7 is not None})
        if cls == "seats":
            m = CORR_SEATS.search(stmt)
            k = key[6:] if key.startswith("round-") else key
            spawns = dispatch_spawns(a.root, a.rev, k)
            claimed = (int(m.group(1)), int(m.group(2))) if m else None
            got = (len(spawns), sum(spawns))
            rec.update({"claimed": claimed, "derived": got, "dispatch": spawns,
                        "ok": claimed == got})
            if claimed != got:
                report["failing"].append({"seats": key})
        elif cls == "path":
            ok = show(a.root, a.rev, key) is not None
            rec.update({"path": key, "exists_at_rev": ok})
            if not ok:
                report["failing"].append({"path": key})
        rec["status"] = "re-derives" if rec.get("ok", rec.get("exists_at_rev")) else "fails"
        report["lines"].append(rec)
    # the two owned-axes rows, as record2.axis_scores reads them (filled and as drafted)
    card = show(a.root, a.rev, "SCORECARD.md") or ""
    body = card.split("## Owned axes", 1)[1].split("\n## ", 1)[0] if "## Owned axes" in card else ""
    report["owned_axes_at_rev"] = {m.group(1): bool(FRAC.search(m.group(2)))
                                   for m in AXIS_SCORE.finditer(body)}
    for blk in ("<N>/<N> knowledge files mapped at the round-50 landing",
                "139/139 knowledge files mapped at the round-49 landing"):
        report.setdefault("block1_frac", {})[blk[:12]] = bool(FRAC.search(blk))
    report["block1_drafted_frac_matches"] = FRAC.findall(sec[0] if False else
        [l for l in md.split("\n") if l.startswith("<N>/<N> knowledge")][0])
    report["exit_code"] = 1 if report["failing"] else 0
    print(json.dumps(report, indent=1, ensure_ascii=False))
    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
