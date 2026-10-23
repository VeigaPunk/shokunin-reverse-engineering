# MutCounterPins — isolated counter-fixture mutation probe

## Result

**48 killed input mutants; 0 survived; 0 inconclusive.** This is a text-only counter-validation result, **not a P34 production score or evidence admission**. Each case changes one fixture field, record/list value, or carrier byte sequence; frozen instruments were not edited.

Observed UTC: **2026-10-23T10:55:49.056330+00:00–2026-10-23T10:56:28.907426+00:00**. Sandbox HEAD, measured revision and supplied freeze: `54a87a51a865ab931fd355e767303337b05cccf4`; branch `seat-r34-MutCounterPins`. Actual visible answering model: `openai-codex/gpt-6.1-sol`. Existing runtime: Python 3.14.8. Tool installs/updates: none.

## Frozen predicate and axes

Predicate preserved verbatim:

> P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.

Axes exercised: carrier byte/size pin enforcement; carrier ID/digest uniqueness; unsafe path rejection; canonical expected-record shape; exact restoration. The isolated fixture target is 2, explicitly labelled `isolated comparator fixture; not a P34 production score` by the counter. The frozen production target remains 12.

## Mutants, source-defined detector, actual output

Expectations were written into [plan.json](MutCounterPins-files/plan.json) before the first detector execution. References below are to the exact [counter bytes exercised](MutCounterPins-files/counter-under-test.py.txt), SHA-256 `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e`.

| Input mutations | Cases | Source-defined expected finding | Actual mutant result |
|---|---:|---|---|
| Wrong declared SHA-256; wrong positive size; same-size `TEXT`→`TEXU` byte edit; truncate one trailing byte | 4 | `carrier_pin:text-a` (114–116) | All exit 2, `met_target:false`, exact finding |
| Size zero, over 16 MiB, boolean, float | 4 | `manifest_row_schema` (153–154) | All exit 2, `met_target:false`, exact finding |
| Duplicate carrier ID; duplicate carrier digest | 2 | `manifest_duplicate` (149–150) | Both exit 2, `met_target:false`, exact finding |
| Empty, absolute, parent, embedded-parent, colon and NUL paths | 6 | `unsafe_path` (57–61,148) | All exit 2, `met_target:false`, exact finding |
| Invalid expected record shapes described below | 32 | `manifest_row_schema` (35–55,153–154) | All exit 2, `met_target:false`, exact finding |

Expected-shape mutations cover: non-object expected value; extra/missing expected keys; boolean/string/unknown schema; non-list `needed`; non-object/extra-key/missing-file needed record; empty/non-string file; non-list versions; non-object/extra-key/missing-hash version record; empty/non-string version name; boolean, negative and overflow values for each of flags/other/hash; unsorted/duplicate `(name,other)` versions; unsorted/duplicate files. The duplicate version case preserves distinct hash values, testing identity by `(name,other)`, not only full-object equality.

**Same detector, pristine → mutated → restored, for every case:**

- 48 pristine runs: exit 0, `finding:version_needs_match`, `matched:2`, `target:2`, `documents_ok:true`, `met_target:true`.
- 48 mutated runs: exit 2, exact predeclared finding above, `met_target:false`.
- 48 restored runs: same successful fixture result as pristine.
- All 144 detector runs: empty stderr, no timeout. Every green run matched both schedules for both carriers.

Full observed stdout/stderr/exit, exact argv, UTC timestamps, source expectation, exact mutated UTF-8 bytes and before/mutated/restored hashes are retained in [batch-0.json](MutCounterPins-files/batch-0.json), [batch-1.json](MutCounterPins-files/batch-1.json), [batch-2.json](MutCounterPins-files/batch-2.json), and [batch-3.json](MutCounterPins-files/batch-3.json). [summary.json](MutCounterPins-files/summary.json) indexes all 48 verdicts and hash triples. No baseline failure was counted as a kill.

## Fixture and invocation boundary

The two private carriers are ordinary UTF-8 text: a `TEXT` line followed by JSON (one named record set, one empty set). The fake [reader.py](MutCounterPins-files/reader.py) checks that text prefix and reads that JSON. Neither fixture is an ELF or a derivative of a held item. The fake reader receives only the counter's opaque input path.

The outer CLI selects `fixture_measure` before production `measure` (counter 281–284), then calls the actual `validate_manifest`, `safe_path`, `canonical` and `score` implementations (222–226). `--root`, `--rev` and `--freeze` are present with the required sandbox/freeze values, but fixture mode does not interpret them as a production measurement. These fixtures intentionally have no `string_table`; their second schedule repeats the text bytes. This probe does not test the randomized naming transform, source/document bindings, or actual ELF extraction.

Each pristine/mutated/restored invocation uses this exact argv, retained as an array in every receipt:

```text
/usr/bin/timeout --signal=TERM --kill-after=1s 15s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r34/w1/MutCounterPins/tools/round-34/version-needs-counter.py --root /fast/scratch/hyaku/kaidoku-r34/w1/MutCounterPins --rev 54a87a51a865ab931fd355e767303337b05cccf4 --freeze 54a87a51a865ab931fd355e767303337b05cccf4 --fixture-spec /fast/scratch/hyaku/kaidoku-r34/w1/MutCounterPins/.ufo/waves/round-34/w1/MutCounterPins-files/spec.json --fixture-reader /fast/scratch/hyaku/kaidoku-r34/w1/MutCounterPins/.ufo/waves/round-34/w1/MutCounterPins-files/reader.py
```

Working directory for all four driver commands: `/fast/scratch/hyaku/kaidoku-r34/w1/MutCounterPins`. Commands exercised, sequentially:

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE /usr/bin/timeout --signal=TERM --kill-after=2s 120s /usr/bin/python3 -I -B .ufo/waves/round-34/w1/MutCounterPins-files/probe.py --batch 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE /usr/bin/timeout --signal=TERM --kill-after=2s 120s /usr/bin/python3 -I -B .ufo/waves/round-34/w1/MutCounterPins-files/probe.py --batch 1
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE /usr/bin/timeout --signal=TERM --kill-after=2s 120s /usr/bin/python3 -I -B .ufo/waves/round-34/w1/MutCounterPins-files/probe.py --batch 2
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE /usr/bin/timeout --signal=TERM --kill-after=2s 120s /usr/bin/python3 -I -B .ufo/waves/round-34/w1/MutCounterPins-files/probe.py --batch 3
```

Each driver reported 12 killed, 0 survived, 0 inconclusive, `exact_final_restoration:true`, `instruments_unchanged:true`. The bounded [probe.py](MutCounterPins-files/probe.py) caps each detector tree at 15 seconds, address space at 512 MiB, CPU at 30 seconds/process, processes at 4096 per UID, and file writes at 2 MiB. It starts only one child tree at a time and kills any remaining members of that owned tree on completion. Fixture restoration is in `finally`, including detector failures.

## Restoration evidence

Every case restored exact bytes before its final detector run; all four batches ended with identical fixture bytes. Final hashes equal pristine hashes:

| File | Pristine = restored SHA-256 |
|---|---|
| `spec.json` | `be5184570e2a99388c27779a9a1792011d44fd184da65e1385be4c5b0149f9b7` |
| `carrier-a.txt` | `96759f5ad5a3235bc618c71297c135942e503fb70e120d44fc27c0db553c27e9` |
| `carrier-b.txt` | `730f7684ce977c79121036b8f65c4e8ac2a8d2e2e5048ee754efde14d4384f66` |
| `reader.py` | `725db1a9e920c371374fbd6af18741870a6f81f956980833505ca4f364f70274` |

Representative changed-byte evidence (full triples for every mutant are in the receipts):

- Wrong declared digest: spec `be518457…` → `c4b2f2d6ffce39505015dbc9ee0f93d05cdce2b81dc37ea8394a7e46cefb8c56` → `be518457…`.
- Wrong declared size: spec `be518457…` → `99cc20ee083e58e1e39683b29e54b43fc83f07e9f8c5032f07cc28f516e07ff7` → `be518457…`.
- Same-size text edit: carrier A `96759f5a…` → `fa27803f1dd0ab7a60dd04c0052a1bf00470e67445709ad5c6e9e4fc75338364` → `96759f5a…`.
- Truncated text: carrier A `96759f5a…` → `16b5cfb1e5ad504aef66dc37ba6917c5d65d8490a4653fa435e40ce4d11716f4` → `96759f5a…`.

Before/after hashes of all four frozen instruments, claims and production manifest were identical in every batch. In particular, production manifest SHA-256 remained `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d`; claims remained `bb971710cb17ef775227cceb1b7024b7380e859564a28648709dd1c786a997a4`.

The [archive manifest](MutCounterPins-files/archive-manifest.json) retains sizes and SHA-256 for the exact code, plan, restored fixtures, source snapshot and raw receipts copied into this seat's archival directory. No production reader invocation, public binary mutation, target execution, REA, held-item access, Git write, shared-source edit, or integration was performed. This report supplies only the assigned counter-fixture evidence; promotion/admission remains with L1.

Report: .ufo/waves/round-34/w1/MutCounterPins.md
