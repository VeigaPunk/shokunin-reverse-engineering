<!-- corpus entry — kaidoku-shokunin arc2-loop1-round6 (2026-10-18). Staging: .ufo/waves/arc2-loop1-round6/E9.md, E10.md, E11.md. This is the 17.7MB mid-rung, not the 91.6MB Godot leg. -->

# 17.7MB PE mid-rung — agent-browser x86-64 held (11 segments / 19012 procedures)

source: `.ufo/waves/arc2-loop1-round6/E9.md:42-66`; independent parse `.ufo/waves/arc2-loop1-round6/E10.md`; census extract `.ufo/waves/arc2-loop1-round6/E11.md`
verified-at: 2026-10-18
recheck: `REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000 GHIDRA_HEADLESS_MAXMEM=6G GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC node /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/scripts/rea.mjs analyze /home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/lib/node_modules/agent-browser/bin/agent-browser-win32-x64.exe --format json` → expect exit 0 and `evidence_id` `ev_8b688ce7b54ef1d08823734fda2f062fd19dfa2ca9f4023c329cbae22f726986` only if the request bytes match (analyze ids are content+params-keyed; `QUALITY.md:25`). Cheap check: stdout sha256 `2f39ab6618fa63d8cb4ac428c4505e923f5218231e738a0c3e962e55bdecadc3` (5660 B). A second run was not made; id stability across a rerun is unknown.

REA pin: `rea-agents@6.5.0` (npx cache `ad9a3fdbcad992c6`, `package.json` version field). Provider Ghidra 12.1.4. JDK 21.0.12.1. Host node on PATH during the run window: v26.12.0. Claim source: the sealed envelope, not the skill text.

Artifact: `/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/lib/node_modules/agent-browser/bin/agent-browser-win32-x64.exe`, 17,694,720 bytes, SHA-256 `a6a9a3654c41ee19c05961b73489db98cff9eae88a77436986df08a7a7a73786`. `file`: PE32+ MS Windows 5.02 console, x86-64, 10 sections, stripped to external PDB. This is the rung named unrun at `LOG.md:1114`. It is not `/home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/windows_release_arm64.exe`.

Run envelope: `/var/tmp/arc2-l6r6-E9-mid/stdout.json` (5660 bytes, sha256 `2f39ab66…`, mtime 2026-10-18 18:27:28 -0300). Exit 0, wall 2479 s (`meta.txt:7-14`). Evidence `ev_8b688ce7…`. `operation: binary_overview`, `confidence: derived`, `authority: shipped-artifact`, `analyzer_preset: ghidra-default` (the disabled-analyzers env was NOT set on this run — the hold is natural, not mitigated), provider `ghidra` 12.1.4 via `rea-agents@6.5.0`.

Procedure census (envelope `normalized_result` only — no per-procedure list, no exported/local/EXTERNAL split): image base `0x140000000`; 11 segments / 19012 procedures / 4382 strings. Segments (end exclusive): Headers `0x140000000-0x140000400` (1024); `.text` `0x140001000-0x140b95400` (12141568); `.data` `0x140b96000-0x140b97000` (4096); `.rdata` `0x140b97000-0x141019200` (4727296); `.pdata` `0x14101a000-0x141035a00` (113152); `.xdata` `0x141036000-0x1410da200` (672256); `.bss` `0x1410db000-0x1410db2a0` (672); `.idata` `0x1410dc000-0x1410de200` (8704); `.CRT` `0x1410df000-0x1410df200` (512); `.tls` `0x1410e0000-0x1410e0200` (512); `.reloc` `0x1410e1000-0x1410e7400` (25600).

Entry-point decompile: NOT IN THE ENVELOPE. `locations` is `[]`, `raw_result` is null, and the 5660 bytes contain zero `decompile` / `pseudocode` / `entry_point` strings (E9 recorded the same gap). Do not invent pseudocode. Header observation only (not a decompile): `AddressOfEntryPoint` `0x1410` + `ImageBase` `0x140000000` = `0x140001410`, inside `.text`. A `decompile` of that VA was not run.

Scale-ladder placement: 2.5MB held in 44s (round-3 bisect leg, `ev_92dea347…`); 17.7MB held in 2479s at 6G heap (this entry, natural, unmitigated); 91.6MB remains the wall — round-4 memory-kill at 7G (10 decompile workers) and round-6 name-validation refusal (unknown analyzer aborts before any disable; `Call Convention ID` is the registered name for the guessed class). The 41.3MB gap between held and wall is now bracketed by two live points.

Not examined: procedure-name census, import thunks, deep strings, second-run evidence-id stability, runtime behavior.
