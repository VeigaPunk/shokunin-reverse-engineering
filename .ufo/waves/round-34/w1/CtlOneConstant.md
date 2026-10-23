# CtlOneConstant — frequency-selected no-reader control

## Result

**The constant control was rejected: 1/12 carriers, `met_target=false`, counter exit 1, `version_needs_mismatch`; documents/source bindings were valid.** Only e12 matched both schedules. No proposed/production reader was run. This is a pre-data control result, not claim admission or a production score.

Axes: frozen-record frequency; exact canonical output; both-schedule discrimination; byte restoration and evidence fidelity. The task's assessed axis remains **depth**, not coverage.

Freeze and measured revision: `54a87a51a865ab931fd355e767303337b05cccf4`. All commands ran in `/fast/scratch/hyaku/kaidoku-r34/w1/CtlOneConstant`; `GIT_*` and `PYTHON*` variables were removed from child environments. The sandbox HEAD was observed at that revision. Production received only this report and its named evidence directory.

## Frozen predicate, unchanged

> P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.

Target remains exactly 12. No acceptance rule was amended after observing results.

## Frequency command and selected constant

The frozen JSON manifest alone supplied expected records; no ELF parser or expected-author program was invoked. The retained command was:

```sh
git --no-replace-objects -c core.fsmonitor=false show 54a87a51a865ab931fd355e767303337b05cccf4:.ufo/waves/round-34/expected.json | jq -cS '.carriers[].expected' | sort | uniq -c | sort -k1,1nr -k2,2
```

This ran under `LC_ALL=C`, `timeout --kill-after=5s 30s`, and `prlimit --as=536870912 --nproc=8192 --cpu=25`; the full argv is in `frequency.receipt.json`. Observed UTC: `2026-10-23T10:54:07.679143+00:00` through `2026-10-23T10:54:07.692963+00:00`; exit 0, empty stderr.

**There is no record shared by two rows. All twelve canonical records are distinct, each frequency 1.** The command's count-descending, canonical-JSON-ascending tie-break therefore selects e12's `{"needed":[],"schema":1}`. This is one of twelve tied maxima, not a unique majority. `frequency.stdout` retains the complete twelve-record frequency output; `frequency-summary.json` retains every frequency and canonical-record digest. Frequency stdout SHA-256: `89825395df21faa0f0e6ea589a9f0435be8aa9cd04ec8ad9fba890add1f5eca9`.

The exercised no-reader control is exactly:

```python
#!/usr/bin/env python3
# Frequency-selected canonical record; intentionally ignores argv and all input bytes.
print('{"needed":[],"schema":1}')
```

Control source SHA-256: `98592ca14ecd64b695012369e0a7bcb5c4bfca7a8942db7682270b851451996a`.

## Frozen counter result and every schedule

Exact detector argv, also retained as an array in `control.receipt.json`:

```sh
/usr/bin/timeout --kill-after=5s 160s /usr/bin/prlimit --as=536870912 --nproc=8192 --cpu=120 -- /usr/bin/python3 -I -B tools/round-34/version-needs-counter.py --root /fast/scratch/hyaku/kaidoku-r34/w1/CtlOneConstant --rev 54a87a51a865ab931fd355e767303337b05cccf4 --freeze 54a87a51a865ab931fd355e767303337b05cccf4 --control-reader /fast/scratch/hyaku/kaidoku-r34/w1/CtlOneConstant/.ufo/waves/round-34/w1/CtlOneConstant-files/constant-reader.py
```

Observed UTC: `2026-10-23T10:55:42.549434+00:00` through `2026-10-23T10:55:42.963847+00:00`. Counter stdout/stderr and exit are retained in `control.stdout`, `control.stderr`, and `control.receipt.json`. Counter stderr was empty. Stdout SHA-256: `ba9e8cbef34df675415e38659990c73786eeb7d44717933b5e73c2c1e1b05994`.

| Carrier | Schedule 0 matched / exit | Schedule 1 matched / exit | Both |
|---|---|---|---|
| e01 | false / 0 | false / 0 | false |
| e02 | false / 0 | false / 0 | false |
| e03 | false / 0 | false / 0 | false |
| e04 | false / 0 | false / 0 | false |
| e05 | false / 0 | false / 0 | false |
| e06 | false / 0 | false / 0 | false |
| e07 | false / 0 | false / 0 | false |
| e08 | false / 0 | false / 0 | false |
| e09 | false / 0 | false / 0 | false |
| e10 | false / 0 | false / 0 | false |
| e11 | false / 0 | false / 0 | false |
| e12 | true / 0 | true / 0 | true |

All 24 attempts observed `{"needed":[],"schema":1}`, with empty stderr and stdout SHA-256 `072fa4dbd2b38317947743fbebe6192492e2126989d98b382d5762d44209920c`. e01–e11 received the counter's fresh schedule-1 translations; e12 correctly had no string table/translation and repeated its empty expectation. `all-schedules.json` preserves each observed record, exit, stderr, input/output hash, and full translation. No fixed expected-author schedule was substituted.

## One-point mutation lifecycle — separate fake-TEXT diagnostic

To satisfy pristine/mutated/restored evidence without running the prohibited production reader, the same frozen counter's **isolated fixture mode** was exercised with one 11-byte ASCII fixture, `libA|VER_1\n`. This diagnostic has a one-row fixture target and is explicitly **not** a P34 score or a replacement for the twelve-row target above.

Pristine fake TEXT reader calls `read_text_fixture()`; the sole mutation replaces that call in the output expression with `{'needed': [], 'schema': 1}`. The mutant no longer reads its input and emits the exact same canonical constant as the assigned control. The call was restored immediately after the mutated probe.

Identical detector argv in all three stages:

```sh
/usr/bin/timeout --kill-after=5s 30s /usr/bin/prlimit --as=536870912 --nproc=8192 --cpu=25 -- /usr/bin/python3 -I -B tools/round-34/version-needs-counter.py --fixture-spec /fast/scratch/hyaku/kaidoku-r34/w1/CtlOneConstant/.ufo/waves/round-34/w1/CtlOneConstant-files/text-spec.json --fixture-reader /fast/scratch/hyaku/kaidoku-r34/w1/CtlOneConstant/.ufo/waves/round-34/w1/CtlOneConstant-files/text-reader.py
```

| Stage | Observed UTC interval | Detector exit | Both schedules matched | Finding |
|---|---|---:|---|---|
| Pristine | 10:56:35.818103–10:56:35.890406, 2026-10-23 UTC | 0 | true | version_needs_match |
| Mutated | 10:56:47.145171–10:56:47.233431, 2026-10-23 UTC | 1 | false | version_needs_mismatch |
| Restored | 10:56:54.411520–10:56:54.498317, 2026-10-23 UTC | 0 | true | version_needs_match |

All six fake reader executions exited 0 with empty stderr. Expected detector: accept input-derived named record; reject constant empty record. **Verdict: killed on this isolated TEXT fixture**, with passing pristine and restored baselines. This does not imply a production-parser mutation was tested.

Reader SHA-256 before mutation and after exact restoration: `fbcb85a4a3fdb5b93a6a8c15887a6f6525e0ce0ff6d0553c1313c197cc7ea118`; mutant: `d4ddc8e626351d2187d38f64b04c42dcb22fd24a43223585da137a04bbdf63b9`. Pristine and restored counter stdout were byte-identical, SHA-256 `038d8d73278d654034b94928d046de5ccbb1672e00453baec180b100e66f52cb`. Source snapshots and all three argv/UTC/stdout/stderr/exit receipts are retained.

## Source preservation, containment, and limitations

`before-sha256.json` and `after-sha256.json` are equal; `changed_paths=[]`. No frozen instrument, manifest, public carrier, pinned source, table, or skill bytes were edited. Relevant unchanged digests:

- Manifest: `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d`.
- Counter: `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e`.
- Proposed reader (hashed only, never executed/imported): `ac7d24a546022c7cc8295450a2692c51c07099e42a1aa02fb69c29455dae3f33`.

An initial frequency wrapper failed before spawning its command because a per-uid process cap of 64 was below existing occupancy (359 processes observed afterward). This is retained as an infrastructure failure, not a detector result; its exact UTC was not captured. A thread-count query used an unsupported `ps -L` option and is not admitted as a measurement. The successful probes used a bounded cap of 8192, one child tree at a time, 512 MiB address-space limits, and finite timeouts. No background services/jobs were started. No binary fixture was authored or target binary executed. No held item, REA, delegation, routing change, Git write, push, build, formatter, or unrelated test was used. No tools were installed or updated. Visible answering model: `openai-codex/gpt-6.1-sol`; no safety refusal or fallback was encountered.

Evidence directory: `.ufo/waves/round-34/w1/CtlOneConstant-files/` (frequency command/output, full control and schedule receipts, text fixture/code bytes and restoration receipts, frozen textual instrument/manifest snapshots, and infrastructure notes).

Report: .ufo/waves/round-34/w1/CtlOneConstant.md
