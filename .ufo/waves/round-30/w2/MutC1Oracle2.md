# MutC1Oracle2 — C1 real-envelope mutation probe

## Scope and verdict

- **Attack:** whether `judge()` catches loss/corruption in the committed C1 package multisets, and uv/uvx record deduplication.
- **Axes:** detector correctness; real-data provenance; scratch isolation and exact restoration.
- **Observation — holds for the assigned damages:** all four requested damage types were killed on all 16 real carriers (**64/64**). No damaged envelope passed. Additional package-name deduplication and whole-envelope uv→uvx replay were also killed (**23/23**). Total **87 killed, 0 survived, 0 inconclusive**.
- **Observation:** pristine baselines passed **16/16**; each of the 87 probes independently repeated pristine → damaged → byte-exact restored detection.
- **Inference:** this specifically challenges the package tuple comparison, not merely package counts: dropping one edge, deleting a root flag and swapping versions all failed with unchanged package counts.
- **Unknown / intentionally unrun:** the live REA CLI, full C1 `measure()`, `committed_check()`, aggregate entry/province checks, and C2. This report does not re-judge or claim either frozen aggregate target passed.

## Producing command and timing

Outer command actually run:

```text
timeout 360 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/run-probe.py
```

The runner's exact bounded behavioral command:

```text
timeout 300 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/probe.py
```

**Observation:** child exit **0**, UTC **2026-10-23T03:15:28.604136+00:00** through **2026-10-23T03:15:32.687408+00:00**. Outer command also exited 0. Child stderr was empty. A harness exit 0 means all expected rejections occurred; each damaged `judge()` call returned `P1-fail`, not a separate process exit.

Full counter-function output: `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/probe.stdout`. Command/exit/UTC receipt: `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/execution.json`.

Exact output excerpt from that command:

```text
SUMMARY damage=drop_build_packages cases=16 killed=16 survived=0 inconclusive=0
SUMMARY damage=drop_one_edge cases=16 killed=16 survived=0 inconclusive=0
SUMMARY damage=drop_root_flag cases=16 killed=16 survived=0 inconclusive=0
SUMMARY damage=swap_two_versions cases=16 killed=16 survived=0 inconclusive=0
SUMMARY damage=deduplicate_package_names cases=16 killed=16 survived=0 inconclusive=0
SUMMARY damage=replay_uv_envelope_for_uvx cases=7 killed=7 survived=0 inconclusive=0
RESTORATION baseline_pass=16/16 exact_restorations=87/87 inputs_unchanged=1 nondamage_controls_pass=7/7
END utc=2026-10-23T03:15:32.667341+00:00
```

## Inputs and expected detector

**Observation:** the harness copied both instruments, all 16 envelopes, manifest, recorded runs and frozen claims from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Each repository input was compared byte-for-byte with read-only `git show` at measured revision `92b1dd2ddc119fda89a611ba515bdf6cfe906f76` before use. Every Git subprocess removed `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` from its environment and used a 30-second `timeout`; no Git writes occurred.

**Observation:** all 16 carrier byte copies matched their manifest SHA-256 and size before the oracle read them. The oracle received only absolute paths under `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/`, never an original carrier path. No carrier was executed and no input-writing binary utility was used.

Expected detector, unchanged across pristine/damaged/restored phases:

```text
section, document = oracle.read_file(scratch_carrier)
tuples = oracle.normalize(document)
counter.judge(json.loads(active_envelope_bytes), frozen_carrier_sha256,
              section, tuples, recorded_run_exit)
```

All recorded REA exits supplied to `judge()` were 0. The oracle and counter files remained unmodified:

- `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/c1-rust-positive.py`: `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a`.
- `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/rust_dep_oracle.py`: `f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d`.

## Damage → verdict

All rows below are **observations** from the bounded command above.

| Damage | Cases | Killed | Survived | Inconclusive |
|---|---:|---:|---:|---:|
| drop_build_packages | 16 | 16 | 0 | 0 |
| drop_one_edge | 16 | 16 | 0 | 0 |
| drop_root_flag | 16 | 16 | 0 | 0 |
| swap_two_versions | 16 | 16 | 0 | 0 |
| deduplicate_package_names | 16 | 16 | 0 | 0 |
| replay_uv_envelope_for_uvx | 7 | 7 | 0 | 0 |

Mutation definitions:

1. **Drop every `kind=build` package:** removed 36 packages per ELF/Mach-O image and 38 per PE image. Remaining dependency indices were reindexed and references to removed packages removed, avoiding an accidental malformed-index rejection. The comparator rejected the changed package multiset.
2. **Drop one edge:** removed the first dependency edge, `aes 0.8.4` → `cfg-if 1.0.4` in the representative ELF x86_64 envelope. Remaining package count was unchanged.
3. **Drop the root flag:** removed the root package's `root: true` key, without deleting the package. Representative root: index 463, `uv 0.13.0`.
4. **Swap two versions:** exchanged `adler2 2.0.1` and `aes 0.8.4` version values, preserving both package names and the total package count.
5. **Deduplicate package names:** retained the first package of each name and redirected dependency indices to the retained row. Representative count: 584 → 562. This tests an erroneous name-keyed map, not legitimate reuse of an identical document.
6. **Replay uv's entire envelope for uvx:** on each of the seven uv/uvx pairs, replaced uvx's envelope with uv's. All seven failed the subject SHA-256 check, despite equal package multisets.

Every real envelope had one `auditable_metadata` instance. All package-damage cases preserved one distinct metadata object and changed its normalized tuples; none was counted as killed merely because two metadata copies disagreed or a mutation was a no-op.

Representative exact output (same command, exit 0, UTC interval above):

```text
CASE elf-x86_64-uvx drop_build_packages pristine=P1-pass mutated=P1-fail restored=P1-pass verdict=killed reason=package multiset differs (rea 548, oracle 584)
CASE elf-x86_64-uvx drop_one_edge pristine=P1-pass mutated=P1-fail restored=P1-pass verdict=killed reason=package multiset differs (rea 584, oracle 584)
CASE elf-x86_64-uvx drop_root_flag pristine=P1-pass mutated=P1-fail restored=P1-pass verdict=killed reason=package multiset differs (rea 584, oracle 584)
CASE elf-x86_64-uvx swap_two_versions pristine=P1-pass mutated=P1-fail restored=P1-pass verdict=killed reason=package multiset differs (rea 584, oracle 584)
CASE elf-x86_64-uvx deduplicate_package_names pristine=P1-pass mutated=P1-fail restored=P1-pass verdict=killed reason=package multiset differs (rea 562, oracle 584)
CASE elf-x86_64-uvx replay_uv_envelope_for_uvx pristine=P1-pass mutated=P1-fail restored=P1-pass verdict=killed reason=subject sha256 '3e801df892439f5cde65d8b51ea69b69abff199ef37cc3cae4481be15d592df0'
```

## uv/uvx qualification

**Observation:** all seven uv/uvx pairs had identical package lists as well as identical package multisets. Copying only uv's package list into its matching uvx envelope, while preserving uvx's subject digest and section range, passed **7/7**. Exact representative output:

```text
CONTROL elf-x86_64-uvx reuse_identical_uv_packages_only same_multiset=1 same_list=1 verdict=P1-pass reason=packages=584 edges=3041
```

**Inference / coverage boundary:** package comparison cannot distinguish reparsing from reuse of byte-value-identical package metadata. This is not a surviving semantic damage: the control changed no package-list value, and the frozen claim already discloses repeated uv/uvx dependency documents. Whole-envelope replay is caught by the subject digest. Do not infer 16 independent dependency graphs or proof of separate REA executions from `judge()` equality alone. This probe found **no passing damage among the specified four mutations** and does not amend the frozen predicate.

## Exact restoration evidence

**Observation:** every active scratch envelope was restored in a `finally` block and the same detector then returned `P1-pass`; **87/87** exact restorations. All **37** source/copied-input pairs had identical before/after SHA-256 values. The 16 active-envelope final hashes equal their pristine-envelope hashes. Deliberate damaged snapshots remain only under the seat's scratch directory as evidence; no originals were changed.

Per-case before/mutated/restored hashes, actual verdicts and UTC timestamps are in `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/results.json`; source/copied-input before/after hashes are in `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/input-hashes.tsv`.

Representative `elf-x86_64-uvx` exact bytes:

| Damage | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 |
|---|---|---|---|
| drop_build_packages | `17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa` | `8071ada596c4b3bcf753e5dc6d64397eecfe7974068b10918f27fdf410d039bb` | `17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa` |
| drop_one_edge | `17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa` | `2a9cf1e0c64813e3a38c7e03cd72abb4136d12d8b0d916413f07d01cb6c87ac9` | `17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa` |
| drop_root_flag | `17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa` | `5013f6d6ba0ab89958e07a3d355d68178d242f23fff0d48a471080f12ed2422e` | `17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa` |
| swap_two_versions | `17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa` | `8086e6d7c215cc6c90d3445ae316d7ac654aab19818aaf147d6903ec8f8be8b0` | `17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa` |
| deduplicate_package_names | `17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa` | `8c1f272679d7a4e393358885e103cc4ff5c94ce0a3530657a846e95fb547e25a` | `17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa` |
| replay_uv_envelope_for_uvx | `17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa` | `d7fdaeb6c28aa7da60a138cb6ffc4549d762364af60c887bc4aa131956b26095` | `17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa` |

**Observation:** no REA invocation, network request, tool installation/update, subagent dispatch, lane index/state mutation, carrier execution, or build/lint/format suite occurred. The runner bounded its child process and cleaned its process group before returning. This scoped report is the only lane write; shared files, callers, tests and docs are intentionally unchanged for this investigation.

## Source register

No external primary source was fetched. `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/sources.tsv` records each of the 37 local source/input URLs (`file://`), access date **2026-10-23**, full-byte SHA-256, and a located ASCII quote of at most 25 contiguous words with its 1-based line and byte offset. For binary carriers, the located quote is `.dep-v0` and the line is the raw-byte newline count; the byte offset is the useful locator.

## Complete scratch artifact inventory

Each line gives SHA-256 followed by its absolute artifact path. This lists all 148 files produced/copied by the run, plus the inventory itself. Paths are under this seat only.

```text
ef46bd97a0e44d9d62f85622c72e6ebb686bef856f831e3ee92c943fc3af8911  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/elf-aarch64-uv.json
c946f4628a25b86eb4b833608333094e613930e21158ff2337ddca0b6fc28882  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/elf-aarch64-uvx.json
1a61dbed32abdc095e67346267f72d8b663fbd0d57bbaf3ce8e1f84bb0ebdb5f  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/elf-riscv64-uv.json
c1e49365d4de0782c9d65399f287c5b59259edc9d818412f2bb36ef5b095098d  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/elf-riscv64-uvx.json
d7fdaeb6c28aa7da60a138cb6ffc4549d762364af60c887bc4aa131956b26095  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/elf-x86_64-uv.json
17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/elf-x86_64-uvx.json
f70877a4444fa5146d6e71c02a0ff15a09a1f54af5dc3e614c1f453ccc1d0597  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/macho-arm64-uv.json
be90ed53c803b321ee6e1fb426bb63b082e44f63c0d74a5e3c255fbbf10e2b0f  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/macho-arm64-uvx.json
79f0113e220dcb89a592843795038ab655c114d1ab1ca9fa2e4cca2b75fad37b  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/macho-x86_64-uv.json
c5475f1f755128f63d6e6496e306b3170d26da3da6ff74093a921f207a47371f  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/macho-x86_64-uvx.json
5d7efbde26d1cde8ba71453f352a2776219a7168d41609142ba6ddb571e59e97  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/pe-arm64-uv.json
fdaeaf9c89bf6e4b13cc60acdb0dcdbef38e8a0e28aacf1b195e2181ab8ff552  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/pe-arm64-uvw.json
6b38ff1a4ee6dc832abbb5fdd9c5f5b204a6015e52740e60276f6ef1ae78ce20  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/pe-arm64-uvx.json
c0e1aa9114e611f77dfa0f84042756c23da574cdaccb5a51b5f3658c95563c03  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/pe-x86_64-uv.json
31b5ef7128c2d8e916da0ba2703852872b3923c15fc31594e485d551843006d9  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/pe-x86_64-uvw.json
1d557589b4771431fdcc4eed481d2bbe41c41667ead0130c2ad45c46175bb0e5  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/active-envelopes/pe-x86_64-uvx.json
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/c1-rust-positive.py
a72b2853c84ac54d63147f32e4ace266a1d9e2017e53e5486fe3b9494145eff4  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/elf-aarch64-uv
e3ef59b327cdf02e5f6c0cf3c3e5a6249d97bb9d67d67538776783364b21d0f9  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/elf-aarch64-uvx
63cc77a4904a9e6ba424959f81f7d6648ddabfb071f713fe391be3bc2505efdc  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/elf-riscv64-uv
20ee113ad020d7ff6dc3e9afc62985d4684f0dee566d92532e8884f92ea82b9d  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/elf-riscv64-uvx
3e801df892439f5cde65d8b51ea69b69abff199ef37cc3cae4481be15d592df0  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/elf-x86_64-uv
2e9105ad948131962cbe20502e406d571a22d11c2f9d62ec8c8b88798172890d  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/elf-x86_64-uvx
4cd60b63cf3221572ccb0e171cfc3404cede505ce8f701b6520439476bc1d240  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/macho-arm64-uv
360f023f4f5354b35e5240d081b7c40fc6b489692e7b178cad697380d753223b  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/macho-arm64-uvx
f31d4fdce12aad810a045b24aa322642fb8bfbaa441b24a90cbad0cdc7a0f3ca  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/macho-x86_64-uv
f25305942412cd98249f7da7f4f88acc5869e3150de09c46f7c110c7264f4058  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/macho-x86_64-uvx
885a370550b1596b2ce072c004afa94ad51196d7f2801b710d1a85f63cce4485  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/pe-arm64-uv
af15b1a1c01cb9924c2a33d3b8eddcba2b8b8112da8489a9a16eacf6e4c2cb52  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/pe-arm64-uvw
15153057351dc6a3dea507c2481df0a472ffe06b8b1a17a6b00518f1a870c2d7  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/pe-arm64-uvx
2bfbe53d3cc95799e98fa08323b04844fc01d4f8c87dd5c00089e43f6554f162  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/pe-x86_64-uv
a6ea65950009f259a08d95410254326f913dbf9f7f966e743c4d36d69bce9d6a  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/pe-x86_64-uvw
3489d6931caef4947b338a1d90b3f450915b56ec190e56c13ae33e55da4acc89  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers/pe-x86_64-uvx
c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/carriers.tsv
65d94d3fbdf7469f8e100c87c96b1eaa6b93382e20521b0606be54b3db1e989a  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/claims.json
627930aa4431a580ff98320b81219b8231bfb3e84f952a605394ebcc0108d891  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/execution.json
24e5ae6e376d86fe9325ce50601c6ed6d36a06783e04a15e35daa831d7210d2a  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/input-hashes.tsv
3748875d6085825bd87b7d4120383ab862d41ed82f61a859b932120d7224dca3  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/elf-aarch64-uv.json
bcbf6cc4e3bd4e77ad85cf88be93f10cb6164992d112c08f5ff253c6c10117ff  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/elf-aarch64-uvx.json
e1a52a21be04529eb4c46eba0e5729c414934a1be7780acab2bfa768e14ed787  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/elf-riscv64-uv.json
5befb0bef099db4c6cbd9b5ff860fe71695560ba435f80b686ae0b4a5e492ccb  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/elf-riscv64-uvx.json
a8c843d65a8064a8ecda7c3cc1383be0154fb97dd5e3058c78b518f93160bd1a  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/elf-x86_64-uv.json
8c1f272679d7a4e393358885e103cc4ff5c94ce0a3530657a846e95fb547e25a  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/elf-x86_64-uvx.json
9ea2d64cc0945de4cc43448a5c0c8d339fcc62af1c960fa140e62811ad689e1f  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/macho-arm64-uv.json
fb824f922c2c619b13f54bfbeb1d2fb085f533a4fe4fa7e85a2a0f0f6cfd234c  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/macho-arm64-uvx.json
6b201a88001e35095b75efa791f99ac4f0024fa4b0182492e28cf8a1df20c4b4  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/macho-x86_64-uv.json
d6ea4babf414ced3f3e353fe33f293e991107355dae3841bb1a64b2751277038  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/macho-x86_64-uvx.json
efeeace27a79de47f332a38a8e5c4d53a3678cf982bf2729e228d5206985e7ce  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/pe-arm64-uv.json
6e7016879aa25693d38a6f70d30598e7a5c270805b9aa4db93def715216501a6  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/pe-arm64-uvw.json
9386893641b1b8f466e10634ce1eccc1b7e887fb4c2ff3a645166129213a361f  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/pe-arm64-uvx.json
2b0a3f6534337294cec12ce9f58decdf6008d19e1954755daee8bfb2303a5a2c  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/pe-x86_64-uv.json
0663071ec88decf1bd8476e4f386440d509460356b03b569b55d9b9778148b3b  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/pe-x86_64-uvw.json
779d0ef3384c636a02bf74fb53ef3d3ae17cecbcd6f2485e1de8efbd63787a90  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/deduplicate_package_names/pe-x86_64-uvx.json
c55b26312d64feeadbffe4546646a9370650179f58e8af68d90a687482ca43bc  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/elf-aarch64-uv.json
5be904cb3ccb37860347023a9c633a9e2b10a858812efe6e83b6fdab13387c33  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/elf-aarch64-uvx.json
272608187537558c6058f5e9fd020f36111e99e13a7f1b0cd11531705232afff  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/elf-riscv64-uv.json
0ac55afe70c9329b70873d57fd67fe91490414138ce8abe2346ca9fdc5b44624  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/elf-riscv64-uvx.json
883851fc40aef8cf6d1e89e910d6d0814e8ea82e40d57ed5b6b29170a3afd0ca  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/elf-x86_64-uv.json
8071ada596c4b3bcf753e5dc6d64397eecfe7974068b10918f27fdf410d039bb  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/elf-x86_64-uvx.json
af70fc2003cb3040728adfe6ed54d9cc50c4bae9a3fb7ec0552a804965aaa379  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/macho-arm64-uv.json
5934c23ca5d0482d0e47c764dbac3c6f0634c8c42c0b24f20cfa1d982a748a9e  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/macho-arm64-uvx.json
640c35713af9ece06732ad9a373eb7415893136d3e9441246812b3503cbaa329  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/macho-x86_64-uv.json
66458c545f7e99a18bdc7c87f5495cf62bf8c1ff56208b5813d932ab81c2f547  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/macho-x86_64-uvx.json
a1e9f562bfb430805a94a90a8263c9e27362c54a55b90cc8a62c0c6f0930abfc  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/pe-arm64-uv.json
3b58f1db37bbcd8388e5ef8ddc33c4c3a9e9421d91bda933c38f818d49e3150c  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/pe-arm64-uvw.json
67e8051421c952f045a1ebc8cb239c3f94097a6edb7b904eda3edc13879e0495  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/pe-arm64-uvx.json
5153a063bdd63770b4d858dae8e83beaa4e2886f63966de2de8de42b875a7539  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/pe-x86_64-uv.json
8d7e1d93b078e3c5697f97f83edffc26cdc2e22000d2596cde27177febf28c64  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/pe-x86_64-uvw.json
2b1c7e551d14e30df8b0a29939ac1294fce5e27aa26510ec1a0dfcfc49c73323  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_build_packages/pe-x86_64-uvx.json
fe1ce7c59dc21228418a39d267e15f57613406cee6b5cdaba6dd2006393eac94  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/elf-aarch64-uv.json
5046bfc31819385987ff17f9eae10859b26449b6809c215f09b774eeadcc5206  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/elf-aarch64-uvx.json
a0fab18ffb566d15bd638d4570106054b3cde2733ae1a3b0d5f9cbde7d27664f  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/elf-riscv64-uv.json
405764aa70943b839160d81f10938d5bc5908e75367f7afa22aac1a49e827e70  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/elf-riscv64-uvx.json
f4521edbcbd85623b13037a7ab5119cbf175348ee54157c5b3ba2bcc138bb814  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/elf-x86_64-uv.json
2a9cf1e0c64813e3a38c7e03cd72abb4136d12d8b0d916413f07d01cb6c87ac9  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/elf-x86_64-uvx.json
dadb3b8e8314102efb5b71b11a61e882eefc35eefb7998a4a977a44e442c687a  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/macho-arm64-uv.json
d29a016a2fae0aa177a3d6e85909cc447085f4f8040990e94c4b944854d022dd  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/macho-arm64-uvx.json
91577dc138df7f0259f61e1eef04951d6568752955919928860cff6c11cf2bac  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/macho-x86_64-uv.json
a2fa3a42c6cfc00f835b48010accd1f9b5cb4d087a86d5ab064388413c12a22f  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/macho-x86_64-uvx.json
1d5a878cd7da6f551b28ae61ab55ce35d8a8572302919fa83980451d5000698d  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/pe-arm64-uv.json
e2c4facf8c89aeb1d1d79f88474cad8558bf600b992102d552228cd62ac584e4  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/pe-arm64-uvw.json
e0df488bf06c99c71b9985a6aa3fd82783a4d7f9780637dc12d8766f6c9eaea5  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/pe-arm64-uvx.json
957a8a0160420feb452eb891d177a8a84c2a40dd4d34bde3bc4d24b57b6eba5c  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/pe-x86_64-uv.json
940bdf59bce6dd61392876691a80d70bcd688ad611eb268ecabddc8d92ddb573  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/pe-x86_64-uvw.json
29f85dffc5a5c17a1fce69464ef6fc5cd16545b6ab242fbf487458a9cd43e9e6  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_one_edge/pe-x86_64-uvx.json
4ce9204ed94099b4fbf5b38a74bef1161634e94578b73cefd2bddd27d0557b89  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/elf-aarch64-uv.json
96ff9b9a1e3c140e06f8903290306a50442d2d5628ee25dc86eacf4524032f07  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/elf-aarch64-uvx.json
4cdbe366af3088dd1aaef6552e942f242d62a325da9ffbe1dda80749e37845f2  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/elf-riscv64-uv.json
e7c5684f0f09a7cac68aec9699ccbc5ed07fe52b001db2e86c3d7e770027b13b  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/elf-riscv64-uvx.json
a79dd8629cce33984957fa1854490e22024277b3bdb3b4c6204e5a780e7f724f  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/elf-x86_64-uv.json
5013f6d6ba0ab89958e07a3d355d68178d242f23fff0d48a471080f12ed2422e  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/elf-x86_64-uvx.json
11c34054f9a5033d15dede59603b228b7f391672f5151280f8f1e684e2add94f  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/macho-arm64-uv.json
bbb149c4a78817b89910f8ff442dcb9da0a7e17d4444c8c6606e95ae19f77215  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/macho-arm64-uvx.json
d0380ebbe86fb042e2a5479d953311f05bf8f38413a929d0aef242e506dd3093  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/macho-x86_64-uv.json
2ab5e0200908847a6655914f65dc6cd6e369368468287388be3a627f28472226  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/macho-x86_64-uvx.json
fbf232d4e0e9a164e898865a3be5392d94ceaaf1a6571a79cc3c6e32489915af  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/pe-arm64-uv.json
2e22f542224c46a1dc7aaa30df3e10ba351e17ab6e7172b4fe16b3174a55286e  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/pe-arm64-uvw.json
5d6012a53d2accfff6f7998de10b344f44683ad2bd6852e44fb4bd5c96094eed  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/pe-arm64-uvx.json
b4903b985868ed2b7aece472504be10b62b6e368845a3405842434724059796b  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/pe-x86_64-uv.json
ac32a3a4e6989976c209d06da31dda2434542fe70dbcfe4e0fa848d9b67fd742  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/pe-x86_64-uvw.json
dcc6a1dc6b4a227713280a9f1715d9dac4c1bd55c586e01ab3cf7e257640fec0  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/drop_root_flag/pe-x86_64-uvx.json
ef46bd97a0e44d9d62f85622c72e6ebb686bef856f831e3ee92c943fc3af8911  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/replay_uv_envelope_for_uvx/elf-aarch64-uvx.json
1a61dbed32abdc095e67346267f72d8b663fbd0d57bbaf3ce8e1f84bb0ebdb5f  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/replay_uv_envelope_for_uvx/elf-riscv64-uvx.json
d7fdaeb6c28aa7da60a138cb6ffc4549d762364af60c887bc4aa131956b26095  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/replay_uv_envelope_for_uvx/elf-x86_64-uvx.json
f70877a4444fa5146d6e71c02a0ff15a09a1f54af5dc3e614c1f453ccc1d0597  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/replay_uv_envelope_for_uvx/macho-arm64-uvx.json
79f0113e220dcb89a592843795038ab655c114d1ab1ca9fa2e4cca2b75fad37b  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/replay_uv_envelope_for_uvx/macho-x86_64-uvx.json
5d7efbde26d1cde8ba71453f352a2776219a7168d41609142ba6ddb571e59e97  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/replay_uv_envelope_for_uvx/pe-arm64-uvx.json
c0e1aa9114e611f77dfa0f84042756c23da574cdaccb5a51b5f3658c95563c03  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/replay_uv_envelope_for_uvx/pe-x86_64-uvx.json
f575e7fe0ba3febc1a78dfc489c20f68b0b1270b3607115ccfbc79f99006e2e1  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/elf-aarch64-uv.json
0cedf2e94591e6c74ddfc7cdca356b484e74ee73103a880b720bf9917a14e7dc  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/elf-aarch64-uvx.json
225b85303623980f514f59a0c95ddadf39bebd39d1a7d13433133fa9111ddadd  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/elf-riscv64-uv.json
b83c74d69aa56fa7118591df0cbc39b42eb7dcc26c5d77493841fa98196f0b06  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/elf-riscv64-uvx.json
72d8d8d301d919002f89057c1f7279e277bcc31d538b1db5fac536c012e09756  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/elf-x86_64-uv.json
8086e6d7c215cc6c90d3445ae316d7ac654aab19818aaf147d6903ec8f8be8b0  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/elf-x86_64-uvx.json
60d596265d20159ead4c3ed267eed9b1800c957cd8c4ac557e2f27730afccae8  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/macho-arm64-uv.json
0029cf6bdb1570b17690d9e093f4b3860b03a9d8ff9e0d1cf0dd9b9794b0f02d  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/macho-arm64-uvx.json
299e43e83a270811383bd998985193e8dddb5eaa6f589c665aa2693ba2b01b43  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/macho-x86_64-uv.json
c625b9f0bf6f7927f16c8b1285298b79929f1f88cb2cf7b150a2e3e02c0dd25b  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/macho-x86_64-uvx.json
b0d9e4a50d93b84df16c8e1b8705cf747329033ee6f4a17504160301cf3b5ebf  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/pe-arm64-uv.json
4497366f982805bc9cabe545ac3db37ed38587f02f1417ec8f991464b00a5251  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/pe-arm64-uvw.json
a55a157f89022ece47ee0182c436f5dc2e4260fa16358bc3d0f34726c920e1a9  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/pe-arm64-uvx.json
91b3a1885a1e14c12e66de7d29fc06ef497714cedd3bfbca503929d18f82256a  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/pe-x86_64-uv.json
83a45c4808b4005a5cbb12a3d0788a1cd7d15d8d1437fe5f488d045f5df7d5f0  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/pe-x86_64-uvw.json
8dcc90e58efe2ce665dbb2e7746b89a3f8e33fa0b6f7ff2369c47358a9b2495a  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/mutated-envelopes/swap_two_versions/pe-x86_64-uvx.json
ef46bd97a0e44d9d62f85622c72e6ebb686bef856f831e3ee92c943fc3af8911  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/elf-aarch64-uv.json
c946f4628a25b86eb4b833608333094e613930e21158ff2337ddca0b6fc28882  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/elf-aarch64-uvx.json
1a61dbed32abdc095e67346267f72d8b663fbd0d57bbaf3ce8e1f84bb0ebdb5f  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/elf-riscv64-uv.json
c1e49365d4de0782c9d65399f287c5b59259edc9d818412f2bb36ef5b095098d  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/elf-riscv64-uvx.json
d7fdaeb6c28aa7da60a138cb6ffc4549d762364af60c887bc4aa131956b26095  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/elf-x86_64-uv.json
17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/elf-x86_64-uvx.json
f70877a4444fa5146d6e71c02a0ff15a09a1f54af5dc3e614c1f453ccc1d0597  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/macho-arm64-uv.json
be90ed53c803b321ee6e1fb426bb63b082e44f63c0d74a5e3c255fbbf10e2b0f  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/macho-arm64-uvx.json
79f0113e220dcb89a592843795038ab655c114d1ab1ca9fa2e4cca2b75fad37b  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/macho-x86_64-uv.json
c5475f1f755128f63d6e6496e306b3170d26da3da6ff74093a921f207a47371f  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/macho-x86_64-uvx.json
5d7efbde26d1cde8ba71453f352a2776219a7168d41609142ba6ddb571e59e97  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/pe-arm64-uv.json
fdaeaf9c89bf6e4b13cc60acdb0dcdbef38e8a0e28aacf1b195e2181ab8ff552  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/pe-arm64-uvw.json
6b38ff1a4ee6dc832abbb5fdd9c5f5b204a6015e52740e60276f6ef1ae78ce20  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/pe-arm64-uvx.json
c0e1aa9114e611f77dfa0f84042756c23da574cdaccb5a51b5f3658c95563c03  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/pe-x86_64-uv.json
31b5ef7128c2d8e916da0ba2703852872b3923c15fc31594e485d551843006d9  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/pe-x86_64-uvw.json
1d557589b4771431fdcc4eed481d2bbe41c41667ead0130c2ad45c46175bb0e5  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/pristine-envelopes/pe-x86_64-uvx.json
2cdf27ed0227471c8f215631582e061801da4c2a1421b6c3e2048498baa36381  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/probe.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/probe.stderr
aa7a56b0e05323fd94dacff5a9f99a7f17f921fc42a333f2f7085bddb8f912fd  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/probe.stdout
f527509d30440ade04a1904f8bda60a55f7dc5df48ec01811c479b4bd1579dae  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/results.json
f94a81d2739984307eb6b5bb17fa8758b9d960750fe3b717e3ae62edf8ec505f  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/run-probe.py
70dd83fcce3939d4e1cebc4b8d0c570686044b9058e3ebee5f6a905b36dc53fb  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/runs.tsv
f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/rust_dep_oracle.py
b3559b820d9ce67fa548997b36cbda8314d94138b285cd2bbb07018289e12137  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/sources.tsv
4b37aebe66221cf09efb85f99bcf6cf20f8e7cf93a5f83f077c78423780add6b  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutC1Oracle2/artifacts.sha256
```
