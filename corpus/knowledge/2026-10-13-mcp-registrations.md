<!-- corpus entry — kaidoku-shokunin round 1 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r1/04-mcp-config.md. Each candidate's `suggested:` field is its curation verdict; `reject` rows are retained calibration entries. -->

# kaidoku-r1 — REA MCP registration surface (this host)

Scope: which MCP clients on this host have the `rea` server registered, the exact
launch command/args/env, and which clients are not registered. Read-only survey;
no client config was modified.

## Candidate: Exactly three client files register REA — omp, devin, kimi — all pinned to `npx -y rea-agents@6.4.0 mcp` with identical env
- claim: `~/.omp/agent/mcp.json`, `~/.config/devin/mcp_config.json`, and `~/.kimi-code/config.toml` each define a server named `rea` launching `npx` with args `["-y","rea-agents@6.4.0","mcp"]` and env `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` + `JAVA_HOME=/usr/lib/jvm/java-21-openjdk`; no other MCP server is defined in any of the three files.
- source: ~/.omp/agent/mcp.json lines 1-17; ~/.config/devin/mcp_config.json lines 1-16; ~/.kimi-code/config.toml lines 1285-1292
- verify: `cat ~/.omp/agent/mcp.json ~/.config/devin/mcp_config.json; sed -n '1285,1293p' ~/.kimi-code/config.toml`
- verified-at: 2026-10-13
- suggested: admit — byte-identical command/args/env across three independent files; directly falsifiable.

## Candidate: Per-client config path and dialect differ; devin omits `type`, kimi adds `startup_timeout_sec`
- claim: omp uses a standalone JSON file `~/.omp/agent/mcp.json` with an explicit `"type": "stdio"`; devin uses `~/.config/devin/mcp_config.json` with no `type` key at all (stdio inferred from `command`); kimi uses a TOML table `[mcp_servers.rea]` inside its monolithic `~/.kimi-code/config.toml` and adds `startup_timeout_sec = 30` — a timeout knob the two JSON registrations do not carry.
- source: same three files; ~/.config/devin/mcp_config.json has 16 lines and no `type`; ~/.kimi-code/config.toml line 1288
- verify: `grep -c '"type"' ~/.config/devin/mcp_config.json ~/.omp/agent/mcp.json; grep -n 'startup_timeout_sec' ~/.kimi-code/config.toml`
- verified-at: 2026-10-13
- suggested: admit — per-host registration mechanics: three dialects (JSON+type, JSON bare, TOML table) for one server shape.

## Candidate: omp's routing authority `~/.omp/agent/config.yml` contains zero MCP keys — registration lives only in the sibling `mcp.json`
- claim: `grep -i 'mcp' ~/.omp/agent/config.yml` returns nothing; the 26 KiB config.yml (seats, fallback chains, budgets) has no `mcp`, `mcpServers`, `rea`, or `ghidra` entry, so omp discovers the REA server solely from `~/.omp/agent/mcp.json`.
- source: `grep -rn -i 'rea-agents\|ghidra\|"rea"\|mcpServers\|mcp_servers' ~/.omp/agent/config.yml` (no output); `ls -la ~/.omp/agent/` shows `mcp.json` beside `config.yml`
- verify: `grep -ni 'mcp\|rea\|ghidra' ~/.omp/agent/config.yml | wc -l` → 0
- verified-at: 2026-10-13
- suggested: admit — establishes that on this host omp MCP registration is file-adjacent auto-discovery, not config-key-driven.

## Candidate: `mcp.json.rea.backup` is a same-second snapshot lacking the `env` block — env vars were grafted onto a prior env-less registration
- claim: `~/.omp/agent/mcp.json.rea.backup` (mtime 2026-10-12 09:51:27.598) is identical to `mcp.json` (mtime 2026-10-12 09:51:27.599 — one millisecond later) except it has no `env` key; the diff is exactly the `GHIDRA_INSTALL_DIR`/`JAVA_HOME` block, matching the skill-documented `rea setup` behavior of writing a backup before mutating registration.
- source: `stat -c '%y %n' ~/.omp/agent/mcp.json*`; `diff ~/.omp/agent/mcp.json.rea.backup ~/.omp/agent/mcp.json`
- verify: `diff ~/.omp/agent/mcp.json.rea.backup ~/.omp/agent/mcp.json`
- verified-at: 2026-10-13
- suggested: admit — explains both the registration tool's backup convention (`<file>.rea.backup`) and when env binding landed (2026-10-12, a day before the devin file's 2026-10-13 11:29 mtime).

## Candidate: codex, opencode, claude are installed but NOT registered; cursor and grok are not installed
- claim: codex (`~/.local/bin/codex`) has `~/.codex/` containing only `skills/omarchy` — no `config.toml`, hence no `[mcp_servers.rea]`; opencode (`~/.opencode/bin/opencode`) has `~/.config/opencode/opencode.json` carrying only `$schema`/`theme`/`autoupdate` — no `mcp` key; claude (`/usr/bin/claude`, outside the seven surfaces) has `~/.claude.json` = `{"mcpServers": {}}` — explicitly empty; `cursor`/`cursor-agent` and `grok` are absent from PATH and `~/.cursor` does not exist (`~/.grok` holds only agents/skills dirs), so neither can hold a local registration.
- source: `command -v` sweep; `find ~/.codex -maxdepth 2`; `cat ~/.config/opencode/opencode.json`; `cat ~/.claude.json`; `ls ~/.cursor` → No such file
- verify: `for c in codex opencode claude cursor cursor-agent grok; do command -v $c; done; ls ~/.codex/config.toml ~/.cursor/mcp.json 2>&1`
- verified-at: 2026-10-13
- suggested: admit — distinguishes "installed but unregistered" (codex, opencode) from "unregistrable on this host" (cursor, grok CLI).

## Candidate: Of the seven supported native surfaces, exactly 3/7 are REA-registered (omp, devin, kimi) and 2/7 are registered-capable but unregistered (codex, opencode)
- claim: mapping registrations onto the contract's seven surfaces — omp ✅, devin ✅, kimi ✅ (via `~/.kimi-code/`, not `~/.kimi/`), codex ❌, opencode ❌, cursor ❌ (client absent), grok ❌ (client absent); the skill's client-ID list (`claude_code, claude_desktop, codex, cursor, gemini_cli, windsurf, devin, opencode, antigravity, copilot_cli, commandcode, qwen_code, vscode, grok_build, omp, pi, hermes, grok_bot`) covers all installed-but-unregistered ones except that `grok_bot` uses a chat registration step rather than a local `mcp.json`.
- source: registration files above + ~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md lines 46-51
- verify: `grep -n 'grok_bot\|client.*ID\|claude_code' ~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md`
- verified-at: 2026-10-13
- suggested: admit — the fleet-relevant coverage matrix; kimi's real config root (`~/.kimi-code/config.toml`, not `~/.kimi/`) is the non-obvious part.

## Candidate: The launch command is npx-ephemeral — no `rea` CLI on PATH, no global install; both npx caches resolve to 6.4.0
- claim: `command -v rea` finds nothing and `npm ls -g` lists no rea-agents; the registered command depends on npx fetching at spawn, but `~/.npm/_npx/` already holds two caches — one keyed `rea-agents@latest` (af752b90…), one keyed `rea-agents@6.4.0` (dea94757…) — both materialized at version 6.4.0, so the pinned launch resolves offline; `npm view rea-agents version` returns `6.4.0`, i.e. the pin equals the newest published release.
- source: `command -v rea` (empty); `cat ~/.npm/_npx/{af752b90495482d7,dea9475797100b20}/package.json`; `npm view rea-agents version`
- verify: `command -v rea; ls ~/.npm/_npx/*/node_modules/rea-agents/package.json; npm view rea-agents version`
- verified-at: 2026-10-13
- suggested: admit — registration is a pinned npx invocation, not an installed binary; cache evidence shows it has already spawned at least twice (latest + pinned forms).

## Candidate: Both env paths exist and predate registration; no REA-side Ghidra extension is installed — registration is client-file-only
- claim: `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` (dir mtime Sep 21) and `JAVA_HOME=/usr/lib/jvm/java-21-openjdk` both exist; `~/.config/ghidra/ghidra_12.1.4_PUBLIC/Extensions/` contains only `ghidra-emotionengine-reloaded` — no REA component — so the MCP registration needs no Ghidra-side plugin on this host.
- source: `ls -ld` on both paths; `ls ~/.config/ghidra/ghidra_12.1.4_PUBLIC/Extensions/`
- verify: `ls -ld ~/.local/opt/ghidra_12.1.4_PUBLIC /usr/lib/jvm/java-21-openjdk; ls ~/.config/ghidra/ghidra_12.1.4_PUBLIC/Extensions/`
- verified-at: 2026-10-13
- suggested: admit — separates the two registration halves: client file (present) vs engine-side extension (absent and apparently unneeded).

## Candidate: Registration depends on the client's PATH resolving `npx`, which on this host is a session-scoped fnm shim
- claim: `which npx` resolves to `/run/user/1000/fnm_multishells/29144_1791904066708/bin/npx` — an fnm multishell path under `/run/user/1000` that exists only for shells with fnm initialized (node v24.21.0, fnm default); any client process launched outside that environment (systemd unit, bare desktop session, non-login shell) would fail to spawn the registered server despite a correct config.
- source: `which npx node` output; `cat ~/.local/share/fnm/aliases/default` → v24.21.0
- verify: `which npx; readlink -f $(which npx)`
- verified-at: 2026-10-13
- suggested: admit — names the one host-specific fragility in an otherwise uniform registration; matches the skill's warning that a missing `rea`/Node in a child shell does not imply broken registration (connection-and-recovery.md line 21).

## Candidate: Supported repair path is per-client `rea doctor`/`rea setup` with dry-run + backup — not hand-editing
- claim: connection-and-recovery.md prescribes `rea doctor --client <id> --json` then `rea setup --client <id> --dry-run --json` (apply with `--yes`), showing exact paths/backups first; a skill install alone never registers MCP (SKILL.md line 19); codex additionally supports per-tool approval tables like `[mcp_servers.rea.tools.open_binary] approval_mode = "approve"`.
- source: ~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md lines 16-17, 39-59, 80-89; SKILL.md line 19
- verify: `sed -n '39,59p' ~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md`
- verified-at: 2026-10-13
- suggested: admit — codifies how the three existing files were likely produced (the `.rea.backup` artifact is the fingerprint) and how the missing codex/opencode registrations should be added if ever authorized.

## Summary
REA is registered for 3 of 7 surfaces (omp via `~/.omp/agent/mcp.json`, devin via `~/.config/devin/mcp_config.json`, kimi via `~/.kimi-code/config.toml`), all launching pinned `npx -y rea-agents@6.4.0 mcp` with `GHIDRA_INSTALL_DIR`/`JAVA_HOME`; codex and opencode are installed but unregistered, cursor and grok are not installed, and the only fragility is npx resolving through a session-scoped fnm shim.
