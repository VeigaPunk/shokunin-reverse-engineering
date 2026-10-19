# Seat CR-4 | chain c2 | role critic — arc3-loop1-round1

Task: attack the cross-chain risk — C3's census re-key (EX-28) edits instrument
files this same wave; could an honest scope re-key trip the citation-drift probe
guard falsely? Analyze + propose the safe ordering.

**VERDICT: NO — an honest census scope re-key cannot trip the probe guard
falsely.** Proven two ways: (a) the probe's resolution set is exactly 14 files,
**none** under `.ufo/gates/` (the census is not among them), and the probe
resolves targets as Git objects at `--rev`, never the moving worktree; (b) a
simulated honest re-key commit (census blob `36e96cd5…` → `e39b1892…`) leaves
the probe verdict invariant (`findings=0`, `--strict` clean) and the digest
EX-16 pins (`sha256(pointer-table.json)` = `738b3a56…`) byte-identical. The
wave's real cross-chain hazards are elsewhere — C1's README edit shape, C2's
row/records text tokens, and the /tmp EDQUOT environment — all demonstrated
below; the safe ordering is `claims/c2/CR-4/proposed-ordering.md`.

Baseline: HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`. EX-16 had **not**
landed at report time (all three real targets still at their before-sha256s,
re-verified: probe `3067621a…`, expected `4e28ba90…`, table `738b3a56…`), so
the guard simulation is of the *declared* semantics (claims-frozen.md:46-50;
EX-20 row text; PL-2 prototype spec), not of landed code.

## 1. Work performed (each bullet with evidence pointer)

- Read frozen claims/roster (`claims-frozen.md:40-54`, `:73-88`), AGENTS.md,
  and the sibling designs: PL-2 plan/prototype spec, EX-20 row patch, SC-4
  changeset, RV-8 guard matrix, CR-5 census attacks.
- Captured instrument identities at HEAD: census `36e96cd5…`, probe `3067621a…`,
  expected `4e28ba90…`, table `738b3a56…` — `evidence/01-baseline.txt:3-7`.
- Probe at HEAD: `reported findings=0 exit=0`; `--strict`: `clean findings=0
  exit=0`; selftest `cases=11 passed=11 failed=0 exit=0` — `01-baseline.txt:8-33`.
- Census at HEAD: `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0
  unresolved=0)` exit 0; counts PROVINCE 162/6, SCORECARD 1336/9, SKILL 371/2 —
  `01-baseline.txt:34-45` (corroborates EX-26/SC-6/RV-11/CR-5).
- **Disjointness enumeration**: table `entries`+`quoted` resolve to 14 distinct
  files; `gates-dir targets: []` — `01-baseline.txt:46-62`. The string "census"
  occurs in the table only inside the `readme22-r7range` note (json scan).
- **Core experiment**: shared-object scratch clone (108K) in `/dev/shm/cr4`;
  plumbing sim commit `95e52bbb…` = HEAD tree + edited census (header
  disposition + one bound re-key; census blob `36e96cd5…` → `e39b1892…`).
  Probe at that rev: `reported findings=0 exit=0`, `--strict` `clean`; table
  blob digest identical at HEAD and at the sim rev (`738b3a56…`) —
  `evidence/02-census-rekey-invariance.txt:1-22`.
- **Guard simulation** (labeled sim wrapper of the declared digest-pin
  semantics, `evidence/` run-all.sh §04): after the re-key, real table + real
  pin → delegate → `findings=0`; one honest appended table entry under the
  stale pin → `pointer_table_tampered … exit=2`; absent table → `exit=2`;
  pre-guard probe on the same edited table is silent in both modes (`0/0`) —
  `evidence/04-guard-sim.txt:1-18`.
- **Mirror attack (C2's SKILL.md edit vs C3's census)**: applied EX-20's
  registry-row diff (SC-4-extracted, sha `dc99484b…`) to a scratch 3-file tree;
  patched `SKILL.md` reproduces SC-4's claimed after-hash `fa94a469…`
  byte-exactly; census on the patched tree: `PASS 0/0/0/0` —
  `evidence/05-census-mirror.txt:1-29`.
- **Boundary demos** (same file): token-stress — adding `rea-agents@6.7.0` to
  the patched row → `FAIL undeclared=1` (loci 2→3, `05:31-43`); parent records
  append, token-free block → `PASS` (SCORECARD 1336→1341 lines, `05:45-56`);
  one pin-bearing records line → `FAIL undeclared=1` (`05:58-65`).
- **C1 edge demo**: line-neutral token appended to `corpus/README.md:22` →
  `findings=0`; a single line inserted before `:175` → **4 findings**
  (`sc69-readme-177`, `readme175-sc1217/r7range/r8e2`) —
  `evidence/03-readme-edge.txt:1-15`.
- All runs read-only on the lane repo (no git mutations there; scratch repo
  commits live in `/dev/shm/cr4` only); custody paths read-only (the census
  greps the three client configs read-only); no installs. Re-runnable pack:
  `claims/c2/CR-4/evidence/run-all.sh` (sha256 `e84e350d…`), transcripts
  `01`–`05` (sha256s `5e5889ad…`, `963e940a…`, `fae393c9…`, `23f57ede…`,
  `a72554e8…`).

## 2. Proposed changes

- **No repo file change proposed by this seat** (critic; and the real targets
  belong to EX-16/EX-28). Two artifacts instead:
  - `claims/c2/CR-4/proposed-ordering.md` — the liftable safe-ordering text
    for the parent's integration.
  - `claims/c2/CR-4/evidence/` — the re-runnable attack pack + transcripts.

## 3. Before→after measurement (chain c2 relevant)

```
before, real target unmodified (01):
  probe --root . --rev HEAD …  → CITATION_DRIFT_VERDICT: reported findings=0 exit=0
  probe --strict               → CITATION_DRIFT_VERDICT: clean findings=0 exit=0
  selftest                     → CLEAN cases=11 passed=11 failed=0 exit=0
  sha256(pointer-table.json)   → 738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f

after, honest census re-key simulated (02, sim commit 95e52bbb…):
  census blob HEAD 36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48
              sim  e39b1892ce6373fcb7f8a69339b1dac113104da279f303e8a166f2283048bafe
  probe at sim rev             → CITATION_DRIFT_VERDICT: reported findings=0 exit=0
  probe at sim rev --strict    → CITATION_DRIFT_VERDICT: clean findings=0 exit=0
  table blob at sim rev        → 738b3a56… (byte-identical to HEAD)
```

The probe's verdict and the pinned digest are invariant under the census edit;
the guard's declared CNE classes fire only on table absence/tamper/unpin, not
on the census. Claim-relevant net: **no false trip exists for C3's re-key.**

## 4. Attacks / refutations attempted, with verdicts

1. *Named hypothesis: honest census re-key trips the guard* — **REFUTED**
   (disjointness `01:46-62`; invariance `02`; digest invariance `02:20-22`).
   Residual coupling: only if a future pointer-table entry cites the census
   file by line — do not add one (rule #11 form: anchor, never line).
2. *Probe default root `.ufo/gates` might read the census instrument* —
   **REFUTED**: the probe reads only table targets, resolved at the rev.
3. *Guard could hash the gate directory (picking up the census / `__pycache__`)*
   — **REFUTED for the declared design** (pin = `sha256(pointer-table.json)`
   only; PL-2 spec, SC-4 manifest row C). Hygiene note: `.ufo/gates/__pycache__/`
   is untracked this wave — keep it out of commits.
4. *An honest **table** edit trips the guard* — **CONFIRMED as designed**
   (exit 2 CNE, never silent; `04:8-11`). Ordering rule: any table edit must
   re-pin `expected.json` in the same commit.
5. *C2's SKILL.md row edit trips C3's census* — **REFUTED as landed**
   (EX-20's row is occurrence-free → PASS; `05:18-29`), but the boundary is
   real: a pin token in the row → `FAIL undeclared=1` (`05:31-43`). The row
   text must stay occurrence-free or the census measurement must follow it.
6. *The parent's records append is census-safe* — **PARTIAL**: token-free
   records PASS (`05:45-56`); one pin-bearing line → `FAIL undeclared=1`
   (`05:58-65`). The round-section text must avoid `rea-agents@x.y.z`, bare
   `6.x.y` in a gate-token unit, and `/path.{json,toml,yml}:N` pointers.
7. *C1's map token is probe-safe* — **PARTIAL**: the claimed line-neutral
   append shape PASSes; a line insertion before `:175` trips **4 findings**
   (`03:5-15`). "Line-neutral" is load-bearing; if a line must be inserted,
   the README pins need re-keying + re-pin in the same commit.
8. *Selftest reliability under /tmp EDQUOT* — **CONFIRMED hazard**: the probe
   selftest needs writable temp dirs (PL-2 measured; my run recorded
   `write error: Disk quota exceeded` on /tmp at `01:1-2`). Run it with a
   writable `TMPDIR` and record it; the census needs no temp dir.
9. *Instrument self-certification (CR-5's A3, cross-checked)* — **CONFIRMED**:
   the census PASS cannot certify its own re-key; the certificates are the
   external diff audit + before/after sha256 recorded in the records commit.
   Probe-side analog: the guard alone does not certify C2 — the measured
   `findings=0` run at the records commit does.

## 5. Blockers

- **/tmp EDQUOT is standing** (tmpfs usrquota; `01:1-2` captured a failing
  write). Scratch relocated to `/dev/shm/cr4` (precedent: EX-20, CR-5, PL-2);
  `/dev/shm` itself hit EDQUOT once mid-wave — retries + assertions added, the
  final transcripts are clean. All scratch removed at close.
- **EX-16 had not landed** at report time. When it lands, re-run the pack
  (`evidence/run-all.sh`) and additionally verify: `sha256(pointer-table.json)`
  equals the pin EX-16 writes into `expected.json`; probe at the records
  commit; census at the same commit.
- **Open, not mine to resolve** (RV-8 matrix): if EX-16 lands the digest check
  for ANY `--table` path (D2), custom-table runs against the committed
  expected.json become exit 2 — the recorded r10 experiment shape (S2). The
  landed scoping (D1 recommended by RV-8) must be stated in the row.
