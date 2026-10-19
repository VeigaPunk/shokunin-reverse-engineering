# CR-6 — verdicts/convergence: independent verification of the three delivered artifacts

Seat **CR-6**, chain **verdicts/convergence** (roster `claims-frozen.md`: `VZ-1..4, CN-1..4,
CR-5..8`), wave arc3-loop1-round6, 2026-10-19. HEAD `c625d5d` (records) / work
`58c3db7`. Scratch `/var/tmp/cr6-r6/` (never `/tmp`; the EDQUOT rule). Writes:
only `claims/verdicts/CR-6.md` + `claims/verdicts/CR-6/`. Custody read-only;
git read-only (`show`/`log`/`ls-tree`/`status` only). Every number below was
re-derived this session from retained bytes, git objects, or live tool runs —
no prior-seat value is quoted as evidence (rule #14). Where a peer reached the
same number independently, that is recorded as reconciliation, not as proof.

## 0. Verdict ledger

| delivered artifact | verdict | one-line basis |
|---|---|---|
| **c1 — PL-4 r10 frontier register** | **VERIFIED**; one residual sentence **CORRECTED** | patch applies to the pristine gate → sha `80027570…`, 713 lines; clean PASS; 6/6 seeded arms reproduce; two structural-edge arms show PL-4 §6.1 overstates what insertions are caught (matches PL-2's independent edge table) |
| **c2 — EX-7 viaIR dispatch entry** | **VERIFIED** (landable as drafted); one wording precision; one Unknown narrowed | all three compile legs recompiled byte-identically; own PUSH-aware walk reproduces the class; 7/7 sealed probe envelopes re-issued with the *same* ids at their paths; command-A projection 85/85 |
| **c3 — SC-3 rule #15** | **REPRODUCED with one CORRECTION** | draft is 1,605 B / 23 lines / sha `763c44b5…`; 14→15 with 15/15 at both revs; its `r4:34` citation mispoints (text is at `:29`); corrected draft (`:34`→`:29`) is sha `6967b1e3…` and still 15/15 |

Cross-chain convergence issues the parent must know:

1. **Two mutually exclusive c1 patches exist.** PL-4's in-place register
   (`80027570…`) is the frozen delivered artifact; RV-3 produced a *different*
   in-place design (self-reported sha `8e420679…`, `RV-3.md:106`) that VZ-4
   audited (`VZ-4.md:108-120`). VZ-4's C1 "REPRODUCED" row (`VZ-4.md:15`)
   therefore certifies RV-3's patch, **not** PL-4's. PL-4's patch has two
   independent verifications: PL-2 (`PL-2.md:1`) and this seat (§1).
2. **VZ-4's C2 row is stale by construction**: it recorded C2 as PENDING
   because EX-7's entry did not exist at its poll (`VZ-4.md:161-221`). The
   entry now exists and is verified here (§2).
3. **SC-3's rule has one bad pointer** (`r4:34` → `:29`); VZ-4 independently
   found the same (`VZ-4.md:17`, `:281`). Fix before landing (§3).
4. **RV-7's F1 is real**: the r3 erratum's internal `:24` pointer is dangling
   (`RV-7.md:131`); verified in §3.3. It is corpus debt, not a defect in
   SC-3's rule.

---

## 1. C1 — PL-4's r10 frontier register

### 1.1 Patch identity and application — VERIFIED

Pristine gate at HEAD: `sha256 d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`,
610 lines. Applied `claims/c1/PL-4/patch-v10-to-r10.diff` to a scratch copy:

```
$ patch c1-census-v10.py < patch-v10-to-r10.diff
patching file c1-census-v10.py
$ sha256sum c1-census-v10.py
8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca  c1-census-v10.py
$ wc -l c1-census-v10.py
713 c1-census-v10.py
```

Matches `PL-4.md:114` (`80027570…`) and the landing recipe `PL-4.md:358`.
The patch applies cleanly, no fuzz, no rejects.

### 1.2 Requirement (a), clean tree — VERIFIED

On the real repo root and on a byte-identical scratch tree (PROVINCE/SKILL/
SCORECARD copied), the patched gate (`r10.py`) reads:

```
FRONTIER register (G21): 14 rows asserted, errors: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)   exit=0
```

### 1.3 Requirement (c), counters and scope — VERIFIED structurally and by JSON

`--json` on the same clean tree, v10 vs r10:

```
shared keys: 17   mismatched: []
r10-only keys: ['frontier_errors', 'frontier_rows']
counts equal: True
current_ok_per_file: {'PROVINCE.md': 17, 'SCORECARD.md': 14, 'SKILL.md': 3}
```

Beyond JSON equality I compared source regions: the `SCOPE = [...]` block is
byte-identical pre/post (22 lines), and `def classify(`, `def scope_of(`,
`def assert_markers(` bodies are byte-identical. So no SCOPE row, no counter
semantic, and no grading function changed. (The `VERDICT:` line is
byte-identical; the G21 line is additive, as the patch text claims.)

### 1.4 Requirement (b), seeded arms — VERIFIED (six trees, two instruments)

I rebuilt the six trees from the real `PROVINCE.md` with independently written
content-asserted edits (not PL-4's `seed.py`), then ran pristine v10 and r10:

| tree | v10 | r10 | r10 declared classes |
|---|---|---|---|
| clean | 0 PASS | 0 PASS | `[]` |
| seeded-forbidden (frozen literal back into `:91-93`) | **0 PASS (blind)** | **1 FAIL** | `['FRONTIER-STALE']` (+ 2 REQUIRED-absent) |
| seeded-forbidden-only (keeps `solc-0.8.37`/`vyper-0.4.3`, adds `untested`) | **0 PASS (blind)** | **1 FAIL** | `['FRONTIER-STALE']` (exactly one error) |
| seeded-required-evm (earning citations stripped) | **0 PASS (blind)** | **1 FAIL** | `['FRONTIER-UNEVALUABLE']` |
| seeded-required-riscv (`r5-01` removed from `:137`) | **0 PASS (blind)** | **1 FAIL** | `['FRONTIER-UNEVALUABLE']` |
| clean-truncated (PROVINCE 161 lines) | **0 PASS (blind)** | **1 FAIL** | `['UNREADABLE','FRONTIER-UNEVALUABLE']` |

Exact lines: `PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested'
(FRONTIER-STALE)`; `PROVINCE.md:135-138 REQUIRED 'r5-01' absent`;
`UNREADABLE: ['PROVINCE.md: 161 lines < declared max 162 (rows beyond EOF)']`.
This reproduces PL-4's §3 table row for row and also reproduces the new
blind-spot instance PL-4 found (v10 PASSes a 161-line PROVINCE).

### 1.5 Residual correction — CORRECTED (behavior unchanged)

PL-4 §6.1 (`PL-4.md:327-333`) says: “Insertions anywhere inside `:73-162` are
caught … inside `:132-162` they shift register spans (REQUIRED-absent —
measured via the seeded arms).” **This is too strong, and was not measured by
the seeded arms.** I built two structural-edge trees:

| edge tree | edit | v10 | r10 | caught by |
|---|---|---|---|---|
| `edge-header` | `## Frontier` → `## Frontier (renamed)` at `:73` | 0 PASS | **0 PASS** | nothing — the header line is in no FRONTIER row |
| `edge-insert-133` | one blank line inserted before `### Round-4 frontier` | 0 PASS | **0 PASS** | nothing — spans shift; anchors stay inside the shifted rows |

PL-2 measured the same edges independently (`PL-2.md:176-177`) and states the
correction in its §5. The register is a **span-assertion** table, not a
line-identity table; a ±1-line insertion whose anchors remain inside the
shifted span is invisible by construction. Requirement (b) — a reintroduced
stale literal — is still met (the FORBIDDEN arm above). The correction is to
the residual sentence, not to the delivered patch behavior. This should be
recorded in the landing receipt as a named residual, not silently absorbed.

### 1.6 C1 peer reconciliation

- **PL-2** (`PL-2.md:1`, “independent verification of PL-4's r10 frontier
  register”): same patch, same clean PASS, same six arms, same edge
  correction. Its two unexercised register entries (`PL-2.md:184`) remain
  UNVERIFIABLE for its seat; my arms cover the same six rows — entries 2-3's
  own literals were not reintroduced by either of us. This does not affect the
  frozen falsifiable (the named seed is entry 6, `:91-93`).
- **RV-3** (`RV-3.md:106`): a different in-place design (`FRONTIER-ANCHOR /
  FRONTIER-UNATTESTED / FRONTIER-STALE`, self-reported sha `8e420679…`).
  VZ-4 round-tripped it (`VZ-4.md:118-120`). Only one in-place r10 can land;
  the frozen deliverable is PL-4's. **Do not apply RV-3's patch after PL-4's.**
- **VZ-4**: its C1 row is an audit of RV-3's patch, not PL-4's (see §0.1).

**C1 verdict: VERIFIED.** The patch closes the Frontier blind spot for the
frozen falsifiable, keeps the clean verdict and all 17 existing JSON keys
intact, and catches the seeded stale literal on the named line. One residual
sentence in the artifact is corrected; two structural edges are named as
residuals.

---

## 2. C2 — EX-7's viaIR dispatcher entry

### 2.1 Before → after under command A — REPRODUCED

Recipe at `SCORECARD.md:88-124`, run verbatim against git objects:

```
c625d5d → {"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
           "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [],
           "revision": "c625d5d", "rule_blocks": 14}
58c3db7 → identical numbers
```

Projection with the entry draft + one README token overlaid (the token appended
to the EVM row, `corpus/README.md:38`):

```
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 85, "mapped": 85, "missing": [],
 "revision": "c625d5d", "rule_blocks": 14}
```

85/85, `missing []`, `dangling []` — the frozen falsifiable's numbers, measured
as a projection (the parent must re-measure after landing; §5).

The Unknown is real and still open at HEAD: `grep -rn -i viair
corpus/knowledge/*.md` returns exactly two hits, both Unknowns lists —
`2026-10-19-arc3-r3-evm-optimizer-shapes.md:33` and
`2026-10-19-arc3-r4-evm-vyper-leg.md:28`. No corpus entry records a viaIR
dispatcher measurement before this draft.

### 2.2 Compile identity — VERIFIED (strongest check)

I recompiled from EX-7's **recorded `input.json` bytes verbatim** with the
wave-1 receipted solc prefix (read-only reuse; `soljson.js` sha256
`221d7a667378…abad4c`, `package.json` `b3a90035…33491` re-hashed equal):

```
solc 0.8.37+commit.f401782d.Emscripten.clang
viair-opt200  runtime 1,517 B 2ec3f557…  creation 1,560 B d85fdde9…  runtime_byte_equal=true creation_byte_equal=true
viair-noopt   runtime 4,144 B 0cc6938c…  creation 4,318 B f1125049…  runtime_byte_equal=true creation_byte_equal=true
std-opt200    runtime 1,921 B c2ceabb1…  creation 1,966 B 4541fd49…  runtime_byte_equal=true creation_byte_equal=true
```

Source `ViaIrVault.sol` sha256 `f5391167…80cbbe`. ABI is byte-identical across
all three legs (`63fcf52f…`, 17 entries = 15 functions + constructor +
`receive`); `method-identifiers.json` is `c32e2ef2…` (15 keys). Every size and
digest in the entry matches. The three legs differ only by pipeline/optimizer,
so the shape delta below is causally attributable to `viaIR`, not to source or
optimizer.

### 2.3 Byte walk — VERIFIED (my own PUSH-aware disassembler)

My walker decodes opcode boundaries (skipping PUSH immediates), not a byte
scan. First-hand measurements:

| measurement | viair-opt200 | viair-noopt | std-opt200 control |
|---|---|---|---|
| guard head (runtime `:0`) | `6080604052 6004 36 10 15 61 0022 57` | same with `61 001d` | `6080604052 6004 36 10 61 00e7 57` — **no `ISZERO`** |
| EQ legs (`DUP1 PUSH4 sel EQ PUSH2 dst JUMPI`) | **14** | **14** | **15** |
| GT legs (`DUP1 PUSH4 sel GT PUSH2 dst JUMPI`) | 0 | 0 | **3** at PUSH4 pcs **19 / 30 / 137** |
| EQ PUSH4 pcs | 41…184 | 41…184 | 41…218 |
| EQ stride | **11 B** (all 13 gaps) | **11 B** | `[11,15,26]` (binary tree) |
| selectors ascending | **yes** | **yes** | no (tree order) |
| distinct EQ selectors | 14 | 14 | 15; 3 appear twice as GT pivot + EQ leaf |
| final leg in another opcode class | **`PUSH4 ee02438e SUB PUSH2 000e JUMPI`** at push4 pc 194 | same at 194 | none |
| EQ dsts all JUMPDEST | **yes** (253…982) | **yes** (208…273) | yes |
| probe offsets = computed handler entry | **15/15** | **15/15** | **15/15** |
| non-JUMPDEST entries | `mark` offset **204 = push4_pc+10**, byte `0x34` | **204**, byte `0x61` | none |
| PUSH4 sites (opcode-boundary) | **19 sites / 18 distinct** | **17 / 16** | **22 / 19** |

The viaIR compare tree is exactly the fourth class the entry claims: sorted
linear EQ chain, 11-byte stride, terminating `SUB` leg whose dst `0x000e` is
the guard block's JUMPDEST (byte 14) and whose fall-through is the `mark`
handler (`CALLVALUE; PUSH2 0x00f9 JUMPI` at 204 in opt200; `PUSH2 0x05a9 JUMP`
at 204 in noopt). The control compiles the r3 GT/EQ binary-search class from
the same source and optimizer, so `viaIR` — not the source — selects the class.

False-positive census matches the entry exactly: opt200's 19 PUSH4 sites are
the 15 selectors + `4e487b71` ×2 + `0c2eae8d` + `3c3332b9`; noopt's 17 are the
15 selectors + `4e487b71` ×2; the control's 22 are 18 selector sites (15
distinct) + `3c3332b9` + `4e487b71` + `0c2eae8d` + CBOR constant `43000825`.
None reported as functions.

CBOR trailer: 51 B ending `…64 736f6c63 43 000825`, `ipfs` present, `solc`
= 0.8.37. The runtime is byte-embedded in the creation blob at **+43** of
1,560 B. Both are the entry's claims, reproduced.

### 2.4 Probe envelopes — VERIFIED, including same-path id determinism

The artifact retains seven sealed envelopes. Re-running REA 6.4.0/6.7.0 **at
the original absolute paths** (`/var/tmp/ex07-r6/out/…`) re-issued the *same
evidence ids*, which is the strongest available authenticity check:

| leg | path | sealed id (artifact) | my rerun | functions |
|---|---|---|---|---|
| viair-opt200 hex @6.4.0 | `out/viair-opt200/runtime.hex` | `ev_409e0442…` | `ev_409e0442…` ✓ | 15/15, `dispatch:"abi"` |
| viair-opt200 raw @6.4.0 | `out/viair-opt200/runtime.bin` | `ev_c55a152c…` | `ev_c55a152c…` ✓ | 15/15 |
| viair-opt200 hex @6.7.0 | same hex | `ev_285d13d0…` | `ev_285d13d0…` ✓ | 15/15 |
| viair-noopt hex @6.4.0 | `out/viair-noopt/runtime.hex` | `ev_8ddef761…` | `ev_8ddef761…` ✓ | 15/15 |
| std-opt200 hex @6.4.0 | `out/std-opt200/runtime.hex` | `ev_3b390132…` | `ev_3b390132…` ✓ | 15/15 |
| TRAP: raw-on-hex @6.4.0 | `out/viair-opt200/runtime.hex`, encoding raw | `ev_2e7e40ba…` | `ev_2e7e40ba…` ✓ | **0**, decoded sha = hex-file sha `19838d66…` |
| creation hex @6.4.0 | `out/viair-opt200/creation.hex` | `ev_ff7ee757…` | `ev_ff7ee757…` ✓ | **0**, decoded sha = creation sha `d85fdde9…` |

All real legs decode to the runtime file's own sha256 (`2ec3f557…`, `0cc6938c…`,
`c2ceabb1…`). A run from a **different** path minted a different id
(`ev_71da9d37…` for the same bytes), confirming the path-sensitive id domain
the entry states in its Unknowns; comparison must be by decoded sha, as the
entry says.

### 2.5 Selector identity and mutability — VERIFIED, one wording precision

- My recompiled `methodIdentifiers` is set-equal to the pre-compile planted
  K=15 (`evidence/planted-K.json`), and the pre-fix set
  (`planted-K.preact.json`) is equal too.
- Zero collisions with the 9 standard ERC-20 selectors (checked explicitly).
- Mutability: 14/15 probe inferences agree with the compiled ABI; the one
  divergence is `scale(uint256,uint256)` ABI `pure` → probe `view` — the r3
  pure/view class. **Precision note:** the probe reports `payable` for exactly
  one function, `deposit()`, which the ABI also declares `payable`; there are
  **zero spurious payable reads** (no non-payable function read as payable).
  The entry's phrase “zero payable-reads” (`entry:27`) is correct only in the
  spurious sense; “zero false-payable reads” would be exact. Not a factual
  defect in the finding.

### 2.6 Cross-carrier corroboration and one narrowed Unknown

EX-6's retained evidence (evidence-only seat; no `.md`) is a **fallback-bearing**
viaIR carrier (`src/ViaIRVault.sol:31` receive, `:37` fallback). Walking its
bytes myself:

- `viair-opt200` runtime 1,127 B: **11 EQ legs + 1 SUB leg** (`f43cc773`, dst
  14), stride **11**, selectors sorted; selector decode deferred (first
  `5f3560e01c` at byte 176, not in the prologue).
- `viair-nopt` runtime 3,039 B: **11 EQ + 1 SUB** at push4 pc 161, dst 14,
  stride 11, sorted; no `5f3560e01c` at all.

So the fourth class reproduces on a second carrier that *does* have a
`fallback()` — the SUB-terminated sorted linear chain is not an artifact of
EX-7's carrier. This narrows the entry's Unknown at `entry:30` (“viaIR carriers
with `fallback()` … unmeasured”): the static shape **is** measured on retained
peer bytes; what remains unmeasured is runtime execution/behavior of the
fall-through interaction. The entry's scope sentence (“solc 0.8.37 with this
carrier family”) still stands, and no landing change is required; the parent
may refine that Unknown line if desired.

### 2.7 C2 verdict

**VERIFIED.** The entry's numbers, byte claims, probe results, envelope ids,
compile identity, projection, and scope are all first-hand reproducible. The
only adjustments are (i) the “zero payable-reads” wording precision and (ii)
the fallback Unknown narrowing above; neither blocks landing.

---

## 3. C3 — SC-3's rule #15

### 3.1 Baseline and draft identity — REPRODUCED

Command A at both revs: `rule_blocks 14`, `citation_resolved_rules 14`,
`knowledge_files 84`, `mapped 84`, `missing []`, `dangling []`.

The draft extracted verbatim from `SC-3.md` §4 is **1,605 B, 23 lines,
sha256 `763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1`** —
exactly the artifact's self-identity. It contains exactly one `- **` rule
start and 8 command-A-pattern citations.

Appending it to the craft section from `git show <rev>:SKILL.md` and running
command A's own split+resolution logic:

| rev | before | after |
|---|---|---|
| `c625d5d` | 14 blocks / 14 resolved | **15 / 15** |
| `58c3db7` | 14 / 14 | **15 / 15** |

The last block carries 8 references, all in-bounds at both revs. The frozen
falsifiable (“rule_blocks 14 → 15 with the new rule's citations resolving”)
is **REPRODUCED**.

### 3.2 The one mis-citation — CORRECTED

The rule's last sentence (`SC-3.md:105`, citation list `:143`) cites
`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:34` for the limitation
“empty results do not prove absence of dispatch”. First-hand:

```
$ sed -n '29p;34p' corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md
:29  … upstream-inference caveat … "empty results do not prove absence of dispatch" …
:34  ## Erratum (arc3-loop1-round5 correctness sweep, append-only)
```

`:34` is the erratum **header**, not the limitation text. Command A still
resolves it (34 ≤ 63 lines), so the depth score is unaffected — but the landed
rule would mispoint. Corrected draft (single `:34`→`:29` substitution):

```
bytes 1605 · lines 23 · sha256 6967b1e3e7fbdb43492e191426399c0311ab3bf85ee307f1a181a3edd235511e
simulation c625d5d → rule_blocks 15, resolved 15 (8 refs in the last block, all valid)
```

This matches VZ-4's independent correction (`VZ-4.md:17`, `:281`). **Land the
corrected bytes, not `SC-3.md` §4 verbatim.**

### 3.3 The rule's core instance — VERIFIED first-hand

CarrierV retained bytes (r4 EX-04, read-only):

```
creation.hex → 1,637 B sha256 3c6673966d821d9d3366283ab2501c4e32167798ae89d92a21143f560994a226
runtime.bin  → 1,562 B sha256 57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
runtime embedded in creation at +20, 55 trailing bytes
live probe creation.hex @6.4.0 → exit 0, functions 0, bytecode.kind "unknown",
  decoded sha = 3c667396…, evidence id ev_53732d0f8c6…
```

So the rule's two halves — probe says 0 functions, bytes contain the full
runtime dispatch table — reproduce on the same blob. The r4/r5 erratum numbers
(`r4:39-46`: +20 / 1,637 / 1,562, 55 trailing) are byte-exact.

### 3.4 RV-7's F1 (corpus pointer) — VERIFIED as a separate debt

`RV-7.md:131` says the r3 erratum's `:24` pointer is dangling. First-hand:

```
corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:41
  - **`:24` "Creation blobs carry no runtime dispatch table" — corrected.** …
corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:24
  - **Observation (RESULT — Rv2TokenOpt @EX-07):** … (not the quoted sentence)
```

The quoted sentence exists in `2026-10-19-arc3-r1-evm-real-solc.md:24` and in
the r3 file only inside the erratum itself. SC-3's rule cites `r3:41-51` (the
erratum), not `r3:24`, so it is unaffected. Queue the r3 pointer as append-only
corpus debt; it is outside this wave's write scope.

### 3.5 Alternative draft (RV-7) — usable, but not both

RV-7's competing draft (`RV-7.md` §3) is **1,565 B, 23 lines, sha256
`ccbc5cdbbefc86081393cd4d60ef9c85606c3dd1c98ed76d63520da1da0b67e7`**; my
simulation gives 15 blocks / 15 resolved, 6 refs in the last block, all valid.
It avoids the `r4:34` mis-citation. Either SC-3-corrected or RV-7 can land;
**landing both would create two rule-#15 blocks and move `rule_blocks` to 16**
(a depth-axis overclaim). Recommendation: SC-3-corrected (the frozen delivered
artifact) with the `:34`→`:29` fix; RV-7's draft is the fallback if the parent
prefers its wording.

**C3 verdict: REPRODUCED with one CORRECTION.** Content is right and the
falsifiable is met; one citation must be fixed before landing.

---

## 4. Peer reconciliation

| peer artifact | what it is | reconciliation |
|---|---|---|
| `c1/PL-2.md` | **verifier** of PL-4's patch (`PL-2.md:1`) | Same patch, same clean PASS, same six arms. Its edge table (`:176-177`) independently measured the two structural edges I reproduced; its §5 correction to PL-4 §6.1 is confirmed. Its own unexercised register entries 2-3 remain UNVERIFIABLE for it; my arms do not exercise them either. |
| `c1/RV-3.md` | **alternative** c1 patch (`FRONTIER-REGISTER`, sha `8e420679…` at `:106`) | Different class set (`FRONTIER-ANCHOR/UNATTESTED/STALE`). VZ-4 round-tripped it. Cannot coexist with PL-4's in-place edit. Not the frozen deliverable. |
| `c2/EX-6/` | **evidence-only** c2 attempt (no `EX-6.md`) | Not a seat artifact (no claim). Its fallback-bearing viaIR bytes independently corroborate EX-7's fourth class (§2.6) and expose EX-7's “fallback unmeasured” wording as too broad. |
| `c3/RV-7.md` | **alternative** rule-#15 draft + F1 | Its draft passes 15/15; its F1 (r3 `:24` pointer) is real (§3.4). Its draft avoids SC-3's `:34` mispoint. One of the two drafts, not both. |
| `verdicts/VZ-4.md` | convergence verdict | C1 row audits **RV-3's** patch, not PL-4's (`:15`, `:108-120`) — a coverage gap this seat closes. C2 row is PENDING by construction (`:161-221`), now resolved by EX-7. C3 correction (`:17`, `:281`) is independently confirmed. |

---

## 5. Convergence: landing order and expected command A

Nothing was landed by this seat; this is the arithmetic/structural projection
the parent should verify after landing.

1. **c1** — apply PL-4's patch in place, once:
   `patch .ufo/gates/c1-census-v10.py < claims/c1/PL-4/patch-v10-to-r10.diff`
   → expect sha `80027570…`, 713 lines; run the gate → PASS, `14 rows
   asserted, errors: []`. **Do not also apply RV-3's patch.**
2. **c2** — copy `claims/c2/EX-7/entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md`
   to `corpus/knowledge/` and append the token to `corpus/README.md:38` in the
   **same commit** (command A couples them; a token without the file is
   `dangling`, a file without the token is `missing`).
3. **c3** — append the corrected rule (sha `6967b1e3…`) as the 15th and last
   bullet of the `## Queue-drain craft` section. Do not append RV-7's draft in
   addition.

Expected command A after all three (projection, not post-landing measurement):

```json
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 85, "mapped": 85, "missing": [],
 "rule_blocks": 15}
```

Named residuals to record in the landing receipt: (a) PL-4's register is
span-based — header renames and ±1-line insertions whose anchors stay inside
the shifted span pass silently (measured; PL-4 §6.1 corrected); (b) the r3
erratum's dangling `:24` pointer (RV-7 F1) remains corpus debt; (c) EX-7's
fallback-bearing viaIR Unknown is narrower than “unmeasured” — static shape
observed on EX-6's bytes, runtime interaction still open.

---

## 6. Evidence inventory (this seat)

Under `claims/verdicts/CR-6/` (read-back verified):

| file | shows |
|---|---|
| `byte-walk.json` | my PUSH-aware walk of all three EX-7 legs: guards, 14/14/15 EQ legs, 3 GT legs, stride 11, sortedness, SUB legs, dst/JUMPDEST checks, 15/15 offsets, PUSH4 censuses, CBOR, +43 embedding; plus EX-6's 11 EQ + 1 SUB corroboration |
| `recompile.txt` | byte-identical recompile of all three legs from the recorded `input.json` (solc 0.8.37) |
| `same-*.json` (7) | REA reruns at EX-7's original absolute paths — same evidence ids, 15/15 real legs, 0-function traps |
| `rea-*.json` (6) | REA reruns at CR-6's own paths — 15/15 all real legs; `rea-opt200-different-path.json` is the same bytes at a different path minting `ev_71da9d37…` (path-sensitive id) |
| `cmdA-before-{58c3db7,c625d5d}.json`, `cmdA-projected-after.json` | command A 84/84 → 85/85 projection |
| `v10-*.out`, `r10-*.out` | six seeded arms + two edge arms, both instruments, exit codes and declared classes |
| `v10-clean.json`, `r10-clean.json` | 17 shared JSON keys, 0 mismatches; two additive keys |
| `rule15.txt`, `rule15-fixed.txt`, `rule15-rv7.txt` | SC-3 draft, the `:34`→`:29` corrected draft, and RV-7's alternative draft |
| `carrierv-creation.json` | live CarrierV creation probe: 0 functions, id `ev_53732d0f8c6…` |
| `checks.txt` | one-line transcript of every numeric verification in this artifact (C1/C2/C3), with command lines |

Key scratch scripts (retained at `/var/tmp/cr6-r6/` for this session):
`walk.py` (PUSH-aware walker), `compile_recheck.js` (independent compile).
No tracked file was modified; `git status --porcelain` shows only the
pre-existing `arc2-loop1-round10/C3.md` modification and the untracked
`arc3-loop1-round6/` wave tree.

## 7. Honest limits

- Static analysis only: no EVM execution of any carrier; mutability/arguments
  remain upstream inferences, as the entry itself states.
- One solc version (0.8.37); the 6.7.0 leg was re-run only for the hex/raw
  forms EX-7 recorded; creation/6.7.0 combinations not re-run.
- I did not re-apply RV-3's patch; its round-trip is VZ-4's measurement, cited
  as such. I did verify its design differs and cannot coexist with PL-4's.
- PL-4 edge correction covers two edits; PL-2 measured a wider edge set
  (including insert-134/150, insert-74, delete-line, empty-bullet), which I
  read but did not all re-run.
- Command A “after” is a projection over a scratch overlay, not a measurement
  on a landed tree; the parent must re-measure.
- The c2 entry's fallback Unknown narrowing rests on EX-6's evidence-only
  bytes, not on a claim written by that seat; it is corroboration, not an
  independent probe run.
