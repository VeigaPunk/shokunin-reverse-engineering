# R22-W2 disposition support review — `list-cutter-sessions`

Scope: author-side support review only. Reviews the actual PROVINCE.md
disposition row, its receipt, the counter grammar, and the pinned
`rea-agents@6.5.0` client implementation. No target execution, no device/hook,
no remote connection, no production mutation. All probes were local non-contact
controls (lstat-only paths; zero socket connects — verified by source below).

## Commands run (exact argv / exit / output)

| # | argv / env | exit | observed |
|---|---|---|---|
| 1 | `npx -y rea-agents@6.5.0 list-cutter-sessions --help` (cwd /tmp) | 0 | "List live Cutter instances connected through the REA Python plugin bridge"; `Usage: rea list-cutter-sessions` — no verb args; only global flags (`--format`, `--full-output`, `--filter-output`, `--llms`, `--schema`, `--token-*`, `--help`) |
| 2 | `npx -y rea-agents@6.5.0 list-cutter-sessions --schema` (cwd /tmp) | 0 | `args: { type: object, properties: (none), additionalProperties: false }` — empty arg set, extra args rejected |
| 3 | `REA_CUTTER_BRIDGE_DIR=/nonexistent-r22-control npx -y rea-agents@6.5.0 list-cutter-sessions --format json --full-output` | 0 | `{"ok":true,"data":{"sessions":[],"bridge_directory":"/nonexistent-r22-control","discovery_status":"no_live_bridge_found","bridge_directory_security":"not_checked"},"meta":{"command":"list-cutter-sessions","duration":"2ms"}}` |
| 4 | `REA_CUTTER_BRIDGE_DIR=/tmp npx -y rea-agents@6.5.0 list-cutter-sessions --format json --full-output` | 0 | `{"ok":true,"data":{"sessions":[],"bridge_directory":"/tmp","discovery_status":"bridge_directory_insecure","bridge_directory_security":"not_private"},"meta":{"command":"list-cutter-sessions","duration":"1ms"}}` |
| 5 | `git show HEAD:PROVINCE.md \| grep list-cutter-sessions` | 0 | row present at HEAD (line 189) |
| 6 | `git show HEAD:.ufo/waves/round-22/evidence/c2/list-cutter-sessions.json` | 0 | receipt committed at HEAD, byte-matches worktree copy |

Client identity: npx cache `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`,
`package.json` version 6.5.0, `dist/cutter/CutterBridgeClient.js`
sha256 `a035240ae9578834…`.

## Valid non-contact probe parameters

The verb takes **zero positional/named arguments** (`args.properties` empty,
`additionalProperties:false`). The complete non-contact control surface is:

- `REA_CUTTER_BRIDGE_DIR` env — the only selector. Overrides the default
  `~/.cache/rea/cutter-bridge` (or `%LOCALAPPDATA%\REA\CutterBridge` on win32)
  (`CutterBridgeClient.js:156-175`).
- Global CLI flags (`--format json --full-output`) — envelope shaping only.

Non-contact outcomes reachable **before any socket connect**
(`#readDescriptors`, `CutterBridgeClient.js:406-530`), each returning
`ok:true` with `sessions:[]` and a `discovery_status` discriminator:

- dir ENOENT → `discovery_status="no_live_bridge_found"`, security `not_checked` (probe #3)
- dir not-a-directory / symlink / non-private (wrong uid or mode&0o077≠0) →
  `discovery_status="bridge_directory_insecure"`, security `not_private` (probe #4)
- lstat other error / opendir failure → `"bridge_directory_unavailable"`, `not_checked`
- ≥256 descriptor candidates → `"bridge_directory_capacity_exceeded"`
- only after a private-verified directory do socket connects to `127.0.0.1:<port>`
  occur; a private dir with 0 or ≤256 invalid/mismatched descriptors also yields
  `sessions:[]` **without contact** but `security="private_verified"` — a stronger
  but config-heavier control.

`REA_ADB_PATH=/usr/bin/false` is **inapplicable here** (no adb fork in this
code path); the analogous explicit absent-client control for this verb is
`REA_CUTTER_BRIDGE_DIR` → nonexistent path, which deterministically short-circuits
at the ENOENT branch.

## Row-vs-grammar verdict (count-c2.py)

Frozen row: `list-cutter-sessions | frontier-blocked | list-cutter-sessions |
ok-empty:sessions | .ufo/waves/round-22/evidence/c2/list-cutter-sessions.json`.
Against `count-c2.py` semantics: `ok-empty:sessions` requires `ok==true` and
`data.sessions==[]` — receipt has `ok:true`, `data.sessions:[]` → **matched**.
`probe`==`verb`==`meta.command`=="list-cutter-sessions"; receipt inside
`RECEIPT_PREFIX`, strict-JSON clean; placement in PLACEMENTS. Row is
**grammar-consistent and counter-valid** at HEAD.

## Placement calibration

`frontier-blocked` is **defensible**: the ambient probe observed only the
empty-set path (`no_live_bridge_found` at an instant), and no `sessions_found`
capability was held. Caveats worth recording:

1. Ambient absence ≠ explicit control. The committed `run.json` shows
   `env_overrides:{}` — the row rests on the ambient default dir being absent,
   not an explicit `REA_CUTTER_BRIDGE_DIR` control. Probe #3 shows an explicit
   ENOENT control yields the identical `ok-empty` envelope **with the controlled
   path echoed in `bridge_directory`** — strictly better attribution, same
   grammar outcome. Recommended upgrade if the row is ever re-earned.
2. `security:"not_checked"` under ambient ENOENT conflates "no bridge dir" with
   "gate not exercised". The reason cell ("Empty discovered sessions at this
   instant only; security status not_checked") is honest and matches the source
   semantics, so the row stands — but `not_checked` is an artifact of the
   ENOENT short-circuit, not a checked-insecure finding.
3. An explicit-control `bridge_directory_insecure` observation (probe #4) would
   support an **adjacent** row in the same envelope grammar via
   `ok-field:discovery_status="bridge_directory_insecure"` — a demonstrated
   refusal-gate behavior rather than absent capability. `frontier-blocked`
   remains the correct placement for the current empty-set evidence.
4. Nothing in any non-contact configuration can evidence live-session
   enumeration; `sessions_found` requires a real Cutter + plugin socket. The
   verb cannot claim `sessions[]`-with-members support from these probes — the
   row does not claim it.

## RecoverReceipts.json

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/w2/RecoverReceipts.json`
— **not yet available** (w2/ contains only `swarm-registry.json` at review
time). Verb envelope could not be reviewed against it.

## Blockers / residual risk

- No blockers. Residual: the row's evidence strength is "ambient empty at one
  instant"; an explicit `REA_CUTTER_BRIDGE_DIR` control receipt would harden it
  without changing grammar or placement.
- Tool installs: none (npx cache hit; pacman untouched per pause).

Report: .ufo/waves/round-22/w2/DispositionListCutterSessions.md
