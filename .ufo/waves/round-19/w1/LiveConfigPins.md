# Live client REA pins — Devin / OMP / Kimi (round 19, w1)

Seat: `KaidokuR19.LiveConfigPins` (read-only; no patch, no clone, no installs). Lane
`refs/heads/main = 85589ac757f9ca3cb25efcd702d0963e25c9c4df`; `git diff --name-only
8a8da7e… refs/heads/main -- PROVINCE.md` is empty (exit 0) and the working tree is clean for that
path, so the PROVINCE anchors cited below are the same text at contract baseline
`8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (re-confirmed at `git show B:PROVINCE.md`, lines 9, 12,
16-18, 19-22, 45).

Scope guard honoured: only the `rea` entries and their two-line diffs were printed. No credential,
token, model list or unrelated block appears in this report.

## Verdict

| client | pin observed now | anchor | PROVINCE statement | verdict |
|---|---|---|---|---|
| Devin | `rea-agents@6.7.0` | `~/.config/devin/mcp_config.json:7` | `:9`/`:16` say `6.5.0` | **stale** |
| OMP | `rea-agents@6.7.0` | `~/.omp/agent/mcp.json:8` | `:9`/`:17` say `6.5.0` | **stale** |
| Kimi | `rea-agents@6.7.0` | `~/.kimi-code/config.toml:4126` | `:10`/`:18` say `6.7.0` at `:4126` | match (anchor and value) |
| OMP `enabled` flag | **absent from the live file** | `~/.omp/agent/mcp.json:1-18` | `contract.md:35`, `wave1-spec.json:10` assert "disabled by operator authorization" | **no longer config-evidenced** |

So the C2 expectation "2 mismatches (Devin, OMP)" is confirmed at line level, and one extra finding
sits outside C2's pin probe: the operator's OMP disable flag is gone from the live config.

## File identities (observation)

| file | mode | size | mtime (-0300, ns) | sha256 |
|---|---|---|---|---|
| `~/.config/devin/mcp_config.json` | 600 | 406 | 2026-10-20 13:35:56.120449714 | `9159ca91487a34daf86d203f04bf747143e750f3508d0f912179e00d8a5f1c39` |
| `~/.omp/agent/mcp.json` | 600 | 429 | 2026-10-20 13:35:56.123987225 | `266078529e5b18f1dc165253c7c2037e6d60edecae0873506c93f95d20bbd9d4` |
| `~/.kimi-code/config.toml` | 600 | 135717 | 2026-10-19 16:09:51.321720218 | `14ef62599580f36f7c4d4447701fb4a179713879f35dc3686005b109323f5e1f` |

Hashes re-taken after all reads were identical (exit 0) — the seat wrote nothing to these files.

Entry shape (observation, JSON parsed):
- Devin `keys = [args, command, env]`, `'enabled' in entry = False`, pin `6.7.0` (`mcp_config.json:3-14`;
  `:3` `"rea": {`, `:4` `"command": "npx"`, `:7` `"rea-agents@6.7.0"`).
- OMP `keys = [args, command, env, type]`, `'enabled' in entry = False`, pin `6.7.0`
  (`mcp.json:3-16`; `:4` `"type": "stdio"`, `:8` `"rea-agents@6.7.0"`).
- Kimi: block `[mcp_servers.rea]` opens at `config.toml:4124`; `:4125` `command = "npx"`;
  `:4126` `args = [ "-y", "rea-agents@6.7.0", "mcp" ]`; `:4127` `startup_timeout_sec = 30`;
  env subtable at `:4129-4131` sets 2 keys (`GHIDRA_INSTALL_DIR`, `JAVA_HOME`) and does **not** set
  `REA_JADX_MCP_JAR`, which both JSON clients do (Devin `:13`, OMP `:14`). No `enabled`-equivalent key
  in the block (grep of `enabled` in 4120-4140 empty; the only `enabled` hits in the file are
  unrelated provider/model keys at `:4019`, `:4040`, `:4061-4063`).

## The OMP `enabled` flag: present at 10:15, dropped at 13:35:56 (observation chain)

Retained copies in `~/.omp/agent/`:

| copy | size | sha256 | content |
|---|---|---|---|
| `mcp.json.pre-disable-20261020T1015` | 429 | `38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b` | pin `6.5.0`, **no** flag; mtime preserved at 2026-10-14 17:53:20.392671581 |
| `mcp.json.rea.backup.e571…recovery` | 453 | `e571d192…d61ad9` (= filename) | pin `6.5.0` (`:8`) **plus** `"enabled": false` (`:16`); mtime 2026-10-20 13:35:56.**123157217** |
| `mcp.json` (live) | 429 | `266078529…bbd9d4` | pin `6.7.0` (`:8`), **no** flag; mtime 13:35:56.**123987225** |

- `diff -u mcp.json.pre-disable-20261020T1015 mcp.json` → exit 1; single hunk, only `6.5.0`→`6.7.0`.
  The 10:15 "pre-disable" copy therefore records the state *before* the disable: 6.5.0, no flag.
- `diff -u <e571 recovery> mcp.json` → exit 1; exactly two changes in one hunk:
  `- "rea-agents@6.5.0"` / `+ "rea-agents@6.7.0"` and `-      },` `-      "enabled": false` / `+      }`.
- Byte arithmetic closes the loop: 453 − 429 = 24 = 23 (`      "enabled": false\n`) + 1 (`},`→`}`).
  The recovery copy was written 0.8 ms before the live file, so the flag was removed by the same
  write that bumped the pin.
- No other file in `~/.omp` or `~/.config/devin` was touched in 13:35:00-13:37:00 except the two
  `mcp*` files and their recovery copies (`find -newermt` window, exit 0); `~/.omp/agent/config.yml`
  (mtime 15:24:50) contains no `mcp`/`rea`/`enabled`-for-mcp record (grep exit 0, only
  `3:enabledModels:`). So the disable was not relocated anywhere I can observe.
- Devin parallel: `mcp_config.json.rea.backup.16f4…recovery` (406 B, mtime …120449714 minus 1.3 ms)
  → live is pin-only (`6.5.0`→`6.7.0`, `diff` exit 1). Devin never carried an `enabled` key in any
  retained copy (303 B `mcp_config.json.rea.backup:7` is `6.4.0`; `grep '"enabled"'` on the live file
  exit 1).

Observation: as of 2026-10-20 16:35:56Z the live OMP entry carries no `enabled` key and pins 6.7.0.
Inference [INFERENCE]: a pin-bump tool rewrote the entry from a canonical template (the recovery
naming and the 13:35:56 1-ms backup are that tool's signature) and lost the `false`; the operator
disable added at 10:15 survives only in the recovery copy. The before-state at 10:15 is *observed*
(config.yml-free, pre-disable copy), the attribution to a template rewrite is not.

## Live server consequence (observation, not inference)

- `pgrep -af rea-agents` → PID **3221** `npm exec rea-agents@6.5.0 mcp`, started
  **Tue Oct 20 09:57:31 2026 -0300** (`ps -o lstart,etime` → elapsed 05:43:19). That predates both
  the 10:15 disable and the 13:35 re-pin, so OMP's running MCP surface is still **6.5.0** while the
  file says 6.7.0. A restart is required for the file to take effect; until then any
  `doctor --client omp` that reads the file and any live `binary_session` will disagree.
- No 6.7.0 MCP server process exists (`pgrep -af 'rea-agents@6.7.0'` matched only a concurrent peer's
  `doctor --client devin --client omp --client kimi` invocation, PID 3149015 — not this seat's).
- This seat's own tool surface lists the rea MCP routes, consistent with an absent `enabled` key
  meaning enabled. Whether OMP's loader defaults absent to true was **not** re-probed (no loader doc
  read); that is the one open inference. The operator prohibition in `contract.md:35` stands as a
  directive regardless of the flag's absence.

## What C2 / PROVINCE must change (anchors, not edits)

- `PROVINCE.md:9` "Devin and OMP use `rea-agents@6.5.0` (207 … `805433f1…`)" → both now 6.7.0;
  `:10-11` Kimi 6.7.0 sentence stays true.
- `PROVINCE.md:16` "Devin `rea-agents@6.5.0` (`…/mcp_config.json:7`)" → value stale, anchor correct;
  `:17` OMP `6.5.0` (`…/mcp.json:8`) → value stale, anchor correct; `:18` Kimi `6.7.0`
  (`config.toml:4126`) → value and anchor both still correct.
- Decide explicitly whether PROVINCE should state the OMP disable state. It cannot state it as a
  live config fact: that would be false since 13:35:56 today. Either state "no `enabled` key in the
  live file; flag last recorded in `mcp.json.rea.backup.e571….recovery:16`" or omit the disable from
  the pin sentence and leave it a contract-only directive.
- Calibration note for `province-pins.py`: if the probe asserts only the pin token, expect exactly 2
  mismatches at baseline (Devin, OMP) as claims say; if it also asserts `enabled == false` for OMP it
  will report a third, today-caused finding. Pin the probe's contract before freezing it.
- Registry cross-check (for the `NpmRegistrySource` row): `dist-tags.latest = 6.7.0`; 6.7.0 published
  `2026-10-18T08:12:05.640Z`, 6.5.0 `2026-10-14T12:56:14.513Z`; **no 6.6.0 exists** (`npm view
  rea-agents@6.6.0` → E404, exit 1) — versions run 6.5.0, 6.7.0. 6.7.0 `dist.shasum =
  11f23ba377303a5c28b3162180cf2bf3f3643708`, integrity `sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwR
  UOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==`.
- Adjacent handoff (`NpxCaches` seat, not my remit): the live npx caches are `a1722018f28f9df2` =
  6.7.0 and `ad9a3fdbcad992c6` = 6.5.0 (both `node -p version` exit 0); **`dea9475797100b20`
  (`/…/6.4.0`) no longer exists** (`ls -ld` exit 2), which falsifies `PROVINCE.md:12` "both versions
  have separate npx cache installs" as read with `:21-23`, and `:45`'s 6.4.0 row anchor.

## Commands run (each with its exit)

| command | exit | yield |
|---|---|---|
| `stat -c '%n mtime=%y size=%s mode=%a'` + `sha256sum` on the three configs | 0 | identity table |
| `grep -n -i rea ~/.config/devin/mcp_config.json` / `-E 'rea\|enabled' ~/.omp/agent/mcp.json` | 0 / 0 | `:7`, `:3,:8,:14` — no `enabled` line |
| `grep -n 'rea-agents@' ~/.kimi-code/config.toml` | 0 | single hit `:4126` |
| `sed -n '4124,4134p' ~/.kimi-code/config.toml` | 0 | block structure |
| `grep -n '"enabled"' ~/.config/devin/mcp_config.json` | 1 | absent (grep: no match) |
| `diff -u mcp.json.pre-disable-20261020T1015 mcp.json` | 1 | pin-only hunk |
| `diff -u <e571 recovery> mcp.json` | 1 | pin + flag-drop hunk |
| `diff -u <devin 16f4 recovery> mcp_config.json` | 1 | pin-only hunk |
| `python3 -c` json parse of both JSON clients | 0 | key sets, `enabled_in=False` |
| `pgrep -af rea-agents` / `ps -o pid,lstart,etime,args -p 3221` | 0 / 0 | 6.5.0 server, start 09:57:31 |
| `pgrep -af 'rea-agents@6.7.0'` | 0 | peer doctor only, no server |
| `node -p …package.json.version` for both cache dirs | 0 | `6.7.0`, `6.5.0` |
| `ls -ld ~/.npm/_npx/dea9475797100b20` | 2 | missing |
| `npm view rea-agents dist-tags --json` / `… time --json` / `… versions --json` | 0 / 0 / 0 | latest + publish times |
| `npm view rea-agents@6.6.0 version` | 1 (E404) | version absent |
| `find ~/.omp/agent ~/.config/devin -maxdepth 1 -newermt …` | 0 | only the 5 mcp/recovery files |
| `git -C LANE diff --name-only B refs/heads/main -- PROVINCE.md` | 0 (empty) | PROVINCE unchanged |
| `sha256sum` re-run on the three configs | 0 | identical to first pass |

Tooling: no installs, no upgrades, no pacman/uv/npx package additions (the only `npx` traffic was
`npm view`, which is registry metadata). Nothing written outside this report.

## Observed vs inferred vs unknown

Observed: every pin value, line number, size, mtime and sha256 above; both diffs; the live 6.5.0
server process and its start time; the missing 6.4.0 cache; the registry timestamps; PROVINCE's
baseline text at the cited lines.

Inferred [INFERENCE]: that the 10:15 disable wrote the `enabled: false` line (before-state observed
via the pre-disable copy, after-state observed via the 13:35 recovery); that the 13:35 bump tool
regenerated the entry without carrying the flag; that absent `enabled` means enabled for OMP's loader.

Unknown: OMP's loader default for an absent `enabled` (not probed); whether a 6.7.0 OMP server
serves the same 207-tool surface (no 6.7.0 server started — that is `Doctor67`/`ReaCatalogRecompute`
territory); operator intent about restoring the flag (configs are operator-owned — not edited here).
