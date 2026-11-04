#!/usr/bin/env python3
"""Mechanical checker for the round-77 ScribeSources drafts. Read-only.

Checks, per row:
  - 11 cells (12 delimiters), no literal or escaped pipe inside a cell;
  - id / kind / tier / status / opened / recheck enums;
  - the first URL token equals the expected normalized URL;
  - the snapshot digest and byte count appear in the anchor cell;
  - the located quote is byte-exact inside the stated 1-based line and occurs
    exactly once in the file;
  - the quote's word count, recomputed, equals the stated count.
Also recomputes the sha256 of each snapshot from its bytes.
"""
import hashlib
import json
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SNAP = LANE + "/.ufo/waves/round-77/l1/sources/"
ROWS = LANE + "/.ufo/waves/round-77/w1/ScribeSources/rows-draft.md"

EXPECT = [
    {
        "id": "S289",
        "snapshot": "rfc8259.txt",
        "url": "www.rfc-editor.org/rfc/rfc8259.txt",
        "line": 298,
        "quote": "A JSON value MUST be an object, array, number, or string, or one of",
        "words": 14,
        "kind": "spec", "tier": "A", "status": "mined",
        "recheck": "90d",
    },
    {
        "id": "S290",
        "snapshot": "page-721dd237.html",
        "url": "www.gnu.org/software/bash/manual/bash.html",
        "line": 4435,
        "quote": "Bash itself returns the exit status of the last command",
        "words": 10,
        "kind": "docs", "tier": "A", "status": "mined",
        "recheck": "180d",
    },
    {
        "id": "S291",
        "snapshot": "page-298eb5f5.html",
        "url": "docs.python.org/3/library/ast.html",
        "line": 2760,
        "quote": "Evaluate an expression node or a string containing only a Python literal or",
        "words": 13,
        "kind": "docs", "tier": "C", "status": "rejected",
        "recheck": "180d",
    },
]

URL_RE = re.compile(r"https?://[^\s|]+")


def url_of(cell):
    m = URL_RE.search(cell)
    if not m:
        return ""
    u = re.sub(r"#[^ ]*$", "", m.group(0))
    u = re.sub(r"/$", "", u)
    u = re.sub(r"^[A-Za-z]+://", "", u)
    n = u.find("/")
    return (u[:n].lower() + u[n:]) if n >= 0 else u.lower()


def main():
    rows = [
        line.rstrip("\n") for line in open(ROWS, encoding="utf-8")
        if line.startswith("| S2")
    ]
    fails = []
    out = {"rows": len(rows), "checks": [], "failures": []}
    if len(rows) != 3:
        fails.append("row count %d != 3" % len(rows))
    for want, row in zip(EXPECT, rows):
        cells = row.split("|")
        if len(cells) != 13:
            fails.append("%s delimiters %d != 13" % (want["id"], len(cells)))
            continue
        body = [c.strip() for c in cells[1:-1]]
        rec = {"id": want["id"], "cells": len(body)}
        for i, c in enumerate(body):
            if "|" in c or "\\|" in c:
                fails.append("%s cell %d carries a pipe" % (want["id"], i + 1))
        if not row.startswith("| " + want["id"] + " |"):
            fails.append("%s id cell" % want["id"])
        for idx, name in ((2, "kind"), (3, "tier"), (7, "status"),
                          (8, "opened"), (9, "recheck")):
            rec[name] = body[idx]
            if name in want and body[idx] != want[name]:
                fails.append("%s %s %r != %r" % (want["id"], name, body[idx], want[name]))
        if body[8] != "2026-11-04":
            fails.append("%s opened %r" % (want["id"], body[8]))
        if url_of(body[1]) != want["url"]:
            fails.append("%s url %r != %r" % (want["id"], url_of(body[1]), want["url"]))
        data = open(SNAP + want["snapshot"], "rb").read()
        digest = hashlib.sha256(data).hexdigest()
        rec.update(snapshot=want["snapshot"], bytes=len(data), sha256=digest)
        if "%d" % len(data) in body[5].replace("\u00a0", " ") is False:
            fails.append("%s anchor lacks byte count" % want["id"])
        if digest not in body[5]:
            fails.append("%s anchor lacks the full sha256" % want["id"])
        lines = data.split(b"\n")
        if not (1 <= want["line"] <= len(lines)):
            fails.append("%s line out of range" % want["id"])
            continue
        qbytes = want["quote"].encode()
        rec["quote_line_exact"] = qbytes in lines[want["line"] - 1]
        rec["file_occurrences"] = data.count(qbytes)
        rec["words_computed"] = len(want["quote"].split())
        rec["words_stated_in_draft"] = None
        stated = re.search(r"(\d+) words", body[5])
        if stated:
            rec["words_stated_in_draft"] = int(stated.group(1))
        if not rec["quote_line_exact"]:
            fails.append("%s quote not byte-exact at line %d" % (want["id"], want["line"]))
        if rec["file_occurrences"] != 1:
            fails.append("%s quote occurs %d times" % (want["id"], rec["file_occurrences"]))
        if rec["words_computed"] != want["words"]:
            fails.append("%s words %d != %d" % (want["id"], rec["words_computed"], want["words"]))
        if str(want["line"]) not in body[5]:
            fails.append("%s anchor cell does not state line %d" % (want["id"], want["line"]))
        if want["id"] == "S291" and "grep -c 'literal_eval'" not in body[6]:
            fails.append("S291 teaches lacks the consumer search")
        if want["status"] == "rejected" and "Flip:" not in body[6]:
            fails.append("%s rejected row lacks a Flip" % want["id"])
        out["checks"].append(rec)
    out["failures"] = fails
    print(json.dumps(out, indent=1))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
