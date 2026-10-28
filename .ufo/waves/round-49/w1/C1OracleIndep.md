# C1OracleIndep — independent oracle re-derivation (R49-C1, pre-freeze)

**Verdict: CLEAN. Zero disagreements** across carriers.json `oracle` (census, members, output_tree_digest), a fresh `/usr/bin/unsquashfs` 4.7.5 extraction, a fresh `/usr/bin/7z` 26.04 extraction, and the unblob `__output__` trees (round-44/oracle). 7z reads all four carriers (exit 0, "Everything is Ok") and agrees with unsquashfs byte-for-byte. Run 2026-10-28T21:05Z; driver `C1OracleIndep/ind.py`, full data `C1OracleIndep/ind.json` (sha256 6a8c5f47…4155).

## Method
For each of v1le/v1be/v2le/v2be (paths from carriers.json, image sha256+size rechecked): `unsquashfs -d $S/un/<id> IMG`, `unsquashfs -lls IMG`, `7z x -y -o$S/7z/<id> IMG` (autodetect) and `7z x -y -tSquashFS …`. Walked every extracted tree (regular/dir/symlink), sha256+size per member, recomputed tree digest (`sha256` of `<path>\t<sha>\n` sorted bytewise), and compared with: `oracle.members`, `oracle.census` (parsed live `-lls` rows: mode, owner, mtime, path), `oracle.output_tree_digest`, `oracle.output_tree.output_tree_digest`, `oracle.listing/extraction.stdout_sha256`, and the committed unblob trees at `output_tree`.

## Findings table
| id | image sha256 ok | unsq -d rc | unsq -lls rc | 7z x rc / -tSquashFS rc | members == carriers.json | census rows == live -lls | digest (all 4 sources equal) | unblob tree == unsq | 7z == unsq | stored stdout sha == fresh |
|---|---|---|---|---|---|---|---|---|---|---|
| v1le | yes (b45925fa…) | 0 | 0 | 0 / 0 | yes (3 reg) | 4/4 | 8faae773…2a48 | yes | yes | yes (lls 14fda199…, extract 7d9a733a…) |
| v1be | yes (529e1077…) | 0 | 0 | 0 / 0 | yes (3) | 4/4 | 8faae773…2a48 | yes | yes | yes (same hashes as v1le) |
| v2le | yes (7c62dbe3…) | 0 | 0 | 0 / 0 | yes (4) | 5/5 | 4178bb83…f947 | yes | yes | yes (lls 55a68d07…, extract 8b767ff6…) |
| v2be | yes (79c0f388…) | 0 | 0 | 0 / 0 | yes (4) | 5/5 | 4178bb83…f947 | yes | yes | yes (same hashes as v2le) |

Member sha256 (all carriers): apple.txt 303980bc…97d0 (6B), banana.txt 5a81483d…16b1 (7B), cherry.txt 86baf352…cf55 (7B) for v1; apple1..4.txt 6181259c…1c30, 919fc82d…4aff, 2d95014e…1ec6, 08d9b05b…8a959d (7B each) for v2. Full list `C1OracleIndep/unsquashfs-members.sha256` (sha 14e9bcb6…).
Census nonregular: exactly one row per carrier, the root dir (`rel ""`, path `squashfs-root`); every extracted tree (unsquashfs, 7z, unblob) holds regular files only, no dirs/symlinks. This matches the counter comment "zero non-regular members" only if the root dir row is excluded from "non-regular" — worth confirming `nonregular` is `[]` in carriers.json (it is, `members`/`nonregular` per-carrier were `[]` for v1le; root dir lives only in `census`).
7z header agrees with carriers.json `sevenzip.header` (v1: SquashFS 1.0, cluster 32768, Headers 4025; v2: SquashFS 2.0, cluster 65536, Headers 4008, Characteristics DUPLICATES_REMOVED; Big-endian `-`/`+` per carrier), 7z summary "Files: 3/4, Size 20/28, Compressed 4096".
Manifest cross-check: round-44 `manifest.json` `files[]` `lfs_oid` == sha256 == `bytes`/`lfs_size` for every unblob member (provenance of the S138 tree contents is genuine LFS content, not pointers).

## Observations (not disagreements; for the L1's judgement)
1. **LE and BE carriers of one version produce byte-identical output** (same member digests, same tree digest, same `unsquashfs -lls` stdout hash). A counter/rerun that compares only published members cannot tell whether the REA run actually parsed the LE or the BE image; endian discrimination must come from the carrier-fresh/layout bindings (image sha) not the oracle. The oracle digest is also identical for v1le/v1be and v2le/v2be, so a cross-carrier output substitution passes the oracle comparison alone.
2. **Member contents are tiny and guessable** (`apple\n` etc., 6–7 bytes): a forgery that writes the plain-text names/contents satisfies the oracle comparison; counter robustness rests on the counter-time REA rerun, not the oracle.
3. `unsquashfs -d` stdout hash is independent of destination path (stored hash from a different scratch dir equals the fresh one) — the stored `extraction.stdout_sha256` is reproducible.
4. The oracle root also contains `squashfs_v2.0_*` and `squashfs_v2.1_*` extract dirs (v2.1 is exploratory/unscored); a loose `resolve_output_tree` fallback by handler/endian would be ambiguous for v2 if it globbed — the explicit carriers.json `output_tree` path used here is unambiguous. Not run: the counter's resolver itself.
5. The 7z (26.04, wrapper `/usr/bin/7z -> /usr/lib/7zip/7z`) does NOT refuse any carrier; no refusal reason to report. Not run: 7z on v2ns/v2.1/v3 carriers (out of scope).

## Not run
Counter (`c1-counter.py`), `c1-oracle.py` itself, REA extraction, any mutation of carriers.

## Tools
No installs. `/usr/bin/unsquashfs` 4.7.5 (sha256 461e1fd9…677c, matches carriers.json `tool_sha256`? — not recomputed by this seat), `/usr/bin/7z` 7-Zip 26.04.
Scratch removed after receipt copy.
