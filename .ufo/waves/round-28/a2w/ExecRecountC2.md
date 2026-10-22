# R28-C2 counter and selftest re-run (ExecRecountC2)

Seat: KaidokuR28a2.ExecRecountC2 (executor, leaf). 2026-10-22 UTC. Lane read-only except this report: no lane file edited, no git write, no jj, no network fetch, no tool installed.

## Answer

The counter re-runs cleanly. At the assigned rev `a267311678309fd17772407e8afa122ec3219289` it prints `responses_complete=230/230 entries=246 mismatches=0 predicted_true=59 entry_ok=0` and exits 1, because the knowledge entry was not yet committed at that rev. Every other counted quantity already meets the frozen target; the single FAIL line is `FAIL entry absent`. The selftest passes all 17 cases, 0 failures, exit 0.

The lane tip advanced during this wave to `9db24c9e10287d44d9f780d782ab608f3c84ff5a` (entry, S084-S086 SOURCES rows, round-28 lesson), then to `2832c5b3e20d84729bbd7f1b30afc081de9557b5` (hygiene). The same counter at either tip prints the same counts with `entry_ok=1` and exits 0, which is the frozen target state.

## Commands, exit codes, exact stdout

1. `git clone -q <lane> <seat>/clone` then `python3 -I -B tools/round-28/c2-filtered-flag.py --root <seat>/clone --rev a267311678309fd17772407e8afa122ec3219289` — 18:23:44Z to 18:23:45Z, exit 1. stdout tail (exact, 2 lines):
   `FAIL entry absent`
   `responses_complete=230/230 entries=246 mismatches=0 predicted_true=59 entry_ok=0`
2. Same command again, same rev: exit 1, byte-identical stdout (diff of the two captures reported no difference). The counter is deterministic.
3. `python3 -I -B tools/round-28/c2-filtered-flag.py --selftest` from the clone working tree: 18:23:50Z, exit 0.
4. Same selftest from `/tmp` with `TMPDIR` pointed at the seat dir, running the clone's copy by absolute path: exit 0, same summary. The selftest does not depend on the working directory.
5. Counter at the claim base `935c36608008f79e3dea4f1ed191df3c89e3b848`: exit 2, stdout `PIN pinned input absent: corpus/evidence/round-28/c2/selectors.tsv`. Matches the frozen before receipt (`.ufo/waves/round-28/before/c2-at-935c3660.txt`, exit 2, pinned inputs absent).
6. Extra, outside the assignment: clone `<seat>/clone-tip` (tip `9db24c9e...`), counter with `--rev 9db24c9e10287d44d9f780d782ab608f3c84ff5a`: 18:24:08Z to 18:24:09Z, exit 0, stdout `responses_complete=230/230 entries=246 mismatches=0 predicted_true=59 entry_ok=1`.
7. Extra: the same counter with `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 9db24c9e...` against the live lane (the counter runs only `git show` and `git log`): exit 0, stdout `responses_complete=230/230 entries=246 mismatches=0 predicted_true=59 entry_ok=1`.
8. Extra: clone `<seat>/clone-tip2` (tip `2832c5b3...`), counter with `--rev 2832c5b3...`: 18:26:50Z, exit 0, stdout `responses_complete=230/230 entries=246 mismatches=0 predicted_true=59 entry_ok=1`. The passing result holds at every tip that carries the entry.

## Selftest summary (exact stdout, 18 lines)

```
ok green-both-branches exit=0 want=0
ok red-flag-flipped-canonical-alternative exit=1 want=1
ok red-flag-flipped-canonical-name exit=1 want=1
ok red-flag-on-non-canonical exit=1 want=1
ok red-flag-not-boolean exit=1 want=1
ok red-missing-response exit=1 want=1
ok red-selector-key-absent exit=1 want=1
ok red-early-fetch exit=1 want=1
ok red-sha exit=1 want=1
ok red-url exit=1 want=1
ok red-status exit=1 want=1
ok red-no-canonical-branch exit=1 want=1
ok red-entry-wrong-count exit=1 want=1
ok red-entry-old-row exit=1 want=1
ok red-row-not-in-gate exit=1 want=1
ok red-row-status exit=1 want=1
ok red-pin-refusal exit=2 want=2
selftest cases=17 failures=0
```

Exit 0. One green case and sixteen red cases, each red case asserting a distinct failure mode: flag flips on canonical and non-canonical selectors, a non-boolean flag, a missing response, an absent selector key, a fetch before the counter commit, a wrong sha256, a wrong URL, a wrong HTTP status, a removed canonical alternative, a wrong entry count, an old SOURCES row, a row missing from the lesson Gate, a wrong SOURCES status, and a pin refusal.

## Independent recount (does not use the counter)

To check the counter is not merely self-consistent, I recomputed the counts straight from the committed bytes with my own script: read the 230 selectors and the pinned canonical list at the tip rev, read each `corpus/evidence/round-28/c2/db/openchain-<selector>.json` plus its manifest entry, check `ok is true`, check the manifest sha256 against the file bytes, apply the rule `filtered == (selector is a canonical key and name != canonical signature)` and compare.

Output: `independent: responses_complete=230/230 entries=246 mismatches=0 predicted_true=59 empty_selectors=48 entries_on_canonical_selectors=69` and `independent: problems=0 []` (sha256 `62a742bfb270421c867e6570188bcf237de7e1c7f35974511b7ae511d11beb55`, exit 0). Every counted quantity agrees with the counter. The same script shows the pinned canonical list has 36 keys, 10 of the 230 selectors are canonical keys (all 10 from the round-25 set; none of the 187 round-28 held-out selectors is canonical), 48 responses hold an empty or null candidate list, and 69 candidate entries sit on the 10 canonical selectors. The 10 canonical names are among the 187 predicted-false entries, so the committed entry's own numbers (10 plus 177) are consistent.

## Frozen-instrument check

The counter file is byte-identical at both revs to the frozen instrument in `.ufo/waves/round-28/claims-c2.json` (`tools/round-28/c2-filtered-flag.py`, sha256 `4fdf7db81c5e56b3dfe8232ae87b89e3094e047f979adb088550381095fd60ef`): the working-tree copy in the clone, `git show a2673116:tools/round-28/c2-filtered-flag.py` and the copy at the tip all hash the same, so the counter did not change between the data commit and the tip. No `PIN` line appeared at `a2673116` or at the tip, so the pinned selectors list and canonical list still hash to the frozen values `ad1b50982922ed69f6953b490716746adb5d5587c4395d29489b1db7fab464ae` and `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2`.

## Labels

- Observation: every counter line, exit code, selftest line and independent recount line quoted above, each produced by the commands listed with their UTC times.
- Observation: the counter file hash at `a2673116` and at the tip is `4fdf7db81c5e56b3dfe8232ae87b89e3094e047f979adb088550381095fd60ef`.
- Inference (strong): the R28-C2 frozen target is met at the lane tip. The target needs `entry_ok 1`, which needs the committed entry, the new SOURCES row and the lesson Gate row; those exist at `9db24c9e` and the counter exits 0 there. Record the re-run rev as `9db24c9e...` or later (both tips pass), not `a2673116`, where the entry is still absent.
- Unknown: which revision of the service actually serves `api.openchain.xyz` is outside this seat; the counter reads only committed bytes and cannot show it. The entry already states that limit.

## Risks and blockers

- No blocker. The one exit-1 condition at the assigned rev is a rev-age artifact, not a data defect.
- Risk for the L1: quoting the count at `a2673116` (the data commit) as the claim result would report `entry_ok=0` and exit 1. The passing rev is a tip that commits the entry.
- Observation: the lane working tree carried uncommitted edits from other seats while I worked (SOURCES.md, PROVINCE.md, SCORECARD.md, corpus/README.md, QUALITY.md, the round-28 entries, plus new `tools/round-28/preseen-overlap.py` and `.ufo/waves/round-28/after/preseen-overlap-c2.txt`). My runs use `--rev` over committed bytes and are unaffected. I changed none of them.

## Artifacts and files changed

Directory `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/ExecRecountC2/`:

| path | sha256 |
|---|---|
| `count.out` (assigned-rev stdout) | `a018cb84dd9217a22fe6e3554deadbf10ae0b55b71ef1df3cbb92fde22a64476` |
| `count2.out` (repeat stdout, identical) | `a018cb84dd9217a22fe6e3554deadbf10ae0b55b71ef1df3cbb92fde22a64476` |
| `selftest.out` | `d6dd57b1a59bf465321d19b9852a5090a774e5d0ab0c1e39cf16a3051f0f12fb` |
| `independent/recount.py` | `62a742bfb270421c867e6570188bcf237de7e1c7f35974511b7ae511d11beb55` |
| `clone/` | sandbox clone at `a267311678309fd17772407e8afa122ec3219289` |
| `clone-tip/` | sandbox clone at `9db24c9e10287d44d9f780d782ab608f3c84ff5a` |
| `clone-tip2/` | sandbox clone at `2832c5b3e20d84729bbd7f1b30afc081de9557b5` |

Environment: Python 3.14.8, git 2.56.0, Linux 7.2.11-arch1-1. Nothing installed, so no install record is due. Lane file written: only `.ufo/waves/round-28/a2w/ExecRecountC2.md` (this report; the L1 should hash it when it commits, since the sha256 changes with each edit).
