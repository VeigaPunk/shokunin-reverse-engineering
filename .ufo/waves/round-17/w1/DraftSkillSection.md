# Round 17 w1 — DraftSkillSection report (author-side advisory)

Draft: `.ufo/waves/round-17/w1/draft-skill-section.md` (not applied to SKILL.md). Edits for L1: replace SKILL.md:448 with the corrected citation-drift row; append the section after SKILL.md:507 (EOF).

## Behavior

- Drafted the citation-drift replacement row (SKILL.md:448 is the old text).
- Drafted the "Retained Go carrier diagnostics — round 17" section: source-law table, pilot-vs-source table, and seven registry rows (carrier-run, log-extract, predict, compare, pins, retain, receipt-validate). All seven are labelled unexercised; `round-17/tools/` does not exist yet (observed).
- Wrote only the draft and this report. No other file touched; no commit; no REA `analyze`/`search`/`decompile`; no Ghidra run; no carrier executed.

## Citation-drift argv finding (calibration)

- Current row (SKILL.md:448) advertises `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . ...` with no `-I` and a relative path. No retained receipt uses that form.
- The exercised isolated form is `python3 -I <abs script> --root <abs root> --rev <rev> --table <abs> --expected <abs> --strict`, run from the repo root: `.ufo/waves/round-16/verification.json` `commands[17]` (label `citation-strict`, exit 0, rev `27b8fc13…`). Observation.
- Round 15 used the same `--strict` argv without `-I` (`.ufo/waves/round-15/verification.json` `commands[9]`, exit 1, rev `7ad23fe1…`). Observation: strict exit 1 is a real outcome, so the row must not imply exit 0 only.
- Grep over every `.ufo/waves/**/*.json` `argv` containing `citation`: four entries, all with `--strict`. No default-probe (no `--strict`) argv and no `--selftest` argv exists in retained JSON receipts. Observation.
- Drafter read-only run at HEAD `b563c799…` with the corrected isolated argv: exit 0, `CITATION_DRIFT_VERDICT: clean findings=0`. Observation. This is not a retained receipt and does not discharge C1(b); outputs were written to `/tmp` and deleted.
- Pinned-table sha256 `7994eec7…` matches `expected.json` `pointer_table.sha256`. Observation.
- `expected.json` frozen run is at rev `679af5d…` with verdict `failed` (`citation_dead`). A run at HEAD is a different measurement per the file's own note. Observation.
- Probe `--help` line: "default probe semantics (0 reported / 2 could-not-evaluate)". The `--strict` and default semantics are different gate maps; the row keeps them separate.

## Source law (installed Ghidra 12.1.4, Base-src.zip) — observations

- `GoBuildInfo.java:488-489`: strips leading `go`. `GoBuildInfo.java:238`: `getGoVer()` = `GoVer.parse(version)`.
- `GoVer.java:62-81`: truncates at first char outside `[.0-9]` (line 65), requires ≥2 parts (66-67), defaults missing patch to 0 via `parse(s,0)` (46-47).
- `GoRttiMapper.java:79` `SUPPORTED_VERSIONS = 1.15-1.25`; `:166-169` invalid version throws; `:170-172` untested logs ERROR and continues; `:174-177` snapshot lookup; `:180` "Using Go API snapshot for version".
- `GoRttiMapper.java:356-361`: bootstrap exception only when `apiSnapshot.isInvalid()` AND struct-registration throws `IOException`.
- `GoApiSnapshot.java:102-116`: `get` returns `EMPTY` (`:115`) when no base file; `:242` defines EMPTY.
- `GoApiSnapshot.java:148-166`: patch-diff fallback; WARN "Falling back" at `:159-161`; "Using" at `:163` only in the no-fallback branch.
- `GoApiSnapshot.java:205`: `read(is, archNames, GoVer ver)` — how `ver` is stored not checked (inference below).

## Pilot observations (not pinned, not final)

- shfmt `go1.27.0-X:nodwarf5`: `shfmt-log/ghidra.log:83` ERROR Untested `[1.27.0]`; `:84` WARN Missing Go bootstrap; no "Using" line; `:85`, `:89` Golang analyzer ERRORs cascade. `shfmt.json` `normalized_result` has no Go status field.
- esbuild `go1.23.12`: `esbuild-0.25.12-log/ghidra.log:63-64` "Using … 1.23.12"; `:67` "Go version 1.23.12"; no Untested, no Missing.
- Pilot pins were not recorded (README.txt); log copies are 1 s polling (`log_capture_limit` applies).

## Selection checks (r16 `selection.py`, source model, run read-only by this seat)

- `1.27.0` and `1.27.2`: `missing_base`. `1.26.0`: `missing_base`. `1.25.7`: `base_only`, base `go1.25.0.json`, selected patch 0. `1.23.12`: `exact_diff`, base `go1.23.0.json`, diff `go1.23.12.json.diff`, patch 12. `1.20.12`: `exact_diff`, base `go1.20.0.json`, patch 12.
- Base files present: `go1.15.0.json`…`go1.25.0.json` only (highest base is 1.25.0; `1.26` absent). Observation of the data directory listing.

## Findings / routed issues for L1

1. **`log-extract` misses the fallback signal.** The contract records `GoApiSnapshot` only as a go_line. The "Falling back" WARN (`GoApiSnapshot.java:159-161`) is the one log-visible sign that a patch diff was skipped. Recommend a `fallback_warnings` field. Proposal, not in contract.
2. **Predict's `missing_bootstrap` rule is stronger than source.** Contract says "iff status `missing_base`". Source shows the exception needs `EMPTY` AND an `IOException` in struct registration (`GoRttiMapper.java:356-361`). Recommend predict emit the rule as "necessary-condition expectation" and label the chain `[INFERENCE]`.
3. **`GoVer.parse` vs r16 parser.** `GoVer.parse("1.27")` gives patch 0; r16 `parse_request` rejects two-part and decorated forms (`selection.py` docstring). Predict must define the two-part case explicitly (exit 2 recommended), not silently normalize.
4. **Evidence JSON is not a diagnostic channel.** `shfmt.json` carries no Go status; the Go outcome lives only in the log. Retention quality is the whole signal; `log_capture_limit` must be surfaced in `compare` output, not just the receipt.
5. **Post-hoc pilot table.** The pilot-vs-source table was derived after reading the pilot logs. It shows consistency, not prediction. The section says so; L1 should not cite it as a blind prediction result.
6. **Row label discipline.** All seven new rows say "unexercised" so `invocation-audit.py` classes them `labelled_unexercised`, not `unlabelled_variant`. L1 must replace the label with the exercised argv once a receipt exists.

## Inferences (labelled)

- `[INFERENCE]` EMPTY → bootstrap exception chain (requires an IOException not observed in any retained stack).
- `[INFERENCE]` Whether `GoRttiMapper.java:180` prints the requested label in the fallback path (depends on `GoApiSnapshot.read`, `:205`, not opened).
- `[INFERENCE]` The shfmt cascade (`:85`, `:89`) is caused by the missing GoRttiMapper (log text: "unable to get GoRttiMapper"), not independently verified.

## Limits

- No carrier executed, no REA analysis, no Ghidra run by this seat.
- Pilot evidence is unpinned, unreceipted, and not final.
- The Go data directory is not pinned by this draft or by the contract's carrier-run step (contract line 34).
- The corrected citation row is drafted from receipts; the drafter's single isolated run at HEAD is an observation only.
- Not drafted (outside my assignment): the SCORECARD capability row, the QUALITY #19 row, the knowledge entry, and the SOURCES rows.

## Installs / updates

None. No package installed or updated; `npx`/`pacman` not used. Read-only tools only.

## Cleanup

Removed `/tmp/kr17-w1-cd.out` and `/tmp/kr17-w1-cd.err` (drafter's probe run output). No other temp files created.

Artifact paths: `.ufo/waves/round-17/w1/draft-skill-section.md`, `.ufo/waves/round-17/w1/DraftSkillSection.md`.
