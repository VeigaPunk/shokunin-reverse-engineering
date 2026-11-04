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

    --battery   bind every check at --rev against the live files; write a receipt.
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
import re
import subprocess
import sys

ROUND = 79
PROVINCE = "PROVINCE.md"
PREDICATE = (
    "R79-C2 is verified iff `python3 -I -B tools/round-79/pointer-bind.py --root . "
    "--rev <measured> --json-out <receipt>` exits 0 with `checks_total 5`, "
    "`matched 5`, `mismatches 0`, `unparsed 0` and a defect-free `validate`, every "
    "pointer bound at the line and range it names, while at base `29d2ca30` the same "
    "command exits 1 with `mismatches 2` naming `omp-pin` (record `:8`, the pin at "
    "`:12`) and `kimi-pin` (record `:4126`, the pin at `:4722`), and the control "
    "`--control path-only` reports `mismatches 0` on that same stale record."
)

RE_PIN = re.compile(r"(Devin|OMP|Kimi)\s+`rea-agents@([0-9][0-9.]*)`\s*\(`([^`]+)`\)")
RE_GHIDRA_PTR = re.compile(r"`([^`]*Ghidra/application\.properties):(\d+)`")
RE_GHIDRA_VALUE = re.compile(r"application\.version=([0-9][0-9.]*)")
RE_BASHRC_PTR = re.compile(r"`([^`]*\.bashrc):(\d+)(?:-(\d+))?`")
RE_POINTER = re.compile(r"^(?P<path>.+?):(?P<start>\d+)(?:-(?P<end>\d+))?$")

BASHRC_TOKENS = ("GHIDRA_INSTALL_DIR=", "JAVA_HOME=")


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


def bind(pointer: str, tokens: list[str], line_count: int,
         lines: list[str] | None) -> dict:
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
    missing = [token for token in tokens if not any(token in line for line in pointed)]
    if missing:
        out["reason"] = (f"token {missing[0]!r} is not on line "
                         f"{start if start == end else f'{start}-{end}'}")
        return out
    out["matched"] = True
    return out


def read_lines(path: str) -> list[str] | None:
    try:
        with open(expand(path), encoding="utf-8", errors="replace") as handle:
            return handle.readlines()
    except OSError:
        return None


def parse_record(text: str) -> tuple[list[dict], list[str]]:
    """Extract the five declared pointer cells from PROVINCE.md."""
    checks: list[dict] = []
    unparsed: list[str] = []
    pins = {name: (pin, pointer) for name, pin, pointer in RE_PIN.findall(text)}
    for client, check_id in (("Devin", "devin-pin"), ("OMP", "omp-pin"),
                             ("Kimi", "kimi-pin")):
        if client not in pins:
            unparsed.append(check_id)
            checks.append({"id": check_id, "pointer": "",
                           "tokens": []})
            continue
        pin, pointer = pins[client]
        checks.append({"id": check_id, "pointer": pointer,
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
    return checks, unparsed


def battery(root: str, rev: str, control: str | None) -> dict:
    blob = git_show(root, rev, PROVINCE)
    if blob is None:
        raise Unevaluable(f"{PROVINCE} absent at {rev}")
    checks, unparsed_ids = parse_record(blob.decode("utf-8"))
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
            entry = bind(check["pointer"], check["tokens"], 0, lines)
            entry = {"id": check["id"], **entry}
            entry["path"] = expand(entry["path"])
        results.append(entry)
    matched = sum(1 for r in results if r["matched"])
    unparsed = sum(1 for r in results if r["unparsed"])
    receipt = {
        "schema": "kaidoku-r79-pointer-bind-v1",
        "round": ROUND,
        "predicate": PREDICATE,
        "checked_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "record": {"path": PROVINCE, "rev": rev,
                   "sha256": sha256_bytes(blob)},
        "control": control,
        "checks_total": len(results),
        "matched": matched,
        "mismatches": len(results) - matched,
        "unparsed": unparsed,
        "checks": results,
    }
    receipt["ok"] = bool(len(results) == 5 and matched == len(results)
                         and unparsed == 0)
    return receipt


def validate_receipt(receipt: dict) -> dict:
    defects: list[str] = []
    checks = receipt.get("checks") or []
    ids = [c.get("id") for c in checks]
    if len(ids) != len(set(ids)):
        defects.append("duplicate check id")
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
        if check.get("matched") and not check.get("line_sha256"):
            defects.append(f"{check.get('id')}: matched without a pointed-line digest")
        start, end = check.get("line_start"), check.get("line_end")
        if check.get("matched") and not (isinstance(start, int) and isinstance(end, int)
                                         and 1 <= start <= end):
            defects.append(f"{check.get('id')}: matched without a 1-based line range")
    record = receipt.get("record") or {}
    if not isinstance(record.get("sha256"), str) or len(record.get("sha256") or "") != 64:
        defects.append("record sha256 is not a 64-hex digest")
    if receipt.get("ok") and (len(checks) != 5 or matched != len(checks) or unparsed):
        defects.append("ok true but the check set is not fully bound")
    return {"defects": defects, "checks": len(checks), "matched": matched}


def selftest() -> int:
    cases: list[dict] = []

    def case(name, got, want):
        cases.append({"case": name, "got": got, "want": want, "pass": got == want})

    lines = ["a\n", '        "rea-agents@6.7.0",\n', "c\n", "d\n"]
    case("green-line", bind("f.json:2", ["rea-agents@6.7.0"], 4, lines)["matched"], True)
    stale = bind("f.json:1", ["rea-agents@6.7.0"], 4, lines)
    case("red-stale-line", (stale["matched"], stale["reason"]),
         (False, "token 'rea-agents@6.7.0' is not on line 1"))
    case("red-past-end", bind("f.json:9", ["x"], 4, lines)["reason"],
         "line range 9-9 runs past end of file (4 lines)")
    absent = bind("f.json:2", ["x"], 4, None)
    case("red-path-absent", (absent["matched"], absent["reason"]),
         (False, "path f.json does not exist"))
    noline = bind("f.json", ["x"], 4, lines)
    case("red-no-line", (noline["unparsed"], noline["reason"]),
         (True, "pointer carries no line number"))
    case("red-backwards", bind("f.json:3-2", ["x"], 4, lines)["reason"],
         "line range 3-2 is not a forward 1-based range")
    rng = bind("f.toml:1-2", ["a", "rea-agents@6.7.0"], 4, lines)
    case("green-range", rng["matched"], True)
    case("green-range-digest", bool(rng["line_sha256"]), True)
    miss = bind("f.toml:1-2", ["a", "d"], 4, lines)
    case("red-range-token-outside", (miss["matched"], miss["reason"]),
         (False, "token 'd' is not on line 1-2"))
    record = (
        "Devin\n`rea-agents@6.7.0` (`/home/x/devin.json:7`) and OMP\n"
        "`rea-agents@6.7.0` (`/home/x/omp.json:8`) and Kimi\n"
        "`rea-agents@6.7.0` (`/home/x/kimi.toml:4126`); "
        "`application.version=12.1.4` (`/home/x/Ghidra/application.properties:17`); "
        "(`/home/x/.bashrc:28-29` (were `:23-24` before the edit))\n")
    parsed, unparsed = parse_record(record)
    case("green-parse-counts", (len(parsed), unparsed), (5, []))
    case("green-parse-pointer", parsed[1]["pointer"], "/home/x/omp.json:8")
    case("green-parse-range", parsed[4]["pointer"], "/home/x/.bashrc:28-29")
    case("green-parse-tokens", parsed[4]["tokens"], list(BASHRC_TOKENS))
    forged = {"checks_total": 5, "matched": 5, "mismatches": 0, "unparsed": 0,
              "record": {"sha256": "a" * 64}, "ok": True,
              "checks": [{"id": f"c{i}", "matched": True, "unparsed": False,
                          "line_start": 1, "line_end": 1,
                          "line_sha256": "b" * 64} for i in range(5)]}
    case("green-forged-consistent", validate_receipt(forged)["defects"], [])
    bad = json.loads(json.dumps(forged))
    bad["checks"][0]["line_sha256"] = ""
    case("red-forged-no-digest", bool(validate_receipt(bad)["defects"]), True)
    bad2 = json.loads(json.dumps(forged))
    bad2["matched"] = 4
    case("red-forged-count", bool(validate_receipt(bad2)["defects"]), True)
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
    if not args.battery or args.rev is None:
        print("usage: --battery --rev <rev> [--json-out <path>] [--control path-only]",
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
