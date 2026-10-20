# W1 ReviewTimestampFormats — timestamp formats in committed evidence vs the D2 lint

Seat: KaidokuR20.ReviewTimestampFormats-2 (advisory, read-only; this file is the seat's only lane write).
No tools installed (none needed). Scope: committed evidence at contract baseline
B = `14f0260ad319ecc26994381b2415d5a999003375` over `.ufo/waves/round-17`, `.ufo/waves/round-18`,
`.ufo/waves/round-19`, `corpus/lessons`, `SCORECARD.md`. D2 interface: round-20 `contract.md`
("D2 `W20/tools/evidence-timestamps.py …`"): every zoned timestamp on a line is compared with the
committer time of the commit that introduced the line (`git blame --porcelain REV`); finding
`future_dated <path>:<line>`.

## Method (OBS unless labeled)

- B committer time `2026-10-20T17:24:21-03:00`:
  `git -C LANE show -s --format='%H %cI %ci' 14f0260a…` → exit 0.
- In-scope content is identical B→main→working tree:
  `git -C LANE diff --stat 14f0260a… main -- .ufo/waves/round-17 .ufo/waves/round-18 .ufo/waves/round-19 corpus/lessons SCORECARD.md`
  → no output, exit 0. Working-tree path:line anchors below are therefore committed content.
- Surveyed every tracked file in scope at B (blobs extracted via `git archive B -- <paths> | tar -x`
  into `tempfile.mkdtemp()` under /tmp, removed on exit; 2 committed symlinks skipped, both named
  `symlink-loop` under round-18/19 `verify/scratch-custody/…` — D1-residue class, not timestamps).
- Extracted all zoned datetimes with a Python `re` covering `YYYY-MM-DD(T| )HH:MM[:SS][.f]` followed by
  `Z | ±HH:MM | ±HHMM | ±HH`, boundary-guarded `(?<!\d)` … `(?![\d:])`; compared each with the
  introducing commit's committer time via `git blame --porcelain -l B -- <file>`.
- Dialect note: `git grep` POSIX ERE cannot express the needed lookarounds —
  `git grep -nE '…[+-]([0-9]{4}(?![0-9])|…)'` → `fatal: … Invalid preceding regular expression`, exit 128.
  Candidate extraction belongs in Python `re`, not ERE.

## Census — what actually occurs (OBS; 2,854 zoned instances in 459 files; raw `git grep -nE` line set was 2,758 lines)

| family (sep, zone, frac) | count | example anchors |
|---|---|---|
| `T` `±HH:MM` frac+sec | 1,801 | receipts `.ufo/waves/round-17/final-recheck/controls-final.receipt.json:11` (`…+00:00` µs); custody local `.ufo/waves/round-17/custody/custody-r17.v2.txt:5` (`-03:00`) |
| `T` `Z` sec | 402 | `.ufo/waves/round-17/custody/custody-r17.v2.txt:4`; `SCORECARD.md:671` |
| `T` `±HH:MM` no frac | 354 | claims `"at"`/`declared_at` `.ufo/waves/round-17/claims.json:5`; git `%cI` quotes `.ufo/waves/round-19/w2/CriticAdmission.md:45` |
| `T` `Z` frac | 281 | swarm registries `.ufo/waves/round-19/w1/swarm-registry.json:4` (`.077Z`); npm quotes `.ufo/waves/round-19/w2/ReopenS037.md:60` (`.640Z`) |
| `T` `Z` minute precision | 7 | `.ufo/waves/round-18/evidence/s032-digests.json:4` (`2026-10-20T15:38Z`); `.ufo/waves/round-17/w2/ScoutReaLogKnob.md:85` |
| `T` `±HHMM` | 5 | pacman-log quotes `.ufo/waves/round-19/w2/R12Addendum.md:85`, `w1/R12Disclosure.md:36,99` (`2026-10-20T09:16:36-0300`); `w1/FallbackReaders.md:82,87` |
| space `Z` | 3 | `.ufo/waves/round-18/w1/RevValidatorPaths.md:10` (`2026-10-20 14:47:24Z`); `w1/ScoutValidate16Sites.md:202`; `.ufo/waves/round-19/w1/LiveConfigPins.md:73` |
| `T` `±HH` (2-digit) | 1 | `.ufo/waves/round-18/w1/ScoutProducerRevSites.md:108` (`2026-10-20T10:46:45-03`) |

Epoch seconds (contract-out-of-scope, no explicit zone): 30 lines in scope — custody `MTIME_EPOCH`/`CTIME_EPOCH`
(`custody-r17.v2.txt:22,26`), `%ct`/reflog epochs (`.ufo/waves/round-18/w2/FreezeBeforeRun.md:84-85,178-179`),
API `reset` (`round-18/w1/ScoutPr9348Reopen.md:61,80,145`), rekor `integratedTime`
(`round-19/w2/ReopenS037.md:113,274`), meta-og epoch (`round-17/w1/ScoutGoReSymReleases.md:31`), even a filename
(`~/.bashrc.bak.1792084648`, `round-19/w1/GhidraJdkRecheck.md:37-38`). INF: keeping epochs unparsed is right —
bare 10-digit parsing would false-positive on digests/sizes; custody records dual renders (Z + `-03:00` + epoch on
adjacent lines) so the zoned forms already cover custody verification; `date -d @epoch` conversions inside reports
re-enter textual scope at the converted form (`FreezeBeforeRun.md:179`).

## What the D2 lint must parse (INF, grounded in the census)

1. `T`-form with `Z` and `±HH:MM` (2,838/2,854 = 99.6% of instances) — the contract regex already covers these,
   including optional seconds and fraction (all fractions seen: 3 or 6 digits).
2. Minute-precision `T…Z` (7) — covered by the contract's optional `[:SS]`.
3. The authored-declaration shapes that the two true findings use: JSON `"at": "…±HH:MM (prose suffix)"`
   — parse only the token; prose must not glue (trailing boundary needed).
4. Recommended coverage extension (cheap, zero cost to false-positive rate): `T`+`±HHMM` (5), `T`+`±HH` (1),
   space+`Z` (3) — the contract regex misses these 9 instances (6 lines); all are historical quotes today, so this
   is calibration completeness, not risk. The contract's space-form ` -03` literal has 0 occurrences in scope.

## Future-dated at B: exactly two, both claims `amendments[].at` (OBS)

Full simulation over all 2,854 instances: `future_dated` = 2; equal-to-commit = 0.

- `.ufo/waves/round-18/claims.json:35` — `"at": "2026-10-20T13:25:00-03:00 (after wave 1, …)"`,
  introduced by `eb6c2668e5cb` (committer-time 1792513435 `-0300` = 13:23:55-03) → **+65 s future**.
  `git blame --porcelain B -L 35,35 -- .ufo/waves/round-18/claims.json` → exit 0.
  Status: disclosed as Mistakes row 10 (`corpus/lessons/round-18.md:74`: "amendment time 13:25:00 is after its own
  commit (13:23:55)") but never routed as a defect id and never withdrawn in-file (no round-18 counterpart of
  round-19's `amendments[1].supersedes`).
- `.ufo/waves/round-19/claims.json:36` — `"at": "2026-10-20T16:20:00-03:00 (…)"`,
  introduced by `4f6c73f81ae8` (committer-time 1792523357 `-0300` = 16:09:17-03) → **+643 s future**.
  `git blame --porcelain B -L 36,36 -- .ufo/waves/round-19/claims.json` → exit 0.
  This is the known routed round-19 D2 (`corpus/lessons/round-19-verifier-spotcheck.md:178-190`), withdrawn in-file
  by `amendments[1]` (`supersedes`/`correction`) — but the offending line remains committed, so a retro D2 run at B
  still fires on it.

INF for the fixing seat: `--strict` over historical paths is expected to exit 1 (round-18: 1 finding; round-19:
1 finding; round-17, `corpus/lessons`, `SCORECARD.md`: 0). Selftest expectations must not assert CLEAN over
round-17..19; round-20 paths are clean by construction only if seats obey "timestamp at or before shipping commit"
(round-20 `claims.json` already asserts no timestamp — the right pattern).

## Quoted historical instants — false-positive analysis (OBS: zero false positives at B)

Blame attribution is load-bearing: 2,854/2,854 non-finding instances include four quote classes a naive
recency/mtime rule would wrongly flag:

1. npm packument publishes `2026-10-18T08:12:05.640Z` quoted on 2026-10-20
   (`.ufo/waves/round-19/w2/ReopenS037.md:60,79,221,239`; `corpus/lessons/round-19.md:43`;
   `round-19-verifier-spotcheck.md:156`) — two days older than their quotes.
2. Quotes of the withdrawn future instant itself: `.ufo/waves/round-19/w2/CriticC3Rule.md:113`
   (`"2026-10-20T16:20:00-03:00"`) — introduced by `b26a6c42207a` (committer 1792525563 = 16:46:03-03), i.e. past
   by 26 min; safe under blame, flagged by any "later than round start" rule.
3. Historical custody mtime/ctime renders 2026-10-14/15 (`custody-r17.v2.txt:24-29,42-47`;
   `R12Addendum.md:55,73`; `GhidraJdkRecheck.md:37`) and the deliberately ancient mutant fixture
   `2000-01-01T00:00:0[01]Z` (`.ufo/waves/round-19/w2/MutStrict.md:100,103`).
4. Round-1..16 lesson/spotcheck log quotes (`corpus/lessons/2026-10-15-round-1.md:63`;
   `round-14/15/16/17/18-verifier-spotcheck.md` launch/complete lines).

Zoneless forms must stay unparsed: the retained Ghidra/script logs use `2026-10-20 13:26:01 INFO …`
(`.ufo/waves/round-18/runs/s1246-noswiss-methods/logs/rea-ghidra-2bOinT/ghidra.log:1`, 5,721 lines;
`script.log:1`) — UTC renders in local-looking shape (13:26 UTC = 10:26 -03).
`git grep -cE '<zoned>' B -- …/logs` over that dir → no matches, exit 1. Interpreting zoneless as host -03 would
flood false findings; the contract's explicit-zone requirement is correct. `LABEL-DEFECT` selftest lines with
zoneless space-forms (`selftest-custody-pair.stdout:63,72,89,90`) are likewise excluded.

## Precision and implementation cautions for `evidence-timestamps.py` (INF)

- Strict `ts > committer_time`; no positive grace window. Legit past margins reach +5.458 s
  (`.ufo/waves/round-19/wave1-registration.json:5` `2026-10-20T18:37:12.542Z` vs its commit) and +8.7 s
  (`round-17/final-recheck/controls-final.receipt.json:11`); 34 instances sit inside (−10 s, 0), 351 inside
  (−60 s, 0). A ±60 s skew tolerance would mask the live round-18 +65 s defect. Whole-second truncation of both
  sides is safe (both true findings are whole-second positive; sub-second receipts stay negative).
- Cross-validation: the lane's own r18 spotcheck window (`round-18-verifier-spotcheck.md:123`: runs/ blobs
  13:23:55–13:32:10-03 before `b2aad08` at 13:38:07) matches this survey's tightest-margin cluster (−595 s).
- Parse zones from the matched offset, never host TZ; `committer-time`/`committer-tz` arrive as two separate
  porcelain lines (a parser expecting one merged line silently yields zero comparisons — bug hit and fixed during
  this survey). `-l` for full hashes; blame the file once, map final line numbers.
- Attribution uses the introducing commit at the measured REV, so findings are rev-stable; re-edits only push
  blame forward (further from any quoted past instant).

## Residual risk / verification gaps

- The 2-finding/0-FP result is my replication of the D2 semantics at one rev (B), not an execution of the (not yet
  present) tool: `git -C LANE ls-tree -r --name-only main -- .ufo/waves/round-20/tools` → empty, exit 0. The
  fixing seat's implementation is the authority once landed.
- 2 committed symlinks (both `symlink-loop`) skipped by the survey; blame on symlink blobs is well-defined but
  they carry no timestamps.
- Findings are per-instance; a line with two timestamps yields two comparisons (observed max 2 on one line in
  scope). Single-line JSON evidence would coarsen `path:line` — none of the two findings is affected.
- In-scope drift B→main verified empty for these paths only; round-20 additions are out of this survey's scope.
