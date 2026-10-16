# Receipt B/leg-1 — L1 version check (rea-agents@6.5.0)

Seat: BB1 (lane B, deepseek-v4.1-flash) | Host date: 2026-10-16
Probe rule honored: npx run from /tmp only, 240s timeout budget.

## Command

```
cd /tmp/rea-bb1 && npx -y rea-agents@6.5.0 --version
```

Launcher resolved: /home/vgpnk/.local/share/mise/installs/node/latest/bin/npx (node v26.12.0)
Wall time: ~0.6s (npx cache hit)

## Stdout (full, verbatim)

```
6.5.0
```

Raw bytes: 36 2e 35 2e 30 0a (6 bytes, trailing newline)

## Stdout sha256

```
3eb8e06ca1e02f0a30b0e3eebd289494b35d4fd1466ed907b9148e03b2459b00
```

## Stderr (full, verbatim)

```
(empty)
```

## Exit code

```
0
```

## Frozen prediction (pre-registered)

L1: version 6.5.0, exit 0 → outcome class RESULT.

Observed: stdout `6.5.0`, exit 0 → RESULT. MATCH.

No MCP server was started (CLI flag only); nothing to terminate.
