# ReviewQualityRows — QUALITY.md rows 45–47 at 18be864a528873b2b70d8c94e31f880290249e90

Reviewed `corpus/QUALITY.md` lines 55–57 (rows 45, 46, 47) at the measured tip `18be864a`, read-only via `read`; blob sha256 `da2ddf0930f20e76ba6a498f502b3b3469d1e4f1d7da2520c87dfd86d98e9605`. Each row was checked for (a) a stated criterion, (b) a stated failure condition, (c) a case that resolves to committed bytes, then compared with rows 29, 33 and 44 for overlap or contradiction. Verdicts are observations; anything inferred is labelled.

## Per-row verdict

### Row 45 — claim-specific source row on the entry's `source:` line — holds

- Criterion: a claim whose entry must cite a new source row names that row in its claims file (`claim_row`); the counter accepts only that row — on the entry's `source:` line, new since the base, status mined, opened in the round, listed in the round lesson's `## Gate`; another new row meeting the same conditions does not satisfy.
- Failure condition: "a counter passes an entry that cites a different valid new row."
- Case resolves to committed bytes: `.ufo/waves/round-29/claims.json` carries `"claim_row": "S088"` (R29-C1, line 43) and `"claim_row": "S087"` (R29-C2, line 56). The counter check at `tools/round-29/c1-fresh-naming.py:346-351` requires exactly `CLAIM["row"]` among the `source:`-line tokens, present in SOURCES rows, absent at `--base`, `rows[s][7]=="mined"`, `rows[s][8]==OPENED`, and in the lesson's Gate ids — all five named conditions plus claim-row identity. Both selftests ship `red-cites-other-new-row` (fixture: valid new row S003 cited instead of S002; `c1-fresh-naming.py:560`, `c2-filtered-unseen.py:322`) and both receipts print `ok red-cites-other-new-row exit=1 want=1` (`.ufo/waves/round-29/before/c1-selftest.txt:20`, `c2-selftest.txt:17`, both `exit=0`, utc 2026-10-22T20:01:31Z/33Z).
- `why` resolves: `corpus/lessons/round-28-verifier-spotcheck.md` "Routed defects" item 6 — "Both round-28 counters accept any new Gate row on the entry's source: line; require the claim-specific row named in the claims file" — and `corpus/lessons/round-28.md` "Routed to future rounds" bullet 1.
- Row 29 comparison: sharpens, no contradiction. Row 29 requires the cited row be "opened, mined" with `used-by` naming the entry; row 45 adds claim-row identity plus new-since-base and Gate-listing. Row 45 does not restate row 29's `used-by` back-link — under the preamble's "supersedes only when named" convention it sharpens (adds), so row 29's `used-by` requirement stands alongside. Observation: the round-29 counters do not check `used-by`; SOURCES S087/S088 `used-by` cells name their own entries anyway (SOURCES.md:93-94), so the real rows satisfy both rows.

### Row 46 — every claims*.json audited, ledger checked with `--disclosures` at filing — holds

- Criterion: the claim-freeze audit covers every `claims*.json` a round commits; the freeze ledger is checked with `--disclosures` before filing, gate exit code in the report.
- Failure condition: "a round's second claims file is audited by hand only, or when the ledger disagrees with its gate at filing."
- Case resolves to committed bytes: `tools/round-29/freeze-gate.py:57` matches `claims[A-Za-z0-9_.-]*\.json` per file, keys `round-N` or `round-N/<file>` (`:62-63`), each audited at its own first-add commit (`:98`). The v2 gate audited 19 freezes — `audited: 19` in `.ufo/waves/round-29/after/freeze-gates-v2.txt` vs `audited: 16` for the round-24 gate in `freeze-gates-at-dbd87cfa.txt` — the 3 extra being `round-14/claims-review.json`, `round-15/claims-review.json`, `round-28/claims-c2.json` (exactly the stated "two claims-review.json files and round-28 claims-c2.json"; all 19 rows present in `corpus/claim-freezes-v2.tsv`). The round-24 gate with `--disclosures` at `7431096b` printed `{"exact": 13, "mismatched": ["round-26", "round-28"], "missing": ["round-29"], "of": 16, ...}`, exit 1 (`.ufo/waves/round-29/after/ledger-before-fix.txt`) — `mismatched: [round-26, round-28]` and the exit code match verbatim; the receipt also shows `missing: ["round-29"]` (round-29's claims did not exist at `7431096b`), which the row does not mention but does not misstate.
- `why` resolves: spot-check routed defect 5 — "The round-24 freeze gate reads only claims.json; make it audit every claims*.json (C2 was checked by hand…)" — and `corpus/lessons/round-29.md` M29-2, which describes the same `mismatched` receipt.

### Row 47 — file only after last seat settles, lane tree clean — holds

- Criterion: a round is filed only after its last seat has settled and the lane tree is clean; `tools/round-29/prefile-check.sh <LANE>` exits 0 immediately before the report commit, output in the report.
- Failure condition: "the lane's `git status --porcelain` is non-empty at filing."
- Case resolves to committed bytes: `tools/round-29/prefile-check.sh` (sha256 `20507911c5f51e6e610499838f600b8a8515e05eb6afdeeb93755f887e868d84`) exits 1 on non-empty `git status --porcelain`. The receipt `.ufo/waves/round-29/after/prefile-check-red-r28.txt` shows a scratch clone at `242b0d8b8ad6ff6c693fa5114216fbb538b587bf` (resolves in lane history) first clean (`prefile: clean`, exit 0), then with ExecR27SelftestFix's post-stop bytes printing ` M .ufo/waves/round-28/a2w/ExecR27SelftestFix.md`, `prefile: NOT CLEAN (1 paths)`, exit 1.
- `why` resolves: spot-check routed defect 1 — "The lane closed with a seat still writing: .ufo/waves/round-28/a2w/ExecR27SelftestFix.md modified after 242b0d8b" — and `corpus/lessons/round-29.md` M29-1, which names the same file, the `19:26Z` timestamps and the new check.
- Row 33/44 comparison: no overlap. Rows 33 and 46 govern commit-order at claim-freeze time; row 47 governs worktree state at filing time. Row 44 governs test-set purity. Distinct axes; `supersedes: new` is accurate.

## Contradictions

None found. Row 45 sharpens row 29 additively (row 29's `used-by` clause is not contradicted, only not restated). Row 46 extends row 33's single-file audit; row 33's sentence "the freeze commit is the one that first adds claims.json" is not redefined by row 46 — the v2 gate applies the same definition per file — so a reader who applies row 33 verbatim to `claims-c2.json` could briefly misread which commit freezes it, but the two rows compose without conflict.

## Wording fixes (minor; none block)

1. Row 45: "(a valid new row S003 cited instead of the claim's S002)" could be misread as real lane rows; S002/S003 are selftest fixture ids. Suggest "(fixture: valid new row S003 cited instead of the claim's S002)".
2. Row 45: "the counter accepts only that row" reads, in isolation, as exclusivity over the `source:` line; the counters implement membership (`s in cited`), so an entry citing the claim's row plus a second new row would pass. Suggest "the counter requires that row among its cited rows" if that is the intent.
3. Row 46: "a round's second claims file" fixes the defect to the two-file case the round met; the criterion itself already covers every `claims*.json`. Suggest "any claims file beyond claims.json" for generality.
4. Row 46: "the round-24 gate with `--disclosures` at `7431096b`" does not give the gate's lane path (`.ufo/waves/round-24/tools/freeze-gate.py`); the receipt does. Suggest naming the path so the case resolves without opening the receipt.
5. Row 47: the script checks tree cleanliness only; "its last seat has settled" is enforced by contract, not by the script (the red case works precisely because the seat's bytes were copied into a clone). A clarifying clause such as "(tree-clean is the observable proxy for settled)" would keep the instrument's reach honest.
6. Row 47's failure condition covers only non-empty `git status`; skipping the check or omitting its output from the report fails the criterion but not the stated condition. Optional: append "or when the check was not run or its output is absent from the report".

## Evidence

All findings from `read`/`bash` on the lane at `18be864a`, 2026-10-22, read-only:

- `read corpus/QUALITY.md:55-57:raw, :39/:43/:54:raw` — the six rows verbatim.
- `cat .ufo/waves/round-29/before/c1-selftest.txt c2-selftest.txt` — `ok red-cites-other-new-row exit=1 want=1`; `selftest cases=22/19 failures=0`; `exit=0`. sha256 `72eee81b…`, `16f72215…`.
- `cat .ufo/waves/round-29/after/ledger-before-fix.txt` — `{"exact": 13, "mismatched": ["round-26", "round-28"], "missing": ["round-29"], "of": 16, …}` `exit=1`. sha256 `db3fe8e0…`.
- `cat .ufo/waves/round-29/after/prefile-check-red-r28.txt` — ` M .ufo/waves/round-28/a2w/ExecR27SelftestFix.md`, `prefile: NOT CLEAN (1 paths)`, `exit=1`. sha256 `7f0e8026…`.
- `cat .ufo/waves/round-29/after/freeze-gates-v2.txt` — `"audited": 19` for the round-29 gate vs `"audited": 16` for the round-24 gate at the same rev.
- `grep tools/round-29/freeze-gate.py` — `CLAIMS` regex `:57`, per-file freeze `:98`, `--disclosures` `:177-187`.
- `grep tools/round-29/c1-fresh-naming.py` — cite check `:346-351`, fixture `:509-515`, `red-cites-other-new-row` `:560`.
- `sed -n '84,96p' corpus/lessons/round-28-verifier-spotcheck.md` — routed defects 1, 5, 6 verbatim.
- `grep corpus/lessons/round-28.md` — "Routed to future rounds" `:55`; `corpus/lessons/round-29.md` M29-1..3 `:44-46`.
- `sed -n '35,60p' .ufo/waves/round-29/claims.json` — `claim_row` S088/S087; `grep corpus/SOURCES.md` — S087/S088 rows present with `used-by` naming their entries.
- `git rev-parse 242b0d8b` → `242b0d8b8ad6ff6c693fa5114216fbb538b587bf`; `git log -1 corpus/QUALITY.md` → `18be864a` 2026-10-22T17:16:21-03:00.

No installs were needed; no network, REA, or lookups were used. No tools were installed (no record to report). No artifacts were produced outside this report.
