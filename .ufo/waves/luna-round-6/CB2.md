# CB2 — availability-to-holding hunt over lane-B outputs

## CLAIM
Hunted all 54 lane-B seat reports present at 19:17 (of 58 commissioned; CB6/SB1/PB1 in flight) plus 10 `receipts-B/leg-*.md` and `receipts-B/MANIFEST.txt` for holding-language upgrades — availability-class evidence (package resolves, version prints, catalog lists 207 tools, probes run) upgraded into held/Core/promotion status. None found; the boundary is explicitly enforced.

## METHOD
Lane-B set = seat-name marker + dispatch provenance (QA8.md:4,9: 58 commissioned; lane-A last 18:53, lane-B first 18:58). Read every present lane-B report (some at earlier revisions; overwrites per CB10.md:10) and receipts-B; lexicon sweep over current bytes (`held|holding|promot|Core|advance|saturat|possess|acquire|upgrade|evidence_id…LOG`), each hit checked in context. Norms: `PROVINCE.md:30-32` ("a catalog-listed tool is *available*, not *held* — ground moves to Core only after an end-to-end probe lands a `LOG.md` entry citing its `evidence_id` and subject sha256"); `P0.md:16` ("availability is not holding"). No probes or re-runs; only this file written.

## FINDINGS
1. Zero upgrades in 54/54. Held/Core/promotion mentions are denials: CB5.md:4 ("The battery measures only — nothing may be promoted to held"), :12-13 ("no promotion may land"; "no round-6 promotion exists"); PB0.md:2 ("promotes nothing"); PB2.md:4 ("no promotion claim"); XB2.md:10,16 ("No advance"); CC9.md:17 ("nothing promoted to held"); RB2.md:9 ("deny promotion").
2. All "hold(s)" tokens are truth-verbs or literal: SB2.md:2 (zero drift "holds for these four paths"); RB8.md:2 ("pinning holds"); RB7.md:2 ("all four hold"); KB1.md:2,16 ("holds nothing" = containment); CC8.md:7 ("stdin held open").
3. Strongest upward phrasing, "cross-lane agreement confirmed" (BB1.md:4; BB8.md:4), is scoped to stdout-hash reproduction; lane-B findings cut the other way: CB8.md:13,19 — legs 2/7/10 are directed replays, not blind convergence; CB1.md:16 — receipts-B trivially forgeable; CB10.md:14,21 — BB8's report↔receipt custody mismatch. ZB1.md:4,23 scores 10/10 with L10 "class-contingent": a measurement tally, not promotion. Receipts-B carry command/frames/stdout/stderr/exit/hash only.

## THREATS
Snapshot 19:17; CB6/SB1/PB1 unaudited. "Holding-language" boundary is judgment; I used PROVINCE's available≠held rule. Receipts were overwritten mid-wave (ZB1.md:26), so some reports were read at earlier revisions. Text audit only — no claims about process existence, authenticity, or re-execution (CB1/CB10 remits).

## VERDICT
CLEAN — no lane-B output upgrades availability evidence to held; promotion language absent, boundary denials explicit (CB5.md:4,13; PB2.md:4; XB2.md:10).
