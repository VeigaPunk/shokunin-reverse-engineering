#!/usr/bin/env python3
"""stop-boundary-repair-battery-v6.py - round-96 counter (R96-C1, calibration).

The VERDICT code is still the round-93 counter `tools/round-93/stop-boundary-repair-battery-v3.py`,
imported by path and pinned by sha256 in `.ufo/waves/round-96/claims.json`. v6 changes only the
RECEIPT WRITER and its self-verification, closing the round-95 named limits 2, 3 (part) and 5:

1. Self-verification is mandatory on every exit: `--json-out` is required for the public
   path. A run without it refuses before scoring with exit 2 and a typed
   `receipt-required` line, so a green verdict can never exist without a verified receipt
   (round-95 M95-g: a v5 run without `--json-out` skipped self-verification and exited 0).
2. The receipt binds the fields round-95 left unbound (M95-g):
   - `head` (the full HEAD resolution of `--root` at run time) is recorded and must equal
     the receipt's `revision`, so a green receipt can only exist when `--rev` names the
     tree HEAD actually measured (`head-not-bound` otherwise);
   - `repair_sha256` / `repair_cmd` are recorded and bound against the bytes at
     `--repair-cmd` (`repair-pin-not-bound`);
   - `counter_sha256` and `verdict_sha256` are now checked by `verify_receipt`, not merely
     recorded (`counter-pin-not-bound` / `verdict-pin-not-bound`);
   - `met_target` is bound downward: a receipt whose label equals the frozen `--expect` but
     that claims `met_target false` is refused (`met-not-recomputed`); the met-true
     direction stays `label-not-frozen` (round-95 reasons are unchanged);
   - a counts object missing or mistyping any label key is a typed refusal
     (`counts-missing-key:<k>` / `counts-type:<k>`), never a `KeyError` (round-95 named
     limit 5).

Usage is identical to v3/v4/v5 plus the mandatory `--json-out`. `--selftest` exercises the
writer helpers, the planted-symlink case and every new binding, including a wrong-revision
case (the round-95 M6 mutant kill under kill rule v2). The claim's evidence is the public
CLI run with `--json-out`, not the selftest.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "tools/round-96/stop-boundary-repair-battery-v6.py"
V3_TOOL = "tools/round-93/stop-boundary-repair-battery-v3.py"
V3 = os.path.join(HERE, "..", "round-93", "stop-boundary-repair-battery-v3.py")

LABEL_RE = re.compile(
    r"^repaired (\d+) of (\d+); wrong (\d+); unsafe (\d+); intact (\d+) of (\d+); "
    r"far-refused (\d+) of (\d+); fresh-roundtrip (\d+) of (\d+)$")

COUNT_KEYS = ("repaired", "scored", "wrong", "unsafe", "intact",
              "far", "far_refused", "fresh_roundtrip", "fresh_scored")


def _load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, os.path.abspath(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v3 = _load(V3, "r96_v3_verdict")


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
    """Full 40-hex resolution of `rev` (hex prefixes and symbolic names like HEAD),
    or None when it does not resolve."""
    if not rev or re.search(r"\s", rev):
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


def count_problems(counts) -> list:
    """Schema check for the label keys: missing or non-int keys are typed reasons."""
    reasons = []
    if not isinstance(counts, dict):
        return reasons
    for k in COUNT_KEYS:
        v = counts.get(k)
        if v is None:
            reasons.append("counts-missing-key:%s" % k)
        elif isinstance(v, bool) or not isinstance(v, int):
            reasons.append("counts-type:%s" % k)
    return reasons


def verify_receipt(path: str, expect: str, rev_full, intact_total: int,
                   pins: dict) -> dict:
    """Re-read the receipt the public command just wrote and bind it to the world:
    valid JSON, label recomputes from schema-valid counts, label equals `--expect`
    when met is claimed and does NOT equal it when met is denied, revision is the
    full resolution of `--rev`, `head` equals the revision, and the counter, verdict
    and repair pins match the bytes this run used."""
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
    schema = count_problems(counts)
    reasons.extend(schema)
    if not isinstance(counts, dict) or not isinstance(label, str):
        if not schema:
            reasons.append("receipt-missing-counts-or-label")
    elif not schema:
        m = LABEL_RE.match(label)
        if m is None:
            reasons.append("label-shape-unparsable")
        elif m.group(0) != recompute_label(counts, intact_total):
            reasons.append("label-not-recomputed")
        if rec.get("met_target") is True and expect is not None and label != expect:
            reasons.append("label-not-frozen")
        if rec.get("met_target") is False and expect is not None and label == expect:
            reasons.append("met-not-recomputed")
    if rev_full is None:
        reasons.append("revision-unresolvable")
    elif rec.get("revision") != rev_full:
        reasons.append("revision-not-bound")
    head = rec.get("head")
    if not isinstance(head, str) or not re.fullmatch(r"[0-9a-f]{40}", head or "") \
            or head != rec.get("revision"):
        reasons.append("head-not-bound")
    for field, key in (("counter_sha256", "counter"), ("verdict_sha256", "verdict"),
                       ("repair_sha256", "repair")):
        got = rec.get(field)
        want = (pins or {}).get(key)
        if not isinstance(got, str) or not re.fullmatch(r"[0-9a-f]{64}", got or ""):
            reasons.append("receipt-missing-pin:%s" % field)
        elif want is not None and got != want:
            reasons.append("%s-pin-not-bound" % key)
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
    planted = b"KAIDOKU-R96-PLANTED-VICTIM\n"
    with open(victim, "wb") as fh:
        fh.write(planted)
    target = os.path.join(run, "receipt.json")
    os.symlink(victim, target + ".tmp")
    pins = {"counter": "c" * 64, "verdict": "d" * 64, "repair": "e" * 64}
    rec = {"label": label, "met_target": True, "exit": 0, "counts": counts,
           "revision": "b" * 40, "head": "b" * 40,
           "counter_sha256": pins["counter"], "verdict_sha256": pins["verdict"],
           "repair_sha256": pins["repair"],
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

    def full(**over):
        base = {"label": label, "met_target": True, "exit": 0, "counts": counts,
                "revision": "b" * 40, "head": "b" * 40,
                "counter_sha256": pins["counter"], "verdict_sha256": pins["verdict"],
                "repair_sha256": pins["repair"]}
        base.update(over)
        p = os.path.join(run, "st-%s.json" % re.sub(r"[^a-z0-9-]+", "-", name_of[0]))
        write_receipt(p, base)
        return p

    # Self-verification: a rewritten label that disagrees with counts is caught.
    name_of = ["not-recomputed"]
    bad = dict(rec)
    bad["met_target"] = False
    bad["exit"] = 1
    bad["label"] = ("repaired 9 of 2; wrong 0; unsafe 0; intact 1 of 1; "
                    "far-refused 1 of 1; fresh-roundtrip 1 of 1")
    p = os.path.join(run, "receipt-badlabel.json")
    write_receipt(p, bad)
    v = verify_receipt(p, label, "b" * 40, 1, pins)
    case("verify-catches-not-recomputed",
         not v["ok"] and v["reasons"] == ["label-not-recomputed"])

    # Self-verification: a met-True receipt whose label is not the frozen expect.
    name_of = ["not-frozen"]
    other_counts = {**counts, "far_refused": 0}
    other = recompute_label(other_counts, 1)
    p2 = os.path.join(run, "receipt-rewritten.json")
    write_receipt(p2, {**rec, "label": other, "counts": other_counts})
    rv_v2 = verify_receipt(p2, label, "b" * 40, 1, pins)
    case("verify-catches-not-frozen",
         not rv_v2["ok"] and rv_v2["reasons"] == ["label-not-frozen"])

    # Wrong revision (the round-95 M6 mutant kill under kill rule rv_v2): the head
    # tracks the revision so the single violated binding stays the revision.
    name_of = ["wrong-revision"]
    p3 = full(revision="c" * 40, head="c" * 40)
    rv_v3 = verify_receipt(p3, label, "b" * 40, 1, pins)
    case("verify-catches-wrong-revision",
         not rv_v3["ok"] and rv_v3["reasons"] == ["revision-not-bound"])

    # met denied while the label equals the frozen expect (public_met binding).
    name_of = ["met-lying"]
    p4 = full(met_target=False, exit=1)
    rv_v4 = verify_receipt(p4, label, "b" * 40, 1, pins)
    case("verify-catches-met-lying",
         not rv_v4["ok"] and rv_v4["reasons"] == ["met-not-recomputed"])

    # A counts object missing a label key is a typed refusal, never a KeyError.
    name_of = ["unlabelled"]
    p5 = full(counts={k: v for k, v in counts.items() if k != "fresh_scored"})
    rv_v5 = verify_receipt(p5, label, "b" * 40, 1, pins)
    case("verify-catches-unlabelled-counts",
         not rv_v5["ok"] and rv_v5["reasons"] == ["counts-missing-key:fresh_scored"])

    # head must be a 40-hex field equal to the revision.
    name_of = ["head-mismatch"]
    p6 = full(head="a" * 40)
    rv_v6 = verify_receipt(p6, label, "b" * 40, 1, pins)
    case("verify-catches-head-mismatch",
         not rv_v6["ok"] and rv_v6["reasons"] == ["head-not-bound"])

    # A counter pin that does not match the bytes this run used.
    name_of = ["counter-pin"]
    p7 = full(counter_sha256="0" * 64)
    rv_v7 = verify_receipt(p7, label, "b" * 40, 1, pins)
    case("verify-catches-counter-pin",
         not rv_v7["ok"] and rv_v7["reasons"] == ["counter-pin-not-bound"])

    # The honest receipt verifies clean (positive control for the bindings).
    name_of = ["honest"]
    p8 = full()
    rv_v8 = verify_receipt(p8, label, "b" * 40, 1, pins)
    case("verify-honest-accepted", rv_v8["ok"] and rv_v8["reasons"] == [])

    # Self-verification is mandatory: no --json-out refuses before scoring.
    def fake(args, _label=label, _counts=counts):
        return 0, {"class": "selftest", "label": _label, "met_target": True,
                   "exit": 0, "counts": _counts, "revision": args.rev,
                   "fresh_cells": []}

    orig_score = v3.score
    v3.score = fake
    try:
        buf_out, buf_err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
            code = main(["--root", os.getcwd(), "--work",
                         os.path.join(work, "usage-w"), "--rev", "b" * 40,
                         "--expect", label])
    finally:
        v3.score = orig_score
    case("usage-refuses-no-json-out", code == 2 and "receipt-required" in buf_err.getvalue())

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
    ap.add_argument("--json-out",
                    help="mandatory: a green exit exists only through a verified receipt")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return _selftest(args.work or os.path.join(
            os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"),
            "kaidoku-r96", "selftest-v6"))
    if not args.work or args.expect is None:
        print("usage: --work <dir> --expect <label> --json-out <path>", file=sys.stderr)
        return 2
    # Self-verification is mandatory on every exit (round-95 M95-g closure): refuse
    # before scoring when no receipt can be written or verified.
    if not args.json_out:
        print("receipt-required: a green exit exists only through a verified receipt",
              file=sys.stderr)
        return 2
    root = os.path.abspath(args.root)
    code, receipt = v3.score(args)
    receipt["tool"] = TOOL
    receipt["verdict_counter"] = V3_TOOL
    receipt["verdict_sha256"] = _sha256_file(os.path.join(root, V3_TOOL))
    receipt["counter_sha256"] = _sha256_file(os.path.join(root, TOOL))
    receipt["repair_cmd"] = args.repair_cmd
    receipt["repair_sha256"] = _sha256_file(os.path.join(root, args.repair_cmd))
    receipt["head"] = resolve_rev(root, "HEAD")
    receipt["exit"] = code
    pins = {"counter": receipt["counter_sha256"],
            "verdict": receipt["verdict_sha256"],
            "repair": receipt["repair_sha256"]}
    write_receipt(args.json_out, receipt)
    selfverify = verify_receipt(args.json_out, args.expect,
                                resolve_rev(root, args.rev), args.intact_total, pins)
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
