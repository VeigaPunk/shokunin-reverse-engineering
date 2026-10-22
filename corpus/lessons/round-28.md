# Round 28 — held-out test of the round-25 EVM naming rule; openchain's `filtered` flag from code

Author: kaidoku L1, round 28, attempt 2 (in-session hyaku lane subagent). Lane-round base
`935c36608008f79e3dea4f1ed191df3c89e3b848`. Attempt 1 froze both claims and collected their data
(`87d3dfb6`, `86fa8526`, `ca4069a4`, `cb8d495e`), then died in an omp process restart at 17:26Z.
Attempt 2 re-verified that work and committed attempt 1's leftover paths (`a2673116`).

## Claims

- R28-C1, coverage (learning claim, frozen at `87d3dfb6`, `.ufo/waves/round-28/claims.json`):
  the round-25 primary naming rule scored, unchanged, on 61 held-out carriers and 187 held-out
  selectors. Target `runs_ok 61/61`, `rows_complete 187/187`, `tally_equal 1`, `entry_ok 1`,
  exit 0. **Missed:** `runs_ok=60/61 rows_complete=186/187`. REA 6.5.0 refused carrier h09
  (unlinked-library placeholder, M28-1). Honest stop. Observed held-out triple:
  named 137, right 137, wrong 0.
- R28-C2, depth (learning claim, frozen at `86fa8526`, `.ufo/waves/round-28/claims-c2.json`):
  openchain's `filtered` flag follows Sourcify's `filterResponse` code. Target
  `responses_complete 230/230`, `mismatches 0`, `predicted_true >= 1`, `entry_ok 1`, exit 0.
- Not claimed: calibration (steered off in round 27). The eight routed defects of
  `corpus/lessons/round-27-verifier-spotcheck.md` are handled as hygiene (SCORECARD round-28
  section).

## Gate

Sources opened on 2026-10-22 by the L1 with plain `curl` (files kept under
`/fast/scratch/hyaku/kaidoku-r28/l1/src/`). Each quote is contiguous served bytes, at most 25
words (QUALITY row 42). S084, S085 and S086 are new rows. No existing row changed status,
recheck or used-by.

| row | source and access date | sha256 of the bytes read | located quote (at most 25 words) | section |
|---|---|---|---|---|
| S084 | https://raw.githubusercontent.com/argotorg/sourcify/189cd726f7ed8fb3d2f503402d5c133e0f50e1fd/services/4byte/src/api/handlers.ts; opened 2026-10-22T17:49Z | `30981efbc7bc1b541954eb75767c8154562f4f77a9bfc1ad22cf19c8996c5a38` | `signatureItem.filtered =` / `signatureItem.name !== expectedCanonical.signature;` (two consecutive lines) | `:47-48`, in `filterResponse` `:39-66` |
| S085 | https://raw.githubusercontent.com/argotorg/sourcify/189cd726f7ed8fb3d2f503402d5c133e0f50e1fd/services/4byte/src/utils/canonical-signatures.json; opened 2026-10-22T17:49Z | `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2` (equal to the lane copy `corpus/evidence/round-28/c2/canonical-signatures.json`) | `"0xd55ec697": {` | `:2`; 36 keys |
| S086 | https://raw.githubusercontent.com/ethereum/solidity/v0.8.30/docs/using-the-compiler.rst; opened 2026-10-22T18:20Z | `76e5db1df6cb67b189c0e8e0b27ed9546a03e5655ffdb400653d62196baac4ae` | `you will notice that the bytecode contains substrings of the form ``__$53aea86b7d70b31448b230b20ae141a537$__``` | `:74`, Library Linking |

Considered and not made rows: the planned S087 (4byte.directory server source, for result order) was never opened, so it is not a row; it stays an unopened lead.

Gate notes after the wave (seat `CriticSourceRows`, `.ufo/waves/round-28/a2w/CriticSourceRows.md`; rows are not edited in place, so the notes live here):
- S084: the "every other candidate keeps `filtered: false`" half rests on `handlers.ts:90` (`filtered: false,` in `mapLookupResult`) and `:262` (the same literal in the second lookup path), not only on `:47-48`. Re-checked by the L1 with `sed -n 86,92p` and `sed -n 258,264p` on the opened bytes.
- S085: the kept signature for the quoted key is on the next line, `:3` `"signature": "upgrade()",`.
- S086: the 34-character rule is at `:75` (`The placeholder is a 34 character prefix of the hex encoding of the keccak256 hash of the fully qualified library name.`, 21 words). Tag `v0.8.30` resolves to commit `73712a01b2de56d9ad91e3b6936f85c90cb7de36` (seat `SourceSolidityLinking`, `git ls-remote`). The h09 carrier was built with solc 0.8.37, and the seat reports that the Library Linking text is identical at v0.8.37. The REA refusal in the row's teaches cell comes from the run's envelope (`corpus/evidence/round-28/c1/envelopes/h09.json`), not from these docs.

## Mistakes

| id | class | evidence pointer | captured-by | fix and how it was shown able to fail |
|---|---|---|---|---|
| M28-1 | a frozen carrier list held a carrier the tool refuses on input format, so the frozen target was unreachable before any run | `corpus/evidence/round-28/c1/runs.tsv` row h09 (exit 1); `corpus/evidence/round-28/c1/envelopes/h09.json` (`invalid_format`, "Hex carrier requires complete hexadecimal byte pairs"); `Cr1LibUser.noopt.runtime.hex` holds `__$a2bad93077572174e8e5044433a5a7d5f3$__` | none: QUALITY rows 38-40 order and pin the instruments but never test that the frozen inputs are admissible to the tool | New QUALITY row 43 and the screen `tools/round-28/hex-screen.py`. Shown able to fail on real bytes: `python3 -I -B tools/round-28/hex-screen.py --root <LANE> corpus/evidence/round-28/c1/carriers.tsv` prints `FAIL h09 … placeholders=1 __$a2bad93077572174e8e5044433a5a7d5f3$__` and `carriers=61 fail=1`, exit 1 (2026-10-22T18:22Z). The next frozen EVM list commits this screen's exit-0 output with its freeze |
| M28-2 | a 73-seat v2 wave was sized without checking free seat capacity; it waited about 30 minutes under the shared 85-seat cap and was withdrawn before dispatch, which cost the round its build wave | `.ufo/waves/round-28/a2-spec.json`, `a2-dispatch.json` (validated, never dispatched); `wave-slot.sh status` at 18:19Z `live_estimate=60 cap=85` | none | Read `wave-slot.sh status` before sizing a wave, and size the wave to the band that fits the free seats. The replacement 36-seat v1 wave (`a2w`) was granted at 18:22Z with `live=49` |
| M28-3 | an L1 one-character edit to `corpus/SOURCES.md` (S084 anchor `:39-65` → `:39-66`) was made with a Python one-liner instead of the edit tool | this lesson; the anchor was first written wrong (the function closes at `handlers.ts:66`) | none | The anchor was re-checked with `sed -n 65,66p` against the opened bytes. Edits go through the edit tool |
