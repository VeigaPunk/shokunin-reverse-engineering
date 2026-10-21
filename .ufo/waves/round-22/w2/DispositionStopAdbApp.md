# Disposition support review — `stop-adb-app` (R22-C2, wave 2)

**Seat:** `KaidokuR22R.DispositionStopAdbApp-6` — author-side review only; not an
outside admission. **Date:** 2026-10-21. **Lane baseline:** `7787fea4d6fd718726de92ed20759d11ce7b8b48`.
**Lane repo:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only except this report).

No target execution, no debug attach, no device contact, no Frida, no remote
connection, no production-file mutation. ADB environment: no adb probing was run
at all for the `--help`/`--schema` reads (they are CLI-local); the existing
receipt was produced under the explicit `REA_ADB_PATH=/usr/bin/false`
unavailable-client control.

---

## 1. CLI surface (rea-agents@6.5.0, observed this session)

Commands actually run (from `/tmp`, no lane writes):

| # | argv | exit | stdout/stderr |
|---|------|------|----------------|
| 1 | `npx -y rea-agents@6.5.0 --help` | 0 | 153-command list; `stop-adb-app` present: "Force-stop every process of one package". stderr empty. |
| 2 | `npx -y rea-agents@6.5.0 stop-adb-app --help` | 0 | `Usage: rea stop-adb-app <serial> <package>`; `serial` = "Device serial exactly as `adb devices` reports it"; `package` = "Package to force-stop". Global options only (`--format`, `--full-output`, `--schema`, `--llms`, `--token-*`, `--filter-output`). No verb-specific flags. stderr empty. |
| 3 | `npx -y rea-agents@6.5.0 stop-adb-app --schema` | 0 | YAML-form JSON Schema (verbatim below). stderr empty. |
| 4 | `REA_ADB_PATH=/usr/bin/false npx -y rea-agents@6.5.0 stop-adb-app --help` / `--schema` | 0 | Byte-identical output to runs 2–3 — **`--help`/`--schema` never resolve the adb client**; they are client-free by construction. |

Schema (run 3, verbatim):

```yaml
args:
  type: object
  properties:
    serial:
      type: string
      minLength: 1
      description: Device serial exactly as `adb devices` reports it
    package:
      type: string
      minLength: 1
      description: Package to force-stop
  required[2]: serial,package
  additionalProperties: false
```

### Exact valid non-contact probe parameters

- **Required, only:** two positional args `serial` and `package`, both
  `type: string, minLength: 1`. `additionalProperties: false` — no other args.
- **Non-contact discipline:** under the explicit unavailable-client control
  `REA_ADB_PATH=/usr/bin/false`, **any** two non-empty strings are valid probe
  parameters because the refusal fires at client-version resolution, before
  serial validation or device contact (receipt `duration:"5ms"`,
  `retryable:false`). The existing receipt uses placeholder values
  `serial=kaidoku-r22-no-device`, `package=com.example.none` — chosen so that
  even a hypothetical bypass could not name a real device/package.
- Output shaping used by the existing receipt: `--format json --full-output`
  (global options; do not affect provider reach).
- **Boundary note:** omitting either positional is a *CLI-parse* failure, not
  the `error:capability_unavailable` provider envelope the row grammar needs;
  the probe must supply both args to reach the provider-selection layer.

## 2. Row-grammar and receipt agreement (count-c2.py)

`.ufo/waves/round-22/tools/count-c2.py` (read at worktree state):

- `stop-adb-app` is a frozen T2 verb (line 32). `PLACEMENTS = {"frontier-blocked","adjacent"}` — the counter accepts **either** label; it validates receipt↔row agreement only, never the placement's semantic fit.
- Grammar for `observed`: `error:<code>` requires envelope `ok==false` and `error.code==<code>`; `ok-empty:<dotted>` requires `ok==true` and empty list at `data.<dotted>`; `ok-field:<dotted>=<json>` requires `ok==true` and `data.<dotted>` equal to the JSON literal.
- `check()` also requires: `probe == verb == meta.command`; receipt path under `.ufo/waves/round-22/evidence/c2/` with no `..`; strict-JSON decode (duplicate members and non-finite numbers refused); `reason` non-empty.

Existing PROVINCE row (§ "Round-22 catalog dispositions", line 198):

```
| stop-adb-app | frontier-blocked | stop-adb-app | error:capability_unavailable |
  .ufo/waves/round-22/evidence/c2/stop-adb-app.json |
  Explicit false-client version refusal; no app stop or device mutation |
```

Existing receipt `.ufo/waves/round-22/evidence/c2/stop-adb-app.json` (verbatim):

```json
{"ok":false,"error":{"code":"capability_unavailable","category":"unsupported_provider",
 "message":"The selected adb binary did not report a usable version.","retryable":false,
 "remediation":{"action":"The selected adb binary did not report a usable version."},
 "details":{"provider_id":"adb","operation":"stop_adb_app",
 "reason":"The selected adb binary did not report a usable version."}},
 "meta":{"command":"stop-adb-app","duration":"5ms"}}
```

Sibling `.run.json`: argv `npx -y rea-agents@6.5.0 stop-adb-app kaidoku-r22-no-device com.example.none --format json --full-output`, env `REA_ADB_PATH=/usr/bin/false`, **exit 1**, stdout = the envelope above, stderr empty.

Per-`check()` evaluation (walked by hand, not executed): placement ∈ PLACEMENTS ✓; reason non-empty ✓; receipt under prefix, no `..` ✓; strict-parseable (no dup keys/non-finite — verified by eye, single-level members) ✓; `meta` dict present, `meta.command == "stop-adb-app" == probe == verb` ✓; `observed` is `error:capability_unavailable` and envelope has `ok===false`, `error.code==="capability_unavailable"` ✓ → **`matched`**. The row satisfies the counter's complete condition set.

## 3. Placement verdict: does the absent-client control support `frontier-blocked` or `adjacent`?

**Supported: `frontier-blocked`. Not supported: `adjacent`.**

- What the control observed: REA's adb provider refused at **client-version
  resolution** — `category:unsupported_provider`, "The selected adb binary did
  not report a usable version" — because `/usr/bin/false` exits 1 with no
  output. The envelope never reached serial handling, daemon startup, or the
  device. It proves only: *this selected client is unusable → the verb cannot
  reach its operation*.
- It is **not** a device-availability observation. Nothing in the receipt
  speaks to devices: no enumeration ran, no `adb devices` output exists, the
  serial was never validated. PROVINCE's own section header states exactly this:
  ADB rows are "explicit `REA_ADB_PATH=/usr/bin/false` unavailable-client
  controls, NOT observations of device absence or of the real adb binary."
- Placement semantics as the lane applies them (consistent across all five ADB
  rows): `frontier-blocked` = the verb's operation is unreachable on this host
  (capability gap named honestly); `adjacent` = the provider *did* respond with
  substance, and what was observed sits on ground the lane declines to own.
  The `stop-adb-app` receipt shows a hard capability wall, not exercised-then-
  declined ground — matching the Frontier bullet "adb device surface — 22/24
  verbs need a live device/emulator" and Core row "ADB client (device-free):
  only 2/24 verbs are serial-free".
- Asymmetry check vs the `adjacent` frida rows: `list-frida-devices`/
  `list-frida-processes` returned `ok:true` data (provider alive, enumeration
  observed); `instrument-with-frida`'s impossible-PID `capability_unavailable`
  still proves the provider layer answered a *process-selection* refusal —
  adjacent because dynamic hooking is refused ground and the provider was
  demonstrably present. `stop-adb-app`'s refusal is one layer earlier
  (client selection), so even the "provider answered" leg of the adjacent
  pattern is absent.
- Residual judgment honesty: a force-stop is device mutation, and "Non-REA
  dynamic analysis" is listed Adjacent — one *could* argue the verb class is
  unowned. But the observed evidence supports only the stronger, narrower
  claim: the capability was unavailable before any device semantics were
  reached. `frontier-blocked` is the defensible row; `adjacent` would claim
  ground (exercised verb, declined ownership) the receipt does not evidence.
- The counter is blind to this distinction (both labels pass `check()`), so
  placement justification rests entirely on the `reason` text — the existing
  wording is accurate and sufficient.

## 4. RecoverReceipts.json status

**Not yet available.** `.ufo/waves/round-22/w2/` contains only
`swarm-registry.json` (plus this report); no `RecoverReceipts.json` exists to
review the `stop-adb-app` verb envelope against. The row-grammar analysis in §2
was done directly against `count-c2.py` and the existing c2 receipt instead.

## 5. Findings

1. **Receipt↔row agreement holds** — the existing `stop-adb-app` row evaluates
   to `matched` under `count-c2.py`'s complete check set (walked manually; all
   six gates pass). [observation]
2. **`frontier-blocked` is the supported placement** — the
   `REA_ADB_PATH=/usr/bin/false` control yields a pre-device
   `capability_unavailable`/`unsupported_provider` refusal; it evidences an
   unreachable verb, not exercised-and-declined ground, and says nothing about
   device availability or the real adb binary. [observation + lane-taxonomy
   inference]
3. **Non-contact probe parameter set is minimal and exact** — two non-empty
   strings `<serial> <package>`; `--help`/`--schema` are client-free by
   construction (identical output with and without the false-client env).
   [observation]
4. **Mutation safety is structural** — the recorded probe is a device-mutating
   verb that provably mutated nothing: refusal at client selection, 5 ms,
   `retryable:false`, and the run record's exit-1 envelope documents no app
   stop occurred. [observation]
5. **No defect found** in the row, receipt, or counter handling for this verb.
   The only residual risk is counter-blindness to placement semantics (§3),
   which is inherent to the frozen grammar, not a row error.

## 6. Tooling record

No installs or updates performed or needed. Used: `npx -y rea-agents@6.5.0`
(resolves from the existing npx cache per PROVINCE; zero network-dependent
install by this seat), host `cat`/`ls`/`grep`. Pacman untouched (host-wide pause
honored). RULES.md read before any tooling consideration.

## 7. Limitations / unknowns

- `count-c2.py` was read and its check logic walked by hand; the counter itself
  was not executed (a `git show` at baseline would see no rows anyway —
  `before_expected` says 0/14 at baseline). [inference: hand-walk, not run]
- The real adb binary's availability on this host is **unknown by design** —
  the control intentionally never resolved it; per contract this is an
  unavailable-client control, not a device or real-client check.
- Whether a real-client run would refuse a dead serial as `capability_unavailable`
  or a different code is unprobed and irrelevant to this row's honesty.
