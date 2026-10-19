# VZ-3 — seat report (chain c3, convergence)

Wave `arc3-loop1-round4` · seat VZ-3 · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD `015e1bab914713568f339fd53999bc180459cc40`
(no seat commits; parent integrates) · lane: devin (declared fallback, per the freeze).
Task: poll `seats/` every 60 s (max 25 checks) and reconcile chain c3 into
`claims/c3/verdict.md` — VERIFIED or NOT-VERIFIED + evidence + named debt.
Seat report last, as the seat line requires.

## 1. Work performed (evidence pointers)

All writes are inside this seat's two authorized locations. Scratch is
`/var/tmp/vz3` (`/tmp` never used). Custody paths and the gate pair were
read-only (hash/stat/`git show`/read-only tool runs) except the two sanctioned
scratch copies below; no git mutations.

| # | work | evidence |
|---|---|---|
| 1 | Read the freeze (`claims-frozen.md`), `AGENTS.md`, the r3 verdicts, the r3 c2 residual patch texts (EX-24, CR-3, CR-4, RV-8), SCORECARD's command-A recipe, the custody README | cited throughout `claims/c3/verdict.md` |
| 2 | **Poller** (seat line): 60 s cadence, `/var/tmp/vz3/poll-log.txt`; 10 of 25 checks used before the landing arrived, 25-check cap respected | `/var/tmp/vz3/poll-log.txt` (seat/claims counts per check) |
| 3 | **Target watcher**: 20 s cadence on the two real targets + `seats/` count — caught the landing transition at 14:09:26Z | `/var/tmp/vz3/target-watch.txt` |
| 4 | **Own before-state harness** (`battery.sh`): all four residuals reproduced on a scratch copy of `7cd19c3c…`; selftest 22/22; live pair 5/5 | `/var/tmp/vz3/before/battery-before.out` |
| 5 | **Own after-state harness** (`after-state.sh`): the four declared-class probes + selftest + live pair on the landed `29bb45ae…` | `/var/tmp/vz3/landed/after-landed.out` |
| 6 | **Sidecar-spelling harness** (`sidecar-both.sh`): spellings A/B/B2 plus the v1 sums/pipe duplicate shapes and the distinct-path control — run on the base, on RV-7's DRESS, on EX-23's variant, on EX-24's `after2`, and on the landed tool | `/var/tmp/vz3/sb-*/` |
| 7 | **Own three targeted mutants of the landed tool** (one per fix) — the sabotage arms | `/var/tmp/vz3/mut2/`, transcripts in `vz3-reconciliation.txt` §11 |
| 8 | Independent re-runs of peers' instruments: EX-23's sidecar probe, EX-24's `after2`/`sabotage2` selftests, EX-26's ruling block, EX-27's `readme_ruling()` regexes, RV-7's mutant builder | `vz3-reconciliation.txt` §4, §6, §7 |
| 9 | Landing-identity discipline: five README digests observed across the landing window; the settled value re-derived after the last edit; every README-side check re-run on it | `vz3-reconciliation.txt` §9, §17 |
| 10 | Verification of EX-21's SKILL registry-row patch text (apply on scratch, line-neutrality, row digests, content clauses, anchor survival) | `vz3-reconciliation.txt` §18 |
| 11 | No-harm instruments at HEAD and after the landing (command A, citation-drift probe both modes + selftest, c1 census, anchor grading with `re.M`) | `/var/tmp/vz3/noHarm/{baseline,landed}.txt` |
| 12 | Backward-compat legs (r3 receipts vs the landed tool; v1 shapes) | `vz3-reconciliation.txt` §15 |
| 13 | EX-25's R4 re-measured first-hand (five hardlink names / one inode vs the distinct-path gate) | `/var/tmp/vz3/r4check/` |
| 14 | **The reconciliation deliverable**: `claims/c3/verdict.md` (VERIFIED on the measured legs, one open leg, seven named residuals) | `claims/c3/verdict.md` |

**Artifacts written by this seat**

- `claims/c3/verdict.md` — sha256 `3d82bbcbba21fbca800c48ba526057bd0a8bb70ed54015807f662b92672e892a`, 210 lines (re-derived after the last append).
- `claims/c3/VZ-3/vz3-reconciliation.txt` — sha256 `b98f30b3d1f35c0efc463eee60899bd9bbac25846888f6808af216d83d968f68`, 217 lines, sections 1-19 (raw first-hand captures; the section-17/18 appends landed after the earlier digest, which is why this file's identity is quoted from the final state only).
- This report.

Nothing else was written: no corpus/, SKILL.md, PROVINCE.md, README, LOG.md,
SCORECARD.md, SHONEN.md, no gate file, no seat's claim dir.

## 2. Proposed changes

**None.** This seat is convergent: it measures, reconciles and names debt. The
landed changes belong to EX-21 (the designated C3 writer, which landed the gate
pair) and the pending SKILL row is EX-21's patch text for the parent to apply.

The verdict's closing procedure (`claims/c3/verdict.md` §7) is this seat's
actionable proposal to the parent: apply EX-21's row patch in the same commit as
the gate pair, re-run the probe + census + identity re-derivation after that
commit, and do not quote three specific values the reconciliation falsified
(EX-21's `(d)` `ABSENT 13` label, EX-26's 214-line claim, an all-absent
`MATCH 5/5` as a content witness).

## 3. Before → after measurement for the chain's claim

Frozen claim (`claims-frozen.md:59-77`): "(a)-(c) closed with declared classes
(selftest 22 → ≥24 with the new fixtures; sabotage arms), (d) adjudicated with the
ruling text landed in the README; the registry row + README re-derived
same-commit; the round's live pair (revised tool) verifies MATCH 5/5; every
receipt self-pins the new tool sha256; command A unchanged."

| claim element | before `7cd19c3c…` | after `29bb45ae…` | verdict |
|---|---|---|---|
| (a) spelling A `--out X --paths X.sha256` | exit 0, measured `X.sha256` destroyed | **exit 2**, sha unchanged | CLOSED |
| (a) spelling B `--out X.sha256 --paths X` | exit 0, neighbour + second sidecar created | **exit 2**, neither created | CLOSED |
| (a) spelling B2 (neighbour pre-exists) | exit 0, bystander overwritten | **exit 2**, bystander unchanged | CLOSED |
| (b) `--out <regular-file>/sub/r.txt` | raw traceback, exit 1 | **exit 2**, declared USAGE | CLOSED |
| (c) 5 duplicate stanzas `--require-paths 5` | exit 0, `MATCH 1/1`, 0 coverage lines | **exit 2**, `REFERENCE-COVERAGE: 1/5` | CLOSED |
| (c) v1 sums / v1 pipe duplicate shapes | sums exit 0 (silent) | **both exit 2** | CLOSED |
| (c) 5 distinct paths (control) | exit 0 `MATCH 5/5` | exit 0 `MATCH 5/5` | unchanged (no harm) |
| (d) README ruling (EX-27's own detector) | 0 hits | **10 hits** | adjudicated + landed |
| selftest | `CLEAN cases=22` | **`CLEAN cases=28`** (prior 22 names retained) | 22 → 28 (claim floor ≥24) |
| sabotage arms | — | 3 mutants: DIRTY 26/28, 27/28, 27/28, each reddening exactly its own cases | load-bearing |
| live pair (revised tool) | — | `MATCH 5/5 exit 0` plain and `--require-paths 5`; post vs live `MATCH 5/5` | VERIFIED |
| receipt self-pin | — | both receipts `# tool: … 29bb45ae…`; sidecars `sha256sum -c` OK | VERIFIED |
| command A | 83/83, 14/14, 10.0/10.0 | 83/83, 14/14, 10.0/10.0 | unchanged |
| **registry row** | `5eec51c0…`, "22 fixture cases" | **still unchanged** — EX-21's patch text verified sound but unapplied | **OPEN (the claim's one unmet leg)** |

**Reconciliation verdict: VERIFIED on every leg measurable on the landed bytes,
with one open leg** — the SKILL.md registry row is not in the tree. It is not a
defect in the landing: EX-21's patch text for it is verified line-neutral and
content-correct by this seat (§18 of the reconciliation capture), so the leg is
unmet only by non-application, and the parent closes it by applying the patch in
the same commit as the gate pair.

## 4. Attacks/refutations attempted, with verdicts

(Full table with evidence in `claims/c3/verdict.md` §6; the load-bearing ones.)

- **"the landing is a half-fix (spelling A only)"** — the risk SC-3 named and
  both RV-7's DRESS and EX-23's variant exhibit. **REFUTED on the landed bytes**:
  all three spellings exit 2 with victims byte-unchanged.
- **"the new selftest cases are decorative"** — **REFUTED**: my three targeted
  mutants each redden exactly their own cases (2/1/1 FAILs) and nothing else.
- **"the (b) fix regresses `--out ''` or a fresh parent"** — **REFUTED** (both
  stay in the declared classes).
- **"the (c) fix breaks the legitimate distinct-path reference"** — **REFUTED**
  (5 distinct still `MATCH 5/5`).
- **"the landing breaks the r3 receipts or v1 shapes"** — **REFUTED** (three
  cross-revision verifies `MATCH 5/5`; v1 classes unchanged).
- **"EX-26's ruling text does not reproduce / is a decoration"** — **REFUTED**
  (its block reproduces its claimed digest exactly and moves the wave's own
  detector 0 → 6; the landed README reads 10).
- **"EX-21's transcripts are narrative"** — **PARTIALLY SUSTAINED**: its
  (a)/(b)/(c) legs reproduce on my runs, but its **`(d)` leg is mislabeled** (it
  deletes the fixture between captures, so it measures one-side-absent and reads
  `ABSENT 13`; the true shape reads `MATCH 0`). Named as §R2.
- **"EX-21's registry-row patch is stale like EX-24's"** — **REFUTED**: exactly
  one line changes (390 → 390), both row digests reproduce, content is
  revision-pinned to the landed tool, three graded SKILL anchors stay alive.
- **"the distinct-path gate is a strong close"** (EX-25's R4) — **PARTIALLY
  SUSTAINED**: five hardlink names for one inode pass the gate and read
  `MATCH 5/5 exit 0` (my own probe). Unit-scope limit, outside the claim's
  letter; named as §R5.
- **"EX-26's patched line count is right"** — **REFUTED**: 215 lines, not 214
  (its digest is right). Named as §R3.
- **"the (c)+(d) compound case is closed by the landing"** — **REFUTED**: a
  five-cleanly-absent reference still passes the gate and reads `MATCH 5/5`; the
  ruling declares it non-silent, not non-vacuous. Named as §R4 (adjudicated, not
  a defect).

## 5. Blockers

None for this seat. Named gaps the parent must close (all in
`claims/c3/verdict.md` §5/§7):

1. **§R1 — the SKILL.md registry row is unapplied.** Apply
   `claims/c3/EX-21/patch/skill-registry-row.patched.md` (`8e56f3d9…`) in the
   same commit as the gate pair; do **not** apply EX-24's stale 24-case
   `SKILL.proposed.md` (`68435482…`).
2. **§R6 — the commit is the parent's.** Receipts self-pin `29bb45ae…`, so any
   later tool revision voids them; re-run the probe (both modes) and the census
   after the row lands, and re-derive every identity the verdict quotes.
3. **§R2/§R3/§R4 — three values not to quote** in the records (EX-21's `(d)`
   `ABSENT 13`, EX-26's 214-line claim, an all-absent `MATCH 5/5` as a content
   witness).
4. **§R7 — records digests.** Quote the **settled** README `9d9400da…` (272
   lines), not the four intermediate values observed during the landing window.

**Identity (rule #14, re-derived after the last write):** this report's
artifact digests are `claims/c3/verdict.md` `3d82bbcb…` (210 lines) and
`claims/c3/VZ-3/vz3-reconciliation.txt` `b98f30b3…` (217 lines); the two real
targets at this seat's close are the tool `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf`
(1343 lines) and the README `9d9400dab7ff7072375c13fad43c02dde0f3923a58cf3af0d50fa3384535022a`
(272 lines); `SKILL.md` is unchanged at `5eec51c0…` (390 lines).
