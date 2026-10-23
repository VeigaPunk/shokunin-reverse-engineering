# ReviewCarrierProvenance — round-31 wave-1 carrier provenance review

- Seat: `KaidokuR31.ReviewCarrierProvenance` (reviewer, leaf)
- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only)
- Frozen: lane commit `35ba7c522dba55f9be27eb161d4254eacaa24330` (2026-10-23T04:05Z), claims.json line 20
- Scope: re-derive every C1 carrier from its published container before data; verify the 3.7.2 proj.db claim
- Access date for all opened sources: 2026-10-23
- No installs performed (no tooling needed beyond Python 3 stdlib, `curl`, `sha256sum`)

## Summary verdict

**PASS.** All 12 carriers re-derived from their published containers: container digest, extracted member, and on-disk file agree for every row (12/12 container ok, 12/12 member ok, 12/12 on-disk ok). The claim "pyproj 3.7.2's proj.db is byte-identical to 3.7.1's" **HOLDS** (both sha256 `a25d85a2...b77109`, which is also the on-disk `proj-371.db` hash).

## Method and producing commands

1. Read frozen carrier list `corpus/evidence/round-31/c1/carriers.tsv` (12 rows, ids `proj-341/350/361/370/371`, `chinook`, `chinook-autoinc`, `gpkg-curve/curvepolygon/line-zm/multisurface/test-gpkg-nulls`).
2. Extracted per-container digest from committed PyPI JSON (`pypi-pyproj-3.4.1.json` … `pypi-pyproj-3.7.1.json`, `pypi-pyogrio-0.11.1.json`) via jq on the committed files; all 6 digests equal the tsv `container_sha256` values (pyproj wheels: `5a53acbd…`, `cd5e2b6a…`, `80fafd1f…`, `ee60895f…`, `1e47c4e9…`; pyogrio sdist: `e1441dc9…`).
3. Downloaded containers into scratch `dl/` (all via `timeout 900 curl -fsSL -o <dst> <url>`; all exit 0):
   - pyproj wheels 3.4.1/3.5.0/3.6.1/3.7.0/3.7.1 cp310 manylinux2014 x86_64 (PyPI files host)
   - `Chinook_Sqlite.sqlite`, `Chinook_Sqlite_AutoIncrementPKs.sqlite` (GitHub release v1.4.5)
   - `pyogrio-0.11.1.tar.gz` (PyPI files host)
   - `pyproj-3.7.2-cp311-cp311-manylinux_2_28_x86_64.whl` (PyPI files host; for the claim)
4. `sha256sum dl/*` at 2026-10-23T~04:10Z: every downloaded container hash equals the tsv `container_sha256` and the committed JSON digest (Chinook: no committed JSON; tsv `container_sha256` is the release-asset digest, matched).
5. Extracted each named member (zip `pyproj/proj_dir/share/proj/proj.db`; tar `pyogrio-0.11.1/pyogrio/tests/fixtures/<name>.gpkg`; Chinook asset is its own member) → `members/<id>.bin`.
6. `python3 -I -B verify_provenance.py` at 2026-10-23T04:11:35Z, exit 0 (full stdout below).
7. `sha256sum /fast/scratch/hyaku/kaidoku-r31/carriers/*` at 2026-10-23T~04:10Z: all 12 on-disk hashes equal the tsv `sha256` column.

## Carrier table (12 rows)

| id | container ok | member ok | on-disk ok | container sha256 | member sha256 (= carrier `sha256`) |
|---|---|---|---|---|---|
| proj-341 | yes | yes | yes | `5a53acbde511…dcb7a` | `97a04533b1e7…4c2414` |
| proj-350 | yes | yes | yes | `cd5e2b6aa255…4ebb83` | `deaa7e9db95e…284c2` |
| proj-361 | yes | yes | yes | `80fafd1f3eb4…f97d35` | `79b660eb3c09…e029c5` |
| proj-370 | yes | yes | yes | `ee60895f60cbd…cf085` | `976d427f03779…3cb7e` |
| proj-371 | yes | yes | yes | `1e47c4e93b88…0f30ee` | `a25d85a2ebfc…b77109` |
| chinook | yes | yes | yes | `bdf635be69850…4a61a` | `bdf635be69850…4a61a` |
| chinook-autoinc | yes | yes | yes | `ca157cb58cb34…8d4` | `ca157cb58cb34…8d4` |
| gpkg-curve | yes | yes | yes | `e1441dc9c866f…8082c` | `03a9c5904fd30…04f302` |
| gpkg-curvepolygon | yes | yes | yes | `e1441dc9c866f…8082c` | `00a1309ab0f29…96bac7` |
| gpkg-line-zm | yes | yes | yes | `e1441dc9c866f…8082c` | `9563e513b0644…2747c70c` |
| gpkg-multisurface | yes | yes | yes | `e1441dc9c866f…8082c` | `898a238bc119f…c6d648d` |
| gpkg-test-gpkg-nulls | yes | yes | yes | `e1441dc9c866f…8082c` | `4281d3c55f20…af71e1d8` |

Script stdout (exact):

```
# carrier provenance verification run @ 2026-10-23T04:11:35Z
id                 container    member   ondisk
proj-341           True         True     True
proj-350           True         True     True
proj-361           True         True     True
proj-370           True         True     True
proj-371           True         True     True
chinook            True         True     True
chinook-autoinc    True         True     True
gpkg-curve         True         True     True
gpkg-curvepolygon  True         True     True
gpkg-line-zm       True         True     True
gpkg-multisurface  True         True     True
gpkg-test-gpkg-nulls True         True     True
claim pyproj-3.7.2-proj.db == 3.7.1-proj.db: True
  3.7.1 proj.db sha256: a25d85a2ebfc4584eba65186b7c41743b084ce5d391941cbb41c805947b77109
  3.7.2 proj.db sha256: a25d85a2ebfc4584eba65186b7c41743b084ce5d391941cbb41c805947b77109
ALL 12 ROWS OK: True
```

## pyproj 3.7.2 claim check

- pyproj 3.7.2 requires Python ≥3.11 and ships **no cp310 wheel** (`requires_python: ">=3.11"` in `https://pypi.org/pypi/pyproj/3.7.2/json`, fetched 2026-10-23). The carrier list's 3.7.1 wheel is cp310/manylinux2014; the closest published 3.7.2 Linux x86_64 build is `pyproj-3.7.2-cp311-cp311-manylinux_2_28_x86_64.whl`.
- Fetched 3.7.2 wheel from `https://files.pythonhosted.org/packages/ad/ab/9bdb4a6216b712a1f9aab1c0fcbee5d3726f34a366f29c3e8c08a78d6b70/pyproj-3.7.2-cp311-cp311-manylinux_2_28_x86_64.whl`; sha256 `281cb92847814e8018010c48b4069ff858a30236638631c1a91dd7bfa68f8a8a` (9,493,977 bytes) verified against the PyPI JSON digest.
- Extracted `pyproj/proj_dir/share/proj/proj.db`: sha256 `a25d85a2ebfc4584eba65186b7c41743b084ce5d391941cbb41c805947b77109` — **identical** to the 3.7.1 proj.db member and to the on-disk `proj-371.db`. Claim HOLDS (observation).
- Note (observation): the 3.7.2 wheel uses the `manylinux_2_28` platform tag and cp311 ABI; byte-identity of the bundled proj.db holds across that build difference, which is the only published 3.7.2 Linux x86_64 analog.

## Sources opened

| URL | date | sha256 of bytes read | quote (≤25 words) |
|---|---|---|---|
| https://pypi.org/pypi/pyproj/3.7.2/json | 2026-10-23 | (JSON served; not hashed as file) | `"requires_python": ">=3.11"` |
| https://files.pythonhosted.org/packages/…/pyproj-3.4.1-….whl | 2026-10-23 | `5a53acbde511a7a9e1873c7f93c68f35b8c3653467b77195fe18e847555dcb7a` | binary payload, N/A |
| https://files.pythonhosted.org/packages/…/pyproj-3.5.0-….whl | 2026-10-23 | `cd5e2b6aa255023c4acd0b977590f1f7cc801ba21b4d806fcf6dfac3474ebb83` | binary payload, N/A |
| https://files.pythonhosted.org/packages/…/pyproj-3.6.1-….whl | 2026-10-23 | `80fafd1f3eb421694857f254a9bdbacd1eb22fc6c24ca74b136679f376f97d35` | binary payload, N/A |
| https://files.pythonhosted.org/packages/…/pyproj-3.7.0-….whl | 2026-10-23 | `ee60895f60cbd1a9c903ab2bc22adea63004296a1c28b8775a11cf50905cf085` | binary payload, N/A |
| https://files.pythonhosted.org/packages/…/pyproj-3.7.1-….whl | 2026-10-23 | `1e47c4e93b88d99dd118875ee3ca0171932444cdc0b52d493371b5d98d0f30ee` | binary payload, N/A |
| https://files.pythonhosted.org/packages/…/pyproj-3.7.2-….whl | 2026-10-23 | `281cb92847814e8018010c48b4069ff858a30236638631c1a91dd7bfa68f8a8a` | binary payload, N/A |
| https://github.com/lerocha/chinook-database/releases/download/v1.4.5/Chinook_Sqlite.sqlite | 2026-10-23 | `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a` | binary payload, N/A |
| https://github.com/lerocha/chinook-database/releases/download/v1.4.5/Chinook_Sqlite_AutoIncrementPKs.sqlite | 2026-10-23 | `ca157cb58cb34ed2e5d4eb3418ae7a9418f0cfe8b751985b6a4482346c9548d4` | binary payload, N/A |
| https://files.pythonhosted.org/packages/…/pyogrio-0.11.1.tar.gz | 2026-10-23 | `e1441dc9c866f10d8e6ae7ea9249a10c1f57ea921b1f19a5b0977ab91ef8082c` | binary payload, N/A |
| committed `corpus/evidence/round-31/c1/pypi-pyproj-3.4.1.json` … `-3.7.1.json`, `pypi-pyogrio-0.11.1.json` | 2026-10-23 | lane read-only; n/a | `"filename": "pyproj-3.4.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"` |

## Scratch artifacts (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/ReviewCarrierProvenance/`)

| artifact | sha256 |
|---|---|
| `verify_provenance.py` (verification script) | `e04630ceb18cc43b66e33351d698edb276ce632c6ce7f8d037c1181e13339e2c` |
| `result.json` (machine-readable verdict) | `6fab12837511aeed7e49f205f4177b4cb89ac2fec201d61346eaee9eaab34a10` |
| `dl/pyproj-3.4.1-….whl` | `5a53acbde511a7a9e1873c7f93c68f35b8c3653467b77195fe18e847555dcb7a` |
| `dl/pyproj-3.5.0-….whl` | `cd5e2b6aa255023c4acd0b977590f1f7cc801ba21b4d806fcf6dfac3474ebb83` |
| `dl/pyproj-3.6.1-….whl` | `80fafd1f3eb421694857f254a9bdbacd1eb22fc6c24ca74b136679f376f97d35` |
| `dl/pyproj-3.7.0-….whl` | `ee60895f60cbd1a9c903ab2bc22adea63004296a1c28b8775a11cf50905cf085` |
| `dl/pyproj-3.7.1-….whl` | `1e47c4e93b88d99dd118875ee3ca0171932444cdc0b52d493371b5d98d0f30ee` |
| `dl/pyproj-3.7.2-cp311-cp311-manylinux_2_28_x86_64.whl` | `281cb92847814e8018010c48b4069ff858a30236638631c1a91dd7bfa68f8a8a` |
| `dl/Chinook_Sqlite.sqlite` | `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a` |
| `dl/Chinook_Sqlite_AutoIncrementPKs.sqlite` | `ca157cb58cb34ed2e5d4eb3418ae7a9418f0cfe8b751985b6a4482346c9548d4` |
| `dl/pyogrio-0.11.1.tar.gz` | `e1441dc9c866f10d8e6ae7ea9249a10c1f57ea921b1f19a5b0977ab91ef8082c` |
| `members/proj-341.bin` | `97a04533b1e7e3bfea9be2e11cc4e43a60539020d8cdd02622203d82db4c2414` |
| `members/proj-350.bin` | `deaa7e9db95ef993358557441d33d26c24e01edb82c82021e8f639cadbb284c2` |
| `members/proj-361.bin` | `79b660eb3c09f50c0f251e958db7cbf9a2d5d18d2836e99082095b31c7e029c5` |
| `members/proj-370.bin` | `976d427f037791c88b8d051a452e1fb13157c1c14b6e56d5a868097a4813cb7e` |
| `members/proj-371.bin` | `a25d85a2ebfc4584eba65186b7c41743b084ce5d391941cbb41c805947b77109` |
| `members/proj-372.bin` | `a25d85a2ebfc4584eba65186b7c41743b084ce5d391941cbb41c805947b77109` |
| `members/gpkg-curve.bin` | `03a9c5904fd3075c61ba96e5bf0aac381721d43799db23c06634a0c56e04f302` |
| `members/gpkg-curvepolygon.bin` | `00a1309ab0f29f97a4c5f6cb9cd3bde27143fc936712d5101767f60f0c96bac7` |
| `members/gpkg-line-zm.bin` | `9563e513b064476ee7ab8c66858f3f434307ca554f7495652d09674d2747c70c` |
| `members/gpkg-multisurface.bin` | `898a238bc119f051622c22de973899f501466a33a6a6c0cc405122802c6d648d` |
| `members/gpkg-test-gpkg-nulls.bin` | `4281d3c55f2042e2174ab9a13c5c5a06d13841071c1aa3ea2cc131afaf71e1d8` |

(Chinook rows have no separate member file: the release asset is both container and member; `members/` holds only extracted members.)

## Findings by severity

No actionable defects found.

1. **[observation] All 12 carriers re-derived with matching digests.** Container, member, and on-disk hashes agree for every row; `container_sha256` in the tsv matches the committed PyPI JSON digests for all 6 packaged containers, and the two Chinook release assets match their self-referential `container_sha256` (which equals the carrier `sha256`, since the asset is the database).
2. **[observation] The 3.7.2 claim holds.** `pyproj-3.7.2` proj.db bytes == `3.7.1` proj.db bytes (sha256 `a25d85a2…`), which also equals the on-disk `proj-371.db`. The 3.7.2 build used is cp311/manylinux_2_28 (no cp310 wheel exists for 3.7.2), noted for reproducibility.
3. **[inference] No carrier requires a different container than named.** The tsv `container`/`member` names resolved exactly (5 wheel members, 5 sdist members, 2 asset-as-carrier), so the frozen carrier list is self-consistent with the published PyPI/GitHub inventory.

## Residual risk / verification gaps

- The 3.7.2 byte-identity check covers the Linux x86_64 cp311 wheel; other 3.7.2 wheels (macOS, Windows, aarch64, musllinux) were not compared — the claim concerns the proj.db data, which is a single bundled artifact per release, so cross-platform variation is not expected.
- Board-gated btrfs overlayfs / plymouth boot-chain packages were not touched, and `pacman` was not used at all (no installs performed; Python stdlib, curl, sha256sum already present).
- No REA execution was required for this item (provenance review only); no counter was run.

## Handoff

- Verification verdict: **PASS** — `carriers=12 container_ok=12 member_ok=12 ondisk_ok=12`; `pyproj-3.7.2-proj.db == 3.7.1-proj.db` holds.
