# MutNameTransform — randomized string-table mutation probe

## Result and scope

**Mutant killed; exact restoration completed.** On the pristine and restored counter, the byte-reading ASCII/NUL text control matched both schedules; the original-content-hash replay matched only schedule 0 and failed schedule 1. Removing one post-transformation sorting statement made the same detector fail only the byte control's transformed schedule. No production reader or ELF input was run or authored.

- Claim axis: **depth**, not coverage. Probe axes: suffix/offset fidelity, canonical ordering, recorded-field preservation, replay discrimination, and isolation/restoration.
- Sandbox: `/fast/scratch/hyaku/kaidoku-r34/w1/MutNameTransform`.
- Measured and freeze revision: `54a87a51a865ab931fd355e767303337b05cccf4`; counter digest matched the frozen instruments from `8897a67f6074580d6eac1a3fc0e37fdcd7aa0df0`.
- Visible answering model: `openai-codex/gpt-6.1-sol`. No model/runtime rerouting, refusal, fallback, tool installation, or update occurred. Python observed: 3.14.8.
- This is an isolated comparator fixture with `target: 1`, explicitly labelled by the counter as **not a P34 production score**. The frozen production target remains exactly 12. No production claim verdict or admission decision is made.

Frozen predicate, verbatim:

> P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.

## Fixture and controls

`MutNameTransform-files/fixture.txt` is **1,769 bytes**, exclusively ASCII bytes and NUL delimiters, SHA256 `67324d55926f2b2ff5ae16bf6de19807c3196ed8240f1c61ae54cae6dc418b2e`. It has an ASCII metadata header, a 195-byte string table at offset 1565, and an unchanged ASCII trailer. There is no ELF header, executable payload, or production-carrier reconstruction.

The table contains `p<c>\0` for every one of the counter's 65 alphabet characters, in ASCII order. Its 65 file names use slot starts; its 65 version names use offsets one byte inside those same slots. Thus every version name is genuinely suffix-shared rather than separately stored. One file record has all 65 versions; the remaining 64 have empty version lists. Recorded flags, indices, and deliberately independent unsigned hash values are ASCII metadata outside the translated table.

- `byte_reader.py` reads only the supplied text bytes, follows these offsets, reads the recorded scalar fields, and sorts the resulting file/version lists. It contains no original-name or original-input-hash lookup.
- `original_hash_replay.py` performs only a lookup by the original text fixture's SHA256. It emits the frozen text answer for that hash and an empty answer for any other hash. It does not decode names.
- The actual counter's unseeded `secrets`/Sattolo transformation ran unchanged. No deterministic schedule or expected-author schedule was substituted. Each invocation retained its actual translation, input hash, observed answer, and corresponding translated text bytes.

Using every alphabet character guarantees file and version ordering reversals for every allowed nonidentity permutation: an increasing bijection of the entire finite ordered alphabet would have to be the identity. The result does not depend on a lucky random reversal.

## One plausible defect and expected detector

In sandbox `tools/round-34/version-needs-counter.py`, delete only original line 103:

```python
    prediction["needed"].sort(key=lambda record: record["file"])
```

Defect: renamed expected file records retain their old order instead of canonical order. Version sorting, byte translation, and scalar fields remain untouched.

Expected detector: pristine/restored text byte reader succeeds on both schedules, while hash replay fails after translation. With this one-line omission, the byte reader still emits the correctly sorted, byte-derived transformed answer, but the counter compares it with an unsorted prediction and reports a mismatch. A failing pristine baseline would be inconclusive; the observed pristine baseline passed.

## Actual bounded outputs

All times below are observed UTC on 2026-10-23. Each counter invocation had two reader child runs, all exiting **0**. Every captured counter stderr was empty. No timeout or parser crash caused the mutation kill.

| Counter bytes | Byte control started | Byte counter exit / finding | Byte schedules 0,1 | Hash-replay counter exit / schedules | Detector exit |
|---|---|---|---|---|---|
| pristine | 10:56:44.460709Z | 0 / `version_needs_match`, matched 1/1 | true, true | 1 / true, false; matched 0/1 | 0 |
| mutated | 10:56:57.220939Z | 1 / `version_needs_mismatch`, matched 0/1 | true, false | 1 / true, false; matched 0/1 | 1 |
| restored | 10:57:04.952904Z | 0 / `version_needs_match`, matched 1/1 | true, true | 1 / true, false; matched 0/1 | 0 |

For all three byte-control runs, the independent receipts recorded: all 65 alphabet bytes changed bijectively; all other byte mappings were identity; total length and outside-table bytes stayed unchanged; all suffix aliases survived; both sorting reversals were present; observed output equalled the independently translated/sorted expectation; and all 65 recorded `(other, hash, flags)` associations were preserved. Retained translated text hashes matched the counter's input hashes. The mutant's byte-derived output passed those independent checks despite the counter mismatch.

The original-hash replay's schedule-1 input hash differed from its lookup key in every phase; it emitted the expected empty miss. Its empty transformed output naturally fails the translation/scalar-preservation audits, rather than being counted as an independent positive control.

**Mutation verdict: killed**, with passing pristine and restored behavioral baselines. No surviving mutant or inconclusive baseline was observed in this single assigned probe.

## Exact execution and evidence

Working directory for every command:

```text
/fast/scratch/hyaku/kaidoku-r34/w1/MutNameTransform
```

Setup, once:

```sh
timeout --signal=TERM --kill-after=2s 20s prlimit --as=536870912 --nproc=4096 --cpu=10 python3 -I -B .ufo/waves/round-34/w1/MutNameTransform-files/prepare.py
```

The same detector command was run in this exact order, with the one-line deletion/restoration between commands:

```sh
timeout --signal=TERM --kill-after=2s 70s prlimit --as=536870912 --nproc=4096 --cpu=25 python3 -I -B .ufo/waves/round-34/w1/MutNameTransform-files/detector.py pristine
timeout --signal=TERM --kill-after=2s 70s prlimit --as=536870912 --nproc=4096 --cpu=25 python3 -I -B .ufo/waves/round-34/w1/MutNameTransform-files/detector.py mutated
timeout --signal=TERM --kill-after=2s 70s prlimit --as=536870912 --nproc=4096 --cpu=25 python3 -I -B .ufo/waves/round-34/w1/MutNameTransform-files/detector.py restored
```

The phase receipts retain each exact nested argv, UTC start/end, exit, stdout, stderr, translation, and input hash. Nested counter commands used `--fixture-spec` and `--fixture-reader`; they also explicitly carried `--root` pointing at this sandbox and both `--rev` and `--freeze` equal to the frozen revision. Each was wrapped with `timeout ... 25s prlimit --as=536870912 --nproc=4096 --cpu=20`. Probes were sequential, one child process tree at a time, with no background jobs or delegates.

Evidence sealing, without another reader invocation:

```sh
timeout --signal=TERM --kill-after=2s 15s prlimit --as=536870912 --nproc=4096 --cpu=10 python3 -I -B .ufo/waves/round-34/w1/MutNameTransform-files/archive.py
```

Archival directory: `.ufo/waves/round-34/w1/MutNameTransform-files/`.

- `setup.json`: measured revision, fixture sizes/offsets/hashes, tool version, and Git-read argv/output.
- `pristine.json`, `mutated.json`, `restored.json`: full counter stdout/stderr/exit/argv and independent checks.
- `<phase>.<byte|replay>.stdout.json` / `.stderr.txt`: exact raw counter streams.
- `<phase>.<byte|replay>.schedule1.txt`: exact translated text fixture bytes retained from the logged mapping, checked against the actual input hash.
- `counter.pristine.py`, `counter.<phase>.snapshot.py`, `mutation.patch`: exact code bytes and the single changed statement.
- `prepare.py`, `detector.py`, both fake readers, `fixture.txt`, `spec.json`, and `expected.json`: complete text-only reproducer. This archival `expected.json` is the tiny fixture oracle, **not** the frozen production manifest.
- `archive-receipt.json`: 35 archived files / 272,808 bytes, per-file SHA256 and exact source/archive byte equality, sealed at 10:58:32.715961Z.

## Restoration evidence

| State | Counter bytes | SHA256 |
|---|---:|---|
| before | 17,275 | `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e` |
| mutated | 17,210 | `e9211b4587f8d4e44c96ebcc5d0801b7f7230e410e49f1343776a0c08b8df3af` |
| restored | 17,275 | `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e` |

Archival sealing compared the saved pristine bytes, restored snapshot, and current sandbox counter **byte-for-byte equal**, not merely equal filenames or revision labels. The restored detector then has the same passing result as pristine. No Git writes, commits, pushes, production edits, or other-seat edits occurred. Production writes were only this report and its named archival directory. No child trees remain from these synchronous completed probes.

## Counter limits

1. The fixture entry point validates a synthetic manifest and uses synthetic `documents_ok: true`; it does **not** exercise the frozen twelve-carrier score, actual source/table bindings, production instrument-pin checks, ELF offsets, or the proposed reader. No full R34-C1 target-met control or production score was measured.
2. A mutated executable counter would fail `running_counter_pin` in production. This probe intentionally used the isolated fixture entry point to test behavioral sensitivity rather than claiming a trivial digest-pin kill.
3. Translation is one global substitution over exactly 65 characters. It preserves offsets, suffix sharing, string lengths, and repeated-character structure; nonalphabet bytes remain unchanged. Rejection of this original-whole-file-hash replay does not establish rejection of every content recognizer or skip-work strategy.
4. Only the missing file re-sort was mutated. Version re-sorting and recorded-hash preservation were exercised positively, but were not independently mutation-tested here.
5. Recorded hashes remain raw recorded values despite renamed strings; this does not establish loader validity, authenticity, execution behavior, or any vulnerability. The empty-carrier limitation described by the frozen claim was not exercised by this nonempty text fixture.

Report: .ufo/waves/round-34/w1/MutNameTransform.md
