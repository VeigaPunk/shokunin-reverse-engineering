# CtlAllFalse — text-only skip-work control

## Result

The all-false reader scored **0/12**, `met_target: false`, `documents_ok: true`, `finding: "version_needs_mismatch"`, counter exit **1**, in explicit `mode: "control"`. Its 24 reader invocations all exited **0**, emitted JSON `false`, had empty stderr, and failed both schedules for every carrier. Eleven second-schedule inputs had recorded string translations. The empty carrier e12 also failed: JSON `false` is not the required canonical empty record.

**Skip-work control verdict: target not met. Mutation-test verdict: INCONCLUSIVE, not killed**, because the pristine text-only baseline also failed the complete frozen predicate (1/12). This probe does not supply a positive production baseline or adjudicate/promote the claim. No predicate, target, counter, manifest, source binding, or production reader was repaired or changed.

## Axes and boundary

- Assigned claim axis: **depth**, R34-C1; not coverage, runtime capability, authenticity, or loader behavior.
- Adversarial axis: input-independent false output versus exact canonical GNU version-needs records on both schedules.
- Evidence axes: frozen detector fidelity, bounded execution, exact byte restoration.

Sandbox: `/fast/scratch/hyaku/kaidoku-r34/w1/CtlAllFalse`.
Measured HEAD, `--rev`, and `--freeze`: `54a87a51a865ab931fd355e767303337b05cccf4`.
Instrument revision recorded by the frozen contract: `8897a67f6074580d6eac1a3fc0e37fdcd7aa0df0`.

Frozen predicate, preserved verbatim:

> P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.

## Mutant and expected detector

Only the one behavior-bearing print statement in the scratch control reader changed:

```python
# Pristine and restored bytes (34 bytes, including final newline):
print('{"schema":1,"needed":[]}')

# Mutated bytes (15 bytes, including final newline):
print('false')
```

Neither version imports modules, reads stdin, inspects argv, opens input, or reads a manifest. The exercised mutant is retained as `CtlAllFalse-files/mutated.reader.py`; the live scratch `control-reader.py` was restored.

Expected detector: the frozen `tools/round-34/version-needs-counter.py`, through `--control-reader`, should reject JSON false. Its `canonical()` requires an object containing exactly `schema` and `needed`, integer schema 1, and a list of canonical requirement records. `score()` additionally requires exact expected-record equality on both schedules; the target remains exactly twelve and all document bindings must hold. The frozen comparator was not mutated.

## Exact command and containment

The counter argv was identical for all four invocations:

```text
/usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r34/w1/CtlAllFalse/tools/round-34/version-needs-counter.py --root /fast/scratch/hyaku/kaidoku-r34/w1/CtlAllFalse --rev 54a87a51a865ab931fd355e767303337b05cccf4 --freeze 54a87a51a865ab931fd355e767303337b05cccf4 --control-reader /fast/scratch/hyaku/kaidoku-r34/w1/CtlAllFalse/.ufo/waves/round-34/w1/CtlAllFalse-files/control-reader.py
```

The successful three-phase harness launch was this exact argv, with the final phase argument respectively `pristine-retry`, `mutated`, and `restored`:

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE /usr/bin/timeout --signal=TERM --kill-after=5s 160s /usr/bin/prlimit --as=536870912 --nproc=16384 --nofile=128 --fsize=16777216 --cpu=120 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r34/w1/CtlAllFalse/.ufo/waves/round-34/w1/CtlAllFalse-files/probe-v2.py PHASE
```

`PHASE` above denotes the three listed literal arguments, not an exercised shell variable. Each receipt retains its complete literal `launch_argv` and counter `argv`, cwd, UTC interval, measured-revision command/stdout/stderr/exit, actual resource limits, counter exit, stdout/stderr hashes, and reader/source before/after hashes.

The harness removed all `GIT_*` and `PYTHON*` environment variables, disabled global/system Git configuration, set `LC_ALL=C`, and placed `TMPDIR` inside its own sandbox evidence directory. Counter timeout was 145 seconds inside the 160-second outer timeout with a five-second forced-kill grace. Limits were 512 MiB address space, 16 MiB per-file size, 128 file descriptors, 120 CPU seconds, and NPROC 16384 (a shared-UID limit, not a private PID namespace). One probe process tree ran at a time; the frozen counter launches its reader/Git subprocesses sequentially. The harness killed its counter process group in `finally` and waited for its direct child. No background jobs or delegates were used.

## Observed receipts

All times UTC, 2026-10-23. Every counter stderr file is exactly empty. No invocation timed out.

| Phase | Start — end | Counter exit | Matched | Finding |
|---|---|---:|---:|---|
| Initial pristine setup | 10:54:22.535098 — 10:54:22.618141 | 2 | not scored | `[Errno 11] Resource temporarily unavailable` |
| Pristine, resource retry | 10:55:38.424190 — 10:55:38.812314 | 1 | 1/12 | `version_needs_mismatch` |
| All-false mutation | 10:55:50.098453 — 10:55:50.376918 | 1 | 0/12 | `version_needs_mismatch` |
| Restored | 10:55:57.705089 — 10:55:57.988315 | 1 | 1/12 | `version_needs_mismatch` |

The initial harness used NPROC 2048 and encountered the recorded resource error before producing a score. That failed attempt is retained, not counted as a rejection or kill. Only the containment wrapper was revised to NPROC 16384; `probe.py` and `probe-v2.py` both remain as exact exercised code. The three scored phases used the same revised bounds and detector. The canonical constant-empty baseline/restoration matched only e12; they were not positive baselines for the full claim.

Counter stdout SHA-256:

```text
pristine:       0da1bf0fb2fb35bda8335cdaa16f12e9094fbd40607d389d0db519bb622c53d6
pristine-retry: 8c64bb29decf1697e6fa6dada71c2f1e1f7c10ed5def2f93c26747068fd91ae0
mutated:        c080bc4604f8093c784ea83e592ade9ee2ce5f72a09c7988f444399ccc3b140f
restored:       1b56a37311639ecfde939467975476ca98ae73a157184a72dcfbe4a95c5517e5
stderr, all:    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

## Restoration and frozen-byte evidence

Reader SHA-256 before mutation and after exact restoration:

```text
aef17bad90a73e412e55e8ff6255dbc70001304cba2ee399a2908e9a03f72bc3
```

Mutant SHA-256 before/after its scoring invocation:

```text
edebb41868804b5c1464047acba2f94be184dcb371f5b0534c845fc543d25c08
```

Every receipt records identical before/after hashes for the counter, production reader, integrity instrument, frozen claims, and expected manifest. In particular:

```text
counter:  d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e
claims:   bb971710cb17ef775227cceb1b7024b7380e859564a28648709dd1c786a997a4
manifest: f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d
```

Different pristine/restored counter stdout hashes are expected: each invocation generates fresh opaque paths and records fresh input-name challenges. Reader-byte equality, not receipt-output equality, establishes restoration.

## Evidence archive and exclusions

Archive: `.ufo/waves/round-34/w1/CtlAllFalse-files/`.

- For each of `pristine`, `pristine-retry`, `mutated`, and `restored`: exact `.reader.py`, `.stdout.json`, `.stderr.txt`, and `.receipt.json`.
- Exact exercised `probe.py` and `probe-v2.py`, plus restored `control-reader.py`.
- Copies of frozen `version-needs-counter.py`, `claims.json`, and `expected.json`. Carrier bytes remain retained in the named frozen Git revision; no new binary fixture was authored.

Only explicit controls were scored. The production reader and expected-author reader were never executed; no REA run, target-binary execution, held-item reconstruction, Git write, integration, routing change, or operator-config write occurred. U064N008Hf47eb933, R33FixtureBuilder, and derivatives were untouched. Lane writes were confined to this report and its named archive. No tools were installed or updated. Visible answering model: `openai-codex/gpt-6.1-sol`; no safety refusal, model switch, or quota fallback was observed.

Report: .ufo/waves/round-34/w1/CtlAllFalse.md
