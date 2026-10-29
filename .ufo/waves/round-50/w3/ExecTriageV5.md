# R50-C3 — triage table v5: the instrument build (wave 3, seat ExecTriageV5)

## VERDICT

**The C3 instrument is built, selftest-green, and measured on the frozen held-out
directory: exit 1 before (19 pair mismatches, the four `v2ns *_ddefault` rows among
them), exit 0 after the v5 table lands (0 mismatches, `table_labels ==
evaluator_labels` on all 126 envelopes).** The draft is ready for the L1 to review and
land. Nothing was landed by this seat, and no lane or fleet tracked file was touched.

Two **disclosed limits** need the L1's attention in the landing prose: the held-out
corpus contains **no** no-reader `extractor-failure` envelope, so the `no-reader-failure`
row is witnessed by the selftest, not by the corpus (F4); and the reader census is
FIXTURE-level while the claim's rule is FAMILY-level, which leaves a measurable residue
in `squashfs_v3_ddwrt` (F10) — the L1 has ruled on it ("disclosed, not fixed"), and my
measurement gives that ruling numbers.

| deliverable | path | sha256 |
| --- | --- | --- |
| the instrument (also landed by the L1 at `tools/round-50-c3/sqfs-triage-v5.py`; the final bytes are a working-tree modification for the freeze) | `.ufo/waves/round-50/w3/ExecTriageV5/tools/round-50-c3/sqfs-triage-v5.py` | `ef4633c523ca8ab4ff096a7d90ef7074461a67f03952ad3652a048dce84d3ed0` |
| the v5 table draft (17 rows) | `…/ExecTriageV5/receipts/v5-table-draft.md` | (see the receipt) |
| the landing draft (rule block 22 + freeze contents + the registry row) | `…/ExecTriageV5/receipts/landing-draft.md` | (see the receipt) |
| the before-state label distribution | `…/ExecTriageV5/receipts/label-distribution-before.md` | (see the receipt) |
| the reader census (35 fixture/reader rows, byte-exact) | `…/ExecTriageV5/receipts/reader-census.txt` | (see the receipt) |
| the reader-boundary what-if (the 8 labels that move) | `…/ExecTriageV5/receipts/reader-boundary-whatif.txt` | (see the receipt) |

**The registry row is not mine to land.** `ExecRegistryRow` measured that my row's
self-test cell fails `c2-record.py`'s own `re.match` (a cell that opens with a backtick
does not match the `<interpreter> <path> … --selftest` shape) and that ITS row passes; the
L1 has `ExecRegistryRow`'s row as the paste source and its row is in `SKILL.md`'s
registry. **Use `ExecRegistryRow`'s row, not mine** — my landing draft keeps its row only
as a marked placeholder. This is a correction to my own draft, on their measurement.

The instrument lands at **`tools/round-50-c3/sqfs-triage-v5.py`**, not `tools/round-50/`:
the L1 committed that path rule at `03f852b9` ("Path rule (measured, not assumed)") after
wave-3 `ExecFetchDry` measured that a file added under the frozen `tools/round-50/` tree
reads as frozen-path drift and takes C1 and C2 down. My instrument's `INSTRUMENT_RELPATH`
constant carries that path, so its own freeze arm checks the right file.

---

## FINDINGS

| # | finding | evidence | command | exit |
| --- | --- | --- | --- | --- |
| F1 | **The v4 table mis-routes exactly 19 of the 126 held-out envelopes, and all 19 are no-reader families.** The v4 `clean` row labels them `clean`/`none`; the R50-C3 precedence labels them `clean-unverified`/`record-unverified`. Every reader-backed family is unchanged — which is what the claim requires. | `receipts/before.json` (mismatch list with per-envelope features), `receipts/label-distribution-before.md` | `python3 -I -B …/sqfs-triage-v5.py --root <LANE> --rev f890bbead20ca2c549487167f56876ae47f1e1a4 --freeze 435d41fd… --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ --json-out receipts/before.json` | **1** (not met, as the predicate requires) |
| F2 | **The four `v2ns *_ddefault` envelopes are among the mismatches**, exactly as the claim names them: `squashfs_v2_nonstandard_squashfs_v2.{0,1}_{le,be}_ddefault`, each `clean`/`none` -> `clean-unverified`/`record-unverified`. This is the round-49 F2 witness, now measured rather than asserted. | `receipts/before.txt` (the four lines), `receipts/before.json` | same as F1 | 1 |
| F3 | **With the v5 table landed, the table and the fixed evaluator agree on all 126 envelopes**: `pair_mismatches 0`, `evaluator_missing 0`, `table_labels == evaluator_labels` true, verdict `met`. Measured for BOTH placements of the block (inside the craft section and as a standalone rule block after block 23) — the instrument finds the v5 marker anywhere in the document, so the L1's placement choice does not change the score. | `receipts/after-sim.json`, `receipts/after-sim-outside.json` | `… --skill <simulated SKILL.md with the v5 block> --envelopes <held-out dir> --json-out receipts/after-sim.json` | **0** (met) |
| F4 | **LIMIT: the held-out corpus cannot witness the no-reader FAILURE branch.** The 126 envelopes hold 38 no-reader envelopes — 19 clean, 19 depth-limited — and **none** a no-reader `extractor-failure` with zero files. So `no-reader-failure` is unexercised by the corpus, and the two mutations that only move that branch (`legacy-glob-widened`, `no-reader-failure-row-deleted`) are **vacuous** on it. The instrument reports this honestly: each control carries a per-scope `red`/`vacuous` flag, and the selftest's fixture scope carries a synthetic no-reader failure envelope, so both mutations are red there. **The landing prose must say that `no-reader-failure` is measured by the selftest, not by the held-out dir.** | `receipts/controls.json` (`scopes.corpus.vacuous`), `receipts/controls.txt` | `… --controls --envelopes <held-out dir> --json-out receipts/controls.json` | 0 (all controls red in some scope) |
| F5 | **All 9 controls are red in at least one scope and none is vacuous everywhere**, including the four the claim names: do-nothing (RED 19 on the corpus, naming the four v2ns rows), junk table (RED 126), guard-row-deleted (RED 19), swapped-action (RED 19). The evaluator is FIXED and is never re-derived from the table under test, so a mutant table cannot score green by construction. | `receipts/controls.json`, `receipts/controls.txt` | same as F4 | 0 |
| F6 | **The v4 grammar cannot express "the reader-backed v1-v3 families" in one cell**, so v5 needs one grammar delta: a handler-family cell may be a comma-separated list of globs. `squashfs_v[123]*` (the v4 cell) also matches the three no-reader families — that is F1; `squashfs_v[123]` drops `squashfs_v3_ddwrt`, which IS reader-backed and must keep the legacy row. The narrowed cell is `squashfs_v1,squashfs_v2,squashfs_v3,squashfs_v3_ddwrt` — the selftest asserts it matches exactly those four of the ten known handlers, and that the three no-reader families match neither it nor the new rows. | `receipts/selftest.txt` (`ddwrt_is_reader_backed`, `no_reader_rows_are_keyed_on_the_families`) | `python3 -I -B …/sqfs-triage-v5.py --selftest --work <scratch>` | **0** |
| F7 | **The selftest is green: 18 cases, pass 18, fail 0.** It carries the red-before witness (the v4 table parsed by the v5 parser mismatches the evaluator on the v2ns fixtures), the v5-draft-matches-the-evaluator case over 10 fixtures (2 v2ns clean, 1 v2ns failed, 2 v3-family legacy rows, 3 clean v4 rows, 1 symlink row), the 7 textual mutations (each flips ≥1 pair and EXACTLY the pairs it owns — none a no-op, none cross-flipping), the rule-level blanked-cell mutation, the junk-table control, the dead-alternative refusal, the **duplicate-handler-glob refusal (H1: a repeated alternative in one handler cell is refused, in both handler columns)**, the **named-guard-row case** (the guard row the guard-deleted control deletes is `clean-unverified`, and the `no-reader-failure` row/action is witnessed by a committed SYNTHETIC zero-file extractor-failure envelope), the **predicate-pinning case** (reads the claims file and compares the sentence the claim carries with the instrument's `PREDICATE` constant, fragment by fragment), the **receipt-existence case** (runs the instrument for real and checks the receipt on disk), the **claim-consistency case** (the claim states the 19-row before-state and binds the before-run to the declared base), the blanked-text-cell refusal, the v3-marker refusal, and the evaluator's independence. | `receipts/selftest.txt` | same as F6 | **0** |
| F12 | **THE PREDICATE SENTENCE NOW MATCHES THE AMENDED CLAIM, AND REACHES THE RECEIPT.** The claim requires "the same sentence in the counter docstring, this file, and the receipt label", and my docstring still carried the PRE-amendment wording ("the four `v2ns *_ddefault` rows") after the L1 amended it to "the no-reader `*_ddefault` rows" at `d71829bf`. Fixed: the sentence is now the constant `PREDICATE`, it is written into **every** JSON receipt under the key `predicate` (the before, after and controls receipts all carry it), the docstring quotes the amended sentence, and a selftest case reads the claims file and compares it fragment by fragment so the two cannot drift again. | `receipts/selftest.txt` (`predicate_matches_the_claim_file`), the `predicate` key in every `receipts/*.json` | `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest` | **0** |
| F13 | **THE RECEIPT GATE IS NOW ENFORCED BY THE INSTRUMENT, NOT JUST ADVISED.** The critic's requirement — "require the JSON receipt to exist and parse before accepting exit 0" — is implemented: after writing the receipt the instrument **re-reads it** and refuses (exit 2) unless it parses and carries `predicate`, `pair_mismatches`, `evaluator_missing`, `table_labels`, `n_envelopes` and `verdict`. A selftest case runs the instrument for real over a fixture set and checks the receipt on disk. This closes the F11 shape: a stub that exits 0 while writing nothing now cannot pass the instrument's own gate. | `receipts/selftest.txt` (`receipt_is_written_and_parses`) | `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest` | **0** |
| F14 | **THE COUNTING-COMMAND INCONSISTENCY IS RESOLVED (by the L1, at `c3121c4f`), AND THE CLAIM NOW STATES THE 19-ROW BEFORE-STATE.** The claim's "Counting command" bullet now reads "before at the declared base `--rev f890bbea…` (exit 1 with the seat-measured **19** no-reader `clean/none` `_ddefault` rows mismatched: 4 v2ns, 7 v3_broadcom, 8 v3_nonstandard)", consistent with its frozen rule details. My receipts used `f890bbea…` and 19 from the start, following the frozen rule details. The selftest case `claim_counting_command_is_consistent` now checks that the claim states the 19-row before-state, binds the before-run to the declared base, **and names the ddwrt failed body `dmg_Z3_v3ddwrt_inode_table`** - the last check currently REPORTS that the claim does not yet name it (the claim discloses the residue in general terms around the two CLEAN no-pad rows, not the FAILED body), and the exact suggested wording is in `receipts/landing-draft.md` for the L1 to add. | `receipts/selftest.txt` (`claim_counting_command_is_consistent`), `git show HEAD:plans/round-50-attempt2-claims.md` | - | 0 (the check) |
| F15 | **THE RECEIPT NOW NAMES THE INSTRUMENT'S OWN BYTES**, so an external scorer can bind a receipt to the frozen file instead of trusting the report's word. Every JSON receipt (the before, after-sim, after-sim-outside, controls and junk-semantic-red receipts) now carries `instrument_sha256` - the sha256 of the running instrument - next to the `predicate` sentence, so a scorer can compare the receipt's named bytes against the file at the freeze and reject a receipt produced by different code. The critic's "external scoring should validate receipt values and frozen instrument bytes" is therefore satisfiable from the receipt alone. | the `instrument_sha256` key in every `receipts/*.json` | - | 0 |
| F8 | **The guards hold.** `--json-out` under `/tmp` -> exit 2; `--json-out` into the lane's `tools/` -> exit 2 ("would write into the graded or frozen surface"); `--work` under `/tmp` -> exit 2; an unknown revision -> exit 2; a FREEZE that is not an ancestor of REV -> exit 2. The instrument reads git read-only (`show`, `rev-parse`, `merge-base --is-ancestor`, `diff --name-only`) and never invokes REA. | measured in-session (transcript of this seat); the receipt set carries the passing paths | see the commands in the seat transcript | 2 each (refusal) |
| F9 | **Two no-reader shapes keep their v4 rows, by the claim's own scope.** A no-reader family that failed while publishing >0 files keeps `partial-body-failure`; a no-reader family with an empty tree keeps `clean-empty`. The claim defines exactly two no-reader labels, so those two shapes are left on the v4 rows and NAMED in the instrument docstring and in the landing draft rather than silently re-labelled. Both are unreachable in the held-out corpus. | `tools/round-50-c3/sqfs-triage-v5.py` docstring ("Two limits of this precedence are stated rather than hidden"), `receipts/landing-draft.md` §5 | — | — |
| F10 | **THE READER BOUNDARY IS FIXTURE-LEVEL IN THE CENSUS AND FAMILY-LEVEL IN THE RULE — and the gap is measurable.** Re-measuring the round-42 fixture bytes with both readers (`unsquashfs` 4.7.5 `-lls`, 7-Zip 26.04 `l -tSquashFS`), byte-exact per family per fixture: `squashfs_v3_nonstandard` is 8/8 **no-reader** (both refuse), `squashfs_v3` is 8/8 readable by both, `squashfs_v3_broadcom` is 7/8 **partial** (7-Zip lists it, `unsquashfs` refuses) and `squashfs_v3_ddwrt` is **6/7 no-reader**. The claim's no-reader set is `{v2ns, v3_broadcom, v3_nonstandard}` — so **ddwrt is routed reader-backed while 6 of its 7 fixtures have no reader at all**, and broadcom is routed no-reader while 7 of its 8 fixtures have a working 7-Zip listing. The instrument's docstring, its `NO_READER_FAMILIES` comment and the table's `cause` prose now all use the claim's wording "no validated COMPLETE independent oracle" and say that a no-reader FAILURE label never suppresses a successful partial cross-read. Measured consequence on the 126 envelopes: under the claim's rule the ddwrt failure envelope `dmg_Z3_v3ddwrt_inode_table` reads `legacy-body-failure`/`cross-read-legacy` — a cross-read on a body whose readers refuse — and 7 ddwrt `clean` envelopes read `clean`/`none` (an oracle-backed action with no oracle). Moving ddwrt into the no-reader set would move exactly those 8 labels and leave `pair_mismatches 0` under both rules. **The L1 has already ruled on this** (claim commit `d71829bf`): the no-reader set stays handler-level and frozen, broadcom's partial listing is worded as "no validated complete independent oracle", ddwrt stays reader-backed, and its no-pad residue is **disclosed, not fixed**, because the discriminator would be a body variant the scored features do not carry. My measurement supports that ruling as the conservative one and gives it numbers. | `receipts/reader-census.txt` (35 fixture/reader rows with digests), `receipts/reader-boundary-whatif.txt` (the 8 labels that move) | `unsquashfs -lls FILE; 7z l -tSquashFS FILE` over the round-42 fixture bytes; `python3 -I -B reader-boundary-whatif.py <instrument> <envelopes>` | 0 |
| F11 | **A do-nothing stub sat at the lane landing path** (`tools/round-50-c3/sqfs-triage-v5.py`, 49 bytes, `# simulated C3 instrument`, sha256 `af1b22ba…`), copied there by the L1's misroot sweep from the fleet stray. It exits 0 on `--selftest` **and** 0 on the full predicate command while writing **no receipt** — a do-nothing GREEN, exactly what the claim's kill rule forbids. The L1 has since replaced it with the real bytes (sha256 `a2ebb5a4…`); the stub is gone and the landing path now carries the instrument. Recorded because the receipt-existence check, not the exit code, is what catches this shape. | measured in-session; `receipts/` carries the post-replacement verification at the landed path | `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest` and the full predicate command | 0 (real instrument), the stub was 0 with no receipt |

### The before-state label distribution (the required before-state evidence)

Full table: `receipts/label-distribution-before.md`. Summary — the v4 table today vs the
v5 evaluator, over the 126 held-out envelopes:

| label | v4 table today | v5 evaluator | difference |
| --- | --- | --- | --- |
| `clean` | 51 | 32 | −19 |
| `clean-unverified` | 0 | 19 | +19 |
| `container-depth-limited` | 3 | 3 | 0 |
| `dep-missing-be` | 2 | 2 | 0 |
| `dep-missing-le` | 8 | 8 | 0 |
| `depth-limited` | 48 | 48 | 0 |
| `in-tree-symlink-metadata` | 1 | 1 | 0 |
| `legacy-body-failure` | 7 | 7 | 0 |
| `partial-body-failure` | 2 | 2 | 0 |
| `unknown-residue` | 4 | 4 | 0 |
| **total** | **126** | **126** | 0 |

One row moves; nothing else does. That is the depth the claim adds.

---

## WHAT THE L1 MUST DO WITH THIS

1. **Land the table** — `receipts/landing-draft.md` carries the rule-block-22 prose
   (already reconciled with the L1's claim amendments at `d71829bf`: the comma-list
   alternation, the "no validated complete independent oracle" wording for broadcom,
   the handler-level frozen no-reader set, and the ddwrt residue disclosed not fixed);
   `receipts/v5-table-draft.md` carries the exact 17 rows (paste verbatim; they are also
   `--print-v5-block` output, so the shipped table and the instrument's draft cannot
   drift).
2. **Freeze the instrument** at `tools/round-50-c3/sqfs-triage-v5.py` (FINAL sha256
   `ef4633c5…`; the lane's tracked version is older and the final bytes are a
   working-tree modification) together with the registry row — **`ExecRegistryRow`'s row, not mine**
   (their cell 3 satisfies `c2-record.py`'s own regex; mine does not). The **table does
   NOT go in the freeze commit** — it lands after, so the frozen instrument is measured
   against a table that did not exist at freeze time.
3. **Run the C3 controls with the frozen instrument BEFORE the table lands** and commit
   the receipts: `--controls --envelopes <held-out dir> --json-out <OUT>`. The
   do-nothing control must be RED and must name the four `v2ns *_ddefault` envelopes.
   **Require the `--json-out` receipt to EXIST and parse** — a 49-byte stub sat at that
   path and exited 0 on both the selftest and the full predicate command while writing
   no receipt (F11). The instrument now enforces this on ITSELF (F13): it re-reads the
   receipt and exits 2 unless it parses and carries the required keys, and an unwritable
   receipt path is exit 2, never a pass.
4. **Carry the two disclosed limits into the landing prose**: the `no-reader-failure` row
   is measured by the selftest, not by the held-out corpus (F4); and the reader census is
   fixture-level while the rule is family-level, which leaves a measurable residue in
   `squashfs_v3_ddwrt` (F10) — disclosed, not fixed, per the L1's own ruling, now with
   numbers behind it.
5. **Re-run the two counting commands** (before at the declared base `f890bbea…`, exit 1
   with the 19 no-reader `*_ddefault` rows among the mismatches; after at the landing
   revision, exit 0) and commit the receipts under
   `.ufo/waves/round-50/l1/scores/c3-{before,after}.json`.

---

## BOUNDARIES HONOURED

- **Read-only on the lane tree.** The only files this seat wrote are under
  `.ufo/waves/round-50/w3/ExecTriageV5/`. `git status` in the lane shows no tracked
  file modified (`git diff --stat` empty at `03f852b9`). No commit, push, stage, stash
  or mutating git/jj command was run in the lane or the fleet repo.
- **No REA run.** The instrument never invokes REA, unblob or sasquatch, never reads a
  carrier, and never touches a network. No `npx rea-agents` was run.
- **No downloads.** No image was fetched; no vendor firmware bytes were copied anywhere.
- **Scratch.** `S=/fast/scratch/hyaku/kaidoku-r50/w3-ExecTriageV5`, `TMPDIR` honoured,
  `--work` used for the selftest fixtures; removed after the receipts were copied. No
  file was written under `/tmp`, and the instrument REFUSES a `--work` or `--json-out`
  on a temporary partition (F8).
- **Fixture repos.** None were needed: every measurement is read-only against the real
  lane git tree and the committed held-out corpus. No clone, no commit, no identity.
- **Tooling.** No tool was installed or upgraded, so no pacman/`uv`/`npx` transaction
  occurred and the paused-pacman guard was never touched. Python 3 (stdlib only) was
  used.
- **Not touched.** `.ufo/state/`, `.ufo/watchdog.log`, `/home/vgpnk/Projects/shokunin/.scratch/`,
  the fleet repo, any sibling seat's directory, `corpus/evidence/`, and no `--data-run`.

### Note on the stray fleet file

A 49-byte stub (`/home/vgpnk/Projects/shokunin/tools/round-50-c3/sqfs-triage-v5.py`,
content `#!/usr/bin/env python3\n# simulated C3 instrument`) appeared in the FLEET repo at
17:51 — a relative-path write, which is a defect. **It was not this seat's**: my
instrument is 90,837 bytes with a full docstring, and every write this seat made used an
absolute path under the lane seat directory (`grep` over this seat's tree finds no
reference to a fleet path). The stub's exact bytes are the string literal in the
`ExecRegistryRow` seat's fixture script
`/fast/scratch/hyaku/kaidoku-r50/w3-ExecRegistryRow-2/final-landing.py:64`, which
writes that stub into its fixture clone to simulate the C3 landing — so the stray came
from that seat's fixture run landing one relative write in the fleet tree. The `misroot`
seat removed it while this seat was checking; the fleet tree is now empty and `git
status` in the fleet repo shows no `?? tools/`. Recorded here so the L1 knows the fleet
tree was briefly dirty and is now clean, and so the finding is not attributed to the
wrong seat.

---

## CHECKS THE MAIN AGENT SHOULD RUN

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
T=tools/round-50-c3/sqfs-triage-v5.py
E=.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes
S=/fast/scratch/hyaku/kaidoku-r50/w3-verify; mkdir -p "$S"

# 1. selftest green (expect: 16 cases, pass 16, fail 0; exit 0)
python3 -I -B "$T" --selftest --work "$S"

# 2. before-state red (expect: exit 1, 19 pair mismatches, the four v2ns _ddefault among them)
python3 -I -B "$T" --root . --rev f890bbead20ca2c549487167f56876ae47f1e1a4 \
  --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --envelopes "$E" --json-out "$S/before.json"

# 3. after-state green (expect: exit 0, pair_mismatches 0, table_labels == evaluator_labels)
python3 -I -B "$T" --root . --rev <LANDING_REV> \
  --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --envelopes "$E" --json-out "$S/after.json"

# 4. controls (expect: every control RED in some scope; do-nothing names the four v2ns rows)
python3 -I -B "$T" --controls --envelopes "$E" --json-out "$S/controls.json"

# 5. lane tree untouched by this seat
git status --porcelain --untracked-files=all -- .ufo/waves/round-50/w3/ExecTriageV5
git diff --stat        # must be empty
```

Not run by this seat, and therefore not claimed: the after-state at a real landing
revision (no table is landed yet — F3 simulates it in scratch, at both placements), the C3
controls at the L1's freeze commit (the L1 runs those, after the table lands or before,
per the claim's landing order), and the C1 data run (out of scope for this seat and
forbidden in this wave).
