# ScribeSources — round-79 wave-1 source rows (draft, not landed)

**Seat:** ScribeSources · **Round:** 79, wave 1 · **Lane:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
**Base:** `29d2ca30` · **Declaration:** `a1f9b81c` · **Freeze:** `ed68cd0a` · **HEAD at work:** `e0c19339`

**Outcome in one line:** both target pages were opened once each and reproduce the registered
bytes exactly; both URLs are already held at `corpus/SOURCES.md:212` (S295) and `:213` (S296), so
both are **refused reuse** and **no row was drafted for append**. The two holding rows are
uncommitted and absent at the declaration and the freeze; S295 is clean, S296 carries a wrong
word count (17 vs 15), a range that belongs to a longer quote, and scope wording that imports
vocabulary the page does not carry. Repairs are drafted below for the L1's pre-commit window.

## Behavior

1. One GET per URL with `curl`, body saved under this evidence dir; HTTP status, byte count,
   content type and sha256 recorded from that single response.
2. Each quote located by searching the saved bytes, counted by whitespace tokenisation, and
   reported with its section heading and snapshot line(s).
3. The pre-append duplicate check ran against the working-tree `corpus/SOURCES.md` before any
   drafting: both URLs (and both hosts) are held, so step 4's rows are refused, not written.
4. Id arithmetic checked with the spec's command and a corrected one.
5. Drafts (Gate block, row repair) written only under this evidence dir.

## Snapshots — one GET each, 2026-11-04

| URL | HTTP | bytes | sha256 | content type |
|---|---|---|---|---|
| https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html | 200 | 21 316 | `9473205c9203676853dd5dfb486f2d7a7e223aa7336a59a3481b05be90dcd531` | text/html; charset=UTF-8 |
| https://mutants.rs/ | 200 | 22 602 | `d056b2b3580903a000f3b7852a85768c61ac190e5da70690281f5175f4a2ec6d` | text/html; charset=utf-8 |

Both bodies are **byte-identical** (`cmp` clean) to the snapshots the holding rows cite in
`.ufo/waves/round-79/l1/sources/`; the fetch time was 13:07:07Z / 13:07:08Z.

## Located quotes

### S295 / R79-C2 — POSIX `grep`, OPTIONS `-n`

> "Precede each output line by its relative line number in the file, each file starting at line 1."

- **Words:** 18 (whitespace tokens).
- **Location:** OPTIONS, term `-n` (snapshot line 96); the quote is a byte-contiguous substring
  of snapshot line **97**.
- **Grounds:** the 1-based, per-file numbering `tools/round-79/pointer-bind.py` relies on. The
  next sentence (line 97-98, outside the budget) adds the reset: `The line number counter shall
  be reset for each file processed.`

### S296 / R79-C1 — cargo-mutants book, Welcome

> "quality by finding places where bugs can be inserted without causing any tests to fail"

- **Words:** 15 (whitespace tokens).
- **Location:** *Welcome to cargo-mutants* (h1 at snapshot line 183); the words occupy snapshot
  lines **185-186** — the raw HTML soft-wraps between `without` and `causing`, with no markup
  between them, so the sentence is contiguous in the rendered paragraph.
- **Grounds:** the survivor premise of `tools/round-79/gate-mutation.py`: a defect that no test
  failure catches was never killed, so an absent declared case is a survivor.
- **Same-claim variant, 21 words, snapshot lines 184-186:**
  "It helps you improve your program’s quality by finding places where bugs can be inserted
  without causing any tests to fail" — this is the span the holding row and the knowledge entry
  both cite, so it is the cheaper repair target.
- **Limit:** the page never uses `mutant` as a standalone noun (13 occurrences, all the product
  name or its URLs) and never uses `kill` or `survive` (0 each).

## Pre-append duplicate check → refused reuse

```
$ grep -nF -- 'https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html' corpus/SOURCES.md
212: | S295 | POSIX.1-2024 `grep` — https://pubs.opengroup.org/…
$ grep -nF -- 'https://mutants.rs/' corpus/SOURCES.md
213: | S296 | cargo-mutants book, Welcome — https://mutants.rs/ …
$ grep -nF -- 'pubs.opengroup.org' corpus/SOURCES.md   → 212 only
$ grep -nF -- 'mutants.rs'          corpus/SOURCES.md   → 213 only
```

Both needles hit exactly one line each; there is no third holder. Full receipt:
`pre-append-url-check.txt`. The rule is decisive — **a URL already held is a refused reuse, not
a row** — so nothing is appended and the two drafted ids are not spent.

## Id check

| check | command | output |
|---|---|---|
| spec (verbatim) | `grep -oE 'S[0-9](3,)' corpus/SOURCES.md \| sort -u \| tail -3` | *(empty)* |
| corrected | `grep -oE 'S[0-9]{3,}' corpus/SOURCES.md \| sort -u \| tail -5` | S292 S293 S294 S295 S296 |
| highest id | `grep -oE '^\| S[0-9]{3,} ' … \| sort -n \| tail -1` | **S296** |
| row count | `grep -cE '^\| S[0-9]{3,}' corpus/SOURCES.md` | 202 |

The spec's pattern matches nothing: in POSIX ERE `(...)` groups, so `S[0-9](3,)` asks for a
literal `3,`. **Actual next ids: `S297`, `S298`** — and `S295`/`S296` were unavailable because
they are occupied, not merely because the registry had moved past them.

## Gate block draft (for `corpus/SOURCES.md`)

`corpus/SOURCES.md` has no `## Gate` section at this revision; the round-78 Gate block lives in
`corpus/lessons/round-78.md`. The draft below follows that block's shape. Note that both
decisions are refusals, so the table is an audit of the holding rows rather than an admission.

## Gate

Both pages were opened this round with one GET each; snapshots, byte counts and sha256s are in
`.ufo/waves/round-79/w1/ScribeSources/`, and both are byte-identical to the snapshots the two
holding registry rows cite in `.ufo/waves/round-79/l1/sources/` (`cmp` clean, same sha256).

| source / decision | URL | accessed | located quote (≤25 words) | digestion |
|---|---|---|---|---|
| S295, POSIX.1-2024 `grep`, OPTIONS `-n` — verified, **no append** (already held) | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html | 2026-11-04 (HTTP 200, 21 316 B, sha256 `9473205c…`) | "Precede each output line by its relative line number in the file, each file starting at line 1." (18 words; OPTIONS `-n`, snapshot line 97) | The row the pointer binder rests on: each file starts at line 1 and the counter resets per file, so a `path:line` pointer is read at that line instead of searching the file for the token. Row verified cell-by-cell against the served bytes; nothing changed. |
| S296, cargo-mutants book, Welcome — refused reuse (held, one cell repair) | https://mutants.rs/ | 2026-11-04 (HTTP 200, 22 602 B, sha256 `d056b2b3…`) | "quality by finding places where bugs can be inserted without causing any tests to fail" (15 words; Welcome to cargo-mutants, snapshot lines 185-186) | Supplies the survivor premise: a defect no test failure catches is the one the battery must not count as killed. The holding row's anchor says 17 words for this text (15 measured) and cites lines 184-186, which is the span of the 21-word full sentence, not of the 15-word quote; the recommended repair is below. The page carries no standalone "mutant", "kill" or "survive". |

**Refused reuse (not a row).** `https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html`
and `https://mutants.rs/` were opened for the two round-79 claims and refused registration: S295
holds the first URL (`corpus/SOURCES.md:212`) and S296 the second (`corpus/SOURCES.md:213`), so a
second row for either would duplicate it. The pre-append grep is `pre-append-url-check.txt`; no row
was appended. Both holding rows are uncommitted working-tree lines — absent at the declaration
`a1f9b81` and at the freeze `ed68cd0a` — so the append-only gate sees them as additions, not as
base rows, and the pre-commit window is the only place their cells can still be repaired.

**Row repair (recommended, uncommitted).** Two defects in S296's cells, neither in S295:

1. *Word count.* The quoted text is 15 words, not 17. Option A (recommended) widens the quote to
   the full sentence ("It helps you improve your program’s quality … to fail", 21 words, snapshot
   lines 184-186), which keeps the range both the row and the knowledge entry already cite; the
   count then reads 21. Option B keeps the 15-word quote, changes the range to 185-186 and the count
   to 15, and must also change `corpus/knowledge/2026-11-04-r79-mutation-and-pointers.md:1`, which
   repeats 184-186.
2. *Vocabulary.* The Welcome page uses neither "mutant" as a noun nor "kill"/"survive" (13
   occurrences of "mutant", all inside the product name and its URLs; 0 of "kill"; 0 of "surviv").
   The scope and teaches cells should state what the page says — bugs can be inserted without
   causing any tests to fail — and leave the kill/survive wording to the instrument.

**Id check.** The spec's `grep -oE 'S[0-9](3,)'` matches nothing (an ERE group, not an interval);
`grep -oE 'S[0-9]{3,}'` ends at S296, so the next free ids are S297 and S298. Neither is used: the
sources are held, not new.

**Census.** `bash scripts/sources-census.sh validate … --today 2026-11-04`: exit 0, `ok`, no
E-codes, 23 W04 warnings (the pre-existing set). `census`: 202 rows, tier A 184, B 10, C 8,
mined 183, rejected 19 (`census-validate.txt`).

**State.** `corpus/SOURCES.md` is HEAD `e0c19339` plus two uncommitted rows (mtime
2026-11-04 10:05:56 -0300); both holding rows postdate the freeze, so the round's frozen artifacts
do not contain them.

## Rows draft

### Append

None — refused reuse. `https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html` is
held by S295 (`corpus/SOURCES.md:212`) and `https://mutants.rs/` by S296 (`corpus/SOURCES.md:213`).
The registry's next free ids are S297 and S298 (max held S296); they are deliberately unused, because
a held URL is not a new row.

### In-place repair of the uncommitted S296 row (not an append)

S295 needs no repair: anchor, quote, count (18 words) and line (97) all reproduce against the fresh
snapshot, and the sha256/byte count in the source cell match byte-for-byte.

S296 carries two cell defects.

**Defect 1 — anchor word count.** The quoted text is 15 words, not the 17 the row states.
`quality by finding places where bugs can be inserted without causing any tests to fail` → 15
whitespace tokens. The cited range 184-186 is the span of the 21-word full sentence, which is the
clean repair: widen the quote to the sentence and state 21 words. The alternative (keep 15 words,
range 185-186) also forces an edit to the knowledge entry that repeats 184-186 at line 1.

**Defect 2 — scope/teaches vocabulary.** The Welcome page has no standalone "mutant" (all 13
occurrences are the product name "cargo-mutants" or its URLs) and no "kill"/"survive" (0 each). The
cells should state the page's own claim — bugs can be inserted without causing any tests to fail —
and attribute the kill/survive rule to the instrument.

The repaired row (11 columns, no cell contains a pipe; Option A):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S296 | cargo-mutants book, Welcome — https://mutants.rs/ (snapshot `cargo-mutants.html`, 22 602 B, sha256 `d056b2b3580903a000f3b7852a85768c61ac190e5da70690281f5175f4a2ec6d`, in `.ufo/waves/round-79/l1/sources/`) | docs | B | Bug-insertion vocabulary as the page states it: a program can have bugs inserted without any test failing, and finding those places is the tool's stated purpose; the page uses neither "mutant" as a noun nor "kill"/"survive" | Welcome to cargo-mutants, snapshot lines 184-186: "It helps you improve your program’s quality by finding places where bugs can be inserted without causing any tests to fail" (21 words); fetched 2026-11-04, HTTP 200 | The page supplies the survivor premise the battery's rule rests on in `tools/round-79/gate-mutation.py` (a defect that no test failure catches); the kill/survive wording is the instrument's, not the page's. Tier B: a tool's book, not the technique's specification. | mined | 2026-11-04 | 180d | corpus/knowledge/2026-11-04-r79-mutation-and-pointers.md |

Minimal alternative if the L1 prefers the shorter quote (keep the 15 words, change two tokens):
`snapshot lines 184-186:` → `snapshot lines 185-186:` and `(17 words)` → `(15 words)`; the knowledge
entry's line 1 then needs the same range correction.

## State facts the record must not lose

- `corpus/SOURCES.md` at the working tree is `HEAD e0c19339` **plus two uncommitted rows**
  (mtime 2026-11-04 10:05:56 -0300): `git diff --unified=0 HEAD` shows `@@ -211,0 +212,2 @@` and
  nothing else.
- `git show a1f9b81:corpus/SOURCES.md | grep -c S296` → **0**; `git show
  ed68cd0a:corpus/SOURCES.md | grep -c S296` → **0**. The rows postdate both the declaration and
  the freeze.
- `tools/round-38/registry-immutable.sh` enforces CORPUS rule 2 for rows *present at base*: only
  `status`, `recheck` and `used-by` may differ at rev. Because S295/S296 are not base rows yet,
  their cells can still be repaired; after the L1 commits them, the anchor and scope are frozen.
- **Concurrency.** The L1 is landing the round-79 record in the same working tree while this
  seat ran: `SCORECARD.md` (mtime 10:09:04), `SKILL.md` (10:07:25), `corpus/QUALITY.md`
  (10:07:18) and `corpus/README.md` (10:06:15) are modified against HEAD; none was written
  by this seat. The duplicate check therefore names its object — `corpus/SOURCES.md`
  sha256 `3b7f44f6…`, 232 495 B, mtime 10:05:56, 202 rows — and that digest was unchanged
  from before the first grep to the end of drafting (13:11:41Z).
- **Frozen-instrument drift (out of this seat's scope).** `tools/round-79/pointer-bind.py` is
  modified against the freeze `ed68cd0a` (+6/−3, mtime 10:11:49, `--rev` now implies battery
  mode); this seat did not author the edit and did not measure behavioural equivalence. Any
  audit pinning the R79-C2 instrument at the freeze sees a different file in the working tree.
- The holding rows' `used-by` target `corpus/knowledge/2026-11-04-r79-mutation-and-pointers.md`
  exists and restates the S296 range `184-186` at line 1.

## Gates run

| gate | command | exit | result |
|---|---|---|---|
| `validate` | `bash scripts/sources-census.sh validate /home/vgpnk/Projects/shokunin/kaidoku-shokunin --today 2026-11-04` | 0 | ok; no E-codes; 23 W04 warnings (pre-existing set, unchanged) |
| `census` | `bash scripts/sources-census.sh census /home/vgpnk/Projects/shokunin/kaidoku-shokunin --today 2026-11-04` | 0 | rows 202; tier.A 184; tier.B 10; tier.C 8; status.mined 183; status.rejected 19; missing 0 |

No `tools/round-79` instrument was run: this seat drafts and verifies sources, it does not
re-run the battery or the pointer binder. The 23 W04 warnings are the pre-existing set (the
round-78 lesson recorded the same 23 at 197 rows); no E-code fires on the two new rows, their
ids are unique, and their `used-by` path resolves on disk.

## Findings

| id | severity | finding |
|---|---|---|
| F79S-1 | blocking-for-append | Both target URLs are already held: pubs.opengroup.org … grep.html at corpus/SOURCES.md:212 (S295) and mutants.rs at :213 (S296). Pre-append duplicate check therefore refuses both; no rows drafted for append. |
| F79S-2 | provenance | The two holding rows are uncommitted: present at neither the declaration a1f9b81 nor the freeze ed68cd0a (`git show <rev>:corpus/SOURCES.md \| grep -c S296` = 0 each). corpus/SOURCES.md is HEAD e0c19339 + 2 lines, mtime 2026-11-04 10:05:56 -0300. Any record that treats S295/S296 as frozen content would be wrong. |
| F79S-3 | defect | S296 anchor word count is 17; the quoted text is 15 words (21 for the full sentence). Neither reading yields 17. |
| F79S-4 | defect | S296 anchor line range 184-186 is the span of the sentence's full form; the quoted substring starts at 'quality' on line 185. Range and quoted text are inconsistent. |
| F79S-5 | defect | S296 scope/teaches credit the Welcome page with mutation-testing vocabulary it does not carry: 13 'mutant' occurrences are all the product name or its URLs, 'kill' 0, 'surviv' 0. The page's claim is 'bugs can be inserted without causing any tests to fail'. |
| F79S-6 | propagation | corpus/knowledge/2026-11-04-r79-mutation-and-pointers.md:1 repeats 'snapshot lines 184-186' for S296; the recommended repair (21-word quote) keeps it true, the 15-word alternative breaks it. |
| F79S-7 | tooling | The spec's id command `grep -oE 'S[0-9](3,)'` returns nothing: in POSIX ERE parentheses group, so the pattern looks for the literal text '3,'. Corrected `grep -oE 'S[0-9]{3,}'` ends at S296; next free ids S297/S298. The spec's proposed ids S295/S296 are both occupied. |
| F79S-8 | window | tools/round-38/registry-immutable.sh enforces CORPUS rule 2 for rows present at BASE (only status/recheck/used-by may differ at REV). S296 is not present at base, so it can still be repaired before commit; once committed, the anchor and scope cells are frozen. |

## Out of scope

- No lane edit was made; the L1 lands every row and the Gate block.
- No instrument was run (gate-mutation.py, pointer-bind.py); this is a drafting/verification seat.
- No commit, push, stash or checkout; no git write of any kind.
- SOURCES.md has no `## Gate` section at this revision (the round-78 Gate block lives in corpus/lessons/round-78.md), so the draft's placement is the L1's decision.

## Artifacts

All under `.ufo/waves/round-79/w1/ScribeSources/`:

- `grep-posix.html` — 21 316 B, sha256 `9473205c…d531`
- `cargo-mutants.html` — 22 602 B, sha256 `d056b2b3…ec6d`
- `receipt.json` — the acceptance receipt (`snapshots`, `quotes`, `duplicate_check`, `next_ids`,
  `rows_draft`, `gate_block_draft`, plus `gates`, `state_facts`, `findings`)
- `pre-append-url-check.txt` — verbatim duplicate-check, id and row-count commands with output
- `quote-check.txt` — verbatim quote span, word count, contiguity and page-vocabulary audit
- `census-validate.txt` — `validate` and `census` runs, exit codes and TSV output

Report: `.ufo/waves/round-79/w1/ScribeSources.md`

## Tooling

No tool was installed or upgraded (no `pacman` transaction; no `uv`/`npx` needed). Used as
present: `bash`, `curl`, `grep`, `sha256sum`, `cmp`, `python3`.

## Remaining risks

- If the L1 commits S296 unchanged, the 17-word count, the mismatched range and the imported
  vocabulary become immutable under CORPUS rule 2 until a documented correction round.
- If the L1 adopts the 15-word Option B instead of the 21-word Option A, the knowledge entry at
  `corpus/knowledge/2026-11-04-r79-mutation-and-pointers.md:1` must change in the same commit or
  the two records disagree about the same snapshot.
- The instrument side of the working tree is moving too: `tools/round-79/pointer-bind.py` changed
  after the freeze. If the round's record cites the freeze pin while the working tree carries
  a different instrument, the claim's provenance needs an explicit re-pin or revert note.
- The working tree is moving under the L1: if `corpus/SOURCES.md` is rewritten after this
  receipt (`3b7f44f6…`), re-run the commands in `pre-append-url-check.txt` against the
  new digest before landing, and re-check that S296 still reads as drafted here.
- A re-fetch on another day may serve different bytes; the sha256 here is the 2026-11-04 body and
  matches the registered snapshot, so the rows stay anchored to the same object.
