#!/usr/bin/env python3
"""normalize-append.py — R38ExecMirrorGate scratch transform for the SOURCES append block.

Reads the scribe's raw admitted-entry rows, emits a normalized 11-column fleet-schema
block (SOURCES-CONTRACT-v1), and refuses (non-zero) on any row that would fail the
fleet census gate. Never writes into the lane corpus: outputs go to --out.

Checks per row:
  N01 cell count != 11 (literal '|' or escaped '\\|' inside a cell also lands here)
  N02 id not S[0-9]{3,}
  N03 id already in the registry (E03 collision) or duplicated inside the block
  N04 kind outside the enum
  N05 tier outside A|B|C
  N06 status != mined (this round admits mined rows only)
  N07 opened not an ISO date, or not the round-38 opening date
  N08 recheck not ISO date | NNd | symbolic cadence
  N09 tier C + mined + used-by != em dash (W01 shape)
  N10 community at tier A
  N11 teaches shorter than 8 characters (W02 shape)
  N12 used-by em dash or empty (W03 shape)
  N13 used-by entry not in the admitted-entry set
  N14 duplicate URL+scope within the block or against the registry, without
      'supersedes S<nnn>' in teaches (E04)
"""
import argparse
import json
import re
import sys

KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book", "community", "own-work"}
STATUSES = {"queued", "mined", "rejected"}
SYMBOLIC = re.compile(r"^[A-Za-z][A-Za-z0-9 _-]*$")
ISO = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
CADENCE = re.compile(r"^[0-9]+d$")
ID_RE = re.compile(r"^S[0-9]{3,}$")
URL_RE = re.compile(r"https?://[^\s|]+")
DASH = "\u2014"


def trim(s):
    return s.strip(" \t")


def split_row(line):
    """Split a markdown table row into cells; returns (cells, raw_pipe_count)."""
    s = line.strip(" \t\r\n")
    if not s.startswith("|"):
        return None, 0
    raw = s.count("|")
    body = s[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [trim(c) for c in body.split("|")], raw


def is_separator(cells):
    if not cells:
        return False
    if cells[0] == "id":
        return True
    return all(re.fullmatch(r":?-+:?", c) for c in cells if c != "")


def url_of(source):
    m = URL_RE.search(source)
    if not m:
        return ""
    u = m.group(0)
    u = re.sub(r"#[^ ]*$", "", u)
    u = u.rstrip("/")
    u = re.sub(r"^[A-Za-z]+://", "", u)
    n = u.find("/")
    return (u[:n].lower() + u[n:]) if n >= 0 else u.lower()


def registry_rows(path):
    """Yield (id, cells) for Registry-section table rows of a SOURCES.md."""
    out = []
    in_registry = False
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            raw = line.rstrip("\n")
            stripped = raw.lstrip(" ")
            indent = len(raw) - len(stripped)
            if indent <= 3 and stripped.startswith("## "):
                in_registry = trim(stripped[3:]) == "Registry"
                continue
            if indent <= 3 and stripped.startswith("# "):
                in_registry = False
                continue
            if not in_registry or indent > 3 or not stripped.startswith("|"):
                continue
            cells, _ = split_row(stripped)
            if not cells or is_separator(cells):
                continue
            if len(cells) < 11:
                continue
            out.append((cells[0], cells))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--block", required=True)
    ap.add_argument("--sources", required=True, help="lane corpus/SOURCES.md (read-only)")
    ap.add_argument("--out", required=True, help="normalized block output path")
    ap.add_argument("--opened", default="2026-10-26")
    ap.add_argument("--used-by", required=True,
                    help="comma-separated admitted entry paths (repo-relative)")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()

    admitted = [trim(p) for p in args.used_by.split(",") if trim(p)]
    admitted_set = set(admitted)

    reg = registry_rows(args.sources)
    reg_ids = {cid for cid, _ in reg}
    reg_url_scope = {}
    for cid, cells in reg:
        u = url_of(cells[1])
        scope = cells[4]
        if u and cells[7] != "rejected":
            reg_url_scope.setdefault((u, scope), cid)

    findings = []
    rows_out = []
    seen_ids = set()
    seen_url_scope = {}
    n_rows = 0

    with open(args.block, encoding="utf-8") as fh:
        lines = fh.readlines()

    for lineno, line in enumerate(lines, 1):
        if not line.lstrip(" ").startswith("|"):
            continue
        cells, raw_pipes = split_row(line)
        if cells is None or is_separator(cells):
            continue
        if cells and cells[0] == "id":
            continue
        n_rows += 1
        rid = cells[0] if cells else ""
        tag = rid or f"line{lineno}"

        # N01: exact 11 cells; a literal or escaped pipe inside a cell inflates raw_pipes.
        if len(cells) != 11:
            findings.append(f"N01 {tag} cells={len(cells)} (want 11)")
            continue
        if raw_pipes != 12:
            findings.append(f"N01 {tag} raw-pipes={raw_pipes} (want 12; literal or escaped '|' in a cell)")
            continue
        if any(("|" in c) or ("\\|" in c) for c in cells):
            findings.append(f"N01 {tag} cell carries a literal or escaped '|'")
            continue

        rid, source, kind, tier, scope, anchor, teaches, status, opened, recheck, usedby = cells

        if not ID_RE.match(rid):
            findings.append(f"N02 {tag} id={rid!r}")
        elif rid in reg_ids:
            findings.append(f"N03 {tag} collides with a registry id (E03)")
        elif rid in seen_ids:
            findings.append(f"N03 {tag} duplicated inside the block")
        seen_ids.add(rid)

        if kind not in KINDS:
            findings.append(f"N04 {tag} kind={kind!r}")
        if tier not in {"A", "B", "C"}:
            findings.append(f"N05 {tag} tier={tier!r}")
        if status not in STATUSES or status not in {"mined", "rejected"}:
            findings.append(f"N06 {tag} status={status!r} (this round admits mined or rejected)")
        if not ISO.match(opened) or opened != args.opened:
            findings.append(f"N07 {tag} opened={opened!r} (want {args.opened})")
        if not (ISO.match(recheck) or CADENCE.match(recheck) or SYMBOLIC.match(recheck)):
            findings.append(f"N08 {tag} recheck={recheck!r}")
        if tier == "C" and status == "mined" and usedby != DASH:
            findings.append(f"N09 {tag} tier-C mined with used-by={usedby!r}")
        if tier == "A" and kind == "community":
            findings.append(f"N10 {tag} community at tier A")
        if len(teaches) < 8:
            findings.append(f"N11 {tag} teaches too short ({len(teaches)})")
        if status == "mined":
            if usedby == DASH or usedby == "":
                findings.append(f"N12 {tag} mined with used-by={usedby!r}")
            else:
                listed = [trim(p) for p in usedby.split(",") if trim(p)]
                if set(listed) != admitted_set or listed != admitted:
                    findings.append(
                        f"N13 {tag} used-by={listed} != admitted entries {admitted}")
        elif status == "rejected" and usedby not in (DASH, ""):
            listed = [trim(p) for p in usedby.split(",") if trim(p)]
            if not set(listed) <= admitted_set:
                findings.append(
                    f"N13 {tag} rejected row used-by={listed} not within admitted entries")
        u = url_of(source)
        key = (u, scope)
        if u:
            if key in seen_url_scope:
                findings.append(f"N14 {tag} duplicate url+scope with {seen_url_scope[key]}")
            elif key in reg_url_scope and "supersedes S" not in teaches:
                findings.append(
                    f"N14 {tag} duplicate url+scope with registry {reg_url_scope[key]} and no supersedes")
            seen_url_scope[key] = rid

        rows_out.append("| " + " | ".join(cells) + " |")

    receipt = {
        "block": args.block,
        "sources": args.sources,
        "opened": args.opened,
        "admitted_entries": admitted,
        "rows_in": n_rows,
        "rows_out": len(rows_out),
        "findings": findings,
        "ok": not findings and n_rows > 0,
    }
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=2)
            fh.write("\n")

    with open(args.out, "w", encoding="utf-8") as fh:
        for r in rows_out:
            fh.write(r + "\n")

    for f in findings:
        print(f)
    print(f"rows_in={n_rows} rows_out={len(rows_out)} findings={len(findings)}")
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
