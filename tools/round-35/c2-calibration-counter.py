#!/usr/bin/env python3
# R35-C2 calibration counter (frozen; reads only immutable git objects).
# Evaluates closure of the four round-34 verifier-routed record defects D-1..D-4
# at the measured revision. Exit 0 = all four closed; 1 = named failures; 2 = unevaluable.
import argparse, datetime, json, re, subprocess, sys, tempfile, os

PREDICATE = (
    "P35-c2: at the measured revision, the four round-34 verifier-routed record "
    "defects are closed: (D-1) the round-35 census-start receipt is committed before "
    "the first corpus/SOURCES.md change of the round and carries the base count "
    "(106 rows, exit 0, 9 W04 warnings); (D-2) the round-35 lesson records the "
    "r34 w2 seat-accounting correction (31/32 reports, AAdjacencyCite unreported) "
    "and states wave seat totals identical to the committed settle receipts; "
    "(D-3) the r34b knowledge entry carries an appended provenance trio "
    "(source:/verified-at:/recheck:) citing S106; (D-4) every data row of the "
    "round-32 and round-34 run-6 instrument-registry tables in SKILL.md has "
    "exactly eight cells."
)

# Registry table sections whose every row must render 8 cells (NF == 9).
EIGHT_CELL_SECTIONS = [
    "### Round-32 instrument registry",
    "### Round-34 run-6 instrument registry",
]

SETTLE_FILES = [
    ".ufo/waves/round-35/w1-settle.json",
    ".ufo/waves/round-35/w2-settle.json",
]

LESSON_PATH = "corpus/lessons/round-35.md"
CENSUS_PATH = ".ufo/waves/round-35/assimilation/census-start.txt"
R34B_ENTRY = "corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md"


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def show(root, rev, path):
    r = git(root, "show", f"{rev}:{path}")
    return r.stdout if r.returncode == 0 else None


def commit_time(root, rev, path):
    r = git(root, "log", "--format=%cI", "-1", rev, "--", path)
    return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else None


def first_change_time(root, base, rev, path):
    r = git(root, "log", "--format=%cI", f"{base}..{rev}", "--", path)
    lines = [x.strip() for x in r.stdout.splitlines() if x.strip()]
    return lines[-1] if lines else None  # oldest = first change


def parse_iso(s):
    return datetime.datetime.fromisoformat(s)


def check(root, base, rev):
    fails = []

    # D-1 census start receipt
    census = show(root, rev, CENSUS_PATH)
    if census is None:
        fails.append("D1_census_start_missing")
    else:
        if "rows=106" not in census or "EXIT=0" not in census or "W04" not in census:
            fails.append("D1_census_content_missing")
        ct = commit_time(root, rev, CENSUS_PATH)
        fc = first_change_time(root, base, rev, "corpus/SOURCES.md")
        if ct is None:
            fails.append("D1_census_commit_unknown")
        elif fc is None:
            fails.append("D1_no_sources_change_after_base")
        elif parse_iso(ct) > parse_iso(fc):
            fails.append("D1_census_after_first_sources_change")

    # D-2 lesson seat accounting + r34 w2 correction
    lesson = show(root, rev, LESSON_PATH)
    if lesson is None:
        fails.append("D2_lesson_missing")
    else:
        if "AAdjacencyCite" not in lesson or "31/32" not in lesson:
            fails.append("D2_r34w2_correction_missing")
        total_spawned = 0
        total_settled = 0
        total_dead = 0
        for sf in SETTLE_FILES:
            j = show(root, rev, sf)
            if j is None:
                fails.append(f"D2_settle_missing:{sf}")
                continue
            try:
                obj = json.loads(j)
            except Exception:
                fails.append(f"D2_settle_unparseable:{sf}")
                continue
            if not isinstance(obj, dict):
                fails.append(f"D2_settle_shape:{sf}")
                continue
            for key in ("spawned", "settled", "dead"):
                v = obj.get(key)
                if not isinstance(v, int):
                    fails.append(f"D2_settle_missing_field:{sf}:{key}")
            total_spawned += obj.get("spawned", 0)
            total_settled += obj.get("settled", 0)
            total_dead += obj.get("dead", 0)
        m = re.search(r"Seat accounting \(round 35\): spawned=(\d+) settled=(\d+) dead=(\d+)", lesson)
        if m is None:
            fails.append("D2_lesson_seat_line_missing")
        elif (int(m.group(1)), int(m.group(2)), int(m.group(3))) != (total_spawned, total_settled, total_dead):
            fails.append("D2_lesson_seat_mismatch")

    # D-3 provenance trio on r34b entry
    body = show(root, rev, R34B_ENTRY)
    if body is None:
        fails.append("D3_entry_missing")
    else:
        if not re.search(r"(?m)^source\s*:", body):
            fails.append("D3_source_missing")
        if not re.search(r"(?m)^verified-at\s*:", body):
            fails.append("D3_verified_at_missing")
        if not re.search(r"(?m)^recheck\s*:", body):
            fails.append("D3_recheck_missing")
        if not re.search(r"(?m)^source\s*:.*S106", body):
            fails.append("D3_source_not_s106")

    # D-4 eight-cell registry rows
    skill = show(root, rev, "SKILL.md")
    if skill is None:
        fails.append("D4_skill_missing")
    else:
        lines = skill.splitlines()
        for sec in EIGHT_CELL_SECTIONS:
            idx = None
            for i, l in enumerate(lines):
                if l.rstrip() == sec:
                    idx = i
                    break
            if idx is None:
                fails.append(f"D4_section_missing:{sec}")
                continue
            j = idx + 1
            while j < len(lines) and not lines[j].startswith("##") and not lines[j].startswith("###"):
                l = lines[j]
                if l.startswith("|"):
                    n = l.count("|") - 1
                    if n != 8:
                        fails.append(f"D4_not_eight_cells:{sec}:line{j+1}:cells={n}")
                        break
                j += 1
    return fails


def selftest(args):
    with tempfile.TemporaryDirectory(prefix="r35c2-selftest-") as d:
        subprocess.run(["git", "init", "-q"], cwd=d, check=True)
        subprocess.run(["git", "config", "user.email", "t@t"], cwd=d, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=d, check=True)
        os.makedirs(os.path.join(d, "corpus/lessons"), exist_ok=True)
        os.makedirs(os.path.join(d, "corpus/knowledge"), exist_ok=True)
        os.makedirs(os.path.join(d, ".ufo/waves/round-35/assimilation"), exist_ok=True)
        os.makedirs(os.path.join(d, ".ufo/waves/round-35"), exist_ok=True)
        os.makedirs(os.path.join(d, "plans"), exist_ok=True)
        with open(os.path.join(d, "plans/round-35-freeze.json"), "w") as f:
            json.dump({"round": 35, "predicate": PREDICATE, "claims": ["C1", "C2"]}, f)
        with open(os.path.join(d, "corpus/SOURCES.md"), "w") as f:
            f.write("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n")
            f.write("|---|---|---|---|---|---|---|---|---|---|---|\n")
            f.write("| S125 | x | docs | A | x | x | x | mined | 2026-10-25 | 180d | — |\n")
        with open(os.path.join(d, "corpus/lessons/round-35.md"), "w") as f:
            f.write("Seat accounting (round 35): spawned=4 settled=4 dead=0\n")
            f.write("AAdjacencyCite 31/32 correction\n")
        with open(os.path.join(d, "corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md"), "w") as f:
            f.write("source: S106\nverified-at: 2026-10-25\nrecheck: 180d\n")
        with open(os.path.join(d, "SKILL.md"), "w") as f:
            f.write("### Round-32 instrument registry\n")
            f.write("| a | b | c | d | e | f | g | h |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
            f.write("| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |\n")
            f.write("### Round-34 run-6 instrument registry\n")
            f.write("| a | b | c | d | e | f | g | h |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
            f.write("| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |\n")
        with open(os.path.join(d, ".ufo/waves/round-35/assimilation/census-start.txt"), "w") as f:
            f.write("rows=106 EXIT=0 W04 warnings\n")
        with open(os.path.join(d, ".ufo/waves/round-35/w1-settle.json"), "w") as f:
            json.dump({"spawned": 2, "settled": 2, "dead": 0}, f)
        with open(os.path.join(d, ".ufo/waves/round-35/w2-settle.json"), "w") as f:
            json.dump({"spawned": 2, "settled": 2, "dead": 0}, f)
        subprocess.run(["git", "add", "-A"], cwd=d, check=True)
        subprocess.run(["git", "commit", "-qm", "green"], cwd=d, check=True)
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=d, text=True).strip()
        # second commit: a post-base corpus/SOURCES.md change, so D-1's
        # first-change ordering is exercised (census commit precedes it)
        with open(os.path.join(d, "corpus/SOURCES.md"), "a") as f:
            f.write("| S130 | y | docs | A | x | x | x | mined | 2026-10-25 | 180d | — |\n")
        subprocess.run(["git", "add", "-A"], cwd=d, check=True)
        subprocess.run(["git", "commit", "-qm", "green2-sources-change"], cwd=d, check=True)
        # green tip: fix first commit time ordering
        green = subprocess.run([sys.executable, "-I", "-B", __file__,
                                "--root", d, "--base", base, "--rev", "HEAD", "--freeze", base],
                               capture_output=True, text=True)
        if green.returncode != 0:
            return "green-failed", green.stdout + green.stderr
        # red: corrupt one check (lesson numbers mismatch settle receipts)
        with open(os.path.join(d, "corpus/lessons/round-35.md"), "w") as f:
            f.write("Seat accounting (round 35): spawned=99 settled=99 dead=0\n")
            f.write("AAdjacencyCite 31/32 correction\n")
        subprocess.run(["git", "add", "-A"], cwd=d, check=True)
        subprocess.run(["git", "commit", "-qm", "red"], cwd=d, check=True)
        red = subprocess.run([sys.executable, "-I", "-B", __file__,
                              "--root", d, "--base", base, "--rev", "HEAD", "--freeze", base],
                             capture_output=True, text=True)
        if red.returncode == 0:
            return "red-accepted", red.stdout
        return "ok", f"green={green.returncode} red={red.returncode}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--base")
    ap.add_argument("--rev")
    ap.add_argument("--freeze")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        verdict, detail = selftest(args)
        print(f"C2_SELFTEST: {verdict}\n{detail}")
        sys.exit(0 if verdict == "ok" else 1)

    if not (args.root and args.base and args.rev and args.freeze):
        ap.print_usage(file=sys.stderr)
        sys.exit(2)

    claims = show(args.root, args.freeze, "plans/round-35-freeze.json")
    if claims is None:
        print("C2: claims file absent at freeze revision", file=sys.stderr)
        sys.exit(2)
    try:
        claims_obj = json.loads(claims)
    except Exception as e:
        print(f"C2: claims unparseable: {e}", file=sys.stderr)
        sys.exit(2)
    if PREDICATE not in json.dumps(claims_obj):
        print("C2: predicate mismatch between counter and claims file", file=sys.stderr)
        sys.exit(2)

    fails = check(args.root, args.base, args.rev)
    receipt = {
        "instrument": "tools/round-35/c2-calibration-counter.py",
        "predicate": PREDICATE,
        "base": args.base,
        "revision": args.rev,
        "freeze": args.freeze,
        "failing": fails,
        "pass": not fails,
    }
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(receipt, f, indent=1)
    if fails:
        print("C2_FAIL:", "; ".join(fails))
        sys.exit(1)
    print("C2_CLEAN revision=" + args.rev)
    sys.exit(0)


if __name__ == "__main__":
    main()
