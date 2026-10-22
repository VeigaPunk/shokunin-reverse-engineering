# CriticMistakes — attack on M29-1..3 (`corpus/lessons/round-29.md` `## Mistakes`)

Seat `KaidokuR29.CriticMistakes`, critic, wave 1. Run 2026-10-22T20:20Z–20:25Z. Read-only on the lane
(tip `18be864a528873b2b70d8c94e31f880290249e90`); every git checkout and gate run below used a sandbox
clone `/fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticMistakes/clone` with GIT_DIR, GIT_WORK_TREE and
GIT_INDEX_FILE unset. No REA, no network lookups, no sources opened over the network. No tools
installed or updated.

## Verdicts

| id | class right? | captured-by honest? | fix fails on real bytes as claimed? | verdict |
|---|---|---|---|---|
| M29-1 | partly. The class is about seat liveness; the fix tests tree cleanliness | yes | **no**: the red receipt uses bytes written after the filing commit; at the real filing state the check exits 0 | **fails** |
| M29-2 | **no**. The gate *was* run with `--disclosures` in round 27, came back red, was reported to the L1 twice, and was dropped. Three filings were affected (r26, r27, r28), not two | **no**: "not run at the round-26 and round-28 filings" leaves out round 27, where it was run and ignored | yes: the detector exits 1 on the pre-fix ledger (reproduced) | **fails** (class and captured-by) |
| M29-3 | yes, but it repeats a shape that the round-28 ledger row already recorded | mostly. The round-24 gate existed before the freeze and could have run on a scratch commit | detector yes; the proposed procedure is not mechanised | **holds**, with a recurrence note |

Missing mistake: **routed red findings are dropped at integration and replaced by unenforced rules** (M29-X below). It covers M29-2's real cause and the gap in M29-1's fix.

---

## M29-1 — "a round was filed while one of its seats was still writing into the lane tree"

**Attacked:** the claim that `tools/round-29/prefile-check.sh` was "shown able to fail on the real r28 state", and QUALITY row 47.

**Counterexample (observation).** The seat's report was first committed *in* the round-28 filing commit. The seat kept writing afterwards. A `git status --porcelain` check run at filing therefore sees a clean tree.

- `git log --format='%h %cI %s' -- .ufo/waves/round-28/a2w/ExecR27SelftestFix.md` (lane, read-only, 2026-10-22T20:22Z, exit 0):
  `7431096b 2026-10-22T17:06:08-03:00 …` and `242b0d8b 2026-10-22T16:25:35-03:00 round-28: final seat reports, SCORECARD defect-2 status (open)`. So the file was first committed at 19:25:35Z, in the L1's filing commit.
- `git diff 242b0d8b 7431096b -- .ufo/waves/round-28/a2w/ExecR27SelftestFix.md` (20:23Z, exit 0): the later bytes carry run times after 19:25:35Z. They include `Run 2026-10-22T18:24Z–19:26Z` and `… at all three revisions tried (2026-10-22T19:26:31Z)`. The 19:26:31Z run is later than the filing commit, so the rewrite landed after filing. That ordering is an observation. The exact write instant is unknown.
- Round-28 spot-check `corpus/lessons/round-28-verifier-spotcheck.md:5` and `:28`: the session ran 19:27Z–19:40Z and found the leftover there, *after* the seat finished.
- Reproduced at the filing state. `git checkout -q 242b0d8b8ad6ff6c693fa5114216fbb538b587bf; sh tools/round-29/prefile-check.sh <clone>` at 2026-10-22T20:24:05Z printed `prefile: clean`, `exit=0` (scratch `prefile-and-gates.txt`). The L1's own receipt `.ufo/waves/round-29/after/prefile-check-red-r28.txt` shows the same first line, `prefile: clean` / `exit=0`. Its red line comes only after "seat ExecR27SelftestFix's post-stop bytes copied in, as the lane stood at round-29 start". That is the state at the start of round 29, not the state at filing.

**Inference.** If the L1 had run the check at 19:25:35Z, it would have passed and round 28 would have filed exactly as it did. The fix does not catch the case it was mined from. The failure mode is "the L1 commits what a live seat has written so far, then the seat rewrites it". A tree-cleanliness check run straight after that commit cannot see the rewrite. Round 29 is exposed the same way: wave-1 reports are being written into `.ufo/waves/round-29/w1/` right now (lane `git status --porcelain` at 20:20:54Z lists `?? .ufo/waves/round-29/w1/` and others).

**QUALITY row 47** says a round files "only after its last seat has settled *and* the lane tree is clean". Its fail clause covers only the second half: "Fails when the lane's `git status --porcelain` is non-empty at filing". Under that clause round 28 passes, because its tree was clean at filing (observation above). The row's own "Round-28 case" uses bytes that arrived after filing.

**Class / captured-by.** The class text is right. Captured-by ("the round contract … a rule, but nothing checked it") is honest. The fix tests a different property from the class.

**Impacted axes:** discernment (a fix recorded as shown able to fail on a case it does not catch) and quality of the QUALITY row.

**Smallest safe correction.**
1. Re-label the receipt as "red on the round-29-start state; green at the round-28 filing state `242b0d8b`".
2. Make the check test seat settlement, not only tree cleanliness. For example, `prefile-check.sh` takes the wave's task-result or registry and exits 1 unless every dispatched seat is completed or cancelled. Then it checks `git status --porcelain`. Or the check runs again after a quiescence interval and requires byte-identical status and HEAD.
3. Change QUALITY row 47's fail clause to match: it fails when any dispatched seat is not settled at filing.

`w1-task-result.json` holds per-seat `"status"` values (44 × `"status": "pending"` and one `"state": "running"` at 20:24Z), so a machine-readable liveness source exists. Which field is authoritative is unknown to this seat.

---

## M29-2 — "the claim-freeze ledger disagreed with the gate … and nobody ran the gate with `--disclosures` at filing"

**Attacked:** the class ("nobody ran"), captured-by ("it exists but was not run at the round-26 and round-28 filings"), and the "two rounds" scope.

**Counterexample (observation).** The gate was run with `--disclosures` in round 27 by two seats. Both got exit 1 on `round-26` and handed it to the L1. Round 27 filed without fixing the row or disclosing the mismatch.

- `.ufo/waves/round-27/w1/CriticFreeze.md:28-31`: `python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root <lane> --rev a4f674b3 --disclosures corpus/claim-freezes.tsv`, exit 1, 14:58:55Z. Quote: `Disclosures: "missing":["round-27"], "mismatched":["round-26"].` and `The round-26 mismatch is pre-existing and outside this seat; it is reported for the L1.`
- `.ufo/waves/round-27/w2/ReviewFreezeRow.md:15`: `the whole-file gate exits 1 at main. The only mismatched row is round-26`. Also `:27`: `"exact":13,"of":14,"mismatched":["round-26"]` with exit 1 at 15:43:30.
- `rg -n 'round-26' corpus/lessons/round-27.md | rg -i 'ledger|freeze|row'` (20:23Z) found no line about the ledger mismatch. The round-27 lesson and its SCORECARD section do not record it. The round-27 closure (`corpus/lessons/round-27-verifier-spotcheck.md:44-52`) checked only the round-27 row.
- Round 28 was told to run the gate. `.ufo/waves/round-28/a2w/CriticC1Miss.md:60` says: `Checks for the L1 to run: … freeze-gate.py --disclosures corpus/claim-freezes.tsv for round-28`. `.ufo/waves/round-28/after/` holds no freeze-gate receipt (directory listing, 20:23Z). The round-28 row was then written with unsorted codes.

**The ledger was wrong at each filing (observation, reproduced in the clone, scratch `gate-at-filings.txt`, 2026-10-22T20:22:05Z).** Command: `python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root . --rev <REV> --disclosures corpus/claim-freezes.tsv`.

| rev (role) | disclosures excerpt | exit |
|---|---|---|
| `fe3eb4ed` (round-26 row written) | `"mismatched": ["round-26"]` | 1 |
| `4084d897` (round-27 row written) | `"mismatched": ["round-26"]` | 1 |
| `e01deb19` (round-28 row written) | `"mismatched": ["round-26", "round-28"]` | 1 |
| `7431096b` (lesson's receipt) | `"mismatched": ["round-26", "round-28"], "missing": ["round-29"]` | 1 (equal to `.ufo/waves/round-29/after/ledger-before-fix.txt`) |

Round 26's instruments landed at `81f63f36` (09:31-03) and `bd0c84bc` (09:49-03), before its row at `fe3eb4ed` (09:52-03). So the row was wrong when it was written; it did not drift later.

**Inference.** The mistake is not "the check exists but nobody ran it". The check ran, came back red, was routed to the L1 twice, and was dropped. Round 28 was asked to run it and did not. Three filings (r26, r27, r28) carried a red ledger, not two. The lesson's fix promises that "the round-29 report runs both gates with `--disclosures` before filing" (QUALITY row 46). That is the same kind of unenforced rule that M29-1's captured-by criticises, and round 27 shows a rule plus a red result is not enough.

**Fix able to fail (observation).** Holds. The detector exits 1 on the pre-fix ledger (table above). After the fix, both gates exit 0 at `18be864a`: scratch `prefile-and-gates.txt`, 20:24:06Z `{"exact": 16, "mismatched": [], …}` exit 0, and 20:24:07Z `{"exact": 19, "mismatched": [], …}` exit 0. These match `.ufo/waves/round-29/after/freeze-gates-v2.txt`.

**Impacted axes:** calibration and discernment (a lesson that under-reports its own history), and false provenance in captured-by.

**Smallest safe correction.**
1. Restate the class: "a red `--disclosures` result reported by seats (r27 `CriticFreeze`, `ReviewFreezeRow`) and a seat-requested run (r28 `CriticC1Miss`) were not acted on at integration; the ledger was red at the r26, r27 and r28 filings".
2. Restate captured-by: "the gate (QUALITY 33) caught it in round 27; the L1 did not integrate it".
3. Make the fix mechanical: have `prefile-check.sh` run both gates with `--disclosures` at HEAD and exit 1 on any non-zero gate exit.

---

## M29-3 — "the L1's own freeze file names a script it does not pin"

**Attacked:** whether `tools/round-28/c1-heldout-naming.py` is truly only a reference, and whether the captured-by and fix are honest.

- **Reference only: holds (observation).** `rg` over `tools/round-29/c1-fresh-naming.py` (20:21Z): the counter execs only `RESOLVER = "tools/round-25/a2/resolve-selectors.py"` (`:55`, `:130`, `:449`). `round-28/c1-heldout-naming.py` appears only in prose (`:4` "Copied from tools/round-28/c1-heldout-naming.py …").
- **Gate disagreement explained (observation).** At `dbd87cfa`, the round-24 gate flags 4 unpinned round-29 paths: `c1-heldout-naming.py`, `collect-c1.py`, `collect-c2.py` and `make-carriers.py`. The round-29 gate flags only the first. This is because the round-29 gate also reads `loaded_by_counter` and `producers_not_counters` (`diff` of the two gates; `PIN_KEYS` at `tools/round-29/freeze-gate.py`). `.ufo/waves/round-29/after/freeze-gates-at-dbd87cfa.txt` shows both. The lesson cites only the round-29 gate's single flag. The ledger row `round-29` in `corpus/claim-freezes.tsv` does disclose all four, so this is not hidden.
- **Recurrence (observation).** The round-28 ledger row (`corpus/claim-freezes.tsv`, `round-28`) already records the same shape: "flags select-heldout.py as unresolved (bare file name in claim text)". Round 29 repeated it with a path in `primary_rule` prose. The lesson does not call it a recurrence.
- **Captured-by "only after the freeze commit" (inference).** This is accurate for the round-29 gate, which was committed at `7431096b` after `dbd87cfa`. But the round-24 gate existed at the base and flags the same path. Running it on a scratch-clone commit before the freeze, which is the lesson's own proposed fix, was already possible this round.
- **Fix able to fail: partly (inference).** The gate's flag shows the *detector* fails. The proposed *procedure* (run the gate on a candidate claims commit before the real freeze) has no script, no QUALITY row and no receipt, so nothing can fail it.

**Small related defect (observation).** The frozen counter's docstring names round-28 evidence: `tools/round-29/c1-fresh-naming.py:14` says `carriers in corpus/evidence/round-28/c1/carriers.tsv` and `:27` says `corpus/evidence/round-28/c1/tally.json`. The code uses `EVDIR = "corpus/evidence/round-29/c1"` (`:56`). This is documentation only and changes no count. It cannot be fixed without an `INSTRUMENT_REVISED` disclosure, so it should be noted in the entry's Limits or the lesson, not edited.

**Verdict:** holds, with two corrections: add "recurrence of the r28 prose-named-script shape", and either mechanise the pre-freeze gate run or label it an unverified procedure.

---

## Missing mistake (M29-X): routed red findings are dropped at integration and replaced with unenforced rules

**Evidence (observation, all cited above).**
- r27: two seats report `--disclosures` exit 1 on `round-26` "for the L1". The round-27 lesson and SCORECARD do not carry it.
- r28: `CriticC1Miss` lists `--disclosures` as a check for the L1 to run. No receipt exists. The row is written mis-sorted.
- r28: routed defect 1 says "do not file while any seat is live". Round 29's answer (QUALITY 47 and `prefile-check.sh`) checks only tree cleanliness. Its own `242b0d8b` line shows `clean, exit=0` at the real filing state.
- r29: M29-2's and M29-3's fixes are again stated as procedures ("the round-29 report runs both gates", "a future freeze runs the gate on a scratch-clone commit") with no exit-code gate.

**Inference.** M29-1 and M29-2 share one root cause the lesson does not mine. Seat outputs and lane checks that come back red reach the L1, but nothing makes a red result block filing. Each round adds another rule. In two of the three mined mistakes, the receipt shown as "able to fail" is the detector, not the step that would have stopped the filing.

**Smallest safe correction.** One pre-file gate that exits 1 when any of these hold:
1. A dispatched seat is unsettled.
2. `git status --porcelain` is non-empty.
3. Either freeze gate with `--disclosures` exits non-zero.

Prove it red on the true r28 filing state. That means seat-unsettled input: the r28 seat was live at 19:25:35Z (19:26:31Z run in its later bytes) and a run with `--disclosures` at `e01deb19` exits 1 (observed above; `242b0d8b` not run by this seat). A post-hoc tree copy does not count as that proof.

## Scratch artifacts

| path | sha256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticMistakes/gate-at-filings.txt` | `f7b151bd8bfb15a79d90c0a7516f2e9f8cb6d323f3fbca94ecb2fb0a323a065e` |
| `/fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticMistakes/prefile-and-gates.txt` | `efc512c76d055da75369b6b82608016140a53dd9db62b75d783a057df7f05a1d` |
| `/fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticMistakes/clone/` (sandbox clone of the lane, left checked out at `18be864a`) | directory, not hashed |

Checks for the L1: run `sh tools/round-29/prefile-check.sh` on a clone at `242b0d8b` (expect exit 0, which refutes the receipt's framing). Run the round-24 gate with `--disclosures` at `4084d897` (expect `mismatched: [round-26]`, exit 1).
