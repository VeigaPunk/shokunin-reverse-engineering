# ALessonDraft — lesson-append draft for the R34-C2 stop, and attack on the landed bytes

Seat: `L1Kaidoku34-2.ALessonDraft` (wave 2, round 34 run-6 re-dispatch). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, read-only for this seat.
Observed window: **2026-10-25T07:29:10Z → 07:35:53Z** (all timestamps UTC; local clock −0300).
Python `/usr/bin/python3` = 3.14.8. **No tool installed or upgraded** (nothing needed; stdlib only). No network. No lane VCS mutation. No ELF carrier, fixture or reader executed as a program of interest; readers ran only as `python3` children of the pinned counters; fixtures were read as static bytes. One report file written: this one. Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w2/ALessonDraft/`.

**VERDICT: `DRAFT_DELTA_READY` — the append this assignment describes landed at `66b84027` while this seat ran, so the deliverable is the part that is still missing (the `## Denied` line) plus four text corrections with exact old/new strings. The stop itself is confirmed: six frozen clauses held, the decisive counterexample reproduces 8/8 at three seeds in my own runs, and the pinned gate refuses the moment that class is registered. One committed defect found that no other seat has reported: `QUALITY.md` row 73 was deleted and replaced by row 74, and the lesson still cites `QUALITY 73`.**

---

## 1. The tree moved under this seat (why the deliverable is a delta)

| UTC | state | evidence |
|---|---|---|
| 07:23:47Z | stop landed `cd75b92e583735729546b0ea3b250f2df6d0652a` (committer `2026-10-25T04:23:47-03:00`) | `git show -s --format=%cI cd75b92e` |
| 07:29:10Z | my frozen-tree extraction from `c79bbe7b`; my clone taken at `cd75b92e` | §2 rows 1–2 |
| 07:32:25Z | `66b840274390d0868c913a544947f9eb40a4ffe6` landed: "SCORECARD section, LOG entry, lesson M34-5..M34-11, QUALITY 68-73, SKILL instrument registry, S106, knowledge entry and README rows" | `git show -s --format='%h %cI' 66b84027` |
| 07:34Z–07:35Z | `5a0435ffb9a8921206144e0b61fe3c12a89b59c2` landed (binds decisive receipts, M34-12, QUALITY corrections); the lesson and QUALITY files were then edited again in the worktree while I read them | §2 row 15 |

Consequence: `## Claim R34-C2`, `## Mistakes` (M34-5…M34-12) and `## Gate` (S106, with access date and quote) are **already in `corpus/lessons/round-34.md`**. A second append carrying those headings again would give the file two `## Mistakes` and two `## Gate` blocks and would reuse ids M34-5..M34-9 with meanings that differ from the landed rows. So this report does **not** draft a duplicate append. It delivers:

1. the missing `## Denied` block (§3, ready to append at the end of the attempt-2 section);
2. exact replacement strings for four defects in the landed bytes (§3, each an edit, not an append);
3. a mapping from the assignment's five named mistake classes to the landed ids, with my verification of each evidence pointer (§4);
4. the attack findings on the stop, its evidence, the disclosed defects and the stop's own repairs (§5).

Live-file caveat: `corpus/lessons/round-34.md` was `bd7b4145…` at 07:35:36Z and `68612674…` at 07:35:53Z; `QUALITY.md` `b605010a…`; `SOURCES.md` `77707752…`. Line numbers below are from the 07:35:36Z read; the quoted strings are the stable anchor.

---

## 2. Exact commands (argv, exit, UTC)

All probes ran on scratch copies: `$S=/fast/scratch/hyaku/kaidoku-r34b/w2/ALessonDraft`; `$S/tools-root` = a copy of the lane's `tools/round-34`; `$S/laneclone` = `git clone --shared` of the lane at `cd75b92e`.

| # | command (cwd) | exit | UTC | observed |
|---|---|---|---|---|
| 1 | `git -C <LANE> archive --format=tar c79bbe7b0959132b9873ff3431cf5eb313b58b33 \| tar -x -C $S/` | 0 | 07:29:10Z | frozen tree 378 MB extracted |
| 2 | `git clone -q --shared <LANE> laneclone` ($S) | 0 | 07:29:33Z | clone HEAD `cd75b92e` |
| 3 | `python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34/r34b --claims .ufo/waves/round-34/r34b/instruments.json --rev c79bbe7b…` ($S/laneclone) | **2** | 07:29:33Z | `freeze-integrity: ERROR no commit adds .ufo/waves/round-34/r34b/instruments.json at c79bbe7b…` |
| 4 | same, **without** `--rev` (HEAD) | **0** | 07:29:37Z | `freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe rev=HEAD`; `grep -c FAIL` = 0 |
| 5 | `python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34/r34b` (default claims path) | **3** | 07:29:37Z | `ERROR schema code=instruments_missing claims=…/r34b/claims.json where=instruments` |
| 6 | `python3 -I -B tools/round-34/mini-fix/mini-counter.py --root $S/tools-root --control-reader <LANE>/.ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py --seed {kaidoku-r34-mini-v1, alt-1, alt-2}` | 0,0,0 | 07:29:32Z, 07:29:33Z, 07:29:33Z | `matched=8, met_target=true, finding=records_match` on all three seeds |
| 7 | `python3 -I -B tools/round-34/replay-gate.py --root $S/tools-root --config tools/round-34/gate-config-mini.json --json-out $S/gate-green-pristine.json` | 0 | 07:29:53Z | `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-` |
| 8 | same with `--config $S/gate-config-nameset.json` (pinned green config + 8th shortcut `{"class":"content-multiset","path":…/nameset.py}`) | **2** | 07:29:54Z | `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=content-multiset` |
| 9 | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev c79bbe7b… --json-out $S/mine-c2.json` ($S/laneclone) | 0 | 07:32:20Z | `GATE_COUNTER_OK … selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`; receipt sha256 `da78f44419ecf839…`; `cmp` vs `after/c2-at-instruments.json` → **exit 0** |
| 10 | `sha256sum .ufo/waves/round-34/r34b/w1/CtlMultiset-files/{nameset.py,pathkey.py,mini-counter-fresh.py}` | 0 | 07:29:24Z | `2e8feaea…8b97` (= stop record's `source_sha256`), `28acfe5a…81a9`, `5181330d…f5c` (= ExecRedReproduce §7) |
| 11 | `python3 -` instruments-vs-claims pin comparison (26 vs 26) | 0 | 07:29:24Z | `n_pins=26 claims_pins=26 same_set=True all_equal=True` |
| 12 | `sha256sum /fast/scratch/…/w1/ScoutReadelfSource/readelf-pinned.c`; `sed -n '13872p;14149p;14020p;14056p;14058p'` on it | 0 | 07:30:16Z | capture `7e81eedf…eff` (matches the scout and the SOURCES row); the five cited lines are byte-for-byte what the lesson describes |
| 13 | `python3 -` whitespace-token count of those five lines | 0 | 07:32:15Z | `13872`→2 tokens; `14149`→5 tokens; `14020`→2; `14056`→7; `14058`→10 |
| 14 | `python3 -` census of `tools/round-34/mini-fix/expected.json` | 0 | 07:32:27Z | 8 fixtures, **25 records, 25 distinct names, 0 names that carry more than one `(flags,value)`**; per-fixture record counts 1,1,2,3,3,4,5,6 |
| 15 | `python3 -I -B $S/probe_invariance.py $S/tools-root` (imports the pinned `mini-counter.permute`) | 0 | 07:32:34Z | all 8 fixtures: `decoded_eq=True`, `soname_multiset_eq=True`, `digest_changed=True` |
| 16 | `git show -s --format='%h %aI %cI' cd75b92e 66b84027 5a0435ff`; `git ls-files`/`git status --porcelain` on `w1/`; `git diff 66b84027..HEAD -- corpus/QUALITY.md` | 0 | 07:32Z–07:35:53Z | commit metadata, tracking census and the QUALITY 73→74 replacement quoted in §5 |

No check was run twice to “confirm” a reported result; each row is one execution except the three seeds in row 6 and the two root spellings in rows 3–4, which are the probe variable.

---

## 3. DRAFT — what the lesson still needs

### 3.1 Append (missing): the `## Denied` block

Paste after the attempt-2 gate block (after the "Prior-art candidates…" bullet) and before `## Limits that remain`, or at the end of the attempt-2 section if the L1 prefers all denials last.

=== BEGIN DRAFT — `## Denied` ===

## Denied

**Denied: the capability row `pre-freeze shortcut-replay gate for finite ELF structural-decoding counters` is not entered.** The R34-C2 capability has no row in `SCORECARD.md` §Capabilities (`:615-630`, including its appended tables), and no new capability table is opened for round 34; `SCORECARD.md:3365` states it outright ("No capability row enters: a capability needs a passing demonstration in the round that enters it, and this round's demonstration failed"), `claims.json` lists `capability` under `not_claimed`, and coverage/depth/calibration stay 10 → 10 (delta 0). The demonstration sentence cannot be written truthfully: the green surface does not force record traversal. `w1/CtlMultiset-files/nameset.py` (sha256 `2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97`) reads no header field, no record entry and no `name_off`; it scores 8/8 at seeds `kaidoku-r34-mini-v1`, `alt-1` and `alt-2` (exit 0), and four further unregistered classes reach the same 8/8. The gate is retained as instrument documentation only; capability entry is deferred to a round whose green surface defeats the class. Denial is a verdict about the demonstration, not about the instrument's usefulness: the six frozen clauses held and the refusal branch works as soon as the class is registered.

=== END DRAFT ===

### 3.2 Edits (not appends) required in the landed bytes

**(a) `corpus/QUALITY.md` — row 73 was deleted and renumbered to 74; restore it.** The file's own rule is "A criterion is replaced by a new row naming the row it supersedes, never rewritten" (`QUALITY.md:5-6`). At `66b84027` row 73 was the receipt criterion; `git diff 66b84027..HEAD -- corpus/QUALITY.md` shows exactly one deletion and one addition:

```
-| 73 | A receipt states what produced it: exact argv, reader digest, the commit the bytes were read at, and a UTC instant — or it declares `caller_asserted` for each field it merely echoes. An unbound receipt is evidence a seat has to reproduce by hand, and three seats auditing an untracked receipt is a lost day. | `corpus/lessons/round-34.md` M34-11; `w1/ExecRecountC2.md` F2/F6, `w1/RevFreezeOrder.md` F2; receipts landed `b917ea64` | sharpens 18, 55 |
+| 74 | A registry or index edit is verified by row count **and** by per-status and per-tier tallies against the base blob, and an insertion anchor is re-read after the edit. A row-count check alone cannot see a swap, and a census that exits 0 does not prove the row you meant to keep is still there. | `corpus/lessons/round-34.md` M34-12; S105 overwritten by the S106 insert, caught by `rejected` falling 4→3 at the same row count (105), restored verbatim from `f432c8e3:corpus/SOURCES.md` | sharpens 33, 68 |
```

Fix: re-insert the removed `| 73 |` line immediately above the current `| 74 |` line, verbatim from `66b84027:corpus/QUALITY.md`. Rows then read 68, 69, 70, 71, 72, 73, 74 and both references resolve. The new corrections block's opening (`QUALITY.md:117`, "Rows 68-74 stand as written") covers a row that is absent today; if the L1 does not restore 73 it must become "Rows 68-72 and 74"; if it does, the phrase becomes true as written.

**(b) `corpus/lessons/round-34.md` M34-11 — no edit needed once (a) is applied.** It reads "QUALITY 73: a receipt carries argv, reader digest and the commit it read, or says `caller_asserted`." and is correct against the restored row. If the L1 instead keeps today's numbering, the cell must be rewritten to point at a real row — not renumbered to 74, whose subject is registry edits.

**(c) `corpus/lessons/round-34.md` Gate bullet, S106 quote — byte fidelity and word count.** Current text: `Line 14149: \`warn (_("Missing Version Needs information\n"))\` (6 words, contiguous code literal).` The captured line 14149 is `\twarn (_("Missing Version Needs information\n"));` — the quote drops the terminating `;`, and its whitespace-token count is **5**, not 6 (command row 13). Replace with:

```
Line 14149: `warn (_("Missing Version Needs information\n"));` (5 whitespace-separated tokens, one contiguous code line; manual code check under QUALITY #1/#17, not machine-gradeable).
```

**(d) `corpus/lessons/round-34.md`, the "two author-side defects" paragraph — mark the provenance.** The paragraph says the permute offset-map defect and the `None`-payload defect "were caught by the instruments themselves before the stop". No failing receipt from before the correction is retained; the only reproductions are post-freeze scratch runs (`w1/ScribeLesson.md` §5: "No retained pre-fix failing run"), and the gate's 12-case `--selftest` cannot catch the permute defect at all because `replay-gate.py`'s selftest substitutes a synthetic counter (`w1/ScribeLesson.md:117`). Suggested replacement tail: "…recorded as found, not as silent repairs; the pre-fix failing runs were not retained, and the reproductions in `w1/ScribeLesson.md` rows 7–10 are post-freeze scratch copies, not author receipts."

### 3.3 Why no second `## Claim R34-C2` / `## Mistakes` / `## Gate` block

- Both headings already appear twice in the file (`## Mistakes` at the attempt-1 and attempt-2 sections; `## Gate` likewise). A third set makes any mechanical reader (first-match) pick the wrong table.
- The assignment's five classes are already covered under different ids (§4). Re-emitting `M34-5..M34-9` with the assignment's ordering would give two different rows the same ids — the exact class of defect the round is about.

---

## 4. Assignment classes → landed rows (coverage and verification)

The assignment names five classes for `M34-5..M34-9`. The landed table carries the same five under the same ids except that three are ordered differently; every one of the five has a landed row.

| assignment class (its position) | landed id | landed evidence pointer | my verification |
|---|---|---|---|
| declarative pins (1st) | **M34-5** | `w1/RevClaimsVsInstruments.md` F1; `freeze-integrity --claims …/claims.json` → exit 3; no `hashlib` in the counters | confirmed: rows 3/5 reproduce exit 2/3; rows 4/11 show the 26-pin container now verifies CLEAN at HEAD; F1's no-op-tamper claim is the review seat's, cited not re-run |
| predicate paraphrase (2nd) | **M34-6** | `predicate-reconciliation.json`; A `7c6c17f0…` (31 words), B `8340aea5…` (46 words), C `09988625…` | confirmed by reading the reconciliation file and both carriers; the two sentences are byte-different |
| class-drop invisibility (3rd) | **M34-8** | `w1/RevPredicateIdentity.md` M3 (7→3, still OK); `w1/RevClaimsVsInstruments.md` F2 | confirmed structurally and by row 7: the pinned 7-class config is CLEAN with `below=7` and nothing asserts equality (`replay-gate.py:31,58`; `MIN_SHORTCUTS=3`) |
| mutant survival (4th) | **M34-9** | `w1/MutGateBranches.md` M3 (`[:-1]` survives 12/12, red → CLEAN); `RevengerGateFailModes.md` D1 + `CritCounterLimits.md` probe C (relabelled 8/8 excluded from `over`) | confirmed by reading both reports and `replay-gate.py:104-127` (`over` filters on the free-text class label); not re-executed |
| green-surface invariant leak (5th) | **M34-7** | `w1/CtlMultiset-files/nameset.py` 8/8 at 3 seeds; four further 8/8 classes (payload-keyed with NULled names, value-keyed, record-order+scalar, `$HOME` hybrid) | **independently reproduced**: row 6 (three seeds, 8/8), row 8 (gate REFUSED once registered), row 15 (layout-only invariance), row 14 (name→record is a function of the fixture content) |

Extra landed rows M34-10 (no-reader counter), M34-11 (unbound receipts), M34-12 (registry row swap) are outside the assignment's five and are not re-drafted here.

---

## 5. Attack findings

### 5.1 On the stop itself (what holds)

- **The six clauses held.** My own counter run (row 9) reproduces the committed receipt byte-for-byte (`da78f444…`, `cmp` exit 0) at worktree `cd75b92e` with `--rev c79bbe7b…`. Because `--rev` is an echo and not a measurement (`c2-shortcut-gate-counter.py:73`), this proves the *bytes at the worktree*; the 26-pin receipt (`pins=26`, 0 FAIL) plus the `c79bbe7b` archive show those bytes are the frozen bytes.
- **The counterexample is real and durable.** `nameset.py`'s tracked copy hashes to the stop's `source_sha256` (row 10); its class is structure-blind by construction (regex over SONAME tokens, table keyed by the sorted set), and it reaches `matched=8, met_target=true` on three seeds in my runs (row 6).
- **The gate is not broken; the registration is incomplete.** Registering the class flips the same pinned gate to `REPLAY_GATE_REFUSED`, `classes_over_target=content-multiset` (row 8). The frozen CLEAN quantifies over the registered set, nothing more.
- **The stop is not compelled by the six clauses or by the kill rule's class-drop sentence** — under the frozen sentence A the claim is met ("registered … readers are scored … none meets the target"), and no class was dropped. The stop rests on the kill rule's first sentence plus the capability criterion, exactly as the record says ("the six frozen clauses hold on the frozen bytes; that is not the whole test"). That is a defensible reading and the record states it in the open; it is noted here because a later reader must not describe it as a clause failure.
- **The class space is open, so no registration count closes it** (see 5.3): the stop's reason is structural, not a missed specimen.

### 5.2 On the disclosed record defects

- **F1 (declarative pins) — corroborated, repair incomplete in two ways.**
  (i) No 26-pin freeze receipt existed when I first searched at 07:29:37Z — `find .ufo/waves/round-34/r34b -name '*freeze*' -o -name '*integrity*'` printed nothing; one exists now at `.ufo/waves/round-34/r34b/after/freeze-integrity-instruments.txt` (26 `ok` rows, 0 `FAIL`, `rev=66b84027`), landed after my check. The landed M34-5 sentence "+ a freeze-integrity receipt over it" is true **as of `66b84027`**, not as of the stop.
  (ii) The repair binds the stop tip, not the measured revision: the same command with `--rev c79bbe7b…` exits **2** (`no commit adds instruments.json at c79bbe7b`) because the container postdates the freeze. So the pin guarantee covers `[b917ea64 … HEAD]`; it does not reach backwards to the claim's measured revision. That limit is not stated in M34-5.
- **F2 (predicate paraphrase) — corroborated.** Two sentences, three carriers, no instrument reads the value (`replay-gate.py:43` only requires the key; the counter echoes its own constant at `:73`). Disclosed, not repaired: correct.
- **F3 (class-drop invisibility) — corroborated** and independently reproducible (row 7 shows the 7-class CLEAN; `MIN_SHORTCUTS=3` at `replay-gate.py:31,58`).
- **F4 (mutant survival) — corroborated** by `w1/MutGateBranches.md` §3 (M3 `[:-1]`: selftest 12/12, red case CLEAN). Tracked at `66b84027`; it was untracked at the stop commit.
- **F5 (receipts untracked) — claim true, pointer wrong.** The stop's evidence names `w1/RevFreezeOrder.md` and calls it "(pending)". That file's current bytes have mtime **07:27:46Z**, 3m59s *after* the stop commit `07:23:47Z`, and it was untracked until `66b84027`; the defect it describes is independently evidenced by the tracked `w1/ExecRecountC2.md` F6. A stop record should not cite a report it predates.
- **Stop record's `frozen_counter_verdict.command` is not an exact argv**: it carries `<LANE>` and `<RECEIPT>` placeholders (`claim-stop.json`), which QUALITY 18 does not admit as a producing command. The decisive run's argv is exact; the six-clause run's is not.
- **`l1_rerun_utc` is impossible as written**: `"2026-10-25T07:28:00Z (approximate…)"` postdates the stop commit `07:23:47Z` and `claim-stop.json`'s own mtime `07:23:32Z`. Already found by `w2/AStopCompleteness.md:45,51,168,243`; recorded here because the landed lesson propagated the same instant ("L1 rerun 2026-10-25T07:28Z"). No receipt carries that instant.

### 5.3 On the stop's proposed repair (the load-bearing attack)

The stop's repair fields (F3 "assert class count == pinned count before CLEAN"; F4 "red-last selftest case + row-count assertion") are **orthogonal to the class that stopped the claim**:

- At the freeze the pinned set and the registered set were the same seven classes, so a count/equality assertion passes while five unregistered classes reach 8/8. `QUALITY 70` (class-set equality) is a defence against *dropping*, not against *not knowing a class*.
- The class-drop and mutant-survival repairs would not have changed the outcome; the only repair that touches the cause is at the **transformation**: generate the green surface per run from unpublished content (demonstrated: `w1/CtlMultiset-files/mini-counter-fresh.py`, sha256 `5181330d…`, structural 8/8 and all nine shortcut classes 0/8, gate CLEAN with nine registered), or break every keyable invariant. The landed lesson added this route (`M34-7`, `QUALITY 69`); the stop record alone did not carry it.
- **Additional measured limit of the current fixture family** (mine, row 14): 25 records, 25 distinct names, and **no name ever carries a second `(flags,value)`**. The name→record association is therefore a global function recoverable from the content alone, which is why both the SONAME-set reader and the pool-only reader reach 8/8. A minimal next-instrument fixture rule would be: at least one duplicated name with two different `(flags,value)` pairs, and at least one `(flags,value)` pair under two different names, in two different fixtures. This is cheaper than per-run generation and it is not in `QUALITY 69` as landed.
- **General form** (row 15, my probe): for any transform `T` with `decode(T(x)) = decode(x)`, a shortcut `S(x)=F(g(x))` with `g(T(x))=g(x)` passes wherever it passes on the original. A layout-only transform can never exclude a key built from a public layout invariant. This is the sentence the next criterion should carry, and `QUALITY 69` is close to it but lists invariants instead of stating the implication.

### 5.4 On the landed docs (defects found this wave)

- **QUALITY 73 deleted, not superseded** (§3.2a): committed at `5a0435ff`; the receipt criterion is gone, M34-11 cites it, and the new corrections block says "Rows 68-74". This is the only finding in this report that no peer draft contains (`grep -l "QUALITY 73"` over `w2/*.md` → none). Severity: the routing for M34-11 is broken for any later reader; the fix is one restored line.
- **S106 row still absent from committed `SOURCES.md`**: at `HEAD=5a0435ff`, `git show HEAD:corpus/SOURCES.md` has six S100–S109 rows with S106 present and **S105 missing**; the S105 restore exists only as an uncommitted one-line worktree change (`git status` → ` M corpus/SOURCES.md`). The restore is byte-identical to `f432c8e3` (checked). M34-12's own sentence therefore describes an uncommitted repair; it should say so, or the change should be committed before the round is called landed.
- **Gate quote fidelity** (§3.2c): missing `;`, word count 6 vs 5.
- **Duplicate headings** (`## Mistakes` ×2, `## Gate` ×2; at least one `# Round 34…` H1 inside the file): mechanical selectors will take the first block. Not fixed here; the L1 may title them "… — attempt 1 / attempt 2".
- **Author-defect paragraph has no retained failing receipt** (§3.2d).

No defect found in: the six clauses' arithmetic, the target `8`, the class list, the receipts' exit codes, `S106`'s capture hash/line numbers, or `M34-12`'s S105 verbatim restore.

---

## 6. Out of scope, unrun, limits

- **Not run**: builds, linters, bulk suites; `scripts/sources-census.sh`; any network re-fetch of S106 (the capture and its sha were verified locally instead); the four non-do-nothing control gates; the remaining w1 seat probes cited from reports. The R34-C1 production reader and its twelve carriers were not executed, read as programs or scored.
- **Not verified by me**: jj operation log, reflog and filesystem birth times (the freeze-order seat's domain); `ExecRedReproduce`'s fresh-counter sweep beyond reading its receipt (I did not execute `mini-counter-fresh.py`); the counterclaim-free status of the w1 reports' cited scratch artifacts.
- **Live tree**: three commits and at least two worktree edits landed while this seat ran. Quantities in §1/§2 are pinned to the shas and instants named there; the L1 should re-read the target lines before applying §3.2.
- **No writes** outside this report and `$S`. No tool installs, so the tooling ledger is empty by absence, not by omission.

---

## 7. Verdict

`DRAFT_DELTA_READY`. The append landed at `66b84027` (`5a0435ff` after it); its Claim R34-C2, Mistakes M34-5..M34-12 and S106 Gate blocks are backed by the evidence I independently reproduced (three-seed 8/8 counterexample, byte-identical counter receipt, REFUSED-on-registration, layout-only invariance). The lesson still lacks the `## Denied` line required by this assignment, so that block is drafted in §3.1; four corrections are specified as exact strings in §3.2, of which the restoration of `QUALITY.md` row 73 (deleted and replaced by row 74 at `5a0435ff`) is the one that breaks a live reference in the lesson. Nothing in this report reopens R34-C1, amends the frozen claim, or awards a score or capability.
