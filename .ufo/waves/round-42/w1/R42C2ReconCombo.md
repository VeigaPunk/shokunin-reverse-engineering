# R42C2ReconCombo — legacy-family combo recon (draft R42-C2 steps 1–13)

Verdict: **CONFIRMED** — the hypothesis holds on real REA envelopes: the round-41 combo factors combine with a legacy-family factor only through *damage, dependency reachability, max_depth and a second (v4) chunk*; symlink factors are not constructible on the v1–v3 member (no v3 writer in the lane). Measured refinements for the draft: the v1–v3 handler names are endian-agnostic (`squashfs_v1/v2/v3`, plus nonstandard/broadcom/ddwrt/adaptive variants), draft step 3's "plain `sasquatch`" claim is **confirmed** for every v1–v3 chunk and v4 LE, and the new step-6 `legacy-body-failure` branch is reachable in both endiannesses with P=0. **One constructional warning**: on the frozen unblob v3 fixtures a *partial* (P>0) v3 failure is **not** constructible — every failing mutation produced P=0 or was absorbed to `clean`; partial legacy bodies need a larger real v3 rootfs or a second chunk.

## 1. Scope and method

Item: verify that legacy (v1–v3) carriers can participate in the round-41 combo factorial family only via the factors that are constructible without a v3 writer (damage, dependency reachability, max_depth, a second v4 chunk). Development inputs only: unblob 26.6.4 SquashFS test fixtures (MIT, LFS) and v4 images built with the lane's `tools/round-41/gen-squashfs.py` writer. No reserved carriers were touched; no REA/unblob run was made on any R42C1Img* candidate.

- Toolchain (unchanged, nothing installed): `rea-agents@6.5.0` via `npx -y` (npm cache), `unblob` 26.6.4 (`$HOME/.local/bin/unblob`, absolute `REA_UNBLOB_COMMAND`), `sasquatch`/`sasquatch-v4be` 4.5.1 (`$HOME/.local/bin`), oracles `unsquashfs` 4.7.5 and `7z` 26.04.
- REA command shape (fresh outdir every run, `cd $S`, depth 1 or 3): `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json --full-output [--max-depth N] <input> <fresh outdir>`. Dependency-missing arm strips `$HOME/.local/bin` from the child PATH (round-41 `arm=before` semantics).
- Fixtures fetched (sha256 in `artifacts/R42C2ReconCombo/fixtures.sha256`): `squashfs_v1.0_le.bin`, `squashfs_v2.0_le.bin`, `squashfs_v3_le.bin`, `squashfs_v3_be.bin`, `squashfs_v3_le.lzma.bin` (adaptive), `bad_symlink.squashfs` (v4 LE). All six are read by **both** oracles (unsquashfs `-s`/`-d`, 7z `l`).
- All 27 REA runs exited 0. Envelope JSONs are in `artifacts/R42C2ReconCombo/envelopes/*.envelope.json`; `summary.json` holds the feature tuple, the draft label step and the named-inventory membership of every run.

## 2. Handler names and dependency resolution (draft step 3)

From unblob 26.6.4 source (`handlers/filesystem/squashfs.py`): v1/v2/v3 family handler names are `squashfs_v1`, `squashfs_v2`, `squashfs_v2_nonstandard`, `squashfs_v3`, `squashfs_v3_ddwrt`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`; only v4 is endian-suffixed (`squashfs_v4_le`, `squashfs_v4_be`, `squashfs_v4_broadcom`). `SquashFSExtractor` uses `sasquatch` for every v1–v3 chunk and for v4 LE; `sasquatch-v4be` only for v4 BE; `-be`/`-le` are appended by endianness (BIG → `-be` for all non-v4BE, and for v4 BE when the AVM marker is absent).

Measured on real envelopes (D = union of `extraction_gaps[].dependencies`):

| run | chunk handler | D when dependency missing | draft step 3 outcome |
|---|---|---|---|
| v3 LE, v3 BE | `squashfs_v3` | `{sasquatch}` | `dep-missing-le` / `install-extractor-le` |
| v1 LE | `squashfs_v1` | `{sasquatch}` | `dep-missing-le` / `install-extractor-le` |
| v2 LE | `squashfs_v2` | `{sasquatch}` | `dep-missing-le` / `install-extractor-le` |
| v4 LE (writer) | `squashfs_v4_le` | `{sasquatch}` | `dep-missing-le` / `install-extractor-le` |
| CB5 (v3 LE + v4 BE) | `{squashfs_v3, squashfs_v4_be}` | `{sasquatch, sasquatch-v4be}` | `dep-missing-be` / `install-extractor-be` (step 3 first branch wins) |

Draft step 3's bracketed claim — *every v1–v3 chunk and every v4 LE chunk resolves plain `sasquatch`* — is **CONFIRMED**. Note a BE v3 chunk with missing dependency still labels `dep-missing-le` (its only dependency is plain `sasquatch`). The mixed CB5 case confirms the order-sensitivity: D containing `sasquatch-v4be` wins the BE label.

## 3. Legacy body failure (draft step 6) — reachable, both endians

The v3 metadata-zero recipe: zero bytes `[96, bytes_used)` of the fixture (bytes_used = 258 LE / 255 BE; data+metadata beyond the superblock). The handler is still selected, `sasquatch` fails before publishing anything.

| run | features (H; G; BE; SR; P) | label |
|---|---|---|
| CB7 (v3 BE body-failure) | `{squashfs_v3}`; `{extractor-failure}`; BE=yes (argv contains `-be`); SR=false; P=0 | `legacy-body-failure` / `cross-read-legacy` (step 6) |
| CB8 (v3 LE body-failure) | `{squashfs_v3}`; `{extractor-failure}`; BE=no (argv contains `-le`); SR=false; P=0 | `legacy-body-failure` / `cross-read-legacy` (step 6) |

Cross-read feasibility of the action: for both carriers `unsquashfs -s`/`-d` fails on the same bytes (metadata unreadable), i.e. the cross-read separates damage from an extractor build fault as the draft intends, and the envelope's `ExtractCommandFailedReport` records the exact binary (`sasquatch -be …` / `sasquatch -le …`). Boundary checks: `squashfs_v3` never matches step 5 (handler ≠ `squashfs_v4_be`), so the new step 6 is the only branch that can own a P=0 legacy failure; a failing `squashfs_v4_le` with P=0 correctly falls to step 7 (`body-extractor-failure`).

## 4. The six requested combos (all run through REA, exit 0)

| ID | construction | observed features (H; G; D; BE; SR; P) | draft label (step) |
|---|---|---|---|
| CB1 | v3 LE fixture @0 + v4 LE with in-tree symlink @4096, depth 3 | `{squashfs_v3, squashfs_v4_le}`; `{unpublished-entry}`; ∅; n/a; false; 3 | `in-tree-symlink-metadata` / `count-gap` (11) |
| CB2 | v4 LE containing the v3 fixture as a file, depth 1 | `{squashfs_v4_le}`; `{depth-limited}`; ∅; n/a; false; 2 | `depth-limited` / `raise-depth` (8) |
| CB3 | same carrier as CB2, depth 3 | `{squashfs_v3, squashfs_v4_le}`; ∅; ∅; n/a; false; 4 | `clean` / `none` (12) |
| CB4 | v3 BE fixture, dependency missing | `{squashfs_v3}`; `{missing-extractor-dependency}`; `{sasquatch}`; n/a; false; 0 | `dep-missing-le` / `install-extractor-le` (3) |
| CB5 | v3 LE fixture @0 + v4 BE @4096, dependency missing | `{squashfs_v3, squashfs_v4_be}`; `{missing-extractor-dependency}`; `{sasquatch, sasquatch-v4be}`; n/a; false; 2 | `dep-missing-be` / `install-extractor-be` (3) |
| CB6 | v3 BE fixture @0 + v4 BE with escaping symlink @4096, depth 3 | `{squashfs_v3, squashfs_v4_be}`; ∅; ∅; n/a; **true**; 3 | `escaping-symlink-removed` / `expect-link-absent` (10) |

CB3's inner v3 chunk is byte-identical to the frozen fixture (`sha256 0161351c…` on both sides) and is read by unsquashfs and 7z; CB1's in-tree link surfaces as `unpublished-entry` with `relative_path` naming `…/4096-4630.squashfs_v4_le_extract/link`; CB6's escaping link surfaces as `MaliciousSymlinkRemoved` with no gap (SR=true, G=∅) — exactly the v4 taxonomy the precedence relies on.

## 5. Reachability matrix (which combinations exist)

Constructible without a v3 writer:

- single legacy chunk: clean (any endian; v1/v2/v3/adaptive all measured `clean`), dependency-missing (`D={sasquatch}`), body-failure P=0 (both endians, recipe above);
- legacy + second v4 chunk: v4 member may carry in-tree or escaping symlinks, damage (zero-id-table), or both chunks fail on missing deps (mixed D set);
- legacy nested *inside* a v4 image (depth 1 hides it → step 8; depth 3 reveals it → step 12);
- trivial: same v4 carrier at depth 1 vs 3 (CB2/CB3) exercises max_depth without any v3 writer.

Not constructible on the frozen inputs:

- **symlinks on the v1–v3 member** — no v3 writer exists anywhere in the lane (`tools/` has only v4 writers; round-41/42 plans confirm). Symlink factors can only enter through a v4 member;
- **v3 as outer image containing nested v4** (requires writing v3);
- **partial (P>0) v3 body failure** on the tiny frozen fixtures — measured: every failing zero-mutation of the v3 fixture produced P=0 `extractor-failure` (metadata first), and tail/padding zeroing (26 B, 64 B, 128 B, 512 B, 2048 B mid, 8 B at [250,258)) was absorbed to `clean` with corrupt bytes on disk (cf. R40-CL4 pin; the fixtures store all files in one fragment, so the "last data block" target of `corruption_partial` is not reachable). A legacy partial body therefore needs a real larger v3 rootfs (e.g. OpenWrt Kamikaze 7.09 development images) or a second chunk.

## 6. Which tuples no named class produces

The round-41 held-out set has 40 named-class carriers; their `declared` six-field tuples form 27 distinct inventory tuples, all with a single `squashfs_v4_*` handler. Comparison of the measured combo tuples (same six fields: H, G, D, BE, SR, P-class):

- Outside the named inventory (7/8 combos): CB1, CB3, CB4, CB5, CB6, CB7, CB8 — every hand that contains a v1–v3 handler name or a two-handler set is unseen; so are the clean single-chunk v1/v2/v3 probes (handler names differ from `squashfs_v4_*`).
- Inside the named inventory (1/8): **CB2** — depth 1 hides the legacy member, so its observable tuple is exactly the v4 `depth-limited` named tuple. This is a real dimensionality trap for the widened combo family: a combo whose legacy factor is unobservable does not add anti-lookup pressure. Recommendation for `heldout-gen-v4.py`: draw combo legacy factors only where the legacy handler is observable in the envelope (or declare the factor tuple separately and let the lookup comparison use it), otherwise the lookup control will legitimately hit those carriers (draft target: lookup scores strictly fewer than half of combos).

The CTL-C2-9 note: the v3 row of the table must not use a `squashfs_v4_*` handler cell — the legacy handler names have no endian suffix (`squashfs_v3`), and step 6's "v1–v3 handler" test must match the family names (including `_nonstandard`, `_ddwrt`, `_broadcom` variants).

## 7. Evidence

- Carriers and meta: `artifacts/R42C2ReconCombo/carriers/{CB1..CB8}.bin` + `.meta.json` (each carries sha256/size/chunk layout/depth/arm).
- Envelopes (27): `artifacts/R42C2ReconCombo/envelopes/*.envelope.json` (REA `--format json --full-output`, exit 0 each).
- Feature/label summary: `artifacts/R42C2ReconCombo/summary.json` (includes per-run `in_named_inventory`).
- Scripts: `build_combos.py` (v4 writer import from `tools/round-41/gen-squashfs.py`, two-chunk assembly, v3 metadata-zero recipe), `run_rea.sh` (fresh outdir, absolute `REA_UNBLOB_COMMAND`, PATH-strip arm), `labels_v4.py` (draft steps 1–13 transcription), `feat.py` (feature extraction).
- Fixture sha256: `artifacts/R42C2ReconCombo/fixtures.sha256`.
- Tool installs: none (no tool was installed or updated; `npx` reused cached `rea-agents@6.5.0`).
