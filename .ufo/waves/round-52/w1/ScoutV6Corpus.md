# ScoutV6Corpus — round 52, wave r52-w1

Verdict: manifest built and verified; the C2 one-pair move is confirmed from the envelope bytes; two claim-level defects found (census snapshot vs. landing; reader-census premise is magic-spelling-dependent). Scout only; no lane file touched.

## 1. Manifest (frozen triage corpus)

- `manifest.txt`: `sha256sum` output for all 126 `envelope.json` files under `.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/`, sorted by path. `sha256sum -c` re-run: exit 0, 126 `OK` (receipt `receipts/scout-probes.json`, key `manifest_check`).
- The 126 directories match the v5 receipt's 126 envelopes (`c3-after.json`, `n_envelopes 126`).

## 2. ddwrt family — every envelope (evidence: `ddwrt-envelopes.tsv` / `.json`)

17 envelopes are ddwrt-named or ddwrt-handled. 15 carry handler `squashfs_v3_ddwrt`; 2 are named ddwrt but carry handler `squashfs_v3` (`squashfs_v3_ddwrt_squashfs_v3_le_{d1,ddefault}`).

| set | envelopes | v5 label |
|---|---|---|
| FAILED body (`extractor-failure`, P=0, handler ddwrt) | `dmg_Z3_v3ddwrt_inode_table` (exits 0 and 1, 3 ExtractCommandFailedReport) | legacy-body-failure / cross-read-legacy |
| clean, handler ddwrt | 6 × `_ddefault` (be/le × 1kpad/4kpad/nopad) + `dep_A2_squashfs_v3.be.nopad` | clean / none |
| dep-missing, handler ddwrt | `dep_A1_squashfs_v3.be.nopad` | dep-missing-le |
| depth-limited, handler ddwrt | 6 × `_d1` | depth-limited / raise-depth |

Arithmetic check against the claim:
- FAILED ddwrt-handler bodies: exactly 1 (`dmg_Z3`). The v6 change moves exactly that pair.
- Clean ddwrt-handler envelopes: **7, not 2**. The claim's "two clean no-pad `_ddefault`" (`be.nopad_ddefault`, `le.nopad_ddefault`) is a correct narrower statement. The full clean set adds four more (`be/le` 1kpad/4kpad `_ddefault`) and `dep_A2_squashfs_v3.be.nopad`. None of the seven moves under v6 (the claim keeps them clean).
- Block 26's disclosed "moving ddwrt into no-reader would move 8 labels" equals 1 FAILED + 7 clean. Consistent.
- The one-pair C2 arithmetic is therefore right. Anyone who reads the family as "1 + 2" will be wrong by five envelopes.

The FAILED body was reconstructed in scratch from the committed `v3ddwrt-be--squashfs_v3.be.nopad.bin` (zero bytes 144..203, REBUILD.md:90). Its sha256 equals the subject digest `839c17a8…50c8` (receipt key `failed_body_reconstruct`, match true). The reconstructed bytes are not copied into the lane.

## 3. Finding — the no-reader census is magic-spelling-dependent (material to C2's premise)

Raw committed fixtures (`unsquashfs -lls` exit): v2ns be/le 1, v3ns be/le 1, v3bc-le 1, ddwrt-be-nopad 1. All four families are "no reader" on raw bytes.

Same bytes with the DD-WRT/vendor magic normalised to the standard word (the lane's own oracle procedure, `tools/round-42/sqfs3-oracle.py` `normalize_magic`; the r42 entry says the same for DD-WRT):
- `unsquashfs -lls` exit 0 and `7z l -tSquashFS` exit 0 on **13 of 14** committed fixtures. The exception is the two LZMA `v3adapt` fixtures, which fail on both raw and normalised bytes.
- This includes ddwrt-be-nopad (4 files, 7-Zip lists `apple1.txt` 7→25 B), v2ns, v3ns and v3bc-le.

The FAILED body `dmg_Z3` is refused by all three readers on both raw and normalised bytes (`unsquashfs` exit 1, `7z` exit 2, `sasquatch` exit 1). So the body-level verdict for C2 is right, but the family-level reader census that block 26 and the v6 audit rest on is not a property of the family. It is a property of the magic spelling for healthy bodies. Recommendation for L1: disclose this in the freeze, or make the reader check body-level (normalised magic, then unsquashfs and 7-Zip). Do not write "no validated second reader" as a family fact without that qualifier. This is a finding, not a claim change: the audit as frozen still passes (1 → 0).

Receipts: `receipts/scout-probes.json`, keys `healthy_raw`, `healthy_norm`, `failed_raw`, `failed_norm`, `fixture_census_normalised`, `fixture_census_raw_unsquashfs_exit`.

## 4. Finding — census3 no-regression binding will break at the landing as written

`tools/round-51/census3.py --check` compares the SKILL.md registry block with the frozen snapshot `tools/round-51/census3.json` (56 paths). It is exact-equality.
- At the claims-draft base `ab0eafed`: exit 0, `census_outside []` (receipt key `census3_at_base`). The claim's "before" holds.
- Probe (scratch clone only, `--shared` clone detached at `ab0eafed`): two round-52 instrument rows added to the registry block, then the same check. **Exit 1, `census_outside` = `[tools/round-52/gap-rule.json, tools/round-52/sqfs-triage-v6.py]`** (receipt key `census3_after_simulated_round52_rows`).
- The claim requires `census_outside 0` at the landing REV. The snapshot must be regenerated at the freeze, but it sits under `tools/round-51/` and the claim does not say that regeneration is permitted. L1 must decide: regenerate `census3.json` in the freeze with the change named, or bind C2's census clause to a round-52 snapshot. As written, the after-arm of that binding cannot hold.

## 5. Other observations

- `census3.py` did land in round 51 (commit `96aee1a5`, registry row, `census3.json`). The prompt's "r51 instruments never landed" is true for the C1 counter/harness/fetch drafts, not for census3.
- The "6/7 ddwrt no-reader" census (v5 docstring) cannot be re-measured from lane bytes: only `v3ddwrt-be--squashfs_v3.be.nopad.bin` is committed under `corpus/evidence/round-42/c2/fixtures/`. The other six ddwrt carriers are not in the lane, and fetching them was outside this seat's named URLs.
- The `legacy-body-failure` cross-read on the damaged V1/V2/V3/V6 bodies (reader-backed families) is not tested here; those damaged-body bytes are not reproducible from the lane (the scratch round-42 dir is gone).

## 6. Tooling and environment

- No tools installed or upgraded. Readers used: `unsquashfs` 4.7.5, `7z` 26.04, `sasquatch` (`~/.local/bin`, already present). No pacman, no network, no REA, no `--data-run`.
- Disk guard checked before the heavy pass (`/fast/scratch/hyaku` 46 %, free 435.4G).

## Receipts and artifacts (under `.ufo/waves/round-52/w1/ScoutV6Corpus/`)

- `manifest.txt`: sha256 manifest, 126 lines.
- `ddwrt-envelopes.tsv`, `ddwrt-envelopes.json`: 17-row ddwrt enumeration with handler, pad, endian, gap kinds, failed-body flag, published count, exit codes, command-failed count, v5 and evaluator labels, subject and envelope sha256.
- `receipts/scout-probes.json`: commands, exit codes, stdout/stderr sha256, UTC for every probe in this report.
- `status.json`.

Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-ScoutV6Corpus` removed after receipts were copied.
