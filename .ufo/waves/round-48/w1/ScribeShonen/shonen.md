# SHONEN.md — four lines for the round-48 landing (draft; no `[x]` awarded)

Anchored at the round-48 declared freeze **A4 `0f06251bf6a3a6964c715f67243d4df12e854258`**
(re-derived: `git log -1 --format=%H -- plans/round-48-claims.md`; tip at write time
`663f30ee751694fb0970e7de68fe88356e680822`, 2026-10-28T18:55Z). The prompt's named freeze
`dc73587a` is the **A1** commit — three amendments stale; the claims file's own rule
("the declared freeze is the commit that carries this paragraph") and the
`git log` re-derivation give A4. `[x]` needs a **named non-author verifier** for the box as a
whole; none exists for any of the four — the round-47 verifier spot-check
(`corpus/lessons/round-47-verifier-spotcheck.md`) verified claims, trends and gate decisions,
not a SHONEN box. Named non-author *lane* seats are listed where they exist.

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  asserted: at A4 the craft section is `SKILL.md:81-642` with **24** rule blocks; command A
  (verbatim recipe, `SCORECARD.md:86-143`) at `0f06251b` re-derived by me →
  `{"rule_blocks":24, "citation_resolved_rules":24, "mapped":138, "knowledge_files":138,
  "missing":[], "dangling":[]}` (receipt `receipts/commandA-at-A4.json`, stdout sha256
  `4cf13474…`) — 24/24, not the round-47 23/24: block 24 (`SKILL.md:632-641`) gained the
  knowledge citation `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66`
  at `04469ee8`; the v4 triage table remains byte-stable (region sha256 `92540586…1b101f2`,
  last re-derived at `1e2c3102`, `.ufo/waves/round-47/w1/ScribeShonen.md`). Round 48 lands the
  25th block: `<!-- verdict-meaning-table v1 -->` (0 occurrences at A4), header
  `trigger | v1 hole | v2 arm | exit`, two rows keyed by routed id (`R46-CL7→meaning`,
  `R47-CL10→floor`), mutations/interpreter pins, ≥5 resolving citations incl. a
  `corpus/knowledge/` entry; and the marker-bound registry section (`SKILL.md:1705-1750`,
  40 rows at A4 = the `tools/round-48/census2.json` path set minus exactly
  `tools/round-48/{meanings,record2}.py`, set-diff re-derived by me) grows to 42 rows with
  every verdict map split into its 0/1/2 meaning segments. verifier for `[x]`: **none outside
  the lane**; non-author lane derivations: the wave-1 seats that attacked the same surfaces
  (`.ufo/waves/round-48/w1/C1Gold.md` classifier counterexample, `w1/CritAxis.md` skipped-row
  counterexample) and my own runs (`receipts/`).

- [~] At least one end-to-end domain task executed and logged in LOG.md
  asserted: `LOG.md:3174-3183` (round 42 — REA `extract-firmware --max-depth 1` on four
  published SquashFS v3 LZMA rootfs images; C1 4/4 at `eb8215ac`, receipts
  `corpus/evidence/round-42/c1/*`), `LOG.md:3184-3197` (round 43 — 78 fresh carriers,
  `matched=78/78` at `77d196c6`), `LOG.md:3164-3173` (round 41, 4/4 at `e9a24d07`, reproduced
  `R41W2ReproL/V3/V4`), `LOG.md:3153-3163` (round 40, 3/4 honest stop), `LOG.md:3137-3152`
  (round 39, 6/6 at `6fdaf4f1`, w2 re-runs). Round 48 adds no domain task — the claims file
  assigns no coverage claim ("adds no domain surface: no knowledge entry, no PROVINCE move,
  no coverage-map row", `plans/round-48-claims.md:16-17`), so the box's freshest pointer stays
  the round-43 LOG entry. verifier for `[x]`: **none outside the lane**;
  `.ufo/waves/round-42/w2/` does not exist — lane reproductions cover rounds 39/40/41 only.

- [~] Instructions executable by an agent without oral context
  asserted: at `663f30ee` run from scratch copies of the committed blobs
  (`receipts/selftest-{sqfs-triage-r39,c2-counter-r39,sqfs-triage-v2-r40}.txt`):
  `tools/round-39/sqfs-triage.py --selftest` → `cases=35 pass=35 fail=0`;
  `tools/round-39/c2-counter.py --selftest` → `{"cases":27,"pass":27,"fail":0}`;
  `tools/round-40/sqfs-triage-v2.py --selftest` → `cases=45 pass=45 fail=0` — all exit 0,
  2026-10-28T18:53Z. New this round and also executed, exit 0 at A4 bytes:
  `tools/round-48/meanings.py --selftest` (`"failures": 0`,
  `receipts/meanings-selftest-HEAD.txt`) and `tools/round-48/record2.py --selftest`
  (`corr_parse true`, `receipts/record2-selftest-HEAD.txt`). Held-out executions stand:
  round-39 table 20/20, round-40 table 26/26 by an independent evaluator
  (`R40W2C2IndepEval`). The counting recipes remain command A + command B only. verifier for
  `[x]`: **none outside the lane**; lane re-runs `R39W2TriageMutants`, `R39W2C2Mutants`,
  `R40W2C2IndepEval`.

- [~] No cross-domain bleed (PROVINCE.md still accurate)
  asserted boundary only: `PROVINCE.md:97-125` (the `## Adjacent` refusal list, safety refusal
  at :116-118, round-36 dated tooling bullet at :119-125) is byte-identical at
  `52b0eb2907c704ed5f184c47b14c723208e5cbbc` and at `663f30ee` — sha256
  `f1a5cfc61851ca3411b462b54d4d0681397aecc6431738a30a968a48138c78b4` for both (re-derived by
  me). The appended sections are `:378-384` (Round-39), `:386-394` (Round-40), `:396` (Round-41),
  `:410` (Round-42) and `:424` (Round-44 measured-not-promoted, the last change — `git log -1`
  → `55bcce69`, 5 h before the freeze). Rounds 45-48 add no PROVINCE line: they are instrument
  rounds (freeze grammar, census registry, exactness, meaning binding), and the round-48
  claims file declares no coverage surface — consistent with the boundary, not a bleed.
  verifier for `[x]`: **none**; lane finding `R39W2C1AxisFit` D2 (repaired) remains the only
  named non-author PROVINCE audit.

## Stale cells (checked against the repo at A4/`663f30ee`; counts this draft does not repeat)

- S1 box 1: `SKILL.md:81-449`, "20/20 rule blocks" are round-41 values; tip is `81-642`,
  24 blocks, **24 resolved** by command A — the round-47 "23/24" observation is itself now
  stale (repaired at `04469ee8`).
- S2 box 1: "no promotion verifier" remains true but is stale in detail — the round-46
  outside spot-check (block 23 re-derived) and the round-47 spot-check (both claims verified)
  are named non-author re-derivations of the box's *content*, without being box verifiers.
- S3 box 2: reproduction coverage is rounds 39/40/41 only; `.ufo/waves/round-42/w2/` and
  `round-43/w2/` do not exist.
- S4 box 4: the asserted append list stops at Round-40 (`:386-394`); `:396`, `:410`, `:424`
  exist and are uncited — four appended sections the box certifies but does not name.
- S5 SHONEN as a file: last changed at `8de80f1d` (round 43); rounds 44-47 have no asserted
  cell and every non-round-43 pointer is ≥5 rounds old at landing.
- S6 R46-V6's SHONEN half still does not resolve: `git log -S 'cases=16' -- SHONEN.md` →
  0 commits; `grep -c 'cases=' SHONEN.md` → 0. Recurrence of the round-47 S8 cell.

## Round-48 observations that bear on the draft (not stale cells)

- O1 The seat prompt names `dc73587a8b9c` (A1) as the declared freeze; the claims file
  re-derives A4 `0f06251b` (four disclosed amendments total: A1 axis-score cell, A2 success
  guard, A3 census object-vs-list, A4 negated-meaning + indented row). Four amendments before
  verdict is the round-47 pattern recurring (M47 process cost), and every prompt built from a
  stale spec names a dead freeze — draft anchors at the re-derived value.
- O2 At the A3 bytes the counter's own `--selftest` crashed (`AttributeError: 'list' object
  has no attribute 'get'`, `receipts/meanings-selftest-A3-committed.txt`, rc=1); A4's fixture
  and classifier edits fix it (`receipts/meanings-selftest-HEAD.txt`, rc=0). A frozen
  instrument shipped an un-runnable selftest for ~2 min between amendments — evidence that the
  selftest is not itself a clause the counter scores.
- O3 `tools/round-48/meanings.py` was ` M` in the worktree 18:51-18:52Z while A4 was being
  prepared (`receipts/frozen-path-status.txt`); any counter run then exits 2
  `frozen_worktree_dirty` (observed in `w1/C1Meaning/receipt.json`). Clean at write time.
- O4 Both counters at `--freeze 0f06251b --rev HEAD`: C1 rc=1 (`block_present 0`,
  `marker_occurrences 0`, `frozen_path_changed []`, battery skipped — matches the ctl-c1-0
  semantics); C2 rc=1 (`failing`: round-47 seat atom, no re-derived `## Record corrections —
  round 48` line, 1 unbacked quoted number; `oracle.met_target true`, `axis_score_bad []`).
  Receipts `receipts/c1-at-A4.json`, `receipts/c2-at-A4.json`.
