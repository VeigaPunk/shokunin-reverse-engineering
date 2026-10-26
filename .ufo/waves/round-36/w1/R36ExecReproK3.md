# R36ExecReproK3 — independent reproduction of R36-C1 carrier K3

Seat: leaf executor, round 36 wave 1. Advisory only; no frozen predicate, counter, carrier or
oracle was changed, and nothing outside this file was written.

**Verdict: K3 reproduces exactly.** Both of my REA extract-firmware runs (sasquatch-on-PATH and
sasquatch-filtered-PATH) reproduce the committed `after.json` / `before.json` file-set and gap
evidence with 0 differing entries; my independent `/usr/bin/unsquashfs` run reproduces the committed
`oracle.tsv` byte-for-byte. Two advisory nuances are recorded in §7 — neither is a defect in the
committed evidence, one is a wording hazard for the frozen counter's `dependencies` expectation.

---

## 1. Environment (all versions as observed, no installs performed)

| component | value | how observed |
|---|---|---|
| rea-agents | `6.5.0` | `npx -y rea-agents@6.5.0 --version` → `6.5.0`, exit 0 |
| unblob | `26.6.4` | `~/.local/bin/unblob --version` → `26.6.4`; receipt `normalized_result.engine.executable_path` = `/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob` in **both** receipts |
| sasquatch | `unsquashfs version 4.5.1 (2022/03/17)` | `~/.local/bin/sasquatch -version` |
| sasquatch sha256 | `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` (382824 B) | `sha256sum` |
| sasquatch-v4be sha256 | `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6` (436232 B) | `sha256sum` |
| unsquashfs (oracle) | `unsquashfs version 4.7.5 (2026/03/01)` | `/usr/bin/unsquashfs -version` |
| node used for id recompute | `fnm_multishells/6713_1792986395296/bin/node` | `command -v node` |

No tool was installed, upgraded or removed. `sasquatch` 4.5.1 was already in `~/.local/bin`
(L1-installed); I used it read-only.

PATH fact used by the whole comparison: **exactly one** PATH directory holds an executable
`sasquatch` — `/home/vgpnk/.local/bin`. Filtering by that predicate drops that single directory
(`before` PATH has 19 entries vs 20), so `after`-PATH and `before`-PATH differ by exactly one
directory. `unblob` stays reachable in both modes because the harness exports the absolute
`REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob`; both receipts name the same engine executable.

## 2. Carrier acquisition (frozen URL, digest checked)

```
curl -fsSL -o nvim-linux-x86_64.appimage \
  https://github.com/neovim/neovim/releases/download/v0.12.6/nvim-linux-x86_64.appimage
sha256sum → b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb   (11454968 bytes)
```
Equal to `carriers.json` K3 `sha256` and to `subject.digest.sha256` in both committed receipts.
`carriers.json` K3 entry is `{"url": ".../nvim-linux-x86_64.appimage", "sha256": "b644d034…f29fb"}` —
the lane holds no K3 fixture copy, so the download is the carrier (as the claim states).

## 3. Squashfs offset, derived independently

ELF64 LE header of the carrier: `e_shoff=942712`, `e_shentsize=64`, `e_shnum=30` →
`942712 + 64*30 = 944632`; bytes at 944632 are `hsqs`. Superblock read at that offset:
`inodes=2247`, `block_size=131072`, `comp=6` (xz), `major=4`, `minor=0`, `bytes_used=10507255`,
file size 11454968. Matches harness-computed offset and committed `oracle-run.json`
(`squashfs_offset: 944632`).

## 4. Oracle reproduction (`/usr/bin/unsquashfs` at offset 944632)

```
bash tools/round-36/c1-run.sh oracle <carrier> <out>/oracle <scratch>   # exit 0
```
- rows written: **2130** (`regular_files: 2130`, same as committed `oracle-run.json`).
- `diff -q` against `corpus/evidence/round-36/c1/K3/oracle.tsv` → **no output, exit 0: byte-identical**.
- entry-type census of my own extraction tree: `regular 2130`, `symlink 2`, `dir 114` (+root) —
  2130+2+115 = 2247, exactly the superblock `inodes` count. The 2 symlinks are
  `.DirIcon → nvim.png` and `nvim.png → usr/share/icons/hicolor/128x128/apps/nvim.png`.

So the committed oracle is genuinely "all regular files, regular files only", and I reproduced it
from an independent extraction with an independent unsquashfs (4.7.5).

## 5. REA runs (`c1-run.sh after|before`, my carrier, my scratch)

Both used `tools/round-36/c1-run.sh` (the frozen harness) so the PATH filter is the frozen one:
`before` = every PATH dir holding an executable `sasquatch` removed, `after` = PATH as given.
Harness exit 0 in both cases.

| | committed `after.json` | my after run | committed `before.json` | my before run |
|---|---|---|---|---|
| `normalized_result.files` | 2147 | **2147** | 2 | **2** |
| `(relative_path, sha256)` set | — | **identical, 0 only-committed / 0 only-mine** | — | **identical, 0 / 0** |
| `published_bytes` | 51122564 | 51122564 | 11454968 | 11454968 |
| `coverage` | partial | partial | partial | partial |
| `chunks` | 27 | 27 | 3 | 3 |
| `derivations` | 2265 | 2265 | 2 | 2 |
| `unpublished_entries` | 2 | 2 | 0 | 0 |
| `diagnostics` | 0 | 0 | 1 | 1 |
| unblob `execution.exit_code` | 0 | **0** | 1 | **1** |
| REA CLI exit | — | **0** | — | **0** |
| `evidence_id` | `ev_b83bd30…f5419b` | `ev_8634def…45fd71` | `ev_91e4ab3…e9a44a` | `ev_3990ac8…115b5d0c` |

Gap comparison (kind / dependencies / handler / input_path / relative_path tuples, exactly as the
seat asked):

- **after, committed == mine:**
  `[["unpublished-entry", [], null, "$output/firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/.DirIcon", "firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/.DirIcon"], ["unpublished-entry", [], null, "…/nvim.png", "…/nvim.png"]]`
  → **no `missing-extractor-dependency` gap, and no `sasquatch` anywhere in the after gaps.**
  The 2 unpublished entries are exactly the 2 symlinks of §4, with correct `link_target` values
  (`.DirIcon → nvim.png`, `nvim.png → usr/share/icons/…/nvim.png`), published as metadata only.
- **before, committed == mine:**
  `[["missing-extractor-dependency", ["sasquatch"], "squashfs_v4_le", "$input", null]]`, with
  `diagnostics[0] = {input_path:"$input", stage:"squashfs_v4_le", missing_dependencies:["sasquatch"],
  report:{severity:"ERROR", dependencies:["sasquatch"], __typename__:"ExtractorDependencyNotFoundReport"}}`
  and `chunks[squashfs_v4_le].extraction_failed = true`.

Oracle coverage, computed per run by suffix path + sha256 against the committed `oracle.tsv`
(2130 rows):

| run | oracle rows matched | unmatched |
|---|---|---|
| my after (sasquatch on PATH) | **2130 / 2130** | 0 |
| my before (sasquatch filtered) | **0 / 2130** | 2130 (its 2 published paths are whole-file chunks: `firmware.bin_extract/0-944632.elf64_extract/carved.elf`, `firmware.bin_extract/944632-11454968.squashfs_v4_le`) |

Extra (non-oracle) published paths in the after run — **17**, fully enumerated:
1 outer carve `firmware.bin_extract/0-944632.elf64_extract/carved.elf` (944632 B);
8 × `<squashfs_extract>/<file>_extract/0-<n>.elf64_extract/carved.elf` (depth 2, whole-file chunks);
8 × `…padding` (1 B each, `analysis_depth: null`). 2130 + 17 = 2147. This matches the pre-freeze
disclosed probe behaviour ("unblob keeps whole-file chunks and publishes recursion output beside
them"); depth histogram of published files: `{1: 2131, 2: 8, null: 8}`, no duplicate
`relative_path`.
unblob's own stdout: after = 2140 files / 124 dirs / 2 links, chunk types ELF64 73.90% +
SQUASHFS_V4_LE 26.10% + PADDING, no ERROR row; before = 2 files / 1 dir / 0 links with
`Severity.ERROR ExtractorDependencyNotFoundReport`.

## 6. Evidence ids: recomputed, and why mine differ

Both committed receipts **recompute to their stored id**, and so do both of mine, under the package's
own rule — `ev_` + `digestCanonicalValue(semanticProjection(evidence))` (RFC-8785 canonical JSON,
SHA-256; `dist/domain/evidence.js:156-182`, hasher `dist/domain/canonicalDigest.js`). I executed the
package's real `digestCanonicalValue` from
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/canonicalDigest.js`
in node against a literal transcription of `semanticProjection`:

| receipt | stored | recomputed | match |
|---|---|---|---|
| committed K3/after.json | `ev_b83bd3056f103a72e2a611a5162f542715119490a44bb60135393b5002f5419b` | same | **true** |
| committed K3/before.json | `ev_91e4ab30b6a5edf4ab7a14d5a14867cac75b0e161090c5db7db6b73027e9a44a` | same | **true** |
| my after.json | `ev_8634defde0e1805304025827720b131f28dbc092a71efd090207b95a2245fd71` | same | **true** |
| my before.json | `ev_3990ac86fb9545cfba24184cb1a88faf66e0e474e85dc9f8adb31aa8115b5d0c` | same | **true** |

Id difference between my receipts and the committed ones is **fully accounted for and not counted**
(semantic projection includes `parameters` and `normalized_result`, hence the volatile paths). A
field-level flatten of both documents shows **exactly 5 differing scalar paths per pair**, and all 5
are path metadata:

```
.evidence_id                      (consequence of the 3 below)
.parameters.output_directory      …/c1-run.7PV16k/out          vs …/R36ExecReproK3/work/after.2888/out
.normalized_result.output_directory  (same two values)
.parameters.path                  …/kaidoku-r36/L1/carriers/nvim-linux-x86_64.appimage
                                  vs …/kaidoku-r36/R36ExecReproK3/carriers/nvim-linux-x86_64.appimage
.subject.local_path               (same two values)
```
`before` shows the identical 5-path pattern. `raw_result.execution.stdout.text`,
`normalized_result` arrays, `subject.digest.sha256`, `engine.*`, `limitations`, and `locations` are
byte-equal between committed and mine. `[INFERENCE]` The claim's "both receipts recompute to their
stored evidence id" is therefore satisfied by construction, and my parallel receipts cannot collide
with the committed ids unless output dir and carrier path are also reused.

## 7. Two advisory nuances (reported, not repaired)

1. **`dependencies` is the runtime-failed executable, not the handler's static list.** unblob
   `handlers/filesystem/squashfs.py` declares
   `SquashFSExtractor.get_dependencies() -> ["sasquatch", "sasquatch-v4be"]`, but the report is raised
   from `extractors/command.py:70` as
   `ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())` on the `Command`
   instance actually executed, and `Command.get_dependencies() -> [self._executable]`
   (`extractors/command.py:101-102`). For a little-endian v4 image the chosen executable is
   `sasquatch`, so the observed gap is `dependencies == ["sasquatch"]` — matching the frozen
   expectation for K3, but only because K3 is LE. **A BE/AVM carrier would name `sasquatch-v4be`**
   (out of scope by the claim's "Not claimed" line). Any later counter that hard-codes the
   handler-level pair, or that runs a BE carrier, would see a different list. No action for K3.
2. **Removing the `sasquatch` PATH directory removes both binaries.** `/home/vgpnk/.local/bin` holds
   `sasquatch` *and* `sasquatch-v4be`, so the frozen `before` filter drops both. That is harmless
   here (unblob only names `sasquatch` and only for LE), and it is why I ran the discriminator in §8
   rather than assuming the filter isolates one variable.

## 8. Extra falsifier I ran: sasquatch *alone* closes the gap

To rule out "the after file set was produced by `sasquatch-v4be`, or by a 7z fallback, or by the
filtered directory's absence", I ran a third REA extraction with a hand-built PATH:
`<scratch>/bin` (holding only a symlink to `sasquatch`) prepended, `~/.local/bin` removed, everything
else unchanged; asserted `command -v sasquatch → <scratch>/bin/sasquatch` (sha `ad02d27a…`),
`command -v sasquatch-v4be → ABSENT`, `node` still resolvable.

Result: `files=2147`, unblob `exit=0`, gaps = the same 2 `unpublished-entry` items,
**published set identical to the full after run (0/0 diff)**, receipt records
`sasquatch_sha256 = ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`.
So `sasquatch` alone is sufficient and necessary for this carrier; unblob's squashfs handler has no
fallback path (its only extractor is the `sasquatch`/`sasquatch-v4be` command), consistent with the
`before` run publishing nothing from the squashfs chunk.

## 9. Exact commands (scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36ExecReproK3`)

```
bash tools/round-36/c1-run.sh after  "$S/carriers/nvim-linux-x86_64.appimage" "$S/out/after"  "$S/work/after.$$"    # exit 0
bash tools/round-36/c1-run.sh before "$S/carriers/nvim-linux-x86_64.appimage" "$S/out/before" "$S/work/before.$$"   # exit 0
bash tools/round-36/c1-run.sh oracle "$S/carriers/nvim-linux-x86_64.appimage" "$S/out/oracle" "$S/work/oracle.$$"   # exit 0
# id recompute: node $S/evid.mjs <4 receipts>   → 4/4 match=true, exit 0
# comparisons: python3 -I over normalized_result.files / extraction_gaps / oracle.tsv
/usr/bin/unsquashfs -no-progress -o 944632 -d "$S/ux/root" "$S/carriers/nvim-linux-x86_64.appimage"                 # exit 0
```

## 10. Limits and what I did not do

- Not run: `c1-counter.py`, `c1-counter.py --selftest`, any control (`CTL-C1-0/1/2`), K1/K2/K4, any
  PROVINCE/README/knowledge binding check — other seats own those; `carriers_matched` and
  `met_target` are **not** asserted here.
- Not re-tested: 7z fallback, BE/AVM images, loader behaviour, extracted programs' behaviour.
- No VCS mutation, no campaign tool in `/home/vgpnk/Projects/shokuknow`, no writes outside this
  report file. No subagents, no background jobs, no `agent://all` message.
- Receipt JSONs lived only in my scratch (paths under `/tmp`-equivalent scratch are not evidence);
  every number above is transcribed into this file. Scratch `$S` removed before finishing, including
  the downloaded carrier and all extraction trees.

## 11. Retained evidence (non-exhaustive, the falsifiable anchors)

- carrier sha256 `b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb`, 11454968 B.
- offset/superblock: `e_shoff=942712 e_shentsize=64 e_shnum=30 → 944632`, magic `hsqs`,
  `inodes=2247 block_size=131072 comp=6 v4.0 bytes_used=10507255`.
- oracle: 2130 rows, `diff -q` against committed `oracle.tsv` clean; entry census
  2130 regular / 2 symlink / 115 dirs = 2247 inodes.
- after: 2147 files, 51122564 published bytes, 2 gaps (both `unpublished-entry`, no dependencies),
  2130/2130 oracle matches, 17 enumerated non-oracle chunks, unblob exit 0, REA exit 0,
  set diff vs committed = 0/0.
- before: 2 files, 11454968 published bytes, 1 gap `missing-extractor-dependency`/`["sasquatch"]`/
  `squashfs_v4_le`/`$input`, 1 diagnostic, 0/2130 oracle matches, unblob exit 1, REA exit 0,
  set diff vs committed = 0/0.
- ids: 4/4 receipts recompute; 5 differing scalar paths per pair, all path metadata.
- sasquatch-only probe: identical 2147-file set, 2 `unpublished-entry` gaps, exit 0.
