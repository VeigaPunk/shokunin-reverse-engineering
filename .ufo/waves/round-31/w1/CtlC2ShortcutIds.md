# CtlC2ShortcutIds — R31-C2 pre-data ID-shortcut control
CONTROL CtlC2ShortcutIds: met=no score=1/23
## Scope, mutant and verdict
- **Observation:** the assigned control did **not** meet the frozen 23/23 target: exit 1, matches 1/23, with both documentation gates satisfied. The attempted target bypass fails for this rotation.
- **Mutation-testing verdict: inconclusive**, not a killed mutant: the required pristine freeze baseline itself exits 1 because all committed envelopes and both documentation surfaces are absent. The restored baseline repeats that result exactly.
- **Observation:** one swapped record survives: `m-not-sqlite` holds the real envelope of the next request, `m-bad-pagesize`, and receives P2-match. The two real envelopes are equal after removing only top-level meta; both say `file is not a database`. This is a coverage/identity limitation, not a whole-control target bypass and not permission to amend the frozen contract.
- Axes: request-to-envelope binding, frozen-target false-positive discrimination, and exact restoration/containment.
- Expected detector: the frozen counter compares every committed/live envelope field except top-level meta, at lines 232–248; the mismatch at lines 244–245 is applied by lines 342–345. Its target/exit gate is lines 361–363. No counter, prediction, oracle, claim, carrier or mutant bytes were changed.

## Control construction
- Isolated clone: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone`. Original freeze: `35ba7c522dba55f9be27eb161d4254eacaa24330`. Branch `ctl` was created there using the contract clone/checkout commands.
- Control commit: `fe9f14ae1ddd5c574497991eef1d43aa335770f3`; commit timestamp 2026-10-23T04:12:58Z; author/committer `ctl <ctl@local>`. It remains reachable through `refs/heads/ctl`.
- Ran all 23 frozen requests directly, once each, using the exact path and JSON argument array from predictions.tsv, REA 6.5.0, CLI JSON/full-output mode, cwd `/tmp`, and the seat TMPDIR. Captured stdout, stderr, exit and UTC interval per request. Observed 20 exits 1 and 3 exits 0, no harness timeouts, 2026-10-23T04:11:37Z–04:11:57Z.
- For each destination id at ordinal i, wrote the unchanged real stdout bytes from ordinal `(i + 1) % 23` to its committed JSON file. All 23 source/destination hashes agree. The last request, `m-wal-over`, wraps to the first, `q-rowlimit-no-table`.
- Added the sandbox knowledge entry naming every id and citing S092. Appended the 23-row SKILL decision table using the frozen outcomes, error codes, issue paths/reasons and exact message templates. These are explicitly marked negative-control material.
- Committed exactly 25 changed files: SKILL, one entry, and 23 envelope JSON files. The frozen target was not changed or rescaled. No control envelopes were copied into the lane.
- Control bytes are retained in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/control-files.tar` (SHA256 `e4ab6905bcae84259e7ee54700fb795240dad377d036f206380769c8fbd6f9b9`) as well as commit `ctl`.

### Changed control files and SHA256 at the measured commit
| Absolute file | SHA256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/SKILL.md` | `64e4d43286f24f84c74b7031b98c49d134e667c9760e87f0780245af1226fc26` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` | `5ed8fcdf01f17147bcadd54133db322942212591a2562d16ded5492dc3a210f0` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/q-rowlimit-no-table.json` | `c2789ba2034ade451de446402db71d573908f57b258bd2b32a9a44ae4999f3c0` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/q-columns-no-table.json` | `8599b202e081572b5a64519e60c5c8e562ae86692ce432b5ab1cd853a6fb512a` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/q-scope-no-table.json` | `3aad7e1987b51f97b96602e12b2846c818364b754a4e5296f96e48fb83ecdf7d` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/q-missing-table.json` | `df1849861cd7074b56f4600faf8189c522094f3034d276428057f8c050d35898` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/q-case-table.json` | `79689c07d4e11430a08f87c527fb8ea01b6fe46f84086ab100bf728203ee2913` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/q-view-as-table.json` | `fc8251dad6f69347df8fba53308714b62bd1fdadbe5099f9c9ed9ac529668d51` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/q-missing-column.json` | `c3c002bb48edecd12b730b083a83a1b4595c956381a4e019b8f9b7d5052a4509` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/q-virtual-rows.json` | `5ca97ad4765d33517157b4799036a45fe55203a94d7244a8f2ec0eda5b13a002` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/q-shadow-rows.json` | `9a5f8df5261d3f37c6a3f134047bf93664bf467137fea826b2baee8cc70bc0a6` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/q-ok-rows.json` | `50fd44a103724bfd71dd7174689873b5411da851915ba1c75eb0fc2235f7e371` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/m-missing.json` | `4cbd614b1b9159f2c3c09339570c6034005f31bdd2857cf0b8f9e5c60a7d1723` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/m-enotdir.json` | `fe524e1e15372fdda070334c85ed1d8785f024970d6a0905fe97f666947aa415` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/m-not-sqlite.json` | `12b802db26f0ab64d9a102238d1bcb8f9929e2bdd4bba0867526fde6588b5eca` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/m-bad-pagesize.json` | `dda7549f7e2c4353f6c32ab4e747bf452b9b961e6f142395dd5b9857d33522a2` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/m-journal-hot.json` | `83ea60f9b3a333d8a1c2b149cf6635582fc98e4f6f084c5a0cbcfd347bf61a78` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/m-journal-short.json` | `100d895259311f26ada6b5fb1fdd3eef82580164b79fd5e0bb0678995f60a3a3` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/m-journal-empty.json` | `49ac63d8a86daea45a74a9396dff1828374853aced418657d878dd8677689009` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/m-journal-zero28.json` | `2208e2ff56b2eb473e13f77df7b16e31b0212dbf1fe7788df95b51169004a090` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/m-journal-symlink.json` | `56366fa4e8b7f0250e38238829d599a36bcf9e638ce33fb93b7ad9d799c33f0e` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/m-db-symlink.json` | `062d9a70a8605c5aa7af62b51114f47ad1a87e984ed40bcb4cf6c4090945cda8` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/m-directory.json` | `02677f59352d401272f92d6ea220f13f920eb8608619dde848d764fe3ca187c7` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/m-over-256mib.json` | `df06c4b55a257f67bf8c7d93ec375a4ce6cff062d2c52f32de1c01427f93b28a` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/corpus/evidence/round-31/c2/envelopes/m-wal-over.json` | `e98c824737aca7f52d75de34f162175141091e7675bed99823d20b6055a75acc` |

## Exact counter commands, full stdout and exits
Every command below ran with cwd `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds` and environment `TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/tmp`. The harness unsets GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE. No --write-evidence flag was used. The control measurement used HEAD while HEAD was `fe9f14ae1ddd5c574497991eef1d43aa335770f3`; after restoration HEAD is the freeze, so replay the control using that explicit commit or `ctl`.

### Pristine freeze, before control edits/commit
UTC: `2026-10-23T04:11:37+00:00` through `2026-10-23T04:11:58+00:00`. **Exit: 1.** Stderr: empty. Harness timeout: false.

Exact counter command:
```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Full stdout:
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

Stdout SHA256: `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0`; stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

### Committed rotated-envelope control
UTC: `2026-10-23T04:13:05+00:00` through `2026-10-23T04:13:32+00:00`. **Exit: 1.** Stderr: empty. Harness timeout: false.

Exact counter command:
```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone --rev HEAD
```

Full stdout:
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
m-not-sqlite	P2-match	refused invalid_request invalid_format
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
requests=23 matches=1 target=23 entry_ok=1 (ok) skill_ok=1 (ok)
```

Stdout SHA256: `a90704812d87d071591a18154e9e083e32d20eb0e732c214dc05a1308e753c21`; stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

### Restored freeze
UTC: `2026-10-23T04:14:24+00:00` through `2026-10-23T04:14:45+00:00`. **Exit: 1.** Stderr: empty. Harness timeout: false.

Exact counter command:
```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Full stdout:
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

Stdout SHA256: `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0`; stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Located row-level survivor
- **Observation:** control stdout at 2026-10-23T04:13:05Z–04:13:32Z, exit 1, contains exactly:

```text
m-not-sqlite	P2-match	refused invalid_request invalid_format
requests=23 matches=1 target=23 entry_ok=1 (ok) skill_ok=1 (ok)
```
- The full target was not met, so there is no clause admitting the entire control. The one-record allowance is the specified `strip_meta(committed) == strip_meta(live)` rule (counter lines 143–146 and 244): the real error envelopes for the zero-magic and invalid-page-size files contain the same error fields and no distinct request-file identity outside meta.
- **Observation:** bounded offline summary command (exit 0, UTC 2026-10-23T04:15:03Z):

```sh
timeout 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/summarize.py
```

Exact output excerpts:
```json
"all_rotation_source_and_destination_hashes_equal": true
"before_and_restored_manifest_bytes_equal": true
"raw_bytes_equal": false
"envelopes_equal_except_top_level_meta": true
```
- The two raw stdout hashes are `fe524e1e15372fdda070334c85ed1d8785f024970d6a0905fe97f666947aa415` (m-not-sqlite) and `12b802db26f0ab64d9a102238d1bcb8f9929e2bdd4bba0867526fde6588b5eca` (m-bad-pagesize). Their canonical, meta-stripped envelope SHA256 is `de25a14f00302d3c610d309089cc3819f3ed71ea25ef86f320495a21e2b2fcf5`.
- **Inference:** a detector required to distinguish producer request identity could not distinguish this pair from those fields alone. The frozen full-envelope equivalence predicate intentionally does not require such provenance; no contract change is proposed or performed.

## Exact-byte restoration
- Restored the clone working tree non-destructively to the freeze commit after preserving the committed control. Producing command (exit 0; snapshot UTC 2026-10-23T04:14:13Z):

```sh
timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/clone checkout -q --detach 35ba7c522dba55f9be27eb161d4254eacaa24330 && timeout 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/probe.py snapshot restored
```
- **Observation:** all 30 affected-or-pinned paths in the before/restored manifests have identical status/hash. SKILL returned from `64e4d43286f24f84c74b7031b98c49d134e667c9760e87f0780245af1226fc26` to exact original SHA256 `3e5cbfbc44c30fe686abe1177fe501c1c0c9e1ab141be97ed83b787b6401c31a`. The newly added entry and all 23 envelope files are absent again. Frozen predictions, instrument, oracle, claims and carrier list are unchanged.
- Before-manifest SHA256 = restored-manifest SHA256 = `5098144d6b53aa27f3ef57ef8bd655eeec913f8205291aefb4c37bdfab8180d9`. Mutated manifest SHA256 = `af1552b8a50496a9cb00120ba876d88946274c161aaa7892147802d8088dce3c`. The restored detector stdout is byte-identical to pristine stdout (SHA256 `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0`) and both exit 1.
- All captured subprocesses completed; the harness kills each owned process group in its finally path. No services were started. Removed only this seat's owned Node compile cache after all runs; raw outputs and control files remain retained. No immutable carriers, mutants, downloads, sibling sources, lane Git index or lane jj state were modified.

## Direct request commands and receipts
Collection producing command: `timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/probe.py collect` (exit 0; interval 2026-10-23T04:11:37Z–04:11:57Z). All per-request commands below used `TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/tmp` and cwd `/tmp`. The corresponding absolute stdout/stderr/metadata files and every SHA256 are listed in the artifact inventory. The full metadata collection and rotation mapping are also retained.

| Request | Exact bounded REA command | UTC start → end | Exit |
|---|---|---|---|
| `q-rowlimit-no-table` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite --row-limit 5 --format json --full-output` | 2026-10-23T04:11:37+00:00 → 2026-10-23T04:11:38+00:00 | 1 |
| `q-columns-no-table` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite --column Name --format json --full-output` | 2026-10-23T04:11:38+00:00 → 2026-10-23T04:11:39+00:00 | 1 |
| `q-scope-no-table` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite --schema-scope selected_table --format json --full-output` | 2026-10-23T04:11:39+00:00 → 2026-10-23T04:11:39+00:00 | 1 |
| `q-missing-table` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite --table NoSuchTable --format json --full-output` | 2026-10-23T04:11:39+00:00 → 2026-10-23T04:11:40+00:00 | 1 |
| `q-case-table` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite --table album --format json --full-output` | 2026-10-23T04:11:40+00:00 → 2026-10-23T04:11:41+00:00 | 1 |
| `q-view-as-table` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/proj-371.db --table coordinate_operation_view --format json --full-output` | 2026-10-23T04:11:41+00:00 → 2026-10-23T04:11:42+00:00 | 1 |
| `q-missing-column` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite --table Album --column Nope --format json --full-output` | 2026-10-23T04:11:42+00:00 → 2026-10-23T04:11:43+00:00 | 1 |
| `q-virtual-rows` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-curve.gpkg --table rtree_curve_geometry --format json --full-output` | 2026-10-23T04:11:43+00:00 → 2026-10-23T04:11:44+00:00 | 1 |
| `q-shadow-rows` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-curve.gpkg --table rtree_curve_geometry_node --format json --full-output` | 2026-10-23T04:11:44+00:00 → 2026-10-23T04:11:45+00:00 | 1 |
| `q-ok-rows` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite --table Album --row-limit 3 --format json --full-output` | 2026-10-23T04:11:45+00:00 → 2026-10-23T04:11:46+00:00 | 0 |
| `m-missing` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-missing/db.sqlite --format json --full-output` | 2026-10-23T04:11:46+00:00 → 2026-10-23T04:11:47+00:00 | 1 |
| `m-enotdir` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-enotdir/file/db.sqlite --format json --full-output` | 2026-10-23T04:11:47+00:00 → 2026-10-23T04:11:47+00:00 | 1 |
| `m-not-sqlite` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-not-sqlite/db.sqlite --format json --full-output` | 2026-10-23T04:11:47+00:00 → 2026-10-23T04:11:48+00:00 | 1 |
| `m-bad-pagesize` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-bad-pagesize/db.sqlite --format json --full-output` | 2026-10-23T04:11:48+00:00 → 2026-10-23T04:11:49+00:00 | 1 |
| `m-journal-hot` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-journal-hot/db.sqlite --format json --full-output` | 2026-10-23T04:11:49+00:00 → 2026-10-23T04:11:50+00:00 | 1 |
| `m-journal-short` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-journal-short/db.sqlite --format json --full-output` | 2026-10-23T04:11:50+00:00 → 2026-10-23T04:11:51+00:00 | 1 |
| `m-journal-empty` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-journal-empty/db.sqlite --schema-scope database --format json --full-output` | 2026-10-23T04:11:51+00:00 → 2026-10-23T04:11:52+00:00 | 0 |
| `m-journal-zero28` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-journal-zero28/db.sqlite --schema-scope database --format json --full-output` | 2026-10-23T04:11:52+00:00 → 2026-10-23T04:11:53+00:00 | 0 |
| `m-journal-symlink` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-journal-symlink/db.sqlite --format json --full-output` | 2026-10-23T04:11:53+00:00 → 2026-10-23T04:11:54+00:00 | 1 |
| `m-db-symlink` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-db-symlink/db.sqlite --format json --full-output` | 2026-10-23T04:11:54+00:00 → 2026-10-23T04:11:55+00:00 | 1 |
| `m-directory` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-directory/db.sqlite --format json --full-output` | 2026-10-23T04:11:55+00:00 → 2026-10-23T04:11:55+00:00 | 1 |
| `m-over-256mib` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-over-256mib/db.sqlite --format json --full-output` | 2026-10-23T04:11:55+00:00 → 2026-10-23T04:11:56+00:00 | 1 |
| `m-wal-over` | `timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-wal-over/db.sqlite --format json --full-output` | 2026-10-23T04:11:56+00:00 → 2026-10-23T04:11:57+00:00 | 1 |

## Opened source receipts
Only local files were opened as primary sources; no HTTP fetch, browser, access-control workaround or additional REA version was used. Each source quote below is at most 25 contiguous words; access date is 2026-10-23. Source SKILL hashes refer to its unmodified frozen bytes, before the clone-only table addition.

```text
url	access_date	sha256	line	quote
file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c2-sqlite-refusals.py	2026-10-23	d23948959835038f4622261b551616863af1e47f3c66a558b8f3b5a232e28223	245	committed envelope differs from the live envelope (full comparison)
file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c2/predictions.tsv	2026-10-23	acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8	14	file is not a database
file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/claims.json	2026-10-23	6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51	44	shortcut keyed on ids/labels (another carrier's or request's envelope under the id)
file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md	2026-10-23	3e5cbfbc44c30fe686abe1177fe501c1c0c9e1ab141be97ed83b787b6401c31a	35	Label every conclusion observation / inference / unknown.
file:///home/vgpnk/.omp/agent/RULES.md	2026-10-23	beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed	14	Record every install or update — tool, version, channel, reason — in your report or handoff.
file:///home/vgpnk/.agents/skills/godspeed/SKILL.md	2026-10-23	1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a	12	Name the axes.
file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md	2026-10-23	056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692	19	The REA MCP server is not registered on this host, by design.
```

## Retained artifact inventory
All scratch artifacts are under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds`. The clone is preserved with the control commit on `ctl` and the restored freeze checked out; its changed-file bytes are identified above and archived. The inventory manifest `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/artifacts.tsv` lists 89 regular evidence files, SHA256 `6be4b331a4c38e0bdb7229e163bc684129107aa45334480924dba4cf30b4a90a`. The manifest itself is included separately below. No per-tool install or update was performed; the requested existing npx pin `rea-agents@6.5.0` was used. No builds, formatters, linters or unrelated test suites were run.

| Absolute artifact | SHA256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/control-files.tar` | `e4ab6905bcae84259e7ee54700fb795240dad377d036f206380769c8fbd6f9b9` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/entry.txt` | `5ed8fcdf01f17147bcadd54133db322942212591a2562d16ded5492dc3a210f0` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/artifacts.tsv` | `6be4b331a4c38e0bdb7229e163bc684129107aa45334480924dba4cf30b4a90a` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/before-hashes.tsv` | `5098144d6b53aa27f3ef57ef8bd655eeec913f8205291aefb4c37bdfab8180d9` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/collection.json` | `7570a964b02e4e7c16268072e5c125de60df5758440da4b39fe4f123f5d2a117` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/control-hashes.tsv` | `af1552b8a50496a9cb00120ba876d88946274c161aaa7892147802d8088dce3c` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/control.json` | `13b080776e13991323a325519756ff7ed990ba8f089dea36ca522dbe2664f181` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/control.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/control.stdout` | `a90704812d87d071591a18154e9e083e32d20eb0e732c214dc05a1308e753c21` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/pristine.json` | `7e9b4f0489d6fe0da848e4d8f6bd7589b721c1b8c2f79c080caad7af3cff91cc` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/pristine.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/pristine.stdout` | `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/restored-hashes.tsv` | `5098144d6b53aa27f3ef57ef8bd655eeec913f8205291aefb4c37bdfab8180d9` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/restored.json` | `bae040b0f98ccb7ba8e632535ec9203e0fea40345514c0212667df3b1d9ad67a` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/restored.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/restored.stdout` | `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/rotation.tsv` | `8ab99d6015b19c295436df33dc8d53b5268bd573b763048c74a07d46d94022eb` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/sources.tsv` | `5814f80423219c7c1d0eb5fc0f561abc2596b76e8f07b31ca16b6f3f2299a6a2` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/out/summary.json` | `46378668b5c5afc664531180b6d853b8b0871f2673e234164b64a8f66a8ce7d5` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/probe.py` | `a1bec210a5a678ca223a1d9e9908e97dbebd0babd990c69a1145f9ce29b9545b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-bad-pagesize.json` | `c2c392d69a0c346aecaf31b3335a949ed5e5e534f27b0ba4cd56948f5cf67c81` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-bad-pagesize.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-bad-pagesize.stdout` | `12b802db26f0ab64d9a102238d1bcb8f9929e2bdd4bba0867526fde6588b5eca` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-db-symlink.json` | `0bde1498765b5aa2a1fef593279de3e0679ac9fee854382f2c290386dbde120c` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-db-symlink.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-db-symlink.stdout` | `56366fa4e8b7f0250e38238829d599a36bcf9e638ce33fb93b7ad9d799c33f0e` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-directory.json` | `74d24f6ac31116211c7d09ea45722644fa4c45eec54d1ed21bc7565eb3f20cf2` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-directory.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-directory.stdout` | `062d9a70a8605c5aa7af62b51114f47ad1a87e984ed40bcb4cf6c4090945cda8` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-enotdir.json` | `a9edd2f43f7941f21abf325d2bfe9c95ccc26c8667ace75c822c91fe5d6e9018` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-enotdir.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-enotdir.stdout` | `4cbd614b1b9159f2c3c09339570c6034005f31bdd2857cf0b8f9e5c60a7d1723` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-empty.json` | `94bfc125afe40ab6c5a30dbf1421dbe05f6161a4ce6ca32d386b18ffd8a95750` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-empty.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-empty.stdout` | `100d895259311f26ada6b5fb1fdd3eef82580164b79fd5e0bb0678995f60a3a3` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-hot.json` | `d48cbee8d185a90a88927f975ed7ce2f515b48e96cccd82d9cd2af99b9b4aa01` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-hot.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-hot.stdout` | `dda7549f7e2c4353f6c32ab4e747bf452b9b961e6f142395dd5b9857d33522a2` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-short.json` | `51f22513c20517114539de3bdd5c808a2f5e090d245f754aa02448738a94d8f8` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-short.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-short.stdout` | `83ea60f9b3a333d8a1c2b149cf6635582fc98e4f6f084c5a0cbcfd347bf61a78` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-symlink.json` | `cf3a323d04993c2b05ff521000cffa02d69f549f3f408b8ed3d6745f14052a5b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-symlink.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-symlink.stdout` | `2208e2ff56b2eb473e13f77df7b16e31b0212dbf1fe7788df95b51169004a090` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-zero28.json` | `bc9dc7de96761f6bbc9c77bd5a92455c65861f8261578afd7a406bc82419b8af` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-zero28.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-journal-zero28.stdout` | `49ac63d8a86daea45a74a9396dff1828374853aced418657d878dd8677689009` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-missing.json` | `59e17c4314dc7e6572323a9514e67c39e3b00c99a995eb19bda7a9602ec428d6` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-missing.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-missing.stdout` | `50fd44a103724bfd71dd7174689873b5411da851915ba1c75eb0fc2235f7e371` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-not-sqlite.json` | `0c63597e1c58a127ad6d5030dac2fc406524765496a3a1bdb7ef8b0f1c750dc5` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-not-sqlite.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-not-sqlite.stdout` | `fe524e1e15372fdda070334c85ed1d8785f024970d6a0905fe97f666947aa415` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-over-256mib.json` | `a875fe574c0b9e53228ab9b2b29ee01560001d8b2b91729e7b495ead0e831688` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-over-256mib.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-over-256mib.stdout` | `02677f59352d401272f92d6ea220f13f920eb8608619dde848d764fe3ca187c7` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-wal-over.json` | `5ddfe1339d4ba0cc79db8217ddbb8a6b6c647fc9ddc54ee07c62fc9b94a3cc88` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-wal-over.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/m-wal-over.stdout` | `df06c4b55a257f67bf8c7d93ec375a4ce6cff062d2c52f32de1c01427f93b28a` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-case-table.json` | `dc2c5c6f013f76613a6794e0046e05e9aa0dbb6e1670de5d820abe26c8858967` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-case-table.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-case-table.stdout` | `df1849861cd7074b56f4600faf8189c522094f3034d276428057f8c050d35898` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-columns-no-table.json` | `067f2cd82cd71af6a4ca62b928132132028aab39084f98da4caa3a583c9cfa56` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-columns-no-table.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-columns-no-table.stdout` | `c2789ba2034ade451de446402db71d573908f57b258bd2b32a9a44ae4999f3c0` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-missing-column.json` | `f80e1af5b607783b9085e9ed58207ba1c7ff9f58e25363f29f78e49e4b5f7f56` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-missing-column.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-missing-column.stdout` | `fc8251dad6f69347df8fba53308714b62bd1fdadbe5099f9c9ed9ac529668d51` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-missing-table.json` | `7e13832407a427eaca95afb4bed75b3382f17b9ac1ef39073c3e8695bf12602b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-missing-table.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-missing-table.stdout` | `3aad7e1987b51f97b96602e12b2846c818364b754a4e5296f96e48fb83ecdf7d` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-ok-rows.json` | `50eef5e4627b8d34ad3e1ba43132899fa6e6024fa2f5937f4253b91a967c4a00` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-ok-rows.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-ok-rows.stdout` | `9a5f8df5261d3f37c6a3f134047bf93664bf467137fea826b2baee8cc70bc0a6` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-rowlimit-no-table.json` | `d034ae7f1e5048bde425302d3f58a5d42f15a05f9e3c33efa0e2d89b23c8e091` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-rowlimit-no-table.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-rowlimit-no-table.stdout` | `e98c824737aca7f52d75de34f162175141091e7675bed99823d20b6055a75acc` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-scope-no-table.json` | `2edc9632034d04d94dd862d987fef240a1efac58ad2f27e99d71eb52c5294e6f` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-scope-no-table.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-scope-no-table.stdout` | `8599b202e081572b5a64519e60c5c8e562ae86692ce432b5ab1cd853a6fb512a` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-shadow-rows.json` | `7ee9428bc7c1ce64de82698dac41acba2a9885c95a2ad44c1d5c1463d2ab6c9a` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-shadow-rows.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-shadow-rows.stdout` | `5ca97ad4765d33517157b4799036a45fe55203a94d7244a8f2ec0eda5b13a002` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-view-as-table.json` | `588c52e5bbe31f61798ba84d3727466360479783fc0e80f9bbf3c88c90e0b60c` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-view-as-table.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-view-as-table.stdout` | `79689c07d4e11430a08f87c527fb8ea01b6fe46f84086ab100bf728203ee2913` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-virtual-rows.json` | `592b33b5d76422f81efd5c616e9b534723b06698dda05e1d910ed4a2186c7f51` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-virtual-rows.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/rea/q-virtual-rows.stdout` | `c3c002bb48edecd12b730b083a83a1b4595c956381a4e019b8f9b7d5052a4509` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2ShortcutIds/summarize.py` | `579f20d58236923d2979d5edb9d97ca231401b6466b87d498e8999ca77bd3960` |

## Completion
**Observation:** required control, pristine comparison, restored comparison, full counter stdout, exact commands, UTC times, exit codes, control file hashes, raw REA outputs and restoration evidence are recorded. No blocker. The scoped assignment is complete.
