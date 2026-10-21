# DispositionInspectPacketCapture — independent disposition support review for `inspect-packet-capture`

Seat: `KaidokuR22R.DispositionInspectPacketCapture-6` (leaf reviewer, author-side only; not outside admission).
Baseline under review: `7787fea4d6fd718726de92ed20759d11ce7b8b48`; lane HEAD observed `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`.
Claim: `R22-C2` (calibration) in `.ufo/waves/round-22/claims.json`; counter `.ufo/waves/round-22/tools/count-c2.py`; row in `PROVINCE.md` §"### Round-22 catalog dispositions".

## 1. Verb parameter surface (observed, `rea-agents@6.5.0`)

`npx -y rea-agents@6.5.0 inspect-packet-capture --help` (exit 0) and `--schema` (exit 0) agree:

| parameter | kind | constraint (schema) | non-contact? |
|---|---|---|---|
| `<path>` | required positional arg | string, `additionalProperties:false` | yes — local file read only |
| `--fields` | **required** option | array 1–1024 strings (1–8192 chars); `options.required[1]: fields`; description: `frame.number` always included | yes — caller-chosen TShark field names |
| `--display_filter` | optional | string 1–8192 or null (default null); `-Y` applied within read limit | yes |
| `--decode_as` | optional | array ≤1024 strings; e.g. `tcp.port==8888,http` | yes |
| `--packet_limit` | optional | int, `exclusiveMinimum:0`, max 2147483647, or null | yes — bounds input reads |
| `--two_pass` | optional | bool, default true; false = single pass | yes |
| `--match_offset` | optional | int 0..2^53-1, default 0 | yes |
| `--match_limit` | optional | int >0, default 50 | yes |
| `--all_matches` | optional | bool, default false | yes |

Global flags (`--format`, `--full-output`, `--token-*`, `--filter-output`) are envelope controls, not probe parameters. The entire surface is inspection-side over a local capture plus a locally spawned TShark; nothing in it addresses a device, serial, remote endpoint, or target process. A valid minimal non-contact probe is exactly what the wave ran: `<abs path>.pcap --fields frame.number`.

## 2. Row grammar vs counter (verified by execution)

Row: `| inspect-packet-capture | frontier-blocked | inspect-packet-capture | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/inspect-packet-capture.json | Supplied empty pcap not dissected because TShark configuration unavailable; not a traffic-absence claim |`

- `placement` ∈ `{frontier-blocked, adjacent}` ✔; `probe == verb` ✔ (required by the worktree `tools/` copy, which adds `row["probe"] != row["verb"]` on top of the `frozen/` copy — see §5).
- `observed` grammar `error:<code>`; envelope `ok:false`, `error.code:"capability_unavailable"` → `matched` ✔.
- Receipt under `RECEIPT_PREFIX`, committed at HEAD, strict-JSON envelope, `meta.command == "inspect-packet-capture"` ✔. Single row for this verb; `foreign_rows:[]`.
- Reason text is accurate and honest: receipt `details.provider_id="tshark-capture"`, `reason:"Supply absolute REA_TSHARK_COMMAND for TShark 4.x."` — a configuration refusal before any spawn; nothing was dissected, so "not a traffic-absence claim" is the correct non-claim.

Counter runs (verbatim):
- `python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root <LANE> --rev HEAD` → `accounted_count:14`, `mismatched:[]`, **exit 0** (claims `after_target` met).
- same at `--rev 7787fea4…` → `accounted_count:0`, every T2 `unaccounted`, **exit 1** (matches `before_expected`).

## 3. Probe receipt provenance (observed)

`capture-probes.py` argv for this verb: `npx -y rea-agents@6.5.0 inspect-packet-capture <abs>/empty.pcap --fields frame.number --format json --full-output`, `env_overrides:{}`, exit 1, stderr empty. `empty.pcap` = 24-byte pcap global header (LE magic `d4c3b2a1`, v2.4, snaplen 65535, linktype 1/Ethernet, zero packet records; sha256 `acc530668c8bc60b2d229281130b1899bfc81d70fdada5c34b3236c628f739c8`) — "empty" is literal.

Independent re-run of the identical argv this session (cwd `/tmp`, env inherited, no `REA_TSHARK_COMMAND` set — `env | grep ^REA_` lists only ADB/APKTOOL/BINWALK/JADX/PWNTOOLS/UNBLOB/WAKARU keys): exit 1, stderr empty, stdout **byte-identical** to the committed receipt (including `meta.duration:"2ms"` — deterministic fixed refusal path, not a defect).

## 4. Absent-client control analysis (the assigned question)

ADB rows use `REA_ADB_PATH=/usr/bin/false` as an "unavailable-client control". Does the equivalent work here? Observed control runs (all `/tmp`, same pcap, `--fields frame.number --format json --full-output`):

| control | exit | `ok` | `error.code` | `details.reason` / diagnostics |
|---|---|---|---|---|
| `REA_TSHARK_COMMAND` unset (=receipt) | 1 | false | `capability_unavailable` | `Supply absolute REA_TSHARK_COMMAND for TShark 4.x.` (provider refused before spawn) |
| `REA_TSHARK_COMMAND=/nonexistent/kaidoku-r22-tshark` | 1 | false | `capability_unavailable` | `ENOENT: no such file or directory, realpath '/nonexistent/kaidoku-r22-tshark'` |
| `REA_TSHARK_COMMAND=/usr/bin/false` | 1 | false | **`execution_failure`** | `diagnostics{exit_code:1, stdout:"false (GNU coreutils) 9.12\n…"}` — REA resolved the binary and ran it (a `--version`-style probe); `false` printed its banner and exited nonzero |
| sibling `inspect-pcap-capture` + `REA_TSHARK_COMMAND=/usr/bin/false` (`pcap` provider) | 1 | false | `capability_unavailable` | `The selected tool /usr/bin/false cannot report its version: Command failed` — this provider gates on the version probe |

Conclusions:
- **`frontier-blocked`: supported** by any of these controls — but the `observed` column must match the control's actual code. Env-unset and nonexistent-path controls reproduce `error:capability_unavailable` (different `details.reason` strings; counter only checks `error.code`, though the prose reason should track the receipt). **`/usr/bin/false` does NOT reproduce it for this verb**: the `tshark-capture` provider treats a resolvable executable as runnable, spawns it, and reports `execution_failure` with captured diagnostics. The ADB `/usr/bin/false` recipe is therefore **not transferable** to `inspect-packet-capture` as an `error:capability_unavailable` receipt — a row pairing that control's receipt with the current observed value would `observed_mismatch` (exit 1).
- **`adjacent`: not supported** by any absent-client control. Every client-absent path yields `ok:false`; `ok-empty:<path>`/`ok-field:<path>=<json>` require `ok:true`, and no parameter in this verb's surface produces a client-free success. Adjacent would only be reachable with a working TShark 4.x (a capability hold, not a control).
- **"not actual device availability": trivially satisfied** — this verb has no device leg at all; the only external dependency is the local TShark client. The control tests REA's client-selection/refusal behavior, never dissection quality, traffic presence, or any device.
- Note the asymmetry across providers: `pcap` (inspect-pcap-*) refuses `/usr/bin/false` at the version gate → `capability_unavailable`; `tshark-capture` (inspect-packet-*) executes it → `execution_failure`. Same control input, different codes — receipt `observed` values are provider-specific and must not be copied across rows.

## 5. Secondary observations (informational)

- `tools/count-c2.py` (the file `claims.json` `counting_command` names) has **uncommitted worktree changes** vs HEAD (`git status: M`): adds the `probe == verb` equality and a `--selftest` mode; `frozen/count-c2.py` retains the laxer original. This verb's row passes both variants, so the divergence is not a defect for this row — flagged only because the committed `counting_command` file and its worktree content currently differ.
- `runs.json` consolidated log agrees with `inspect-packet-capture.run.json` (argv, `env_overrides:{}`, exit 1).
- Peer `PrimaryTshark.md` corroborates host absence (`command -v tshark`/`capinfos`/`dumpcap` exit 1, `pacman -Q wireshark-cli` not found) — consistent with, but independent of, the refusal; the receipt itself attributes the gap to missing `REA_TSHARK_COMMAND` configuration, and `env` inspection confirms that key is unset in this shell.
- Schema requires `--fields` (min 1 item); `capture-probes.py` supplies `frame.number`, satisfying it. A fields-less invocation would fail argument validation, not reach the provider — irrelevant to the current row but the only schema-mandated parameter.

## 6. `RecoverReceipts.json` — not yet available

`.ufo/waves/round-22/w2/` contains no `RecoverReceipts.json` (`find .ufo/waves/round-22 -name '*RecoverReceipts*'` empty; directory listing has 49 files, none matching). Per assignment, the verb-envelope-vs-row review in §2–§4 stands on the committed receipt and live re-observations instead.

## 7. Findings

| sev | finding | evidence |
|---|---|---|
| — | Row is grammar-valid, receipt-matched, and honest; counter `matched` at HEAD (14/14, exit 0) and `unaccounted` at baseline (exit 1). No actionable defect for this verb. | §2–§3 |
| info | Absent-client control supports `frontier-blocked` only, and `/usr/bin/false` yields `error:execution_failure` (not `capability_unavailable`) for this provider; nonexistent-path preserves `capability_unavailable`. `adjacent` is unreachable without a working client. | §4 |
| info | `tools/count-c2.py` worktree≠HEAD (adds `probe==verb`, `--selftest`); row passes both. | §5 |

## 8. Constraints honoured

No installs (npx consumed the cached `rea-agents@6.5.0` pin; PROVINCE records its cache dir `ad9a3fdbcad992c6`; ~1s runs indicate cache hit [INFERENCE]). No pacman/uv/npm transaction. No device/target/hook, no remote connection, no config or account inspection, no Frida. All probe output written under `/tmp/kaidoku-r22-ipc/`; lane writes limited to this report and its `.json` attachment. Controls are local-binary executions only (`/usr/bin/false`, nonexistent path) — the explicit unavailable-client-control analogue of the ADB convention, not device checks.
