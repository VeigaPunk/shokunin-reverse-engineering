# Round-30 SCORECARD correction draft — ScribeScorecard3166

Prepared 2026-10-23T02:45:16Z. This is a proposed appended bullet only; SCORECARD.md was not edited.

## Proposed appended correction bullet

- **Correction — round-28 S085 teaches cell (round 30):** At `SCORECARD.md:3166`, the old line says “S085's ‘the signature it keeps for each’ covers 31 of 36 keys; 5 `system:magic` keys have none.” Observation: 31 of 36 keys carry a signature, and 6 of those 31 signatures do not hash to their own key; the five remaining keys are `system:magic` keys with no `signature`. Inference from `31 - 6`: only 25 keys keep their own signature. Evidence: `corpus/lessons/round-29.md:27-42`; `.ufo/waves/round-29/after/canonical-keyhash.txt:2-10`; `.ufo/waves/round-29/w1/ExecCanonicalHash.md:20-48`; `.ufo/waves/round-29/w1/ReopenS087.md:56-63,77-87`; `corpus/lessons/round-29-verifier-spotcheck.md:95-99,127-129`; `corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md:89-95`.

The wording above is also saved at `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ScribeScorecard3166/SCORECARD-correction-draft.md` (sha256 `be95fd7b1dd0f14ee25f6f425c41a7570664cdc1d0a755155bed188512394aef`).

## Evidence and provenance

- **Observation — stale wording.** This seat's `grep` tool query for `covers 31 of 36` on `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md` returned line 3166; the read of `SCORECARD.md:3160-3171` returned the quoted text above. The read/grep tools returned successfully (not shell processes; no process exit code). The inspected SCORECARD proceeds through its Round-29 section ending at line 3203; no Round-30 section was present in this inspected snapshot.
- **Observation — hash audit.** Prior round-29 artifact `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-29/w1/ExecCanonicalHash.md:20-48` records the producing command `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecCanonicalHash/venv/bin/python /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecCanonicalHash/audit.py | tee /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecCanonicalHash/audit-output.json` (run with `set -o pipefail`). Its exact output includes `"canonical_entry_count": 36`, `"magic_keys": 5`, `"signature_bearing_keys": 31`, `"signature_mismatch_count": 6`, and six key/signature/computed-selector records (lines 38-44). Recorded UTC: `2026-10-22T20:21:47Z`; `COMMAND_EXIT=0`.
- **Observation — retained round-29 receipt.** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-29/after/canonical-keyhash.txt:1-11` records command `$ python3 -I -B -c "<exec tools/round-25/a2/resolve-selectors.py; hash every kept signature of corpus/evidence/round-29/c2/canonical-signatures.json and every candidate in corpus/evidence/round-29/c2/db/openchain-*.json>"`, UTC `2026-10-22T20:26:48Z`, revision `18be864a528873b2b70d8c94e31f880290249e90`, output `keys=36 with_signature=31 magic=5 mis_keyed=6` and six `MISKEYED` rows (lines 4-9), `exit=0`. This is a pre-existing receipt, not a run by this seat.
- **Observation — no-signature entries.** The local read of `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-29/c2/canonical-signatures.json:118-131` returned five consecutive keys whose only field is `"source": "system:magic"`; none has a `signature` field. The independent reopen record `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-29/w1/ReopenS087.md:56-63` records that S087's canonical list is byte-identical to S085 and confirms exactly these five no-signature entries.
- **Observation — correction route.** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-29-verifier-spotcheck.md:127-129` explicitly routes defect 6 to an appended named correction and identifies the old SCORECARD pointer. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-29.md:27-42` records the S085/S087 source identity and the 6-of-31 correction; `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md:89-95` contains the existing pointer explaining that 11 of 36 keys do not have their own kept signature (5 none, 6 another selector's).
- **Inference.** 31 signature-bearing keys minus the six that do not hash to their keys leaves 25 that do. This subtraction is not a separate counter output.

## Scope, gates, and touched surfaces

- **Behavior:** drafted the requested correction, preserving the historical line and making the count distinction explicit.
- **Touched surfaces:** created the required scratch draft and this seat report only. SCORECARD.md and all other lane/product files were read-only. No external sources were opened.
- **Gates:** no build, test, lint, counter, REA, git/jj write, or verification run. No tools were installed or updated. Scratch setup/hash commands returned successfully; the hash command output is recorded above, and the directory setup command output was the timestamp `2026-10-23T02:43:28Z`.
- **Out of scope / limit:** the SCORECARD snapshot inspected ends at the Round-29 section, so this report supplies text for the Round-30 section when integrated; it does not insert it. The hash audit and canonical-keyhash receipt are prior round-29 evidence and were not rerun.
- **Findings:** stale quoted wording at `SCORECARD.md:3166` is corrected by the proposed bullet; the independent evidence supports 31 signature-bearing entries, six mis-keyed entries, five `system:magic` entries without signatures, and therefore 25 entries retaining their own signature.

Report: .ufo/waves/round-30/w1/ScribeScorecard3166.md
