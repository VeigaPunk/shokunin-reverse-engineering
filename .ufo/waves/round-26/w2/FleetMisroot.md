# Fleet-root misroot sweep (round 26, wave 2)

Seat: KaidokuR26.FleetMisroot. Scope: fleet root `/home/vgpnk/Projects/shokunin` only, compared
against the wave-1 baseline `.ufo/waves/round-26/w1/FleetMisrootPrecheck.md` (baseline instant
2026-10-22T12:12:58Z, fleet HEAD then `a20e701e`). Nothing moved, nothing deleted; the lane was
not edited except this report.

## Verdict

Exactly one kaidoku round-26 misroot at the fleet root:

| path | sha256 | size | mtime (UTC) |
|---|---|---|---|
| `kaidoku-r26/seats/EntryCorrection/final-report.md` | `ec2a97afd68b2c29a6ce0b79d61fe33c30ea430adf266480a43a00f0bde8a7c1` | 8429 | 2026-10-22T12:53:02Z |

Seat: `KaidokuR26.EntryCorrection` (round 26, wave 1, scribe; routed defect 4, the "138 responses
per selector" correction). Observation: its first line reads `# Round 26 wave 1 — EntryCorrection
(scribe): routed defect 4, "138 responses per selector"` and its third line
`Seat: KaidokuR26.EntryCorrection.` The correct home for this report is the lane
`.ufo/waves/round-26/w1/EntryCorrection.md`, which exists (8001 B, mtime 13:00:58Z) and is a
revised, tightened variant of the same report (diff shows rewording only; same evidence, same
counts 69 / 43 / 138, same artifact hashes). The misrooted copy is an earlier draft of the same
write, landed at the fleet root instead of the lane.

## Command and comparison

- Command: `git -C /home/vgpnk/Projects/shokunin status --porcelain` and `--porcelain -uall`
  (read-only), exit 0, run 2026-10-22T12:59:48Z and again 2026-10-22T13:02:02Z; both runs show
  the same record set. Fleet HEAD now `1fc0832` (moved from `a20e701e` by hyaku ledger commits,
  unrelated to status drift).
- Baseline had 19 records (18 files plus the expanded round-49 untracked file). All 18
  tracked-file records are byte-for-byte the same set with the same status letters. The
  round-49 file `.ufo/waves/round-49/falsify/RowGameDev2d.md` is unchanged: 13630 B, mtime
  11:38:25Z, sha256 `37aaa836a5d650b658484cf99d3722acff55cd569a7410a36c588d60aaedce99` —
  identical to the baseline's hash (observation). It is kotoba round 49, not kaidoku.
- The only new record is `?? kaidoku-r26/seats/EntryCorrection/final-report.md`
  (collapsed to `?? kaidoku-r26/` in the bare form). The three directories `kaidoku-r26/`,
  `kaidoku-r26/seats/`, `kaidoku-r26/seats/EntryCorrection/` all carry the same creation mtime
  2026-10-22T09:53:02-03:00 = 12:53:02Z, i.e. two minutes after the wave-2 dispatch (12:51Z)
  and long after wave-1 results were collected (w1-task-result.json mtime 12:11Z).
- Timing note (unknown): neither wave-1 nor wave-2 `*-task-result.json` mentions the path
  `kaidoku-r26/seats/EntryCorrection` (grep count 0 in both), so no harness record points at
  the misroot; the writer mechanism (which tool path wrote it) cannot be determined from the
  records present.
- Negative scan (observation): `find` at the fleet root, depth 3, excluding `.git`, lane dirs
  (`*-shokunin`), `.ufo`, `.scratch` and the new `kaidoku-r26/`, for files modified after the
  round-26 launch (11:54:45Z) returns nothing — no second invisible misroot appeared at the
  searched depth. The pre-round fingerprints from baseline section D (`write`,
  `bash: .../souji-shokunin`, `tameshi-shokukin/`, `mori-shokukin/`, empty `reports/`) are
  unchanged in kind: `write` still shows as staged `A` with its old identity, the rest stay
  file-less or ignored, none kaidoku.

## Conclusion

- Observation: one new fleet-root path since the wave-1 baseline; it is a kaidoku round-26
  wave-1 seat report written outside the lane.
- Inference: misroot cause is a report-write aimed at the wrong root; the lane copy that landed
  seven minutes later is the version wave-2 seats review, so the misroot is a duplicate draft,
  not missing evidence.
- Left in place per instructions. Suggested disposition (not executed): the lane owner may copy
  nothing — the lane already holds the revised report — and may delete the fleet-root
  `kaidoku-r26/` tree at its discretion.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r26/seats/w2/FleetMisroot/)

| file | sha256 |
|---|---|
| porcelain-uall.txt (timestamp, full `-uall` output, exit 0, 2026-10-22T13:02:02Z) | `7463b3d0720e68f590ec5032aa74a0de7bf88907b11e437310becef13a62e9f7` |
| misroot-copy.md (copy of the misrooted report) | `ec2a97afd68b2c29a6ce0b79d61fe33c30ea430adf266480a43a00f0bde8a7c1` |

Tool installs or upgrades: none. No REA calls, no web sources. Read-only on the lane and fleet;
no git/jj writes anywhere.
