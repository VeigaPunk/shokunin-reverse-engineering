#!/usr/bin/env python3
"""stop-boundary-repair-battery-v5.py - round-95 counter (R95-C1, calibration).

The VERDICT code is the round-93 counter `tools/round-93/stop-boundary-repair-battery-v3.py`,
imported by path and pinned by sha256 in `.ufo/waves/round-95/claims.json`. v5 changes
exactly two things and both live in the RECEIPT WRITER (the verdict code is untouched):

1. Hardened temp file (round-94 SentinelWrite F1 remediation): the receipt is written
   through `tempfile.mkstemp` - a unique temporary name created in the receipt's own
   directory - so a pre-planted `<json-out>.tmp` symlink is neither read nor followed.
   The bytes encoding (bytes -> {"bytes": n, "sha256": hex}) and the unknown-type
   `TypeError` are carried over unchanged from v4.
2. Receipt self-verification (round-94 M94-e routed fix): after writing, the counter
   re-reads its own receipt and verifies, before it may exit 0 on a met-True verdict:
   the receipt parses as a whole, the label recomputes byte-exact from the receipt's own
   counts, the label equals the frozen `--expect` string whenever met_target is true,
   and `revision` is the full 40-hex resolution of `--rev`. Any failed binding turns a
   green verdict into exit 1 with a typed `selfverify` line (fail closed). A red verdict
   still writes its receipt and exits 1 as before.

Usage is identical to v3/v4: `--root --repair-cmd --work --rev --expect --json-out`.
`--selftest` exercises the writer helpers including the planted-symlink case; the
claim's evidence is the public CLI run with `--json-out`, not the selftest.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "tools/round-95/stop-boundary-repair-battery-v5.py"
V3_TOOL = "tools/round-93/stop-boundary-repair-battery-v3.py"
V3 = os.path.join(HERE, "..", "round-93", "stop-boundary-repair-battery-v3.py")

LABEL_RE = re.compile(
    r"^repaired (\d+) of (\d+); wrong (\d+); unsafe (\d+); intact (\d+) of (\d+); "
    r"far-refused (\d+) of (\d+); fresh-roundtrip (\d+) of (\d+)$")


def _load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, os.path.abspath(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v3 = _load(V3, "r95_v3_verdict")


def _sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _default(obj):
    """JSON encodable version of bytes; any other unknown type is an error, never a str()."""
    if isinstance(obj, (bytes, bytearray)):
        return {"bytes": len(obj), "sha256": hashlib.sha256(bytes(obj)).hexdigest()}
    raise TypeError(f"Cannot serialize object of {type(obj)}")


def write_receipt(path: str, receipt: dict) -> None:
    """Complete JSON or absent, and immune to a planted `<path>.tmp` symlink: the
    temporary name comes from mkstemp (unique, created fresh in the same directory),
    never from the predictable `<path>.tmp` a local attacker can pre-plant."""
    d = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(dir=d, prefix=os.path.basename(path) + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True, default=_default)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def recompute_label(counts: dict, intact_total: int) -> str:
    return ("repaired %d of %d; wrong %d; unsafe %d; intact %d of %d; "
            "far-refused %d of %d; fresh-roundtrip %d of %d") % (
        counts["repaired"], counts["scored"], counts["wrong"], counts["unsafe"],
        counts["intact"], intact_total, counts["far_refused"], counts["far"],
        counts["fresh_roundtrip"], counts["fresh_scored"])


def resolve_rev(root: str, rev: str):
    """Full 40-hex resolution of `--rev`, or None when it does not resolve."""
    if not re.fullmatch(r"[0-9a-f]{6,64}", rev or ""):
        return None
    try:
        out = subprocess.run(["git", "-C", root, "rev-parse", "--verify", rev],
                             capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    full = out.stdout.strip()
    return full if re.fullmatch(r"[0-9a-f]{40}", full) else None


def verify_receipt(path: str, expect: str, rev_full, intact_total: int) -> dict:
    """Re-read the receipt the public command just wrote and bind it to the world:
    valid JSON, label recomputes from counts, label equals `--expect` when met, and
    revision is the full resolution of `--rev`."""
    reasons = []
    try:
        with open(path, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, ValueError) as exc:
        return {"ok": False, "reasons": ["receipt-not-valid-json:%s" % type(exc).__name__]}
    if not isinstance(rec, dict):
        return {"ok": False, "reasons": ["receipt-not-an-object"]}
    counts = rec.get("counts")
    label = rec.get("label")
    if not isinstance(counts, dict) or not isinstance(label, str):
        reasons.append("receipt-missing-counts-or-label")
    else:
        m = LABEL_RE.match(label)
        if m is None:
            reasons.append("label-shape-unparsable")
        elif m.group(0) != recompute_label(counts, intact_total):
            reasons.append("label-not-recomputed")
        if rec.get("met_target") is True and expect is not None and label != expect:
            reasons.append("label-not-frozen")
    if rev_full is None:
        reasons.append("revision-unresolvable")
    elif rec.get("revision") != rev_full:
        reasons.append("revision-not-bound")
    return {"ok": not reasons, "reasons": reasons}


def _selftest(work: str) -> int:
    os.makedirs(work, exist_ok=True)
    results = []

    def case(name: str, ok: bool) -> None:
        results.append((name, ok))
        print(f"selftest {name}: {'ok' if ok else 'FAIL'}")

    blob = b"\x7fELF-fixture"
    case("bytes-encoded", _default(blob) == {"bytes": len(blob),
                                             "sha256": hashlib.sha256(blob).hexdigest()})

    counts = {"repaired": 2, "scored": 2, "wrong": 0, "unsafe": 0, "intact": 1,
              "far": 1, "far_refused": 1, "fresh_roundtrip": 1, "fresh_scored": 1}
    label = recompute_label(counts, 1)
    case("label-recomputes", label == "repaired 2 of 2; wrong 0; unsafe 0; "
         "intact 1 of 1; far-refused 1 of 1; fresh-roundtrip 1 of 1")

    # Planted-symlink case: the victim must survive the write untouched and the
    # receipt must land at the target as complete JSON.
    run = os.path.join(work, "symlink-case")
    shutil.rmtree(run, ignore_errors=True)
    os.makedirs(run, exist_ok=True)
    victim = os.path.join(run, "victim.txt")
    planted = b"KAIDOKU-R95-PLANTED-VICTIM\n"
    with open(victim, "wb") as fh:
        fh.write(planted)
    target = os.path.join(run, "receipt.json")
    os.symlink(victim, target + ".tmp")
    rec = {"label": label, "met_target": True, "exit": 0, "counts": counts,
           "revision": "b" * 40,
           "fresh_cells": [{"output": blob, "rc": 0}]}
    write_receipt(target, rec)
    with open(victim, "rb") as fh:
        victim_after = fh.read()
    with open(target, encoding="utf-8") as fh:
        back = json.load(fh)
    case("planted-tmp-symlink-ignored",
         victim_after == planted and not os.path.islink(target)
         and back["counts"]["repaired"] == 2)

    # Unknown type still raises; no partial target, no leftover temp.
    q = os.path.join(run, "receipt-unknown.json")
    try:
        write_receipt(q, {"x": object()})
        raised = False
    except TypeError:
        raised = True
    leftovers = [n for n in os.listdir(run) if n.startswith("receipt-unknown.json")]
    case("unknown-type-raises-clean", raised and not os.path.exists(q) and not leftovers)

    # Self-verification: a rewritten label that disagrees with counts is caught.
    bad = dict(rec)
    bad["met_target"] = False
    bad["exit"] = 1
    bad["label"] = ("repaired 9 of 2; wrong 0; unsafe 0; intact 1 of 1; "
                    "far-refused 1 of 1; fresh-roundtrip 1 of 1")
    p = os.path.join(run, "receipt-badlabel.json")
    write_receipt(p, bad)
    v = verify_receipt(p, label, "b" * 40, 1)
    case("verify-catches-not-recomputed",
         not v["ok"] and v["reasons"] == ["label-not-recomputed"])

    # Self-verification: a met-True receipt whose label is not the frozen expect.
    # The rewrite is internally consistent (it recomputes from its own counts),
    # so the only violated binding is the frozen label.
    p2 = os.path.join(run, "receipt-rewritten.json")
    other_counts = {**counts, "far_refused": 0}
    other = recompute_label(other_counts, 1)
    write_receipt(p2, {**rec, "label": other, "counts": other_counts})
    v2 = verify_receipt(p2, label, "b" * 40, 1)
    case("verify-catches-not-frozen",
         not v2["ok"] and v2["reasons"] == ["label-not-frozen"])

    print(f"SELFTEST cases={len(results)} failures={sum(1 for _, ok in results if not ok)}")
    return 0 if all(ok for _, ok in results) else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--repair-cmd", default=v3.DEFAULT_REPAIR)
    ap.add_argument("--work")
    ap.add_argument("--rev", default="worktree")
    ap.add_argument("--expect", help="frozen label: %r" % v3.FROZEN_LABEL)
    ap.add_argument("--intact-total", type=int, default=6,
                    help="intact-arm denominator of the frozen label (5 public + 1 fresh)")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return _selftest(args.work or os.path.join(
            os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"),
            "kaidoku-r95", "selftest-v5"))
    if not args.work or args.expect is None:
        print("usage: --work <dir> --expect <label> [--json-out <path>]", file=sys.stderr)
        return 2
    code, receipt = v3.score(args)
    root = os.path.abspath(args.root)
    receipt["tool"] = TOOL
    receipt["verdict_counter"] = V3_TOOL
    receipt["verdict_sha256"] = _sha256_file(os.path.join(root, V3_TOOL))
    receipt["counter_sha256"] = _sha256_file(os.path.join(root, TOOL))
    receipt["exit"] = code
    selfverify = {"ok": None, "reasons": []}
    if args.json_out:
        write_receipt(args.json_out, receipt)
        selfverify = verify_receipt(args.json_out, args.expect,
                                    resolve_rev(root, args.rev), args.intact_total)
        # Fail closed: a green verdict may only exit 0 through a verified receipt.
        if code == 0 and not selfverify["ok"]:
            code = 1
    print("selfverify ok=%s reasons=%d" % (selfverify["ok"], len(selfverify["reasons"])))
    for r in selfverify["reasons"]:
        print("selfverify reason: %s" % r, file=sys.stderr)
    print(receipt.get("label", receipt.get("unevaluable")), "met",
          receipt.get("met_target"), "exit", code)
    return code


if __name__ == "__main__":
    sys.exit(main())
