# MutC2Judge — offline C2 decision-code mutation probe

## Result and scope

**Observation — attack verdict: fails.** The offline selftest did not detect 15 of 24 selected single-point decision defects: **9 killed, 15 survived, 0 inconclusive**. This is a selftest-coverage finding, not a finding that the frozen live predicate is false.

- Target: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c2-sqlite-refusals.py`.
- Isolated active copy: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/c2-sqlite-refusals.py`.
- Axes: decision-path breadth; strict offline/bounded detector consistency; exact restoration and attributable evidence.
- Fourteen mutants target `judge`, three `committed_check`, four `skill_ok`, and three `strip_meta`. Each changes exactly one physical source line at one decision point; the selftest is unchanged. Original and mutant sources were parsed with Python AST before execution.
- Observation window: `2026-10-23T04:12:50.557100+00:00` through `2026-10-23T04:13:59.803194+00:00`.
- Only the requested offline detector ran: 24 pristine, 24 mutated, and 24 restored runs, 72 total. No measure/build mode, REA, npx, carrier/mutant access, Git/JJ writes, installs, or updates. All spawned detector processes completed synchronously; none was left running. The frozen target line was not evaluated.

## Expected detector and producing command D1

Expected detector: the unmodified copy’s `--selftest`. A reported selftest failure with exit 1 kills a mutant only when its pristine and restored runs pass. Exit 0 is survival, not a contract change. Baseline/restoration failure or a crash/timeout would be inconclusive.

Working directory: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge`. Every case below was produced by this exact command, unchanged across its three phases:

```sh
env TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/tmp timeout --kill-after=5s 30s python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/c2-sqlite-refusals.py --selftest
```

The command is bounded to 30 seconds with a five-second kill grace; the caller also used a 40-second subprocess bound. All 72 runs had empty stderr. All 48 pristine/restored runs exited 0 and ended with the exact line `selftest cases=12 failures=0`.

### Full initial pristine stdout (D1, exit 0)

UTC: `2026-10-23T04:12:50.557100+00:00` through `2026-10-23T04:12:50.632502+00:00`.

```text
ok	refusal exact	refused invalid_request invalid_value
ok	refusal wrong exit	exit 0 != 1
ok	refusal wrong code	code 'x' != 'invalid_request'
ok	refusal wrong message	issues [{"path": ["path"], "reason": "invalid_value", "message": "gone: /q"}] != [{"path": ["path"], "reason": "invalid_value", "message": "gone: /p/db"}]
ok	refusal wrong reason	issues [{"path": ["path"], "reason": "invalid_format", "message": "gone: /p/db"}] != [{"path": ["path"], "reason": "invalid_value", "message": "gone: /p/db"}]
ok	refusal extra issue	issues [{"path": ["path"], "reason": "invalid_value", "message": "gone: /p/db"}, {"path": ["path"], "reason": "invalid_value", "message": "gone: /p/db"}] != [{"path": ["path"], "reason": "invalid_value", "message": "gone: /p/db"}]
ok	refusal but ok	envelope ok, refusal predicted
ok	no envelope	no JSON envelope (exit 1)
ok	accept but refused	accept predicted, exit 1 ok False
ok	meta ignored
ok	data compared
ok	error compared
selftest cases=12 failures=0
```

## Mutant table — observed D1 results

All original line numbers refer to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c2-sqlite-refusals.py`. Every row has pristine/restored exits **0/0**. The summary column is an exact stdout line. Complete stdout, stderr, UTC start/end, commands, and before/after hashes for all phases are preserved in the receipt artifacts below.

| Mutant | Function:line | Single-point defect | Verdict | Mutated exit | Exact stdout summary | Mutated UTC start |
|---|---|---|---|---:|---|---|
| M01 | judge:165 | Compare expected issue as a subset, admitting extra issues. | **killed** | 1 | `selftest cases=12 failures=1` | `2026-10-23T04:13:26.102860+00:00` |
| M02 | judge:163 | Copy the live reason into the expectation, ignoring the frozen reason. | **killed** | 1 | `selftest cases=12 failures=1` | `2026-10-23T04:13:57.110837+00:00` |
| M03 | judge:155 | Omit the refusal exit-code check. | **killed** | 1 | `selftest cases=12 failures=1` | `2026-10-23T04:13:57.217217+00:00` |
| M04 | judge:160 | Omit the refusal error-code check. | **killed** | 1 | `selftest cases=12 failures=1` | `2026-10-23T04:13:57.334168+00:00` |
| M05 | judge:164 | Copy the live message into the expectation, ignoring the frozen message. | **killed** | 1 | `selftest cases=12 failures=1` | `2026-10-23T04:13:57.446596+00:00` |
| M06 | judge:164 | Skip request-path substitution in the expected message. | **killed** | 1 | `selftest cases=12 failures=1` | `2026-10-23T04:13:57.555880+00:00` |
| M07 | judge:157 | Check only presence of ok, allowing ok=true refusals with an exact error. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:57.666720+00:00` |
| M08 | judge:163 | Copy the live issue path into the expectation, ignoring the frozen path. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:57.772035+00:00` |
| M09 | judge:168 | Ignore nonzero exit status for acceptance envelopes. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:57.874827+00:00` |
| M10 | judge:171 | Omit the accepted operation identity check. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:57.983747+00:00` |
| M11 | judge:173 | Omit the accepted subject SHA-256 check. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:58.093267+00:00` |
| M12 | judge:195 | Omit the database-report comparison against the independent oracle. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:58.207795+00:00` |
| M13 | judge:178 | Omit the selected table, row-limit and returned-row checks. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:58.325558+00:00` |
| M14 | judge:188 | Accept row values not present in the independent Album oracle. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:58.464455+00:00` |
| M15 | committed_check:244 | Compare committed/live error.code only instead of full envelopes except meta. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:58.585344+00:00` |
| M16 | committed_check:238 | Omit the post-freeze first-added requirement. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:58.709569+00:00` |
| M17 | committed_check:246 | Omit the requirement that the entry names the request. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:58.831756+00:00` |
| M18 | skill_ok:268 | Do not require the predicted code in each SKILL table row. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:58.951195+00:00` |
| M19 | skill_ok:268 | Do not require the predicted message prefix in each SKILL table row. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:59.068336+00:00` |
| M20 | skill_ok:263 | Accept a prose line instead of a decision-table row. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:59.193502+00:00` |
| M21 | skill_ok:271 | Do not require SKILL to link the knowledge entry. | **survived** | 0 | `selftest cases=12 failures=0` | `2026-10-23T04:13:59.319324+00:00` |
| M22 | strip_meta:146 | Strip error along with meta during envelope comparison. | **killed** | 1 | `selftest cases=12 failures=1` | `2026-10-23T04:13:59.433943+00:00` |
| M23 | strip_meta:146 | Strip data along with meta during envelope comparison. | **killed** | 1 | `selftest cases=12 failures=1` | `2026-10-23T04:13:59.566728+00:00` |
| M24 | strip_meta:146 | Keep meta, comparing volatile timing fields. | **killed** | 1 | `selftest cases=12 failures=1` | `2026-10-23T04:13:59.713135+00:00` |

### Exact failing output excerpts for killed mutants

Each excerpt is from D1 at the UTC shown in the table; each corresponding mutant exited 1 with `selftest cases=12 failures=1`, not an exception or timeout.

**M01 — observation:**

```text
FAIL	refusal extra issue	refused invalid_request invalid_value
selftest cases=12 failures=1
```

**M02 — observation:**

```text
FAIL	refusal wrong reason	refused invalid_request invalid_value
selftest cases=12 failures=1
```

**M03 — observation:**

```text
FAIL	refusal wrong exit	refused invalid_request invalid_value
selftest cases=12 failures=1
```

**M04 — observation:**

```text
FAIL	refusal wrong code	refused invalid_request invalid_value
selftest cases=12 failures=1
```

**M05 — observation:**

```text
FAIL	refusal wrong message	refused invalid_request invalid_value
selftest cases=12 failures=1
```

**M06 — observation:**

```text
FAIL	refusal exact	issues [{"path": ["path"], "reason": "invalid_value", "message": "gone: /p/db"}] != [{"path": ["path"], "reason": "invalid_value", "message": "gone: {P}"}]
selftest cases=12 failures=1
```

**M22 — observation:**

```text
FAIL	error compared
selftest cases=12 failures=1
```

**M23 — observation:**

```text
FAIL	data compared
selftest cases=12 failures=1
```

**M24 — observation:**

```text
FAIL	meta ignored
selftest cases=12 failures=1
```

## Surviving mutants: missing selftest cases

**Observation:** M07–M21 each exited 0 with the exact line `selftest cases=12 failures=0`, at the UTCs in the table. Their pristine/restored runs also passed.

**Inference:** the following discriminating cases are missing from the existing selftest; these are coverage recommendations only, not implemented tests or relaxed contracts.

| Survivor | Missing discriminating selftest case |
|---|---|
| M07 | Exact refusal error/code/exit payload with ok=true (or another non-False value). |
| M08 | Otherwise exact refusal with a different issue.path. |
| M09 | A complete valid acceptance envelope run with a nonzero exit status. |
| M10 | A complete valid acceptance envelope differing only in data.operation. |
| M11 | A complete valid acceptance envelope differing only in subject.digest.sha256. |
| M12 | A complete non-row acceptance envelope with a report differing from the oracle. |
| M13 | Valid q-ok-rows envelope with table, row_limit, or returned_rows changed one at a time. |
| M14 | Valid q-ok-rows envelope containing one syntactically valid row absent from the oracle. |
| M15 | Call committed_check with post-freeze JSON whose error.code agrees but an issue, data, or ok differs. |
| M16 | Call committed_check with equal/earlier/missing first-added time or missing freeze time. |
| M17 | Call committed_check with otherwise-valid committed/live envelopes but no request id in the entry. |
| M18 | Call skill_ok with a refusal row naming the correct request/message but the wrong code. |
| M19 | Call skill_ok with a refusal row naming the correct request/code but a wrong message prefix. |
| M20 | Call skill_ok with request/code/message only in prose while verb and entry references are present. |
| M21 | Call skill_ok with otherwise-valid table rows and verb but the entry path omitted. |

**Source observation:** the existing `selftest` calls `judge` and `strip_meta`, but does not call `committed_check` or `skill_ok`. Its sole acceptance-labelled case is an already-refused envelope, rejected before acceptance-content checks. Its `refusal but ok` case also lacks the expected error, so another guard can reject it even if the `ok` guard is defective.

**Observation:** the M15 full-envelope-to-error-code-only regression survived, while M22 (stripping `error` directly) was killed. **Inference:** testing `strip_meta` in isolation does not protect `committed_check`’s use of the full-envelope comparison, the repaired M30-3 boundary. No live-envelope or claim-data conclusion was drawn.

## Restoration evidence

**Observation:** lane source SHA-256 before and after, initial copied bytes, and final active-copy bytes all equal:

```text
d23948959835038f4622261b551616863af1e47f3c66a558b8f3b5a232e28223
```

Every case records that same pristine hash before mutation and restored hash after restoration; each mutant’s distinct hash is in the table of artifacts and machine receipts. The active copy was restored in a `finally` block after every mutant, even when the selftest failed, and the same D1 command then passed on restored bytes. The archived mutant sources are intentionally retained as evidence, not left as the active copy.

**Observation:** no lane file was edited except this scoped report. No tooling was installed or updated.

## Artifacts and SHA-256

The JSON receipt and raw log contain **full** stdout and stderr for every pristine/mutated/restored run, exact producing commands, UTC start/end, exit codes, and both hashes. Mutation specifications preserve each old/new line. The TSV manifest lists all other artifacts; its own hash is supplied here. The scratch temporary directory contains no retained evidence files.

| Absolute artifact path | SHA-256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/pristine.py` | `d23948959835038f4622261b551616863af1e47f3c66a558b8f3b5a232e28223` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/c2-sqlite-refusals.py` | `d23948959835038f4622261b551616863af1e47f3c66a558b8f3b5a232e28223` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutations.json` | `cc3f382968e66c9c3ce6ac0d4415bb244fab8c819f82bdf3415070edd9c75012` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/detector-runs.json` | `f1840d34178339373de4d7856a12aecd21bd53127ab4b1ebf08c0217aedca088` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/detector-stdout.log` | `ed4dfdd52e5123a7ca6dd0caadd80f99e39a11922a5a7f2728eda381f6754d8f` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutant-results.tsv` | `10d69ddc4f844bc51baf49755012fae97b518e640fce9aee279f179d7bd26f10` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/source-provenance.json` | `58b918a6bea6be57cc194e895020a0228198836c6157566c56389cfd36e8b948` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M01.py` | `a8d75a5f72426c263dd9a18fd4c37881fcc5f98da453875f2e949f70d9f9fbfc` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M02.py` | `e1419edbf71550357a0922282f41329bf020c4faa5f5b244197fc62843403f36` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M03.py` | `9a1b6ee7ee47b5f9149f6fe1e676103ae6a189625af333cc0b1ffdc258b2dc54` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M04.py` | `9993523279ec7df4c8e4c0621664e4cfdabc588614b70210d464c2ba0f0ea6ed` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M05.py` | `45659c28a8fb1947a373d5f261211fe0ed81ab357c93878d49cdd37c5c80f9aa` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M06.py` | `dfad50656b07f1a141363ba4a8c3aa336a85956548ad789a0664e7a48b7510d3` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M07.py` | `d451af71e5f87c1adc65ec4a92ed7a358957f89be6572d0d0f90b9e07ab49e9e` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M08.py` | `114a05b1ef91f47a86f0cf3a24ff8df147fe33284e90a1fea2d45fc6289efd21` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M09.py` | `9c012186569f980b652e88187df007285d015e1956c4b8195d7e02bf112cdd00` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M10.py` | `2e6df306d9e55a6f03a6b39686b174da6d123bd1f3123ee375e0e909c9311f8f` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M11.py` | `93be9d63d7612c644425803366017167c01b077bc2f4726709860a1e0c078062` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M12.py` | `5a523704aace373a1893e11564dbedab2d230dbec71731282fa4cac9d516a0cc` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M13.py` | `f6c62805b3d38182d74bf0bfbbe78bedf0e6e33241c8d505ca0e9dce60bbb9fb` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M14.py` | `53acc836c49547f2c0ce78e673f5603ce3af558f279beb7896d359143302d6e3` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M15.py` | `f2ad0b80e07f323ee39419cd18c610d1039a6a0cdfd027e34f5099c819b358c3` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M16.py` | `45fac104a58fe6905434bdc415657c0e7310634e1ce131d21005cfb43a23a2f2` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M17.py` | `f732631cc13a7966fb462f2c4e3a8f9a3d5f282f25382d801bb7abe0ea58ff06` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M18.py` | `8f7718503ed111db7d970b39a0ec2a7900f8ab1241a8ec03ad196dd158a04b32` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M19.py` | `9d573288e10150eddf53c135e2e4ba8130b9539d2889d4ebc76b6c295c40a914` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M20.py` | `5943ef344eacfae49a5b50f67976b96af29efa07871abb3a131b7ac070398eee` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M21.py` | `0570e3dcc47e52690bed35a37cd46929723ba040f3bdaf4a7bccfd66bf0087e1` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M22.py` | `ef2a549cf3493908c97dd5c4e20c5092b3212ba884a808fcb03ee48062d6bc10` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M23.py` | `a83c366a2c5bd6ff3655057ccb89f90a3b14f6917d827cb75a23c805132573d5` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/mutants/M24.py` | `f8bce14442358e734adf5ed94cf74c011ae7258f7f3c01d80b0c4761b75c5054` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutC2Judge/artifact-sha256.tsv` | `0f99e2c5be75443b8b8bca9c5efb26f8727e3624a8d0249bc3fe937f286ddeae` |

## Opened local source provenance

No external source was opened. Access date for every local source below: **2026-10-23**. Quotes are located and at most 25 contiguous words.

| Source URL | SHA-256 of source bytes | Located quote |
|---|---|---|
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c2-sqlite-refusals.py` | `d23948959835038f4622261b551616863af1e47f3c66a558b8f3b5a232e28223` | Line 245: committed envelope differs from the live envelope (full comparison) |
| `file:///home/vgpnk/.omp/agent/RULES.md` | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | Line 8: Official sources |
| `file:///home/vgpnk/.agents/skills/godspeed/SKILL.md` | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | Line 12: 1. **Name the axes.** |

## Tool acquisition note

**Observation:** the raw-reader result omitted the original file’s final newline (18,181 returned UTF-8 bytes versus 18,182 file bytes). This was reported to `xd://report_issue`; copying used the complete file bytes instead. The initial copy hash matched the lane source before any probe. One rejected tool-call argument form also performed no edit; the source was re-read before applying a valid hashline edit. Neither acquisition issue was counted as a mutant result.
