# ScoutRecon — round 86 (kaidoku), recon for R86-C1 / R86-C2

Seat: ScoutRecon (scout, read-only). BASE `2cf0b7ff93c698809bed321f7338276a22d6beb9`.
Full findings: **`.ufo/waves/round-86/w1/ScoutRecon/recon.md`**. No production file was
edited; no commit was made.

## The six things a later seat must not miss

1. **A3 needs exactly ONE `| coverage |` row in the whole `SCORECARD.md`, not one in
   `## Owned axes`.** BASE has **23**. The counter (`record-agreement.py:154`) does
   `line.startswith("| coverage |")` with **no section scope** and fails on the count
   (`"expected exactly one '| coverage |' row, found 23"`) before it ever reaches the
   pointer check. Two independent edits are needed; the second is invisible until the
   first lands.
2. **A3's receipt must be a blob at `--rev` with a 40-hex `rev`, at a round ≥ the row's own
   round (85).** `.ufo/waves/round-85/l1/scores/` does **not** exist at BASE — the receipt
   must be committed before the measured revision (round-86 works). The `rev` field need
   only be 40-hex, not an ancestor.
3. **A1's `count N` clause belongs in the `teaches` cell (index 6), not the `anchor` cell
   (index 5).** BASE S303's "five scopes" is in cell 5; the counter reads `cells[6]`.
   The correct count is **7** with ids **S079 S080 S083 S090 S092 S119 S123** — not the 5
   ids in S303's own cell, and not 8 (the counter excludes S303 and the superseding row).
   The new row's `teaches` must **start with** the literal `supersedes S303`.
4. **Editing `tools/round-84/mutation-closure.py`'s docstring (A2) breaks the round-86
   claims-container pin.** That file is pinned in `claims.json` under both
   `target_instruments` and `loaded_by_counter` (sha256 `e5cfd2ed…`); after the edit
   `tools/round-84/freeze-precheck.py` reports
   `COUNTER_PIN_MISMATCH:tools/round-84/mutation-closure.py` and the container goes
   **FLAGGED**. The L1 must re-issue the pin. The code assigns `survived`; the docstring
   must say `surviv…` and must not contain `inconclusive` or `killed` in that sentence.
5. **`gate-registry.py` executes the tool from `--root`'s WORKING TREE**, not from `--rev`
   and not from `--worktree` (measured: `--root R --worktree W` ran R's copy). The row's
   self-test cell must name a command that works from the lane root.
6. **`SKILL.md` at BASE has zero `predicate-bind` occurrences.** Insertion point: line
   **1930** — immediately after the last tool row (`tools/round-84/nested-sqfs.py`, line
   **1929**) and before `<!-- /instrument-registry -->` (line **1930**, section open at
   line **1780**, 140 tool rows). Row must be **7 cells**, cell 0 exactly
   `` `tools/round-85/predicate-bind.py` `` (backticked), verdict cell literally
   containing `0=`/`1=`/`2=`, self-test cell of the form
   `` `python3 -I -B tools/round-85/predicate-bind.py --selftest` — N cases, exit 0 on <date> ``
   (the `exit N` must be **after** the ` — `, since only the text before the first ` — `
   is parsed as the command), pinned cell naming `.ufo/waves/round-85/claims.json`, owner
   cell exactly `kaidoku-r85`.

## S255

Tier **A**, kind `docs`, status **`mined`**, opened **2026-11-01**, recheck **`on-release`**,
used-by = 7 paths (`plans/round-55-claims.md`, `tools/round-55/corrections-pin.py`,
`corpus/lessons/round-55.md`, `corpus/knowledge/2026-11-04-r81-…`, `corpus/lessons/round-81.md`,
`corpus/knowledge/2026-11-04-r83-…`, `corpus/lessons/round-83.md`).
**Openable again this round — yes**: it was re-opened the same way in round 83
(`corpus/lessons/round-83.md:19`: status and recheck unchanged, **only `used-by` changed**),
which the append-only rule (`tools/round-38/registry-immutable.sh`: only status/recheck/used-by
may differ) permits. Leave `opened` at `2026-11-01` (round-75 search-log convention); record
the re-open in `## Search log` and add the round-86 path to `used-by`. `E11` requires the
added `used-by` path to exist on disk.

## LIVE: L1's integration commit `4cc03025e` — every finding confirmed

The L1 landed `4cc03025e` while I was finishing. Re-running both counters at that commit:

- **C2 (R86-C2): already GREEN — `agreed 5/5 mismatches []`.** No further work needed.
- **C1: `agreed 2/3`** — A1 and A2 landed exactly as I derived them (`declared_count: 7`
  with ids `S079 S080 S083 S090 S092 S119 S123`, `superseding_row: S305`; docstring
  `an absent declared case scores survived, never a pass` → `code_status: survived`,
  `conflicting_words: []`).
- **A3 still red, for exactly the predicted reason:** `"expected exactly one '| coverage |'
  row, found 23"`. The row still names only the round-84 receipt and
  `.ufo/waves/round-86/l1/` does not exist yet.

**A3-i + A3-ii together take C1 to 3/3** — verified on a full `git checkout` of
`4cc03025e` with exactly two edits (rename the 22 historical `| coverage |` rows; commit
`.ufo/waves/round-86/l1/scores/coverage-selfcheck.json` with a 40-hex `rev` and name it in the
surviving row's evidence cell):

```
RECORD_AGREEMENT agreed=3/3 mismatches=[]
A3-receipt-pointer True {"claim_round": 85, "receipt": ".ufo/waves/round-86/l1/scores/coverage-selfcheck.json", "receipt_round": 86}
```

**Consumer safety, measured against a zero-edit control** (I first got a misleading
reading from a partial fixture; the control separates the effects):

| Audit | control (HEAD, 0 edits) | HEAD + A3 edits | delta |
|---|---|---|---|
| round-73 record-audit | `[]` | `[]` | none |
| round-74 record-audit | `[]` | `[]` | none |
| round-75 record-audit | `['D20_grammar_reds']` | `['D20_grammar_reds']` | none |
| round-76 record-audit | `['D24_capability_rows']` | `['D24_capability_rows']` | none |

`D20_grammar_reds` / `D24_capability_rows` are **pre-existing at `4cc03025e`**, not caused by
the rename. `round-66 --selfcheck` on the fixed fixture: `169/169 missing [] dangling []
mismatches 0`. Census: 0 `E0` findings.

**⚠ F4 is live — the pin must be re-issued.** At `4cc03025e`,
`tools/round-84/freeze-precheck.py` reports
`COUNTER_PIN_MISMATCH:tools/round-84/mutation-closure.py`, verdict **FLAGGED** — exactly as
predicted in §2. Re-issuing both `loaded_by_counter` and `target_instruments` for that file
to the post-repair digest restores `verdict: CLEAN`, `met: true` (verified on the fixture).
**Independent of A3** — either order works.

### Remaining L1 work, itemised
1. Re-issue the `tools/round-84/mutation-closure.py` pin in `.ufo/waves/round-86/claims.json`
   (both `loaded_by_counter` and `target_instruments`).
2. **A3-i** — rename the 22 historical `| coverage |` rows in `SCORECARD.md`.
3. **A3-ii** — commit `.ufo/waves/round-86/l1/scores/coverage-selfcheck.json` (40-hex `rev`)
   and name it in the surviving row's evidence cell.
4. Re-run both counters at the measured revision: C1 → 3/3, C2 → 5/5 (already green).

No counter byte, atom rule, plan file, `claims.json` atom text or `pre/` receipt needs to
change for any of this.

## Fixture drivability

Both counters accept `--worktree` and both were driven to a green fixture:
`record-agreement.py --root . --worktree <fx>` → `agreed 3/3 mismatches []`;
`gate-registry.py --root . --worktree <fx> --work <scratch>` → `agreed 5/5 mismatches []`.
Caveat: in worktree mode every read comes from the fixture tree, so only `--rev` exercises
the `git show`/blob-at-rev path; and the tool is always executed from `--root`.

## Census / consumer safety

`bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → 0 `E0`
findings at BASE, and **0** on a fixture that adds the S305 superseding row (`E04` is exempted
because `teaches` matches `/supersedes S[0-9]{3}/`; `W04` remains a warning).
Renaming the 22 historical `| coverage |` rows was checked against every consumer in the lane
(round-25, round-26, round-53, round-66, round-73/74/75/76 record-audits) — **all unaffected**
(`round-66 --selfcheck` on the renamed fixture: `missing []`, `dangling []`, `mismatches 0`;
record-audits: `"defects": []`). That rename is still a rewrite of 22 historical SCORECARD
sections — **an L1 decision**, and the only route that leaves the counter byte-identical.

## Scratch

`/fast/scratch/hyaku/kaidoku-r86/ScoutRecon/` deleted after this report. Fixture repos were
`mktemp -d` + `git -C "$D" init -q` with `rev-parse --show-toplevel` asserted; no mutating
git/jj command touched the lane.
