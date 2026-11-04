#!/usr/bin/env python3
"""Round-79 pointer binding: the record's live pointers are checked at their line.

`PROVINCE.md` names drift-prone live objects with `path:line` pointers.  The
round-78 surface recheck compared only `pointer.split(":")[0]` — the file — so a
pointer whose line moved still scored green (the round-78 closure routed it:
the OMP pointer `:8` was `:12` and the Kimi pointer `:4126` was `:4722`).  This
instrument binds each pointer to the token it claims:

  devin-pin       `rea-agents@<pin>` must occur on the pointed line
  omp-pin         same
  kimi-pin        same
  ghidra-version  `application.version=<value>` must occur on the pointed line
  bashrc-exports  `GHIDRA_INSTALL_DIR=` and `JAVA_HOME=` must occur in the range

A pointer with no line, a line past end of file, an absent path and a line that
does not carry the token are all mismatches.  The receipt keeps the pointed
lines' sha256, never their bytes (the configs' non-pin content is not evidence).

    --battery   bind every check at --rev against the live files; write a receipt
                (the default mode whenever --rev is supplied: the frozen R79-C2
                counting command omits this flag, and a printed command must run
                as printed).
    --selftest  unit cases, one red per failure shape plus the look-alikes.
    --validate  re-derive a receipt's counts from its own check list.
    --control   `path-only`: the round-78 rule (the path exists, the line is not
                read) — recorded to show it cannot fail on a moved line.

Exit: 0 every check bound; 1 otherwise; 2 could-not-evaluate.
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
PREDICATE = (
    "R80-C1 is verified iff `tools/round-80/strictness-battery.py` scores a "
    "candidate binder with `candidate_false_greens 0` against four red fixtures "
    "while the round-79 control binder scores 4, no green control is refused, "
    "and the live arm reads `checks_total 5`, `matched 5`, `mismatches 0`, "
    "`unparsed 0`, `duplicates []`."
)

RE_PIN = re.compile(r"(Devin|OMP|Kimi)\s+`rea-agents@([0-9][0-9.]*)`\s*\(`([^`]+)`\)")
RE_GHIDRA_PTR = re.compile(r"`([^`]*Ghidra/application\.properties):(\d+)`")
RE_GHIDRA_VALUE = re.compile(r"application\.version=([0-9][0-9.]*)")
RE_BASHRC_PTR = re.compile(r"`([^`]*\.bashrc):(\d+)(?:-(\d+))?`")
RE_POINTER = re.compile(r"^(?P<path>.+?):(?P<start>\d+)(?:-(?P<end>\d+))?$")

# A token binds only where both sides are word boundaries or the slice edge:
# `rea-agents@6.7.0` must not bind inside `rea-agents@6.7.05`.
TOKEN_CHARS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")

BASHRC_TOKENS = ("GHIDRA_INSTALL_DIR=", "JAVA_HOME=")

# The live object each cell must name (round 78's `same_path` rule, kept).
DECLARED = {
    "devin-pin": "/home/vgpnk/.config/devin/mcp_config.json",
    "omp-pin": "/home/vgpnk/.omp/agent/mcp.json",
    "kimi-pin": "~/.kimi-code/config.toml",
    "ghidra-version": "<GHIDRA_INSTALL_DIR>/Ghidra/application.properties",
    "bashrc-exports": "/home/vgpnk/.bashrc",
}


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


def expand(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


def occurrence_context(line: str, token: str) -> tuple[bool, str]:
    """(binds, context): binds when one occurrence is delimited on both sides."""
    binds = False
    context = ""
    start = 0
    while True:
        index = line.find(token, start)
        if index < 0:
            break
        before = line[index - 1] if index else ""
        after = line[index + len(token)] if index + len(token) < len(line) else ""
        if (not before or before not in TOKEN_CHARS) and \
                (not after or after not in TOKEN_CHARS):
            binds = True
        elif not context:
            context = before + token + after
        start = index + 1
    return binds, context


def bind(pointer: str, tokens: list[str], lines: list[str] | None) -> dict:
    """Bind one pointer to its tokens; no I/O, so the selftest can inject lines."""
    out = {"pointer": pointer, "tokens": tokens, "path": "", "line_start": None,
           "line_end": None, "matched": False, "unparsed": False, "reason": "",
           "line_sha256": ""}
    match = RE_POINTER.match(pointer)
    if not match:
        out["unparsed"] = True
        out["reason"] = "pointer carries no line number"
        return out
    out["path"] = match.group("path")
    start = int(match.group("start"))
    end = int(match.group("end") or start)
    out["line_start"], out["line_end"] = start, end
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
    where = f"{start if start == end else f'{start}-{end}'}"
    missing: list[str] = []
    embedded: list[str] = []
    for token in tokens:
        verdicts = [occurrence_context(line, token) for line in pointed]
        if any(binds for binds, _ in verdicts):
            continue
        missing.append(token)
        context = next((ctx for binds, ctx in verdicts if ctx), "")
        if context:
            embedded.append(context)
    if missing:
        if embedded:
            out["reason"] = (f"token {missing[0]!r} occurs on line {where} only "
                             f"inside a longer token ({embedded[0]!r})")
        else:
            out["reason"] = f"token {missing[0]!r} is not on line {where}"
        return out
    out["matched"] = True
    out["mode"] = "delimited"
    return out


def read_lines(path: str) -> list[str] | None:
    try:
        with open(expand(path), encoding="utf-8", errors="replace") as handle:
            return handle.readlines()
    except OSError:
        return None


def parse_record(text: str) -> tuple[list[dict], list[str], list[str]]:
    """Extract every declared pointer cell; a repeated client is a duplicate."""
    checks: list[dict] = []
    unparsed: list[str] = []
    duplicates: list[str] = []
    found: dict[str, list[tuple[str, str]]] = {}
    for name, pin, pointer in RE_PIN.findall(text):
        found.setdefault(name, []).append((pin, pointer))
    for client, check_id in (("Devin", "devin-pin"), ("OMP", "omp-pin"),
                             ("Kimi", "kimi-pin")):
        cells = found.get(client) or []
        if not cells:
            unparsed.append(check_id)
            checks.append({"id": check_id, "pointer": "",
                           "tokens": []})
            continue
        if len(cells) > 1:
            duplicates.append(check_id)
        for index, (pin, pointer) in enumerate(cells, start=1):
            checks.append({"id": check_id if index == 1 else f"{check_id}#{index}",
                           "pointer": pointer,
                           "tokens": [f"rea-agents@{pin}"]})
    ghidra_ptr = RE_GHIDRA_PTR.search(text)
    ghidra_value = RE_GHIDRA_VALUE.search(text)
    if not (ghidra_ptr and ghidra_value):
        unparsed.append("ghidra-version")
        checks.append({"id": "ghidra-version", "pointer": "", "tokens": []})
    else:
        checks.append({"id": "ghidra-version",
                       "pointer": f"{ghidra_ptr.group(1)}:{ghidra_ptr.group(2)}",
                       "tokens": [f"application.version={ghidra_value.group(1)}"]})
    bashrc = RE_BASHRC_PTR.search(text)
    if not bashrc:
        unparsed.append("bashrc-exports")
        checks.append({"id": "bashrc-exports", "pointer": "", "tokens": []})
    else:
        pointer = f"{bashrc.group(1)}:{bashrc.group(2)}"
        if bashrc.group(3):
            pointer += f"-{bashrc.group(3)}"
        checks.append({"id": "bashrc-exports", "pointer": pointer,
                       "tokens": list(BASHRC_TOKENS)})
    return checks, unparsed, duplicates


def battery(root: str, rev: str, control: str | None) -> dict:
    blob = git_show(root, rev, PROVINCE)
    if blob is None:
        raise Unevaluable(f"{PROVINCE} absent at {rev}")
    checks, unparsed_ids, duplicates = parse_record(blob.decode("utf-8"))
    results: list[dict] = []
    for check in checks:
        if not check["pointer"]:
            results.append({"id": check["id"], "pointer": "", "tokens": [],
                            "path": "", "line_start": None, "line_end": None,
                            "matched": False, "unparsed": True,
                            "reason": "the record cell does not parse",
                            "line_sha256": ""})
            continue
        lines = read_lines(check["pointer"].rsplit(":", 1)[0])
        if control == "path-only":
            exists = lines is not None
            entry = {"id": check["id"], "pointer": check["pointer"],
                     "tokens": check["tokens"],
                     "path": expand(check["pointer"].rsplit(":", 1)[0]),
                     "line_start": None, "line_end": None,
                     "matched": exists, "unparsed": False,
                     "reason": "" if exists else "path does not exist",
                     "line_sha256": ""}
        else:
            entry = bind(check["pointer"], check["tokens"], lines)
            entry = {"id": check["id"], **entry}
            entry["path"] = expand(entry["path"])
        entry["declared_path"] = expand(DECLARED.get(check["id"], ""))
        entry["path_is_declared"] = declared_ok(check["id"], check["pointer"].rsplit(":", 1)[0])
        if not entry["path_is_declared"]:
            entry["matched"] = False
            entry["reason"] = (entry.get("reason") or "") + (
                " (the pointer does not name the declared live object)"
                if not entry.get("reason") else
                "; the pointer does not name the declared live object")
        results.append(entry)
    matched = sum(1 for r in results if r["matched"])
    unparsed = sum(1 for r in results if r["unparsed"])
    receipt = {
        "schema": "kaidoku-r80-pointer-bind-v2",
        "round": ROUND,
        "predicate": PREDICATE,
        "checked_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "instrument": {"path": "tools/round-80/pointer-bind.py",
                       "sha256": sha256_bytes(pathlib.Path(__file__).read_bytes())},
        "record": {"path": PROVINCE, "rev": rev,
                   "sha256": sha256_bytes(blob)},
        "control": control,
        "duplicates": duplicates,
        "checks_total": len(results),
        "matched": matched,
        "mismatches": len(results) - matched,
        "unparsed": unparsed,
        "checks": results,
    }
    receipt["would_pass"] = bool(len(results) == 5 and matched == len(results)
                                 and unparsed == 0 and not duplicates)
    receipt["ok"] = bool(receipt["would_pass"] and control is None)
    return receipt


def validate_receipt(receipt: dict) -> dict:
    defects: list[str] = []
    checks = receipt.get("checks") or []
    ids = [c.get("id") for c in checks]
    if len(ids) != len(set(ids)):
        defects.append("duplicate check id")
    duplicates = receipt.get("duplicates")
    if not isinstance(duplicates, list):
        defects.append("duplicates is not a list")
        duplicates = []
    for duplicate in duplicates:
        if not isinstance(duplicate, str):
            defects.append("a duplicate id is not a string")
            continue
        if duplicate not in ids:
            defects.append(f"duplicate id {duplicate!r} has no cell")
        if f"{duplicate}#2" not in ids:
            defects.append(f"duplicate id {duplicate!r} kept no second cell")
    if len(checks) != receipt.get("checks_total"):
        defects.append("checks_total does not re-derive from the check list")
    matched = sum(1 for c in checks if c.get("matched"))
    unparsed = sum(1 for c in checks if c.get("unparsed"))
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
        if check.get("matched") and check.get("mode") != "delimited":
            defects.append(f"{check.get('id')}: matched without the delimited mode")
        if check.get("matched") and not check.get("line_sha256"):
            defects.append(f"{check.get('id')}: matched without a pointed-line digest")
        start, end = check.get("line_start"), check.get("line_end")
        if check.get("matched") and not (isinstance(start, int) and isinstance(end, int)
                                         and 1 <= start <= end):
            defects.append(f"{check.get('id')}: matched without a 1-based line range")
    record = receipt.get("record") or {}
    if not isinstance(record.get("sha256"), str) or len(record.get("sha256") or "") != 64:
        defects.append("record sha256 is not a 64-hex digest")
    rev = record.get("rev")
    if not (isinstance(rev, str) and len(rev) == 40
            and all(c in "0123456789abcdef" for c in rev)):
        defects.append("record rev is not a 40-hex commit")
    if not receipt.get("checked_at"):
        defects.append("checked_at is absent")
    inst = receipt.get("instrument") or {}
    if inst.get("sha256") != sha256_bytes(pathlib.Path(__file__).read_bytes()):
        defects.append("instrument sha256 is not this file's digest")
    if receipt.get("ok") and (len(checks) != 5 or matched != len(checks) or unparsed):
        defects.append("ok true but the check set is not fully bound")
    if receipt.get("ok") and duplicates:
        defects.append("ok true with a duplicate cell")
    if receipt.get("ok") and receipt.get("control") is not None:
        defects.append("ok true under a control")
    return {"defects": defects, "checks": len(checks), "matched": matched}


def selftest() -> int:
    cases: list[dict] = []

    def case(name, got, want):
        cases.append({"case": name, "got": got, "want": want, "pass": got == want})

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
    rng = bind("f.toml:1-2", ["a", "rea-agents@6.7.0"], lines)
    case("green-range", rng["matched"], True)
    case("green-range-digest", bool(rng["line_sha256"]), True)
    miss = bind("f.toml:1-2", ["a", "d"], lines)
    case("red-range-token-outside", (miss["matched"], miss["reason"]),
         (False, "token 'd' is not on line 1-2"))
    record = (
        "Devin\n`rea-agents@6.7.0` (`/home/x/devin.json:7`) and OMP\n"
        "`rea-agents@6.7.0` (`/home/x/omp.json:8`) and Kimi\n"
        "`rea-agents@6.7.0` (`/home/x/kimi.toml:4126`); "
        "`application.version=12.1.4` (`/home/x/Ghidra/application.properties:17`); "
        "(`/home/x/.bashrc:28-29` (were `:23-24` before the edit))\n")
    parsed, unparsed, duplicates = parse_record(record)
    case("green-parse-counts", (len(parsed), unparsed), (5, []))
    case("green-parse-no-duplicates", duplicates, [])
    case("green-parse-pointer", parsed[1]["pointer"], "/home/x/omp.json:8")
    case("green-parse-range", parsed[4]["pointer"], "/home/x/.bashrc:28-29")
    case("green-parse-tokens", parsed[4]["tokens"], list(BASHRC_TOKENS))
    forged = {"checks_total": 5, "matched": 5, "mismatches": 0, "unparsed": 0,
              "checked_at": "2026-11-04T00:00:00-03:00", "control": None,
              "instrument": {"path": "tools/round-80/pointer-bind.py",
                             "sha256": sha256_bytes(pathlib.Path(__file__).read_bytes())},
              "duplicates": [],
              "record": {"sha256": "a" * 64, "rev": "b" * 40}, "ok": True,
              "checks": [{"id": f"c{i}", "matched": True, "unparsed": False,
                          "mode": "delimited", "path_is_declared": True,
                          "line_start": 1, "line_end": 1,
                          "line_sha256": "b" * 64} for i in range(5)]}
    case("green-forged-consistent", validate_receipt(forged)["defects"], [])
    bad = json.loads(json.dumps(forged))
    bad["checks"][0]["line_sha256"] = ""
    case("red-forged-no-digest", bool(validate_receipt(bad)["defects"]), True)
    bad2 = json.loads(json.dumps(forged))
    bad2["matched"] = 4
    case("red-forged-count", bool(validate_receipt(bad2)["defects"]), True)
    bad3 = json.loads(json.dumps(forged))
    bad3["checks"][0]["path_is_declared"] = False
    case("red-forged-self-pointer", bool(validate_receipt(bad3)["defects"]), True)
    bad4 = json.loads(json.dumps(forged))
    del bad4["checked_at"]
    case("red-forged-no-checked-at", bool(validate_receipt(bad4)["defects"]), True)
    bad5 = json.loads(json.dumps(forged))
    bad5["control"] = "path-only"
    case("red-forged-control-ok", bool(validate_receipt(bad5)["defects"]), True)
    case("green-declared-path", declared_ok("bashrc-exports", "/home/vgpnk/.bashrc"), True)
    case("red-undeclared-path", declared_ok("bashrc-exports", "/etc/hosts"), False)
    # round 80 (R80-C1): exact-token binding and the duplicate-cell rule.
    quoted = ['        "rea-agents@6.7.0",\n']
    longer_line = ['        "rea-agents@6.7.05",\n']
    longer_argv = ['args = [ "-y", "rea-agents@6.7.00", "mcp" ]\n']
    prefixed = ['xrea-agents@6.7.0\n']
    case("green-exact-quoted", bind("f.json:1", ["rea-agents@6.7.0"], quoted)["matched"],
         True)
    case("green-exact-mode", bind("f.json:1", ["rea-agents@6.7.0"], quoted)["mode"],
         "delimited")
    sub = bind("f.json:1", ["rea-agents@6.7.0"], longer_line)
    case("red-substring-longer-line", (sub["matched"], "longer token" in sub["reason"]),
         (False, True))
    sub2 = bind("f.json:1", ["rea-agents@6.7.0"], longer_argv)
    case("red-substring-longer-argv", (sub2["matched"], "longer token" in sub2["reason"]),
         (False, True))
    sub3 = bind("f.json:1", ["rea-agents@6.7.0"], prefixed)
    case("red-substring-prefix-before", (sub3["matched"], "longer token" in sub3["reason"]),
         (False, True))
    bash = ["#!/bin/bash\n", "export GHIDRA_INSTALL_DIR=/home/x/ghidra\n"]
    case("green-range-second-line",
         bind("f.sh:1-2", ["GHIDRA_INSTALL_DIR="], bash)["matched"], True)
    dup_record = record + "OMP `rea-agents@6.7.0` (`/home/x/omp2.json:9`)\n"
    dup_checks, dup_unparsed, dup_ids = parse_record(dup_record)
    case("red-duplicate-omp-counted",
         (len(dup_checks), dup_unparsed, dup_ids), (6, [], ["omp-pin"]))
    case("red-duplicate-omp-second-cell",
         [c["id"] for c in dup_checks[1:3]], ["omp-pin", "omp-pin#2"])
    devin_record = record + "Devin `rea-agents@6.7.0` (`/home/x/devin2.json:9`)\n"
    case("red-duplicate-devin-counted",
         parse_record(devin_record)[2], ["devin-pin"])
    dup_receipt = json.loads(json.dumps(forged))
    dup_receipt["duplicates"] = ["c0"]
    case("red-validate-duplicates-ok",
         any("duplicate" in d for d in validate_receipt(dup_receipt)["defects"]), True)
    mode_receipt = json.loads(json.dumps(forged))
    mode_receipt["checks"][0]["mode"] = "substring"
    case("red-validate-mode-absent",
         any("delimited mode" in d for d in validate_receipt(mode_receipt)["defects"]),
         True)
    failures = [c for c in cases if not c["pass"]]
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
        receipt = json.loads(open(args.validate, encoding="utf-8").read())
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
                      "mismatch_ids": [c["id"] for c in receipt["checks"]
                                       if not c["matched"]],
                      "ok": receipt["ok"]}, sort_keys=True))
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
