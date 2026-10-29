# R50-C3 control fixtures — round 50 attempt 2, wave 3, seat ExecTriageControls

**These are inputs, not results.** The C3 instrument (`tools/round-50/sqfs-triage-v5.py`) does
not exist yet; nothing here runs it. The L1 freezes the instrument, then scores these controls
before the v5 table lands. Every number below is a *prediction* derived from committed lane
bytes (the v4 table at base, the 126 committed round-42 recon envelopes, the attempt-2 claim
text) — it is not a measurement of the v5 instrument.

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · base revision
`f890bbead20ca2c549487167f56876ae47f1e1a4` · held-out dir
`.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/` (126 envelopes, committed at base,
verified by `git ls-tree` — receipts R02/R04/R08/R09).

## Files

| file | what it is |
|---|---|
| `envelopes-manifest.json` | every envelope: path, bytes, sha256, declared tuple (OP/PV/H/HF/G/D/BE/SR/P), the v4 label/action at base, its family and whether the family is one of the claim's no-reader families |
| `v4-table-at-base.md` | the v4 table block extracted from base `SKILL.md` (marker, vocabulary, header, separator, 15 rows), sha256 `99cd54d7fe8847486175db9fbf06fa4da3c891a17dd74ffc00eacd64c8ddd6da` |
| `ctl-<X>.table.md` | the mutated table block alone (v5 marker + v5 vocabulary) |
| `ctl-<X>.skill.md` | the whole base `SKILL.md` with that block substituted in place of the v4 block (v4 marker + v4 vocabulary) |
| `ctl-<X>.skill.v5surface.md` | the same document with the marker re-stamped to `<!-- sqfs-triage-table v5 -->` and the vocabulary extended with `record-unverified preserve-unverified`; it differs from `ctl-<X>.skill.md` on exactly 2 lines (receipt R07) |
| `ctl-<X>.expected-red.json` | the clause that must fire, the expected exit, the expected mismatch count and the exact envelope list |
| `receipts.tsv` / `receipts.json` | every command run for this seat: exit code, stdout and stderr sha256, UTC time |
| `build_controls.py` | the generator (deterministic; re-running it reproduces every artefact byte-for-byte) |
| `analyze.py` | the independent per-envelope decision dumper used for the manifest |

Two surfaces are shipped for each control because the v5 instrument does not exist yet: use
`.skill.md` if the instrument accepts a v4-marked live table, `.skill.v5surface.md` if it
requires a v5 marker. The table rows are identical in both.

## The four controls and the clause each guards

Kill rule (attempt-2 claims, R50-C3): *do-nothing green at the freeze, a committed mutation
leaving its pair green or flipping the wrong pair, or a no-op mutation, stops C3.* Each control
below must come out **red** (the instrument must not exit 0).

| control | construction | kill-rule clause | expected exit | expected pair mismatches (claim's 3-family reading) |
|---|---|---|---|---|
| `ctl-do-nothing` | the v4 table at base, extracted (not hand-copied); the document is **byte-identical to base `SKILL.md`** (sha256 `19046cf2…`, receipt R06) | "do-nothing (v4 table at base → red)" | 1 | **19** (19 label + 19 action) |
| `ctl-junk` | every row's label cell replaced by `clean` | "junk table (every row `clean` → red)" | 1 (see caveat) | **94** (94 label + 19 action) |
| `ctl-guard-deleted` | the `legacy-body-failure` row deleted | "guard-row-deleted mutant → red" | 1 | **26** (19 inherited from the base table + 7 the guard row decided) |
| `ctl-action-swapped` | the `clean` row's action `none` → `inspect-input` | "swapped-action mutant → red" | 1 | **51** (19 label + 51 action) |

Envelope lists are in the `expected-red.json` files. All four contain the four v2ns `_ddefault`
rows among their mismatches (`must_include_v2ns_ddefault_count: 4`):
`squashfs_v2_nonstandard_squashfs_v2.{0,1}_{be,le}_ddefault`.

## The mismatch sets, and why they are what they are

The base table's `clean` row decides **51** envelopes (`clean`/`none`). Of those, **19** belong to
the three no-reader families and have no gap and >0 published files, so the v5 evaluator gives
them `clean-unverified`/`record-unverified` — that is finding F2 (the oracle-backed action no
oracle can serve) and it is the whole of the do-nothing red. The other 32 are reader-backed and
keep the v4 rows, so they stay matched.

`ctl-guard-deleted` adds the 7 envelopes the `legacy-body-failure` row decided
(`dmg_V1_inode_last`, `dmg_V2_inode_table`, `dmg_V3_dir_last`, `dmg_V6_frag_index`,
`dmg_Z1_v1_inode_table`, `dmg_Z2_v2_inode_table`, `dmg_Z3_v3ddwrt_inode_table`). All seven are
reader-backed families (`squashfs_v1`, `squashfs_v2`, `squashfs_v3`, `squashfs_v3_ddwrt`), so
the v5 evaluator keeps the v4 legacy row for them and the mutant must mismatch.

`ctl-action-swapped` is the only control that is red **because the action half of the pair is
compared**: 32 of its 51 mismatches are action-only (label `clean` matches, action
`inspect-input` ≠ `none`). An instrument that compares labels only would report the same 19 as
the do-nothing control and would not distinguish this one.

### Family-set readings (the L1 must pin one)

The claim's evaluator text names three no-reader families; the round-49 reader census
(`corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`, "What stays Frontier") gives
`v2ns` **no** reader (unsquashfs exit 1, 7z exit 2) and `v3_nonstandard` none, but `v3_broadcom`
a **partial** reader (7-Zip lists the committed LE broadcom fixture; unsquashfs refuses it).
Each reading is in `expected-red.json` under `family_set_readings`:

| reading | families | do-nothing | guard-deleted | junk | action-swapped |
|---|---|---|---|---|---|
| `claim-three-families` (claim text) | v2ns, v3_broadcom, v3_nonstandard | 19 | 26 | 94 | 51 |
| `census-two-families` | v2ns, v3_nonstandard | 12 | 19 | 87 | 51 |
| `census-v2ns-only` | v2ns | 4 | 11 | 79 | 51 |

Every reading keeps the four v2ns `_ddefault` rows among the mismatches, so the predicate
("the four `v2ns *_ddefault` rows among the mismatches") holds for all three. The base
mismatch count the L1's frozen instrument reports must equal the reading it implements.

## Instrument requirements these controls expose (pre-freeze)

1. **`--skill` (or an equivalent) is required.** The claim's predicate command line
   (`--root --rev --freeze --envelopes --json-out`) names no document to score. The controls must
   be scored **before** the v5 table lands, so the instrument must be able to score a table that
   is not `SKILL.md` at `--rev`; the v4 pattern (`--skill`) is the lane's own.
2. **The live-table marker check must accept v4 (and v5).** The landed `SKILL.md` will carry the
   v4 table as history (rule block 21) *and* the v5 table (rule block 22). The instrument must
   select the v5 block when both are present and must still be able to score a document whose
   only triage table is v4 — that document is `ctl-do-nothing`. If the instrument refuses a
   v4-marked document, the do-nothing control is unscoreable as a mismatch red (it becomes
   exit 2) and the kill-rule clause cannot be evidenced.
3. **The action-vocabulary check must be membership, not equality.** The v5 vocabulary adds
   `record-unverified` and `preserve-unresolved`; the v4 line is a subset of it. A v4-vocabulary
   document must still parse.
4. **The duplicate-label check decides what the junk control is.** The junk table repeats the
   label `clean` in all 15 rows; the v4 parser refuses it (`sqfs-triage-v4: line 531: duplicate
   label 'clean' (first on line 530)`, exit 2 — receipt R11-ctl-junk). Either the v5 parser drops
   that check (then the junk control is a mismatch red, 94 mismatches) or the L1 records the
   exit-2 refusal as this control's red. The v4-style refusal is a refusal, not a comparison, so
   the weaker reading is preferred.
5. **The pair must be (label, action).** The predicate's `pair_mismatches` name and the
   round-42 driver's own method both compare pairs. A label-only comparison weakens
   `ctl-action-swapped` to the do-nothing set.
6. **Do not renumber the craft-section rule blocks.** "Rule block 22" is already the
   freeze-integrity block: the craft section holds 25 rule blocks at the tip (block 21 = the
   v4 triage table, blocks 22–25 = the freeze/exactness/meaning tables, whose explicit titles
   `23. `, `24. `, `25. ` are asserted by `tools/round-46/attest.py`, `tools/round-47/exact.py`
   and `tools/round-48/meanings.py`). Land the v5 table as an **unnumbered** bullet right after
   the v4 bullet (blocks 1–21 are unnumbered) and leave 22–25 untouched; the instrument then
   finds the v5 table by marker, not by block number. Receipt: `receipts-craft-blocks.txt`.

## Caveats stated rather than hidden

- The evaluator side of every expectation is an **offline reconstruction** of the attempt-2 claim
  text (R50-C3 clauses 1 and 2) applied to the measured v4 features, not a run of the frozen
  instrument. The table side is measured (the lane's own `tools/round-42/sqfs-triage-v4.py` run
  offline over the 126 committed envelopes with each control document as `--skill`).
- The second new label (`no-reader-failure`/`preserve-unresolved`) is **not witnessed** by this
  corpus: no no-reader envelope among the 126 carries an `extractor-failure` gap, so the
  held-out dir exercises only the `clean-unverified` half of the new rule.
- Finding **F1** (the `squashfs_v[123]*` glob over-matching the no-reader families) is a
  rule-level defect that this corpus cannot witness either: all 7 envelopes the legacy row
  decides are reader-backed, so no no-reader envelope ever reaches that row. The F1 fix must be
  justified by the rule text and the reader census, not by a corpus mismatch.
- The corpus is not fresh data: it is the round-42 recon corpus (126 envelopes, committed since
  round 42), 78 of which v4 scored at R43-C1. The claim itself discloses this.

## Post-freeze scoring (for the L1)

```
python3 -I -B tools/round-50/sqfs-triage-v5.py --root <LANE> --rev <REV> --freeze <FREEZE> \
  --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes \
  --skill .ufo/waves/round-50/w3/ExecTriageControls/ctl-do-nothing.skill.md \
  --json-out <OUT>.json
```

…one invocation per control, `--skill` pointing at `ctl-<X>.skill.md` (or the `.v5surface.md`
variant). Each must exit 1 with `pair_mismatches` equal to the number in
`ctl-<X>.expected-red.json` for the family-set reading the instrument implements. A control that
exits 0 stops C3.

## Provenance

Generated by seat ExecTriageControls, round 50 attempt 2 wave 3, from committed lane bytes only:
`git show f890bbea…:SKILL.md`, `tools/round-42/sqfs-triage-v4.py`, and the 126 committed
envelopes. No REA run, no network, no write outside
`.ufo/waves/round-50/w3/ExecTriageControls/`. Exact commands, exit codes and sha256 digests:
`receipts.tsv`.
