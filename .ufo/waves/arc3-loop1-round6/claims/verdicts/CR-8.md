# CR-8 — verdicts/convergence: the three delivered artifacts audited, competing drafts reconciled

Seat CR-8, verdicts/convergence chain, wave arc3-loop1-round6, 2026-10-19.
Repo HEAD `c625d5de57e045188b5ce8cd450a57b349f90785` (`c625d5d`; work
`58c3db7`), both re-derived first-hand. Every number below is my own
measurement this session (lane rule #14); peer artifacts are used as claims to
test, never as evidence. Write scope honored: only
`.ufo/waves/arc3-loop1-round6/claims/verdicts/CR-8.md` and `…/verdicts/CR-8/`
were created. Git was read-only; `.ufo/gates/`, `corpus/`, `SKILL.md`,
`PROVINCE.md`, `SCORECARD.md`, `LOG.md` were never modified. Scratch:
`/var/tmp/cr8-r6/` (never `/tmp` — EDQUOT). Evidence: `claims/verdicts/CR-8/`
(23 files, `manifest.sha256`).

Snapshot: at artifact write time (~14:02 local) the chain dirs held 16 seat
Markdowns — c1: PL-2, PL-4, RV-3; c2: EX-7, EX-9; c3: EX-14, EX-15, EX-16,
RV-5, RV-6, RV-7, RV-8, SC-1, SC-3, SC-4; verdicts: VZ-4 — plus c1 evidence
dirs PL-1, EX-3, RV-1 without a seat Markdown yet.

## 0. Verdict in one screen

| Claim | Delivered artifact | My ruling |
|---|---|---|
| C1 operability (census Frontier blind spot) | PL-4 patch `patch-v10-to-r10.diff` | **VERIFIED end-to-end**: round-trips to `80027570…` (713 lines); clean tree PASS; seeded frozen literal FAILs with `FRONTIER-STALE` exit 1 while v10 stays PASS; 17/17 JSON keys unchanged. Two of PL-4's residual claims are **CORRECTED** (a one-line reflow and two other historical stale literals pass). Late peers converge on landing PL-4; PL-1's measured delta hardens the named gaps. |
| C2 coverage (corpus Unknown) | EX-7 viaIR entry draft | **VERIFIED + REPRODUCED**: all three runtime hashes/sizes reproduce; my own opcode walk reproduces the fourth dispatcher class exactly; the five real probe legs are 15/15 and both trap envelopes reproduce; a live 6.4.0 probe returns 15/15; command A with entry+token measures **85/85** in a scratch repo. One text correction before landing: the CBOR-trailer hex writes `73 736f6c63`, the byte is `64 736f6c63` (EX-9's catch, independently confirmed). |
| C3 depth (rule #15) | SC-3 rule-15 draft | **VERIFIED with two content-anchor corrections**: draft identity `763c44b5…` reproduces (1,605 B / 23 lines); landing sim reads 14→15 rules with 15/15 resolved at both revs. `r4:34` must be `r4:29`; `r1:24` is cited for containment it denies (`:31` carries it). The recommended corrected bytes are `a1bceb40…` (also 15/15). RV-7's differently-worded draft (`ccbc5cdb…`) also verifies; land exactly one. |

**Convergence:** the lane can land **one c1 patch (PL-4), one c2 entry
(EX-7, two text fixes), and one c3 rule (SC-3 with both anchor fixes)**. The
integrated end-state was measured in a scratch repo (entry + map token +
corrected rule): `knowledge_files=85, mapped=85, missing=[], dangling=[],
rule_blocks=15, citation_resolved_rules=15, coverage_score=10.0,
depth_score=10.0` (`claims/verdicts/CR-8/` evidence; §7).

## 1. Baseline re-derivation (first-hand)

- `git rev-parse HEAD` → `c625d5de57e045188b5ce8cd450a57b349f90785`;
  `git log --oneline -3` → `c625d5d` records / `58c3db7` work / `71668cc`
  previous records. Matches the brief and `claims-frozen.md`.
- `sha256sum .ufo/gates/c1-census-v10.py` →
  `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`;
  `wc -l` → gate 610, PROVINCE.md 162, SKILL.md 390, SCORECARD.md 1696.
- Command A (`SCORECARD.md:88-124`, verbatim, Git-object reads) at both revs:
  `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
  "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [],
  "rule_blocks": 14}` at `58c3db7` and `c625d5d`. Before-state REPRODUCED.
- SCOPE coverage, imported from the gate module, PROVINCE.md rows:
  `[(8,13,CURRENT),(15,26,CURRENT),(40,43,DATED),(44,44,CURRENT),(45,62,DATED),(64,71,CURRENT),(119,131,DATED)]`
  — exactly the frozen list; covering rows for `(73,93)` = `[]` and for
  `(133,162)` = `[]`. The Frontier blind spot is real.

## 2. C1 — PL-4's census patch, independent verification

### 2.1 Identity and round-trip

- Patch `claims/c1/PL-4/patch-v10-to-r10.diff`: 182 lines, sha256
  `3f94355cfe747c10c968c2382004ab1e95792518eba2f03ae99df2f7f16a6513`.
- `git show HEAD:.ufo/gates/c1-census-v10.py` → sha `d0772ce8…`. `patch` applied
  to that pristine copy produced **713 lines, sha256
  `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`** — equal
  to `PL-4/c1-census-v10-r10.py`, and to PL-4's claimed identity.
- Requirement (c), mechanically: `--json` on a clean scratch tree, v10 vs r10 —
  **17 shared keys, 0 differing**; r10-only keys
  `['frontier_errors','frontier_rows']`; `counts` equal
  (`PROVINCE 162/6, SCORECARD 1696/9, SKILL 390/2`); `current_ok_per_file`
  `{'PROVINCE.md':17,'SCORECARD.md':14,'SKILL.md':3}` unchanged. No SCOPE row
  is touched by the diff (the register lives outside SCOPE by design).

### 2.2 Acceptance arms (scratch `/var/tmp/cr8-r6/c1/`)

| arm | v10 | PL-4 r10 |
|---|---|---|
| clean, real repo root | PASS exit 0 | **PASS exit 0**, `FRONTIER register (G21): 14 rows asserted, errors: []` |
| clean scratch tree | PASS exit 0 | PASS exit 0, same counters |
| seeded frozen literal at PROVINCE.md:91-93 (`…real solc/vyper-compiled bytecode untested…`, line-count neutral) | **PASS exit 0** (blind) | **FAIL exit 1**, `DECLARED FAIL CLASSES: ['FRONTIER-STALE']`; errors: `REQUIRED 'solc-0\.8\.37' absent`, `REQUIRED 'vyper-0\.4\.3' absent`, `FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)` |
| stripped-required at :91-93 (`- **EVM bytecode (extended)** — see corpus.`), 162 lines | PASS exit 0 (blind) | FAIL exit 1, `DECLARED FAIL CLASSES: ['FRONTIER-UNEVALUABLE']`, 2 × REQUIRED-absent, no STALE |
| instrument-visible stale pin `rea-agents@6.3.0` added inside :87-88, all original text kept | FAIL exit 1, `undeclared=1` | FAIL exit 1, `undeclared=1`, FRONTIER register errors `[]` |

The last row is the boundary check: the pre-existing UNDECLARED class already
fails pin/version/path loci anywhere in PROVINCE; G21's job is precisely the
locus-free class. Both instruments fail it, and G21 adds no false positive on
the bullet that carries an invisible-to-`classify()` stale pin.

Transcripts: `CR-8/c1-census-v10-{clean,seeded}.out`,
`CR-8/c1-census-v10-r10-{clean,seeded}.out`, `CR-8/c1-stripped-required.txt`,
`CR-8/c1-frontier-pin-{v10,r10}.txt`, `CR-8/c1-json-compare.json`.

### 2.3 Corrections to PL-4's residual section (measured, not inherited)

1. **Insertion claim overstated (`PL-4.md:330-333`).** PL-4 says insertions
   inside `:132-162` shift register spans and fail REQUIRED-absent. Measured:
   inserting one blank line before `### Round-4 frontier (post-unlock)`
   (`PROVINCE.md:133`) still reads **PASS exit 0, frontier errors []** under
   PL-4's r10 — the 14 rows' spans still contain every required pattern.
   `CR-8/c1-pl1-reflow.txt`; RV-3 independently reports the same (`RV-3.md:151`,
   `ins132` → v10 PASS and r10 PASS). The register is span-based; it is not an
   anchor-based reflow detector.
2. **On-record literals claim incomplete (`PL-4.md:337-341`).** PL-4 declares
   only `untested` as FORBIDDEN. Measured: restoring the pre-`40de383` wall
   wording `hits REA's ~900s internal session deadline` inside `:139-144`
   reads **PASS exit 0, frontier errors []** under PL-4's r10 (v10 PASS too).
   RV-3 independently reports `stale159` → r10 PASS (`RV-3.md:152`). The two
   other literals are on record in the `40de383` diff; the frozen C1 requires
   only the EVM seed, so this is a residual correction, not a claim failure.

Neither correction voids the frozen C1 falsifiable: (a) clean PASS, (b) the
frozen seeded EVM literal is caught with a named class, (c) all counters/SCOPE
rows intact.

### 2.4 Competing c1 designs — reconciliation

- **PL-2 (current artifact, 13:59).** Its prior register design was moved to
  `claims/c1/PL-2/prior-attempt/`; the current artifact explicitly endorses
  **landing PL-4's patch** and offers an optional two-row header hardening
  (`PL-2.md:293,308,312-342`). Its prior design is measurably weaker on
  stripped bullets: RV-1's matrix records `r10-pl2 seed-required` and
  `seed-riscv` **PASS** (blind; PL-1's battery likewise has `pl2-r10
  seed-wall` PASS) — consistent with PL-2 having only literal hits, no
  positive floor.
- **RV-3 (updated 13:59).** Independent `FRONTIER_REGISTER` patch: 13 rows,
  three classes (`FRONTIER-ANCHOR/UNATTESTED/STALE`). I re-extracted its diff
  from `RV-3.md` and round-tripped it onto the pristine gate: **sha
  `8e4206796fec2e16fb6f2c1959f33b63bbcb9643471d42472ac6bc2cba195ebf`, 712
  lines** — matches RV-3's identity. Its artifact now states "land PL-4's
  patch as-is" (`RV-3.md:206,215`), while correcting the same two PL-4
  residuals. It remains an alternate design, not a co-landing.
- **PL-1 (evidence only at write time).** Delta `patch-pl4-to-pl1.diff` applied
  to PL-4's r10 yields **748 lines, sha `7724adccdf6391cffc622b8fa3144ede421eb24aedc1431893c2482f892c12a1`**,
  16 rows with per-row anchors, whitespace-collapsed matching, and three
  FORBIDDEN literals (`untested`, `~900s … deadline`, `probe-refused since r2`).
  My arms: clean **PASS**; reflow133 **FAIL `['FRONTIER-ANCHOR']`** (9 anchor
  errors); wall seed **FAIL `['FRONTIER-STALE']`** (PL-4 passes that same tree).
  This is a measured hardening of the two corrections above — but it is not
  yet a claimed seat artifact, and the frozen claim does not require it.
- **EX-3 / RV-1 (evidence only).** EX-3's apply receipt reproduces the same
  patch sha and counter integrity; RV-1's matrix independently confirms PL-4
  catches the frozen seed and misses the two residual classes. Their results
  agree with mine.

**C1 recommendation:** land PL-4's patch unchanged (it meets the frozen
falsifiable and the chain converged on it); record corrections 2.3(1)-(2) in
the landing receipt as named residuals. If the lane wants a reflow/anchor
closure this round, PL-1's delta is measured and applies on top of PL-4 — but
land it as a separate, explicitly re-verified follow-up, not as a second
competing base patch.

## 3. C2 — EX-7's viaIR entry, independent verification

### 3.1 Carrier and pipeline identity

- Entry draft: `claims/c2/EX-7/entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md`
  (34 lines, 13,659 B). Source `src/ViaIrVault.sol` sha256
  `f53911672f2e33eaabaeff85e75c2565bb2899638d194fb3ffe6747abe80cbbe` —
  matches the entry.
- Runtime/creation sizes and hashes re-hashed by me:
  viair-opt200 runtime **1,517 B `2ec3f557…581a`**, creation 1,560 B
  `d85fdde9…83d5`; viair-noopt runtime **4,144 B `0cc6938c…29b4`**; std-opt200
  control runtime **1,921 B `c2ceabb1…7e27`**. All match the entry.
- `method-identifiers.json` on all three legs: 15 keys, set-equal to the
  pre-compile planted K (`evidence/planted-K.json`); ABI mutability census
  `{view:7, pure:1, nonpayable:6, payable:1}` = 15 functions — matches the entry.

### 3.2 The dispatch-shape claim, re-derived with my own decoder

My walker (`CR-8/c2-my-walk.py`, written for this seat) disassembles at opcode
boundaries and detects `DUP1 PUSH4 <sel> EQ PUSH2 <dst> JUMPI` legs
(11-byte stride) and `PUSH4 <sel> SUB PUSH2 <dst> JUMPI` legs. Output
(`CR-8/c2-independent-walk.jsonl`):

| carrier | size | PUSH4 sites | EQ legs | EQ pdst gaps | EQ dsts | sorted | SUB leg | prologue head |
|---|---|---|---|---|---|---|---|---|
| viair-opt200 | 1,517 | 19 | **14** | `[11]` | 253,272,311,340,374,425,485,572,631,694,723,771,935,982 (all JUMPDEST) | ascending | **`ee02438e` → 14 @ pc 194** | `6080604052 60043610 15 61 0022 57 … 5f3560e01c` |
| viair-noopt | 4,144 | 17 | **14** | `[11]` | 208…273 (all JUMPDEST) | ascending | `ee02438e` → 14 @ pc 194 | `…60043610 15 61 001d 57…` |
| std-opt200 | 1,921 | 22 | 15 | `[11,15,26]` | unsorted | **no** | none | `6080604052 60043610 61 00e7 57 …` (no `ISZERO`) |

This reproduces the entry's fourth-class finding: viaIR = inverted calldatasize
guard (`LT ISZERO`) + linear ascending EQ chain + `SUB`-terminated 15th leg
whose dst is the guard's JUMPDEST (byte 14); the same source with `viaIR` unset
= legacy GT/EQ binary search, no SUB leg. The `5f3560e01c` prologue is shared;
the compare tree identifies the pipeline. Selector set = the 15 planted
selectors (zero collisions, zero false positives; non-selector PUSH4 constants
`4e487b71`×2, `0c2eae8d`, `3c3332b9` on opt200 match the entry).

### 3.3 Probes, live re-run, traps, mutability

- The seven sealed envelopes parse as claimed: viair-opt200 hex/raw @6.4.0,
  hex @6.7.0, viair-noopt hex, std-opt200 hex → **15 functions, `dispatch:"abi"`
  ×15**, decoded sha = the leg's runtime sha; trap raw-on-hextext → 0 functions,
  decoded sha `19838d66…` (= the hex *text* file's own sha); creation probe →
  0 functions, decoded sha `d85fdde9…` (= creation bin). Evidence IDs in
  `CR-8` are the envelopes' own; see `EX-7/probe/`.
- **Live re-run (this seat):** `TMPDIR=/var/tmp/cr8-r6/tmp npx -y
  rea-agents@6.4.0 inspect-evm-interface <EX-7>/out/viair-opt200/runtime.hex hex
  --format json` → exit 0, **15 functions, `dispatch:"abi"` ×15**, decoded
  `bytecode.sha256 2ec3f557…581a`, subject sha `19838d66…` (the hex file),
  evidence id `ev_71da9d37a97c939cc6595db2c051ec0ab7ad4ac1daf7a846665cf31f8ada43cd`
  (path-sensitive, so different from EX-7's relative-path id — the recorded
  r3/r4 id-domain behaviour; compare by decoded sha + function payload).
  Envelope: `CR-8/c2-live-probe-6.4.0.json`.
- Mutability delta: mapped each probe selector through
  `method-identifiers.json` to the ABI — **14/15 agree; `scale(uint256,uint256)`
  ABI `pure` reads `view`**. The entry's r3-class divergence is exact.
- Creation embedding: `creation.bin[43:43+1517] == runtime.bin` exactly, no
  trailing bytes. The entry's +43 claim REPRODUCED.

### 3.4 Command A 84 → 85, measured

In a scratch repo (`git archive c625d5d`, entry copied into
`corpus/knowledge/`, EX-7's exact EVM token appended to `corpus/README.md:38`
— the context line matches the live line byte-for-byte), command A read:

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 85, "mapped": 85, "missing": [], "revision": "4b911e6", "rule_blocks": 14}
```

**85/85, missing [], dangling []** — EX-7's projection is now a measurement
(`CR-8/c2-landing-simulation.json`).

### 3.5 Landing corrections (one content, one cosmetic)

1. **CBOR trailer, entry line 28 (CORRECTED).** The entry writes
   `… 58 22 <ipfs …> 73 736f6c63 43 000825 00 33`. The actual runtime tail is
   `… 58 22 <34-byte ipfs> 64 736f6c63 43 000825 00 33`: the CBOR text(4)
   header before `solc` is `0x64`, not `0x73`. EX-9's catch independently
   confirmed (`CR-8/c2-cbor-trailer.txt`). The substantive claim (`ipfs` +
   `solc 0x000825` = 0.8.37) is unaffected. Fix before landing.
2. **Draft comment.** Lines 1-6 are a landing instruction (`corpus entry DRAFT
   — … LAND-MOVE: parent copies this file to …`). Corpus entries do carry
   provenance HTML comments (r1/r3 entries), so keep a one-line provenance
   comment but drop the `DRAFT`/`LAND-MOVE` instructions on landing. This does
   not affect any command-A counter.

## 4. C3 — SC-3's rule #15, independent verification and corrections

### 4.1 Identity and mechanical landing

- The fenced §4 body in `claims/c3/SC-3.md` measures **1,605 B, 23 lines,
  sha256 `763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1`**
  — exactly SC-3's self-identity (fence body + trailing newline; without the
  newline it is 1,604 B, sha `f34846be…`, recorded here so the extraction
  domain is unambiguous).
- Simulated landing (insert the bytes after the rule-14 bullet, before
  `## Config custody`) and command A's exact split/resolve logic at both revs:
  `58c3db7` and `c625d5d` → **rule_blocks 15, citation_resolved_rules 15,
  depth_score 10.0**; the new rule parses as exactly one block and is the 15th.
  REPRODUCED. (`CR-8/c3-landing-simulation.txt`.)

### 4.2 Citation content audit — 6/8 correct, two corrections

The instrument checks only line bounds, so I read each anchor's content:

| citation | what the draft cites it for | content at the cited line | verdict |
|---|---|---|---|
| `r1…:24` | "probed 0 functions on blobs that byte-contain the full runtime" | records 0 functions and `kind:"unknown"`, then asserts the *retracted* "Creation blobs carry no runtime dispatch table" | **CORRECTED (precision)** — attach `:24` to "0 functions", move containment to `:31` |
| `r1…:31` | erratum: embedding measured, "not byte-level absence" | exact | VERIFIED |
| `r3…:41-51` | same correction re-landed on r3 | erratum with embedded-runtime measurements | VERIFIED |
| `r3…:27` | raw-on-hex-text trap, not a carrier defect | exact | VERIFIED |
| `r4…:17` | entry had repeated the r1/r3 class | "initcode carries no runtime dispatch table" | VERIFIED |
| `r4…:25` | Vyper trap repetition | exact | VERIFIED |
| `r4…:39-46` | "creation probes parse empty while the runtime bytes are present verbatim" | exact at `:46` | VERIFIED |
| `r4…:34` | tool limitation "empty results do not prove absence of dispatch" | `## Erratum (arc3-loop1-round5 correctness sweep, append-only)` — the quote is at `:29` | **CORRECTED → `:29`** |

F1 was independently reported by EX-14/EX-16, RV-5, RV-6, SC-1, SC-4, and
EX-15 (VZ-4 earlier). One peer discrepancy: RV-8's table marks `r4:34`
VERIFIED — measured false here, because `:34` is the erratum header. F2 was
independently reported by RV-6, SC-4, EX-15, SC-1 (D1), RV-8 (N1), and noted
by EX-14; the EX-14/EX-16 corrected drafts fix F1 only. Line counts: r1 46, r3 57,
r4 63 — all bounds resolve either way. The quote at `:29` is verbatim; `:34`
is a section header.

### 4.3 Corrected landing candidates (identities re-derived)

| candidate | bytes | sha256 | landing |
|---|---|---|---|
| SC-3 as delivered | 1,605 | `763c44b5…` | 15/15 both revs; two anchor defects |
| F1-only fix (= EX-14/EX-16) | 1,605 | `6967b1e3e7fbdb43492e191426399c0311ab3bf85ee307f1a181a3edd235511e` | 15/15; leaves the `:24` precision issue |
| **recommended: F1+F2** | **1,605** | **`a1bceb4074328d9d60d14ddf0789b9bcd18ca38936c217d78fc37b1091ec1789`** | **15/15 both revs (re-measured)** |
| RV-7 alternative | 1,565 | `ccbc5cdbbefc86081393cd4d60ef9c85606c3dd1c98ed76d63520da1da0b67e7` | 15/15 both revs; 6 refs, no anchor defect found |

The recommended bytes differ from SC-3's only by the two edits shown in
`CR-8/rule15-SC-4-recommended.txt` (a re-wrap of the `r1:24` clause plus the
`r4:34`→`:29` token; 6 changed lines, 2 logical edits). **Land exactly one
rule-15 bullet**; landing both SC-3/RV-7 texts would create rule #16
duplicating the lesson.

### 4.4 RV-7's separate finding, verified

RV-7's F1 says the r3 entry's erratum (`r3…:41`) attributes to "`r3:24`" a
sentence that is r1's. Measured at four revs — `c418be0` (r3 landing),
`40de383`, `58c3db7`, `c625d5d` — `r3…:24` is always the Rv2TokenOpt RESULT
row, never "Creation blobs carry no runtime dispatch table"; that sentence is
`r1…:24` (and is corrected at `r1…:31`). **RV-7's F1 VERIFIED**; it is an
append-only corpus erratum opportunity, not a rule-15 blocker. RV-7's draft
avoids propagating the pointer.

### 4.5 Minor rationale correction (peer, verified)

SC-3 §2 says candidate (b) (coupled-landing discipline) lacks citable corpus
grounding. There are in-corpus anchors: `corpus/knowledge/2026-10-13-ghidra-install.md:74-76`
("repaired to 34 in the same commit as this erratum … coupled PROVINCE
repair") and `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-57`
("superseded at the same commit … landing commit `40de383` writes …"). RV-8's
minor correction is right; it does not affect the chosen rule.

## 5. Peer reconciliation

| chain | artifact | my reconciliation |
|---|---|---|
| c1 | **PL-4** | canonical; frozen a/b/c verified first-hand (§2). EX-3's apply receipt and RV-1's matrix agree; PL-2 (current) and RV-3 (updated) both recommend landing PL-4. |
| c1 | PL-2 | its prior register design is archived under `PL-2/prior-attempt/` and is blind to stripped bullets (PL-1 battery: `seed-required` PASS); its current artifact is a PL-4 endorsement + optional 2-row hardening. Do not land the prior design. |
| c1 | RV-3 | alternate 13-row/3-class register, round-trip sha `8e420679…` verified; superseded by its own landing recommendation for PL-4. |
| c1 | PL-1 | evidence-only hardening of PL-4 (748-line gate, `7724adcc…`); closes the reflow + extra-literal gaps I measured; queue as a follow-up, not a second base patch. |
| c2 | **EX-7** | canonical; verified + 85/85 measured; fix the CBOR text-length byte before landing. EX-9 independently compiled and verified the same claims (and found the same CBOR typo). |
| c3 | **SC-3** | canonical draft; two anchor corrections; recommended corrected bytes `a1bceb40…`. EX-14/EX-15/EX-16/RV-5/RV-6/RV-8/SC-1/SC-4 independently converge on the same corrections. |
| c3 | RV-7 | alternate rule (different wording, 6 refs) that also verifies; do not co-land. Its r3 `:24` pointer finding is a separate valid erratum. |
| verdicts | VZ-4 | its point-in-time verdict is superseded on one axis: C2 was PENDING there and is now delivered/verified (85/85). Its C1 audit was of RV-3's patch, not PL-4's — §2 closes that gap; its C3 `:34→:29` correction is confirmed. |

## 6. Per-item verdict table

| # | item | verdict |
|---|---|---|
| 1 | HEAD `c625d5d` / work `58c3db7` | VERIFIED (first-hand) |
| 2 | Gate sha `d0772ce8…`, 610 lines; PROVINCE 162 / SKILL 390 / SCORECARD 1696 | VERIFIED |
| 3 | Command A baseline 84/84, missing [], dangling [], 14 rules, depth 10.0 at both revs | REPRODUCED |
| 4 | SCOPE PROVINCE rows exactly 7; Frontier `(73,93)` and `(133,162)` uncovered | VERIFIED (module import) |
| 5 | v10 clean PASS; v10 blind on the seeded EVM literal | REPRODUCED |
| 6 | PL-4 patch identity `80027570…`, 713 lines, applies to pristine | REPRODUCED |
| 7 | PL-4 clean tree PASS, 14 rows, counters/SCOPE unchanged (17/17 keys) | REPRODUCED |
| 8 | PL-4 catches the frozen seeded literal: FAIL exit 1, `FRONTIER-STALE` | REPRODUCED |
| 9 | PL-4 stripped-required arm: FAIL `FRONTIER-UNEVALUABLE` | REPRODUCED |
| 10 | Frontier visible stale pin still fails `undeclared=1` under both instruments | REPRODUCED |
| 11 | PL-4 residual "insertions inside 132-162 are caught" | **CORRECTED** — reflow133 PASSes PL-4; RV-3's `ins132` agrees |
| 12 | PL-4 residual "only on-record literals declared" | **CORRECTED (incomplete)** — wall literal (:139-144) and RV-3's `stale159` PASS PL-4 |
| 13 | PL-1 delta closes reflow + wall literal (`FRONTIER-ANCHOR` / `FRONTIER-STALE`) | REPRODUCED (748 lines, `7724adcc…`) |
| 14 | RV-3 patch identity `8e420679…` (712 lines) | REPRODUCED (independent round-trip) |
| 15 | EX-7 entry exists; source `f5391167…`; three leg hashes/sizes | VERIFIED |
| 16 | EX-7 fourth dispatcher class: 14 EQ legs, stride 11, ascending dsts 253-982, SUB leg `ee02438e`→14 | REPRODUCED (my own decoder) |
| 17 | Control legacy class: unsorted GT/EQ, 15 EQ legs, no SUB leg | REPRODUCED |
| 18 | Seven probe envelopes: 15/15 real legs; both trap classes | VERIFIED (parsed) |
| 19 | Live 6.4.0 probe: 15/15, decoded sha `2ec3f557…`, id `ev_71da9d37…` | REPRODUCED (live) |
| 20 | Mutability 14/15; `scale(uint256,uint256)` pure→view | REPRODUCED |
| 21 | Runtime embedded in creation at +43, creation 1,560 B | REPRODUCED |
| 22 | Command A with entry+token: 85/85, missing [], dangling [] | REPRODUCED (scratch repo) |
| 23 | EX-7 CBOR trailer `73 736f6c63` | **CORRECTED** — actual byte `64`; substantive claim stands |
| 24 | SC-3 draft identity 1,605 B / 23 lines / `763c44b5…` | REPRODUCED |
| 25 | SC-3 landing: rule_blocks 14→15, 15/15 resolved, both revs | REPRODUCED |
| 26 | SC-3 citation `r4:34` for the limitation quote | **CORRECTED** → `:29` |
| 27 | SC-3 `r1:24` used for byte-containment | **CORRECTED (precision)** → containment is `:31`; `:24` states the retracted claim |
| 28 | Corrected candidates `6967b1e3…` (F1 only) and `a1bceb40…` (F1+F2) | REPRODUCED (bytes + 15/15 landing) |
| 29 | RV-7 draft `ccbc5cdb…` 1,565 B, 6 refs, 15/15 | REPRODUCED |
| 30 | RV-7's r3 `:24` dangling-pointer finding | VERIFIED at four revs |
| 31 | SC-3 §2 rationale vs candidate (b) corpus anchors | CORRECTED (minor; peers agree) |
| 32 | Integrated end-state (entry+token+corrected rule) 85/85, 15/15, 10.0/10.0 | REPRODUCED (scratch rev `0193666`) |

## 7. Landing recipe for the parent (single consistent set)

**C1** — land PL-4 unchanged:

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
patch .ufo/gates/c1-census-v10.py < .ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum .ufo/gates/c1-census-v10.py   # expect 8002757078a685f5…e18d14aecca, 713 lines
python3 .ufo/gates/c1-census-v10.py --quiet  # PASS, "FRONTIER register (G21): 14 rows asserted, errors: []"
```

Record in the landing receipt: the two residual corrections from §2.3 and,
optionally, PL-1's measured hardening as a follow-up (separate diff
`PL-1/patch-pl4-to-pl1.diff`, 16 rows, sha `7724adcc…`; re-run clean +
reflow133 + wall-seed arms).

**C2** — land EX-7's entry with two text fixes, then the map token:

1. Copy `EX-7/entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md` to
   `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md`.
2. Fix the CBOR byte in line 28 (`73 736f6c63` → `64 736f6c63`); normalize the
   leading comment (drop the `DRAFT`/`LAND-MOVE` instruction lines).
3. Append the token `2026-10-19-arc3-r6-viair-dispatch-shape` to the EVM row
   `corpus/README.md:38` exactly as in `EX-7.md` §3.
4. `REV=HEAD` command A → expect `knowledge_files=85, mapped=85, missing=[],
   dangling=[], coverage_score=10.0` (measured in simulation).

**C3** — land exactly one corrected rule-15 bullet:

Append the `a1bceb40…` bytes (`CR-8/rule15-SC-4-recommended.txt`, byte-equal
to SC-4's §6 recommended block) after the rule-14 bullet, before `##
Config custody`. Command A → expect `rule_blocks=15,
citation_resolved_rules=15, depth_score=10.0`. Do not also land RV-7's
`ccbc5cdb…` bullet.

**Integrated projection (measured, scratch rev `0193666`):** all three
landings together read `knowledge_files=85, mapped=85, missing=[], dangling=[],
rule_blocks=15, citation_resolved_rules=15, coverage_score=10.0,
depth_score=10.0`. The c1 gate landing is orthogonal to command A.

## 8. Scope, limits, what I did not do

- Did not modify the gate, PROVINCE.md, SKILL.md, SCORECARD.md, LOG.md,
  corpus, or any tracked file; git read-only. No landing was done by this seat.
- Did not re-derive every peer artifact: PL-1 (evidence-only), EX-3 and RV-1
  (evidence-only) were spot-audited; PL-2/RV-3/RV-7/VZ-4 were re-measured only
  at the points the convergence verdict depends on (patch round-trips, landing
  recommendations, the `:34→:29` correction, the r3 `:24` finding).
- Snapshot is point-in-time (~14:02); 32 seats were still absent. Later
  arrivals do not change the three delivered claims' measured verdicts, but a
  later seat could supersede a peer recommendation.
- `--root` scratch runs read live HOME configs for anchors (read-only); v10
  and r10 share that input, so the comparisons stand.
- The live probe was run once at 6.4.0 with a disk-backed `TMPDIR`; the 6.7.0
  leg was verified from the sealed envelope, not re-run live by me.
