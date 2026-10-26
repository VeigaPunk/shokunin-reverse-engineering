# R39W2C1EntryReview — falsify the round-39 C1 landing (entry, PROVINCE row, README rows)

VERDICT: DEFECTS FOUND — predicate P39-C1 itself **confirmed** at 52b0eb2907c704ed5f184c47b14c723208e5cbbc (6/6 carriers, all bindings true, frozen paths clean, every published number re-derived); two minor documentation defects (D1, D2) and one informational gap (D3), none falsifying.

Axes attacked: coverage (primary — entry/registry numbers vs evidence), depth (entry accuracy as a craft record), calibration (no overclaim).

Measured revision: 52b0eb2907c704ed5f184c47b14c723208e5cbbc (lane HEAD e40a25df adds only the wave-2 dispatch; `git -C <lane> diff 52b0eb2 -- corpus/ PROVINCE.md tools/round-39/ .ufo/waves/round-39/c1/` is empty, so every file cited below is byte-identical to the review commit). Freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b is an ancestor (`git merge-base --is-ancestor` → 0).

## 1. Every published number re-derived from the committed evidence — all match

Commands (jq over `corpus/evidence/round-39/c1/K*/after.json`, `corpus/evidence/round-39/c1/K*/symlinks.tsv`, `.ufo/waves/round-39/c1/carriers.json`):

| carrier | files published (claimed) | re-derived | gaps (claimed) | re-derived | gap kind | in-tree/escaping (claimed) | re-derived (symlinks.tsv) |
|---|---|---|---|---|---|---|---|
| K1 | 5 | 5 | 0 "none" | 0 | — | 0 / 1 | 0 / 1 |
| K2 | 3 | 3 | 1 | 1 | `unpublished-entry` | 1 / 0 | 1 / 0 |
| K3 | 4 | 4 | 0 "none" | 0 | — | 0 / 0 | 0 / 0 |
| K4 | 4 | 4 | 0 "none" | 0 | — | 0 / 0 | 0 / 0 |
| K5 | 10 | 10 | 2 | 2 | `unpublished-entry` ×2 | 2 / 1 | 2 / 1 |
| K6 | 8 | 8 | 1 | 1 | `unpublished-entry` | 1 / 2 | 1 / 2 |

- `jq '(.normalized_result.files|length)'` → 5, 3, 4, 4, 10, 8; `(.normalized_result.extraction_gaps|length)` → 0, 1, 0, 0, 2, 1. Matches the entry table (`corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md:15-20`), the PROVINCE row (`PROVINCE.md:382` "(5, 3, 4, 4, 10, 8) … (0, 1, 0, 0, 2, 1)") and README rows (`corpus/README.md:93,203`).
- Gap paths equal the in-tree link set exactly: K2 `firmware.bin_extract/var/lib/run-link`; K5 `…/usr/share/demo/link-blob`, `…/usr/share/demo/link-notes`; K6 `…/a/b/link-in`. No other gap kind anywhere.
- `normalized_result.unpublished_entries` carries the kept links with their targets (`link-blob → ../opt/blob.bin`, `link-notes → notes.txt`) — matches symlinks.tsv.
- Every `symlinks.tsv` sha256 matches `carriers.json .symlinks_sha256` (6/6); every carrier pin matches the on-disk carrier bytes (6/6, `sha256sum`).
- Every oracle row (`corpus/evidence/round-{37,39}/c1/K*/oracle.tsv`, 5/3/4/4/10/8 rows) matches a published file by relative-path suffix **and** sha256; published count == oracle count, so no extra files.
- All six chunks: `handler == "squashfs_v4_be"`, `extraction_failed == false` ("no chunk fails" holds).
- Subject digest == frozen carrier pin for all six (`jq '.subject.digest.sha256'`).

## 2. Symlink rule and removal reports — confirmed from retained receipt bytes

- K1/K5/K6 `raw_result.report` holds `MaliciousSymlinkRemoved` for exactly the escaping links: K1 `link-to-hello` (target resolved `<…>/extracted/hello.txt`, outside `firmware.bin_extract`), K5 `usr/share/demo/escape` (`…/extracted/etc/shadow`), K6 `data/escape-deep` (`…/K6-scratch/etc/passwd`) and `outside` (`…/extracted/outside`) — counts 1/1/2, matching the tables; no published path for any escaping link (`grep -iE "escape|outside|link-to-hello"` over published paths → nothing).
- Containment arithmetic re-done by hand for all 8 links under "target joined to the link's directory, resolved, still under the per-chunk extraction directory" (entry :27-29): K2 `var/lib` + `../../a/run.sh` → `<chunkroot>/a/run.sh` in-tree ✓; K5 `usr/share/demo` + `../../../../etc/shadow` → above root ✓ escaping; K6 `a/b` + `../../etc/config.ini` → `<chunkroot>/etc/config.ini` in-tree ✓. The entry's "does not clamp `..` at the root, so a root-level `../hello.txt` escapes (K1)" is exactly what the K1 receipt shows.
- Independent reader: `python3 -I -B tools/round-39/sqfs-list.py <carrier> --files … --symlinks …` exit 0; output diff-equal to the committed `oracle.tsv` and `symlinks.tsv` for K1, K5, K6 (sorted diff, empty).
- Direct extractor: `sasquatch-v4be -be -d <scratch>/out <carrier>` exit 0; K5 10/10 files, K6 8/8 files, sha256-equal to the oracle, no extras.
- K6 superblock parsed from bytes: magic `sqsh`, compression id **4** (offset 20:22 BE), s_major 4, and exactly **4** occurrences of the xz magic `fd 37 7a 58 5a 00` — matches the claims file's "compression id 4, four compressed xz data blocks". K5: block_size 4096, largest file `var/lib/state.db` 20000 B = 5 blocks, `empty.flag` 0 B, UTF-8 name `アイコン.txt`, space name `notes with space.txt` — matches the entry's K5 row.

## 3. S122 source line vs the live URL — confirmed

- Fetched `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/file_utils.py` (curl, exit 0): 27989 B, sha256 `87d4dc9a51bc4e92ee410fba77dfcf88fb32266e58e1e6be0ea70bfe44320745` — equal to the SOURCES.md S122 row (`corpus/SOURCES.md:128`) and byte-identical (`diff`) to the installed copy at `~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/file_utils.py`.
- `def is_safe_path` is at line 34; the body `basedir.joinpath(path).resolve().relative_to(basedir.resolve())` / `except ValueError: return False` / `return True` spans 34-39 — the entry's "lines 34-39" (`…r39-be-squashfs-v4-core.md:3`) and the S122 row are accurate.
- S122 used-by (col 12) lists `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md`; status mined, opened 2026-10-26 (17:09:05Z = 14:09:05-03:00, before the entry's introducing commit 6fdaf4f1 at 14:18:32-03:00 — QUALITY 23 satisfied).
- Recheck command runs and prints 1: `grep -c 'basedir.joinpath(path).resolve().relative_to(basedir.resolve())' ~/.local/share/uv/tools/unblob/…/file_utils.py` → `1`, exit 0 (entry :5).

## 4. Counter, freeze integrity, provenance — confirmed

- Counter at the review revision: `python3 -I -B tools/round-39/c1-counter.py --root <lane> --rev 52b0eb2… --freeze 8fcda41c… --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <scratch>/c1-counter-at-52b0eb2.json` → exit 0, `met_target: true`, `carriers_matched: 6`, all 9 bindings true, `frozen_path_changed: []`. Same shape as the author's receipt `.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json`.
- Unmoved command: same counter with `--rev 8fcda41c…` → **exit 1**, `carriers_matched: 0` (claims' "Command that shows it unmoved" holds).
- Evidence ids re-minted independently: froze `tools/round-27/xpin-attribute.mjs` at the freeze into scratch, wrapped each after.json as `{"data": …}`, ran `node xpin-attribute.mjs --pkg65 <rea-agents 6.5.0> --pkg67 <same>` → all six minted ids equal the stored `.evidence_id` (QUALITY 78's recompute — noted below this is not provenance by itself).
- Run provenance (run.json, all six): rea-agents 6.5.0 (pin + package root), unblob 26.6.4 (`REA_UNBLOB_COMMAND` env value `/home/vgpnk/.local/bin/unblob`, resolved `…/uv/tools/unblob/bin/unblob`, sha256 `0ce7b624…`), `sasquatch-v4be` 4.5.1 at `/home/vgpnk/.local/bin/sasquatch-v4be` (sha256 `fac88740…`), child PATH contains `/home/vgpnk/.local/bin`, output directories under `/fast/scratch/hyaku/kaidoku-r39/l1/c1runs/K*-scratch/extract` (contains `/kaidoku-r39/`, no `..`).
- Commit topology: controls 72359309 (14:16:27) → C2 held-out data 3c07eed7 (14:18:28) → C1 receipts+entry+rows 6fdaf4f1 (14:18:32) → lesson/scores 52b0eb2 (14:22:52), all descending from the freeze (14:12:51). `git log 8fcda41c..52b0eb2` over the frozen C1 paths (counter, c1-run.sh, carriers.json, carriers, oracles, symlink tables) touches none of them; the only listed commit 6fdaf4f1 is the data/docs commit itself. Carriers.json, c1-counter.py, c1-run.sh, gen-squashfs.py, sqfs-list.py all first-added at the freeze.

## 5. Defects

**D1 (minor, doc staleness — superseded text left without an inline pointer).** `PROVINCE.md:157` (at 52b0eb2): the Frontier bullet's inline bracket still asserts "big-endian/AVM stays here. Round 38: … **not promoted** — R38-C1 honest stop, K2's in-tree symlink leaves an `unpublished-entry` gap." and `PROVINCE.md:376` (round-38 note) still ends "Big-endian SquashFS stays Frontier." Both are superseded for standard BE by the round-39 row (:382) and the round-39 frontier note (:384), but neither line carries a round-39 pointer — the supersession is recorded only ~230 lines below at :384. Rounds 36 and 38 both annotated the bullet inline (the bracket at :157 is their work); round 39 broke that pattern. The frozen predicate is satisfied (the note exists and names the bullet `PROVINCE.md:156-157` and the entry stem), so this is not a claim failure — but a reader at :157 or :376 gets the wrong current status, and the lane fixed exactly this pointer-hygiene class in this same commit (the R36-CL2 sentence appended to the note at :384). Suggested fix: append a round-39 pointer to the :157 bracket and a one-clause pointer to the :376 note.

**D2 (minor, evidence-scope overreach in the entry).** `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md:37-38`: "Without `sasquatch-v4be` on the child `PATH` **the same carriers** publish nothing and carry `missing-extractor-dependency` naming `sasquatch-v4be` (round-38 before-arms)." "The same carriers" reads as the six carriers of the table above, but the cited round-38 before-arms cover only K1–K4; no before-arm receipt exists for the K5 (5999eafc…) or K6 (00152518…) bytes anywhere in the lane — the wave-1 stripped-PATH arms ran on different recon carriers (`w1/artifacts/R39C2ReconDep/envelopes/stripped-be1-gzip.json` subject `ae673f04…`, `stripped-be2-gzip.json` `afbf53ed…`; feature-table rows 20-27), and `w1/R39Sentinel.md` ran no REA at all. The mechanism claim is certainly true at handler level, but for K5/K6 it is inference from other bytes stated in observation voice — per QUALITY 5/10 it should be scoped ("the round-38 carriers; K5/K6 not run without the dependency") or labeled [INFERENCE].

**D3 (informational, QUALITY-82-adjacent).** `…r39-be-squashfs-v4-core.md:41-42`: "no third-party BE v4 writer is available" is a negative availability claim with no stated sweep root or scope. The operative reason given ("`mksquashfs` writes LE only") checks out on this host (`mksquashfs -help` exposes no endian option; `/usr/bin/mksquashfs` present), and the sentence is not load-bearing for the predicate — noted for completeness, no action required.

## 6. QUALITY bar check (applicable rows)

1 (resolvable source: S122 ✓), 2 (falsifiable ✓ — counter + re-derivable numbers), 4 (carriers pinned by sha256 ✓), 5/10 (held claims run on real carriers this round ✓, except D2's voice), 7 (Limits name what was not held ✓), 8 (versions pinned ✓), 12 (K5/K6 synthesized carriers committed as bytes + generator `tools/round-39/gen-squashfs.py` committed at the freeze ✓), 13 (recheck command reproduces ✓), 23 (S122 opened 14:09:05-03:00 ≤ entry commit 14:18:32-03:00 ✓; entry dates are date-only/zoneless, unchecked per row 23), 78 (recompute-not-provenance limit is disclosed in the entry (:42-43) and the claims' disclosed-limit paragraph; this seat's independent reader + direct-sasquatch semantic-payload comparison is the row-78-style corroboration for the published set), 79 (frozen-drift clean at the measured revision ✓), 82 (D3-adjacent only).

## 7. Residual risk / verification gaps

- I did not re-run REA `extract-firmware` myself; the committed receipts' semantic payload was instead compared against two independent producers (stdlib `sqfs-list.py`, direct `sasquatch-v4be -be`) — the full re-run comparison is the assigned work of the R39W2ReproK4/K5 seats.
- The counter's 33-case selftest was not re-run here (other wave-2 seats cover counter internals; my scope was the entry/registry rows).
- "Absolute targets are re-rooted and kept" (entry :31) is not exercised by any frozen carrier (all targets relative) — it stands on S118/S119 via the triage entry's Symlinks paragraph (`corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md:41`), which exists as cited.
- LOG.md/SCORECARD.md carry no round-39 rows yet at 52b0eb2 — expected mid-wave (filing happens after wave 2); not judged here.

## 8. Tooling record

No tool installed, upgraded, moved or removed. Used only: `python3` (stdlib), `jq`, `node` (for the frozen xpin re-mint), `curl` (S122 fetch), `git` (read-only verbs), `sasquatch-v4be` 4.5.1 (read-only use, extraction into scratch), `diff`/`sha256sum`/`grep`. No pacman transaction; no REA invocation (not needed for this seat's scope); no VCS mutation.

Artifacts copied to `.ufo/waves/round-39/w2/artifacts/R39W2C1EntryReview/`: `c1-counter-at-52b0eb2.json`, `c1-counter-at-freeze.json`, `xpin/out.tsv` (re-minted ids), `file_utils_live.py` (S122 fetch), `recheck/K{1,5,6}-{files,symlinks,sasquatch}.tsv` (independent-reader and direct-extractor outputs).

Report: .ufo/waves/round-39/w2/R39W2C1EntryReview.md
