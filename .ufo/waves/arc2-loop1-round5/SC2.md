# SC2 — round-5 config pin corroboration

**Verdict — CONFIRMED:** Round-5 pre-pair receipt matches the round-4 post-pair payload byte-for-byte, and all five current custody paths pass its hashes (5/5, rc=0). Current pins are Devin `rea-agents@6.5.0`, OMP `rea-agents@6.5.0`, and Kimi `rea-agents@6.7.0`; Kimi's stanza anchor is `[mcp_servers.rea]` at line 3155, pin at 3157, and env-table anchor at 3160. No custody-path content or metadata churn is observed after the round-4 post-pair timestamp, 2026-10-18T19:44:52Z.

## Evidence

Receipt pointers: round-4 post-pair, `.ufo/waves/arc2-loop1-round4/receipts/config-post-pair.txt:1-6`; round-5 pre-pair, `.ufo/waves/arc2-loop1-round5/receipts/config-pre-pair.txt:1-6`. Their timestamps are respectively `2026-10-18T19:44:52Z` and `2026-10-18T19:50:16Z`. Round-4's in-window rewrite record says Kimi config changed to file hash `e0634d8c…`, 3181 lines, stanza line 3155 and pin line 3157 while the REA stanza stayed byte-identical: `.ufo/waves/arc2-loop1-round4/receipts/drift-config-toml-20261018T191721Z.txt:1-3`.

Commands run and observed output excerpts:

```
$ tail -n +2 .ufo/waves/arc2-loop1-round5/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
# exit status 0 (5/5)

$ if cmp -s <(tail -n +2 .ufo/waves/arc2-loop1-round4/receipts/config-post-pair.txt) <(tail -n +2 .ufo/waves/arc2-loop1-round5/receipts/config-pre-pair.txt); then printf 'payload-identical rc=0\n'; else printf 'payload-differs rc=1\n'; fi
payload-identical rc=0

$ sha256sum /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json
e0634d8c5335aaf013bac5d4e45e4cfb513021f5fa027f36b5ad227324aa1c20  /home/vgpnk/.kimi-code/config.toml
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  /home/vgpnk/.omp/agent/mcp.json

$ python -c 'from pathlib import Path
for p in (Path("/home/vgpnk/.config/devin/mcp_config.json"), Path("/home/vgpnk/.omp/agent/mcp.json"), Path("/home/vgpnk/.kimi-code/config.toml")):
    for n, line in enumerate(p.read_text().splitlines(), 1):
        if "rea-agents@" in line or line.strip() in ("[mcp_servers.rea]", "[mcp_servers.rea.env]"):
            print(f"{p}:{n}:{line.strip()}")'
/home/vgpnk/.config/devin/mcp_config.json:7:"rea-agents@6.5.0",
/home/vgpnk/.omp/agent/mcp.json:8:"rea-agents@6.5.0",
/home/vgpnk/.kimi-code/config.toml:3155:[mcp_servers.rea]
/home/vgpnk/.kimi-code/config.toml:3157:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
/home/vgpnk/.kimi-code/config.toml:3160:[mcp_servers.rea.env]

$ sed -n '/^\[mcp_servers\.rea\]$/,/^$/p' /home/vgpnk/.kimi-code/config.toml | sha256sum
3751281c2a379b04d303df21a32a2936b0e2dd782bd710cead4c59a2e1643528  -

$ stat -c 'mtime=%y ctime=%z ino=%i size=%s %n' /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.bashrc /home/vgpnk/.profile
mtime=2026-10-14 17:53:20.395671586 -0300 ctime=2026-10-14 17:53:20.395671586 -0300 ino=11341318 size=406 /home/vgpnk/.config/devin/mcp_config.json
mtime=2026-10-14 17:53:20.392671581 -0300 ctime=2026-10-14 17:53:20.393671583 -0300 ino=11341316 size=429 /home/vgpnk/.omp/agent/mcp.json
mtime=2026-10-18 16:17:21.801598268 -0300 ctime=2026-10-18 16:17:46.601691565 -0300 ino=31684890 size=102426 /home/vgpnk/.kimi-code/config.toml
mtime=2026-10-16 13:33:16.272618342 -0300 ctime=2026-10-16 13:33:16.272618342 -0300 ino=25991953 size=3601 /home/vgpnk/.bashrc
mtime=2026-10-15 03:12:07.440808802 -0300 ctime=2026-10-15 03:12:07.440808802 -0300 ino=40274 size=736 /home/vgpnk/.profile
```

The live file locations are `.config/devin/mcp_config.json:7`, `.omp/agent/mcp.json:8`, and `.kimi-code/config.toml:3155,3157,3160` (absolute paths as shown in command output). The Kimi stanza digest reproduces the round-4 SC2 canonical digest (`3751281c2a379b04…`), previously recorded at `.ufo/waves/arc2-loop1-round4/SC2.md:90-98`.

## Text for parent to land verbatim

```text
REA pin corroboration, round 5 (SC2, read-only): the round-5 pre-pair receipt (2026-10-18T19:50:16Z) verifies all five custody paths (sha256sum -c, 5/5, rc=0), and its five hash lines are byte-identical to the round-4 post-pair receipt (2026-10-18T19:44:52Z). Current pins: Devin rea-agents@6.5.0 (/home/vgpnk/.config/devin/mcp_config.json:7), OMP rea-agents@6.5.0 (/home/vgpnk/.omp/agent/mcp.json:8), Kimi rea-agents@6.7.0 (/home/vgpnk/.kimi-code/config.toml:3157); Kimi stanza anchor [mcp_servers.rea] :3155 and env anchor :3160. The current Kimi file hash is e0634d8c5335aaf013bac5d4e45e4cfb513021f5fa027f36b5ad227324aa1c20, matching both receipt payloads; the canonical stanza digest is 3751281c2a379b04d303df21a32a2936b0e2dd782bd710cead4c59a2e1643528. No custody-path content or metadata churn is observed after the round-4 post-pair timestamp: all five current hashes pass, and every listed ctime predates 19:44:52Z (Kimi ctime 2026-10-18T19:17:46.601Z).
```

## Conclusions by label

- **Observation** — The round-4 post-pair and round-5 pre-pair hash payloads compare identical; all five current paths verify against the round-5 receipt. Current three client pins and Kimi stanza anchors are as stated above. Kimi's current file hash equals the receipt's `e0634d8c…`; its ctime is 19:17:46.601Z, earlier than the post-pair receipt. The canonical stanza digest matches the round-4 reference.
- **Inference** — There is no evidence of custody-path churn between the 19:44:52Z round-4 post-pair and this 19:50:16Z round-5 pre-pair. The round-4 rewrite documented at 19:17Z predates that interval; round 5 re-baselines the same endpoint bytes.
- **Unknown** — These file/hash checks establish configured pins, not which versions a client process loaded at runtime. No runtime probes were performed.

## Scope

Read-only on all source/config paths; only versions, key/table anchors, hashes, and file metadata were emitted. No secrets printed; no config edits, installs, network access, or git mutations. This report is the sole write.
