# ConnectorSibling — cross-lane pattern finding, round 80 wave 1

**Seat.** connector (leaf). **Mode.** read-only across sibling lanes; absorbed nothing, edited
nothing, ran no VCS mutation. **Lane.** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
**Base.** `16dfa009bf143080dfcdfc5f9ec34bd359536d90`. **Declaration.** `84d68e90f8a1ea3a3a7f94a208695c21023c0472`
(guard for `plans/round-80-claims.md`).

**Structured receipt.** `.ufo/waves/round-80/w1/ConnectorSibling/receipt.json`
(`sibling_impls`, `delta`, `considerthese`, `overlap`).
**Measurements.** `.ufo/waves/round-80/w1/ConnectorSibling/measurements.txt` (M1–M10; every
number below is one of those runs).

**Axes.** calibration (R80-C1), freshness (R80-C2), depth (R80-C3). This report finds one bounded
move on freshness and files five implementation findings the other seats need before their
predicates are reachable.

---

## 1. What the fleet already has

Searched `*/tools/` and `*/scripts/` across all 21 lane roots for `provenance`,
`instrument.sha256`, `word boundary`, `duplicate key`, `sole_detector`, `guard`, `clause`, then
read every hit that concerned a receipt sweep, a token matcher or a clause/case binder. Fourteen
implementations are load-bearing enough to compare; the rest are unrelated uses of the words
(`add_mutually_exclusive_group`, `flock(2) exclusive`, prose "guard", CJK clause splitting in
`chousa/tools/inference-ground.py`).

**Fleet-level answer to the seat's question.** All three patterns exist in sibling lanes, but
none of the three round-80 rules is a copy of one:

| pattern | exists elsewhere | closest sibling | what it is not |
|---|---|---|---|
| receipt-provenance sweep | **yes**, four times | `chousa/tools/digest-in-tree.py` | path-agnostic; one receipt; no control split |
| exact-token / word-boundary matcher | **yes**, four times | `kama/tools/round74-receipt-claim-binding.py:82` | hex alphabet only; paragraph claims, not record cells |
| clause-to-case binding | **no** | `kama/tools/round75-survivor-probe.py` | mutants → hardcoded arms, never → a document table row |

A fleet-wide grep for the round-80 marker convention
(`<!-- round-80 receipt-guard table: begin -->` / `table: end -->`) returns **only this lane's own
round-80 files** (`gen-w1.py`, `l1/guard-table-draft.md`, the dispatch JSON). No sibling has a
delimited decision-table block, let alone a binder for one.

## 2. Sibling implementations (path · rule · scope)

| # | path | rule | scope |
|---|---|---|---|
| 1 | `chousa-shokunin/tools/digest-in-tree.py` | every 64-hex pin in one receipt must equal the sha256 of a blob committed at `--revision` (or `--all-objects`); the matched **path is printed, never matched**; no pin → exit 2 `NO_DIGESTS` | one receipt; any 64-hex token; path-agnostic |
| 2 | `chousa-shokunin/tools/receipt-pin.py` | `SHA256=<64hex> <path>` header must equal `git cat-file blob REVISION:PATH`; header `REVISION` must equal the caller's `--revision` | one receipt, one caller-named revision; digest and path adjacent in one header line |
| 3 | `tameshi-shokunin/tools/receipt-window.py` | `instrument_sha256` must be lowercase 64-hex and a member of the contract's frozen/installed/historical set, with an edit-window ordering on `measurement_interval` | receipt batch vs one `contract.json`; **membership, not byte re-derivation** |
| 4 | `tameshi-shokunin/tools/receipt-measure.py` | frozen `FROZEN_GATE_SHA` / `FROZEN_MEASURE_SHA` literals + a digest→name table for four historical instruments | its own round-20 instrument identity |
| 5 | `kama-shokunin/tools/citation-provenance.py` | `cite(<rev>, <path>, sha256=<hex>)` tokens must equal `git cat-file <rev>:<path>`; missing and mismatching rows counted apart | registry-required rows × nominated documents |
| 6 | `kama-shokunin/tools/digest-ledger.py` | every cited 64-hex classified against a rev/dir blob set via a committed ledger; classes include `external` and `unverifiable` (+required note) | whole-lane `.md`/`.tsv` population, `.ufo/` excluded; **classification, not only acceptance** |
| 7 | `kama-shokunin/tools/round72-receipt-tip-binding.py` | cited receipt must carry `# tip=`/`# rev=`, name an ancestor of the tip, and `<rev>..<tip>` may touch only declared record paths; **exit 2 rather than a silent 0** | one round's self-record citations, read at `--tip` |
| 8 | `kama-shokunin/tools/round74-receipt-claim-binding.py:82` | `(?:^\|[^\w-])(?:#\s*)?(?:tip\|rev)=([0-9a-fA-F]{40})(?![0-9a-fA-F])`, `re.I`; paragraph-scoped claim grading | 40-hex revision tokens in a self-record; **hex alphabet only** |
| 9 | `kama-shokunin/tools/round75-survivor-probe.py` | five named source mutations on a copy; pristine green, every mutant red, each mapped to one named arm; `sole_detector` = exactly one failing case | one target module's `--selftest`; arms hardcoded in the tool |
| 10 | `kumitate-shokunin/scripts/routed-ledger.mjs` | quote binds by `(^\|[^A-Za-z0-9])quote([^A-Za-z0-9]\|$)` with ≥3 words and uniqueness per section; answers at the exact named line; `ROW_CONTRADICTED` **skips** a second non-open row | routed ledger rows, quotes, answer paths |
| 11 | `kake-shokunin/scripts/citing_set.py` | token `^S[0-9]{3,}$`; a range needs `\b` before the left `S` and `\b` after the right digits; an unreachable population id is rejected, not measured clean | citation ids in a population-bounded set; **endpoint-contextual** boundary |
| 12 | `tsukuroi-shokunin/tools/check-knowledge-refs-r68.py` | the frozen predicate is `S\d{3,}` with **no** word boundary; selftest `glued-ids-are-counted` asserts glued ids count | knowledge-ref ids; **opposite polarity, deliberately** |
| 13 | `kotodama-shokunin/tools/check-gate-battery.py` | isolated gate selftests in a mirror with before/after sha256 + path-set snapshots, then baseline validation (`gate_sha256` vs the live gate, input digests vs snapshot, 10/10 coverage) | ten registered gates + baselines; **no clause→row binding in the file** |
| 14 | `kotodama-shokunin/tools/check-gate-quotes.py` | quoted runs in `## Gate` rows must not exceed 25 words | prose only; the nearest per-row checker, still no code binding |

Two of these carry a rule the fleet has converged on twice and this lane's round-80 claims do not
state: **an empty or uncollected population must fail closed, not pass.**
`digest-in-tree.py:21-23` (`NO_DIGESTS`, exit 2) and `round72-receipt-tip-binding.py:20-26`
("never a silent 0 — S052: a check that collected nothing cannot pass").

## 3. Delta — what this lane adds, what it lacks

### R80-C1 (calibration)

**Adds.** (a) The only **duplicate-declaration** rule in the fleet that keeps the population
honest *and* names the duplicate: `checks_total` counts both cells and the id lands in
`duplicates`. Every sibling refuses or collapses instead — `routed-ledger.mjs:343` skips the
second row (`continue`), `kotodama/tools/d2-typed-labels.py:245-248,336-338` raises
`P-DUPLICATE-KEY` and refuses the parse, `kama/tools/round45-claim-outcome-audit.py:216-217`
labels the repeat `duplicate key` on an outcome row. (b) A delimiter class shaped like a **token
alphabet** (`[A-Za-z0-9._-]`) rather than like `\w`: `.` and `-` stay inside a version pin, where
`round74-receipt-claim-binding.py:82`'s `[^\w-]` would treat `.` as a delimiter. (c) A scored
**do-nothing control** (`control_false_greens 4`) beside the candidate; no sibling scores a weak
control on the same fixtures.

**Lacks.** `+`. The version alphabet is `[0-9A-Za-z.-+]` and the class omits `+`, so

```
True   semver build +build.5   | args = [ "-y", "rea-agents@6.7.0+build.5", "mcp" ]
```

a declared pin binds a longer live token — precisely the class the claim exists to kill (M5).
Adding `+` changes none of the four frozen red cases and neither green control, but the fixture
set is frozen at the declaration, so this is a round-81 fixture class, not a repair. Also absent:
kumitate's uniqueness requirement (not a defect — different subject) and any relaxation of the
left boundary (`x-rea-agents@6.7.0` refuses here, which is correct for a package pin).

### R80-C2 (freshness)

**Adds.** (a) **Path binding.** `digest-in-tree.py:160-171` scans `for oid, path in blobs: if
computed[oid] == want` and never matches `path`, so a receipt pinning a *different* committed
file's digest passes it; R80-C2 fails that receipt because the digest is not of its declared
`instrument.path`. That dimension exists in no sibling. (b) A population sweep with a declared
exclusion, an expected-negative control (`prov-forged-instrument.json`) and an `unexpected`
counter that must be 0 — `receipt-pin.py` takes one receipt and one revision;
`citation-provenance.py` takes registry rows. (c) The three-leg acceptance order (declared rev →
branch tip → any committed revision of the branch) survives honest historical receipts while
failing worktree-only digests. Measured: `round-78/l1/scores/c1-at-tip.json` is **honest at its
own rev** (`961d5a23…` = blob at `51c08cda`, MATCH) and `round-79/l1/scores/c2-at-landing.json` is
**not** (`a0044c4c…` vs `91d23dad…` at `ed68cd0a`, and `a0044c4c` is not in the path's 2-blob
history) — so the flag is not a false positive and the rule is not over-strict (M2, M3).

**Lacks.** (a) `receipts 34` is **not reachable from the frozen surface sentence**: the literal
glob for rounds 60–79 excluding `/attacks/` returns **141** receipts, and 34 only under the
undeclared filter "carries `instrument{path,sha256}`"; **107** receipts drop out with no counter
(M1). (b) No exit-2 could-not-evaluate class, where all three committed-blob siblings reserve one
(`digest-in-tree.py:21-23`, `receipt-pin.py:12-16`, `round72-receipt-tip-binding.py:20-26`) — a
git failure can surface as `flagged N`. (c) No escape class for a legitimately unverifiable
instrument, where `digest-ledger.py` has `external` / `unverifiable`+note. No such receipt exists
in the current 34, so (c) is a forward limit only.

### R80-C3 (depth)

**Adds.** The **only** implementation in the fleet binding a document table row to a code clause
*and* a selftest case with a deletion proof. `check-gate-battery.py` binds baselines to gates and
has no clause→row relation; `round75-survivor-probe.py` proves mutation kills but against a
hardcoded arm dict; `routed-ledger.mjs` binds rows to quotes, not to code. Plus a bijection
constraint (no orphan row, no duplicate clause id, no two rows on one clause) that no sibling
table enforces, and a guard count taken from the source (`guards 9` from the nine
`defects.append` sites) so a tenth clause breaks the target visibly.

**Lacks / traps.**

1. **Four of the nine frozen "clause prefixes" are infixes.** The message is
   `f"{fixture.get('id')}: fixture dir mismatch"` (attack-gate.py:790, 792, 794, 797), so G03–G06
   render `rb01: …` and their clause text is *contained*, not prefixed:

   ```
   clause  startswith  contained_in_own   cross_containment: []
   G01  True   True
   G02  True   True
   G03  False  True
   G04  False  True
   G05  False  True
   G06  False  True
   G07  True   True
   G08  True   True
   G09  True   True
   ```

   A `startswith` matcher binds at most 5 of 9 and `bound 9` is unreachable. Containment binds all
   nine, and no prefix is contained in a second message, so containment + uniqueness is a clean
   bijection (M4).
2. **The case arithmetic is 8, not 9.** `SELFTEST cases=29 failures=0` today, and G05's case
   `red-validate-refused-no-reason` already exists at `attack-gate.py:921`. The frozen
   `pristine.cases 37` therefore fixes **exactly eight** new isolating cases; nine new cases report
   38 and violate the frozen value (M6).
3. **Do not reuse `sole_detector`.** `round75-survivor-probe.py:197-200` and round-79's
   `gate-mutation.py:197-200,255-259` require *exactly one* failing case. R80-C3 requires the
   declared case to fail, not to be the only failure; a seat that imports the stricter semantics
   will report survivors for clauses whose deletion also trips an aggregate case.

## 4. `considerthese/`

**`considerthese/` does not exist in this lane** (verified: `cd <lane> && ls -d considerthese` →
`No such file or directory`, exit 2). No unimplemented proposal can be named from it. The path is
absent, not empty — 17 of the 21 lane roots carry one (`kaidoku`, `kotodama`, `souji`, `tabi` do
not; M8). The nearest cross-lane substitute, kama's `considerthese/2026-10-25.md` proposal 1, is
already implemented as `kama-shokunin/tools/digest-ledger.py` and is cited above as provenance,
not adopted.

**The single line the report must carry:**

> `considerthese/` does not exist in this lane (verified: `ls -d considerthese` → absent, exit 2),
> so no unimplemented proposal can be named from it.

## 5. Overlap — who touches this lane's evidence surfaces

**Cross-lane round 80: none.** A grep for
`instrument\.sha256|l1/scores|receipt-provenance|pointer-bind|attack-gate` across the round-80
wave trees of kake, kama, kengaku, kotoba, kumitate, mado, mori and tameshi returns **0 lines**
(M9). No shared instrument path, no shared receipt, so nothing to route.

What exists is **defect-class convergence on different subjects**, which is worth knowing and not
worth merging:

- kama's round-80 C2 (`tools/round80-engine-pin-relations.py`) — a pinned ref must re-derive from
  a live/committed source, the register must cover every engine, every row's receipt must exist
  and be committed. Same shape as R80-C2, different population.
- kengaku's `SentinelReceiptsR80.md` — producer provenance (`LANE_TIP` vs the executed checkout)
  over its own receipts.
- tameshi's `T80W1R1/R2` — receipt re-derivation reviewers over their own rounds.

Three siblings read **pre-round-80** kaidoku surfaces read-only: kama `CN01Connector.md:40,43`
(round-41/50 oracle TSVs as substring hash collisions), kumitate `K80ConnectSiblings.md:102-108`
(round-50 `ExecTriageV5` bullet-scoped assertion), mado `R80ConnSiblings.md:58` (the waybar core in
`corpus/knowledge/2026-10-13-crash-evidence.md`). None touches a round-80 path.

**In-lane cross-claim coupling (L1 sequencing, not routing).** C3 edits
`tools/round-78/attack-gate.py` to add its eight cases. That file is the declared instrument of
**2 of C2's 34 receipts** — `round-78/l1/scores/c1-at-record.json` (`a86f6d4d…`) and
`c1-at-tip.json` (`961d5a23…`) — and both digests are committed blobs of the path (M2). C2 stays
green **only because its rule accepts a blob at any committed revision**; under a tip-only leg both
would flip and the frozen `flagged 1` would become `flagged 3`. Neither seat should "repair" those
receipts, and the C2 seat should not narrow the leg to the tip.

## 6. The one move

**Make the R80-C2 receipt describe its own population.** Print the predicate and three counters —
`receipts`, `excluded_no_instrument`, `excluded_attacks` — and have `--validate` re-derive all
three from the receipt's own file lists.

- **Axis.** freshness. The rule is sound; the *number* is not reproducible. A sweep can score
  `receipts 34` correctly while 107 matching receipts sit outside a class it never states.
- **Why non-obvious.** No sibling prints an *excluded* count beside an *included* one.
  `digest-in-tree.py` prints `MODE=… SCANNED_BLOBS=<n>`; `digest-ledger.py` prints ledger class
  counts. The move is a synthesis of chousa's counter discipline and kama's classification
  discipline, applied to the exclusion dimension neither has.
- **Harm check.** Target arm unchanged (`receipts 34`, `flagged 1`, `expected_control_flags 1`,
  `unexpected 0`); base arm unchanged (`flagged 2`, `unexpected 1`); no claim text, no fixture and
  no other counter changes. The receipt gains two integers and one sentence.
- **Risks.** `--validate` must re-derive the new counters from the receipt's own lists or they
  become unvalidated prose (the C2 kill rule already forbids a `--validate` defect); a future
  population change becomes louder, which is the point; an empty population still exits 1, so
  F3's exit-2 class should land in the same edit.
- **Verification.** Run at base `16dfa009` and at the measured rev: expect
  `receipts 34 excluded_no_instrument 107` on both, `flagged 2`/`unexpected 1` at base,
  `flagged 1`/`unexpected 0` at target, `--validate` defect-free. `receipts 141` means the filter
  was not applied; `excluded_no_instrument 0` means it was applied but not counted.

## 7. Findings the seats need (routing)

| id | claim | kind | one line |
|---|---|---|---|
| F1 | C1 | limit | `+` is outside the delimiter class, so `6.7.0` binds `6.7.0+build.5`; round-81 fixture, name it in the lesson |
| F2 | C2 | reachability | literal surface = 141 receipts; `receipts 34` needs the undeclared `instrument{path,sha256}` filter; 107 uncounted |
| F3 | C2 | risk | no exit-2 class for environment faults; all three sibling committed-blob tools reserve it |
| F4 | C3 | trap | G03–G06 are infixes; `startswith` caps `bound` at 5; containment + uniqueness binds 9 unambiguously |
| F5 | C3 | arithmetic | pristine = 29 today; the frozen 37 means **8** new cases, not 9 (G05's case already exists) |
| F6 | C3 | risk | round-79's `sole_detector` must not be reused; R80-C3 needs the declared case to fail, not to be the only failure |

## 8. Limits of this report

- Nothing was executed against a candidate `tools/round-80/*` (no such file exists yet); C1/C2/C3
  deltas are read from the frozen claim text, the frozen fixtures, the committed source and the
  receipts, not from a candidate's output.
- The C2 target numbers (`receipts 34`, `flagged 1`, `unexpected 0`) were **not** re-measured —
  no sweep exists. What was measured: the population composition (M1), the committed blob sets
  (M2), and the declared-rev leg on two receipts (M3).
- The C3 mutation kills were **not** re-measured; `MutInstruments`/`ReviewerC3` own that. What was
  measured: the pristine count and the containment matrix (M4, M6).
- One `--selftest` run used scratch `TMPDIR=/fast/scratch/hyaku/kaidoku-r80/ConnectorSibling/tmp`
  and wrote nothing to the lane; the scratch tree was removed after the measurements and before
  yield. No fixture repo was created. No tool was installed (none needed; pacman pause respected).
- Sibling reads were at whatever revision each sibling worktree was at when read; their round-80
  waves were mid-flight (kama, kengaku, tameshi all had live w1 output). Line numbers in §2 are
  therefore checkable but not pinned to a sibling commit.
