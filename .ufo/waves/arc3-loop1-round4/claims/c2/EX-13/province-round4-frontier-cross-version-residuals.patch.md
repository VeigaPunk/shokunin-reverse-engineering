# PROVINCE.md repair — Round-4 frontier bullet "Cross-version residuals": `compare-application-versions` is no longer probe-refused

Authored by SEAT EX-13 (chain c2, executor), wave `arc3-loop1-round4`, 2026-10-19.
**Patch text only** — seats never write `PROVINCE.md`; the parent applies.

## Stale item (census-checked, falsified)

`PROVINCE.md` `### Round-4 frontier (post-unlock)` bullet `Cross-version
residuals`, current bytes:

> `compare-application-versions` still probe-refused since r2; multi-version
> pacman pairs beyond expac unexercised

The first clause is falsified: the verb's success path is exercised and
admitted. The second clause stands and is preserved.

Admitted corpus:

- `corpus/knowledge/2026-10-14-r12-02-queue-b-ledger.md` — row **L203
  `compare-application-versions` success path — WAS TRULY-OPEN, NOW EXERCISED
  (this lane, both classes; candidates 1–3)**; run-log row 4:
  `compare-application-versions cav-js.in.json` (39,119,964 B) → exit 0, 3.3 s,
  `ev_7a8d0ec4…`/`javc_efb02d28…`, 10 changed/208 unknown; row 9:
  `cav-mgd.in.json` ×2 → `ev_b5fc998f…`, `{unknown:4114}`, byte-identical.
  The entry's own header records that before this lane the verb existed in the
  corpus "only as the r2 typed refusal".
- `corpus/knowledge/2026-10-14-r14-01-queue-b-residual.md` — Candidate 1: the
  **runtime-reconciliation input class** (the sub-class r12-02 left open) is
  accepted: exit 0, 0.75 s, `ev_8f0ac46c…`, comparison_id `javc_b64686f7…`,
  over 86 items; "**L203 is now wholly discharged**: all three named input
  classes (JavaScript analysis, runtime reconciliation, managed application
  graph) exercised with live successes".

So the r2 refusal datum (`corpus/knowledge/2026-10-13-r2-version-diff-compare.md`
run-log row 13) is **historical**, not the verb's current state.

**Not repaired:** `multi-version pacman pairs beyond expac unexercised`. The
admitted pacman pair work covers `expac`, `bwrap` and `op`
(`corpus/knowledge/2026-10-13-r2-version-diff-compare.md`,
`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md`) — the clause's own
claim is that pairs *beyond* those are unexercised, which the corpus does not
contradict. It stays verbatim.

## Change (same-line replacement, line count held at 4)

`PROVINCE.md`

```diff
# file: PROVINCE.md
-- **Cross-version residuals** — `compare-application-versions` still
-  probe-refused since r2; multi-version pacman pairs beyond expac unexercised
-  [r5-audit C1: merged from the pruned Frontier bullet — its
-  `compare_javascript_export_shapes` item is now held (Core, r4-09)].
+- **Cross-version residuals** — `compare-application-versions` exercised since
+  r12 (all three input classes; the r2 refusal is historical); multi-version
+  pacman pairs beyond expac unexercised [r5-audit C1: merged from the pruned
+  Frontier bullet — its `compare_javascript_export_shapes` item is now held (Core, r4-09)].
```

## Census conformance

- Line-neutral: 4 → 4 lines; `PROVINCE.md` stays at 162 lines (DATED marker at
  line 119 does not shift; this bullet sits at 157–160).
- Needle-free: no `rea-agents@x.y.z`, no bare `6.x.y`, no `~`/`/`-absolute
  `path:line`. (`r12`/`r2` are round tokens, not version pins.)
- The `[r5-audit C1: …]` annotation and the `compare_javascript_export_shapes`
  clause are preserved verbatim — both still true.
- Search text verbatim and unique (verified in the apply-and-census run under
  `claims/c2/EX-13/evidence/`).
