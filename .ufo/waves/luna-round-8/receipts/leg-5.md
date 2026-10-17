# L5 receipt

- Command: from `/tmp`, start MCP server with `npx -y rea-agents@6.4.0 --mcp` (240-second ceiling); initialize protocol `2024-11-05`, then issue `tools/call` with name `inspect_electron_fuses` and arguments `{ "path": "/usr/lib/signal-desktop/signal-desktop" }`.
- Carrier verification command: `cd /tmp && stat -c '%F %s bytes %n' /usr/lib/signal-desktop/signal-desktop && sha256sum /usr/lib/signal-desktop/signal-desktop`
- Carrier verification output: `regular file 223513856 bytes /usr/lib/signal-desktop/signal-desktop`; `f7a9b441e825b388260430f9edd9a2f94fd50be497bf66192a16aeab87afc85a  /usr/lib/signal-desktop/signal-desktop`
- Full MCP server stdout:
```text
{"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{"listChanged":true},"completions":{},"prompts":{"listChanged":true}},"serverInfo":{"name":"rea","version":"6.4.0"},"instructions":"REA provides reverse-engineering tools for local artifacts, native binaries, managed code, browser pages, and runtimes. Use the tool that directly answers the question; discover targets or inspect inventory only when needed. Tool results include inline Evidence and report their coverage and limitations."},"jsonrpc":"2.0","id":1}
{"jsonrpc":"2.0","id":2,"error":{"code":-32602,"message":"Tool inspect_electron_fuses not found"}}
```
- Full MCP server stderr: *(empty)*
- MCP server exit code: `0` (after stdin closed)
- MCP server stdout sha256: `adfb73708050d445e14a8079945a1f7a437dc90f85c8e2491d3533a1f927b115`
