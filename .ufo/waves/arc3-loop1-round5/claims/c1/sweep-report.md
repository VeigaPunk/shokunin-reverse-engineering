# arc3-loop1-round5 — C1 aggregate sweep report

Consolidated from the 16 c1-chain seat artifacts (SC-1..8, EX-1..4, RV-1..4,
TB-1..4) and the four VZ convergence verdicts. Parent-written aggregate; every
number below is re-derived by the named seats first-hand and quoted with its
seat pointer. HEAD at sweep close: records commit `71668cc` (work `40de383`).

## The six scoped checks

| # | check | verdict | evidence |
|---|---|---|---|
| a | command A at the named work commits | **REPRODUCED** with a grouping correction | table below |
| b | custody-pair selftest (28 cases) | **REPRODUCED** with an invocation correction | `custody-pair.py selftest` → `CLEAN cases=28 passed=28` |
| c | citation-drift probe, both modes | **REPRODUCED** | default `reported findings=0`; `--strict` `clean findings=0` |
| d | census v10 PASS | **REPRODUCED** | `PASS stale=0 ambiguous=0 undeclared=0 unresolved=0`, `PROVINCE.md lines=162` |
| e | PROVINCE 162-line hold + nine stale-literal absences | **DISCREPANCY** — 8/9 absent, one is the adjudicated NO-CHANGE | `JEB (unprobed)` survives at `PROVINCE.md:88` |
| f | Vyper entry claims spot-checked | **REPRODUCED** with one wording correction | 15/15 K/K, runtime sha `57d6fd0a…`, modulo table at `0x600`; CODECOPY copies a 2-byte entry not the whole table |

## (a) command A, re-derived per object — REPRODUCED, grouping corrected

| revision | knowledge/mapped | rules/blocks | round attribution |
|---|---|---|---|
| `fbbbd45` | 82/82 | 13/13 | r1 work |
| `28aa7a9` | 82/82 | 14/14 | r2 work |
| `5be4a26` | 83/83 | 14/14 | **hygiene child of r3, not an r2 commit** |
| `c418be0` | 83/83 | 14/14 | r3 work |
| `520341d` | 83/83 | 14/14 | **r4 C3 work, parent of `40de383`** |
| `40de383` | 84/84 | 14/14 | r4 C1+C2 work |
| HEAD `71668cc` | 84/84 | 14/14 | r4 records |

All rows `missing=[]`, `dangling=[]`, coverage/depth `10.0/10.0`. The counts are
valid for the hashes; the frozen-claim grouping mislabeled `5be4a26` (a
hygiene-only commit — pyc removal + `.gitignore`) as an r2 work commit and
omitted `520341d`. Corrected attribution recorded.

## (b) custody selftest — REPRODUCED, invocation corrected

The frozen-claim spelling `custody-pair.py --selftest` exits 2 (`the following
arguments are required: cmd`). The supported positional `custody-pair.py
selftest` passes `CLEAN cases=28 passed=28 failed=0`. The test result
reproduces; the invocation syntax in the frozen claim (and the SCORECARD
counting-command cell) is wrong. Correction: use the positional subcommand.

## (c) citation-drift probe — REPRODUCED

`--root .` → `reported findings=0 exit=0`; `--root . --strict` → `clean
findings=0 exit=0`. No findings on the landed tree in either mode.

## (d) census v10 — REPRODUCED

`VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0.
`PROVINCE.md` line count 162 confirmed. (The gate's Frontier-region blind spot
is the round-4 R1 residual — the PASS certifies declared-scope hygiene, not the
repaired rows.)

## (e) PROVINCE nine-literal absence — DISCREPANCY (8/9, not "all nine")

`grep -cF` per literal on the landed `PROVINCE.md`: eight of the nine stale
literals are absent; **`JEB (unprobed)` survives at `PROVINCE.md:88`**. This is
not a missed repair — it is the adjudicated NO-CHANGE-with-cause (EX-15 D1:
the verb was probed at r2 and re-probed; no JEB install exists, so "unprobed"
is shorthand for "no JEB surface held", which is true). The r4 SCORECARD line
"all nine stale literals cleared" is a reporting overstatement: the correct
count is **8 literals cleared + 1 adjudicated NO-CHANGE**. Correction applied
to the records (SCORECARD wording) this round.

## (f) Vyper entry spot-check — REPRODUCED, one wording correction

`CarrierV` retained runtime 1,562 B, sha256
`57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`; the three
saved probe envelopes recover the same 15 selectors (15/15, `dispatch:"abi"`).
The runtime carries a 13-entry uint16 table at `0x600`. **Wording correction:**
the entry's dispatch description implies the whole 26-byte table is copied;
decoding the prefix shows `CODECOPY` copies only the selected two-byte entry
(`src=0x600+2*(selector%13)`, `dst=0x1e`, `size=2`), not all 26 bytes. This
corrects `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:21`'s
memory-copy wording; it does not negate the table's presence or the 15/15
result. Correction landed append-only this round (see C2 audit).

## Discrepancy ledger (each names the corrected value)

| item | recorded (wrong) | corrected |
|---|---|---|
| revision grouping | `5be4a26` under r2; `520341d` unlisted | `5be4a26` = r3 hygiene child; `520341d` = r4 C3 work (parent of `40de383`) |
| custody invocation | `--selftest` flag | positional `selftest` subcommand |
| nine-literal absence | "all nine cleared" | 8/9 cleared + 1 adjudicated NO-CHANGE (`JEB (unprobed)`) |
| Vyper CODECOPY | whole 26-byte table copied | 2-byte entry `table[selector%13]` copied |
| roster | `claims-frozen.md:81-86` omits TB-1..4 | TB seats are c1-chain (16 c1 reports incl. 4 TB) — roster-table assignment boundary ambiguous; seat text maps TB→c1 |

Zero re-derivations skipped silently: all six scoped checks ran; five
reproduced (two with invocation/grouping corrections), one (e) is a real
reporting discrepancy corrected in the records.
