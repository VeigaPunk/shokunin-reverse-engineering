# R35Audit19 — audit 677 count method

Seat: `R35Audit19` (executor). Scope: read-only audit; only lane write is this report. No VCS mutation, scoring, counter changes, delegation, or external-source access.

## Findings

**F1 — VERIFIED: the C1 counter is a finite predicate checklist, not a cardinality count.** `tools/round-35/c1-coverage-counter.py:98-141` returns named failures for two fixed entry paths, three anchored provenance lines and row citation per entry, S125/S129 registry rows with `status=mined`, date-prefix and used-by checks, plus substring presence in PROVINCE and README. It does not calculate knowledge-entry totals or measure semantic coverage. A pass is the conjunction of these declared tokens/locations, not a count of the broader corpus.

**F2 — VERIFIED: C2 is four closure checks with a small numeric equality, not a score.** `tools/round-35/c2-calibration-counter.py:60-153` checks D1 census content and commit-time ordering, D2 required lesson tokens and equality of the parsed lesson seat tuple to aggregate `spawned/settled/dead` values, D3 three line prefixes plus S106 token, and D4 8-cell rows in two specifically located sections. The counter's success means no recorded failures; no weighting, normalized score, or aggregate quantity is produced.

**F3 — VERIFIED: this method aligns with the frozen concrete after-state.** The plan specifies two named C1 entries and four named C2 defects; C1 has six receipt check groups and C2 reports the individual failing IDs. Do-nothing controls at base are committed and fail: C1 lists missing entries/rows/map tokens, while C2 lists D1-D4 failures. Therefore these claims are not reachable by merely leaving the base tree unchanged.

**F4 — MATERIAL LIMIT: counters establish presence/structure, not full semantic correctness.** C1 row matching uses an 11-column regex that captures the first ten cells after ID and then checks only selected cells; it does not verify URL reachability, source truth, source quality, or whether the entry content accurately teaches the mapper. `source:` only needs to contain the row token. PROVINCE/README checks are unscoped substring tests. C2's census requires the substrings `rows=106`, `EXIT=0`, and `W04`, rather than parsing warning count or full output; its commit ordering compares Git commit timestamps, which are not a total-order proof under skew/equal timestamps. D2 JSON values are checked with `isinstance(v, int)` (Python booleans qualify as integers) and totals default malformed/missing values to zero after recording failures; D3 is substring-based; D4 checks pipe count, not Markdown cell parsing. These are limits of what a counter pass demonstrates, not evidence that the frozen predicates should be widened.

**F5 — VERIFIED setup-order limitation.** `.ufo/waves/round-35/freeze-status.md` records the earlier freeze-integrity failure and states the canonical freeze's instrument-revision debt and that C1/C2 were not scored before the final freeze. Current counter bytes match the pins in `claims-canonical.json`; `instrument_revision` names `d2729cba`, whose counter hashes differ from the current hashes. The committed controls and current hashes show the later final instruments; do not represent this as clean instrument-first scoring. The counters require `claims-canonical.json` at the supplied `--freeze`; that file is absent at `f1ea3a6d` and present at `2323d197`, so scoring with the former gives unevaluable/exit 2, not a base red result. A counter selftest's synthetic-green/single-red-path result alone cannot repair this history.

## Exact evidence and commands

- Read `plans/round-35-claims.md` (C1/C2 after-states and controls), `claims-canonical.json`, both counter sources, `freeze-status.md`, and committed do-nothing receipts. The receipts say C1 base fails on two entries, two registry rows, two province stems and two README entries; C2 base failures name D1, D2, D3 and D4.
- `sha256sum tools/round-35/c1-coverage-counter.py tools/round-35/c2-calibration-counter.py` → `e28792c7e54fcfa2185fe12f07c9e3eb328652d405e98d1ffaf2737b28d24220` and `576c14dd95c0a54b2de05b765d171b25429a893289b85516258e83daa9179b94`; both equal canonical instrument pins. Plan hash equals canonical plan pin.
- `git show <rev>:tools/round-35/{counter}` hash comparison: at `d2729cba`, C1 `cd4ab7e7…`, C2 `39fe39c5…`; at `a85ca674`, C1 `018e96d0…`, C2 `3a23f3eb…`; at `f1ea3a6d`, C1 `d49ff16a…`, C2 `c0f37d21…`; at `2323d197` and HEAD, hashes match the current pins above.
- `git cat-file -e <rev>:.ufo/waves/round-35/claims-canonical.json`: absent at `f1ea3a6d`, `e4ca43dd`, `13d7a815`; present at `2323d197`.
- Predicate identity check: canonical predicate == counter constant == do-nothing receipt predicate for each claim (whitespace-normalized). Plan does not spell either P35 predicate sentence verbatim; it specifies the corresponding after-state/checks. Plan SHA256 matches canonical plan pin.

## Limits

No live counter run, selftest, or alternate mutation was performed; other wave seats own those checks. Counts above are read from counter logic / committed receipts, not freshly produced scoring output. No source fetch or source-semantic audit; conclusions are strictly about count/check mechanics. No lane production edits, no VCS state change, no package installs, and no `/fast/scratch` traversal.

Report: `.ufo/waves/round-35/w1/R35Audit19.md`
