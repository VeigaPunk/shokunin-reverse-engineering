# R31-C1 no-reader pre-data control — CtlC1NoReader

CONTROL CtlC1NoReader: met=no score=0/12

**Observation — attack verdict: holds against this assigned control.** The control did not meet the frozen target and exited 1. Every carrier was rejected with `committed envelope differs from the live envelope (full comparison)`; both documentation gates passed.

**Mutation-testing verdict: inconclusive, not killed.** The pristine pre-data revision also exits 1 because no committed envelopes or documentation additions exist. That baseline failure is not a killed mutant. The separate negative-control observation is that the fabricated records do not obtain a passing target.

Axes: control fidelity; frozen-detector discrimination; containment; exact restoration.

## Control built

- Isolated sandbox: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone`; branch `ctl`, initially pinned at `35ba7c522dba55f9be27eb161d4254eacaa24330`.
- Fabrication command: `timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/build-control.py`; exit 0; recorded UTC `2026-10-23T04:12:06+00:00`. The script imports the clone's frozen oracle and calls `expected_report(path)` once per carrier. It invokes no REA process.
- Each fabricated envelope has exactly the requested outer shape: `ok=true`, `data.evidence_id`, `data.operation=inspect_sqlite_database`, `data.subject.digest.sha256`, and `data.normalized_result`. Reports add `engine.version="3.53.4"` and `limitations=[]`. Evidence IDs are `ev_` followed by SHA-256 of UTF-8 report JSON serialized with `ensure_ascii=False`, `sort_keys=True`, and compact separators, after those additions.
- New entry: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/knowledge/2026-10-23-r31-sqlite-positive.md`; cites S096 and names all 12 fabricated IDs. The entry explicitly identifies the records as fabricated.
- Modified `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/PROVINCE.md`: appended `### Round-31 additions to Core` and a table row naming `inspect-sqlite-database` and the required entry path.
- Control commit: `15ca6a07a4d75d7de50b75cbabd0ba9deb0ab06b`; tree `536d42831cb36d25e0451015e92d036f7dacaabd`. Git reported `14 files changed, 27377 insertions(+)`. Commit and all Git writes were confined to the sandbox.
- Exact control payload remains in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/control.patch` and the control commit, even though working bytes were subsequently restored.

### Affected files and before / control / restored SHA-256

`absent` means that no file existed, not the hash of an empty file. The 13 new files are absent again after restoration.

| Absolute file path | Pristine SHA-256 | Control SHA-256 | Restored SHA-256 |
|---|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/PROVINCE.md` | `a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8` | `a0142c1a152f6ad5c520dd9bca0cc5a4b78c22df3995742f01cfbdefc399b179` | `a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-31/c1/envelopes/chinook-autoinc.json` | `absent` | `2ad3e51fb7d76cb29cf8918ed8860b564a09747efa2c6b01b9ea6252ab8231cd` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-31/c1/envelopes/chinook.json` | `absent` | `2e4045a227106974ed695aef4beb05f77c1ca57fda9e66935d588170a282adeb` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-31/c1/envelopes/gpkg-curve.json` | `absent` | `1893f0d185f5377af5a596b3e451cf245ed7b472d4ec341d600d530f096a8cfb` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-31/c1/envelopes/gpkg-curvepolygon.json` | `absent` | `60b4717fbb4359e6fb58348d86418eefc59038fd89771aea362c9748b45adbf5` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-31/c1/envelopes/gpkg-line-zm.json` | `absent` | `14a315ec39dffd4cd16b6bc3aabfb4ecb30692c52ad1f918205dd6f8b6d54bb0` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-31/c1/envelopes/gpkg-multisurface.json` | `absent` | `c7d69463615cf14f53433adcea748ada19ceba8149817724889f2ea1d3f21432` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-31/c1/envelopes/gpkg-test-gpkg-nulls.json` | `absent` | `5c907c9a071cfd5e1ec15b09923e39c2a4469d003c41856dc7399a8bdab8e87d` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-31/c1/envelopes/proj-341.json` | `absent` | `0d31503715a3dad1644b376e53927868e5ffa903d7c27386917f97ff2e3fbf58` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-31/c1/envelopes/proj-350.json` | `absent` | `e7c4a87fdd7e4658f842ae0d806edca1ce3d32b0622537d40812d0342d69f4ba` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-31/c1/envelopes/proj-361.json` | `absent` | `9f36836e7760d505482b8b44b2f99dbc334906194fc40aa0d740b50f6e77a39e` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-31/c1/envelopes/proj-370.json` | `absent` | `ffb9967e4fea20700727156ffeebd8d9489f7c70d9d6e95dc6c1dfdc686b7c04` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-31/c1/envelopes/proj-371.json` | `absent` | `c8681a0d1079a7107cf0d6ed5f2d99082459b07f325910df93d10590d7269274` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/knowledge/2026-10-23-r31-sqlite-positive.md` | `absent` | `f0f82e75445a57cad941e28d533d3474ff6d57290f78a7e2741d5e8c0973defd` | `absent` |

### Fabricated identities

| Carrier | Fabricated evidence ID |
|---|---|
| proj-341 | `ev_aed57cb7c5021923b0e52c9ed49f98245888516537663c8c906fa423ff6096cc` |
| proj-350 | `ev_f5a64bd63fd900356ce25c99b02fb91e33dbfbb69f4c92d048c1f9187145f5c6` |
| proj-361 | `ev_8675e69260a5caf9dd4c61484f506e11e1bbe56df8ebce5f5a16a39c574d885f` |
| proj-370 | `ev_c69e748b7440807eb31581798655d38f201f12b13f29dc5c1f18db19e7d5ca61` |
| proj-371 | `ev_8f39db839d0ceb9078675771e35abf1198d4ec1e1c3e0972ea1c792ae2556649` |
| chinook | `ev_fc6872620c8ffcdeec68045390b56e3868907031cbeba8f1b3275632fde822c6` |
| chinook-autoinc | `ev_c600f5da29110a154f90588d1f13a49329ff253ad2947347dc7855cd83371939` |
| gpkg-curve | `ev_54df6382ace6f65697e12179780985eacfa8d3c1721c446300fe6b1ef7426ed3` |
| gpkg-curvepolygon | `ev_c0b58feee0b53308b0cf9cb8740fc8d1bbff9ccd97e596f979b6aabe36dcca01` |
| gpkg-line-zm | `ev_28b46ba17cd8b56d0dc248c8c55b77d6bdbe80d86d18ad8e3d13c9d3825c5817` |
| gpkg-multisurface | `ev_f9a075276d98751acfdd0cfbbc98560423e45e5a3f5a94a34831fff551727ef9` |
| gpkg-test-gpkg-nulls | `ev_7d9d130b4039f646354dafc10f706c8740585b3450ae68be3ea4eaa2431a6a7b` |

## Bounded behavioral detector — actual outputs

All three counter executions used working directory `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader`, `TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/tmp`, and an environment with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset. The exact executed counter argv is shown below. No `--write-evidence` mode, monkeypatch, reader substitution, counter edit, direct carrier REA call, or alternate REA version was used. REA ran live only inside the unchanged frozen counter.

### Pristine, before the control commit

Command (cwd as stated above):

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Capture wrapper: `timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/run-counter.py pristine 35ba7c522dba55f9be27eb161d4254eacaa24330`.

- UTC start: `2026-10-23T04:11:42+00:00`
- UTC end: `2026-10-23T04:11:54+00:00`
- Measured commit: `35ba7c522dba55f9be27eb161d4254eacaa24330`
- Exit code: `1`
- Frozen target MET: **no**
- Full counter stdout (verbatim; the wrapper's metadata line is not counter stdout):

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

Counter stderr: empty, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Stdout SHA-256: `a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e`.

### Committed no-reader control

Command (cwd as stated above):

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone --rev HEAD
```

Capture wrapper: `timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/run-counter.py mutated HEAD`.

- UTC start: `2026-10-23T04:12:26+00:00`
- UTC end: `2026-10-23T04:12:38+00:00`
- Measured commit: `15ca6a07a4d75d7de50b75cbabd0ba9deb0ab06b`
- Exit code: `1`
- Frozen target MET: **no**
- Full counter stdout (verbatim; the wrapper's metadata line is not counter stdout):

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

Counter stderr: empty, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Stdout SHA-256: `2dcb1e93c38ccb2d365f0841137330529e7d6cdcd9fc2f5a68d64f88d3b629df`.

### Restored exact bytes

Command (cwd as stated above):

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone --rev HEAD
```

Capture wrapper: `timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/run-counter.py restored HEAD`.

- UTC start: `2026-10-23T04:14:07+00:00`
- UTC end: `2026-10-23T04:14:19+00:00`
- Measured commit: `aa1bcf4796cffbfd5a6813f8531d53ad9c0e5204`
- Exit code: `1`
- Frozen target MET: **no**
- Full counter stdout (verbatim; the wrapper's metadata line is not counter stdout):

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

Counter stderr: empty, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Stdout SHA-256: `a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e`.

## Detector clause and interpretation

**Observation:** at the control revision all 12 output rows identify the same rejecting clause, while the final line reports `entry_ok=1 (ok) province_ok=1 (ok)`. The control therefore did not fail merely because its entry, Core placement, or committed files were absent.

**Observation from frozen source:** `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/tools/round-31/c1-sqlite-positive.py:113-114` rejects whenever `strip_meta(committed) != strip_meta(live)`, returning the exact printed full-comparison failure. Lines 180-183 invoke this check only after the live report judge passed.

**Inference from the unchanged control flow and these outputs:** every live reader run passed the exit/operation/subject/oracle-report gate, and rejection occurred at the committed-versus-live full-envelope equality check. No clause let the no-reader control through.

**Unknown:** the individual live-envelope field differences were not retained by this read-only counter mode; no claim is made about a particular evidence-ID or other field being the sole mismatch. This is one assigned synthetic control, not proof against every possible fabrication.

## Restoration and containment evidence

Restoration command, executed with the three Git environment variables unset:

```sh
timeout 60 git -C /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone -c user.name=ctl -c user.email=ctl@local revert --no-edit 15ca6a07a4d75d7de50b75cbabd0ba9deb0ab06b
```

Observation: exit 0, UTC `2026-10-23T04:14:06+00:00` through `2026-10-23T04:14:06+00:00`. Output excerpt: `14 files changed, 27377 deletions(-)`. Full restoration stdout is `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/restoration.stdout`. The revert restores only this seat's control commit and preserves its history.

- Pristine Git tree: `0063d2b6c8ae3fc50047e1a8c3ff5772a72c0c9c`.
- Restored Git tree: `0063d2b6c8ae3fc50047e1a8c3ff5772a72c0c9c` — identical.
- Final branch `ctl` commit: `aa1bcf4796cffbfd5a6813f8531d53ad9c0e5204`.
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/PROVINCE.md` returns to SHA-256 `a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8`; the entry and all 12 envelopes return to absence.
- All before/after affected-file hash maps are unchanged across each individual detector execution. Frozen counter, oracle, claims, carrier list, and installed package JSON hashes are identical across all three runs.
- Restored counter stdout is byte-identical to pristine stdout: SHA-256 `a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e`; both exit 1.
- Clone manifests inventory 21523 control-state tracked paths and 21510 restored tracked paths. Each regular file is hashed by its exact bytes; symlinks are represented by SHA-256 of `b"symlink:" + os.fsencode(os.readlink(path))` without following the target. `.git` administrative files are not included in these content manifests. Their SHA-256 values are listed below.
- Every launched command was bounded; the counter wrapper also kills any remaining child process group after capture. No long-running process or service was started. The owned Node compile cache under the seat's tmp directory was removed after the final counter run.
- Lane writes: only this report at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/w1/CtlC1NoReader.md`. No lane Git/index/jj mutation, immutable-carrier change, sibling write, or peer message occurred.

## Preparation caveats and tooling

Two helper preparation errors are retained in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/preparation-errors.txt`: an accidental Python footer syntax error before the first actual detector run, and an inventory attempt that followed an unrelated dangling symlink before restoration. Both helpers were corrected; neither error is counted as a detector result or mutant kill. Their UTC timestamps were not captured (**unknown**). The recorded pristine, control, and restored counter runs above are the three actual detector executions.

No tool was installed or updated. The counters used the already-present `rea-agents@6.5.0` npm pin through `npx`; no pacman transaction, runtime replacement, build, lint, formatter, unrelated test, integration, or shipping action was performed.

## Opened local sources

All accesses were ordinary local reads on **2026-10-23**; no remote source was opened. Hashes cover the full file bytes read for digest capture. Each located quote is at most 25 contiguous words. Self-authored files and raw receipts are inventoried separately below.

| Local source URL | Access date | SHA-256 | Located quote |
|---|---|---|---|
| `file:///home/vgpnk/.agents/skills/godspeed/SKILL.md` | 2026-10-23 | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | L2: `name: godspeed` |
| `file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md` | 2026-10-23 | `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692` | L2: `name: reverse-engineer-anything` |
| `file:///home/vgpnk/.omp/agent/RULES.md` | 2026-10-23 | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | L3: `Any agent — main session or subagent, any lane, any wave — installs or updates any tool that` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c1-sqlite-positive.py` | 2026-10-23 | `048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0` | L113: `if strip_meta(committed) != strip_meta(live):` |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/tools/round-31/c1-sqlite-positive.py` | 2026-10-23 | `048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0` | L113: `if strip_meta(committed) != strip_meta(live):` |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/tools/round-31/sqlite_oracle.py` | 2026-10-23 | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` | L164: `con = sqlite3.connect("file:%s?mode=ro&immutable=1" % path, uri=True)` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/claims.json` | 2026-10-23 | `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` | L43: `no-reader (envelopes fabricated from the oracle or the predictions, never produced by REA)` |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/.ufo/waves/round-31/claims.json` | 2026-10-23 | `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` | L43: `no-reader (envelopes fabricated from the oracle or the predictions, never produced by REA)` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c1/carriers.tsv` | 2026-10-23 | `46f180b837b77297cfba11f4cc805d9f849034e411c279bf5744fa6c21c19211` | L1: `id	path	sha256` |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-31/c1/carriers.tsv` | 2026-10-23 | `46f180b837b77297cfba11f4cc805d9f849034e411c279bf5744fa6c21c19211` | L1: `id	path	sha256` |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/clone/PROVINCE.md` | 2026-10-23 | `a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8` | L332: `Addition to Core (the Core table above is not rewritten; the Frontier list is unchanged by this round):` |
| `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` | 2026-10-23 | `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` | L4: `"version": "6.5.0",` |

## Scratch artifacts and SHA-256

Producing commands: the three absolute-path helper scripts shown above, plus Python SHA-256 aggregation of their captured bytes (summary UTC `2026-10-23T04:15:32+00:00`). `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/artifact-manifest.sha256` records every top-level, non-directory scratch artifact except itself. The two clone-file manifests enumerate every tracked clone path with its own content digest; this is the explicit content inventory for the clone artifact rather than a hash of its changing Git administrative directory.

| Absolute artifact path | SHA-256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/PROVINCE.pristine.md` | `a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/archive-restore.py` | `bd133d01dd289fb25ab26f9088cd8740a63646dc1c5371ab0380f1c1918cd16b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/build-control.py` | `80a2f79c8a12b3b9230d7936c6d44e7ec48df61ab2fb754faa403d0f5210b842` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/control.patch` | `96b0762081facc98bce763e452dc1820ace5f9806730b38e08b1089ab109f910` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/evidence-summary.json` | `f6f46232ccaaff528c51c03a6199e251e261242cb0ce2f39cd664c567df41687` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/fabrication.json` | `2b569ce9de6b1df645901a63304c41b8b791aed702b6697560479193a1c7e8b7` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/mutated-clone-files.sha256` | `0fd2e9c7dbf9cb29c6d729445145e2ef6a6599d9c104027938f611fdf3c6782b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/mutated.json` | `523c5fecb9cdcac6c919c7a2f17de250c2d2aefc47fb31baeac06a504e6b596f` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/mutated.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/mutated.stdout` | `2dcb1e93c38ccb2d365f0841137330529e7d6cdcd9fc2f5a68d64f88d3b629df` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/preparation-errors.txt` | `290c5c0652105a8448f29aa271e3167184045a479fbc83e5fc1899b7a994a290` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/pristine.json` | `09b1665f9282be48217abfd05e1d72d6a9a820b24f0ba675fa439123052a0079` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/pristine.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/pristine.stdout` | `a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/restoration.json` | `3f65a00e9960368fcd6ed371bb92c26891b701a55fc9d622b7284d6bc7020618` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/restoration.stdout` | `59f4feaa4c978c5d7e456dde1c6795c559e182f1262c1394a97019893f4bb29b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/restored-clone-files.sha256` | `9bd101ce59ef8b9469e4df89e875ea29e949ef3b4852547181de44b98529fc4b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/restored.json` | `53ed3b1979ae0eb64d2045276c067714df5c91320f243b828f2e04b0d6b85ad5` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/restored.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/restored.stdout` | `a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/run-counter.py` | `7cde259d102a20ceac38d8e54c8fda91e9c857d7a947c344bcefa182e92bcbeb` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1NoReader/artifact-manifest.sha256` | `0332beaabe5fcabcc8111866ca2585a66d04cf3eb2ad18026459c72e892b92fa` |

CONTROL CtlC1NoReader: met=no score=0/12
