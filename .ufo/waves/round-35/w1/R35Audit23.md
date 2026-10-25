# R35Audit23 — static/dynamic execution boundary audit (wave 1)

Seat: `R35Audit23` (executor/leaf). Item: *Audit static/dynamic execution boundary. Read-only or private /tmp only; no lane writes.* Milestone: build evidence and first falsifications. All commands ran with cwd = lane root; only the file you are reading was written into the lane. No VCS mutation, no network, no subagent dispatch.

## 1. Instrument identity (frozen pins hold)

| file | sha256 (worktree) | canonical pin (claims-canonical.json) | match |
|---|---|---|---|
| `tools/round-35/c1-coverage-counter.py` | `e28792c7e54fcfa2185fe12f07c9e3eb328652d405e98d1ffaf2737b28d24220` | same | yes |
| `tools/round-35/c2-calibration-counter.py` | `576c14dd95c0a54b2de05b765d171b25429a893289b85516258e83daa9179b94` | same | yes |

Freeze snapshot: `git show 2323d197456f1328459d9420aff025cffbcb3e27:.ufo/waves/round-35/claims-canonical.json` sha256 = `1b985540…` = worktree file. The counter's freeze-read path (claims file at `--freeze`) resolves to the canonical commit `2323d197` (first commit adding `claims-canonical.json`; log: `2323d197 round-35: canonicalize claim snapshot and counters before any claim score`).

## 2. Static execution boundary — evidence

Code audit (both counters, full read):
- All data access is via subprocess `git -C <root> show|ls-tree|log` on the given revision. No `open()`/`read()` of any worktree content file in the `check()` path; the only `open()` calls are `--json-out` (explicit, path chosen by caller) and stdio. No network, no HTTP, no source fetch at score time.
- Production args required: `--root --rev --freeze` (C1), `--root --base --rev --freeze` (C2); missing → exit 2. `-I -B` (isolated, no bytecode) is the documented invocation; selftests re-invoke the counter with `-I -B`.

Runtime proof (`strace -f -qq -e trace=openat,open,connect,socket` on C1 at base `aa04633`):
- network syscalls: 0
- lane-touching opens: 7 total, all `O_RDONLY`; 0 with write flags:
  - `.git/HEAD` (5), `.git/config` (15, via child git), `.git/packed-refs`, `.git/refs/`, `.git/objects/…` blobs (read-only), `.git/objects/info/commit-graph*`, `.git/shallow`, `.git/info/grafts`, `.git/objects/pack/multi-pack-index`
  - the counter script itself (`tools/round-35/c1-coverage-counter.py`, read-only — inherent to executing the instrument)
- no worktree content path (`corpus/…`, `PROVINCE.md`, `SKILL.md`, `.ufo/waves/round-35/assimilation/census-start.txt`, etc.) was ever opened; all such data reached the counter only as `git show <rev>:<path>` object bytes. Static boundary confirmed.

## 3. Dynamic execution boundary — observations (advisory)

- `git` binary is resolved from PATH at score time (git 2.56.0 here); no version pin, no environment cleaning beyond `-I -B`. Counter output depends on git CLI behavior (e.g. `%cI` timestamps, `ls-tree -r --name-only`).
- `--rev`/`--freeze`/`--base` accept any git revision expression. The frozen design scores at full commit hashes (base `aa04633…`, instrument `d2729cba…`, freeze `2323d197…`); scoring with a moving ref (branch/`HEAD`) would be non-deterministic. Advisory: score only full hashes.
- The counter executes from the worktree file (checked against the pin, §1). If a future run uses different bytes, the pin check (exit 2 on predicate mismatch only) will not catch it; the instrumentation guard is the receipt hash, not runtime enforcement.

## 4. First falsifications (all reproduced, read-only)

| probe | command | result |
|---|---|---|
| C1 do-nothing control at base | `python3 -I -B tools/round-35/c1-coverage-counter.py --root <lane> --rev aa04633a686d49756763b1feed4be6830d5bb479 --freeze 2323d197456f1328459d9420aff025cffbcb3e27` | exit 1; 8 fails: entry_missing ×2, registry_row_missing S125/S129, province_missing ×2, readme_missing ×2 |
| C2 do-nothing control at base | `… c2-calibration-counter.py --root <lane> --base aa04633… --rev aa04633… --freeze 2323d197…` | exit 1; 8 fails: D1_census_start_missing, D2_lesson_missing, D3_source_missing, D3_verified_at_missing, D3_recheck_missing, D3_source_not_s106, D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4, D4_section_missing:### Round-34 run-6 instrument registry |
| C1 at instrument rev (pre-data) | `… --rev d2729cba895b8664f3ccb27196091494f3cda83b --freeze 2323d197…` | exit 1; same 8 fails as base |
| C2 at instrument rev (pre-data) | `… --base aa04633… --rev d2729cba… --freeze 2323d197…` | exit 1; D1_no_sources_change_after_base (SOURCES untouched by then) + same D2–D4 fails |
| claims file absent at freeze | `--freeze 13d7a8152f7f80cb2499200056a556fa932c1d2c` (pre-canonical) | exit 2 `claims file absent at freeze revision` (both counters) |
| predicate tamper | temp repo: `claims-canonical.json` predicate altered; run C1 with `--freeze HEAD` | exit 2 `predicate mismatch between counter and claims file` |
| selftests | `--selftest` (both counters) | `C1_SELFTEST: ok green=0 red=1`; `C2_SELFTEST: ok green=0 red=1` — green passes, red fails as designed |
| json-out | `--json-out /tmp/c1-receipt.json` | receipt written only to /tmp; shape: instrument/predicate/revision/freeze/checks/failing/pass; exit 1 with `pass:false` |

Base control failures match the committed red receipts byte-for-byte (`controls/c1-do-nothing.json`, `controls/c2-do-nothing.json`), confirming the controls were committed before data and are reproducible.

## 5. Boundary/limit notes

- Lane limits honored: no lane writes beyond this report; scratch under /tmp only; no `find`/`du` under `/fast/scratch`; no nested delegation/background work; no VCS mutation.
- Known recorded setup debt (not caused here): `freeze-status.md` documents the round-34 gate rejecting the earlier freeze (`f1ea3a6d`, pin mismatch) and canonical `claims-canonical.json` superseding `claims-frozen.json`; §1 shows current pins match the canonical snapshot, so the supersession is internally consistent.
- Advisory defects (not blocking): (a) D-1 compares the *latest* commit touching `census-start.txt` vs the *first* post-base `SOURCES.md` change — a benign later census edit would fail D-1 even if the initial commit was timely; the predicate says "committed no later than", so using first-commit time would match the wording more exactly. (b) `hashlib`, `datetime` (C1) and `os` (C2) imports are unused — cosmetic only. (c) `text=True` decoding relies on locale default encoding; ASCII content only, non-issue here.

## 6. Verdict

Execution boundary is static as claimed: zero network, zero worktree reads/writes at score time; all evidence read through immutable git objects. Controls behave as frozen: base fails (exit 1) identically to the pre-data red receipts; unevaluable and tamper probes exit 2; selftests green/red pass. No falsification of the frozen claims or counters was found at any revision probed; first falsifications are the expected pre-data failure states listed in §4.
