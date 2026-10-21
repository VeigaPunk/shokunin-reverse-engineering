#!/usr/bin/env python3
"""R22-C2 counter: frozen T2 catalog verbs carrying a receipt-matched disposition.

Reads PROVINCE.md at REV, section `### Round-22 catalog dispositions`, table
`| verb | placement | probe | observed | receipt | reason |`. A T2 verb counts
as accounted only when exactly one row names it and:
  - placement is `frontier-blocked` or `adjacent`;
  - receipt is a lane path under RECEIPT_PREFIX present at REV;
  - the receipt decodes as strict JSON (duplicate members/non-finite refused)
    and is a REA CLI envelope whose meta.command equals `probe`, with
    `probe` equal to the row's `verb`;
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
import subprocess
import sys
import math
from decimal import Decimal
import os
import hashlib
SELFTEST_MANIFEST_SHA256 = "1abdd9df347610a77f01afbe157c7fdbfb4c90bc2e26b6b3ecebd08fbd930bb8"

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
    def number(value):
        if not math.isfinite(float(value)):
            raise ValueError("nonfinite_number: " + value)
        return Decimal(value)
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant, parse_float=number)


def section_rows(province):
    lines = []
    fence = None
    comment = False
    for line in province.splitlines():
        if fence is None:
            visible = ""
            remaining = line
            while remaining:
                if comment:
                    _, end, remaining = remaining.partition("-->")
                    if not end:
                        break
                    comment = False
                else:
                    before, start_comment, remaining = remaining.partition("<!--")
                    visible += before
                    if not start_comment:
                        break
                    comment = True
            line = visible
        text = line.lstrip(" ")
        if len(line)-len(text) <= 3 and text[:1] in ("`", "~"):
            mark = text[0]
            count = len(text)-len(text.lstrip(mark))
            if count >= 3:
                if fence is None:
                    fence = (mark, count)
                elif mark == fence[0] and count >= fence[1] and not text[count:].strip():
                    fence = None
                continue
        if fence is None:
            lines.append(line)
    starts = [i for i, line in enumerate(lines) if line == HEADING]
    if not starts:
        return []
    if len(starts) != 1:
        raise ValueError("ambiguous_disposition_sections")
    start = starts[0]
    rows = []
    for line in lines[start + 1:]:
        if line.startswith("#"):
            break
        if not line.startswith("|"):
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if cells == ["verb","placement","probe","observed","receipt","reason"]:
            continue
        if len(cells)==6 and all(cell and set(cell)<=set("-: ") for cell in cells):
            continue
        if len(cells) != 6:
            raise ValueError("malformed_disposition_row")
        rows.append(dict(zip(("verb", "placement", "probe", "observed", "receipt", "reason"), cells)))
    return rows


def dig(node, dotted):
    if not dotted or any(not part for part in dotted.split(".")):
        raise KeyError(dotted)
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            raise KeyError(dotted)
        node = node[part]
    return node


def same_json(actual, expected):
    if isinstance(actual, bool) or isinstance(expected, bool):
        return type(actual) is type(expected) and actual == expected
    if isinstance(actual, dict) and isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(same_json(actual[key], expected[key]) for key in actual)
    if isinstance(actual, list) and isinstance(expected, list):
        return len(actual) == len(expected) and all(same_json(a, b) for a, b in zip(actual, expected))
    return actual == expected


def check(row, root, rev):
    if row["placement"] not in PLACEMENTS:
        return "bad_placement"
    if not row["reason"]:
        return "missing_reason"
    receipt = row["receipt"]
    if not receipt.startswith(RECEIPT_PREFIX) or ".." in receipt.split("/"):
        return "receipt_outside_prefix"
    try:
        text = git_show(root, rev, receipt)
    except UnicodeError:
        return "receipt_unevaluable"
    if text is None:
        return "receipt_absent"
    try:
        env = strict(text)
    except (ValueError, RecursionError):
        return "receipt_unevaluable"
    if not isinstance(env, dict) or not isinstance(env.get("meta"), dict):
        return "receipt_not_envelope"
    if row["probe"] != row["verb"] or env["meta"].get("command") != row["probe"]:
        return "probe_mismatch"
    observed = row["observed"]
    try:
        if observed.startswith("error:"):
            if not observed[len("error:"):]:
                return "bad_observed_grammar"
            ok = env.get("ok") is False and isinstance(env.get("error"), dict) \
                and env["error"].get("code") == observed[len("error:"):]
        elif observed.startswith("ok-empty:"):
            value = dig(env.get("data"), observed[len("ok-empty:"):])
            ok = env.get("ok") is True and isinstance(value, list) and value == []
        elif observed.startswith("ok-field:") and "=" in observed:
            dotted, literal = observed[len("ok-field:"):].split("=", 1)
            ok = env.get("ok") is True and same_json(dig(env.get("data"), dotted), strict(literal))
        else:
            return "bad_observed_grammar"
    except (KeyError, ValueError, RecursionError):
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
    clean = len(accounted) == len(T2) and not mismatched and not foreign
    return {"rev": resolved, "claim": "R22-C2", "finding": "dispositions_complete" if clean else "dispositions_incomplete", "t2_total": len(T2),
            "accounted": accounted, "accounted_count": len(accounted),
            "mismatched": mismatched, "per_verb": per, "foreign_rows": foreign,
            "limit": "only observed fields/codes are compared; reason/placement semantics and run metadata require manual review; not provider availability over time"}


def main():
    for key in tuple(os.environ):
        if key.startswith("GIT_"):
            del os.environ[key]
    os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root")
    parser.add_argument("--rev")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        root = Path(args.root).resolve() if args.root else next(
            (path for path in Path(__file__).resolve().parents if
             (path / ".ufo/waves/round-22/tools/counter-fixtures.py").is_file()), None)
        if root is None:
            print(json.dumps({"finding":"unevaluable","error":"selftest_root_required"}))
            return 2
        try:
            manifest_bytes=(root/".ufo/waves/round-22/frozen/expected-v2.json").read_bytes()
            if hashlib.sha256(manifest_bytes).hexdigest()!=SELFTEST_MANIFEST_SHA256:
                raise ValueError("manifest_digest")
            manifest=json.loads(manifest_bytes)
            observed_inputs={}
            for rel,digest in manifest["inputs"].items():
                observed_inputs[rel]=hashlib.sha256((root/rel).read_bytes()).hexdigest()
                if observed_inputs[rel]!=digest:
                    raise ValueError("input_digest: "+rel)
        except (OSError,UnicodeError,ValueError,KeyError) as error:
            print(json.dumps({"finding":"snapshot_tampered","error":str(error)}))
            return 2
        spec = importlib.util.spec_from_file_location("r22_c2_fixtures", root / ".ufo/waves/round-22/tools/counter-fixtures.py")
        fixtures = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fixtures)
        result, code = fixtures.run("C2", Path(__file__).resolve(), root)
        result["selftest_manifest_sha256"]=SELFTEST_MANIFEST_SHA256
        result["selftest_input_sha256"]=observed_inputs
        print(json.dumps(result, sort_keys=True))
        return code
    if not args.root or not args.rev:
        parser.error("--root and --rev required unless --selftest")
    try:
        out = measure(args.root, args.rev)
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        print(json.dumps({"finding": "unevaluable", "error": str(error)}))
        return 2
    print(json.dumps(out, sort_keys=True))
    clean = out["accounted_count"] == out["t2_total"] and not out["mismatched"] and not out["foreign_rows"]
    return 0 if clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
