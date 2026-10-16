# Receipt B/leg-9 — L9 identify_flutter_build on non-Flutter `/usr/bin/jq` (typed refusal)

Seat: BB9 (lane B, deepseek-v4.1-flash) | Host date: 2026-10-16
Probe rule honored: npx/MCP run from /tmp only, 240s timeout budget, no config edits, MCP server terminated.

## Target identity (input)

`/usr/bin/jq`: ELF 64-bit LSB pie executable, x86-64, stripped, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=cc56d2fd644ddd549b5339882e77f22f781525d3; `jq-1.8.2`; sha256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`.

## Command

```
cd /tmp/rea-bb9 && timeout 240 node probe.mjs   # stdout -> stdout.txt, stderr -> stderr.txt
```

Harness `/tmp/rea-bb9/probe.mjs` spawns (child process, cwd `/tmp/rea-bb9`):

```
npx -y rea-agents@6.5.0 mcp
```

Launcher: `/home/vgpnk/.local/share/mise/installs/node/latest/bin/npx` (node v26.12.0, npx 11.20.0). 6.5.0 npx cache present: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`. Wall time ~0.7s.

## JSON-RPC token set (exact, sent)

1. `initialize` id 1, protocolVersion `2025-03-26`, clientInfo `kaidoku-seat-bb9`. Server reply: protocolVersion `2025-03-26`, serverInfo `{"name":"rea","version":"6.5.0"}`.
2. `notifications/initialized`
3. `tools/call` id 2: `{"name":"identify_flutter_build","arguments":{"path":"/usr/bin/jq"}}` (schema is strictObject `{path}` per the 6.5.0 tool contract).

## Stdout (full, verbatim, 772 bytes)

```json
{
  "result": {
    "_meta": {
      "provenance": {
        "untrusted_content": true,
        "source": "analysis_target"
      }
    },
    "content": [
      {
        "type": "text",
        "text": "{\"error\":{\"code\":\"invalid_request\",\"category\":\"invalid_input\",\"message\":\"Analysis input is invalid. Check the arguments and try again.\",\"retryable\":true,\"remediation\":{\"action\":\"Correct the listed arguments and retry.\"},\"details\":{\"operation\":\"identify_flutter_build\",\"issues\":[{\"path\":[\"path\"],\"reason\":\"invalid_format\",\"message\":\"The APK could not be read as a package: /usr/bin/jq: ZIP archive is malformed: End of central directory not found\"}]}}}"
      }
    ],
    "isError": true
  },
  "jsonrpc": "2.0",
  "id": 2
}
```

## Stdout sha256

```
2a20c456d5cccebbe1b84f86582f774001f93527fedf88b1d5fbd1c332e747bd
```

## Stderr (full, verbatim, 189 bytes)

```
initialize ok after 654ms; serverInfo={"name":"rea","version":"6.5.0"}
tools/call response received after 665ms total
server exit: code=0 signal=null graceful=true
server stderr bytes: 188
```

Server-process stderr (188 bytes, raw pino log line, file `/tmp/rea-bb9/raw-server.stderr`, sha256 `f1617b4fffef4b1c2ce5fd509a21dd2d0b6c67b19edd8dd010b1bfb734e8dbaa`):

```json
{"level":40,"time":1792188090514,"application":"rea","mode":"mcp","layer":"server","tool":"identify_flutter_build","durationMs":4.03,"status":"error","msg":"MCP tool execution completed"}
```

## Exit code

```
0
```

(Command exit 0; MCP server exited code 0, no signal, on stdin EOF — graceful shutdown, no SIGTERM/SIGKILL needed.)

## Termination / process hygiene

Graceful stdin-EOF shutdown; server exit code 0 recorded above. Post-run scan for node/npx with cwd `/tmp/rea-bb9`: none (only the scanning shell itself matched text greps). A broad `pgrep -af rea-agents` matched unrelated processes of concurrent seats (e.g. `timeout 60 npx -y rea-agents@6.5.0 mcp --help` from `/tmp/cc6-leg6`) — none belong to this seat; this seat's tree had already exited 0.

## Frozen prediction vs observed

L9 frozen prediction: `identify_flutter_build` on `/usr/bin/jq` → TYPED-REFUSAL class.

Observed: MCP result `isError: true` carrying a structured typed error — `code: invalid_request`, `category: invalid_input`, `details.issues[0].reason: invalid_format` with message "The APK could not be read as a package: /usr/bin/jq: ZIP archive is malformed: End of central directory not found". Structured, typed, input-bound refusal → TYPED-REFUSAL. **MATCH.**

## Not audited here

Operator-config drift, command A / map-token set, and the other nine legs were not measured by this seat (not its assignment). No config file was read or edited.
