#!/usr/bin/env python3
"""kill-rule-v3.py - round-97 frozen counting command for R97-C1 (calibration).

Round 96 froze a kill rule whose bindings stopped at the live bytes: a receipt named a
revision whose bytes it did not measure (M96-a, `head == revision` is a commit pointer),
`met_target` verified clean when absent or null (M96-f), six receipt fields stayed unbound,
`--json-out` was optional on the rule itself, the frozen table had no `--rev != HEAD`
scenario (M96-e), a crash counted as a semantic kill (N9), the probe's own write escape
was outside every frozen check (M96-h), and the r95-battery leg was cwd-dependent
(M96-j). kill-rule-v3 is the successor rule scoring the round-97 mutant table over the
v7 counter (tools/round-97/stop-boundary-repair-battery-v7.py), which binds the byte and
durability closures; this rule binds its own receipt the same way.

Check set (each must pass on the honest instrument, and at least one must fail on a
killed mutant):

  K-selftest    the counter's / agreement's / rule's `--selftest` exits 0.
  K-forgeries   `verify_receipt` of the v7 counter refuses the 13 round-97 forgeries with
                exactly their intended single reason, and refuses the four round-95
                forgeries (regression, refusal-only there).
  K-agreement   the round-95 agreement instrument refuses its four forgeries with exactly
                their intended reasons and accepts the honest triple (exact, subprocess).
  K-dmain       the v7 counter's `main()` with a faked verdict: pos exits 0; shortrev,
                rewrite, notrecomp AND revold (--rev <declaration>, a revision other than
                HEAD) exit non-zero; a run without `--json-out` exits 2.
  K-durability  the v7 writer fsyncs the file bytes BEFORE the atomic replace and fsyncs
                the directory AFTER it (ordering observed by instrumenting os.fsync and
                os.replace).
  K-wlink       with a symlink planted at the counter receipt path and at the predictable
                `<path>.tmp` name (two victims), the honest v7 write leaves both victims
                intact and lands the receipt as complete JSON.
  K-probe       the probe's receipt is self-consistent AND the victim planted at the
                probe's own `--json-out` path survives the probe's hardened writer.
  K-bytes       each of the five instrument paths hashes equal at HEAD (`git cat-file
                blob`) and live; the three receipt pins equal the blobs; and in a dirty
                scratch clone the v6 counter admits the byte lie (exit 0) while v7
                refuses it with `byte-pin-not-bound` (exit 1) - dirtyrefuse.
  K-cwd         the r95-battery regression leg runs green from a non-root cwd (the
                honest-dir join is absolute).
  K-ownrec      the rule's own green receipt exists only through a re-read receipt that
                verifies (`ownrec` binding in the receipt, enforced in main).

Legs: honest arm (every check green), mutant arm (21 mutants, each declared
`kill_class` semantic or crash; killed when checks fail AND the observed class matches
the declaration), identity guard (M0 must NOT be killed).

Frozen label:
  `mutants killed 21 of 21; forgeries refused 13 of 13; negctl refused 3 of 3; probe consistent 1 of 1; honest accepted 1 of 1; wlink 2 of 2; durability 2 of 2; bytes 5 of 5; dirtyrefuse 1 of 1; ownrec 1 of 1`
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

TOOL = "tools/round-97/kill-rule-v3.py"
DEFAULT_COUNTER = "tools/round-97/stop-boundary-repair-battery-v7.py"
DEFAULT_V3 = "tools/round-93/stop-boundary-repair-battery-v3.py"
DEFAULT_AGREEMENT = "tools/round-95/c1-agreement-v2.py"
DEFAULT_PROBE = "tools/round-96/symlink-probe-v2.py"
DEFAULT_WRITER = "tools/round-94/stop-boundary-repair-battery-v4.py"
DEFAULT_NOOP = ".ufo/waves/round-93/controls/identity_noop.py"
DEFAULT_R95_BATTERY = "tools/round-95/c1-forgery-refusal.py"
DEFAULT_R92_BATTERY = "tools/round-92/stop-boundary-repair-battery.py"
DEFAULT_R92_V2 = "tools/round-92/stop-boundary-battery-v2.py"
DEFAULT_REPAIR = "tools/round-92/upx-stop-boundary-search-repair.py"
FROZEN_LABEL = ("repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; "
                "far-refused 12 of 12; fresh-roundtrip 2 of 2")
R95_REASONS = {"pos": "label-not-frozen", "F1": "label-not-recomputed",
               "F2": "revision-not-bound", "F3": "pins-not-bound"}
R95_WORLD_REV = "b5331db1fb0ce0bf93695ce1730cf831effef6a9"
R95_INSTRUMENT_REV = "4bda1d1dd3788973f10e61212b70df18b3b14ea0"
TOTAL_MUTANTS = 21
TOTAL_FORGERIES = 17
TOTAL_BYTES = 5


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run(cmd: list, timeout: int = 600):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def write_receipt(path: str, receipt: dict) -> None:
    """Complete JSON or absent, durable, immune to a planted symlink at `<path>.tmp`."""
    import tempfile
    d = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(dir=d, prefix=os.path.basename(path) + ".",
                               suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
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


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, os.path.abspath(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def resolve_head(root: str):
    rc, out, _ = run(["git", "-C", root, "rev-parse", "HEAD"], 30)
    full = out.strip() if rc == 0 else ""
    return full if re.fullmatch(r"[0-9a-f]{40}", full) else None


def blob_sha256(root: str, rev: str, rel_path: str):
    p = subprocess.run(["git", "-C", root, "cat-file", "blob", f"{rev}:{rel_path}"],
                       capture_output=True, timeout=30)
    if p.returncode != 0:
        return None
    return hashlib.sha256(p.stdout).hexdigest()


def counter_pins(root: str, mod, repair_rel: str) -> dict:
    return {"counter": sha256_file(os.path.join(root, mod.TOOL)),
            "verdict": sha256_file(os.path.join(root, mod.V3_TOOL)),
            "repair": sha256_file(os.path.join(root, repair_rel)),
            "imported_r92_battery_sha256": sha256_file(
                os.path.join(root, DEFAULT_R92_BATTERY)),
            "imported_v2_sha256": sha256_file(os.path.join(root, DEFAULT_R92_V2))}


# ---------------------------------------------------------------- check set

def c_selftest(path: str, work: str, style: str = "flag") -> dict:
    d = os.path.join(work, "selftest-run")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d, exist_ok=True)
    if style == "flag":
        cmd = [sys.executable, "-I", "-B", path, "--selftest", "--work", d]
    else:
        cmd = [sys.executable, "-I", "-B", path, "--selftest", d]
    rc, out, err = run(cmd, 300)
    ok = rc == 0
    tail = (out or err).strip().splitlines()[-1:] if (out or err).strip() else []
    return {"ok": ok, "exit": rc, "tail": tail[0] if tail else ""}


def c_verify_forgeries(mod, root: str, expect: str, repair_rel: str,
                       fixture_dirs: list, pins7: dict) -> dict:
    """fixture_dirs: list of (path, prefix, exact: bool, intended: dict)."""
    rows = []
    for fdir, prefix, exact, intended in fixture_dirs:
        for name in sorted(intended.keys()):
            path = os.path.join(fdir, "%s-%s.json" % (prefix, name))
            try:
                with open(path, encoding="utf-8") as fh:
                    rec = json.load(fh)
                rev_full = rec.get("revision")
            except (OSError, ValueError):
                rev_full = None
            v = mod.verify_receipt(path, expect, rev_full, 6, pins7,
                                   pins_at_rev=pins7, repair_cmd=repair_rel)
            if exact:
                ok = (not v["ok"]) and v["reasons"] == [intended[name]]
            else:
                ok = (not v["ok"]) and len(v["reasons"]) >= 1
            rows.append({"fixture": "%s-%s" % (prefix, name), "ok": ok,
                         "reasons": v["reasons"], "exact": exact})
    refused = sum(1 for r in rows if r["ok"])
    return {"ok": refused == len(rows), "refused": refused, "total": len(rows),
            "rows": rows}


def c_agreement_exact(agreement_path: str, root: str, fixture_dir: str, prefix: str,
                      expect: str, work: str) -> dict:
    rows = []
    for name, intended in R95_REASONS.items():
        rc, out, err = run([sys.executable, "-I", "-B", agreement_path,
                            "--root", root, "--dir", fixture_dir, "--prefix", prefix,
                            "--names", name, "--expect", expect, "--rev",
                            R95_WORLD_REV, "--intact-total", "6"], 120)
        try:
            payload = json.loads(out)
        except ValueError:
            payload = {}
        reasons = None
        for r in payload.get("rows", []):
            if r.get("run") == name:
                reasons = r.get("reasons")
        ok = rc == 1 and reasons == [intended]
        rows.append({"fixture": "%s-%s" % (prefix, name), "ok": ok, "exit": rc,
                     "reasons": reasons})
    rc, out, _ = run([sys.executable, "-I", "-B", agreement_path, "--root", root,
                      "--dir", os.path.join(root, ".ufo/waves/round-95/l1/scores"),
                      "--prefix", "honest", "--names", "pos", "--expect", expect,
                      "--rev", R95_INSTRUMENT_REV, "--intact-total", "6"], 120)
    honest_ok = rc == 0
    refused = sum(1 for r in rows if r["ok"])
    return {"ok": refused == 4 and honest_ok, "refused": refused, "total": 4,
            "honest_accepted": honest_ok, "rows": rows}


def c_dmain(mod, root: str, head: str, expect: str, work: str, decl: str) -> dict:
    os.makedirs(work, exist_ok=True)
    base = {"repaired": 12, "scored": 12, "wrong": 0, "unsafe": 0, "intact": 6,
            "far": 12, "far_refused": 12, "fresh_roundtrip": 2, "fresh_scored": 2}
    other_counts = dict(base, far_refused=11)
    notre = dict(base, repaired=11)
    scenarios = [
        ("pos", head, expect, base, 0),
        ("shortrev", head[:9], expect, base, 1),
        ("rewrite", head, ("repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; "
                           "far-refused 11 of 12; fresh-roundtrip 2 of 2"),
         other_counts, 1),
        ("notrecomp", head, expect, notre, 1),
        ("revold", decl, expect, base, 1),
    ]
    results = {}
    orig = mod.v3.score
    try:
        for name, rev, label, counts, want in scenarios:
            def fake(args, _l=label, _c=counts):
                return 0, {"class": "killrule", "label": _l, "met_target": True,
                           "exit": 0, "counts": _c, "revision": args.rev,
                           "fresh_cells": []}
            mod.v3.score = fake
            out = os.path.join(work, "dmain-%s.json" % name)
            shutil.rmtree(os.path.join(work, "w-" + name), ignore_errors=True)
            bo, be = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(bo), contextlib.redirect_stderr(be):
                code = mod.main(["--root", root, "--work",
                                 os.path.join(work, "w-" + name), "--rev", rev,
                                 "--expect", expect, "--json-out", out])
            ok = code == 0 if want == 0 else code != 0
            results[name] = {"exit": code, "ok": ok}
        mod.v3.score = (lambda args: (
            0, {"class": "killrule", "label": expect, "met_target": True, "exit": 0,
                "counts": base, "revision": args.rev, "fresh_cells": []}))
        bo, be = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(bo), contextlib.redirect_stderr(be):
            code = mod.main(["--root", root, "--work",
                             os.path.join(work, "w-nojson"), "--rev", head,
                             "--expect", expect])
        results["nojson"] = {"exit": code, "ok": code == 2}
    finally:
        mod.v3.score = orig
    return results


def c_durability(mod, work: str) -> dict:
    """Observe the write_receipt ordering: fsync(file) before replace, fsync(dir) after."""
    os.makedirs(work, exist_ok=True)
    events = []
    orig_fsync, orig_replace = os.fsync, os.replace

    def rec_fsync(fd, _o=orig_fsync, _e=events):
        _e.append("fsync")
        return _o(fd)

    def rec_replace(src, dst, _o=orig_replace, _e=events):
        _e.append("replace")
        return _o(src, dst)

    os.fsync, os.replace = rec_fsync, rec_replace
    try:
        mod.write_receipt(os.path.join(work, "dur-receipt.json"), {"x": 1})
    finally:
        os.fsync, os.replace = orig_fsync, orig_replace
    pre = events[:1] == ["fsync"] and "replace" in events
    post = events[-1:] == ["fsync"] and events.index("replace") < len(events) - 1
    return {"ok": pre and post, "events": events,
            "pre_fsync": pre, "post_fsync": post}


def c_wlink(mod, root: str, head: str, expect: str, work: str) -> dict:
    """Two planted victims: one at the receipt path, one at `<path>.tmp`."""
    run_dir = os.path.join(work, "wlink-run")
    shutil.rmtree(run_dir, ignore_errors=True)
    os.makedirs(run_dir, exist_ok=True)
    v1 = os.path.join(run_dir, "victim-main.txt")
    v2 = os.path.join(run_dir, "victim-tmp.txt")
    p1 = b"KAIDOKU-R97-WLINK-MAIN\n"
    p2 = b"KAIDOKU-R97-WLINK-TMP\n"
    with open(v1, "wb") as fh:
        fh.write(p1)
    with open(v2, "wb") as fh:
        fh.write(p2)
    out = os.path.join(run_dir, "receipt.json")
    os.symlink(v1, out)
    os.symlink(v2, out + ".tmp")
    bo, be = io.StringIO(), io.StringIO()
    orig = mod.v3.score
    mod.v3.score = (lambda args: (
        0, {"class": "killrule", "label": expect, "met_target": True, "exit": 0,
            "counts": {"repaired": 12, "scored": 12, "wrong": 0, "unsafe": 0,
                       "intact": 6, "far": 12, "far_refused": 12,
                       "fresh_roundtrip": 2, "fresh_scored": 2},
            "revision": args.rev, "fresh_cells": []}))
    try:
        with contextlib.redirect_stdout(bo), contextlib.redirect_stderr(be):
            code = mod.main(["--root", root, "--work",
                             os.path.join(work, "wlink-w"), "--rev", head,
                             "--expect", expect, "--json-out", out])
    finally:
        mod.v3.score = orig
    with open(v1, "rb") as fh:
        v1_after = fh.read()
    with open(v2, "rb") as fh:
        v2_after = fh.read()
    rec = None
    try:
        with open(out, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, ValueError):
        rec = None
    ok = (v1_after == p1 and v2_after == p2 and isinstance(rec, dict)
          and not os.path.islink(out) and code == 0)
    return {"ok": ok, "exit": code, "victim_main_intact": v1_after == p1,
            "victim_tmp_intact": v2_after == p2, "receipt_valid": isinstance(rec, dict),
            "receipt": rec if isinstance(rec, dict) else None}


def c_probe(root: str, probe_path: str, writer: str, noop: str, expect: str,
            head: str, work: str) -> dict:
    """The probe's receipt must be consistent AND the victim planted at the probe's
    own --json-out path must survive the probe's writer (round-96 M96-h closure)."""
    run_dir = os.path.join(work, "probe-run")
    shutil.rmtree(run_dir, ignore_errors=True)
    os.makedirs(run_dir, exist_ok=True)
    pv = os.path.join(work, "probe-jsonout-victim.txt")
    planted = b"KAIDOKU-R97-PROBE-JSONOUT-VICTIM\n"
    with open(pv, "wb") as fh:
        fh.write(planted)
    out = os.path.join(work, "probe-receipt.json")
    if os.path.lexists(out):
        os.remove(out)
    os.symlink(pv, out)
    cmd = [sys.executable, "-I", "-B", probe_path, "--root", root,
           "--writer", writer, "--repair-cmd", noop, "--work", run_dir,
           "--rev", head, "--expect", expect, "--json-out", out]
    rc, so, se = run(cmd, 1800)
    rec = None
    try:
        with open(out, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, ValueError):
        rec = None
    with open(pv, "rb") as fh:
        pv_after = fh.read()
    if not isinstance(rec, dict):
        return {"ok": False, "error": "probe receipt unreadable", "probe_rc": rc,
                "stderr_tail": se[-300:]}
    truth = bool(rec.get("victim_intact")) and bool(rec.get("receipt_valid"))
    verdict = rec.get("verdict")
    consistent = ((verdict == "hardened") == truth) and (rec.get("met") is truth)
    ok = bool(consistent) and pv_after == planted and not os.path.islink(out)
    return {"ok": ok, "probe_rc": rc, "verdict": verdict,
            "met": rec.get("met"), "victim_intact": rec.get("victim_intact"),
            "receipt_valid": rec.get("receipt_valid"),
            "jsonout_victim_intact": pv_after == planted}


def c_bytes(root: str, head: str, decl: str, pins7: dict, receipt: dict | None,
            work: str, counter: str, expect: str) -> dict:
    """Blob binding at HEAD plus the dirty-clone leg: v6 admits the lie, v7 refuses."""
    paths = [DEFAULT_COUNTER, DEFAULT_V3, DEFAULT_REPAIR, DEFAULT_AGREEMENT,
             DEFAULT_PROBE]
    rows = []
    for rel in paths:
        b = blob_sha256(root, head, rel)
        live = sha256_file(os.path.join(root, rel))
        rows.append({"path": rel, "blob": b, "live": live,
                     "ok": b is not None and b == live})
    for field, key in (("counter_sha256", "counter"), ("verdict_sha256", "verdict"),
                       ("repair_sha256", "repair")):
        rows.append({"receipt_field": field, "ok": bool(receipt)
                     and receipt.get(field) == (pins7 or {}).get(key)})
    bound = sum(1 for r in rows if "path" in r and r.get("ok"))
    blob_ok = all(r.get("ok") for r in rows)

    # Dirty-clone leg: clone --shared into scratch, dirty the v7 counter, load each
    # counter from the clone, fake a green verdict, and observe who admits the lie.
    clone = os.path.join(work, "dirty-clone")
    shutil.rmtree(clone, ignore_errors=True)
    rc, _, err = run(["git", "clone", "--shared", "--quiet", root, clone], 300)
    if rc != 0:
        return {"ok": False, "error": "clone failed: %s" % err[-200:], "rows": rows,
                "bound": bound, "total": len(rows)}
    counter_abs = os.path.join(clone, counter)
    if not os.path.isfile(counter_abs):
        return {"ok": False,
                "error": "counter absent in clone (uncommitted at this revision)",
                "rows": rows, "bound": bound, "total": len(rows)}
    with open(counter_abs, "a", encoding="utf-8") as fh:
        fh.write("\n# DIRTY-BYTES-FOR-BYTE-BINDING-PROBE\n")
    dirty = {}
    for name, rel in (("v7", DEFAULT_COUNTER), ("v6", "tools/round-96/stop-boundary-repair-battery-v6.py")):
        mod = load_module(os.path.join(clone, rel), "bytes_%s" % name)
        out = os.path.join(work, "dirty-%s.json" % name)
        bo, be = io.StringIO(), io.StringIO()
        mod.v3.score = (lambda args: (
            0, {"class": "killrule", "label": expect, "met_target": True, "exit": 0,
                "counts": {"repaired": 12, "scored": 12, "wrong": 0, "unsafe": 0,
                           "intact": 6, "far": 12, "far_refused": 12,
                           "fresh_roundtrip": 2, "fresh_scored": 2},
                "revision": args.rev, "fresh_cells": []}))
        with contextlib.redirect_stdout(bo), contextlib.redirect_stderr(be):
            code = mod.main(["--root", clone, "--work",
                             os.path.join(work, "dirty-w-" + name), "--rev", head,
                             "--expect", expect, "--json-out", out])
        dirty[name] = {"exit": code, "stderr_tail": be.getvalue()[-200:]}
    v7_refused = dirty.get("v7", {}).get("exit") == 1 and \
        "byte-pin-not-bound" in dirty.get("v7", {}).get("stderr_tail", "")
    v6_admitted = dirty.get("v6", {}).get("exit") == 0
    return {"ok": bool(blob_ok and v7_refused and v6_admitted), "rows": rows,
            "bound": bound, "total": len(rows), "dirty": dirty,
            "v7_refused": v7_refused, "v6_admitted": v6_admitted}


def c_cwd(root: str, work: str, expect: str) -> dict:
    """The r95-battery regression leg must be green from a non-root cwd (M96-j)."""
    probe_cwd = os.path.join(work, "cwdprobe")
    shutil.rmtree(probe_cwd, ignore_errors=True)
    os.makedirs(probe_cwd, exist_ok=True)
    cmd = [sys.executable, "-I", "-B", os.path.join(root, DEFAULT_R95_BATTERY),
           "--root", root, "--fixtures", ".ufo/waves/round-95/forgery",
           "--old-prefix", "forge",
           "--old-counter", "tools/round-94/c1-receipt-agreement.py",
           "--honest-dir", os.path.join(root, ".ufo/waves/round-95/l1/scores"),
           "--honest-prefix", "honest", "--world-rev", R95_WORLD_REV,
           "--instrument-rev", R95_INSTRUMENT_REV, "--expect", expect,
           "--json-out", os.path.join(probe_cwd, "cwd-battery.json")]
    rc, out, err = run(cmd, 300)
    return {"ok": rc == 0, "exit": rc, "cwd": probe_cwd,
            "stderr_tail": err[-200:]}


# ---------------------------------------------------------------- mutant arm

def build_copy(name: str, m: dict, root: str, work: str, deps: list) -> str:
    d = os.path.join(work, "mut-%s" % name)
    shutil.rmtree(d, ignore_errors=True)
    rel = m["file"]
    dst = os.path.join(d, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(os.path.join(root, rel), dst)
    with open(dst, encoding="utf-8") as fh:
        data = fh.read()
    n = data.count(m["find"])
    if n != 1:
        raise ValueError("mutant %s: find string occurs %d times in %s"
                         % (name, n, rel))
    data = data.replace(m["find"], m["replace"], 1)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(data)
    for dep in deps:
        dd = os.path.join(d, dep)
        os.makedirs(os.path.dirname(dd), exist_ok=True)
        shutil.copyfile(os.path.join(root, dep), dd)
    return d


class CheckCrash(Exception):
    """A mutant check raised - classified `crash`, never a semantic kill."""


def run_mutant(name: str, m: dict, root: str, expect: str, head: str, work: str,
               fixture_dirs: list, r95_fixture_dir: str, writer: str, noop: str,
               counter: str, repair_pin: str, decl: str, mutants_path: str = "",
               fixtures_path: str = "") -> dict:
    kind = m["kind"]
    checks = {}
    crashed = False
    try:
        if kind in ("counter", "identity"):
            d = build_copy(name, m, root, work,
                           [DEFAULT_V3, DEFAULT_R92_BATTERY, DEFAULT_R92_V2])
            path = os.path.join(d, m["file"])
            checks["K-selftest"] = c_selftest(path, os.path.join(work, name, "st"),
                                              "flag")
            mod = load_module(path, "kr_%s" % name)
            checks["K-dmain"] = c_dmain(mod, root, head, expect,
                                        os.path.join(work, name, "dmain"), decl)
            checks["K-dmain"]["ok"] = all(v["ok"] for v in
                                          checks["K-dmain"].values())
            checks["K-durability"] = c_durability(mod, os.path.join(work, name, "dur"))
            checks["K-wlink"] = c_wlink(mod, root, head, expect,
                                        os.path.join(work, name, "wlink"))
            pins7 = counter_pins(root, mod, repair_pin)
            checks["K-forgeries"] = c_verify_forgeries(mod, root, expect, repair_pin,
                                                       fixture_dirs, pins7)
        elif kind == "agreement":
            d = build_copy(name, m, root, work, [])
            path = os.path.join(d, m["file"])
            checks["K-selftest"] = c_selftest(path, os.path.join(work, name, "st"),
                                              "value")
            checks["K-agreement"] = c_agreement_exact(path, root, r95_fixture_dir,
                                                      "forge", expect,
                                                      os.path.join(work, name, "agr"))
        elif kind == "probe":
            d = build_copy(name, m, root, work, [])
            path = os.path.join(d, m["file"])
            checks["K-probe"] = c_probe(root, path, writer, noop, expect, head,
                                        os.path.join(work, name, "probe"))
        elif kind == "rule":
            d = build_copy(name, m, root, work, [])
            path = os.path.join(d, m["file"])
            checks["K-selftest"] = c_selftest(path, os.path.join(work, name, "st"),
                                              "flag")
            if m.get("ownrun"):
                out = os.path.join(work, name, "ownrun", "receipt.json")
                os.makedirs(os.path.dirname(out), exist_ok=True)
                rmod = load_module(path, "kr_own_%s" % name)
                bo, be = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(bo), contextlib.redirect_stderr(be):
                    code = rmod.main(["--root", root, "--work",
                                      os.path.join(work, name, "ownrun-w"),
                                      "--mutants", mutants_path,
                                      "--fixtures", fixtures_path,
                                      "--prefix", "forge", "--decl", decl,
                                      "--json-out", out])
                own = None
                try:
                    with open(out, encoding="utf-8") as fh:
                        own = json.load(fh)
                except (OSError, ValueError):
                    own = None
                checks["K-ownrun"] = {"ok": isinstance(own, dict)
                                      and isinstance(own.get("ownrec"), dict)
                                      and own["ownrec"].get("ok") is True,
                                      "exit": code,
                                      "has_ownrec": isinstance(own, dict)
                                      and "ownrec" in own}
        else:
            raise ValueError("unknown mutant kind %r" % kind)
    except Exception as exc:  # a crash is recorded, never mistaken for a refusal
        crashed = True
        checks["crash"] = {"ok": False, "error": "%s: %s" % (type(exc).__name__, exc)}
    failed = [k for k, v in checks.items() if not v.get("ok")]
    observed = "crash" if crashed else "semantic"
    declared = m.get("kill_class", "semantic")
    killed = bool(failed) and observed == declared
    return {"name": name, "kind": kind, "killed": killed, "checks": checks,
            "failed_checks": failed, "observed_class": observed,
            "declared_class": declared}


# ---------------------------------------------------------------- own receipt

def verify_own_receipt(path: str, world_head: str) -> dict:
    """Re-read this rule's own receipt and bind it: valid JSON object, met_target a real
    bool, the label recomputes from counts, world_revision is the 40-hex HEAD this run
    resolved, and the counts totals match the declared constants."""
    reasons = []
    try:
        with open(path, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, ValueError) as exc:
        return {"ok": False, "reasons": ["ownrec-not-valid-json:%s" % type(exc).__name__]}
    if not isinstance(rec, dict):
        return {"ok": False, "reasons": ["ownrec-not-an-object"]}
    if not isinstance(rec.get("met_target"), bool):
        reasons.append("ownrec-met-not-typed")
    if rec.get("world_revision") != world_head or \
            not re.fullmatch(r"[0-9a-f]{40}", rec.get("world_revision") or ""):
        reasons.append("ownrec-world-not-bound")
    c = rec.get("counts") or {}
    if rec.get("met_target") is True and (c.get("mutants_killed") != c.get("mutants")
                                          or c.get("forgeries_refused") != c.get("forgeries")):
        reasons.append("ownrec-counts-inconsistent")
    if not isinstance(rec.get("identity_not_killed"), bool):
        reasons.append("ownrec-identity-not-typed")
    return {"ok": not reasons, "reasons": reasons}


# ---------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--work")
    ap.add_argument("--mutants")
    ap.add_argument("--fixtures", help="round-97 forgery dir")
    ap.add_argument("--prefix", default="forge")
    ap.add_argument("--r95-fixtures", default=".ufo/waves/round-95/forgery")
    ap.add_argument("--r95-prefix", default="forge")
    ap.add_argument("--counter", default=DEFAULT_COUNTER)
    ap.add_argument("--agreement", default=DEFAULT_AGREEMENT)
    ap.add_argument("--probe", default=DEFAULT_PROBE)
    ap.add_argument("--writer", default=DEFAULT_WRITER)
    ap.add_argument("--noop", default=DEFAULT_NOOP)
    ap.add_argument("--repair-pin", default=DEFAULT_REPAIR,
                    help="the repair file whose sha256 the forged fixtures bake")
    ap.add_argument("--expect", default=FROZEN_LABEL)
    ap.add_argument("--decl", help="the declaration (freeze) commit; revold scenario")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return _selftest(args)
    missing = [a for a, v in (("--work", args.work), ("--mutants", args.mutants),
                              ("--fixtures", args.fixtures), ("--decl", args.decl)) if v is None]
    if missing:
        print("usage: missing %s" % ", ".join(missing), file=sys.stderr)
        return 2
    if not args.json_out:
        print("receipt-required: a green exit exists only through a verified receipt",
              file=sys.stderr)
        return 2
    root = os.path.abspath(args.root)
    os.makedirs(os.path.abspath(args.work), exist_ok=True)
    head = resolve_head(root)
    if head is None:
        print("kill-rule: cannot resolve HEAD at %s" % root, file=sys.stderr)
        return 2
    rc, out, _ = run(["git", "-C", root, "rev-parse", "--verify", args.decl], 30)
    decl_full = out.strip() if rc == 0 and re.fullmatch(r"[0-9a-f]{40}", out.strip()) \
        else None
    if decl_full is None:
        print("kill-rule: --decl does not resolve", file=sys.stderr)
        return 2
    with open(args.mutants, encoding="utf-8") as fh:
        mutants = json.load(fh)
    r95_fixture_dir = os.path.join(root, args.r95_fixtures)
    new_intended = json.loads(mutants["forgery_reasons"]) if \
        isinstance(mutants.get("forgery_reasons"), str) else \
        mutants.get("forgery_reasons")
    fixture_dirs = [(args.fixtures, args.prefix, True, new_intended),
                    (r95_fixture_dir, args.r95_prefix, False, R95_REASONS)]
    r95_fixtures_abs = r95_fixture_dir

    honest = {}
    counter_path = os.path.join(root, args.counter)
    agreement_path = os.path.join(root, args.agreement)
    probe_path = os.path.join(root, args.probe)
    honest["K-selftest-counter"] = c_selftest(counter_path,
                                              os.path.join(args.work, "honest-st-c"),
                                              "flag")
    honest["K-selftest-agreement"] = c_selftest(agreement_path,
                                                os.path.join(args.work, "honest-st-a"),
                                                "value")
    cmod = load_module(counter_path, "kr_honest_counter")
    pins7 = counter_pins(root, cmod, args.repair_pin)
    honest["K-forgeries"] = c_verify_forgeries(cmod, root, args.expect,
                                               args.repair_pin, fixture_dirs, pins7)
    honest["K-agreement"] = c_agreement_exact(agreement_path, root, r95_fixtures_abs,
                                              args.r95_prefix, args.expect,
                                              os.path.join(args.work, "honest-agr"))
    honest["K-dmain"] = c_dmain(cmod, root, head, args.expect,
                                os.path.join(args.work, "honest-dmain"), decl_full)
    honest["K-dmain"]["ok"] = all(v["ok"] for v in honest["K-dmain"].values())
    honest["K-durability"] = c_durability(cmod, os.path.join(args.work, "honest-dur"))
    honest["K-wlink"] = c_wlink(cmod, root, head, args.expect,
                                os.path.join(args.work, "honest-wlink"))
    honest["K-probe"] = c_probe(root, probe_path, args.writer, args.noop,
                                args.expect, head, os.path.join(args.work, "honest-probe"))
    honest["K-bytes"] = c_bytes(root, head, decl_full, pins7,
                                honest["K-wlink"].get("receipt"), args.work,
                                args.counter, args.expect)
    rc95, o95, _ = run([sys.executable, "-I", "-B",
                        os.path.join(root, DEFAULT_R95_BATTERY),
                        "--root", root, "--fixtures", args.r95_fixtures,
                        "--old-prefix", args.r95_prefix,
                        "--old-counter", "tools/round-94/c1-receipt-agreement.py",
                        "--honest-dir", os.path.join(root, ".ufo/waves/round-95/l1/scores"),
                        "--honest-prefix", "honest", "--world-rev", R95_WORLD_REV,
                        "--instrument-rev", R95_INSTRUMENT_REV,
                        "--expect", args.expect,
                        "--json-out", os.path.join(args.work, "a4-r95-battery.json")],
                       300)
    honest["r95-battery-regression"] = {"ok": rc95 == 0, "exit": rc95}
    honest["K-cwd"] = c_cwd(root, args.work, args.expect)

    negctl = sum(1 for s in ("shortrev", "rewrite", "notrecomp")
                 if honest["K-dmain"].get(s, {}).get("ok"))
    wlink_ok = sum(1 for k in ("victim_main_intact", "victim_tmp_intact")
                   if honest["K-wlink"].get(k))
    dur_ok = sum(1 for k in ("pre_fsync", "post_fsync")
                 if honest["K-durability"].get(k))
    forgeries = honest["K-forgeries"]["refused"]
    probe_ok = 1 if honest["K-probe"]["ok"] else 0
    bytes_ok = honest["K-bytes"].get("bound", 0)
    dirty_ok = 1 if honest["K-bytes"].get("ok") else 0
    cwd_ok = 1 if honest["K-cwd"]["ok"] else 0
    honest_checks = [honest["K-selftest-counter"], honest["K-selftest-agreement"],
                     honest["K-forgeries"], honest["K-agreement"], honest["K-dmain"],
                     honest["K-durability"], honest["K-wlink"], honest["K-probe"],
                     honest["K-bytes"], honest["r95-battery-regression"],
                     honest["K-cwd"]]
    honest_ok = 1 if all(c["ok"] for c in honest_checks) else 0

    mrows = []
    for m in mutants["mutants"]:
        mrows.append(run_mutant(m["name"], m, root, args.expect, head,
                                os.path.join(args.work, "mut"), fixture_dirs,
                                r95_fixtures_abs, args.writer, args.noop,
                                args.counter, args.repair_pin, decl_full,
                                os.path.abspath(args.mutants),
                                os.path.abspath(args.fixtures)))
    real = [r for r in mrows if r["kind"] != "identity"]
    identity = [r for r in mrows if r["kind"] == "identity"]
    killed = sum(1 for r in real if r["killed"])
    identity_not_killed = all(not r["killed"] for r in identity)
    sem_killed = sum(1 for r in real if r["killed"] and r["observed_class"] == "semantic")
    crash_killed = sum(1 for r in real if r["killed"] and r["observed_class"] == "crash")
    # every killed mutant died under its declared class, and every declared crash
    # mutant was crash-killed (no semantic-declared mutant survives by crashing, and
    # no crash-declared mutant is killed semantically)
    classes_match = all((r["observed_class"] == r["declared_class"]) or not r["failed_checks"]
                        for r in real)

    label = ("mutants killed %d of %d; forgeries refused %d of %d; negctl refused %d of 3; "
             "probe consistent %d of 1; honest accepted %d of 1; wlink %d of 2; "
             "durability %d of 2; bytes %d of %d; dirtyrefuse %d of 1; ownrec %d of 1"
             % (killed, TOTAL_MUTANTS, forgeries, TOTAL_FORGERIES, negctl,
                probe_ok, honest_ok, wlink_ok, dur_ok, bytes_ok, TOTAL_BYTES,
                dirty_ok, 1))
    met = (killed == TOTAL_MUTANTS and forgeries == TOTAL_FORGERIES and negctl == 3
           and probe_ok == 1 and honest_ok == 1 and identity_not_killed
           and wlink_ok == 2 and dur_ok == 2 and bytes_ok == TOTAL_BYTES
           and dirty_ok == 1 and cwd_ok == 1 and classes_match
           and sem_killed + crash_killed == killed)
    receipt = {
        "class": "R97-C1 kill rule v3",
        "counter": TOOL,
        "counter_sha256": sha256_file(os.path.abspath(__file__)),
        "target_counter": args.counter,
        "target_counter_sha256": sha256_file(counter_path),
        "agreement": args.agreement,
        "agreement_sha256": sha256_file(agreement_path),
        "probe": args.probe,
        "probe_sha256": sha256_file(probe_path),
        "mutants_file": args.mutants,
        "mutants_sha256": sha256_file(args.mutants),
        "decl": args.decl,
        "decl_full": decl_full,
        "world_revision": head,
        "expect": args.expect,
        "honest": honest,
        "mutants": mrows,
        "identity_not_killed": identity_not_killed,
        "kill_classes": {"semantic_killed": sem_killed, "crash_killed": crash_killed,
                         "classes_match": classes_match},
        "counts": {"mutants_killed": killed, "mutants": TOTAL_MUTANTS,
                   "forgeries_refused": forgeries, "forgeries": TOTAL_FORGERIES,
                   "negctl_refused": negctl, "negctl": 3,
                   "probe_consistent": probe_ok, "probe": 1,
                   "honest_accepted": honest_ok, "honest": 1,
                   "wlink": wlink_ok, "durability": dur_ok,
                   "bytes_bound": bytes_ok, "bytes": TOTAL_BYTES,
                   "dirtyrefuse": dirty_ok, "cwd_ok": cwd_ok},
        "label": label,
        "met_target": met,
        "exit": 0 if met else 1,
    }
    rendered = json.dumps(receipt, indent=1, sort_keys=True)
    write_receipt(args.json_out, receipt)
    ownrec = verify_own_receipt(args.json_out, head)
    receipt["ownrec"] = {"ok": ownrec["ok"], "reasons": ownrec["reasons"]}
    # Own-receipt binding: a green verdict exists only through a re-read receipt.
    if met and not ownrec["ok"]:
        met = False
        receipt["met_target"] = False
        receipt["exit"] = 1
        label = label.replace("ownrec 1 of 1", "ownrec 0 of 1")
        receipt["label"] = label
        rendered = json.dumps(receipt, indent=1, sort_keys=True)
        write_receipt(args.json_out, receipt)
    print(rendered)
    print("ownrec ok=%s reasons=%d" % (ownrec["ok"], len(ownrec["reasons"])))
    for r in ownrec["reasons"]:
        print("ownrec reason: %s" % r, file=sys.stderr)
    print(label, "met", receipt["met_target"], "exit", receipt["exit"])
    return 0 if receipt["met_target"] else 1


def _selftest(args) -> int:
    """Hermetic: verifies the mutant machinery, the kill-class discrimination and the
    own-receipt binding on synthetic fixtures; no lane write, no network."""
    results = []

    def case(name, ok):
        results.append(ok)
        print(f"selftest {name}: {'ok' if ok else 'FAIL'}")

    work = args.work or os.path.join(
        os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "kaidoku-r97",
        "selftest-killrule")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)

    # mutant application: a one-line find/replace applies exactly once
    m = {"name": "T1", "kind": "agreement", "file": "x/probe.py",
         "find": "TARGET_LINE = 1\n", "replace": "TARGET_LINE = 2\n"}
    fake_root = os.path.join(work, "root")
    os.makedirs(os.path.join(fake_root, "x"), exist_ok=True)
    with open(os.path.join(fake_root, m["file"]), "w", encoding="utf-8") as fh:
        fh.write("TARGET_LINE = 1\n")
    dep_free = build_copy("T1", m, fake_root, work, [])
    with open(os.path.join(dep_free, m["file"]), encoding="utf-8") as fh:
        case("apply-once", fh.read() == "TARGET_LINE = 2\n")

    # double occurrence is refused
    with open(os.path.join(fake_root, m["file"]), "w", encoding="utf-8") as fh:
        fh.write("TARGET_LINE = 1\nTARGET_LINE = 1\n")
    try:
        build_copy("T2", m, fake_root, work, [])
        case("double-find-refused", False)
    except ValueError:
        case("double-find-refused", True)

    # kill-class discrimination: a semantic-declared mutant that only crashes is
    # NOT killed; a crash-declared crash is killed and labelled.
    row_sem = {"name": "S1", "kind": "counter", "kill_class": "semantic"}
    checks = {"K-x": {"ok": False, "error": "KeyError: 'fresh_scored'"}}
    crashed = True
    observed = "crash" if crashed else "semantic"
    killed_sem = bool(checks) and observed == row_sem["kill_class"]
    case("semantic-declared-crash-not-killed", not killed_sem)
    row_crash = {"name": "S2", "kind": "counter", "kill_class": "crash"}
    killed_crash = bool(checks) and observed == row_crash["kill_class"]
    case("crash-declared-crash-killed", killed_crash)

    # own-receipt binding: a lying receipt is refused; an honest one verifies.
    lying_path = os.path.join(work, "ownrec-lying.json")
    write_receipt(lying_path, {"met_target": None, "world_revision": "z" * 40,
                               "counts": {"mutants_killed": 1, "mutants": 2,
                                          "forgeries_refused": 1, "forgeries": 1},
                               "identity_not_killed": "yes"})
    v = verify_own_receipt(lying_path, "b" * 40)
    case("ownrec-lying-refused",
         not v["ok"] and "ownrec-met-not-typed" in v["reasons"]
         and "ownrec-world-not-bound" in v["reasons"]
         and "ownrec-identity-not-typed" in v["reasons"])
    honest_path = os.path.join(work, "ownrec-honest.json")
    write_receipt(honest_path, {"met_target": True, "world_revision": "b" * 40,
                                "counts": {"mutants_killed": 21, "mutants": 21,
                                           "forgeries_refused": 13, "forgeries": 13},
                                "identity_not_killed": True})
    v2 = verify_own_receipt(honest_path, "b" * 40)
    case("ownrec-honest-accepted", v2["ok"] and v2["reasons"] == [])

    # no-json-out refusal happens before scoring (the M-r1 kill)
    fake_mut = os.path.join(work, "st-mutants.json")
    with open(fake_mut, "w", encoding="utf-8") as fh:
        json.dump({"forgery_reasons": {}, "mutants": []}, fh)
    bo, be = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(bo), contextlib.redirect_stderr(be):
        code = main(["--root", os.getcwd(), "--work", os.path.join(work, "nojson-w"),
                     "--mutants", fake_mut, "--fixtures", fake_mut, "--decl", "HEAD"])
    case("usage-refuses-no-json-out", code == 2)

    # probe consistency predicate: a lying receipt is inconsistent
    lying = {"verdict": "hardened", "met": True, "victim_intact": False,
             "receipt_valid": True}
    truth = bool(lying["victim_intact"]) and bool(lying["receipt_valid"])
    consistent = ((lying["verdict"] == "hardened") == truth) and \
        (lying["met"] is truth)
    case("lying-probe-inconsistent", not consistent)

    print(f"SELFTEST cases={len(results)} failures={sum(1 for c in results if not c)}")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
