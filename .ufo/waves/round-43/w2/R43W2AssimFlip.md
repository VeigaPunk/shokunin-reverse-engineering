# R43W2AssimFlip — fresh-byte attack on assimilation ADMIT flip

## Result

**The assimilation flip did not fire.** On fresh official GitHub API and releases-page bytes at **2026-10-27T11:34:53Z–11:34:54Z**, I found no ninth release, no change to any release/asset field other than mutable `download_count`, no body containing a standalone `1.0` token, and no change in the per-release digest-presence pattern. The six published digests for `sasquatch-v4.5.1-6` still match the admitted entry. This is a bounded recheck, not evidence that future API/page bytes cannot change.

## Axes and target

- **Coverage:** attacked every assigned flip dimension: release count/tag set, release asset set, body version-pair, and digest-presence pattern; also rechecked the page's tag links and absence of asset filenames.
- **Depth:** compared fresh API JSON structurally against both retained round-43 and round-42 API receipts, including per-field diffs, asset sizes/names/digests, digest counts and body content. Did not rely on a summary claim alone.
- **Calibration:** mutable download counters and page instability are reported separately from substantive drift. No inference that API/page facts establish package behavior or permission to redistribute.

The frozen plan is `plans/round-43-claims.md` at freeze `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`. The measured lane revision for this attack is **`5856614ac4bf7f2363bbcd1956644474a82108e5`**. The lane tip was read before fetching. The attack is specifically the R42 assimilation review's ADMIT flip (`.ufo/waves/round-42/w1/R42Assim.md`, candidate 1): *"refetch shows a ninth release / changed assets / a body stating a version pair"*. The digest-presence pattern is also explicitly tested because it is part of the admitted entry's recheck projection.

## Evidence and findings

Fresh fetch artifacts are under `artifacts/R43W2AssimFlip/`:

| URL | HTTP | fetched bytes | SHA-256 |
|---|---:|---:|---|
| `https://api.github.com/repos/onekey-sec/sasquatch/releases` | 200 | 107313 | `235408bf4bbf6d54af86cf96d616b1229e693607abce15b07d0c12759ff18aa1` |
| `https://api.github.com/repos/onekey-sec/sasquatch/releases?per_page=100&page=2` | 200 | 5 | `2ba33ca0557f1bb5b7ba88d67f9d0093c7185a36ec51fe2b7bd9372d3e001d6d` |
| `https://api.github.com/repos/onekey-sec/sasquatch/tags?per_page=100` | 200 | 9508 | `517fd06a590e7088d30fa4d96e963c2182252a3bffce0e77d5e120b89ca01292` |
| `https://github.com/onekey-sec/sasquatch/releases` | 200 | 349273 | `0af9efe3fc0b7799017c8a5dc26daae8850cceaef0e7cd52d607c56182d88cfe` |

All four fetch commands returned exit 0. Exact fetch commands, timestamps and per-command exits are preserved in `fetch-transcript.txt`; the executable fetch script is `fetch.sh`.

### Ninth release / release identity

- Fresh releases API: **8** objects, with the same eight tags as the retained R43 receipt (`tag_set_equal_r43: true`).
- `?per_page=100&page=2`: parsed JSON item count **0**.
- Tags API: **19** tags, of which exactly the same eight `sasquatch-v*` tags appear; **no new `sasquatch-v*` tag** relative to the release receipt.
- Thus the ninth-release limb is **not triggered**. The tags endpoint is a cross-check, not proof that an unpublished/draft release is absent.

### Changed asset set

Fresh per-release asset counts are **`[6,6,6,6,6,6,6,2]`**, matching the entry and retained receipt. Every asset name remains present; the aggregate asset-name multiset matches R43. Fresh JSON was compared field by field with the committed R43 receipt and R42 receipt:

- Fresh vs R43: **6 differences**, all `download_count` fields.
- Fresh vs R42: **7 differences**, all `download_count` fields; no non-`download_count` differences.
- In particular, release tags, `published_at`, bodies, asset names, sizes and digests did not differ. The entry's eight package-size rows all matched (0 mismatches).
- Canonical structural SHA-256 after removing asset `download_count` (JSON sorted by keys, compact separators): fresh, R42 and R43 each **`1cc30de9cc37473f3093ff9ca6311545159b20e80a7b962df57fd1107667d9d9`**.

The asset-set limb is **not triggered**. The differing download counters are ordinary mutable API metadata; they are not an asset addition/removal/rename/size/digest change.

### Body version-pair

The fresh bodies have lengths `[645,560,0,0,0,38,0,0]` in release order. The three non-empty bodies were read from the fresh JSON: v4.5.1-6 and v4.5.1-5 contain change notes, and v4.5.1-1 says `Rebased on top of squashfs-tools 4.5.1`. A standalone-token check for `1.0` (`(?<![0-9.])1\.0(?![0-9.])`) found **0 of 8** bodies containing it. Therefore the stated body version-pair limb is **not triggered**. This check tests the entry's stated standalone-`1.0` proxy; it does not establish that no wording could imply a version relationship without that token.

### Digest-presence pattern

Fresh digest counts per release are **`[6,0,0,0,0,0,0,0]`**, with projection exactly **`[8,[6,6,6,6,6,6,6,2],[6,0,0,0,0,0,0,0]]`**. All six v4.5.1-6 digest values match the six pins in `corpus/knowledge/2026-10-27-sasquatch-release-matrix.md`; no older release gained a digest and the newest release lost none. This limb is **not triggered**.

### Rendered page

The newly fetched page is 349273 bytes (its response digest differs from earlier same-day captures, consistent with the admitted entry's stated per-request instability). It has **8 distinct `sasquatch-v*` release-tag links** and 0 occurrences each of `sasquatch_1.0_amd64.deb`, `sasquatch_1.0_arm64.deb`, `sasquatch_1.0_armhf.deb`, or `sasquatch-dbgsym_1.0_amd64.deb`. This supports the page's limited claim that its bytes carry tag links but not these asset filenames; asset facts remain grounded in the API.

## Lane-side comparison inputs

- Admitted entry: `corpus/knowledge/2026-10-27-sasquatch-release-matrix.md`, SHA-256 `e1aae6ef1ab05a601f3a76c7f2b4988afa03f8311a1140f5af18cef90646795c`.
- R43 comparison receipt: `.ufo/waves/round-43/w1/artifacts/R43AssimGround/receipts/rel-r43-assimground.json`, SHA-256 `cb42cd61728f994dc18e4937d2d173b543c6a976bea25fa922e50f7213a105d0`.
- Independent R43 comparison receipt: `.ufo/waves/round-43/w1/artifacts/R43ScribeAssim/receipts/rel-r43.json`, same SHA-256 `cb42cd61728f994dc18e4937d2d173b543c6a976bea25fa922e50f7213a105d0`.
- R42 comparison receipt: `.ufo/waves/round-42/w1/artifacts/R42Assim/receipts/rel.json`, SHA-256 `57a19513ca266c10a310504fc33fa16f15e04f92f0be6840c2eb4e6c56a499db`.
- The entry is tracked at the measured lane revision; `corpus/SOURCES.md` is tracked and contains one each of S135, S136 and S137 (`grep -c '^| S13[567] |'` → 3).

The comparison script is `compare.py`; its machine-readable output is `verdict.json`. Both are preserved with the raw responses. Artifact SHA-256s: `compare.py` `718ae7ef133c5ecbfbeb83d659da64882f3b6908be3293111d0210f62ce658f2`; `fetch-transcript.txt` `0b1a3ee0ff82fea5bab11ba4171473831c8992441fc04cf3f1edee4ba90af047`; `fetch.sh` `f261f0a4bd2aa88b324b0e25ea475bbfe892b265bd285b67f4da930b7aa0b078`; `verdict.json` `9043fce01dd9309f2d365fe41864bcc1f46bdc59025612d810b78edcb08a879d`. Raw response hashes are in the table above and in `sha256sum` output from the artifact directory.

## Commands and exits

Commands actually used (all read-only with respect to the lane):

1. `git -C <lane> rev-parse HEAD` → `5856614ac4bf7f2363bbcd1956644474a82108e5` (exit 0).
2. `curl -fsSL -w '\nHTTP_STATUS=%{http_code}\n' -o rel-r43w2.json https://api.github.com/repos/onekey-sec/sasquatch/releases` → HTTP 200 (curl exit 0); analogous fetches for page 2, tags, and rendered page each HTTP 200 / exit 0.
3. `sha256sum` and `wc -c` on each response → exit 0; exact values in `fetch-transcript.txt`.
4. `python3 compare.py` from the assigned scratch directory → exit 0; all comparison findings are in `verdict.json`.
5. `sha256sum` over the committed comparison receipts and admitted entry → exit 0; hashes recorded above.
6. `git -C <lane> ls-files ...` and `git -C <lane> log --oneline -2 -- corpus/knowledge/2026-10-27-sasquatch-release-matrix.md` → entry and SOURCES tracked; latest entry-related commit shown as `eadcbfa5` (exit 0).
7. `grep -c '^| S13[567] |' corpus/SOURCES.md` → `3` (exit 0).

No tool was installed or upgraded. No pacman command, REA, unblob, sasquatch, extractor, firmware input, or VCS mutation was used. Disk check before the probe reported 591G available on both `/fast` and `/home` filesystems. The checks were limited to read-only official API/page fetches and committed receipt/entry comparisons. I did not inspect or copy any published firmware bytes.

## Limitations / inference

- **[INFERENCE]** The public unauthenticated releases/tags endpoints and rendered page are the accessible evidence. They do not expose private or draft releases; this review does not claim those are absent.
- GitHub API `download_count` fields are mutable, and page response bytes vary between requests. Neither is treated as substantive drift.
- The check validates the entry's source-observation claims at fetch time only. It does not prove package contents, extractor compatibility, behavior on carriers, upstream source correctness, or redistribution licensing.
- No assimilation admission framework/control was rerun; this seat attacked the specified fresh-byte flip only.

## Bounds and cleanup

Wrote this report and artifacts only to the assigned lane w2 paths. Scratch path used: `/fast/scratch/hyaku/kaidoku-r43/w2/R43W2AssimFlip/`; it was removed before yield. No production files, commits, VCS state, fleet/sibling/shokuknow paths, or background jobs were changed/used.

Report: `.ufo/waves/round-43/w2/R43W2AssimFlip.md`
