#!/usr/bin/env python3
"""Round-78 surface recheck: the record's drift-prone surface values, re-derived from live bytes.

PROVINCE.md records the lane's REA pins, the Ghidra provider and the JDK as
prose with a date.  Nothing re-derives those values: a token grep finds
`21.0.12.1` in the sentence whether the host runs it or not.  This instrument
parses each recorded value with a declared pattern, reads the live object the
record names (the three client configs' `rea` entry, the Ghidra provider's
`application.properties`, the `.bashrc` provider exports, `java -version`), and
compares typed values.  A pointer that is not the declared live source, a value
that does not parse, and a value that differs are all defects.

    --battery   compare the record at --rev with the live host; write a receipt.
    --selftest  unit cases: one red per failure shape plus the look-alikes.
    --validate  re-derive a receipt's counts from its own check list.
    --control   `token-grep`: the do-nothing control that searches the live text
                for the recorded token instead of parsing it.

Exit: 0 every check matched with nothing unparsed; 1 otherwise; 2 could-not-evaluate.
The receipt is dated: a live value is an observation at the receipt's `checked_at`.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import tomllib

ROUND = 78
PROVINCE = "PROVINCE.md"
PREDICATE = (
    "R78-C2 is verified iff `python3 -I -B tools/round-78/surface-recheck.py --root . "
    "--rev <measured> --json-out <receipt>` exits 0 with `checks_total 8`, `matched 8`, "
    "`mismatches 0`, `unparsed 0` and a defect-free `validate`, every value re-derived "
    "from the live object the record names and compared typed to the record's parsed "
    "value, while at base `6205ec8c` the same command exits 1 with `mismatches 2` "
    "naming the JDK version (`21.0.12.1` recorded, `21.0.13` live) and the OMP rea "
    "disable (the record says the live file no longer records it, the live file "
    "carries `disabledServers: [\"rea\"]`), and the control `--control token-grep` "
    "accepts a forged record whose value appears in the live text but not in the "
    "object the record names."
)

DECLARED = {
    "devin": "/home/vgpnk/.config/devin/mcp_config.json",
    "omp": "/home/vgpnk/.omp/agent/mcp.json",
    "kimi": "/home/vgpnk/.kimi-code/config.toml",
    "bashrc": "/home/vgpnk/.bashrc",
    "java": "java -version (PATH)",
    "ghidra": "<GHIDRA_INSTALL_DIR>/Ghidra/application.properties",
}

RE_PIN = re.compile(r"(Devin|OMP|Kimi)\s+`rea-agents@([0-9][0-9.]*)`\s*\(`([^`]+)`\)")
RE_GHIDRA_VERSION = re.compile(r"application\.version=([0-9][0-9.]*)")
RE_GHIDRA_DIR = re.compile(r"GHIDRA_INSTALL_DIR=([^\s`\"]+)")
RE_JDK = re.compile(r"openjdk version \"([0-9][0-9._]*)\"")
RE_JAVA_HOME = re.compile(r"JAVA_HOME=([^\s`\",;]+)")
RE_DISABLE_ABSENT = re.compile(r"no longer records the disable")
RE_DISABLE_PRESENT = re.compile(r"records the disable in `?disabledServers")
RE_PIN_ARG = re.compile(r"rea-agents@([0-9][0-9.]*)")


class Unevaluable(Exception):
    """Exit-2 class: the recheck cannot read a declared object."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_show(root: str, rev: str, path: str) -> bytes | None:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text)


# ------------------------------------------------------------- record side ---

def parse_record(text: str) -> tuple[dict, list[str]]:
    """Extract every declared surface value from the record's prose."""
    flat = squash(text)
    values: dict = {}
    unparsed: list[str] = []
    pins = {m.group(1): {"pin": m.group(2), "pointer": m.group(3)}
            for m in RE_PIN.finditer(flat)}
    for client, key in (("Devin", "devin"), ("OMP", "omp"), ("Kimi", "kimi")):
        if client in pins:
            values[f"{key}_pin"] = pins[client]
        else:
            unparsed.append(f"{key}_pin")
    found = RE_GHIDRA_VERSION.search(flat)
    values["ghidra_version"] = found.group(1) if found else None
    found = RE_GHIDRA_DIR.search(flat)
    values["ghidra_dir"] = found.group(1) if found else None
    found = RE_JDK.search(flat)
    values["jdk_version"] = found.group(1) if found else None
    found = RE_JAVA_HOME.search(flat)
    values["java_home"] = found.group(1) if found else None
    absent = bool(RE_DISABLE_ABSENT.search(flat))
    present = bool(RE_DISABLE_PRESENT.search(flat))
    values["omp_disable_claim"] = (False if absent and not present
                                   else True if present and not absent else None)
    for key in ("ghidra_version", "ghidra_dir", "jdk_version", "java_home",
                "omp_disable_claim"):
        if values[key] is None:
            unparsed.append(key)
    return values, unparsed


def expand(path: str) -> str:
    return str(pathlib.Path(path.replace("$HOME", str(pathlib.Path.home()))
                            .replace("~", str(pathlib.Path.home()))).expanduser())


# --------------------------------------------------------------- live side ---

def read_json(path: str) -> dict:
    try:
        return json.loads(pathlib.Path(path).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise Unevaluable(f"{path}: {exc}") from exc


def rea_pin_from_args(args) -> str | None:
    if not isinstance(args, list):
        return None
    joined = " ".join(str(a) for a in args)
    found = RE_PIN_ARG.search(joined)
    return found.group(1) if found else None


def probe_live() -> dict:
    """Read the declared live objects; return parsed values, texts and sources."""
    live: dict = {}
    texts: dict = {}
    devin = read_json(DECLARED["devin"])
    omp = read_json(DECLARED["omp"])
    kimi = tomllib.loads(pathlib.Path(DECLARED["kimi"]).read_text())
    bashrc = pathlib.Path(DECLARED["bashrc"]).read_text()
    texts["devin"] = json.dumps(devin, sort_keys=True)
    texts["omp"] = json.dumps(omp, sort_keys=True)
    texts["kimi"] = pathlib.Path(DECLARED["kimi"]).read_text()
    texts["bashrc"] = bashrc
    live["devin_pin"] = rea_pin_from_args(
        ((devin.get("mcpServers") or {}).get("rea") or {}).get("args"))
    omp_entry = (omp.get("mcpServers") or {}).get("rea") or {}
    live["omp_pin"] = rea_pin_from_args(omp_entry.get("args"))
    disabled = omp.get("disabledServers") or []
    live["omp_disable"] = isinstance(disabled, list) and "rea" in disabled
    live["omp_enabled_key"] = "enabled" in omp_entry
    live["kimi_pin"] = rea_pin_from_args(
        ((kimi.get("mcp_servers") or {}).get("rea") or {}).get("args"))
    found = re.search(r"(?m)^export GHIDRA_INSTALL_DIR=\"?([^\"\n]+)\"?", bashrc)
    live["ghidra_dir"] = expand(found.group(1)) if found else None
    live["ghidra_version"] = None
    if live["ghidra_dir"]:
        props = pathlib.Path(live["ghidra_dir"], "Ghidra/application.properties")
        if props.is_file():
            texts["ghidra"] = props.read_text()
            found = RE_GHIDRA_VERSION.search(texts["ghidra"])
            live["ghidra_version"] = found.group(1) if found else None
    found = re.search(r"(?m)^export JAVA_HOME=\"?([^\"\n]+)\"?", bashrc)
    live["java_home"] = expand(found.group(1)) if found else None
    proc = subprocess.run(["java", "-version"], capture_output=True, text=True)
    texts["java"] = (proc.stdout + proc.stderr).strip()
    found = re.search(r"openjdk version \"([0-9][0-9._]*)\"", texts["java"])
    live["jdk_version"] = found.group(1) if found else None
    return {"values": live, "texts": texts}


# ------------------------------------------------------------- comparisons ---

def same_path(a: str, b: str) -> bool:
    try:
        return pathlib.Path(a).resolve() == pathlib.Path(b).resolve()
    except OSError:
        return a == b


def compare(record: dict, live: dict) -> list[dict]:
    checks: list[dict] = []

    def add(check_id, record_value, live_value, matched, source, note=""):
        checks.append({"check": check_id, "record": record_value,
                       "live": live_value, "matched": bool(matched),
                       "source": source, "note": note})

    for key, client in (("devin_pin", "devin"), ("omp_pin", "omp"),
                        ("kimi_pin", "kimi")):
        rec = record.get(key) or {}
        pointer = rec.get("pointer", "")
        declared = DECLARED[client]
        clean = pointer.split(":")[0]
        pointer_ok = same_path(expand(clean), declared)
        add(f"{client}-rea-pin", rec.get("pin"), live.get(key),
            rec.get("pin") is not None and rec.get("pin") == live.get(key)
            and pointer_ok, declared,
            "" if pointer_ok else f"record points at {clean}")
    add("omp-rea-disable", record.get("omp_disable_claim"),
        live.get("omp_disable"),
        record.get("omp_disable_claim") is not None
        and record.get("omp_disable_claim") is live.get("omp_disable"),
        DECLARED["omp"] + " disabledServers",
        "the record's claim about whether the live file records the disable")
    add("ghidra-version", record.get("ghidra_version"), live.get("ghidra_version"),
        record.get("ghidra_version") is not None
        and record.get("ghidra_version") == live.get("ghidra_version"),
        DECLARED["ghidra"])
    add("ghidra-dir", record.get("ghidra_dir"), live.get("ghidra_dir"),
        record.get("ghidra_dir") is not None
        and same_path(record.get("ghidra_dir"), live.get("ghidra_dir") or ""),
        DECLARED["bashrc"] + " export GHIDRA_INSTALL_DIR")
    add("jdk-version", record.get("jdk_version"), live.get("jdk_version"),
        record.get("jdk_version") is not None
        and record.get("jdk_version") == live.get("jdk_version"),
        DECLARED["java"])
    add("java-home", record.get("java_home"), live.get("java_home"),
        record.get("java_home") is not None
        and same_path(record.get("java_home"), live.get("java_home") or ""),
        DECLARED["bashrc"] + " export JAVA_HOME")
    return checks


def token_grep(record: dict, texts: dict) -> list[dict]:
    """Control: the recorded token appears somewhere in the live text."""
    pairs = [("devin-rea-pin", "devin", (record.get("devin_pin") or {}).get("pin")),
             ("omp-rea-pin", "omp", (record.get("omp_pin") or {}).get("pin")),
             ("kimi-rea-pin", "kimi", (record.get("kimi_pin") or {}).get("pin")),
             ("ghidra-version", "ghidra", record.get("ghidra_version")),
             ("ghidra-dir", "bashrc", record.get("ghidra_dir")),
             ("jdk-version", "java", record.get("jdk_version")),
             ("java-home", "bashrc", record.get("java_home"))]
    checks = []
    for check_id, key, value in pairs:
        text = texts.get(key, "")
        checks.append({"check": check_id, "record": value,
                       "live": "token present" if value and value in text
                               else "token absent",
                       "matched": bool(value) and value in text,
                       "source": "token grep of the live text"})
    claim = record.get("omp_disable_claim")
    checks.append({"check": "omp-rea-disable", "record": claim,
                   "live": "not searched",
                   "matched": claim is not None, "source": "token grep"})
    return checks


def validate_receipt(receipt: dict) -> dict:
    defects: list[str] = []
    checks = receipt.get("checks") or []
    ids = [c.get("check") for c in checks]
    if len(ids) != len(set(ids)):
        defects.append("duplicate check id")
    if receipt.get("checks_total") != len(checks):
        defects.append("checks_total does not match the check list")
    if receipt.get("matched") != sum(1 for c in checks if c.get("matched")):
        defects.append("matched does not re-derive from the check list")
    if receipt.get("mismatches") != sum(
            1 for c in checks if c.get("record") is not None
            and not c.get("matched")):
        defects.append("mismatches does not re-derive from the check list")
    for check in checks:
        if not isinstance(check.get("matched"), bool):
            defects.append(f"{check.get('check')}: matched is not a bool")
        if check.get("record") is None and check.get("matched"):
            defects.append(f"{check.get('check')}: an unparsed value counted as matched")
    instrument = receipt.get("instrument") or {}
    if instrument.get("sha256") != sha256_bytes(pathlib.Path(__file__).read_bytes()):
        defects.append("instrument sha256 is not this file's digest")
    if receipt.get("unparsed") != len(receipt.get("unparsed_ids") or []):
        defects.append("unparsed count does not match the id list")
    return {"defects": defects, "checks": len(checks)}


def battery(root: str, rev: str, control: str | None) -> dict:
    raw = git_show(root, rev, PROVINCE)
    if raw is None:
        raise Unevaluable(f"{PROVINCE} absent at {rev}")
    record_text = raw.decode("utf-8", "replace")
    values, unparsed = parse_record(record_text)
    live = probe_live()
    checks = (token_grep(values, live["texts"]) if control == "token-grep"
              else compare(values, live["values"]))
    matched = sum(1 for c in checks if c["matched"])
    mismatches = sum(1 for c in checks
                     if c["record"] is not None and not c["matched"])
    receipt = {
        "schema": "kaidoku-r78-surface-recheck-v1",
        "predicate": PREDICATE,
        "rev": rev,
        "root": str(pathlib.Path(root).resolve()),
        "checked_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "control": control,
        "record": values,
        "live": live["values"],
        "checks": checks,
        "checks_total": len(checks),
        "matched": matched,
        "mismatches": mismatches,
        "unparsed": len(unparsed),
        "unparsed_ids": sorted(set(unparsed)),
        "instrument": {"path": "tools/round-78/surface-recheck.py",
                       "sha256": sha256_bytes(pathlib.Path(__file__).read_bytes())},
    }
    receipt["validate"] = validate_receipt(receipt)
    ok = (receipt["checks_total"] == 8 and matched == 8 and mismatches == 0
          and receipt["unparsed"] == 0 and not receipt["validate"]["defects"])
    receipt["ok"] = ok
    receipt["exit"] = 0 if ok else 1
    return receipt


# --------------------------------------------------------------- selftest ---

GENUINE = """
Installed pin, re-read 2026-10-20: Devin `rea-agents@6.7.0` (`/home/vgpnk/.config/devin/mcp_config.json:7`),
OMP `rea-agents@6.7.0` (`/home/vgpnk/.omp/agent/mcp.json:8`), and Kimi `rea-agents@6.7.0`
(`~/.kimi-code/config.toml:4126`).
`GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`, `application.version=12.1.4`;
`JAVA_HOME=/usr/lib/jvm/java-21-openjdk`; `java -version 2>&1 | head -n 1` returned
`openjdk version "21.0.13" 2026-10-20`. The live OMP file records the disable in `disabledServers`.
"""


def selftest() -> int:
    cases: list[dict] = []

    def case(name, got, want):
        cases.append({"case": name, "got": got, "want": want, "pass": got == want})

    values, unparsed = parse_record(GENUINE)
    case("green-parse-all", unparsed, [])
    case("green-devin-pin", values["devin_pin"]["pin"], "6.7.0")
    case("green-omp-pointer", values["omp_pin"]["pointer"].split(":")[0],
         "/home/vgpnk/.omp/agent/mcp.json")
    case("green-disable-claim", values["omp_disable_claim"], True)
    case("green-jdk", values["jdk_version"], "21.0.13")
    case("green-ghidra-dir", values["ghidra_dir"],
         "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC")
    # red: an unparsed value is never a match
    red_values, red_unparsed = parse_record("No surface block here.")
    case("red-unparsed-ids", sorted(red_unparsed),
         ["devin_pin", "ghidra_dir", "ghidra_version", "java_home",
          "jdk_version", "kimi_pin", "omp_disable_claim", "omp_pin"])
    # red: the record's own old JDK value is a mismatch against a live 21.0.13
    live = {"devin_pin": "6.7.0", "omp_pin": "6.7.0", "kimi_pin": "6.7.0",
            "omp_disable": True, "ghidra_version": "12.1.4",
            "ghidra_dir": "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC",
            "jdk_version": "21.0.13", "java_home": "/usr/lib/jvm/java-21-openjdk"}
    forged = dict(values, jdk_version="21.0.12.1")
    checks = compare(forged, live)
    case("red-stale-jdk", [c["check"] for c in checks if not c["matched"]],
         ["jdk-version"])
    # red: the record claims the live file no longer records the disable
    forged = dict(values, omp_disable_claim=False)
    checks = compare(forged, live)
    case("red-disable-claim", [c["check"] for c in checks if not c["matched"]],
         ["omp-rea-disable"])
    # red: a pointer that is not the declared live source
    forged = dict(values, devin_pin={"pin": "6.7.0",
                                     "pointer": "/home/vgpnk/.config/other.json:1"})
    checks = compare(forged, live)
    case("red-pointer", [c["check"] for c in checks if not c["matched"]],
         ["devin-rea-pin"])
    # the control: a token that lives in the live text but not in the object
    texts = {"ghidra": "application.version=12.1.4\napplication.gradle.min=8.5\n",
             "devin": '{"mcpServers": {"rea": {"args": ["-y", "rea-agents@6.7.0"]}}}',
             "omp": '{"mcpServers": {}, "disabledServers": []}',
             "kimi": 'args = ["-y", "rea-agents@6.7.0"]', "bashrc": "",
             "java": 'openjdk version "21.0.13"'}
    forged = dict(values, ghidra_version="8.5")
    control = {c["check"]: c["matched"] for c in token_grep(forged, texts)}
    parsed = {c["check"]: c["matched"] for c in compare(forged, live)}
    case("red-token-grep-accepts", (control["ghidra-version"],
                                    parsed["ghidra-version"]), (True, False))
    case("green-token-grep-real", token_grep(values, texts)[0]["matched"], True)
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
    ap.add_argument("--control", choices=("token-grep",))
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.validate:
        data = json.loads(pathlib.Path(args.validate).read_text())
        result = validate_receipt(data)
        print(json.dumps(result, sort_keys=True))
        return 0 if not result["defects"] else 1
    if not args.battery:
        ap.error("one of --battery, --selftest, --validate is required")
    rev = args.rev or subprocess.run(["git", "-C", args.root, "rev-parse", "HEAD"],
                                     capture_output=True, text=True).stdout.strip()
    try:
        receipt = battery(args.root, rev, args.control)
    except Unevaluable as exc:
        print(json.dumps({"unevaluable": str(exc), "exit": 2}))
        return 2
    if args.json_out:
        pathlib.Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(args.json_out).write_text(
            json.dumps(receipt, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"checks": receipt["checks_total"], "matched": receipt["matched"],
                      "mismatches": receipt["mismatches"],
                      "unparsed": receipt["unparsed"], "ok": receipt["ok"]},
                     sort_keys=True))
    print(json.dumps({"unmatched": [c["check"] for c in receipt["checks"]
                                    if not c["matched"]]}, sort_keys=True))
    return receipt["exit"]


if __name__ == "__main__":
    sys.exit(main())
