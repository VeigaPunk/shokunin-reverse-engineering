# records-outline — arc3-loop1-round2 parent-records package (seat CN-2, cross connector)

Assembled 2026-10-19 by seat CN-2. Status: **v1.1 — all three chains'
records drafts landed and folded; merged pasteable texts written and measured;
C2/C3 revised their literal blocks after the first fold and the updated
bullets are spliced (see §7.1).** Every number below is from a landed in-wave
artifact (cited inline) or a named `[[FILL]]` the parent measures at the
records commit. Method: read the frozen
claims (`claims-frozen.md`), the round-1 committed records (the precedent
shape, `SCORECARD.md:1338-1417` + `LOG.md:1398-1430`), the round-1 connector
package (`.ufo/waves/arc3-loop1-round1/claims/cross/{records-outline.md,consistency.md}`),
the three chains' literal drafts, and the **landed** instruments; then reduce
the three chains' material to one package under an explicit consistency
contract with a measured PIN-FREE gate.

Delivered artifacts of this seat:

| Artifact | What it is |
|---|---|
| `claims/cross/records-outline.md` | this outline |
| `claims/cross/CN-2/merged-SCORECARD-section.md` | merged §R2 pasteable section (spliced from all three chains, re-folded after their revisions; **final body 187 lines sha256 `ce83a08cc92a063e…`; pin-free, projection-tested on the final census revision**) |
| `claims/cross/CN-2/merged-LOG-entry.md` | merged §R1 pasteable LOG entry |
| `claims/cross/CN-2/pin-free-check.py` | the PIN-FREE checker (exit 1 on any locus token) |
| `claims/cross/CN-2/receipts/*` | measurement receipts (see §6.4, §10) |

Sources folded (shas of the chains' literal blocks at fold time —
`claims/{c1,c2,c3}/records-drafts/`):
C1 SCORECARD block 83 lines sha256-prefix `123b1a30…` (unchanged through the
re-fold); C2 SCORECARD block 107 lines `8151360a…` → **re-folded at 143 lines
`990da14a…`**; C3 SCORECARD block 77 lines `654df0d9…` → **re-folded at 140
lines `8a023483…`** (the two chains revised their blocks after the first fold;
§7.1). Extraction scratch: `/dev/shm/cn2/blocks/`; the wave-tree source files
are the citation of record.

---

## 1. Package inventory — what the parent lands, where

| # | File | Action | Source material | Status at v1 |
|---|---|---|---|---|
| R1 | `LOG.md` | append one `### arc3-loop1-round2 …` entry at EOF (after `:1430`) | `claims/cross/CN-2/merged-LOG-entry.md` §literal block | ready-to-paste, [[FILL]]s remain |
| R2 | `SCORECARD.md` | append one `## arc3-loop1-round2 …` section at EOF (after `:1417`) | `claims/cross/CN-2/merged-SCORECARD-section.md` §literal block | ready-to-paste, [[FILL]]s remain; **projection-tested** |
| R3 | `.ufo/reports/arc3-loop1-round2/kaidoku.md` | new file (`claims-frozen.md:82` names this path) | §5 skeleton | skeleton |
| R4 | `.ufo/waves/arc3-loop1-round2/` (seats/ + claims/) | wave-artifacts commit content | all seats | in progress |
| R5 | `SKILL.md` queue-drain craft section | C1's work: insert rule #14 at the craft-section tail (after the natural-control rule) | C1 (SC-1/EX-05/EX-06/EX-07/RV-2; candidate text `claims/c1/EX-05/fallback-rule14-candidate.txt`) | **NOT LANDED** (`git status`: SKILL.md clean) |
| R6 | `.ufo/gates/c1-census-v10.py` | C2's work: EX-16's real-target write (H1 UNREADABLE + H3 BLIND-INSTRUMENT classes) | C2 (EX-11/EX-14/EX-15/EX-16/EX-17/EX-19/EX-21) | **LANDED in worktree, uncommitted**; sha at CN-2 close `a4c16763…`, still churning (history §6.4 W1); behavior stable PASS |
| R7 | `.ufo/gates/custody-pair/` | C3's work: new committed tool (v2 receipt) | C3 (EX-31/EX-32/EX-33/EX-34/EX-35) | **LANDED in worktree, untracked**; `custody-pair.py` sha `112d01dc…`; dir also holds `README.md` and a `__pycache__/` that must be excluded |
| R8 | `.ufo/gates/citation-drift/*` | unchanged this round — probe + table byte-stable (no pins added by R1/R2; LOG carries no pins) | — | clean |

Records package = R1+R2+R3 (+R4 artifacts commit). R5–R7 are **work**.

## 2. Commit sequence and gates (arc2-r8/r10 + arc3-r1 precedent)

1. **Work commit(s)** — C1 (R5), C2 (R6), C3 (R7). R7 creates a new gate dir
   (`custody-pair/`), which must be committed *in the work commit* (a new gate
   file cannot ride the records commit without conflating the classes). Exclude
   `__pycache__/` from both the new dir and `.ufo/gates/`.
2. **Gate re-runs post-work-commit** (gates grade a settled tree — round-1
   caught two mid-write races; this round CN-2 observed the census churn
   through six revisions, §6.4 W1): command A (expected 82/82, 14/14,
   10.0/10.0 after C1's append), probe `--selftest` (13/13 exit 0) + normal
   run (findings=0), census (PASS 0/0/0/0 — ordinary run at HEAD), custody v2
   pair (exit 0, 5/5).
3. **Wave-artifacts commit** — `.ufo/waves/arc3-loop1-round2/`.
4. **Records commit** — R1+R2+R3; **PIN-FREE preflight first** (§8 recipe),
   then re-run the full gate set and quote it verbatim in R2/R3.

## 3. LOG.md entry skeleton

Ready-to-paste merged text: **`claims/cross/CN-2/merged-LOG-entry.md`**
(literal block between the BEGIN/END markers). Structure: title → dispatch
bullet (64 seats, key 2 of 7, delivery [[FILL]]) → C1/C2/C3 bullets → custody
bullet → process notes → carried debt → retired → scope. All chains'
irreplaceable evidence is cited; remaining slots are [[FILL]] with the
producing seat named.

## 4. SCORECARD.md round-section skeleton

Ready-to-paste merged text: **`claims/cross/CN-2/merged-SCORECARD-section.md`**
(literal block between the BEGIN/END markers; 152 lines). Order mirrors the
committed round-1 section: title (round-1 precedent form: `… — depth +
freshness + operability: three claims admitted, 2026-10-19`) → opening
paragraph (window position, lane/key, axis tie + tie-break, freeze history,
causal separability) → wave bullet → one bullet per chain (C1 depth, C2
freshness, C3 operability) → custody bullet → measured-at bullet → process
notes → verdict table (depth—C1, freshness—C2, operability—C3, coverage,
calibration) → learning trends / planned / carried debt / retired.

**The section text must be PIN-FREE (§6.4).** It is: measured CLEAN by the
checker and PASS by the census projection at the settled revision.

## 5. Round-report skeleton — `.ufo/reports/arc3-loop1-round2/kaidoku.md`

```markdown
# kaidoku arc3-loop1-round2 — depth (rule #14) / freshness (census fail-closures) / operability (custody receipt v2)

Date: 2026-10-19. Wave: 64 seats on `opencode-go/deepseek-v4.1-flash`, roster
frozen pre-dispatch (mechanically enumerated); ⟨N⟩/64 delivered. Work commits:
⟨…⟩. Wave artifacts: ⟨…⟩.

**Round admitted: ⟨…⟩**

## Work performed
1. **C1 — depth** (owned): queue-drain rule #14 landed in the craft section;
   [[FILL: rule text pointer, the command-A before/after (13→14), prior-13
   byte-identity, the live catch]].
2. **C2 — freshness**: census fail-closures landed ([[FILL: instrument sha at
   landing, the two closed classes — UNREADABLE, BLIND-INSTRUMENT — the
   before/after matrix, the creep audit, the named residuals]]).
3. **C3 — operability**: custody receipt v2 tool committed ([[FILL: tool shas,
   v2 fields, v1 back-compat, the rewrite attack, the live pair]]).

## Landed changes
⟨per-file bullets with commits; R5–R7; the work-commit classes⟩

## Before → after measurements
⟨C1: 13→14 rules resolved, prev-13 byte-identical; C2: silent-PASS injections
now declared FAILs (UNREADABLE / BLIND-INSTRUMENT), ordinary runs PASS 0/0/0/0;
C3: label defect reproduced before / absent after, same-content rewrite
detected (ctime/inode), v1 sha256 contract 5/5; side-harm check: command A +
probe + census + custody at the records commit⟩

## SHONEN — all four boxes retained [~]
⟨four boxes with SHONEN.md cites; gate `../PROTOCOL.md` (no outside verifier
→ `[~]`)⟩

## Verdicts
⟨depth/freshness/operability improved; coverage/calibration unchanged;
stagnation/regimen line — arc3 loop 1 round 2 of 10⟩
```

## 6. Cross-chain consistency contract (the reconciliation core)

### 6.1 Single-source numbers (must agree across R1/R2/R3)

| Number | Value | Source of truth | Measured by CN-2? |
|---|---|---|---|
| rules | 13 → 14, 14/14 resolved at the work commit | command A | before-state only (13/13, CN-1 + SC-1) |
| knowledge files / mapped | 82 / 82 (no movement expected) | command A | yes (before-state, CN-1 t0 + SC-1) |
| coverage/depth scores | 10.0 / 10.0 (depth denominator moves 13→14) | command A | before-state |
| probe selftest | 13/13 exit 0 | probe `--selftest` | not re-run by CN-2 (CN-1 + SC-3 receipts) |
| probe findings | 0 | probe normal run | not re-run by CN-2 |
| census verdict | PASS 0/0/0/0 at HEAD, settled revision `df9ffdf9…` | census run | **yes** — `receipts/ordinary-head-settled.txt` |
| census injections | absent file → `UNREADABLE` exit 1; zero-locus → `BLIND-INSTRUMENT` exit 1 (before: silent PASS both) | census runs on scratch copies | **yes** — `receipts/census-h1h3-settled-matrix.txt` |
| records text | pin-free; projection PASS; injected unmarked pin → FAIL undeclared=1 | checker + census projection | **yes** — `receipts/merged-section-{projection,injection-control}.txt` |
| custody | 5/5 pre + 5/5 post; v2 receipt; sha256 contract 5/5 vs v1; rewrite detection exit 11 | C3 tool + captures | **yes** (selftest 15/15, capture 5/5, attacks, v1 back-compat) |
| seats | 64 declared == items; ⟨N⟩/64 delivered | roster reconciliation (VZ-4) | no — in progress |

### 6.2 Line-shift couplings

- **R1/R2 are append-only at EOF** — no line shifts inside either file. The
  probe's 31 table entries carry no `LOG.md` pin (verified: entry files =
  PROVINCE/SCORECARD/SKILL/SHONEN/corpus/evidence/wave receipts), and SCORECARD
  pins are ≤ `:699`.
- **R5 (C1) appends inside SKILL.md's craft section** — the registry row moves
  off `:371`. The table's `skill-registry-row` is kind `anchor` (content match,
  no line number) and `shonen-skill-range`/`shonen-province-range` are
  `extracted` SHONEN.md ranges — no pin constrains SKILL.md line numbers. The
  promotion assertion's stated range end + prior count go stale as **prose**
  (needle unaffected; the natural-control rule stays inside the stated range) —
  the C1 chain drafted the refresh as patch text; parent decides.
- **R6/R7** touch `.ufo/gates/` only — outside the probe's entries (none under
  `.ufo/gates/`) and outside the census SCOPE (three scoped files only).
- **Census scope end (`SCORECARD.md:855`)** — R2 appends past `:1417`; the
  appended text is locus-free by §6.4 (the scope re-key alternative stays
  refused: `c1-census-v10.py` header, tail-expansion measurement).

### 6.3 Digest / identity couplings

- **The census's own after-receipts pin `82fb807e…` (12:06:58Z); the settled
  file is `df9ffdf9…`.** Per this round's own rule #14, the parent re-derives
  the landed identity at the records commit — the receipts under
  `claims/c2/EX-16/receipts/after/` cover the revision they measured, not the
  landed one. (Same for the custody tool: `112d01dc…` at CN-2 measurement time,
  and the live pre-pair receipt records tool sha `4862f642…`.)
- **C1's rule-#14 self-application**: the rule text, its patch, and any
  identity claim about SKILL.md's craft section must be re-derived at landing.
- **Custody**: quote the v2 fields (epoch integers + UTC renders + inode +
  ctime), never a client config path; v1 receipts compare on sha256 only.

### 6.4 PIN-FREE contract (measured gate, this seat's core test)

**Rule:** the appended R2 text (and, by the same instrument, C1's appended
SKILL.md rule text) must contain **zero** census-locus tokens — no
`rea-agents@x.y.z`, no bare `6.x.y`, no `~`/absolute `path.ext:NNN` — in any
unit the census's gate vocabulary can reach. Everything past the declared scope
is UNDECLARED → FAIL exit 1 even when the sentence is factually true.

Measured by this seat (HEAD `14b1682b`, projection roots in `/dev/shm`):

| Test | Appended text | before-instrument `6f1d19ff…` | settled instrument `df9ffdf9…` |
|---|---|---|---|
| baseline projection (no append) | — | PASS 0/0/0/0 exit 0 | PASS 0/0/0/0 exit 0 (`receipts/ordinary-head-settled.txt`) |
| v0 skeleton (§4 of this outline, before chain texts) | 50 lines | PASS exit 0 | — |
| **merged chain texts (`merged-SCORECARD-section.md`, 152 lines)** | — | — | **PASS 0/0/0/0 exit 0** (`receipts/merged-section-projection.txt`) |
| injection A — unmarked pin sentence | +2 lines | FAIL undeclared=1 exit 1 | **FAIL undeclared=1 exit 1** (`receipts/merged-section-injection-control.txt`) |
| injection B — bare version in a client clause | +1 line | FAIL undeclared=1 exit 1 | — (same detector family) |
| chains' own drafts (all six files) | — | checker CLEAN 6/6 | checker CLEAN |

The checker (`claims/cross/CN-2/pin-free-check.py`) prints the offending
line/token and exits 1; the preflight recipe is §8. **Escape hatches that are
NOT repairs:** an inline `historical` marker (the instrument's declared escape),
and a new DATED row wrapping the section (the refused tail-expansion creep).

**W1 — instrument churn observed in-window (recorded, resolved).** The census
file moved through at least seven observed revisions while this seat measured:
`6f1d19ff…` (round-1 landed) → `2a89793a…` → `59975ae0…` → `82fb807e…`
(EX-16's own after-receipts, 12:06:58Z) → `762bfebe…` → `c95a5cf3…` →
`df9ffdf9…` → `a4c16763…` (CN-2 close). At `762bfebe…`/`c95a5cf3…` the H3
floor counted current-ok *blocks* per file, and SKILL.md's mixed block (3
current-ok pins + 1 historical bare) read 0 → **the ordinary HEAD run FAILed**
(`SKILL.md=0`, `BLIND-INSTRUMENT`), contradicting the frozen claim's "ordinary
runs at HEAD stay PASS". From `df9ffdf9…` on, the floor counts asserts per file
and passes (`PROVINCE 17 / SCORECARD 14 / SKILL 3`, stable across ≥10 checks 30 s
apart, `/dev/shm/cn2/sha-watch.log`). Consequences for the records:
(i) the after-values must be quoted from the **landed** revision, re-derived at
the records commit; (ii) the churn + the stale after-receipt identity is
itself an instance of the class rule #14 (C1's claim) addresses — a good
learning-trend sentence if the parent wants it; (iii) do not land a revision
that fails the ordinary HEAD run; (iv) the final CN-2 measurements were taken
at `a4c16763…` and the recipient must re-derive (the receipts name the sha
they measured).

## 7. Merge-slot map (chain drafts → package slots)

| Slot | Needs | From | Status |
|---|---|---|---|
| ⟨C1⟩ rule text + command-A before/after + identity evidence | R1 C1 bullet, R2 depth bullet + verdict row, R3 §Work | `claims/c1/records-drafts/{log-entry,scorecard-section}-draft.md` | **LANDED + FOLDED**; the landed rule text + command-A run stay [[FILL]] (R5 not written yet) |
| ⟨C2⟩ instrument sha + closed classes + injection matrix + creep audit | R1 C2 bullet, R2 freshness bullet + verdict row, R3 §Work | `claims/c2/records-drafts/*` | **LANDED + FOLDED**; after-values filled from CN-2's settled-revision measurements; creep-audit output path [[FILL]] |
| ⟨C3⟩ tool shas + v2 fields + label-defect before/after + rewrite attack | R1 C3 bullet, R2 operability bullet + verdict row, R3 §Work | `claims/c3/records-drafts/*` | **LANDED + FOLDED**; CN-2 re-verified independently; post-pair [[FILL]] |
| Delivery count + roster reconciliation | R1 dispatch line, R2 wave bullet, R3 header | `claims/cross/VZ-4/` | **IN PROGRESS** — counted from polling, never from the declared 64 |
| Custody times/digests pre+post | R1 custody bullet, R2 custody bullet | CU-1 / VZ-3 / RV-12 / C3 tool | pre landed; post [[FILL]] |
| Verdict-table strings + learning-trend sentences | R2 table + trends, R3 §Verdicts | CN-2 (merged texts) | drafted; C1 row/verdict stays [[FILL]] until R5 lands |

### 7.1 Merge delta — what CN-2 changed vs each chain's draft

| Change | Why |
|---|---|
| **Re-fold (v1.1): C2 and C3 revised their literal blocks after the first fold; the updated chain bullets are spliced in, and CN-2's connector annotation (churn history) is kept as a bracketed note** | their revised bullets carry their own measured after-values and independent re-runs (agreeing with CN-2's measurements); the stale versions would have shipped draft-time `[[FILL]]`s the chains had since closed |
| One title (round-1 precedent form `… three claims admitted,`) replaced C1's/C3's fill-in titles | the three drafts each carried a variant; the committed precedent fixes the form |
| One opening paragraph (freeze history + causal separability + lane/key) replaced three variants | round-1's committed opener is one paragraph; the drafts' openers duplicated each other |
| Placeholder convention normalized to `[[FILL: …]]` (C1/C3 used `⟨FILL⟩`/`⟨PARENT-FILL⟩`) | one convention for the parent's fill pass |
| C2 bullet: after-values filled from CN-2's settled-revision measurements (UNREADABLE / BLIND-INSTRUMENT + HEAD PASS) and the churn history + W1 recorded | the draft's after-values were `[[FILL]]`; C2's own receipts pin an earlier revision than the settled file |
| C3 bullet: condensed to the section bullet scale; kept the tool-sha caution ("observations, not pins") and the earlier-revision pre-pair note; added CN-2's independent selftest/capture/attack/v1 results | the draft was LOG-scale prose; the section bullet needs the verified numbers with the re-derivation caveat |
| C1 bullet: kept the metric-limit note (decoration also scores 14/14) and the celebration of the live catch as the discriminating evidence | it is the honest reading of the C1 verdict and matches the critic's run |
| Table: 5 rows — `depth—C1`, `freshness—C2`, `operability—C3`, `coverage`, `calibration` (round-1 shape, one row per chain) | the three drafts proposed three different table shapes |
| Learning-trends line: merged the three chains' sentences; added the instrument-churn/discernment note | one sentence per axis, plus the measured process finding |

## 8. Pre-flight recipe for the records commit (parent-runnable)

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
R=/dev/shm/cn2-preflight; rm -rf $R; mkdir -p $R/root
for f in PROVINCE.md SKILL.md SCORECARD.md; do git show HEAD:$f > $R/root/$f; done
# 1. PIN-FREE check on the exact appended text (R2 section; and C1's SKILL.md rule text)
python3 .ufo/waves/arc3-loop1-round2/claims/cross/CN-2/pin-free-check.py <section-text-file>
# 2. projection census with the section appended (use the LANDED instrument)
printf '\n' >> $R/root/SCORECARD.md && cat <section-text-file> >> $R/root/SCORECARD.md
python3 .ufo/gates/c1-census-v10.py --root $R/root    # expect PASS 0/0/0/0, exit 0
# 3. discrimination control (must FAIL undeclared=1 — proves the test is live)
printf '\nThe probe ran through the npx cache of `rea-agents@6.4.0` on this host.\n' >> $R/root/SCORECARD.md
python3 .ufo/gates/c1-census-v10.py --root $R/root    # expect FAIL undeclared=1, exit 1
```

Angle-bracket names are shell placeholders; the block is paste-safe as written.
The same check applies to C1's SKILL.md rule text (the census scans the whole
file; a locus in the craft section is UNDECLARED unless it matches a live
anchor with receipt language).

## 9. Named gaps / risks (v1.1)

- **R5 (C1's rule #14) has not landed** — SKILL.md is clean in `git status`.
  Until it lands, the depth axis's before→after (13→14) and the verdict-table
  row stay [[FILL]], and the records must not assert 14/14 as measured. All
  three candidate rule texts on disk (EX-05's fallback, EX-03's scoped
  proposal, CR-1's candidate set) pass the PIN-FREE checker — the SKILL.md
  append is cleared on the census side once one of them lands.
- **R6 (census) is uncommitted and still churning** (sha at CN-2 close
  `a4c16763…`) — quote and re-derive the landed revision; W1 records the
  transient that failed the ordinary HEAD run (do not land a revision in that
  state).
- **R7 (custody-pair) is untracked** and carries a `__pycache__/` — exclude it
  from the work commit.
- **The census's after-receipts pin `82fb807e…`, not the current revision** —
  a stale self-identity of exactly the rule-#14 class; the parent re-derives at
  landing.
- **Delivery count** from the roster reconciliation only.
- Standing hazards (record, do not absorb): `/tmp` EDQUOT; `.ufo/gates/__pycache__/`
  residue (plus one inside the new gate dir); the pre-existing dirty path
  `.ufo/waves/arc2-loop1-round10/C3.md`.

## 10. Receipt index (this seat's measurements)

Under `claims/cross/CN-2/receipts/`: `census-h1h3-before-after.txt` (first
matrix, before-instrument `6f1d19ff…` vs then-landed), `census-h1h3-settled-matrix.txt`
(before vs `df9ffdf9…`), `ordinary-head-settled.txt`,
`merged-section-projection.txt` (**final 187-line body `ce83a08c…`, census
`d0772ce8…`** — the earlier 180-line run at `a4c16763…` is superseded),
`merged-section-injection-control.txt` (same revision, FAIL undeclared=1).
Checker + merged texts as listed at the top. All measurements are read-only
over the repo; scratch under `/dev/shm/cn2` (`/tmp` never used).

## 11. Peer connector cross-reference (read together with CN-1)

Peer CN-1's sweep `claims/cross/consistency.md` covers the same surface from the
verification side and agrees on the essentials: no contradiction in any shared
reading; the records-commit pre-flight over all three chains' literal sections
shows **0 token hits** and census PASS (§3d there), including a combined
projection with C1's rule-#14 SKILL.md text and the SHONEN refresh — evidence
beyond what this outline could carry (R5 had not landed at CN-2's fold time).
Their flagged items that touch this outline: **F1** revision churn (this
outline's W1 — same finding, independently), **F3** the C1↔census↔SHONEN
same-commit coupling, **F4** v1-receipt verification exits 12 (METADATA-DRIFT)
by design, **F5** naming — say "the round-2 revision of the census instrument",
not a version number (adopted in the merged text's connector note), **F6**
`__pycache__` hygiene (also in §9 here). The parent should treat the two
documents as one handoff: this outline owns the package shape and the merged
text; CN-1's owns the cross-chain agreement matrix and the combined projection.
