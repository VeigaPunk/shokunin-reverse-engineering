#!/usr/bin/env python3
"""EX-15 fixture harness — run the census against every fixture case and check
the declared expectations (arc3-loop1-round2, chain c2).

Usage:
  python3 run_fixtures.py --phase before|after [--instrument PATH]
                          [--work /dev/shm/ex15-fixtures] [--cases cases.json]
                          [--outdir measurements/<phase>-<sha8>] [--json-check]
                          [--expect-sha HEX]

Contract:
  * --phase selects which expectation block in cases.json is enforced.
    before expects the frozen pre-edit v10 (6f1d19ff...);
    after  expects the landed v11 fail-closures (82fb807e...).
  * every case is materialized fresh under --work (never in the repo, never /tmp);
    per-case HOME is either the fixture fakehome or the real user home.
  * hard-severity mismatches fail the run (exit 1); advisory cases and `soft`
    tokens report as WARN; `reading` cases report which floor reading the
    instrument exhibits (STRICT = current-ok loci >= 1, WEAK = any locus).
  * raw stdout+exit per case is written under --outdir, plus results.json.
"""
import argparse, hashlib, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
FILES = ("PROVINCE.md", "SKILL.md", "SCORECARD.md")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def force_rmtree(path):
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        try:
            os.chmod(dirpath, 0o700)
        except OSError:
            pass
        for fn in filenames:
            try:
                os.chmod(os.path.join(dirpath, fn), 0o600)
            except OSError:
                pass
    shutil.rmtree(path, ignore_errors=True)


def materialize(case, work, fixtures):
    cdir = os.path.join(work, case["id"])
    if os.path.exists(cdir):
        force_rmtree(cdir)
    root = os.path.join(cdir, "root")
    os.makedirs(root)
    src = case.get("source")
    if src == "@repo":
        for f in FILES:
            shutil.copy2(os.path.join(REPO, f), os.path.join(root, f))
    elif src:
        srcdir = os.path.join(fixtures, src)
        for f in sorted(os.listdir(srcdir)):
            shutil.copy2(os.path.join(srcdir, f), os.path.join(root, f))
    for op in case.get("ops", []):
        p = os.path.join(root, op["path"])
        kind = op["op"]
        if kind == "mkdir":
            os.makedirs(p, exist_ok=True)
        elif kind == "symlink":
            os.symlink(op["target"], p)
        elif kind == "chmod":
            os.chmod(p, int(op["mode"], 8))
        else:
            raise SystemExit("unknown op %r" % op)
    return root


def run_inst(instrument, root, home, extra=()):
    env = dict(os.environ)
    env["HOME"] = home
    p = subprocess.run([sys.executable, instrument, "--root", root] + list(extra),
                       capture_output=True, text=True, env=env)
    return p.returncode, p.stdout + p.stderr


def check_block(expect, rc, out, classes):
    problems = []
    if rc != expect["exit"]:
        problems.append("exit %d != expected %d" % (rc, expect["exit"]))
    for tok in expect.get("must", []):
        if tok not in out:
            problems.append("missing token %r" % tok)
    for tok in expect.get("must_not", []):
        if tok in out:
            problems.append("forbidden token present %r" % tok)
    for cl in expect.get("classes", []):
        spec = classes[cl]
        if not any(t in out for t in spec["tokens_any"]):
            problems.append("missing declared-class token for %s (%s)"
                            % (cl, spec["declared_label"]))
    soft = [t for t in expect.get("soft", []) if t not in out]
    return problems, soft


def json_probe(instrument, root, home, expect, classes):
    rc, out = run_inst(instrument, root, home, ["--json"])
    notes = []
    try:
        d = json.loads(out)
    except ValueError as ex:
        return ["json parse failed: %s" % ex]
    if rc != expect["exit"]:
        notes.append("json-mode exit %d != expected %d" % (rc, expect["exit"]))
    for cl in expect.get("classes", []):
        spec = classes[cl]
        v = d.get(spec["json_key"])
        if spec.get("json_must_be_nonempty") and not v:
            notes.append("json[%r] empty" % spec["json_key"])
        if spec.get("json_must_contain") and spec["json_must_contain"] not in (v or []):
            notes.append("json[%r] lacks %r" % (spec["json_key"], spec["json_must_contain"]))
    return notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True, choices=["before", "after"])
    ap.add_argument("--instrument", default=os.path.join(REPO, ".ufo/gates/c1-census-v10.py"))
    ap.add_argument("--cases", default=os.path.join(HERE, "cases.json"))
    ap.add_argument("--work", default="/dev/shm/ex15-fixtures")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--json-check", action="store_true")
    ap.add_argument("--expect-sha", default=None,
                    help="refuse to run unless the instrument sha256 equals this")
    ap.add_argument("--keep", action="store_true", help="keep the scratch work tree")
    args = ap.parse_args()

    man = json.load(open(args.cases, encoding="utf-8"))
    classes = man["classes"]
    if args.expect_sha:
        got = sha256_file(args.instrument)
        if got != args.expect_sha:
            print("REFUSING: instrument sha %s != --expect-sha %s" % (got, args.expect_sha))
            return 2

    inst_sha = sha256_file(args.instrument)
    outdir = args.outdir or os.path.join(HERE, "measurements", "%s-%s" % (args.phase, inst_sha[:8]))
    os.makedirs(outdir, exist_ok=True)
    fakehome = os.path.join(HERE, "fakehome")
    realhome = os.path.expanduser("~")
    if not os.path.isdir(fakehome):
        print("fixture fakehome missing; run gen_fixtures.py first")
        return 2

    results, hard_fail = [], 0
    for case in man["cases"]:
        home = fakehome if case.get("home") == "fakehome" else realhome
        root = materialize(case, args.work, HERE)
        rc, out = run_inst(args.instrument, root, home)
        open(os.path.join(outdir, case["id"] + ".out"), "w", encoding="utf-8").write(
            "$ python3 %s --root %s   [HOME=%s]\nexit=%d\n%s" %
            (os.path.basename(args.instrument), root,
             "fakehome" if case.get("home") == "fakehome" else "real", rc, out))

        exp = case["expect"]
        row = {"id": case["id"], "severity": case["severity"], "class": case["class"],
               "exit": rc, "root": root}
        if "readings" in exp:
            reading = None
            for mode in exp["readings"]:
                problems, _ = check_block(exp["readings"][mode], rc, out, classes)
                if not problems:
                    reading = mode
                    break
            row["status"] = "READING(%s)" % (reading or "UNKNOWN")
            row["observed"] = {"g2_line": next(
                (l for l in out.splitlines() if l.startswith("G2 positive-assertion")), None)}
            print("%-20s %-16s exit=%d  %s" % (case["id"], row["status"], rc,
                                               row["observed"]["g2_line"] or ""))
        else:
            problems, soft = check_block(exp[args.phase], rc, out, classes)
            if problems and case["severity"] == "hard":
                row["status"] = "FAIL"
                row["problems"] = problems
                hard_fail += 1
            elif problems:
                row["status"] = "WARN"
                row["problems"] = problems
            else:
                row["status"] = "PASS"
            if soft:
                row["status"] = "WARN" if row["status"] == "PASS" else row["status"]
                row["soft_missing"] = soft
            print("%-20s %-16s exit=%d  %s" % (case["id"], row["status"], rc,
                                               "; ".join(row.get("problems", []) or row.get("soft_missing", []))[:110]))
        if args.json_check:
            row["json_notes"] = json_probe(args.instrument, root, home, exp.get(args.phase, exp), classes) \
                if "readings" not in exp else ["(reading case: json probe skipped)"]
            if row["json_notes"] and row["status"] == "PASS":
                row["status"] = "PASS"
        results.append(row)

    summary = {"instrument": args.instrument, "sha256": inst_sha, "phase": args.phase,
               "hard_fail": hard_fail,
               "readings": {r["id"]: r["status"] for r in results if r["status"].startswith("READING")}}
    with open(os.path.join(outdir, "results.json"), "w", encoding="utf-8") as fh:
        json.dump({"summary": summary, "cases": results}, fh, indent=1)
    print("\nsummary: phase=%s sha=%s hard_fail=%d results=%s" %
          (args.phase, inst_sha[:8], hard_fail, os.path.join(outdir, "results.json")))
    if not args.keep:
        force_rmtree(args.work)
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
