# R25 a3 wave 1 — per-claim SCORECARD rows, attempt 3 (seat ScorecardDraft)

Date 2026-10-22. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76`. Read-only seat: no lane product file was
written by this seat; the only lane write is this report.

## Deliverable — paste-ready table

```markdown
| claim | axis | score delta | before → after | counting command | measured commit | evidence |
|---|---|---|---|---|---|---|
| R25-C1 | calibration | finite proxy 10.0 → 10.0, delta 0 | 5 → 0 mismatches of 5 fixed items (exit 1 → 0) | `python3 -I -B tools/round-25/a2/c1-calibration.py --root <LANE> --rev <REV>` | before `9dcd11ec`; after `0e333eb2fc25f538a99058761f379845f2534c42` (C1 alone), re-measured at `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76` (both claims) | `corpus/evidence/round-25/a2/before/c1-calibration.json`; `corpus/evidence/round-25/a3/after/c1-at-0e333eb2.json`, `corpus/evidence/round-25/a3/after/c1-at-08c7a729.json` |
| R25-C2 | coverage | finite proxy 10.0 → 10.0, delta 0 | knowledge Markdown 107 → 108; entry sourced 0 → 1 (S075, S076, S077 qualify) | `python3 -I -B tools/round-25/a2/c2-coverage.py --root <LANE> --rev <REV>` | before `9dcd11ec`; after `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76` | `corpus/evidence/round-25/a2/before/c2-coverage.json`; `corpus/evidence/round-25/a3/after/c2-at-08c7a729.json`; `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md` |
```

Optional Round-24-parity third row: `| depth | — | unchanged (finite proxy 10.0 → 10.0, delta 0) | unchanged; not claimed by either round-25 claim | command A | 08c7a729 | — |`

Suggested closing line under the table:

```markdown
Command A at `08c7a729`: mapped 108/108, missing [], dangling [], rule blocks 17/17. A green
C1 shows that five fixed statements agree with the repository; it is not a full audit of
SCORECARD or SHONEN. C2's counter checks presence, count and source linkage, not the
entry's truth; the falsify seats and the closure judge the content. No axis is retired;
no capability row is added.
```

## Behaviour of each claim, as measured

| claim | command (read-only, from the lane root) | rev | exit | key output | UTC |
|---|---|---|---|---|---|
| R25-C1 | `python3 -I -B tools/round-25/a2/c1-calibration.py --root <lane> --rev <REV>` | `9dcd11ec` | 1 | `"items": 5, "mismatches": 5` | 10:44:18Z |
| R25-C1 | same | `0e333eb2` | 0 | `"items": 5, "mismatches": 0` | 10:42:59Z |
| R25-C1 | same | `08c7a729` | 0 | `"items": 5, "mismatches": 0` | 10:43:08Z |
| R25-C2 | `python3 -I -B tools/round-25/a2/c2-coverage.py --root <lane> --rev <REV>` | `9dcd11ec` | 1 | `"knowledge_md": 107, "entry_sourced": 0` | 10:44:18Z |
| R25-C2 | same | `08c7a729` | 0 | `"knowledge_md": 108, "entry_sourced": 1` | 10:43:08Z |

Both claims hold (observation). C1 before detail (saved receipt): I1, I2, I3 all false
(no SCORECARD, LOG or QUALITY line recorded the round-24 rejected-honest-stop); I4
stated [78, 78] against observed 107; I5 stated [88, 116] against observed [95, 266].
After, all five items are `"match": true` at both revisions; at `08c7a729` I4 reads
stated [108, 108] against observed 108. C2 after detail: cited rows S021, S075, S076,
S077; qualifying rows S075, S076, S077 (S021 was opened 2026-10-19, so it does not
qualify); the entry's `source:` line names all four rows.

Fresh runs at `0e333eb2`, `08c7a729` (C1) and `08c7a729` (C2) are byte-identical to the
three saved receipts in `corpus/evidence/round-25/a3/after/` (`diff`, exit 0 each); the
before run is byte-identical to
`corpus/evidence/round-25/a2/before/c1-calibration.json` (sha256
`24c295c2377ff46bebec02325aaa82d1360c08b890a0569af30319a1c8affb53`). Command A
(extracted from `SCORECARD.md:88-124`, 10:44:52Z) and
`git ls-tree -r --name-only <rev> -- corpus/knowledge/` (10:44:09Z) agree:

| revision | knowledge_files | mapped | missing | dangling | rule_blocks | citation_resolved_rules | coverage_score | depth_score |
|---|---|---|---|---|---|---|---|---|
| `9dcd11ec` | 107 | 107 | [] | [] | 17 | 17 | 10.0 | 10.0 |
| `0e333eb2` | 107 | 107 | [] | [] | 17 | 17 | 10.0 | 10.0 |
| `08c7a729` | 108 | 108 | [] | [] | 17 | 17 | 10.0 | 10.0 |

## Score delta, and why it is zero

`claims.json` freezes `axes_before` coverage 10, depth 10, calibration 10 and states the
three owned finite proxies tie at 10, so both claims work a tied-lowest axis. Command A
gives coverage_score 10.0 and depth_score 10.0 at every revision above (observation).
The calibration proxy is the round-1 `command B` rubric, whose current score of 10 is
unchanged by either claim (observation: `SCORECARD.md:27` still reads `0 → 10`, measured
at `75af886a`). Neither claim moves a finite proxy, so both deltas are 0, as in round
24's "Finite proxy 10.0 → 10.0, delta 0". No axis is retired, no capability row is added.

## Findings for the L1 (not mine to fix)

- **The three after-receipts are untracked.** `git cat-file -e 08c7a729:<path>` fails
  for `corpus/evidence/round-25/a3/after/c1-at-0e333eb2.json`, `c1-at-08c7a729.json`,
  `c2-at-08c7a729.json`; `git status --porcelain` lists
  `?? corpus/evidence/round-25/a3/after/`. The before receipts under
  `corpus/evidence/round-25/a2/before/` are tracked (landed with the attempt-2 freeze).
  The evidence pointers in the table above resolve only once these are committed;
  otherwise they are dangling (observation). The census receipt
  `corpus/evidence/round-25/a3/census-after-08c7a729.txt` is untracked too (five
  inherited W04 duplicate-URL warnings plus one `ok` row for `corpus/SOURCES.md`,
  `exit=0`).
- **An uncommitted SCORECARD.md edit already exists** carrying a table of the same shape
  as the one drafted above (working-tree diff, 9 added lines at
  `SCORECARD.md:3051-3059`, file mtime 2026-10-22 07:43:07 -0300, author unknown to this
  seat; it appeared during this seat's run). This seat did not write it. Its numbers
  agree with every measurement above (observation). The L1 owns that edit; this report
  supplies verified values.
- **Stale self-assessment outside the five frozen C1 items.** The owned-axes `depth` row
  still cites `SKILL.md:77-191` and "9/9 queue-drain rule blocks", but at `08c7a729`
  `SKILL.md`'s "## Queue-drain craft" section spans lines 81–318 and command A counts 17
  rule blocks, all 17 resolved (observation). The five frozen items do not cover this
  row, so R25-C1's 0-mismatch result is unaffected; the L1 may want to disclose it (peer
  seat `C1Cherrypick` covers the same question).
- The cited-but-not-qualifying row **S021** appears in the entry's `source:` line next to
  S075–S077; the C2 counter needs one qualifying row, which S075–S077 supply. No action
  needed (observation).

## Out of scope for this seat

No lane file was edited, no commit, jj command or push was run, the lane Git index was
not touched. No REA run and no web fetch: this seat only re-ran the two frozen counters
and command A and read committed blobs. The entry's content truth, the falsify wave and
the closure judge belong to other seats.

## Artifacts (scratch, sha256)

Base path `/fast/scratch/hyaku/kaidoku-r25-a3/seats/ScorecardDraft/`.
`measurements.txt` 19a4443b9a70116696b310fce2d5f7bc7c7760dd0d347ba7abde8790ec93ee6b ·
`rerun/c1-at-0e333eb2.json` 38fe3dc869a240f2327077c902cf0e59a7c8d1e102aae8ef6d4aa659e686064a ·
`rerun/c1-at-08c7a729.json` d6be83a566570f0abd6ad8b0dbc38bc83cea7bbd6e2c095e697426229ba91591 ·
`rerun/c2-at-08c7a729.json` 4f55becf0b676eb1d5cba15d57960768f996476989c1b986c615bc8ff975f2e4 ·
`cmdA/commandA.py` 236dde1da2d78b5ee2f4827fb884901857385fe1f40bbb09bbb4b4ab4f6e9b01 ·
`cmdA/cmdA-9dcd11ec…json` b702683e0a9f63439165bf6054e32fcf14a1aea1597f941949541c409e255b9a ·
`cmdA/cmdA-0e333eb2…json` 9b354f61a1a35770d52d5845231c8e1e8b759b61ce981008082ed495e65e9083 ·
`cmdA/cmdA-08c7a729…json` a856cf6f8fa67cf6cf40ae89c87c3c4e57855b35dc1d3ed74ac82b0446438a5a.
Nothing installed or upgraded; host Python 3 and git only. Values are counted at three
revisions only; the two counters are the frozen attempt-2 instruments, so this seat
confirmed what they report rather than re-deriving items I1–I5 or the SOURCES linkage
by an independent rule.
