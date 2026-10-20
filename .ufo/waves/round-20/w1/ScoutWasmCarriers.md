# ScoutWasmCarriers-2 — WASM carriers on this host (round 20, w1)

Read-only scout. Report written 2026-10-20T17:50:33-03:00 (clock at write time). No installs/upgrades
were made or needed. No lane file other than this report was written; scratch lived under
`/tmp/kr20-ScoutWasmCarriers-2.*` and was removed after writing.

Scope = exactly `find /usr/lib /opt /home/vgpnk/.npm/_npx -xdev -name '*.wasm' -size +1k`.
Labels: **[O]** observed from command output/bytes; **[I]** inference; **[U]** unknown.

## Verdict

1. **13 carrier files, 6 distinct contents, 3 owner families** — [O]: `chatgpt-bin 26.1013.40934-1`
   (4 files), `zcode 3.16.2-1` (3 files), npm npx caches for `rea-agents@6.5.0` and `@6.7.0` (6 files).
2. **Same-module version pairs (same filename/package, different version AND different sha256): zero** — [O].
   Every repeated filename is byte-identical; the only in-scope version pair (`rea-agents` 6.5.0 vs 6.7.0)
   ships identical `evmole 0.9.3` / `@zip.js/zip.js 2.15.0` files with identical lockfile integrity.
3. **The size and exit-code filters are inert/noise here** — [O]: no `.wasm` ≤ 1024 B exists under the three
   roots, and `find`'s exit 1 comes from two permission-denied directories (sudo recheck: 0 matches).

## Inventory (13 files)

| # | path | bytes | sha256 | owner |
|---|---|---|---|---|
| 1 | `/usr/lib/chatgpt/resources/cua_node/lib/node_modules/@oai/browser-desktop/scripts/zxing_reader.wasm` | 1065866 | `0e8d688d71932ebb6b8b33f700d43d3cb997f59ed9cab3c05102d7f10288a392` | pacman `chatgpt-bin 26.1013.40934-1`; npm `@oai/browser-desktop 0.1.1` |
| 2 | `/usr/lib/chatgpt/resources/cua_node/lib/node_modules/@oai/cua/dist/lib/js/oai_js_browser/dist/skill/scripts/zxing_reader.wasm` | 1065866 | `0e8d688d71932ebb6b8b33f700d43d3cb997f59ed9cab3c05102d7f10288a392` | pacman `chatgpt-bin 26.1013.40934-1`; npm `@oai/cua 0.2.6` |
| 3 | `/usr/lib/chatgpt/resources/plugins/openai-bundled/plugins/browser/scripts/zxing_reader.wasm` | 1065866 | `0e8d688d71932ebb6b8b33f700d43d3cb997f59ed9cab3c05102d7f10288a392` | pacman `chatgpt-bin 26.1013.40934-1`; plugin `browser 26.1013.40934` (no npm ancestor) |
| 4 | `/usr/lib/chatgpt/resources/plugins/openai-bundled/plugins/chrome/scripts/zxing_reader.wasm` | 1065866 | `0e8d688d71932ebb6b8b33f700d43d3cb997f59ed9cab3c05102d7f10288a392` | pacman `chatgpt-bin 26.1013.40934-1`; plugin `chrome 26.1013.40934` (no npm ancestor) |
| 5 | `/opt/ZCode/resources/glm/packages/pdf-plugin/dist/ui/pdfjs/wasm/openjpeg.wasm` | 250009 | `67b8e2b162da472e98cb48d3d32e3e38fff481b9b32ff4818e78bb248af88ab2` | pacman `zcode 3.16.2-1`; npm `@zcode/pdf-plugin 0.2.1` |
| 6 | `/opt/ZCode/resources/glm/packages/pdf-plugin/dist/ui/pdfjs/wasm/qcms_bg.wasm` | 94519 | `6017eca5939cde1836e88e6d8cd27ae039246f206515ea4487bdfd0e3fb16e26` | pacman `zcode 3.16.2-1`; npm `@zcode/pdf-plugin 0.2.1` |
| 7 | `/opt/ZCode/resources/glm/packages/spreadsheets-plugin/dist/ui/sheets.wasm` | 4345449 | `ab475856ab69ce1c29866d8961952578c488804bc4ca6bc13a6db13eb09e20de` | pacman `zcode 3.16.2-1`; npm `@zcode/spreadsheets-plugin 0.2.0` |
| 8 | `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/@zip.js/zip.js/lib/core/streams/zlib-wasm/zlib-streams.wasm` | 55126 | `1ebaf6e62f247a005189493097f460bc9050f248755c55ecba34fd54257a6bb2` | npx `rea-agents@6.5.0`; npm `@zip.js/zip.js 2.15.0` (pacman: none) |
| 9 | `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/@zip.js/zip.js/dist/zip-module.wasm` | 55126 | `1ebaf6e62f247a005189493097f460bc9050f248755c55ecba34fd54257a6bb2` | npx `rea-agents@6.5.0`; npm `@zip.js/zip.js 2.15.0` (pacman: none) |
| 10 | `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/evmole/dist/evmole_bg.wasm` | 480805 | `542b24e22eab36910fe2e797b329ab24b5423c0577fa85e49a97d9edf068b884` | npx `rea-agents@6.5.0`; npm `evmole 0.9.3` (pacman: none) |
| 11 | `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/@zip.js/zip.js/lib/core/streams/zlib-wasm/zlib-streams.wasm` | 55126 | `1ebaf6e62f247a005189493097f460bc9050f248755c55ecba34fd54257a6bb2` | npx `rea-agents@6.7.0`; npm `@zip.js/zip.js 2.15.0` (pacman: none) |
| 12 | `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/@zip.js/zip.js/dist/zip-module.wasm` | 55126 | `1ebaf6e62f247a005189493097f460bc9050f248755c55ecba34fd54257a6bb2` | npx `rea-agents@6.7.0`; npm `@zip.js/zip.js 2.15.0` (pacman: none) |
| 13 | `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/evmole/dist/evmole_bg.wasm` | 480805 | `542b24e22eab36910fe2e797b329ab24b5423c0577fa85e49a97d9edf068b884` | npx `rea-agents@6.7.0`; npm `evmole 0.9.3` (pacman: none) |

Identity anchors: npx requests `rea-agents@6.5.0` `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/package.json:7`
and `rea-agents@6.7.0` `/home/vgpnk/.npm/_npx/a1722018f28f9df2/package.json:7`; `evmole 0.9.3`
(`.../evmole/package.json:2,4` in both caches); `@zip.js/zip.js 2.15.0`
(`.../@zip.js/zip.js/package.json:2,6` in both); `@oai/browser-desktop 0.1.1`
(`/usr/lib/chatgpt/resources/cua_node/lib/node_modules/@oai/browser-desktop/package.json:2-3`);
`@oai/cua 0.2.6` (`.../@oai/cua/package.json:2-3`); `@zcode/pdf-plugin 0.2.1`
(`/opt/ZCode/resources/glm/packages/pdf-plugin/package.json:3-4`); `@zcode/spreadsheets-plugin 0.2.0`
(`.../spreadsheets-plugin/package.json:3-4`); plugins `browser`/`chrome` version `26.1013.40934`
(`.../plugins/browser/.codex-plugin/plugin.json:2-3`, `.../plugins/chrome/.codex-plugin/plugin.json:2,55`);
pacman versions `/var/lib/pacman/local/chatgpt-bin-26.1013.40934-1/desc:2,5` and
`/var/lib/pacman/local/zcode-3.16.2-1/desc:2,5`.

## Same-module version pairs — negative result with the tested legs

| basename | copies | package@version(s) | distinct sha256 | version pair? |
|---|---|---|---|---|
| `zxing_reader.wasm` | 4 (#1-4) | `@oai/browser-desktop 0.1.1`, `@oai/cua 0.2.6`, plugins `browser`/`chrome 26.1013.40934` | **1** | no — same bytes, 4 independent copies (distinct inodes, link count 1) |
| `evmole_bg.wasm` | 2 (#10, #13) | `evmole 0.9.3` under `rea-agents@6.5.0` / `@6.7.0` | **1** | no — outer package versions differ, wasm dep does not |
| `zip-module.wasm` | 2 (#9, #12) | `@zip.js/zip.js 2.15.0` under both rea-agents caches | **1** | no |
| `zlib-streams.wasm` | 2 (#8, #11) | `@zip.js/zip.js 2.15.0` under both caches | **1** | no; also byte-identical to `zip-module.wasm` inside the same package (two names, one build output) |
| `openjpeg.wasm`, `qcms_bg.wasm`, `sheets.wasm` | 1 each | — | 1 each | n/a |

Evidence for the one candidate pair: both lockfiles pin the same dependency versions and the same tarball
integrity — `@zip.js/zip.js 2.15.0` `sha512-hYAuHAaWjt0axbofaDL5XUlmrQPsBDcK3f45ApZuh6N+8UGVk26GoGdtGDvcvzahsHytTQ6DtBVXwG9IcCMjjQ==`
(`ad9a…/package-lock.json:313-317` = `a172…/package-lock.json:313-317`), `evmole 0.9.3`
`sha512-UhO5HMAoEPCupSxvBJPlm/L0Qk/KVJ/OJo3r4EyhXADIEHqU5aTkAzsBfzk4lXGjqxVnaYbh1GPSmZtmSHFnQQ==`
(both `:814-818`), while `rea-agents` itself differs: `6.5.0` at `ad9a…/package-lock.json:1589-1593` vs
`6.7.0` at `a172…/package-lock.json:1607-1611`. An in-scope census of all `package.json` files reported
exactly one version per wasm-owning package name above — [O], so no divergent module version exists in
scope to pair. (The two extra npx caches `52027bd8fc0022aa` = `node@22`, `ce601f5be3f19082` = `c8` contain
0 wasm files.)

## Module identity of the 6 distinct contents

| module (sha prefix) | bytes | funcs | imports | exports | producers section | toolchain markers |
|---|---|---|---|---|---|---|
| `zxing_reader` (`0e8d…`) | 1065866 | 1319 | 77 | 21 | none | `/emsdk/emscripten/system/lib/libcxxabi/...` strings → Emscripten build [O marker]; library identity from filename [I] |
| `openjpeg` (`67b8…`) | 250009 | 202 | 17 | 6 | none | `/tmp/openjpeg/src/bin/common/color.c`, `opj_*` error strings → OpenJPEG [O]; build toolchain [U] (no producers/emsdk marker) |
| `qcms_bg` (`6017…`) | 94519 | 138 | 5 | 23 | `language=Rust`; `rustc 1.87.0 (17067e9ac 2025-05-09)`, `walrus 0.23.3`, `wasm-bindgen 0.2.100` [O] | `/rustc/17067e9ac…/…` [O] |
| `sheets` (`ab47…`) | 4345449 | 4918 | 74 | 153 | `language=Rust`; `rustc 1.97.0 (2d8144b78 2026-07-07)`, `walrus 0.24.4`, `wasm-bindgen 0.2.108` [O] | imports `./duke_sheets_wasm_bg.js` [O] |
| `zip-module`/`zlib-streams` (`1ebaf…`) | 55126 | 77 | 0 | 32 | none | exports `inflate9_*`, `deflate_new`; no imports (self-contained) [O]; zlib port [I] |
| `evmole_bg` (`542b…`) | 480805 | 450 | 30 | 21 | `walrus 0.26.4`, `wasm-bindgen 0.2.126 (21ac804a9)`; no `language` field [O] | `/rustc/8bab26f4…/…` → Rust [O] |

`target_features` custom sections exist only for `qcms_bg` and `sheets`, both exactly
`+mutable-globals +nontrapping-fptoint +bulk-memory +sign-ext +reference-types +multivalue` [O].
All six unique modules carry the Wasm 1.0 header `00 61 73 6d 01 00 00 00` and pass WABT 1.0.42
`wasm-validate` (6/6 exit 0) [O].

## Calibration and coverage

- [O] `find` returns **exit 1** with exactly 2 stderr lines: `/usr/lib/chromium/extensions` and
  `/opt/containerd` (`Permission denied`, os error 13). `sudo -n find` on those two trees: exit 0, 0 wasm.
  The inventory is not truncated by the exit code.
- [O] `-size +1k` excludes nothing: a `-size -1025c` pass returned 0 rows, and an unfiltered pass returned
  the same 13 files. `-iname` also returns 13 (no non-lowercase extension).
- [O] `-xdev` semantics: `/opt` and `/usr/lib` are on `/dev/mapper/root[/@]`; `/home` is a separate btrfs
  subvolume, so the third root was walked on its own — it is explicitly in the command, so nothing is lost.
- [O] Supplementary host-boundary count (not part of the assigned inventory): 7 wasm > 1 KiB on `/`,
  60 on `/home` (6 of them are the in-scope npx files) → 67 on the scanned filesystems; the three assigned
  roots cover 13/67 ≈ 19%. Not scanned (separate mounts): `/tmp` (xfs), `/fast` (xfs), `/boot` (vfat),
  `/var/cache/pacman/pkg`, `/var/log`.
- [O] In the 54 out-of-scope `/home` files, basename grouping finds 3 differing-sha groups, **none a
  same-module version pair**: `draco_decoder.wasm` (gltf vs core build of one three.js tree),
  `onig.wasm` (chromium extension `5.5.3.17_0` vs `5.5.3.18_0` — identical sha — plus a different
  `shiki 2.5.0` copy), `tree-sitter.wasm` (3 copies inside one `web-tree-sitter 0.25.10`: lib and debug
  identical, root copy differs). Package-version provenance for those was not audited [U].

## Commands and exit codes (all run on this host, 2026-10-20)

| command (abridged) | exit | result |
|---|---|---|
| `find /usr/lib /opt /home/vgpnk/.npm/_npx -xdev -name '*.wasm' -size +1k -printf '%s\t%p\n' 2>/dev/null` | 1 | 13 rows; exit from 2 permission-denied dirs |
| same, stderr redirected to `/dev/null` and counted | – | 2 stderr lines |
| `sudo -n find /usr/lib/chromium/extensions /opt/containerd -xdev -name '*.wasm' -size +1k -printf …` | 0 | 0 rows |
| `find … -size -1025c -printf '%s\t%p\n' 2>/dev/null` | 1 | 0 rows (same permission dirs) |
| `find … -iname '*.wasm' -size +1k \| wc -l` | 0 | 13 |
| `find … -name '*.wasm' -size +1k -print0 \| xargs -0 sha256sum` | 0 | 13 lines, 6 unique sha256 |
| python3 re-verification (size+sha256+mode per file) | 0 | matches sha256sum; modes 0644 except 4 zip files 0755 |
| per-file `pacman -Qo <path>` loop | 0 | 7 owned (`chatgpt-bin`, `zcode`), 6 `No package owns` (npx) |
| python3 nearest-`package.json` ancestor walk | 0 | 13 resolved; 2 plugin copies have none |
| python3 in-scope package census (all `package.json`) | 0 | 8 identities, one version per name |
| `wasm-validate` on 6 unique modules | 0 ×6 | all valid |
| `wasm-objdump -x` on 6 unique modules (scratch dumps) | 0 ×6 | section/import/export tables |
| python3 producers/target_features parser (stdlib) | 0 | values in table above |
| `strings -a -n 6` marker pass on 4 modules | 0 ×4 | emsdk / rustc / openjpeg markers |
| `stat -c '%i %h %s %n'` on zxing copies + evmole/zip | 0 | distinct inodes, link count 1 |
| `findmnt -rno TARGET,FSTYPE` | 0 | mount boundary list above |
| supplementary `find / -xdev` and `find /home -xdev` (>1 KiB) | 1 / 0 | 7 rows / 60 rows |

WABT used read-only from the contract path `/home/vgpnk/.local/opt/wabt-1.0.42/bin` (`wasm-validate`,
`wasm-objdump`); they are not on `PATH` (`command -v` exit 1) — no install performed.

## Remaining unknowns

- [U] Which runtime loads each module (import graph in the owning JS bundles) was not traced — outside this
  inventory question.
- [U] `openjpeg.wasm` build toolchain (no producers; no emsdk/emscripten string hit).
- [U] Package/version provenance of the 54 out-of-scope `/home` carriers, and any wasm on the unscanned
  mounts (`/tmp`, `/fast`, `/boot`).
- [U] Whether the intra-package duplicate (`zip-module.wasm` ≡ `zlib-streams.wasm`) is an intentional
  build output or a packaging artifact.
