# DispositionListFridaDevices — R22-C2 `list-frida-devices` disposition support review

Author-side review; not an outside admission. Scope: the single T2 verb
`list-frida-devices` — its CLI parameter surface, absent-client-control
feasibility, and the existing `### Round-22 catalog dispositions` row vs. the
counter grammar in `.ufo/waves/round-22/tools/count-c2.py`. No target executed,
no device contacted, no hook, no remote connection, no production-file mutation.
Package sources under `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6` (rea-agents
6.5.0, the contract-pinned carrier catalog) were read statically.

## Commands exercised (exact argv / observed exit)

| argv | exit | key output |
|---|---|---|
| `npx -y rea-agents@6.5.0 list-frida-devices --help` | 0 | verb options: `--remote-address`, `--token`, `--certificate`, `--origin`, `--keepalive-interval`; globals: `--format`, `--full-output`, `--filter-output`, `--llms(-full)`, `--schema`, `--token-*` |
| `npx -y rea-agents@6.5.0 list-frida-devices --schema` | 0 | `args: {type:object, properties:(none), additionalProperties:false}`; `options` = only the five remote knobs (see below) |
| `grep -rn "process\.env" dist/frida/ dist/cli/fridaCommands.js dist/contracts/frida{ToolContracts,RemoteAddress}.js dist/application/frida/` | 1 (no matches) | zero environment reads in the entire Frida code path |
| `grep -n REA_FRIDA\|FRIDA_\|frida_path` across 6.5.0 dist | — | only constants (`FRIDA_PROVIDER_IDENTITY`, `FRIDA_KEEPALIVE_INTERVAL_DESCRIPTION`, `FRIDA_TOOL_CONTRACTS`); no client-selection env key |

`--help`/`--schema` are metadata surfaces; the verb itself was NOT executed —
the receipt already exists and executing it would be a Frida device-manager
enumeration outside this review's mandate.

## Finding 1 — Existing row is grammar-consistent (status: `matched` by static evaluation)

`PROVINCE.md` row: `| list-frida-devices | adjacent | list-frida-devices | ok-field:cleanup_error=null | .ufo/waves/round-22/evidence/c2/list-frida-devices.json | Provider successfully enumerated local descriptors; not provider absence, remote connection, or lane ownership |`

Checked against `count-c2.py:87-121` `check()`:

- `placement=adjacent` ∈ PLACEMENTS; `reason` non-empty; `receipt` under
  `.ufo/waves/round-22/evidence/c2/` with no `..` segments.
- `probe == verb` and receipt `meta.command == "list-frida-devices"` — pass.
- Receipt decodes strict JSON by inspection (unique keys at every level, no
  `NaN`/`Infinity`, envelope shape `{ok,data,meta}`).
- `ok-field:cleanup_error=null`: `dig(data,"cleanup_error")` → `null`; literal
  `null` parses via `strict` → `None`; `ok===true`. **matches → `matched`.**
- `.run.json` sidecar records argv `npx -y rea-agents@6.5.0 list-frida-devices
  --format json --full-output`, `env_overrides:{}`, exit 0, empty stderr;
  stdout is byte-identical to the receipt body.

The counter itself was NOT executed (no mid-flight counter runs; it also reads
via `git show` at the measured revision, so the receipt must be committed in
the integrated tree — an L1 integration responsibility, not a defect here).

## Finding 2 — `ok-field:cleanup_error=null` is tautological for the bare probe (weak observation, no defect)

`FridaInstrumentationManager.js:57-64`: `cleanupError` initializes to `null`
and is only reassigned when a remote device was retained and `#releaseRemote`
throws. The bare invocation never retains a remote, so `cleanup_error=null`
is guaranteed on every successful bare run — it attests "no remote cleanup was
attempted," not that enumeration succeeded. The real success signal lives in
`ok:true` + the `devices` array. Alternatives considered:

- `ok-field:devices=[{"deviceId":"local",...}]` is expressible grammar (the
  `ok-field` literal side runs through `strict`, so JSON arrays/objects are
  legal) but fragile — it commits to the full descriptor order/shape.
- `ok-empty:` cannot apply (`devices` is non-empty).

Recommendation-grade only: the row matches as written and the section preamble
already scopes it ("The Frida enumeration provider was available… No real
process was attached or hooked"). No change required for counter agreement;
noted for calibration honesty.

## Finding 3 — Exact valid non-contact probe parameter set

**Only the bare invocation** (`list-frida-devices` + optional global output
flags such as `--format json --full-output`) is a legal non-contact probe.
Every verb-specific option is a remote-endpoint knob, and none is usable:

- `--remote-address`: syntactically validatable
  (`contracts/fridaRemoteAddress.js` — host[:port], no userinfo/path), but its
  execution path is `#retainRemote → manager.addRemoteDevice` and awaiting the
  device promise (`FridaInstrumentationManager.js:761-791`) — a remote Frida
  connection attempt, forbidden by contract.
- `--token/--certificate/--origin/--keepalive-interval` without
  `--remote-address`: rejected by the `remoteAddressRequired` refine
  (`cli/fridaCommands.js:70-74`) as an input-grammar refusal (`invalid_request`
  class) — an option-validation receipt, not a capability observation;
  honest dispositions should not rest on it.
- There is no `--device-id`/`--serial` selector on this verb (the
  `getDeviceById` selector exists only on `list-frida-processes`,
  `cli/fridaCommands.js:94-98`), so an "impossible selector" control like
  `instrument-with-frida`'s PID 2147483647 is not expressible here.

## Finding 4 — No Frida absent-client control exists; `adjacent` is the only reachable honest placement

Unlike ADB, where `REA_ADB_PATH=/usr/bin/false` yields an explicit
unavailable-client control that refuses before device contact (`capability_
unavailable` receipts for the ADB T2 rows), the Frida provider has **no
caller-selectable client surface**:

- Client is the bundled `frida` npm binding loaded lazily via
  `(await import("frida")).getDeviceManager()` (`FridaInstrumentationManager.js:39`)
  — an in-process dependency, not a host binary.
- Zero `process.env` reads in `dist/frida/`, `dist/cli/fridaCommands.js`,
  `dist/contracts/frida*.js`, `dist/application/frida/` — no `REA_FRIDA_*` or
  equivalent key exists to point at `/usr/bin/false`.
- A `capability_unavailable` outcome would require the `import("frida")` /
  `getDeviceManager()` load to fail, i.e., breaking the installed package —
  forbidden package-install mutation, out of scope.

Consequence: for `list-frida-devices`, `frontier-blocked` is unreachable by
any legal non-contact probe; the only producible honest envelope is
`ok:true` (local descriptors enumerated) or an input-grammar refusal.
`adjacent` is the maximum-supportable disposition and the row's placement is
correct. One calibration subtlety: `devices` contains frida-core's built-in
descriptors (`local`, `socket`, `barebone`), which enumerate unconditionally —
the `ok` attests the bundled provider initialized and enumerated, NOT that any
attachable remote or physical device exists. The row reason already says
"not provider absence, remote connection, or lane ownership"; consistent.

## Finding 5 — `RecoverReceipts.json`: not yet available

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/w2/`
contained only `swarm-registry.json` at review time;
`.ufo/waves/round-22/w2/RecoverReceipts.json` is **absent — not yet
available**. Per assignment, the `list-frida-devices` verb envelope itself
(c2 receipt + `.run.json`) was the only envelope reviewed; Findings 1–2 cover
its row-grammar and operation consistency.

## Residual risks / verification gaps

- Counter agreement asserted by static evaluation of `check()` + receipt, not
  by an executed `count-c2.py` run (out-of-scope mid-flight verification; also
  requires the receipt committed at the measured rev).
- `meta.duration` and `run.json` exit/stdout/stderr are not grammar-checked by
  the counter — reviewed manually, consistent.
- Schema/help output is unversioned text; if a sibling re-pins the CLI the
  option surface should be re-read.
- `isValidFridaRemoteAddress` accepts `local`/`barebone` as remote addresses;
  a `frontier-blocked` attempt via a descriptor name that resolves locally is
  still a connection attempt — not a non-contact control.

## Tooling record

No installs. `npx` resolved `rea-agents@6.5.0` from the existing npx cache
(`~/.npm/_npx/ad9a3fdbcad992c6`, matching PROVINCE's recorded 6.5.0 cache
identity `tools_sha256 805433f1…`). Pacman transactions remain paused host-wide
per contract; only read-only invocations used.
