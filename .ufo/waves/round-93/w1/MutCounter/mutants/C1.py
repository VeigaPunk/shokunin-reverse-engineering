#!/usr/bin/env python3
"""craft-citation-semantic.py - round-93 counter (R93-C2, depth).

A craft row's criterion citation must name a criterion whose text states the
rule the row asserts. Round 91 landed craft block 31 whose row 3 cited
`corpus/QUALITY.md` row 169 (guard inheritance) for the intact-input rule —
a citation that resolves but mis-states, invisible to every citation-resolves
counter until the round-92 non-author spot-check named it (D-91-3). This
checker freezes, per row, the keyword atoms the cited criterion must contain.

Input: a frozen JSON manifest (`--manifest`):

    {"block": 32,
     "marker": "stop-boundary-supersedes-citation v1",
     "rows": [{"row_snippet": "intact input refused by mistake",
               "keywords": ["exactly one candidate", "packer's own verdict"]},
              ...]}

For every manifest row the checker:
1. reads the `## Queue-drain craft` section of `SKILL.md` (at `--rev` via
   `git show`, or `--worktree` from the tree) and takes rule block `<block>`;
2. requires the block to carry its marker comment and a decision-table shape
   (header + separator + >= 3 body rows of >= 4 cells);
3. finds exactly one body row whose first cell contains `row_snippet`;
4. parses the criterion cell's `QUALITY <N>` citation (exactly one);
5. reads criterion row N of `corpus/QUALITY.md` (bullet `- **Row N (**` or
   table `| N |`) and requires every keyword verbatim in its text.

Exit 0 iff every atom passes; 1 names the failing atoms (row not found, block
missing, marker missing, shape violated, citation absent, keyword missing);
2 on could-not-evaluate (unknown revision, unreadable files, malformed
manifest, ambiguous row snippet, criterion cell without a `QUALITY N` form is
an atom failure, not exit 2). `--selftest` runs 10 fixture cases under
`--work` and exits 0 iff every case lands its expected exit.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

TOOL = "tools/round-93/craft-citation-semantic.py"
CRAFT = "SKILL.md"
QUALITY = "corpus/QUALITY.md"


def _read(root: str, rev, path: str) -> str:
    if rev in (None, "worktree"):
        with open(os.path.join(root, path), encoding="utf-8") as fh:
            return fh.read()
    out = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise FileNotFoundError(f"{path} at {rev}")
    return out.stdout


def _blocks(text: str) -> list:
    craft = text.split("## Queue-drain craft", 1)[1].split("\n## ", 1)[0]
    return re.split(r"(?m)^- \*\*", craft)[1:]


def _table_rows(block: str) -> list:
    rows = []
    for line in block.splitlines():
        s = line.strip()
        if s.startswith("|") and not set(s) <= {"|", "-", " ", ":"}:
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(set(c) <= {"-", ":", " "} for c in cells):
                continue  # separator
            rows.append(cells)
    return rows  # first row is the header


def _quality_row(qtext: str, num: int):
    lines = qtext.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if re.match(rf"^- \*\*Row {num} \(", ln) or re.match(rf"^\|\s*{num}\s*\|", ln):
            start = i
            break
    if start is None:
        return None
    if lines[start].startswith("|"):
        return lines[start]
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r"^- \*\*Row \d+ \(", lines[j]) or lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end])


def check(root: str, manifest: dict, block_no: int, rev) -> tuple:
    failing, unevaluable = [], None
    if not isinstance(manifest, dict) or not isinstance(manifest.get("rows"), list) \
            or not manifest["rows"] or not isinstance(manifest.get("marker"), str):
        return 2, {"tool": TOOL, "unevaluable": "malformed manifest",
                   "failing": [], "manifest_block": block_no}
    try:
        skill = _read(root, rev, CRAFT)
        quality = _read(root, rev, QUALITY)
    except FileNotFoundError as exc:
        return 2, {"tool": TOOL, "unevaluable": str(exc), "failing": [],
                   "manifest_block": block_no}
    blocks = _blocks(skill)
    if not 1 <= block_no <= len(blocks):
        failing.append(f"block {block_no} missing (craft has {len(blocks)} blocks)")
        return 1, {"tool": TOOL, "failing": failing, "manifest_block": block_no,
                   "atoms": {"block_present": False}}
    block = blocks[block_no - 1]
    atoms = {"block_present": True}
    if manifest["marker"] not in block:
        failing.append(f"marker {manifest['marker']!r} absent from block {block_no}")
    atoms["marker"] = manifest["marker"] in block
    rows = _table_rows(block)
    header, body = (rows[0] if rows else []), rows[1:]
    shape = len(rows) >= 4 and len(header) >= 4 and len(body) >= 3 \
        and all(len(r) >= 4 for r in body)
    atoms["shape"] = shape
    if not shape:
        failing.append(f"block {block_no} table shape violated "
                       f"(header {len(header)} cells, body rows {len(body)})")
    checked = []
    for entry in manifest["rows"]:
        snippet = entry.get("row_snippet")
        keywords = entry.get("keywords")
        if not isinstance(snippet, str) or not snippet \
                or not isinstance(keywords, list) or not keywords \
                or not all(isinstance(k, str) and k for k in keywords):
            unevaluable = "malformed manifest row"
            break
        hits = [r for r in body if snippet in r[0]]
        if len(hits) == 0:
            failing.append(f"row not found: {snippet!r}")
            checked.append({"row_snippet": snippet, "found": False})
            continue
        if len(hits) > 1:
            unevaluable = f"row snippet matches {len(hits)} rows: {snippet!r}"
            break
        row = hits[0]
        criterion = row[-1]
        m = re.findall(r"QUALITY (\d+)", criterion)
        if len(m) != 1:
            failing.append(f"row {snippet!r}: criterion cell {criterion!r} "
                           f"names {len(m)} QUALITY citations, expected 1")
            checked.append({"row_snippet": snippet, "citations": m})
            continue
        num = int(m[0])
        qrow = _quality_row(quality, num)
        if qrow is None:
            failing.append(f"row {snippet!r}: cited QUALITY row {num} not found")
            checked.append({"row_snippet": snippet, "cited": num, "found": False})
            continue
        missing = []
        item = {"row_snippet": snippet, "cited": num,
                "missing_keywords": missing}
        checked.append(item)
        if missing:
            failing.append(f"row {snippet!r}: QUALITY {num} lacks {missing!r}")
    if unevaluable:
        return 2, {"tool": TOOL, "unevaluable": unevaluable, "failing": failing,
                   "manifest_block": block_no}
    ok = not failing
    return (0 if ok else 1), {"tool": TOOL, "manifest_block": block_no,
                              "revision": rev if rev not in (None,) else "worktree",
                              "atoms": atoms, "checked": checked,
                              "failing": failing, "ok": ok}


def _selftest(work: str) -> tuple:
    """10 fixture cases: expected exit per case."""
    os.makedirs(work, exist_ok=True)
    skill_body = (
        "# t\n\n## Queue-drain craft\n\n"
        "- **1. alpha rule.** <!-- alpha-marker v1 --> prose\n\n"
        "| class | signature | guard | criterion |\n|---|---|---|---|\n"
        "| alpha one | s | g | QUALITY 90 |\n"
        "| alpha two | s | g | QUALITY 91 |\n"
        "| alpha three | s | g | QUALITY 92 |\n\n"
        "  Refs: x.\n\n"
        "- **2. beta rule.** <!-- beta-marker v1 --> prose\n\n"
        "| class | signature | guard | criterion |\n|---|---|---|---|\n"
        "| intact input refused by mistake | s | never refuse an intact input | QUALITY 91 |\n"
        "| silent rc zero | s | refuse unless green | QUALITY 92 |\n"
        "| broken file silent | s | typed refusal | QUALITY 90 |\n\n"
        "  Refs: y.\n\n"
        "- **3. gamma rule.** <!-- gamma-marker v1 --> prose\n\n"
        "| class | signature | guard | criterion |\n|---|---|---|---|\n"
        "| gamma one | s | g | QUALITY 90 |\n"
        "| gamma two | s | g | QUALITY 91 |\n\n"
        "  Refs: z.\n\n## Next\n"
    )
    quality_body = (
        "# q\n\n## Admission criteria\n\n"
        "| 90 | table row criterion about nothing specific |\n|---|---|\n\n"
        "- **Row 91 (the intact rule).** Output is written only when exactly one "
        "candidate is green under the packer's own verdict; an intact input returns "
        "byte-identical.\n"
        "- **Row 92 (typed refusal).** Refuse with rc 2 and no output.\n"
    )
    root = os.path.join(work, "repo")
    os.makedirs(os.path.join(root, "corpus"), exist_ok=True)
    with open(os.path.join(root, "SKILL.md"), "w") as fh:
        fh.write(skill_body)
    with open(os.path.join(root, "corpus", "QUALITY.md"), "w") as fh:
        fh.write(quality_body)
    cases = []
    green = {"block": 2, "marker": "beta-marker v1", "rows": [
        {"row_snippet": "intact input refused", "keywords": ["exactly one candidate"]},
        {"row_snippet": "silent rc zero", "keywords": ["rc 2"]},
        {"row_snippet": "broken file silent", "keywords": ["nothing specific"]},
    ]}
    cases.append(("green", green, 0))
    cases.append(("keyword-miss", {"block": 2, "marker": "beta-marker v1", "rows": [
        {"row_snippet": "intact input refused", "keywords": ["byte-identical to the input"]}]}, 1))
    cases.append(("cited-row-missing", {"block": 2, "marker": "beta-marker v1", "rows": [
        {"row_snippet": "intact input refused", "keywords": ["exactly one candidate", "zzz"]},
        {"row_snippet": "broken file silent", "keywords": ["w"]}]}, 1))
    cases.append(("row-not-found", {"block": 2, "marker": "beta-marker v1", "rows": [
        {"row_snippet": "no such class", "keywords": ["x"]}]}, 1))
    cases.append(("block-missing", {"block": 9, "marker": "beta-marker v1", "rows": [
        {"row_snippet": "intact input refused", "keywords": ["exactly one candidate"]}]}, 1))
    cases.append(("marker-missing", {"block": 2, "marker": "no-such-marker", "rows": [
        {"row_snippet": "intact input refused", "keywords": ["exactly one candidate"]}]}, 1))
    cases.append(("shape", {"block": 3, "marker": "gamma-marker v1", "rows": [
        {"row_snippet": "gamma one", "keywords": ["nothing specific"]}]}, 1))
    cases.append(("no-citation-form", {"block": 2, "marker": "beta-marker v1", "rows": [
        {"row_snippet": "silent rc zero", "keywords": []}]}, 2))
    cases.append(("malformed", {"block": 2}, 2))
    cases.append(("unknown-rev", green, 2))
    results = []
    ok = True
    for name, manifest, want in cases:
        rev = "deadbeefnonexistent" if name == "unknown-rev" else None
        code, rec = check(root, manifest, manifest.get("block", 2), rev)
        good = code == want
        ok = ok and good
        results.append({"case": name, "want": want, "got": code, "ok": good})
        print(f"selftest {name}: want {want} got {code} {'ok' if good else 'FAIL'}")
    print(f"SELFTEST cases={len(cases)} failures={sum(1 for r in results if not r['ok'])}")
    return (0 if ok else 1), results


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--manifest", help="frozen manifest JSON")
    ap.add_argument("--block", type=int)
    ap.add_argument("--rev", default=None, help="revision or omitted/--worktree for the tree")
    ap.add_argument("--worktree", action="store_true")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work", help="scratch dir for --selftest fixtures")
    args = ap.parse_args(argv)
    if args.selftest:
        code, _ = _selftest(args.work or os.path.join(
            os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "kaidoku-r93",
            "l1", "selftest-c2"))
        return code
    if not args.manifest or not args.block:
        print("usage: --manifest <json> --block <N> [--rev R | --worktree]")
        return 2
    with open(args.manifest, encoding="utf-8") as fh:
        manifest = json.load(fh)
    rev = None if (args.worktree or args.rev in (None, "worktree")) else args.rev
    code, rec = check(os.path.abspath(args.root), manifest, args.block, rev)
    rec["manifest_path"] = args.manifest
    rec["exit"] = code
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(rec, fh, indent=1, sort_keys=True)
    print(("ok" if code == 0 else ("unevaluable: " + rec.get("unevaluable", "")
                                   if code == 2 else "failing")), "exit", code)
    for f in rec.get("failing", []):
        print("  -", f)
    return code


if __name__ == "__main__":
    sys.exit(main())
