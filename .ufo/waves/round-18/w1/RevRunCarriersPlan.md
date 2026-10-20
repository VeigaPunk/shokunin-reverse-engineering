# RevRunCarriersPlan — round-18 ten-carrier run plan

Seat: author-side advisory reviewer (`KaidokuR18.RevRunCarriersPlan`). Read-only; this file is my only write.
Scope: the plan to run 10 carriers (8 synthetic `s1246-*/s1250-*` + `calib-aether` + `calib-notesmd-cli`)
through `W17/tools` via `W18/run-carriers.sh` — env, session dirs, pin list, timeouts, wall estimate,
failure modes, L1 preconditions.

Anchor set used throughout: `W17` = `.ufo/waves/round-17`, `W18` = `.ufo/waves/round-18`, `LANE` =
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

Labels in this file: **[OBS]** = observed by command in this session (appendix C); **[INF]** = inference
from cited evidence, not measured.

---

## 1. State of the plan at review time

`W18/run-carriers.sh` landed at 12:31, after this review began (8183 B; `bash -n` exit 0). Its bytes are
reviewed in §1a, and each plan-level finding below is marked fixed/open against them. State table records
what each artifact was when first checked, then now:

| Artifact | State |
|---|---|
| `W18/run-carriers.sh` | absent at 12:24 → **present at 12:31**, 181 lines, reviewed in §1a [OBS] |
| `W18/predictions/carriers.tsv` | absent at 12:24 → **present**, 10 tab-separated rows, final newline, 3 fields each; labels `calib-aether`, `calib-notesmd-cli`, and the 8 `s12*` [OBS] |
| `W18/predictions/<label>.prediction.json` | **still absent** — `predictions/` holds only `carriers.tsv` [OBS] |
| `W18/tools/swiss-misread.py` | **still absent**; `W18/tools/` now holds `revpin.py`, `routed-defects.py`, `jj-red-before.py` [OBS] |
| `W18/measure.py`, `W18/verify.py`, `W18/controls.py` | absent at 12:24 → **present** by 12:36 (914/299/807 lines) [OBS] |
| r18 carriers | present, 8 files, `sha256sum -c SHA256SUMS` → 8×OK, exit 0 [OBS] |
| calibration carriers | `/usr/bin/aether` sha `06c91f55…006e`, `/home/vgpnk/.local/bin/notesmd-cli` sha `412dc53…002d` — both equal the r17 receipts (`runs/pro-aether/receipt.json`, `runs/pro-notesmd-cli/receipt.json`) [OBS] |
| lane working tree | dirty: ` M .ufo/waves/round-17/tools/compare.py`; `refs/heads/main` = `HEAD` = `origin/main` = `9011581d…470` [OBS] |
| plan text | `contract.md:133-136` (+ carrier/calibration text `:104-119`, measure text `:139-140`) [OBS] |

Consequence of the still-absent predictions: a run *today* would preflight clean (it checks the tsv, not
the per-label predictions) and then skip all ten rows with exit 2 per row and overall exit 1
(`run-carriers.sh:154-160`) — loud, but no REA analysis and no `compare.json`.

The contract sentence the script implements:
> `contract.md:134-136` — "Adapt `W17/run-carriers.sh`: labels from `W18/predictions/carriers.tsv`, tools
> from `W17/tools`, output `${RUNS_DIR:-W18/runs}/<label>`, pins the carrier, its prediction,
> `W18/tools/swiss-misread.py`, r16 `selection.py` and all Go data files."

§1a checks the implementation against that sentence and against §3; §3 remains the gap list.

---

## 1a. The runner as written (181 lines) — new findings and status of §3

Fixed by the script (verified by reading the cited lines):
- F3 coordinates 1–4: `cd "$W"` (`run-carriers.sh:140`), `TOOLS_DIR` defaults to `$W17/tools` (`:20`),
  prediction path absolute via `$PREDICTIONS_DIR` (`:21,155`), `--pin "$SWISS_MISREAD"` (`:167`).
  F3.5 (env) is not addressed → F5.
- Shared-input preflight once (`:132-138`), non-empty Go glob (`:141-142`), per-row skip for a missing
  carrier or prediction with `carrier-run.exit=2` and `overall=1` (`:154-160`).
- A real fixture-based `--selftest` with stub tools under `/tmp` (`:26-127`): every written path is under
  `$root` (carrier, prediction, `RUNS_DIR`, tools), the only lane-side access is reading the Go data dir,
  and it leaves no residue (observed `SELFTEST: CLEAN cases=9`, exit 0; `ls /tmp/r18-run-carriers-selftest.*`
  exit 2 afterwards).
- `bound`-gated compare preserved (`:171-177`), so a failed analyze with a bound log still compares.

Still open from §3: F1 (count), F2 (predictions unowned/absent), F4 (no row count; a last line without
`\n` still drops a label), F5 (no env), F6 (1500, no watchdog), F7 (session dirs unchanged), F9 (no carrier
sha check), F10 (tool sources unpinned), F11 (`rm -rf "$out"` unguarded at `:153`), F13 (no real-fixture dry mode).

### R1 — HIGH — the runner's `--selftest` cannot fail: a red case prints FAILED, then CLEAN, exit 0

`fail()` *returns* 1 instead of exiting (`run-carriers.sh:92`); every assertion is `… || fail "name"`
(`:96-118`); the function unconditionally ends with `echo "SELFTEST: CLEAN cases=$cases"; return 0`
(`:121-122`). There is no `set -e` (`:16` is `set -u` only), so a failed assertion never aborts.

Proof (appendix C): on a copy outside LANE, I replaced the stub's red marker test with `if False:`, which
makes the `fakeBad compare exit` case fail. Output:
`SELFTEST: FAILED fakeBad compare exit` **then** `SELFTEST: CLEAN cases=9`, exit 0. The item's acceptance —
"paste the exact last line and exit code" — would therefore certify the tool no matter which case regresses.

Independently, the mixed-run assertion is vacuous: `bash "$0" > … && fail "mixed-run exit (expected 1)"`
followed by `[ $? = 1 ] || true` (`:107-108`) passes whether the child exits 0 or 1.

Fix: `fail() { echo "SELFTEST: FAILED $1"; exit 1; }` (inside a function run in the main shell, `exit`
ends the script), and replace `:107-108` with
`bash "$0" > …; s=$?; [ "$s" = 1 ] || fail "mixed-run exit (got $s)"`.

### R2 — MEDIUM — the env overrides that select the tools are not recorded in any run artifact

`TOOLS_DIR`, `PREDICTIONS_DIR`, `SWISS_MISREAD`, `SELECTION_PY` (`:20-23`) are overridable, and the receipt
pins only their *inputs*; a measured pass with a non-default `TOOLS_DIR` leaves artifacts
indistinguishable from a default one. For the measured run: use defaults, and print the four resolved
paths once before the loop (or pin the tool sources, F10), so the run log binds producer bytes to output.

### R3 — LOW — the skip path deletes a prior run directory before deciding the label cannot run

`rm -rf "$out"; mkdir -p "$out"` (`:153`) precedes the carrier/prediction existence check (`:155`), so a
rerun with a still-missing prediction destroys the earlier attempt's retained `carrier-run.exit`. Under
the "no rerun to change a result" rule this matters only if the earlier attempt is evidence; move the
existence check before the `rm`, or move the old directory aside.

### R4 — LOW — the selftest's stub carrier-run is more lenient than the real tool

The stub writes a `receipt.json` (`{"error": …}`) and exits 2 on a missing pin (`:33-42`); the real
carrier-run writes **no** receipt on that path (`carrier-run.py:345-348`), so the `jq`-on-missing-receipt
branch is never exercised. The script's own skip path (`:154-160`) also bypasses the stub. Not a defect in
the runner, but the selftest proves less than it appears to.

### R5 — LOW — header line 5, "Reuses the round-17 tools unchanged", is stale

`compare.py` in the working tree already carries the round-18 `eof_reads`/`analyzer_errors_empty` code
(`git status` → ` M`). The sentence is harmless operationally but wrong as custody text; correct it.

---

## 2. Verdict

The carrier set, pin concept and the landed runner are sound in skeleton: the four hard-coded r17
coordinates are fixed, shared inputs are preflighted once, missing per-label inputs are loud, and the
`bound`-gated compare is preserved. Four defects are blocking before a measured pass:

1. **R1** — the runner's `--selftest` cannot fail (a red case prints FAILED then CLEAN, exit 0), so its
   acceptance evidence is worthless as written.
2. **F1** — the C3 count can be inflated from the claimed 8 to 10 by calibration predictions carrying
   `extra.eof_reads`.
3. **F2** — the per-label `*.prediction.json` files still do not exist and no item owns them; without
   `extra_expectations` the run is silently green while `measure.py` counts 0.
4. **F9/F10** — no carrier identity check and no tool-source pins, while the working tree is dirty and the
   runner's env overrides are unrecorded (R2).

The remaining medium/low gaps (F4 row count, F5 env, F6 watchdog, F7 session dirs, F11 `rm -rf` guard,
R3–R5) are cheap and listed below. The carrier matrix and the wall-time estimate are unaffected by any of
them.

---

## 3. Findings

### F1 — HIGH — calibration compare files can inflate the C3 metric from 8 to 10 (open)

- Claim: `claims.json:27` — "compared against a bound retained log: **0 -> 8**".
- Metric: `contract.md:139-140` — "C3 count of `W18/runs/*/compare.json` that carry an `extra.eof_reads`
  or `extra.analyzer_errors_empty` field". The implemented counter agrees and does **not** filter by label:
  `W18/measure.py:61` (`EXTRA_FIELDS`), `:66-68`, `:377`, `:444-447` count one per run directory and report
  every label in `c3.labels`.
- Mechanism: `W17/tools/compare.py:176` takes extras only from `prediction["extra_expectations"]`;
  `:201-209` emits a field entry `extra.analyzer_errors_empty` / `extra.eof_reads` **iff** the prediction
  carries that key. A `compare.json` with 10 eof-carrying predictions counts 10.
- The item text (`wave1-spec.json` item `RunCarriers18`) puts all ten labels in one `carriers.tsv`, so if
  the two calibration predictions also carry `eof_reads`, `measure.py`'s literal rule reports 10 ≠ 8.

**Fix (no new tool).** Keep the metric literal and choose the calib prediction vocabulary deliberately:
8 synthetic predictions carry `extra_expectations.eof_reads` + `analyzer_errors_empty`; `calib-aether`
carries the existing r17-style key `analyzer_errors_contain: "Go analysis failure"` (still a mechanical
assertion of the known failure, but **not** a metric key); `calib-notesmd-cli` carries only
snapshot/`language_compiler` keys. Then the count is exactly 8 and the calibration runs stay honest.
If instead the intent is to count 10, the claim at `claims.json:27` must be restated — do not silently
let the tool and the claim disagree.
[OBS for all anchors; INF that a eof-carrying calib prediction is the planned shape.]

### F2 — HIGH — `W18/predictions/<label>.prediction.json` has no owner and no defined schema; two distinct silent failures follow (open — files still absent)

- The runner must `--pin` "its prediction" (`contract.md:135`), i.e. `W18/predictions/<label>.prediction.json`.
- The `RunCarriers18` item only asks for `carriers.tsv`; `swiss-misread.py`'s output schema
  (`contract.md:110-117`: `predicted_eof_reads`, `predicted_failure`) is **not** `compare.py`'s prediction
  schema (`compare.py:8-14`; r17 exemplar `W17/predictions/pro-esbuild-0.27.7.prediction.json`:
  `expected.{…}` + `extra_expectations.{…}`). No item performs the translation.
- Failure A (loud): prediction absent at run time → `carrier-run.py:345-348` returns 2 **before**
  `receipt.json` is written (`:416-419`), so there is no receipt and no compare; the runner records
  `carrier-run.exit=2` for all ten. Diagnosable only from `carrier-run.stderr`.
- Failure B (silent green): prediction present but without `extra_expectations` → `compare.py` emits no
  `extra.eof_reads`, `all_match: true`, exit 0; the run log looks clean and `measure.py` counts **0**.
  This is the failure mode that can survive to the integrative pass.

**Fix.** L1 owns a pre-freeze translation step:
`W18/predictions/<label>.prediction.json` = `{expected: {untested_version, snapshot_label,
missing_bootstrap…}, extra_expectations: {eof_reads: <predicted_eof_reads>,
analyzer_errors_empty: <not predicted_failure>}}`, produced from the swiss-misread run and **committed**
before the first carrier. Add a preflight assertion that each of the 8 parses and has the key
`extra_expectations.eof_reads` (appendix A, P4).

Note: `eof_reads` must be the pair **as printed** by the log (`A, B`, e.g. `[17645861, 111938854]`), because
`log-extract` (new field) and `compare.py:207-209` compare exact list equality; `contract.md:115` calls the
first element `index`, while `W17/runs/pro-aether/logs/rea-ghidra-J5bcRT/ghidra.log:177` prints it as the
read offset. Record the semantics in the prediction, not just the values.

### F3 — HIGH — five r17 coordinates in the skeleton must change (items 1–4 fixed in the landed runner; item 5 is F5)

`W17/run-carriers.sh` (line numbers as in the file):

1. `:9` `W=…/.ufo/waves/round-17` and `:11` `cd "$W"` → r18 must `cd` to `W18` (so `predictions/…` and
   `${RUNS_DIR:-runs}` resolve under `W18`) while tool paths remain `$W17/tools/…`.
2. `:25` `tools/carrier-run.py` → `$W17/tools/carrier-run.py` (there is no `W18/tools/carrier-run.py`).
3. `:26` `"$W/predictions/$label.prediction.json"` → `$W18/predictions/…` (absolute; never let cwd decide).
4. `:26` pin list must add `--pin "$W18/tools/swiss-misread.py"` (contract `:135-136`).
5. `:23` `[ "$label" = "pro-op" ]` env rule can never fire for `s1246-*`/`s1250-*`/`calib-*` (see F6).

A copy that keeps `cd "$W"` *and* changes only the tool path will read r17 predictions for r18 labels:
`carrier-run` then fails the pin with `no such file` (exit 2) — loud, but the wrong-revision comparison is
one edit away from running. Keep prediction paths absolute.

### F4 — MEDIUM — empty or malformed `carriers.tsv` yields exit 0 with zero runs (false success; still open — no row count)

`W17/run-carriers.sh:17,38`: the `while IFS=$'\t' read -r label path kind` loop has no row count, no
duplicate check, and no final-line guard. Consequences: an empty tsv → loop never executes → `overall=0` →
**`run-carriers exit=0` with no `W18/runs`**; a space-delimited tsv → `label` swallows the whole line and
`path` is empty → `carrier-run` returns 2 (carrier unreadable); a last line without `\n` is skipped.

**Fix.** Accumulate `n`; when no `only` argument is given require `n == 10` and exit 1 otherwise; use
`while … || [ -n "$label" ]`; validate `[ -n "$label" ] && [ -n "$path" ] && [ "$kind" = … ]`, label regex
`^[A-Za-z0-9._-]+$`, no duplicate labels, and `[ -f "$path" ]` before the loop. Add `set -o pipefail` next
to `set -u` (`:8`); do **not** add `set -e` (it would abort the batch on the first nonzero step the script
is designed to record).

### F5 — MEDIUM — `REA_GHIDRA_STARTUP_TIMEOUT_MS` decision must be explicit; the r17 rule cannot fire (open — runner sets no env)

`W17/run-carriers.sh:23` sets `REA_GHIDRA_STARTUP_TIMEOUT_MS=900000` only for `pro-op`, and the r17 receipt
confirms that is the only label that got it (`runs/pro-op/receipt.json` `rea_ghidra_env`); every other r17
receipt records `{}`. Neither `aether` nor `notesmd-cli` (both present in r18) needed it in r17, and no r18
label is `pro-op`, so a literal adaptation runs all ten with REA's default startup timeout.

Options, both defensible, must be chosen and written down:
- (i) `export REA_GHIDRA_STARTUP_TIMEOUT_MS=900000` once for the whole run. It is inherited by the child
  (`carrier-run.py:280` allows `REA_GHIDRA_*`) and recorded per receipt (`carrier-run.py:324`), so the
  choice is auditable. Cost: a genuine startup hang can burn up to 900 s before the step deadline
  (`carrier-run.py:462-472`). Benefit: the one carrier with a known `Go analysis failure` path
  (`calib-aether`) and the eight that intentionally re-enter that reader are not aborted by a loaded host.
- (ii) set nothing, for strict parity with r17's aether/notesmd receipts.

I recommend (i), **and** state in the run log that r18 used the env globally while r17 used it only for
`pro-op` — otherwise a later reader will treat the receipt field as noise.

### F6 — MEDIUM — timeouts: keep `--timeout 1500`; the r17 maximum is not the right basis for tightening (open — no watchdog)

Observed r17 per-step durations (receipt `steps.*.started_at_utc`/`ended_at_utc`; tabulation in appendix C):

| label | size (B) | inspect (s) | analyze (s) |
|---|---|---|---|
| calib-shfmt | 3,601,168 | 0.92 | 36.64 |
| pro-containerd-shim | 9,341,024 | 0.71 | 50.65 |
| pro-notesmd-cli | 4,808,888 | 0.71 | 41.14 |
| pro-aether | 20,694,888 | 0.76 | 76.24 |
| pro-esbuild-0.21.5 | 9,707,520 | 0.97 | 96.79 |
| calib-esbuild-0.25.12 | 10,358,936 | 0.71 | 104.30 |
| pro-esbuild-0.27.7 | 11,120,788 | 0.66 | 104.79 |
| pro-op | 47,161,506 | 0.71 | 222.21 |

`--timeout 1500` (`W18/run-carriers.sh:166`) is per step, so an uncapped batch ceiling is
10 labels × 2 steps × 1500 s = 30,000 s (8 h 20 m). Keeping 1500 gives 6.7× the worst r17 analyze and
≥34× the two calibration re-runs. Do **not** tighten toward the r17 maximum: the failing-reader path is the
slow outlier (222 s vs a 76–105 s median at comparable sizes), and no r18 synthetic has ever been analysed.

Recommended: keep 1500 per step and add a per-label watchdog,
`timeout --signal=TERM --kill-after=30 2400 python3 -I -B …`. A legitimate worst case is
inspect ≈1 s + analyze 1500 s ≈ 1503 s, so 2400 s never cuts a real run; the ceiling becomes
10 × 2400 s = 6 h 40 m. If a tighter ceiling is wanted, lower the per-step timeout to 900 s (4× the worst
r17 analyze) and the watchdog to 1500 s → 4 h 10 m. Either pair is defensible; an uncapped loop is not.
Note the watchdog returns 124 and `carrier-run` then writes no receipt at all (the receipt is written at
`:416-419`), so the label's diagnosis lives in its stdout/stderr and any logs already copied under
`out/logs/`.

### F7 — MEDIUM — "session dirs" are owned by `carrier-run.py`, not the script; the plan has no lever there (unchanged)

`carrier-run.py:299` creates a fresh private parent `tempfile.mkdtemp(prefix="kr17-rea-", dir="/tmp")`;
`:303` sets the session glob under it; `:281` forces `TMPDIR` to that parent; `:322` records it;
`:403-410` asserts no leftovers and removes it when empty. The runner therefore cannot (and must not try to)
place sessions: any `TMPDIR` set by `run-carriers.sh` is overwritten. Two consequences for the plan:

- The prefix stays `kr17-` in round 18. Harmless, but r18 receipts will name `/tmp/kr17-rea-*`; custody
  checks must not read that as an r17 artifact. (Do not change the prefix: `carrier-run.py`'s only
  contracted edit is the mid-map retention, `contract.md:129-132`.)
- The only script-side session obligations are disk headroom and residue: `/tmp` has 119 GB free [OBS] and
  no `/tmp/kr17-rea-*` or `/tmp/rea-ghidra-*` exists [OBS]. Post-run, assert per receipt
  `bound_sessions` length 1, `unbound_sessions == []`, `session_parent_leftovers == []`.

### F8 — MEDIUM — compare runs on `carrier-run` exit 2 (correct), but the aggregate exit conflates "analysis failed" with "prediction mismatched" (preserved)

`receipt.json` is written at `carrier-run.py:416-419`, **before** the exit gates at `:423-434`; so
`bound_sessions` is readable and the compare step runs even when `carrier-run` returns 1 (pin drift) or 2
(analyze nonzero/timeout). Preserve the `bound` gate (`W18/run-carriers.sh:171-177`, adapted from `W17/run-carriers.sh:30-35`), not `rc`.

The aggregate at `:37` (`rc==0 && compare==0`) is the honest single bit, but for C3 a compare mismatch is
*evidence*, not a runner failure — `claims.json:27` itself says "compare exit per carrier reported, match or
not". Requirement for the plan: the per-label log line must always print `carrier-run=<rc> compare=<rc>`
(`:36` already does), and the run must never be re-executed to turn a mismatch into a match. A second run
after seeing the result is a calibration defect, not a retry.

### F9 — LOW — pins prove stability, not identity; add the one identity check `pins.py` explicitly cannot make (open)

`W17/tools/pins.py:8-14` states the limit: a pin pair proves "same bytes at two instants", never that the
bytes are the intended carrier. The runner pins 146 paths in r17 (143 Go data files + carrier +
`selection.py` + prediction) and none of them is the intended-identity check. So before the loop the script
should verify all 8 synthetic carriers against `/home/vgpnk/.local/share/kaidoku-r18/carriers/SHA256SUMS`
(`sha256sum -c` from that directory) and the 2 calibration carriers against the r17 receipt hashes
(`06c91f55…`, `412dc53…`; already verified here by `sha256sum`, exit 0). Without this, a rebuilt or
swapped carrier runs cleanly and pins perfectly.

### F10 — LOW — pin the tool bytes the run actually executes; the tree is dirty right now (open)

`git status --porcelain --untracked-files=no` → ` M .ufo/waves/round-17/tools/compare.py` [OBS], and
`compare.py:197-209` already contains the round-18 `eof_reads`/`analyzer_errors_empty` code. The run's
comparison output therefore depends on working-tree bytes with no revision identity; r17 pinned no tool
source. Cheap fix: add `--pin` for `W17/tools/{carrier-run.py,pins.py,log-extract.py,compare.py}` and
`W18/tools/swiss-misread.py` (≈50 KB hashing; the 143-file Go snapshot already costs ~92 MB per snapshot).
This closes the producer-identity question (`corpus/lessons/round-17-verifier-spotcheck.md:139`)
for the C3 artifacts without a new tool.

### F11 — LOW — `rm -rf "$out"` needs a guard for `RUNS_DIR` (open — `run-carriers.sh:153`)

`W18/run-carriers.sh:151-153` (inherited from `W17/run-carriers.sh:19-21`) deletes `${RUNS_DIR:-runs}/$label` unconditionally. If `RUNS_DIR` resolves into
`W17/runs` the round violates the round-18 non-goal "no edit of round-17 retained receipts/logs"
(`claims.json`, `non_goals`). Add: resolve `RUNS_DIR` with `realpath -m`; accept only paths under `W18` or
under `/tmp`; require labels to match `^[A-Za-z0-9._-]+$` before the `rm`.

### F12 — LOW — a failed preflight leaks one empty `/tmp/kr17-rea-*`; "zero mutation" holds for the lane, not for `/tmp` (carrier-run; unchanged)

`carrier-run.py:299` creates the private session parent before the pin snapshot at `:336`. The pin-failure
return (`:345-348`) and the `inspect-go-binary`-failure return (`:355-360`) both bypass the cleanup block at
`:403-410`, so each failed label leaves an empty `/tmp/kr17-rea-*` directory behind. (The
carrier-unreadable return at `:291-294` precedes `mkdtemp`, so it is clean.) No functional risk: the session
glob is scoped to one private parent (`:303`), so stale empty parents cannot enter `session_dir_baseline` or
be mistaken for REA roots. But a batch that dies on missing predictions leaves ten empty parents, which
will make a later "no `/tmp` residue" check read as contamination. Preflight (appendix A P2/P4/P5) avoids
it; if it happens, `rmdir /tmp/kr17-rea-*` before retrying.

### F13 — LOW — a dry mode against the *real* ten rows and pins is still missing (`--selftest` runs stubs)

The item asks `bash -n` plus a "dry-check with a fake `tools` dir"; the landed `--selftest`
(`run-carriers.sh:26-127`) is stronger in that it executes the real control flow against stub tools, but it
never validates the real `carriers.tsv`, the real carrier paths or the real pin list. A `--dry-run` mode
that (1) validates `carriers.tsv` per F4, (2) verifies every pin exists, (3) prints each label's exact argv
and timeout, (4) creates nothing and exits 0 gives the L1 the whole precondition list (appendix A) in one
command. Default behaviour is unchanged, so no contract conflict.

---

## 4. Wall-time estimate

Model: wall per label ≈ `inspect + analyze + 0.26 s` (r17: 741 s wall from `runs/run-log.txt` vs
`sum(analyze)=732.75 s` + `sum(inspect)=6.17 s`; overhead 2.08 s over 8 labels) [OBS].

| component | per label | count | total |
|---|---|---|---|
| synthetic analyze, central 30 s [INF] | 31.06 s | 8 | 248.5 s |
| `calib-notesmd-cli` (r17 41.14 s) | 42.1 s | 1 | 42.1 s |
| `calib-aether` (r17 76.24 s) | 77.3 s | 1 | 77.3 s |
| **central total** | | | **≈ 368 s ≈ 6 min 08 s** |
| pessimistic synthetic 45 s [INF] | 46.06 s | 8 | 488 s ≈ **8 min 08 s** |
| pessimistic synthetic 60 s [INF] | 61.06 s | 8 | 608 s ≈ **10 min 08 s** |

The 30 s central figure is an extrapolation from the two smallest r17 carriers (3.6 MB/36.6 s,
4.8 MB/41.1 s) downward for a 2.2 MB binary whose program is a few dozen functions; size does not predict
analysis time in r17 (`containerd-shim` 9.3 MB/50.7 s vs `esbuild` 9.7 MB/96.8 s), so treat 30 s as a floor
plus startup, not a fit [INF]. Cold `npx` adds an unknown one-off (r17's `inspect-go-binary` steps are
0.66–0.97 s, so the package was warm [OBS]); an offline host fails at the first step, not late.
Absolute ceilings (not estimates): uncapped, 10 labels × 2 steps × 1500 s = **30,000 s (8 h 20 m)**; with
the F6 watchdog at 2400 s/label, **6 h 40 m**; with 900 s/step + a 1500 s watchdog, **4 h 10 m**. The
*expected* wall is the 6–10 min table above in every configuration.

---

## 5. Failure modes, ranked by "can it look green"

| # | Mode | First observable | Cost / consequence |
|---|---|---|---|
| 1 | `carriers.tsv` empty or last line without newline | `run-carriers exit=0`, no `W18/runs` | **false success**; C3 count 0 |
| 2 | prediction present but no `extra_expectations` | `compare.json` `all_match: true`, no `extra.eof_reads` | **silent green**; measure 0 |
| 3 | prediction absent | runner skip: stderr line, `carrier-run.exit=2`, **no receipt**, no REA child (`run-carriers.sh:155-160`) | 10× instant; loud |
| 3b | `swiss-misread.py` absent | preflight exit 1 before any label (`run-carriers.sh:132-138`) | instant |
| 4 | cold `npx`/offline | `inspect-go.exit` null → exit 2, no receipt (carrier-run.py:355-360) | first label fails, rest repeat |
| 5 | Ghidra startup exceeds REA default | `analyze.timeout: true` → exit 2; receipt and bound log still written | up to 1500 s |
| 6 | Go-analysis failure path (expected for swiss+methods) | `analyzer_errors` non-empty in log; analyze may still exit 0 (r17 aether did) | data, not failure |
| 7 | session log lost in the 0.5 s poll race | `bound_sessions: []` → no compare | count short; r17 bound 8/8 [OBS], low risk |
| 8 | mid-run pin drift (carrier rebuilt, Go data touched) | `pins_compare.equal: false` / `mid_run_drift_steps` non-empty → exit 1 (carrier-run.py:423-424) | rerun only with the drift fixed |
| 9 | two JVMs at once (another seat runs REA) | host memory pressure, possible OOM-kill of the analyze step | sequencing precondition (A7) |
| 10 | aether's r18 EOF pair differs from r17's | `compare` mismatch on `extra.eof_reads` | not a refutation; see §6 |

jq/dependency note: in the interactive harness `jq --version` reports `jaq 3.1.1` because the harness
provides a `jq` **builtin**; in a real `bash` script the loader resolves `~/.local/bin/jq` or `/usr/bin/jq`,
both **jq-1.8.2**, and `jq -r '.bound_sessions[0] // empty'` behaves correctly (verified under
`env -i … bash -c`, exit 0). So the `run-carriers.sh:172` dependency is safe as written; it is only a
portability wrinkle worth removing if the script is ever run with a restricted PATH [OBS].

---

## 6. Calibration / depth notes (what the run will and will not establish)

- Both calibration carriers are Go ≥ 1.24 Swiss builds (`aether` go1.25.14, `notesmd-cli` go1.25.8;
  buildinfo scan, appendix C) [OBS]. `notesmd-cli` produced no `Go analysis failure` in r17 while `aether`
  did, so the swiss axis alone does not predict failure; the `{methods, nomethods}` axis is the intended
  discriminator. The 2×2×2 pair therefore contains a real negative control (`noswiss` + methods) and a
  within-swiss control (`swiss` + nomethods), which is the strongest part of the design [OBS for the r17
  contrast; INF for the causal reading].
- `aether`'s EOF pair `[17645861, 111938854]` is one sample; its determinism across runs is unmeasured
  [INF]. If the r18 re-run yields a different pair, that is evidence about Ghidra's read order, **not** a
  refutation of the mechanism the eight synthetic carriers test. Pre-register this reading before the run;
  the calibration reference remains the r17 log at
  `runs/pro-aether/logs/rea-ghidra-J5bcRT/ghidra.log:97,177`.
- The r18 re-runs add 119 s (32 % of the central estimate) but buy the only within-round same-identity
  replication (same REA 6.5.0 argv, same Ghidra install, same carrier sha256). Keep them.
- `log-extract.py:204-205` already records `analyzer_errors` from `ERROR` + `Golang*` components, which is
  what the new `analyzer_errors_empty` rule consumes; the new `symbol_analysis_failures` field is additive
  evidence but is **not** the comparison source. Do not assume it changes a verdict.

---

## 7. No resume path (honest statement)

This harness has no resume/continuity machinery: `carrier-run.py` contains no resume or preflight-rejection
code, and `W18/run-carriers.sh:153` deletes the output directory before each label, so a re-run is a full
re-analysis, not a continuation. The analogous invariants I checked instead are the receipt-write-before-
exit-gate ordering (`carrier-run.py:416-419` before `:423-434`, which is what keeps a failed analysis's log
comparable) and the zero-mutation-on-preflight-failure behaviour: a missing pin returns at `:345-348`
before any REA child is started, and an unreadable carrier returns at `:291-294` before `mkdtemp`. A failed
preflight writes only the `out_dir` the script already created and, for the pin/inspect-go paths, one empty
`/tmp/kr17-rea-*` parent (F12); it starts no REA child, writes no `receipt.json`, and touches nothing in
the lane or in `RUNS_DIR` beyond the per-label directory.

---

## Appendix A — Preconditions the L1 must check (run before committing to the batch)

Each check is cheap and read-only; P1–P6 are blocking.

1. **Revision and cleanliness.** `git -C LANE status --porcelain --untracked-files=no` must be empty, or
   F10's tool pins must be in place; `git rev-parse refs/heads/main` must equal `HEAD` and `origin/main`.
2. **Predictions frozen.** `git cat-file -e <rev>:W18/predictions/carriers.tsv` and one
   `<label>.prediction.json` per row (all ten). A tsv that exists only in the working tree does not satisfy
   `contract.md:15` ("after predictions are frozen in Git") or `:104-107`'s label/calibration definition.
3. **Carrier identity.** Ten rows; eight sha256 match
   `~/.local/share/kaidoku-r18/carriers/SHA256SUMS` (`sha256sum -c`, exit 0 demonstrated here);
   `calib-aether` = `06c91f55…006e`, `calib-notesmd-cli` = `412dc53…002d`.
4. **Predictions valid.** Each of the eight parses and has `extra_expectations.eof_reads` (list of
   `[int,int]`) and `extra_expectations.analyzer_errors_empty` (bool); the two calib files must **not**
   carry those two keys if the claim's 0→8 is to hold (F1).
5. **Tools green.** `swiss-misread.py --selftest` exit 0 and its two calibration gates (`aether` pair,
   `notesmd` no-failure) pass; `W17/tools/{pins,carrier-run,log-extract,compare,receipt-validate}.py
   --selftest` each exit 0 (r17 verify runs exactly this set, `W17/verify.py:84-89`).
6. **Runtime warm.** One `npx -y rea-agents@6.5.0` invocation succeeds quickly; `GHIDRA_INSTALL_DIR` is
   set (`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` [OBS]) and `JAVA_HOME` points at a JDK
   (`/usr/lib/jvm/java-21-openjdk` [OBS]); `python3 -I -B` runs (3.14.8 [OBS]).
7. **Exclusive host.** No `analyzeHeadless`/`rea-agents … analyze` process is running
   (`pgrep -af` → only the idle `rea-agents@6.5.0 mcp` bridge, pid 3221 [OBS]); the L1's sequential rule is
   what makes the ten analyses comparable.
8. **Space and residue.** `df -h /tmp` → 119 GB free; no `/tmp/rea-ghidra-*` or `/tmp/kr17-rea-*` [OBS].
9. **Output target.** `${RUNS_DIR:-W18/runs}` resolves under `W18` (not `W17`), is absent or writable, and
   F11's guard passes.
10. **Dry run.** Once F13 lands, `run-carriers.sh --dry-run` prints ten labels, ten existing carriers,
    148+ existing pins, and the exact argv/`--timeout`, creates nothing and exits 0. Until then, `--selftest`
    plus P1–P9 checked by hand are the gate (and read R1 before trusting its exit code).

## Appendix B — Post-run acceptance (assert, do not infer)

Per label: `carrier-run.exit` recorded; `receipt.json` with `carrier.sha256_pre == sha256_post`,
`pins_compare.equal: true`, `mid_run_drift_steps: []`, `bound_sessions` length 1,
`unbound_sessions: []`, `session_parent_leftovers: []`. Ten `compare.json` files exist; per-label
`all_match` reported verbatim, including any mismatch. `receipt-validate.py` exits 0 on all ten (`W18/verify.py:201` runs exactly this; `W17/verify.py:93` is the
same pattern). `measure.py <rev>` C3 count equals 8 with `all_match` per label, and its
`open_count`/`live_count` are unaffected by the runs. `runs/run-log.txt` present with start/end per label
so wall time is reconstructible without the receipts (`W17/runs/run-log.txt` format).

## Appendix C — Commands run (exit codes as observed)

| Command | Exit |
|---|---|
| `ls -la W18/ W17/` (two dirs) | 0 |
| `read W18/run-carriers.sh` | tool: path not found |
| `ls W18/predictions W18/tools` | 2 (`predictions` absent; `tools/revpin.py` present) |
| `sha256sum -c SHA256SUMS` in `~/.local/share/kaidoku-r18/carriers` | 0 (8×OK) |
| `sha256sum /usr/bin/aether /home/vgpnk/.local/bin/notesmd-cli` | 0 (hashes match r17 receipts) |
| `sed -n '280,440p' W17/tools/carrier-run.py` | 0 |
| `grep -n 'private_root = tempfile.mkdtemp…' W17/tools/carrier-run.py` | 0 (line 299) |
| `grep -n 'if "eof_reads"' W17/tools/compare.py` | 0 (line 207) |
| `grep -n 'eof_reads\|symbol_analysis_failures' W17/tools/log-extract.py` | 1 (neither field yet) |
| `grep -c 'Unable to read past EOF' W17/runs/*/logs/*/ghidra.log` | 0 (one hit, `pro-aether`) |
| `git -C LANE status --porcelain --untracked-files=no` | 0 (` M …/compare.py`) |
| `git -C LANE rev-parse --verify {refs/heads/main,HEAD,refs/remotes/origin/main}^{commit}` | 0 (`9011581d…470` ×3) |
| python3 buildinfo scan of the 8 carriers | 0 (versions/GOEXPERIMENT as cited) |
| `df -h /tmp` | 0 (119 GB avail) |
| `pgrep -af 'analyzeHeadless\|rea-agents\|Ghidra'` | 0 (one idle MCP bridge) |
| `type -a jq` (harness interpreter) | 0 (builtin + two paths; `jq --version` → jaq 3.1.1) |
| `env -i PATH=/usr/bin:/bin:/home/vgpnk/.local/bin bash -c 'jq --version; … // empty'` | 0 (jq-1.8.2, correct output) |
| `/home/vgpnk/.local/bin/jq --version` | 0 (jq-1.8.2) |
| python3 tabulation of r17 receipts | 0 (sum analyze 732.75 s, inspect 6.17 s) |
| `bash -n W18/run-carriers.sh` | 0 |
| `bash W18/run-carriers.sh --selftest` | 0 (`SELFTEST: CLEAN cases=9`) |
| `ls -d /tmp/r18-run-carriers-selftest.*` after selftest | 2 (no residue) |
| `cat -A W18/predictions/carriers.tsv` + `wc -l` | 0 (10 rows, tab-separated, `$`-terminated) |
| `cp run-carriers.sh /tmp/… && sed -i 's/if "COMPARE_FAIL" in body:/if False: …/' && bash /tmp/… --selftest` | 0 (`SELFTEST: FAILED fakeBad compare exit` **then** `SELFTEST: CLEAN cases=9` — R1) |
| `rm -f /tmp/kr18-selftest-probe.sh` | 0 |
| `grep -n 'fail()\|SELFTEST: CLEAN\|rm -rf\|--timeout\|jq ' W18/run-carriers.sh` | 0 (anchors cited in §1a) |

No tool was installed; nothing was written outside this report and the throwaway `/tmp` probe (removed).
