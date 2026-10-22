# kaidoku round 28: verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Session `HyakuCloseKaidoku28`, 2026-10-22, 19:27Z to 19:40Z. Range `935c36608008f79e3dea4f1ed191df3c89e3b848..242b0d8b8ad6ff6c693fa5114216fbb538b587bf`. Report `.ufo/reports/round-28/kaidoku.md` (fleet `656e724de4e01f017d25d6d9765e966c11473eaf`). No seats were dispatched: every re-check below was run by this session. No tools were installed.

Driver digest (copied from `.ufo/watchdog.log`):

```
2026-10-22T14:09:06-03:00 launch kaidoku round=28 pgid=4046479 driver=hyaku-inline attempt=1
2026-10-22T14:30:08-03:00 lane-dead-no-report kaidoku round=28; retry same round (hyaku-inline attempt=1: omp process restart at 17:26Z; no landed report; fresh successor inherits work)
2026-10-22T14:30:09-03:00 launch kaidoku round=28 pgid=1003349 driver=hyaku-inline attempt=2
2026-10-22T16:27:10-03:00 complete kaidoku round=28; hyaku-inline attempt=2
```

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by the lane | `git log --format='%an %H' -- .ufo/reports/round-28/kaidoku.md` (fleet) | `kaidoku-shokunin 656e724de4e01f017d25d6d9765e966c11473eaf` | pass |
| SHONEN heading, one line per box | read of the report `## SHONEN` | 4 lines, all `[~]`, each with a pointer | pass |
| cited commits on the branch | `git merge-base --is-ancestor <h> main` for the 12 commits `87d3dfb6` … `242b0d8b` | all 12 ok; 12 commits in range, all `kaidoku-shokunin <kaidoku@shokunin.local>` | pass |
| pushed | `scripts/hyaku/jj-lane.sh state <lane>` | `branch=main local=242b0d8b… remote=242b0d8b… ahead=0 behind=0 head=detached tracked=1 untracked=0` | pass |
| leftovers | `git status --porcelain` | ` M .ufo/waves/round-28/a2w/ExecR27SelftestFix.md` | defect (below) |
| prompt carries the template contract | `grep -nE '^## ' .ufo/prompts/kaidoku-round-28.md` | §1 MISSION/AXES, §2 Claims, §2b Frontier, §3 L2 floor, §4 Report contract, §5 Commit/push, §6 hyaku addendum | pass |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | `kaidoku ok`, six W04 (S033, S047, S054, S062, S069, S083), exit 0 | pass, equal to the report |

The one tracked leftover, `.ufo/waves/round-28/a2w/ExecR27SelftestFix.md`: 13 insertions, 14 deletions against the committed copy (committed 16:25:35-03 = 19:25:35Z in `242b0d8b`). The diff only changes the seat's run timestamps (19:19Z → 19:26Z, 19:17Z → 19:24Z) and adds one sentence about dead assignments removed from its sandbox patch. It is the seat's own report, rewritten by the still-running seat `KaidokuR28a2.ExecR27SelftestFix` after Main's 19:25Z hard stop. It is **not round work**: no claim, counter, entry, SCORECARD or LOG byte depends on it, and the report already says this seat's diff was not integrated. Status-neutral defect: the lane closed with a live seat still writing into its tree.

Frozen inputs unchanged since their freezes (`git diff --quiet 87d3dfb6 242b0d8b -- .ufo/waves/round-28/claims.json tools/round-28/c1-heldout-naming.py corpus/evidence/round-28/c1/carriers.tsv corpus/evidence/round-28/c1/heldout.tsv` → 0; `git diff --quiet 86fa8526 242b0d8b -- .ufo/waves/round-28/claims-c2.json tools/round-28/c2-filtered-flag.py corpus/evidence/round-28/c2/selectors.tsv corpus/evidence/round-28/c2/canonical-signatures.json` → 0). Order: C1 freeze 14:17:16-03, C1 runs 14:22:32-03; C2 freeze 14:21:55-03, C2 fetch commit 14:45:05-03.

## Per-claim re-check

Both counters are lane-owned gates (PROTOCOL §Gate standard): they were not executed. Their committed receipts were verified, and the counted quantities were re-measured with plain awk/jq/grep over the bytes at `242b0d8b`.

### R28-C1 (coverage): re-measured, target missed

- Runs: `git show 242b0d8b:corpus/evidence/round-28/c1/runs.tsv | awk -F'\t' 'NR>1{e[$3]++} END{for(k in e) print "exit"k"="e[k]}'` → `exit0=60 exit1=1`. Reported `runs_ok=60/61`: agree.
- Rows: `heldout.tsv` has 187 data rows; `tally.json` `.tally.selector_rows 187`, `recovered_by_rea 186`. Reported `rows_complete=186/187`: agree.
- Triple: `jq '.tally.rules.openchain_sole_unfiltered_args_consistent'` → `named 137, right 137, wrong 0, no_name 50`. Agree with the report and the entry.
- Miss cause: `git show 242b0d8b:.ufo/waves/arc3-loop1-round3/claims/c1/CR-1/out/Cr1LibUser.noopt.runtime.hex | grep -o '__\$[0-9a-f]*\$__' | sort | uniq -c` → `1 __$a2bad93077572174e8e5044433a5a7d5f3$__`; `envelopes/h09.json` reason `invalid_format`, "Hex carrier requires complete hexadecimal byte pairs". Agree.
- Committed gate evidence: `.ufo/waves/round-28/after/c1-at-9db24c9e.txt` ends `runs_ok=60/61 rows_complete=186/187 tally_equal=1 entry_ok=1`, `exit=1`; selftest `cases=21 failures=0`, `exit=0`. The frozen target (`61/61`, `187/187`, exit 0) is not met.
- Verdict: claim **does not verify** (honest stop, declared as such). No list, counter or target edit after the freeze (diff above).

### R28-C2 (depth): re-measured, target met, weakened test

- Responses: 230 `openchain-*.json` files plus `manifest.json` (230 keys); `jq -s '[.[]|select(.ok==true)]|length'` → 230.
- Independent rule check (my own jq, not the lane counter): for every candidate under `.result.function`, predicted `filtered` = selector is a key of `canonical-signatures.json` and the name differs from its `signature` → `{"entries":246,"mismatches":0,"predicted_true":59}`. Reported `entries=246 mismatches=0 predicted_true=59`: agree.
- Committed gate evidence: `after/c2-at-9db24c9e.txt` `exit=0`; selftest `cases=17 failures=0`. `after/preseen-overlap-c2.txt`: `test_selectors=230 seen_before_freeze=168`, exit 1.
- Verdict: the frozen target verifies. As the lane itself found (M28-4, M28-5), 168 of 230 selectors and all 59 predicted-true entries were seen before the freeze, so this is a re-observation of a code rule (S084 `:47-48`), not a held-out test. I rule depth **unprovable-but-better**: the mechanism now rests on opened code (S084, S085, re-opened below) and 246 entries agree with it, but the test could not have failed on unseen data.

### Harm check

`git diff --stat 935c3660 242b0d8b` → 749 files, `+16482 -0`: the round deleted no line anywhere. `SCORECARD.md` +38 lines, all inside a new `## Round 28` section appended after `:3129`; `SKILL.md` +9, `PROVINCE.md` +1 (annotation at `:94`), `corpus/README.md` +4, `LOG.md` +12. No owned axis is harmed.

| axis | verdict | reason |
|---|---|---|
| coverage | unchanged | C1 missed its frozen target; the frontier bullet is annotated, not moved |
| depth | unprovable-but-better | C2 verifies but is a re-observation (M28-4) |
| calibration | unchanged | not claimed |
| operability | unchanged | not claimed; r27 selftest still red (`FAIL correct-stub`) |
| freshness | unchanged | not claimed |
| adjacency | unchanged | not claimed; PROVINCE Adjacent untouched |

Admission: not every claim verifies (C1 missed) → `admitted=false`, verdict `rejected-honest-stop`.

## Discernment spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S084 Sourcify `handlers.ts` @ `189cd726` | admit | `curl -sSL <S084 URL> \| sha256sum` → `30981efb…6c5a38`; `sed -n '39p;47,48p;66p;90p'` | agree | sha256 equals the Gate row; `:39` opens `filterResponse`, `:47-48` read `signatureItem.filtered =` / `signatureItem.name !== expectedCanonical.signature;`, `:66` closes it, `:90` `filtered: false,` as the Gate note says |
| S086 Solidity docs `v0.8.30`, Library Linking | admit | `curl -sSL <S086 URL> \| sha256sum` → `76e5db1d…ac4ae`; `sed -n 74,75p` | agree | sha256 equals; `:74` holds the quoted placeholder sentence; `:75` holds the 34-character rule (Gate note). It explains h09's placeholder; the REA refusal itself is from the envelope, as disclosed |
| S085 canonical list (same commit) | admit | `curl -sSL <S085 URL> \| sha256sum` → `5572beb5…78b3e2` | agree | equal to the Gate row and to the lane copy |
| S087 4byte.directory server source | reject (not made a row) | `git show 242b0d8b:corpus/SOURCES.md \| grep -E '^\| S087 \|'` → no row | agree | never opened, so no quote or hash exists to admit; keeping it as an unopened lead is the right call |

New `corpus/SOURCES.md` row re-opened: S084. Its quote is two consecutive served lines, `signatureItem.filtered =` / `signatureItem.name !== expectedCanonical.signature;` (5 words, ≤25), located at `:47-48` in the bytes I fetched. S086's located quote is about 20 words of `:74`, also ≤25 and contiguous.

## Trend verdicts

- **expansion: improved.** Knowledge files 110 → 112 (`git ls-tree --name-only <rev> corpus/knowledge/ | grep -c '\.md$'`), SOURCES rows 83 → 86 (`grep -cE '^\| S[0-9]{3,} \|'`), three tier-A rows re-opened above with matching hashes. The new ground (out-of-sample naming score; the code mechanism of `filtered`) is real even though neither claim is admitted.
- **quality: unprovable-but-better.** The round-25 rule's zero-error record holds on 137 named held-out rows (re-measured), and both claims' failures are disclosed rather than edited away. But C1 missed on an inadmissible frozen carrier (M28-1) and C2's held-out framing was wrong (M28-4, M28-5): the gain is not provable from this round.
- **discernment: unprovable-but-better.** All four sampled gate decisions agree on re-opening; the lane's own wave found its C2 pre-registration weakness before filing. Still one round, self-found, and the r27 routed defect 2 stays open.

## Routed defects (lane must fix next round)

1. The lane closed with a seat still writing: `.ufo/waves/round-28/a2w/ExecR27SelftestFix.md` modified after `242b0d8b` (19:26Z timestamps). Next round: commit or discard that seat's final report deliberately, and do not file while any seat is live.
2. Round-27 routed defect 2 is still open: the r27 selftest stays `FAIL correct-stub`, exit 1. The seat's sandbox diff exists; apply and re-run it, with a receipt.
3. Freeze a new held-out C1 only on a hex-screened carrier list (`tools/round-28/hex-screen.py` before the freeze; QUALITY row 43).
4. A real held-out test of the `filtered` rule needs selectors frozen before any lookup, and at least one predicted-false and one predicted-true unseen entry (QUALITY row 44; `preseen-overlap.py` must exit 0 at freeze).
5. The round-24 freeze gate reads only `claims.json`; make it audit every `claims*.json` (C2 was checked by hand; confirmed unchanged here by `git diff --quiet`).
6. Both round-28 counters accept any new Gate row on the entry's `source:` line; require the claim-specific row named in the claims file.

Operator note: the four SHONEN boxes are `[~]` with concrete pointers; this session did not judge them fully checkable, and promotion stays operator-owned.
