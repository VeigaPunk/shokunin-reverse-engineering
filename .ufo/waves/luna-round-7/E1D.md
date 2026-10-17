## CLAIM
Draft one QUALITY.md-grounded knowledge entry for `inspect_go_binary`, from retained round-6 evidence only. The specified `E1V.md` was not found in the repo.

## METHOD
Read `corpus/QUALITY.md`, the two leg-3 receipts, and SC1; compared the corpus entry style. `Glob("**/E1V.md")` → `No matches found`. No live probes, network, git mutations, or corpus/map edits.

## FINDINGS
Draft destination (not written per seat constraints): `corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md`.

Full proposed file text:

```markdown
# inspect_go_binary — embedded Go build information

REA pin: `rea-agents@6.5.0` (MCP server reports 6.5.0); provider `go-build-info` v1.

Artifact: `/usr/bin/docker`, ELF x86_64, SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9`.

Reproduce: run `cd /tmp && npm_config_cache=/tmp/kaidoku-luna-round-6-npm-cache TMPDIR=/tmp npx -y rea-agents@6.5.0 mcp`; send MCP `tools/call` for `inspect_go_binary` with `{"path":"/usr/bin/docker"}`. The recorded input schema accepts only `path` (no detail or filter options). The call returned Evidence ID `ev_671861638ed7fe544cce229c3d4a9258766337a5e72dcf79f107af713b596a4b`.

- **Observation:** The result binds that path and SHA-256; reports ELF/amd64, 29,327,600 bytes, inline build info at offset 28,873,984, Go version `go1.26.5-X:nodwarf5`, module path `github.com/docker/cli/cmd/docker`, and settings including `GOOS=linux`, `GOARCH=amd64`, `CGO_ENABLED=1`. It reports `module.complete=true` and no unparsed lines.
- **Inference:** On this carrier, the verb extracts embedded Go build metadata; this single positive result does not establish general detection coverage.
- **Unknown:** Missing metadata is not proof an image is not Go. Compiler identity, dependency authenticity, and runtime behavior are not established.
- **Limitations:** This does not recover functions, source mappings, types, or decompiled code. The receipt describes 256 MiB read/header-search bounds, 1 MiB aggregate embedded-string bound, 16 MiB structural-table bound, and 8 MiB complete-metadata bound; these are not OS resource limits.

Sources: `.ufo/waves/luna-round-6/receipts/leg-3.md:3-8,16-18,71-79,93-108,169-181`; corroborating receipt `.ufo/waves/luna-round-6/receipts-B/leg-3.md:10-21,25-30,40-53,84-95`; carrier scout `.ufo/waves/luna-round-6/SC1.md:4-18`.
```

## THREATS
E1V.md is absent, so this draft follows retained receipts rather than that seat's requested input. The result is scoped to one pinned carrier; it does not claim universal capability or promote the exercise to Core.

## VERDICT
FINDING: evidence-backed draft prepared; E1V.md unavailable, and no corpus entry was written.