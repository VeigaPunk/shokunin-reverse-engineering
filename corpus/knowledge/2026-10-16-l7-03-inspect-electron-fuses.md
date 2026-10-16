# inspect_electron_fuses — nine-fuse sentinel on a pinned Signal ELF

source: `.ufo/waves/luna-round-6/receipts/leg-5.md:3-12`; `.ufo/waves/luna-round-6/receipts-B/leg-5.md:8-10,24-52`
verified-at: 2026-10-16
recheck: `cd /tmp && timeout 240 npx -y rea-agents@6.5.0 inspect-electron-fuses /usr/lib/signal-desktop/signal-desktop --format json`; expect evidence `ev_36045c43ecbed14e3eb3b77a720c24c115cc2377737d2ed2fe8acce76a4288ed`, carrier `f7a9b441e825b388260430f9edd9a2f94fd50be497bf66192a16aeab87afc85a`, one complete v1 sentinel at offset 35,260,752, nine fuse states.

REA pin: `rea-agents@6.5.0`; provider `electron-fuses` v1; confidence `observed`; RESULT, exit 0.

Carrier: `/usr/lib/signal-desktop/signal-desktop`, SHA-256 `f7a9b441e825b388260430f9edd9a2f94fd50be497bf66192a16aeab87afc85a` (223,513,856 bytes, ELF x86-64).
Round-6 call: `cd /tmp && timeout 240 npx -y rea-agents@6.5.0 inspect-electron-fuses /usr/lib/signal-desktop/signal-desktop --format json`; Evidence ID `ev_36045c43ecbed14e3eb3b77a720c24c115cc2377737d2ed2fe8acce76a4288ed`.

- **Observation:** One slice (223,513,856 bytes) contains one complete v1 sentinel at offset 35,260,752 (`wire_version` 1, `declared_length` 9) reporting: RunAsNode=disabled (48), EnableCookieEncryption=enabled (49), EnableNodeOptionsEnvironmentVariable=disabled (48), EnableNodeCliInspectArguments=disabled (48), EnableEmbeddedAsarIntegrityValidation=disabled (48), OnlyLoadAppFromAsar=enabled (49), LoadBrowserProcessSpecificV8Snapshot=disabled (48), GrantFileProtocolExtraPrivileges=enabled (49), WasmTrapHandlers=enabled (49) — raw_byte values in parentheses (`receipts/leg-5.md:8`).
- **Observation (lane B):** An independent run reported the same carrier digest, Evidence ID, and nine-state fingerprint (`receipts-B/leg-5.md:8,48-52`).
- **Inference (REA-derived, not runtime-observed):** The result's derived implications are that Node CLI inspect and RunAsNode are not honored, embedded ASAR integrity validation is unknown, and app loading is restricted to the app ASAR (`receipts/leg-5.md:8`).
- **Unknown / limitations (tool-reported):** "Fuse state does not prove the application enables Inspector through other means, such as app.commandLine or a remote-debugging switch in application code." "A missing sentinel means fuse state is unknown, not that every fuse is disabled." "Electron compiles embedded ASAR integrity validation only on macOS and Windows; the observed fuse byte at file offset 35260752 does not establish enforcement." "The selected file is admitted as one regular file of at most 1 GiB. Sentinel search uses 262144-byte windows, and each slice keeps at most 32 sentinels." One Linux carrier/slice only; RESULT-class exercise, no Core promotion.

Sources: `.ufo/waves/luna-round-6/receipts/leg-5.md:3-12`; `.ufo/waves/luna-round-6/receipts-B/leg-5.md:8,48-52`; carrier `.ufo/waves/luna-round-6/SC3.md:10`.
