# records-outline — arc3-loop1-round3 parent-records package (seat CN-2, cross connector)

Assembled 2026-10-19 by seat CN-2. Status: **v1.4 — LATE-JOIN revision: the
wave's token-plan lane hit its monthly quota mid-run and this seat re-ran the
connector role on the Devin backfill. All three chains' records drafts are
folded; the current merged texts are the **v7 fold** (section 213 lines
`83772cc4…`, entry 207 lines `6e20b662…`), PIN-FREE CLEAN and
census-projection PASS, re-gated after C2's last in-window revision
(13:28Z).** The v1.3 texts (v5 fold) were superseded by chain revisions; every
number in this outline was re-derived at v1.4 write time (rule #14), and the
prior fold's receipts are retained with their fold labels. **One cross-chain
collision was measured and independently verified at v1.4: C2's required
registry-row edit reddens C3's landed table entry `skill-registry-custody-pair-row`
unless EX-32's re-anchor (already filed, verified here) lands in the same
commit — §6.5, the round's named landing-order coupling.** Chain work landed
while this seat measured: EX-41's table + expected pair (verified below), C2's
tool + README revision (selftest 22/22, verified below), the round's live
pre/post custody pair (MATCH 5/5, verified below); C1's corpus entry + map
token remain drafts (patch texts; landing rehearsal re-derived here: 83/83),
the SKILL.md registry-row edit is patch text (projection PASS, §6.2).

Every number below is from a landed artifact (cited inline) or a named
`[[FILL]]` the parent measures at the records commit. This seat's artifact
identities are re-derived at close in `claims/cross/CN-2/receipts/identity.txt`
(rule #14 — never inlined).

Method: read the frozen claims (`claims-frozen.md`), the round-2 committed
records (shape precedent, `SCORECARD.md:1418-1496` + `LOG.md:1431-1455`), the
round-2 connector package, the three chains' literal drafts, and the landed
instruments; then reduce the chains' material to one package under an explicit
consistency contract with a measured PIN-FREE gate. The fold is mechanized
(`claims/cross/CN-2/assemble-merge.py`) so a re-fold after any chain revision
is one command plus the §8 gates.

Delivered artifacts of this seat:

| Artifact | What it is |
|---|---|
| `claims/cross/records-outline.md` | this outline |
| `claims/cross/CN-2/merged-SCORECARD-section.md` | merged §R2 pasteable section, 213 lines (literal body 200, **v7 fold**) — C1/C2/C3 bullets spliced verbatim; **pin-free, projection-tested PASS** |
| `claims/cross/CN-2/merged-LOG-entry.md` | merged §R1 pasteable LOG entry, 207 lines (literal body 194, **v7 fold**) — same provenance |
| `claims/cross/CN-2/pin-free-check.py` | the PIN-FREE checker (token families mirror `.ufo/gates/c1-census-v10.py:239-242`; `--units` also replays the census `units()`/`REA_GATE` reach) |
| `claims/cross/CN-2/assemble-merge.py` | the fold script (extracts each chain's literal block; reproducible) |
| `claims/cross/CN-2/receipts/*` | measurement receipts (see §10) |

## 1. Package inventory — what the parent lands, where

| # | File | Action | Source material | Status at v1.4 |
|---|---|---|---|---|
| R1 | `LOG.md` | append one `### arc3-loop1-round3 …` entry at EOF (after `:1455`) | `claims/cross/CN-2/merged-LOG-entry.md` literal block (v7 fold) | **ready-to-paste** (`[[FILL]]`s: 5 in the body — delivery count, C1 landing identity, C2 post-landing identity, custody post-pair, C3 verifier confirmations) |
| R2 | `SCORECARD.md` | append one `## arc3-loop1-round3 …` section at EOF (after `:1496`) | `claims/cross/CN-2/merged-SCORECARD-section.md` literal block (v7 fold) | **ready-to-paste**; **projection-tested PASS** (v7); `[[FILL]]`s: 15 in the body |
| R3 | `.ufo/reports/arc3-loop1-round3/kaidoku.md` | new file (`claims-frozen.md:99` names this path) | §5 skeleton | skeleton |
| R4 | `.ufo/waves/arc3-loop1-round3/` (seats/ + claims/) | wave-artifacts commit content | all seats | in progress (61/64 seat reports at v1.4 close per VZ-4 census; undelivered: EX-14, SC-3, VZ-4) |
| R5 | `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md` + `corpus/README.md` (EVM row, line-neutral) | C1's work — **drafts**: entry `claims/c1/records-drafts/knowledge-entry-draft.md` (rev 3), token `claims/c1/records-drafts/map-token-patch.md` (PRIMARY now additive-only per the c1 verdict's debt #2; honest-stop variant retained) | C1 chain artifacts | **not landed** (`corpus/README.md` at HEAD `6ac43e83…`, unchanged; entry file absent); landing rehearsal re-derived by this seat at v1.4: 83/83, 14/14, prior-82 byte-identical |
| R6 | `.ufo/gates/custody-pair/custody-pair.py` + `README.md` + `SKILL.md` registry row | C2's work — tool **landed in worktree** (`7cd19c3c…`, 1155 L, +290/−24 vs HEAD `112d01dc…`; selftest CLEAN **22/22** — this seat re-ran it at v1.4); README **landed in worktree** (`f30df42e…`, 185 L — advanced from the v1.3-quoted `039993ed…`; both tool and README re-hashed at v1.4); SKILL.md row is **patch text only** (`claims/c2/EX-30/registry-row.patch.md` v2 + `readme.patch.md`; 390→390 one-line edit; patched SKILL.md `03832723…` re-derived by applying the diff to HEAD at v1.4; projection PASS, §6.2) | C2 (EX-21 target + EX-30 patch texts + SC-3/SC-4 records) | tool + README uncommitted; SKILL.md clean at HEAD `c134afcb…` |
| R7 | `.ufo/gates/citation-drift/pointer-table.json` + `expected.json` | C3's work — **landed in worktree**: table `bfc42f1b…`, **57 entries** (+26), quoted 4, exempt 8; expected `d97dd60a…` re-pinning the table digest (F3 coupling MATCH, this seat verified at v1.4); probe findings=0 both modes + selftest 13/13 (this seat re-ran at v1.4). **Landing-order coupling (§6.5): with C2's row patch applied, the landed pair reads findings=1 (`citation_dead`, `skill-registry-custody-pair-row`) — EX-32's re-anchor (table `a810bd17…`, expected `e33f0e2d…`, both re-derived here) must land in the same commit** | C3 (EX-41 target + SC-5 records) | uncommitted |
| R8 | `.ufo/gates/c1-census-v10.py`, `.ufo/gates/citation-drift/citation-drift-probe.py` | **unchanged this round** | — | clean: census `d0772ce8…` (610 L), probe `e2665074…` (499 L) — re-hashed at v1.4 |

Records package = R1+R2+R3 (+R4 artifacts commit). R5–R7 are **work**.

## 2. Commit sequence and gates (arc2-r8/r10 + arc3-r1/r2 precedent)

1. **Work commit(s)** — C1 (R5: entry + token), C2 (R6: tool + README + the
   SKILL.md row — the row MUST land in the same commit as the tool revision,
   the claim's coupled-landing clause), C3 (R7: table + expected re-pin in the
   same commit; **AND — new at v1.4 — the EX-32 re-anchor of
   `skill-registry-custody-pair-row` with its digest re-pin, because the landed
   table reads findings=1 against the patched row (§6.5); the re-anchor is
   compatible with both pre- and post-row landing orders by construction**).
   Exclude `__pycache__/` from `.ufo/gates/` (three residue dirs currently
   present).
2. **Gate re-runs post-work-commit** (gates grade a settled tree): command A
   (expected 83/83, 14/14, 10.0/10.0 after C1's append), probe selftest +
   findings both modes, census PASS 0/0/0/0, custody selftest (landed count 22
   at the current revision — re-quote at landing).
3. **Wave-artifacts commit** — `.ufo/waves/arc3-loop1-round3/`.
4. **Records commit** — R1+R2+R3; **PIN-FREE preflight first** (§8 recipe),
   then re-run the full gate set and quote it verbatim in R2/R3.

## 3. LOG.md entry skeleton

Ready-to-paste: **`claims/cross/CN-2/merged-LOG-entry.md`** (body 194 lines,
v7 fold): title → dispatch bullet (64 seats, token-plan key 1 of 3, delivery
`[[FILL]]`) → C1/C2/C3 bullets (chains' own text) → custody bullet → scope
bullet. C1/C2/C3 bullets are their scribes' latest revisions spliced verbatim.
Remaining `[[FILL]]`s (5) are the post-landing values (delivery count; C2
post-landing identity; custody post-pair; C1 landing identity; C3 verifier
confirmations).

## 4. SCORECARD.md round-section skeleton

Ready-to-paste: **`claims/cross/CN-2/merged-SCORECARD-section.md`** (body 200
lines, v7 fold): title → single opener (3/10, token-plan key 1 of 3, three-way
tie + tie-break, causal separability, mechanical roster enumeration) → wave
bullet → C1 coverage bullet (K/K across four carriers; entry + line-neutral
token; command A 82→83 rehearsal, parent re-measures) → C2 operability bullet
(before-state reproduced by the scribe; post-fix `[[FILL]]`s pending the
settled tool revision) → C3 freshness bullet (**filled from the landed
table**: 31 → 57, exemptions 3 → 8 with causes, digest re-pin `738b3a56…` →
`bfc42f1b…`, findings=0, selftest 13/13, drift-injection teeth) →
measured-at bullet → verdict table (5 rows: `coverage—C1`, `operability—C2`,
`freshness—C3`, `depth`, `calibration`) → learning trends (three chains'
sentences) → planned → carried debt (C1's Unknowns + C2's D1/D4/D5/D7 + C3
`[[FILL]]` + standing hazards) → retired. `[[FILL]]`s in the body: 15.

## 5. Round-report skeleton — `.ufo/reports/arc3-loop1-round3/kaidoku.md`

```markdown
# kaidoku arc3-loop1-round3 — coverage (EVM optimizer shapes) / operability (custody-pair hardening) / freshness (citation-drift arc3 coverage)

Date: 2026-10-19. Wave: 64 seats on `alibaba-token-plan/deepseek-v4.1-flash`,
roster frozen pre-dispatch (mechanically enumerated); ⟨N⟩/64 delivered. Work
commits: ⟨…⟩. Wave artifacts: ⟨…⟩.

**Round admitted: ⟨…⟩**

## Work performed
1. **C1 — coverage** (owned): ⟨FILL: entry + token landing; K/K across the four
   carriers; command A 82→83 at the records commit⟩.
2. **C2 — operability**: ⟨FILL: the four holes' declared classes at the landed
   revision; selftest count; registry row in the same commit; live pair⟩.
3. **C3 — freshness**: table 31 → 57 entries with causes; digest re-pin in the
   same commit; findings=0 both modes; selftest 13/13. **Landing-order
   coupling (CN-2 §6.5): the table's `skill-registry-custody-pair-row` anchor
   must be re-anchored (EX-32 patch) in the same commit as C2's row, or the
   probe reads findings=1 — measured in both worlds.**

## Landed changes
⟨per-file bullets with commits; include the SKILL.md row + README same-commit
  + the EX-32 re-anchor + digest re-pin same-commit⟩

## Before → after measurements
⟨C1: 82→83; C2: injections as declared classes (14 UNEVALUABLE, coverage 2,
write guard 2, scratch 2), selftest 15→22; C3: 31→57 entries, coupling MATCH;
side-harm: command A + probe + census + custody at the records commit⟩

## SHONEN — ⟨per SHONEN.md⟩

## Verdicts
⟨coverage/operability/freshness improved; depth/calibration unchanged; arc3
loop 1 round 3 of 10⟩
```

## 6. Cross-chain consistency contract (the reconciliation core)

### 6.1 Single-source numbers (must agree across R1/R2/R3)

| Number | Value | Source of truth | Measured by CN-2? |
|---|---|---|---|
| knowledge files / mapped | 82/82 → **83/83 at landing** (rehearsal 83/83 on a scratch tree, re-derived at v1.4) | command A | baseline 82/82 verified at HEAD `c07af80`; landing value `[[FILL]]`; rehearsal 83/83 + prior-82 byte-identical re-run at v1.4 |
| craft rules | 14, 14/14 (unchanged this round) | command A | baseline 14/14 |
| coverage/depth scores | 10.0 / 10.0 | command A | baseline (denominator moves at landing) |
| probe selftest | 13/13 exit 0 | probe `--selftest` | **yes** — at t0, at the landed table, and at the v1.4 re-check (`receipts/c3-landed-verification.txt`) |
| probe findings | 0 both modes (landed pair at HEAD) — **1 finding (`citation_dead`) once C2's row patch is applied; 0 again with EX-32's re-anchor (§6.5)** | probe normal + `--strict` | **yes** — all three states measured at v1.4 |
| probe table | 31 → **57** entries; quoted 4; exempt 3 → 8 | table census | **yes** — landed state |
| F3 coupling | expected pin `bfc42f1b…` == table sha `bfc42f1b…`; expected file `d97dd60a…`; frozen-run revision/verdict/case table byte-unchanged | digest recompute | **yes** — MATCH; EX-32 re-anchor pair re-derived: table `a810bd17…`, expected `e33f0e2d…` |
| census verdict | PASS 0/0/0/0 (instrument `d0772ce8…`) | census run | **yes** — t0, v4 projection, v7 projection, and the full work-commit projection |
| records text | pin-free; projection PASS; control FAIL undeclared=1 | checker + projection | **yes** — v4 and v7 receipts |
| custody selftest | 15 → **22** (floor ≥17 met) | tool selftest | **yes** — at the in-window revision (v1.4 re-run: CLEAN 22/22) |
| custody before/after | 6 injections: fail-open MATCH / traceback / clobber / coverage-blind (HEAD `112d01dc…`) → `14 UNEVALUABLE` / `2 USAGE` declared classes (in-window revision) | scratch reproduction | **yes** — `receipts/c2-before-after-repro.txt` (fixtures only, no custody path touched) |
| custody pre-pair | 5/5 exit 0, receipt sha `d31ece6f…` = sidecar, 13:06:57Z, verifies MATCH 5/5 vs live; mut-copy control CONTENT-DRIFT exit 10; round-2-vs-r3 4/5 (path 3, operator-side churn) | C2 receipts (+ CU-1) | quoted from landed C2 artifacts; v1.4: pre-pair re-verified live `MATCH 5/5 exit 0` |
| custody post-pair | `config-post-pair-v2r3.txt` sha `4969133b…` = sidecar, captured 13:17:23Z by the revised tool `7cd19c3c…`; verifies MATCH 5/5 vs live; pre-vs-post pair MATCH 5/5 (`--require-paths 5`) | C2 receipts | **yes** — all three verifications re-run at v1.4 |
| seats | 64 declared == items; [[FILL: N]]/64 delivered | roster reconciliation (VZ-4) | v1.4 census at close: 61/64 delivered (undelivered: EX-14, SC-3, VZ-4); CN-2's report landed with this revision |

### 6.2 Line-shift couplings

- **R1/R2 append at EOF** — no line shifts. Probe pins sit at `SCORECARD.md:59,
  60,68,69,72,270,622,699` and `PROVINCE.md:18`; the table's `SKILL.md` entry is
  kind `anchor` (content match). **Verified at the landed 57-entry table**: the
  probe reads findings=0 with the round's new entries in place.
- **R6's SKILL.md registry-row edit** (patch text, 390→390): projected in
  place over a scratch copy **with the merged section appended** → census
  PASS (`receipts/skill-row-projection-v7.txt`, re-run at v1.4); the row
  carries no locus tokens; EX-30's own §7 simulation agrees (probe + census in
  a scratch clone). The patched SKILL.md re-derived at v1.4 by applying the
  v2 diff to HEAD: `03832723…` (390 L), matching EX-30's claim. The row MUST
  land in the same commit as the tool (its verdict map would otherwise
  describe a superseded revision — the rule-#14 class) **and, per §6.5, the
  table re-anchor must land with it**.

### 6.3 Digest / identity couplings

- **C3's F3 coupling** — verified MATCH at the landed pair (§6.1). Any further
  table edit without a same-commit re-pin is a broken pair (probe preflight
  `pointer_table_tampered` exit 2 by design).
- **Rule #14** — applies to: C1's entry identity + README, C2's tool sha (the
  head line every receipt self-pins), README sha, R1/R2 texts. This seat
  re-derives its own at close (`receipts/identity.txt`).
- **Custody quoting** — epochs/UTC renders/inode/ctime_ns field names; never a
  client-config path line. (The tool's own `REFERENCE-COVERAGE` line prints the
  five path strings when `--require-paths` fires — a receipt artifact, not
  records text: do not paste that line into R1/R2.)

### 6.4 PIN-FREE contract (measured gate, this seat's core test)

**Rule:** the appended R1/R2 text (and any SKILL.md text C2 lands) must contain
**zero** census-locus tokens — no `rea-agents@x.y.z`, no bare `6.x.y`, no
`~`/absolute `path.ext:NNN` — in any unit the census's gate vocabulary can
reach. Everything past the declared scope is UNDECLARED → FAIL exit 1 even when
factually true. Escape hatches that are NOT repairs: an inline `historical`
marker; a new DATED row wrapping the section (the refused tail-expansion).

Measured by this seat at HEAD `c07af80` (scratch `/dev/shm/cn2r3-preflight`;
instrument `d0772ce8…`, re-hashed at each run; v7 rows are the v1.4
re-measurements):

| Test | Appended text | Result |
|---|---|---|
| baseline projection (no append) | — | PASS 0/0/0/0 exit 0 |
| **v4 merged section + LOG entry** (superseded fold) | bodies 182 + 156 lines | PASS 0/0/0/0 exit 0 (`receipts/merged-projection.txt`) |
| **v7 merged section + LOG entry** (current) | bodies 200 + 194 lines | **PASS 0/0/0/0 exit 0** (`receipts/merged-projection-v7.txt`); G2 floors unchanged (PROVINCE 17 / SCORECARD 14 / SKILL 3) |
| PIN-FREE checker on both v7 bodies (`--units`) | — | CLEAN, 0 pin/version/pointer tokens; 1 census-reachable unit in the section (classifies clean), 0 in the entry (`receipts/pin-free-merged-v7.txt`) |
| control — same projection + 1 planted pin | +1 line | **FAIL undeclared=1 exit 1** (`receipts/merged-injection-control-v7.txt`) |
| SKILL.md row patch in place + v7 section appended | 1 replaced line | PASS 0/0/0/0 (`receipts/skill-row-projection-v7.txt`) |

The chains' own §3 simulations agree (C2's file and C3's file each report zero
added loci with planted-pin controls failing); this seat re-measured both
journals with the real instrument on the merged text.

### 6.5 Landing-order collision: C2's row edit vs C3's table anchor (measured at v1.4)

**The coupling.** C2's required SKILL.md registry-row rewrite changes the
custody-pair row's precedence clause to include the new `UNEVALUABLE` class.
C3's landed table anchors `skill-registry-custody-pair-row` on the round-2
clause verbatim (`precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT >
METADATA-DRIFT > MATCH`). At the coupled landing the probe reads **findings=1**
(`citation_dead`) — the C3 claim's own failure mode (`findings=0 both modes at
the work commit`). Measured by this seat, not quoted:

| state | how measured | result |
|---|---|---|
| patched SKILL.md (`03832723…`, EX-30 v2 diff applied at v1.4) + landed pair `bfc42f1b…`/`d97dd60a…`, scratch clone rev `a13940f7` | **real probe** `--strict` | `citation_dead entry=skill-registry-custody-pair-row` — **failed findings=1 exit=1** (`receipts/collision-probe-patched.txt`) |
| same pair over HEAD (unpatched) | real probe `--strict` | clean findings=0 exit=0 (control — the finding is caused by the row landing, not the table) |
| full work-commit projection (C1 entry+token, C2 tool+README+row, C3 pair, section appended; scratch clone rev `da8ed548`) | real probe `--strict` | failed findings=1 exit=1 — same single entry |
| same projection + **EX-32's re-anchor** (scratch clone rev `32e6aa18`) | real probe `--strict` | **clean findings=0 exit=0** |

**The repair — EX-32's re-anchor, independently re-derived here.** EX-32
(`claims/c2/EX-32/pointer-table-reanchor.patch.md`) filed a one-entry patch
making the anchor an alternation —
`precedence CONTENT-DRIFT > (UNEVALUABLE > )?ABSENT > REWRITE-DRIFT >
METADATA-DRIFT > MATCH` — which holds in both worlds (round-2 row and revised
row). This seat re-derived its artifacts byte-exactly: applying the diff to the
landed table reproduces EX-32's claimed `a810bd17…`; replacing the digest in
`expected.json` reproduces their claimed `e33f0e2d…` (the expected file's only
byte change is the 64-hex digest, verified by character diff). Teeth: a
reordered-precedence mutant still reddens under the alternation (`failed
findings=1`, scratch rev `a1b0efab`), so the fix does not neuter the entry.
EX-32's §3 tightened variant (`… MATCH(;|\||$)` tail anchor) closes the
inherited substring laxity (a `MATCH > UNEVALUABLE;` tail passes §2, fails §3)
— offered as a design option; the parent applies §2 **or** §3, never both, and
either way the digest re-pin must land in the same commit (the F3 coupling).
Caveat re-derived at v1.4: EX-32's §4 cites the patched SKILL.md as `8efd8a87…`
— that is EX-30's **v1** emission; the current v2 patch applies to `03832723…`
and carries the identical precedence clause, so the re-anchor's correctness is
unaffected (this seat's collision runs used `03832723…` directly).

**The pre-registered acceptance test stands either way**: probe findings=0 in
both modes at the work commit. CN-1 pre-registered the same prediction
independently (`claims/cross/CN-1/consistency.md` §3g); this seat's measurement
is the confirmation, and the scratch clones above are the free reproduction.

## 7. Merge-slot map (chain drafts → package slots)

| Slot | Needs | From | Status |
|---|---|---|---|
| ⟨C1⟩ bullets + row + trend | R1 C1 bullet, R2 coverage bullet + verdict row, R3 §Work | `claims/c1/records-drafts/{records-drafts.md,knowledge-entry-draft.md,map-token-patch.md}` | **FOLDED** (SC-2's text verbatim); landing identity + records-commit count stay `[[FILL]]` |
| ⟨C2⟩ bullets + row + trend | R1 C2 bullet, R2 operability bullet + verdict row, R3 §Work | `claims/c2/records-drafts/{LOG-entry-draft.md,scorecard-section-draft.md}` | **FOLDED** (v7 fold: SC-4's 13:28Z revision); post-fix values `[[FILL]]` until the tool revision settles at landing |
| ⟨C3⟩ bullets + row + trend | R1 C3 bullet, R2 freshness bullet + verdict row, R3 §Work | `claims/c3/records-drafts/{log-entry-draft.md,scorecard-section-draft.md}` | **FOLDED** (SC-5 rev 3/4, post-landing values filled by the scribe from EX-41) |
| Delivery count + roster reconciliation | R1 dispatch line, R2 wave bullet, R3 header | `claims/cross/VZ-4/` | v1.4 census at close: 61/64 delivered (undelivered: EX-14, SC-3, VZ-4) |
| Custody times/digests pre+post | R1 custody bullet, R2 custody bullet | CU-1 / C2 tool | **both landed**: pre `d31ece6f…` 13:06:57Z, post `4969133b…` 13:17:23Z, both 5/5 MATCH vs live, pair MATCH 5/5 (v1.4 re-verified); R1's custody bullet `[[FILL]]` remains for the parent's one-voice merge |
| Verdict-table strings + learning-trend sentences | R2 table + trends, R3 §Verdicts | CN-2 (merged texts) | C1/C2/C3 rows + trends folded; `[[FILL]]`s named |
| Collision re-anchor (§6.5) | C3's table entry + expected re-pin | EX-32 patch texts | **verified apply-ready at v1.4** (digests re-derived); must land with the row |

### 7.1 Merge delta + fold timeline — what CN-2 changed vs each chain's draft

Fold sources (literal-block shas at the **v7** fold, 2026-10-19T13:29Z —
current): C1 `records-drafts.md` block 146 lines `36d14342…`; C2 SCORECARD
block 124 L `93b221ca…`; C2 LOG block 112 L `f445a993…`; C3 SCORECARD block
77 L `4ce06e90…`; C3 LOG block 92 L `c32b990e…` (block/segment shas under
`/dev/shm/cn2r3/blocks/`; fold receipt `receipts/v7-fold.txt`; this seat's own
artifact identities in `receipts/identity.txt`).

Fold timeline (each fold re-gated; a chain revision voids the earlier
projection receipt):

| fold | time (UTC) | what changed |
|---|---|---|
| v1 | 13:10 | C2 + C3 drafts folded; C1 absent → named-gap slot |
| v2 | 13:12 | C2 SCORECARD block revised (84 → 107 L) — re-folded |
| v3 | 13:14 | C1 `records-drafts.md` landed → all three chains folded; C2 LOG (72 → 95 L), C3 SCORECARD (67 → 77 L) revised — re-folded |
| v4 | 13:16 | C3 LOG revised (71 → 92 L, post-landing values) — re-folded |
| v5 | 13:17 | C2 SCORECARD (107 → 110 L) and LOG (95 → 97 L) revised — re-folded; superseded |
| v6 | 13:24 | late-join re-fold after the wave-lane quota interruption: C2 LOG block revised (97 → 112 L, `b7c1287a…` → `ba95eba0…` → `f445a993…` across two edits) — re-folded; superseded by v7 |
| v7 | 13:29 | C2 SCORECARD (110 → 124 L `93b221ca…`) and LOG (112 L `f445a993…`) 13:26–13:28Z revisions; fold script's placeholder normalizer extended for the new `⟨PARENT: …⟩` form — **current** |

| Change | Why |
|---|---|
| One title + one opener (round-2 committed shape) replaced the chains' near-duplicate openers | the committed precedent has one opener; the drafts' openers duplicated each other |
| Verdict table normalized to **5 rows** (`coverage—C1`, `operability—C2`, `freshness—C3`, `depth`, `calibration`) | C1's draft proposed a 5-row table with different phrasing, C2's and C3's 4-row tables; the round-2 committed table carries 5 |
| All three chains' bullets spliced **verbatim** (only placeholder convention normalized to `[[FILL: …]]`) | their bullets carry their own measured receipts; paraphrasing would break single-sourcing |
| C1 bullets folded from SC-2's `records-drafts.md` (which landed after v2); the earlier connector-composed C1 slot retired | the chain's own text is the single source once it exists |
| C2's verdict row + learning sentence + D1/D4/D5/D7 debt clauses taken from the SCORECARD draft (outside its literal block) | they are drafted complete there; the row's `⟨…⟩` markers normalized |
| LOG entry: one dispatch + one scope bullet; chains' bullets verbatim; one custody `[[FILL]]` | same field, one voice |
| Connector annotations kept OUT of the literal blocks | only the literal blocks are pasteable; the outline's prose contains an example pin in §8's control recipe |
| `[[FILL]]` count check: merged section 17, merged LOG 13 (from the chains' remaining slots) | the parent's fill pass is bounded and enumerable |

## 8. Pre-flight recipe for the records commit (parent-runnable)

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
R=/dev/shm/cn2r3-preflight; rm -rf $R; mkdir -p $R/root
for f in PROVINCE.md SKILL.md SCORECARD.md; do git show HEAD:$f > $R/root/$f; done
# 0. re-fold after any chain revision (mechanized; prints block/segment shas)
python3 .ufo/waves/arc3-loop1-round3/claims/cross/CN-2/assemble-merge.py
# 1. extract the literal blocks, PIN-FREE check them
python3 - "$R" <<'PY'
import re, pathlib, sys
R = pathlib.Path(sys.argv[1])
for src, dst in [(".ufo/waves/arc3-loop1-round3/claims/cross/CN-2/merged-SCORECARD-section.md", "sec.md"),
                 (".ufo/waves/arc3-loop1-round3/claims/cross/CN-2/merged-LOG-entry.md", "log.md")]:
    txt = pathlib.Path(src).read_text()
    m = re.search(r"<!-- BEGIN LITERAL (?:SECTION|ENTRY) TEXT -->\n(.*?)<!-- END LITERAL (?:SECTION|ENTRY) TEXT -->", txt, re.S)
    (R/dst).write_text(m.group(1))
    print("extracted", src, "->", len(m.group(1).splitlines()), "lines")
PY
python3 .ufo/waves/arc3-loop1-round3/claims/cross/CN-2/pin-free-check.py --units $R/sec.md $R/log.md
# 2. projection census with the section appended (use the LANDED instrument)
printf '\n' >> $R/root/SCORECARD.md && cat $R/sec.md >> $R/root/SCORECARD.md
python3 .ufo/gates/c1-census-v10.py --root $R/root    # expect PASS 0/0/0/0, exit 0
# 3. discrimination control (must FAIL undeclared=1 — proves the test is live)
printf '\nThe probe ran through the npx cache of `rea-agents@6.4.0` on this host.\n' >> $R/root/SCORECARD.md
python3 .ufo/gates/c1-census-v10.py --root $R/root    # expect FAIL undeclared=1, exit 1
# 4. (only if C2's row + C3's table land together) verify the §6.5 coupling in a clone:
#    the landed pair against the patched row reads findings=1; EX-32's re-anchor pair
#    (table a810bd17…, expected e33f0e2d…, re-derived at v1.4) reads findings=0.
#    Reproduce: receipts/collision-probe-patched.txt + receipts/ex32-reanchor-verification.txt
```

The extraction step is inline (equivalent to the scratch helper used at fold
time); angle-bracket names are shell placeholders; the block is paste-safe as
written.

## 9. Named gaps / risks (v1.4)

- **Post-landing `[[FILL]]`s** (15 in the section, 5 in the entry): delivery
  count (VZ-4); C2's post-fix landing values; custody post-pair one-voice
  merge; C1's landing identity + records-commit command A; C3's verifier
  confirmations. An unrun check has not passed — do not fill from the frozen
  claim.
- **C1's work is unlanded** (`corpus/` untouched): command A reads 82/82 at
  HEAD; the 83/83 line is a scratch rehearsal (re-derived at v1.4 with the
  prior-82 slice byte-identical). Land entry + token, then re-measure.
- **The §6.5 collision is OPEN until the re-anchor lands**: with the row patch
  applied and the landed table, the probe reads findings=1. The parent must
  land EX-32's re-anchor (§2 form or the §3 tightened variant, never both)
  with the digest re-pin in the same commit. This is the round's one named
  landing-order coupling.
- **In-window churn**: the custody tool moved through at least twelve observed
  revisions and the gate README through five; my after-repro and selftest
  quotes name the revision they measured (`7cd19c3c…` tool, `f30df42e…`
  README — both re-hashed at v1.4). Re-derive at landing (rule #14). C3's
  table/expected pair is settled at the digests above but any further edit
  voids the coupling check.
- **Chain revisions**: chains revised their literal blocks six times during
  this seat's fold window (§7.1, v1–v7). Re-fold (§8 step 0) after the wave's
  last write; a revised block voids the projection receipt. The fold script's
  normalizer accepts `⟨FILL: …⟩`, `⟨PARENT-FILL: …⟩` and `⟨PARENT: …⟩`; a new
  placeholder form fails loudly (exit 1) rather than splicing raw angle
  brackets.
- **`__pycache__/` residue** under `.ufo/gates/` (three dirs, including
  `citation-drift/` and `custody-pair/`) — exclude from commits.
- Standing hazards: `/tmp` EDQUOT (the EVM recheck form in C1's draft requires
  a disk-backed `TMPDIR` — its own text says so); the pre-existing dirty
  `.ufo/waves/arc2-loop1-round10/C3.md`.

## 10. Receipt index (this seat's measurements)

Under `claims/cross/CN-2/receipts/`:
- `census-t0.txt` — baseline projection PASS at HEAD `c07af80` (instrument `d0772ce8…`).
- `probe-t0.txt` — probe selftest 13/13 + findings=0 both modes at t0.
- `injection-control.txt` — first planted-pin control → FAIL undeclared=1 exit 1.
- `pin-free-merged.txt` / `merged-projection.txt` / `merged-injection-control.txt` / `skill-row-projection.txt` — the v4-fold receipts (superseded by the v7 set below; retained for fold provenance).
- `v6-fold.txt`, `pin-free-merged-v6.txt`, `merged-projection-v6.txt`, `merged-injection-control-v6.txt`, `skill-row-projection-v6.txt` — the v6 fold (late-join first re-fold; superseded by v7).
- `v7-fold.txt`, `pin-free-merged-v7.txt`, `merged-projection-v7.txt`, `merged-injection-control-v7.txt`, `skill-row-projection-v7.txt` — **current fold gates** (section 213 L `83772cc4…`, entry 207 L `6e20b662…`; bodies also staged as `merged-section-body-v7.md`, `merged-log-body-v7.md`).
- `c2-before-repro.txt` — first injection run (hit the already-revised tool; superseded by the pair below).
- `c2-before-after-repro.txt` — independent before/after reproduction of the named holes on scratch fixtures (HEAD revision vs in-window revision).
- `c2-landed-verification.txt` — selftest CLEAN 22/22 at the in-window revision; coverage flag semantics.
- `c3-landed-verification.txt` — table/expected coupling MATCH, 57 entries, probe findings=0 both modes, selftest 13/13.
- `collision-probe-patched.txt` — §6.5: real probe over the patched-row clone (findings=1) + HEAD control (0).
- `ex32-reanchor-verification.txt` — §6.5: EX-32's digests re-derived; landed pair vs re-anchor pair at the full work-commit projection; teeth; tightened-variant discrimination table.
- `identity.txt` — rule-#14 re-derivation of every artifact in this seat's tree (written at close; the only place this seat's own byte-identities appear).
All measurements are read-only over the repo; scratch under `/dev/shm/cn2r3*`
(`/tmp` never used).

## 11. Peer connector cross-reference

CN-1's baseline receipts agree with this seat's t0 readings (census PASS;
command A 82/82, 14/14; probe 13/13 + findings=0). CN-1's §3g pre-registered
the §6.5 collision independently — this seat's probe runs confirm it and the
EX-32 re-anchor repairs it. CU-1 holds the independent pre-capture; VZ-4 holds
the roster reconciliation (v1.4 census at close: 61/64 delivered, this seat's
report landed). [[FILL: at the records commit, reconcile CN-1's consistency
sweep and VZ-4's delivery count against the numbers folded here; a
contradiction is the finding — quote both.]]