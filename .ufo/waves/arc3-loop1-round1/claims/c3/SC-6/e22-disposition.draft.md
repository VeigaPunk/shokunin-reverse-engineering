# E22 disposition record — DRAFT (SC-6, chain c3, arc3-loop1-round1)

Seat SC-6 · role scribe · 2026-10-19 · measured at HEAD
`e845c2b524ad2e59871e004c51a1386e192a74ab` (work tree: only
`?? .ufo/waves/arc3-loop1-round1/` + pre-existing ` M .ufo/waves/arc2-loop1-round10/C3.md`).
This is a DRAFT for parent integration; nothing here is applied. SC-6 is not the
EX-28 seat and did not write `.ufo/gates/c1-census-v10.py`.

## 1. The finding as recorded

`SCORECARD.md:850-852` (arc2-loop1-round3 section; inside the DATED row
`:769-855`), verbatim:

> … E22 census scope-table drift (FAIL undeclared=2 at 766-line HEAD vs PASS at
> 701-line `b21c0da` — re-key or retire next calibration round) …

Origin, as measured by the round-3 seats (all read-only captures, in-repo):

- `.ufo/waves/arc2-loop1-round3/E5.md:14` — "the instrument FAILs at HEAD for an
  unrelated reason … `VERDICT: FAIL (stale=0 ambiguous=0 undeclared=2
  unresolved=0)`, exit 1. The two UNDECLARED loci are round-2's *own records
  append* (SCORECARD.md blocks 731-737 and 747-766), which fell outside the
  instrument's hardcoded SCOPE table — the G6 guard firing correctly on file
  growth." Baseline block verbatim at `E5.md:48`; second copy `E5.md:126`.
- `.ufo/waves/arc2-loop1-round3/R8.md:227-233` (re-anchor duty) — v9 returns
  PASS 0/0/0/0 at `b21c0da`, FAIL undeclared=2 at HEAD; SCOPE's last entry was
  `:635-701`; extending SCOPE alone trips `G11 current-ok without receipt
  language: ['SCORECARD.md:731']`.
- Instrument at finding time: `c1-census-v9.py`, sha256
  `213fe679838ea217f4d34aa7d0e85bf73845a42ae49b68c9d8d52b4d38e6707c`
  (`.ufo/waves/arc2-loop1-round2/E22.md:698`; v9 was never committed under
  `.ufo/gates/`).

## 2. Measured verdict at HEAD

Instrument at HEAD: `.ufo/gates/c1-census-v10.py`, 433 lines, sha256
`36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48`.

```
$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
$ python3 .ufo/gates/c1-census-v10.py            # exit 0
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1336 loci=9
SKILL.md       lines=371  loci=2
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

Capture: `claims/c3/SC-6/census-v10-at-head.txt` (91 lines, sha256
`3b677b8ee47eccb217616eba641fc0b66f72e53634a5ae51a92f8b04e2a22418`), **byte-identical**
to EX-26's independent capture (diff empty; EX-26 `census-at-HEAD.exit` = 0),
to EX-30's `census-head-t0.txt`, and to RV-11's `census-head.out` — four
independent captures, one digest.

The two formerly-undeclared blocks read at HEAD (same capture, lines 35-42):

- `SCORECARD.md block 732-738 [scope DATED]` — 5 bare loci, all `current-ok`
  ("value equals a live anchor", G16).
- `SCORECARD.md block 748-767 [scope DATED]` — `:753 [bare] kimi=6.7.0 ->
  current-ok (matches live kimi)`.

"At HEAD" proof: EX-26 verified the three scoped files and the instrument are
byte-identical worktree-vs-HEAD-blob (`.ufo/waves/arc3-loop1-round1/seats/EX-26.md`
§1, "dirty-worktree attack, refuted"); the one dirty path
(`.ufo/waves/arc2-loop1-round10/C3.md`) is outside the instrument's scope.

## 3. Row-level disposition — re-keyed / retired, with causes

SCOPE rows that changed between the finding (v9, 2026-10-18) and HEAD:

| # | row | change | commit | cause |
|---|---|---|---|---|
| 1 | `("SCORECARD.md", 702, 767, "DATED", 703, r"arc2-loop1-round2")` | **ADDED** (v9 had no row covering the round-2 records append) | `265e1aa` (arc2-loop1-round4) | the two UNDECLARED blocks (then `:731-737`, `:747-766`) were round-2's own records append; G6 fired correctly on file growth. Fixed bound to the then-EOF was chosen over an open-ended tail — the open-ended-bound laundering path was measured and refused (`.ufo/waves/arc2-loop1-round4/Z1.md:138` §4d; SCORECARD.md:908 "fixed-bound re-key; laundering path refused") |
| 2 | `("SCORECARD.md", 768, 854, "DATED", 768, r"arc2-loop1-round3")` | **ADDED** (fixed bound at the then-EOF) | `265e1aa` (round 4) | same re-key; the bound must move in the commit that appends the next records section (Z1 §4d, quoting round-3's own precedent at SCORECARD.md:849-851) |
| 3 | `RECEIPT` regex `r"2026-10-18\|receipt\|SHA-256\|sha256\|re-grepped"` | **WIDENED** so the round-2 battery block's receipt language is recognized | `265e1aa` (round 4) | R8.md:227-233's G11 trap — extending SCOPE alone left `G11 … ['SCORECARD.md:731']` |
| 4 | rows 1-3 above, plus the r1 row `635-701` | **SHIFTED +1**: `635-701→636-702`, `702-767→703-768`, `768-854→769-855` (markers re-assert at 636/704/769) | `6bc4c29` (arc2-loop1-round8) | the r7 capability row inserted at `SCORECARD.md:622` shifted the file below by one line; `git show 6bc4c29 -- .ufo/gates/c1-census-v10.py` shows exactly these three row edits |
| 5 | — | **RETIRED: none** | — | the debt's "or retire" branch was not taken; no row was removed |

Post-r8, rounds 9 and 10 appended SCORECARD sections **without** touching the
instrument (`git log --oneline -- .ufo/gates/c1-census-v10.py` → `6bc4c29`,
`265e1aa` only), and the census still reads PASS (rounds 9/10 records:
SCORECARD.md:1249, :1312 "census v10 PASS").

Prior disposition records already in the tree, for continuity:

- SCORECARD.md:908 (round-4 row) — "census verdict FAIL(undeclared=2,
  unreproducible at HEAD) → v10 PASS 0/0/0/0 at the work tree (fixed-bound
  re-key; laundering path refused) | improved".
- SCORECARD.md:990 (round-5 section) — "E22-v9 fence = CLOSED (v10 canonical)".
- SCORECARD.md:1096 (round-6 section) — "the round-4 E22-v9... closed (r5).
  Retired: none."

## 4. Final verdict

**DISCHARGED — by re-key, at HEAD, by measurement.**

- No undeclared loci, no stale loci, no scope errors, no unresolved, no G11/G7
  warnings at HEAD (`e845c2b`); the FAIL class of the finding cannot reproduce
  under v10.
- v9 remains red at HEAD **by construction** — RV-11 re-ran the recovered v9:
  `v9-at-b21c0da.txt` → PASS 0/0/0/0; `v9-at-679af5d.txt` → FAIL undeclared=2
  (the original finding, reproduced); `v9-at-HEAD.txt` → FAIL undeclared=2 +
  `SCOPE-ERRORS ["SCORECARD.md:635 marker '2026-10-18' absent from ''"]`.
  The fence is the re-key, not a scope retirement.
- Residual (named, measured, not a defect): the declared SCORECARD bound is
  `:855` against a 1336-line file; rounds 4-10 records sections (`:856-1336`)
  are outside the table. At HEAD that tail holds **zero** loci in this
  instrument's unit — no `rea-agents@` pin, no bare `6.x.y`, no `~`/`/`-absolute
  `path:line` pointer (raw greps; EX-26's independent grep concurs: 0
  `rea-agents`, 0 `6.x.y` in 856-1336; EX-26 also measured 0 asserts outside
  declared ranges). Two relative-path pointers exist in the tail
  (`evidence/round-1-2026-10-15/rubric.json:61` at :923-924, `rubric.json:61` at
  :989) and are outside the PTR unit by construction (PTR requires a `~` or `/`
  prefix) — a unit boundary, stated.
- The fixed bound is the deliberate fail-closed posture, and it is **measured**
  (attacks §5): an injected `rea-agents@6.4.0` at EOF reads
  `UNDECLARED … FAIL … exit 1`.
- Forward note for the records commit (parent-owned): the round's SCORECARD
  records append lands at EOF. Per the instrument's own design the appended
  text must be locus-free in the census unit (no `rea-agents@x.y.z`, no bare
  `6.x.y`, no `~`/`/`-absolute `path:line`) **or** the bound must be re-keyed
  in the same commit — round-3's precedent, quoted at Z1 §4d. The claim's
  terminal reading ("PASS at the records commit") is re-runnable verbatim with
  `python3 .ufo/gates/c1-census-v10.py`; it is not measurable by SC-6 because
  the records commit does not exist yet.

## 5. Attacks / refutations attempted (all on fixture copies in this seat's artifact dir)

Fixture = byte copies of `PROVINCE.md` / `SKILL.md` / `SCORECARD.md` at HEAD,
run through the real instrument with `--root <fixture>` (client configs still
read read-only from `$HOME`). Baseline fixture run: PASS 0/0/0/0, exit 0
(`fixture-baseline.txt`).

| # | attack | result | verdict |
|---|---|---|---|
| A1 | append `rea-agents@6.4.0` at SCORECARD EOF (line 1338) | `SCORECARD.md block 1338-1338 [scope None] … UNDECLARED (1)`, `VERDICT: FAIL`, exit 1 (`fixture-tail-locus.txt`) | **caught** — fail-closed posture measured |
| A2 | strip the date from the round-3 header (`:769`) only, keep the section name | PASS, exit 0 (`fixture-marker-strip.txt`) | **not caught — attack mis-designed**: that row's declared marker regex is the section name `arc2-loop1-round3`, not the date. Re-designed as A3. Kept as evidence: the r2/r3 rows assert section names, so a date edit inside a dated section is not a scope error for those rows |
| A3 | strip the marker text entirely at `:769` | `SCOPE-ERRORS ["SCORECARD.md:769 marker 'arc2-loop1-round3' absent …"]`, FAIL, exit 1 (`fixture-marker-strip2.txt`) | **caught** — G15 marker assertion works |
| A4 | corrupt the r1 row's date marker at `:636` (`2026-10-18`→`2026-10-XX`) | `SCOPE-ERRORS ["SCORECARD.md:636 marker '2026-10-18' absent …"]`, FAIL, exit 1 (`fixture-r1-date-strip.txt`) | **caught** — the exact stale-row class v9 failed on at HEAD (v9 `:635` marker absent) is what v10's re-keyed `:636` row catches |
| A5 | independent-run agreement | my capture byte-identical to EX-26 / EX-30 / RV-11 captures (sha `3b677b8e…`) | **no divergence** |
| A6 | reproduce the finding's before-state | RV-11's v9@`679af5d` → FAIL undeclared=2 (matches E5.md:48 verbatim) | **reproduced** |

Fixture copies were removed after the runs; the six capture files above remain
in this directory. /tmp was unusable (see blockers), so the fixtures lived in
this seat's artifact directory.

## 6. Proposed patch text (for EX-28 / parent; NOT applied)

**P1 — instrument header stanza** (`.ufo/gates/c1-census-v10.py`, lines 1-2).
The C3 claim requires the disposition "stated in the instrument's own header".

Current:

```python
"""C1 census v10 — v9 (sha256 213fe679…) re-keyed per arc2-loop1-round4 Z1 section 4d."""
#!/usr/bin/env python3
```

Proposed:

```python
"""C1 census v10 — v9 (sha256 213fe679…) re-keyed per arc2-loop1-round4 Z1 section 4d.

E22 DISPOSITION (arc3-loop1-round1; measured 2026-10-19 at HEAD e845c2b,
instrument sha256 36e96cd5…): the arc2-loop1-round3 carried debt "census
scope-table drift (FAIL undeclared=2 at 766-line HEAD vs PASS at 701-line
b21c0da — re-key or retire)" is DISCHARGED BY RE-KEY, none retired. Rows added
at 265e1aa (round-2 :702-767, round-3 :768-854, fixed-bound at the then-EOF;
RECEIPT widened) and shifted +1 at 6bc4c29 (r1 :636-702, r2 :703-768,
r3 :769-855) for the capability-row insertion at :622. At HEAD: PASS 0/0/0/0
(scope-errors [], g11 []); the declared SCORECARD bound :855 vs file EOF :1336
is the deliberate fixed-bound posture — the uncovered tail :856-1336 holds zero
loci in this unit at HEAD, and an injected tail locus reads UNDECLARED (FAIL,
exit 1). Records appends must stay locus-free in this unit or re-key the bound
in the same commit."""
#!/usr/bin/env python3
```

**P2 — optional round-records sentence** for the parent's SCORECARD records
section (draft text, not applied):

```
- C3 freshness — E22 dispositioned at HEAD by measurement: census v10 PASS
  0/0/0/0 (undeclared=2 → 0; four independent captures, one digest `3b677b8e…`);
  rows re-keyed at `265e1aa` (r4; two fixed-bound DATED rows + RECEIPT widening)
  and `6bc4c29` (r8; +1 shift for the :622 capability row); none retired; the
  uncovered tail :856-1336 measured locus-free, injected tail locus → UNDECLARED
  (FAIL, exit 1); v9 stays red at HEAD by construction (v10 canonical).
```

## 7. Blockers / environment

- **/tmp user quota exhausted** on this host: `echo test > /tmp/x` →
  `bash: echo: write error: Disk quota exceeded`; a python redirect to /tmp
  exits 120 with empty output (the interpreter cannot flush stdout). All scratch
  therefore lives in this seat's artifact directory; the wave rule "scratch
  copies go under /tmp" is not executable as written right now. This matches
  the standing hazard already recorded at SCORECARD.md:991 ("/tmp quota hazard =
  standing (seats relocated, evidence intact)").
- EX-28 (the seat authorized to write `.ufo/gates/c1-census-v10.py`) had not
  landed at last poll (07:03Z); P1/P2 are proposals only.
- SC-6's footprint: created `claims/c3/SC-6/` (captures + this draft) and, from
  a read-only `importlib` audit of the instrument, transiently created
  `.ufo/gates/__pycache__/c1-census-v10.cpython-314.pyc` (mtime 07:02) — removed
  at 07:03; a new `__pycache__` appeared at 07:04:16 from another seat's module
  audit (not SC-6) and was left in place. No git mutations were run by SC-6.
