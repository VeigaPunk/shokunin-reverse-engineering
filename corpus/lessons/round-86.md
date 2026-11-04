# Round 86 — a record is re-derived where it states a value; a gate row is run, not read

Base `2cf0b7ff93c698809bed321f7338276a22d6beb9`; declaration `b205bb8b66ec7b61e028bccd92f64eade8942461`
(plan, both counters, BASE receipts); container commit `ec9963eb9e5c1eedfada9a69f073c1639e7911f9`;
integration `4cc03025e6d4f6f1e00b5e402fcc0180e6e730bc` (measured revision). One v1 wave `r86-w1`, twelve
seats. The round-85 non-author spot-check (`corpus/lessons/round-85-verifier-spotcheck.md` §8) is the
input; its routed defects are answered in the Corrections section below. The round-85 lesson is not
rewritten.

Claims: **R86-C1** (calibration — three record cells re-derived from the bytes they describe): **missed**
on its frozen target (A1 and A2 agree; A3 cannot be met under its frozen rule). **R86-C2** (operability —
the round-85 gate's registry row re-derived by running it): target met at `4cc03025` (5/5), **not
admitted**, because operability is not an owned lane axis.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M86-1 | a correction filed in prose leaves a record cell wrong where the instruments read it: the round-85 S303 correction went into a lesson, while `corpus/SOURCES.md:219` still said "five scopes" for eight rows that carry the URL | `corpus/lessons/round-85.md` Corrections C-R2; `corpus/SOURCES.md:219` at `2cf0b7ff`; `.ufo/waves/round-86/pre/c1-at-base.json` (A1 mismatch) | QUALITY 149 was applied to lesson text, not to the registry cell it describes | supersession row S305 (`corpus/SOURCES.md:221`) with count 7 and seven ids; A1 agrees at `4cc03025` (`.ufo/waves/round-86/l1/scores/c1-at-integration.json`); QUALITY 150 |
| M86-2 | a frozen atom clause the counter does not enforce: G3 says the self-test command must be "on that tool path"; `gate-registry.py` checks only that the cell starts with `python3 ` | `.ufo/waves/round-86/l1/sweep/g3-behavioural-red.txt` and `g3-foreign-command-accepted.json` (a foreign `python3 -c` row scores 5/5); critic C2.1; sentinel C-2 | the plan-to-counter sweep for token lists (QUALITY 148) does not cover path clauses; a text-presence sweep also passes, because the phrase sits in the counter's docstring (`l1/sweep/atom-clause-sweep-red.txt`) | QUALITY 151 names the behavioural check; the successor declaration carries a foreign-command fixture, shown red on the frozen counter now, so it can fail |
| M86-3 | a frozen rule and its BASE description were not re-derived against the BASE bytes before freeze: A3 says the coverage row "names only a round-67 receipt" (the row names rounds 84, 76, 75, 68 and 67) and requires "exactly one `| coverage |` row" (the card has 23) | `git show 2cf0b7ff:SCORECARD.md \| grep -c '^| coverage |'` = 23 (`l1/sweep/atom-clause-sweep-red.txt`); `pre/c1-at-base.json` detail "found 23"; ReviewerC1 BASE table; critic C1.14 and C1.15 | nothing compared the plan's stated BASE cause or the row count with the BASE receipt before the container was frozen | a successor declaration must sweep the rows its rule selects at BASE and compare them with the plan text before freeze; the sweep is red on this round's plan (23 against one) |
| M86-4 | evidence exit codes lost through a pipe: the start-of-round census run piped through `tail`, so the printed `EXIT` was `tail`'s | the first census command in this round's session; re-run as `.ufo/waves/round-86/pre/sources-census-before.txt` (exit 0 recorded directly) | none; caught only on re-reading the command | re-ran each gate with its exit captured directly (`cmd > file 2>&1; echo $?`); every exit in this round's receipts is taken that way |

Captured in-round, recorded as a working example: the freeze precheck (R84-C1 gate) reported the container
FLAGGED at `b205bb8b` because the receipt paths sat inside scanned claim strings. The receipts were moved
into a `receipts` map and the container is CLEAN at `ec9963eb` (`pre/freeze-precheck-at-declaration.json`,
met true with the positive and negative containers).

### Why QUALITY 149 did not catch M86-1

Round 85 did re-derive the count (`git show 91eeb72f:corpus/SOURCES.md | grep -c -F 'rea-agents-6.5.0.tgz'`
returned 8, seven of them prior rows) and wrote the derivation into `corpus/lessons/round-85.md`
Corrections C-R2. The registry cell at `corpus/SOURCES.md:219` was never changed: the round-85 commit
`01f2d5193` adds one row (S304) and changes no existing cell. A lesson says that a number was wrong; the
cell is what a reader and a counter read. QUALITY 150 now states the rule where the cell lives.

## Gate

| source | decision | opened 2026-11-04 | located quote and judgment |
|---|---|---|---|
| S255 git-show documentation, `https://git-scm.com/docs/git-show` | admit by re-open (mined, tier A); used-by extended by the round-86 knowledge entry | HTTP 200, 246736 bytes, sha256 `a3716a4d6c236082b0f6d08da64735765f376c1c32ba5ede93b70b013f52a9aa` (this lane's fetch; byte-identical on a second fetch) | DESCRIPTION, served page: "For plain blobs, it shows the plain contents." (8 words, ≤25). The row's `opened` cell stays 2026-11-01; this re-open is recorded here and in the knowledge entry, not by changing the row's date. |
| S303 npm tarball as authority for the gap taxonomy | stays **rejected**, unchanged | — | The supersession does not flip a rejection. Flip condition unchanged. |
| S305 correction row for S303's scope count | **rejected** (a correction row, like S303; it adds no source) | no document opened; the URL is S303's | teaches opens `supersedes S303`; count 7 and seven prior ids, re-counted with `grep -c -F` over the registry at the round-86 base. It carries no URL of its own, so it adds no duplicate-URL warning. |

**Sourced claim.** The knowledge entry `corpus/knowledge/2026-11-04-r86-record-agreement.md` cites S255,
re-opened this round. It satisfies §2b item 4.

**Per-entry scope.** One knowledge entry, bounded to record cells and registry rows; no artifact class and
no frontier promotion. No `merge/kaidoku/` package was consumed and no `considerthese/` directory exists in
this lane, so the assimilation line reads "none".

## Corrections (append-only; the round-85 texts are not rewritten)

### C-R86-1 — the A2 docstring status (routed R85-5)

Old, `tools/round-84/mutation-closure.py` line 8, at `2cf0b7ff` (the sentence about an absent declared
case):

```text
present in the target's own output; an absent declared case is inconclusive, never a pass).
```

New, the same line, docstring only:

```text
present in the target's own output; an absent declared case scores survived, never a pass).
```

The code assigns `survived` in its `not case_present` branch (`tools/round-84/mutation-closure.py`
`elif not case_present:`). The word `inconclusive` is the code's name for a different condition. The
docstring-only revision has sha256 `4d73c89e45fd1657dfc56d30f0ab4e15f08e84093d080f81a6c87668f3cff5ed`
(previously `e5cfd2ed…`). Code and selftest bytes are unchanged (selftest 10 cases, failures 0), and the
round-85 frozen 21-row depth table still kills 21 of 21 at `4cc03025` (`l1/scores/c2-mutation-closure-r85-table-at-integration.json`).
Round-85 receipts keep the old digest; this revision is disclosed in the container's
`instrument_supersessions`.

### C-R86-2 — the S303 supersession (routed R85-3)

`corpus/SOURCES.md:219` (S303's scope cell, "five scopes") is left as written, per SOURCES rule 2. The
correction is the new row at `corpus/SOURCES.md:221`, S305, with count 7 (S079 S080 S083 S090 S092 S119 S123).
A1 agrees at `4cc03025`.

### C-R86-3 — the A3 coverage pointer (routed R85-6): not repaired

The frozen A3 rule requires exactly one `| coverage |` row, and the card has 23. Making the counter's rule
true would mean deleting or relabelling 22 history rows, and the rule was not re-derived before freeze
(M86-3). The coverage row is unchanged, so its evidence and round still read round 85. No receipt was
created to satisfy the counter, and none was backdated. R85-6 stays open.

## Sweep evidence

- `.ufo/waves/round-86/l1/sweep/atom-clause-sweep-red.txt` — phrase counts across the plan and the two
  counters (text presence, not enforcement; shows why M86-2 passed a text sweep) and the BASE coverage-row count (23).
- `.ufo/waves/round-86/l1/sweep/g3-behavioural-red.txt` and `g3-foreign-command-accepted.json` — the
  behavioural sweep that is red on the frozen counter.

## Routed to the next steered round (a new declaration, never an in-place edit)

1. C1 atom A3: re-declare against a rule the card's own current-assessment pointer selects, with the BASE row count in the pre-freeze sweep (M86-3).
2. Gate counter (`tools/round-86/gate-registry.py`): run G2 and G3 from `git show REV:` blobs (sentinel C-1); enforce "on that tool path" (M86-2); refuse a verdict substring and six-cell rows (critic C2.5/C2.6, reviewer e3, b1, b2); refuse `--json-out` into `pre/` (sentinel C-13).
3. Record counter (`tools/round-86/record-agreement.py`): define "newest" by id or date, not file order (critic C1.2); make the count selector match its docstring (C1.3); refuse fenced examples and split status sentences (reviewer); make the rev-shape check a commit check (critic C1.16).
4. Selftests: 13 of 20 mutants survive the two counters' selftests (`.ufo/waves/round-86/w1/MutationR86/report.md`); add the named missing cases and make the selftest exercise the production atoms, not a fixture tool (critic C2.14).
5. Axis: operability is not an owned lane axis. Either name an owned score a gate-registry claim moves, or record the operator's ruling in `.ufo/l0-questions.md`.
6. Carried: R85-4 (declared-case binding limits); R85-6 (coverage pointer); the planner-seat deviation (L1-held, disclosed).
