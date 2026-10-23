# MutC1Judge — offline C1 decision-code mutation probe

## Result and scope

- **Observation:** 18 independent, single-line mutants across all four assigned functions: **8 killed, 10 survived, 0 inconclusive**.
- **Observation:** Each mutant received the same bounded `--selftest` command on pristine, mutated and byte-restored source: 54 detector invocations. All 18 pristine and all 18 restored runs exited 0 with `selftest cases=14 failures=0`.
- **Observation:** The current selftest exercises seven `judge` cases and seven `province_ok` cases; it does not call `committed_check` or `entry_ok` (source lines 204–242). All five committed-check mutants and both entry-check mutants survived.
- **Inference:** The survivors are missing-selftest coverage findings, not evidence that the frozen C1 measurement predicate is false and not permission to alter it.
- **Unknown / intentionally not evaluated:** Live REA behavior, carrier results and the frozen `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1` target. No measure-mode command, REA invocation, carrier read or carrier mutation was performed.
- Scope axes: decision-branch coverage, one-defect isolation, bounded detection, exact restoration. The lane counter and contract remain frozen; only this report is written in the lane. No tool installs or updates; no subagents; no Git/JJ writes; no background services or outstanding child processes.

## Source identity and method

Counter: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c1-sqlite-positive.py`.

Frozen commit: `35ba7c522dba55f9be27eb161d4254eacaa24330`. Source SHA256 **S** = `048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0`.

An exact source snapshot is retained at `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/pristine.py`. Each mutant changed just one line in a separate working copy. Mutation snapshots retain the tested altered bytes; every working copy was then overwritten from the exact pristine snapshot in a `finally` restoration path. The detector recorder hashes the source immediately before and after every invocation and never modifies it.

**Observation:** At `2026-10-23T04:14:41.274463+00:00`, the source-identity SHA256 command exited 0; the frozen Git blob command at `2026-10-23T04:14:41.279033+00:00` exited 0 and its stdout bytes hashed to S. Commands and exact source-hash output are retained in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/outputs/source-provenance.json`:

```sh
timeout 30 sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c1-sqlite-positive.py /home/vgpnk/.omp/agent/RULES.md /home/vgpnk/.agents/skills/godspeed/SKILL.md
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file blob 35ba7c522dba55f9be27eb161d4254eacaa24330:tools/round-31/c1-sqlite-positive.py
```

For all detector commands, cwd was `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge` and TMPDIR was `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/tmp`; `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` were unset. Each selftest had a 20-second timeout with a 2-second kill grace, plus a 25-second parent wait cap. The phase driver had an outer 180-second timeout with a 5-second kill grace. Runs completed normally; no timeout or stderr occurred.

Phase-driver commands (all exited 0; individual mutant exits are recorded below):

```sh
timeout --kill-after=5 180 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/run_phase.py pristine
timeout --kill-after=5 180 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/run_phase.py mutated
timeout --kill-after=5 180 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/run_phase.py restored
```

| Phase | Detector UTC start through UTC end | Runs | Exact summary / exit |
|---|---|---:|---|
| pristine | 2026-10-23T04:12:25.387199+00:00 — 2026-10-23T04:12:25.524554+00:00 | 18 | `selftest cases=14 failures=0`, exit 0 |
| mutated | 2026-10-23T04:13:05.843411+00:00 — 2026-10-23T04:13:06.076216+00:00 | 18 | 8 exits 1 with explicit FAIL lines; 10 exits 0 with failures=0 |
| restored | 2026-10-23T04:13:06.148577+00:00 — 2026-10-23T04:13:06.383821+00:00 | 18 | `selftest cases=14 failures=0`, exit 0 |

## Mutant table — observed outputs

Every row is an **observation** from its D-ID detector command listed below. All timestamps are UTC on 2026-10-23; full start/end timestamps, complete stdout/stderr, argv, exit codes and before/after hashes are retained in the phase JSON files. Tabs in exact stdout excerpts are escaped as `\t`. A kill requires a passing pristine run and an explicit selftest FAIL, not merely a process error.

| ID | Function:original line; single-point defect | Expected detector | Mutated UTC start | Exit | Verdict | Exact killing stdout line, or surviving summary |
|---|---|---|---|---:|---|---|
| M01 | `judge:72` — Disable the frozen subject-SHA check | wrong sha | 04:13:05.843411+00:00 | 1 | **killed** | `FAIL\twrong sha\ttables=0 indexes=0 views=0 triggers=0 columns=0` |
| M02 | `judge:75` — Compare schema.tables only | schema differs (view-only difference) | 04:13:05.845071+00:00 | 1 | **killed** | `FAIL\tschema differs\ttables=0 indexes=0 views=0 triggers=0 columns=0` |
| M03 | `judge:70` — Disable the operation check | wrong operation | 04:13:05.845169+00:00 | 1 | **killed** | `FAIL\twrong operation\ttables=0 indexes=0 views=0 triggers=0 columns=0` |
| M04 | `judge:67` — Ignore the exit code; require only ok is True | exit 1 | 04:13:05.847604+00:00 | 1 | **killed** | `FAIL\texit 1\ttables=0 indexes=0 views=0 triggers=0 columns=0` |
| M05 | `judge:67` — Ignore the ok flag; require only exit 0 | Missing: exit 0, otherwise exact envelope, ok False | 04:13:05.847370+00:00 | 0 | **survived** | `selftest cases=14 failures=0` |
| M06 | `judge:75` — Compare schema only, ignoring other report fields | Missing: artifact-only mismatch | 04:13:05.846745+00:00 | 0 | **survived** | `selftest cases=14 failures=0` |
| M07 | `committed_check:107` — Disable the after-freeze gate | Missing: committed envelope not after freeze | 04:13:05.902733+00:00 | 0 | **survived** | `selftest cases=14 failures=0` |
| M08 | `committed_check:113` — Compare raw envelopes instead of stripping meta | Missing: meta-only difference must be accepted | 04:13:05.903229+00:00 | 0 | **survived** | `selftest cases=14 failures=0` |
| M09 | `committed_check:113` — Compare only normalized_result, not the full non-meta envelope | Missing: subject-only committed/live difference | 04:13:05.905443+00:00 | 0 | **survived** | `selftest cases=14 failures=0` |
| M10 | `committed_check:116` — Disable evidence_id-in-entry and missing-ID rejection | Missing: entry omits the live evidence_id | 04:13:05.922262+00:00 | 0 | **survived** | `selftest cases=14 failures=0` |
| M11 | `committed_check:105` — Accept an absent committed envelope | Missing: show returns None | 04:13:05.929733+00:00 | 0 | **survived** | `selftest cases=14 failures=0` |
| M12 | `province_ok:139` — Accept any governing heading | row under Frontier; row under Adjacent exclusion | 04:13:05.934048+00:00 | 1 | **killed** | `FAIL\trow under Frontier\tok`<br>`FAIL\trow under Adjacent exclusion\tok` |
| M13 | `province_ok:138` — Accept prose instead of requiring a table row | prose, not a table row | 04:13:05.961139+00:00 | 1 | **killed** | `FAIL\tprose, not a table row\tok` |
| M14 | `province_ok:138` — Accept a verb row without the entry path | verb without entry | 04:13:05.964864+00:00 | 1 | **killed** | `FAIL\tverb without entry\tok` |
| M15 | `province_ok:139` — Ignore Frontier/Adjacent/exclusion vetoes | row under Adjacent exclusion | 04:13:05.977314+00:00 | 1 | **killed** | `FAIL\trow under Adjacent exclusion\tok` |
| M16 | `province_ok:135` — Update heading only when it mentions Core (sticky placement) | Missing: Core heading followed by Frontier heading and row | 04:13:05.982195+00:00 | 0 | **survived** | `selftest cases=14 failures=0` |
| M17 | `entry_ok:124` — Disable the S096 citation requirement | Missing: present entry without S096 | 04:13:05.991483+00:00 | 0 | **survived** | `selftest cases=14 failures=0` |
| M18 | `entry_ok:123` — Accept an absent entry | Missing: entry_ok(None) | 04:13:05.992647+00:00 | 0 | **survived** | `selftest cases=14 failures=0` |

Exact replacement statements (the only changed line in each copy; indentation remains at the original depth):

```text
M01 judge:72: if False:
M02 judge:75: if got.get("schema", {}).get("tables") != expected.get("schema", {}).get("tables"):
M03 judge:70: if False:
M04 judge:67: if env.get("ok") is not True:
M05 judge:67: if code != 0:
M06 judge:75: if got.get("schema") != expected.get("schema"):
M07 committed_check:107: if False:
M08 committed_check:113: if committed != live:
M09 committed_check:113: if (committed.get("data") or {}).get("normalized_result") != (live.get("data") or {}).get("normalized_result"):
M10 committed_check:116: if False:
M11 committed_check:105: return True, "committed envelope absent"
M12 province_ok:139: if True:
M13 province_ok:138: if "inspect-sqlite-database" in ln and ENTRY in ln:
M14 province_ok:138: if ln.startswith("|") and "inspect-sqlite-database" in ln:
M15 province_ok:139: if "Core" in heading:
M16 province_ok:135: if re.match(r"#{1,6} ", ln) and "Core" in ln:
M17 entry_ok:124: if False:
M18 entry_ok:123: return True, "entry absent"
```

## Survivors — missing selftest cases

**Observation:** M05, M06, M07, M08, M09, M10, M11, M16, M17 and M18 all exited 0 with `selftest cases=14 failures=0`.

**Inference:** The following cases would distinguish the surviving defects from the frozen behavior. They are coverage findings only; they were neither added to the frozen counter nor separately executed:

- **M05:** Keep the operation, subject SHA and normalized_result exact; set exit=0 and ok=False. Expect P1-fail. Also isolate missing/non-True ok values from the exit-code guard.
- **M06:** Keep subject and schema exact but change normalized_result.artifact.sha256 only. Expect P1-fail. The frozen predicate also names wal, engine name and database_encoding; these need independently varying cases.
- **M07:** Supply an otherwise matching committed envelope and evidence reference with first-added time equal to or before freeze_ct; expect False. Missing freeze_ct and missing first-added time also require rejection cases, plus a valid after-freeze acceptance case.
- **M08:** Supply after-freeze committed/live envelopes identical except meta, with the evidence_id cited in the entry; expect True. This survivor is an over-rejection defect, not a weakened acceptance rule.
- **M09:** Keep normalized_result equal but change the committed subject (or another non-meta field), with all other gates valid; expect False. This protects the full-envelope rule rather than normalized_result-only equality.
- **M10:** Supply matching after-freeze envelopes but omit their live evidence_id from the entry; expect False. Separately test a missing/empty live evidence_id.
- **M11:** Make the committed envelope absent (show returns None); expect False, before any history or JSON comparison.
- **M16:** Use ## Core, then ## Frontier, then the valid verb-and-entry table row; expect False. The existing isolated Frontier case lacks a preceding Core heading and therefore does not kill sticky-heading state.
- **M17:** Pass a present entry that does not cite S096; expect False. Pair it with a present, S096-citing entry expecting True.
- **M18:** Call entry_ok(None); expect False. The current province absent case exercises a different function.

## Exact detector commands

D-ID identifies the producing command for the matching table row. Each command was invoked once in each phase on the same absolute working-copy path:

```sh
# D-M01
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M01/c1-sqlite-positive.py --selftest
# D-M02
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M02/c1-sqlite-positive.py --selftest
# D-M03
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M03/c1-sqlite-positive.py --selftest
# D-M04
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M04/c1-sqlite-positive.py --selftest
# D-M05
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M05/c1-sqlite-positive.py --selftest
# D-M06
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M06/c1-sqlite-positive.py --selftest
# D-M07
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M07/c1-sqlite-positive.py --selftest
# D-M08
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M08/c1-sqlite-positive.py --selftest
# D-M09
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M09/c1-sqlite-positive.py --selftest
# D-M10
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M10/c1-sqlite-positive.py --selftest
# D-M11
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M11/c1-sqlite-positive.py --selftest
# D-M12
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M12/c1-sqlite-positive.py --selftest
# D-M13
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M13/c1-sqlite-positive.py --selftest
# D-M14
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M14/c1-sqlite-positive.py --selftest
# D-M15
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M15/c1-sqlite-positive.py --selftest
# D-M16
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M16/c1-sqlite-positive.py --selftest
# D-M17
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M17/c1-sqlite-positive.py --selftest
# D-M18
timeout --kill-after=2 20 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M18/c1-sqlite-positive.py --selftest
```

## Restoration evidence

**Observation:** Each ID has byte chain **S → mutant snapshot SHA256 → S**, where S is `048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0` and the corresponding mutant hash is listed in the artifact inventory below. Pristine and restored per-run before/after hashes are S for all 18 IDs. Mutated per-run before/after hashes are equal to their retained mutation-snapshot hashes. The detector itself changed no source bytes.

**Observation:** All 18 restoration copy commands exited 0; their exact argv, UTC start times and outputs are retained in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/outputs/command-runs.json`. The final 18 restored selftests all exited 0 with `selftest cases=14 failures=0`; full records are at `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/outputs/restored.json`.

**Observation:** The source-identity command above also reports the lane source SHA256 as S after the probes. No lane source restoration was necessary because no lane source was modified. All started child commands completed synchronously; no process tree remains to kill.

## Opened local primary sources

Access date for all: **2026-10-23**. No network source was opened. Each located quote is at most 25 contiguous words. The policy/skill sources are listed for completeness, not as counter-behavior evidence.

| URL | SHA256 of bytes | Located quote |
|---|---|---|
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c1-sqlite-positive.py` (also the frozen Git blob and pristine snapshot) | `048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0` | line 130: “A table row naming the verb and the entry whose governing heading names Core.” |
| `file:///home/vgpnk/.omp/agent/RULES.md` | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | line 12: “never pipe an unverified remote script into a shell.” |
| `file:///home/vgpnk/.agents/skills/godspeed/SKILL.md` | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | line 10: “You are a Godspeed-enabled subagent.” |

## Artifact inventory

All scratch files are enumerated below with SHA256. The empty temporary directory is `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/tmp`. Inventory-producing command, exit 0, UTC `2026-10-23T04:14:41.296433+00:00`: `timeout 30 sha256sum` followed by every artifact path in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/outputs/artifact-inventory.json` (its exact argv and full stdout are retained there).

```text
16637c29bcc51550ab54a00ecc185a4c929fb406b59b643e1e03082d7d95fe01  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/run_phase.py
d23336ec7ee9a5bd7053fd30cd397cbb82b70e0a86562e8ad0f451ae7ae5e298  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/outputs/setup.json
f44598b874a1036676ab07d5a06f2b43cb22590869d32ba2768839c7f31628c7  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/outputs/pristine.json
e0857ac6324257c0667535ddc7722ed5ced650a1088f2287c17d72c6e397271c  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/outputs/mutated.json
18d3cc158689ee7765268de0a48bef74da9e0bb06d0113afc97569df052b77c3  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/outputs/restored.json
a068b703dea83a857c69b0792a6128ea0964d2632db143544d14d22bbb7a78a7  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/outputs/command-runs.json
30e55d6acbc0d78c0da2e96275d6bd2874fc21360c9e2ccd28a0450b8d3c0d15  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/outputs/source-provenance.json
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/pristine.py
fcfef0b12fb20505db145b29e88ad492db8ea54a200a093252aff6b18712c783  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M01.py
18e199906dda5a3265f693b1002adf06929f049d37629d623c7501868468740a  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M02.py
71619e303c8e5a2d08c58d93b5b9147cb290ec00f58c66a3f5b495d08ad2ea5c  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M03.py
122dc3620c101a27fce2bd8a5f54ae958482cc9718ebfe46a36eff5eeec9fee3  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M04.py
de0a09c9dc35c0773e020c2d042b702a2e1502de15821d50fc66c647855f8e00  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M05.py
a4d24c7da52b0ddfde40de9599fd5b2c6c83e71c1c8840570a1fd70e82008e07  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M06.py
c23c3a6572bba036dd61ce731c0c8ed82e904a6ffdc90d3690e382628ec92391  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M07.py
2a7b3e08492924c460cf8b565a610ba2045e5d7e07a7096f140a7c59074a39f4  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M08.py
d378d4791df66799d882048a6175ba133d0a55510755104d332b301aa9bc39af  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M09.py
95751699a2c7de4148dc839652529663ce5ad2411537ee38a3dc94e247507896  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M10.py
6309db893fbc6f2cb68a52a01664407f237f98672ea9cecba578949d1a92efbf  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M11.py
a8b2ea2818ca982b67ef26b151ad46e73d65cae451a48e541a2ecedb340f282b  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M12.py
d52a2bf88c985892a802f95c35417811dd6a523dcc417e01ab2322dd52d53592  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M13.py
c1400608e1cefdc5dc229291bf464b809f5130522bec360cf4052e09813f5f7b  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M14.py
4f57687e0e2a3bf39f949677394a360e786e6924d0f85b694a4cf4de75178d65  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M15.py
4708d23b4e4e98631711177bc196354c972b31893ecb8166c5ad88ba9f5e55f0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M16.py
b11863913c1bd67972d875da8860324852ac6c99f78b2afcff7a3605afb7bace  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M17.py
a1f2721fe1a695f10afb6ffb1f1f84fbf98ffe331021e16fa729c83e6f5405c5  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/snapshots/M18.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M01/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M02/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M03/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M04/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M05/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M06/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M07/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M08/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M09/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M10/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M11/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M12/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M13/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M14/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M15/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M16/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M17/c1-sqlite-positive.py
048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/work/M18/c1-sqlite-positive.py
a00301ff5b35e58917535a8bcdf77099ba5fc1c34437313bb81e099171ccf3bf  /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC1Judge/outputs/artifact-inventory.json
```

No integration, contract change, measurement run or additional mutation probe was performed.
