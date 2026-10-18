# SC1 (scout) — host surface census: 6.7.0 cache contents, offline npx resolution, ghidra/java unchanged; E2 inventory corroborated

Wave arc2-loop1-round2 · Seat SC1 · 2026-10-18 · read-only census (only write: this report). No secret/credential values printed anywhere — only version strings, line numbers, key names, file counts, and sha256 digests. Scratch: `/tmp/arc2-l2r2-SC1-scratch/` only.

## Verdict

**PASS — 6.7.0 cache complete and offline-resolvable; E2's inventory corroborated independently, and the 6.7.0 counts E2 left unprobed are now resolved (207 MCP tools / 153 CLI commands / 6 prompts).** The cache at `~/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents` is a complete shipped artifact: `package.json` version `6.7.0` (`:4`), `dist/` present (1699 files), `skills/reverse-engineer-anything/` present (7 files, frontmatter v42/207), plus `bridge/`, `scripts/`, `native/windows/`, `third_party/`, `licenses/` (19 files). `npx --offline rea-agents@6.7.0 --version` → `6.7.0` (pure cache hit; log line `cache hit`); plain (non-`--offline`) `npx` performs a **network revalidation** (`fetch GET 200 … cache revalidated`) — the offline guarantee belongs to `--offline` specifically. Ghidra 12.1.4, JDK 21.0.12.1 and `/usr/lib/libjq.so.1.0.4` (`7e8bccc6…`) are unchanged from round 1. Three findings beyond E2: (1) a 6.7.0-only `dist/recordedCatalogDigests.js` whose `tools_sha256 af39310c…` is confirmed **live** by `doctor`'s identity block, not just read from the file; (2) `doctor` on 6.7.0 exposes **two rea registrations outside PROVINCE.md's three-config surface** — `~/.grok/config.toml:30` pins `rea-agents@6.5.0` (`stale`) and `~/.codex/config.toml:77` pins the 6.5.0 cache's **absolute** `.bin/rea` path (`stale`); (3) `doctor` checks Kimi at `~/.kimi-code/mcp.json` (no rea entry → `missing`), not at the `config.toml` that actually carries the pin — the doctor's client census and the pin census measure different surfaces.

## Evidence — commands run THIS session with observed output excerpts

Session stamps: `date -u` → `2026-10-18T16:59:24Z` (first), `2026-10-18T17:04:05Z` (last). HEAD `165057e36f558c95eb02bf24de4a874d559d6950`; `git status --porcelain` → `?? .ufo/waves/arc2-loop1-round2/` only.

### 1. 6.7.0 cache identity and contents

```
$ cat ~/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/package.json | head -8
{
  "name": "rea-agents",
  "mcpName": "io.github.morluto/rea",
  "version": "6.7.0",
  "description": "Reverse engineer anything from your terminal or agent with one CLI and MCP server.",
  ...
$ ls -la ~/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents
bridge/  DISCLAIMER.md  dist/  install.sh  LICENSE  licenses/  native/  package.json
README.md  scripts/  skills/  third_party/  THIRD_PARTY_NOTICES.md
$ find dist -type f | wc -l          → 1699
$ find . -type f | wc -l             → 1775   (whole package)
$ find skills -type f                → SKILL.md + references/{android-applications,connection-and-recovery,
                                       evidence-workflows,javascript-applications,native-and-artifacts,
                                       runtime-observation}.md   (7 files)
$ head -10 skills/reverse-engineer-anything/SKILL.md
metadata:
  version: "42"
  tool_count: 207
```

Whole-package digest (files sorted by path, sha256sum piped to sha256sum), **stable across three checks** (17:00:24Z, 17:03Z, 17:04:05Z):

```
8f4eba1f72e2c63d6800f734630233b7ffe747a4e8863c1ec1be4e7c95e8009e  -   # 6.7.0 whole package
7d86d47b4d571ed911dd7becfab71948b912048231d2ab0a427e810d8d01fa5c  -   # 6.7.0 dist/ only
```

`package.json:4` = `"version": "6.7.0"` (verified `grep -n '"version"'`). `engines` at `:44-46` requires node `^22.19.0 || ^24.11.0 || >=26.0.0`; host node is `v26.12.0` (satisfies).

### 2. Static catalog counts — node import (resolves E2's "counts unprobed")

```
$ node --input-type=module -e "const t = await import('file://…/a1722018f28f9df2/node_modules/rea-agents/dist/contracts/toolContracts.js'); …"
TOOL_CONTRACTS length: 207
CLI_COMMANDS keys: 153
digests: {"tools_sha256":"af39310c9591bb981893ec0d2188b1bcf6e9cc8ba3ac513d5bbefc8ddcb85639",
          "prompts_sha256":"7152916ab48bd2a9677a5ad9cdbde0a51dc53c113934952ad096e93f5f18aa7e",
          "combined_sha256":"96d8f6e6ea1b1ba13557216624a3461c738729d53c79b4b0100d1f3a3a32441c"}
pkgmeta: {"name":"rea-agents","version":"6.7.0","serverSdkVersion":"2.3.1","clientSdkVersion":"2.3.1","coreSdkVersion":"2.3.1","skillVersion":"42"}
```

`dist/recordedCatalogDigests.js` (411 B, sha256 `8206fc7fc62310cb2f51208b71b3b749879466f33c14b75dfa9a74fdc6bdb4f6` — matches `E2.md:120`) carries the same triple. Catalog-identity files present: `dist/catalogIdentity.js` (4217 B), `dist/identity.js` (1095 B), `dist/serverIdentity.js` (3486 B), `dist/generatedPackageMetadata.js` (297 B). No `.json` catalog file ships inside `dist/` (`find dist -name '*.json'` → empty); the catalog is compiled JS constants.

### 3. Live `doctor` identity on 6.7.0 (offline) — digests confirmed live, not just read

```
$ npx --offline rea-agents@6.7.0 doctor --format json --full-output   (rc=1; audit-wide failures)
{"ok":false,"error":{… "identity": {
 "cli_package_version": "6.7.0",
 "expected_skill_version": "42",
 "sdk": {"server":"2.3.1","client_test":"2.3.1","core":"2.3.1"},
 "catalog": {"counts": {"cli_commands":153,"mcp_tools":207,"mcp_prompts":6},
             "digests": {"tools_sha256":"af39310c…","prompts_sha256":"7152916a…","combined_sha256":"96d8f6e6…"}},
 "live_server": {"state":"unknown","remediation":"Call binary_session in the active client …"},
 "installations": {"paths":["/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/.bin/rea"],"state":"single"},
 "skill": {"installed_version":"42","installed_tool_count":207,"state":"stale"}}}}
```

`scope_checks` spot values: node `26.12.0` ok; host `arch unknown`; ghidra `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` ok; ghidra-version `12.1.4`; ghidra-java `21.0.12.1; 64-bit; JDK; /usr/lib/jvm/java-21-openjdk`; jadx ok (`jadx-headless-mcp-0.7.1-all.jar`); hopper/ida/kuna `missing_analysis_engine`; `skill:identity` `config_drift` ("Installed REA skill identity is stale" — at equal version 42, the same anomaly E24 recorded in round 1). `providerInspections[ghidra]`: configured+available, providerVersion `12.1.4`, env `GHIDRA_INSTALL_DIR`/`JAVA_HOME` as configured. The 6.7.0 counts are now **probed live** (CLI doctor level); the live MCP-server `binary_session` probe remains the battery seats' scope.

### 4. npx offline resolution — and the network nuance

```
$ cd /tmp/arc2-l2r2-SC1-scratch && npx --offline --loglevel=http rea-agents@6.7.0 --version
npm http cache https://registry.npmjs.org/rea-agents 9ms (cache hit)
6.7.0
rc=0
$ npx --loglevel=http rea-agents@6.7.0 --version        # WITHOUT --offline
npm http fetch GET 200 https://registry.npmjs.org/rea-agents 55ms (cache revalidated)
6.7.0
rc=0
```

Observation: with `--offline` the resolution is a pure cache hit (no network); without it, npm **revalidates against the registry over the network** — observed, not forced, and it succeeded (host online). Any "offline resolution" claim must therefore be tied to `--offline` specifically. `npx --offline rea-agents@6.7.0 doctor --help` and a full `doctor` run also executed offline (rc=0 for `--help`). The cache's `package-lock.json` records `"resolved": "https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz"`, `"integrity": "sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw=="` (`:1607-1610`) — byte-identical to E2's quoted integrity.

### 5. E2 inventory corroboration — five headline numbers reproduced

```
$ for d in dea9475797100b20 ad9a3fdbcad992c6 a1722018f28f9df2; do find ~/.npm/_npx/$d/node_modules/rea-agents -type f | wc -l; done
1161   1650   1775                      # == E2.md:52 exactly
$ sha256sum <each>/node_modules/rea-agents/package.json
1c6244e5689db5354fffc0e92f4ee0e0237c3a6d645de564ade2d8375fa570f9   # 6.4.0  == E2.md:22
a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c   # 6.5.0  == E2.md:23
3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570   # 6.7.0  == E2.md:24
```

Also reproduced: all three `.bin/rea` symlinks → `../rea-agents/scripts/rea.mjs`; dist dir-name diff 6.5.0→6.7.0 adds exactly `kuna/`, `providers/`, `recordedCatalogDigests.js`; 6.5.0 lacks `recordedCatalogDigests.js` (grep for its digest across the 6.5.0 package → 0 hits). **Verdict on E2: AGREE on every inventory number re-derived here; one refinement — E2's "no network was used or attempted" is true of its own `--offline`/`--no` commands, but plain npx does revalidate (my §4).**

### 6. `doctor` identity for the other two caches — PROVINCE's cache-side values hold

```
$ npx --offline rea-agents@6.5.0 doctor --format json --full-output
cli_package_version: 6.5.0 | expected_skill_version: 42
catalog: cli_commands 153, mcp_tools 207, mcp_prompts 6
         tools_sha256 805433f17bb4f709558ff20c04f96fe561fca2938fd0f459b1f8cc0f6b438ded   # == PROVINCE.md:20
$ npx --offline rea-agents@6.4.0 doctor --format json --full-output
cli_package_version: 6.4.0 | expected_skill_version: 37
catalog: cli_commands 127, mcp_tools 170, mcp_prompts 6
         tools_sha256 25802f6de8c14ba736dc61ff1cbc7c5cd738fd74426aa01338f2dd03e0911166   # == PROVINCE.md:21-23
skill: installed_version 42, installed_tool_count 207, state stale
```

Static cross-check: 6.4.0 node import → tools 170, cli 127 (matches its doctor). Envelope difference noted: 6.4.0 doctor returns `{"ok":true,"data":{…}}` while 6.7.0 returns `{"ok":false,"error":{…}}` — same `healthy:false` inside; the JSON envelope routing differs between versions (parser-relevant for any landed recipe).

### 7. Registration census from 6.7.0 doctor — two pins outside PROVINCE's three-config surface

```
"registrations": [ …, 
 {client: devin,  config_path: /home/vgpnk/.config/devin/mcp_config.json, command: [npx,-y,rea-agents@6.5.0,mcp], package_reference: rea-agents@6.5.0, state: stale},
 {client: omp,    config_path: /home/vgpnk/.omp/agent/mcp.json,           command: [npx,-y,rea-agents@6.5.0,mcp], package_reference: rea-agents@6.5.0, state: stale},
 {client: grok_build, config_path: /home/vgpnk/.grok/config.toml,         command: [npx,-y,rea-agents@6.5.0,mcp], package_reference: rea-agents@6.5.0, state: stale},
 {client: grok_bot, config_path: /home/vgpnk/.grokbot,                    command: [], state: manual},
 {client: codex,  config_path: /home/vgpnk/.codex/config.toml,            command: [/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/.bin/rea, mcp], state: stale},
 {client: kimi,   config_path: /home/vgpnk/.kimi-code/mcp.json,           command: [], state: missing},
 {client: claude_code / copilot_cli / cursor / hermes / opencode / pi / zcode, state: missing} ]
```

Independent greps confirming the two extra pins:

```
$ grep -n 'rea-agents' ~/.grok/config.toml
30:    "rea-agents@6.5.0",
$ sed -n '26,31p' ~/.grok/config.toml      → [mcp_servers.rea] command="npx", args=[-y, "rea-agents@6.5.0", mcp], startup_timeout_sec=30; env table :35
$ sed -n '76,79p' ~/.codex/config.toml     → [mcp_servers.rea] command = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/.bin/rea" (absolute path into the 6.5.0 cache), args=["mcp"], startup_timeout_sec=30
```

Observations: (a) PROVINCE.md:44's "three client configs" surface undercounts the configured rea registrations on this host — `grok_build` and `codex` carry rea entries too (mtimes 2026-10-16 23:47 / 2026-10-17 00:06, i.e. after PROVINCE's 2026-10-16 reverify); (b) doctor resolves the **kimi** client to `~/.kimi-code/mcp.json` (which contains only `cli-agents`, no rea key — matches SC2 round-1 §8) and reports `missing`, while the actual live Kimi pin sits in `config.toml:2940` — doctor's client census and the pin census are different surfaces; (c) all pins other than Kimi's are `stale` relative to the CLI package in use (6.7.0), per doctor's own message "This registration requests rea-agents@6.5.0, while the current REA CLI package is 6.7.0".

### 8. Live pin re-check (independent of E1/E2)

```
$ grep -n 'rea-agents' /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json /home/vgpnk/.kimi-code/config.toml
/home/vgpnk/.config/devin/mcp_config.json:7:        "rea-agents@6.5.0",
/home/vgpnk/.omp/agent/mcp.json:8:        "rea-agents@6.5.0",
/home/vgpnk/.kimi-code/config.toml:2940:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
$ sed -n '1478p;2938,2940p' /home/vgpnk/.kimi-code/config.toml
model = "kimi-k3"
[mcp_servers.rea]
command = "npx"
args = [ "-y", "rea-agents@6.7.0", "mcp" ]
```

### 9. Ghidra / Java / jq unchanged (vs round-1 SC1.md values)

```
$ sed -n '17p' ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties
application.version=12.1.4
$ sha256sum ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties
e84c26b08545eee63d24a1a8a4dd7905e4209538e2e7192093877c435c64eb67
$ stat -c '%n size=%s mtime=%y' …/ghidraRun …/support/analyzeHeadless
…/ghidraRun size=1461 mtime=2026-09-21 16:38:14   …/analyzeHeadless size=2388 mtime=2026-09-21 16:38:14
$ java -version → openjdk version "21.0.12.1" 2026-08-18 / build 21.0.12.1+1
$ readlink -f /usr/bin/java → /usr/lib/jvm/java-21-openjdk/bin/java ; sha256sum /usr/bin/java
e08a8b21479a8d39d46b23af483d78fb88a891b7fe0e2c9abd50a8fe16ad2a15  /usr/bin/java
$ sha256sum /usr/lib/libjq.so.1.0.4 /usr/bin/jq
7e8bccc6df37a55fb90703c9069b3770f5cdc502e96959c866d2f30fbf5e8b6b  /usr/lib/libjq.so.1.0.4   # == round-1 expected prefix
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
```

### 10. Installed shared skill vs cache copies (stale-at-equal-version anomaly)

```
$ sha256sum ~/.agents/skills/reverse-engineer-anything/SKILL.md   → c86398238b2a382dd34f4df230f83a5a1c3377a4f0c4df39ea43053ea0b49da0  (22513 B)
$ cache copies: 6.4.0 46b495fe… (13580 B) | 6.5.0 3456aab9… (22513 B) | 6.7.0 fbcd39d6… (23523 B)
$ cmp installed vs each → all three differ; frontmatter (version 42, tool_count 207) identical in 6.5.0/6.7.0 copies
```

Observation: the installed copy matches **none** of the three shipped copies byte-for-byte, yet its frontmatter claims v42/207 — consistent with doctor's `skill:identity` `stale` verdict at equal version (E24's round-1 anomaly now explained by byte difference, not version difference). The installed skill is a regular directory at `~/.agents/skills/reverse-engineer-anything` (symlinked from `~/.kimi-code/skills/`), mtime 2026-10-18 08:23, with `.rea.backup` siblings.

### 11. Mutation sweep and custody re-verify (post-probes)

```
$ find ~/.npm/_npx -mindepth 2 -newermt '2026-10-18 13:45' -type f     → (empty)
$ stat -c '%n %y' ~/.npm/_npx/a1722018f28f9df2 ~/.npm/_npx/ad9a3fdbcad992c6 ~/.npm/_npx/dea9475797100b20
…/a1722018f28f9df2 2026-10-18 14:02:02 -0300   …/ad9a3fdbcad992c6 14:02:25   …/dea9475797100b20 14:02:38
```

No file inside any rea cache changed during my probes (only directory mtimes bumped, consistent with E2.md:112's recorded side effect; my probes pushed them from E2's 13:59–14:00 to 14:02). Whole-package digests stable: 6.7.0 `8f4eba1f…` (3 checks), 6.5.0 `4192c743634979df6c98e82c5c3afcfdb0f757b2836e8974448b8cccfddf77b9` (2 checks), 6.4.0 `0c78de9a8ffb20b13f5d9dcc1e6e1072f5eb9ce3380f25a95732b828816e122f`.

```
$ { date -u +%Y-%m-%dT%H:%M:%SZ; sha256sum <5 paths>; }            # my capture 2026-10-18T17:03:09Z
$ tail -n +2 .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt | sha256sum -c -
…5× OK ; rc=0     # receipt self-hash 4097ec77397308855bfb170733cf32d8c001de298ed1bf9bc1f4753ec25c6245
```

My 5-path capture is byte-identical to the round-2 pre-pair (shape 6/5/1 verified: 6 lines, 5 hash lines, 1 timestamp).

### 12. Session hygiene

```
$ ps aux | grep -iE 'rea-agents|rea\.mjs|rea mcp' | grep -v grep
vgpnk 3693330 … node /tmp/arc2-l2r2-P3/scripts/rea.mjs
```

My seat opened **no** MCP session: every `npx` invocation was a one-shot CLI (`--version`, `doctor`, `doctor --help`) that exited (rc 0/1); the only live rea process on the host belongs to seat P3 (their scratch path) — not mine, flagged for the parent. No processes of mine remain.

## Text for the parent to land VERBATIM (fenced)

```text
SC1 host-surface census (arc2-loop1-round2, read-only, 2026-10-18T16:59–17:04Z): 6.7.0 cache `~/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents` is complete — package.json:4 `"version": "6.7.0"` (sha256 3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570), dist/ 1699 files, whole package 1775 files digest 8f4eba1f72e2c63d6800f734630233b7ffe747a4e8863c1ec1be4e7c95e8009e (stable 3 checks), skills/reverse-engineer-anything (v42/tool_count 207). 6.7.0 catalog RESOLVED (static import + live offline doctor identity): 207 MCP tools / 153 CLI commands / 6 prompts, tools_sha256 af39310c9591bb981893ec0d2188b1bcf6e9cc8ba3ac513d5bbefc8ddcb85639 (also in shipped dist/recordedCatalogDigests.js, sha256 8206fc7f…); skill:identity reports stale at equal version 42. Offline resolution: `npx --offline rea-agents@6.7.0 --version` → 6.7.0 (rc=0, npm log `cache hit`, no network); plain npx DOES revalidate over the network (`fetch GET 200 … cache revalidated`) — the offline guarantee is `--offline`-specific. E2's inventory independently corroborated: file counts 1161/1650/1775 and all three package.json sha256s (1c6244e5…/a5003023…/3f6c47fb…) match byte-for-byte; 6.5.0 doctor identity tools_sha256 805433f1… and 6.4.0 25802f6d…/expects v37 both match PROVINCE.md:20-24 — the cache-side PROVINCE values are accurate; only the Kimi pin claim (6.4.0@:1478) is stale. NEW registration surface: 6.7.0 doctor lists grok_build `~/.grok/config.toml:30` → rea-agents@6.5.0 (stale) and codex `~/.codex/config.toml:77` → absolute path `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/.bin/rea` (stale); doctor checks the kimi client at `~/.kimi-code/mcp.json` (no rea entry → missing), NOT config.toml — doctor's client census ≠ the pin census; PROVINCE.md:44's three-config surface undercounts configured rea registrations (5 found). Ghidra 12.1.4 (application.properties sha256 e84c26b08545eee63d24a1a8a4dd7905e4209538e2e7192093877c435c64eb67), JDK 21.0.12.1, /usr/lib/libjq.so.1.0.4 7e8bccc6… all unchanged. Zero file mutation in any rea cache during probes (only dir mtimes); 5-path custody re-verified 5/5 OK vs round-2 pre-pair at 17:03:09Z; no MCP session opened by this seat.
```

## Conclusions by label

- **Observation** — (a) 6.7.0 cache identity/contents as in §1 (package.json:4, dist 1699, package 1775, skills 7 files, v42/207 frontmatter); (b) static counts 207/153 via node import and live doctor identity with digests `af39310c…` (§2, §3); (c) `npx --offline` pure cache hit vs plain-npx network revalidation, both observed (§4); (d) E2's five headline numbers reproduced independently (§5); (e) 6.5.0 `805433f1…` and 6.4.0 `25802f6d…`/v37 doctor identities match PROVINCE.md:20-24 (§6); (f) doctor registration list incl. grok_build/codex pins and the kimi→mcp.json `missing` resolution (§7); (g) live pins unchanged, `:1478` = `model = "kimi-k3"` (§8); (h) ghidra/java/jq hashes as listed (§9); (i) installed skill matches no cache copy byte-for-byte (§10); (j) zero file mutation in caches; whole-package digests stable; 5-path custody 5/5 OK (§11); (k) only P3's rea process on host; no session of mine (§12).
- **Inference** — the 6.7.0 package is the artifact any offline `npx -y rea-agents@6.7.0` serves on this host, and its counts/digest (`207/153/6`, `af39310c…`) are the correct current-surface values for the Kimi pin, superseding the 6.4.0-era `170/127/25802f6d…` in PROVINCE.md:10/:18; doctor's `stale` verdict on the installed skill is explained by byte divergence, not version; the registration census (5 rea pins, 4 clients beyond the three configs) is a wider surface than PROVINCE.md:44 describes and than any custody receipt covers.
- **Unknown** — live MCP-server `tools_sha256` for a Kimi-side 6.7.0 session (doctor's `live_server.state = unknown`; battery seats' `binary_session` scope); whether the live Kimi client has loaded the 6.7.0 pin (configured ≠ held); whether codex/grok_build registrations are ever exercised by those clients (no probe ran them); whether npm's revalidation request mutated any `_cacache` state (not inspected; outside scope).

## Scope compliance

Read-only on all repo and home files; no git mutations; no config edits; no installs. Network: one observed-and-reported revalidation by a non-`--offline` npx probe (succeeded, host online); no other network. No secret values read or emitted (only version strings, line numbers, key names, file counts, digests). Only write: this report. Scratch: `/tmp/arc2-l2r2-SC1-scratch/` only.
