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

Gate note (after the fetch, by the L1): over the S087 bytes, 6 of the 31 kept signatures do not
hash to their key (`corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md`, Rule). This is
a reading of the list, not a counter output; the row's teaches cell does not state it.

## Mistakes

| id | class | evidence pointer | captured-by | fix and how it was shown able to fail |
|---|---|---|---|---|
| M29-1 | a round was filed while one of its seats was still writing into the lane tree | round-28 spot-check routed defect 1; at this round's start `git status --porcelain` printed ` M .ufo/waves/round-28/a2w/ExecR27SelftestFix.md` (seat `KaidokuR28a2.ExecR27SelftestFix`, 19:26Z timestamps, after the 19:25Z hard stop) | the round contract ("cancel or settle every seat before filing") — a rule, but nothing checked it | The file is committed as evidence (`7431096b`). New pre-file check `tools/round-29/prefile-check.sh`: exit 1 when the lane's `git status --porcelain` is non-empty. Shown able to fail on the real r28 state: `.ufo/waves/round-29/after/prefile-check-red-r28.txt` (a scratch clone at `242b0d8b` with the seat's later bytes copied in → exit 1) |
| M29-2 | the claim-freeze ledger disagreed with the gate it discloses for two rounds and nobody ran the gate with `--disclosures` at filing | `.ufo/waves/round-24/tools/freeze-gate.py --root <LANE> --rev 7431096b --disclosures corpus/claim-freezes.tsv` → `mismatched: [round-26, round-28]`, exit 1 (`.ufo/waves/round-29/after/ledger-before-fix.txt`). round-26 row says `INSTRUMENT_ABSENT`, the gate says `INSTRUMENT_ABSENT,INSTRUMENT_REVISED`; round-28 row lists its codes unsorted | the gate's own `--disclosures` check (QUALITY row 33) — it exists but was not run at the round-26 and round-28 filings | Rows corrected with a pointer note; the round-29 report runs both gates with `--disclosures` before filing. Shown able to fail: the receipt above (exit 1 before the fix) |
| M29-3 | the L1's own freeze file names a script it does not pin | `tools/round-29/freeze-gate.py --rev dbd87cfa` flags round-29 `INSTRUMENT_UNPINNED tools/round-28/c1-heldout-naming.py` (`.ufo/waves/round-29/after/freeze-gates-at-dbd87cfa.txt`): the C1 `primary_rule` text says "unchanged from tools/round-28/c1-heldout-naming.py", a reference, not a file the counter runs | the freeze gate, but only after the freeze commit | Disclosed in the ledger row for round 29. A future freeze runs the gate on a scratch-clone commit of the candidate claims file before the real freeze. Shown able to fail: the gate's flag on this round's own freeze |
