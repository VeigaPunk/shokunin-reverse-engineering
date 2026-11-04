#!/usr/bin/env python3
"""Round-80 pointer binding: exact tokens, and a duplicate cell is a defect.

`PROVINCE.md` names drift-prone live objects with `path:line` pointers.  Round
79 bound each pointer to the token it claims, but it matched that token with a
bare substring test and collapsed duplicate cells in a dict comprehension, so a
longer live token (`rea-agents@6.7.05`) satisfied a shorter declared pin
(`rea-agents@6.7.0`) and a record naming the same client twice silently kept
the last cell.  This revision keeps round 79's surface and exit contract and
changes the two rules:

  exact token     a declared token binds only when *every* occurrence in the
                  pointed lines is delimited on both sides — start/end of the
                  pointed slice, or a character outside `[A-Za-z0-9._-]`.  A
                  refusal names the longer token it found.
  duplicate cell  every declared cell is counted (a second OMP cell is a sixth
                  check, not a replacement), each cell is bound independently,
                  and the receipt carries the duplicated check id in
                  `duplicates`.  `ok` is false while `duplicates` is non-empty.

The receipt keeps the pointed slice's sha256, never its bytes.

Module API for the round-80 strictness battery:

    bind(pointer, tokens, lines) -> {"matched": bool, "delimiter_evidence": [...]}
    parse_record(text) -> (checks, unparsed, duplicates)
        checks      one dict per declared cell, cells grouped per client in
                    record order (a duplicated client contributes every cell)
        unparsed    check ids with no parsable cell
        duplicates  check ids declared more than once, each still in `checks`

Modes (round 79's CLI, unchanged):

    --battery   bind every check at --rev against the live files; write a
                receipt (the default mode whenever --rev is supplied: the
                frozen counting command omits this flag, and a printed command
                must run as printed).
    --selftest  unit cases, one red per failure shape plus the look-alikes.
    --validate  re-derive a receipt's counts from its own check list.
    --control   `path-only`: round 78's rule (the path exists, the line is not
                read) — recorded to show it cannot fail on a moved line.

Exit: 0 every check bound and no duplicate; 1 otherwise; 2 could-not-evaluate.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

ROUND = 80
PROVINCE = "PROVINCE.md"
INSTRUMENT_PATH = "tools/round-80/pointer-bind.py"
PREDICATE = (
    "R80-C1 is verified iff `tools/round-80/strictness-battery.py` scores the "
    "candidate binder and the round-79 control binder on the four frozen red "
    "fixtures and two green controls (cases 4, green_cases 2, "
    "candidate_false_greens 0, control_false_greens 4, candidate_green_refusals "
    "0, control_green_refusals 0) and `tools/round-80/pointer-bind.py --root . "
    "--rev <measured> --json-out <live>` exits 0 with `checks_total 5`, "
    "`matched 5`, `mismatches 0`, `unparsed 0` and `duplicates []`."
)

RE_PIN = re.compile(r"(Devin|OMP|Kimi)\s+`rea-agents@([0-9][0-9.]*)`\s*\(`([^`]+)`\)")
RE_GHIDRA_PTR = re.compile(r"`([^`]*Ghidra/application\.properties):(\d+)`")
RE_GHIDRA_VALUE = re.compile(r"application\.version=([0-9][0-9.]*)")
RE_BASHRC_PTR = re.compile(r"`([^`]*\.bashrc):(\d+)(?:-(\d+))?`")
RE_POINTER = re.compile(r"^(?P<path>.+?):(?P<start>\d+)(?:-(?P<end>\d+))?$")

BASHRC_TOKENS = ("GHIDRA_INSTALL_DIR=", "JAVA_HOME=")

# A token character: the delimiters a strict binding requires outside the match.
TOKEN_CHARS = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-")
# `@` is a delimiter, but it is part of a package pin's shape, so a refusal
# reports the whole `name@version` run that swallowed the declared token.
REPORT_CHARS = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-@")

# The live object each cell must name (round 78's `same_path` rule, kept).
DECLARED = {
    "devin-pin": "/home/vgpnk/.config/devin/mcp_config.json",
    "omp-pin": "/home/vgpnk/.omp/agent/mcp.json",
    "kimi-pin": "~/.kimi-code/config.toml",
    "ghidra-version": "<GHIDRA_INSTALL_DIR>/Ghidra/application.properties",
    "bashrc-exports": "/home/vgpnk/.bashrc",
}

PIN_CLIENTS = (("Devin", "devin-pin"), ("OMP", "omp-pin"), ("Kimi", "kimi-pin"))


def ghidra_dir() -> str:
    """The installed Ghidra root: the live env var, else the .bashrc export."""
    env = os.environ.get("GHIDRA_INSTALL_DIR")
    if env:
        return env
    for line in read_lines("/home/vgpnk/.bashrc") or []:
        match = re.search(r"""export\s+GHIDRA_INSTALL_DIR=["']?([^"'\s]+)""", line)
        if match:
            return os.path.expandvars(os.path.expanduser(match.group(1)))
    return ""


def declared_ok(check_id: str, path: str) -> bool:
    want = DECLARED.get(check_id)
    if want is None:
        return False
    if want.startswith("<GHIDRA_INSTALL_DIR>"):
        root = ghidra_dir()
        if not root:
            return False
        want = want.replace("<GHIDRA_INSTALL_DIR>", root)
    return os.path.realpath(expand(path)) == os.path.realpath(expand(want))


class Unevaluable(Exception):
    """Exit-2 class: the battery cannot read the record."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_show(root: str, rev: str, path: str) -> bytes | None:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def is_commit_sha(text: object) -> bool:
    """A receipt stores a resolved 40-hex commit, never a symbolic name."""
    return (isinstance(text, str) and len(text) == 40
            and all(character in "0123456789abcdef" for character in text))


def resolve_rev(root: str, rev: str) -> str:
    """The 40-hex commit `rev` names; a receipt never stores a symbolic name."""
    proc = subprocess.run(
        ["git", "-C", root, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}"],
        capture_output=True, text=True)
    resolved = proc.stdout.strip()
    if proc.returncode != 0 or not is_commit_sha(resolved):
        raise Unevaluable(f"rev {rev!r} does not resolve to a commit")
    return resolved


def expand(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


def find_occurrences(line: str, token: str) -> list[dict]:
    """Every substring occurrence, with its two delimiter characters."""
    found: list[dict] = []
    start = 0
    while True:
        index = line.find(token, start)
        if index < 0:
            return found
        end = index + len(token)
        before = line[index - 1] if index > 0 else ""
        after = line[end] if end < len(line) else ""
        found.append({
            "index": index,
            "before": before,
            "after": after,
            "delimited": ((not before or before not in TOKEN_CHARS)
                          and (not after or after not in TOKEN_CHARS)),
            "longer": longer_token(line, index, end),
        })
        start = index + 1


def longer_token(line: str, start: int, end: int) -> str:
    """The maximal `[A-Za-z0-9._-@]` run around a match, for the refusal."""
    left = start
    while left > 0 and line[left - 1] in REPORT_CHARS:
        left -= 1
    right = end
    while right < len(line) and line[right] in REPORT_CHARS:
        right += 1
    return line[left:right]


def bind(pointer: str, tokens: list[str], lines: list[str] | None) -> dict:
    """Bind one pointer to its tokens; no I/O, so the selftest can inject lines."""
    out = {"pointer": pointer, "tokens": list(tokens), "path": "",
           "line_start": None, "line_end": None, "matched": False,
           "unparsed": False, "reason": "", "line_sha256": "",
           "delimiter_evidence": []}
    match = RE_POINTER.match(pointer)
    if not match:
        out["unparsed"] = True
        out["reason"] = "pointer carries no line number"
        return out
    out["path"] = match.group("path")
    start = int(match.group("start"))
    end = int(match.group("end") or start)
    out["line_start"], out["line_end"] = start, end
    span = str(start) if start == end else f"{start}-{end}"
    if start < 1 or end < start:
        out["reason"] = f"line range {start}-{end} is not a forward 1-based range"
        return out
    if lines is None:
        out["reason"] = f"path {match.group('path')} does not exist"
        return out
    if end > len(lines):
        out["reason"] = (f"line range {start}-{end} runs past end of file "
                         f"({len(lines)} lines)")
        return out
    pointed = lines[start - 1:end]
    out["line_sha256"] = sha256_bytes("".join(pointed).encode("utf-8"))
    evidence: list[dict] = []
    for token in tokens:
        occurrences: list[dict] = []
        for number, line in enumerate(pointed, start):
            for found in find_occurrences(line, token):
                found["line"] = number
                occurrences.append(found)
        if not occurrences:
            evidence.append({"token": token, "occurrences": 0,
                             "delimited": False,
                             "reason": f"token {token!r} is not on line {span}"})
            out["delimiter_evidence"] = evidence
            out["reason"] = evidence[-1]["reason"]
            return out
        undelimited = [item for item in occurrences if not item["delimited"]]
        if undelimited:
            longer = undelimited[0]["longer"]
            evidence.append({
                "token": token,
                "occurrences": len(occurrences),
                "delimited": False,
                "reason": (f"token {token!r} occurs inside the longer token "
                           f"{longer!r} on line {undelimited[0]['line']}"),
            })
            out["delimiter_evidence"] = evidence
            out["reason"] = evidence[-1]["reason"]
            return out
        evidence.append({"token": token, "occurrences": len(occurrences),
                         "delimited": True, "reason": ""})
    out["delimiter_evidence"] = evidence
    out["matched"] = True
    return out


def read_lines(path: str) -> list[str] | None:
    try:
        with open(expand(path), encoding="utf-8", errors="replace") as handle:
            return handle.readlines()
    except OSError:
        return None


def parse_record(text: str) -> tuple[list[dict], list[str], list[str]]:
    """Extract every declared pointer cell; return the duplicated check ids.

    A client declared twice contributes two cells with the same id, so the
    caller's `checks_total` counts both and neither cell can be last-wins.
    """
    checks: list[dict] = []
    unparsed: list[str] = []
    duplicates: list[str] = []
    cells: dict[str, list[tuple[str, str]]] = {}
    for found in RE_PIN.finditer(text):
        cells.setdefault(found.group(1), []).append(
            (found.group(2), found.group(3)))
    for client, check_id in PIN_CLIENTS:
        declared = cells.get(client, [])
        if not declared:
            unparsed.append(check_id)
            checks.append({"id": check_id, "pointer": "", "tokens": [], "cell": 0})
            continue
        if len(declared) > 1:
            duplicates.append(check_id)
        for number, (pin, pointer) in enumerate(declared, 1):
            checks.append({"id": check_id, "pointer": pointer,
                           "tokens": [f"rea-agents@{pin}"], "cell": number})
    ghidra_ptr = RE_GHIDRA_PTR.search(text)
    ghidra_value = RE_GHIDRA_VALUE.search(text)
    if not (ghidra_ptr and ghidra_value):
        unparsed.append("ghidra-version")
        checks.append({"id": "ghidra-version", "pointer": "", "tokens": [],
                       "cell": 0})
    else:
        checks.append({"id": "ghidra-version",
                       "pointer": f"{ghidra_ptr.group(1)}:{ghidra_ptr.group(2)}",
                       "tokens": [f"application.version={ghidra_value.group(1)}"],
                       "cell": 1})
    bashrc = RE_BASHRC_PTR.search(text)
    if not bashrc:
        unparsed.append("bashrc-exports")
        checks.append({"id": "bashrc-exports", "pointer": "", "tokens": [],
                       "cell": 0})
    else:
        pointer = f"{bashrc.group(1)}:{bashrc.group(2)}"
        if bashrc.group(3):
            pointer += f"-{bashrc.group(3)}"
        checks.append({"id": "bashrc-exports", "pointer": pointer,
                       "tokens": list(BASHRC_TOKENS), "cell": 1})
    return checks, unparsed, duplicates


def bounded(checks_total: int, matched: int, unparsed: int,
            duplicates: list[str]) -> bool:
    """Round 79's 5/5 verdict, plus the duplicate-cell condition."""
    return bool(checks_total == 5 and matched == checks_total
                and unparsed == 0 and not duplicates)


def ok_under(control: str | None, bound_ok: bool) -> bool:
    return bool(bound_ok and control is None)


def battery(root: str, rev: str, control: str | None) -> dict:
    resolved = resolve_rev(root, rev)
    blob = git_show(root, resolved, PROVINCE)
    if blob is None:
        raise Unevaluable(f"{PROVINCE} absent at {resolved}")
    checks, _, duplicates = parse_record(blob.decode("utf-8"))
    results: list[dict] = []
    for check in checks:
        if not check["pointer"]:
            results.append({"id": check["id"], "cell": check.get("cell", 0),
                            "pointer": "", "tokens": [],
                            "path": "", "line_start": None, "line_end": None,
                            "matched": False, "unparsed": True,
                            "reason": "the record cell does not parse",
                            "line_sha256": "", "delimiter_evidence": []})
            continue
        lines = read_lines(check["pointer"].rsplit(":", 1)[0])
        if control == "path-only":
            exists = lines is not None
            entry = {"id": check["id"], "cell": check.get("cell", 1),
                     "pointer": check["pointer"],
                     "tokens": check["tokens"],
                     "path": expand(check["pointer"].rsplit(":", 1)[0]),
                     "line_start": None, "line_end": None,
                     "matched": exists, "unparsed": False,
                     "reason": "" if exists else "path does not exist",
                     "line_sha256": "", "delimiter_evidence": []}
        else:
            entry = bind(check["pointer"], check["tokens"], lines)
            entry = {"id": check["id"], "cell": check.get("cell", 1), **entry}
            entry["path"] = expand(entry["path"])
        entry["declared_path"] = expand(DECLARED.get(check["id"], ""))
        entry["path_is_declared"] = declared_ok(
            check["id"], check["pointer"].rsplit(":", 1)[0])
        if not entry["path_is_declared"]:
            entry["matched"] = False
            entry["reason"] = (entry.get("reason") or "") + (
                " (the pointer does not name the declared live object)"
                if not entry.get("reason") else
                "; the pointer does not name the declared live object")
        results.append(entry)
    matched = sum(1 for result in results if result["matched"])
    unparsed = sum(1 for result in results if result["unparsed"])
    bound_ok = bounded(len(results), matched, unparsed, duplicates)
    receipt = {
        "schema": "kaidoku-r80-pointer-bind-v1",
        "round": ROUND,
        "predicate": PREDICATE,
        "checked_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "instrument": {"path": INSTRUMENT_PATH,
                       "sha256": sha256_bytes(pathlib.Path(__file__).read_bytes())},
        "record": {"path": PROVINCE, "rev": resolved, "rev_arg": rev,
                   "sha256": sha256_bytes(blob)},
        "control": control,
        "checks_total": len(results),
        "matched": matched,
        "mismatches": len(results) - matched,
        "unparsed": unparsed,
        "duplicates": duplicates,
        "checks": results,
        "would_pass": bound_ok,
        "ok": ok_under(control, bound_ok),
    }
    return receipt


def rederive_duplicates(checks: list[dict]) -> list[str]:
    counts: dict[str, int] = {}
    order: list[str] = []
    for check in checks:
        check_id = str(check.get("id"))
        if check_id not in counts:
            counts[check_id] = 0
            order.append(check_id)
        counts[check_id] += 1
    return [check_id for check_id in order if counts.get(check_id, 0) > 1]


def delimiter_evidence_ok(check: dict) -> bool:
    evidence = check.get("delimiter_evidence")
    tokens = check.get("tokens") or []
    if not isinstance(evidence, list) or not evidence:
        return False
    for item in evidence:
        if not isinstance(item, dict):
            return False
        if item.get("delimited") is not True:
            return False
        if not isinstance(item.get("occurrences"), int) or item["occurrences"] < 1:
            return False
    if sorted(str(item.get("token")) for item in evidence) != sorted(map(str, tokens)):
        return False
    return True


def validate_receipt(receipt: dict) -> dict:
    defects: list[str] = []
    checks = receipt.get("checks") or []
    matched = sum(1 for check in checks if check.get("matched"))
    unparsed = sum(1 for check in checks if check.get("unparsed"))
    duplicates = receipt.get("duplicates")
    rederived = rederive_duplicates(checks)
    if not isinstance(duplicates, list) or not all(
            isinstance(item, str) for item in duplicates):
        defects.append("duplicates is not a list of check ids")
    elif sorted(duplicates) != sorted(rederived):
        defects.append("duplicates does not re-derive from the check list")
    if len(checks) != receipt.get("checks_total"):
        defects.append("checks_total does not re-derive from the check list")
    if matched != receipt.get("matched"):
        defects.append("matched does not re-derive from the check list")
    if len(checks) - matched != receipt.get("mismatches"):
        defects.append("mismatches does not re-derive from the check list")
    if unparsed != receipt.get("unparsed"):
        defects.append("unparsed does not re-derive from the check list")
    for check in checks:
        if check.get("matched") and check.get("unparsed"):
            defects.append(f"{check.get('id')}: matched and unparsed")
        if check.get("matched") and check.get("path_is_declared") is not True:
            defects.append(f"{check.get('id')}: matched without naming the declared live object")
        if check.get("matched") and not check.get("line_sha256"):
            defects.append(f"{check.get('id')}: matched without a pointed-line digest")
        start, end = check.get("line_start"), check.get("line_end")
        if check.get("matched") and not (isinstance(start, int) and isinstance(end, int)
                                         and 1 <= start <= end):
            defects.append(f"{check.get('id')}: matched without a 1-based line range")
        if check.get("matched") and not delimiter_evidence_ok(check):
            defects.append(f"{check.get('id')}: matched without delimiter evidence")
    record = receipt.get("record") or {}
    if not isinstance(record.get("sha256"), str) or len(record.get("sha256") or "") != 64:
        defects.append("record sha256 is not a 64-hex digest")
    rev = record.get("rev")
    if not is_commit_sha(rev):
        defects.append("record rev is not a 40-hex commit")
    if not receipt.get("checked_at"):
        defects.append("checked_at is absent")
    instrument = receipt.get("instrument") or {}
    if instrument.get("sha256") != sha256_bytes(pathlib.Path(__file__).read_bytes()):
        defects.append("instrument sha256 is not this file's digest")
    if receipt.get("ok"):
        if len(checks) != 5 or matched != len(checks) or unparsed:
            defects.append("ok true but the check set is not fully bound")
        if duplicates:
            defects.append("ok true with duplicate cells")
        if receipt.get("control") is not None:
            defects.append("ok true under a control")
    return {"defects": defects, "checks": len(checks), "matched": matched}


RECORD_TEMPLATE = (
    "The clients pin `rea-agents@6.7.0` today: Devin `rea-agents@6.7.0` "
    "(`/home/vgpnk/.config/devin/mcp_config.json:7`), OMP `rea-agents@6.7.0` "
    "(`/home/vgpnk/.omp/agent/mcp.json:12`), and Kimi `rea-agents@6.7.0` "
    "(`~/.kimi-code/config.toml:4722`).\n"
    "Ghidra: `application.version=12.1.4` "
    "(`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties:17`, "
    "`/home/vgpnk/.bashrc:28-29`).\n"
)


def selftest() -> int:
    cases: list[dict] = []

    def case(name, got, want):
        cases.append({"case": name, "got": got, "want": want, "pass": got == want})

    def forged(checks: list[dict], **overrides) -> dict:
        receipt = {
            "checks_total": 5, "matched": 5, "mismatches": 0, "unparsed": 0,
            "checked_at": "2026-11-04T00:00:00-03:00", "control": None,
            "duplicates": [],
            "instrument": {"path": INSTRUMENT_PATH,
                           "sha256": sha256_bytes(
                               pathlib.Path(__file__).read_bytes())},
            "record": {"sha256": "a" * 64, "rev": "b" * 40,
                       "rev_arg": "16dfa009"},
            "ok": True,
            "checks": checks,
        }
        receipt.update(overrides)
        return receipt

    def cells(count: int = 5) -> list[dict]:
        return [{"id": f"c{index}", "matched": True, "unparsed": False,
                 "path_is_declared": True, "line_start": 1, "line_end": 1,
                 "tokens": ["t"], "line_sha256": "b" * 64,
                 "delimiter_evidence": [{"token": "t", "occurrences": 1,
                                         "delimited": True}]}
                for index in range(count)]

    lines = ["a\n", '        "rea-agents@6.7.0",\n', "c\n", "d\n"]
    case("green-line", bind("f.json:2", ["rea-agents@6.7.0"], lines)["matched"], True)
    stale = bind("f.json:1", ["rea-agents@6.7.0"], lines)
    case("red-stale-line", (stale["matched"], stale["reason"]),
         (False, "token 'rea-agents@6.7.0' is not on line 1"))
    case("red-past-end", bind("f.json:9", ["x"], lines)["reason"],
         "line range 9-9 runs past end of file (4 lines)")
    absent = bind("f.json:2", ["x"], None)
    case("red-path-absent", (absent["matched"], absent["reason"]),
         (False, "path f.json does not exist"))
    noline = bind("f.json", ["x"], lines)
    case("red-no-line", (noline["unparsed"], noline["reason"]),
         (True, "pointer carries no line number"))
    case("red-backwards", bind("f.json:3-2", ["x"], lines)["reason"],
         "line range 3-2 is not a forward 1-based range")
    # A range fixture whose first token is a whole token: `a` would not be,
    # since it occurs inside `rea-agents` on the second line.
    span_lines = ["zz\n", '        "rea-agents@6.7.0",\n', "c\n", "d\n"]
    rng = bind("f.toml:1-2", ["zz", "rea-agents@6.7.0"], span_lines)
    case("green-range", rng["matched"], True)
    case("green-range-digest", bool(rng["line_sha256"]), True)
    miss = bind("f.toml:1-2", ["zz", "d"], span_lines)
    case("red-range-token-outside", (miss["matched"], miss["reason"]),
         (False, "token 'd' is not on line 1-2"))
    parsed, unparsed, duplicates = parse_record(RECORD_TEMPLATE)
    case("green-parse-counts", (len(parsed), unparsed), (5, []))
    case("green-parse-pointer", parsed[1]["pointer"],
         "/home/vgpnk/.omp/agent/mcp.json:12")
    case("green-parse-range", parsed[4]["pointer"], "/home/vgpnk/.bashrc:28-29")
    case("green-parse-tokens", parsed[4]["tokens"], list(BASHRC_TOKENS))
    case("green-parse-no-duplicates", duplicates, [])
    no_ghidra = RECORD_TEMPLATE.replace("`application.version=12.1.4`", "")
    checks_no_ghidra, unparsed_no_ghidra, _ = parse_record(no_ghidra)
    case("red-record-no-ghidra-value",
         (len(checks_no_ghidra), unparsed_no_ghidra), (5, ["ghidra-version"]))
    no_client = RECORD_TEMPLATE.replace(
        "and Kimi `rea-agents@6.7.0` (`~/.kimi-code/config.toml:4722`)", "")
    checks_no_client, unparsed_no_client, _ = parse_record(no_client)
    case("red-record-no-client", (len(checks_no_client), unparsed_no_client),
         (5, ["kimi-pin"]))
    no_bashrc = RECORD_TEMPLATE.replace(", `/home/vgpnk/.bashrc:28-29`", "")
    checks_no_bashrc, unparsed_no_bashrc, _ = parse_record(no_bashrc)
    case("red-record-no-bashrc",
         (len(checks_no_bashrc), "bashrc-exports" in unparsed_no_bashrc),
         (5, True))
    good = forged(cells())
    case("green-forged-consistent", validate_receipt(good)["defects"], [])
    bad = json.loads(json.dumps(good))
    bad["checks"][0]["line_sha256"] = ""
    case("red-forged-no-digest", bool(validate_receipt(bad)["defects"]), True)
    bad2 = json.loads(json.dumps(good))
    bad2["matched"] = 4
    case("red-forged-count", bool(validate_receipt(bad2)["defects"]), True)
    bad3 = json.loads(json.dumps(good))
    bad3["checks"][0]["path_is_declared"] = False
    case("red-forged-self-pointer", bool(validate_receipt(bad3)["defects"]), True)
    bad4 = json.loads(json.dumps(good))
    del bad4["checked_at"]
    case("red-forged-no-checked-at", bool(validate_receipt(bad4)["defects"]), True)
    bad5 = json.loads(json.dumps(good))
    bad5["control"] = "path-only"
    case("red-forged-control-ok", bool(validate_receipt(bad5)["defects"]), True)
    case("green-declared-path",
         declared_ok("bashrc-exports", "/home/vgpnk/.bashrc"), True)
    case("red-undeclared-path", declared_ok("bashrc-exports", "/etc/hosts"), False)

    # The exact-token rule: a longer token on either side of the declared one.
    live_long = bind("live.txt:1", ["rea-agents@6.7.0"],
                     ['  "rea-agents@6.7.05",\n'])
    case("red-substring-live-token", (live_long["matched"], live_long["reason"]),
         (False, "token 'rea-agents@6.7.0' occurs inside the longer token "
                 "'rea-agents@6.7.05' on line 1"))
    argv_long = bind("live.txt:1", ["rea-agents@6.7.0"],
                     ['args = [ "-y", "rea-agents@6.7.00", "mcp" ]\n'])
    case("red-substring-argv-token", (argv_long["matched"], argv_long["reason"]),
         (False, "token 'rea-agents@6.7.0' occurs inside the longer token "
                 "'rea-agents@6.7.00' on line 1"))
    mixed = bind("live.txt:1", ["rea-agents@6.7.0"],
                 ['"rea-agents@6.7.0" and "rea-agents@6.7.05"\n'])
    case("red-mixed-occurrence", mixed["matched"], False)
    case("green-exact-pin",
         bind("live.txt:1", ["rea-agents@6.7.0"], ['  "rea-agents@6.7.0",\n'])["matched"],
         True)
    case("green-range-second-line",
         bind("live.sh:1-2", ["GHIDRA_INSTALL_DIR="],
              ["#!/bin/bash\n",
               "export GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra\n"])["matched"],
         True)
    case("green-line-start",
         bind("live.txt:1", ["start"], ["start of line\n"])["matched"], True)
    prefixed = bind("live.txt:1", ["start"], ["xstart\n"])
    case("red-prefixed-token", (prefixed["matched"], prefixed["reason"]),
         (False, "token 'start' occurs inside the longer token 'xstart' on line 1"))
    case("green-line-end",
         bind("live.txt:1", ["end"], ["the end"])["matched"], True)
    followed = bind("live.txt:1", ["end"], ["endless\n"])
    case("red-followed-token", (followed["matched"], followed["reason"]),
         (False, "token 'end' occurs inside the longer token 'endless' on line 1"))
    package = bind("live.txt:1", ["6.7.0"], ['  "rea-agents@6.7.05",\n'])
    case("red-substring-package-pin", package["reason"],
         "token '6.7.0' occurs inside the longer token "
         "'rea-agents@6.7.05' on line 1")

    # Duplicate cells: counted, reported, and never collapsed.
    dup_omp = RECORD_TEMPLATE + (
        "OMP `rea-agents@6.7.0` (`/home/vgpnk/.omp/agent/mcp.json:12`)\n")
    parsed_omp, unparsed_omp, duplicates_omp = parse_record(dup_omp)
    case("red-duplicate-omp-cell", (len(parsed_omp), duplicates_omp),
         (6, ["omp-pin"]))
    case("red-duplicate-omp-counted",
         sum(1 for check in parsed_omp if check["id"] == "omp-pin"), 2)
    dup_devin = RECORD_TEMPLATE + (
        "Devin `rea-agents@6.7.0` "
        "(`/home/vgpnk/.config/devin/mcp_config.json:7`)\n")
    parsed_devin, _, duplicates_devin = parse_record(dup_devin)
    case("red-duplicate-devin-cell", (len(parsed_devin), duplicates_devin),
         (6, ["devin-pin"]))

    # `--validate` guards for the new fields, each asserted by its exact defect
    # list so the case isolates one guard rather than "some defect".
    bad6 = json.loads(json.dumps(good))
    bad6["checks"][0].pop("delimiter_evidence")
    case("red-forged-no-delimiter", validate_receipt(bad6)["defects"],
         ["c0: matched without delimiter evidence"])
    zero_occurrences = forged(cells())
    zero_occurrences["checks"][0]["delimiter_evidence"][0]["occurrences"] = 0
    case("red-forged-zero-occurrences",
         validate_receipt(zero_occurrences)["defects"],
         ["c0: matched without delimiter evidence"])
    wrong_token = forged(cells())
    wrong_token["checks"][0]["delimiter_evidence"][0]["token"] = "zzz"
    case("red-forged-wrong-evidence-token",
         validate_receipt(wrong_token)["defects"],
         ["c0: matched without delimiter evidence"])
    duplicate_cells = cells()
    duplicate_cells[1]["id"] = "omp-pin"
    duplicate_cells[2]["id"] = "omp-pin"
    dup_under_ok = forged(duplicate_cells, duplicates=["omp-pin"])
    case("red-forged-duplicates-under-ok",
         validate_receipt(dup_under_ok)["defects"],
         ["ok true with duplicate cells"])
    unlisted = forged(json.loads(json.dumps(duplicate_cells)), duplicates=[],
                      ok=False)
    case("red-forged-undeclared-duplicate",
         validate_receipt(unlisted)["defects"],
         ["duplicates does not re-derive from the check list"])
    untyped = forged(cells(), duplicates="omp-pin", ok=False)
    case("red-forged-duplicates-not-list", validate_receipt(untyped)["defects"],
         ["duplicates is not a list of check ids"])
    honest = forged(json.loads(json.dumps(duplicate_cells)),
                    duplicates=["omp-pin"], ok=False)
    case("green-forged-duplicate-not-ok", validate_receipt(honest)["defects"], [])
    wrong_instrument = forged(cells())
    wrong_instrument["instrument"]["sha256"] = "c" * 64
    case("red-forged-instrument-digest",
         validate_receipt(wrong_instrument)["defects"],
         ["instrument sha256 is not this file's digest"])
    short_record = forged(cells())
    short_record["record"]["sha256"] = "a" * 63
    case("red-forged-record-digest", validate_receipt(short_record)["defects"],
         ["record sha256 is not a 64-hex digest"])
    symbolic = forged(cells())
    symbolic["record"]["rev"] = "main"
    case("red-forged-rev-symbolic", validate_receipt(symbolic)["defects"],
         ["record rev is not a 40-hex commit"])
    no_range = forged(cells())
    no_range["checks"][0]["line_start"] = None
    case("red-forged-no-range", validate_receipt(no_range)["defects"],
         ["c0: matched without a 1-based line range"])
    both = forged(cells(), ok=False)
    both["checks"][0]["unparsed"] = True
    both["unparsed"] = 1
    case("red-forged-matched-unparsed", validate_receipt(both)["defects"],
         ["c0: matched and unparsed"])
    case("green-commit-sha", is_commit_sha("b" * 40), True)
    case("red-commit-sha-short", is_commit_sha("16dfa009"), False)
    case("red-commit-sha-symbolic", is_commit_sha("main"), False)
    case("red-commit-sha-nonhex", is_commit_sha("z" * 40), False)
    nonhex = forged(cells())
    nonhex["record"]["rev"] = "z" * 40
    case("red-forged-rev-nonhex", validate_receipt(nonhex)["defects"],
         ["record rev is not a 40-hex commit"])

    # The verdict conjuncts, so a mutated `bounded`/`ok_under` has a case.
    case("green-bounded", bounded(5, 5, 0, []), True)
    case("red-bounded-duplicate", bounded(6, 6, 0, ["omp-pin"]), False)
    case("red-bounded-five-with-duplicate", bounded(5, 5, 0, ["omp-pin"]), False)
    case("red-bounded-unparsed", bounded(5, 5, 1, []), False)
    case("green-ok-no-control", ok_under(None, True), True)
    case("red-ok-under-control", ok_under("path-only", True), False)

    failures = [case_ for case_ in cases if not case_["pass"]]
    for case_ in cases:
        print(json.dumps(case_, sort_keys=True))
    print(f"SELFTEST cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--json-out")
    ap.add_argument("--battery", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--validate")
    ap.add_argument("--control", choices=("path-only",))
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    root = os.path.abspath(args.root)
    if args.validate:
        with open(args.validate, encoding="utf-8") as handle:
            receipt = json.load(handle)
        result = validate_receipt(receipt)
        print(json.dumps(result, sort_keys=True))
        return 0 if not result["defects"] else 1
    if args.rev is None:
        print("usage: --rev <rev> [--battery] [--json-out <path>] [--control path-only]",
              file=sys.stderr)
        return 2
    try:
        receipt = battery(root, args.rev, args.control)
    except Unevaluable as exc:
        print(json.dumps({"ok": False, "unevaluable": str(exc)}))
        return 2
    text = json.dumps(receipt, indent=1, sort_keys=True) + "\n"
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            handle.write(text)
    print(json.dumps({"exit": 0 if receipt["ok"] else 1,
                      "checks_total": receipt["checks_total"],
                      "matched": receipt["matched"],
                      "mismatches": receipt["mismatches"],
                      "unparsed": receipt["unparsed"],
                      "duplicates": receipt["duplicates"],
                      "mismatch_ids": [check["id"] for check in receipt["checks"]
                                       if not check["matched"]],
                      "ok": receipt["ok"]}, sort_keys=True))
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
