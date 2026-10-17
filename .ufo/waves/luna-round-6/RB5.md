# RB5 — Review SC1–SC6 carrier selection (lane B, deepseek-v4.1-flash)

## CLAIM
SC1–SC6 carrier selections are sound: every carrier is a genuine Go/Rust/Electron/SQLite artifact, or a valid non-matching input for L9–L10, and none is manufactured or faked.

## METHOD
Independent read-only re-verification of every path named in SC1–SC6: `file`, `stat`, `sha256sum`, `pacman -Qo`, `readelf`, `strings`, `od`. Recomputed hashes compared against each SC report. No carrier executed; no lane-A receipt read.

## FINDINGS
- Hash equality 9/9. Recomputed SHA-256 match the SC reports verbatim: docker `70f68a77…45c9` (SC1), rg `d006acfe…ae42` (SC2), signal-desktop `f7a9b441…c85a` and Typora `d9635cd3…7767a` (SC3), true `8bc9a73a…002d` and jq `e8156675…7806` (SC5), Pinta.dll `76472751…b9e8` (SC6), tree-sitter-json.wasm `d2119fb9…2405` (SC5), pnpm index.db `3701a7e3…9728` (SC4). jq hash is identical in SC5 and SC6 — cross-consistent.
- Provenance: `readelf -p .go.buildinfo /usr/bin/docker` shows `path github.com/docker/cli/cmd/docker`, `go1.26.5`, `CGO_ENABLED=1` — real Go (closes SC1's own gap that `file` alone doesn't prove Go). `strings -a /usr/bin/rg` shows `/build/.cargo/registry/src/index.crates.io-…/aho-corasick-1.1.4/…` — real Rust. Both Electron trees carry `app.asar`, `chrome-sandbox` (15232 B), `icudtl.dat`; ELF strings show `Electron/43.5.0` (Signal) and `Electron/42.2.0` (Typora); SC3 correctly excluded `/usr/bin/obsidian` (verified: bash script). `od` on index.db: `53 51 4c 69 74 65 20 66 6f 72 6d 61 74 20 33 00` = "SQLite format 3\0". wasm magic `00 61 73 6d 01 00 00 00`.
- Refusal inputs: `readelf -d /usr/bin/jq` NEEDED = libjq.so.1, libonig.so.5, libc.so.6; no libflutter/libil2cpp found — valid not-Flutter L9 input. Pinta.dll header `4d 5a`, PE32 Mono/.NET (pinta 3.1.2-2) — valid non-Harmony L10 fallback.
- Anti-cheat: every system carrier is distro-package-owned (`pacman -Qo`: docker 1:29.7.2-1, ripgrep 15.2.0-1, signal-desktop 8.26.0-1, typora 1.14.9-1, jq 1.8.2-1, coreutils 9.11-2, pinta 3.1.2-2); none is a hand-crafted stub, copied stand-in, or text file behind a magic header.

## THREATS
- pnpm index.db is live host state; SC4 itself flags copy-to-`/tmp` before probing — a lane runtime-discipline issue, not a selection flaw.
- SC6's negative claim (no wasm in its searched roots) is scoped and consistent with SC5's root-wide find; negative scans not exhaustively re-run.
- This review verifies carrier identity only, not later REA leg outcomes.

## VERDICT
CLEAN — all nine carriers real, hash-exact, package-sourced; no cheating detected.
