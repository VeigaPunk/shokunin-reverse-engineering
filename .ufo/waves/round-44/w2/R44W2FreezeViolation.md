# R44W2FreezeViolation — freeze-integrity adjudication (round 44, wave 2)

Seat `R44W2FreezeViolation` (critic). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84`; measured revision
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; violating commit
`c86ea508188c50e2645b1f9bba65df4177cda6b1`; lane tip at dispatch `c86ea508`, lane tip at this
review `8bb1090af3fef64477c4337855e4347472db2701`.

Scope: the freeze-integrity defect (M44-2) and the parts of the C1/C2 verdicts that depend on the
freeze rule. I change no claim, counter, rubric, frozen byte or production document. Every number
below is from a command I ran; commands, exit codes and stdout digests are in the receipt block.

## 0. Verdict

| question | verdict | one-line ground |
|---|---|---|
| (a) does the frozen claim's rule forbid `c86ea508` on its own words? | **YES**, four independent clauses | `plans/round-44-claims.md:77-85` (M/D/R/T/U are changes; directory pathspec), `:307` (directory pathspec, populated before FREEZE), `:311` (`control-fixtures/**` byte-frozen), `:242` ("no later tool is added there") |
| (b) is measuring at `55bcce69` a legitimate measured revision or a silent revision change? | **legitimate as a REV-scoped score, and I verified it is clean across the claim's whole frozen list; not legitimate as a statement about the round's state** | rule is per-REV (`:77-79`); `55bcce69` exit 0 on all 12 claim frozen pathspecs; claim+counters+rubric byte-identical at `55bcce69` and at HEAD |
| (c) is C2's `met` defensible? | **only qualified: `met@55bcce69`, inadmissible at the tip.** As recorded (both qualifiers in the cells) it is defensible; as "round 44 met C2" it is not | `c2-score-at-55bcce69.json` exit 0 / 80 evaluated / `mismatches []`; `c2-score-at-tip.json` exit 2 / **0** evaluated |
| (d) what must the report say? | 10 required statements, §9; 5 are missing or wrong today | FV-1…FV-7 |

The round's freeze handling is **defensible in its arithmetic and in its disclosure of the
violation, and wrong in two of the reasons it gives** (the C1 "unsatisfiable" story, and calling an
unwired, pathspec-scoped script "the fix"), plus it understates what the 8 frozen files were.

## 1. Facts re-derived (not inherited)

| # | command | exit | observed |
|---|---|---|---|
| 1 | `git log --oneline c48f8a4..c86ea508 -- tools/round-44/` | 0 | exactly one commit: `c86ea508` |
| 2 | `git log --name-status --format='%h %s' c48f8a4..c86ea508 -- tools/round-44/` | 0 | 8 paths, **all status `M`**, zero `A` |
| 3 | `git log --oneline c48f8a4..55bcce69 -- tools/round-44/` | 0 | empty — the measured revision is clean on that pathspec |
| 4 | `git merge-base --is-ancestor c48f8a4 55bcce69`; `… 55bcce69 c86ea508` | 0 / 0 | freeze → measured → violation, linear |
| 5 | `git diff --stat 55bcce69 HEAD -- plans/round-44-claims.md tools/round-44/c1-counter.py tools/round-44/c2-counter.py tools/round-44/c2-rubric.json tools/round-44/carriers.json` | 0 | empty — the rule and the instruments did not move after the score |
| 6 | preflight gate `--freeze c48f8a4 --rev c86ea508 --pathspec tools/round-44` | **1** | `frozen_path_changed`, 8 touched, 8 blob_changed |
| 7 | preflight gate `--rev 55bcce69 --pathspec tools/round-44` | **0** | `clean` |
| 8 | preflight gate `--rev 8bb1090a --pathspec tools/round-44` | **1** | `frozen_path_changed`, 8/8 — the current tip still fails |
| 9 | preflight gate `--rev 55bcce69` with **all 12 claim frozen pathspecs** (`plans/round-44-claims.md`, `tools/round-44`, `tools/round-42/{fixtures.json,c1-counter.py}`, `tools/round-43/c1-counter.py`, `corpus/evidence/round-42/c2/fixtures`, `corpus/evidence/round-42/c1`, `corpus/evidence/round-42/c2/heldout`, `corpus/evidence/round-43/c1/heldout`, `corpus/evidence/round-44/oracle`, `SKILL.md`, `corpus/SOURCES.md`) | **0** | `clean`, 0 touched, 0 blob — the measured revision is clean for the **whole claim**, not just the counter's subset |
| 10 | same 12 pathspecs `--rev c86ea508` | **1** | 8 touched / 8 blob (same 8) |
| 11 | `.ufo/waves/round-44/l1/c1-score-at-tip.json` / `c2-score-at-tip.json` (committed) | — | both `"exit_code": 2`, `"reason": "frozen_path_changed"`, same 8 paths; C2 also `"entries_evaluated": 0`, `"usable_as_claim_score": false` |
| 12 | `git diff --name-only c48f8a4 c86ea508 -- tools/round-44/control-fixtures/` (test that these are *control inputs*) | 0 | 8 files; freeze→tip sha256 all differ (table §5) |

`c1-score-at-55bcce69.json`: `carriers_matched 4`, `met_target false`, `exit_code 1`,
`frozen_path_changed []`, `bindings_false ["province_core_section","province_core_row","frontier_note"]`,
`failing []`.

`c2-score-at-55bcce69.json`: `entries_evaluated 80`, `entries_count 80`, `mismatches []`,
`unevaluable_count 0`, `frozen_path_changed []`, `met_target true`, `exit_code 0`,
`rubric_sha256 == rubric_sha256_at_freeze == e8cc0ded…55e7`, `counter_sha256 ==
counter_sha256_at_freeze == 085192ea…c277`.

## 2. (a) The frozen rule forbids `c86ea508` on its own words — four clauses, not one

The claim's freeze rule (`plans/round-44-claims.md:77-85`) says, verbatim: *"A score at `REV` is
admissible only if `FREEZE` is an ancestor of `REV`, no commit in `FREEZE..REV` touches a frozen
path of that claim, and each frozen regular-file blob at FREEZE equals the blob at REV; a later
restore does not un-block (exit 2 `frozen_path_changed`, never `met_target`). … M/D/R/T/U are
changes, A is a change whenever the path existed at FREEZE, plus a tree-level blob backstop…
`tools/round-44/` is frozen as a DIRECTORY pathspec — a file added under it after the freeze is a
change."*

`c86ea508` is caught by four independent clauses:

1. **The status clause** (`:80-81`): all 8 paths are `M`. M is a change. Nothing in the claim
   limits the walk to additions.
2. **The directory freeze** (`:82-83`): the 8 paths are under `tools/round-44/`.
3. **The explicit byte-freeze** (`:311`): *"`tools/round-44/control-fixtures/**` (committed
   red/positive control inputs)"* is listed separately from the directory pathspec in the
   byte-frozen list, so even if the directory clause were read as additions-only, these files
   were declared byte-frozen.
4. **The separability clause** (`:242`): *"every file under it is pre-landed before freeze and the
   directory scope is explicit only if no later tool additions occur."*

**The strongest defender's reading, and why it fails.** "`tools/round-44/` is frozen as a DIRECTORY
pathspec — *a file added under it* after the freeze is a change" gives an addition as its only
example, and M44-2's own text in the record says the commit "added/edited 8 files". If the clause
were additions-only, this commit would be legal on clause 2. It is still illegal: the control
fixtures are a separate **byte**-freeze (clause 3), the walk's status filter names M (clause 1), and
the tree backstop — which compares every frozen blob at FREEZE with the blob at REV — fires on all
8 by itself (`blob_changed 8`, check 6). Both counters, implemented separately, list byte-identical
sets. So the defender's reading changes nothing about this case; it only shows that the record's
wording ("added/edited", and the claim's addition-only example) is the weakest sentence in an
otherwise unambiguous rule. **Defect FV-7 (low): say "modified 8 committed files", not "added".**

## 3. (b) `55bcce69` is a legitimate measured revision — and the rule's asymmetry is worth naming

**Legitimate, on the rule's own terms.** The rule quantifies over `REV`, not over "the tip": *"A
score at `REV` is admissible only if …"*. `55bcce69` satisfies all three conditions, and I checked
the third one beyond the counters' own subset: with all 12 frozen pathspecs from `:305-313` plus the
counter's `FROZEN_PATHS`/`FROZEN_PREFIXES` (`tools/round-44/c1-counter.py:272-286`), the gate exits
0 at `55bcce69` and 1 at `c86ea508` (checks 9-10). That matters because the counters do **not** freeze
the whole claim list — `FROZEN_PATHS` omits `SKILL.md`, `corpus/SOURCES.md` and the four carrier
bins, all declared byte-frozen at `:307-313`. Had those moved after the freeze, both counters would
have said `frozen_path_changed []` while the claim was violated. They did not move; the measured
revision is clean under the claim's own list, not only under the instruments' narrower one.

**Not a silent revision change**, because:
- the rule the score was taken under did not move (`git diff 55bcce69 HEAD` over the claims file,
  both counters, the rubric and the carriers is empty — check 5). If the claims file had been
  amended after the score and the amendment still cited `55bcce69`, that *would* be the change the
  restore clause exists to prevent, because the score would then be quoted under a rule that did
  not exist when it ran;
- both revisions are named: `55bcce69` in every score cell, `c86ea508` in
  `.ufo/waves/round-44/l1/{c1,c2}-score-at-tip.json`, `preflight-c86ea508.json`, and the record text
  (`LOG.md:3203`, `SCORECARD.md:3530`, `corpus/lessons/round-44.md:16`);
- the at-tip receipts are committed, so a reader can see the failure rather than take it on trust.

**The asymmetry that a successor rule must close.** The frozen text forbids *break → restore*
("a later restore does not un-block") and says nothing about *score → break*. Read literally, a
round can score at any clean ancestor and then damage the frozen tree; the damage costs it nothing
as long as it discloses. That is the exact shape of what happened: the round scored, then wrote 8
frozen files, then declared the earlier revision "the" measured revision. The outcome here is
honest because the damage is disclosed and the earlier revision is independently clean — but the
rule, not the disclosure, should decide that. **Proposed text for the next freeze, not applied
here:** *"A score at `REV` is inadmissible if any commit after `REV` and at or before the round's
filing commit touches a frozen path of that claim; the admissible revision is then the claim's
last measured revision and the claim is recorded as not met at filing."* This round's text permits
what happened; I am not asking the L1 to rewrite a frozen claim.

**One factual residue.** "The tip" in `c86ea508`-era receipts is `c86ea508`; the lane's tip at this
review is `8bb1090a`. I verified `8bb1090a` also fails (preflight exit 1, 8 touched, 8 blob —
check 8), so the sentence "both counters exit 2 at the tip" is true of the *current* tip, but the
committed receipt behind it names one commit earlier. **FV-6 (low).**

## 4. (c) C2's `met`: both readings, and the one I defend

**For the verdict.** The claim's target is explicitly REV-scoped: *"Target: `mismatches == 0` over
the frozen rubric at REV, `entries_evaluated >= 1`, every check evaluable, `frozen_path_changed []`,
exit 0"* (`:247-249`). At `55bcce69` all of that holds, with the **frozen** rubric and the **frozen**
counter bytes (`rubric_sha256 == rubric_sha256_at_freeze`; `counter_sha256 ==
counter_sha256_at_freeze`), 80 of 80 entries evaluated, 0 mismatches, 0 unevaluable. The scored
surfaces (`SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `README`) are untouched by `c86ea508`, and the
round says so in the same cells that carry the verdict (`SCORECARD.md:3526`: *"**met at the measured
revision**; inadmissible at the lane tip — see below"*; `LOG.md:3202` "met at the measured
revision").

**Against the verdict.** A round is filed by its tip. At the tip the same counter returns `exit 2`,
`entries_evaluated 0`, `usable_as_claim_score false`. A reader who encounters "round 44 — C2 met"
without the qualifier has been told something false about the repository, because the claim's own
instrument cannot be run there. The freeze rule's title is *"(both claims)"*; a round that ends with
its own freeze rule red cannot present itself as a round whose two claims were scored, only as a
round whose one claim was scored at a named ancestor.

**The vacuity trap, stated so nobody falls into it.** `c2-score-at-tip.json` still contains
`"mismatches": []` and `"mismatches_count": 0`. Those are **not** a result: `entries_evaluated` is
0 and the counter's own gate block says `"usable_as_claim_score": false`. Any summary that quotes
the at-tip `mismatches []` as "0 mismatches at the tip" is reporting a measurement that was never
made. The record does not currently do this — it cites the `55bcce69` JSON — and it must not start.

**Free-pass / note-vs-value.** I inspected the rubric's entry shape (`C2-a1-1`, `asserted "137/137"`,
`check: json`, `argv_digests` incl. the check body's sha256, 8 argv digests) and confirmed the
frozen-rubric provenance above; I did **not** re-derive all 80 entries or re-run CTL-C2-4 — that is
the C2 seats' scope (`R44W2C2Rescore`, `R44W2C2Corrections`, `R44W2C2Freeze`). My statement is
narrower: the `met` I can see is measured, frozen-rubric, non-vacuous at `55bcce69`, and
unreproducible at the tip.

**Verdict I would defend.** *C2 is met at `55bcce69` and not met as a property of the round's tip.
The calibration axis move (10 → 10) rests on that qualified verdict; an unqualified "C2 met" is
inadmissible.* The record as written already carries both halves, so the verdict is defensible **as
recorded** — the report must not flatten it (§9, item 8).

## 5. What the 8 frozen files actually are — the record understates M44-2

They are not "unsettled wave evidence" that happened to land under a frozen directory. They are the
**CTL-C1-POS positive control's inputs**, regenerated:

| path (under `tools/round-44/control-fixtures/`) | bytes freeze → tip | sha256 freeze → tip |
|---|---|---|
| `pos/…/c1/v1le/after.json` | 13814 → 14440 | `12c794ada076a87d…` → `51dd0688f4e8385b…` |
| `pos/…/c1/v1be/after.json` | 13813 → 14439 | `0cb895d56cc3d56a…` → `c4ede8bf56b27fd2…` |
| `pos/…/c1/v2le/after.json` | 15552 → 16281 | `5b065cb75ce82d21…` → `d0f2117b8de34cb5…` |
| `pos/…/c1/v2be/after.json` | 15551 → 16280 | `003446dfbd7c42c1…` → `e44d365393db27b8…` |
| `pos/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` | 16880 → 20280 | `4d26a052d98a5327…` → `ee04ffc7144f3d5c…` |
| `pos/manifest.json` | 4630 → 4630 | `3647f1af0b366110…` → `02a076ca1f52da49…` |
| `c3/…/c1/v1le/after.json` | 10214 → 10404 | `adba89ea3d22de71…` → `8b15697baae79379…` |
| `c3/manifest.json` | 874 → 874 | `41ad7b5cd284d009…` → `7b4c200301f35311…` |

The change is semantic, not cosmetic: the four `pos` receipts were re-minted with new
`evidence_id`s (`ev_4d2155ed4dae142a…` → `ev_03c9cdb31c9c5a0b…` for `v1le`) and new
`provider_id`s (`1239772:1` → `2463841:1`), and the `pos` knowledge fixture was rewritten (143 insertions / 104 deletions), changing what the
positive control demonstrates. Consequences that the record does not state:

1. `CTL-C1-POS`'s recorded `stdout_sha256 88900939982efb9b…` (`controls/summary.json`) has **no
   reproducible input at the tip** — the fixture bytes it scored no longer exist there.
2. Both counters exit 2 before any control arm runs, so the tip cannot re-run *any* control, not
   just the frozen-path check.
3. The control ledger is reproducible at `≤55bcce69` only. A reader must be told that.

`LOG.md:3203` and `corpus/lessons/round-44.md:16` say the commit "wrote 8 files" / "added/edited 8
files under the frozen `tools/round-44/control-fixtures/`". That is true and insufficient.
**FV-3.**

## 6. Does `tools/round-45/frozen-path-preflight.py` really catch it?

**Yes, for this violation and for the status classes the claim names.** Verified on the real lane
and on throwaway repos (`mktemp -d`, `git -C "$D"` everywhere, `rev-parse --show-toplevel` asserted
equal to `$D` before each commit):

| probe | exit | meaning |
|---|---|---|
| real lane `--rev c86ea508 --pathspec tools/round-44` | 1 | 8 touched, 8 blob — catches the violation |
| real lane `--rev 55bcce69 --pathspec tools/round-44` | 0 | clean — the green arm is real |
| real lane `--rev 8bb1090a --pathspec tools/round-44` | 1 | the current tip is still red |
| real lane, 12 claim pathspecs, `--rev 55bcce69` | 0 | clean across the whole claim |
| fixture: modify then **restore** the freeze bytes | 1 | "a later restore does not un-block" is implemented by the walk, not by the blob backstop |
| fixture: frozen file edited **only on a merged branch** | 1 | `git log -m --diff-merges=first-parent` shows the merge's `M`; the round-43 port is not blind to merges |
| fixture: **new** file added under the frozen dir | 1 | `A` is a change |
| fixture: `--rev == --freeze` | 0 | no false positive on an empty range |

**But it is a script, not yet a gate, and its scope is whatever the caller types:**

1. **Pathspec-scoped blindness (demonstrated).** With a frozen path edited *outside* the supplied
   pathspec the gate is green: fixture repo with `plans/claims.md` mutated, `--pathspec tools/round-44`
   → **exit 0**. Adding `--pathspec plans/claims.md` → exit 1. The round-44 claim's frozen list needs
   12 pathspecs; with only `tools/round-44` an edit to `SKILL.md`, `corpus/SOURCES.md`, a carrier bin
   or an oracle tree passes green while both counters would exit 2. The tool does not read the
   claim's `## Frozen paths` section, and nothing derives the list.
2. **The default mode is a blanket red.** With no `--pathspec`, the walk is unrestricted, so every
   file any commit in the range touched is reported: at the clean revision `55bcce69` it exits **1**
   with `touched 557`. Meanwhile the blob backstop is *skipped* when no pathspec is given
   (`frozen-path-preflight.py:69` `if pathspec:`), which is exactly backwards — a whole-tree call is
   where you want the backstop. The `--help` text still says *"Default: none (tree backstop only)"*
   (`:30`).
3. **Nothing invokes it.** `grep -rn frozen-path-preflight` outside its own file returns only
   documentation (lesson, QUALITY, SCORECARD, LOG, wave spec). No hook, no CI step, no wrapper. It
   landed in `8bb1090a`, *after* the violation it is cited as fixing.
4. It has no `--selftest`, so the four red arms above exist only in this report's transcript.

`SCORECARD.md:3530` says *"The fix is `tools/round-45/frozen-path-preflight.py`, shown red at
`c86ea508` … and green at `55bcce69`."* The lesson's routed defect (`corpus/lessons/round-44.md:60`)
is more accurate — *"wire it into the round's commit sequence before the next freeze"*. **FV-4.**

## 7. R44-C1: the verdict stands, "the stop is the only correct reading" does not

**Confirmed.** At `55bcce69` the frozen C1 counter returns `carriers_matched 4`, `met_target false`,
`exit_code 1`, `failing []`, with `province_core_section`/`province_core_row`/`frontier_note` false
because the round's honest-stop landing replaced the Core row with a "measured, not promoted" row.
C1 is not met at `55bcce69`; the target requires `met_target true`.

**Falsified — "no run can satisfy the whole frozen claim" (`LOG.md:3201`) / "internally
unsatisfiable on one field" (`corpus/lessons/round-44.md:63`) / "is unsatisfiable"
(`corpus/QUALITY.md:139`).** Four independent reasons:

1. **The round's own committed receipt shows the instrument reaching `met`.** `c1-score-4cc1.json`
   / `corpus/evidence/round-44/c1/counter-at-4cc1.json` at `4cc1ac11`: `exit_code 0`,
   `carriers_matched 4`, **`met_target true`**, `frozen_path_changed []` — with the *same* four
   scratch-form receipts (`corpus/evidence/round-44/c1/*/after.json` are unchanged since
   `fee6e98a`). So a run did satisfy the counter.
2. **The counter never tests the disputed clause.** `plans/round-44-claims.md:34` requires
   `parameters.output_directory` to name a `corpus/evidence/round-44/c1/` path;
   `tools/round-44/c1-counter.py:1176-1182` tests only `PROV_SEGMENT = '/kaidoku-r44/'` and the
   absence of `..`. `AFTERDIR = 'corpus/evidence/round-44/c1'` (`:246`) is used only to *locate*
   `after.json` (`:2070`, `:2856`), never as a provenance assertion. `run_provenance_ok` is `true`
   for `output_directory = /fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1le.1342995/rea-out`.
3. **The two prose clauses are jointly satisfiable by one path.** A scratch output directory laid
   out as `<scratch>/kaidoku-r44/<seat>/corpus/evidence/round-44/c1/<id>/` names both the
   `/kaidoku-r44/` segment (`:137`) and a `corpus/evidence/round-44/c1/` path (`:34`), and the
   counter's substring test accepts it. "No run can satisfy" is therefore false as written; the
   correct statement is narrower: *the four receipts this round produced do not*, because their
   `output_directory` lacks the committed-path segment.
4. **The exit 1 at `55bcce69` is caused by the round's own withdrawal, not by the provenance
   clause.** The Core row existed and was scored through at `4cc1ac11` and `9d3d1862`
   (`git show 4cc1ac11:PROVINCE.md` → `## Round-44 additions to Core` at `:424`, row `:428`,
   frontier note `:430` "moved Frontier → Core"); `55bcce69` replaced that block with
   `## Round-44 measured, not promoted (R44-C1 honest stop)`. The provenance contradiction was
   discovered, then the landing was withdrawn — it did not make the counter return 1.

**What is right in the record.** `PROVINCE.md:428` states the disagreement accurately: *"the claim
required the committed evidence path, while the counter accepts only the `/kaidoku-r44/` scratch
provenance. The score therefore does not satisfy the frozen predicate; no Core promotion is
claimed."* That sentence is correct and should be the model for the other three. What is missing
everywhere is the 4cc1ac11 green and the promote→withdraw cycle. **FV-1 and FV-2.**

**Consequence for my assignment's three-part test** — *confirm the verdict, confirm the stop is the
only correct reading, confirm the record says exactly that*: verdict **confirmed**, uniqueness
**falsified** (the counter's green at `4cc1ac11` is a live alternative that the round instead
withdrew), record **not exact** (the right conclusion from the wrong premise).

## 8. Defects for the L1 (numbered; each with path:line, command, exit, observed)

**FV-1 — blocking (record accuracy / false provenance).** The round's stated cause for the C1 stop
is contradicted by its own committed receipt.
`LOG.md:3201` ("so no run can satisfy the whole frozen claim"), `corpus/lessons/round-44.md:63`
("internally unsatisfiable on one field"), `corpus/QUALITY.md:139` ("is unsatisfiable").
Command: `python3 -c "import json;d=json.load(open('corpus/evidence/round-44/c1/counter-at-4cc1.json'));print(d['exit_code'],d['met_target'],d['carriers_matched'])"` → exit 0, prints `0 True 4`.
Observed: the frozen counter reached `met_target true / exit 0` at `4cc1ac11` with the scratch-form
receipts; `tools/round-44/c1-counter.py:1176-1182` never tests `corpus/evidence/round-44/c1/`; a
single output path can carry both segments.
Smallest safe correction: replace "unsatisfiable" with *"the frozen instrument does not implement
the amendment's `corpus/evidence/round-44/c1/` clause, so the `4cc1ac11` `met` is a met against a
weaker predicate than the claim prose; the landing was withdrawn rather than restated, and C1 is not
met against the frozen text."*

**FV-2 — blocking (record omission).** The promote→withdraw cycle is nowhere disclosed. `LOG.md:3201`
mentions the `4cc1ac11` exit 0 but not that a Core row was live; the lesson headline
(`corpus/lessons/round-44.md:1`) and `SCORECARD.md:3528` ("No capability row enters: R44-C1
stopped") read as if no promotion ever existed.
Command: `git show 4cc1ac11:PROVINCE.md | grep -n 'Round-44'` → `424:## Round-44 additions to Core`, `430:… moved Frontier → Core …`; `git show 55bcce69:PROVINCE.md | sed -n '422,424p'` → `## Round-44 measured, not promoted (R44-C1 honest stop)`.
Observed: two commits with the promotion live, then withdrawal. Smallest safe correction: one
sentence in the lesson, LOG bullet and SCORECARD row — "the Core row was landed at `4cc1ac11`,
scored `met_target true`, and withdrawn at `55bcce69`; the headline describes the final state".

**FV-3 — high (severity understatement of M44-2).** The 8 frozen files are the `CTL-C1-POS`
positive control's inputs, regenerated (new `evidence_id`s, `provider_id 1239772:1 → 2463841:1`,
knowledge fixture 16880 → 20280 B, 247 changed lines; table §5).
Command: `git diff --name-only c48f8a4 c86ea508 -- tools/round-44/control-fixtures/ | wc -l` → `8`;
`git show c48f8a4:<p> | sha256sum` vs `git show c86ea508:<p> | sha256sum` differ for all 8.
Observed: the control ledger (`controls/summary.json`, `CTL-C1-POS stdout_sha256 88900939…`) is
reproducible only at `≤55bcce69`, and the tip cannot re-run any control (both counters exit 2
first). Smallest safe correction: state in M44-2 and `SCORECARD.md:3530` *what* the commit
regenerated and that the positive control's inputs no longer exist at the tip.

**FV-4 — medium (the "fix" is an unwired, pathspec-scoped script).** `SCORECARD.md:3530` calls
`tools/round-45/frozen-path-preflight.py` "the fix"; it is invoked nowhere and, given only
`--pathspec tools/round-44`, is green when a frozen path outside that pathspec changes.
Command: `grep -rn frozen-path-preflight --include='*.py' --include='*.sh' . | grep -v '^./tools/round-45/frozen-path-preflight.py'` → documentation only; fixture probe (transcript
`artifacts/R44W2FreezeViolation/gate-probes.txt`, case D) → `gate --pathspec tools/round-44` exit
**0** with `plans/claims.md` mutated, exit **1** with the claims pathspec. Also: no-pathspec at the
clean `55bcce69` → exit 1 (`touched 557`), and the backstop is skipped without a pathspec
(`:69`). Smallest safe correction: call it a candidate gate, make `--pathspec` required or add
`--claim <claims.md>` deriving the list, run the backstop when no pathspec is given, and add
`--selftest` for the four red arms.

**FV-5 — medium (duplicate criterion id).** `corpus/QUALITY.md:139` labels the new rule
"Row 77 (freeze paths are gated at commit time, not at scoring time)", but row 77 is the round-36
self-assessment rule at `corpus/QUALITY.md:85`, and the highest id before the append is 85, so the
next free id is 86. `SCORECARD.md:3530` and `LOG.md:3203` cite "QUALITY 77" for the freeze-path
rule, which resolves to the wrong rule for a reader following the citation.
Command: `grep -cE '^\| 77 \|' corpus/QUALITY.md` → `1`; `grep -nE '^\| 8[0-9] \|' corpus/QUALITY.md`
→ `92:| 84 |`, `93:| 85 |`.
Smallest safe correction: relabel the bullet "Row 86 added after the round" (convention:
`corpus/QUALITY.md:135`, "Row 76 added after the round") and fix the two citations.

**FV-6 — low (the "tip" receipt is one commit behind the tip).** The at-tip receipts name
`c86ea508`; the current tip is `8bb1090a`. The claim is still true, but not of the revision the
receipt names.
Command: preflight `--rev 8bb1090a --pathspec tools/round-44` → exit 1 (8 touched, 8 blob);
`.ufo/waves/round-44/l1/c1-score-at-tip.json` argv names `--rev c86ea508…`.
Smallest safe correction: either re-take the at-tip receipts at `8bb1090a` or write "at `c86ea508`
(and at `8bb1090a`, the record commit)".

**FV-7 — low (precision).** `corpus/lessons/round-44.md:16` says the commit "added/edited 8 files";
all 8 statuses are `M` and none is `A`, and that wording invites the additions-only reading
rebutted in §2.
Command: `git log --name-status --format='%h %s' c48f8a4..c86ea508 -- tools/round-44/` → 8 lines,
every one starting `M\t`.
Smallest safe correction: "modified 8 committed files (no additions)".

## 9. What the report must say for the round not to be a misrepresentation

1. **Name the violation precisely**: `c86ea508` **modified** 8 committed files under
   `tools/round-44/control-fixtures/`, in `FREEZE..tip`, and the clause broken is the claim's own
   (`plans/round-44-claims.md:77-83`, `:311`, `:242`) — not an unwritten convention.
2. **State the admissible revision and the proof it is admissible across the whole claim**: check 9
   (12 pathspecs, exit 0) and check 5 (rule and instruments unmoved). Say it is the *last clean
   ancestor*, not "the tip".
3. **State the tip's status semantically**: both counters `exit 2` / `frozen_path_changed`, C2
   `entries_evaluated 0`, and *a 2 counts toward no target*. Say it at the current tip and at the
   revision the receipt names.
4. **Never quote the at-tip `mismatches []` or `carriers_matched 0` as a result** — they are the
   "could not evaluate" payload (`usable_as_claim_score false`).
5. **Say what the 8 files were**: the positive control's receipts and landing fixture, regenerated;
   the control ledger is reproducible only at `≤55bcce69` and no control arm can run at the tip.
6. **Say the C1 landing was promoted then withdrawn**: Core row live at `4cc1ac11`/`9d3d1862`,
   `met_target true` at `4cc1ac11`, withdrawn at `55bcce69`; "measured, not promoted" is a
   final-state statement.
7. **Give the C1 stop's exact ground**: the receipts' `output_directory` lacks the amendment's
   committed-path segment, and the frozen counter does not test that clause — so the `4cc1ac11`
   `met` is not a valid met against the claim prose. Do not write "unsatisfiable" without also
   saying a composite scratch path would satisfy both clauses.
8. **Carry both C2 qualifiers in every summary**: `met@55bcce69`, inadmissible at the tip; the
   calibration axis move rests on that.
9. **Describe the freeze-path gate as a candidate, unwired, pathspec-scoped script**, with the
   four red arms and the blind spot named — not "the fix".
10. **Give the revision each cited receipt lives at**: `controls/summary.json` and
    `l1/c1-score-4cc1.json` land at `c86ea508`; a reader re-deriving `55bcce69` will not find them.

Items 1, 2, 4 and 8 are present today; 3 is present for `c86ea508` but stale for `8bb1090a`;
**5, 6, 7, 9, 10 are missing or wrong** (FV-1…FV-5).

## 10. Limits of this review; no-change statement

- I re-derived the freeze facts and the gate behaviour myself; I did **not** re-run either frozen
  counter (peer seats `R44W2C1Rescore`/`R44W2C2Rescore` own that), re-derive all 80 C2 entries, or
  run REA. Counter claims rest on the committed receipts plus my independent preflight re-derivation.
- Fixture probes use throwaway repos (`mktemp -d` under my scratch, `git -C "$D"` on every call,
  `rev-parse --show-toplevel` asserted equal to `$D` before the first commit); they test git
  semantics, not the lane.
- Every git invocation was read-only (`log`, `show`, `diff`, `rev-parse`, `merge-base`,
  `ls-tree`, `name-status`). No mutating git/jj command was run anywhere. No fleet-root file, no
  sibling lane, no `.ufo/state/`, no `MANIFEST.json` was touched. No tool was installed or upgraded
  (nothing was needed; pacman not used).
- Files I wrote: this report and `artifacts/R44W2FreezeViolation/` only. My scratch
  `/fast/scratch/hyaku/kaidoku-r44/R44W2FreezeViolation/` was removed before yielding.

## Receipts (seat `R44W2FreezeViolation`, 2026-10-28)

All paths absolute; `P=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-45/frozen-path-preflight.py`,
`L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `F=c48f8a4bfd449300c975668e59aae5b5538b6a84`.

| command | exit | stdout sha256 (first 32) | wall s | observed |
|---|---|---|---|---|
| `python3 -I -B $P --root $L --freeze $F --rev c86ea508… --pathspec tools/round-44` | 1 | `20a87d4d81eedaa79defea6c0fcbbe24` | 0.100 | `frozen_path_changed`, 8 touched, 8 blob |
| `python3 -I -B $P --root $L --freeze $F --rev 55bcce69… --pathspec tools/round-44` | 0 | `c8a03c2673a9bfd52b23077a604e4828` | 0.098 | `clean` |
| `python3 -I -B $P --root $L --freeze $F --rev 8bb1090a… --pathspec tools/round-44` | 1 | `c302813c8069f581e4674d3f5335f9a8` | 0.096 | `frozen_path_changed`, 8/8 |
| `python3 -I -B $P --root $L --freeze $F --rev 8bb1090a…` (no pathspec) | 1 | `ea8cfe7638b88ed0319ac7c987e6f288` | 0.034 | `touched 557`, `blob_changed 0` (backstop skipped) |
| `python3 -I -B $P … --rev 55bcce69…` + 12 claim pathspecs | 0 | `3421dfe2475829b33f6a9fd06c445af5` | 1.207 | `clean` |
| `python3 -I -B $P … --rev c86ea508…` + 12 claim pathspecs | 1 | `fc4173fb17a9c944a2bf8783c951d257` | 1.235 | `frozen_path_changed`, 8/8 |
| `python3 -I -B $P … --rev 4cc1ac11…` + 12 claim pathspecs | 0 | `a6327b884ae3e35a602c158777849ddc` | 1.136 | `clean` |
| `bash gate-probes.sh $S` (fixture red arms A–F) | — | transcript `artifacts/…/gate-probes.txt` | — | A=1, B=1, C=1, D=0/1/1, E=0, F=1 |
| `git log --oneline c48f8a4..c86ea508 -- tools/round-44/` | 0 | — | — | only `c86ea508` |
| `git log --name-status … c48f8a4..c86ea508 -- tools/round-44/` | 0 | — | — | 8 × `M` |
| `git diff --stat 55bcce69 HEAD -- <claims,counters,rubric,carriers>` | 0 | — | — | empty |
| `python3 -c … counter-at-4cc1.json` | 0 | — | — | `exit_code 0`, `met_target True`, `carriers_matched 4` |
| `git show 4cc1ac11:PROVINCE.md \| grep -n 'Round-44'` | 0 | — | — | `424:## Round-44 additions to Core`, `430:… moved Frontier → Core` |
| `grep -cE '^\| 77 \|' corpus/QUALITY.md` | 0 | — | — | `1` (row 77 is the round-36 rule, `:85`) |
| `grep -rn frozen-path-preflight …` (excl. itself) | 0 | — | — | documentation only; no invocation |

Artifacts: `artifacts/R44W2FreezeViolation/{receipts.json,preflight-receipts.json,
preflight-claimset-receipts.json,gate-probes.txt,preflight-*.stdout.json}`.
