# CN-2 — arc3-loop1-round6 convergence verdict

Seat CN-2, verdicts/convergence chain, wave `arc3-loop1-round6`, 2026-10-19.
Repo HEAD `c625d5de57e045188b5ce8cd450a57b349f90785` (records) / work `58c3db7`
— both re-derived first-hand. Every number below is my own measurement this
seat (lane rule #14); peer artifacts are compared only after re-derivation.
Scratch `/var/tmp/cn2-r6/` (never `/tmp`). Write scope honored: only
`claims/verdicts/CN-2.md` + `claims/verdicts/CN-2/`; git read-only; gate,
PROVINCE.md, SKILL.md, SCORECARD.md, corpus untouched.

## Summary

| Claim | Ruling |
|---|---|
| **C1 operability** (census Frontier blind spot) | Before-state **VERIFIED**. Three in-place `r10` patches were delivered and are mutually exclusive; the chain has since **converged on PL-4** — PL-2's current artifact and RV-3's current artifact both explicitly endorse landing PL-4. PL-4 **VERIFIED** on all three frozen sub-claims (round-trip `80027570…`, clean PASS, seeded FAIL `FRONTIER-STALE`, 17/17 shared JSON keys equal; G19 truncation closure). Measured residual limits: PL-4's span-based register is blind to a pure ±1-line reflow (blank line before `:133` → PASS) and to the two other `40de383` stale literals (`~900s internal session deadline` at `:139-144`, `probe-refused since r2` at `:157-160` → PASS). RV-3 **VERIFIED** as an alternative (`8e420679…`, per-bullet anchors, catches the reflow); PL-2's *prior* design (`2d7ee95b…`, now archived under `prior-attempt/`) is **incomplete** — a stripped bullet reads PASS. **Recommendation: land PL-4 as-is** (frozen falsifiable met, chain consensus); optional measured hardenings in §2.5 (CN-4 two-literal amendment, PL-2 two header rows, the combined 4-row set at sha `6f8f3fe8…`, PL-1's 16-row anchor delta at `7724adcc…`). |
| **C2 coverage** (corpus Unknown) | **REPRODUCED end-to-end.** Command A 84/84 before; EX-7's viaIR entry drafts a fourth dispatcher class whose retained bytes I re-walked (14 EQ legs at stride 11 + `SUB`-terminated 15th leg), whose live 6.4.0 re-probe I ran (**15/15 `abi`**, decoded sha `2ec3f557…`), and whose landing overlay reads **85/85, missing [], dangling []**. EX-6's independent carrier (12 functions) shows the same class (11 EQ + `SUB` at dst 14). **Ready to land.** |
| **C3 depth** (rule #15) | **REPRODUCED with two CORRECTIONS to SC-3.** SC-3's draft identity reproduces byte-exact (1,605 B / 23 lines / `763c44b5…`) and simulates 14→15 with 15/15 resolved. Correction 1: `r4…md:34` is a content mis-citation — the quoted limitation lives at `:29`; `:34` is the erratum header (`:34`→`:29` alone gives sha `6967b1e3…`). Correction 2: the first clause cites `r1…md:24` for "blobs that byte-contain the full runtime", but r1 `:24` denies containment; `:31` carries it (my minimal `:24`→`:31` repoint gives sha `1a66dd55…`; CR-8's combined bytes `a1bceb40…` come from a different exact edit and are not reproduced). RV-7's draft (1,565 B / `ccbc5cdb…`) is content-clean as written and also simulates 15/15. **Land exactly one; RV-7 verbatim is the zero-edit path, SC-3 only with both pointer fixes and a re-derived identity.** |

## 1. Base re-derivations (first-hand)

| # | Fact | My measurement | Verdict |
|---|---|---|---|
| 1 | HEAD records `c625d5d`, work `58c3db7` | `git rev-parse HEAD` → `c625d5de57e0…`; `git log --oneline -5` shows `c625d5d … (measured at work commit 58c3db7)` | REPRODUCED |
| 2 | Gate at `.ufo/gates/c1-census-v10.py` | sha256 `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`, 610 lines; unchanged throughout my work | REPRODUCED |
| 3 | Scoped file sizes | `wc -l` → PROVINCE.md 162, SKILL.md 390, SCORECARD.md 1696 | REPRODUCED |
| 4 | v10 clean baseline | `python3 .ufo/gates/c1-census-v10.py --quiet` → `PROVINCE.md loci=6`, `SCORECARD.md loci=9`, `SKILL.md loci=2`; `G2 … PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3`; `VERDICT: PASS (0/0/0/0)` exit 0 | REPRODUCED |
| 5 | Command A before | exact SCORECARD.md:88-124 recipe at both revs → `knowledge_files 84, mapped 84, missing [], dangling [], rule_blocks 14, citation_resolved_rules 14, coverage 10.0, depth 10.0` (`/var/tmp/cn2-r6/cmdA/before.txt`) | REPRODUCED |
| 6 | SCOPE covers PROVINCE only 8-13/15-26/40-43/44/45-62/64-71/119-131 | gate `:216-222` read; no row reaches 73-93 or 133-162 | VERIFIED |
| 7 | Frontier region = 73-93 + 133-162 | PROVINCE.md `:73 ## Frontier`, `:133 ### Round-4 frontier (post-unlock)`; file 162 lines | VERIFIED |

## 2. C1 — the census Frontier blind spot and the three-way patch fork

### 2.1 Before-state: the blind spot is real and broader than locus-free staleness

- **Seeded stale literal** at `:91-93` (the r4 before-state: `real
  solc/vyper-compiled bytecode untested`), line-count neutral on a 162-line
  scratch copy: v10 → **`VERDICT: PASS (0/0/0/0)` exit 0**, counters identical
  to clean. REPRODUCED.
- **Truncation to 161 lines** (drops the last Frontier line): v10 → **PASS exit
  0**. The instrument reads PASS on silent content loss past `:131` — a second
  blind-spot face beyond the frozen example. REPRODUCED.
- **Stripped bullet** (`:91-93` → `- **EVM bytecode (extended)** — held.`,
  blanks to keep 162 lines): v10 → PASS exit 0. This is the arm that
  discriminates the three patches below.

### 2.2 The three delivered patches — round-trip identities

All applied to a pristine `git show HEAD:.ufo/gates/c1-census-v10.py` copy
(sha `d0772ce8…`) in `/var/tmp/cn2-r6/c1/`:

| Seat | Patch source | Result sha256 / lines | Claimed | Verdict |
|---|---|---|---|---|
| PL-4 | `claims/c1/PL-4/patch-v10-to-r10.diff` | `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca` / 713 | same | **REPRODUCED byte-exact** |
| RV-3 | diff fenced in `claims/c1/RV-3.md` §4 | `8e4206796fec2e16fb6f2c1959f33b63bbcb9643471d42472ac6bc2cba195ebf` / 712 | same | **REPRODUCED byte-exact** |
| PL-2 | `claims/c1/PL-2/prior-attempt/c1-census-v10-r10.patch` (path at my apply time; the seat moved its prior design there at 14:00) | `2d7ee95ba2743bde0b658c91d867a46e04e3e9e14de41d2cb60f2ff46238ce7b` / 705 | same (and equals its `…proposed.py`) | **REPRODUCED byte-exact** |

### 2.3 Arm matrix (five trees × four instruments) — `CN-2/c1-arms.txt`

| Tree | v10 | PL-4 | RV-3 | PL-2 *prior* |
|---|---|---|---|---|
| clean (byte-identical copies of the three scoped files) | PASS 0 | PASS 0, `14 rows, errors: []` | PASS 0, `13 rows, 0 error(s)` | PASS 0, `3 entries: []` |
| seeded stale literal `:91-93` (frozen example) | **PASS 0 (blind)** | FAIL 1, `['FRONTIER-STALE']` + 2 REQUIRED-absent | FAIL 1, `['FRONTIER-STALE','FRONTIER-UNATTESTED']` | FAIL 1, `['FRONTIER-STALE']`, hit `:92` |
| stripped bullet (no stale literal) | PASS 0 (blind) | FAIL 1, `['FRONTIER-UNEVALUABLE']` | FAIL 1, `['FRONTIER-UNATTESTED']` | **PASS 0 — hole** |
| PROVINCE truncated to 161 lines | PASS 0 (blind) | FAIL 1, `['UNREADABLE','FRONTIER-UNEVALUABLE']` (+14 uncheckable rows) | FAIL 1, `['FRONTIER-UNATTESTED']` (last row loses `HOPPER_LAUNCHER_PATH`) | FAIL 1, `['UNREADABLE']` |
| real repo root (`--root .`) | PASS 0 | PASS 0 | PASS 0 | PASS 0 |

JSON invariance on the clean tree, key-by-key vs v10: **17 shared keys, zero
mismatched** for all three; extras are additive only —
PL-4/RV-3 add `frontier_errors`, `frontier_rows`; PL-2 adds
`frontier_register`, `frontier_stale`. `current_ok_per_file` stays
`{'PROVINCE.md': 17, 'SCORECARD.md': 14, 'SKILL.md': 3}` for all three
(`CN-2/c1-json-invariance.txt`). Every existing SCOPE row is byte-preserved
(PL-2 only inserts two rows after the last existing row).

**Second arm set — the gaps the delivered patches leave** (my own trees,
`CN-2/c1-hardening.txt`):

| Tree | v10 | PL-4 | RV-3 | PL-2 *prior* |
|---|---|---|---|---|
| **two other `40de383` stale literals** `~900s internal session deadline` in `:139-144` + `probe-refused since r2` in `:157-160`, anchors kept | PASS 0 (blind) | **PASS 0 — blind** | **PASS 0 — blind** | FAIL 1, `['FRONTIER-STALE']` ×2 |
| **one blank line inserted before `:133`** (pure reflow, 163 lines) | PASS 0 | **PASS 0 — blind (span-based)** | FAIL 1 (`FRONTIER-ANCHOR`/`UNATTESTED`) | FAIL 1 (`SCOPE-ERROR` marker at `:133`) |
| **header renamed** `## Frontier` → `## Frontier (renamed)` | PASS 0 | **PASS 0 — blind** | FAIL 1 | FAIL 1 (`SCOPE-ERROR` at `:73`) |

So the three patches are complementary on measured classes: PL-4/RV-3 catch
claim-less bullet rewrites but not the two other on-record literals; PL-2
catches the literals but not claim-less bullets; RV-3/PL-2 catch pure reflow,
PL-4 does not. No single delivered patch is the union.

### 2.4 Design discriminator and fork resolution

- **PL-2's current artifact no longer proposes its prior design as a base.**
  It was updated at 14:00: the prior attempt (2 SCOPE `FRONTIER` rows +
  3-literal register, sha `2d7ee95b…`) moved to `prior-attempt/`, and the
  current text explicitly endorses landing PL-4. Its prior design is measured
  incomplete: a bullet rewritten to a bare "held" claim reads **PASS exit 0**
  (my arm; the seat's own §6 reports the same). Its contribution is the two
  optional header rows in §2.5.
- **RV-3's current artifact also endorses landing PL-4 as-is** (its §7,
  `RV-3.md:215-225`), while preserving its own 13-row design as an alternative
  and naming the same two residuals. Its anchor rows are the only delivered
  mechanism that fails loudly on a pure reflow (measured).
- **PL-4 is span-based, not line-identity-based.** A content-changing edit
  fails closed, but a pure ±1-line insertion whose required patterns remain
  inside the shifted spans reads **PASS** (measured: blank line before `:133`;
  header rename). This corrects PL-4's own §6.1 claim that insertions inside
  `:132-162` are caught; the frozen falsifiable (a)/(b)/(c) still holds because
  the seed is content-changing.
- **They cannot coexist.** Applying RV-3 onto PL-4's result: **3 of 7 hunks
  fail**; applying PL-2's prior patch onto RV-3's result: **3 of 10 hunks
  fail** (`CN-2/c1-cross-apply.txt`). Exactly one may land, and its
  post-landing sha must be recorded in the landing receipt (the gate's own
  rule-#14 discipline, gate `:89-93`).

### 2.5 Optional hardening (scratch-measured; not part of PL-4)

Three peer proposals plus the combined set were re-derived first-hand; all
apply additively on PL-4's `FRONTIER[]` and change only `frontier_rows`:

| Option | Rows added | Result sha / lines / rows | Arms measured |
|---|---|---|---|
| CN-4 two-literal amendment | FORBIDDEN `~900s internal session deadline` (139-144) + `probe-refused since r2` (157-160) | `2f01f8498351bd3a799f5ad94ebf0076072460f7d858bd4f3d2c7978116e00df` / 713 / 14 | clean PASS; seeded FAIL `FRONTIER-STALE`; stripped FAIL; extra-stale2 **FAIL ×2**; trunc FAIL |
| PL-2 two header rows | `(73,73,^## Frontier$)` + `(133,133,^### Round-4 frontier \(post-unlock\)$)` | not separately built; measured by PL-2 | PL-2 §7: clean PASS; header rename / insert-133 FAIL |
| **combined 4-row set** | both of the above | `6f8f3fe87fb8a4cb1f4f7446fc95c90fc2697521229de17401dd157a173498c0` / 715 / **16** | clean PASS; seeded, stripped, extra-stale2, trunc, **edge-insert**, **edge-header** all FAIL closed; 17/17 shared keys equal |
| PL-1 per-bullet anchor delta | 16 rows with anchor lines + 3 FORBIDDEN (applies on PL-4) | `7724adccdf6391cffc622b8fa3144ede421eb24aedc1431893c2482f892c12a1` / 748 / 16 | my round-trip reproduces the sha; patched file carries 16 anchor rows and all 3 FORBIDDEN literals; CR-8 measured clean PASS, reflow133 FAIL `FRONTIER-ANCHOR`, wall seed FAIL `FRONTIER-STALE` |

The combined 4-row set is the only measured single instrument that closes
every arm in this section; PL-1's delta additionally hardens reflow at all 13
bullets. Neither is required by the frozen C1 — the claim asks for the frozen
seed to be caught and the clean tree to stay PASS, which PL-4 already does.

**C1 ruling: before-state VERIFIED. PL-4 VERIFIED complete on (a) clean-tree
PASS, (b) seeded-reintroduction FAIL with a named class, (c) every SCOPE row
and counter intact; it is the recommended landing patch and the chain
converged on it (PL-2 current and RV-3 current both endorse it). Record in the
landing receipt, not inline: the pure-reflow blindness, the two other on-record
literals, and the optional hardening shas above. RV-3 is a verified alternative
design; its prior competitor PL-2 is archived and measured incomplete as a
standalone.**

## 3. C2 — the viaIR corpus Unknown (EX-7)

### 3.1 Before-state and Unknown provenance

- Command A before: 84 files / 84 mapped / missing [] / dangling [], both
  revs — REPRODUCED (§1.5).
- `grep -n -i viaIR corpus/knowledge/*.md` → exactly two hits, both Unknowns:
  `2026-10-19-arc3-r3-evm-optimizer-shapes.md:33` and
  `2026-10-19-arc3-r4-evm-vyper-leg.md:28`. No entry names a viaIR dispatcher
  measurement. The Unknown is open — VERIFIED.
- The new token `2026-10-19-arc3-r6-viair-dispatch-shape` occurs **0** times
  in `corpus/README.md`; the EVM row (`:38`) carries 4 existing tokens.

### 3.2 Entry byte audit — `CN-2/c2-audit.txt`

Retained compiled bytes (my sha/size): `viair-opt200` runtime **1,517 B
`2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a`**, creation
1,560 B `d85fdde9…`; `viair-noopt` 4,144 B `0cc6938c…` / 4,318 B `f1125049…`;
`std-opt200` control 1,921 B `c2ceabb1…` / 1,966 B `4541fd49…`. Runtime occurs
in the viaIR creation at **+43**, trailing 0. All equal the entry's stated
values.

### 3.3 Live re-probe (my run, first-hand)

`TMPDIR=/var/tmp/cn2-r6/c2/tmp npx -y rea-agents@6.4.0 inspect-evm-interface
.ufo/waves/…/EX-7/out/viair-opt200/runtime.hex hex --format json` → exit 0,
`raw_result.functions` **15**, all `dispatch:"abi"`, 15 distinct selectors,
decoded `bytecode.sha256 2ec3f557…f20363ec1732845c99581a`, 1,517 bytes,
evidence id `ev_71da9d37…` (path-minted, as the entry's id-domain caveat
predicts). Offsets exactly the entry's list: 982, 935, 771, 723, 694, 631,
572, 485, 425, 374, 340, 311, 272, 253, **204** for `ee02438e`. K/K confirmed.

### 3.4 Opcode walk (my decoder)

viair-opt200: 19 opcode-boundary `PUSH4` sites; **14 EQ legs** at a strict
**11-byte stride**, selectors ascending `01681a62 … d0e30db0`, all EQ dsts
JUMPDESTs; then **`PUSH4 ee02438e SUB PUSH2 0x000e JUMPI` at pc 194** (`SUB`,
not `EQ`) → dst 14, the guard block's JUMPDEST. Prologue
`608060405260043610156100` = `PUSH1 4 CALLDATASIZE LT ISZERO PUSH2 … JUMPI`
(the `ISZERO` is the legacy-distinguishing byte). The entry's fourth-class
claim reproduces.

### 3.5 Independent corroboration (EX-6's second viaIR carrier)

EX-6's `ViaIRVault` (different source, 12 ABI functions) carries the same
class on both legs: `viair-opt200` runtime 1,127 B — 11 EQ legs, stride 11,
ascending, plus `PUSH4 f43cc773 SUB PUSH2 0x000e JUMPI` at pc 302; `viair-nopt`
3,039 B — 11 EQ legs + the same SUB leg at pc 161. So the class is
**N−1 EQ legs + one `SUB`-terminated final leg**, reproduced on two carriers
(12 and 15 functions) and both optimizer settings. VZ-4's earlier note that
EX-6's prologue has "no selector decode" is a narrow-prologue reading
corrected in context: the chain sits at pc 182/161, and its `SUB` leg confirms
the same class rather than a different one.

### 3.6 Landing overlay and two text corrections

Minimal scratch git repo with the corpus at HEAD + the entry + the EVM-row
token, exact command-A recipe: before `84/84`, after **`knowledge_files 85,
mapped 85, missing [], dangling [], coverage 10.0`**, `rule_blocks` 14
untouched (`CN-2/c2-audit.txt`). This is a simulation, not a substitute for
the post-landing measurement on the real tree.

Two text-only corrections, each re-derived against the retained bytes; neither
changes a measurement or a command-A count:

1. **CBOR trailer byte.** The entry's metadata observation writes
   `a2 64 69706673 58 22 <ipfs…> 73 736f6c63 43 000825 00 33`. The actual tail
   (`runtime.bin[-64:]`) is `…a2 64 69706673 5822…5d 64 736f6c63 43000825
   0033`: the `solc` text-string header is **`64`** (major type 2, length 4),
   not `73` (a 19-byte string header). `64 736f6c63` is present; `73 736f6c63`
   is absent. Fix `73`→`64` in the entry text. (CR-8 credits EX-9's catch; I
   re-derived it from the bytes.)
2. **Recheck parenthetical.** The entry says decoded `bytecode.sha256
   2ec3f557…` is "the carrier file's own sha256". The carrier file is
   `runtime.hex`, whose own sha256 is `19838d66…`; `2ec3f557…` is the sha of
   the **decoded** runtime (`runtime.bin`). Fix the parenthetical, keep the
   hash. (CN-4 found the same.)

**C2 ruling: REPRODUCED end-to-end.** The entry is ready to land as
`corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md` + the EVM-row
token, after the two text corrections above. Landing detail: the draft's HTML
comment header is staging-flavored ("LAND-MOVE: parent copies …"); existing
corpus entries carry a standard `corpus entry — … Staging: …` comment, so the
integrator may normalize it — command A is indifferent.

## 4. C3 — rule #15 (SC-3 vs RV-7)

### 4.1 Baseline

`rule_blocks=14`, `citation_resolved_rules=14`, `depth_score=10.0` at both
revs; the craft section is SKILL.md `:81-255`, 14 `- **` blocks ending "never
a carried-over number." — REPRODUCED.

### 4.2 Draft identities and boundary hygiene — `CN-2/c3-audit.txt`

| Draft | Bytes / lines | sha256 | Parses as |
|---|---|---|---|
| SC-3 §4 fenced block (with trailing newline) | **1,605 / 23** | `763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1` | exactly 1 rule block |
| SC-3 after `:34`→`:29` only | 1,605 / 23 | `6967b1e3e7fbdb43492e191426399c0311ab3bf85ee307f1a181a3edd235511e` | exactly 1 rule block |
| SC-3 after `:34`→`:29` + `:24`→`:31` (minimal repoint) | 1,605 / 23 | `1a66dd55e79e0c2c56167764d786d89a69b1e2a3120c2b36e53f6effcd6a9b07` | exactly 1 rule block |
| RV-7 `rule15-bullet.md` (identical to its fenced §3 block) | 1,565 / 23 | `ccbc5cdbbefc86081393cd4d60ef9c85606c3dd1c98ed76d63520da1da0b67e7` | exactly 1 rule block |

SC-3's self-identity claim (1,605 B, 23 lines, `763c44b5…`) is **REPRODUCED
byte-exact**; both drafts have no inner `- **` line that would split a second
block. The corrected shas are my measurements of the indicated edits; CR-8's
combined-fix sha `a1bceb40…` corresponds to a different exact byte edit (it
rewords the first clause) and is **not reproduced** by a pure `:24`→`:31`
repoint.

### 4.3 Simulated landing (append to the craft section, exact command-A split)

| Draft | before | after |
|---|---|---|
| SC-3 | `rule_blocks 14, resolved 14, depth 10.0` | **`rule_blocks 15, resolved 15, depth 10.0`** |
| RV-7 | same | **`rule_blocks 15, resolved 15, depth 10.0`** |

Both falsifiables pass on scratch at the HEAD tree. The command-A pattern
cannot discriminate them further: **every citation, including a wrong one,
resolves if its line number is within the file** (that is the instrument's
documented scope limit, and the reason the clause-level audit is the real
check — the r1 lesson).

### 4.4 Two corrections (SC-3) and the zero-edit alternative (RV-7)

- **Correction 1 — SC-3 mis-cites r4 `:34`.** The quoted limitation "empty
  results do not prove absence of dispatch" lives at
  `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:29` (the Limitations
  bullet); `:34` is `## Erratum (arc3-loop1-round5 correctness sweep…)` — the
  section header. `34 ≤ 63`, so command A resolves it; the landed rule would
  point readers at the wrong line. **Fix `:34` → `:29`** (sha `6967b1e3…`).
- **Correction 2 — SC-3 cites `r1:24` for containment it denies.** The first
  clause reads "The r1 creation legs probed 0 functions on blobs that
  byte-contain the full runtime (`r1…md:24`)". r1 `:24` says the opposite
  ("Creation blobs carry no runtime dispatch table"); the containment is
  established at r1 `:31` ("…is measured false — `Rv2Token.creation.hex`
  (1,971 B) embeds the runtime and its five `EQ;PUSH2;JUMPI` sites"). The
  second half of the same sentence already cites `:31` for the erratum, so the
  minimal fix is to cite `:24` for the 0-function result and `:31` for the
  containment (a pure `:24`→`:31` repoint gives my sha `1a66dd55…`; CR-8
  reports `a1bceb40…` for its own combined-fix bytes, which I did not
  reproduce). Either way, the landing receipt must carry the sha of the bytes
  actually landed.
- **RV-7 is content-clean as written.** Its citations (`r1:24` for the
  original claim, `r1:31` for the correction, `r3:27`, `r3:41-51`, `r4:25`,
  `r4:39-46`) all resolve and all match the text at the named lines. Its
  embedding numbers re-derive first-hand: CarrierV creation 1,637 B
  `3c667396…`, runtime 1,562 B `57d6fd0a…`, at **+20**, 55 trailing; VaultB
  opt200 1,621 B `b24a0115…` at **+34** in 1,655 B; VaultB nopt 3,163 B
  `bcdf64ab…` at **+80** in 3,243 B.
- **RV-7's finding F1 VERIFIED.** The r3 erratum at `:41` claims to correct
  "`:24` 'Creation blobs carry no runtime dispatch table'", but r3 `:24` is
  the Rv2TokenOpt RESULT row at HEAD **and** at `c418be0`; the quoted sentence
  is r1 `:24` (corrected at r1 `:31`). The erratum's byte facts are true; its
  pointer is dangling. That is corpus debt outside this wave's write scope —
  record it for the next append-only pass.

**C3 ruling: SC-3 REPRODUCED with two CORRECTIONS (r4 `:34`→`:29`; r1
containment attribution `:24`→`:31`/rewording), identity to be re-derived
after the edits. RV-7 VERIFIED as a landable alternative that is correct as
written. Land exactly one — two would parse as rules #15 and #16 and move
`rule_blocks` to 16, outside the frozen falsifiable. For a zero-edit landing,
RV-7 verbatim is the lower-risk path; if the wave prefers SC-3's wording, land
it only after both fixes and record the new sha.**

## 5. Peer reconciliation (all re-derived before ruling)

- **VZ-4** — C1: its audit of RV-3 reproduces (sha `8e420679…`, clean PASS,
  seeded FAIL with `FRONTIER-STALE`/`FRONTIER-UNATTESTED`, 17-key invariance,
  citations present). Its `PENDING` C1 row predates PL-4/PL-2; the replacement
  is the fork ruled in §2. C2: its `PENDING` is superseded by EX-7's entry —
  my audit confirms the entry, the live K/K probe and the 85/85 overlay. Its
  EX-6 "no selector decode in the prologue" note is **CORRECTED in context**
  (§3.5). C3: its `:34`→`:29` correction is **CONFIRMED** first-hand.
- **CN-4** — converges on the same three landings (PL-4, EX-7, SC-3+fix or
  RV-7). Its two-literal amendment to PL-4 (FORBIDDEN `~900s internal session
  deadline`, `probe-refused since r2`) is **REPRODUCED** on my own trees
  (amended sha `2f01f849…`; extra-stale2 FAIL ×2, all other arms unchanged).
  Its EX-7 recheck-parenthetical correction is **CONFIRMED** (§3.6). Its
  claim-less-bullet arm (RISC-V strip) reproduces (PL-4/RV-3 FAIL, PL-2
  PASS). No conflict with this artifact; my §2.5 adds the combined 4-row
  measurement it did not build.
- **CR-6** — PL-4 verification reproduces (same sha, six arms, 17-key
  invariance); its two structural-edge corrections reproduce (header rename
  and blank-line-before-133 PASS under PL-4); its SC-3 `:34`→`:29` correction
  and C2 verifications reproduce. It does not see the `r1:24` attribution
  issue; my §4.4 adds it.
- **CR-8** — PL-4/EX-7/SC-3 verifications reproduce. Its two PL-4 residual
  corrections reproduce (reflow, two on-record literals). Its EX-7 CBOR typo
  (`73`→`64`) is **CONFIRMED** from the bytes (§3.6). Its SC-3 `r1:24`
  attribution finding is **CONFIRMED** in substance; its combined-fix sha
  `a1bceb40…` is not reproducible by a pure `:24`→`:31` repoint (my `1a66dd55…`),
  so the landing receipt must record the exact landed bytes. Its PL-1 delta
  round-trip (`7724adcc…`, 748 lines) reproduces.
- **PL-4** — all three frozen sub-claims reproduce; the 17-key JSON comparison
  reproduces exactly (only `frontier_errors`/`frontier_rows` added); its
  five-tree seeded matrix reproduces on my own trees. Its residual §6.1 claim
  that insertions inside `:132-162` are caught is **CORRECTED** (pure reflow
  PASSes, measured); the other residuals (past-the-bound appends, re-key
  discipline, earned-not-exhaustive FORBIDDEN coverage) stand.
- **RV-3** — all claims reproduce; its current artifact **endorses landing
  PL-4 as-is** and preserves its own design as an alternative. Its
  anchor semantics are the only delivered mechanism that catches pure reflow
  (measured). Its design note that SCOPE-only rows would grade nothing is
  re-measured true (v10 loci stay 6; PL-2's SCOPE rows add no grading).
- **PL-2** — its current artifact is an independent PL-4 verification that
  endorses landing PL-4 and offers two optional header rows; its *prior*
  design (moved to `prior-attempt/`) reproduces as an instrument (sha
  `2d7ee95b…`, clean PASS, seeded FAIL) but is measured incomplete (stripped
  bullet PASS; paraphrase also missed per its §6). Its header-row hardening
  (§7) is consistent with my edge arms (header rename / insert-133 FAIL).
- **EX-7** — every byte value, the live K/K result, the opcode walk and the
  84→85 overlay reproduce. Its honest limits (single solc version, one
  carrier family, K=15, one 6.7.0 leg) stand; EX-6's independent carrier
  widens the class evidence to a second family.
- **SC-3** — self-identity, byte census and scratch 14→15 reproduce; two
  citation corrections are §4.4.
- **RV-7** — its rule draft, citation table, F1 and byte-embedding facts
  reproduce; its candidate-(a) "unlandable without a corpus entry" analysis is
  consistent with command A's `valid = bool(refs)` rule (read at
  SCORECARD.md:105-117).

## 6. Composite landing simulation (interaction check)

A scratch git repo with **c2 entry + EVM-row token + a c3 rule** all applied
in one commit, exact recipe. Measured twice — once with SC-3's rule, once with
RV-7's: `{"knowledge_files": 85, "mapped": 85, "missing": [], "dangling": [],
"rule_blocks": 15, "citation_resolved_rules": 15, "coverage_score": 10.0,
"depth_score": 10.0}` both times. The three chains do not
interact: c1 is the gate file, c2 is corpus/README + corpus/knowledge, c3 is
SKILL.md. They can land in one round commit (with one c1 patch and one c3
draft chosen).

## 7. Per-item verdict table

| # | Item | Verdict |
|---|---|---|
| 1 | HEAD `c625d5d` / work `58c3db7`; gate sha `d0772ce8…`; 162/390/1696 lines | REPRODUCED |
| 2 | v10 clean PASS 0/0/0/0; G2 17/14/3 | REPRODUCED |
| 3 | SCOPE rows; Frontier 73-93 + 133-162 UNDECLARED | VERIFIED |
| 4 | v10 PASS on seeded stale literal at `:91-93` | REPRODUCED (blind) |
| 5 | v10 PASS on a 161-line PROVINCE (past-`:131` content loss) | REPRODUCED (second blind face) |
| 6 | PL-4 round-trip sha `80027570…` / 713 lines | REPRODUCED |
| 7 | PL-4 clean PASS; seeded FAIL `FRONTIER-STALE`; stripped FAIL; trunc FAIL `UNREADABLE` | REPRODUCED |
| 8 | PL-4 17 shared JSON keys unchanged; 2 additive keys | REPRODUCED |
| 9 | RV-3 round-trip sha `8e420679…` / 712 lines; all arms; 3 named classes | REPRODUCED |
| 10 | PL-2 round-trip sha `2d7ee95b…` / 705 lines; clean/seeded arms | REPRODUCED |
| 11 | PL-2 prior design stripped-bullet hole (PASS exit 0); its current artifact endorses PL-4 | **DISCREPANCY (prior design incomplete)** |
| 12 | Three c1 patches mutually exclusive (3/7, 3/10 hunks fail) | VERIFIED |
| 13 | PL-4 recommended; RV-3 alternative (current artifact endorses PL-4); PL-2 prior design not standalone | RULING |
| 14 | Command A 84/84 before, both revs | REPRODUCED |
| 15 | viaIR Unknown open only at r3:33 / r4:28; token absent from README | VERIFIED |
| 16 | EX-7 retained sizes/shas (1,517/1,560/4,144/4,318/1,921/1,966) | REPRODUCED |
| 17 | EX-7 live 6.4.0 probe 15/15 `abi`, decoded `2ec3f557…`, offsets incl. 204 | REPRODUCED |
| 18 | viaIR opcode class: 14 EQ @ stride 11 ascending + `SUB` leg `ee02438e`→14 | VERIFIED |
| 19 | EX-6 second carrier: 11 EQ @ stride 11 + `SUB` `f43cc773`→14 | VERIFIED |
| 20 | C2 landing overlay 85/85, missing/dangling [] | REPRODUCED (simulation) |
| 21 | SC-3 draft identity 1,605 B / 23 lines / `763c44b5…` | REPRODUCED |
| 22 | SC-3 scratch 14→15, 15/15, depth 10.0 | REPRODUCED |
| 23 | SC-3 `r4:34` citation content | **CORRECTED → `:29`; sha `6967b1e3…`** |
| 24 | RV-7 draft 1,565 B / 23 lines; scratch 14→15, 15/15 | REPRODUCED |
| 25 | RV-7 embedding numbers (+20/1,637/1,562/55; +34/1,621/1,655; +80/3,163/3,243) | REPRODUCED |
| 26 | RV-7 F1: r3 erratum's `:24` pointer dangling (r3:24 is the RESULT row at HEAD and `c418be0`; quote is r1:24) | VERIFIED |
| 27 | Composite c1-independent landing: 85/85 + 15/15 in one tree | REPRODUCED (simulation) |
| 28 | PL-4/RV-3 blind to the two other `40de383` literals; PL-2 catches both | **CORRECTED (coverage gap measured)** |
| 29 | PL-4 blind to pure reflow (blank line before `:133`, header rename); RV-3/PL-2 catch | **CORRECTED (PL-4 §6.1 overstated)** |
| 30 | CN-4 two-literal amendment: sha `2f01f849…`, all arms green | REPRODUCED |
| 31 | Combined 4-row hardening: sha `6f8f3fe8…`, 715 lines, 16 rows, all arms FAIL closed | REPRODUCED |
| 32 | PL-1 16-row anchor delta round-trip: sha `7724adcc…`, 748 lines | REPRODUCED |
| 33 | EX-7 CBOR trailer text `73 736f6c63` vs actual `64 736f6c63` | **CORRECTED (text only)** |
| 34 | EX-7 recheck parenthetical: `2ec3f557…` is decoded runtime.bin, not `runtime.hex` (`19838d66…`) | **CORRECTED (text only)** |
| 35 | SC-3 first-clause `r1:24` containment attribution (r1:24 denies it; `:31` carries it) | **CORRECTED (second content anchor)** |

## 8. Residuals (named, not silently open)

1. **C1 past-the-bound appends**: a brand-new Frontier bullet appended past
   `:162` sits outside all three registers until re-keyed (PL-4 and RV-3 both
   name this class; it is the same standing rule as the SCORECARD bound).
2. **C1 re-key discipline**: any legitimate frontier edit must re-key the
   chosen register in the same commit; until then the run fails closed.
3. **C1 span-based blindness (PL-4), measured**: a pure ±1-line insertion whose
   required patterns remain inside the shifted spans PASSes (blank line before
   `:133`; header rename at `:73`), and a mid-bullet reflow is invisible. This
   corrects PL-4's §6.1 claim; content-changing edits still fail closed. The
   intro `:75-80` row is boilerplate and fails on a legitimate prose rewrite
   until re-keyed. RV-3's anchor rows and PL-1's 16-row delta close the reflow
   class (PL-1 sha `7724adcc…`); the combined 4-row set (sha `6f8f3fe8…`)
   closes headers + the two literals but not mid-bullet reflow.
4. **C1 on-record literal breadth**: PL-4 declares only `untested`; the two
   other `40de383` before-states pass. CN-4's two-literal amendment closes
   them (measured sha `2f01f849…`). The frozen C1 requires only the EVM seed,
   so this is a named residual, not a claim failure.
5. **C2 text-only corrections**: the CBOR `73`→`64` byte and the recheck
   parenthetical (`2ec3f557…` is the decoded runtime, not the hex file) must
   be fixed before landing; neither changes a measurement.
6. **C2 scope**: the entry closes viaIR for solc 0.8.37 / its carrier family;
   other solc versions, Vyper's IR pipeline, runs ≠ 200 and `fallback()`-
   bearing viaIR shapes stay Unknown. Raw legs at 6.4.0 only; one 6.7.0 hex
   leg.
7. **C3 identity after corrections**: fixing SC-3's pointers changes the
   draft's bytes; the 1,605 B / `763c44b5…` value must not be quoted for the
   corrected text (`:34`→`:29` gives `6967b1e3…`; my `:24`→`:31` repoint gives
   `1a66dd55…`). The landing receipt must carry the re-derived sha.
8. **Corpus debt (not this wave's write scope)**: the r3 erratum's `:24`
   pointer (F1) remains dangling; queue an append-only pointer correction.

## 9. Landing order for the parent

1. **c1**: apply PL-4's patch to `.ufo/gates/c1-census-v10.py`:
   `patch .ufo/gates/c1-census-v10.py < claims/c1/PL-4/patch-v10-to-r10.diff`;
   expect sha `8002757078a685f5…e18d14aecca`, 713 lines;
   `python3 .ufo/gates/c1-census-v10.py --quiet` → exit 0, PASS,
   `FRONTIER register (G21): 14 rows asserted, errors: []`. Record the
   post-edit identity **and** the measured residuals in the landing receipt,
   not inline: pure-reflow blindness, the two other on-record literals, and
   the optional hardening shas (§2.5). Do **not** also apply RV-3 or PL-2.
   If the lane accepts a same-round hardening, the combined 4-row set
   (`6f8f3fe8…`, 715 lines, 16 rows) is the only measured single instrument
   that closes headers + all three on-record literals; it changes only
   `frontier_rows` (14→16).
2. **c2**: copy
   `claims/c2/EX-7/entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md` →
   `corpus/knowledge/` **after** the two text fixes (§3.6: `73`→`64`; the
   recheck parenthetical); append the token to the EVM row
   (`corpus/README.md:38`). Command A must read `knowledge_files 85, mapped
   85, missing [], dangling []`.
3. **c3**: land **one** rule. Zero-edit path: RV-7's `rule15-bullet.md`
   verbatim. SC-3 path: apply both pointer fixes (r4 `:34`→`:29`; r1
   containment attribution `:24`→`:31` or a rewording) and record the
   re-derived sha (`6967b1e3…` for the first fix alone; `1a66dd55…` for my
   minimal two-fix version). Command A must read `rule_blocks 15,
   citation_resolved_rules 15, depth_score 10.0`.
4. Re-run the composite expectation after all three:
   `{"knowledge_files": 85, "mapped": 85, "missing": [], "dangling": [],
   "rule_blocks": 15, "citation_resolved_rules": 15, "coverage_score": 10.0,
   "depth_score": 10.0}` (simulated first-hand; land and re-measure).
5. Retire the non-chosen c1 designs (RV-3, PL-2 prior) and the non-chosen c3
   draft to the wave record with their verdicts intact — they are verified
   alternatives, not failures, except PL-2's prior design coverage hole. Note
   that PL-2's and RV-3's current artifacts already endorse landing PL-4.

## 10. Evidence

- `CN-2/c1-arms.txt` — five trees × four instruments, exit codes, classes,
  error lines.
- `CN-2/c1-hardening.txt` — extra-stale2 / edge-insert / edge-header arms,
  amended PL-4 and combined 4-row shas, PL-1 delta round-trip, corrected
  SC-3 identities, EX-7 CBOR bytes, peer convergence statements.
- `CN-2/c1-json-invariance.txt` — 17-key comparison per patch.
- `CN-2/c1-cross-apply.txt` — mutually-exclusive patch evidence.
- `CN-2/c2-audit.txt` — entry sizes/shas, live probe fields, opcode walk,
  EX-6 corroboration, 84→85 overlay, Unknown provenance.
- `CN-2/c3-audit.txt` — draft identities, citation sets, simulated landings,
  citation-dispute line checks, byte census, boundary hygiene.
- `CN-2/git-status.txt` — write-scope check (only the pre-existing
  `arc2-loop1-round10/C3.md` modification and the untracked wave tree).
