# FinalCustodyOrder — residual custody/order critique

Evidence measured on **2026-10-23 UTC**, principally 07:14:25.003278–07:14:25.113426, with report reconciliation at 07:16:39.040545–07:16:39.040998 and the additional round-17 chronology question at 07:22:17.481058–07:22:17.500020.

Immutable product: **`bb0af56c29e7b4c11d0583ed6697d0e17aba9d26`**. This is author-side advisory evidence, not outside admission or a canonical Rust-judge verdict. No counter, predicate, fixture, production document, Git/JJ state, routing, or held item was changed. Only this Report and this seat's own scratch were written.

## Axes and result

- **Coverage custody:** frozen C1 bytes, controls-before-production evidence, and persisted-envelope identity.
- **Calibration / provenance truth:** correct attribution of counter failures, C2 honest stop, and no invented execution chronology.
- **Dispatch certainty:** planned items versus actual starts versus authenticated deaths. Depth and saturation were not assessed.

**Observed:** the controls commit is the product's direct parent and has the earlier committer timestamp; all twelve production `runs.tsv` starts follow it by at least 22 seconds. All frozen claim/instrument/input bytes checked are unchanged. All ten receipt rows agree with their complete committed reports, including four separately preserved initial provider failures. No removed attempt-1 raw-log bytes were used as claim outcomes.

**Residuals:** (1) the lesson still opens with the unsupported “36 w1 seats died” sentence, although its later explicit correction is sound; (2) the additional private round-17 partial-positive fixture's execution order relative to controls is **unknown**, not established pre-control or post-control. These do not justify changing a frozen predicate. C2 remains the already-recorded honest stop.

## 1. Strongest counterexamples and smallest safe corrections

| Counterexample | Committed evidence at the product | Impacted axis | Smallest safe correction |
|---|---|---|---|
| A reader taking the introduction literally counts 36 deaths, even though 36 is the plan and only a 12-seat group count survives from an untrusted historical log. | `corpus/lessons/round-32.md:3` asserts “36 w1 seats died”; `:53` expressly withdraws that overstatement. `attempt1-discard.json:48–339` has 36 planned members, all null IDs, all excluded, and a separately limited untrusted start count of 12. | Provenance truth / calibration. | Make the current introductory summary say **36 planned/excluded; one reported 12-seat start group; individual deaths not authenticated**. Preserve the historical mistake and correction, but do not repeat the old assertion as current fact. This is a reporting defect, not a counter defect. |
| The same aggregate `carriers=12 pass=0 ... entry_ok=1 ... province_ok=1` occurs both when the live provider fails and when the committed-envelope requirement actually rejects the fixture. A flat numerator alone cannot distinguish them. | Complete A2C1Empty, A2C1False, A2C1NoReader and A2C1Labels reports retain both receipts. Their initial reason is `exit 1 ok False`; their resolved reason is `committed envelope absent` or the full-comparison mismatch. | Coverage-evidence discrimination / calibration. | Keep the linked complete reports and count **only the provider-bound committed-check receipts** as these five controls' discrimination evidence. The landed lesson already makes this distinction. Do not turn the four initial failures into four additional successful controls. |
| “All positive scoring followed controls” is not established by a report window that straddles the controls commit. | `a2audit/A2Capability17.md`, opening timestamp 06:55–06:58Z and §6 private fixture `1d2c9814...`, versus controls committer 06:56:11Z. There is no per-invocation timestamp in §6. | Chronology truth / C2 calibration. | Disclose the private partial-positive run and its **unknown order**. Do not infer pre-data compliance from when its report landed. No new run could recover this historical instant. Production C2 repair and C1 envelopes remain at `bb0af56c`; C2 was already stopped. |

No new axis tradeoff was exercised here. The known negative-prose/word-bag acceptance is the frozen C2 measure's discrimination failure, not something this custody review can repair or relabel. Canonical disposition remains outside this review.

## 2. DAG and actual committer timestamps

The measured chain is linear. Each row's parent is the preceding row, except the first parent is base `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`.

| Full revision | Committer UTC from `%ct` / `%cI` | Recorded author UTC (not used for ordering) |
|---|---|---|
| `9a73680af21b002e3b99956c89234b2bbde2a71b` | 06:03:46Z / 1792735426 | 05:44:59Z |
| `9d54070bebceff77401b25a1bb12e19107b3ab67` | 06:06:39Z / 1792735599 | 06:03:46Z |
| `f382e3b7978e6091a19ca93277c15a75c0016b43` | 06:10:01Z / 1792735801 | 06:06:39Z |
| `411f3a80a1efefabe2ba12f227147023cfbce4bd` | 06:51:01Z / 1792738261 | 06:10:01Z |
| `33393e594f1e278777fa49020b42c66ac4fa352e` | **06:56:11Z / 1792738571** | 06:51:01Z |
| `bb0af56c29e7b4c11d0583ed6697d0e17aba9d26` | **07:06:23Z / 1792739183** | 06:56:11Z |

Observed direct parent of `bb0af56c` is `33393e59`; this is stronger than a timestamp-only comparison. `merge-base --is-ancestor` exited **0**, stdout/stderr empty, for controls→product and each of the three freezes→controls.

All ten report files are present at `33393e59` and byte-identical at the product. More precisely, **A2C2False and A2C2Labels were first added at `411f3a80`**, while the remaining eight reports and `controls/a2-receipts.tsv` were first added at `33393e59`. “All present by 33393e59” is accurate; “all first created by that commit” would not be. Both receipt-table and metadata files have an empty diff from controls to product.

`git log --reverse --diff-filter=A` for `corpus/evidence/round-32/c1/envelopes` returns only product `bb0af56c`, committer 07:06:23Z, adding k01–k12 `.json` and `.stderr`. `ls-tree` at controls returns **empty stdout** for both that envelope directory and `corpus/evidence/round-32/c1/runs.tsv`.

These are observed immutable Git metadata and retained receipt times, not externally signed wall-clock attestations. This scope concerns the twelve production carrier envelopes; the explicitly disclosed pre-freeze probe and negative-control calls are different inputs/evidence roles.

### Production run starts versus controls

Source: `bb0af56c:corpus/evidence/round-32/c1/runs.tsv`, SHA-256 `62df49f73c3a8da0caa94b4e93711edcb5bc21e30e77f79b8043d98a6e2856b9`.

| Carrier | Retained UTC start | Retained UTC end | Retained exit |
|---|---|---|---|
| k01 | 06:56:33 | 06:56:41 | 0 |
| k02 | 06:56:41 | 06:56:49 | 0 |
| k03 | 06:56:49 | 06:56:58 | 0 |
| k04 | 06:56:58 | 06:57:07 | 0 |
| k05 | 06:57:07 | 06:57:19 | 0 |
| k06 | 06:57:19 | 06:57:32 | 0 |
| k07 | 06:57:32 | 06:57:47 | 0 |
| k08 | 06:57:47 | 06:57:58 | 0 |
| k09 | 06:57:58 | 06:58:07 | 0 |
| k10 | 06:58:07 | 06:58:16 | 0 |
| k11 | 06:58:16 | 06:58:27 | 0 |
| k12 | 06:58:27 | 06:58:38 | 0 |

The measured minimum is unambiguous: first start **06:56:33Z**, **22 seconds after** controls' committer 06:56:11Z; final end 06:58:38Z. Twelve rows, all exit 0, each package version 6.5.0 and package JSON SHA-256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`.

For every carrier ID, the TSV's exact argv shape is `npx -y rea-agents@6.5.0 inspect /fast/scratch/hyaku/kaidoku-r32/carriers/<ID>.dll --format json --full-output`; all twelve expanded strings and their per-call instants are retained in the cited immutable TSV and in `audit.json:runs_receipt.stdout`.

The separate committed producer receipt `a2after/c1-write.txt` explicitly runs against controls revision with `--write-evidence`; it retains `exit=3` and `WRITE-MODE ... (not a receipt; no target line)`. Its twelve `P1-pass` lines are **not** a final committed-clause/target measurement. I did not rerun it.

## 3. Frozen bytes: endpoint identity and no intervening changes

For each frozen claim document, read the blob at its named freeze and at product; parse its `instruments` and `frozen_inputs`; SHA-256 both versions of every referenced file; compare with the declared pin; and inspect `git log --full-history <freeze>..<product> -- <path>`. **15 checks / 14 unique files**, because freeze-integrity.py is pinned by both v2 and v3. All endpoint bytes match; every declared instrument/input hash matches; every post-freeze path history is empty. Claim-document hashes below are measured whole-document hashes, not self-declared pins.

| Freeze | Path | SHA-256 at freeze and product |
|---|---|---|
| 9a73680a | `.ufo/waves/round-32/claims.json` | `8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435` |
| 9a73680a | `tools/round-32/c1-arm64x-positive.py` | `7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a` |
| 9a73680a | `tools/round-32/arm64x_oracle.py` | `17eea1f9768ec73e4e66712e7cf4221de83a1052cda40c5801d1e64a80936686` |
| 9a73680a | `tools/round-32/c2-capability-calibration.py` | `c3412b04f5b6c663367217f3a5747f7e3bc32b7a06d4400e53f9e92654bc4446` |
| 9a73680a | `tools/round-32/build-arm64x-carriers.sh` | `7da284da5986295263c69a8b7ee779638428d3bb6c9d5c9d8fb224c40a737ba3` |
| 9a73680a | `corpus/evidence/round-32/c1/carriers.tsv` | `8cf97b37f72bf5b494ac5993a88051e4697038c8f66606e2a6e17fda1bf3d16e` |
| 9a73680a | `corpus/evidence/round-32/c1/predictions.tsv` | `fd8049498e519d13c9bd28415327a0bafa75c43684b2d1998d8e5d769737c56b` |
| 9a73680a | `corpus/evidence/round-32/c1/inputs/loadconfig-arm64.s` | `7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d` |
| 9a73680a | `corpus/evidence/round-32/c1/inputs/loadconfig-arm64ec.s` | `c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4` |
| 9d54070b | `.ufo/waves/round-32/claims-v2.json` | `805a05146515580d644074792db3d84a241307e65fbd9c54b916b762d82e5609` |
| 9d54070b | `tools/round-32/c2-capability-calibration-v2.py` | `82434cba039e62d8824dfb3236ad376d93cb2d57ab906cc3373c70bc93a8d36a` |
| 9d54070b and f382e3b7 | `tools/round-32/freeze-integrity.py` | `6b5aa1dfcaef04b8d6e58babebf826d677d6eeecc8b13906213dfd8f041804cd` |
| f382e3b7 | `.ufo/waves/round-32/claims-v3.json` | `a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d` |
| f382e3b7 | `tools/round-32/c2-capability-calibration-v3.py` | `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f` |

The manifest byte identity also preserves all twelve listed carrier digests. This read-only Git-object audit **does not independently hash the external carrier DLL files**, rebuild them, or run REA. It establishes committed frozen-input custody, not new live input authenticity.

## 4. Ten receipt rows versus complete reports

Receipt source: `bb0af56c:.ufo/waves/round-32/controls/a2-receipts.tsv`, SHA-256 `3f486796fd28e1e5640f7963a1542b504d11ec5fcea43294e760c211a83d0f9c`. Metadata SHA-256 `5583467eadb3a24da01c3428ecf9b178372263ce4acfc11b33827dc94a9224db`.

The audit read **533,747 report bytes**, all ten complete blobs, not just headings. For each row: the whole-report SHA-256 equals `report_sha256`; the measured full revision is present; the report is byte-identical at controls/product; the complete printed score blocks agree with the row's numerator and target; retained exits agree with `counter_exit`; and the row's `met_target` agrees with numerator/target/exit. Six reports have machine-parsed structured exits; the other four exits are explicitly retained in their narrative/tool-output receipts. No scoring was repeated here.

All paths in the following two tables are under `.ufo/waves/round-32/a2audit/`, at **product revision**, and contain complete fixture and receipt evidence. The report-line references identify the actual retained result, not a new execution by this seat.

| Control / predicate | Measured private fixture revision | Numerator / target; exit; met target | Actual retained decisive reason / reverse count | Receipt location |
|---|---|---|---|---|
| A2C1Empty / P1-pass | `e8e468b74471e9f32359e709b0ed94e72a0b22d6` | 0/12; 1; no | all 12 `committed envelope absent`; doc gates 1/1 | `A2C1Empty.md:95–134`, structured at :221 |
| A2C1Garbage / P1-pass | `a1335f9e16e6209c443721f970f654074d033a22` | 0/12; 1; no | all 12 full committed/live mismatches; doc gates 1/1 | `A2C1Garbage.md:31–84` |
| A2C1False / P1-pass | `1199091b68f39271ffeeec4bdfff72297659d4f5` | 0/12; 1; no | all 12 full committed/live mismatches; doc gates 1/1 | `A2C1False.md:61–116` |
| A2C1NoReader / P1-pass | `f7ba512dd9244df02773378cb0f66f22abac32fb` | 0/12; 1; no | all 12 full committed/live mismatches; doc gates 1/1 | `A2C1NoReader.md:9–33`, :268 |
| A2C1Labels / P1-pass | `db9099752efadc2f130e10f6df07509c3fc9ea23` | 0/12; 1; no | all 12 full committed/live mismatches; doc gates 1/1 | `A2C1Labels.md:64–116` |
| A2C2Empty / P2-match | `28fcbcdf3ef47893cc38f84ec1c73702a3582abc` | 0/4; 1; no | all four summary rows absent; reverse 0 | `A2C2Empty.md:39–93` |
| A2C2Garbage / P2-match | `9b939fce514b34581dc76b9f900f6993b9c1f47c` | 0/4; 1; no | each description shares 0 words; reverse 4 | `A2C2Garbage.md:99–122` |
| A2C2False / P2-match | `42d814ff5f46ac45bf2b6f9b659ac094bca88f61` | **4/4; 0; yes** | explicit denials accepted; description overlaps 8,12,12,11; reverse 0 | `A2C2False.md:29–69` |
| A2C2NoReader / P2-match | `b8c508e0059fcb79eab240101fd37b2b820cf9be` | 0/4; 1; no | no resolving anchor in each evidence cell; reverse 4 | `A2C2NoReader.md:56–84` |
| A2C2Labels / P2-match | `cbb7dbce50861117076e57d42ec5f471f71bd413` | **4/4; 0; yes** | alphabetized five-word bags accepted; reverse 0 | `A2C2Labels.md:89–105`, :132–150 |

**C2 disposition is unchanged:** the two yes rows are failed-discrimination controls, not successful repairs. The negative-prose fixture/receipt had already been retained at `411f3a80`; this review neither re-freezes nor rescues it.

### Whole-report identities

| Report | Bytes | SHA-256, equal to receipt row |
|---|---:|---|
| A2C1Empty.md | 22854 | `06309603f0c5d2c48a783c52966b5eb0d8c364c72dfb759bfd6938f654a88c8f` |
| A2C1Garbage.md | 20430 | `1daa897e028be12706029ab7d0f9d664c95beab277978e2efc83d4bfceb85a04` |
| A2C1False.md | 86657 | `d5d5eb1f9583d92da539a2b2a499c2bbb9af974498281c803681859c8bd218e4` |
| A2C1NoReader.md | 98438 | `3aa64a289c8eb897ce872517a7e14b99ce271fecfa54f085921f535a3a98cb32` |
| A2C1Labels.md | 85593 | `70b28ae90b38979718811805a77c0dad9f94c37481b599eb0b06e8ff9ecf927f` |
| A2C2Empty.md | 143451 | `8d18eb8348daeb8fdea9efe3c7d23c03f91e8997058f24823c14b019e7b68504` |
| A2C2Garbage.md | 13518 | `fb1f74b37b853a50106812520888092f9fa9d472e8afff4a955bf4096fd84cf8` |
| A2C2False.md | 15236 | `53466078bb28e226abf37bc60fca2c9219fbe65bd5aa8131fb27c316408f1a8f` |
| A2C2NoReader.md | 33854 | `8f16289607f425975a1022f665f7d9157c7d097602cadd41b103900a98e7571d` |
| A2C2Labels.md | 13716 | `1142f21c7004e6cde73e263c3b0550da81b5ece48a567b2acb8ff155187f4fb8` |

### Initial failures are not discrimination credit

All dates below are 2026-10-23 UTC. The same fixture revision is retained for initial and provider-bound runs.

| C1 report | Initial failure interval, exit 1 | Provider-bound committed-check interval, exit 1 |
|---|---|---|
| Empty | 06:47:26–06:47:35 | 06:48:54–06:50:36 |
| False | 06:47:55–06:48:04 | 06:49:15–06:51:03 |
| NoReader | 06:48:25–06:48:37 | 06:50:02–06:51:49 |
| Labels | 06:47:41–06:47:50 | 06:48:47–06:50:29 |

The four initial stdout receipts print k01–k12 `P1-fail\texit 1 ok False`, followed by the same 0/12/doc-gates-green aggregate. They do **not** print a committed-envelope rejection. The changed-environment receipts explicitly supply `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` and `JAVA_HOME=/usr/lib/jvm/java-21-openjdk`. Garbage's one Bash run already inherited those values; it had no initial provider-failure receipt (outer launch observation 06:47:10Z, receipt observation 06:48:50Z, wall time 91.37 s; no invented per-carrier timestamps).

[INFERENCE from immutable counter `c1-arm64x-positive.py:198–202`] the committed-check reasons are reached only after the live judge passes. This supports the bounded discrimination interpretation. It is **not** a separately captured live-envelope/exit trace: measure mode suppresses those inner bytes. Labels' later, separate non-carrier probe diagnostic records `provider_unavailable`/Ghidra `not_configured`; it is not an extra carrier control or retroactive retention of all original inner errors. The other suppressed inner errors remain unknown.

Exact original scoring argv, exits, stdout and fixture bytes are available in the ten committed reports named and whole-file-hashed above; they are not citations solely to ephemeral scratch. The reconciliation output also retains the parsed structured receipts and every complete score block.

## 5. Attempt-1 discard: 36 planned, limited 12-start provenance, no 36-death finding

Product inputs:

- `.ufo/waves/round-32/attempt1-discard.json`, 9795 bytes, SHA-256 `ca87e6dc0283d07b93961eadbbae3b3c6534f31bd237df1d8165e68e78db27fe`.
- `.ufo/waves/round-32/a2audit/A2AttemptForensics.md`, 12413 bytes, SHA-256 `122b1ddd09d0c31f22f17affd1edd305f0ca472edb45e8b9c172e9c511dcd5b2`.
- `corpus/lessons/round-32.md`, 10747 bytes, SHA-256 `a6eea0b454150269b83d717dd47963e0deb178a6f084f76a1498ad9c3e495ee6`.

Observed JSON structure: **36 planned_members; 36 null agentId values; all 36 dispositions exactly `excluded; no report used; no retry/replacement`**. It inventories seven discarded files and marks every one untrusted/not claim evidence. The historical group-start count is explicitly named `observed_start_count_from_untrusted_log: 12`, with this exact limit:

```text
Only group count and one exact runtime id preserved. Other planned24 refused/unknown. SIGSEGV death supplied by assignment, not independently authenticated from scratch.
```

The committed forensic report says one accepted 12-seat chunk, one later refused 12-seat chunk, and another 12 without later-start evidence. Its single exact surviving accepted ID is `KaidokuR32-10.CtlC1DoNothing-6`; the other first-group identities are inferred from ordering, not preserved per-seat IDs. The supplied 06:19:06Z SIGSEGV is contextual group-cause information, not an independently authenticated local per-seat death record.

**Observed now:** these bounded statements exist in committed objects. **Not independently observed by this review:** those historical starts or any individual death. The removed raw logs were not reopened to authenticate or extend them. A SHA-256 inventory can identify bytes; it cannot authenticate their truth.

A bounded `ls-tree` at product returns empty stdout for all seven discarded raw paths (`w1-dispatch.err`, `w1-dispatch.json`, `w1-dispatched-at.txt`, `w1-payload.json`, `w1-refusals.txt`, `w1-spec.json`, `w1/swarm-registry.json`). This proves their absence from that committed tree, not their absence from every filesystem or historical object.

A targeted search over the read-only snapshots used for claims, counters, receipts and complete control reports found the old raw-log references only in the discard inventory and its forensic report. They are dispatch-uncertainty provenance, **not C1/C2 outcome receipts**. The new controls are supported by their own complete committed reports; the producer by its committed envelopes/runs/write receipt. No attempt-1 report/result was substituted.

The lesson's later correction at :53 is explicit and sufficient to identify the earlier error. Its still-unqualified introductory :3 is the remaining reporting defect. Do not convert a null-ID plan into fabricated 36 deaths, or promote the 12-start historical count to a newly authenticated measurement.

## 6. Added question: private round-17 partial-positive fixture order

**Answer: unknown from the available authorized Git evidence.** The report's **06:55–06:58Z** window crosses controls' measured **06:56:11Z** committer instant. Section 6 has no scoring-start/end UTC. It retains these command descriptions and results, verbatim variable spelling:

```text
python3 -I -B $S/c2-v3-counter.py --root $S/lane --rev 283aad7fe56d82f4ed4f8e43f099c2e1ceed5525 --fleet $S/fleet
→ ... statements=4 match=1 target=4 reverse_mismatch=0 ; exit 1

python3 -I -B $S/c2-v3-counter.py --root $S/lane --rev 1d2c9814eef3ea3f7ea95704f3670dd27ee6a66d --fleet $S/fleet
→ round-17 P2-match "row 6 anchor evidence .ufo/waves/round-17/run-carriers.sh; description words 29";
  round-27 P2-match; statements=4 match=2 target=4 reverse_mismatch=0 ; exit 1
```

The ellipsis in the first excerpt is a report summary, **not a claim of complete counter stdout**. The report itself supplies summarized results/unexpanded `$S`, not a complete per-call argv/environment/time receipt. No exact execution order can be recovered by expanding a variable or treating the broad report window as an invocation timestamp.

Input: `bb0af56c:.ufo/waves/round-32/a2audit/A2Capability17.md`, **15059 bytes**, SHA-256 `3b70cab34a04b22f4e3b5e9b8934d9755fe32a8708f96c378e048791a174fa2a`.

At 07:22:17.483303–07:22:17.498952, the exact argv below exited 0, stderr empty:

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --reverse --diff-filter=A --format=%H%x09%ct%x09%cI --name-only bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 -- .ufo/waves/round-32/a2audit/A2Capability17.md
```

Complete stdout (tabs between revision, epoch and timestamp):

```text
bb0af56c29e7b4c11d0583ed6697d0e17aba9d26	1792739183	2026-10-23T04:06:23-03:00

.ufo/waves/round-32/a2audit/A2Capability17.md
```

This dates the **report's landing**, not the private run. At 07:22:17.498977–07:22:17.500020:

```text
argv: git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -t 1d2c9814eef3ea3f7ea95704f3670dd27ee6a66d
exit: 128
stdout: ""
stderr: "fatal: git cat-file: could not get object info\n"
```

Thus the named private fixture object is not available through the lane object database for a timestamp inspection. No sibling scratch/clone was opened. Even a fixture commit timestamp would not alone establish the scoring instant unless it supplied a decisive bound.

Do **not** claim blanket pre-data ordering for every private positive fixture on this evidence. If the canonical chronology rule covers that partial positive run, the compliance question remains unresolved rather than passed. This uncertainty does not relocate production C2 repair or any C1 envelope from `bb0af56c`, and does not change the already-retained 06:47:20.941072–06:47:21.012394 C2 negative-control acceptance / honest stop.

## 7. Execution receipts and reproducibility

Existing tools: Git **2.56.0**; Python **3.14.8** (`3.14.8 (main, Oct  2 2026, 10:23:31) [GCC 16.2.1 20260810]`). **Installs/updates: none.** Operator rules were read. No pacman operation, clone, build, carrier execution, REA call, counter/selftest run, judge, or other agent/runtime was invoked.

Every audit Git subprocess uses absolute `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin`, a 30-second subprocess bound, and:

```text
GIT_DIR unset
GIT_WORK_TREE unset
GIT_INDEX_FILE unset
GIT_OPTIONAL_LOCKS=0
GIT_NO_REPLACE_OBJECTS=1
LC_ALL=C
```

The exact audit scripts and complete new machine-output bytes are named below **for L1 to commit if citing the computation**. All substantive inputs also have immutable product/freeze paths and hashes in this Report; no claim depends solely on an unavailable scratch citation. The scripts perform bounded read-only Git retrieval and report parsing; they do not import or execute lane code.

| Owned scratch artifact under `/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalCustodyOrder/` | SHA-256 | Role |
|---|---|---|
| `custody_audit.py` | `6e6cbbfa623f50c25e8a7a3db04985c405d55d81f6c8192d4f64c64854fd2087` | Complete retrieval/chronology/freeze/report audit script |
| `audit.json` | `c5bb8db1b9ad21186cd365bfbe3a096ce2829ffd57bad4a66c84a2d59f478d13` | 165270 bytes; exact child Git argv, UTC, exits, stdout/stderr, complete score blocks and structured receipts |
| `receipt_reconciliation.py` | `a77362db8985d41e18016141b2b0d663da130d19513de25191c8219db350a7ca` | Complete numeric/exit/dispatch reconciliation script; reads only the preceding JSON |
| `reconciliation.json` | `02586c550eb93c03feb8180d1fe6a68f60ff9541e8bd9f0eab7b64f5f401de70` | Complete per-row reconciliation and preserved initial/resolved structured receipts |

The cached `objects/<full-revision>/<path>` files are byte copies of named UTF-8 Git blobs, not new authorities. They need not be committed in duplicate because their source bytes already exist at the cited immutable revisions.

### Audit invocation: exact argv / exit / complete stdout

CWD `/home/vgpnk/Projects/shokunin`; completed successfully, exit 0, stderr empty:

```text
timeout --kill-after=5s 120 python3 -I -B /fast/scratch/hyaku/kaidoku-r32/a2residual/FinalCustodyOrder/custody_audit.py
```

```json
{
  "utc_start": "2026-10-23T07:14:25.003278+00:00",
  "utc_end": "2026-10-23T07:14:25.113426+00:00",
  "revision": "bb0af56c29e7b4c11d0583ed6697d0e17aba9d26",
  "script_sha256": "6e6cbbfa623f50c25e8a7a3db04985c405d55d81f6c8192d4f64c64854fd2087",
  "audit_json_sha256": "c5bb8db1b9ad21186cd365bfbe3a096ce2829ffd57bad4a66c84a2d59f478d13",
  "audit_json_bytes": 165270,
  "freeze_checks": 15,
  "freeze_mismatches": [],
  "run_order": {
    "count": 12,
    "all_after_control_commit": true,
    "first_start": "2026-10-23T06:56:33+00:00",
    "last_end": "2026-10-23T06:58:38+00:00",
    "first_start_minus_control_seconds": 22.0,
    "all_exit_zero": true
  },
  "receipt_rows": 10,
  "receipt_mismatches": []
}
```

### Reconciliation invocation: exact argv / exit / complete stdout

Same CWD; completed successfully, exit 0, stderr empty:

```text
timeout --kill-after=5s 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r32/a2residual/FinalCustodyOrder/receipt_reconciliation.py
```

```json
{
  "utc_start": "2026-10-23T07:16:39.040545+00:00",
  "utc_end": "2026-10-23T07:16:39.040998+00:00",
  "script_sha256": "a77362db8985d41e18016141b2b0d663da130d19513de25191c8219db350a7ca",
  "audit_json_sha256": "c5bb8db1b9ad21186cd365bfbe3a096ce2829ffd57bad4a66c84a2d59f478d13",
  "reconciliation_json_sha256": "02586c550eb93c03feb8180d1fe6a68f60ff9541e8bd9f0eab7b64f5f401de70",
  "all_ten_numeric_matches": true,
  "row_met_target_consistent": true,
  "initial_provider_failure_controls": [
    "A2C1Empty",
    "A2C1False",
    "A2C1NoReader",
    "A2C1Labels"
  ],
  "recorded_exit_matches_where_structured": true,
  "exit_requires_narrative_read": [
    "A2C1Garbage",
    "A2C2Garbage",
    "A2C2False",
    "A2C2Labels"
  ],
  "report_bytes_read": 533747,
  "attempt1": {
    "discard_sha256": "ca87e6dc0283d07b93961eadbbae3b3c6534f31bd237df1d8165e68e78db27fe",
    "planned_members": 36,
    "null_runtime_ids": 36,
    "all_excluded": true,
    "recorded_untrusted_start_count": 12,
    "count_limit": "Only group count and one exact runtime id preserved. Other planned24 refused/unknown. SIGSEGV death supplied by assignment, not independently authenticated from scratch.",
    "trust_boundary": "Inventory/dispatch uncertainty only; inherited scratch never used to support claimed outcomes",
    "inventory_only_files": 7,
    "removed_raw_paths_absent": true,
    "lesson_36_deaths_line": [
      3,
      53
    ],
    "lesson_corrective_lines": [
      53
    ]
  }
}
```

`lesson_36_deaths_line` is a lexical occurrence list: :53 **quotes and corrects** the old claim; it is not a second assertion of 36 deaths.

### Additional receipt-continuity measurement

At 07:21:32.718198–07:21:32.719187, exact argv:

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --exit-code --no-ext-diff --no-textconv 33393e594f1e278777fa49020b42c66ac4fa352e bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 -- .ufo/waves/round-32/controls/a2-receipts.tsv .ufo/waves/round-32/controls/a2-receipts-meta.json
```

Exit **0**; exact stdout `""`; exact stderr `""`. The adjacent first-add census (07:21:32.691887–07:21:32.718185) exited 0/stderr empty and returned the first-add mapping in §2. No failure was discarded; the private-object lookup exit 128 is preserved in §6.

## Limits and closure

Observed retained evidence is separated above from source-flow inference and unavailable historical/live observations. This audit does not authenticate the truth of author-produced receipts, independently replay REA, decide the frozen C2 claim, or grant outside admission. The main owner may preserve the named scripts/outputs when integrating this advisory evidence; no counter or predicate repair is indicated by this custody check.

All owned subprocesses were synchronous/bounded and returned. No owned service or background job was started or left running. No other seat's process tree was touched. No production edits or Git/JJ writes were made. This completes the assigned review and the added chronology question.

Report: `.ufo/waves/round-32/a2residual/FinalCustodyOrder.md`
