# ExecCapGrammar — D24 capability-row grammar attack (round-76 w1)

Seat: ExecCapGrammar (executor). Date: 2026-11-04.
Instrument under attack (read-only, never edited):
`tools/round-76/record-audit.py` — in particular
`claimed_capability_rows` / `capability_table` / `capability_defects`
(D24, R76-C1 calibration). Machine-readable results:
`.ufo/waves/round-76/w1/ExecCapGrammar/receipt.json` (`ok: true`).

## 1. Instrument binding (no forgery)

- Imported in-process with `python3 -I -B` via `importlib.util.spec_from_file_location`; no `sys.path` mutation, lane file opened read-only.
- Live module sha256 `805a8ba5ff6c83a374e88db589ff95b6f70b90fee1b102123b47ada22fe70f0e` == `git show HEAD:tools/round-76/record-audit.py` blob == worktree file.
- `claims.json` freeze pin `88e3c2ceca…989` == blob at freeze `5824d5d8` (`freeze_pin_matches_freeze_blob: true`). The pin deliberately does NOT equal the live module: `claims.json`'s supersessions record two revisions — `a8908930…` (backtick-stripped table keys, D12 erratum bound to the round-75 record rev) and the wave-mutation revision (populated absent-row fixture, `cap-wrapped-claim-accepts`). The receipt carries both the recorded reason text and the digest lineage (freeze / supersession / HEAD / worktree).
- `inspect.getsource` equality: `claimed_capability_rows`, `capability_table`, `capability_defects` are byte-identical between the supersession revision and the live module (`grammar_source_matches_supersession_revision` all true). Only `capability_table` differs from the freeze revision — exactly the change the first supersession records.
- The lane is live: HEAD moved during this seat (891902a7 → 98407fad → 1de75ea1 across the checks; `record-audit.py` byte-identical over the move). Results are bound to the sha above.

## 2. Cosmetic battery — every construction a token-presence predicate accepts, the grammar rejects

Each fixture is a full synthetic SCORECARD (`## Capabilities` table + one round-75 claim section), run through `capability_defects(text, exists)` in-process. Every fixture returns ≥1 defect naming its failed shape (exact strings from the receipt):

| id | construction | defect returned |
|---|---|---|
| cos-1-absent-named-row | claim names `phantom capability row`; table holds only a well-formed other row | `round 75 claims row 'phantom capability row': absent from the ## Capabilities table` |
| cos-2-em-dash-evidence | evidence cell is `—` | `row 'a checked capability': evidence cell names no path` |
| cos-2b-single-slash-evidence | path-like token `corpus/x.md` (one slash) | `row 'a checked capability': evidence cell names no path` |
| cos-3-unresolved-evidence-path | well-formed path token, `exists` → False | `row 'a checked capability': evidence path absent at the measured revision: ['corpus/ghosts/receipt-that-never-was.json']` |
| cos-4-round-mismatch | first-working-round cell `74` in a round-75 section | `row 'a checked capability': first-working-round cell '74' does not name the claiming round 75` |
| cos-5-stub-description | three-word description `does a thing now` | `row 'a checked capability': description is fewer than eight words` |
| cos-6-empty-table | claim present, header-only table | `the ## Capabilities table holds no data rows` |
| cos-7-no-claim-line | round section with no claim line | `no round section claims \`Capabilities rows appended\`` |

No cosmetic fixture passed. (Blocking-defect clause not triggered.)

## 3. Accept probes — the grammar is not reject-everything

- `acc-1-well-formed-row`: one well-formed row + matching claim → `defects: []`.
- `acc-2-real-two-names-wrapped`: table rows `A12 case-independence closure` and `exact-grammar record audit`, claim wrapped exactly as committed at the freeze rev (backticked name straddling the wrap) → `defects: []`.
- Live landed card: `capability_defects` over the working-tree `SCORECARD.md` with real `os.path.exists` → `defects: []` (landed table is green under the live grammar).

## 4. The wrapped claim line at the freeze rev

Source: `git show 5824d5d8e135194a59db3df1533b76ff479753bf:SCORECARD.md`, lines 5868–5869:

```
**Capabilities rows appended** in the table above (`## Capabilities`): `A12 case-independence
closure` and `exact-grammar record audit`, each with its `l1/scores` receipt.
```

- Paragraph-level parser (`claimed_capability_rows`): exactly one claim on the whole card — round 75, `line: 5868`, names exactly `["A12 case-independence closure", "exact-grammar record audit"]` (receipt.wrap.paragraph_parser_recovers_exactly_two_names).
- Line-level parsers both fail:
  - scoped (claim phrase must share the line with its backticked tokens): `[]` — on line 1 the A12 backtick pair is unclosed (so even the truncated name is not extractable) and `## Capabilities` is grammar-skipped; line 2 carries no claim phrase and is never examined. Both true names missed.
  - blind (backtick scan of the claim's own lines, phrase ignored): `["and", ", each with its"]` — the straddled backtick shifts pairing, corrupting the name into two phantom fragments. Neither fragment is the true name; both are absent from the landed table (`phantom_fragments_absent_from_landed_table: true`), so a line-level parser would file false-positive "absent row" defects on `and` / `, each with its` while never recovering the real claim.

## 5. Committed selftest names through `--selftest`

`python3 -I -B tools/round-76/record-audit.py --selftest` → rc 0, 18 cases, `failures: []`. All six committed red names present and passing: `cap-absent-row-red`, `cap-empty-evidence-red`, `cap-absent-evidence-path-red`, `cap-round-mismatch-red`, `cap-stub-description-red`, `cap-no-claim-line-red`; plus `cap-complete-accepts` and the new `cap-wrapped-claim-accepts`. (The committed `pre/audit-selftest.json` shows 17 cases; the live instrument gained the wrapped case via the wave-mutation supersession.)

## 6. Cross-revision check

The same battery was run against a scratch copy of the freeze-blob module (`git show 5824d5d8:…record-audit.py`): identical verdicts on all 9 fixtures (`cross_revision.all_batteries_agree: true`). One divergence probe reproduces the recorded supersession in behavior: a table row whose first cell is backticked (`` `a checked capability` ``) with a bare claim name → freeze grammar flags `absent from the ## Capabilities table`; live grammar accepts. The attack results therefore hold for the frozen grammar too, except for that one recorded key-normalization change.

## Risks / notes

- The lane HEAD is a moving target (two moves observed mid-seat). The receipt binds everything to module sha `805a8ba5…`; if a later commit touches the three grammar functions, this battery must be re-run before the seat's evidence is consumed.
- A validator that naively compares the `claims.json` freeze pin against HEAD will see a mismatch; it is fully covered by the recorded supersessions (digest lineage + reasons are in the receipt).
- No blocking defects found. No lane files outside this evidence directory were written; the scratch dir was deleted.
