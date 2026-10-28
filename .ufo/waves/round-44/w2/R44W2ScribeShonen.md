# R44W2ScribeShonen — SHONEN checklist pointer verification (round 44, wave 2)

**Seat** R44W2ScribeShonen (scribe) · **Fleet** `kaidoku` · **Lane** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
**Backbone** base `c29360e3` · freeze `c48f8a4b` · admissible measured revision `55bcce69` · lane tip at dispatch `c86ea508` · **lane tip measured here `8bb1090a`** (the round's final commit: "round-44: land lesson, LOG/SCORECARD/QUALITY record, frozen-path preflight, and wave-2 spec").
**Wrote only** `.ufo/waves/round-44/w2/R44W2ScribeShonen.md` and `.ufo/waves/round-44/w2/artifacts/R44W2ScribeShonen/**`, plus scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2ScribeShonen/` (deleted, §9). No claim, counter, rubric, frozen byte or production doc was edited; no mutating `git`/`jj` command was run; no tool was installed (`pacman` untouched).

## 0. Verdict in one paragraph

Every file, range and hash pointer in all four SHONEN boxes resolves — **no pointer is broken**. Two pointers/claims are stale or contradicted at the tip: box 1's `SKILL.md:81-449` describes the craft section only at its pin `e1c83313` (at the tip the craft section is `SKILL.md:81-543`), and `SHONEN.md` was not touched by round 44 at all (same blob at base, freeze, REV and tip), so the checklist carries no round-44 line although round 44 ran an end-to-end REA task, landed its receipts and got a LOG entry. Box 3's promotion claim ("Instructions executable by an agent without oral context") is contradicted by the round it certifies: the frozen R44-C1 predicate and its own counter require contradictory `parameters.output_directory` values (R44-CL2), so no agent following the frozen text can produce a met receipt. Box 4 resolves cleanly and its boundary claim still holds. Separately, the lane's own **command A** exits **1** with **5 assertion mismatches** at the measured revision — including the three statements C2 says it repaired — and **no round-44 document states that** (finding D3).

## 1. Method

Read `plans/round-44-claims.md`, `corpus/lessons/round-44.md`, and `SHONEN.md` (18 lines, 4 boxes, blob `afeee543…` at every revision from base to tip). For each box's `asserted:` text, every pointer was resolved at the tip `8bb1090a`:

- **path** → `test -e` (and directory listing where the pointer names a set);
- **range** → `sed -n '<a>,<b>p' | wc -l` for existence, plus an anchor check (`grep -n` for the marker/text the pointer claims to be in that range) because a range can exist while the cited text has moved;
- **hash** → `git cat-file -t` for commits, `git rev-parse <rev>:<file>` for blobs, and a recomputed sha256 over the extracted byte region for the table-region hash;
- **claim truth** → re-ran the lane's command A (`tools/round-38/c2-counter.py`, the executable mirror SCORECARD cites) at six revisions, the frozen C2 counter at the measured revision and the tip, and the M44-2 preflight red/green pair; read the committed C1/C2 receipts rather than re-running C1 (§8).

All commands were read-only. Full machine receipts (seat, exact command, exit code, stdout sha256, wall ms) are in §7 and in `artifacts/R44W2ScribeShonen/receipts.json`; the resolution data is in `artifacts/R44W2ScribeShonen/pointer-resolution.json`.

### Record-revision note (worktree drift during this run)

At measurement time `HEAD` was `8bb1090a`, but the worktree carried **uncommitted L1 edits** to `LOG.md`, `SCORECARD.md` and `corpus/lessons/round-44.md` (`git status --porcelain` → ` M` on all three; the attempt-2 record revision, which among other things rewords M44-2 to name the fleet orchestrator's non-author lane sweep that committed `c86ea508` at 10:43:43). `SHONEN.md`, `SKILL.md`, `PROVINCE.md` and every other file this report names as a pointer target were **clean at `HEAD`** (identical blob/diff), so all pointer resolutions are against committed bytes.

Where this report cites `LOG.md`, `SCORECARD.md` or the lesson it gives the **committed `8bb1090a` line**: lesson `R44-CL1` :54-56 and `R44-CL2` :57-62, `M44-2` row :16; `LOG.md` round-44 heading :3198 (round-43 :3184, round-42 :3174); `SCORECARD.md` correction text :3511, markers :3512-3517, round-44 heading :3519, owned-scores line :3528, M44-2 paragraph :3530. The worktree variants shift the lesson (`R44-CL1` :62, `R44-CL2` :69) and replace the same LOG/SCORECARD lines in place (line counts unchanged). The L1 should re-pin these line numbers after the record edit is committed; no pointer or claim conclusion in this report depends on the worktree variant.

## 2. The four-row table

Legend — **[x]**: every cited pointer resolves at the tip *and* the cited claim holds there. **[~]**: pointers resolve only at their pin, or the claim is stale/contradicted at the tip. **[ ]**: a pointer fails to resolve, or the claim is false at its own pin.

| box | pointer(s) cited | resolves? | verdict | reason |
|---|---|---|---|---|
| **1** — `SHONEN.md:5` "SKILL.md contains real decision tables…" | `SKILL.md:81-449`; `e1c83313`; `SKILL.md:387-449`; `4d62ee5a`; `SKILL.md:348-375`; `52b0eb29`; `SKILL.md:316-343`; `eb8215ac`; `77d196c6`; v4 region sha256 `92540586…` | 9/10 at the tip; `SKILL.md:81-449` is the craft section **only** at `e1c83313` | **[~]** | The rule-block claim is true (20/20 at `e1c83313`; 21/21 at the freeze tree — both recomputed), the v4 region hash reproduces byte-for-byte at the tip, every commit/blob resolves, and the v3/v2/v1 markers still fall inside their cited ranges. But the craft-range pointer is stale against the tip (`81-543`), the box has no round-44 line, and command A's R2 check reds exactly that pointer at the measured revision (D2). |
| **2** — `SHONEN.md:8` "At least one end-to-end domain task executed and logged in LOG.md" | `corpus/evidence/round-42/c1/`; LOG round-42 entry; `eb8215ac`; `e9a24d07`; `.ufo/waves/round-41/w2/R41W2Repro*.md`; `corpus/evidence/round-40/c1/`; `.ufo/waves/round-40/w2/R40W2Repro*.md`; `corpus/evidence/round-39/c1/K{1..6}/`; `6fdaf4f1`; `corpus/lessons/round-39.md`; `tools/round-43/c1-counter.py`; LOG round-43 entry | 12/12 at the tip (receipt dirs 4/4/4/6 carriers; 2 + 3 repro files; LOG.md:3174 and :3184) | **[~]** | The claim is true and every pointer resolves, but the asserted text stops at round 43. Round 44's own end-to-end run exists and is uncited: receipts `corpus/evidence/round-44/c1/{v1le,v1be,v2le,v2be}`, `carriers_matched 4`, `met_target false`, `LOG.md:3198`, lesson line 1. The checklist is one round behind the task it certifies. |
| **3** — `SHONEN.md:11` "Instructions executable by an agent without oral context" | `.ufo/waves/round-40/w2/R40W2C2IndepEval.md`; `tools/round-39/sqfs-triage.py`; `tools/round-39/c2-counter.py`; `.ufo/waves/round-39/w2/R39W2C2Shortcut.md`; round-43 `CTL-C1-2`/`CTL-C1-4` | 6/6 files resolve; selftests re-run green (35/35, 45/45); `26/26` and `20/20` appear in the cited documents | **[~]** | All pointers resolve, but the claim is falsified for round 44: `corpus/lessons/round-44.md:57-62` (at `8bb1090a`) records that the frozen R44-C1 text and its frozen counter require contradictory `parameters.output_directory` values, so an agent reading only the frozen instructions cannot produce a met receipt without oral adjudication (D5). |
| **4** — `SHONEN.md:14` "No cross-domain bleed (PROVINCE.md still accurate)" | `PROVINCE.md:97-125`, `:116-118`, `:119-125`, `:157`, `:376`, `:378-384`, `:386-394`; "byte-identical at `52b0eb29`" | 8/8 at the tip; range bytes sha256 `f1a5cfc6…` at both `52b0eb29` and the tip; base PROVINCE bytes are an exact prefix of the tip (`e385f119…`, 53354 of 54780 B) | **[x]** | Every line number still lands on the text the box says it does (Adjacent at :97, safety refusal :116-118, tooling bullet :119-125, round-39 heading/row/note :378/:382/:384, round-40 block :386-394, dated round-39 pointers at :157 and :376). Round 44 appended only at `PROVINCE.md:424-430` (`## Round-44 measured, not promoted`), which is append-only and is not a Core row, so "no cross-domain bleed" holds. |

## 3. Per-box detail

### Box 1 — `SHONEN.md:5`

| pointer | kind | tip | pin | resolves |
|---|---|---|---|---|
| `SKILL.md:81-449` | range | exists (SKILL.md = 1572 lines); line 81 = `## Queue-drain craft (rounds 5-12, distilled in round 13)`; the craft section now ends at 543 | at `e1c83313` the craft section is exactly 81-449 (command A `observed.craft_range [81,449]`) | pin-only |
| `e1c83313f33a3d97edbd8fef402db2d06172fcdc` | commit | `cat-file -t` = commit | — | yes |
| `SKILL.md:387-449` (block 20, table v3) | range | exists; v3 marker at line 440 (inside) | block 20 starts line 387; v3 marker at 434 | yes |
| `4d62ee5a86b4692a13f682b29ed7975e8d7e5326` | commit | commit | — | yes |
| `SKILL.md:348-375` (table v2) | range | exists; v2 marker at 371 (inside) | v2 marker at 361 | yes |
| `52b0eb2907c704ed5f184c47b14c723208e5cbbc` | commit | commit | — | yes |
| `SKILL.md:316-343` (table v1) | range | exists; v1 marker at 339 (inside) | v1 marker at 333 | yes |
| `eb8215ac` | commit | commit; `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json` = `matched 78`, `n 78`, `met_target false`, `exit_code 1` — i.e. "matched its evaluator 78/78" is accurate and the claim itself stopped | — | yes |
| `77d196c6` | commit | commit; `.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json` = `met_target true`, `exit_code 0` | — | yes |
| v4 table region sha256 `92540586…` | hash | 13 856 B, `92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2` at WORKTREE, `c29360e3`, `c48f8a4b`, `55bcce69`, `8bb1090a`, `d1681696`, `eb8215ac`; absent at `e1c83313` (round 42 added the table) | — | yes |

Rule-block claim: command A at `e1c83313` = `resolved_rules 20 / rule_blocks 20` (the box's 20/20); at `4d62ee5a` 19/19; at `52b0eb29` 18/18; at `c48f8a4b`/`55bcce69`/`8bb1090a` 21/21. The v4 table shape claim (13 columns, 15 rules) recomputes: 13 header cells, 15 data rows.

Caveat on the three pinned table ranges: at the tip each range still *contains* its marker (`v3` 440∈387-449, `v2` 371∈348-375, `v1` 339∈316-343), but the block boundaries themselves moved as later rounds inserted text above them (round 42 added block 21, shifting the v1 marker 333→339, v2 361→371, v3 434→440). The pin (`e1c83313`/`4d62ee5a`/`52b0eb29`) is therefore the only correct reference for those three ranges; at the tip they are approximate windows, not the blocks the box describes.

### Box 2 — `SHONEN.md:8`

| pointer | resolves | observed |
|---|---|---|
| `corpus/evidence/round-42/c1/` | yes | 4 carrier dirs: `DW-FONERA`, `DW-MEGA`, `OW-A8092`, `OW-X86FS` |
| LOG round-42 entry | yes | `LOG.md:3174` — `## Round 42 — 2026-10-26 (KaidokuR42)` |
| `eb8215ac` | yes | commit; R42-C1 receipt exists under the same scores dir |
| `e9a24d07` | yes | commit; `corpus/evidence/round-41/c1/` has `L3`, `L4`, `V3`, `V4` |
| `.ufo/waves/round-41/w2/R41W2Repro*.md` | yes | 2 files (`R41W2ReproL.md`, `R41W2ReproV3.md`) |
| `corpus/evidence/round-40/c1/` | yes | 4 carrier dirs `L1`,`L2`,`V1`,`V2` |
| `.ufo/waves/round-40/w2/R40W2Repro*.md` | yes | 3 files |
| `corpus/evidence/round-39/c1/K{1..6}/` | yes | all six exist |
| `6fdaf4f1` | yes | commit; `.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json` = `carriers_matched 6`, `met_target true` |
| `corpus/lessons/round-39.md` | yes | 13 458 B |
| `tools/round-43/c1-counter.py` | yes | 195 574 B |
| LOG round-43 entry | yes | `LOG.md:3184` |
| **round 44 (not cited)** | — | `corpus/evidence/round-44/c1/{v1le,v1be,v2le,v2be}` exist; `LOG.md:3198`; lesson line 1 — the end-to-end task the box certifies is missing from its text |

### Box 3 — `SHONEN.md:11`

| pointer | resolves | observed |
|---|---|---|
| `.ufo/waves/round-40/w2/R40W2C2IndepEval.md` | yes | 21 201 B; 12 matches for `26/26`/`26 of 26` |
| `tools/round-39/sqfs-triage.py` | yes | `--selftest` re-run: `SELFTEST cases=35 pass=35 fail=0`, exit 0 |
| `tools/round-39/c2-counter.py` | yes | 36 517 B (not re-run; its `--selftest` is claimed separately by the box's "27/27") |
| `.ufo/waves/round-39/w2/R39W2C2Shortcut.md` | yes | 16 139 B; 10 matches for `20/20`/`20 of 20` |
| round-43 `CTL-C1-2`, `CTL-C1-4` | yes | `.ufo/waves/round-43/controls/c1/receipts/CTL-C1-2.json`, `…CTL-C1-4.json` |
| **claim** "instructions executable…" | **contradicted for round 44** | `corpus/lessons/round-44.md:57-62` (at `8bb1090a`): the controls amendment demands `parameters.output_directory` = a committed `corpus/evidence/round-44/c1/` path, the predicate and counter demand `/kaidoku-r44/`; every receipt this round is the scratch form (`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/.../rea-out`), and the counter rejects the committed form |

### Box 4 — `SHONEN.md:14`

| pointer | resolves | observed |
|---|---|---|
| `PROVINCE.md:97-125` | yes | 29 lines; `## Adjacent` starts at 97 |
| `PROVINCE.md:116-118` | yes | the quality/safety verdict refusal bullet |
| `PROVINCE.md:119-125` | yes | the dated-2026-10-26 tooling bullet |
| "byte-identical at `52b0eb29`" for :97-125 | yes | sha256 `f1a5cfc61851ca3411b462b54d4d0681397aecc6431738a30a968a48138c78b4` at `52b0eb29` and at the tip |
| `PROVINCE.md:378-384` | yes | heading 378, table row 382, round-39 frontier note 384 |
| `PROVINCE.md:386-394` | yes | heading 386 … round-40 frontier note 394 |
| `PROVINCE.md:157`, `:376` | yes | both carry the dated `Round 39:` pointer |
| round-44 append | yes | `PROVINCE.md:424-430` = `## Round-44 measured, not promoted (R44-C1 honest stop)` + note; base PROVINCE (422 lines, 53 354 B) is an exact byte prefix of the tip (430 lines, 54 780 B), both sha256 `e385f119…` |

Round-44 note: the new section says "measured 4/4 but not promoted" and the frontier note keeps `squashfs_v2_nonstandard`, v3/v4 Broadcom, gzip v3, LE AVM (`hsqs`), AVM kernels and nested sub-images Frontier. That is the correct boundary outcome of a C1 stop and adds no Core row, so box 4's claim is not harmed.

## 4. Stale pointers and what they should cite

| # | pointer (path:line) | how it is stale | should cite |
|---|---|---|---|
| 1 | `SHONEN.md:5` — `SKILL.md:81-449` "craft section" | true only at its pin `e1c83313`; at `8bb1090a` the `## Queue-drain craft` section spans **81-543** (last non-blank line 543; line 547 opens `## Config custody…`). command A: `R2 SHONEN box1 craft range observed [81,543] stated [81,449]`. | Keep `81-449` explicitly as the `e1c83313` pin, and add a current line: "craft section `SKILL.md:81-543`; command A at `c48f8a4b` = 21/21 rule blocks" (the value SCORECARD.md:3511 already records). |
| 2 | `SHONEN.md:8` — end-to-end evidence list | no broken pointer, but the newest instance is round 43; round 44's run is omitted. | Add: "2026-10-28 round 44 — REA 6.5.0 `extract-firmware` on the four committed v1/v2 fixtures, receipts `corpus/evidence/round-44/c1/{v1le,v1be,v2le,v2be}`, counter `carriers_matched 4`, `met_target false` (measured, not promoted); `LOG.md:3198`; `corpus/lessons/round-44.md`." |
| 3 | `SHONEN.md:11` — executable-instruction evidence | pointers resolve, but round 44 is a counterexample to the claim. | Add the counterexample (R44-CL2, lesson :57-62 at `8bb1090a`) and the currently executable set: `tools/round-44/c2-rubric.json` + `tools/round-44/c2-counter.py` (80/80, 0 mismatches, exit 0 at `55bcce69`). |
| 4 | `SHONEN.md:14` — boundary pointer set | no stale pointer; the checklist simply has no round-44 boundary line. | Optional: "Round 44 appends `## Round-44 measured, not promoted (R44-C1 honest stop)` at `PROVINCE.md:424-430`; Adjacent unchanged." |

No pointer should be *deleted*: each historical pin remains true at its own revision (`e1c83313`, `4d62ee5a`, `52b0eb29`), which is exactly how the frozen C2 rubric dispositions them (`C2-b4…b8`).

## 5. Findings (numbered; each is for L1 to act on)

### D1 — SHONEN.md was never touched by round 44, so the checklist has no round-44 line
- **Path:** `SHONEN.md:5`, `:8`, `:11`, `:14` (all four boxes).
- **Command:** `for r in c29360e3 c48f8a4b 55bcce69 8bb1090a; do printf '%s ' $r; git rev-parse $r:SHONEN.md; done` (receipt `log-and-shonen`) and `git log --oneline c29360e3..8bb1090a -- SHONEN.md` (receipt `shonen-history`).
- **Exit:** 0. **Observed:** the blob is `afeee543775114804328065150379642799b4e60` at base, freeze, measured revision and tip — byte-identical, and `git log c29360e3..8bb1090a -- SHONEN.md` is empty.
- **Why it matters:** round 44 executed the end-to-end domain task (`corpus/evidence/round-44/c1/`, `LOG.md:3198`) and landed a met C2 claim, yet the promotion checklist that the C2 rubric reads still ends at round 43. Consistency with prior rounds (each of which added a dated line to boxes 1-4) is broken.
- **Action:** append a dated round-44 line to boxes 1, 2 and 3 (and optionally 4), or state explicitly in the round record that SHONEN is deliberately held.

### D2 — Stale craft-range pointer in box 1 (`SHONEN.md:5`)
- **Path:** `SHONEN.md:5`; `SKILL.md:81-449` vs the tip's `81-543`.
- **Command:** `python3 -I -B tools/round-38/c2-counter.py --root . --rev 8bb1090a --base c29360e3` (receipt `commandA-8bb1090a`).
- **Exit:** 1. **Observed:** `{"check": "R2 SHONEN box1 craft range", "observed": [81, 543], "stated": [81, 449]}` (also at `55bcce69`: same mismatch, exit 1; at `c48f8a4b`: same, exit 1). Direct read: `sed -n '81p;543p' SKILL.md` = `## Queue-drain craft…` … last table row; `sed -n '547p'` = `## Config custody for live-probe rounds (SOP)`.
- **Action:** see §4 row 1. The repair itself is a one-line clarification (81-543 plus a pin qualifier), but the frozen C2 claim's landing scope forbids rewriting frozen text — so it belongs to the L1's post-round-44 record repair, not to this wave.

### D3 — Command A is red at the measured revision, and the round record never says so
- **Path:** `corpus/lessons/round-44.md:1` (headline "three self-assessment mismatches repaired and scored 80/80"), `LOG.md:3198` (same headline), `SCORECARD.md:3519` (same headline), `SCORECARD.md:3528` (mentions command A only for its observed values), `SCORECARD.md:3511-3517` (the append-only `<!-- c2-correction: … -->` blocks).
- **Command:** `python3 -I -B tools/round-38/c2-counter.py --root . --rev 55bcce69 --base c29360e3` (receipt `commandA-55bcce69`).
- **Exit:** 1. **Observed** (`met_target false`, `mismatches 5`):
  - `O1 coverage mapped/files` observed `[138,138]` vs stated `[133,133]`
  - `O2 depth resolved/rules` observed `[21,21]` vs stated `[20,20]`
  - `O4 SHONEN box1 rule blocks` observed `[21,21]` vs stated `[20,20]`
  - `R1 depth row craft range` observed `[81,543]` vs stated `[387,449]`
  - `R2 SHONEN box1 craft range` observed `[81,543]` vs stated `[81,449]`
- **Disclosure check:** `grep -c 'command A' corpus/lessons/round-44.md` → 0; the LOG.md round-44 block (`3198-3205`) → 0. The frozen C2 counter is green at the same revision (`entries_evaluated 80`, `mismatches []`, exit 0 — receipt `c2-counter-55bcce69`), because it evaluates pinned/append semantics, while command A reads the row text.
- **Honest scope of this finding:** command A is red at *every* revision tested (`e1c83313`, `4d62ee5a`, `52b0eb29`, `c48f8a4b`, `55bcce69`, `8bb1090a` — all exit 1 with the same five-check structure). It is a one-round-lag detector, not new breakage; the round's numbers are not wrong. The defect is that a headline claiming the statements were "repaired" is not visible to the lane's own command A, and the round record contains no sentence saying command A still exits 1 at REV.
- **Action:** add one sentence to the round-44 record ("command A at `55bcce69` still exits 1 with these five mismatches because the repairs are append-only correction blocks") or name the C2 semantics that supersede command A. Do not touch the frozen claim.

### D4 — The M44-2 fix is a detector, not a gate (and is not yet wired)
- **Path:** `tools/round-45/frozen-path-preflight.py` (4 008 B); `corpus/lessons/round-44.md:54-56` at `8bb1090a` (R44-CL1 "wire it into the round's commit sequence"); `.git/hooks/` (only `*.sample` files, no `pre-commit`).
- **Commands / exits / observed:**
  - `python3 -I -B tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4b --rev c86ea508 --pathspec tools/round-44/` → **exit 1**, `touched 8`, `blob_changed 8`, verdict `frozen_path_changed` (matches M44-2 and the committed `.ufo/waves/round-44/l1/preflight-c86ea508.json`).
  - same at `--rev 55bcce69` → **exit 0**, `touched []`, verdict `clean` (55bcce69 is the last admissible revision — confirmed).
  - same at `--rev 8bb1090a` → **exit 1** (the violation is still in history; a later restore would not un-block, per the claim).
  - same at `--rev 55bcce69` **without** `--pathspec` → **exit 1**, `touched 110`, `blob_changed 0`: with no pathspec the `git log` call has no pathspec and the tree backstop is skipped, so a clean revision is reported red.
- **Why it matters:** the tool catches the admitted violation when invoked exactly right, but nothing invokes it — the only non-artifact references are documentation (`corpus/lessons/round-44.md:16`, `:54`, `LOG.md:3203`, `SCORECARD.md:3530`, `corpus/QUALITY.md:139`) and the wave-2 dispatch spec. It also cannot be wired blind: the claim's frozen set must be passed explicitly (`--pathspec tools/round-44/`), or the gate is useless.
- **Sufficiency verdict for the record:** the *record* is honest and sufficient — both counters' exit 2 at the tip are disclosed (`c1-score-at-tip.json`, `c2-score-at-tip.json`), `55bcce69` is named as the admissible revision, and a later restore is already declared not to un-block. The *fix* does not yet prevent recurrence; R44-CL1's "wire it in" remains open.
- **Semantics note (not a defect):** the walk treats every `A` under the pathspec as a change, while the frozen claim says "A is a change whenever the path existed at FREEZE". For a directory pathspec this is the stricter, correct reading ("a file added under it after the freeze is a change"); it diverges from the claim prose for an added path that did not exist at FREEZE, which no round-44 file exercised (all 8 paths are `M`).

### D5 — Box 3's claim is falsified by the round it certifies (R44-CL2)
- **Path:** `SHONEN.md:11`; `corpus/lessons/round-44.md:57-62` (at `8bb1090a`); `plans/round-44-claims.md` ("Predicate P44-C1" — the `parameters.output_directory` conjunct); `PROVINCE.md:424-430`.
- **Evidence:** the frozen C1 text requires `parameters.output_directory` to name a committed `corpus/evidence/round-44/c1/` path (controls amendment) *and* the `/kaidoku-r44/` scratch segment (predicate); the four receipts carry `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/.../rea-out`, and the counter accepts only that form. No single run satisfies the frozen prose, so "instructions executable by an agent without oral context" fails for this round by construction.
- **Action:** keep box 3 **[~]**, cite this as the standing counterexample, and let the already-routed round-45 satisfiability preflight close it.

## 6. Adjacent confirmations of the record (measured, so the L1 can rely on them)

- **C2 at the measured revision:** `python3 -I -B tools/round-44/c2-counter.py --root . --rev 55bcce69 --freeze c48f8a4b` → **exit 0**, `entries 80`, `entries_evaluated 80`, `mismatches []`, `frozen_path_changed []`, `met_target true`, `counter_sha256 == counter_sha256_at_freeze` (`085192ea…`). The committed `.ufo/waves/round-44/l1/c2-score-at-55bcce69.json` agrees. The claimed value is confirmed.
- **C2 at the tip:** same counter at `8bb1090a` → **exit 2**, `entries_evaluated 0`, 8 `frozen_path_changed` under `tools/round-44/control-fixtures/`. The committed `c2-score-at-tip.json` agrees; the round's "measure at 55bcce69, not the tip" is exactly what the instrument reports.
- **C1 at the measured revision (read, not re-run):** `.ufo/waves/round-44/l1/c1-score-at-55bcce69.json` = `carriers_matched 4`, `met_target false`, `exit_code 1`, `frozen_path_changed []`. This is consistent with the claim's honest stop; I did not re-run C1 (§8).
- **Freeze walk:** `55bcce69` green, `c86ea508` red, `8bb1090a` red — so `55bcce69` is verifiably the last admissible revision.

## 7. Receipts

Every row is a command I ran in this seat; `stdout_sha256` covers stdout+stderr. Full JSON: `artifacts/R44W2ScribeShonen/receipts.json`; captured stdout: `artifacts/R44W2ScribeShonen/<name>.out`.

| name | command | exit | stdout sha256 | wall ms |
|---|---|---|---|---|
| `cat-file-all-revs` | `for r in e1c83313f33a3d97edbd8fef402db2d06172fcdc 4d62ee5a86b4692a13f682b29ed7975e8d7e5326 52b0eb2907c704ed5f184c47b14c723208e5cbbc eb8215ac 77d196c6 e9a24d07 6fdaf4f1 55bcce69 c48f8a4b c29360e3 c86ea508 8bb1090a d1681696; do printf '%s ' $r; git cat-file -t $r; done` | 0 | `b1fd36c1c85921e74df56443f2ab53baa023d4f26fd2187bb1231e5a29d48c14` | 9 |
| `commandA-e1c83313` | `python3 -I -B tools/round-38/c2-counter.py --root . --rev e1c83313 --base c29360e3` | 1 | `d436c9087c2d2c53c0c44fa106befd6b74dede40e4a3e130a8e01312e0b230a7` | 225 |
| `commandA-4d62ee5a` | `python3 -I -B tools/round-38/c2-counter.py --root . --rev 4d62ee5a --base c29360e3` | 1 | `8491bcc5c454db0463207c7b6a9332d7356eb3abc2cd1296d4887840b6d045f2` | 216 |
| `commandA-52b0eb29` | `python3 -I -B tools/round-38/c2-counter.py --root . --rev 52b0eb29 --base c29360e3` | 1 | `ae35497c3d8f5039efa579127f13767b64c702df7332a0af231d0c2183a9a76c` | 223 |
| `commandA-c48f8a4b` | `python3 -I -B tools/round-38/c2-counter.py --root . --rev c48f8a4b --base c29360e3` | 1 | `b6a9a87da2c0c11b0bbbdb86683eefddd9387e8e0c972e72845f983ae7ff7e62` | 241 |
| `commandA-55bcce69` | `python3 -I -B tools/round-38/c2-counter.py --root . --rev 55bcce69 --base c29360e3` | 1 | `76369189ec022d0f9dddf7f7bb234cacf7a43265d66eea70fcdba18e8aaa2d37` | 240 |
| `commandA-8bb1090a` | `python3 -I -B tools/round-38/c2-counter.py --root . --rev 8bb1090a --base c29360e3` | 1 | `3395bd7c440de5113812bd82d99948a5be48d6c78417f099649a994249a9070d` | 247 |
| `c2-counter-55bcce69` | `python3 -I -B tools/round-44/c2-counter.py --root . --rev 55bcce69 --freeze c48f8a4b --work /fast/scratch/hyaku/kaidoku-r44/R44W2ScribeShonen/c2work --json-out …/c2-at-55bcce69.json` | 0 | `dd7c529bb6340c364854093937bce3d90ec980ebdea951263bb38dc52316a9b3` | 4305 |
| `c2-counter-8bb1090a` | `python3 -I -B tools/round-44/c2-counter.py --root . --rev 8bb1090a --freeze c48f8a4b --work …/c2work-tip --json-out …/c2-at-tip.json` | 2 | `0a81b8b2e85b08914b5a2f1b3856601f53d8c6f491ae5e00794c9bcf9a064c64` | 83 |
| `preflight-c86ea508` | `python3 -I -B tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4b --rev c86ea508 --pathspec tools/round-44/` | 1 | `add6bc5d944582fde00cd47b1d6a407796fd603800f53daf622b8519a9aa9039` | 88 |
| `preflight-55bcce69` | `… --rev 55bcce69 --pathspec tools/round-44/` | 0 | `7f8df9e366a40cb84eea03f418f803be85ec4327e18ee38aa8858b9be2f427b6` | 89 |
| `preflight-8bb1090a` | `… --rev 8bb1090a --pathspec tools/round-44/` | 1 | `dae13b0acb4810b6e15e35a814011964bfb52d48f979171400ab81dcd696bb15` | 93 |
| `province-prefix` | `bs=$(git show c29360e3:PROVINCE.md \| wc -c); …; git show c29360e3:PROVINCE.md \| sha256sum; head -c "$bs" PROVINCE.md \| sha256sum` | 0 | `3b3f124bddc708c319bf0df888700ba85120b29cdc72b927a946f42479c15fa5` | 5 |
| `province-ranges` | `for r in 97-125 116-118 119-125 157 376 378-384 386-394 424-430; do sed -n "${r/-/,}p" PROVINCE.md \| wc -l; done` | 0 | `c571fb45831cb9e08460da0a90987776d33dfd3466c083f6a4cf6074a2a749c2` | 5 |
| `province-97-125-52b0eb29-vs-tip` | `git show 52b0eb29:PROVINCE.md \| sed -n '97,125p' \| sha256sum; sed -n '97,125p' PROVINCE.md \| sha256sum` | 0 | `0c0ecb04813bb459a89052088cd4b7727f704e36a2b50a870b2986cea7774814` | 2 |
| `skill-anchors` | tip line count, v1-v4 marker lines, craft 81/543, 544-547 | 0 | `ab47e6f98e214bbf73ba059b69d04aab42d2195e2cad2a5a0ac3d6038910d151` | 3 |
| `skill-pin-markers` | marker lines at `e1c83313`, `4d62ee5a`, `52b0eb29` | 0 | `671f28b843ea53cb86a26613cf506924e4102320bbddcd7a09adaf26e28cdc8f` | 9 |
| `pointer-existence` | 15-path existence census + repro-file counts + `26/26`, `20/20` occurrence counts | 0 | `f5e710a06fea7db3f9f5928dcca5333b83852da16c605742c807838033b9f4bf` | 4 |
| `log-and-shonen` | LOG headings + `rev-parse <rev>:SHONEN.md` at 4 revisions + line count | 0 | `f824391f126d83af5c63c34a8dd2dfdc3ccd42eb475245ca7e33e5b3967cab79` | 5 |
| `v4-region-hash` | region extraction + sha256 at 8 revisions | 0 | `058f36394a8b8d60f5ce908e69795f98c18b83dafdd384f2d1c4cd01e44c8e61` | 27 |
| `selftest-r39-triage` | `python3 -I -B tools/round-39/sqfs-triage.py --selftest` | 0 | `235d201f191a94ee4ccfe35dc04a7656b6f8864e1b7d642081b88aa16da9e9eb` | 1311 |
| `selftest-r40-triage-v2` | `python3 -I -B tools/round-40/sqfs-triage-v2.py --selftest` | 0 | `2298d7027730335b0f6463190899093f1a1f686031a1ff80c5db00108d2fb499` | 1772 |
| `v4-table-shape` | v4 region header-cell / data-row count | 0 | `77622c1a46f6aaa22fd99860bbf6a45e3f7e73ffdbbd0ef4bec37774bef7adc7` | 11 |
| `r39-c1-receipt-read` | read `.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json` | 0 | `40dda39703d589dccda52c493ef095242948c6f30537bf899d4fb36499786af4` | 11 |
| `worktree-drift-status` | `git rev-parse HEAD; git status --porcelain \| grep -E '^ M '; git diff --stat LOG.md SCORECARD.md corpus/lessons/round-44.md; git diff --quiet -- SHONEN.md/SKILL.md/PROVINCE.md` | 0 | `f8155b862e614f644e0dcd9d3efdd6e680fe3861cf844b9679cb57f2a6ffae31` | 61 |
| `committed-record-anchors` | `git show 8bb1090a:{corpus/lessons/round-44.md,LOG.md,SCORECARD.md} \| grep -n …` (R44-CL1/CL2/M44-2, LOG headings, SCORECARD correction markers) | 0 | `f9831f7bdded37df51a7b7d7b07bd643c78cb1f448d45468b3f71b9e6712834a` | 5 |
| `shonen-history` | `git log --oneline c29360e3..8bb1090a -- SHONEN.md` | 0 | `c975372dca8fdc999c86ac8f59bfe42427966e87bb222399179eb0bb3029b87e` | 4 |

Rows marked with `…/` or a prose summary (`pointer-existence`, `skill-anchors`, `province-ranges`, `province-prefix`, `v4-table-shape`, `committed-record-anchors`, the two `c2-counter-*` rows and the short `preflight-*` rows) are abbreviated for table width only. The **verbatim** command, cwd, exit code, full stdout sha256 and wall time for all 27 rows are recorded in `artifacts/R44W2ScribeShonen/receipts.json`, and each row's captured stdout is `artifacts/R44W2ScribeShonen/<name>.out`. All scratch paths named there are under `/fast/scratch/hyaku/kaidoku-r44/R44W2ScribeShonen/` and have been deleted (§9).

## 8. What I did not do (limits of this report)

- **Did not re-run C1.** It needs the rea-agents 6.5.0 `--pkg65` package root, and the C1 verdict is another seat's measurement; I read the committed receipt `.ufo/waves/round-44/l1/c1-score-at-55bcce69.json` and the LOG/lesson text. The C1 numbers in this report are therefore **record values, not my execution**.
- **Did not edit** any claim, counter, rubric, frozen byte, `MANIFEST.json`, `.ufo/state/`, production doc, or another seat's output. Findings only.
- **Did not run any mutating git/jj command**, and built no fixture repo (the preflight red/green is on real lane revisions).
- **Installed no tool**; `pacman` untouched; no network fetch.
- **Resolution is structural + anchor-based.** "Resolves" means the cited file/line/commit/marker exists and the cited text is at the cited position — not a semantic audit of every sentence (the same limit command A states: depth 10 is citation existence plus in-file ranges). Where a numeric claim was cheap to re-derive (selftests 35/35 and 45/45, v4 shape 13×15, r39 6/6, r42 78/78, region hash) I re-derived it and say so; where it was not (e.g. `c2-counter.py --selftest` 27/27, the round-40/41 receipt bodies) I treat it as receipt-bound.
- **D3 does not claim the round's numbers are wrong.** Command A's five checks are a one-round-lag structure that is red at every revision tested; the defect is disclosure, not arithmetic.

## 9. Scratch

Scratch root `/fast/scratch/hyaku/kaidoku-r44/R44W2ScribeShonen/` (receipts, counter `--work` dirs `c2work`/`c2work-tip`, `pf-*.json`, region/shape scripts) was deleted after the receipts and hashes were copied into `.ufo/waves/round-44/w2/artifacts/R44W2ScribeShonen/`. No `/tmp` path is cited anywhere in this report.
