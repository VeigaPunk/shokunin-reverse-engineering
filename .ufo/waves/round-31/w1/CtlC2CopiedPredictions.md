# R31-C2 control — CtlC2CopiedPredictions

CONTROL CtlC2CopiedPredictions: met=no score=0/23

## Result and mutation verdict

**Observation:** the specified prediction-copy control did not meet the frozen target. All 23 requests were rejected by the committed/live full-envelope comparison, while both documentation gates passed. The counter exited 1, not 0.

**Attack verdict: holds against this assigned negative control.** No counter clause let the fabrication through. This is not a judgment of either lane claim or a positive claim-data run.

**Formal mutation verdict: inconclusive, not killed.** The pristine pre-data revision itself exits 1 because its committed envelopes and documentation are absent. Therefore there is no passing pristine baseline from which to claim a killed mutant. The narrower observed result is that fabricated observations score 0/23 despite satisfying the documentation gates.

**Axes:** sandbox containment; discrimination of predictions from observations; byte-exact restoration and reproducible receipts.

## Mutant built

- Isolated clone: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone`. Branch: `ctl`. Freeze: `35ba7c522dba55f9be27eb161d4254eacaa24330`.

- Control commit: `82a64676fcaa9a4e6de2b42e867a636f119aca4a`. The sandbox-only commit command exited 0; UTC interval 2026-10-23T04:11:55+00:00 through 2026-10-23T04:11:56+00:00. Exact commit output excerpt: `25 files changed, 387 insertions(+)`.

- Created `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` with `cites S092`, a `junk` line, and every one of the 23 frozen request ids.

- Appended to `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/SKILL.md` a line naming `inspect-sqlite-database` and the entry, followed by exactly one junk-control table row per prediction: backticked id, predicted code or `accept`, and the unchanged prediction message. The table retained literal `{P}` placeholders as required by the junk-row recipe. No substantive decision guidance was added.

- Created 23 JSON files under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes` from the frozen predictions, not from REA output: 20 refusal envelopes contained only `ok=false`, predicted error code, and the one predicted issue (JSON issue path, reason, and message with `{P}` replaced by the request path); three acceptance envelopes contained only `ok=true` and `data.operation=inspect_sqlite_database`.

- No counter, oracle, frozen prediction, claim, carrier, mutant, package, or lane documentation was modified. The only lane write is this report. No claim envelopes were collected or written in the lane.

- The committed mutation is preserved in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/control.patch` and in the clone Git objects. All changed-file control hashes are below and in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/control-hashes.json`.

## Expected detector

`/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/tools/round-31/c2-sqlite-refusals.py` is unmodified. Its `committed_check` (lines 232–248) compares committed and live envelopes after removing only top-level `meta`; lines 244–245 reject unequal full envelopes. Measure mode applies this check only after the live prediction predicate has matched (lines 341–345).

**Expected:** fabricated minimal envelopes must not satisfy the target, even with `entry_ok=1` and `skill_ok=1`; the discriminating failure should be `committed envelope differs from the live envelope (full comparison)`. **Observed:** precisely that failure for all 23 rows, as reproduced in full below.

**Inference from the counter control flow:** the live half of each prediction matched in this run, since the recorded full-comparison reason is produced only after that half returns `P2-match`. This does not turn the fabricated committed records into observations.

**Unknown:** the counter does not print or retain each live JSON body in measurement mode, so this receipt does not identify the exact non-meta field difference for each row. No extra REA run was made to manufacture that evidence.

## Exact bounded detector invocations and full output

All three invocations used cwd `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions` and environment `TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/tmp` with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset. The shell-equivalent counter commands below reproduce the actual argv and cwd. The outer capture harness was `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/run-counter.py`; its own invocation was also capped by `timeout 900`. The harness waited for the counter, saved stdout/stderr as bytes, and performed process-group cleanup. No background service was started.

### Pristine comparison before the control commit

UTC start: `2026-10-23T04:10:46+00:00`. UTC end: `2026-10-23T04:11:07+00:00`. **Exit code: 1.**

Counter command:

```sh
cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions && timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Producing capture command:

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/run-counter.py baseline 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Full counter stdout (unabridged; receipt metadata is not part of stdout):

```text
q-rowlimit-no-table	P2-miss	committed envelope absent
q-columns-no-table	P2-miss	committed envelope absent
q-scope-no-table	P2-miss	committed envelope absent
q-missing-table	P2-miss	committed envelope absent
q-case-table	P2-miss	committed envelope absent
q-view-as-table	P2-miss	committed envelope absent
q-missing-column	P2-miss	committed envelope absent
q-virtual-rows	P2-miss	committed envelope absent
q-shadow-rows	P2-miss	committed envelope absent
q-ok-rows	P2-miss	committed envelope absent
m-missing	P2-miss	committed envelope absent
m-enotdir	P2-miss	committed envelope absent
m-not-sqlite	P2-miss	committed envelope absent
m-bad-pagesize	P2-miss	committed envelope absent
m-journal-hot	P2-miss	committed envelope absent
m-journal-short	P2-miss	committed envelope absent
m-journal-empty	P2-miss	committed envelope absent
m-journal-zero28	P2-miss	committed envelope absent
m-journal-symlink	P2-miss	committed envelope absent
m-db-symlink	P2-miss	committed envelope absent
m-directory	P2-miss	committed envelope absent
m-over-256mib	P2-miss	committed envelope absent
m-wal-over	P2-miss	committed envelope absent
requests=23 matches=0 target=23 entry_ok=0 (entry absent) skill_ok=0 (SKILL names neither the verb nor the entry)
```

Full counter stderr: empty (0 bytes).

Raw stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/baseline.stdout`; SHA-256 `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0`. Receipt: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/baseline.receipt.json`.

### Committed fabricated-observation control

UTC start: `2026-10-23T04:11:59+00:00`. UTC end: `2026-10-23T04:12:21+00:00`. **Exit code: 1.**

Counter command:

```sh
cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions && timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone --rev HEAD
```

Producing capture command:

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/run-counter.py control HEAD
```

Full counter stdout (unabridged; receipt metadata is not part of stdout):

```text
q-rowlimit-no-table	P2-miss	committed envelope differs from the live envelope (full comparison)
q-columns-no-table	P2-miss	committed envelope differs from the live envelope (full comparison)
q-scope-no-table	P2-miss	committed envelope differs from the live envelope (full comparison)
q-missing-table	P2-miss	committed envelope differs from the live envelope (full comparison)
q-case-table	P2-miss	committed envelope differs from the live envelope (full comparison)
q-view-as-table	P2-miss	committed envelope differs from the live envelope (full comparison)
q-missing-column	P2-miss	committed envelope differs from the live envelope (full comparison)
q-virtual-rows	P2-miss	committed envelope differs from the live envelope (full comparison)
q-shadow-rows	P2-miss	committed envelope differs from the live envelope (full comparison)
q-ok-rows	P2-miss	committed envelope differs from the live envelope (full comparison)
m-missing	P2-miss	committed envelope differs from the live envelope (full comparison)
m-enotdir	P2-miss	committed envelope differs from the live envelope (full comparison)
m-not-sqlite	P2-miss	committed envelope differs from the live envelope (full comparison)
m-bad-pagesize	P2-miss	committed envelope differs from the live envelope (full comparison)
m-journal-hot	P2-miss	committed envelope differs from the live envelope (full comparison)
m-journal-short	P2-miss	committed envelope differs from the live envelope (full comparison)
m-journal-empty	P2-miss	committed envelope differs from the live envelope (full comparison)
m-journal-zero28	P2-miss	committed envelope differs from the live envelope (full comparison)
m-journal-symlink	P2-miss	committed envelope differs from the live envelope (full comparison)
m-db-symlink	P2-miss	committed envelope differs from the live envelope (full comparison)
m-directory	P2-miss	committed envelope differs from the live envelope (full comparison)
m-over-256mib	P2-miss	committed envelope differs from the live envelope (full comparison)
m-wal-over	P2-miss	committed envelope differs from the live envelope (full comparison)
requests=23 matches=0 target=23 entry_ok=1 (ok) skill_ok=1 (ok)
```

Full counter stderr: empty (0 bytes).

Raw stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/control.stdout`; SHA-256 `7b1be42a1d13d409178cca7b6fda6db9aac319de14611686354cb12acab011c5`. Receipt: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/control.receipt.json`.

### Restored-byte comparison

UTC start: `2026-10-23T04:13:04+00:00`. UTC end: `2026-10-23T04:13:31+00:00`. **Exit code: 1.**

Counter command:

```sh
cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions && timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Producing capture command:

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/run-counter.py restored 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Full counter stdout (unabridged; receipt metadata is not part of stdout):

```text
q-rowlimit-no-table	P2-miss	committed envelope absent
q-columns-no-table	P2-miss	committed envelope absent
q-scope-no-table	P2-miss	committed envelope absent
q-missing-table	P2-miss	committed envelope absent
q-case-table	P2-miss	committed envelope absent
q-view-as-table	P2-miss	committed envelope absent
q-missing-column	P2-miss	committed envelope absent
q-virtual-rows	P2-miss	committed envelope absent
q-shadow-rows	P2-miss	committed envelope absent
q-ok-rows	P2-miss	committed envelope absent
m-missing	P2-miss	committed envelope absent
m-enotdir	P2-miss	committed envelope absent
m-not-sqlite	P2-miss	committed envelope absent
m-bad-pagesize	P2-miss	committed envelope absent
m-journal-hot	P2-miss	committed envelope absent
m-journal-short	P2-miss	committed envelope absent
m-journal-empty	P2-miss	committed envelope absent
m-journal-zero28	P2-miss	committed envelope absent
m-journal-symlink	P2-miss	committed envelope absent
m-db-symlink	P2-miss	committed envelope absent
m-directory	P2-miss	committed envelope absent
m-over-256mib	P2-miss	committed envelope absent
m-wal-over	P2-miss	committed envelope absent
requests=23 matches=0 target=23 entry_ok=0 (entry absent) skill_ok=0 (SKILL names neither the verb nor the entry)
```

Full counter stderr: empty (0 bytes).

Raw stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/restored.stdout`; SHA-256 `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0`. Receipt: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/restored.receipt.json`.

The control target was **not met**: its observed summary was `requests=23 matches=0 target=23 entry_ok=1 (ok) skill_ok=1 (ok)`, exit 1. Neither documentation nor freeze-date absence caused these 23 misses; every reason explicitly names full comparison. No `PIN ... absent or altered` output occurred in any invocation.

## Restoration evidence and changed-file hashes

After the control run, the appended lines were removed with the surgical edit tool and the 24 files created by this seat were removed. The clone working-tree bytes/states were restored to the freeze; the control commit remains at `ctl`/`HEAD` for evidence, so this is intentionally an uncommitted restoration relative to that control commit. The restored counter therefore selected `--rev 35ba7c522dba55f9be27eb161d4254eacaa24330`, exactly as the pristine run did. No destructive Git restore/reset or lane Git write was used.

Producing hash operation: `hashlib.sha256(path.read_bytes()).hexdigest()` with explicit `ABSENT` states, in the successful `functions.eval` cells “Building copied prediction records”, “Committing isolated control fixture”, and “Recording restoration byte identities”. These are in-process tool operations (process exit code not applicable); the hash receipts record UTC times `2026-10-23T04:11:30+00:00`, `2026-10-23T04:11:56+00:00`, and `2026-10-23T04:13:31+00:00`. The restoration cell printed exactly `RESTORATION True INSTRUMENTS True`.

**Observation:** all 25 changed path states equal their pristine states after restoration. The five frozen instrument/input hashes below are unchanged in pristine, control, and restored states. Pristine and restored counter stdout are byte-identical (SHA-256 above), and both exit 1.

| Absolute clone path | Pristine SHA-256/state | Control SHA-256 | Restored SHA-256/state |
|---|---|---|---|

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/SKILL.md` | `3e5cbfbc44c30fe686abe1177fe501c1c0c9e1ab141be97ed83b787b6401c31a` | `f82de07dc2335395f22521d05379d349087c3bce959c629c050f911019a93459` | `3e5cbfbc44c30fe686abe1177fe501c1c0c9e1ab141be97ed83b787b6401c31a` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` | `ABSENT` | `7b81a30139b83de32a3db57d7ad033bfc94a34a5991a216b7a202a12f032f49d` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/q-rowlimit-no-table.json` | `ABSENT` | `64ba824ef52bd3d8b1b21ee0ead3397505e0603d4642ae8638aa16e5d345d500` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/q-columns-no-table.json` | `ABSENT` | `8d4cc25730aa4267a23c3ef15185cb20f32149984613d8cb074400571e9df21a` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/q-scope-no-table.json` | `ABSENT` | `2b745b37ddc3d214b965bf7d0fd5261533f763b8bcd808e5b318265d5a477f16` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/q-missing-table.json` | `ABSENT` | `51458672dfc3d4392f7f600c27b4d833c78e6180c3f29a023a877bf5ffef63a1` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/q-case-table.json` | `ABSENT` | `b1edd405ce12d1b9dbaebd589fcaf48dc5aabb76effa52ecd1dbb00c3631ab9d` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/q-view-as-table.json` | `ABSENT` | `0b462554336a5cae2952a17aac0a3c3b6560347ef379d91f1b1dbd7e0886820d` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/q-missing-column.json` | `ABSENT` | `d2ee3a9f66ed34f153e440e3b680997fd0004d0a5c8620476cb383f215ea80c2` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/q-virtual-rows.json` | `ABSENT` | `e5bdd0bd5eafb5b97d2008dd87c16bb929c5480c1f19ad4094f53b43f18640c4` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/q-shadow-rows.json` | `ABSENT` | `5cbb076293e9a174582f584f2f7f79c8cce2891e9557ca2bc9ecadaf1b1671f8` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/q-ok-rows.json` | `ABSENT` | `01d5a93da7761c6fc2664904432e5cd06dcf4ec5cab177c948914a07ddf12958` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/m-missing.json` | `ABSENT` | `2a41432fa5f65e2715f260d1daada7ba33c825cbfdcc85d7c6402fcc9fe8d8ef` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/m-enotdir.json` | `ABSENT` | `612c59375f0e1216fe1ed1902aa5e50636e9deb4f657e0019866156684a0c643` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/m-not-sqlite.json` | `ABSENT` | `cbe24db16ac112fc4cc342f4b5c3cc0e4e93c02776b7cd2ebb4c92407aa82720` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/m-bad-pagesize.json` | `ABSENT` | `cbe24db16ac112fc4cc342f4b5c3cc0e4e93c02776b7cd2ebb4c92407aa82720` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/m-journal-hot.json` | `ABSENT` | `bd7c990950674d7c9ecfceff5058a187e238f3591da22b19e9021d0ed29e12e3` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/m-journal-short.json` | `ABSENT` | `4ac572ecc0fcadfdbd61b7f713d1a6c104db6c46c558e69883d74e6aedb98c38` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/m-journal-empty.json` | `ABSENT` | `01d5a93da7761c6fc2664904432e5cd06dcf4ec5cab177c948914a07ddf12958` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/m-journal-zero28.json` | `ABSENT` | `01d5a93da7761c6fc2664904432e5cd06dcf4ec5cab177c948914a07ddf12958` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/m-journal-symlink.json` | `ABSENT` | `53b02f3be02129f74f810ba393c280e23909e4a4ae377259ec237940339bddd7` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/m-db-symlink.json` | `ABSENT` | `1b21d5f913ca827e513ae0775a060730d2ca464c9b9bbcedf49d6dcb317be31e` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/m-directory.json` | `ABSENT` | `0a51a89ce31c675115c46daa6af3ba9243c6e553eb7b59af88cc9680cfeda145` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/m-over-256mib.json` | `ABSENT` | `9a4d5b107aefec810346d4ede0fff1cafd51f9fc2482675dd77b8dbeaff0fcfc` | `ABSENT` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/envelopes/m-wal-over.json` | `ABSENT` | `ba5e38179ba8c250d53869b0274643e28068dc4f91fde77013c5c1d9919fc180` | `ABSENT` |


Frozen instruments/inputs (same SHA-256 in all three states):

| Absolute clone path | SHA-256 |
|---|---|

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/tools/round-31/c2-sqlite-refusals.py` | `d23948959835038f4622261b551616863af1e47f3c66a558b8f3b5a232e28223` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/tools/round-31/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/.ufo/waves/round-31/claims.json` | `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c1/carriers.tsv` | `46f180b837b77297cfba11f4cc805d9f849034e411c279bf5744fa6c21c19211` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/corpus/evidence/round-31/c2/predictions.tsv` | `acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8` |


## Artifact inventory

All artifacts are below `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions`. Each of the 21,551 clone files/links (including its Git evidence) is listed with its SHA-256 in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone-inventory.json`. Each non-clone artifact, including the 535 generated Node compile-cache files below `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/tmp`, is listed individually with its SHA-256 in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/artifact-inventory.json`. Symlink entries explicitly hash the link target bytes. The inventories are identity evidence, not additional behavioral tests.

| Artifact | SHA-256 |
|---|---|

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/baseline.receipt.json` | `9e066e3f153618ca708d78544e5365a6c5e573cd71f6c74d153b762c7a9873bf` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/baseline.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/baseline.stdout` | `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/before-hashes.json` | `71d4911ba673739515321a502971b5a5a34423f0b8be2a1fef54301688833e6f` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone-inventory.json` | `9908f4dd19c258991b4edf8bdd2f89c84ddaf4045564039e96408b0aee319ff2` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/control-commit.receipt.json` | `70f582358c7ed5bf9e158a0e32aab796ac6612a490db7cd3972b0b978cc41732` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/control-hashes.json` | `07bd4fba3ceccba60bdaf190ed82d16eb4d85e2d7fe9788f5ae22e0cb7aace5b` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/control.patch` | `b37c80240104e36d3e5981baf52d1663a7eab5855bfa0782aab0a2b5d0fc30d4` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/control.receipt.json` | `407581cd7f06fedb8313b8751f2a2f78960e9ac4ccbcc536eafe2ec5f89144b7` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/control.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/control.stdout` | `7b1be42a1d13d409178cca7b6fda6db9aac319de14611686354cb12acab011c5` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/restoration-hashes.json` | `5cc1b16d86fc808815b5f15338858fe46942147c1fb9b9492bb88b7199766149` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/restored.receipt.json` | `38ad5667ca14e0de8546f909e41d19fad3048d03275169746725548b77515582` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/restored.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/restored.stdout` | `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/run-counter.py` | `62ba7343b7f2c19b3a7f4587259fd16422a4d08b3d5130b5b955a0fbb83eb089` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/sources.json` | `474d6d527979e71fb166fa3238e711c9e630bbed7e4ed71c2bd49913ddf3ced1` |

| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/artifact-inventory.json` | `4191433e42b820326325430ea288d71e36935588a16ab26a40c298bd6aaae8e6` |


The artifact inventory excludes itself to avoid a self-hash cycle; its hash is recorded above. It includes the clone-inventory file, whose entries cover the clone. This report is the only artifact outside the seat, as required.

## Sources opened

Access date for every source: **2026-10-23**. Sources were ordinary local-file reads; no browser, challenge bypass, external source fetch, or additional runtime was invoked. SHA-256 below identifies the entire local source file; each short quotation is located in the opened source lines. These records are also preserved in the source inventory.

| Local source URL | SHA-256 | Located quote (≤25 words) |
|---|---|---|

| [file:///home/vgpnk/.agents/skills/godspeed/SKILL.md](file:///home/vgpnk/.agents/skills/godspeed/SKILL.md) | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | line 12: `1. **Name the axes.**` |

| [file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md](file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md) | `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692` | line 28: `Invoke REA as a CLI instead.` |

| [file:///home/vgpnk/.omp/agent/RULES.md](file:///home/vgpnk/.omp/agent/RULES.md) | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | line 14: `- Record every install or update — tool, version, channel, reason — in your report or handoff.` |

| [file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c2-sqlite-refusals.py](file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c2-sqlite-refusals.py) | `d23948959835038f4622261b551616863af1e47f3c66a558b8f3b5a232e28223` | line 245: `return False, "committed envelope differs from the live envelope (full comparison)"` |

| [file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/claims.json](file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/claims.json) | `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` | line 31: `"target": "requests=23 matches=23 target=23 entry_ok=1 skill_ok=1, exit 0"` |

| [file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c2/predictions.tsv](file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c2/predictions.tsv) | `acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8` | line 2: `row_limit requires an explicit table selection` |

| [file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/w1-spec.json](file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/w1-spec.json) | `c1a6a256d4d11b0dc295788e90264b7956b94bfce0dbb35039d50b1bef281ec4` | line 45: `R31-C2 pre-data control: junk-row` |

| [file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/SKILL.md](file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2CopiedPredictions/clone/SKILL.md) | `3e5cbfbc44c30fe686abe1177fe501c1c0c9e1ab141be97ed83b787b6401c31a` | line 996: `### Round-30 measurement registry` |


## Tooling and scope

- No tools were installed or updated by this seat. The existing frozen `rea-agents@6.5.0` CLI was invoked only through the assigned counter. The general skill’s newer example pin was not substituted for the frozen assignment pin.

- No subagents were dispatched; no peer messages, carrier/mutant changes, immutable-flag changes, lane/fleet Git writes, or sibling-source edits were made. No build, lint, formatter, selftest, broader runtime, or claim-data integration was run.

- Completed only this assigned fabrication probe, its requested pristine comparison, and its required restored-byte comparison. No passing-baseline mutant kill or broader claim verification is asserted.
