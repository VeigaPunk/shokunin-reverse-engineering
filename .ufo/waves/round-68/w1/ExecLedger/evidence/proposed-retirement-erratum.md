**ERRATUM — `corpus/claim-freezes.tsv` retired at round 68 (bytes frozen as filed; no row added, no row rewritten).**

- **What it was.** The disclosure ledger of the round-24 R24-C2 claim-freeze gate
  (`.ufo/waves/round-24/tools/freeze-gate.py`), keyed `round-N` for
  `.ufo/waves/round-N/claims.json` and for no other claims file.
- **What superseded it.** `corpus/claim-freezes-v2.tsv`, audited by
  `tools/round-29/freeze-gate.py`: it discloses every `claims*.json` in the lane under the key
  `round-N` (`claims.json`) or `round-N/<file>` (any other claims file), and it is the ledger the
  pre-file check's third step reads. At `6ffa9ce1119ec01c953494d8f5b28e419efad646` it audits 43
  freezes where the round-24 gate audits 36 — the round-24 gate's subjects are a strict subset
  (36 + 7 `claims*-<name>.json` files = 43).
- **Why it cannot be brought into agreement.** Measured at `6ffa9ce1` with the round-24 gate and
  `--disclosures corpus/claim-freezes.tsv`: exit 1, `audited 36`, `exact 20 of 36`,
  `missing` = the 16 keys the file never carried (`round-53` … `round-68`), `stray ["round-35"]`.
  Appending the 15 rounds 53-67 would not clear it: `stray` is computed from the ledger's keys
  against the audited freeze keys, and `.ufo/waves/round-35/claims.json` was **removed** at
  `13d7a815` (its freezes are `claims-canonical.json`/`claims-frozen.json`), so the `round-35` row
  has no key to match at any later revision. Clearing it would take deleting a filed verdict row —
  the in-place rewrite QUALITY #100 forbids — and that row is itself a truthful record of a
  setup-order defect (`INSTRUMENT_ABSENT,INSTRUMENT_REVISED`). The ledger is not append-only in
  any case: `a85ca674` (2026-10-25) rewrote the pointer cells of `round-27` and `round-28` when it
  added `round-35`.
- **Detector-specific verdicts.** The filed rows are the verdicts of a superseded detector, so they
  cannot be replaced from v2: `round-28` is `INSTRUMENT_UNPINNED,INSTRUMENT_UNRESOLVED` here (the
  round-24 gate does not read pins under `producers_not_counters`) against v2's
  `INSTRUMENT_UNRESOLVED`. Porting v2 rows in would be wrong, and recomputing 15 rounds against a
  retired detector would mint 15 verdicts that no gate reads.
- **Nothing is lost.** Every one of the 21 filed rows' rounds is disclosed in v2 under the same key,
  except `round-35`, whose two freezes are disclosed there as `round-35/claims-canonical.json` and
  `round-35/claims-frozen.json`.
- **Disposition.** The file stays byte-frozen as filed (last change `a85ca674`, 2026-10-25: 21 data
  rows, rounds 14-32, 34, 35). No row is appended to it and none is edited — an erratum line inside
  the file is impossible anyway: the gate's TSV reader requires exactly four tab-separated cells per
  row and a `round / verdict / findings / pointer` header, so any comment row makes it exit 2.
  `tools/round-29/prefile-check.sh` step 2 stops reading the ledger (patch below); the round-24 gate
  stays in the tree as frozen history; future freeze disclosures go to
  `corpus/claim-freezes-v2.tsv` only.

**Landing (three places, all the L1's):**

1. `corpus/README.md` — one line in a `## Ledgers` section (new):
   `| `corpus/claim-freezes.tsv` | RETIRED at round 68 — the round-24 gate's ledger, byte-frozen at `a85ca674`; superseded by `corpus/claim-freezes-v2.tsv` (round-29 gate, 43 freezes at `6ffa9ce1`); cannot be brought into agreement (16 missing keys, one stray `round-35` whose `claims.json` was removed at `13d7a815`) — retirement erratum in the round-68 LOG entry; step 2 of `tools/round-29/prefile-check.sh` no longer reads it |`
2. `LOG.md` — the round-68 entry carries the erratum text above (abbreviated is not acceptable; the LOG row is the named retirement).
3. `tools/round-29/prefile-check.sh` — the patch in `proposed-prefile-step2.patch` (header comment
   renumbered + the `old=...` block replaced by a comment). Without it the pre-file gate can never
   print `prefile: PASS` again, because step 2 runs unconditionally whenever the round-24 gate file
   exists.

**Rejected alternatives, with reasons.**

- *Append the 16 missing rows and delete `round-35`.* Still red until the delete; the delete is the
  forbidden in-place rewrite of a filed row and erases an honest FLAGGED record.
- *Run the round-24 gate without `--disclosures`.* It then exits 0 unconditionally (its exit code is
  `1 if required_failed else 0`, and no `--require-clean` is passed), so the step proves nothing; and
  its verdicts disagree with the operative detector (`round-28`), so it is not a usable second opinion.
- *Re-file v2's rows into the round-24 ledger.* Wrong by construction (different pin keys, different
  keyspace); see "Detector-specific verdicts".
