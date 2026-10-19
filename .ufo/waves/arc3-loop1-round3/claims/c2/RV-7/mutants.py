#!/usr/bin/env python3
"""RV-7 mutation harness — custody-pair write-guard scope + D3 reference coverage.

Runs two injection scenarios against a given tool revision:

  CL  clobber-scope: `capture --paths X --out X` on a scratch file X.
      PRE (un-guarded): X is overwritten with the receipt it measured, exit 0.
      POST (guarded):   refused with a declared usage class, X byte-stable.

  D3  partial-coverage: a 1-path reference receipt vs a 5-path candidate.
      PRE (un-guarded): exit 0, 4 paths unaccounted.
      POST (guarded):   `--require-paths 5` refuses with the declared class;
                        default-mode behaviour is measured, not assumed.

Assertions are on the CLASS LINE (REFERENCE-COVERAGE / refusing), not on the
exit code alone: at the pre-revision `--require-paths` does not exist and
argparse returns exit 2 with a usage screen — same code, no class.

Scratch only. The harness refuses any `--out` outside the run root, so the real
custody paths can never be aimed at even by a fully reverted guard.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
V1_PARTIAL_FIXTURE = REPO / ".ufo/waves/arc3-loop1-round2/claims/c3/EX-35/fixtures/v1-partial-1of5.txt"


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


def tail_line(text: str, needles) -> str:
    for line in text.splitlines():
        if any(n in line for n in needles):
            return line.strip()
    return ""


PAYLOAD = b"scoped-content-v1\n"


def _cap(tool: Path, cwd: Path, paths, out, label="rv7-clobber"):
    return run(tool, ["capture", "--paths"] + [str(p) for p in paths]
               + ["--out", str(out), "--label", label], cwd)


def _clob_result(pre_sha, watched: Path, rc, out, err, extra=None):
    post_sha = sha256_file(watched)
    text = watched.read_text(errors="replace")
    is_receipt = "PATH:" in text and "SHA256:" in text
    res = {
        "target_pre_sha256": pre_sha,
        "target_post_sha256": post_sha,
        "clobbered": post_sha != pre_sha,
        "content_is_receipt": is_receipt,
        "exit": rc,
        "out_tail": tail_line(out, ["CUSTODY_PAIR_CAPTURE", "RECEIPT:"]),
        "err_tail": tail_line(err, ["USAGE", "refus"]),
        "guard_class_seen": ("refusing" in err or "refusing" in out or "USAGE" in err),
        "verdict": "CLOBBER" if (post_sha != pre_sha and is_receipt) else (
            "MOVED-NOT-RECEIPT" if post_sha != pre_sha else "BLOCKED"),
    }
    if extra:
        res.update(extra)
    return res


def _fresh(base: Path, name: str) -> Path:
    d = base / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    return d


def scenario_clobber(tool: Path, root: Path) -> dict:
    base = root / "clobber"
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    sub = {}

    # 1. the register's shape: --paths X --out X, same spelling both sides
    d = _fresh(base, "same_path")
    x = d / "scoped.conf"
    x.write_bytes(PAYLOAD)
    pre = sha256_file(x)
    rc, o, e = _cap(tool, d, [x], x)
    sub["same_path"] = _clob_result(pre, x, rc, o, e)

    # 2. adjacent scope: --out is a symlink resolving onto the scoped path
    d = _fresh(base, "symlink_out")
    x = d / "scoped.conf"
    x.write_bytes(PAYLOAD)
    link = d / "via-link.txt"
    link.symlink_to(x)
    pre = sha256_file(x)
    rc, o, e = _cap(tool, d, [x], link)
    sub["symlink_out"] = _clob_result(pre, x, rc, o, e, {"out_was_symlink": True})

    # 3. adjacent scope: scoped set written relative, --out absolute (resolution)
    d = _fresh(base, "relpath_abs")
    x = d / "scoped.conf"
    x.write_bytes(PAYLOAD)
    pre = sha256_file(x)
    rc, o, e = _cap(tool, d, ["./scoped.conf"], x)
    sub["relpath_abs"] = _clob_result(pre, x, rc, o, e, {"paths_form": "./scoped.conf"})

    # 4. adjacent scope: the receipt target is NOT scoped, but its .sha256
    #    sidecar is -- `--paths X.sha256 --out X` (sidecar write escapes a
    #    guard that only inspects --out).
    d = _fresh(base, "sidecar_scope")
    p = d / "target.sha256"
    p.write_bytes(b"scoped-sidecar-content\n")
    q = d / "target"
    pre = sha256_file(p)
    rc, o, e = _cap(tool, d, [p], q)
    extra = {"receipt_written": q.exists(), "sidecar_path": str(p),
             "sidecar_written_by_tool": (d / "target.sha256").exists()}
    sub["sidecar_scope"] = _clob_result(pre, p, rc, o, e, extra)

    # 5. negative control: unrelated --out must still succeed (guard is not a
    #    blanket capture refusal)
    d = _fresh(base, "control")
    x2 = d / "scoped2.conf"
    x2.write_bytes(PAYLOAD)
    pre2 = sha256_file(x2)
    y = d / "unrelated-receipt.txt"
    rc2, o2, e2 = _cap(tool, d, [x2], y, label="rv7-control")
    sub["negative_control"] = {
        "exit": rc2, "receipt_written": y.exists(),
        "target_unmoved": sha256_file(x2) == pre2,
        "ok": rc2 == 0 and y.exists() and sha256_file(x2) == pre2,
    }

    return {
        "scenario": "CL",
        "tool": str(tool),
        "tool_sha256": sha256_file(tool),
        "runs": sub,
        "verdict": "CLOBBER" if sub["same_path"]["verdict"] == "CLOBBER" else "BLOCKED",
        "adjacent": {k: sub[k]["verdict"] for k in ("symlink_out", "relpath_abs", "sidecar_scope")},
    }


def scenario_partial(tool: Path, root: Path) -> dict:
    work = root / "partial"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    names = ["a", "b", "c", "d", "e"]
    for n in names:
        (work / ("%s.conf" % n)).write_bytes(b"partial-fixture-%s\n" % n.encode())

    r1 = work / "r1.txt"
    r5 = work / "r5.txt"
    rc1, o1, e1 = run(tool, ["capture", "--out", r1, "--paths", work / "a.conf"], work)
    rc5, o5, e5 = run(tool, ["capture", "--out", r5, "--paths"] + [work / ("%s.conf" % n) for n in names], work)
    if rc1 != 0 or rc5 != 0:
        return {"scenario": "D3", "error": "reference capture failed", "rc1": rc1, "rc5": rc5,
                "e1": e1, "e5": e5}

    runs = {}
    for name, argv in [
        ("v2live_r1", ["verify", r1, "--live"]),
        ("v2live_r1_flag5", ["verify", r1, "--live", "--require-paths", "5"]),
        ("v2live_r5_flag5", ["verify", r5, "--live", "--require-paths", "5"]),
        ("default", ["verify", r1, r5]),
        ("flag5", ["verify", r1, r5, "--require-paths", "5"]),
        ("flag1", ["verify", r1, r5, "--require-paths", "1"]),
        ("control_full", ["verify", r5, r5, "--require-paths", "5"]),
        ("v1fixture_default", ["verify", V1_PARTIAL_FIXTURE, "--live"]),
        ("v1fixture_flag5", ["verify", V1_PARTIAL_FIXTURE, "--live", "--require-paths", "5"]),
    ]:
        rc, out, err = run(tool, argv, work)
        runs[name] = {
            "argv": [str(a) for a in argv],
            "exit": rc,
            "coverage_class": tail_line(out, ["REFERENCE-COVERAGE"]),
            "coverage_class_present": "REFERENCE-COVERAGE" in out,
            "usage_line": tail_line(err + out, ["USAGE", "unrecognized", "no such option"]),
            "verdict_line": tail_line(out, ["VERDICT:"]),
            "tail": tail_line(out, ["CUSTODY_PAIR_VERIFY"]),
        }
    return {
        "scenario": "D3",
        "tool": str(tool),
        "tool_sha256": sha256_file(tool),
        "runs": runs,
        "verdict": "EXIT0-ON-PARTIAL" if runs["default"]["exit"] == 0 else "REFUSED-DEFAULT",
    }


def apply_mutation(src: Path, dst: Path, spec: dict, note: str) -> dict:
    """Apply a textual revert spec {old: new, ...} with an applied-count check."""
    import difflib
    text = src.read_text()
    applied = []
    for old, new in spec.items():
        n = text.count(old)
        if n == 0:
            raise SystemExit("MUTATION ANCHOR NOT FOUND in %s: %r" % (src, old[:80]))
        text = text.replace(old, new)
        applied.append({"old": old, "new": new, "count": n})
    dst.write_text(text)
    diff = "".join(difflib.unified_diff(
        src.read_text().splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile="hardened", tofile="mutant"))
    return {"mutant": str(dst), "note": note, "applied": applied,
            "diff": diff, "mutant_sha256": sha256_file(dst),
            "src_sha256": sha256_file(src)}


def scenario_coverage_subversion(tool: Path, root: Path) -> dict:
    """The --require-paths gate counts stanzas (len(ref_sections)); a reference
    repeating one path N times may satisfy it while still examining one path."""
    work = root / "coverage-subversion"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    a = work / "a.conf"
    a.write_bytes(b"subversion-fixture-a\n")
    dup = work / "dup5.txt"
    rc0, o0, e0 = run(tool, ["capture", "--out", dup, "--paths"] + [a] * 5, work)
    runs = {}
    for name, argv in [
        ("dup5_default", ["verify", dup, "--live"]),
        ("dup5_flag5", ["verify", dup, "--live", "--require-paths", "5"]),
    ]:
        rc, out, err = run(tool, argv, work)
        runs[name] = {
            "argv": [str(x) for x in argv],
            "exit": rc,
            "coverage_line": tail_line(out, ["REFERENCE-COVERAGE"]),
            "coverage_class_present": "REFERENCE-COVERAGE" in out,
            "verdict_line": tail_line(out, ["VERDICT:"]),
            "usage_line": tail_line(err, ["USAGE"]),
        }
    return {
        "scenario": "D3sub",
        "tool_sha256": sha256_file(tool),
        "dup_capture_exit": rc0,
        "dup_stanzas": dup.read_text().count("PATH:") if dup.exists() else 0,
        "runs": runs,
        "verdict": ("SUBVERTED" if runs["dup5_flag5"]["exit"] == 0 and
                    "REFERENCE-COVERAGE" in (runs["dup5_flag5"]["coverage_line"] + " ")
                    else ("PASSED-GATE" if runs["dup5_flag5"]["exit"] == 0 else "GATE-FIRED")),
    }


def scenario_selftest(tool: Path, root: Path) -> dict:
    """The tool's own fixture suite as a second oracle: a mutant the shipped
    selftest does not kill is a measurement about the selftest, not the guard."""
    base = root / "selftest-scratch"
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    rc, out, err = run(tool, ["selftest", "--scratch", base], root)
    cases = [l.strip() for l in out.splitlines() if l.strip().startswith("case ")]
    failed = [c for c in cases if " FAIL" in c]
    return {
        "exit": rc,
        "summary": tail_line(out, ["CUSTODY_PAIR_SELFTEST"]),
        "cases": len(cases),
        "failed_cases": failed,
        "traceback": ("Traceback" in err),
        "err_tail": tail_line(err, ["Error", "error", "USAGE"]),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--root", required=True, help="scratch run root")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--note", default="")
    ap.add_argument("--mutate-spec", default=None, help="JSON file of {old:new} reverts")
    ap.add_argument("--out", required=True, help="result JSON path")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    assert str(root).startswith(("/dev/shm/", "/var/tmp/")), "scratch must be /dev/shm or /var/tmp"

    src_tool = Path(args.tool).resolve()
    # Materialise the revision/mutant as <tag>/tool/custody-pair.py: the tool's
    # own selftest TZ case re-invokes a sibling named custody-pair.py, so a
    # differently-named copy fails a case that is not about the code under test.
    tool_dir = root / args.tag / "tool"
    tool_dir.mkdir(parents=True, exist_ok=True)
    tool = tool_dir / "custody-pair.py"
    mutation = None
    if args.mutate_spec:
        spec = json.loads(Path(args.mutate_spec).read_text())
        mutation = apply_mutation(src_tool, tool, spec, args.note or args.tag)
    else:
        shutil.copyfile(src_tool, tool)

    res = {
        "tag": args.tag,
        "note": args.note,
        "tool_src": str(src_tool),
        "tool_src_sha256": sha256_file(src_tool),
        "utc": subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True).stdout.strip(),
        "mutation": mutation,
        "selftest": scenario_selftest(tool, root / args.tag),
        "clobber": scenario_clobber(tool, root / args.tag),
        "partial": scenario_partial(tool, root / args.tag),
        "coverage_subversion": scenario_coverage_subversion(tool, root / args.tag),
    }
    Path(args.out).write_text(json.dumps(res, indent=2) + "\n")
    print(json.dumps({k: res[k] for k in ("tag", "utc")}, indent=2))
    print("SELFTEST:", json.dumps(res["selftest"], indent=2))
    print("CL :", json.dumps(res["clobber"], indent=2))
    print("D3 :", json.dumps(res["partial"], indent=2))
    print("D3sub:", json.dumps(res["coverage_subversion"], indent=2))


if __name__ == "__main__":
    main()