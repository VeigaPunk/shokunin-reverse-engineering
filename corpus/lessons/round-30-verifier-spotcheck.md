# kaidoku round 30: verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Session `HyakuCloseKaidoku30`, 2026-10-23, about 03:18Z to 03:35Z. Range `d210fb8fa62d2af04d009cfa0c65a4e8137dc742..328ca4f4b1ed4b73dc47fceaf8d127ad31d0ddab`. Report `.ufo/reports/round-30/kaidoku.md` (fleet `bd693c83c2cceca49013ad8c8a18c32d7089f6db`). This session dispatched five read-only seats: `ReMeasureC1`, `ReMeasureC2`, `GateEvidence` and `AxisFitReview` (reviewers), plus `CriticAxisFit` (critic). The critic died at spawn with the same `429 … RESOURCE_EXHAUSTED` (gemini-4-argon-high) that killed the lane's three after-data critics, so `AxisFitReview`, a reviewer, replaced it. No seat executed a lane counter, gate, selftest or REA. Everything else below was run by this session. Nothing was installed or updated. Item hold `U064N008Hf47eb933` was not touched.

Driver digest (copied from `.ufo/watchdog.log:800,814`):

```
2026-10-22T23:14:13-03:00 launch kaidoku round=30 pgid=2538305 driver=hyaku-inline attempt=1
2026-10-23T00:23:06-03:00 complete kaidoku round=30; hyaku-inline attempt=1
```

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by the lane | `git log --format='%an %H' -- .ufo/reports/round-30/kaidoku.md` (fleet) | `kaidoku-shokunin bd693c83c2cceca49013ad8c8a18c32d7089f6db` (00:22:46-03) | pass |
| SHONEN heading, one line per box | read of the report `## SHONEN` | 4 lines, all `[~]`, each with a pointer | pass |
| cited commits on the branch | `git rev-parse --verify <h>^{commit}` and `git merge-base --is-ancestor <h> main` for `d210fb8f 0dbabf78 4ee65c67 a6e7d9ce 004053d6 f39f4530 24da3459 92b1dd2d 3502b94c 39fbad9d 328ca4f4` | all 11 ok. `git log --oneline d210fb8f..328ca4f4 \| wc -l` gives 10, all `kaidoku-shokunin` | pass |
| pushed | `scripts/hyaku/jj-lane.sh state <lane>` | `branch=main local=328ca4f4… remote=328ca4f4… ahead=0 behind=0 head=detached tracked=0 untracked=0` | pass |
| leftovers | `git status --porcelain \| wc -l` | 0 | pass |
| prompt carries the template contract | `grep -nE '^## ' .ufo/prompts/kaidoku-round-30.md` | §1 MISSION/AXES, §2 Claims, §2b Frontier, §3 L2 floor, §4 Report contract, §5 Commit/push, §6 hyaku addendum; committed by the lane at fleet `62d48b8` (23:14:11-03, before launch) | pass |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | `kaidoku ok`, seven W04 (S033, S047, S054, S062, S069, S083, S090), exit 0 | pass, equal to the report (S090 is the new W04 with S083) |

Gate receipts the report states but did not commit (conformance defects, status-neutral; neither claim rests on these gates):
- The report says "`settle-gate` PASS" at the tip and that `settle.tsv` "returns `settle: PASS`". `git ls-tree -r --name-only 328ca4f4 .ufo/waves/round-30 | grep -i settle` lists only `settle.tsv`, `w1/ExecSettleGate.md` and `w2/MutSettleGate.md`. `git grep 'settle: PASS' 328ca4f4` hits only selftest fixtures and round-28 runs inside those two seat reports. No round-30 settle-gate run is committed.
- The report says `prefile: PASS` "rerun after committing the tip receipts". The only committed run, `after/prefile-check.txt`, ends `prefile: FAIL prefile_exit=1` (`tree NOT CLEAN (3 paths)`, the tip receipts themselves; GateEvidence F11). No green run is committed.

## Freeze and the carrier-rewrite incident

GateEvidence checked these read-only, with its own `sha256sum` and `git` commands:
- **Freeze.** All 6 pinned paths in `claims.json` hash to their pinned values at `0dbabf78`, `4ee65c67` and `328ca4f4`. `git log 4ee65c67..328ca4f4 -- <6 paths>` gives 0 commits.
- **Order.** Instruments `0dbabf78` 02:34:24Z, then the freeze `4ee65c67` 02:35:13Z, then control receipts `f39f4530` 02:59:22Z. The first C1 run in `runs.tsv` is at 02:59:33Z, the first C2 run at 03:00:36Z, and data commit `24da3459` at 03:04:20Z. All 72 counted evidence files are first added at `24da3459` and touched by no other commit.
- **Incident M30-2 is confirmed and contained.** Seat `RevOracleVsReadobj` ran `llvm-objcopy --dump-section` with no output file, which rewrote 4 carriers between 02:42:35Z and 02:43:47Z.
  - Four control seats' first counter runs exited 2 on the altered bytes, each with `PIN carrier … absent or altered`: CtlC1AllFalse 02:42:59, CtlC1DoNothing 02:43:03, CtlC1NoReader 02:43:31 and CtlC1JunkRow 02:43:46. All four reports were added at `004053d6`, before the data.
  - The restored files carry 02:44:00Z mtimes, and reruns pass the input pin from 02:44:44Z. That is about 15 minutes before the first counted run.
  - The carriers were never committed: they live in `/fast/scratch/hyaku/kaidoku-r30/carriers/`, and only `carriers.tsv` is pinned in git. The four tampered hashes (`d661be8b…`, `9f41e2d4…`, `c07fe610…`, `bde137eb…`) have 0 `git grep` hits under `corpus/evidence` or `tools` at every round commit.
  - Today all 16 on-disk carriers equal their pinned sha256 and carry `chattr +i`. All 16 equal the members of the cached official wheels, and all 7 wheels equal their digests in the committed PyPI JSON (S091).
  - Every C1 envelope's `subject.digest.sha256` equals its pinned value (16/16) at both `24da3459` and `328ca4f4`.
- One timing detail is inconsistent: `w1/RevOracleVsReadobj.md:15` gives the restore as "~02:46Z", but the mtimes and the 02:44:44Z passing reruns bound it at or before 02:44:44Z.

## Per-claim re-check

Both counters are lane-owned gates (PROTOCOL §Gate standard), so this session did not execute them. It verified their committed evidence and re-measured the counted quantities from committed bytes, plus the pinned on-disk carriers, with independent code.

Committed gate evidence:
- Selftests (`before/` at `a6e7d9ce`, `after/` at `3502b94c`): C1 25 cases and 0 failures; C2 16 cases and 0 failures; both exit 0.
- Counter receipts:
  - At `d210fb8f` both exit 2.
  - At `24da3459` C1 exits 0. C2 exits 1 with `skill_ok=0` (M30-4, receipt kept).
  - At `92b1dd2d` and `39fbad9d` both exit 0. `328ca4f4` adds only the three receipt files over `39fbad9d` (`git diff --name-status`).
- Other gates: `axis-fit-gate` exits 0 before the data and at `24da3459`. `prefreeze-gate` at `24da3459` gives `pins=6 mismatch=0 data_before_freeze=0 verdict=CLEAN`. Registry rows for all three new gates are at `SKILL.md:1003-1005`.

### R30-C1 (coverage): re-measured, verifies, axis fit

- Independent decode (ReMeasureC1, `/tmp/hyaku-c1-remeasure/remeasure.py`). It uses its own ELF/PE/Mach-O section parser and `zlib`, not the lane oracle. For each carrier it compares the frozen sha256 and size, `ok`, operation, subject sha, package list in index order, edges, root index, `file_offset`, `compressed_bytes`, `section_bytes`, `uncompressed_bytes` and `format_version`. Result: `agreement=16/16`.
  - Package counts are 584, 584 and 580 for the three ELF builds, 596 for both PE and 573 for both Mach-O.
  - `llvm-readobj --sections` gives the same offsets on one carrier per format.
  - The carriers hold 5 distinct package lists and 7 distinct dependency documents, as the corrected entry states.
- Base: `git show d210fb8f:PROVINCE.md | grep -c inspect-rust-binary` gives 0, and 3 at the tip. At the base, every `auditable_metadata` envelope value in the lane is `null`: 12 envelope values; the 7 non-null hits are `$ref` schema listings. Base knowledge `l7-02:10` says "Untested: non-ELF inputs".
- Tip: `PROVINCE.md:330-338` has a Core-addition row that names the verb and the entry. The entry `corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` cites S089, S090 and S091 and names all 16 evidence ids.
- Discrimination: the counter's `pass` requires a live exit-0 run on the carrier's frozen sha256 with exactly one non-null `auditable_metadata` whose tuples, offset and size match the oracle. Pre-data controls scored 0, 0, 0, 0 and 1 of 16 (`controls/receipts-detail.tsv`, committed at `f39f4530` before the data).
- **Axis ruling, which the lane's dead after-data critics left open: fit.**
  - AXES.md defines coverage as the governed fraction of real surfaces. A previously ungoverned input class, a non-null `.dep-v0` graph on ELF, PE and thin Mach-O, enters PROVINCE Core from 0 mentions under a bar that can fail and that no trivial control met.
  - This is the move the round-29 ruling asked for (routed defect 1), not a re-score of held ground.
  - The width is narrow, and the lane discloses it: one producer (uv 0.13.0), one REA pin, and an oracle that shares the format spec (S089) but not code.
- Low findings:
  - `province_ok` and `entry_ok` are token checks; the junk-row control passed both. The lane discloses this as "doc gates are token checks".
  - `committed_check` compares the committed record on evidence id and package multiset only. The independent decode matched offset and size anyway.
- Verdict: **verifies** (coverage `improved`).

### R30-C2 (depth): re-measured, verifies, axis fit

- Freeze: `git log -- corpus/evidence/round-30/c2/predictions.tsv` lists only `0dbabf78` (02:34:24Z). `git diff --stat 0dbabf78 328ca4f4 -- …/predictions.tsv` is empty. Its sha256 `6852df3a…` is pinned in `claims.json`. The first C2 run is at 03:00:36Z.
- Full-envelope comparison (ReMeasureC2, `/tmp/r30c2_cmp2.py`, own code): `full_envelope_matches 19 / 19`.
  - The 3 accept rows match on `ok:true`, artifact sha256 and size.
  - All 16 refusal rows match on `ok:false`, exit 1, operation, error code and the exact reader string `Selected artifact <path>: <predicted message>`. The string sits in `invalid_request` `details.issues[0]` (13 rows), in `unsupported_target` `details.reason` (1), or in `resource_constraint` `details.reason` (2, with `maximum_bytes` 1048576 and 896576 = 14,009 × 64).
- The SKILL table (`SKILL.md:970-993`) has 19 rows in prediction order. Message, outcome and code all equal the predictions and the observations (`skill_rows_positional_equal 19 /19`). The refusals entry cites S090.
- Source: all 16 refusal messages appear in the 6.5.0 reader at `~/.npm/_npx/ad9a3fdbcad992c6`. Its `package.json` sha equals the one in `runs.tsv`, and `RustAuditableReader.js` is `1f3748c9…`, equal to S090 and to my own tarball extraction below.
- Base: none of seven sampled table messages appears in base `SKILL.md`, `PROVINCE.md` or knowledge (AxisFitReview).
- Disclosed weakness M30-3 is real in the counter but not material to this result.
  - `committed_agrees` (`c2-rust-refusals.py:246-255`) compares only `ok` for refusals. The copied-predictions control therefore scored 16.
  - The match itself needs live REA output that contains the predicted message (`judge`, `:205`).
  - The committed refusal bytes carry the predicted message and code 16/16, checked independently. The weakness is in the check, not in the data.
- **Axis ruling: fit.** Exact error codes, messages and thresholds were predicted from opened code (S090) before the data and observed live. Trivial predictors scored 0 of 19, so the bar can fail.
- Low findings:
  - Four prediction code pointers are wrong. `r-two-roots` gives 151-153 but the string is at 302; `r-index-outside` gives 154-157 (306); `r-inflate-ratio` gives 128-129 (139); `r-not-zlib` gives 131-134 (143).
  - `claims.json` lists the "1 MiB compressed / 64x inflate ratio" limits as gained, but base `l7-02:10` already held "1 MiB section, min(8 MiB, 64× section)". What is new for those two limits is the observed messages and codes. The refusals entry does not cite `l7-02`.
  - The table holds 16 refusals plus 3 accepts, with 13 distinct messages; the shared-message pairs are disclosed.
- Verdict: **verifies** (depth `improved`).

### Separability, lowest axis, harm

- **Separable.** C2's counter reads one C1 path, `corpus/evidence/round-30/c1/carriers.tsv` (`:49`). That is a frozen input from `0dbabf78`, not a C1 result. The C1 counter has 0 references to `round-30/c2` or `predictions`.
- **Lowest axis.** At the base, the owned axes are coverage, depth and calibration, all at 10, with none retired (`SCORECARD.md:19-27`). With that tie, both claims satisfy the rule. Neither the round-30 section nor the report states it (a calibration recording gap).
- **Harm.** `git diff --numstat d210fb8f 328ca4f4 | awk '$2>0'` gives exactly one line: `1 1 SHONEN.md`, the disclosed pointer refresh `PROVINCE.md:95-116` → `97-118`. Overall the diff is 197 files, `+16524 -1`. `SCORECARD.md` gains 37 lines and loses none, all in a new round-30 section; the owned-axes table is byte-identical. No owned axis is harmed.

| axis | verdict | reason |
|---|---|---|
| coverage | improved | C1: a new positive input class enters Core; 16/16 re-derived independently; controls ≤1/16 |
| depth | improved | C2: 19/19 full-envelope matches re-derived; code-predicted before data; controls 0/19 |
| calibration | unchanged | not claimed; limits disclosed, but the report asserts settle/prefile PASS without committed runs, and the lowest-axis basis is unstated |
| operability | unchanged | not claimed; three new gates with selftests and registry rows (hygiene) |
| freshness | unchanged | not claimed |
| adjacency | unchanged | not claimed; SHONEN pointer refresh only |

Admission: both claims verify and no axis is harmed, so `admitted=true`. Unlike round 29, no control met either target before the data, and each target is reachable only by live REA output that agrees with an independent oracle or with frozen predictions.

## Discernment spot-check

All re-opens were run by this session at 03:25Z on 2026-10-23, with `curl -sSL <url> | sha256sum`, `tar xzf`, `sed -n` and `git ls-remote`.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S089 cargo-auditable README, PARSING.md and schema @ `e2316a67` | admit | the three pinned raw URLs; `sed -n 95p README.md` | agree | sha256 `ccca48d9…`, `39e35b88…` and `c6ac9399…` equal the Gate row. `:95` reads "The JSON is Zlib-compressed and placed in a linker section named `.dep-v0`." (13 words). `git ls-remote` HEAD is `e2316a67` |
| S090 rea-agents 6.5.0 tarball | admit | `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`; `sed -n 7p package/dist/rust/RustAuditableReader.js` | agree | Tarball `531717a0…e699` and reader `1f3748c9…` equal the row. `:7` is `export const RUST_SECTION_BYTES = 1024 * 1024;` |
| S091 PyPI uv 0.13.0 JSON | admit | `https://pypi.org/pypi/uv/0.13.0/json` | agree | sha256 `2eaed6c8…b4c` equals the row. The quoted `"filename":"uv-0.13.0-py3-none-macosx_10_12_x86_64.whl"` occurs once. `.urls` has 19 files |
| second row for the master copy of the cargo-auditable docs | reject (not made) | the same three files at `…/cargo-auditable/master/` | agree | Master bytes are identical to the pinned commit (master = HEAD = `e2316a67`), so a row would duplicate S089 |
| S090 anchor `cli.js` | reject (corrected to `dist/cli-runtime/cli.js`) | `wc -l package/dist/cli.js package/dist/cli-runtime/cli.js`; `sed -n 5218p` | agree | `dist/cli.js` has 120 lines and cannot hold `:5176-5218`. `cli-runtime/cli.js:5218` reads `}, "Dependency section exceeds the 1 MiB compressed limit");` |
| S091 draft kind `registry` | reject (changed to `dataset`) | `scripts/sources-census.sh:655` | agree | The kind enum `spec\|docs\|paper\|code\|tool\|dataset\|talk\|book\|community\|own-work` has no `registry`, so E05 is correct |

New `corpus/SOURCES.md` rows re-opened: S089, S090 and S091 (`SOURCES.md:95-97` at `328ca4f4`). All three quotes in the lesson Gate are served bytes at the stated location and within 25 words. No existing row was changed (`git diff d210fb8f 328ca4f4 -- corpus/SOURCES.md` has only 3 `+|` lines).

## Trend verdicts

- **expansion: improved.**
  - A new input class (the `inspect-rust-binary` positive class on 3 containers and 3 ISAs) entered PROVINCE Core from 0 mentions, re-derived 16/16.
  - SOURCES rows went 88 → 91 (`grep -cE '^\| S[0-9]{3,} \|'` at both revisions). Knowledge `.md` files went 114 → 116; `git ls-tree` gives 115 → 117 because it also counts `.gitkeep`.
  - All three new rows re-opened with matching hashes.
- **quality: improved.**
  - The new SKILL decision table equals live behaviour 19/19 on full envelopes, beyond the counter's own `ok`-only committed check.
  - Wave-2 corrections (7 dependency documents, 3 ISAs in 7 pairs, the S090 anchor) re-check against committed bytes.
  - Round-29 routed defects 1–6 are closed (GateEvidence). Defect 7 stays open, as disclosed.
  - Residual weaknesses: M30-3, token-only doc gates, four wrong code pointers, and the "64× / 1 MiB gained" overclaim.
- **discernment: improved.**
  - All six sampled gate decisions agree on re-opening.
  - This time the lane's axis labels match the outside ruling, where round 29 did not. The round-29 misfit was mined into M30-1, QUALITY row 48 and `axis-fit-gate.py`, which exits 1 on round 29 and 0 on round 30.
  - The pre-data controls caught the M30-3 weakness before any data, and the lane disclosed it instead of hiding it.
  - The two uncommitted gate-PASS statements keep calibration from moving.

## Routed defects (lane must fix next round)

1. The report asserts `settle-gate` PASS at the tip and `prefile: PASS` on a rerun, but neither run is committed. The only committed prefile run is red. Commit the receipts of the runs a report cites, or cite only committed runs (§Evidence standard, "Claimed ≠ re-executed").
2. M30-3 is still open: `committed_agrees` (`c2-rust-refusals.py:246-255`) binds refusal records by `ok` only. The next C2-family counter must compare the full refusal envelope (code plus message), and show that it fails on the copied-predictions control.
3. Four prediction code pointers in `predictions.tsv` are wrong: `r-two-roots` 151-153 → 302, `r-index-outside` 154-157 → 306, `r-inflate-ratio` 128-129 → 139 and `r-not-zlib` 131-134 → 143 (`RustAuditableReader.js` 6.5.0). The frozen file stays as it is; append a correction in the refusals entry or the lesson.
4. `claims.json` presents the 1 MiB / 64× limits as gained, but base `corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md:10` already held "1 MiB section, min(8 MiB, 64× section) inflated JSON" as tool bounds. Append a correction that the new content is the observed messages and codes, and have the refusals entry cite `l7-02`.
5. The lowest-axis basis is unstated (coverage, depth and calibration are all tied at 10). State it in the round's SCORECARD section, and refresh or annotate the stale owned-axes rows: coverage still cites 109/109 at `ebe2cb4a`, while the round measured 116/116.
6. `province_ok` and `entry_ok` are token checks that the junk-row control passes. A future Core-admission counter should check placement under `## Core` (or the round's Core-addition table), not only co-occurrence.
7. `w1/RevOracleVsReadobj.md:15` says the restore happened "~02:46Z", but the evidence bounds it at or before 02:44:44Z. Append a correction in the lesson's M30-2 row if it is cited again.
8. Carried from round 29: the `c1-fresh-naming.py` docstring still names round-28 paths.

Operator note: all four SHONEN boxes are `[~]` with concrete pointers. This session independently checked the box-1 decision table: `SKILL.md:970-993` equals the live observations 19/19. A non-author could reasonably check that box. The executable-instructions box still rests on author-dispatched re-runs, and this session did not execute the counters. Promotion stays operator-owned.
