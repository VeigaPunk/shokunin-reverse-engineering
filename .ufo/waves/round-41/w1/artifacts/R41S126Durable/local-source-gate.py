#!/usr/bin/env python3
"""local-source-gate — close round-40 closure D1 (unresolvable out-of-lane SOURCES rows).

Problem
-------
`corpus/SOURCES.md` rows may point at a *local absolute path* as their URL cell
(the column right after the row id).  When that path lives outside the lane, a
fresh checkout cannot resolve the row: the bytes it cites are not in the tree.
D1's instance is row S126, whose URL cell is
`/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv`.

The gate is a *report*, not a rewrite: it lists every row in that class and
says, per path, whether the lane names an in-lane copy with a matching digest.

Convention (normative for this tool)
------------------------------------
A sidecar map `corpus/evidence/local-sources.json` (override with --map) binds
each out-of-lane absolute path to exactly one in-lane copy:

  {
    "version": 1,
    "sources": {
      "/abs/external/path": {
        "copy": "corpus/evidence/round-41/s126/lead1-avm-image.tsv",
        "sha256": "<64 lowercase hex>",
        "sha256_file": "corpus/evidence/round-41/s126/lead1-avm-image.tsv.sha256",  # optional
        "kind": "file" | "tree-archive",                                            # optional, descriptive
        "note": "free text"                                                         # optional
      }
    }
  }

`copy` is relative to --root (never absolute, never escaping the root) and names
a *regular file*: either the byte-exact copy of a source file, or an archive of a
source directory.  `sha256` is the digest of that copy's bytes.

Per out-of-lane path the gate requires, in order:
  map-present -> entry-present -> copy-in-lane -> copy-exists-as-regular-file
  -> copy-digest-equals-entry  ->  (if the row itself pins digests) entry digest
  is one of the row's own pins  ->  (if the entry names a sha256_file) the
  sidecar is present, parses, and agrees.

A digest counts as a pin on the path only when it is written in the same URL cell
that names the path (`row-pin: url-cell`).  Digests elsewhere in the row describe
members or derived artefacts and are not consulted: row S035 pins the digest of
individual `.go` files, row S082 a package field, and neither can bind a directory
archive or a database file.

Exit status: 0 every row resolved, 1 at least one row unresolved, 2 usage /
parse error (bad table arity, unreadable rev, malformed map).

Advisory (never changes the exit status): for each unresolved path the tool
reports the first public `http(s)://` URL found in the *same* URL cell, if any.
That is a cell-level hint, not a per-path claim: on a multi-path row the URL may
cover only one of the paths (row S035 cites the go1.25.0 tag and also names the
go-1.24.6 directory).  A row whose URL cell is a local path alone has neither an
in-lane copy nor a public pin: that is the D1 class proper.

Stdlib only; honours TMPDIR; no network; read-only git (`show`) when --rev is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

SOURCES_REL = "corpus/SOURCES.md"
DEFAULT_MAP_REL = "corpus/evidence/local-sources.json"
ENTRY_KEYS = {"copy", "sha256", "sha256_file", "kind", "note", "source_sha256", "rebuild"}
HEX64 = re.compile(r"(?<![0-9a-fA-F])([0-9a-fA-F]{64})(?![0-9a-fA-F])")
URL = re.compile(r"[A-Za-z][A-Za-z0-9+.\-]*://[^\s`|]*")
# An absolute path token: a leading '/' that is not part of '//' or ':/' and at
# least one 'seg/' pair, so prose slashes such as `operation`/provider.id do not
# parse as paths.  A trailing '/' is kept and normalised away later.
ABSPATH = re.compile(r"(?<![\w:/~.\-])/(?:[A-Za-z0-9_.@%+~\-]+/)+[A-Za-z0-9_.@%+~\-]*")

ROW_START = re.compile(r"^\|\s*(S\d{3})\s*\|")
EXPECTED_COLS = 11  # id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by


class GateError(Exception):
    """Exit-2 condition: the gate could not be evaluated at all."""


# ---------------------------------------------------------------- table reading


def read_sources(root: str, rev: str | None, sources_path: str | None) -> tuple[str, str]:
    """Return (text, provenance).

    Precedence: --sources, then --rev (git show), then the on-disk
    `<root>/corpus/SOURCES.md`.  Reading the working tree by default keeps the
    gate usable outside git; pass --rev to pin a commit.
    """
    if sources_path:
        path = sources_path if os.path.isabs(sources_path) else os.path.join(root, sources_path)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return fh.read(), "file:" + path
        except OSError as exc:
            raise GateError("cannot read --sources %s: %s" % (path, exc)) from exc
    if rev is None:
        path = os.path.join(root, SOURCES_REL)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return fh.read(), "file:" + path
        except OSError as exc:
            raise GateError("cannot read %s: %s" % (path, exc)) from exc
    try:
        out = subprocess.run(
            ["git", "-C", root, "show", "%s:%s" % (rev, SOURCES_REL)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as exc:
        raise GateError("git not found; pass --sources") from exc
    except subprocess.CalledProcessError as exc:
        raise GateError(
            "git show %s:%s failed in %s: %s"
            % (rev, SOURCES_REL, root, exc.stderr.decode("utf-8", "replace").strip())
        ) from exc
    return out.stdout.decode("utf-8"), "git:%s:%s" % (rev, SOURCES_REL)


def split_row(line: str) -> list[str]:
    body = line.strip()
    if not (body.startswith("|") and body.endswith("|")):
        raise GateError("row is not pipe-delimited: %r" % line[:80])
    return [cell.strip() for cell in body[1:-1].split(" | ")]


def parse_rows(text: str) -> list[dict]:
    rows = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if not ROW_START.match(line):
            continue
        cells = split_row(line)
        if len(cells) != EXPECTED_COLS:
            raise GateError(
                "row %s at line %d has %d cells, expected %d"
                % (cells[0], lineno, len(cells), EXPECTED_COLS)
            )
        rows.append({"id": cells[0], "line": lineno, "cells": cells})
    if not rows:
        raise GateError("no SOURCES rows found (table missing or renamed)")
    return rows


def external_paths(url_cell: str) -> list[str]:
    stripped = URL.sub(" ", url_cell)
    seen, out = set(), []
    for match in ABSPATH.findall(stripped):
        norm = match.rstrip("/") or "/"
        if norm in seen:
            continue
        seen.add(norm)
        out.append(norm)
    return out


def inside(path: str, root: str) -> bool:
    root = os.path.normpath(root)
    path = os.path.normpath(path)
    return path == root or path.startswith(root + os.sep)


def digests_in(text: str) -> list[str]:
    return [m.group(1).lower() for m in HEX64.finditer(text)]


# ------------------------------------------------------------------- the checks


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_sidecar(path: str) -> list[tuple[str, str]]:
    """Parse `sha256sum`-style lines: <hex><space><space or *><name>."""
    entries = []
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            match = re.match(r"^([0-9a-fA-F]{64})\s+\*?(.+)$", line)
            if match:
                entries.append((match.group(1).lower(), match.group(2).strip()))
    return entries


def check_path(root: str, path: str, entry: dict | None, row_pins: list[str],
               map_present: bool) -> dict:
    """Evaluate one out-of-lane path.  Returns a result record."""
    def fail(reason: str, **extra) -> dict:
        return {"path": path, "ok": False, "reason": reason, **extra}

    if not map_present:
        return fail("map-missing")
    if entry is None:
        return fail("no-copy-named")

    copy = entry.get("copy")
    if not isinstance(copy, str) or not copy:
        return fail("entry-copy-not-a-string")
    if os.path.isabs(copy):
        return fail("copy-outside-lane", copy=copy)
    copy_abs = os.path.normpath(os.path.join(root, copy))
    if not inside(copy_abs, root):
        return fail("copy-outside-lane", copy=copy)
    if copy_abs == os.path.normpath(path):
        return fail("copy-is-the-external-path", copy=copy)
    if not os.path.exists(copy_abs):
        return fail("copy-missing", copy=copy)
    if not os.path.isfile(copy_abs):
        return fail("copy-not-a-regular-file", copy=copy)

    want = entry.get("sha256")
    if not isinstance(want, str) or not HEX64.fullmatch(want.strip()):
        return fail("map-digest-invalid", copy=copy)
    want = want.strip().lower()
    got = sha256_file(copy_abs)
    if got != want:
        return fail("copy-digest-mismatch", copy=copy, expected=want, actual=got)

    # Only a digest written in the same cell that names the path is taken as a
    # pin on those bytes.  Digests elsewhere in the row describe members or
    # derived artefacts (S035 pins member files, S082 the pacman fields), so they
    # cannot bind a directory archive and are not consulted here.
    scope = "url-cell" if row_pins else "none"
    if row_pins and want not in row_pins:
        return fail("row-pin-conflict", copy=copy, digest=want, row_pins=row_pins, scope=scope)

    sidecar = entry.get("sha256_file")
    if sidecar is not None:
        if not isinstance(sidecar, str) or not sidecar:
            return fail("sidecar-not-a-string", copy=copy)
        sidecar_abs = os.path.normpath(os.path.join(root, sidecar))
        if not inside(sidecar_abs, root):
            return fail("sidecar-outside-lane", copy=copy)
        if not os.path.isfile(sidecar_abs):
            return fail("sidecar-missing", copy=copy, sidecar=sidecar)
        pairs = parse_sidecar(sidecar_abs)
        if not pairs:
            return fail("sidecar-unparseable", copy=copy, sidecar=sidecar)
        names = {os.path.basename(copy_abs)}
        named = [dig for dig, name in pairs if os.path.basename(name) in names]
        if not named:
            return fail("sidecar-unnamed", copy=copy, sidecar=sidecar)
        if want not in named:
            return fail("sidecar-mismatch", copy=copy, sidecar=sidecar, sidecar_digests=named)

    kind = entry.get("kind")
    if kind is not None and kind not in ("file", "tree-archive"):
        return fail("map-kind-invalid", copy=copy, kind=kind)

    # Optional provenance: the digest the external source had when it was
    # captured.  Verified only when that source is a regular file on this host;
    # an absent or directory source is reported, never guessed.
    src_digest = entry.get("source_sha256")
    if src_digest is not None:
        if not isinstance(src_digest, str) or not HEX64.fullmatch(src_digest.strip()):
            return fail("map-source-digest-invalid", copy=copy)
        src_digest = src_digest.strip().lower()
        if os.path.isfile(path):
            actual_src = sha256_file(path)
            if actual_src != src_digest:
                return fail("source-digest-mismatch", copy=copy,
                            expected=src_digest, actual=actual_src)
            src_check = "file"
        elif os.path.isdir(path):
            src_check = "skipped-directory"
        else:
            src_check = "skipped-absent"
    else:
        src_check = "none"

    return {
        "path": path,
        "ok": True,
        "reason": "resolved",
        "copy": copy,
        "sha256": want,
        "kind": kind or "file",
        "row_pin_scope": scope,
        "source_digest_check": src_check,
    }


# ----------------------------------------------------------------------- driver


def load_map(root: str, map_rel: str) -> tuple[dict, bool]:
    map_abs = map_rel if os.path.isabs(map_rel) else os.path.join(root, map_rel)
    if not os.path.exists(map_abs):
        return {}, False
    try:
        with open(map_abs, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise GateError("cannot parse map %s: %s" % (map_abs, exc)) from exc
    if not isinstance(doc, dict):
        raise GateError("map %s: top level is not an object" % map_abs)
    version = doc.get("version")
    if version != 1:
        raise GateError("map %s: unsupported version %r (want 1)" % (map_abs, version))
    sources = doc.get("sources")
    if not isinstance(sources, dict):
        raise GateError("map %s: `sources` is not an object" % map_abs)
    for key, value in sources.items():
        if not isinstance(key, str) or not key.startswith("/"):
            raise GateError("map %s: key %r is not an absolute path" % (map_abs, key))
        if not isinstance(value, dict):
            raise GateError("map %s: entry for %r is not an object" % (map_abs, key))
        unknown = sorted(set(value) - ENTRY_KEYS)
        if unknown:
            raise GateError(
                "map %s: entry for %r has unknown key(s) %s (allowed: %s)"
                % (map_abs, key, ", ".join(unknown), ", ".join(sorted(ENTRY_KEYS)))
            )
    return sources, True


def evaluate(root: str, text: str, map_sources: dict, map_present: bool) -> dict:
    rows = parse_rows(text)
    records: list[dict] = []
    checked_rows = 0
    for row in rows:
        url_cell = row["cells"][1]
        paths = [p for p in external_paths(url_cell) if not inside(os.path.normpath(p), root)]
        if not paths:
            continue
        checked_rows += 1
        row_pins_url = digests_in(URL.sub(" ", url_cell))
        public = [u for u in URL.findall(url_cell) if u.lower().startswith(("http://", "https://"))]
        path_records = []
        for path in paths:
            norm = os.path.normpath(path)
            rec = check_path(root, norm, map_sources.get(path) or map_sources.get(norm),
                             row_pins_url, map_present)
            # Reported for every path, resolved or not: the pin scope is a
            # property of the row, not of the outcome.
            rec["row_pin_scope"] = "url-cell" if row_pins_url else "none"
            rec["url_cell_pins"] = row_pins_url
            rec["source_present"] = os.path.exists(norm)
            rec["cell_url"] = public[0] if public else None
            path_records.append(rec)
        records.append(
            {
                "id": row["id"],
                "line": row["line"],
                "ok": all(r["ok"] for r in path_records),
                "paths": path_records,
            }
        )
    failed = [r["id"] for r in records if not r["ok"]]
    return {
        "rows_total": len(rows),
        "rows_checked": checked_rows,
        "rows_failed": failed,
        "records": records,
        "exit": 1 if failed else 0,
    }


def render_text(result: dict, provenance: str, root: str, map_rel: str) -> str:
    out = []
    out.append("local-source-gate")
    out.append("  root       %s" % root)
    out.append("  table      %s" % provenance)
    out.append("  map        %s" % (map_rel if os.path.exists(
        map_rel if os.path.isabs(map_rel) else os.path.join(root, map_rel)) else "(absent)"))
    out.append("  rows       %d total, %d with an out-of-lane URL cell"
               % (result["rows_total"], result["rows_checked"]))
    if not result["rows_checked"]:
        out.append("  verdict    PASS (no out-of-lane URL cells)")
        return "\n".join(out)
    for record in result["records"]:
        head = "%s  %s" % ("FAIL" if not record["ok"] else "ok  ", record["id"])
        first = True
        for rec in record["paths"]:
            line = "  %s %s" % (head if first else " " * len(head), rec["path"])
            first = False
            if rec["ok"]:
                extra = "" if rec.get("copy") is None else "  <- %s" % rec["copy"]
                src = "" if rec.get("source_digest_check") in (None, "none") else "  src[%s]" % rec["source_digest_check"]
                out.append("%s  [%s/%s]%s%s" % (line, rec["reason"], rec.get("row_pin_scope", "n/a"), extra, src))
            else:
                bits = ["[%s]" % rec["reason"]]
                if "expected" in rec:
                    bits.append("expected %s actual %s" % (rec["expected"][:12], rec["actual"][:12]))
                if "row_pins" in rec:
                    bits.append("row pins %s" % ",".join(p[:12] for p in rec["row_pins"]))
                if "sidecar" in rec:
                    bits.append("sidecar %s" % rec["sidecar"])
                if not rec.get("source_present"):
                    bits.append("source absent on this host")
                if rec.get("url_cell_pins"):
                    bits.append("url-cell pins %s" % ",".join(p[:12] for p in rec["url_cell_pins"]))
                if rec.get("cell_url"):
                    bits.append("cell has a public URL %s" % rec["cell_url"])
                else:
                    bits.append("no public URL in the same cell")
                out.append("%s  %s" % (line, "  ".join(bits)))
    out.append("  verdict    %s (rows: %s)" % (
        "FAIL" if result["exit"] else "PASS",
        ", ".join(result["rows_failed"]) if result["rows_failed"] else "none"))
    return "\n".join(out)


def run_gate(args) -> int:
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print("local-source-gate: --root %s is not a directory" % root, file=sys.stderr)
        return 2
    try:
        text, provenance = read_sources(root, args.rev, args.sources)
        map_sources, map_present = load_map(root, args.map)
        result = evaluate(root, text, map_sources, map_present)
    except GateError as exc:
        print("local-source-gate: %s" % exc, file=sys.stderr)
        return 2
    if args.json:
        doc = {
            "root": root,
            "table": provenance,
            "table_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "map": args.map,
            "map_present": map_present,
            **result,
        }
        print(json.dumps(doc, indent=2, sort_keys=True))
    else:
        print(render_text(result, provenance, root, args.map))
    return result["exit"]


# --------------------------------------------------------------------- selftest

SELFTEST_ROWS_HEAD = """# SOURCES test fixture

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
"""


def _row(sid: str, source: str, anchor: str = "anchor text", status: str = "mined") -> str:
    return "| %s | %s | own-work | A | scope | %s | teaches | %s | 2026-01-01 | 180d | none |\n" % (
        sid, source, anchor, status)


def selftest() -> int:
    import shutil
    import tempfile

    cases = []
    runs: list[tuple[int, str, str]] = []
    bases: list[str] = []

    def fixture(name: str, rows: list[str], files: dict[str, bytes], map_doc: str | None) -> str:
        base = os.path.join(tempfile.mkdtemp(prefix="lsg-%s-" % name, dir=os.environ.get("TMPDIR") or None))
        root = os.path.join(base, "lane")
        os.makedirs(os.path.join(root, "corpus"))
        with open(os.path.join(root, "corpus", "SOURCES.md"), "w", encoding="utf-8") as fh:
            fh.write(SELFTEST_ROWS_HEAD + "".join(rows))
        for rel, payload in files.items():
            dest = os.path.join(root, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as fh:
                fh.write(payload)
        if map_doc is not None:
            mpath = os.path.join(root, DEFAULT_MAP_REL)
            os.makedirs(os.path.dirname(mpath), exist_ok=True)
            with open(mpath, "w", encoding="utf-8") as fh:
                fh.write(map_doc)
        bases.append(base)
        return root, base

    def run(root: str, *extra: str) -> tuple[int, str, str]:
        # Every case calls run() immediately before its expect(); results are
        # paired positionally with `cases` below.
        proc = subprocess.run(
            [sys.executable, os.path.abspath(__file__), "--root", root, *extra],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        result = (proc.returncode, proc.stdout, proc.stderr)
        runs.append(result)
        return result

    payload = b"external-bytes\n"
    digest = hashlib.sha256(payload).hexdigest()
    ext = "/nonexistent/external/source.tsv"

    def expect(name: str, want: int, needle: str):
        cases.append((name, want, needle))

    # 1: no map at all -> red, row named.
    root, base = fixture("nomap", [_row("S900", ext)], {}, None)
    code, out, _ = run(root)
    expect("no-map-is-red", 1, "FAIL  S900")
    # 2: valid copy + digest -> green.
    root, base = fixture("green", [_row("S900", ext)], {"corpus/evidence/x.tsv": payload},
                         json.dumps({"version": 1, "sources": {ext: {"copy": "corpus/evidence/x.tsv",
                                                                     "sha256": digest}}}))
    code, out, _ = run(root)
    expect("copy-and-map-is-green", 0, "PASS")
    # 3: digest mismatch -> red.
    root, base = fixture("dig", [_row("S900", ext)], {"corpus/evidence/x.tsv": payload},
                         json.dumps({"version": 1, "sources": {ext: {"copy": "corpus/evidence/x.tsv",
                                                                     "sha256": "0" * 64}}}))
    code, out, _ = run(root)
    expect("digest-mismatch-is-red", 1, "copy-digest-mismatch")
    # 4: copy path escaping the root -> red.
    root, base = fixture("escape", [_row("S900", ext)], {"corpus/evidence/x.tsv": payload},
                         json.dumps({"version": 1, "sources": {ext: {"copy": "../../etc/passwd",
                                                                     "sha256": digest}}}))
    code, out, _ = run(root)
    expect("copy-escape-is-red", 1, "copy-outside-lane")
    # 5: absolute copy path -> red.
    root, base = fixture("abs", [_row("S900", ext)], {"corpus/evidence/x.tsv": payload},
                         json.dumps({"version": 1, "sources": {ext: {"copy": "/tmp/x.tsv",
                                                                     "sha256": digest}}}))
    code, out, _ = run(root)
    expect("absolute-copy-is-red", 1, "copy-outside-lane")
    # 6: row pins a different digest than the map -> red.
    root, base = fixture("pin", [_row("S900", "%s (sha256 %s)" % (ext, "a" * 64))],
                         {"corpus/evidence/x.tsv": payload},
                         json.dumps({"version": 1, "sources": {ext: {"copy": "corpus/evidence/x.tsv",
                                                                     "sha256": digest}}}))
    code, out, _ = run(root)
    expect("row-pin-conflict-is-red", 1, "row-pin-conflict")
    # 7: row pin matching the map -> green.
    root, base = fixture("pinok", [_row("S900", "%s (sha256 %s)" % (ext, digest))],
                         {"corpus/evidence/x.tsv": payload},
                         json.dumps({"version": 1, "sources": {ext: {"copy": "corpus/evidence/x.tsv",
                                                                     "sha256": digest}}}))
    code, out, _ = run(root)
    expect("row-pin-agrees-is-green", 0, "PASS")
    # 8: in-lane absolute path and https URLs are not flagged.
    root, base = fixture("inlane", [_row("S902", "https://example.org/a/b.md")], {}, None)
    with open(os.path.join(root, "corpus", "SOURCES.md"), "a", encoding="utf-8") as fh:
        fh.write(_row("S901", "%s/corpus/x.md" % root))
    code, out, _ = run(root)
    expect("in-lane-and-url-ignored", 0, "no out-of-lane URL cells")
    # 9: prose slashes are not paths.
    root, base = fixture("prose", [_row("S903", "envelope `operation`/provider.id pair")], {}, None)
    code, out, _ = run(root)
    expect("prose-slash-ignored", 0, "no out-of-lane URL cells")
    # 10: multi-path row, only one mapped -> red, names both.
    root, base = fixture("multi", [_row("S904", "%s and %s" % (ext, ext + "2"))],
                         {"corpus/evidence/x.tsv": payload},
                         json.dumps({"version": 1, "sources": {ext: {"copy": "corpus/evidence/x.tsv",
                                                                     "sha256": digest}}}))
    code, out, _ = run(root)
    expect("half-mapped-row-is-red", 1, "no-copy-named")
    # 11: sidecar mismatch -> red.
    root, base = fixture("side", [_row("S900", ext)],
                         {"corpus/evidence/x.tsv": payload,
                          "corpus/evidence/x.tsv.sha256": (("%s  x.tsv\n" % ("b" * 64)).encode())},
                         json.dumps({"version": 1, "sources": {ext: {
                             "copy": "corpus/evidence/x.tsv", "sha256": digest,
                             "sha256_file": "corpus/evidence/x.tsv.sha256"}}}))
    code, out, _ = run(root)
    expect("sidecar-mismatch-is-red", 1, "sidecar-mismatch")
    # 12: valid sidecar -> green.
    root, base = fixture("sideok", [_row("S900", ext)],
                         {"corpus/evidence/x.tsv": payload,
                          "corpus/evidence/x.tsv.sha256": (("%s  x.tsv\n" % digest).encode())},
                         json.dumps({"version": 1, "sources": {ext: {
                             "copy": "corpus/evidence/x.tsv", "sha256": digest,
                             "sha256_file": "corpus/evidence/x.tsv.sha256"}}}))
    code, out, _ = run(root)
    expect("sidecar-agrees-is-green", 0, "PASS")
    # 13: copy is a directory -> red.
    root, base = fixture("dir", [_row("S900", ext)], {"corpus/evidence/d/keep": payload},
                         json.dumps({"version": 1, "sources": {ext: {"copy": "corpus/evidence/d",
                                                                     "sha256": digest}}}))
    code, out, _ = run(root)
    expect("copy-must-be-a-file", 1, "copy-not-a-regular-file")
    # 14: malformed map -> exit 2.
    root, base = fixture("badmap", [_row("S900", ext)], {}, "{not json")
    code, out, _ = run(root)
    expect("malformed-map-is-exit2", 2, "")
    # 15: wrong table arity -> exit 2.
    root, base = fixture("arity", ["| S999 | only | three |\n"], {}, None)
    code, out, _ = run(root)
    expect("bad-arity-is-exit2", 2, "")
    # 16: unresolved row that also carries a public URL is reported re-derivable.
    root, base = fixture("rederive", [_row("S905", "%s and https://example.org/pin" % ext)], {}, None)
    code, out, _ = run(root)
    expect("cell-url-annotation", 1, "cell has a public URL https://example.org/pin")
    # 17: --rev reads the committed table, not the mutated working tree.
    root, base = fixture("rev", [_row("S900", "%s (sha256 %s)" % (ext, digest))],
                         {"corpus/evidence/x.tsv": payload},
                         json.dumps({"version": 1, "sources": {ext: {"copy": "corpus/evidence/x.tsv",
                                                                     "sha256": digest}}}))
    for argv in (["init", "-q"], ["add", "-A"],
                 ["-c", "user.name=fx", "-c", "user.email=fx@fx", "commit", "-qm", "fixture"]):
        subprocess.run(["git", "-C", root, *argv], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    top = subprocess.run(["git", "-C", root, "rev-parse", "--show-toplevel"],
                         check=True, stdout=subprocess.PIPE, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(root), (top, root)
    code, out, _ = run(root)
    expect("rev-fixture-green-on-disk", 0, "PASS")
    with open(os.path.join(root, "corpus", "SOURCES.md"), "w", encoding="utf-8") as fh:
        fh.write(SELFTEST_ROWS_HEAD + _row("S900", ext + "2"))
    code, out, _ = run(root)
    expect("mutated-working-tree-is-red", 1, "no-copy-named")
    code, out, _ = run(root, "--rev", "HEAD")
    expect("rev-reads-committed-table", 0, "PASS")
    # 18: an unknown map key is a map error, not a silently ignored typo.
    root, base = fixture("key", [_row("S900", ext)], {"corpus/evidence/x.tsv": payload},
                         json.dumps({"version": 1, "sources": {ext: {
                             "copy": "corpus/evidence/x.tsv", "sha256": digest,
                             "sha_256": digest}}}))
    code, out, _ = run(root)
    expect("unknown-map-key-is-exit2", 2, "")
    # 19/20: source_sha256 binds the copy to the live source bytes.
    root, base = fixture("src", [], {"corpus/evidence/x.tsv": payload}, None)
    srcfile = os.path.join(base, "external", "source.tsv")
    os.makedirs(os.path.dirname(srcfile), exist_ok=True)
    with open(srcfile, "wb") as fh:
        fh.write(payload)
    with open(os.path.join(root, "corpus", "SOURCES.md"), "a", encoding="utf-8") as fh:
        fh.write(_row("S906", srcfile))
    map_path = os.path.join(root, DEFAULT_MAP_REL)
    with open(map_path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"version": 1, "sources": {srcfile: {
            "copy": "corpus/evidence/x.tsv", "sha256": digest, "source_sha256": digest}}}))
    code, out, _ = run(root)
    expect("source-digest-agrees-is-green", 0, "src[file]")
    with open(map_path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"version": 1, "sources": {srcfile: {
            "copy": "corpus/evidence/x.tsv", "sha256": digest, "source_sha256": "c" * 64}}}))
    code, out, _ = run(root)
    expect("source-digest-mismatch-is-red", 1, "source-digest-mismatch")
    # 21: a digest outside the URL cell does not bind the copy.
    root, base = fixture("wide", [_row("S907", ext, anchor="member sha256 " + "d" * 64)],
                         {"corpus/evidence/x.tsv": payload},
                         json.dumps({"version": 1, "sources": {ext: {"copy": "corpus/evidence/x.tsv",
                                                                     "sha256": digest}}}))
    code, out, _ = run(root)
    expect("row-wide-digest-does-not-bind", 0, "[resolved/none]")

    failures = 0
    if len(cases) != len(runs):
        print("selftest: %d cases but %d runs (harness bug)" % (len(cases), len(runs)))
        return 1
    for (name, want, needle), (code, out, err) in zip(cases, runs):
        ok = code == want and (needle in out or needle == "")
        print("%-34s %s  want=%d got=%d" % (name, "PASS" if ok else "FAIL", want, code))
        if not ok:
            failures += 1
            print("    stdout: %s" % out.replace("\n", "\\n")[:400])
            print("    stderr: %s" % err.replace("\n", "\\n")[:400])
    for base in bases:
        shutil.rmtree(base, ignore_errors=True)
    print("selftest: %d/%d cases" % (len(cases) - failures, len(cases)))
    return 0 if failures == 0 else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="List SOURCES rows whose URL cell is an out-of-lane local path "
                    "and require an in-lane copy with a matching digest.")
    parser.add_argument("--root", required=False, default=".",
                        help="lane root that must contain corpus/SOURCES.md")
    parser.add_argument("--rev", default=None,
                        help="git revision to read corpus/SOURCES.md from "
                             "(default: read the working tree)")
    parser.add_argument("--sources", default=None,
                        help="read this SOURCES.md instead of the tree or a revision")
    parser.add_argument("--map", default=DEFAULT_MAP_REL,
                        help="sidecar map, relative to --root (default %s)" % DEFAULT_MAP_REL)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--selftest", action="store_true", help="run the built-in fixture suite")
    args = parser.parse_args(argv[1:])
    if args.selftest:
        return selftest()
    if not args.root:
        parser.error("--root is required")
    return run_gate(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv))

