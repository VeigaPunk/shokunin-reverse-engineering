# DispositionInspectPcapCapture — disposition support review for `inspect-pcap-capture`

Seat: `KaidokuR22R.DispositionInspectPcapCapture-6` (leaf, author-side only; not outside admission).
Targets reviewed: REA 6.5.0 CLI `--help`/`--schema` for `inspect-pcap-capture`,
`.ufo/waves/round-22/tools/count-c2.py`, `PROVINCE.md` §"Round-22 catalog dispositions",
and the four TShark/pcap receipts under `.ufo/waves/round-22/evidence/c2/`.
Lane HEAD observed: `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67` (`git log --oneline -3`).
No installs, no pacman transaction, no target/device/hook/remote contact, no production edits.

## 1. Scope note on ADB-style controls

`REA_ADB_PATH=/usr/bin/false` (the lane's ADB control convention) does **not** apply to this verb
family. Grep of the 6.5.0 bundle shows `REA_ADB_PATH` referenced only in the MCP server bundle
(2 hits in `dist/mcp/main-kBXHZ8S5.js`); the pcap provider reads only `REA_TSHARK_COMMAND`,
`REA_CAPINFOS_COMMAND` (`dist/pcap/PcapConfiguration.js:4-5`) and
`REA_TSHARK_PRLIMIT_COMMAND` (default `/usr/bin/prlimit`, `dist/pcap/PcapNativeBound.js:6,21`).
The pcap analogue of the unavailable-client control is `REA_TSHARK_COMMAND`/`REA_CAPINFOS_COMMAND`,
probed in §4.

## 2. Exact valid non-contact probe parameters (observed)

### CLI surface, 6.5.0

| probe | argv | exit | observed |
|---|---|---|---|
| help | `npx -y rea-agents@6.5.0 inspect-pcap-capture --help` | 0 | `rea inspect-pcap-capture — Inspect one pcap/pcapng capture: endpoints, DNS, TLS SNI, and protocol distribution`; args: `path — Local pcap or pcapng capture file to inspect` |
| schema | `npx -y rea-agents@6.5.0 inspect-pcap-capture --schema` | 0 | `args: type object; properties: path (string, minLength 1); required[1]: path; additionalProperties: false` |
| client help | `npx -y rea-agents@6.5.0 inspect-pcap-client --help` | 0 | no verb-local arguments |
| client schema | `npx -y rea-agents@6.5.0 inspect-pcap-client --schema` | 0 | `properties:` (empty); `additionalProperties: false` |

So the complete CLI-valid non-contact invocation is exactly one positional `path` plus global
flags (`--format json --full-output` as receipted). No `--detail`, `--fields`, `--offset`, or
`--limit` exists at the CLI 6.5.0 layer. The MCP contract
(`dist/contracts/pcap/pcapToolContracts.js:22-25`) extends `inspect_pcap_capture` with a `detail`
field and retains facts for `inspect_analysis_view kind pcap` paging — that pagination surface is
MCP-session-only and not expressible in the 6.5.0 CLI, matching the PROVINCE-wide retained-evidence
convention.

### Path need not exist — source-verified

`dist/domain/pcap/pcapAnalysis.js:10-13`: input is
`z.strictObject({ path: localPathStringSchema })`; `localPathStringSchema` is
`nulFreeStringSchema.min(1)` (`dist/domain/localPath.js:18`) — a non-empty, NUL-free string, no
existence check. More importantly, the tool gate precedes any file access:
`dist/pcap/PcapProvider.js` `executeAdmitted` calls `this.client(request.operation, signal)`
(version probes of tshark/capinfos) **before** `PcapSnapshot.create()` and
`snapshot.capture(request.input.path, ...)`. A refusing selected tool therefore never reads the
capture file — the probe stays non-contact toward the artifact as well. (The receipted runs used
the lane's own 24-byte synthetic `empty.pcap`, global pcap header `d4c3 b2a1 …`, which is
lane-authored, not captured traffic.)

### Environment-key contract (6.5.0 source, `dist/pcap/PcapConfiguration.js:21-49`)

- `REA_TSHARK_COMMAND` / `REA_CAPINFOS_COMMAND`: if set and non-blank they must be **absolute**
  (`isAbsolute`), else `PcapConfigurationFailure("tshark_not_absolute"|"capinfos_not_absolute")`;
  if unset/blank, REA falls back to PATH name `tshark`/`capinfos` (`source: "path"`).
- Both tools must pass a `--version` probe parsed by
  `^<tool> \(Wireshark\) (\d+)\.\d+\.\d+` with major `4`; anything else is
  `version_unresolved`/`version_unsupported` (`PcapConfiguration.js:61-74`, provider `client()`).
- `inspectAvailabilityAdmitted` wraps any `PcapConfigurationFailure` into
  `pcapToolUnavailable` → `AnalysisCapabilityUnavailableError` → CLI `error.code
  = "capability_unavailable"`, `category "unsupported_provider"`
  (`analysisErrorProjection.js:145`); a refusing tool version probe maps to the same envelope via
  `PcapCommand.js:139-140`.
- Ordering note: the prlimit memory bound (`prepareCaptureBound`, `REA_TSHARK_PRLIMIT_COMMAND`,
  default `/usr/bin/prlimit`) is prepared **after** the client gate succeeds, so a false-client
  control never reaches it; `/usr/bin/prlimit` present on this host is recorded but unexercised
  by the refusal path.
- Concurrency: at most one in-flight inspection (`max_concurrent_inspections: 1`).

## 3. Host state at probe time (observed 2026-10-21)

`command -v`: `tshark` exit 1 (absent), `capinfos` exit 1 (absent), `dumpcap` exit 1 (absent),
`prlimit` → `/usr/bin/prlimit` exit 0. This reproduces PrimaryTshark's recorded host observation
independently.

## 4. Absent-client controls executed (bounded, non-contact; each refuses before any capture read)

| # | env | verb/argv | exit | envelope (observed) |
|---|---|---|---|---|
| A | (ambient PATH, as receipted) | `inspect-pcap-capture empty.pcap --format json --full-output` | 1 (receipted) | `capability_unavailable`, reason `Cannot run selected tool tshark: spawn tshark ENOENT` (`.run.json` line 15; duration 29ms) |
| B | `REA_TSHARK_COMMAND=/usr/bin/false REA_CAPINFOS_COMMAND=/usr/bin/false` | `npx -y rea-agents@6.5.0 inspect-pcap-capture .ufo/waves/round-22/evidence/c2/empty.pcap --format json --full-output` | 1 | `ok:false`, `error.code "capability_unavailable"`, category `unsupported_provider`, message `The selected tool /usr/bin/false cannot report its version: Command failed…`, `details.captured_output.stdout` = coreutils banner `false (GNU coreutils) 9.12 …`, `exit_code 1`; duration 83ms |
| C | `REA_TSHARK_COMMAND=/nonexistent-definitely-absent/tshark` | `npx -y rea-agents@6.5.0 inspect-pcap-client --format json --full-output` | 1 | `capability_unavailable`, `Cannot run selected tool /nonexistent-definitely-absent/tshark: spawn … ENOENT` (message names the exact selected path); duration 67ms |
| D | `REA_TSHARK_COMMAND=tshark` (relative) | `npx -y rea-agents@6.5.0 inspect-pcap-client --format json --full-output` | 1 | `capability_unavailable`, `REA_TSHARK_COMMAND must be an absolute path to the tshark binary` (config refusal pre-spawn); duration 2ms |

Artifacts: full stdout of B and C retained in the run transcript (`artifact://52593`,
`artifact://52589` as captured by the session; text reproduced in `DispositionInspectPcapCapture.json`).
All four land on the identical envelope shape `{"ok":false,"error":{"code":"capability_unavailable",…},"meta":{"command":…}}`,
i.e. the exact grammar the counter matches for `error:capability_unavailable`.

### Could the absent-client control support frontier-blocked? — Yes (and it hardens the row)

- **Grammar**: every refusal variant — ENOENT spawn, run-but-fail (`/usr/bin/false`), absolute
  nonexistent path, non-absolute env value — produces `error:capability_unavailable`, which
  `count-c2.py:check` matches against the PROVINCE row verbatim.
- **Robustness**: the receipted ambient-PATH observation (A) is accurate but PATH-dependent — if
  `tshark` later entered PATH, the same argv would no longer produce ENOENT. Variant B pins the
  refusal to the caller's explicit selection and is deterministic regardless of host tool state
  (on this host it additionally reproduces with the real coreutils banner in `captured_output`).
  If L1 wants this hardening, it requires a **new** receipt (e.g. `inspect-pcap-capture.json`
  variant with `env_overrides {"REA_TSHARK_COMMAND":"/usr/bin/false","REA_CAPINFOS_COMMAND":"/usr/bin/false"}`)
  and a row update — integration decision, not made here.
- **Semantics**: the refusal is a caller-toolchain gap (Wireshark not supplied), not lane-deferred
  ground, so `frontier-blocked` is the correct placement — consistent with the ADB false-client
  rows, all of which are `frontier-blocked`.

### Could it support adjacent? — No

- Shape: with an unavailable client, the **only** reachable observed values are
  `error:capability_unavailable` (both verbs gate on a passing 4.x version probe of both tools
  before anything else; `ok-field:`/`ok-empty:` outcomes are unreachable). An `adjacent` row with
  `observed error:capability_unavailable` would pass the counter grammar, but it would misdescribe
  a supply-chain gap as ground the lane refuses/defers — the pcap-capture analysis of a
  caller-supplied saved file is exactly the ground the lane wants to hold once tshark/capinfos
  exist. No property of a false client contributes `adjacent` evidence for this verb.

## 5. PROVINCE.md row audit (row for `inspect-pcap-capture`)

`| inspect-pcap-capture | frontier-blocked | inspect-pcap-capture | error:capability_unavailable |
.ufo/waves/round-22/evidence/c2/inspect-pcap-capture.json | Selected tshark command ENOENT; no
packet summary capability acquired |`

- Row `probe` == row `verb` == receipt `meta.command` == `inspect-pcap-capture` — satisfies
  `count-c2.py:check` (`probe_mismatch` guard).
- `observed error:capability_unavailable` == receipt envelope (§4 A) — matched.
- The reason is honest ("no packet summary capability acquired") and correctly narrower than any
  traffic-absence claim; consistent with the sibling `inspect-packet-capture` row's explicit
  traffic disclaimer.
- Precision note: "Selected tshark command ENOENT" is true of the recorded instant and means
  "the PATH-fallback name `tshark`" (selection `source:"path"`). It is not evidence that no
  tshark exists under an explicit key; §4 C/D show the message the envelope would carry for those
  variants. Keep the present wording unless upgrading to the explicit control.

## 6. RecoverReceipts.json

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/w2/RecoverReceipts.json`
**not yet available** as of this review (2026-10-21; w2/ contains only `PrimaryGdb.md`,
`SimplifyC2.{md,json}`, `PrimaryTshark.{md,json}`, `swarm-registry.json`). No verb-envelope
review could be performed; nothing inferred from its absence.

## 7. count-c2.py verification run (read-only; receipt/row agreement at one revision)

- argv: `python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root <LANE> --rev HEAD`
- exit 0; `accounted_count 14`, `t2_total 14`, `mismatched []`, `foreign_rows []`;
  `per_verb["inspect-pcap-capture"].status == "matched"`.
- Caveat recorded: the working tree `count-c2.py` is **modified relative to HEAD**
  (`git diff` = 33 insertions/13 deletions: strict single-heading parse, `malformed_disposition_row`
  on 6-cell mismatch, probe==verb enforcement, deep strict-JSON equality with bool/int
  distinction, dropped `re` import). The run above used the hardened working-tree copy against
  HEAD objects; at commit `cd596f4` (HEAD's counter) the outcome may differ only in strictness
  direction (HEAD's parser is looser, so rows accepted by the working tree are a superset check,
  not a subset). L1 integration owns the counter's commit state; no lane file was changed.

## 8. Constraints honoured / residuals

- No installs or updates (tooling directive: none needed). No pacman transaction.
- REA only via `npx -y rea-agents@6.5.0`; no MCP devices; no target execution, debug attach,
  device or remote contact; no config/credential/account inspection. The only executed REA verbs
  are the two pcap verbs in refusal-only configurations; `empty.pcap` was never read by any
  provider (client gate precedes `snapshot.capture`).
- Unknowns: whether REA upstream changes the 4.x version gate or env keys in later versions
  (review pins 6.5.0 by lane contract); `TsharkCaptureProvider` (`inspect-packet-fields`/
  `inspect-packet-capture`) internals were read only via receipt text, not source-traced here.
- Findings are author-side support for L1's disposition integration; nothing in this report is
  outside admission.
