# EX-29 — census SCOPE retirement analysis (chain c3, arc3-loop1-round1)

Seat EX-29, executor, chain c3. Task: for each stale-bound or dated row of the
census SCOPE table, make the **re-key-vs-retire** call **with cause**; apply the
r3 "dated records adjudicated, not edited" precedent; flag any row where a
re-key would widen bounds just to pass (laundering risk).

State at analysis time (all receipts below are re-runnable):

| item | value |
|---|---|
| HEAD | `e845c2b524ad2e59871e004c51a1386e192a74ab` |
| instrument | `.ufo/gates/c1-census-v10.py`, 433 lines, sha256 `36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48` |
| PROVINCE.md | 162 lines, sha256 `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` |
| SKILL.md | 371 lines, sha256 `5c93c7c1bf45c72ca518f87fbba6f2a0bbf5685f67d263714b210a9a058830d4` |
| SCORECARD.md | 1336 lines, sha256 `30129a98d6f3f32d0920b3782a91cd3dc46b0d350a94c7ae15cb5f82164b57f8` |

Receipts in this directory: `census-head-verbose.txt` (full v10 run at HEAD),
`scope-audit.txt` (per-row bound/content audit), `row-locus-counts.txt` (per-row
locus-block counts), `literal-audit.txt` (every version literal vs locus vs
scope row), `sim-outputs.txt` + `sim/sim-suite.py` (the eight measured
simulations), `patched-run.txt` (the recommended patch applied to a verification
copy: PASS at the repo root, tripwire still fires on a planted append),
`patch-diff.txt` (the generated diff), `PATCH-census-disposition.patch.md`
(patch text for EX-28).

## 0. Verdict

- Census v10 at HEAD, verbatim: `VERDICT: PASS  (stale=0 ambiguous=0
  undeclared=0 unresolved=0)`, `SCOPE-ERRORS (marker assertions): []`, exit 0
  (`census-head-verbose.txt`).
- **No row's bound is stale at HEAD.** All 20 rows are content-tight: each row's
  first line is the heading/first block line it was keyed for, and its last line
  is the last line of that block (next line blank or a heading). Evidence per
  row: `scope-audit.txt`. → **re-key: none required at HEAD.**
- **4 rows carry zero loci**: 3 (PROVINCE 40-43), 12 (SCORECARD 417-466),
  13 (SCORECARD 467-502), 20 (SCORECARD 769-855) (`row-locus-counts.txt`).
- **Calls: RETIRE 2 rows (3, 20); RETAIN 18 rows.** Cause per group in §2.
- Every version literal in the three files sits **inside** a declared row
  (49 literals; 0 outside) — a stronger measurement than the instrument's own
  `undeclared=0`, because the instrument only evaluates gate-token-bearing
  blocks (`literal-audit.txt`; §4.3).
- 4 laundering vectors flagged and refused with measured receipts (§3).

## 1. Decision rule (stated so the call is reproducible, not judged per case)

A row is a **candidate** for retirement only if it has no classification duty.
Measured test, applied to every row at HEAD:

> **RETIRE** iff the row's range contains **no census locus** AND **no version
> literal** AND the row is not needed by another row's marker assertion.
> **RETAIN** otherwise. **RE-KEY** iff the row's bounds are not content-tight at
> HEAD (none are).

Rationale for the literal clause: a locus is only the *current* way a literal is
evaluated; the census's own `INLINE_MARKER`/G16 machinery exists because
literals migrate in and out of gate-visible blocks. A row whose range holds a
literal is the only classification path for that literal that does not require
editing the dated record that carries it — which r3 forbids ("dated records
adjudicated, not edited", `SCORECARD.md:789-791`). A row whose range holds
nothing at all classifies nothing.

## 2. Per-row dispositions (all 20 rows, HEAD content)

loci = census locus blocks whose first assertion line falls in the row;
lit = version literals (`VER` semantics) on lines in the row.

| # | row | class | marker@ | loci | lit | tight | CALL |
|---|---|---|---|---|---|---|---|
| 1 | PROVINCE.md 8-13 | CURRENT | — | 1 | 3 | yes | RETAIN |
| 2 | PROVINCE.md 15-26 | CURRENT | — | 1 | 9 | yes | RETAIN |
| 3 | PROVINCE.md 40-43 | DATED | 40 | **0** | **0** | yes | **RETIRE** |
| 4 | PROVINCE.md 44-44 | CURRENT | — | 1 | 1 | yes | RETAIN |
| 5 | PROVINCE.md 45-62 | DATED | 40 | 1 | 1 | yes | RETAIN |
| 6 | PROVINCE.md 64-71 | CURRENT | — | 1 | 1 | yes | RETAIN |
| 7 | PROVINCE.md 119-131 | DATED | 119 | 1 | 1 | yes | RETAIN |
| 8 | SKILL.md 10-16 | CURRENT | — | 1 | 1 | yes | RETAIN |
| 9 | SKILL.md 18-20 | CURRENT | — | 1 | 2 | yes | RETAIN |
| 10 | SCORECARD.md 56-60 | CURRENT | — | 1 | 4 | yes | RETAIN |
| 11 | SCORECARD.md 273-326 | DATED | 273 | 1 | 5 | yes | RETAIN |
| 12 | SCORECARD.md 417-466 | DATED | 417 | **0** | 1 | yes | RETAIN |
| 13 | SCORECARD.md 467-502 | DATED | 467 | **0** | 4 | yes | RETAIN |
| 14 | SCORECARD.md 503-533 | DATED | 503 | 1 | 2 | yes | RETAIN |
| 15 | SCORECARD.md 534-560 | DATED | 534 | 1 | 3 | yes | RETAIN |
| 16 | SCORECARD.md 619-619 | DATED | 619 | 1 | 1 | yes | RETAIN |
| 17 | SCORECARD.md 620-620 | DATED | 620 | 1 | 1 | yes | RETAIN |
| 18 | SCORECARD.md 636-702 | DATED | 636 | 1 | 1 | yes | RETAIN |
| 19 | SCORECARD.md 703-768 | DATED | 704 | 2 | 8 | yes | RETAIN |
| 20 | SCORECARD.md 769-855 | DATED | 769 | **0** | **0** | yes | **RETIRE** |

### 2a. RETAIN — justified by loci (16 rows: 1,2,4,5,6,7,8,9,10,11,14,15,16,17,18,19)

Cause (common): the row contains at least one census locus whose disposition it
determines, its bounds are content-tight at HEAD, and where DATED, its declared
marker text is present at the declared line (re-asserted: `SCOPE-ERRORS: []`).
Two of these rows carry the r3 precedent in their own content and are retained
*un-edited*: row 7's cells carry in-place erratum annotations
(`PROVINCE.md:124` "**round-12 audit correction**", `:125` "[r5-audit C8: …]")
and row 18 carries round-2's receipt-anchored `config.toml:2940` reference
(`SCORECARD.md:699`), adjudicated at r3 as dated text (`SCORECARD.md:789-791`).

Row 16 deserves a note: its single locus `:619` is disposed `current-ok (value
equals a live anchor)` **by G16, not by its DATED scope** — the DATED declaration
is still load-bearing, because without the row the same literal falls to
`AMBIGUOUS` (no client token in clause; not a G17 keyword) and fails the run.
The literal `6.5.0` is correct at record time (the luna-round-6 battery ran on
6.5.0); per r3 the capability record is adjudicated, not edited.

### 2b. RETAIN — zero loci but literal-bearing (rows 12, 13)

- Row 12 (SCORECARD 417-466, luna-round-5): literal `:463` (`6.5.0`).
- Row 13 (SCORECARD 467-502, luna-round-6): literals `:467` (heading), `:471`,
  `:496`, `:500` (all `6.5.0`).

Cause: these literals are **gate-invisible** — their paragraph blocks contain no
`REA_GATE` token (`rea-agents|\brea\b|config.toml|mcp_config.json|mcp.json|
mcp_servers|devin|\bomp\b|kimi|npx`), so no locus is minted and the row
classifies nothing today. They are retained because (a) they are the only
classification path for dated-record literals if a future edit adds a client
token to those blocks, and (b) the alternative classification path is an inline
marker written into the dated prose — record editing, refused by r3. Measured:
retiring them anyway is verdict-neutral at HEAD (SIM-A2), so this is a
defensible-minority call, not a load-bearing one; the recommended set in §0
keeps them.

### 2c. RETIRE — loss-free (rows 3 and 20)

**Row 3 — PROVINCE.md 40-43, DATED, marker@40.** Zero loci, zero literals. The
range holds the Core section's dated opener ("Surfaces owned now — each verified
on this host 2026-10-13.") and the table header. Cause for retirement:
(i) it classifies nothing at HEAD — a one-token edit cannot make it a locus,
because no literal exists in it (a locus there would require *new text*);
(ii) row 5's marker assertion does not depend on it — `ml=40` is asserted
against the file's line 40, which survives the retirement (SIM-A1:
`SCOPE-ERRORS: []`);
(iii) after retirement PROVINCE 40-43 is undeclared, which is **fail-closed**:
any future literal written there raises `UNDECLARED` and forces a decision at
that time — the r4 fail-closed doctrine (E15 §3.4, "re-keyed to EOF each round
(fail-closed, visible)"), applied to the retire direction.
Cost: a future errant literal there costs one narrow declaration later.

**Row 20 — SCORECARD.md 769-855, DATED, marker@769.** Zero loci, zero literals
(the whole r3 section is adjudication prose: the 30 literals in SCORECARD.md all
sit at or below `:753`; `literal-audit.txt`). Same cause as row 3. Additional
measured point: the section's own E22 debt line (`SCORECARD.md:850-852`) is
discharged by this artifact, so the range's remaining content is pure history.

Both retirements are **verdict-neutral at HEAD, measured**: SIM-A1 (rows 3+20
removed) → `PASS 0/0/0/0`, `SCOPE-ERRORS: []`, exit 0; SIM-A2 (rows 3+12+13+20)
→ same (`sim-outputs.txt`). Recommended patch, line-safe, in
`PATCH-census-disposition.patch.md`.

**Divergence to adjudicate (named, not hidden).** Same-chain drafts conclude the
opposite branch: SC-6's E22 disposition draft says "**RETIRED: none** — the
debt's 'or retire' branch was not taken"
(`claims/c3/SC-6/e22-disposition.draft.md` §3 row 5), and SC-7's header draft
says "No SCOPE-table edit: at HEAD no scope row is undeclared or stale … no row
is retired" (`claims/c3/records-drafts/census-header-draft.md` §1). Those drafts
are correct on the claim's *antecedent* (nothing is stale, so the re-key branch
is not triggered) but neither performs the per-row retire analysis this seat was
tasked with. EX-29's finding: the two retirements are **not required** for the
claim's PASS (both drafts' zero-diff landing is claim-satisfying, and the patch
file says so), but they are the loss-free discharge of the debt's "or retire"
branch under the §1 criterion — rows that classify nothing at all. Parent's call;
the measurement exists either way.

## 3. Laundering-risk flags (each with the measured receipt)

**F1 — widening a DATED end bound to cover a new append. REFUSED.**
The move: extend row 20's end past 855 so a new round's records append (which
cites a version) lands inside a DATED range and is classified `historical`.
Measured (SIM-B1/B2/B3, `sim-outputs.txt`): with a stale claim planted at the
append's first line (`:856`, `rea-agents@6.4.0` under kimi), the landed table
gives `FAIL undeclared=1` exit 1; the same plant under row 20 widened `855→856`
gives `PASS 0/0/0/0` with the locus disposed `historical (dated scope)`; widened
`855→1336` (to EOF) gives the same shelter. This reproduces r4's finding —
"an open-ended DATED bound launders any future stale append; a fixed bound does
not" (`R3.md:62-75`, matrix rows 10/11 vs 12 at `R3.md:293-294`), and the
overshoot form `635,900` (`R3.md:69`) — and CR3 §2.5's in-range caveat
(`CR3.md:110-124`). The r4 disposition already refused this path
(`SCORECARD.md:881-884`: "the open-ended-bound laundering path (CR3/P3/R3,
measured) was refused"); this seat re-verified it independently.

**F2 — declaring the currently undeclared regions as DATED. REFUSED.**
The move: add DATED rows for SCORECARD 856-1336, PROVINCE 132-162, SKILL 21-371.
Zero loci today (measured: 0 literals in all three regions; the 856-1336
pin-freeness is also recorded at `SCORECARD.md:1069`), so the rows would buy
nothing and would convert 480+ lines of future content into a historical
shelter — exactly F1's shelter, pre-installed. The property that keeps the short
bound safe is the *pin-free append discipline* (`E15.md:183-198`, "clean form",
`E21` convergence), not an extended bound. If a future append does carry a
literal, the correct response is a narrow declaration anchored to that block —
never a blanket range. Related, independent finding (RV-10,
`claims/c3/RV-10/bounds-line-by-line.md` §3): Z1 §4d's fixed-bound *comment* was
never landed with the two r4 rows — a documentation gap in the same doctrine
this flag protects; RV-10's restore patch is
`claims/c3/RV-10/proposed-fixed-bound-guard.patch.md`.

**F3 — widening the single-line rows 16/17 (619, 620) to the Capabilities
table. REFUSED.** Those two rows exist to classify two capability-row literals
(`REA 6.5.0`, `REA 6.4.0`). A future capability row with a stale literal is
correctly `AMBIGUOUS` → FAIL under the landed table; widening the rows to
`619-625` would auto-classify it `historical`. Same shelter, same refusal.

**F4 — un-anchored bound moves / un-re-keyed slides (residual, needs an
assertion). REFUSED as a re-key form; not fixable by any bound choice.**
The move: leave the line numbers alone after the file grows above a row (or move
them without re-deriving from content). Measured (SIM-C1/C2/C3,
`sim-outputs.txt`): a stale claim planted in the luna-round-1 tail (`:272`,
undeclared today) is caught by the landed table (`FAIL undeclared=1`, exit 1);
under row 11 as the content-equivalent of an un-re-keyed +5 slide
(`273,326 → 268,321`) the same claim is absorbed as `historical (dated scope)`
and the run PASSes; the content-anchored re-key of the same geometry (`278,331`)
does **not** absorb it (`FAIL undeclared=1`). So the slide direction silently
absorbs stale statements into DATED ranges, and nothing in v10 detects it (G15
asserts the marker line, never that the endpoints still bracket the keyed
block). Mitigation, proposed not landed: a **G18 bound-drift assertion** — for
each DATED row, assert `start` is the declared marker/heading line and `end+1`
is blank or a heading (the anchor test in `scope-audit.txt` is a working
prototype; it is green on all 20 rows at HEAD). Sketch only; it is a new
assertion and needs its own falsification before landing.

## 4. Residuals and honest limits

1. **The instrument has always trusted DATED ranges absolutely** (CR3 §2.5:
   "a fabricated pin there passes today"). This analysis does not fix that and
   does not claim to; it refuses *new* shelters and removes two that classified
   nothing. F4's assertion proposal is the only structural fix named here.
2. **"0 undeclared" ≠ "0 literals outside declared rows".** 13 of SCORECARD's
   30 literals are gate-invisible (§2b), so the instrument cannot see them at
   all. This seat measured the stronger property directly: 0 literals outside
   declared rows (`literal-audit.txt`). That property, not the instrument's
   verdict, is what the retirements were checked against.
3. **Retirement is fail-closed, and that has a cost**: a future erratum appended
   inside 40-43 or 769-855 that cites a version will FAIL the census until
   declared narrowly. That is the intended signal (r4 doctrine), not a defect —
   but the parent should expect it rather than be surprised by it.
4. **Wave-level constraint for the records append**: the round's own SCORECARD
   section (which lands at `:856+`, outside every declared row) must be
   **version-token-free** or the census FAILs `undeclared=1` at the new block —
   measured by SIM-B1 and already recorded at `SCORECARD.md:1069`. This applies
   to the parent's records commit, not to this seat.
5. **The census edit must be line-safe.** r5 seat reports cite census line
   numbers (`arc2-loop1-round5/E6.md:7` `:67-70,370-429`; `E5.md:56,90`
   `:97-108,202-215,391-399`; `CR4.md:66,72` `:74-83,124-135,218-234,370-386`;
   `R6.md:13` `:5-10,74-80,124-134,218-234,376-399`; `C4.md:107` `:85-108`);
   those are dated records (r3: adjudicated, not edited), and the lane's
   precedent is line-safe landings (r8's re-key changed 3 lines in place, net 0;
   `git show 6bc4c29 -- .ufo/gates/c1-census-v10.py`; CR7's +18-line shift attack
   refused, `SCORECARD.md:755`). The recommended patch therefore replaces the
   two retired rows in place and appends the disposition at EOF.
   **Trade-off the parent must weigh:** the claim asks for the disposition
   "stated in the instrument's own header", and the same-chain header stanzas
   (SC-6 `e22-disposition.draft.md` §6 P1; SC-7 `records-drafts/census-header-draft.md`
   §2) achieve that by expanding line 1 into a ~15-line docstring — a **net +14
   to +16 line insertion** that moves every citation below it (SCOPE 86→~100,
   `:97-108`→~111-122, `:370-429`→~384-443). Checked and *not* a probe risk:
   `.ufo/gates/citation-drift/pointer-table.json` pins no census line (0 matches
   for `census` in its `entries`/`quoted` rows), so no probe finding is created;
   the r5 citations drift as dated records and are adjudicated under r3. If the
   header form lands, this seat's EOF block is redundant — take one, not both.
6. **Scratch**: `/tmp` was unusable at this seat's run time — writes fail with
   `Errno 122 Disk quota exceeded` (13G used of 16G tmpfs; the write probe
   returned exit 120 for a redirected `--json` run, exit 1 for a shell write).
   All simulations therefore ran self-contained from this seat directory,
   building their fixtures at run time and removing them at the end
   (`sim/sim-suite.py`); no scratch survives outside this directory.
7. **Scope of this artifact**: it is an analysis + patch text. It writes no
   instrument, no corpus file, no SCORECARD/LOG line. Landing the patch is
   EX-28's (c3) write; the disposition text for the census header is drafted in
   the patch file.

## 5. Reproduction

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 .ufo/gates/c1-census-v10.py                       # PASS 0/0/0/0, exit 0
python3 .ufo/gates/c1-census-v10.py > claims/c3/EX-29/census-head-verbose.txt
python3 claims/c3/EX-29/sim/sim-suite.py > claims/c3/EX-29/sim-outputs.txt
# per-row audits: scope-audit.txt, row-locus-counts.txt, literal-audit.txt
#   (generated by the inline scripts recorded in this seat report §1)
git show 6bc4c29 -- .ufo/gates/c1-census-v10.py           # the r8 line-neutral re-key
```
