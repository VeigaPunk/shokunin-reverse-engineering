# DispositionInspectPcapClient — independent disposition support review

Seat: `KaidokuR22R.DispositionInspectPcapClient-6` — author-side review only, not
outside admission. Scoped to `inspect-pcap-client` under claim R22-C2
(calibration), baseline `7787fea4d6fd718726de92ed20759d11ce7b8b48`, measured
lane HEAD `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`.

## Verb surface (REA CLI, rea-agents@6.5.0)

`rea inspect-pcap-client --help` (exit 0) and `--schema` (exit 0) establish:

- Grammar: `rea inspect-pcap-client` — **zero positional arguments, zero
  verb-specific options**. `--schema` prints `args: {type: object,
  properties: []…, additionalProperties: false}` (an empty property set); only
  global output flags apply (`--format`, `--full-output`, `--filter-output`,
  `--token-*`, `--llms*`, `--schema`, `--help`).
- Selection is entirely environmental: PATH fallback (`tshark`, then
  `capinfos`), overridden by absolute `REA_TSHARK_COMMAND` /
  `REA_CAPINFOS_COMMAND`. The remediation text on the frozen receipt names
  exactly these two env keys plus PATH — no other knob (notably not
  `REA_TSHARK_PRLIMIT_COMMAND`, which belongs to the `tshark-capture` provider
  family, `provider_id:"tshark-capture"`, not this verb's
  `provider_id:"pcap"`).
- Distinct sibling behavior: `inspect-packet-fields` and
  `inspect-packet-capture` demand an *absolute* `REA_TSHARK_COMMAND` up front
  (no PATH fallback, receipt `inspect-packet-fields.json`) —
  `inspect-pcap-client` is the PATH-fallback member of the packet family.
- Non-contact by construction: this verb "inspects the caller-selected tshark
  and capinfos binaries **without reading a capture**" (help line), takes no
  file argument, opens no device and makes no network connection. It only
  resolves the two binaries and asks each for its version banner (proven
  below).

Exact valid non-contact probe parameters: bare
`npx -y rea-agents@6.5.0 inspect-pcap-client --format json --full-output` —
no argument slot exists to get wrong; outcome is decided solely by the two
env keys / PATH.

## Disposition row vs receipt (counter-verified at HEAD)

PROVINCE.md `### Round-22 catalog dispositions` row:
`| inspect-pcap-client | frontier-blocked | inspect-pcap-client |
error:capability_unavailable | .ufo/waves/round-22/evidence/c2/inspect-pcap-client.json
| Selected tshark command ENOENT; capinfos availability not independently
established |`.

Receipt `.ufo/waves/round-22/evidence/c2/inspect-pcap-client.json`:
`ok:false`, `error.code:"capability_unavailable"`,
`category:"unsupported_provider"`, `retryable:false`,
`details.provider_id:"pcap"`, `details.operation:"inspect_pcap_client"`,
`details.reason:"Cannot run selected tool tshark: spawn tshark ENOENT"`,
`meta.command:"inspect-pcap-client"`, `duration:"31ms"`. Run record
`inspect-pcap-client.run.json`: argv
`npx -y rea-agents@6.5.0 inspect-pcap-client --format json --full-output`,
`env_overrides: {}` (no explicit control — see below), `exit:1`, stdout =
the envelope, `stderr:""`.

`python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root . --rev HEAD`
(cwd lane) → exit 0; `accounted_count:14/14`, `mismatched:[]`,
`foreign_rows:[]`, `per_verb["inspect-pcap-client"].status:"matched"`. Row
grammar (`error:` needs `ok==false` + `error.code` equality; `probe` equals
`verb` and `meta.command`) is satisfied exactly. Receipt and PROVINCE row are
both committed at HEAD `2ee3d9f` (`git show` succeeded for both).

## Could the absent-client control support `frontier-blocked` or `adjacent`?

Supports **frontier-blocked** — with one calibration nuance the other seats
do not have:

- **This receipt is a host observation, not an explicit control.**
  `env_overrides:{}`: the run observed that the host has no `tshark` on PATH
  (`command -v tshark` exit 1; `/usr/bin/tshark` and `/usr/bin/capinfos` do
  not exist; `pacman -Qs wireshark` empty — no Wireshark package installed).
  The ADB family's `/usr/bin/false` pattern has a pcap analogue that was
  *not* used (`REA_TSHARK_COMMAND` unset). This is honest — the row reason
  says exactly what happened ("Selected tshark command ENOENT") — but it is
  an environment fact, not a manipulated control.
- **Fresh corroborating false-client probe (same verb, explicit control):**

  ```
  env REA_TSHARK_COMMAND=/usr/bin/false REA_CAPINFOS_COMMAND=/usr/bin/false \
    npx -y rea-agents@6.5.0 inspect-pcap-client --format json --full-output
  exit 1, stderr ""
  stdout: {"ok":false,"error":{"code":"capability_unavailable",
  "category":"unsupported_provider","message":"The selected tool
  /usr/bin/false cannot report its version: Command failed; …", …,
  "details":{"provider_id":"pcap","operation":"inspect_pcap_client",
  "reason":"The selected tool /usr/bin/fa… (truncated at capture; same shape
  as receipt)}},"meta":{"command":"inspect-pcap-client",…}}
  ```

  Identical error code/category from an explicit control proves the same
  client-selection gate fires regardless of how absence is produced — so the
  receipt's meaning (no pcap client capability acquired) is robust.
- **Staged gate established by stub probes** (tshark checked first, capinfos
  second):

  ```
  env REA_TSHARK_COMMAND=/tmp/r22-pcap-stubs/tshark  # echoes "TShark (Wireshark) 4.4.1 (stub-for-r22-review)"
      REA_CAPINFOS_COMMAND=/usr/bin/false … inspect-pcap-client --format json --full-output
  exit 1 — error blames "/usr/bin/false cannot report its version" (tshark passed)
  ```

  This independently corroborates the row's honesty: in the production run
  tshark never spawned, so **capinfos was genuinely never reached** — the
  reason text is exact, not boilerplate.
- **End-to-end non-contact proof** (`ok:true`, exit 0, `duration:"166ms"`):
  with both env keys pointed at stub scripts that only echo a version line,
  the verb returns
  `normalized_result.client.{tshark_command,tshark_source:"environment",tshark_version,capinfos_command,capinfos_source:"environment",capinfos_version}`,
  `parameters:{}`, `raw_result:null`, `limitations:["Artifact identity is
  unavailable for this observation."]`, `evidence_id
  ev_f55e48988fef49cb3d8981a371a45cd406bf440dcd521bc8cc5daa03369eba9e`,
  `subject:null`. The stubs executed nothing but `echo`; therefore the verb's
  entire observable behavior is *resolve + version-check* the two binaries.
  This envelope is a **mechanics demonstration under synthetic clients, NOT a
  capability claim** — the stub banners were accepted verbatim, so no
  Wireshark-4.x validation happens at this verb; deeper gating belongs to the
  capture/fields verbs that would consume a real tshark.
- `frontier-blocked` is the calibrated label: the lane names a gap it does
  not hold (tshark/capinfos absent, install is operator-owned per PROVINCE
  adjacent notes), and the row's `limit` framing (counter output: "not
  provider availability over time") holds.

Does **not** support `adjacent`: adjacent rows in this table mean the
provider initialized and enumerated real state (`ok:true` payloads for
`list-frida-*`) or refused a real provider over an impossible request
(`instrument-with-frida`). Here the provider never initialized — nothing was
enumerated, deferred, or observed about any pcap capability beyond the
absence of its two client binaries.

Does **not** support any real-tool availability claim: the envelope cannot
distinguish "tshark never installed" from "tshark hidden by PATH", and the
receipt's exit-1 gives zero information about what a real Wireshark 4.x
client would report. No row grammar can extract a positive client finding
from this envelope, and none was claimed.

## Findings by severity

No actionable defects in scope.

- **Info** — disposition row, receipt, and counter all agree; `matched` at
  HEAD `2ee3d9f`, accounted 14/14.
- **Info** — run provenance nuance (worth keeping visible at integration):
  unlike the four ADB rows, this receipt's `env_overrides` is empty, so it is
  a PATH-absence *observation*, not the explicit false-client control the
  round preamble language uses for ADB. Its row reason already states the
  observed cause precisely, so calibration is intact; an explicit
  `REA_TSHARK_COMMAND=/usr/bin/false` rerun (recorded above) produces the
  identical error envelope if a control-form receipt is ever wanted.
- **Residual risk** — the `capability_unavailable` envelope is client-gate
  ambiguity by construction (staged tshark→capinfos gate means `ok:false`
  names only the first failed binary). Any future edit reinterpreting the
  receipt as "capinfos checked and absent" or as any positive tool finding
  would be a defect. Current reason text avoids this.
- **Gap** — counter versions differ: committed `.ufo/waves/round-22/tools/count-c2.py`
  at HEAD includes `probe == verb` and `--selftest`, unlike the older
  `.ufo/waves/round-22/frozen/count-c2.py`. The **worktree tools counter is
  modified relative to HEAD** and adds more behavior (unique exact heading,
  malformed-row rejection, type-sensitive JSON equality, recursion guards,
  and revised `finding`/`limit` fields). The command below used that modified
  worktree script against HEAD's committed row/receipt and returned 14/14;
  it does not claim an execution of the committed counter version. For this
  specific row, the committed check still requires envelope
  `meta.command == probe`, and both the row and receipt have
  `probe == meta.command == verb`. Treat the reported count as a worktree
  counter measurement of HEAD inputs, not as a check of the exact committed
  script.
- **Gap** — the two sibling pcap verbs (`inspect-packet-fields`,
  `inspect-packet-capture`) gate on absolute `REA_TSHARK_COMMAND` and never
  reach the staged PATH fallback this verb uses; the empty.pcap receipt for
  `inspect-packet-capture` is therefore not comparable evidence for this
  verb's client surface (different `provider_id`).

## RecoverReceipts.json

**Not yet available.** `.ufo/waves/round-22/w2/RecoverReceipts.json` did not
exist at review time (checked twice, last at 13:08:07Z 2026-10-21; the
directory holds the sibling Disposition/Critic/Primary/Schema/Mutate/Simplify
reports and `swarm-registry.json`). Per assignment, no verb-envelope review
was performed against it.

## Commands run (all non-contact, no target/device/hook, no production mutation)

| argv / env | exit | stdout/stderr |
|---|---|---|
| `npx -y rea-agents@6.5.0 --help` | 0 | command list / empty |
| `npx -y rea-agents@6.5.0 inspect-pcap-client --help` | 0 | usage text above / empty |
| `npx -y rea-agents@6.5.0 inspect-pcap-client --schema` | 0 | empty-args schema / empty |
| `env REA_TSHARK_COMMAND=/usr/bin/false REA_CAPINFOS_COMMAND=/usr/bin/false npx -y rea-agents@6.5.0 inspect-pcap-client --format json --full-output` | 1 | capability_unavailable envelope / `""` |
| same with `REA_TSHARK_COMMAND=/tmp/r22-pcap-stubs/tshark REA_CAPINFOS_COMMAND=/usr/bin/false` | 1 | error blames `/usr/bin/false` (capinfos stage) / `""` |
| same with both keys → `/tmp/r22-pcap-stubs/{tshark,capinfos}` (echo-only stubs) | 0 | `ok:true` client inventory envelope, `ev_f55e489…` / `""` |
| `python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root . --rev HEAD` (cwd lane) | 0 | `accounted_count:14/14`, pcap-client `matched` / empty |
| `command -v tshark` / `command -v capinfos` | 1 / 1 | not found — host PATH observation |
| `pacman -Qs wireshark`; `ls /usr/bin/tshark /usr/bin/capinfos` | 1 | no wireshark pkgs; No such file (read-only queries) |
| `git rev-parse/status --short/show` read-only inspections | 0 | HEAD `2ee3d9f`; receipts+PROVINCE committed; `.ufo/waves/round-22/tools/count-c2.py` is modified relative to HEAD (the counter command used this modified worktree version; details above) |

Stub scripts created in `/tmp/r22-pcap-stubs/` (session scratch, outside the
lane, removed of any production effect): two `#!/bin/sh` scripts each echoing
one version line; nothing else. Tooling: **no installs performed** (pacman
paused host-wide; none needed). `rea-agents@6.5.0` resolved via the existing
npx cache; record: tool rea-agents, version 6.5.0, channel npx cache, reason
= contract-pinned CLI. Companion machine-readable record:
`DispositionInspectPcapClient.json`.

## Residual risk / verification gaps

- The receipt is a host-state observation under empty `env_overrides`; its
  calibration value rests entirely on the row reason's precise wording,
  which is correct. The explicit-control and stub probes recorded here
  bracket the gate's behavior but are author-side evidence, not production
  receipts, and are not outside admission.
- Counter verifies row↔receipt agreement at one revision, not provider
  availability over time (its own declared `limit`).
- This seat reviewed support for the existing disposition only; it does not
  re-execute the production probe, install Wireshark, or admit the wave.
