# kaidoku luna-round-1 — coverage map completion

Date: 2026-10-16. Axis: **coverage** (lowest on SCORECARD: 9.72 vs depth 10,
calibration 10). One axis-move. Wave: one batched 64-seat AgentSwarm on
`openai-codex/gpt-6-luna-max`, parent-integrated (no seat commits).

## Work performed

- Baseline reproduced four times before integration: seat R1 replayed command
  A inside an isolated `git archive` tree; seats C1, P2, R4 replayed it at
  HEAD `a79945c4`. All four: mapped=70, missing=[r14-01, r14-02], dangling=[],
  coverage 9.72, depth 10.0 (9/9 rules). Wave reports: `.ufo/waves/luna-round-1/`.
- Exclusion case examined and defeated (seat C1): both r14 files belong in
  the map — README's row rule is file-existence-based (`corpus/README.md:8-9`),
  both are Knowledge-table listed (`:126-127`), and partial-work precedent
  exists (`:32`, `:44`).
- Both files deep-read by 6 seats (X1–X6): map-worthy; r14-01 is a
  discharged-residue record, r14-02 a checks/sweep record. Their own caveats
  (stale 6.4.0 pins, dead external citations, `/tmp` scratch pointers — X2/X4/X5)
  are content debt of the files, not map blockers.
- Row drafts: M1/M2 with per-phrase defense bullets; independent convergence
  drafts R3 (r14-01) and R4 (r14-02) matched substance. Critic C5 forced
  **partial** qualifiers into both rows.
- Format ruling: seat D3 claimed the r9-r12 precedent has four cells; refuted
  by direct measurement — all 58 map rows carry 4 pipes (3 cells). New rows
  follow the 3-cell precedent.
- Sibling scan (K1): revenger topical overlap recorded, not absorbed; no
  lore/chousa/mori boundary touched.
- Integration: two rows added after the r12-02 row; work commit `2abd30f5`
  under lane identity `kaidoku-shokunin <kaidoku@shokunin.local>`.

## Landed changes

- `corpus/README.md` — +2 coverage-map rows — commit `2abd30f5` (lane identity).
- `LOG.md` — this round's append entry — bookkeeping commit (see below).
- `SCORECARD.md` — coverage row 9.72 → 10.0 with measured commits, coverage
  open-gap closed, this round's section appended; the frozen 2026-10-15
  reconciliation table left intact (superseded on the 70/72 point, not rewritten).

## Before → after measurements

Counting command: SCORECARD.md:91-122 (command A, source-derived, reads git
objects only).

- Before, at `a79945c4`:
  `{"citation_resolved_rules": 9, "coverage_score": 9.72, "dangling": [], "depth_score": 10.0, "knowledge_files": 72, "mapped": 70, "missing": ["2026-10-14-r14-01-queue-b-residual", "2026-10-14-r14-02-final-sweep"], "rule_blocks": 9}`
- After, at `2abd30f5`:
  `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 72, "mapped": 72, "missing": [], "rule_blocks": 9}`
- Structural check at `2abd30f5`: map section rows 58 → 60, uniform 3-cell
  pipe shape, no section-boundary change (`## Knowledge` intact).
- The observable is unchanged and still limited: **index integrity only, not
  fraction of the REA domain held** (SCORECARD.md:23). No semantic correctness
  of any row's summary is claimed by this measurement.

## Findings & named debt (recorded, deliberately not fixed — one-axis move)

Map-row drift found by V-seats (future row-accuracy/freshness round):
V01 asar wording + doctor-registration subclaim; V03 README:41/:15 pointers;
V05 r2-frontier-prereqs misfiled under Firmware; V06 r3-appimage
"unaddressable" + r3-apk "120 nodes" overstatement; V08 typora zero-finding
scope; V11 libsignal 188MB vs 24.9MB (README:25 area); V15 r4-15 count +
Electron completeness; V16 → r4-16 supported; V17 firmware GSP unblob
wording; V18 README:44 implication; V20 r5-01 timeout qualifier + r5-02
"3/3 selected probes"; V27 r12-01 byte-exact overstatement; V28 r9-02
statuses clause. Seat-level defects: D3 miscount (refuted pre-integration);
X6 conflated the Knowledge table (:127) with map membership; R4 no-peeking
breach (self-reported; only path metadata returned); S2 pointer-style
conformance notes; S1: four untracked `.ufo/interactive-sessions/` files
predate this wave — untouched. C7: SCORECARD stale-summaries `:157` pointer
is at `:160` in HEAD.

## SHONEN

- [~] SKILL.md decision tables/citations: unchanged — no semantic audit this
  round; no identified outside verifier.
- [~] e2e domain task executed and logged: unchanged — new rows cite prior
  e2e work; nothing new executed this round.
- [~] executable without oral context: unchanged — command A replayed by 4
  seats, but no box-specific verifier named.
- [~] no cross-domain bleed: unchanged — K1 recorded the revenger overlap;
  PROVINCE.md untouched.
- Seat R8's assessment stands: wave seats are parent-dispatched and do not
  satisfy the fleet's named non-author verifier bar; no box advanced.

## Verdicts

- coverage: **improved** (9.72 → 10.0, map completeness only).
- depth: **unchanged** (10.0; 9/9 citation-resolved rules both sides).
- calibration: **unchanged** (10; no reconciliation obligations touched).
- Learning trends: expansion unchanged; quality improved (index completeness
  only, not content truth); discernment unchanged.
- Admitted: yes — one axis improved, none harmed.
