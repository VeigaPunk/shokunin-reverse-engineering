# ReviewContract — R17 contract vs claims (advisory)

Seat: `KaidokuR17.ReviewContract-3`. Read-only; this file is the only write.
Labels: **OBS** = observed from a file/command; **INF** = reading/source inference.
Anchors: `contract.md`/`claims.json` are under `.ufo/waves/round-17/`; baseline
`b563c799d97774aae4351276fe43cb897311e349`; source reads are from installed
`Ghidra/Features/Base/lib/Base-src.zip` (12.1.4).

Method: read contract + claims; `git show` baseline artifacts; extracted the Go
source members; re-read pilot logs/JSON; allowed REA calls only —
`rea-agents@6.5.0 inspect-go-binary --help`, `inspect-go-binary /usr/bin/shfmt
--format json`, `search --help`. No analyzer ran; no carrier executed; no tool
installed or upgraded (npx reused the pilot cache).

## Verdict

The contract defines usable *instruments*, but several of the claims' falsifiers
are not mechanically bound to them, and two source-law statements the contract
tells executors to encode are wrong or absent for 12.1.4. Five findings are of the
"passes the contract, does not support the claim" class (F5–F8, F10).

| Claim | Contract support | Weakest point | Amendments |
|---|---|---|---|
| C1(a) temporal | `temporal-sweep.py:90-96` | site set misses a live statement; sites read at REV let a correction text self-satisfy; correction matches by path only | F5, F6 |
| C1(b) invocation | `invocation-audit.py:80-88` | `unexercised` is a free-text pass; row↔argv normalization undefined; citation-drift re-exercise not in the metric | F7–F9 |
| C1(c) QUALITY #19 | `measure.py:116-119` | presence-only; no grounding check | F12 |
| C2 retained log | `carrier-run.py:31-49`, `log-extract.py:51-60` | prediction not pre-registered; no receipt↔prediction↔log binding; empty/partial capture still exits 0 | F1–F4, F10, F11 |
| C2 prediction law | `predict.py:62-73` | `fromVersionString` does not exist; `GoVer.parse` on the raw REA string is INVALID; `missing_bootstrap ⇔ missing_base` is not the source law | F2 |
| both | `measure.py:115-119` | no `before/after` predicates or thresholds, so `N→0`, `M→0`, `0→≥3` are not computed | F6 |

## Findings (severity order)

### F1 — C2 predictions are not pre-registered (high; calibration)
**Anchor:** `contract.md:32-48` runs inspect→analyze; `predict.py:62-73` is a
separate tool. Nothing fixes the prediction before the observation exists.
**OBS:** pilot `README.txt` records only the analyze argv; there is no
`inspect-go.json` and no prediction in `pilot/`.
**Defect:** an executor may run `predict.py` after reading `ghidra.log` and pick
`--goos/--goarch` (the flag defaults) or a normalization that makes the fields
match. "Prediction mismatches are reported, never hidden" is then unfalsifiable.
**Amendment:** make the order inspect → predict → analyze normative and bind it:
- `carrier-run.py ... --prediction P.json` (required for C2 runs). Pin `P` in
  `pins_pre`, record `prediction_sha256` and `prediction_created_utc`, and exit 2
  if `prediction_created_utc > analyze.started_at_utc` or if `P.input` differs
  from `inspect-go.json` `normalized_result.build_info.go_version`.
- `compare.py --prediction P.json --observation O.json --receipt R.json` records
  `prediction_sha256` and refuses (exit 2) unless `R.prediction_sha256` equals it.

### F2 — `predict.py`'s source law is mis-cited and partly wrong (high; depth)
**Anchor:** `contract.md:65-66` ("Normalize exactly as Ghidra's `GoVer.parse`/
`fromVersionString`"), `contract.md:71` (`missing_bootstrap` iff `missing_base`).
**OBS:** `fromVersionString` occurs 0 times in every `.java` member of
`Base-src.zip`. The actual chain is `GoBuildInfo.getGoVer()` →
`GoVer.parse(version)` (`GoBuildInfo.java:237-239`), after the version string is
read and the `go` prefix is stripped (`GoBuildInfo.java:488-489`); `GoVer.parse`
truncates at the first non-`[.0-9]` char (`GoVer.java:46,62-79`).
**OBS (simulated from those two rules):** `go1.27.0-X:nodwarf5`→`1.27.0`,
`go1.23.12`→`1.23.12`, `go1.21rc2`→`1.21.0`, `1.22.8 X:rangefunc`→`1.22.8`,
`devel go1.24-abcdef`→INVALID. `GoVer.parse` applied to the raw REA string
returns INVALID (`g` is the first char), so the contract as written licenses
either exit 2 on every carrier or an ad-hoc strip, not one law.
**OBS:** missing bootstrap is not a pure function of EMPTY: `GoRttiMapper.java:353-365`
throws `BootstrapInfoException("Missing Go bootstrap type info…")` only when
`apiSnapshot.isInvalid()` **and** `registerStructures` throws `IOException`; a
valid snapshot that fails mapping throws a different `IOException`
(`GoRttiMapper.java:363-365`). `GoApiSnapshot.get` returns `EMPTY` at
`GoApiSnapshot.java:102-116,242`.
**Amendment:** replace `contract.md:65-66,71` with the explicit algorithm and
anchors above; mark `missing_bootstrap` as `basis_kind: "conditional_inference"`
with anchors `GoRttiMapper.java:353-365` + `GoApiSnapshot.java:102-116,242`, and
require the executor to record whether the log showed the alternative failure
strings (F11). Delete the phrase `fromVersionString`.

### F3 — No receipt↔observation↔comparison binding (high; claim text)
**Anchor:** `contract.md:43-47` receipt has no prediction/compare fields;
`compare.py:75-78` takes two arbitrary JSON files.
**OBS:** nothing in the contract requires `W/runs/*/compare.json`, and
`measure.py:118` counts `receipt.json` files only.
**Defect:** a receipt can carry carrier A's pins/evidence while the comparison is
run on the pilot log or a hand-edited `log-extract` output; C2's "with … a
prediction comparison" is satisfied on paper.
**Amendment:** `compare.py` requires `--receipt`; `match` is permitted only when
`O.log_sha256` equals one `retained_logs[*].files["ghidra.log"].sha256` in the
receipt, `P.input` equals the receipt's inspect `go_version`, and
`P.carrier_sha256` equals the receipt's carrier sha. Record the resulting
`compare.json` path in the receipt (or require `W/runs/<label>/compare.json` and
`prediction.json` beside it). `measure.py` counts only receipts that satisfy all
three bindings and `receipt-validate.py` exit 0.

### F4 — Log capture can be empty/partial and still "succeed" (high; depth)
**Anchor:** `contract.md:36-40` hardcodes `/tmp/rea-ghidra-*`; `contract.md:48`
exits 0 when all steps ran.
**OBS:** pilot `ghidra.log` lines carry the analyzed target as
`target-58f765638eed.bin` / `target-bab29b2ca7a9.bin` — the first 12 hex of the
carrier's sha256 (shfmt `58f765638eed…`, esbuild `bab29b2ca7a9…`).
**Defect:** if `TMPDIR` is set, or REA deletes the root before the first poll, or
`ghidra.log` never appears, `retained_logs` is `[]`/short and exit is 0. Also, the
log can belong to a different file than the carrier the receipt pins. Finally,
`log-extract`'s absence-based comparisons cannot distinguish "line absent" from
"line after the final copy"; the contract only records prose in
`log_capture_limit`.
**Amendment:** (i) honor/record `TMPDIR` (or take `--tmpdir`), scan the effective
temp dir, and exit 2 when any analyze step ran and no `ghidra.log` was retained;
(ii) record per-file `[{poll, utc, bytes}]`, `first_seen_utc`, `last_copy_utc`,
`tail_gap_s = analyze.ended_at_utc - last_copy_utc`, `partial` (true when bytes
grew on the last two polls or `tail_gap_s > 2*poll`); (iii) `log-extract` emits
`target_sha12` (regex `target-([0-9a-f]{12})\.bin`), and `carrier-run` exits 2
unless it equals `carrier_sha256[:12]`; (iv) `compare.py` classifies a
predicted-but-absent field as `unknown` (not mismatch) when `partial` is true, and
reports `unknowns` separately.

### F5 — C1(a) site set omits a live statement and is evaluated on the wrong side (high)
**Anchor:** `contract.md:91-96`.
**OBS:** at baseline, the regex matches exactly three lane statements:
- `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` — *"Producer and
  fixture pins were unchanged during the run."* — **not in the contract's file
  list**;
- `corpus/lessons/round-16.md:154` — in the list;
- `.ufo/waves/round-16/verification.json:419` — `pins_unchanged_during_run: true`.
`LOG.md`, `SCORECARD.md`, `SKILL.md` have no matching line at baseline.
`corpus/lessons/round-16-verifier-spotcheck.md:183` also matches, but it is the
*defect description* and `controls.py` requires that file byte-identical.
**Defect:** `unqualified: 0` is reachable while the knowledge statement stands.
Sites read at REV also include correction prose that quotes the phrase; a
correction line containing `R16-PROVENANCE` + the path can then be counted as a
site, and self- or path-only matching makes `corrected` true without a named
correction.
**Amendment:** evaluate sites at a `BASELINE` argument, corrections at `REV`;
add the knowledge file explicitly and exclude `*-verifier-spotcheck.md` plus any
line containing `R16-PROVENANCE`; emit
`correction: {file, line, text}` and count `corrected` only when the correction
names `site_path:site_line` and the line is after the site (same-file append) or
in LOG/SCORECARD/`corpus/lessons/round-17.md`/`--extra`; accept same-file
appends for lesson/knowledge sites; require the correction text to contain
`not evidenced` (or a `R16-PROVENANCE:corrected` marker); report
`non_vacuous` (true only when `sites > 0` at BASELINE). This matters because
`verification.json` itself may not be rewritten (`contract.md:122-123` requires
pre-existing `.ufo/waves/**` blobs byte-identical).

### F6 — `measure.py` has no before/after predicates or thresholds (high)
**Anchor:** `contract.md:115-119` lists *presence* checks only.
**OBS:** `measure.py REV` cannot express `N→0`, `M→0`, `0→≥3`, "row 19 presence
0→1", or "capability row enters only if the receipt validates".
**Amendment:** `measure.py [--baseline REV] REV` emitting
`predicates: [{id, before, after, target, met}]` for at least:
C1a (`sites_baseline>0`, `unqualified_after==0`, every site has a correction),
C1b (`unlabelled_variant_after==0`, citation-drift row `exercised_match` with a
round-17 receipt), C1c (row 19 present **and** grounded, F12), pins red-case,
C2 (F3/F4). Fail (exit 1) when a target is missed; `--baseline` defaults to
`claims.json`'s `baseline`.

### F7 — `invocation-audit`'s `unexercised` is a free-text pass (high; C1(b))
**Anchor:** `contract.md:87` — `labelled_unexercised` iff the row text contains
`unexercised`; `contract.md:88` counts only `unlabelled_variant`.
**OBS:** at baseline, 7 rows match `(probe|gate|tool) / kaidoku` and none contain
`unexercised` (`SKILL.md:447-450,487,506-507`). C1(b)'s falsifier is `M→0`.
**Defect:** appending the word `unexercised` to all 7 rows satisfies the metric
with zero executions and zero receipts, while the claim also requires
"the citation-drift row is re-exercised with its isolated absolute argv and the
receipt retained" — not measured at all.
**Amendment:** (i) `labelled_unexercised` requires the label to name the
alternative that *was* exercised (path under `.ufo/waves/round-17/`) or state
`no receipt`; count a label without either as `unlabelled_variant`;
(ii) add `counts.rows_with_zero_receipts`; (iii) make the citation-drift
predicate explicit in `measure.py`: `name == "citation-drift"` ⇒
`class == exercised_match`, `matched_receipt` under `W/`, and receipt argv equal
to the row command after canonicalization. Do not accept a label for that row.

### F8 — Row↔argv normalization is undefined; the citation-drift case is already a mismatch (high; C1(b))
**Anchor:** `contract.md:86` — "equals some exercised argv modulo leading
`python3`/interpreter path"; `<...>` wildcards.
**OBS:** row 448's first backticked span is
`python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV>
--table .ufo/… --expected .ufo/…` (the second span in the same cell is
`--strict`). The r16 exercised argv
(`.ufo/waves/round-16/verification.json` `commands[17].argv`) is
`python3 -I /home/vgpnk/…/citation-drift-probe.py --root /home/vgpnk/… --rev <sha>
--table /home/vgpnk/… --expected /home/vgpnk/… --strict`.
So the advertised command differs in `-I`, relative vs absolute paths, and the
presence of `--strict`; `--strict` is a *different mode* (report vs gate,
probe `--strict` at `citation-drift-probe.py:482`). Under strict token equality
the row can never match; under a loose wildcard it matches anything.
**Defect:** "re-exercised with its isolated absolute argv" and `M→0` cannot both
be interpreted unambiguously.
**Amendment:** define canonicalization precisely: drop the interpreter token and
its flags up to and including the first token ending `.py`; resolve path-looking
tokens against LANE (so `.`→LANE, relative≡absolute); `<NAME>` matches exactly one
token; `[ … ]` expands to zero or one occurrence; **no extra tokens** beyond the
pattern; exclude args containing `--selftest` unless the row itself contains
`--selftest`. Then pick one outcome for row 448: either update the row text to
the exercised strict argv, or retain a new round-17 receipt that runs the
advertised probe-mode argv (no `--strict`) and label nothing. Also fix
`[--label <L>]` in the custody row, which otherwise tokenizes as literals.

### F9 — An "exercised" argv is any JSON array of strings (medium; audit trust)
**Anchor:** `contract.md:83-85`.
**Defect:** `W/runs/x/receipt.json` (or a hand-written `*receipt*.json`) with an
`argv` array but no execution record counts as exercised; a selftest argv can
also match.
**Amendment:** an argv counts only when the containing object also has `exit`
(int) and `ended_at_utc`, or the file validates (`receipt-validate.py` exit 0);
record `coverage: {receipt_files, argv_arrays, rows}` and exit 2 if
`receipt_files == 0` at REV (otherwise "0 mismatches" and "nothing scanned" are
indistinguishable).

### F10 — The compared fields do not test the base/diff selection the claim names (medium-high)
**Anchor:** `contract.md:54` (`snapshot_labels` from two messages),
`contract.md:76-78` (three fields).
**OBS:** source emits three distinguishable outcomes:
`Using Go API snapshot for <req>` when the exact patch diff exists
(`GoApiSnapshot.java:161-166`), `Falling back from <req> to <sel>` when it does
not (`:158-160`), and only the mapper's `… for version <req>` when patch 0
(`GoRttiMapper.java:174-181`; `read()` stores the *requested* `ver`,
`GoApiSnapshot.java:111,239`). A naive "for (.*)" regex also captures
`version 1.23.12` from the mapper line.
**Defect:** `selection.py` may predict `exact_diff` where the log says
`Falling back`, and the comparison still reports `match` because the requested
label appears either way; C2's "GoApiSnapshot base/diff selection via r16
selection.py" is untested.
**Amendment:** define exact patterns — `Using Go API snapshot for version
(\S+)$`, then `Using Go API snapshot for (\S+)$` (excluding `version`),
`Falling back from (\S+) to (\S+) for Go API snapshot`; emit
`snapshot_source ∈ {exact_diff, fallback_diff, base_only, missing}` and a fourth
compared field `snapshot_path` mapping prediction `selection.status` +
`patch_applied` to observed source; dedupe labels.

### F11 — `classification` conflates distinct failure modes (medium)
**Anchor:** `contract.md:58-59`.
**OBS:** the mapper can also emit `Invalid Go version string [%s]`
(`GoRttiMapper.java:166-169`) and `Invalid Go bootstrap struct mapping info: %s`
(`GoRttiMapper.java:363-365`), and the read path `Failed to read Go info`
(`GoRttiMapper.java:119-121`).
**Defect:** a valid-snapshot carrier whose mapping failed is classified
`snapshot_loaded`/`other` and compares `missing_bootstrap:false` → "match", even
though the run failed. The claim is about discriminating bootstrap failure.
**Amendment:** add `invalid_version`, `bootstrap_invalid_mapping`,
`snapshot_read_error` classes; `missing_bootstrap` extraction must use the exact
substring `Missing Go bootstrap type info`; `analyzer_errors` = level `ERROR`
with component in the same Go set as `go_lines` (the current "from Golang*"
text would drop `(GoRttiMapper) Untested Go version …`).

### F12 — C1(c)/capability/SOURCES/README predicates are presence-only (medium)
**Anchors:** `contract.md:117-120`; `claims.json:12-13,21-23`.
**OBS:** admission rows 1–18 exist (`corpus/QUALITY.md:11-28`); the SCORECARD
capability table has 4 rows (`SCORECARD.md:619-622`); SOURCES status vocabulary
is `mined|rejected`, S003 opened 2026-10-19, S023 2026-10-20, both `on-release`
(`corpus/SOURCES.md:9,29`).
**Defect:** "QUALITY row 19" can be an empty row; "capability row text" can be
added without a validating receipt; new SOURCES rows and reopened S003/S023 are
not identified; README token *counts* do not prove the new knowledge filename is
mapped.
**Amendment:** row 19 must cite `corpus/lessons/round-16-verifier-spotcheck.md`
and both `R16-PROVENANCE`/`R16-INVOCATION`; capability row must cite the
validating `W/runs/*/receipt.json` and have first-working-round 17; SOURCES
predicate requires ≥1 row with `opened = 2026-10-20` and S003/S023 `used-by`
carrying the round-17 knowledge token; README must contain the literal filename
`2026-10-20-r17-go-carrier-diagnostics.md`; all computed at BASELINE and REV.

### F13 — `pins.compare` missing-path semantics undefined (medium-low)
**Anchor:** `contract.md:15-16`.
**Defect:** `equal` is false for errors, but which paths go to `changed` vs
`missing` is unspecified; a post-absent/pre-absent path can be reported as
`changed` or omitted while `equal:false`. The selftest only covers mutation.
**Amendment:** define `missing` = path absent/errored in either snapshot;
`changed` = differing sha256/size; a path in both appears only in `missing`;
CLI prints the path names; selftest adds an absent-path case (exit 1, path in
`missing`).

### F14 — Global rules contradict the tools' own npx calls (medium-low, but make it explicit)
**Anchor:** `contract.md:7` ("Never write outside the paths a CLI is given. No
network.") vs `contract.md:35,40,112` (`npx -y rea-agents@…`), which resolves
from the registry and writes `~/.npm/_cacache`.
**Amendment:** scope the rule: "no network and no writes outside `--out-dir`
except the npx package cache; every REA step's exact argv and the resolved
`rea-agents` version are recorded". Optionally add `--offline`/prefer a pinned
local binary, and record `npm cache` reuse.

### F15 — Stated log line format is wrong for 5-letter levels (low, but breaks ERROR parsing)
**Anchor:** `contract.md:60` (`LEVEL  (Component)`, two spaces).
**OBS:** pilot `shfmt-log/ghidra.log:83,84` are `ERROR (…)` (one space) while
`INFO  (…)`/`WARN  (…)` have two; the level field is space-padded (`ERROR ` has one space, `INFO  `/`WARN  ` two).
**Amendment:** use `^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) ([A-Z]+)\s+\(([^)]+)\)
(.*?)\s*$`; state the padding rule.

### F16 — Smaller binding gaps
- `contract.md:45` "`evidence_id` … if present" → required; exit 2 if absent.
  **OBS:** pilot analyze JSON has top-level `evidence_id`
  (`pilot/shfmt.json`, `ev_2b29a1dd…`).
- `contract.md:48` exit precedence: define 2 > 1 > 0; and decide whether
  `analyze.exit != 0` disqualifies a run or is merely recorded (C2 wants retained
  runs; measure must then require `steps.analyze.exit == 0` explicitly).
- `contract.md:34` pins only carrier + `selection.py`; predictions also consume
  `Base-src.zip` (S003) and the selected `go<M.m.p>.json`/`.diff` files. Pin
  `Base-src.zip` (sha must equal S003's) and the `selection.base`/`selected_diff`
  files; keep "Go data dir" unpinned only if the selected files are pinned.
- `contract.md:106-108` "required fields" unenumerated; "every recorded file"
  ambiguous. Enumerate: pin entries, step stdout/stderr, `inspect-go.json`,
  retained logs, `prediction.json`, `compare.json`; verify `pins_compare` by
  recomputation and the F3 bindings.
- `contract.md:110-113` census exits 0 on failure; add per-path `error` and exit
  2 if any path is unreadable/inspect fails; add `buildinfo_probe_go_version` +
  `agree` (this is the only independent reader and is otherwise orphaned).
- `retain.py` (`contract.md:22-29`) has no consumer in the contract; either bind
  it to the citation-drift re-exercise (`W/runs/citation-drift/receipt.json` with
  `--pin` on probe/table/expected) or drop it so `measure.py` cannot pass on a
  presence-only artifact.
- `temporal-sweep`/`invocation-audit` exit 0 always; add mandatory `coverage`
  counters and exit 2 on a missing input file at REV.
- `--search` steps (`contract.md:40`) are not needed by C2 and can fail the run
  for unrelated reasons; record them without making them load-bearing.

## Verified, not findings
- `GoRttiMapper.java:79` is `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")`
  and `contains` is inclusive (`GoVerRange.java:83-87`). The contract anchor is
  right.
- `inspect-go-binary` output shape is as the contract assumes:
  `normalized_result.build_info.go_version` exists (OBS: live call on
  `/usr/bin/shfmt` → `go1.27.0-X:nodwarf5`, top-level `evidence_id`).
- `search` flags `--pattern/--kind/--format` exist (`search --help`); the
  carrier-run argv shape is valid.
- Pilot analyze exits are `0` for both carriers, including out-of-range 1.27.0
  (`pilot/*.exit`); "exit 2 if analyze exit != 0" does not by itself block C2.
- Baseline registry: 7 rows, none labelled; QUALITY rows 1–18;
  4 capability rows; SOURCES statuses `mined|rejected`; S003/S023 exist.
- `GoApiSnapshot.read` stores the requested version
  (`GoApiSnapshot.java:111,239`), so "predicted label = normalized request" is
  correct for the mapper line.

## Residual risk / verification gaps
- I did not run `rea analyze`/`search` or Ghidra (lane rule); runtime-root
  lifecycle and final-poll loss remain inference from the pilot README. The
  `target-<sha12>.bin` binding (F4) is OBS in the two pilot logs only.
- The pilot contains no `inspect-go.json` and no pre/post pins, so F1/F3 cannot be
  demonstrated from pilot evidence; they are contract-level defects.
- `fromVersionString` absence is exhaustive over `Base-src.zip` `.java` members
  (grep count 0); if the executor intends a different Ghidra class, it must name
  it and cite lines.
- No outside review, promotion or SHONEN claim is made here; this seat is
  author-side and only recommends amendments.
