# R39MistakeHunt — round-39 lesson mining (wave 1, pre-freeze)

**Verdict: DEFECTS FOUND** — five mistakes from rounds 36–38 that no `M36-*`/`M37-*`/`M38-*` row records, four of them with a fix demonstrated red→green (one of the four is live in this wave's own context). One of the five also falsifies a sentence inside an existing M38 row.

Seat: `R39MistakeHunt` (leaf, critic). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base
`a2f64e1da78afcf8cc39287106604dbcc270844c` (`main`), lane tip at read time `a2f64e1d`.
Read-only git only; nothing installed; no REA run; no carrier touched (K1–K6 untouched, no held-out material opened).
Scratch `/fast/scratch/hyaku/kaidoku-r39/R39MistakeHunt`, removed at end.
Report path: `.ufo/waves/round-39/w1/R39MistakeHunt.md`. Artifacts: `.ufo/waves/round-39/w1/artifacts/R39MistakeHunt/`.

The ticket's `M37-*` family does not exist: round 37 filed no lesson file at all
(`ls corpus/lessons/round-37.md` → *No such file or directory*; `git ls-files corpus/lessons | grep -c round-37` → 1,
the verifier spot-check only). Sweep 1/2 below is the receipt. So every round-37 mistake is, by construction,
unrecorded — R37-CL1..CL3 are the only trace, and they live in a closure file.

## 1. Sweep (commands + output)

Full capture: `artifacts/R39MistakeHunt/sweep.txt`.

```
######## SWEEP 1: lesson rows present per round
-- corpus/lessons/round-36.md: 7 M-rows
-- corpus/lessons/round-38.md: 9 M-rows
ls: cannot access 'corpus/lessons/round-37.md': No such file or directory

######## SWEEP 2: ids in each lesson/closure
corpus/lessons/round-36.md: M36-1 M36-2 M36-3 M36-4 M36-5 M36-6 M36-7
corpus/lessons/round-38.md: M38-1 M38-2 M38-3 M38-4 M38-5 M38-6 M38-7 M38-8 M38-9 R36-CL1 R37-CL1 R37-CL2 R37-CL3
corpus/lessons/round-38-verifier-spotcheck.md: M38-5 M38-6 R36-CL1 R37-CL1 R38-CL1 R38-CL2 R38-CL3 R38-CL4
corpus/lessons/round-37-verifier-spotcheck.md: R36-CL1 R36-CL2 R37-CL1 R37-CL2 R37-CL3
corpus/lessons/round-36-verifier-spotcheck.md: M36-3 M36-4 R36-CL1 R36-CL2 R36-CL3 R36-CL4 R36-CL5 R36-CL6

######## SWEEP 3: routed ids in round-38 lesson vs round-38 spotcheck
R36-CL1 R37-CL1 R37-CL2 R37-CL3          <- round-38 lesson
R36-CL1 R37-CL1 R38-CL1 R38-CL2 R38-CL3 R38-CL4   <- round-38 closure

######## SWEEP 4: stray files in lane/fleet
?? .ufo/waves/round-39/
?? plans/round-39-claims.md
fleet: (nothing)

######## SWEEP 5: unblob.log locations
ls: cannot access '/home/vgpnk/Projects/shokunin/unblob.log': No such file or directory
-rw-r--r-- 1 vgpnk vgpnk 2652 Oct 26 03:56 unblob.log   (tracked; M38-7's intentional copy)

######## SWEEP 6: round-39 wave-1 committed?
0        <- files under .ufo/waves/round-39/ in the tree at HEAD
12       <- wave-1 .md reports on disk at sweep time (13 by the end of the seat)

######## SWEEP 7: ledger report-pointer shapes
.ufo/waves/round-36/w1-results.json 43 {'repo_rel': 27, 'absolute': 4, 'repo_name_prefix': 2, 'prose_suffix': 0, 'none': 10}
.ufo/waves/round-36/w2-results.json 36 {'repo_rel': 29, 'absolute': 2, 'repo_name_prefix': 0, 'prose_suffix': 0, 'none': 5}
.ufo/waves/round-38/r38-w1-results.json 40 {'repo_rel': 25, 'absolute': 0, 'repo_name_prefix': 0, 'prose_suffix': 1, 'none': 14}
.ufo/waves/round-38/r38-w2-results.json 44 {'repo_rel': 35, 'absolute': 0, 'repo_name_prefix': 0, 'prose_suffix': 1, 'none': 8}
```

Candidates named in the ticket and already recorded (checked, not re-mined): R38-CL1 false absence (routed,
`corpus/lessons/round-38-verifier-spotcheck.md` §5.1), R38-CL3 overstatement (routed, §5.3), R38-CL2 unregistered
gates (routed, §5.2, re-stated inside M38-2's fix column), unblob.log misroot (M38-7 — no new misroot found: fleet root
clean, lane copy tracked, `unblob.log` absent from `/home/vgpnk/Projects/shokunin`).

## 2. Rows for `corpus/lessons/round-39.md` `## Mistakes`

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M39-1 | **handoff ledger** — a closure's routed defects are dropped by the next round instead of carried with a state; one routed defect was closed by narrative while its required artifact still does not exist | `artifacts/…/routed-ledger-runs.txt` A2/A3: `R36-CL2..CL6` are named in `corpus/lessons/round-36-verifier-spotcheck.md:196-212`, carried forward by `round-37-verifier-spotcheck.md:84`, and appear in neither `corpus/lessons/round-38.md` nor `.ufo/reports/round-38/kaidoku.md` (`routed-ledger.py` → `missing=5/6`). A1: `R38-CL1..CL4` appear in no round-39 file — `plans/round-39-claims.md` and `.ufo/prompts/kaidoku-round-39.md` contain zero `R38-CL` (`missing=6/6`). R37-CL3 demanded `corpus/lessons/round-37.md` `## Gate` decisions; round-38 lesson §"Routed defects (round-37 closure)" calls CL3 addressed ("this section"), and the file still does not exist | the prompt's §6.5/§10 addendum asks the L1 to "turn every … routed defect into a" lesson line, but no check enumerates ids | `artifacts/R39MistakeHunt/routed-ledger.py` (`--closure` × `--next`); selftest green 0 / red 1 (`selftests.txt`) |
| M39-2 | **no wave checkpoint** — a wave's reports exist only in the working tree until the round's last commits, so the round survives an L1 death only because the workspace survived | attempt 1 tip `077e212b` (03:33:18) holds only `.ufo/waves/round-38/{c1,controls}` — 0 files under `w1/` (`git ls-tree -r 077e212b -- .ufo/waves/round-38/`); the driver logged `lane-dead-no-report` at 03:37:05 (`.ufo/watchdog.log:1491`); the 40 wave-1 reports + the wave-1 dispatch stamp were first added by attempt 2 at `3b960fe5` (03:46:44, 484 files), and `r38-w1-results.json` only at `7a1ac7fe` (04:13:36). Same shape in round 36: at its freeze `790561d4` the `w2/` tree is empty; the 36 wave-2 reports are first added at `018ae628`, the round's last commit | driver retry (attempt 2) papered over it; no row | `artifacts/…/wave-checkpoint.py --lane --rev --wave`; B1/B2/B5 red (ledger absent), selftest green 0 / red 1 |
| M39-3 | **the per-seat record cannot bind seat → report** — the wave ledger stores free-form seat output with no schema, so 14/40 and 8/44 round-38 rows carry no report pointer, and the pointers that exist use three incompatible forms | SWEEP 7; `git ls-tree`+ledger join (`wave-checkpoint-runs.txt` B3/B4/B6/B7: `unbound_rows=14 of 40`, `8 of 44`, `5 of 36`, `10 of 43`). Three of the four ledgers hold at least one non-repo-relative pointer: `.ufo/waves/round-36/w1-results.json` rows `R36ScoutQuarantine`/`R36ScribeSources` name `kaidoku-shokunin/.ufo/…` (does not resolve from the lane root), and 6 rows across r36 name absolute host paths. `dispatcher` stores `{'name','agent','output','note'}` verbatim (`scripts/hyaku/inline-dispatcher.py:282`). QUALITY 22 ("reproducible from a retained per-seat record") has no implementing check | the report's liveness sentence reads `manifest's per-seat 'status' field is null for every seat` while result rows have **no** `status` key at all (`results[].keys()` = `name, agent, output, note`) — the schema was described without being read (same class as M38-5) | `wave-checkpoint.py` row binding (a row with no `report`/`report_path`/`artifact` pointer fails) + normalising the three pointer forms; red on both round-38 ledgers, selftest green 0 / red 1 |
| M39-4 | **control receipts re-scored in place: the receipt now certifies the amendment, and one control degenerated into do-nothing while still exiting 1** | `ctl-c1-0-do-nothing.json` argv at `efd5c47a`: `--rev e059ca93 --freeze e059ca93`; at the tip `7e979514`: `--rev f1010f67 --freeze f1010f67` (freeze = the amendment commit). `ctl-c1-1-three-carriers.json`: `carriers_matched 3 → 0` between the two revisions — at the tip it reports the same number as `ctl-c1-0` (`carriers_matched 0`), i.e. the drop-one-carrier control is indistinguishable from do-nothing, and its `exit` stays 1. 6 of 7 receipts record the **generator's** argv (`tools/round-38/gen-controls.py:174,184,193,202` `res['argv'] = sys.argv`), not the counter's, and 6 of 7 `output.revision` values (`a3646b58`, `a4cf495d`, `87dc8502`, `d8fe10c7`, `21028bcd`, `801e2019`) resolve to no object (`git cat-file -e` fails) because they are fixture commits in deleted scratch — the same control mints a different id per run (`801e2019` at `efd5c47a` vs `a3646b58` at the tip; `gen-controls.py` pins `GIT_*_NAME/EMAIL` but no `GIT_*_DATE`). This also **falsifies a clause of M38-2**: "overwrote the C1 control receipts with v2/v3 re-scores under unchanged argv" — the receipts' own `argv` arrays differ | M38-2 discloses the overwrite but not its argv re-point, the control degeneration, or the unresolvable revision; wave-2 `R38W2C2Controls.md` §1 replayed at `efd5c47a` (values were reproducible then, with the generator on hand) | `artifacts/…/control-bind.py --lane --rev --freeze --controls [--freeze-tip]`; C1 red `controls_unbound=7/7`, C2 red `6/7` (c1-0 bound at the freeze only), selftest green 0 / red 1 |
| M39-5 | **a fix that lives only in one wave's hand-written context lapses the next round** (recurrence of M36-6, whose fix was a sentence typed into one spec) | `No \`find\`/\`du\` under \`/fast/scratch\`` is present in `.ufo/waves/round-36/w2-spec.json` and **absent** in `round-38/w1-spec.json`, `round-38/w2-spec.json` and `round-39/w1-spec.json` (`context-rules-runs.txt` D1 = 1 present / 3 ABSENT). The newer M38-7 rule is present only where it was hand-typed: `cd "$S"` appears in `round-39/w1-spec.json` and in neither round-38 spec (D2). No generator emits the context (`templates/round-prompt.md` carries neither rule; `grep -c 'find\|/fast/scratch' templates/round-prompt.md` → 0) | M38-7's fix column names the rule for "next round's contexts" and it was typed in by hand again; no structural carrier | `artifacts/…/context-rules.py --require … SPEC.json…` with a rule table + selftest; D3 red on the live `round-39/w1-spec.json` (`missing=['scratch-no-find-du']`) |

### Is each a defect or a tradeoff the canonical judge could reject?

- **M39-1** is a defect, not a tradeoff: the closure's own §6 requires it, and the lane's evidence for "addressed" is a
  section that never names the id. `corpus/lessons/round-37.md` is a concrete missing artifact, not a judgement call.
- **M39-2** is a defect with conditional harm — attempt 1's reports did survive on disk, so no measured number is wrong.
  The claim is narrow: *nothing in the round required them to be committed, and the driver's retry is the only reason the
  wave was not lost*. A critic could downgrade it to "risk", not "mistake"; the row says exactly that, and the fix is the
  checkpoint check rather than a rewrite.
- **M39-3** is a defect about the record, not about the counts: 40/40 and 44/44 are correct, counted from files in the
  wave directory. What fails is QUALITY 22's "reproducible from a retained per-seat record".
- **M39-4** is a defect: a control whose measurement collapses to the do-nothing value while its exit stays 1 is a
  survivor-control (the same failure family as QUALITY 79/80), and the re-pointed `--freeze` is checkable from the
  receipt's own bytes — no judgement needed.
- **M39-5** is a defect because the rule was already a lesson fix and the loss is mechanical, not stylistic.

## 3. Red → green receipts (all four tools, `--selftest`)

`artifacts/R39MistakeHunt/selftests.txt`, run with `python3 -I -B` under `TMPDIR=/fast/scratch/hyaku/kaidoku-r39/R39MistakeHunt`:

```
==== routed-ledger --selftest     selftest green(complete) rc=0 / red(dropped) rc=1   PASS
==== wave-checkpoint --selftest   selftest green(committed wave) rc=0 / red(lost report) rc=1   PASS
==== context-rules --selftest     selftest green(all rules) rc=0 / red(missing rule) rc=1   PASS
==== control-bind --selftest      selftest green(bound control) rc=0 / red(unbound control) rc=1   PASS
```

Real-run verdicts (files `routed-ledger-runs.txt`, `wave-checkpoint-runs.txt`, `context-rules-runs.txt`,
`control-bind-runs.txt`):

```
A1 round-38 closure -> round-39 claims+prompt     R38-CL1..CL4 DROPPED                    exit 1
A2/A3 round-36 closure -> r37 report, r38 lesson R36-CL2..CL6 DROPPED                     exit 1
B1/B2 r38 w1 @077e212b / @3b960fe5               ledger absent                           exit 1
B3/B4 r38 w1,w2 @7e979514                        26/26 + 36/36 reports found, unbound_rows 14/40, 8/44   exit 1
B5/B6 r36 w2 @790561d4 / @018ae628               absent / 31/31 found, unbound_rows 5/36   exit 1
B7   r36 w1 @7e979514                            unbound_rows 10/43; 2 pointers unresolvable as written   exit 1
D1   find/du rule: r36-w2 present, r38-w1, r38-w2, r39-w1 ABSENT                          exit 1
D2   cd "$S" rule: r39-w1 present, the other three ABSENT (rule typed once)               exit 1
D3   round-39 w1 full rule set                   missing ['scratch-no-find-du'] (live)     exit 1
C1   r38 controls @7e979514 vs freeze e059ca93   controls_unbound 7/7                      exit 1
C2   r38 controls @efd5c47a                      controls_unbound 6/7 (only c1-0 bound)     exit 1
```

## 4. Live impact on round 39 (smallest safe correction, for the L1)

1. **M39-5 is live in this wave.** `.ufo/waves/round-39/w1-spec.json` carries `cd "$S"` (M38-7's fix survived once) but
   not the `find`/`du` restriction; 13 wave-1 reports exist on disk, the wave includes unblob-source and AVM-probe
   seats that `cd "$S"` before running it, and any seat that scans `/fast/scratch` for another lane's tree does so
   unguarded. Cheapest fix:
   add the sentence to the wave-1 context (the L1 owns the spec) or record the omission as disclosed; put both rules in
   the generator so wave 2 cannot lose them.
2. **M39-2 is live and larger this wave.** `git ls-tree HEAD -- .ufo/waves/round-39/` is empty while wave-1 seats are
   producing the freeze inputs (K5/K6 carriers, oracles, symlink tables). If the L1 dies before the freeze commit, the
   round loses the very bytes the freeze needs — worse than round 38, where only reports were at risk. Commit the wave at
   WAVE-DONE before the freeze commit.
3. **M39-1 must be discharged inside round 39.** `plans/round-39-claims.md` and the round prompt name none of
   R38-CL1..CL4; R38-CL1 explicitly requires a lesson correction plus a QUALITY criterion for negative-existence sweeps.
   Add a `## Routed defects (round-38 closure)` section to the round-39 lesson with one line per id and its state.
4. **M39-3/M39-4 shape this round's instruments.** The round-39 counters will again emit controls; bind every receipt to
   `--rev/--freeze`, record the *counter's* argv (not the generator's), pin `GIT_COMMITTER_DATE` in fixture builders so a
   control's fixture id is stable, and keep the wave ledger's `report` pointer mandatory and repo-relative.

Nothing in this report asks the lane to change a scored surface; the rows and the four tools are additive, and each tool
is a probe until the L1 registers it with an entry command, a verdict map and a pinned-value path (R38-CL2's demand).

## 5. Limits

- Rows are mined from bytes in the lane repo, the fleet prompt dir and `.ufo/reports/`; no REA call, no carrier, no
  held-out material, no `tools/round-39/*` execution.
- `git ls-tree 077e212b … == 0 wave-1 files` proves the reports were uncommitted at attempt-1 death; that they existed
  on disk at 03:37 is [INFERENCE] from attempt 2 committing exactly those 40 files nine minutes later plus M38-1 citing
  their findings at 03:30 (`R38ExecAfterK2.md` lines 7-11) — the workspace was never archived, so a byte-level proof of
  the 03:37 disk state does not exist.
- The `output.revision` ids in the control receipts may exist in a scratch fixture repo; they resolve in no retained repo,
  which is the defect. I did not attempt to reconstruct them.
- Tool installs/upgrades: none. sasquatch/sasquatch-v4be 4.5.1 and unblob 26.6.4 untouched, `~/.local/bin` unchanged.
- Scratch `/fast/scratch/hyaku/kaidoku-r39/R39MistakeHunt` removed; the four scripts, their four run logs, `selftests.txt`
  and `sweep.txt` are copied into the artifacts dir (paths above).
