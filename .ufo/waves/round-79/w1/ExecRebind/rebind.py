#!/usr/bin/env python3
"""Independent re-derivation of R79-C2 (ExecRebind seat).

Re-implemented from the frozen claim text, not from `tools/round-79/pointer-bind.py`
(no import, no copy of its parse table).  Reads `PROVINCE.md` at `--rev` via
`git show`, extracts the five drift-prone pointer cells it names:

  * three REA pins      ``rea-agents@<version>`` next to a ``<path>:<line>`` pointer
  * Ghidra              ``application.version=<v>`` next to an
                        ``.../Ghidra/application.properties:<line>`` pointer
  * .bashrc export range: the ``.bashrc:<start>-<end>`` cell in the sentence that
                        declares ``GHIDRA_INSTALL_DIR=`` and ``JAVA_HOME=``

Each cell is then bound against the LIVE file the pointer names (``~`` expanded,
1-based inclusive range): every declared token must occur on a line inside the
declared range.  The receipt keeps the pointed lines' sha256 only, never bytes.

Exit 0 iff all five bound; 1 on any mismatch/unparsed; 2 if the record is
unreadable at the requested revision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

RECORD = "PROVINCE.md"

# Client-scoped, bounded and non-greedy so the lead-in sentence on the first
# paragraph ("and Kimi all pin `rea-agents@...`") cannot steal another client's
# pointer.  Only the adjacency `pin` + `(pointer)` counts.
PIN_RE = re.compile(
    r"\b(Devin|OMP|Kimi)\b"
    r"(?:(?!\b(?:Devin|OMP|Kimi)\b)[\s\S]){0,200}?"
    r"`rea-agents@(?P<pin>[0-9][0-9.]*)`\s*"
    r"\(`(?P<pointer>[^`\s]+?:\d+(?:-\d+)?)`\)"
)

GHIDRA_PTR_RE = re.compile(r"`([^`\s]*Ghidra/application\.properties):(\d+)`")
GHIDRA_VALUE_RE = re.compile(r"application\.version=([0-9][0-9.]*)")

BASHRC_PTR_RE = re.compile(r"`([^`\s]*\.bashrc):(\d+)(?:-(\d+))?`")
BASHRC_TOKENS = ("GHIDRA_INSTALL_DIR=", "JAVA_HOME=")

POINTER_RE = re.compile(r"^(?P<path>.+?):(?P<start>\d+)(?:-(?P<end>\d+))?$");


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_show(root: str, rev: str, path: str) -> bytes | None:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def extract_cells(text: str) -> tuple[list[dict], list[str]]:
    """Return the five declared cells; ids that do not parse are listed apart."""
    cells: list[dict] = []
    unparsed: list[str] = []

    found: dict[str, tuple[str, str]] = {}
    for match in PIN_RE.finditer(text):
        found.setdefault(match.group(1), (match.group("pin"), match.group("pointer")))
    for client, cid in (("Devin", "devin-pin"), ("OMP", "omp-pin"),
                        ("Kimi", "kimi-pin")):
        if client not in found:
            unparsed.append(cid)
            cells.append({"id": cid, "pointer": "", "tokens": []})
            continue
        pin, pointer = found[client]
        cells.append({"id": cid, "pointer": pointer, "tokens": [f"rea-agents@{pin}"]})

    # Paragraph-scoped (blank-line blocks): the "Reverified Ghidra/JDK" paragraph
    # declares the version value, the properties pointer and both export names.
    paragraphs = re.split(r"\n[ \t]*\n", text)
    ghidra_cell = None
    for paragraph in paragraphs:
        pointer = GHIDRA_PTR_RE.search(paragraph)
        value = GHIDRA_VALUE_RE.search(paragraph)
        if pointer and value:
            ghidra_cell = (f"{pointer.group(1)}:{pointer.group(2)}",
                           f"application.version={value.group(1)}")
            break
    if ghidra_cell is None:
        unparsed.append("ghidra-version")
        cells.append({"id": "ghidra-version", "pointer": "", "tokens": []})
    else:
        cells.append({"id": "ghidra-version", "pointer": ghidra_cell[0],
                      "tokens": [ghidra_cell[1]]})

    # The export-range cell is the .bashrc pointer sharing a sentence with both
    # export names (the record also cites the REA key block with other ranges).
    bashrc_cell = None
    for paragraph in paragraphs:
        if not all(token in paragraph for token in BASHRC_TOKENS):
            continue
        pointer = BASHRC_PTR_RE.search(paragraph)
        if pointer:
            ptr = f"{pointer.group(1)}:{pointer.group(2)}"
            if pointer.group(3):
                ptr += f"-{pointer.group(3)}"
            bashrc_cell = ptr
            break
    if bashrc_cell is None:
        unparsed.append("bashrc-exports")
        cells.append({"id": "bashrc-exports", "pointer": "", "tokens": []})
    else:
        cells.append({"id": "bashrc-exports", "pointer": bashrc_cell,
                      "tokens": list(BASHRC_TOKENS)})
    return cells, unparsed


def read_file_lines(path: str) -> list[str] | None:
    try:
        with open(os.path.abspath(os.path.expanduser(path)),
                  encoding="utf-8", errors="replace") as handle:
            return handle.readlines()
    except OSError:
        return None


def bind(cell: dict) -> dict:
    out = {
        "id": cell["id"],
        "pointer": cell["pointer"],
        "tokens": cell["tokens"],
        "path": "",
        "line_start": None,
        "line_end": None,
        "matched": False,
        "unparsed": False,
        "reason": "",
        "line_sha256": "",
    }
    if not cell["pointer"]:
        out["unparsed"] = True
        out["reason"] = "the record cell does not parse"
        return out

    match = POINTER_RE.match(cell["pointer"])
    if not match:
        out["unparsed"] = True
        out["reason"] = "pointer carries no line number"
        return out
    start, end = int(match.group("start")), int(match.group("end") or match.group("start"))
    out["path"] = os.path.abspath(os.path.expanduser(match.group("path")))
    out["line_start"], out["line_end"] = start, end
    if start < 1 or end < start:
        out["reason"] = f"line range {start}-{end} is not a forward 1-based range"
        return out

    lines = read_file_lines(out["path"])
    if lines is None:
        out["reason"] = f"path {match.group('path')} does not exist"
        return out
    if end > len(lines):
        out["reason"] = (f"line range {start}-{end} runs past end of file "
                         f"({len(lines)} lines)")
        return out

    pointed = lines[start - 1:end]
    out["line_sha256"] = sha256("".join(pointed).encode("utf-8"))
    missing = [token for token in cell["tokens"]
               if not any(token in line for line in pointed)]
    if missing:
        where = str(start) if start == end else f"{start}-{end}"
        out["reason"] = f"token {missing[0]!r} is not on line {where}"
        return out
    out["matched"] = True
    return out


def evaluate(text: str, rev: str, record_sha: str, control: str | None) -> dict:
    cells, unparsed = extract_cells(text)
    checks: list[dict] = []
    for cell in cells:
        if control == "path-only":
            exists = (read_file_lines(cell["pointer"].rsplit(":", 1)[0])
                      is not None) if cell["pointer"] else False
            checks.append({
                "id": cell["id"], "pointer": cell["pointer"],
                "tokens": cell["tokens"],
                "path": os.path.abspath(os.path.expanduser(
                    cell["pointer"].rsplit(":", 1)[0])) if cell["pointer"] else "",
                "line_start": None, "line_end": None,
                "matched": exists, "unparsed": False,
                "reason": "" if exists else "path does not exist",
                "line_sha256": "",
            })
        else:
            checks.append(bind(cell))
    matched = sum(1 for c in checks if c["matched"])
    return {
        "rev": rev,
        "record_sha256": record_sha,
        "control": control,
        "checks_total": len(checks),
        "matched": matched,
        "mismatches": len(checks) - matched,
        "unparsed": len(unparsed),
        "mismatch_ids": [c["id"] for c in checks if not c["matched"]],
        "unparsed_ids": unparsed,
        "checks": checks,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True, help="lane repo")
    ap.add_argument("--rev", default="", help="revision whose PROVINCE.md is read")
    ap.add_argument("--record-file", default="",
                    help="read the record from this file instead of --rev (controls)")
    ap.add_argument("--control", choices=("path-only",), default=None)
    ap.add_argument("--json-out", default="")
    args = ap.parse_args(argv)

    if args.record_file:
        try:
            with open(args.record_file, "rb") as handle:
                blob = handle.read()
        except OSError as exc:
            print(f"unevaluable: {exc}", file=sys.stderr)
            return 2
        rev = f"file:{args.record_file}"
    else:
        if not args.rev:
            print("unevaluable: --rev or --record-file required", file=sys.stderr)
            return 2
        blob = git_show(args.root, args.rev, RECORD)
        if blob is None:
            print(f"unevaluable: {RECORD} absent at {args.rev}", file=sys.stderr)
            return 2
        rev = args.rev

    receipt = evaluate(blob.decode("utf-8"), rev, sha256(blob), args.control)
    receipt["schema"] = "exec-rebind-r79-c2-v1"
    receipt["ok"] = bool(receipt["checks_total"] == 5
                         and receipt["matched"] == 5
                         and receipt["unparsed"] == 0)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            json.dump(receipt, handle, indent=1, sort_keys=True)
            handle.write("\n")
    print(json.dumps(receipt, indent=1, sort_keys=True))
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
