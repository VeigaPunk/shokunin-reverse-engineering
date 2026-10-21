# R22-C2 disposition review — `list-frida-processes`

Seat: `KaidokuR22R.DispositionListFridaProcesses-6` — independent disposition
support review. Read-only: no code writes, no device/remote/hook contact, no
production-file mutation. Scope files: `count-c2.py`, `PROVINCE.md`, the verb's
committed receipt pair, CLI `--help`/`--schema`, and the bundled provider code.
Author-side findings only; not outside admission.

## Verdict

| verb | row as committed (HEAD `2ee3d9f`) | counter status | independent verdict |
|---|---|---|---|
| `list-frida-processes` | `adjacent` / probe `list-frida-processes` / `ok-field:device_id="local"` / receipt `.ufo/waves/round-22/evidence/c2/list-frida-processes.json` | **matched** (counter run, exit 0, see below) | **Supported — `adjacent` is the only honest placement.** `frontier-blocked` is unreachable: no absent-client control exists for this verb (see Finding 1). |

## Commands run and observed results

1. `npx -y rea-agents@6.5.0 list-frida-processes --help` → exit 0.
   Options printed: `--remote-address`, `--token`, `--certificate`, `--origin`,
   `--keepalive-interval`, `--device-id` plus globals (`--format`, `--full-output`,
   `--schema`, `--llms`, `--token-*`, `--filter-output`). No env knob is advertised.
2. `npx -y rea-agents@6.5.0 list-frida-processes --schema` → exit 0. JSON Schema:
   `options` object with `remoteAddress/token/certificate/origin/keepaliveInterval/deviceId`,
   all optional, `additionalProperties: false`; no required fields.
3. `python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root <LANE> --rev HEAD` →
   **exit 0**; `accounted 14/14`, `mismatched []`, `foreign_rows []`,
   `per_verb["list-frida-processes"].status = "matched"`. (Committed counter at
   HEAD; the working-tree copy adds a `probe == verb` check this row also passes.)
4. Receipt re-parse: `list-frida-processes.json` → `ok: true`,
   `meta.command: "list-frida-processes"`, `data.device_id: "local"`,
   `data.processes`: 149 entries of `{pid, name, identifier:null}`.
   `.run.json` → argv `npx -y rea-agents@6.5.0 list-frida-processes --format json
   --full-output`, `env_overrides: {}`, exit 0, stderr empty.

## Findings (by severity)

### F1 — No absent-client control exists for this verb; `frontier-blocked` cannot be honestly produced (supports `adjacent`)

- REA 6.5.0 implements Frida as a **bundled npm dependency**: `node_modules/frida`,
  invoked in-process via `await import("frida")` in
  `dist/frida/FridaInstrumentationManager.js:39`. There is no external binary to
  substitute, unlike ADB's `REA_ADB_PATH` (present in `dist/adb/AdbConfiguration.js`
  and `CapabilityInventory.js`).
- Exhaustive env-key enumeration of `dist/` shows **no `REA_FRIDA_*` key**
  (grep over the package: adb/jadx/apktool/binwalk/wakaru/tshark/sigrok/wabt/
  unblob/browser/ghidra keys all present; nothing for frida).
- A control was already attempted by this lane:
  `.ufo/waves/round-22/verify/frida-unsupported-env.json` records
  `REA_FRIDA_PYTHON=/usr/bin/false rea-agents@6.5.0 list-frida-devices` →
  **exit 0**, provider enumerated normally;
  `finding: "undocumented_override_did_not_disable_provider"`,
  `control_pass: false`. The undocumented knob does nothing.
- Therefore the only `capability_unavailable` path for this verb is genuine
  provider failure (dynamic `import("frida")` failure or device-lookup timeout)
  — which cannot be induced by a caller control without tampering with the
  package (would also invalidate the recorded `tools_sha256`). An `error:` row
  claiming `frontier-blocked` could not be labeled an "explicit unavailable-client
  control" the way the ADB rows are.
- Consequence: honest placements for `list-frida-processes` are `adjacent`
  (observed local enumeration — what the row says) or `adjacent` with an
  `error:` observed (a refusal is not provider absence — same precedent as
  `instrument-with-frida`'s `error:capability_unavailable`/`adjacent` row).
  `frontier-blocked` has no constructible, non-deceptive probe.

### F2 — `ok-field:device_id="local"` is the correct observed grammar and the row reasons correctly

- Counter grammar (`count-c2.py` `check()`): `ok-field:<dotted>=<json>` requires
  `env.ok === true` and `strict(data.device_id) === strict("local")`. The receipt
  satisfies both. `probe` equals `verb` and `meta.command` equals probe — all
  three identities hold.
- CLI default resolution (`dist/cli/fridaCommands.js` `listFridaProcesses`):
  with no flags, `service.listProcesses({ deviceId: options.deviceId ?? "local" })`
  — bare argv deterministically selects `"local"`. The receipt's
  `device_id: "local"` is the direct consequence of a bare invocation, exactly
  as `.run.json` records (`env_overrides: {}`).
- Reason text is accurate: the envelope carries pid/name only
  (`identifier: null` everywhere observed) — no command lines, no hooks, no
  runtime ownership. Enumerating local process names is read-only observation,
  and PROVINCE.md explicitly lists "Frida-style hooking" as Adjacent/unowned —
  consistent with `adjacent`, not core-claim or blocked ground.
- The `instrument-with-frida` sibling row (`adjacent`,
  `error:capability_unavailable`, PID 2147483647 refusal) and PROVINCE's note
  "the Frida enumeration provider was available; the missing impossible PID does
  not establish provider absence" corroborate that the provider is held —
  reinforcing that `frontier-blocked` would misreport this verb.

### F3 — Parameter surface: valid non-contact vs. contact probes

- **Strictly non-contact** (never touch the frida provider or a device):
  `--help`, `--schema`, `--llms`/`--llms-full`. All exit 0 and emit static text.
- **Provider-contact but lane-legal** (local enumeration, no remote, no mutation,
  no hook): bare argv; `--device-id local`; `--device-id <bogus>` (local lookup
  refusal — still no remote contact; any resulting `error:` is `adjacent` per F1
  precedent, never `frontier-blocked`); `--format`, `--full-output`,
  `--filter-output`, `--token-*` (all still enumerate).
- **Forbidden by lane bounds** (remote connection): `--remote-address` and its
  companions `--token`, `--certificate`, `--origin`, `--keepalive-interval`
  (schema enforces credentials require `remoteAddress`; `deviceId` and
  `remoteAddress` are mutually exclusive).

### F4 — `RecoverReceipts.json`: not yet available

`.ufo/waves/round-22/w2/` contains only `swarm-registry.json`
(`ls` verified 2026-10-21; `RecoverReceipts.json` ENOENT). The requested
envelope-review of this verb against row grammar/operation on that file is
**not yet available — skipped by absence**, not failed. The committed receipt
pair was reviewed instead (above) and is internally consistent.

## Residual risk / verification gaps

- Counter was exercised at `HEAD` (`2ee3d9f`), where the row+receipt are
  committed; at baseline `7787fea` the section and receipt do not exist, so the
  verb is `unaccounted` — matching the frozen `before_expected`.
- `git status` shows `count-c2.py` modified in working tree (docstring probe==verb
  note + unused `import re` removal); evaluated row passes both committed and
  working-tree grammars — no row-level risk either way.
- The bundled `frida` npm version was not read from its own package.json in this
  pass (dependency is a real `node_modules/frida` dir; version pin is REA's, not
  a caller knob) — noted as cosmetic gap, no bearing on the disposition.
- A bogus `--device-id` lookup-failure probe was reasoned but **not executed**;
  its `error:` code was not needed since the existing `ok-field` row is already
  matched. Executing it would remain `adjacent`-class evidence, not
  `frontier-blocked`.

## Tooling log

No installs or updates performed (pacman paused host-wide; none needed).
`npx -y rea-agents@6.5.0` resolved from the existing pinned cache
`~/.npm/_npx/ad9a3fdbcad992c6` (tools_sha256 `805433f1…` per PROVINCE).
No target execution, no device/remote contact, no hooking, no lane mutations;
only this report written under `w2/`.
