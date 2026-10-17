## CLAIM
L3–L5 replays each returned typed `RESULT`. L5 matches its existing receipt’s key fields; L3/L4 receipt comparison is unavailable because those baseline receipts are absent.

## METHOD
From `/tmp`, ran a separate `timeout 240 npx -y rea-agents@6.5.0 mcp` session per leg. Each session completed initialize, called the assigned tool, waited for response id 2, then closed stdin; each exited 0. Full captures and stdout digests: `/tmp/luna-round-6-rv2/leg-{3,4,5}.md`. A first batched attempt returned no tool response and was discarded before this handshake-based replay.

## FINDINGS
- L3 `/usr/bin/docker`: RESULT; Go provider `go-build-info`; artifact SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9`, Go `go1.26.5-X:nodwarf5`, module `github.com/docker/cli/cmd/docker`. Replay stdout SHA-256 `af23888b23bc19c51360d99913ed4de22c3f8aea0c3999593fbb72a61c6ccfea` (`/tmp/luna-round-6-rv2/leg-3.md:13`). No `receipts/leg-3.md` in `ls -la .ufo/waves/luna-round-6/receipts` output.
- L4 `/usr/bin/rg`: RESULT; Rust provider `rust-auditable`; artifact SHA-256 `d006acfe51619144af4709e85945fe3b5a6f05038d356c4d8f752a33b4ecae42`; `.dep-v0` metadata and rustc commit are null. Replay stdout SHA-256 `1c586f5a45612f425b3e061f44f060fffb4ad9f6969ac663be017118816cc25a` (`/tmp/luna-round-6-rv2/leg-4.md:13`). No `receipts/leg-4.md` in the same listing.
- L5 Signal: RESULT; evidence ID `ev_36045c43ecbed14e3eb3b77a720c24c115cc2377737d2ed2fe8acce76a4288ed`, artifact hash, sentinel offset `35260752`, and all nine fuse states match `receipts/leg-5.md:5,8`. Replay stdout SHA-256 is `6b35f64df3f4c07264a07562eef2ddfbaf58a47da74d46c4f5f0a9746c95d600`, unlike receipt hash `afebe903c95c3505b253b273666622a2b1c0cfbcb39b3bcce618053ec9835a41`, because replay stdout also includes MCP protocol frames.

## THREATS
No host-mutation, config-drift, command-A, or map-token audit was part of this seat. The L3/L4 comparison remains incomplete pending their canonical receipts.

## VERDICT
FINDING: L3/L4 baseline receipts were absent, preventing the requested receipt comparison; L5 replay matched its receipt.