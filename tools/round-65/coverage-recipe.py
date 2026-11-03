#!/usr/bin/env python3
"""coverage-recipe.py - round-65 instrument (R65-C2, calibration, capability).

Round 64's SCORECARD closed with a named defect: "The old measurement A regex
accepts October-dated names only; it cannot measure these November/non-date-named
additions and is not reinterpreted as a current score."  The r1-era recipe A
(`SCORECARD.md`, "Measurement recipes") derives BOTH sides of the coverage
fraction from the same `2026-10-\\d{2}-` token filter: the population is
`files matching the date regex`, so a knowledge file whose name is not
October-dated disappears from numerator AND denominator and the recipe still
prints a perfect score.  On the round-65 base the tree holds 144 knowledge
files and the recipe assesses 142 of them: two round-64 entries
(`jsc-mapper-cli-contract`, `jsc-mapper-release-inventory`) are silently
outside the assessed population.

This instrument measures that mismatch, and the repaired recipe:

  --recipe date   the superseded r1-era filter, reproduced exactly
                  (`2026-10-\\d{2}-[a-z0-9-]+` tokens; population = files whose
                  stem matches the same regex).  `population_dropped` counts the
                  files the filter hides; it is a finding, never a clean score.
  --recipe stem   the repaired recipe: population = every `corpus/knowledge/*.md`
                  blob at the revision; a file is mapped when its stem appears
                  as a token in the `## Coverage map` section of
                  `corpus/README.md` (backticked spans, comma-split, with a
                  leading `knowledge/` and a trailing `.md` normalized away).

`mismatches = missing + dangling + population_dropped`, one number per run:

  missing             population files whose stem no map token names
  dangling            map tokens that CLAIM a knowledge entry (a `knowledge/`
                      prefix or a `YYYY-MM-DD-` date prefix) and resolve to no
                      file at the revision
  population_dropped  files the recipe's own filter keeps out of the population

Limit (stated, never claimed covered): a bare non-dated token in the section
cannot be distinguished from ordinary backticked prose, so the dangling half
only sees tokens that claim a path or a dated entry name.  A non-dated entry
that is missing from the map is still counted by the `missing` half.

Exit: 0 clean (`mismatches == 0`, `mapped > 0`); 1 any mismatch; 2
could-not-evaluate (no coverage-map section, no knowledge files, unknown
revision, failed git call).

--selftest runs the extractor, both recipes and the exit classes over in-memory
fixtures (no git, no writes outside an optional --json-out).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

TOOL = "tools/round-65/coverage-recipe.py"
DATE_TOKEN_RE = re.compile(r"^2026-10-\d{2}-[a-z0-9-]+$")
DATED_STEM_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
CLAIM_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}-[a-z0-9-]+|[a-z0-9][a-z0-9-]+)$")
SECTION_HEAD = "## Coverage map"


def map_section(readme: str) -> str | None:
    marker = "\n" + SECTION_HEAD + "\n"
    if marker not in readme:
        return None
    body = readme.split(marker, 1)[1]
    return body.split("\n## ", 1)[0]


def extract_tokens(section: str) -> list[dict]:
    """Backticked spans, comma-split; each token with its normalized form."""
    out = []
    for span in re.findall(r"`([^`]+)`", section):
        for part in span.split(","):
            raw = part.strip()
            if not raw:
                continue
            norm = re.sub(r"^knowledge/", "", raw)
            norm = re.sub(r"\.md$", "", norm)
            if not CLAIM_RE.match(norm):
                continue
            claimed = raw.startswith("knowledge/") or bool(DATED_STEM_RE.match(norm))
            out.append({"raw": raw, "norm": norm, "claimed": claimed})
    return out


def assess(files: list[str], section: str, recipe: str) -> dict:
    """files: knowledge-file stems at the revision. Returns the assessment dict."""
    tokens = extract_tokens(section)
    if recipe == "date":
        population = [f for f in files if DATE_TOKEN_RE.match(f)]
        token_set = {t["norm"] for t in tokens if DATE_TOKEN_RE.match(t["norm"])}
    elif recipe == "stem":
        population = list(files)
        token_set = {t["norm"] for t in tokens}
    else:
        raise ValueError(f"unknown recipe {recipe}")
    mapped = sorted(set(population) & token_set)
    missing = sorted(set(population) - token_set)
    claimed = {t["norm"] for t in tokens if t["claimed"]}
    dangling = sorted(claimed - set(files))
    dropped = len(files) - len(population)
    return {"recipe": recipe, "knowledge_files": len(files),
            "population": len(population), "mapped": len(mapped),
            "missing": missing, "dangling": dangling,
            "population_dropped": dropped,
            "mismatches": len(missing) + len(dangling) + dropped}


def exit_class(result: dict) -> int:
    if result["mapped"] == 0 and result["population"] == 0:
        return 2
    return 0 if result["mismatches"] == 0 and result["mapped"] > 0 else 1


def git(root: str, *argv: str) -> str:
    return subprocess.check_output(["git", "-C", root, *argv], text=True)


def read_inputs(root: str, rev: str) -> tuple[list[str], str]:
    paths = git(root, "ls-tree", "-r", "--name-only", rev, "--", "corpus/knowledge").splitlines()
    stems = []
    for p in paths:
        if p.endswith(".md"):
            stems.append(p.rsplit("/", 1)[-1][:-3])
    readme = git(root, "show", f"{rev}:corpus/README.md")
    return stems, readme


def selftest() -> int:
    cases = []

    def check(name, got, want):
        cases.append((name, got == want, got, want))

    map_text = """
## Coverage map

| section | entries | state |
|---|---|---|
| a | `2026-10-01-alpha`, `2026-10-02-beta` | held |
| b | `knowledge/2026-10-03-gamma` | held |
| c | `jsc-mapper-cli-contract`, `jsc-mapper-release-inventory` | held |
"""
    files = ["2026-10-01-alpha", "2026-10-02-beta", "2026-10-03-gamma",
             "jsc-mapper-cli-contract", "jsc-mapper-release-inventory"]
    sec = map_section("\n" + map_text.lstrip("\n"))
    check("section-found", sec is not None, True)
    check("section-absent", map_section("# nothing\n"), None)
    toks = extract_tokens(sec)
    check("token-count", len(toks), 5)
    check("token-normalized", sorted(t["norm"] for t in toks),
          sorted(files))
    check("token-claimed-date", toks[0]["claimed"], True)
    check("token-claimed-plain", [t["claimed"] for t in toks if t["norm"] == "jsc-mapper-cli-contract"], [False])

    r = assess(files, sec, "stem")
    check("stem-mapped", r["mapped"], 5)
    check("stem-missing", r["missing"], [])
    check("stem-dangling", r["dangling"], [])
    check("stem-mismatches", r["mismatches"], 0)
    check("stem-exit", exit_class(r), 0)

    d = assess(files, sec, "date")
    check("date-population", d["population"], 3)
    check("date-dropped", d["population_dropped"], 2)
    check("date-mismatches", d["mismatches"], 2)
    check("date-exit", exit_class(d), 1)

    one_out = assess(files + ["2026-10-04-delta"], sec, "stem")
    check("stem-one-missing", one_out["missing"], ["2026-10-04-delta"])
    check("stem-one-missing-count", one_out["mismatches"], 1)
    check("missing-no-dangling", one_out["dangling"], [])
    removed_dated = assess(files[1:], sec, "stem")
    check("removed-dated-dangles", removed_dated["dangling"], ["2026-10-01-alpha"])
    # stated limit: a removed non-dated entry leaves a bare map token the
    # dangling half cannot distinguish from prose; the file is gone from the
    # population too, so this recipe reports it clean.  Named, never claimed covered.
    limit = assess(files[:-1], sec, "stem")
    check("limit-nondated-removal-clean", (limit["mismatches"], exit_class(limit)), (0, 0))

    dangling_map = map_text + "| d | `knowledge/2026-10-09-ghost` | held |\n"
    dm = map_section("\n" + dangling_map.lstrip("\n"))
    dd = assess(files, dm, "stem")
    check("stem-dangling-named", dd["dangling"], ["2026-10-09-ghost"])
    check("stem-dangling-count", dd["mismatches"], 1)
    check("stem-dangling-exit", exit_class(dd), 1)

    empty = assess([], sec, "stem")
    check("empty-exit", exit_class(empty), 2)
    nomap = assess(files, "| x |\n", "stem")
    check("nomap-exit", exit_class(nomap), 1)
    check("nomap-unmapped", len(nomap["missing"]), 5)

    # the r65 base itself: the date recipe drops the two November names
    base_files = ["2026-10-31-seventeen", "2026-10-30-sixteen",
                  "jsc-mapper-cli-contract", "jsc-mapper-release-inventory"]
    base_map = map_section(
        "\n## Coverage map\n| x | `2026-10-31-seventeen`, `2026-10-30-sixteen`, "
        "`jsc-mapper-cli-contract`, `jsc-mapper-release-inventory` | held |\n")
    bd = assess(base_files, base_map, "date")
    check("base-date-reproduces", (bd["mapped"], bd["population"], bd["mismatches"]), (2, 2, 2))
    bs = assess(base_files, base_map, "stem")
    check("base-stem-clean", (bs["mapped"], bs["mismatches"], exit_class(bs)), (4, 0, 0))

    failures = [c for c in cases if not c[1]]
    for name, ok, got, want in cases:
        print(f"{'PASS' if ok else 'FAIL'} {name} got={got!r} want={want!r}")
    print(f"SELFTEST {'CLEAN' if not failures else 'FAILED'} "
          f"cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev", help="revision to measure (required for a run)")
    ap.add_argument("--recipe", choices=("stem", "date"), default="stem")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.rev:
        ap.error("missing: --rev")
    try:
        files, readme = read_inputs(args.root, args.rev)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"{TOOL}: could not read inputs: {exc}", file=sys.stderr)
        return 2
    section = map_section(readme)
    if section is None:
        print(f"{TOOL}: no '{SECTION_HEAD}' section at {args.rev}", file=sys.stderr)
        return 2
    result = {"tool": TOOL, "rev": args.rev, **assess(files, section, args.recipe)}
    result["exit"] = exit_class(result)
    text = json.dumps(result, indent=1, sort_keys=True) + "\n"
    if args.out:
        from pathlib import Path
        Path(args.out).write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return result["exit"]


if __name__ == "__main__":
    sys.exit(main())
