# arc3-loop1-round6 — kaidoku-shokunin — round report

**Schedule slot:** R6 — 32–64 seats, `xai-oauth/grok-4.7-fast`.
**Executed as:** 3 zai + 45 opencode-go-7 — the scheduled xai lane returned
403 out-of-credits on all 48 seats; the zai `glm-5.3-flash-low` wave was
interrupted after 3 seats delivered verified artifacts (PL-4's census patch,
EX-7's viaIR entry, SC-3's rule-15 draft — all kept); `antigravity/
gemini-3.8-flash` and `cursor/grok-4.7-xhigh-fast` were each interrupted at
dispatch (0 delivered); the 45 remaining seats completed on
`opencode-go-7/deepseek-v4.1-flash`. Every substitution recorded with cause.
**Work commit:** `2fba56f`. **Records commit:** this commit.

## Work performed

- **C1 — operability: census Frontier blind spot (R1 residual) closed.**
  PL-4's G21 frontier-register patch applied to `.ufo/gates/c1-census-v10.py`
  (sha `d0772ce8…` → `80027570…`, 610→713 lines). The register pins each
  Frontier bullet's span (PROVINCE:73-93 `## Frontier`, :133-162 post-unlock)
  and asserts REQUIRED earning anchors (positive floor — a stripped or
  truncated bullet fails REQUIRED-absent) plus FORBIDDEN retracted literals
  (a reintroduced stale literal fails `FRONTIER-STALE`). **Measured on a
  scratch tree:** the seeded literal "real solc/vyper-compiled bytecode
  untested" back in :91-93 now FAILs `FRONTIER-STALE` where v10 read PASS
  exit 0; the clean tree still reads PASS, 14 rows asserted, errors `[]`;
  all 17 shared JSON counters unchanged. This is the instrument fix that
  makes the r4/r5 PROVINCE repairs instrument-graded instead of hand-audited.
- **C2 — coverage: the r3/r4 named `viaIR` Unknown closed.**
  `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md` landed (EX-7's
  entry + VZ-3's three corrections): viaIR compiles a **fourth dispatcher
  class** — inverted calldatasize guard + linear ascending EQ chain (11-byte
  stride, selectors sorted) + a `SUB`-terminated final leg — distinct from
  the r1 linear, r3 GT/EQ binary-search, and r4 Vyper modulo-jump classes.
  Probe K/K 15/15 at both pins, `dispatch:"abi"`, decoded sha ≡ carrier sha.
  The load-bearing lesson: the `5f3560e01c` prologue does NOT identify the
  pipeline — the compare-tree class does. Map token landed; command A 84→85.
- **C3 — depth: rule #15 landed** (the corrected `a1bceb40…` text, chosen over
  the verbatim `763c44b5…` draft and the RV-7 alternative — only one text may
  land): "a parsed-and-empty result is a statement about the parser's scope,
  never proof of byte absence — settle byte questions with a census (decode,
  locate, hash), not with the probe's function count." The two citation fixes
  (`r4:34`→`:29`, `r1:24`→`:31`) applied. Eight citations, all in-bounds;
  `rule_blocks` 14→15.

## Landed changes

- `2fba56f` — work commit: `.ufo/gates/c1-census-v10.py` (G21 register),
  `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md` (new),
  `corpus/README.md` (EVM map token), `SKILL.md` (rule #15), plus the
  committed wave tree `.ufo/waves/arc3-loop1-round6/` (48 seat artifacts).
- This records commit — SCORECARD section, LOG entry, this report.

## Before → after measurements

| claim | before | after | counting command / evidence | measured at |
|---|---|---|---|---|
| C1 operability | Frontier region UNDECLARED in census SCOPE (no row covers 73-93 or 133-162); seeded stale literal → PASS | G21 register: seeded literal → FAIL `FRONTIER-STALE`; clean → PASS, 14 rows asserted | `python3 .ufo/gates/c1-census-v10.py --root .` on clean vs seeded scratch | `2fba56f` |
| C2 coverage | corpus 84 files; viaIR a named Unknown | 85 files; viaIR closed, fourth dispatcher class | command A (`SCORECARD.md:88`) `mapped` | `2fba56f` → 85/85 |
| C3 depth | `rule_blocks` 14 | `rule_blocks` 15, all 15 resolved | command A `rule_blocks` + `citation_resolved_rules` | `2fba56f` → 15/15 |

Gate confirmations at `2fba56f`: census `PASS (stale=0 ambiguous=0
undeclared=0 unresolved=0)` + `FRONTIER register (G21): 14 rows asserted,
errors: []`; citation-drift `findings=0` both modes; custody `CLEAN 28/28`;
PROVINCE 162 lines.

## Axis verdicts (per-axis, no scalar)

| axis | verdict | evidence |
|---|---|---|
| operability | **improved** | Frontier blind spot closed; stale literal caught; clean PASS held |
| coverage | **improved** | 84→85; viaIR closed with measured fourth class |
| depth | **improved** | 14→15 rules; the parsed-and-empty lesson codified |
| freshness | unchanged | r5 errata hold; no staleness reintroduced |
| calibration | unchanged | 10 → 10 |
| adjacency | unchanged | PROVINCE boundary untouched; gate edit in-lane |

Admission: all three claims verified by measurement; no axis harmed →
**admitted**.

## Provider-resilience record (the round's honest shape)

The round survived two full provider failures and two dispatch interruptions
— xai 403, zai interrupted mid-wave (3 artifacts kept), antigravity + cursor
both interrupted at dispatch — and landed on its fourth effective lane. The
three surviving zai artifacts (PL-4, EX-7, SC-3) turned out to be the three
load-bearing deliverables; the 45-seat refire verified them independently and
caught the corrections the verbatim drafts needed. Recorded as resilience,
not as a clean wave.

## Carried debt (named, not smoothed)

1. Register append-past-:162 residual (named in PL-4's patch text): a new
   Frontier bullet beyond the last declared line sits outside the register
   until re-keyed — same past-the-bound class as SCORECARD:856+.
2. Census `ptr_check` blind spot (R2): unreachable on pin-carrying clauses.
3. Mid-leg faithful retest: still operator-gated (the ~20 GiB host cost).
4. `.ufo/waves/arc2-loop1-round10/C3.md` still dirty; `/tmp` quota standing.

## SHONEN

- `[~]` SKILL.md real decision tables / cited sources — rule #15 landed this
  round (parsed-and-empty ≠ byte-absence), cited to four corpus entries; no
  named non-author verifier.
- `[~]` end-to-end domain task executed and logged — the viaIR leg is a new
  end-to-end leg (compile → probe → byte-walk → entry); logged this round.
- `[~]` instructions executable without oral context — the G21 register is
  self-documenting in the gate; the landing recipe is in the VZ-3 verdict.
- `[~]` no cross-domain bleed — PROVINCE boundary untouched; the gate edit is
  in-lane instrument work; corpus/SKILL changes are scope-internal.
