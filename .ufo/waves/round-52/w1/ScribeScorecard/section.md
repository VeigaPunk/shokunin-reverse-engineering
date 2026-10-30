<!--
DRAFT — round-52 SCORECARD section skeleton (seat ScribeScorecard, wave r52-w1).
Not a claim verdict. Every AFTER / verdict / measured-commit / planned cell is an
explicit placeholder for the L1 to fill from committed receipts only.
Placeholders are written as <ANGLE-BRACKET TOKENS>; a token must be replaced by a
measured value or the cell must be deleted — an unfilled token may not ship.
Landing rule: this section lands ONLY at the round-52 landing commit, and only if
the L1 has receipts for both claims. If a claim is not measured, its row states
"not measured" and the section says so — an absent receipt is not a 0.
-->

## Round 52 (2026-10-30) — <HEADLINE: one-line round outcome, written after the landing; e.g. "the device-accounting law re-frozen and measured; triage v6 executability audit landed">

Base `c525de54a53eb3c4fee28ede2721da4527cf8ece` (round-start tip, pushed). Claims draft
`ab0eafedc41402b43b41a4362084119578dfe7ce` (`plans/round-52-claims.md`; the round's rule — the
file is authoritative over any summary). Round-52 freeze commit: <FREEZE-HASH>; landing commit:
<LANDING-HASH>. The freeze is ONE commit adding the round-52 instruments, fixtures and the
amended claims; amendments found by wave-1 attacks land in that commit and are listed in
`plans/round-52-claims.md` `## Wave-1 amendment record`.

Round shape: wave r52-w1 = **64 seats**, policy v2, band 64–128, build + attack mixed
(`.ufo/waves/round-52/w1/`; dispatch `1842addcef3458515859b928b92d9bbd0a46c5d5`; roles from
`w1-dispatch.json`: executor 21, scribe 8, reviewer 8, scout 7, critic 7, mutation-tester 4,
connector 3, sentinel 3, revenger 2, simplifier 1; attack roles 24/64 = 37.5 %, above the 25 % attack-role floor;
the §3 planner seat is the L1). Wave r52-w2 (falsify, 32–64 seats) is dispatched after the
landing only when wave 1 yields ≥32 distinct attack items; otherwise one residual `task` call of
≤8 reviewer/critic seats. Round total ≤128. <W2-OR-RESIDUAL: dispatched count and seat total, or
"not dispatched" with the reason>.

Both claims are written against the same committed before-state: the round-50 attempt-2 receipt
`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` (`carriers_matched 2`, exit 1) for C1, and
the v5 triage-table bytes for C2. R52-C1 works the coverage axis, R52-C2 works the depth axis;
the owned axes stay tied at 10, so both satisfy the lowest-axis rule, and the two claims share
no write surface except their own record sections here and in `LOG.md`.

| claim | axis / surface | before | after | counting command | measured at |
|---|---|---|---|---|---|
| R52-C1 | coverage — `PROVINCE.md` Frontier entry **LE AVM members (`hsqs`)** promoted to Core under the re-frozen device-accounting law; `tools/round-52/` package (`gap-rule.json` law-derived rule, `c1-counter.py` v2, `c1-controls.py`, `c1-run.sh`, `fetch-vendor.py`); knowledge entry `corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md`; README map row, SOURCES row(s), PROVINCE Core section, registry rows | **committed, measured.** Round-50 attempt-2 receipt `carriers_matched 2` of target 4, exit 1 (`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`; `met_target false`; failing `g7581:gaps_ok`, `g7581:projection_ok`, `g7582:gaps_ok`; `bindings_false` = `province_core_section`, `province_core_row`; `frozen_path_changed []`; `counter_sha256 9820811b…`). The rule's single silent char-device allowance `247:0` was generalised from the Cable class, leaving the FRITZ!Box class's other twelve device rows unaccounted. | <AFTER-C1: `carriers_matched N`, `gaps_ok`/`law_shape_ok`/`census_rederived_ok`/`depth_gap_recorded`, every binding, `frozen_path_changed []`, exit code, receipt path> | <COUNTING-CMD-C1: the exact predicate command, e.g. `python3 -I -B tools/round-52/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --receipts corpus/evidence/round-52/c1 --json-out <OUT>`> | <MEASURED-AT-C1: the `revision` field of the C1 after receipt, and the receipt path `.ufo/waves/round-52/l1/scores/c1-after.json`> |
| R52-C2 | depth — `SKILL.md` rule block 27 (triage table v6: new `legacy-body-unreadable` row, action `preserve-unresolved`, no cross-read) plus the instrument `tools/round-52/sqfs-triage-v6.py` with the frozen executability audit and freeze-drift gating; block 26 (v5) stays as history | **committed bytes, measured routing.** At the claims-draft base the v5 table routes the ddwrt FAILED no-pad body `dmg_Z3_v3ddwrt_inode_table` to `legacy-body-failure` / `cross-read-legacy` — a cross-read prescribed on a body whose readers refuse (ddwrt family 6/7 no-reader). Measured by seat ScribeScorecard over the frozen 126-envelope corpus with the committed v5 instrument at the claims-draft SKILL bytes: `pair_mismatches 0`, `evaluator_missing 0`, label distribution `legacy-body-failure 7`, and the named envelope labelled `legacy-body-failure` / `cross-read-legacy` (receipt `ScribeScorecard/receipts.json`, entry `c2-v5-baseline-at-claims-draft`, exit 0, stdout sha256 `0d598516…`). Measured in the same run: the two clean ddwrt no-pad `_ddefault` envelopes (`squashfs_v3_ddwrt_squashfs_v3.be.nopad_ddefault`, `…le.nopad_ddefault`) are labelled `clean` / `none`, so the v6 route change is confined to the one FAILED-body pair. The claims draft states the frozen executability audit's before-state as **1 violation** naming `dmg_Z3_v3ddwrt_inode_table`; the v6 audit instrument does not exist in committed bytes yet, so that violation count is a declared before-state, **not yet a receipt** — <C2-BEFORE-RECEIPT: receipt path once the L1 has scored the v5 bytes with the v6 audit>. `census_outside 0` on both sides: `python3 -I -B tools/round-51/census3.py --root . --rev <REV> --check` exits 0 with `registry_paths 56`, `census_paths 56`, `census_outside []` at the round base `c525de54…` and at the claims draft `ab0eafed…` (receipt `ScribeScorecard/receipts.json`, entries `census3-check-at-round-base` and `census3-check-at-claims-draft`) — a no-regression binding inherited from round 51, not a claimed move. | <AFTER-C2: `pair_mismatches 0`, `evaluator_missing 0`, `executability_violations 0`, `census_outside 0`, selftest cases green, exit code, receipt path> | <COUNTING-CMD-C2: the exact predicate command, e.g. `python3 -I -B tools/round-52/sqfs-triage-v6.py --root <LANE> --rev <REV> --freeze <FREEZE> --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes --json-out <OUT>`> | <MEASURED-AT-C2: the `rev` field of the C2 after receipt, and the receipt path `.ufo/waves/round-52/l1/scores/c2-after.json`> |

Owned scores: coverage `<COVERAGE-SCORE>` (<COVERAGE-HEAD-UPDATE: the coverage observable moves
from 141/141 to 142/142 once the round-52 knowledge entry `2026-10-30-r52-avm-le-squashfs-core`
lands and its `corpus/README.md` coverage-map row is written — the map's 142nd file; paste the
measured command-A line at the landing revision (`knowledge_files`, `mapped`, `missing []`,
`dangling []`, `coverage_score`) inside this cell; the finite proxy is at its ceiling and the move
would be the measured promotion of LE AVM members to Core, not a number above 10 — write the score
only after the measurement, and write "unchanged" if the promotion did not happen>). depth
`<DEPTH-SCORE>` (<DEPTH-HEAD-UPDATE: rule blocks 26 → 27 with `citation_resolved_rules 27/27`
and `depth_score 10.0` at the landing — paste the measured command-A line here; nothing in this
cell is asserted before the landing>). calibration `<CALIBRATION-SCORE>`
(<CALIBRATION-HEAD-UPDATE: the round-52 record's own self-assessment atoms, if the round
re-derives any; otherwise "unchanged, no calibration claim">). <If a claim is not measured, its
owned-axis line says "unchanged" and names the absence rather than crediting a partial run.>

Learning trends: expansion <EXPANSION-TREND> (if the entry lands, it is a promotion of
already-measured ground; a promotion is not new ground unless the round measured a surface the
map did not name).
quality <QUALITY-TREND> (bounded by what the receipts show: pre-freeze controls red where they
must be, the data run's own provenance, and the falsify wave's independent re-measurement).
discernment <DISCERNMENT-TREND> (the bar is a disagreement that becomes a grounded criterion or
an outside agreement, not internal control behaviour).

Limits: <LIMITS-PARAGRAPH: what each claim's receipt does and does not establish — e.g. the
device law's width statement (char-device rows only: no fifo, socket or block-device row exists in
any measured carrier), the receipts not naming the path a `depth-limited` gap stopped at, the
held-out corpus being the round-42 recon set (depth, not held-out generalization), and the
per-carrier-class derivation resting on the committed non-regular census tables>.

- **planned (round 53):** <PLANNED-NEXT-ROUND: the concrete next move(s), each naming its axis
and its evidence obligation; empty is allowed only with the reason>.
- **retired:** <RETIRED: none, unless an axis is genuinely retired, with the reason>.

<!--
Coverage-head update line (the `## Owned axes` coverage row is edited IN PLACE at the landing,
not appended):

OLD (round-51 head, current at `1aa273694f4409d3432fbcd73e83a33bee0dd8e9:SCORECARD.md:23`):
  "Round-51 index integrity: 141/141 knowledge files mapped; no Frontier→Core promotion. …"

NEW (round-52 head, to be written at the landing, only if the entry and its README map row land):
  "Round-52 coverage head: 142/142 knowledge files mapped (the 142nd file is the round-52 LE AVM
   Core entry `2026-10-30-r52-avm-le-squashfs-core`); LE AVM members (`hsqs`) promoted
   Frontier → Core under the re-frozen device-accounting law. …"

If the entry does NOT land (claim missed), the head stays 141/141 and the row says the promotion
did not happen — a measured miss does not move the index.

Measurements backing the before column (all run by seat ScribeScorecard, receipts in
`ScribeScorecard/receipts.json`, each entry carries argv, cwd, UTC, exit code and stdout
sha256; full stdout sha256 values are in the receipt file):

  census3-check-at-round-base        exit 0  sha256 05fd7281c9cc723ad57a37d0dac670670fb3110807991be5c6a95e9756f1aaef
  census3-check-at-claims-draft      exit 0  sha256 6b2484fc157f52e6327d686cf3c36b54c55874a825af52c5b5ecdf47fef07bff
  c2-v5-baseline-at-claims-draft     exit 0  sha256 0d5985165972868c9bc10a1cb43121cd3dd206ea50033ff393dca7cc446ac172
  git-diff-base-to-claims-draft      exit 0  sha256 e6e6d5148327c7834e617044c3af91dc83a81a24f3da84c42e43ade89ed0fc6f
  git-ls-tree-knowledge-count-base   exit 0  sha256 85a0e6eb5530a682fa88345a5e7a144248f49e5b71b3eb587a9db5cd2957495a

  (the `git diff` receipt shows the claims draft adds exactly one path,
   `plans/round-52-claims.md`; command A at both `c525de54…` and `ab0eafed…` reports
   knowledge_files 141, mapped 141, missing [], dangling [], rule_blocks 26,
   citation_resolved_rules 26, coverage_score 10.0, depth_score 10.0 — the pre-freeze
   coverage observable is therefore 141/141 and the depth observable 26/26.)
-->
