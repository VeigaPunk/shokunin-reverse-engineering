# C2 verdict — custody-pair hardening: D2 + D3 + write-guard scope + D6 (chain convergence, seat VZ-2, late join)

Wave `arc3-loop1-round3` · chain c2 · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD at verdict work
`c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (no seat commits; parent integrates).
Frozen claim: `claims-frozen.md:38-57`. Seat line: LATE JOIN — reconcile the c2
chain end-to-end, name gaps. This seat's own packet: `claims/c2/VZ-2/`
(partial: before-state injections, run-before/run-after harnesses, final-harness
transcripts) — adopted, re-run and completed here.

**Method note (rule #14).** Every load-bearing number below was re-derived
first-hand by this seat on scratch copies at write time (13:22–13:27Z): the base
column from a `git show HEAD:…` blob in `/var/tmp/vz2/base`, the after column
from a byte-identical copy of the landed tool in `/var/tmp/vz2/final`. Seat
reports and their transcripts were read, not trusted; where this seat re-ran a
seat's harness it says so. Scratch under `/var/tmp/vz2` (never `/tmp`); no git
mutation; custody paths opened for reading only.

## Verdict: **VERIFIED** — all four named holes close as declared classes, the selftest grows 15 → 22, the round's live pair verifies MATCH 5/5, v1 receipts remain sha256-verifiable, and every regression leg re-measured first-hand holds; the one word that remains parent-side ("the registry row … updated in the SAME commit") is a landing action whose patch text is packaged and measured — no measured result contradicts the claim

Frozen claim requires: (a) each named hole closed with a **declared exit class**
(EACCES → its class, no fail-open MATCH; verify coverage declared; write-guard
extended to `set(paths) ∪ CUSTODY_PATHS`; selftest scratch-guard → USAGE);
(b) selftest **15 → ≥17** with the new fixtures; (c) the **registry row +
README updated in the SAME commit** (revision-pinned clauses re-derived);
(d) the round's **live pre/post pair verifies MATCH 5/5**; (e) **v1 receipts
remain sha256-verifiable**; (f) **every receipt self-pins the revised tool's
sha256**; (g) command A unchanged. This seat measured (a), (b), (d), (e), (f)
and (g) directly; (c) is the parent's landing action (only the parent commits)
with both halves measured here — README landed in place, row as patch text.

## Revisions under measurement (identity, re-derived)

| object | revision | lines | bytes | how pinned |
|---|---|---|---|---|
| tool BEFORE | `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` | 889 | 39157 | `git show HEAD:.ufo/gates/custody-pair/custody-pair.py` → `/var/tmp/vz2/base/custody-pair.py`, sha re-derived |
| tool AFTER | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` | 1155 | 54279 | worktree path, sha + `wc -l` + `stat` re-derived 13:22Z; stable across the whole wave window (VZ-4's poller r17–r41 shows the same sha) |
| README AFTER | `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193` | 185 | 9603 | worktree path, re-derived |
| README BEFORE | `fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba` | 132 | — | `git show HEAD:` blob |
| SKILL.md (row target) | `c134afcb2e648aa3f8ff96f11d03aee2be6715811cb7edb3b7be6ac40aa0aa90` | 390 | — | worktree, unmodified by any seat |

## Claim components — status and evidence

| # | Component | Status | Evidence (this seat's own runs unless stated) |
|---|---|---|---|
| 1 | D2 closed — EACCES → declared class, no fail-open MATCH | DELIVERED | base: blocked-parent-dir capture `PARTIAL paths=0/1 exit=13` with `STAT-ERROR`, then `verify --live` **`VERDICT: MATCH paths=1 exit=0`** (fail-open); landed: capture `UNEVALUABLE exit=14` with the `STAT-ERROR` marker preserved, `verify --live` and receipt-vs-receipt both `VERDICT: UNEVALUABLE … exit=14`; chmod-000 file: base **traceback `PermissionError` exit 1, no receipt written**, landed `exit=14` with `EXISTS: yes` + `READ-ERROR: [Errno 13]` and the receipt written |
| 2 | D3 closed — coverage declared and gated | DELIVERED | base: 1-of-5 reference `MATCH paths=1 exit=0`; `--require-paths` **unrecognised** (argparse exit 2). landed: plain form unchanged `MATCH exit=0` (declared default), `--require-paths 5` → `USAGE: reference covers 1 of the required 5 paths` + `REFERENCE-COVERAGE: 1/5 paths present in reference; unaccounted: ~/.config/devin/mcp_config.json ~/.omp/agent/mcp.json ~/.kimi-code/config.toml ~/.bashrc ~/.profile`, exit 2; 5-of-5 reference under the gate stays `MATCH 5/5 exit 0` (no false positive) |
| 3 | Write-guard extended to `set(paths) ∪ CUSTODY_PATHS` | DELIVERED | base `--paths X --out X` → `exit=0`, **X clobbered** (sha moved); landed → `USAGE: refusing to write a receipt over a path it measures or a custody path (path or inode)`, `exit=2`, X sha byte-identical; hardlink alias (`ln -f`) and symlink alias as `--out` also refused, target intact; canonical-direction refusal unchanged |
| 4 | D6 closed — selftest scratch-guard → USAGE | DELIVERED | base `selftest --scratch <missing>` → `FileNotFoundError` traceback, exit 1; landed → `USAGE: scratch base is not a directory: …`, exit 2, zero traceback lines; explicit `/tmp/…` base refused by the EDQUOT guard regardless of explicitness |
| 5 | Selftest 15 → ≥17 with the new fixtures | DELIVERED (22) | base blob `CUSTODY_PAIR_SELFTEST: CLEAN cases=15 passed=15 failed=0 exit=0`; landed `CLEAN cases=22 passed=22 failed=0 exit=0` (this seat's run, `--scratch /var/tmp/vz2/final/st`). Seven new cases, named from the landed bytes: `unreadable-path-is-unevaluable`, `unevaluable-never-matches`, `parsed-unevaluable-reference-never-matches`, `partial-reference-require-paths-gate`, `refuses-to-write-over-scoped-path`, `selftest-missing-scratch-usage-exit`, `refuses-write-through-hardlink-alias` |
| 6 | Live pre/post pair verifies MATCH 5/5 | DELIVERED | this seat's own fresh pair (`/var/tmp/vz2/final/live-{pre,post}.txt`, both `CUSTODY_PAIR_CAPTURE: OK paths=5/5 exit=0`): `MATCH 5/5 drift=0 exit=0`, identical with `--require-paths 5`. The chain's round pair in `claims/c2/receipts/` re-verified by this seat: `config-pre-pair-v2r3-revised.txt` vs `config-post-pair-v2r3.txt` → `MATCH 5/5 exit=0`; both vs `--live` → `MATCH 5/5`; cross-revision `config-pre-pair-v2r3.txt` (old tool) vs post → `MATCH 5/5 exit=0`; all three sidecars `sha256sum -c` **OK** |
| 7 | Every receipt self-pins the revised tool's sha256 | DELIVERED | `grep '^# tool:'` over the chain's three receipts: revised-pre and post both `7cd19c3c…`; round-start receipt pins `112d01dc…` (correct for its own bytes). This seat's fresh pair pins `7cd19c3c…`; equality with an independent `sha256sum` of the tool re-derived |
| 8 | v1 receipts remain sha256-verifiable | DELIVERED | r1 sums-shape vs live: `SHA256-CONTRACT: 4/5 paths agree on sha256`, `CONTENT-DRIFT exit 10` — path 3 (`~/.kimi-code/config.toml`) is the **recorded operator-side drift** (`8cbacd48…`→`bc66d543…`, mtime 2026-10-19T12:57:45Z, pre-wave; field diff in `claims/c2/EX-29/r2-vs-roundstart-fielddiff.txt`, reproduced in this seat's run); clean control with the drifted path removed: `MATCH-V1-PARTIAL 4/4 exit=0`; r1 canonical stanza vs live: `METADATA-DRIFT`×4 with `LABEL-DEFECT` lines + `SHA256-CONTRACT 4/5`, `CONTENT-DRIFT exit 10` (unchanged class from round 2) |
| 9 | Registry row + README in the SAME commit | PARENT-SIDE, patch text apply-ready | README **landed in place** (`f30df42e…`, 185 lines); the row is patch text only (seats cannot edit `SKILL.md`) — two measured variants: `claims/c2/EX-21/proposed-skill-registry-row.patch` (+ anchored apply script) and `claims/c2/EX-30/registry-row.patch.md`; both are line-neutral on the 390-line `SKILL.md` (EX-30's re-emission 390→390 lines, this seat's `diff` of the applied forms confirms one row replaced). **One voice must land** — parent's merge decision |
| 10 | command A unchanged | MEASURED | verbatim SCORECARD.md:92-123 recipe at HEAD `c07af80f`: `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "rule_blocks": 14}` — byte-for-byte the round baseline in `EX-21/commandA-head.json`; C2's edits live under `.ufo/gates/`, outside command A's read set |
| 11 | Round instruments unaffected | MEASURED | census `.ufo/gates/c1-census-v10.py --root .` at HEAD and on a scratch clone carrying the landed tool+README (commit `be8333c`): `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)` exit 0, byte-identical both sides; citation-drift probe on the same clone: `reported findings=0 exit=0`, `--strict clean findings=0 exit=0`, selftest `CLEAN cases=13 passed=13 failed=0 exit=0` |

## Before → after reconciliation (the discriminating unit, all first-hand)

Runner: this seat's own scratch harness runs (`/var/tmp/vz2/base` for the HEAD
blob, `/var/tmp/vz2/final` for the landed bytes), plus the re-runs of the chain's
own harnesses named in §Regression.

| # | injection (declared class) | before `112d01dc…` | after `7cd19c3c…` |
|---|---|---|---|
| L1 | D6 `selftest --scratch <missing>` (USAGE) | `FileNotFoundError` traceback, exit 1 | `USAGE: scratch base is not a directory: …`, exit 2, 0 traceback lines |
| L2 | D2a blocked parent dir (14) | capture `PARTIAL 13` + `STAT-ERROR`; verify **`MATCH exit 0`** | capture `14`; verify `UNEVALUABLE exit 14`, no MATCH |
| L3 | D2b chmod-000 file (14) | capture traceback exit 1, **no receipt** | capture `14`, receipt written with `EXISTS: yes` + `READ-ERROR` |
| L4 | D3 1-of-5 reference (USAGE) | plain `0`; gate flag unrecognised | plain `0` (declared default); gated `2` + `REFERENCE-COVERAGE: 1/5 … unaccounted: …` |
| L5 | write guard `--paths X --out X` (USAGE) | `exit=0`, X **clobbered** | `exit=2`, X bytes unchanged |
| L6 | write guard, hardlink + symlink alias (USAGE) | clobbered (inode arm absent) | `exit=2`, target bytes unchanged (both alias forms) |
| L0 | selftest | `CLEAN cases=15 passed=15 failed=0 exit=0` | `CLEAN cases=22 passed=22 failed=0 exit=0` |
| L7 | live pair + gate | `MATCH 5/5 exit 0` (gate unrecognised) | `MATCH 5/5 exit 0`; `--require-paths 5` → `MATCH 5/5 exit 0` |
| L8 | v1 shapes | sums 4/4 `MATCH-V1-PARTIAL 0`; r1 canonical `CONTENT-DRIFT 10` / `SHA256-CONTRACT 4/5` | identical classes both shapes |
| L9 | custody digests | round-1 pins, path 3 drifted | identical (read-only block, re-measured) |

**Headline numbers:** selftest **15 → 22** (claim bar ≥17); the four injections
reproduce as their declared classes on both sides; live pair `MATCH 5/5` plain
and gated; command A `82/82`, `14/14`, `10.0/10.0` unchanged; census `PASS`,
probe `findings=0` both modes, probe selftest `13/13`.

## Regression matrix (re-run first-hand, not read)

| harness | seat | this seat's re-run | result |
|---|---|---|---|
| `EX-27/harness/regress.py` — 41-row round-2 regression | EX-27 | baseline phase vs the HEAD blob → `rows=41 hold=37 fail=0 observed-only=4`; revised phase vs the landed bytes → `rows=41 hold=41 fail=0 observed-only=0` | **matches EX-27's recorded tally exactly**; the 4 observed rows are the four hole before-states; 13/13 CR-4 rewrite forms keep their classes (`REWRITE-DRIFT 11` / `CONTENT-DRIFT 10`), live-pair and self-pin legs HOLD |
| `CR-3/run_matrix.py` — 54-case type-swap matrix | CR-3 | re-run on a copy of the harness pointed at `/var/tmp/vz2/cr3` against the landed tool; 51 named cases, **exit-line diffs vs `CR-3/matrix-AFTER2.out` = 0 of 51**, no case-name set difference | **exit-for-exit identical** to CR-3's recorded after-state |
| `RV-5/sabotage.py` — 4 mutation arms | RV-5 | re-run first-hand | **identical to RV-5's log**: S1 DIRTY with exactly `[unreadable-path-is-unevaluable, unevaluable-never-matches, parsed-unevaluable-reference-never-matches]`; S2 DIRTY with the two guard cases; S4 DIRTY with `partial-reference-require-paths-gate`; **S3 CLEAN with the case missing from the run** — see residual R1 |
| citation-drift probe / census / command A | EX-31, EX-32, EX-29 | re-run on the landed-revision clone `be8333c` | probe `findings=0` default + `--strict`, selftest 13/13; census `PASS`; command A as above |
| `RV-7/summarize.py` over `snap2-7cd19c3c-*.json` — 5-arm guard mutation matrix | RV-7 | read + cross-checked against this seat's own RV-5 sabotage re-run | clean `BLOCKED` 22/22 CLEAN; M1 (whole guard reverted) **CLOBBER** + DIRTY 20/22; M1a (scoped arm reverted) **CLOBBER** + DIRTY 20/22; M1b (inode arm reverted) `BLOCKED` + DIRTY 21/22 (the hardlink case alone); M2 (coverage reverted) `BLOCKED` + DIRTY 21/22 (the gate case alone) — each arm fails exactly its own cases, so both guard arms and the gate are load-bearing |

EX-32's own `probe.md` left its §5 post-EX-21 measurement as a `PLACEHOLDER`
(the probe grades committed blobs, so the reading needed a commit). This seat
supplied the missing measurement: a scratch clone at `c07af80` with the landed
`custody-pair.py` + `README.md` committed as `be8333c` (tool sha re-derived
`7cd19c3c…`, README `f30df42e…`) → `findings=0` in both modes, selftest 13/13,
no needle staled. That is the closest available reading before the round's work
commit; the parent re-runs it at the real commit.

## Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | "the 22-case selftest is a rubber stamp" | **refuted, re-measured** — each closure case fails on a mutated copy: RV-5's four sabotage arms re-run here reproduce DIRTY with exactly the expected failing sets (S1 3 cases, S2 2, S4 1), while the 15 legacy cases stay green on both revisions (15/15 → 22/22), so the growth is additive |
| A2 | "the D2 closure is a cosmetic exit-code change" | **refuted** — the fail-open is a *verdict* change: base `MATCH paths=1 exit=0` on an exists-but-unstattable path (both `--live` and receipt-vs-receipt), landed `UNEVALUABLE exit=14`. RV-6's single-hunk mutation (removing only the 8-line `compare_section` guard) restores the fail-open while capture-side stays closed — the verify-path guard is the load-bearing line, and this seat's own before-state run shows the same shape |
| A3 | "the write guard refuses only `--paths X --out X` because X is somehow special" | **refuted** — hardlink alias and symlink alias are refused too, with the same USAGE line and the target sha unchanged; EX-25's independent decoy-twin 10-case probe and CR-4's 19-case battery agree |
| A4 | "the D3 gate breaks fixture/v1 workflows" | **refuted** — opt-in by declaration: plain `verify` on a 1-of-5 reference still reads `MATCH exit 0` (this seat's run, plus the selftest case), v1 shapes keep their classes, and a 5-of-5 reference under the gate passes |
| A5 | "the EACCES class swallows genuinely-absent paths" | **refuted** — `ENOENT` carries no error marker and stays `ABSENT 13`; the base case `absent-path-detected` is green on the landed revision and the `ABSENT` class is untouched by the new markers |
| A6 | "the receipts' self-pin is stale relative to the landed bytes" | **refuted at write time** — all three chain receipts' `# tool:` lines re-checked against an independent `sha256sum` of the landed tool; sidecars `sha256sum -c` OK; the cross-revision verify shows the shipped pair is valid even though the round-start receipt pins the previous revision |
| A7 | "C2's edits broke a neighbouring instrument" | **refuted** — census byte-identical PASS at HEAD and on the landed clone; probe `findings=0` both modes; probe selftest 13/13; command A unchanged |
| A8 | "the chain's regression claims are seat text, not measurements" | **partially sustained then discharged** — EX-27's and CR-3's *recorded* outputs were re-run by this seat rather than trusted: 41/41 HOLD revised, 37/0/4 baseline, 51/51 exit-line agreement. **One first attempt produced 8 spurious FAILs in the baseline phase** — caused by a third-party clobber of a round-1 receipt mid-run, not by the tool (see Blockers/§R2) |
| A9 | "the live pair is stale because the tool moved after capture" | **refuted** — VZ-4's 60 s poller records the tool at `7cd19c3c…` from r17 through r41 (13:17:30Z–13:25:30Z), i.e. unchanged across every capture quoted here; this seat re-derived the sha at 13:22Z |

## Named residuals (measured; none voids the claim)

1. **R1 — RV-5 S3's sabotage arm is not load-bearing as written.** Reverting the
   `if not base.is_dir():` scratch guard leaves the selftest `CLEAN` with
   `selftest-missing-scratch-usage-exit` **missing from the run** — the case
   re-invokes `cmd_selftest` in-process, and the `try/except OSError` around
   `tempfile.mkdtemp` (`custody-pair.py:729-733`) still converts the missing-dir
   failure to USAGE. So the guard's *behaviour* is doubly closed (two
   independent arms) but the *case* cannot distinguish which arm is live. This
   seat reproduced the exact row RV-5 logged; RV-5 recorded it as a `missing`
   entry rather than smoothing it. Not a defect in the tool; a coverage note.
2. **R2 — third-party clobber of a round-1 historical receipt (observed; restored
   33 s later by another seat).** `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt`
   was overwritten at **13:25:02Z** by VZ-4's late C2 after-state suite
   (worktree content began `== VZ-4 C2 after-state suite ==`; 21017 B / 305
   lines vs the HEAD blob `b8ed19365c103a4ab355678f0fffe0db4e0011a18b441e79f38d9e80de3d0776`,
   2045 B / 52 lines). Independently observed and exonerated by RV-9
   (`claims/c2/RV-9/rv9-third-party-clobber-observation.out`). It broke this
   seat's first baseline regression run (8 spurious FAILs) until re-run against
   a pristine clone. **Re-checked at 13:27Z: the worktree file is back to the
   HEAD blob** (`sha256sum` = `b8ed1936…`, 2045 B, mtime 13:25:55Z, clean
   against HEAD in `git status`) — some other seat restored it inside the same
   minute. No restore action is outstanding; the parent should just confirm the
   file is not committed in a clobbered state. Nothing in the c2 chain depends
   on that file, but the round's records must not quote a clobbered path.
3. **Sidecar path is not scope-checked** (`--out X.sha256 --paths X` can aim a
   derived sidecar at a measured file's neighbour) — measured by RV-8 (gap 2)
   and CR-4 (T7/T18); EX-30's v2 README patch text names it as a residual and
   EX-21's landed README does not claim it. Outside the frozen claim's letter.
4. **`out.parent.mkdir(...)` outside the guarded `try`** (CR-3 U3 / CR-4 T16):
   `--out` whose parent *component* is a regular file tracebacks at both
   revisions (exit 1, outside the declared map). Deliberately not landed after
   freeze — it would invalidate the wave's independently re-derived pins on
   `7cd19c3c…` for a non-claim hole. Patch sketch in CR-3 §3 / CR-4 §2.
5. **Coverage gate counts stanzas, not distinct paths** (EX-24): a
   duplicate-stanza reference can pass the gate. Patch-ready
   (`EX-24/proposed-coverage-count.patch.md`), outside the claim's letter.
6. **Contract denominator / `--require-sha`** (EX-28) — proposal only, named as
   residual; and EX-33's self-pin context lines (a pin is a render-time disk
   read, so it can name bytes that did not execute) — patch text, no claim.
7. **CR-3 W4 wording**: the gate's `unaccounted:` list names the canonical paths
   *absent from the reference*, which is the declared semantics; wording only.
8. **`__pycache__` residue** under `.ufo/gates/`, `.ufo/gates/citation-drift/`,
   `.ufo/gates/custody-pair/` — untracked; EX-21 measured that the pyc predates
   every round-3 run. Must stay out of the landing commit (round-2 precedent).

## Patch texts (index, with identities re-derived at write time)

| file | sha256 | purpose |
|---|---|---|
| `PL-2/candidate.patch` | `838f98fbc1d63d17d4c703521b66a2e25b283887acb08e95da4c21955aa49aec` | the plan's generated candidate (pre-landing revision) |
| `PL-2/landed-fix.patch.md` | `f54adadd2d87ae0c99099a0d928e6f44ffa66daf8a4c4a41ef9bc69527dc21fd` | the `_run_verify` interim-defect fix |
| `EX-21/proposed-skill-registry-row.patch` (+ `.patch.md`) | `c0c6d705…` / `9cf7d117…` | registry row, implementer's revision-pinned form + anchored apply script |
| `EX-30/readme.patch.md`, `EX-30/registry-row.patch.md` | `29c5dd82…`, `353ff2b6…` | scribe's v2 drafts (RV-8's two corrections applied; README half superseded by EX-21's landed file). **Re-emitted at 13:25:56–58Z, after this seat's first hash read** — the re-emission was re-read and re-hashed here; content is still the corrected v2 form (the refuted "reported but not enforced" clause appears only inside the correction note, and the sidecar path is named as an unguarded residual) |
| `EX-24/proposed-coverage-count.patch.md` | `579304d4…` | distinct-path coverage counting |
| `EX-26/proposed-scratchguard-residuals.patch.md` | `3313b9d4…` | scratch-guard residuals |
| `EX-28/proposed-contract-denominator.patch.md` | `cf0ad2cc…` | contract denominator / `--require-sha` |
| `EX-33/proposed-selfpin-context.patch.md` | `b0790db2…` | self-pin context lines |
| `CR-3/typeswap-declarations.patch.md` | `46c7f78c…` | type-swap declaration texts (§1 resolved in-flight; §2–§5 open) |
| `CR-4/proposed-write-guard.patch.md` | `6033d20b…` | sidecar guard, mkdir mapping, TOCTOU declaration |
| `EX-32/pointer-table-reanchor.patch.md` | `c0b0d2b4…` | re-anchor proposal for line-pinned needles into the custody tool |
| `RV-8/rv8-corrections.patch.md` | `34902a8b…` | the two EX-30 clause corrections (both adopted in EX-30 v2) |
| `RV-6/mutations/*.patch` | (5 files) | the mutation arms behind A2 |

## Seat delivery status at verdict time (poll tally, this seat's checks)

**Rev 2 (13:27Z):** the seats dir held **55 files** at the rev-2 read (56 at
13:27:44Z, 57 at 13:28:01Z — the wave was still delivering); every c2 seat has a
report **except SC-3, SC-4, RV-5 and VZ-2** (this seat, written after this file).
The reports that landed between rev 1 and rev 2 — EX-23, EX-29, EX-30, EX-31,
EX-32, RV-7, RV-9 — were read here and **none contradicts any row of this
verdict**; three strengthen it:

- **EX-32's** isolation matrix is stronger than this seat's clone rehearsal: the
  tool+README revision alone (world H) reads `findings=0` both modes, no needle
  target is `custody-pair.py` (0 entries), and all four custody README anchors
  `HIT` on both the pre- and post-revision README. It also reproduces a
  **collision case**: if the parent lands the extended pointer table *and* a
  registry row whose text the table pins, the row entry reads `citation_dead`
  (world G, `60/61 clean`, strict `exit=1`). **Landing-order consequence for the
  parent:** land the re-anchored table and the row in the same commit and re-run
  the probe; if the collision fires, take EX-32's `pointer-table-reanchor.patch.md`
  form (which reads 0 for both row drafts).
- **RV-7** independently confirms both guard arms are load-bearing (M1/M1a fail
  the two guard cases; M1b fails the hardlink case alone), matching this seat's
  RV-5 sabotage re-run; and confirms `verify r5 r5 --require-paths 5` → `MATCH
  5/5` where a 1-of-5 reference alone gates at exit 2 (no false positive).
- **RV-9** corroborates EX-29 with six `MATCH 5/5` pair directions.

At rev 1 the tally was 44 files with EX-23/29/30/31/32/RV-7/RV-9 missing; every
one of those seats had landed artifacts that this verdict read and, where
load-bearing, re-measured — the missing reports were paperwork, not evidence.
The parent's roster reconciliation counts the items array, not this tally.

## Closing procedure (what flips the remaining parent-side words to green)

1. **Confirm the clobbered-then-restored round-1 receipt** (§R2) is clean before
   quoting it; it reads the HEAD blob again as of 13:27Z.
2. Land **one voice** of the registry row in the SAME commit as the tool +
   README (both already in place); re-derive the tool/README/row identities at
   the commit (rule #14). README patch text is not needed — EX-21's landed file
   is the corrected form.
3. Exclude the three `__pycache__` dirs from the commit.
4. Re-run at the work commit: command A (expect 82/82, 14/14, 10.0/10.0),
   census (`PASS 0/0/0/0`), citation-drift probe both modes (`findings=0`),
   probe selftest 13/13 — this verdict's clone-based readings are the
   pre-flight. If the extended pointer table and the registry row land together,
   take EX-32's re-anchored table form and re-check the collision case (see the
   delivery-status section).
5. Re-quote the live pair from `claims/c2/receipts/` with `--require-paths 5`,
   and the v1 numbers with the `SHA256-CONTRACT` line attached (the round-2
   wording ruling).
6. This file's own identity is re-derived **after** its last revision and
   recorded out-of-band in
   `claims/c2/VZ-2/evidence/verdict-identity.txt` (a self-hash written inside
   this file would invalidate itself on write).

## Verdict basis note (evidence discipline)

Every component row cites a command this seat ran at write time plus, where the
chain produced one, the seat artifact that first recorded it. No seat report was
treated as evidence without at least one first-hand re-measurement against the
landed bytes: the four injections on both revisions, the selftest count, the live
pair and its sidecars, the v1 shapes, command A, census, probe, EX-27's 41-row
battery on both phases, CR-3's 51-case matrix exit-lines, and RV-5's four
sabotage arms. Where a first-hand run disagreed with a recorded one (the
baseline FAILs), the cause was found and named rather than averaged away.
