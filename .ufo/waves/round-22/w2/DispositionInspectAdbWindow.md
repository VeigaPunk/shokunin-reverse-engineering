# Disposition support review — inspect-adb-window (R22-C2)

Reviewer: KaidokuR22R.DispositionInspectAdbWindow-6 — author-side disposition
support only; no admission, no integration, no device/daemon contact.
Baseline: 7787fea4d6fd718726de92ed20759d11ce7b8b48. All probes via the round
carrier pin `npx -y rea-agents@6.5.0` (contract-mandated version).

## Verdict

The PROVINCE.md row for `inspect-adb-window` is **correctly formed and
correctly placed** as `frontier-blocked`. The absent-client control
(`REA_ADB_PATH=/usr/bin/false`) legitimately supports `frontier-blocked`
because the observed refusal is a provider client-gate
(`capability_unavailable`/`unsupported_provider`, `provider_id:"adb"`) that
fires *before* any adb daemon or device contact — it is an unavailable-client
control, NOT evidence of device absence and NOT evidence about the real adb
binary. `adjacent` would under-claim: the lane did not electively defer held
ground; the verb cannot execute at all under the configured client selection.

## RecoverReceipts.json

**Not yet available.** `.ufo/waves/round-22/w2/` contains only
`swarm-registry.json`; no `RecoverReceipts.json` exists to review. (Glob of
`w2/**` run 2026-10-21.) No verb-envelope review performed.

## Probe surface (observed, re-run this review)

`npx -y rea-agents@6.5.0 inspect-adb-window --help` → **exit 0**:

    Usage: rea inspect-adb-window <serial>
    Arguments:
      serial  Device serial exactly as `adb devices` reports it
    Global Options: --filter-output --format <toon|json|yaml|md|jsonl>
      --full-output --help --llms/--llms-full --schema --token-count
      --token-limit <n> --token-offset <n>

`npx -y rea-agents@6.5.0 inspect-adb-window --schema` → **exit 0**:

    args:
      type: object
      properties:
        serial: { type: string, minLength: 1,
                  description: Device serial exactly as `adb devices` reports it }
      required[1]: serial
      additionalProperties: false

### Exact valid non-contact probe parameters

- One positional `<serial>` (string, `minLength:1`, `required`,
  `additionalProperties:false`). Any non-empty token is grammar-valid; the
  frozen run uses the deliberately-nonexistent `kaidoku-r22-no-device`.
- No serial-free or dry-run flag exists: the only options are global output
  shapers (`--format`, `--full-output`, `--filter-output`, `--token-*`,
  `--schema`, `--llms`, `--help`). None changes provider behavior.
- Non-contact is achieved entirely by env: `REA_ADB_PATH=/usr/bin/false`
  makes the selected adb binary fail the client version gate, so the verb
  refuses before dispatching any adb command. This is the contract-mandated
  unavailable-client control, an explicit client-selection outcome — not a
  device check.

### Boundary control (observed)

`REA_ADB_PATH=/usr/bin/false npx -y rea-agents@6.5.0 inspect-adb-window
--format json --full-output` (serial omitted) → **exit 1**, envelope
`{"ok":false,"error":{"code":"VALIDATION_ERROR", ... fieldErrors:[{path:
"serial", code:"invalid_type", missing:true}]},"meta":{"command":
"inspect-adb-window"}}`. Argument validation precedes the provider gate; a
receipt built this way would carry `error:VALIDATION_ERROR` and would
**mismatch** the row's `error:capability_unavailable`. A serial token must be
supplied to reach the client gate.

## Receipt ↔ row agreement (counter-grammar check)

Row (PROVINCE.md `### Round-22 catalog dispositions`):

    | inspect-adb-window | frontier-blocked | inspect-adb-window |
      error:capability_unavailable |
      .ufo/waves/round-22/evidence/c2/inspect-adb-window.json |
      Explicit false-client control only; no focused window observed |

Against `count-c2.py` rules:

- placement `frontier-blocked` ∈ {frontier-blocked, adjacent} ✓
- reason non-empty ✓; receipt under `.ufo/waves/round-22/evidence/c2/`, no
  `..` segments ✓; exactly one row names the verb (T2 member) ✓
- `probe == verb == meta.command == "inspect-adb-window"` ✓
- observed grammar `error:<code>`: receipt strict-parses (no duplicate
  members, no non-finite numbers — verified by replaying the counter's
  strict hook, PYEXIT=0), `ok==false`, `error.code=="capability_unavailable"`
  → **matched**

Receipt body (`.ufo/waves/round-22/evidence/c2/inspect-adb-window.json`):

    {"ok":false,"error":{"code":"capability_unavailable","category":
    "unsupported_provider","message":"The selected adb binary did not report
    a usable version.","retryable":false,...,"details":{"provider_id":"adb",
    "operation":"inspect_adb_window",...}},"meta":{"command":
    "inspect-adb-window","duration":"5ms"}}

Run record (`.ufo/waves/round-22/evidence/c2/inspect-adb-window.run.json`):
argv `npx -y rea-agents@6.5.0 inspect-adb-window kaidoku-r22-no-device
--format json --full-output`, env `REA_ADB_PATH=/usr/bin/false`, exit 1,
stderr empty, stdout byte-identical to the receipt envelope.

### Re-run this review (independent, non-contact, cwd /tmp)

    REA_ADB_PATH=/usr/bin/false npx -y rea-agents@6.5.0 inspect-adb-window \
        kaidoku-r22-no-device --format json --full-output
    → exit 1, stderr empty; stdout identical to the receipt except
      meta.duration ("7ms" vs recorded "5ms" — nondeterministic field).

## Residual risk / gaps

- `count-c2.py` reads receipts via `git show <REV>:<path>`: the row counts
  only after PROVINCE.md and the receipt are committed at the measured
  revision — an L1 integration concern, not a row defect.
- `runs.json` aggregate and the sibling adb rows (`inspect-adb-package`,
  `list-adb-services`, `start-adb-app`/`stop-adb-app`) use the same
  serial token and env control and show the identical client-gate refusal;
  consistency across the adb block is coherent.
- The row never claims device absence; section prose states the controls are
  "NOT observations of device absence or of the real adb binary" — honest
  saturation wording holds for this verb.
- No findings requiring changes. No tool installs performed (none needed;
  npx cache already carried rea-agents@6.5.0 per PROVINCE.md).
