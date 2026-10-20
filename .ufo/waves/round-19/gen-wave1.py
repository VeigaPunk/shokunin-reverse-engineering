#!/usr/bin/env python3
"""Generate the round-19 wave-1 spec (L1-authored). Writes wave1-spec.json next to this file."""
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
W17 = LANE + "/.ufo/waves/round-17"
W18 = LANE + "/.ufo/waves/round-18"
W19 = LANE + "/.ufo/waves/round-19"
B = "8a8da7e19375aadc66c6bcbff0bbcbb596048fb0"
B18 = "9011581d84527ba34c675f9cf912e54d2e72d470"
A18 = "a245bb00c581ae3423a10a055c77d4bc873918df"
SPOT = LANE + "/corpus/lessons/round-18-verifier-spotcheck.md"
L18 = LANE + "/corpus/lessons/round-18.md"
FREP = "/home/vgpnk/Projects/shokunin/.ufo/reports/round-18/kaidoku.md"
GO = "/home/vgpnk/.local/opt/go-1.25.0"
GH = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC"
PRE = W19 + "/evidence/prescan"
CON = W19 + "/contract.md"
with open(os.path.expanduser("~/.agents/skills/godspeed/directive.md")) as f:
    DIRECTIVE = f.read()

RO = ("# Acceptance\nRead-only: write only your report. Cite exact path:line anchors, paste each command with its "
      "exit code, label observation vs inference, never fabricate.")
EX = (f"# Acceptance\nWork in your own clone per {CON} section `Writers`; deliver one patch at "
      f"{W19}/w1/patches/<YourSeatName>.patch plus your report. Run your tool's --selftest once in the clone and "
      "paste the exact last line and exit code; paste every other command you ran with its exit. Cite path:line.")
DR = ("# Acceptance\nRead-only except your report: put the drafted text verbatim in your report under a heading "
      "`## Draft`, every factual sentence carrying its path:line or command source. The L1 integrates; never edit "
      "lane files.")

items = []


def add(name, role, body, acc):
    items.append({"name": name, "role": role,
                  "prompt": "/skill:godspeed\n" + DIRECTIVE + "\n" + body.strip() + "\n" + acc})


# ---------------- executors (code) ----------------
add("RoutedR18Tool", "executor", f"""
# Target
Create {W19}/tools/routed-r18.py — the C1 counting command: `python3 -I -B routed-r18.py --root LANE --rev REV
[--strict] [--selftest]`. The seven defects are {SPOT}:193-199. A defect is OPEN unless BOTH checks pass at REV
(Git objects only, `git show REV:path`, never the working tree):
(a) named correction: `SCORECARD.md` and `corpus/lessons/round-19.md` each contain a line starting `- R18-<ID>:`;
(b) substance (run tools extracted from REV into mkdtemp; build fixtures, never trust tokens):
 MIDMAP-LISTSTEP — take one round-18 receipt at REV (`.ufo/waves/round-18/runs/<label>/receipt.json`), convert
 `steps` to list shape with `pin_checks` only on a non-`analyze` step; the REV round-17 `receipt-validate.py
 --require-mid-maps` must exit non-zero on it (open if it exits 0).
 VALIDATOR-DIGEST — in a mkdtemp clone at REV, commit a well-formed but wrong `validator_sha256` into
 `.ufo/waves/round-18/evidence/validate16/summary.json`; REV's round-18 `routed-defects.py` must report R17-VALIDATE16
 open; AND `.ufo/waves/round-19/evidence/validate16-remap/digests.json` exists with one sha256 per remapped receipt
 copy, each copy retained beside it and re-hashing equal.
 STRICT-BASELINE — `.ufo/waves/round-19/evidence/strict-baseline/` holds receipts for routed-defects `--strict` at
 `{B18}` (exit 1) with argv, tool blob sha256, stdout/stderr files whose sha256 match the receipt.
 HEAD-ALIASES — REV's citation-drift-probe.py exits 2 for each of `--rev @`, `HEAD~0`, `HEAD^{{commit}}`,
 `HEAD@{{0}}`, `main~0^{{}}`-style aliases of HEAD you can derive (list the set; run in a mkdtemp clone); AND REV's
 round-18 `head-rev-lint.py` reports the two nested compare-only reads (round-17 `verify.py`, `revpin.py`) in a
 separate non-live class.
 DEADSEAT-RECORD — `.ufo/waves/round-19/evidence/r18-dead-seats.json` lists exactly the round-18 wave seats with no
 report at `{A18}` (recompute: registration names vs `w1/`,`w2/` report files) with non-empty `cause` and `source`.
 REGISTRY-PINNED — `SKILL.md` registry rows `pins` and `go-buildinfo-probe`: `Pinned values:` cell names a path that
 exists at REV or the literal `probe; no persisted baseline`.
 INSTALL-RECORD — `corpus/lessons/round-19.md` names go1.24.6 and go1.25.0 with full 64-hex archive sha256 (values
 from {FREP} near line 90 / go.dev JSON), channel and reason.
Output JSON {{rev, open_count, named_open, substance_open, defects:[{{id, named, substance, why}}]}}; `--strict` exit 1
if open_count>0. Selftest with fixtures that keep token-only closures OPEN. Then run at `--rev {B}` (expect 7 open)
and paste.""", EX)
add("MidmapListStep", "executor", f"""
# Target
Fix R18-MIDMAP-LISTSTEP ({SPOT}:193): in {W17}/tools/receipt-validate.py (~:570-580) the list-shaped `steps` branch
of `--require-mid-maps` passes if ANY step has `pin_checks`; require the `analyze` step's pin checks exactly as the
object branch does. Add a red selftest case (list-shaped receipt, pin_checks only on a non-analyze step → reject).
Then re-run the patched validator `--require-mid-maps` on all 15 round-18 receipts {W18}/runs/*/receipt.json (in
your clone) and paste exits (must stay 0; they are object-shaped).""", EX)
add("ValidatorDigestGuard", "executor", f"""
# Target
Fix the first half of R18-VALIDATOR-DIGEST ({SPOT}:194): {W18}/tools/routed-defects.py check
`validator-sha256-pinned` verifies only the format. Make it compare `validator_sha256` against the sha256 of
`git show {B18}:.ufo/waves/round-17/tools/receipt-validate.py` (the validator the summary names). Add a red selftest
case (well-formed wrong digest → R17-VALIDATE16 open). Run `--selftest`, then `--rev {B} --strict` in your clone
and paste (expected still 0 open: the committed digest is correct, 618448829ba6…126f).""", EX)
add("Validate16RemapDigests", "executor", f"""
# Target
Second half of R18-VALIDATOR-DIGEST: the r18 remapped receipt copies (see {W18}/evidence/validate16/summary.json and
{L18}:55) were written to /tmp and not retained. Re-create them exactly per the recorded remap, retain each copy
under {W19}/evidence/validate16-remap/copies/<label>.receipt.json, write {W19}/evidence/validate16-remap/digests.json
{{source_rev:"da64646adcb19c1ede7537b799b8c7d283fe43da", validator_rev:"{B18}", validator_sha256, remap,
copies:[{{label, sha256, validator_exit, stdout_sha256}}]}} and re-run the {B18} validator on each copy (paste exits;
report honestly if any differs from the r18 summary).""", EX)
add("StrictBaselineReceipts", "executor", f"""
# Target
R18-STRICT-BASELINE ({SPOT}:195): retain the strict baseline runs. In a mkdtemp clone run the round-18
routed-defects.py as committed at `{A18}` (`git show {A18}:.ufo/waves/round-18/tools/routed-defects.py`) with
`--root <clone> --rev {B18} --strict` and with `--rev 454dee6923750698cc36041236db13b52c6fcade --strict`. Write
{W19}/evidence/strict-baseline/<rev12>.receipt.json {{argv, tool_rev, tool_sha256, rev, exit, stdout_sha256,
stderr_sha256, started_utc, ended_utc}} plus the stdout/stderr files. Expected exit 1 and 0; report what you get.""", EX)
add("CitationDriftAliases", "executor", f"""
# Target
R18-HEAD-ALIASES part 1 ({SPOT}:196): {LANE}/.ufo/gates/citation-drift/citation-drift-probe.py (~:329) refuses only
the literal `--rev HEAD`. Refuse (exit 2, named cause) every rev expression that resolves through HEAD or the
working-copy: `@`, `@~N`, `HEAD` with any suffix (`~`, `^`, `@{{…}}`, `^{{commit}}`), `HEAD@{{…}}`, `ORIG_HEAD`,
`FETCH_HEAD`; accept full hex, `refs/heads/main`, `main`, and their ancestors. Keep every existing selftest exit; add
red/green cases in a mkdtemp git repo. Run `--selftest` and the registered strict argv from {LANE}/SKILL.md (grep
`citation-drift`) with `--rev {B}`; exit must equal the pre-change exit.""", EX)
add("HeadRevLintNested", "executor", f"""
# Target
R18-HEAD-ALIASES part 2: {W18}/tools/head-rev-lint.py cannot see compare-only HEAD reads behind nested wrappers
(`{W17}/verify.py:83`, `{W18}/tools/revpin.py:108`; {SPOT}:112-113). Add a `nested` class that reports such sites
(keep the `live` rule and count unchanged), with a selftest fixture. Run `--rev {B}` and paste live/nested counts.""", EX)
add("RevpinWording", "executor", f"""
# Target
Carried item ({L18}:92): {W18}/tools/revpin.py:6 says HEAD sits on the working-copy commit; under jj colocation git
HEAD is the working-copy parent (`@-`). Fix the docstring/comment wording only (cite S036,
{LANE}/corpus/SOURCES.md), and any other line in revpin.py repeating the error. Run `--selftest` if present.""", EX)
add("CustodyRepoRoot", "executor", f"""
# Target
Carried item ({L18}:90): {LANE}/.ufo/gates/custody-pair/custody-pair.py records `repo-root` as the `--repo` argument,
not the repository top level. Record `git rev-parse --show-toplevel` (keep the argument as a separate field if the
receipt format allows; bump receipt-version only if required, say why). Add a red selftest case (subdirectory
argument).""", EX)
add("JjRedBeforeSafety", "executor", f"""
# Target
Carried item ({L18}:90): {W18}/tools/jj-red-before.py — scrub the environment of GIT_*/JJ_* variables for every
git/jj subprocess (pass an explicit env), and guard the pointer-table paths so the probe refuses (exit 2) any path
outside its mkdtemp clone. Red selftest cases for both. Run `--selftest`; never run jj in {LANE}.""", EX)
add("ProvincePinsTool", "executor", f"""
# Target
Create {W19}/tools/province-pins.py — C2 counting command: `--root LANE --rev REV [--strict] [--selftest]`. Parse
PROVINCE.md at REV (Git object) for the stated per-client REA pins (Devin, OMP, Kimi: `rea-agents@X.Y.Z`) in the
surface summary, the `Drift-prone values` paragraph and the Core `REA MCP server` row; read the LIVE pins from
`~/.config/devin/mcp_config.json`, `~/.omp/agent/mcp.json`, `~/.kimi-code/config.toml` (print only the
`rea-agents@…` token, file sha256 and mtime; never print other config content). Output {{rev, stated:[{{client,
version, line}}], live:[…], mismatches:[…], mismatch_count}}; a client stated at two versions counts each stale
statement. `--strict` exit 1 on mismatch. Selftest with fixture configs via env overrides. Run at `--rev {B}`.""", EX)
add("GenPredictionsR19", "executor", f"""
# Target
Create {W19}/gen-predictions.py adapted from {W18}/gen-predictions.py: labels `t1250-<name>` for the 9 binaries in
{GO}/bin and {GO}/pkg/tool/linux_amd64 (link: record `status: excluded` with the emulator's unparseable cause),
running the UNCHANGED {W18}/tools/swiss-misread.py (`--carrier --golang-root {GH}/Ghidra/Features/Base/data/typeinfo/golang`);
write W19/predictions/<label>.prediction.json, carriers.tsv (label, path, kind, sha256), decision-rule.json (reuse
{W18}/predictions/decision-rule.json semantics; diagnostic set D = labels predicted to fail under H1), SHA256SUMS.
Run it in your clone and paste the per-label summary; compare to {PRE}/*.json. Do not freeze; the L1 does.""", EX)
add("RunCarriersR19", "executor", f"""
# Target
Create {W19}/run-carriers.sh as a thin parameterization of {W18}/run-carriers.sh for W19 (predictions dir
W19/predictions, runs W19/runs, sums from W19/predictions/carriers.tsv sha256 column, REA pinned
`rea-agents@6.5.0`), with a per-carrier timeout suited to 2–22 MB Go ELFs (cite {W18}/runs/*/receipt.json timings).
Keep `--selftest` (stubs only, never REA). Paste selftest result.""", EX)
add("MeasureR19", "executor", f"""
# Target
Create {W19}/measure.py `<REV>` printing JSON {{c1:{{open_count}} (via REV's tools/routed-r18.py), c2:{{mismatch_count,
c1_census_verdict, c1_census_exit}}, c3:{{labels_frozen, compare_jsons, compare_exit0, matched}}}} reading Git objects
at REV (extract tools to mkdtemp). Model on {W18}/measure.py; absent tools at REV read as `null` with a reason, never
crash. Selftest. Run at `{B}` and paste.""", EX)
add("VerifyR19", "executor", f"""
# Target
Create {W19}/verify.py modelled on {W18}/verify.py: one post-integration pass at a named source rev (branch tip,
never HEAD) running every round-19 tool selftest, the counting commands at {B} and at the source rev, sources
census, c1-census-v10, and recording argv/exit/stdout sha256 into W19/verification.json. Expected exits are a table
in the script. Do not run the full pass; prove the runner with a 2-command dry fixture.""", EX)
add("ReaCatalogRecompute", "executor", f"""
# Target
Recompute the REA catalog identities PROVINCE.md:8-24 states (CLI command count, MCP tool count, tools_sha256) for
`rea-agents@6.7.0` and `@6.5.0` using the method the lane recorded (find it: `git -C {LANE} grep -n tools_sha256`,
corpus/knowledge and earlier waves). Write {W19}/evidence/rea-catalog.json {{version, npx_cache_dir, cli_commands,
mcp_tools, tools_sha256, method_argv}} via your patch. Read-only REA calls only (`--version`, catalog/list).""", EX)
add("WaveOutcomesTool", "executor", f"""
# Target
Forward fix for R18-DEADSEAT-RECORD: create {W19}/tools/wave-outcomes.py `--registration <wave-registration.json>
--report-dir <dir> --causes <causes.json> --out <json> [--selftest]`: per seat {{name, role, report_present,
cause}}; exit 1 if any seat without a report lacks a non-empty cause. Model input shape on
{W18}/wave2-registration.json. Selftest; then run against round-18 wave 2 with an empty causes file and paste the
missing set (expected 4 at {A18}).""", EX)

# ---------------- scouts ----------------
add("DeadSeatHistoryR18", "scout", f"""
# Target
R18-DEADSEAT-RECORD ({SPOT}:197): find the terminal error text of each round-18 seat with no report:
GatePRODUCERREV, GateSUMSRUNLOG, ShonenLines, TruthREGISTRY (wave 2) and DecisionRuleApply (late), using agent ids
in {W18}/wave2-registration.json / wave2-assignments.json and `agent://<id>` / `history://<id>` reads. Paste the
verbatim final error line per seat (or `unrecoverable` with what you tried) as a JSON block for
r18-dead-seats.json.""", RO)
add("DeadSeatW1R18", "scout", f"""
# Target
Same for round-18 wave 1: SwissMisreadTool ended aborted after writing its report ({W18} SCORECARD.md:2462). Find
its terminal status text via its agent id in {W18}/wave1-registration.json. Also check whether any other w1 seat
lacks a report in {W18}/w1/. Paste a JSON block.""", RO)
add("LiveConfigPins", "scout", """
# Target
Read the REA pin token (only) in ~/.config/devin/mcp_config.json, ~/.omp/agent/mcp.json, ~/.kimi-code/config.toml
with line numbers, file mtime and sha256; also note OMP's `enabled` flag for the rea entry (operator-disabled this
phase). Never print other content.""", RO)
add("NpxCaches", "scout", """
# Target
List every ~/.npm/_npx/*/node_modules/rea-agents/package.json with version and cache dir; note which versions
PROVINCE.md:19-23 names and whether those dirs still exist.""", RO)
add("Doctor67", "scout", """
# Target
Run `npx -y rea-agents@6.7.0 doctor` and `npx -y rea-agents@6.5.0 doctor` (read-only; JSON if supported). Paste the
client-registration alignment lines (devin/omp/kimi) and the providerInspections ghidra line, with exits.""", RO)
add("GhidraJdkRecheck", "scout", f"""
# Target
Re-verify PROVINCE.md:25 values: {GH}/Ghidra/application.properties version/build lines, `java -version` first line,
~/.bashrc GHIDRA_INSTALL_DIR/JAVA_HOME lines (line numbers). Report current vs stated.""", RO)
add("ProviderKeysRecheck", "scout", """
# Target
Re-probe PROVINCE.md:26 provider-key inventory: which REA_* / HOPPER_* variable NAMES are exported in ~/.bashrc and
~/.profile (line numbers) and whether each referenced path exists. Never print values that are not filesystem
paths; never print secrets.""", RO)
add("FallbackReaders", "scout", """
# Target
Re-verify PROVINCE.md:62 host fallback readers: `command -v` for every tool listed there and the listed absent tools
(cabextract, rizin, ltrace, pacman-contrib via `pacman -Q`). Report changes.""", RO)
add("C1CensusDiag", "scout", f"""
# Target
`python3 -I -B {LANE}/.ufo/gates/c1-census-v10.py --root {LANE}` reads FAIL stale=4 undeclared=2 at {B}. Identify
each stale/undeclared locus (file:line, value), which scope-table row covers it, and the minimal content edit that
makes it current-ok WITHOUT widening any DATED range or re-classing rows (see the gate's refusal notes at its
header). Note whether its scope table is line-number keyed (edits shifting PROVINCE/SCORECARD lines would break it).""", RO)
add("NpmRegistrySource", "scout", """
# Target
Open https://registry.npmjs.org/rea-agents (and /rea-agents/6.7.0): record dist-tags.latest, 6.7.0 and 6.5.0
publish times, dist.integrity/shasum, repository/homepage URLs, access date, response sha256. Draft a SOURCES row
(contract: /home/vgpnk/Projects/shokunin/CORPUS.md §SOURCES.md) with a ≤25-word contiguous located quote.""", RO)
add("ReaReleaseNotes", "scout", """
# Target
Find official release notes/changelog for rea-agents 6.6.0/6.7.0 (npm README, repository CHANGELOG/releases). Open
it; summarize what changed vs 6.5.0 relevant to PROVINCE (tool counts, Ghidra provider, CLI verbs). Draft a SOURCES
row or a rejection row (`REJECTED: <reason>; flip: …`) with located quote.""", RO)
add("GoDlJsonSource", "scout", f"""
# Target
Open https://go.dev/dl/?mode=json&include=all; record go1.25.0 linux-amd64 archive filename + sha256 and go1.24.6;
compare to {FREP} (~line 90) and to {SPOT}:147. Draft a SOURCES row (C3 carrier provenance) with a located quote
(JSON: quote the object fields verbatim) and access date.""", RO)
add("ToolchainIdentity", "scout", f"""
# Target
Without executing any carrier: sha256 + size of the 9 binaries under {GO}/bin and {GO}/pkg/tool/linux_amd64; Go
build info per binary via the lane's static parser (find it: `git -C {LANE} grep -ln buildinf -- .ufo`), compare with
{PRE}/*.json; whether the files match the official tarball (if a local tarball or its sha256 record exists).""", RO)
add("CarrierCensus125", "scout", f"""
# Target
Census other Go 1.25.x ELFs on the host outside {GO} (~/.local/bin, ~/go/bin, /usr/bin, /usr/lib, ~/.local/opt) by
static build-info read only; list path, sha256, go version, size. Purpose: alternative held-out carriers for C3.""", RO)
add("PriorRunTimes", "scout", f"""
# Target
From {W18}/runs/*/receipt.json and run-log.txt, tabulate carrier size vs Ghidra analyze wall time and peak memory if
recorded; estimate wall time for the 8 C3 carriers ({PRE}/*.json sizes, compile 21.5 MB) and recommend timeouts.""", RO)
add("SkillStalePins", "scout", f"""
# Target
Sweep {LANE}/SKILL.md, corpus/README.md, PROVINCE.md and corpus/QUALITY.md for every `rea-agents@` / REA version /
tool-count statement; classify each as current, historical-labelled, or stale-unlabelled at {B} against the live
pins (6.7.0 for all three clients). Paste a table.""", RO)
add("R12Queue", "scout", f"""
# Target
Carried r12 items ({L18}:88): (1) `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` has no S### row
and no custody-leg disclosure — determine what sources it actually uses and whether an existing row covers them;
(2) the r12 operability axis "add or withdraw" decision — find the origin text (grep SCORECARD/LOG/lessons r12-r13)
and what a decision record must contain.""", RO)
add("ReadmeFrontier", "scout", f"""
# Target
{LANE}/corpus/README.md coverage map (:11), Knowledge index (:70) and Frontier (:170): which rows the round-19
C3 entry (Go 1.25.0 toolchain held-out replay) and C2 (REA pin freshness) touch; propose exact new index row text.""", RO)
add("SpotcheckAnchors", "scout", f"""
# Target
Verify the anchors W19/claims.json uses: {SPOT}:191-199 (seven routed), :201-206 (carried), {L18}:86-92 (Open). Then
for each routed defect, quote the exact defect sentence and the exact file:line it names at {B}, confirming it is
still present (not already fixed).""", RO)
add("R18ClosureResiduals", "scout", f"""
# Target
{SPOT}:97-101 lists residuals (validator digest format-only, remap copies undigested, pins/go-buildinfo cells, r17
SUMS edited in place). Map each residual to a routed defect or state it is unrouted; for unrouted ones propose
whether the round should address it (with evidence).""", RO)
add("MisrootSweepW1", "scout", """
# Target
Run `git -C /home/vgpnk/Projects/shokunin status --porcelain` and list untracked files whose content names kaidoku
or round-19 (head -5 each). Do not move or delete anything; paste the list (empty is a result).""", RO)
add("SourcesRowAudit", "scout", f"""
# Target
Census {LANE}/corpus/SOURCES.md at {B}: run the frozen CORPUS.md §SOURCES census commands (from the lane root) and
paste outputs; list rows whose recheck date is due by 2026-10-20 and rows citing REA versions.""", RO)
add("GhidraGoDetect", "scout", f"""
# Target
In {GH}/Ghidra/Features/Base/lib/Base-src.zip (unzip -p), find how Ghidra 12.1.4 detects a Go binary and its version
(GoRttiMapper / GoBuildInfo / version fallback). Predict what Ghidra does for a Go ELF with no build info (the
`link` carrier, {PRE}/kr19-sm-link.json). Cite member:line.""", RO)

# ---------------- revengers ----------------
add("VetMisreadTrace", "revenger", f"""
# Target
Byte-trace the emulator's H1 invalid_index prediction for {GO}/pkg/tool/linux_amd64/vet ({PRE}/kr19-sm-vet.json;
run `{W18}/tools/swiss-misread.py --carrier … --golang-root {GH}/Ghidra/Features/Base/data/typeinfo/golang --debug`):
which map type, its slot size, the misread name/pkgPath offsets and the predicted index. Read-only; never run REA.""", RO)
add("H0H1Semantics", "revenger", f"""
# Target
In {PRE}/kr19-sm-vet.json `predicted_failure_h0` is false while `predicted_failure_kind_h0` is `invalid_index`.
Read {W18}/tools/swiss-misread.py and {W18}/predictions/decision-rule.json: define H0/H1, explain the field
semantics, and say whether this is a bug that would change a frozen prediction.""", RO)
add("LinkNoBuildinfo", "revenger", f"""
# Target
Why does {GO}/pkg/tool/linux_amd64/link have no Go build info (emulator: unparseable)? Static read only (section
headers, `.go.buildinfo`, magic `\\xff Go buildinf:`). Is it still a Go ELF with moduledata/typelinks the emulator
could use given `--go-version go1.25.0`? Recommend include (with forced version) or exclude.""", RO)
add("AliasRevSemantics", "revenger", f"""
# Target
Enumerate git revision syntaxes that resolve through HEAD or the jj working copy (gitrevisions: `@`, `HEAD~0`,
`HEAD^{{commit}}`, `HEAD@{{0}}`, `@{{-1}}`, `HEAD^0`, `:/text`, `HEAD:path`), and test each against
{LANE}/.ufo/gates/citation-drift/citation-drift-probe.py's --rev handling at {B} (read code; run only in a mkdtemp
clone). Table: form, resolves-to, accepted-at-B.""", RO)

# ---------------- connectors ----------------
add("SiblingOverlap", "connector", """
# Target
Scan sibling lanes (/home/vgpnk/Projects/shokunin/*-shokunin, read-only) for REA pin/version rows, Go 1.25 Ghidra
knowledge, and jj 0.45.1 doc rows; report overlap with kaidoku round-19 claims and who owns what.""", RO)
add("JjRowRouting", "connector", f"""
# Target
Carried adjacency item ({L18}:92): jj 0.45.1 git-compatibility doc registered by kaidoku S036, tameshi S061, tabi
S049; the routing report gives the jj fact to kumitate (/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjConnectorProvinces.md:181,189).
Draft kaidoku's disposition (keep S036 only for its own pin tools; report to kumitate) and decide if an L0 line is
warranted.""", DR)
add("QualityLineage", "connector", f"""
# Target
Should any R18 routed defect ({SPOT}:193-199) or the PROVINCE drift become a QUALITY criterion #22 (e.g. a dead seat
is recorded with its retained cause; a strict/red baseline is admitted only with a retained receipt)? Check
{LANE}/corpus/QUALITY.md #18-#21 for coverage first; draft at most one row with its lesson grounding, or argue none.""", DR)
add("SkillRowsFromRouted", "connector", f"""
# Target
Map each routed R18 fix and carried item to the {LANE}/SKILL.md registry rows (grep `Pinned values:`) that must
change or be added (routed-r18, province-pins, wave-outcomes). Paste the row anchors and needed edits.""", RO)
add("CoverageMapGo125", "connector", f"""
# Target
Connect the C3 replay to the lane's Go knowledge chain (r16-r18 entries in {LANE}/corpus/knowledge, README rows):
what exactly the go1.25.0 held-out result would add, which statements in the r18 entry it would upgrade, and what
must stay labelled INFERENCE.""", RO)
add("ProvinceSkillConsistency", "connector", f"""
# Target
Cross-check PROVINCE.md, SKILL.md and README statements about REA versions, Ghidra, JDK and providers for mutual
contradictions at {B}; list each pair with anchors.""", RO)
add("CarryDispositions", "connector", f"""
# Target
Build the full disposition table for {L18}:86-92 Open items and {SPOT}:201-206 carried items: item → this round's
seat/fix or explicit carry with reason.""", DR)
add("MeasureReuse", "connector", f"""
# Target
Which of {W18}/measure.py, controls.py, verify.py can round 19 call with parameters vs copy? Name the controls
needed for no-harm (QUALITY rows identical, LOG/SCORECARD prefix-exact, scores) and their argv.""", RO)

# ---------------- scribes ----------------
add("LessonSkeleton", "scribe", f"""
# Target
Draft corpus/lessons/round-19.md skeleton modelled on {L18}: header, Claims (from W19/claims.json), Gate (candidate
table, opened sources, registry changes, outside spot-check pending), `## R18 routed defects — named corrections`
with one `- R18-<ID>:` line per defect, Mistakes table header, Open.""", DR)
add("MistakesDraft", "scribe", f"""
# Target
Draft `## Mistakes` rows (class · evidence · captured-by · fix) for: R18-DEADSEAT-RECORD (SCORECARD.md:2462 "1 dead"
vs erratum 3), R18-STRICT-BASELINE (unretained red run), R18-MIDMAP-LISTSTEP, R18-VALIDATOR-DIGEST, PROVINCE pin
drift left for a round. Classes from /home/vgpnk/Projects/shokunin/CORPUS.md (kaika rules). Fix cells name the
red-before command.""", DR)
add("InstallRecordDraft", "scribe", f"""
# Target
R18-INSTALL-RECORD ({SPOT}:199): draft the install record for corpus/lessons/round-19.md from {FREP} (~:90) and
{SPOT}:147: tool, version, channel, full sha256, install path, reason, date; named as a correction of round 18.""", DR)
add("ScorecardDeadSeatDraft", "scribe", f"""
# Target
Draft the append-only SCORECARD correction line `- R18-DEADSEAT-RECORD: …` for {LANE}/SCORECARD.md:2462 using the
fleet report erratum ({FREP}, tail) and the r18 wave files (count reports in {W18}/w2 vs wave2-registration.json).""", DR)
add("ProvinceRewriteDraft", "scribe", f"""
# Target
Draft replacement text for {LANE}/PROVINCE.md:8-26 and :44-45 that states the current pins (Devin/OMP/Kimi
rea-agents@6.7.0 per live configs; OMP rea entry operator-disabled this phase) and keeps historical values labelled
historical. Ground each value in a command you run (read-only).""", DR)
add("SkillRegistryDraft", "scribe", f"""
# Target
Draft SKILL.md registry row text for `pins` and `go-buildinfo-probe` (R18-REGISTRY-PINNED, {SPOT}:198) and new rows
`routed-r18`, `province-pins`, `wave-outcomes` in the existing row format (grep `Pinned values:` in {LANE}/SKILL.md).""", DR)
add("KnowledgeEntrySkeleton", "scribe", f"""
# Target
Draft the skeleton of corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md modelled on
{LANE}/corpus/knowledge/2026-10-20-r18-swiss-map-replay.md: provenance trio, carriers table (from {PRE}), frozen
predictions, method, placeholders for observations (marked TO-FILL), limits.""", DR)
add("SourcesRowsDraft", "scribe", """
# Target
Open https://registry.npmjs.org/rea-agents/6.7.0 and https://go.dev/dl/?mode=json&include=all yourself; draft two
SOURCES rows in contract format (/home/vgpnk/Projects/shokunin/CORPUS.md §SOURCES.md) with ids S037/S038, plus the
Gate quote table lines (URL, access date, ≤25-word contiguous quote with location).""", DR)
add("LogEntryDraft", "scribe", f"""
# Target
Draft the LOG.md round-19 entry skeleton modelled on the round-18 entry (grep `round-18` in {LANE}/LOG.md): motivating
evidence for C1-C3 with pointers.""", DR)
add("R12Disclosure", "scribe", f"""
# Target
Draft the correction/disclosure note for corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md ({L18}:88):
which S### rows ground it (open SOURCES.md), and its custody-leg disclosure, as an append-only addendum.""", DR)

# ---------------- critics / sentinels ----------------
add("CriticC1", "critic", f"""
# Target
Attack C1 (W19/claims.json): can routed-r18.py be closed by tokens or fabrication (r18 Mistake 6, {L18}:70)? Design
concrete fabrication attacks per defect for wave 2.""", RO)
add("CriticC2", "critic", f"""
# Target
Attack C2: is the pin-mismatch count trivially movable by deleting statements; is c1-census PASS reachable only by
laundering (see the gate header refusals); is this freshness or just edits? Propose the falsification test.""", RO)
add("CriticC3", "critic", f"""
# Target
Attack C3: are the go1.25.0 toolchain binaries truly held-out (emulator calibration set: {W18}/predictions)?
Prescan before freeze ({PRE}) — does it bias? Is one diagnostic carrier (vet) enough; what result refutes?""", RO)
add("CriticSeparability", "critic", """
# Target
Attack separability and no-harm across C1-C3: shared files (SKILL.md, SCORECARD), shared tools; which axis could be
harmed (coverage via README rows, depth via entry edits). Name the controls that must run.""", RO)
add("CriticSourced", "critic", """
# Target
Attack the sourced-claim plan: do npm registry metadata and go.dev JSON actually ground C2/C3, or are they
decoration? What would a sourced claim need to cite to be non-vacuous?""", RO)
add("CriticCarried", "critic", f"""
# Target
Attack the carried-item fixes (revpin wording, custody repo-root, jj-red-before env/path guard, r12 items): are they
real fixes shown able to fail, or wording? ({L18}:86-92)""", RO)
add("SentinelSandbox", "sentinel", f"""
# Target
Security review: every round-19 tool that runs git/jj (routed-r18 substance checks, jj-red-before, citation-drift
fixtures) must write only in mkdtemp; check the patch delivery path ({CON}) cannot write outside LANE/W19.""", RO)
add("SentinelReaRun", "sentinel", f"""
# Target
REA run hygiene for the 8 go1.25.0 toolchain carriers: {W17}/tools/carrier-run.py env allowlist, session.json token
exclusion, private TMPDIR, no carrier execution; memory risk of compile (21.5 MB). Report leak paths.""", RO)

# ---------------- reviewers ----------------
add("ReviewReceiptValidateList", "reviewer", f"""
# Target
Review {W17}/tools/receipt-validate.py list vs object `steps` branches under `--require-mid-maps` (~:560-590):
state the exact fix and a red fixture.""", RO)
add("ReviewRoutedDefectsDigest", "reviewer", f"""
# Target
Review {W18}/tools/routed-defects.py `validator-sha256-pinned` and every other format-only check; list each with
line and whether a fabrication passes.""", RO)
add("ReviewValidate16Summary", "reviewer", f"""
# Target
Review {W18}/evidence/validate16/summary.json and its producer: exact remap rule, what a retained-copy digest binds,
and whether re-creating copies is deterministic.""", RO)
add("ReviewCitationDrift", "reviewer", f"""
# Target
Review {LANE}/.ufo/gates/citation-drift/citation-drift-probe.py --rev resolution and its selftest; list every
code path that reads HEAD.""", RO)
add("ReviewHeadRevLint", "reviewer", f"""
# Target
Review {W18}/tools/head-rev-lint.py rules; enumerate blind spots beyond the two nested reads (string concatenation,
subprocess lists built dynamically, shell scripts).""", RO)
add("ReviewSkillRegistry", "reviewer", f"""
# Target
Review {LANE}/SKILL.md registry rows: which `Pinned values:` cells name no path; which rows' write scope is stale.""", RO)
add("ReviewScorecardDeadSeat", "reviewer", f"""
# Target
Re-derive round-18 seat outcomes: registrations vs report files in {W18}/w1 and w2 at {A18} and at {B}; compare with
SCORECARD.md:2462 and the fleet erratum ({FREP} tail). Exact counts.""", RO)
add("ReviewProvinceStale", "reviewer", f"""
# Target
Enumerate every stale or unverifiable statement in {LANE}/PROVINCE.md (all 162 lines) at {B} with the live check
that shows it.""", RO)
add("ReviewC1CensusScope", "reviewer", f"""
# Target
Review {LANE}/.ufo/gates/c1-census-v10.py scope table: is it keyed by line ranges in PROVINCE/SCORECARD; would
round-19 appends (SCORECARD, LOG) or PROVINCE rewrites shift ranges into UNDECLARED? State the safe edit plan.""", RO)
add("ReviewDecisionRule", "reviewer", f"""
# Target
Review {W18}/predictions/decision-rule.json applicability to go1.25.0 held-out toolchain labels; propose the exact
round-19 rule text (confirmed/refuted/unresolved) before any run.""", RO)
add("ReviewCarrierRunEnv", "reviewer", f"""
# Target
Review {W17}/tools/carrier-run.py for large carriers: timeouts, memory, REA flags, and what a timeout records.""", RO)
add("ReviewRevpin", "reviewer", f"""
# Target
Review {W18}/tools/revpin.py semantics vs jj colocation (S036 in corpus/SOURCES.md); list every wrong statement.""", RO)
add("ReviewCustodyPair", "reviewer", f"""
# Target
Review {LANE}/.ufo/gates/custody-pair/custody-pair.py receipt fields; what repo-root should be and what changes
downstream if it changes.""", RO)
add("ReviewJjRedBefore", "reviewer", f"""
# Target
Review {W18}/tools/jj-red-before.py env and path handling; list every subprocess call and its env.""", RO)
add("ReviewMeasureR18", "reviewer", f"""
# Target
Review {W18}/measure.py and controls.py: functions round 19 must replicate; bugs.""", RO)
add("ReviewQualityRows", "reviewer", f"""
# Target
Compute the QUALITY.md data-row digest at {B} (`git show {B}:corpus/QUALITY.md | grep -E '^\\| *([1-9]|1[0-9]|2[0-1]) *\\|' | sha256sum`)
and LOG/SCORECARD byte sizes at {B} for prefix controls. Paste.""", RO)
add("ReviewR18Mistakes", "reviewer", f"""
# Target
Review {L18} Mistakes rows 1-10: which fixes were not shown able to fail; which remain open and should be mined this
round.""", RO)
add("ReviewR18FleetReport", "reviewer", f"""
# Target
Review {FREP} for statements contradicting committed lane files at {A18} (seat counts, installs, claims). List.""", RO)

# ---------------- simplifiers ----------------
add("SimplifyR19Tools", "simplifier", f"""
# Target
YAGNI review of the round-19 tool plan ({CON}, W19/claims.json): can routed-r18.py reuse {W18}/tools/routed-defects.py
structure; can province-pins be a c1-census mode; what to drop.""", RO)
add("SimplifyC3Run", "simplifier", f"""
# Target
YAGNI review of the C3 run plan: minimum carrier set that still discriminates (vet diagnostic + silent controls);
can {W19}/run-carriers.sh be the r18 script with env overrides only?""", RO)

spec = {
    "wave": "kaidoku-r19-w1",
    "axes": ["calibration", "freshness", "depth"],
    "reportDir": ".ufo/waves/round-19/w1",
    "maxLanes": 100,
    "context": (
        "# Goal\nKaidoku round 19 (hyaku phase 2), axes calibration + freshness + depth. Claims: "
        f"{W19}/claims.json. Shared contract (read it first): {CON}. L1 (KaidokuR19) holds the canonical planner "
        "seat and is the single integration owner; you are an author-side advisory seat, never an outside reviewer. "
        "REA CLI: `npx -y rea-agents@6.5.0 <command>` (the OMP rea MCP entry is disabled by operator authorization; "
        "never use xd://mcp__rea_* devices).\n"
        "# Contract\nLeaf: never delegate (executors may spawn at most one read-only labrat for a falsifiable "
        "hypothesis). Never run REA analyze/search/decompile or Ghidra analyzeHeadless on the C3 carriers (the L1 "
        "runs them after freezing predictions). Never execute carrier binaries. Writers: work only in your own "
        f"`/tmp/kr19-<SeatName>` clone at the baseline and deliver a patch under {W19}/w1/patches/ (contract "
        "`Writers`); read-only seats write only their report. Never run `jj` or any git write in the lane; never "
        "write the lane working tree beyond your report/patch; never write the fleet repo /home/vgpnk/Projects/shokunin "
        f"outside the lane dir, sibling lanes, .ufo/state, MANIFEST.json or client configs. Every `Report:` trailer "
        f"path is relative to {LANE} — write it at {LANE}/<that path>. Keep reports concise; cite exact path:line "
        "anchors; label observation vs inference; never fabricate output. Message only KaidokuR19 if blocked; never "
        "the orchestrator, never agent://all.\n"
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
