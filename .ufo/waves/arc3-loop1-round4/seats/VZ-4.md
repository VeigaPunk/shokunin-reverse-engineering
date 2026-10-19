# VZ-4 — seat report (chain cross, wave-integrator, arc3-loop1-round4)

Seat VZ-4 · chain cross · role **wave-integrator** · wave `arc3-loop1-round4`,
2026-10-19. Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`015e1bab914713568f339fd53999bc180459cc40` (immobile at every sample; no seat
commits — the parent integrates).

**Task as frozen:** poll seats every 60 s (max 30 checks); write
`claims/cross/wave-summary.md` — seats delivered /48 vs the frozen roster (name
undelivered), per-chain verdicts, custody outcome, parent-facing admission inputs;
note the lane substitution. Seat report last.

**Lane note read and honored:** the hyper lane returned **402 out-of-credits on the
entire 48-seat roster at first dispatch** (zero delivered, ~30 s); per the round-4
schedule's declared fallback and the operator directive the full roster
re-dispatched on the devin lane (`devin/deepseek-v4-1-flash-max`). Recorded with
cause, **not** a lane signal; the roster, claims and assertions are unchanged.

**Writes by this seat:** `claims/cross/wave-summary.md`, this report, and
`claims/cross/VZ-4/**` only. No git mutation. No corpus/LOG/SCORECARD/README/
SKILL/PROVINCE write; no custody-path write (opened read-only for sha256/stat and
for receipt capture, which the tool itself is read-only over). Scratch under
`/var/tmp/vz4` — **`/tmp` never used** (standing EDQUOT rule).

---

## 1. Work performed (evidence pointers)

**Poller (30 × 60 s) and real-target watcher (30 × 60 s).** `poll.log` (seat dir +
non-empty claim files per check), `targets.log` (custody tool, README, pointer
table, `expected.json`, `PROVINCE.md`, `SKILL.md` hashes + `git status` per check).
Both ran from 14:04Z; the poll window closed at check 27.

**Baseline instruments, re-run first-hand at HEAD.** command A (verbatim
`SCORECARD.md:92-124` recipe, git-mode) → `83/83, missing [], dangling [], 14/14,
10.0/10.0`; census `PASS (0/0/0/0)`; citation-drift probe `findings=0` both modes +
selftest `13/13`; custody selftest `22/22 CLEAN`.
`evidence/instruments-baseline.txt`.

**Four independent REA probes of the round's Vyper carriers** (`rea-agents@6.4.0`,
hex leg, disk-backed `TMPDIR`), all first-hand:

| carrier | recovered | vs ABI-derived set | sealed id | evidence file |
|---|---|---|---|---|
| EX-02 smoke | 4/4 | equal, 0 missing / 0 extra | `ev_073f845c…` | `vz4-probe-smoke-6.4.0.json` |
| EX-03 StewardToken (ERC-20-bearing) | 22/22 | equal | `ev_6b8a15c4…` | `vz4-probe-ex03-6.4.0.json` |
| EX-04 CarrierV (non-ERC-20 vault) | 15/15 | equal | `ev_d1792f57…` | `vz4-probe-carrierv-6.4.0.json` |
| PL-1 CarrierW | 9/9 | equal | `ev_b9d050db…` | `vz4-probe-carrierw-6.4.0.json` |

My `ev_d1792f57…` for EX-04's runtime is **byte-identical** to VZ-1's independent
run at the same path with the same request — same-path/same-request id
determinism.

**C1 landing rehearsal on the actual landing source.** Extracted the entry
**literal block** (32 lines / 18,166 B / `da42d9a2…`) and the map token, applied
both to a scratch tree carrying the 83 prior knowledge files: command A →
**84/84, missing [], dangling [], 14/14, 10.0/10.0**; README **190 → 190**,
`1cd05260…` (matching SC-1's independent prediction); **prior-83 byte-identical
83/83, 0 mismatches** against their git-HEAD blobs.
`evidence/c1-records-identities-check.txt`.

**C2 — census and repair verification.** Re-ran VZ-2's
`province-staleness-census.py` (`e6eef574…`) → `total=26 stale=6 adjudicated=2
current=18`, the identical stale set. Reproduced **EX-14 v2** (`69ceea9b…`, 162 L,
6/7 needles), **EX-13's per-row set + F3 + C1** (6/7), **EX-11's A+B+C+D**
(`e2335400…`, 162 L, 7 hunks), and **PL-2's candidate-with-s5** (`163a546e…`,
162 L, 7/7 needles via a content-anchored parser). Confirmed the census cannot
grade repairs (it measures live evidence, not text).
`evidence/c2-*.txt`.

**C3 — before AND after, first-hand.** Measured all four residuals on the r3 base
`7cd19c3c…` (sidecar spelling A **clobber** `fbeec2be…`→`cfcc6947…`; spelling B
clobbers a genuine pre-existing sidecar `63fa9d49…`→`85deabbc…`; mkdir raw
`NotADirectoryError` exit 1; 5× dupe stanzas pass the gate silently) and on the
landed `29bb45ae…` (all closed: exit 2 with files intact, declared USAGE,
`REFERENCE-COVERAGE: 1/5`). **Sabotage arms** — reverting each fix individually
returns its residual. Selftest **22 → 28**. Live pairs `MATCH 5/5`.
`evidence/c3-residuals-before.txt`, `c3-residuals-after.txt`.

**Records-side verification.** CN-2's merged SCORECARD section (`7bfeaa90…`) and
LOG entry (`815980b9…`) are **pin-free CLEAN**; appending the section to a scratch
root (1580 → 1760 L) leaves the census at **PASS 0/0/0/0**. Same for SC-3's C3
draft (8208 chars appended → PASS). `evidence/records-fold-check.txt`,
`pin-free-verification.txt`.

**Closing sweep** at 14:30Z: every instrument green, real targets frozen.
`evidence/closing-sweep.txt`.

**Deliverable:** `claims/cross/wave-summary.md` (579 lines) — the wave's arc and
lane substitution, per-chain verdicts, custody outcome, attacks, parent-facing
admission inputs, and the closing census (47/48 at census time, 48/48 once this
report lands).

---

## 2. Proposed changes (patch-text paths)

**None by this seat.** VZ-4 is the wave integrator; it wrote no real target and
proposes no repo-surface change. The landing actions it verified are named in
`claims/cross/wave-summary.md` §6 (C1 entry literal + token; C2 repair set; C3
tool + README + registry row; the records fold).

---

## 3. Before → after measurement for the chain's claim

VZ-4's chain is `cross` — it carries no single falsifiable claim of its own; its
measurement is the wave-level before → after:

| quantity | before (14:04Z) | after (14:30Z) |
|---|---|---|
| seat reports delivered | 0/48 | **47/48** (48/48 with this report) |
| custody tool | `7cd19c3c…`, 1155 L | **`29bb45ae…`, 1343 L** |
| custody README | `f30df42e…`, 185 L | **`9d9400da…`, 272 L** |
| custody selftest | `22/22 CLEAN` | **`28/28 CLEAN`** |
| custody live pair | — | **`MATCH 5/5`** (two independent pairs) |
| command A | `83/83, 14/14, 10.0/10.0` | unchanged at HEAD (**84/84 projected** on the C1 landing) |
| census | `PASS 0/0/0/0` | unchanged |
| citation probe | `findings=0`, selftest 13/13 | unchanged |
| `corpus/README.md` / `PROVINCE.md` / `SKILL.md` | `a451ad16…` / `d075a3c6…` / `5eec51c0…` | **unchanged all window** (patch texts only) |

---

## 4. Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| 1 | "the freeze's literal sidecar spelling (B) is closed by the candidates then in the tree" | **SUSTAINED at the time** — B was open on base, on RV-7's DRESS2, and on EX-24's `after`/`after2`; the landed revision's `neighbours` arm closes it, and removing that arm returns the residual (VZ-4 measured both directions) |
| 2 | "K/K against vyper's own `method_identifiers` is safe" | **CONFIRMED as a trap, REFUTED as a defect** — the fallback pseudo-entry (`__default__() -> 0x89402a72`, absent from the runtime bytes) and leading-zero stripping (`0xc751377`) would each produce spurious mismatches; the chain's own scripts normalize both |
| 3 | "the r1/r3 `offsets land on JUMPDEST` reading generalizes to Vyper" | **REFUTED** — 0/15, 0/9, 0/4 on JUMPDEST; 15/15, 9/9, 4/4 immediately after `JUMPI`; EX-09's sharper rule `offset == push4_pc + 11` holds 7/7 and 4/4 |
| 4 | "the PROVINCE Frontier bullet is fine" | **REFUTED** — stale on both legs; VZ-4 applied a line-neutral repair and the census stayed PASS at 162 lines |
| 5 | "C2's best patch drives stale to 0" | **REFUTED at the revision measured** (6 → 2); **later SUSTAINED** once v2/EX-13/EX-11/PL-2 landed — the verdict was revised, not smoothed |
| 6 | "VZ-2's census rating of the pacman clause is right" | **REFUTED** — r4-10's own header says "cached pacman pairs"; RV-3, EX-15 and VZ-4 converge on STALE; EX-15 diagnosed the substring-test failure mode |
| 7 | "EX-11's patch identity reproduces" | **REFUTED** — fabricated header digest + dead evidence pointer; EX-11 revised, and the repaired four-patch claim then reproduced byte-exactly (`e2335400…`) |
| 8 | "EX-14 v2 is a clean patch" | **REFUTED (CR-2's finding, VZ-4 confirmed)** — 5 of 6 hunks fail under `--fuzz=0`; default fuzz lands a self-contradictory X1 sentence. CR-2's replacement applies cleanly under strict fuzz |
| 9 | "PL-2's patch texts are landable" | **REFUTED** — non-standard `@@ line NN @@` headers; `patch` reports "Only garbage was found in the patch input"; no applier shipped |
| 10 | "the census PASS certifies the repairs" | **REFUTED** — the Frontier region is UNDECLARED and the EVM bullet carries no needle, so the gate reads the same PASS before and after; the acceptance test must be the clause-level audit |
| 11 | "the census instrument can grade the repairs" | **REFUTED** — it computes verdicts from live evidence, not text; it prints `stale=6` against both the original and the fully-patched file |
| 12 | "the records fold risks a census regression" | **REFUTED** — CN-2's merged section is pin-free CLEAN and appending it leaves the census at PASS (VZ-4's own run) |
| 13 | "my own `69656e74` PUSH4 claim was right" | **REFUTED — my own error, corrected** — it is a substring of the revert string `insufficient` inside a `PUSH32` payload, not a PUSH4 immediate; conclusion (zero false positives) unchanged. Recorded in `vyper-kk-traps.txt` with the original left as written |

---

## 5. Blockers

**None.** The wave completed with every seat reporting. Residual items the parent
inherits (none blocking a landing):

1. **C1** — two entry-text repairs named by the c1 verdict (the `69656e74`
   mechanism sentence, the "same three legs at the same path" sentence); CR-1's
   five edits; EX-07's r3-entry 6.5.0 correction. All have patch texts.
2. **C2** — the X1 bullet's wording (both current forms are wrong; the
   r14-01-cited form is the corpus-supported one), the pacman clause (repaired by
   PL-2 and EX-15's adjudication, not by EX-14 v2/EX-13/EX-11), and CR-2's hunk-6
   correction for v2.
3. **C3** — the SKILL registry row is unmet only by non-application (apply
   EX-21's `skill-registry-row.patched.md`; do **not** apply EX-24's superseded
   proposal); RV-6's M5 coverage gap (the `--out`-name guard has no selftest case).
4. **Records** — quote the delivered count **per lane** (the hyper 402 → devin
   fallback), keep `__pycache__/` out of the landing commit, and note the
   pre-existing dirty ` M .ufo/waves/arc2-loop1-round10/C3.md` as not this
   round's.

*Written by seat VZ-4. This seat wrote only this report,
`claims/cross/wave-summary.md` and `claims/cross/VZ-4/**`. No git mutation of the
real repo; custody paths read-only; scratch under `/var/tmp/vz4` (never `/tmp`);
no corpus/LOG/SCORECARD/README/SKILL/PROVINCE writes.*
