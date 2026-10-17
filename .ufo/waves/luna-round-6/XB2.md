## CLAIM
Are SH1's and RE4's Box-3 ("Instructions executable by an agent without oral context") discussions sound, and is any SHONEN advance defensible under the fleet promotion rule?

## METHOD
Documentary read of `SH1.md`, `RE4.md`, `SHONEN.md`, `SCORECARD.md:86-141`, `SKILL.md:42-80,197-206`, `corpus/lessons/2026-10-15-round-1.md:87-109`, and fleet `PROTOCOL.md:59-73,433-435` (repo-root copy vs skill-protocol copy: `diff -q` IDENTICAL). Resolved every cited range. Read `receipts/leg-1.md` and `XA.md`; listed `receipts/` and `receipts-B/`. No probes, no MCP servers, no config edits; did not run or replay any battery leg.

## FINDINGS
- **SH1 sound.** `SHONEN.md:9-10` shows box 3 `[~]` with author assertion only. `PROTOCOL.md:63-68` requires a reviewer who did not author the changes, and states a lane-dispatched subagent is still the lane; `:433-435` reserves `[x]` for a named non-author verifier. All SH1 cites resolve (lesson `:87-109` = open→inspect→export→close; scorecard `:86-141` = runnable recipes A/B). Its self-exclusion (`SH1.md:10`) follows the gate text.
- **RE4 conclusion sound; premise stale.** `RE4.md:10` says "one receipt, not ten" — `receipts/leg-1..10.md` now exist. But the disqualifiers are provenance and durability, not count: the battery recipes live in the parent dispatch, while box 3 gates on `SKILL.md`/`corpus/` self-containment (`PROTOCOL.md:71-73`). SKILL.md lists 6.5.0/207 surfaces (`SKILL.md:19-20`) but no battery runbook; corpus records `tools/list` as NOT run (`corpus/knowledge/2026-10-13-rea-cli-surface.md:84`).
- **No advance.** Neither report writes `[x]` or LOG.md; the round pre-commits "the battery MEASURES; nothing gets promoted"; no named non-author verifier exists. Additionally `XA.md:9,12` finds the manifest incomplete, L9's raw-process digest unverifiable, and receipt overwrites — so completeness would not equal clean verification.

## THREATS
RE4's snapshot ("only `leg-1`") is not retroactively verifiable (RE4 mtime 18:19:20 vs leg-2 mtime 18:19; ordering unknown). Whether this wave's lane B could ever count as "a fresh lane" depends on dispatch provenance not resolvable wave-internally; SH1 handles this correctly by self-excluding. Secondary cites (PS4, EX1, XG2, SC2/SC5) were range-checked, not semantics-audited.

## VERDICT
CLEAN: Box-3 discussion in SH1 and RE4 is sound; no advance defensible under the fleet rule.
