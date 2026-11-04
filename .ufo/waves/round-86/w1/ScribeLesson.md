# ScribeLesson — round 86, kaidoku (seat report)

Seat: scribe. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, round 86, wave `r86-w1`.
BASE `2cf0b7ff93c698809bed321f7338276a22d6beb9`; declaration `b205bb8b66ec7b61e028bccd92f64eade8942461`
and `ec9963eb9e5c1eedfada9a69f073c1639e7911f9`; integration `4cc03025e6d4f6f1e00b5e402fcc0180e6e730bc`;
L1 record commit `63c30e9d37556bd14fc21ec172d079f676684a2d`.

**Status: my draft is superseded.** The L1 wrote and committed `corpus/lessons/round-86.md` and the
two QUALITY rows (150, 151) itself, at `63c30e9d`. The L1 instructed this seat to make no further
edits, delete its scratch, and yield. The lesson draft I had prepared under
`.ufo/waves/round-86/w1/ScribeLesson/` is therefore **not** the landed text and is retained only as
this seat's pre-integration draft. **My A3 coverage-row edit was not adopted**, and the L1 states why:
the frozen A3 rule requires exactly one `| coverage |` row and the card carries 23, so the rule was
not re-derived before freeze (the L1's M86-3) and no receipt was created to satisfy the counter.

## Behaviour

The seat's task was to draft `corpus/lessons/round-86.md` and the two QUALITY.md criterion rows the
round's evidence supports, as **candidates only**. The drafts exist under this seat's wave directory
and are not integrated; the landed texts are the L1's.

What the draft derived, independently of the L1, from committed and wave-tree bytes:

- **M86-1 (the mined mistake, the round-85 correction class).** The round-85 S303 correction was
  filed as a lesson correction (`corpus/lessons/round-85.md` Corrections C-R2) while the registry
  cell that states the count — `corpus/SOURCES.md:219` — kept the wrong value ("five scopes
  (S083/S090/S092/S119/S123)") for the eight rows that carry `rea-agents-6.5.0.tgz`. Round 85's
  commit `01f2d5193` adds one row to `corpus/SOURCES.md` (S304) and changes no existing cell, so the
  wrong count survived where a reader and a counter read it. **QUALITY 149** ("a counted scope and a
  cited pointer are re-derived at the revision they name") should have caught it and did not, because
  the rule was applied to the **lesson text** rather than to the **registry cell** the rule names.
  The draft's fix: file the correction as a registry row (SOURCES rule 2's supersession row), so the
  count is re-derived by command from the committed bytes.
- **The Gate.** S255 (`https://git-scm.com/docs/git-show`) re-opened this round: HTTP 200, 246 736 B,
  sha256 `a3716a4d6c236082b0f6d08da64735765f376c1c32ba5ede93b70b013f52a9aa` (three fetches this
  round, byte-identical), DESCRIPTION section, served line 3287, quote "For plain blobs, it shows the
  plain contents." (8 whitespace words). The reject kept from the round's set: **S303 stays
  rejected** — a tarball is not an anchored document, S302 is the anchored authority, the flip
  condition is unchanged, and **its supersession does not flip it** (S305 is itself `rejected`).
- **C-R86-2 / A2 docstring.** Old line 8 of `tools/round-84/mutation-closure.py` at BASE: `present in
  the target's own output; an absent declared case is inconclusive, never a pass).` New: `present in
  the target's own output; an absent declared case scores survived, never a pass).` The code assigns
  `survived` in its `not case_present` branch. **Landed** by the L1 at `4cc03025e`; the L1's receipt
  `.ufo/waves/round-86/l1/scores/c1-at-integration.json` carries `A2-docstring-status ok: true`.
- **C-R86-3 / A3 pointer.** Old cells 3 and 4 of the `| coverage |` row (the evidence pointer and the
  own round `85 (…at the round-85 record…)`); new cells naming
  `.ufo/waves/round-86/l1/scores/coverage-at-landing.json` and round 86. **Not adopted** by the L1,
  for the reason above.
- **The two QUALITY rows the round's evidence supports**, in the existing numbered style, next free
  numbers 150 and 151: (a) a correction filed in prose leaves the record wrong where it is re-derived
  — the supersession row is the correction, and its count is re-derived by command; (b) a registry row
  is a claim about behaviour — its entry command is executed and its declared exit observed, or the
  row is decoration. The L1 landed its own wording of both rows at `63c30e9d`, citing the same
  round-86 mistake ids.

## Gates

- **R86-C1 (calibration).** BASE `agreed 0/3` (`pre/c1-at-base.json`). At the integration revision
  `4cc03025e` the L1's receipt reads `agreed 2/3`, `mismatches ["A3-receipt-pointer"]` — A1 and A2
  agree, A3 does not. The `substring-only` control accepts at BASE and at integration
  (`mismatches []`, `ok true`), as the plan requires of a false-green control. **R86-C1 is missed on
  its frozen target**; the L1 records it so, and records the A3 cause as M86-3.
- **R86-C2 (operability).** BASE `agreed 0/5` (`pre/c2-at-base.json`); at `4cc03025e` the L1's receipt
  reads `agreed 5/5`, `mismatches []`, with `G3-self-invocation` detail
  `{"argv": ["-B", "tools/round-85/predicate-bind.py", "--selftest"], "declared_exit": 0,
  "observed_exit": 0, "last_line": "SELFTEST cases=21 failures=0"}`. **Not admitted**, because
  operability is not an owned lane axis.
- **This seat's own gate checks.** The counter was re-run by this seat at BASE (exit 1, `agreed 0/3`,
  matching the frozen pre-receipt) and at the integration revision (exit 1, `agreed 2/3`), under both
  the frozen production counter and the hardened candidate counter; the S255 page was fetched three
  times and hashed; the S303 row count was re-derived with `grep -c -F` at BASE. **No claim target was
  re-measured to a landing verdict by this seat**, and none is asserted.

## Touched surfaces

Writes, all inside this seat's own wave directory (`.ufo/waves/round-86/w1/ScribeLesson/`):

- `lesson.md` — the pre-integration lesson draft (218 lines; the sections `## Mistakes`, `## Gate`,
  `## Corrections (append-only)`, `## QUALITY rows`, `## Wave`, `## Limits`, in that order).
  **Superseded** by `corpus/lessons/round-86.md` at `63c30e9d`.
- `quality-rows.md` — the two QUALITY rows in the existing numbered style (150, 151) with their
  citations, plus notes for the L1. **Superseded** by the L1's rows at `63c30e9d`.
- `sweep.txt` — the command that shows the S303 cell wrong at BASE, with its output: the eight rows
  carrying `rea-agents-6.5.0.tgz` (S079, S080, S083, S090, S092, S119, S123, S303) and the counter's
  A1 detail (`url_rows` = the same eight; "no row whose teaches opens `supersedes S303`").
- `receipts/` — nine retained receipts: `c1-at-base-rederived.json`,
  `c1-at-integration-rederived.json`, `c1-at-integration-candidate-counter.json`, `a2-after.json`,
  `a3-after.json`, `a3-after-under-production-counter.json`, `all-three-after.json`,
  `all-three-after-candidate-counter.json`, and the S255 snapshot `git-show-2026-11-04.html`
  (sha256 `a3716a4d…`).

**No production file was edited by this seat and nothing was committed by it.** Verified at the end:
`git status --porcelain | grep -v '^??'` is empty — no tracked file in the lane is modified. The only
lane-tree writes are this seat's files under `.ufo/waves/round-86/w1/ScribeLesson/`.

## Out of scope

- The lesson text and the QUALITY rows themselves: the L1 wrote and committed both at `63c30e9d`.
  This seat's drafts are not integrated and are not claimed as landed.
- The A3 coverage-row correction: **not adopted**; the L1's C-R86-3 records it as unrepaired and
  routes it to the next declaration, with the cause recorded as M86-3 (a frozen rule and its BASE
  description not re-derived against the BASE bytes before freeze).
- The `tools/round-86/gate-registry.py` G3 clause (a self-test cell naming a command on the tool's
  path is not enforced): the L1 records it as M86-2 and routes it, with the behavioural sweep at
  `.ufo/waves/round-86/l1/sweep/g3-behavioural-red.txt` and
  `.ufo/waves/round-86/l1/sweep/g3-foreign-command-accepted.json` as the evidence.
- The axis question (operability is not an owned lane axis) and every other routed item: the L1's.
- Any claim verdict, the round verdict, the wave seat counts and the wave accounting: the L1's.

## Findings

1. **The A3 atom was misspecified at freeze, and this seat's independent re-derivation agrees with
   the L1's M86-3.** The frozen production counter requires exactly one `| coverage |` row in the whole
   file; `SCORECARD.md` carries 23 (lines 23, 179, 258, 317, 363, 404, 450, 492, 522, 551, 605, 736,
   797, 961, 1059, 1535, 2243, 2301, 2359, 2417, 2506, 2948, 3409). Under the production counter the
   two-cell correction leaves A3 false at the *uniqueness* check, before the counter ever reaches the
   receipt it was asked to check — receipt `a3-after-under-production-counter.json`, detail
   "expected exactly one `| coverage |` row, found 23". The hardened candidate counter
   (`.ufo/waves/round-86/w1/ExecRecordAgreement/candidate/…`, sha256 `a8c5a3db6f05…`), whose A3 arm
   selects the row under `## Owned axes`, does reach the receipt — receipt `a3-after.json`, A3
   `ok: true`. The L1 chose not to land either the row edit or the counter change, and routed the
   atom to a successor declaration instead. **Both receipts are retained; neither is presented as a
   landing measurement.**
2. **The plan's BASE description of A3 does not match the BASE bytes.** The frozen plan says the row
   "names only a round-67 receipt"; the row at BASE names five receipts (rounds 84, 76, 75, 68, 67)
   and its own round is 85. The atom's *rule* is unaffected — the row names no receipt at or after its
   own round — but the plan's stated cause was not re-derived before the freeze. This seat found the
   same discrepancy independently before the L1's commit and reported it in the draft.
3. **The correction class is confirmed as the round's own mined mistake.** The round-85 lesson
   carries the correct count ("8 rows / 7 prior") in prose while the registry cell that states the
   count is unchanged since round 84 (`git log -S 'five scopes' -- corpus/SOURCES.md` returns only
   `8ae9c8ee`, round-84). QUALITY 149 was applied to the lesson text, not to the cell.
4. **A curation correction does not flip a rejection.** S303 stays `rejected` with its flip condition
   unchanged, and the superseding row S305 is itself `rejected`, as the L1's landed lesson also states.
5. **The S255 re-open is stable.** Three fetches this round returned byte-identical bytes
   (246 736 B, sha256 `a3716a4d…`); the lane's committed round-55 snapshot is a different byte
   sequence (246 519 B, sha256 `0a95cbcd…`) but the located quote is identical in both, so the quote
   is re-derivable from live bytes and no new single-hash claim is made about a page whose bytes
   differ between snapshots.

## Tooling

No tool was installed, upgraded or removed by this seat; no host service was restarted. The round
used only what the host already provided: `git` (read-only `show`/`log`/`status`/`diff`/`ls-tree`),
`python3` (the frozen counter and its candidate), `curl`, `grep`, and `sha256sum`.

## Artifact paths

All relative to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

- This report: `.ufo/waves/round-86/w1/ScribeLesson.md`
- Superseded draft lesson: `.ufo/waves/round-86/w1/ScribeLesson/lesson.md`
- Superseded QUALITY rows: `.ufo/waves/round-86/w1/ScribeLesson/quality-rows.md`
- BASE sweep: `.ufo/waves/round-86/w1/ScribeLesson/sweep.txt`
- Receipts: `.ufo/waves/round-86/w1/ScribeLesson/receipts/` (nine files, listed above)
- Landed by the L1, not by this seat: `corpus/lessons/round-86.md`, `corpus/QUALITY.md` (rows 150
  and 151), `corpus/SOURCES.md` (S305), `corpus/knowledge/2026-11-04-r86-record-agreement.md`,
  `tools/round-84/mutation-closure.py` (the A2 docstring line), `SKILL.md` (three registry rows),
  `.ufo/waves/round-86/l1/scores/` (five receipts), `.ufo/waves/round-86/l1/sweep/` (three files),
  `LOG.md`, `SCORECARD.md`, `.ufo/waves/round-86/claims.json`.
