#!/usr/bin/env python3
"""CN-1 emulation: does a C1 coverage-map edit break C3's pointer-table entries?

Faithful re-implementation of the probe's entry-checking code path for the
`exact` / `extracted` / `anchor` kinds (citation-drift-probe.py:168-260,
specifically: citing_line = citing[line_no-1]; re.search on that one line;
no match -> citation_dead). The probe itself resolves files through
`git show <rev>:<path>`; this emulation reads the SAME bytes from the same
source (`git show HEAD:<path>`) and applies a simulated line insertion to
corpus/README.md only - the file C1's claim edits. Output is a PREDICTION
(simulation), not a probe run, and is labeled as such.

Variants:
  A  line-neutral token add: the EVM map row (line 31) gains the new token,
     physical line count unchanged.
  B  new map row: one physical line inserted after the EVM row.

Usage: python3 readme-line-shift-emulation.py
"""
import json
import re
import subprocess

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"


def git_show(path):
    out = subprocess.run(["git", "-C", REPO, "show", f"HEAD:{path}"],
                         capture_output=True)
    return out.stdout.decode("utf-8")


def load(path):
    return git_show(path).splitlines()


def check_entry(entry, lines_by_file):
    """Mirror of citation-drift-probe.py check_entry for exact/extracted/anchor."""
    target = entry["file"]
    lines = lines_by_file.get(target)
    if lines is None:
        return "citation_file_absent"
    kind = entry["kind"]
    if kind == "anchor":
        hits = [i + 1 for i, l in enumerate(lines)
                if re.search(entry["must_match"], l)]
        if not hits:
            return "citation_dead"
        if entry.get("pin_line") is not None and entry["pin_line"] not in hits:
            return "citation_moved"
        return None
    line_no = entry.get("line")
    if not isinstance(line_no, int) or not (1 <= line_no <= len(lines)):
        return "citation_out_of_range"
    citing_line = lines[line_no - 1]
    if kind in ("quoted", "exact"):
        return None if re.search(entry["must_match"], citing_line) else "citation_dead"
    if kind == "extracted":
        return None if re.search(entry["pattern"], citing_line) else "citation_dead"
    return None


def main():
    table = json.load(open(f"{REPO}/.ufo/gates/citation-drift/pointer-table.json"))
    readme = load("corpus/README.md")

    # sanity: the map section bounds as command A sees them
    text = "\n".join(readme)
    section = text.split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
    map_lines = section.count("\n")
    print(f"README lines at HEAD: {len(readme)}; coverage-map section lines: {map_lines}")

    evm_row = next(i for i, l in enumerate(readme, 1)
                   if l.startswith("| EVM |"))
    print(f"EVM map row at line {evm_row}")

    # Variant A - line-neutral: append the new token to the EVM row
    var_a = list(readme)
    var_a[evm_row - 1] = var_a[evm_row - 1].replace(
        "`2026-10-19-arc3-r1-evm-real-solc`",
        "`2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-<slug>`")

    # Variant B - new physical row inside the map section
    var_b = list(readme)
    var_b.insert(evm_row, "| (simulated new row) | `2026-10-19-arc3-r3-<slug>` | held |")

    for name, lines in (("A line-neutral", var_a), ("B new-row-insertion", var_b)):
        by_file = {}
        for entry in table["entries"]:
            by_file.setdefault(entry["file"], None)
        for f in by_file:
            by_file[f] = lines if f == "corpus/README.md" else load(f)
        findings = []
        for entry in table["entries"]:
            verdict = check_entry(entry, by_file)
            if verdict:
                findings.append((entry["id"], verdict))
        print(f"\n=== Variant {name}: README lines={len(lines)} ===")
        print(f"simulated findings: {len(findings)}")
        for eid, v in findings:
            print(f"  {eid}: {v}")

    # control: unmodified
    by_file = {e["file"]: load(e["file"]) for e in table["entries"]}
    control = [(e["id"], check_entry(e, by_file)) for e in table["entries"]]
    bad = [x for x in control if x[1]]
    print(f"\n=== Control (unmodified HEAD): simulated findings={len(bad)} ===")
    for eid, v in bad:
        print(f"  {eid}: {v}")


if __name__ == "__main__":
    main()