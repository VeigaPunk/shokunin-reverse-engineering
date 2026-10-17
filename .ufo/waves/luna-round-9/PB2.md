## CLAIM
Independent LOG/SCORECARD drafts for luna-round-9's four carried freshness items, built from primary receipts, not P2; diffed against P2. No tracked file changed.

## METHOD
Read `LOG.md:751-782,835-858` and `SCORECARD.md:417-465,534-559` (house format); the four source loci (`corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:750-754`, `2026-10-14-r12-01-queue-b-ready.md:99-120`, `2026-10-13-r2-jq-shadow-verdict.md:217,236-237`, `PROVINCE.md:114-116`); round-9 receipts Z1/Z2/Z4, G2-G4, T1, H4, R6, C1, S1, X4, X5, Z5. Re-ran command A (`SCORECARD.md:92-123`) at HEAD `a280e07`: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "a280e07133f52f719b0805fc73c0b997e77b5062", "rule_blocks": 9}`; `git diff --quiet HEAD --` → clean. Otherwise text-only.

## FINDINGS
**Draft LOG entry** (house format; `[sha]`/wave counts pending landing):
> ### luna-round-9 — freshness: carried-spill queue
> - Motivating evidence: round-5 BB1 flag (`r4-16:751-752`); rounds-4/5 census instrument debt (`SCORECARD.md:458-460`); `/tmp` hygiene question (`SCORECARD.md:556-559`).
> - Work: (1) short append-only cross-reference in r4-16 — pointer to `r12-01:99-104,110-120`, four sites, "7 values" attributed, no r4-16-supersession claim; (2) `SCORECARD.md` known-census-instrument-limits note (X4 ruling `X4.md:8-11`; comma-token SIZES + opener/F18 breadth; descriptive, not a waiver — B3/H4); (3) `/tmp` audit: no current instruction/gate/recheck requires pre-existing `/tmp` (`C1.md:2`; Q3/R3/Z3); `corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md:5` npm-cache necessity unproven (`S1.md:2`); cleanup operator-owned, nothing deleted; (4) jq-shadow append disavowing safety/trust/reuse for "benign," covering `:217-219,236-237` (D3/Z4/H4).
> - Landed at `[sha]`; measured at `[sha]`: command A 79/79, 9/9, 10.0/10.0; token set 79 unchanged (G3); non-target tracked paths byte-identical (G4 allowlist); PROVINCE untouched.

**Draft SCORECARD section** `## luna-round-9 — freshness: carried-spill queue, 2026-10-16`: claim = four append-only dispositions, no deletion; wave bullet `[parent]`; freshness verdict conditional on post-landing evidence — `improved` inadmissible from proposed text alone (Z5:13; `H1.md:2`); coverage/depth/calibration `unchanged` at the re-run invariant; `Planned next: luna-round-10` (X5); `Retired: none`; residuals: F3/R6 omitted debt, SHONEN `[~]`×4 unpromoted (X1).

**Diff vs P2** (`P2.md`): (1) `P2:12` leaves the item-2 home open (`SCORECARD.md` vs `QUALITY.md`); X4/X2 now rule SCORECARD. (2) `P2:13` item-3 placeholder; the audit result exists (C1/S1/Q3/R3/Z3). (3) `P2:14` keeps a scoped "benign"; D3/Z5 prefer explicit disavowal, and P2 omits `:219` (H4). (4) `P2:12,17` lack the B3/H4 guard; the draft omits the table and closing lines. (5) `P2:17` pre-states "four queue items dispositioned" before landing; this draft keeps the verdict conditional. Item-1 wording and the `:114-116` cite converge.

## THREATS
Wave counts unverified (X3 snapshot: 4 lane-A reports). Post-landing sha, command-A rerun, byte-identity, item-4 final wording, and F3/R6 residuals are parent decisions. No probes, network, `/tmp` access, or deletions.

## VERDICT
FINDING: independent drafts and five-point diff delivered; landings, wordings, and post-landing measurements all remain pending.
