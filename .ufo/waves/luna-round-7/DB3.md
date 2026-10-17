# DB3 — content derivability for entry 3 (`inspect-electron-fuses`, leg-5)

## CLAIM
Every content element of entry 3 is derivable from the tracked leg-5 receipts at HEAD `411175e`; the substance is exact, but six of nine fuse names in `E3D.md:8` are shortened, and integration must use provider-exact names, the mandated metadata header, and hyphenated row stems.

## METHOD
Read-only: `git show HEAD:.ufo/waves/luna-round-6/receipts/leg-5.md` — line 8 parsed with `jq` (digest, bytes, sentinel, 9 fuses, implications, limitations); `git show HEAD:...receipts-B/leg-5.md` (:8, :28, :48-52); Python diff of E3D:8 names vs `receipt.fuses[].name` (result: six shortened). Read `E3D.md:2,8`, `M1.md:13`, `K3.md:10`, SC3, CC5, E3V, G3, Z3, `SCORECARD.md:101`. No probe/network. SC3/CC5/E3D/M1/K3 are untracked (`git cat-file -e` fails); the receipts are the durable anchor.

## FINDINGS
- Carrier `/usr/lib/signal-desktop/signal-desktop`, SHA-256 `f7a9b441e825b388260430f9edd9a2f94fd50be497bf66192a16aeab87afc85a`, 223,513,856 B; call `npx -y rea-agents@6.5.0 inspect-electron-fuses … --format json`, exit 0 (`receipts/leg-5.md:3,8,11`); lane-B MCP 6.5.0 reproduces the digest and Evidence `ev_36045c43ecbed14e3eb3b77a720c24c115cc2377737d2ed2fe8acce76a4288ed` (`receipts-B/leg-5.md:8,16,28`).
- Sentinel at 35260752, wire 1, declared 9, `complete:true`; states RunAsNode disabled(48), EnableCookieEncryption enabled(49), EnableNodeOptionsEnvironmentVariable disabled(48), EnableNodeCliInspectArguments disabled(48), EnableEmbeddedAsarIntegrityValidation disabled(48), OnlyLoadAppFromAsar enabled(49), LoadBrowserProcessSpecificV8Snapshot disabled(48), GrantFileProtocolExtraPrivileges enabled(49), WasmTrapHandlers enabled(49) (`receipts/leg-5.md:8`; lane-B fingerprint `receipts-B/leg-5.md:50-52`).
- Implications are `derivation`, not runtime observation: node_cli_inspect_arguments `not_honored`, electron_run_as_node `not_honored`, embedded_asar_integrity_validation `unknown`, only_load_app_from_asar `restricted_to_app_asar`; four static-only limitations (`receipts/leg-5.md:8`).
- Corrections: (1) `E3D.md:8` shortens six names—`CookieEncryption`, `NodeOptions`, `NodeCliInspectArguments`, `EmbeddedAsarIntegrityValidation`, `BrowserProcessSpecificV8Snapshot`, `FileProtocolExtraPrivileges`—use the exact spellings above. (2) Header: `source: .ufo/waves/luna-round-6/receipts/leg-5.md:3-12; .ufo/waves/luna-round-6/receipts-B/leg-5.md:8,24-52` / `verified-at: 2026-10-16` / `recheck: repeat inspect_electron_fuses on the pinned path+hash; compare Evidence ID, offset 35260752, nine states`. (3) `M1.md:13`/`K3.md:10` tokens use `inspect_electron_fuses`; Command A's map regex `2026-10-\d{2}-[a-z0-9-]+` (`SCORECARD.md:101`) skips `_`—use `2026-10-16-l7-03-inspect-electron-fuses`.

## THREATS
Receipt review, not re-execution; one Linux carrier/slice; SC3/CC5 are untracked auxiliaries; E3V.md:10/G3.md:10 cite `E3D.md:12-26` (current file ends :14). Row edits, Command A post-state, and the 78/78 claim are other seats' scope. No Core-promotion claim.

## VERDICT
FINDING: content is derivable and correctly RESULT-scoped; apply the provider-exact names plus rulings (a)/(d) before integration.
