## CLAIM
The host has `.wasm` carriers; `/usr/bin/true` is a sub-500 KB ELF suitable for `search_bytes`; `/usr/bin/jq` exists for the objdump leg.

## METHOD
Read-only discovery from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`: `find / -type f -name '*.wasm' -print 2>/dev/null`; `stat`, `file`, and `sha256sum` on selected carriers and binaries. No carrier was executed.

## FINDINGS
- `.wasm` files found, including `/home/vgpnk/.local/share/opentui/tree-sitter/languages/tree-sitter-json.wasm` (5,596 bytes; `file`: WebAssembly MVP module; SHA-256 `d2119fb98d5912719b13f9458574f8608d2d29dfbe45f6be1f860ea1fe2a2405`). The host scan also found WebAssembly files under installed Node packages and Chromium extensions.
- `/usr/bin/true`: 43,320 bytes; `file`: ELF 64-bit LSB pie executable, x86-64; SHA-256 `8bc9a73afd7d85061160857536e093ded799dae7a2f0cf5758c4553f2f83002d`.
- `/usr/bin/jq`: 30,800 bytes; `file`: ELF 64-bit LSB pie executable, x86-64; SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`.

## THREATS
The root `find` returned exit 1; stderr was redirected, so the cause and completeness of enumeration are unverified. Positive matches establish that host `.wasm` carriers exist. Initial `git status --short` showed untracked `.ufo/interactive-sessions/` and `.ufo/waves/`; no existing tracked files were modified.

## VERDICT
CLEAN
