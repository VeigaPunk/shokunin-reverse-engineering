# ReviewerRepairs — repairs-draft review (append-only discipline, red-before, R68-V1..V6)

Seat: `ReviewerRepairs` (reviewer, r69-w1, leaf). Scope: the repairs drafts for the six defects routed
by the round-68 non-author closure (`corpus/lessons/round-68-verifier-spotcheck.md` §5), reviewed
against `CORPUS.md`, `corpus/QUALITY.md` and the filed bytes. Measured 2026-11-03 23:33-23:44 -03:00
at lane HEAD `3f3d20fc065b5be62f676028b9a38d316ddfe8fd` plus the live worktree (the L1's landing in
flight). Drafts reviewed: `w1/ExecRepairs/repair.md` (+ `evidence/`, `prefile-check.patched.sh`),
`w1/ExecLedger/v1-correction-block.md`, `w1/ExecLedger/v2-index-row-move.md`,
`w1/ExecLedger/v5-supersede-row.md` (+ `evidence/`), and the already-landed worktree edits
(`corpus/knowledge/2026-11-03-r68-packed-elf-route.md`, `corpus/README.md`, `corpus/SOURCES.md`,
`tools/round-29/prefile-check.sh`, `LOG.md`, `corpus/QUALITY.md`).

Attribution (**observation** + **inference**): every modified tracked path is the L1's landing in
progress, not a seat write. Both executor seats independently record this (ExecRepairs §3.5 captures
the third-party prefile edit "as-found"; ExecLedger labels the worktree "L1 landing in flight"), and
neither seat's wave dir claims a tracked-path write. I reviewed the worktree bytes as the
landing-under-review; attribution is resolved by the L1's own landing act.

Every fix verdict below is grounded in commands I ran or receipts I read; hashes quoted were
re-computed by me unless marked otherwise.

## Verdict table

| defect | draft source | verdict |
|---|---|---|
| R68-V1 provenance trio | ExecLedger v1 block; landed variant in the r68 entry | **ACCEPT shape / REVISE receipt** — the missing red/green must be the unanchored occurrence count (QUALITY #101), not the anchored grep |
| R68-V2 index row move | ExecLedger v2 note; landed move | **ACCEPT move / REVISE one byte** — the landed delimiter `|---|---|---|` breaks the GFM table; restore 4 cells |
| R68-V3 prefile PASS receipt | none | **OPEN** — filing-time obligation, correctly named in the LOG carry-in; not yet executed |
| R68-V4 prefile script + LOG line | ExecRepairs repair.md | **ACCEPT** — land exactly one variant; append the §5 LOG correction before filing |
| R68-V5 S269 word-count label | ExecLedger S271 package vs landed reason-path | **DECISION REQUIRED** — two mutually exclusive conformant packages; recommend S271 (QUALITY #93's letter) |
| R68-V6 report erratum | none | **ACCEPT-AS-SCOPED** (report-only, correctly no lane artifact) — erratum text pending in the round-69 report |

---

## R68-V1 — ACCEPT the block's shape; REVISE the receipt

What landed (`git diff HEAD -- corpus/knowledge/2026-11-03-r68-packed-elf-route.md`): a pure EOF
append (+21 lines, filed text untouched — append-only ✓). The trio lands as backticked list items
(`- \`source:\``, `- \`verified-at:\``, `- \`recheck:\``), exactly QUALITY #101's correction shape and
the shipped r67 precedent (`2026-11-03-r67-avm-le-squashfs-core.md:49`). Content re-derives: S269 sha
`4dc547ed…` matches the row and my own fetch record reads; `verified-at` names the landing
`978436bdc533…`, which is the r68 record's landing. The new r69 entry passes QUALITY #112's write-time
check (line-start trio at its lines 1-8 — verified by read).

**REVISE — the red/green receipt is the wrong checker.** The spot-check's evidence and M69-2 both cite
`grep -nE '^(source|verified-at|recheck):'` (anchored). Against list-item fields that grep **can never
turn green**: `- \`source:\`` does not start with `source:`. QUALITY #101 binds the correction-shape
receipt explicitly: it "greps unanchored and states that the count is occurrence-based, not
line-anchored". Note also that the CORPUS sweep recipe `grep -rlE '^[-* ]*recheck *:'` does **not**
match the backticked form either (a backtick sits between the `[-* ]*` prefix and the field), so it is
not a green check here either; QUALITY #112's anchored check is write-time and applies to **new**
entries only. Exact receipt wording to commit (wave evidence or the M69-2 fix cell):

```text
red (before, at 3f3d20fc): grep -c '`recheck:`' corpus/knowledge/2026-11-03-r68-packed-elf-route.md
  → 0, exit 1   (same for '`source:`' and '`verified-at:`')
green (after the append):   the same three commands → 1 each, exit 0
  count is occurrence-based, not line-anchored (QUALITY #101)
```

## R68-V2 — ACCEPT the move; REVISE one byte (delimiter)

The move is sanctioned by the routing ("move the row after the delimiter and log the correction in the
next round") and executed correctly: the r68 row leaves its paragraph position above the header and
re-enters byte-identical as the first body row; the r69 row joins it; the correction is logged
(M69-5). ExecLedger's scratch mirror proves the pure-move target parses (`e865a0dd…`: header 4,
delimiter 4, 121 rows ok, `<table> 1`).

**REVISE — the landed worktree shortened the delimiter to three cells** (`|---|---|---|` under the
4-cell header `| entry | topic | source | verified-at |`). Under GFM a header and delimiter with
different cell counts is not a table: ExecLedger's strict parse (markdown-it-py 4.2.0, gfm-like,
`evidence/table-parse.txt`) reads the worktree block 118-241 as CELL-COUNT MISMATCH and the knowledge
window renders `<table> 0 … first tag <p>` — the r68 entry is still not in a parsed table, i.e. V2 is
not yet repaired in the landing. My own read of `git diff HEAD -- corpus/README.md` confirms the
delimiter hunk. Exact fix (one byte, from `v2-index-row-move.md`, mirror `eb459258…`):

```text
corpus/README.md, the delimiter line directly under the header (worktree line 119):
  |---|---|---|      →      |---|---|---|---|
Nothing else changes. Post-fix parse: header 4, delimiter 4, rows 122 ok; window renders <table> 1, <th> 4, <td> 12.
```

Also update M69-5's fix cell: "the check is the table shape (`sed -n` header/delimiter/row order)" is
an order-only check and **passes the broken state**; the check that would have caught the defect is a
cell-count parse (header cells = delimiter cells). Name it.

Scope note: the pre-existing malformed material (coverage-map continuation at 90-111, single rows
113/115, Lessons table 243-272 with body widths [3, 4]) is present at HEAD, unchanged by this repair,
and correctly recorded as out of scope rather than silently fixed.

## R68-V3 — OPEN (filing-time obligation)

No PASS receipt and no recorded deterministic rerun exists yet; the corrected script **is** the
deterministic command, and the LOG carry-in names the target ("a committed prefile receipt at the
ticket tree"). The red state already exists and is committed: the two r68 receipts
(`.ufo/waves/round-68/w1/ExecLedger/evidence/prefile-at-4b0892cd{,-final}.txt`) both show FAIL, and
the report's PASS was a paste. At filing the L1 must commit the PASS receipt (or the named command
plus its exit-0 output) at the ticket tree. An unrun check has not passed.

## R68-V4 — ACCEPT

The three defect measurements are receipt-backed and my own commands agree:

- ledger census (mine): 21 data rows, rounds 14-32, 34, 35, nothing after round-35; round-35's
  container is `claims-frozen.json` and its `claims.json` was removed at `13d7a815` — "stops at
  round-52" is false, "no row for any round 36-68" is exact.
- gate receipts (I read all four committed JSON receipts' fields): audited/exact/of =
  21/20/21 (`f78fc766`), 36/20/36 (`6ffa9ce1`), 36/20/36 (base `d7d9a62…`), 37/20/37 (`3f3d20fc`);
  `stray ["round-35"]`, exit 1 at each — "20 exact of 36 on every round from 53 on" is false as
  written, and the corrected comment's three-revision sentence is exact.
- unreachable branch (mine): `git show` failure leaves stdout empty; `sha256sum` of empty input is
  `e3b0c442…`, so `${got:-absent}` can never substitute — confirmed by ExecRepairs' fixture demo and
  by arithmetic.

Red-before/green-after (`evidence/redgreen.out`, sha `fb730f07…` — recomputed by me): on the
absent-blob fixture the orig prints the misleading `got e3b0c442…` and the patched prints
`got absent`, exit 1 in both — the named diagnostic defect goes red→green with the fix as the only
delta; pinmatch and changed fixtures are byte-identical orig-vs-patched (no regression); `sh -n` OK
both. This satisfies CORPUS "a fix is shown able to fail before it counts".

Two variants exist and agree on every fixture except the absent-case wording (`got absent` vs
`absent at <rev>` — cosmetic): the draft `prefile-check.patched.sh` (59 lines, `d19a6508…`) and the
as-found worktree edit (58 lines, `9a403dc1…`). The script is a tool, not a filed record — editable.
**Land exactly one** (repair.md §8 says the same); re-hash before landing as the draft advises.

LOG half: repair.md §5 supplies the append-only correction (dated `## … — correction:` heading plus a
one-line alternative), never rewrites `LOG.md:4137` — conformant with the routing and CORPUS. At
review time LOG.md has gained only the carry-in entry (append-only ✓); **the V4 correction line is
still pending and must be appended before filing**, else V4 lands half-done.

Draft nit, resolved: repair.md:251 and ExecRepairs.md:34 now state "52 → 59" (orig 52 at HEAD,
as-found 58, draft 59) — verified by grep; an earlier snapshot's "57 → 59" is gone.

## R68-V5 — DECISION REQUIRED (recommend S271)

Two mutually exclusive, individually conformant packages exist:

- **Path A (currently landed everywhere):** recorded reason, no superseding row. Lives in the lesson
  `## Gate` ("S269 is not superseded: … a superseding row would duplicate the same URL and scope while
  carrying no new claim — the label is a miscount, not a claim drift") and in the r68 entry block's
  final paragraph. Satisfies the routing's second option ("or a recorded reason to leave the label");
  append-only holds; S269 stays byte-identical. **Cost:** QUALITY #93's letter says a routed
  SOURCES-row defect "is closed **only** by a new row whose `teaches` opens `supersedes S0NN —` … in
  the round that receives the routing or the next one", and its closure check
  (`grep -c 'supersedes S0NN —'`) will count R68-V5 **open** at every future closure unless an
  exception is recorded.
- **Path B (drafted, unlanded):** `v5-supersede-row.md`'s S271 (teaches opens exactly
  `supersedes S269 — `, 11 cells matching S269/S270, no inner pipes, explains the hyphen-split
  arithmetic that produced 11; `evidence/row-s271.txt` format checks) + the r68-lesson appended
  correction + the r69-lesson bullet. Satisfies the routing's first option **and** #93's letter; used-by
  dependency on the V1 block is correctly conditioned. **Cost:** duplicates URL/scope (the lesson's own
  argument), and requires retracting the landed reason sentences.

**Recommendation: Path B.** It satisfies both the routing and the standing criterion; #93 exists
precisely so a closure can count routed SOURCES defects closed. If the L1 keeps **A**, it must append
a dated exception line (lesson `## Gate` or a QUALITY amendment) stating that #93's superseding-row
mechanism is not applied to this label-nit and why — otherwise every future closure flags V5 open. If
the L1 switches to **B**, replace the entry block's final paragraph and the lesson Gate's V5 paragraph
with S271 pointers; exact replacement for the entry block:

```text
Label correction: the S269 anchor cell in `corpus/SOURCES.md` says the quote is 11 words; `wc -w` on
the quote is 10 (round-68 closure R68-V5). The correction is filed as S271, whose `teaches` opens
`supersedes S269 — `; S269 stays byte-identical.
```

Either way: exactly one package; the measurement itself (10 vs 11) is red-before-committed twice over
(word-count.txt here; the filed spot-check §5), so the fix can fail.

## R68-V6 — ACCEPT-AS-SCOPED (report-only)

The routing says "report erratum in the next round's report, or a LOG note; **no artifact change**" —
so the absence of a lane artifact is correct, and no append-only question arises. OPEN at filing: the
erratum (report prose said "two of them corrected" of the four registry rows; both advisory-derived
texts are in the one `SKILL.md:1861` packed-elf row) must appear in the round-69 report or a LOG note.

---

## Cross-cutting observations

- **QUALITY #112 landed** and matches both citations (lesson M69-2, ExecLedger v1 block); #113/#114
  also landed for the r69 findings that cite them. No ghost criteria remain.
- **Gate word counts now correct.** The reworked S270 Gate row quotes are labelled (4 words) and
  (5 words) and the upx.1 secondary-locator line (6 words); I re-derived all three with `wc -w` —
  `fprintf(f, "upx %s\n", UPX_VERSION_GIT_DESCRIBE);` = 4, `if (strcmp(argv[i], "--version") == 0)` =
  5, `--version: print the version of UPX` = 6. An earlier draft snapshot labelled the upx.1 line
  "(5 words)"; it was corrected in-draft before filing, so no filed byte carries it. M69-3's rule
  ("the count is computed before the row is written") is being followed.
- **S270 was reworked in place pre-landing** (doc/upx.1 manual page → src/help.cpp + src/main.cpp,
  kind docs→code). Legitimate: the row has never been a filed byte (uncommitted landing); the lesson
  Gate row and the r69 entry's `source:` were updated in step (shas `0b893ca8…`/`a02c7cba…` match the
  landed row).
- **SOURCES worktree census (my run):** 177 rows, malformed 0, duplicate ids none. The +2 lines are
  the S270 row and one blank line before `## Paths`; S269 is byte-identical (not in the diff).
- **PROVINCE.md +8** is a pure append (r69 Core section + frontier note) — outside my six defects;
  noted for the L1's no-harm ledger.
- **LOG.md** has gained only the carry-in entry so far (append-only ✓); V3/V4/V6 items ride the
  landing/close entries.
- No tool installs or upgrades were recorded by either seat, and I installed none (observation).

## Residual risk and verification gaps

- I did not re-run the strict Markdown parse, the three git fixtures, or the round-24 gate myself. I
  verified the committed evidence by hash (patched `d19a6508…`, redgreen `fb730f07…`, patch.diff
  `08e1c43f…`), read all four gate receipts' audited/exact/of/stray/exit fields, and re-derived the
  ledger census and the word counts with my own commands. The parse verdicts rest on ExecLedger's
  committed receipt plus my direct byte-level read of the delimiter hunk.
- V3 (PASS receipt), the V4 LOG correction line, the V5 decision, and the V6 erratum are all
  filing-time obligations that had not landed at 23:44; each is named above with its exact wording or
  its source draft. Unrun checks have not passed.
- The r69 claims (C1/C2/C3) themselves are outside this ticket (ReviewerGates/CriticClaims scope); I
  reviewed repairs discipline only.
