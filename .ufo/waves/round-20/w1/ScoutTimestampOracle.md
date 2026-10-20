# ScoutTimestampOracle — independent oracle: round-19/18 zoned timestamps vs introducing-commit committer time

Seat `KaidokuR20.ScoutTimestampOracle-2` (read-only advisory; leaf, no dispatch). Base rev
`14f0260ad319ecc26994381b2415d5a999003375`. Lane HEAD at dispatch was `d1d981d2cc041dda4656c5b01d2c8445d8d17124`;
**every read below is a Git object read at the base rev, never the working tree**. Scope: all tracked blobs under
`.ufo/waves/round-19` and `.ufo/waves/round-18`. Question: every timestamp with an explicit zone that is **later** than
the committer time of the commit that introduced its line (`git blame --porcelain`).

## 1. The full list (2 findings) — OBSERVATION

| # | path:line | token | instant (UTC) | epoch | introducing commit | committer time | delta |
|---|---|---|---|---|---|---|---|
| 1 | `.ufo/waves/round-19/claims.json:36` | `2026-10-20T16:20:00-03:00` | 2026-10-20T19:20:00Z | 1792524000 | `4f6c73f81ae8d31de18377d7ff57e4e10140ce48` | 1792523357 = 2026-10-20T16:09:17-03:00 (−0300) | **+643 s** (10 m 43 s) |
| 2 | `.ufo/waves/round-18/claims.json:35` | `2026-10-20T13:25:00-03:00` | 2026-10-20T16:25:00Z | 1792513500 | `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0` | 1792513435 = 2026-10-20T13:23:55-03:00 (−0300) | **+65 s** |

Line text at the base rev (verbatim minus the file's leading spaces):

- `.ufo/waves/round-19/claims.json:36` → `"at": "2026-10-20T16:20:00-03:00 (before any after-revision measurement of C1/C2; C3 predictions frozen at a1140e7 before any analyze)",`
- `.ufo/waves/round-18/claims.json:35` → `"at": "2026-10-20T13:25:00-03:00 (after wave 1, before any round-18 REA run)",`

That is the whole list. The expected seed (`round-19/claims.json:36`) is present. No other zoned timestamp in either
tree is later than its introducing commit's committer time (2 of 2280; §5 gives the nearest miss).

## 2. Method and counts — OBSERVATION

- Grammar (frozen D2, contract `contract.md:41-45`): `YYYY-MM-DDTHH:MM[:SS][.f](Z|±HH:MM)`, plus
  `YYYY-MM-DD HH:MM[:SS] ±HH[MM]` and ` -03`. Regex used:

  ```
  (?<![0-9])(?P<y>\d{4})-(?P<mo>\d{2})-(?P<d>\d{2})(?P<sep>[T ])(?P<h>\d{2}):(?P<mi>\d{2})
  (?::(?P<s>\d{2}))?(?:\.(?P<f>\d+))?(?: ?(?P<z>Z|z|[+-]\d{2}(?::?\d{2})?))(?![0-9])
  ```
- Instant: `datetime(..., tzinfo=timezone(offset)).timestamp()`; comparison strict `ts > committer-time`
  (equality is not a finding). `git blame --porcelain --root <rev> -- <path>`; the `committer-time` header of the
  group owning each final line is used (`--root` so root commits are attributed, not boundary-omitted).
- Counts: **1518** tracked blobs (1491 mode `100644`, 25 `100755`, 2 symlink blobs); **2280** zoned timestamp
  occurrences on **2197** distinct lines in **366** files (round-19: 1302 occurrences / 1282 lines; round-18: 978 / 915).
  2280/2280 lines resolved by blame, 0 errors, 0 unparsable, 0 NUL-containing blobs. Delta distribution:
  min −1792516605 s, max **+643 s**, median −728 s. Exactly 2 deltas > 0, 0 deltas = 0.
- The 2 symlinks (`round-18/verify/scratch-custody/.../symlink-loop`,
  `round-19/verify/scratch-custody/.../symlink-loop`) are self-referential path strings; no timestamp, blame resolved.

## 3. Commands pasted with exit codes — OBSERVATION

```
$ git -C LANE rev-parse --verify '14f0260ad319ecc26994381b2415d5a999003375^{commit}'
14f0260ad319ecc26994381b2415d5a999003375                              # exit 0
$ git -C LANE ls-tree -r --name-only 14f0260ad319ecc26994381b2415d5a999003375 \
    -- .ufo/waves/round-19 .ufo/waves/round-18 | wc -l
1518                                                                   # exit 0
$ git -C LANE blame --porcelain --root -L 36,36 14f0260 -- .ufo/waves/round-19/claims.json \
    | grep -E '^(committer-time|committer-tz)'
committer-time 1792523357
committer-tz -0300                                                     # exit 0
$ git -C LANE blame --porcelain --root -L 35,35 14f0260 -- .ufo/waves/round-18/claims.json \
    | grep -E '^(committer-time|committer-tz)'
committer-time 1792513435
committer-tz -0300                                                     # exit 0
$ date -d '2026-10-20T16:20:00-03:00' +%s; date -d '2026-10-20T13:25:00-03:00' +%s
1792524000
1792513500                                                             # exit 0  (+643 s and +65 s)
$ python3 -I -B "$D/scan.py" "$D/cand.json"        # blob scan of all 1518 files ($D = mkdtemp)
{"rev": "14f0260ad319ecc26994381b2415d5a999003375", "files": 1518,
 "timestamp_occurrences": 2280, "parsed": 2280, "unparsable": [],
 "candidate_lines": 2197, "candidate_files": 366}                      # exit 0
$ python3 -I -B "$D/pass.py" default "$D/cache-default.json" "$D/cand.json"
DONE mode=default files=366                                            # exit 0
$ python3 -I -B "$D/pass.py" mc "$D/cache-mc.json" "$D/cand.json"      # blame -M -C
DONE mode=mc files=366                                                 # exit 0
$ python3 -I -B "$D/analyze.py" "$D/cand.json" "$D/cache-default.json" \
    "$D/cache-mc.json" "$D/analysis.json"
== default_committer 2 … == mc_committer 2 … == default_author 1275     # exit 0
{"stats": {"files_blamed": 366, "lines_resolved": 2280, "lines_missing": 0},
 "errors": [], "findings": […2…]}  FINDINGS 2 FILES 2                  # exit 0
$ python3 -I -B "$D/audit2.py"      # near-miss zone audit
NEAR-MISS count: 0                                                     # exit 0
$ python3 -I -B "$D/fixture.py"     # positive control, mkdtemp repo, removed
SELFTEST: CLEAN cases=1                                                # exit 0
    (first run of this fixture exited 1 on a wrong expectation I had written for
     `12:30:00.500+00:00`; the scanner was correct — see §5. Corrected run: exit 0.)
```

## 4. Coverage audit — OBSERVATION (formats searched, zero hits unless stated)

- lowercase `t` separator (`2026-10-20t16:20`): 0. RFC 2822 (`Tue, 20 Oct 2026 16:20:00 -0300`): 0.
- dotted (`2026.10.20 16:20`) and slash (`2026/10/20 16:20`) dates: 0. Month-name dates: 0.
- NBSP or U+2212 between time and offset: 0. Date-time followed by a parenthesised zone: 0 outside the grammar.
- Compact `YYYYMMDDTHHMMSS[Z]`: **8**, all path segments of receipt/log filenames under round-18
  (`20261018T173220Z`, `20261018T180140Z`, `20261018T191721Z`, `20261019T100704Z`, each twice in
  `final-recheck/controls.receipt.json.stdout` and `verify/controls.stdout`). All are 2026-10-18/19Z, past by ≥1 day.
- 14-digit runs: 17. Checked: 13 Go pseudo-version stamps (`v0.0.0-20240102092130-…`, `v0.0.0-20200116055534-…`,
  `v0.0.0-20180814174437-…`, `v0.0.0-20201227073835-…`), `20261010120053` twice (pseudo-version-like; that instant,
  2026-10-10T12:00:53, is past), and two sha256 hex prefixes (`19536458150345…`). None carries a zone designator.
- Near-miss rule: for every date-time token the strict grammar did not match, look for `Z`, `±HH:MM`, `±HHMM`, `±HH`,
  `UTC/GMT`, or a parenthesised offset in its immediate (±4 whitespace) tail/head. **0 hits**, so the strict grammar
  loses nothing in these two trees.
- Timestamps in escaped JSON string values are scanned on their physical line; all matched normally.

## 5. Calibration — OBSERVATION

- Closest **non**-finding: `.ufo/waves/round-19/wave1-registry.json:4,5` `2026-10-20T18:37:12.542Z` vs commit
  `85589ac` → **−5.458 s**. Closest finding: **+65 s**. A tolerance up to 5 s changes nothing; a tolerance of 65 s
  or more would drop the round-18 finding, 643 s or more the round-19 one. 0 timestamps land exactly on their commit
  instant.
- `-M -C` blame yields the identical two findings → not a line-move/copy artefact.
- Author time instead of committer time yields **1275** findings. This is the jj/rewrite effect (committer = rewrite
  time). It follows that D2's tool must read `committer-time`; an `author-time` implementation would be red almost
  everywhere and useless. `[INFERENCE]`
- Replacing per-line blame with a whole-file/latest-commit comparison would **miss** `round-19/claims.json:36`:
  the file's later commit `b26a6c4` has committer `16:46:03-03` > `16:20:00-03`. Per-line blame is load-bearing.
- Positive control (fixture, `mkdtemp`, deleted after the run): one commit at `2026-10-20T15:00:00Z`; findings asserted
  for `T…-03:00`, ` … -0300`, ` … -03`, `…Z`, `…\.500Z`, and a zone-sensitivity case `12:10:00-03:00` (= 15:10Z future
  even though the naive 12:10 reading is past); no finding for a zone-less line and for an exactly-equal instant.
  Result `SELFTEST: CLEAN cases=1`, exit 0. (My first expectation wrongly treated `12:30:00.500+00:00` as future; the
  scanner was right and the fixture expectation was corrected — noted so the earlier failure is not read as a tool bug.)

## 6. Corroboration — OBSERVATION

- The lane's own withdrawal at `.ufo/waves/round-19/claims.json:45` (commit `b26a6c4`) says: "The 16:20 timestamp was
  future-dated relative to the commit carrying it (4f6c73f, committed 16:09:17 -03) and is withdrawn." Same commit,
  same clock as finding 1.
- Round-18's own w2 audits already record finding 2: `w2/FreezeBeforeRun.md:50`, `w2/ScorecardAudit.md:82,88`,
  `w2/DecisionRuleApply.md:160`, `w2/KnowledgeEntryReview.md:295-296`; `w2/ScorecardMeasuredDraft.md:133-134` states
  the block is already in `eb6c266`. It was never corrected in the claims file:
  `git log --format='%h %ct %cI %s' 14f0260 -- .ufo/waves/round-18/claims.json` → single commit `eb6c266`
  `1792513435 2026-10-20T13:23:55-03:00` (exit 0). Round-19's file has three commits: `85589ac`, `4f6c73f`, `b26a6c4`.
- Independent sibling: `W20/w1/EvidenceTimestampLint.md:9-10` (the D2 tool author) reports the same two findings with
  the same commit clocks.

## 7. Residual unknowns / limits

- (a) A token split across a physical newline is invisible to a line scan; nothing in these trees suggests one, but it
  is not measurable by this method. `[INFERENCE]`
- (b) Bare time-of-day + zone (no date) is outside D2's grammar. Four prose lines exist; with the implied date
  2026-10-20 they are all **past** relative to their introducing commit: `round-19/w2/BindingCover.md:81`
  (commit `b26a6c4`, −2414 s) and `round-18/w2/ReportDraft.md:160`, `round-18/w2/Runcalibaether.md:27`,
  `round-18/w2/ScorecardMeasuredDraft.md:46` (all commit `db4bdb1`, −3088 to −3170 s). They do not change the answer
  under any reading that supplies the date.
- (c) Date-only strings with a zone and zone-less times are out of scope by the frozen grammar; widening it would
  change the interface the counter relies on.
- (d) `[INFERENCE]` The 65 s delta in finding 2 is small enough that machine clock skew could in principle explain it;
  its own round's w2 audits independently call the stamp wrong, so the finding does not rest on skew.
- (e) I examined only the two directories, only objects reachable at the base rev. HEAD's untracked scratch dirs
  (e.g. `round-19/verify/scratch-custody/...`) do exist as committed round-19 blobs, and were included.
  During this run the lane working tree acquired 11 modified tracked files (gates, tools, `corpus/*.md`) from other
  seats; none is mine, and none affects rev-pinned object reads. My only lane write is this report.
- (f) The two findings are equal under default blame and `-M -C`; a different "introducing commit" definition
  (whole-file, or the latest commit touching the file) changes the answer to **0** — this is the calibration point
  the D2 counter should pin.

## 8. Tooling

No installs or upgrades (nothing needed); no Go toolchain execution; no REA/Ghidra invocation. Scratch scripts and the
fixture lived in one `mktemp -d` directory and were removed after evidence collection.

Clock at write time: `date -Iseconds` → `2026-10-20T17:58:04-03:00`.
