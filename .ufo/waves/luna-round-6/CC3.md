## CLAIM
Cross-lane leg-3 comparison (frozen class: RESULT — `inspect_go_binary` on a Go ELF): lane A `receipts/leg-3.md` vs lane B `receipts-B/leg-3.md` (BB3) for outcome class and key fields, corroborated by my own CC3 re-run.

## METHOD
Read both lane receipts and `BB3.md`/`EX3.md`; recomputed lane-A stdout digest `fb47bd53…` (`receipts/leg-3.md:221`) and lane-B receipt hash `9785585…` (`receipts-B/MANIFEST.txt:3`). Re-verified carrier `/usr/bin/docker` (`file`+`sha256sum` → `70f68a77…`). Independent CC3 re-run from `/tmp`: staggered stdio harness (initialize → initialized → tools/list → tools/call `inspect_go_binary`), stdin closed after the id:3 response; raw stdio kept at `/tmp/cc3-luna6/` (stdout 3,099,964 B, sha256 `fb47bd53…`; stderr 181 B; exit 0; MCP tree verified gone). No config edits.

## FINDINGS
- RESULT class both lanes: typed structured result, `operation=inspect_go_binary`, no refusal/error, exit 0, graceful stdin-close (`BB3.md:11`; `receipts/leg-3.md:219-221`).
- Key fields identical: carrier sha256 `70f68a77…` (= live file), `go_version` `go1.26.5-X:nodwarf5`, module `github.com/docker/cli/cmd/docker`, provider `go-build-info` v1, predicate `rea.analysis`, confidence `observed`, authority `shipped-artifact`, locations [28873984, 28874016] (`BB3.md:12`; lane-A id:3 response).
- My re-run's stdout is byte-identical to lane A's (`fb47bd53…`; lines `fb227b57…`, `71dd0a2e…`, `9adf6c03…`). Lane-B stdout differs only by harness shape (no `tools/list` fetch: 12,904 B, `75b83edf…`, `BB3.md:11`) — equivalence, not mismatch.
- Incident repaired: my 19:07:53 write replaced BB3's receipt (`9785585…`→`0fe9cd2c…`); reconstructed its exact bytes from `/tmp/rea-bb3/` parts (raw concat of header+stdout+footer = `9785585…`, 15,803 B) and restored `receipts-B/leg-3.md`; all ten manifest entries re-verify MATCH.

## THREATS
BB3's receipt was briefly replaced mid-wave (mtime moved; content byte-exact). The CC-overwrites-BB class also hit legs 7–8 and stays unrepaired (`CB3.md:21`). Comparison is host/package-version specific; battery-wide controls are other seats' scope.

## VERDICT
FINDING: leg-3 comparison CLEAN (RESULT, key fields agree cross-lane) but CC3's re-run overwrote BB3's receipt mid-wave; byte-restored and manifest re-verified.
