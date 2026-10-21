# Disposition support review — `start-adb-activity` (R22-C2 row)

Seat: `KaidokuR22R.DispositionStartAdbActivity-6`, recovery wave w2.
Baseline `7787fea4d6fd718726de92ed20759d11ce7b8b48`; lane HEAD observed `2ee3d9f`
("round-22: retain static frontier evidence and calibrated catalog dispositions").
Author-side support only; no admission. Lane read-only except this report and its
same-name attachment `DispositionStartAdbActivity.json`. No target run, no device
contact, no hook, no production mutation. REA exercised only via `npx -y
rea-agents@6.5.0`; every adb-family invocation carried `REA_ADB_PATH=/usr/bin/false`
— an explicit unavailable-client control, never a device-availability observation.

## Findings (severity order)

1. **No defect against the `start-adb-activity` row/receipt pair.** The row at
   `PROVINCE.md` HEAD line 197 —

   `| start-adb-activity | frontier-blocked | start-adb-activity | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/start-adb-activity.json | Explicit false-client version refusal; no activity start or device mutation |`

   — satisfies every clause the frozen C2 counter checks
   (`.ufo/waves/round-22/tools/count-c2.py`): placement in
   `{frontier-blocked, adjacent}`; non-empty reason; receipt under
   `.ufo/waves/round-22/evidence/c2/` with no `..`; receipt is strict-JSON
   (single-member objects, finite numbers) and a REA envelope with
   `meta.command == "start-adb-activity" == verb == probe`; `observed`
   `error:capability_unavailable` matches `ok:false` +
   `error.code:"capability_unavailable"` in the committed receipt
   (`{"ok":false,"error":{"code":"capability_unavailable","category":"unsupported_provider","message":"The selected adb binary did not report a usable version.",...,"details":{"provider_id":"adb","operation":"start_adb_activity",...}},"meta":{"command":"start-adb-activity","duration":"5ms"}}`).
   Exactly one table row names the verb (no `duplicate_rows`); the verb is in
   the frozen `T2` tuple; the receipt file is committed at HEAD
   (`git ls-files` confirms tracking; `git show HEAD:...` resolvable), so
   `receipt_absent` cannot trigger at `--rev HEAD`. This row counts as
   `matched` under the counter as written.

2. **Load-bearing flag: `--full-output`.** Without it the CLI prints the bare
   error object (`code/category/message/...`) with no `ok` field and no `meta`
   object — such a receipt would score `receipt_not_envelope` or
   `observed_mismatch`, not `matched`. Observed 2026-10-21:
   `start-adb-activity x y` → exit 1, bare object; `… --format json` → exit 1,
   bare object. Only `--format json --full-output` yields the counter-required
   `{ok, error, meta}` envelope. The frozen `.run.json` argv carries exactly
   those flags. Any regenerated receipt MUST keep `--full-output`.

3. **Placement calibration: `frontier-blocked` is supported, `adjacent` is
   not, by this verb's structure.** The refused envelope is produced by the
   adb provider gate (`details.provider_id:"adb"`, reason: selected binary did
   not report a usable version) — a client-side refusal before any serial or
   `am start` dispatch. For this device-mutating verb no `ok` outcome exists
   that does not contact a device: `ok-empty`/`ok-field` grammar entries are
   unreachable without real adb + device, i.e. outside the no-contact contract.
   So the only honest observed value this control can ever produce is an
   `error:<code>` row → `frontier-blocked`. `adjacent` would require either an
   `ok` observation (impossible non-contact) or a lane-ownership refusal
   reading, which the verb does not supply — the tool *tried* the provider and
   was refused; it did not decline the domain. The preamble line ("ADB rows are
   explicit `REA_ADB_PATH=/usr/bin/false` unavailable-client controls, NOT
   observations of device absence") is the honest reading the row requires.

4. **Calibration caveat (known limit, already declared).** The counter binds
   `observed` to `error.code` only; it cannot distinguish a false-client
   refusal from an identical-code refusal for other causes. Mitigation present
   in-tree: `start-adb-activity.run.json` pins argv + `env_overrides:
   {"REA_ADB_PATH":"/usr/bin/false"}` + exit 1 + stdout/stderr, and the section
   preamble states the control explicitly. The counter's own `limit` field
   ("receipt/row agreement at one revision; not provider availability over
   time") scopes the claim. No row change needed; this is residual risk, not a
   mismatch.

5. **Working-tree counter drift is cosmetic.** `git diff HEAD
   count-c2.py` = docstring clause ("with `probe` equal to the row's `verb`" —
   documents the existing `row["probe"] != row["verb"]` check) + removal of
   unused `import re`. Row grammar and verdicts identical; this review used the
   working-tree file and re-verified against HEAD.

## Exact non-contact probe shape (from `--help` and `--schema`, 2026-10-21)

```
rea start-adb-activity <serial> <action> [--data-uri s] [--component s] [--extra t:k:v ...]
```

- `serial` (positional, required): string minLength 1 — "Device serial exactly
  as `adb devices` reports it". A sentinel (`kaidoku-r22-no-device` /
  `kaidoku-r22r-review-no-device`) is never dereferenced under the false-client
  gate; the refusal precedes serial resolution.
- `action` (positional, required): string minLength 1 — the intent action.
- `--data-uri`, `--component`: optional strings minLength 1; `--extra`:
  repeatable `type:key:value` (declared types string/boolean/int/long/float per
  help text; CLI schema enforces only string minLength 1, no max-items bound —
  the "up to 16 typed extras" bound in the tool description is provider-side,
  unreachable under this control). None are needed for the probe; all are
  intent payload that is never dispatched.
- Envelope flags required for row grammar: `--format json --full-output`.
- `args`/`options` schema objects both `additionalProperties:false`; no hidden
  serial-free or dry-run flag exists — the only non-contact path is the
  unavailable-client gate itself.
- Exit code is **1** on the refusal (envelope `ok:false`); 0 is unreachable
  without a device. `--schema` exit 0, `--help` exit 0.

## Bounded confirmation probes run this seat (false-client control, /tmp cwd)

| # | argv tail (prefix `REA_ADB_PATH=/usr/bin/false npx -y rea-agents@6.5.0`) | exit | stdout | stderr |
|---|---|---|---|---|
| 1 | `start-adb-activity --help` | 0 | usage text (above) | — |
| 2 | `start-adb-activity --schema` | 0 | args/options schema (above) | — |
| 3 | `schema start-adb-activity` | 0 | `COMMAND_NOT_FOUND` error body | — |
| 4 | `start-adb-activity kaidoku-r22r-review-no-device android.intent.action.VIEW --format json --full-output` | 1 | `{"ok":false,"error":{"code":"capability_unavailable","category":"unsupported_provider","message":"The selected adb binary did not report a usable version.",...,"details":{"provider_id":"adb","operation":"start_adb_activity",...}},"meta":{"command":"start-adb-activity","duration":"6ms"}}` | (empty) |
| 5 | `start-adb-activity x y` | 1 | bare error object, no `ok`/`meta` | — |
| 6 | `start-adb-activity x y --format json` | 1 | bare error object, no `ok`/`meta` | — |

Probe 4 reproduces the frozen receipt byte-for-byte except `duration`
(5ms→6ms) and the sentinel serial — deterministic refusal, consistent with a
gate that runs before serial/argument use. The envelope cannot prove which
internal check failed beyond the message; `provider_id:"adb"` +
`operation:"start_adb_activity"` confirm the adb provider refused before
dispatch. Full argv/env/exit/stdout/stderr also in
`DispositionStartAdbActivity.json` (same-name attachment).

## RecoverReceipts.json status

**Not yet available.** `.ufo/waves/round-22/w2/` contained only
`swarm-registry.json` at review time; `RecoverReceipts.json` does not exist, so
no verb-envelope vs. row-grammar review of that artifact was possible. If it
lands later, the applicable grammar is the counter's: `meta.command` must equal
the row's `probe`, `probe` must equal `verb`, and `observed` must match
`error:`/`ok-empty:`/`ok-field:` semantics exactly — plus `--full-output`-shape
envelopes only.

## Residual risk / verification gaps

- The control says nothing about real adb client presence, device presence,
  or whether `am start` would have succeeded — by design; the row's reason and
  preamble already disclaim all three.
- `capabilities`/`doctor` cross-checks of the adb provider were not run (out of
  scoped seat; also the frozen row's claim needs only the refused envelope).
- If L1 ever regenerates the receipt without `--full-output`, the counter
  flips to `receipt_not_envelope` — see finding 2.

## Tooling record

No installs or updates performed. Used: `npx -y rea-agents@6.5.0` (already in
npm npx cache, pin per contract), git 2.x read-only subcommands, coreutils.
Channel: n/a. Reason: n/a.
