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
