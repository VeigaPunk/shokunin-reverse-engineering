#!/usr/bin/env python3
"""receipt-provenance.py - round-80 instrument (R80-C2 freshness).

Decides whether every landing-class receipt's declared instrument digest names a
COMMITTED blob of the instrument it names.  Round 79's landing receipt
`.ufo/waves/round-79/l1/scores/c2-at-landing.json` recorded
`instrument.sha256 a0044c4c…`, which matches no committed revision of
`tools/round-79/pointer-bind.py`; the round-79 non-author spot-check found it by
reading, not by a check.  This instrument makes that class checkable.

Population: `.ufo/waves/round-<N>/l1/scores/*.json` for N in
[--from-round, --to-round], read from `--rev`, excluding any path containing
`/attacks/` (declared forged fixtures live there).  A receipt enters the
population only when it is a JSON object carrying `instrument.path` and a 64-hex
`instrument.sha256`.

Rule: the digest is provenance-bound iff it equals
  * the blob at the lane branch tip,
  * the blob at the receipt's own declared `rev`/`record.rev` (only when that is
    a 40-hex commit: symbolic names are not committed revisions), or
  * the blob at any committed revision of that path (`git rev-list --all --`).
A digest that matches only the working tree is NOT committed.  One receipt is a
declared negative control (`prov-forged-instrument.json`, round 69's forged
instrument) and must stay flagged.

Modes
  (no mode)          sweep and score the population
  --selftest         the rule's cases as a selftest
  --validate FILE    re-derive every count of a saved receipt
Exit: 0 no unexpected flag; 1 an unexpected flag or a validate defect; 2
could-not-evaluate (no rev, unreadable population).
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
SCHEMA = "kaidoku-r80-receipt-provenance-v1"
EXPECTED_CONTROLS = ("prov-forged-instrument.json",)
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
RECEIPT = re.compile(r"^\.ufo/waves/round-(\d+)/l1/scores/.+\.json$")


class Unevaluable(Exception):
    """Exit-2 class: the population cannot be read."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: str, data) -> None:
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")


def git(root: str, *argv: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", root, *argv], capture_output=True)


def git_bytes(root: str, rev: str, path: str) -> bytes | None:
    proc = git(root, "show", f"{rev}:{path}")
    return proc.stdout if proc.returncode == 0 else None


def git_commits(root: str, path: str) -> list[str]:
    proc = git(root, "rev-list", "--all", "--", path)
    if proc.returncode != 0:
        return []
    return [line for line in proc.stdout.decode().split() if HEX40.match(line)]


def list_receipts(root: str, rev: str, lo: int, hi: int) -> list[str]:
    proc = git(root, "ls-tree", "-r", "--name-only", rev)
    if proc.returncode != 0:
        raise Unevaluable(f"cannot list {rev}")
    out = []
    for path in proc.stdout.decode().splitlines():
        if "/attacks/" in path:
            continue
        match = RECEIPT.match(path)
        if not match:
            continue
        if lo <= int(match.group(1)) <= hi:
            out.append(path)
    return sorted(out)


class Resolver:
    """Committed-blob oracle, cached per (path, rev) and per path history."""

    def __init__(self, root: str, tip: str):
        self.root = root
        self.tip = tip
        self._blob: dict[tuple[str, str], str | None] = {}
        self._history: dict[str, list[str]] = {}

    def blob(self, path: str, rev: str) -> str | None:
        key = (path, rev)
        if key not in self._blob:
            data = git_bytes(self.root, rev, path)
            self._blob[key] = None if data is None else sha256_bytes(data)
        return self._blob[key]

    def history(self, path: str) -> list[str]:
        if path not in self._history:
            self._history[path] = git_commits(self.root, path)
        return self._history[path]

    def bound_at(self, path: str, digest: str, rev: str | None) -> str:
        """The revision the digest is bound at, or "" when unbound."""
        if self.blob(path, self.tip) == digest:
            return self.tip
        if rev and HEX40.match(rev) and self.blob(path, rev) == digest:
            return rev
        for candidate in self.history(path):
            if candidate == self.tip:
                continue
            if self.blob(path, candidate) == digest:
                return candidate
        return ""

    def safe_path(self, path: str) -> bool:
        return bool(path) and not path.startswith("/") and ".." not in path.split("/")


def safe_instrument_path(path) -> bool:
    return isinstance(path, str) and bool(path) and not path.startswith("/") \
        and ".." not in path.split("/")


def classify(entries: list[dict], resolver: Resolver) -> dict:
    """Score already-loaded entries; no git access, so the selftest can inject."""
    rows: list[dict] = []
    for entry in entries:
        path = entry.get("path", "")
        inst = entry.get("instrument") or {}
        ipath = inst.get("path")
        digest = inst.get("sha256")
        row = {"receipt": path, "instrument": ipath, "sha256": digest,
               "declared_rev": entry.get("rev") or "", "verdict": "",
               "matched_rev": "", "reason": ""}
        if not safe_instrument_path(ipath):
            row["verdict"] = "unsafe-instrument-path"
            row["reason"] = "instrument path escapes the lane or is not a relative path"
        elif not (isinstance(digest, str) and HEX64.match(digest)):
            row["verdict"] = "unparsed-digest"
            row["reason"] = "instrument.sha256 is not a 64-hex digest"
        else:
            bound = resolver.bound_at(ipath, digest, row["declared_rev"])
            if bound:
                row["verdict"] = "bound"
                row["matched_rev"] = bound
            else:
                row["verdict"] = "uncommitted-digest"
                row["reason"] = ("the digest matches no committed blob of the "
                                 "instrument at --rev, the tip or its history")
        row["expected_control"] = pathlib.PurePosixPath(path).name in EXPECTED_CONTROLS
        rows.append(row)
    flagged = [r for r in rows if r["verdict"] != "bound"]
    expected = [r for r in flagged if r["expected_control"]]
    unexpected = [r for r in flagged if not r["expected_control"]]
    return {"rows": rows, "receipts": len(rows), "flagged": len(flagged),
            "expected_control_flags": len(expected),
            "unexpected": len(unexpected),
            "unexpected_receipts": [r["receipt"] for r in unexpected]}


def collect(root: str, rev: str, lo: int, hi: int) -> list[dict]:
    entries: list[dict] = []
    for path in list_receipts(root, rev, lo, hi):
        data = git_bytes(root, rev, path)
        if data is None:
            continue
        try:
            record = json.loads(data)
        except ValueError:
            continue
        if not isinstance(record, dict):
            continue
        inst = record.get("instrument")
        if not isinstance(inst, dict):
            continue
        entries.append({"path": path, "instrument": inst,
                        "rev": record.get("rev") or
                        (record.get("record") or {}).get("rev") or ""})
    return entries


def sweep(root: str, rev: str, lo: int, hi: int) -> dict:
    if not HEX40.match(rev):
        raise Unevaluable(f"--rev {rev!r} is not a 40-hex commit")
    tip = git(root, "rev-parse", rev)
    if tip.returncode != 0:
        raise Unevaluable(f"cannot resolve {rev}")
    tip = tip.stdout.decode().strip()
    resolver = Resolver(root, tip)
    scored = classify(collect(root, rev, lo, hi), resolver)
    scored.update({
        "schema": SCHEMA,
        "round": ROUND,
        "checked_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "instrument": {"path": "tools/round-80/receipt-provenance.py",
                       "sha256": sha256_bytes(pathlib.Path(__file__).read_bytes())},
        "rev": rev,
        "tip": tip,
        "from_round": lo,
        "to_round": hi,
        "expected_controls": list(EXPECTED_CONTROLS),
    })
    scored["would_pass"] = scored["unexpected"] == 0 and scored["receipts"] > 0
    scored["ok"] = scored["would_pass"]
    return scored


def validate_receipt(receipt: dict) -> dict:
    defects: list[str] = []
    rows = receipt.get("rows") or []
    if not isinstance(rows, list):
        return {"defects": ["rows is not a list"]}
    receipts = len(rows)
    if receipt.get("receipts") != receipts:
        defects.append("receipts does not re-derive from rows")
    flagged = [r for r in rows if r.get("verdict") != "bound"]
    expected = [r for r in flagged if r.get("expected_control")]
    unexpected = [r for r in flagged if not r.get("expected_control")]
    if receipt.get("flagged") != len(flagged):
        defects.append("flagged does not re-derive from rows")
    if receipt.get("expected_control_flags") != len(expected):
        defects.append("expected_control_flags does not re-derive from rows")
    if receipt.get("unexpected") != len(unexpected):
        defects.append("unexpected does not re-derive from rows")
    if sorted(receipt.get("unexpected_receipts") or []) != \
            sorted(r.get("receipt") for r in unexpected):
        defects.append("unexpected_receipts does not re-derive from rows")
    for row in rows:
        if row.get("verdict") not in ("bound", "uncommitted-digest",
                                      "unsafe-instrument-path", "unparsed-digest"):
            defects.append(f"{row.get('receipt')}: unknown verdict")
        if row.get("verdict") == "bound" and not HEX40.match(row.get("matched_rev") or ""):
            defects.append(f"{row.get('receipt')}: bound without a 40-hex revision")
        if row.get("verdict") == "bound" and not safe_instrument_path(row.get("instrument")):
            defects.append(f"{row.get('receipt')}: bound with an unsafe instrument path")
        if row.get("verdict") != "bound" and not row.get("reason"):
            defects.append(f"{row.get('receipt')}: flagged without a reason")
    if not HEX40.match(receipt.get("rev") or ""):
        defects.append("rev is not a 40-hex commit")
    if not receipt.get("checked_at"):
        defects.append("checked_at is absent")
    inst = receipt.get("instrument") or {}
    if inst.get("sha256") != sha256_bytes(pathlib.Path(__file__).read_bytes()):
        defects.append("instrument sha256 is not this file's digest")
    if receipt.get("ok") and receipt.get("unexpected"):
        defects.append("ok true with an unexpected flag")
    if receipt.get("ok") and receipts == 0:
        defects.append("ok true over an empty population")
    if receipt.get("would_pass") and not receipt.get("ok"):
        defects.append("would_pass true without ok")
    return {"defects": defects, "receipts": receipts,
            "flagged": len(flagged), "unexpected": len(unexpected)}


class FakeResolver:
    """Selftest oracle: (path, rev) -> digest, tip fixed."""

    def __init__(self, tip: str, blobs: dict, history: dict):
        self.tip = tip
        self.blobs = blobs
        self._history = history

    def blob(self, path, rev):
        return self.blobs.get((path, rev))

    def history(self, path):
        return self._history.get(path, [])

    def bound_at(self, path, digest, rev):
        if self.blob(path, self.tip) == digest:
            return self.tip
        if rev and HEX40.match(rev) and self.blob(path, rev) == digest:
            return rev
        for candidate in self.history(path):
            if candidate != self.tip and self.blob(path, candidate) == digest:
                return candidate
        return ""


def selftest() -> int:
    cases: list[dict] = []

    def case(name, got, want):
        cases.append({"case": name, "got": got, "want": want, "pass": got == want})

    tip = "a" * 40
    old = "b" * 40
    dig_tip, dig_old, dig_wt = "1" * 64, "2" * 64, "3" * 64
    inst = "tools/round-79/pointer-bind.py"
    res = FakeResolver(tip, {(inst, tip): dig_tip, (inst, old): dig_old},
                       {inst: [tip, old]})

    def entry(path, digest, rev=""):
        return {"path": path, "instrument": {"path": inst, "sha256": digest},
                "rev": rev}

    def one(entries, r=res):
        return classify(entries, r)

    case("green-tip-digest",
         one([entry(".ufo/waves/round-79/l1/scores/a.json", dig_tip)])["flagged"], 0)
    case("green-history-digest",
         one([entry(".ufo/waves/round-79/l1/scores/a.json", dig_old)])["flagged"], 0)
    case("green-declared-rev-digest",
         one([entry(".ufo/waves/round-79/l1/scores/a.json", dig_old, old)])["flagged"], 0)
    case("red-uncommitted-digest",
         one([entry(".ufo/waves/round-79/l1/scores/a.json", dig_wt)])["unexpected"], 1)
    case("red-working-tree-only-is-not-committed",
         one([entry(".ufo/waves/round-79/l1/scores/a.json", dig_wt, "main")])["unexpected"], 1)
    case("red-symbolic-rev-not-a-commit",
         one([entry(".ufo/waves/round-79/l1/scores/a.json", dig_wt, "@HEAD@")])["unexpected"], 1)
    case("green-declared-control-counted",
         one([entry(".ufo/waves/round-69/l1/scores/prov-forged-instrument.json",
                    dig_wt)])["expected_control_flags"], 1)
    case("red-path-escape-named",
         one([{"path": ".ufo/waves/round-79/l1/scores/a.json",
               "instrument": {"path": "../etc/passwd", "sha256": dig_tip},
               "rev": ""}])["rows"][0]["verdict"], "unsafe-instrument-path")
    case("red-absolute-path-named",
         one([{"path": ".ufo/waves/round-79/l1/scores/a.json",
               "instrument": {"path": "/etc/passwd", "sha256": dig_tip},
               "rev": ""}])["rows"][0]["verdict"], "unsafe-instrument-path")
    case("red-unparsed-digest",
         one([{"path": ".ufo/waves/round-79/l1/scores/a.json",
               "instrument": {"path": inst, "sha256": "zz"},
               "rev": ""}])["rows"][0]["verdict"], "unparsed-digest")
    case("green-population-rule",
         [bool(RECEIPT.match(".ufo/waves/round-79/l1/scores/x.json")),
          bool(RECEIPT.match(".ufo/waves/round-79/attacks/a1/x.json")),
          bool(RECEIPT.match(".ufo/waves/round-79/w1/x.json"))],
         [True, False, False])

    # validate: a consistent receipt is clean, a tampered count is named
    good = one([entry(".ufo/waves/round-79/l1/scores/a.json", dig_wt)])
    good.update({"rev": tip, "checked_at": "2026-11-04T00:00:00-03:00",
                 "instrument": {"path": "tools/round-80/receipt-provenance.py",
                                "sha256": sha256_bytes(
                                    pathlib.Path(__file__).read_bytes())},
                 "ok": False, "would_pass": False,
                 "unexpected_receipts": good["unexpected_receipts"]})
    case("green-validate-consistent", validate_receipt(good)["defects"], [])
    tampered = json.loads(json.dumps(good))
    tampered["flagged"] = 0
    case("red-validate-tampered-count",
         validate_receipt(tampered)["defects"][:1],
         ["flagged does not re-derive from rows"])
    empty = json.loads(json.dumps(good))
    empty.update({"rows": [], "receipts": 0, "flagged": 0, "unexpected": 0,
                  "expected_control_flags": 0, "unexpected_receipts": [],
                  "ok": True, "would_pass": True})
    case("red-validate-empty-population-ok",
         validate_receipt(empty)["defects"][:1],
         ["ok true over an empty population"])

    failures = [c for c in cases if not c["pass"]]
    for case_ in cases:
        print(json.dumps(case_, sort_keys=True))
    print(f"SELFTEST cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--from-round", type=int, default=60)
    ap.add_argument("--to-round", type=int, default=79)
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--validate")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.validate:
        data = json.loads(pathlib.Path(args.validate).read_text())
        result = validate_receipt(data)
        print(json.dumps(result, sort_keys=True))
        return 0 if not result["defects"] else 1
    try:
        receipt = sweep(args.root, args.rev or "", args.from_round, args.to_round)
    except Unevaluable as exc:
        print(json.dumps({"unevaluable": str(exc), "exit": 2}))
        return 2
    check = validate_receipt(receipt)
    receipt["validate"] = check
    if check["defects"]:
        receipt["ok"] = False
    if args.json_out:
        write_json(args.json_out, receipt)
    print(json.dumps({k: receipt[k] for k in
                      ("receipts", "flagged", "expected_control_flags",
                       "unexpected", "ok")}, sort_keys=True))
    print(json.dumps({"unexpected_receipts": receipt["unexpected_receipts"],
                      "validate_defects": check["defects"]}, sort_keys=True))
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
