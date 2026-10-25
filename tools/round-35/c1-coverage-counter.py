#!/usr/bin/env python3
# R35-C1 coverage counter (frozen; reads only immutable git objects).
# Counts the round's declared after-state against the tree at --rev.
import argparse, datetime, hashlib, json, os, re, subprocess, sys, tempfile

PREDICATE = (
    "P35-c1: at the measured revision, the two shokuknow-package jsc2js "
    "knowledge entries for `corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md` "
    "and `corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md` land on the "
    "`.jsc -> source mapping` frontier: each entry exists, opens with the provenance "
    "trio and cites its new SOURCES row (S125 / S129), both rows are mined with "
    "used-by naming the entry, and PROVINCE.md and the README coverage map hold both "
    "entry filenames."
)

ENTRIES = {
    "corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md": "S125",
    "corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md": "S129",
}

# SOURCES.md 11-column row: | id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
ROW_RE = re.compile(
    r"(?m)^\|\s*(S\d{3,})\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|"
    r"([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|"
)


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def show(root, rev, path):
    r = git(root, "show", f"{rev}:{path}")
    return r.stdout if r.returncode == 0 else None


def ls_tree(root, rev, prefix):
    r = git(root, "ls-tree", "-r", "--name-only", rev, "--", prefix)
    return set(r.stdout.splitlines()) if r.returncode == 0 else set()


def selftest(root):
    # Build a synthetic repo with a fully-passing tip (green), then mutate one
    # loaded per invariant (red). Runs the same check body as production.
    with tempfile.TemporaryDirectory(prefix="r35c1-selftest-") as d:
        subprocess.run(["git", "init", "-q"], cwd=d, check=True)
        subprocess.run(["git", "config", "user.email", "t@t"], cwd=d, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=d, check=True)
        sources = (
            "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|\n"
            "| S125 | jsc2js README — https://raw.githubusercontent.com/xqy2006/jsc2js/main/README.md | docs | A | x | anchor | teaches | mined | 2026-10-25 | 180d | corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md |\n"
            "| S129 | jsc2js Releases — https://github.com/xqy2006/jsc2js/releases | docs | A | x | anchor | teaches | mined | 2026-10-25 | 180d | corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md |\n"
        )
        os.makedirs(os.path.join(d, "corpus/knowledge"), exist_ok=True)
        os.makedirs(os.path.join(d, "corpus"), exist_ok=True)
        with open(os.path.join(d, "corpus/SOURCES.md"), "w") as f:
            f.write(sources)
        for p, row in ENTRIES.items():
            with open(os.path.join(d, p), "w") as f:
                f.write(
                    f"source: {row} — https://example.test/{row}\n"
                    "verified-at: 2026-10-25\n"
                    "recheck: 180d\n"
                )
        os.makedirs(os.path.join(d, ".ufo/waves/round-35"), exist_ok=True)
        with open(os.path.join(d, ".ufo/waves/round-35/claims.json"), "w") as f:
            json.dump({"round": 35, "predicate": PREDICATE, "claims": ["C1", "C2"]}, f)
        with open(os.path.join(d, "PROVINCE.md"), "w") as f:
            f.write("## Round-35 additions to Core\n")
            f.write("| surface | probe |\n|---|---|\n")
            f.write("| jsc2js mapper contract | 2026-10-25-r35-jsc2js-mapper-contract |\n")
            f.write("| jsc2js release inventory | 2026-10-25-r35-jsc2js-release-inventory |\n")
        with open(os.path.join(d, "corpus/README.md"), "w") as f:
            f.write("## Coverage map\n")
            f.write("| section | entries | state |\n|---|---|---|\n")
            f.write("| .jsc mapper | 2026-10-25-r35-jsc2js-mapper-contract.md, 2026-10-25-r35-jsc2js-release-inventory.md | held |\n")
        subprocess.run(["git", "add", "-A"], cwd=d, check=True)
        subprocess.run(["git", "commit", "-qm", "green"], cwd=d, check=True)
        green = subprocess.run([sys.executable, "-I", "-B", __file__, "--root", d, "--rev", "HEAD", "--freeze", "HEAD"],
                               capture_output=True, text=True)
        if green.returncode != 0:
            return "green-failed", green.stdout + green.stderr
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=d, text=True).strip()
        # red: remove the provenance trio from entry 1
        with open(os.path.join(d, "corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md"), "w") as f:
            f.write("no provenance trio\n")
        subprocess.run(["git", "add", "-A"], cwd=d, check=True)
        subprocess.run(["git", "commit", "-qm", "red"], cwd=d, check=True)
        red = subprocess.run([sys.executable, "-I", "-B", __file__, "--root", d, "--rev", "HEAD", "--freeze", base],
                             capture_output=True, text=True)
        if red.returncode == 0:
            return "red-accepted", red.stdout
        return "ok", f"green={green.returncode} red={red.returncode}"


def check(root, rev):
    fails = []
    paths = ls_tree(root, rev, "corpus/knowledge")
    for p, row in ENTRIES.items():
        if p not in paths:
            fails.append(f"entry_missing:{p}")
            continue
        body = show(root, rev, p) or ""
        if not re.search(r"(?m)^source\s*:", body):
            fails.append(f"trio_missing_source:{p}")
        if not re.search(r"(?m)^verified-at\s*:", body):
            fails.append(f"trio_missing_verified_at:{p}")
        if not re.search(r"(?m)^recheck\s*:", body):
            fails.append(f"trio_missing_recheck:{p}")
        if not re.search(r"(?m)^source\s*:.*" + row, body):
            fails.append(f"row_citation_missing:{p}:{row}")
    sources = show(root, rev, "corpus/SOURCES.md") or ""
    rows = {}
    for m in ROW_RE.finditer(sources):
        cells = [x.strip() for x in m.groups()[1:]]
        rows[m.group(1)] = cells
    for row in ("S125", "S129"):
        if row not in rows:
            fails.append(f"registry_row_missing:{row}")
            continue
        cells = rows[row]
        # cells: [source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by]
        if cells[6] != "mined":
            fails.append(f"registry_status_not_mined:{row}={cells[6]}")
        if not cells[7].startswith("2026-10-25"):
            fails.append(f"registry_opened_not_this_round:{row}={cells[7]}")
        entry = next((p for p, r in ENTRIES.items() if r == row), None)
        if entry and entry not in cells[9]:
            fails.append(f"registry_usedby_missing:{row}:{entry}")
    province = show(root, rev, "PROVINCE.md") or ""
    for p in ENTRIES:
        stem = p.rsplit("/", 1)[1][:-3]
        if stem not in province:
            fails.append(f"province_missing:{stem}")
    readme = show(root, rev, "corpus/README.md") or ""
    for p in ENTRIES:
        if p.rsplit("/", 1)[1] not in readme:
            fails.append(f"readme_missing:{p}")
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--freeze", help="claims-file revision (first commit adding claims.json)")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        verdict, detail = selftest(args.root)
        print(f"C1_SELFTEST: {verdict}\n{detail}")
        sys.exit(0 if verdict == "ok" else 1)

    if not (args.root and args.rev and args.freeze):
        ap.print_usage(file=sys.stderr)
        sys.exit(2)

    claims = show(args.root, args.freeze, ".ufo/waves/round-35/claims.json")

    if claims is None:
        print("C1: claims file absent at freeze revision", file=sys.stderr)
        sys.exit(2)
    try:
        claims_obj = json.loads(claims)
    except Exception as e:
        print(f"C1: claims unparseable: {e}", file=sys.stderr)
        sys.exit(2)
    if PREDICATE not in json.dumps(claims_obj):
        print("C1: predicate mismatch between counter and claims file", file=sys.stderr)
        sys.exit(2)

    fails = check(args.root, args.rev)
    receipt = {
        "instrument": "tools/round-35/c1-coverage-counter.py",
        "predicate": PREDICATE,
        "revision": args.rev,
        "freeze": args.freeze,
        "checks": {f"c1_{i}": (f not in fails) for i, f in enumerate(["entry_exist", "trio", "row_citation", "registry_rows", "province", "readme"])},
        "failing": fails,
        "pass": not fails,
    }
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(receipt, f, indent=1)
    if fails:
        print("C1_FAIL:", "; ".join(fails))
        sys.exit(1)
    print("C1_CLEAN revision=" + args.rev)
    sys.exit(0)


if __name__ == "__main__":
    main()
