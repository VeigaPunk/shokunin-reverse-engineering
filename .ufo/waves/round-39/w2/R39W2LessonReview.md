# R39W2LessonReview — falsification review of `corpus/lessons/round-39.md` @ `52b0eb2`

**Verdict: DEFECTS FOUND.** The lesson's substantive content verifies — every repo-relative backticked path resolves at the reviewed commit, all five Gate quotes are verbatim and ≤25 words with correct locators, all nine routed-defect states check out against bytes, and the executable fixes for M39-1/M39-6/M39-7 reproduce exactly as cited. Four defects remain, all in the fix-evidence layer: the routed-defect ledger drops two ids its own instrument flags (exit 1 on the landed lesson), the M39-4 instrument cannot parse the round-39 control receipts it certifies, M39-5's green half cites a file absent from the reviewed commit, and M39-3's "green on a committed wave" exists only as a selftest fixture.

Reviewed object: `git show 52b0eb2907c704ed5f184c47b14c723208e5cbbc:corpus/lessons/round-39.md` (101 lines). Line numbers below are that blob's. Every command in this report was run by this seat in this wave; raw outputs are in `.ufo/waves/round-39/w2/artifacts/R39W2LessonReview/`. Scratch `/fast/scratch/hyaku/kaidoku-r39/R39W2LessonReview` used and removed at close. Tooling: nothing installed or upgraded (operator rule 2026-10-19 — no install to record); read-only git only, no VCS mutation.

## Findings

### F1 [medium] M39-2's fix claim "carries every id with a state" is falsified by its own instrument — lesson :29 (fix cell), ledger :87-97

The round-38 closure (`corpus/lessons/round-38-verifier-spotcheck.md` §5) routes **six** ids: R38-CL1..CL4, R36-CL1, R37-CL1. The landed ledger (:89-97) carries nine rows — R38-CL1..CL4 and R36-CL2..CL6 — and drops **R36-CL1 and R37-CL1**. Real run of the lane's own instrument (the tool M39-2 cites):

```
python3 -I -B .ufo/waves/round-39/w1/artifacts/R39MistakeHunt/routed-ledger.py \
  --closure corpus/lessons/round-38-verifier-spotcheck.md --next corpus/lessons/round-39.md
  R36-CL1: DROPPED
  R37-CL1: DROPPED
  VERDICT missing=2/6 ['R36-CL1', 'R37-CL1']   exit 1
```

Against the round-36 closure the same run exits 1 with R36-CL1 dropped (R36-CL2..CL6 all named). No round-39 report exists yet to carry them either: fleet `.ufo/reports/round-39/` has no `kaidoku.md` (the ten files there are other lanes' reports; none names either id). Mitigation: both ids were genuinely fixed in round 38 — R36-CL1's `w2.ready.dispatched` committed at freeze `e059ca93` (round-38 lesson :141-142), R37-CL1's receipts committed by the round-38 last commit — so no open defect is lost. But the ledger re-carries the equally-fixed R38-CL1..CL4 with state `fixed`, so by its own practice "every id" is false, and the fix column fails the very tool it cites. Fix: add the two rows with a state (e.g. `R36-CL1 | fixed (round 38, freeze e059ca93) | …`, `R37-CL1 | fixed (round 38) | …`) or reword the fix cell.

### F2 [medium] M39-4's instrument cannot evaluate the round-39 controls it was fixed to check — lesson :31

`control-bind.py` reads `argv`/`exit` from each receipt. The round-39 control receipts use a different schema: `counter_cmd`/`counter_exit`, no `exit` key (`ctl-c1-1.json` … `ctl-c1-9.json`, `ctl-c2-dev-scores.json`; only `ctl-c1-0-do-nothing.json` uses `argv`). Real run:

```
python3 -I -B .ufo/waves/round-39/w1/artifacts/R39MistakeHunt/control-bind.py \
  --lane <lane> --rev 72359309a052284029f8e0331ef211a67fe4b13b \
  --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b --controls .ufo/waves/round-39/controls
  ctl-c1-0-do-nothing.json: exit=None BOUND
  ctl-c1-1.json … ctl-c1-9.json, ctl-c2-dev-scores.json: FAIL argv_binds_freeze
  VERDICT controls_unbound=9/10   exit 1
```

The underlying practice IS real — byte-checked: each `counter_cmd` contains `--rev aa7a7a03…` and `--freeze 8fcda41c…`, and the receipts land in their own commit `72359309` before data. But the cited instrument false-fails 9/10 on schema drift, and even with the schema fixed it could not certify them: the receipts' `--rev aa7a7a03cc87b075706fcae2ff52879a66500922` resolves in no lane repo (`git rev-parse --verify aa7a7a03…^{commit}` fails — it is a scratch-clone commit), so `revision_resolves` fails too. `control-bind-runs.txt` holds only the round-38 runs (C1/C2) and the selftest — no real-run green on round-39 controls exists or is reachable with the tool as written. The lesson cites only "`control-bind.py --selftest` green/red" (passes, 2 synthetic fixtures) — accurate as written, but the fix's instrument is unable to pass or fail on its own round's artifacts. The schema is also inconsistent within one controls dir (`argv` in ctl-c1-0, `counter_cmd` in the rest).

### F3 [minor] M39-5's green half dangles at the reviewed commit — lesson :32

The fix cell cites "`context-rules.py` red on `w1-spec.json`, green on `w2-spec.json`". At `52b0eb2`, `.ufo/waves/round-39/w2-spec.json` does not exist (`git cat-file -e 52b0eb2:.ufo/waves/round-39/w2-spec.json` fails); it is first added at `e40a25df` (= HEAD, "round-39: wave-2 spec, generator and validated dispatch (39 seats, policy v1)"), a descendant of the lesson commit. The red half verifies at the reviewed commit; the green half is only verifiable at HEAD/working tree, where it does pass:

```
context-rules.py .ufo/waves/round-39/w1-spec.json → exit 1, missing=['scratch-no-find-du']
context-rules.py .ufo/waves/round-39/w2-spec.json → exit 0, complete (all 3 rules)
context-rules.py --selftest → PASS, exit 0
```

So the rule-carrying fix is real, but the lesson commit precedes the file its green run needs — the assigned "every backticked path resolves at 52b0eb2" check fails for this token, as-written and under the `.ufo/waves/round-39/` base.

### F4 [minor] M39-3's "green on a committed wave" is fixture-only — lesson :30

Replicated red: `wave-checkpoint.py --lane <lane> --rev 077e212b --wave .ufo/waves/round-38/r38-w1-results.json` → exit 1 ("ledger absent"). But no real committed wave ledger passes the tool: `wave-checkpoint-runs.txt` B1–B7 are all exit 1 (r38 w1: 14 unbound rows; r38 w2: 8; r36 w2: 5; r36 w1: 10 unbound + 2 missing reports), and round-39 wave 1 has **no results ledger at all** — absent at the freeze `8fcda41c`, at `52b0eb2`, and at HEAD. The only green anywhere is the selftest's synthetic committed-wave fixture (B0, "checkpoint_ok reports=2"). The lesson's "red on `077e212b`, green on a committed wave" reads as two real runs; the green is a fixture (the selftest case is literally named "green(committed wave)", so the author may have meant that — but then the fix column should say so).

### F5 [minor] M39-8's evidence pointer §8 does not exist — lesson :35

`w1/R39SrcSasquatch.md` has sections 1–7 only (`grep '^## '`). The self-reported slip ("my first `bash` call died on a `cd` and ran in the fleet root. It left three curl output files there: `f96fe7.out`, `234826.out`, `f8923e.out`") is in **§7 "Tools, limits, hygiene"**, not §8. The substance verifies (three outputs at the fleet root, removed by the seat); the pointer is wrong.

### F6 [nit] Header "none meets its target" (:6) vs `FREEZE-table-informational`

`ctl-c2-dev-scores.json` holds 10 entries: the 8 named ones (CTL-C2-0..6 + `FREEZE-table-informational`) plus two `.formatfix` re-scores of CTL-C2-5/6 kept alongside the originals (transparent, not in-place). `FREEZE-table-informational` has `met_target true, matched 20` — it is the freeze table itself, not one of the claims' CTL-C2-0..6 kill controls (claims: "Any control at 20/20 stops C2"), so "none meets its target" is defensible for the kill controls but false for that entry as written. "C2: 8 controls" counts the named entries; "C1: 9 controls" ✓ (9 receipts, all `met_target false`). Also S121's Gate row: the located quote comes from `debian/rules` (line 17, inside the cited 15-18 block at tag `sasquatch-v4.5.1-6`), not from the row's URL (`unsquashfs.c`) — disclosed in the row, and independently flagged by `w2/R39W2SrcReopen.md` §4.

### F7 [nit] M39-6's quoted draft phrase is a compression, not verbatim — lesson :33

The lesson quotes the draft predicate's sentence as "POSIX join against the image root /". The draft text reads "POSIX join against the link's own directory with the extraction root as `/`" (`w1/R39C1Harness.md:83-84`); `w1/R39C1AxisFit.md` d.0 (:243-246) quotes it as "resolved POSIX-style against the link's own directory inside the image root". The substance is fully verified (below); only the quotation marks overstate verbatimness.

### F8 [observation, current wave] M39-8's class recurred live in wave 2

`git -C /home/vgpnk/Projects/shokunin status --porcelain` now shows `?? .ufo/waves/round-39/` at the **fleet** root: `/home/vgpnk/Projects/shokunin/.ufo/waves/round-39/w2/R39W2HeldReproB.md` (10085 B, written 14:30 today) — a wave-2 seat report at the fleet root. The lesson's fix ("fleet status shows no round-39 file before the report") was true at wave-1 time (`sweep.txt` SWEEP 4: fleet empty) and is false now. Not a lesson defect — a live misroot by seat R39W2HeldReproB; flagged for the wave.

## Verified clean (what was run and passed)

**Backticked paths.** All repo-relative tokens resolve at `52b0eb2` via `git cat-file -e` (shorthands resolved against the lesson's established bases: `w1/`, `controls/`, `l1/`, `w1-spec.json` under `.ufo/waves/round-39/`; the M39-4 control under `.ufo/waves/round-38/`; `carriers.json` under `.ufo/waves/round-39/c1/`; brace token expanded to the three `tools/round-38/` files). Host paths verified on disk: both shokuknow tsvs exist with the exact stated sha256s (`d8fa9eae…af6d`, `709cddc7…ea43`) and sizes (1204/1177 B); `/home/vgpnk/Projects/shokuknow/merge/kaidoku` exists. External file refs verified at their external locations: S119 `dist/domain/firmware/firmwareAnalysis.js:100` exact; S121 `debian/rules` at tag `sasquatch-v4.5.1-6`. All hashes resolve (`a2f64e1d`, `8fcda41c`, `72359309`, `3c07eed7`, `6fdaf4f1`, `077e212b`, `efd5c47a`, `7e979514`). Only miss: `w2-spec.json` (F3).

**Mistakes table.** All 8 rows have class, evidence pointer, captured-by and a fix; fixes executed:

- **M39-1** — round-38 lesson :80-82 and :96-97 carry the "exists nowhere on this host" sentences rooted at the fleet `find` ✓; `absence-sweep.py`: fleet-only → exit 0 ABSENT on both claims, fleet+shokuknow → exit 1 PRESENT on both (hits exactly the two tsv paths); `--selftest` 18/18 pass, exit 0; `l1/absence/summary.txt` matches line-for-line; QUALITY 82 exists (`corpus/QUALITY.md:90`) with the same gate; the "56/57" figure = QUALITY rows 56/57 (spelling/scope, not root), explained in `w1/artifacts/R39CL1Correction/` (`R39CL1Correction.md:97`).
- **M39-2** — `round-36-verifier-spotcheck.md:196-212` names R36-CL2..CL6 ✓; `routed-ledger-runs.txt` A1 shows the draft dropped R38-CL1..CL4 (exit 1) ✓; `--selftest` PASS ✓ — but see F1.
- **M39-3** — `git ls-tree -r 077e212b -- .ufo/waves/round-38/` = 13 files, **0 under `w1/`** ✓; 43 top-level w1 reports at the freeze ✓; wave-checkpoint red on `077e212b` replicated (exit 1) ✓ — but see F4.
- **M39-4** — round-38 `ctl-c1-1-three-carriers.json` `carriers_matched` 3 at `efd5c47a` → 0 at `7e979514` ✓ (byte-checked both blobs); `--selftest` PASS ✓ — but see F2.
- **M39-5** — `context-rules-runs.txt` D1–D3 ✓ (rule present only in the round-36 w2 spec among r36→r39); live red on `w1-spec.json`, green on `w2-spec.json`, selftest PASS ✓ — but see F3.
- **M39-6** — `sqfs-list.py` on K1 (pin `1cfb6c33…` matches `carriers.json`) outputs `link-to-hello	../hello.txt	escaping` — byte-equal to the frozen `corpus/evidence/round-39/c1/K1/symlinks.tsv`; K2 outputs `var/lib/run-link	../../a/run.sh	in-tree` — byte-equal to the frozen K2 table. K1's `..`-target classifies **escaping** (no clamping), i.e. the frozen containment rule holds and the draft sentence would have flipped it ✓. Draft sentence located (`w1/R39C1AxisFit.md` d.0 :243-246; `w1/R39C1SymlinkK1K4.md` §5 "Freeze-blocking defect" :135; naive-join arithmetic in `artifacts/R39C1AxisFit/superblock-compression.txt:16-18`) ✓.
- **M39-7** — `sqfs-list.py --inspect` on the committed K6 carrier: `"compression": "xz"`, superblock compression id 4, `compressed_data_blocks: 4` ✓ (plus escaping 2 / in-tree 1). Evidence pointers check: `w1/R39Sentinel.md:1-2` ("two freeze-blocking tool-provenance" defects) ✓, `w1/R39C1CarrierK5.md` §7 (non-ASCII corruption) ✓, `w1/R39C2HeldoutGen.md` §3 (writer defects corrected) ✓; the C1 `xz_leg` binding exists in `c1-counter.py` and the control receipt's `xz_leg_detail` shows K6: 4 ✓.
- **M39-8** — the slip is self-reported in the seat's report (§7, see F5) and the fleet was clean at wave-1 time (`sweep.txt` SWEEP 4) ✓ — current state see F8.

**Gate quotes** — all five verbatim and ≤25 words (18/11/10/2/1 words), locators verified against the live bytes: S118 docstring at extractor.py:51-57, quote at :53-55 (lesson says 51-56; the quote is inside the range — nit); S119 at `firmwareAnalysis.js:100` exact; S120 quote at report.py:92, class block 91-98 ✓; S121 at `debian/rules`:17 (block 15-18) ✓; S122 `is_safe_path` def at :34, quote at :36, body 34-39 ✓. S118's opened timestamp (16:39:23Z) verified at `w1/R39SrcUnblobSymlink.md:7`; S122's (17:09:05Z) recorded in `w2/R39W2C1EntryReview.md:42` and `w2/artifacts/R39W2SrcReopen/cells.txt:26`.

**Registry** — `corpus/SOURCES.md` 117 → 122 rows; diff base→`52b0eb2` = 0 removed / 5 added lines (S118–S122), all tier A, status `mined` ✓ (append-only holds). Freeze SOURCES = S118–S121 as the header says (S122 appended after the freeze, consistent with its 17:09 L1 access) ✓. Quarantine slice byte-identical to round 38 (`cmp` True) ✓.

**Routed-defect ledger states** — every state checked against bytes:

- R38-CL1 `fixed` ✓ (corrections at :71-83; QUALITY 82 at `corpus/QUALITY.md:90`; `absence-sweep.py` green/red as above).
- R38-CL2 `fixed` ✓ — `freeze-drift.py --selftest` 8/8 PASS, `intended-doc.py --selftest` 9/9 PASS, `registry-immutable.sh --selftest` 5/5 PASS (incl. `row-deletion` and `row-reorder` cases = "refuses a deleted or reordered row"); `SKILL.md:1328` `### Round-35/37/38/39 instrument registry` ✓.
- R38-CL3 `fixed` ✓ — the fleet report `.ufo/reports/round-38/kaidoku.md:88` still carries the original "would have turned C1 green (v3: 4/4)" (not edited) and the lesson's correction (:82-83) restates it as carrier-green.
- R38-CL4 `fixed` ✓ — `plans/round-39-claims.md:14-24` `## Freeze-integrity rule` states the block-on-touch rule and lists the frozen paths; `c1-counter.py` exits 2 `frozen_path_changed` (:69, :124, :392, :573) and `c2-counter.py` raises `Unevaluable('frozen_path_changed')` (:161).
- R36-CL2 `fixed` ✓ — `PROVINCE.md:384` round-39 frontier note names `2026-10-26-r36-sasquatch-squashfs-recursion` (and the r39 stem).
- R36-CL3 `superseded` ✓ — the re-minted fabrication limit is disclosed in the claims (:79-82, CTL-C1-3) and `w1/R39C1Counter.md` states every red case fails on exactly the clause it targets (33-case selftest).
- R36-CL4 `fixed for round 39` ✓ — claims :20-23 list every frozen path for both claims; `carriers.json` pins carrier/oracle/symlinks by sha256.
- R36-CL5 `open` ✓ — nothing in round-39 addresses it (grep: only the ledger row and w2 scribe notes repeating "open"/"remains open").
- R36-CL6 `fixed for round 39` ✓ — `c1-counter.py` binds `subject_pin_ok` = `subject.digest.sha256` == frozen pin (:34, :455, :487); `local_path` appears only in the selftest fixture builder (:656), never as a binding.

**Header score citations** (spot-checked, not re-adjudicated): `l1/scores/c1-at-6fdaf4f1.json` carriers_matched 6 / met_target true; `c2-at-6fdaf4f1.json` matched 20 of n 20 / met_target true; `ctl-c1-0-do-nothing.json` carriers_matched 0 / met_target false; `c2-at-freeze.json` contains `no_manifest_at_rev`; `c1-at-base.json` exists (base rev argv); `3c07eed7` = the held-out data commit (20 carriers + envelopes under `corpus/evidence/round-39/c2/heldout/`); wave 1 = 43 seats ✓.

## Not run (out of seat scope)

Re-adjudicating R39-C1/R39-C2 themselves (counters, carriers, held-out scoring) — other wave-2 seats own those; the Assimilation AVM dispute's substance — pointers resolve and the quarantine byte-identity holds, the scout/critic disagreement is recorded faithfully in the lesson's own words.

## Residual risk

The two medium findings are claim-accuracy defects in the lesson's fix layer, not lost defects: R36-CL1/R37-CL1 are genuinely fixed upstream, and the round-39 control receipts genuinely name the freeze. The risk is that the lesson's fix columns cite instruments that cannot currently certify the artifacts they point at (routed-ledger exits 1 on the landed lesson; control-bind cannot parse the round-39 receipts) — a reader trusting the fix columns would over-trust the ledger and the control binding. F3/F4 are evidence-sequencing weaknesses (green runs verifiable only at HEAD / only as fixtures).
