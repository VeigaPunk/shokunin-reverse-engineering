# VZ-1 — arc3-loop1-round6 convergence verdict: C1/C2/C3 re-derived, corrections named

Seat VZ-1, verdicts/convergence chain, wave arc3-loop1-round6, 2026-10-19.
Repo state at every direct check: HEAD `c625d5de57e045188b5ce8cd450a57b349f90785`
(`c625d5d`, records; work `58c3db7` two entries below in `git log --oneline`),
gate `.ufo/gates/c1-census-v10.py` sha256
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`, 610 lines.
Every number below is my own measurement this session (rule #14); peer artifacts
are cited only as convergence observations, never as evidence. Scratch was
`/var/tmp/vz1-r6/` (never `/tmp`; EDQUOT avoided). Writes are confined to
`claims/verdicts/VZ-1.md` + `claims/verdicts/VZ-1/`; no tracked file, gate,
corpus, SKILL.md, PROVINCE.md or SCORECARD.md was modified; git was read-only
(only local commits in throwaway clones under `/var/tmp/vz1-r6/clone*`).

## 0. Verdicts in one line

| Claim | Delivered artifact | My ruling |
|---|---|---|
| **C1 operability** — census Frontier blind spot | PL-4 `patch-v10-to-r10.diff` (in-place r10, `FRONTIER[]` register / G21) | **VERIFIED on frozen (a)(b)(c)** — round-trip `80027570…`, 713 lines; clean PASS; seeded stale literal FAIL `FRONTIER-STALE`; 17/17 JSON keys unchanged. **3 CORRECTIONS** to its residual prose: insertion shifts in the post-unlock region can pass silently; two other recorded pre-r5 literals have no FORBIDDEN arm; mixed-fault class reporting is exclusive. |
| **C2 coverage** — one named corpus Unknown | EX-7 `entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md` + EVM map token | **VERIFIED / REPRODUCED** — three compile legs byte-identical, dispatch class re-walked, 15/15 probes, traps reproduce, overlay measures 85/85, missing/dangling `[]`. **5 text CORRECTIONS** before landing; none changes a byte or a counter. |
| **C3 depth** — queue-drain rule #15 | SC-3 §4 draft (parsed-and-empty ≠ byte-absence) | **REPRODUCED** — draft is byte-exact 1,605 B / 23 lines / `763c44b5…`; landing reads `rule_blocks=15`, `citation_resolved_rules=15`, depth 10.0. **1 blocking CORRECTION**: `r4:34` → `:29`; corrected draft 1,605 B / `6967b1e3…` also lands 15/15. |

Combined after-state measured on one scratch tree (EX-7 entry + corrected
SC-3 rule): `knowledge_files=85, mapped=85, missing=[], dangling=[],
rule_blocks=15, citation_resolved_rules=15, coverage_score=10.0, depth_score=10.0`
(`/var/tmp/vz1-r6/clone` rev `82dd299`). Nothing is landed in the lane repo.

## 1. C1 — operability: the census Frontier blind spot

### 1.1 Before-state, re-derived first-hand

- **SCOPE covers PROVINCE only at 8-13/15-26/40-43/44/45-62/64-71/119-131.**
  Gate `:216-222` read directly; `## Frontier` at PROVINCE.md:73 and
  `### Round-4 frontier (post-unlock)` at :133; `wc -l PROVINCE.md` = 162. No
  row covers 73-93 or 133-162. **VERIFIED.**
- **v10 clean-tree baseline.** `python3 .ufo/gates/c1-census-v10.py --quiet`
  from the repo root → exit 0, `VERDICT: PASS (stale=0 ambiguous=0
  undeclared=0 unresolved=0)`, counts `PROVINCE.md 162/6`, `SCORECARD.md
  1696/9`, `SKILL.md 390/2`, floor 17/14/3, live anchors
  `{'devin':'6.5.0','omp':'6.5.0','kimi':'6.7.0'}`. **REPRODUCED.**
- **Blind spot.** My own seeded tree (`/var/tmp/vz1-r6/seeded-stale`, the
  frozen example literal "real solc/vyper-compiled bytecode untested"
  re-introduced into :91-93, line-count neutral): v10 reads **PASS exit 0**
  with counters byte-identical to clean. **REPRODUCED.**
- The historical by-hand-audit process itself is not derivable from artifacts;
  the operative half (region ungraded at HEAD) is reproduced. PARTLY, as PL-4
  also recorded.

### 1.2 PL-4 patch — frozen requirements

Round-trip: `patch` of `claims/c1/PL-4/patch-v10-to-r10.diff` onto a pristine
`git show HEAD:.ufo/gates/c1-census-v10.py` copy →

```
8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca  713 lines
```

= PL-4's claimed identity; `diff` of the SCOPE tables is empty (**byte-identical**).

| Frozen requirement | My measurement |
|---|---|
| (a) clean tree still PASS | real repo root: exit 0, `FRONTIER register (G21): 14 rows asserted, errors: []`, `DECLARED FAIL CLASSES: []`, VERDICT line unchanged. Clean scratch tree: same. |
| (b) seeded stale literal FAILs / named disposition | `seeded-stale` → exit 1, `DECLARED FAIL CLASSES: ['FRONTIER-STALE']`, errors name `PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested'`. Stripped-required arm → exit 1, `['FRONTIER-UNEVALUABLE']`; 161-line truncation → exit 1, `['UNREADABLE','FRONTIER-UNEVALUABLE']` with `PROVINCE.md: 161 lines < declared max 162 (rows beyond EOF)`. |
| (c) existing SCOPE rows / counters intact | `--json` clean: 17 shared keys, **0 mismatched**; r10-only keys `['frontier_errors','frontier_rows']`; `counts` equal; `current_ok_per_file {'PROVINCE.md':17,'SCORECARD.md':14,'SKILL.md':3}`. |

All three frozen sub-claims **REPRODUCED**. Full runs: `VZ-1/c1-arms.txt`.

### 1.3 Corrections to PL-4's residual claims (measured, not inherited)

**C1-CORR-1 — insertions in the post-unlock region are not caught.** PL-4 §6.1
says "Insertions anywhere inside :73-162 are caught … inside :132-162 they
shift register spans (REQUIRED-absent)". Measured on trees built by VZ-1
(content-asserted insertions, line-count +1):

| insertion at | v10 | PL-4 r10 |
|---|---|---|
| `:94` | PASS | FAIL — G15 marker at :119 shifted (`scope_errors`) |
| `:125` | PASS | **PASS exit 0**, register errors [] |
| `:132` (blank before the post-unlock header) | PASS | **PASS exit 0** |
| `:133` (header line) | PASS | **PASS exit 0** |
| `:135` (before the first post-unlock bullet) | PASS | **PASS exit 0** |
| append past `:162` | PASS | PASS — the named past-the-bound residual |

So the §6.1 claim is **CORRECTED**: a one-line shift beginning in the
`:120-:134` window (measured points above) leaves every REQUIRED pattern inside
its declared window and the run reads PASS. The register still grades the
declared text, but it can silently unregister the tail (old `:162` drifts to
`:163`). This is a fail-open shift, not a failure of the frozen falsifier.

**C1-CORR-2 — no FORBIDDEN arm for the other recorded pre-r5 literals.**
`git show 40de383 -- PROVINCE.md` shows three measured before-states: the EVM
"bytecode untested" line (guarded), plus the `>90 MB PE` remediation
(`Next: raise REA_GHIDRA_STARTUP_TIMEOUT_MS`) and the cross-version
"`compare-application-versions` still probe-refused since r2" line. I
re-introduced the cross-version literal into :160 while keeping `r12-02`/
`r14-01` intact (`stale159`): v10 **PASS**, PL-4 r10 **PASS exit 0**,
`frontier_errors []`. PL-4 §6.3 frames coverage as "literals on record"; only
the EVM literal is actually forbidden. **CORRECTED (coverage limit).**

**C1-CORR-3 — mixed-fault class reporting is exclusive.** On `seeded-stale`
three errors fire (two REQUIRED-absent + one FORBIDDEN) but
`declared_fail_classes` is `['FRONTIER-STALE']` only; the UNEVALUABLE half is
visible only in `frontier_errors`/text. A reviewer sees one class, not the set.
Minor reporting granularity, not a requirement failure.

Non-blocking recommendation: PL-4's register rows are 5-tuples
`(file,start,end,required,forbidden)` with **no per-row corpus citation**; rule
#14 would favor adding a `cite` when the register is next re-keyed. Also note the
`seeded-mention` arm (a bullet that says "do not claim … untested") fails
FRONTIER-STALE — a literal-register false positive that fails closed.

### 1.4 Competing designs and convergence

At my first read the c1 chain held three competing r10 patch texts; all three
round-trip byte-exactly on my pristine gate:

- **PL-2 prior attempt** → `2d7ee95ba2743bde0b658c91d867a46e04e3e9e14de41d2cb60f2ff46238ce7b`
  (also byte-identical to its retained `c1-census-v10-r10-proposed.py`);
  design: two FRONTIER SCOPE rows + a 3-literal register. It catches the frozen
  seed, but **not** a stripped-required bullet (my `seeded-required` → PASS) and
  not my reflow-135 arm. Its patch later moved to `claims/c1/PL-2/prior-attempt/`.
- **RV-3 prior attempt** → `8e4206796fec2e16fb6f2c1959f33b63bbcb9643471d42472ac6bc2cba195ebf`;
  design: 13 anchored rows (`FRONTIER_REGISTER`) with anchor line/regex,
  required, forbidden, cite. It caught every one of my eight structural arms
  (`seeded-stale`, `seeded-required`, `truncated`, `reflow94/125/132/133/135`)
  with FRONTIER-ANCHOR/STALE/UNATTESTED. Preserved at
  `claims/c1/RV-3/prior-attempt.md` after RV-3 pivoted to verification.
- **PL-4** (the delivered artifact) → `80027570…`; 14 rows, required+forbidden,
  no anchor line. Meets the frozen claim; gap C1-CORR-1 above.

Point-in-time convergence: the c1 chain's 12 seat artifacts (PL-1..4, EX-1..4,
RV-1..4) now verify PL-4; the independent corrections reported by PL-2
(insertions at :133/:134/:150), PL-3 (insertion points after :119) and RV-3
(insertion at :132) agree with my measured window. Peer measurements are
convergence only, not my evidence.

**C1 ruling:** PL-4's patch **satisfies the frozen claim** and is the wave's
converged artifact. Land it as-is if the corrected residual list is recorded in
the landing receipt (not inline — the gate's own rule-#14 discipline). If a
strict instrument is wanted next round, the cheap strengthening is RV-3's prior
design: per-row anchor line + cite, plus FORBIDDEN rows for the two other
`40de383` before-states. Those are not frozen requirements.

Landing recipe (expected):
```
patch .ufo/gates/c1-census-v10.py < claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum .ufo/gates/c1-census-v10.py    # 8002757078a685f5…e18d14aecca, 713 lines
python3 .ufo/gates/c1-census-v10.py --quiet  # exit 0, PASS, 14 rows, errors []
```

## 2. C2 — coverage: the named viaIR Unknown

### 2.1 Baseline and Unknown

- Command A at `c625d5d` (and `58c3db7`) → `knowledge_files=84, mapped=84,
  missing=[], dangling=[], rule_blocks=14, citation_resolved_rules=14,
  coverage/depth=10.0`. **REPRODUCED** (verbatim SCORECARD.md:88-124 recipe,
  run against immutable Git objects; `VZ-1/c2-recompile-walk.txt`).
- The Unknown is open at HEAD: `grep -n -i viaIR corpus/knowledge/*.md` →
  `2026-10-19-arc3-r3-evm-optimizer-shapes.md:33` and
  `2026-10-19-arc3-r4-evm-vyper-leg.md:28`, both in Unknowns lists.
  **VERIFIED.**

### 2.2 Independent rebuild — byte-exact

My own standard-JSON driver (`/var/tmp/vz1-r6/compile-vz1.js`) recompiled
EX-7's source (`f5391167…80cbbe`) with the wave-1 receipted
`solc 0.8.37+commit.f401782d.Emscripten.clang` (soljson `221d7a66…abad4c`,
package `b3a90035…33491`):

| leg | my runtime | my creation |
|---|---|---|
| viair-opt200 (viaIR + runs 200) | 1,517 B `2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a` | 1,560 B `d85fdde9…83d5` |
| viair-noopt (viaIR, optimizer off) | 4,144 B `0cc6938cd768199159cbed74a7e9f5bd4273c583afbf6babca643b0ffdbd29b4` | 4,318 B `f1125049…4063` |
| std-opt200 (viaIR unset, runs 200) | 1,921 B `c2ceabb163ad9c1e6d88244c29c5187602eaf4c810029d0018e76eb9643f7e27` | 1,966 B `4541fd49…c5d9e` |

All six size/hash pairs are identical to EX-7's retained files. ABI and
method-identifiers are semantically identical (my serialization differs from
the retained files by a trailing newline; EX-7's byte hashes `63fcf52f…`/
`c32e2ef2…` are those files' bytes).

### 2.3 Dispatch walk — my own decoder, no EX-7 code

viair-opt200 (1,517 B, 990 ops, 19 PUSH4 sites):

- head `6080604052 6004 36 10 15 61 0022 57 5b 36 15 61 0018 57 5f80fd 5b …` —
  `PUSH1 4 CALLDATASIZE LT ISZERO PUSH2 0x22 JUMPI`: **inverted guard** (the
  legacy control has `60043610 61 00e7 57`, no `ISZERO`).
- **14 EQ legs** at pcs 41..184, stride `[11]×13`, selectors ascending, dsts
  `[982,935,771,723,694,631,572,485,425,374,340,311,272,253]` — all JUMPDESTs.
- **15th leg** `PUSH4 ee02438e SUB PUSH2 0x000e JUMPI` at pc 194; dst 14 is the
  guard's router JUMPDEST. Post-SUB bytes `34 61 00f9 57 …` (opt200) /
  `61 05a9 56` (noopt) at 204.
- 15/15 selectors match solc `methodIdentifiers`; non-selector PUSH4s are
  `4e487b71` ×2, `0c2eae8d`, `3c3332b9` — none reported as functions.
- viair-noopt: same shape, 14 EQ dsts 208-273, SUB leg at 194.
- std control: 15 EQ (unordered, gaps 11/15/26), **3 GT legs** with pivots
  `6e69f38c` (pc 19), `90ab171e` (30), `3f4ba83a` (137); those three selectors
  appear twice and are deduplicated; 18 selector sites / 15 distinct.
- Probe offsets on viair-opt200: 14/15 equal their EQ `PUSH2` dst; the 15th is
  204 = `push4_pc+10`, not a JUMPDEST — EX-7's fifth offset convention.

### 2.4 Probes, traps, inference delta

Cached `rea-agents@6.4.0` (`~/.npm/_npx/dea9475797100b20`), disk-backed TMPDIR:

| leg | result |
|---|---|
| viair-opt200 raw + hex | **15/15**, `dispatch:"abi"` ×15, decoded `2ec3f557…` |
| viair-noopt raw | **15/15**, decoded `0cc6938c…` |
| std-opt200 raw | **15/15**, decoded `c2ceabb1…` |
| TRAP: raw fed the hex *text* | exit 0, **0 functions**, decoded sha = the hex text's own `19838d66…` |
| creation raw + hex | exit 0, **0 functions**, decoded `d85fdde9…`; runtime byte-embedded at **+43** (unique), 0 trailing bytes |
| mutability delta | **14/15**; sole divergence `scale(uint256,uint256)` ABI `pure` → inferred `view`; 0 payable-reads |
| CBOR tail | `a2 64 "ipfs" 58 22 … 64 "solc" 43 000825 00 33` (solc 0.8.37) |

Evidence ids are **path-keyed**: my runs at the retained artifact path mint
stable ids different from EX-7's envelopes, whose ids are tied to
`/var/tmp/ex07-r6/…` (EX-7's Unknowns already declare this; compare by decoded
sha, per `corpus/QUALITY.md` #15). A peer recheck of the retained path produced
the same id as mine (`ev_71da9d37…`), corroborating the path-keying.

### 2.5 Landing projection — measured, not quoted

Scratch clone at `c625d5d` + EX-7's entry + the EVM map-token patch (applies
cleanly to `corpus/README.md:38`) → command A at the local commit `d5ad52d`:
`{"knowledge_files": 85, "mapped": 85, "missing": [], "dangling": [],
"coverage_score": 10.0, "rule_blocks": 14}`. **85/85 REPRODUCED.**

### 2.6 Corrections before landing (text only; substance unaffected)

1. **Function count.** Entry line 16 says "14 explicit external functions +
   `receive()`". The source has **15** `function` declarations and the ABI has
   17 entries = 15 functions + constructor + receive; the selector chain is
   14 EQ + 1 SUB = 15 legs. K=15 and 15/15 are correct; only "14" is wrong.
2. **File count.** §4 says "42 files": `find` measures **46**
   (src 1 + scripts 5 + evidence 8 + out 24 + probe 7 + entry-draft 1).
3. **Cross-reference.** The entry says `0c2eae8d` appears in the r3 VaultB
   census; `grep -rn 0c2eae8d corpus/` → **0 hits**. `3c3332b9` is at r3:26;
   `0c2eae8d` is first recorded by this entry's own bytes.
4. **Byte-14 semantics.** Entry calls dst `0x000e` "the guard's small-calldata
   revert-path JUMPDEST". Bytes `[14:26] = 5b 36 15 61 0018 57 5f 80 fd 5b`:
   zero calldata jumps to `0x18` (receive), 1-3 bytes and selector mismatch
   fall through/return to revert (or `fallback` when one exists). It is a
   calldata-size **router**, not only a revert path.
5. **CBOR byte.** Entry line 28 prints `73 736f6c63` for the `solc` key; the
   actual tail is `64 736f6c63` (CBOR text(4)). `73` would be text(19).

### 2.7 Second viaIR carrier (convergence check, my walk)

EX-6's pre-existing carrier (a *different* source: 12 selectors + receive +
fallback, `ViaIRVault.viair-opt200.runtime.bin` 1,127 B) walks as **11 EQ legs
at stride 11, ascending, plus a final `PUSH4 f43cc773 SUB PUSH2 0x000e JUMPI`**
at pc 302; `f43cc773` is the largest selector, post-SUB `34 61 0154 57 …`.
So the fourth class is not a one-carrier artifact. (EX-6.md is a verification
artifact with its own new fallback-bearing carriers; it is not a duplicate
entry and does not add a second corpus file.)

**C2 ruling:** EX-7's entry **reproduces end-to-end**; it is land-ready after
the five text corrections. Do **not** land a second c2 entry this round if the
frozen `84 → 85` is to hold: the chain now holds five distinct Vyper
optimizer-form drafts (EX-5/EX-8/EX-10/EX-12/CR-2, two filenames, five hashes);
EX-10's own artifact states both-landing measures **86**. Land EX-7 only; hold
the Vyper forms entry for the next round and choose exactly one of its drafts
if it lands (EX-10's is the most complete, with a both-landing projection).

## 3. C3 — depth: rule #15 (parsed-and-empty ≠ byte-absence)

### 3.1 Baseline and draft identity

- `c625d5d:SKILL.md` craft section → **14** rule blocks, first
  "Evidence ids are content-addressed…", last "An artifact that records its own
  byte-identity…", ending "never a carried-over number." Command A 14/14.
  **REPRODUCED.**
- SC-3 §4 fenced bytes: **1,605 B, 23 lines, sha256
  `763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1`** —
  exactly SC-3's self-identity. **REPRODUCED.**
- Corrected draft (peer EX-14, re-hashed by me): **1,605 B,
  `6967b1e3e7fbdb43492e191426399c0311ab3bf85ee307f1a181a3edd235511e`**; diff vs
  the §4 bytes is exactly one token on line 21.

### 3.2 Landing simulation

Inserted after rule 14, before `## Config custody` (the §4 landing spec), on a
scratch clone that also carries EX-7's entry:

| rev | rule_blocks | citation_resolved_rules | depth_score | knowledge_files/mapped |
|---|---|---|---|---|
| `d5ad52d` (before rule) | 14 | 14 | 10.0 | 85/85 |
| `0a8ec41` (SC-3 as drafted) | **15** | **15** | 10.0 | 85/85 |
| `82dd299` (corrected `:29`) | **15** | **15** | 10.0 | 85/85 |

The new rule parses as exactly one block and is the 15th/last. **REPRODUCED.**

### 3.3 Citation audit — one blocking correction

Eight pattern citations in the draft; all resolve in-bounds, but one content
pointer is wrong:

- **`r4:34` → `:29` (CORRECTED, blocking).** The quoted tool limitation "empty
  results do not prove absence of dispatch" lives at
  `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:29` (the Limitations
  bullet); `:34` is `## Erratum (arc3-loop1-round5 correctness sweep,
  append-only)`. Command A is bounds-only, so the rule still resolves 15/15 —
  but the landed text would point readers at the wrong line. Land the corrected
  draft.
- **Minor precision (not blocking):** the draft attaches "blobs that
  byte-contain the full runtime" to `r1:24`; `r1:24` records the 0-function
  probe and the (later corrected) "no runtime dispatch table" sentence, while
  the embedding is measured at `r1:31`. The next sentence already cites `:31`,
  so the pair is defensible; splitting the citation would be cleaner.
- The other six citations (`r1:31`, `r3:41-51`, `r4:39-46`, `r4:17`, `r3:27`,
  `r4:25`) check out at the named lines; `corpus/QUALITY.md:21` (outside the
  pattern) is the row-11 gate text.

### 3.4 Rule content — byte census re-derived

CarrierV from the retained r4 evidence (read-only):
`creation.bin` 1,637 B `3c667396…a226`; `runtime.bin` 1,562 B `57d6fd0a…dae0`;
`runtime.hex` decodes byte-identically; runtime occurs once at **+20** with
**55** trailing bytes. The sealed r4 envelope
`EX-06/probe/CarrierV-creation-6.4.0.json` reports 0 functions with decoded sha
`3c667396…`; the r1 envelope `RV-2/probe-creation-hex-6.4.0.json` reports 0
functions. Probe 0 vs bytes present — the rule's core instance **VERIFIED**.

### 3.5 Corpus-side finding (verified, not inherited)

The r3 entry's erratum at `:41` claims to correct "`:24` 'Creation blobs carry
no runtime dispatch table'". At HEAD `:24` is the `Rv2TokenOpt` result row;
`grep -n 'Creation blobs'` finds the sentence **only inside the erratum at
:41**; at the round-3 landing `c418be0` there is **no match** at all. The quoted
sentence is r1's (`r1:24`). This is a dangling pointer in the corpus, not in
SC-3's draft (which does not repeat it). Queue an append-only re-pointer for a
later round.

**C3 ruling:** SC-3's rule **meets the frozen falsifiable** (14 → 15 with
citations resolving) and the content is first-hand verified. Land the
one-token-corrected draft (`EX-14/rule15-corrected.md`, `6967b1e3…`), not the
uncorrected §4 bytes. RV-7's alternative rule draft (1,565 B `ccbc5cdb…`, 15/15
on an 84/84 tree) is a valid different rule but must not be landed alongside
SC-3 — two rule-15 bullets would make `rule_blocks=16`.

## 4. Peer reconciliation (point-in-time, ~14:05 -03:00)

| Chain | Peers present | Convergence |
|---|---|---|
| c1 | PL-1..4, EX-1..4, RV-1..4 (12 artifacts) | All now verify PL-4. PL-2 reports insertions at :133/:134/:150, PL-3 insertion points after :119, RV-3 insertion at :132 — my independent window (:125/:132/:133/:135) agrees. PL-2's and RV-3's earlier competing patches are preserved under `prior-attempt*`; my round-trip shas for them (`2d7ee95b…`, `8e420679…`) are recorded in `peer-crosscheck.txt`. |
| c2 | EX-6, EX-9, CR-3 verification artifacts; EX-5/8/10/12/CR-2 entry drafts | EX-6 independently verifies EX-7 with four prose corrections; I re-derived all four (function count 15, 46 files, `0c2eae8d` absent, byte-14 router) and add the fifth (CBOR `73`/`64`). The five Vyper drafts are distinct bytes; only one c2 entry should land for 84→85 (EX-10 itself says both = 86). |
| c3 | EX-13..16, RV-5..8, SC-1/2/4 (verification) | All converge on `r4:34` → `:29`; several supply corrected drafts. EX-14's corrected 1,605 B / `6967b1e3…` was re-hashed and re-simulated by me. RV-7's separate draft is an alternative, not the frozen deliverable. |
| verdicts | VZ-2, VZ-4, CN-1/2/4, CR-5..8 present | VZ-4's final poll (14:00) rules the same three claims: PL-4 reproduced with the insertion correction, EX-7 85/85 with a CBOR `73`→`64` text fix, SC-3 with `:34`→`:29` and the `r1:24` wording note. My artifact is independent and reaches the same rulings; VZ-4's earlier 13:14 "C2 PENDING" is closed by the measured 85/85 overlay here. |

No conflict of substance was found between the delivered artifacts and the
peers; the only reconciliation decision is the c2 one-entry limit above.

## 5. Per-item verdict table

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | HEAD `c625d5d`, work `58c3db7` | VERIFIED | `git rev-parse HEAD`; `git log --oneline` |
| 2 | Gate sha `d0772ce8…`, 610 lines; SCOPE :216-222 exactly the frozen list | VERIFIED | `c1-arms.txt` §custody |
| 3 | Frontier 73-93 + 133-162 UNDECLARED | VERIFIED | gate `:216-222`; PROVINCE.md:73/:133; 162 lines |
| 4 | v10 clean PASS 162/6, 1696/9, 390/2, floor 17/14/3 | REPRODUCED | `c1-arms.txt` |
| 5 | v10 blind to the stale :91-93 literal (PASS exit 0) | REPRODUCED | `c1-arms.txt` arm matrix |
| 6 | PL-4 patch identity `80027570…`, 713 lines; SCOPE byte-identical | VERIFIED | `c1-arms.txt` §patch |
| 7 | Frozen (a): r10 clean PASS, 14 rows, errors [] (real root + scratch) | REPRODUCED | `c1-arms.txt` |
| 8 | Frozen (b): seeded stale literal FAIL `FRONTIER-STALE`; stripped-required FAIL `FRONTIER-UNEVALUABLE`; truncation FAIL `UNREADABLE` | REPRODUCED | `c1-arms.txt` |
| 9 | Frozen (c): 17 shared JSON keys, 0 mismatch; 2 additive keys; counts/floor equal | REPRODUCED | `c1-arms.txt` |
| 10 | PL-4 §6.1 "insertions inside :132-162 caught" | **CORRECTED** | insertion at :125/:132/:133/:135 → PASS exit 0 |
| 11 | PL-4 §6.3 "literals on record" coverage | **CORRECTED** | `stale159` → PASS; second `40de383` literal unguarded |
| 12 | PL-4 mixed-fault declared classes | minor limitation | 3 errors, `['FRONTIER-STALE']` only |
| 13 | PL-4 per-row corpus citations | recommendation | rows are 5-tuples, no cite |
| 14 | Prior competing patches round-trip (PL-2 `2d7ee95b…`, RV-3 `8e420679…`) | VERIFIED | `c1-arms.txt` tail |
| 15 | Command A baseline 84/84, missing/dangling [], 14 rules | REPRODUCED | `c2-recompile-walk.txt` |
| 16 | viaIR Unknown open at r3:33 / r4:28 | VERIFIED | grep at HEAD |
| 17 | Three compile legs byte-identical (1,517/4,144/1,921 B; sha `2ec3f557…`/`0cc6938c…`/`c2ceabb1…`) | REPRODUCED | `c2-recompile-walk.txt` §recompile |
| 18 | Fourth dispatch class: inverted guard, 14 EQ legs stride 11 ascending, SUB final leg dst 0x0e, all dsts JUMPDEST | REPRODUCED | `c2-recompile-walk.txt` §walk |
| 19 | Legacy control: GT/EQ binary search, pivots `6e69f38c`/`90ab171e`/`3f4ba83a`, 15 EQ + 3 GT | REPRODUCED | same |
| 20 | Probe legs 15/15, decoded sha = runtime sha; raw-on-hex trap 0 fns; creation 0 fns with runtime at +43 | REPRODUCED | `c2-recompile-walk.txt` §probe |
| 21 | Mutability 14/15; `scale` pure→view; 0 payable-reads | REPRODUCED | same |
| 22 | Command A overlay 85/85, missing/dangling [] | REPRODUCED | same §command A |
| 23 | EX-7 entry text: 15 functions (not 14), 46 files (not 42), `0c2eae8d` not in r3, byte-14 router, CBOR `64` not `73` | **CORRECTED** (text) | `peer-crosscheck.txt` §c2; runtime bytes |
| 24 | SC-3 draft identity 1,605 B / 23 lines / `763c44b5…` | REPRODUCED | `c3-rule15.txt` |
| 25 | Rule 14 → 15, citation_resolved 15, depth 10.0 (as drafted and corrected) | REPRODUCED | `c3-rule15.txt` §command A |
| 26 | `r4:34` for the tool-limitation quote | **CORRECTED** → `:29` | `c3-rule15.txt` §citation audit |
| 27 | r3 erratum `:24` attribution | DISCREPANCY (corpus debt, not in SC-3's draft) | `c3-rule15.txt` §r3 |
| 28 | CarrierV census 1,637/1,562 B, +20, 55 trailing, hex==bin | REPRODUCED | `c3-rule15.txt` |
| 29 | Corrected draft `6967b1e3…` lands 15/15 | REPRODUCED | `c3-rule15.txt` |
| 30 | RV-7 alternative rule identity + 15/15 on 84/84 | VERIFIED (alternative, do not co-land) | `c3-rule15.txt` tail |
| 31 | c2 one-entry limit for 84→85 (five Vyper drafts; both = 86) | **CONVERGENCE DECISION** | `peer-crosscheck.txt`; EX-10's own projection |

## 6. Residuals and handoff

1. **Land C1:** apply PL-4's patch; expected `80027570…`, 713 lines, clean PASS.
   Record in the landing receipt the corrected residual list — insertion shifts
   in `:120-:134` can pass silently; FORBIDDEN coverage is the EVM row only;
   mixed faults name one class; register rows carry no per-row cite. A strict
   next-round variant is RV-3's anchored register (`prior-attempt.md`).
2. **Land C2:** copy EX-7's entry after the five text fixes (or fix in the same
   commit); add the EVM map token; expect 85/85 with `missing []`/`dangling []`.
   Do not land any of the five Vyper optimizer-form drafts this round if the
   frozen 84→85 is to hold; if the operator wants both, the count is 86 and the
   falsifiable must be restated. The entry's "fourth class / fifth convention"
   taxonomy versus r1/r3/r4 was not re-measured by me; my evidence is the
   same-session control and the second viaIR carrier walk.
3. **Land C3:** use `claims/c3/EX-14/rule15-corrected.md` (1,605 B,
   `6967b1e3…`), inserted after rule 14; expect `rule_blocks=15`,
   `citation_resolved_rules=15`, depth 10.0. Do not land RV-7's alternative
   rule in the same round.
4. **Corpus debt:** r3:41's `:24` pointer is dangling (r1's sentence, never in
   r3 at any measured rev). Fix append-only in a later round.
5. **Not done (by design):** no landing, no gate edit, no SKILL/corpus write;
   no re-measurement of the r1/r3/r4 carrier classes for the C2 taxonomy; no
   audit of every c2/c3 peer's numbers beyond the convergence points recorded.

## 7. Evidence and custody

- `VZ-1/c1-arms.txt` — gate custody, SCOPE rows, patch round-trip, full arm
  matrix (v10 vs PL-4 r10 over 12 trees), real-root run, JSON invariance,
  reflow/insertion probes, stale159, prior-patch identities.
- `VZ-1/c2-recompile-walk.txt` — toolchain digests, independent compile
  hashes/sizes, full walker output, probe table, embedding, mutability delta,
  command-A baseline/overlay, second viaIR carrier walk.
- `VZ-1/c3-rule15.txt` — draft identities (as-drafted and corrected), craft
  baseline, `:29`/`:34` and r3 `:24` audit, CarrierV census, 14→15 runs,
  RV-7 alternative.
- `VZ-1/peer-crosscheck.txt` — point-in-time peer inventory, prior attempts,
  the five EX-6 corrections re-derived, corrected-draft inventory.

Custody: lane gate sha before and after all experiments = `d0772ce8…d97b5`
(unchanged). `git status` shows only the pre-existing
` M .ufo/waves/arc2-loop1-round10/C3.md` and the untracked round-6 wave tree.
Scratch `/var/tmp/vz1-r6/` only; no `/tmp` writes. The only commits I made are
inside `/var/tmp/vz1-r6/clone` and `clone2` (throwaway clones), never in the
lane repo.
