# CtlDenyWords — fresh text-only denial and vocabulary controls

## Result and axes

Both assigned no-reader controls were rejected by the unchanged frozen counter: **0/12, target not met, exit 1**, with all document/source bindings passing. Exact-byte restored denial also returned 0/12. No production-reader score was produced.

Axes: **R34-C1 depth only; lexical-shortcut rejection; no-reader containment; reproducible provenance.** These are pre-data negative controls for the R32 denial/word-bag shortcut, **not calibration claims**, claim admission, or general semantic robustness evidence.

- Sandbox: `/fast/scratch/hyaku/kaidoku-r34/w1/CtlDenyWords`.
- Measured revision and freeze: `54a87a51a865ab931fd355e767303337b05cccf4` (sandbox HEAD measured with read-only `git rev-parse HEAD`; detector independently reports both revisions).
- Frozen instruments revision: `8897a67f6074580d6eac1a3fc0e37fdcd7aa0df0`.
- Answering model visible in runtime context: `openai-codex/gpt-6.1-sol`; no provider-log audit or other model runtime invoked.

## Predicate preserved verbatim

> P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.

Target remains exactly 12. No predicate, source binding, denominator, counter, production reader or expected manifest was repaired or rescaled.

## Sources and controls

The prior shortcut/control requirement was reopened at `.ufo/waves/round-34/prep/R34Overlap.md:17-24,64-68`. Frozen claim and bindings are in `.ufo/waves/round-34/claims.json:6-16,54-69`. Scoring requires a canonical structured object and exact equality, not vocabulary matching (`tools/round-34/version-needs-counter.py:34-55,119-139`); the explicit control route substitutes only the supplied reader bytes (`:213-219`).

Both sources contain only a comment and one `print` of a constant JSON string: no imports, argv inspection, input/file reads, subprocesses, reader delegation or per-carrier dispatch.

1. [Explicit denial](CtlDenyWords-files/denial.py): states “These GNU ELF dependency/version requirements do not exist. None of the following named dependencies is present; this text explicitly denies every requirement:” followed by the real dependency names.
2. [Vocabulary-only bag](CtlDenyWords-files/vocabulary.py): only the whitespace-separated real dependency names, without relationships, requirement records or numeric metadata.

The bag contains **all 71 distinct dependency names** in the frozen manifest. Extraction: `[.carriers[].expected.needed[].file] | unique`. The authored list equals that exact union; no carrier bytes were consulted by either control. The names are static constants at execution, not loaded from the manifest. Source manifest SHA-256: `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d`.

Both outputs are valid JSON **strings**, deliberately not canonical requirement objects. Thus rejection is not a reader exception, nonzero reader exit or JSON syntax failure. This tests these specific lexical shortcuts only; it does not test denial semantics inside otherwise canonical records.

[Control design](CtlDenyWords-files/control-design.json), written before the first detector run, fixes expected 0/12, `met_target=false`, exit 1 for every phase.

## Bounded detector and actual outputs

The same argv was used for pristine denial, vocabulary and restored denial, with `active-reader.py` as the only changing input. Only line 2 (the output literal) changed. Counter and production-reader bytes were never mutated. Git/Python environment overrides were removed; the recorded environment policy disables global/system Git configuration and sets `LC_ALL=C`.

```sh
/usr/bin/timeout --signal=TERM --kill-after=3s 150s /usr/bin/prlimit --as=1073741824 --cpu=90 --fsize=16777216 --nofile=128 --nproc=4096 --core=0 /usr/bin/python3 -I -B tools/round-34/version-needs-counter.py --root /fast/scratch/hyaku/kaidoku-r34/w1/CtlDenyWords --rev 54a87a51a865ab931fd355e767303337b05cccf4 --freeze 54a87a51a865ab931fd355e767303337b05cccf4 --control-reader /fast/scratch/hyaku/kaidoku-r34/w1/CtlDenyWords/.ufo/waves/round-34/w1/CtlDenyWords-files/active-reader.py
```

Address space 1 GiB; CPU 90 seconds; file size 16 MiB; open files 128; per-user process ceiling 4096; core size 0; wall timeout 150 seconds, forced kill after 3 seconds. Fixed twelve carriers/two schedules, one foreground child tree at a time. The driver attempts process-group cleanup in `finally`; no background jobs or delegates were started.

| Phase | Observed UTC start–end | Score | Counter exit | Finding |
|---|---|---:|---:|---|
| Pristine explicit denial | 10:55:24.539872–10:55:24.868309Z | 0/12 | 1 | `version_needs_mismatch` |
| Mutated vocabulary-only bag | 10:56:07.752658–10:56:08.056479Z | 0/12 | 1 | `version_needs_mismatch` |
| Exact restored denial | 10:56:23.572388–10:56:23.918016Z | 0/12 | 1 | `version_needs_mismatch` |

For **each** phase: `mode=control`, `documents_ok=true`, `met_target=false`; all 24 child invocations exited 0, emitted the exact expected JSON string, had empty stderr and failed exact-record equality. Eleven second-schedule attempts received the frozen counter's unpredictable naming transformation; e12's empty case also rejected the scalar output. Counter stderr was empty, with no timeout or detector evaluation error. Full stdout retains each observed value, input/output hashes and string translation.

## Verdict and exact restoration

**Control verdict:** both fresh skip-work controls fail the frozen target as required. Neither meets the kill-rule predicate. These outputs do not justify a production pass or calibration improvement.

**Mutation classification:** **inconclusive as mutation-kill evidence**, because the pristine denial already fails the target intentionally. No killed or surviving counter mutant is claimed. The one behavior-bearing substitution is denial text → vocabulary bag, not a counter repair.

| Bytes | SHA-256 |
|---|---|
| Initial denial / pristine active source | `37338f0bbbf4be3a58ae4f09c06f93677d0f648fef51a24415c19e8d9c7bf88a` |
| Vocabulary / mutated active source | `694d1efb68f2d52e4b8a59a055b3df528f1b1df3b6fe77c3622705dd69955b8c` |
| Restored active source | `37338f0bbbf4be3a58ae4f09c06f93677d0f648fef51a24415c19e8d9c7bf88a` |
| Frozen counter, unchanged before/after all runs | `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e` |
| Production reader, hashed only and never run | `ac7d24a546022c7cc8295450a2692c51c07099e42a1aa02fb69c29455dae3f33` |

Restored active bytes equal the original denial source byte-for-byte; the restored detector run confirms the same 0/12 behavior. Claims and manifest hashes also remain unchanged in every before/after receipt. Both immutable source variants and the restored active copy are archived.

## Evidence and containment

Owned archive: `.ufo/waves/round-34/w1/CtlDenyWords-files/` (23 files; archive writes returned their expected resolved paths: `true`). Key receipts:

- [Pristine stdout](CtlDenyWords-files/pristine-denial.stdout), [stderr](CtlDenyWords-files/pristine-denial.stderr), [argv/UTC/exit/hashes](CtlDenyWords-files/pristine-denial.receipt.json).
- [Vocabulary stdout](CtlDenyWords-files/mutated-vocabulary.stdout), [stderr](CtlDenyWords-files/mutated-vocabulary.stderr), [argv/UTC/exit/hashes](CtlDenyWords-files/mutated-vocabulary.receipt.json).
- [Restored stdout](CtlDenyWords-files/restored-denial.stdout), [stderr](CtlDenyWords-files/restored-denial.stderr), [argv/UTC/exit/hashes](CtlDenyWords-files/restored-denial.receipt.json).
- [Exact probe driver](CtlDenyWords-files/probe-driver.py), [mutation patch](CtlDenyWords-files/mutation.patch), [restoration patch](CtlDenyWords-files/restoration.patch), expected output bytes for both sources, and frozen detector/claims/manifest snapshots.
- [Summary](CtlDenyWords-files/probe-summary.json) and [byte/hash inventory](CtlDenyWords-files/archive-inventory.json).

One setup-only tool-wrapper `TypeError` applied no edit; unchanged bytes were reopened and the direct edit tool succeeded. No detector retry or runtime/model switch resulted. No safety/content-policy refusal occurred. No tool install/update occurred.

Only text controls/evidence were authored. The frozen counter made its prescribed private never-executed schedule copies; no binary fixture was authored by this seat. No target binary execution, production-reader run, REA run, held-item reconstruction, Git write, integration or shipping occurred. Lane writes are limited to this report and its named archive; the sandbox-only LOG entry was appended per local guidance. Held exclusions and sibling artifacts remain untouched. No further probe is claimed or run.

Report: .ufo/waves/round-34/w1/CtlDenyWords.md
