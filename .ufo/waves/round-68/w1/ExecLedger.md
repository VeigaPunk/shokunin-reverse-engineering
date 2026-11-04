# ExecLedger — round 68 / w1 — defect 3 (QUALITY #100 companion row) and defect 4 (prefile receipt + freeze-ledger retirement)

Seat: `ExecLedger` (leaf). Scope: the two routed defects of the round-67 closure
(`LOG.md:4125` items 3 and 4), closed on paper. **No tracked lane file was edited, no commit, no
jj/git mutation; every write is under `.ufo/waves/round-68/w1/ExecLedger/`.**

- Measured revision `6ffa9ce1119ec01c953494d8f5b28e419efad646` (HEAD at measurement), lane
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
- Round base `fcbe200f6739c38939e0dabf3f251de2cc6bd727`; operative freeze `1eaf596e5f241762349fbd102c9e09ec1df18e3f`.
- Both gates read **Git objects only** (`git show <rev>:<path>`, `git ls-tree`), so every number
  below is a property of the revision, not of the working tree. Stated because the working tree
  changed under this seat while it ran (see §5).
- Scratch `/fast/scratch/hyaku/kaidoku-r68/ExecLedger/` was created and is removed before yield;
  the receipts below were copied into this seat's tree first.

---

## 0. Verdicts

| item | verdict | evidence |
|---|---|---|
| Defect 3 (QUALITY #100 companion row for the round-64 findings cell) | **row derived, exact, append-only**; series id `round-64/correction-1` | §1; `evidence/proposed-correction-row.tsv` |
| Defect 4a (prefile gate receipt) | **run; exit 1 at `6ffa9ce1`** — red for three independent reasons, all expected in-wave (§2.1) | `evidence/prefile-at-6ffa9ce1.txt` |
| Defect 4b (round-24 ledger retirement) | **21 rows: 20 exact, 1 stray, 16 missing keys**; retirement erratum text supplied | §2.3 + `evidence/proposed-retirement-erratum.md` |
| Item 3 (round-68 gate verdict) | **FLAGGED `INSTRUMENT_UNPINNED`** ×2 paths; needs one appended v2 row, and the finding is **permanent** for that claims file | §3 |

---

## 1. Defect 3 — the QUALITY #100 companion row for `round-64`

### 1.1 The exact row (8 columns, single line, tab-separated)

```
round-64/correction-1	round-64 (corpus/claim-freezes-v2.tsv)	findings	INSTRUMENT_UNRESOLVED mkcache.js; INSTRUMENT_UNRESOLVED view8.py; INSTRUMENT_UNPINNED tools/round-64/jsc-route-matrix.py	INSTRUMENT_UNPINNED,INSTRUMENT_UNRESOLVED	the round-67 repair (451f3102, filed as QUALITY #46) normalised a prose findings cell into the gate's machine form - the sorted unique finding codes joined by commas - by an in-place edit of an already-filed row, which QUALITY #100 forbids; the gate's own audit of .ufo/waves/round-64/claims.json at its freeze a35e5141 reports exactly INSTRUMENT_UNRESOLVED for mkcache.js and INSTRUMENT_UNRESOLVED for view8.py (both named by bare file name, so no blob can be identified) and INSTRUMENT_UNPINNED for tools/round-64/jsc-route-matrix.py (named by lane path, no sha256 recorded at the freeze), so the code set now filed is the audit's own set and not a re-reading of the row; the verdict cell is unchanged (FLAGGED) and this row is appended, never an edit of corpus/claim-freezes-v2.tsv	451f3102 (git diff 8672cf40 451f3102 -- corpus/claim-freezes-v2.tsv, the two cells above); the same audit reproduces the filed cell at 6ffa9ce1 with round-64 among its exact disclosures (disclosures.mismatched [] in .ufo/waves/round-68/w1/ExecLedger/evidence/r29-gate-v2-at-6ffa9ce1.txt)	2026-11-04T01:48:49Z
```

Committed verbatim as a one-line file at `evidence/proposed-correction-row.tsv` (append it; do not
retype it).

### 1.2 How each cell was re-derived (no guess)

| cell | derivation |
|---|---|
| `correction-id` = `round-64/correction-1` | the ledger's series is `<corrected round>/correction-<n>`: existing ids are `round-53/correction-1` and `round-55/correction-1` (`cut -f1 corpus/claim-freezes-corrections.tsv`), each naming the round its row corrects; `round-64` has no correction yet → `correction-1` |
| `corrects` | `round-64 (corpus/claim-freezes-v2.tsv)` — the form of both existing rows |
| `field` = `findings` | the edited column; the row's cells are `round / verdict / findings / pointer` (`corpus/claim-freezes-v2.tsv` header) |
| `was` | `git show 8672cf40:corpus/claim-freezes-v2.tsv \| sed -n 41p \| cut -f3` → `INSTRUMENT_UNRESOLVED mkcache.js; INSTRUMENT_UNRESOLVED view8.py; INSTRUMENT_UNPINNED tools/round-64/jsc-route-matrix.py` |
| `now` | same extraction at `451f3102` → `INSTRUMENT_UNPINNED,INSTRUMENT_UNRESOLVED` |
| `cause` | the row was **added** at `39a91a99` (round-67 declaration, "the missing r64/r66 ledger rows (QUALITY #33)") carrying the prose cell, then **rewritten in place** at `451f3102` ("round-67: ledger correction — the round-64 row's findings cell normalised to the gate's finding-set form (QUALITY #46)"), which is one commit **after** the round-67 close `8672cf40`. QUALITY #100 forbids an in-place edit of a landed verdict row and routes the change to the companion ledger. The new value is the round-29 gate's own form: `','.join(sorted({finding codes}))` (gate lines 179-181) |
| `receipt` | `451f3102` (the edit this row corrects) + the reproduction: the gate at `6ffa9ce1` audits `.ufo/waves/round-64/claims.json` (freeze `a35e5141`) to exactly `{INSTRUMENT_UNRESOLVED: mkcache.js, INSTRUMENT_UNRESOLVED: view8.py, INSTRUMENT_UNPINNED: tools/round-64/jsc-route-matrix.py}` and counts the `round-64` row among its exact disclosures (`mismatched: []`, 42 of 43 exact, only `round-68` missing) |
| `utc` | filing instant, `2026-11-04T01:48:49Z` (= 22:48:49 -03:00); it precedes any landing commit, as QUALITY #23 requires |

The `now` cell is not merely plausible — the gate **agrees** with it: with that cell filed, the
round-64 row is in `disclosures.exact`, and `disclosures.mismatched` is empty
(`evidence/r29-gate-v2-at-6ffa9ce1.txt`).

### 1.3 Relation to the row the L1 already staged in the working tree

While this seat ran, the working tree gained an uncommitted 8-column variant of the same correction
(`git diff HEAD -- corpus/claim-freezes-corrections.tsv`: appended `round-64/correction-1`, utc
`2026-11-04T01:46:04Z`, receipt `451f3102`, a shorter cause). Audited, it is **compliant**: 8 cells,
`was`/`now` byte-equal to §1.2, appended at the end. Either it or the file above satisfies defect 3;
**only one may land** — two rows with the same `correction-id` would collide. The variant above
carries the reproduction receipt (the gate's `mismatched []`) that the staged one lacks; the staged
one is otherwise correct and its `utc` is earlier.

---

## 2. Defect 4 — the prefile gate, and the retirement of `corpus/claim-freezes.tsv`

### 2.1 `tools/round-29/prefile-check.sh` — output verbatim, exit code

Run exactly as the script defines it (one argument: the lane root), at HEAD `6ffa9ce1`, with the
script as committed at that revision:

```
$ sh /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-29/prefile-check.sh /home/vgpnk/Projects/shokunin/kaidoku-shokunin
 M SKILL.md
 M corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md
?? .ufo/waves/round-68/r68-w1-dispatch.err
?? .ufo/waves/round-68/r68-w1.ready.dispatched
?? .ufo/waves/round-68/w1/
prefile: tree NOT CLEAN (5 paths)
prefile: round-24 gate --disclosures corpus/claim-freezes.tsv at 6ffa9ce1119ec01c953494d8f5b28e419efad646 exit=1
prefile: round-29 gate --disclosures corpus/claim-freezes-v2.tsv at 6ffa9ce1119ec01c953494d8f5b28e419efad646 exit=1
prefile: FAIL
$ echo $?
1
```

`evidence/prefile-at-6ffa9ce1.txt`. Three independent causes, all expected at this instant and none
of them a surprise:

1. **step 1 tree** — 5 paths dirty: two tracked files of other seats' in-flight work
   (`SKILL.md`, the r67 knowledge entry) and this wave's own artifacts. A pre-file gate is defined to
   run *after* the last commit, so this is a timing state, not a defect.
2. **step 2 round-24 gate** — exit 1, by construction at every revision since round 53 (§2.3).
3. **step 3 round-29 gate** — exit 1 for one reason only: `round-68` has no row yet
   (`disclosures: exact 42 of 43, missing ["round-68"], mismatched [], stray []`). The row text that
   clears it is in §3.

### 2.2 The two gates, full output and exit codes (script output suppresses it with `> /dev/null`)

`evidence/r24-gate-claim-freezes-at-6ffa9ce1.txt` and `evidence/r29-gate-v2-at-6ffa9ce1.txt` hold
the byte-verbatim stdout; `evidence/r24-verdicts.tsv` (36 rows) and `evidence/r29-verdicts.tsv`
(43 rows) render every audited freeze with its full finding detail, so the tables lose nothing.

**Round-24 gate** (`python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root <lane> --rev 6ffa9ce1 --disclosures corpus/claim-freezes.tsv`, **exit 1**):

```json
{"audited": 36, "claim": "R24-C2", "clean": 18, "disclosures": {"exact": 20, "mismatched": [], "missing": ["round-53", "round-54", "round-55", "round-56", "round-57", "round-58", "round-59", "round-60", "round-61", "round-62", "round-63", "round-64", "round-65", "round-66", "round-67", "round-68"], "of": 36, "path": "corpus/claim-freezes.tsv", "present": true, "stray": ["round-35"]}, "flagged": ["round-14", "round-15", "round-16", "round-17", "round-18", "round-19", "round-20", "round-21", "round-22", "round-23", "round-25", "round-26", "round-27", "round-28", "round-29", "round-53", "round-64", "round-68"], "required_clean": [], "required_failed": [], "rev": "6ffa9ce1119ec01c953494d8f5b28e419efad646", "summary": {"INSTRUMENT_ABSENT": 12, "INSTRUMENT_NONE": 4, "INSTRUMENT_PIN_MISMATCH": 0, "INSTRUMENT_REVISED": 15, "INSTRUMENT_UNPINNED": 13, "INSTRUMENT_UNRESOLVED": 11}}
```
(the `freezes` array is 36 entries, rendered in `evidence/r24-verdicts.tsv`)

**Round-29 gate** (`python3 -I -B tools/round-29/freeze-gate.py --root <lane> --rev 6ffa9ce1 --disclosures corpus/claim-freezes-v2.tsv`, **exit 1**):

```json
{"audited": 43, "claim": "R29-freeze-gate", "clean": 21, "disclosures": {"exact": 42, "mismatched": [], "missing": ["round-68"], "of": 43, "path": "corpus/claim-freezes-v2.tsv", "present": true, "stray": []}, "flagged": ["round-14", "round-14/claims-review.json", "round-15", "round-15/claims-review.json", "round-16", "round-17", "round-18", "round-19", "round-20", "round-21", "round-22", "round-23", "round-25", "round-26", "round-27", "round-28", "round-29", "round-32/claims-v3.json", "round-35/claims-frozen.json", "round-53", "round-64", "round-68"], "required_clean": [], "required_failed": [], "rev": "6ffa9ce1119ec01c953494d8f5b28e419efad646", "summary": {"INSTRUMENT_ABSENT": 12, "INSTRUMENT_NONE": 6, "INSTRUMENT_PIN_MISMATCH": 2, "INSTRUMENT_REVISED": 17, "INSTRUMENT_UNPINNED": 12, "INSTRUMENT_UNRESOLVED": 11}}
```
(the `freezes` array is 43 entries, rendered in `evidence/r29-verdicts.tsv`; the two
`INSTRUMENT_PIN_MISMATCH` findings are both in `round-35/claims-frozen.json` —
`tools/round-35/c1-coverage-counter.py` pinned `cd4ab7e7…` vs `d49ff16a…` at the freeze, and
`tools/round-35/c2-calibration-counter.py` pinned `39fe39c5…` vs `c0f37d21…`)

### 2.3 Audit of `corpus/claim-freezes.tsv` — counts, missing rounds, the stray row

- **Data rows: 21** (header + 21 = 22 lines, `wc -l`). Rounds present: `round-14` … `round-32` (19),
  `round-34`, `round-35`. Nothing after `round-35`.
- **Missing rounds 53-67: all 15** (`round-53`, `-54`, `-55`, `-56`, `-57`, `-58`, `-59`, `-60`,
  `-61`, `-62`, `-63`, `-64`, `-65`, `-66`, `-67`). The gate's `missing` list adds `round-68`, this
  round's own key, which is expected to be absent until the round files. (`round-33` has no
  `claims.json` at any revision, so it is not a missing row.)
- **Stray `round-35`**: the key `round-35` is defined for `.ufo/waves/round-35/claims.json`, which
  **existed and was removed** — added `131eacfa`, deleted `13d7a815` ("canonical claims-frozen.json
  … draft claims.json removed"). Round 35's freezes live on as `claims-canonical.json` and
  `claims-frozen.json` and are disclosed in v2 under those keys. The `round-35` row was written
  *after* the deletion (`a85ca674`, 16:10:48 vs 16:07:04), so it was stale on arrival; it is the
  single stray at every revision since.
- **It cannot be greened.** `stray` is computed as `set(ledger keys) - set(audited freeze keys)`; no
  appended row removes a key, so `round-35` keeps the gate at exit 1 forever. Appending the 15
  missing rows would fix `exact` only:
  `python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root <lane> --rev 6ffa9ce1 --disclosures corpus/claim-freezes.tsv`
  would then read `exact 36 of 36, stray ["round-35"]` → still exit 1. **Removing the row is the
  only other way, and that is the in-place deletion QUALITY #100 forbids** — it would also erase a
  truthful FLAGGED record (`INSTRUMENT_ABSENT,INSTRUMENT_REVISED`).
- **The ledger is not append-only anyway**: `a85ca674` added the `round-35` row *and* rewrote the
  pointer cells of two already-filed rows — `round-27` 1009 → 701 characters and `round-28`
  959 → 709 (`git diff 54a87a51 a85ca674 -- corpus/claim-freezes.tsv`, cells compared field by
  field).
- **Its verdicts are a superseded detector's, so v2 cannot be ported in**: `round-28` is
  `INSTRUMENT_UNPINNED,INSTRUMENT_UNRESOLVED` here (the round-24 gate does not read pins under
  `producers_not_counters`) against v2's `INSTRUMENT_UNRESOLVED`; both ledgers are exact against
  their own gates, which is why they legitimately disagree.
- **Nothing is lost by retiring it**: every one of the 21 rows' rounds is disclosed in v2 under the
  same key except `round-35`, whose two freezes v2 carries as `round-35/claims-canonical.json` and
  `round-35/claims-frozen.json`.

### 2.4 The retirement erratum (exact text)

Full text in `evidence/proposed-retirement-erratum.md`; the operative sentence:

> **ERRATUM — `corpus/claim-freezes.tsv` retired at round 68 (bytes frozen as filed; no row added,
> no row rewritten).** … The file stays byte-frozen as filed (last change `a85ca674`, 2026-10-25:
> 21 data rows, rounds 14-32, 34, 35). No row is appended to it and none is edited — an erratum line
> inside the file is impossible anyway: the gate's TSV reader requires exactly four tab-separated
> cells per row and a `round / verdict / findings / pointer` header, so any comment row makes it exit
> 2. `tools/round-29/prefile-check.sh` step 2 stops reading the ledger as a disclosure input; the
> round-24 gate stays in the tree as frozen history; future freeze disclosures go to
> `corpus/claim-freezes-v2.tsv` only.

Landing: (1) the round-68 `LOG.md` entry carries the text (this is the *named* retirement — at
measurement no LOG entry existed); (2) `corpus/README.md` gains one `## Ledgers` row (the
working-tree README diff at measurement touches only knowledge/frontier rows, so this is still
owed); (3) `tools/round-29/prefile-check.sh` step 2, which the L1 has already changed in the working
tree — **verified below**.

### 2.5 The retired step-2 mechanism the L1 staged — verified, with three prose/logic nits

The staged (uncommitted) `tools/round-29/prefile-check.sh` replaces the round-24 run with a
**byte-identity pin** of the retired ledger (`legacy_sha=2a840d72…`) and renames the check
`ledger1 retired (erratum r68-1)`. This is stronger than dropping the step: it keeps the retired
file's bytes provably frozen. Verified:

- **The pin is correct** — `sha256sum corpus/claim-freezes.tsv` and
  `git show HEAD:corpus/claim-freezes.tsv | sha256sum` both give
  `2a840d72acfd71e55fc16aa614dcefee7afd0cf67e276b799ac9d41e773dda81` (observation).
- **The step passes on the real tree** — running the staged script at HEAD prints
  `prefile: ledger1 retired (erratum r68-1) — legacy ledger byte-identical to its retirement pin`
  (`evidence/prefile-landed-step2-at-6ffa9ce1.txt`).

Three defects to fix before landing (all cosmetic; none changes a verdict):

1. **"It stops at round-52"** — false: the last row is `round-35`, and there are no rows for
   rounds 36-52 either (21 rows: 14-32, 34, 35). The true sentence is "it carries nothing after
   `round-35`".
2. **"the gate reported 20 exact of 36 on every round from 53 on"** — the `exact` count happened to
   be 20 throughout, but `of` grows with the lane: at `f78fc766` (round-53's ledger-verdict commit)
   the gate reads `audited 21, exact 20 of 21, missing ["round-53"], stray ["round-35"]`; at
   `6ffa9ce1` it reads `audited 36, exact 20 of 36, missing` the 16 keys, `stray ["round-35"]`
   (`evidence/r24-verdicts.tsv`, both runs). What is stable from round 53 on is `stray ["round-35"]`,
   hence exit 1 at every revision.
3. **`${got:-absent}` is unreachable** — a failed `git show` feeds empty stdin to `sha256sum`, whose
   digest of empty input is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
   (verified), never the empty string, so a missing ledger reports `got e3b0c442…` instead of
   `absent`. Functionally harmless (both fail), but the diagnostic reads wrong.

(The header comment also keeps the `gate (the` / `freeze-gate.py` line break introduced by the edit.)

### 2.6 What the prefile gate will read once the round lands

Projection, not a run (the landing commit is the L1's):

| step | state after the landing commit | basis |
|---|---|---|
| 1 tree | clean | it is the last commit before filing |
| 2 ledger1 | exit 0 | staged pin verified against HEAD's blob (§2.5) |
| 3 ledger2 | exit 0 | the staged `round-68` row makes the disclosure agreement `exact 43 of 43, mismatched [], missing [], stray []` (`evidence/projection-v2-after-landing.json`), and the same shape was proved end-to-end in a two-commit fixture: `exact 1 of 1, exit 0` (`evidence/fixture-valid-row68-row-at-a334d6bf.txt`) |

---

## 3. Round-68 verdict, and exactly what the gate needs

No `round-68` row exists in `corpus/claim-freezes-v2.tsv` at `6ffa9ce1` (the ledger's last row is
`round-67`; the gate reports `missing ["round-68"]`). The gate's own audit of the round-68 freeze:

- freeze `1eaf596e5f241762349fbd102c9e09ec1df18e3f` (the first commit adding
  `.ufo/waves/round-68/claims.json`),
- **verdict FLAGGED**, findings `INSTRUMENT_UNPINNED` for `tools/round-67/avm-le-counter.py` and
  `tools/round-67/mutation-battery.py`,
- `instruments` the gate extracts: those two plus `tools/round-68/packed-elf.py` and
  `tools/round-68/registry-conformance.py`; the container's `instruments` map pins only the three
  round-68 files (`registry-conformance`, `packed-elf`, `controls`), so the two round-67 paths are
  unpinned.
- Where they are named: `.claims.R68-C1.predicate` and `.repairs[1]` — the C1 predicate names them
  as the two unregistered tools it repairs, i.e. **the claim's own subject**, and a claim string is
  exactly what the detector scans.

**What the gate needs: one appended row.**

```
round-68	FLAGGED	INSTRUMENT_UNPINNED	<pointer prose: freeze 1eaf596e, the three pins, the two unpinned paths, the disclosure reason>
```

(Committed as `evidence/proposed-round68-disclosure-row.tsv`; the L1's staged working-tree row has
exactly this verdict and code set. The `findings` cell is the **unique sorted** code set — writing
the code twice, as the raw finding list does, is `mismatched ["round-68"]`, exit 1:
`evidence/fixture-duplicate-code-row-at-81468c8f.txt`.)

**The finding cannot be repaired after the freeze** — observations, not inference: the gate builds
`pins` from the *frozen* copy (`frozen.get(key)`, gate lines 109-111) and compares the blob at the
freeze commit. Fixture proof (`evidence/fixture-post-freeze-pin-at-db7798fc.txt`): a two-commit repo
whose second commit adds both missing pins to the `instruments` map still audits as
`INSTRUMENT_UNPINNED` for both paths, `clean 0`. Consequences for this round:

- the round-68 record must disclose `FLAGGED` — that is the honest verdict of the container as
  frozen. It does not block the round: the gate's exit code is governed by **disclosure agreement**
  (`len(exact) == len(expected)` and no stray), not by CLEAN verdicts; a disclosed FLAGGED row still
  yields exit 0 (fixture: `evidence/fixture-valid-row68-row-at-a334d6bf.txt`).
- the C1 predicate itself is untouched by this finding: it is a statement about the *registry* and
  the census, not about the container's pin map.
- the durable lesson for the container builder: **any instrument a claim string names must appear in
  `instruments` at the freeze commit** — here the predicate's own subject could not be pinned after
  the fact.

---

## 4. Files written (absolute)

Under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-68/w1/ExecLedger/`:

- `report.md` (this file), `evidence/sha256.txt`
- `evidence/proposed-correction-row.tsv` — the defect-3 row, verbatim, append-ready
- `evidence/proposed-round68-disclosure-row.tsv` — the defect-3-adjacent §3 row, verbatim
- `evidence/proposed-retirement-erratum.md` — the defect-4 erratum text + landing + rejected alternatives
- `evidence/prefile-at-6ffa9ce1.txt` — the committed prefile script's stdout and exit code
- `evidence/prefile-landed-step2-at-6ffa9ce1.txt` — the staged script's run (step 2 green)
- `evidence/r24-gate-claim-freezes-at-6ffa9ce1.txt`, `evidence/r29-gate-v2-at-6ffa9ce1.txt` — byte-verbatim gate stdout
- `evidence/r24-verdicts.tsv` (36 rows), `evidence/r29-verdicts.tsv` (43 rows) — every freeze, every finding field
- `evidence/projection-v2-after-landing.json` — disclosure agreement with the staged round-68 row
- `evidence/fixture-valid-row68-row-at-a334d6bf.txt`, `evidence/fixture-duplicate-code-row-at-81468c8f.txt`,
  `evidence/fixture-post-freeze-pin-at-db7798fc.txt` — the three fixture receipts (scratch repos, each
  asserting `git rev-parse --show-toplevel` == the fixture dir before any commit; deleted with the scratch)
- Also `.ufo/waves/round-68/w1/ExecLedger.md` — the same report at the seat's declared Report path.

No tracked lane file, no fleet file, no other lane, no index, no commit, no push. Scratch removed.

## 5. Observation / inference / unknown

- **Observation** — every number in §2.2-§2.3 and §3 is the output of a gate run at `6ffa9ce1`;
  the verdict tables are transcriptions of the same JSON, not re-derivations.
- **Observation** — the working tree changed under this seat between 22:44 and 22:52 local
  (5 → 16 dirty paths, including `corpus/claim-freezes-v2.tsv`, `corpus/claim-freezes-corrections.tsv`
  and `tools/round-29/prefile-check.sh`), i.e. the L1 (or another writer) is landing the two
  defects' repairs concurrently. My gate numbers are unaffected (the gates read Git objects at a
  revision), but the *staged* files are uncommitted and were read as working-tree text — labelled as
  such wherever cited (§1.3, §2.5, §2.6).
- **Inference** — that the landing commit will make step 1 clean and step 3 exit 0: derived from the
  gate's own agreement code plus the fixture, not from a run at a commit that does not exist yet.
- **Unknown** — whether the L1 will land my row variant or its shorter staged one; both are
  compliant, only one may land (§1.3). Unknown whether the round-68 lesson/LOG will carry the
  erratum verbatim.
- **No tool was installed or upgraded** (nothing was needed); no pacman transaction was attempted
  (transactions are paused host-wide); no L0 question arises.

## 6. Risks

- **Stray-row rule is asymmetric**: any future row for a round whose `claims.json` is later deleted
  becomes stray and permanently reds the round-24 gate — the reason retirement, not re-filing, is the
  correct disposition (§2.3). The same trap exists in v2 for `round-35/claims-frozen.json` (it is
  `flagged`, not stray, because its file still exists).
- **The prefile gate's step 2 remains a hard failure if the retired ledger's bytes ever change** —
  that is the intent of the pin; a legitimate future edit would need a new erratum, not a silent
  edit.
- **Duplicate correction row** if both §1.1 and the staged row land (§1.3).
