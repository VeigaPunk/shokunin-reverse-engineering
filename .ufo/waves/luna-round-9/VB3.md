## CLAIM
Item-3 verification: no CURRENT kaidoku gate or instruction requires pre-existing `/tmp` content to persist, and the hygiene proposal (C2) authorizes no lane/unilateral deletion. Tested independently against primary texts, not peer reports.

## METHOD
Read-only audit at HEAD `a280e07`: root controls (`AGENTS.md`, `PROVINCE.md`, `SKILL.md`, `MINT.md`, `README.md`, `SHONEN.md`, `corpus/QUALITY.md`); gate registry (`SKILL.md:242-251`) and full `verify-recovery.py`; SCORECARD recipes A/B (`:88-142`); all 7 `recheck:` fields vs 468 inline `verify:` bullets; greps of `.ufo/rounds`, `.ufo/continuation`, `evidence/`. Ran read-only: Command A at REV=`a280e07133f52f719b0805fc73c0b997e77b5062`; gate normal entry. No `/tmp` inspection, network, or writes outside this file.

## FINDINGS
- Command A reproduced byte-exact: mapped 79/79, `citation_resolved_rules` 9/9, coverage 10.0, depth 10.0, `missing`/`dangling` empty — inputs are Git objects only (`SCORECARD.md:92-123`); no `/tmp`.
- Gate normal entry: `RECOVERY_EVIDENCE: CLEAN ... exit=0`. It hashes repo-relative pinned snapshots (`verify-recovery.py:12-15,67-87`); selftest fixture is under `HERE` (repo), not `/tmp` (`:123`).
- Current `recheck:` fields: 7, all l7/l8 (2026-10-16). Four use `/tmp` only as cwd; L7-01 also names read-through cache `/tmp/kaidoku-luna-round-6-npm-cache` (`2026-10-16-l7-01-inspect-go-binary.md:5`) — an absent cache forces refetch, not failure; offline behavior untested. No recheck cites a must-persist `/tmp` artifact; the others use pinned host paths or copy the pnpm store file.
- 468 historical inline `verify:` recipes consume round-era `/tmp` files (e.g. `2026-10-13-r3-renderer-asar.md:11,19,35`); archival provenance, superseded by tracked receipts (`LOG.md:798`; `SCORECARD.md:497`).
- Hygiene: C2 (`:10`) keeps deletion operator-only, exact-path, manual, post-close-state; its figures verified (SB1: 43 entries ≈1.2 GB, 7 dirs unattributed; SB3: 59-entry ≈1.21 GiB floor). No round-9 draft proposes deletion (spot-check concurs with CB6); `git diff --quiet HEAD` clean; PROVINCE worktree = HEAD blob `8a1cec88…`.

## THREATS
`/tmp` never inspected (round constraint): current existence of historical artifacts and cache state unverified; no live recheck or offline replay. "Current vs historical" recipe split is inferred from the field convention (`LOG.md:820`), not a written policy line — a reader treating a `verify:` bullet as live would inherit `/tmp`-input dependencies. Snapshot: lane-B files were still landing (VB4.md appeared mid-audit).

## VERDICT
CLEAN — no current gate/instruction requires `/tmp` persistence; L7-01's cache is the sole soft, untested candidate; cleanup remains operator-owned.
