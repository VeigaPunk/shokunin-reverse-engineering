## CLAIM
Assigned legs 1–2 reproduce the preregistered outcomes and match their round-6 receipt stdout bytes.

## METHOD
From `/tmp`, ran `timeout 240 npx -y rea-agents@6.5.0 --version`; queried `tools/list` over MCP after initialize/initialized using `npx -y rea-agents@6.5.0 mcp` with a 240-second timeout. Kept npm cache and replay bytes under `/tmp/kaidoku-luna-round6-rv1-rr7ezvqj`. Compared stdout bytes directly with the captured stdout sections in `.ufo/waves/luna-round-6/receipts/leg-1.md` and `leg-2.md`.

## FINDINGS
- L1: stdout `6.5.0\n`, exit 0; direct byte comparison MATCH. SHA-256 `3eb8e06ca1e02f0a30b0e3eebd289494b35d4fd1466ed907b9148e03b2459b00` matches `.ufo/waves/luna-round-6/receipts/leg-1.md:3-11`.
- L2: typed `tools/list` response count 207, exit 0; raw stdout 3,089,024 bytes; direct byte comparison MATCH. SHA-256 `38d44bf8ee0944315a1d50d3e3acec1401be50efe7090ac22ec8498e853d4129` matches `.ufo/waves/luna-round-6/receipts/leg-2.md:6-10`.
- My MCP process group was terminated after its response. A cold L1 npx call emitted npm deprecation/update notices on stderr; stdout and exit status remained as predicted.

## THREATS
This replay covers only legs 1–2 and does not establish global host-mutation or config-drift claims. A final `ps -eo pid,ppid,pgid,args` check found peer EX8’s MCP launcher still running as PID 5403 (PGID 5401); I left it untouched to avoid terminating another seat’s probe.

## VERDICT
FINDING: A peer EX8 MCP process remained active at the final process check.
