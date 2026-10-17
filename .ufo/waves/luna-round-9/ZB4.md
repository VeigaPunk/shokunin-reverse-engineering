## CLAIM
Every place the round-9 dispatch steer drifted from repo state at HEAD a280e07, with each consequence. Steer text is not in-repo; recovered from seat quotes (`D1.md:5`, `D2.md:12`, `E1.md:11`, `H.md:11`, `H3.md:11`, `P0.md:8`, `P1.md:21`, `Q4.md:8`, `Z4.md:12`; `HB2.md:24` records the same limitation).

## METHOD
`git blame -L 100,117 PROVINCE.md`; reads of `PROVINCE.md:100-116`, r4-16 `:725-759`, r12-01 `:95-120`, `SCORECARD.md:74-82,455-460,494-499,555-559`, `.ufo/waves/luna-round-4/C04.md:30-36`, round-4 report `:40-46`, round-5 report `:48-67`, `.ufo/waves/luna-round-5/X1.md:30-36`, jq-shadow `:8-14,214-222,233-240`, lessons `:149-153`, `SHONEN.md:12`, `LOG.md:296,798,808-809`; tracked-file `/tmp` git-grep. Command A at a280e07: mapped 79/79, rules 9/9, coverage/depth 10.0/10.0; `git status -- PROVINCE.md` clean. No probes, network, `/tmp` access, or tracked writes.

## FINDINGS
1. **Refusal locator.** Steer cites `PROVINCE.md:107-109`; the refusal is `:114-116` and has been since seed a43d442 — blame shows `:100-116` untouched, so not a numbering shift; `:107-109` is anti-trigger/installer scope. Consequence: ≥8 seats spent verification on it, and the same stale cite sits in tracked files — `SCORECARD.md:79`, `corpus/lessons/2026-10-15-round-1.md:152` — while `SHONEN.md:12`'s bleed gate cites `PROVINCE.md:88-109`, a range ending before the refusal, so the promotion check cannot see the jq bleed (flagged r8 `RB7.md:11`; unclosed). Item 4's jq append fixes neither.
2. **Queue labeling.** `SCORECARD.md:556-558` records the carried spill as three items (r4-16 `:751-752`; census debt rounds 4-5; /tmp hygiene). Item 4 is fresh correction debt from `SCORECARD.md:77-80`; "queue closed" would mislabel it.
3. **Census naming.** Round-4's adjudicated check is F18's `v37_flagged_stale~v37_stale` matcher (`C04.md:34`; report `:43-46`); the opener-detector is round-5's README rename (report `:63-67`). "Round-4/5 opener-detector" (echoing `SCORECARD.md:458-460`) implies one instrument; `B1.md:8` says sameness is unestablished. Consequence: known-limits text may misname the round-4 matcher.
4. **/tmp premise.** No instruction/gate requires persistence (`PROVINCE.md:48` self-clean; `SKILL.md:39` never clean another session's dir). Dependence is claim-layer: `r12-01:95` held `/tmp/r4u-*` evidence; already broken — `r12-01:115-118` attributes "7 values" because receipts are gone (`LOG.md:798`); litter left by design (`LOG.md:808-809`). Instruction-scoped audit returns empty; no deletions warranted (`C3.md:9`).
5. **Bleed scope.** Steer names "benign" (`:217,:236-237`); safety language also includes "Benign payload" (`:12`) and "not binary compromise" (`:217-219`). Consequence: D2/Z4 drafts ruled incomplete (`E1.md:11`, `Q4.md:8`, `D4.md:8`, `R5.md:11`).
6. Minor: steer anchor `:751-752` is exact; `P0.md:5`'s target `r12-01:97-114` truncates `:115-118` (blocks are `:97-104`, `:110-120`).

## THREATS
Steer text reconstructed from quotes, not the original; F18 semantics read from row+report, not executed; no live `/tmp`/host checks; command A reads git objects only.

## VERDICT
FINDING: six steer-drift points; the refusal-locator drift is already embedded in tracked citations (`SCORECARD.md:79`, `lessons:152`, `SHONEN.md:12` range) and no round-9 disposition corrects them.
