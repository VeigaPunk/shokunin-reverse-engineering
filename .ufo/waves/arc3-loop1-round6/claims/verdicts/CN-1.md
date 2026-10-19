# CN-1 — verdicts/convergence: the three delivered artifacts + peers, reconciled

Seat CN-1, verdicts/convergence chain, wave arc3-loop1-round6, 2026-10-19.
Repo HEAD re-derived first-hand: `c625d5de57e045188b5ce8cd450a57b349f90785`
(`c625d5d` records; work `58c3db7`). Scratch: `/dev/shm/cn1/` and
`/var/tmp/cn1-recheck/` (never `/tmp`). Write scope honored: only
`.ufo/waves/arc3-loop1-round6/claims/verdicts/CN-1` (`CN-1.md` + `CN-1/`);
git read-only; no gate, corpus, PROVINCE.md, SKILL.md, SCORECARD.md or other
tracked file modified. Every number below is my own measurement this session
(rule #14); peer artifacts are cited only as the objects being audited.
Where late peers landed after my first draft, §0.1 records what changed and
§1.4/§3 re-derive the new claims rather than adopting them on report.

## 0. Ruling in one table

| Claim | Delivered | Other peer(s) in the tree | My ruling | What lands |
|---|---|---|---|---|
| C1 operability | PL-4 patch (`80027570…`) | PL-1 merged build (`7724adcc…`); revised PL-2 and RV-3 (both now verify PL-4; prior designs archived) | **PL-4 VERIFIED, with three measured CORRECTIONS** to its residual prose; **PL-1's merged build VERIFIED and strictly closes those holes**; prior PL-2 design **CORRECTED**, prior RV-3 design **VERIFIED alternative** | **PL-1's merged build** (PL-4 as the minimal frozen-deliverable fallback) |
| C2 coverage | EX-7 viaIR entry | EX-6 (evidence only, no artifact) | **VERIFIED end-to-end**, including live 15/15 K/K re-runs and command A **85/85** on a scratch landing repo; one cosmetic byte-label typo in the draft's CBOR listing | **EX-7 entry + README token** |
| C3 depth | SC-3 rule-15 (`763c44b5…`) | SC-4 corrected text (`a1bceb40…`), RV-7 (`ccbc5cdb…`) | SC-3 **REPRODUCED, two CORRECTIONS**; SC-4's text fixes both and is content-clean (**15/15**); RV-7's text is content-clean and zero-edit | **SC-4's corrected text**; RV-7 as the zero-edit alternative; never both |

The convergence fact that matters: the wave carries **three different r10 gate
patches** and **three rule-15 texts**. All gate patches apply cleanly and
reproduce their own claimed sha256, so "it applies" does not choose between
them; the fault arms and the claim's constraints do. By the end of the wave
the two competing c1 seats had revised their artifacts to verify PL-4, and
PL-1 had built a measured superset.

## 0.1 Late-peer addendum (what changed after my first draft)

1. **PL-1's merged build** (`claims/c1/PL-1.md`, `PL-1/patch-pl4-to-pl1.diff`):
   PL-4 + a 146-line delta → **748 lines, sha
   `7724adccdf6391cffc622b8fa3144ede421eb24aedc1431893c2482f892c12a1`**. I
   applied it to my PL-4 copy and reproduced the sha exactly. It adds per-row
   anchor lines (a reflow fails `FRONTIER-ANCHOR`), section-header rows, and
   FORBIDDEN patterns for the two other measured pre-`40de383` stale clauses
   (the `~900s` wall form and `probe-refused since r2`). Its discriminator arms
   are measured in §1.3.
2. **PL-2 and RV-3 revised their artifacts.** Their current headers verify
   PL-4 and preserve their earlier competing designs verbatim under
   `claims/c1/PL-2/prior-attempt/` and `claims/c1/RV-3/prior-attempt.md`
   (read this session). My §1.4 numbers for those designs apply to the archived
   bytes, not to the current files; the current artifacts endorse PL-4.
3. **SC-4's corrected rule-15 text** (`claims/c3/SC-4.md`): 1,605 B, 23 lines,
   sha `a1bceb4074328d9d60d14ddf0789b9bcd18ca38936c217d78fc37b1091ec1789`.
   It differs from SC-3's draft by exactly the two citation fixes below
   (`diff` in `CN-1/late-peer-addendum.txt`), and lands 15/15 (85/85 with the
   c2 entry overlaid).
4. Late convergence seats (CN-2, CN-4, CR-5..8, VZ-2) reach the same landing
   triad (PL-4/PL-1, EX-7, SC-3-lineage rule). Their agreement is
   reconciliation, not evidence; the numbers here are mine.

## 1. C1 — census Frontier blind spot

### 1.1 Baseline, re-derived (the frozen "before")

- Instrument: `.ufo/gates/c1-census-v10.py`, 610 lines, sha256
  `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`
  (the same bytes as `git show c625d5d:.ufo/gates/c1-census-v10.py`).
- SCOPE at gate `:215-236`: PROVINCE.md rows exactly `8-13`, `15-26`,
  `40-43`, `44`, `45-62`, `64-71`, `119-131` (gate `:216-222`). Programmatic
  coverage check: **no row covers 73-93 or 133-162**.
- PROVINCE.md: 162 lines; `:73 ## Frontier`, `:133 ### Round-4 frontier
  (post-unlock)`, EOF `:162`. SKILL.md 390, SCORECARD.md 1696.
- Clean run at the repo root: `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0
  unresolved=0)` exit 0, counters `PROVINCE 6 / SCORECARD 9 / SKILL 2`,
  G2 per-file `17/14/3`.
- Blindness re-measured on my own seeded trees (`CN-1/runs/`): the r9 gate
  reads **PASS exit 0** on (i) the frozen retracted literal reinserted at
  `:91-93`, (ii) the same with earning tokens kept but "untested" added,
  (iii) earning tokens stripped, (iv) a 161-line truncation, (v) a one-line
  reflow before `:133`, (vi) a token-retained wall literal, and (vii) a
  token-retained cross-version literal; only an instrument-visible stale pin
  fails (`undeclared=1`). This independently reproduces the frozen before-state
  and VZ-4's boundary result.

### 1.2 The patches — identities

Applied with `patch` onto byte-copies of the pristine gate (PL-1 applied on
top of the PL-4 result); no gate file in the repo was touched
(`CN-1/c1-patch-identities.txt`, `CN-1/late-peer-addendum.txt`):

| Artifact | Patch | Applied sha256 | Claimed | Lines |
|---|---|---|---|---|
| PL-4 | `claims/c1/PL-4/patch-v10-to-r10.diff` | `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca` | same | 713 |
| PL-1 | `claims/c1/PL-1/patch-pl4-to-pl1.diff` (on PL-4) | `7724adccdf6391cffc622b8fa3144ede421eb24aedc1431893c2482f892c12a1` | same | 748 |
| PL-2 prior | `claims/c1/PL-2/prior-attempt/` patch | `2d7ee95ba2743bde0b658c91d867a46e04e3e9e14de41d2cb60f2ff46238ce7b` | same | 705 |
| RV-3 prior | diff in `claims/c1/RV-3/prior-attempt.md` §4 | `8e4206796fec2e16fb6f2c1959f33b63bbcb9643471d42472ac6bc2cba195ebf` | same | 712 |

PL-4 and PL-1 preserve, on the clean tree, **all 17 shared `--json` keys** with
zero value drift; PL-4 adds `frontier_rows`/`frontier_errors`, PL-1 the same
shape with 16 rows. Counts stay `PROVINCE.md:17, SCORECARD.md:14, SKILL.md:3`.
The prior PL-2 and RV-3 designs also preserve the 17 shared keys on the clean
tree. So requirement (c)'s clean-tree half is satisfied by all four
(`CN-1/json.*.json`).

### 1.3 Fault-arm matrix (my seeds, not the peers' transcripts)

Full transcript tables: `CN-1/gate-arms-matrix.txt` and
`CN-1/late-peer-addendum.txt`; raw runs in `CN-1/runs/`.

| tree (my seed) | r9 | PL-4 | PL-1 | PL-2 prior | RV-3 prior |
|---|---|---|---|---|---|
| clean | PASS | PASS, 14 rows, 0 err | PASS, 16 rows, 0 err | PASS, 3 entries | PASS, 13 rows, 0 err |
| frozen literal at `:91-93` | **PASS** | **FAIL** `FRONTIER-STALE` | **FAIL** `FRONTIER-STALE`+`UNEVALUABLE` | **FAIL** `FRONTIER-STALE` | **FAIL** `STALE`+`UNATTESTED` |
| tokens kept + "untested" | PASS | FAIL `FRONTIER-STALE` | FAIL `FRONTIER-STALE` | **PASS** | FAIL `FRONTIER-STALE` |
| earning tokens stripped | PASS | FAIL `FRONTIER-UNEVALUABLE` | FAIL `FRONTIER-UNEVALUABLE` | **PASS** | FAIL `FRONTIER-UNATTESTED` |
| trunc 161 / 160 lines | PASS | FAIL `UNREADABLE` | FAIL `UNREADABLE` | FAIL (161) `UNREADABLE` | FAIL (161) `UNATTESTED` |
| stale pin `:88`, no client token | FAIL `undeclared=1` | FAIL `undeclared=1` | FAIL `undeclared=1` | FAIL **`ambiguous=1`** | FAIL `undeclared=1` |
| stale pin `:88` (`kimi`) | FAIL `undeclared=1` | FAIL `undeclared=1` | FAIL `undeclared=1` | FAIL **`stale=1`** | FAIL `undeclared=1` |
| **reflow: blank line before `:133`** | PASS | **PASS (fail-open)** | **FAIL `FRONTIER-ANCHOR`** | FAIL (scope marker) | FAIL `FRONTIER-ANCHOR` |
| **wall literal, tokens retained** (`hits REA's ~900s internal…`) | PASS | **PASS (fail-open)** | **FAIL `FRONTIER-STALE`** | PASS | PASS |
| **cross literal, tokens retained** (`probe-refused since r2`) | PASS | **PASS (fail-open)** | **FAIL `FRONTIER-STALE`** | FAIL `FRONTIER-STALE` | PASS |

### 1.4 Per-artifact verdicts

**PL-4 — VERIFIED, with three CORRECTIONS to its residual prose.** Requirement
(a): clean PASS on the real repo root and on a scratch copy
(`CN-1/pl4-repo-root.txt`, exit 0, 14 rows, errors []). Requirement (b): the
frozen literal fails exit 1 with named class `FRONTIER-STALE`; the stripped
claims arm fails `FRONTIER-UNEVALUABLE`; the 161/160-line truncations are
declared `UNREADABLE` because `max_end` now includes `FRONTIER` rows.
Requirement (c): JSON 17/17 shared keys equal; text output adds exactly one
line, the `VERDICT` line is byte-identical.
Measured corrections: (1) a one-line insertion before `:133` reads **PASS**
(span absorption), contradicting PL-4 §6.1's "insertions inside `:132-162` are
caught"; (2) a *token-retained* wall literal (`hits REA's ~900s internal
session deadline`) reads **PASS**; (3) a token-retained cross-version literal
(`probe-refused since r2`) reads **PASS** — PL-4's FORBIDDEN list carries only
`untested`. These are coverage residuals, correctly bounded by PL-4 §6.3's
"earned, not exhaustive", but its §6.1 insertion sentence is measurably false
for the reflow arm. Cosmetic: `%r` renders regexes with doubled backslashes.

**PL-1 — VERIFIED and recommended.** The merged build applies on PL-4 to
`7724adcc…` (748 lines). It keeps every PL-4 arm (clean PASS; seed, stripped,
trunc, pin all unchanged) and closes the three measured holes: reflow →
`FRONTIER-ANCHOR`; wall literal → `FRONTIER-STALE`; cross literal →
`FRONTIER-STALE`. It also reports both `STALE` and `UNEVALUABLE` on the
multi-class seed, which PL-4's either/or drops. No regression measured. One
residual of the same class as every literal register: the wall FORBIDDEN
pattern is the exact phrase `hits REA's ~900s internal session deadline`; my
paraphrase "hit REA's" passes. That is the honest limit of a text register.

**Prior PL-2 design — CORRECTED** (archived under `PL-2/prior-attempt/`; the
seat's current artifact verifies PL-4). It catches the frozen literal and its
clean-tree JSON is invariant, but: (1) with earning citations stripped it reads
**PASS exit 0** (no positive floor — the claim's first sentence asks that
Frontier staleness become *gradable*); (2) its two SCOPE rows change an
unattributable Frontier pin from `undeclared=1` to `ambiguous=1`, a
counter-class change; (3) its `VERDICT` line gains `frontier=0`. It does catch
the token-retained cross literal, which PL-4 misses.

**Prior RV-3 design — VERIFIED (alternative)** (archived at
`RV-3/prior-attempt.md`; the seat's current artifact verifies PL-4). Same
(a)/(b)/(c) results; per-row anchors catch the reflow; per-error classes are
finer. Residual: no explicit max-end guard (my 161-line truncation was caught
only because it removed `HOPPER_LAUNCHER_PATH`), and no FORBIDDEN for the wall
or cross clauses.

### 1.5 Convergence ruling for C1

**Land PL-1's merged build** (`7724adcc…`, 748 lines): it is PL-4 plus a
measured delta, satisfies the frozen (a)/(b)/(c) identically, and strictly
closes the three fail-open arms PL-4 leaves. If the integrator will land only
the frozen delivered artifact, **PL-4 (`80027570…`, 713 lines) is the minimum
compliant fallback** — but record the three corrections as named residuals.
Do not land the prior PL-2 or RV-3 designs; their seats have already withdrawn
them in favor of PL-4. Never land two gate revisions in one commit.

Landing recipe (post-edit identity in the receipt, not inline — the gate's own
rule-#14 discipline):

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
patch .ufo/gates/c1-census-v10.py < \
  .ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff
patch .ufo/gates/c1-census-v10.py < \
  .ufo/waves/arc3-loop1-round6/claims/c1/PL-1/patch-pl4-to-pl1.diff
sha256sum .ufo/gates/c1-census-v10.py   # expect 7724adcc…, 748 lines
python3 .ufo/gates/c1-census-v10.py --quiet   # exit 0, PASS, 16 rows, []
# then re-run the seeded arm on a scratch copy: expect FAIL FRONTIER-STALE
# and the reflow arm: expect FAIL FRONTIER-ANCHOR
```

## 2. C2 — the viaIR corpus Unknown

### 2.1 Baseline and entry

Command A at `c625d5d` (SCORECARD.md:88-124 recipe): `knowledge_files 84,
mapped 84, missing [], dangling [], citation_resolved_rules 14, rule_blocks
14, coverage 10.0, depth 10.0` — before-state REPRODUCED. The Unknown is named
at `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:33` and
`2026-10-19-arc3-r4-evm-vyper-leg.md:28` — both verified present.

Entry draft: `claims/c2/EX-7/entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md`
(34 lines). Every number I could re-derive agrees:

| Claim in entry | My measurement | Verdict |
|---|---|---|
| viair-opt200 runtime 1,517 B `2ec3f557…` | 1,517 B sha `2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a` | VERIFIED |
| viair-noopt 4,144 B `0cc6938c…` | 4,144 B sha `0cc6938cd768199159cbed74a7e9f5bd4273c583afbf6babca643b0ffdbd29b4` | VERIFIED |
| std-opt200 1,921 B `c2ceabb1…` | 1,921 B sha `c2ceabb163ad9c1e6d88244c29c5187602eaf4c810029d0018e76eb9643f7e27` | VERIFIED |
| creation shas `d85fdde9`/`f1125049`/`4541fd49`, ABI `63fcf52f`, method ids `c32e2ef2` | all six re-hashed equal | VERIFIED |
| guard `36 10 15 61<0022> 57`, `5f3560e01c` at 35 | exact bytes at 7 and 35 of the opt200 runtime | VERIFIED |
| 14 EQ legs, 11-byte stride, ascending, dsts 253–982 all JUMPDESTs | 14 legs, gaps `{11}`, ascending, 253–982, all JUMPDEST | VERIFIED |
| 15th leg `PUSH4 ee02438e SUB PUSH2 0x000e JUMPI` at 194 | exact, dst 14 is a JUMPDEST; falls into `mark` handler | VERIFIED |
| offsets: 14/15 = EQ dst, 15th = 204 (`0x34`, not JUMPDEST) | probe offsets `[204,253,272,311,340,374,425,485,572,631,694,723,771,935,982]`; mismatch only `ee02438e`→204; byte 204 = `0x34` | VERIFIED |
| 19 boundary PUSH4 sites = 15 selectors + `4e487b71`×2, `0c2eae8d`, `3c3332b9` | 19 sites; 15 selectors; constants exactly those four | VERIFIED |
| mutability 14/15, `scale` pure→view | 14/15; only `scale` ABI `pure` vs inferred `view` | VERIFIED |
| creation embeds runtime at +43 of 1,560 B | `creation[43:43+1517] == runtime`, 0 trailing | VERIFIED |
| std control = GT/EQ binary search, pivots pcs 19/30/137 | GT legs at pc 19 `6e69f38c`→135, pc 30 `90ab171e`→87, pc 137 `3f4ba83a`→194; 15 EQ legs, 15 distinct selectors | VERIFIED |
| CBOR tail `ipfs` + `solc 0x000825` | tail contains `64 69706673 58 22 … 64 736f6c63 43 000825 00 33`; the draft prints the solc length byte as `73`, actual `64` | VERIFIED; **one cosmetic byte-label correction** |

**Live K/K re-run (my own, not a re-read of EX-7's envelopes).**
`TMPDIR=/var/tmp/cn1-recheck npx -y rea-agents@6.4.0 inspect-evm-interface
…/viair-opt200/runtime.hex hex --format json` → exit 0, **15 functions, all
`dispatch:"abi"`, decoded sha `2ec3f557…`**, new evidence id `ev_71da9d37…`.
Same result at 6.7.0 (`ev_db5f8470…`), for viair-noopt at 6.4.0
(`ev_0dbb0e7f…`) and for the std control (`ev_7e7e340c…`). The creation probe
returns **0 functions, decoded sha `d85fdde9…`** (`ev_5b422197…`) on the blob
that byte-embeds the runtime at +43 — the parsed-and-empty distinction,
re-measured live. My ids differ from EX-7's because the path differs; the
decoded sha and function payload agree, which is the lane's comparison rule.

### 2.2 Command A with the entry landed — 85/85

Built a scratch git repo from `git archive c625d5d`, copied the entry to
`corpus/knowledge/`, applied EX-7's README token patch, committed, and ran the
SCORECARD recipe at that repo's `HEAD`. Output
(`CN-1/commandA-landing-transcripts.txt`):

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 85, "mapped": 85, "missing": [],
 "rule_blocks": 14}
```

So the frozen falsifiable `84 → 85, mapped 85, missing [], dangling []` is
**REPRODUCED on the overlaid tree**, not merely projected. `rule_blocks`
stays 14, as it must (c3's axis). Late convergence seats (VZ-2, CR-5..8)
independently reached the same 85/85; that agreement is reconciliation.

### 2.3 Verdict and landing moves

**C2 VERIFIED.** Land in this order: (1) copy the entry to
`corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md`; (2) append the
token to the EVM row (`corpus/README.md:38`, patch text in EX-7.md §3);
(3) fix the one cosmetic CBOR byte label (`73 736f6c63` → `64 736f6c63`) in the
same copy if the integrator wants the entry's byte listing exact — no claim
depends on it; (4) re-run command A for the record. Precision note, not a
discrepancy: the headline `5f3560e01c` prologue is opt200's; viair-noopt
reaches the same EQ-chain + SUB-leg shape through a `PUSH2 0x0116 JUMP` routine
(no `5f3560e01c` at the head). The entry's "same shape holds in viair-noopt
(chain dsts 208–273, same SUB final leg at 194)" is accurate as written.

## 3. C3 — rule #15

### 3.1 Baseline and the three texts

Command A before: `rule_blocks 14`, `citation_resolved_rules 14`, depth 10.0
at `c625d5d` — REPRODUCED. The craft section is SKILL.md:81, ends at :255,
next header at :260.

- **SC-3's draft**: extracted from `claims/c3/SC-3.md` §4 fenced block →
  **1,605 B, 23 lines, sha256
  `763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1`** —
  byte-exact match to SC-3's self-identity claim.
- **SC-4's corrected text**: extracted from `claims/c3/SC-4.md` →
  **1,605 B, 23 lines, sha
  `a1bceb4074328d9d60d14ddf0789b9bcd18ca38936c217d78fc37b1091ec1789`**. Its
  `diff` against SC-3 is exactly the two citation fixes below (no other
  change).
- **RV-7's draft**: `claims/c3/RV-7/rule15-bullet.md` → **1,565 B, 23 lines,
  sha `ccbc5cdbbefc86081393cd4d60ef9c85606c3dd1c98ed76d63520da1da0b67e7`**,
  and the copy in RV-7.md's fenced block is byte-identical.

### 3.2 Content checks

- **SC-3 CORRECTION 1 (VZ-4/SC-4/CR-8, independently reproduced):** the draft
  cites `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:34` for "empty
  results do not prove absence of dispatch". `:34` is the erratum header
  `## Erratum (arc3-loop1-round5 correctness sweep, append-only)`; the quote is
  at **`:29`**.
- **SC-3 CORRECTION 2:** the first clause attaches `r1:24` to "blobs that
  byte-contain the full runtime"; `:24` carries the 0-function result and says
  the opposite about containment ("Creation blobs carry no runtime dispatch
  table"). The containment measurement is at `:31`, cited later in the same
  draft. SC-4's text moves the `:24` citation behind "0 functions" and lets
  the following `:31` carry the embedding — both fixes, nothing else.
- **RV-7's draft**: every citation resolves (command A 15/15), the r1:24 quote
  and its :31 erratum are correctly separated, and its extra numbers re-derive
  exactly: **VaultB opt200 1,621 B at +34 in 1,655 B; CarrierV 1,562 B at +20
  in 1,637 B**.
- **RV-7's F1 VERIFIED:** the r3 entry's round-5 erratum at `:41` attributes
  "Creation blobs carry no runtime dispatch table" to r3 `:24`, but that
  sentence never appears in the r3 entry at `c418be0`, `40de383` or `58c3db7`
  (it appears only inside the erratum itself); r3 `:24` is the Rv2TokenOpt
  RESULT row, and the quoted sentence is r1's at `:24`. The erratum's byte
  facts are true; only the pointer is wrong. Disposition: a future append-only
  correction in the r3 entry; the landed rule must not propagate the pointer
  (neither SC-4's nor RV-7's text does).

### 3.3 Before → after, demonstrated

Appended each text verbatim to the craft section of a `c625d5d` scratch repo
(entry + token from §2 already present), committed, and ran command A's exact
split/resolution. SC-3, SC-4 and RV-7 each give `rule_blocks 15`,
`citation_resolved_rules 15`, `depth_score 10.0`, coverage 10.0, 15/15 rules
resolvable (`CN-1/commandA-landing-transcripts.txt`). The frozen falsifiable is
met by all three.

### 3.4 Convergence ruling for C3

**Land exactly one, and land it verbatim.** Recommended: **SC-4's corrected
text (`a1bceb40…`, 1,605 B)**. Reasons: (1) it preserves the designated SC-3
draft's wording and differs only by the two citation fixes, both independently
confirmed; (2) it is content-clean — 15/15 resolved, no known wrong-line
anchor; (3) its delivered identity is valid for the landed bytes (no
post-delivery edit). **RV-7's text (`ccbc5cdb…`) is the zero-edit
alternative** if the integrator prefers a draft that never needed a fix; it is
also content-clean and lands 15/15. Do **not** land both (that would read
`rule_blocks=16`; the claim's falsifiable is 14→15). Do not land SC-3's
original `763c44b5…` bytes without both fixes.

## 4. Peer reconciliation

- **PL-2 / RV-3 (revised):** their current artifacts verify PL-4 and archive
  their prior competing designs (`PL-2/prior-attempt/`, `RV-3/prior-attempt.md`).
  My §1.4 numbers apply to those archived bytes; the seats' own convergence is
  correct on the evidence I measured. Their endorsement plus PL-1's superset
  makes PL-4/PL-1 the c1 landing base.
- **PL-1:** merged build `7724adcc…` independently reproduced; discriminator
  arms measured. Recommended over PL-4 alone.
- **VZ-4** (`claims/verdicts/VZ-4.md`): its C1 before-state, seeded faults and
  boundary (locus-free staleness only) are independently confirmed; its C2
  PENDING is now closed by EX-7 with a measured 85/85; its C3 `:34`→`:29`
  CORRECTION is reproduced. Its C1 audit covered only the prior RV-3 design
  (PL-4/PL-2 landed after its poll); this artifact fills that gap.
- **RV-7** (`claims/c3/RV-7.md`): F1 verified; draft and all cited numbers
  verified. Its F3 warning — landing candidate (a) before a corpus entry would
  drop depth to 9.33 — is consistent with command A's rule (`valid =
  bool(refs)`); irrelevant to the three landed candidates.
- **SC-4** (`claims/c3/SC-4.md`): its corrected text verified byte-exactly and
  at 15/15. Its two fixes match mine independently.
- **Late convergence seats (CN-2, CN-4, CR-5..8, VZ-2):** same landing triad;
  their split between PL-4-as-is and PL-1 is reconciled here by measurement:
  PL-1 keeps every PL-4 arm and closes the three holes, so it is the stronger
  landing; PL-4 remains the minimum compliant fallback.
- **EX-6** (`claims/c2/EX-6/`): evidence only, no `.md` artifact — by the
  wave's own standard that seat is incomplete, not a deliverable. Its three
  pipeline outputs are real and consistent with EX-7's; EX-7 supersedes it for
  the viaIR Unknown.

## 5. What I did not do

- Did not land any change (integrator's move) and did not modify the gate,
  corpus, SKILL.md, PROVINCE.md or SCORECARD.md.
- Did not re-run every late-peer arm; I verified the discriminators (PL-1 vs
  PL-4 on reflow/wall/cross/truncation, SC-4 identity and 15/15, PL-2/RV-3
  revision headers).
- Did not test PL-1's wall FORBIDDEN list against paraphrases beyond "hit" vs
  "hits"; the exact phrase is caught, a paraphrase is not — the literal-register
  residual is stated, not hidden.
- Did not audit the full 42-file EX-7 manifest; I verified the `out/`,
  `probe/` and entry files the claims name.
- Did not run the bypass-of-the-gate paths or REA 6.5/6.6 pins; c2's live legs
  used 6.4.0 and 6.7.0, matching the entry's pins.

## 6. Evidence inventory (under `claims/verdicts/CN-1/`)

- `c1-patch-identities.txt`, `late-peer-addendum.txt` — applied vs claimed
  shas, PL-1 identity and discriminator arms, SC-3→SC-4 diff.
- `gate-arms-matrix.txt` + `runs/` — every gate × tree arm run (4 gates ×
  12 trees where applicable), exits and declared classes.
- `json.gate-pristine.json`, `json.pl4.json`, `json.pl2.json`,
  `json.rv3.json` — clean-tree JSON invariance pairs.
- `clean.v10.txt`, `pl4-repo-root.txt` — baseline and PL-4 on the real root.
- `byte-census.txt` — leg sizes/shas, guard, EQ/SUB/GT legs, PUSH4 census,
  probe envelope summary, VaultB/CarrierV embeddings.
- `probe-live-*.json` — my live REA probes (6.4.0/6.7.0, viaIR opt/noopt,
  std control, creation).
- `commandA-landing-transcripts.txt` — 84/84 before; 85/85 entry landing;
  15-rule landings for SC-3, SC-4 and RV-7.
- `SC-3-rule15.md`, `SC-4-rule15.md`, `RV-7-rule15.md` — the extracted draft
  bytes measured above; `pl1-r10.py` — the PL-1 build I reproduced.
