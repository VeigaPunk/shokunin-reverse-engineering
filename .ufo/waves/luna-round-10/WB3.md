## CLAIM
Re-audit seat W2's finding on kaidoku luna-round-2 records commit `a9580eb`: does its `SCORECARD.md` diff replace 8 pre-existing lines, breaking the arc's "LOG+SCORECARD appended, never rewritten" criterion?

## METHOD
`git diff --numstat 75af886 a9580eb` → `60 8 SCORECARD.md`. Per-hunk counts on the saved diff: `-22,7` 1del/1add; `-53,13` 7del/5add; `-268,3 +266,57` 0del/54add. Authorship via `git blame -L 25,25 75af886 -- SCORECARD.md` and `-L 56,62`. Independent replay of command A (`SCORECARD.md:91-123`) at `75af886` and `a9580eb`; same recipe at `2abd30f`/`6e83a20`/`c343939`. Round-1 records diff `a79945c..a4bd355` compared. Read `.ufo/waves/luna-round-2/F6.md`, `LOG.md:653-681`, `.ufo/reports/luna-round-2/kaidoku.md`, PROTOCOL.md:351-352,420,447, AXES.md:77-83. Git read-only; no live probes, no network.

## FINDINGS
CONFIRMED byte-exact: the 8 deleted lines are the calibration row (old `:25`) and the 7-line Version-drift bullet (old `:56-62`), replaced by 6 lines; the other 54 additions are a clean EOF append. W2's citation `SCORECARD.md:25,56-60` is exact for the post-image; pre-image the bullet is `:56-62`, as round-2 seat `.ufo/waves/luna-round-2/F6.md:10` itself cites. Deleted lines were pre-existing, authored `c265db9b` (2026-10-15). Net −2 lines: dropped "The lesson preserves the observed status excerpt; this status call supplies no Evidence ID." — that fact survives at `corpus/lessons/2026-10-15-round-1.md:58`; the guard phrase "failure-selected completeness" was retained.

Not a round-2 anomaly: round-1 records `a4bd355` also rewrote pre-existing rows (numstat `40 4` vs `a79945c`: old `:20` coverage row, old `:52-54` Coverage-map bullet). Living-row updates fit SCORECARD's contract ("last-change round", PROTOCOL.md:420; AXES.md:77-83), and PROTOCOL.md:447's append-only rule names LOG only — so whether the goal criterion forbade living-row edits is parent adjudication; I could not locate the quoted criterion verbatim in-repo.

Unexcused: no disclosure. `LOG.md:653-681` names SCORECARD only as the gap's source; report `:39` lists SCORECARD.md as a bookkeeping file; nothing names the superseded text (PROTOCOL.md:351-352 norm).

My command-A replay at `75af886` reproduced W2's JSON exactly: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 72, "mapped": 72, "missing": [], "rule_blocks": 9}`. Report headings verified at `:8,:36,:43,:55,:70,:80`; seat census 64 (B5,F7,G9,L15,R9,S5-sentinel). Brief drift: actual HEAD is `c343939` (2026-10-16 22:42, pure append 0/12), not `6e83a20`.

## THREATS
Criterion provenance unverified in-repo; deleted-line counts measure form, not information loss. F6 is untracked wave litter, admissible only as an in-repo artifact. Dispatch telemetry not checked; no seat-file provenance claim made.

## VERDICT
FINDING: W2 confirmed — `a9580eb` deletes 8 pre-existing SCORECARD lines (two living-row rewrites) with no named correction; the same pattern opens in round 1 (`a4bd355`), so adjudicate arc-wide, not per-round.
