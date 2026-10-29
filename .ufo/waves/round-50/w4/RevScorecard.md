# RevScorecard — round 50 attempt 2, wave 4 (falsify): SCORECARD.md review

Verdict: **LANDING HOLDS with 3 documentation-calibration defects + 1 precision nit** — every quantitative claim re-ran or re-derived reproduced (C1 2/4 and the twelve-entry derivation, C3 19→0/126, 18 selftest cases, controls 19/126/26/51, C2 11 atoms/52 mutations, coverage 140/140, QUALITY 94–95, SOURCES 152→156 with all four rows byte-reopened, `## Record corrections — round 50` last, round-51 bullet names the gap-rule re-freeze). No measurement overturns; the defects are stale or overstated citation text, each with a minimal fix.

Reviewed rev `c67b741e8f6bd8d64adbdb15e059d47fde004c77` (clone at `/fast/scratch/hyaku/kaidoku-r50/w4-RevScorecard/clone`). Note: two later commits (`a3615f70` w4 dispatch, `db61a907` w3 stragglers) touch only `.ufo/waves/` — no review target moved. No installs needed (pacman paused; nothing installed).

## Findings (severity order)

### F1 — SCORECARD claims table pins a stale C3 instrument hash (minor, calibration)
- **Claim**: `SCORECARD.md` round-50 attempt-2 table, R50-C3 "before" cell: instrument `tools/round-50-c3/sqfs-triage-v5.py` "(sha256 `05df514f…`)".
- **Measured**: tip instrument is `ef4633c523ca8ab4ff096a7d90ef7074461a67f03952ad3652a048dce84d3ed0`.
  Command: `sha256sum tools/round-50-c3/sqfs-triage-v5.py` (clone @ c67b741e). `05df514f…` existed only at `c3121c4f`/`bff7d96c` (the SCORECARD's own commit — correct then, stale at the tip). The instrument at the C3 landing rev `1439dfe9` is a third hash, `a2ebb5a4…` (all four blobs swept: ef4633c5 / 05df514f / a2ebb5a4 / af1b22ba = the never-landed 49-byte stub).
- **Evidence**: receipt `c3-after.json` binds `instrument_sha256 ef4633c5…` and its freeze block honestly records `instrument_sha256_at_rev a2ebb5a4…`; `SKILL.md:572` (block 26 status) already cites the correct `ef4633c5…`. Only the SCORECARD cell drifted. Exit codes: all 0. sha256s above.
- **Minimal fix**: in `SCORECARD.md:3796` change `05df514f…` → `ef4633c523ca…` (append-only lane: land as a record correction, cf. the round-50 attempt-2 record-corrections pattern).

### F2 — LOG.md C3 line cites a hash that exists at no landed revision, and the wrong selftest count (minor, calibration)
- **Claim**: `LOG.md:3479` — instrument "(sha256 `99294ea36066483697f2dc10d2051a759d0f5cbdde6883c4b49b1e89362671bf`, … `--selftest` 16 cases green)"; "final instrument addbfb4d→(this commit's parent chain)".
- **Measured**: `git rev-list --all --objects | grep sqfs-triage-v5.py` + per-blob sha256 → only ef4633c5, 05df514f, a2ebb5a4, af1b22ba ever existed. `99294ea3…` is none of them. The commit LOG names as final, `addbfb4d`, carries `a2ebb5a4…` with **15** selftest cases (`git show addbfb4d:… | grep -c 'def c_'` = 15); from `c3121c4f` through the tip the count is **18**. So "16 cases" was never true at any landed rev, and the hash was never true anywhere. The LOG entry was committed at `bff7d96c` where the instrument was already `05df514f`/18 cases — internally inconsistent at its own commit and further stale at the tip.
- **Evidence**: selftest re-run (this seat) — `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest --root <clone> --work <scratch>` → **exit 0, "selftest: 18 cases, pass 18, fail 0"** (stdout sha256 `78cefa32…`, artifact `RevScorecard/selftest2.out`).
- **Minimal fix**: append a LOG correction line (LOG is append-only): C3 final instrument `ef4633c5…`, `--selftest` 18 cases, landing rev `1439dfe9`; the `99294ea3…`/16-case parenthetical described a pre-landing draft.

### F3 — SCORECARD C1 claim "the counter's own REA rerun reproduced every projection" is contradicted by its own receipt (minor, accuracy; verdict unaffected)
- **Claim**: `SCORECARD.md:3796` R50-C1 "after" cell.
- **Measured**: `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` → `carriers.g7581.projection_ok = False`; `projection_error` = `execution_failure` (unblob `ENOENT … readlink '…/usr/www.myfritz/avme/cgi-bin/luacgi'`, exit 1, `retryable false`); `failing` includes `g7581:projection_ok`. `projection_ok` is defined in the counter (`c1-counter.py:209`) as "the counter's own REA run of the carrier bytes". c6430/c6490/g7582 have `projection_ok True` — 3/4 reruns reproduced. All four carriers still have `published_files == oracle_files` (4 556/4 564/4 709/3 955), so "REA published every frozen-oracle regular file on all four carriers" holds (from the data-run receipts).
- **Minimal fix**: qualify the clause — "the rerun reproduced the projection on the two matched carriers and g7582; g7581's scoring-time rerun errored (unblob `execution_failure`), its published-file equality holding from the data-run receipt". The honest-miss verdict is untouched (g7581 already fails `gaps_ok`).

### F4 — wave-shape sentence "attack 11/35 = 31%" doesn't match its own role enumeration (nit)
- **Claim**: `SCORECARD.md:3790` and `LOG.md:3478` — "executor 10, scribe 7, scout 5, critic 4, reviewer 4, connector 2, mutation-tester 1, revenger 1, sentinel 1 — attack 11/35 = 31%".
- **Measured**: `.ufo/waves/round-50/w3/swarm-registry.json` — 35 members; role counts exactly as enumerated. Attack-kind roles (critic+reviewer+mutation-tester+revenger) = **10** → 10/35 = 28.6%. 11/35 = 31.4% only if sentinel is counted as attack.
- **Minimal fix**: either "attack 10/35 = 28.6% (critic/reviewer/mutation-tester/revenger)" or name sentinel in the attack set.

## Checks attacked and held (all re-ran / re-derived by this seat)

| # | check | command (clone @ c67b741e) | result |
|---|---|---|---|
| B1a | coverage head 140/140 | `git ls-tree -r --name-only c67b741e -- corpus/knowledge \| grep -c '\.md$'` | **140**, exit 0; base `f890bbea` → 139 (matches "attempt-1 landing read 139/139") |
| B1b | `## Record corrections — round 50` is last `##` | `grep -n '^## ' SCORECARD.md \| tail -1` | line 3806, last ✓ |
| B2a | C1 before | read `l1/scores/c1-before-attempt2.json` | `carriers_matched 0`, target 4, exit 1, rev 435d41fd ✓ |
| B2b | C1 after | read `l1/scores/c1-after-attempt2.json` | `carriers_matched 2`, target 4, exit 1, rev 646d29c9, counter/gap-rule/carriers unchanged ✓ |
| B2c | twelve-entry derivation | oracle TSVs + gap-rule.json | g7581/g7582 each **13** char-device entries (`dev/led 247:0`, `dev/pts/0-7 136:x`, `dev/tiatm 230:0`, `dev/ttyp0-2 3:x`); rule `removed.silent.char-device=["247:0"]` admits 1 → **12** with no disposition ✓ (entry/README/SCORECARD all say twelve; receipt `gaps_note` truncates at 8 by `c1-counter.py:1564` `sorted(missing)[:8]` — cosmetic cap, scoring uses the full set) |
| B2d | carrier counts 4 556/4 564/4 709/3 955 | receipt per-carrier | g7581 4556, g7582 4564, c6490 4709, c6430 3955; `published_files == oracle_files` on all four ✓ |
| B2e | POS red PRE-data, kill silent | `controls-attempt2/pos/{counter,receipt}.json`, `summary.json` | POS measured exit 1 vs expect exit 0 (all-bindings-true) at rev 80074886 **before** the data run (UTC 20:43 vs data run 21:0x); `kill_rule_fires: False` ✓ |
| B3a | C3 before re-run | `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root <clone> --rev f890bbea… --freeze 435d41fd… --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes --json-out <out> --work <w>` | **exit 1**, 19 mismatches, all `*_ddefault`, per-family 4 v2ns + 7 v3_broadcom + 8 v3_nonstandard, all evaluator labels `clean-unverified`/`record-unverified` ✓ (receipt `RevScorecard/c3-before-rerun.json`, sha256 `7cac07cf…`) |
| B3b | C3 after re-run | same at `--rev 1439dfe9…` | **exit 0**, `pair_mismatches 0`, `evaluator_missing 0`, n=126, table v5, binds `ef4633c5…` ✓ (`RevScorecard/c3-after-rerun.json`, sha256 `b14eb434…`) |
| B3c | selftest 18 cases | `… --selftest --root <clone> --work <w>` | **exit 0, 18/18** ✓ (case 17 confirms the claim file names the ddwrt failed body) |
| B3d | controls 19/126/26/51 | read `c3/ctl-{do-nothing,junk,guard-deleted,action-swapped}.json` | 19/126/26/51 ✓; `ctl-junk-parse-refusal.log` exists (literal all-`clean` variant refused) ✓. These are base-rev/v4-table controls per `ExecTriageControls.md` F10 — consistent with the claims file |
| B3e | ddwrt residue | after-rerun labels | `dmg_Z3_v3ddwrt_inode_table` → `legacy-body-failure` under table AND evaluator ✓ (disclosure accurate) |
| B3f | v5-table mutation battery (this seat, fixture clone) | 6 mutations, receipts `RevScorecard/mutations.json` (sha256 `cefa1cdf…`) | guard-deleted → exit 1/19; action-swap → exit 1/19; silent `squashfs_v[123]` → exit 1/1 (ddwrt body); malformed junk → exit 2 refused; grammar-valid junk → **exit 1**/94 (semantic red, never green); **glob-revert → exit 0/0 corpus-green but fixture-caught** — disclosed corpus limit (zero no-reader extractor-failure envelopes, ExecTriageV5 F4); the same mutation (`legacy-glob-widened`) is in the instrument's MUTATIONS battery and flips synthetic pairs (selftest case `mutations_each_flip_their_own_pairs` green) |
| B4 | wave shape | registry count | 35 seats; role counts exact ✓ (only the "attack 11" arithmetic off — F4) |
| B5 | round-51 bullet | read SCORECARD | names "re-freeze the C1 gap-accounting rule from per-carrier-class derivation … then re-run the four carriers" ✓ |
| B6 | QUALITY rows 94–95 | `corpus/QUALITY.md:151-152` | exist as bullets (precedent: rows 75–79 same list), cite `corpus/lessons/round-50.md` M50-7/M50-10, supersedes `—` ✓; lesson sections M50-7..M50-10 present ✓ |
| B7 | C2 at tip | committed receipt + independent re-run `python3 -I -B tools/round-50/c2-record.py --root <clone> --rev c67b741e… --freeze 435d41fd… --battery` (734 s) | committed `c2-final-attempt2.json`: atoms 11, mismatches 0, exit 0, battery failing [], `do_nothing_red 11`, `mutation_count 52`, counter == freeze hash ✓. **Independent re-run at the true tip: exit 0, atoms 11, mismatches 0, failing [], do_nothing_red all 11, 52 mutations, counter==freeze** ✓ (`RevScorecard/c2-rerun-tip.json`, sha256 `99feef93…`). The "re-verified green at the tip" claim holds at `c67b741e` proper, not only at the receipt's named rev `bff7d96c` |
| B8 | SOURCES re-open | re-fetched all four URLs 2026-10-29 | S243 patch byte-identical (`e28b3341…4c707`, 1,153 B; quote `:7` + `:17-18` locate ✓); S245 `squashfs.py` byte-identical (`2d7b901b…599287`, 19,842 B; `:53-54`, `:455` locate ✓); S249 `info_en.txt` byte-identical (`6c601b34…070a7`, 67,591 B; `:850` 18-word quote locates ✓); S244 four carrier dirs list the exact size/date rows ✓. Registry 152 (`f890bbea`) → 156 ✓; one-bullet `## Search log` ✓ (artifacts `RevScorecard/s243.patch`, `s245.py`, `s249.txt`) |
| B9 | entry/README/PROVINCE/LOG | read | entry line 52 states 13 entries/twelve undisposed ✓; README coverage-map row + knowledge row + frontier note ✓; PROVINCE `## Round-50 measured, not promoted` ✓; LOG C1/C3 entries ✓ (C3 line defective — F2) |

## Pending / not run
- **C1 counter `--selftest`**: attempted, killed at my 240 s guard (exit 124). The C1 predicate command was not run (L1-owned, REA-invoking — contract). All other C1 evidence was verified by reading the committed receipts and independently re-deriving the gap arithmetic from the frozen oracle tables.
- Assignment fragment "19 W04" maps to no artifact in `SOURCES.md` (no `W04` string anywhere; the Search log records one bullet, identified/screened/included 4). Residual notation gap, not a lane defect.

## Residual risk
- The depth head still reads "25/25 queue-drain rule blocks" (round-48 proxy); block 26 (triage v5) is landed and scored, making the live count 26. The round section discloses this ("historical statement … not re-run this round") — a deliberate proxy choice, not a defect, but the next round that touches the head should re-run command A.
- The two hash defects (F1/F2) are the kind a future round quotes without re-checking; both are cheap record corrections. The C3 receipt's own dual-hash binding (tip hash + `instrument_sha256_at_rev`) is the model of how to state it.
- m1 (glob revert) staying corpus-green is disclosed but worth re-stating in any v6 work: a table that re-condemns no-reader families would score 0/126 until a no-reader extractor-failure envelope enters the corpus.
- No fleet-root or lane-tree writes were made by this seat; all mutations ran on a scratch clone (`/fast/scratch/hyaku/kaidoku-r50/w4-RevScorecard/mutlane`, toplevel verified), removed at yield.
