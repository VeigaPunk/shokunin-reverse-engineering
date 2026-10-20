#!/usr/bin/env python3
"""route-model.py -- independent reimplementation of the Ghidra
GoApiSnapshot route logic, then a sweep diff vs tools/predict.py.

Reimplemented from scratch (no import of r16 selection.py or r17
predict.py) against:

  Base-src.zip:ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java

    :118-145  getApiSnapshotJsonFile
        baseVer = goVer.withPatch(0)
        jsonFile = getApiSnapshotFile(baseVer, "", "")
        if jsonFile == null -> return null                     (route "none")
        patchDiffFile = getPatchVerDiffFile(goVer)
        if patchDiffFile == null -> serve base jsonFile
        else -> derived provider patching base -> goVer

    :148-166  getPatchVerDiffFile
        patchVer = goVer
        while patchVer.getPatch() > 0 &&
              (patchDiffFile = getApiSnapshotFile(patchVer,
                                                  "patchverdiffs/",
                                                  ".diff")) == null:
            patchVer = patchVer.prevPatch()
        if patchVer.getPatch() != goVer.getPatch():
            WARN "Falling back from <goVer> to <patchVer> ..." (route "fallback")
        else:
            INFO "Using Go API snapshot for <goVer>"           (route "info")

    :168-177  getApiSnapshotFile
        Application.getModuleDataFile("typeinfo/golang/%sgo%s.json%s"
                                      .formatted(subdir, goVer, suffix))
        -> ResourceFile; FileNotFoundException -> null.
        Application.getDataFileInModule (Generic-src.zip
        ghidra/framework/Application.java:354-374) throws
        FileNotFoundException when the path is absent OR a directory,
        so presence = "regular file exists".
        ResourceFile.getFile(true) returns the OS File for an on-disk
        module dir (Utility-src.zip generic/jar/ResourceFile.java:247-251).

  Base-src.zip:ghidra/app/util/bin/format/golang/GoVer.java
        :127-131 prevPatch: patch>0 ? patch-1 : 0
        :154-159 toString: "%d.%d.%d" (patch != -1)

Model route vocabulary (chosen to mirror predict.py expected fields):
  "none"     - base go<M.m.0>.json missing: getApiSnapshotJsonFile
               returns null before the diff search; no GoApiSnapshot
               log line at all.
  "info"     - selected patchVer.patch == requested patch (includes
               patch==0 short-circuit and exact-diff hits): INFO line.
  "fallback" - selected patchVer.patch != requested patch (lower diff,
               or no diff at all => patchVer == base patch 0):
               WARN "Falling back from <req> to <sel>".
  fallback_to - patchVer.toString() when route == "fallback", else null.

CLI:
  route-model.py --golang-root DIR [--predict PY] [--out FILE]
                 [--jobs N] [--selftest]

Sweep: M=1, m in 13..28, p in 0..20 (336 versions).
For each version the model route is computed two ways and required to
agree: (a) literal per-patch countdown (Java loop), (b) directory
listing -> max same-minor diff patch <= request. predict.py is invoked
once per version; expected.snapshot_route/fallback_to are compared.

Exit: 0 emitted & zero disagreements, 1 disagreements found,
2 could-not-evaluate.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PATCH_SUBDIR = "patchverdiffs"
# Canonical GoVer.toString() diff names; Java probes literal names so any
# non-canonical file can never match the countdown either.
DIFF_NAME_RE = re.compile(r"go(\d+)\.(\d+)\.(\d+)\.json\.diff")


def _regular_file(path):
    """Application.getDataFileInModule FileNotFoundException cases:
    absent path OR directory -> getApiSnapshotFile returns null.
    (Generic-src.zip ghidra/framework/Application.java:362-374)"""
    return os.path.isfile(path)


def _base_exists(root, major, minor):
    """getApiSnapshotFile(baseVer=withPatch(0), "", ""):
    typeinfo/golang/go<M.m.0>.json as a regular file."""
    return _regular_file(
        os.path.join(root, "go%d.%d.%d.json" % (major, minor, 0)))


def _diff_exists(root, major, minor, patch):
    """getApiSnapshotFile(patchVer, "patchverdiffs/", ".diff"):
    typeinfo/golang/patchverdiffs/go<M.m.p>.json.diff regular file."""
    return _regular_file(
        os.path.join(
            root, PATCH_SUBDIR,
            "go%d.%d.%d.json.diff" % (major, minor, patch)))


def _selected_patch_countdown(root, major, minor, req_patch):
    """Literal Java while-loop of getPatchVerDiffFile (GoApiSnapshot.java
    :153-156). Returns the patchVer.patch the loop lands on."""
    patch_ver = req_patch
    while patch_ver > 0 and not _diff_exists(root, major, minor, patch_ver):
        patch_ver -= 1  # GoVer.prevPatch(), GoVer.java:127-131
    return patch_ver


def _selected_patch_listing(root, major, minor, req_patch):
    """Independent equivalent: highest canonical same-M.m diff patch
    <= req_patch, else 0. Countdown over a contiguous probe space equals
    max present candidate; checked per call as an internal cross-check."""
    if req_patch <= 0:
        return 0
    best = 0
    diff_dir = os.path.join(root, PATCH_SUBDIR)
    try:
        names = os.listdir(diff_dir)
    except OSError:
        names = []
    for name in names:
        m = DIFF_NAME_RE.fullmatch(name)
        if not m:
            continue
        if int(m.group(1)) != major or int(m.group(2)) != minor:
            continue
        cand = int(m.group(3))
        # Java probes the literal canonical filename; "go1.3.04.json.diff"
        # can never be hit (it also fails r16's stricter regex).
        if name != "go%d.%d.%d.json.diff" % (major, minor, cand):
            continue
        if 0 < cand <= req_patch and cand > best \
                and _regular_file(os.path.join(diff_dir, name)):
            best = cand
    return best


def model_route(root, major, minor, req_patch):
    """Return (route, fallback_to, crosscheck_ok) for request M.m.p."""
    if not _base_exists(root, major, minor):
        # GoApiSnapshot.java:124-126: null before the diff search;
        # GoApiSnapshot emits no log line (observed: 1.27.x runs).
        return "none", None, True
    sel_c = _selected_patch_countdown(root, major, minor, req_patch)
    sel_l = _selected_patch_listing(root, major, minor, req_patch)
    cross_ok = sel_c == sel_l
    if sel_c == req_patch:
        return "info", None, cross_ok
    return "fallback", "%d.%d.%d" % (major, minor, sel_c), cross_ok


def _run_predict(predict_py, golang_root, version):
    argv = [
        sys.executable, "-I", "-B", predict_py,
        "--go-version", "go%d.%d.%d" % version,
        "--golang-root", golang_root,
    ]
    try:
        cp = subprocess.run(
            argv, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"exit": -1, "error": "%s: %s" % (type(e).__name__, e),
                "argv": argv}
    out = {"exit": cp.returncode, "argv": argv}
    if cp.returncode == 0:
        try:
            doc = json.loads(cp.stdout)
        except ValueError as e:
            out["error"] = "predict stdout not JSON: %s" % e
        else:
            exp = doc.get("expected") or {}
            sel = doc.get("selection") or {}
            out.update(
                route=exp.get("snapshot_route"),
                fallback_to=exp.get("fallback_to"),
                selection_status=sel.get("status"),
                normalized=doc.get("normalized"))
    else:
        out["stderr"] = cp.stderr.strip()[:400]
    return out


def sweep(golang_root, predict_py, jobs):
    versions = [
        (1, m, p) for m in range(13, 29) for p in range(0, 21)]
    rows = []
    disagreements = []
    crosscheck_failures = []

    def one(ver):
        route, fb, cross_ok = model_route(golang_root, *ver)
        pred = _run_predict(predict_py, golang_root, ver)
        vstr = "%d.%d.%d" % ver
        agree = (
            pred.get("exit") == 0
            and pred.get("route") == route
            and pred.get("fallback_to") == fb)
        return vstr, route, fb, cross_ok, pred, agree

    with ThreadPoolExecutor(max_workers=jobs) as ex:
        for vstr, route, fb, cross_ok, pred, agree in \
                ex.map(one, versions):
            row = {
                "version": vstr,
                "model": {"route": route, "fallback_to": fb},
                "predict": {
                    "exit": pred.get("exit"),
                    "route": pred.get("route"),
                    "fallback_to": pred.get("fallback_to"),
                    "selection_status": pred.get("selection_status"),
                },
                "agree": agree,
            }
            if pred.get("stderr"):
                row["predict"]["stderr"] = pred["stderr"]
            if pred.get("error"):
                row["predict"]["error"] = pred["error"]
            rows.append(row)
            if not cross_ok:
                crosscheck_failures.append(vstr)
            if not agree:
                disagreements.append(row)

    counts = {}
    for row in rows:
        counts[row["model"]["route"]] = \
            counts.get(row["model"]["route"], 0) + 1
    return rows, disagreements, crosscheck_failures, counts


def _selftest():
    """Fixture roots proving the four route classes and the
    directory-decoy and non-canonical-name exclusions."""
    root = tempfile.mkdtemp(prefix="route-model-selftest-")
    cases = []

    def mk(rel, data=b"{}"):
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)

    # minor 1: base + contiguous diffs 1..3
    mk("go1.1.0.json")
    for p in (1, 2, 3):
        mk("patchverdiffs/go1.1.%d.json.diff" % p)
    # minor 2: base + sparse diff at 5 only
    mk("go1.2.0.json")
    mk("patchverdiffs/go1.2.5.json.diff")
    # minor 3: base + decoys: diff name as directory; non-canonical name
    mk("go1.3.0.json")
    os.makedirs(os.path.join(
        root, PATCH_SUBDIR, "go1.3.7.json.diff"), exist_ok=True)
    mk("patchverdiffs/go1.3.04.json.diff")  # leading zero: never probed
    mk("patchverdiffs/go1.3.0.json.diff")   # patch 0: while-guard skips

    checks = [
        ((1, 1, 0), ("info", None)),          # patch 0: no probe
        ((1, 1, 2), ("info", None)),          # exact diff
        ((1, 1, 4), ("fallback", "1.1.3")),   # beyond last diff
        ((1, 2, 4), ("fallback", "1.2.0")),   # diffs only above request
        ((1, 2, 5), ("info", None)),
        ((1, 2, 9), ("fallback", "1.2.5")),
        ((1, 3, 7), ("fallback", "1.3.0")),   # directory decoy skipped
        ((1, 3, 4), ("fallback", "1.3.0")),   # "04" file unreachable
        ((1, 9, 0), ("none", None)),          # no base
        ((1, 9, 3), ("none", None)),
    ]
    for ver, want in checks:
        got = model_route(root, *ver)
        if got[:2] != want or not got[2]:
            cases.append(
                "FAIL %s -> %r want %r" % (ver, got, want))
    try:
        shutil_rmtree(root)
    except OSError:
        pass
    if cases:
        for c in cases:
            print(c)
        print("SELFTEST: FAILED cases=%d" % len(cases))
        return 1
    print("SELFTEST: CLEAN cases=%d" % len(checks))
    return 0


def shutil_rmtree(p):
    import shutil
    shutil.rmtree(p)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Independent GoApiSnapshot route model; sweeps "
        "1.13..1.28 x patch 0..20 and diffs vs predict.py expected "
        "fields. Never executes carriers.")
    ap.add_argument(
        "--golang-root",
        default="/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/"
                "Features/Base/data/typeinfo/golang")
    ap.add_argument(
        "--predict",
        default="/home/vgpnk/Projects/shokunin/kaidoku-shokunin/"
                ".ufo/waves/round-17/tools/predict.py")
    ap.add_argument("--out")
    ap.add_argument("--jobs", type=int, default=16)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    if not os.path.isdir(args.golang_root):
        print(json.dumps(
            {"error": "golang root not a directory: %s" % args.golang_root},
            sort_keys=True), file=sys.stderr)
        return 2
    if not os.path.isfile(args.predict):
        print(json.dumps(
            {"error": "predict.py missing: %s" % args.predict},
            sort_keys=True), file=sys.stderr)
        return 2

    rows, disagreements, crosscheck_failures, counts = sweep(
        args.golang_root, args.predict, args.jobs)

    result = {
        "tool": "route-model.py (independent reimplementation; no import "
                "of r16 selection.py / r17 predict.py)",
        "model_source": "Base-src.zip ghidra/app/util/bin/format/golang/"
                        "rtti/GoApiSnapshot.java:118-166 + GoVer.java:"
                        "127-131,154-159 + Application.java:354-374",
        "golang_root": args.golang_root,
        "predict": args.predict,
        "sweep": {
            "major": 1,
            "minor_range": [13, 28],
            "patch_range": [0, 20],
            "count": len(rows),
        },
        "route_counts": counts,
        "model_vs_predict": {
            "agree": sum(1 for r in rows if r["agree"]),
            "disagree": len(disagreements),
        },
        "internal_crosscheck": {
            "countdown_vs_listing_disagreements": len(crosscheck_failures),
            "versions": crosscheck_failures,
        },
        "disagreements": disagreements,
        "rows": rows,
    }
    text = json.dumps(result, sort_keys=True, indent=2)
    if args.out:
        try:
            with open(args.out, "w") as f:
                f.write(text + "\n")
        except OSError as e:
            print(json.dumps(
                {"error": "cannot write %s: %s" % (args.out, e)},
                sort_keys=True), file=sys.stderr)
            return 2
    print(text)
    return 1 if disagreements or crosscheck_failures else 0


if __name__ == "__main__":
    sys.exit(main())
