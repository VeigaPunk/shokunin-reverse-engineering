# SC2 — round-6 config pin corroboration

**Verdict — CONFIRMED:** Round-6 pre-pair receipt verifies all five custody paths (5/5, rc=0). Its five hash lines are byte-identical to the round-5 post-pair payload. Current pins: Devin `rea-agents@6.5.0`, OMP `rea-agents@6.5.0`, Kimi `rea-agents@6.7.0` (stanza `[mcp_servers.rea]` :3155, pin :3157, env :3160). No custody-path content or metadata churn after the round-5 post-pair timestamp `2026-10-18T20:35:25Z`.

## Evidence

Receipt pointers: round-5 post-pair `.ufo/waves/arc2-loop1-round5/receipts/config-post-pair.txt:1-6` (`2026-10-18T20:35:25Z`); round-6 pre-pair `.ufo/waves/arc2-loop1-round6/receipts/config-pre-pair.txt:1-6` (`2026-10-18T20:39:12Z`). Live pins: `/home/vgpnk/.config/devin/mcp_config.json:7`, `/home/vgpnk/.omp/agent/mcp.json:8`, `/home/vgpnk/.kimi-code/config.toml:3155,3157,3160`.

Commands (cwd repo; capture `2026-10-18T20:44:07Z`, recheck `20:44:21Z`):

```
$ tail -n +2 .ufo/waves/arc2-loop1-round6/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
# rc=0 (5/5); recheck at 20:44:21Z also rc=0

$ if cmp -s <(tail -n +2 .ufo/waves/arc2-loop1-round5/receipts/config-post-pair.txt) <(tail -n +2 .ufo/waves/arc2-loop1-round6/receipts/config-pre-pair.txt); then printf 'payload-identical rc=0\n'; fi
payload-identical rc=0

$ sha256sum /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json
e0634d8c5335aaf013bac5d4e45e4cfb513021f5fa027f36b5ad227324aa1c20  /home/vgpnk/.kimi-code/config.toml
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  /home/vgpnk/.omp/agent/mcp.json

$ sed -n '/^\[mcp_servers\.rea\]$/,/^$/p' /home/vgpnk/.kimi-code/config.toml | sha256sum
3751281c2a379b04d303df21a32a2936b0e2dd782bd710cead4c59a2e1643528  -

$ stat -c 'mtime=%y ctime=%z ino=%i size=%s %n' <five custody paths>
devin mcp_config.json  mtime=ctime=2026-10-14 17:53:20.395671586 -0300 ino=11341318 size=406
omp mcp.json           mtime=2026-10-14 17:53:20.392671581 -0300 ctime=…393671583 ino=11341316 size=429
kimi config.toml       mtime=2026-10-18 16:17:21.801598268 -0300 ctime=2026-10-18 16:17:46.601691565 -0300 ino=31684890 size=102426
.bashrc                mtime=ctime=2026-10-16 13:33:16.272618342 -0300 ino=25991953 size=3601
.profile               mtime=ctime=2026-10-15 03:12:07.440808802 -0300 ino=40274 size=736
```

Key/version census (values redacted except version pins and non-secret command tokens):

- Devin `:3` `"rea"`, `:7` `"rea-agents@6.5.0"`; keys `command=npx`, `args=["-y","rea-agents@6.5.0","mcp"]`, `env` keys `GHIDRA_INSTALL_DIR`, `JAVA_HOME`, `REA_JADX_MCP_JAR` (values not printed).
- OMP `:3` `"rea"`, `:8` `"rea-agents@6.5.0"`; keys `type=stdio`, `command=npx`, same args pin, same three env keys (values not printed).
- Kimi 3181 lines: `:3155 [mcp_servers.rea]`, `:3156 command=npx`, `:3157 args=["-y","rea-agents@6.7.0","mcp"]`, `:3158 startup_timeout_sec=30`, `:3160 [mcp_servers.rea.env]`, env keys `GHIDRA_INSTALL_DIR`, `JAVA_HOME` (values not printed). Word-boundary `rea` footprint is those three lines only.
- Non-custody bonus: `~/.grok/config.toml:30` `"rea-agents@6.5.0"`; `~/.codex/config.toml` 0 `rea-agents` hits. Not in the five-path receipt.
- Stanza digest `3751281c2a379b04…` matches round-5 SC2 (`.ufo/waves/arc2-loop1-round5/SC2.md:39-50`). Kimi file hash `e0634d8c…` matches both receipt payloads. HEAD `54bc9dd`.

## Text for parent to land verbatim

```text
REA pin corroboration, round 6 (SC2, read-only): the round-6 pre-pair receipt (2026-10-18T20:39:12Z, .ufo/waves/arc2-loop1-round6/receipts/config-pre-pair.txt) verifies all five custody paths (sha256sum -c, 5/5, rc=0 at 20:44:07Z and recheck 20:44:21Z), and its five hash lines are byte-identical to the round-5 post-pair receipt (2026-10-18T20:35:25Z). Current pins: Devin rea-agents@6.5.0 (/home/vgpnk/.config/devin/mcp_config.json:7), OMP rea-agents@6.5.0 (/home/vgpnk/.omp/agent/mcp.json:8), Kimi rea-agents@6.7.0 (/home/vgpnk/.kimi-code/config.toml:3157); Kimi stanza anchor [mcp_servers.rea] :3155 and env anchor :3160. Kimi file hash e0634d8c5335aaf013bac5d4e45e4cfb513021f5fa027f36b5ad227324aa1c20 matches both receipt payloads; canonical stanza digest 3751281c2a379b04d303df21a32a2936b0e2dd782bd710cead4c59a2e1643528. No custody-path content or metadata churn after the round-5 post-pair timestamp: all five hashes pass, and every listed ctime predates 20:35:25Z (Kimi ctime 2026-10-18T19:17:46.601Z).
```

## Conclusions by label

- **Observation** — Round-5 post-pair and round-6 pre-pair hash payloads compare identical; all five current paths verify against the round-6 receipt (twice). Pins and Kimi anchors are as stated. Kimi ctime 19:17:46.601Z is earlier than 20:35:25Z. Stanza digest matches the round-5 reference.
- **Inference** — No custody-path churn between the 20:35:25Z round-5 post-pair and this 20:39:12Z round-6 pre-pair, nor through the 20:44:21Z recheck. Round 6 re-baselines the same endpoint bytes.
- **Unknown** — File/hash checks establish configured pins, not which versions a client process loaded at runtime. No runtime probes were performed.

## Scope

Read-only on all source/config paths; only versions, key/table anchors, hashes, and file metadata were emitted. No secrets printed; no config edits, installs, network access, or git mutations. This report is the sole write.
