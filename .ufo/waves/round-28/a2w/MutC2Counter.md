# MutC2Counter — mutation test of the R28-C2 counter

Target: `tools/round-28/c2-filtered-flag.py` (lane commit `9db24c9e`, pristine sha256
`4fdf7db81c5e56b3dfe8232ae87b89e3090e047f979adb088550381095fd60ef`). Seat: sandbox clone
`/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutC2Counter/clone` (`git clone -q` of the lane); the
lane was never modified and the counter ran against it as a read-only `--root` only.
Date 2026-10-22, all times UTC.

**Verdict: holds.** 12 of 16 mutants were killed by `--selftest`; the rule check, pin check,
provenance checks and entry checks all resisted mutation. The 4 survivors are **coverage gaps in
the selftest and in the live corpus, not defects in the counter** — each is a genuine deviation
(proved by a probe), but no shipped case distinguishes it.

**Method.** Each mutant = one edit to the pristine bytes, kept in `mutants/`. Per mutant: run
`--selftest` on the mutant bytes; run the real count `python3 <mutant> --root <lane> --rev
a267311678309fd17772407e8afa122ec3219289`; restore the pristine bytes and check sha256.
Harness `mutate.py`, survivor probes `probe_survivors.py`, both in the seat dir. Baseline
(pristine): selftest 17 of 17 ok, exit 0; real count at `a2673116`
`responses_complete=230/230 entries=246 mismatches=0 predicted_true=59 entry_ok=0`, exit 1,
`FAIL entry absent` (the knowledge entry does not exist at that commit); at the lane tip
`9db24c9e` the same numbers give `entry_ok=1`, exit 0.

## Per-mutation results (16 mutants)

`real count` = summary line at `a2673116`; `tip` = exit code at `9db24c9e`. That rev predates the
knowledge entry, so `entry_ok` is 0 and the exit code is 1 for every mutant there; the
discriminating signal there is the summary line. The tip carries the entry, so its exit code is
the clean pass/fail signal. Diffs `runs/mutation-diffs.txt`, outputs `runs/<id>-*.txt`.

| # | Mutation (file:line) | selftest | real count at a2673116 | tip |
|---|---|---|---|---|
| M1 | `:188` name compare made case-insensitive | **survived** | unchanged | 0 |
| M2 | `:188` ignore canonical membership | killed (2 cases) | **changed** `mismatches=177 predicted_true=236` | 1 |
| M3 | `:163` drop fetch-time-after-counter check | killed | unchanged | 0 |
| M4 | `:158` drop URL check | killed | unchanged | 0 |
| M5 | `:186` count only the first entry per selector | killed | **changed** `entries=182 predicted_true=0` | 1 |
| M6 | `:165` drop sha256-of-bytes check | killed | unchanged | 0 |
| M7 | `:160` drop status!=200 check | killed | unchanged | 0 |
| M8 | `:168` drop first-commit-after-counter check | **survived** | unchanged | 0 |
| M9 | `:190` identity `is not` → equality `!=` on `filtered` | killed | unchanged | 0 |
| M10 | `:188` invert name comparison | killed | **changed** `mismatches=69 predicted_true=10` | 1 |
| M11 | `:122` drop entry `mismatches M of N` phrase check | killed | unchanged | 0 |
| M12 | `:133` drop `## Gate` membership check | killed | unchanged | 0 |
| M13 | `:133` drop `opened == 2026-10-22` check | **survived** | unchanged | 0 |
| M14 | `:132` drop "new since base" check | **survived** | unchanged | 0 |
| M15 | `:173` drop `ok=true`/selector-key check | killed | unchanged | 0 |
| M16 | `:158` weaken URL check to presence-only | killed | unchanged | 0 |

## Survivors: probe evidence that each is a real deviation

Probe repositories built in `/tmp` by `probe_survivors.py` (read-only on the lane); each
exercises exactly the branch the mutant removed; pristine and mutant then run on the same repo.
All four differ on the probe, so each is a real deviation, not an equivalent mutant.
- **M1** (case-insensitive compare). Candidate `Transfer(address,uint256)` vs canonical
  `transfer(address,uint256)`: pristine `mismatches=1 predicted_true=1 entry_ok=0`; mutant
  `mismatches=0 predicted_true=0 entry_ok=1`. The upstream rule is case-sensitive (source read
  below), so the pristine compare is right; 0 of 246 live entries differ from their canonical
  signature by case only, so the corpus cannot exercise the branch either.
- **M8** (first-commit-after-counter guard). Response bytes committed before the counter:
  pristine `FAIL openchain-a9059cbb.json: first committed before the counter`,
  `responses_complete=0/1`; mutant `responses_complete=1/1`. 0 of the 230 live response files
  predate the counter commit.
- **M13** (opened-date check). Cited row opened `2026-10-21`: pristine `FAIL source: line names
  no S### new since base, mined, opened 2026-10-22 and in ## Gate`, `entry_ok=0`; mutant
  `entry_ok=1`. The selftest has no wrong-date case; the shipped S084 row is opened `2026-10-22`.
- **M14** (new-since-base check). Cited row already in the base SOURCES.md: pristine `entry_ok=0`
  with the same FAIL line; mutant `entry_ok=1`. The selftest's `red-entry-old-row` case is caught
  by the opened-date check, so removing the base check alone still fails that case.

These four are coverage findings. They do **not** license changing the rule or the checks; the
fix is four more selftest cases (case-only name difference; response file committed before the
counter; cited row opened on another date; cited row present in the base) and, for M1, a corpus
entry differing from its canonical signature by case only.

**Source read for the M1 verdict.** Local file read, no fetch:
`/fast/scratch/hyaku/kaidoku-r28/src/sourcify/services/4byte/src/api/handlers.ts`, sha256
`30981efbc7bc1b541954eb75767c8154562f4f77a9bfc1ad22cf19c8996c5a38`, checkout at commit
`189cd726f7ed8fb3d2f503402d5c133e0f50e1fd`, opened 2026-10-22; quote at lines 47-48:
`signatureItem.filtered = signatureItem.name !== expectedCanonical.signature;`

## Restoration evidence

After every mutant the pristine bytes were written back and hashed; the assertion
`sha256(restore) == 4fdf7db81c5e56b3dfe8232ae87b89e3090e047f979adb088550381095fd60ef` passed 16
of 16 times, so the lane file, the sandbox clone file and `runs/pristine-counter.py` all end at
that hash. `git -C <lane> status --porcelain -- tools/ corpus/` is empty; no git write, add,
commit, checkout or ref update was performed in the lane; the pristine selftest re-run after the
last restore prints `selftest cases=17 failures=0`.

## Artifacts (all under `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutC2Counter/`)

- `mutate.py` sha256 `29eb28cdb1991ad678265930872faae87521161d9a213429cc54f830ebd27727`;
  `probe_survivors.py` sha256 `08f90e28d7dd02cd8e7dbfbb4839ad7d54300105c14681b7391d00a353b2088b`
- `runs/pristine-counter.py` sha256 `4fdf7db81c5e56b3dfe8232ae87b89e3090e047f979adb088550381095fd60ef`;
  `runs/mutation-diffs.txt` sha256 `d9db8039c490c81719abe934ecd5ad4a39856b8811433cde49e8d958fc3277ef`
- `runs/survivor-probes.txt` sha256 `ac4ff290a7af203b30e461efd4cac69e251e5c750c6048639521e63d97ca0fed`;
  `runs/summary.tsv`, `runs/M0-*.txt`, `runs/<id>-*.txt` (48 per-mutant output files);
  `mutants/<id>.mutant.py` (16 patched copies; sha256 each in the seat dir)
- No tool was installed or upgraded for this task.
