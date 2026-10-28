# Round 48 number ledger — ExecReportNums

All derivations below are from retained evidence or explicitly labeled as unmeasured. Seat census is the 75-member `r48-w1` manifest at `.ufo/waves/round-48/w1/swarm-registry.json`; the parent integration report should rederive from that frozen manifest if the registry changes.

| Number | Value | Exact deriving command / evidence | Receipt |
|---|---:|---|---|
| Registered seats | 75 | `python3 -c 'import json,collections; p="/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-48/w1/swarm-registry.json"; d=json.load(open(p)); m=d["members"]; print("seats",len(m)); print("roles",dict(sorted(collections.Counter(x["role"] for x in m.values()).items()))); print("wave",d["wave"]))'` → `seats 75` | stdout retained in this execution transcript; no hashed receipt captured |
| Wave size | 75 | Same command; `len(d["members"])` | same |
| Role mix | executor 22; scribe 16; scout 9; reviewer 9; critic 6; mutation-tester 6; connector 2; revenger 2; simplifier 2; sentinel 1 | Same command; `Counter(x["role"] for x in m.values())` | same |
| C1 marker rows before landing | 0 marker occurrences; 0 marker blocks; 24 rule blocks | Frozen counter receipt `C1IdsArms/receipt.json` | `.ufo/waves/round-48/w1/C1IdsArms/receipt.json` |
| C1 registry meaning rows failed | Not measured in this run; counter battery skipped because structural marker clause failed | Receipt has `battery.skipped = "artefact fails a structural clause first"`. Do not state a failed-row count as observed. | same |
| C1 forged-arm attempt | `v3_exit=1`, `v2_exit=1`; invalid fixture (three unresolved citations, stale pin, malformed census), so it establishes no meaningful v2/v3 distinction | `C1IdsArms/fixtures/permuted-arms-result.json` | `.ufo/waves/round-48/w1/C1IdsArms/fixtures/permuted-arms-result.json` |
| C2 floor counts | Sections have no completed valid landing; round-47 seat atom absent (other receipt fields are retained) | Counter output recorded in `C2Quote/counter-receipt.json`; `failing` includes `round-47: no seat atom and no re-derived seats correction` | `.ufo/waves/round-48/w1/C2Quote/counter-receipt.json` |
| C2 correction lines re-derived | 0 | Same receipt: `corrections: 0`; `corrections_bad: []`; no round-48 correction line re-derived | same |
| C2 quoted-number failures | 1 | Same receipt: `failing` includes `quoted numbers with no backing receipt: 1` | same |
| C2 axes atoms | 2 | Same receipt: `axes_atoms: 2` | same |
| C2 axes score cells | Coverage 138/138 → 9.72, score 10.0; depth 24/24 → 10.0, score 10.0; `axis_score_bad=[]` | Same receipt: `axis_score_cells` / `axis_score_bad` | same |
| C1/C2 forensic battery green counts | Not measured; both batteries skipped before structural requirements passed | C1 and C2 receipts explicitly say battery skipped | respective receipts |
| Self-test case count | C1 16 cases, 0 failures | `ExecSelftest.md` records exact output `MEANINGS_SELFTEST: cases=16 failures=0` | `.ufo/waves/round-48/w1/ExecSelftest.md` (no stdout hash/time-of-day captured) |
| C2 self-test result | parser checks only; no numeric case total | Exact output in `ExecSelftest.md`: `corr_parse: true`, quote parser outputs atoms 42/exempted 1 and receipt path | same |

## Evidence limits

No new counter run or forge battery was executed in this seat; all claims above are carefully limited to retained peer receipts, not inferred pass counts. The registered roster is a 75-seat manifest, not evidence of 75 agents completing work. Do not present the skipped C1/C2 live batteries as green or as numeric before/after results. Receipts gathered by peers lack complete exact command/stdout SHA-256/UTC-time tuples in several cases; this ledger does not fabricate missing fields. Disk guard reported 32% utilization and 546.1G available on `/fast/scratch/hyaku`; no install performed. No source or frozen file was changed.