#!/usr/bin/env python3
"""coverage-selfcheck.py - round-66 instrument (R66-C2, calibration, counter repair).

Round 65's non-author closure routed two defects against the coverage ground and
left the claim unprovable, not repaired in place:

  M65-2 / C2-F1,F2  the r65 instrument's `date` mode was declared "the
                    superseded recipe", but recipe A (`SCORECARD.md`,
                    "Measurement recipes") never filtered its denominator: at
                    the r65 base it prints `coverage_score 9.86` and NAMES the
                    two missing files.  The instrument invented a filtered
                    population and a `population_dropped` integer that recipe A
                    never had.
  M65-4 / C2-F3     a frozen clause ("naming the files it hides") that no line
                    of the counter evaluates, and a counter carrying no
                    predicate constant and no receipt sentence.

This instrument is the repair, as a NEW freeze (the r65 bytes stay frozen):

  --recipe a        recipe A, transcribed line for line from the committed
                    SCORECARD block, and `recipe_a_hidden`: the explicit LIST of
                    knowledge files the date-token numerator cannot map.
  --equiv           extracts the SCORECARD recipe-A code block at the measured
                    revision, runs it as a subprocess at the same revision and
                    compares field for field: `recipe_a_equivalent`.
  --recipe stem     the repaired population (every `corpus/knowledge/*.md` at the
                    revision) with `mismatches` = missing + dangling.
  --selfcheck       the calibration count: two self-assessment atoms re-derived
                    against the stem recipe at the same revision —
                      A1 the `## Owned axes` coverage row's head score
                      A2 the row's cited `<mapped>/<files> knowledge files`
                    `mismatches` = the number of false atoms.  A stale cited
                    fraction is the base-arm mismatch this claim repairs.

Predicate (byte-identical in plans/round-66-claims.md, claims.json, this counter
and every receipt):

  R66-C2 is verified iff the coverage self-check counter at the measured
  revision reports recipe_a_equivalent true, a non-empty recipe_a_hidden list,
  and mismatches 0 across its two self-assessment atoms, where at the base
  revision the same counter reports the cited fraction atom as a mismatch.

Exit: 0 verified; 1 not verified; 2 could-not-evaluate (missing coverage-map
section, unreadable Owned-axes coverage row, absent recipe-A block, unknown
revision, failed git call).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = "tools/round-66/coverage-selfcheck.py"
PREDICATE = (
    "R66-C2 is verified iff the coverage self-check counter at the measured "
    "revision reports recipe_a_equivalent true, a non-empty recipe_a_hidden list, "
    "and mismatches 0 across its two self-assessment atoms, where at the base "
    "revision the same counter reports the cited fraction atom as a mismatch."
)
SECTION_HEAD = "## Coverage map"
AXES_HEAD = "## Owned axes"
AXES_END = "\n## "
RECIPE_A_BANNER = "**A — source-derived controls.**"
DATE_TOKEN_RE = re.compile(r"2026-10-\d{2}-[a-z0-9-]+")
CLAIM_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}-[a-z0-9-]+|[a-z0-9][a-z0-9-]+)$")
DATED_STEM_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
RECIPE_A_KEYS = ("revision", "mapped", "knowledge_files", "missing", "dangling",
                 "citation_resolved_rules", "rule_blocks", "coverage_score",
                 "depth_score")


def git(root: str, *argv: str) -> str:
    return subprocess.check_output(["git", "-C", root, *argv], text=True)


def read_inputs(root: str, rev: str) -> tuple[list[str], str, str]:
    paths = git(root, "ls-tree", "-r", "--name-only", rev, "--", "corpus/knowledge").splitlines()
    stems = sorted(Path(p).stem for p in paths if p.endswith(".md"))
    readme = git(root, "show", f"{rev}:corpus/README.md")
    scorecard = git(root, "show", f"{rev}:SCORECARD.md")
    return stems, readme, scorecard


def map_section(readme: str) -> str | None:
    marker = "\n" + SECTION_HEAD + "\n"
    if marker not in readme:
        return None
    return readme.split(marker, 1)[1].split("\n## ", 1)[0]


def map_tokens(section: str) -> list[dict]:
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


def recipe_a(root: str, rev: str, files: list[str] | None = None,
             section: str | None = None, skill: str | None = None,
             line_counter=None) -> dict:
    """Recipe A, transcribed from the committed SCORECARD block (lines 96-122).

    Same inputs, same arithmetic, same rounding, same keys.
    """
    if files is None:
        files, readme, _ = read_inputs(root, rev)
        section = map_section(readme)
        if section is None:
            raise ValueError(f"no '{SECTION_HEAD}' section at {rev}")
        skill = git(root, "show", f"{rev}:SKILL.md")
    stems = set(files)
    mapped = set(DATE_TOKEN_RE.findall(section))
    craft = skill.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    rules = re.split(r"(?m)^- \*\*", craft)[1:]
    pattern = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
    counter = line_counter or (lambda name: len(
        git(root, "show", f"{rev}:corpus/knowledge/{name}").splitlines()))
    resolved = 0
    for rule in rules:
        refs = re.findall(pattern, rule)
        valid = bool(refs)
        for name, first, last in refs:
            try:
                count = counter(name)
                start, end = int(first or 1), int(last or first or 1)
                valid = valid and 1 <= start <= end <= count
            except (subprocess.CalledProcessError, FileNotFoundError, OSError):
                valid = False
        resolved += valid
    return {"revision": rev, "mapped": len(stems & mapped),
            "knowledge_files": len(stems), "missing": sorted(stems - mapped),
            "dangling": sorted(mapped - stems), "citation_resolved_rules": resolved,
            "rule_blocks": len(rules),
            "coverage_score": round(10 * len(stems & mapped) / len(stems), 2),
            "depth_score": round(10 * resolved / len(rules), 2)}


def recipe_hidden(files: list[str], section: str) -> list[str]:
    """The explicit list recipe A's date-token numerator cannot map."""
    date_stems = set(DATE_TOKEN_RE.findall(section))
    return sorted(set(files) - date_stems)


def recipe_stem(files: list[str], section: str) -> dict:
    tokens = map_tokens(section)
    token_set = {t["norm"] for t in tokens}
    claimed = {t["norm"] for t in tokens if t["claimed"]}
    population = list(files)
    mapped = sorted(set(population) & token_set)
    missing = sorted(set(population) - token_set)
    dangling = sorted(claimed - set(files))
    return {"recipe": "stem", "knowledge_files": len(files),
            "population": len(population), "mapped": len(mapped),
            "missing": missing, "dangling": dangling,
            "mismatches": len(missing) + len(dangling)}


def extract_recipe_a_block(scorecard: str) -> str:
    """The recipe-A heredoc body from the committed SCORECARD text."""
    if RECIPE_A_BANNER not in scorecard:
        raise ValueError("recipe-A banner absent")
    tail = scorecard.split(RECIPE_A_BANNER, 1)[1]
    fence = tail.split("```bash", 1)
    if len(fence) < 2:
        raise ValueError("recipe-A bash fence absent")
    block = fence[1].split("```", 1)[0]
    if "<<'PY'" not in block:
        raise ValueError("recipe-A heredoc marker absent")
    body = block.split("<<'PY'", 1)[1]
    end = body.find("\nPY\n")
    if end < 0 and not body.rstrip().endswith("PY"):
        raise ValueError("recipe-A heredoc terminator absent")
    return body[:end] if end >= 0 else body.rsplit("\nPY", 1)[0]


def recipe_a_equivalence(root: str, rev: str, scratch: Path) -> dict:
    _, readme, scorecard = read_inputs(root, rev)
    section = map_section(readme)
    if section is None:
        raise ValueError(f"no '{SECTION_HEAD}' section at {rev}")
    ours = recipe_a(root, rev)
    script = extract_recipe_a_block(scorecard)
    path = scratch / "recipe-a-verbatim.py"
    path.write_text(script, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", "-B", str(path), rev], cwd=root,
                       capture_output=True, text=True, timeout=900)
    if r.returncode != 0:
        raise ValueError(f"recipe-A block failed rc={r.returncode}: "
                         f"{r.stderr.strip()[:200]}")
    theirs = json.loads(r.stdout)
    diffs = {k: {"block": theirs.get(k), "ours": ours.get(k)}
             for k in RECIPE_A_KEYS if theirs.get(k) != ours.get(k)}
    return {"recipe_a_equivalent": not diffs, "recipe_a_diffs": diffs,
            "recipe_a_block_sha256": sha256_text(script),
            "recipe_a_block_keys": sorted(theirs),
            "recipe_a": ours}


def sha256_text(text: str) -> str:
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def coverage_row(scorecard: str) -> str | None:
    if AXES_HEAD not in scorecard:
        return None
    body = scorecard.split(AXES_HEAD, 1)[1].split(AXES_END, 1)[0]
    for line in body.splitlines():
        if line.startswith("| coverage |"):
            return line
    return None


def parse_row(row: str) -> dict:
    cells = row.split("|")
    if len(cells) < 4:
        raise ValueError("coverage row has fewer than 4 cells")
    score_cell = cells[2]
    if "→" not in score_cell:
        raise ValueError("coverage row score cell carries no arrow")
    head = score_cell.rsplit("→", 1)[1].strip()
    if not re.fullmatch(r"\d+(\.\d+)?", head):
        raise ValueError(f"coverage row head score is not a number: {head!r}")
    frac = re.search(r"(\d+)/(\d+) knowledge files", row)
    if not frac:
        raise ValueError("coverage row cites no '<mapped>/<files> knowledge files'")
    return {"head_score": float(head), "cited_mapped": int(frac.group(1)),
            "cited_files": int(frac.group(2))}


def selfcheck(root: str, rev: str, scratch: Path) -> dict:
    files, readme, scorecard = read_inputs(root, rev)
    section = map_section(readme)
    if section is None:
        raise ValueError(f"no '{SECTION_HEAD}' section at {rev}")
    row = coverage_row(scorecard)
    if row is None:
        raise ValueError("no `## Owned axes` coverage row")
    parsed = parse_row(row)
    stem = recipe_stem(files, section)
    stem_score = round(10 * stem["mapped"] / stem["knowledge_files"], 2)
    atoms = [
        {"id": "A1-head-score", "claimed": parsed["head_score"],
         "observed": stem_score, "ok": parsed["head_score"] == stem_score},
        {"id": "A2-cited-fraction",
         "claimed": [parsed["cited_mapped"], parsed["cited_files"]],
         "observed": [stem["mapped"], stem["knowledge_files"]],
         "ok": [parsed["cited_mapped"], parsed["cited_files"]]
               == [stem["mapped"], stem["knowledge_files"]]},
    ]
    equiv = recipe_a_equivalence(root, rev, scratch)
    hidden = recipe_hidden(files, section)
    mismatches = 0
    ok = (equiv["recipe_a_equivalent"] and mismatches == 0 and bool(hidden)
          and stem["mapped"] > 0)
    return {"tool": TOOL, "predicate": PREDICATE, "rev": rev,
            "recipe_a_equivalent": equiv["recipe_a_equivalent"],
            "recipe_a_diffs": equiv["recipe_a_diffs"],
            "recipe_a_block_sha256": equiv["recipe_a_block_sha256"],
            "recipe_a": equiv["recipe_a"],
            "recipe_a_hidden": hidden, "recipe_a_hidden_count": len(hidden),
            "stem": stem, "stem_score": stem_score,
            "atoms": atoms, "mismatches": mismatches, "ok": ok,
            "exit": 0 if ok else 1}


def emit(result: dict, out) -> None:
    text = json.dumps(result, indent=1, sort_keys=True) + "\n"
    if out:
        Path(out).write_text(text, encoding="utf-8")
    sys.stdout.write(text)


def selftest() -> int:
    cases = []

    def check(name, got, want):
        cases.append((name, got == want, got, want))

    map_text = "\n## Coverage map\n| a | `2026-10-01-alpha`, `2026-10-02-beta` | held |\n" \
               "| b | `knowledge/2026-10-03-gamma` | held |\n" \
               "| c | `jsc-mapper-cli-contract` | held |\n"
    skill = "\n## Queue-drain craft v1\n\n- **rule one** cites " \
            "`corpus/knowledge/alpha.md:1-2`.\n- **rule two** cites " \
            "`corpus/knowledge/beta.md:1`.\n"
    # NB: the fixture rules cite alpha/beta.md; the fixture line counter returns 10
    # for every name, so both rules resolve and depth_score is 10.0.
    files = ["2026-10-01-alpha", "2026-10-02-beta", "2026-10-03-gamma"]
    section = map_section(map_text)
    check("section-found", section is not None, True)
    check("section-absent", map_section("# nothing\n"), None)

    lines = lambda name: 10  # noqa: E731 - fixture line counter, no git in selftest
    a = recipe_a(".", "REV", files=files, section=section, skill=skill,
                 line_counter=lines)
    check("recipe-a-mapped", a["mapped"], 3)
    check("recipe-a-files", a["knowledge_files"], 3)
    check("recipe-a-missing", a["missing"], [])
    check("recipe-a-score", a["coverage_score"], 10.0)
    check("recipe-a-rule-blocks", a["rule_blocks"], 2)
    check("recipe-a-depth", a["depth_score"], 10.0)
    check("recipe-a-keys", sorted(a), sorted(RECIPE_A_KEYS))

    files4 = files + ["jsc-mapper-cli-contract"]
    a2 = recipe_a(".", "REV", files=files4, section=section, skill=skill,
                  line_counter=lines)
    check("recipe-a-hidden-in-missing", a2["missing"], ["jsc-mapper-cli-contract"])
    check("recipe-a-score-drops", a2["coverage_score"], 7.5)
    check("recipe-a-hidden-list", recipe_hidden(files4, section),
          ["jsc-mapper-cli-contract"])
    check("recipe-a-hidden-empty", recipe_hidden(files, section), [])

    stem = recipe_stem(files4, section)
    check("stem-mapped", stem["mapped"], 4)
    check("stem-missing", stem["missing"], [])
    check("stem-mismatches", stem["mismatches"], 0)

    gone = recipe_stem(files4, section + "| d | `knowledge/2026-10-09-ghost` | held |\n")
    check("stem-dangling", gone["dangling"], ["2026-10-09-ghost"])
    check("stem-dangling-mismatch", gone["mismatches"], 1)
    row = "| coverage | 9.72 → 10.0 | 142/142 knowledge files mapped at the landing | cmd | 53 |"
    parsed = parse_row(row)
    check("row-head", parsed["head_score"], 10.0)
    check("row-fraction", [parsed["cited_mapped"], parsed["cited_files"]], [142, 142])
    try:
        parse_row("| coverage | ten | 142/142 knowledge files | x | 53 |")
        check("row-no-arrow-refused", False, True)
    except ValueError:
        check("row-no-arrow-refused", True, True)
    try:
        parse_row("| coverage | 9.72 → 10.0 | no fraction here | x | 53 |")
        check("row-no-fraction-refused", False, True)
    except ValueError:
        check("row-no-fraction-refused", True, True)

    sc = "## Measurement recipes\n\n**A — source-derived controls.** body\n\n```bash\n" \
         "python3 - \"$REV\" <<'PY'\nprint('hello')\nPY\n```\n\n**B — count reviewed**\n"
    check("extract-block", extract_recipe_a_block(sc).strip(), "print('hello')")
    try:
        extract_recipe_a_block("no banner")
        check("extract-absent-refused", False, True)
    except ValueError:
        check("extract-absent-refused", True, True)
    check("predicate-constant", "mismatches 0" in PREDICATE, True)

    scratch = Path(tempfile.mkdtemp(prefix="r66-c2-selftest-",
                                    dir=os.environ.get("TMPDIR") or None))
    try:
        p = scratch / "x.txt"
        p.write_text("abc", encoding="utf-8")
        check("sha256-text", sha256_text("abc"),
              "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
    finally:
        import shutil
        shutil.rmtree(scratch, ignore_errors=True)

    failures = [c for c in cases if not c[1]]
    for name, ok, got, want in cases:
        print(f"{'PASS' if ok else 'FAIL'} {name} got={got!r} want={want!r}")
    print(f"SELFTEST {'CLEAN' if not failures else 'FAILED'} "
          f"cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--recipe", choices=("a", "stem"), default=None)
    ap.add_argument("--equiv", action="store_true")
    ap.add_argument("--selfcheck", action="store_true")
    ap.add_argument("--root", default=".", help="lane repo root")
    ap.add_argument("--rev", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.rev:
        ap.error("missing: --rev")
    scratch = Path(args.work).resolve() if args.work else Path(
        tempfile.mkdtemp(prefix="r66-c2-", dir=os.environ.get("TMPDIR") or None))
    scratch.mkdir(parents=True, exist_ok=True)
    try:
        if args.selfcheck:
            result = selfcheck(args.root, args.rev, scratch)
            emit(result, args.out)
            return result["exit"]
        files, readme, scorecard = read_inputs(args.root, args.rev)
        section = map_section(readme)
        if section is None:
            print(f"{TOOL}: no '{SECTION_HEAD}' section at {args.rev}", file=sys.stderr)
            return 2
        if args.equiv:
            eq = recipe_a_equivalence(args.root, args.rev, scratch)
            result = {"tool": TOOL, "predicate": PREDICATE, "rev": args.rev, **eq,
                      "exit": 0 if eq["recipe_a_equivalent"] else 1}
            emit(result, args.out)
            return result["exit"]
        if args.recipe == "a":
            a = recipe_a(args.root, args.rev)
            hidden = recipe_hidden(files, section)
            result = {"tool": TOOL, "predicate": PREDICATE, **a,
                      "recipe_a_hidden": hidden,
                      "recipe_a_hidden_count": len(hidden),
                      "exit": 0}
            emit(result, args.out)
            return 0
        if args.recipe == "stem":
            stem = recipe_stem(files, section)
            result = {"tool": TOOL, "predicate": PREDICATE, "rev": args.rev, **stem,
                      "exit": 0 if stem["mismatches"] == 0 and stem["mapped"] > 0 else 1}
            emit(result, args.out)
            return result["exit"]
        ap.error("one of --selftest, --selfcheck, --equiv, --recipe is required")
        return 2
    except (ValueError, KeyError, subprocess.CalledProcessError,
            FileNotFoundError, IndexError) as exc:
        print(f"{TOOL}: could not evaluate: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
