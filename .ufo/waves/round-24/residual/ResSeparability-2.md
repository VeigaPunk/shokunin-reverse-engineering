# ResSeparability-2 — R24-C1 / R24-C2 separability at 69e82c48

Seat: KagiR27-2.ResSeparability-2 (critic, read-only). Scratch: `/fast/scratch/kaidoku-r24/seats/ResSeparability-2/` (`overlays.sh`, `overlays.log`, `out/*.json`). Instruments run from Git blobs of 69e82c48: count-c1.py sha256 `f1859605…ff00c` (equals the frozen pin), freeze-gate.py `8a71fe84…b329` (equals the disclosed supersession), and the frozen gate from 97ade2e `1e2a9370…870f`. Installs: none.

## Verdict

**Separable at the measurement level, with one designed causal edge in each direction. None of these edges is a deliverable dependency.**

- **R24-C1 can be verified without R24-C2.** The C1 counter reaches 4/4 on a C1-only overlay that has no ledger, no gate revision and no S068 row. It also reaches 4/4 on an overlay that has no `claims.json` at all.
- **R24-C2 can be verified without R24-C1.** The gate reports 11/11 disclosed, exit 0, with round-24 CLEAN on a C2-only overlay from which all C1 envelopes and the knowledge entry are absent. On that overlay C1 is 0/4.
- **Coupling 1 (C1 instrument to C2 verdict, a causal edge).** C2's round-24 CLEAN verdict depends on C1's instrument file not changing after the freeze.
- **Coupling 2 (C2 row to C1 parse, a parse-only causal edge).** C1's counter parses the whole of `corpus/SOURCES.md`, so a badly formed C2 row (S068) makes C1 unevaluable.
- **Coupling 3 (shared commit and history, non-causal).** No commit in the lane has exactly one claim landed: 69e82c48 carries both claims' deliverables. The C2 disclosure pins commit `9fb4eacd`, and C1's evidence commit 74cd4e3 is in that commit's ancestry. This is a history-identity tie only; it does not feed either count.

I do not call the round verified.

## Findings

Every result below is an observation from `overlays.log` (instrument exit code plus JSON) unless it is tagged [INFERENCE].

### Overlays built for this review

| overlay | construction | C1 count-c1 | C2 freeze-gate (`--require-clean round-24 --disclosures corpus/claim-freezes.tsv`) |
|---|---|---|---|
| O0 | HEAD 69e82c48 | exit 0, 4/4 | exit 0, 11/11, r24 CLEAN |
| O1 | C1-only: 74cd4e3 + knowledge entry + SOURCES without the S068 row and its Paths line | exit 0, 4/4 | exit 1, 0/11 (all 11 ledger rows missing), r24 CLEAN; with `--require-clean` only: exit 0 under both the revised and the frozen gate |
| O1b | C1-only on 97ade2e (instruments only, **no claims.json**) + envelopes + entry + C1 SOURCES | exit 0, 4/4 | — |
| O2 | C2-only: 9fb4eac with `evidence/c1/` removed + HEAD claims.json + ledger | exit 1, 0/4 | exit 0, 11/11, r24 CLEAN |
| O2b-literal | C2-only on 5dc49bf, gate revision re-applied (new hash), HEAD claims.json unchanged | exit 1, 0/4 | exit 1, round-24 mismatched, FLAGGED INSTRUMENT_REVISED (freeze-gate.py, undisclosed new hash) |
| O2b-rewritten | same, with the supersession `commit` set to the new hash | exit 1, 0/4 | exit 0, 11/11, r24 CLEAN |

### Edge tests (counterexamples on HEAD)

| case | mutation | C1 | C2 | edge? |
|---|---|---|---|---|
| X1 | append a comment line to `count-c1.py` post-freeze | exit 0, 4/4 | **exit 1**, round-24 FLAGGED INSTRUMENT_REVISED (count-c1.py) | **yes, C1 instrument to C2** |
| X2 | S068 row id changed to S064 (malformed C2 source row) | **exit 2** `duplicate_source_id: S064` | exit 0, 11/11 | **yes, C2 row to C1, parse/prefix only** |
| X3 | post-freeze edit of R24-C1 `total` 4→2, `target`, and R24-C2 `target` in claims.json | exit 0, 4/4 | exit 0, 11/11, CLEAN | neither instrument guards claim text (see note) |
| X4 | S068 row and its Paths line removed | exit 0, 4/4 | exit 0, 11/11 | no (S068 is not machine-required by either) |
| X5 | knowledge entry and `evidence/c1/` removed | exit 1, 0/4 | exit 0, 11/11 | no |
| X6 | `claim-freezes.tsv` removed, QUALITY.md reverted to 9fb4eac | exit 0, 4/4 | exit 0 (`--require-clean` only), r24 CLEAN | no |
| X7 | append a comment line to `run-rea.py` (the C1 producer) post-freeze | exit 0, 4/4 | exit 0, 11/11 | no (the producer is outside both instruments) |
| X8 | `freeze-gate.py` reverted to the frozen 97ade2e blob | exit 0, 4/4 | exit 1, FLAGGED INSTRUMENT_REVISED (freeze-gate.py) | no to C1; C2 self-edge only |

### Shared files and their causal status

1. **`.ufo/waves/round-24/claims.json`** holds both claims.
   - C1: never read. `count-c1.py:117-205` has no claims read, and O1b holds 4/4 with no claims file.
   - C2: causal. The gate reads the frozen claims' strings and pins (`freeze-gate.py:81-94`) and the current `instrument_supersessions` (`:89-91`).
   - Command check: between 5dc49bf and 69e82c4 the `claims` and `instruments` objects are equal. Only `instrument_supersessions` was added.
   - Status: C2-only causal. C1 is the subject of C2's audit, because R24-C1's `counting_command` names `count-c1.py`.
2. **`.ufo/waves/round-24/tools/count-c1.py`** is C1's instrument. It is also in C2's audit set, because `SCRIPT` at `freeze-gate.py:46` matches it in the R24-C1 strings, and the history walk at `:109-113` covers it.
   - Status: **causal edge C1 to C2** (X1).
   - Consequence: any future C1 repair to the counter flips C2's round-24 row to red unless it is disclosed in `instrument_supersessions` and the ledger.
3. **`corpus/SOURCES.md`**: S064–S067 belong to C1 and S068 belongs to C2.
   - C1 parses every 13-cell row. A duplicate id raises an error (`count-c1.py:64-72`), and the BASE prefix must be preserved (`:129-132`).
   - C2: never read.
   - Status: **causal edge C2 to C1, well-formedness and append-order only** (X2). There is no semantic dependency (X4).
4. **`corpus/claim-freezes.tsv`**: C2-only (`freeze-gate.py:118-131`). C1 does not read it (X6). Its pointer column cites `corpus/lessons/round-24.md`, but the gate checks only that the pointer is non-empty (`:128`). Status: non-causal for C1.
5. **`corpus/knowledge/2026-10-21-r24-pcap-family-envelopes.md`** and **`.ufo/waves/round-24/evidence/c1/*`**: C1-only. C2 is unaffected (X5, O2). Status: non-causal for C2.
6. **`.ufo/waves/round-24/tools/freeze-gate.py`**: C2-only. C1 is unaffected (X8). Status: non-causal for C1.
7. **`corpus/README.md`, `corpus/QUALITY.md` (row 33), `corpus/lessons/round-24.md`, `PROVINCE.md`, `SKILL.md`**: shared documentation that neither instrument reads.
   - C1 reads only `corpus/knowledge/` (`count-c1.py:75-83,151`).
   - C2 reads only claims files and the ledger.
   - Status: non-causal (X6 for QUALITY).
8. **Commit 69e82c48 and the supersession hash `9fb4eacd`**: there is no single-claim commit, and the disclosed revision commit has C1's 74cd4e3 in its ancestry.
   - Under the gate, history matters only through the instrument paths (`freeze-gate.py:109`).
   - O2 (envelopes removed, hash kept) stays CLEAN.
   - O2b-literal goes red only because the disclosed commit literal no longer exists in that history.
   - Status: a non-causal history-identity tie. Verifying one claim on its own needs an overlay, not a lane commit.
9. **`.ufo/waves/round-24/tools/selftest.py`** (the L1 selftest).
   - It is **not in 69e82c48**: `git cat-file -e 69e82c4:…selftest.py` returned exit 128, "exists on disk, but not in '69e82c4'", and the lane status shows it as untracked.
   - It is joint by design. A single clone of the measured revision must pass both `c1_positive_at_rev` (expects 4/4) and `c2_clean_at_rev` (expects 11/11) (`selftest.py:95-139`).
   - Status: the L1 demonstration cannot be run per claim. It is also not a frozen, revision-bound artifact at the reviewed commit.
10. **`.ufo/waves/round-24/tools/run-rea.py`** (C1's producer). R24-C1 does not name it (grep of claims.json: exit 1), so C2 does not audit it, and C1 only checks run-record argv strings.
    - A post-freeze edit is invisible to both instruments (X7).
    - Status: non-causal, but it is a gap shared by both claims. It is disclosed under C2 `not_claimed` ("instruments named only outside claims.json").

Note on X3 [observation + INFERENCE]:
- Observation: the gate audits only instrument freeze, not claim-text freeze. It reads claims from the freeze commit (`freeze-gate.py:82-84`) and never compares them with the claims at the measured revision. Editing R24-C1's `total` and `target` after the freeze leaves both instruments green.
- Inference: this is not a separability defect. It does mean C2's "claim-freeze audit" wording is broader than what the gate checks. At 69e82c48 the claim text is in fact unchanged (the command check under item 1).

## Recommended L1 action

1. **Record the two causal edges in the round record:** count-c1.py to C2's round-24 row, and SOURCES.md well-formedness to C1. Also record that per-claim verification needs overlays like O1 and O2, because no lane commit isolates either claim.
   - Smallest safe correction for the C1-to-C2 edge: if `count-c1.py` must change after the freeze, append an `instrument_supersessions` entry and a matching ledger row in the same commit.
   - Smallest safe correction for the C2-to-C1 edge: append S068-style rows only after the BASE rows, with unique ids.
2. **Commit `selftest.py`, or exclude it from the evidence.** The 17-case L1 selftest is not at 69e82c48, so citing it against that revision is unbound. If it is committed, add per-claim cases or note that it is joint-only.
3. **Optionally narrow the R24-C2 wording** to "instrument-freeze audit". If the broader wording stays, add a frozen-vs-measured `claims` equality check as a new disclosed supersession; it would turn X3 red. This is a tradeoff for the judge, not a defect at this commit.
