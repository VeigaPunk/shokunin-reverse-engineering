# WB5 — enum-adjudicator: six prose-decorated MANIFEST verdicts

## CLAIM
Adjudicate the six prose-decorated MANIFEST verdicts: exact disposition options (append correction row? report-note only?) with fleet-ledger precedent.

## METHOD
Read-only. Enumerated all 260 verdict fields in `../MANIFEST.json` (python json); provenance via `git log -S`. Read `PROTOCOL.md:230-310,440-455`, shokunin `SKILL.md:77-78`, wave seats `A2.md:7,15`/`P0.md:5`, `SCORECARD.md:74-76`, `.ufo/history-pin.json`. No probes/network.

## FINDINGS
- Confirmed: six decorated fields in five kaidoku train rows — `MANIFEST.json:2791,2805,2819,2846,2847,2860` (luna 4/5/6/8/9; freshness x3, operability x2, coverage x1). Leading tokens are exact enums; prose follows.
- Fleet-wide non-bare population is 10, all kaidoku: +4 pre-arc at `:1509` (`improved (audit queued…)`), `:1522,:1535,:1548` (`verified (…)`, non-enum token). All ten authored by integrator `ci <ci@local>` in the closure commits (c03d38b, 43c204f, d803c05, ae734c7, f2366e1), not the lane.
- Criterion: `P0.md:5` demands "exact enum verdicts"; vocabulary `improved | harmed | unchanged | unprovable-but-better` (`SKILL.md:77-78`). 250/260 values bare; no code consumer of MANIFEST verdicts found (grep `.py/.sh/.js`, parent + kaidoku).
- Append precedent: `PROTOCOL.md:299-305` — corrections are appended `closure-correction` rows (`supersedes {round,type,date}`), never in-place. 50 precedents (all 2026-09-28/29; targets work 3 / retroactive-closure 4 / closure 23 / closure-correction 20; 38/50 carry `entry`), but none targets a `train` row, none carries `verdicts` — first-of-kind. Triple {round,"train","2026-10-16"} unique for rounds 8,9,10,12,13 (count=1; `entry` unnecessary). Appends are integrator-of-record scope (`PROTOCOL.md:452`).
- Report-note precedent: the arc recorded five short-counts and other defects in notes/reports, never retro-corrected; `SCORECARD.md:74-76`: ledger slips are "fleet-owned; this lane does not alter them". Aggregator routed-defect ledger is the durable queue (`PROTOCOL.md:230-233`).

## THREATS
- A correction targeting a train row drops from `type=="train"` audits (`A2.md:7`) and last-wins consumers unless a `verdicts` key is added (annotation keys allowed, `PROTOCOL.md:241`; precedent-less).
- Rows 9/10/12/13 notes do not restate the "fleet axis / unowned proxy" ruling; prose cannot be dropped without displacement into notes.
- No gate parses verdicts → documentation-level; a lenient reading (leading token exact) may be ruled compliant.
- `.ufo/history-pin.json` pins entries 0-47 only, so an in-place edit would evade the pin — the bar is the rule (`PROTOCOL.md:299,307-310`), not the pin.

## VERDICT
FINDING: six confirmed (five rows, integrator-authored). Options: (a) report-note/debt-row only — lane-legal, arc-precedented; (b) strict fix = integrator-appended closure-correction per `PROTOCOL.md:299` with prose displaced to notes (first-of-kind for train rows; breaks type-filtered counts); in-place rewrite barred. Recommend (a) plus forward-fix at round-10 closure.
