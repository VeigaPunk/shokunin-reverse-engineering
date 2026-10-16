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
