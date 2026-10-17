## CLAIM
`/usr/bin/jq` is a suitable definitely-not-Flutter ELF for L9. `/usr/lib/pinta/Pinta.dll` is a suitable definitely-not-Harmony app artifact for the L10 refusal fallback.

## METHOD
Read-only carrier discovery: `file`, `sha256sum`, `pacman -Qo`, `readelf -d`, `jq --version/--help`, `find`, plus inspection of Pinta's desktop launcher. No REA, MCP, or npx probe.

## FINDINGS
- `file /usr/bin/jq` → “ELF 64-bit LSB pie executable, x86-64”; SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`; `pacman -Qo` → owner `jq 1.8.2-1`. `jq --version` → `jq-1.8.2`; `--help` identifies it as a command-line JSON processor. `readelf -d` lists only `libjq.so.1`, `libonig.so.5`, and `libc.so.6` as NEEDED libraries (no Flutter dependency).
- Pinta launcher `/usr/share/applications/com.github.PintaProject.Pinta.desktop:3,59,114,227-234` identifies Pinta as an image-editing Application (`Exec=pinta`, Graphics categories). `/usr/lib/pinta/Pinta.dll` is a PE32 Mono/.NET GUI assembly (`file`); SHA-256 `76472751de517b04c163b4931da34223a5263df54866a30e121d0a67d246b9e8`; package owner `pinta 3.1.2-2`. This Linux desktop image editor assembly is a clear non-Harmony input candidate.
- `find` for `*.wasm` under the kaidoku corpus, `/usr/lib`, `/usr/share`, `/home/vgpnk/Projects/shokunin`, and `/opt` returned no paths.

## THREATS
This is carrier discovery only; neither preregistered refusal outcome is verified until the actual REA calls. The Wasm search is limited to the named roots and does not establish machine-wide absence.

## VERDICT
CLEAN — candidates identified: `/usr/bin/jq` for L9 and `/usr/lib/pinta/Pinta.dll` for the L10 Harmony-refusal fallback; no standalone Wasm carrier found in the searched roots.
