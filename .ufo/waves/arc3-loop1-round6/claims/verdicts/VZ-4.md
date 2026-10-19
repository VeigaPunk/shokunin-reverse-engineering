# VZ-4 — arc3-loop1-round6 convergence verdict (final poll 2026-10-19T14:00-03:00)

Seat VZ-4, verdicts/convergence chain, wave arc3-loop1-round6.
Repo state at every direct check: HEAD `c625d5de57e045188b5ce8cd450a57b349f90785`
(records; work `58c3db7`) — `git rev-parse HEAD`, `git log --oneline -3`.
Every number below is my own measurement this session (lane rule #14). Peer
artifacts are used only for comparison and are re-derived before I rule on
them. Scratch: `/var/tmp/vz4-r6c/` (never `/tmp`). Git in the lane repo was
read-only; the only writes are this file and `claims/verdicts/VZ-4/evidence/`.

This file supersedes the 13:14-poll VZ-4 artifact written before PL-4, EX-7 and
the later peers landed; that file is preserved byte-for-byte at
`claims/verdicts/VZ-4/prior-poll-1314.md`. The wave is still live (new peer
directories appeared at 13:59-14:00 during this poll); the reconciliation in §6
is point-in-time.

## Summary

| Claim | Delivered artifact | Ruling |
|---|---|---|
| **C1 operability** — census Frontier blind spot | PL-4 `patch-v10-to-r10.diff` (in-place r10, `FRONTIER[]` register / G21) | **REPRODUCED** on all three frozen sub-claims: round-trip sha `80027570…`, clean tree PASS, seeded stale literal FAILs `FRONTIER-STALE`, every SCOPE row and every shared counter intact. **One CORRECTION**: the patch's residual "insertions anywhere inside :73-162 are caught" is false — a +1-line insertion at `PROVINCE.md:134` reads PASS. |
| **C2 coverage** — one named corpus Unknown | EX-7 `entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md` + EVM map token | **VERIFIED / REPRODUCED**: 84 → 85 measured on a scratch git repo with the entry + token landed (`85/85`, missing `[]`, dangling `[]`); all seven probe envelopes and every byte claim re-derived. **One text CORRECTION before landing**: the CBOR transcript says `73 736f6c63`; the bytes are `64 736f6c63`. |
| **C3 depth** — queue-drain rule #15 | SC-3 §4 draft (parsed-and-empty ≠ byte-absence) | **REPRODUCED**: draft is byte-exact 1,605 B / 23 lines / sha `763c44b5…`; scratch landing reads `rule_blocks=15`, `citation_resolved_rules=15` at both revs. **Two citation-content CORRECTIONS** invisible to command A: `r4:34` → `:29`, and `r1:24` is cited for byte-containment that line denies (`:31` measures it). |
| **Convergence** | C1+C2+C3 after-state | Combined scratch landing: `knowledge_files=85, mapped=85, missing=[], dangling=[], rule_blocks=15, citation_resolved_rules=15, coverage=10.0, depth=10.0`. Nothing is landed in the repo yet. |

Before-state at HEAD, re-measured: `python3 .ufo/gates/c1-census-v10.py --quiet`
→ exit 0, `VERDICT: PASS`, `DECLARED FAIL CLASSES: []`, counts
`PROVINCE.md 162/6`, `SCORECARD.md 1696/9`, `SKILL.md 390/2`, G2 17/14/3.
Command A at both `58c3db7` and `c625d5d` →
`{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "rule_blocks": 14}`.

## C1 — operability: the census Frontier blind spot

### Before-state (frozen facts, re-derived)

- Gate `.ufo/gates/c1-census-v10.py`: sha256
  `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`,
  610 lines (`sha256sum`, `wc -l`).
- `SCOPE` table (`:215-237`): 20 rows, PROVINCE.md only at 8-13, 15-26, 40-43,
  44, 45-62, 64-71, 119-131. I parsed both the pristine and patched gates with
  `ast.literal_eval`: **20 rows, identical lists**; no row reaches 73-93 or
  133-162.
- PROVINCE.md: `## Frontier` at :73 (intro :75-80, bullets :82-93),
  `### Round-4 frontier (post-unlock)` at :133 (bullets :135-162); file is 162
  lines. Confirmed with `nl -ba`.
- Historical stale literal: `git show fbbbd45:PROVINCE.md` lines 91-93 carry
  "real solc/vyper-compiled bytecode untested" inside the undeclared region —
  the R1 debt is historical, not invented.
- v10 blindness: on my own seeded trees it reads `PASS` exit 0 whether the
  frontier bullet is stale, stripped, or the file is truncated. Matrix below.

### PL-4 patch — applied on scratch, byte-exact

`git show HEAD:.ufo/gates/c1-census-v10.py` → pristine (sha above);
`patch pristine < claims/c1/PL-4/patch-v10-to-r10.diff` → exit 0,
**sha256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`,
713 lines** — exactly PL-4's stated identity. Patch file's own sha256:
`3f94355cfe747c10c968c2382004ab1e95792518eba2f03ae99df2f7f16a6513`.
Scratch trees are byte-identical copies of PROVINCE/SKILL/SCORECARD from the
repo; seeds are content-asserted edits (my own script, not PL-4's seeder).

### Seeded-fault matrix (my trees; JSON retained at `VZ-4/evidence/c1-matrix.json`)

| tree | seed | v10 | r10 (PL-4) | r10 (RV-3 prior design) |
|---|---|---|---|---|
| clean | none | PASS | **PASS**, 0 errors | PASS |
| seeded-forbidden | `:92-93` → "real solc/vyper-compiled bytecode untested" | PASS | **FAIL** `['FRONTIER-STALE']`, 3 errors | FAIL `['FRONTIER-STALE','FRONTIER-UNATTESTED']` |
| forbidden-only | keeps `solc-0.8.37`/`vyper-0.4.3`, adds "untested" | PASS | **FAIL** `['FRONTIER-STALE']`, 1 error | FAIL `['FRONTIER-STALE']`, 1 |
| seeded-required | `:92-93` stripped of both earning tokens | PASS | **FAIL** `['FRONTIER-UNEVALUABLE']`, 2 errors | FAIL `['FRONTIER-UNATTESTED']`, 2 |
| truncated | PROVINCE.md 161 lines | PASS | **FAIL** `['UNREADABLE','FRONTIER-UNEVALUABLE']`, 14 | FAIL `['FRONTIER-UNATTESTED']`, 1 |
| short159 | PROVINCE.md 159 lines | PASS | **FAIL** `['UNREADABLE','FRONTIER-UNEVALUABLE']`, 14 | FAIL `['FRONTIER-ANCHOR']`, 1 |
| insert134 | +1 line after `:133` header | n/a | **PASS**, 0 errors (defect) | FAIL `['FRONTIER-ANCHOR']`, 8 |

Representative r10 errors (exact strings):

```
PROVINCE.md:91-93 REQUIRED 'solc-0\.8\.37' absent (G21 frontier register)
PROVINCE.md:91-93 REQUIRED 'vyper-0\.4\.3' absent (G21 frontier register)
PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)
PROVINCE.md: 161 lines < declared max 162 (rows beyond EOF)   [UNREADABLE]
```

### Requirement (c) — counters and SCOPE intact

`--json` at the real repo root, pristine vs patched: **17 shared keys, 0 value
mismatches**; r10-only keys `['frontier_errors','frontier_rows']`; no v10-only
keys. `counts` equal (`PROVINCE 162/6`, `SCORECARD 1696/9`, `SKILL 390/2`);
`current_ok_per_file` equal; `declared_fail_classes` equal (`[]`);
`VERDICT:` text line byte-identical. `SCOPE` AST-identical (20 rows).

### CORRECTIONS to PL-4 (do not affect (a)-(c), do affect honesty of the residual)

1. **Insertion absorption (measured).** PL-4 §6 residual 1 says insertions
   anywhere inside `:73-162` are caught. My `insert134` tree (one line inserted
   after the :133 header, shifting every post-unlock bullet by +1) reads
   **PASS, 0 frontier errors**. The fixed spans absorb ±1-line shifts whenever
   the required tokens remain inside the shifted window. PL-2 and PL-1 report
   the same class independently; I reproduced it first-hand. The gate's
   provenance comment and the landing receipt should state the measured gap,
   or the register should gain per-row anchor assertions.
2. **Class-list collapse (minor).** On `seeded-forbidden` the error list has
   three entries (2 × REQUIRED-absent + 1 × FORBIDDEN) but
   `DECLARED FAIL CLASSES` names only `['FRONTIER-STALE']` — the `if/else`
   reports one family. The run still FAILs and every error is printed; this is
   a reporting limitation, not a blindness. PL-4's own table discloses the
   three errors.

### Competing design (preserved, not landed)

The earlier RV-3 in-place design (now `claims/c1/RV-3/prior-attempt.md`,
sha claim `8e420679…`) adds `FRONTIER_REGISTER` with per-row
anchor-line + anchor-regex + cite, 13 rows (bullets only), and three classes
`FRONTIER-ANCHOR / FRONTIER-UNATTESTED / FRONTIER-STALE`. I extracted its
patch while the earlier RV-3.md was current, applied it to a pristine gate →
**sha256 `8e4206796fec2e16fb6f2c1959f33b63bbcb9643471d42472ac6bc2cba195ebf`,
712 lines**; clean PASS, all seed arms FAIL, and `insert134` FAILs with 8
`FRONTIER-ANCHOR` rows. It is strictly stricter on reflow on my seed set. I did
not reproduce PL-1's different "cross-version restore" seed against it, so I
claim only the measured insertion differential. The current RV-3.md (13:59) is
a verification artifact that recommends PL-4's patch and preserves this design
as prior attempt.

**C1 ruling:** PL-4's patch **satisfies the frozen (a)/(b)/(c)**. Land it if
the wave keeps the designated artifact; correct the residual text (or add
anchors) in the same commit. Do not land PL-4 and the anchored design
together — they rewrite the same table.

## C2 — coverage: the viaIR dispatch-shape Unknown

### Before-state and Unknown openness

Command A recipe verbatim (SCORECARD.md:88-124) at `58c3db7` and `c625d5d` →
84/84, `missing []`, `dangling []`, `rule_blocks 14` (output above).
`grep -rn -i viaIR corpus/knowledge/*.md` → exactly two hits, both Unknowns
lists: `2026-10-19-arc3-r3-evm-optimizer-shapes.md:33` and
`2026-10-19-arc3-r4-evm-vyper-leg.md:28`. No corpus entry measures a viaIR
dispatcher at HEAD.

### Retained evidence re-derived (EX-7 tree)

Sizes and sha256 of `out/*/runtime.bin` and `creation.bin` (my `sha256sum` /
`stat`):

| leg | runtime | sha256 | creation | sha256 |
|---|---|---|---|---|
| viair-opt200 | 1,517 B | `2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a` | 1,560 B | `d85fdde93b1fcb620a8a0dcf16885b7b55113b9ef7860ae5ebdbf5ad5fbd83d5` |
| viair-noopt | 4,144 B | `0cc6938cd768199159cbed74a7e9f5bd4273c583afbf6babca643b0ffdbd29b4` | 4,318 B | `f1125049532f0dd9a71ab0f9963590d7a40913e521c43709400c92b96cc54063` |
| std-opt200 | 1,921 B | `c2ceabb163ad9c1e6d88244c29c5187602eaf4c810029d0018e76eb9643f7e27` | 1,966 B | `4541fd490eb46198e788c148328dfb74e0ae1fd29c961a47c6f3056b823c5d9e` |

All seven probe envelopes re-read (`VZ-4/evidence/c2-probe-summary.json`):
the five real legs (`viair-opt200` hex/raw ×6.4.0 + hex ×6.7.0,
`viair-noopt` hex, `std-opt200` hex) each report **15 functions, 15
`dispatch:"abi"`, zero missing/extra**, and decoded `bytecode.sha256` equal to
the corresponding runtime file's sha. Two traps: raw fed the hex text
(`ev_2e7e40ba…`) → 0 functions, decoded sha `19838d66…` = the hex *file's*
sha; creation probe (`ev_ff7ee757…`) → 0 functions, decoded sha `d85fdde9…`.

### Byte walk (my own decoder, not EX-7's script)

viair-opt200 runtime:

- Head `6080604052 6004361015 610022 57 5b 361561 0018 57 5f80fd ...`
  — `PUSH1 4 CALLDATASIZE LT ISZERO PUSH2 0x0022 JUMPI`; the `ISZERO`
  distinguishes it from the std control's `60043610 6100e7 57`.
- `5f3560e01c` at byte 35; dispatch at 40.
- **14 EQ legs** `DUP1 PUSH4 <sel> EQ PUSH2 <dst> JUMPI`, gaps `[11]×13`
  (strict 11-byte stride), selectors ascending, all dsts `0x5b` (JUMPDEST),
  dsts `982,935,771,723,694,631,572,485,425,374,340,311,272,253`.
- **15th leg** `PUSH4 ee02438e SUB PUSH2 0x000e JUMPI` at push4 pc **194**;
  `SUB` (0x03), not `EQ`; dst 14 is the guard block's JUMPDEST.
- Reported offset for `mark` (`ee02438e`) is **204 = push4_pc+10**;
  `rt[204]=0x34` (CALLVALUE) — not a JUMPDEST, not a PUSH2 target.
- 19 opcode-boundary `PUSH4` sites = the 15 selectors (15 distinct) +
  `4e487b71` ×2 (pc 553,1143), `0c2eae8d` (1094), `3c3332b9` (1261).
- CBOR tail: `...56 fe a2 64 69706673 58 22 <32 B> 64 736f6c63 43 000825 00 33`.
- Creation blob: runtime occurs at **+43**, trailing 0 (1,560 = 43 + 1,517).

viair-noopt: 14 EQ legs, same `[11]` stride, ascending, all dsts JUMPDEST,
dsts `273,268,263,258,253,248,243,238,233,228,223,218,213,208`; same SUB leg
at push4 pc 194/dst 14; reported mark offset 204 = pc+10, `rt[204]=0x61`
(PUSH2). **Precision note:** noopt does **not** contain the `5f3560e01c` head —
its dispatch base is `610027 5f35 610116 56`; the shared "prologue" statement
in the draft (line 22) is true for opt200 and the std control, not for noopt.
The compare-tree/SUB-leg "same shape" claim is true.

std-opt200 control (same source, `viaIR` unset): head
`60043610 6100e7 57`, GT/EQ binary search — GT pivots `6e69f38c` pc 19,
`90ab171e` pc 30, `3f4ba83a` pc 137; 15 EQ legs with gaps `{11,15,26}`, three
selectors duplicated as GT pivot + EQ leaf; 22 PUSH4 sites (18 selector sites +
4 constants). This is the r3 class reproduced under the same source, so the
viaIR class is pipeline-controlled, not source-controlled.

### Selector derivation — independent Keccak

I wrote my own Keccak-f[1600]/Keccak-256 (no peer code) and checked public
vectors: empty string → `c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470`,
`transfer(address,uint256)` → `a9059cbb`. Computing all 15 ABI signatures gives
**15/15 exact matches** to solc's `method-identifiers.json` and to the 14 EQ
selectors + the SUB selector in the runtime. `planted-K.json` carries the same
15 (`K=15`).

### Landing simulation

Scratch git repo at `c625d5d` (`git archive` → init → commit), entry draft
copied to `corpus/knowledge/`, EVM row token appended exactly as EX-7's patch
text specifies. Command A recipe at `HEAD` →

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 85, "mapped": 85, "missing": [],
 "rule_blocks": 14}
```

### Corrections

1. **CBOR transcript (must fix before landing).** Draft line 28 reads
   `73 736f6c63`; the actual bytes are `64 736f6c63` (`0x64` = CBOR text
   string, length 4 = "solc"; `0x73` would be length 3). The surrounding
   `a2 64 69706673 58 22` and `43 000825 00 33` are correct. EX-9 reports the
   same; I re-derived it from the runtime hex.
2. **noopt prologue wording (precision).** See above — "shared `5f3560e01c`"
   should be scoped to opt200/legacy; the viaIR *shape* claim is unaffected.
3. **Custody count (cosmetic).** EX-7.md line 62 says 42 files; the tree
   contains 46 regular files excluding `__pycache__`. No claim depends on it.

**C2 ruling:** EX-7's entry is **VERIFIED** in content and evidence; it lands
84 → 85 as claimed after the one-token CBOR fix. The "fourth dispatcher class"
is verified as a measured compare-tree class distinct from the same-source std
control; distinctness from the recorded r1/r4 classes is corpus-supported but
not re-measured here.

## C3 — depth: rule #15 (parsed-and-empty ≠ byte-absence)

### Baseline and draft identity

`rule_blocks=14`, `citation_resolved_rules=14` at both revs (command A above);
craft section at SKILL.md:81, 14 `- **` blocks ending at :255, `## Config
custody` at :260. `git diff --stat c625d5d 58c3db7 -- SKILL.md` is empty.

SC-3's §4 fenced bytes: **1,605 B, 23 lines, sha256
`763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1`**, one
`- **` marker. Matches SC-3's self-identity exactly.

### Byte census / evidence re-derived

CarrierV retained r4 files: creation 1,637 B
`3c6673966d821d9d3366283ab2501c4e32167798ae89d92a21143f560994a226`;
runtime 1,562 B `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`;
`runtime.hex` decodes byte-identical to `runtime.bin`; runtime occurs in the
creation at **+20**, **55** trailing bytes. Re-read sealed envelope
`EX-06/probe/CarrierV-creation-6.4.0.json`: `ev_53732d0f…`, **0 functions**,
`bytecode.kind "unknown"`, decoded sha `3c667396…` — probe says empty on a blob
that byte-contains the runtime. r1's sealed creation envelope re-read agrees
(0 functions). This is the rule's core instance, proven on one blob.

### Falsifiable — simulated landing

Appended the §4 bytes at the end of the craft section in scratch git copies of
`58c3db7` and `c625d5d`; command A's exact split/resolution logic →

| rev | rule_blocks | citation_resolved_rules | depth_score |
|---|---|---|---|
| `58c3db7` after | **15** | **15** | 10.0 |
| `c625d5d` after | **15** | **15** | 10.0 |

The new block parses as one rule; no stray `- **`; 8 pattern citations resolve
in-bounds.

### Citation-content corrections (command A is bounds-only; it cannot see these)

1. **`r4:34` → `:29`.** The quoted limitation "empty results do not prove
   absence of dispatch" is on
   `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:29` (Limitations
   bullet). `:34` is `## Erratum (arc3-loop1-round5 correctness sweep,
   append-only)`. The quote is absent there. Command A still counts the rule as
   resolved because 34 ≤ 63 (file has 63 lines) — instrument-green,
   content-red. Fix both occurrences (draft §4 and §6 table).
2. **`r1:24` attribution conflation.** The draft says the r1 creation legs
   "probed 0 functions on blobs that byte-contain the full runtime
   (`…r1…:24`)". Line 24 records the 0-function result but asserts the
   opposite of containment ("Creation blobs carry no runtime dispatch
   table"); the containment measurement and the correction are at `:31`
   ("measured false — `Rv2Token.creation.hex` (1,971 B) embeds the runtime and
   its five `EQ;PUSH2;JUMPI` sites"). Minimal fix: attach `:24` to "0
   functions" and let `:31` carry byte-containment. The draft's next sentence
   already cites `:31`, so this is a precision defect, not a false fact.
Other six anchors (r1:31, r3:41-51, r4:39-46, r4:17, r3:27, r4:25) match their
cited content; `QUALITY.md:21` is outside command A's pattern but exists.

### Corrected text candidates (exactly one rule lands)

- SC-4 §6 corrected text (same 23-line shape): I re-measured **1,605 B, sha
  `a1bceb4074328d9d60d14ddf0789b9bcd18ca38936c217d78fc37b1091ec1789`**,
  contains `:29` and the split `r1:24` clause; scratch landing →
  `rule_blocks=15, citation_resolved_rules=15, depth_score=10.0`.
- RV-7 alternative bullet: I re-measured **1,565 B, sha
  `ccbc5cdbbefc86081393cd4d60ef9c85606c3dd1c98ed76d63520da1da0b67e7`**,
  23 lines; scratch landing 15/15 at both revs. It avoids both SC-3 citation
  defects and additionally records measured embedding offsets from the r5
  sweep; I did not re-derive its non-CarrierV embedding numbers, so I do not
  certify those here.
- Do **not** land both: that yields rule #16 duplicating the lesson and breaks
  the frozen 14 → 15 falsifiable.

**C3 ruling:** SC-3's draft **reproduces** the frozen falsifiable and the byte
evidence; land a corrected text (SC-4 `a1bceb40…` recommended because it fixes
both defects at the same 1,605-byte shape, or RV-7 `ccbc5cdb…` if the parent
prefers that wording). Do not land SC-3 `763c44b5…` verbatim.

## Peer reconciliation (point-in-time, 14:00 poll)

Present at this poll — c1: `PL-1`, `PL-2`, `PL-3` (dir), `PL-4`, `EX-3`,
`RV-1`, `RV-3`; c2: `EX-6` (evidence-only), `EX-7`, `EX-9`, `CR-3` (dir);
c3: `EX-13..EX-16`, `RV-5..RV-8`, `SC-1..SC-4`; verdicts: `CN-2`, `CN-4`,
`CR-8`, the prior `VZ-4` poll. Several landed while this seat was measuring;
this verdict is therefore a snapshot, not a final wave census.

Peer findings that intersect my ruling, each independently reproduced by me
before being used:

- PL-1/PL-2: PL-4's insertion residual is fail-open (+1-line seed) — I
  reproduced `insert134` PASS and RV-3-prior FAIL.
- PL-1: PL-4's class list collapses `FRONTIER-UNEVALUABLE` under
  `FRONTIER-STALE` — I reproduced 3 errors / 1 class on my seeded tree.
- EX-9: the entry's CBOR transcript `73` vs `64` — I re-derived `64` from the
  runtime bytes.
- SC-2/SC-4/RV-6/EX-14/EX-16: SC-3 `r4:34`→`:29` and the `r1:24` conflation —
  I re-read both lines and reproduced both defects.
- RV-7: r3's erratum `:24` pointer is dangling at HEAD (line 24 is the
  Rv2TokenOpt RESULT row; the phrase occurs only at the erratum, :41) — I
  spot-checked this at HEAD; it does not affect the landable rule body.
No peer's numeric value is used as evidence in this file without my own
re-derivation.

## Per-item verdict table

| # | Item | Verdict |
|---|---|---|
| 1 | HEAD `c625d5d` / work `58c3db7` | REPRODUCED |
| 2 | Gate sha `d0772ce8…`, 610 lines | REPRODUCED |
| 3 | SCOPE 20 rows; PROVINCE 8-13/15-26/40-43/44/45-62/64-71/119-131 only | VERIFIED (AST) |
| 4 | Frontier 73-93 + 133-162; PROVINCE 162 lines | VERIFIED |
| 5 | v10 PASS on clean tree, counts 162/6, 1696/9, 390/2 | REPRODUCED |
| 6 | v10 blind on stale/stripped/truncated frontier trees | REPRODUCED (5 seeds) |
| 7 | Historical stale literal at `fbbbd45:91-93` | REPRODUCED |
| 8 | PL-4 patch round-trip → sha `80027570…`, 713 lines | REPRODUCED |
| 9 | PL-4 clean tree PASS, 0 frontier errors | REPRODUCED |
| 10 | PL-4 seeded stale literal → FAIL `FRONTIER-STALE` exit 1 | REPRODUCED |
| 11 | PL-4 stripped earning tokens → FAIL `FRONTIER-UNEVALUABLE` | REPRODUCED |
| 12 | PL-4 161/159-line truncation → FAIL `UNREADABLE`+`FRONTIER-UNEVALUABLE` | REPRODUCED |
| 13 | PL-4 17 shared JSON keys equal, 2 additive keys, SCOPE identical | REPRODUCED |
| 14 | PL-4 residual "insertions inside :73-162 are caught" | **CORRECTED** — +1 line at :134 reads PASS |
| 15 | PL-4 declared-class list on multi-class fault | **CORRECTION (minor)** — only `FRONTIER-STALE` named |
| 16 | RV-3 prior anchored design round-trip `8e420679…`, 712 lines; catch arms | REPRODUCED (competing, not landed) |
| 17 | Command A at `58c3db7`/`c625d5d`: 84/84, missing [], dangling [], 14 rules | REPRODUCED |
| 18 | viaIR Unknown open at r3:33 and r4:28; no entry | VERIFIED (exactly 2 hits) |
| 19 | EX-7 runtime/creation sizes + sha256 (3 legs) | REPRODUCED |
| 20 | Seven probe envelopes: five real legs 15/15 abi, two traps 0 | REPRODUCED (static re-read) |
| 21 | viaIR dispatch: guard, 14 EQ/11-byte stride/ascending/JUMPDEST, SUB leg pc 194 dst 14 | REPRODUCED |
| 22 | mark offset 204 = push4_pc+10, not JUMPDEST; noopt chain 208-273 | REPRODUCED |
| 23 | std control GT/EQ binary search, pivots pc 19/30/137 | REPRODUCED |
| 24 | 19 PUSH4 sites, constants 4e487b71×2/0c2eae8d/3c3332b9 | REPRODUCED |
| 25 | Selectors = Keccak(signatures), 15/15 (my own implementation) | REPRODUCED |
| 26 | Creation embeds runtime at +43, 1,560 B | REPRODUCED |
| 27 | Simulated C2 landing: 85/85, missing [], dangling [] | REPRODUCED |
| 28 | EX-7 CBOR transcript `73 736f6c63` | **CORRECTED** — actual `64 736f6c63` |
| 29 | EX-7 noopt "shared 5f3560e01c" wording | **CORRECTION (precision)** — noopt head is `6100275f3561011656` |
| 30 | SC-3 draft 1,605 B / 23 lines / sha `763c44b5…` | REPRODUCED |
| 31 | CarrierV 1,637/1,562 B, +20, 55 trailing; envelope `ev_53732d0f…` 0 fns | REPRODUCED |
| 32 | SC-3 scratch landing 15/15 at both revs | REPRODUCED |
| 33 | SC-3 `r4:34` limitation quote | **CORRECTED** → `:29` |
| 34 | SC-3 `r1:24` byte-containment attribution | **CORRECTED** — containment is `:31` |
| 35 | SC-4 corrected text 1,605 B / sha `a1bceb40…`; landing 15/15 | REPRODUCED |
| 36 | RV-7 alternative 1,565 B / sha `ccbc5cdb…`; landing 15/15 | REPRODUCED (mechanics only) |
| 37 | Combined C2+C3 scratch landing: 85 files, 15 rules, 15 resolved | REPRODUCED |
| 38 | Actual repo after-state | **NOT LANDED** — all after-values are scratch simulations |

## Handoff — landing moves and expected receipts

1. **C1.** Apply `claims/c1/PL-4/patch-v10-to-r10.diff` to
   `.ufo/gates/c1-census-v10.py`; expect sha `80027570…`, 713 lines. In the same
   commit, correct the residual comment/receipt: a +1-line shift at the
   post-unlock boundary can pass silently; the register grades declared spans,
   not novel staleness. Re-run: clean tree PASS/exit 0; seeded stale literal
   FAIL `FRONTIER-STALE`; seeded stripped citations FAIL `FRONTIER-UNEVALUABLE`.
   If a same-round strengthening is desired, add per-row anchors (the archived
   RV-3 design is the tested template) — do not land both patches.
2. **C2.** Fix `73` → `64` in the entry's CBOR sentence; copy
   `EX-7/entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md` →
   `corpus/knowledge/`; append
   `2026-10-19-arc3-r6-viair-dispatch-shape` to the EVM row
   (`corpus/README.md:38`). Command A must read
   `knowledge_files=85, mapped=85, missing=[], dangling=[]`.
3. **C3.** Choose exactly one rule-15 text. Recommended: SC-4's corrected
   `a1bceb40…` (1,605 B, both citation fixes); alternative RV-7's
   `ccbc5cdb…` (1,565 B). Append after SKILL.md:255, before the
   `## Config custody` header. Command A must read `rule_blocks=15,
   citation_resolved_rules=15, depth_score=10.0`.
4. **Combined receipt.** After both landings: `knowledge_files=85, mapped=85,
   missing=[], dangling=[], rule_blocks=15, citation_resolved_rules=15,
   coverage_score=10.0, depth_score=10.0` (measured on my scratch repo before
   either landing). The real repo remains at 84/84 and 14 rules until the
   parent lands.

## What I did NOT do

- Did not modify the gate, PROVINCE.md, SKILL.md, SCORECARD.md, corpus, or any
  tracked file; no git mutation in the lane repo. All patched gates, seeded
  trees, landing simulations and command A runs live under `/var/tmp/vz4-r6c/`
  and are summarized in `claims/verdicts/VZ-4/evidence/`.
- Did not re-run the live `rea-agents` probes; the seven sealed envelopes were
  re-read and every byte claim was re-derived from the retained artifacts. The
  probe summary is therefore static evidence, not a fresh execution.
- Did not fully audit peers outside the three claims (PL-1/PL-3/EX-3/RV-1,
  EX-9, SC-1/SC-2/SC-4, RV-5/RV-6/RV-8); only their findings that intersect my
  ruling were independently reproduced.
- Did not certify RV-7's non-CarrierV embedding numbers or the "fourth class"
  against r1/r4 carriers byte-for-byte; those parts remain corpus-scoped claims
  whose lines I read but did not re-measure.
