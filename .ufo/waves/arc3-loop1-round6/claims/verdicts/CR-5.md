# CR-5 — verdicts/convergence: independent reconciliation of the three delivered artifacts + peers

Seat CR-5, verdicts/convergence chain, wave `arc3-loop1-round6`, 2026-10-19.
Repo HEAD `c625d5de57e045188b5ce8cd450a57b349f90785` (`c625d5d`, records; work
`58c3db7` beneath it) — re-derived this session with `git rev-parse HEAD` and
`git log --oneline -3`. Every number below is first-hand (lane rule #14); peer
artifacts are cited only as claims I tested, never as evidence. Scratch:
`/var/tmp/cr5-r6/` (never `/tmp`; EDQUOT standing rule). The live gate was never
edited: `sha256sum .ufo/gates/c1-census-v10.py` =
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` before and
after all work (610 lines). Git used read-only; the only writes are this artifact
and `claims/verdicts/CR-5/`. Evidence bundle: `claims/verdicts/CR-5/`.

Command A at both source commits (SCORECARD.md:88-124 recipe, run verbatim,
`CR-5/commandA-both.txt`):

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "c625d5d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "58c3db7", "rule_blocks": 14}
```

`git status --porcelain` before/after: only the pre-existing
` M .ufo/waves/arc2-loop1-round10/C3.md` and untracked `.ufo/waves/arc3-loop1-round6/`.

## 0. Rulings at a glance

| Delivered artifact | Ruling |
|---|---|
| **C1 — PL-4 r10 frontier register** | **VERIFIED** against frozen C1 (a)(b)(c): patch round-trips byte-exact, clean PASS, seeded reintroduction caught with a named class, counters intact. **Two measured coverage gaps** (one-line reflow fail-open; only one FORBIDDEN literal) — documented and quantified in §2.4; they do not void the frozen falsifiable. |
| **C2 — EX-7 viaIR corpus entry** | **VERIFIED / REPRODUCED** on byte identities, live 15/15 probe, independent dispatch walk, traps, creation embedding, Unknown provenance and 84→85 projection. **One CORRECTED item**: draft line 28's CBOR transcript says `73 736f6c63`; the byte is `64` (§3.6). |
| **C3 — SC-3 rule #15 draft** | **VERIFIED / REPRODUCED**: 1,605 B / 23 lines / `763c44b5…`; 14→15 with 15/15 citations at HEAD; core instance byte-exact. **Two CORRECTED anchors** to fix before landing: `r4:34` → `:29` (§4.3), and the `r1:24` containment clause (§4.4). |
| C1 peer — PL-1 merged build | **VERIFIED full battery**: PL-4 + 146-line delta → 748 lines, sha `7724adcc…`; closes all three measured holes. My recommended C1 landing (§2.6). |
| C2 peer — EX-9 | Independent verification of EX-7; its one correction (CBOR byte) is **CONFIRMED** by my own byte read (§3.6). |
| C3 peers — SC-2/SC-4/EX-14/EX-15/EX-16/RV-6 | Converge on the `:34`→`:29` correction; I confirmed it independently. RV-7's alternative draft also passes (§4.5). |

## 1. C1 — PL-4's r10 frontier register: verification

### 1.1 Round-trip and clean-tree requirement (a)

Pristine gate from `git show HEAD:.ufo/gates/c1-census-v10.py` (610 lines, sha
`d0772ce8…`); PL-4's `patch-v10-to-r10.diff` (182 lines) applies with
`patch -p0` and reproduces the claimed instrument exactly:

```
8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca  r10.py
713 r10.py
```

Scratch clean tree = byte-copies of PROVINCE.md/SKILL.md/SCORECARD.md at HEAD.
On that tree and on the real repo root (`--root` default), r10 reads exit 0:

```
FRONTIER register (G21): 14 rows asserted, errors: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

The `VERDICT:` line is byte-identical to v10's; the G21 count is a separate new
line. `--json` at the repo root (`CR-5/v10-repo.json`, `r10-repo.json`): **17
shared keys, zero value mismatches**, r10-only keys `['frontier_errors',
'frontier_rows']`, `counts` equal, `current_ok_per_file` `{PROVINCE.md: 17,
SCORECARD.md: 14, SKILL.md: 3}`, `frontier_rows: 14`, `frontier_errors: []`.
No SCOPE row is removed or edited: `diff` shows 5 replaced code lines and zero
removed `SCOPE` rows; every existing counter semantics is preserved.

### 1.2 Fault battery (requirement b) — my own trees, not PL-4's

Trees built this session from the HEAD copies, content-asserted edits
(`CR-5/arms.txt`):

| tree (my seed) | v10 | r10 |
|---|---|---|
| clean | PASS exit 0 | **PASS exit 0**, `14 rows, errors: []` |
| `seeded` — frozen literal `…real solc/vyper-compiled bytecode untested` back into :91-93 (keeps line count) | **PASS exit 0** (blind, copies v10) | **FAIL exit 1**, `['FRONTIER-STALE']`; errors: REQUIRED `solc-0\.8\.37`/`vyper-0\.4\.3` absent + `FORBIDDEN 'untested' matched 'untested'` |
| `seeded-only` — earned version tokens kept, `untested` added | PASS exit 0 | **FAIL exit 1**, exactly one error, `FRONTIER-STALE` |
| `required` — :91-93 replaced by `- **EVM bytecode (extended)** — see corpus.` | (v10 blind) | **FAIL exit 1**, `['FRONTIER-UNEVALUABLE']`, both REQUIRED patterns absent |
| `trunc` — PROVINCE.md truncated to 161 lines | **PASS exit 0** (silent content loss past :131) | **FAIL exit 1**, `['UNREADABLE', 'FRONTIER-UNEVALUABLE']`, `PROVINCE.md: 161 lines < declared max 162` |

The frozen claim's requirement (b) is met literally: the example literal is caught
with a named disposition, while the clean tree still reads PASS. Requirement (c)
is met as measured in §1.1.

### 1.3 Corrections to PL-4's residual claims

Two peer corrections are real; I re-derived both.

1. **One-line insertion fail-open (CORRECTED).** PL-4 §6.1 says insertions inside
   `:132-162` shift register spans → `REQUIRED-absent`. Measured false for a
   single inserted blank line before `:133`: PROVINCE.md becomes 163 lines,
   the spans shift by one, every REQUIRED token still falls inside its window
   (the spans have ≥1 line of slack), and r10 reads **PASS exit 0**
   (`CR-5/arms.txt` reflow run; the shifted file's `:134` is the section header).
   The design silently grades shifted lines — exactly the class a census exists to
   prevent. `+2`/`+3` insertions do fail (`FRONTIER-UNEVALUABLE`), so the window is
   exactly one line plus the named past-the-bound append.
2. **Multi-class either/or (CORRECTION, minor).** The declared-class expression
   chooses `FRONTIER-STALE` when any forbidden hit exists, dropping
   `FRONTIER-UNEVALUABLE` for concurrently-absent REQUIRED anchors. Measured on
   my `seeded` tree: `declared_fail_classes: ['FRONTIER-STALE']` although two
   REQUIRED patterns were absent. The error list still names both; only the class
   label is narrower. PL-1's build reports both classes.

Neither correction touches requirement (a), (b) or (c); both are coverage/documentation
defects to fix before relying on the residual text.

### 1.4 Competing c1 designs — measured

Identities (all applied on scratch pristine copies; `CR-5/arms-competing.txt`,
`arms-postunlock.txt`):

| design | built size / sha | frozen seed | required-stripped | reflow +1 | wall+cross literals | trunc 161 | VERDICT line |
|---|---|---|---|---|---|---|---|
| **PL-4** | 713 L / `80027570…` | FAIL `FRONTIER-STALE` | FAIL `FRONTIER-UNEVALUABLE` | **PASS (fail-open)** | **PASS (not declared)** | FAIL `UNREADABLE` | identical |
| **RV-3** | 712 L / `8e420679…` | FAIL `STALE+UNATTESTED` | FAIL `FRONTIER-UNATTESTED` | FAIL `FRONTIER-ANCHOR` (13 per-row anchors) | **PASS** (only EVM forbidden) | FAIL `FRONTIER-UNATTESTED` | identical |
| **PL-2 prior attempt** (preserved at `claims/c1/PL-2/prior-attempt/`; current PL-2.md verifies PL-4 and archives it) | 705 L / `2d7ee95b…` | FAIL `FRONTIER-STALE` | **PASS** (no REQUIRED floor) | FAIL via scope marker | FAIL `FRONTIER-STALE` ×2 (on one-line forms) | FAIL `UNREADABLE` | **changed** adds `frontier=0` |
| **PL-1 merged build** | 748 L / `7724adcc…` | FAIL `STALE+UNEVALUABLE` | FAIL `FRONTIER-UNEVALUABLE` | FAIL `FRONTIER-ANCHOR` | FAIL `FRONTIER-STALE` ×2 | FAIL `UNREADABLE` | identical |

My `seeded-postunlock` tree keeps the current REQUIRED anchors and reintroduces the
two other measured-stale pre-`40de383` literals (`git show 40de383 -- PROVINCE.md`
shows both before-states): **PL-4 and RV-3 read PASS exit 0; PL-2 prior and PL-1's
build read FAIL**. The frozen claim only names the EVM literal, so PL-4 is not in
breach — but the debt's wording ("Frontier-region staleness claims become
gradable") is only fully served by a build that declares all three measured
literals.

PL-1's merged build is **PL-4 + `patch-pl4-to-pl1.diff` (146 lines)**; I applied
that delta to my PL-4 copy and reproduced `7724adcc…` byte-exactly. On my whole
battery it FAILs with named classes and clean-PASSes; its `--json` shares all 17
v10 keys with zero mismatches (adds `frontier_errors`/`frontier_rows`, 16 rows),
and its `VERDICT:` line is byte-identical. Its `frontier_errors` name both classes
on multi-class faults.

### 1.5 C1 verdict and recommendation

PL-4's delivered patch: **VERIFIED** against the frozen claim's three requirements,
with §1.3's two corrections to its residual text. It is not the strongest available
design, though: the one-line reflow fail-open means it can silently grade shifted
lines, and it declares only one of the three measured-stale literals.

**Recommendation (land exactly one c1 patch):** apply **PL-1's merged build**
(PL-4 + 146-line delta, sha `7724adcc…`, 748 lines), which I verified on the full
matrix. If the lane restricts landing to the three delivered artifacts, land
PL-4's patch and immediately queue two additive fixes — per-line/row anchors
(close the reflow hole) and the two extra FORBIDDEN patterns — and correct PL-4
§6.1's residual claim in the landing receipt. Do **not** land PL-2's prior attempt
(misses a stripped bullet, changes the `VERDICT:` line) or RV-3 alone (misses the
two post-unlock literals). My scratch-only two-line extension `r10-plus.py`
(catches both extra literals; clean PASS) is evidence the FORBIDDEN addition is
safe, not a competing complete design — it does not close the reflow hole.

Landing recipe (parent):

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
# 1) PL-4 base
patch .ufo/gates/c1-census-v10.py \
  < .ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum .ufo/gates/c1-census-v10.py   # expect 80027570…, 713 lines
# 2) PL-1's 146-line delta on that base
patch .ufo/gates/c1-census-v10.py \
  < .ufo/waves/arc3-loop1-round6/claims/c1/PL-1/patch-pl4-to-pl1.diff
sha256sum .ufo/gates/c1-census-v10.py   # expect 7724adcc…, 748 lines
python3 .ufo/gates/c1-census-v10.py --quiet  # expect PASS, 16 rows, errors []
```

(I verified this exact two-step sequence on a pristine copy:
`80027570…` → `7724adcc…`.)

## 2. C2 — EX-7's viaIR corpus entry: verification

### 2.1 Byte identities — REPRODUCED

From the delivered `out/` tree (sha256 first 16 hex; `CR-5/ex7-probe.json` and the
`evidence/manifest.sha256` check, which passed):

| leg | runtime | creation | ABI | method ids |
|---|---|---|---|---|
| `viair-opt200` | 1,517 B `2ec3f557f6f2fb22` | 1,560 B `d85fdde93b1fcb62` | 17 entries, sha `63fcf52f…` | 15 keys, sha `c32e2ef2…` |
| `viair-noopt` | 4,144 B `0cc6938cd7681991` | 4,318 B `f1125049532f0dd9` | same file sha | same file sha |
| `std-opt200` | 1,921 B `c2ceabb163ad9c1e` | 1,966 B `4541fd490eb46198` | same file sha | same file sha |

ABI: 15 functions + constructor + `receive` = 17 entries; method-identifier maps
are byte-identical across the three legs. `planted-K.json` has 15 functions, and
**planted set == probe set == method-identifier values** (15/15, zero mismatches).

### 2.2 Live probe — REPRODUCED 15/15

```
TMPDIR=/var/tmp/cr5-r6 npx -y rea-agents@6.4.0 inspect-evm-interface \
  .../EX-7/out/viair-opt200/runtime.hex hex --format json   → exit 0
raw_result.functions: 15, normalized_result.functions: 15
dispatch: {"abi"} only; decoded bytecode sha256 2ec3f557…; bytes 1517
offsets: [982,935,771,723,694,631,572,485,425,374,340,311,272,253,204]
evidence_id ev_71da9d37… (my path; path-sensitive id domain, as the entry states)
```

Trap legs, re-run this seat:

- `runtime.hex` fed as `raw` → exit 0, **0 functions**, decoded sha
  `19838d6680f1…` == the input file's own sha, 3,035 B (ASCII hex) — parsed-and-empty,
  not carrier absence.
- `creation.hex` fed as `hex` → exit 0, **0 functions**, decoded sha `d85fdde9…`
  (the creation's own sha), 1,560 B; the 1,517-B runtime is byte-exactly embedded
  at **+43**, one occurrence (`CR-5/ex7-creation.json`).

### 2.3 Independent dispatcher walk — REPRODUCED byte-for-byte

Own minimal EVM decoder over `runtime.bin` (not EX-7's script):

- viair-opt200 head `6080604052 60043610 15 61<0022> 57 …` — the `ISZERO` (0x15)
  after `LT`; 14 `DUP1 PUSH4 <sel> EQ PUSH2 <dst> JUMPI` legs at DUP1 pcs
  40…183 (selector immediates 41…184), **stride 11**, selectors strictly ascending,
  all 14 dsts JUMPDESTs; 15th leg `PUSH4 ee02438e SUB PUSH2 0x000e JUMPI` at
  push4 pc **194** (dst 14, the guard JUMPDEST).
- PUSH4 census: **19 sites = 15 selectors (15 distinct) + `4e487b71`×2, `0c2eae8d`,
  `3c3332b9`** — exactly the entry's list and pcs.
- viair-noopt: same topology (14 EQ legs, stride 11, ascending, SUB leg pc 194,
  17 PUSH4 = 15 + `4e487b71`×2).
- std-opt200 control: head `60043610 61<00e7> 57` (no `ISZERO`); **15 EQ legs with
  non-uniform gaps [11,15,26]** and **3 GT pivots** `DUP1 PUSH4 {6e69f38c@19,
  90ab171e@30, 3f4ba83a@137} GT` — binary search, not a linear scan; 22 PUSH4 =
  18 selector sites (15 distinct; the three duplicates are the GT pivots) + four
  non-selector constants. This is exactly the pipeline-controlled contrast the
  entry claims.

### 2.4 The finding — VERIFIED

The fourth dispatcher class (linear ascending EQ + `SUB`-terminated final leg,
`ISZERO` guard) is real and distinct from the legacy binary-search class on the
same source/optimizer; the prologue alone (`5f3560e01c`) does not identify the
pipeline — the compare tree does. Offset semantics: 14/15 are JUMPDEST handler
heads, the SUB-leg `mark` reports `push4_pc+10 = 204`, not a JUMPDEST/PUSH2
target. The 85/85 projection is measured on a scratch git repo seeded from HEAD
with the entry + EVM map token overlaid (`CR-5/c2-projection.txt`):

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 85, "mapped": 85, "missing": [], "rule_blocks": 14}
```

Provenance of the Unknown: `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:33`
and `…r4-evm-vyper-leg.md:28` both name "the `viaIR` pipeline" (grep, two hits);
no prior corpus entry measures its dispatcher. The entry closes it for solc 0.8.37
on this host and narrows the rest.

### 2.5 C2 verdict + one correction for landing

**VERIFIED / REPRODUCED** on every number I could measure; the entry is complete
and lands 84→85. **One CORRECTED item before landing:** draft line 28's CBOR
transcript reads `… 73 736f6c63 43 000825 …`; the byte before `736f6c63` is
`0x64`, not `0x73` (`runtime[1506] = 0x64`; a manual decode of the 51-byte trailer
gives `a2 64"ipfs" 58 22 1220<32> 64"solc" 43 000825` + length `0033`). EX-9 found
this independently; I confirm it first-hand. Fix the transcript (`73`→`64`) — a
one-character correction; it does not change any byte identity or the K/K result.

## 3. C3 — SC-3's rule #15: verification

### 3.1 Baseline and draft identity — REPRODUCED

`rule_blocks=14`, `citation_resolved_rules=14`, `depth_score=10.0` at both revs
(§0). Extracting the fenced draft bytes exactly from `claims/c3/SC-3.md` §4:

```
1605 bytes, 23 newline-terminated lines, sha256
763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1
```

— matches SC-3's self-identity claim. The draft parses as exactly one new
`- **` block (no stray block starts).

### 3.2 Landing falsifiable — REPRODUCED on scratch

Draft appended after SKILL.md rule #14 (before `## Config custody`) in a scratch
git repo seeded from HEAD; command A's exact rule split and citation resolver run
(`CR-5/c3-landing.txt`):

| variant | rule_blocks | citation_resolved_rules | depth_score | refs in rule 15 | unresolved |
|---|---|---|---|---|---|
| SC-3 as delivered | **15** | **15** | 10.0 | 8 | [] |
| SC-3 with `:34`→`:29` | 15 | 15 | 10.0 | 8 | [] |
| RV-7's alternative | 15 | 15 | 10.0 | 6 | [] |

### 3.3 Citation audit — one CORRECTED (the quote's line)

Every SC-3 citation resolves in-bounds; content checked at the named lines:

- `r4:34` is **`## Erratum (arc3-loop1-round5 correctness sweep, append-only)`**;
  the quoted limitation "empty results do not prove absence of dispatch" lives at
  **`:29`** (the Limitations bullet). **CORRECTED: `:34` → `:29`.** Command A is
  bounds-only, so this defect is invisible to the metric — precisely the
  "census-checked vs instrument-graded" gap the c1 claim targets. Independently
  confirmed here; SC-2/SC-4/EX-14/EX-15/EX-16/RV-6 report the same.
- Other anchors verified at the line: `r1:24` (0-function creation-leg result),
  `r1:31` (append-only erratum: "measured false … embeds the runtime"),
  `r3:27` (raw-on-hex-text trap, "a probe-input trap, not a carrier defect"),
  `r3:41-51` (the round-5 erratum with embedded-runtime offsets),
  `r4:17` (original uniformly parsed-and-empty sentence), `r4:25` (same trap on
  Vyper carriers), `r4:39-46` (erratum: "creation probes parse empty while the
  runtime bytes are present verbatim"), `QUALITY.md:21` (row 11, the
  parsed-and-empty vs excluded-from-inventory gate). All present.

### 3.4 Second correction — the `r1:24` containment clause (precision)

SC-3's sentence "The r1 creation legs probed 0 functions on blobs that
byte-contain the full runtime (`…r1…:24`)" can be read as citing `:24` for
byte-containment; `:24` actually asserts the opposite ("Creation blobs carry no
runtime dispatch table") and the containment is earned by `:31`/the r3 erratum.
**CORRECTED (wording):** keep `:24` for the 0-function probe, move the
containment clause to `:31` (or reword "…probed 0 functions (`:24`); the
round-3 census and the entry's `:31` erratum then measured that the runtime bytes
are present"). This is a precision fix, not a factual failure of the rule; SC-4,
RV-6, EX-15 arrive at the same reading, while EX-14 treats it as defensible.

### 3.5 The core instance — REPRODUCED first-hand

CarrierV (retained r4 EX-04 bytes, read-only): creation `1,637 B
3c6673966d821d9d…`, runtime `1,562 B 57d6fd0ae0da0019…`, `runtime.hex` decodes
byte-identical to `runtime.bin`, runtime embedded at **+20**, **55** trailing
bytes, one occurrence. Live probe of the same absolute creation.hex path:

```
exit 0; evidence_id ev_53732d0f8c67d15c… (== round-4 EX-06's sealed id at the
same path); functions 0; bytecode.kind "unknown"; decoded sha 3c667396… (1,637 B)
```

— the probe says 0 functions while the bytes contain the full runtime at +20.
The distinction is **VERIFIED**; the same-path id equality is same-path
determinism (SC-3 says so correctly), and the byte census is the independent half.

### 3.6 Competing draft — RV-7, and its F1 finding

RV-7's alternative bullet extracts to **1,565 B, 23 lines, sha `ccbc5cdb…`**,
6 refs, and also lands 15/15/depth 10.0. It avoids the `:34` mis-citation and adds
measured VaultB/CarrierV embedding numbers. Its F1 is **VERIFIED**: the r3 erratum
at `:41` says it corrects "`:24` 'Creation blobs carry no runtime dispatch
table'", but `git show` at `c418be0`, `40de383` and `58c3db7` shows r3:24 is the
Rv2TokenOpt RESULT row at every revision, and "Creation blobs" occurs in r3 only
at `58c3db7` — inside that erratum itself. The quoted sentence is r1's (`r1:24`),
already corrected at `r1:31`. So the r3 erratum's pointer is dangling; RV-7's
draft correctly does not propagate it.

### 3.7 C3 verdict + recommendation

SC-3's rule #15 is **VERIFIED** on its falsifiable and core evidence, with two
pre-landing corrections (§3.3, §3.4). **Land exactly one rule:** either SC-3's
draft with `:34`→`:29` (and the `r1:24` clause re-pointed), or RV-7's draft (which
needs neither fix and carries the extra measured byte numbers). Do not land both —
that would make `rule_blocks=16` and duplicate the lesson. My recommendation:
land SC-3's corrected draft (the delivered artifact; 8 refs, concise), unless the
integrator prefers RV-7's more explicit byte witnesses; both read
`rule_blocks=15, citation_resolved_rules=15, depth_score=10.0`.

## 4. Peer reconciliation (point-in-time, ~14:02 local)

- **VZ-4** (earlier convergence seat) audited RV-3 and SC-3 before PL-4/EX-7
  landed. Its C1 conclusion (RV-3 verified) is confirmed by me, but PL-4 and
  PL-1's build now supersede RV-3 on coverage; its C2 "PENDING" is now resolved
  by EX-7 (C2 **VERIFIED**), and its C3 correction (`:34`→`:29`) is confirmed.
- **PL-1, EX-3, RV-1** independently verify PL-4 and flag the one-line reflow
  hole; I reproduced both. PL-1's merged build is the only design I measured that
  passes the full battery (frozen seed, stripped anchors, both extra literals,
  reflow +1, truncation) while keeping the VERDICT line and all 17 JSON keys.
- **PL-2** revised its artifact: the current `PL-2.md` verifies PL-4 and archives
  its own prior competing patch under `prior-attempt/`. My §1.4 audit of that
  prior design is historical evidence; the seat's current claim agrees with PL-4.
- **EX-9** verifies EX-7 and finds the CBOR transcript byte error; I confirmed it
  from the runtime bytes (§2.5). No other EX-7 discrepancy surfaced in my checks.
- **c3 cluster** (SC-1/SC-2/SC-4, EX-13..16, RV-5/6/8): all converge on SC-3's
  draft with the `:34`→`:29` correction; RV-6/SC-4 add the `r1:24` precision
  point. RV-7's draft is a valid alternative; its F1 (dangling r3 `:24` pointer)
  is verified.
- **Not audited by this seat** (point-in-time; outside the three delivered
  artifacts): the c1 EX-1/EX-2/EX-4 directories, EX-9's full c2 evidence set, and
  the detailed c3 transcripts of SC-1/2/4 and RV-5/6/8. My ruling does not depend
  on them.

## 5. Per-item verdict table

| # | Item | Verdict |
|---|---|---|
| 1 | HEAD `c625d5d` / work `58c3db7` | REPRODUCED |
| 2 | Gate identity `d0772ce8…`, 610 lines, unchanged after all work | REPRODUCED |
| 3 | SCOPE covers PROVINCE only 8-13/15-26/40-43/44/45-62/64-71/119-131; Frontier 73-93+133-162 undeclared | VERIFIED |
| 4 | PL-4 patch round-trip → 713 lines, `80027570…` | REPRODUCED |
| 5 | PL-4 clean tree/repo PASS, 14 rows, errors [], VERDICT identical | REPRODUCED |
| 6 | PL-4 seeded frozen literal: v10 PASS / r10 FAIL `FRONTIER-STALE` | REPRODUCED |
| 7 | PL-4 required-stripped → `FRONTIER-UNEVALUABLE`; trap `seeded-only` isolates FORBIDDEN | REPRODUCED |
| 8 | PL-4 truncation 161 L: v10 PASS / r10 `UNREADABLE`+`FRONTIER-UNEVALUABLE` | REPRODUCED |
| 9 | PL-4 counters: 17 shared JSON keys, zero mismatches, 2 additive keys | REPRODUCED |
| 10 | PL-4 §6.1 one-line insertion caught | **CORRECTED** — reads PASS (fail-open) |
| 11 | PL-4 multi-class declared label | **CORRECTION (minor)** — either/or drops UNEVALUABLE |
| 12 | PL-2 prior design catches frozen seed / wall+cross | VERIFIED (on one-line forms); misses stripped anchors; VERDICT line changed |
| 13 | RV-3 design round-trip `8e420679…`, catches frozen seed + reflow + stripped | REPRODUCED; misses wall/cross literals |
| 14 | PL-1 merged build `7724adcc…` (PL-4+146 L) round-trip | REPRODUCED |
| 15 | PL-1 build full battery (clean PASS; 6 fault classes named) | REPRODUCED |
| 16 | EX-7 runtime/creation sizes+hashes, ABI/method-id identities | REPRODUCED |
| 17 | EX-7 probe 15/15, dispatch abi, decoded sha `2ec3f557…`, offsets | REPRODUCED |
| 18 | EX-7 raw-on-hex trap and creation parsed-and-empty + embedding at +43 | REPRODUCED |
| 19 | EX-7 fourth dispatcher class (stride 11, ascending, SUB leg at 194) | REPRODUCED |
| 20 | EX-7 control binary search (15 EQ, 3 GT pivots @19/30/137) | REPRODUCED |
| 21 | EX-7 Unknown provenance r3:33, r4:28 | VERIFIED |
| 22 | EX-7 landing projection 85/85 | REPRODUCED |
| 23 | EX-7 CBOR transcript `73 736f6c63` | **CORRECTED** — byte is `64 736f6c63` |
| 24 | SC-3 baseline 14/14 and draft identity 1,605 B / 23 L / `763c44b5…` | REPRODUCED |
| 25 | SC-3 landing 14→15, 15/15 resolve, depth 10.0 | REPRODUCED |
| 26 | SC-3 citation `r4:34` for the limitation quote | **CORRECTED** → `:29` |
| 27 | SC-3 `r1:24` byte-containment clause | **CORRECTED (precision)** → `:31`/reword |
| 28 | SC-3 core instance: CarrierV 1,637/1,562 B, +20, 55 trailing; probe 0 fns | REPRODUCED |
| 29 | RV-7 alternative draft 1,565 B / `ccbc5cdb…`, 15/15 | REPRODUCED |
| 30 | RV-7 F1: r3 erratum `:24` pointer dangling | VERIFIED |

## 6. Residuals and honest limits

1. **PL-4 is verified but not the best build.** Its two gaps are measured; the
   frozen falsifiable does not require them closed. If the parent lands PL-4
   unmodified, record the reflow fail-open and the two undeclared literals as
   named residuals (do not repeat §6.1's claim that all insertions are caught).
2. **PL-1's build is peer work.** I verified its identity, its delta round-trip,
   its clean PASS, its full fault battery, its JSON key identity and its VERDICT
   line, but it is not my artifact and I did not re-derive its build script line
   by line.
3. **C2 scope.** I re-ran one 6.4.0 probe (viair-opt200 hex), the two trap legs
   and the creation probe; I did not recompile the carriers (EX-9 did) nor re-run
   the 6.7.0 leg. The byte identities, the walk and the entry's internal
   consistency were checked first-hand. All 34 entry lines were not audited; the
   key result/observations were.
4. **C3 scope.** I verified the draft's bytes, its landing, every citation's
   bounds and content, the CarrierV census and one live probe. I did not re-run
   the r3/r4 non-creation legs or recompile Vyper; those citations are the r5
   audit's, and their line content was read.
5. **Live tree.** The wave directory was being written by other seats during this
   seat (PL-2 archived its prior attempt; many c1/c2/c3 verification artifacts
   landed after my first poll). Peer statuses above are point-in-time ~14:02
   local; the three delivered artifacts' files I used were stable throughout and
   their identities are recorded.

## 7. Landing summary for the parent

1. **C1:** land PL-1's merged build (PL-4 + 146-line delta, `7724adcc…`) — or
   PL-4's patch (`80027570…`) plus the two additive fixes. Exactly one c1 patch.
2. **C2:** copy `EX-7/entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md` to
   `corpus/knowledge/`, append the EVM map token (`corpus/README.md:38`), fix the
   CBOR transcript byte first (`73`→`64` at draft line 28), then command A must
   read `knowledge_files 85, mapped 85, missing [], dangling []`.
3. **C3:** append SC-3's §4 draft after SKILL.md:255 with `r4:34`→`r4:29` (and the
   `r1:24` clause re-pointed), or append RV-7's alternative; then command A must
   read `rule_blocks 15, citation_resolved_rules 15, depth_score 10.0`. Exactly
   one rule-15 draft.
