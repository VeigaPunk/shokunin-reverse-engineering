# R22-C2 disposition review — `list-adb-services`

Reviewer: `KaidokuR22R.DispositionListAdbServices-6` (author-side only, not outside admission)
Target verb: `list-adb-services` — frozen T2 row, `rea-agents@6.5.0` (baseline 7787fea4d6fd718726de92ed20759d11ce7b8b48, claims R22-C2).

## CLI surface (observed, `npx -y rea-agents@6.5.0`)

- `rea list-adb-services --help` → "List the device's binder services and interfaces"; one POSITIONAL arg `serial` ("Device serial exactly as `adb devices` reports it") plus global output flags only.
- `rea list-adb-services --schema` → `args: {type: object, properties.serial: {type: string, minLength: 1}, required: [serial], additionalProperties: false}`. No `--serial` flag; no device/emulator/env knobs.

## Exact valid non-contact probe parameters

- `serial` must be supplied as the first positional: type string, `minLength 1`. Content is arbitrary — a placeholder (e.g. `kaidoku-r22-no-device`) is valid because argument validation precedes the provider path and the serial is never echoed in the envelope.
- Validation ordering observed (each run under `REA_ADB_PATH=/usr/bin/false` — explicit unavailable-client control, not a device check):
  - missing serial → `{"ok":false,"error":{"code":"VALIDATION_ERROR", … invalid_type, path:["serial"]}}`, exit 1.
  - empty serial `""` → `VALIDATION_ERROR` ("Too small: expected string to have >=1 characters"), exit 1.
  - well-formed serial + extra positional (`probe-serial unexpected-extra-arg`) → extra arg silently ignored; reached the provider gate and produced the same `capability_unavailable` envelope, exit 1. CLI layer does NOT reject surplus positionals even though the schema says `additionalProperties:false`.
- `--format json --full-output` is required for a count-c2-valid receipt: the frozen grammar needs a top-level envelope with `meta.command == "list-adb-services"`.

## Control run (reproduced this review)

- argv: `REA_ADB_PATH=/usr/bin/false npx -y rea-agents@6.5.0 list-adb-services kaidoku-r22-no-device --format json --full-output`
- exit: 1; stderr: empty
- stdout: `{"ok":false,"error":{"code":"capability_unavailable","category":"unsupported_provider","message":"The selected adb binary did not report a usable version.","retryable":false,…"details":{"provider_id":"adb","operation":"list_adb_services",…}},"meta":{"command":"list-adb-services","duration":"6ms"}}`
- Byte-agreement with retained receipt `.ufo/waves/round-22/evidence/c2/list-adb-services.json` (differs only in `meta.duration`; the frozen receipt's `.run.json` records the same argv/env/exit 1).

## Row grammar + disposition verdict

Against `count-c2.py` `check()` semantics the frozen row
`| list-adb-services | frontier-blocked | list-adb-services | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/list-adb-services.json | … |`
is internally consistent: placement ∈ {frontier-blocked, adjacent}; receipt under `evidence/c2/`; strict-JSON envelope; `meta.command == probe == verb`; `ok==false` and `error.code == "capability_unavailable"` → evaluates `matched`. The serial placeholder does not appear in the envelope, so no grammar hazard.

**`frontier-blocked` is the correct and only defensible placement.**

- The probe is an explicit unavailable-client control (`/usr/bin/false` cannot report an adb version, so the provider refuses at client inspection, `operation:list_adb_services`, before any binder/serial contact). No adb daemon or device was touched; duration ~5-7ms.
- It supports a *gap* claim: the lane cannot exercise `service list` on this host without a real adb client + device, consistent with PROVINCE.md's "adb device surface — 22/24 verbs need a live device" frontier note and the sibling ADB rows.
- It does NOT support `adjacent`: `ok-field:`/`ok-empty:` grammar requires `ok==true` data, and adjacent semantics (exercised ground the lane declines to own) needs a successful provider observation, which this control cannot produce.
- It does NOT support a device-absence claim: the serial is never validated against a live bus; nothing about real adb binary presence, daemon state, or attached devices was observed. PROVINCE.md's ADB-row preamble states exactly this scope and is accurate.

## RecoverReceipts.json

`.ufo/waves/round-22/w2/RecoverReceipts.json` does **not yet exist** (w2 holds only `SimplifyC2.{json,md}`, `PrimaryTshark.{json,md}`, `swarm-registry.json` at review time) — verb-envelope vs row-grammar recheck against it is not yet available. The independent check above stands on the frozen receipt itself.

## Blockers / notes

- None blocking. No installs (npx cache `rea-agents@6.5.0` already resident); pacman untouched per pause.
- Residual: the false-client control cannot distinguish "adb absent" from "adb present but unusable" — both collapse to `capability_unavailable`; honest saturation wording in PROVINCE.md already says "unavailable-client controls, NOT observations of device absence or of the real adb binary".
