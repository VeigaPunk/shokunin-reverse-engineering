# AStopFields — field-by-field audit of the R34-C2 stop record

Seat: `L1Kaidoku34-2.AStopFields` (leaf, Godspeed). Round 34 run-6 re-dispatch, wave 2.
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` — read-only for this seat (no VCS mutation, no
frozen-instrument edit, no lane write except this report).
Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w2/AStopFields/probe/` (a `cp -a` of `tools/round-34`, 26/26
pins byte-identical; every probe run there; lane never executed in place).
Audit window: `2026-10-25T07:28:23Z` … `2026-10-25T07:38:48Z`.
Tooling installed/updated: **none**. Runtime `/usr/bin/python3` = Python 3.14.8 (preexisting); `git`
read-only (`rev-parse`, `show`, `log`, `merge-base --is-ancestor`, `status`, `diff`, `cat-file`). No
network used. No ELF carrier/fixture/reader executed as a program; readers ran only as `python3` via the
pinned counters; the R34-C1 production reader and its twelve carriers were not touched.

## 0. Target and temporal discipline

Target: `.ufo/waves/round-34/r34b/claim-stop.json` as landed at `cd75b92e`
(committer `2026-10-25T04:23:47-03:00` = `07:23:47Z`). File sha256
`e6303d061da219bb100f3a9acfc7492c9880acc177c4b98f5b695392b5cbcbfc` — unchanged at every tip I sampled.

The lane moved under this audit (normal wave-2 churn, not mine):

| UTC | tip | note |
|---|---|---|
| 07:28:23Z | `cd75b92e` | HEAD/main/origin-main at audit start |
| 07:33:27Z | `66b84027` | record landing (SCORECARD/LOG/lessons/QUALITY/S106) |
| 07:37:55Z | `5a0435ff` | `claim-stop-addendum.json`, `after/freeze-integrity-instruments.txt`, `nameset-green-receipt.json`, `payload_keyed.py` + receipt, six w2 reports |
| 07:38:01Z | `417a8211` | further w2 reports |
| 07:38:48Z | `b62b4767` | further churn |

The frozen revision `c79bbe7b…` is an ancestor of each of these tips (`git merge-base --is-ancestor` exit
0 at `cd75b92e` 07:28:23Z, at `66b84027` 07:33:27Z, at `5a0435ff` 07:38:01Z, at `b62b4767` 07:38:48Z).

Consequence for this audit: later artifacts are treated as **evidence about** the record, never as the
record. Where a defect was repaired only by the append-only `claim-stop-addendum.json` (landed
`5a0435ff`, 07:35:10Z committer), both states are reported: what the stop record asserted at its landing,
and what the addendum later bound.

## 1. Field-by-field audit

Legend: **OK** = assertion equals committed evidence; **WEAK** = supported in substance, wording bears a
formal defect; **MISMATCH** = assertion is not backed by committed evidence as written.

| # | field | assertion | evidence checked | verdict |
|---|---|---|---|---|
| 1 | `attempt` | "run-6 re-dispatch, attempt 1" | `claims.json:attempt` identical; LOG round-34 run-6 section | OK |
| 2 | `axis` | `depth` | `claims.json:claims[0].axis` = `depth` | OK |
| 3 | `claim` | `R34-C2` | `claims.json:claims[0].id` | OK |
| 4 | `decisive_counterexample.argv` | `python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . --control-reader …/nameset.py` | `mini-counter.py:main` has exactly `--root`, `--control-reader`, `--seed`, `--selftest`; argv runs from a 26/26-pin copy, exit 0 (CHECK-11) | OK |
| 5 | `decisive_counterexample.class` | "content-multiset memorization (SONAME-set key + stored name->flags/value table)" | `nameset.py:19` TOKEN regex, `:21-44` TABLE keyed by `\|`-joined sorted names, `:48-53` read_bytes/findall/table | OK |
| 6 | `decisive_counterexample.producer_seat` | `ExecRedReproduce.md`, "independent of the L1-authored readers" | `w1-seat-map.json` entry `["ExecRedReproduce","executor",…prompts/ExecRedReproduce.md,4961]` (a distinct executor seat); its Appendix A code block is **byte-identical** to the landed `nameset.py` (2781 bytes, sha `2e8feaea…`) | OK |
| 7 | `decisive_counterexample.source` | `.ufo/…/w1/CtlMultiset-files/nameset.py` | file present; commit `cd75b92e` added it | OK |
| 8 | `decisive_counterexample.source_sha256` | `2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97` | `sha256sum` = same (07:37:42Z, exit 0); equals the wave-1 artifact pin quoted in `ExecRedReproduce.md` §5/Appendix A and the addendum's `artifact_shas` | OK |
| 9 | `decisive_counterexample.l1_rerun_utc` | `2026-10-25T07:28:00Z (approximate; exact clock in the wave report)` | see **F1** | **MISMATCH** |
| 10 | `decisive_counterexample.observed.exit/matched/target/met_target` | `0 / 8 / 8 / true` | reproduced: exit 0, `matched=8`, `target=8`, `met_target=true` (07:37:42Z and 07:37:47Z); `mini-counter.py:TARGET=8`, `return 0 if met_target` | OK |
| 11 | `decisive_counterexample.observed.seeds` | `kaidoku-r34-mini-v1:8, alt-1:8, alt-2:8` | reproduced all three (07:37:47Z) plus `alt-3:8`; `kaidoku-r34-mini-v1` is the counter's `--seed` default; see **F4** for artifact provenance at record time | OK numerically, WEAK provenance |
| 12 | `decisive_counterexample.why_this_falsifies_the_surface` | reads no header / no record array / no `name_off`; keyed on sorted SONAME set; counter's only transformation is name-pool permutation | `nameset.py:48-53` reads raw bytes and replays TABLE (no header field, no `name_off` dereference); `mini-counter.py:permute` reorders pool strings and rewrites only `name_off`, decoded output unchanged | OK (wording narrowed by addendum D1: it *scans* pool bytes as text) |
| 13 | `frozen_claim_revision` | `c79bbe7b0959132b9873ff3431cf5eb313b58b33` | `git cat-file -t` = commit; ancestor of every tip (see §0); `git log --diff-filter=A -- claims.json` = added exactly at `c79bbe7b`; committer `07:13:11Z` | OK |
| 14 | `frozen_counter_verdict.command` | `… c2-shortcut-gate-counter.py --root <LANE> --rev c79bbe7b… --json-out <RECEIPT>` | both flags exist (`c2-shortcut-gate-counter.py:66-68`); argv reproduced in scratch (07:37:42Z) | OK |
| 15 | `frozen_counter_verdict.exit` | `0` | receipt `exit: 0`; my run exit 0 | OK |
| 16 | `frozen_counter_verdict.line` | `GATE_COUNTER_OK … clauses_failed=-` | byte-equal to `after/c2-at-instruments.txt` (07:37:42Z); my run printed the identical line (07:37:42Z); format matches `c2…:127-132` | OK |
| 17 | `frozen_counter_verdict.note` | "the six frozen clauses hold on the frozen bytes; that is not the whole test" | receipt `clauses` all true; my run `{gate_present, green_clean, green_positive_meets_target, mutants_killed, red_refused, selftest_clean}` all true | OK |
| 18 | `frozen_counter_verdict.receipt` | `after/c2-at-instruments.json` | present; `measured_revision=c79bbe7b…`; `green.positive_matched=8`, `green.shortcuts_below_target=7`, `mutants_killed=3`, `selftest_failures=0`; matches `claims.json:after_receipt`; see **F3** for the `measured_revision` echo | OK in substance, WEAK binding |
| 19 | `kill_rule_applied` | frozen-before-data rule; seven registered classes below target; unregistered structure-blind class reaches it; "no capability row enters SCORECARD; owned scores stay 10->10" | green receipt `shortcuts_below_target=7`; gate config registers exactly 7 classes and not `content-multiset`; `claims.json:scores_unchanged` 10→10; stop commit `cd75b92e` touched no SCORECARD file (`git show --stat`); see **F5** for the literal SCORECARD clause | OK in substance, WEAK literal |
| 20 | `not_claimed` | capability / coverage / depth score / calibration score / R34-C1 revival | `git show --stat cd75b92e` = `claim-stop.json` + 3 `CtlMultiset-files/*.py` only; no SCORECARD/LOG/corpus/claims edit | OK |
| 21 | `predicate_frozen` | sentence A | byte-equal to `claims.json:claims[0].predicate`; both sha256 `7c6c17f0cca6c680507d4eec33b4c0c82a76c4f73e9a98ceb4bde54a9a96279b` (07:37:42Z) | OK |
| 22 | `predicate_note` | A = 7c6c17f0…; counter+receipts carry longer paraphrase B = 8340aea5…; disclosed, not repaired | recomputed: counter `PREDICATE` concatenation = `8340aea5…`; `after/c2-at-instruments.json:predicate` equals it; all five `controls/*.json:predicate` = `8340aea5…`; `predicate-reconciliation.json` word counts 31/46 match | OK |
| 23 | `record_defects_disclosed[F1]` | pins under `claims[0].pins`; `freeze-integrity.py` exits 3 `instruments_missing`; no instrument hashes a pinned file; repair = `instruments.json` 26-pin container + freeze-integrity receipt over it | pins: `instruments.json` has 26 entries, key set and values **byte-identical** to `claims[0].pins` (07:37:42Z); `frozen_claims_sha256` = `de3afbfb…` = sha256(claims.json); `freeze-integrity.py --round 34/r34b --rev c79bbe7b` on the default claims path = `ERROR schema code=instruments_missing … exit 3` (07:36:21Z); `grep -c hashlib` = 0 in both `replay-gate.py` and `c2-…counter.py`; but see **F2** for the missing receipt | WEAK/MISMATCH |
| 24 | `record_defects_disclosed[F2]` | predicate identity false; "no instrument reads the predicate value" | A/B verified; `replay-gate.py:43` requires the `predicate` **key** present but never compares its value — no instrument compares/verifies it. Wording imprecise (**F6**) | OK in substance |
| 25 | `record_defects_disclosed[F3]` | class drop to `MIN_SHORTCUTS` floor still CLEAN; nothing asserts registered set == pinned set | `replay-gate.py:31 MIN_SHORTCUTS=3`, `:58` only floor check, no pin comparison anywhere (no hashlib, no git); `RevPredicateIdentity.md:75` M3 row: trim 7→3 → `shortcuts_below_target=3`, CLEAN, exit 0, 07:19:17Z; `RevClaimsVsInstruments.md:132` F2 heading | OK |
| 26 | `record_defects_disclosed[F4]` | gate mutant M3 (ignore last shortcut row) survives its selftest and turns the red case CLEAN | `MutGateBranches.md:73` row: M3 `selftest` failures **0** (12/12 cases, 3/3 mutants), naive config **0 CLEAN**, "SURVIVED", "red inverted to CLEAN"; `:121-165` detail; recommended repair "red-last + row-count" matches the record's route | OK |
| 27 | `record_defects_disclosed[F5]` | receipts were untracked at first audit; repair landed `b917ea64…`; evidence `RevFreezeOrder.md (pending)` / `ExecRecountC2.md F6` | `b917ea64` exists, is the direct parent of `cd75b92e`, and its stat adds `after/`, `before/`, `controls/`, `assimilation/`; `ExecRecountC2.md:132` F6 says exactly this; `RevFreezeOrder.md` now exists (landed `66b84027`) and was honestly marked pending | OK |
| 28 | `round`, `type` | `34`, "capability acquisition" | `claims.json:round`, `claims[0].type` | OK |
| 29 | `verdict` | "falsified measure; honest stop after wave-1, before any capability or score credit" | counterexample reproduced; no capability/score artifacts; `claims.json:scores_unchanged` 10→10; SCORECARD run-6 rows keep depth 10→10 | OK |

## 2. Findings by severity

### F1 — HIGH — `decisive_counterexample.l1_rerun_utc` names a run that did not yet exist when the record was written, and no artifact anywhere binds that clock

- Record birth and last write: `stat -c '%w %y'` → `2026-10-25 04:23:32.032146615 -0300` / `04:23:32.033256201 -0300` = **07:23:32Z**; ctime identical.
- Record commit `cd75b92e` committer time `04:23:47 -0300` = **07:23:47Z**.
- The field's value **07:28:00Z** is therefore 4 m 28 s in the **future** at the record's write and 4 m 13 s in the future at its commit. The w2 prompt tree itself was created at `04:24:35 -0300` = 07:24:35Z, also before 07:28.
- The record was never rewritten: sha256 `e6303d06…` at `cd75b92e`, `66b84027`, `5a0435ff`, `b62b4767`; `git status --porcelain` empty; `git log -- …/claim-stop.json` shows only `cd75b92e`.
- The cited "exact clock in the wave report" had no referent: no w2 report existed at commit time and none is cited by path. `LOG.md` (landed `66b84027`, 07:32:25Z) repeats "L1 rerun 07:28Z" with no receipt path.
- The only artifact for this class with argv+UTC+seeds is `w1/CtlMultiset-files/nameset-green-receipt.json` (sha `fa6e8f09…`, landed `5a0435ff`), whose four runs are all stamped **`utc_start`/`utc_end` = `2026-10-25T07:34:01Z`** — not 07:28. So the post-stop binding confirms the numbers and **contradicts the field's clock**.
- Searches for an earlier rerun receipt: none. `find .ufo/waves/round-34/r34b -name '*receipt*'` → 0 at stop time; `ExecRedReproduce` scratch holds only `b2.txt`/`d2.txt`/`gate-*.json` (04:18–04:19 local = 07:18–07:19Z, seedless); no L1 scratch dir under `/fast/scratch/hyaku/kaidoku-r34b/w2/`; no `/tmp` file containing `nameset` from 04:26–04:31 local.
- Why it matters: the `observed` block sits inside `decisive_counterexample`, immediately beside `l1_rerun_utc`, so the record attributes the observed numbers to a run that had not happened at write time; unlike `frozen_counter_verdict`, the block carries no `receipt` path. The numbers are independently true (§3), so the stop's substance is unaffected — the field is the defect.
- Repair that closes it: bind the counterexample to `nameset-green-receipt.json` (its UTC is 07:34:01Z, not 07:28) and drop the forward-dated clock. The addendum's `why` names "an approximate UTC" among the gaps it answers, but it binds no clock and leaves 07:28Z standing in the record while the bound receipt says 07:34:01Z.

### F2 — HIGH (record-time) / now bound differently — F1's `repair_landed` claims a "freeze-integrity receipt over it" that was absent at landing and, when produced, binds the repair commit, not the freeze

- Container half is true: `instruments.json` carries 26 pins whose key set and digests are byte-identical to `claims[0].pins`; `frozen_claims_sha256` = `de3afbfb…` = sha256(`claims.json`).
- Receipt half was false at the stop commit: `git show --stat cd75b92e` and `b917ea64` list no such receipt; `find .ufo/waves/round-34/r34b -name '*receipt*'` returned nothing at 07:28–07:34Z.
- Produced later at `5a0435ff`: `after/freeze-integrity-instruments.txt` (sha `d68e4e17…`) ends
  `freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe rev=66b84027…`.
- Reproduced independently (07:37:42Z):
  - `python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34/r34b --claims .ufo/waves/round-34/r34b/instruments.json --rev c79bbe7b…` → `ERROR no commit adds … at c79bbe7b…`, **exit 2**.
  - same with `--rev b917ea64…` → `CLEAN pins=26 freeze=b917ea64ebbe rev=b917ea64…`, **exit 0**.
- So no freeze-bound CLEAN at `c79bbe7b` is producible by this tool: the container was added after the freeze (`b917ea64`, the stop's parent). The addendum states this honestly ("freeze=b917ea64 is the commit that added instruments.json, not c79bbe7b"). The frozen record's field still reads as if the receipt were landed with the repair; it was not.

### F3 — MEDIUM — `frozen_counter_verdict` presents `measured_revision` as a revision binding; the counter echoes `--rev` and reads no revision

- `c2-shortcut-gate-counter.py:73` sets `receipt["measured_revision"] = args.rev`; `grep -c 'git\|hashlib'`… the file imports neither and runs no VCS command (SentinelContainment C6 independently: "imports no `hashlib`, runs no `git`/`jj`").
- Demonstrated (07:37:45Z): same tree, `--rev 0000…0000` → exit 0 and a receipt **identical in every field except `measured_revision`** (`receipt-echo.json` vs `receipt-frozen.json`, `only_measured_revision_differs=True`).
- The measurement is nevertheless materially at the frozen bytes: receipt birth `04:13:24.882 -0300` = 07:13:24Z, 13 s after the freeze commit 07:13:11Z and before any later commit; and `git diff c79bbe7b HEAD -- tools/round-34` is empty (frozen instruments unchanged at every tip). So the field is not a false measurement — it is an unenforced binding, and the stop record does not list it among its five defects (LOG and SCORECARD item (6) do).

### F4 — MEDIUM (record-time provenance, now bound) — the `observed.seeds` map had no receipt artifact when written

- The pinned counter emits no seed field (`mini-counter.py:score/main` return `rows` without seed), and wave-1 scratch holds no seed-named receipts: `grep -l 'alt-1\|alt-2' /fast/scratch/hyaku/kaidoku-r34b/w1/ExecRedReproduce/*` → no match; `b2.txt` (naive, matched 8) and `d2.txt` (green, matched 8) are seedless.
- The seed rows existed only as prose in `ExecRedReproduce.md` §5. Also, the third key `kaidoku-r34-mini-v1` is the counter's default `--seed` (verified in source), which the wave-1 table presents only as the unseeded 07:19:02Z run; the label is a correct inference, not a receipt label.
- All three values are true: reproduced 8/8 at `kaidoku-r34-mini-v1`, `alt-1`, `alt-2` (and `alt-3`) at 07:37:47Z.
- Post-stop: `nameset-green-receipt.json` (sha `fa6e8f09…`, addendum-bound) now carries argv, cwd, `utc_start/utc_end` 07:34:01Z, exit 0, matched 8, target 8, `source_sha256 2e8feaea…`, `counter_sha256 43ef669f…` for four seeds. It binds the values; it does not make the record's 07:28 clock true (F1).

### F5 — LOW — `kill_rule_applied` "no capability row enters SCORECARD" is literally false at every tip after `66b84027`

- At the stop commit the clause held: `git show --stat cd75b92e` touches no SCORECARD file.
- `66b84027` (07:32:25Z) added a Round-34 run-6 `R34-C2` row with verdict "falsified measure / honest stop" and owned axes `coverage 10→10`, `depth 10→10`, `calibration 10→10` (`SCORECARD.md:3347-3360`). The row enters no capability and no score, so the intent ("no capability credit") is satisfied; the literal wording needs the scope "at the stop".

### F6 — LOW — F2's wording "no instrument reads the predicate value"

`replay-gate.py:43` requires the `predicate` key to be present (so the config value is *read* into memory) but never compares or asserts it against anything; the C2 counter echoes its own constant. Substance ("nothing verifies predicate identity") is correct; "reads" should be "verifies/compares".

## 3. Positive verifications (what the record gets right)

- Predicate identity of the frozen sentence: `predicate_frozen` ≡ `claims[0].predicate`, sha256 `7c6c17f0cca6c680507d4eec33b4c0c82a76c4f73e9a98ceb4bde54a9a96279b` (CHECK-2).
- The A/B split and hashes in `predicate_note`: A `7c6c17f0…` (claims + both configs), B `8340aea5…` (counter constant + after receipt + all five control receipts).
- Frozen revision: exists, is the claims-freeze commit, ancestor of the audit-start tip and of every later tip (CHECK-4).
- Source binding: `nameset.py` sha256 equals the record, the wave-1 report pin, the Appendix A code, and the addendum's artifact map.
- Counterexample reproduced independently in a 26/26-pin copy: `matched 8`, `target 8`, `met_target true`, exit 0 at four seeds.
- Frozen verdict reproduced verbatim: `GATE_COUNTER_OK … green_positive_matched=8 clauses_failed=-`, exit 0, six clauses true.
- Pins enforced in the repair container: 26 keys/digests identical to the frozen map; `frozen_claims_sha256` recomputes.
- Defect evidence pointers F1–F5 all exist and state what the record says they state (F3 floor=3 with no pin comparison; F4 M3 surviving selftest and inverting red to CLEAN; F5 receipts untracked until `b917ea64`, which is the stop's parent).
- No capability/score artifacts in the stop commit; owned scores 10→10 in `claims.json` and SCORECARD.

## 4. Exact commands, exits, UTC (authoritative receipts)

All UTC from `date -u` in the same shell call. `L` = lane root; cwd for checks 9–11 =
`/fast/scratch/hyaku/kaidoku-r34b/w2/AStopFields/probe` (copy of `tools/round-34`, 26/26 pins verified).

| # | argv (abridged) | UTC | exit | result |
|---|---|---|---|---|
| 1 | `sha256sum $L/.ufo/…/w1/CtlMultiset-files/nameset.py` | 07:37:42Z | 0 | `2e8feaea…8b97` |
| 2 | `python3 -c` compare `claims[0].predicate` vs `predicate_frozen` + sha | 07:37:42Z | 0 | `equal=True sha=7c6c17f0…279b` |
| 3 | `sha256sum …/claim-stop.json`; `git show 66b84027:…/claim-stop.json \| sha256sum` | 07:37:42Z | 0 | both `e6303d06…cbfc` |
| 4 | `git merge-base --is-ancestor c79bbe7b… <tip>` (4 tips, §0) | 07:28:23Z / 07:33:27Z / 07:38:01Z / 07:38:48Z | 0,0,0,0 | ancestor holds |
| 5 | `python3 -c` compare `instruments.json` vs `claims[0].pins` | 07:37:42Z | 0 | `n=26 keys_eq=True vals_eq=True` |
| 6 | `python3 -c` compare record `line`/`exit` vs `after/c2-at-instruments.{txt,json}` | 07:37:42Z | 0 | `line_eq_txt=True exit 0=0 measured_revision=c79bbe7b…` |
| 7 | `python3 -I -B $L/tools/round-34/freeze-integrity.py --root $L --round 34/r34b --claims .ufo/waves/round-34/r34b/instruments.json --rev c79bbe7b…` | 07:37:42Z | **2** | `ERROR no commit adds … at c79bbe7b…` |
| 8 | same with `--rev b917ea64…` | 07:37:42Z | 0 | `CLEAN pins=26 freeze=b917ea64ebbe rev=b917ea64…` |
| 9 | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev c79bbe7b…` | 07:37:42Z | 0 | `GATE_COUNTER_OK … clauses_failed=-` (identical line) |
| 10 | same with `--rev 000…0` | 07:37:45Z | 0 | receipt identical except `measured_revision` (echo proven) |
| 11 | `python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . --control-reader $L/.ufo/…/nameset.py --seed {kaidoku-r34-mini-v1,alt-1,alt-2}` | 07:37:47Z | 0,0,0 | `matched=8 target=8 met=True` each (also `alt-3` at 07:32:17Z) |
| 12 | `git show --stat cd75b92e` / `b917ea64` / `66b84027` / `5a0435ff` | 07:29–07:38Z | 0 | file sets quoted in §1/§2 |
| 13 | `python3 -I -B $L/tools/round-34/freeze-integrity.py --root $L --round 34/r34b --rev c79bbe7b…` (default claims path) | 07:36:21Z | **3** | `ERROR schema code=instruments_missing … where=instruments` |
| 14 | `stat -c '%w %y %z' …/claim-stop.json`; `git show -s --format=%ci cd75b92e` | 07:30Z | 0 | birth/mtime 07:23:32Z; commit 07:23:47Z |
| 15 | `python3 -c` dump `nameset-green-receipt.json` runs | 07:38:48Z | 0 | 4 seeds, `utc_start/utc_end=2026-10-25T07:34:01Z`, matched 8, exit 0 |

## 5. Residual risk and verification gaps

- **Record immutability vs addendum.** The defects above live in frozen bytes that are (correctly) not
  edited; the addendum binds new artifacts but does not rewrite the record's clock or its F1 wording.
  Anyone reading `claim-stop.json` alone still sees `l1_rerun_utc = 07:28`, which the bound receipt
  (`07:34:01Z`) contradicts.
- **No run of the pinned readers or the four control gates** by this seat (out of scope; other seats own
  them). I verified the frozen verdict's aggregate receipt only.
- **Receipt provenance before `b917ea64`.** F5 is disclosed; receipt bytes were mutable in the workdir at
  freeze time. My reproduction of the verdict line shows the value is reproducible but cannot prove the
  original run's argv.
- **Class-blindness is source-read, not executed.** I read `nameset.py` (raw-byte regex + table) and did
  not attempt to construct a case where the regex reads record bytes to emit a wrong answer; the addendum
  D1 already notes blindness is content-contingent.
- **Lane is still moving** (five tips inside eleven minutes). Later commits may change the evidence I
  cite; every hash above is pinned to the UTC at which I read it.
- **Stop substance untouched.** Nothing found here weakens the stop: the six clauses, the target, the
  predicate, the source hash and the 8/8 counterexample all hold as reproduced. No score, row or credit is
  implied by this report.

## VERDICT

`STOP_SUSTAINED / RECORD_FIELDS_DEFECTIVE`: every substantive field of `claim-stop.json` matches the
committed evidence and reproduces (predicate `7c6c17f0…`, freeze `c79bbe7b…` an ancestor of all tips,
source `2e8feaea…`, 8/8 at three seeds, the frozen `GATE_COUNTER_OK … clauses_failed=-` line and exit 0);
but `decisive_counterexample.l1_rerun_utc` is forward-dated 4 m 28 s past the record's own write and is
bound by no artifact (the only receipt for that class is stamped `07:34:01Z`), F1's "freeze-integrity
receipt over it" did not exist at landing and, when produced, binds `b917ea64` not `c79bbe7b`
(`--rev c79bbe7b` exits 2), `measured_revision` is an echoed argv with zero VCS contact (proved by an
all-zero-rev run producing an otherwise identical receipt), and three low-precision statements need scope
("no capability row enters SCORECARD" at `66b84027`; "no instrument reads the predicate value"; the seed
map's record-time provenance). No clause, target, class, threshold or label is affected, and no capability
or score is awarded.
