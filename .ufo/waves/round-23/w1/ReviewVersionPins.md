# ReviewVersionPins — REA 6.5.0 CLI pin vs operator live 6.7.0 registration; sigrok-cli 0.7.2 facts

Seat: `KaidokuR23.ReviewVersionPins` (reviewer, read-only, leaf). Round 23, W1. Author-side report, not outside verification. All observations from static file reads, registry metadata queries, and digest recomputation on 2026-10-21 unless marked **[INFERENCE]** / **[UNKNOWN]**. No REA probe, no MCP device, no AppImage execution, no pacman/uv install, no config edit.

Wave-declared interface (assignment source): `.ufo/waves/round-23/gen-wave1.py:10` / `wave1-spec.json` / `wave1-dispatch.json` — "REA only via npx -y rea-agents@6.5.0 CLI, --format json --full-output. No MCP devices." This seat: `gen-wave1.py:55` (`ReviewVersionPins`).

## Findings

### 1. Wave pin: rea-agents CLI 6.5.0 — observed identity is exact and matches the published tarball

- Self-report: `npx -y rea-agents@6.5.0 --version` → stdout `6.5.0`, exit 0 (this seat, 2026-10-21; independently reproduced by `w1/SchemaFlutter.md:18`, `w1/SchemaGdb.md:26,31`, `w1/SchemaRizin.md:36`).
- Installed cache: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6` — `package.json` `"version": "6.5.0"`; `package-lock.json` records `"resolved": "https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz"`, `"integrity": "sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A=="` — byte-identical to the registry's `dist.integrity` for 6.5.0 (finding 3). The cached bytes are the published tarball; the pin is exact, not range-resolved.
- **[INFERENCE, hazard]** the npx dir's `package.json` records the dependency as `"^6.5.0"`. The registry has **no 6.6.0** (versions list and `time` map jump 6.5.0 → 6.7.0), so any future re-resolution of `^6.5.0` would land on 6.7.0 and silently invalidate every source-line/hash anchor seats cite against this cache. As of 2026-10-21 the cache still holds 6.5.0 (re-read this session).
- System state: `command -v sigrok-cli` → not found; `pacman -Q | grep -iE 'sigrok|libsigrok|pulseview'` → no rows. No system-level rea/sigrok install competes with the pin; the only channels are the npx cache and the operator registration.

### 2. Operator live registration: rea-agents@6.7.0, rewritten 2026-10-20 13:35:56 -03 — full pin history reconstructed

Live file `/home/vgpnk/.omp/agent/mcp.json` (mode 0600, mtime `2026-10-20 13:35:56.123987225 -0300`, sha256 `266078529e5b18f1dc165253c7c2037e6d60edecae0873506c93f95d20bbd9d4`): server `rea`, `npx -y rea-agents@6.7.0 mcp`, env `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`, `JAVA_HOME=/usr/lib/jvm/java-21-openjdk`, `REA_JADX_MCP_JAR=/home/vgpnk/.local/opt/jadx-headless-mcp/jadx-headless-mcp-0.7.1-all.jar`, **no `enabled` key**.

Observed backup chain (sha256 computed this session; the two `*.recovery` filenames are content-addressed — filename equals sha256 of the file's own content, verified for both):

| file (sha256 prefix) | mtime | rea pin | notes |
|---|---|---|---|
| `mcp.json.rea.backup` `a2c4a6c3…` | Oct 12 09:51 | `6.4.0` | no env, no enabled |
| `mcp.json.rea.backup.619e9309….recovery` `619e9309…` | Oct 14 17:53 | `6.4.0` | + env (GHIDRA, JAVA_HOME), no JADX |
| `mcp.json.pre-disable-20261020T1015` `38d2a1d0…` (mtime preserved from Oct 14 17:53) | Oct 20 10:15 (name) | `6.5.0` | + env incl. `REA_JADX_MCP_JAR`, no enabled |
| `mcp.json.rea.backup.e571d192….recovery` `e571d192…` | Oct 20 13:35 | `6.5.0` | + env, **`"enabled": false`** — the pre-rewrite state |

So the operator-side registration ran 6.4.0 until Oct 14 17:53, 6.5.0 from then until Oct 20 13:35:56, and 6.7.0 since. The 13:35:56 event archived the 6.5.0+disabled state under a digest-named recovery file and wrote the live file with the pin raised to 6.7.0 and `enabled:false` removed. This matches the standing prompt block (`.ufo/prompts/kaidoku-round-23.md:280-283`: "An unidentified writer rewrote that file at 13:35:56 -03; the rea pin is now `rea-agents@6.7.0` and `enabled: false` is gone"; operator-owned, never edit or restore). This seat observed the files read-only; hashes above are the point-in-time record.

### 3. Registry identity of both pins (npm registry, queried 2026-10-21)

Source: `npm view rea-agents@6.5.0|6.7.0 … --json`, `npm view rea-agents dist-tags time versions --json` against `https://registry.npmjs.org/rea-agents`; all queries exit 0.

- **6.5.0** — published `2026-10-14T12:56:14.513Z`; tarball `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`; shasum `7ea5e6f669bc18c45dbf5dba653edaa1ada07ab3`; integrity `sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==`.
- **6.7.0** — published `2026-10-18T08:12:05.640Z`; tarball `…/rea-agents-6.7.0.tgz`; shasum `11f23ba377303a5c28b3162180cf2bf3f3643708`; integrity `sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==`. `dist-tags.latest = "6.7.0"`; package `time.modified = 2026-10-18T08:12:05.977Z`.
- **No 6.6.0 exists** in either the `versions` array or the `time` map (6.5.0 → 6.7.0 directly).
- Manifest comparison (engines/bin/dependencies): `engines` (`^22.19.0 || ^24.11.0 || >=26.0.0`) and `bin` (`rea`, `rea-agents` → `scripts/rea.mjs`) identical; the sole dependency delta 6.5.0 → 6.7.0 is an **added `openpgp 6.3.2`**.
- Second npx cache `/home/vgpnk/.npm/_npx/a1722018f28f9df2`: installed `6.7.0`; its lockfile integrity `sha512-yhIx…` matches the registry 6.7.0 integrity — also byte-exact published tarball.

### 4. Cross-version behavioral delta relevant to wave receipts (why the 6.5.0 pin is load-bearing)

- Typed-refusal exit code differs: on the retained Saber refusal, 6.5.0 CLI exits **1** with `{ok:false,error…}`; the 6.7.0 cache copy returns exit **0** with the error envelope, and adds dynsym/dynstr `SHF_ALLOC`/PT_LOAD validation (`sectionMappingFailure`) — observation with probes in `w1/SchemaDart.md:167-174`, `w1/DartSaberRefusal.md:210-212`.
- Signals domain is stable across the pins: `diff` shows `dist/domain/signals/annotationTextWindow.js` and `dist/domain/signals/signalRecording.js` identical; `dist/signals/SigrokRecordingProvider.js` differs by 7 lines, all cancellation-cause/cleanup plumbing (`w1/SignalDecodePaging.md:90-92`).
- **[INFERENCE]** any evidence captured through the operator 6.7.0 registration would not be receipt-compatible with 6.5.0-based evidence (refusal exit semantics at minimum). The wave's "No MCP devices" rule plus the 6.5.0 CLI pin keeps the two channels apart; this seat found no wave evidence recorded through 6.7.0 (`round-23/evidence/c1/*.run.json` argv rows all pin `rea-agents@6.5.0`).

### 5. sigrok-cli 0.7.2 pin facts — static, no execution

Pinned binary: `/home/vgpnk/.local/opt/sigrok-cli-0.7.2-x86_64.AppImage` (mode 0755, 49,558,848 bytes, mtime Oct 21 08:39).

- Digest recomputed this session: `sha256sum` → `49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614`, exit 0. It matches **both** the wave1 spec expectation (`gen-wave1.py:17`) and the recorded extraction (`round-23/sigrok-extraction.json:7`, whose argv was `--appimage-extract`, cwd `round-23/runtime`, exit 0). One digest, three independent records agree.
- Upstream identity [web-sourced]: the official distribution point is `https://sigrok.org/download/binary/sigrok-cli/`, whose index lists `sigrok-cli-0.7.2-x86_64.AppImage` dated 2021-03-01 (alongside `sigrok-cli-0.7.2-i386.AppImage` and the `sigrok-cli-0.7.2.tar.gz` source release); distro packages (Debian sid, Ubuntu) corroborate 0.7.2 as the upstream sigrok-cli release.
- Static version markers inside the wave-local extraction `round-23/runtime/squashfs-root/` (tree mtimes Oct 21 11:36):
  - `org.sigrok.sigrok-cli.desktop:12` → `X-AppImage-Version=0.7.2`.
  - `strings usr/bin/sigrok-cli | grep -m3 '0\.7\.2'` → `0.7.2`, exit 0 (version string embedded in the launcher binary).
  - Bundled libraries: `usr/lib/libsigrok.so.4.1.1`, `usr/lib/libsigrokdecode.so.4.2.1`; `strings libsigrokdecode.so*` carries `0.5.3` and `3.5.2`. **[INFERENCE]** `0.5.3` is libsigrokdecode's own library version and `3.5.2` the linked Python; not verified against upstream here. **[UNKNOWN]** whether the bundled libsigrokdecode decoder catalog matches what REA's "0.7.2 catalog grammar" parser expects on a live run — gate pass/fail was not exercised by this seat (known launch blocker `g_module_open_full`/libgio is BuildSigrok's assignment, `gen-wave1.py:17`; `sigrok-extraction.json:9` is a 124.4 KB single-line inventory payload this seat did not fully parse).
- REA's own enforcement of the pin — identical in **both** 6.5.0 and 6.7.0 (read from the two caches):
  - `dist/signals/SigrokRecordingProvider.js:25` (6.5.0) / `:26` (6.7.0): `version: "sigrok-cli@0.7.2"` (adapter metadata "REA sigrok recording adapter").
  - `:73` / `:76`: `REA_SIGROK_COMMAND` must be an absolute path ("Supply absolute REA_SIGROK_COMMAND for sigrok-cli 0.7.2 with libsigrokdecode.").
  - `:141-142` / `:144-145`: runtime gate executes `--version` and requires stdout matching `/^sigrok-cli 0\.7\.2(?:\r?\n|$)/u` **and** containing `libsigrokdecode`, else typed refusal "Expected sigrok-cli 0.7.2 with libsigrokdecode; inspect the selected installation."
  - `dist/domain/signals/parseDecoderDiscovery.js:4` (both): "Parse only the 0.7.2 catalog grammar; help remains literal producer text."
  - `dist/application/CapabilityInventory.js:290` (both) and the MCP bundles (`mcp/main-kBXHZ8S5.js:18004,18106` in 6.5.0; `mcp/main-Cx-Z7m_n.js:25800,25902` in 6.7.0) carry the same pin/remediation text; `README.md:191`/`:199` and `skills/reverse-engineer-anything/SKILL.md:146-148` (both) state "sigrok-cli 0.7.2 + prlimit" via `REA_SIGROK_COMMAND` / `REA_SIGROK_PRLIMIT_COMMAND` (default `/usr/bin/prlimit`).
- Consequence [INFERENCE]: the sigrok pin is version-anchored independently of the rea-agents pin — upgrading 6.5.0 → 6.7.0 does not move the sigrok-cli requirement, and any selected `REA_SIGROK_COMMAND` whose `--version` does not open with exactly `sigrok-cli 0.7.2` is refused at execution time, regardless of which CLI pin invoked it.

### 6. Consistency verdict

**[INFERENCE]** The wave's two version declarations are internally consistent and both are byte-anchored: rea-agents 6.5.0 via registry integrity == npx lockfile integrity, and sigrok-cli 0.7.2 via one sha256 (`49d2f597…`) agreeing across spec, extraction record, and the on-disk AppImage. The operator's live 6.7.0 registration is a separate invocation channel (MCP, `xd://mcp__rea_*`) that the wave explicitly forbids, so the 6.5.0/6.7.0 divergence has no effect on wave evidence provided the no-MCP rule holds. The one concrete behavioral divergence found between the pins that would matter if channels were mixed is the typed-refusal exit code (6.5.0 exit 1 vs 6.7.0 exit 0, finding 4). No action taken by this seat; the operator file remains operator-owned.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ReviewVersionPins.md` — this report; sha256 recorded in the seat's delivered result to Main (hash-of-record over the delivered bytes). No other files were created; operator config files were read in place, not copied.

## Installs

None. No pacman, uv, npm-global, cargo, or release-binary install; no global or config write. Tool usage was read-only against pre-existing npx caches plus `npm view` registry queries. (Session-side note: bash `strings`/`grep` pipelines on the AppImage binaries are static reads; the AppImage itself was never executed.)

## Open risks

1. **npx cache mutability.** The 6.5.0 cache dir records `"^6.5.0"`; with no 6.6.0 in the registry, a cache refresh that re-resolves that spec jumps to 6.7.0 and silently invalidates every source-line/hash anchor seats cite against `ad9a3fdbcad992c6`. Exact `@6.5.0` specifiers and the lockfile integrity are the only guards; today's re-check shows 6.5.0 still installed.
2. **Operator file drift.** `/home/vgpnk/.omp/agent/mcp.json` was rewritten by an unidentified writer as recently as 2026-10-20 13:35:56; the hashes here are point-in-time and may already be stale.
3. **Untested sigrok gate.** Whether the pinned AppImage passes REA's `--version` gate on this host (including the `libsigrokdecode` stdout requirement) remains unobserved; the known libgio/g_module launch blocker sits with BuildSigrok. This report's 0.7.2 facts are static identity facts, not a runtime pass.
4. **openpgp addition unexplained.** 6.7.0 adds `openpgp 6.3.2` to its dependencies; what feature it backs was not investigated (no manifest/docs pointer examined).
5. **Bundled decoder library version.** libsigrokdecode 0.5.3 inside the AppImage is inferred from binary strings, not an upstream manifest; the actual decoder catalog content (what `inspect-signal-decoders` will page through) follows the library, not the CLI's 0.7.2 number.

---
Report: `.ufo/waves/round-23/w1/ReviewVersionPins.md` (path relative to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`)
