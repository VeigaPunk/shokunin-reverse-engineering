# RV-2 — C3 instrument coverage of appended Frontier bullets

## Finding and re-derived facts

**Claim:** G21 can silently pass a newly appended Markdown bullet beyond its final registered span. Proposed fix: have the G21 check find Markdown bullets inside headings whose text contains `frontier`, and flag any such bullet outside every `FRONTIER[]` span. This is patch text only; the instrument was not edited.

- **VERIFIED — checkout identity:** `git rev-parse HEAD` returned `5694506a862c32d2f7aac44935778bce4b6184f2`. The gate was not listed as modified by the initial `git status --short`.
- **VERIFIED — live G21 boundary:** `.ufo/gates/c1-census-v10.py:292-308` declares 14 `FRONTIER` rows; the last is `("PROVINCE.md", 161, 162, ...)`. The source check at `:422-444` checks only those fixed spans (`lines[s - 1:e]`) and returns the accumulated errors. The corresponding current Frontier content ends at `PROVINCE.md:162` (the two Frontier sections are at `:73-93` and `:133-162`). The main path calls the check at gate `:633`; any errors become `FRONTIER-UNEVALUABLE` at `:667-672` and force FAIL.
- **VERIFIED — gate identity:** `sha256sum .ufo/gates/c1-census-v10.py` returned `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`.

## Measurements

**REPRODUCED — ordinary gate run at checkout:**

Command: `python3 .ufo/gates/c1-census-v10.py --quiet` (exit 0).

```text
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1924 loci=11
SKILL.md       lines=413  loci=2

SCOPE-ERRORS (marker assertions): []
FRONTIER register (G21): 14 rows asserted, errors: []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=20, SCORECARD.md=18, SKILL.md=3; total loci=19; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

**REPRODUCED — seeded fail-open at HEAD:** copied `PROVINCE.md`, `SKILL.md`, and `SCORECARD.md` to `/var/tmp/kaidoku-rv2.00iuGt/root/`, then appended this new bullet to the scratch `PROVINCE.md` (it landed on line 164, after a blank line):

```text
- **RV-2 seeded frontier claim**: unregistered text beyond the G21 bound.
```

Command: `python3 .ufo/gates/c1-census-v10.py --root /var/tmp/kaidoku-rv2.00iuGt/root --quiet` (exit 0). It reported `PROVINCE.md lines=164`, `FRONTIER register (G21): 14 rows asserted, errors: []`, `DECLARED FAIL CLASSES: []`, and `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`. Thus the stated silent-pass gap is present.

## Proposed patch text (tested on a scratch copy only)

Insert below the existing `FRONTIER` row loop and before `return errs` in `frontier_check` (`.ufo/gates/c1-census-v10.py:422-444`):

```python
    lines = filelines.get("PROVINCE.md")
    if lines:
        in_frontier = False
        for n, line in enumerate(lines, 1):
            heading = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
            if heading:
                in_frontier = bool(re.search(r"\bfrontier\b", heading.group(1), re.I))
                continue
            if in_frontier and re.match(r"^\s*[-*+]\s+", line):
                covered = any(f == "PROVINCE.md" and s <= n <= e
                              for f, s, e, _, _ in FRONTIER)
                if not covered:
                    errs.append("PROVINCE.md:%d unregistered Frontier bullet (G21)" % n)
```

The existing `main` maps any such error to the declared `FRONTIER-UNEVALUABLE` class and fails the verdict. No scope range or existing positive/negative G21 anchor was changed.

**REPRODUCED — scratch candidate verification:** copied the gate to `/var/tmp/kaidoku-rv2.00iuGt/c1-census-v10-candidate.py`, applied exactly the insertion above to that copy, and ran `python3 -m py_compile` successfully. Then ran the candidate with `--json` on both the clean scratch copy and the seeded scratch root:

```text
clean rc=0 verdict=PASS frontier_rows=14 frontier_errors=[] declared_fail_classes=[] lines=162
seeded rc=1 verdict=FAIL frontier_rows=14 frontier_errors=['PROVINCE.md:164 unregistered Frontier bullet (G21)'] declared_fail_classes=['FRONTIER-UNEVALUABLE'] lines=164
```

## Limits

This closes the measured append-past-the-last-span case for unordered Markdown bullets inside headings containing `frontier`; it does not claim to detect unregistered prose that is not a bullet, an additional bullet placed inside an already-covered span, or a renamed Frontier heading. The candidate and scratch trees are measurements, not landed instrument changes.