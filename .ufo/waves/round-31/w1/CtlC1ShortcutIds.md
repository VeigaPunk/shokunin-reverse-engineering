# R31-C1 control: shortcut keyed on carrier ids

CONTROL CtlC1ShortcutIds: met=no score=0/12

## Result and scope

- **Observation:** the committed rotation control did not meet the frozen target. The counter exited **1**, with all 12 rows rejected as `committed envelope differs from the live envelope (full comparison)`; both documentation gates passed.
- **Observation / attack verdict: holds for this control.** Correct carrier filenames, genuine but rotated REA envelopes, every evidence id named in the entry, and the Core row were insufficient to pass.
- **Mutation-test classification: inconclusive, not killed.** The required pristine pre-data baseline already failed (no committed envelopes, no entry, no Core row). Therefore this receipt is not a passing-baseline mutant kill. It is an observed rejection of the specified negative control.
- **Inference:** the effective blocking clause is the full committed-versus-live envelope comparison in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/tools/round-31/c1-sqlite-positive.py:113-114`: `strip_meta(committed) != strip_meta(live)`. No clause let the control through. Every row reached this comparison rather than failing the envelope-presence or post-freeze-addition gate.
- **Unknown:** these control runs do not establish that R31-C1 claim data will meet its target. No claim data or envelope was written into the lane.
- Axes: faithful single-defect control; isolation; discriminating rejection; reproducible receipts; exact-byte restoration.

## Control built

- Sandbox: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone`; branch `ctl`; frozen parent `35ba7c522dba55f9be27eb161d4254eacaa24330`.
- Control commit: `62df38b96af89b37dd66bb1f5265664ff07a9d85`, committed at `2026-10-23T04:12:31Z` (14 changed files).
- Creation command (exit 0; construction recorded at `2026-10-23T04:12:06.391924+00:00`): `timeout 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/build_control.py`.
- The sole behavioral defect is assigning each carrier id the NEXT carrier's complete, unmodified real REA stdout envelope, wrapping the last id to the first. Subject hashes, paths, parameters, schema content and evidence ids were not repaired or fabricated.
- The entry cites `S096` and names all 12 evidence ids. The province addition uses exactly `### Round-31 additions to Core` and a table row naming `inspect-sqlite-database` and the entry.
- Originals are preserved outside the clone under the absolute paths below. Clone worktree bytes were restored after the probe; the control commit, Git index, bundle and immutable control snapshots remain available for reproduction.

Initial sandbox commands (both exit 0):
```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone checkout -q -B ctl 35ba7c522dba55f9be27eb161d4254eacaa24330
```
Pristine byte snapshot observation: `2026-10-23T04:11:00.595372+00:00`. Setup commands did not separately instrument their wall-clock timestamps.

Commit command (exit 0; UTC interval `2026-10-23T04:12:30.391873079Z`–`2026-10-23T04:12:31.590538806Z`):
```sh
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone -c user.name=ctl -c user.email=ctl@local commit -m 'control: rotate real SQLite envelopes by carrier id'
```

### Rotation and generated-file SHA-256

Each file was ABSENT before the mutation, had the following SHA-256 in the committed control, and was ABSENT again after restoration. These envelope hashes equal the corresponding source stdout hashes, including original meta bytes.

| Destination envelope (absolute clone path at control commit) | Real source carrier | Evidence id | SHA-256 |
|---|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/envelopes/proj-341.json` | `proj-350` | `ev_55b3f96bbc31f16782c8bde3ba06acd4646178224bd3e225b9b10e1457ec76aa` | `670484b07746c4d607d3f284967dc6bbe7e692a90bb4c011175660218c8a7cab` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/envelopes/proj-350.json` | `proj-361` | `ev_64b5feb7dadec43ad7eeb4f1972a845e697a36615ee6b505fa8f60e980349350` | `0dd964b8e348adbf5a79d6160f116ddd93c23c7ffaa34514325c289862cbfdb0` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/envelopes/proj-361.json` | `proj-370` | `ev_4bd51490c5d690a628d39e9217a635985d57fea0a7d5d65d2f8c2a5253d526da` | `c79f1120e11cd1030ebbac85b16717bad3fea8d07d08a3265c452c125bc26cce` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/envelopes/proj-370.json` | `proj-371` | `ev_4a9d1724322141214d9678dcb36a5075036b6eee9b75c46996e045aca21a495f` | `7ab3853359ec85bb165bc6619b8429e03ba2b6632233ee8a526044a758fd9122` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/envelopes/proj-371.json` | `chinook` | `ev_fe9589c14b3445f946d1b213dd9915b44e67101a000ec14a92c5fb2fff303d52` | `c1b7b9314b01edce7cb1a76bd77a41603bd8fa47840c899fa05a3ce2b14cee64` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/envelopes/chinook.json` | `chinook-autoinc` | `ev_979cf0eb91af644ab3e6033917ccead5a4684dd71127d070346c085d94b92cce` | `ca19e6f1d822b072bbdc75fb69a753f4f7621a1755d9413e1efc8e460fae3113` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/envelopes/chinook-autoinc.json` | `gpkg-curve` | `ev_4e5aa3c972f950b6e84a5ec33b123e7fdc896064db38809b035b7009eabac35f` | `8e92b5766e02b2a830755b52b37b24b31140d9a43fc61850f4231845f51b11ad` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/envelopes/gpkg-curve.json` | `gpkg-curvepolygon` | `ev_4c282804977b2f03c53715d6d736277713e471ba1744e8eeb5fd1471754d7e3e` | `b10a15805df23e8662c390f916ab360b932d5b24f2ad150968fb459565378b35` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/envelopes/gpkg-curvepolygon.json` | `gpkg-line-zm` | `ev_92b9b645011eb1aec86970a4fdf108da99f4598143ef9b9e739042979af03580` | `28fe113882a0f5e100cd0ce50d1e36924871c99f14d1cd5055f3e35c77665362` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/envelopes/gpkg-line-zm.json` | `gpkg-multisurface` | `ev_c836ccb09a6ac28a7e719a1e4682c088068c8ed73e1ad14392affe159b1f5af0` | `021e693dd34fe09352241b6b01a4c305b0a6b1113f4ab49c932800961abe4d22` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/envelopes/gpkg-multisurface.json` | `gpkg-test-gpkg-nulls` | `ev_699901859c0d92f8c46a05dfbb9ce51d0e4e7d53aea78bf16c55d2e1450ec99e` | `0591d918d6855b3bda732bbf20fd65d3f24fa64437f4ab56ca80b1071497a843` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/envelopes/gpkg-test-gpkg-nulls.json` | `proj-341` | `ev_52a9b4951d991aeead1fab8ed0374b3d22b5632e7927442f289df8f2ad4d1835` | `00b4335dd72ab323bf726214f10153512eecb4d84c3accdd1089d30ddd20adfc` |

| Other changed file | Before SHA-256 | Control SHA-256 | Restored state |
|---|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/PROVINCE.md` | `a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8` | `63bc6bb7a4182c1aa16db4c355f511612636157f1b7433f665e4e023b5189ff2` | `a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/knowledge/2026-10-23-r31-sqlite-positive.md` | ABSENT | `c6155039b3c7c778804913844590c3d3375cecb81015c10cbd7bd68f0d19c196` | ABSENT |

## Real REA producers

**Observation:** all 12 explicitly assigned CLI calls exited 0 and emitted `ok:true` JSON for the requested carrier. Stdout and stderr are retained independently. No other REA operation or version was invoked. Every producer used the scratch TMPDIR.

### Producer `proj-341`

UTC: `2026-10-23T04:11:29.626533+00:00`–`2026-10-23T04:11:30.720475+00:00`; exit `0`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/proj-341.db --schema-scope database --format json --full-output
```
Stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-341.stdout`; stderr: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-341.stderr` (empty).

### Producer `proj-350`

UTC: `2026-10-23T04:11:30.721428+00:00`–`2026-10-23T04:11:31.651325+00:00`; exit `0`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/proj-350.db --schema-scope database --format json --full-output
```
Stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-350.stdout`; stderr: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-350.stderr` (empty).

### Producer `proj-361`

UTC: `2026-10-23T04:11:31.652189+00:00`–`2026-10-23T04:11:32.584753+00:00`; exit `0`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/proj-361.db --schema-scope database --format json --full-output
```
Stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-361.stdout`; stderr: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-361.stderr` (empty).

### Producer `proj-370`

UTC: `2026-10-23T04:11:32.586736+00:00`–`2026-10-23T04:11:33.725134+00:00`; exit `0`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/proj-370.db --schema-scope database --format json --full-output
```
Stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-370.stdout`; stderr: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-370.stderr` (empty).

### Producer `proj-371`

UTC: `2026-10-23T04:11:33.726504+00:00`–`2026-10-23T04:11:34.655095+00:00`; exit `0`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/proj-371.db --schema-scope database --format json --full-output
```
Stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-371.stdout`; stderr: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-371.stderr` (empty).

### Producer `chinook`

UTC: `2026-10-23T04:11:34.656550+00:00`–`2026-10-23T04:11:35.559211+00:00`; exit `0`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite --schema-scope database --format json --full-output
```
Stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-chinook.stdout`; stderr: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-chinook.stderr` (empty).

### Producer `chinook-autoinc`

UTC: `2026-10-23T04:11:35.559972+00:00`–`2026-10-23T04:11:36.454118+00:00`; exit `0`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/chinook-autoinc.sqlite --schema-scope database --format json --full-output
```
Stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-chinook-autoinc.stdout`; stderr: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-chinook-autoinc.stderr` (empty).

### Producer `gpkg-curve`

UTC: `2026-10-23T04:11:36.454533+00:00`–`2026-10-23T04:11:37.316285+00:00`; exit `0`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-curve.gpkg --schema-scope database --format json --full-output
```
Stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-curve.stdout`; stderr: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-curve.stderr` (empty).

### Producer `gpkg-curvepolygon`

UTC: `2026-10-23T04:11:37.316623+00:00`–`2026-10-23T04:11:38.224517+00:00`; exit `0`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-curvepolygon.gpkg --schema-scope database --format json --full-output
```
Stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-curvepolygon.stdout`; stderr: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-curvepolygon.stderr` (empty).

### Producer `gpkg-line-zm`

UTC: `2026-10-23T04:11:38.224917+00:00`–`2026-10-23T04:11:39.275064+00:00`; exit `0`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-line-zm.gpkg --schema-scope database --format json --full-output
```
Stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-line-zm.stdout`; stderr: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-line-zm.stderr` (empty).

### Producer `gpkg-multisurface`

UTC: `2026-10-23T04:11:39.275474+00:00`–`2026-10-23T04:11:40.234828+00:00`; exit `0`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-multisurface.gpkg --schema-scope database --format json --full-output
```
Stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-multisurface.stdout`; stderr: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-multisurface.stderr` (empty).

### Producer `gpkg-test-gpkg-nulls`

UTC: `2026-10-23T04:11:40.235174+00:00`–`2026-10-23T04:11:41.265237+00:00`; exit `0`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-test-gpkg-nulls.gpkg --schema-scope database --format json --full-output
```
Stdout: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-test-gpkg-nulls.stdout`; stderr: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-test-gpkg-nulls.stderr` (empty).

## Bounded counter receipts

All commands below ran with cwd `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds`. The counter and oracle bytes were unchanged throughout. The capture runner records the actual child counter exit code; its own successful capture exit is not substituted for that code.

### Pristine comparison, before control commit

UTC: `2026-10-23T04:11:29.623402+00:00`–`2026-10-23T04:11:41.321612+00:00`. Counter exit: **1**. Supervisor timeout: `false`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```
Full counter stdout:
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
Full counter stderr: empty (0 bytes).

### Committed rotated-envelope control

UTC: `2026-10-23T04:12:45.733908+00:00`–`2026-10-23T04:13:06.634477+00:00`. Counter exit: **1**. Supervisor timeout: `false`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone --rev HEAD
```
Full counter stdout:
```text
proj-341	P1-fail	committed envelope differs from the live envelope (full comparison)
proj-350	P1-fail	committed envelope differs from the live envelope (full comparison)
proj-361	P1-fail	committed envelope differs from the live envelope (full comparison)
proj-370	P1-fail	committed envelope differs from the live envelope (full comparison)
proj-371	P1-fail	committed envelope differs from the live envelope (full comparison)
chinook	P1-fail	committed envelope differs from the live envelope (full comparison)
chinook-autoinc	P1-fail	committed envelope differs from the live envelope (full comparison)
gpkg-curve	P1-fail	committed envelope differs from the live envelope (full comparison)
gpkg-curvepolygon	P1-fail	committed envelope differs from the live envelope (full comparison)
gpkg-line-zm	P1-fail	committed envelope differs from the live envelope (full comparison)
gpkg-multisurface	P1-fail	committed envelope differs from the live envelope (full comparison)
gpkg-test-gpkg-nulls	P1-fail	committed envelope differs from the live envelope (full comparison)
carriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)
```
Full counter stderr: empty (0 bytes).

### Restored-byte comparison

UTC: `2026-10-23T04:14:07.671626+00:00`–`2026-10-23T04:14:19.931131+00:00`. Counter exit: **1**. Supervisor timeout: `false`.
```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/tmp timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```
Full counter stdout:
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
Full counter stderr: empty (0 bytes).

## Restoration and unchanged instruments

- **Observation:** restoration ran during `2026-10-23T04:13:44.149181+00:00`–`2026-10-23T04:14:07.655073+00:00` with successful tool results and exit 0 for empty-directory removal.
- Restoration used `functions.edit` to remove only the appended province lines and the 13 newly created files, then `timeout 5 rmdir /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/envelopes`.
- **Observation:** every mutated worktree path returned to its original byte hash or original absence. The restored counter explicitly selected the frozen revision; its full stdout is byte-identical to the pristine comparison and it again exited 1.
- The clone branch and index intentionally retain the control commit. `--rev HEAD` still selects that preserved committed control despite restored worktree documentation/envelope paths. No Git reset, stash, checkout-after-probe, or lane Git/JJ write was used.
- No `PIN ... absent or altered` diagnostic occurred in any counter receipt. Immutable carrier, mutant and download paths were never modified, moved or reflagged.

| Unchanged file (absolute path) | Before and restored SHA-256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/tools/round-31/c1-sqlite-positive.py` | `048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/tools/round-31/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/.ufo/waves/round-31/claims.json` | `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/carriers.tsv` | `46f180b837b77297cfba11f4cc805d9f849034e411c279bf5744fa6c21c19211` |

## Artifact inventory

All retained generated files outside clone internals are listed below with SHA-256. The complete per-file digest inventory for the restored clone (21,506 non-Git files) is `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone.restored.sha256`; this manifest, rather than a nonexistent raw directory byte stream, defines the clone worktree directory digest. Git history for the one control commit is preserved in the bundle (requires the frozen parent). No transient Node compile cache is retained.

| Absolute artifact | SHA-256 | Bytes |
|---|---|---:|
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/build_control.py` | `fdfc4611e9975eb45c483c408bd59c9e4643d23c1ca6f770939abf3384521035` | 3189 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone.restored.sha256` | `76079aed6eaa6388806912c6fe1efa3822dd912bb8d72dd3fdd0e80639d977bb` | 4199860 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control/PROVINCE.md` | `63bc6bb7a4182c1aa16db4c355f511612636157f1b7433f665e4e023b5189ff2` | 39402 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control/corpus/evidence/round-31/c1/envelopes/chinook-autoinc.json` | `8e92b5766e02b2a830755b52b37b24b31140d9a43fc61850f4231845f51b11ad` | 22934 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control/corpus/evidence/round-31/c1/envelopes/chinook.json` | `ca19e6f1d822b072bbdc75fb69a753f4f7621a1755d9413e1efc8e460fae3113` | 20156 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control/corpus/evidence/round-31/c1/envelopes/gpkg-curve.json` | `b10a15805df23e8662c390f916ab360b932d5b24f2ad150968fb459565378b35` | 23338 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control/corpus/evidence/round-31/c1/envelopes/gpkg-curvepolygon.json` | `28fe113882a0f5e100cd0ce50d1e36924871c99f14d1cd5055f3e35c77665362` | 23044 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control/corpus/evidence/round-31/c1/envelopes/gpkg-line-zm.json` | `021e693dd34fe09352241b6b01a4c305b0a6b1113f4ab49c932800961abe4d22` | 23338 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control/corpus/evidence/round-31/c1/envelopes/gpkg-multisurface.json` | `0591d918d6855b3bda732bbf20fd65d3f24fa64437f4ab56ca80b1071497a843` | 24942 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control/corpus/evidence/round-31/c1/envelopes/gpkg-test-gpkg-nulls.json` | `00b4335dd72ab323bf726214f10153512eecb4d84c3accdd1089d30ddd20adfc` | 270864 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control/corpus/evidence/round-31/c1/envelopes/proj-341.json` | `670484b07746c4d607d3f284967dc6bbe7e692a90bb4c011175660218c8a7cab` | 271529 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control/corpus/evidence/round-31/c1/envelopes/proj-350.json` | `0dd964b8e348adbf5a79d6160f116ddd93c23c7ffaa34514325c289862cbfdb0` | 274178 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control/corpus/evidence/round-31/c1/envelopes/proj-361.json` | `c79f1120e11cd1030ebbac85b16717bad3fea8d07d08a3265c452c125bc26cce` | 279552 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control/corpus/evidence/round-31/c1/envelopes/proj-370.json` | `7ab3853359ec85bb165bc6619b8429e03ba2b6632233ee8a526044a758fd9122` | 301670 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control/corpus/evidence/round-31/c1/envelopes/proj-371.json` | `c1b7b9314b01edce7cb1a76bd77a41603bd8fa47840c899fa05a3ce2b14cee64` | 20008 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control/corpus/knowledge/2026-10-23-r31-sqlite-positive.md` | `c6155039b3c7c778804913844590c3d3375cecb81015c10cbd7bd68f0d19c196` | 1982 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control-identity.json` | `13b5714e124a25b55c744ac19da285e39eb70531eda36642789bf56b7d6e36ed` | 561 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/control.bundle` | `ce46722524b6bad2495165b8ab94d3f2950274c4b50f4967d65036c5945e0888` | 71817 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/counter-baseline.json` | `ea13605fb6c7c55fdebf216ef8d70686a3ccdcfb6b5cf4f6060d5f1eb214b389` | 916 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/counter-baseline.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/counter-baseline.stdout` | `a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e` | 680 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/counter-mutated.json` | `2eb1f3bea1d6f54e380ed46c02ee33e8344158117fd833f52856f58019d1350a` | 843 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/counter-mutated.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/counter-mutated.stdout` | `2dcb1e93c38ccb2d365f0841137330529e7d6cdcd9fc2f5a68d64f88d3b629df` | 1126 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/counter-restored.json` | `8bab0834615042c9cea239f70d0f3c54f648f16ca19a244f7e4caac6ee13394b` | 916 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/counter-restored.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/counter-restored.stdout` | `a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e` | 680 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-chinook-autoinc.json` | `994419afd9e4cf194491924f0a0bbbf77500ac1d0b9131f2b8ceab16e45e00ba` | 795 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-chinook-autoinc.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-chinook-autoinc.stdout` | `ca19e6f1d822b072bbdc75fb69a753f4f7621a1755d9413e1efc8e460fae3113` | 20156 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-chinook.json` | `8d98950bd9873c9640e370680f33df25f7466779a64305c46c323e9df82a181e` | 771 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-chinook.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-chinook.stdout` | `c1b7b9314b01edce7cb1a76bd77a41603bd8fa47840c899fa05a3ce2b14cee64` | 20008 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-curve.json` | `911646f269b736d714fe515d00396ff62e1379d29541166ae187b1a2ce1af4de` | 776 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-curve.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-curve.stdout` | `8e92b5766e02b2a830755b52b37b24b31140d9a43fc61850f4231845f51b11ad` | 22934 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-curvepolygon.json` | `7baed23d3b24df4a0a101d637089ac83383b9a39c8f65f9bfe860d6c17752f8c` | 797 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-curvepolygon.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-curvepolygon.stdout` | `b10a15805df23e8662c390f916ab360b932d5b24f2ad150968fb459565378b35` | 23338 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-line-zm.json` | `f75c5d7456c45867ca10e3a3509badc78aa86bda35692ac09273cbc6cd06debd` | 782 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-line-zm.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-line-zm.stdout` | `28fe113882a0f5e100cd0ce50d1e36924871c99f14d1cd5055f3e35c77665362` | 23044 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-multisurface.json` | `b9be62d1f361417bd636e2d0eb7b427ecc8e7e7ba67050887b668580595112e9` | 797 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-multisurface.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-multisurface.stdout` | `021e693dd34fe09352241b6b01a4c305b0a6b1113f4ab49c932800961abe4d22` | 23338 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-test-gpkg-nulls.json` | `e3c8e8ea572d63e09e478875c279ce78885ca335bc7b1bde628032d6c83fb3fe` | 806 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-test-gpkg-nulls.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-test-gpkg-nulls.stdout` | `0591d918d6855b3bda732bbf20fd65d3f24fa64437f4ab56ca80b1071497a843` | 24942 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-341.json` | `287013749f82c6d7c0a46dc12c6331b2ee53ae7581bc8cb1b000310814174f71` | 766 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-341.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-341.stdout` | `00b4335dd72ab323bf726214f10153512eecb4d84c3accdd1089d30ddd20adfc` | 270864 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-350.json` | `d52a7946bcf75559648c7daec5dbb893f8a194e0c545b502ea980fc5f1808bc7` | 766 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-350.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-350.stdout` | `670484b07746c4d607d3f284967dc6bbe7e692a90bb4c011175660218c8a7cab` | 271529 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-361.json` | `9980d1c6629e284fe66d4faa12174d5f29e720185ca78ea13c218149cbda7d39` | 766 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-361.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-361.stdout` | `0dd964b8e348adbf5a79d6160f116ddd93c23c7ffaa34514325c289862cbfdb0` | 274178 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-370.json` | `7dc9305d2441b802a9172b8d44311ac686306ffc80d3adcfb753e0d7671e21f1` | 766 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-370.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-370.stdout` | `c79f1120e11cd1030ebbac85b16717bad3fea8d07d08a3265c452c125bc26cce` | 279552 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-371.json` | `e29ba6e4e734a07a845c1855cf3585fb4ab348aaf86063e98fe812c0441a75fd` | 766 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-371.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-371.stdout` | `7ab3853359ec85bb165bc6619b8429e03ba2b6632233ee8a526044a758fd9122` | 301670 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/rotation.json` | `829ffe25f84ce3c62672dd43ae36495dbaf1fc9013942751044b42d70fecfcbf` | 6618 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/run_probe.py` | `08f26c292774ae94ab26f6b3f981ef0f50018ad9b398a3b5d09312eaec4a9de0` | 3534 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/snapshots/PROVINCE.pristine.md` | `a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8` | 38929 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/snapshots/mutated.json` | `d12b588178bdb676073499d47de4a1abc3ecf28ba507de0d3fdaeffefd66a45e` | 1844 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/snapshots/pristine.json` | `3c7496e826bd3c5e2ea69aaef0634a214955a5274a752c21ed4b3134507d74fa` | 717 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/snapshots/restored.json` | `1c8f7c8fb8ca807e6e6a836647fce6193a71222780652bd6cf0c6e3b78bbb61e` | 3611 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/sources.json` | `e12a7634264dfcbde7f83c6762017d88af74bda73a79ce8dc6d02a23ce5e67b3` | 13666 |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/artifacts.sha256` | `6c6ce10dc52e9de418cf2a26543b42860c155805efd14883e1dadcb36726446f` | 10948 |

## Primary-source access records

Access date for every record: **2026-10-23**. Only ordinary local file reads and the explicitly assigned CLI calls were used; no browser, external source fetch, challenge bypass or additional runtime was invoked. Each quote is at most 25 contiguous served words; the complete producer commands and timestamps are also retained in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/sources.json`.

| Opened source URL | SHA-256 of bytes read | Located quote |
|---|---|---|
| `file:///home/vgpnk/.agents/skills/godspeed/SKILL.md` | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | line 10: You are a Godspeed-enabled subagent. |
| `file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md` | `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692` | line 313: Every conclusion must distinguish observations, inferences, and unknowns. |
| `file:///home/vgpnk/.omp/agent/RULES.md` | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | line 14: - Record every install or update — tool, version, channel, reason — in your report or handoff. |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/tools/round-31/c1-sqlite-positive.py` | `048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0` | line 114:         return False, "committed envelope differs from the live envelope (full comparison)" |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/.ufo/waves/round-31/claims.json` | `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` | line 44:   "shortcut keyed on ids/labels (another carrier's or request's envelope under the id)" |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-31/c1/carriers.tsv` | `46f180b837b77297cfba11f4cc805d9f849034e411c279bf5744fa6c21c19211` | line 1: id path sha256 bytes source_row container container_sha256 member |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/snapshots/PROVINCE.pristine.md` | `a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8` | line 338: Before round 30 the lane held only `auditable_metadata: null` runs of `inspect-rust-binary` (no section). |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/SOURCES.md` | `0ceda6e4b48fa1fd67fbe29ebdb06c391e763e134959dd1bee4b7d936467ca01` | line 1: # SOURCES — where kaidoku learns |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/clone/corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md` | `bf4ab45d7a921c276fb432f7c5c587f8623fa94bd2866aec7408cee5410b2e63` | line 1: # inspect_sqlite_database — offline SQLite schema inventory |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c1-sqlite-positive.py` | `048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0` | line 114:         return False, "committed envelope differs from the live envelope (full comparison)" |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/claims.json` | `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` | line 44:   "shortcut keyed on ids/labels (another carrier's or request's envelope under the id)" |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c1/carriers.tsv` | `46f180b837b77297cfba11f4cc805d9f849034e411c279bf5744fa6c21c19211` | line 1: id path sha256 bytes source_row container container_sha256 member |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md` | `a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8` | line 338: Before round 30 the lane held only `auditable_metadata: null` runs of `inspect-rust-binary` (no section). |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-chinook-autoinc.stdout` | `ca19e6f1d822b072bbdc75fb69a753f4f7621a1755d9413e1efc8e460fae3113` | line 1: ev_979cf0eb91af644ab3e6033917ccead5a4684dd71127d070346c085d94b92cce |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-chinook.stdout` | `c1b7b9314b01edce7cb1a76bd77a41603bd8fa47840c899fa05a3ce2b14cee64` | line 1: ev_fe9589c14b3445f946d1b213dd9915b44e67101a000ec14a92c5fb2fff303d52 |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-curve.stdout` | `8e92b5766e02b2a830755b52b37b24b31140d9a43fc61850f4231845f51b11ad` | line 1: ev_4e5aa3c972f950b6e84a5ec33b123e7fdc896064db38809b035b7009eabac35f |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-curvepolygon.stdout` | `b10a15805df23e8662c390f916ab360b932d5b24f2ad150968fb459565378b35` | line 1: ev_4c282804977b2f03c53715d6d736277713e471ba1744e8eeb5fd1471754d7e3e |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-line-zm.stdout` | `28fe113882a0f5e100cd0ce50d1e36924871c99f14d1cd5055f3e35c77665362` | line 1: ev_92b9b645011eb1aec86970a4fdf108da99f4598143ef9b9e739042979af03580 |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-multisurface.stdout` | `021e693dd34fe09352241b6b01a4c305b0a6b1113f4ab49c932800961abe4d22` | line 1: ev_c836ccb09a6ac28a7e719a1e4682c088068c8ed73e1ad14392affe159b1f5af0 |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-gpkg-test-gpkg-nulls.stdout` | `0591d918d6855b3bda732bbf20fd65d3f24fa64437f4ab56ca80b1071497a843` | line 1: ev_699901859c0d92f8c46a05dfbb9ce51d0e4e7d53aea78bf16c55d2e1450ec99e |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-341.stdout` | `00b4335dd72ab323bf726214f10153512eecb4d84c3accdd1089d30ddd20adfc` | line 1: ev_52a9b4951d991aeead1fab8ed0374b3d22b5632e7927442f289df8f2ad4d1835 |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-350.stdout` | `670484b07746c4d607d3f284967dc6bbe7e692a90bb4c011175660218c8a7cab` | line 1: ev_55b3f96bbc31f16782c8bde3ba06acd4646178224bd3e225b9b10e1457ec76aa |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-361.stdout` | `0dd964b8e348adbf5a79d6160f116ddd93c23c7ffaa34514325c289862cbfdb0` | line 1: ev_64b5feb7dadec43ad7eeb4f1972a845e697a36615ee6b505fa8f60e980349350 |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-370.stdout` | `c79f1120e11cd1030ebbac85b16717bad3fea8d07d08a3265c452c125bc26cce` | line 1: ev_4bd51490c5d690a628d39e9217a635985d57fea0a7d5d65d2f8c2a5253d526da |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1ShortcutIds/raw/rea-proj-371.stdout` | `7ab3853359ec85bb165bc6619b8429e03ba2b6632233ee8a526044a758fd9122` | line 1: ev_4a9d1724322141214d9678dcb36a5075036b6eee9b75c46996e045aca21a495f |

## Tooling and process closure

- **Observation:** no tool was installed or updated. Existing cached `rea-agents@6.5.0` was reused through npx. Its package JSON SHA-256 was `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` (producing command: `timeout 10 sha256sum /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json`, exit 0; recorded with this report). No pacman transaction occurred.
- All producers were bounded by 300 seconds; each detector by 900 seconds. Every capture returned and its owned child process group received cleanup in a `finally` block. No service, watcher or background job started by this seat remains active.
- The lane received only this scoped report. No control envelopes, entry, province edit, Git index mutation or commit were integrated there.
- Report assembled from retained receipts at `2026-10-23T04:16:50.212481+00:00`. No extra tests, builds, lints, runtime probes or claim-data collection were run.
