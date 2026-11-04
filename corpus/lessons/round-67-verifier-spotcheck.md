author: hyaku closure (non-author integrator, @m_zfl)
lane: kaidoku · round 67 (attempt 1) · base `a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92` · tip `451f3102c1be3fe476b8c600979eba5ecaade1f8`
report: `.ufo/reports/round-67/kaidoku.md` (fleet commit `e6ebf771`, lane identity)
closure: `CLOSURE kaidoku r67 status=ok admitted=false` — `rejected-harmed`, quality trend

This file is the non-author verification required by `LEARNING.md` §"Discernment is checked from
outside" and `PROTOCOL.md` §Round-robin closure. It re-checks the round from committed bytes; it did
not author any round artifact. All commands below were run by the closure on 2026-11-04 against the
lane repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless a path says otherwise. No lane
gate or instrument was executed (the lane's tools are its own write scope); where a claim rests on
one, its committed receipts were verified and the claim is marked **evidence-verified**, never
re-executed.

## 1. Step-1 conformance (status-neutral defects named)

| item | command | observed |
|---|---|---|
| report committed by the lane identity | `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H %ci' -1 -- .ufo/reports/round-67/kaidoku.md` | `kaidoku-shokunin <kaidoku@shokunin.local> e6ebf771… 2026-11-03 22:16:15 -0300` |
| report lands last | lane tip `451f3102` (22:14:48) < report `e6ebf771` (22:16:15) | holds; report cites the tip 3× |
| report scope | `git -C /home/vgpnk/Projects/shokunin show --stat --format= e6ebf771` | 1 file, `.ufo/reports/round-67/kaidoku.md`, 189 insertions |
| cited lane commits exist and are ancestors | `git cat-file -e <h>^{commit}` then `git merge-base --is-ancestor <h> 451f3102` for every 7–40-char hex token in the report | 19 lane hashes: all exist, all `merge-base` exit 0 (`1e7fe7b7 2dd5f2cd 3663e6b2 39a91a99 3e7b59db 451f3102 454071dd 4c2c85d3 66389549 6dcc447e 7a3c21d4 7cfe83e4 83239917 8672cf40 a4c1d0fc a7a4ce69 cf705c53 eadc2188 ecc4de0e`); `e3dcf177` is the upstream squashfs-tools-ng commit cited by S268, not a repo commit |
| lane pushed, no uncommitted round work | `scripts/hyaku/jj-lane.sh state …/kaidoku-shokunin`; `git status --porcelain` | `branch=main local=451f3102 remote=451f3102 ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty |
| `SHONEN` heading, one line per box | `grep -n '^## SHONEN' -A5 .ufo/reports/round-67/kaidoku.md` | heading present; 4 `[~]` lines, each with a pointer; `SHONEN.md` untouched by the round (`git diff --stat a7a4ce69 451f3102 -- SHONEN.md` empty; `grep -c '\[x\]' SHONEN.md` = 0) |
| dispatched prompt carries the template contract | `wc -l .ufo/prompts/kaidoku-round-67.md` = 704; sections 1, 2, 2b, 3, 4, 5 compared against `templates/round-prompt.md` | sections 1–5 are the template rendering verbatim with the lane/round substitutions (`sed`-rendered template vs prompt lines 1–140: `diff` exit 0, only the `<repo>` name substituted); the five child-lane items (report path, commit-before-report, `SHONEN` heading, hash-citation rule, lane write scope) are present; §3 carries the L2 floor (≥8, one batched call) and the route-table deferral |
| L2 route map vs `MISSION.md` | prompt §6 addendum lines 143–149 vs `MISSION.md` §L2 concurrency | §3 quotes the template's route-table deferral; the addendum carries the run-15 map plus the 2026-11-03 amendment ("ONLY reviewer uses `@m_zfl`") and is self-superseding; `MISSION.md` holds role-class buckets only (advisory), so no bucket contradicts the prompt |
| dispatch/completion digest | `grep -nE 'launch kaidoku round=67' .ufo/watchdog.log`; `grep -nE 'complete kaidoku round=67' .ufo/watchdog.log` | `2026-11-03T21:37:59-03:00 launch kaidoku round=67 pgid=2346633 driver=hyaku-inline attempt=1`; `2026-11-03T22:16:38-03:00 complete kaidoku round=67; hyaku-inline attempt=1` |

Conformance defects (recorded, never status-changing here):

1. **Wrong prompt-commit citation.** The report (line 4) says the round-67 prompt is "committed
   `b8507c60`". `b8507c60` is the fleet commit adding `.ufo/prompts/kaidoku-round-66.md`
   (`git show --stat b8507c60` → `kaidoku-round-66.md | 704 +`). The round-67 prompt landed at
   `754f9074` (`git show --stat 754f9074` → `kaidoku-round-67.md | 704 +`, lane identity,
   2026-11-03 21:37:58). The hash, not the content, is wrong; route as a report erratum.
2. **QUALITY #47 prefile gate exits 1 at filing.** The report pastes `prefile: FAIL` (round-24 gate
   `--disclosures corpus/claim-freezes.tsv` exit 1; round-29 gate `--disclosures corpus/claim-freezes-v2.tsv`
   exit 0) and discloses the cause; no receipt for the prefile output is committed, only the paste
   (`grep -rl prefile .ufo/waves/round-67/` → no file). Disclosed defect, routed.
3. **QUALITY #100 same-round ledger correction lacks its companion record.** `corpus/claim-freezes-v2.tsv`
   row `round-64` was appended at `8672cf40` and its findings cell rewritten in place at `451f3102`
   (`-INSTRUMENT_UNRESOLVED mkcache.js; INSTRUMENT_UNRESOLVED view8.py; INSTRUMENT_UNPINNED tools/round-64/jsc-route-matrix.py`
   → `+INSTRUMENT_UNPINNED,INSTRUMENT_UNRESOLVED`). The row was still unfiled at the edit (same round),
   but QUALITY #100's exception requires a companion row in `corpus/claim-freezes-corrections.tsv`
   plus LOG and lesson disclosure: `git diff 8672cf40 451f3102 -- corpus/claim-freezes-corrections.tsv`
   is empty and no lesson row names it. Routed.
4. **Instrument registry rows missing for both round-67 gates.** `SKILL.md`'s instrument registry
   (between the registry markers; entries run to `tools/round-66/coverage-selfcheck.py` at line 1857)
   has no row for `tools/round-67/avm-le-counter.py` or `tools/round-67/mutation-battery.py`
   (`grep -n 'round-67\|r67\|R67' SKILL.md` → no match). Under PROTOCOL §Gate standard (Registry +
   Delivery) neither new gate is graded conformant until its row exists; the report's SHONEN box-1
   pointer ("`SKILL.md` instrument registry rows (round-66/67 counters)") is true only for the 66
   rows. Status-neutral, routed.

## 2. Claim re-check

Method split: **re-measured** = a count/digest computed by the closure from committed bytes;
**evidence-verified** = a lane instrument's committed receipt inspected against its pins and its
named revision (never executed). Neither claim was executed end-to-end: the four AVM carriers are
not on this host (`ls /fast/scratch/hyaku/kaidoku-r67/carriers` → absent; AVM licence S249 forbids
committing them), so the extraction event itself is only as good as its committed receipts.

### R67-C1 — coverage (frontier → core)

| check | command | observed |
|---|---|---|
| before: round-50 rule vs round-67 rule over the same four envelopes | `jq '{g50:.gaps_ok_round50,g67:.gaps_ok_round67}' .ufo/waves/round-67/l1/pre/control-dryrun.json`; per-carrier booleans counted from `.per_carrier` (2 true of 4 for `gaps_ok_round50`, 4 of 4 for `gaps_ok_round67`; exact command in the block below) | `g50 = 2`, `g67 = 4`; the two failures are `g7581`/`g7582`, note `required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/pts/0' … 'dev/pts/7']` (the 8 of 12 char-device rows the note truncates); receipt `rev a7a4ce69`, `control_ok true`, exit 0 |
| red controls | same receipt `.red_controls` | `round67_rule_still_fails true` (dropped symlink gap `bin/adsl`), `publication_check_names_it true` (`dev/led` published as a regular file), `junk_rule_would_pass true` (a rule that waives symlinks passes the first red fixture) |
| after: landing and record | `jq '{rev,carriers_matched,target,met_target,exit_code,failing,bindings_false,carriers_unchanged,gap_rule_unchanged}'` on `l1/scores/c1-at-landing.json` / `c1-at-record.json` | landing `rev 83239917…`: `4/4`, `met_target true`, exit 0, `failing []`, `bindings_false []`, `carriers_unchanged true`, `gap_rule_unchanged true`; record `rev 7a3c21d4…`: identical |
| the engine's 23 clauses on all four carriers | `jq` clause-matrix cross-check (exact command in the block below) | `c6430 23 0`; `c6490 23 0`; `g7581 23 0`; `g7582 23 0`; `patches.dropped_clauses` length 0 |
| envelope digests bound by the receipt | `git show 7a3c21d4:…/after.json` piped to `sha256sum` ×4 vs `.evidence_digests` | `g7581 d10522f2…`, `g7582 af5863b9…`, `c6490 2d6bcaa6…`, `c6430 b6c3f5a4…` — all four match the receipt |
| envelope contents re-counted (re-measured) | `.normalized_result.files` counted and `.normalized_result.extraction_gaps` grouped by `.kind`, per carrier | files `4556 / 4564 / 4709 / 3955` (the report's four counts); gaps `637/637/613/568`, every gap `depth-limited: 1` + `unpublished-entry` of kind `symlink` (636/636/612/567); **no char-device gap record in any envelope**, which is the class rule's point |
| pins the receipts name | `sha256sum` over `git show <rev>:<path>` for the counter, the engine and the rule | counter `b5a660d2…` = receipt `counter.sha256`; engine `9820811b…` = `counter_sha256`; rule `e66ba022…` = `rule_v2_sha256` = freeze bytes = tip bytes |
| surface moved | `git show 2dd5f2cd -- PROVINCE.md corpus/README.md`; `grep` the entry | `## Round-67 additions to Core` row + frontier note in `PROVINCE.md`; Core map row + knowledge row + frontier note in `corpus/README.md`; entry `corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md` cites S268 first and receipt `bindings.entry_source_ids = [S244,S245,S249,S250,S268]` |

Exact commands whose output the table reports (pipes are shell pipes, kept here outside the
table so the table renders):

```sh
jq '{g50:.gaps_ok_round50,g67:.gaps_ok_round67}' .ufo/waves/round-67/l1/pre/control-dryrun.json
jq '. as $r | ($r.patches.clauses) as $cl | $r.carriers | to_entries[]
    | .key as $id | ([$cl[] as $c | select(.value[$c] != true)] | length) as $bad
    | "\($id) clauses=\($cl|length) not_true=\($bad)"' .ufo/waves/round-67/l1/scores/c1-at-record.json
for c in g7581 g7582 c6490 c6430; do git show 7a3c21d4:corpus/evidence/round-67/c1/$c/after.json | sha256sum; done
```

Verdict: **verified, evidence-verified.** The before-arm (2/4 under the round-50 rule) and the
after-arm (4/4 under the class rule) are the arithmetic the receipts carry; the closure re-derived
the per-carrier clause matrix, the envelope digests and the publication/gap counts from committed
bytes. The class waiver is class-level, not a per-path escape: `gap-rule-v2.json` sets
`required.char-device = false` with a `class_disposition` block, keeps `removed`/`structural`,
keeps symlinks required, and the two red fixtures show the rule can fail. What is not re-measured
here is the REA extraction event on the four carriers (absent from the host).

### R67-C2 — depth (counter repair)

| check | command | observed |
|---|---|---|
| before: round-66 detectors alone | `jq '{rev,killed_before,survived_before,verdicts}' .ufo/waves/round-67/l1/pre/control-dryrun-c2.json` | `rev a7a4ce69…`, `killed_before 0`, `survived_before 2`, both `r66_selftest_exit 0` with `cases=30` / `cases=26` |
| after: landing and record | `jq '{rev,exit_code,killed_before,killed_after,survived_before,pristine,verdicts}'` on `c2-at-landing.json` / `c2-at-record.json` | landing `rev 2dd5f2cd…`, record `rev 7a3c21d4…`: `killed_after 2`, `killed_before 0`, exit 0, pristine `SELFTEST CLEAN cases=30 failures=0` and `cases=26 failures=0`; exact failed sets `{arm-false-bound}` and `{equiv-doctored-bound, equiv-doctored-diffs}`, each equal to its expected set |
| the mutants are the declared defects | `nl -ba tools/round-67/mutation-battery.py` | closure mutant rewrites the sole `"passed": bool(passed)` to `"passed": True` (hits must be 1); coverage mutant replaces the `subprocess.run…` span with an early `return {…"recipe_a_equivalent": True…}`; both are written under `--work`, never into the repo |
| the kill test is exact-set | battery 382–383 | `killed_after = (after_rc != 0 and set(failed_cases) == EXPECTED_CASES[name])`; `EXPECTED_CASES` = the two sets above |
| case inventory | `.cases` counted in `pre/selftest-c2.json`; battery 255–262 | 10 cases including `case-inventory`; the check compares executed names to the registered inventory, not a count floor |
| freeze binding | `git show 3663e6b2:.ufo/waves/round-67/claims.json` queried at `.instruments[…mutation-battery.py]` = `cabc0a0b…`; receipt `counter.sha256` = `ecf55987…` (first committed at `7cfe83e4`, re-pinned at `eadc2188`) | **freeze equality fails; measured-revision equality holds.** The freeze-era dry run at `3663e6b2` (`l1/pre/score-dryrun-at-base.json`, counter `cabc0a0b…`) already reports `verified true`, `killed_after 2`, `survived_before 2` with the same failed-case sets, so the predicate holds under the frozen instrument as well |
| coverage self-check (standing duty) | `jq` on `l1/scores/coverage-selfcheck-at-record.json`; `git ls-tree -r --name-only <rev> corpus/knowledge` filtered to `*.md` and counted | atoms A1 `10.0/10.0`, A2 `[147,147]/[147,147]`, `mismatches 0`, exit 0; knowledge md files `146` at base → `147` at the record and tip — the cited fraction is the population at the record |

Verdict: **verified, evidence-verified, with the freeze-binding caveat below.** The substantive
predicate (2 of 2 killed, 0 of 2 before, both pristine counters green) is carried by both the
freeze-era receipt and the record receipt; the exact-set kill and the names-based inventory are
present in the committed battery. The freeze-era instrument already reached the same verdict, so
the claim is not falsified by the disclosed post-freeze repair.

**Ruling on the report's routed item 4 (ExecPins F1).** The claim's frozen `kill_rule` names "a
post-freeze instrument edit" without the word *undisclosed*; the record receipt runs the repaired
battery. The lane's standing criterion QUALITY #33 (a later instrument change is allowed as an
appended `instrument_supersessions` entry with reason and a re-taken before record; an *undisclosed*
change is the finding) is the criterion under which the freeze is judged, and the container carries
five disclosed supersessions with re-taken before records. The closure reads the kill rule as the
undisclosed case it exists to prevent, and confirms the predicate independently under the frozen
bytes (`score-dryrun-at-base.json` at `3663e6b2`, counter `cabc0a0b…`: `verified true`,
`killed_after 2`). The reading is accepted; the wording is routed for the next round so the rule
says what it means.

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | **improved** | the `squashfs_v4_le` LE AVM surface moves Frontier → Core on the four chain-pinned carriers: `PROVINCE.md` `## Round-67 additions to Core`, `corpus/README.md` map row, entry, and the 4/4-vs-2/4 control; the 0–10 score stays 10.0 (saturated; the move is a surface, not a re-score) |
| depth | **improved** | the two round-66 mutation survivors are closed by exact-set cases (`arm-false-bound`; `equiv-doctored-bound`/`equiv-doctored-diffs`) with both pristine counters green and a names-based inventory; the r66 counter receipts now carry their revision |
| calibration | **unchanged** | no calibration claim this round; the coverage row's cited fraction is re-derived at the population change (146 → 147), `mismatches 0`; no SCORECARD claim was found contradicted by the receipts. The stale entry text below is recorded as quality, not calibration |

No owned axis is harmed. The admission bar is nonetheless not met because the quality **trend** is
harmed (see §5).

## 4. Discernment spot-check (non-author)

Every row was re-opened from the live URL/bytes and from the committed copies; the closure ran the
fetches itself (the reviewer seat repeated them independently and agreed).

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| (a) S268 admit | admit | `https://raw.githubusercontent.com/AgentD/squashfs-tools-ng/e3dcf1770fd77a0babcca422dcbe7b2cc7b8ab90/doc/format.adoc` — HTTP 200, 41 981 B, sha256 `08c38b69…c82eb` | **agree** | live bytes byte-identical to the committed copy; `=== Device Special Files` at line 730, quote at line 732 (13 words, one occurrence, offset 28 445), major/minor extraction at 745–746 (`742-746` block), type codes 5/12 at 549/556; tier A for the on-disk-layout scope |
| (b) kernel docs reject | reject as this round's row | `https://docs.kernel.org/filesystems/squashfs.html` — HTTP 200, 26 045 B, sha256 `10767bbf…33685` | **agree** | the §3.2 class sentence exists (line 412) but the page states no device-number field: `major` 0, `minor` 0, `rdev` 0 occurrences in the bytes; it cannot ground the field set the class rule rests on, and it is unversioned rendered HTML |
| (c) plain `.rst` reject | reject | `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/filesystems/squashfs.rst` — HTTP 200, 14 201 B, sha256 `e709573a…ba5f9` | **agree** | same paragraph at 184–186, but the URL carries no tag, commit or `?h=`, so the anchor rule's "plus revision" is unmet |
| (d) receipt-as-source reject | reject as a source | committed `l1/pre/control-dryrun.json` (`rev a7a4ce69`, `gaps_ok_round50 2`, g7581 note naming `dev/pts/0`–`dev/pts/7`) | **agree** | a receipt shows one rule's red arm on one carrier; it cannot establish why the class is not publishable — the ground is the format's field set, which is what S268 supplies |
| S268 row | admit as authored | `corpus/SOURCES.md:185` at `451f3102` (11 columns; `docs`/`A`/`mined`; `used-by` entry exists at the tip; quote 13 words) | **agree** | id unique, anchor carries commit + digest, `opened 2026-11-03`, `recheck 180d`, status `mined` satisfied by an existing entry, no literal pipe character in a cell |

Spot-check verdict: **agree on all five items** (the one admit, all three rejects, the row's
shape). One incident was found outside the five gate items and is recorded in §6 as a quality harm.

## 5. Trend verdicts and admission

| trend | verdict | evidence |
|---|---|---|
| expansion | **improved** | one admitted `corpus/knowledge/` entry on ground held only as Frontier, its `source:` citing S268 (`mined`, `used-by` names the entry), with the map row and the PROVINCE Core row; registry `174 → 175` rows, tier `A=160 → 161`, status `mined=165 → 166`, malformed 0, the same 19 W04 (census re-run: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` exit 0) |
| quality | **harmed** | `corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md:33` states the round-67 rule is `sha256 b55d5e87…` and "keeps … `removed` (including `removed.silent.char-device = ["247:0"]`)". At the record and at the tip the rule is `e66ba022…` and its `removed` block has no `silent` key (the rule's `.removed` read from `git show 451f3102:tools/round-67/gap-rule-v2.json` → `{"diagnostic":"MaliciousSymlinkRemoved","kinds":["symlink"],"disposition":"exclusive"}`). `b55d5e87…` existed only between the wave-1 repair `7cfe83e4` and the revert `3e7b59db`; the entry blob is unchanged since `2dd5f2cd` (`f520968a…` at `2dd5f2cd`, `3e7b59db`, the tip) and no correction block marks the superseded sentence. The lane's M67-5 corrected the rule and the wrapper docstring but not the entry — the "corrections sweep every mention" rule left a sibling mention standing. LEARNING.md's quality harm condition ("an entry is found false or stale and left unmarked") fires literally; also `plans/round-67-claims.md:59` still claims a `carrier_fresh_ok` clause drop while the shipped `dropped_clauses` is `[]` |
| discernment | **improved** | the outside spot-check agrees with the gate on the admit and on all three rejects (§4); the round mined nine mistakes (`M67-0` … `M67-8`, each with class · evidence · captured-by · fix) and added four grounded criteria (QUALITY rows 107–110, each citing its lesson row); the wave found defects the L1 freeze missed (`F0`, `F1`–`F6`, `M1`, `N1`–`N5`) and each is repaired with a disclosed supersession or routed in the lesson |

**Admission: false.** Both claims verify, and no owned axis is harmed, but LEARNING.md is explicit:
"`expansion: improved` with `quality: harmed` is a trade, reported as a trade, never admitted."
This row is recorded `ok` (the report is real, its work is committed, its hashes resolve) and
`rejected-harmed` (quality), matching the kasegi-46 reconciliation precedent.

## 6. Routed defects (the lane must close these next round)

1. **Quality harm — the promoted entry misdescribes its instrument.**
   `corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md:33` must be corrected by an appended
   correction block that names the superseded sentence, the sha it cited (`b55d5e87…`), the rule
   now at the pin (`e66ba022…`) and the silent row's absence; never by an in-place rewrite. The
   lesson and LOG disclose the correction. `plans/round-67-claims.md:59` gets the same treatment
   (or an explicit "frozen plan, superseded by A4/M67-4" note).
2. **Instrument registry rows missing (PROTOCOL §Gate standard, Registry + Delivery).** Add
   registry rows for `tools/round-67/avm-le-counter.py` and `tools/round-67/mutation-battery.py`
   to `SKILL.md`'s instrument registry: name, gate/probe, entry command, verdict map, selftest
   command and spelling, pinned-value path, write scope, owner. The report's SHONEN box-1 pointer
   must then name the rows it actually has.
3. **QUALITY #100 companion record.** Append the correction row for the round-64 findings cell to
   `corpus/claim-freezes-corrections.tsv` (`correction-id`, `corrects`, `field`, `was`, `now`,
   `cause`, `receipt` = `451f3102`, `utc`), and disclose it in LOG and the lesson.
4. **Prefile gate (QUALITY #47).** Commit the prefile-check output as a receipt next round (this
   round's evidence is the report paste only), and settle the superseded `corpus/claim-freezes.tsv`
   (15 missing rounds 53–67, one stray `round-35` row): retire it with a named erratum or backfill
   it from the round-24 gate's own verdicts. The `-v2` ledger is exact at 42 rows.
5. **Kill-rule wording.** Make the frozen C2 kill rule say "undisclosed post-freeze instrument
   edit", so the ruling in §2 is textual rather than interpretive.
6. **Receipt `rev` provenance.** `l1/pre/score-dryrun-at-base.json` and its sibling carry
   `rev = a7a4ce69`, a revision where `tools/round-67/mutation-battery.py` does not exist
   (`git show a7a4ce69:…` absent). Name the instrument-bearing revision (or state "instrument
   absent at base; control reads pinned r66 counters only") in the next round's receipts.
7. **Report erratum.** The prompt hash in the report line 4 is `b8507c60` (round-66 prompt); it is
   `754f9074`. Land the erratum in the next report or as an appended erratum after the filed bytes.
8. **Carry the lane's own routed list**: MutBattery Probe B (no-extra-failures clause), the REA
   `package.json`+tree-digest pin, the r63 planned record-section sweep, the r58/r60 bare-name and
   r64 placeholder-token debt.

## 7. SHONEN and promotion

The report's SHONEN lines are `[~]` (author-asserted) for all four boxes; no `[x]` was written by
this closure and `SHONEN.md` is untouched. As a non-author I did not check the boxes. Boxes 1–3 look
checkable by an operator or a future non-author reviewer against the registry rows (once defect 2
is fixed), `LOG.md`, and the instrument docstrings; promotion remains operator-owned.
