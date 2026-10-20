# SimplifyR17Tools — w2 falsify: dead code / overlap after integration

Status: read-only, advisory. No pre-existing lane file was edited; this report is the only file I
added, and no commit was made. All citations resolve on
**HEAD `da64646adcb19c1ede7537b799b8c7d283fe43da`** via `git show HEAD:<path>`. During review the
working tree drifted by one line (`run-carriers.sh:14` `out="runs/$label"` → `out="${RUNS_DIR:-runs}/$label"`);
it does not touch any finding, and every anchor below is the HEAD text. Labels: **O** observed by a
command or a direct read; **I** inference. Scratch copies used for the two-line validator proof live
under `/tmp/r17check`; nothing was written under the lane except this report.

Axes: calibration (C1), depth (C2), no-harm (retained artifacts), re-runnability (registry/measure).
Move rule: keep a deletion only if no C1/C2 consumer and no retained receipt loses its instrument.

## F1 — HIGH — `receipt-validate.py` cannot validate any produced receipt (integration break)

O. Producer writes `steps` as a **mapping**; validator requires a **list**.

- `tools/receipt-validate.py:98` `if isinstance(receipt.get("steps"), list) and isinstance(`; `:284`
  `for index, step in enumerate(receipt.get("steps") or []):`.
- Producer: `tools/carrier-run.py:275` `"steps": {}`, keys at `:312` (`inspect-go-binary`), `:331`
  (`analyze`), `:338` (`search:<name>`), assignment at `:349` `receipt["steps"] = steps`.
- `jq -r '.steps|type' runs/calib-shfmt/receipt.json` → `object`; same for all 8 receipts.

O. Command and output (explicit 8 receipt paths):
`python3 -I -B tools/receipt-validate.py runs/calib-shfmt/receipt.json runs/calib-esbuild-0.25.12/receipt.json runs/pro-aether/receipt.json runs/pro-containerd-shim/receipt.json runs/pro-esbuild-0.21.5/receipt.json runs/pro-esbuild-0.27.7/receipt.json runs/pro-notesmd-cli/receipt.json runs/pro-op/receipt.json`
→ `exit 1`, `.counts = {"invalid": 8, "receipts": 8, "unreadable": 0, "valid": 0}`, every receipt
`kind: "unknown"`, single finding `{"code": "unrecognized_shape"}`. 306 checks were still performed
per receipt (the digest walk runs), but the verdict is fixed to invalid.

O. Why the green selftest did not catch it: the fixture fabricates the list shape —
`tools/receipt-validate.py:469-470` `"steps": [{`. No producer emits that shape.

O. This is the knowledge entry's own recheck command:
`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3` (`recheck:`) runs `receipt-validate.py`
on `runs/<label>/receipt.json`; running it now exits 1 on `runs/calib-shfmt/receipt.json`. The C2
capability gate (`w1/ConnCapabilityHistory.md:70` "each `receipt-validate.py` exit 0") and the
registry row `SKILL.md:536` ("0 valid, 1 digest/pin/field finding") are therefore false against the
produced artifacts.

Smallest fix — **two** edits; both are required (O, proved by patched copies):
1. `:98` accept the container the producer writes: `isinstance(receipt.get("steps"), (list, dict))`.
2. `:284` iterate values for a mapping: `_items = list(steps.values()) if isinstance(steps, dict) else (steps or [])`, then `enumerate(_items)`.
With both edits: `kind: "carrier"`, `valid: true`, `checks_performed: 336`, **exit 0**. With edit 1
only: exit 1 with two `{"code": "field_type", "detail": "step is not an object", "where": "$.steps[0]"}`.
Tradeoff: fixing the validator (not the producer) is the only option that preserves the 8 retained
receipts; changing `carrier-run.py` to a list would invalidate every receipt already committed.

## F2 — MEDIUM — mid-run pin drift is recorded but never asserted (C1 hole)

O. `tools/carrier-run.py:425-433` snapshots the full pin set every 30 s and, on mismatch, writes
`rec["pins_changed_during_run"] = {changed, missing}`. The run verdict is decided only by the final
pre/post compare (`:376-377` → exit 1) and the analyze exit (`:378-379` → exit 2); a mutate-then-restore
between the 30 s samples still exits **0**.

O. No consumer reads the field: `grep -rn pins_changed_during_run tools/` → only
`tools/carrier-run.py:430`; `receipt-validate.py` has no match. Proof: I injected
`steps.analyze.pins_changed_during_run={"changed":["/usr/bin/shfmt"],"missing":[]}` into a copy of
`runs/calib-shfmt/receipt.json`; the two-line-fixed validator returned `valid: true`, exit 0.

I. That reintroduces exactly the R16-PROVENANCE defect class the round exists to discharge: the only
mechanism able to see intra-run instability produces a field nobody asserts. The pins docstring's
"same bytes at two instants" caveat (`tools/pins.py:8-15`) remains true; the 30 s sample is not used
to bound the claim.

Smallest fix (one place): in `receipt-validate.py`'s carrier branch, after `CARRIER_STEP_REQUIRED`,
flag any `pins_changed_during_run` whose `changed` or `missing` is non-empty
(`{"code": "pins_changed_during_run", "where": ...}`), 6 lines. Alternative: delete the mid-run block
and the field, and drop "every 30 s" from `SKILL.md:532`; that loses the only intra-run signal, so the
validator wiring is the no-harm move.

## F3 — MEDIUM (wave-1 calibration) — T4 is unsafe to apply; the carrier digests have two live consumers

`w1/SimplifyTools.md:49-51` (T4) recommends dropping `carrier {sha256_pre, sha256_post}` because the
same paths appear in `pins_pre`/`pins_post`. O, two consumers make that a regression:

- `tools/carrier-run.py:351` `carrier_sha = receipt["carrier"].get("sha256_pre")` feeds
  `bind_session`; `:128-131` returns both flags false when `carrier_sha256` is falsy, so `bound` is
  empty and `:381` `len(bound) != 1 + len(list(searches))` returns **2 on every CLI run**.
- `tools/receipt-validate.py:280-283` requires a digest under `carrier` (`newest_sha` over
  `SHA_KEYS`); without it every receipt gains `missing_field`.

The duplication is *derived* (`:302`, `:348` copy the value from the pins snapshot) and checked
against live bytes by the validator, so it is not a second authority. Verdict: reject T4; keep.
By contrast T3 (`pins.snapshot.monotonic_ns`, `tools/pins.py:70`) is genuinely unread —
`grep -rn monotonic_ns tools/` → writer only — so T3 stands (one-line drop, no consumer).

## F4 — LOW — per-step `retained_logs` is a duplicate of the receipt-level copy, and is cumulative, not per-step

O. `tools/carrier-run.py:443` sets `rec["retained_logs"] = poller.retained()` inside `_run_polled`
(also `:399`, `:409` for the two early-error paths). The `LogPoller` is shared across all polled
steps (`:323`), and `retained()` returns *every* tracked session so far; the receipt-level copy is
`:350/:354`. On `runs/calib-shfmt/receipt.json`: `steps.analyze.retained_logs` and the top-level list
have length 1, the same `session_dir`, the same `polls` (59) and the same file digests — the step copy
is the top copy minus the `binding` key.

O. No consumer needs the step copy: `CARRIER_STEP_REQUIRED` (`receipt-validate.py:62-65`) omits it;
the contract's step record (`contract.md:43-44`) omits it; `retained_logs` is specified at receipt
level (`contract.md:45-47`). I. If `--search` is ever used, `steps["search:k"].retained_logs` would
attribute the analyze session to the search step — a false attribution in the exact field wave-1
wanted for step attribution.

Smallest fix: delete the three `retained_logs` assignments in `_run_polled` (`:399`, `:409`, `:443`);
keep `receipt["retained_logs"]`. Zero behavior change: the step copies are a strict subset of the
top-level list, and no reader uses them.

## F5 — LOW — dead code, zero behavior change

- **O** `tools/carrier-run.py:93-94` `_popen` and `:268` `runner = runner or _popen` are unreachable.
  Whenever the parameter is `None`, `:260-267` replaces it with `_private_runner(child_env)`, so at
  `:268` `runner` is always callable. Callers: `main()` `:617-620` passes none; the selftest passes
  `fake_runner` (`:543-547`). Delete `_popen` and line 268.
- **O** `tools/carrier-run.py:19` `import fnmatch` — sole occurrence of `fnmatch` in the file.
- **O** `tools/retain.py:32` `import time` — sole occurrence outside a child code string (`:244`).
- **O** `tools/carrier-census.py:213` `canned_stdout` is assigned and never read; `fake_inspect`
  (`:224-235`) returns a hardcoded dict, so `run_inspect`'s JSON parse (`:133-146`) is never exercised.
  Which exposes the second issue: the one function that consumes REA output has no test. Either feed
  `canned_stdout` through `run_inspect`'s parser or delete the variable (deleting only hides the gap).
- **O** `run-carriers.sh:12` reads a third TSV column into `kind` that is never used;
  `predictions/carriers.tsv` column 3 is prose ("calibration (pilot-seen)" / "prospective"). Use `_`.

Verified with an AST scan over `tools/*.py` (only `fnmatch` and `time` flagged as unused imports) and
`grep -c` for each symbol.

## F6 — LOW — `carrier-census.py` has no surviving consumer; drop candidate (with one wrong constant if kept)

Consumers checked (O):

| Consumer | State |
|---|---|
| `measure.py:41` `"carrier-census.py"` | presence check only; one-line edit if dropped |
| `contract.md:110-113` | spec; would need a one-line retirement note |
| `w1/CarrierCensusTool.md:7,20`, `w1/carrier-census.json` | historical evidence; readable without the tool |
| knowledge entry | `git show HEAD:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md \| grep -c carrier-census` → **0** |
| SKILL registry | rows at `SKILL.md:532-540` (9 rows) contain no census row |
| retained receipts | none reference it (`grep -rn carrier-census runs/` → nothing) |

Its columns are not unique work: sha256/size are one `sha256sum`; ELF class/machine is `file`; owner is
`pacman -Qo PATH`; `go_version`/`evidence_id` duplicate `inspect-go-binary`, which `carrier-run.py:312-314`
already runs for every *chosen* carrier. The `evidence_id` column is read by no artifact. So wave-1's
T2 conditional ("if the pool table is cited, fold into buildinfo-probe") does not resolve to a fold:
folding would delete the REA evidence id and keep a second parser of the same blob for nothing.
Recommendation: **DROP** the tool plus `measure.py:41`, and append one contract line that the census
section is retired (the w1 JSON/report stay as historical evidence). If L1 instead keeps it as
one-shot pool evidence, fix `tools/carrier-census.py:74` (`0x28: "aarch64"`): ELF `EM_ARM` is 40 =
0x28 and AArch64 is 183 = 0xB7 (`/usr/include/elf.h:197,317`), so a 32-bit ARM carrier is mislabeled
as `aarch64` — the same string also appears twice in the map (`:74`, `:76`).

## F7 — LOW — `run-carriers.sh` success status is not a summary

O, control flow: `set -u` only (`:4`); the loop body's last command is `echo` (`:30`) and the last
command of the script is `done < predictions/carriers.tsv` (`:31`). Bash returns the last body
command's status, so the script exits 0 even when `carrier-run.exit` is 1/2 or `compare.exit` is 1.
Nothing is hidden in the artifacts (each run writes `carrier-run.exit` / `compare.exit`, and the
knowledge recheck reads files), so this is convenience-only. Smallest fix: `bad=1` on
`[ "$rc" -ne 0 ] || [ "$(cat "$out/compare.exit" 2>/dev/null)" != 0 ]`, `exit "$bad"` after `done`.
Do **not** add `set -e`; 1/2 are intentional codes (`SKILL.md:532`).

## F8 — calibration note (no action) — the mid-run pin set is 146 paths / 92 MB

O. `run-carriers.sh:8-10` expands 143 installed Go data files into `--pin`:
`find …/data/typeinfo/golang -type f | wc -l` → 143; `du -sh` → 92M. With carrier +
`round-16/selection.py` + the frozen prediction, every receipt pins 146 entries
(`jq '.pins_pre.entries|length' runs/*/receipt.json` → 146 ×8). `carrier-run.py:427` re-snapshots all
146 every 30 s; the eight analyze windows are 30–250 s (from `steps.analyze.started/ended_at_utc`),
so ≈0–8 mid-run snapshots per run, **23** across the sweep, ≈2.2 GB of extra hashing in total (≈1.5 s
at sha256 rates, more on a cold page cache). Measurable, not a deletion driver; recorded so a later
seat does not re-litigate it. If F2 is wired, the mid-run set can be narrowed to
`[carrier, prediction]` (the only inputs whose mutation changes evidence) without losing the signal.

## `--search` — wave-1 T1 confirmed; deletion inventory completed

O. Consumers: none.
- All 8 receipts: `jq -r '[.steps|keys[]]|join(",")' runs/*/receipt.json` → `analyze,inspect-go-binary`.
- `run-carriers.sh:19-21` passes `--carrier/--label/--out-dir/--timeout/--poll/--pin` only.
- Text: `git grep -n -- "--search" HEAD` → `tools/carrier-run.py`, `contract.md:33,40-41`, and wave-1
  reports only; no SKILL row, no knowledge entry, no draft registry row.

Deletion inventory (wave-1 named only the contract lines): `carrier-run.py:606-607` (CLI arg), `:620`
(pass-through), `:256` (`searches=()`), `:336-341` (loop), `:381` (`1 + len(list(searches))` → `1`),
`:545`, `:557-558`, `:563` (selftest), `:534-537` (fake runner branch), `:65-66` `sanitize` (sole caller
`:337`), docstring `:4`, `:15`; `contract.md:33`, `:40-41`. No retained receipt depends on a search
step, so the drop is clean. Tradeoff: the only multi-session attribution path disappears — but that
path is also where F4's cumulative misattribution lives, so nothing usable is lost until it is
re-specced.

## retain.py — usage checked; keep (C1(b) instrument), fix the silent selftest dispatch

O. Usage: zero receipts.
`find .ufo/waves/round-17 -name '*.json'` outside `runs/`, `w1/`, `pilot/` with `argv` **and**
`pins_compare` → none. `git grep -n "retain.py" HEAD` outside `w1/` → `contract.md:22-23`,
`measure.py:32,272`, `receipt-validate.py` docstrings/loader comments, and `retain.py` itself. No SKILL
row at HEAD (`SKILL.md:532-540` covers the other nine tools). That is consistent with the plan: the
citation-drift re-exercise that needs it is still open (`w1/draft-lesson-gate.md:70`, S4) and
`claims.json` C1(b) names the receipt as the instrument. Deleting it would remove C1(b)'s only
non-REA argv+pin receipt producer; **keep**.

O. Latent bug: `tools/retain.py:168` tests `if "--selftest" in raw` **before** splitting on `--`
(`:169-174`). A retained child argv that itself carries `--selftest` therefore switches retain into
its own selftest. Proof (import only, no child run):
`parse_args(["--out","/tmp/x","--","/bin/true","--selftest"])[0]` → `selftest`;
`parse_args(["--out","/tmp/x","--","/bin/true"])[0]` → `run`.
Failure mode is silent: the child never runs, no receipt is written at `--out`, exit 0. Severity
MEDIUM-latent: no current consumer triggers it, but the natural use of a retention tool is to retain
another tool's `--selftest` argv, which is exactly the broken shape. Smallest fix:
`if raw[:1] == ["--selftest"]:`.

## Duplicate pins logic — conclusion (the asked overlap)

O. There is **no second production authority**. `def snapshot` / `def compare` exist only in
`tools/pins.py:62` / `:75`; `retain.py:51-58`, `carrier-run.py:58-62`, `receipt-validate.py:84-92`
import that file by absolute path; `run-carriers.sh` hashes nothing itself. What remains is:

1. **F4** per-step log record (delete, above).
2. **F2** a third snapshot (mid-run) whose output no consumer reads (wire or delete, above).
3. **O** Three `sha256_file` copies (`retain.py:43`, `carrier-run.py:50`, `receipt-validate.py:76`) plus
   inline hashes in `carrier-census.py:85`, `buildinfo-probe.py:313`, `log-extract.py:233`. No action:
   a shared hasher would couple tools whose value is that each fails independently; the contract makes
   `pins.py` the authority for *snapshots*, not for a one-line digest helper.
4. **O** `carrier-run.py:468-490` embeds a **fake** `pins.py` in the selftest whose semantics differ
   from the real module: it keys raw paths (real `snapshot` realpaths, `pins.py:66`), treats any entry
   change including `mtime_ns` as `changed` (real `compare` ignores mtime, `pins.py:96-97`), and has no
   `errors` list (real `compare` returns one, `:103`). The selftest therefore never exercises the
   production module and can green a real incompatibility. Fix (test fidelity, not a deletion): drop
   the `textwrap` block (`:468-490`) and pass `pins_path=PINS_PATH`; the temp carrier is a real file,
   so the real snapshot/compare works unchanged.

## Deletion list, ranked, with consumers checked

| ID | Candidate | Consumers checked | Verdict |
|---|---|---|---|
| D1 | `carrier-run.py --search` path (+ `sanitize`, gate, selftest branch, docstring) | 8 receipts, run-carriers.sh, SKILL, knowledge, drafts → none | drop |
| D2 | `carrier-census.py` + `measure.py:41` (+ contract retirement note) | measure, contract, w1 report/JSON (historical), knowledge → no C1/C2 consumer, 0 knowledge citations | drop |
| D3 | `_popen` + `runner = runner or _popen`; `fnmatch`; `time`; `canned_stdout`; TSV `kind` | grep + AST scan; no caller/reader | drop |
| D4 | per-step `retained_logs` (`:399,:409,:443`) | validator, contract, 8 receipts → duplicate only | drop |
| D5 | fake `pins.py` in carrier-run selftest | only the selftest | replace with real import |
| — | `retain.py` | C1(b) instrument, unexercised | **keep** |
| — | `carrier.sha256_pre/post` | bind_session + validator | **keep** (rejects T4) |
| — | `pins.py`, pre/post pin maps | single authority / C1 metric | **keep** |

## Preserved contract (what these moves must not weaken)

- `pins.py` pre/post maps and its red case (`pins.py:233-247`, mutate → exit 1) — untouched.
- `carrier-run` exit semantics 0/1/2 and the one-bound-session-per-polled-step gate (`:376-383`) —
  untouched; F3 exists to protect the gate.
- `log-extract → predict → compare` chain and `receipt-validate` digest walk — untouched.
- Receipt shape: F1 repairs the validator to the producer. The producer's mapping is the richer record
  and the one embedded in all 8 committed receipts.

## Searched / not searched

Read at HEAD `da64646`: all 11 `tools/*.py`, `run-carriers.sh`, `measure.py`, `SKILL.md:532-540`,
`contract.md`, `claims.json`, the r17 knowledge entry, all 8 `runs/*/receipt.json`, `w1/SimplifyTools.md`,
`w1/CarrierRunTool.md`, `w1/ConnCapabilityHistory.md`, `w1/draft-lesson-gate.md`, `w1/CarrierCensusTool.md`,
`w1/carrier-census.json`. Ran: `receipt-validate.py` over the 8 receipts (exit 1), two patched copies in
`/tmp` (proving the two-edit fix and that edit 1 alone fails), `git show`/`grep`/`jq`/`find`/`du`/`stat`,
and one import-only call to `retain.parse_args`. Did **not** run: `carrier-run`/`retain` selftests (other
seats' tools), any REA `analyze`/`search`/`decompile`, Ghidra, or any carrier. Tool installs/upgrades:
none.

## Stop point

After D1–D4, the next deletion that would harm an axis is any of the pin maps, `pins.py` itself, the
`carrier.sha256_pre/post` pair (F3), or `retain.py` — each is the only instrument for a named C1/C2
falsifier. F1 is not a deletion; it is the prerequisite for any receipt-based claim in this round.
