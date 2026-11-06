# Round 100 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Lane-round: kaidoku round 100. Base `6371c88633f6ce6692eaeff17e256b80ad21ece0` → lane HEAD
`7aeba805f43061a274e9bedfbdf2b625b97ebb77`. Report `.ufo/reports/round-100/kaidoku.md` (fleet repo).
Driver digest (copied from the mutable `.ufo/watchdog.log`, lines 2944 and 2953):
`2026-11-05T19:38:33-03:00 launch kaidoku round=100 pgid=1163466 driver=hyaku-inline attempt=1`;
`2026-11-05T21:49:33-03:00 complete kaidoku round=100; hyaku-inline attempt=1`.
This closure session ran every measurement below on 2026-11-05. It did not execute any lane gate: the
C1 battery `tools/round-100/pe-upx-corrupt-battery.py` and the C2 counter
`tools/round-100/registry-selftest-truth.py` were not run. It ran one held-out probe of its own
(§2, C1). That probe called the lane's repair *candidates* (round 99 and round 100) and `upx`
directly, in a scratch directory it deleted afterwards.

## 1. Conformance (PROTOCOL §Round-robin closure step 1)

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-100/kaidoku.md` (fleet repo) | `kaidoku-shokunin <kaidoku@shokunin.local> 9110c0ffb2f4e23491128c67da79e8610395ebef 2026-11-05 21:46:25 -0300`; the final lane commit is at 21:40:13 -0300, so the report was filed after its commits | pass |
| SHONEN heading | `awk '/^## SHONEN/…' report \| wc -l`; `grep -cE '^\s*- \[[ x~]\]' SHONEN.md` | 4 lines, 4 boxes, all `[~]` | pass |
| cited commits exist and are ancestors of `refs/heads/main` | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> refs/heads/main` over base + 8 cited hashes | all 9 `ok`; `git log 6371c886..refs/heads/main` lists exactly the 8 cited commits, all authored by `kaidoku-shokunin` | pass |
| pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …`; `git status --porcelain`; `git ls-remote origin refs/heads/main` | `ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `7aeba805…` | pass |
| prompt carries template contract | `diff <(sed -n 1,140p .ufo/prompts/kaidoku-round-100.md) kimi-shokunin/templates/round-prompt.md` | 10 hunks, every one a placeholder substitution (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); hyaku addendum §6 follows at line 141; prompt committed `02e3cdba` (19:38:31 -0300, before launch) | pass |
| marker? | — | real report with 8 checkable commits | not a marker |

Conformance defects: none found.

## 2. Claims (re-measured vs evidence-verified)

### R100-C1 — coverage (frontier → core; capability)

Evidence-verified (lane gate, PROTOCOL §Gate standard, Closure consequence):
- The counter has not changed since the freeze. `git diff --stat 8e24c29a 7aeba805 -- tools/round-100/pe-upx-corrupt-battery.py tools/round-100/registry-selftest-truth.py tools/round-100/forgeries plans/round-100-claims.md` prints nothing. `git show <rev>:tools/round-100/pe-upx-corrupt-battery.py | sha256sum` gives `8f148d33…` at both `8e24c29a` and `7aeba805`, which equals `counter_sha256` in every C1 receipt.
- The repair is pinned. `sha256` of `tools/round-100/upx-pe-repair.py` is `15ada0b0…` at both `a610671d` and `7aeba805`, which equals `repair_sha256` in the three after-receipts.
- Before (`jq -r '[.exit,.label]' .ufo/waves/round-100/pre/c1-*-at-freeze.json`): the round-99 repair scores `corrupt 0 of 40`, exit 1. h0–h6 all exit 1. h4 scores `corrupt 20 of 40; … exec 0 of 1`, h5 `corrupt 0 of 40`, and h6 is full except `exec 0 of 1`. Every value matches the report.
- After (`.ufo/waves/round-100/l1/scores/c1-at-{a610671d,b0a7bb8c,9a054c17}.json`): each receipt has `exit 0` and the label `recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of 20; truncated 40 of 40; corrupt 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; exec 1 of 1; effective 119 of 119`, which matches the report. Each receipt's `rev` matches its filename.

Re-measured by this session (held-out probe, plain python + upx):
- Carrier: `/opt/ghidra/docs/GhidraClass/ExerciseFiles/VersionTracking/WallaceSrc.exe`. It is not one of the battery's ten pinned `CARRIERS`.
- Packed with `upx --best -q -f` (upx 5.2.0): 33792 → 10752 bytes, win32/pe. One PackHeader was found at offset 992 with `c_len` 8113, and `zlib.adler32` of the `c_len` bytes after it equals `c_adler`.
- I made two flips at intact length: the middle byte and the last byte of the compressed data, each XOR `0x01`.

| input | `upx -t` | round-99 repair | round-100 repair |
|---|---|---|---|
| flip mid | rc 1, `Exception: checksum error` | rc 0, `ok intact` | rc 2, `refused: checksum: adler32 of compressed data 3895b758 != c_adler 28bcb757`, no `--out` written |
| flip last | rc 1, `Exception: checksum error` | rc 0, `ok intact` | rc 2, `refused: checksum: … 28bbb756 != c_adler 28bcb757`, no `--out` written |
| intact pack | — | — | rc 0, `ok intact`, output written |

The before → after (exit-0 false green → `checksum` refusal) reproduces outside the pinned population, and the intact pack does not trigger an over-refusal.

Rule re-opened:
- https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.cpp has 13236 bytes and sha256 `41b4a51b…f37a`, and is byte-identical (`cmp`) to the committed copy `.ufo/waves/round-100/pre/s327-packhead-v5.2.0.cpp`.
- Lines 334-338 hold `if (verify_checksum) { unsigned adler = upx_adler32(raw_bytes(in, ph.c_len), ph.c_len, ph.saved_c_adler); if (adler != ph.c_adler) throwChecksumError();`.
- The repair implements this check at lines 149-155 (`zlib.adler32(bytes(b[cs:cs + c_len])) != c_adler` → `Refuse("checksum: …")`).

Named limits (lane-reported, not re-measured): the CriticC1 pristine-cache and ReviewerCounter F6 filename-keyed forgeries both meet the full label, and MutationC1 found the compressed-data bound branch unreached. The rule's substance is confirmed above, so these limits bound the counter, not the claim.

Verdict: **coverage improved**. Re-measured on a held-out carrier and evidence-verified on the frozen battery.

### R100-C2 — calibration (registry self-test counts vs what the tools print)

Evidence-verified (lane counter, pinned `counter_sha256` `496a4979…` = `sha256` of the committed tool at `7aeba805`):
- Base receipt `.ufo/waves/round-100/pre/c2-do-nothing-at-base.json`: `rows 93; claimed 93 of 93; green 93 of 93; counted 93 of 93; agree 86 of 93; mismatches 7`, exit 1.
- Forgery controls F-drop, F-dup and F-tool: each `mismatches 7`, exit 1.
- After receipts at `cbd224ef`, `b0a7bb8c` and `9a054c17`: `agree 93 of 93; mismatches 0`, exit 0.

Re-measured by this session:
- `jq '.mismatches'` on the base receipt names 7 tools: round-46 `attest.py`, round-47 `record.py`, round-71 `packed-elf.py`, round-71 `seam-probe.py`, round-76 `plan-command.py`, round-76 `record-audit.py` and round-89 `upx-field-value-repair.py`.
- `jq -r '.rows[]|select(.agree|not)|[.path,.claimed,.counted]'` gives claimed → counted pairs of 15→18, 9→10, 31→32, 7→9, 3→7, 17→18 and 16→22.
- `git diff -U0 cbd224ef^ cbd224ef -- SKILL.md`: that commit touches only `SKILL.md`, with 7 rows removed and 7 added (`grep -c '^[-+]|'` = 7 / 7). The added rows carry exactly the counted values for the same seven tools, and each keeps a "this cell said …" trace of its old figure.
- Independent static counts over committed source, without running any tool:
  - `tools/round-71/seam-probe.py` `selftest()` (lines 595-633) assigns 9 `cases[...]` keys. The row now says 9; at base it said 7.
  - `tools/round-76/plan-command.py`: each of the 7 `case_names` printed in the receipt tail occurs in the source. The row now says 7; at base it said 3.

Named limits (lane-reported): CriticC2 L1–L7 (edit classes outside the first stated count) and ExecReproC2 F1–F5 (out-of-population rows, including two round-82 self-tests that exit 1 silently).

Verdict: **calibration improved**. Re-measured by diff, receipt rows and static case counts; the counter is evidence-verified.

### Harm check (no owned axis harmed)

- `git diff 6371c886 7aeba805 -- SCORECARD.md` replaces only the `coverage` head row. It now cites the round-100 re-derivation, keeps the round-99 text as "Previous:", and states recipe A as 142/184 = 7.72. The diff also appends the round-100 capability row and the round-100 section. No earlier claim row is edited.
- Knowledge files: `git ls-tree --name-only <rev> corpus/knowledge/ | grep -c '\.md$'` gives 183 at base and 184 at HEAD. The new entry stem occurs 3 times in `corpus/README.md`.
- Coverage receipts `stem`: 183/183 with mismatches 0 at `6371c886`, and 184/184 with mismatches 0 at `b0a7bb8c` and `9a054c17`.
- Depth: `recipe_a.citation_resolved_rules` is 36 and `depth_score` 10.0 at all three revisions.

| axis | verdict | basis |
|---|---|---|
| coverage | improved | C1: held-out re-measure + frozen receipts; map 184/184 |
| calibration | improved | C2: registry mismatches 7 → 0, re-derived by diff and static counts |
| depth | unchanged | 36 resolved rule blocks, 10.0 at base and HEAD |

## 3. Discernment spot-check (LEARNING.md §Discernment is checked from outside)

Sample from `corpus/lessons/round-100.md` `## Gate`:

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S327 UPX 5.2.0 `src/packhead.cpp` | admit (tier A) | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.cpp, fetched 2026-11-05: 13236 bytes, sha256 `41b4a51b…f37a`, `cmp`-identical to the committed copy | agree | Lines 336-338 carry the quoted `upx_adler32(…) … if (adler != ph.c_adler) throwChecksumError();` verbatim (12 words, ≤25). This is the packer's own refusal of altered compressed data, and the held-out probe confirms `upx -t` behaves that way |
| S328 UPX 5.2.0 `src/check/dt_check.cpp` | admit (tier A) | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/check/dt_check.cpp: sha256 `83f97d79…74fe`, matching the row | agree | Line 1154 is `assert_noexcept(upx_adler32(d, 4) == 0x09f003f7);`, and line 1145 is `d = dd + 7`. Run here, `zlib.adler32(bytes([0xff,0xfe,0xfd,0xfc]))` = `0x9f003f7` and seed 0 gives `0x9ec03f6`, which matches lines 1154-1155. The row grounds the repair's use of `zlib.adler32` |
| `src/compress/compress_zlib.cpp` 231-235 | reject (no row) | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/compress/compress_zlib.cpp (9730 bytes) plus `src/compress/compress.cpp` (7331 bytes) | agree | Line 231 is `#if 0 // UNUSED` around `upx_zlib_adler32`. In `compress.cpp`, `upx_adler32` takes the `#if 1` branch `return upx_ucl_adler32(...)` at line 40. Admitting the zlib wrapper would misattribute the live arithmetic, so the rejection is correct |

SOURCES row check: `corpus/SOURCES.md` row S327 (new, line 243). Its URL, byte count and sha256 all match my fetch, and its located quote (12 words) occurs verbatim at the cited lines.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` exits 0 and prints `kaidoku ok` with 34 W04 lines, which matches the report. One of them is `S327 duplicate url …/v5.2.0/src/packhead.cpp across scopes`, the declared scope split from S308. Row count via `grep -cE '^ {0,3}\| *S[0-9]{3,}' corpus/SOURCES.md` is 231 at base and 233 at HEAD. The only removed rows in the diff are S324 and S326, rewritten for the `used-by` widening.

## 4. Trend verdicts

- **expansion: improved.** "Payload corruption at intact length" moves into Core for PE. The knowledge count goes 183 → 184, mapped 184/184. There are two new tier-A packer-source rows (S327, S328), both re-opened here.
- **quality: improved.** The round-99 repair's exit-0 false green on altered compressed data is closed. This session reproduced it on a carrier outside the pinned set (`ok intact` → `checksum` refusal, no over-refusal on the intact pack). The battery's `exec` leg turns the h4/h6 aliased-exec forgeries red (frozen receipts).
- **discernment: improved.** The lane found seven of its own false registry counts by running the tools rather than reading the rows. I confirmed two of them by static count. The non-author sample above agrees on 2 admits and 1 reject.

## 5. Routed defects (lane fixes next round)

1. The C1 battery admits two forgeries with exit 0: the CriticC1 pristine-cache forgery and the ReviewerCounter F6 filename-keyed forgery. Its compressed-data bound branch is also unreached (MutationC1). Commit them as red fixtures before the next C1-family freeze. The plan's item (a) already names this; the fix must land.
2. C2 counter limits L1–L7 (CriticC2): word-form counts, second-count tokens, documented argv/exit text, and text outside the markers.
3. Five out-of-population registry defects (ExecReproC2 F1–F5), including two round-82 self-tests that exit 1 silently. Registry rows must not state green for them.
4. Round-97 routed defects 2–5 and 7 are still open (report, round-99 spot-check defect 6). Carry them on the queue.
5. Location wording: the report cites S327 as lines 334-338 (the function block), while SOURCES and the lesson cite 336-338 (the quote). Both are true. Cite the quote lines consistently.

Operator note (promotion is operator-owned): SHONEN box 2 (an end-to-end task in `LOG.md`) and box 3 (executable instructions) look checkable by a non-author. This session executed the round-100 repair from the committed bytes and the entry's rule alone, on a held-out carrier, without oral context.
