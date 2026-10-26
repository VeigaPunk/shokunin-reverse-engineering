# Exact dummy rows used in the scratch mirror test (R39RevCensus, 2026-10-26)

Well-formed rows S118 and S119 — inserted after the S117 line, inside `## Registry`:

```
| S118 | Dummy source one (R39RevCensus scratch mirror test) — https://example.org/dummy-s118 | docs | B | scratch mirror test row one (not a real source) | test anchor `Registry` (dummy) | WELL-FORMED SCRATCH TEST ROW: proves a well-formed append passes the census gate; delete before use. | queued | 2026-10-26 | 90d | — |
| S119 | Dummy source two (R39RevCensus scratch mirror test) — https://example.org/dummy-s119 | docs | B | scratch mirror test row two (not a real source) | test anchor `Registry` (dummy) | WELL-FORMED SCRATCH TEST ROW: proves a second well-formed append passes the census gate; delete before use. | queued | 2026-10-26 | 90d | — |
```

Malformed row S120 — escaped pipe `\|` inside the `teaches` cell; awk `-F'|'` counts the
pipe as a separator, so the line has 13 textual cells instead of 11 → E01:

```
| S120 | Dummy source three, malformed (R39RevCensus scratch mirror test) — https://example.org/dummy-s120 | docs | B | scratch mirror test row three (not a real source) | test anchor `Registry` (dummy) | MALFORMED ROW: cell text contains an escaped pipe X \| Y which awk -F'|' counts as a column separator, so NF!=13. | queued | 2026-10-26 | 90d | — |
```

These rows exist only in scratch mirrors (`/fast/scratch/hyaku/kaidoku-r39/R39RevCensus/…`,
removed after the test). They were never written to the lane registry.
