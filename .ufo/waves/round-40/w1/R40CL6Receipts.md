DONE — R39-CL6 receipt leg: `score-receipt.sh` (exit-code/argv/revision-aware receipt wrapper) and `ledger-status.py` (per-seat `ok`/`no-report`/`empty-report` fill) are written, selftested (51/51 and 43/43), exercised on both round-39 wave ledgers and wrapped around a real lane counter at two exit states. No REA/unblob run, no VCS mutation, no lane file outside this seat's artifacts touched.

# R40CL6Receipts — routed defect R39-CL6 (receipts carry the exit code; ledgers carry seat status)

Item: `R40CL6Receipts`, wave 1 (pre-freeze build). Base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`; nothing frozen.

## 1. Deliverables

Artifact dir `.ufo/waves/round-40/w1/artifacts/R40CL6Receipts/` (all writes for this seat are here; L1 integrates):

| path | bytes | sha256 | role |
|---|---|---|---|
| `score-receipt.sh` | 19415 | `c42caec8c9326f7a7e2356e1eca20887743da6815de9cc5ae62dde9cb0088fd1` | counter-run receipt wrapper (`--selftest`) |
| `ledger-status.py` | 17325 | `277cdb8970da542b647ffaef4e5d79c277a48218d906bc71403dd02ea86583f1` | per-seat status filler (`--selftest`) |
| `r39-w1-status.json` | 221991 | `73edb174a77a56b59ada13aad169a6cb547ae429b25ec533d51eef725278e5af` | copy of `r39-w1-results.json` with statuses |
| `r39-w2-status.json` | 200287 | `b24b77f79aeb08af77c96f8dbbd0d9978aa38c01b6f964d065514ef3a29419f4` | copy of `r39-w2-results.json` with statuses |
| `r39-w1-status-nocanonical.json` | 222112 | `622eb98007766c53154601c571bc74103bc974967f549ff20636140f7f68b648` | sensitivity run (canonical fallback disabled) |
| `receipt-c2-met.json` | 1571 | `564d317c2e8b7bd630acb4d93cbd48e4de0ae4bf9bbfac1a69f3cd5ffbc0f1ca` | real counter, exit 0 (`met_target true`) |
| `receipt-c2-freeze.json` | 1500 | `ca8977403a9226a08f2a023c7ed4b8eb21fb97459d0534d924fa5b7907db24e9` | real counter, exit 2 (`no_manifest_at_rev`) |
| `score-receipt-selftest.txt` | 41 | — | `score-receipt selftest: 51/51 cases pass` |
| `ledger-status-selftest.txt` | 42 | — | `ledger-status selftest: 43/43 checks pass` |
| `r39-w1-status.stderr.txt`, `r39-w2-status.stderr.txt`, `r39-w1-status-nocanonical.stderr.txt` | — | — | each run's stderr summary |
| `demo/demo-ledger.json` | 850 | `2449ccdef3419c12830c162f9eceae4337b8629c73cb0951537aac832fd46b8b` | 5-seat fixture covering every discovery route |
| `demo/demo-status.json` | 1632 | `0ce339cc85d80ee27e5bc7eb456fb9b56482f494218b29d2984374035aac6b72` | its filled copy (`ok=2 no-report=2 empty-report=1`) |
| `demo/demo-ok.md`, `demo/demo-empty.md` | 15 / 0 | — | fixture reports (non-empty / zero byte) |

`demo/demo-status.stderr.txt` records `ledger-status: 5 seats ok=2 no-report=2 empty-report=1 (wave_dir=.ufo/waves/round-39/w1)`.

## 2. `score-receipt.sh` — what it guarantees

Contract: `score-receipt.sh OUT.json -- <counter argv...>` runs the counter once with stdout/stderr captured and writes `OUT.json` = the counter's own JSON object spread at top level (a JSON array/scalar goes under `result` with `result_kind`) plus the routed-defect keys `exit_code`, `argv`, `counter_sha256`, `utc_start`, `utc_end`, and the diagnostics `receipt_version`, `counter`, `counter_bytes`, `stdout_sha256`, `stdout_bytes`, `stderr_sha256`, `stderr_bytes`, `stdout`, `stdout_truncated`, `stderr`, `stderr_truncated`, `stdout_json`, `counter_json_key_collisions`, `lane_revision_arguments` (plus `lane_root`/`lane_head` with `--lane`). Exit status is the counter's exit status. The five required keys are the first five keys of every receipt.

- **Exit code is unfalsifiable by counter output**: a counter key that collides with a wrapper/diagnostic key is kept out of the top level and named in `counter_json_key_collisions`; selftest case `collision:status wins` prints `{"exit_code": 99}` from a counter that exits 0 and the receipt still says `exit_code: 0`.
- **Revision arguments are recorded independently**: `--rev`, `--freeze`, `--base`, `--at`, `--lane-rev`, `--root`, `--lane`, in both `--flag value` and `--flag=value` forms, repeats as lists. The real receipt shows `lane_revision_arguments {root, rev: 8b9634ed…, freeze: 8fcda41c…}`.
- **Counter identity**: `counter_sha256` is the sha256 of the counter FILE, not of the interpreter; arg `python3 tools/round-39/c2-counter.py` resolves to `tools/round-39/c2-counter.py` (`counter_bytes 36517`). `--counter PATH` overrides the heuristic.
- **Streams**: full bytes are always hashed/sized; embedding is capped at `--max-capture-bytes` (default 1 MiB) per stream with `*_truncated`. Invalid UTF-8 is replaced (`\ufffd`) so the receipt is always valid UTF-8 JSON; the byte hash still pins the raw stream.
- **UTF-8/locale-independent receipt text**: `json.dump(..., ensure_ascii=True)`, indent 1, exactly one trailing newline; written to `OUT.json.tmp.<pid>` then `os.replace` (no partial receipt; tmp removed on failure).
- **Exit surface**: counter status passed through (0 seen on `met`, 2 on `no_manifest_at_rev`, 127 for a missing executable, 143 for SIGTERM — selftest); 2 only for a usage/environment error (missing `--`, missing OUT, missing OUT parent, unreadable `--counter`, receipt assembly failure).
- `utc_start`/`utc_end` are UTC ISO-8601 with milliseconds taken immediately around the counter; selftest asserts format and `start <= end`.
- cwd is the caller's cwd (relative counter paths resolve; selftest case `cwd passthrough`); staging dir is `mktemp -d`, so `TMPDIR` is honoured, and it is removed on exit.

Selftest: 51 assertions across 17 scenarios (object/array/scalar/non-JSON/invalid-UTF-8 stdout, exit 0/1/2/3/127/143, stderr capture, collision shadowing, interpreter-script sha, `--counter`, revision harvest, `--lane`, capture cap, UTF-8 text, argv with spaces, usage errors, cwd). Run with `TMPDIR=/fast/scratch/hyaku/kaidoku-r40/R40CL6Receipts ./score-receipt.sh --selftest` → `score-receipt selftest: 51/51 cases pass`, exit 0.

### Real-counter evidence (lane counter, no REA/unblob)

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
$A/score-receipt.sh $A/receipt-c2-met.json -- python3 tools/round-39/c2-counter.py \
  --root "$PWD" --rev 8b9634ed8253653e7eb994aad9860a624e3b0366 \
  --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b
score-receipt.sh: exit=0 receipt=…/receipt-c2-met.json          # shell exit 0
```
Receipt: `exit_code 0`, `matched 20`, `n 20`, `met_target true`, `stdout_bytes 208`, `stderr_bytes 0`, `counter_sha256 775766d86de0f1adbb2b7836664bc5641f92c0493bf0aa012b176ce03e7f0e41`, `argv` verbatim.

Same counter, `--rev 8fcda41c… --freeze 8fcda41c…`:
```
score-receipt.sh: exit=2 receipt=…/receipt-c2-freeze.json       # shell exit 2
```
Receipt: `exit_code 2`, `unevaluable: "no_manifest_at_rev"`, `revision 8fcda41c…`, same `counter_sha256`. This is exactly the round-39 gap (cited `l1/scores/*.json` carried no exit code): the two states are now distinguishable from the receipt alone, and the wrapper's own exit equals the counter's.

## 3. `ledger-status.py` — what it guarantees

Contract: `ledger-status.py RESULTS.json --root LANE [--wave-dir DIR] [--out PATH] [--selftest]`; writes a COPY of the ledger with per-seat `status` ∈ {`ok`, `no-report`, `empty-report`} plus `report`, `report_bytes`, `report_source` (`output`|`canonical`); a pre-existing non-null `status` is preserved as `status_previous`; the input file is never written. Without `--out` the copy goes to stdout; a count line always goes to stderr. Exit 0 written, 2 usage/parse.

- **Report presence only**: `ok` = report file exists and holds non-whitespace text; `empty-report` = exists but zero/whitespace-only; `no-report` = no candidate resolves to a file.
- **Discovery order**: every string under a report-style key (`report`, `report_path`, `report_file`, `report_md`, `reportpath`, …) anywhere inside `output` (decoded JSON object, JSON string, or already-decoded object; depth-capped, document order, top level first) → a `Report: <path>.md` trailer for non-JSON output → the lane convention `<wave-dir>/<name>.md`. `--wave-dir` defaults to `.ufo/waves/round-<round>/<w1|w2>` derived from the ledger's own `round`/`wave`.
- **Path normalisation**: leading `./` dropped; a leading lane basename (`kaidoku-shokunin/`) dropped; relative paths resolve against `--root`; candidates outside `--root` (compared on realpath, so symlinks cannot escape) are rejected.
- **Copy semantics**: `copy.deepcopy`, key order preserved; only `status`, `report`, `report_bytes`, `report_source` (and `status_previous` when a prior status existed) are added. Verified on both real ledgers: every original field of every seat is byte-equal in the copy, no unexpected keys, `seats` unchanged.

Selftest: 43 checks over 12 seats covering all routes — top-level `report`, nested `deliverables.report`, lane-basename-prefixed path, empty file, whitespace file, canonical-only seat, absolute path outside root (rejected), `Report:` text trailer, missing/`None` output, null pre-status, preserving a pre-existing `status`, canonical fallback disabled, bad ledger, and a CLI arm asserting the input file's bytes are unchanged and `--out` is written. `./ledger-status.py --selftest` → `ledger-status selftest: 43/43 checks pass`, exit 0.

### Real-ledger evidence

```
$A/ledger-status.py .ufo/waves/round-39/r39-w1-results.json --root $PWD --out $A/r39-w1-status.json
ledger-status: 43 seats ok=43 no-report=0 empty-report=0 (wave_dir=.ufo/waves/round-39/w1)   # exit 0
$A/ledger-status.py .ufo/waves/round-39/r39-w2-results.json --root $PWD --out $A/r39-w2-status.json
ledger-status: 39 seats ok=39 no-report=0 empty-report=0 (wave_dir=.ufo/waves/round-39/w2)   # exit 0
```
- `r39-w1-status.json`: 43/43 `ok`; `report_source` output 35 / canonical 8; no `status_previous`; originals preserved.
- `r39-w2-status.json`: 39/39 `ok`; output 34 / canonical 5; the two bucket-relative seats `R39W2HarmCheck` and `R39W2LessonReview` (whose `output.report` is `kaidoku-shokunin/.ufo/waves/round-39/w2/…`) resolve through prefix stripping to `.ufo/waves/round-39/w2/…` with `report_source: output` — i.e. normalisation, not the canonical fallback, found them.
- Independent cross-check before writing the tools: every one of the 43+39 canonical `<wave-dir>/<name>.md` files exists and is non-zero, which is why all seats are `ok`; the fill is data-driven, not hardcoded (see sensitivity below).
- Inputs untouched: `git -C <lane> status --porcelain .ufo/waves/round-39/r39-w1-results.json .ufo/waves/round-39/r39-w2-results.json` → empty.

### Sensitivity (proves statuses are computed, not assumed)

Same w1 ledger with `--wave-dir .ufo/waves/round-39/absent-wave`:
```
ledger-status: warning: wave dir not found under root: …
ledger-status: 43 seats ok=35 no-report=8 empty-report=0   # exit 0
```
The 8 seats whose `output` carries no report path fall to `no-report`; the 35 with an output report path stay `ok`. Demo fixture additionally shows `empty-report` and the non-JSON `Report:` route in one run.

## 4. Limits / risks (recorded, not hidden)

- `score-receipt.sh` embeds explicit diagnostics beyond the five required keys (stream text/hashes, counter bytes, collisions, revision args). A consumer reading only the five specified keys is unaffected; a consumer comparing the receipt to a strict five-key schema would see extras — deliberate, since "captures stdout/stderr" and "lane revision arguments" need a home.
- Counter-file resolution is a documented heuristic (explicit `--counter` else argv[0] if a regular file else the first regular-file argument after `python*|bash|sh|dash|node|nodejs|perl|ruby`). `npx`/`uv` are deliberately NOT interpreter-recognised: `npx … <input> <outdir>` would otherwise record an input carrier as "the counter". For such runners pass `--counter`.
- stdout is parsed as JSON only if the whole stream is valid UTF-8 JSON; otherwise `stdout_json: false` and no spread (stdout is still hashed and embedded). A counter printing JSON after log lines therefore does not spread — correct for the lane counters, documented limitation otherwise.
- `utc_start`/`utc_end` come from the host clock (ms resolution); they bracket the child but are not monotonic-proof.
- `ledger-status.py` judges report PRESENCE only; an `ok` seat may still be a bad report. `empty-report` is a whitespace test (files ≤1 MiB read whole; larger files are sampled head 64 KiB + tail 4 KiB — `[INFERENCE]` this bounds I/O rather than reading multi-MB artefacts).
- Discovery depends on a `report`-style key, the `Report:` trailer, or the `<wave-dir>/<name>.md` convention; a seat whose report is elsewhere and unnamed is `no-report`.
- `status` is always recomputed; a prior non-null value is kept as `status_previous`. Round-39 ledgers have no prior value (0 occurrences).
- Receipt assembly failure exits 2 rather than the counter's status (no receipt = no evidence); everything else exits the counter's status.

## 5. Boundaries, tooling, scratch

- Writes: only `.ufo/waves/round-40/w1/artifacts/R40CL6Receipts/` (this report plus that dir). No `corpus/`, `tools/`, `plans/`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`; lane `git status --porcelain` shows only the pre-existing untracked `.ufo/waves/round-40/` and `plans/round-40-claims.md`.
- No VCS mutation (read-only `git status` only), no REA/unblob invocation, no frozen-carrier contact, no C2 held-out build. The real-counter receipts wrapped `tools/round-39/c2-counter.py`, which reads lane git objects only.
- No tool installed or upgraded (no pacman/uv/npx/npm).
- Scratch `TMPDIR=/fast/scratch/hyaku/kaidoku-r40/R40CL6Receipts` removed after the runs; selftests stage under `mktemp -d` and clean up. `__pycache__` from a syntax check removed.

Report: `.ufo/waves/round-40/w1/R40CL6Receipts.md`
