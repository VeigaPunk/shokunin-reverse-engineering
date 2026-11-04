# ScribeLesson — round 79, lesson rows and QUALITY rows drafted from committed evidence

Seat scope: draft `corpus/lessons/round-79.md`'s `## Mistakes` rows and the `corpus/QUALITY.md` rows
from committed evidence; name, for each of the round-78 spot-check's six routed items, whether
round 79 closes it, where, and what a mistake row would say; expose at least two mistake classes the
two round-79 instruments' own design carries; state the coverage-map consequence. **No lane
production file was edited.** Every write is under
`.ufo/waves/round-79/w1/ScribeLesson/` plus this report.

- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- Base: `29d2ca30b83a6a0d85b0aa979de0138fde1660e6`
- Declaration: `a1f9b81cf0cd5065df3a9b25b30ce2eb184d012d`
- Freeze: `ed68cd0a6cc790cca342380a2d80d1927a668c8c`
- Instruments read: `tools/round-79/gate-mutation.py` (417 lines), `tools/round-79/pointer-bind.py`
  (344 lines at the freeze). Line citations are to the **freeze blob**: during this seat the
  worktree copy of `pointer-bind.py` was being edited (6 insertions / 3 deletions, uncommitted,
  mtime 10:11:49), so its worktree line numbers differ.

Deliverables in this directory: `receipt.json` (machine form of everything below), `mistakes.md`
(5 paste-ready rows), `quality.md` (3 paste-ready rows, ids 141–143), `coverage-row.md` (row text +
measured numbers), `prove.py` + `proofs.txt` (the re-derivations, 23 checks, 0 failures).

## Method

Read the frozen instruments and receipts; then re-derive each drafted claim read-only. `prove.py`
copies the two instruments into `TMPDIR` and imports the copies, so nothing under `tools/` is
touched; `__pycache__` is never written (`-B`, `PYTHONDONTWRITEBYTECODE=1`). One run
produced `proofs.txt`; all 23 checks pass.

## Findings

1. **The frozen R79-C2 counting command cannot run on the frozen instrument.** `.ufo/waves/round-79/claims.json:22`
   prints `python3 -I -B tools/round-79/pointer-bind.py --root . --rev <measured> --json-out <receipt>`
   — no `--battery` — and the freeze-era `main` made the flag mandatory (`pointer-bind.py:319-321` at
   `ed68cd0a`: `if not args.battery or args.rev is None:` → usage, exit 2). Run as printed: exit 2,
   no receipt written (`proofs.txt` §G). The same bytes with `--battery`: exit 0, `checks_total 5`,
   `mismatches 0`. The C2 receipts that exist were therefore taken with the flag; the predicate as
   printed has never been executed. The worktree already carries an uncommitted repair (`--rev` alone
   selects battery mode), which closes the defect once landed **and disclosed as a post-freeze
   supersession**. C1's command (`claims.json:10`) does carry `--battery`.
2. **Two R79-C1 predicate conjuncts are recorded and never scored.** The predicate names "a pristine
   selftest of 29 cases and 0 failures" and "`m03`, `m05` and `m08` … detected by that one case alone".
   The receipt writes `pristine.cases` (`gate-mutation.py:303`) and each mutant's `sole_detector`
   (`:196`, `:269`); `receipt["ok"]` (`:313-317`) and `validate_receipt` (`:200-243`, `pristine.failures`
   only at `:236`) read neither. Forged receipts with `pristine.cases 1`, and with `m03` killed by
   three cases, return `defects []` (`proofs.txt` §A1/A2). At the freeze `m01`, `m06` and `m07` are
   killed by two cases each, so the fix must score the **named subset**, not every mutant.
3. **`pointer-bind.py` resolves duplicate record cells two ways.** Client pins go through a dict
   comprehension (`:127`, last occurrence wins); the Ghidra and `.bashrc` cells through `re.search`
   (`:138`, `:147`, first occurrence wins). A record keeping a superseded cell above the live one
   binds the superseded cell (`proofs.txt` §B: `.bashrc:23-24` then `:28-29` → binds `:23-24`; Kimi
   `:4126` then `:4722` → binds `:4722`). The live `PROVINCE.md` passes only because the operative
   range is on line 27 and the historical `.bashrc:63-69` on line 28 — document order, not a
   declared rule.
4. **The cell-population floor is the parser's own constant.** `ok` requires `len(results) == 5`
   (`:205`), but `parse_record` always emits five checks: three clients (placeholders for absent
   ones), one Ghidra, one `.bashrc`. Empty record → 5 checks, all `unparsed`; a six-cell record → 5
   checks, one cell silently dropped (`proofs.txt` §C). `bind()`'s `line_count` parameter (`:79`) is
   never read — `bind(..., 0, lines)` and `bind(..., 999, lines)` are identical, and the past-end
   bound comes from `len(lines)` (§D). This is the `path-only` control's vacuity, but inside the
   counter.
5. **One remaining read primitive, bounded by digest-only retention.** `battery` reads whatever path
   the record names (`read_lines` → `expand`, `:115-118`, called at `:174`) with no root allowlist; an
   out-of-lane absolute path binds normally (`proofs.txt` §E). The receipt keeps a 64-hex
   `line_sha256` and no line bytes, so the leak is one digest per pointed line; the record's pointers
   are legitimately outside the lane (`~/.omp`, `~/.kimi-code`, `~/.bashrc`), so the fix is a declared
   pointer-root allowlist with a recorded refusal, not a lane-root `commonpath`.
6. **Spot-check item 4 is closed by commit context, not by the receipt's bytes.**
   `.ufo/waves/round-79/pre/selftest-gate.txt` ends `SELFTEST cases=29 failures=0`, contains **zero**
   8+-hex tokens (no rev, path or digest). Its binding is external: `git show a1f9b81c:tools/round-78/attack-gate.py`
   → sha256 `4e4baf00ef0cb34c5615155abd0a746b7e12a6a997340d32ce72c5402d32d2bf` (= the pin at
   `gate-mutation.py:42`), and re-running that blob reproduces the file byte-for-byte
   (`proofs.txt` §F, both sides `7a01905a7381c724`).
7. **The coverage self-check has been red since the round-77 tip.** `SCORECARD.md:23` cites the
   round-76 pair `157/157 knowledge files`; observed: `159/159` at `749c5717`, `161/161` at
   `29d2ca30` and `ed68cd0a`. `A2-cited-fraction` is `ok false` and `--selfcheck` exits 1 at all
   three. Landing the r79 entry makes the population 162; **158 is not the number** (see §Coverage).
8. **Spot-check item 2's count is now five, not four.** At the freeze rev, `.ufo/waves/round-78/claims.json`
   held four disclosures (`01768ac5`, `59a92fbd`, `1a99064b`, `e134045e`) and the round-29 gate flagged
   the freeze `INSTRUMENT_REVISED` on `a1f9b81c`. That fifth revision — round 79's three selftest
   cases — was then disclosed in the round-78 container by `da8e5d5e`, which clears the flag
   (finding 10). The round-79 record's correction must therefore say **five** and name `a1f9b81c`.
9. **Routed item 3 is closed cleanly.** `pre/c2-at-base.json` 5 checks / 3 matched / 2 mismatches
   (`omp-pin`, `kimi-pin`); `pre/controls/c2-path-only.json` 5/5 on the same stale ledger record;
   `l1/scores/c2-at-landing.json` 5/5, `unparsed 0`; `PROVINCE.md:16-18` now names OMP `:12` and Kimi
   `:4722`, `PROVINCE.md:27` names `.bashrc:28-29`.
10. **Freeze gate.** Re-run read-only at two revs (`tools/round-29/freeze-gate.py --root . --rev <rev>
    --require-clean round-79`, scratch `TMPDIR`, 4.27 s each):
    - at the freeze `ed68cd0a`: 54 freezes audited, **29 clean**, gate exit 1. Round-79's entry is
      `CLEAN`, `findings []`, three instruments (`tools/round-78/attack-gate.py`,
      `tools/round-79/gate-mutation.py`, `tools/round-79/pointer-bind.py`) — the freeze narrative
      holds. Round-78's entry is `FLAGGED` with `INSTRUMENT_REVISED` naming `a1f9b81c` (the
      declaration's three selftest cases), `disclosed 4`; round-73 is `FLAGGED`
      `INSTRUMENT_PIN_MISMATCH`.
    - at the new HEAD `da8e5d5e`: **30 clean**, round-78 now `CLEAN` — the commit
      `da8e5d5e round-79: disclose the round-79 revision of the round-78 gate in the round-78 freeze
      container` appends `a1f9b81c` to round-78's `instrument_supersessions`, and the gate accepts a
      post-freeze disclosure there by design (round-78 did the same three times). Round-73 stays
      `FLAGGED`, so the gate still exits 1.
    Consequence for the record: "round-79's entry audits CLEAN" is true at both revs; "the gate exits
    0" is not, and a record that says so is wrong.
11. **The tree moved during this seat.** HEAD advanced `ed68cd0a` → `e0c19339` → `da8e5d5e` while I
    worked, and the worktree now also carries edits to `SCORECARD.md`, `LOG.md`, `SKILL.md`,
    `corpus/{QUALITY,README,SOURCES}.md` and **both** instruments. Every residual-pointer citation
    below is verified against `git show HEAD:` at `da8e5d5e`, and every instrument citation against
    the freeze blob `ed68cd0a`.

## Round-78 routed items — disposition

| # | item | closed by round 79? | where | drafted row |
|---|---|---|---|---|
| 1 | Stale filing-receipt revisions in report + SCORECARD | **no — open at the freeze** (unclaimed record repair) | `SCORECARD.md:6043` still says the receipt rev is `3bb87162`; `LOG.md:4656` still names `bc73b27a` + `3bb87162`; operative rev is `e2846648…` in `.ufo/waves/round-78/l1/scores/{prefile-at-filing,gate-at-tip}.json` | "**superseded revision in prose** — correct every prose copy in the next record, naming old and operative hash" (QUALITY 132) |
| 2 | SCORECARD supersession count | **no — open**, and the correct count is now **five** | `SCORECARD.md:6041` ("changed twice … both"); five disclosures (`01768ac5`, `59a92fbd`, `1a99064b`, `e134045e`, `a1f9b81c`), the fifth disclosed by `da8e5d5e` in round-78's container | "**count restated from memory** — re-derive `len(instrument_supersessions)`" (QUALITY 132) |
| 3 | Stale line pointers + path-only rule | **yes — R79-C2** | `tools/round-79/pointer-bind.py`; base `pre/c2-at-base.json` 3/5, control `mismatches 0`, freeze `l1/scores/c2-at-landing.json` 5/5; `PROVINCE.md:16-18,27` | landed rows + drafted M79-7/M79-8 (parser residue) |
| 4 | No self-test receipt at the final instrument revision | **partly — by commit context only** | `pre/selftest-gate.txt` (`SELFTEST cases=29 failures=0`, no rev/digest); blob at `a1f9b81c` = pin `4e4baf00…`; byte-identical re-run | **M79-9** + QUALITY 143 |
| 5 | Stale line range `attack-gate.py:1-940` | **no in the filed report** (filed bytes are append-only); round 79 closes it by stating measured counts | fleet-root `.ufo/reports/round-78/kaidoku.md:32`; measured 949 lines at `29d2ca30`, 974 at `ed68cd0a` | "**line range without a revision** — state the counted lines with the rev" (QUALITY 18) |
| 6 | LOG structure (round-78 block under the round-77 heading) | **no — open at the freeze** | `LOG.md`'s last `## ` heading is round 77 at line 4574; the round-78 block runs to the tail beneath it | "**heading-less append** — every round opens its own `##` heading" |

## `## Mistakes` rows drafted (M79-5 … M79-9)

Paste-ready in `mistakes.md`. Numbering follows the four rows already in the land lesson (QUALITY
138–140 cite M79-2/M79-3/M79-4); ids 5–9 are free.

- **M79-5 — unrunnable counter.** The frozen predicate's counting command is refused by the frozen
  instrument (`--battery` missing; exit 2, no receipt; `proofs.txt` §G). Captured by QUALITY 141,
  sharpening 76 and 87. Fix: `--rev` alone selects battery mode, disclosed as a supersession; the
  regression case is the command run verbatim against the pinned blob.
- **M79-6 — unscored conjunct.** `pristine.cases` and `sole_detector` are written and never read;
  forged receipts pass `--validate` (§A1/A2). Captured by QUALITY 141. Fix: score `pristine.cases == 29`
  and the three named ids only.
- **M79-7 — undeclared precedence.** One parser, last-wins for client pins and first-wins for
  Ghidra/`.bashrc`; the live record passes on document order (§B). Captured by QUALITY 142.
- **M79-8 — vacuous floor.** `len(results) == 5` is the parser's constant; six cells truncate to
  five; `line_count` is dead (§C/§D). Captured by QUALITY 142 and Row 139's control clause.
- **M79-9 — context-bound receipt.** The landing tally names no revision (§F). Captured by
  QUALITY 143, extending 18 and 130.

## QUALITY rows drafted (141–143)

Paste-ready in `quality.md`; the highest existing id is 140 (rows 138–140 are the L1's in-flight
landing), so 141–143 are free and do not reuse an id.

- **141** — a frozen predicate runs as printed, and every conjunct it states is scored.
- **142** — a record parser declares its cell precedence and its cell population.
- **143** — a cited count carries the revision and population it was measured at, and is restated
  when the population moves.

## Coverage-map consequence

Measured with `tools/round-66/coverage-selfcheck.py` (see `coverage-row.md`):

| state | population | stem map | recipe A | `A2` |
|---|---|---|---|---|
| `ed68cd0a` (freeze) | 161 | 161/161 → **10.0** | 142/161 → 8.82 | `[157,157]` vs `[161,161]`, **ok false**, exit 1 |
| `749c5717` (round-77 tip) | 159 | 159/159 → 10.0 | 142/159 → 8.93 | `[157,157]` vs `[159,159]`, ok false |

If the L1 lands the one knowledge entry `corpus/knowledge/2026-11-04-r79-mutation-and-pointers.md`:

- **without** the map row: stem 161/162 → head score **9.94**, `A1-head-score` fails;
- **with** the row: stem 162/162 → head **10.0**, `A1` holds; recipe A moves 142/161 (8.82) →
  142/162 (**8.77**) because `DATE_TOKEN_RE` matches `2026-10-` only.

So the row is load-bearing, not cosmetic. The row text I would add (after `corpus/README.md:119`):

```
| Instrument and record layer, round 79 | `2026-11-04-r79-mutation-and-pointers` | held — the selftest mutation battery (eight exact single-occurrence edits to `tools/round-78/attack-gate.py` at the measured rev, each killed only by its own declared selftest case, an absent case a survivor, and `m03`/`m05`/`m08` each caught by that one case alone) and the line-bound pointer binder (five `PROVINCE.md` pointer cells read at the 1-based line or range they name, the pointed lines retained as a sha256, with a committed `path-only` control that cannot fail); the lane's own record layer, not a new carrier class |
```

The cited fraction must be restated **in place** at `SCORECARD.md:23` to the observed pair **162/162**
— not 158. `157` is the round-76 count, already four entries behind at the round-77 tip. The
counter splits on the first `## Owned axes` (only one, `SCORECARD.md:19`) and takes its first
`| coverage |` line (line 23), so an appended second axes table would be invisible.

## Limits

- I did not execute either claim's battery as a claim measurement. Counters here are re-derived from
  the committed receipts; the only executions are read-only re-runs of the instruments' own logic on
  copies (`prove.py`) and the printed-command reproduction.
- Citations are freeze-blob citations. `tools/round-79/pointer-bind.py` was mid-edit in the worktree
  during this seat, so any worktree-anchored line number would drift.
- The coverage numbers are measured at three revs; a later entry, map row or scorecard restatement
  invalidates them.
- No client config was opened for this seat; the pointer digests in the receipts are the
  instruments' and were not re-read.
- No tool was installed or upgraded (Python 3 standard library only), so there is nothing to record
  under the operator's install log.

## Files written

- `.ufo/waves/round-79/w1/ScribeLesson.md` (this report)
- `.ufo/waves/round-79/w1/ScribeLesson/receipt.json`
- `.ufo/waves/round-79/w1/ScribeLesson/mistakes.md`
- `.ufo/waves/round-79/w1/ScribeLesson/quality.md`
- `.ufo/waves/round-79/w1/ScribeLesson/coverage-row.md`
- `.ufo/waves/round-79/w1/ScribeLesson/prove.py`
- `.ufo/waves/round-79/w1/ScribeLesson/proofs.txt`
