#!/usr/bin/env python3
"""craft-citation-v2.py - round-97 counter (R97-C2, depth).

Supersedes `tools/round-93/craft-citation-semantic.py` on three counts, routed by the
round-96 CriticC2 attacks (a)-(d) and frozen before data:

1. **Criterion-cell restatement (kills attacks a and b).** At least one of the
   manifest row's keywords must occur verbatim in the matched craft row's own cells.
   A rule-free criterion (`see (QUALITY 193)`) or a criterion carrying the opposite
   rule with none of its row's vocabulary is refused (`criterion-not-restated`).
2. **Citation-number validation (kills attack c).** A manifest row may declare
   `expected_quality`; the single `QUALITY <N>` citation parsed from the criterion
   cell must equal it (`criterion-citation-mismatch:<num>!=<expected>`), so citing an
   overlapping neighbor row no longer passes.
3. **The snippet-carrying table is the shape oracle (kills attack d's padding).** The
   block's shape (header + separator + >= 3 body rows of >= 4 cells) is evaluated on
   the contiguous table that contains the matched row - a padded decoy table elsewhere
   in the block no longer rescues a junk table (`matched-table-shape:*`).

Everything else is unchanged from v1 (block + marker, one row per snippet, exactly one
`QUALITY <N>` citation, verbatim keywords in the cited QUALITY row, exit 0/1/2).
`--selftest` runs 14 fixture cases under `--work`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

TOOL = "tools/round-97/craft-citation-v2.py"
CRAFT = "SKILL.md"
QUALITY = "corpus/QUALITY.md"
MIN_BODY_ROWS = 3
MIN_CELLS = 4


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


def _tables(block: str) -> list:
    """Contiguous runs of `|`-starting lines; each run is a list of cell-lists."""
    tables, current = [], []
    for line in block.splitlines():
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            current.append([c.strip() for c in s.strip("|").split("|")])
        else:
            if current:
                tables.append(current)
                current = []
    if current:
        tables.append(current)
    return tables


def _is_separator(cells: list) -> bool:
    return all(set(c) <= {"-", ":", " "} for c in cells)


def _matched_table_shape(tables: list, row_index_global: int) -> tuple:
    """Shape of the table that contains the matched row (global body-row index).
    Returns (ok, problems). v1 merged every `|` line of the block; the padded decoy
    table must not rescue a junk table."""
    if not tables:
        return False, ["matched-table-shape:no-table"]
    # walk tables, tracking the global row index (v1 counted every | line as a row)
    idx = 0
    for t in tables:
        n = len(t)
        if idx <= row_index_global < idx + n:
            header = t[0]
            if len(t) < 2 or not _is_separator(t[1]):
                return False, ["matched-table-shape:no-separator"]
            body = t[2:]
            problems = []
            if len(body) < MIN_BODY_ROWS:
                problems.append("matched-table-shape:rows:%d<%d" % (len(body), MIN_BODY_ROWS))
            if len(header) < MIN_CELLS or any(len(r) < MIN_CELLS for r in body):
                problems.append("matched-table-shape:cells:<%d" % MIN_CELLS)
            return not problems, problems
        idx += n
    return False, ["matched-table-shape:row-not-in-table"]


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
    tables = _tables(block)
    header = tables[0][0] if tables else []
    body_rows = [r for t in tables for r in t[1:]]
    shape = bool(tables) and len(tables[0]) >= 2 and _is_separator(tables[0][1]) \
        and len(body_rows) >= 3 and len(header) >= 4 \
        and all(len(r) >= 4 for r in body_rows)
    atoms["shape"] = shape
    if not shape:
        failing.append(f"block {block_no} table shape violated "
                       f"(header {len(header)} cells, body rows {len(body_rows)})")
    checked = []
    for entry in manifest["rows"]:
        snippet = entry.get("row_snippet")
        keywords = entry.get("keywords")
        expected_quality = entry.get("expected_quality")
        if not isinstance(snippet, str) or not snippet \
                or not isinstance(keywords, list) or not keywords \
                or not all(isinstance(k, str) and k for k in keywords):
            unevaluable = "malformed manifest row"
            break
        # locate the matched row inside the contiguous tables (global row index)
        flat = [r for t in tables for r in t]
        hits = [i for i, r in enumerate(flat) if snippet in (r[0] if r else "")]
        if len(hits) == 0:
            failing.append(f"row not found: {snippet!r}")
            checked.append({"row_snippet": snippet, "found": False})
            continue
        if len(hits) > 1:
            unevaluable = f"row snippet matches {len(hits)} rows: {snippet!r}"
            break
        gi = hits[0]
        row = flat[gi]
        tok, tproblems = _matched_table_shape(tables, gi)
        checked.append({"row_snippet": snippet, "matched_table_shape": tok})
        if not tok:
            failing.append(f"row {snippet!r}: {tproblems[0]}")
            continue
        criterion = row[-1]
        m = re.findall(r"QUALITY (\d+)", criterion)
        if len(m) != 1:
            failing.append(f"row {snippet!r}: criterion cell {criterion!r} "
                           f"names {len(m)} QUALITY citations, expected 1")
            checked.append({"row_snippet": snippet, "citations": m})
            continue
        num = int(m[0])
        if expected_quality is not None and num != int(expected_quality):
            failing.append(f"row {snippet!r}: cites QUALITY {num}, "
                           f"expected {int(expected_quality)} "
                           f"(criterion-citation-mismatch:{num}!={int(expected_quality)})")
            checked.append({"row_snippet": snippet, "cited": num,
                            "expected": int(expected_quality)})
            continue
        restated = [k for k in keywords if k in "|".join(row)]
        if not restated:
            failing.append(f"row {snippet!r}: criterion cell restates none of its row's "
                           f"keywords {keywords!r} (criterion-not-restated)")
            checked.append({"row_snippet": snippet, "restated": []})
            continue
        qrow = _quality_row(quality, num)
        if qrow is None:
            failing.append(f"row {snippet!r}: cited QUALITY row {num} not found")
            checked.append({"row_snippet": snippet, "cited": num, "found": False})
            continue
        missing = [k for k in keywords if k not in qrow]
        item = {"row_snippet": snippet, "cited": num, "restated": restated,
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
    """14 fixture cases: expected exit per case."""
    os.makedirs(work, exist_ok=True)
    block36 = (
        "- **36. byte-bound receipts.** <!-- receipt-byte-binding v1 --> prose\n\n"
        "| class | signature | guard | criterion |\n|---|---|---|---|\n"
        "| pins name bytes the run did not use | s | refuse before scoring | "
        "QUALITY 195 (`git cat-file blob`, byte-pin-not-bound) |\n"
        "| met is not a real boolean | s | typed refusal | "
        "QUALITY 195 (met-not-typed) |\n"
        "| a crash is published as a kill | s | classify the kill | "
        "QUALITY 196 (crash kill class) |\n"
        "| green without a re-read receipt | s | rc 2 without json-out | "
        "QUALITY 196 (re-read) |\n\n  Refs: x.\n\n"
    )
    skill_body = (
        "# t\n\n## Queue-drain craft\n\n"
        "- **1. alpha rule.** <!-- alpha-marker v1 --> prose\n\n"
        "| class | signature | guard | criterion |\n|---|---|---|---|\n"
        "| alpha one | s | g | QUALITY 90 |\n"
        "| alpha two | s | g | QUALITY 91 |\n"
        "| alpha three | s | g | QUALITY 92 |\n\n"
        "  Refs: y.\n\n" + block36 + "## Next\n"
    )
    quality_body = (
        "# q\n\n## Admission criteria\n\n"
        "| 90 | table row criterion about nothing specific |\n|---|---|\n\n"
        "- **Row 91 (the intact rule).** Output is written only when exactly one "
        "candidate is green under the packer's own verdict; an intact input returns "
        "byte-identical.\n"
        "- **Row 92 (typed refusal).** Refuse with rc 2 and no output.\n"
        "- **Row 195 (byte-bound pins).** A receipt pin binds the exact bytes at the "
        "revision it names through git cat-file blob; byte-pin-not-bound refuses, and "
        "a met value is admitted only as a real boolean (met-not-typed).\n"
        "- **Row 196 (crash class and re-read).** A crash is classified, never "
        "published as a semantic kill, and the rule re-reads its own receipt before "
        "it may exit green.\n"
    )
    root = os.path.join(work, "repo")
    os.makedirs(os.path.join(root, "corpus"), exist_ok=True)
    with open(os.path.join(root, "SKILL.md"), "w") as fh:
        fh.write(skill_body)
    with open(os.path.join(root, "corpus", "QUALITY.md"), "w") as fh:
        fh.write(quality_body)
    rows = [
        {"row_snippet": "pins name bytes", "keywords": ["git cat-file blob"],
         "expected_quality": 195},
        {"row_snippet": "not a real boolean", "keywords": ["met-not-typed"],
         "expected_quality": 195},
        {"row_snippet": "published as a kill", "keywords": ["crash"],
         "expected_quality": 196},
        {"row_snippet": "green without a re-read", "keywords": ["re-read"],
         "expected_quality": 196},
    ]
    green = {"block": 2, "marker": "receipt-byte-binding v1", "rows": rows}
    cases = [("green", green, 0)]
    # attack b: rule-free criterion cells (`see (QUALITY 195)`) restate no keyword
    block36_rf = (
        "- **36. byte-bound receipts.** <!-- receipt-byte-binding v1 --> prose\n\n"
        "| class | signature | guard | criterion |\n|---|---|---|---|\n"
        "| pins name bytes the run did not use | s | refuse before scoring | "
        "see (QUALITY 195) |\n"
        "| met is not a real boolean | s | typed refusal | see (QUALITY 195) |\n"
        "| a crash is published as a kill | s | classify the kill | see (QUALITY 196) |\n"
        "| green without a re-read receipt | s | rc 2 without json-out | "
        "see (QUALITY 196) |\n\n  Refs: x.\n\n"
    )
    skill_body_rf = skill_body.replace(block36, block36_rf)
    root_rf = os.path.join(work, "repo-rf")
    os.makedirs(os.path.join(root_rf, "corpus"), exist_ok=True)
    with open(os.path.join(root_rf, "SKILL.md"), "w") as fh:
        fh.write(skill_body_rf)
    with open(os.path.join(root_rf, "corpus", "QUALITY.md"), "w") as fh:
        fh.write(quality_body)
    cases.append(("attack-b-rule-free", green, 1))
    # attack c: the row cites the overlapping neighbor row (195 vs expected 196)
    c_rows = [
        {"row_snippet": "pins name bytes", "keywords": ["git cat-file blob"],
         "expected_quality": 196},
        rows[1], rows[2], rows[3]]
    cases.append(("attack-c-wrong-row", {"block": 2, "marker": "receipt-byte-binding v1",
                                         "rows": c_rows}, 1))
    # attack d: padded decoy table cannot rescue a junk matched table
    padded = (
        "- **37. padded decoy.** <!-- decoy-marker v1 --> prose\n\n"
        "| class | signature | guard | criterion |\n|---|---|---|---|\n"
        "| junk row one | s | g | QUALITY 90 (nothing specific) |\n\n"
        "| pad1 | pad2 | pad3 | pad4 |\n|---|---|---|---|\n"
        "| a | b | c | d |\n| e | f | g | h |\n| i | j | k | l |\n\n  Refs: z.\n\n"
    )
    skill_body2 = skill_body.replace("## Next\n", padded + "## Next\n").replace(
        "# t\n", "# t2\n")
    root2 = os.path.join(work, "repo2")
    os.makedirs(os.path.join(root2, "corpus"), exist_ok=True)
    with open(os.path.join(root2, "SKILL.md"), "w") as fh:
        fh.write(skill_body2)
    with open(os.path.join(root2, "corpus", "QUALITY.md"), "w") as fh:
        fh.write(quality_body)
    cases.append(("attack-d-decoy", {"block": 3, "marker": "decoy-marker v1",
                "rows": [{"row_snippet": "junk row one", "keywords": ["nothing specific"],
                          "expected_quality": 90}]}, 1))
    cases.append(("keyword-miss", {"block": 2, "marker": "receipt-byte-binding v1",
                "rows": [{"row_snippet": "pins name bytes",
                          "keywords": ["byte-identical to the input"],
                          "expected_quality": 195},
                         rows[1], rows[2], rows[3]]}, 1))
    cases.append(("row-not-found", {"block": 2, "marker": "receipt-byte-binding v1",
                "rows": [{"row_snippet": "no such class", "keywords": ["x"],
                          "expected_quality": 195}, rows[1], rows[2], rows[3]]}, 1))
    cases.append(("block-missing", {"block": 9, "marker": "receipt-byte-binding v1",
                "rows": [rows[0]]}, 1))
    cases.append(("marker-missing", {"block": 2, "marker": "no-such-marker",
                "rows": [rows[0]]}, 1))
    cases.append(("no-citation-form", {"block": 2, "marker": "receipt-byte-binding v1",
                "rows": [{"row_snippet": "pins name bytes", "keywords": [],
                          "expected_quality": 195}]}, 2))
    cases.append(("malformed", {"block": 2}, 2))
    cases.append(("unknown-rev", green, 2))
    results = []
    ok = True
    for name, manifest, want in cases:
        root_use = root2 if name == "attack-d-decoy" else \
            root_rf if name == "attack-b-rule-free" else root
        rev = "deadbeefnonexistent" if name == "unknown-rev" else None
        code, rec = check(root_use, manifest, manifest.get("block", 2), rev)
        good = code == want
        ok = ok and good
        results.append({"case": name, "want": want, "got": code, "ok": good})
        print(f"selftest {name}: want {want} got {code} {'ok' if good else 'FAIL'} "
              f"{'' if good else rec.get('failing', [])[:2]}")
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
            os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "kaidoku-r97",
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
