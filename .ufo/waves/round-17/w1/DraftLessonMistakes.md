# DraftLessonMistakes (KaidokuR17.DraftLessonMistakes-3), advisory

## Behavior
Drafted the `## Mistakes` rows (class · evidence · captured-by · fix · red-before) for R16-PROVENANCE, R16-INVOCATION and the r16 dead-seat provider incident. Draft: `.ufo/waves/round-17/w1/draft-lesson-mistakes.md` (new file). Every fix row names a red-before command, run at baseline `b563c79` via Git objects. 11 rows: M1-M3, I1-I3, D1-D5; plus control C0.

## Gates
- No REA analyze/search/decompile, no Ghidra, no carrier execution, no tool runs from the round-17 contract. The contract tools (`pins.py`, `temporal-sweep.py`, `invocation-audit.py`) do not exist in the tree; the red-before commands are Git-object or `jq` checks.
- Stdlib classifier over Git objects (one-off, read-only): approximates the contract `invocation-audit` rule. Not the contract tool.

## Findings (observation unless marked [INFERENCE])
1. **Temporal claim has no pre/post record.** `verification.json:419` is a bare boolean; no pre/post keys (RB-M1 false, exit 1). Lesson `round-16.md:154` asserts stability. Captured by `round-16-verifier-spotcheck.md:183`.
2. **Contract sweep undercounts (new).** Contract regex `contract.md:93` finds 2 in-scope sites. `LOG.md:2012` ("remain unchanged across execution") is missed by the regex. `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` ("unchanged during the run") is outside the sweep file list (`contract.md:91`). [INFERENCE] The sweep count would therefore report 2 where the in-round set has at least 3 in-scope plus 1 knowledge site.
3. **Routed text overclaims one site.** The verifier says the r16 SCORECARD says pins stayed unchanged (`round-16-verifier-spotcheck.md:183`). The SCORECARD r16 window (`SCORECARD.md:2294-2348`) has 0 temporal phrases (RB-M3). Not reproduced.
4. **Registry command not isolated and not labelled.** `SKILL.md:448` uses `python3 .ufo/...` with `--root .` and no `-I`; the only retained argv is absolute and isolated (`verification.json:317-330`). The row has no `unexercised` text. Confirms `round-16-verifier-spotcheck.md:184`.
5. **Matcher ambiguity (new).** The contract's literal matching yields 4 exercised / 3 unlabelled; resolving relative paths against `--root` yields 5 / 2. custody-pair (`SKILL.md:449`) is unlabelled under the contract's scan only because its text receipts (`arc3-loop1-round2/claims/c3/EX-33/receipts/*.v2.json`) carry no `argv` key. Quote-fidelity is classified differently by rule. [INFERENCE] The red-before count for R16-INVOCATION depends on the rule chosen; the contract does not pin it.
6. **Dead-seat counts are internally consistent (control).** 64 = 36 + 28; 28 = `len(failure_records)`; role join gives scout 14, connector 8, critic 6; provider classes 22 credit (`charm-hyper` 402) and 6 capacity (`openai-codex`). Consistent with `round-16.md:159-160` and `LOG.md:2016`.
7. **Dead-seat provenance is thin.** `wave1-outcomes.json:7` records no role, provider or timestamp per failure (RB-D1 false). Dispatch carries no provider per seat (`wave1-dispatch.json:676`; RB-D4 false). `role_mix` (`:153`) is the dispatched mix, not the completed mix (RB-D5 false).
8. **"Immediate" timing is unsupported.** Asserted in `round-16.md:59`, `LOG.md:1965`, and fleet `.ufo/reports/round-16/kaidoku.md:13`. The verifier itself says the timing is unverified (`round-16-verifier-spotcheck.md:186`).
9. **Ambiguous follow-up sentence (fleet).** Fleet `kaidoku.md:13` "Follow-ups retained original identities" vs `wave2-outcomes.json:2` "Follow-ups retained the same seat identities" (w2 only). `wave1-dispatch.json:1001` `resumeSends: []`. The verifier rejected the w1 reading (`round-16-verifier-spotcheck.md:58`). The fleet line is outside this lane.
10. **Recurrence not cited.** The same hyper 402-on-all-seats class appears in `LOG.md:1489-1494` (arc3-loop1-round4) and `SCORECARD.md:1585` (cites "within ~30s"). The round-16 lesson cites neither. [INFERENCE] A dispatch-time provider probe would have caught this class before the wave; unverified that such a probe would have succeeded.

## Touched surfaces
- New: `.ufo/waves/round-17/w1/draft-lesson-mistakes.md`, `.ufo/waves/round-17/w1/DraftLessonMistakes.md`.
- Read only: lane docs at `b563c79`, round-16 wave artifacts, arc3 receipts, fleet `.ufo/reports/round-16/kaidoku.md`.
- No edits to LOG, SCORECARD, QUALITY, SKILL, SHONEN, SOURCES, PROVINCE, README, knowledge, lessons, or commits.

## Out-of-scope items for L1
- Live round-17 dispatch: `.ufo/waves/round-17/wave1-dispatch-attempts.json` records `refused: 78` at 10:25:15 and 10:28:15 and `refused: 0` at 10:31:15 (-03). Adjacent to D1-D4; not analysed further.
- Fleet report line edits (D2, D3, M2 knowledge site) belong to L1 / orchestrator; this lane cannot write them.
- The verifier's SCORECARD attribution (M3) should be dropped or re-checked by L1.

## Installs / updates
None. Tools used as present: `git` 2.56.0, `python3` 3.14.8 (stdlib), `jq` (jaq 3.1.1 on this host).

## Limits
- Red-before commands are the defect-present checks at `b563c79`. Post-fix runs require the round-17 tools, which are absent from the tree.
- The stdlib classifier is an approximation. Its counts (I3) are not contract verdicts.
- Dead-seat provider class is taken from `error` strings. No seat output and no provider call were observed.
- The M2 knowledge-site count and the I2 custody receipts are scoped to the revisions and paths cited.
