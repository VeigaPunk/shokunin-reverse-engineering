## CLAIM
Disposition gate: every arc defect (rounds 1–9 plus round-10 notes) carries exactly one disposition. The register is 1:1 except four orphan sets, one conflicting filing, and one undispositioned citation erratum.

## METHOD
Read rounds 1–9 reports and the round-10 D/K/N/P/S/X/Y notes. HEAD is `c343939`, one commit past the D-seats' `6e83a20` anchor; `git show --numstat c343939` = 28 insertions, 0 deletions (additive scaffolds, no rewrite). Exact: `sha256sum .ufo/waves/luna-round-2/receipts/L7-mcp-tools-6.5.0.txt L5-help.txt` → `dc740c46…` / `224965bad…`; `python3` json enumeration of `MANIFEST.json`, lane=kaidoku → 13 rows, 44 verdict values, 10 non-enum; `find .ufo/interactive-sessions -type f | wc -l` → 4, still untracked (`git status`). Read-only sibling reads: `tameshi-shokunin/corpus/knowledge/verification-patterns-fleet.md:35,73,102`, `.../corpus/README.md:9`, `tsukuroi-shokunin/PROVINCE.md:42,70-71`.

## FINDINGS
Orphans (zero disposition, by the wave's own words):
1. Historical `/tmp` verify-recipe citations + L7-01 cold-cache (`SCORECARD.md:593-598`) — SCORECARD labels them "archival debt"/"untested", yet `D3.md:10` and `D4.md:9` say these "have no disposition". Vocabulary split; unresolved either way.
2. Four untracked `.ufo/interactive-sessions/` files (`.ufo/waves/luna-round-9/GB5.md:11`; `D4.md:9`).
3. Unattributable pre-existing `/tmp/probe*.log` (`GB5.md:12`; `D4.md:9`).
4. R8 leg-3 pre-repair `/tmp` audit copy (round-8 report:42-44; `GB5.md:14`) — "survives for audit", no disposition line.

Conflict (two dispositions): `D4.md:8` files census instrument limits under "**Closed:**"; `SCORECARD.md:576` plus `D3.md:10`/`D5.md:10` carry them "ADJUDICATED, not PASS" with a repair/retest trigger.

Erratum: `D5.md:9` misquotes B2 — `B2.md:9` is the L5 line (its `224965bad…` hash matches); the `a910c6…` L7 claim is `B2.md:10`, mismatched against `dc740c46…` (no round-2 receipt hashes `a910c6`). The B2 defect itself is single-disposition (carried; round-2 report:65-66); the misquote needs its own erratum line.

Cleared 1:1: Tameshi's stale universal formula (route to its owner only; bytes re-resolve at the pinned sibling state), tsukuroi ADJ-06 (integrator only; sibling text verbatim), `SCORECARD.md:68-72` (explicit in-file partition: pointer corrected / content carried — not a double), R6 127/128 plus five short-counts (one retained process defect), R8 pre-pair, SHONEN 4×`[~]`. MANIFEST prose values hold one disposition (criterion defect; no closed-row rewrite), but "six values in five rows" is window-scoped: lane-wide it is 10 non-enum values, four leading with `verified` (rounds 2–4).

## THREATS
D4 raced D1–D3 and D6 raced D4 (`D4.md:1-2`; `D6.md:5`), so the orphan list is as of landed notes. `/tmp` liveness unprobed. Untracked receipts: provenance unknowable; "stale" means mismatch against today's bytes only.

## VERDICT
FINDING: register 1:1 except four orphan sets (session files, probe logs, `/tmp` archival residuals, R8 audit copy), census limits filed Closed vs carried, and the `D5.md:9` B2 misquote — closeout must assign each exactly once.
