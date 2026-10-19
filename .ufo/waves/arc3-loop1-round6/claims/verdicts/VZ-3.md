# VZ-3 — convergence verdict: c1 census patch, c2 viaIR entry, c3 rule #15, and the peer field

Seat VZ-3, verdicts/convergence chain, wave arc3-loop1-round6, 2026-10-19.
Repo HEAD measured this session: `c625d5de57e045188b5ce8cd450a57b349f90785`
(`c625d5d` records; work `58c3db7` two entries below). Every number below is my
own measurement at that HEAD (lane rule #14); peer artifacts are audited objects,
never quoted as evidence. Scratch: `/var/tmp/vz3-r6/` (never `/tmp`; a first
mistake of writing two transient files under `/tmp` failed EDQUOT and was
re-run entirely under `/var/tmp`). Write scope honored: only
`claims/verdicts/VZ-3.md` + `claims/verdicts/VZ-3/`; the gate, PROVINCE.md,
SKILL.md, SCORECARD.md, corpus, `.ufo/gates/` source and git were untouched
(`sha256sum .ufo/gates/c1-census-v10.py` = `d0772ce8…97b5` before and after;
`git status` shows only the pre-existing `M .ufo/waves/arc2-loop1-round10/C3.md`
and the untracked round-6 wave tree).

## 0. Rulings in one screen

| Claim | Delivered artifact | My ruling | Landing move |
|---|---|---|---|
| **C1 operability** | PL-4's in-place r10 frontier register (`patch-v10-to-r10.diff`) | **VERIFIED** — round-trips to `80027570…` (713 lines), clean PASS, frozen seed FAILs `FRONTIER-STALE`, 17/17 shared counters identical. Two residual claims **CORRECTED** (insertion tolerance; class-list exhaustiveness). | **Land PL-4 only.** PL-2 (`2d7ee95b…`) and RV-3 (`8e420679…`) are complete but mutually exclusive with it (measured: all six cross-applies exit 1) and each has a measured catch gap. |
| **C2 coverage** | EX-7's viaIR entry draft + EVM map token | **VERIFIED with three CORRECTIONS** — fresh compile reproduces all three legs byte-exactly; my own walk reproduces the fourth dispatcher class; live probes 15/15. Text fixes: (a) CBOR transcript byte at draft line 28 (`73` → `64`); (b) carrier census is **15 explicit functions + `receive()`** (not "14 + receive = 15"); (c) the SUB terminal is carrier-layout-scoped — the invariant marker is the inverted guard + sorted linear scan, and "legacy = binary search" is K-scoped. | **Land the corrected entry + token.** My overlay reads `85/85, missing [], dangling []`; peer EX-9 measured the same on a scratch clone. Six Vyper optimizer-form drafts also landed: they are alternatives, not additions — landing EX-7 plus any one reads 86/86, overshooting the frozen 84→85. Land **exactly one** C2 entry: EX-7's. |
| **C3 depth** | SC-3's rule #15 draft | **VERIFIED with two CORRECTIONS** — identity `1605 B / 23 lines / 763c44b5…`; `r4:34` is the erratum header (quote is at `:29`); the `r1:24` compound over-attributes byte containment (it lives at `:31`). Corrected texts `6967b1e3…` (minimal) and `a1bceb40…` (both fixes) each land 15/15 at both revs. | **Land exactly one corrected text.** Recommended `a1bceb40…`; accepted fallback `6967b1e3…`. Do not land the verbatim draft, and do not also land RV-7's `ccbc5cdb…` (would read `rule_blocks=16`). |
| **Combined** | all three | **CONVERGENT** | Gate `80027570…` + corpus 85/85 + one rule-15 text → command A `{knowledge_files:85, mapped:85, missing:[], dangling:[], coverage_score:10.0, rule_blocks:15, citation_resolved_rules:15, depth_score:10.0}` at both revs (my simulation). |

## 1. Baseline, re-derived first-hand

```
git rev-parse HEAD                 c625d5de57e045188b5ce8cd450a57b349f90785
git log --oneline -3               c625d5d records / 58c3db7 work / 71668cc records
sha256sum .ufo/gates/c1-census-v10.py
                                   d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5
wc -l                              gate 610 / PROVINCE.md 162 / SKILL.md 390 / SCORECARD.md 1696
```

Command A (SCORECARD.md:88-124 verbatim, immutable Git objects) — both source
commits (`claims/verdicts/VZ-3/commandA-*.json`):

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "58c3db7", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "c625d5d", "rule_blocks": 14}
```

Census SCOPE (gate `:216-236`, read directly): PROVINCE.md rows are exactly
`8-13` CURRENT, `15-26` CURRENT, `40-43` DATED, `44` CURRENT, `45-62` DATED,
`64-71` CURRENT, `119-131` DATED. No row covers the Frontier regions
`73-93`/`133-162`; PROVINCE.md is 162 lines, so the blind spot is structural.
This matches the frozen before-state and the peer audits (EX-2 §1, EX-3 §1,
VZ-4), but is re-derived here from the table itself.

## 2. C1 — PL-4's r10 frontier register, audited

### 2.1 Patch identity and round-trip

```
git show HEAD:.ufo/gates/c1-census-v10.py > pristine.py   # d0772ce8…, 610 L
cp pristine.py r10-pl4.py
patch r10-pl4.py < claims/c1/PL-4/patch-v10-to-r10.diff  # applies clean
sha256sum r10-pl4.py
  8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca
wc -l r10-pl4.py                                         713
cmp r10-pl4.py claims/c1/PL-4/c1-census-v10-r10.py       BYTE-IDENTICAL
```

The `SCOPE` table block is byte-identical between pristine and r10
(sha `220de29f085bf57e…`), and the patch touches no `classify()` or
`assert_markers()` line. `claims/verdicts/VZ-3/c1/patch-identity.txt`.

### 2.2 Requirement (a) — clean tree still PASS

On a byte-copy scratch tree and on the real repo root
(`claims/verdicts/VZ-3/c1/REPO-ROOT-r10.txt`):

```
FRONTIER register (G21): 14 rows asserted, errors: []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      exit 0
```

### 2.3 Requirement (b) — seeded arms (my own trees, `claims/verdicts/VZ-3/c1/`)

| tree | v10 | PL-4 r10 | declared classes |
|---|---|---|---|
| clean | PASS | PASS | `[]` |
| frozen literal at `:91-93` (line-count neutral, `seeded-forbidden`) | PASS (blind) | **FAIL exit 1** | `['FRONTIER-STALE']` (+2 REQUIRED-absent rows) |
| earning tokens kept, `untested` appended (`seeded-forbidden-only`) | PASS | **FAIL exit 1** | `['FRONTIER-STALE']` (exactly one error) |
| EVM earning tokens stripped (`seeded-required-evm`) | PASS | **FAIL exit 1** | `['FRONTIER-UNEVALUABLE']` |
| `r5-01` stripped from `:135-138` | PASS | **FAIL exit 1** | `['FRONTIER-UNEVALUABLE']` |
| PROVINCE truncated to 161 lines | PASS | **FAIL exit 1** | `['UNREADABLE','FRONTIER-UNEVALUABLE']` |
| instrument-visible stale pin at `:88` | FAIL `undeclared=1` | **FAIL `undeclared=1`** | `[]` (pre-existing class preserved) |
| stale bullet appended past `:162` | PASS | PASS | `[]` (PL-4's named past-the-bound residual) |
| two-line deletion at `:143-144` | PASS | **FAIL** | `['UNREADABLE','FRONTIER-UNEVALUABLE']` |

Representative r10 lines:

```
PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)
PROVINCE.md:91-93 REQUIRED 'solc-0\.8\.37' absent (G21 frontier register)
PROVINCE.md:135-138 REQUIRED 'r5-01' absent (G21 frontier register)
UNREADABLE (could-not-evaluate): ['PROVINCE.md: 161 lines < declared max 162 (rows beyond EOF)']
```

### 2.4 Requirement (c) — counters and rows intact

Clean-tree `--json`, v10 vs r10 (`claims/verdicts/VZ-3/c1/clean-*.json`):

```
shared keys: 17   mismatched: []   v10-only: []
r10-only: ['frontier_errors', 'frontier_rows']
counts equal: True
current_ok_per_file: {'PROVINCE.md': 17, 'SCORECARD.md': 14, 'SKILL.md': 3}
frontier_rows: 14   frontier_errors: []
```

### 2.5 Corrections and residuals (measured, non-blocking)

1. **Insertion tolerance (CORRECTED).** PL-4 §6.1 says insertions inside
   `:132-162` shift spans and fail REQUIRED. My arm: insert one new bullet
   carrying the retracted literal after `:138` (file 163 lines) → PL-4 **PASS**,
   RV-3 **FAIL FRONTIER-ANCHOR** (7 errors). A one-line insert slides every
   required anchor inside its row window. Peer EX-2 (§6 C1) and EX-3 (§0/§3)
   measured the same class; my arm is independent. The landing receipt should
   state the residual as positional, not absolute.
2. **Mixed-class report is not exhaustive (CORRECTED, cosmetic).** On
   `seeded-forbidden` the run reports three errors (2 REQUIRED-absent + 1
   FORBIDDEN) but `DECLARED FAIL CLASSES: ['FRONTIER-STALE']` only; all three
   errors remain in `frontier_errors` and the text line. The ternary at
   `frontier_class` prefers STALE.
3. **Required floor is a floor, not a binder.** A line-neutral `CLOSED` →
   `OPEN` edit in `:139-144` passes PL-4 (required set: `90 MB PE`, `arc2-r7`)
   while RV-3 fails it (RV-3 requires `CLOSED`). Likewise the recorded PE-wall
   and cross-version stale clauses can be re-appended with anchors kept
   (EX-3 §3, CN-4 c1 matrix `extra-stale2`: PL-4/RV-3 PASS, PL-2 catches only
   its own one-line literal). This is PL-4 §6.3's own "earned, not exhaustive"
   residual; it does not fail the frozen claim, whose falsifier is the EVM
   `untested` literal. CN-4's optional 2-FORBIDDEN amendment is a later re-key,
   not a landing blocker.
4. **Past-the-bound appends** pass (measured) — named by PL-4 §6.1; keep it in
   the receipt.

### 2.6 Competing c1 patches — mutually exclusive, one landable

| patch | identity | clean | frozen seed | required-strip | verdict |
|---|---|---|---|---|---|
| **PL-4** | `80027570…`, 713 L | PASS | FAIL `FRONTIER-STALE` | FAIL `FRONTIER-UNEVALUABLE` | **LAND** |
| RV-3 | `8e420679…`, 712 L (diff extracted from RV-3.md 109-265) | PASS | FAIL `FRONTIER-STALE`+`UNATTESTED` | FAIL `FRONTIER-UNATTESTED` | not landable alongside; anchor binding is stronger (catches insertions) but its required set misses the canonical cross-version revert (EX-2 §7; not my rerun) |
| PL-2 | `2d7ee95b…`, 705 L | PASS | FAIL `FRONTIER-STALE` | **PASS** (no positive floor) | not landable alongside; measured weaker (also passes `forbidden-only`, which is the isolated FORBIDDEN arm) |

Every cross-apply exits 1 (`claims/verdicts/VZ-3/c1/cross-apply.txt`); the three
patch the same pristine bytes, so a landing can carry only one. Why PL-4:
it is the delivered artifact, its diff is additive-only, it is the only one
whose every frozen arm I re-derived end-to-end, and its catch set is the
broadest on historical reverts (EX-2 §7; EX-3 §0; CN-4 c1 matrix; CR-8
`c1-pl4-clean.txt`). Landing recipe:

```
patch .ufo/gates/c1-census-v10.py < .ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum .ufo/gates/c1-census-v10.py   # 8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca
python3 .ufo/gates/c1-census-v10.py --quiet   # exit 0; FRONTIER register (G21): 14 rows asserted, errors: []
```

## 3. C2 — EX-7's viaIR entry, audited

### 3.1 Before-state and Unknown

Command A before = 84/84 (§1). The two Unknown lines are real:
`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:33` and
`…r4-evm-vyper-leg.md:28` both name "the `viaIR` pipeline"; no corpus entry
measures it. EX-9 independently reached the same provenance.

### 3.2 Compile bytes — fresh recompile

I re-ran EX-7's `compile.js` against the receipted wave-1 solc prefix
(read-only) into `/var/tmp/vz3-r6/c2/recompile`, not reusing the delivered
outputs; all three legs reproduce the manifest byte-exactly
(`claims/verdicts/VZ-3/c2/recompile.log`):

```
solc 0.8.37+commit.f401782d.Emscripten.clang
viair-opt200 runtime 1,517 B 2ec3f557…  creation 1,560 B d85fdde9…
viair-noopt  runtime 4,144 B 0cc6938c…  creation 4,318 B f1125049…
std-opt200   runtime 1,921 B c2ceabb1…  creation 1,966 B 4541fd49…
```

`sha256sum -c evidence/manifest.sha256` → all OK; source sha
`f5391167…80cbbe`; planted K pre/post fix selector sets equal (15); planted set
== `methodIdentifiers` values; ABI `scale` pure / `digestOf` view.

### 3.3 Dispatcher walk — my own decoder

`claims/verdicts/VZ-3/c2/walk-out.json` (independent opcode scanner; PUSH
immediates handled, JUMPDEST set derived at instruction boundaries):

- **viair-opt200**: `5f3560e01c` present; guard `6004361015` present;
  **14 EQ legs** `DUP1 PUSH4 <sel> EQ PUSH2 <dst> JUMPI`, PCs 40…183, strict
  **11-byte stride**, selectors ascending, dsts
  `253/272/311/340/374/425/485/572/631/694/723/771/935/982`, all JUMPDESTs;
  **1 SUB leg** at 194: `ee02438e SUB PUSH2 0x000e JUMPI`, dst 14 (JUMPDEST).
- **viair-noopt**: same 14+1 tree (dsts 208…273), but the selector decode is
  behind a helper JUMP (`0x116`: `PUSH1 e0 SHR SWAP1 JUMP`), so the contiguous
  `5f3560e01c` string is opt200-only; the entry's "same shape" is correctly
  scoped to the compare tree.
- **std-opt200 control**: no `ISZERO` guard; 15 EQ legs at mixed gaps
  `[11,15,26]`, not sorted, no SUB — the legacy GT/EQ class.

### 3.4 Live probes (fresh, TMPDIR under `/var/tmp`)

| leg | pin | functions | dispatch | decoded sha |
|---|---|---|---|---|
| opt200 `runtime.hex` hex | 6.4.0 | **15** | `abi` ×15 | `2ec3f557…` |
| opt200 `runtime.bin` raw | 6.4.0 | **15** | `abi` ×15 | `2ec3f557…` |
| opt200 `runtime.hex` hex | 6.7.0 | **15** | `abi` ×15 | `2ec3f557…` |
| noopt `runtime.hex` hex | 6.4.0 | **15** | `abi` ×15 | `0cc6938c…` |
| std `runtime.hex` hex | 6.4.0 | **15** | `abi` ×15 | `c2ceabb1…` |
| creation.hex hex | 6.4.0 | **0** | — | `d85fdde9…` (parsed-and-empty) |
| `runtime.hex` raw (trap) | 6.4.0 | **0** | — | `19838d66…` (the hex text's own sha) |

Evidence ids are path-sensitive; mine are fresh (`ev_71da9d37…` for the
documented recheck path, matching EX-9's independent run). Offsets, mutability
14/15 (`scale` pure→view), and the CBOR trailer (`ipfs` + `solc 0x000825`) all
reproduce. Creation embedding: `creation[43:43+1517] == runtime`, one
occurrence, zero trailing bytes.

### 3.5 Corrections (three; text/scope only, none changes a measurement)

**(a) CBOR transcript — the one character-level error.** EX-7's entry line 28
writes:

```
a2 64 69706673 58 22 <ipfs 22958d9b…4945d64> 73 736f6c63 43 000825 00 33
```

The actual tail is `… 64 736f6c63 43 000825 00 33` (`64` = text(4), then
`"solc"`; `73` is the ASCII `s`). Peer EX-9 found it, CR-8 recorded it, and I
re-derived it from the runtime bytes. The prose (`ipfs` + `solc` 0x000825) is
correct. One-byte-fixed copy: **13,659 B, sha256
`97bfc4b02d16a7a968911418737d7780ceccd61833d64a64343d438ab9d1290a`**
(delivered: `6e331882…`):
`c2/entry-corrected-2026-10-19-arc3-r6-viair-dispatch-shape.md`.

**(b) Carrier census.** The source has **15** explicit `function` declarations
(`grep -c '^    function ' ViaIrVault.sol` → 15) plus `receive()`; the ABI is
15 functions + constructor + receive = 17 entries, and `methodIdentifiers` has
15 keys. The draft's "14 explicit external functions + `receive()` = 15
dispatched entries" misstates the arithmetic (its own mutability census,
view 7 + pure 1 + nonpayable 6 + payable 1, already counts 15 functions).
Correct wording: 15 explicit functions (15 selectors) + the calldatasize==0
`receive()` path, which carries no selector.

**(c) Class-marker scope.** The draft titles the class by its `SUB`-terminated
final leg. I recompiled EX-11's two carriers with the receipted solc and walked
them (`c2/ex11-terminal/walk-summary.txt`): `Ex11Linear5` (K=5, 373 B
`31b74644…`) terminates in an **EQ→handler** leg at pc 67→dst 80, with no SUB
leg; `Ex11Fallback6` (K=6, 592 B `6fe9958b…`) carries the **SUB→default** leg
at 111→14. Both have the inverted guard `6004361015`. The same sources under
the legacy pipeline (`std`, 391 B / 728 B) have no `ISZERO` guard and are
**linear EQ chains with 0 GT legs** — so "legacy = binary search" holds at
K=15/20, not at K≤6 (EX-11 measured six carriers; I re-derived the two terminal
forms and both std controls). The invariant class marker is the sorted
ascending linear scan + inverted guard; terminal orientation is
carrier-layout-scoped.

These are the entry's prose scope, not its measurements: every byte value,
selector set, offset and probe result stands. Landing copy with (a)+(b)+(c)
applied: **14,080 B, 34 lines, sha256
`09f44ce193f38aa1ec84f44b99155e10fe4e860612ef9980cb060aa0e3a64456`**:
`c2/entry-corrected-full-2026-10-19-arc3-r6-viair-dispatch-shape.md`. The
parent may land the (a)-only copy if it prefers to keep the draft's wording and
record (b)/(c) as scope notes in the landing receipt; the sha must be re-derived
for whichever copy is landed.

### 3.6 Landing and the before→after

The EVM row patch in EX-7.md §3 matches `corpus/README.md:38` byte-for-byte
(verified by diff of the minus line). My overlay of the corrected entry stem +
token on the immutable 58c3db7 objects gives
`{knowledge_files:85, mapped:85, missing:[], dangling:[], coverage_score:10.0}`
with `rule_blocks=14` unchanged (`c2/projected-85.txt`). EX-9 measured the same
on a scratch clone (`9f4f569`), so the frozen 84 → 85 is closable.

**Ruling: land exactly one C2 entry — EX-7's corrected viaIR entry + EVM
token.** Six c2 seats (EX-5, EX-8, EX-10, EX-12, CR-1, CR-2) have now landed
complete drafts of the *other* frozen candidate, the Vyper 0.4.3
`--no-optimize` / `-O none` / `-O codesize` forms; EX-11 additionally
byte-characterized five fresh carriers. They are alternatives to, not additions
to, EX-7's entry: each alone projects 85/85, while EX-7 plus any one reads
**86/86**, overshooting the frozen 84 → 85. The named deliverable and the only
candidate with independent multi-seat verification (EX-9, EX-11, CR-4, CN-1,
CN-4, this seat) is EX-7's viaIR entry; land it. The six Vyper drafts are not
interchangeable copies — they use different carriers/K (EX-5 `K8`/`Ex05Vault`,
EX-8/EX-10/EX-12/CR-1/CR-2 with their own carriers and form matrices) — so if
the integrator prefers that branch, it needs its own pick-and-verify pass, which
this seat did not do. The Vyper drafts queue for a later round (85 → 86), or
would replace EX-7 if the integrator prefers that Unknown — not both.

## 4. C3 — SC-3's rule #15, audited

### 4.1 Identity

Extracted between the ` ```markdown ` fence in SC-3.md §4, trailing LF
included: **1,605 B, 23 lines, sha256
`763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1`** —
matches SC-3's self-identity exactly. It parses as exactly one craft block and
carries 8 command-A-pattern citations.

### 4.2 Citation audit — 7/8 content-verified, 2 corrections

| citation | claim | my read | verdict |
|---|---|---|---|
| r1 `:24` | creation legs probed 0 functions | present | VERIFIED for the probe half |
| r1 `:31` | erratum: tool scope, "not byte-level absence"; runtime embedded | present | VERIFIED |
| r3 `:41-51` | same correction re-landed | erratum with six embeddings | VERIFIED |
| r4 `:39-46` | "creation probes parse empty while the runtime bytes are present verbatim" | quote at `:46` | VERIFIED |
| r4 `:17` | entry had repeated the class | "uniformly parsed-and-empty … no runtime dispatch table" | VERIFIED |
| r3 `:27` | raw-over-hex-text trap, "not a carrier defect" | present | VERIFIED |
| r4 `:25` | Vyper repetition of the trap | present | VERIFIED |
| r4 `:34` | "empty results do not prove absence of dispatch" | **absent; `:34` = `## Erratum (arc3-loop1-round5…)`; the quote is at `:29`** | **CORRECTED** |
| QUALITY.md `:21` (non-pattern) | zero-finding must state parsed-and-empty vs excluded-from-inventory | row 11 present | VERIFIED |

**F1 (mandatory fix):** `…r4-evm-vyper-leg.md:34` → `:29`. Command A cannot see
this (34 ≤ 63); it is instrument-green / content-red, the exact
"census-checked vs instrument-graded" gap. Corrected text: **`6967b1e3e7fbdb43492e191426399c0311ab3bf85ee307f1a181a3edd235511e`**
(1,605 B / 23 lines). Independently produced by EX-14, EX-16, RV-5 and
CN-4/CR-5/CR-6.

**F2 (precision fix):** the same sentence attaches "on blobs that byte-contain
the full runtime" to r1 `:24`, whose actual claim is the opposite ("Creation
blobs carry no runtime dispatch table"); the containment measurement is r1
`:31`, cited in the next clause. SC-4 re-anchors the sentence; its text is
**`a1bceb4074328d9d60d14ddf0789b9bcd18ca38936c217d78fc37b1091ec1789`**
(1,605 B / 23 lines). The only diff vs `6967b1e3` is the `:24` clause position.

### 4.3 Landing simulation (my own, both revs, combined with C2)

`claims/verdicts/VZ-3/c3/simulation.txt` — exact command-A split and citation
resolution, corpus read via `git show`:

```
58c3db7 / c625d5d before : rule_blocks 14, resolved 14, depth 10.0
+ 6967b1e3                : rule_blocks 15, resolved 15, depth 10.0 (8 refs)
+ a1bceb40                : rule_blocks 15, resolved 15, depth 10.0 (8 refs)
+ RV-7 ccbc5cdb           : rule_blocks 15, resolved 15, depth 10.0 (6 refs)
EX-7 corrected entry + token + one rule-15:
{knowledge_files:85, mapped:85, missing:[], dangling:[], coverage_score:10.0,
 rule_blocks:15, citation_resolved_rules:15, depth_score:10.0}
```

### 4.4 Candidate reconciliation

| text | bytes | sha256 | refs | 15/15 | ruling |
|---|---|---|---|---|---|
| SC-3 verbatim | 1,605 | `763c44b5…` | 8 | yes | **do not land** (F1 wrong-line quote; F2) |
| SC-3 + `:34→:29` | 1,605 | `6967b1e3…` | 8 | yes | accepted minimal fallback |
| SC-3 + both fixes | 1,605 | `a1bceb40…` | 8 | yes | **recommended** |
| RV-7 alternative | 1,565 | `ccbc5cdb…` | 6 | yes | valid substitute; do not land with SC-3 |

RV-7's text is content-clean and avoids both anchors (its F1 finding — r3's
erratum points `:24` at a sentence that is r1's — I confirm: r3:24 is the
Rv2TokenOpt row at `c418be0`/`40de383`/`58c3db7`). But it is a second complete
rule for the same lesson; landing two yields `rule_blocks=16` (measured by
EX-13/EX-15, and implied by my split), failing the frozen 14 → 15 falsifiable.
RV-8's recommendation to land SC-3 verbatim did not content-check `:34`; its
own citation table calls `:34` verified while CN-2's byte grep (`'untested'
inside r4:34? 0`) and my read show otherwise — do not follow that part.

**Ruling: land exactly one rule-15 text; recommended `a1bceb40…` (both fixes),
fallback `6967b1e3…`.** Command:
`sed -i '255r <file>' SKILL.md` (line 255 is rule 14's last line; the draft
ends with LF), then command A must read 15/15/depth 10.0.

## 5. Peer field — what I audited and how it reconciles

| peer | artifact | my audit | disposition |
|---|---|---|---|
| PL-2 | c1 patch `2d7ee95b…` (705 L) | round-trip reproduced; measured no positive floor | duplicate; do not land |
| RV-3 | c1 patch `8e420679…` (712 L) | round-trip reproduced; insertion anchors stronger; own required set has gaps (EX-2) | duplicate; do not land |
| EX-2 | c1 verification | read; corrections (insertion tolerance, class list) match my arms | concurs with PL-4 |
| EX-3 | c1 verification | read; 44/44 insertion sweep, unguarded-literal finding match my probes | concurs with PL-4 |
| EX-6 | c2 evidence-only (different carrier) | retained bytes real; no entry | no conflict; EX-7 is the entry |
| EX-9 | c2 verification | read; CBOR `73`→`64` confirmed by my byte parse; 85/85 scratch landing | concurs with corrected EX-7 |
| EX-11 | c2 verification + 5 fresh carriers | recompiled `Ex11Linear5`/`Ex11Fallback6` (shas equal), re-derived both terminal forms and the std K-scope | its three scope corrections adopted (census / terminal / K-scope) |
| EX-5 / EX-8 / EX-10 / EX-12, CR-1 | Vyper optimizer-form entry drafts | headers, sources and evidence trees read; each is a complete alternative entry; EX-11/CR-2 rechecks 15/15 | do not land alongside EX-7 (86/86) |
| CR-2 | Vyper entry draft + rechecks | 15/15 payloads present; a full draft has now landed | alternative; not this round |
| CN-1 | verdict seat | read; PL-4, EX-7 85/85, exactly-one-rule rulings agree; recommends RV-7 for c3 (split with the SC-3-corrected seats) | concurs except the c3 text preference |
| VZ-1 / VZ-2 / CR-7 | verdict seats | artifacts present with c1/c2/c3 evidence; not fully audited here | point-in-time |
| RV-7 | c3 alternative `ccbc5cdb…` | identity + 15/15 reproduced; F1 confirmed | do not land alongside |
| EX-13/14/15/16, RV-5/6/8, SC-1/2/4 | c3 verification cluster | `:34→:29` consensus verified; SC-4's `a1bceb40…` verified; EX-15's RV-7 alternative read | one text only; recommend `a1bceb40…` |
| CN-2 | verdict seat | c1 cross-apply conflicts (my own 6/6 exit 1), c2 overlay 85, c3 sims 15/15 | concurs |
| CN-4 | verdict seat | c1 matrix matches my arms; c2 85/85 projection; c3 6967b1e3 + combined 85/85 | concurs |
| CR-5/CR-6/CR-8 | verdict seats | c3 sims/file `rule15-fixed` = `6967b1e3`; CR-8 records the CBOR fix | concurs |
| VZ-4 | earlier verdict | audited RV-3 because PL-4 landed after its poll; C2 pending; C3 `:34→:29` | superseded by this audit on C1/C2 |

## 6. Combined landing recipe (parent)

1. **C1** — apply `claims/c1/PL-4/patch-v10-to-r10.diff` to
   `.ufo/gates/c1-census-v10.py`; expect `80027570…`, 713 lines, clean PASS,
   `FRONTIER register (G21): 14 rows asserted, errors: []`.
2. **C2** — copy
   `claims/verdicts/VZ-3/c2/entry-corrected-full-2026-10-19-arc3-r6-viair-dispatch-shape.md`
   (all three fixes, `09f44ce1…`) — or the (a)-only copy
   `…/entry-corrected-2026-10-19-arc3-r6-viair-dispatch-shape.md`
   (`97bfc4b0…`) if (b)/(c) are recorded as landing-receipt scope notes — to
   `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md`; apply the
   EVM-row token patch from `claims/c2/EX-7.md` §3 (minus line = current
   `corpus/README.md:38`). Land **no** Vyper optimizer-form draft this round.
3. **C3** — insert **one** of
   `claims/verdicts/VZ-3/c3/rule15-a1bceb40.md` (recommended) or
   `…/rule15-6967b1e3.md` after `SKILL.md:255`; do not insert both.
4. **Measure** at the landing commit: command A →
   `{knowledge_files:85, mapped:85, missing:[], dangling:[], coverage_score:10.0,
   rule_blocks:15, citation_resolved_rules:15, depth_score:10.0}`; census gate →
   exit 0 PASS. Record the fresh identities in the landing receipt (gate
   `80027570…`; entry `09f44ce1…` or `97bfc4b0…`; chosen rule hash), never
   inline in the hashed files.

## 7. Residuals and what I did not do

- **C1 residual:** register rows are span+required floors, not bullet anchors;
  a one-line insertion (even carrying a retracted literal) passes; a
  line-neutral semantic flip that keeps the required tokens (`CLOSED`→`OPEN`)
  passes; past-`:162` appends pass; recorded PE-wall/cross-version literals are
  not FORBIDDEN in PL-4 (CN-4's 2-literal amendment is a later re-key). The
  landing receipt must name these; none fails the frozen claim.
- **C2 residual:** single solc 0.8.37, one carrier family (EX-11's five fresh
  carriers extend the class but are not in the entry), K=15, runtime class
  1.5–4.1 KB; the terminal-leg orientation and "legacy = binary search" claims
  are K-/layout-scoped in the full corrected copy; six Vyper optimizer-form
  drafts queue for a later round. The (a)-only entry copy changes one
  character; the full copy changes three prose passages.
- **C3 residual:** F2 is precision-only; RV-7's alternative remains a valid
  substitute; the r3 erratum's dangling `:24` pointer (RV-7 F1) is append-only
  debt for a later correction pass.
- **Not done:** I did not modify the gate, corpus, SKILL.md or any tracked file;
  I did not land anything; I did not re-run the r3/r4 carrier probes beyond the
  c2/c3 evidence I cite; peer numbers I did not re-execute are marked as peer
  audits above, not as my evidence.

## 8. Evidence index (`claims/verdicts/VZ-3/`)

- `commandA-58c3db7.json`, `commandA-c625d5d.json` — before-state.
- `c1/patch-identity.txt`, `c1/clean-v10.json`, `c1/clean-r10.json`,
  `c1/REPO-ROOT-r10.txt`, `c1/arms-summary.txt`, `c1/*__*.txt` (per-gate arm
  outputs), `c1/cross-apply.txt`, `c1/insert-correction.txt`,
  `c1/row-strength.txt`, `c1/c1-census-v10-r10-verified.py`.
- `c2/walk-out.json`, `c2/recompile.log`, `c2/live-probe-summary.json`,
  `c2/live-probe-*.json` (7 legs), `c2/cbor-correction.txt`,
  `c2/projected-85.txt`, `c2/overlay.py`, `c2/overlay-out-{58c3db7,c625d5d}.json`,
  `c2/entry-corrected-…md` (a-only), `c2/entry-corrected-full-…md` (a+b+c),
  `c2/ex11-terminal/` (recompiled carriers, compile scripts, walk summary).
- `c3/identities.txt`, `c3/simulation.txt`, `c3/simulate.py`,
  `c3/simulate-out.txt`, `c3/rule15-6967b1e3.md`,
  `c3/rule15-a1bceb40.md`, `c3/rule15-sc3-original-763c44b5.md`.
