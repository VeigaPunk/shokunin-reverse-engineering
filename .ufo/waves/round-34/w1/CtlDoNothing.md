# CtlDoNothing — frozen empty-reader control

## Scope and axes

R34-C1, **depth**, attempt 1; axes: frozen-predicate fidelity, skip-work detection, evidence completeness, and isolation. All execution used `/fast/scratch/hyaku/kaidoku-r34/w1/CtlDoNothing`. Measured sandbox HEAD, counter-reported revision, and freeze were `54a87a51a865ab931fd355e767303337b05cccf4`. No production reader, expected-author, target binary, held item, build, or unrelated test was executed. No Git writes or tool installations/updates occurred. The only lane writes are this report and `CtlDoNothing-files/`.

## Mutant / control

A 57-byte text-only reader ignores every argument and input and always emits the canonical empty record:

```python
#!/usr/bin/env python3
print('{"schema":1,"needed":[]}')
```

Source: [CtlDoNothing-files/empty-reader.py](CtlDoNothing-files/empty-reader.py). SHA-256: `5da8f1f2bd3fde8aa55adf3ba1b571da27797a2084daa14012e3f54fd6e1dbd0`.

This is a `--control-reader` substitution, not an edit to the production reader or frozen counter.

## Expected detector — unchanged predicate

> P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.

Target remains exactly **12**, with both schedules required for each carrier. Expected: e01–e11 mismatch in both schedules; the genuinely empty e12 matches both. The production counter's private naming schedule was retained; no fixed expected-author schedule was used.

Exact exercised detector argv:

```text
/usr/bin/timeout --signal=TERM --kill-after=5s 150s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r34/w1/CtlDoNothing/tools/round-34/version-needs-counter.py --root /fast/scratch/hyaku/kaidoku-r34/w1/CtlDoNothing --rev 54a87a51a865ab931fd355e767303337b05cccf4 --freeze 54a87a51a865ab931fd355e767303337b05cccf4 --control-reader /fast/scratch/hyaku/kaidoku-r34/w1/CtlDoNothing/.ufo/waves/round-34/w1/CtlDoNothing-files/empty-reader.py
```

The capture supervisor used an outer 170-second timeout, 512 MiB address-space limit, 120 CPU seconds, a 4096-process per-UID ceiling and 128 open files. One child process tree; the counter's 24 reader invocations were sequential, each bounded to 10 seconds. Exact outer argv is retained in [probe-description.json](CtlDoNothing-files/probe-description.json); the evidence-capture source is retained unchanged.

## Actual output

Observed UTC: **2026-10-23T10:54:32.276972+00:00 → 2026-10-23T10:54:33.285311+00:00**.

```json
{"mode":"control","matched":1,"target":12,"met_target":false,"documents_ok":true,"finding":"version_needs_mismatch"}
```

Counter exit: **1**. Counter stderr: empty. All 24 control invocations exited **0**, returned `{"schema":1,"needed":[]}`, and had empty stderr. e01–e11 failed equality in both schedules; only e12 matched both. All seven document/source/table checks were `true`, including the two frozen documents, approved SKILL section, S103/S104 rows, and both source captures. Thus rejection was caused by the unchanged record-equality predicate, **not an absent document or execution/JSON error**.

Complete, unabridged output and exit are retained in [counter.stdout.json](CtlDoNothing-files/counter.stdout.json), [counter.stderr.txt](CtlDoNothing-files/counter.stderr.txt), [counter.exit.txt](CtlDoNothing-files/counter.exit.txt), and [run-receipt.json](CtlDoNothing-files/run-receipt.json). The full JSON includes all 24 input hashes and naming translations. Stdout SHA-256: `6bfed3ac13f5b56f34db5a19a11e65b2441770b19fb055dfa39e10b55c2a6aa9`.

## Verdict

**Skip-work control rejected: 1/12; target not met.** No predicate, target, expected records, or source bindings were amended. This result does not establish a production-reader pass or authorize claim admission.

Baseline-relative mutation classification: **inconclusive / no killed-mutant claim**. This assignment authorized the empty control only and prohibited production-reader data production. Consequently no pristine or restored production-reader run was performed; there was no in-place source mutation to restore. The observed control rejection itself is complete, not an inferred mutation kill.

## Restoration and retained evidence

Before/after snapshots cover the control, counter, all four instrument pins, manifest, frozen carrier originals, documents, source captures, SKILL.md and corpus/SOURCES.md. Every recorded size/hash pair is equal before and after; every declared pin matched both snapshots. No restoration write was necessary. The capture observed no remaining child process group requiring cleanup.

| Bytes | Before and after SHA-256 |
|---|---|
| Frozen counter | `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e` |
| Frozen manifest | `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d` |
| Production reader, statically hashed only | `ac7d24a546022c7cc8295450a2692c51c07099e42a1aa02fb69c29455dae3f33` |
| Empty control | `5da8f1f2bd3fde8aa55adf3ba1b571da27797a2084daa14012e3f54fd6e1dbd0` |

[restoration.json](CtlDoNothing-files/restoration.json), [before-hashes.json](CtlDoNothing-files/before-hashes.json), and [after-hashes.json](CtlDoNothing-files/after-hashes.json) contain the complete measured hashes. Reader/capture/counter source, frozen claims and manifest bytes, summary, exact stdout/stderr/exit and receipt are archived; [archive-manifest.json](CtlDoNothing-files/archive-manifest.json) records their byte sizes and hashes. Large raw-reader responses required paged archival reconstruction; the reconstructed manifest matches its frozen byte size and SHA-256, and archived stdout matches its capture hash. The detector was exercised once, not rerun during archival recovery.

Visible answering-model context: `openai-codex/gpt-6.1-sol`; no safety refusal, routing switch, or quota fallback was observed.

Report: .ufo/waves/round-34/w1/CtlDoNothing.md
