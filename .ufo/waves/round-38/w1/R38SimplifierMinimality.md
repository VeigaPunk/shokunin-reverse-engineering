# R38SimplifierMinimality — minimality review of the six drafted production patches

Seat: simplifier, wave 1, leaf (no subagents, no background jobs). Advisory: **no draft, counter,
carrier or oracle was edited**; every defect below is reported, not repaired. Nothing was written
outside this file.

Axes reviewed, in the seat's own terms:

1. **dead text** — sentences that are false or empty once the patch lands (seat state, draft paths,
   "not yet committed", `[L1-FILL]` scaffolding written as production prose);
2. **duplicated statements** — the same fact stated twice within one production surface, or repeated
   verbatim across two of them;
3. **scope containment** — content the frozen predicates do not read and the plan does not ask for;
4. **padding** — editorial sentences that carry no measurement, pointer or decision;
5. **preserved weight** — the counterpart check: lines that *look* like padding but are load-bearing
   for a frozen counter binding, a routed defect or a Gate rule, and must not be trimmed.

## 1. Drafts reviewed (exact bytes)

| surface | path (under `.ufo/waves/round-38/w1/artifacts/`) | sha256 (first 16) | bytes |
|---|---|---|---|
| entry | `R38ScribeEntry/entry.md` | `32f1c546139afe50` | 18 899 |
| SOURCES append block | `R38ScribeSOURCES/append-block.md` | `984bcc965396fea5` | 5 926 |
| PROVINCE patch | `R38ExecProvincePatch/patch.txt` | `c4564d111cd67884` | 6 012 |
| README patch | `R38ExecReadmePatch/patch.txt` | `c20b134cbe572dde` | 6 027 |
| SCORECARD + LOG section | `R38ScribeScorecardDraft/scorecard-section.md` | `f0166b3b7f6ce6b0` | 17 712 |
| lesson | `R38ScribeLessonSkeleton/lesson.md` | `5f161e5c0ca0208c` | 19 788 |

Total 74 364 B. All six were still being written while this seat read them (`lesson.md` changed
four times, `scorecard-section.md` twice, `c1-counter.py` repeatedly). Line anchors below are
against the digests above; a later edit can shift them, the quoted text is the stable handle.

The *frozen* side moved during the review as well: `e059ca93` (freeze v1) → `79f69347` (freeze v2:
amended P38-C1 with before receipts, counters/harness updated) → `3b0da5dd` (C1 controls re-scored
under v2). My binding and scope checks use the v2 bytes at `79f69347`, which is what the patches
must satisfy; §5 covers the one post-v2 counter edit that is still uncommitted.

Method: read the frozen predicate (`plans/round-38-claims.md`), both counters, and the destination
files (`PROVINCE.md`, `corpus/README.md`, `SCORECARD.md`, `corpus/SOURCES.md`, an existing entry, an
existing lesson) to establish which drafted lines a binding or a house convention actually needs.
Cross-draft 7-gram overlap was measured (0 shared 7-grams PROVINCE↔README, PROVINCE↔SOURCES,
README↔SOURCES, SOURCES↔SCORECARD; 2 shared only for the frozen carrier description
"…unblob 26.6.4 `squashfs_v4_be` integration fixtures against the frozen…"). **The redundancy in
this wave is semantic, not verbatim** — the same fact restated in different words — so the findings
below are fact-level, not string-level.

## 2. Calibration: what "every line pulls weight" means in this lane

| baseline | measurement | consequence for the review |
|---|---|---|
| round-36 entry | 16 477 B / 215 lines (`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`) | the r38 entry is 18 899 B / 256 lines, **+15 %** for a claim whose carrier set is half the size (no AppImage carve, 4-7 B members vs 2 130) |
| round-36 lesson | 11 659 B / 59 lines; r34 30 735 B / 134 lines | the r38 lesson is 19 788 B / 157 lines, larger than any recent lesson except r34, and ~32 % of it (§3.5 findings L1-L4) is wave-status rather than mistake/gate |
| PROVINCE preamble | `PROVINCE.md:339` and `:352` already open a round section with "Addition to Core (the Core table above is not rewritten; the Frontier list is …)" | the r38 preamble at patch L36 is **house convention, not padding** — withdrawn from the finding list |
| SOURCES `own-work` rows | 9 precedents (`S039`, `S053`, `S055`, `S057`, `S060`, `S061`, `S063`, `S067`, `S072`) | an own-work row is schema-legal, so S116 is judged on the frozen candidate list only, not on kind |
| capability table | a round-36 row already reads "REA SquashFS recursion through sasquatch (LE v4) … Big-endian/AVM not demonstrated" (`SCORECARD.md:625`) | a second row on the same mechanism needs a delta-only wording or none at all |
| README knowledge index | 104 of 124 entries listed; 21 knowledge files are absent by design | the index row is **optional**, not an invariant — see finding R3 |

## 3. Findings — removable or compressible content

Each row: location, size, and the one-line reason. **D** = delete; **C** = compress. Sizes are the
measured bytes of the named span.

### 3.1 entry (`R38ScribeEntry/entry.md`)

| # | line span | size | act | reason |
|---|---|---|---|---|
| E1 | `verified-at:` line 6, the clause "the frozen C1 counter at freeze … and at tip … reports `carriers_matched 0`, `entry_present false`, `sourced false`" | 540 B | D | measures the entry's *own absence*; true only before the landing and false in the commit that carries the entry — a provenance trio states what backs the entry, not its pre-landing counter state |
| E2 | L68-74 (the four-carrier `jq` echo, the "Oracle matching re-implemented exactly as the frozen counter" line, the `5 3 4 4` hits restatement) | 423 B | D | restates the table's columns L61-64 and the oracle counts already given at L45; the frozen counter is the matching authority, so the re-implementation sentence also invites a second authority |
| E3 | L179-181 ("The inode-table metadata header at offset 121 reads big-endian (`00 3a` = 58) … [source: wave-1 scout …; the parse itself was not re-run here]") | 274 B | D | the entry cites a measurement it explicitly did not run, inside a section whose conclusion (`mkfs_time != bytes_used`, so `-be` is passed) already rests on the superblock fields in the previous sentence |
| E4 | L213-215 ("Not that stock unblob needs no external extractor. The opposite: …") | 206 B | D | third statement of L25-26 ("Refused — no external extractor") and L112-121 (declared dependency); keep the two that carry the evidence |
| E5 | L220 ("Not an independent-implementation cross-check …") | 98 B | D | duplicates the bolded paragraph at L155-157, which says the same in one sentence with the reason |
| E6 | L226-229 ("Not committed evidence yet. … Numbers above are re-derived from the drafts at 2026-10-26T06:23Z") | 305 B | D | seat state; false in the landing commit that commits `corpus/evidence/round-38/c1/`, so it is dead text the moment the patch applies (the claim's own receipt path is already in §Receipts) |
| E7 | L252-256 ("Limit worth knowing when reading these ids: three runs over the same K4 subject stored `ev_3d1197d1…`, `ev_de83842f…`, `ev_b62e21b8…`") | 459 B | C | the caveat (a stored id covers the whole record, including `parameters.output_directory`, not the subject digest) pulls weight and should stay in one sentence; the three-id catalogue cites two ids that appear nowhere else in the entry, so it cannot be re-derived by a reader |
| E8 | title L9, second clause "…and gap-free depends on the link, not the endianness" | ~40 B | C | the body measures one escaping symlink (K1, gap-free) against one in-tree symlink (K2, one gap); "depends on the link" generalises from n=1 per branch and is weaker than the section's own hedged wording |
| E9 | L172 "This is why the sasquatch build matters at all on a Linux host." | 72 B | D | editorial conclusion to a section whose table already shows both refusals |
| **sum** | | **≈ 2 377 B** | | 12.6 % of the entry |

### 3.2 PROVINCE patch (`R38ExecProvincePatch/patch.txt`)

| # | line span | size | act | reason |
|---|---|---|---|---|
| P1 | L42 Limits, clause "Coverage reads `complete` only on K3/K4; K1 and K2 read `partial` (K2's `partial` comes from its one unpublished symlink entry)." | ~250 B | D | the same cell of the same round block (row L40, Verified evidence) already states "zero extraction gaps on K1/K3/K4, one `unpublished-entry` gap on K2 (`var/lib/run-link` symlink)"; coverage/gap is one fact, stated twice inside 3 lines |
| P2 | L42 Limits, citation "(`.ufo/waves/round-38/w1/artifacts/R38ExecAfterK3/after.json`)" | ~90 B | D | a seat artifact cited for a four-carrier statement, and (under freeze v2) `after.json` is the arm with 4/4, not the dependency arm — the cited file does not show what the sentence claims; the claim's receipt path `corpus/evidence/round-38/c1/K*/` is already in the row |
| P3 | L40 row, "`-be`" and "from `PATH` with `-be`" / L42 "shells out to `sasquatch-v4be` on `PATH`" | ~120 B | C | the dependency is stated in the row, the Limits paragraph and the frontier note; **one** of the three is load-bearing under freeze v2 (see §5), two are echo |
| P4 | L44 frontier note, closing "AVM-BE and vendor-mangled images stay Frontier" | ~70 B | C | third statement of the same boundary (row Limits, Edit 2 bullet, note); the note's distinctive job is naming the superseded surface and the closing clause of the round-36 note — that part stays |
| **sum** | | **≈ 530 B** | | 8.8 % of the patch |

Preserved deliberately: the preamble at L36 (house convention, see §2), the row's entry-path cell
(the counter's `province_core_row` binding requires the entry path *in the row*), Edit 2 and the
frontier note both naming `big-endian` + `superseded` (two candidates for the single binding; the
predicate names "the round-38 frontier note", so both are defensible — do not drop the note), and
the doctor-pointer edit (C2's only repair).

### 3.3 README patch (`R38ExecReadmePatch/patch.txt`)

| # | line span | size | act | reason |
|---|---|---|---|---|
| R1 | added L23 (frontier bullet), the parenthesis "— AVM-BE (the handler's `bytes_used == mkfs_time` test selects a path this round did not measure) and vendor-mangled images stay Frontier" | ~300 B | C | the `bytes_used == mkfs_time` mechanism is stated in the entry (§AVM-BE), in the PROVINCE Limits cell and in S114's scope; the README bullet only needs the dated supersession + the stem + "AVM/vendor-mangled stay Frontier" (the round-36 note's own three-sentence shape) |
| R2 | added L7 (coverage row), "publishes every regular file of the frozen oracle (K1 5/5, K2 3/3 …; K3/K4 4/4 …)" | ~60 B | C | the prose and the counts are the same claim twice; keep the counts as the enclosing phrase |
| R3 | added L15 (knowledge index row) | 558 B | D* | no invariant requires it (21 of 124 entries are absent from that table) and it restates L7's gist; *keep if the L1 wants the recent-round convention (rounds 29-36 are all listed) — it is a convention choice, not weight |
| **sum** | | **≈ 860-1 420 B** | | 14-24 % of the patch |

Preserved: the coverage-map row must name the entry **stem** (`coverage_map_row` binding), the
`missing-extractor-dependency` / `dependencies:["sasquatch-v4be"]` clause (under freeze v2 this is
claim shape, not colour), "K2's tree symlink is recorded as `unpublished-entry`" (it is why C1
cannot reach 4/4 — the row would otherwise misstate its own limit).

### 3.4 SCORECARD + LOG section (`R38ScribeScorecardDraft/scorecard-section.md`)

| # | line span | size | act | reason |
|---|---|---|---|---|
| S1 | L30-37 capability row + "Entry rule for that row" paragraph | 2 076 B | D or C | neither frozen predicate reads a capability row; `SCORECARD.md:625` already holds the LE row for the same mechanism, so the drafted row repeats its mechanics ("publishes every regular file … `missing-extractor-dependency` … publishes no bytes") almost sentence for sentence; if the L1 keeps it, the entry rule (5 lines of instruction to the L1) reduces to the one disclosure that matters — the extractor dependency and the K2 gap |
| S2 | LOG L80 (seven controls enumerated with per-control `carriers_matched`/`mismatches`) | 615 B | C | the SCORECARD claim rows already carry the control names and values in their `before` cells, and the section's own intro line says "all seven controls exit 1"; one enumeration is enough |
| S3 | LOG L81 (pre-claim recount at three revisions, with command-A/B numbers, craft/Adjacent ranges) | 603 B | C | duplicates the C2 row's `before` cell (48 pointers, 124/124, 17/17, 9/9, `SKILL.md:81-314`, `PROVINCE.md:97-125`) and the Owned-scores paragraph (124/124, 17/17); the LOG needs the receipt path and the verdict, not a third copy of the numbers |
| S4 | LOG L86 + §D L105 (freeze-drift, twice) | 576 B | D | §A0 (L46-71, 2 012 B) is the canonical disclosure with the digests and the decision the L1 must take; the two echoes repeat it without adding a fact — keep §A0, point at it once. §A0's own text is now a freeze behind and must be re-pointed (§5) |
| S5 | L38 "Assimilation: [L1-FILL] — theme …, per-entry gate with ≥1 admit and ≥1 reject, id-collision check and quarantine hand-check before any append" | 490 B | D | restates §2b of the frozen plan and the lesson's Gate; as written it is a placeholder that repeats the rule instead of the outcome. Replace with the outcome once the Gate lands (round-36's precedent: "one entry admitted …, three refused") |
| S6 | L28, "a landed round-38 entry makes it 125/125 and the row must be re-stated in the same landing" | ~120 B | D | instruction to the L1 inside a scored row; belongs in §C (verdict placeholders) |
| S7 | L28 "The finite proxies retire no domain axis." | ~60 B | D | the section already ends with "**retired:** none" |
| S8 | capability row's `before`/`after`-adjacent prose "Provisional: no axis harmed by the round [L1-FILL at the landing revision]" | ~80 B | D | placeholder assertion with no measurement behind it; round-36's section has no equivalent |
| S9 | "Draft-stage clause table (not claim data): … `draft-clauses.py` … `xpin-recompute-drafts.txt`" inside the capability rule | ~300 B | D | seat-artifact citation inside production text, and the scorecard's own §D already says those artifacts must not be cited as claim data |
| **sum** | | **≈ 3 500-4 900 B** | | 20-28 % of the section |

Preserved: both claim rows' `before` values and receipt paths (the round-36 contrast is that its
cells hold one JSON path each — the r38 cells are heavier because the wave-1 findings must be
disclosed *somewhere*; trim the duplicates, not the disclosure), the owned-scores sentences (C2's
O1-O4 assertions are read out of them), §A0 (freeze drift), the harness `mkdir -p` note (an
instrument limit the round must carry), and the `[L1-FILL]` markers themselves.

### 3.5 lesson (`R38ScribeLessonSkeleton/lesson.md`)

| # | line span | size | act | reason |
|---|---|---|---|---|
| L1 | §"Kill-rule and control status", L106-110 | 305 B | D | the header (L6-7) already states "seven frozen controls (`CTL-C1-0/1/2`, `CTL-C2-0/1/2/3`), **all exit 1**, … neither kill rule stopped a claim"; the section's only unique sentence ("the controls do not exercise the harness: M38-4 is the defect they could not see") is already M38-4's captured-by cell |
| L2 | §"Wave-1 falsifiers this draft must carry forward", L112-133 (5 bullets, 20 lines) | 1 760 B | C→D | wave status, not lesson: the K1/K2/K4 clause state duplicates the entry's §"What the four after-runs publish" and the SCORECARD LOG bullet, and the v2-amendment bullet repeats the header paragraph (L8-17) verbatim in substance. Keep **one** row in `## Mistakes` for the finding that is actually a lesson — K2's structural unmatchability (no-gap clause vs a retained symlink), class `predicate design` |
| L3 | §"Routed defects carried into this round — status at the draft", L134-147 (12 lines, 5 of them `[L1-FILL]`) | 937 B | C | duplicates the SCORECARD LOG bullet "Routed defects landed as fixes at the freeze" and §2b of the plan; a lesson cites defect status only where a Mistake row needs it (R37-CL1→M38-1, R37-CL3→M38-2) |
| L4 | §"[L1-FILL] citation pointers", L148-157 | 705 B | D | integration scaffolding; every bullet is a `<line>` placeholder for the L1, and the same landing list is in the plan and in the entry's Sources section. Must not reach `corpus/lessons/round-38.md` |
| L5 | M38-2 fix cell tail "The skeleton itself now exists at …/lesson.md while `.ufo/waves/round-38/w1.ready` exists and no `w1.done` marker does" | ~200 B | D | seat-timeline state; unverifiable and meaningless after the wave closes |
| L6 | M38-3 captured-by and evidence cells (the full v1→v2 story, the `grep -v sasquatch` mechanism, "the L1's uncommitted v2 amendment applies this fix") | ~600 B | C | the mechanism is now written in the claims file's own "Freeze v2 note" (`plans/round-38-claims.md` at `79f69347`); the lesson needs the class, the red-before command and the exit code, and can cite the plan for the mechanism |
| L7 | Gate rows S110-S116, repeated digests/oids/PATH mechanism (the same sha256/oid numbers are in the SOURCES row, the entry's `source:` line and here) | ~500 B | C | R37-CL3 asks for *decisions* with reason + flip, not a third copy of the evidence file's digests; cite the row id |
| **sum** | | **≈ 4 300 B** | | 21.7 % of the lesson |

Preserved: every Mistake row's red-before command with its failing path and exit code (the spec's
"A fix counts only with a shown red-before"), the green leg for M38-1/M38-2/M38-3/M38-4, the
quarantine hand-checks (5 rows, each with a live fact), the id-collision numbers and the guard
proof pointer, and the ≤25-word Gate quotes rule as it applies to the *source* rows.

## 4. Defects found while reading (reported, not repaired)

These are not minimality items, but each one makes drafted lines either redundant or unsupported.

1. **Entry §Receipts inverts the freeze-v2 filenames.** The table (L246-250) maps
   `.ufo/…/R38ExecAfterK3/after.json` to "(0 files, 1 `missing-extractor-dependency`)" and
   `diagnostic-after-with-declared-extractor.json` to "(4/4, 0 gaps)". The frozen v2 counter (`79f69347`) reads
   `corpus/evidence/round-38/c1/K*/before.json` for the 0-file/dependency arm and `after.json` for
   the 4/4 arm (`before_missing_extractor_gap`, `before_oracle_hits == 0`, `after_gaps_empty`). The
   entry will therefore cite the wrong arm under the v2 naming. [Command: `git diff
   tools/round-38/c1-counter.py` — after-loop reads `f'{AFTERDIR}/{k}/{mode}.json'`.]
2. **One-sided `used-by`.** The entry cites S107, S108, S110, S111 in its Sources table, but those
   rows' `used-by` cells name only the round-36 entries (S108: `corpus/knowledge/2026-10-26-r36-…`).
   `R38ScribeSOURCES.md` §F6 already flags it; the drafted patches do not resolve it. Only S112 can
   satisfy `c1-counter.py`'s `sourced` binding.
3. **README knowledge-index source cell is a subset.** Added L15 lists "S107, S108, S112, S113"
   while the entry cites S112-S116 (+S107/S108/S110/S111). Either list all cited ids (round-36 style)
   or none.
4. **Lesson `## Gate` Decision 1 admits a source with no row.** It admits `unblob-format-matrix`
   (staged S122, to be renumbered "into the S112+ space on append") — but the append block holds
   S112-S116 only and the entry does not cite it. As drafted the admission is dead text: either add
   the row and cite it, or drop Decision 1 (the ≥1 admit / ≥1 reject quota is already met by
   S112-S114 admits and S115 reject).
5. **New census warning from the two-row design.** Appending S112 raises the duplicate-URL count
   9 → 10: `gate-validate.out` prints `W04 S112 duplicate url
   raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py`
   (S108 already holds that URL). This is the **only** new duplicate authority the wave creates and
   it is unavoidable: S108's `used-by` is closed to this round, so a fresh row is the only way to
   satisfy the binding. Record the warning; do not split it further.
6. **Both drafts describe freeze v2 as uncommitted; it was committed while they were written.**
   Lesson header L8-17 ("the L1 left a **freeze v2 amendment** in the working tree … uncommitted at
   this seat's read") and the §Wave-1 falsifiers bullet "The freeze v2 amendment is in the working
   tree, not in a commit" are now false: `79f69347` carries v2, `3b0da5dd` re-scores the C1 controls
   under it. Scorecard §A0 has the same problem (§5). Any sentence of the form "the L1 must decide
   between the frozen blob and a re-freeze" must be replaced by the decision actually taken, or by
   the *remaining* open edit (the relaxed gap clause).

## 5. Freeze-v2 interaction (content that becomes *required* — and one line of it about to go stale)

Freeze v2 (`79f69347`) adds a per-carrier before-receipt arm to P38-C1. Read against it, three
drafted surfaces are **under-cited**, and trimming them would break the frozen predicate:

- PROVINCE row L40 cites "receipts `corpus/evidence/round-38/c1/K*/after.json`" only — v2 requires
  the paired `before.json` to be committed too; the row's Probe cell states the after-run only.
- Entry `## Receipts` needs `before` and `after` per carrier (see defect 1).
- README L7's dependency clause and PROVINCE L42's dependency sentence stop being optional colour:
  under v2 they describe a required binding. Keep exactly one of them per surface (finding P3).

**Frozen v2 still forbids every extraction gap** (`git show 79f69347:tools/round-38/c1-counter.py`
→ `d['after_gaps_empty'] = gaps(envs.get(f'{k}/after')) == []`, used in the `matched` conjunction at
L205). K2's retained symlink therefore still blocks `carriers_matched == 4`, and the drafted lines
that say so — entry "Not a claim that the frozen C1 target is met … cannot exceed 3", PROVINCE row +
Limits ("one `unpublished-entry` gap on K2"), scorecard C1 row and §A0, lesson "K2 cannot satisfy
'no extraction gap' as frozen" — are **correct and load-bearing against the frozen bytes**. Do not
trim them.

**But the worktree counter no longer says that.** `git diff tools/round-38/c1-counter.py` (still
uncommitted at this read) replaces exactly that clause with
`after_no_missing_extractor_gap = not any(g.kind == 'missing-extractor-dependency' …)`, i.e. it
drops the `unpublished-entry` gap from the predicate. If that edit lands as-is, every statement
listed in the previous paragraph becomes false, and the one finding the drafts treat as
target-sinking on these bytes (K2's gap) disappears while the counter keeps the name `c1-counter.py`. This is not a
minimality problem, it is the one open integration decision of the round, and it needs to be taken
on purpose:

- score the frozen blob `79f69347:tools/round-38/c1-counter.py`, or
- commit the relaxation as a further freeze and then rewrite the six K2 sentences in one pass
  (entry, PROVINCE row, PROVINCE Limits, scorecard C1 row, scorecard §A0, lesson falsifiers/mistake).

I did not score either version and did not revert. Derived register: the scorecard draft's §A0
(`scorecard-section.md:46-71`) is already **one freeze behind** — it frames v2 itself as uncommitted
worktree drift and asks the L1 to choose between "score the frozen blob `a7a62b09…` or re-freeze";
v2 has since been committed (`79f69347`) and its controls re-scored (`3b0da5dd`). Keep the section,
re-point it at the *remaining* uncommitted relaxation, and cite both commits — otherwise the only
paragraph in the SCORECARD that talks about counter identity describes a state that no longer exists.

## 6. Totals and the tradeoff

| surface | drafted bytes | removable (D+C) | share |
|---|---|---|---|
| entry | 18 899 | ≈ 2 377 | 12.6 % |
| PROVINCE patch | 6 012 | ≈ 530 | 8.8 % |
| README patch | 6 027 | ≈ 860-1 420 | 14-24 % |
| SCORECARD + LOG | 17 712 | ≈ 3 500-4 900 | 20-28 % |
| lesson | 19 788 | ≈ 4 300 | 21.7 % |
| SOURCES block | 5 926 | ≈ 947 (S116) | 16 % |
| **total** | **74 364** | **≈ 12 500-14 500** | **17-19 %** |

The S116 row (`kaidoku lane synthetic SquashFS v4 writer — tools/round-37/gen-squashfs.py`, 947 B) is
the one SOURCES row the frozen plan does not name: §2b lists three candidates (handler source,
fixture provenance, Freetz AVM-BE note) and R37-CL3 adds the 7-Zip rejection; the generator is
already pinned in the entry by path, 216 lines and sha256. Dropping it costs nothing the entry does
not already state; keeping it is defensible under the 9 `own-work` precedents. Reported as a
candidate, not a defect.

Tradeoff: the heaviest remaining prose is not padding — it is disclosure of the two findings that
sink the claim as frozen (K2's symlink gap; the extractor dependency). Cutting those below one
statement per surface would make the patches *smaller and wrong*. The 17-19 % above is what can go
while every frozen binding, routed defect and Gate rule still has a line.

## 7. Evidence and limits

- Reviewed against `plans/round-38-claims.md` at `79f69347` (freeze v2; v1 read at `e059ca93` for
  the contrast), `tools/round-38/{c1,c2}-counter.py` at `79f69347` plus the uncommitted worktree
  c1 edit, `PROVINCE.md:38-90,128-175,355-374`, `corpus/README.md:11-51,194-200,226-238`,
  `SCORECARD.md:19-32,615-640,3385-3397`, `corpus/SOURCES.md:1-30,195-213`,
  `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`,
  `corpus/lessons/round-36.md`, `corpus/lessons/round-37-verifier-spotcheck.md`.
- Freeze sequence read with `git log --oneline` / `git show --stat` / `git show
  <rev>:<path>` only (no mutating git): `9c9d496b` wave-1 dispatch → `cb4326b2` harness fix →
  `79f69347` freeze v2 → `3b0da5dd` C1 controls re-scored.
- Duplication measurement: cross-draft 7-gram intersection over the four patch files; fact-frequency
  counts (`grep -o` per term per file, added-lines only for the diff-formatted patches:
  README additions 4 lines / 1 891 B, PROVINCE additions 13 lines / 2 287 B).
- Census effect: `.ufo/waves/round-38/w1/artifacts/R38ExecMirrorGate/gate-validate.out` (exit 0,
  10 W04 after the append vs 9 at the start).
- Not done, deliberately: no counter run (advisory seat; the count is the reviewer/executor lane), no
  draft edited, no VCS mutation, no tool installed or upgraded (nothing was needed).
- Limits: the six drafts were in flight during this review (hashes pinned above; later edits can
  shift line anchors). Two findings I first recorded were withdrawn after checking house precedent —
  the PROVINCE "Addition to Core for …" preamble (exists at `PROVINCE.md:339,352`) and the S116
  `own-work` kind (9 precedents) — both are noted in §2 so the L1 does not re-litigate them.

Scratch `/fast/scratch/hyaku/kaidoku-r38/R38SimplifierMinimality` removed; every number above is
reproducible from the committed-lane paths and the hashes in §1.
