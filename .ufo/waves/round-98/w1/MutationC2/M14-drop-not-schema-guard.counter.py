#!/usr/bin/env python3
"""stop-boundary-repair-battery-v8.py - round-98 counter (R98-C2, calibration).

v8 = v7 with one change (round-97 closure routed defect 1, M97-j): the counts allow-list is
the verdict's own fourteen-key set (`v3.score`, tools/round-93/stop-boundary-repair-battery-v3.py
lines 288-300), so an honest public run verifies, and the round-97 nine-key stub is refused
`counts-missing-key:<k>` on the five keys it drops. The selftest fixture carries all fourteen
keys and gains a `verify-catches-nine-key-stub` case. Everything below describes v7.

The VERDICT code stays the round-93 counter `tools/round-93/stop-boundary-repair-battery-v3.py`,
imported by path and pinned by sha256 in `.ufo/waves/round-97/claims.json`. v7 changes only the
RECEIPT WRITER and its bindings, closing the round-96 named limits 2, 3, 5, 6 and the byte
binding routed from M96-a:

1. Byte binding (M96-a): `--rev` names the measured revision and the receipt's pins are bound
   to the bytes at that revision through `git cat-file blob <rev>:<path>` (`pins_at_rev`), not
   only to the live files. A tree measured dirty under a clean revision name refuses with
   `byte-pin-not-bound:<field>` before scoring; the round-96 counter admitted exactly this lie.
2. `met_target` is typed (M96-f / ReviewerInstruments H-1): absent, null or string met values
   refuse `met-not-typed` instead of verifying clean.
3. The counts object is allow-listed: any key outside COUNT_KEYS (v8: the verdict's fourteen)
   refuses `counts-extra-key:<k>`; `repair_cmd` is bound (`repair-cmd-not-bound`).
4. The imported instrument pins are bound: `imported_r92_battery_sha256` and
   `imported_v2_sha256` must equal the bytes of the two round-92 files the verdict imports
   (`imported-pin-not-bound:<field>`); `public_met` / `public_label` are recorded and bound.
5. Durability (round-97 planned (b), the souji model): `write_receipt` fsyncs the file bytes
   BEFORE the atomic replace and fsyncs the receipt's directory AFTER it, so a crash publishes
   either the previous receipt or the complete new one - never a half-written file.

Usage is identical to v6 (mandatory `--json-out`). `--selftest` exercises every new binding,
the durability ordering and the planted-symlink cases. The claim's evidence is the public CLI
run with `--json-out`, not the selftest.
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
TOOL = "tools/round-98/stop-boundary-repair-battery-v8.py"
V3_TOOL = "tools/round-93/stop-boundary-repair-battery-v3.py"
V3 = os.path.join(HERE, "..", "round-93", "stop-boundary-repair-battery-v3.py")
IMPORTED_R92_BATTERY = "tools/round-92/stop-boundary-repair-battery.py"
IMPORTED_V2 = "tools/round-92/stop-boundary-battery-v2.py"

LABEL_RE = re.compile(
    r"^repaired (\d+) of (\d+); wrong (\d+); unsafe (\d+); intact (\d+) of (\d+); "
    r"far-refused (\d+) of (\d+); fresh-roundtrip (\d+) of (\d+)$")

# v8: the verdict's own fourteen-key counts set (v3.score; round-97 closure routed defect 1).
COUNT_KEYS = ("repaired", "scored", "wrong", "unsafe", "intact",
              "far", "far_refused", "fresh_roundtrip", "fresh_scored",
              "fresh_far", "fresh_far_refused", "fresh_repaired", "refused", "silent")
NINE_LABEL_KEYS = ("repaired", "scored", "wrong", "unsafe", "intact",
                   "far", "far_refused", "fresh_roundtrip", "fresh_scored")


def _load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, os.path.abspath(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v3 = _load(V3, "r97_v3_verdict")


def _sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _default(obj):
    """JSON encodable version of bytes; any other unknown type is an error, never a str()."""
    if isinstance(obj, (bytes, bytearray)):
        return {"bytes": len(obj), "sha256": hashlib.sha256(bytes(obj)).hexdigest()}
    raise TypeError(f"Cannot serialize object of {type(obj)}")


def blob_sha256(root: str, rev: str, rel_path: str):
    """sha256 of `<rev>:<rel_path>` via `git cat-file blob`, or None when it cannot be read."""
    p = subprocess.run(["git", "-C", root, "cat-file", "blob", f"{rev}:{rel_path}"],
                       capture_output=True, timeout=30)
    if p.returncode != 0:
        return None
    return hashlib.sha256(p.stdout).hexdigest()


def write_receipt(path: str, receipt: dict) -> None:
    """Complete JSON or absent, immune to a planted `<path>.tmp` symlink, and durable:
    the file bytes are fsynced BEFORE the atomic replace and the directory is fsynced
    AFTER it, so a crash publishes either the previous receipt or the complete new one."""
    d = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(dir=d, prefix=os.path.basename(path) + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True, default=_default)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
        dfd = os.open(d, os.O_RDONLY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
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
    """Schema check: the fourteen verdict keys must be present ints; no key outside the
    allow-list is accepted (a counts object with an extra key is a refusal, not a pass)."""
    reasons = []
    if not isinstance(counts, dict):
        return reasons
    for k in COUNT_KEYS:
        v = counts.get(k)
        if v is None:
            reasons.append("counts-missing-key:%s" % k)
        elif isinstance(v, bool) or not isinstance(v, int):
            reasons.append("counts-type:%s" % k)
    for k in sorted(counts.keys()):
        if k not in COUNT_KEYS:
            reasons.append("counts-extra-key:%s" % k)
    return reasons


def verify_receipt(path: str, expect: str, rev_full, intact_total: int,
                   pins: dict, pins_at_rev: dict | None = None,
                   repair_cmd: str | None = None) -> dict:
    """Re-read the receipt the public command just wrote and bind it to the world.

    When `pins_at_rev` is given, each pin field must equal the digest of the bytes at
    the receipt's revision (`git cat-file blob`) - the byte binding closes M96-a: a
    receipt naming revision R while carrying pins of bytes that differ from R refuses
    `byte-pin-not-bound:<field>`, and a dirty tree measured under a clean revision name
    refuses the same way (its live pins differ from the revision blobs)."""
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
    met = rec.get("met_target")
    if not isinstance(met, bool):
        reasons.append("met-not-typed")
    if not isinstance(counts, dict) or not isinstance(label, str):
        if not schema:
            reasons.append("receipt-missing-counts-or-label")
    elif isinstance(met, bool):
        m = LABEL_RE.match(label)
        if m is None:
            reasons.append("label-shape-unparsable")
        elif m.group(0) != recompute_label(counts, intact_total):
            reasons.append("label-not-recomputed")
        if met is True and expect is not None and label != expect:
            reasons.append("label-not-frozen")
        if met is False and expect is not None and label == expect:
            reasons.append("met-not-recomputed")
    if rev_full is None:
        reasons.append("revision-unresolvable")
    elif rec.get("revision") != rev_full:
        reasons.append("revision-not-bound")
    head = rec.get("head")
    if not isinstance(head, str) or not re.fullmatch(r"[0-9a-f]{40}", head or "") \
            or head != rec.get("revision"):
        reasons.append("head-not-bound")
    pin_fields = (("counter_sha256", "counter"), ("verdict_sha256", "verdict"),
                  ("repair_sha256", "repair"))
    for field, key in pin_fields:
        got = rec.get(field)
        want = (pins_at_rev if pins_at_rev is not None else (pins or {})).get(key)
        if not isinstance(got, str) or not re.fullmatch(r"[0-9a-f]{64}", got or ""):
            reasons.append("receipt-missing-pin:%s" % field)
        elif want is not None and got != want:
            if pins_at_rev is not None:
                reasons.append("byte-pin-not-bound:%s" % key)
            else:
                reasons.append("%s-pin-not-bound" % key)
        elif pins_at_rev is not None and pins is not None \
                and pins_at_rev.get(key) not in (None, (pins or {}).get(key)):
            # the world itself is dirty at the named revision: the live bytes differ
            # from the revision blobs, so no receipt measured under this name is bound
            # (the M96-a class - v6 admitted exactly this lie)
            reasons.append("byte-pin-not-bound:%s" % key)
    if repair_cmd is not None and rec.get("repair_cmd") != repair_cmd:
        reasons.append("repair-cmd-not-bound")
    for field in ("imported_r92_battery_sha256", "imported_v2_sha256"):
        got = rec.get(field)
        want = (pins or {}).get(field)
        if not isinstance(got, str) or not re.fullmatch(r"[0-9a-f]{64}", got or ""):
            reasons.append("receipt-missing-pin:%s" % field)
        elif want is not None and got != want:
            reasons.append("imported-pin-not-bound:%s" % field)
    if "public_met" not in rec or rec.get("public_met") != met:
        reasons.append("public-met-not-bound")
    if "public_label" not in rec or rec.get("public_label") != label:
        reasons.append("public-label-not-bound")
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
              "far": 1, "far_refused": 1, "fresh_roundtrip": 1, "fresh_scored": 1,
              "fresh_far": 1, "fresh_far_refused": 1, "fresh_repaired": 1,
              "refused": 0, "silent": 0}
    label = recompute_label(counts, 1)
    case("label-recomputes", label == "repaired 2 of 2; wrong 0; unsafe 0; "
         "intact 1 of 1; far-refused 1 of 1; fresh-roundtrip 1 of 1")

    # Planted-symlink cases: the victims must survive and the receipt lands as JSON.
    run = os.path.join(work, "symlink-case")
    shutil.rmtree(run, ignore_errors=True)
    os.makedirs(run, exist_ok=True)
    victim = os.path.join(run, "victim.txt")
    planted = b"KAIDOKU-R97-PLANTED-VICTIM\n"
    with open(victim, "wb") as fh:
        fh.write(planted)
    target = os.path.join(run, "receipt.json")
    os.symlink(victim, target + ".tmp")
    pins = {"counter": "c" * 64, "verdict": "d" * 64, "repair": "e" * 64,
            "imported_r92_battery_sha256": "f" * 64, "imported_v2_sha256": "a" * 64,
            "repair_cmd": "tools/round-92/upx-stop-boundary-search-repair.py"}
    rec = {"label": label, "met_target": True, "exit": 0, "counts": counts,
           "revision": "b" * 40, "head": "b" * 40,
           "counter_sha256": pins["counter"], "verdict_sha256": pins["verdict"],
           "repair_sha256": pins["repair"],
           "imported_r92_battery_sha256": pins["imported_r92_battery_sha256"],
           "imported_v2_sha256": pins["imported_v2_sha256"],
           "repair_cmd": pins["repair_cmd"],
           "public_met": True, "public_label": label,
           "fresh_cells": [{"output": blob, "rc": 0}]}
    write_receipt(target, rec)
    with open(victim, "rb") as fh:
        victim_after = fh.read()
    with open(target, encoding="utf-8") as fh:
        back = json.load(fh)
    case("planted-tmp-symlink-ignored",
         victim_after == planted and not os.path.islink(target)
         and back["counts"]["repaired"] == 2)

    # Durability: fsync(file) BEFORE replace, fsync(dir) AFTER replace.
    events = []
    orig_fsync, orig_replace = os.fsync, os.replace

    def rec_fsync(fd):
        events.append("fsync")
        return orig_fsync(fd)

    def rec_replace(src, dst):
        events.append("replace")
        return orig_replace(src, dst)

    os.fsync, os.replace = rec_fsync, rec_replace
    try:
        write_receipt(os.path.join(run, "receipt-dur.json"), rec)
    finally:
        os.fsync, os.replace = orig_fsync, orig_replace
    case("durability-order",
         len(events) >= 3 and events[0] == "fsync" and "replace" in events
         and events[-1] == "fsync")

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
        base = dict(rec)
        base.update(over)
        p = os.path.join(run, "st-%s.json" % re.sub(r"[^a-z0-9-]+", "-", name_of[0]))
        write_receipt(p, base)
        return p

    name_of = ["not-recomputed"]
    bad = dict(rec)
    bad["met_target"] = False
    bad["exit"] = 1
    bad["public_met"] = False
    bad["label"] = ("repaired 9 of 2; wrong 0; unsafe 0; intact 1 of 1; "
                    "far-refused 1 of 1; fresh-roundtrip 1 of 1")
    bad["public_label"] = bad["label"]
    p = os.path.join(run, "receipt-badlabel.json")
    write_receipt(p, bad)
    v = verify_receipt(p, label, "b" * 40, 1, pins)
    case("verify-catches-not-recomputed",
         not v["ok"] and v["reasons"] == ["label-not-recomputed"])

    # met denied while the label equals the frozen expect.
    name_of = ["met-lying"]
    p_metly = full(met_target=False, exit=1, public_met=False)
    rv_mly = verify_receipt(p_metly, label, "b" * 40, 1, pins)
    case("verify-catches-met-lying",
         not rv_mly["ok"] and rv_mly["reasons"] == ["met-not-recomputed"])

    name_of = ["not-frozen"]
    other_counts = {**counts, "far_refused": 0}
    other = recompute_label(other_counts, 1)
    p2 = os.path.join(run, "receipt-rewritten.json")
    write_receipt(p2, {**rec, "label": other, "counts": other_counts,
                       "public_label": other})
    rv_v2 = verify_receipt(p2, label, "b" * 40, 1, pins)
    case("verify-catches-not-frozen",
         not rv_v2["ok"] and rv_v2["reasons"] == ["label-not-frozen"])

    name_of = ["wrong-revision"]
    p3 = full(revision="c" * 40, head="c" * 40)
    rv_v3 = verify_receipt(p3, label, "b" * 40, 1, pins)
    case("verify-catches-wrong-revision",
         not rv_v3["ok"] and rv_v3["reasons"] == ["revision-not-bound"])

    name_of = ["met-null"]
    p4 = full(met_target=None, public_met=None)
    rv_v4 = verify_receipt(p4, label, "b" * 40, 1, pins)
    case("verify-catches-met-null",
         not rv_v4["ok"] and rv_v4["reasons"] == ["met-not-typed"])

    name_of = ["met-str"]
    p4b = full(met_target="true", public_met="true")
    rv_v4b = verify_receipt(p4b, label, "b" * 40, 1, pins)
    case("verify-catches-met-str",
         not rv_v4b["ok"] and rv_v4b["reasons"] == ["met-not-typed"])

    name_of = ["counts-extra"]
    p5 = full(counts=dict(counts, forged=1))
    rv_v5 = verify_receipt(p5, label, "b" * 40, 1, pins)
    case("verify-catches-counts-extra",
         not rv_v5["ok"] and rv_v5["reasons"] == ["counts-extra-key:forged"])

    name_of = ["unlabelled"]
    p5b = full(counts={k: v for k, v in counts.items() if k != "fresh_scored"})
    rv_v5b = verify_receipt(p5b, label, "b" * 40, 1, pins)
    case("verify-catches-unlabelled-counts",
         not rv_v5b["ok"] and rv_v5b["reasons"] == ["counts-missing-key:fresh_scored"])

    name_of = ["nine-key-stub"]
    p5c = full(counts={k: counts[k] for k in NINE_LABEL_KEYS})
    rv_v5c = verify_receipt(p5c, label, "b" * 40, 1, pins)
    case("verify-catches-nine-key-stub",
         not rv_v5c["ok"] and rv_v5c["reasons"] == [
             "counts-missing-key:%s" % k for k in
             ("fresh_far", "fresh_far_refused", "fresh_repaired", "refused", "silent")])

    name_of = ["head-mismatch"]
    p6 = full(head="a" * 40)
    rv_v6 = verify_receipt(p6, label, "b" * 40, 1, pins)
    case("verify-catches-head-mismatch",
         not rv_v6["ok"] and rv_v6["reasons"] == ["head-not-bound"])

    name_of = ["counter-pin"]
    p7 = full(counter_sha256="0" * 64)
    rv_v7 = verify_receipt(p7, label, "b" * 40, 1, pins)
    case("verify-catches-counter-pin",
         not rv_v7["ok"] and rv_v7["reasons"] == ["counter-pin-not-bound"])

    # Byte binding: pins_at_rev differs from the receipt's pin -> byte refusal.
    name_of = ["byte-pin"]
    p7b = full(counter_sha256="0" * 64)
    rv_v7b = verify_receipt(p7b, label, "b" * 40, 1, pins, pins_at_rev=pins)
    case("verify-catches-byte-pin",
         not rv_v7b["ok"] and rv_v7b["reasons"] == ["byte-pin-not-bound:counter"])

    # A receipt whose pins equal the revision blobs but NOT the live files is the
    # M96-a lie and refuses with the byte reason.
    name_of = ["byte-lie"]
    blob_pins = {"counter": "9" * 64, "verdict": pins["verdict"], "repair": pins["repair"]}
    p7c = full(counter_sha256=blob_pins["counter"])
    rv_v7c = verify_receipt(p7c, label, "b" * 40, 1, pins, pins_at_rev=blob_pins)
    case("verify-catches-byte-lie",
         not rv_v7c["ok"] and rv_v7c["reasons"] == ["byte-pin-not-bound:counter"])

    name_of = ["repair-cmd"]
    p8 = full(repair_cmd="tools/round-87/upx-magic-repair.py")
    rv_v8 = verify_receipt(p8, label, "b" * 40, 1, pins, None, pins["repair_cmd"])
    case("verify-catches-repair-cmd",
         not rv_v8["ok"] and rv_v8["reasons"] == ["repair-cmd-not-bound"])

    name_of = ["imported-pin"]
    p8b = full(imported_r92_battery_sha256="0" * 64)
    rv_v8b = verify_receipt(p8b, label, "b" * 40, 1, pins)
    case("verify-catches-imported-pin",
         not rv_v8b["ok"] and rv_v8b["reasons"] ==
         ["imported-pin-not-bound:imported_r92_battery_sha256"])

    name_of = ["public-met"]
    p8c = full(public_met=False)
    rv_v8c = verify_receipt(p8c, label, "b" * 40, 1, pins)
    case("verify-catches-public-met",
         not rv_v8c["ok"] and rv_v8c["reasons"] == ["public-met-not-bound"])

    name_of = ["public-label"]
    p8d = full(public_label="repaired 0 of 0")
    rv_v8d = verify_receipt(p8d, label, "b" * 40, 1, pins)
    case("verify-catches-public-label",
         not rv_v8d["ok"] and rv_v8d["reasons"] == ["public-label-not-bound"])

    # The honest receipt verifies clean (positive control), including pins_at_rev.
    name_of = ["honest"]
    p9 = full()
    rv_v9 = verify_receipt(p9, label, "b" * 40, 1, pins)
    rv_v9b = verify_receipt(p9, label, "b" * 40, 1, pins, pins_at_rev=pins)
    case("verify-honest-accepted",
         rv_v9["ok"] and rv_v9["reasons"] == [] and rv_v9b["ok"])

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
            "kaidoku-r98", "selftest-v8"))
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
    rev_full = resolve_rev(root, args.rev)
    # Byte binding (round-97): bind the pins to the bytes at the named revision.
    pins_at_rev = None
    if rev_full is not None:
        pins_at_rev = {}
        for rel in (TOOL, V3_TOOL, args.repair_cmd):
            b = blob_sha256(root, rev_full, rel)
            if b is None:
                pins_at_rev = None
                break
            pins_at_rev[("counter" if rel == TOOL
                         else "verdict" if rel == V3_TOOL else "repair")] = b
    code, receipt = v3.score(args)
    receipt["tool"] = TOOL
    receipt["verdict_counter"] = V3_TOOL
    receipt["verdict_sha256"] = _sha256_file(os.path.join(root, V3_TOOL))
    receipt["counter_sha256"] = _sha256_file(os.path.join(root, TOOL))
    receipt["repair_cmd"] = args.repair_cmd
    receipt["repair_sha256"] = _sha256_file(os.path.join(root, args.repair_cmd))
    receipt["imported_r92_battery_sha256"] = _sha256_file(
        os.path.join(root, IMPORTED_R92_BATTERY))
    receipt["imported_v2_sha256"] = _sha256_file(os.path.join(root, IMPORTED_V2))
    receipt["head"] = resolve_rev(root, "HEAD")
    receipt["public_label"] = receipt.get("label")
    receipt["public_met"] = receipt.get("met_target")
    receipt["exit"] = code
    pins = {"counter": receipt["counter_sha256"],
            "verdict": receipt["verdict_sha256"],
            "repair": receipt["repair_sha256"],
            "imported_r92_battery_sha256": receipt["imported_r92_battery_sha256"],
            "imported_v2_sha256": receipt["imported_v2_sha256"]}
    write_receipt(args.json_out, receipt)
    selfverify = verify_receipt(args.json_out, args.expect, rev_full,
                                args.intact_total, pins, pins_at_rev,
                                args.repair_cmd)
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
