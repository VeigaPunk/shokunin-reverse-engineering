# CN-3 — arc3-loop1-round5 convergence verdict

## Scope and current inventory

This reconciliation follows `claims-frozen.md:17-79` and compares available seat reports with the frozen roster (`:81-86`). The current Markdown inventory was re-enumerated at verdict time: C1 has 16/16 expected reports plus unrostered TB-1..TB-4; C2 has 15/16 (EX-9 absent); C3 has 16/16. The required `claims/c1/sweep-report.md`, `claims/c2/audit.md`, and `claims/c3/disposition.md` are all absent. Older CN-2/CN-4 inventory statements are snapshots superseded by later C2 and C3 reports.

No REA provider probe, expensive retest, or seat re-dispatch was run. No corpus, PROVINCE, SCORECARD, LOG, or other seat artifact was changed.

## C1 — calibration: substantive checks reproduce, with discrepancies

**Command A:** independently re-derived values recorded in `claims/verdicts/CN-2.md:11-25` (also compared with C1 `EX-3.md:7-18`):

| Revision | Mapped / files | Resolved / rules |
|---|---:|---:|
| `fbbbd45` | 82/82 | 13/13 |
| `28aa7a9` | 82/82 | 14/14 |
| `5be4a26` | 83/83 | 14/14 |
| `c418be0` | 83/83 | 14/14 |
| `520341d` | 83/83 | 14/14 |
| `40de383` | 84/84 | 14/14 |
| HEAD `71668cc` | 84/84 | 14/14 |

All recorded objects have empty missing/dangling sets and 10.0/10.0 scores. The values reproduce, but the frozen shorthand is not a linear round history: `5be4a26` is a hygiene child of `c418be0`, not an R2 work commit, and `520341d` is parent of `40de383` (`CN-2.md:25`).

- Census v10 passes; citation drift default and strict both report zero findings. The frozen custody command `custody-pair.py --selftest` fails argparse (exit 2); the supported `custody-pair.py selftest` passes 28/28 (`CN-2.md:27-32`).
- The exact nine-literal vector from round 4 yields **8/9 absent**, not 9/9: `JEB (unprobed)` remains at `PROVINCE.md:88`. SCORECARD records a JEB no-change-with-cause disposition, but that does not make the literal absent. SC-4/EX-4 use a different vector that omits JEB (`CN-2.md:39-40`; `CN-4.md:36-40`).
- CarrierV’s 15/15 selectors, 1,562-byte runtime identity and table contents reproduce. However, r4’s dispatcher copies one selected **2-byte** table entry from the 26-byte table at `0x600`, not all 13 entries; the r4 prose at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:21` overstates the CODECOPY length. The byte walk is recorded in `claims/c1/EX-3.md:28-30`.

The C1 individual roster is present, but the frozen consolidated sweep report is absent; C1 is not closed at the required artifact level.

## C2 — coverage: substantial byte evidence, but chain result UNVERIFIABLE-with-cause

CR-3 and RV-8 have now appeared, bringing the count to 15/16; prior CN-2/CN-4 counts are stale. The audited principal selector sets, decoded byte counts and SHA-256 identities for retained r1/r3/r4 carriers broadly reproduce (`claims/c2/CR-3.md:13-30`, `claims/c2/RV-8.md:7-53`). This does not establish every alternate/cross-pin leg or matrix-only probe identity; e.g. the solc npm-tarball digest and exact matrix IDs remain unverified (`CR-3.md:36`, `RV-8.md:60-61`).

Material corrections and limits:

- **Byte domains:** r1’s Smoke file is 1,370 bytes of hex text with its own digest; decoding yields 685 bytes and a different digest. The r1 sentence at `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:15` conflates those domains (`CR-3.md:17`).
- **Creation probes:** zero returned functions means parsed-and-empty, not that creation bytes lack embedded runtime. The Rv2Token, VaultB opt200, and CarrierV creation blobs embed their runtimes at offsets 28, 34, and 20. R1’s append-only correction at `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:31` addresses its older `:24` wording; r4’s corresponding false wording remains at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:17`. EX-12’s pointer to r3 `:24` is wrong: that line is the Rv2TokenOpt result, not the quoted creation claim (`claims/c2/EX-12.md:31`; `claims/c2/RV-8.md:13`). Embedded bytes do not show that initcode executes the runtime dispatcher.
- **r3 trailer:** `43000825` is in the CBOR trailer, beyond code ends 3,110 (VaultB nopt) and 925 (Rv2TokenOpt), not an executable code-region PUSH4 as r3 `:26` implies (`CN-2.md:60`).
- **Vyper dispatch:** the same r4 entry’s table-copy description at `:21` needs the 2-byte correction above. Separately, EX-10’s two-selector-missing report is a traversal false negative: direct walking of Ex09Vault’s table and chains recovers all seven expected selectors (`CN-2.md:62`).
- **Core boundary:** r1/r3 entries disclaim Core promotion (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:33`, `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:35`), while `PROVINCE.md:92` explicitly calls real-solc arc3-r1/r3 Core. PROVINCE mentions Vyper arc3-r4 at `:93` without an explicit Core parenthetical. This is a cross-file status conflict for r1/r3; do not overstate r4 as explicitly Core. Preserve the entries’ no-availability-to-holding limit (`CR-3.md:35`, `RV-8.md:14,35,53`).
- **Scope:** the freeze calls for four arc3 entries plus r2/r3 errata, but the corpus has only three dated `2026-10-19-arc3-r*.md` entries (r1/r3/r4); C2 peers treated Ghidra errata as another audit unit. No separate arc3-r2 file is present, leaving the intended fourth unit ambiguous (`CR-3.md:62-63`, `RV-8.md:3,63`).

The required per-claim `audit.md` is absent and EX-9’s report is missing. Despite the useful independent re-derivations, C2 is **UNVERIFIABLE-with-cause** against the frozen deliverable.

## C3 — freshness: dispositions recorded by peers, census remains partial

Available C3 reports support the following rulings (`claims/c3/PL-1.md:5-11`, `claims/verdicts/CN-2.md:70-89`):

1. **Faithful retest — STOPPED-with-reason.** MemAvailable cleared 20 GiB in sampled checks, while MemFree did not; the phrase “free RAM” is ambiguous, and no affirmative operator host-cost authorization is evidenced. No retest was launched; this is not a retest result (`claims-frozen.md:60-66`).
2. **R10 deficit — DISCHARGED-BY-PRECEDENT under the specific R5 rule, with caveats.** The frozen roster has 64 unique seats versus 59 current reports; the current missing IDs are `CR1,E1,E17,E28,R7`, with no unrostered reports. The old receipt instead names P1, CR1, E1, E17 and an unspecified fifth; P1 exists. The R5 instruction permits this recorded disposition unless the sweep needs the missing findings (`claims-frozen.md:67-70`). Available findings do not show such a dependency, but the generic counting lesson calls for replacement dispatch on a true shortfall and contains no interruption exception (`corpus/lessons/2026-10-18-wave-dispatch-counting.md:39-51`). Do not cite that lesson as the basis for discharge; reopen if the missing R10 findings prove necessary.
3. **Full C3 census — CARRIED-forward (partial).** R2–R4 each have 60 report files, but the preserved dispatch arrays/denominators needed for a full lane-delivery comparison are absent; `.ufo/waves/arc2-loop1-round10/E19.md:212-217` still has `<fill>` cells (`PL-1.md:50-70`, `CN-2.md:89`).

All 16 expected C3 reports exist, but the frozen `disposition.md` aggregate is absent. The three peer rulings are not a completed full-wave census.

## Overall ruling

**UNVERIFIABLE-with-cause; not closed at the frozen artifact level.** Many individual measurements and corrections reproduce, but the required C1 sweep report, C2 audit, and C3 disposition are all absent. The roster, scope, byte-interpretation, and cross-file Core discrepancies above must remain visible; do not claim full 64-seat convergence or chain completion until the specified aggregates and unresolved scope/rationale issues are addressed.