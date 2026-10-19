# PROVINCE.md repair — Frontier bullet "Alternate providers": JEB is probed, not "unprobed"

Authored by SEAT EX-13 (chain c2, executor), wave `arc3-loop1-round4`, 2026-10-19.
**Patch text only** — seats never write `PROVINCE.md`; the parent applies.

## Stale item (census-checked, falsified)

`PROVINCE.md` Frontier bullet `Alternate providers`, current bytes:

> IDA (`REA_IDA_MCP_CONFIG` unset), Hopper (absent), JEB (unprobed).

`JEB (unprobed)` is stale: the JEB provider has been probed and its gate is
recorded as a **typed refusal**, in admitted corpus:

- `corpus/knowledge/2026-10-13-r2-provider-capability-matrix.md` — run-log row
  `rea inspect-jeb-client` → fail, `provider_id: jeb`,
  `capability_unavailable` / `unsupported_provider`, gate: start a JEB client
  serving MCP (default `http://127.0.0.1:8425/mcp`) or set `REA_JEB_MCP_URL`;
  live probe recorded as `fetch failed`. The same entry's provider matrix names
  `jeb` (`REA_JEB_MCP_URL`, probes `127.0.0.1:8425/mcp`) among the 7 observed
  provider ids.
- `corpus/knowledge/2026-10-13-r2-frontier-prereqs.md` — candidate "JEB
  provider": "Fully absent. `REA_JEB_MCP_URL` unset; no JEB install …", with the
  gate row "env unset, no install, port 8425 closed — **absent — operator-owned**".
- `corpus/knowledge/2026-10-14-r12-02-queue-b-ledger.md` — re-verifies the same
  gate: "`REA_JEB_MCP_URL` UNSET, no JEB install, :8425 closed."

Host re-check this wave: `REA_JEB_MCP_URL` unset (empty expansion);
`ss -ltn | grep 8425` → closed. IDA (`REA_IDA_MCP_CONFIG` unset) and Hopper
(`/opt/hopper/bin/Hopper` → "No such file or directory") remain correct, and
`Alternate providers … Engine installs are operator-owned` stays true.

## Change (same-line replacement, line count held at 2)

`PROVINCE.md`

```diff
# file: PROVINCE.md
-- **Alternate providers** — IDA (`REA_IDA_MCP_CONFIG` unset), Hopper (absent),
-  JEB (unprobed). Engine installs are operator-owned.
+- **Alternate providers** — IDA (`REA_IDA_MCP_CONFIG` unset), Hopper (absent),
+  JEB (`REA_JEB_MCP_URL` unset; typed `capability_unavailable`). Operator-owned.
```

## Census conformance

- Line-neutral: 2 → 2 lines; `PROVINCE.md` stays at 162 lines (DATED marker at
  line 119 does not shift).
- Needle-free: no `rea-agents@x.y.z`, no bare `6.x.y`, no `~`/`/`-absolute
  `path:line`. (`REA_JEB_MCP_URL` and `REA_IDA_MCP_CONFIG` are env-key names,
  not version pins — the same forms the current bullet already carries.)
- Search text verbatim and unique (verified in the apply-and-census run under
  `claims/c2/EX-13/evidence/`).
