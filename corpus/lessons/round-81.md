# Round 81 — registry columns and the committed-record boundary

**Declared freeze:** `4bb318a8e6393e533ea89c3dacaa6e64889cbb42` (first claims container). Declaration `abdcfd3c28d98288a3dc6b4e98c88d115ed42b53` already committed the fixed predicates, counting counter and red controls before wave candidate data. The target at the container freeze is a byte-identical round-80 battery copy; the revised target is a disclosed subject change, not a replacement counter.

## Mistakes

| id | class | evidence pointer | captured-by | fix and shown failure |
|---|---|---|---|---|
| M81-1 | number-drift / row grammar | `pre/c1-base.json`: 129 rows, seven nonconformant, exit 1; r80 outside review kept the row debt named | frozen `tools/round-71/registry-census.py`; registry delivery criterion 92 | Preserve the entire base path population and four historical exceptions; repair the seven malformed rows to seven meaningful cells. Candidate independently reviewed by ReviewerC1-12; both purpose pipes must be escaped in the attack-gate row, not misclassified as pinned inputs. |
| M81-2 | survivor / wrong observation boundary | `pre/c2-base.json`: omission of the fixture commit leaves pristine and mutant 9/0, survivor 1 | none in the old FakeModule cases; QUALITY 141 now states the boundary | Two real-reader integration cases commit PROVINCE then poison its working file. The candidate is green 11/0 but omission makes the named clean case fail and retains an 11/2 summary (`w1/ExecRecord/counter.json`). This is not a sole-detector claim: the duplicate case also fails. |
| M81-3 | number-drift | r80 outside D1: SOURCES search says “two included (S297/S298)” and “Rows 202 -> 204” although S297 was withdrawn | registry census plus CORPUS append-only correction rule | New source search correction preserves the original note and states two admitted documents = one reused row S049 + one added row S298, 202 -> 203. The base source count is 203 in `pre/sources-start-counts.json`, not the note's 204. |
| M81-4 | number-drift | r80 outside D2: three SKILL selftest counts 33/8/14 versus committed registrations 34/9/16 | row 74 count/tally check; `w1/ExecRegistry/d2-counts.json` | Correct only the three declared tallies to 34/9/16; no older instrument bytes change. Red-before values stay in the original base row blobs and candidate-edits. |
| M81-5 | attribution / reference-drift | r80 outside D3/D4: filed report says “the three claim rows and the four capability rows” and “All receipts are in `.ufo/waves/round-80/l1/scores/`” | outside spot-check; QUALITY 65 | Appended errata here and in this round's report: three capability rows, not four (four were registry rows); live receipts additionally reside at `w1/ExecBinder/live-16dfa009.json` and `w1/CriticClaims/c1-live-head.json`. The old filed report is untouched. |
| M81-6 | reference-drift | r80 outside D6: freshness summary command cited b00419fb while its receipt names 6037f599 | outside receipt re-derivation | Owned-axes command now cites 6037f599; old -> new is explicit here. Both commits produced the same 34-receipt population and unexpected 0, so no score delta is claimed for this repair. |
| M81-7 | stale-premise | r80 outside D7: `w1/ExecProv/selftest.txt` has 19 cases / 3 failures before the final repaired instrument; final result 16 cases / 0 failures | outside timestamps and byte provenance | Mark the old seat output superseded, not rewritten: use the committed round-80 final selftest/provenance evidence and the source registration count. No current claim relies on the stale seat file. |
| M81-8 | vacuous / counter predicate gap | `w1/ExecCounter/undersized-pristine.json` and `dirty-pristine-summary.json`: counter exit 0 on pristine 1/0 or 11/3 | ReviewerC2-13 and ExecCounter, not counter `ok` | Frozen counter stays immutable. Review the full declared conjunction from retained summary data and binder digest, separately from `ok`; record the missing enforcement as future instrument debt. No claim that this counter alone enforces every prose obligation. |

All `pre/` and `w1/` evidence paths in this lesson resolve beneath `.ufo/waves/round-81/`.

## Gate

Opened by L1 on 2026-11-04:

| source / decision | URL and location | located quote (<=25 words) | scoped use |
|---|---|---|---|
| S258, admit by reuse | https://github.github.com/gfm/ — Tables (extension), retained `l1/sources/gfm.html:4575-4576`, SHA256 b153d814fdfc8624bb6da7449162c1cd707a637f7d1c1b636eb44b9cf63fa220 | “Include a pipe in a cell’s content by escaping it, including inside other inline spans:” (15 words; newline normalized) | Primary specification for escaping the two purpose-cell pipes; not permission to widen the registry's custom seven-cell rule. |
| S255, admit by reuse | https://git-scm.com/docs/git-show — DESCRIPTION, plain blobs paragraph, native reader fetched this round | “For plain blobs, it shows the plain contents.” (8 words) | Official object-read semantics; the real reader demonstration, not the documentation alone, proves the local boundary. Raw urllib fetch returned 403 separately; no fresh raw-HTML snapshot/hash is asserted. |
| S261 usage, reject as evidence for this boundary | https://git-scm.com/docs/git-diff — DESCRIPTION, `--no-index` form, native reader fetched this round | “This form is to compare the given two paths on the filesystem.” (12 words) | Scope rejection: filesystem comparison is not a committed-blob read. Flip: a claim comparing filesystem paths. Primary docs remain tier A for their own semantics; no duplicate source row appended. |

Consumer check for the rejected form: the real binder `git_show()` calls `git show`, not `git diff --no-index` (`tools/round-80/pointer-bind.py:108-111`). This is rejection of a proposed usage, not a claim that the complete git-diff manual is irrelevant.

Source changes, each used-by only; status `mined` and recheck `on-release` unchanged:

- S255 old: `plans/round-55-claims.md, tools/round-55/corrections-pin.py, corpus/lessons/round-55.md`; new: that list plus `corpus/knowledge/2026-11-04-r81-registry-and-record-boundary.md, corpus/lessons/round-81.md`.
- S258 old: `plans/round-58-claims.md, SKILL.md, corpus/lessons/round-58.md`; new: that list plus `corpus/knowledge/2026-11-04-r81-registry-and-record-boundary.md, corpus/lessons/round-81.md`.
- No source ID reused or renumbered. No new source row is needed; rows remain 203, tier counts A185/B10/C8 and status mined184/rejected19, subject to the retained round-end census.

Bounded search: three official pages identified and screened; two admitted existing sources, one refused usage, zero new rows. Stop: each claimed boundary has direct primary documentation. Source access and old/new cells: `l1/sources/access.json`, `changes.json`. No staged shokuknow theme was adopted: **Assimilation: none**. The deployment prompt identifies no kaidoku considerthese directory; the lane root listing also contains none.

Outside spot-check of this round's gate decisions remains for the non-author integrator. Dispatched seats are still this lane and do not satisfy that duty.

## Carried timeline correction and limits

R80 outside D5 observed report author-time earlier than the cited lane tip, while committer-time and content ordering were correct. Round 81 invokes the serialized fleet helper only after the final lane push; the helper's `metaedit --update-author` sets the fresh author identity/time. No historical commit or filed report is rewritten.

The printed-command executor's round-specific prefix restriction, round-78 receipt-auth/gate-exits limits and the r63 record-section sweep stay explicit debt; no third claim is inferred. The actual printed commands will be executed by L1 against the integrated commit and retained, with their real exit codes.

## Integrated measurements and newly discovered disclosure defect

Measured work `047d18ff49d3f41d8199fadfb545e2d4cbf475e1`:

- Frozen census: exit 0, 131 rows, zero nonconformant/duplicate, four multicell exceptions; its unchanged selftest 14/0. Independent retained population review finds no base path removed and exactly two new tool rows; all seven repaired rows are seven cells and the four round-69 rows byte-identical (`l1/scores/full-obligations.json`).
- Frozen omission counter: exit 0, one mutant killed, zero survivors; pristine 11/0 and mutant 11/2. The exact frozen binder digest is retained and matches; all nine old case names appear first in pristine output. Direct canonical-layout selftest also exits 0, 11/0 (`l1/scores/selftest-canonical.txt`).
- Source census end exits 0: 203 rows, malformed 0, A185/B10/C8 and mined184/rejected19 unchanged (`sources-end.txt`, `sources-end-counts.json`). Corpus index retains 164/164 knowledge files mapped (`coverage-no-harm.json`); this is index hygiene, not new domain expansion.

**M81-9 — landing / unresolved frozen name.** `freeze-audit-before-ledger.json` reports the bare `pointer-bind.py` name inside the first round-81 container as `INSTRUMENT_UNRESOLVED`. The full path's top-level digest does not make the frozen gate resolve a bare spelling. Captured-by: QUALITY 33 and the maintained round-29 freeze audit. The defect remains permanent at this freeze; do not rewrite the predicate after data. Fix shown able to fail is the actual flagged audit and a truthful disclosure row, not a claim that the freeze became clean. Next freeze must name full script paths before data.

The same maintained audit found the inherited round-80 ledger row absent and its real state FLAGGED: `INSTRUMENT_UNPINNED` for the round-79 control binder and `INSTRUMENT_REVISED` for three c935b543 counter revisions missing from supersessions. The prior outside review explicitly did not execute the lane's gates; these new results do not rewrite its reviewed observations. Round 81 appends the actual round-80 and round-81 disclosure rows. Exit 0 of a disclosures consistency gate is not a clean-freeze verdict.

The 11-seat WAVE-DONE handoff contains seven substantive outputs and four empty outputs. No replacements were dispatched. L1 completed the source/lesson work that empty drafting seats did not deliver; these empties receive no verification credit. Actual provider error text is recorded only when the orchestrator supplies it.

## Standing-duty red receipts and repairs

The final-record checks at `bcd3f78e2a7168548269f1edebdb627a0696fc74` exposed two inherited defects beyond D1–D7; both are repaired rather than suppressed:

- **M81-10, landing / missing cross-round supersession.** `l1/scores/gate-at-record.json` exits 1, disclosures exact 55/56: round-78's container lacks the round-80 `b8260107` attack-gate selftest revision. The revision was disclosed only in round-80's own container. Captured-by QUALITY 33/46 and the maintained audit. Append the missing `(tools/round-78/attack-gate.py, b8260107, reason)` to round-78 supersessions, preserving all frozen claim strings, pins and historical outputs.
- **M81-11, provenance / unrecoverable inherited crosscheck producer.** The standing sweep extended through round 81 reads 45 receipts and exits 1: one unexpected flag, `round-80/l1/scores/c3-crosscheck-execguard-base.json`, whose declared guard-battery digest `efa1a889…` matches no committed production blob. The retained worker candidate has digest `d97fcc60…`, so it cannot honestly be substituted as the claimed producer. Captured-by the unchanged round-80 provenance sweep. Preserve original bytes at `.ufo/waves/round-81/l1/archive/c3-crosscheck-execguard-base.original.json` and genuinely re-run the committed guard counter against the original round-79 base. Replacement is explicitly an L1 round-81 re-observation, **not** the original independent ExecGuard run; its new timestamp and producing digest are real. It reproduces the red baseline: guards 9, rows/bound 0, survivors 9, pristine 29/0, exit 1, validation defect-free. Full original/replacement identities, argv and author distinction: `l1/inherited-crosscheck-supersession.json`; run: `l1/scores/inherited-crosscheck-retake.txt`. No historic success or independence is manufactured.
