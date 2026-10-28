# C2FleetSweep — round-48 fleet report citation sweep

**Verdict: the closure's 15/16 holds. One cited full hash does not resolve. Three further defects are not in the closure: `7fe11332` is absent from the LOG lines it is grouped with; two uncited commits (`e1cce19a`, `b7590749`) authored that LOG block; `corpus/QUALITY.md` row 79 is a pre-existing different rule. A fourth, smaller defect: bare `ctl-c2-0-do-nothing.json` matches 7 committed paths.**

Sweep target: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-48/kaidoku.md` (10649 bytes, 87 lines, sha256 `a6895609b910ec8f4511f0783f18f7151c86934bf04495018a503a1e5749914b`). Resolved only against lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` at `8847042a140b044dbf335210c965bf7b06b09b4f`. Current HEAD at sweep was `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`; `git merge-base --is-ancestor 8847042a140b044dbf335210c965bf7b06b09b4f HEAD` exited 0. No tools installed.

Receipts: `.ufo/waves/round-49/w1/C2FleetSweep/commands.jsonl` (batch UTC `2026-10-28T21:16:01Z`–`21:16:02Z`), `quality.diff`. Empty stdout/stderr sha256 is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. `git cat-file -t <commit>` stdout `commit\n` sha256 `50836eee574ecff79dea3b4fd40673d7d000f7a5f177d8a6a3000b59c78383b8`.

Closure criterion re-run, against the pinned rev rather than today's `refs/heads/main`: `git cat-file -e <hash>^{commit}` and `git merge-base --is-ancestor <hash> 8847042a140b044dbf335210c965bf7b06b09b4f`. Distinct full hashes in the report: **16** (28 occurrences). **15** are commits and ancestors (both exits 0). **1** is missing (both exits 128). Count **15/16 confirmed**.

## 40-hex hashes

| citation | report lines | cat-file -t / -e ^{commit} | ancestor exit | resolves? | note |
|---|---|---|---|---|---|
| `2e785632863f043a985f7953775b6aca191f1169` | 9, 22 | 0 / 0 | 0 | yes | subject: land instrument moves. Parent `165d45d1e27740c2adc789f939fe51ebf4690cd7`. |
| `33f65a913cfd21a4491a4f8b7ccc8f00069f058d` | 9, 24, 30, 34, 35 | 0 / 0 | 0 | yes | subject: bind final-freeze do-nothing and v2 controls. Parent `b75907496a17df1a865a5abbd070a474a0615126` (not A8). |
| `0d76deedd7ce9dd17c510494c33b7b00c3282554` | 13, 26 | 0 / 0 | 0 | yes | subject: inherited seat evidence. `diff-tree --name-only` is 212 files under round-45 (8), round-46 (158), round-47 (46). "Three wave directories" matches. |
| `663f30ee7516942a0120e7de68fe88356e680822` | 13, 26 | 128 / 128 | 128 | **no** | stderr `fatal: Not a valid object name …^{commit}` sha256 `6a21c62ed8518398f404652fe18682aa7cf5300dfc4a0c2bfa2d5fc8d4421652`. `cat-file -t` stderr sha256 `93051ef5e7bf1424b70ed514d3f012953c936894eec9c3018251c6cfb674dd83`. Closure-named. |
| `7fe11332781356ec3d5b0b314698de27dd25b50d` | 21 | 0 / 0 | 0 | yes as object; **no as LOG citation** | Initial freeze, parent of A1 (`61b87d742032e65fca9c38267d7d6ed7e555edad` → this → `dc73587a`). Not an A-number. See further defect 1. |
| `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` | 21 | 0 / 0 | 0 | yes | A1. 8-char form is on LOG.md:3439. |
| `ac02a79ff84133220d01ce3b59a4789b7004dbc5` | 21 | 0 / 0 | 0 | yes | A2. On LOG.md:3439. |
| `f3a7afc42c1da2457ab0ffd1883c5bdb822f2962` | 21 | 0 / 0 | 0 | yes | A3. On LOG.md:3439. |
| `0f06251bf6a3a6964c715f67243d4df12e854258` | 21 | 0 / 0 | 0 | yes | A4. On LOG.md:3439. Parent of `0d76deed`. |
| `04f9d4b7698deb9bff04380e781ae5090ea9bb76` | 21 | 0 / 0 | 0 | yes | A5. Parent is the real `663f30ee751694fb…`, so A5 is not a child of A4. |
| `24b4e5cbe22e1eafd93d3a5a1706ec381c77f563` | 21 | 0 / 0 | 0 | yes | A6. On LOG.md:3439. |
| `c8d7da5539157bf719fa29aa71d8a540fb5c136b` | 21 | 0 / 0 | 0 | yes | A7. On LOG.md:3439. |
| `b6f7ca2a6391964dfdedd477cd560bd42159873a` | 21, 30, 34, 35 | 0 / 0 | 0 | yes | A8. Full hash is on LOG.md:3439. |
| `c093e798106eba7e5372f63108ec32748bdc115f` | 23 | 0 / 0 | 0 | yes | Named on LOG.md:3440, 3441, and 3445. |
| `577a02a52b68b02d33374e8a3f9a913a257fee7d` | 25 | 0 / 0 | 0 | yes as object; **no as a LOG name** | Closure-named: not in LOG.md. It did author LOG.md:3440, 3441, 3444, 3446 (blame). |
| `8847042a140b044dbf335210c965bf7b06b09b4f` | 25, 30, 87 | 0 / 0 | 0 | yes as object; **no as a LOG name** | Closure-named: not in LOG.md. Authored none of LOG.md:3436–3449. |

Corrected object, not cited: `663f30ee751694fb0970e7de68fe88356e680822` type commit, `cat-file -e ^{commit}` exit 0, ancestor exit 0. Subject: `round-48: the one inherited receipt above 1 MiB, named as a file`. Parent `0d76deed…`. Sole path in `diff-tree`: `.ufo/waves/round-47/w1/SentFixtures/receipts/trace2-c2-baseline.json`. `git cat-file -s <rev>:<that path>` exit 0, stdout `2382654\n`, stdout sha256 `18c00eecb7f284d4fe0df00e39be77ea0d4d989fdd00054c6372152cd6946e1b`. Among 534 commits from `git rev-list 8847042a…` (stdout sha256 `b6a0e619412b4ff73a2fa548d180ddc084461a139805e843ccf6c3e67f844c6b`), prefix `663f30ee` matches only this commit. The cited hash swaps `fb0970` for `2a0120`. LOG.md:3449 contains the 8-char prefix, not the dead full hash (`git grep -F` of the dead hash exit 1, empty stdout sha256 `e3b0c442…`; grep of `663f30ee` exit 0, stdout sha256 `4a63a95979fe4532c9db1a104425b2d58ecb575493c7541d1feb03ba11953fab`).

8-hex commit tokens, each `git rev-parse --verify <pref>^{commit}` exit 0 and exactly one hit in `rev-list` of the pin: `165d45d1` → `165d45d1e27740c2adc789f939fe51ebf4690cd7`; `2e785632`, `33f65a91`, `dc73587a` → the full hashes above. All four resolve. Not a defect.

## LOG.md line pointers

`git show 8847042a…:LOG.md` is 3449 lines, so every cited number is inside the file. `git blame -L 3436,3449 --porcelain 8847042a… -- LOG.md` exit 0, stdout sha256 `c552cbcb0f2e5807aebfd4688705642e01719f875f9ed144d2ddf42a05d67f6a`. Authors of those lines: `e1cce19a` (3436–3439, 3442–3443, 3445, 3447), `577a02a5` (3440–3441, 3444, 3446), `b7590749` (3448–3449).

| citation | report line | resolves? | note |
|---|---|---|---|
| `LOG.md:3436-3439` | 21 | partial | A1–A8 short hashes and the full A8 hash are on line 3439. `7fe11332` is not in the range and not in the file (`git grep -F 7fe11332 <rev> -- LOG.md` exit 1). Lines authored by uncited `e1cce19a`, not by the nine listed commits. |
| `LOG.md:3442-3444` | 22 | **no** | Closure-named. `2e785632` is a commit label on 3440, 3441, and 3445, not inside 3442–3444. 3442–3443 authored by `e1cce19a`; 3444 by `577a02a5`. |
| `LOG.md:3440-3441` | 23 | yes | `c093e798` is named here (also on 3445). Lines authored by `577a02a5`, which names `c093e798`; it does not mean `c093e798` wrote the line. |
| `LOG.md:3439` | 24 | **no** | Closure-named. Line 3439 is the A1–A8 freeze list. `33f65a91` is a commit label on 3440 and 3441. On 3444 the same 8 hexes occur only inside filename `c2-final-33f65a91.json`. |
| `LOG.md:3446-3449` | 25 | **no** | Closure-named for the names: `git grep -F 577a02a5` and `8847042a` each exit 1. Range is three authors: 3446 `577a02a5`, 3447 `e1cce19a`, 3448–3449 `b7590749`. `8847042a` authored none of it. Line 3449 names different commits (`0d76deed`, `663f30ee`). |
| `LOG.md:3449` | 26 | yes for the 8-char prefixes | `0d76deed` and `663f30ee` are on the line. The second prefix is the real commit, not the dead full hash in the report cell. Line authored by uncited `b7590749`. |

`git log --first-parent --format='%H %s' 61b87d742032e65fca9c38267d7d6ed7e555edad..8847042a…` lists 19 commits. Two of them appear nowhere in the fleet report: `e1cce19a54cce5dc55b6e21d6a769242cec1ebc4` (`log claims, sources, mistakes and routed limits; retain final counter receipts`) and `b75907496a17df1a865a5abbd070a474a0615126` (`log the inherited late seat-write custody`). Those are the commits that wrote the LOG block the table points at.

## sha256

Both cited digests are 64-hex. Command shape: `git cat-file blob 8847042a…:<path>`, then sha256 of those bytes and of those bytes with one trailing `\n` removed. Both blobs end with one `\n`. Neither JSON contains a timestamp field. `git grep -F 2026-10-28T19:33 8847042a… -- .ufo/waves/round-48` was not re-run in the final receipt batch; an earlier `git grep` of that pattern under `.ufo/waves/round-48` exited 1. The closure's "C2 timestamp is four seconds later" claim is **not run** against git bytes (blobs have no timestamp). Not confirmed and not contradicted here.

| citation | line | blob | raw sha256 | strip-one-nl | resolves? |
|---|---|---|---|---|---|
| `3cc2d72d8f6564545a7d9f32c86a4d3a81bf5367f8b55bdb15075e60401e8f77` | 34 | `.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json` (2589 bytes) | `6320c5d240e4822d1612c2cb929b383ca6f628953f032c7c92253e53d8ced86e` | equals the citation | yes only with the newline removed. Closure-named. `met_target` true, `rev` is `33f65a91…`, `failing` `[]`. |
| `c30628ae7c439754f570476d570ed57db3361c1a3b5178ecb1c97f065c1e1ce8` | 35 | `.ufo/waves/round-48/l1/scores/c2-final-33f65a91.json` (2710 bytes) | `d1bb87d883ebfc25210d10073f00e98edf7e83c8a21417e4dc62a0bc28a23914` | equals the citation | same. Closure-named. `met_target` true, `rev` is `33f65a91…`, `failing` `[]`. |

`git cat-file -e 33f65a913cfd21a4491a4f8b7ccc8f00069f058d:<each final receipt>` exited 128; the same path at `8847042a…` exited 0. The report already says the receipts are committed at `8847042a…`. Not an extra defect.

## File paths

Literal `git cat-file -e 8847042a…:<path>` exit 0 (resolves): `SKILL.md`, `SCORECARD.md`, `LOG.md`, `SHONEN.md`, `PROVINCE.md`, `plans/round-48-claims.md`, `corpus/SOURCES.md`, `corpus/lessons/round-48.md`, `corpus/QUALITY.md`, `tools/round-48/meanings.py`, `tools/round-48/record2.py`, `.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json`, `.ufo/waves/round-48/l1/scores/c2-final-33f65a91.json`, `.ufo/waves/round-48/l1/scores/c2-at-165d45d1.json`, `.ufo/waves/round-48/r48-w1-results.json`, `.ufo/waves/round-48/controls/ctl-c1-0-do-nothing.json`. `git ls-tree -d 8847042a… tools/round-48` exit 0, tree `cc31ac997b67999d6eb4903b325483534a9dc8a7`. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` is `git rev-parse --show-toplevel`. Absolute `…/corpus/SOURCES.md` is that file.

Unique suffix, literal path absent (resolves by unique basename): `ctl-c2-1-v2-profile.json`, `ctl-c2-a1-before.json`, `controls/ctl-c2-a1-before.json`, `l1/scores/c2-final-33f65a91.json`, `c1-final-33f65a91.json`, `c2-at-165d45d1.json`, all under `.ufo/waves/round-48/`. `ctl-c2-a1-before.json` has `"axis_score_cells": {}`, matching the report's claim for that file.

**Does not uniquely resolve:** `ctl-c2-0-do-nothing.json` (report line 35) matches 7 blobs: round-36, round-38, round-43 `controls/c2/`, round-45, round-46, round-47, and `.ufo/waves/round-48/controls/ctl-c2-0-do-nothing.json`. Further defect 4.

`considerthese/` as a directory is absent. Paths that contain the letters are files under `.ufo/waves/round-44/w2/artifacts/R44W2Assim/considerthese-*`, not a `considerthese/` directory. The report's "absent" claim resolves. S145 and S146 are rows at `corpus/SOURCES.md` lines 151 and 152, not file paths. Their locator/rationale errors are closure defects 2 and 3; existence resolves. `refs/heads/main` is a ref, not a tree path. `.scratch/` is not a lane tree path.

`c2-at-165d45d1.json`: `met_target` false, `rev` `165d45d1e27740c2adc789f939fe51ebf4690cd7`, `freeze` `b6f7ca2a…`, `failing` `["the round-47 atom oracle does not accept the card (mismatches 2)"]`. The string `<REV>` is not in the file. The two mismatch atoms are absent paths `.ufo/waves/round-48/l1/scores/c1-at-` and `c2-at-`. Sibling `c1-at-165d45d1.json` has `met_target` true and `failing` `[]`, which matches the report's "C1 exit 0" half. The `<REV>` gloss is not stored in the cited receipt; the absent-path half is, on those truncated paths. Not scored as a clean falsification.

Wave file the report cites, `.ufo/waves/round-48/r48-w1-results.json`: `seats` is integer 75; `results` length 75. Role counts match the report exactly (executor 22, scribe 16, reviewer 9, scout 9, critic 6, mutation-tester 6, connector 2, revenger 2, simplifier 2, sentinel 1; reviewer+critic+mutation-tester = 21). Report artifacts, counted as `w1/<name>.md` or any `w1/<name>/**/*.md`: **72 present, 3 absent**. Absent: `C1Meaning` (only `receipt.json`), `C1Battery` (no path), `ScribeReportNumbers` (no path). `ExecGateRun` is present as `w1/ExecGateRun/ExecGateRun.md` and is inside the 72. `C1Battery-2` is not a `results[].name`; its only path is `w1/C1Battery-2/receipt.json`. This confirms closure defect 7 (report says 73 and names `C1Battery-2`). Not a further count defect.

The report bytes contain no `cross-domain` (closure-named omission). Not re-listed as new.

## Further defects the closure did not name

1. **`7fe11332781356ec3d5b0b314698de27dd25b50d` is in the A1–A8 cell and in `LOG.md:3436-3439`, and it is not in LOG.md.** `git grep -n -F 7fe11332 8847042a… -- LOG.md` exit 1, empty stdout sha256 `e3b0c442…`, UTC `2026-10-28T21:16:01Z`. The closure listed `577a02a5` and `8847042a` as unnamed and did not list this hash. It is the pre-A1 freeze commit, parent `61b87d74…`, subject `round-48: freeze — the meaning-bound registry counter and the record floor counter`. Line 3439 names A1–A8 only. The nine-hash cell is one commit wider than the series the LOG line describes.

2. **The LOG lines the table cites were written by two commits the report never cites.** `e1cce19a54cce5dc55b6e21d6a769242cec1ebc4` wrote 3436–3439 (the freeze paragraph the table assigns to the A-series), 3442–3443, 3445 (the "Landed commits" line that names `2e785632` and `c093e798`), and 3447. `b75907496a17df1a865a5abbd070a474a0615126` wrote 3448–3449 (the inherited-custody line the table assigns to `0d76deed` and the dead hash) and is the parent of `33f65a91`. Blame command and stdout sha256 are above. The closure's string test did not name these authors.

3. **`corpus/QUALITY.md` row 79 does not resolve to the round-48 rule the report says it added.** `git diff -U0 61b87d742032e65fca9c38267d7d6ed7e555edad 8847042a… -- corpus/QUALITY.md` exit 0, stdout sha256 `3be2b1c6f83ea5a68c948156bec042dbf2cdd98ff5ed878ff0d038e9b57f00d1`, 1082 bytes, UTC `2026-10-28T21:16:02Z`. The only addition is a prose bullet titled "Row 79 added after round 48" about the score-cell parser. Table row 79, line 87, is unchanged and is a different rule: the bytes of the first freeze commit, checked with `tools/round-38/freeze-drift.py`. The report's "added QUALITY row 79" (line 12) and LOG.md:3444's "QUALITY row 79 records the rule" point at the old table row, not at a new numbered row.

4. **`ctl-c2-0-do-nothing.json` on report line 35 does not uniquely resolve** (7 committed paths, listed above). The round-48 blob exists; the citation does not pick it. `ctl-c2-1-v2-profile.json` beside it is unique.

Closure defects confirmed and not repeated as new: dead hash `663f30ee7516942a…`; both stdout sha256s match the receipt only after stripping one trailing newline (raw `6320c5d2…` and `d1bb87d8…`, the same raw digests the closure printed); LOG string misses for `2e785632` (not in 3442–3444), `33f65a91` (not on 3439), `577a02a5` and `8847042a` (absent from LOG.md); wave report artifacts 72/75 with missing seats `C1Meaning`, `C1Battery`, `ScribeReportNumbers`, and `C1Battery-2` not a seat; no cross-domain sentence. C2 receipt timestamp: **not run** from git.
