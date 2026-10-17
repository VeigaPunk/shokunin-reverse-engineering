## CLAIM
RV6 cannot establish carrier continuity: its recorded pass saw no SC reports or receipts, and the available receipt format hashes stdout, not input bytes. A later exact-path comparison could catch different-path substitutions, not same-path byte swaps or replay.

## METHOD
Read `RV6.md:5-11`, `SC1.md`–`SC6.md`, and receipts `leg-1.md:3-11`, `leg-2.md:1-7`. Current `Glob .ufo/waves/luna-round-6/receipts/leg-*.md` returns only L1 and L2. No REA/MCP probes.

## FINDINGS
Easiest substitutions; RV6 status means its recorded audit, not a hypothetical rerun:
1. L1: PATH `npx` shim printing `6.5.0` — **no**; no carrier identity, stdout hash only.
2. L2: replay/canned 207-tool listing instead of live 6.5.0 `tools/list` — **no**; receipt text does not authenticate the process.
3. L3: use any easier Go ELF instead of `/usr/bin/docker` — **no at snapshot**; a later path check could flag a different path, not replacement bytes at that path (`SC1.md:10-16`).
4. L4: any Rust ELF instead of `/usr/bin/rg` — same (`SC2.md:8-15`).
5. L5: substitute another Electron binary (SC3 already lists Signal and Typora) — **no**; no unique carrier selected (`SC3.md:10-16`).
6. L6: use a tiny/fabricated SQLite DB instead of pnpm `index.db` — **no at snapshot**; path-only check conditional (`SC4.md:8-21`).
7. L7: use a tiny file containing ELF magic instead of `/usr/bin/true` — **no at snapshot**; path-only check conditional (`SC5.md:8-10`).
8. L8: inspect `/usr/bin/true` instead of pinned `/usr/bin/jq` — **no at snapshot**; later path check could catch.
9. L9: same swap to get an easy non-Flutter refusal — **no at snapshot**; later path check could catch.
10. L10: force the Pinta/Harmony-refusal fallback despite discovered Wasm — **not shown caught**; SC5 reports Wasm present, while SC6’s narrower search says none (`SC5.md:8-13`, `SC6.md:10-13`).

## THREATS
No L3–L10 receipts yet; cannot establish what was actually supplied. RV6 explicitly marks its result as a snapshot (`RV6.md:11`). SC3 permits two Electron candidates; SC5/SC6 disagree on Wasm scope.

## VERDICT
FINDING: RV6’s recorded check cannot catch or rule out these substitutions; stdout digests do not bind input identity.