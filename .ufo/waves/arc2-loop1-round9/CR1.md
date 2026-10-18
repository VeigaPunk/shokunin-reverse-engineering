# CR1 — C1 dated-summary revisionism review

## (1) Verdict

**C1's target pair is wrong; do not land it as stated.** The current-state rows are `corpus/README.md:22` and `:175` (the latter is baseline `:174`, per `SCORECARD.md:16-17`), not `:22` and `:117`. Rewording a mutable index summary is not inherently revisionism when it preserves the at-the-time result, temporal scope, and evidence. But `:117` is the dated Knowledge-table synopsis of the 2026-10-13 r4 entry (`verified-at 2026-10-13`); replacing that historical result with the r7/r8 outcome would rewrite its meaning. Leave `:117` unchanged. Correct the two live summaries in place and explicitly keep r4/r6 outcomes historical. The numerical `2→0` may fit those corrected targets, but the claimed `:22/:117` edits would leave the actual current Frontier assertion at `:175` stale. Existing gates do not count these README wall statements, so the metric needs a disclosed textual census, not an implied gate PASS.

**Line:** update present-state summaries; preserve a dated observation's original finding, date, and limitations (or append a clearly scoped erratum). A rewrite crosses into revisionism when it removes/recasts what the old run found, imports later evidence as if known then, or erases its uncertainty. The r7 wall entry's own r8 erratum is the model: append-only, attribution scoped, unknown updated explicitly.

## (2) Evidence — textual only; no live probes

- Command: `git show HEAD:corpus/README.md | awk 'NR==22 || NR==117'`.
  Output excerpt: row 22 joins the r4/r6/r7 entries but says the 91.6MB PE `dies at the ~900s` deadline; row 117 summarizes only `2026-10-13-r4-12` as `provider_timeout` and ends `| 2026-10-13`. Resolving pointers: `corpus/README.md:22,70-74,117`. Row 22 is a current synthesis; row 117 is a dated r4 index row.
- Command: `git show HEAD:corpus/README.md | awk 'NR>=170 && NR<=177'`.
  Output excerpt at current `:175`: `>90MB PE scale — 91.6MB Godot ARM64 hits the ~900s internal session deadline; raise ... or bisect 2-5MB.` This is the live Frontier claim that remains stale if only `:22/:117` are touched. `SCORECARD.md:1215-1216` names the debt as `README:22/:174`; `SCORECARD.md:16-17` says pre-existing-file citations are baseline-relative and the inserted lesson row shifts later README lines, resolving baseline `:174` to current `:175`.
- Command: `git show HEAD:corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md | awk 'NR>=13 && NR<=20 || NR>=23 && NR<=37'`.
  Output excerpt: `:13` r7 exit 0 / `Result=success`, 1424.663s, 7.9G peak; `:15` 75,218 procedures and `+disabled` preset; `:19` records the wall falling and natural-hold unknown; `:23` labels the r8 correction append-only; `:29-37` records the no-disable control OOM kill, no natural hold at this cap, and rerun-ID unknown. Resolving path: `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:13-37`.
- Command: `git show HEAD:.ufo/waves/arc2-loop1-round8/E2.md | awk 'NR>=23 && NR<=46'`.
  Output excerpt: `:27-31` `Result=oom-kill`, peak equals 9 GiB cap, raised deadline unused; `:32-42` unit/kernel journal says OOM killer, 4m42.945s and memcg-scoped Java kill. Resolving path: `.ufo/waves/arc2-loop1-round8/E2.md:23-46`.
- Command: `git show HEAD:.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json | awk 'NR<=7 || NR>=35 && NR<=39'`.
  Output excerpt: `:2-4 code/category/message: cancelled`; `:38-39 failure_kind: cancelled; failure_message: Ghidra startup was cancelled`. The receipt alone is not an OOM verdict; pair it with E2's unit/kernel journals. The erratum correctly preserves both channels at `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:29-33`.
- Commands: `git show HEAD:SCORECARD.md | awk '(NR>=16 && NR<=17) || (NR>=1212 && NR<=1217)'`; `git show HEAD:SCORECARD.md | awk '(NR>=275 && NR<=301) || (NR>=781 && NR<=791)'`.
  Output excerpts: `:16-17` baseline-relative README citations; `:1215-16` stale debt `:22/:174`; `:280-300` says historical evidence cells stay byte-identical and dated Core cells/append-only logs were untouched; `:789-791` says dated records were adjudicated, not edited. Resolving paths: `SCORECARD.md:16-17,275-300,789-791,1215-1217`.
- Instrument boundary: `.ufo/gates/c1-census-v10.py:5-18,85-107` scopes its current/dated census to REA version/pin statements in PROVINCE/SKILL/SCORECARD, not README wall status. `.ufo/gates/citation-drift/citation-drift-probe.py:4-16,78-84,189-195` says it reports pinned citation drift; quoted append-only records must stay verbatim. Neither instrument proves a README stale-row count. `corpus/lessons/2026-10-18-wave-dispatch-counting.md:29-37` likewise says correct records append-only when census and records disagree.

## (3) Verbatim-landable text

Replace only the two current-state rows (`corpus/README.md:22` and current `:175`) in place; keep the Knowledge row at `:117` byte-identical:

```text
| `knowledge/2026-10-13-r4-12-godot-arm64-scale`, `2026-10-18-arc2-r6-pe-midrung`, `2026-10-18-arc2-r7-pe-wall` | Historical r4 timeout and r6 name-validation refusal remain dated outcomes. Current 91.6MB result: r7 HELD with three validated analyzers disabled (9 segments / 75,218 procedures, 1424.663s, 7.9G peak); r8 no-disable natural control OOM-killed at 9G in 4m42.945s (REA envelope typed `cancelled`, no evidence_id). No natural hold at this cap; rerun id-stability remains unknown. | History: `corpus/README.md:117` (r4), `SCORECARD.md:1045-1053` (r6); r7: `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:13-19`; r8: `.ufo/waves/arc2-loop1-round8/E2.md:23-45` + `receipts/r8-ctl-envelope.json` |
- >90MB PE scale — CLOSED, not frontier: r7's validated analyzer-disable recipe produced a mitigated hold; r8's no-disable control OOM-killed at 9G in 4m42.945s. No natural hold at this cap; rerun id-stability remains unknown (`SCORECARD.md:1217`; r7: `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:13-37`; r8: `.ufo/waves/arc2-loop1-round8/E2.md:23-45`).
```

## (4) Observation / inference / unknown

- **Observation:** the dated r4 index row ends `verified-at 2026-10-13`; the current Frontier bullet still prescribes timeout work; round 8 retired the wall thread (`SCORECARD.md:1217`).
- **Inference:** safe freshness work is `:22` + current `:175`; editing `:117` to replace the r4 outcome would be revisionist, while an explicit, chronology-preserving annotation would not be. Better leave it unchanged because it indexes the dated source.
- **Unknown:** no round-9 proposed diff or README-specific census command was supplied, so the actual same-line/zero-shift edit and claimed `2→0` count are not verified. No live probes were run.
