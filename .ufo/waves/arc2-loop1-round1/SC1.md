# SC1 — host surface census (read-only) — arc2-loop1-round1

Census run: 2026-10-18T11:52:31-03:00 (`date -Is`). All commands read-only; no repo files edited except this report.

## Verdict

PASS — all six census targets resolve on this host: REA npx caches for 6.5.0 (`ad9a3fdbcad992c6`) and 6.4.0 (`dea9475797100b20`) both present with matching package versions; Ghidra 12.1.4 at `~/.local/opt/ghidra_12.1.4_PUBLIC` (`application.version=12.1.4`); OpenJDK 21.0.12.1; `/usr/bin/jq` and `/usr/lib/libjq.so.1.0.4` present, libjq sha256 `7e8bccc6…` **matches the battery's expected prefix**. One caveat: PATH `jq` is a *different* binary than `/usr/bin/jq` (see O4).

## Evidence (commands + observed output)

### 1. REA npx caches

```
$ ls -d ~/.npm/_npx/*/node_modules/rea-agents
/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents
/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
/home/vgpnk/.npm/_npx/dea9475797100b20/node_modules/rea-agents
```

Version probe per dir (`grep -n '"version"' …/package.json`):

| cache dir | `package.json:4` version |
|---|---|
| `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` | `"version": "6.5.0"` |
| `~/.npm/_npx/dea9475797100b20/node_modules/rea-agents` | `"version": "6.4.0"` |
| `~/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents` | `"version": "6.7.0"` (extra, not requested) |

- `name` field at `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json:2` = `"rea-agents"` (exact path resolves; `:4` line shown above).
- mtimes: 6.5.0 pkg `2026-10-16 12:49:41 -0300`; 6.4.0 pkg `2026-10-16 14:40:49 -0300` (`stat -c '%n mtime=%y'`).
- Remaining npx dirs: `94207acffe67148d` → typescript-language-server; `c8ab89660c602c20` → @openai; `ceb651102292ad92` → empty.

### 2. Ghidra

```
$ cat ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties | grep -n application.version
17:application.version=12.1.4
```
Pointer: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties:17` (also `:16` = `application.layout.version=3`).
- Install dir: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` (found via `find /opt /usr/local /home/vgpnk -maxdepth 3 -iname "*ghidra*" -type d`).
- `ghidraRun` present, `-rwxr-xr-x`, 1461 bytes, mtime Sep 21 16:38; `support/analyzeHeadless` present.
- `which ghidra ghidraRun analyzeHeadless` → no output: **not on PATH** (launch via absolute path).

### 3. Java

```
$ java -version
openjdk version "21.0.12.1" 2026-08-18
OpenJDK Runtime Environment (build 21.0.12.1+1)
OpenJDK 64-Bit Server VM (build 21.0.12.1+1, mixed mode, sharing)
```
`which java` → `/usr/bin/java`.

### 4. jq — /usr/bin/jq and /usr/lib/libjq.so.1.0.4

```
$ ls -la /usr/bin/jq /usr/lib/libjq.so.1.0.4
-rwxr-xr-x 1 root root  30800 Jun 20 14:10 /usr/bin/jq
-rwxr-xr-x 1 root root 350384 Jun 20 14:10 /usr/lib/libjq.so.1.0.4

$ sha256sum /usr/bin/jq /usr/lib/libjq.so.1.0.4
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
7e8bccc6df37a55fb90703c9069b3770f5cdc502e96959c866d2f30fbf5e8b6b  /usr/lib/libjq.so.1.0.4
```

- `/usr/lib/libjq.so.1.0.4` sha256 = `7e8bccc6df37a55fb90703c9069b3770f5cdc502e96959c866d2f30fbf5e8b6b` — **prefix `7e8bccc6` matches the battery's expected value**.
- `readlink /usr/lib/libjq.so.1` → `libjq.so.1.0.4`; `ldd /usr/bin/jq` → `libjq.so.1 => /usr/lib/libjq.so.1`.
- `file`: `/usr/bin/jq` = ELF 64-bit PIE, stripped, BuildID `cc56d2fd644ddd549b5339882e77f22f781525d3`; `libjq.so.1.0.4` = ELF shared object, stripped, BuildID `4bd539a8e23e0c939d759a1400acf610bd71ee78`.
- **Caveat (O4)**: `which jq` → `/home/vgpnk/.local/bin/jq`, a *different* binary (2,267,912 bytes, mtime Oct 3 18:34, sha256 `b1c22172dd303f3be49e935aa56aa48a8b7a46e0bc838b4997d3bb451495870f`, reports `jq-1.8.2`). `/usr/bin/jq --version` also reports `jq-1.8.2` but is the 30,800-byte dynamically-linked build. Bare `jq` in a shell exercises the ~/.local binary, NOT `/usr/bin/jq`/`libjq.so.1.0.4`.
- `node --version` → `v26.12.0` (context for npx legs).

## Verbatim block for parent (optional to land)

```text
REA 6.5.0 cache: /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents (package.json:4 "version": "6.5.0")
REA 6.4.0 cache: /home/vgpnk/.npm/_npx/dea9475797100b20/node_modules/rea-agents (package.json:4 "version": "6.4.0")
Ghidra: /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC (Ghidra/application.properties:17 application.version=12.1.4)
Java: /usr/bin/java — openjdk 21.0.12.1 2026-08-18 (build 21.0.12.1+1)
/usr/bin/jq sha256 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
/usr/lib/libjq.so.1.0.4 sha256 7e8bccc6df37a55fb90703c9069b3770f5cdc502e96959c866d2f30fbf5e8b6b (expected prefix 7e8bccc6 — MATCH)
```

## Conclusions by label

- **Observation** — every command output above, captured this session at 2026-10-18T11:52:31-03:00. libjq sha256 matches the battery's expected `7e8bccc6…` prefix.
- **Observation** — PATH `jq` (`~/.local/bin/jq`, sha256 `b1c22172…`) ≠ `/usr/bin/jq` (sha256 `e8156675…`); the pinned library `/usr/lib/libjq.so.1.0.4` is only exercised via `/usr/bin/jq` or by loading `libjq.so.1` explicitly.
- **Inference** — a battery leg that invokes bare `jq` would probe the ~/.local binary, not the pinned `/usr/lib/libjq.so.1.0.4`; legs 1–3 as specified (npx `rea-agents@6.5.0`, REA binary_session, explicit libjq path) are unaffected.
- **Inference** — `npx -y rea-agents@6.5.0` will hit the existing `ad9a3fdbcad992c6` cache (its sole package is rea-agents@6.5.0), barring a cache-key mismatch I did not re-run npx to confirm.
- **Unknown** — whether npx at battery time re-resolves 6.5.0 to that exact dir (not re-verified by running npx; read-only census only). A newer 6.7.0 cache also exists and would be used only for an unpinned/`@latest` invocation.
- **Unknown** — Ghidra 12.1.4's exact JDK requirement compatibility with system Java 21.0.12.1 (not read from Ghidra docs this session; Java presence alone observed).
