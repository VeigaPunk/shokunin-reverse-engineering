# R40-C2 axis fit — pre-freeze attack (DRAFT `plans/round-40-claims.md` :69-99)

**DEFECTS FOUND** — R40-C2 is genuine depth *content* but its drafted target does not measure that content:
N/N on 13 published classes is reachable by a table with 7 non-`*` cells (executed, 20/20 on the frozen
round-39 set), and the draft's "block 18 stays byte-identical" requirement leaves **two live tables that
already disagree on committed Core evidence**, beside a third divergent copy of table v1 that mislabels
2 of the 20 frozen envelopes. Fixable before the freeze; no tradeoff requires rejection.

Lane revision read: `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`. No REA/unblob run, no carrier built or
touched; every measurement is committed bytes read with the frozen `tools/round-39/sqfs-triage.py`.
Artifacts: `.ufo/waves/round-40/w1/artifacts/R40C2AxisFit/` (index + hashes in its `README.md`).

## Answers

| question | answer |
|---|---|
| (a) depth move or re-scoring? | **Content: depth. Measure: not yet.** 9 of the 13 classes (18 of 26 envelopes) are classes the frozen v1 rule already decides (v1 scores 20/20 on the round-39 set; the 18/26 is a projection from class identity, not a score over round-40 bytes), and the depth proxy is a block count (18/18 → 19/19) that any 19th block reaches. |
| (b) does it fix the round-39 bounds? | **1 of 7 fixed, 3 partly, 3 not fixed.** Fixed: rows 5/8's excluded outcomes (partial, clean-empty). Not fixed: the saturated/shortcut proxy, the 7-cell reach, the distinct-decision metric. Partly: cause→action scoring, the mixed row (contradicted by the retained v1 table), the domain guard (intent right, mechanism wrong). |
| (c) can fewer non-`*` cells reach N/N? | **Yes — 7 cells, 20/20, executed.** Lower bound for any first-match table with L distinct labels is L−1 cells; a 15-cell table over the draft's own class list reaches 26/26 with **zero** non-load-bearing cells (simulated). |
| (d) two live tables? | **Yes, and worse: three copies exist today.** With both blocks live, the v1 interpreter still exits 0 and still decides K5 `escaping-symlink-removed`; the interpreter's embedded `TABLE_BLOCK` is a second, divergent copy scoring 18/20 on the same set. Byte-identity of block 18 is unnecessary — the r39 counter reads `SKILL.md` from git at `--rev`. |
| (e) separable from C1? | **Data-separable, rule-coupled.** C2's `avm-marker-be-dropped` row restates C1's marker rule (C1 :63-64 kill control (d) is the same mechanism inverted) and its action now contradicts the ground C1 moves to Core. Give the rule one owner (C1) and drop or scope the class. |

---

## (a) Is v2 a depth move under QUALITY 75 and prompt §6 item 9?

### What the bytes show

The depth axis in `SCORECARD.md` is `10 → 10`, observable `18/18 queue-drain rule blocks have resolvable
file/range citations`, with a self-declared limit: "**not** semantic correctness, generality, or fresh
execution". The axis is therefore saturated at its ceiling, and the round's measurable delta is a
*ratio* (18/18 → 19/19), not a score. Round 39 did the same (17/17 → 18/18, score 10 → 10).

QUALITY #75 is satisfied in the narrow sense: the depth surface ("the SKILL/corpus craft section and its
counting recipe") *is* the surface v2 moves — block 19 in `SKILL.md` `## Queue-drain craft` (section
`SKILL.md:81-347` at this revision). QUALITY #48's junk-row class is not: a nineteenth `- **` block whose
citations resolve reaches 19/19 whether or not its table decides anything new.

### Why N/N does not carry the depth claim

The draft's 13 classes vs the round-39 measured set:

| group | classes | envelopes | v1 already decides it? |
|---|---|---|---|
| carried | clean-be, clean-le, escaping-symlink-removed, in-tree-symlink-metadata, dep-missing-be, dep-missing-le, avm-marker-be-dropped, body-extractor-failure, no-squashfs-chunk | 18 of 26 | **yes** — measured 20/20 on `corpus/evidence/round-39/c2/heldout/` (`v1-baseline-and-cells.txt`) |
| new | clean-empty, mixed-symlinks, partial-body-failure, out-of-domain | 8 of 26 | no |

So 69 % of the drafted N re-asks a question the frozen rule already answers, and the only *new* labels
carry 8 envelopes. Prompt §6 item 9's sentence ("Re-scoring a rule the lane already holds on new
inputs … is quality work, never coverage or depth") is not literally met — v2 changes the rule, not just
the inputs — but the *measurement* is dominated by held ground, and (c) shows the measurement cannot see
the rule change at all.

**Fix (smallest safe):** split the target and gate the new part:
`matched_carried == 18` (regression floor) and `matched_new == 8` (the delta), reported separately in the
receipt; add one sentence to the SCORECARD depth row for this block giving the decision-content measure,
so the row's delta is not a block count (see §6 P1).

---

## (b) Round-39 closure bounds (`corpus/lessons/round-39-verifier-spotcheck.md` §2 R39-C2)

| bound (closure wording) | draft fixes it? | evidence |
|---|---|---|
| "the axis proxy was already saturated" | **no** | depth `10 → 10`, `18/18`; see (a). The target stays pass/fail at N/N. |
| "an 8-row table with 7 non-`*` cells also reaches 20/20" | **no** | executed: an 8-row, **7**-cell table reaches **20/20**, and all 7 cells are load-bearing (`min7-score.txt`, `min7-loadbearing.txt`). The draft's control "a 'best table + `*` default row'" (draft :97) names a *plausible* table, not the minimal one; the target still admits the minimal one. |
| "the `cause -> action` column is not scored" | **partly** | an `action` column is scored (:79), but (i) the "closed vocabulary" is defined nowhere and frozen nowhere, (ii) nothing says actions are unique per row, so two rows may share one and a swap is undetectable, (iii) the *expected* action is written by the same hand that writes the table in the same commit — the pair is a consistency check, not an independent prediction. |
| "the 20 envelopes contain 9 distinct predicate decisions" | **no** | the draft only makes the counter *report* "the number of distinct row decisions" (:81-82). Report-only is not a gate, and with replicates differing only in a non-decision feature the count equals the label count by construction — the 7-cell shortcut already yields `distinct_rows=8` = 8 labels. |
| "rows 5 and 8 exclude two measured outcomes" (D1 `full-be1-xz` damaged P>0; D2 `full-be-dirempty-gzip` clean P=0) | **yes** | `partial-body-failure (P>0)` and `clean-empty` enter the class list (:91-93). Measured that they are new: an H02 envelope with `files := []` falls to `unclassified` under v1 (`clean-empty-probe.txt`). **But** the draft gives `clean-empty` no action semantics, and "clean… nothing to fix" is the wrong action for an image with entries and no published file. |
| "mixed-symlink images (K5 and K6) get the `escaping-symlink-removed` label, whose action contradicts their own `unpublished-entry` gaps" | **partly** | the class and row enter (:77), but block 18 stays live and keeps giving the old verdict on the same committed evidence — measured on K5 (`two-tables.txt`, `k5-two-tables-label.json`). The fix is contradicted by the table the draft keeps. |
| "the interpreter labels non-firmware envelopes because it has no `operation`/`provider` guard" | **intent yes, mechanism unclear** | `tools/round-39/sqfs-triage.py` contains no reference to `operation` or `provider` (grep, 0 hits), so the guard is new code. Reachability measured: a committed envelope with `operation` rewritten to `inspect` gets `no-squashfs-chunk`, and one that still carries a squashfs chunk gets `escaping-symlink-removed` (`ood-probe.txt`). As *columns*, the guard adds two constant cells to each of the 12 authored rows (24 cells that decide nothing) — see §6 P4. |

Two more defects the closure does not cover and the draft inherits:

1. **The replicate rule is unrepresented.** Draft :81 requires "held-out classes whose two replicates
   differ in a non-decision feature", but the class list (:91-94) drops round-39's `version-minor-mismatch`
   — the only class that exercised it. Either re-add such a class or delete the bullet.
2. **`avm-marker-be-dropped`'s action is unsafe on R40-C1's new Core ground** (see (e)).

---

## (c) A table with fewer non-`*` cells reaching N/N

### Executed, on the frozen round-39 held-out set (real envelopes)

An 8-row table with **7** non-`*` decision cells replaces block 18's 8-row, **40**-cell table and scores
**20/20**, with `distinct_rows = 8` and **no** non-load-bearing cell:

| label | handler | gaps | deps | -be | symlink | files |
|---|---|---|---|---|---|---|
| `no-squashfs-chunk` | `none` | `*` | `*` | `*` | `*` | `*` |
| `dep-missing-be` | `*` | `*` | `sasquatch-v4be` | `*` | `*` | `*` |
| `dep-missing-le` | `*` | `*` | `sasquatch` | `*` | `*` | `*` |
| `avm-marker-be-dropped` | `*` | `*` | `*` | `no` | `*` | `*` |
| `body-extractor-failure` | `*` | `*` | `*` | `yes` | `*` | `*` |
| `escaping-symlink-removed` | `*` | `*` | `*` | `*` | `yes` | `*` |
| `in-tree-symlink-metadata` | `*` | `unpublished-entry` | `*` | `*` | `*` | `*` |
| `clean` | `*` | `*` | `*` | `*` | `*` | `*` |

(`min7-table.md`, `min7-score.txt`, `min7-loadbearing.txt`; rebuild with `mk-variants.py`.) It omits the
handler check on every failure row and the gap check on both extractor-failure rows — i.e. it does not
hold the rule the claim advertises.

### The general bound

**Any first-match table with L distinct labels needs at least L−1 non-`*` cells, and L−1 usually
suffices** (one distinguishing cell per non-default row; the default row may be all-`*` unless the
out-of-domain class forbids it). So N/N can never measure decision content beyond "one predicate per
label".

### On the draft's own class list [INFERENCE]

A 15-cell, 11-row table reaches **26/26** (label, action) pairs over the 13 drafted classes (2 replicates
each), with **0** non-load-bearing cells under the drop-the-cell test — because the draft's whole gate set
(N/N + distinct decisions + cell necessity) is satisfied (`min-table-sim.py`, `min-table-sim.txt`).
This is a simulation over feature vectors derived from the draft's class descriptions, not a score over
real envelopes; the executed 7-cell result above is the evidence.

### What actually forces depth: classes the author never published

The only mechanizable device left is a **held-out subset whose classes are not in the claims file** (the
QUALITY #69/#44 direction: fresh content whose expectation comes from the generation). Publish the class
*families* and the decision fields; freeze counts, not names:

> `n_published = 26` (13 named classes, 2 replicates), `n_unpublished >= 6` drawn by the same frozen
> generator from the same outcome space; `matched_unpublished == n_unpublished` gates, and a table fitted
> to the published 13 fails it.

Candidate unpublished classes that a shortcut table provably misses: LE body damage (BE=yes on
`squashfs_v4_le`), `missing-extractor-dependency` with both binaries absent, an unknown gap kind
(`unknown-chunk-handler`), a marker-holding image that extracts with files *and* carries a gap, and a
dependency miss with a published file (partial dependency failure).

---

## (d) Block 19 beside block 18: which table wins for a reader?

Nothing in the draft says (draft :71-73 only requires block 18 to stay byte-identical). Three measured
consequences:

1. **Two live graders.** With a v2 block appended and block 18 untouched, the v1 interpreter still parses
   its own table and **exits 0** (`two-tables.txt`). Its registry row (`SKILL.md:1351`) still advertises
   "labels REA envelopes", so a later reader or counter can satisfy a question with either table.
2. **A disagreement on committed Core evidence.** K5 and K6 are *mixed* (`SR=yes` **and**
   `G=['unpublished-entry']`, measured). v1 → `escaping-symlink-removed` (row 6); the draft's v2
   `mixed-symlinks` row "ahead of the escaping row" (:77) matches the same vector → `mixed-symlinks`. Two
   tables in one craft section give two verdicts for the round-39 C1 carriers, with no precedence rule.
   This is the QUALITY #77 shape: a second contradictory statement reachable at the same time as the
   scored one.
3. **A third copy already diverges.** `tools/round-39/sqfs-triage.py` embeds `TABLE_BLOCK`, emitted by
   `--print-table` and asserted by its own selftest. At this revision it differs from the SKILL table in
   **5 decision cells across 5 rows** (dep-missing-be/le `files` `*` vs `0`; escaping/in-tree/clean
   `handler` `squashfs_v4_*` vs `squashfs_v4_be`) and scores **18/20** on the frozen set, turning H03/H04
   (`clean-le`) into `unclassified` (`v1-table-two-copies.txt`, `tableblock-score.txt`). Adding v2 without
   consolidating makes a fourth copy.

**The byte-identity requirement is unnecessary.** The round-39 counter reads `SKILL.md` from git objects
at `--rev`/`--freeze` (`tools/round-39/c2-counter.py:205-206`), so the round-39 demonstration stays
reproducible at `8b9634ed` whatever live SKILL holds. And the depth count is a count of `- **` blocks, so
keeping block 18 as a block with its table replaced by a pointer still yields 19/19.

**Smallest safe correction**

1. `SKILL.md` keeps **exactly one** `<!-- sqfs-triage-table v* -->` marker, and it is v2. Block 18 stays a
   rule block with its prose; its *table rows* are replaced by one line: "Table v1 (frozen at
   `8b9634ed:SKILL.md:334-343`) lives in `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md`; where
   the two disagree the v2 table governs."
2. `tools/round-39/sqfs-triage.py`'s registry row changes to: description "superseded by
   `tools/round-40/sqfs-triage-v2.py`; labels only its embedded v1 table", verdict `2` on a SKILL without
   its marker (measured: `single_exit=2`, which is already the row's own "table missing/malformed"
   verdict, `SKILL.md:1351`).
3. The v2 counter asserts the marker is unique: `count('<!-- sqfs-triage-table ') == 1` and the marker is
   v2.
4. Resolve the embedded-copy divergence in the same round: either delete `TABLE_BLOCK`/`--print-table`
   (the selftest `c_print_table` then goes with it) or re-pin it byte-identically to the archived v1 rows.
   Leaving it as a third authority with a 2/20 error is the defect, not the duplication alone.
5. If the lane prefers keeping both tables live, the precedence line is the *minimum*, but it does not stop
   a reader from following block 18's `escaping-symlink-removed` action ("never materialise the link…"),
   so option 1 is the safe one.

---

## (e) Separability from R40-C1

Data-separable: C1 reads PROVINCE/README/SOURCES/knowledge/receipts/oracles; C2 reads SKILL, its
interpreter, generator and held-out evidence. C1's carriers (V1/V2, AVM-layout L1/L2) share no bytes with
C2's generated envelopes. But four couplings are real, one of them a contradiction:

1. **Same rule, two owners.** C1's kill control "a genuine AVM body with the marker stripped (unblob adds
   `-be`, extraction fails)" (C1 :63-64) and C2's `avm-marker-be-dropped` class are one rule used in both
   directions. A defect in the marker rule (`bytes_used == mkfs_time`) falsifies both claims at once, and
   both are scored in the same round. Fix: the marker rule has one owner — C1, which must cite it from
   source — and C2's rows cite C1's knowledge entry without re-deriving it.
2. **Contradictory action on new Core ground.** v1's row action (carried into v2 if unchanged) says: marker
   holds + no `-be` + failure → "rerun through a PATH wrapper named `sasquatch-v4be` that appends `-be`".
   After R40-C1 lands, marker-holding AVM-layout images extract *correctly without* `-be` (that is what
   makes them Core). The two outcomes are separated only by the body's metadata block-length endianness,
   which the triage table cannot see (it reads envelopes; none of the six fields carries it). So the row's
   action would break a genuine AVM-layout carrier, and the SKILL would hold two statements about the same
   marker condition. Fix: C2 drops the class (`Not claimed` already excludes genuine AVM-layout outcomes,
   :98) or scopes the action: "append `-be` only when the carrier's first metadata block length decodes
   big-endian; do not wrap a genuine AVM-layout body".
3. **Generator/writer coupling.** The held-out generator loads its writer by path, pinned in its manifest
   (`heldout-gen.py:119-148`; round-39's manifest pins `tools/round-37/gen-squashfs.py`). If round 40's
   generator switches to C1's new little-endian-block-length writer, a C1 writer bug breaks C2. Fix: state
   in P40-C2 that the writer stays `tools/round-37/gen-squashfs.py` at its pinned sha256, and that C1's
   writer is out of C2's read-set.
4. **The domain-guard class crosses both claims' vocabulary.** C1's `Not claimed` says "AVM
   kernel/`filesystem.image` wrappers beyond the carved member"; C2's out-of-domain class is "a
   non-`extract-firmware` REA operation on a SquashFS carrier". If the chosen operation is one C1 also
   runs on V1/V2 recon, the two claims would share an input class. Name the C2 out-of-domain operation as
   one C1 never runs (e.g. `inspect`), or generate it on a round-39 K copy only.

---

## Concrete predicate changes (drop-in for P40-C2, draft :84-89)

**P1 — split the target and gate the new part.**
> … assigns every held-out envelope the (label, action) pair its frozen generator assigned before any REA
> run — `matched_carried == 18` for the nine carried classes and `matched_new == 8` for the four new ones —
> and the receipt prints both counts separately.

**P2 — a class subset whose names are not published.**
> … **and** `matched_unpublished == n_unpublished` (`n_unpublished >= 6`, frozen as a count, classes drawn
> by the same generator from the same outcome space and not named in this file) …

**P3 — no default row; out-of-domain must match nothing.**
> … the table holds no row whose six decision cells are all `*` (a table containing one is refused, exit 2
> `default_row`), so an out-of-domain envelope reaches no row and is labelled `unclassified` …

**P4 — domain as a precondition, not 24 constant cells.**
> … the v2 block states once, before the table, `operation == extract_firmware AND provider.id == unblob`;
> the interpreter enforces that precondition before matching rows (exit 0 `unclassified`, not a row
> decision); no `operation` or `provider` cell appears in a row unless it distinguishes two rows …

**P5 — action vocabulary frozen and unique.**
> … every `action` cell is a member of the frozen vocabulary `tools/round-40/action-vocabulary.txt` (added
> in the freeze commit, before the table), no two rows share an action, and the receipt prints the
> vocabulary sha256 …

**P6 — cell necessity, reported and gated.**
> … the receipt prints `non_star_cells` and `non_load_bearing_cells`; `non_load_bearing_cells == 0` is
> required, and every cell the physics entails but no envelope witnesses is marked `entailed` in the
> source cell and excluded from the count.

**P7 — one table, one marker.**
> … `SKILL.md` contains exactly one `<!-- sqfs-triage-table ` marker, it is `v2`, and the block-18 prose
> states that v2 governs; the v1 interpreter's registry row is updated to `superseded` with the
> `table missing` verdict.

**P8 — drop or scope `avm-marker-be-dropped`** (see (e) 2), and re-add a replicate-varying class if the
draft keeps the :81 bullet.

## Kill controls to add (all actionable before data)

- **CTL-min-cell:** the 7-cell table in (c), scored with the frozen v2 counter — it must **not** reach the
  target. If it does, P1/P2/P6 are missing.
- **CTL-embedded-v1:** the current `tools/round-39/sqfs-triage.py --print-table` bytes transcribed as v2 —
  must fail (it is a real table with a measured 2/20 error, `tableblock-score.txt`).
- **CTL-two-tables:** a SKILL holding both markers — must exit 2 (marker not unique), not score.
- **CTL-every-cell-load-bearing:** the 15-cell draft-list table from `min-table-sim.py` — must fail on the
  unpublished subset (it passes the published one, 26/26).
- **CTL-action-shared:** a table whose two rows share one action string — must fail (P5).
- **CTL-default-row:** a "best table + all-`*` clean row" — must fail on the out-of-domain envelope (P3).

## Limits

- The executed 20/20 and the 18/20 embedded-copy score are measurements over the **round-39** frozen
  held-out set, not the round-40 set (which does not exist yet and must not be built here). They are
  evidence about the *instruments and tables*, not about round-40 data.
- `min-table-sim.txt` is a simulation over feature vectors I derived from the draft's class descriptions;
  a real envelope may differ (e.g. an `inspect` envelope's `normalized_result` shape). Marked
  **[INFERENCE]**, and the executed 7-cell result is the load-bearing evidence for (c).
- The `operation`-rewritten and `files := []` envelopes are lab rewrites of committed bytes, used only to
  exercise an interpreter that never reads `operation`/`provider`. They are not real REA envelopes and are
  not offered as claims about REA output.
- No REA and no unblob run was made in this seat; no C1 carrier and no C2 held-out carrier was touched.

## Hygiene

- Scratch `S=/fast/scratch/hyaku/kaidoku-r40/R40C2AxisFit` created, used with `TMPDIR=$S`, removed before
  this report was written (`rm -rf -- "$S"`); nothing cited above depends on it — every artifact is
  rebuildable from the lane plus `mk-variants.py`.
- No tool installed or upgraded; no VCS mutation; writes confined to this report and the artifacts
  directory.
