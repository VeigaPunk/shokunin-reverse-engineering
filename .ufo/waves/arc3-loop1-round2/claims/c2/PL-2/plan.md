# PL-2 plan — C2 census fail-closures H1+H3: merged v11 (design of record + as-built verification)

Seat PL-2, chain c2, role planner, wave arc3-loop1-round2, 2026-10-19.
This plan was written *after* the designated implementer (EX-16) landed the edit
(it raced ahead of the plan); it therefore has two jobs: state the design of
record for v11, and verify the as-built bytes against that design at the
implementer's own receipts and at this seat's independent matrix. Divergences
are listed as findings (§6), not silently accepted.

## 0. Revision banner — as-built history (read first)

The implementer re-landed the instrument three times while this plan was being
written. Every statement below is sha-anchored; the claim-critical state is the
last revision, which this seat re-verified end-to-end:

| Rev | sha256 | floor | ordinary HEAD run | this seat's verification |
|---|---|---|---|---|
| v10 (before) | `6f1d19ff…` | none | PASS 0/0/0/0 exit 0 | baseline (RV-6 before copy), §2 |
| r1 | `82fb807e…` | tree-level (`current-ok > 0`) | PASS 0/0/0/0 exit 0 | full matrix green, §1-§7 as first written |
| r2 | `c95a5cf3…` | per-file, counted in *blocks* | **FAIL exit 1, `['BLIND-INSTRUMENT']` — claim-breaking false FAIL** | measured 09:11-09:12 (SKILL.md has 0 current-ok *blocks* and 3 current-ok *dets*); EX-14's `proposed-h3-floor-scoping.patch.md` Trap 1 predicted it |
| r3 | `df9ffdf9…` | per-file, counted in *dets* | PASS 0/0/0/0 exit 0 | full matrix re-run green; invariance HOLDS; creep 0 flags |
| r4 | `a4c16763…` | unchanged (text-only over r3) | PASS 0/0/0/0 exit 0 | re-verified: H1 FAIL `UNREADABLE`, nullskill FAIL `BLIND-INSTRUMENT`, invariance HOLDS, creep 0 flags, 13/13 shared JSON keys equal |
| r5 (live at handoff) | `d0772ce8…` | unchanged (text-only over r4) | PASS 0/0/0/0 exit 0 | re-verified at the same hand: H1 FAIL `UNREADABLE`, nullskill FAIL `BLIND-INSTRUMENT`, invariance HOLDS, creep 0 flags |

r3 additionally closes a class the frozen claim did not name: a present,
readable `SKILL.md` whose declared rows are stripped of every needle
("nullskill") — v10 and r1 read PASS, r3 reads FAIL `BLIND-INSTRUMENT`
(`receipts/matrix-final.txt` §nullskill, probe below). The transient r2 state is
recorded because it is the C1 rule-#14 hazard in the concrete: a mid-wave
revision invalidates every already-captured receipt, and EX-16's
`after-sha256.txt` still cites r1 (`82fb807e…`) — it must be re-derived at the
final sha before the records commit.

## 1. Debt, claim, upstream texts

- Frozen claim (`.ufo/waves/arc3-loop1-round2/claims-frozen.md:34-50`): after the
  round's commit, the census FAILs with a declared class when a scoped file is
  absent, and FAILs when its positive-floor assertion finds zero loci in a
  non-empty scope; every round-1 silent-PASS injection reproduces as a declared
  FAIL; ordinary runs at HEAD stay PASS 0/0/0/0; scope bounds byte-stable
  (creep audit 0 flags); the H4 self-certification residual stays named, with
  the external diff audit (`scope-diff.py` form) as the chain's certificate.
- Round-1 verdict items closed here: H1 (`.ufo/waves/arc3-loop1-round1/claims/
  c3/verdict.md:62-69`, absent all-CURRENT scoped file reads silent PASS) and H3
  (`verdict.md:71-76`, blind instrument passes). Patch texts: `claims/c3/RV-11/
  proposed-missing-file-guard.patch.md` and `claims/c3/CR-5/
  proposed-g2-positive-floor.patch.md`.
- **Both patch texts are stale-anchored**: they were drafted against v9 (sha
  `36e96cd5…`, lines 382-398). The landed instrument before this round was v10
  (`6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`, 490
  lines, HEAD `14b1682`), where the corresponding code sits at `:438-447`
  (missing-file path) and `:453` (G2 disjunct). Re-anchoring was the planner's
  first task; the implementer's landing is the re-anchor of record.
- Explicitly out of scope (stay named): H2 inline-marker excusal (`verdict.md:
  70`), H4 self-certification (`:77`), H5 gate-free version statements (`:81`),
  H6 fixed-bound rationale text (`:84`).

## 2. Before-state (measured; commands and receipts in §5/§7)

| Item | Value |
|---|---|
| v10 baseline anchor | `.ufo/waves/arc3-loop1-round2/claims/c2/RV-6/before/c1-census-v10.py`, sha256 `6f1d19ff…` |
| H1 at v10 | absent `SKILL.md` → `lines=0 loci=0`, SCOPE-ERRORS `[]`, PASS exit 0 (hole) |
| H1 siblings at v10 | 0-byte file, 5-line truncation, EACCES, directory-as-file → all PASS exit 0 (hole; EX-17 `before-*.txt`, this seat's `receipts/matrix.txt`) |
| H3 at v10 | PIN/VER/PTR neutered → all files `loci=0`, `G2 … ok`, PASS exit 0 (hole); REA_GATE narrowed → same |
| DATED-bearing files at v10 | absent `PROVINCE.md`/`SCORECARD.md` already FAIL via "marker uncheckable" scope errors — H1's silent class is exactly the all-CURRENT file |
| HEAD at v10 | PASS exit 0, counts PROVINCE 162/6, SCORECARD 1417/9, SKILL 371/2 |

## 3. Design of record — three prongs, each load-bearing

The merged v11 closes H1 and H3 plus the shrink siblings H1 leaves open. Each
prong below is the *only* prong that fails at least one fixture, so no prong is
vestigial:

1. **P1 UNREADABLE (H1; landed as G19, `c1-census-v10.py:491-506`)** — a scoped
   file that cannot be read (OSError: absent, EACCES, is-a-directory) is a
   declared could-not-evaluate class: appended to `unreadable`, carried in
   `counts` as `{"lines": None, "loci": None}` (an honest "could not read", not
   a false zero), printed as its own line, mirrored in `--json`
   (`unreadable`, `declared_fail_classes`), and folded into `ok`. Load-bearing:
   in the absent-SKILL fixture the other two files still hold `current-ok=5`, so
   the floor alone would not fail it.
2. **P2 BLIND-INSTRUMENT floor (H3; landed as G20, `:513-529`)** — `g2_ok` is now
   `current-ok loci >= 1`; the vacuous second disjunct is gone. The class is
   declared in text and JSON (`BLIND-INSTRUMENT`), exit 1. Because
   `current-ok > 0` implies `loci_total > 0`, this is equivalent to the claim's
   "zero loci in a non-empty scope" floor. Load-bearing: neutered needles leave
   every other counter empty, and no other prong fires.
3. **P3 row-beyond-EOF fold (H1's truncation sibling; landed inside G19 via
   `max_end`, `:491/499-505`)** — a readable file shorter than the maximum end
   of its declared rows makes those rows unevaluable (`"SKILL.md: %d lines <
   declared max %d (rows beyond EOF)"`). This closes 0-byte, truncated, and any
   shrink-through-a-declared-range file. Load-bearing: with a 0-byte or 5-line
   SKILL.md the floor still reads `current-ok=5`, so only this prong fails it.
   Design note: the planner's draft had this as a separate SCOPE-ERROR class
   (G21); the landed fold into UNREADABLE is one class instead of two, same
   fail-closed effect, and the report line names the cause verbatim. Accepted as
   the better form.

Merge decisions (vs the two upstream patch texts): RV-11's minimal diff is kept
in substance (`unreadable` capture + verdict conjunct + report line) but its
report line moved next to the SCOPE-ERRORS block and its class is also in JSON;
CR-5's floor is adopted in its stronger form (`> 0` without the "or
everything-clean" escape) and its G2 line extension is kept (`current-ok
loci=%d, total loci=%d`). Nothing was dropped from either text.

## 4. Exit codes and output contract (decided)

- Map UNCHANGED: **0 PASS, 1 FAIL, 2 anchor failure**. The new classes ride
  verdict FAIL + exit 1 and are named in `DECLARED FAIL CLASSES:` (text) and
  `declared_fail_classes` (JSON).
- Refused alternative A: reuse exit 2 for the new classes. It would give 2 two
  meanings (host-config anchor failure vs repo-file unevaluability) and change a
  map that the fleet's before/after harnesses (EX-11, EX-17, EX-21, RV-8, this
  seat's matrix) already read; the round-1 probe's "2 = could-not-evaluate" is
  that instrument's contract, not this one's.
- Refused alternative B: a new exit code 3. No consumer; the class name already
  carries the distinction.
- Output stability: the verdict line and the per-file `lines=/loci=` lines stay
  byte-identical at HEAD; the delta is exactly three added lines (UNREADABLE,
  G2 extended, DECLARED FAIL CLASSES) — `receipts/head-text-delta.txt`. The
  counts printer changed `%-4d`→`%-4s` (`:544`) so the readable-file rendering
  is unchanged while `None` renders without a crash.
- `--json` schema: 13 shared keys, all values equal at HEAD; three keys added
  (`unreadable`, `declared_fail_classes`, `g2_floor`) — `receipts/
  json-key-delta.txt`. Consumers computing over `counts` must tolerate `None`
  (contract note, §6/F2).

## 5. Fixture list (the matrix; before → after)

This seat's independent matrix (`tools/matrix.py`, output `receipts/matrix.txt`)
runs the v10 baseline copy and the landed snapshot side by side over the same
roots; EX-16's own before/after receipts cover the same classes with more
variants (`claims/c2/EX-16/receipts/{before,after}/`). The load-bearing set:

| Fixture | v10 | landed v11 | class that fires |
|---|---|---|---|
| HEAD root | PASS 0/0/0/0 exit 0 | PASS 0/0/0/0 exit 0 | — (parity) |
| SKILL.md absent | PASS exit 0 | FAIL exit 1 | UNREADABLE |
| SKILL.md 0 bytes | PASS exit 0 | FAIL exit 1 | UNREADABLE (rows beyond EOF) |
| SKILL.md truncated to 5 lines | PASS exit 0 | FAIL exit 1 | UNREADABLE (rows beyond EOF) |
| SKILL.md EACCES (chmod 000) | PASS exit 0 | FAIL exit 1 | UNREADABLE (PermissionError) |
| SKILL.md is a directory | PASS exit 0 | FAIL exit 1 | UNREADABLE (IsADirectoryError) |
| PROVINCE.md / SCORECARD.md absent | FAIL (marker uncheckable) | FAIL + UNREADABLE | class added, verdict unchanged |
| needles neutered (PIN+VER+PTR) | PASS exit 0 | FAIL exit 1 | BLIND-INSTRUMENT |
| REA_GATE narrowed | PASS exit 0 | FAIL exit 1 | BLIND-INSTRUMENT |
| all three files absent (empty root) | FAIL (markers) | FAIL, classes [UNREADABLE, BLIND-INSTRUMENT] | both |
| PIN narrowed (weak pin) | PASS exit 0 | PASS exit 0 | none — residual H4/partial blindness |
| 7 historical trees (RV-11 scratch) | 6 FAIL / 1 PASS | identical verdicts | none — no verdict flips |

EX-16's receipts extend the set: `h3-blind-pin` (PIN alone neutered → PASS,
quantified in `residual-partial-blindness.txt`: 50 pin-assertions → 0 with loci
> 0), `w1/w2` instrument self-widening (H4; certificate path), and the round-1
t0-t6 injection battery re-run (`SUMMARY-after.txt`) with t5-dated-shelter still
PASS on both sides (H2/H5 family, named).

## 6. As-built findings (deltas vs the design and vs the claim text)

- **F1 (CLOSED at r4)** — the v9 title/usage nit this seat reproduced at r1/r3
  (then `:95` "…instrument v9 (E22…) — FINAL." and `:190` "Usage: python3
  c1-census-v9.py") is fixed in r4 `a4c16763…`: docstring B now reads "C1 census
  instrument v10-r9 …" with an explicit history note and usage
  `c1-census-v10.py`. F9 (the duplicated "Still named, NOT closed here"
  paragraph, `grep -c` = 2 at r4) remains open.
- **F2 (contract note)** — `counts` for an unreadable file is `{"lines": None,
  "loci": None}`. Documented in the landed header (`:60-61`) and in EX-16's
  `json-fields.txt`; the census's own printer and arithmetic guard it
  (`:522, :544`). Flagged for any *out-of-tree* consumer that assumes numeric
  counts.
- **F3 (token hygiene)** — the G2 text line prints `SUSPECT` while the declared
  class token is `BLIND-INSTRUMENT`; `UNREADABLE` prints as class + list. The
  round record (SCORECARD/LOG/verdict) should use the JSON tokens
  `UNREADABLE` / `BLIND-INSTRUMENT` so prose and machine output agree.
- **F4 (design confirmed)** — the row-beyond-EOF fold is independently
  load-bearing (fixtures 3-4 above): without it those two roots stay PASS.
- **F5 (residual, named)** — assertion-level blindness survives the floor:
  per-needle narrowing and content blanking that leaves `current-ok > 0` read
  PASS (cD1b, h3-blind-pin, w1). H4 self-certification is exactly this class;
  the certificate is the external audit, demonstrated green on the landed diff
  (§7). No claim is made that v11 detects narrowing.
- **F6 (unit boundary, unchanged)** — H5 gate-free version statements are not
  loci in this instrument's unit; H2 inline-marker excusal (t5-dated-shelter)
  is untouched and stays named.
- **F7 (standing rule, extended)** — the file-length contract now cuts both
  ways: growth must not add undeclared loci, and a *shrink* below a declared max
  end fails UNREADABLE. Any future row retirement that shortens a file must
  re-key the scope table in the same commit (same rule, reverse direction).
- **F8 (attack surface left to verifiers, not closed here)** — (a) symlink swap
  of a scoped file to another readable file with `>= max_end` lines (G19 sees a
  readable file; loci would come from swapped content); (b) line-count-preserving
  content blanking inside declared rows (partial blindness, F5); (c) `--root`
  pointing at a tree where two scoped files are the same inode (not checked).
- **F0 (claim-breaking transient, resolved in the live revision)** — revision r2
  (`c95a5cf3…`) made the ordinary run FAIL: `G2 … SUSPECT (current-ok loci per
  file: PROVINCE.md=1, SCORECARD.md=4, SKILL.md=0)` → `DECLARED FAIL CLASSES:
  ['BLIND-INSTRUMENT']` → `VERDICT: FAIL`, exit 1, and EX-21's invariance read
  `BROKEN (3 diffs)` (exit, verdict, g2_ok). Cause: the per-file floor was
  counted in *block* dispositions while SKILL.md's only current-ok evidence sits
  inside an `info`-dispositioned mixed block. r3 (`df9ffdf9…`) re-based the
  count on *detections* and restores parity (13/13 shared JSON keys equal at
  HEAD). Evidence: `receipts/matrix-c95a5cf3.txt`,
  `receipts/head-text-delta.txt`; the r2 receipt pair is retained because an
  unreceipted transient would be indistinguishable from a rumour.
- **F9 (header hygiene, open, cosmetic)** — the final header still carries the
  "Still named, NOT closed here" paragraph twice (`grep -c` = 2) and docstring
  B's title/usage still read v9 (`:95`, `:190`). Fold into the same edit as F1
  if a re-land happens for any other cause; never re-land for cosmetics alone.
- **F10 (fixture added by r3, beyond the frozen claim)** — the per-file det
  floor closes `nullskill` (present, readable SKILL.md with all needles
  stripped): v10 PASS, r1 PASS, r3 FAIL `BLIND-INSTRUMENT`. This is stronger
  than the frozen claim asked; it redeems EX-14's strengthening proposal in its
  *det* form without adding the `EMPTY-SCOPE` class name. Record it in the
  SCORECARD bullet as an extra closure, not as claim scope.

## 7. Certificates (run by this seat, against the landed bytes)

Landed snapshots tested: r1 `82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa`
(560 lines, matches EX-16 `after-sha256.txt`) and **r3
`df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43`, 601
lines, the live file at write time**; the certificate runs below were repeated
against r3 (`receipts/matrix-final.txt`).

- `claims/c2/EX-21/scope-audit.py compare` — rows 20/20, ADDED 0, REMOVED 0,
  CHANGED 0, scope-literal sha256 `000b74e2…` identical on both sides, all 10
  detector constants `same`, `CREEP FLAGS: []` (`receipts/scope-compare-head.txt`).
- `claims/c3/CR-5/tools/scope-diff.py` — rows 20/20, flags `[]`, exit 0.
- `claims/c2/EX-21/scope-audit.py invariance … .` — INVARIANCE: HOLDS on all 10
  checked fields at HEAD (`receipts/invariance-head.txt`).
- HEAD text/JSON parity — `receipts/head-text-delta.txt`,
  `receipts/json-key-delta.txt`.

## 8. Handoff and remaining work

- EX-16: re-derive the after-receipts at the FINAL sha (r3, `df9ffdf9…`): the
  existing `after-sha256.txt` / receipts cite r1, and the r2→r3 revision landed
  after them (C1 rule-#14). Optional text nits F1/F9 only if the re-land happens
  for that reason.
- Parent/records commit: record the *final* instrument sha; re-run the census at
  the records commit after the SCORECARD section + LOG append; keep the appended
  block locus-free in the census unit (standing rule) or re-key in the same
  commit. Use the JSON class tokens per F3, and record F10 (nullskill) as an
  extra closure beyond the frozen claim.
- Verifiers (VZ-2/CR-2/CR-3/RV-3…RV-10): attack per F8; re-derive the floor
  fixtures; the before/after pair for the claim is (v10 `6f1d19ff…` PASS on the
  H1/H3 injections) → (**r3 `df9ffdf9…`** FAIL exit 1 with `UNREADABLE` /
  `BLIND-INSTRUMENT`); re-run any receipt captured against r1/r2.
- Blocker: none. Scratch used `/dev/shm/pl2` (repo untouched by this seat; the
  real target was written only by EX-16).
