# R45W2Distill — distillation of the round-45 wave-2 falsifications

Seat `R45W2Distill` (critic, leaf — no subagent). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
read-only. Freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`; landing
`e715263cb51b713c342ab992d527fe9d61d6f8ff`; A1 `1f4b27f8`; A2 `fedd11bf`; A3 / measured revision
`f59565b782c18b0eb691bec12f52d2f80d9f5032`; lane HEAD observed `a63d109f`.

**Snapshot: 2026-10-28T16:18:44Z.** Every `report.md` under `.ufo/waves/round-45/w2/` with mtime
≤ `2026-10-28T16:09:42Z` is read below. Finding ids are `<Seat>#<the seat's own local id>`; where a
seat used prose rather than ids I name its section. Nothing here re-verdicts a seat's work: the
groups are the L1's sort key.

## 0. What I read (coverage, stated not implied)

| item | count | detail |
|---|---|---|
| wave-2 seats in `w2-spec.json` / `w2-dispatch.json` | 36 / 36 | incl. this seat |
| peer seats with a published report (`<Seat>/report.md`) | **34 of 35** | `R45W2Immutable` still `running`, no output, no dir |
| reports read in full for their verdict/finding sections | **34** | 4 have no verdict table (`Log`, `Misroot`, `MutC1Landing`, `MutC2Landing`) and were read by headings + findings |
| flat `<Seat>.md` byte-identical to `report.md` | 32 | convention holds |
| flat `<Seat>.md` a 3.7 KB **trailer** pointing at `report.md` | 2 | `R45W2PreflightReal` (3785 B vs 14270 B), `R45W2SecShell` (3741 B vs 20504 B) — a reader that reads only the flat file gets a pointer, not findings |
| reports with zero findings of any class | 2 | `R45W2Scorecard` (all 9 numbers re-derived, all hold), `R45W2SecWrite` (write scope holds; only hygiene notes) |
| seat-declared "not run" items | 9 | `RevSweepPath#A2,#A8`; `Misroot` four items; `SecShell#A3,#C6`; `Src140#A9`; `Waves#V12`; `Log#F7`; `NoTmp#A11`; `SecWrite` n/a |

I executed five checks of my own (receipts in `receipts.tsv`): `c1-counter` at A3 (exit 0, all six
fields equal to `l1/scores/c1-at-A3.json`); `c2-counter` at A3 (exit 0, `registered` = six,
`unregistered []`, `thin []`); `frozen-path-preflight --selftest` (exit 0, `cases=11 failures=0`);
and the row-10 adjudication fixture (§5.1). I did **not** re-run Command A, the seats' mutation
suites, or any seat's scratch fixture.

## 1. Classification rule (so the groups are falsifiable)

- **(a) claim-falsifying** — would change a claim verdict (`met`/not), an axis score or label, or a
  recorded before/after value the verdict rests on.
- **(b) instrument-defect** — a defect in an instrument's or the landed artefact's *behaviour*; real,
  routable, verdict unchanged.
- **(c) record/format** — record wording, numbers, pointers, formats; verdict unchanged.
- **(d) duplicate** — restates an already-routed `R45-CL*` finding or another seat's finding; first
  occurrence named.

| group | unique findings | seats contributing |
|---|---|---|
| (a) claim-falsifying | **2** | 1 |
| (b) instrument-defect | **30** | 21 |
| (c) record/format | **22** | 19 |
| (d) duplicates | **17 routed ids restated + 16 within-wave clusters** | 25 |

**Headline for the L1.** No seat found a falsification of either claim *predicate*: 11 independent
seats reproduce exit 0 / `met_target true` at A1/A2/A3 with the recorded field values, and both
mutation-testing seats say so explicitly in their own words (`MutC1Landing` §4.3 "what survived that
would *falsify* the landed artefact: **nothing**"; `MutC2Landing` §5 "the landed R45-C2 target is
**not falsified** at any recorded revision"). What the wave did find is (i) two overstated trend
labels, (ii) a large instrument/routing debt including three classes no wave-1 id names, and (iii)
a record whose numbers are right in the cells and wrong in the sentences that summarise them.

## 2. (a) Claim-falsifying — 2

| id | attack | verdict | why it would change a verdict |
|---|---|---|---|
| `Trends#quality-improved` | `SCORECARD.md` "Learning trends: quality **improved**" | **overstated** (falsified as worded) | Two of its three named supports are not improvements: "an instrument registry that now covers every claim-carrying tool" is the *calibration* axis, and "the depth proxy held at 22/22" is a hold at the ceiling (`depth_score 10.0` at base and at A3). The third cannot be read off the proxy at all. A trend **label** is a verdict of the round's record; accepting this forces the label to change. |
| `Trends#discernment-improved` | `SCORECARD.md` "discernment **improved**" | **overstated** (falsified as worded) | Two of three acts hold on live bytes, but the third slot is filled with a non-defect (the A1 self-catch) where `R44-CL10` belongs; `R44-CL10` is only partially adjudicated and its restore case is not arm-isolating. Same reason as above. |

**Verdict-adjacent, does not flip (kept in (b) deliberately).** `C1Rerun#E` / `PathspecArm#P-1`: the
gate's history arm is scoped by `--pathspec`, so with a *subset* pathspec a tampered-then-restored
frozen file reads `clean` (exit 0) where block 22 row 2 declares exit 1. It does not flip
`met_target` (the predicate's clause 6 is the interpreter's `--selftest`, which still passes), but if
the L1 reads block 22's rows as part of the claim ("arms are proven red"), this is the single (a)
candidate in the wave. See §5.2 for why I do not so read it.

## 3. (b) Instrument-defect — 30

Grouped by target. "NEW" = no `R45-CL1..CL17` id covers it; "routed" = an existing id covers it and
the row is the corroborating receipt.

| id | target | finding | status |
|---|---|---|---|
| B1 | preflight `covers()`/history scope | a pathspec **inside** the frozen dir is accepted as coverage and narrows commit+blob arms: `--pathspec tools/x/sub/ --freeze-path tools/x` → exit **0 clean** with `tools/x/a.txt` tampered then restored (`PathspecArm#P-1`); the live-lane single-file pathspec returns exit 0 too (`PathspecArm#W1/W2`); same behaviour from `C1Rerun#E` (fixture shaped like this round's own two frozen paths, `GATE_EXIT=0`, `GATE_EXIT_BOTH=1`) | NEW (HIGH) |
| B2 | preflight `covers()` direction | a **parent** pathspec that does cover the frozen dir is refused with exit 2, byte-identical to the no-pathspec receipt (`PathspecArm#P-2`, `ReviewPreflight#F2` `a6-covers-parent` 2 `dc5a4a97388b`) | NEW |
| B3 | preflight `covers()` | a **descendant file** pathspec yields a false clean: `a6b-covers-file` exit **0** (`267b6a1b2c67`) while control `b8` (full pathspec) exits 1 (`ReviewPreflight#F1`) | NEW |
| B4 | preflight `git replace` | `git replace` rewrites what `log`/`rev-parse` read: gate exits **0 clean** on a repo whose frozen file changed (`SentPreflight#F1`) | NEW (HIGH) |
| B5 | preflight pathspec-requirement | with **no** pathspec on a **clean** tree the gate reports `frozen_path_changed` (false red) (`SentPreflight#F2`) | NEW |
| B6 | preflight pathname encoding | non-ASCII paths: the arm's `text=True` decode raises `UnicodeDecodeError` → exit **1** with empty stdout instead of exit 2 with a receipt (`Src140#A7`); the C-quoted record `"\"frozen/\\303\\274.txt\""` never equals a real path, so the `restored` arm is dead for it and `blob_changed` names a directory for an absent file (`Src141#A10`, `ReviewPreflight#F3`); U+2028 truncates the recorded path (`SentPreflight#(c)`) | NEW |
| B7 | preflight dirty arm | `--check-dirty` is blind to `--assume-unchanged` and `--skip-worktree` (`a9-assume-unchanged` 0 `439e10113b89`, `b5-skip-worktree` 0 `f496a458f51c`) (`ReviewPreflight#F4`) | NEW |
| B8 | preflight dirty arm | ignored content is invisible: an ignored file inside a frozen directory reads `clean` (`CommandA#V10`); the worktree gained `tools/round-45/__pycache__/*.pyc` **after** the freeze with both counters still exit 0 (`SweepAudit#A8`); ignored untracked content limit (`ReviewPreflight#F5`) | NEW (low–med) |
| B9 | preflight receipts | an untracked directory collapses to one `touched` entry, so the receipt undercounts the files it stands for (`ReviewPreflight#F6`) | NEW (low) |
| B10 | preflight classifier | mode-only tamper (`100644`→`100755`, content never edited) is reported in **`restored[]`** while the entry at REV still differs from FREEZE — contradicts row 2's "restored to its FREEZE bytes" (`RestoredArm#A5`) | NEW (med) |
| B11 | preflight history model | tamper+restore folded by `git merge --squash` reads exit **0 `clean`** (`RestoredArm#A6`) | NEW (med) |
| B12 | c1-counter exit column | the exit cell is **domain-checked, never compared with the arm**: flipping the `touched` row's `1`→`2` scores exit 0, `met_target true` (`MutC1Landing#m3b`) — the seat states no routed id names this class | NEW (routed as a round-46 re-freeze item) |
| B13 | c2-counter scope | the counter parses **any** pipe line in the whole file: rows under no registry heading, inside an HTML comment or a fence, register (`ReviewC2#A2`, `CritC2Text#A3`); 21 of the 45 rows it counts come from a 7-column table with **no delimiter row** (`ConnFormat#F5`, provenance `receipts/row-provenance-at-a1.txt`) | routed (CL14 a, CL9 A3) + NEW (F5) |
| B14 | c2-counter separability | a block-22-shaped table whose cell 2 is `0, 1, 2` registers as a C2 row: `met_target true` (`CritC2Text#A6`, stdout `156f1477…`) — the claims file's "it never reads block 22 / either lands without the other" is false | NEW |
| B15 | c2-counter selftest | the exit-2 "freeze is not an ancestor" arm is live and correct (exit 2, `c1b9db74…`) but **no selftest case covers it** (`CritC2Text#A7`) | NEW (gap) |
| B16 | both counters, `scope_size` | `scope_size` is a list length, not a distinct set: one path repeated six times satisfies it (`C2Rerun#A13`, `ReviewC2#A6`, `FreezeBytes#V15`); frozen file itself is clean | routed (CL9 A5 family) |
| B17 | c1-counter citation arm | `REF` validates only `corpus/{knowledge,lessons}/**` and `plans/**`, so `SKILL.md:99999`, `LOG.md:9999`, `tools/…:7` are invisible to both the count and the resolution arm; line-less refs count as refs (`C1Rerun#F`, `CritC1Text#F2/#F3`, `ReviewC1#4`, `MutC1Landing#m4b/#m4c`) | routed (CL9 A2, CL13 b) |
| B18 | c1-counter S140 clause | "cites `S140`" is a token test, not a row test (`CritC1Text#F4`) | NEW (refinement) |
| B19 | block 22 title | "every arm has a red case" is overstated: `blob` has no dedicated case; `restored`'s case does not isolate the arm (`Rollback#E4`, `CritC1Text#F5`, `Lesson#A3`) | routed (CL15) |
| B20 | c1-counter selftest case | `red-relabelled-21-block` tests the *count*, not the relabelling: 21 plain blocks score 1, 20 plain + 1 relabelled score 0 (`DoNothing#A6`) | NEW |
| B21 | both counters freeze arm | merge-introduced frozen touch is invisible: `git log --name-only` prints nothing for a merge; evil-merge fixture scores `met_target` (`FreezeBytes#V9`, `ReviewC1#B1`, `ReviewC2#A5′`, `CritC1Text#F7`) | routed (CL6) |
| B22 | preflight arms | the `touched` arm is a **third** non-isolating arm and the only arm the counters use; A3's disclosure names only `blob` and `restored` (`FreezeBytes#V10`) | NEW (extends CL15) |
| B23 | c1-counter block parsing | `craft_blocks` splits on `^- \*\*` anywhere, so a top-level bullet inside a rule body manufactures a block (2 markers/23 blocks read as 1/22, exit 0); a `## Queue-drain craft` heading without the trailing space raises `IndexError` → exit 1 empty stdout (`ReviewC1#1`) | routed (CL9 A1, CL13 e/f) |
| B24 | c1-counter header test | header cells are substring tests: one cell `triggeralarmexitreceipt` satisfies all four; a collapsed one-cell header plus ten `1` rows scores green (`ReviewC1#3`, `CritC1Text#F1`) | routed (CL13 c) + NEW (collapse probe) |
| B25 | c1-counter selftest binding | the "cases >= 11, failures == 0" claim is read from a script with **no sha256 pin**: a 4-line stub printing the line passes (`ReviewC1#5`, `MutC1Landing#m6c`) | routed (CL13 a) |
| B26 | c1-counter depth proxy | `22/22` is presence + line-bounds only: an unrelated knowledge file `:1-66` and the same file `:1-1` both score 22/10.0; only a past-EOF range drops it to 21/9.55 (`CommandA#V2`) | routed (CL13 b family) |
| B27 | frozen control receipt | `controls/preflight-at-freeze.json` is narrower than the claim's frozen set — it names only `tools/round-45`, not `plans/round-45-claims.md` (`C1Rerun#H`) | routed (CL10 family) |
| B28 | `--json-out` | unvalidated: `--json-out ../../SKILL.md` overwrites the graded surface (3/3, exit 0), overwrites a **frozen** path (incl. at exit 2), follows a symlink, and on an unwritable target exits **1** with empty stdout and no receipt where the contract says 2 (`SecShell#B1–B4` = CL19) | routed (CL19, coined by this seat) |
| B29 | environment redirection | `GIT_DIR=<repo>/.git` makes fixture commits land in the named repo and `GIT_INDEX_FILE` rewrites its index — including on the **scoring** run, which still prints `met_target: True` (`SecShell#C4/#C5` = CL18); `HYAKU_SCRATCH`/`TMPDIR` can point inside the scored tree (662 paths, 11 nested `.git`, exit 0) and a relative base resolves against CWD (`SecShell#C1–C3`, `SecShell#C6`, `SecShell#CL20`) | routed (CL18, CL20) |
| B30 | scratch/exit discipline | with both env vars unset the selftest fixtures are created under bare `/tmp` (docstring says "never a bare /tmp root") (CL21, `NoTmp#A4`); an unevaluable scratch state exits **1**, indistinguishable from a violation (contract says 2) (`NoTmp#A5`); the preflight's selftest never `rmtree`s its 11 fixture repos (400 files / 261 dirs / 316,981 B per run) (`NoTmp#A6`, `SecWrite` §1.2); `--root` never influences scratch, and an empty scratch dir written inside the tree is invisible to `git status --porcelain` (`SecWrite` §1.2) | routed (CL21) + NEW (A5, A6) |

Also in (b) but land in the block-22 *text* rather than an instrument: `C1Rerun#I` (row 4's exit
depends on `--check-dirty`, a flag named only in the receipt cell), `Rollback#E3` (row 6 is dead under
first-match and its receipt cell names fields the gate never emits), `RestoredArm#A5`/`Rollback#E2`
(rows 2 and 10 as written), `CritC1Text#F8`, `CommandA#V6` (row 5 narrow), `PathspecArm#P-2`
(claims `:136-137` "no pathspec covers it" / "a whole-tree scan is refused"). These are counted once,
in B1/B10 and in §5.1 — not double-counted in the 30.

## 4. (c) Record/format — 22

| id | site | finding | seats (first named first) |
|---|---|---|---|
| C1 | `SCORECARD.md:3581`, `:3591`; `LOG.md:3316` | "every value is identical at both" / "identical at `e715263c`, `1f4b27f8`, `fedd11bf` and A3" is **false on `block22_refs`**: 6 / 7 / 8 / 8 (`.ufo/waves/round-45/l1/scores/c1-at-*.json`). The table cell at `:3532` correctly quotes 7 *for its own revision*; the summary sentences do not | `Pins#A1`, `CommandA#V4`, `CommandA#V5`, `Log#F1` |
| C2 | `SCORECARD.md:3527-3528`; `LOG.md:3273-3275` | wave-2 seat count is **32**; spec, dispatch, registry and `.ready` all carry **36**, and `r45-w2-results.json` is absent in the worktree *and* at HEAD (the cited source for both counts does not exist) | `Pins#A2`, `Waves#V5`, `Waves#V6`, `Log#F2`, `SweepAudit#F1` |
| C3 | same lines | "Wave 1: 40 seats" is true of seats *allocated*, false of seats *delivered*: 25 reports / 25 dirs, 15 `output:null` with a never-spawned note | `Waves#V4`, `SweepAudit#A9` |
| C4 | `SCORECARD.md:3527` | section head still names `1f4b27f8` as the measured revision while `:3590` names A3; the **wave-2 dispatch inherits the stale value** ("A1 … the measured revision") so 24 of 36 seat prompts carry it; the fleet report's line 248 repeats A2 | `SweepAudit#F2`, `Waves#V14`, `CensusEnd` §5.1, `Misroot#5` |
| C5 | `corpus/lessons/round-45.md` S138 correction | the receipt it cites (`w1/R45W1SrcS138Fix/`) is **absent at every revision the round measured** (0 entries at `e715263c`, A1, A2, A3, `1d04c6af`; 1 at `0ee50aaf`), and the fetch it records is 15:39:00Z, after the 15:33:03Z landing | `S138Top#F1`, `Rollback#C2`, `Rollback#C3`, `Lesson#A4` |
| C6 | `corpus/SOURCES.md:144` (S138) | the correction's "the endpoint the `opened` cell names" does not match the cell (`2026-10-28`); two further clauses falsified | `S138Top#F2`, `S138Top#F3` |
| C7 | lesson Gate | "16 W04 warnings" at landing/A1 — measured **14** at both ends (repaired append-only at A2); S141 quote "(23 words)" at landing/A1 — measured **20** (repaired at A2) | `CensusEnd#4`, `CensusEnd#5`, `Src141#A3` |
| C8 | lesson Gate, S140 | the `15:31Z` fetch stamp appears only in prose; the retained fetches are 15:38:50Z / 15:41:04Z, both **after** the 15:33:03Z landing | `Src140#A9` |
| C9 | `corpus/SOURCES.md:146-147` | `used-by` lists only `corpus/lessons/round-45.md`; `SKILL.md` cites S140 twice and S141 twice, the gate docstring cites both, the claims file cites both, and registry precedent admits multiple consumers | `Src140#A5`, `Src141#A6` |
| C10 | lesson M45-1 | evidence pointer `.ufo/waves/round-45/w1/R45W1InhSweepEvidence/` **does not exist** (seat never spawned: host job-cap refusal); and "the lane's own commit helper never looked at the worktree" is false as worded — `scripts/hyaku/jj-lane.sh:721` does run `git status --porcelain --ignored -z -- <files>`, pathspec-limited | `Lesson#A4`, `Lesson#A5` |
| C11 | lesson M45-2 | evidence pointers ("round-44 closure routing item 4"; "the claim is in `round-44.md` `## Gate`") do not resolve; no artifact contains a numbered item 4 and round-44 `## Gate` (21–53) never says it | `Lesson#A7` |
| C12 | lesson M45-3 | `captured-by` names the prompt requirement, not a capturer (conformance, low) | `Lesson#A10` |
| C13 | `SKILL.md:607` | cites `corpus/lessons/round-45.md:12-17` for the operator/integrator placement limit; those lines are the Mistakes table — the limit is at **70–73** | `Lesson#A15` |
| C14 | `### Round-44/45 instrument registry` | 7 fields vs the house 8 (`entry command` absent); full path in cell 0 is a *minority* convention (Round-40 uses bare names, so the lane carries three cell-0 conventions); a **house-order row makes the lane's own C2 counter report `thin`** (two rubrics mutually exclusive); the section header sentence is stale (states A1 as measured) | `ConnFormat#F1`, `#F2`, `#F3`, `#F6` |
| C15 | `LOG.md` round-45 entry | "four red arms" vs five documented arms; the routed range conflates round-44 remainders with wave-1 findings; "Tools installed this round: none." stands against this wave's own installs (none made) — OK, but the sentence is a standing hazard; assimilation `none` not run | `Log#F5`, `Log#F3`, `Log#F6`, `Log#F7` |
| C16 | `FREEZE..main` | 8 of 12 commit subjects are uncited by any round record (completeness in the reverse direction) | `Pins#A3` |
| C17 | `corpus/SOURCES.md` at the freeze | 0 rows for S140/S141 at the freeze while the claims file names them 5 times — "rows opened this round" is true only from the landing onward | `CensusEnd` §5.2 |
| C18 | fleet report `.ufo/reports/round-45/kaidoku.md` | "shows three untracked fleet-root files" — observed **seven** `??` lines; "none names kaidoku" false over the whole set; **"no fleet-root file edited" false**: `.ufo/l0-questions.md` carries a two-line kaidoku append (worktree sha256 `bdbf1853…`, mtime 15:53:54Z) | `Misroot#1`, `#2`, `#4` |
| C19 | `plans/round-45-claims.md` §Sources | "the commit arm parses that" (the `-z` form) is false: the arm runs plain tab-split `--name-status` (line 93); the page states the tab separator only in the raw-format field list | `Src141#A8`, `Src141#A9`, `Src140#A8` |
| C20 | round ledger | `r45-w1-results.json` cannot be produced by the committed dispatcher (`inline-dispatcher.py:295` writes a different dead-seat note); exit 2 on who wrote it; the ledger schema has no `status`/error field, so "dead seats carry their last error text" is not run | `Waves#V13`, `Waves#V12` |
| C21 | `controls/ctl-c2-0-base-unevaluable.json` | not reproducible as recorded (reason string differs) and carries none of the fields its siblings carry | `Log#F4` |
| C22 | routed-id space | **`R45-CL5` is used for two different defects**: wave-1 `R45W1CritC2` §"For the L1" item 2 coined `R45-CL5` for merge blindness; the lesson assigns CL5 to "r44 counters exit 2 at the tip" and merge blindness to CL6 | distiller (verified: `w1/R45W1CritC2/report.md:238` vs `lessons/round-45.md:87-90`) |

## 5. Cross-seat contradictions I adjudicated

### 5.1 Block 22 row 10 — `MutC1Landing` says "10/10 rows right", `Rollback#E2` says "falsified"

Both are right about different invocations, and the row is **under-specified** rather than false.
My fixture (`receipts.tsv` rows `clean`, `dirty`): freeze == REV, frozen file clean →
exit **0** `clean` (sha `977669af…`); same freeze/rev, frozen file dirty, `--check-dirty` →
exit **1** `frozen_path_changed` (sha `563f0c94…`). Row 10 reads
`FREEZE equals REV (empty range) | all arms | 0 | verdict clean`; the dirty arm **is** an arm, so
the row as written is false for a dirty tree. `MutC1Landing`'s "10/10" was checked against a clean
worktree only. **Smallest correction:** qualify the row's trigger ("and no frozen path is dirty") or
drop "all arms". Same under-specification class as row 4 (`C1Rerun#I`).

### 5.2 `C1Rerun#E` / `PathspecArm#P-1` vs `MutC1Landing` §4.3 ("no falsification of the landed artefact")

Not a contradiction: `E`/`P-1` exercise a **subset** pathspec, which block 22's own prose forbids
("An invocation must name every frozen path … routed R45-CL10"). Under the documented invocation the
rows are true. What is false is that the *requirement is unenforced*: the gate accepts a subset
pathspec, and on the live lane `--pathspec tools/round-45/c1-counter.py` exits 0 with both frozen
paths named (`P-1` `W1/W2`). So the finding is real and lands in (b) as **requirement-not-enforced +
row 5's "covers" misimplemented**, not as a claim falsification. This is the wave's single most
consequential (b) item and the one I would put first in the report's disclosure list.

### 5.3 Record numbers: "identical" vs the table cells

`SCORECARD.md:3532` quoting `block22_refs 7` is **correct for its cited receipt**
(`c1-at-1f4b27f8.json` = 7); the false statements are the three *summary* sentences (C1). I checked
this because a wholesale "the record's numbers are wrong" reading would be wrong: re-derivation
agrees with every cell and with all nine `R45W2Scorecard` numbers.

## 6. (d) Duplicates

### 6.1 Routed wave-1 ids restated by wave-2 seats (17)

First occurrence is the wave-1 seat/finding the lesson names; "—" means L1-authored (no seat id).

| routed id | first occurrence (wave-1) | restated by (wave-2) |
|---|---|---|
| CL1 | — (L1; prompt §3) | `RevSweepPath#A1/#A3/#A5`, `Log`, `Trends` |
| CL2 | `R45W1CritC2` §Attack 3 (`tool_present_at_rev`) | `CritC2Text#A1`, `ReviewC2#A7` |
| CL3 | `R45W1RegScopeAudit` (a) → routed by L1 | `CritC2Text#A1` |
| CL4 | `R45W1CritC1` (class) → routed by L1 | `MutC1Landing#m7`, `DoNothing#A4`, `SecWrite` |
| CL5 | **id collision** — `R45W1CritC2` item 2 (merge) vs lesson (r44 tip) | `RevSweepPath#A6` |
| CL6 | `R45W1RevFreezeCommit#F1` | `ReviewC2#A5′`, `FreezeBytes#V9`, `ReviewC1#B1`, `CritC1Text#F7`, `DoNothing`, `Src140`, `Src141`, `SweepAudit#A5`, `Trends` |
| CL7 | `R45W1C1CounterMutants#m1/#m2` | `MutC1Landing`, `Log`, `Trends` |
| CL8 | `R45W1C2CounterMutants#m1/#m2` | `ConnFormat#F?`, `CritC2Text`, `Log` |
| CL9 | `R45W1C1SelftestFromFreeze` §4 A1–A6 | `MutC1Landing#m4b/#m4c/#m7`, `ReviewC1#1/#3/#4`, `CritC1Text#F2/#F3`, `C2Rerun#A13`, `SecWrite` |
| CL10 | `R45W1RevFreezeCommit#F2/#F3/#F4` | `PathspecArm`, `PreflightReal`, `C1Rerun#H` |
| CL11 | `R45W1SrcGitDiffTree#F3` | `Src141#A8/#A9`, `CritC1Text#F6`, `ReviewPreflight`, `Lesson` |
| CL12 | `R45W1SrcS138Fix#F1` | `S138Top#A2`, `Src140`, `Log` |
| CL13 | `R45W1CritC1` | `CommandA#V2`, `MutC1Landing`, `Pins`, `SecWrite`, `Trends` |
| CL14 | `R45W1CritC2` | `MutC2Landing#m4/#m5b/#m6/#m11`, `Pins`, `CritC2Text`, `ConnFormat` |
| CL15 | `R45W1PreflightArms` (`m2`, `x2/x2b`, §1.4) | `RestoredArm#A7`, `Lesson#A3/#A16`, `FreezeBytes#V10/#V12`, `CritC1Text#F5/#F8`, `SentPreflight`, `ReviewPreflight`, `Src140/141`, `Pins`, `CommandA`, `DoNothing` |
| CL16 | `R45W1RegR44C1Run` | `Pins#A8` |
| CL17 | `R45W1RegScopeAudit` (c) | `CritC2Text#A1`, `ConnFormat`, `FreezeBytes#V15`, `SweepAudit` |

### 6.2 Within-wave duplicate clusters (same defect, 2+ wave-2 seats, no prior id) — 16

| # | defect | first wave-2 occurrence (mtime) | later occurrences |
|---|---|---|---|
| D1 | "values identical" record sentence | `Pins#A1` 16:03:22 | `CommandA#V4`, `CommandA#V5`, `Log#F1` |
| D2 | wave-2 count 32 vs 36 | `Pins#A2` 16:03:22 | `Log#F2`, `Waves#V5`, `SweepAudit#F1` |
| D3 | pathspec narrowing / `covers()` false green | `PathspecArm#P-1` 16:04:17 | `CommandA#V6`, `C1Rerun#E`, `ReviewPreflight#F1` |
| D4 | first-cell `re.search` (not equality) | `C2Rerun#A3/A4` 16:04:35 | `ReviewC2#A3`, `CritC2Text#A4` |
| D5 | `thin` first-row-wins | `C2Rerun#A5` 16:04:35 | `ReviewC2#A1`, `CritC2Text#A5` |
| D6 | `scope_size` length not set | `C2Rerun#A13` 16:04:35 | `ReviewC2#A6`, `FreezeBytes#V15` |
| D7 | scoped citation regex / line-less refs | `C1Rerun#F` 16:04:46 | `ReviewC1#4`, `CritC1Text#F3` |
| D8 | flag-conditional exit (row 4/5) | `C1Rerun#I` 16:04:46 | `CritC1Text#F8`, `Rollback#E3` |
| D9 | merge blindness (also CL6) | `ReviewC2#A5′` 16:05:34 | `FreezeBytes#V9`, `ReviewC1#B1`, `CritC1Text#F7` |
| D10 | header substring / collapsed header | `ReviewC1#3` 16:06:00 | `CritC1Text#F1` |
| D11 | selftest binding with no sha256 pin | `ReviewC1#5` 16:06:00 | `MutC1Landing#m6c` |
| D12 | non-ASCII / C-quoted pathnames | `Src141#A10` 16:06:07 | `SentPreflight#(c)`, `ReviewPreflight#F3`, `Src140#A7` |
| D13 | C2 parses rows from any pipe line | `ReviewC2#A2` 16:05:34 | `CritC2Text#A3`, `ConnFormat#F5` |
| D14 | unevaluable state exits 1 not 2 | `NoTmp#A5` 16:04:17 | `SecShell#B4` |
| D15 | preflight leaves scratch fixtures | `NoTmp#A6` 16:04:17 | `SecWrite` §1.2 |
| D16 | `/tmp` fallback + write-scope cell wrong | `NoTmp#A4` 16:04:17 | `SecShell#C7` |

## 7. What the L1 should read first

1. **`(b) B1/B2/B3`** — the pathspec requirement is unenforced; this is the one instrument hole in
   the exact shape of this round's frozen set (§5.2), and it is the honest limit the A3 disclosure
   does not yet name.
2. **`(c) C1/C2/C4`** — three summary sentences the record's own receipts refute; one correction can
   cover C1's three sites (per `Log#F1`).
3. **`(a) Trends`** — two trend labels to soften or defend; this is the only (a) in the wave.
4. **`(b) B4/B6/B12/B13/B14`** — four classes no wave-1 id names (`git replace`, pathname encoding,
   unvalidated exit column, whole-file row scope + separability); route them as new ids and do not
   let them hide inside CL6/CL13/CL14.
5. **`(c) C22`** — `R45-CL5` is two defects under one id; fix before round 46 cites it.

## 8. Not run / limits

- `R45W2Immutable` had published nothing at the snapshot (still `running`, no dir). Its subject
  (registry append-only) is therefore unrepresented; `S138Top#A6` is the only wave-2 receipt on
  `registry-immutable.sh` and it reports `holds` base→A1/A3/tip.
- I did not re-execute any seat's fixtures, mutation suites, live fetches or Command A. Where two
  seats disagreed I built my own fixture (only §5.1) or read the record's own receipts (§5.3).
- `Src140#A9` (the 15:31Z stamp) is a "no receipt" finding: I did not re-fetch to invent one.
- Receipts for my five executions: `receipts.tsv` (label, exit, stdout sha256, UTC) plus the raw
  stdout files in this directory. Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W2Distill` removed after
  copying; nothing outside this seat's report directory was written. No installs.
