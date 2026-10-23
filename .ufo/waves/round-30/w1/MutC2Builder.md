# MutC2Builder — deterministic builder mutation probe

## Result

- **[OBSERVATION] Seven of eight requested mutations were pinned and killed.** The root-package-0 substitution survived, but generated identical bytes: this carrier's root is package 463, so the original `other` already equals 0.
- **[OBSERVATION] Prediction-text defect demonstrated separately:** changing only the builder's dependency-index message from 584 to 583 preserved all 19 image hashes, and `--build` exited 0 without a PIN warning.
- **[OBSERVATION] All nine probes had passing pristine and restored runs.** Totals: 7 killed, 2 survived, 0 inconclusive; 27 bounded detector invocations.
- **[INFERENCE] The exercised non-equivalent image-byte changes are protected by the frozen SHA column. An assertion that every source/prediction edit must produce a PIN mismatch is too strong.** The equivalent root substitution is not evidence of an undetected image-byte change. The message-only survivor is a builder prediction-text coverage finding.
- **[OBSERVATION] No REA invocation, carrier/mutant execution, measure-mode run, or claim-data collection occurred.** No control met or emitted the frozen measurement target `mutants=19 matches=19 target=19 entry_ok=1 skill_ok=1`; a successful build is not that target.

## Isolation and detector

Axes: mutation sensitivity, isolation, exact restoration, reproducible receipts.

Sandbox clone command (exit 0):

```text
timeout 10 mkdir -p /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder && timeout 180 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/clone
```

Read-only `rev-parse HEAD` observed `4ee65c6771058284aa947a266475839d196ed4d4`. The copied tool's sole permanent adaptation was:

```text
MUT_DIR = "/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants"
```

Each mutation was applied alone to `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/c2-rust-refusals.py`, then reversed before the restored run. The frozen TSV in the clone was never edited. Its absolute `path` column still names the shared mutant directory, but **`--build` writes through the seat-local `MUT_DIR`, not that column**; measure mode, which would read that column, was never invoked.

Exact detector, identical in all 27 runs:

```text
timeout --kill-after=5 120 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/c2-rust-refusals.py --build --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/clone
```

The receipt recorder was invoked for each table row and phase using this exact form, substituting the literal case ID and `baseline`, `mutated`, or `restored`:

```text
timeout --kill-after=5 180 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/probe.py --case alignment-pad-8 --phase baseline
```

The recorder captures the detector's own stdout, stderr, exit, UTC start/end, source hashes before/after, and all 19 generated image hashes plus builder/frozen prediction fields. It also confirms written image bytes equal the builder tuples. **[OBSERVATION] All 27 runs had empty detector stderr, no watchdog timeout, and matching written bytes.** All child processes exited; none remains running.

## Requested mutant table

Expected for each requested non-equivalent edit: at least one `PIN mutant … sha256 differs from frozen` and detector exit 2. The extra text-only probe addresses the separate prediction-text acceptance requirement.

| Case ID | Smallest source change, original tool line | PIN mismatches | Mutated exit | Pinned / verdict |
|---|---|---:|---:|---|
| alignment-pad-8 | L96: alignment modulus 16 → 8 | 15 | 2 | Pinned; killed |
| compression-level-6 | L118: zlib default level 9 → 6 | 11 | 2 | Pinned; killed |
| junk-seed-11 | L144: junk increment 7 → 11 | 1 | 2 | Pinned; killed |
| nesting-32 | L153: both nesting counts 33 → 32 | 1 | 2 | Pinned; killed |
| extra-package-1 | L156: extra field on package 0 → package 1 | 1 | 2 | Pinned; killed |
| kind-Build | L159: kind `dev` → `Build` | 1 | 2 | Pinned; killed |
| root-package-0 | L162: package `other` → package 0 | 0 | 0 | Unpinned source edit; survived, byte-equivalent |
| index-n-minus-1 | L165: appended dependency `n` → `n - 1` | 1 | 2 | Pinned; killed |
| prediction-text-index | L167 only: message interpolation `% n` → `% (n - 1)` | 0 | 0 | Unpinned prediction text; survived |

**[OBSERVATION] None of the eight requested payload mutations changed the builder's prediction text.** The ninth, text-only mutation did so without changing any image SHA256.

### UTC and exit receipts

All dates below are **2026-10-23 UTC**; times are observed start times. Full microsecond start/end values and the exact argv are preserved in the corresponding JSON receipts and aggregate summary.

| Case ID | Pristine UTC / exit | Mutated UTC / exit | Restored UTC / exit |
|---|---|---|---|
| alignment-pad-8 | 02:44:06.762849 / 0 | 02:44:12.621722 / 2 | 02:44:28.401361 / 0 |
| compression-level-6 | 02:44:28.682883 / 0 | 02:44:34.554599 / 2 | 02:44:41.334507 / 0 |
| junk-seed-11 | 02:44:41.559451 / 0 | 02:44:47.784774 / 2 | 02:44:54.459474 / 0 |
| nesting-32 | 02:44:54.740072 / 0 | 02:45:04.188941 / 2 | 02:45:13.842283 / 0 |
| extra-package-1 | 02:45:14.101071 / 0 | 02:45:20.110152 / 2 | 02:45:26.414914 / 0 |
| kind-Build | 02:45:26.682781 / 0 | 02:45:32.863303 / 2 | 02:45:41.248811 / 0 |
| root-package-0 | 02:45:41.462074 / 0 | 02:45:47.673283 / 0 | 02:45:55.117026 / 0 |
| index-n-minus-1 | 02:45:55.364484 / 0 | 02:46:01.356224 / 2 | 02:46:10.443701 / 0 |
| prediction-text-index | 02:46:10.678335 / 0 | 02:46:21.658410 / 0 | 02:46:27.686971 / 0 |

### Full counter stdout

For **every pristine and restored run**, and the **root-package-0** and **prediction-text-index mutated runs**, the entire counter stdout was exactly this single line; each exited 0:

```text
mutants=19 rebuilt pin_mismatch=0
```

`alignment-pad-8` mutated stdout, exit 2:

```text
PIN mutant g-relocated sha256 differs from frozen
PIN mutant g-recompressed sha256 differs from frozen
PIN mutant g-no-root sha256 differs from frozen
PIN mutant r-not-zlib sha256 differs from frozen
PIN mutant r-trailing-bytes sha256 differs from frozen
PIN mutant r-over-1mib sha256 differs from frozen
PIN mutant r-inflate-ratio sha256 differs from frozen
PIN mutant r-not-utf8 sha256 differs from frozen
PIN mutant r-bad-json sha256 differs from frozen
PIN mutant r-nesting-33 sha256 differs from frozen
PIN mutant r-format-negative sha256 differs from frozen
PIN mutant r-extra-field sha256 differs from frozen
PIN mutant r-kind-dev sha256 differs from frozen
PIN mutant r-two-roots sha256 differs from frozen
PIN mutant r-index-outside sha256 differs from frozen
mutants=19 rebuilt pin_mismatch=15
```

`compression-level-6` mutated stdout, exit 2:

```text
PIN mutant g-recompressed sha256 differs from frozen
PIN mutant g-no-root sha256 differs from frozen
PIN mutant r-inflate-ratio sha256 differs from frozen
PIN mutant r-not-utf8 sha256 differs from frozen
PIN mutant r-bad-json sha256 differs from frozen
PIN mutant r-nesting-33 sha256 differs from frozen
PIN mutant r-format-negative sha256 differs from frozen
PIN mutant r-extra-field sha256 differs from frozen
PIN mutant r-kind-dev sha256 differs from frozen
PIN mutant r-two-roots sha256 differs from frozen
PIN mutant r-index-outside sha256 differs from frozen
mutants=19 rebuilt pin_mismatch=11
```

`junk-seed-11` mutated stdout, exit 2:

```text
PIN mutant r-not-zlib sha256 differs from frozen
mutants=19 rebuilt pin_mismatch=1
```

`nesting-32` mutated stdout, exit 2:

```text
PIN mutant r-nesting-33 sha256 differs from frozen
mutants=19 rebuilt pin_mismatch=1
```

`extra-package-1` mutated stdout, exit 2:

```text
PIN mutant r-extra-field sha256 differs from frozen
mutants=19 rebuilt pin_mismatch=1
```

`kind-Build` mutated stdout, exit 2:

```text
PIN mutant r-kind-dev sha256 differs from frozen
mutants=19 rebuilt pin_mismatch=1
```

`index-n-minus-1` mutated stdout, exit 2:

```text
PIN mutant r-index-outside sha256 differs from frozen
mutants=19 rebuilt pin_mismatch=1
```

## Survivor interpretation and prediction-text finding

### Root substitution

Producing command: the common detector above, with the root-package-0 source snapshot; UTC `2026-10-23T02:45:47.673283+00:00`, exit 0, full stdout shown above. Recorder observations:

```text
package_count=584
root_indices=[463]
sha_mismatches=[]
prediction_differences=[]
```

**[INFERENCE]** At original L121, `other = 0 if 0 not in root_i else 1` evaluates to 0 for this frozen base. Replacing `other` with 0 therefore is not a distinct image mutation. Its survival cannot establish a missing byte-hash check, although it does not satisfy the task's literal expectation that every listed edit prints PIN.

### Prediction-text-only substitution

Producing command: the common detector above, with the prediction-text-index snapshot; UTC `2026-10-23T02:46:21.658410+00:00`, exit 0. Recorder output excerpt:

```text
sha_mismatches=
prediction_differences=r-index-outside
```

**[OBSERVATION]** The builder returned:

```text
Dependency index 583 from package 0 is outside the package list
```

while the unchanged frozen TSV says:

```text
Dependency index 584 from package 0 is outside the package list
```

The binary's SHA256 remained `04a1bcddda326d2c6ba16f22eccbdd654ef88dd7761977afb0a842239a741539`; all other 18 image hashes also remained frozen. Original L306 compares only SHA256; original L309 carries the message forward but does not compare it against the frozen message.

**[INFERENCE]** This is a prediction-text defect that the build pin detector does not catch. It is specifically drift in the builder-returned prediction text. With the frozen TSV present, `--build` does not rewrite it, and measure mode reads predictions from that TSV at original L324. Thus this probe does **not** demonstrate that this message-only edit would alter the effective frozen prediction used by live measurement.

**[UNKNOWN]** No actual REA refusal message or R30-C2 live-match outcome was measured in this seat. No inference about live matches is promoted to an observation.

## Hash and restoration evidence

Original lane tool SHA256, both initial observation and final source registry:

```text
1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b
```

Seat-local pristine tool, with only `MUT_DIR` redirected:

```text
fcdcb01efc8acff610e11c339ad37e7945ca0607513d22c1eb7beb3a65a72d7c
```

**[OBSERVATION]** Every baseline source hash equals that seat-local pristine hash; every restored source hash equals it exactly. Each mutated snapshot's source hash is listed in the artifact inventory below. The last restored run ended at `2026-10-23T02:46:27.800577+00:00`, exit 0, and restored all 19 output-image hashes to their frozen values. The complete 19-row before/mutated/restored hash sets for every probe are retained in the JSON receipts, including the 15 alignment and 11 compression mismatches.

Representative image hashes, with the first column also equal to the observed restored hash:

| Case / image | Pristine and restored SHA256 | Mutated SHA256 |
|---|---|---|
| alignment-pad-8 / g-relocated | `8620146512a7a1ffe01ed248726fc3326d74f2a8f853eb7dc94deda7854fbf0c` | `2cf159ff16d23609009310b9cbafb5e7d96773a7ab266368f1901ed276dbbecb` |
| compression-level-6 / g-recompressed | `a5ebc1fc29431ce66cf2b2323a9c2cdac352219b94ec3f270c3491ccd45a7f7a` | `110d6897c22805979cec025d8d2e33a5bccdaccada2a07d84e0af1322a4f3a93` |
| junk-seed-11 / r-not-zlib | `fe06adf465df9b54e4563b9f4a7952b6af6c25860ce583633aa7e808038f69e6` | `5d22fd46b26869585c4c5ee3d169a751e123db16766fe40a42ee8e5a9631e107` |
| nesting-32 / r-nesting-33 | `278c2b9d0e37b930924e0adb5224992511fd541a357d77891a9eea98233dceea` | `cdcb0508c0aaa4ddb9116e16d0e21fbb511487115a3c07c050ea1a863185ec62` |
| extra-package-1 / r-extra-field | `817538ebbe233f38013cde0b0777a2c56823563d5df185bb1e0bf971c4304464` | `4d37dbf63625656cea91bfbf418be2cc348616c9c698ae604bb09f35821230b8` |
| kind-Build / r-kind-dev | `1f971a6eeb831427118263b706c8ff80dc28f47df15ece8467b500892968025a` | `80639c9893bd863649427e77df26a3dbea8eb85791baa18df068754c75ba1061` |
| root-package-0 / r-two-roots | `6c8bc2eca7dc9f631b57ca4e329a12b7cd21a52f909238b882a2e6d87eb2efc7` | `6c8bc2eca7dc9f631b57ca4e329a12b7cd21a52f909238b882a2e6d87eb2efc7` |
| index-n-minus-1 / r-index-outside | `04a1bcddda326d2c6ba16f22eccbdd654ef88dd7761977afb0a842239a741539` | `fbcaea46a84f1da27d2374e7bbd96ba9960f3e8562759444578bab149943891b` |
| prediction-text-index / r-index-outside | `04a1bcddda326d2c6ba16f22eccbdd654ef88dd7761977afb0a842239a741539` | `04a1bcddda326d2c6ba16f22eccbdd654ef88dd7761977afb0a842239a741539` |

**[OBSERVATION]** Frozen predictions SHA256 before and after all 27 runs was always `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315`. The base carrier hash recorded by every run was `2e9105ad948131962cbe20502e406d571a22d11c2f9d62ec8c8b88798172890d`, size 332008. Its 16-byte alignment pad is 8 bytes, versus 0 at 8-byte alignment.

### L1 carrier-tampering notice

**[OBSERVATION] This seat did not alter any carrier or shared mutant.** The copied builder only read the carrier and wrote the seat-local mutant directory.

The initial pristine detector at `2026-10-23T02:44:06.762849+00:00` exited 0, with full stdout `mutants=19 rebuilt pin_mismatch=0`. **No `PIN base carrier altered`/carrier-PIN-blocked run was observed in this seat; there is no such failed run to report.** The intentional mutant PIN failures above are not baseline failures.

Following the L1 notice, pristine/restored counter runs continued. In particular, the final restored rerun at `2026-10-23T02:46:27.686971+00:00` exited 0 with the same full stdout and the verified carrier hash above. This supplies an actual rerun after the notice's stated approximately-02:46 restoration. **[UNKNOWN]** The identity and mechanism of the writer described in the L1 notice were not investigated by this scoped seat.

## Local sources and access records

No remote source was opened. Each local primary source below was read by ordinary local-file access on **2026-10-23**; hashes cover the complete file bytes. Quotes are contiguous excerpts of at most 25 words.

| URL | SHA256 | Located quote |
|---|---|---|
| [Builder](file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py) | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` | L306: `if frozen and frozen.get(mid, {}).get("sha256") != h:` |
| [Frozen predictions](file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv) | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` | L1, tab-separated: `id kind message sha256 size path code_pointer` |
| [Carrier inventory](file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv) | `c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b` | L3: `elf-x86_64-uvx` |
| [Independent oracle, exploratory read only](file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py) | `f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d` | L3: `Shares no code with REA.` |

The raw tab-preserving prediction-header quote and full source URLs are also recorded in `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/summary.json`.

## Artifact inventory and tooling

**[OBSERVATION]** Final evidence summarization command:

```text
timeout --kill-after=5 90 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/summarize.py
```

Exit 0; UTC `2026-10-23T02:48:47.068474+00:00`; exact output excerpts:

```text
counts={"inconclusive": 0, "killed": 7, "survived": 2}
all_detector_stderr_empty=True
all_written_files_match_builder_bytes=True
predictions_sha256=6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315
clone_tracked_file_count=21316
```

An initial ancillary inventory attempt, not a detector run, exited 1 on a dangling tracked fixture symlink (`FileNotFoundError`). The inventory helper was corrected to hash a symlink's link-text bytes rather than follow it; no probe or builder contract was changed. The successful clone manifest enumerates all 21,316 tracked clone paths with SHA256 (symlinks use link-text bytes). Clone Git administrative files are not authored deliverables and are outside that tracked-content manifest.

The complete authored/output artifact inventory is `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/artifact-manifest.sha256`, SHA256 **`631f9af893bf9390fad50678f7bffcc8cf93469cd7ddb8b07c4a938053c1ddd3`**. Its full contents follow; the clone's complete tracked-content inventory is itself listed and hashed here.

```text
fcdcb01efc8acff610e11c339ad37e7945ca0607513d22c1eb7beb3a65a72d7c  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/c2-rust-refusals.pristine.py
fcdcb01efc8acff610e11c339ad37e7945ca0607513d22c1eb7beb3a65a72d7c  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/c2-rust-refusals.py
f479aaf4f16afb6a79c3384b53a06ea37247e0e41f3bb6b2d2777242f90fe6b6  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/clone-tracked.sha256
003cf60d734c165fd826b2100b1e62da72bb4f30c2d7eb3d73d408404f665cc7  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/g-no-root
a5ebc1fc29431ce66cf2b2323a9c2cdac352219b94ec3f270c3491ccd45a7f7a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/g-recompressed
8620146512a7a1ffe01ed248726fc3326d74f2a8f853eb7dc94deda7854fbf0c  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/g-relocated
c50d13f858c55aa256163c189dc1fa6d6801bd14c2b66cfd363888d946ff46a0  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-bad-json
d3f0dc6aa3bfd558d5a27ef53c43914bc5ada4d4da47e6033a60f666025bb25c  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-compressed-flag
e26e2ff2951c1da625f4d5871e85bf1912e6e825ee35fb0bf5a7390045c40681  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-empty
817538ebbe233f38013cde0b0777a2c56823563d5df185bb1e0bf971c4304464  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-extra-field
b5194f81ddb2f0e32375ee968b486b150a1607ffa434dae1668d643ddb55a336  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-format-negative
04a1bcddda326d2c6ba16f22eccbdd654ef88dd7761977afb0a842239a741539  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-index-outside
c6434b546b9b848d50a2732899ad130db88414c6cb20df4cc5d2d8286fff4ab5  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-inflate-ratio
1f971a6eeb831427118263b706c8ff80dc28f47df15ece8467b500892968025a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-kind-dev
278c2b9d0e37b930924e0adb5224992511fd541a357d77891a9eea98233dceea  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-nesting-33
efcaf55e3b01c67844a11ddab81cda0ca309f5de78b7de3ff615a4325315c16f  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-nobits
6399a2730ce9b609c8f111ef47ca4026e9a961d194e2abe253458098cda957c7  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-not-utf8
fe06adf465df9b54e4563b9f4a7952b6af6c25860ce583633aa7e808038f69e6  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-not-zlib
b645eb8149af2b1d6b4655b6ea6f327667e9b47b2b7bba6ea25e97cf74792089  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-over-1mib
33d81ca13ded5cc36f138b56bce39c8cdd0840e1e54ee47b39b8ac60a6057727  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-trailing-bytes
6c8bc2eca7dc9f631b57ca4e329a12b7cd21a52f909238b882a2e6d87eb2efc7  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-two-roots
25edfe0e3ff1f73ba1636241c3b1be2b83c44a9b5b7ca30b22c0d15c410c56db  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/mutants/r-two-sections
678d16623b57f5bdfb098c0657f3fe2186f72436484ed2363039fd0f1b129351  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/probe.py
37ab7b7fb1b35fb8482d60db3801e160cf7ccc0e3e863efe388f8df94ff1189d  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/alignment-pad-8.baseline.json
53f6bd688a3f1614031a6a7c7f742a13c98233634e7f5069b43d7b4abf3a97f7  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/alignment-pad-8.mutated.json
c2623c5b19104ce61f592f351742ad7fe8aba2cec1b79fa9498302fcbd3c792e  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/alignment-pad-8.mutated.py
29c876a106f4b6237619a8d23c301f93dd1bcb385dc155273048d023ffb02bb3  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/alignment-pad-8.restored.json
a6ab4b85f7f5338cd0fedc5d36fa4840d8d0be8d4eda3eb43fcb1930b2e8c286  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/compression-level-6.baseline.json
6948983cd837b63308221750426c52117e8bb7700ca075d77ad6dd1a9c6255c1  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/compression-level-6.mutated.json
2e616944f3c74a90b1dd9fefaea2e778dbbfd3da4bb96cb240733449bf82a9cc  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/compression-level-6.mutated.py
003e5547123d5bd50b564312508ca67f4e95627482731bc6f0c2beccd8b67936  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/compression-level-6.restored.json
60dc11b6e4d178a6b6dceffcbc0ae55648ebb5b82519a86d42f810fc56629f4c  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/extra-package-1.baseline.json
c50bded7528f295282f801461b38761f6a6770d9d09dd5b1c8e1acb67dfc757a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/extra-package-1.mutated.json
2d4bd6dbf8979b483e21943bb411f1e3dd45dc7ec31eda11d6bf2157129f4316  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/extra-package-1.mutated.py
0d7fc2a63b146151422a8a0b00cc5e64d1e39c89a2f13ea1b61417edff1669d0  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/extra-package-1.restored.json
afa3af6a082205a41f550a676fbf10e5b2231f4a39513859ff63c76ae9af64e0  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/index-n-minus-1.baseline.json
888a7e1cea06cfa1a2489bc61eb565775d79e176de7b53c3f497a76b2a7edbdf  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/index-n-minus-1.mutated.json
72f3a5654e53fdfdc9ce2788de9f2499afc565e5531f14991b2c798c5286b3c7  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/index-n-minus-1.mutated.py
cd7522d21da955692d49df164dbfed86aed806835e3716e35fc925ea0d2e2cad  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/index-n-minus-1.restored.json
914782734a40653bd0d98695f780e00b220d4845aa68ce1505feac8c582cb49a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/junk-seed-11.baseline.json
b2eb1efd3f4942277cd814739f0538c93fd6c8a3f8f53cdc7051b30c5f6fc52b  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/junk-seed-11.mutated.json
733dbf78faaf5d59e7a6086cd7bede0e10c99a8ce2e4a313958703b761d312a3  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/junk-seed-11.mutated.py
2fa18cc0e1bb392e33977298ea183d49f67ae3d6284bba794be55ef78f3991c9  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/junk-seed-11.restored.json
1043f7dbf2eb5f33e2fe7012f1953eee03c15b58ac3856df20bcc96edf81d23c  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/kind-Build.baseline.json
a684960229d87a7149eb615a9c1fd781cf02bc21676e1a83ddb90888de13623d  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/kind-Build.mutated.json
26f890a75466a46735e00dc608d5219338dbf620d084032d79db9dfaf833580c  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/kind-Build.mutated.py
8d93df6c0c1df553b17bde38cc94fa246188d23c8b417ef85476b63b20966836  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/kind-Build.restored.json
ad550bf6ba5ae9b9c55cfbe6390c6e113dcb3b52257e77253543afca0d9f2ebb  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/nesting-32.baseline.json
ec10eba87c3b89ce058861dffccffda9e2330862baa2716249ecd281ae736420  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/nesting-32.mutated.json
c9157fc0414546328480b10fd147768c15a12b53f8b06d395e0df42a2ea53917  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/nesting-32.mutated.py
c646e431286815518acdf8ef2402fd8e0c61798c00eac7d574c4985e69c0a2e6  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/nesting-32.restored.json
811b166dd7168787f382e80a9a8d7ad27f57a8be5f6d63cad549d44cfecd5b62  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/prediction-text-index.baseline.json
19a512fe37a65a213bdad7375f59de19a3c713d269cde527596a2166b0e70670  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/prediction-text-index.mutated.json
cbe72fab390b32b1b5eb500485ea297f7db6f59d85f02b18305a8ab5e5232721  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/prediction-text-index.mutated.py
2da027660c25a12e0d03016d5e1995daf35486bc2fd73bb12dcb469e41d1be8f  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/prediction-text-index.restored.json
f1499fec9cbaaba8b8df7ec7c48a1fbcdf392d99e4baee382f95a944c3274349  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/root-package-0.baseline.json
6b40bb791e353935b488902fefd8102e64b353cf7fc9cfc01872ed8c91143de8  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/root-package-0.mutated.json
76cd605d7778f4c5c8bd7b6ba16a4a3fe6fa00c67efe0438f6b9634df7dad374  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/root-package-0.mutated.py
988d4ea02730e5dff3c9c1ab43c3d57565956a40343e0059eebc153c94784d34  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/receipts/root-package-0.restored.json
389e9451a8aed89d35267678b15e9eda5cd0c8118da542411b52eda9138acfa9  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/summarize.py
51c4c86b811e9d1992d45edfb8dd21b6fe2be98fbf8ff591a81a4cff230b5418  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC2Builder/summary.json
```

Tool installs/updates: **none**. No pacman transaction, git/jj write in the lane/fleet, sibling-source change, or unbounded process was performed. The only lane file written by this seat is this scoped report. No integration, repair, or claim judgment was performed.
