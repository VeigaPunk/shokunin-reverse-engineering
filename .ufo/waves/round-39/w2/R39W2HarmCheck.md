# R39W2HarmCheck — no-harm check across owned axes, round 39 wave 2

**Verdict: DEFECTS FOUND** — no owned axis is harmed (every instrument and surface check below is green), but round 39 landed without touching `SCORECARD.md` or `SHONEN.md`, leaving **5 stale current-state self-assessment statements** (§5, D1–D5) plus 3 minor convention items (§5.2) that the L1 must fix before the report.

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base `a2f64e1da78afcf8cc39287106604dbcc270844c`, tip `52b0eb2907c704ed5f184c47b14c723208e5cbbc`, freeze `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b`. All git use read-only (`show`, `diff`, `numstat`, `ls-tree`, `cat-file`, `rev-parse`, `status`); no VCS mutation, no subagents, no background jobs. Scratch `/fast/scratch/hyaku/kaidoku-r39/R39W2HarmCheck` removed at the end; cited material copied to `artifacts/R39W2HarmCheck/`. **No tools were installed or upgraded** (none needed; pacman transactions are paused host-wide and were not touched).

## 1. Whole-diff census (base → tip)

`git diff a2f64e1d 52b0eb29 --stat`: 1429 files, +118628 −4. Exactly **3 files carry deletions** (`artifacts/true_deletions.txt`), all in `tools/round-38/` and all part of the declared `--selftest` landing:

| file | +/− | what the − lines are |
|---|---|---|
| `tools/round-38/freeze-drift.py` | 178/1 | the `import argparse, json, subprocess, sys` line, widened to add `os, shutil, tempfile` |
| `tools/round-38/intended-doc.py` | 170/1 | same import-line widening |
| `tools/round-38/registry-immutable.sh` | 100/2 | the awk program's `NR==FNR` line and `END` block — the disclosed run-mode strictening (deletion/reorder detection) |

Everything else is additive and round-39-scoped: `.ufo/waves/round-39/**` (1256), `corpus/evidence/round-39/**` (146), `tools/round-39/**` (13), the six surfaces below, `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md`, `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md`, `corpus/lessons/round-39.md`, `plans/round-39-claims.md` (added by the freeze). `LOG.md`, `SCORECARD.md` and `SHONEN.md` are **unchanged** across base..tip (see §5).

## 2. Per-surface diffs — all purely additive, all inside allowed regions

| surface | diff | confinement check |
|---|---|---|
| `PROVINCE.md` | +8/−0 | 8 lines appended at :377–384 (`## Round-39 additions to Core` + round-39 frontier note); every line ≤:376 byte-identical |
| `SKILL.md` | +57/−0 | rule block 18 inserted after base :315 (tip :316–344: prose :316–331, marker `<!-- sqfs-triage-table v1 -->` :333, table :334–343) and `### Round-35/37/38/39 instrument registry` appended at :1328–1354; craft rules 1–17 byte-identical; nothing else |
| `corpus/SOURCES.md` | +5/−0 | rows S118–S122 appended; **rows S001–S117 byte-identical** (row-level compare of all 117 ids: 0 changed, 0 missing) |
| `corpus/QUALITY.md` | +1/−0 | row 82 appended (single hunk); **rows 1–81 byte-identical** |
| `corpus/README.md` | +6/−0 | 2 coverage-map rows, 2 knowledge rows, 1 lessons row, 1 Frontier line |
| `SCORECARD.md` | no diff | — (that is the finding, §5) |
| `SHONEN.md` | no diff | — (that is the finding, §5) |

Patch evidence: `artifacts/surfaces.patch`.

## 3. Command A at both revisions (SCORECARD recipe, verbatim)

Run from the lane repo over git objects only (`artifacts/command-a.json`):

```json
base a2f64e1d: {"citation_resolved_rules": 17, "coverage_score": 10.0, "craft_heading_line": 81,
 "craft_last_nonblank_line": 314, "dangling": [], "depth_score": 10.0, "knowledge_files": 126,
 "mapped": 126, "missing": [], "rule_blocks": 17}
tip 52b0eb29: {"citation_resolved_rules": 18, "coverage_score": 10.0, "craft_heading_line": 81,
 "craft_last_nonblank_line": 343, "dangling": [], "depth_score": 10.0, "knowledge_files": 128,
 "mapped": 128, "missing": [], "rule_blocks": 18}
```

**Instruments unharmed.** At the tip both new knowledge entries are mapped (`missing: []`, `dangling: []`), rule block 18's citations all resolve (`2026-10-26-r39-sqfs-outcome-triage.md:11-28/29-40/41-54` fit the entry's line count), and coverage/depth scores hold at 10.0/10.0. The craft section grew from last-non-blank 314 → 343 (heading line 81 unchanged).

## 4. Round-38 tool changes and frozen-path spot check

- The three `--selftest` additions run clean at the 52b0eb29 bytes (worktree `e40a25df` is byte-identical to the tip on these three files — `git diff 52b0eb29..e40a25df` on them is empty): `freeze-drift.py --selftest` exit 0, cases=8 pass=8; `intended-doc.py --selftest` exit 0, cases=9 pass=9; `registry-immutable.sh --selftest` exit 0, cases=5 pass=5 (`artifacts/selftests.txt`). Case counts match the SKILL registry rows (8/9/5).
- `registry-immutable.sh`'s run mode is now stricter (exits 1 on a deleted or reordered base row, which the round-38 bytes accepted) — disclosed in the SKILL registry row and consistent with the round-38 lesson's M38-8 intent. No owned-axis statement depends on the old lenient behavior; round-38 scores are pinned at round-38 revisions and are unaffected.
- C2 frozen path: `git diff 8fcda41c 52b0eb29 -- SKILL.md` is a **single hunk** `@@ -1324,3 +1324,31 @@` (the registry append) — the triage-table block (:333–343) is byte-identical from the freeze through the tip (`artifacts/freeze-to-tip-SKILL.patch`).

## 5. Calibration debts — self-assessment statements now FALSE at 52b0eb2

Round 39 edited SKILL.md/PROVINCE/README/QUALITY/SOURCES but never refreshed `SCORECARD.md` or `SHONEN.md`, so their current-state cells are stale. Exact lines in `artifacts/cited-lines.txt`.

### 5.1 Debts (L1 must fix before the report)

- **D1 — `SCORECARD.md:23` (coverage row).** "126/126 knowledge files mapped after the round-38 landing (two entries added and mapped: <r38 pair>; …)". False at the tip: command A measures **128/128**. Corrected form: "128/128 knowledge files mapped after the round-39 landing (two entries added and mapped: `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md`, `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md`; 126/126 after the round-38 landing, …)". The row's last-change cell "count refreshed rounds 25, 26, 31, 36 and 38" must gain 39.
- **D2 — `SCORECARD.md:24` (depth row), count.** "17/17 queue-drain rule blocks have resolvable file/range citations at `c369242f` (recount, round 31; also 17/17 at `ebe2cb4a`, round 26)". The pinned recounts remain true, but as the current-state count this is false at the tip: **18/18** at `52b0eb29` (rule block 18 added by R39-C2; `rule_blocks` 18, `citation_resolved_rules` 18, `depth_score` 10.0). The last-change cell "count refreshed rounds 25 and 26" must gain 39.
- **D3 — `SCORECARD.md:24` (depth row), craft range.** "craft section `SKILL.md:81-314` (heading line 81, last non-blank line 314; …)". False at the tip: **`SKILL.md:81-343`** (heading line 81, last non-blank line 343 — the `clean` table row; rule-18 block inserted after base :315).
- **D4 — `SHONEN.md:6` (box 1).** "asserted: `SKILL.md:81-314` (craft section; 17/17 rule blocks have resolvable citations, …) at round-14 work commit `3e99fbd6…`". Stale as a current-state assertion: at `52b0eb29` the craft section is **:81-343** with **18/18** resolvable citations. The pinned historical assertion itself is internally consistent — command A at `3e99fbd6` measures 92/92 mapped, 17/17 rules, craft 81–314 — so the fix is to add/refresh a current recount, not to delete the pin. [INFERENCE] observation: `3e99fbd6` holds 92 knowledge files and 17 rule blocks, which is arc2-era state, not round-14-era (70/72, 9–10 rules); the "round-14 work commit" label looks like a pre-existing mislabel, not a round-39 defect.
- **D5 — `PROVINCE.md:374` (round-36 frontier note), final sentence.** "Big-endian/AVM and vendor-mangled images stay Frontier." False for standard BE at the tip, and the round-39 note (:384) names only the bullet (:156–157) and the round-38 note (:376) as superseded — :374 is not in the supersession chain. Corrected form: extend :384's list to name the round-36 frontier note (or add a dated pointer at :374), e.g. "…and the round-36 frontier note's final sentence are superseded for standard big-endian SquashFS v4…".

### 5.2 Minor / convention items (judgment calls, listed for completeness)

- `PROVINCE.md:157` — the bullet's dated bracket still reads "big-endian/AVM stays here. Round 38: … not promoted" with no round-39 sentence. Round 38 updated this bracket in place; round 39 did not. The :384 note supersedes "the big-endian part of the bullet" by name, so the claim predicate is met; this is a convention gap only.
- `corpus/README.md` Frontier, round-36 dated line — "Still frontier: big-endian/AVM (`sasquatch-v4be`) and vendor-mangled images." The new round-39 line names only "the round-38 line above". Same class as D5 under the dated-history convention; the round-39 line is the current state.
- `tools/round-38/registry-immutable.sh` — the in-file VARIANT NOTE still says "this copy … is NOT the assigned deliverable; tools/round-38/registry-immutable.sh is unchanged by this seat", but the file **was** landed as this variant in 52b0eb2. The SKILL registry row documents the landed behavior correctly; the in-file note is now self-contradictory (cosmetic).

### 5.3 Statements checked and NOT false at the tip

- `SHONEN.md:12` (box 4) — "PROVINCE.md still accurate", ranges `PROVINCE.md:97-125`, `:8-14`, `:24`: intact (the round-39 append starts at :377; nothing shifted).
- `PROVINCE.md:372` round-36 Core row aside "(`sasquatch-v4be` is its big-endian sibling, unmeasured)" — superseded by :376 ("the row's aside … is history as of round 38"), which :384 names; covered transitively.
- `PROVINCE.md:376` "Big-endian SquashFS stays Frontier." — named by :384; covered.
- `SCORECARD.md:25` (calibration row) — rubric.json/result.json/command B inputs untouched by round 39.
- `SCORECARD.md` historical recounts and history cells — pinned to revisions, remain true.

## 6. Limits

- The SKILL registry's "behaviour parity 18/18 on recorded receipts" claim for `freeze-drift.py` was not re-run here (wave-1 evidence `.ufo/waves/round-39/w1/R39CL2Selftests.md`); I verified the selftests and the disclosure only.
- Command A is the SCORECARD recipe executed verbatim; it measures index integrity and citation resolvability, not semantic correctness (the recipe's own stated limitation).
- The two UTF-8-filename entries in the diff (K5 carrier/evidence `アイコン.txt`) are inside the round-39 wave/evidence trees and were not opened (out of seat scope).
- `LOG.md` is unchanged across base..tip; round 39's log lives in `corpus/lessons/round-39.md`. Noted as an observation; LOG.md is not in this seat's surface list.

## 7. Evidence index (artifacts/R39W2HarmCheck/)

`command-a.json` (command A at base/tip + the 3e99fbd6 pin), `surfaces.patch` (six-surface diff), `round38-tools.patch` (the three tool diffs), `freeze-to-tip-SKILL.patch` (single registry hunk), `true_deletions.txt` (the 3 files with deletions), `selftests.txt` (8/8, 9/9, 5/5), `cited-lines.txt` (exact stale lines).
