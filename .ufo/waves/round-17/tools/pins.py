#!/usr/bin/env python3
"""pins.py — pre/post filesystem pins for retained runs (R16-PROVENANCE fix).

snapshot() records, for each given path, the sha256, size and mtime_ns of the
bytes observable at one instant. compare() checks two snapshots and reports
which paths changed, went missing, or errored.

A pin pair proves only "same bytes at two instants". It never proves a file
was unchanged throughout the interval between the snapshots — a file could be
modified and restored, and a file could even mutate between the stat and the
read inside a single snapshot (detected when size/mtime_ns move). That is the
point of the R16-PROVENANCE fix: round-16 statements such as "pins remained
unchanged during execution" asserted temporal stability the tooling never
measured. New receipts carry pre_taken_at_utc/post_taken_at_utc so the claim
is bounded to two instants.

Python 3 stdlib only. Runnable as `python3 -I pins.py ...`.
Exit codes: 0 emitted/equal, 1 snapshots differ (compare), 2 could-not-evaluate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

_CHUNK = 1 << 20


def _entry(path: str) -> dict:
    """Pin one path: sha256/size/mtime_ns, or {"error": ...} on failure."""
    try:
        st = os.stat(path)
    except OSError as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}
    try:
        digest = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(_CHUNK), b""):
                digest.update(chunk)
        st2 = os.stat(path)
    except OSError as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}
    if st.st_size != st2.st_size or st.st_mtime_ns != st2.st_mtime_ns:
        return {
            "error": "changed during read: size/mtime_ns differ before and after hashing"
        }
    return {
        "sha256": digest.hexdigest(),
        "size": st.st_size,
        "mtime_ns": st.st_mtime_ns,
    }


def snapshot(paths: list) -> dict:
    """Pin every path at this instant; keys are canonical absolute paths."""
    entries = {}
    for raw in paths:
        ap = os.path.realpath(raw)
        entries[ap] = _entry(ap)
    return {
        "taken_at_utc": datetime.now(timezone.utc).isoformat(timespec="microseconds"),
        "monotonic_ns": time.monotonic_ns(),
        "entries": entries,
    }


def compare(pre: dict, post: dict) -> dict:
    """Compare two snapshots. equal is false on any diff, missing, or error."""
    pre_entries = pre.get("entries") or {}
    post_entries = post.get("entries") or {}
    changed = []
    missing = []
    errors = []
    for path in sorted(set(pre_entries) | set(post_entries)):
        a = pre_entries.get(path)
        b = post_entries.get(path)
        if a is None or b is None:
            missing.append(path)
        elif "error" in a or "error" in b:
            # An errored path can never prove same-bytes. A FileNotFoundError
            # opposite a real entry means the file vanished: missing. Every
            # other error (even the same error on both sides) is unprovable.
            if ("error" not in a and str(b.get("error", "")).startswith("FileNotFoundError")) or \
               ("error" not in b and str(a.get("error", "")).startswith("FileNotFoundError")):
                missing.append(path)
            else:
                errors.append(path)
        elif a.get("sha256") != b.get("sha256") or a.get("size") != b.get("size"):
            changed.append(path)
    equal = not changed and not missing and not errors
    return {
        "equal": equal,
        "changed": changed,
        "missing": missing,
        "errors": errors,
        "pre_taken_at_utc": pre.get("taken_at_utc"),
        "post_taken_at_utc": post.get("taken_at_utc"),
    }


def _emit(obj) -> None:
    json.dump(obj, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")


def _cmd_snapshot(args) -> int:
    snap = snapshot(args.paths)
    out = os.path.abspath(args.out)
    tmp = out + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(snap, fh, sort_keys=True, indent=2)
            fh.write("\n")
        os.replace(tmp, out)
    except OSError as exc:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        _emit({"error": f"cannot write snapshot to {out}: {exc}"})
        return 2
    _emit(snap)
    return 0


def _load_snapshot(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    if not isinstance(doc, dict) or not isinstance(doc.get("entries"), dict):
        raise ValueError(f"{path}: not a pins snapshot (missing entries object)")
    if not all(isinstance(v, dict) for v in doc["entries"].values()):
        raise ValueError(f"{path}: entries must map paths to objects")
    return doc


def _cmd_compare(args) -> int:
    try:
        pre = _load_snapshot(args.pre)
        post = _load_snapshot(args.post)
    except (OSError, ValueError) as exc:
        _emit({"error": f"{type(exc).__name__}: {exc}"})
        return 2
    result = compare(pre, post)
    _emit(result)
    if not result["equal"]:
        named = result["changed"] + result["missing"] + result["errors"]
        print(f"pins: snapshots differ: {' '.join(named)}", file=sys.stderr)
        return 1
    return 0


def _selftest() -> int:
    """Build temp fixtures, exercise API + CLI, including the red mutate case."""
    here = os.path.abspath(__file__)
    failures = []
    cases = 0

    def check(ok: bool, label: str, detail: str) -> None:
        if not ok:
            failures.append(f"{label}: {detail}")

    root = os.path.realpath(tempfile.mkdtemp(prefix="pins-selftest-"))
    try:
        f1 = os.path.join(root, "a.txt")
        f2 = os.path.join(root, "b.txt")
        with open(f1, "w", encoding="utf-8") as fh:
            fh.write("alpha")
        with open(f2, "w", encoding="utf-8") as fh:
            fh.write("beta")
        ghost = os.path.join(root, "never-existed.bin")

        def run_cli(*argv):
            return subprocess.run(
                [sys.executable, "-I", here, *argv],
                capture_output=True, text=True, check=False,
            )

        # C1 — API green: identical instants compare equal.
        cases += 1
        res = compare(snapshot([f1, f2]), snapshot([f1, f2]))
        check(res["equal"] is True and not res["changed"] and not res["missing"],
              "api-green", f"expected equal, got {res}")

        # C2 — API red: mutate between snapshots -> not equal, path in changed.
        cases += 1
        s_pre = snapshot([f1])
        with open(f1, "w", encoding="utf-8") as fh:
            fh.write("alpha-mutated")
        res = compare(s_pre, snapshot([f1]))
        check(res["equal"] is False and f1 in res["changed"],
              "api-red", f"expected changed=[{f1}], got {res}")

        # C3 — API missing: delete between snapshots -> missing, not equal.
        cases += 1
        s_pre = snapshot([f2])
        os.unlink(f2)
        res = compare(s_pre, snapshot([f2]))
        check(res["equal"] is False and f2 in res["missing"],
              "api-missing", f"expected missing=[{f2}], got {res}")

        # C4 — API error entry: pin a nonexistent path; even identical error
        # snapshots must not prove equal.
        cases += 1
        s_err_a = snapshot([ghost])
        s_err_b = snapshot([ghost])
        res = compare(s_err_a, s_err_b)
        check(res["equal"] is False and ghost in res["errors"],
              "api-error", f"expected errors=[{ghost}], got {res}")

        # C5 — CLI green: snapshot --out x2, compare -> exit 0.
        cases += 1
        g1 = os.path.join(root, "g1.json")
        g2 = os.path.join(root, "g2.json")
        r = run_cli("snapshot", "--out", g1, f1)
        check(r.returncode == 0 and isinstance(json.loads(r.stdout), dict),
              "cli-green-snapshot", f"rc={r.returncode} err={r.stderr!r}")
        r = run_cli("snapshot", "--out", g2, f1)
        check(r.returncode == 0, "cli-green-snapshot2",
              f"rc={r.returncode} err={r.stderr!r}")
        r = run_cli("compare", g1, g2)
        ok = r.returncode == 0 and json.loads(r.stdout).get("equal") is True
        check(ok, "cli-green-compare",
              f"rc={r.returncode} out={r.stdout!r}")

        # C6 — CLI red (required): snapshot, mutate the temp file, snapshot,
        # compare -> exit 1 and the changed list names the mutated path.
        cases += 1
        r1 = os.path.join(root, "r1.json")
        r2 = os.path.join(root, "r2.json")
        run_cli("snapshot", "--out", r1, f1)
        with open(f1, "w", encoding="utf-8") as fh:
            fh.write("alpha-mutated-again")
        run_cli("snapshot", "--out", r2, f1)
        r = run_cli("compare", r1, r2)
        doc = json.loads(r.stdout) if r.stdout.strip() else {}
        check(r.returncode == 1 and f1 in doc.get("changed", []),
              "cli-red", f"rc={r.returncode} changed={doc.get('changed')}")
        if r.returncode == 1:
            print(f"red case observed: compare exit 1 names {f1}")

        # C7 — CLI exit 2: unreadable compare input, invalid JSON shape,
        # snapshot --out into a nonexistent directory.
        cases += 1
        r = run_cli("compare", os.path.join(root, "absent.json"), r2)
        check(r.returncode == 2, "cli-unreadable", f"rc={r.returncode}")
        bad = os.path.join(root, "bad.json")
        with open(bad, "w", encoding="utf-8") as fh:
            fh.write("[1, 2, 3]")
        r = run_cli("compare", bad, r2)
        check(r.returncode == 2, "cli-invalid", f"rc={r.returncode}")
        r = run_cli("snapshot", "--out",
                    os.path.join(root, "no-such-dir", "s.json"), f1)
        check(r.returncode == 2, "cli-bad-outdir", f"rc={r.returncode}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    if failures:
        print("SELFTEST: FAILED " + "; ".join(failures))
        return 1
    print(f"SELFTEST: CLEAN cases={cases}")
    return 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        return _selftest()
    ap = argparse.ArgumentParser(
        prog="pins.py",
        description="Pre/post filesystem pins: sha256+size+mtime_ns snapshots "
                    "compared across a retained run (R16-PROVENANCE fix).",
        epilog="A pin pair proves only 'same bytes at two instants'; it never "
               "proves a path was unchanged throughout the interval between "
               "the two snapshots.")
    sub = ap.add_subparsers(dest="command", required=True)
    sp = sub.add_parser("snapshot", help="pin PATH... and write JSON to --out")
    sp.add_argument("--out", required=True, metavar="FILE",
                    help="snapshot JSON output path")
    sp.add_argument("paths", nargs="+", metavar="PATH")
    cp = sub.add_parser("compare", help="compare two snapshot JSON files")
    cp.add_argument("pre", metavar="PRE")
    cp.add_argument("post", metavar="POST")
    args = ap.parse_args(argv)
    if args.command == "snapshot":
        return _cmd_snapshot(args)
    return _cmd_compare(args)


if __name__ == "__main__":
    sys.exit(main())
