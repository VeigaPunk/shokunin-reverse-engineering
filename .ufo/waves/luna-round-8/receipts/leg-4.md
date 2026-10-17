# L4 receipt — `inspect_rust_binary` on `/usr/bin/rg`

- Working directory: `/tmp`
- Command: `/tmp` cwd; `npx -y rea-agents@6.4.0 --mcp` (stdio child of a 240-second Python harness)
- MCP requests (JSON-RPC 2.0, protocol `2024-11-05`): initialize; `notifications/initialized`; `tools/call` id 2 with `{"name":"inspect_rust_binary","arguments":{"path":"/usr/bin/rg"}}`.
- Full stdout SHA-256: `0fbd3bd0d3095c7c5fe6b2605618dfb88cc3b5f4268cfd9f7d18c683f7030d5f`
- Full stderr: *(empty)*
- Exit code: `0` (server exited after client stdin closed).
- Full stdout:

```text
{"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{"listChanged":true},"completions":{},"prompts":{"listChanged":true}},"serverInfo":{"name":"rea","version":"6.4.0"},"instructions":"REA provides reverse-engineering tools for local artifacts, native binaries, managed code, browser pages, and runtimes. Use the tool that directly answers the question; discover targets or inspect inventory only when needed. Tool results include inline Evidence and report their coverage and limitations."},"jsonrpc":"2.0","id":1}
{"jsonrpc":"2.0","id":2,"error":{"code":-32602,"message":"Tool inspect_rust_binary not found"}}
```
