# QualityRow — draft QUALITY.md rows for round-26 routed defects 2 and 4

Seat KaidokuR27.QualityRow (scribe). 2026-10-22. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
base `cd32264f7ee356a9c0f48bd8e3fcdac222db22a0`, tip `a4f674b3`. Read-only on the lane: no lane file was
edited except this seat report (the wave-1 report path the L1 assigned); no git write, no jj, no REA call,
no install. Next free row numbers after the last row (37) are 38 and 39.

## Drafted rows (verbatim, ready for `corpus/QUALITY.md`)

Row 38 — instrument with red fixtures before the data, refusing data older than itself:

```
| 38 | A round's counting instrument is committed, with its red fixtures and its before receipt, before the data it counts: the instrument's own commit time is no later than the first commit of every envelope and evidence file it measures, and the instrument itself refuses any run that started, and any evidence file that was first committed, earlier than that commit. The instrument's red fixtures ship in the same commit as the instrument and before the data, so a later data commit cannot invent the oracle. Fails when the instrument or its selftest is first committed after the data it counts, when the instrument has no rule that refuses pre-instrument data, or when the red fixtures first appear after the data. Round-26 case, judged by this row: R26-C1's data commit `ebe2cb4a` (committer 2026-10-22T09:47:57-03:00) precedes the instrument commit `bd0c84bc` (2026-10-22T09:49:24-03:00), and that same commit carries the after receipt and the selftest; `tools/round-26/c1-id-identity.py` contains no `utc_start` comparison and never reads `runs.tsv`, so it cannot refuse pre-instrument data; `corpus/claim-freezes.tsv` row `round-26` reads `FLAGGED INSTRUMENT_ABSENT`. Round-27 case, judged by this row: at `a4f674b3` (2026-10-22T11:51:23-03:00) both counters, both red selftest receipts and both before receipts are committed with no `corpus/evidence/round-27` file present, and `tools/round-27/c1-rename-identity.py` refuses a run whose `utc_start` is earlier than the counter's own commit and an envelope first committed earlier than it, with the committed red case `run-before-counter` firing. | `corpus/lessons/round-26-verifier-spotcheck.md:201-204` (routed defect 2); `corpus/claim-freezes.tsv` row `round-26`; `corpus/lessons/round-24.md` M24-1 | sharpens 33 (row 33 orders instruments before the claims file but is silent on data order, on red fixtures, and on refusing data older than the instrument) |
```

Row 39 — the call record names the resolved package version and package.json sha256 per call:

```
| 39 | Every REA call record — the per-run `runs.tsv` row and the envelope it names — names the resolved package version and the sha256 of that package's own `package.json`, per call; a claim's tool pin is carried by the record of the call that produced the evidence, not by the frozen invocation alone. The counting instrument rejects any run whose recorded version or `package.json` sha256 differs from the pin the claim names, and the red fixtures that show that rejection are committed before the data. Fails when the call record has no version or `package.json` sha256 column, when the recorded digest is not the resolved package's own `package.json` digest, or when the instrument never reads those columns. Round-26 case, judged by this row: `corpus/evidence/round-26/c1/runs.tsv` at `ae8bcd86` has 11 columns (`seat` to `subject_sha256`) and no version column, the 24 envelopes carry no version string, and `tools/round-26/c1-id-identity.py` never reads `runs.tsv`, so the 6.5.0 pin rests on the frozen invocation and the id-rule fit. Round-27 case, judged by this row: `tools/round-27/c1-rename-identity.py` freezes the header with `pkg_version` and `pkg_json_sha256`, rejects a run whose values differ from `6.5.0` and `a5003023…50a6c`, and its committed red cases `package-version` and `package-json-sha` fire exit 1; the installed 6.5.0 `package.json` re-measures to `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`. | `corpus/lessons/round-26-verifier-spotcheck.md:208-209` (routed defect 4); QUALITY #8 and #6 (pins and reproducing calls); `corpus/lessons/round-26.md` (the 6.5.0 pin rested on the frozen invocation) | sharpens 6, 8 (a pin asserted for the round, not per call, and a reproducing call that names no resolved version) |
```

## Gates — every command with its output
Round 26 FAILS both rows (`<lane>` = the lane above, `git -C <lane>` implied):

```
$ git log --format='%h %cI %s' -1 ebe2cb4a
ebe2cb4a 2026-10-22T09:47:57-03:00 round-26: R26-C1 depth — evidence-ID identity table for eight native reader verbs at rea-agents 6.5.0 (24 envelopes, runs, table, recompute tool and receipt), knowledge entry, SOURCES S079-S080 and search log, lesson with Gate and Mistakes, README map, knowledge and Known-gaps rows
$ git log --format='%h %cI %s' -1 bd0c84bc
bd0c84bc 2026-10-22T09:49:24-03:00 round-26: R26-C1 counting instrument tools/round-26/c1-id-identity.py (selftest), before receipt at a0639d8e (0 of 8, entry_ok 0) and after receipt at ebe2cb4a (8 of 8, entry_ok 1); R26-C2 after receipt at 46ebfd2f (0 of 6)
$ git log --diff-filter=A --format='%h %cI' ae8bcd86 -- tools/round-26/c1-id-identity.py  ->  bd0c84bc 2026-10-22T09:49:24-03:00
$ git log --diff-filter=A --format='%h %cI' ae8bcd86 -- corpus/evidence/round-26/before/c1-selftest.txt  ->  bd0c84bc 2026-10-22T09:49:24-03:00
$ for p in 'utc_start' 'pkg_version' 'pkg_json_sha256' 'not after counter commit' 'runs.tsv'; do echo -n "$p: "; grep -c -- "$p" tools/round-26/c1-id-identity.py; done  ->  utc_start: 0 / pkg_version: 0 / pkg_json_sha256: 0 / not after counter commit: 0 / runs.tsv: 0
$ git show ae8bcd86:corpus/evidence/round-26/c1/runs.tsv | head -1 | tr '\t' '\n' | nl  ->  1 seat, 2 verb, 3 run, 4 path, 5 argv, 6 exit, 7 utc_start, 8 utc_end, 9 envelope_sha256, 10 evidence_id, 11 subject_sha256  (11 columns, no version column)
$ git show ae8bcd86:corpus/evidence/round-26/c1/envelopes/analyze-base.json | grep -c '6\.5\.0\|6\.7\.0\|package'  ->  0
$ grep -n 'round-26' corpus/claim-freezes.tsv  ->  round-26	FLAGGED	INSTRUMENT_ABSENT	definitions-first freeze c27f445e: counting rules and targets frozen, instruments written in wave 1 and committed after (C2 at 81f63f36 before any repair edit; C1 at bd0c84bc after the C1 data at ebe2cb4a); disclosed in claims.json freeze_kind; corpus/lessons/round-26.md
$ git show c27f445e:.ufo/waves/round-26/claims.json | grep -n 'freeze_kind'  ->  6:  "freeze_kind": "definitions-first: the counting rules below bind; the two instruments are written in wave 1 to these rules, committed and sha256-pinned before any after-measurement, and attacked by mutation-testers. Under the round-24 freeze gate this freeze is INSTRUMENT_ABSENT by design and is disclosed as such.",
```

Round 27 PASSES both rows:

```
$ git log --format='%h %cI %s' -1 a4f674b3  ->  a4f674b3 2026-10-22T11:51:23-03:00 round-27: freeze claims; commit both counters, red selftests and before receipts before any data
$ git show --stat --format='%h %cI' a4f674b3  ->  7 files changed, 1138 insertions(+): .ufo/waves/round-27/before/c1-at-cd32264f.txt (19), .ufo/waves/round-27/before/c1-selftest.txt (24), .ufo/waves/round-27/before/c2-at-cd32264f.txt (5), .ufo/waves/round-27/before/c2-selftest.txt (12), .ufo/waves/round-27/claims.json (62), tools/round-27/c1-rename-identity.py (609), tools/round-27/c2-xpin-check.py (407)
$ git ls-tree -r --name-only a4f674b3 corpus/evidence/round-27 | wc -l  ->  0
$ git log --diff-filter=A --format='%h %cI' a4f674b3 -- tools/round-27/c1-rename-identity.py  ->  a4f674b3 2026-10-22T11:51:23-03:00
$ git log --diff-filter=A --format='%h %cI' a4f674b3 -- tools/round-27/c2-xpin-check.py  ->  a4f674b3 2026-10-22T11:51:23-03:00
$ sed -n '74,77p' tools/round-27/c1-rename-identity.py
RUNS_HEADER = [
    "seat", "carrier", "verb", "run", "path", "argv", "exit", "utc_start", "utc_end",
    "envelope_sha256", "evidence_id", "subject_sha256", "pkg_version", "pkg_json_sha256",
]
$ sed -n '244,248p;256,257p' tools/round-27/c1-rename-identity.py
                start = parse_utc(r["utc_start"])
                if start is None or start < counter_time:
                    reasons.append("%s: utc_start %s not after counter commit" % (tag, r["utc_start"]))
                if r["pkg_version"] != PKG_VERSION or r["pkg_json_sha256"] != PKG_JSON_SHA256:
                    reasons.append("%s: package %s/%s not the frozen 6.5.0" % (tag, r["pkg_version"], r["pkg_json_sha256"][:12]))
                added = first_commit_time(root, rev, env_path)
                if added is None or added < counter_time:
$ sha256sum /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json  ->  a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
$ grep -o '"version": *"[^"]*"' /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json | head -1  ->  "version": "6.5.0"
```

The committed red fixtures fire, so both fail clauses are demonstrable on committed bytes:

```
$ TMPDIR=/fast/scratch/hyaku/kaidoku-r27/seats/QualityRow/tmp python3 -I -B tools/round-27/c1-rename-identity.py --selftest
PASS green: exit 0 (want 0) rows_complete=16/16 entry_ok=1 rev=HEAD
PASS swap-renamed-with-base: exit 1 (want 1) expects 'envelope sha256 differs' rows_complete=15/16 entry_ok=1 rev=HEAD
PASS reuse-one-run: exit 1 (want 1) expects 'shared with another run' rows_complete=15/16 entry_ok=1 rev=HEAD
PASS swap-verbs: exit 1 (want 1) expects 'meta.command' rows_complete=14/16 entry_ok=1 rev=HEAD
PASS run-before-counter: exit 1 (want 1) expects 'not after counter commit' rows_complete=15/16 entry_ok=1 rev=HEAD
PASS package-version: exit 1 (want 1) expects 'not the frozen 6.5.0' rows_complete=15/16 entry_ok=1 rev=HEAD
PASS package-json-sha: exit 1 (want 1) expects 'not the frozen 6.5.0' rows_complete=15/16 entry_ok=1 rev=HEAD
... 15 further cases (22 total) ...
selftest cases=22 failures=0
exit=0
```

The run reproduced the committed receipt `.ufo/waves/round-27/before/c1-selftest.txt` line for line. Lane
`git status --porcelain` was 5 lines before and 5 lines after the selftest run: it wrote nothing in the
lane (observation). A later status shows 6 entries; the extra one, `tools/round-27/assemble-c1.py`, was
written by a sibling seat, not by this seat.
## Findings
1. Observation — round 26 fails row 38: the C1 data commit `ebe2cb4a` (09:47:57-03:00) precedes the
   instrument commit `bd0c84bc` (09:49:24-03:00), which also carries the after receipt and the selftest;
   `tools/round-26/c1-id-identity.py` has no `utc_start` comparison and never reads `runs.tsv`.
2. Observation — round 26 fails row 39: `corpus/evidence/round-26/c1/runs.tsv` has 11 columns with no version
   or `package.json` sha256 column, the sampled envelope carries no version string, and the counter never
   reads `runs.tsv`, so the 6.5.0 pin rests on the frozen invocation.
3. Observation — round 27 passes both rows as committed at `a4f674b3`: counters, red selftests and before
   receipts precede any data (`corpus/evidence/round-27` is empty at that commit), and the counter refuses
   pre-instrument runs, pre-instrument envelopes, and a wrong package version or `package.json` digest.
4. Inference — row 39's per-call clause is currently carried by round 27's committed instrument and its
   committed red fixtures, not yet by a committed round-27 call record: no round-27 evidence tree exists in
   a commit yet, so the clause becomes checkable only when that data lands.
5. Observation — both rows are lesson-backed: routed defect 2 at
   `corpus/lessons/round-26-verifier-spotcheck.md:201-204`, routed defect 4 at `:208-209`; row 33 already
   exists in `corpus/QUALITY.md` and is the row row 38 sharpens.

## Touched surfaces
- Wrote `.ufo/waves/round-27/w1/QualityRow.md` (this file, the report path the L1 assigned) and
  `/fast/scratch/hyaku/kaidoku-r27/seats/QualityRow/draft.md` (same two rows, full command log). No other
  lane file created, edited or deleted; no git write, no jj command, no REA call, no install.
## Out of scope
- Not applied: `corpus/QUALITY.md` was not edited; the L1 integrates and commits the rows.
- Routed defects 1, 3 and 5 (the 6.7.0 code source row, the counter forgery gates, the 11 stale SCORECARD
  statements) were not worked here; defect 3's content is visible in the round-27 counter but is not a
  QUALITY row in this draft.
- No calibration claim, no SCORECARD edit, no lesson edit, no source opened.
## Artifacts
| path | sha256 |
|---|---|
| /fast/scratch/hyaku/kaidoku-r27/seats/QualityRow/draft.md | `e77c8916b8790968cfaec9176e08bbefa9407224cfd4c8700eeb64a79f6994f9` |
| /fast/scratch/hyaku/kaidoku-r27/seats/QualityRow/tmp | empty scratch directory used as TMPDIR |

## Labels
Every statement above is an observation unless it says inference. No source was opened, so no source row is
claimed. No tool was installed or upgraded.
