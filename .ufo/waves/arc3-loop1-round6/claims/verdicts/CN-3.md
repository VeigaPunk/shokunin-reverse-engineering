# CN-3 — convergence verdict: the three delivered artifacts + peers

Seat CN-3, verdicts/convergence chain, wave `arc3-loop1-round6`, 2026-10-19.
Repo HEAD measured this session: `c625d5de57e045188b5ce8cd450a57b349f90785`
(`c625d5d`, records; work `58c3db7`). Gate `.ufo/gates/c1-census-v10.py`
sha256 `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`,
610 lines — **unchanged before and after this seat**. Scratch:
`/var/tmp/cn3-r6/` (never `/tmp` — EDQUOT). Write scope honored: only this
artifact and `claims/verdicts/CN-3/`; git read-only; no tracked file, gate,
corpus, PROVINCE/SKILL/SCORECARD or peer artifact was modified.

Every number below is my own measurement (rule #14). Peer artifacts are
**reconciliation objects, never evidence**; where I agree with a peer, that
agreement is stated as convergence, not as support. The wave tree was live
during this seat (peer artifacts mtimes spanned 15:57–17:04Z); `CN-3/peer-index.txt`
is a point-in-time index.

## 0. Rulings

| Claim | Delivered artifact | Ruling |
|---|---|---|
| **C1** operability — census Frontier blind spot | PL-4 `c1/PL-4/patch-v10-to-r10.diff` | **VERIFIED** against the frozen (a)/(b)/(c): applies to `80027570…`, clean tree PASS, frozen stale literal caught `FRONTIER-STALE`, 17/17 shared JSON keys identical. **One CORRECTED claim**: §6 residual 1's "insertions anywhere inside :73-162 are caught" is false — a +1-line insertion at :133 reads PASS. |
| **C2** coverage — one named corpus Unknown | EX-7 `c2/EX-7/entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md` + EVM map token | **VERIFIED / REPRODUCED**: live probe 15/15 with payloads byte-identical to the sealed envelope; independent byte walk confirms the fourth dispatcher class and the +43 embedding; overlay landing reads **85/85**, missing `[]`, dangling `[]`. **One CORRECTED transcription** before landing: entry line 28 says `73 736f6c63`; the bytes are `64 736f6c63`. |
| **C3** depth — queue-drain rule #15 | SC-3 §4 draft (+ RV-7's independent draft) | **VERIFIED numerically, CORRECTED twice**: identity 1,605 B / 23 lines / `763c44b5…`, landing 14→15 with 15/15 resolution at both revs; but `r4:34` must be `:29` (blocking), and the `r1:24` sentence needs the `:24` probe / `:31` embedding split (precision). **Land exactly one draft** — both measure 16 blocks; RV-7's draft is the citation-clean one. |

The three deliverables are **file-disjoint** (gate / corpus / SKILL) and can
land in one commit without coupling. The only real conflicts are alternatives,
not overlaps: three c1 patches for one gate file, and two c3 drafts for one
rule slot.

## 1. Baseline, first-hand (all before-state facts)

| # | Fact | Measurement | Verdict |
|---|---|---|---|
| 1 | HEAD / work | `git rev-parse HEAD` → `c625d5de…`; `git log --oneline -2` → `c625d5d` / `58c3db7` | REPRODUCED |
| 2 | Gate identity | `sha256sum` → `d0772ce8…`; 610 lines | REPRODUCED |
| 3 | Scoped sizes | PROVINCE 162, SKILL 390, SCORECARD 1696 (`wc -l`) | REPRODUCED |
| 4 | SCOPE blind spot | gate `:216-222` holds 7 PROVINCE rows (8-13, 15-26, 40-43, 44, 45-62, 64-71, 119-131); programmatic overlap check: `covering(73,93)=[]`, `covering(133,162)=[]`, `max_end=131` | VERIFIED |
| 5 | v10 clean run | `python3 .ufo/gates/c1-census-v10.py --root . --json` → PASS, `stale/ambiguous/undeclared/unresolved` all 0, counts `PROVINCE 162/6, SCORECARD 1696/9, SKILL 390/2`, G2 floor 17/14/3 | REPRODUCED |
| 6 | Command A before | SCORECARD.md:88-124 recipe at both revs → `{"knowledge_files": 84, "mapped": 84, "missing": [], "dangling": [], "rule_blocks": 14, "citation_resolved_rules": 14, "coverage_score": 10.0, "depth_score": 10.0}` | REPRODUCED |
| 7 | v10 is blind in the Frontier region | 15 fault trees (content staleness incl. a wrapped literal, silent bullet rewrites, truncation, section reflows, locus pin, append): **v10 PASSes 13/15**. It FAILs only `f-pin` (`undeclared=1`, a locus pin at :88) and `g-reflow82` (insertion above :119 shifts the DATED marker at :119 — existing G15 machinery, not Frontier grading) | VERIFIED / REPRODUCED |
| 8 | Historical residual record | `SCORECARD.md:1620` "the census gate cannot grade the Frontier region — named residual R1"; `:1631-1632` "Frontier region UNDECLARED — the repairs are clause-audited, not instrument-graded" | VERIFIED |

Full fault matrix: `CN-3/fault-matrix.txt` (15 trees × 4 instruments, exit +
verdict + classes). Baseline transcripts: `CN-3/command-A-baseline.txt`.

## 2. C1 — three patches for one file: identity, invariance, fault coverage

### 2.1 Identity and requirement (c)

| Patch | Patch bytes (sha256) | Applied instrument sha | Lines | Register shape | Clean run | Shared JSON |
|---|---|---|---|---|---|---|
| PL-4 | `3f94355c…` (`c1/PL-4/patch-v10-to-r10.diff`) | **`80027570…`** | 713 | `FRONTIER[]` 14 rows (intro + 13 bullets), REQUIRED + FORBIDDEN, no anchors | PASS | 17 shared keys, 0 diffs; additive `frontier_rows`/`frontier_errors` |
| PL-2 | `976188cc…` (`c1/PL-2/prior-attempt/c1-census-v10-r10.patch`) | **`2d7ee95b…`** | 705 | 2 SCOPE `FRONTIER` rows with section markers + 3-literal `FRONTIER_STALE` register | PASS | 17 shared keys, 0 diffs; additive `frontier_register`/`frontier_stale` |
| RV-3 | inline diff (`c1/RV-3/prior-attempt.md` §4; scratch copy `c9ab162e…`) | **`8e420679…`** | 712 | `FRONTIER_REGISTER` 13 rows, per-row anchor line + REQUIRED + FORBIDDEN + cite | PASS | 17 shared keys, 0 diffs; additive `frontier_rows`/`frontier_errors` |

**Artifact status at my final poll (17:04Z).** PL-2.md and RV-3.md were
rewritten during the wave as PL-4 verification artifacts; PL-2's original
design is archived byte-for-byte at `c1/PL-2/prior-attempt/` and RV-3's at
`c1/RV-3/prior-attempt.md` (the diff I re-extracted there is byte-identical
to my earlier scratch extraction, sha `c9ab162e…`). The c1 chain has therefore
already converged on PL-4; the comparison below audits the archived originals,
pinned by their applied-instrument shas.

All three preserve the 20-row base SCOPE table byte-identically (PL-2 *adds*
two rows after the last one; the other two add none). On the real repo root
all three read PASS with counts 162/1696/390.

**Text contract.** PL-4 and RV-3 leave the `VERDICT:` line byte-identical and
add one separate report line. PL-2 changes the verdict line itself
(`… unresolved=0 frontier=0`), which breaks an exact-line receipt grep; it
also reclassifies a pre-existing Frontier pin fault (v10 `undeclared=1` →
PL-2 `ambiguous=1` via the FRONTIER scope class). Both are measured design
differences, not clean-tree counter drift.

### 2.2 Frozen requirement (b) — the named falsifier

The frozen seed (`real solc/vyper-compiled bytecode untested` back into
`:91-93`) is caught by all three:

- PL-4: exit 1, `['FRONTIER-STALE']`, `PROVINCE.md:91-93 FORBIDDEN 'untested'
  matched` (+ REQUIRED-absent for the stripped solc/vyper tokens).
- PL-2: exit 1, `['FRONTIER-STALE']`, `PROVINCE.md:92 'solc/vyper-compiled
  bytecode untested' (r4 before-state, repaired in 40de383)`.
- RV-3: exit 1, `['FRONTIER-STALE','FRONTIER-UNATTESTED']`, line 93 hit plus
  required-claim absences.

A **line-wrapped** variant (`real solc/vyper-compiled` / `bytecode untested`)
is caught by PL-4 and RV-3 (single-token FORBIDDEN) but **PASSes PL-2**
(its literal is a line-local phrase). PL-4's FORBIDDEN-only arm (keep
solc/vyper tokens, add `untested`) fails with exactly one error — FORBIDDEN
works independently of the required floor.

### 2.3 Fault-coverage matrix (summarized; full in `CN-3/fault-matrix.txt`)

| fault arm | v10 | PL-4 | PL-2 | RV-3 |
|---|---|---|---|---|
| frozen literal at :91-93 | PASS | FAIL STALE | FAIL STALE | FAIL STALE+UNATTESTED |
| frozen literal, line-wrapped | PASS | FAIL STALE | **PASS** | FAIL STALE+UNATTESTED |
| stripped earned citations (:91-93; :135-138) | PASS | FAIL UNEVALUABLE | **PASS** | FAIL UNATTESTED |
| PROVINCE truncated to 161 lines | PASS | FAIL UNREADABLE+UNEVAL | FAIL UNREADABLE | FAIL UNATTESTED |
| +1 blank line before :133 (`### Round-4 frontier`) | PASS | **PASS** | FAIL scope_errors | FAIL ANCHOR |
| +1 blank line before :82 | FAIL (marker shift) | FAIL UNEVALUABLE | FAIL scope_errors | FAIL ANCHOR |
| stale pin `rea-agents@6.3.0` at :88 | FAIL undeclared=1 | FAIL undeclared=1 | FAIL ambiguous=1 | FAIL undeclared=1 |
| stale `~900s` wall form, one line, `arc2-r7` kept | PASS | **PASS** | FAIL STALE | **PASS** |
| cross-version stale bullet, `r12-02/r14-01` removed | PASS | FAIL UNEVALUABLE | FAIL STALE | **PASS** |
| stale bullet appended past :162 | PASS | PASS | PASS | PASS |

### 2.4 Findings (per item)

- **F-C1-1 (CORRECTED) — PL-4's reflow residual is too strong.** A +1-line
  insertion at :133 (blank before the post-unlock header) shifts every
  post-unlock row by one line; row 135-138 still contains `RISC-V` (at 136) and
  `r5-01` (at 138), so `frontier_check()` returns `[]` and the gate reads PASS
  exit 0. PL-4 §6.1 says such insertions fail REQUIRED-absent "measured via the
  seeded arms"; the arms it cites are citation-removal and truncation, not a
  pure insertion. Evidence: `CN-3/reflow-evidence.txt` (lines 133-140 + `[]`).
  Independently found by EX-2 item 16, EX-3 item 18, PL-1 §2.5, RV-1 §3 and
  VZ-4's revised poll.
- **F-C1-2 (measured limit) — PL-4 does not catch the other two measured stale
  literals.** A one-line `~900s internal session deadline` wall form that keeps
  `90 MB PE`/`arc2-r7` reads PASS (its only FORBIDDEN is `untested`). PL-4
  declares FORBIDDEN coverage "earned, not exhaustive" (§6.3), so this is a
  named limit, not a false claim — but it bounds what the register grades.
- **F-C1-3 (CORRECTED) — PL-2 has no positive floor.** Stripping all earned
  citations from :91-93 or :135-138 leaves PL-2 PASSing. Its register grades
  only literal reintroductions; a silent bullet rewrite is invisible. Its
  design does not claim otherwise, but the frozen axis ("staleness claims
  become gradable") is only partially met.
- **F-C1-4 (CORRECTED) — PL-2's literal match is line-local.** A wrapped frozen
  literal passes (measured); PL-1/EX-2 found the same for its wall entry. Any
  multi-word literal that can reflow is a fragile needle.
- **F-C1-5 (measured) — PL-2 changes two pre-existing contracts:** the exact
  `VERDICT:` line (adds `frontier=0`) and the class of a Frontier pin fault
  (`undeclared` → `ambiguous`). Both still FAIL closed; neither is a clean-tree
  counter change.
- **F-C1-6 (measured) — RV-3 has the best reflow discipline** (anchor line per
  row; 4/4 reflow arms fail `FRONTIER-ANCHOR`) and a positive floor, but only
  one FORBIDDEN literal: the wall and cross-version forms read PASS.
- **F-C1-7 (common residual) — all three PASS a stale bullet appended past
  :162.** All three declare this (past-the-bound append); it is not a
  PL-4-specific flaw.
- **F-C1-8 (requirement c, measured)** — all three are additive on
  `--json`: 17 shared keys with **zero** differing values, base SCOPE rows
  identical, clean counts identical. `CN-3/c1-identities.txt`.

### 2.5 Peer reconciliation (c1)

EX-2, EX-3, PL-1 and RV-1 each independently verified PL-4 and each found the
same reflow correction; PL-1/EX-2 additionally found PL-2's wall entry
line-wrap blindness and RV-3's cross-version miss. No peer reports a c1 defect
I did not measure, and I report none they did not. The peers differ only in
recommendation weight: EX-3 lands PL-4 as-is with the corrected residual;
PL-1 prefers PL-4 + a measured delta patch; EX-2 lands PL-4 + grafts
(anchors + the two PL-2 literals). VZ-4's revised poll also rules PL-4
REPRODUCED with the same correction. PL-2 and RV-3 themselves have since
retracted their competing designs in place and independently verify PL-4
(their current artifacts), so the chain's own convergence agrees with this
ruling.

### 2.6 C1 recommendation (single landing)

1. **Land PL-4** (`patch-v10-to-r10.diff` → instrument `80027570…`, 713
   lines). It is the artifact that meets the frozen letter and has the
   broadest measured catch set on the historical reverts (frozen literal incl.
   wrapped, stripped citations, truncation, cross-version required floor).
2. **Record the corrected residual in the landing receipt**: a +1-line reflow
   inside the post-unlock region is NOT detected by this register. Do not
   repeat §6.1's "insertions anywhere … are caught" sentence.
3. **Optional hardening, only if the integrator will take a new patch with a
   new identity**: add RV-3-style anchor lines (RV-3 measurement:
   `8e420679…`) and the two `FORBIDDEN` literals already earned in PL-2's
   register (`hits REA's ~900s internal session deadline`,
   `probe-refused since r2`). Re-run this matrix after the change; a grafted
   patch is a new artifact and must not inherit `80027570…`.
4. **Do not land PL-2 as-is** (no positive floor; line-local literals; verdict
   line change). Do not land two c1 patches — same file, same r10 label.

## 3. C2 — EX-7's viaIR entry

### 3.1 Re-derived, first-hand

- **Unknown is open at HEAD**: `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:33`
  and `…r4-evm-vyper-leg.md:28` both name "the `viaIR` pipeline"; no entry
  measures its dispatcher.
- **Live probe** (my run, `TMPDIR=/var/tmp/cn3-r6/tmp`):
  `npx -y rea-agents@6.4.0 inspect-evm-interface EX-7/out/viair-opt200/runtime.hex hex --format json`
  → exit 0, **15 functions**, all `dispatch:"abi"`, decoded
  `bytecode.sha256 2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a`,
  1,517 bytes. New evidence id `ev_71da9d37…` (path-dependent — the entry
  itself warns ids are path-sensitive; the sealed envelope was minted at
  `/var/tmp/ex07-r6/` as `ev_409e0442…`). Function payloads and CBOR metadata
  are **identical** to the sealed envelope.
- **Independent byte walk** (`CN-3/c2-probe-walk.txt`): prologue
  `60806040526004361015610022575b3615610018575f80fd`, guard with `ISZERO`
  targeting `0x0022`; **14 EQ legs** `DUP1 PUSH4 <sel> EQ PUSH2 <dst> JUMPI`
  at exactly 11-byte stride, selectors ascending, all dsts JUMPDEST
  (range 253–982); final **`PUSH4 ee02438e SUB PUSH2 0x000e JUMPI`** at pc 194
  (mark offset 204 = pc+10, dst 14 = guard JUMPDEST). Same shape in
  `viair-noopt` (dsts 208–273, guard target `0x001d`).
- **Pipeline control**: `std-opt200` (same source/optimizer, `viaIR` unset)
  has guard `60043610 61 00e7 57` **without** ISZERO, 15 EQ legs with
  non-uniform gaps {11,15,26} and no `SUB` leg — the legacy GT/EQ tree.
- **Creation embedding**: `creation.bin` 1,560 B `d85fdde9…` embeds the 1,517 B
  runtime at **+43** with 0 trailing bytes, 1 occurrence; `runtime.hex`
  decodes byte-identical to `runtime.bin`.
- **Selector set**: probe = `method-identifiers.json` (15) = planted K=15
  (`evidence/planted-K.json`, stage pre-compile/pre-probe); zero ERC-20
  collisions. ABI 17 entries / 15 functions, sha `63fcf52f…`;
  `method-identifiers.json` sha `c32e2ef2…`.
- **Entry digests** re-derived: runtime 1,517 B `2ec3f557…`; creation 1,560 B
  `d85fdde9…`; noopt 4,144 B `0cc6938c…`; std 1,921 B `c2ceabb1…` — all match
  the entry's claims.

### 3.2 Landing simulation (84 → 85)

Overlay of `corpus/knowledge/*.md` (85 files incl. the entry) + the EVM-row
token exactly as EX-7.md's patch text + the verbatim command-A algorithm:
`{"knowledge_files": 85, "mapped": 85, "missing": [], "dangling": [],
"coverage_score": 10.0}`; `rule_blocks`/`depth` untouched (14/14). Transcript:
`CN-3/command-A-overlay.txt`. This is a simulation, not the landed
measurement — the parent must re-measure after copying the file and token.

### 3.3 Correction and peer reconciliation

- **F-C2-1 (CORRECTED, blocking for the record) — entry line 28's CBOR hex.**
  Actual runtime tail bytes:
  `a2 64 69706673 58 22 <34B ipfs> 64 736f6c63 43 000825 00 33`.
  The entry transcribes `73 736f6c63`; the text-string header before `solc` is
  `0x64` (text(4)), not `0x73` (text(19)). The on-disk bytes are correct and
  the decode is correct; only the prose transcription is wrong. Fix before
  landing. EX-9 independently found the same; EX-7's own metadata claim is
  otherwise exact.
- **PUSH4 counts read consistently**: opt200 19 sites / 18 distinct
  (15 selectors + Panic `4e487b71` ×2 + two constants); noopt 17/16;
  control 22/19 (18 selector occurrences: 15 EQ + 3 GT pivots, + 4 constants).
  The entry's "control's 18 sites/15 distinct" is the selector-occurrence
  count, not total PUSH4 sites.
- **Peers**: EX-9 independently verified the entry (its own compile and walk)
  and found the same transcription defect. `c2/EX-6/` is evidence-only (no
  `EX-6.md`): duplicate staging of the same carrier experiment, not a
  competing claim. No peer contradicts any measured byte fact.

### 3.4 C2 recommendation

Land the entry + token after fixing line 28 (`73` → `64`). The command-A
after-state to verify post-landing is `85/85`, missing `[]`, dangling `[]`.
The entry's recheck path and pin (`rea-agents@6.4.0`) are correct and
reproduce 15/15 on this host.

## 4. C3 — two drafts for one rule slot

### 4.1 Identities and landing mechanics

| Draft | Bytes / lines | sha256 | Landing at `58c3db7` and `c625d5d` |
|---|---|---|---|
| SC-3 §4 (fenced block) | 1,605 B / 23 | `763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1` | before 14/14 → after **15/15**, depth 10.0 |
| RV-7 `rule15-bullet.md` | 1,565 B / 23 | `ccbc5cdbbefc86081393cd4d60ef9c85606c3dd1c98ed76d63520da1da0b67e7` | before 14/14 → after **15/15**, depth 10.0 |
| **both** | — | — | **16 blocks / 16 resolved** (duplicate rule; score still 10.0) |

Both parse as exactly one new `^- \*\*` block; every citation resolves
in-bounds at both revs. The metric cannot see duplication: landing both is
numerically invisible at depth 10.0. **Land exactly one.**

### 4.2 Citation-content audit and corrections

- **F-C3-1 (CORRECTED, blocking) — `r4:34` is the erratum header.**
  SC-3's §4 draft and §6 table cite
  `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:34` for "empty results
  do not prove absence of dispatch". Measured: `:34` is
  `## Erratum (arc3-loop1-round5 correctness sweep, append-only)`; the quoted
  limitation is at **`:29`** (the Limitations bullet). The citation resolves
  in-bounds either way (34 ≤ 63), so command A cannot see it. Fix `:34` → `:29`.
- **F-C3-2 (CORRECTED, precision) — the `r1:24` compound attribution.**
  SC-3's first sentence cites `r1:24` for "0 functions on blobs that
  byte-contain the full runtime". `r1:24` records the 0-function probe and says
  "Creation blobs carry no runtime dispatch table"; the embedding half is
  `r1:31`'s erratum. Re-point the two halves (`:24` probe, `:31` embedding).
  This is RV-6's F2 and SC-4's F-SC4-2, confirmed here.
- **F-C3-3 (VERIFIED) — the r3 erratum's `:24` pointer is dangling.**
  `git show c418be0:… | grep 'Creation blobs'` → no line;
  `40de383` → no line; `58c3db7` → line 41 only (the erratum quoting it).
  r3's line 24 is a RESULT row at every rev. The quoted sentence belongs to
  `r1:24` (corrected at `r1:31`). RV-7's draft avoids propagating it; SC-3's
  §6 evidence table repeats "r5 erratum correcting r3 `:24`". The rule text
  itself does not repeat the pointer, but the seat artifact does.
- All other SC-3 citations were read at the named lines and match content:
  `r1:24`, `r1:31`, `r3:41-51`, `r3:27`, `r4:17`, `r4:25`, `r4:39-46`,
  `QUALITY.md:21`. RV-7's six pattern citations were read at the named lines
  and match. Draft identities and line content: `CN-3/c3-drafts.txt`.

### 4.3 Peer reconciliation (c3)

Eight peers independently find `:34` → `:29` (EX-13, EX-14, EX-15, EX-16,
RV-5, RV-6, SC-2, SC-4) and several add the `r1:24` precision issue
(RV-6, SC-4; EX-15's E-F2). **One peer conflicts: RV-8 recommends landing
SC-3 verbatim and reports "8/8 content anchors hold"; its table lists `r4:34`
without measuring the line's content.** My measurement (and the eight peers')
shows `:34` is the erratum header. RV-8's recommendation is unsafe on that
point; its other numbers were not re-derived by this seat. EX-15 recommends
RV-7's bullet; SC-1 recommends a corrected variant or RV-7; SC-2/SC-4/EX-14/
EX-16/RV-5 supply corrected SC-3 texts. VZ-4's revised poll agrees with both
corrections.

**Field split on the replacement text.** The verdict seats split between two
zero-risk alternatives: RV-7's `ccbc5cdb…` (CN-2, EX-15, and this seat) and
SC-4's corrected SC-3 `a1bceb40…` (CN-4, VZ-3, CR-8). I verified RV-7's
identity and landing first-hand; I did not re-derive `a1bceb40…`, so I
recommend it only as a peer-reported alternative. Either is acceptable; the
non-negotiable is one text, never verbatim SC-3.

### 4.4 C3 recommendation (single landing)

1. **Land RV-7's bullet verbatim** (`ccbc5cdb…`, 1,565 B, 23 lines): it is
   citation-clean (neither F-C3-1 nor F-C3-2), avoids the r3 dangling pointer,
   and measures 15/15 at both revs. This is the smallest-risk landing.
2. **Acceptable alternative:** SC-3's text with both corrections applied
   (`:34`→`:29`; split `r1:24`/`:31`) and its identity re-derived after the
   edit. Any edit voids `763c44b5…`; do not land the original bytes.
3. **Do not land both drafts**, and do not follow RV-8's verbatim-SC-3
   recommendation. One rule slot, one rule.

## 5. Cross-chain convergence and combined landing

The three claims touch disjoint files, and the c2/c3 landings do not modify
PROVINCE.md, so PL-4's register needs no re-key. Measured combined after-state
on the overlay (`CN-3/command-A-overlay.txt`):

```
{"knowledge_files": 85, "mapped": 85, "missing": [], "dangling": [],
 "rule_blocks": 15, "citation_resolved_rules": 15,
 "coverage_score": 10.0, "depth_score": 10.0}
```

Landing order and receipts:

1. **c1**: apply PL-4's patch to `.ufo/gates/c1-census-v10.py`; verify
   `80027570…` / 713 lines; run clean PASS + the frozen-fault arm on the real
   tree; record post-edit identity in the landing receipt (not in the gate —
   the gate's own rule-#14 discipline), and record the corrected reflow
   residual.
2. **c2**: copy the entry to `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md`
   after the line-28 fix; append the token to `corpus/README.md`'s EVM row;
   re-measure command A → 85/85.
3. **c3**: append exactly one rule-15 bullet after `SKILL.md:255`; re-measure
   → 15/15.

No ordering coupling exists between them; a single commit is safe. The one
coupling worth stating in the LOG: the c1 landing receipt and the corrected
residual are one record, and the c3 rule's `r4:29` citation is only correct if
the corpus line numbers are unchanged (they are — c2 adds a file, it does not
edit r1/r3/r4).

## 6. Per-item verdict table

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | HEAD `c625d5d`, work `58c3db7`; gate `d0772ce8…`, 610 lines | REPRODUCED | §1 |
| 2 | SCOPE covers PROVINCE only 8-13/15-26/40-43/44/45-62/64-71/119-131; 73-93 + 133-162 undeclared | VERIFIED | gate :216-222; programmatic overlap `[]` |
| 3 | v10 clean PASS, counters 162/1696/390, floor 17/14/3 | REPRODUCED | §1 |
| 4 | v10 blind to Frontier content staleness | REPRODUCED | 13/15 fault trees PASS |
| 5 | Command A 84/84, 14/14, missing/dangling empty at both revs | REPRODUCED | `CN-3/command-A-baseline.txt` |
| 6 | PL-4 patch applies to `80027570…`, 713 lines | VERIFIED | `CN-3/c1-identities.txt` |
| 7 | PL-4 clean PASS; 17/17 shared JSON keys; base SCOPE intact; VERDICT byte-identical | VERIFIED | `CN-3/c1-identities.txt` |
| 8 | PL-4 catches the frozen stale literal and the FORBIDDEN-only variant | REPRODUCED | matrix |
| 9 | PL-4 §6.1 "insertions anywhere inside :73-162 are caught" | **CORRECTED** | +1 line at :133 → PASS; `CN-3/reflow-evidence.txt` |
| 10 | PL-4's register covers the other measured stale literals (`~900s` wall, `probe-refused since r2`) | **CORRECTED (limit)** | wall one-line PASS; its only FORBIDDEN is `untested` |
| 11 | PL-2 applies to `2d7ee95b…`; clean PASS; counters intact | VERIFIED | §2.1 |
| 12 | PL-2 has a positive floor / catches wrapped literals | **CORRECTED** | stripped citations PASS; wrapped frozen literal PASS |
| 13 | PL-2 keeps the exact VERDICT line and pre-existing pin class | **CORRECTED (measured difference)** | adds `frontier=0`; pin → ambiguous |
| 14 | RV-3 applies to `8e420679…`; clean PASS; reflow anchors work | VERIFIED | §2.1, matrix |
| 15 | RV-3 catches the wall / cross-version measured stale forms | **CORRECTED** | both PASS |
| 16 | All three PASS a stale bullet appended past :162 | REPRODUCED (common declared residual) | matrix |
| 17 | EX-7's entry: Unknown open at r3:33 / r4:28 | VERIFIED | §3.1 |
| 18 | EX-7 live probe 15/15, dispatch abi, decoded sha `2ec3f557…`, payloads identical to sealed envelope | REPRODUCED | `CN-3/c2-probe-walk.txt` |
| 19 | EX-7 dispatch walk: ISZERO guard, 14 EQ legs stride 11 ascending, SUB leg dst 14 at pc 194; control is GT/EQ | REPRODUCED | `CN-3/c2-probe-walk.txt` |
| 20 | EX-7 creation 1,560 B embeds runtime at +43, 0 trailing; hex == bin | REPRODUCED | `CN-3/c2-probe-walk.txt` |
| 21 | EX-7 selector set = methodIdentifiers = planted K=15; no ERC-20 collisions | REPRODUCED | `CN-3/c2-probe-walk.txt` |
| 22 | EX-7 line 28 CBOR transcription `73 736f6c63` | **CORRECTED** → actual `64 736f6c63` | `CN-3/c2-probe-walk.txt` |
| 23 | C2 landing 84 → 85, missing/dangling empty | REPRODUCED (overlay) | `CN-3/command-A-overlay.txt` |
| 24 | SC-3 draft identity 1,605 B / 23 lines / `763c44b5…` | REPRODUCED | `CN-3/c3-drafts.txt` |
| 25 | SC-3 landing 14 → 15, 15/15 at both revs | REPRODUCED | `CN-3/c3-drafts.txt` |
| 26 | SC-3 `r4:34` citation for the limitation quote | **CORRECTED** → `:29` | `CN-3/c3-drafts.txt` |
| 27 | SC-3 `r1:24` compound attribution | **CORRECTED (precision)** → split `:24`/`:31` | `CN-3/c3-drafts.txt` |
| 28 | r3 erratum's `:24` pointer is dangling (RV-7 F1) | VERIFIED | three-rev `git show` grep |
| 29 | RV-7 draft identity 1,565 B / 23 / `ccbc5cdb…`; landing 15/15 both revs | REPRODUCED | `CN-3/c3-drafts.txt` |
| 30 | Landing both drafts | REPRODUCED = 16 blocks/16 resolved — **do not** | `CN-3/c3-drafts.txt` |
| 31 | RV-8's "SC-3 verbatim, 8/8 anchors" | **CORRECTED (peer conflict)** | its own table lists `:34` without content check |
| 32 | Combined after-state 85/85 + 15/15, both scores 10.0 | REPRODUCED (overlay) | `CN-3/command-A-overlay.txt` |

## 7. What I did not do / residuals

- Did not land anything, patch the real gate, edit corpus/SKILL/PROVINCE/
  SCORECARD, or mutate git. Gate sha is unchanged (`d0772ce8…`); `git status`
  shows only the pre-existing `arc2-loop1-round10/C3.md` modification and the
  untracked wave tree.
- Did not run the c1 patches on the repo root *after* applying them (write
  scope); all r10 measurements are on scratch trees with byte-identical scoped
  files. The parent's landing run is the authoritative post-landing
  measurement.
- Did not re-run EX-7's 6.7.0 probe leg or the noopt probe; those rest on the
  sealed envelopes + EX-9's independent rerun, while I re-ran the primary
  6.4.0 opt200 leg and the creation leg, and byte-walked all three runtimes.
- Did not re-derive every peer number; peers are reconciliation objects only.
  `CN-3/peer-index.txt` is point-in-time — the wave tree was still receiving
  artifacts during this seat. PL-2's artifact moved to `prior-attempt/` mid-run;
  the bytes I measured are pinned by file sha `976188cc…` → instrument
  `2d7ee95b…`.
- Named residuals carried by the recommended landings: PL-4's reflow
  fail-open and the two unregistered literals; PL-2's absent positive floor
  and line-local literals; RV-3's two missing literals; all three's
  append-past-:162; EX-7's line-28 transcription until fixed; SC-3's two
  citation corrections unless RV-7's text is used instead.
- One peer seam remains open for the next round, not this one: the r3 entry's
  erratum quotes a dangling `:24` (F-C3-3). An append-only corpus erratum
  re-pointing it to `r1:24` is the honest fix; no seat in this wave owns a
  corpus write and the rule texts do not propagate it.

## 8. Evidence files (this seat's writes)

All under `.ufo/waves/arc3-loop1-round6/claims/verdicts/CN-3/`:

- `fault-matrix.txt` — 15 trees × 4 instruments (v10, PL-4, PL-2, RV-3),
  exit/verdict/classes.
- `c1-identities.txt` — patch bytes/applied shas/lines, JSON invariance,
  SCOPE base-row integrity, text-output diffs.
- `command-A-baseline.txt` — command A at both revs, fresh capture.
- `command-A-overlay.txt` — entry-only 85/85, entry+one-rule 85/85 + 15/15,
  both-drafts 16/16.
- `c2-probe-walk.txt` — live probe, selector equality, byte walks, creation
  embedding, CBOR actual-vs-transcribed, digests.
- `c3-drafts.txt` — draft identities, landing simulations, citation line
  content, r3 pointer check.
- `reflow-evidence.txt` — PL-4's +1-line insertion at :133 and its `[]`
  frontier result.
- `peer-index.txt` — point-in-time peer artifact list with one-line readings.
