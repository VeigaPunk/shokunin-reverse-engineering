# FB1 — lane-A report format audit (five headings)

## CLAIM
Every lane-A report of luna-round-8 carries exactly the five required sections — `## CLAIM`, `## METHOD`, `## FINDINGS`, `## THREATS`, `## VERDICT` — in that order, once each, with no other `## ` headings, and a one-line verdict beginning `CLEAN` or `FINDING:`. Round context's "64 lane-A reports" is reconciled against the actual set.

## METHOD
Read-only; snapshot 2026-10-16 21:27:04 (-03). Lane-A set = the 52 non-`*B<digits>.md` seat files in `.ufo/waves/luna-round-8/` (mtimes 20:52:40–21:10:32, all before the first lane-B report `CB4.md` 21:17:42). Python check per file: `[l for l in lines if l.startswith('## ')] == ['## CLAIM','## METHOD','## FINDINGS','## THREATS','## VERDICT']` — one comparison enforcing presence, exact text, order, uniqueness, and rejecting extra `## ` headings — plus first non-blank line after `## VERDICT` starts `CLEAN`/`FINDING:`, plus no `\r` bytes. Roster cross-check: parent's own dispatch batch in session wire `…/agents/main/wire.jsonl` record 4188 = 52 items (`P0 K1 X1 EX1–EX10 RV1–RV8 PS1–PS4 CA1–CA10 RE1–RE6 SE1–SE4 PR1 PR2 CE1 CE2 SH1 XG1 XG2`; first item "P0 planner | Round-8 integration plan…"). Aggregate over sorted `sha256␣␣name` lines of the audited set: `eb875aba0bbdce243b88f3791ac2016d5b509251fae6aba3ef55a3105e6eadee`.

## FINDINGS
52/52 pass every check; 0 failures. Verdict lines: 19 `CLEAN*`, 33 `FINDING:*`. The landed 52 reports are exactly the 52 seats of the parent's lane-A dispatch batch — no lane-A report is missing. The round context's "64" matches the standing 64-seat-per-lane wave format, not this round's lane-A batch, so it is not a 12-report deficit.

## THREATS
Scope = seat reports in the wave dir; `receipts/leg-*` are FB2's subject and were not audited here. Lane-B reports (B-infix names, still accumulating as of write time) are excluded and their heading compliance is unverified by this seat. The check is structural only (no content or word-count judgement). If the parent's roster differs from the session-wire batch, re-run the comparison and diff the aggregate hash. The wave dir is append-only: any later-landing non-B-named file falls outside this snapshot.

## VERDICT
CLEAN — 52/52 lane-A reports carry the five required headings, exactly and in order, with well-formed verdict lines; the count is 52 (dispatch roster), not 64.
