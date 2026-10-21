# Disposition review — `cutter-command` (R22-C2)

Author-side support review, not an outside admission. Scoped to the single
T2 verb `cutter-command`; lane repo read-only except this report. No target,
device, or hook executed; no Cutter session existed to contact, and none was
contacted. Client used per contract: `npx -y rea-agents@6.5.0` (already in the
npx cache; no install performed).

## 1. CLI surface (`--help`, `--schema`)

Observed 2026-10-21:

```text
$ npx -y rea-agents@6.5.0 cutter-command --help        # exit 0
Usage: rea cutter-command <sessionId> <expectedGeneration> <command> [options]
  sessionId           Session ID copied from list-cutter-sessions.
  expectedGeneration  Session generation returned by list-cutter-sessions.
  command             One unrestricted Rizin command to run in Cutter.
Options: --json; plus global --format/--full-output/--schema/--filter-output/...
```

```text
$ npx -y rea-agents@6.5.0 cutter-command --schema      # exit 0
args required[3]: sessionId, expectedGeneration, command
  sessionId          string, format uuid, anchored pattern — versions 1–8
                     UUIDs PLUS the two sentinels
                     00000000-0000-0000-0000-000000000000 and
                     ffffffff-ffff-ffff-ffff-ffffffffffff
  expectedGeneration integer, 0 ≤ n ≤ 9007199254740991
  command            string, minLength 1
  additionalProperties: false
options: json:boolean (default false); additionalProperties: false
```

All three parameters are positional on the CLI; no file/device/serial/host
input exists. The verb has exactly one input surface: a (sessionId,
generation, command) triple.

## 2. Exact valid non-contact probe parameters

A non-contact probe is one where no live Cutter bridge session can be
addressed, so `command` can never be dispatched. Two disjoint gates give
that guarantee:

- **Schema-gate (invalid arguments):** any non-UUID `sessionId` and/or
  non-integer `expectedGeneration` fails argument validation before any
  session lookup. Retained receipt: `cutter-command.json` +
  `cutter-command.run.json` —
  `cutter-command kaidoku-r22-nonexistent kaidoku-r22-nonexistent i` →
  exit 1, `error.code = VALIDATION_ERROR` with per-field `fieldErrors`.
- **Existence-gate (schema-valid, session nonexistent):** `sessionId` must
  pass the UUID pattern, so the only guaranteed-nonexistent values are the
  two schema-sentinel UUIDs or a fresh random UUID. `expectedGeneration` any
  integer in range (0 used). Retained receipt: `cutter-command-missing.json`
  + `cutter-command-missing.run.json` —
  `cutter-command ffffffff-ffff-ffff-ffff-ffffffffffff 0 i` → exit 1,
  `error.code = invalid_request`, `category = invalid_input`,
  `retryable: true`, `duration: 2ms`.

Independent re-probe this review (not previously retained):

```json
argv: ["npx","-y","rea-agents@6.5.0","cutter-command",
       "00000000-0000-0000-0000-000000000000","0","i",
       "--format","json","--full-output"]
exit: 1
stdout: {"ok":false,"error":{"code":"invalid_request","category":"invalid_input",
        "message":"Analysis input is invalid. Check the arguments and try again.",
        "retryable":true,"remediation":{"action":"Correct the listed arguments
        and retry."}},"meta":{"command":"cutter-command","duration":"2ms"}}
stderr: ""
```

Same envelope as the all-`f` sentinel: the refusal is an input/session-
identity check, identical across both schema-accepted sentinel UUIDs.
`command = i` (read-only Rizin info) is a belt-and-suspenders choice — the
triple is undispatchable regardless of command text because no session with
that ID exists; a hostile command string would be equally non-contact.

## 3. Does the absent-session control support `frontier-blocked`?

**Yes — `frontier-blocked` is the calibrated placement; `adjacent` would be
the weaker claim.**

- The absent-client control for this verb is an absent *session*, not an
  absent client binary (unlike the ADB rows' `REA_ADB_PATH=/usr/bin/false`).
  Its complement `list-cutter-sessions` returned `ok-empty:sessions` —
  discovery is functional, zero live sessions observed at that instant. So
  the operative path (Rizin command channel inside a bridged Cutter session)
  is unreachable for a capability reason, not a lane-policy reason.
- `adjacent` in this grammar means ground the lane refuses or defers
  (cf. Frida rows: hooking/process-ownership is refused adjacent ground).
  Running Rizin commands inside a Cutter session is not refused adjacent
  ground per se — it is blocked only by the absence of a session to
  address. `frontier-blocked` matches the ADB/TShark rows' semantics:
  typed refusal before operative contact, provider-side capability surface
  not held.
- Calibration caveat (must not be overclaimed): `invalid_request` proves
  only that this specific (sessionId, generation) triple is undispatchable.
  It does NOT prove the Cutter bridge is absent, that a *live* session would
  reject commands, or provider unavailability over time — the receipt is
  `retryable: true` and the code is `invalid_input`, not
  `capability_unavailable`. The row's `reason` states exactly this
  ("Well-formed nonexistent UUID/generation rejected"), which is honest.
  The section preamble's "no device operation was dispatched" covers the
  same non-contact property. The counter's own `limit` field applies:
  "receipt/row agreement at one revision; not provider availability over
  time".

## 4. Row vs counter grammar (`count-c2.py`)

Frozen PROVINCE.md row (§ `### Round-22 catalog dispositions`):

```text
| cutter-command | frontier-blocked | cutter-command | error:invalid_request |
  .ufo/waves/round-22/evidence/c2/cutter-command-missing.json |
  Well-formed nonexistent UUID/generation rejected; earlier malformed
  argument receipt retained separately |
```

Against the grammar in `tools/count-c2.py` (`check()`, lines 87–121):

- placement `frontier-blocked` ∈ PLACEMENTS ✓
- receipt under `RECEIPT_PREFIX`, present at rev, strict-JSON envelope with
  `meta.command == "cutter-command" == probe == verb` ✓
- `observed = error:invalid_request` requires `ok == false` and
  `error.code == "invalid_request"` — the cited receipt is exactly that
  (single-line envelope, `ok:false`, `code:"invalid_request"`) ✓
- falsifier "receipt error code differs from observed" not tripped; the
  earlier `VALIDATION_ERROR` receipt is *not* the cited one, which is why
  citing `cutter-command-missing.json` (existence-gate) rather than
  `cutter-command.json` (schema-gate) is the correct choice: the row claims
  a well-formed-argument refusal.

Observed counter run this review (bounded, read-only):

```text
$ python3 -I -B .ufo/waves/round-22/tools/count-c2.py \
    --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev HEAD
exit 0 — accounted_count 14/14, mismatched [], foreign_rows [],
per_verb.cutter-command.status = "matched"
```

(HEAD = `2ee3d9f` "round-22: retain static frontier evidence and calibrated
catalog dispositions". Working-tree `count-c2.py` carries a docstring +
unused-import diff only; row-grammar unchanged.)

## 5. RecoverReceipts.json

**Not yet available.** `.ufo/waves/round-22/w2/` contains only
`swarm-registry.json` at review time, and no `RecoverReceipts.json` exists
anywhere under `.ufo/`. No verb-envelope review against it was possible.

## 6. Commands executed (all observed)

| argv | exit | stderr | result |
|---|---|---|---|
| `npx -y rea-agents@6.5.0 cutter-command --help` | 0 | — | usage/args text above |
| `npx -y rea-agents@6.5.0 cutter-command --schema` | 0 | — | JSON schema above |
| `npx -y rea-agents@6.5.0 cutter-command 00000000-0000-0000-0000-000000000000 0 i --format json --full-output` | 1 | empty | `invalid_request`/`invalid_input`, 2ms |
| `python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root <lane> --rev HEAD` | 0 | — | 14/14 matched |
| `git -C <lane> log/status/diff` | 0 | — | read-only repo state |

## 7. Verdict

Disposition supportable: `cutter-command` → `frontier-blocked` via the
existence-gate non-contact control (sentinel or random UUID + in-range
generation + any ≥1-char command → `invalid_request`, exit 1). The cited
receipt, placement, `observed` grammar token, and reason are all consistent;
the counter independently reports `matched`. Residual risk: the row rests on
a session-absence refusal, so it calibrates "no dispatchable session" — it
does not evidence that the Cutter bridge itself works or fails. No blocker.
