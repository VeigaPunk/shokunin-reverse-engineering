# Round 86 — a correction is filed where the record is re-derived, or it is not a correction

Base `2cf0b7ff93c698809bed321f7338276a22d6beb9`; declaration commits `b205bb8b66ec7b61e028bccd92f64eade8942461`
and `ec9963eb9e5c1eedfada9a69f073c1639e7911f9`; BASE receipts commit `b205bb8b`. One v1 wave `r86-w1`.
Integration commit `4cc03025e6d4f6f1e00b5e402fcc0180e6e730bc`.

This lesson records what this round mined and the corrections the round's C1 atoms required. The
round-85 lesson and its spot-check are **not** rewritten; the corrections below are appended text only.

Round 86 declares two claims: R86-C1 (calibration — three record cells re-derive the bytes they
describe) and R86-C2 (operability — the round-85 gate is registered and its row re-derives by running
it). Their verification is the L1's; this lesson does not assert either outcome.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M86-1 | a correction filed in prose leaves the record wrong where it is re-derived: the round-85 correction for S303 was filed as a lesson correction while the registry row kept the wrong count, so a reader who re-derives the cell still reads a wrong number | `corpus/lessons/round-85.md` Corrections C-R2 (the count "8 rows / 7 prior" is stated there) against `corpus/SOURCES.md:219` at BASE `2cf0b7ff93c698809bed321f7338276a22d6beb9`, whose cell still read "the registry already holds this URL in five scopes (S083/S090/S092/S119/S123)"; `sweep.txt` (the eight rows carrying `rea-agents-6.5.0.tgz`, and the counter's A1 detail `url_rows` = S079/S080/S083/S090/S092/S119/S123/S303) and `receipts/c1-at-base-rederived.json` (`A1-s303-supersede-count` false: "no row whose teaches opens `supersedes S303`") | none in round 85 — the round-85 non-author spot-check routed the defect and the round-85 wave answered it by appending prose to the lesson; no gate re-derived the registry cell, so the wrong count survived in the place a reader reads it. Round 86's frozen C1 counter (`tools/round-86/record-agreement.py`, atom A1) is the first instrument to re-derive the cell itself | the correction is filed as a **registry row**, not as prose: SOURCES rule 2's supersession row (a new row whose `teaches` cell opens `supersedes S303 —`) carries the count and the row-id list in the cell the reader re-derives, and the C1 counter's A1 atom re-derives that count from the committed bytes at the measured revision. **Landed** as row `S305` in commit `4cc03025e`; the lesson's prose correction points at the row instead of restating the number |
| M86-2 | a registry row is decoration when it is scored by its text: the lane's own checklist named a tool's behaviour that no instrument could re-derive, because the row that should carry the entry command was never written | `SKILL.md` at BASE `2cf0b7ff93c698809bed321f7338276a22d6beb9` holds **no** row for `tools/round-85/predicate-bind.py` between the `<!-- instrument-registry v2 -->` and `<!-- /instrument-registry -->` markers (`git show 2cf0b7ff…:SKILL.md \| grep -n 'round-85/predicate-bind'` → no match), although the tool itself landed in round 85 (`5ed965638`); `.ufo/waves/round-86/pre/c2-at-base.json` scores that unregistered state `agreed 0/5`, every atom false, `G1-row-present` detail "rows: 0" | the round-85 non-author spot-check (R85-2, carried into round 85's plan) — and, for the first time, a **counter**: the round-86 C2 counter re-derives the row by *running* the tool (`tools/round-86/gate-registry.py`, atoms `G2-exit-map-observed` and `G3-self-invocation`), so a row is admitted only when its entry command is executed and its declared exit is observed | the row is registered in the lane's own checklist and every one of its five fields is re-derived by command. **Landed** in commit `4cc03025e`; the L1's receipt `.ufo/waves/round-86/l1/scores/c2-at-integration.json` scores the landed row `agreed 5/5`, `mismatches []`, at revision `4cc03025e`, with `G3-self-invocation` detail `{"argv": ["-B", "tools/round-85/predicate-bind.py", "--selftest"], "declared_exit": 0, "observed_exit": 0, "last_line": "SELFTEST cases=21 failures=0"}` |

### Why QUALITY 149 did not catch M86-1

QUALITY 149 ("a counted scope and a cited pointer are re-derived at the revision they name") is the
rule that should have caught it: a line that states a count is checked by the command that produces
it, at the revision the line names, **before the line is written**.

It did not fire because the rule was applied to the **lesson text**, not to the **registry cell**.
Round 85 did re-derive the count — `git show 91eeb72f:corpus/SOURCES.md | grep -c -F
'rea-agents-6.5.0.tgz'` returned `8`, seven of them prior rows — and wrote that derivation into
`corpus/lessons/round-85.md` (Corrections C-R2). But the line that states the count in the registry
is `corpus/SOURCES.md:219`, and that line was never touched: the round-85 commit `01f2d5193` adds one
row to `corpus/SOURCES.md` (S304) and changes no existing cell (`git show 01f2d5193 -- corpus/SOURCES.md`
shows a single `+|` line and no `-|` line). The cell's wording "five scopes (S083/S090/S092/S119/S123)"
was still the operative text at BASE, and wrong twice over: it undercounted the prior rows (5 named,
7 present) and it named only the rows whose scope mentions the tarball, not every row holding the URL.

The lesson of the class is not "write more prose". It is that **a correction is filed where the record
is re-derived**. A lesson is where a reader learns *that* a number was wrong; the registry row is
where a reader learns *what the number is*. Answering a routed defect in the first place leaves the
second place wrong, and the second place is the one the lane's own instruments read.

## Gate

| item | decision | source opened 2026-11-04 | judgment |
|---|---|---|---|
| S255 git-show documentation — re-opened this round for the C1 knowledge entry | admit by reuse (mined, tier A) | `https://git-scm.com/docs/git-show` → HTTP 200, 246 736 B, sha256 `a3716a4d6c236082b0f6d08da64735765f376c1c32ba5ede93b70b013f52a9aa` (three fetches this round, byte-identical; snapshot retained at `receipts/git-show-2026-11-04.html`); DESCRIPTION section, served line 3287: "For plain blobs, it shows the plain contents." (8 whitespace words) | grounds the object-read discipline the C1 counter depends on: a record cell's value is read from the object's bytes at a named revision, never from a mutable worktree file. The lane's committed S255 row already carried this document at the round-55 snapshot sha256 `0a95cbcd8868054d851eedb192864798092c597592851989f5d1bb392730168a` (`.ufo/waves/round-55/l1/s255/`, fetched 2026-11-01); this round's re-open re-derives the quote from live bytes. The two snapshots differ in bytes but not in the located quote. **Landed** in commit `4cc03025e`: the S255 row's anchor cell now carries the round-86 re-open (HTTP 200, 246 736 bytes, sha256 `a3716a4d…`) beside the round-55 snapshot digest, and its `used-by` cell names `corpus/knowledge/2026-11-04-r86-record-agreement.md` |

Rejected this round, carried forward unchanged: **S303** (npm tarball `rea-agents-6.5.0.tgz` as
authority for the extraction-gap taxonomy) stays **rejected**. A tarball is not an anchored document
and the URL is already in scope; S302 is the anchored authority; the flip condition is unchanged (a
published REA documentation URL that anchors the gap taxonomy). Round 86 adds a **supersession row**
for S303 — the new row `S305` carries the corrected prior-row count and row-id list in its `teaches`
cell — and **the supersession does not flip the rejection**. A curation correction changes what a row
says; it does not change what a row decides. The superseding row is itself `rejected`, for the same
reason with the same flip condition, and its `teaches` cell says so: "supersedes S303 — S303 stays
rejected and its own row is unchanged; count 7 (S079/S080/S083/S090/S092/S119/S123)".

The C1 knowledge entry cites the S255 row re-opened this round. The entry is the claim's
counter/receipt path: `tools/round-86/record-agreement.py` and the receipts under
`.ufo/waves/round-86/w1/ScribeLesson/receipts/` and `.ufo/waves/round-86/l1/scores/`.

## Corrections (append-only)

These are appended by round 86. The round-85 lesson (`corpus/lessons/round-85.md`) and the round-85
spot-check are not rewritten; where this round's wording differs from theirs, this section governs.

### Correction, round 86 — C-R86-2 (the A2 docstring's status word contradicts the code it documents)

Routed from `corpus/lessons/round-85-verifier-spotcheck.md` §5/§9 (R85-5) and re-derived by the
round-86 C1 counter, atom `A2-docstring-status`.

**Old text** — `tools/round-84/mutation-closure.py`, module docstring, line 8 (1-based) at BASE
`2cf0b7ff93c698809bed321f7338276a22d6beb9` (`cat -A`: the line ends with `pass).` and a newline):

```text
present in the target's own output; an absent declared case is inconclusive, never a pass).
```

**New text** — the same line, docstring only, no code change:

```text
present in the target's own output; an absent declared case scores survived, never a pass).
```

The code assigns `survived` in its `not case_present` branch
(`tools/round-84/mutation-closure.py:202-204`: `elif not case_present:` → `entry["status"] =
"survived"`), and the same docstring's status list already says `survived` for that case at line 12.
`inconclusive` is the code's name for a *different* condition (an anchor that does not occur exactly
once, a non-leaf id, a non-green pristine tool), so the old sentence gave one case two names.

**Receipt that proves the atom went true** — the L1's integration receipt
`.ufo/waves/round-86/l1/scores/c1-at-integration.json` (revision `4cc03025e`, instrument
`tools/round-86/record-agreement.py`, sha256 `99cb8f27cdfdf3bd…`): atom `A2-docstring-status`
`ok: true`, detail `{"code_status": "survived", "conflicting_words": [], "sentence": "an absent
declared case scores survived, never a pass)."}`; the receipt reads `agreed 2/3`,
`mismatches ["A3-receipt-pointer"]`, exit 1. This seat's isolated re-derivation — the docstring
replaced, `corpus/SOURCES.md` and `SCORECARD.md` left at BASE — is `receipts/a2-after.json`: A2
`ok: true`, `agreed 1/3`, `mismatches ["A1-s303-supersede-count", "A3-receipt-pointer"]`, exit 1.
The atom is isolated: only A2 is true, and it is true for the sentence edit alone.

**Landed** in commit `4cc03025e` (a one-line docstring change: `-inconclusive` → `+scores survived`).

### Correction, round 86 — C-R86-3 (the A3 `| coverage |` row's receipt pointer predates the row's own round)

Routed from `corpus/lessons/round-85-verifier-spotcheck.md` §5/§9 (R85-6) and re-derived by the
round-86 C1 counter, atom `A3-receipt-pointer`.

**Old text** — `SCORECARD.md`, the `| coverage |` row of the `## Owned axes` table (line 23 at BASE),
cells 3 (evidence pointer) and 4 (own round), verbatim:

```text
cell 3: `corpus/README.md` Coverage map; `tools/round-66/coverage-selfcheck.py --selfcheck` (atoms A1/A2, `recipe_a_equivalent`, `recipe_a_hidden`); the command A transcript re-run by `--equiv`
cell 4: 85 (self-assessment fraction re-derived at the round-85 record; score unchanged)
```

The row's own round is R = 85, and the newest `.ufo/waves/round-M/l1/scores/*.json` receipt the row
names is M = 84 (`.ufo/waves/round-84/l1/scores/coverage-selfcheck.json`; the row also names round-76,
round-75, round-68 and round-67 receipts). M < R, so the row's own round is covered by no receipt it
names. (The frozen plan's BASE description of this atom — "names only a round-67 receipt" — does not
match the BASE bytes: the row names five receipts and the newest is round-84. The atom's *rule* is
unaffected — the row names no receipt at or after its own round.)

**New text** — cells 3 and 4 only; cell 2 (the evidence prose) is kept byte-for-byte:

```text
cell 3: `.ufo/waves/round-86/l1/scores/coverage-at-landing.json`; `corpus/README.md` Coverage map; `tools/round-66/coverage-selfcheck.py --selfcheck` (atoms A1/A2, `recipe_a_equivalent`, `recipe_a_hidden`); the command A transcript re-run by `--equiv`
cell 4: 86 (self-assessment fraction re-derived at the round-86 record; score unchanged)
```

The row's own round is then R = 86 and the named receipt is M = 86, so M ≥ R; the receipt is a blob
at the measured revision and carries a 40-hex `rev` field.

**Receipt that proves the atom went true** — `receipts/a3-after.json` (this seat's fixture; the two
SCORECARD cells replaced, `corpus/SOURCES.md` and `tools/round-84/mutation-closure.py` left at BASE):
atom `A3-receipt-pointer` `ok: true`, detail `{"claim_round": 86, "covering_receipts":
[".ufo/waves/round-86/l1/scores/coverage-at-landing.json"], "receipt_round": 86, "receipt_revs":
{"…": "<40-hex>"}}`, `agreed 1/3`,
`mismatches ["A1-s303-supersede-count", "A2-docstring-status"]`, exit 1. The atom is isolated: only
A3 is true, and it is true for the two-cell edit alone. With all three corrections applied the same
fixture reads `agreed 3/3`, `mismatches []`, exit 0
(`receipts/all-three-after-candidate-counter.json`).

**This correction is NOT landed, and the reason is a counter property, not a missing edit.** Two
receipts bound it:

| receipt | instrument | result |
|---|---|---|
| `receipts/a3-after.json` | hardened candidate counter `.ufo/waves/round-86/w1/ExecRecordAgreement/candidate/tools/round-86/record-agreement.py` (sha256 `a8c5a3db6f05…`), whose A3 arm selects the `\| coverage \|` row **under the `## Owned axes` section** | A3 `ok: true`; all three atoms `3/3`, `mismatches []` |
| `receipts/a3-after-under-production-counter.json` | frozen production counter `tools/round-86/record-agreement.py` (sha256 `99cb8f27cdfdf3bd…`) | A3 `ok: false`, detail "expected exactly one `\| coverage \|` row, found 23"; `agreed 2/3` |

The production counter's A3 arm requires exactly one `| coverage |` row **in the whole file**, and
`SCORECARD.md` carries 23 such rows (lines 23, 179, 258, 317, 363, 404, 450, 492, 522, 551, 605, 736,
797, 961, 1059, 1535, 2243, 2301, 2359, 2417, 2506, 2948, 3409 — the historical round rows). Under it
the two-cell edit leaves A3 false at the *uniqueness* check, before the counter ever reaches the
receipt it was supposed to check. The L1's own sweep at the integration commit records the same fact
(`.ufo/waves/round-86/l1/sweep/atom-clause-sweep-red.txt`, last lines "# BASE coverage rows (plan
says A3 has one row):" / `23`), and the round's knowledge entry states the same limit at
`corpus/knowledge/2026-11-04-r86-record-agreement.md` ("A3 cannot be met by a record edit under its
frozen rule, because the SCORECARD carries 23 `| coverage |` rows and the rule requires exactly one.
That is reported in the round-86 lesson as a misspecified atom, not relaxed."). Which counter the L1
lands, and whether the instrument digest pinned in `.ufo/waves/round-86/claims.json` needs an
`instrument_supersessions` entry, is the L1's decision; this lesson does not assert a round verdict.

## QUALITY rows (draft, next free numbers 150 and 151)

Two rows are proposed for `corpus/QUALITY.md`, in the existing numbered style, appended at the end of
the file after Row 149. Full text with citations is in `quality-rows.md`.

- **Row 150** — a correction filed in prose leaves the record wrong where it is re-derived; the
  supersession row is the correction, and its count is re-derived by command.
- **Row 151** — a registry row is a claim about behaviour: its entry command is executed and its
  declared exit observed, or the row is decoration.

## Wave

`r86-w1` is one v1 wave of 12 seats — 3 executor, 2 scribe, 1 scout, 2 reviewer, 1 critic, 1
mutation-tester, 1 sentinel, 1 connector; attack roles 5/12 = 41.7 %; one connector; the L1 holds the
planner seat (a disclosed deviation, never a swarm role).

**Seat outcomes, counts, and the round verdict are the L1's and are not filled here.** What this seat
can state from committed and wave-tree bytes:

- Committed at the base and the declaration: `plans/round-86-claims.md`,
  `.ufo/waves/round-86/claims.json` (frozen instruments and pins), the two counters under
  `tools/round-86/`, and the seven BASE/control receipts under `.ufo/waves/round-86/pre/`.
- Committed in the wave: `.ufo/waves/round-86/r86-w1-spec.json` and
  `.ufo/waves/round-86/r86-w1-dispatch.json` (commit `0864a7bdb`).
- Committed at integration (commit `4cc03025e`): the A2 docstring repair, the `S305` supersession
  row, the S255 re-open and `used-by` extension, the C1 knowledge entry
  `corpus/knowledge/2026-11-04-r86-record-agreement.md`, three `SKILL.md` instrument-registry rows
  (`tools/round-85/predicate-bind.py`, `tools/round-86/record-agreement.py`,
  `tools/round-86/gate-registry.py`), and the corpus README coverage-map and index rows. The
  `SCORECARD.md` `| coverage |` row was **not** changed by that commit, so C-R86-3 is not landed.
- The L1's measured receipts at revision `4cc03025e`, under `.ufo/waves/round-86/l1/scores/`:
  `c1-at-integration.json` (`agreed 2/3`, `mismatches ["A3-receipt-pointer"]`),
  `c1-control-at-integration.json` (the `substring-only` control, `mismatches []`, `ok true` — the
  false green the plan requires), `c2-at-integration.json` (`agreed 5/5`, `mismatches []`),
  `c2-control-at-integration.json`, and `c2-mutation-closure-r85-table-at-integration.json`. The L1's
  own clause sweep is at `.ufo/waves/round-86/l1/sweep/atom-clause-sweep-red.txt`.
- This seat's own outputs: `lesson.md` (this file), `quality-rows.md`, `sweep.txt`, and the receipts
  under `receipts/`.

## Limits

- This lesson asserts no claim outcome. The two claims' verification is the L1's.
- C-R86-2 is landed and its atom's receipt is the L1's committed integration receipt. C-R86-3 is a
  **candidate**: its atom's receipt was produced in a fixture under the hardened candidate counter,
  and the same edit leaves the atom false under the frozen production counter for a reason no cell
  edit reaches (23 rows named `| coverage |`). Both receipts are retained; neither is presented as a
  landing measurement.
- No production file was edited by this seat and nothing was committed by it.
- The Gate's S255 re-open is a live fetch this round (three byte-identical fetches, sha256
  `a3716a4d…`; the bytes are retained at `receipts/git-show-2026-11-04.html`). The lane's committed
  snapshot is the round-55 one (sha256 `0a95cbcd…`). The two differ in bytes; the located quote is
  identical in both.
- The `S305` row's exact text is quoted above from the committed `corpus/SOURCES.md` at `4cc03025e`,
  not from a draft: the C1 atom's frozen rule requires a row whose `teaches` cell opens
  `supersedes S303 —` and states the count, and that row *is* the correction M86-1 is about.
