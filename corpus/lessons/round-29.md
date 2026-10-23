# Round 29 — fresh-carrier test of the round-25 EVM naming rule; unseen-selector test of openchain's `filtered` flag

Author: kaidoku L1, round 29, attempt 1 (in-session hyaku lane subagent). Lane-round base
`bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47`. Both claims frozen together at `dbd87cfa`
(`.ufo/waves/round-29/claims.json`) before any REA run, lookup or fetch; data at `4fcea978`.

## Claims

- R29-C1, coverage (learning claim): the round-25 primary naming rule scored, unchanged, on 16
  fresh carriers compiled from published interface lists and 152 held-out selectors that appear
  nowhere in the lane at the base. Target `runs_ok 16/16`, `rows_complete 152/152`,
  `tally_equal 1`, `entry_ok 1`, exit 0. Observed triple: named 122, right 122, wrong 0.
- R29-C2, depth (learning claim): openchain's `filtered` flag follows Sourcify's `filterResponse`
  on 178 selectors with no openchain response in the lane at the base (26 canonical keys, 152
  R29-C1 selectors). Target `responses_complete 178/178`, `mismatches 0`, `predicted_true >= 1`,
  `predicted_false >= 1`, `entry_ok 1`, exit 0. Observed: 252 entries, 0 mismatches, 38 predicted
  true, 214 predicted false.
- Not claimed: calibration. The six routed defects of `corpus/lessons/round-28-verifier-spotcheck.md`
  are handled as hygiene (SCORECARD round-29 section).

## Gate

Sources opened on 2026-10-22 by the L1 with plain `curl` and `git ls-remote` (files kept under
`/fast/scratch/hyaku/kaidoku-r29/l1/src/`). Each quote is contiguous served bytes, at most 25 words
(QUALITY row 42). S087 and S088 are new rows. No existing row changed status, recheck or used-by.

| row | source and access date | sha256 of the bytes read | located quote (at most 25 words) | section |
|---|---|---|---|---|
| S087 | https://raw.githubusercontent.com/argotorg/sourcify/0966a3bcf13a46b335dae390a0c95b3b0d980c69/services/4byte/src/api/handlers.ts and, same commit, `services/4byte/src/utils/canonical-signatures.json`; opened 2026-10-22T19:52Z (`git ls-remote`: HEAD = staging = `0966a3bc`, master = `189cd726`) | handlers.ts `30981efbc7bc1b541954eb75767c8154562f4f77a9bfc1ad22cf19c8996c5a38`; canonical-signatures.json `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2` (both equal to the master copies, S084 and S085) | `signatureItem.filtered =` / `signatureItem.name !== expectedCanonical.signature;` (two consecutive lines) | `:47-48`, in `filterResponse` `:39-66` |
| S088 | https://raw.githubusercontent.com/ethereum/ERCs/3c0f7076cf20d70bdd6142f012d8e03322f4518c/ERCS/erc-4626.md; opened 2026-10-22T20:00Z (`git ls-remote`: master = `3c0f7076`) | `698c05bff73bfb796f59cd7c4732edccdf7e40176f9bb027c19a0bbe7251e10a` | `This standard is an extension on the EIP-20 token that provides basic functionality for depositing` | `:18`, Abstract; method blocks `:54`–`:481` |

Considered and not made rows: the master copies of handlers.ts and canonical-signatures.json
(byte-identical to S084 and S085, already rows). The other 15 carrier interface lists were not
opened this round (search log entry, `corpus/SOURCES.md`).

Gate notes (after the fetch, by the L1, checked by wave-1 seats `ExecCanonicalHash` and
`CriticMisKeyed`): over the S087 bytes, 6 of the 31 kept signatures do not hash to their key
(receipt `.ufo/waves/round-29/after/canonical-keyhash.txt`; entry section "Mis-keyed list
entries"). This is a reading of the list, not a counter output; the row's teaches cell does not
state it. The same reading makes S085's teaches cell "with the signature it keeps for each" wrong
for 11 of the 36 keys (5 keep none, 6 keep another selector's); rows are not edited in place, so
the correction lives here and in the pointer appended to the round-28 entry.

## Mistakes

| id | class | evidence pointer | captured-by | fix and how it was shown able to fail |
|---|---|---|---|---|
| M29-1 | a round was filed while one of its seats was still running; the seat rewrote its report into the lane tree after the filing commit | round-28 spot-check routed defect 1; the seat's report was first committed in the filing commit `242b0d8b` (19:25:35Z) and its later bytes carry a 19:26:31Z run (wave-1 critic `CriticMistakes`); at this round's start `git status --porcelain` printed ` M .ufo/waves/round-28/a2w/ExecR27SelftestFix.md` | the round contract ("cancel or settle every seat before filing"), which no tool checks | The file is committed as evidence (`7431096b`). Corrected after the wave: a tree-clean check cannot see a seat that writes after the filing, and on a clean clone at `242b0d8b` the tree step passes (`prefile-gate-at-filings.txt`). The first receipt (`prefile-check-red-r28.txt`) is red only on bytes from after the filing, so it detects the leftover at the next round's start, not the live seat. A live seat is visible only in the session's job listing; the round-29 report records that listing before filing. Not shown able to fail as a filing gate |
| M29-2 | the claim-freeze ledger disagreed with its gate at three filings, and red `--disclosures` results that round-27 seats reported were not carried into the lesson or SCORECARD | the round-24 gate with `--disclosures` exits 1 at the round-26, round-27 and round-28 filing commits `fe3eb4ed`, `4084d897`, `242b0d8b` (`.ufo/waves/round-29/after/prefile-gate-at-filings.txt`) and at `7431096b` (`ledger-before-fix.txt`: `mismatched: [round-26, round-28]`). Round-27 seats `CriticFreeze` and `ReviewFreezeRow` got exit 1 and reported it; round-28 seat `CriticC1Miss` asked for the run and no receipt exists (critic `CriticMistakes`). The round-26 row was wrong when written | the gate's own `--disclosures` check (QUALITY row 33): it existed and was run by seats, but its exit code gated nothing | Rows corrected with pointer notes. `tools/round-29/prefile-check.sh` now runs both gates with `--disclosures` and exits 1 when either does. Shown able to fail on the real filing states: clean clones at `fe3eb4ed`, `4084d897` and `242b0d8b` each give `prefile: FAIL`, exit 1 (`prefile-gate-at-filings.txt`); at the round-29 tip both gates exit 0 (`freeze-gates-v2.txt`) |
| M29-3 | the L1's own freeze file names a script it does not pin — a recurrence of the round-28 ledger finding (a script named in claim text and flagged) | `tools/round-29/freeze-gate.py --rev dbd87cfa` flags round-29 `INSTRUMENT_UNPINNED tools/round-28/c1-heldout-naming.py` (`.ufo/waves/round-29/after/freeze-gates-at-dbd87cfa.txt`): the C1 `primary_rule` text says "unchanged from tools/round-28/c1-heldout-naming.py", a reference, not a file the counter runs. The round-24 gate existed before the freeze and flags the same path | the freeze gate, run only after the freeze commit | Disclosed in both ledgers. Proposed: run the gate on a scratch-clone commit of the candidate claims file before the real freeze. That is a procedure with no script or receipt, so it is not shown able to fail |
| M29-4 | red results that seats report to the L1 are dropped at integration, and each round adds a rule that nothing enforces by exit code | M29-2's dropped round-27 ledger result and skipped round-28 run; M29-1 and M29-3's fixes as first written were procedures, and their "able to fail" receipts were the detectors, not steps that would have stopped a filing (wave-1 critic `.ufo/waves/round-29/w1/CriticMistakes.md`) | none | One exit-code gate at filing, `tools/round-29/prefile-check.sh` (tree clean, both freeze gates with `--disclosures`), red on the real round-26, round-27 and round-28 filing states (`prefile-gate-at-filings.txt`); the report runs it last and records the output. The seat-settled condition stays a session check |

Correction (R29-C1 carrier provenance, round 30): only carrier n04 rests on an opened source (S088); the other 15 lists were written from the L1's knowledge of the standards and are author-selected names, not opened published interfaces (wave-2 `ReviewCorrections.md`). The frozen files `tools/round-29/make-carriers.py` and `.ufo/waves/round-29/claims.json:49` keep their wording.
