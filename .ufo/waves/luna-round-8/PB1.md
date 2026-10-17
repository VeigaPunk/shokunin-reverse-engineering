# PB1 — lane-B summary (paragraph for the round report)

## CLAIM
Lane-B summary paragraph for the luna-round-8 round report; quiescence snapshot 21:36 -0300. Read-only elsewhere; only this file written.

## METHOD
Polled the wave dir to quiet (last peer write CB5.md 21:35:13; 240 s quiet). Read all 47 landed lane-B peers, the leg receipts, MANIFEST.txt and census-pre.txt. Own spot-checks: MANIFEST recompute via `sha256sum` (9/10 OK; leg-10 `6cd389e9…` ≠ claimed `c89eea7a…`); `head -n 59 leg-10.md | sha256sum` = `c89eea7a…`; leg-3 stdout block 623 B = claim `5c682099…` = `/tmp` raw; `wc -l leg-2-tools.txt` = 170 with the six verbs absent; Command A verbatim at `6e2ee8f` → 78/78, 9/9, 10.0.

## FINDINGS
**Paragraph:** Lane B (deepseek-v4.1-flash; 47 peers incl. PB2's records drafts, 25 CLEAN / 22 FINDING) was the round's receipt-level verification layer over lane A's pre-registered 6.4.0 SYMMETRY battery, re-deriving results without re-running REA. Custody held: all ten legs' displayed stdout blocks recompute to their claims (`VB1.md`, `FB2.md`, `HB1.md`), 9/10 whole-file hashes match `MANIFEST.txt` (`VB5.md`; PB1 recomputed), the 170-name list recounts with the six 6.5-only verbs absent (`HB2.md`), leg-9's six absences corroborate round-2's A6 list (`CB6.md`), and all six refusals are one schema-level class, `-32602 Tool <name> not found` (`VB7.md`). Independent scorers reproduce 10/10 (`RB1.md`, `PB0.md`, `CB5.md`); L10's RESULT criteria pass (`CB8.md`); the pending 78→79 entry rehearses to 79/79·9/9·10.0 in scratch stores (`QB2.md`, `RB8.md`). Guards: Command A replays 78/78·9/9·10.0, token `c6c025f3…` (`TB1.md`), tracked tree frozen at `6e2ee8f` (`CB4.md`, `SB4.md`), config sentinels matched with no pre/post pair (`SB2.md`), host process-clean (`SB3.md`), no sibling battery (`KB1.md`). Defects were adjudicated, not hidden: ten stale absent/unscored verdicts superseded (`VB6.md`, `ZB1.md`); `leg-10.md` was appended after MANIFEST/census, so its whole-file hash is stale (`VB5.md`, `RB2.md`); `census-pre.txt:97` carries a pre-repair legs-3–4 snapshot (`RB4.md`, `CB3.md`); the briefed leg-3 corruption is already repaired — current block = claim = `/tmp` raw (`ZB3.md`, `VB2.md`); disk holds 52 lane-A report files, not 64 (`FB1.md`, `ZB4.md`). Parent-owned: MANIFEST/census refresh, the 78→79 entry decision, SHONEN `[~]`×4 (`RB7.md`, `ZB2.md`).

## THREATS
Attribution by seat-name family and self-labels; dispatch roster not visible. Peers stayed mutable after snapshot (CB5 rewritten 21:35:13); hashes prove stored bytes, not re-execution; `/tmp` checks are best-effort; lane-A files beyond spot-checks were not re-audited.

## VERDICT
CLEAN — paragraph delivered; 47 peers triaged; four own spot-checks reproduced key claims and defects; only this file written.
