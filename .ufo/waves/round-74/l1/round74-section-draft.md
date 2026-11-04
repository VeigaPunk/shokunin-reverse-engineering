## 2026-11-04 — round 74: the selftest's six survivors close, and the record binds its routed set

Base `04fdc2c4dbedbe5ee50a069af14310068393233e`; declaration `b3a7e28` (five round-74
instruments, the plan, the census-start receipt); pre-freeze instrument revision `b3a7e28`
(receipts bind their runners, selftest case names); freeze `021914c0e638454e507087accfe41af1ab69f185`
(the round-29 gate audits it **CLEAN**, no findings — planned item (d) demonstrated, unlike the
round-73 freeze's permanent `INSTRUMENT_PIN_MISMATCH`). Two claims on two distinct axes, both
capability acquisitions.

**lowest-axis: calibration** (coverage/depth/calibration tied at 10.0 behind different proxies;
R74-C2 works a tied-lowest axis). No nudge waiver is claimed.

| claim | axis | type | predicate (frozen) | before → after | verdict |
|---|---|---|---|---|---|
| R74-C1 | operability | capability acquisition (probe-mutation closure) | the frozen battery reports patch set `r74probe` `survivor_count 0`, each mutant killed by its declared case, pristine 20 cases green, target pinned — while `r73probe` on the landed round-73 probe names exactly the six MutProbe survivors | base `pre/c1-base-arm.json`: 6 survivors (the six MutProbe names), 4 killed; landing `l1/scores/c1-at-landing.json`: 0 survivors, 10 killed-by-declared-case | |
| R74-C2 | calibration | capability acquisition (record audit v2) | the frozen audit at the measured revision exits 0 with `mismatch_count 0` over 16 atoms — while at base it exits 1 with 11 mismatches naming D3, D6, D7b, D8–D15 | base `pre/c2-at-base.json`: 11 mismatches; landing `l1/scores/c2-at-landing.json`: 0 | |

**Capabilities entered.** (1) a probe-mutation closure that scores each selftest conjunct against
a declared case and refuses a wrong-case kill, first working round 74; (2) a record audit that
binds the previous round's routed-defect list, its own pointer selection, the capability table,
the registry's rejected rows and its freeze pins, first working round 74.

**Name by surface.** R74-C1's surface is the selftest's acquisition and wiring seams
(`kernel_witness`'s injected readers, `forged_subrun`, `assemble_arm`), not the runtime arm.
R74-C2's surface is the record's own evidence pointers and the freeze container it pins, not the
instruments' runtime behaviour.

**census erratum (round-73 report).** The round-73 report states the end census prints 24 W04
lines; the committed receipt prints 23 (`grep -c W04 .ufo/waves/round-73/l1/census-end.txt` → 23,
the file's 24th line being the `ok` row). The filed report is never rewritten; both values are
recorded here (routed defect 5).

**Wave.** One v1 wave `r74-w1`: 15 seats (5 executor, 3 scribe, 2 reviewer, 1 critic, 1
mutation-tester, 1 sentinel, 1 scout, 1 connector); attack roles 4/15 = 27%; one connector;
L1 held the planner seat; no residual call.

**planned (next steered round only):** the debt the wave names; standing duties every round that
lands receipts.
