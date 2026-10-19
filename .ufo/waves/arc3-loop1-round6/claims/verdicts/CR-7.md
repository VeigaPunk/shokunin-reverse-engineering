# CR-7 — verdicts/convergence: the three delivered artifacts re-derived first-hand, with landing ruling

Seat **CR-7**, chain **verdicts/convergence** (roster: `VZ-1..4, CN-1..4, CR-5..8`),
wave `arc3-loop1-round6`, 2026-10-19. Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
HEAD `c625d5de57e045188b5ce8cd450a57b349f90785` (records `c625d5d`; work `58c3db7`),
both re-derived this session (`git rev-parse HEAD`, `git log --oneline -2`).
Every number below is my own measurement from retained bytes, git objects, or a
live run; peer values are cited only as claims under audit (rule #14).
Scratch `/var/tmp/cr7-r6/` (never `/tmp`; TMPDIR `/var/tmp/cr7-r6/tmp`).
Write scope honored: only `claims/verdicts/CR-7.md` + `claims/verdicts/CR-7/`.
The live gate, PROVINCE.md, SKILL.md, SCORECARD.md, corpus, `.ufo/gates/` and
custody paths were never modified; git was read-only (`show`/`log`/`rev-parse`/
`status`/`ls-tree`).

## 0. Ruling ledger

| Claim | Delivered artifact | Ruling | Landing move |
|---|---|---|---|
| **C1 operability** (census Frontier blind spot) | PL-4 `patch-v10-to-r10.diff` | **VERIFIED** on frozen (a)(b)(c); one residual sentence **CORRECTED** (span absorption) | Apply PL-4's patch in place → `80027570…`, 713 lines. Optionally add PL-2 §7's two header rows. Do not land the prior PL-2/RV-3 designs. |
| **C2 coverage** (corpus Unknown) | EX-7 entry-draft + map token | **VERIFIED / REPRODUCED** end-to-end, including a fresh live 15/15 probe; one byte-text **CORRECTION** (CBOR `73`→`64`) plus four prose corrections (15 not 14 externals; `0c2eae8d` has no r3 hit; 46 not 42 evidence files; byte-14 router wording) | Copy the entry, append the token; apply the text corrections first. Command A → 85/85. |
| **C3 depth** (rule #15) | SC-3 rule-15 draft | **VERIFIED**; two content-anchor **CORRECTIONS** (`:34`→`:29` required; `r1:24` attachment optional) | Land exactly one: SC-3 corrected (`6967b1e3…`), CR-8's reflow (`a1bceb40…`), or RV-7 (`ccbc5cdb…`). |

Snapshot of the audited bytes (`CR-7/snapshot.txt`): PL-4.md `d0762a8d…`,
PL-4 patch `3f94355c…`, EX-7.md `509c9193…`, entry-draft `6e331882…`,
SC-3.md `ae489151…`. The three primary artifact files were last modified
12:57–13:33, before my audit; PL-2.md and RV-3.md were revised by their own
seats at 13:57–14:00 (both now verify PL-4 — see §5).

## 1. C1 — PL-4's r10 frontier-claim register

### 1.1 Before-state (re-derived)

- Gate `.ufo/gates/c1-census-v10.py`: sha256 `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`, 610 lines; working tree clean for it.
- SCOPE (`gate:216-222`) declares PROVINCE.md only at 8-13, 15-26, 40-43, 44, 45-62, 64-71, 119-131. No row covers 73-93 or 133-162 (`CR-7/c1-scope-coverage.txt`); `wc -l PROVINCE.md` = 162; `:73` = `## Frontier`, `:133` = `### Round-4 frontier (post-unlock)`.
- v10 reads PASS on a scratch tree carrying the retracted literal back inside :91-93 (`CR-7/c1-arms.txt`, `v10-seeded`: `VERDICT: PASS … exit 0`) while the clean tree also reads PASS. The blind spot is real.

### 1.2 Patch round-trip

Applied `PL-4/patch-v10-to-r10.diff` (`patch -p0`) to a pristine copy made with
`git show HEAD:.ufo/gates/c1-census-v10.py`:

```
8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca  713 lines  ast.parse OK
```

The built instrument shipped at `PL-4/c1-census-v10-r10.py` has the **same**
sha256. `PL-4.md`'s claimed identity is reproduced. (`CR-7/c1-roundtrip.txt`.)

### 1.3 Frozen clauses — measured on real and scratch trees

| arm | tree | instrument | result | exit |
|---|---|---|---|---|
| clean, **real repo root** | HEAD | r10 | `FRONTIER register (G21): 14 rows asserted, errors: []`; `VERDICT: PASS (0/0/0/0)` | 0 |
| clean, scratch | byte-copy of HEAD | v10 | PASS 0/0/0/0 | 0 |
| frozen seed (:91-93 stale literal) | scratch | v10 | **PASS 0/0/0/0** (blind) | 0 |
| frozen seed | scratch | r10 | **FAIL**; `DECLARED FAIL CLASSES: ['FRONTIER-STALE']`; error names `FORBIDDEN 'untested' matched 'untested'` | 1 |
| isolated FORBIDDEN (earning tokens kept, "untested" added) | scratch | r10 | FAIL; **exactly one** error: `PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)` | 1 |
| earning tokens stripped | scratch | r10 | FAIL; `FRONTIER-UNEVALUABLE` (3 REQUIRED-absent errors) | 1 |
| PROVINCE truncated to 161 lines | scratch | r10 | FAIL; `UNREADABLE` + `FRONTIER-UNEVALUABLE` | 1 |
| instrument-visible stale pin at :88 | scratch | v10 / r10 | both FAIL `undeclared=1`; r10 register errors `[]` (pre-existing class untouched) | 1 |

Transcripts: `CR-7/c1-arms.txt`, `CR-7/c1-r10-real-root.txt`,
`CR-7/c1-v10-real-root.txt`. On the real root, the **only** text delta between
v10 and r10 is the added line `FRONTIER register (G21): 14 rows asserted,
errors: []`.

Counter integrity (requirement c): `--json` on the clean tree gives **17 shared
keys, zero value mismatches**; r10 adds only `frontier_errors` and
`frontier_rows`; `counts` and `current_ok_per_file` are identical
(`PROVINCE.md` 17, `SCORECARD.md` 14, `SKILL.md` 3). `CR-7/c1-json-invariance.txt`.

Register coverage: the 14 rows cover all 13 Frontier bullets (5 at :82-93,
8 at :135-162) plus the :75-80 intro; no non-blank, non-header line in
73-93/133-162 is uncovered (`CR-7/c1-scope-coverage.txt`; §1.4). Requirement
(a), (b), (c) all hold first-hand.

### 1.4 CORRECTION to PL-4 §6.1 (behavior unchanged; prose wrong)

PL-4's residual #1 says insertions inside `:132-162` are caught because they
shift register spans into REQUIRED-absent. I measured four one-line structural
edits on a scratch copy of the patched r10, all **PASS exit 0, 14 rows,
errors []**:

- blank line inserted before `### Round-4 frontier` (before :133);
- blank line inserted at :134 (inside the section);
- blank line inserted at :150 (between bullets);
- `### Round-4 frontier (post-unlock)` renamed at :133.

Cause: a uniform +1 shift moves each span and its REQUIRED text together, so
`re.search` inside the shifted span still matches; the section headers are not
registered, so a rename is invisible. This does **not** void the frozen
falsifiable (the FORBIDDEN reintroduction still fails, measured), but the
residual prose overstates coverage. PL-2 and RV-3 independently reached the
same correction (`PL-2.md` §0/§5; current `RV-3.md` §0). Optional hardening,
tested by PL-2 on scratch and not part of PL-4's patch: add two rows
`("PROVINCE.md", 73, 73, [r"^## Frontier$"], [])` and
`("PROVINCE.md", 133, 133, [r"^### Round-4 frontier \(post-unlock\)$"], [])`.
I did not re-test that hardening; it is offered, not required.

### 1.5 Ruling

Land **PL-4's patch** (`80027570…`). It is the only c1 design still offered as
a landing candidate: PL-2 and RV-3 have revised their artifacts into
verifications of PL-4 (their prior designs are preserved under
`PL-2/prior-attempt/` and in RV-3 history — my audits of those are in §5).
The prior PL-2 design is narrower (3 retracted literals, no per-bullet
positive floor) and should not land standalone. The frozen claim is met.

## 2. C2 — EX-7's viaIR dispatch entry

### 2.1 Before-state and Unknown provenance

Command A (SCORECARD.md:88-124 recipe, verbatim) at `c625d5d`:
`{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
"depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [],
"rule_blocks": 14}` (`CR-7/c2-commandA-before.txt`). The named Unknown is live
at `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:33` ("the
`viaIR` pipeline") and `...r4-evm-vyper-leg.md:28` (same, plus the optimizer
forms).

### 2.2 Retained bytes (re-hashed)

| leg | runtime | creation |
|---|---|---|
| viair-opt200 | 1,517 B `2ec3f557…` | 1,560 B `d85fdde9…` |
| viair-noopt | 4,144 B `0cc6938c…` | 4,318 B `f1125049…` |
| std-opt200 control | 1,921 B `c2ceabb1…` | 1,966 B `4541fd49…` |

ABI sha `63fcf52f…` and method-identifiers sha `c32e2ef2…` are byte-identical
across all three legs (17 ABI entries = 15 functions + constructor + `receive`;
15 method IDs). Planted K=15 was recorded pre-compile; the pre-fix
`planted-K.preact.json` has the identical selector set. I re-derived four
selectors with `js-sha3` from the receipted solc prefix:
`deposit()`→`d0e30db0`, `mark(bytes32)`→`ee02438e`,
`scale(uint256,uint256)`→`6e69f38c`, control
`transfer(address,uint256)`→`a9059cbb`.

### 2.3 Sealed envelopes and a fresh live probe

Seven sealed envelopes (`CR-7/c2-probe-envelopes.txt`): five real legs are
**15/15, `dispatch:"abi"` ×15**, decoded `bytecode.sha256` equal to the leg's
runtime file sha; the raw-on-hex-text trap and the creation probe are
parsed-and-empty (0 functions) with decoded shas equal to the hex *text* file
(`19838d66…`) and the creation bin (`d85fdde9…`) respectively.

I did not stop at the envelopes. Fresh run this seat:

```
TMPDIR=/var/tmp/cr7-r6/tmp npx -y rea-agents@6.4.0 inspect-evm-interface \
  .../EX-7/out/viair-opt200/runtime.hex hex --format json
→ exit 0, 15 functions, dispatch "abi" ×15, decoded sha 2ec3f557…, 1,517 B,
  new evidence id ev_71da9d37… (path-sensitive id domain, as the entry says)
```

Raw envelope retained at `CR-7/c2-live-probe-71da9d37.json`.

### 2.4 Independent byte walk (my decoder, not EX-7's script)

`CR-7/c2-bytewalk.txt`:

- viair-opt200: head `6080604052 60043610 15 61<0022> 57 5b 3615 61<0018> 57
  5f80fd 5b … 5f3560e01c`; **14 EQ legs** at pcs 41–184, stride **[11]×13**,
  selectors strictly ascending, every EQ dst a JUMPDEST; final leg at pc 194 is
  **`PUSH4 ee02438e SUB` (0x03)** `PUSH2 0x000e JUMPI` (dst 14, the guard
  JUMPDEST). This is a fourth compare-tree class.
- Probe offsets vs my raw expectation: all 15 selectors present, **zero offset
  mismatches** — 14 offsets equal their EQ `PUSH2` dst; `mark` = push4_pc+10 =
  204, not a JUMPDEST.
- viair-noopt: same 14 EQ legs/selectors at the same pcs; eq dsts 208–273; SUB
  leg still pc 194. Nuance: the literal `5f3560e01c` is **absent** from noopt's
  bytes (the dispatch is reached by a jump); the shared shape is the compare
  tree, which is exactly the entry's own thesis ("the prologue does not
  identify the pipeline, the compare tree does"). No false claim, but the
  landed text should not be read as "same prologue bytes".
- std-opt200 control: 15 EQ + 3 GT legs; GT pivots `6e69f38c` (pc 19),
  `90ab171e` (pc 30), `3f4ba83a` (pc 137); EQ strides 11/15/26, not sorted →
  the r3 binary-search class, same source/optimizer, `viaIR` unset.
- PUSH4 census: opt200 19 sites = 15 selectors + `4e487b71`×2, `0c2eae8d`,
  `3c3332b9`; noopt 17 = 15 + `4e487b71`×2; std 22 = 18 selector sites
  (3 duplicated pivots) + the four non-selector constants. Matches the entry.
- Trailer: `… 64 736f6c63 43 000825 00 33` (CBOR map, `ipfs` 34-byte multihash,
  `solc` 0.8.37) — see §2.6 for the one text fix.
- Mutability: 14/15 agree with ABI; the one delta is
  `scale(uint256,uint256)` `pure`→`view`. The probe reports `payable` only for
  `deposit()`, which the ABI also declares payable — zero *spurious* payable
  reads.
- Creation embedding: the 1,517 B runtime occurs exactly once at **+43** in the
  1,560 B creation, 0 trailing bytes.

### 2.5 Landing projection (scratch overlay)

Entry + README EVM-row token overlaid on a copy of HEAD's corpus, exact
command-A logic: `{"knowledge_files": 85, "mapped": 85, "missing": [],
"dangling": [], "coverage_score": 10.0, "depth_score": 10.0,
"rule_blocks": 14}` (`CR-7/c2-landing-simulation.txt`). The frozen falsifiable
84→85 is demonstrated; the real-tree measurement remains the parent's
post-landing step.

### 2.6 CORRECTION before landing (byte text, not byte claims)

Entry line 28 writes the CBOR trailer as `… 73 736f6c63 43 000825 00 33`.
The actual runtime bytes are `64 736f6c63` (`64` = CBOR text(4), then "solc");
`73 736f6c63` does not occur in the runtime. Measured:
`bytes.fromhex('64736f6c63') in runtime == True`,
`bytes.fromhex('73736f6c63') in runtime == False`. Fix the token to
`64 736f6c63` (and let the ipfs hash end at `…4945d`, not `…4945d64`) before
landing. CR-5, CR-8 and CN-4 independently caught the same byte; this seat
confirms it from the raw carrier. No function-count, selector, offset or
coverage number is affected.

Four further pre-landing **prose** corrections, each confirmed first-hand
(EX-6.md landed at 14:02 as an independent verifier and raised them; I
re-measured them rather than quoting):

1. Entry line 16 says "14 explicit external functions + `receive()`". The
   source declares **15** functions (`grep -cE '^\s*function '` = 15) and the
   ABI is `{function:15, constructor:1, receive:1}`; the same sentence's
   mutability census already sums to 15 (view 7 + pure 1 + nonpayable 6 +
   payable 1). Say "15 explicit external functions + `receive()`".
2. Entry line 25 says `3c3332b9`/`0c2eae8d` "also appear in the r3 VaultB
   census". Measured: `3c3332b9` is at
   `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:26`;
   `0c2eae8d` has **no** hit anywhere under `corpus/`. Drop that half or cite
   this entry's own byte walk.
3. `EX-7.md`'s custody statement says "42 files"; the tree holds **46** (1 src,
   5 scripts, 8 evidence, 24 out, 7 probe, 1 entry-draft). State 46 or drop the
   count.
4. Entry line 22 calls byte 14 "the small-calldata revert path". Bytes
   `[14:25] = 5b 36 15 61 0018 57 5f 80 fd 5b` and dst 24 is a JUMPDEST:
   zero calldata routes to the receive trampoline at 24, 1-3 bytes revert, and
   a selector mismatch jumps back to 14 and reverts. The precise wording is
   "small-calldata router (receive / revert / mismatch)" — the entry's
   "revert path" is incomplete, not false.

Transcript for all four: `CR-7/c2-prose-corrections.txt`.

**C2 ruling: VERIFIED / REPRODUCED; land the entry + token after the
one-token CBOR fix and the four prose fixes.**

## 3. C3 — SC-3's rule #15

### 3.1 Draft identity and landing

Extracted the §4 fenced block from `SC-3.md` byte-for-byte:
**1,605 B, 23 lines, sha256 `763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1`**
(`CR-7/c3-identity-and-citation.txt`). Appending it to the craft section
extracted from `git show <rev>:SKILL.md` and running command A's exact
rule-split + citation-resolution logic:

| rev | before | after |
|---|---|---|
| `c625d5d` | 14 blocks, 14/14 resolved | **15 blocks, 15/15 resolved** |
| `58c3db7` | 14 blocks, 14/14 resolved | **15 blocks, 15/15 resolved** |

The new rule parses as exactly one `- **` block, is the 15th/last, and its 8
`corpus/knowledge/` refs all resolve in bounds. `CR-7/c3-landing-simulation.txt`.

### 3.2 Corrections (content anchors)

1. **Required:** `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:34` is
   cited for "empty results do not prove absence of dispatch". Measured: the
   quote is at **:29** (Limitations bullet); **:34** is the erratum section
   header. The citation still resolves under command A (34 ≤ 63), so the numbers
   do not move, but the landed rule would mispoint. VZ-4, CR-6, CR-8, CN-2 and
   CN-4 independently reached the same correction.
   Minimal fixed draft (`:34`→`:29`): **1,605 B, 23 lines, sha256
   `6967b1e3e7fbdb43492e191426399c0311ab3bf85ee307f1a181a3edd235511e`**; lands
   15/15 at both revs.
2. **Optional wording:** the first sentence cites `r1…:24` while saying "blobs
   that byte-contain the full runtime". r1:24 is the 0-functions observation
   and even carries the later-corrected "creation blobs carry no runtime
   dispatch table" sentence; the byte-containment half is measured at r1:31
   (also cited later in the rule). CR-8's reflowed variant
   (`rule15-SC-4-recommended.txt`, sha `a1bceb40…`) moves the citation behind
   "0 functions"; I simulated it: 15/15 at both revs. Not required for
   command-A resolution, but the clearer text.
3. Precision (not a defect): "zero payable-reads" means zero *spurious*
   payable reads; only `deposit()` is payable and the ABI agrees (CR-6's note).

### 3.3 Alternatives and the F1 finding

RV-7's independent draft (`rule15-bullet.md`, 1,565 B, sha `ccbc5cdb…`) also
lands 15/15 at both revs and avoids the `:34` mis-citation. RV-7's F1 is
confirmed first-hand: `git show c418be0:…r3… | grep -c 'Creation blobs carry
no runtime dispatch table'` = **0** at the round-3 landing; the sentence appears
in the r3 entry only from `58c3db7` (the round-5 erratum itself) — it is r1:24's
sentence, so the r3 erratum's `:24` pointer is an attribution error (byte facts
in that erratum are true).

**C3 ruling: VERIFIED with the required `:34`→`:29` correction. Land exactly
one of SC-3-corrected (`6967b1e3…`), CR-8's reflow (`a1bceb40…`), or RV-7
(`ccbc5cdb…`). Do not land two — the craft section would read 16 rules.**

## 4. Combined landing expectation

Overlaying c2 (entry + token) and c3 (corrected rule) on HEAD's corpus and
SKILL.md, command-A logic returns:

```json
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 85, "mapped": 85, "missing": [],
 "rule_blocks": 15}
```

(`CR-7/combined-landing-simulation.txt`.) c1 does not interact with command A
(the gate reads the tree, it is not a knowledge file); its expected post-landing
run is `VERDICT: PASS`, `FRONTIER register (G21): 14 rows asserted, errors: []`,
exit 0.

## 5. Peer reconciliation (current wave state)

- **PL-2 and RV-3 have revised themselves into verifications of PL-4**
  (`PL-2.md` sha `38f7c38d…`, `RV-3.md` sha `105a7c3a…`), both recommending
  PL-4. Their earlier competing designs are preserved (`PL-2/prior-attempt/`,
  patch `2d7ee95b…`) or historical (RV-3's applied gate `8e420679…`, 13 rows,
  FRONTIER-ANCHOR/UNATTESTED/STALE). My audits of those prior designs:
  PL-2-prior clean PASS + frozen seed caught, but a 3-literal register with no
  per-bullet floor; RV-3-prior clean PASS (13 rows), seeded/truncated arms
  FAIL with named classes. Neither is a landing candidate now.
- **Their edge correction is confirmed** by my four one-line edge tests (§1.4).
- **EX-6.md** landed at 14:02, after my earlier poll, as an **independent
  verification of EX-7** (not a competing entry). Its four prose corrections
  are confirmed by my re-measurements (§2.6). Its own independent carrier
  (different source sha `5684069e…`, 12 functions) compiles the same fourth
  class: 11 EQ legs + 1 SUB (`f43cc773`, dst 14), 0 GT; viair-nopt 3,039 B
  same chain. This corroborates EX-7 on a second carrier. Caveat: EX-6's
  row-12 CBOR prose repeats the `73"solc"` error; I rely on the raw bytes
  (`64 736f6c63`), not that prose.
- **RV-7** is a complete c3 alternative; its F1 is confirmed (§3.3).
- **VZ-4** is point-in-time (13:14 poll): its C1/C2/C3 PENDING items are now
  resolved by the three artifacts; its `:34`→`:29` correction is confirmed.
  Two cosmetic corrections: its HEAD sha is 39 hex chars (actual
  `…b349f90785`), and its EX-6 viaIR characterization ("no selector decode in
  the prologue at all") is imprecise — EX-6's viair-opt200 carries
  `5f3560e01c` and its first EQ leg is at pc 182.
- **Verdict-seat peers** CR-5, CR-6, CR-8, CN-2, CN-4 are present at the final
  snapshot and align on the same three rulings (land PL-4; EX-7 with the CBOR
  and prose fixes; SC-3 with `:34`→`:29`, or RV-7). CR-5 independently reports both the
  CBOR `73`→`64` correction and the one-line-reflow gap. I read their headline
  rulings, not their full texts; my own re-derivations stand on the evidence
  cited above. `CR-7/peer-reconciliation.txt` has the granular notes.

## 6. Landing recipe for the parent

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin

# c1 — apply PL-4's in-place patch, then re-run clean and seeded arms
patch .ufo/gates/c1-census-v10.py < \
  .ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum .ufo/gates/c1-census-v10.py        # expect 80027570…, 713 lines
python3 .ufo/gates/c1-census-v10.py --quiet  # expect exit 0, PASS, 14 rows, []
# (optional) add PL-2 §7's two header rows to FRONTIER[], then re-run.

# c2 — land the entry and token, after the one-token CBOR text fix
#   in the draft: s/73 736f6c63/64 736f6c63/ (hash span ends …4945d)
cp .ufo/waves/arc3-loop1-round6/claims/c2/EX-7/entry-draft/\
2026-10-19-arc3-r6-viair-dispatch-shape.md corpus/knowledge/
# apply the EVM-row patch printed in EX-7.md §3
#   (append `2026-10-19-arc3-r6-viair-dispatch-shape` to corpus/README.md:38)

# c3 — land ONE corrected rule after the rule-#14 bullet (SKILL.md:255)
#   SC-3 with :34→:29  -> sha 6967b1e3… (1,605 B / 23 lines)
#   or CR-8 reflow      -> sha a1bceb40…
#   or RV-7            -> sha ccbc5cdb… (1,565 B)

# measure: run the SCORECARD.md:88-124 recipe verbatim with REV=c625d5d.
# expected: knowledge_files 85, mapped 85, missing [], dangling [],
#           rule_blocks 15, citation_resolved_rules 15,
#           coverage_score 10.0, depth_score 10.0
```

Post-landing, record the new gate and entry/rule identities in the landing
receipt, not inline (the gate's own rule-#14 discipline). For c3, the draft's
self-identity line must be re-derived after the citation fix — `6967b1e3…` for
the minimal fix, `a1bceb40…` for CR-8's reflow, `ccbc5cdb…` for RV-7.

## 7. Per-item verdict table

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | HEAD `c625d5d` / work `58c3db7` | VERIFIED | `git rev-parse`/`log`; `CR-7/c1-roundtrip.txt` |
| 2 | Gate sha `d0772ce8…`, 610 lines, unchanged | VERIFIED | `sha256sum`, status clean |
| 3 | SCOPE PROVINCE rows exactly 7; 73-93 + 133-162 UNDECLARED | VERIFIED | `CR-7/c1-scope-coverage.txt`; gate :216-222 |
| 4 | v10 blind to the :91-93 stale literal | REPRODUCED | `CR-7/c1-arms.txt` v10-seeded PASS |
| 5 | PL-4 patch round-trip → `80027570…`, 713 lines | VERIFIED | `patch -p0`; ast OK; built file same sha |
| 6 | r10 clean PASS on real root, 14 rows, 0 errors | REPRODUCED | `CR-7/c1-r10-real-root.txt` |
| 7 | r10 catches frozen seed as FRONTIER-STALE | REPRODUCED | seeded arm, exit 1 |
| 8 | r10 catches isolated FORBIDDEN (one error) / required-strip / truncation | REPRODUCED | `CR-7/c1-arms.txt` |
| 9 | Existing SCOPE rows/counters intact | REPRODUCED | 17 shared JSON keys, 0 mismatch; +2 keys |
| 10 | Register covers all 13 bullets + intro | VERIFIED | `CR-7/c1-scope-coverage.txt` span map |
| 11 | PL-4 §6.1 insertion-coverage claim | **CORRECTED** | 4 edge edits PASS; span absorption |
| 12 | Command A before: 84/84, 14/14, missing/dangling [] | REPRODUCED | `CR-7/c2-commandA-before.txt` |
| 13 | viaIR Unknown open at r3:33 / r4:28 | VERIFIED | cited lines read |
| 14 | Runtime/creation sizes+shas, ABI/method-id identity | REPRODUCED | re-hashed; `CR-7/c2-bytewalk.txt` |
| 15 | 15/15 K/K on all real probe legs | REPRODUCED (envelopes) + **live re-probe 15/15** | 7 envelopes; `ev_71da9d37…` |
| 16 | Fourth dispatcher class (14 EQ stride 11 sorted + SUB leg) | VERIFIED | my raw walk; offsets all match |
| 17 | std control is the legacy GT/EQ binary search | VERIFIED | 15 EQ + 3 GT pivots |
| 18 | Traps parsed-and-empty; creation embedding +43 | REPRODUCED | trap/creation envelopes + `bytes.find` |
| 19 | Mutability 14/15, `scale` pure→view | REPRODUCED | probe vs ABI |
| 20 | Entry+token landing 85/85 | REPRODUCED (scratch overlay) | `CR-7/c2-landing-simulation.txt` |
| 21 | CBOR trailer token `73 736f6c63` | **CORRECTED** → `64 736f6c63` | byte search; `CR-7/c2-bytewalk.txt` |
| 21a | Entry prose: 14 vs 15 externals; `0c2eae8d` r3 cross-ref; 42 vs 46 files; byte-14 router | **CORRECTED** (4 items, §2.6) | source/ABI count; corpus grep; file count; bytes `[14:32]` |
| 22 | SC-3 draft identity 1,605 B / 23 lines / `763c44b5…` | REPRODUCED | `CR-7/c3-identity-and-citation.txt` |
| 23 | SC-3 landing 14→15, 15/15 at both revs | REPRODUCED | `CR-7/c3-landing-simulation.txt` |
| 24 | SC-3 `r4…:34` citation | **CORRECTED** → `:29`; fixed sha `6967b1e3…` | grep `:29`; identity |
| 25 | SC-3 `r1:24` attached to containment | CORRECTED (optional wording; `a1bceb40…` variant 15/15) | clause/citation check |
| 26 | RV-7 alternative landing / F1 | REPRODUCED / VERIFIED | 15/15; r3 history 0→1 hits |
| 27 | Combined c2+c3 landing 85/85, 15/15 | REPRODUCED | `CR-7/combined-landing-simulation.txt` |
| 28 | Peer designs PL-2-prior / RV-3-prior | REPRODUCED as instruments, not landing candidates | `CR-7/c1-roundtrip.txt`, `c1-json-invariance.txt` |

## 8. Limits and what I did not do

- Did not modify the gate, corpus, PROVINCE.md, SKILL.md, SCORECARD.md, LOG.md,
  `.ufo/gates/` or any tracked file; no git mutation.
- Did not recompile the three c2 legs (CR-6 reports byte-identical recompiles);
  I verified retained bytes, ABI/method IDs, all sealed envelopes, and one
  fresh live probe.
- Did not re-run every PL-4 arm (six trees); I ran clean (real + scratch),
  frozen seed, isolated forbidden, required-strip, truncation, stale-pin
  boundary, plus four structural edge edits.
- Did not test the optional two-row header hardening end-to-end.
- Verified EX-6's four prose corrections against the source, ABI, corpus and
  raw bytes, but did not recompile EX-6's independent carriers (`RelayDesk`,
  `RelayDeskFb`); its class corroboration is read from its retained bytes, not
  re-derived.
- Did not audit peer verdict artifacts (CR-5/CR-6/CR-8/CN-2/CN-4) beyond their
  headline rulings; their detailed transcripts are their own evidence.
- The after-state numbers for c1/c2/c3 are scratch-overlay measurements; the
  real-tree post-landing measurement is the parent's move.
