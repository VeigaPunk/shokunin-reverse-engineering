# FINAL-MANIFEST — luna-round-7 six entries (BB1, integration seat)

Seat: BB1 (final manifest compiler, Lane B backfill). This file is the only artifact this seat writes; nothing is landed, no tracked file is touched, no probe or network call is made. The six entry texts below are complete and copy-paste-ready.

## CLAIM
Six frozen, correction-complete artifacts for the parent's landing: per entry — final hyphenated filename, complete file text (`source:`/`verified-at:`/`recheck:` on all six), 3-cell coverage-map row, 4-cell Knowledge-table row. RESULT-class only; no promotion claims.

## METHOD
Read ZB (manifest), GB6 (keep/drop), PB0 (rulings), QB1–QB6 (gates), E1D–E6D, G1–G6, Z1–Z6, M1/M2, K3/K4, `corpus/QUALITY.md:11-25`, `corpus/README.md:11-66`, `CORPUS.md:17-19`, and both leg-3–8 receipts. Command A verbatim (`SCORECARD.md:92-123`) at REV `411175e337c0725ae9bee3fd478ae9bf05bedf3f` → `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 72, "mapped": 72, "missing": [], "rule_blocks": 9}`. Self-check of this file: the six filenames and six map rows were extracted and re-run through the same set algebra against the HEAD corpus in memory → `mapped=78, knowledge_files=78, missing=[], dangling=[], coverage_score=10.0`. Evidence re-read for corrections: `.ufo/waves/luna-round-6/receipts/leg-3.md:3` (reproducer command), `receipts/leg-5.md:8` (canonical nine fuse names, `sentinel_offset 35260752`, `wire_version` 1, four limitations), `receipts-B/leg-7.md:22,60` (request carries only `pattern`; `limit 100 (default)`); `wc -l` shows every cited range endpoint ≤ file length (legs 3–8: 222/96, 43/71, 12/62, 25/60, 28/72, 25/78); the 26 searched blocks sum to 33,668 bytes.

## FINDINGS
Deltas applied per entry (all other text carried from the named source):
1. Z1.md:11-23 body unchanged; header prepended (source = Z1's Sources line; `recheck:` = E1D.md:19 replay, confirmed against `receipts/leg-3.md:3`).
2. QB2.md:10-19 carried verbatim; lane-A fallback and lane-B SC2 carrier stay distinct.
3. E3D.md:8 body + QB3.md:9-12 header; fuse names corrected to receipt canon (`LoadBrowserProcessSpecificV8Snapshot`, `GrantFileProtocolExtraPrivileges`); resource bounds and the four receipt limitations transcribed from `receipts/leg-5.md:8`; reproducer = `recheck:`; SC3 citation added.
4. G4.md:11-22 body + header; admitted sources B-only (`receipts-B/leg-6.md` + SC4); the comparator line no longer cites E4D's lane-A receipt.
5. Composed from E5D.md:2-13, G5.md:8-11, E5V.md:8-13, Z5.md:8-10; call shows only the `pattern` argument; `limit 100` recorded as the tool-reported default; SC5 citation added.
6. E6D.md:10-19 verbatim (already carries all three fields); rows are E6D's (hyphenated), not K4's underscore variant; SC6 citation line added (N1.md:5).

## THREATS
SC1–SC6/CB3 are untracked and cited only as auxiliary anchors; tracked receipts carry the admitted content. Entries 3 and 5 are composed here, so no gate verified those exact bytes before now — the deltas above are reviewable. No replay was performed: post-landing Command A 78/78, 72-file byte identity, and README row placement are parent-side measurements.

## VERDICT
FINDING: six entries compiled with rulings (a)–(d) applied; parent lands them, then re-measures Command A for the 78/78 claim.

---

## Entry 1 — `inspect_go_binary`

FINAL FILENAME: `corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md`

FINAL FILE TEXT:

```markdown
# inspect_go_binary — embedded Go build information

source: `.ufo/waves/luna-round-6/receipts/leg-3.md:3-8,17,71-108,118-166,169-181`; corroboration `.ufo/waves/luna-round-6/receipts-B/leg-3.md:8-21,29,41-42,84-86`; carrier `.ufo/waves/luna-round-6/SC1.md:10-18`
verified-at: 2026-10-16
recheck: `cd /tmp && npm_config_cache=/tmp/kaidoku-luna-round-6-npm-cache TMPDIR=/tmp npx -y rea-agents@6.5.0 mcp`; send MCP `tools/call` for `inspect_go_binary` with `{"path":"/usr/bin/docker"}`; expect Evidence `ev_671861638ed7fe544cce229c3d4a9258766337a5e72dcf79f107af713b596a4b` with complete module `github.com/docker/cli/cmd/docker`.

REA pin: `rea-agents@6.5.0`; captured MCP server version 6.5.0; provider `go-build-info` v1.

Artifact: `/usr/bin/docker` (ELF x86_64), SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9`.
Round-6 call: `inspect_go_binary` with `{"path":"/usr/bin/docker"}`; Evidence ID `ev_671861638ed7fe544cce229c3d4a9258766337a5e72dcf79f107af713b596a4b`.

- **Observation (captured description; other formats not exercised):** Lists local ELF, PE, and thin Mach-O images; says absent metadata is unknown and malformed, unsupported, or oversized inputs receive typed failures.
- **Observation (tested RESULT):** Reports inline build info, `go1.26.5-X:nodwarf5`, module `github.com/docker/cli/cmd/docker`, complete module text/no unparsed lines, and `GOOS=linux`, `GOARCH=amd64`, `CGO_ENABLED=1`.
- **Inference:** This one carrier demonstrates extraction of embedded Go build metadata, not general detection.
- **Unknown / limitations:** No missing-metadata or rejected input was tested. Metadata does not establish compiler identity, dependency authenticity, or runtime behavior; functions, source mappings, types, and decompilation are not recovered. Documented guards (256 MiB reads/searches each, 1 MiB aggregate strings, 16 MiB structural decoding, 8 MiB complete metadata) are not OS limits.

Sources: `.ufo/waves/luna-round-6/receipts/leg-3.md:3-8,17,71-108,118-166,169-181`; corroboration `.ufo/waves/luna-round-6/receipts-B/leg-3.md:8-21,29,41-42,84-86`; carrier `.ufo/waves/luna-round-6/SC1.md:10-18`.
```

MAP ROW (3-cell — coverage map, append after the `2026-10-14-r14-02-final-sweep` row, before `## Knowledge`):

```markdown
| `knowledge/2026-10-16-l7-01-inspect-go-binary` | Observed inline Go build metadata in `/usr/bin/docker` (SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9`): `go1.26.5-X:nodwarf5`, module `github.com/docker/cli/cmd/docker`; not runtime or compiler-authenticity evidence | REA 6.5.0 `inspect_go_binary`; round-6 `receipts/leg-3.md` + `receipts-B/leg-3.md` |
```

KNOWLEDGE ROW (4-cell — `## Knowledge` table):

```markdown
| `2026-10-16-l7-01-inspect-go-binary` | `inspect_go_binary`: Docker's inline build metadata parsed complete; metadata does not authenticate compiler identity or runtime behavior | rea-agents@6.5.0; `.ufo/waves/luna-round-6/receipts/leg-3.md:3-8,52-96`; `.ufo/waves/luna-round-6/receipts-B/leg-3.md:23-29,56-86`; `SC1.md:9-13` | 2026-10-16 |
```

Deltas: M1.md:11 and K3.md:8 tokens hyphenated; header added.

---

## Entry 2 — `inspect_rust_binary`

FINAL FILENAME: `corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md`

FINAL FILE TEXT:

```markdown
# REA 6.5.0 `inspect_rust_binary` — typed RESULT on two distinct carriers

source: `.ufo/waves/luna-round-6/receipts-B/leg-4.md:8-24,45-53,66-71`; `.ufo/waves/luna-round-6/receipts/leg-4.md:5-22,27-28,39,43`
verified-at: 2026-10-16
recheck: Under `npx -y rea-agents@6.5.0 --mcp`, call `inspect_rust_binary` on the two pinned paths below; record Evidence IDs, `auditable_metadata`, `rustc_commit`, limitations.

- **Observation (lane B; SC2-designated carrier):** `/usr/bin/rg`, SHA-256 `d006acfe51619144af4709e85945fe3b5a6f05038d356c4d8f752a33b4ecae42` (SC2 candidate, `.ufo/waves/luna-round-6/SC2.md:8-12`): `{"path":"/usr/bin/rg"}` returned Evidence `ev_9ea97685bf6313d1e1816a43ba644a25d68459d9ec37f06dfc1b39934eb1bff2` from provider `rust-auditable` v1 — RESULT, exit 0; elf/amd64/64-bit/little-endian; `auditable_metadata` null; `rustc_commit` null.
- **Observation (lane A; separate fallback artifact):** `/usr/lib/signal-desktop/resources/app.asar.unpacked/node_modules/@signalapp/libsignal-client/prebuilds/linux-x64/@signalapp+libsignal-client.node`, SHA-256 `1b44ed531f404f5358ee0618a423560463819534a38db5176bb1064b9d14d1f7` (24,944,200 B): Evidence `ev_0618e7a50e32ff9556490beeff7e0debc5d6aecf3deedb92b0d4953c747c99d3`; same provider/class/exit; `auditable_metadata` null; `rustc_commit` `{evidence_kind:"inferred", hash da80ed0708a09dc096c184345d6eb42cbcd50a1e, file_offset 2287779}`. Lane A recorded a fallback because SC2 attribution was unavailable (`receipts/leg-4.md:15,43`) — this carrier is not SC2's. The two artifacts share only the RESULT class; no same-target corroboration is claimed.
- **Inference:** Each call returned a typed metadata record; the operation inspects only `.dep-v0` and read-only compiler-path strings, not functions, types, or runtime behavior. Nulls are not evidence of missing dependencies or compilers; embedded metadata authenticates no package, source, or compiler. Scope: these two calls only; no Core promotion.
- **Unknown / limitations (tool-reported):** "No `.dep-v0` section was found. Absence of `.dep-v0` does not mean the binary has no dependencies." `/usr/bin/rg`'s rustc commit is unknown ("No `/rustc/<40-hex>/` path was found in read-only data"); the `.node` hash is inferred from such a path. `/usr/bin/rg`'s Rust provenance rests on SC2's path identification, not tool output (`SC2.md:14-15`). Untested: non-ELF inputs, missing-metadata/rejected-input behavior, other REA versions. Guards — 256 MiB file, 1 MiB section, min(8 MiB, 64× section) inflated JSON, 8 MiB report — are tool bounds, not OS limits.
```

MAP ROW (3-cell):

```markdown
| `knowledge/2026-10-16-l7-02-inspect-rust-binary` | RESULT on SC2 `/usr/bin/rg` (SHA-256 `d006acfe51619144af4709e85945fe3b5a6f05038d356c4d8f752a33b4ecae42`): `.dep-v0`/rustc commit unknown, not evidence of no dependencies; lane-A fallback `/usr/lib/signal-desktop/resources/app.asar.unpacked/node_modules/@signalapp/libsignal-client/prebuilds/linux-x64/@signalapp+libsignal-client.node` (SHA-256 `1b44ed531f404f5358ee0618a423560463819534a38db5176bb1064b9d14d1f7`) had no `.dep-v0` and only an inferred rustc hash | REA 6.5.0 `inspect_rust_binary`; round-6 `receipts/leg-4.md` + `receipts-B/leg-4.md` |
```

KNOWLEDGE ROW (4-cell):

```markdown
| `2026-10-16-l7-02-inspect-rust-binary` | `inspect_rust_binary`: no `.dep-v0` found in libsignal `.node` or `rg`; `rg` has no `/rustc/<40-hex>/` marker; absence does not prove no dependencies | rea-agents@6.5.0; `.ufo/waves/luna-round-6/receipts/leg-4.md:7-22,28-43`; `.ufo/waves/luna-round-6/receipts-B/leg-4.md:13-18,37-71`; `SC2.md:8-12` | 2026-10-16 |
```

Deltas: M1.md:12 and K3.md:9 tokens hyphenated; QB2 text carried verbatim.

---

## Entry 3 — `inspect_electron_fuses`

FINAL FILENAME: `corpus/knowledge/2026-10-16-l7-03-inspect-electron-fuses.md`

FINAL FILE TEXT:

```markdown
# inspect_electron_fuses — nine-fuse sentinel on a pinned Signal ELF

source: `.ufo/waves/luna-round-6/receipts/leg-5.md:3-12`; `.ufo/waves/luna-round-6/receipts-B/leg-5.md:8-10,24-52`
verified-at: 2026-10-16
recheck: `cd /tmp && timeout 240 npx -y rea-agents@6.5.0 inspect-electron-fuses /usr/lib/signal-desktop/signal-desktop --format json`; expect evidence `ev_36045c43ecbed14e3eb3b77a720c24c115cc2377737d2ed2fe8acce76a4288ed`, carrier `f7a9b441e825b388260430f9edd9a2f94fd50be497bf66192a16aeab87afc85a`, one complete v1 sentinel at offset 35,260,752, nine fuse states.

REA pin: `rea-agents@6.5.0`; provider `electron-fuses` v1; confidence `observed`; RESULT, exit 0.

Carrier: `/usr/lib/signal-desktop/signal-desktop`, SHA-256 `f7a9b441e825b388260430f9edd9a2f94fd50be497bf66192a16aeab87afc85a` (223,513,856 bytes, ELF x86-64).
Round-6 call: `cd /tmp && timeout 240 npx -y rea-agents@6.5.0 inspect-electron-fuses /usr/lib/signal-desktop/signal-desktop --format json`; Evidence ID `ev_36045c43ecbed14e3eb3b77a720c24c115cc2377737d2ed2fe8acce76a4288ed`.

- **Observation:** One slice (223,513,856 bytes) contains one complete v1 sentinel at offset 35,260,752 (`wire_version` 1, `declared_length` 9) reporting: RunAsNode=disabled (48), EnableCookieEncryption=enabled (49), EnableNodeOptionsEnvironmentVariable=disabled (48), EnableNodeCliInspectArguments=disabled (48), EnableEmbeddedAsarIntegrityValidation=disabled (48), OnlyLoadAppFromAsar=enabled (49), LoadBrowserProcessSpecificV8Snapshot=disabled (48), GrantFileProtocolExtraPrivileges=enabled (49), WasmTrapHandlers=enabled (49) — raw_byte values in parentheses (`receipts/leg-5.md:8`).
- **Observation (lane B):** An independent run reported the same carrier digest, Evidence ID, and nine-state fingerprint (`receipts-B/leg-5.md:8,48-52`).
- **Inference (REA-derived, not runtime-observed):** The result's derived implications are that Node CLI inspect and RunAsNode are not honored, embedded ASAR integrity validation is unknown, and app loading is restricted to the app ASAR (`receipts/leg-5.md:8`).
- **Unknown / limitations (tool-reported):** "Fuse state does not prove the application enables Inspector through other means, such as app.commandLine or a remote-debugging switch in application code." "A missing sentinel means fuse state is unknown, not that every fuse is disabled." "Electron compiles embedded ASAR integrity validation only on macOS and Windows; the observed fuse byte at file offset 35260752 does not establish enforcement." "The selected file is admitted as one regular file of at most 1 GiB. Sentinel search uses 262144-byte windows, and each slice keeps at most 32 sentinels." One Linux carrier/slice only; RESULT-class exercise, no Core promotion.

Sources: `.ufo/waves/luna-round-6/receipts/leg-5.md:3-12`; `.ufo/waves/luna-round-6/receipts-B/leg-5.md:8,48-52`; carrier `.ufo/waves/luna-round-6/SC3.md:10`.
```

MAP ROW (3-cell):

```markdown
| `knowledge/2026-10-16-l7-03-inspect-electron-fuses` | Observed one complete nine-fuse sentinel at offset 35,260,752 in `/usr/lib/signal-desktop/signal-desktop` (SHA-256 `f7a9b441e825b388260430f9edd9a2f94fd50be497bf66192a16aeab87afc85a`); static fuse state does not establish runtime behavior or ASAR-integrity enforcement | REA 6.5.0 `inspect-electron-fuses`; round-6 `receipts/leg-5.md` + `receipts-B/leg-5.md` |
```

KNOWLEDGE ROW (4-cell):

```markdown
| `2026-10-16-l7-03-inspect-electron-fuses` | `inspect_electron_fuses`: Signal's nine fuse states parsed complete; static states do not prove runtime behavior and ASAR-integrity enforcement remains unknown | rea-agents@6.5.0; `.ufo/waves/luna-round-6/receipts/leg-5.md:3-12`; `.ufo/waves/luna-round-6/receipts-B/leg-5.md:8-10,22-52`; `SC3.md:9-12` | 2026-10-16 |
```

Deltas: M1.md:13 and K3.md:10 tokens hyphenated; header added; fuse names taken from receipt canon; SC3 citation added for N1.md:5's census requirement.

---

## Entry 4 — `inspect_sqlite_database`

FINAL FILENAME: `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md`

FINAL FILE TEXT:

```markdown
# inspect_sqlite_database — offline SQLite schema inventory

source: `.ufo/waves/luna-round-6/receipts-B/leg-6.md:10,20,23-28,34-35,50-55`; `.ufo/waves/luna-round-6/SC4.md:8-21`
verified-at: 2026-10-16
recheck: Copy the hash-pinned pnpm v11 index (SHA-256 `3701a7e3465525c57e14106987c66bed10b4938ec190c2692beb6e434eaf9728`) to an absolute path and call `inspect_sqlite_database({"path":...})` under `rea-agents@6.5.0`; expect Evidence `ev_7572e622b7b3c5c281d3eae0d48282690c6f0b78ab8aae5a550bda07f93d6f9a` with the complete `package_index` inventory and `rows:null`.

REA: `rea-agents@6.5.0`; provider `sqlite` (REA SQLite database inspector), SQLite 3.54.0.

Carrier: `/tmp/bb6-leg-6/sc4-index.db`, SHA-256 `3701a7e3465525c57e14106987c66bed10b4938ec190c2692beb6e434eaf9728`; byte-identical to `/home/vgpnk/.local/share/pnpm/package-manager-store/v11/index.db` (SC4 source). Call: `inspect_sqlite_database({"path":"/tmp/bb6-leg-6/sc4-index.db"})`; Evidence ID `ev_7572e622b7b3c5c281d3eae0d48282690c6f0b78ab8aae5a550bda07f93d6f9a`.

- Observation: This path-only call returned RESULT with `wal:null`, a complete `inventory` schema containing one `package_index` table (`column_count:2`; column details not requested), no indexes/views/triggers, and `rows:null`.
- Inference: On this pinned offline copy, the default call inventories schema without returning rows; one carrier does not establish general behavior.
- Unknown: This run did not request table columns or rows, and does not establish behavior for changing databases, WAL inputs, encrypted/corrupt files, or other schemas.
- Limitations: The provider describes stable-file inspection, not an atomic snapshot; deleted or uncommitted records, invalid WAL tails, encryption, forensic recovery, and full integrity verification are outside scope. Views/triggers are not executed; virtual-table column expansion is unsupported.

Sources: `.ufo/waves/luna-round-6/receipts-B/leg-6.md:10,20,23-28,34-35,50-55`; `.ufo/waves/luna-round-6/SC4.md:8-21`. Excluded comparator: lane A's separate synthetic-fixture run is not admitted (`corpus/QUALITY.md:22`; self-made fixture per `CB3.md:12`).
```

MAP ROW (3-cell):

```markdown
| `knowledge/2026-10-16-l7-04-inspect-sqlite-database` | Path-only `inspect_sqlite_database` inventory of a hash-pinned offline copy of the pnpm v11 index: complete `package_index` schema, columns not requested, `rows:null`; lane-A synthetic fixture excluded | REA 6.5.0; `.ufo/waves/luna-round-6/receipts-B/leg-6.md` + `.ufo/waves/luna-round-6/SC4.md:8-21` |
```

KNOWLEDGE ROW (4-cell):

```markdown
| `2026-10-16-l7-04-inspect-sqlite-database` | 6.5.0 SQLite path-only inventory of a pinned offline pnpm-index copy: `package_index` schema, columns not requested, no rows returned; offline and bounded, not forensic | `.ufo/waves/luna-round-6/receipts-B/leg-6.md`; `.ufo/waves/luna-round-6/SC4.md:8-21` | 2026-10-16 |
```

Deltas: M2.md:10/K4.md:10 rows rebuilt B-only (E4D's lane-A receipt dropped); header added.

---

## Entry 5 — `search_bytes`

FINAL FILENAME: `corpus/knowledge/2026-10-16-l7-05-search-bytes.md`

FINAL FILE TEXT:

```markdown
# search_bytes — one ELF-magic hit in loader-adjusted memory

source: `.ufo/waves/luna-round-6/receipts/leg-7.md:3-14,19-21`; `.ufo/waves/luna-round-6/receipts-B/leg-7.md:18-27,56-72`; carrier `.ufo/waves/luna-round-6/SC5.md:9`
verified-at: 2026-10-16
recheck: `cd /tmp && npx -y rea-agents@6.5.0 --mcp`, then `open_binary({"path":"/bin/true"})` and `search_bytes({"pattern":"7f 45 4c 46"})`; expect Evidence `ev_4b0badc6b166fb6e6196ec561521d48873af50c2f41329deca72ccc685eab903`: exactly one hit at address `0x100000` / `file_offset:0`, 33,668 bytes searched over loader-adjusted blocks, `complete:true`, `next_cursor:null`.

REA pin: `rea-agents@6.5.0`; provider Ghidra 12.1.4, default auto-analysis (`receipts/leg-7.md:3-13`).

Carrier: `/bin/true`, resolved to `/usr/bin/true` (ELF x86-64, 43,320 bytes), SHA-256 `8bc9a73afd7d85061160857536e093ded799dae7a2f0cf5758c4553f2f83002d`.
Round-6 call: `search_bytes` with `{"pattern":"7f 45 4c 46"}` (after `open_binary`); Evidence ID `ev_4b0badc6b166fb6e6196ec561521d48873af50c2f41329deca72ccc685eab903`.

- **Observation:** The call returned exactly one match — address `0x100000`, segment `segment_2.1`, `file_offset:0`, `procedure:null` — with 33,668 bytes searched across 26 initialized loader-adjusted blocks, `complete:true`, `next_cursor:null`. The response records the query's limit as `100`, the tool default (`receipts-B/leg-7.md:60`).
- **Observation (lane B):** An independent replay returned byte-identical stdout, SHA-256 `3492d27d66e086d683935f396ea05fce4cbddc660874052a955c9133866629a8`, agreeing on hit, offset, byte count, and completion (`receipts-B/leg-7.md:64-72`).
- **Inference:** The hit is the ELF magic at file offset 0. This one pinned query demonstrates that search; it does not establish general pattern, target, or raw-file coverage.
- **Unknown / limitations:** `complete:true` covers the reported eligible blocks only; the receipt lists uninitialized and not-loaded blocks separately and states patterns never cross block boundaries (`receipts/leg-7.md:21`) — it is not proof that all 43,320 carrier bytes were searched. No-hit, multi-hit, paging/cursor, cancellation, and other-pattern behavior were not exercised. This static search is not runtime-behavior evidence; RESULT-class exercise only, no Core promotion.

Sources: `.ufo/waves/luna-round-6/receipts/leg-7.md:3-14,19-21`; `.ufo/waves/luna-round-6/receipts-B/leg-7.md:18-27,56-72`; carrier `.ufo/waves/luna-round-6/SC5.md:9`.
```

MAP ROW (3-cell):

```markdown
| `knowledge/2026-10-16-l7-05-search-bytes` | ELF magic hit at file offset 0; loaded-block scope | REA 6.5.0 / Ghidra 12.1.4 |
```

KNOWLEDGE ROW (4-cell):

```markdown
| `2026-10-16-l7-05-search-bytes` | 6.5.0 loader-adjusted byte search; ELF magic hit at `0x100000` / file offset 0, with block-scope limits | `.ufo/waves/luna-round-6/receipts/leg-7.md` + `receipts-B/leg-7.md` | 2026-10-16 |
```

Deltas: K4.md:11 token hyphenated; header added; call shows only the `pattern` argument; SC5 citation added for N1.md:5's census requirement.

---

## Entry 6 — `inspect_with_objdump`

FINAL FILENAME: `corpus/knowledge/2026-10-16-l7-06-inspect-with-objdump.md`

FINAL FILE TEXT:

```markdown
# REA 6.5.0 `inspect_with_objdump`: `file_headers` only

source: `.ufo/waves/luna-round-6/receipts/leg-8.md:3-14`; `.ufo/waves/luna-round-6/receipts-B/leg-8.md:41-55,67-76`
verified-at: 2026-10-16
recheck: Repeat `inspect_with_objdump` with the pinned path, SHA-256, `operation=file_headers`, and `follow_debug_links=false`; record Evidence metadata and complete provider output.

- Observation — On `/usr/bin/jq` (SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`), REA 6.5.0 call `inspect_with_objdump({path:"/usr/bin/jq", operation:"file_headers", follow_debug_links:false})` against this SHA returned Evidence `ev_aa75cc2e36b149a82b41e763b92697efc1e2c432571d14c003e3a7bff0219c2f`; provider `gnu.objdump`, argv `objdump -f /usr/bin/jq`, exit 0, complete/untruncated output. It reports `elf64-x86-64`, architecture `i386:x86-64`, flags `HAS_SYMS, DYNAMIC, D_PAGED`, start `0x3cf0`. Lane B's same-carrier compare reproduced the Evidence ID and raw provider stdout. (`.ufo/waves/luna-round-6/receipts/leg-8.md:8-14,19`; `.ufo/waves/luna-round-6/receipts-B/leg-8.md:41-55`.)
- Observation — Lane B also got RESULT on `/home/vgpnk/.local/bin/jq` (SHA-256 `b1c22172dd303f3be49e935aa56aa48a8b7a46e0bc838b4997d3bb451495870f`), a distinct carrier and Evidence ID (`.ufo/waves/luna-round-6/receipts-B/leg-8.md:6-8,16-35`); this is not same-output evidence.
- Inference — The exact `file_headers` request completed on these two pinned jq ELF inputs; this does not establish general format support or classification accuracy.
- Unknown — REA format/architecture metadata are `unknown`/`null`; provider version is `null`; supported formats and behavior of other operations, including disassembly, remain unestablished. `artifact_changed=false` does not prove the exact bytes consumed.

Sources: `.ufo/waves/luna-round-6/receipts/leg-8.md:3-14,19`; `.ufo/waves/luna-round-6/receipts-B/leg-8.md:6-8,16-35,41-55,67-76`; carrier `.ufo/waves/luna-round-6/SC6.md:8`.
```

MAP ROW (3-cell):

```markdown
| `knowledge/2026-10-16-l7-06-inspect-with-objdump` | `file_headers` returned complete headers for two pinned jq ELF inputs; other operations untested | REA 6.5.0; .ufo/waves/luna-round-6/receipts/leg-8.md + .ufo/waves/luna-round-6/receipts-B/leg-8.md |
```

KNOWLEDGE ROW (4-cell):

```markdown
| `2026-10-16-l7-06-inspect-with-objdump` | `inspect_with_objdump` — `file_headers` only; two pinned jq ELF inputs returned RESULT, broader behavior unknown | REA 6.5.0; .ufo/waves/luna-round-6/receipts/leg-8.md + .ufo/waves/luna-round-6/receipts-B/leg-8.md | 2026-10-16 |
```

Deltas: K4.md:12 underscore variant not used; E6D's rows carried (hyphenated already); body verbatim plus the SC6 citation line N1.md:5's census requires.
