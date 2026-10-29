# R50-C3 landing draft — table v5 (SKILL.md rule block 22)

**Status: DRAFT for the L1 to review and land. Nothing here is landed by this seat.**
Seat: `ExecTriageV5` (round 50, attempt 2, wave 3, build). Base revision: the **declared
base `f890bbead20ca2c549487167f56876ae47f1e1a4`** (per the claim's frozen rule details),
not the older `8ccc05e6…` — see §5.1. No lane tracked file was written by this seat.

The instrument is at `tools/round-50-c3/sqfs-triage-v5.py`, tracked in the lane by the
L1, with this seat's final bytes as a working-tree modification for the C3 freeze commit
(the committed version predates the receipt gate, the predicate constant and two
selftest cases — see §3). The **table** is what still needs landing.

---

## 1. The SKILL.md rule block 22 text (paste-ready)

The v4 table (rule block 21) stays where it is, as history. Rule block 22 is a **new**
dated block that supersedes it for the three families with no validated complete
independent oracle.

Paste the following as a new numbered rule block in `SKILL.md`. The marker and the
vocabulary line are part of the block: the parser reads the marker, then the vocabulary
line directly above the table, then the table.

```markdown
- **22. SquashFS outcome triage v5: the three families with no validated complete
  independent oracle get their own labels (round 50).** Rule block 21's table v4 stays as
  history; this block supersedes its routing and action columns for
  `squashfs_v2_nonstandard`, `squashfs_v3_broadcom` and `squashfs_v3_nonstandard`, the
  three SquashFS handler families with **no validated complete independent oracle**
  (round-49 `w2/W2Skill.md` F1, F2; the round-49 landing fixed F3/F4/F5 only, and F1/F2
  were routed, not fixed). The reader census behind the split is in
  `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md:102-104`: on the healthy `v2ns`
  fixtures `unsquashfs` 4.7.5 exits 1 and 7-Zip 26.04 exits 2, so for these families a
  cross-read cannot decide — reader failure is guaranteed by definition, not evidence of
  a damaged body. (`squashfs_v3_broadcom` has a PARTIAL reader: 7-Zip lists the committed
  LE fixture while `unsquashfs` refuses it, so it has no *complete* independent oracle; a
  no-reader FAILURE label never suppresses a successful partial cross-read.)

  Two defects in table v4 are repaired here. (a) The `legacy-body-failure` row's
  `failing handler` cell `squashfs_v[123]*` matches all three no-reader families, and
  the row's cross-read rule — "if the independent readers fail where sasquatch failed
  the body is damaged" — therefore condemns a **healthy** no-reader body (F1). Its cell
  becomes the comma-separated alternation `squashfs_v1,squashfs_v2,squashfs_v3,squashfs_v3_ddwrt`,
  matched as ANY-of-exact-alternatives (per-alternative `fnmatch`, so plain names are
  exact). (b) The `clean` row's action is `none` ("match files to the oracle by exact
  relative path and sha256"), and no oracle can exist for a family with none: the four
  committed v2ns `_ddefault` recon envelopes label `clean`/`none` today, contradicting the
  Frontier status those families hold in `PROVINCE.md` (F2). v5 gives them
  `clean-unverified`/`record-unverified` — uncorroborated, never clean.

  One grammar delta rides with the table: a handler-family cell may be a
  **comma-separated list of globs**, not only one glob. No single glob over the ten
  SquashFS handler names unblob 26.6.4 registers can express "the reader-backed v1-v3
  families": `squashfs_v[123]*` also matches the three no-reader families, and
  `squashfs_v[123]` drops `squashfs_v3_ddwrt`, which **is** reader-backed and must keep
  the legacy row. Every alternative is validated against the pinned ten-name vocabulary
  (a dead alternative makes the table malformed, never a silent non-match), a REPEATED
  alternative is refused, and the cell still matches when **any** alternative matches
  **any** member of the handler set — the same positive subset test the single-glob cell
  had. The `*` and `none` cells keep their meaning and may not be combined with other
  alternatives.

  The action vocabulary below is table v4's fifteen tokens plus `record-unverified` and
  `preserve-unresolved`. Two unmeasured boundaries are stated rather than hidden: a
  no-reader family that failed while publishing **more** than zero files keeps v4's
  `partial-body-failure`, and a no-reader family whose tree is empty keeps v4's
  `clean-empty` — the claim defines exactly two no-reader labels, so those two shapes are
  left on the v4 rows and named here rather than silently re-labelled. Every
  reader-backed family (`squashfs_v1`, `squashfs_v2`, `squashfs_v3`, `squashfs_v3_ddwrt`,
  `squashfs_v4_le`, `squashfs_v4_be`, `squashfs_v4_broadcom`) keeps its v4 label and its
  v4 action, unchanged.
```

…followed by the marker, the vocabulary line and the **17 table rows**, verbatim from
`receipts/v5-table-draft.md` (which also carries the marker and the vocabulary line).

**Do not hand-edit the table rows.** They are in `receipts/v5-table-draft.md` and are
embedded in the instrument (constant `V5_ROWS`); `--print-v5-block` prints the whole
block. Paste that verbatim so the shipped table and the instrument's draft cannot drift.

**Placement note.** The instrument finds the `<!-- sqfs-triage-table v5 -->` marker
ANYWHERE in the document (it does not require the craft section), so the block may land
inside the craft section or as a standalone rule block. Both placements were measured
(seat report F3): exit 0, `pair_mismatches 0` either way.

---

## 2. The instrument-registry v2 row — NOT MINE TO LAND

**Use `ExecRegistryRow`'s row, not the one below.** They measured that my cell 3 fails
`c2-record.py`'s own `re.match` (a cell that opens with a backtick does not match the
`<interpreter> <path> … --selftest` shape), while theirs passes; their row is
`.ufo/waves/round-50/w3/ExecRegistryRow/row-final.txt` (sha256 `3cce0727…`) and it is the
one the L1 has in `SKILL.md`'s registry. Their one open item was my case count/exit code,
which is now measured: **`--selftest` -> 18 cases, pass 18, fail 0, exit 0** at the final
bytes (`receipts/selftest.txt`).

My row is kept below only as a marked placeholder, and it is NOT the paste source:

```markdown
| `tools/round-50-c3/sqfs-triage-v5.py` | gate — R50-C3 depth: labels REA extract-firmware envelopes against the SKILL.md triage table v5 and compares every pair against the fixed R50-C3 evaluator; the two new labels `clean-unverified` and `no-reader-failure` and the narrowed `legacy-body-failure` failing-handler cell are what it measures, and it never invokes REA or reads a carrier | 0=met: `pair_mismatches 0` and `evaluator_missing 0` on every envelope of the held-out dir, the table label equals the evaluator label on every envelope, and --selftest is green; 1=not met: at least one pair mismatch, or the base revision does not exit 1 with the four `v2ns *_ddefault` rows among the mismatches; 2=could-not-evaluate: unknown revision, missing or refused triage table, unreadable envelope, freeze not an ancestor of the revision, or a work/output directory on a temporary partition | `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest` (18 cases, pass 18, fail 0, exit 0 at the freeze) | the `<!-- sqfs-triage-table v5 -->` block in `SKILL.md` rule block 22, read at a named revision by `git show REV:SKILL.md`; the evaluator precedence is the claim's, in the instrument, not in the table | stdout plus the `--json-out` receipt | kaidoku |
```

---

## 3. What the C3 freeze commit must carry

Per `plans/round-50-attempt2-claims.md` §R50-C3, the C3 freeze is ONE commit carrying:

1. `tools/round-50-c3/sqfs-triage-v5.py` — the instrument (evaluator + parser + selftest +
   the committed mutation battery). **The L1 must commit this seat's FINAL bytes**: the
   lane's tracked version predates the receipt gate, the `PREDICATE` constant and its
   receipt key, the H1 duplicate-alternative refusal, the predicate-pinning selftest
   case, the receipt-existence selftest case and the claim-consistency selftest case.
   `git status` shows the final bytes as a working-tree modification on the tracked file.
2. the instrument-registry v2 row (`ExecRegistryRow`'s);
3. the C3 section of `plans/round-50-attempt2-claims.md` (already present, amended at
   `d71829bf`).

**The path is `tools/round-50-c3/`, not `tools/round-50/`** — the L1's own path rule
(`03f852b9`, "Path rule (measured, not assumed)"): both frozen round-50 counters freeze
the WHOLE `tools/round-50/` tree, so a file added there reads as frozen-path drift and
takes C1 and C2 down. The instrument's own `INSTRUMENT_RELPATH` constant carries that
path, and its freeze arm reports the instrument's sha256 at FREEZE and at REV plus
`instrument_unchanged`.

**The table itself does NOT land in the freeze commit**: the table lands after the
freeze, so the frozen instrument is measured against a table that did not exist when the
instrument was frozen. That is what makes the do-nothing control meaningful.

**The L1 must run the C3 controls with the frozen instrument BEFORE the table lands**,
and commit the receipts. The instrument ships the control harness:

```bash
python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --controls \
  --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ \
  --json-out <OUT>
```

| control | expected (measured by this seat) |
| --- | --- |
| `do-nothing-v4` (the v4 table at the base revision) | RED on the corpus (19 mismatches), naming the four `v2ns *_ddefault` envelopes |
| `junk-table` (every row reads clean, unique labels) | RED on the corpus (126 mismatches); **exit 1, never exit 2** — measured as a semantic red (`receipts/junk-semantic-red.txt`) |
| `guard-row-deleted` (deletes `clean-unverified`) | RED on the corpus (19) |
| `new-row-actions-swapped` | RED on the corpus (19) |
| `legacy-glob-widened` | RED on the fixture scope (1); VACUOUS on the corpus — see §5.2 |
| `no-reader-failure-row-deleted` | RED on the fixture scope (1); VACUOUS on the corpus — see §5.2 |
| `no-reader-family-moved-to-clean` | RED on the corpus (7) |
| `precedence-order-swapped` | RED on the corpus (19) |
| `legacy-row-deleted` | RED on the corpus (7) |

Kill rule: if the do-nothing control is green, the instrument is broken — re-design
before data, never after.

**The receipt gate (the critic's requirement, now enforced by the instrument itself).**
The instrument now **re-reads its own receipt after writing it** and refuses (exit 2)
unless it parses and carries `predicate`, `pair_mismatches`, `evaluator_missing`,
`table_labels`, `n_envelopes` and `verdict`. The freeze gate should apply the SAME
check to the receipt it accepts: a 49-byte stub was measured exiting 0 on the full
predicate command while writing NO receipt at all (`--selftest` and the predicate
command both exited 0, stdout empty), so the exit code alone is not evidence — the
receipt is.

---

## 4. The two counting commands (the claim's predicate, unchanged)

```bash
# BEFORE (at the DECLARED BASE f890bbea…): must exit 1 with the no-reader `*_ddefault`
# rows among the mismatches — 19 of them (4 v2ns + 7 v3_broadcom + 8 v3_nonstandard).
python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root <LANE> --rev f890bbead20ca2c549487167f56876ae47f1e1a4 \
  --freeze <FREEZE> --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ \
  --json-out <OUT>

# AFTER (at the landing revision): must exit 0 with pair_mismatches 0.
python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root <LANE> --rev <LANDING_REV> \
  --freeze <FREEZE> --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ \
  --json-out <OUT>
```

Exit codes are semantic: 0 met, 1 not met (a pair mismatch), 2 could-not-evaluate.

**Note on `--freeze`.** The instrument verifies that FREEZE is an ancestor of REV (exit 2
otherwise) and reports, in the JSON receipt, the sha256 of the instrument file at FREEZE
and at REV plus `instrument_unchanged`. At the base revision the instrument file does not
exist yet, so those fields read `null` — expected, not a failure.

---

## 5. The disclosed limits the L1 must carry into the landing text

1. **The claim's own two bullets name different before-run revisions.** The "Counting
   command" bullet still says "before at `--rev 8ccc05e6…` (exit 1, ≥4 mismatches incl.
   the four v2ns `_ddefault` rows)", while the "Frozen rule details" bullets say the
   before-run `--rev` is "the exact declared base `f890bbea…`" and the expected
   before-state is the seat-measured **19** rows. **This seat's receipts use `f890bbea…`
   and 19**, following the frozen rule details, because that is the declared base and it
   is what the instrument was measured against. The two bullets must be reconciled in the
   claim file (the L1's to edit) — a selftest case (`claim_counting_command_is_consistent`)
   checks that the claim states the 19-row before-state and binds the before-run to the
   declared base, so the divergence cannot survive silently.
2. **The held-out corpus cannot witness the no-reader FAILURE branch.** The 126
   envelopes hold 38 no-reader envelopes: 19 clean (no gap, >0 files) and 19
   depth-limited, and **none** a no-reader `extractor-failure` with zero files. So the
   `no-reader-failure` row is unexercised by the held-out dir, and the two mutations
   that only move that branch (`legacy-glob-widened`, `no-reader-failure-row-deleted`)
   are **vacuous** on it. The instrument reports that honestly (each control carries a
   per-scope `red`/`vacuous` flag) and the selftest carries a committed SYNTHETIC
   zero-file no-reader extractor-failure envelope, so both mutations are red there and
   the `no-reader-failure` row/action is witnessed. The landing prose must say the row
   is selftest-measured, not corpus-measured.
3. **THE READER BOUNDARY IS FIXTURE-LEVEL IN THE CENSUS AND FAMILY-LEVEL IN THE RULE,
   AND THE RESIDUE IS EXPLICIT.** Re-measured byte-exact on the committed round-42
   fixture bytes (`receipts/reader-census.txt`): `squashfs_v3` 8/8 readable by both,
   `squashfs_v3_nonstandard` 8/8 no-reader, `squashfs_v3_broadcom` 7/8 **partial** (7-Zip
   lists it, `unsquashfs` refuses), `squashfs_v3_ddwrt` **6/7 no-reader**. A reader is
   therefore only trusted for the BODY VARIANT it was measured on, and the handler name
   cannot carry that distinction — the scored features do not expose a body variant. Two
   consequences, both disclosed, neither fixed by this claim:
   - **`squashfs_v3_ddwrt` stays reader-backed, and its FAILED body is the sharper
     residue.** `dmg_Z3_v3ddwrt_inode_table` (built from the ddwrt no-pad fixture, which
     both readers refuse) reads `legacy-body-failure`/`cross-read-legacy` — a cross-read
     prescribed on a body whose readers refuse. Its two CLEAN no-pad `_ddefault`
     envelopes read `clean`/`none` — an oracle-backed action with no oracle. Moving
     ddwrt into the no-reader set moves exactly those 8 labels and leaves
     `pair_mismatches 0` under both rules (`receipts/reader-boundary-whatif.txt`).
   - **`squashfs_v3_broadcom` has a working 7-Zip listing on 7 of its 8 fixtures**, so
     the no-reader wording is "no validated COMPLETE independent oracle", and a
     no-reader FAILURE label here never suppresses a successful partial cross-read. The
     instrument's docstring, its `NO_READER_FAMILIES` comment and the table's `cause`
     prose now carry that wording verbatim, and the `no-reader-failure` row's cause says
     explicitly that a partial reader that DOES list the tree is not suppressed by that
     label.

   **THE CLAIM MUST NAME THE ddwrt FAILED BODY (the L1's edit to `plans/`).** The claim's
   frozen-rule bullet discloses the ddwrt residue in general terms — "their known v4
   residue (reader-refused no-pad bodies) is unchanged by this claim" — but frames it
   around the two CLEAN no-pad `_ddefault` envelopes. The sharper case is the FAILED
   body, and the claim should name it. Suggested addition to that bullet:

   > its FAILED no-pad body `dmg_Z3_v3ddwrt_inode_table` still reads
   > `legacy-body-failure`/`cross-read-legacy` — a cross-read prescribed on a body whose
   > readers refuse — while its two clean no-pad `_ddefault` envelopes keep `clean`;
   > moving ddwrt into the no-reader set would move exactly those 8 labels and leave
   > `pair_mismatches 0` under both rules.

   The instrument's selftest case `claim_counting_command_is_consistent` reports whether
   the claim names that envelope, so the disclosure cannot go missing silently.
4. **Two no-reader shapes keep v4 rows.** A no-reader family that failed while publishing
   >0 files keeps `partial-body-failure`; a no-reader family with an empty tree keeps
   `clean-empty`. Both are unreachable in the held-out corpus.
5. **The evaluator and the table share the instrument.** The evaluator's precedence is
   written from the claim's text and is never re-derived from the table under test; the
   mutant controls therefore cannot score green by construction. It is still ONE file,
   so the C3 freeze carries the evaluator and the table parser together — the L1 may want
   a second reader to check that the two are independent in the frozen bytes.
