# CritCensus — attack on the R51-C2 registry-census re-derivation

Base `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab` (claims-draft commit). Declared claim base
`1aa27369` (round-50 spot-check). Both re-measured; every number below is identical at both
revs (verified). Scratch `/fast/scratch/hyaku/kaidoku-r51/w1-CritCensus`, removed at yield
after copying receipts. No REA run, no lane write, no git mutation in the lane, no install.

`Round-51-claims.md:183-186` states the defect: "`tools/round-48/census2.json` froze 42
registered-instrument paths; twelve instruments registered by M50-2's fix plus the round-50 C3
instrument make **13** registered paths the frozen census does not list". `:213-216` states the
fix: "a frozen re-derive command (ported from the `meanings.py` census surface) enumerates the
registered instrument paths from the registry markers at REV and reports `census_outside` =
registered paths absent from the active census artifact; the landing adds
`tools/round-51/census3.json` ... and the drift drops 13 → 0."

## Verdict

**The `13 → 0` closure is not re-derivable, and the "13" itself is a comparator artifact, not
the drift the claim names.** Three independent defects, each with a measured counterexample:

1. `13` counts registry rows against the **frozen `census2.json` artifact**, not against any
   re-derivation. The moment the comparator is the re-derived census the claim asks for, the
   count is **4** (claims-file rule extended) or **1** (directory rule), not 13. The predicate
   "at the declared base ... the same command exits 1 with ... `census_outside 13`"
   (`plans/round-51-claims.md:203`) is therefore **unreachable** for any instrument that
   implements the rule the claim specifies. The before-arm as written can only be produced by
   comparing against the artifact the claim replaces.
2. Landing `census3.json` **does not clear the frozen atom it is supposed to fix.** The frozen
   `tools/round-48/meanings.py` hard-codes `CENSUS = "tools/round-48/census2.json"`
   (`meanings.py:39`) and compares the registry against *that* (`meanings.py:441-442`,
   `failing` at `:441-443`). Measured at base: `meanings.py` already exits **1** with
   `registry rows outside the census: [13 paths]`. Adding `census3.json` leaves `meanings.py`
   reading `census2.json` — so the red stays. Measured in a scratch clone: after adding three
   round-51 registry rows, `registry_extra` = **16**, still red, `census_rederived_equal`
   true. The claim's own registry clause (`plans/round-51-claims.md:171-172`, every new
   `.py`/`.sh` under `tools/round-51/` gets one `instrument-registry v2` row) therefore
   **increases** the frozen atom's red count from 13 to 16+ at the landing.
3. The supersession is **unrecorded and unread**. `census3.json` "records which artifact it
   supersedes for which surface" (`:215-216`) — but no frozen consumer is repointed. The only
   frozen readers of a census artifact are `meanings.py` (hard-codes `census2.json`) and
   `tools/round-50/c2-record.py` (`census_paths()` at `:845-849` re-derives from
   `git ls-tree` at BASE/REV, never reading `census2.json` or `census3.json` at all). Nothing
   reads `census3.json`. The number 0 would be self-certified by the same code that writes it.

Full numbering and demanded fixes below.

---

## F1 (BLOCKER) — `census_outside 13` cannot be produced by the re-derive rule the claim names

The claim binds the count to a *re-derive* ("a frozen re-derive command (ported from the
`meanings.py` census surface) enumerates the registered instrument paths from the registry
markers at REV"). But `13` is the count against the **frozen artifact**, not against a
re-derivation.

Measured, identical at `1aa27369` and `f04b51dd` (command + stdout sha in
`receipts/measure.out`, sha256 `b6afbc7e8e0cd03a899a529c58ab84466a1a94111393135f15d1f7e55387c5e7`):

| comparator for "registered paths absent from the census" | base count |
|---|---|
| frozen `tools/round-48/census2.json` (42 paths) | **13** |
| census2's *rule* extended to rounds 41..51, restricted to paths present at REV | **4** |
| round-50's draft `census3.py` rule (claims 41..50 named ∪ whole-dir `tools/round-49/`, `tools/round-50/`) | **1** |
| census derived *from the registry markers* (what the claim literally says) | **0 by construction** |

Registry marker block = 55 rows; `census2.json` = 42 paths; `census2.json` ⊆ registry (0
missing), registry − census2 = 13 (6× round-49, 6× round-50, 1× `tools/round-50-c3/`).

The four-vs-thirteen gap is exactly the four paths no claims file names: `tools/round-49/`
`c1-controls.py`, `c1-oracle.py`, `c1-run.py` (named by no claims file) and
`tools/round-50-c3/sqfs-triage-v5.py` (named only in `plans/round-50-attempt2-claims.md`,
which is outside every `plans/round-{n}-claims.md` glob — the filename trap the round-50 seat
already documented as its `whole_directory_additions` finding).

**Consequence.** The predicate at `plans/round-51-claims.md:203` ("at the declared base
`1aa27369…` the same command exits **1** with `executability_violations 1` naming
`dmg_Z3_v3ddwrt_inode_table` and `census_outside 13`") is unreachable by an instrument
implementing the specified re-derive. The before-arm is only producible by comparing against
`census2.json` — the very artifact the landing replaces. A "13 → 0" pair where the before-arm
uses comparator A and the after-arm uses comparator B is not a measurement of drift closing;
it is a change of denominator.

**Demanded fix.** State the comparator explicitly in the claims and make the two arms
like-for-like. Either (a) the before-arm is `registry − re-derived census at base` and the
claimed before-number is amended to the rule's true value (**4** for the claims-file rule,
**1** for the round-50 draft directory rule — the L1 must pick one rule and state it), or
(b) both arms compare against the *same* artifact family and the claim states that the
before-number is 13 only because `census2.json` is the stale artifact, while the *rule-derived*
number is already 4/1 and the real defect is narrower than "13". Option (a) is the smaller
safe correction: amend the literal `13` in `:203` and `:186` to the number the stated rule
actually yields, and keep `census_outside 0` as the after-arm only if the after-arm uses the
same rule.

**Additional demand.** The re-derive rule must be *stated in the claims*, not left to the
implementer. The three candidate rules give 13 / 4 / 1 at base; "ported from the `meanings.py`
census surface" names `census2.py`'s rule (`census2.py:27-29`), whose `CLAIMS` glob
`plans/round-{41..48}-claims.md` and `TOOL` regex `tools/round-4[1-8]/…` are both
round-bounded and must be widened — and widening the glob to `plans/round-50-attempt2-claims.md`
(or a `plans/round-*-claims.md` glob) is required to ever reach `census_outside 0`.

## F2 (BLOCKER) — landing `census3.json` does not clear the frozen `meanings.py` red; the registry clause makes it worse

`tools/round-48/meanings.py` is a **frozen** atom (its bytes and its `SKILL.md`/census inputs
are the round-48 claim's surface). It hard-codes its census artifact:

- `meanings.py:39` `CENSUS = "tools/round-48/census2.json"`
- `meanings.py:40` `CENSUS_TOOL = "tools/round-48/census2.py"`
- `meanings.py:297-302` `census_rederive()` execs `census2.py`'s `census_text` from the bytes at REV
- `meanings.py:441-443` computes `registry_missing` / `registry_extra` against **that** document
  and appends `failing` when either is non-empty

Measured at base (`f04b51dd`, `--no-battery`, exit **1**):
`failing: ["registry rows outside the census: [13 paths]"]`, `registry_rows 55`,
`census_paths 42`, `census_rederived_equal true`, `registry_duplicates []`,
`registry_missing []`. This is the *same* 13 the claim calls the drift — but it is
`meanings.py`'s own clause-8 failure (R48-C1: "the marker-bound registry section's rows are
exactly the `tools/round-48/census2.json` path set"), not a number a new artifact can retire.

Scratch-clone experiment (a `git clone --shared` of the lane at base, detached at
`f04b51dd`, `git rev-parse --show-toplevel` asserted equal to the clone dir, `user.name`/
`user.email` set in the clone only, commits confined to the clone):

| probe | result |
|---|---|
| +3 synthetic round-51 registry rows in the `instrument-registry v2` block | `meanings.py` exit **1**, `registry_extra` **16**, `census_paths` 42, `census_rederived_equal` true, `frozen_path_changed []` |
| edit `census2.json` in place (add one path) | exit **1**, `census_rederived_equal` **false**, failing `committed census2.json does not equal a fresh derivation` |
| add a **second** `instrument-registry v2` marker pair | exit **1**, `registry/census malformed: registry markers doubled` |
| one row with an escaped `\|` in a cell | exit **1**, `registry/census malformed: registry row has 8 cells, not 7` |

So: adding `census3.json` leaves `meanings.py` reading `census2.json` and still reporting the
13 (plus every round-51 row the claim obliges). The claim's own registry clause
(`plans/round-51-claims.md:171-172`, and `:228-229` for C2) requires one `instrument-registry v2`
row per new `tools/round-51/` `.py`/`.sh` — **six or more** new rows are expected (v6
instrument, census re-derive tool, `c1-counter.py`, `c1-controls.py`, `c1-run.sh`,
`fetch-vendor.py`, `misroot-sweep.sh`). At the landing the frozen red becomes **19+**, not 0.

**Demanded fix.** The claim must state which of the two mutually exclusive worlds it is in,
and the L1 must be able to score both:

- **(a) Supersede-and-repoint.** The landing must repoint the *consumer* of the census to
  `census3.json` — i.e. `meanings.py` must read `tools/round-51/census3.json`, and
  `census2.json` must be regenerated/extended so that `census_rederived_equal` stays true.
  This changes a frozen round-48 file, which the round-48 claims forbid to amend; the L1 must
  therefore amend the R48-C1 clause-8 surface explicitly and say so in the claims and the
  amendment record.
- **(b) Add-only.** `census2.json` and `meanings.py` stay byte-frozen; `census3.json` is a
  *new* census for a *new* surface. Then the R48-C1 atom stays red (13 → 19+) **by
  construction**, and the claim's `census_outside 0` measures only the new surface. The claims
  must then say plainly that R48-C1 is knowingly left red — the round-50 claims already
  disclose the same pattern at `plans/round-50-claims.md:35-38` ("added rows in the
  `instrument-registry v2` block of `SKILL.md` are rows outside the frozen round-48
  `census2.json`; both older counters were verified at their own revisions and are not re-run
  as gates this round"). R51 cannot inherit that disclosure silently while claiming to close
  the drift.

(b) is the smaller safe correction. Under (b) the claim must also drop the assertion that the
13 is "the drift" for R48-C1 — it is R48-C1's *known, disclosed* red.

## F3 (MAJOR) — the supersession record has no reader and no authority

`:215-216`: "The frozen round-48 census bytes stay untouched; `census3.json` records which
artifact it supersedes for which surface." A JSON field recording a supersession is not a
supersession — it is a comment about a comment. Nothing in the tree reads it:

- `tools/round-48/meanings.py:39` — hard-codes `census2.json`; it never opens `census3.json`.
- `tools/round-50/c2-record.py` — its `census_paths()` (`:845-849`) re-derives from
  `git ls-tree` at `BASE`/`REV` under `CENSUS_BASE_PREFIX='tools/round-49'` /
  `CENSUS_REV_PREFIX='tools/round-50'` (`:143-144`); it reads **no** census JSON at all. So
  the frozen round-50 calibration atom is unaffected by either artifact — and equally, it
  cannot corroborate the supersession.
- `tools/round-46/registry.py:38` binds `CENSUS = "tools/round-46/census.json"` — a third
  census artifact with a third scope (38 paths, rounds 41..46). The lane now has three census
  surfaces and no stated precedence among them.

Grep for consumers of a census JSON outside `.ufo/` returns only `meanings.py` (and prose).
There is no rule, marker, or row that names which census artifact is authoritative for which
surface.

**Demanded fix.** The supersession must be *enforced*, not recorded. Minimum: the claims name
the surface (`SKILL.md` `instrument-registry v2` block + `tools/round-48/meanings.py`'s
registry clause) and the artifact that serves it (`tools/round-51/census3.json`), the new
instrument's docstring and its `instrument-registry v2` row's pinned-value cell both name the
same path, and the predicate's before/after arms are computed against that one artifact so
the two arms are comparable. If the L1 intends (b) from F2, the supersession statement must
additionally name the surface that keeps reading `census2.json` (R48-C1's own clause 8) and
say that it is knowingly red.

## F4 (MAJOR) — `census_outside` is one-sided: it cannot detect the drift it is named for

`census_outside` = *registered paths absent from the census*. The converse — *census paths
absent from the registry* — is not counted. The frozen counter checks both
(`meanings.py:441-443`: `registry_missing` and `registry_extra`), and the round-50 calibration
atom checks both directions too (`c2-record.py:852-889` `b9()` walks census paths and requires
a registry row for each, with cell-count, kind-cell, entry-command, meaning-class, self-test
and pinned-value clauses per path).

A one-sided metric is trivially satisfiable: a `census3.json` that lists **exactly** the 55
registry rows and nothing else scores `census_outside 0` while omitting every instrument the
rule would require. Measured: the round-50 draft rule at base yields 54 paths, of which
`registry − census` = 1 and `census − registry` = 0 — but that equality is a *consequence* of
the rule's whole-directory clause, not a checked property. A hand-written `census3.json`
listing the registry verbatim scores 0/0 and detects nothing.

**Demanded fix.** The predicate must require **both** directions (`registry_outside 0` and
`registry_missing 0`) and the counts must come from a rule-derived census, not from the
registry. Add the missing-direction control to the control list: a `census3.json` with one
extra path must be red. The claims' control list
(`:220-222`: do-nothing, junk table, audit-guard-deleted, swapped-new-row-action,
census-guard-deleted) has no "census artifact with an unregistered extra path" mutant.

## F5 (MAJOR) — generator-registered rows are missed by every named glob, and the count can silently double-count

Two independent miss-classes, both measured at base:

- **Miss — claims-file filename shape.** `tools/round-50-c3/sqfs-triage-v5.py` is named in
  `plans/round-50-attempt2-claims.md` and in `plans/round-51-claims.md:193` only. `census2.py`'s
  `CLAIMS` list (`census2.py:27`) is `plans/round-{n}-claims.md` for n in 41..48 — literal
  filename, no `attempt` variants. Any re-derive that keeps that shape silently omits the
  round-50 C3 instrument. This is the single path that survives even the round-50 draft's
  whole-directory rule (`tools/round-50-c3/` is not `tools/round-50/`), which is why that rule
  yields 1, not 0.
- **Miss — directory prefixes.** `git ls-tree -- tools/round-50` does **not** match
  `tools/round-50-c3/…` (verified: 0 hits). The round-50 draft rule's `WHOLE_DIRS` are
  `tools/round-49/` and `tools/round-50/`, so `tools/round-50-c3/` is invisible to it.
- **Double-count — the whole-directory clause and the named clause overlap.** The draft rule
  computes `present` as a set union of `{named ∧ present}` and `{whole-dir}` and separately
  records `whole_directory_additions = whole − named` — a set difference, so no literal
  double-count in `paths`. But `per_claims_file` counts *names per file* (census2.py:38-44),
  and a path named in two claims files is counted twice across those per-file maps while
  appearing once in `paths`. A metric computed as "sum of per-file counts minus registry
  rows" would therefore double-count; a metric computed as a set difference would not. The
  claims do not say which.

**Demanded fix.** The claims must (i) name the exact `CLAIMS` glob (including
`plans/round-*-claims.md` or an explicit attempt-list) and the exact directory prefixes
(including `tools/round-50-c3/` and `tools/round-51/`), (ii) state that `census_outside` is a
**set difference** over `paths` only (never a per-file sum), and (iii) name the
`named_but_absent` treatment for paths named but not yet present at REV (measured: 6 such
paths at base — the round-51 tools). Without (iii) the after-arm count depends on whether
absent-but-named paths count as outside, which the claim never fixes.

## F6 (MINOR) — two registry parsers disagree; the census tool must pick one and say so

The lane has two frozen readers of the `instrument-registry v2` block and they are **not**
equivalent:

- `tools/round-48/meanings.py:183-198` `registry_rows()`: splits on `|` with **no** escape
  handling (`_cells`, `:159-160`), and **raises `Malformed` on any row whose cell count ≠ 7**
  (`:193-194`) → the whole registry clause fails (`registry/census malformed`).
- `tools/round-50/c2-record.py:828-842` `registry_region()` + `:342-345` `cells()`: **does**
  handle `\|` escapes (via `\x01`), and tolerates any cell count at parse time (the 7-cell
  requirement is enforced later, per-path, in `b9()`).

Measured divergence, one synthetic row containing an escaped `\|`:
`meanings.py` sees **8** cells and fails the whole registry clause; `c2-record.py` sees **7**
and proceeds. Measured second divergence: `c2-record.py` requires the kind cell to open
`gate|probe` (`c2-record.py:872`) — `meanings.py` has no kind check. So a `census3.json`
derived with one parser and validated with the other can disagree silently.

**Demanded fix.** The census re-derive tool must name the parser it uses and, if it does not
reuse `meanings.py`'s exact `registry_rows()`, must state the escape and cell-count semantics
it implements. New registry rows must not contain a bare `|` in any cell (the escape is
meaningful to one parser and fatal to the other).

## F7 (MINOR) — 39 registry rows live outside the marker block and are invisible to the census

`SKILL.md` has **100** `| \`tools/…\`` table-row occurrences (**94** unique paths) at
base; only **55** are inside the `instrument-registry v2` marker block. The other **39**
unique paths (rounds 30–39: `axis-fit-gate.py`,
`c1-sqlite-positive.py`, `freeze-integrity.py`, …) sit in earlier, unmarked sections. Every
marker-scoped re-derive (the claim's "enumerates the registered instrument paths from the
registry markers at REV") sees 55, not 94. Round-50's seat found the same structural fact
under a different name (its F3: "the marker pair … is the real scoping device").

This is not itself a defect (the marker scope is the registry by house rule), but the claims
should say *which* scope the census covers, because "the registry" is ambiguous between 55 and
94 rows and the `census_outside` count depends on it.

**Demanded fix.** One sentence in the R51-C2 census bullet naming the scope: "the
`<!-- instrument-registry v2 -->` … `<!-- /instrument-registry -->` region of `SKILL.md` at
REV (55 rows at base; the 39 unmarked `tools/` rows of rounds 30–39 are out of scope)".

## F8 (MINOR) — the claim's arithmetic on the origin of the 13 is wrong by one

`:184-186` says "twelve instruments registered by M50-2's fix plus the round-50 C3 instrument
make **13**". Measured: the marker block goes 42 → **54** at commit `11ccdb72` ("round-50:
R50-C2 landing … registry rows") and 54 → **55** at `1439dfe9` ("round-50: C3 freeze+landing …
registry row"). So the round-50 C2 landing added **12** rows and the C3 landing added **1**,
total 13 — the claim's arithmetic is right, but its attribution is inverted: the 12 come from
the **round-50 C2 landing**, not from "M50-2's fix" as a separate earlier act. Minor; worth
correcting in the claims because the L1 will cite this sentence in the SCORECARD row.

---

## Not run / limits

- No REA invocation, no `--data-run`, no network fetch, no install, no tool upgrade.
- No write to the lane tree except this seat's own directory and report; the scratch clone was
  created with `git clone --shared` at `/fast/scratch/…/clone`, detached at `f04b51dd`, and
  every commit in it asserted `git rev-parse --show-toplevel` == that clone dir. Nothing in
  the lane repo was mutated; `git status` in the lane was not run (read-only `log`/`show`/
  `ls-tree`/`cat-file` only).
- `tools/round-48/meanings.py` was run with `--no-battery` only; the 4-forgery battery was not
  run, so the `met_target` values above are "structural clauses only".
- `tools/round-50/c2-record.py` and `tools/round-50/selftest-r49-c2.py` were **read**, not
  executed; no receipt for their runtime behaviour is claimed.
- The "after" numbers (16, 19+) are extrapolations from a 3-row synthetic probe, measured, not
  simulated at the real landing; the real count depends on how many `tools/round-51/` `.py`/
  `.sh` files land.
- `disk-guard.sh status` exit 0 before the heavy pass (`/tmp` 24%, `/var/tmp` 41%,
  `/fast/scratch/hyaku` 47%).

## Receipts

All under `.ufo/waves/round-51/w1/CritCensus/receipts/`. Each entry carries the exact
command, exit code, stdout sha256 and UTC time; `measure.out` is the load-bearing one.

| file | what |
|---|---|
| `measure.out` | the four-comparator table at both revs (sha256 `b6afbc7e…87c5e7`, exit 0, 2026-10-30T05:22:37Z) |
| `measure.py` | the script that produced it |
| `meanings-base.json` | `meanings.py --no-battery` at `f04b51dd`: exit 1, 13 `registry_extra` |
| `meanings-ownrev.json` | `meanings.py --no-battery` at its own rev `2e785632`: exit 0, 42 = 42, `failing []` |
| `meanings-synth.json` | +3 round-51 registry rows: exit 1, `registry_extra` 16 |
| `meanings-c2edit.json` | `census2.json` edited in place: exit 1, `census_rederived_equal` false |
| `meanings-dupmarkers.json` | second marker pair: exit 1, `registry markers doubled` |
| `meanings-escpipe.json` | escaped `\|` row: exit 1, `registry row has 8 cells, not 7` |
| `census3-draft.json` | round-50 draft `census3.py` run at base: 54 paths, exit 0 |
| `registry-rows.json` | marker-block row set, per-round breakdown, `census2.json` comparison |
