# Disposition support review — `instrument-with-frida` (R22-C2, w2)

Seat: `KaidokuR22R.DispositionInstrumentWithFrida-6` · author-side review only ·
2026-10-21 · lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` ·
REA CLI pin: `rea-agents@6.5.0` (npx cache `~/.npm/_npx/ad9a3fdbcad992c6`,
catalog `tools_sha256 805433f1…`).

**Verdict:** the frozen row `instrument-with-frida | adjacent |
error:capability_unavailable` is supported. `adjacent` is the **maximum honest
placement** for this verb on this host — an absent-client control like the ADB
rows' `REA_ADB_PATH=/usr/bin/false` does not exist for the Frida provider, so
`frontier-blocked` is not defensible. All findings below are observations from
static sources and non-contact CLI probes; no process was attached, spawned, or
hooked, and no remote endpoint was contacted.

## 1. CLI surface (observed, exit 0)

`npx -y rea-agents@6.5.0 instrument-with-frida --help` (exit 0):

```
Usage: rea instrument-with-frida <attach|spawn> <target> [options]
  mode    Attach to a PID or spawn a program
  target  Process ID for attach or program path for spawn
  --remote-address / --token / --certificate / --origin / --keepalive-interval
  --device-id / --script / --script-file / --argument / --duration-ms (default 1000)
```

`--schema` (exit 0): `args` requires `mode∈{attach,spawn}` + `target`
(minLength 1); `options`: `remoteAddress`(1..2048), `token`, `certificate`,
`origin`, `keepaliveInterval`(int>0), `deviceId`(minLength 1), `script`,
`scriptFile`(minLength 1), `argument` (string array), `durationMs`
(int, 0..60000, default 1000). Both objects are `additionalProperties:false`.

Refinement rules read in `dist/cli/fridaCommands.js` (6.5.0):

- exactly one of `--script`/`--script-file` (lines 155–163);
- `attach` target must match `^[1-9][0-9]*$` and be a safe integer > 0
  (lines 168–177);
- `--remote-address` and `--device-id` are mutually exclusive (line 152);
- any credential/connection option without `--remote-address` is rejected
  (`remoteAddressRequired`, lines 70–74);
- `--remote-address` grammar: host[:port≤65535], no userinfo/path/query
  (`dist/contracts/fridaRemoteAddress.js`).

## 2. Valid non-contact probe parameters (this run, all exit 1)

Three refusal layers, cheapest first; each was re-run under this seat and
records are in `DispositionInstrumentWithFrida.json`:

| argv tail | observed envelope | layer |
|---|---|---|
| `attach abc --script x` | `error.code=invalid_request`, issue `attach mode needs a positive integer process ID.` (1 ms) | CLI input validation, zero provider contact |
| `attach 2147483647` (no script source) | `error.code=invalid_request`, `Provide exactly one of --script or --script-file.` (1 ms) | CLI input validation |
| `attach 2147483647 --script x` (wave-1 argv) | `error.code=capability_unavailable`, `provider_id=frida`, `operation=start_frida_session`, `reason="Unable to find process with pid 2147483647"` (14 ms in wave-1 receipt) | provider refused at `device.attach(pid)` — local device session, missing PID |
| `attach 2147483647 --device-id kaidoku-r22-nonexistent --script x` | `error.code=capability_unavailable`, `reason="Device not found"` (1057 ms ≈ `DEVICE_LOOKUP_TIMEOUT_MS=1000`) | local device enumeration misses unknown id; no remote contact |
| `spawn /kaidoku-r22-nonexistent-program --script x` | `error.code=capability_unavailable`, `reason="Unable to find executable at '/kaidoku-r22-nonexistent-program'"` (11 ms) | spawn refused before exec — nothing ran |
| `attach 1 --script x --token foo` | `error.code=VALIDATION_ERROR` (CLI arg envelope, *different shape* — not the REA analysis envelope), `Remote credentials and connection options require remoteAddress` (1 ms) | incur/zod arg validation |

Notes on ordering (read in
`dist/application/frida/FridaInstrumentationService.js:149–180`): `instrument`
= `startSession` → `loadScript` → duration window → detach/cleanup. A script is
only loaded after a session exists, so all rows above guaranteed **zero script
delivery** — the wave-1 `--script "// inert"` was never sent. `--script-file
<nonexistent>` cannot be a pre-attach probe: `readFile` runs inside
`loadScript`, after attach.

`spawn` with a real path or `attach` with a live PID crosses the contact line —
both are banned by this seat's contract (no target execution/attach) and by
PROVINCE.md Adjacent ("Frida-style hooking (unowned)"). `--remote-address`
crosses the no-remote-connections ban even on a loopback literal, so remote
refusals were not probed.

## 3. Absent-client control: **unsupported** — `frontier-blocked` not available

The ADB rows earned `frontier-blocked` through an explicit client-absence
control: `REA_ADB_PATH=/usr/bin/false` → `capability_unavailable` ("The selected
adb binary did not report a usable version") before any device I/O (receipts
`evidence/c2/*adb*.run.json`).

No equivalent exists for Frida:

- Package-wide grep of `dist/` finds **zero `REA_FRIDA*` keys**; the Frida
  provider is the vendored `frida` npm module loaded in-process
  (`dist/frida/FridaInstrumentationManager.js:39`,
  `(await import("frida")).getDeviceManager()` — no external binary, no
  `process.env` reads in any `frida*.js`).
- Wave verify artifact `.ufo/waves/round-22/verify/frida-unsupported-env.json`
  already executed the natural guess: `REA_FRIDA_PYTHON=/usr/bin/false
  list-frida-devices` → **exit 0, `ok:true`, devices enumerated**
  (`finding: "undocumented_override_did_not_disable_provider"`,
  `control_pass:false`). The guess names no live key; it is a negative control,
  not a device check.
- The provider is proven live on this host: `list-frida-devices` →
  `ok-field:cleanup_error=null`; `list-frida-processes` →
  `ok-field:device_id="local"` (both adjacent rows, receipts in `evidence/c2/`).

Consequence for the claim's `not_claimed` list ("provider availability over
time"): the wave-1 `capability_unavailable` is a **missing-process refusal on a
live provider** (provider resolved, `attach` failed), never provider absence.
That is precisely adjacent semantics ("ground the lane refuses or defers …
never absorbed"): the provider is reachable while the lane defers hooking.
`frontier-blocked` would require a receipt where the capability itself is
unavailable; no supported control produces one, so `adjacent` is the maximal
defensible placement.

## 4. Row-grammar check vs `count-c2.py`

Frozen row (PROVINCE.md `### Round-22 catalog dispositions`):

```
| instrument-with-frida | adjacent | instrument-with-frida |
  error:capability_unavailable |
  .ufo/waves/round-22/evidence/c2/instrument-with-frida.json |
  PID2147483647 is not a real selected process; missing-process refusal is not
  provider absence |
```

Against `count-c2.py` (`check()`, lines 87–121):

- `placement "adjacent"` ∈ `PLACEMENTS` ✓; `reason` non-empty ✓;
- `receipt` under `.ufo/waves/round-22/evidence/c2/`, no `..` segments ✓;
- receipt decodes as strict JSON; `meta.command == "instrument-with-frida" ==
  probe == verb` ✓;
- `observed "error:capability_unavailable"` ↔ receipt `ok:false` +
  `error.code:"capability_unavailable"` ✓ (verbatim receipt shown in §5);
- `probe` column equals `verb`, so `probe_mismatch` impossible.

Cross-check run this seat (read-only):
`python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root . --rev HEAD`
(HEAD = `2ee3d9f`) → **exit 0**, `accounted_count:14/14`, `mismatched:[]`,
`foreign_rows:[]`, `instrument-with-frida` status `matched`.

## 5. Wave-1 receipt audit (`evidence/c2/instrument-with-frida{,.run}.json`)

```
argv: npx -y rea-agents@6.5.0 instrument-with-frida attach 2147483647
      --script "// inert" --format json --full-output
env_overrides: {}   exit: 1   stderr: ""
stdout: {"ok":false,"error":{"code":"capability_unavailable",
  "category":"unsupported_provider","retryable":false,
  "details":{"provider_id":"frida","operation":"start_frida_session",
  "reason":"Unable to find process with pid 2147483647"}},
  "meta":{"command":"instrument-with-frida","duration":"14ms"}}
```

`2147483647` (2³¹−1) is statically impossible on this host
(`/proc/sys/kernel/pid_max` = 4194304), matching `capture-probes.py`'s stated
intent. `capture-probes.py` applies `REA_ADB_PATH` only to `adb` verbs
(`'adb' in verb`); the frida run used ambient env, which is correct — the probe
asserts provider-live-missing-target, not client-absence. Consistent with
`reason` text and with this seat's §2 repros.

## 6. `w2/RecoverReceipts.json`

**Not yet available.** Checked 2026-10-21: absent. `wave2-spec.json` does name a
`RecoverReceipts` wave item (receipt-set rebuild for the frozen 14), but no
envelope exists to review, so the verb-envelope row-grammar check requested for
that file cannot be performed. The frozen receipts in `evidence/c2/` (reviewed
in §§4–5) remain the operative receipts until that file lands.

## 7. Residual risk / verification gaps

- The probe's `error.code` is `capability_unavailable` although the provider is
  live — a reader could misread the code as provider absence. The `reason`
  column and `details.provider_id=frida` + missing-PID text carry the
  correction; row grammar only checks `code`, not `details.reason` (counter
  limitation, not a defect).
- `spawn` probe refuses *before* exec on a nonexistent path; a path that exists
  but is non-executable was not probed (same refusal class expected [INFERENCE]).
- `--remote-address` connect-refusal class (e.g. refused loopback) unprobed by
  contract; expected `capability_unavailable` after connect timeout
  [INFERENCE].
- `REA_FRIDA_PYTHON` absence-of-effect was verified on `list-frida-devices`
  only; no other candidate key was tested because none exists in the package.
- `RecoverReceipts.json` review deferred by absence (§6).

## Commands run by this seat (all read-only / non-contact)

| command | exit |
|---|---|
| `npx -y rea-agents@6.5.0 --help` | 0 |
| `npx -y rea-agents@6.5.0 instrument-with-frida --help` | 0 |
| `npx -y rea-agents@6.5.0 instrument-with-frida --schema` | 0 |
| `npx -y rea-agents@6.5.0 list-frida-devices --help` / `list-frida-processes --help` | 0 |
| `instrument-with-frida attach abc --script x` | 1 (`invalid_request`) |
| `instrument-with-frida attach 2147483647` (no script source) | 1 (`invalid_request`) |
| `instrument-with-frida attach 2147483647 --device-id kaidoku-r22-nonexistent --script x` | 1 (`capability_unavailable`, Device not found) |
| `instrument-with-frida spawn /kaidoku-r22-nonexistent-program --script x` | 1 (`capability_unavailable`, executable not found) |
| `instrument-with-frida attach 1 --script x --token foo` | 1 (`VALIDATION_ERROR`) |
| `python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root . --rev HEAD` | 0 (14/14 matched) |
| `git log/status`, `grep` over `dist/` and `.ufo/`, `cat /proc/sys/kernel/pid_max` | 0 |

No tool installs performed or needed (pacman transactions paused host-wide;
npx cache for `rea-agents@6.5.0` already present).
