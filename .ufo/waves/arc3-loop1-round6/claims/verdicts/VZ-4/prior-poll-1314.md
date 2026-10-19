# VZ-4 — arc3-loop1-round6 convergence verdict

Seat: VZ-4, verdicts/convergence chain, wave arc3-loop1-round6, 2026-10-19.
Repo HEAD at direct checks: `c625d5de57e045188b5ce8cd450a57b34f90785` (records;
work `58c3db7` — matches claims-frozen.md). Every number below is my own
measurement (lane rule #14); peer artifacts are used only for convergence
comparison and are re-derived before I rule on them. I wrote only this
artifact dir (`claims/verdicts/VZ-4.md` + `claims/verdicts/VZ-4/`); git
read-only; gates/corpus/SKILL.md/PROVINCE.md untouched. Scratch: `/var/tmp/vz4-r6-scratch/`.

## Summary

| Claim | Ruling |
|---|---|
| C1 operability (census Frontier blind spot) | **REPRODUCED end-to-end**: before-state verified first-hand (Frontier 73-93 + 133-162 UNDECLARED; seeded locus-free stale literal at :91-93 reads PASS exit 0 under the r9 gate while the clean tree also reads PASS; an instrument-visible stale pin in the same region reads FAIL undeclared=1 — the gap is precisely locus-free staleness). Peer RV-3's in-place r10 patch (FRONTIER_REGISTER) audited by me: round-trips byte-exact (`8e420679…`), clean tree PASS with JSON identical modulo two additive keys, my pre-existing fault tree now FAILs with named FRONTIER-STALE/FRONTIER-UNATTESTED classes, UNDECLARED path intact, all 14 register citations exist. One cosmetic nit (repr-escaped patterns in messages). |
| C2 coverage (corpus Unknown) | **BEFORE-STATE REPRODUCED** (command A 84/84, missing [], dangling []); both frozen candidates are genuinely open at HEAD (r3 `:33` viaIR; r4 `:28` optimizer forms; CR-1's K8 variants probed 8/8 K/K, never byte-characterized). Peer EX-6's retained viaIR evidence spot-checked first-hand and real; the C2 entry itself was not yet landed at my final poll — **PENDING** on the entry + map token (85/85). |
| C3 depth (rule #15) | **REPRODUCED with one CORRECTION**: peer SC-3's draft reproduces end-to-end under my own re-derivation (byte census, draft self-identity, scratch 14→15 with 15/15 resolved at both revs), but its citation `2026-10-19-arc3-r4-evm-vyper-leg.md:34` is a **mis-citation** — the quoted limitation text lives at `:29`; `:34` is the erratum section header. Fixes before landing; does not affect command-A resolution (34 ≤ 63 lines) but the landed rule would mispoint. |

## C1 — operability: the census Frontier blind spot (R1 residual)

### SCOPE coverage at HEAD — VERIFIED ABSENT

`.ufo/gates/c1-census-v10.py` (sha256 `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`)
SCOPE table (`:216-236`) declares PROVINCE.md only at:

```text
216: ("PROVINCE.md",   8,  13, "CURRENT", ...)
217: ("PROVINCE.md",  15,  26, "CURRENT", ...)
218: ("PROVINCE.md",  40,  43, "DATED",   40, ...)
219: ("PROVINCE.md",  44,  44, "CURRENT", ...)
220: ("PROVINCE.md",  45,  62, "DATED",   45, ...)
221: ("PROVINCE.md",  64,  71, "CURRENT", ...)
222: ("PROVINCE.md", 119, 131, "DATED",  119, ...)
```

No row covers 73-93 (`## Frontier`, confirmed at PROVINCE.md:73) or 133-162
(`### Round-4 frontier (post-unlock)`, confirmed at :133). `wc -l PROVINCE.md`
→ `162 PROVINCE.md`. The frozen "before" claim — Frontier UNDECLARED at HEAD —
**REPRODUCES**.

### Clean tree reads PASS — REPRODUCED

`python3 .ufo/gates/c1-census-v10.py --root .` (at the repo root, HEAD tree):

```text
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)   exit=0
```

### Seeded fault #1 (the frozen falsifiable) — BLIND SPOT REPRODUCED

Scratch tree `/var/tmp/vz4-r6-scratch/seeded` (copies of the three scoped files
+ the gate), with the EVM bullet at :91-93 replaced by the stale literal
(full diff retained at `claims/verdicts/VZ-4/seeded-fault-diff.txt`):

```diff
92,93c92,93
<   (Core, r3-07), real solc-0.8.37 carriers (Core, arc3-r1/r3) and a vyper-0.4.3
<   carrier (arc3-r4); selectors stay bare hashes (no signature DB → no name resolution).
---
>   (Core, r3-07); real solc/vyper-compiled bytecode untested.
>   Retention decays oldest-first.
```

Gate on the seeded tree → **`VERDICT: PASS (stale=0 ambiguous=0 undeclared=0
unresolved=0)` exit 0**, byte-counters identical to the clean run
(PROVINCE=17/SCORECARD=14/SKILL.md=3, total loci 17; full output retained at
`claims/verdicts/VZ-4/seeded-fault-gate-output.txt`). Note the seeded bullet
even carries non-instrument version literals (`solc-0.8.37`/`vyper-0.4.3` sit
in the *clean* text and are already invisible) — the instrument's needles
(`rea-agents@\d+.\d+.\d+`, `(?<![\d.])6\.\d+\.\d+`, config `path:line`) match
none of them. "Reads PASS identically whether or not the bullets are stale" —
**VERIFIED**.

### Seeded fault #2 (boundary characterization, VZ's own)

Restoring :91-93 and planting an *instrument-visible* stale pin at PROVINCE.md:88
(Frontier region): `- **Alternate providers** — REA lane pins rea-agents@6.3.0
on all engines (STALE TEST)` → **`VERDICT: FAIL (stale=0 ambiguous=0
undeclared=1 unresolved=0)` exit 1** (retained at
`claims/verdicts/VZ-4/frontier-pin-fault.txt`). So the UNDECLARED→FAIL class
already fires for pin/bare-6.x/path loci anywhere in PROVINCE; the C1 gap is
**locus-free capability staleness only**. This matches the frozen claim's own
framing ("a marker scheme suited to bullets that carry no pin/version/path
loci, or a declared secondary classification … a frontier-claim register").
Any c1 patch must keep fault #2 failing (it already does via UNDECLARED) while
making fault #1's class gradable, and must not disturb the clean PASS or any
SCOPE row/counter.

### Hand-audit markers consistent with the residual record

PROVINCE.md:157 still carries a bracketed hand-audit note ("[r5-audit C1: lane
landed — stale pending-status wording removed]"), and the r4-round record
names the residual verbatim at `SCORECARD.md:1620` ("the census gate cannot
grade the Frontier region — named residual R1") and `:1631-1632` ("Frontier
region UNDECLARED — the repairs are clause-audited, not instrument-graded").
The "clause-audited by hand, not instrument-graded" premise — **VERIFIED**.

**C1 before-state verdict:** **VERIFIED** (blind spot reproduces; boundary is
locus-free staleness). Historical depth also verified: `git show fbbbd45:PROVINCE.md`
line 92 carries the retired literal "…real solc/vyper-compiled bytecode
untested; …" and `git log --oneline -S 'real solc-0.8.37 carriers' -- PROVINCE.md`
names `40de383` (r4 work) as the repair — the literal sat in the UNDECLARED
Frontier region across rounds 1-3 while the instrument read PASS (RV-3's §1
provenance claim, re-derived by me).

### Peer RV-3's c1 patch — audited first-hand, REPRODUCED

RV-3 (landed mid-run at `.ufo/waves/arc3-loop1-round6/claims/c1/RV-3.md`)
proposes an **in-place extension to r10**: a new `FRONTIER_REGISTER` table
(13 rows covering all 13 Frontier bullets of :82-93 and :135-162; intro
:75-80 deliberately unregistered) + `frontier_audit()` with three declared
fail classes (FRONTIER-ANCHOR / FRONTIER-UNATTESTED / FRONTIER-STALE), one new
verdict conjunct, two new JSON keys, one new text line. My audit, all
first-hand (lab: `/var/tmp/vz4-r6-scratch/rv3-audit/`):

- **Round-trip — VERIFIED.** Extracted the diff from RV-3.md, `patch -p0`
  onto a pristine `git show HEAD:.ufo/gates/c1-census-v10.py` copy → applies
  clean; resulting sha256 `8e4206796fec2e16fb6f2c1959f33b63bbcb9643471d42472ac6bc2cba195ebf`
  — byte-exact match to RV-3's claimed identity.
- **Frozen (a) clean tree still PASS — REPRODUCED.** r10 gate on a scratch
  clean tree → `FRONTIER register (r10): 13 rows, 0 error(s)`, `VERDICT: PASS`
  exit 0, G2 per-file 17/14/3 unchanged.
- **Frozen (b) seeded reintroduction FAILs with a named disposition —
  REPRODUCED** on **my own seeded fault tree, built before RV-3 landed** (the
  frozen claim's own literal at :91-93): r10 gate → exit 1, `DECLARED FAIL
  CLASSES: ['FRONTIER-STALE', 'FRONTIER-UNATTESTED']`, with
  `FRONTIER-STALE PROVINCE.md:92 stale literal 'untested' reintroduced` plus
  two FRONTIER-UNATTESTED rows for the removed required claims. The exact
  blind spot my seeded fault #1 demonstrated against the r9 gate is closed.
- **Frozen (c) existing rows/counters intact — REPRODUCED.** `--json` on the
  clean tree: r10 vs r9 differ by **exactly the two new additive keys**
  (`frontier_rows`, `frontier_errors`); **no shared key changed** (counts,
  stale/ambiguous/undeclared/unresolved, scope_errors, g7, g11, g2, historical,
  current_ok all identical). My seeded fault #2 (stale pin at :88) under r10 →
  `FAIL undeclared=1` exit 1 with frontier rows clean — the pre-existing
  UNDECLARED class is untouched.
- **Register citations — VERIFIED present.** All 14 corpus files named in the
  13 register rows exist under `corpus/knowledge/` (checked by file, including
  `2026-10-13-r2-crash-inspect-probe.md` and `2026-10-13-r4u-06-adb-surface.md`);
  the two operator-gated rows declare their non-corpus receipt anchor
  (PROVINCE.md:26) in the row text itself. The clean-tree 0-error run also
  proves all 13 anchors and required claims match the live tree.
- **Cosmetic nit (no action required):** FRONTIER-UNATTESTED messages render
  patterns repr-escaped (`'real solc-0\\.8\\.37'`) because the format uses
  `%r` on a raw string; readable, but a landing seat may prefer `%s`-style
  plain text.

Design-choice check: RV-3 records WHY in-place (receipt-web path stability,
in-file provenance convention) and measured WHY the SCOPE-declaration variant
is inadequate (frontier bullets produce zero loci — consistent with my own
boundary experiment). Recorded as the lane's choice per the frozen claim.

**C1 verdict:** before-state **VERIFIED**; RV-3's r10 extension **REPRODUCED**
on all three frozen sub-claims + round-trip + citations. Remaining for the
integrator: apply the patch to the real gate and re-run the two fault arms on
the repo tree (my scratch demonstrations do not substitute for the landed
gate's own run — the write stayed out of my scope, as it must).

## C2 — coverage: the named corpus Unknown

### Command A before-state — REPRODUCED

SCORECARD.md:88-124 recipe, run by me at both source commits (exact JSON
retained at `claims/verdicts/VZ-4/command-A-{58c3db7,c625d5d}.json`):

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "58c3db7", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "c625d5d", "rule_blocks": 14}
```

Before = 84/84, missing [], dangling [] — **REPRODUCED**. The after half
(85/85 with the new entry + map token) had not landed at my final poll —
**PENDING** on the parent's landing.

### Both frozen candidates are genuinely open at HEAD — VERIFIED

- viaIR: named Unknown at `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:33`
  ("optimizer runs values other than 200, the `viaIR` pipeline, and
  cross-minor optimizer differences") and again in r4's Unknowns list at
  `2026-10-19-arc3-r4-evm-vyper-leg.md:28` ("the `viaIR` pipeline; dispatcher
  prologue classes beyond the three now recorded"). Open — **VERIFIED**.
- Vyper optimizer forms: r4 `:28` — "CR-1's `--no-optimize` / `-O codesize` /
  `-O none` and hardfork variants were probed K/K by the probe but their
  dispatcher forms were not byte-characterized here". I re-derived the K/K
  half myself: CR-1's retained `K8.methodids.json`, `K8.nooptimize.methodids.json`,
  `K8.Onone.methodids.json`, `K8.Ocodesize.methodids.json`
  (`.ufo/waves/arc3-loop1-round4/claims/c1/CR-1/out/`) each hold **8 keys**,
  and the default vs `nooptimize` selector sets diff **IDENTICAL** — probed
  K/K ✓; no byte-level shape characterization of those variants exists in the
  corpus (the r4 entry records the Form-A-scoped caveat at `:8` in its source
  list and `:28`). Open — **VERIFIED**.

### Peer EX-6 (c2) raw evidence — spot-checked first-hand (entry not yet landed)

At my final poll EX-6 had landed evidence only (no `.md`):
`claims/c2/EX-6/{src/ViaIRVault.sol, out/, evidence/}` with three pipelines
(`legacy-opt200`, `viair-opt200`, `viair-nopt`) × runtime/creation hex+bin,
abi, methodIdentifiers, opcodes. I read the retained opcodes myself:

- `legacy-opt200` prologue: `PUSH1 0x4 CALLDATASIZE LT PUSH2 … JUMPI PUSH0
  CALLDATALOAD PUSH1 0xE0 SHR … PUSH4 0x8DA5CB5B GT … EQ …` — the recorded
  solc legacy class (GT pre-filter + EQ compare tree), consistent with r3/r4.
- `viair-nopt` prologue: `CALLDATASIZE … JUMPI … JUMP` into a routine running a
  **linear EQ chain** (`DUP1 PUSH4 0x017A5C46 EQ PUSH2 … JUMPI …`) — reached by
  direct `JUMP`, not inline in the prologue: a shape distinct from all three
  recorded prologue classes.
- `viair-opt200` prologue: input-size check then **fallback-first** layout —
  `CALLDATASIZE ISZERO PUSH2 … JUMPI` into a `PUSH3 0x461BCD PUSH1 0xE5 SHL`
  Error("ViaIRVault: no such function") revert path; no selector decode in the
  prologue at all (dispatch deferred behind body jumps).

This is raw-material verification only: it shows the candidate is closable
from this evidence set, but the C2 claim (a characterized viaIR dispatch shape
landed as a corpus entry + map token, 84→85) remains **PENDING** until the
entry exists; I did not audit a claim that had not yet been written.

**C2 verdict:** before-state **REPRODUCED**; candidates' openness **VERIFIED**;
EX-6's retained bytes spot-checked **REAL** (not fabricated); entry **PENDING**.

## C3 — depth: rule #15 (peer SC-3, audited)

### Baseline — REPRODUCED

`rule_blocks=14`, `citation_resolved_rules=14` at both revs (command A output
above). The craft section sits at SKILL.md:81 (header `## Queue-drain craft
(rounds 5-12, distilled in round 13)`) with the 14 `- **` rule blocks at
:86-255, ending "…never a carried-over number." — matches the frozen
"SKILL.md:81-255 holds rules #1-14". **REPRODUCED**.

### SC-3's evidence chain — re-derived by me, REPRODUCED

- Byte census (my own python over the retained r4 files): `EX-04/out/creation.hex`
  decodes to **1,637 B, sha256 `3c6673966d821d9d…`**; `runtime.bin` **1,562 B,
  sha256 `57d6fd0ae0da0019…`**; runtime occurs in creation at **offset +20**
  with **55 trailing bytes**; `runtime.hex` decodes byte-identical to
  `runtime.bin`. Matches SC-3 §3 and the r5 erratum (`2026-10-19-arc3-r4-evm-vyper-leg.md:43-44`) — **REPRODUCED**.
- Sealed-envelope anchor: `.ufo/waves/arc3-loop1-round4/claims/c1/EX-06/probe/CarrierV-creation-6.4.0.json`
  reads `evidence_id ev_53732d0f8c67d15c…`, `functions: []`,
  `bytecode.sha256 3c667396…` (parsed-and-empty on a blob that byte-contains
  the runtime). Static re-read — **REPRODUCED**. (SC-3's own live-probe id
  equality is same-path determinism by its own correct reasoning; I did not
  re-run the probe.)
- Rule draft identity: the fenced §4 bytes measure **1,605 B, sha256
  `763c44b504f9964d…`**, 23 newline-terminated lines — matches SC-3's
  self-identity claim — **REPRODUCED**.
- Landing mechanics: appending those bytes to the craft section extracted from
  `git show <rev>:SKILL.md` and re-running command A's exact rule-split +
  citation-resolution gives **rule_blocks=15, citation_resolved_rules=15** at
  BOTH `58c3db7` and `c625d5d` (my own scratch re-derivation, agreeing with
  SC-3 §5's table) — **REPRODUCED**.

### One CORRECTION for the integrator

SC-3 cites `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:34` for the
quote "empty results do not prove absence of dispatch" (both in the §4 draft
text and in the §6 table). Measured: the quote lives at **`:29`** (the
Limitations bullet — my grep: `29:- **Limitations (tool-reported, every
leg):** … empty results do not prove absence of dispatch …`); `:34` is the
erratum section header `## Erratum (arc3-loop1-round5 correctness sweep,
append-only)`. The citation still resolves in-bounds under command A's pattern
(1 ≤ 34 ≤ 63), so rule_blocks/resolution are unaffected — but the landed rule
text would point readers at the wrong line. **Fix `:34` → `:29` before
landing.** (Minor, no action needed: the draft's `r1…md:24` anchor covers the
0-functions probe result; the byte-containment clause of the same sentence is
carried by the `:31` erratum citation later in that sentence.)

### Remaining SC-3 citations spot-checked — VERIFIED

`r4…md:39-46` (initcode erratum, "+20"/"present verbatim") ✓; `r4…md:17`
(initcode legs "uniformly parsed-and-empty") ✓; `r4…md:25` (raw-over-hextext
trap) ✓; `r3…md:27` (raw-on-hex-text trap, "a probe-input trap, not a carrier
defect") ✓; `r3…md:41-51` (r5 erratum correcting r3 `:24`, with the six
embedding measurements) ✓; `r1…md:24` (creation legs parsed-and-empty) ✓;
`r1…md:31` (r1 erratum "measured false … embeds the runtime") ✓;
`corpus/QUALITY.md:21` (row 11, parsed-and-empty vs excluded-from-inventory)
✓ — all read at the named lines by me.

**C3 verdict:** SC-3's rule #15 draft **REPRODUCED** end-to-end under my own
re-derivation, with **one corrected citation** (`:34` → `:29`). The falsifiable
(rule_blocks 14 → 15, citations resolving) is demonstrated on scratch trees at
both revs; the real-tree landing is the integrator's move and was not done at
my final poll.

## Peer reconciliation (point-in-time, final poll 13:14 local)

Present at final poll: `claims/c3/SC-3.md` (audited above — the only landed
peer Markdown), `claims/c2/EX-6/` (evidence-only, spot-checked above). Absent
at final poll: all 12 c1-chain artifacts (PL-1..4, EX-1..4, RV-1..4), the
remaining 11 c2 artifacts, the remaining 11 c3 artifacts, and all other
verdicts/convergence artifacts (VZ-1..3, CN-1..4, CR-5..8). No convergence
verdict across chains is possible yet; this artifact records the before-state
measurements each absent chain must move, plus the two seeded faults that
define C1's pass bar.

## Per-item verdict table

| # | Item | Verdict |
|---|---|---|
| 1 | Command A at `58c3db7` + `c625d5d`: 84/84, missing [], dangling [], rule_blocks=14, resolved=14 | REPRODUCED |
| 2 | Gate clean-tree PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0, G2 ok) | REPRODUCED |
| 3 | SCOPE covers PROVINCE only at 8-13/15-26/40-43/44/45-62/64-71/119-131; 73-93 + 133-162 UNDECLARED | VERIFIED |
| 4 | Seeded locus-free stale literal at :91-93 → instrument still PASS exit 0 | REPRODUCED (blind spot real) |
| 5 | Instrument-visible stale pin in Frontier (:88) → FAIL exit 1, undeclared=1 | REPRODUCED (boundary: gap is locus-free staleness only) |
| 6 | "Clause-audited by hand, not instrument-graded" residual record (SCORECARD.md:1620,1631-1632; hand markers e.g. PROVINCE.md:157) | VERIFIED |
| 7 | C1 extension patch (v11 or in-place) — frozen AFTER half | PENDING (no c1 artifact at final poll) |
| 8 | viaIR named Unknown open at HEAD (r3:33; r4:28) | VERIFIED |
| 9 | Vyper optimizer-form Unknown open at HEAD (r4:28); CR-1 K8 variants probed 8/8 K/K, selector sets identical, never byte-characterized | VERIFIED |
| 10 | EX-6 viaIR raw evidence real; three distinct dispatch shapes visible in retained opcodes | VERIFIED (raw material only) |
| 11 | C2 corpus entry + map token, 84 → 85 | PENDING (not landed at final poll) |
| 12 | SC-3 byte census (1,637/1,562 B, +20, 55 trailing; hex==bin) | REPRODUCED |
| 13 | SC-3 draft self-identity (1,605 B, `763c44b5…`, 23 lines) | REPRODUCED |
| 14 | SC-3 scratch 14→15, 15/15 resolved, both revs | REPRODUCED |
| 15 | SC-3 citation `r4…md:34` for the "empty results…" quote | CORRECTED — quote is at `:29`; `:34` is the erratum header; fix before landing |
| 16 | SC-3's other 8 citations incl. `corpus/QUALITY.md:21` | VERIFIED at named lines |
| 17 | Sealed r4 EX-06 creation envelope (`ev_53732d0f…`, 0 functions, sha `3c667396…`) | REPRODUCED (static re-read) |
