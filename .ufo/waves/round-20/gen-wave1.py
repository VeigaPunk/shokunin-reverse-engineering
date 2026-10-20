#!/usr/bin/env python3
"""Generate the round-20 wave-1 spec (L1-authored). Writes wave1-spec.json next to this file."""
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
W17 = LANE + "/.ufo/waves/round-17"
W18 = LANE + "/.ufo/waves/round-18"
W19 = LANE + "/.ufo/waves/round-19"
W20 = LANE + "/.ufo/waves/round-20"
B = "14f0260ad319ecc26994381b2415d5a999003375"
SPOT = LANE + "/corpus/lessons/round-19-verifier-spotcheck.md"
L19 = LANE + "/corpus/lessons/round-19.md"
FREP = "/home/vgpnk/Projects/shokunin/.ufo/reports/round-19/kaidoku.md"
GO6 = "/home/vgpnk/.local/opt/go-1.24.6"
GO5 = "/home/vgpnk/.local/opt/go-1.25.0"
GH = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC"
WABT = "/home/vgpnk/.local/opt/wabt-1.0.42/bin"
PKG = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"
CON = W20 + "/contract.md"
REA = "npx -y rea-agents@6.5.0"
with open(os.path.expanduser("~/.agents/skills/godspeed/directive.md")) as f:
    DIRECTIVE = f.read()

RO = ("# Acceptance\nRead-only: write only your report. Cite exact path:line anchors, paste each command with its "
      "exit code, label observation vs inference, never fabricate.")
EX = (f"# Acceptance\nWork in your own clone per {CON} section `Writers` (clone at /tmp/kr20-<YourSeatName>); deliver "
      f"one patch at {W20}/w1/patches/<YourSeatName>.patch plus your report. Run your tool's --selftest once in the "
      "clone and paste the exact last line and exit code; paste every other command you ran with its exit. Cite "
      "path:line. Interfaces in the contract are binding.")
RUN = (f"# Acceptance\nWork in your own clone per {CON} `Writers`; retained evidence goes in your patch under "
       f"{W20}/evidence/c2/<leg>/ (path in the clone mirrors the lane): for every REA call keep argv, cwd, env keys "
       "set (names and values of REA_* only), start/end UTC, exit, stdout and stderr files with sha256 and the "
       "carrier path+sha256 in a receipt.json. Keep each file <= 8 MiB (xz-compress larger stdout and keep its sha256 "
       "before and after compression). Deliver the patch at "
       f"{W20}/w1/patches/<YourSeatName>.patch and a report summarising observations (Evidence IDs, subject sha256, "
       "statuses, limitations) with path:line pointers into your retained files.")
DR = ("# Acceptance\nRead-only except your report: put the drafted text verbatim in your report under a heading "
      "`## Draft`, every factual sentence carrying its path:line, URL or command source. The L1 integrates; never "
      "edit lane files.")
SRC = ("# Acceptance\nRead-only except your report. Open the source yourself now (curl/gh/web fetch), record the exact URL, "
       "access date (`date -Iseconds`), the document's sha256 when fetchable, and one contiguous <=25-word quote with "
       "its located section/line. Under `## Draft` give a complete SOURCES.md row in the 11-column contract shape "
       "(id `S0NN` placeholder; kind, tier scoped to `scope`, anchor with revision, teaches, status queued, opened, "
       "recheck, used-by —) — or a REJECTED row with reason and flip if it does not support the scope. Never "
       "fabricate a quote.")

items = []


def add(name, role, body, acc):
    items.append({"name": name, "role": role,
                  "prompt": "/skill:godspeed\n" + DIRECTIVE + "\n" + body.strip() + "\n" + acc})


# ================= C1 executors: routed round-19 defects =================
add("RoutedR19Tool", "executor", f"""
# Target
Create {W20}/tools/routed-r19.py — the C1 counter: `python3 -I -B routed-r19.py --root LANE --rev REV [--strict]
[--live] [--selftest]`. Items (from {SPOT}:178-190): D1, D2, D3, D4, D5, D6a, D6b, D6c, D6d, D6e, D6f. An item is
OPEN unless BOTH (a) named: `SCORECARD.md` and `corpus/lessons/round-20.md` at REV each contain a line starting
`- R19-<ITEM>:` and (b) substance passes, executing REV's own tool bytes extracted from Git objects into mkdtemp
(never the working tree) against attack fixtures you build, using exactly the interfaces in {CON} §Interfaces:
D1 custody-pair refuses an in-worktree scratch (exit 2, `scratch_inside_worktree`) and leaves no
`custody-pair-selftest-*` under an outside scratch; with `--live`, also no untracked nested `.git` under LANE/.ufo
(`git -C LANE status --porcelain --ignored`). D2 REV's evidence-timestamps.py flags `.ufo/waves/round-19/claims.json:36`
at rev {B} (exit 1, `future_dated`) and passes a clean fixture. D3 REV's carrier-guard.py selftest is CLEAN and its
`exec_refused` and `mode_restored` cases appear; plus `.ufo/waves/round-20/evidence/carrier-guard/` at REV holds an
arm.json and >=1 check record with exit 0 whose carrier set equals predictions/carriers.tsv (if that file exists at REV).
D4 c1-census-v10.py from REV, run over a `git archive REV` export in mkdtemp, prints `VERDICT: PASS` exit 0. D5
`.ufo/waves/round-20/verify/final-census.json` at REV names a rev whose tree differs from REV only in that record and its
stdout file, exit 0, stdout sha256 matches. D6a REV head-rev-lint.py reports a `nested` finding for round-17 verify.py
and revpin.py. D6b REV revexec.py selftest CLEAN with `write_outside_refused`,`net_refused`; AND routed-r19.py itself
executes REV tools only through revexec (self-check by AST: no direct subprocess of extracted .py except via revexec).
D6c REV citation-drift-probe.py exits 2 `slug_unsafe` for slugs `../x`, `a/b`, and a symlink escape fixture. D6d REV
receipt-validate.py rejects a receipt whose only `analyze` token sits outside the post-package position
(`analyze_step_unauthenticated`). D6e REV wave-outcomes.py counts a seat named `causes` correctly in a fixture. D6f REV
jj-red-before.py --selftest exit 0 with >=2 more `jj_` case ids than at {B}.
Output JSON {{rev, open_count, named_open, substance_open, items:[{{id, named, substance, why}}]}}; --strict exit 1 if open.
Selftest with fixtures that keep token-only closures OPEN. Run `--rev {B}` (expect 11 open) and paste.""", EX)
add("CustodySelftestFix", "executor", f"""
# Target
Fix round-19 D1 ({SPOT}:180-181): {LANE}/.ufo/gates/custody-pair/custody-pair.py selftest (`run_selftest`, ~:887-1420)
created nested fixture repos `repo-fixture`/`repo-sub-fixture` under `--scratch` which round-19 verify.py pointed
inside the lane ({W19}/verify.py:537-539), leaving untracked nested repos. Implement the D1 interface in {CON}:
refuse a scratch inside any Git worktree (exit 2, `scratch_inside_worktree`), always remove the selftest dir on exit
(try/finally, also on failure), and add selftest cases `scratch_in_worktree_refused` and `cleanup_after_run`. Update
the README in that dir with one line. Paste selftest before/after (before: run the baseline tool with
`--scratch <a dir inside your clone>` and show it creates the nested repos — the red-before).""", EX)
add("EvidenceTimestampLint", "executor", f"""
# Target
Create {W20}/tools/evidence-timestamps.py per the D2 interface in {CON} (round-19 D2: `{W19}/claims.json:36` asserts
16:20:00-03:00 inside commit 4f6c73f committed 16:09:17 -03). Use `git blame --porcelain REV -- path` for the
introducing commit's committer-time of each line. Skip binary files; cap per-file size at 4 MiB (report skipped). Ignore
timestamps inside lines that are explicit quotations of another file only if marked `quoted:`? — no: report every
finding; offer `--allow FILE:LINE` exemptions recorded in output. Red-before: at rev {B} with `--path .ufo/waves/round-19`
it must report claims.json:36 (paste); also run over `.ufo/waves/round-18` and `round-17` and paste the finding list.
Selftest cases: `future_line_flagged`, `past_line_clean`, `zulu_and_offset_parsed`, `later_commit_line_uses_own_time`.""", EX)
add("CarrierGuardTool", "executor", f"""
# Target
Create {W20}/tools/carrier-guard.py per the D3 interface in {CON} (round-19 D3: a seat ran `bin/go version` despite the
no-carrier-execution contract; nothing prevented or detected it). Manifest TSV columns `label<TAB>path<TAB>...`.
arm must refuse (exit 2) if any manifest path is not a regular file. check also re-verifies sha256. Records are JSON with
UTC `taken_at_utc` from the clock. The L1 already cleared exec bits manually and recorded them in
{W20}/evidence/carrier-guard/manual-arm.json — add `adopt --from manual-arm.json --record DIR` that converts that record
into an arm.json (original modes from `mode_before`) without touching files. Never run against real carriers in your
clone; selftest uses mkdtemp copies of /usr/bin/true. Document the loader-mapped and root limits in the module docstring.""", EX)
add("CensusRekey", "executor", f"""
# Target
Round-19 D4 ({SPOT}:186-187): {LANE}/.ufo/gates/c1-census-v10.py exits 1 `undeclared=2` on SCORECARD.md 2380-2382 and
SKILL.md 511-519 (round-17 text). Read those lines at {B}, decide their true class in the gate's SCOPE table (~:254-290;
CURRENT vs HISTORICAL etc.) and declare them so the gate grades them — never delete a check, widen an unrelated range, or
mark live pins historical to silence them. If SKILL.md line numbers are fragile, key the row by a stable anchor the gate
already supports, or add anchor support with a selftest. Show: baseline run exit 1 in your clone; patched run
`VERDICT: PASS` exit 0; selftest/fixture proving a NEW undeclared block still FAILs (anti-vacuity).""", EX)
add("HeadRevNested", "executor", f"""
# Target
Round-19 D6a: {W18}/tools/head-rev-lint.py misses two nested compare-only HEAD reads (round-17 `verify.py`, `revpin.py`),
registered as a limit in SKILL.md. A dead round-19 seat's attempt failed its selftest
({W19}/w1/inherited/HeadRevLintNested.patch; {L19}:33). Implement a `nested` class that detects HEAD reads reached via a
nested helper call (compare-only) and reports them separately from live reads; keep all existing selftest cases green and
add `nested_compare_only` cases. Run on the lane at {B} and paste the new findings.""", EX)
add("RevexecSandbox", "executor", f"""
# Target
Round-19 D6b ({L19}:176-179: "Trusted lane Python/JavaScript is still executed by checker/catalog tools: mkdtemp is not
an OS security sandbox"). Create {W20}/tools/revexec.py per the D6b interface in {CON}. bwrap is not installed and pacman is
paused: probe `unshare --user --map-root-user --net --mount` (util-linux) and/or `systemd-run --user --pipe --wait -p
PrivateNetwork=yes -p ProtectHome=read-only`; pick what actually works on this host, paste the probe. Inside: network
namespace without interfaces, every path read-only except the mkdtemp work dir (e.g. `mount --bind -o remount,ro` the
root in the user+mount namespace, then bind the work dir rw). Selftest cases `write_outside_refused` (write to a mkdtemp
sibling outside work dir fails), `net_refused` (connect to 127.0.0.1 on a listening port opened outside the sandbox
fails), `runs_ok`. Docstring states the residual trust (same uid; kernel bugs; not a security boundary against root).""", EX)
add("CitationSlugEscape", "executor", f"""
# Target
Round-19 D6c ({L19}:180-181): {LANE}/.ufo/gates/citation-drift/citation-drift-probe.py `_snapshot(slug)` (~:159-170)
reads `@<slug>` from --snapshot-dir; an adversarial table/expected pair can escape it. Implement the D6c interface in
{CON}; add selftest `slug_escape_refused` (cases `../x`, `a/b`, absolute, symlink pointing outside). Show the escape
red-before on the baseline tool in your clone (a fixture that reads a file outside the snapshot dir), then green.""", EX)
add("ArgvDecoy", "executor", f"""
# Target
Round-19 D6d ({L19}:182-183): {W17}/tools/receipt-validate.py identifies the analyze step by `step`/`name` "analyze" or
an argv carrying the `analyze` token (~:38 docstring); a decoy token in an unrelated command passes. Implement the D6d
interface in {CON}; selftest `argv_decoy_refused` plus a positive case. Then re-run the patched validator
`--require-mid-maps` on every round-18 and round-19 pass2 receipt ({W18}/runs/*/receipt.json,
{W19}/runs/pass2/*/receipt.json) in your clone and paste exits (they must stay 0, or explain each change).""", EX)
add("CausesKeyCollision", "executor", f"""
# Target
Round-19 D6e ({L19}:183-184): {W19}/tools/wave-outcomes.py treats a flat map containing key `causes` as the wrapper,
so a seat literally named `causes` collides. Implement the D6e interface in {CON} (e.g. wrapper detection only when the
`causes` value is an object AND a `wave` key is present, or a schema tag); selftest `seat_named_causes`; re-run the tool
on the round-18 and round-19 inputs used in round 19 (see {W19}/verify.py for argv) and paste identical outputs.""", EX)
add("JjSelftestGaps", "executor", f"""
# Target
Round-19 D6f ({L19}:184-185, "jj sandbox selftest coverage limits"): read {W18}/tools/jj-red-before.py and its selftest,
the round-19 report {FREP} residual-limits text and {W19}/w2 reports mentioning jj (grep -l jj). Name the concrete
uncovered behaviours (e.g. detached HEAD in colocated repo, bookmark ahead of git ref, conflicted op), and add
selftest cases `jj_<gap>` (>=2) that run in mkdtemp sandbox repos only (never the lane; jj 0.45.1 at ~/.local/bin/jj).
Paste case count before/after.""", EX)
add("FinalCensusRecorder", "executor", f"""
# Target
Round-19 D5: create {W20}/tools/final-census.py: `--root LANE --out-dir W20/verify` runs `python3 -I -B
.ufo/gates/c1-census-v10.py --root LANE` and `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kaidoku`, records {{rev: `git rev-parse refs/heads/main`, worktree_clean: bool (porcelain
empty except the out files), argv, exit, stdout_path, stdout_sha256, taken_at_utc}} into final-census.json; refuses
(exit 2) if the worktree has tracked modifications. Selftest on a mkdtemp fixture repo outside any worktree.""", EX)

# ================= C2 executors: verb coverage =================
add("VerbCoverageTool", "executor", f"""
# Target
Create {W20}/tools/verb-coverage.py per the C2 interface in {CON}. Read CLI_COMMAND_NAMES via
`node --input-type=module -e` importing `file://{PKG}/dist/cliCommandNames.js` (pattern: {W19}/tools/rea-catalog.py
PROBE). Token boundary: the name or its underscore form not adjacent to `[a-z0-9_-]`. Output JSON {{rev, package_version,
cli_commands, mentioned, zero:[...], per_command counts, targets{{...}}}}; default targets = the five in {W20}/claims.json
C2. Run at --rev {B}: paste `mentioned`/`cli_commands` and the zero list (L1 shell sweep found 128/153 with 25 zero).
Selftest: fixture repo with entries mentioning / not mentioning, underscore form, substring trap (`inspect-artifact` must
not count from `inspect-artifact-x`), exercised requires ev id + existing evidence path.""", EX)
add("WasmInspectLeg", "executor", f"""
# Target
C2 leg: run `{REA} inspect-wasm-artifact <path> --format json` with `REA_WABT_BIN_DIRECTORY={WABT}` on >=3 real shipped
WASM carriers (candidates: {PKG}/../evmole/dist/evmole_bg.wasm (480805 B),
{PKG}/../@zip.js/zip.js/dist/zip-module.wasm (55126 B), /opt/ZCode/resources/glm/packages/pdf-plugin/dist/ui/pdfjs/wasm/qcms_bg.wasm,
.../openjpeg.wasm). Record identity (sha256, owning package via `pacman -Qo` or npm package.json version), Evidence IDs,
sections/imports/exports counts, limitations/unknowns, WABT version banner; repeat one call to test Evidence-ID
determinism. Leg dir `wasm-inspect`.""", RUN)
add("WasmCompareLeg", "executor", f"""
# Target
C2 leg: exercise `{REA} compare-wasm-interfaces` (read `--schema` first) with `REA_WABT_BIN_DIRECTORY={WABT}`. It needs two
authenticated inspect_wasm_artifact Evidence records inline. Find a genuine version pair of one WASM module on this host
(e.g. the same module shipped by two packages/versions: search `find / -xdev -name '*.wasm' 2>/dev/null` under /usr/lib,
/opt, ~/.npm/_npx; compare sha256 and package versions) plus one identical-bytes control pair. Retain both inspect
envelopes and every compare output; report statuses for imports/exports/both. Leg dir `wasm-compare`.""", RUN)
add("WasmRefusalLeg", "executor", f"""
# Target
C2 leg: refusal/limit taxonomy of `{REA} inspect-wasm-artifact`: (a) REA_WABT_BIN_DIRECTORY unset; (b) pointed at a dir
with a fake wasm-objdump printing another version; (c) a truncated copy (first 1000 bytes) of a real wasm in mkdtemp;
(d) a non-wasm file; (e) `--glue_paths` with the JS glue next to evmole_bg.wasm. Retain every envelope; classify each
error code/message and whether an Evidence record was emitted. Leg dir `wasm-refusals`.""", RUN)
add("RizinLeg", "executor", f"""
# Target
C2 leg: `{REA} execute-rizin-command <path> <command> --format json` (rizin 0.8.2 at /usr/bin/rizin) on /usr/bin/jq and
/usr/lib/libjq.so.1 with read-only commands `iI`, `iS`, `ie`, `il`, `izj~?` (or similar). Record Evidence IDs, the argv
REA passes (`command_arguments`), provider version field, output caps/truncation, determinism of a repeated call, and
cross-check one result against readelf. Never use write/debug commands. Leg dir `rizin`.""", RUN)
add("RizinPeLeg", "executor", f"""
# Target
C2 leg: `{REA} execute-rizin-command` on a PE (find `cli-64.exe` used in round 2: `git -C {LANE} grep -n cli-64.exe
refs/heads/main -- corpus/knowledge | head`) with `iI`/`iS`, plus the error taxonomy: nonexistent path, a directory,
an unknown rizin command, a command with `;` chaining or `!` shell escape (record whether REA refuses or rizin runs it
— do NOT use any command that writes files or executes programs; use `!echo` only if REA documents shell escapes as
refused, otherwise skip and say so). Leg dir `rizin-pe`.""", RUN)
add("ObjdumpArchLeg", "executor", f"""
# Target
C2 leg: `{REA} list-objdump-architectures --format json` (read `--schema`), compare with `objdump -i` / `objdump --help`
target lists on this host (binutils version), and exercise one `inspect-with-objdump` operation not held before (held:
`file_headers` only, corpus/knowledge/2026-10-16-l7-06-inspect-with-objdump.md) on /usr/bin/jq. Leg dir `objdump`.""", RUN)
add("HarmonyLeg", "executor", f"""
# Target
C2 leg: `{REA} project-harmony-application-graph` (read `--schema`; source in {PKG}/dist — grep -ril harmony). It projects
authenticated inventory Evidence of a HAP/HSP/App Pack. No HarmonyOS package exists on this host: synthesize a minimal
Stage-model HAP (zip with `module.json` declaring a module + one ability, plus a `resources.index` and an `ets/modules.abc`
placeholder) and an FA-model variant (`config.json`), recipe retained byte-exact (QUALITY #12), run `{REA} inspect-artifact`
on each and feed the inventory Evidence to the projection. Report packaging-model hints and what is unknown. Leg dir
`harmony`.""", RUN)

# ================= C3 executors: first-failure emulator =================
add("EmulatorV2", "executor", f"""
# Target
Create {W20}/tools/swiss-misread-v2.py from {W18}/tools/swiss-misread.py (unchanged r18 emulator) per the C3 interface
in {CON}: (1) mask the func-type variadic bit (0x8000) of outCount as Ghidra does (`GoFuncType.java:79,86` in
{GH}/Ghidra/Features/Base/lib/Base-src.zip) — round 19 found the unmasked walk read 32771 params (see
{LANE}/corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md "Preserved second pass and model rejection");
(2) emit `first_failure` per hypothesis = the first read failure in Ghidra's actual order with kind/index/va/phase,
null if silent; keep every r18 field. Selftest: keep r18 cases, add `variadic_masked` and `first_failure_shape`. Run
v2 (byte reading only) on the eight round-19 carriers {GO5}/bin/{{go,gofmt}} and {GO5}/pkg/tool/linux_amd64/
{{asm,cgo,compile,cover,preprofile,vet}} and paste first_failure per label (retro input; round-19 logs say vet
H1 Invalid index 13902080, others silent). Do not run Ghidra/REA.""", EX)
add("FirstFailureExtract", "executor", f"""
# Target
Create {W20}/tools/first-failure-extract.py per the C3 interface in {CON}: from a bound Ghidra log, the FIRST Go-analysis
failure (component Golang*/GoRttiMapper/GoTypeManager; `Invalid index: N` EOFException, `Unable to read past EOF`, other
IOException) with line number, plus a separate `other_errors` list (e.g. AnalysisTaskWrapper NPEs) never folded in.
Absence is claimed only up to the last line. Run on all round-19 logs ({W19}/runs/*/logs/*/ghidra.log and
runs/pass2/...) and round-18 logs ({W18}/runs/*/logs/*/ghidra.log); paste a table label→first failure. Selftest with
synthetic log snippets.""", EX)
add("CompareFirstFailure", "executor", f"""
# Target
Create {W20}/tools/compare-first-failure.py per the C3 interface in {CON}: compares a frozen prediction's
`first_failure.h1` (the D hypothesis) with the extractor's result: match = both null, or same kind and same index; it
imports/executes the extractor from a path argument (`--extractor`), records both objects, exit 0/1/2. Selftest. Then
produce {W20}/tools/retro-v2.py that, given v2 outputs (JSON dir) and round-19 pass2 logs, writes a retro table (label,
predicted, observed, match) — run it with stub v2 JSONs you construct from round-19 frozen predictions to show the plumbing.""", EX)
add("GenPredictionsR20", "executor", f"""
# Target
Create {W20}/gen-predictions.py (pattern: {W19}/gen-predictions.py): reads {W20}/predictions/carriers.tsv (create it:
labels t1246-<tool> for {GO6}/bin/{{go,gofmt}} and {GO6}/pkg/tool/linux_amd64/{{asm,cgo,compile,cover,preprofile,vet,
pprof,trace}}, columns label/path/class/sha256), runs {W20}/tools/swiss-misread-v2.py per carrier (byte reading only;
until EmulatorV2 lands use a `--emulator` path arg), writes predictions/swiss-misread-v2/<label>.json,
<label>.prediction.json (first_failure.h1 as the forecast; extra_expectations none), decision-rule.json (D = labels with
h1 first_failure non-null and h0 null; compare rule = compare-first-failure; binding gate as round 19) and SHA256SUMS.
Exclude carriers with no Go build info (record why). Paste the carriers.tsv you generated (sha256 of each).""", EX)
add("RunnerR20", "executor", f"""
# Target
Create {W20}/run-carriers.sh from {W19}/run-carriers.sh: carriers from {W20}/predictions/carriers.tsv, outputs under
{W20}/runs/<label>/ (receipt.json as round 19, logs bound by session path + digest), compare step =
{W20}/tools/compare-first-failure.py, and before each label `python3 -I -B {W20}/tools/carrier-guard.py check --manifest
predictions/carriers.tsv --record evidence/carrier-guard` (abort the run on exit 1). Add `--dry-run` that prints the
plan without running REA. Shellcheck it if available. Never run it for real (the L1 runs it after freezing).""", EX)
add("MeasureR20", "executor", f"""
# Target
Create {W20}/measure.py REV (pattern {W19}/measure.py): fields c1 (routed-r19 --strict summary via
{W20}/tools/routed-r19.py), c2 (verb-coverage summary), c3.first_failure_bound = labels whose prediction blob at REV equals the
freeze commit blob (`--freeze <hash>` argument), whose receipt validates (`{W17}/tools/receipt-validate.py
--require-mid-maps`), and that have a compare-first-failure record; c3.matched; plus raw counts. Read Git objects at REV
only; tools executed from REV blobs. Selftest on a mkdtemp fixture repo.""", EX)
add("ControlsR20", "executor", f"""
# Target
Create {W20}/controls-r20.py BASE SOURCE (pattern {W19}/controls-r19.py): no-harm controls — README coverage map rows vs
knowledge files (command A: no missing/dangling), depth citation proxy, QUALITY rows 1-22 byte-identical, LOG.md and
SCORECARD.md BASE bytes are a prefix of SOURCE, prior lessons unchanged, round-17/18/19 runs/predictions unchanged except
files the round-20 routed fixes list explicitly (tools edited in place: custody-pair.py, citation-drift-probe.py,
receipt-validate.py, head-rev-lint.py, wave-outcomes.py, jj-red-before.py, c1-census-v10.py), SOURCES rows append-only
except status/recheck/used-by cells (print each changed cell old→new). Run BASE=SOURCE={B} and paste.""", EX)
add("VerifyR20", "executor", f"""
# Target
Create {W20}/verify.py (pattern {W19}/verify.py) that runs every round-20 counting command at B={B} and at a SOURCE rev
argument, records argv/exit/expected_exit/stdout/stderr sha256 into {W20}/verification.json and files under
{W20}/verify/. ALL scratch/selftest dirs go to tempfile.mkdtemp() outside the lane (round-19 D1 was verify.py:537-539
passing a lane scratch). Include: routed-r19 --strict at B (expect 1) and SOURCE (0), verb-coverage at both, measure.py,
controls-r20, evidence-timestamps over .ufo/waves/round-20 at SOURCE (expect 0), each new tool --selftest, census. Dry-run
in your clone at B and paste the command table.""", EX)

# ================= scouts (m_flash) =================
add("ScoutLaneScratchWriters", "scout", f"""
# Target
Sweep every lane tool under {LANE}/.ufo (gates + waves/round-1[6-9]/tools + verify/measure scripts) for writes inside the
lane tree during selftests/verification: `mkdtemp(dir=`, `--scratch`, `TMPDIR`, fixed output dirs. List each with
path:line and whether it can leave untracked or nested-repo residue (round-19 D1 class).""", RO)
add("ScoutTimestampOracle", "scout", f"""
# Target
Independent oracle for round-19 D2: in {LANE} at {B}, find every timestamp with an explicit zone in committed files under
.ufo/waves/round-19 and round-18 that is later than the committer time of the commit introducing its line (use git
blame --porcelain). Paste the full list (expected includes round-19/claims.json:36).""", RO)
add("ScoutCarrierExecPaths", "scout", f"""
# Target
Round-19 D3 recon: list every way a seat could execute a Go carrier on this host despite cleared exec bits (loader
`/lib64/ld-linux-x86-64.so.2 <file>`, copying the file, sudo, `go` on PATH?). Check `command -v go`, PATH entries,
whether any other lane's committed files reference {GO6} or {GO5} executables as tools (read-only grep over
/home/vgpnk/Projects/shokunin/*-shokunin, excluding .git). Never execute any Go binary.""", RO)
add("ScoutCensusBlocks", "scout", f"""
# Target
Show the exact text of SCORECARD.md 2380-2382 and SKILL.md 511-519 at {B}, the c1-census-v10.py SCOPE table rows and the
classify() rules (~:129-300), and propose the true scope class of each block with reasons. Run the census at {B} in a
`git archive` export under mkdtemp and paste the UNDECLARED section.""", RO)
add("ScoutHeadRevNested", "scout", f"""
# Target
Locate the two nested compare-only HEAD reads in round-17 verify.py and revpin.py (path:line), the call chain from the
entry point, and why {W19}/w1/inherited/HeadRevLintNested.patch failed (apply it to a /tmp clone at {B}, run
`--selftest`, paste the FAILED lines). Read-only in the lane.""", RO)
add("ScoutSandboxPrimitives", "scout", f"""
# Target
Probe sandbox primitives on this host for D6b (no installs): `unshare --user --map-root-user --net --mount true`,
`cat /proc/sys/kernel/unprivileged_userns_clone /proc/sys/user/max_user_namespaces`, `systemd-run --user --pipe --wait -p
PrivateNetwork=yes true`, `command -v bwrap firejail nsjail`. Paste each with exit; say which give network isolation and
read-only root for an unprivileged user.""", RO)
add("ScoutSlugEscape", "scout", f"""
# Target
In {LANE}/.ufo/gates/citation-drift/citation-drift-probe.py, trace how `@<slug>` targets resolve against --snapshot-dir
and the expected.json digest check; describe an exact escape (table + expected pair) and whether the digest check
mitigates it. path:line.""", RO)
add("ScoutArgvDecoy", "scout", f"""
# Target
In {W17}/tools/receipt-validate.py, trace analyze-step identification for object and list `steps` shapes; describe an
exact decoy receipt that passes at {B}; list every retained round-18/19 receipt's analyze argv shape (jq over
{W18}/runs/*/receipt.json and {W19}/runs/pass2/*/receipt.json) so a fix keeps them valid.""", RO)
add("ScoutCausesKey", "scout", f"""
# Target
In {W19}/tools/wave-outcomes.py, trace wrapped vs flat causes-map detection; construct the collision input; list every
causes file the lane has committed (round-18/19 evidence/wave-outcomes) and its shape.""", RO)
add("ScoutJjGaps", "scout", f"""
# Target
Enumerate {W18}/tools/jj-red-before.py selftest cases (ids, what each covers) and every round-19 mention of jj selftest
gaps ({FREP}, {L19}, {W19}/w2/*.md: grep -n jj). Propose the concrete missing cases with reasons.""", RO)
add("ScoutWasmSchema", "scout", f"""
# Target
Capture `{REA} inspect-wasm-artifact --schema`, `{REA} compare-wasm-interfaces --schema` and the matching `--llms-full`
sections; summarize inputs, outputs, detail options, WABT requirements. Paste schema excerpts with sha256 of full output.""", RO)
add("ScoutRizinSchema", "scout", f"""
# Target
Capture `{REA} execute-rizin-command --schema` and `--llms-full` section; grep {PKG}/dist for REA_RIZIN_COMMAND and the
command-observation implementation: argv, timeout, output caps, command allow/deny rules. path:line.""", RO)
add("ScoutHarmonySchema", "scout", f"""
# Target
Capture `{REA} project-harmony-application-graph --schema`; grep {PKG}/dist for harmony/HAP/module.json/config.json logic;
state exactly what inventory Evidence and archive members the projection needs. path:line.""", RO)
add("ScoutObjdumpArch", "scout", f"""
# Target
Capture `{REA} list-objdump-architectures --schema` and one run's output summary; `objdump --version`; which other
`inspect-with-objdump` operations exist (schema) beyond file_headers.""", RO)
add("ScoutWasmCarriers", "scout", f"""
# Target
Inventory WASM carriers on this host: `find /usr/lib /opt /home/vgpnk/.npm/_npx -xdev -name '*.wasm' -size +1k`
with sizes, sha256, owning pacman package (`pacman -Qo`) or npm package name+version (nearest package.json). Identify
same-module version pairs (same filename/package, different versions and sha256). Table.""", RO)
add("ScoutGo1246Carriers", "scout", f"""
# Target
C3 carrier recon (never execute any Go binary): for {GO6}/bin/* and pkg/tool/linux_amd64/* give size, sha256, whether the
bytes contain `\\xff Go buildinf:` and the Go version string (python byte search / `strings -a | grep -m1 go1.24`); confirm
the install matches the official archive (go.dev JSON go1.24.6 linux-amd64 sha256 bbca37cc…8712 per {L19}:71-73; nine-member
spot-hash against a fresh download in /tmp if feasible). Prior exposure: grep the lane's committed .ufo/waves for each
file's sha256 and path to prove none was ever analyzed by REA/Ghidra (round-18 used go1.24.6 only to build synthetics).""", RO)
add("ScoutGhidraVariadic", "scout", f"""
# Target
From {GH}/Ghidra/Features/Base/lib/Base-src.zip, extract and quote (path:line) GoFuncType.java variadic/outCount masking,
GoTypeManager.java failure handling around :639-646, and GolangSymbolAnalyzer's abort behaviour on the first IOException.
State precisely what "first failure" in the log means in Ghidra's order.""", RO)
add("ScoutLogFirstFailures", "scout", f"""
# Target
Oracle for the extractor: for every bound Ghidra log under {W19}/runs (both passes) and {W18}/runs, give the first
Go-analysis failure line (line number + text) or `none up to line N`, and any non-Golang error lines (AnalysisTaskWrapper
NPE etc.). Table; use grep -n only.""", RO)
add("ScoutVerbZeroOracle", "scout", f"""
# Target
Independent oracle for C2: list the 153 CLI_COMMAND_NAMES of {PKG} (node import of dist/cliCommandNames.js) and, for each,
whether any corpus/knowledge entry at {B} names it (hyphen or underscore form, token boundary; `git grep` on refs/heads/main).
Paste the count and the zero list.""", RO)
add("ScoutInheritedState", "scout", f"""
# Target
Inherited-state sweep: `git -C {LANE} status --porcelain --ignored`, untracked nested `.git` dirs under {LANE}/.ufo
(`find {LANE}/.ufo -name .git -prune`), and any `lane-dead-no-report kaidoku round=20` line in
/home/vgpnk/Projects/shokunin/.ufo/watchdog.log. List each residue path with its creator (mtime, content).""", RO)
add("ScoutOperatorLessons", "scout", f"""
# Target
List {LANE}/corpus/lessons/operator-*.md (if any) and for each whether QUALITY.md or SKILL.md cites it at {B}. Also list
which QUALITY rows cite which lessons (row → lesson path).""", RO)
add("ScoutGo1273Exposure", "scout", f"""
# Target
/home/vgpnk/.local/opt/go-1.27.3 exists: who installed it (mtimes, lane records: git grep 1.27.3 across the lane), is it
an official archive (go.dev JSON), and would its toolchain ELFs be suitable later carriers (Ghidra Go snapshot coverage for
1.27 in {GH}/Ghidra/Features/Base/data/typeinfo/golang). Never execute.""", RO)

# ================= reviewers (m_zfl) — first falsifiers =================
add("ReviewClaimsC1", "reviewer", f"""
# Target
Attack C1 in {W20}/claims.json against {SPOT}:178-190: is the 11-item split faithful (nothing dropped, nothing invented)?
Which substance check in {CON} §Interfaces could pass vacuously? Propose stricter checks.""", RO)
add("ReviewClaimsC2", "reviewer", f"""
# Target
Attack C2 in {W20}/claims.json: is "named in an admitted knowledge entry" a defensible coverage observable; can the 128
baseline be gamed; what must `exercised` require so a mention cannot count; does it need a coverage-map row per verb?""", RO)
add("ReviewClaimsC3", "reviewer", f"""
# Target
Attack C3 in {W20}/claims.json: first-failure forecast definition, freeze ordering, carrier exposure, whether the retro
check on round-19 logs (outcomes already known) can be misread as prediction evidence; list falsifiers to pin now.""", RO)
add("ReviewSeparability", "reviewer", f"""
# Target
Check causal separability of C1/C2/C3 in {W20}/claims.json: can each be verified with the others reverted? Name any shared
file or tool coupling (e.g. receipt-validate edits used by C3 measurement) and how to keep them separable.""", RO)
add("ReviewQualityRows", "reviewer", f"""
# Target
Read {LANE}/corpus/QUALITY.md rows 18-22 and {SPOT}:178-190; propose grounded QUALITY #23 (evidence timestamps at or
before shipping commit, mechanised) and #24 (a no-execution contract needs a technical guard record) — check neither
duplicates an existing row; compute the rows 1-22 digest at {B} (`git show {B}:corpus/QUALITY.md | grep -E '^\\| *([1-9]|1[0-9]|2[0-2]) *\\|' | sha256sum`).""", RO)
add("ReviewR19Open", "reviewer", f"""
# Target
Review {L19} Open (:95-101), residual limits (:180-191) and Mistakes (:82-91): which items are not covered by D1-D6 and
still open; which fixes were not shown able to fail.""", RO)
add("ReviewCensusGate", "reviewer", f"""
# Target
Review {LANE}/.ufo/gates/c1-census-v10.py: what PASS requires, how SCOPE rows are graded, and which kinds of re-key would be
suppression rather than declaration. Give the anti-vacuity test a rekey must keep.""", RO)
add("ReviewReceiptValidate", "reviewer", f"""
# Target
Review {W17}/tools/receipt-validate.py tests: which validated properties lack a red selftest case; how the D6d fix could
break retained receipts.""", RO)
add("ReviewRunCarriers", "reviewer", f"""
# Target
Review {W19}/run-carriers.sh: everything that must change for round 20 (carriers, outputs, compare step, guard check), and
any place it could execute a carrier or write inside the lane outside runs/.""", RO)
add("ReviewVerifyScratch", "reviewer", f"""
# Target
Review {W19}/verify.py for every scratch/output path, selftest invocation and timestamp it writes; list what round-20
verify.py must do differently (D1 scratch, D2 timestamps, D5 final census).""", RO)
add("ReviewSourcesRegistry", "reviewer", f"""
# Target
Run the CORPUS.md manual census commands (/home/vgpnk/Projects/shokunin/CORPUS.md:133-148) on {LANE}/corpus/SOURCES.md at
{B} (git show into mkdtemp) and the maintained `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kaidoku`; paste outputs; next free id; rules a new row must satisfy.""", RO)
add("ReviewSkillRegistry", "reviewer", f"""
# Target
Read the gate/probe registry in {LANE}/SKILL.md (grep -n 'gate|\\|probe|'); list the row fields (PROTOCOL Gate standard)
and draft-check what rows the new round-20 tools need (evidence-timestamps, carrier-guard, revexec, verb-coverage,
swiss-misread-v2, first-failure-extract, compare-first-failure, routed-r19, final-census) — gate vs probe each.""", RO)
add("ReviewProvinceCoverage", "reviewer", f"""
# Target
Which PROVINCE.md and corpus/README.md rows must change when the five C2 verbs become held (Core rows, coverage map
sections, Frontier, Known gaps)? Keep README coordinates of Frontier/frozen pointers stable (round-19 SkillRegistryOld
lesson {L19}:170-175).""", RO)
add("ReviewDeadSeatRecording", "reviewer", f"""
# Target
Per QUALITY #22, describe how round 20 must record wave outcomes: inputs for {W19}/tools/wave-outcomes.py, cutoff naming,
per-seat causes for reportless seats; check {W19}/evidence/wave-outcomes for the round-19 pattern.""", RO)
add("ReviewSpotcheckDisagreements", "reviewer", f"""
# Target
Read {SPOT} and the round-18/17 spotchecks' Discernment sections: any disagreement not yet turned into a QUALITY row?
List with pointers.""", RO)
add("ReviewTimestampFormats", "reviewer", f"""
# Target
Survey timestamp formats in committed lane evidence ({LANE}/.ufo/waves/round-1[7-9], corpus/lessons, SCORECARD round
sections): ISO with offset, `HH:MM -03`, Z, epoch. Which must the D2 lint parse; which are quoted historical instants that
would false-positive?""", RO)

# ================= revengers (m_zfl) =================
add("RevWasmVerb", "revenger", f"""
# Target
Reverse-engineer {PKG}/dist/domain/wasm/wasmArtifact.js and the wasm contracts: WABT version gate (`1.0.42`), which WABT
binaries run with which argv, what is parsed into sections/imports/exports, Evidence subject, limits. path:line.""", RO)
add("RevRizinVerb", "revenger", f"""
# Target
Reverse-engineer REA's execute-rizin-command implementation in {PKG}/dist: provider selection (REA_RIZIN_COMMAND), `-N -q
-c` argv, timeout, output capture limits, how stdout becomes raw_result, whether any command is refused. path:line.""", RO)
add("RevHarmonyVerb", "revenger", f"""
# Target
Reverse-engineer project-harmony-application-graph in {PKG}/dist: inputs, packaging-model hint logic (module.json vs
config.json), component kinds, what a minimal synthetic HAP must contain to project. path:line.""", RO)
add("RevGhidraFirstFailure", "revenger", f"""
# Target
From Base-src.zip ({GH}/Ghidra/Features/Base/lib/Base-src.zip): reconstruct the Go RTTI analysis order (discovery,
gap scan, markup walk) and which exception ends GolangSymbolAnalyzer's pass vs which are caught and continue; what log line
the first fatal read emits. Compare with {W18}/tools/swiss-misread.py's order (docstring anchors). path:line.""", RO)

# ================= connectors (m_grok) =================
add("ConnSiblingWasm", "connector", """
# Target
Sibling-overlap scan: does any sibling lane (/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md, corpus/SOURCES.md,
corpus/knowledge) own or hold WASM analysis, WABT or wasm interface comparison? Report contested scope with path:line.""", RO)
add("ConnSiblingRizin", "connector", """
# Target
Sibling-overlap scan for rizin / radare2 / objdump-architecture knowledge across sibling lanes (PROVINCE, SOURCES,
knowledge). Report overlaps and whether kaidoku's REA-verb framing stays inside its province.""", RO)
add("ConnSiblingHarmony", "connector", """
# Target
Sibling-overlap scan for HarmonyOS / HAP / mobile packaging across sibling lanes (mado? tabi? others). Report owners and
contested scope with path:line.""", RO)
add("ConnJjSelftests", "connector", """
# Target
Across sibling lanes, find jj-related selftests/tools and lessons (grep -ril 'jj ' in */.ufo/waves/*/tools and
corpus/lessons). Which covered cases could inform kaidoku's jj-red-before gaps? path:line.""", RO)
add("ConnTimestampDefects", "connector", """
# Target
Fleet sweep for future-dated evidence timestamp defects and how lanes fixed them (grep -ril 'future-dated\\|future dated'
in */corpus/lessons and /home/vgpnk/Projects/shokunin/.ufo/reports). Summarize mechanisms with pointers.""", RO)
add("ConnExecGuards", "connector", """
# Target
Fleet sweep for no-execution / carrier-execution enforcement in sibling lanes (grep -ril 'noexec\\|chmod a-x\\|carrier
execution\\|do not execute' in */corpus and */.ufo/waves/*/contract*.md). Patterns and gaps, with pointers.""", RO)
add("ConnSandboxPatterns", "connector", """
# Target
Fleet sweep for OS sandboxing of lane checkers (unshare, systemd-run, bwrap, firejail) in sibling lanes' tools and lessons.
Which approach worked on this host, with pointers.""", RO)
add("ConnSourcesOverlap", "connector", """
# Target
Sibling SOURCES.md rows for WABT, WebAssembly spec, rizin, GNU objdump, HarmonyOS docs, go.dev go1.24.6 (grep across
*/corpus/SOURCES.md). List row ids/lanes to avoid duplicate rows and to cross-cite.""", RO)

# ================= scribes (m_haiku) — sources and drafts =================
add("SourceWabtRelease", "scribe", f"""
# Target
Open the WABT 1.0.42 release: https://github.com/WebAssembly/wabt/releases/tag/1.0.42 (and `gh release view 1.0.42 -R
WebAssembly/wabt --json assets`), asset wabt-1.0.42-linux-x64.tar.gz and its .sha256 asset (L1 install hash
84895407a6bbb80e918f33b16b2fb2206021c150b6bc9ff6f761263a745ab131, 4761911 bytes). Scope: identity of the WABT binaries
REA's inspect-wasm-artifact runs.""", SRC)
add("SourceRizinDocs", "scribe", """
# Target
Open rizin's official documentation for the info commands REA's execute-rizin-command will run (`iI`, `iS`, `ie`) and the
`-N`/`-q`/`-c` CLI flags: rizin book (https://book.rizin.re/) and/or `rizin -h` / the v0.8.2 release page
(https://github.com/rizinorg/rizin/releases/tag/v0.8.2). Scope: meaning of those commands/flags in rizin 0.8.x.""", SRC)
add("SourceHarmonyDocs", "scribe", """
# Target
Open the official HarmonyOS/OpenHarmony documentation for the Stage-model `module.json5`/`module.json` and FA-model
`config.json` package layout (e.g. https://gitee.com/openharmony/docs or developer.huawei.com app-configuration pages).
Scope: which files a HAP must contain and how Stage vs FA is distinguished.""", SRC)
add("SourceWasmSpec", "scribe", """
# Target
Open the WebAssembly Core Specification binary format (https://webassembly.github.io/spec/core/binary/modules.html,
sections/imports/exports). Scope: what an import/export section entry is, for interpreting inspect-wasm-artifact and
compare-wasm-interfaces results.""", SRC)
add("SourceGo1246", "scribe", f"""
# Target
Open https://go.dev/dl/?mode=json&include=all (curl to /tmp, sha256 the document) and locate the go1.24.6
linux-amd64 archive entry: filename, sha256 (expected bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712 per
{L19}:71-73), size. Scope: carrier provenance of the round-20 C3 go1.24.6 toolchain ELFs only.""", SRC)
add("SourceObjdumpDocs", "scribe", """
# Target
Open the GNU binutils objdump manual (https://sourceware.org/binutils/docs/binutils/objdump.html) for `-i`/`--info`
(list supported object formats and architectures). Scope: what list-objdump-architectures reflects.""", SRC)
add("DraftLessonMistakes", "scribe", f"""
# Target
Draft the `## Mistakes` rows for {LANE}/corpus/lessons/round-20.md (class · evidence · captured-by · fix) mining round-19
D1 (nested-repo residue, {SPOT}:29,33-35,180-181) and D2 (future-dated timestamp, {SPOT}:100-103,182-183), using classes from
/home/vgpnk/Projects/shokunin/CORPUS.md:171-178; state for each what red-before must be shown.""", DR)
add("DraftQualityRows", "scribe", f"""
# Target
Draft QUALITY #23 and #24 rows for {LANE}/corpus/QUALITY.md (format: `| # | criterion | why (lesson) | supersedes |`):
#23 evidence timestamps at or before the shipping commit, checked by evidence-timestamps.py; #24 a no-execution contract is
admitted only with a guard record (arm/check/disarm) and declared bypass limits. Ground each in {SPOT} lines.""", DR)
add("DraftSkillRows", "scribe", f"""
# Target
Draft SKILL.md registry rows (fields: name, gate|probe, entry command, verdict map, self-test command and spelling,
pinned-value path, write scope, owner) for the round-20 tools named in {CON} §Interfaces, matching the existing row style
in {LANE}/SKILL.md (grep -n 'routed-defects\\|head-rev-lint' SKILL.md).""", DR)
add("DraftCoverageRows", "scribe", f"""
# Target
Draft corpus/README.md coverage-map and Knowledge rows and PROVINCE.md Core rows for the five C2 verbs (placeholders
`<ev_id>`, `<sha256>` for values the L1 fills from retained runs), matching {LANE}/corpus/README.md:11-68,72-154 style.""", DR)

# ================= critics (m_swe) =================
add("CriticC1", "critic", f"""
# Target
Falsify C1 before it lands: for each of the 11 items in {W20}/claims.json, how could it be "closed" while the outside
defect remains (token closure, fixture-only fix, rekey that hides)? Name the strongest attack and the evidence that would
defeat it.""", RO)
add("CriticC2", "critic", f"""
# Target
Falsify C2: could the five target verbs be counted without real coverage (mentions in lessons, refusal-only runs,
synthetic HAP that proves nothing)? Which of the five would you reject and why? What counts as uncovered ground?""", RO)
add("CriticC3", "critic", f"""
# Target
Falsify C3: first-failure forecasting on go1.24.6 — can the forecast be trivially right (all silent)? Is go1.24.6 toolchain
held-out given round-18 synthetics built with it? What prior-exposure would invalidate it? Propose a non-trivial
discrimination requirement.""", RO)
add("CriticNoHarm", "critic", f"""
# Target
Which existing axis or file could round 20 harm: in-place edits to r17/r18/r19 tools (receipt-validate, head-rev-lint,
wave-outcomes, jj-red-before, citation-drift, custody-pair, census), README coordinates, SOURCES cells, QUALITY rows?
List the control that must prove no harm for each.""", RO)
add("CriticFrontierStep", "critic", f"""
# Target
Attack the frontier step plan (claims.json frontier_step; /home/vgpnk/Projects/shokunin/CORPUS.md SOURCES contract v1):
what makes a SOURCES row non-conformant, what makes the sourced claim hollow, what makes the mined mistake's fix
unfalsifiable.""", RO)
add("CriticGuardSufficiency", "critic", f"""
# Target
Is clearing exec bits (contract D3; {W20}/evidence/carrier-guard/manual-arm.json) enforcement or theatre? Bypasses, false
greens of `check`, and what wording the knowledge/QUALITY text must use so it does not overclaim.""", RO)
add("CriticCensusRekey", "critic", f"""
# Target
Attack any re-key of {LANE}/.ufo/gates/c1-census-v10.py that turns FAIL into PASS for SCORECARD 2380-2382 / SKILL
511-519: under what classification would that be suppression; what must the reviewer see to accept it?""", RO)
add("CriticTrends", "critic", f"""
# Target
Given the plan in {W20}/claims.json, under LEARNING.md (/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md:26-38)
what evidence would make expansion `improved` legitimate this round, and what would make it a trade with quality?""", RO)

# ================= sentinels (m_luna) =================
add("SentinelRevexec", "sentinel", f"""
# Target
Security design review for {W20}/tools/revexec.py (interface D6b in {CON}): unprivileged user+mount+net namespaces on this
host; escape paths (/proc, fds, symlinks in extracted blobs, environment); what a selftest must prove. Probe only with
harmless commands in mkdtemp.""", RO)
add("SentinelCarrierGuard", "sentinel", f"""
# Target
Security/safety review of carrier-guard (D3 in {CON}): risks of chmod on {GO6} (other users of the install, restore on
crash, TOCTOU between check and analyze), and whether the arm/check/disarm records are forgeable. Read-only.""", RO)

# ================= simplifiers (m_flash) =================
add("SimplifyC1Tools", "simplifier", f"""
# Target
YAGNI review of the C1 tool plan in {CON} §Interfaces: which tools could be merged or dropped (e.g. final-census into
verify.py) without weakening any substance check?""", RO)
add("SimplifyC3Pipeline", "simplifier", f"""
# Target
YAGNI review of the C3 pipeline (swiss-misread-v2, first-failure-extract, compare-first-failure, retro-v2, run-carriers,
measure): minimum set that still freezes, binds and compares; what can reuse round-19 code unchanged.""", RO)

spec = {
    "wave": "kaidoku-r20-w1",
    "axes": ["calibration", "coverage", "depth"],
    "reportDir": ".ufo/waves/round-20/w1",
    "maxLanes": 100,
    "context": (
        "# Goal\nKaidoku round 20 (hyaku phase 2), axes calibration + coverage + depth. Claims: "
        f"{W20}/claims.json. Shared contract (read it first): {CON}. L1 (KaidokuR20) holds the canonical planner "
        "seat and is the single integration owner; you are an author-side advisory seat, never an outside reviewer. "
        "REA CLI: `npx -y rea-agents@6.5.0 <command>` (the OMP rea MCP entry is operator-owned; never use "
        "xd://mcp__rea_* devices; never edit ~/.omp/agent/mcp.json).\n"
        "# Contract\nLeaf: never delegate (executors may spawn at most one read-only labrat for a falsifiable "
        "hypothesis). Never execute any Go toolchain binary; never run REA analyze/search/decompile or Ghidra "
        "analyzeHeadless on /home/vgpnk/.local/opt/go-1.24.6 files (the L1 runs them after freezing predictions). "
        "Writers: work only in your own `/tmp/kr20-<SeatName>` clone at the baseline and deliver a patch under "
        f"{W20}/w1/patches/ (contract `Writers`); read-only seats write only their report. Selftests/fixtures/scratch only "
        "under tempfile.mkdtemp() in the system temp dir, never inside the lane or any Git worktree. Never run `jj` or "
        "any git write in the lane; never write the lane working tree beyond your report/patch; never write the fleet "
        "repo /home/vgpnk/Projects/shokunin outside the lane dir, sibling lanes, .ufo/state, MANIFEST.json or client "
        f"configs. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Keep reports "
        "concise; cite exact path:line anchors; label observation vs inference; never fabricate output; any timestamp "
        "you write comes from the clock at write time. Final message at most 8 lines. Message only KaidokuR20 if "
        "blocked; never the orchestrator, never agent://all.\n"
        "# Host safety\nYou and every seat may install or upgrade tools that help the task — read "
        "/home/vgpnk/.omp/agent/RULES.md first (official channels; record tool/version/channel/reason in your "
        "report). pacman guard: ALL pacman transactions are PAUSED host-wide (read-only `pacman -Q*` queries are "
        "fine); install via `uv tool`/`npx`/an official binary in ~/.local/bin instead, or report the need. When the "
        "pause lifts: before any `pacman -S` run `pacman -Sp --print-format '%n %v' <pkgs>` and proceed only if every "
        "listed package is not installed; never -Sy/-Syu/-U/-R, downgrade, or restart a host service. Never "
        "open/copy/query ~/.omp/agent/agent.db* or credential/auth files; never launch omp CLI processes; never modify "
        "client routing or host services. Prefer no installs."),
    "items": items,
}
with open(os.path.join(HERE, "wave1-spec.json"), "w") as f:
    json.dump(spec, f, indent=1, ensure_ascii=False)
print(len(items), dict(Counter(i["role"] for i in items)))
