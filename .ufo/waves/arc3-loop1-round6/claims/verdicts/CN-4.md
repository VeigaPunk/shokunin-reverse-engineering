# CN-4 — verdicts/convergence: reconcile the three delivered artifacts + all landed peers

Seat CN-4, chain verdicts/convergence, wave arc3-loop1-round6, 2026-10-19.
Measured state: HEAD `c625d5de57e045188b5ce8cd450a57b349f90785` (records `c625d5d`,
work `58c3db7`), re-derived first-hand. Gate `.ufo/gates/c1-census-v10.py` sha256
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`, 610 lines.
Every number below is my own measurement (lane rule #14); peer artifacts are cited
as objects under audit, never as evidence. Scratch: `/var/tmp/cn4-arc3r6/` (nothing
under `/tmp`). No tracked file, gate, corpus, PROVINCE/SKILL/SCORECARD or custody
path was modified; git was read-only. Evidence: `claims/verdicts/CN-4/`
(`baseline.txt`, `c1-arms.txt`, `c2-verification.txt`, `c3-verification.txt`,
`c2-rederive.json`).

## 0. Rulings in one table

| Claim | Artifact audited | Ruling |
|---|---|---|
| C1 operability | **PL-4** `claims/c1/PL-4.md` + patch | **REPRODUCED** end-to-end — **recommended landing base**, with a four-row amendment (§1.5) |
| C1 | **RV-3** `claims/c1/RV-3.md` + inline patch | **REPRODUCED** end-to-end — valid alternative; do not land both |
| C1 | **PL-2** `claims/c1/PL-2.md` + patch | **REPRODUCED as an instrument, CORRECTED as a design**: blind to claim-less bullets; not sufficient for frozen C1; do not land standalone. Its two earned literals and its header-marker idea are carried into §1.5 |
| C2 coverage | **EX-7** `claims/c2/EX-7.md` + entry-draft | **REPRODUCED** — all byte claims independently re-derived; projected 85/85; four content fixes + one wording fix before landing (§2.2) |
| C2 | **EX-6** `claims/c2/EX-6.md` | **VERIFICATION REPRODUCED**: its four entry defects independently confirmed where re-derived (§2.2); its `fallback()` carrier is a narrowing of the entry's Unknown, not part of the entry |
| C3 depth | **SC-3** `claims/c3/SC-3.md` rule #15 | **REPRODUCED with two CORRECTIONS** (`:34`→`:29`; the `r1:24` attachment); best-corrected text is SC-4's `a1bceb40…` (§3.3) |
| C3 | **SC-4** `claims/c3/SC-4.md` corrected rule | **REPRODUCED** — `a1bceb40…`, 15/15 at both revs; **recommended rule text** |
| C3 | **RV-7** `claims/c3/RV-7.md` rule #15 + F1 | **REPRODUCED**; F1 (r3 erratum dangling `:24` pointer) **VERIFIED** — alternative zero-edit draft |
| Verdicts | **VZ-4** `claims/verdicts/VZ-4.md` | Its C1 audit of RV-3 and its C3 `:34`→`:29` correction **REPRODUCED**; its C2 PENDING is **superseded** by the now-landed EX-7 entry; it did not see PL-2/PL-4/RV-7 |
| Verdicts | **CN-2 / CR-6 / CR-8** | Independent convergence seats; same landing triad (PL-4, EX-7, SC-3-lineage rule). CR-6's PL-4 §6.1 residual correction and CR-8's `a1bceb40…` recommendation are re-derived in §1.5/§3.3 |

The wave cannot land all three c1 patches (they are three mutually exclusive edits to
the same gate) or multiple c3 rules. Convergence recommendation:
**C1 = PL-4 + the §1.5 amendment; C2 = EX-7 entry with the §2.2 fixes; C3 = SC-4's
corrected text `a1bceb40…`** (RV-7's draft is the zero-edit alternative).
The verification/convergence seats that landed after the three delivered artifacts
(EX-6, SC-4, CN-2, CR-6, CR-8) reached the same triad independently; their agreement
is reconciliation, not evidence. The `c3` chain also carries EX-13..16, RV-5/6/8,
SC-1/SC-2 verification seats I did not re-derive — their headings report the same
SC-3 lineage and the same two anchor corrections; they do not change the landing
decision.

## 1. C1 — the census Frontier blind spot

### 1.1 Baseline, first-hand

`baseline.txt`: HEAD/work as above; gate `d0772ce8…` 610 lines; PROVINCE 162,
SKILL 390, SCORECARD 1696 lines. SCOPE PROVINCE rows at gate `:216-222` read exactly
8-13/15-26 (CURRENT), 40-43/45-62/119-131 (DATED), 44/64-71 (CURRENT) — no row
covers 73-93 or 133-162. v10 clean run: `VERDICT: PASS (stale=0 ambiguous=0
undeclared=0 unresolved=0)` exit 0, G2 17/14/3. The frozen before-state
**REPRODUCED**.

### 1.2 The three c1 patches — identity and arm matrix

All three were applied to a pristine `git show HEAD:` copy and measured by me
(`c1-arms.txt`). No patch was applied to the repo gate.

| patch | applies | resulting sha256 / lines | clean tree | frozen seeded literal :91-93 | claim-less bullet (RISC-V :135-138 stripped) | the two other earned stale literals (§1.3) | 161-line truncation |
|---|---|---|---|---|---|---|---|
| PL-4 | clean | `80027570…aecca` / 713 | PASS 0 | FAIL `FRONTIER-STALE` | **FAIL** `FRONTIER-UNEVALUABLE` | **PASS (blind)** | FAIL `UNREADABLE`+`FRONTIER-UNEVALUABLE` |
| RV-3 | clean | `8e420679…95ebf` / 712 | PASS 0 | FAIL `FRONTIER-STALE`+`FRONTIER-UNATTESTED` | **FAIL** `FRONTIER-UNATTESTED` | **PASS (blind)** | FAIL `FRONTIER-UNATTESTED` |
| PL-2 | clean | `2d7ee95b…8ce7b` / 705 | PASS 0 | FAIL `FRONTIER-STALE` | **PASS 0 (blind)** | **FAIL `FRONTIER-STALE` ×2** | FAIL `UNREADABLE` |

JSON invariance (`--json`, clean real tree): all three keep the **17 shared keys
identical** (`differing: []`), counts equal, floor `PROVINCE=17/SCORECARD=14/SKILL=3`;
PL-4/RV-3 add `frontier_rows` + `frontier_errors`, PL-2 adds `frontier_register` +
`frontier_stale`. PL-4 and RV-3 keep the human `VERDICT:` line byte-identical; PL-2
appends `frontier=N` (`…unresolved=0 frontier=0`), a format change for any strict
line parser. PL-2 also adds two SCOPE rows (73-93, 133-162 class FRONTIER).

### 1.3 The convergence defect found across the three (measured, not inferred)

I built two fault trees independently of every peer's seeder:

- **Claim-less regression** (`/var/tmp/cn4-arc3r6/strip`): PROVINCE `:135-138`
  replaced by `- **RISC-V analysis** — see corpus.` + blank lines (line count kept).
  v10 PASS (blind); PL-4 FAIL; RV-3 FAIL; **PL-2 PASS** — its register holds three
  historical literals, not per-bullet claims.
- **Other earned stale literals** (`/var/tmp/cn4-arc3r6/extra-stale2`): the two
  wordings repaired in `40de383` and cited by PL-2's register — `hits REA's ~900s
  internal session deadline` into `:139-144` and `probe-refused since r2` into
  `:157-160` — while keeping each bullet's required anchors. PL-4 PASS, RV-3 PASS,
  **PL-2 FAIL (both)**.
  Provenance `git show 40de383 -- PROVINCE.md`: `-- **>90 MB PE scale wall** — 91.6 MB
  Godot ARM64 PE hits REA's ~900s internal …` and `- probe-refused since r2;`.

So no single patch satisfies the frozen claim's intent ("the Frontier-region staleness
claims become gradable … a frontier-claim register each bullet is checked against"):
PL-4/RV-3 cover each bullet + one retired literal; PL-2 covers three retired literals
but not the bullets. The union is required.

### 1.4 Ruling and landing recommendation

- **PL-4 is the recommended base.** 14 register rows (13 bullets + intro `:75-80`),
  REQUIRED positive floor + FORBIDDEN retired literal, G19 max-end raised to 162
  (measured: 161-line tree → `UNREADABLE`), six-tree demonstration reproduced, and
  the frozen (a)/(b)/(c) all hold. Its only material gap is FORBIDDEN coverage of the
  two literals in §1.3.
- **RV-3 is an equally valid alternative** (13 rows, per-row anchor line,
  FRONTIER-ANCHOR/UNATTESTED/STALE) and has one advantage PL-4 lacks: a bullet-head
  anchor that fails loudly on a reflow instead of silently grading shifted spans.
  It has the same two-literal FORBIDDEN gap. Landing both is impossible — they edit
  the same table region; the integrator must pick one.
- **PL-2 should not land standalone.** It passes the named falsifier but is blind to
  claim-less bullets, and it alters the `VERDICT:` line format. Two contributions
  are worth carrying: the two extra earned literals and the section-header marker
  idea; both are grafted into PL-4 in §1.5.

### 1.5 Amendment to PL-4 (scratch-measured; integrator applies)

Four additions: two section-header rows (closing the reflow edge CR-6 measured:
a renamed `## Frontier` and a blank line before `:133` both PASS PL-4 as delivered;
measured on my own trees `edge-header`/`edge-insert133`), and the two earned literals
from PL-2 (§1.3). The header rows are PL-2's marker idea expressed in PL-4's row
shape. Amended arm matrix, all measured (`c1-arms.txt`): clean **PASS 0**; `:91-93`
seed **FAIL `FRONTIER-STALE`**; citations stripped **FAIL `FRONTIER-UNEVALUABLE`**;
161-line truncation **FAIL `UNREADABLE`+`FRONTIER-UNEVALUABLE`**; claim-less RISC-V
bullet **FAIL**; both extra literals **FAIL `FRONTIER-STALE` ×2**; renamed header
**FAIL**; header insertion **FAIL**.

```diff
--- a/.ufo/gates/c1-census-v10.py (PL-4 r10)
+++ b/.ufo/gates/c1-census-v10.py (PL-4 r10 + CN-4 amendment)
@@ FRONTIER[] rows (add two header rows, extend two FORBIDDEN lists)
 FRONTIER = [
+    ("PROVINCE.md", 73, 73, [r"^## Frontier$"], []),
     ("PROVINCE.md", 75, 80, [r"Claimed in MINT\.md, not yet held"], []),
+    ("PROVINCE.md", 133, 133, [r"^### Round-4 frontier \(post-unlock\)$"], []),
@@
-    ("PROVINCE.md", 139, 144, [r"90 MB PE", r"arc2-r7"], []),
+    ("PROVINCE.md", 139, 144, [r"90 MB PE", r"arc2-r7"], [r"~900s internal session deadline"]),
-    ("PROVINCE.md", 157, 160, [r"Cross-version", r"r12-02|r14-01"], []),
+    ("PROVINCE.md", 157, 160, [r"Cross-version", r"r12-02|r14-01"], [r"probe-refused since r2"]),
```

After this amendment the register closes the union of every measured Frontier
regression in this wave: `untested` (:91-93), the two `40de383`-repaired wordings
(:139-144, :157-160), claim-less rewrites on all 13 bullets, section-header renames /
insertions, and silent truncation. The header rows also fix the residual CR-6 named
against PL-4 §6.1 (`PL-4.md:327-333`) — that sentence's "insertions anywhere inside
`:73-162` are caught" is too strong for the *delivered* register; it becomes true with
this amendment. The landing receipt must record post-edit identity (the gate's own
rule-#14 discipline; the r10 block at gate `:89-93` forbids an inline self-hash).

## 2. C2 — the corpus Unknown (viaIR dispatcher)

### 2.1 Before-state and Unknown provenance

Command A at `58c3db7` (`baseline.txt`): `{"knowledge_files": 84, "mapped": 84,
"missing": [], "dangling": [], "citation_resolved_rules": 14, "rule_blocks": 14,
"coverage_score": 10.0, "depth_score": 10.0}`. The designated Unknown is open at
HEAD: `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:33` and
`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28` both name "the `viaIR`
pipeline". **VERIFIED.**

### 2.2 EX-7's byte claims — independently re-derived

I wrote my own EVM opcode walker (`/var/tmp/cn4-arc3r6/scan2.py`, PUSH1..PUSH32
immediates handled; PUSH4 counted only at opcode boundaries) over the retained
runtimes. Results (`c2-rederive.json`, `c2-verification.txt`):

| EX-7 claim | My measurement | Verdict |
|---|---|---|
| viair-opt200 runtime 1,517 B `2ec3f557…` | 1,517 B, sha `2ec3f557f6f2fb22…`, 990 opcodes | REPRODUCED |
| 19 PUSH4 sites; 15 selectors + `4e487b71`×2 + `0c2eae8d` + `3c3332b9` | 19 sites, 18 distinct (15 selector + 3 constants; `4e487b71` twice) | REPRODUCED |
| Inverted guard `PUSH1 4 CALLDATASIZE LT ISZERO PUSH2 0x0022 JUMPI` | head `6080604052 60043610 15 610022 57 5b 3615 610018 57 5f80fd` | REPRODUCED |
| 14 `DUP1 PUSH4 sel EQ PUSH2 dst JUMPI` legs, 11-byte stride, ascending, all dst JUMPDEST | 14 EQ legs, EQ-pc gaps `[11]×13`, selectors ascending `01681a62`→`d0e30db0`, dsts 253–982 all JUMPDEST | REPRODUCED |
| 15th leg `PUSH4 ee02438e SUB PUSH2 0x000e JUMPI` | PUSH4 at 194, `SUB` at 199, dst 14 (a JUMPDEST); no EQ on this leg | REPRODUCED |
| viair-noopt same shape, dsts 208–273, SUB leg at 194 | 14 legs, dsts 208–273 ascending, PUSH4 `ee02438e` at 194 | REPRODUCED |
| std-opt200 control: GT/EQ binary search; 18 dispatch PUSH4 sites/15 distinct + 4 constants | 22 sites/19 distinct total = 18 dispatch (15 EQ + 3 GT) + `3c3332b9`,`4e487b71`,`0c2eae8d`,`43000825`; selectors not ascending | REPRODUCED |
| Offsets: 14/15 = EQ `PUSH2` dst (JUMPDEST); `mark` = 204 = push4_pc+10, not a JUMPDEST | probe rows: 14/15 equal EQ dst; `0xee02438e`→204; 194+10=204; control 15/15 | REPRODUCED |
| Selector set = `methodIdentifiers` (15) | dispatch set == methodIdentifiers, 15/15, zero missing/extra | REPRODUCED |
| Runtime embedded in creation at +43 of 1,560 B | `creation.bin.find(runtime.bin)` = 43, trailing 0, exact | REPRODUCED |
| Probe legs 15/15 K/K; traps 0 | envelopes: opt200 15, raw 15, 6.7.0 15, noopt 15, control 15; TRAP 0 (decoded sha = hex file `19838d66…`), creation 0 (decoded sha = creation `d85fdde9…`) | REPRODUCED |
| Mutability: 14/15 agree; `scale(uint256,uint256)` pure→view | 1 divergence, exactly that function | REPRODUCED |
| CBOR trailer `solc 0x000825` (=0.8.37) | tail `…736f6c63430008250033` in all three runtimes | REPRODUCED |

**Pre-landing text fixes** (all re-derived by me, none changes a measured byte, a
probe result, or command A; EX-6 found the same four content defects, (a)-(d)):

- **(a) "14 explicit external functions" → 15.** ABI census: `{function:15,
  constructor:1, receive:1, fallback:0}`; the selector chain is 14 EQ + 1 SUB = 15
  legs. The sentence's own mutability census (7+1+6+1) sums to 15. K=15 is correct;
  only the word is wrong.
- **(b) "42 files" → 46.** `find …/EX-7 -type f | wc -l` = 46 (src 1, scripts 5,
  evidence 8, out 24, probe 7, entry-draft 1).
- **(c) Drop `0c2eae8d` from "also appear in the r3 VaultB census".**
  `grep -rn 0c2eae8d corpus/` = **0 hits**; only `3c3332b9`/`4e487b71` appear at
  `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:26`. Keep the
  viaIR-runtime measurement of `0c2eae8d`; drop the corpus attribution.
- **(d) `0x000e` is a zero-calldata router, not only a revert path.** Bytes
  `14..25` = `5b 36 15 61 0018 57 5f 80 fd 5b`: at 14, `CALLDATASIZE; ISZERO;
  PUSH2 0x18; JUMPI` → 0-byte calldata goes to the receive trampoline (24);
  nonzero falls through `PUSH0; DUP1; REVERT`. The SUB-leg mismatch case does reach
  it with nonzero calldata and reverts; describe both branches.
- **(e, wording only) "the carrier file's own sha256".** The carrier file is
  `runtime.hex` (sha `19838d66…`); `2ec3f557…` is the **decoded** runtime's sha.
  Fix the parenthetical, not the hash.

### 2.3 Projected landing

Overlay of the entry stem + EVM map token on `58c3db7` objects (no write):
`{"knowledge_files": 85, "mapped": 85, "missing": [], "dangling": [],
"coverage_score": 10.0}`. Combined with the recommended c3 rule (SC-4's text) the
projection is `85/85, rule_blocks=15, citation_resolved_rules=15, depth_score=10.0`
(measured by overlay at `58c3db7`, `c3-verification.txt`).
**C2 verdict: the entry artifact is COMPLETE and REPRODUCED; the after-state is
pending the parent's landing** (the file must move to `corpus/knowledge/` and the
token to `corpus/README.md:38`; command A must be re-run on the landed tree).

## 3. C3 — rule #15

### 3.1 Baselines and drafts

Command A at both revs: `rule_blocks=14`, `citation_resolved_rules=14` (84/84) —
**REPRODUCED**. The chain produced one delivered draft plus corrected variants and
one independent alternative:

| draft | bytes / lines / sha256 | corpus refs (distinct) | lands 15/15 at `58c3db7` and `c625d5d` |
|---|---|---|---|
| SC-3 §4 | 1,605 / 23 / `763c44b504f9964d…` | 8 (r1:24,31; r3:27,41-51; r4:17,25,34,39-46) | yes |
| SC-3 fixed (`:34`→`:29` only) | 1,605 / 23 / `6967b1e3e7fbdb43…` | 8 | yes |
| **SC-4 corrected (both anchors)** | **1,605 / 23 / `a1bceb4074328d9d…`** | 8 | yes |
| RV-7 §3 | 1,565 / 23 / `ccbc5cdbbefc8608…` | 5 (r1:24; r3:27,41-51; r4:25,39-46) | yes |

### 3.2 Corrections, all verified first-hand

- **SC-3's `r4:34` citation is wrong (VZ-4's correction, confirmed).**
  `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:34` is
  `## Erratum (arc3-loop1-round5 correctness sweep, append-only)`; the quoted
  limitation — "empty results do not prove absence of dispatch" — is at `:29`.
  Both `:29` and `:34` resolve in-bounds under command A, so the mis-citation does
  not move `rule_blocks`; it would land a wrong pointer. **Fix before landing.**
- **SC-3's `r1:24` attachment is a precision defect (SC-4/CR-8; I re-derived the
  content).** The sentence "probed 0 functions on blobs that byte-contain the full
  runtime (`r1:24`)" hangs the containment clause on a line that asserts the
  opposite: `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:24` contains the
  0-function result and "Creation blobs carry no runtime dispatch table"; the
  containment measurement is at `:31`. Minimal fix: attach `:24` to "0 functions"
  and let the following `:31` citation carry the embedding. Not a factual error in
  the rule, but the landed rule would mispoint readers. SC-4's `a1bceb40…` text is
  exactly this fix; measured 15/15 at both revs.
- **RV-7's F1 is real.** At `c418be0`, `40de383` and `58c3db7`, r3's line 24 is the
  `Rv2TokenOpt` RESULT row; the sentence "Creation blobs carry no runtime dispatch
  table" exists only inside the erratum at `:41`. The r3 erratum's `:24` pointer is
  therefore dangling (it is r1's `:24`). The byte facts in the erratum are true; only
  the attribution is wrong. Queue as an append-only corpus correction in a later
  round — outside this wave's write scope.

### 3.3 Ruling

**Land SC-4's corrected text `a1bceb40…`** (the SC-3 rule with both anchors fixed;
1,605 B / 23 lines; re-derive its sha after landing). It is the best-corrected
candidate: the fuller SC-3 citation web (8 distinct refs), both mispoint fixes, and
15/15 resolved at both revs. If the integrator wants a zero-edit landing, **RV-7's
draft is the already-correct alternative** (5 distinct refs, same measured outcome).
If only the `:34`→`:29` fix is adopted (`6967b1e3…`), the `r1:24` precision defect
remains — acceptable but recorded here. Do not land more than one: two rule texts
would read `rule_blocks=16` with duplicate content and the craft table would carry
the same rule twice.

## 4. Peer reconciliation

| Peer | What it claimed | My ruling |
|---|---|---|
| PL-4 (c1) | in-place r10, 14-row register, sha `80027570…` | REPRODUCED; recommended base + §1.5 amendment |
| RV-3 (c1) | in-place r10, 13-row register, sha `8e420679…` | REPRODUCED; valid alternative (better reflow anchor), same two-literal gap |
| PL-2 (c1) | in-place r10, 2 SCOPE rows + 3-literal register, sha `2d7ee95b…` | Instrument REPRODUCED; design CORRECTED — blind to claim-less bullets, VERDICT line changed; do not land standalone |
| EX-6 (c2) | independent verification of EX-7; second carrier family; `fallback()` extension | **VERIFICATION REPRODUCED**: its four entry defects (a)-(d) independently confirmed (§2.2); its `fallback()` carrier is a narrowing of the entry's Unknown, not part of the entry |
| EX-7 (c2) | entry-draft + 7 sealed probes + 3 compile legs | REPRODUCED in full (`c2-verification.txt`); four content fixes + one wording fix (§2.2); projected 85/85 |
| SC-3 (c3) | rule #15, 1,605 B `763c44b5…` | REPRODUCED with two anchor corrections; its citation web is the basis of the landed rule |
| SC-4 (c3) | corrected rule `a1bceb40…` + chain reconciliation | REPRODUCED — both anchor fixes; **recommended rule text** |
| RV-7 (c3) | alternative rule #15 + F1 finding | REPRODUCED; F1 VERIFIED; valid zero-edit alternative |
| VZ-4 (verdicts) | RV-3 audit + SC-3 correction + C2 PENDING | RV-3 audit and `:34`→`:29` correction REPRODUCED; C2 PENDING superseded by EX-7's landed entry; it did not see PL-2/PL-4/RV-7 |
| CN-2 (verdicts) | same three-way c1 fork; PL-4 recommended, RV-3 alternative, PL-2 rejected | CONCURS with my independent ruling; its "bare held" bullet test is the same defect class as my RISC-V strip |
| CR-6 (verdicts) | PL-4 verified + §6.1 residual correction; EX-7; SC-3 | CONCURS; its two edge trees (`## Frontier` renamed, blank before `:133`) were invisible to PL-4 as delivered — I reproduced the header-rename edge and closed both in §1.5 |
| CR-8 (verdicts) | PL-4 + EX-7 + SC-3/SC-4; integrated 85/85+15/15 | CONCURS; its `a1bceb40…` recommendation is the text I measured and recommend |

## 5. Residuals (named, not absorbed)

1. **C1 register is a declared-literal list, not a semantics engine.** Novel frontier
   staleness (a claim never previously retracted) stays with the round audit. The
   amendment closes only the three literals with measured `40de383` provenance.
2. **Reflow/header edges are design-dependent (measured).** Delivered PL-4 *passes*
   a renamed `## Frontier` header and a blank line inserted before `:133` (my trees
   `edge-header`, `edge-insert133`; CR-6 measured the same) and fails a one-line
   insert before `:82` with two REQUIRED-absent rows. RV-3 fails both insertion
   shapes (`:82` → 13 FRONTIER-ANCHOR rows; `:133` → 8) but **also passes the header
   rename** — it has no header row. PL-2 catches the header rename via its marker
   rows (my run: FAIL), which is where the §1.5 header-row idea comes from. The
   amendment closes the header edges in the PL-4 base — amended arm matrix: renamed
   header FAIL, header insertion FAIL. Without it, PL-4's §6.1 claim ("insertions
   anywhere inside `:73-162` are caught") is **too strong** and should be corrected
   in the landing receipt.
3. **The three c1 patches are mutually exclusive.** Applying more than one will fail
   to apply; the landing receipt must name the chosen base and its sha.
4. **C2/C3 after-states require landing.** My 85/85 and 15/15 are overlays on
   `58c3db7` objects; the parent must re-run command A on the landed tree and record
   the real numbers.
5. **EX-7's entry is not yet a corpus entry.** Its `source:` block and recheck line
   point at wave artifacts; that is correct at draft stage but the landed file must
   keep the citations resolvable (they are `.ufo/waves/…` paths, outside command A's
   `corpus/knowledge/` pattern, so they do not affect `citation_resolved_rules`).
6. **EX-6's `fallback()` measurement is corpus debt, not part of EX-7's entry.**
   It narrows one of the entry's named Unknowns (viaIR + real `fallback`, K=10 K/K,
   SUB-leg at dst 14) but is a single carrier / single solc / opt200 result; queue
   as a future entry or erratum, do not fold into this landing.
7. **Pre-existing dirty file**: `git status --porcelain` shows `M
   .ufo/waves/arc2-loop1-round10/C3.md` from a prior round; it is not mine and I did
   not touch it.

## 6. Landing order for the parent

1. **c1**: apply `c1/PL-4/patch-v10-to-r10.diff` to `.ufo/gates/c1-census-v10.py`,
   then the four-row §1.5 amendment. Re-run clean (`PASS`, `FRONTIER register (G21):
   16 rows asserted, errors: []`), the `:91-93` seed (`FRONTIER-STALE`), the RISC-V
   strip and the two extra literals. Record the post-edit sha in the landing receipt
   (not inline).
2. **c2**: copy `EX-7/entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md` to
   `corpus/knowledge/` after the §2.2 text fixes; append the token to the EVM row at
   `corpus/README.md:38`. Re-run command A → expect 85/85, `missing []`, `dangling []`.
3. **c3**: append SC-4's `a1bceb40…` text after `SKILL.md:255`, before the blank
   lines preceding `## Config custody…`; re-derive its sha; re-run command A →
   `rule_blocks=15`, `citation_resolved_rules=15`, depth 10.0.
4. **Combined** (measured overlay): `knowledge_files=85, mapped=85, missing=[],
   dangling=[], rule_blocks=15, citation_resolved_rules=15, coverage=10.0, depth=10.0`.
5. **Queue for later rounds, do not fold into this landing**: RV-7's F1 (r3 erratum
   `:24` pointer) and EX-6's `fallback()` narrowing as corpus debt.

## 7. Custody

- Wrote only `claims/verdicts/CN-4.md` and `claims/verdicts/CN-4/` (`baseline.txt`,
  `c1-arms.txt`, `c2-verification.txt`, `c3-verification.txt`, `c2-rederive.json`).
- Read-only: gate, PROVINCE.md, SKILL.md, SCORECARD.md, `corpus/`, the peer
  artifacts cited in §0/§4, `git show`/`rev-parse`/`ls-tree`/`status`.
- Scratch: `/var/tmp/cn4-arc3r6/` (pristine patch copies, `pl4/amended.py`,
  `pl4/amended2.py`, trees `clean`, `seeded-forbidden`, `seeded-req-evm`,
  `truncated`, `strip`, `extra-stale2`, `edge-header`, `edge-insert133`). Never
  `/tmp`.
- The amended PL-4 instrument (`pl4/amended2.py`) is a scratch measurement artifact,
  not a proposed file: the four-row diff in §1.5 is the deliverable.
