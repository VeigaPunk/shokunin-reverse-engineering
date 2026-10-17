## CLAIM
Disposition of revenger's open UNKNOWN (`../revenger-shokunin/reports/round-1/connector.md:51`): kaidoku owes one PROVINCE scope note (exact text below) — not an L0 entry, no debt beyond it. The drift is already partially realized, so the note is due now; it is census-neutral.

## METHOD
Read connector.md in full; kaidoku PROVINCE.md (worktree byte-identical to HEAD cfc84c2, `cmp`), SCORECARD.md:285-315, corpus/README.md, LOG.md; revenger r57 receipt/LEDGER, README, brief; fleet MISSION.md:89-93, PROTOCOL.md:504-510, PROTOCOL-APPENDIX.md:39, `.ufo/l0-questions.md`; wave KB1.md and receipts/census-pre.sh. Reads only; no probes, no repo writes.

## FINDINGS
- **Drift is not hypothetical.** Kaidoku's own map already spans versions — Devin/OMP `rea-agents@6.5.0`, Kimi `6.4.0` (`PROVINCE.md:8-24`, "Drift-prone values: reverified 2026-10-16"; receipted `SCORECARD.md:288-304`). Sibling r55-r57 receipts freeze `npx -y rea-agents@6.4.0 inspect-pe-resources …` (`../revenger-shokunin/corpus/live/runs/round-57/receipt.json`).
- **Revenger already states the route** (`connector.md:25`: drift = "a kaidoku surface-map refresh (`rea doctor` verdict), never a license to re-pin the historical receipt command or to claim current runtime capability"; `:33-36`: ledger semantics live only in the lane's LEDGER/LOG/receipts). Kaidoku's half is implicit only: `PROVINCE.md:61-64` says the map is refreshed each round, not that it is no identity authority.
- **L0 is the wrong instrument.** `MISSION.md:89-93`: L0 is for questions the operator answers; no operator action is reachable here — replay is a byte-ledger check, never a producer rerun (`connector.md:35`; revenger `brief.md:7`), so live drift cannot invalidate a saved receipt. The fleet ledger has zero kaidoku/revenger lines and no 6.4.0 mention; durability is a known hazard (`PROTOCOL-APPENDIX.md:39`); the kengaku fleet-standard precedent (`l0-questions.md:7`) needs a second lane freezing receipts — only one exists.
- **Owed text** — append same-physical-line to `PROVINCE.md:64` after `each round.` (zero line drift; a new line stales `SCORECARD.md:45,79` / `SHONEN.md:12`; cf. `DB3.md:12`): "Map entries are live state only: a version drift past 6.4.0 is refreshed here, never re-bases a sibling lane's frozen receipt command or historical artifact path, and never stands for that lane's current runtime capability (routing: `../revenger-shokunin/reports/round-1/connector.md:25,33-36`)."
- **Census-neutral:** `receipts/census-pre.sh:25` PIN tokens sit at :32; `:35-40` read README/SKILL only. If deferred, this text is named debt for kaidoku's next round; a fleet-wide standard stays an integrator option, not owed.

## THREATS
Reads at HEAD cfc84c2 (PROVINCE identical to HEAD; tree otherwise only untracked `.ufo/waves`, `.ufo/interactive-sessions`). No sibling file touched; the note's placement is independent of the pending module-identity insert at :32.

## VERDICT
FINDING: kaidoku owes the `PROVINCE.md:64` scope note (text above) — not an L0 entry, no debt beyond it.
