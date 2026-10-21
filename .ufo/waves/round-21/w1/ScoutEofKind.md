# Scout: EOF nullable index and original extractor contract

**Axes:** C1 calibration (tied-lowest finite proxy) and C2 depth. **Confidence:** high for the statically read source contract; no LSP semantic resolution or extractor execution.

## Scope

Read only the round-20 contract, original extractor/comparator and their carrier-run callsite; the round-21 frozen fixture contract and comparator; and the named round-21 claims and round-20 spotcheck lesson. Searched retained R20 prediction/extractor/comparator JSON for the literal EOF-kind member. No external URLs were opened and no source-registry rows were written.

## Observed source facts

- R20 specifies a failure record with `kind`, `index: int|null`, `va: int|null`, and `phase`; the extractor is `W20/tools/first-failure-extract.py LOG` and the comparator returns 0/1/2 for match/mismatch/unevaluable (`.ufo/waves/round-20/contract.md:76-80`).
- The original extractor recognizes only Go components (`GoRttiMapper`, `GoTypeManager`, or `Golang` plus an alphanumeric suffix; `.../tools/first-failure-extract.py:36-39`). It takes the first qualifying Go-analysis summary or direct I/O error in log order (`:156-175`), then classifies its record plus continuation context (`:60-68`, `:84-131`). Classification precedence is material:
  - `Invalid index: N` → `kind=invalid_index`, integer `index=N` (`:91-112`).
  - `Unable to read past EOF: N, M` → `kind=eof`, integer `index=N` (`:96-117`).
  - `EOFException` without either recognized numeric form → `kind=eof`, `index=null` (`:100-122`). Exact source quote: `{"failure": {"kind": "eof", "index": None, "va": None, "phase": phase},` (`:118-122`).
  - Other `IOException` → `kind=io_exception`, null index; fallback → `kind=other`, null index (`:123-131`).
- For a non-null failure the extractor always constructs all four shape fields (`kind`, `index`, `va`, `phase`); `va` is null in every extractor classification branch. The returned JSON envelope has `log_path`, `first_failure` (object or null), `first_failure_line`, `cause_line`, `last_line`, and `other_errors` (`:170-195`). The first-failure line is the qualifying Go record; cause line is the recognized detail/exception line. No qualifying record means `first_failure=null`, bounded by `last_line` (docstring `:4-11`; line-bound calculation `:142-149`). Other ERROR records are retained separately (`:177-187`). The CLI prints that JSON and exits 0 on parse success; an unreadable log produces exit 2 (`:296-312`).
- R20’s comparator invokes the supplied extractor, requires exit 0 and JSON, unwraps the envelope when both `first_failure` and `last_line` exist, and compares null/null or exact `kind`+`index` only; it ignores `va` and `phase` (`.../tools/compare-first-failure.py:50-78`, `:28-35`). Its validator uses `.get()` for `index`/`va`, so omitted index is treated as null there (`:12-25`); this differs from the explicit-member contract frozen for R21.
- The R20 production callsite assigns these exact tools and passes the extractor into the comparator (`.../run-carriers.sh:21-24`, `:438-441`). The comparator’s output-envelope shape is therefore the original extractor’s caller-facing contract, not just a docstring convention.
- Frozen R21 C2 cases require `nullable_eof_positive` to match with explicit null index, while `missing_index` is unevaluable; malformed extractor JSON and nonzero extraction are also unevaluable (`.ufo/waves/round-21/fixture-contract.json:19-39`). The current R21 comparator requires all of `kind/index/va/phase`, accepts null or exact integer for index/va (excluding bool), requires a bounded `{first_failure,last_line}` envelope, and compares kind/index (`.../tools/compare-first-failure.py:32-47`, `:50-74`). Thus the old extractor’s emitted envelope and explicit nullable index fit that input shape; its output field completeness is stronger than R20 comparator’s validation.

## Calibration and gaps

- **Inference, high confidence:** `kind=eof` alone does not imply `index=null`: the original extractor emits a numeric index when the log exposes either `Invalid index: N` (classified as `invalid_index`) or the structured past-EOF detail; it emits null only for the EOFException-only path. The frozen R21 positive therefore correctly tests a legitimate EOF object with an explicit null index, not an absent member and not every EOF report.
- The original extractor selftest has an EOF read with numeric index 900 and an EOFException carrying `Invalid index: 41`; it does not have a dedicated bare-EOFException-only fixture (`.../tools/first-failure-extract.py:199-243`). The nullable branch is present in code but that specific branch is not demonstrated by the checked-in selftest.
- Literal search found no `"kind": "eof"` in the named retained R20 `predictions/`, `evidence/extract/`, or `evidence/compare-rerun/` surfaces. This is only a targeted text-search result, not evidence that no EOF-kind data exists elsewhere; no concrete retained R20 EOF/null-index outcome was located.
- The required LSP device is not mounted: `read xd://lsp` returned “No such tool.” Searches were literal fallback only; caller tracing is anchored by direct source reads, not semantic LSP proof. No external source quote/date applies.

## Parent checks (not run here)

Run the full frozen 20-case R21 C2 battery without changing its denominator, particularly `nullable_eof_positive`, `missing_index`, `malformed_extractor_json`, and `extractor_nonzero`; retain the 19 exact-artifact R20 comparison regression. No tests, builds, linters, or extractor executions were run in this scouting task.

**Report:** `.ufo/waves/round-21/w1/ScoutEofKind.md`
