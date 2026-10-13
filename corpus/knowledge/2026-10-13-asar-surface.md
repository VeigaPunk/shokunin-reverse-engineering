<!-- corpus entry — kaidoku-shokunin round 1 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r1/11-asar-surface.md. Each candidate's `suggested:` field is its curation verdict; `reject` rows are retained calibration entries. -->

# kaidoku-r1 · 11-asar-surface — Electron/ASAR artifact survey (read-only)

Axes for this sweep: **coverage** (what asar-bearing apps exist on the host), **enumeration-reliability** (which probes actually see the surface), **evidence-quality** (every claim backed by a run command), **REA-fit** (where REA adds value over raw asar tooling). All probes read-only; the one accidental materialization (`extract-file` writes to cwd) was cleaned and is recorded below.

## Candidate: Six ASAR archives ship across four installed apps
- claim: `find /usr/lib /opt ~/.config -maxdepth 6 -name '*.asar'` returns exactly 6 archives: obsidian `app.asar` (469K) + `obsidian.asar` (25M), `signal-desktop/resources/app.asar` (37M), `1Password/resources/app.asar` (39M), `electron39/resources/default_app.asar` (107K), `electron43/resources/default_app.asar` (109K). `~/.config` contributes zero.
- source: find run on host; `ls -lh`; `sha256sum` (obsidian app.asar 8588f1fd…, obsidian.asar a52a7daf…, signal 7cd804fa…, 1password 769e0962…)
- verify: `find /usr/lib /opt ~/.config -maxdepth 6 -name '*.asar' 2>/dev/null | wc -l` → 6; `find ~/.config -maxdepth 6 -name '*.asar'` → empty
- verified-at: 2026-10-13
- suggested: admit — direct observation, stable paths under /usr/lib and /opt.

## Candidate: Obsidian's app.asar IS the main-process bundle; obsidian.asar is a sibling resource
- claim: `/usr/bin/obsidian` execs `electron43 /usr/lib/obsidian/app.asar`; app.asar's package.json is `"name": "obsidian", "version": "1.13.7", "main": "main.js"` and its main.js is Obsidian's real main process (registers privileged `app://` scheme with `codeCache`, initializes `@electron/remote`, computes APP_PATH by stripping the literal `app.asar` from `app.getAppPath()` to reach sibling resources — i.e., obsidian.asar). The 25M obsidian.asar holds the renderer payload (`/app.js`, `/app.css`, `/enhance.js`, `/help.html`, `/i18n/*.txt`).
- source: `cat /usr/bin/obsidian`; extracted `app.asar` `main.js`/`package.json`; `asar list` of obsidian.asar; `pacman -Q obsidian` = 1.13.7-2 (matches package.json)
- verify: `cat /usr/bin/obsidian; cd $(mktemp -d) && npx -y @electron/asar extract-file /usr/lib/obsidian/app.asar main.js && grep -n 'app.asar\|registerSchemesAsPrivileged' main.js`
- verified-at: 2026-10-13
- suggested: admit — two independent sources (launcher script + package.json version match) corroborate; useful REA target split (main vs renderer graphs).

## Candidate: file(1) is not a reliable ASAR enumerator on this host
- claim: `file` reports `/usr/lib/obsidian/app.asar` as `data` while `/usr/lib/obsidian/obsidian.asar` is correctly reported `Electron ASAR archive` — yet both parse identically (`asar list` works on both; both have the standard pickle header `04 00 00 00` + JSON `{"files":{…}}` at offset 0x10). Signature-based detection has false negatives.
- source: `file /usr/lib/obsidian/*.asar`; `od -A x -t x1z -v -N 32` on both
- verify: `file /usr/lib/obsidian/app.asar && npx -y @electron/asar list /usr/lib/obsidian/app.asar | wc -l` → "data" yet 54 entries
- verified-at: 2026-10-13
- suggested: admit — falsifiable and directly relevant to enumeration strategy (prefer extension glob + header parse over magic).

## Candidate: .unpacked sibling trees carry native .node modules outside the archive
- claim: `/usr/lib/obsidian/app.asar.unpacked/` exists and holds ELF natives `node_modules/btime/binding.node` and `node_modules/get-fonts/binding.node` (plus their JS shims). An ASAR survey that globs `*.asar` alone misses the native-code slice of the same app — kaidoku's native lane (Ghidra) and ASAR lane overlap here.
- source: `find /usr/lib/obsidian/app.asar.unpacked -type f`; `pacman -Ql obsidian | grep asar.unpacked`
- verify: `find /usr/lib /opt -maxdepth 6 -name '*.asar.unpacked' -o -name '*.node' -path '*unpacked*'`
- verified-at: 2026-10-13
- suggested: admit — enumeration must include `<archive>.unpacked/` siblings; these .node files are ELF inputs for the Ghidra provider.

## Candidate: `npx -y @electron/asar list` is a working read-only enumerator; `extract-file` is NOT side-effect-free
- claim: `npx -y @electron/asar list <archive>` (Node v24.21.0, fnm) enumerated all 6 archives read-only with zero writes — counts: app.asar 54, obsidian.asar 380, signal app.asar 1866, 1password app.asar 486, electron39 default_app 14. BUT `asar extract-file <archive> <name>` silently materializes the file into the CURRENT working directory (created `~/main.js` and `~/package.json`, RC=0, no stdout) — it is not a stdout streamer. Extraction must run inside a scratch dir.
- source: ran `asar list` on each archive; ran `extract-file` and observed files appear in `~` (deleted after inspection)
- verify: `cd $(mktemp -d) && npx -y @electron/asar extract-file /usr/lib/obsidian/app.asar package.json && ls` → file appears in cwd
- verified-at: 2026-10-13
- suggested: admit — operationally critical: "read-only survey" discipline breaks if extract-file runs in a repo dir.

## Candidate: 1Password's app.asar is flat webpack-numbered chunks — enumeration alone yields no semantics
- claim: `/opt/1Password/resources/app.asar` (486 entries) tops out at numeric chunk names `/1075.js`, `/1098.js`, `/1103.js`, `/1112.js`… — module identity is bundler-internal; `asar list` gives shape but not meaning. Signal's 1866-entry archive is _locales+source-heavy; obsidian.asar is named modules (`app.js`, `enhance.js`).
- source: `npx -y @electron/asar list /opt/1Password/resources/app.asar | head -15`; same for signal/obsidian
- verify: `npx -y @electron/asar list /opt/1Password/resources/app.asar | grep -cE '^/[0-9]+\.js$'`
- verified-at: 2026-10-13
- suggested: admit — motivates REA `recover-javascript-sources`/`analyze-javascript-application` over raw listing for the obfuscated-style bundles.

## Candidate: REA CLI resolves on this host; doctor shows Ghidra healthy, Hopper missing, overall unhealthy
- claim: `npx -y rea-agents@6.4.0` runs (150-line help). `rea doctor` reports `healthy: false` / `environment_healthy: false` at top level, yet `ghidra` + `ghidra-platform` + `ghidra-architecture` + `ghidra-installation` checks are all healthy (`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`, x64, JDK path per MINT.md), `node` healthy (24.21.0); `hopper` fails `missing_analysis_engine`; `skill: false` in scope. Doctor-unhealthy ≠ surface-blind: the JS/Electron tool surface is still listed.
- source: `timeout 90 npx -y rea-agents@6.4.0 doctor` (full output captured); `rea --help`
- verify: `npx -y rea-agents@6.4.0 doctor 2>&1 | grep -A3 'name: ghidra$\|name: hopper' | head -8`
- verified-at: 2026-10-13
- suggested: admit — corrects the naive "doctor red means unusable" reading; hopper is only needed for commercial-engine workflows.

## Candidate: REA's role on the ASAR surface is analysis+Evidence, not enumeration
- claim: plain `@electron/asar` enumerates and extracts raw members; REA (`rea-agents@6.4.0`) exposes `analyze-javascript-application` ("Statically reconstruct a local JavaScript/Electron application"), `recover-javascript-sources`, `trace-javascript-semantics`, `compare-application-versions`, `compare-javascript-export-shapes`, `extract-artifact`, plus runtime side `list-electron-targets`/`inspect-electron-page`/`capture-electron-scenario`/`reconcile-javascript-runtime` — all under `electron-provider` in doctor's tool list. Skill `~/.agents/skills/reverse-engineer-anything/SKILL.md:48` routes "ASAR or extracted JavaScript/Electron tree" to `analyze_javascript_application`. Division of labor: asar CLI = cheap inventory; REA = authenticated Evidence graphs, source recovery, semantic tracing, version diffing, runtime reconciliation.
- source: `rea --help` command table; `rea doctor` surface list (`surface: electron-provider`); SKILL.md:48, references/javascript-applications.md:3
- verify: `npx -y rea-agents@6.4.0 --help | grep -iE 'javascript|electron|asar'`; `sed -n '45,52p' ~/.agents/skills/reverse-engineer-anything/SKILL.md`
- verified-at: 2026-10-13
- suggested: admit — establishes the tool boundary this lane's REA mandate depends on.

## Candidate: Signal Desktop bundles its own Electron runtime; only Obsidian rides system electron
- claim: `/usr/bin/signal-desktop` execs `/usr/lib/signal-desktop/signal-desktop` (self-contained binary, asar under its `resources/`); `/usr/bin/obsidian` execs system `electron43` against a bare asar path. Two host-installed electron versions coexist (electron39 39.8.10-2, electron43 43.6.0-1) whose `default_app.asar` stubs (14 entries each) are runtime fallback, not app surface.
- source: `cat /usr/bin/signal-desktop`, `cat /usr/bin/obsidian`; `pacman -Q signal-desktop electron39 electron43` → 8.26.0-1, 39.8.10-2, 43.6.0-1
- verify: `head -5 /usr/bin/signal-desktop /usr/bin/obsidian`
- verified-at: 2026-10-13
- suggested: admit — matters for runtime-observation candidates (`list_electron_targets` needs a CDP endpoint; bundled vs system electron change how you'd attach).

## Candidate: `asar extract-file` streams bytes to stdout — REJECTED
- claim (falsified): `@electron/asar extract-file` prints member contents to stdout.
- source: ran `npx -y @electron/asar extract-file /usr/lib/obsidian/app.asar main.js` — RC=0, empty stdout, file `~/main.js` appeared on disk
- verify: `cd $(mktemp -d) && npx -y @electron/asar extract-file /usr/lib/obsidian/app.asar package.json > out.txt; wc -c out.txt package.json` → out.txt empty, package.json on disk
- verified-at: 2026-10-13
- suggested: reject — counter-evidence recorded above; keep as a calibration entry so future lanes don't script it as a streamer.

## Summary
Six ASARs across obsidian (split main/renderer bundles + native .node in .unpacked), signal-desktop, 1Password (webpack-flattened), and two electron runtime stubs; `@electron/asar list` enumerates all read-only while `file` misses one and `extract-file` writes to cwd; REA 6.4.0 resolves with a healthy Ghidra provider and owns the analysis layer (`analyze-javascript-application`, source recovery, runtime reconciliation) that raw asar enumeration cannot reach.
