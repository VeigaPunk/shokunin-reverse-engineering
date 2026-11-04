#!/usr/bin/env python3
"""capsule-audit.py - round-72 instrument (R72-C3 operability).

Standalone reader for a retained child-environment capsule: given the capsule
(JSON Lines) and the summary a receipt carries about it, re-derive every
property from the capsule bytes and adjudicate the seven clauses (see
`capsule_audit.py`).  The producer's summary is never trusted; a lying summary
over a polluted capsule fails with the clause that contradicts it.

Modes:
  --capsule <log> [--audit <summary.json>] [--run-root <dir>]
        adjudicate one capsule; exit 0 clean, 1 each failure named, 2 unreadable
  --tamper-battery --capsule <genuine log> --audit <genuine summary> --work <dir>
        cut the seven tampered shapes from the genuine bytes, require the
        genuine capsule accepted and every shape rejected with its declared
        clause; exit 0 met, 1 a shape accepted or a clause unnamed
  --selftest
        the pure clauses and the shape cutter over in-memory fixtures

Scratch discipline: every battery file is written under --work (a mkdtemp of
the run), never /tmp; the instrument writes nothing beside its inputs.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capsule_audit  # noqa: E402

TOOL = "tools/round-72/capsule-audit.py"
EXPECTED_SHAPES = ("log_sha256", "records", "keys", "canary", "home_under_run",
                   "tmpdir_under_run", "children")


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: summary is not an object")
    return payload


def adjudicate(capsule: str, summary: dict, run_root: str | None,
               out: str | None) -> int:
    result = capsule_audit.audit(capsule, summary, run_root=run_root)
    text = json.dumps(result, indent=1, sort_keys=True)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    if "unevaluable" in result:
        return 2
    return 0 if result["ok"] else 1


def tamper_battery(capsule: str, summary: dict, work: str,
                   out: str | None) -> int:
    if not os.path.isdir(work):
        print(json.dumps({"unevaluable": f"work is not a directory: {work}"}),
              file=sys.stderr)
        return 2
    try:
        with open(capsule, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        print(json.dumps({"unevaluable": f"capsule unreadable: {exc.__class__.__name__}"}),
              file=sys.stderr)
        return 2
    want = capsule_audit.normalize_summary(summary)
    root = want.get("run_root")
    if not isinstance(root, str) or not root:
        print(json.dumps({"unevaluable": "summary names no run root"}), file=sys.stderr)
        return 2
    scratch = tempfile.mkdtemp(prefix="capsule-battery-", dir=work)
    genuine = capsule_audit.audit(capsule, summary, run_root=root)
    rows = []
    cut = capsule_audit.shapes(data, root)
    for name, (payload, clause) in cut.items():
        path = os.path.join(scratch, f"shape-{name}.jsonl")
        with open(path, "wb") as fh:
            fh.write(payload)
        result = capsule_audit.audit(path, summary, run_root=root)
        rows.append({"shape": name, "declared_clause": clause,
                     "path": path, "accepted": result["ok"],
                     "rejected": not result["ok"],
                     "failures": result["failures"],
                     "clause_found": clause in result["failures"],
                     "sha256": result.get("sha256")})
    missing = [name for name in EXPECTED_SHAPES if name not in cut]
    accepted = [r["shape"] for r in rows if r["accepted"]]
    unnamed = [r["shape"] for r in rows if not r["clause_found"]]
    ok = (genuine["ok"] is True and not missing and not accepted and not unnamed
          and len(rows) == len(EXPECTED_SHAPES))
    result = {"instrument": TOOL, "capsule": capsule, "genuine": {
                  "ok": genuine["ok"], "records": genuine["records"],
                  "sha256": genuine["sha256"], "failures": genuine["failures"]},
              "shapes": rows, "missing_shapes": missing,
              "accepted_shapes": accepted, "unnamed_clause": unnamed,
              "target": len(EXPECTED_SHAPES), "rejected": sum(
                  1 for r in rows if r["rejected"]),
              "work_dir": scratch, "ok": bool(ok)}
    text = json.dumps(result, indent=1, sort_keys=True)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if ok else 1


def selftest() -> int:
    cases: dict[str, bool] = {}
    root = "/run/root"
    good_env = {"HOME": os.path.join(root, "home"), "LANG": "C",
                "PATH": "/usr/bin", "TMPDIR": os.path.join(root, "tmp")}
    records = [{"argv": ["/usr/bin/git", "show"], "env": dict(good_env)},
               {"argv": ["/usr/bin/readelf", "-h"], "env": dict(good_env)}]
    data = ("\n".join(json.dumps(r) for r in records) + "\n").encode()
    import hashlib
    summary = {"records": 2, "log_sha256": hashlib.sha256(data).hexdigest(),
               "exact_key_sets": True, "canary_absent": True,
               "home_under_run": True, "tmpdir_under_run": True,
               "children": {"git": 1, "readelf": 1}, "original_run_root": root}
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "capsule.jsonl")
        with open(path, "wb") as fh:
            fh.write(data)
        cases["genuine-clean"] = capsule_audit.audit(path, summary, root)["ok"] is True
        lying = dict(summary, records=3)
        cases["records-mismatch"] = "records" in capsule_audit.audit(
            path, lying, root)["failures"]
        lying_canary = dict(summary, canary_absent=False)
        cases["summary-canary-lie"] = "canary" in capsule_audit.audit(
            path, lying_canary, root)["failures"]
        cut = capsule_audit.shapes(data, root)
        cases["shape-count"] = set(cut) == set(EXPECTED_SHAPES)
        for name, (payload, clause) in cut.items():
            shape_path = os.path.join(tmp, f"shape-{name}.jsonl")
            with open(shape_path, "wb") as fh:
                fh.write(payload)
            result = capsule_audit.audit(shape_path, summary, root)
            cases[f"shape-{name}-rejected"] = (not result["ok"]
                                               and clause in result["failures"])
        cases["containment-sibling"] = (capsule_audit.under("/w/run", "/w/run-out/h") is False
                                        and capsule_audit.under("/w/run", "/w/run/home") is True)
        cases["schema-both-read"] = (
            capsule_audit.normalize_summary(summary)["canary_present"] is False
            and capsule_audit.normalize_summary(
                {"canary_present": False, "keys": list(capsule_audit.ALLOW)})["keys_exact"] is True)
    failed = [name for name, ok in cases.items() if not ok]
    print(json.dumps({"selftest": TOOL, "cases": len(cases),
                      "failed": failed, "ok": not failed},
                     indent=1, sort_keys=True))
    return 0 if not failed else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--capsule")
    ap.add_argument("--audit")
    ap.add_argument("--run-root")
    ap.add_argument("--work")
    ap.add_argument("--json-out")
    ap.add_argument("--tamper-battery", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.capsule:
        print("capsule-audit: --capsule is required", file=sys.stderr)
        return 2
    summary = {}
    if args.audit:
        try:
            summary = load_json(args.audit)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(json.dumps({"unevaluable": f"summary unreadable: {exc.__class__.__name__}"}),
                  file=sys.stderr)
            return 2
    if args.tamper_battery:
        if not args.work:
            print("capsule-audit: --tamper-battery requires --work", file=sys.stderr)
            return 2
        return tamper_battery(args.capsule, summary, args.work, args.json_out)
    return adjudicate(args.capsule, summary, args.run_root, args.json_out)


if __name__ == "__main__":
    sys.exit(main())
