# DispositionInspectAdbPackage — independent disposition support review

Seat: `KaidokuR22R.DispositionInspectAdbPackage-6` — author-side review only, not
outside admission. Scoped to `inspect-adb-package` under claim R22-C2
(calibration), baseline `7787fea4d6fd718726de92ed20759d11ce7b8b48`, measured
lane HEAD `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`.

## Verb surface (REA CLI, rea-agents@6.5.0)

`rea inspect-adb-package` help (exit 0) and `--schema` (exit 0) establish:

- Grammar: `rea inspect-adb-package <serial> <package>` — two required
  positionals, both `type: string, minLength: 1`; `additionalProperties: false`;
  no verb-specific options. Only global output flags apply
  (`--format`, `--full-output`, `--filter-output`, `--token-*`, `--llms*`,
  `--schema`, `--help`).
- `serial` is declared "exactly as `adb devices` reports it" — the verb cannot
  meaningfully run serial-free; a planted serial is the honest probe form.
- Sibling adb verbs `inspect-adb-client --schema` and `list-adb-devices
  --schema` (both exit 0) take **zero** args (`properties: {}`,
  `additionalProperties: false`) — they are the serial-free members of the
  family.

Exact valid non-contact probe parameters: any two non-empty strings for
`<serial> <package>` under `REA_ADB_PATH=/usr/bin/false`. The produced probe
(`run.json`) used `kaidoku-r22-no-device` / `com.example.none` with
`--format json --full-output`; both placeholders satisfy the schema and are
never resolved, because the client gate fires first.

## Disposition row vs receipt (counter-verified)

PROVINCE.md `### Round-22 catalog dispositions` row:
`| inspect-adb-package | frontier-blocked | inspect-adb-package |
error:capability_unavailable | .ufo/waves/round-22/evidence/c2/inspect-adb-package.json
| Explicit false-client control refused version inspection before device
contact; real client/device unexamined |`.

Receipt `.ufo/waves/round-22/evidence/c2/inspect-adb-package.json`:
`ok:false`, `error.code:"capability_unavailable"`,
`category:"unsupported_provider"`, `retryable:false`,
`details.provider_id:"adb"`, `details.operation:"inspect_adb_package"`,
`meta.command:"inspect-adb-package"`, `duration:"6ms"`.
Run record `inspect-adb-package.run.json`: argv as above,
`env_overrides.REA_ADB_PATH="/usr/bin/false"`, `exit:1`, stdout = the envelope,
`stderr:""`.

`python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root . --rev HEAD`
→ exit 0; `accounted_count:14/14`, `mismatched:[]`, `foreign_rows:[]`,
`per_verb.inspect-adb-package.status:"matched"`. Row grammar (`error:` needs
`ok==false` + `error.code` equality; `probe` must equal `verb` and
`meta.command`) is satisfied exactly.

## Could the absent-client control support `frontier-blocked` or `adjacent`?

Supports **frontier-blocked**: the refusal is a shared client-side version gate.
Fresh corroborating probe (same control, serial-free verb):

```
REA_ADB_PATH=/usr/bin/false npx -y rea-agents@6.5.0 list-adb-devices \
  --format json --full-output
exit 1, stderr ""
stdout: {"ok":false,"error":{"code":"capability_unavailable",
"category":"unsupported_provider","message":"The selected adb binary did not
report a usable version.",...,"details":{"provider_id":"adb",
"operation":"list_adb_devices","reason":"The selected adb binary did not
report a usable version."}},"meta":{"command":"list-adb-devices","duration":"6ms"}}
```

Identical envelope on a zero-arg verb proves the gate runs before serial
resolution, package lookup, or any adb protocol exchange — an explicit
unavailable-client control, not a device check. `frontier-blocked` is the
calibrated label: the lane names a gap it does not hold (adb device surface,
22/24 verbs need a live device per PROVINCE frontier notes).

Does **not** support `adjacent`: adjacent rows in this table (`list-frida-*`,
`instrument-with-frida`) mean the provider was reached and enumerated real
state, with the lane deferring ownership — `ok:true` payloads or an
impossible-PID refusal. Here the provider itself never initialized; nothing
was enumerated, deferred, or observed about devices.

Does **not** support any device-availability claim: the control cannot
distinguish "no adb client", "no device", or "no package" — all collapse into
the same client-gate refusal, so no row grammar can extract a device finding
from this envelope. The row's `reason` already states this correctly
("real client/device unexamined").

## Findings by severity

No actionable defects in scope.

- **Info** — disposition row, receipt, and counter all agree; `matched` at
  HEAD `2ee3d9f`.
- **Residual risk** — the `error:capability_unavailable` envelope is
  client-gate ambiguity by construction; calibration holds only because the
  row reason scopes the claim. Any future edit reinterpreting this envelope
  as device absence would be a defect.
- **Gap** — `count-c2.py` in the working tree differs from committed HEAD:
  docstring now documents the `probe == verb` equality already enforced by the
  code, and unused `import re` was dropped. Semantics unchanged; the counter
  result above used the working-tree script against committed artifacts.
- **Gap** — `inspect-adb-client`/`list-adb-devices` (the 2 serial-free verbs)
  are not in T2; this review is envelope-support only and asserts nothing
  about their live-client behavior (historical r4u-06 records provider adb
  37.0.0 — a different, real-client probe).

## RecoverReceipts.json

**Not yet available.** `.ufo/waves/round-22/w2/` contained only
`swarm-registry.json` at review time; per assignment, no verb-envelope review
was performed against it.

## Commands run (all non-contact, no target/device/hook, no production mutation)

| argv | exit | stdout/stderr |
|---|---|---|
| `npx -y rea-agents@6.5.0 inspect-adb-package --help` | 0 | usage text above / empty |
| `npx -y rea-agents@6.5.0 inspect-adb-package --schema` | 0 | schema above / empty |
| `npx -y rea-agents@6.5.0 inspect-adb-client --schema` | 0 | empty-args schema / empty |
| `npx -y rea-agents@6.5.0 list-adb-devices --schema` | 0 | empty-args schema / empty |
| `REA_ADB_PATH=/usr/bin/false npx -y rea-agents@6.5.0 list-adb-devices --format json --full-output` | 1 | envelope above / `""` |
| `python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root . --rev HEAD` (cwd lane) | 0 | JSON `accounted_count:14`, `matched` / empty |
| `git log/status/diff` read-only inspections | 0 | HEAD `2ee3d9f`, tree state above |

Tooling: no installs performed (pacman paused host-wide; none needed).
`rea-agents@6.5.0` resolved via the existing npx cache; record: tool
rea-agents, version 6.5.0, channel npx cache, reason = contract-pinned CLI.
Companion machine-readable record: `DispositionInspectAdbPackage.json`.

## Residual risk / verification gaps

- Envelope ambiguity noted above is inherent to the control; mitigated by the
  row's explicit reason text.
- Counter verifies row↔receipt agreement at one revision, not provider
  availability over time (its own declared `limit`).
- This seat reviewed support for the existing disposition only; it does not
  re-execute the production probe or admit the wave.
