# CtlJunk — pre-data wrong-structure control

## Result

**Control miss: 0/12, `met_target=false`, exit 1, `version_needs_mismatch`.** The junk control completed normally and was not accepted. No production-reader score was run.

**Mutation-test verdict: inconclusive, not killed.** The pristine empty-output control already fails the full twelve-carrier predicate (1/12). Its failure cannot establish a killed mutant. Restoring its exact bytes restored the same 1/12 outcome.

Axes: structural discrimination; frozen source/table binding; reproducible evidence; containment. Claim axis remains **depth**, not coverage.

## Frozen contract

Predicate, verbatim:

> P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.

- Freeze and measured revision, all three runs: `54a87a51a865ab931fd355e767303337b05cccf4`.
- Sandbox root: `/fast/scratch/hyaku/kaidoku-r34/w1/CtlJunk`.
- Frozen counter SHA-256, unchanged before/after every run: `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e`.
- Frozen manifest SHA-256: `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d`.
- Frozen claims SHA-256: `bb971710cb17ef775227cceb1b7024b7380e859564a28648709dd1c786a997a4`.
- Every output reports `mode=control`, target 12 and `documents_ok=true`.

## Mutant and expected detector

One behavior-bearing point changed: line 3 of an isolated, text-only control reader. The pristine output was `{"schema":1,"needed":[]}`. The mutation replaced that empty array with a plausible but wrongly structured file/version object. The exact exercised junk source is archived as `CtlJunk-files/mutated.reader.py`:

```python
#!/usr/bin/env python3
"""Text-only skip-work control: never reads or executes its supplied input."""
print('{"schema":1,"needed":{"file":"libc.so.6","versions":["GLIBC_2.34","GLIBC_2.2.5"]}}')
```

The reader neither opens its opaque input nor invokes another program. File/version words alone must not satisfy the contract. In the frozen counter, `canonical` requires `needed` to be a list (lines 35–38), then exact typed record fields and exact expected-record equality (lines 40–55, 127–128). This output instead supplies an object and version-name strings. Expected result: no carrier matches and the target remains unmet.

## Exact invocation and bounds

The same detector argv was exercised on pristine, mutated and restored bytes at the same control-reader path:

```sh
/usr/bin/timeout --signal=TERM --kill-after=5s 150s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r34/w1/CtlJunk/tools/round-34/version-needs-counter.py --root /fast/scratch/hyaku/kaidoku-r34/w1/CtlJunk --rev 54a87a51a865ab931fd355e767303337b05cccf4 --freeze 54a87a51a865ab931fd355e767303337b05cccf4 --control-reader /fast/scratch/hyaku/kaidoku-r34/w1/CtlJunk/.ufo/waves/round-34/w1/CtlJunk-files/control_reader.py
```

Each was launched sequentially by the retained recorder, using the following exact outer command with respectively `pristine`, `mutated`, and `restored` as its final argv element:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --signal=TERM --kill-after=5s 180s python3 -I -B /fast/scratch/hyaku/kaidoku-r34/w1/CtlJunk/.ufo/waves/round-34/w1/CtlJunk-files/run_probe.py pristine
```

Each phase receipt retains its fully expanded `launch_argv`, `detector_argv`, `counter_argv`, cwd, UTC interval, exit, stream hashes and source hashes. The recorder removes inherited `GIT_*`/`PYTHON*` variables and supplies `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `LC_ALL=C`.

Bounds: one detector tree at a time; 150-second detector timeout inside a 180-second launch timeout; 512 MiB address space, 90 CPU seconds, UID process ceiling 4096, 128 file descriptors, 16 MiB output-file limit, no core files. No timeout occurred. At recorder cleanup each detector process group was already gone; no remaining group needed killing. The recorder exits 0 after preserving the detector's actual exit 1; these are not target-pass exits.

## Observed outputs

| Bytes exercised | Observed UTC start → end | Counter exit | Matched carriers | Matched schedules |
|---|---|---:|---:|---:|
| Pristine | 2026-10-23T10:54:35.699491+00:00 → 10:54:36.722485+00:00 | 1 | 1/12 (e12 only) | 2/24 |
| Mutated junk | 2026-10-23T10:54:47.092726+00:00 → 10:54:47.640446+00:00 | 1 | 0/12 | 0/24 |
| Restored | 2026-10-23T10:54:56.843766+00:00 → 10:54:57.220939+00:00 | 1 | 1/12 (e12 only) | 2/24 |

All three: `finding=version_needs_mismatch`, `met_target=false`, `documents_ok=true`, empty counter stderr. Each exercised 24 schedules, including eleven nonempty second-schedule name translations; e12 repeated its empty case.

For the junk run, **all 24 reader children exited 0 with empty stderr**, and all decoded observations were precisely the wrong-structure object above. Their common stdout SHA-256 was `75623497ef0f5fbeb9e8b32517a1bc6f142e6be108bc6278bc949e15935fa4e6`. Thus the observed rejection was not a child crash or missing JSON response.

Complete, unabridged counter stdout/stderr bytes are retained in `CtlJunk-files/{pristine,mutated,restored}.stdout.json` and `.stderr.txt`. Counter stdout hashes:

- Pristine: `af65dfb4c21ec1a618b7535653e6caa672d16b4ed4439d9cc7e62d77ec2da287` (14,512 bytes).
- Mutated: `c8323863c33b04bc1090ed565e0d59330150d5c8f2b4711d5779a5ca4c3994e5` (16,003 bytes).
- Restored: `e4a33dd1ff45c267ff72c73875b995549eaeaf42ff06b30c3fa51caa5f16a093` (14,512 bytes).
- Every counter stderr: zero bytes, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Fresh randomized schedules mean pristine/restored full stdout need not be byte-identical; the reader bytes and carrier outcomes were restored, not the random schedule.

## Restoration and evidence

Reader-source SHA-256:

- Before mutation: `229440f69e49cd2d11be33cd1a70b6b465ed00d235767b4be440fe8d6f961bc5`.
- Mutated: `8802ca8ef4ba105a54b5b6062f5636880a856fe8a38fc7988d57886ebc3386a6`.
- Restored and final working control: `229440f69e49cd2d11be33cd1a70b6b465ed00d235767b4be440fe8d6f961bc5`.

`CtlJunk-files/restoration.json` records exact byte equality for pristine/restored snapshots and for the final working reader against pristine. Each phase additionally records matching before/after reader hashes. The counter remained unchanged throughout.

`CtlJunk-files/` retains the three reader snapshots, working restored reader, recorder source, single-line `mutation.patch`, all three exact stream/receipt sets, restoration receipt, frozen counter/claims/manifest bytes, and the sandbox-only LOG entry. `artifact-manifest.json` records source/archive hashes and exact byte equality for all 20 archived files (165,571 bytes excluding the manifest itself).

## Scope and limits

- Production-lane writes were confined to this report and `CtlJunk-files/`. The only tracked sandbox edit outside receipts was the required sandbox-only `LOG.md` entry; no production LOG was changed.
- No production reader, REA runtime, target binary, held item or excluded builder was executed. No binary fixtures were authored; only the frozen counter's assigned static naming challenge ran.
- No Git writes, commits, pushes, delegates, background jobs or routing/configuration changes.
- No builds, formatters, general selftests or additional mutation probes. This result is a bounded skip-work control, not a production score, authenticity claim or admission judgment.
- Existing Python: 3.14.8. Tool installs/updates: **none**.
- Visible answering model: `openai-codex/gpt-6.1-sol`. No safety refusal or model switch observed.

Report: `.ufo/waves/round-34/w1/CtlJunk.md`
