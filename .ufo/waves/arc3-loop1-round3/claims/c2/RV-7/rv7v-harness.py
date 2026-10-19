#!/usr/bin/env python3
"""RV-7 late-join independent harness — write-guard scope + D3 coverage gate.

Fresh implementation (does not import or reuse mutants.py). Every arm runs on a
/var/tmp copy of the tool. Scenarios:

  A. write-guard scope
     A1 same-path   : capture --paths X --out X           (the VZ-4 register shape)
     A2 hardlink    : capture --paths X --out H (H hardlink alias of X)
     A3 symlink     : capture --paths X --out S (S symlink to X)
     A4 control     : capture --paths X --out R (unrelated) must still succeed

  B. D3 reference coverage
     B1 verify r1 r5 (default)              -> declared: exit 0, no gate
     B2 verify r1 r5 --require-paths 5      -> POST: exit 2 + REFERENCE-COVERAGE
                                               PRE : exit 2, NO class (argparse)
     B3 verify r1 --live --require-paths 5  -> same distinction
     B4 verify r5 r5 --require-paths 5      -> control: exit 0
     B5 dup-path ref --require-paths 5      -> gate counts stanzas (subversion probe)

Load-bearing assertions are on the CLASS LINE plus byte-stability of the
scoped file, never on exit code alone (PRE argparse exit 2 collides with the
declared USAGE exit 2).
"""
import argparse
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRATCH_ROOTS = ("/var/tmp/", "/dev/shm/")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(tool: Path, args, cwd: Path):
    proc = subprocess.run([sys.executable, str(tool)] + [str(a) for a in args],
                          capture_output=True, text=True, cwd=str(cwd))
    return proc.returncode, proc.stdout, proc.stderr


def grep_line(text: str, needles) -> str:
    for line in text.splitlines():
        if any(n in line for n in needles):
            return line.strip()
    return ""


def fresh(base: Path, name: str) -> Path:
    d = base / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    return d


def scenario_guard(tool: Path, root: Path) -> dict:
    base = root / "guard"
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    out = {}

    def cap(d, paths, receipt, label):
        rc, o, e = run(tool, ["capture", "--paths"] + [str(p) for p in paths]
                       + ["--out", str(receipt), "--label", label], d)
        return rc, o, e

    def guarded_case(name, build, note=""):
        d = fresh(base, name)
        target, receipt = build(d)
        pre = sha256_file(target)
        rc, o, e = cap(d, [target], receipt, "rv7v-" + name)
        post = sha256_file(target)
        body = target.read_text(errors="replace")
        return {
            "note": note,
            "target": str(target),
            "receipt_arg": str(receipt),
            "exit": rc,
            "target_sha_before": pre,
            "target_sha_after": post,
            "byte_stable": pre == post,
            "content_now_receipt": ("PATH:" in body and "SHA256:" in body),
            "class_line": grep_line(o + e, ["REFUS", "refus", "USAGE"]),
            "clobbered": pre != post and ("PATH:" in body and "SHA256:" in body),
            "out_tail": grep_line(o, ["RECEIPT:", "CUSTODY_PAIR_CAPTURE"]),
        }

    def same(d):
        x = d / "scoped.conf"
        x.write_bytes(b"rv7v-scoped-payload\n")
        return x, x

    def hardlink(d):
        x = d / "scoped.conf"
        x.write_bytes(b"rv7v-scoped-payload\n")
        h = d / "alias-receipt.txt"
        os.link(x, h)
        return x, h

    def symlink(d):
        x = d / "scoped.conf"
        x.write_bytes(b"rv7v-scoped-payload\n")
        s = d / "via-symlink.txt"
        s.symlink_to(x)
        return x, s

    out["A1_same_path"] = guarded_case("A1_same_path", same, "register shape: --paths X --out X")
    out["A2_hardlink"] = guarded_case("A2_hardlink", hardlink, "inode arm: --out is a hardlink alias")
    out["A3_symlink"] = guarded_case("A3_symlink", symlink, "resolution arm: --out symlinks onto X")

    # A5: the guard inspects --out, but capture also writes the `.sha256`
    # sidecar next to it — scoping the *sidecar* path is the escape shape.
    def sidecar(d):
        p = d / "target.sha256"
        p.write_bytes(b"rv7v-sidecar-payload\n")
        q = d / "target"
        return p, q

    out["A5_sidecar_escape"] = guarded_case(
        "A5_sidecar_escape", sidecar,
        "--paths X.sha256 --out X: receipt at X, sidecar write lands on X.sha256")

    d = fresh(base, "A4_control")
    x = d / "scoped.conf"
    x.write_bytes(b"rv7v-scoped-payload\n")
    r = d / "receipt.txt"
    pre = sha256_file(x)
    rc, o, e = cap(d, [x], r, "rv7v-control")
    out["A4_control"] = {
        "exit": rc, "receipt_written": r.exists(),
        "target_untouched": sha256_file(x) == pre,
        "ok": rc == 0 and r.exists() and sha256_file(x) == pre,
    }
    return out


def scenario_coverage(tool: Path, root: Path, fixture_1of5: Path) -> dict:
    work = root / "coverage"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    names = ["a", "b", "c", "d", "e"]
    for n in names:
        (work / (n + ".conf")).write_bytes(b"rv7v-fixture-" + n.encode() + b"\n")
    r1, r5 = work / "ref-1.txt", work / "ref-5.txt"
    rc1, o1, e1 = run(tool, ["capture", "--out", r1, "--paths", work / "a.conf"], work)
    rc5, o5, e5 = run(tool, ["capture", "--out", r5, "--paths"] + [work / (n + ".conf") for n in names], work)
    if rc1 or rc5:
        return {"error": "reference capture failed", "rc1": rc1, "rc5": rc5, "e1": e1, "e5": e5}

    def one(name, argv, note=""):
        rc, o, e = run(tool, argv, work)
        return {
            "argv": [str(a) for a in argv], "note": note, "exit": rc,
            "coverage_class": grep_line(o, ["REFERENCE-COVERAGE"]),
            "class_present": "REFERENCE-COVERAGE" in o,
            "usage_line": grep_line(e + o, ["USAGE"]),
            "verdict_line": grep_line(o, ["VERDICT:"]),
        }

    res = {
        "B1_default_pair": one("B1", ["verify", r1, r5], "default: no gate by design"),
        "B2_flag5_pair": one("B2", ["verify", r1, r5, "--require-paths", "5"], "the D3 gate"),
        "B3_flag5_live": one("B3", ["verify", r1, "--live", "--require-paths", "5"], "live + gate"),
        "B4_control_full": one("B4", ["verify", r5, r5, "--require-paths", "5"], "control: 5-path ref passes"),
    }
    # the round-2 recorded fixture, if present (absolute path outside scratch)
    if fixture_1of5.exists():
        rc, o, e = run(tool, ["verify", fixture_1of5, "--live", "--require-paths", "5"], work)
        res["B5_v1_1of5_fixture"] = {
            "argv": ["verify", str(fixture_1of5), "--live", "--require-paths", "5"],
            "exit": rc, "coverage_class": grep_line(o, ["REFERENCE-COVERAGE"]),
            "class_present": "REFERENCE-COVERAGE" in o, "usage_line": grep_line(e + o, ["USAGE"]),
        }
    # subversion probe: a reference repeating one path 5x satisfies a stanza count
    dup = work / "dup5.txt"
    rc0, o0, e0 = run(tool, ["capture", "--out", dup, "--paths"] + [work / "a.conf"] * 5, work)
    res["B6_dup_stanzas"] = one("B6", ["verify", dup, "--live", "--require-paths", "5"],
                                "subversion: 5 stanzas, 1 distinct path")
    res["B6_dup_stanza_count"] = dup.read_text().count("PATH:") if dup.exists() else 0
    res["B6_dup_capture_exit"] = rc0
    return res


def scenario_selftest(tool: Path, root: Path) -> dict:
    base = root / "selftest-scratch"
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    rc, o, e = run(tool, ["selftest", "--scratch", base], root)
    cases = [l.strip() for l in o.splitlines() if l.strip().startswith("case ")]
    return {
        "exit": rc,
        "summary": grep_line(o, ["CUSTODY_PAIR_SELFTEST"]),
        "cases": len(cases),
        "failed": [c for c in cases if " FAIL" in c],
        "traceback": "Traceback" in e,
    }


def apply_mutation(src: Path, dst: Path, spec: dict) -> dict:
    text = src.read_text()
    applied = []
    for old, new in spec.items():
        n = text.count(old)
        if n == 0:
            raise SystemExit("ANCHOR NOT FOUND: %r" % old[:90])
        text = text.replace(old, new)
        applied.append({"count": n, "old": old[:100], "new": new[:100]})
    dst.write_text(text)
    diff = "".join(difflib.unified_diff(src.read_text().splitlines(keepends=True),
                                        text.splitlines(keepends=True),
                                        fromfile="landed", tofile="mutant"))
    return {"applied": applied, "mutant_sha256": sha256_file(dst),
            "src_sha256": sha256_file(src), "diff": diff,
            "net_lines": len(text.splitlines()) - len(src.read_text().splitlines())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--note", default="")
    ap.add_argument("--mutate-spec", default=None)
    ap.add_argument("--fixture-1of5", default="/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round2/claims/c3/EX-35/fixtures/v1-partial-1of5.txt")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    assert str(root).startswith(SCRATCH_ROOTS), "scratch must be /var/tmp or /dev/shm"

    src = Path(args.tool).resolve()
    tdir = root / args.tag / "tool"
    tdir.mkdir(parents=True, exist_ok=True)
    tool = tdir / "custody-pair.py"
    mutation = None
    if args.mutate_spec:
        mutation = apply_mutation(src, tool, json.loads(Path(args.mutate_spec).read_text()))
    else:
        shutil.copyfile(src, tool)

    res = {
        "tag": args.tag, "note": args.note,
        "tool_src": str(src), "tool_src_sha256": sha256_file(src),
        "tool_materialized_sha256": sha256_file(tool),
        "utc": subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                              capture_output=True, text=True).stdout.strip(),
        "mutation": mutation,
        "selftest": scenario_selftest(tool, root / args.tag),
        "guard": scenario_guard(tool, root / args.tag),
        "coverage": scenario_coverage(tool, root / args.tag, Path(args.fixture_1of5)),
    }
    Path(args.out).write_text(json.dumps(res, indent=2) + "\n")
    print("== %s  tool=%s" % (args.tag, res["tool_materialized_sha256"][:16]))
    print("selftest:", res["selftest"]["summary"])
    for k in ("A1_same_path", "A2_hardlink", "A3_symlink", "A5_sidecar_escape"):
        r = res["guard"][k]
        print("%-14s exit=%d stable=%s clobbered=%s class=%r" %
              (k, r["exit"], r["byte_stable"], r["clobbered"], r["class_line"][:70]))
    print("A4_control ok=%s" % res["guard"]["A4_control"]["ok"])
    for k in ("B1_default_pair", "B2_flag5_pair", "B3_flag5_live", "B4_control_full", "B6_dup_stanzas"):
        r = res["coverage"].get(k)
        if r:
            print("%-18s exit=%d class_present=%s class=%r" %
                  (k, r["exit"], r["class_present"], r["coverage_class"][:70]))


if __name__ == "__main__":
    main()
