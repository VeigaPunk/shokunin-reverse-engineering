# R49 wave 1 — seat C2LogPtr (pre-freeze attack on atoms A3 and A4 of `tools/round-49/c2-mismatch.py`)

Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Read-only on the lane; no commit, stage, stash or push. Scratch removed; receipts in `.ufo/waves/round-49/w1/C2LogPtr/` (SHA256SUMS there). Run UTC 2026-10-28, 21:08–21:16.

## Verdict

**Defects to fold before the freeze.** The numbers the round-48 closure states about LOG pointers and the 72/75 wave accounting re-derive exactly from base git objects, and the counter's derived values match them. But the counter's A3 predicate is vacuous in three ways (partial pointer sets, duplicate lines, a stated 2e785632 phrasing the counter rejects), A3 and A4 leave named closure defects uncovered (c093e798 and 7fe11332 pointers, the LOG.md:3446 and fleet L14 wave wording, "0 dead seats"), and the plan's A3 wording ("per hash", "round-48 entry") disagrees with the code. A4 is consistent with the closure under the `.md`-bounded definition the counter encodes. Fold F-1 to F-6 before the freeze.

Counter at base (freeze = rev = base, lesson absent): `mismatches 9`, `atoms_total 9`, exit 1, all nine atoms red. Matches the plan's "at FREEZE reads 9".

## Findings (verdict-ordered; severity = would it let a wrong or incomplete record go green?)

| id | sev | finding | exact evidence | fix before freeze |
|---|---|---|---|---|
| F-1 | high | **A3 is not per-hash complete.** The counter checks only the `log_<hash>` keys a lesson states, and checks `unnamed` only one-directionally (listed hashes must be unnamed; omitted unnamed hashes are never noticed). The plan says "per hash, the full set" and "the hashes the round-48 entry never named". | Overlay with only `- A3 log_33f65a91=3440,3441,3444 unnamed=577a02a5,8847042a` → `A3: []` (green). Overlay R2 (`unnamed` omits 7fe11332, which is absent from LOG but cited by fleet L21) → `A3: []`. Command: `python3 -I -B forge_a34.py` (F1), `forge_recommend.py` (R2). Output: `forge_a34.out`, `forge_recommend.out`. | Require the stated key set to equal the set of hashes the closure/fleet report cites in LOG ranges (or a fixed list in the docstring), and the `unnamed` set to equal the set of cited hashes with zero LOG lines. |
| F-2 | high | **Duplicate atom lines: last one silently wins.** `lesson_lines` assigns `out[A3]=kv` per line. | F4: first line `log_2e785632=3442,3443,3444`, second honest → `A3: []`. F11 (A4): first `reports=73 missing=C1Battery-2,ScribeReportNumbers`, second honest → `A4: []`. Both in `forge_a34.out`. | Reject more than one `- A3`/`- A4` line (exit 1). |
| F-3 | high | **Closure phrasing for 2e785632 disagrees with the counter.** Closure text says "the 2e785632 commit is at LOG.md:3445". LOG names it at 3440, 3441 and 3445. The counter requires the full set. A lesson copying the closure's phrasing goes red. | F2: `log_2e785632=3445` → `A3: ["log_2e785632: stated [3445], derived [3440, 3441, 3445]"]`. Closure line 18 vs `grep`-equivalent derivation (`derive_a3_a4.out`, A3 block). The closure's 33f65a91 sentence ("3440, 3441 and 3444") is complete; only 2e785632 is short. | Lesson must state the full derived set; record in the lesson that the closure's 2e785632 pointer omitted 3440/3441. |
| F-4 | med | **c093e798 not covered.** Fleet report L23 cites `LOG.md:3440-3441` for c093e798; LOG names it at 3440, 3441 and 3445. Neither the closure nor any atom mentions it. | `derive_a3_a4.out` fleet block: `fleet L23 cite LOG.md:3440-3441 hash c093e798 LOG lines [3440, 3441, 3445]`. R1 with `log_c093e798=3440,3441,3445` → `A3: []`; R3 with `3440,3441` → red (`stated [3440, 3441], derived [3440, 3441, 3445]`). | Add c093e798 to A3 keys (F-1 fix covers it). |
| F-5 | med | **7fe11332 not covered.** Fleet report L21 cites `LOG.md:3436-3439` for the round-48 first freeze `7fe11332`; LOG never names it (0 lines), and the counter's `unnamed` list omits it. `7fe11332` is a real commit (`git cat-file`, subject "round-48: freeze — the meaning-bound registry counter…"). | `derive_a3_a4.out`: `fleet L21 … hash 7fe11332 LOG lines [] within-cite []`. R1 (`unnamed=7fe11332,577a02a5,8847042a`, `log_7fe11332=none`) → green. | Add to `unnamed` (F-1 fix covers it). |
| F-6 | med | **Wave-accounting wording in LOG.md:3446 and fleet L14 is not covered.** Both say "73 seats produced reports; no-report seats: C1Battery-2 (and) ScribeReportNumbers" and "0 dead seats" / "Dead seats: 0". `C1Battery-2` is a receipt directory, not a seat. No atom checks either line; A4 checks only the round-49 lesson line. The registry gives no durable settlement evidence: `agentId` is null for all 75 members. Closure routed defect 7 asks for settlement evidence or no "0 dead seats" claim. | `derive_a3_a4.out`: `registry agentId null: 75`. LOG.md:3446 and fleet L14 quoted in `derive_a3_a4.out` tail. | Either add an A4 clause that the correction line names the superseded lines (LOG.md:3446, fleet L14), or disclose in the plan's limits that the "0 dead seats" and "73" wording stays uncounted. Do not assert "0 dead seats" in the landing. |
| F-7 | verified, definitional | **Report-artifact definition: the slash boundary and the `.md` restriction both matter.** The counter and the closure agree on `md_bound`. Other readings give the round-48 record's numbers. | `derive_a3_a4.out`: `md_bound reports=72 missing=[C1Meaning, C1Battery, ScribeReportNumbers]` (= closure, = counter); `any_bound reports=73 missing=[C1Battery, ScribeReportNumbers]` (C1Meaning counted via `C1Meaning/receipt.json`; this is what LOG.md:3446's "73" effectively used); `any_nobound reports=74` (C1Battery counted via `C1Battery-2/receipt.json`, which the `w1/<seat>/` slash prevents). | State in the plan: non-`.md` files (receipt.json, counter-command.txt) do not count; `<seat>-2` directories are not seats. The counter already does this correctly; the text should say so. |
| F-8 | low | **Plan vs counter wording.** Plan A3 says "the hashes the round-48 entry never named"; the counter tests the whole LOG.md (`line_numbers(base, h)`). Closure says "not named in LOG.md" (whole file). At base the two agree for 577a02a5 and 8847042a (0 lines in the whole file). | `c2-mismatch.py` A3 `un` loop; `derive_a3_a4.out`. | Align the plan to the counter (whole file) or change the counter to the round-48 section (LOG.md 3436–3449). |
| F-9 | low | **Key-length fragility.** LOG names hashes by 8 hex (except `b6f7ca2a…` at 3439 in full). A lesson keyed by 40-hex gets a false mismatch, and the battery regex `log_([0-9a-f]{8})=` then finds no pointer to mutate (battery count drops below 11). | F3: `log_33f65a913cfd21a4491a4f8b7ccc8f00069f058d=3440,3441,3444` → `"stated [3440, 3441, 3444], derived []"`. | Normalize keys to 8 hex or reject 40-hex keys with a message; the plan should fix the key format. |
| F-10 | hygiene | **`tools/round-49/__pycache__/` exists** with `c1-counter.cpython-314.pyc` (18:10:36), `c1-run.cpython-314.pyc` (18:09:53), `c2-mismatch.cpython-314.pyc` (18:10:14). My runs used `-B` / `dont_write_bytecode`; I did not delete it (not mine; the tree is shared). The freeze commit must not include it. | `ls -la` of the draft dir. | Remove `__pycache__` before the freeze or ignore it; keep it out of the `tools/round-49` blob set. |

## Closure statements re-derived (the requested check)

| closure statement (`corpus/lessons/round-48-verifier-spotcheck.md`, Step-1 "Cited lane hashes" / "Report shape", Routed defects 7–8) | re-derivation at base | counter definition | agree? |
|---|---|---|---|
| `2e785632` "is at LOG.md:3445, outside the cited 3442–3444" | 3440, 3441, 3445 (8-hex substring over base blob) | full set `[3440,3441,3445]` | **Partly.** Pointer outside 3442–3444: true. Set incomplete in the closure (omits 3440, 3441); counter requires the full set (F-3). |
| `33f65a91` "appears at 3440, 3441 and 3444, not the cited 3439" | 3440, 3441, 3444 | `[3440,3441,3444]` | Yes. |
| `577a02a5` / `8847042a` "not named in LOG.md" | 0 lines each (8-hex and full 40-hex) | `unnamed` check | Yes (but one-directional, F-1). |
| "72/75 seats have report artifacts, not 73" | 72 (`md_bound`) | `reports=72` | Yes. |
| missing = C1Meaning, C1Battery, ScribeReportNumbers | same three | `missing` | Yes. |
| `results registry names C1Battery; C1Battery-2 is a receipt directory, not a seat` | `results.json` 75 unique names, no `-2`; registry `swarm-registry.json` 75 members, identical set; `w1/C1Battery-2/receipt.json` only | — | Yes. |
| C1Meaning "blocked by frozen_worktree_dirty" | token present in its results output; `dirty-worktree` guard text | not counted by A4 (fleet-report wording, F-6) | Yes for the fact; uncovered as a claim. |
| "The prompt required a planner role; the wave had none" | 0 members with role `planner` | not counted | Yes (uncovered). |
| LOG.md:3446 role mix `executor 22, scribe 16, reviewer 9, scout 9, critic 6, mutation-tester 6, connector 2, revenger 2, simplifier 2, sentinel 1` | identical to registry role counts; sums to 75; attack roles 21/75 | not counted | Yes (uncovered; fleet L14 repeats it). |
| Fleet report L22/L24 LOG pointers (2e785632 cited 3442–3444; 33f65a91 cited 3439) | as above | A3 keys | Stated defects; counter covers 2e785632 and 33f65a91 only through the lesson's own keys (F-1). |

## Verification performed (exit codes and hashes)

- `git show e4f2cfa5…:LOG.md` = `cd855f88a7a0af65261e59b2a7bd294ad206a6ef2f21cb59b3bb8764346e7b10`; identical to tip `8847042a…:LOG.md` (`git diff --name-only 8847042a e4f2cfa5 -- LOG.md` empty).
- `git show e4f2cfa5…:.ufo/waves/round-48/r48-w1-results.json` = `8eec161e5e250d6747d1127b104b10dfab7469492cc62813b3651e376fd2b2c7`, 75 names, 75 unique.
- `git ls-tree -r --name-only e4f2cfa5… -- .ufo/waves/round-48/w1` → 494 entries, newline-joined sha256 `c0a65a87c3444a0718685c9c32aa6e1fe331ec9036455ca788bcb112f3a139a9`.
- `git show e4f2cfa5…:.ufo/waves/round-48/w1/swarm-registry.json` = `5849042c9bc8c8c2cd876e6e97a13d6cc8d72c6c8e6ff1195ed5263ae108a4e0`.
- Fleet report `git -C /home/vgpnk/Projects/shokunin show 7b845bef80a797b7b90944c6ab2752dbbc9afaa9:.ufo/reports/round-48/kaidoku.md` = `a6895609b910ec8f4511f0783f18f7151c86934bf04495018a503a1e5749914b` (read-only).
- Counter at base: `python3 -I -B .ufo/waves/round-49/draft/tools/round-49/c2-mismatch.py --root <lane> --rev e4f2cfa5… --freeze e4f2cfa5… --json-out …` → exit **1**, stdout sha256 `d78401f2…`, `counter_sha256 90fa4722c960a8c21dd3166f115f721fa097115cc576703478c7a55c7d15243f`, `mismatches 9`.
- `derive_a3_a4.py` (`python3 -I -B`) → exit 0; output `derive_a3_a4.out` sha256 `451187bac6685ff1e1838c5be2ce3cfd91dcb6b7543dae792cb6c051651e852c`.
- Forgery harness (`forge_a34.py`, `forge_recommend.py`, both `python3 -I -B`, in-memory overlay of the lesson path on the base revision; no file written) → exit 0 each; outputs `forge_a34.out` (`5d586f9f…`), `forge_recommend.out` (`d0eb275c…`). The harness imports the draft counter read-only; `dont_write_bytecode` is set.
- Battery arms A3 and A4 (honest overlay): mutation "A3 one pointer line number moved" flips only A3 (`stated [3441, 3441, 3445]`); "A4 reports count off by one" flips only A4 (`reports stated 73, derived 72`). Both arms are live.
- Lesson working tree = HEAD: `sha256 a46da21f264b5c6fd23f2fe6c0ab6cadc7dad2788d5093dfc7a776131aac13e8`; `git diff --quiet HEAD` exit 0.
- Not run: `--battery` at base (needs the round-49 lesson; cannot run before the freeze); atoms A1, A2, A5–A9 (outside this seat's scope; C2 seats or the freeze must check).
- Tools installed: none.

## Landing text (validated in the harness; green under the current counter, must pass after F-1 to F-2)

```
- A3 log_2e785632=3440,3441,3445 log_33f65a91=3440,3441,3444 log_c093e798=3440,3441,3445 log_7fe11332=none unnamed=7fe11332,577a02a5,8847042a
- A4 seats=75 reports=72 missing=C1Meaning,C1Battery,ScribeReportNumbers
```

Suggested correction prose (not counted by the atoms): name the superseded LOG.md:3446 "73 seats / C1Battery-2" wording and fleet L14 as superseded; state that `C1Battery-2` is a receipt directory; record the closure's 2e785632 omission of 3440 and 3441.

## Files

- Derivations and forgeries: `.ufo/waves/round-49/w1/C2LogPtr/` (`derive_a3_a4.py/.out`, `forge_a34.py/.out`, `forge_recommend.py/.out`, `c2-at-base.json/.stdout`, `swarm-registry.json`, `fleet-report-r48.md`, `SHA256SUMS`).
- No draft tool, plan, doc, corpus, LOG, SCORECARD or tools file was edited.
