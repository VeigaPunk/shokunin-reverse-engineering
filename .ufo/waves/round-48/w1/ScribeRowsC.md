# ScribeRowsC — third pass, failing registry verdict cells (R48-C1 clause 8)

Full report + receipts: `.ufo/waves/round-48/w1/ScribeRowsC/report.md` and
`.ufo/waves/round-48/w1/ScribeRowsC/receipts/` (SHA256SUMS included).

## Findings (scoped)

1. **16 of 40 registry rows fail `meaning_classes`** under the frozen A2 counter; verified
   end-to-end by running the real `score()` v3 on a synthetic landing (real SKILL.md +
   well-formed block 25): `meaning_rows_failed 16`, `registry_missing
   [tools/round-48/meanings.py, tools/round-48/record2.py]`, `census_rederived_equal true`.

2. **All 16 have honest repairs** — class prefixes or one-word rewrites, no semantics
   change; every repaired cell verified `{0:success,1:not-met,2:unevaluable}` and a
   simulated fully-repaired registry scores clause 8 green (`meaning_rows_failed 0`,
   `registry_rows 42` = census 42). Full replacement texts in
   `receipts/proposed-cells.json`; per-row table in `report.md`.
   Two rows had seg-1 failures masked behind seg-0 (counter returns on the first missing
   class): `round-41/c2-controls.py`, `round-43/c2-score-r43.py` — re-check after edits.

3. **`tools/round-46/gate.py` is the arguable row.** Its only exit-1 producer is
   `gate.py:247` `sys.exit("gate.py is a library; …")` — a usage refusal (unevaluable
   class), not a measurement. The frozen `cls["1"]=="not-met"` binding cannot name it
   without vocabulary stretch; the proposed honest text is
   `1=refusal, not a verdict: …` which passes via NOTMET's `refusal` token. If L1 reads
   not-met strictly, the counter's digit→class table is wrong for this tool — the least-
   dishonest landing is the `refusal` phrasing, which never calls the refusal a failed
   measurement.

4. **Residual forgery hole in the frozen clause (new).** Clause 8 binds token shape, not
   meaning: `NOTMET`'s `red` is unanchored (`meanings.py:59`) and the placeholder ban
   covers only `banana|nope|whatever` (`meanings.py:62,233-234`). The forged cell
   `0=met and green; 1=scored; 2=usage error` scores
   `{0:success,1:not-met,2:unevaluable}` — demonstrated through `meaning_classes`
   (`receipts/forgery-probes.txt`, P2/P3). R46-CL7 is closed only against the three named
   mutations; meaning-free rows still score clean. Candidate round-49 routing: anchor the
   unanchored alternates — but note `gate.py`'s honest repair rides that same overlap.

5. **Missing rows drafted**: verdict cells for `tools/round-48/meanings.py` and
   `tools/round-48/record2.py` verified green (report §"Two missing census rows").

Token-level pitfalls for L1 edits: `passes`/`met_target`/`written`/`emitted`/`errored`/
`errors` never satisfy their class regexes; `never a verdict`/`no designed verdict` lack
the `no verdict` token — use `refusal`/`violation`/`failed` or an explicit `not met`.

Frozen bytes untouched; all evidence is read-only scoring. Battery/selftest not run
(sibling seats own it); no installs.
