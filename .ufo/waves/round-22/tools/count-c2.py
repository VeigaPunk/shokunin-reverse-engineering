#!/usr/bin/env python3
"""R22-C2 counter: frozen T2 catalog verbs carrying a receipt-matched disposition.

Reads PROVINCE.md at REV, section `### Round-22 catalog dispositions`, table
`| verb | placement | probe | observed | receipt | reason |`. A T2 verb counts
as accounted only when exactly one row names it and:
  - placement is `frontier-blocked` or `adjacent`;
  - receipt is a lane path under RECEIPT_PREFIX present at REV;
  - the receipt decodes as strict JSON (duplicate members/non-finite refused)
    and is a REA CLI envelope whose meta.command equals `probe`;
  - `observed` matches the envelope: `error:<code>` needs ok==false and
    error.code==<code>; `ok-empty:<dotted.path>` needs ok==true and the list at
    data.<dotted.path> to be empty; `ok-field:<dotted.path>=<json>` needs
    ok==true and data.<dotted.path> to equal the JSON literal.
A row whose receipt contradicts its `observed` value is a mismatch.

Exit 0 when all T2 verbs are accounted with no mismatch, 1 otherwise, 2 when
the revision itself cannot be read.
"""
import argparse
import importlib.util
from pathlib import Path
import json
import re
import subprocess
import sys

T2 = ("inspect-packet-fields", "inspect-packet-capture", "inspect-pcap-client",
      "inspect-pcap-capture", "list-cutter-sessions", "cutter-command",
      "list-frida-devices", "list-frida-processes", "instrument-with-frida",
      "inspect-adb-package", "list-adb-services", "inspect-adb-window",
      "start-adb-activity", "stop-adb-app")
PLACEMENTS = {"frontier-blocked", "adjacent"}
RECEIPT_PREFIX = ".ufo/waves/round-22/evidence/c2/"
HEADING = "### Round-22 catalog dispositions"


def git_show(root, rev, path):
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True, check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8")


def strict(text):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError("duplicate_member: " + key)
            out[key] = value
        return out

    def constant(value):
        raise ValueError("nonfinite_number: " + value)
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def section_rows(province):
    lines = province.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.startswith(HEADING))
    except StopIteration:
        return []
    rows = []
    for line in lines[start + 1:]:
        if line.startswith("#"):
            break
        if not line.startswith("|"):
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) != 6 or cells[0] in ("verb", "") or set(cells[0]) <= set("-: "):
            continue
        rows.append(dict(zip(("verb", "placement", "probe", "observed", "receipt", "reason"), cells)))
    return rows


def dig(node, dotted):
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            raise KeyError(dotted)
        node = node[part]
    return node


def check(row, root, rev):
    if row["placement"] not in PLACEMENTS:
        return "bad_placement"
    if not row["reason"]:
        return "missing_reason"
    receipt = row["receipt"]
    if not receipt.startswith(RECEIPT_PREFIX) or ".." in receipt.split("/"):
        return "receipt_outside_prefix"
    text = git_show(root, rev, receipt)
    if text is None:
        return "receipt_absent"
    try:
        env = strict(text)
    except ValueError:
        return "receipt_unevaluable"
    if not isinstance(env, dict) or not isinstance(env.get("meta"), dict):
        return "receipt_not_envelope"
    if row["probe"] != row["verb"] or env["meta"].get("command") != row["probe"]:
        return "probe_mismatch"
    observed = row["observed"]
    try:
        if observed.startswith("error:"):
            ok = env.get("ok") is False and isinstance(env.get("error"), dict) \
                and env["error"].get("code") == observed[len("error:"):]
        elif observed.startswith("ok-empty:"):
            value = dig(env.get("data"), observed[len("ok-empty:"):])
            ok = env.get("ok") is True and isinstance(value, list) and value == []
        elif observed.startswith("ok-field:") and "=" in observed:
            dotted, literal = observed[len("ok-field:"):].split("=", 1)
            ok = env.get("ok") is True and dig(env.get("data"), dotted) == strict(literal)
        else:
            return "bad_observed_grammar"
    except (KeyError, ValueError):
        return "observed_mismatch"
    return "matched" if ok else "observed_mismatch"


def measure(root, rev):
    proc = subprocess.run(["git", "-C", root, "rev-parse", "--verify", f"{rev}^{{commit}}"],
                          capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise ValueError("invalid_revision")
    resolved = proc.stdout.strip()
    province = git_show(root, resolved, "PROVINCE.md")
    if province is None:
        raise ValueError("province_absent")
    rows = section_rows(province)
    per = {}
    for verb in T2:
        mine = [row for row in rows if row["verb"] == verb]
        if not mine:
            per[verb] = {"status": "unaccounted"}
        elif len(mine) > 1:
            per[verb] = {"status": "duplicate_rows"}
        else:
            per[verb] = {"status": check(mine[0], root, resolved), "row": mine[0]}
    foreign = sorted({row["verb"] for row in rows} - set(T2))
    accounted = [v for v in T2 if per[v]["status"] == "matched"]
    mismatched = [v for v in T2 if per[v]["status"] not in ("matched", "unaccounted")]
    return {"rev": resolved, "claim": "R22-C2", "t2_total": len(T2),
            "accounted": accounted, "accounted_count": len(accounted),
            "mismatched": mismatched, "per_verb": per, "foreign_rows": foreign,
            "limit": "receipt/row agreement at one revision; not provider availability over time"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root")
    parser.add_argument("--rev")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        root = Path(__file__).resolve().parents[4]
        spec = importlib.util.spec_from_file_location("r22_c2_fixtures", root / ".ufo/waves/round-22/tools/counter-fixtures.py")
        fixtures = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fixtures)
        result, code = fixtures.run("C2", Path(__file__).resolve(), root)
        print(json.dumps(result, sort_keys=True))
        return code
    if not args.root or not args.rev:
        parser.error("--root and --rev required unless --selftest")
    try:
        out = measure(args.root, args.rev)
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"finding": "unevaluable", "error": str(error)}))
        return 2
    print(json.dumps(out, sort_keys=True))
    clean = out["accounted_count"] == out["t2_total"] and not out["mismatched"] and not out["foreign_rows"]
    return 0 if clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
