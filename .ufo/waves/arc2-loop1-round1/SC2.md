# SC2 (scout) — REA pin census: 3 client configs vs PROVINCE.md surface summary

Wave arc2-loop1-round1 · Seat SC2 · 2026-10-18 · read-only census (only write: this report). No secret/credential values printed anywhere — only version pins, config key names, and file hashes are emitted. (This file wholly overwrites the interrupted first attempt's SC2.md.)

## Verdict

**MIXED — Devin and OMP claims CORROBORATED; Kimi claim REFUTED (stale version + stale pointer).** Configured today: Devin `rea-agents@6.5.0` (`/home/vgpnk/.config/devin/mcp_config.json:7`) and OMP `rea-agents@6.5.0` (`/home/vgpnk/.omp/agent/mcp.json:8`) match PROVINCE.md:16-17 byte-for-byte. Kimi does not: PROVINCE.md:10 and :18 claim `rea-agents@6.4.0` at `/home/vgpnk/.kimi-code/config.toml:1478`, but the file's only `rea-agents` occurrence is `rea-agents@6.7.0` at `:2940` (table `[mcp_servers.rea]` :2938), and `:1478` is now `model = "kimi-k3"` inside a models table. The drift predates this wave: both 2026-10-18 config.toml backups already carry 6.7.0 (:2915, :2932). Zero drift during the wave window: current sha256s of all three configs equal `.ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt` (stamped 2026-10-18T14:49:13Z, file mtime 11:49:13 -03:00).

## Evidence — commands run this session with observed output excerpts

Census stamp: `date -Is` → `2026-10-18T13:40:27-03:00`.

1. Pin scan (value-safe; only the version substring emitted):
   `grep -n 'rea-agents'` on each config —
   ```
   /home/vgpnk/.config/devin/mcp_config.json:7:        "rea-agents@6.5.0",
   /home/vgpnk/.omp/agent/mcp.json:8:        "rea-agents@6.5.0",
   /home/vgpnk/.kimi-code/config.toml:2940:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
   /home/vgpnk/.kimi-code/mcp.json: (no matches)
   ```
2. Kimi targeted scan: `grep -n 'rea-agents\|mcp_servers\.rea\|REA_' /home/vgpnk/.kimi-code/config.toml` →
   ```
   2938:[mcp_servers.rea]
   2940:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
   2943:[mcp_servers.rea.env]
   ```
   → `:2940` is the whole file's only pin; PROVINCE.md:18's pointer `:1478` is stale.
3. Stale-pointer proof: `sed -n '1478p' /home/vgpnk/.kimi-code/config.toml` → `model = "kimi-k3"` (inside `[models."opencode-go-3/kimi-k3"]`, a models table). File is 2964 lines (`wc -l`).
4. Drift timeline: `stat -c '%y %n'` → kimi `config.toml` mtime `2026-10-18 11:45:57 -0300`; devin/omp configs mtime `2026-10-14 17:53:20 -0300` (unchanged since PROVINCE's 2026-10-16 reverify — their corroboration is not mtime-tainted). Both backups already 6.7.0:
   `grep -n 'rea-agents' config.toml.20261018-085645.bak config.toml.20261018-114557.bak` →
   ```
   config.toml.20261018-085645.bak:2915:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
   config.toml.20261018-114557.bak:2932:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
   ```
   → 6.7.0 present at/before 2026-10-18 08:56; drift happened between the 2026-10-16 reverify and 08:56:45.
5. Pin resolution sanity — npx caches exist for all three versions (`ls -d ~/.npm/_npx/*/node_modules/rea-agents`; `jq -r '.name + " " + .version'` on each package.json):
   ```
   a1722018f28f9df2: rea-agents 6.7.0
   ad9a3fdbcad992c6: rea-agents 6.5.0
   dea9475797100b20: rea-agents 6.4.0
   ```
   The 6.7.0 pin has a matching cache, so it is resolvable (also independently seen by SC1.md:26).
6. Zero-drift re-check vs pre-pair receipt: `sha256sum` now —
   ```
   16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json
   38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  /home/vgpnk/.omp/agent/mcp.json
   3546e033aeaf68093faf4099ea8289de5dea7ec224e7c557f08bfa9d51cf9a2a  /home/vgpnk/.kimi-code/config.toml
   ```
   Identical to `.ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt:2-4` — zero drift across the census window (two checks this session, same values).
7. Key-name census (names only; no values beyond pins):
   - Devin: `mcpServers.rea.{command,args[0..2],env}`; env keys `GHIDRA_INSTALL_DIR`, `JAVA_HOME`, `REA_JADX_MCP_JAR` (`jq -r 'paths | join(".")'`).
   - OMP: same as Devin plus extra key `mcpServers.rea.type`.
   - Kimi: `[mcp_servers.rea]` {`command`, `args`, `startup_timeout_sec`}; `[mcp_servers.rea.env]` {`GHIDRA_INSTALL_DIR`, `JAVA_HOME`} — no `REA_JADX_MCP_JAR` key.
   - PROVINCE.md:44's env-key claim (`GHIDRA_INSTALL_DIR`, `JAVA_HOME`) holds for all three.
8. Other candidate sites scanned, no pin: `~/.kimi-code/mcp.json` (holds only `mcpServers.cli-agents`), `~/.config/devin/config.json`, `~/.omp/agent/config.yml` (no `rea-agents` matches). Historic pre-upgrade backups do carry 6.4.0: `mcp_config.json.rea.backup:7`, `mcp.json.rea.backup:8` (both `"rea-agents@6.4.0"`) — consistent with an upgrade path 6.4.0→6.5.0 for those clients.
9. Repo-side staleness sweep: `grep -n '6\.[457]\.0'` across repo — `LOG.md` has 0 occurrences of `6.7.0`; MINT.md:10, SKILL.md:12,19-20, SCORECARD.md:58,291 still say Kimi 6.4.0 (`SCORECARD.md:291` even cites `~/.kimi-code/config.toml:1478`). SKILL.md:12 self-labels its 6.4.0 mention "historical, verified 2026-10-13".

## Text for parent to land VERBATIM

```text
REA pin census 2026-10-18 (read-only, SC2 scout): configured pins are Devin `rea-agents@6.5.0` (`/home/vgpnk/.config/devin/mcp_config.json:7`, key `mcpServers.rea.args[1]`) and OMP `rea-agents@6.5.0` (`/home/vgpnk/.omp/agent/mcp.json:8`, same key path, plus key `mcpServers.rea.type`) — both corroborate PROVINCE.md:16-17 byte-for-byte. Kimi is REFUTED: PROVINCE.md:10 and :18 claim `rea-agents@6.4.0` at `config.toml:1478`, but the file's only `rea-agents` occurrence is `rea-agents@6.7.0` at `:2940` (table `[mcp_servers.rea]` :2938; env `[mcp_servers.rea.env]` :2943), and `:1478` now reads `model = "kimi-k3"` in a models table. Both 2026-10-18 config.toml backups already carry 6.7.0 (`config.toml.20261018-085645.bak:2915`, `config.toml.20261018-114557.bak:2932`) and a 6.7.0 npx cache exists (`/home/vgpnk/.npm/_npx/a1722018f28f9df2`), so the drift predates this wave (window: after 2026-10-16 reverify, at/before 2026-10-18 08:56:45). Zero drift across the wave window: current sha256 of all three configs equals `.ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt:2-4` — devin `16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4`, omp `38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b`, kimi `3546e033aeaf68093faf4099ea8289de5dea7ec224e7c557f08bfa9d51cf9a2a`.
```

## Conclusions by label

- **Observation** — (a) pin values/lines exactly as in the table/verdict (two independent sha256 checks + two greps this session); (b) PROVINCE.md:18's Kimi pointer `:1478` holds `model = "kimi-k3"` and the only pin is `:2940` = 6.7.0; (c) both 2026-10-18 backups already carried 6.7.0; (d) current sha256s == pre-pair receipt (lines 2-4) for all three files; (e) 6.7.0 npx cache `a1722018f28f9df2` exists; (f) devin/omp config mtimes 2026-10-14, kimi config.toml mtime 2026-10-18 11:45:57; (g) repo files (LOG.md 0 hits of 6.7.0; MINT/SKILL/SCORECARD still 6.4.0) contain no record of the Kimi 6.7.0 pin.
- **Inference** — PROVINCE.md:10's "Kimi uses `rea-agents@6.4.0` (170 MCP tools + 127 CLI commands)" and :18's drift-prone pointer no longer describe the configured Kimi surface; if Kimi spawns REA from this config it now resolves 6.7.0, so the 6.4.0 tool counts (170/127, tools_sha256 25802f6d…) should be treated as historical until a 6.7.0 catalog is probed. Live-load behavior was not probed (read-only seat; live probes are battery seats' scope).
- **Unknown** — exact drift date (bounded after 2026-10-16 reverify, at/before 2026-10-18 08:56:45); whether the 11:45:57 config.toml edit touched anything related (pin line identical in both backups → pin value unchanged); 6.7.0 catalog tool counts / `tools_sha256` (not probed); whether the live Kimi client actually loads this pin.

## Scope compliance

Read-only on all repo and home files; no git; no network; no config edits; no secret values printed (only pins, key names, hashes). Only write: this report.
