# R30-C1 control — CtlC1DoNothing

CONTROL CtlC1DoNothing met_target=no

## Result and attack verdict

- **Observation:** the untouched control did not meet the frozen target in either run. The first run exited **2** at the input guard. After L1 restored the shared inputs and explicitly requested a rerun, the rerun exited **1** with **carriers=16 pass=0 target=16 entry_ok=0 province_ok=0**.
- **Attack:** can the unchanged freeze revision, with no committed C1 envelopes, entry, PROVINCE line or SOURCES row, pass solely because the counter runs REA live?
- **Verdict: holds for this control.** The attempted do-nothing bypass fails: all 16 carriers were rejected for absent post-freeze committed envelopes; the entry and PROVINCE gates also failed. The initial PIN-blocked run alone was inconclusive.
- **Impacted axes:** R30-C1 coverage and control validity/input identity. No conclusion about R30-C2 depth.
- **Smallest safe correction:** the initial prerequisite repair was restoration of the exact frozen carrier bytes, performed by L1 rather than this seat. No control, predicate, manifest or counter change was needed. This result does not establish robustness against the other controls or admit the coverage claim.

## Construction

The following construction command completed successfully with no stdout/stderr:

```sh
timeout 30 mkdir -p /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/tmp && timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/clone
```

No edits or commits were made in the sandbox. No envelope, knowledge entry, PROVINCE line or SOURCES row was added. The capture script and receipts were written outside the clone. Both counter runs used that same untouched state; the second run was specifically requested after shared-input restoration, not after a control edit.

The timed identity command, run with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset, was:

```sh
timeout 30 git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/clone log -1 --format=%H%n%D%n%cI main
```

UTC start/end: **2026-10-23T02:43:03+00:00**. Exit **0**. Full stdout:

```text
4ee65c6771058284aa947a266475839d196ed4d4
HEAD -> main, origin/main, origin/HEAD
2026-10-22T23:35:13-03:00
```

Thus the sandbox commit was the required **4ee65c6771058284aa947a266475839d196ed4d4**. The construction command itself did not record a wall-clock timestamp; the timed identity receipt establishes the clone's state before the counter.

## First run — exact counter command and complete output

Working directory: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing`.
Environment: GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset; TMPDIR set to `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/tmp`.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/clone/tools/round-30/c1-rust-positive.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/clone --rev main
```

UTC start/end: **2026-10-23T02:43:03+00:00**. Counter exit **2**.

Full counter stdout:

```text
PIN carrier elf-x86_64-uvx absent or altered at /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx
```

Full counter stderr: **empty**.

The frozen target `carriers=16 pass=16 target=16 entry_ok=1 province_ok=1`, exit 0, was **not met**. No predicate clause let the control through. In this first run, no REA invocation was reached. No carrier or mutant was executed in either run: the rerun used only the assigned read-only REA inspections. Both capture process groups were disposed of after completion; no seat-started process remains running.

## Initial input-identity blocker and evidence

**Observation at the first run:** the carrier existed, but its bytes did not match the frozen manifest. The follow-up evidence was recorded at **2026-10-23T02:43:56+00:00**; the standalone hash command did not itself embed a clock timestamp.

Producing command:

```sh
timeout 30 sha256sum /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx
```

Exit **0**, full stdout:

```text
9f41e2d43ca085f1200cd52f1856fa3e821a05942a90d8084122a9ad9ef903a1  /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx
```

The frozen manifest at line 3 requires SHA256 **2e9105ad948131962cbe20502e406d571a22d11c2f9d62ec8c8b88798172890d** and size **332008** bytes.

Additional producing command, launched at **2026-10-23T02:43:56+00:00**:

```sh
timeout 30 stat '--printf=%n size=%s mode=%a mtime=%y ctime=%z\n' /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx
```

Exit **0**, full stdout:

```text
/fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx size=332000 mode=444 mtime=2026-10-22 23:42:35.490935545 -0300 ctime=2026-10-22 23:42:35.491750546 -0300
```

**Inference:** input restoration, rather than a counter or control change, was the smallest prerequisite repair. The read counter checks all carrier identities before its REA loop; therefore the first exit provided no live-format result and no envelope-gate result. Attribution of the shared-file change is **unknown**. **This seat was not the writer: it never altered any shared carrier.** The blocker and digest mismatch were sent only to agent://KaidokuR30. Shared carriers and lane content other than this report were left untouched by this seat.

## Restored-input rerun — complete output and decisive result

L1 reported restoring the four altered carriers from verified wheel members and making all 16 carriers immutable, then explicitly instructed this rerun. The immutable flags were not independently checked by this seat. The rerun passed the counter's carrier-identity validation, as evidenced by reaching all 16 per-carrier results rather than a PIN exit.

Same unchanged clone, working directory, unset Git variables and TMPDIR as above. Exact command:

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/clone/tools/round-30/c1-rust-positive.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/clone --rev main
```

UTC start: **2026-10-23T02:45:41+00:00**. UTC end: **2026-10-23T02:45:52+00:00**. Counter exit **1**.

Full counter stdout:

```text
elf-x86_64-uv	P1-fail	committed envelope absent or not added after the freeze
elf-x86_64-uvx	P1-fail	committed envelope absent or not added after the freeze
elf-aarch64-uv	P1-fail	committed envelope absent or not added after the freeze
elf-aarch64-uvx	P1-fail	committed envelope absent or not added after the freeze
elf-riscv64-uv	P1-fail	committed envelope absent or not added after the freeze
elf-riscv64-uvx	P1-fail	committed envelope absent or not added after the freeze
pe-x86_64-uv	P1-fail	committed envelope absent or not added after the freeze
pe-x86_64-uvx	P1-fail	committed envelope absent or not added after the freeze
pe-x86_64-uvw	P1-fail	committed envelope absent or not added after the freeze
pe-arm64-uv	P1-fail	committed envelope absent or not added after the freeze
pe-arm64-uvx	P1-fail	committed envelope absent or not added after the freeze
pe-arm64-uvw	P1-fail	committed envelope absent or not added after the freeze
macho-x86_64-uv	P1-fail	committed envelope absent or not added after the freeze
macho-x86_64-uvx	P1-fail	committed envelope absent or not added after the freeze
macho-arm64-uv	P1-fail	committed envelope absent or not added after the freeze
macho-arm64-uvx	P1-fail	committed envelope absent or not added after the freeze
carriers=16 pass=0 target=16 entry_ok=0 (entry absent at rev) province_ok=0 (no PROVINCE line names inspect-rust-binary with the entry)
```

Full counter stderr: **empty**.

**Observation:** this control did not meet the target; it contributed no P1-pass carrier. No predicate clause let it through.

**Inference from the counter's control flow:** each emitted committed-envelope failure is reached only after the live envelope passes the live half of P1. Thus even 16 live-positive results did not substitute for the missing committed records. This is the strongest tested attempted bypass here, and it failed. The missing entry also prevents the SOURCES-row gate from being reached separately; this run does not isolate that subgate.

CONTROL CtlC1DoNothing met_target=no

## Artifacts

All artifacts below are outside the lane. The clone is identified by its Git commit above. The rerun-generated Node compile-cache directory was removed from the seat's temporary directory after completion; no cache artifact is retained.

| Absolute artifact path | SHA256 |
| --- | --- |
| /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/run-control.py | 3507b550c05230b7e7b058d958bf0ad844c14d4e1a7d82a5181638d4a6bd832c |
| /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/clone-identity.json | f24faec5ac15adceb58ace93ae8defdf540623e7dc95394be7bfa91cc1a393b6 |
| /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/counter.stdout | cfb493f83436e46c5c431a5fd421d2ad26e97be0df0eab13ed745b43708e4278 |
| /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/counter.stderr | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/counter-receipt.json | e14693402e45dd788371269c4ea85406da9fcbb2d24bfd08d5763e1c7f6058ed |
| /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/pin-blocker.json | c5e8f54af722910c6ea633dc852b5e61d962f8dd7f7230b14ecae593ccd2420d |
| /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/rerun-counter.stdout | afa4cc794aad76161a1570f46fde93e024585c61a98b441dbf216124bceba98b |
| /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/rerun-counter.stderr | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/rerun-counter-receipt.json | fe6fec397238986a62fa47c67c137994757ea64e7ee562bb6ed36704d77a0ba9 |

## Opened sources

Access date for every source: **2026-10-23**. Only local reads; no web access, browser, bot challenge or access-control bypass.

| URL | SHA256 of source bytes | Located quote (≤25 words) |
| --- | --- | --- |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json | 65d94d3fbdf7469f8e100c87c96b1eaa6b93382e20521b0606be54b3db1e989a | line 73: `Any other outcome is an honest stop for that claim.` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py | e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a | line 187: `committed envelope absent or not added after the freeze` |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1DoNothing/clone/corpus/evidence/round-30/c1/carriers.tsv | c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b | line 3: `uv-0.13.0.data/scripts/uvx` |
| file:///home/vgpnk/.agents/skills/godspeed/SKILL.md | 1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a | line 12: `Name the axes.` |
| file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md | 056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692 | line 19: `The REA MCP server is not registered on this host, by design.` |
| file:///home/vgpnk/.omp/agent/RULES.md | beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed | line 14: `Record every install or update` |

Tool installations/updates: **none explicitly performed by this seat**. The assigned counter invoked pinned REA 6.5.0 through npx during the rerun. No build, lint, formatter, selftest, C2 counter, direct REA command or unrelated runtime was invoked.
