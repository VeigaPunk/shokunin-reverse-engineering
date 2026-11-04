#!/usr/bin/env python3
"""capsule_audit.py - round-72 library (R72-C3 operability).

The raw-witness capsule audit.  A capsule is the per-child environment log a
capture launcher writes (one JSON object per line: `argv` + `env`); a summary
is what a receipt carries about it (`child_env_observed`, or the retained
`c1-env-audit.json` shape).  The summary is a claim; this reader re-derives
every property from the capsule's own bytes and then compares.

Clauses (each re-derived, never trusted):
  log_sha256        sha256 of the capsule bytes equals the summary's digest
  records           the parsed record count equals the summary's count
  keys              every record's key set is exactly HOME/LANG/PATH/TMPDIR
  canary            no record carries KAIDOKU_ENV_CANARY
  home_under_run    every HOME is a descendant of the run root
  tmpdir_under_run  every TMPDIR is a descendant of the run root
  children          the child-class census equals the summary's census

The run root is the summary's own `run_root`/`original_run_root` unless the
caller passes one.  Containment is `os.path.commonpath`, never a string
prefix (QUALITY #119).  A failed clause is named; the audit never repairs its
input and never writes beside it.
"""

from __future__ import annotations

import hashlib
import json
import os

ALLOW = ("HOME", "LANG", "PATH", "TMPDIR")
CANARY = "KAIDOKU_ENV_CANARY"


def under(root, path) -> bool:
    """Descendant test without the sibling-prefix false green (QUALITY #119)."""
    try:
        root_abs = os.path.abspath(str(root))
        return os.path.commonpath([root_abs, os.path.abspath(str(path))]) == root_abs
    except (TypeError, ValueError):
        return False


def parse_capsule(data: bytes) -> tuple[list[dict], list[str]]:
    """Records and parse errors from capsule bytes (JSON Lines, one object each)."""
    records: list[dict] = []
    errors: list[str] = []
    for lineno, raw in enumerate(data.split(b"\n"), 1):
        if not raw.strip():
            continue
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"line {lineno}: {exc.__class__.__name__}")
            continue
        if not isinstance(payload, dict):
            errors.append(f"line {lineno}: not an object")
            continue
        records.append(payload)
    return records, errors


def child_census(records: list[dict]) -> dict:
    out: dict[str, int] = {}
    for rec in records:
        argv = rec.get("argv") or ["?"]
        name = os.path.basename(str(argv[0]))
        out[name] = out.get(name, 0) + 1
    return out


def summarize(records: list[dict], run_root: str | None) -> dict:
    """Every clause input re-derived from the records themselves."""
    envs = [rec.get("env") if isinstance(rec.get("env"), dict) else {}
            for rec in records]
    keys_exact = bool(envs) and all(sorted(e) == sorted(ALLOW) for e in envs)
    canary_present = any(CANARY in e for e in envs)
    home_ok = bool(envs) and bool(run_root) and all(
        under(run_root, e.get("HOME", "")) for e in envs)
    tmp_ok = bool(envs) and bool(run_root) and all(
        under(run_root, e.get("TMPDIR", "")) for e in envs)
    return {"records": len(records), "keys_exact": keys_exact,
            "canary_present": canary_present, "home_under_run": home_ok,
            "tmpdir_under_run": tmp_ok,
            "keys": sorted({k for e in envs for k in e}),
            "children": child_census(records), "run_root": run_root}


def normalize_summary(summary: dict) -> dict:
    """Read either summary schema into the audit's clause fields."""
    if not isinstance(summary, dict):
        return {}
    if "exact_key_sets" in summary or "original_run_root" in summary:
        return {"records": summary.get("records"),
                "log_sha256": summary.get("log_sha256"),
                "keys_exact": summary.get("exact_key_sets"),
                "canary_present": (not summary.get("canary_absent")
                                   if isinstance(summary.get("canary_absent"), bool)
                                   else None),
                "home_under_run": summary.get("home_under_run"),
                "tmpdir_under_run": summary.get("tmpdir_under_run"),
                "children": summary.get("children"),
                "run_root": summary.get("original_run_root")
                or summary.get("run_root")}
    return {"records": summary.get("records"),
            "log_sha256": summary.get("log_sha256"),
            "keys_exact": (sorted(summary.get("keys") or []) == sorted(ALLOW)
                           if summary.get("keys") is not None else None),
            "canary_present": summary.get("canary_present"),
            "home_under_run": summary.get("home_under_run"),
            "tmpdir_under_run": summary.get("tmpdir_under_run"),
            "children": summary.get("children"),
            "run_root": summary.get("run_root")}


def audit(log_path: str, summary: dict, run_root: str | None = None) -> dict:
    """Adjudicate one capsule against its summary; every failure names a clause."""
    try:
        with open(log_path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        return {"ok": False, "unevaluable": f"capsule unreadable: {exc.__class__.__name__}",
                "path": log_path, "failures": ["unreadable"], "clauses": {}}
    digest = hashlib.sha256(data).hexdigest()
    records, parse_errors = parse_capsule(data)
    want = normalize_summary(summary)
    root = run_root or want.get("run_root")
    derived = summarize(records, root if isinstance(root, str) else None)
    claimed_sha = want.get("log_sha256")
    clauses: dict[str, bool | None] = {
        # None = the summary makes no byte-integrity claim, so the clause is
        # not evaluated; a claimed digest must equal the capsule's own bytes.
        "log_sha256": None if claimed_sha is None else claimed_sha == digest,
        "records": want.get("records") == derived["records"],
        "keys": derived["keys_exact"] and want.get("keys_exact") is not False,
        "canary": derived["canary_present"] is False
        and want.get("canary_present") is not True,
        "home_under_run": derived["home_under_run"],
        "tmpdir_under_run": derived["tmpdir_under_run"],
        "children": want.get("children") == derived["children"],
    }
    failures = []
    if parse_errors:
        failures.append("parse: " + "; ".join(parse_errors[:3]))
    for name, ok in clauses.items():
        if ok is False:
            failures.append(name)
    if not derived["records"]:
        failures.append("records: empty capsule")
    return {"ok": not failures, "path": log_path, "sha256": digest,
            "run_root": root, "records": derived["records"],
            "derived": derived, "clauses": clauses, "failures": failures,
            "parse_errors": parse_errors}


def shapes(data: bytes, run_root: str) -> dict[str, tuple[bytes, str]]:
    """Seven tampered capsules cut from the genuine bytes, each with its clause.

    Every shape keeps the genuine summary as the claim, so a reader that trusts
    the summary accepts it; the audit must reject it naming the clause.
    """
    records, _ = parse_capsule(data)
    text_records = [json.loads(line.decode("utf-8"))
                    for line in data.split(b"\n") if line.strip()]
    out: dict[str, tuple[bytes, str]] = {}

    def dump(rows: list[dict]) -> bytes:
        return ("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n").encode()

    out["log_sha256"] = (data + b"\n", "log_sha256")
    if records:
        out["records"] = (dump(text_records[:-1]), "records")
        polluted = json.loads(json.dumps(text_records))
        polluted[0].setdefault("env", {})["EXTRA_KEY"] = "1"
        out["keys"] = (dump(polluted), "keys")
        canary = json.loads(json.dumps(text_records))
        canary[0].setdefault("env", {})[CANARY] = "not-a-secret"
        out["canary"] = (dump(canary), "canary")
        escaped = json.loads(json.dumps(text_records))
        escaped[0].setdefault("env", {})["HOME"] = os.path.join(
            os.path.dirname(os.path.abspath(run_root)), "outside-home")
        out["home_under_run"] = (dump(escaped), "home_under_run")
        escaped_tmp = json.loads(json.dumps(text_records))
        escaped_tmp[0].setdefault("env", {})["TMPDIR"] = os.path.join(
            os.path.dirname(os.path.abspath(run_root)), "outside-tmp")
        out["tmpdir_under_run"] = (dump(escaped_tmp), "tmpdir_under_run")
        census = json.loads(json.dumps(text_records))
        census[0]["argv"] = ["/usr/bin/curl"]
        out["children"] = (dump(census), "children")
    return out
