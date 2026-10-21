# CriticScope — debug-with-gdb / debug-with-rizin held ambition vs the dynamic-analysis boundary

Seat `KaidokuR22R.CriticScope-6` (critic, author-side W2 only, not outside admission). Lane read-only; the only lane writes are this file and `CriticScope.json`. Scratch work ran in `/tmp/criticscope-r22/` (temp git repos created and removed by the probe). Judged axes: coverage (R22-C1), calibration (R22-C2). Lane HEAD measured: `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`. This judges only current authored evidence; no later W2 report is assumed.

## Verdict

**Fixable calibration defect, not a reason to reject the round's claims.** The counter cannot count `debug-with-gdb` or `debug-with-rizin` from any record REA 6.5.0 actually emits, and under the wave contract `debug-with-rizin` cannot legitimately be run at all. These two verbs therefore sit in the `k/6` denominator at zero by construction, not because of a measured gap. Nothing on disk names that state honestly, and the only section where gaps get named (the C2 table) rejects them.

R22-C1 still verifies at k=1 (`identify-flutter-build`), and R22-C2 still verifies at 14/14. What has to change is the reporting: the closure MUST NOT present the two debug verbs as frontier that is "pending" or "unexercised", and the dynamic boundary must be named outside the C2 table.

## Finding 1 — the counter cannot bind either debug verb from real 6.5.0 records (OBSERVED)

The C1 counter delegates binding to the round-21 `bind` function, which requires `record.operation == verb.replace('-', '_')`. The only alias it knows is the special case for `list-objdump-architectures`:

- `.ufo/waves/round-21/tools/verb-coverage.py:85`: `operation = 'inspect_with_objdump' if verb == 'list-objdump-architectures' else verb.replace('-', '_')`
- `.ufo/waves/round-21/tools/verb-coverage.py:88`: rejects any record whose `operation` differs.
- `.ufo/waves/round-22/tools/count-c1.py:21-22` (T1 includes both debug verbs) and `:71` (calls `r21.bind(blob, verb, evidence_id)`).

REA 6.5.0 (`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`) never emits `debug_with_gdb` or `debug_with_rizin`. A search of `dist/` for both strings returned nothing. The package declares these verbs as aliases of differently named MCP operations:

- `dist/cliCommandNames.js:177-178`: `"debug-with-gdb": ["gdb_console"]` and `"debug-with-rizin": ["rizin_debug_command"]`.
- `dist/cli-runtime/cli.js:40963-40964`: `debug-with-gdb` returns `executed.value.evidence`, created with `operation: "gdb_console"` (`dist/gdb/GdbSessionManager.js:580-582`). Session start uses `start_gdb_session` (`GdbSessionManager.js:474`).
- `dist/cli-runtime/cli.js:41018-41019` and `dist/rizin/RizinDebugSessionManager.js:33`: `debug-with-rizin` returns a record with `operation: "rizin_debug_command"`.

The other four T1 verbs emit matching names (`identify_flutter_build`, `inspect_dart_aot` at `dist/cli/flutterCommands.js:18,38`; `inspect_signal_decoders`, `decode_signal_recording` at `cli.js:1061,1078`). The defect is confined to the two debug verbs.

**Counterexample (executed).** Command: `cd /tmp/criticscope-r22 && python3 -I -B probe.py > probe-out.json`, which exited 0 (probe sha256 `b70aae33554722862955fe8ffe8ef18e13f8ce64c0a645705b83e2b72813908f`). The probe builds a temp git repo holding a fully sourced entry (S051 mined, opened 2026-10-21, used-by naming the entry) that cites a retained record per verb. It then runs the lane's own counter, `python3 -I -B …/tools/count-c1.py --root <tmp> --rev <rev>`. stderr was empty in every case.

| case | record `operation` | debug-with-gdb | debug-with-rizin | t1_exercised_count | exit |
|---|---|---|---|---|---|
| real 6.5.0 console ops | `gdb_console` / `rizin_debug_command` | false | false | 0 | 1 |
| real 6.5.0 start ops | `start_gdb_session` / `start_rizin_debug_session` | false | false | 0 | 1 |
| fabricated names | `debug_with_gdb` / `debug_with_rizin` | **true** | **true** | 2 | 1 |

A correct, non-refused, properly sourced REA record cannot count. A record shape REA cannot produce does count.

**Impacted axes:** coverage (two of six targets are unreachable, so the 6/6 maximum is false) and calibration (`k/6` mixes "measured absent" with "unmeasurable").

## Finding 2 — the `all_six` positive control certifies a record shape the provider never produces (OBSERVED)

- `.ufo/waves/round-22/tools/counter-fixtures.py:44-47` writes every T1 fixture record as `'operation': verb.replace('-', '_')`.
- `:74` expects `('all_six', base, 0, 6, None)`.

The `all_six` positive passes only because the fixture invents `debug_with_gdb` and `debug_with_rizin`. This is false provenance for the control: it shows the counter reaching 6/6 on records that REA 6.5.0 cannot emit (see the fabricated row in the Finding 1 table). The lesson's "preserve positive/refusal/split/duplicate controls" (`corpus/lessons/round-22.md`, the working-tree `## Exercised counter and probe corrections` table) inherits this blind spot. The refusal, split and duplicate negatives remain valid.

**Impacted axes:** calibration (the counter controls overstate reach).

## Finding 3 — `debug-with-rizin` is target execution; holding it contradicts PROVINCE Adjacent and the wave contract (OBSERVED code path, INFERENCE on placement)

- `dist/rizin/RizinDebugSessionManager.js:207-218` spawns `rizin -N -0 -d -R stdout=<tty> -R stderr=<tty> -e dbg.exitkills=false <resolvedPath>`. With `-d`, rizin launches the artifact as a debuggee, and `dbg.exitkills=false` lets the inferior outlive the debugger. `cli.js:40999-41005` makes both `path` and `--inferior-tty` mandatory.
- `debug-with-gdb` (`cli.js:40947-40950`) also requires `--inferior-tty`. Its non-executing uses are no-inferior commands such as `show version`, or `core-file` on a supplied core. Even those emit `gdb_console` records, which Finding 1 shows cannot bind.
- `PROVINCE.md:103-105` (Adjacent): "**Non-REA dynamic analysis** — gdb scripting … `(unowned)`. gdb stays a fallback reader for supplied cores, not a lane-run tracer."
- `PROVINCE.md:30-31`: a catalog-listed tool is *available*, not *held*.
- `PROVINCE.md:168`: the lane's existing rizin ground is static `execute-rizin-command`, "read-only info commands only".
- `PROVINCE.md:175-176`: the dispositions "do not absorb revenger's contested runtime province".
- `claims.json:13` (move "hold zero-mention catalog verbs T1"), `:17` (T1 includes both debug verbs) and `:39` (`not_claimed`: "dynamic-analysis ownership (kaidoku/revenger overlap stays open)").
- The W2 contract forbids "target execution/debug attach".
- The inherited W1 plan intended exactly that execution: `.ufo/waves/round-22/gen-wave1.py:74-79` runs `debug-with-rizin` on a copied `/usr/bin/true` with `dr`, `dm` and `dbt`. The seats that were meant to adjudicate this boundary (`gen-wave1.py:236` RevProvinceDynamic, `:266` CriticDynamicScope) died with the 93-seat wave and left no report.

Holding `debug-with-rizin` in Core means the lane runs a tracer on its own target. That is the ground PROVINCE:103-105 refuses and `claims.json:39` disclaims. The claim names the verb as held ambition while the same declaration says the ownership question stays open. Those two statements are internally inconsistent.

**Hidden-regression risk:** if any later W2 report brings `rizin -d` or attached-gdb receipts, they violate the contract and MUST NOT count, even if a successor counter learns the alias.

**Impacted axes:** coverage (premature claim on contested ground), calibration.

## Finding 4 — the only honest-gap channel rejects the debug verbs, so they stay silently absent (OBSERVED)

R22-C2's standard is "gaps named honestly, not silently absent" (`claims.json:26`). Its table only accepts T2 verbs:

- `.ufo/waves/round-22/tools/count-c2.py:143`: `foreign = sorted({row["verb"] for row in rows} - set(T2))`.
- `:174-175`: exit 0 requires `not out["foreign_rows"]`.

**Counterexample (executed, same probe).** The probe copied HEAD's `PROVINCE.md` and its `evidence/c2/*.json` into a temp repo, then appended one honest row after `stop-adb-app`:

`| debug-with-rizin | adjacent | debug-with-rizin | error:invalid_request | .ufo/waves/round-22/evidence/c2/debug-with-rizin.json | probe: dynamic ground named, not held |`

The lane counter returned `accounted_count 14`, `mismatched []`, `foreign_rows ["debug-with-rizin"]`, exit 1, with empty stderr. Naming the debug gap in the calibration table breaks R22-C2.

The only naming on disk today is `PROVINCE.md:203-205`: "the remaining T1 debugger/signal verbs stay unclaimed unless separately demonstrated." That sentence gives no placement (Adjacent or frontier-blocked) and no reason. Its "unless separately demonstrated" suggests a demonstration that Findings 1 and 3 show is unreachable this round. `catalog_zero_count` at HEAD is 19, with both debug verbs among the zeros and labelled neither as boundary nor as gap.

**Impacted axes:** calibration.

## Measured state at lane HEAD (OBSERVED)

| argv | exit | stdout (key fields) | stderr |
|---|---|---|---|
| `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev HEAD` | 1 | rev `2ee3d9f5…`; `t1_exercised ["identify-flutter-build"]`, count 1/6; `catalog_zero_count 19`; debug-with-gdb and debug-with-rizin `entries 0, exercised false` | empty |
| `python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev HEAD` | 0 | `accounted_count 14`, `mismatched []`, `foreign_rows []` | empty |

Full stdout was retained in scratch at `/tmp/criticscope-c1-head.json` and `/tmp/criticscope-c2-head.json`. Both runs are read-only `git show` measurements. No build, test or lint was run.

## Smallest safe corrections (for L1; this seat edits nothing)

1. **Closure and lesson wording (needed this round).** Report C1 as `k=1/6`, stating that debug-with-gdb and debug-with-rizin are unbindable by the frozen counter: `bind` requires `debug_with_*`, while 6.5.0 emits `gdb_console`/`start_gdb_session` and `rizin_debug_command`. Add one `## Mistakes` row to `corpus/lessons/round-22.md`: class *vacuous — frozen target unreachable by construction*; evidence: this report's probe table; fix: a successor bind reads `CLI_COMMAND_TOOL_ALIASES` (the same mechanism as the existing objdump special case). Do NOT add the alias to the frozen-successor counter this round. That would move the goalposts after freeze, and it would also invite contract-forbidden `rizin -d` runs.
2. **Fixture honesty.** Next round, change the `all_six` case in `counter-fixtures.py:44-47,74` to use each verb's real 6.5.0 operation name. With the current bind it should then expect 4/6, and 6/6 only once alias-aware binding lands. This round, at minimum note in the lesson that `all_six` uses fabricated operations for the two debug verbs.
3. **Name the boundary outside the C2 table.** Replace the vague `PROVINCE.md:203-205` sentence with explicit prose under `### Round-22 narrowly added static ground`, for example: "`debug-with-rizin` launches the artifact under `rizin -d` (`dbg.exitkills=false`) and `debug-with-gdb` requires an inferior TTY; both are dynamic, Adjacent per PROVINCE:103-105, with the kaidoku/revenger L0 overlap open; not held; the C1 counter cannot bind their `gdb_console`/`rizin_debug_command` records." Do not add rows to the `### Round-22 catalog dispositions` table, because `count-c2.py:143,174-175` would turn C2 red (Finding 4).
4. **Future claims.** Remove both debug verbs from any coverage T-set until L0 resolves the kaidoku/revenger dynamic overlap. Static and refusal-only gdb uses (no inferior, or a supplied core) could later be claimed as narrow `adjacent` calibration rows in a counter whose T-set includes them.

## Tradeoff vs fixable

- Findings 1, 2 and 4 are fixable in wording and in next-round tooling. They do not flip either claim's verification at HEAD.
- Finding 3 is a tradeoff the canonical judge should reject if presented as coverage. Any closure text, or any later receipt, that counts `debug-with-rizin` execution or calls the debug verbs "held" or "frontier pending" claims contested dynamic ground, contradicting `claims.json:39` and `PROVINCE.md:103-105`.

## Scratch probe (retained for reproduction; not lane code)

`/tmp/criticscope-r22/probe.py`, sha256 `b70aae33554722862955fe8ffe8ef18e13f8ce64c0a645705b83e2b72813908f`. It copies the three round-20/21 dependencies (`.ufo/waves/round-20/tools/verb-coverage.py`, `.ufo/waves/round-21/tools/verb-coverage.py`, `.ufo/waves/round-20/verify/round20/verb-coverage.json`) into temp git repos. It writes one sourced knowledge entry plus a SOURCES S051 row and per-verb records for the three C1 cases, or HEAD's PROVINCE plus c2 receipts plus one debug row for the C2 case. It then invokes the lane's `tools/count-c1.py` / `tools/count-c2.py` by subprocess and removes each temp repo afterwards. Its full output is `/tmp/criticscope-r22/probe-out.json`; every case is summarized above.

## Tooling and safety

- No install or update was performed (no tool, version or channel change). No pacman transaction was run.
- No REA command was executed: I only read files in the installed 6.5.0 npx cache.
- No target execution, debug attach, ADB, Frida, remote connection, or credential/config inspection.
- No subagent was dispatched and no peer was messaged.
