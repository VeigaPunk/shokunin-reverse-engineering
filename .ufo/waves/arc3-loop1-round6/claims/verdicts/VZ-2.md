# VZ-2 — arc3-loop1-round6 convergence verdict (c1/c2/c3 + peers)

Seat VZ-2, verdicts/convergence chain, wave arc3-loop1-round6, 2026-10-19.
Repo HEAD at every direct check: `c625d5de57e045188b5ce8cd450a57b349f90785`
(records; work `58c3db7`). Every number below is my own measurement this
session (lane rule #14); peer artifacts enter only as claims to be reproduced,
never as evidence. I wrote only `claims/verdicts/VZ-2.md` + `claims/verdicts/VZ-2/`;
the lane repo's git was read-only (the only commits are in a throwaway clone
under `/var/tmp`). Scratch: `/var/tmp/vz2-r6/` (never `/tmp`). The live gate was
never edited — `sha256sum .ufo/gates/c1-census-v10.py` =
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`, 610 lines,
before and after all runs.

Evidence pack (all first-hand): `VZ-2/matrix.tsv` (5 gates × 12 trees),
`VZ-2/patch-roundtrip.txt`, `VZ-2/json-integrity.txt`,
`VZ-2/commandA-baseline.txt`, `VZ-2/commandA-landing-commits.txt`,
`VZ-2/rule15-identities.txt`, `VZ-2/cbor-trailer.txt`,
`VZ-2/recheck-live-6.4.0.json`.

## Summary

| Claim | Ruling |
|---|---|
| C1 operability (census Frontier blind spot) | **REPRODUCED before-state; FOUR candidate patches round-trip byte-exact.** No single delivered design closes the whole fault set: PL-4 misses a +1-line reflow (CORRECTED), RV-3 misses a faithful cross-version restore (CORRECTED), PL-2 has no positive floor and misses stripped/rewritten bullets (CORRECTED). PL-1's merged build (`7724adcc…`, 748 lines) passes all eight of my fault classes — recommendation: land it (or PL-4 + its delta). |
| C2 coverage (viaIR Unknown) | **REPRODUCED end-to-end, not just projected**: EX-7's six byte identities, dispatch walk, four 15/15 probe legs and two traps all re-derived; a live 6.4.0 re-run returned 15/15 on the same decoded sha; landing in a scratch clone measured command A **85/85**. One CORRECTED transcription: CBOR `73`→`64` (EX-9's catch, confirmed first-hand). |
| C3 depth (rule #15) | **REPRODUCED**. SC-3's draft self-identity is exact (1,605 B, `763c44b5…`); its one mis-citation is confirmed (`:34`→`:29`), and the corrected draft lands `rule_blocks` 14→15 with 15/15 resolved. RV-7's competing draft also lands 15/15 and its r3-erratum finding F1 is confirmed. Four seats' corrected texts converge byte-identically (`6967b1e3…`). **Only one may land** — both would make 16 blocks. |

## C1 — operability: the Frontier blind spot and four r10 candidates

### Before-state — VERIFIED

- SCOPE declares PROVINCE.md only at `8-13, 15-26, 40-43, 44, 45-62, 64-71,
  119-131` (gate `:216-222`, read; programmatic load of `SCOPE`).
  `covering rows for (73,93) = []`, `for (133,162) = []`.
- `PROVINCE.md:73 ## Frontier`, `:95 ## Adjacent`, `:133 ### Round-4 frontier
  (post-unlock)`; `wc -l` → 162.
- v10 on eight seeded trees (frozen literal at `:91-93`, forbidden-only,
  EVM-required-stripped, RISC-V-required-stripped, trunc-161, reflow +1 before
  `:133`, reflow inside `:91-92`, silent `22/24`→`20/24` rewrite):
  **PASS exit 0 on all eight**, counters identical. The region is genuinely
  ungraded, not merely unreserved.
- Provenance (historical, not structural): `git show fbbbd45:PROVINCE.md`
  carries "real solc/vyper-compiled bytecode untested" at the EVM bullet;
  `git log -S 'real solc-0.8.37 carriers' -- PROVINCE.md` → `40de383` (r4 work)
  repaired it. The literal sat in the UNDECLARED region across rounds 1-3.
- Boundary (my own): an instrument-visible stale pin at `:88` → v10
  `FAIL undeclared=1`; the gap is specifically locus-free staleness.

### The candidates

| build | identity (my round-trip) | rows / mechanism | declared classes | G19 max-end |
|---|---|---|---|---|
| PL-4 | `80027570…`, 713 L | 14 rows, REQUIRED + FORBIDDEN, no anchors | FRONTIER-STALE / FRONTIER-UNEVALUABLE | 162 (register ends) |
| RV-3 | `8e420679…`, 712 L | 13 rows, anchor line + REQUIRED + FORBIDDEN + cite | FRONTIER-ANCHOR / FRONTIER-UNATTESTED / FRONTIER-STALE | unchanged (131) |
| PL-2 | `2d7ee95b…`, 705 L | 2 SCOPE rows class FRONTIER + a 3-literal register | FRONTIER-STALE | 162 (SCOPE row) |
| PL-1 | `7724adcc…`, 748 L | PL-4 + 146-line delta: 16 rows with anchors, collapsed whitespace, 3 measured-stale FORBIDDEN literals, claim-word REQUIRED, all classes reported | all three | 162 |

All four apply to a pristine `git show` copy with `patch -p0` and reproduce the
sha their seat claimed (`VZ-2/patch-roundtrip.txt`). Requirement (c), JSON
sense: every build leaves all **17 shared `--json` keys unchanged**; the only
additions are `frontier_rows`/`frontier_errors` (PL-4, RV-3, PL-1) or
`frontier_register`/`frontier_stale` (PL-2) (`VZ-2/json-integrity.txt`).

### My fault matrix (excerpt; full 60-cell table in `VZ-2/matrix.tsv`)

| tree | v10 | PL-4 | RV-3 | PL-2 | PL-1 |
|---|---|---|---|---|---|
| clean | PASS | PASS | PASS | PASS | PASS |
| frozen literal `:91-93` | PASS | FAIL STALE | FAIL STALE+UNATT | FAIL STALE | FAIL STALE+UNEVAL |
| forbidden-only (`untested` added, tokens kept) | PASS | FAIL STALE | FAIL STALE | **PASS** | FAIL STALE |
| EVM required stripped | PASS | FAIL UNEVAL | FAIL UNATT | **PASS** | FAIL UNEVAL |
| RISC-V required stripped | PASS | FAIL UNEVAL | FAIL UNATT | **PASS** | FAIL UNEVAL |
| trunc 161 | PASS | FAIL UNREADABLE+UNEVAL | FAIL UNATT | FAIL UNREADABLE | FAIL UNREADABLE+UNEVAL |
| reflow +1 before `:133` | PASS | **PASS** | FAIL ANCHOR | FAIL (scope-error) | FAIL ANCHOR |
| silent `22/24`→`20/24` | PASS | FAIL UNEVAL | FAIL UNATT | **PASS** | FAIL UNEVAL |
| faithful cross-version restore `:157-160` | PASS | FAIL UNEVAL | **PASS** | FAIL STALE | FAIL STALE+UNEVAL |
| append at 163 (locus-free) | PASS | PASS | PASS | PASS | PASS |
| stale pin `:88` | FAIL undecl 1 | FAIL undecl 1 | FAIL undecl 1 | FAIL ambiguous 1 | FAIL undecl 1 |

### Per-design verdicts

- **PL-4 — REPRODUCED with one CORRECTION.** Round-trip, clean PASS (scratch and
  repo root), frozen-literal catch, required-strip catch, truncation catch, and
  per-key JSON identity all reproduce. **CORRECTED: §6 residual 1 claims
  insertions inside `:132-162` fail via REQUIRED-absent; a +1-line insertion
  before `:133` reads PASS exit 0** (`VZ-2/matrix.tsv`). Every register span has
  one line of slack, so the shift is absorbed. (Minor, also measured: when a
  FORBIDDEN and a REQUIRED fault co-occur, the either/or class logic reports
  only `FRONTIER-STALE` and drops `FRONTIER-UNEVALUABLE`.) An insertion inside
  the EVM bullet fails only through the pre-existing `:119` DATED marker, not
  through the register.
- **RV-3 — REPRODUCED with one CORRECTION.** Identity, clean PASS, EVM literal
  catch, anchor-on-reflow catch (8 `FRONTIER-ANCHOR` errors) all reproduce.
  **CORRECTED: a faithful restore of the measured-stale cross-version bullet
  (`compare-application-versions` still probe-refused since r2 …) reads PASS** —
  its REQUIRED token `compare-application-versions` occurs in the stale text
  too, and it declares no FORBIDDEN literal for that bullet. Truncation is
  caught here by the dropped `HOPPER_LAUNCHER_PATH`, not by a line-count guard
  (no `max_end` change), and `frontier_audit()` silently `continue`s if the
  file is absent from `filelines`.
- **PL-2 — identity REPRODUCED, design CORRECTED (not recommended).** Its
  literal register knows only three exact strings; with the tokens preserved
  and `untested` appended it reads PASS, and stripped or silently rewritten
  bullets read PASS. Its SCOPE rows change the frontier's locus disposition
  (`:88` pin: v10 `undeclared=1` → PL-2 `ambiguous=1`) and its VERDICT line
  gains `frontier=0`, so "every current counter intact" holds only in the
  structural sense. It is the only design that grades a *locus-bearing*
  frontier drift as STALE/AMBIGUOUS rather than UNDECLARED — a real but
  different capability.
- **PL-1 — REPRODUCED on every arm.** Applied `patch-pl4-to-pl1.diff` to the
  PL-4 build → sha `7724adcc…`, 748 lines, matching PL-1's claim. Clean PASS;
  all eight fault classes caught; shared JSON keys unchanged; the three
  FORBIDDEN literals are grounded in the pre-repair tree (I re-read
  `40de383~1:PROVINCE.md`: `:139` "hits REA's ~900s internal", `:158`
  "probe-refused since r2", and `fbbbd45:PROVINCE.md:92` "untested").

### Recommended landing for C1

Land PL-1's merged build (`claims/c1/PL-1/pl1-r10.py`, sha `7724adcc…`) — it is
the only candidate that passes all eight of my fault classes, and its delta is
a reviewable 67+/32− on top of PL-4. If the lane prefers a delivered-as-briefed
artifact, land PL-4 and apply PL-1's delta in the same commit (the coupled-
landing discipline the wave itself is codifying). Do **not** land RV-3 alone
(cross-version fail-open) and do not land PL-2 (no positive floor).

Residual shared by every build (measured, incl. PL-1): a **new locus-free
bullet appended past `:162` reads PASS** (`append-163` tree). This is inherent
to a line-keyed register and is named by PL-4/PL-1; only a locus-bearing append
fails (via UNDECLARED). Record it in the landing receipt.

## C2 — coverage: the `viaIR` dispatcher entry

### Before-state — REPRODUCED

Command A (SCORECARD.md:88-124, run verbatim against immutable Git objects) at
both source commits → `{"knowledge_files": 84, "mapped": 84, "missing": [],
"dangling": [], "rule_blocks": 14, "citation_resolved_rules": 14,
"coverage_score": 10.0, "depth_score": 10.0}` (`VZ-2/commandA-baseline.txt`).
The Unknown is open at `2026-10-19-arc3-r3-evm-optimizer-shapes.md:33` and
`2026-10-19-arc3-r4-evm-vyper-leg.md:28` (read at those lines).

### EX-7's entry — bytes REPRODUCED

| leg | runtime | sha | creation | sha | embed |
|---|---|---|---|---|---|
| viair-opt200 | 1,517 B | `2ec3f557` | 1,560 B | `d85fdde9` | +43, 0 trailing |
| viair-noopt | 4,144 B | `0cc6938c` | 4,318 B | `f1125049` | — |
| std-opt200 | 1,921 B | `c2ceabb1` | 1,966 B | `4541fd49` | — |

Every `.hex` decodes byte-identically to its `.bin`; `methodIdentifiers` holds
15 keys; `planted-K.json` records K=15 pre-compile. The walk JSONs give, for
viair-opt200: 14 EQ, 0 GT, `eq_sorted_ascending=true`, `all_dst_jumpdests=true`,
`eq_pc_gaps=[11]×13`, EQ dsts 253–982 and the 15th selector `ee02438e` at
reported offset 204 (= push4 pc 194 + 10), byte `0x34`, not a JUMPDEST. The
std control gives 15 EQ + 3 GT at pcs 19/30/137 with pivots
`6e69f38c`/`90ab171e`/`3f4ba83a` — the r3 binary-search class. viair-noopt
EQ dsts step 208→273 by 5. The `PUSH4 ee02438e SUB PUSH2 0x000e JUMPI` pattern
is at pc 194 in both viaIR legs. Selector sets union to the 15 MI selectors
(the SUB leg carries the 15th). **The fourth-dispatcher-class claim
REPRODUCES at byte level.**

Probe envelopes (static re-read): 15/15, `dispatch:"abi"` on viair-opt200 hex
6.4.0 (`ev_409e0442…`), raw (`ev_c55a152c…`), hex 6.7.0 (`ev_285d13d0…`),
viair-noopt (`ev_8ddef761…`), std control (`ev_3b390132…`); traps 0 functions
with decoded sha equal to the hex text's own sha (`19838d66…`) and to the
creation bin's sha (`d85fdde9…`).

Live re-run (my own, `TMPDIR=/var/tmp/vz2-r6/tmp`,
`npx -y rea-agents@6.4.0 inspect-evm-interface …runtime.hex hex`): exit 0,
**15 functions, all `dispatch:"abi"`, decoded sha `2ec3f557…`, 1,517 B**,
evidence id `ev_71da9d37…` (a new path-minted id — path sensitivity, as the
entry states; compare by decoded sha per QUALITY row 15).

### Landing — MEASURED, not projected

In a `git clone` of the lane (scratch), I copied the entry draft to
`corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md`, applied EX-7's
exact EVM-row token patch to `corpus/README.md`, committed, and ran command A:
`{"knowledge_files": 85, "mapped": 85, "missing": [], "dangling": [],
"coverage_score": 10.0, "rule_blocks": 14}`. The frozen falsifiable is met.

### CORRECTED items on the entry (both non-blocking, fix before landing)

1. **CBOR trailer transcript** (draft line 28): the draft prints
   `73 736f6c63`; the measured tail is
   `a2 64 69706673 58 22 <34> 64 736f6c63 43 000825 00 33` — the `solc` key
   marker is `64`, not `73` (`VZ-2/cbor-trailer.txt`; EX-9 found this
   independently). Everything else in that sentence (ipfs, 0x000825, cbor
   length 51) reproduces.
2. **Draft header**: the file opens with a six-line HTML "LAND-MOVE" comment
   addressed to the parent. Copied verbatim it lands as part of the corpus
   entry. Strip lines 1-6 (or leave deliberately) at landing time.

Scope note: the entry's own Unknowns list (other solc versions under viaIR,
Vyper IR, runs ≠ 200, fallback-bearing carriers, 6.7.0 raw) is honest; my
checks cover the pinned bytes and the 6.4.0/6.7.0 hex legs only.

## C3 — depth: rule #15

### Baseline — REPRODUCED

`rule_blocks=14`, `citation_resolved_rules=14` at `c625d5d` and `58c3db7`
(same run as C2). Craft section starts `SKILL.md:81`, rule 14 ends at `:255`
("never a carried-over number.").

### SC-3's draft — identity REPRODUCED exactly

Extracted the fenced block: **1,605 B, 23 lines, sha256 `763c44b5…`** — matches
SC-3's self-identity. It parses as exactly one `^- \*\*` block.

### The one CORRECTION (VZ-4's, confirmed first-hand)

SC-3 cites `2026-10-19-arc3-r4-evm-vyper-leg.md:34` for "empty results do not
prove absence of dispatch". Read at the file: **:29** is the Limitations bullet
carrying that phrase; **:34** is the `## Erratum (arc3-loop1-round5 …)` header.
The citation resolves in-bounds either way (34 ≤ 63), so command A cannot see
the error — but a landed rule would mispoint readers. Fix `:34` → `:29`.

### Landing mechanics — MEASURED at both ends

With the draft appended after `:255` in a scratch clone commit:
`rule_blocks=15, citation_resolved_rules=15, depth_score=10.0` (SC-3 as-is,
SC-3 with the `:29` fix, and RV-7's competing draft all measure the same;
`VZ-2/commandA-baseline.txt`). All 8 SC-3 citations and all 6 RV-7 citations
resolve in-bounds.

### RV-7 as a competing draft — VERIFIED, and its F1 is real

RV-7's bullet (1,565 B, 23 lines, sha `ccbc5cdb…`) lands the same 15/15 without
a mis-citation, and carries the VaultB numbers. I re-derived them from the
retained r3 artifacts: **VaultB opt200 runtime 1,621 B at +34 in a 1,655 B
creation; nopt 3,163 B at +80 in 3,243 B**. RV-7's finding **F1 is confirmed**:
the r3 erratum at `:41` attributes to "`:24`" the sentence "Creation blobs
carry no runtime dispatch table", but `r3:24` is the `Rv2TokenOpt @EX-07`
RESULT row; the quoted sentence is `r1:24`. A later append-only pass should
re-point or drop that pointer.

### Convergence and landing choice

Four independent corrected drafts are byte-identical to my own `:34`→`:29` fix:
`EX-14/rule15-corrected.md`, `EX-16/rule15-SC3-corrected.md`,
`RV-5/rule15-corrected.md`, and my `rule-sc3-fixed.md` — all sha
**`6967b1e3…`**, 1,605 B (`VZ-2/rule15-identities.txt`). SC-1's variant
(`a8aef40e…`) differs only in where the `r1:24` citation sits in the sentence.

**Land exactly one rule.** SC-3-corrected (converged text) and RV-7 (shorter,
no correction debt, richer provenance) are both valid; landing both would read
`rule_blocks=16`, not the claimed 15. Recommendation: land the converged
SC-3-corrected text (`6967b1e3…`); it is the artifact every c3 verifier
reproduced, and the fix is a one-token edit.

## Peer reconciliation

| peer | what it claimed | my ruling |
|---|---|---|
| VZ-4 | C1 REPRODUCED on RV-3; C2 PENDING; C3 with `:34`→`:29` correction | The RV-3 audit and the C3 correction both reproduce. Its C1 ruling is incomplete: it polled before PL-4/PL-2 landed, so it never compared designs, and it did not test a faithful cross-version restore (RV-3's fail-open). Its C2 PENDING is superseded by EX-7 + my 85/85 measurement. |
| PL-1 | PL-4 verified; +1 reflow fail-open; merged build | My independent matrix reproduces the reflow finding and the merged build's sha/behavior exactly. |
| EX-3, RV-1 | PL-4 verified; reflow corrected | Converge with my measurements (same hole, same 6/6 style counterexamples). |
| EX-9 | EX-7 verified; CBOR `73`→`64` | Confirmed first-hand from the runtime bytes; its compile-derived shas match mine. |
| EX-13/14/15/16, RV-5/6/7/8, SC-1/2/4 | rule #15; citation corrections; corrected drafts | Converge: the corrected text is byte-identical across EX-14/EX-16/RV-5 (and mine); RV-7's F1 confirmed. |
| PL-2 | its own r10 variant | Identity reproduced; behavior materially weaker on stripped/rewritten bullets (see matrix). |
| EX-6 | viaIR raw evidence only (no artifact) | Superseded by EX-7; its retained bytes are consistent with EX-7's legs. |
| EX-7 | viaIR entry draft | VERIFIED (one transcription correction). |

## Per-item verdict table

| # | Item | Verdict |
|---|---|---|
| 1 | HEAD `c625d5d` / work `58c3db7`; gate sha `d0772ce8…`, 610 L | REPRODUCED |
| 2 | PROVINCE 162 / SKILL 390 / SCORECARD 1696; Frontier at `:73`,`:133` | VERIFIED |
| 3 | SCOPE PROVINCE rows 8-13/15-26/40-43/44/45-62/64-71/119-131; covering rows for 73-93 and 133-162 = [] | VERIFIED |
| 4 | v10 blind on eight seeded Frontier faults (incl. truncation and reflow) | REPRODUCED |
| 5 | Historical stale literal at `fbbbd45:PROVINCE.md:92`, repaired at `40de383` | VERIFIED |
| 6 | Instrument-visible pin at `:88` → v10 `undeclared=1` | REPRODUCED |
| 7 | PL-4 identity `80027570…`/713, clean PASS, (a)/(b)/(c) | REPRODUCED |
| 8 | PL-4 §6.1 "+1 insertion inside 132-162 caught" | CORRECTED — reads PASS |
| 9 | PL-4 multi-class fault drops FRONTIER-UNEVALUABLE when STALE present | CORRECTED (minor) |
| 10 | RV-3 identity `8e420679…`/712, clean PASS, EVM literal, reflow anchor | REPRODUCED |
| 11 | RV-3 faithful cross-version restore | CORRECTED — reads PASS |
| 12 | PL-2 identity `2d7ee95b…`/705; frozen literal catch | REPRODUCED |
| 13 | PL-2 stripped/rewritten bullets, token-only EVM fault | CORRECTED — no positive floor, reads PASS |
| 14 | PL-1 merged identity `7724adcc…`/748; all eight fault classes | REPRODUCED |
| 15 | Shared JSON keys unchanged (17/17) for all four builds | REPRODUCED |
| 16 | Locus-free append past `:162` | PASS in all five gates (shared residual, measured) |
| 17 | Command A before 84/84/rule_blocks 14 at both revs | REPRODUCED |
| 18 | EX-7 six runtime/creation sizes+shas; hex≡bin; embed +43 | REPRODUCED |
| 19 | EX-7 viaIR walk (14 EQ, stride 11, ascending, SUB leg pc 194 / offset 204) | REPRODUCED |
| 20 | EX-7 std control (15 EQ + 3 GT, pivots 19/30/137); noopt chain 208–273 | REPRODUCED |
| 21 | EX-7 probe legs 15/15 ×5, traps 0 fns with decoded-sha identity | REPRODUCED (static) |
| 22 | EX-7 live recheck 6.4.0 | REPRODUCED — 15/15, `2ec3f557…` |
| 23 | EX-7 landing → command A 85/85, missing/dangling [] | REPRODUCED (scratch clone commit) |
| 24 | EX-7 CBOR transcript `73 736f6c63` | CORRECTED — byte is `64` |
| 25 | SC-3 draft identity 1,605 B / `763c44b5…` / 23 L | REPRODUCED |
| 26 | SC-3 `:34` for the tool-limitation quote | CORRECTED — quote is at `:29` |
| 27 | SC-3 scratch 14→15, 15/15 resolved (as-is and fixed) | REPRODUCED |
| 28 | RV-7 draft identity 1,565 B / `ccbc5cdb…`; 15/15 landing | REPRODUCED |
| 29 | RV-7 VaultB embeddings 1,621@+34/1,655; 3,163@+80/3,243 | REPRODUCED |
| 30 | RV-7 F1: r3 erratum's `:24` pointer is to r1's sentence | VERIFIED |
| 31 | Corrected rule-15 text convergence (4 files, `6967b1e3…`) | VERIFIED |

## Landing recipes (for the integrator; nothing below was executed on the lane repo)

C1 (recommended build):

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
cp .ufo/waves/arc3-loop1-round6/claims/c1/PL-1/pl1-r10.py .ufo/gates/c1-census-v10.py
sha256sum .ufo/gates/c1-census-v10.py   # expect 7724adcc…, 748 lines
python3 .ufo/gates/c1-census-v10.py --quiet   # expect PASS, "16 rows asserted, errors: []"
```

(Alternative: `patch .ufo/gates/c1-census-v10.py < …/c1/PL-4/patch-v10-to-r10.diff`
then `patch .ufo/gates/c1-census-v10.py < …/c1/PL-1/patch-pl4-to-pl1.diff`.)
Record the post-edit sha in the landing receipt, not inline.

C2:

1. Copy `claims/c2/EX-7/entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md`
   to `corpus/knowledge/` (strip the LAND-MOVE comment; fix the `73`→`64` byte
   in the trailer sentence).
2. Apply EX-7's EVM-row token patch to `corpus/README.md:38`.
3. `python3` command A → expect `knowledge_files 85, mapped 85, missing [],
   dangling []`.

C3:

1. Append `claims/c3/EX-14/rule15-corrected.md` (= `EX-16/`, `RV-5/`, my
   `rule-sc3-fixed.md`, sha `6967b1e3…`) after `SKILL.md:255`.
2. Command A → `rule_blocks 15, citation_resolved_rules 15, depth_score 10.0`,
   `knowledge_files` unchanged (84 until C2 lands; if C2 lands first, 85).
3. Land exactly one rule, not both SC-3 and RV-7.

## What I did not do

- Did not apply any patch to the lane repo, PROVINCE.md, SKILL.md, SCORECARD.md,
  corpus, or the gate; all "after" measurements come from scratch copies or a
  throwaway clone under `/var/tmp/vz2-r6/clone`. `git status` at the end shows
  only the pre-existing `arc2-loop1-round10/C3.md` modification and the
  untracked wave tree.
- Did not re-run the 6.7.0 live probe (static envelope check only) or compile
  from source for C2 (EX-7's and EX-9's compile receipts already agree with my
  byte reads; I re-derived the bytes, not the compile).
- Did not test the Vyper `-O codesize`/`--no-optimize` alternative Unknown
  (candidate (b)); the viaIR candidate is now closed, so the alternative stays
  queued.
- Did not test `+2`/`+3` reflows on my own trees (PL-1 reports them caught by
  PL-4); my single measured counterexample is the +1 case.
