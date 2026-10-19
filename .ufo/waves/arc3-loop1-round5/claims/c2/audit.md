# arc3-loop1-round5 — C2 aggregate corpus audit

Consolidated from the 16 c2-chain seat artifacts (EX-5..12, CR-1..4, RV-5..8)
and the VZ/CR verdict seats. Parent-written aggregate; each row cites the seat
that re-derived it first-hand. HEAD at audit close: `71668cc` (work `40de383`).

Audit unit: the three dated arc3 knowledge entries
(`2026-10-19-arc3-r1-evm-real-solc`, `…-r3-evm-optimizer-shapes`,
`…-r4-evm-vyper-leg`) plus their append-only errata and the new Ghidra erratum.
Statuses: VERIFIED / CORRECTED / UNVERIFIABLE.

## Per-claim audit table

| entry / claim | status | evidence |
|---|---|---|
| r1 selector sets & decoded identities (Rv2Token 5/5, Rv2Many 11/11, KdxToken 6/6; solc linear/EQ shape) | **VERIFIED** | CR-2 `evidence/rederive.out:1-11`; EX-12 `:7`; EX-5 `:22` |
| r1 Smoke creation digest domain | **CORRECTED** | `Smoke.bin` is 1,370 ASCII-hex B sha `530efc7b…`; the 685 B is the *decoded* bytecode sha `08299f31…` — the entry pairs decoded size with the text-carrier digest (`:15`). Two byte domains; clarify append-only. (VZ-1, CR-2, EX-5) |
| r1 creation/initcode absence | **VERIFIED as corrected** | the r1 append-only erratum at `:31` already records the parsed-and-empty-vs-embedded-bytes distinction (Rv2Token runtime 1,943 B embedded at +28 in its 1,971 B creation). (EX-5 `:23,26`, CR-2 `:16`, EX-12 `:31`) |
| r3 selector sets & shapes (VaultB opt/nopt 13/13, carrierB 11/11, CarrierB/Err 8/8, Rv2TokenOpt 5/5; JUMPDEST offsets; carrier-A `(58,48,38)` non-JUMPDEST exception) | **VERIFIED** | EX-12 `:13,27`; EX-5 `:25`; the opt200 EQ/GT/PUSH4 counts reproduce the binary-search class |
| r3 convergence-matrix roster rows (CarrierA opt K=9, vaultB opt K=11, OptVault K=5, MutMix K=6, MutMixOpt K=6) | **UNVERIFIABLE** | primary sealed probe envelopes not retained in the r3 evidence set; matrix-only rows. (CR-2 `:23`) |
| r3 creation/initcode wording (`:24` "Creation blobs carry no runtime dispatch table") | **CORRECTED** | same defect class as r1's pre-erratum line: runtimes are byte-embedded in initcode (VaultB opt200 +34, nopt +80, carrierB +387/+1404, CarrierB +91). The corrected reading is probe-scope (parsed-and-empty), not byte absence. (EX-12 `:31`, EX-5 `:26`) |
| r4 selector sets & byte identities (CarrierV 15/15 `57d6fd0a…`, Ex09Vault 7/7 `54b14e30…`, StewardToken 22/22 `1846469b…`, CarrierW 9/9 `67d1d88f…`, Smoke 4/4 `415e6b1b…`) | **VERIFIED** | EX-5 `:27`, EX-12 `:19-25`, CR-2 `:27`; method-id maps reproduce (with the `__default__()` phantom-key caveat) |
| r4 modulo-indexed Vyper dispatch (XOR chain, `push4_pc+11` offset rule, JUMPDEST-at-`offset−12`, 13-entry table at `0x600`, Ex09Vault 6-entry at `0x239`) | **VERIFIED** | EX-5 `:28`, EX-12 `:29`, CR-2 `:28`; the offset rule is a different convention from solc's JUMPDESTs — both correct, family-scoped |
| r4 CODECOPY wording (`:21`) | **CORRECTED** | the prefix copies the selected 2-byte entry (`src=0x600+2*(sel%13)`, `size=2`), not the whole 26-byte table. (VZ-1, EX-5 `:28`) |
| r4 creation/initcode absence (`:17` "initcode carries no runtime dispatch table") | **CORRECTED — real defect** | CarrierV runtime byte-exactly embedded at +20 in its 1,637 B creation; Ex09Vault +24; Smoke +27. Creation probes return 0 functions — parsed-and-empty is the probe result, not proof of byte absence (per `corpus/QUALITY.md:21`). (EX-5 `:29`, EX-12 `:31`) |
| r4 Ex09Vault input-text identity (`:13`) | **CORRECTED / UNVERIFIABLE provenance** | local hex `vyper/Ex09Vault.runtime.hex` = 1,165 B `05a29536…`; the probe envelope's input = 1,163 B `aee38762…`. Different input-text serializations of the *same* decoded 581 B runtime `54b14e30…`. Not a runtime-digest mismatch; the 2-byte difference is unverifiable (temp input gone). (EX-5 `:29`, CR-2 `:29`) |
| r4 "no Core promotion" scope (`:30`) | **CORRECTED — real defect** | the same work commit `40de383` writes "Core, arc3-r1/r3" and "Core, arc3-r4" into `PROVINCE.md:91-93`; `LOG.md:1495-1500` cites the entry. The RESULT-class / no-availability→holding qualifications stay valid for the probe, but the flat "no Core promotion" sentence is contradicted by the same-commit PROVINCE wording. (EX-5 `:31`) |
| r1/r3 "no Core promotion" (historical) | **VERIFIED at their round scope** | predates the r4 PROVINCE promotion; the promotion is what r4's same commit did — the earlier entries' scope statements are unchanged and correct for their classes. (EX-5 `:31`) |
| r3-07 historical Carrier-3 offsets 62/68/74 = JUMPDESTs | **UNVERIFIABLE** | the `/tmp` carrier/probe is not retained; recorded, not disproved. (CR-2 `:35`) |
| Ghidra feature-count erratum | **VERIFIED** | `ls -1 …/Ghidra/Features` = 34; PROVINCE:46 = 34; `40de383` diff shows the 35→34 row change + the append-only erratum in the same commit. (EX-5 `:30`, EX-12 `:37`, CR-2 `:36`) |
| compiler-install provenance + every inferred argument/mutability | **UNVERIFIABLE in this seat** | sources hashed but installs/builds not replayed; the entries' own upstream-inference caveats stand. (EX-5 `:32`) |

## Corrections to land (append-only, never rewrites)

1. **r4 `:17`** — append an erratum: "initcode carries no runtime dispatch
   table" → corrected to the parsed-and-empty reading; the runtime is
   byte-embedded in initcode (CarrierV +20, Ex09Vault +24, Smoke +27), which
   does not mean the initcode executes that dispatcher.
2. **r4 `:21`** — CODECOPY copies the selected 2-byte entry, not the 26-byte
   table (fold into the same erratum).
3. **r4 `:30`** — append an erratum qualifying "no Core promotion": at this
   round's own work commit `40de383`, PROVINCE:91-93 lists the arc3 EVM
   carriers as Core; the RESULT-class / no-availability→holding scope stands,
   the flat no-promotion sentence is superseded by the same-commit promotion.
4. **r3 `:24`** — same initcode class as (1): "Creation blobs carry no runtime
   dispatch table" → parsed-and-empty; runtimes embedded (offsets measured).
5. **r1 `:15`** — Smoke digest domain: the 685 B is decoded-bytecode size with
   sha `08299f31…`; `530efc7b…` is the 1,370 B ASCII-hex file's digest.
6. **PROVINCE:91-93 vs r4 `:30`** — resolved by (3): PROVINCE's Core wording is
   authoritative post-`40de383`; no PROVINCE change needed.

Items named for the parent that stay as audit-record only (not corpus edits):
the r3 matrix-only roster rows are UNVERIFIABLE (evidence not retained —
recorded, not corrected); the r3-07 Carrier-3 offsets are UNVERIFIABLE
(historical `/tmp` gone — recorded, not disproved); the EX-09 dispatch note at
`arc3-loop1-round4/claims/c1/EX-09/analysis/dispatch-structure.txt:12-21`
(says two selectors absent) contradicts its own support record — a wave
artifact correction, out of corpus scope, flagged.

Verdict: **the audit is complete at the seat level; two entries carry real
defects (r4 initcode + no-Core, r3 initcode) and two carry wording/domain
corrections (r4 CODECOPY, r1 Smoke domain). All corrections land append-only
this round.**
