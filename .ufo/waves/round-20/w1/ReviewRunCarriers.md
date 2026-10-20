# ReviewRunCarriers — round 20

**Axes:** calibration, coverage, depth. **Scope:** read-only review of the round-19 driver against round-20's runner contract. No W20 runner existed at review time (`test -e` below); conclusions about changes are contract-backed requirements, not a review of an unlanded implementation. The R19 script is tracked in the declared baseline and its working-tree diff is empty.

## Findings

### HIGH — R19's integrity hash does not enforce the no-execution boundary

**Observation:** R19 checks the TSV SHA-256 and then invokes `carrier-run.py`; no carrier-guard check occurs in that path (`.ufo/waves/round-19/run-carriers.sh:302-307,335-340`). Round 20 explicitly requires a guard check before each label (`.ufo/waves/round-20/gen-wave1.py:265-269`); D3's check detects executable-mode, ctime, and content changes, but explicitly does not prevent loader-mapped execution or root (`.ufo/waves/round-20/contract.md:46-52`). The only current guard evidence is a manual arm record, whose own `action` says the tool did not yet exist (`.ufo/waves/round-20/evidence/carrier-guard/manual-arm.json:2-3`). The guard-tool assignment requires adopting that record into `arm.json` without touching the carriers (`.ufo/waves/round-20/gen-wave1.py:101-109`).

**Required:** the W20 runner must check `predictions/carriers.tsv` against the adopted arm record before every label and fail closed on any nonzero check result; do not re-arm from current state, which would reset the baseline. The precheck is detection, not a sandbox or proof against same-UID races; retain D3's stated limits. A final post-run check is also advisable: the assigned pre-label-only check does not observe changes made during the last run.

### HIGH — Old observation comparison cannot measure C3

**Observation:** the R19 driver wires the W17 `log-extract.py` and `compare.py` into `observation.json`/`compare.json` (`.ufo/waves/round-19/run-carriers.sh:57,321-328,343-350`). C3 instead forecasts the first Go-analysis failure and requires comparison against the bound Ghidra log; the W20 task defines the new extractor/comparator and the comparator's `--extractor` path argument (`.ufo/waves/round-20/claims.json:36-39`; `.ufo/waves/round-20/gen-wave1.py:241-252`; `.ufo/waves/round-20/contract.md:76-81`).

**Required:** run `W20/tools/compare-first-failure.py` with the frozen per-label prediction and the receipt-bound log, passing `W20/tools/first-failure-extract.py`; retain its JSON and exit code in `W20/runs/<label>/`. Treat comparator exit 1 (mismatch) and 2 (unevaluable) as non-success. Preserve the receipt and exact session/log binding; do not substitute the old generic observation comparison. The round-20 runner assignment explicitly requires outputs at `W20/runs/<label>/` (`gen-wave1.py:265-269`).

### MEDIUM — A green carrier-run exit is not the C3 admission gate

**Observation:** R19's wrapper marks success from `carrier-run.py` and compare exits (`.ufo/waves/round-19/run-carriers.sh:341-350`); it does not invoke `receipt-validate.py`. C3 counts a label only with a frozen prediction, a validated bound receipt, and a first-failure comparison; any counted receipt failing `receipt-validate --require-mid-maps` falsifies the claim (`.ufo/waves/round-20/claims.json:36-39`).

**Required:** keep the R19-style receipt in each W20 run, and ensure the W20 measurement/counting path rejects every receipt that fails `--require-mid-maps` or lacks the required comparison record. Do not count wrapper exit 0 as receipt validation or as a first-failure match.

### MEDIUM — Retarget the carrier and tool identity; retain the output-path boundary

**Observation:** R19's fixed defaults still name W18/W17 inputs and its comments/error say W19 (`.ufo/waves/round-19/run-carriers.sh:2-15,46-57,291`). Round 20's carrier set is the Go 1.24.6 tree (`.ufo/waves/round-20/contract.md:88-92`); the existing scout report records 20 executable toolchain ELFs, all with build info (`.ufo/waves/round-20/w1/ScoutGo1246Carriers.md:9-24,35-59`). The R19 `producer.json` hashes five W17 tools plus the old swiss-misread and selection inputs (`.ufo/waves/round-19/run-carriers.sh:309-328`), so it will not identify the new comparator, extractor, or guard unless updated.

**Required:** use W20's frozen TSV/prediction blobs and W20 v2/comparison/guard paths; update producer/tool pins to include the actual W20 producers. Keep the canonicalized output allowlist: R19 resolves `RUNS_DIR` and accepts only `<W>/runs/*` or `/tmp/*` before `rm -rf`/mkdir (`.ufo/waves/round-19/run-carriers.sh:286-295`), so copying the script under W20 naturally scopes the default to W20/runs. Update the stale W19 diagnostic. Keep dry-run from invoking REA or deleting/creating run outputs.

### MEDIUM — Test-only `TOOLS_DIR` override is not enforced as test-only

**Observation:** `TOOLS_DIR` can be replaced through the environment (`.ufo/waves/round-19/run-carriers.sh:50-53`), and the selected `carrier-run.py` is executed as Python (`:335-340`). The normal W17 runner passes the carrier to REA `inspect-go-binary`/`analyze` commands (`.ufo/waves/round-17/tools/carrier-run.py:352-381`); the wrapper itself does not invoke the carrier path as a shell command. The R19 header describes its overrides as dry-check-only, but that is not enforced.

**Inference / risk:** a caller able to set `TOOLS_DIR` can make the wrapper execute arbitrary Python, which could execute a carrier; the normal default path is the documented REA static-analysis route, not direct carrier execution. Keep production paths fixed or validate test overrides so they cannot silently change the code being run. Never use loader-based execution as a substitute for REA analysis.

## Writes and residual risk

**Observation:** wrapper-owned run artifacts are directed to the guarded `outabs` (`producer.json`, carrier stdout/stderr, receipt/log and comparison outputs: `.ufo/waves/round-19/run-carriers.sh:286-295,313-328,335-347`). Its selftest fixture is created and removed under `/tmp`; its `$HOME` guard case asserts that no directory is created (`:59-66,196-213`). No direct wrapper write outside `runs/` was found. W20's required `carrier-guard check --record evidence/carrier-guard` intentionally writes check records outside runs, as specified by D3 (`.ufo/waves/round-20/gen-wave1.py:267-269`; `.ufo/waves/round-20/contract.md:46-49`); arm/adopt records there are likewise intentional.

**Inference / residual:** `run-carriers.sh` changes cwd to the wave (`.ufo/waves/round-19/run-carriers.sh:270`); `carrier-run.py` passes that cwd to subprocesses while setting a private `/tmp` TMPDIR (`.ufo/waves/round-17/tools/carrier-run.py:97-107,276-285`). The wrapper's output allowlist does not sandbox a child that independently writes to cwd. No real REA run was performed, so dependency-side writes outside `runs/` cannot be ruled out from this static review. Also, a pre-label guard check is a snapshot, not atomic protection; after the final label it does not attest post-run state.

## Verification and command exits

- **Observation:** `bash -n /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/run-carriers.sh` → exit 0 (syntax only; no script run).
- **Observation:** `test -e /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/run-carriers.sh` → exit 1 (no W20 runner at review time).
- **Observation:** `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -e 14f0260ad319ecc26994381b2415d5a999003375:.ufo/waves/round-19/run-carriers.sh` → exit 0.
- **Observation:** `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --no-ext-diff --unified=1 14f0260ad319ecc26994381b2415d5a999003375 -- .ufo/waves/round-19/run-carriers.sh` → exit 0, empty diff.
- **LSP:** unavailable: `read xd://lsp` returned “No such tool” and the mounted-device list has no LSP device. Text search was only a literal fallback; it is not semantic caller/reference evidence, and no semantic caller claim is made.
- No selftest, REA, Ghidra, or Go toolchain binary was run; no tools were installed.

Report: .ufo/waves/round-20/w1/ReviewRunCarriers.md
