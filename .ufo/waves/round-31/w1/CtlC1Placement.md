# CtlC1Placement — R31-C1 pre-data Core-placement control

## Result

**Observation:** neither assigned control met the frozen target. Both obtained `carriers=12 pass=12 target=12 entry_ok=1`, but `province_ok=0` and exit 1. No counter emitted a `PIN` diagnostic.

| Variant | Control met target? | Carrier score | province_ok | Exit | Attack verdict |
|---|---|---|---|---|---|
| A: row directly after `## Frontier` | no | 12/12 | 0 | 1 | holds for this control |
| B: prose only after `### Round-31 additions to Core` | no | 12/12 | 0 | 1 | holds for this control |

**Inference:** the frozen placement gate rejected both specified shortcuts even with all live/committed envelope checks satisfied. This is bounded to these two variants, not a general parser audit.

**Mutation-testing verdict: inconclusive, not killed.** The required pristine pre-data baseline already failed (missing committed data and documentation); therefore these runs do not establish a passing-baseline killed-mutant result. Neither control survived in the sense of satisfying the frozen target.

Axes: C1 coverage, nearest-heading/table-row placement integrity, exact envelope binding, and sandbox isolation. No claim contract or counter was changed.

## Control construction and isolation

- Sandbox clone: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone`; built on branch `ctl` at freeze `35ba7c522dba55f9be27eb161d4254eacaa24330`.
- Variant A commit: `6fb0ef581b1ceb2b028aa1f26be091f6af0261c3` (2026-10-23T04:12:18Z).
- Variant B commit: `f3fcfb9f3dc9d336dd82294295160ff73b17b73f` (2026-10-23T04:12:53Z), changing only PROVINCE placement from A.
- Both controls commit 12 genuine REA stdout envelopes under the correct carrier ids plus one entry citing S096 and naming all 12 returned evidence ids. No envelopes were copied into the lane.
- Entry bytes are retained at `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/entry.control.md`; SHA-256 `134abea48c40d8dce87911a40282826f02864c0a5d463f8bdf261e421c0d7f48`.
- Only the assigned report is written into the lane. All authored control files, command receipts, raw outputs and control commits remain in this seat. Immutable carriers, mutants and downloads were not modified.
- No agents, MCP devices, services, other REA versions, package installs or tool updates were used. The existing cached `rea-agents@6.5.0` was used through the required npx CLI.

Clone commands (all Git environment overrides unset):

```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone checkout -q -B ctl 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Clone-only commits used `git -c user.name=ctl -c user.email=ctl@local commit`; complete exact add/commit commands, UTC times, outputs and exit codes are in the hashed git receipts below.

Variant A inserted this exact single row immediately after the `## Frontier` line (line 74 in the variant):

```markdown
| `inspect-sqlite-database` | x | x | `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` |
```

Variant B removed that row and appended only:

```markdown
### Round-31 additions to Core

`inspect-sqlite-database` is recorded in `corpus/knowledge/2026-10-23-r31-sqlite-positive.md`.
```

## Real envelope acquisition

Producer command: `timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/probe.py envelopes` (exit 0). Each underlying command below ran in `/tmp`, with `TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/tmp`, the same REA argv as the counter, and its complete unmodified stdout was written to the corresponding clone envelope file. Every REA process exited 0. All acquisition stderr files were empty.

| Carrier | UTC start | UTC end | Exit | Exact underlying command |
|---|---|---|---|---|
| proj-341 | 2026-10-23T04:11:12+00:00 | 2026-10-23T04:11:13+00:00 | 0 | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/proj-341.db --schema-scope database --format json --full-output` |
| proj-350 | 2026-10-23T04:11:13+00:00 | 2026-10-23T04:11:15+00:00 | 0 | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/proj-350.db --schema-scope database --format json --full-output` |
| proj-361 | 2026-10-23T04:11:15+00:00 | 2026-10-23T04:11:16+00:00 | 0 | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/proj-361.db --schema-scope database --format json --full-output` |
| proj-370 | 2026-10-23T04:11:16+00:00 | 2026-10-23T04:11:17+00:00 | 0 | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/proj-370.db --schema-scope database --format json --full-output` |
| proj-371 | 2026-10-23T04:11:17+00:00 | 2026-10-23T04:11:18+00:00 | 0 | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/proj-371.db --schema-scope database --format json --full-output` |
| chinook | 2026-10-23T04:11:18+00:00 | 2026-10-23T04:11:19+00:00 | 0 | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite --schema-scope database --format json --full-output` |
| chinook-autoinc | 2026-10-23T04:11:19+00:00 | 2026-10-23T04:11:20+00:00 | 0 | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/chinook-autoinc.sqlite --schema-scope database --format json --full-output` |
| gpkg-curve | 2026-10-23T04:11:20+00:00 | 2026-10-23T04:11:21+00:00 | 0 | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-curve.gpkg --schema-scope database --format json --full-output` |
| gpkg-curvepolygon | 2026-10-23T04:11:21+00:00 | 2026-10-23T04:11:22+00:00 | 0 | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-curvepolygon.gpkg --schema-scope database --format json --full-output` |
| gpkg-line-zm | 2026-10-23T04:11:22+00:00 | 2026-10-23T04:11:23+00:00 | 0 | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-line-zm.gpkg --schema-scope database --format json --full-output` |
| gpkg-multisurface | 2026-10-23T04:11:23+00:00 | 2026-10-23T04:11:24+00:00 | 0 | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-multisurface.gpkg --schema-scope database --format json --full-output` |
| gpkg-test-gpkg-nulls | 2026-10-23T04:11:24+00:00 | 2026-10-23T04:11:25+00:00 | 0 | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-test-gpkg-nulls.gpkg --schema-scope database --format json --full-output` |

Committed control-file SHA-256 values (the same envelopes and entry in A and B; restored working-tree copies are absent as originally):

| Absolute control-file path | SHA-256 in both control commits |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/evidence/round-31/c1/envelopes/proj-341.json` | `455306ead20a77cabfa6a1e92ef94a005054f154d5a9d944e55118e1caaee3b3` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/evidence/round-31/c1/envelopes/proj-350.json` | `841bb3e449fa3422dbe26b4e2e5c546413868d0e37608937b228426f5925b2aa` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/evidence/round-31/c1/envelopes/proj-361.json` | `ff24d0707a3da45ae425336f8b9ce9a5bbe3eb91a37f4a1b3222247e802c3ec7` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/evidence/round-31/c1/envelopes/proj-370.json` | `a896ba9aec86740f7dbbd5a65d03143b25ce82897d7f76a98463e133f92afd9a` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/evidence/round-31/c1/envelopes/proj-371.json` | `d80542611e71de980e777a2bdd0b16759ba2213a9df7b796f9a316e21bf44e5b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/evidence/round-31/c1/envelopes/chinook.json` | `75f77bb98adaba709b971965c3816bcd07285b185dad76883744aee0c283571e` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/evidence/round-31/c1/envelopes/chinook-autoinc.json` | `bea63657a56b82ad74da59f1777941271e3e494ad62e8458c3f56e18cadf796e` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/evidence/round-31/c1/envelopes/gpkg-curve.json` | `9f7482cecb51e1eb9770df389319bd4174f762652168cf6da7245446a86a28ea` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/evidence/round-31/c1/envelopes/gpkg-curvepolygon.json` | `575afd17d0a47af432ea7eb4d0bb5a44120401d655bcd4268e1c42ac56d63b2d` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/evidence/round-31/c1/envelopes/gpkg-line-zm.json` | `10b34d2c64602eae0d4b51899d5fafc0859a07bf51a0a94da2c4dbd86f634d6c` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/evidence/round-31/c1/envelopes/gpkg-multisurface.json` | `7f91f70f35d7255829d6fef1d42ff441bfd742d35ad7adf581a174684faee969` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/evidence/round-31/c1/envelopes/gpkg-test-gpkg-nulls.json` | `881d9cd58b4c6ea76a2c7b0257aa43d6ccb9f3fdb928d24a1e7378dadf544ed0` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/knowledge/2026-10-23-r31-sqlite-positive.md` | `134abea48c40d8dce87911a40282826f02864c0a5d463f8bdf261e421c0d7f48` |

| PROVINCE state | Absolute retained bytes | SHA-256 |
|---|---|---|
| pristine | `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/PROVINCE.pristine.md` | `a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8` |
| variant A | `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/PROVINCE.variant-a.md` | `2505dc1eff012f23dbac23f84be190ec704a83c335d70f13f6e6799c158a5e57` |
| variant B | `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/PROVINCE.variant-b.md` | `750bfc37f90baeb12962012f271cb1364400ce376838ce7eff43fd8b6f609475` |

## Exact bounded behavioral-detector runs

For every run, working directory was `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement`, `TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/tmp`, and `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` were unset. The bounded runner invoked exactly the detector command shown below; it saved full stdout/stderr and UTC/exit metadata. The frozen counter itself ran REA live on all 12 carriers in every run. All four counter stderr streams were empty.

Frozen target: `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1`, exit 0.

### Pristine pre-data comparison

Revision resolved at execution: `35ba7c522dba55f9be27eb161d4254eacaa24330`. UTC: `2026-10-23T04:10:54+00:00` through `2026-10-23T04:11:07+00:00`. **Exit: 1. Target met: no.**

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Full stdout:

```text
proj-341	P1-fail	committed envelope absent
proj-350	P1-fail	committed envelope absent
proj-361	P1-fail	committed envelope absent
proj-370	P1-fail	committed envelope absent
proj-371	P1-fail	committed envelope absent
chinook	P1-fail	committed envelope absent
chinook-autoinc	P1-fail	committed envelope absent
gpkg-curve	P1-fail	committed envelope absent
gpkg-curvepolygon	P1-fail	committed envelope absent
gpkg-line-zm	P1-fail	committed envelope absent
gpkg-multisurface	P1-fail	committed envelope absent
gpkg-test-gpkg-nulls	P1-fail	committed envelope absent
carriers=12 pass=0 target=12 entry_ok=0 (entry absent) province_ok=0 (no PROVINCE table row names the verb and the entry)
```

Stdout SHA-256: `a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e`. Stderr: empty, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

### Variant A: table row under Frontier

Revision resolved at execution: `6fb0ef581b1ceb2b028aa1f26be091f6af0261c3`. UTC: `2026-10-23T04:12:20+00:00` through `2026-10-23T04:12:33+00:00`. **Exit: 1. Target met: no.**

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone --rev HEAD
```

Full stdout:

```text
proj-341	P1-pass	tables=36 indexes=21 views=7 triggers=35 columns=385
proj-350	P1-pass	tables=36 indexes=21 views=7 triggers=35 columns=385
proj-361	P1-pass	tables=36 indexes=21 views=7 triggers=35 columns=385
proj-370	P1-pass	tables=37 indexes=21 views=7 triggers=36 columns=395
proj-371	P1-pass	tables=38 indexes=21 views=7 triggers=36 columns=396
chinook	P1-pass	tables=11 indexes=11 views=0 triggers=0 columns=64
chinook-autoinc	P1-pass	tables=12 indexes=11 views=0 triggers=0 columns=66
gpkg-curve	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-curvepolygon	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-line-zm	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-multisurface	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-test-gpkg-nulls	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=64
carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=0 (row sits under '## Frontier', not a Core heading)
```

Stdout SHA-256: `6f99cc6cb4e3bb8868df73941c56405b25c433d6175617ae9340363badfb60af`. Stderr: empty, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

**Observation / rejecting clause:** the nearest preceding heading was `## Frontier`. The frozen counter, lines 138–141, finds the row but rejects its heading; line 201 requires `p_ok` for exit 0. All 12 carrier records and the entry passed. No clause let the control through.

CONTROL CtlC1Placement: met=no score=12/12

### Variant B: prose only under a Core-named heading

Revision resolved at execution: `f3fcfb9f3dc9d336dd82294295160ff73b17b73f`. UTC: `2026-10-23T04:12:56+00:00` through `2026-10-23T04:13:14+00:00`. **Exit: 1. Target met: no.**

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone --rev HEAD
```

Full stdout:

```text
proj-341	P1-pass	tables=36 indexes=21 views=7 triggers=35 columns=385
proj-350	P1-pass	tables=36 indexes=21 views=7 triggers=35 columns=385
proj-361	P1-pass	tables=36 indexes=21 views=7 triggers=35 columns=385
proj-370	P1-pass	tables=37 indexes=21 views=7 triggers=36 columns=395
proj-371	P1-pass	tables=38 indexes=21 views=7 triggers=36 columns=396
chinook	P1-pass	tables=11 indexes=11 views=0 triggers=0 columns=64
chinook-autoinc	P1-pass	tables=12 indexes=11 views=0 triggers=0 columns=66
gpkg-curve	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-curvepolygon	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-line-zm	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-multisurface	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-test-gpkg-nulls	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=64
carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=0 (no PROVINCE table row names the verb and the entry)
```

Stdout SHA-256: `bb706facc0e33eb379370b560600d6ce60cce7c258639210481359811e032637`. Stderr: empty, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

**Observation / rejecting clause:** the prose line did not satisfy the line-138 requirement `ln.startswith("|")`; line 142 returned `no PROVINCE table row names the verb and the entry`. A Core-named heading alone did not help. Line 201 requires `p_ok` for exit 0. No clause let the control through.

CONTROL CtlC1Placement: met=no score=12/12

### Exact-byte restoration comparison

Revision resolved at execution: `35ba7c522dba55f9be27eb161d4254eacaa24330`. UTC: `2026-10-23T04:13:31+00:00` through `2026-10-23T04:13:42+00:00`. **Exit: 1. Target met: no.**

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Full stdout:

```text
proj-341	P1-fail	committed envelope absent
proj-350	P1-fail	committed envelope absent
proj-361	P1-fail	committed envelope absent
proj-370	P1-fail	committed envelope absent
proj-371	P1-fail	committed envelope absent
chinook	P1-fail	committed envelope absent
chinook-autoinc	P1-fail	committed envelope absent
gpkg-curve	P1-fail	committed envelope absent
gpkg-curvepolygon	P1-fail	committed envelope absent
gpkg-line-zm	P1-fail	committed envelope absent
gpkg-multisurface	P1-fail	committed envelope absent
gpkg-test-gpkg-nulls	P1-fail	committed envelope absent
carriers=12 pass=0 target=12 entry_ok=0 (entry absent) province_ok=0 (no PROVINCE table row names the verb and the entry)
```

Stdout SHA-256: `a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e`. Stderr: empty, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Restoration evidence

**Observation:** at `2026-10-23T04:13:28+00:00`, the clone-only restoration command below exited 0:

```sh
timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone checkout -q --detach 35ba7c522dba55f9be27eb161d4254eacaa24330
```

PROVINCE SHA-256 before mutations and after restoration was exactly `a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8`. A direct byte comparison with `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/PROVINCE.pristine.md` also returned true. All 13 originally absent additions (entry plus 12 envelope files) were absent again. The complete 14-path before/after state is `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/restoration.json`; both `exact_target_bytes_restored` and `province_exact_bytes_restored` are true.

The restored detector stdout SHA-256 `a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e` equals the pristine baseline stdout SHA-256 exactly; both exited 1 with `pass=0`, `entry_ok=0`, `province_ok=0` as expected for the frozen pre-data tree.

Control history is retained on clone branch `ctl` at `f3fcfb9f3dc9d336dd82294295160ff73b17b73f` with A as its parent; the working checkout is detached at the pristine freeze. The authored delta is also retained losslessly as `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/control-commits.bundle`, SHA-256 `cc31f73e5595ee45e089bbd3e0003b277095d85a35ff7780fb2c245a6ebb8878` (bundle prerequisite: freeze commit). Thus exact-byte restoration did not discard the committed controls.

Every captured child command was bounded by timeout, reaped, and its process group received cleanup via the runner finally block. No persistent service was started. No further mutation or runtime probe was performed after the restored comparison.

## Opened-source provenance

Only ordinary local file reads were used for source inspection; no external documentation fetch, browser or access-control workaround was used. Access date for every source below: **2026-10-23**. SHA-256 covers the exact full local file bytes read; each quote is at most 25 contiguous words. The pristine PROVINCE snapshot is byte-identical to the freeze PROVINCE read in the lane and clone.

| URL | SHA-256 | Located quote |
|---|---|---|
| file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/tools/round-31/c1-sqlite-positive.py | `048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0` | line 130: A table row naming the verb and the entry whose governing heading names Core. |
| file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/.ufo/waves/round-31/claims.json | `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` | line 17: a PROVINCE.md table row names inspect-sqlite-database and the entry |
| file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/PROVINCE.pristine.md | `a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8` | line 73: ## Frontier |
| file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/evidence/round-31/c1/carriers.tsv | `46f180b837b77297cfba11f4cc805d9f849034e411c279bf5744fa6c21c19211` | line 1: id    path    sha256    bytes    source_row    container    container_sha256    member |
| file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/clone/corpus/SOURCES.md | `0ceda6e4b48fa1fd67fbe29ebdb06c391e763e134959dd1bee4b7d936467ca01` | line 1: # SOURCES — where kaidoku learns |
| file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json | `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` | line 4: "version": "6.5.0" |
| file:///home/vgpnk/.omp/agent/RULES.md | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | line 3: Any agent — main session or subagent, any lane, any wave — installs or updates any tool that |
| file:///home/vgpnk/.agents/skills/godspeed/SKILL.md | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | line 12: 1. **Name the axes.** |
| file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md | `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692` | line 19: **The REA MCP server is not registered on this host, by design.** |

The carrier-inventory line-1 quote uses displayed spacing for literal TSV tabs; exact quote bytes are retained in the hashed sources JSON. S096 is the required citation token in the control entry; this seat did not create or edit a source registry row.

## Complete produced-artifact inventory

Every produced seat artifact is listed below with its absolute path and SHA-256. The clone directory is identified by its frozen working-tree revision and retained control commit ids above; the authored clone delta is the hashed Git bundle and the individual control-file hashes above. Unchanged pre-existing repository files are not duplicated into this inventory. No drafts or unlisted throwaway scripts were created.

Manifest itself: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/artifacts.sha256`, SHA-256 `80853bf52f16c3b69d83e0b1540d7ffaf33a1e66b53c8aa4cfc766e3bc49b369`. It contains the following 84 records (the manifest hash is outside its own contents):

```text
a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/PROVINCE.pristine.md
2505dc1eff012f23dbac23f84be190ec704a83c335d70f13f6e6799c158a5e57  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/PROVINCE.variant-a.md
750bfc37f90baeb12962012f271cb1364400ce376838ce7eff43fd8b6f609475  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/PROVINCE.variant-b.md
cc31f73e5595ee45e089bbd3e0003b277095d85a35ff7780fb2c245a6ebb8878  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/control-commits.bundle
bf90685d0a5410193eab27ec0308553af66af06484c15abfb1d98800d1434678  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/counter-baseline.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/counter-baseline.stderr
a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/counter-baseline.stdout
0c1e30ec8dce2b4bc4b40790f15e05a13ece9485b76f174b991528b920b2b975  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/counter-restored.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/counter-restored.stderr
a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/counter-restored.stdout
727785123dee93e37d1d3f646a8798cc710d40698bdb0c46fc237879a1c92e2a  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/counter-variant-a.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/counter-variant-a.stderr
6f99cc6cb4e3bb8868df73941c56405b25c433d6175617ae9340363badfb60af  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/counter-variant-a.stdout
78becb1c78797315df4370ba26030321b3d75ee6a19c69bd0fb1de8e9c0b9ae6  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/counter-variant-b.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/counter-variant-b.stderr
bb706facc0e33eb379370b560600d6ce60cce7c258639210481359811e032637  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/counter-variant-b.stdout
134abea48c40d8dce87911a40282826f02864c0a5d463f8bdf261e421c0d7f48  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/entry.control.md
32c93c795d2dd154a81fc88c1417766e48e4d64c33f839d782d216a6cbf52079  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/envelopes.json
148e8e8d48e61c977bd91c957de5f8b6107ecdfb6a660ad004378f325f7cfda8  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-add-variant-a.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-add-variant-a.stderr
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-add-variant-a.stdout
927333d25556e749c7c3bdcf655d227d4a8e21601032508c54e1356ba045afb5  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-add-variant-b.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-add-variant-b.stderr
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-add-variant-b.stdout
39e5c78c22e31a538753afcff83cbd37d1472c1dc3dc8a1a062a7201aa0194e1  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-bundle-controls.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-bundle-controls.stderr
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-bundle-controls.stdout
b89a52e1594d8cd5c1b9e67f93cd75ec88c20d8d1fefa8abf2dfb34ad24379c6  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-commit-variant-a.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-commit-variant-a.stderr
327aca304159a0caa087bfce41f268f096383710a61c2bff784d784bdc9cac0c  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-commit-variant-a.stdout
aa931b4690f1f01b7059223a5b31fd74c085e3c17c322de7a7774f8b9f42f387  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-commit-variant-b.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-commit-variant-b.stderr
644bf83a33e4f98deeb95920923220f1e50dc269e5935833baaf820781ffe158  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-commit-variant-b.stdout
52c1ee62eccc19011889bc0133de3d331c089176604f54d7403ce5e2964b1292  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-identity-variant-a.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-identity-variant-a.stderr
903bf6d563559996bfaa8c19808caa0faea1a439280fad636a1268f435ec3968  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-identity-variant-a.stdout
8855c62d5b5940db247590f30aac02c927f921d70179420e60089362f80b3c16  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-identity-variant-b.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-identity-variant-b.stderr
03ac66f0cbae3748f8d9ecfee627c3c7c0a962b5cc68ee0a2b2be1dd186ef61f  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-identity-variant-b.stdout
15e241710424d49747625e5b318ed6e5b705d8109dc47daaff7c0172b8aa5ecb  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-restore-freeze.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-restore-freeze.stderr
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/git-restore-freeze.stdout
5f2bfe3a2a8811a2704bb2ccb5506adf8dd330804093aa983afef2b573657f06  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/pristine-state.json
afa9747ad74c0770cd3da20178dac5e7be27dc8e1e06ad14c17554f545201ceb  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/probe.py
712bfe9426bdd5be696e22b52df420bdb7a47b8bf65ff92ecd74ab016004307b  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-chinook-autoinc.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-chinook-autoinc.stderr
bea63657a56b82ad74da59f1777941271e3e494ad62e8458c3f56e18cadf796e  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-chinook-autoinc.stdout
3e9a54cc1b45fd7c36b831fc997806e039895336384f8a170d03aeede9063e0f  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-chinook.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-chinook.stderr
75f77bb98adaba709b971965c3816bcd07285b185dad76883744aee0c283571e  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-chinook.stdout
f753ec3536a04fb134e5011f7f9349f3f84ae83f65f45254fef3974a729746eb  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-curve.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-curve.stderr
9f7482cecb51e1eb9770df389319bd4174f762652168cf6da7245446a86a28ea  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-curve.stdout
d6d00dd2b356a6c549d9c25e18e1090b6579a6a477251dca6385d6013b6cbc75  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-curvepolygon.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-curvepolygon.stderr
575afd17d0a47af432ea7eb4d0bb5a44120401d655bcd4268e1c42ac56d63b2d  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-curvepolygon.stdout
3d900fd06962376854457fc52039d1a4b2990189943892c64d700c008356f1b1  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-line-zm.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-line-zm.stderr
10b34d2c64602eae0d4b51899d5fafc0859a07bf51a0a94da2c4dbd86f634d6c  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-line-zm.stdout
9bb6c832c312245fad0164727933ad8403aded73ac1ea8148171dd75c0de7d87  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-multisurface.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-multisurface.stderr
7f91f70f35d7255829d6fef1d42ff441bfd742d35ad7adf581a174684faee969  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-multisurface.stdout
c6ae75c4898ae1e2ce9e7b639114ea94a6448833fd107706720037cd0cc7f22f  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-test-gpkg-nulls.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-test-gpkg-nulls.stderr
881d9cd58b4c6ea76a2c7b0257aa43d6ccb9f3fdb928d24a1e7378dadf544ed0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-gpkg-test-gpkg-nulls.stdout
493d261a140f6266e49760a0527889fec4db1a9221861b7b2768c7cf029391ec  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-341.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-341.stderr
455306ead20a77cabfa6a1e92ef94a005054f154d5a9d944e55118e1caaee3b3  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-341.stdout
6391cf7664306087e59087e13e0556561f21c416aac6ef8704ca4d5eab2742e6  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-350.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-350.stderr
841bb3e449fa3422dbe26b4e2e5c546413868d0e37608937b228426f5925b2aa  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-350.stdout
615df8532d81742a617a1f3d18738848f15404d14a12fe744ba3925ff0e481c3  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-361.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-361.stderr
ff24d0707a3da45ae425336f8b9ce9a5bbe3eb91a37f4a1b3222247e802c3ec7  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-361.stdout
8d19ccc42737edfe091b58ef6a59e2c7b9807599529b89a0fd5742e45946656d  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-370.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-370.stderr
a896ba9aec86740f7dbbd5a65d03143b25ce82897d7f76a98463e133f92afd9a  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-370.stdout
4b1770b444673e349cd93cf27939efceadadb11ab5a1b9baa7bc0ccb25a085a8  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-371.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-371.stderr
d80542611e71de980e777a2bdd0b16759ba2213a9df7b796f9a316e21bf44e5b  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/rea-proj-371.stdout
37e92d25f5eee7101eb7cae5a62c781ea361485083a35f837a4d7946523adff7  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/restoration.json
67592503413308908a954ca04837540802ffc9b706729dae13c00bb0e1df22f4  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/sources.json
395908348991e96afc1b85ca619d7ef7d82f9c1e499ef9af1c7d44796ae28d0b  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/variant-a-state.json
1e6c7336e5f893945ef54639184b96935fdc8ba30050140c6d591caf5998877b  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1Placement/variant-b-state.json
```

**Final bounded verdict:** holds for both assigned Core-placement controls; formal killed-mutant classification remains inconclusive because the pristine pre-data baseline failed. No frozen target was met.

CONTROL CtlC1Placement: met=no score=12/12
