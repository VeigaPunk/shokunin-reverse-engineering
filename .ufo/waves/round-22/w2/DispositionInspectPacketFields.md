# DispositionInspectPacketFields — disposition support review for `inspect-packet-fields`

**Seat:** `KaidokuR22R.DispositionInspectPacketFields-6` (leaf reviewer; author-side only, not outside admission).
**Baseline:** `7787fea4d6fd718726de92ed20759d11ce7b8b48`; **lane HEAD observed:** `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`.
**Scope:** verb envelope vs. `count-c2.py` row grammar and PROVINCE.md §"Round-22 catalog dispositions" row; absent-client control support for `frontier-blocked` vs `adjacent`. No target/device/hook runs; no production-file mutation. Tooling installs: none (npx cache `rea-agents@6.5.0` only, per contract pin).

## 1. Verb envelope — `npx -y rea-agents@6.5.0 inspect-packet-fields`

`--help` (exit 0) and `--schema` (exit 0) agree: provider `tshark-capture`, operation `inspect_packet_fields`, kind `artifact-provider` (source: `dist/application/captures/TsharkCaptureProvider.js`, `dist/contracts/captureToolContracts.js`).

Parameter surface (all non-contact; the tool contract states: *"No capture file, interface or binary target needed. Registrations describe tool capabilities, not observed traffic."*):

| option | schema | default |
|---|---|---|
| `--kind` | enum `protocols` \| `fields` | `protocols` |
| `--protocol` | string 1–8192 or null (exact abbreviation) | null |
| `--query` | string ≤8192, case-insensitive literal substring | `""` |
| `--offset` | integer 0..2^53−1 | 0 |
| `--limit` | integer >0..2^53−1 | 50 |
| `--all` | boolean (maps to `limit:null` — "all remaining within resource limits") | false |

The verb takes **no path, no serial, no remote endpoint** — every valid parameter combination is a local TShark glossary enumeration. Only environmental prerequisites: Linux, absolute `REA_TSHARK_COMMAND`, and `REA_TSHARK_PRLIMIT_COMMAND` (default `/usr/bin/prlimit`; must be absolute if overridden). `prlimit` is present on this host (`/usr/bin/prlimit`); `tshark`, `capinfos`, `dumpcap` are **absent** (`command -v` → exit 1 each). No `REA_TSHARK_*` key is exported in `.bashrc` (per PROVINCE §provider-key inventory).

## 2. Probe observations (all non-contact; no capture file, interface, or device)

| # | argv / env | exit | envelope |
|---|---|---|---|
| P1 | `npx -y rea-agents@6.5.0 inspect-packet-fields --format json --full-output` (no `REA_TSHARK_COMMAND`) — frozen receipt `.ufo/waves/round-22/evidence/c2/inspect-packet-fields.json`, `.run.json` recorded `env_overrides {}` | 1 | `ok:false`, `error.code=capability_unavailable`, `category=unsupported_provider`, `provider_id=tshark-capture`, reason `Supply absolute REA_TSHARK_COMMAND for TShark 4.x.` |
| P2 | `REA_TSHARK_COMMAND=relative/tshark npx … inspect-packet-fields --kind fields --protocol tcp --query seq --format json --full-output` | 1 | `capability_unavailable` — identical refusal; **parameter shape never reached** (config gate precedes execution) |
| P3 | `REA_TSHARK_COMMAND=/nonexistent/tshark npx … --format json --full-output` | 1 | `capability_unavailable`, reason `ENOENT: no such file or directory, realpath '/nonexistent/tshark'` — still a configuration-phase refusal |
| P4 | `REA_TSHARK_COMMAND=/usr/bin/false npx … --format json --full-output` | 1 | `ok:false`, **`error.code=execution_failure`**, `category=execution_failure`; `diagnostics.exit_code=1`, `diagnostics.stdout` carries the GNU coreutils `false` banner — the false client **was spawned** (version/identity run) and failed identity, so this is a tool-phase failure, *not* `capability_unavailable` |
| P5 | `npx … inspect-packet-fields --kind bogus --format json --full-output` | 1 | `ok:false`, `error.code=VALIDATION_ERROR` (CLI arg-parse layer; envelope `code` is the literal `VALIDATION_ERROR`, not `invalid_request`) — rejected before any provider contact |

## 3. What absent-client control can support

- **`frontier-blocked` — YES.** Any absent-client control produces `ok:false` + `error.code ∈ {capability_unavailable, execution_failure}` (P1–P4); all fit the `error:<code>` row grammar. Unset/relative/nonexistent `REA_TSHARK_COMMAND` → `capability_unavailable` (config-phase, honest "no TShark configured"); `REA_TSHARK_COMMAND=/usr/bin/false` → `execution_failure` (spawned-but-not-TShark — the closer ADB-style analogue, but the row `observed` must then read `error:execution_failure`, not `error:capability_unavailable`). Neither is evidence about real TShark availability, version, or device/traffic absence; reason text must stay scoped to the control (the existing row does this: "Explicit TShark configuration unavailable for this request; no field registrations examined").
- **`adjacent` — NO.** `adjacent` semantically means ground the lane demonstrates but defers/refuses to own (PROVINCE Adjacent list; all four `adjacent` rows in the table carry `ok-*:` observations — successful operations). An absent client cannot yield `ok:true`, so it can never substantiate `ok-empty:*` or `ok-field:*`. Grammatically the counter accepts `placement:adjacent` + `observed:error:capability_unavailable` (placements and observed-grammar are checked independently — `PLACEMENTS={frontier-blocked,adjacent}` is validated, then `observed` is matched against the envelope regardless of placement). **Calibration caveat:** that semantically impossible combination would report `matched`; nothing in `count-c2.py` enforces error→frontier-blocked / ok→adjacent correlation. Support here is author-side calibration, not counter-enforced.
- A third non-contact control exists — invalid-parameter rejection (`VALIDATION_ERROR`, P5) — but it calibrates schema adherence, not provider gap; it would satisfy `error:<code>` grammar yet is a weaker frontier claim and is not what the row asserts.

## 4. Row grammar & counter verification (`count-c2.py`)

Row for this verb: `| inspect-packet-fields | frontier-blocked | inspect-packet-fields | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/inspect-packet-fields.json | Explicit TShark configuration unavailable for this request; no field registrations examined |`.

Checks performed (read-only):
- `python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root . --rev HEAD` → **exit 0**; `accounted 14/14`, `mismatched []`, `foreign_rows []`; `per_verb["inspect-packet-fields"].status = "matched"`.
- Same command at `--rev 7787fea4d6fd718726de92ed20759d11ce7b8b48` → `accounted 0/14`, `inspect-packet-fields: unaccounted` — matches `claims.json` `before_expected` (0/14, exit 1 at baseline).
- Grammar fit verified manually against `check()`: `placement ∈ PLACEMENTS`; receipt path under `RECEIPT_PREFIX` `.ufo/waves/round-22/evidence/c2/`; receipt is strict-JSON envelope with `meta.command == "inspect-packet-fields" == verb == probe`; `observed error:capability_unavailable` requires `ok==false` ∧ `error.code=="capability_unavailable"` — both hold in the frozen receipt (P1). Reason is non-empty and accurately scoped (no claim of TShark binary absence — correctly narrower than PrimaryTshark's host observations).

## 5. `RecoverReceipts.json`

**Not yet available.** `w2/` contains 32 entries but no `RecoverReceipts.json`. Producer seat `KaidokuR22R.RecoverReceipts-6` (executor) is recorded `status:"failed"` in `wave2-terminal-initial.json` — "[openai-codex/gpt-6-luna] Retry budget exhausted after 5 retries: Codex is at capacity… (code=turn_rate_limit_exceeded)". Rechecked before writing — still absent. No envelope review possible for this verb from that artifact; the frozen `evidence/c2/` receipt (P1) is the only inspected envelope.

## 6. Findings

1. **Row is correctly matched and calibrated.** `frontier-blocked` + `error:capability_unavailable` + receipt all agree; reason honestly scopes the refusal to configuration, not binary/device absence. No change needed.
2. **Absent-client control supports `frontier-blocked` only** — via `capability_unavailable` (unset/relative/ENOENT `REA_TSHARK_COMMAND`) or `execution_failure` (`/usr/bin/false`, which *is* spawned and fails the `tshark@4` identity check). It cannot support `adjacent`, which requires a successful (`ok:true`) operation the lane then declines to own.
3. **Calibration gap (counter, not row):** `count-c2.py` does not correlate placement with observed class — `adjacent`+`error:*` would pass `matched`. Documented for L1; no row currently exploits it.
4. **False-client semantics differ from ADB's.** `REA_ADB_PATH=/usr/bin/false` produces `capability_unavailable` (version probe refused pre-operation); `REA_TSHARK_COMMAND=/usr/bin/false` passes configuration checks and produces `execution_failure` with the coreutils banner captured in diagnostics. A w2 re-probe choosing `/usr/bin/false` must write `observed: error:execution_failure` to stay counter-valid.
5. **Every parameter combination is non-contact** — the envelope admits no path/serial/endpoint; the only refusal surface for this verb is `REA_TSHARK_COMMAND`/`REA_TSHARK_PRLIMIT_COMMAND` configuration and Linux platform.

## Blockers / unknowns

- `RecoverReceipts.json` never landed (producer seat dead on rate limit); conditional review leg is vacuous — stated explicitly per assignment.
- Whether REA passes `-G fields`/`-G protocols` to tshark was not traced (PrimaryTshark left it unknown); irrelevant to disposition since no TShark run occurs.
- No installs; no mid-flight tests beyond the bounded read-only probes above (all argv/exit recorded).
