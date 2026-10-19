# RV-2 grade — drafted c1 knowledge entry (arc3-loop1-round4, Vyper leg)

Seat RV-2 · chain c1 · role reviewer · 2026-10-19. Task (seat line): grade the
drafted entry against `corpus/QUALITY.md` + the r1/r3 entries (incl. the
honest-stop/partial forms if triggered); list required fixes.

**Graded artifact:** `.ufo/waves/arc3-loop1-round4/claims/c1/records-drafts/knowledge-entry-draft.md`
21,166 B / 87 lines / sha256 `df9582ac8b253e611eba194ef9b466325d23ebb9a5b5270d64a577dbc37ef094`
(mtime 2026-10-19T14:10 local). Method pre-registered before the draft landed in
`prereg-verification-plan.md` (this dir). Every number below re-derived first-hand.

**Graded text:** the literal block between the BEGIN/END markers, extracted
first-hand — **18,166 B / 32 lines / sha256 `da42d9a23eaea87104ad71c7beacf0465a04f27482dd063d625b8e54a7161ebc`**
(scratch copy `/var/tmp/rv2-r4/literal.md`). This matches SC-1's own
`README-identities.txt` row exactly.

**VERDICT: ACCEPT-WITH-FIXES.** All hard gates re-derive PASS end-to-end; the
round's core measurements (K/K on five Vyper carriers, the third dispatcher
shape, the offset-semantics reversal) reproduce from my own probe legs and my
own byte census. Three must-fixes remain (F1 citation, F2 citation,
F3 provenance wording) plus two advisories. **None changes a measured result.**

## 1. Hard gates (all first-hand)

| gate | result | evidence |
|---|---|---|
| stem == map token | PASS | stem `2026-10-19-arc3-r4-evm-vyper-leg` appears in the entry's header line and in `records-drafts/map-token-patch.md` PRIMARY (7 occurrences in the patch file); command A reads `dangling []` in rehearsal |
| command A **before** | PASS | recipe A at HEAD `015e1bab` from real Git objects: `{"knowledge_files":83,"mapped":83,"missing":[],"dangling":[],"citation_resolved_rules":14,"rule_blocks":14,"coverage_score":10.0,"depth_score":10.0}` — `evidence/commandA-before.txt` |
| command A **after** (literal + PRIMARY token, scratch tree) | PASS | **84/84**, `missing []`, `dangling []`, rules 14/14, 10.0/10.0 — my own rehearsal, `evidence/commandA-rehearsal.txt` |
| README line-neutral | PASS | 190 → 190 lines, exactly `:38` differs; after-sha `1cd052605e9d27f38e8c9b9b164fa64d0482b61d4acf0a2b80223cb4cec29d1e` ≡ the draft's claimed value |
| prior-83 byte-identical | PASS | `evidence/prior-83.sha256` set: 83/83 identical, 0 modified, 0 removed; added = `2026-10-19-arc3-r4-evm-vyper-leg.md` only |
| entry first line is the staging comment | PASS | line 1 is the `<!-- corpus entry — … -->` form, matching the r1/r3 precedent |
| K/K recovered, zero extras | PASS | my own three CarrierV legs 15/15 zero missing/extra `dispatch:"abi"`; my oracle (js-sha3 over the compiled ABI) set-equal to the planted set and to vyper's own `method_identifiers`; PL-1's EX03/CarrierW/Smoke legs re-verified against my oracle: 22/22, 9/9, 4/4 set-equal |
| decoded `bytecode.sha256` ≡ carrier bytes | PASS | every cited leg's decoded digest equals the sha256 I compute over the carrier file (`57d6fd0a…`, `54b14e30…`, `1846469b…`, `67d1d88f…`, `415e6b1b…`) |
| recheck line reproduces | PASS | verbatim re-run of the entry's `recheck:` command: exit 0, 15 functions, `dispatch:"abi"` ×15, decoded `57d6fd0a…`, id `ev_d1792f57…` — envelope sha256 `68415a3d…` |
| cited `ev_` ids resolve | PASS | all 19 quoted ids resolve to real envelopes in the tree (`evidence/ids-resolve.txt`) |
| citations resolve | **FAIL (F1, F2)** | see §2 |
| label discipline | PASS | Observation ×8 / Inference / Unknowns / Limitations / Scope; zero `grep -c`; no `held`/`works` verb in the literal; QUALITY 11 honored (parsed-and-empty vs excluded stated) |
| identity discipline (rule #14) | PASS | the draft claims no hash of itself; SC-1's `README-identities.txt` rows re-derive exactly (draft 21,166 B `df9582ac…`; literal 18,166 B `da42d9a2…`) |

## 2. Required fixes

**F1 (citation, must-fix — QUALITY 1).** The `source:` line cites
`` `.ufo/waves/arc3-loop1-round4/claims/c1/SC-1/evidence/` `` containing
`c1-inventory.txt`; the file is **not** there. Measured: `SC-1/evidence/` holds
six files (five envelopes + `command-A-before.json`); `c1-inventory.txt` sits at
`SC-1/c1-inventory.txt`. Fix: move the clause out of the `evidence/` list, or
cite `SC-1/c1-inventory.txt` directly.

**F2 (citation, must-fix — QUALITY 1).** The `source:` line's EX-09 clause
writes `` `probe/vy-{runtime,creation}-{hex,raw,0xhex}-{6.4.0,6.7.0}.json` ``,
which expands to 12 names of which **two do not exist**:
`vy-runtime-0xhex-6.7.0.json` and `vy-creation-0xhex-6.7.0.json`. Measured:
EX-09's probe dir has the `0xhex` legs at **6.4.0 only**; the 6.7.0 set is
hex/raw only. The entry's own observation line (correctly) cites the `0xhex`
leg as `ev_d91e5f6a…` @6.4.0 — so the body is right and the source line
over-claims. Fix: write the actual set, e.g.
`probe/vy-{runtime,creation}-{hex,raw}-{6.4.0,6.7.0}.json` + the two
`vy-*-0xhex-6.4.0.json` files named separately.

**F3 (provenance wording, must-fix — QUALITY 5/6, the r3 "costume" class).**
The source line describes `SC-1/evidence/` as "this entry's scribe's own five
probe envelopes". Measured first-hand: SC-1's five staged envelopes are
**byte-identical** to the RV-2 / VZ-1 / EX-06 legs (same sha256, e.g.
`68415a3d…` for the 6.4.0 hex leg), and SC-1's scratch dir `/var/tmp/sc1-r4/`
holds its own runs at 11:06:25–11:07:05 (before my 11:06:46 staging and before
EX-06's 11:09). A fresh re-run by me at grade time reproduced the same sha256 —
so the byte-identity is **verbatim determinism of the tool, not copying**, and
SC-1's "run first-hand" statement in `seats/SC-1.md` is **true**. The defect is
only in the entry's wording: "own" reads as *independent corroboration* when the
envelopes are by construction identical to the other seats' legs. Fix: say
"this seat's own runs (verbatim-deterministic; identical bytes to RV-2/VZ-1/EX-06
legs on the same paths)" — the claim is unaffected.

## 3. corpus/QUALITY.md criteria (15 admission rows)

Rows 1–14 PASS with the evidence in §1 (row 1 gated by F1/F2 — the *defects* are
two non-existent names among ~150 correct ones). Row 15:

| # | criterion | verdict | note |
|---|---|---|---|
| 1 | resolvable source | PASS-with-fix | F1/F2; 136+ cited names resolve, 2 do not |
| 2 | falsifiable, or marked opinion | PASS | Inference row present; Unknowns enumerated |
| 3 | domain-specific | PASS | EVMole/vyper/selector-level throughout |
| 4 | absolute path + stable identity | PASS | every carrier carries path + sha256 + size |
| 5 | observation/inference/unknown labels | PASS | 8/1/1 + Limitations + Scope |
| 6 | exact reproducing call | PASS | `recheck:` carries tool, path, encoding, `--format json`, expected payload |
| 7 | names what was NOT examined | PASS | Unknowns + Limitations + explicit "Only the carriers and pins named above were probed" |
| 8 | pins tool/provider versions | PASS | `rea-agents@6.4.0`/`6.7.0`, `evmole@0.9.3`, vyper `0.4.3+commit.bff19ea2`, wheel sha256 |
| 9 | runtime claims need runtime provenance | PASS | "no runtime execution, chain/RPC lookup, or network request" |
| 10 | held/works only for verbs run this round | PASS | RESULT-class, no availability→holding claim |
| 11 | parsed-and-empty vs excluded | PASS | creation legs explicitly "parsed-and-empty (exit 0, 0 functions)" |
| 12 | synthesized carriers retain bytes/recipe | PASS | "Byte-exactness is claimed for these pinned bytes only" + source sha256s |
| 13 | counts via `grep -o … | wc -l` | PASS | no `grep -c` in the literal; counts are byte-level/derived |
| 14 | evidence-id identity states full domain | PASS | family-scoped, formula-free, "compare by decoded `normalized_result.bytecode.sha256`" (no `subject.digest` costume — the r3 RV-3 R5a fix is honored) |
| 15 | id domain per verb family **with its corpus citation** | **FAIL (F4)** | the id-domain observation states path-sensitivity but cites **no corpus file**; the r1 entry cites `corpus/QUALITY.md:24-25` and the r3 entry cites the r1 entry. Fix: add the `corpus/QUALITY.md:24-25` + r3-entry pointer, or drop the sentence's normative weight. |

Weak-signal rows (6): none present — no pseudocode-as-behavior, no unqualified
negative claim, no floating target, no docs-sourced capability claim, no static
source for dynamic behavior, no "tool is broken" without the spawn wrapper.

## 4. Attacks / refutations attempted

1. **K/K oracle-independence attack.** I did not trust any planted file: the
   selector sets were re-derived from the compiled ABIs with js-sha3 (r1
   receipted prefix). My oracle == EX-04 planted == vyper `method_identifiers`
   (15/15 after zfill-8 normalization). EX03/CarrierW/Smoke legs re-verified
   against my own oracle: 22/22, 9/9, 4/4, zero missing/extra. **Verdict: PASS.**
2. **Offset-semantics attack (the round's sharpest claim).** Re-derived by
   disassembly: the compare node is `PUSH4 sel; DUP2; XOR; PUSH2 next; JUMPI`
   (11 B), so the reported offset is the match **fall-through**, and
   `byte[offset-12]` is the compare-site JUMPDEST carrying that function's own
   selector — measured **15/15** on CarrierV. `0/15` offsets land on `0x5b`.
   Second carrier (Ex09Vault) `0/7`; PL-1's `verify.txt` independently reports
   0/15, 0/9, 0/22. **Verdict: the entry's line 46 claim is CONFIRMED**, and the
   r1/r3 "offsets are JUMPDESTs" reading is correctly scoped to solc carriers.
3. **Third-dispatcher-shape attack.** Prologue decode reproduced: `selector % 13`
   → 13-entry uint16 table at `0x600` → all 13 entries `0x5b`; `0x5e7` ×3
   sentinel at buckets 1/7/11; 15 XOR compare sites. My independent computation
   agrees byte-for-byte. **Verdict: PASS.** (Note: my `% 13` bucket census finds
   **4 colliding buckets / 5 extra selectors**, which is what "4 collisions"
   means; wording is acceptable.)
4. **Zero-false-positive attack.** My own byte census: 17 distinct PUSH4
   immediates = the 15 selectors + `08c379a0` (6 sites) + `69656e74` (1 site);
   neither was reported. `__default__()`'s `89402a72` occurs in **neither**
   CarrierV nor StewardToken bytes (0 occurrences) — the phantom claim is
   CONFIRMED. **Verdict: PASS.**
5. **Mutability-delta attack.** Re-derived against the compiled ABI for all 15
   CarrierV functions: **7 agree, 8 read `payable`** (5 view + 2 nonpayable +
   1 pure), exactly the draft's numbers; `inferred_arguments` reads `uint256`
   for all three `address` params (dropping `address`). Ex09Vault: 5 agree,
   2 payable-reads (draft says 2 of 7). **Verdict: PASS**, and the direction is
   uniform — no function is misassigned.
6. **Cited-id resolution attack.** All 19 quoted `ev_` prefixes resolve to real
   envelopes; the five Ex09Vault ids match their claimed pins/encodings.
   **Verdict: PASS.**
7. **Trap-class attack.** raw-over-hextext leg reproduces: exit 0, 0 functions,
   decoded sha == the hex *text* file's own sha `e0b1021c…`. Creation legs on
   both carriers × two pins × three encodings are uniformly 0 functions at exit
   0. **Verdict: PASS** (parsed-and-empty, correctly labeled).
8. **Id-domain attack.** EX-10's `var-*` legs are **cwd/TMPDIR variants at one
   path** (all five share id `ev_45849c8b…`), so they show same-path
   re-derivation, not path-sensitivity; the path-sensitivity evidence is EX-10's
   `b2-altpath-copy` (`ev_4899d147…` vs repo `ev_45849c8b…`), `ino-a`/`ino-b`
   (`ev_ed1452cc…` vs `ev_4364a3bf…`, same inode) and EX-07's D1/D2/D7. The
   entry's sentence lists the `var-*` legs first, which reads as if they carried
   the path-sensitivity — they do not. **Verdict: the claim HOLDS on the other
   legs; see A1 advisory.**
9. **Prior-entries recheck attack.** Both prior entries' recheck lines re-run
   clean at this HEAD: r1 `ev_45849c8b…` (5/5, `c1081a56…`), r3 `ev_d409bd50…`
   (13/13, `b24a0115…`). So the new entry does not invalidate them.
   **Verdict: PASS.**
10. **Ledger-hash spot check.** The ledger cites `EX-02/custody-stat-readonly.txt`
    as `f9ae3dbc…`; the file now hashes `67b1014e…` (2091 B, mtime 11:09:50).
    The entry itself cites the file **without** a hash, so the entry is clean;
    recorded for the parent (A2).

## 5. Advisories (not must-fix)

- **A1.** Line 26's id-domain sentence: reorder so the path-sensitivity legs
  (EX-10 `b2-altpath-copy`/`ino-*`, EX-07 D-series) lead, and describe `var-*`
  as the same-path re-derivation control. One clause; no measurement changes.
- **A2.** The chain ledger's `f9ae3dbc…` pin for `EX-02/custody-stat-readonly.txt`
  is stale (file re-written at 11:09:50; now `67b1014e…`). Ledger is not a
  landing surface, but the parent should re-derive before citing it.

## 6. Honest-stop / partial forms

**Not triggered, verified.** The claim's three pre-written stops were (a) venv
infeasible, (b) typed refusal, (c) partial recovery. Measured: the install
succeeded (wheel `3b967172…` 403,104 B, `bin/vyper 615f792c…`, python
`d78f9cf7…` — all re-derived); every Vyper **runtime** leg recovered K/K; the
only zero-function results are creation-code legs, which the entry labels
parsed-and-empty. The draft's success form is therefore the correct branch, and
its `map-token-patch.md` carries the honest-stop variant unused. **Verdict:
correctly NOT triggered.**

## 7. Before → after measurement for the chain's claim (c1)

| quantity | before (HEAD `015e1bab`) | after (literal + PRIMARY token, scratch tree) |
|---|---|---|
| knowledge files | 83 | **84** |
| mapped | 83 | **84** |
| missing / dangling | [] / [] | **[] / []** |
| citation-resolved rules | 14 / 14 | **14 / 14** |
| coverage / depth score | 10.0 / 10.0 | **10.0 / 10.0** |
| README lines | 190 | **190** (one line differs, `:38`) |
| README sha256 | `a451ad16…` | `1cd05260…` |
| prior-83 knowledge files | — | **byte-identical (83/83, 0 modified)** |

Rehearsal caveat (stated, per the r3 precedent): my rehearsal reads a filesystem
tree (`git archive HEAD` + literal + token), not Git objects; the parent must
re-measure at the records commit. An unrun check has not passed.
