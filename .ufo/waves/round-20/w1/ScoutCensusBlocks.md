# ScoutCensusBlocks — round-20 advisory (C1/D4, D5) — 2026-10-20

Scope: read-only. Baseline measured throughout = `14f0260ad319ecc26994381b2415d5a999003375`
(observed: `git rev-parse refs/heads/main` = `d1d981d2cc041dda4656c5b01d2c8445d8d17124` at
observation time, i.e. the lane tip has moved past the baseline; baseline existence verified:
`git rev-list -1 14f0260…` exit 0). Every lane file was read via
`git --no-optional-locks show 14f0260…:<path>`; the census and the candidate-declaration
harness ran on a `git archive` export under `mktemp -d` (no lane write, no `jj`, no git write).
Tools installed/upgraded: none.

## 1. Exact text at the baseline (observation)

`SCORECARD.md:2380-2382` (verbatim; `cat -A` shows no trailing whitespace, no hidden bytes):

```
- The capture reads REA 6.5.0's private, undocumented session directory.
  REA 6.7.0 adds no keep-log knob (w2 `ScoutReaLogKnob`). Re-check on every
  REA/Ghidra release.
```

`SKILL.md:511-519` (verbatim):

```
`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` (S003/S023/S024/
S025/S026/S029/S031/S032) runs real, pinned Go carriers through REA 6.5.0
`analyze` with the Ghidra analyzer log retained and bound to the run. It
compares each log against a route predicted from installed source and frozen
in Git before the measured runs. Scope: Ghidra 12.1.4, x86-64 Linux ELF, two
passes per carrier. 8/8 routes matched in both passes. Of the six prospective
carriers, three were on routes unseen at freeze (1.25.x fallback, no build
info) and three repeated pilot-seen routes. Use it before attributing Go
symbol loss to a layout change.
```

Both are folded units under `.ufo/gates/c1-census-v10.py:342-357` (`units()`): a bullet absorbs
its indented continuation lines, so SCORECARD yields block `2380-2382`; SKILL's blank-line-free
paragraph yields block `511-519`. Headings: `SCORECARD.md:2350` `## Round 17 — retained Go carrier
diagnostics and routed r16 defects, 2026-10-20`, `:2370` `### Capability addition (demonstrated
before this row)`; `SKILL.md:509` `## Retained Go carrier diagnostics — round 17`.

Provenance (observation, `git blame` at baseline): SCORECARD 2370-2392 all from
`8e7642c` (2026-10-20T11:49:41-03:00, "round-17: measured records, scorecard capability row,
lesson evidence"); SKILL 511 from `da64646`, 512-519 from `d0ab299` (2026-10-20T11:47:24-03:00,
"round-17: w2 integration…"). All three are ancestors of the baseline (`merge-base --is-ancestor`
exit 0 each). The capability row `:2374` ends with `round-17` in its *First-working round* cell.

## 2. SCOPE table and classify() rules (observation, `.ufo/gates/c1-census-v10.py`)

SCOPE, verbatim `:253-277` (line numbers 1-based, inclusive; `scope_of()` `:400-404` returns the
**first** matching row, `None` otherwise):

```python
SCOPE = [
    ("PROVINCE.md", 8, 13, "CURRENT", None, None),
    ("PROVINCE.md", 15, 26, "CURRENT", None, None),
    ("PROVINCE.md", 40, 43, "DATED", 40, r"verified on this host 2026-10-13"),
    ("PROVINCE.md", 44, 44, "CURRENT", None, None),
    ("PROVINCE.md", 45, 62, "DATED", 45, r"2026-10-13"),
    ("PROVINCE.md", 64, 71, "CURRENT", None, None),
    ("PROVINCE.md", 119, 131, "DATED", 119, r"verified 2026-10-13"),
    ("SKILL.md", 10, 16, "CURRENT", None, None),
    ("SKILL.md", 18, 20, "CURRENT", None, None),
    ("SCORECARD.md", 56, 60, "CURRENT", None, None),
    ("SCORECARD.md", 273, 326, "DATED", 273, r"2026-10-16"),
    ("SCORECARD.md", 417, 466, "DATED", 417, r"2026-10-16"),
    ("SCORECARD.md", 467, 502, "DATED", 467, r"2026-10-16"),
    ("SCORECARD.md", 503, 533, "DATED", 503, r"2026-10-16"),
    ("SCORECARD.md", 534, 560, "DATED", 534, r"2026-10-16"),
    ("SCORECARD.md", 619, 619, "DATED", 619, r"luna-round-\d"),
    ("SCORECARD.md", 620, 620, "DATED", 620, r"luna-round-\d"),
    ("SCORECARD.md", 636, 702, "DATED", 636, r"2026-10-18"),

    ("SCORECARD.md", 703, 768, "DATED", 704, r"arc2-loop1-round2"),
    ("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3"),
    ("SCORECARD.md", 1759, 2122, "DATED", 1759, r"arc3-loop1-round7"),
]
```

Highest declared end per file: PROVINCE.md 131 (162 via FRONTIER `:292-308`), SKILL.md 20,
SCORECARD.md 2122. The two blocks sit **past every declared end**, which is exactly D4.

Rules that produce this failure, quoted from the instrument:

- Layers `:128-144`: SCOPE classes are only `CURRENT` ("live state, must be reconciled") and
  `DATED` ("record of a past verification, historical by construction"); a locus inside no
  declared range is UNDECLARED and fails the run.
- Needles `:315-318`: `PIN = rea-agents@(\d+\.\d+\.\d+)`, `VER = (?<![\d.])6\.\d+\.\d+`,
  `PTR = ((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)`; `REA_GATE` `:319` admits `\brea\b`.
- Client vocabulary `:246-251`: `PATH_TOKENS`/`NAME_TOKENS` cover devin/omp/kimi — **`REA` is not
  a client token**, so "REA 6.5.0" can never attribute to a client surface.
- `classify()` `:527-541`: a unit is graded only if `REA_GATE` matches and it holds ≥1 of
  pin/bare/ptr; `bare` spans are de-duplicated against pin spans `:534-537`.
- `:543-559`: physical line via `line_of()`, `scope_of()` on that line, clause bounds, then
  `nearest_client()`; for `bare`, `target = clients or [None]`.
- `:571-583` (the decisive branch): with `c is None`, `DATED` → `historical (dated scope)`;
  inline marker → `historical`; G17 keywords (`doctor|expects|skill|reports|aligned|stale`) →
  version-intrinsic cache check; **else `AMBIGUOUS`, "no client token in clause"**.
- `:591-595` G16: a historical value equal to any live anchor is promoted `current-ok`.
- `:600-602`: `if any(d["scope"] is None and d["disp"] != "historical")` → block `UNDECLARED`.
- `:615`: G11 — block `current-ok` with no `RECEIPT` language (`:321`) is a finding.
- `:697-699`: PASS iff stale, ambiguous, undeclared, unresolved, scope_errors, g11 all empty and
  G2/anchor/frontier hold.

## 3. Census run at the baseline (observation)

Command (lane read-only; export under mkdtemp):

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && TMPD=$(mktemp -d /tmp/kr20-censusblocks-XXXXXX) \
 && git --no-optional-locks archive 14f0260ad319ecc26994381b2415d5a999003375 | tar -x -C "$TMPD" \
 && python3 -I -B "$TMPD/.ufo/gates/c1-census-v10.py" --root "$TMPD" >"$TMPD/census.out" 2>"$TMPD/census.err"
```

`archive_exit=0`, `CENSUS_EXIT=1` (stderr empty). Output counts and the UNDECLARED section, verbatim:

```
live anchors (re-derived): {'devin': '6.7.0', 'omp': '6.7.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=2567 loci=13
SKILL.md       lines=623  loci=3

-- UNDECLARED (2) --
  SCORECARD.md block 2380-2382 [scope None]
      :2380 [bare] None=6.5.0 -> AMBIGUOUS (no client token in clause)
      :2381 [bare] None=6.7.0 -> AMBIGUOUS (no client token in clause)
  SKILL.md block 511-519 [scope None]
      :512 [bare] None=6.5.0 -> AMBIGUOUS (no client token in clause)

SCOPE-ERRORS (marker assertions): []
FRONTIER register (G21): 14 rows asserted, errors: []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=16, SCORECARD.md=12, SKILL.md=3; total loci=22; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)
```

## 4. Proposed true scope class (inference from the observed text + measured declarations)

Both blocks are **DATED**: each is a record of a past verification round, not live state.
Support: round-17 headings (`SCORECARD.md:2350`, `SKILL.md:509`); the SCORECARD bullet is one of
the six `Limits:` of the capability row whose *First-working round* is `round-17`
(`SCORECARD.md:2374`); all three SCORECARD lines and all SKILL lines are authored by round-17
commits (§1); the content asserts measured/probed facts ("8/8 routes matched in both passes",
"REA 6.7.0 adds no keep-log knob (w2 `ScoutReaLogKnob`)", "Re-check on every REA/Ghidra
release"), i.e. probe results, not pins. `CURRENT` is not merely a judgement call: with
`scope=None` the 6.5.0 clauses carry no client token (`:571-583`) and measure AMBIGUOUS —
declaring them CURRENT reproduces FAIL (measured below).

Exact rows to land, inserted after `c1-census-v10.py:276` (the `1759-2122` row):

```python
    ("SCORECARD.md", 2370, 2392, "DATED", 2374, r"round-17"),
    ("SKILL.md", 511, 519, "DATED", 511, r"2026-10-20-r17"),
```

Why these ranges: G18 (`:418-420`) rejects a marker line outside its own range, so a bullet-only
`2380-2382` row cannot name `:2374`/`:2350`. `2370-2392` is the tightest range containing both the
locus block and the section's own round token at `:2374`; `git blame` shows 2370-2392 is exactly one
commit (`8e7642c`), so it is the authored block, not an arbitrary widening. SKILL's own marker is
in-range at `:511` (`…2026-10-20-r17-go-carrier-diagnostics.md`), so its row stays literal.

Measured (harness imports the census module, appends rows to `mod.SCOPE`, then calls its own
`main()` — no reimplementation of the verdict logic; `python3 -I -B measure.py <export> <variant>`):

| variant | rows appended | verdict | exit |
|---|---|---|---|
| none | — (baseline) | FAIL undeclared=2 | 1 |
| recommended | SCORECARD 2370-2392 ml 2374 `round-17`; SKILL 511-519 ml 511 `2026-10-20-r17` | **PASS** | 0 |
| narrow_ok | SCORECARD 2380-2382 ml 2380 `REA 6\.5\.0`; SKILL 511-519 ml 511 | PASS | 0 |
| block_ok | SCORECARD 2370-2392 ml 2374; SKILL 509-519 ml 509 `round 17` | PASS | 0 |
| current_red | both blocks CURRENT | FAIL ambiguous=2 | 1 |
| marker_outside | SCORECARD 2380-2382 ml 2374; SKILL 511-519 ml 509 | FAIL, 2× SCOPE-ERROR G18 | 1 |
| tail_widen | SCORECARD 2123-2567 ml 2294 `2026-10-20`; SKILL 511-519 | PASS | 0 |
| ver_marker | SCORECARD 2380-2382 ml 2381 `6\.7\.0`; SKILL 511-519 | PASS | 0 |
| sc_only_narrow / skill_only_narrow | one row only | FAIL undeclared=1 | 1 |

`narrow_ok` is instrument-valid but its marker is a release token, not the date/round token the
instrument's own records-commit rule requires (`:41-45`); `ver_marker` shows G15 is presence-only,
so a "passing" marker proves nothing by itself. `tail_widen` passes only by laundering the entire
appended tail into DATED — the fail-OPEN path the instrument refuses at `:26-32`; do not land it.
Both rows are required (one alone leaves undeclared=1).

## 5. Coverage, depth, and delivery caveats

- Coverage of the gap: enumerating every locus-bearing block of the three scoped files shows the
  appended tails contain **only** these two — SCORECARD ≥2123 → `2380-2382`; SKILL ≥21 →
  `511-519` (22 locus-bearing blocks total, same set with the tails declared). So the D4 re-key
  closes the whole census gap in the appended records, not just the two reported lines.
- Line-key fragility (inference): SCOPE rows are literal 1-based lines. Any round-20 insert above
  `SCORECARD.md:2370` or `SKILL.md:511` (QUALITY rows, capability rows at `:615-622`, new round
  sections) shifts the anchors and either mis-grades them or trips G15. D5 requires the final
  census at the delivered tip: apply/re-key the rows **after** the last insert, in the same commit
  as the edits (the instrument's standing rule, `:41-45`). Observed at tip `d1d981d2`: SCOPE is
  still unchanged and the anchors are still 2380/512 — transient, the tip is moving.
- Residual named (inference, measured logic at `:591-595`): G16 promotes a dated value equal to a
  live anchor to `current-ok`. Today the block is mixed (`6.5.0` historical + `6.7.0` current-ok →
  disposition `info`, no G11). If the live pins later become the mixed set `{6.5.0, 6.7.0}`, both
  dets become `current-ok` and the block trips G11 (no receipt language). If a rollback makes
  `SKILL.md:512`'s 6.5.0 the live value, SKILL's block becomes `current-ok` and trips G11. The
  DATED declaration is correct but not drift-immune; re-key/receipt if the pins move.
