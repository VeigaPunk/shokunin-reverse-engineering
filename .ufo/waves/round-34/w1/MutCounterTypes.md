# MutCounterTypes — frozen outer-fixture probe

## Result

**37 text-only cases; 111 detector invocations: 29 mutants killed, six fixture-envelope type challenges survived, two positive controls passed. No inconclusive baseline.** Every case ran pristine → one-file mutation → exact-byte restoration using the same frozen outer CLI. All 37 pristine and all 37 restored runs exited 0 with boolean `met_target: true`.

The six survivors are isolated fixture-interface acceptance/type-conflation findings, **not a production P34 score, target-met skip-work control, or R34-C1 admission judgment**. No malformed reader-output mutant survived. The fixture-envelope strict-type expectation is the probe's challenge, not a new restriction added to the frozen predicate. No counter repair was made.

Axes: duplicate JSON keys; bool/int and scalar-type separation; array order and row uniqueness; reader exit status.

## Frozen boundary and execution

- Sandbox, measured revision and freeze: `/fast/scratch/hyaku/kaidoku-r34/w1/MutCounterTypes`, `54a87a51a865ab931fd355e767303337b05cccf4`.
- UTC: `2026-10-23T10:55:35.760922+00:00` through `2026-10-23T10:55:43.264316+00:00`.
- Only `--fixture-spec` / `--fixture-reader` was exercised. The input was exactly `benign text fixture only\n`; fake readers printed small JSON constants. The rich baseline has sorted `libA`/`libB` rows and three version rows. No ELF was authored, read as probe input, or executed. No production reader invocation/import, REA run, held-item reconstruction, or production scoring occurred.
- One child process tree at a time; 512 MiB address-space limit; 5-second detector timeout plus 1-second kill grace, 8-second communication cap; 150-second enclosing timeout. All runs completed without timeout. No background jobs or remaining started child trees.
- Visible answering model: `openai-codex/gpt-6.1-sol`. Existing Python 3.14.8 and GNU timeout 9.12; no installations/updates or routing changes.

Frozen predicate, verbatim:

> P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.

The detector's fixture-mode predicate was exactly `isolated comparator fixture; not a P34 production score`. The fixture target was one; the frozen production target remains twelve. Fixture rows had no string-table challenge, so both schedules deliberately received the same tiny text bytes; this probe makes no randomized-naming claim.

## Detector and expected behavior

Launch, from the sandbox:

```sh
/usr/bin/timeout --signal=TERM --kill-after=2s 150s /usr/bin/python3 -I -B .ufo/waves/round-34/mut-counter-types/probe.py
```

Every pristine/mutated/restored detector used this exact argv (fully expanded strings are also retained in every `run.json`):

```sh
/usr/bin/timeout --signal=TERM --kill-after=1s 5s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r34/w1/MutCounterTypes/tools/round-34/version-needs-counter.py --root /fast/scratch/hyaku/kaidoku-r34/w1/MutCounterTypes --rev 54a87a51a865ab931fd355e767303337b05cccf4 --freeze 54a87a51a865ab931fd355e767303337b05cccf4 --fixture-spec /fast/scratch/hyaku/kaidoku-r34/w1/MutCounterTypes/.ufo/waves/round-34/mut-counter-types/active/spec.json --fixture-reader /fast/scratch/hyaku/kaidoku-r34/w1/MutCounterTypes/.ufo/waves/round-34/mut-counter-types/active/reader.py
```

Expected detector: valid baseline succeeds; malformed output is rejected with exit 1; duplicate/invalid outer fixture records are rejected with exit 2; valid object-key reordering and stderr-only diagnostics remain accepted. The envelope type challenges asked whether non-integer schema/target and non-boolean document status were rejected; they did not prescribe an existing diagnostic for unimplemented envelope checks.

## Observed outputs and verdicts

| Mutation family | Cases | Mutated detector exit / observed result | Verdict |
|---|---:|---|---|
| Output duplicate schema (equal and conflicting), needed, file, versions, hash keys; conflicting cases end with the correct value | 6 | 1; `matched: 0`, `met_target: false`, `version_needs_mismatch`; both attempts report `reader_json` / `duplicate_json_key:<key>` | Killed |
| Outer duplicate target, manifest schema, expected hash | 3 | 2; `met_target: false`; `duplicate_json_key:target`, `:schema`, `:hash` respectively | Killed |
| Output schema=true, flags=false, other=true, hash=true | 4 | 1; `matched: 0`, `met_target: false`, `version_needs_mismatch` | Killed |
| Output schema=1.0, flags=0.0, other=1.0, hash=1.0 | 4 | 1; same mismatch | Killed |
| Needed order reversed, version order reversed, exact duplicate needed row, duplicate file with different versions, exact duplicate version, duplicate (name, other) with different hash | 6 | 1; same mismatch | Killed |
| Correct JSON followed by reader exit 1, 2, 7, or 255 | 4 | Outer exit 1; both attempts retain the actual nonzero reader exit, `observed: null`, `matched: false`; outer `matched: 0` | Killed |
| Expected-record schema=true; carrier size=true | 2 | 2; `manifest_row_schema`, `met_target: false` | Killed |
| Recursive JSON object-key order changes; correct JSON plus `TEXT_PROBE_STDERR` on stderr | 2 | 0; `matched: 1`, boolean `met_target: true` | Positive controls passed |

### Six surviving fixture-envelope type challenges

Each changed only `spec.json`; the reader, input, exact expected records, and two schedule matches remained unchanged. All six emitted `version_needs_match`, `matched: 1`, and exited 0. Outer stderr was empty.

| Case | Changed value | Observed `met_target` |
|---|---|---|
| `spec-manifest-schema-boolean` | manifest schema `1` → `true` | boolean `true` |
| `spec-manifest-schema-float` | manifest schema `1` → `1.0` | boolean `true` |
| `spec-target-boolean` | fixture target `1` → `true` | boolean `true` |
| `spec-target-float` | fixture target `1` → `1.0` | boolean `true` |
| `spec-documents-integer` | documents_ok `true` → `1` | integer `1` |
| `spec-documents-string-false` | documents_ok `true` → string `"false"` | string `"false"` |

The last case literally returned `"documents_ok": "false", "finding": "version_needs_match", "matched": 1, "met_target": "false"` with exit 0. This is a fixture-only false accept against strict boolean document-status handling; string `"false"` is not JSON boolean `false`.

Source explanation: frozen counter lines 141–154 use equality for manifest schema, while lines 137–139 compare count/target by numeric equality and propagate document truthiness. `fixture_measure` (222–226) passes fixture target/documents through unchanged. In production, `measure` supplies literal target 12 and computes document status with `all(...)`, and the manifest is frozen and digest-pinned. These fixture observations do not demonstrate a production bypass. Canonical reader records independently enforce exact integer types (35, 48) and sorted/unique arrays (53–55); the exercised output challenges were rejected.

## Restoration and evidence

Counter, claims and manifest were never mutated. Before and after SHA-256 were identical, and the probe recorded direct byte equality:

| File | Before = after SHA-256 |
|---|---|
| `tools/round-34/version-needs-counter.py` | `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e` |
| `.ufo/waves/round-34/claims.json` | `bb971710cb17ef775227cceb1b7024b7380e859564a28648709dd1c786a997a4` |
| `.ufo/waves/round-34/expected.json` | `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d` |

Pristine = restored fixture SHA-256 in every case and at final return:

- `input.txt`: `bdaf7d1080cbe1f04982885b304526945b4da685c0a4f4158ea3ba956a8b6548`
- `spec.json`: `0bc00c6e2f5170db633f63b63c7e0a0625e034754dc3cc278923c652ada94109`
- `reader.py`: `a701490b83e1fb2d96eff0185b41bb053e29c469a7cf99e076d07c727f969c88`

Evidence: [launch receipt](MutCounterTypes-files/launch.json), [complete probe receipts](MutCounterTypes-files/probe-receipts.tar.gz). Archive SHA-256: `57573261dfbe0b639501326b8f4e632d648c236451e2a8dda34b9fe4df67578e`.

Archive contains the exact probe and frozen counter bytes, frozen claims, revision receipt, baseline, restored active fixtures, and `summary.json` with all 37 case verdicts and pristine/mutated/restored hashes. For every one of the 111 runs, `receipts/<case>/<pristine|mutated|restored>/` retains exact `input.txt`, `spec.json`, `reader.py`, complete `stdout.txt`, complete `stderr.txt`, and `run.json` with exact argv, UTC, exit, parsed output and hashes. These are retained evidence, not proposed production fixtures. No frozen rule was changed and no further probe was run after this assigned batch.

Report: .ufo/waves/round-34/w1/MutCounterTypes.md
