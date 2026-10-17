## CLAIM
Audit of EX1–EX10 reports against the delivered receipts in `.ufo/waves/luna-round-6/receipts/`. 8/10 match on every checkable point; EX6 and EX9 do not, both traceable to concurrent receipt overwrites rather than numbers that fail to reproduce.

## METHOD
Read all ten reports; recomputed each recorded stdout SHA-256 from receipt bytes (Python sha256 over the exact frame/block lines, LF-inclusive); checked every cited line; re-hashed carriers read-only (`sha256sum /bin/true /usr/bin/jq /usr/bin/docker`; libsignal `.node`; `receipts/MANIFEST.txt`); confirmed WABT absence (`REA_WABT_BIN_DIRECTORY` unset; `command -v wasm-validate/wasm-objdump/wasm2wat` empty). No re-runs, no writes outside this file.

## FINDINGS
Reproduce exactly: EX1 `3eb8e06c…`=sha256(`6.5.0\n`), MANIFEST matches leg-1.md; EX2 207 tools, `38d44bf8…`=sha256(init+tools frames, 3,089,024 B), round-2 `L7.md:2,5` valid; EX3 `fb47bd53…`=sha256(init+tools+result frames, 3,099,964 B), cites `leg-3.md:75-106,219-221` valid, docker `70f68a77…`; EX4 evidence `ev_0618e7a5…`, 24,944,200 B, libsignal `1b44ed53…` re-verified (deviation self-flagged; SC2.md:8 does name `/usr/bin/rg`); EX5 `ev_36045c43…`, sentinel 35,260,752; EX7 every cite valid (`:3-10`, `:11-12`, `:14`, `:21`), replay 19,151 B / 3 frames / `3492d27d…`, SC5.md:9 and `/bin/true` 43,320 B `8bc9a73a…`→`/usr/bin/true` confirmed, failed-batch hash `fb227b57…`=sha256(initialize frame); EX8 `22205280…`=sha256(provider objdump stdout embedded in leg-8.md), `ev_aa75cc2e…`; EX10 `e4cf0833…`, two `capability_unavailable` calls, compare/harmony never reached (self-flagged).
Mismatch: EX9 cites `leg-9.md:3-19,14,21-35,39-42`, but delivered leg-9.md is 13 lines with no preserved batch-attempt block; both recorded hashes do derive (`2b596b31…` refusal frame; `1ff84c06…` init+refusal).
Unverifiable: EX6 — collision text accurate (leg-6.md is RV3's `ev_e0eb…`/`9a1445…`; `ev_1570cc…` exists only in EX6.md), but its claimed `/tmp/luna-round-6-ex6-*` captures and `/tmp/luna-round-6-leg-6.sqlite` carrier are gone.

## THREATS
Concurrent writers: RV3 claims L6–L8, RV4 claims L9–L10; PS3.md:18, CA2.md:10, RV7.md cite leg-8/leg-9 line numbers (e.g. `leg-9.md:45-47`) that no longer resolve. `.ufo` is untracked (`?? .ufo/waves/luna-round-6/`), so overwritten versions are unrecoverable. EX8's "tools/list 207" and "stalled attempt terminated" appear in no receipt (not contradicted). This audit rests on delivered bytes only.

## VERDICT
FINDING: 8/10 EX reports verify against delivered receipts; EX9 cites a superseded leg-9 version, and EX6's own L6 transcript has no surviving artifact.
