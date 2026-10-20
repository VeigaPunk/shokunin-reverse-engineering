# ScoutObjdumpArch — `list-objdump-architectures` schema, one run, and the full operation inventory (round 20, w1)

Seat: `KaidokuR20.ScoutObjdumpArch-2` (scout, read-only; no lane file changed; no subagent; no tool installed or upgraded).
Clock at write: `2026-10-20T17:50:13-03:00` (`date -Iseconds`). Baseline for lane reads: `14f0260` (working tree not modified).
Consumer: `ObjdumpArchLeg` (`.ufo/waves/round-20/wave1-spec.json:103`) and the C2 counter (`claims.json:26`; `contract.md:71-76`).
Complements `SourceObjdumpDocs` (`.ufo/waves/round-20/w1/SourceObjdumpDocs.md:33` records that seat did not execute the verb); this report supplies the executed run and the provider-side operation inventory.

Host, observed: `objdump --version` → `GNU objdump (GNU Binutils) 2.47`, first line only; exit 0.
Calibration carrier (disposable, not retained): `/usr/bin/true`, 43320 bytes, mode `-rwxr-xr-x`, sha256 `8398af7d1f94a88be3303caa083616ad22a12783e4dfee0373298bc61aef0662` (`sha256sum`, exit 0).

## 1. `--schema` output, verbatim

Command (exit 0, empty stderr):

```
npx -y rea-agents@6.5.0 list-objdump-architectures --schema
```

```
args:
  type: object
  properties:
  additionalProperties: false
```

Observation: the verb takes **no input arguments and declares no options** — not even a path. `properties:` is present and empty, so this is the rendered `z.object({})` at `dist/cli/reverseEngineeringCommands.js:106`.
Observation: `--help` prints `Usage: rea list-objdump-architectures` with only global options (`--format`, `--schema`, …); exit 0.
Observation: the `.ufo/waves/round-20/w1/SourceObjdumpDocs.md:33` reading of the same schema matches byte-for-byte.

For contrast, `inspect-with-objdump --schema` (exit 0) is the artefact branch only:

```
args:
  type: object
  properties:
    path: {type: string, minLength: 1}
    operation: {type: string, enum[7]: file_headers,section_headers,symbols,relocations,dwarf,disassemble,disassemble_all}
  required[2]: path,operation
  additionalProperties: false
options:
  type: object
  properties:
    followDebugLinks: {type: boolean, default: false}
  additionalProperties: false
```

Observation: three different spellings of one field — schema `followDebugLinks`, CLI flag `--follow-debug-links`, Evidence field `follow_debug_links` (`parameters.follow_debug_links: false` in the run below). Cite the flag by its `--help` form, not by the schema key.

## 2. One run, output summary

Command (exit 0, empty stderr, 6147-byte YAML envelope):

```
npx -y rea-agents@6.5.0 list-objdump-architectures
```

| field | observed value |
|---|---|
| `evidence_id` | `ev_4d59366d3e60960da306e5b984acca68678ca83f20dd5d2ae40cb5f4851719b7` |
| `subject` | `null` (no artefact) |
| `provider` | `{id: gnu.objdump, name: "GNU objdump", version: null}` |
| `analysis_profile`, `environment` | `null`, `null` |
| `predicate_type` | `rea.reverse-engineering.command-observation` |
| `operation` | `inspect_with_objdump` |
| `parameters` | `{operation: architectures, provider_executable: objdump, command_arguments: ["-i"]}` |
| `raw_result` | `stdout` 2343 chars, `stderr` `""`, `exit_code` 0, `signal` null, `output_truncated` false, `completion_status` complete, `artifact_sha256_after` null, `artifact_changed` null |
| `normalized_result` | byte-identical to `raw_result` |
| `confidence`, `authority` | `observed`, `shipped-artifact` |
| `locations`, `evidence_links`, `relationship_coverage` | `[]`, `[]`, `null` |

`limitations[4]`, verbatim: "Artifact identity is unavailable for this observation.", "The objdump version is not reported; the output lists BFD targets advertised by the installed tool and does not establish support for the selected artifact.", "A non-zero process exit is preserved as an observed command result.", "This output lists BFD targets advertised by the installed objdump and is independent of the selected artifact."

Output content: 94 stdout lines; a header `BFD header file version (GNU Binutils) 2.47`; **23** BFD target names with per-arch little/big-endian rows plus an at-a-glance compatibility matrix at the end. The 23, in order: `elf64-x86-64, elf32-i386, elf32-x86-64, pei-i386, pe-x86-64, pei-x86-64, elf64-little, elf64-big, elf32-little, elf32-big, pe-bigobj-x86-64, pe-i386, pe-bigobj-i386, pdb, elf64-bpfle, elf64-bpfbe, srec, symbolsrec, verilog, tekhex, binary, ihex, plugin`.

Substance checks (all exit 0):

- REA's normalized stdout is **byte-identical** to host `objdump -i` — both sha256 `8cebf3c9e476beaaed7fa66d7681af49b07377d661af0bea598699d5f96d5f83`, 2343 bytes, `diff` empty. `objdump --info` hashes identically too.
- `objdump --help` line 98 emits one `objdump: supported targets:` line whose 23 names are **set-equal and order-equal** to the above (checked in Python). So the run's content is corroborated by two independent host surfaces; this is a host observation, not REA Evidence.
- Determinism: two bare YAML runs are byte-identical (`1639f967693f868d64ae906981e13b7e6485f7041c6c290bba4e1b671ee54c62`), and `--format json` reports the **same** `evidence_id` (`ev_4d59…`). The id is content-addressed, not a per-run nonce.
- Stray positionals are **silently accepted**: `list-objdump-architectures /usr/bin/true` and `… foo bar` both exit 0 with the same Evidence (`parameters` unchanged, no path field). This contradicts the schema's `additionalProperties: false` at the CLI positional layer.

## 3. Operation inventory beyond `file_headers`

Observation (schema): `inspect-with-objdump --schema` enumerates **7** operations; the corpus holds only `file_headers` (`corpus/knowledge/2026-10-16-l7-06-inspect-with-objdump.md:1`, `:10`). The 6 new ones are `section_headers`, `symbols`, `relocations`, `dwarf`, `disassemble`, `disassemble_all`. Novelty check: `grep -rn 'section_headers\|disassemble_all\|relocations' corpus/knowledge/*.md` returns 12 hits, all non-REA field names (pwntools/Rizin contexts, e.g. `corpus/knowledge/2026-10-13-r4-13-pwntools-persist.md:77`); none names an `inspect-with-objdump` operation, so no existing knowledge row is displaced or double-counted.

Observation (provider vs CLI): the provider schema is a **discriminated union** (`dist/domain/reverseEngineering.js:18-21`): artefact branch `{path, operation ∈ 7, follow_debug_links}` (`:2-16`) or pathless `z.strictObject({operation: z.literal("architectures")})` (`:20`). Thus there is an **8th operation, `architectures`**, which the CLI `inspect-with-objdump` args enum omits (`dist/cli/reverseEngineeringCommands.js:73-89`; the enum itself `:79-87`). Its only CLI entry point is the wrapper verb `list-objdump-architectures` (`:104-113`, which calls `service.inspectWithObjdump({operation:"architectures"})` at `:108`); the name maps to the same provider operation at `dist/cliCommandNames.js:55,175`. The contract description states the pathless rule explicitly (`dist/contracts/reverseEngineeringToolContracts.js:24`; example `:34`).

Observation (negative test): `npx -y rea-agents@6.5.0 inspect-with-objdump /usr/bin/true architectures` → exit 1, `code: VALIDATION_ERROR`, message enumerating exactly the 7 artefact operations. So `architectures` is **not** reachable through `inspect-with-objdump` on the CLI; do not cite that form.

Operation → argv → result on `/usr/bin/true` (each `… inspect-with-objdump /usr/bin/true <op> --format json`, all exit 0, all `subject.digest.sha256` = `8398af7d…af0662`):

| operation | argv after `objdump` | exit | stdout bytes | evidence_id prefix |
|---|---|---|---|---|
| `file_headers` | `-f /usr/bin/true` | 0 | 151 | `ev_e7c4ba517df` |
| `section_headers` | `-h /usr/bin/true` | 0 | 3662 | `ev_472627791d0` |
| `symbols` | `-t /usr/bin/true` | 0 | 73 | `ev_483d91f917c` |
| `relocations` | `-r /usr/bin/true` | 0 | 218 | `ev_48c245c7251` |
| `dwarf` | `-W -WN /usr/bin/true` | 0 | 54871 | `ev_98512e0d2d3` |
| `disassemble` | `-d /usr/bin/true` | 0 | 290352 | `ev_2be9572e074` |
| `disassemble_all` | `-D /usr/bin/true` | 0 | 514316 | `ev_b621a890da7` |

Observation: `dwarf` is two flags (`-W -WN`, i.e. wide + no-follow), which is where the `--follow-debug-links` option would change argv (`-W -WK`-class); I did not run that variant. Observation: `symbols` on the stripped `/usr/bin/true` yields only 73 bytes — thin ground. Inference: if the C2 row wants to claim `symbols` behaviour, use a carrier with a real symbol table (`/usr/bin/jq`, executor leg's target, is a candidate but is itself not verified here to be unstripped).

`dwarf` also shows the buffer limit is far above these sizes (54871/290352/514316 bytes, all `output_truncated: false`, `completion_status: complete`); the contract limit is a shared 16 MiB (`dist/contracts/reverseEngineeringToolContracts.js:24`).

## 4. Calibration findings for the C2 counter and the executor leg

1. **`subject` is `null` for this verb.** C2 says each target entry cites a "subject SHA-256" (`claims.json:27`, with the verb list at `:26`; `contract.md:74-75` requires the `ev_` id plus a retained path). The architectures run cannot supply a subject digest by construction. Recommendation for `ObjdumpArchLeg`: the entry should carry **two** Evidence IDs — `ev_4d59…` for the pathless run, and an artifact-bearing `inspect-with-objdump` run (e.g. `section_headers` on `/usr/bin/jq`, subject `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`) whose subject field is populated. Do not invent a subject for the pathless run; state `subject: null` and cite the host binary/version separately, labelled as a host observation.
2. **The `ev_` id is content-addressed, so it proves retention, not recency.** Two runs, two formats, same id; stray arguments did not change it. A counter that accepts "entry names verb + carries `ev_` + file exists" (`contract.md:74-75`) cannot distinguish a fresh round-20 run from a re-copied older capture with identical content. Mitigation: the retained receipt's start/end clock and the round-20 evidence path are the only freshness evidence; require them (`ObjdumpArchLeg` acceptance already asks for start/end UTC).
3. **`provider.version` is `null` while the version is visible in raw text.** Limitation 2 says the version "is not reported"; raw stdout line 1 says `BFD header file version (GNU Binutils) 2.47`, matching `objdump --version`. Any corpus sentence about the binutils version must cite the raw-output line as text, not a structured field.
4. **Schema strictness ≠ CLI positional strictness.** The verb's schema is `z.object({})` with `additionalProperties: false`, yet extra positionals exit 0 and are ignored. Do not use a stray-argument probe as a negative/refusal test for this CLI family; use the enum probe (`inspect-with-objdump … architectures`, exit 1 `VALIDATION_ERROR`) instead, which is a real refusal.
5. **Do not generalise the target list.** The 23 names reflect the installed binutils 2.47 build on this host, not an REA catalogue; `SourceObjdumpDocs.md:1-6,20-26` already establishes from the manual that `-i` lists what `-b`/`-m` can select. A cross-host claim would need a second host's run.

## Remaining unknowns (not closed here)

- The `evidence_id` derivation is unresolved. Five naive hypotheses over the JSON envelope (sorted/default serialization, normalized stdout, raw-result object) did not reproduce `ev_4d59…`. Inference only: deterministic over provider+parameters+output, with some unrecovered frame.
- Whether the C2 counter counts a pathless verb as `exercised` is unobservable at baseline: `W20/tools/verb-coverage.py` and `.ufo/waves/round-20/evidence/c2/` do not exist at `14f0260` (verified by `ls`, `No such file or directory`). Finding 1 above is therefore a recommendation, not a contradiction of an existing rule.
- The `--follow-debug-links` argv variant (e.g. on `dwarf`) was not executed.
- No claim is made about `inspect-with-objdump` on any Go toolchain ELF; none was touched or executed.

## Commands (all read-only; exit codes as observed)

- `objdump --version` → binutils 2.47 first line, exit 0.
- `npx -y rea-agents@6.5.0 list-objdump-architectures --schema` → §1 text, exit 0.
- `npx -y rea-agents@6.5.0 list-objdump-architectures --help` → usage, exit 0.
- `npx -y rea-agents@6.5.0 list-objdump-architectures` → 6147-byte YAML, exit 0.
- `npx -y rea-agents@6.5.0 list-objdump-architectures --format json` → `ev_4d59…`, exit 0.
- `npx -y rea-agents@6.5.0 list-objdump-architectures /usr/bin/true` and `… foo bar` → exit 0, stray args ignored.
- `npx -y rea-agents@6.5.0 inspect-with-objdump --schema` → 7-operation enum, exit 0.
- `npx -y rea-agents@6.5.0 inspect-with-objdump /usr/bin/true architectures` → exit 1 `VALIDATION_ERROR`.
- `npx -y rea-agents@6.5.0 inspect-with-objdump /usr/bin/true <op> --format json` for the 7 operations → all exit 0 (table §3).
- `npx -y rea-agents@6.5.0 inspect-with-objdump --path …` / `--operation …` → exit 1 `Unknown flag` (the CLI is positional; useful negative for argument-form claims).
- `objdump -i`, `objdump --info`, `objdump --help` → exit 0; hashes/diff as in §2.
- `sha256sum /usr/bin/true /usr/bin/jq` → `8398af7d…0662`, `e8156675…7806`, exit 0.
- `grep -n` over the pinned dist files (`~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents@6.5.0/dist/…`) for the anchors in §3, exit 0.

Package provenance: `npx` cache already held `rea-agents@6.5.0` at `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (6.5.0 confirmed via its `package.json`); no install or upgrade was performed by this seat. A separate cache slot holds 6.7.0 (`a1722018f28f9df2`), which was not invoked.

## Verdict

ACCEPTED (queued) on scope: the schema, one executed run, the host `objdump --version`, and the complete 8-operation inventory with argv are grounded. The C2-relevant caveat is finding 1 (`subject: null` for pathless `architectures`) plus finding 2 (content-addressed `ev_` ids do not date a run); both are actionable for `ObjdumpArchLeg` and the counter, neither blocks the verb's admission.
