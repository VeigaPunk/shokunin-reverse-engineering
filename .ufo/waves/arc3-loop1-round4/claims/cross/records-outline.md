# records-outline — arc3-loop1-round4 parent-records package (seat CN-2, cross connector)

Assembled 2026-10-19 by seat CN-2. Status: **v7 — all three chains' records
drafts are folded (v7 fold: section 180 lines `fa1e2c1a…`, entry 209 lines
`815980b9…`), PIN-FREE CLEAN, projection PASS 0/0/0/0 with a live planted-pin
control (FAIL `undeclared=1`), and the coupled landing (C2 PROVINCE patch + C3
SKILL.md row + records section) projects PASS with probe findings=0 at scratch
commit `4ab031f`.** Every number below was re-derived at v7 write time (rule
#14); the chains were still revising their drafts through the fold window (a
later revision voids the v7 gates — re-fold).

Task (seat line): records reconciliation — merge the chains' records-drafts
into one parent-records outline, PIN-FREE; run the census against a projection
with the drafted sections appended. Artifact: `claims/cross/records-outline.md`
(this file).

Method (r3 precedent): read the frozen claims (`claims-frozen.md`), the round-3
committed records (shape precedent), the three chains' literal drafts as they
landed, and the landed instruments; reduce to one package under an explicit
consistency contract with a measured PIN-FREE gate. The fold is mechanized
(`claims/cross/CN-2/assemble-merge.py`) so a re-fold after any chain revision
is one command plus the §8 gates.

## 1. Package inventory — what the parent lands, where

| # | File | Action | Source material | Status at v7 |
|---|---|---|---|---|
| R1 | `LOG.md` | append one `### arc3-loop1-round4 …` entry at EOF (after `:1487`) | `claims/cross/CN-2/merged-LOG-entry.md` literal block (209 lines) | **ready-to-paste**; `[[FILL]]`s: 8 |
| R2 | `SCORECARD.md` | append one `## arc3-loop1-round4 …` section at EOF (after `:1580`) | `claims/cross/CN-2/merged-SCORECARD-section.md` literal block (180 lines) | **ready-to-paste**; **projection PASS** (§6.4); `[[FILL]]`s: 13 |
| R3 | `.ufo/reports/arc3-loop1-round4/kaidoku.md` | new file (`claims-frozen.md:94` names this path) | §5 skeleton | skeleton |
| R4 | `.ufo/waves/arc3-loop1-round4/` (seats/ + claims/) | wave-artifacts commit content | all seats | in progress (39/48 seat reports at v7 close) |
| R5 | `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md` + `corpus/README.md` (EVM row `:38`, line-neutral) | C1's work — **patch texts**: `claims/c1/records-drafts/{knowledge-entry-draft.md,map-token-patch.md}` | C1 chain artifacts | **not landed**; landing rehearsal re-derived by this seat: 84/84, prior-83 byte-identical, one README line differs (§6.6) |
| R6 | `PROVINCE.md` Frontier/surface repairs | C2's work — **patch texts**: `claims/c2/EX-14/evidence/candidate-complete-frontier-repair.patch.md` (+ VZ-2's census) | C2 chain artifacts | **not landed**; projected in place by this seat: 162 → 162 lines, census PASS (§6.5) |
| R7 | `.ufo/gates/custody-pair/` tool + README (+ SKILL.md registry row) | C3's work — tool+README **landed in worktree** (`29bb45ae…`, 1343 L; README `9d9400da…`, 272 L); SKILL.md row is **patch text** (`claims/c3/EX-21/patch/`) | C3 chain artifacts | tool+README uncommitted; row unapplied (CN-1's F-1; §6.5) |
| R8 | `.ufo/gates/c1-census-v10.py`, `.ufo/gates/citation-drift/*` | **unchanged this round** | — | clean at v7: census `d0772ce8…` (610 L), probe `e2665074…`, table `1b3ab955…`, expected `9df0452c…` |

Records package = R1+R2+R3 (+R4 artifacts commit). R5–R7 are **work**.

## 2. Commit sequence and gates (arc2-r8/r10 + arc3-r1/r2/r3 precedent)

1. **Work commit(s)** — C1 (R5: entry + token), C2 (R6: PROVINCE patch applied
   by the parent — C2's claim is explicit that seats never write PROVINCE),
   C3 (R7: tool + README + the SKILL.md registry row in the same commit, every
   receipt self-pinning the new tool sha256). Exclude `__pycache__/` residue
   (three dirs under `.ufo/gates/`, plus wave-tree `__pycache__` dirs already
   present under `claims/c1/EX-04/evidence/` and `claims/c1/EX-08/`).
2. **Wave-artifacts commit** — the `.ufo/waves/arc3-loop1-round4/` tree.
3. **Records commit** — R1+R2+R3 with the `[[FILL]]`s filled from landed
   artifacts only; the census and the citation probe re-run at the settled tree.

## 3. LOG.md entry skeleton

Ready-to-paste: **`claims/cross/CN-2/merged-LOG-entry.md`** (209 lines, v7 fold):
title → dispatch bullet (48 seats, hyper lane → devin fallback after 402 on all
48 seats, delivery `[[FILL]]`) → C1/C2/C3 bullets (chains' own text) → custody
bullet → scope bullet. LOG.md is not census-scanned, but the entry keeps the
same pin-free voice (one voice across both records).

## 4. SCORECARD.md round-section skeleton

Ready-to-paste: **`claims/cross/CN-2/merged-SCORECARD-section.md`** (180 lines,
v7 fold): title → single opener (4/10, roster 16+14+14+4 = 48 frozen
pre-dispatch, hyper→devin fallback recorded with cause, three-way tie +
most-falsifiable tie-break, causal separability of the three edit targets) →
wave bullet → C1/C2/C3 bullets (spliced verbatim) → measured-at bullet →
verdict table (5 rows: `coverage (owned)—C1`, `freshness (fleet)—C2`,
`operability (fleet)—C3`, `depth`, `calibration`) → learning trends → planned →
carried debt → retired.

**Axis mapping note:** this round **C2 owns freshness** (the PROVINCE staleness
census) and **C3 owns operability** (custody residuals) — the inverse of round
3's mapping. The verdict-table row labels follow the frozen claims, not r3.

## 5. Round-report skeleton — `.ufo/reports/arc3-loop1-round4/kaidoku.md`

```markdown
# kaidoku arc3-loop1-round4 — coverage (Vyper leg) / freshness (PROVINCE census) / operability (custody residuals)

Date: 2026-10-19. Wave: 48 seats declared on `hyper/deepseek-v4.1-flash`;
re-dispatched in full on `devin/deepseek-v4-1-flash-max` after the hyper lane
returned 402 out-of-credits on all 48 seats (the schedule's declared fallback;
recorded with cause). Roster frozen pre-dispatch. ⟨N⟩/48 delivered. Work
commits: ⟨…⟩.

**Round admitted: ⟨…⟩**

## Work performed
1. **C1 — coverage** (owned): ⟨FILL: the Vyper leg — venv receipt (0.4.3, wheel
   sha256 `3b967172…`, four independent derivations), five carriers compiled,
   K/K on every runtime leg, the three measured deltas, the entry + line-neutral
   token, command A 83 → 84 with the prior 83 byte-identical⟩.
2. **C2 — freshness**: ⟨FILL: the PROVINCE staleness census — 7 named stale
   items (one falsified, one false absence claim) → 0; same-line repairs
   (162 → 162); census PASS at the patched tree; the certificate-scope caveat⟩.
3. **C3 — operability**: ⟨FILL: residuals (a)-(d) closed with declared classes;
   selftest 22 → 28; live pair MATCH 5/5; registry row in the same commit⟩.

## Landed changes
⟨per-file bullets with commits; include the SKILL.md row same-commit⟩

## Before → after measurements
⟨per claim; side-harm: command A + probe + census + custody at the records commit⟩

## SHONEN — ⟨per SHONEN.md⟩

## Verdicts
⟨coverage/freshness/operability improved; depth/calibration unchanged; arc3
loop 1 round 4 of 10⟩
```

## 6. Cross-chain consistency contract (the reconciliation core)

### 6.1 Single-source numbers (must agree across R1/R2/R3)

| Number | Value | Source of truth | Measured by CN-2? |
|---|---|---|---|
| knowledge files / mapped | 83/83 at HEAD → **84/84 at landing** | command A | **yes both sides** — HEAD `015e1ba` (`receipts/t0.txt`) and the landing rehearsal (`receipts/c1-landing-rehearsal.txt`) |
| craft rules | 14, 14/14 (unchanged) | command A | **yes** both sides |
| coverage/depth scores | 10.0 / 10.0 | command A | **yes** both sides |
| census verdict | PASS 0/0/0/0 (`d0772ce8…`) | census run | **yes** — HEAD, v1–v7 projections, coupled projection, rehearsal clone |
| probe selftest / findings | 13/13 exit 0; findings=0 both modes at HEAD | probe `--selftest` / normal + `--strict` | **yes** at HEAD; **yes** over the coupled projection (`receipts/coupled-projection.txt`) |
| probe table | 57 entries at HEAD (`1b3ab955…`), expected `9df0452c…` | table census + digest recompute | **yes** (pin == table sha) |
| custody tool / README | HEAD `7cd19c3c…` (1155 L) / `f30df42e…` (185 L); landed revision `29bb45ae…` (1343 L) / `9d9400da…` (272 L) | sha256 + `wc -l` + selftest | **yes** both sides (`receipts/c3-tool-verification.txt`) |
| custody selftest | HEAD 22/22 → landed **28/28** | tool `selftest` | **yes** both sides |
| custody pair | r3 post-pair re-verifies MATCH 5/5 live; round-4 pair (revised tool) MATCH 5/5 with and without the gate | C3 receipts + CN-1 F-4 | **partially** — this seat re-verified the canonical-5 pair against live with the revised tool (`receipts/c3-tool-verification.txt`) |
| seats | 48 declared == items; [[FILL: N]]/48 delivered | roster reconciliation (VZ-4) | 39 seat reports at v7 close |
| records text | pin-free; projection PASS; control FAIL undeclared=1 | checker + projection | **yes** — v1–v7 + coupled (`receipts/`) |

### 6.2 Line-shift couplings

- **R1/R2 append at EOF** — no line shifts for any landed citation. Probe
  findings=0 re-measured over the coupled projection commit (§6.5).
- **C2's PROVINCE repairs must hold the line count** (frozen claim). Measured:
  the EX-14 patch is 162 → 162 and the census reads PASS; CN-1 independently
  measured that a +1 net shift (and even a compensating +1/−1 at held total)
  FAILs at the `PROVINCE.md:119` DATED marker — so **total line count is not
  sufficient; the marker line must stay put**.
- **C3's custody tool revision** — every receipt self-pinning the old digest is
  voided (rule #14 class); the landed receipts self-pin `29bb45ae…`. The
  registry row must land in the same commit (CN-1's F-1; C3's own verdict §R1
  names the same uncovered leg).

### 6.3 Digest / identity couplings

- **Rule #14** — applies to C1's entry identity + README token, C2's patched
  PROVINCE identity, C3's tool + README + every receipt self-pin, R1/R2 texts.
  This seat re-derives its own at close (`receipts/identity.txt`).
- **Custody quoting** — epochs/UTC renders/inode/ctime_ns field names; never a
  client-config path line (a `path.toml:NNN` pointer is a census locus token).

### 6.4 PIN-FREE contract (measured gate, this seat's core test)

**Rule:** the appended R1/R2 text must contain **zero** census-locus tokens —
no `rea-agents@x.y.z`, no bare `6.x.y`, no `~`/absolute `path.ext:NNN` — in
any unit the census's gate vocabulary can reach. Everything past the declared
scope is UNDECLARED → FAIL exit 1 even when factually true.

Measured by this seat (scratch `/var/tmp/cn2r4`; instrument `d0772ce8…`,
re-hashed per run):

| Test | Appended text | Result |
|---|---|---|
| baseline projection (no append) | — | PASS 0/0/0/0 exit 0 (`receipts/t0.txt`) |
| harness smoke — r3 merged section (precedent fixture) | body 200 L | PASS 0/0/0/0 exit 0 (`receipts/harness-smoke.txt`) |
| control — same + 1 planted pin | +1 line | **FAIL undeclared=1 exit 1** (`receipts/harness-smoke-control.txt`) |
| v1 skeleton (chains stubbed) | body 46 L | PASS; control FAIL undeclared=1 (`receipts/v1-skeleton-projection.txt`) |
| v2 (C3 folded) | body 86 L | PASS; control FAIL (`receipts/v2-fold.txt`) |
| v3 (all three folded) | body 145 L | PASS; control FAIL (`receipts/v3-fold.txt`) |
| v4 (rows + trends populated) | body 153 L | PASS; control FAIL; 14+8 `[[FILL]]`s (`receipts/v4-fold.txt`) |
| **v5 (all three folded, rows+trends)** | body 167 L | **PASS 0/0/0/0 exit 0; control FAIL undeclared=1** (`receipts/v5-fold.txt`) |
| **v6 / v7 (final fold)** | body 167 L | **PASS 0/0/0/0 exit 0; control FAIL undeclared=1; PIN-FREE CLEAN** (`receipts/v6-fold.txt`, `receipts/v7-fold.txt`) |
| **coupled landing** (C2 PROVINCE patch + C3 SKILL row + section, scratch clone `4ab031f`) | — | **census PASS 0/0/0/0; probe findings=0 --strict; PROVINCE 162 L; SKILL 390 L** (`receipts/coupled-projection.txt`) |

### 6.5 Landing-order couplings

**No r3-class collision this round — measured, not assumed.** C3's registry-row
patch changes the SKILL.md line that C3's own probe table anchors
(`skill-registry-custody-pair-row`). The r3 precedent (four seats measured a
guaranteed `citation_dead`) made this the round's first candidate collision.
Measured here, twice (scratch clones `0a60120` and `4ab031f`, the second against
the final v7 fold): the coupled projection (row applied + PROVINCE patched +
records appended) reads **probe clean findings=0 exit 0** in `--strict` mode,
with the HEAD control also clean (`receipts/coupled-projection.txt`). CN-1
independently applied the same row on a scratch root and read findings=0. The
collision is **absent because C3 re-anchored the table entry itself** (the
round's own work) — the two chains coordinated; the residual requirement is
only the same-commit landing.

**The one real coupling (CN-1's F-1, independently confirmed here):** the
SKILL.md registry row is **not in the tree** — the row still declares 22 cases
while the landed tool runs 28. No instrument grades the count cell (measured by
CN-1), so the C3 claim's "registry row re-derived same-commit" clause is met
**only if the parent applies C3's patch text in the coupled landing**. This is
a landing requirement, not a chain contradiction: C3's verdict names the same
leg as uncovered, and the patch text is verified sound by two seats.

### 6.6 C1 landing rehearsal (this seat's own, end-to-end)

On a scratch clone of HEAD: entry file (stem `2026-10-19-arc3-r4-evm-vyper-leg`,
18,166 B, sha256 `da42d9a2…`) + README PRIMARY additive token (`:38`, one line
differs, 190 → 190) → command A reads **84/84, missing [], dangling [], 14/14,
10.0/10.0**; prior-83 files **byte-identical 83/83**; added file set = exactly
the one entry. Receipt: `receipts/c1-landing-rehearsal.txt`. CN-1's independent
simulation agrees (84/84, 0 diffs, probe clean), and CN-1 additionally measured
that a **row insert** (instead of the line-neutral token) reddens the probe
with 5 `citation_dead` findings — the line-neutral form is load-bearing.

### 6.7 C2 census independent re-run (this seat's own)

C2's staleness instrument (`claims/c2/VZ-2/evidence/province-staleness-census.py`,
sha256 `e6eef574…`) was copied to scratch and re-run by this seat against the
real (read-only) `PROVINCE.md`: **`SUMMARY: total=26 stale=6 adjudicated=2
current=18`; `STALE: F1b, F3, F5b, X1, C1, R2`** — identical to C2's own
recorded baseline (`VZ-2/evidence/census-before.txt`). Receipt:
`receipts/c2-census-independent.txt`. The merged text's counts agree with this
run (6 → 0; an earlier draft revision read 7 — the chain's own later revision
superseded it, and the fold carries the final number).

## 7. Merge-slot map (chain drafts → package slots)

| Slot | Needs | From | Status |
|---|---|---|---|
| ⟨C1⟩ bullets + row + trend | R1 C1 bullet, R2 coverage bullet + verdict row, R3 §Work | `claims/c1/records-drafts/records-drafts.md` (`1bcf2306…` block) | **FOLDED** |
| ⟨C2⟩ bullets + row + trend | R1 C2 bullet, R2 freshness bullet + verdict row, R3 §Work | `claims/c2/records-drafts/{scorecard-section-draft.md,LOG-entry-draft.md}` | **FOLDED** (v7 fold; the chain revised 4× in the fold window) |
| ⟨C3⟩ bullets + row + trend | R1 C3 bullet, R2 operability bullet + verdict row, R3 §Work | `claims/c3/records-drafts/{scorecard-section-draft.md,LOG-entry-draft.md}` | **FOLDED** |
| Delivery count + roster reconciliation | R1 dispatch line, R2 wave bullet, R3 header | `claims/cross/VZ-4/` | partial — `[[FILL]]` (35/48 seat reports at v7 close) |
| Custody times/digests pre+post | R1 custody bullet, R2 custody bullet | CU-1 / C3 receipts | CU-1's report landed (install-window 5/5 IDENTICAL); round-4 pair `[[FILL]]` |
| Verdict-table strings + learning-trend sentences | R2 table + trends, R3 §Verdicts | CN-2 (merged texts) | C1/C2/C3 rows + trends folded; `[[FILL]]`s named |

## 8. Pre-flight recipe for the records commit (parent-runnable)

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
CN=.ufo/waves/arc3-loop1-round4/claims/cross/CN-2
R=/var/tmp/cn2r4-preflight; rm -rf $R; mkdir -p $R/root
for f in PROVINCE.md SKILL.md SCORECARD.md; do git show HEAD:$f > $R/root/$f; done
# 0. re-fold after any chain revision (mechanized; prints block/segment shas)
CN2_ALLOW_GAPS=1 python3 $CN/assemble-merge.py
# 1. PIN-FREE check both literal bodies
python3 $CN/pin-free-check.py --units $CN/merged-SCORECARD-section.md $CN/merged-LOG-entry.md
# 2. projection census with the section appended (harness extracts the body)
python3 $CN/project.py $R/root $CN/merged-SCORECARD-section.md
#    expect PASS 0/0/0/0 exit 0
# 3. discrimination control (must FAIL undeclared=1 — proves the test is live)
python3 $CN/project.py $R/root $CN/merged-SCORECARD-section.md \
  --inject "The probe ran through the npx cache of \`rea-agents@6.4.0\` on this host."
#    expect FAIL undeclared=1 exit 1
# 4. coupled landing (C2 PROVINCE patch + C3 row) in one command:
python3 $CN/project.py $R/root $CN/merged-SCORECARD-section.md \
  --province-patch .ufo/waves/arc3-loop1-round4/claims/c2/EX-14/evidence/candidate-complete-frontier-repair.patch.md \
  --skill-patch .ufo/waves/arc3-loop1-round4/claims/c3/EX-21/patch/skill-registry-row.patched.md
#    expect PASS; PROVINCE 162 lines; SKILL 390 lines
```

## 9. Named gaps / risks (v7)

- **Chains were still revising through the v7 fold window** (C2's SCORECARD
  block moved four times; C3's twice). A later revision voids the v7 gates —
  re-fold (§8 step 0) and re-run steps 1–3.
- **Post-landing `[[FILL]]`s**: 13 in the section, 8 in the entry. The largest
  are the C2 verdict row + the C3 after-column (the landed revision identity and
  injection transcripts) and the custody pre/post pair. An unrun check has not
  passed — do not fill from the frozen claim.
- **F-1 landing requirement** (§6.5) — the SKILL.md registry row must land with
  the tool or the C3 claim's same-commit clause is unmet.
- **C2's PROVINCE repairs are patch text**: the parent applies them; the round's
  C2 claim is written for that form.
- **`__pycache__/` residue** — `.ufo/gates/` has three dirs; the r4 wave tree
  has two more under `claims/c1/`. Exclude from commits.
- Standing hazards: `/tmp` EDQUOT (all recipes disk-backed scratch); the
  pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md` (not this round's).

## 10. Receipt index (this seat's measurements)

Under `claims/cross/CN-2/receipts/`:
- `t0.txt` — HEAD `015e1ba`: instrument hashes, scoped `wc -l`, census PASS,
  command A 83/83 · 14/14 · 10.0, probe 13/13 + findings=0 both modes, custody
  22/22.
- `census-t0.json` — full census JSON at HEAD.
- `harness-smoke.txt` / `harness-smoke-control.txt` — projection harness
  self-test on the r3 precedent (PASS) and its planted-pin control (FAIL).
- `v1-skeleton-projection.txt` … `v7-fold.txt` — the fold timeline's gates
  (v1 stubbed → v7 all three chains folded at their final revisions).
- `coupled-projection.txt` — the coupled landing on scratch clone commits
  `0a60120` and `4ab031f`: census PASS + probe findings=0 + the identities.
- `c1-landing-rehearsal.txt` — C1's entry+token applied on scratch clone commit
  `6b990397…`: command A 84/84, prior-83 byte-identical, one README line differs.
- `c3-tool-verification.txt` — the landed custody tool `29bb45ae…` re-verified
  first-hand: selftest 28/28, (a)/(b)/(c) as declared classes, canonical-5 pair
  MATCH 5/5.
- `c2-census-independent.txt` — C2's staleness instrument re-run by this seat
  over the read-only PROVINCE.md: `total=26 stale=6 adjudicated=2 current=18`,
  the six rows named.
- `identity.txt` — rule-#14 re-derivation of every artifact in this seat's tree
  (written at close; the only place this seat's own byte-identities appear).

All measurements are read-only over the repo; scratch under `/var/tmp/cn2r4`
(`/tmp` never used). Scratch clones are separate throwaway Git repos.

## 11. Peer connector cross-reference

CN-1's consistency record (`.ufo/waves/arc3-loop1-round4/claims/cross/consistency.md`
+ `seats/CN-1.md`) and this seat's readings **agree on every shared number**:
command A 83/83 · 14/14 at `015e1ba`; census PASS; probe 13/13 + findings=0;
custody selftest 22 → 28; C1's landing 84/84 with prior-83 byte-identical; the
coupled landing clean in both instruments. CN-1's F-1 (registry row unapplied)
is confirmed here and carried as the round's one landing requirement; F-2/F-4
(re-derive README/receipt identities at the records commit) are carried in §9.
VZ-4's roster reconciliation and CU-1's custody captures are the other two
cross seats; at v7 close VZ-4's count was not yet published — [[FILL: reconcile
the delivered count at the records commit; a contradiction is the finding —
quote both]].
