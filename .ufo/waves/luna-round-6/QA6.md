# QA6 — /tmp hygiene evidence

## CLAIM
Which luna-round-6 battery receipts record cwd=/tmp, and which don't. Both sets audited: lane A `receipts/leg-1..10.md`, lane B `receipts-B/leg-1..10.md`.

## METHOD
Read-only grep/read for `cd /tmp|cwd[=:]|server_cwd|Working directory` in both dirs. No re-runs, no MCP started, no config edits, lane-A receipts read only as evidence (never for output). Snapshot: 2026-10-16 19:04:31 -03:00; receipts-B still in flight.

## FINDINGS
Lane A — all 10 record cwd=/tmp:
- Explicit `Working directory: /tmp` field: `receipts/leg-1.md:4`, `leg-3.md:4`, `leg-4.md:5`, `leg-5.md:4` (1/3/5 also embed `cd /tmp &&`).
- `cd /tmp &&` in command text only: `leg-2.md:1`, `leg-6.md:3`, `leg-7.md:3`, `leg-8.md:3`.
- Narrative forms: `leg-9.md:1` ("From /tmp"), `leg-10.md:3` ("(cwd=/tmp)").

Lane B — 4 of 10 literal /tmp:
- Literal: `receipts-B/leg-4.md:9,33` (`server_cwd: /tmp`), `leg-6.md:8,11`, `leg-7.md:10`, `leg-10.md:9`.
- Record `/tmp/<seat-dir>` instead: `leg-1.md:9` (/tmp/rea-bb1), `leg-2.md:1` (cwd=/tmp/rea-bb2), `leg-3.md:4,36` (cwd=/tmp/rea-bb3), `leg-5.md:13-14` (/tmp/rea-bb5), `leg-8.md:4,26,51` (/tmp/rea-cc8), `leg-9.md:13` (/tmp/rea-bb9).

No receipt omits a cwd claim; none claims a repo/home cwd. Non-leg artifacts: `receipts/MANIFEST.txt` hashes only leg-1.md; `census-pre.txt` carries python `cwd=` kwargs (git), not a probe record; `census-laneB-pre.txt` (XB1, 19:04) has no cwd claim.

## THREATS
cwd is self-reported command text; `grep -rnw pwd` over both dirs = 0 hits, so no instrumented `pwd` witness exists anywhere. receipts-B was mid-write: leg-8 changed at 19:03:24 (earlier version showed `cd /tmp`), `census-laneB-pre.txt` appeared at 19:04:24; later edits are unclassified. Whether `/tmp/<seat-dir>` satisfies "from /tmp only" is protocol interpretation, not measurable from text.

## VERDICT
FINDING: lane A 10/10 record cwd=/tmp; lane B 4/10 literal (4,6,7,10) and 6/10 record /tmp/rea-<seat> subdirs (1,2,3,5,8,9).
