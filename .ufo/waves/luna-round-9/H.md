## CLAIM
Adjudicate the four carried freshness disputes at HEAD `a280e07133f52f719b0805fc73c0b997e77b5062`; no source edits or cleanup.

## METHOD
Read the primary corpus, round-4/5 reports, current lane instructions/gate/rechecks, and adversary receipts. `git rev-parse HEAD` → `a280e07133f52f719b0805fc73c0b997e77b5062`. Static review only; G2 independently records Command A = 79/79, 9/9, 10.0/10.0 (`.ufo/waves/luna-round-9/G2.md:5-10`).

## FINDINGS
1. **Stale L197 account: stands.** `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:751-753` names two varying fields; `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:99-104,110-120` corrects this to four sites and attributes—not re-derives—“7 values.” A cross-reference from r4-16 is warranted. A3’s caution stands: the r12-01 erratum says it supersedes its own main text (:112-114), not r4-16; preserve historical text and avoid claiming otherwise (`.ufo/waves/luna-round-9/A3.md:8-10`).
2. **Census limits: stand.** F18’s predicate is structurally unsatisfiable despite stale wording being absent (`.ufo/reports/luna-round-4/kaidoku.md:43-46`); round 5 documents comma-token SIZES mismatch and the README opener matcher catching retained wording (`.ufo/reports/luna-round-5/kaidoku.md:50-56,63-67`). These are instrument limits, not corpus defects; record them, with the home left to X4 (`SCORECARD.md:458-460`).
3. **`/tmp`: no retained-litter dependency proven; cleanup remains operator-owned.** SKILL describes shared ephemeral sessions and forbids cleaning another session (`SKILL.md:39-40`); PROVINCE says Ghidra scratch self-cleans (`PROVINCE.md:48`). Command A reads Git objects (`SCORECARD.md:88-123`); the recovery gate’s temporary fixture is under `HERE`, not `/tmp` (`.ufo/rounds/interactive-r1/verify-recovery.py:120-129`). Current rechecks run from `/tmp` (`corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md:5`, `corpus/knowledge/2026-10-16-l7-03-inspect-electron-fuses.md:5`, `corpus/knowledge/2026-10-16-l7-05-search-bytes.md:5`, `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:5`); L7-01 names an npm cache there. Whether that cache must pre-exist is unverified.
4. **jq wording bleed: stands, with D3’s qualification warning.** R2 calls the payload “benign” and “not binary compromise” (`corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:217-219,236-237`), but the safety/trust refusal is at `PROVINCE.md:114-116` (prompt’s :107-109 is not that rule). Append-only text must tie the historical word only to recorded byte identity and explicitly disclaim safety/trust/reuse; avoid leaving an ambiguous endorsement (`.ufo/waves/luna-round-9/D3.md:8-10`).

## THREATS
No `/tmp` access, live probes, network, or independent re-derivation of “7 values” or cache behavior. This is a static adjudication; no tracked file was changed.

## VERDICT
FINDING: disputes 1, 2, and 4 are substantiated; 3 has no proven persistent-input dependency, but its named `/tmp` cache and any cleanup decision remain unresolved/operator-owned.
