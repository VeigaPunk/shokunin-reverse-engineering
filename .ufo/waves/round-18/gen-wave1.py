#!/usr/bin/env python3
"""Generate the round-18 wave-1 spec (L1-authored). Writes wave1-spec.json next to this file."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
W17 = LANE + "/.ufo/waves/round-17"
W18 = LANE + "/.ufo/waves/round-18"
B = "9011581d84527ba34c675f9cf912e54d2e72d470"
GODATA = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang"
SRCZIP = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip"
CARR = "/home/vgpnk/.local/share/kaidoku-r18/carriers"
SPOT = LANE + "/corpus/lessons/round-17-verifier-spotcheck.md"
AUDIT = "/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md"
TRIAL = "/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjTrialKaidoku.md"
KENTRY = LANE + "/corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md"
with open(os.path.expanduser("~/.agents/skills/godspeed/directive.md")) as f:
    DIRECTIVE = f.read()

RO = ("# Acceptance\nRead-only: write only your report. Cite exact path:line anchors, paste each command "
      "with its exit code, label observation vs inference, never fabricate.")
EX = ("# Acceptance\nWrite only your assigned file(s) and your report. Run your tool's --selftest once and paste "
      "the exact last line and exit code; paste every other command you ran with its exit. Cite path:line.")
DR = ("# Acceptance\nRead-only except your report: put the drafted text verbatim in your report under a heading "
      "`## Draft`, with every factual sentence carrying its path:line or command source. The L1 integrates; never "
      "edit lane files.")

items = []


def add(name, role, body, acc):
    items.append({"name": name, "role": role,
                  "prompt": "/skill:godspeed\n" + DIRECTIVE + "\n" + body.strip() + "\n" + acc})


# ---------------- executors (code) ----------------
add("RoutedDefectsTool", "executor", f"""
# Target
Implement {W18}/tools/routed-defects.py exactly per {W18}/contract.md section `routed-defects.py` (C1 counting
command). The six routed defects are defined at {SPOT}:137-147. Then run it read-only at the baseline:
`python3 -I -B {W18}/tools/routed-defects.py --root {LANE} --rev {B}` and paste the JSON summary (expected
open_count 6; if any defect reads closed at the baseline, report which check and why — that is a design bug).""", EX)
add("HeadRevLintTool", "executor", f"""
# Target
Implement {W18}/tools/head-rev-lint.py per {W18}/contract.md section `head-rev-lint.py` (C2 counting command).
Ground truth for the baseline: {AUDIT} section 3.1 (32 live call sites; the three HEAD-keyed live sites are
round-17 verify.py:59, citation-drift-probe.py:477 default, custody-pair.py:327). Run it at `--rev {B}` and paste
sites + live_count; explain every live site beyond those three (true positive or lint bug) and every fixture
site classification.""", EX)
add("RevpinModule", "executor", f"""
# Target
Implement {W18}/tools/revpin.py per {W18}/contract.md section `revpin.py` (module + CLI). Then run
`python3 -I -B {W18}/tools/revpin.py --root {LANE}` once (read-only) and paste output/exit; explain the result
against `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state {LANE}`.""", EX)
add("CitationDriftBranchTip", "executor", f"""
# Target
Edit in place {LANE}/.ufo/gates/citation-drift/citation-drift-probe.py per {W18}/contract.md bullet
`citation-drift-probe.py` (jj risk R2 in {AUDIT} lines 164-166 and 244). Keep all existing selftest cases'
exits; add the two new red/green cases (fixtures under mkdtemp with a detached off-branch HEAD made by plain
git in the fixture repo). Run `--selftest` once, then the registered strict argv from {LANE}/SKILL.md:448 with
`--rev {B}` and paste exit (must equal the pre-change exit; run the pre-change bytes from
`git -C {LANE} show {B}:.ufo/gates/citation-drift/citation-drift-probe.py` saved under /tmp for the comparison).""", EX)
add("CustodyPairBranchTip", "executor", f"""
# Target
Edit in place {LANE}/.ufo/gates/custody-pair/custody-pair.py per {W18}/contract.md bullet `custody-pair.py`
(jj risk R3 in {AUDIT} line 167 and 246). Keep compare semantics and the receipt self-pin; add the selftest red
case. Run `--selftest` once; run one `capture --out /tmp/kr18-custody-test.txt` and paste the new header lines
(then delete the /tmp file). State whether the receipt-version must change and why.""", EX)
add("Verify17BranchTip", "executor", f"""
# Target
Edit in place {W17}/verify.py per {W18}/contract.md bullet `round-17/verify.py` (jj risk R1, {AUDIT} line 187
and 242). Minimal diff: only the source-revision resolution and the pre-run refusal; do NOT run verify.py (it
runs the whole r17 pass). Instead, prove the new resolution logic by extracting it into a tiny /tmp harness
that runs against a mkdtemp git repo with (a) HEAD == main == origin/main → ok, (b) detached off-branch HEAD →
exit 2. Paste the diff (`git -C {LANE} diff -- .ufo/waves/round-17/verify.py`) and harness outputs.""", EX)
add("JjRedBeforeProbe", "executor", f"""
# Target
Implement {W18}/tools/jj-red-before.py per {W18}/contract.md section `jj-red-before.py`. jj is
/home/vgpnk/.local/bin/jj 0.45.1; run jj ONLY inside the mkdtemp clone, never in {LANE}. The fixed tools are
being written concurrently by seats CitationDriftBranchTip, CustodyPairBranchTip and RevpinModule — implement
against the contract; you may run your probe only once those files exist in the working tree (check mtimes);
otherwise run only `--selftest`-equivalent dry setup (clone + jj init + off-branch commit + baseline steps) and
report that the green steps were not yet runnable.""", EX)
add("SwissMisreadTool", "executor", f"""
# Target
Implement {W18}/tools/swiss-misread.py per {W18}/contract.md section `swiss-misread.py`. Read the Ghidra
12.1.4 Go type reader in {SRCZIP} (unzip -p to stdout; members under ghidra/app/util/bin/format/golang/rtti/
and structmapping/) and the installed JSON {GODATA}/go1.24.0.json, go1.25.0.json (`runtime.maptype` aliases
`internal/abi.OldMapType`). Prior byte traces: {W17}/w2/RevAetherEOF.md, {W17}/w2/CriticAetherUnknown.md.
Acceptance gates you must run and paste: aether (/usr/bin/aether) must predict EOF read [17645861, 111938854];
/home/vgpnk/.local/bin/notesmd-cli must predict no failure; then run on all 8 carriers in {CARR} and paste the
per-carrier summary (do not freeze predictions — the L1 does).""", EX)
add("LogExtractEof", "executor", f"""
# Target
Edit in place {W17}/tools/log-extract.py per {W18}/contract.md bullet `log-extract.py` (additive `eof_reads`,
`symbol_analysis_failures`). Prove backward compatibility: for all 16 retained logs (8 at working tree under
{W17}/runs/*/logs/*/ghidra.log and 8 from `git -C {LANE} archive da64646 .ufo/waves/round-17/runs` extracted
to mkdtemp) old fields are byte-equal before/after (diff the JSON minus new keys). Aether must yield
`eof_reads` [[17645861, 111938854]]. Add red selftest cases.""", EX)
add("CompareEofFields", "executor", f"""
# Target
Edit in place {W17}/tools/compare.py per {W18}/contract.md bullet `compare.py` (`analyzer_errors_empty`,
`eof_reads` extra expectations), with red selftest cases. Then re-run compare on every retained r17
prediction/observation pair in {W17}/runs/*/ and paste that all exits are unchanged (the r17 predictions carry
no new keys).""", EX)
add("CarrierRunMidMaps", "executor", f"""
# Target
Edit in place {W17}/tools/carrier-run.py and {W17}/tools/receipt-validate.py per {W18}/contract.md bullet
`carrier-run.py` (R17-PINMAP forward fix: retain each mid-run map with its sha256; validator recomputes and
recompares). The defect text: {SPOT}:137. Selftests of both tools must stay clean and gain the tampered-mid-map
red case. Then run the updated receipt-validate.py on all 8 working-tree receipts {W17}/runs/*/receipt.json and
paste exits (must stay 0: r17 receipts carry no map_path).""", EX)
add("Validate16Run", "executor", f"""
# Target
Produce the R17-VALIDATE16 evidence ({SPOT}:138): run the round-17 receipt-validate.py exactly as committed at
{B} (`git show {B}:.ufo/waves/round-17/tools/receipt-validate.py` to /tmp) over the 8 first-pass receipts at
`da64646adcb19c1ede7537b799b8c7d283fe43da` (`git -C {LANE} archive da64646 .ufo/waves/round-17/runs | tar -x -C <mkdtemp>`).
Receipts record absolute paths under {W17}/runs — determine (read the validator) whether it reads those
absolute paths; if so, never validate the working-tree pass-2 files by accident: rewrite only the path prefix
in temp copies and record that remap. Write {W18}/evidence/validate16/summary.json
`{{rev, validator_rev, validator_sha256, remap, receipts: [{{label, exit, stdout_sha256, findings}}]}}` plus
per-label stdout/stderr files in the same dir. Report whatever the exits are (0 or not).""", EX)
add("SumsRestoreEvidence", "executor", f"""
# Target
R17-SUMS-RUNLOG evidence ({SPOT}:140-143). Write {W18}/evidence/sums-runlog.json: (1) the dropped line from
`git -C {LANE} diff 2711674 {B} -- .ufo/waves/round-17/predictions/SHA256SUMS`, (2) sha256 of carriers.tsv at
2711674, da64646 and {B} (must all equal 8ac38afe…), (3) a verify of every other SHA256SUMS line at {B} against
its blob, (4) the da64646 `runs/run-log.txt` lines and which carrier is missing (calib-shfmt) plus the evidence
that its first-pass receipt exists at da64646 with its timestamps. Do not edit the r17 SHA256SUMS; the L1
applies the restore.""", EX)
add("RunCarriers18", "executor", f"""
# Target
Write {W18}/run-carriers.sh per {W18}/contract.md section `run-carriers.sh` (adapt {W17}/run-carriers.sh;
same exit semantics; RUNS_DIR override). Also write {W18}/predictions/carriers.tsv with the 8 synthetic labels
from {CARR}/SHA256SUMS (kind column `synthetic-minimal-pair`) plus calibration rows for /usr/bin/aether and
/home/vgpnk/.local/bin/notesmd-cli labelled `calib-aether`, `calib-notesmd-cli`. `bash -n` it and dry-check
it with a fake `tools` dir under /tmp; never run REA.""", EX)
add("Measure18", "executor", f"""
# Target
Write {W18}/measure.py per {W18}/contract.md `measure.py` (Git objects at REV; imports routed-defects.py and
head-rev-lint.py by spec_from_file_location only when present at REV, otherwise reports could-not-evaluate
for that claim). Selftest with fixture repo. Run `measure.py {B}` and paste.""", EX)
add("Controls18", "executor", f"""
# Target
Write {W18}/controls.py per {W18}/contract.md `controls.py` (adapt {W17}/controls.py). Selftest red cases: a
rewritten LOG line, a changed QUALITY row 1-20, a changed S0xx cell other than status/recheck/used-by. Run
`controls.py {B} {B}` and paste (must report zero harm).""", EX)
add("Verify18Harness", "executor", f"""
# Target
Write {W18}/verify.py: the round-18 single post-integration pass, modelled on {W17}/verify.py but with
`source` from {W18}/tools/revpin.py `resolve_source(LANE)` (refuse before running anything on a finding). Commands
(argv lists, expected exits): every new/edited tool's --selftest (expect 0); routed-defects at baseline and
source; head-rev-lint at baseline and source (`--strict` at source expect 0, at baseline expect 1);
jj-red-before; receipt-validate over W18 runs receipts; compare over W18 runs; measure baseline/source;
controls baseline source; citation-drift strict at source; temporal-sweep and invocation-audit at source;
sources census `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`;
custody capture. Pins pre/post via {W17}/tools/pins.py. Do not run it; `python3 -I -B -c 'import ast,sys;ast.parse(open(sys.argv[1]).read())' <file>` only.""", EX)
add("CarrierRecipeAudit", "executor", f"""
# Target
Independently re-run the carrier recipe {W18}/carriers/build.sh with `OUT=<mkdtemp>` twice and compare against
{CARR}/SHA256SUMS (determinism, QUALITY #12 at {LANE}/corpus/QUALITY.md:22). Then read each carrier's build info
with `/home/vgpnk/.local/opt/go-1.27.3/bin/go version -m <file>` and {W17}/tools/buildinfo-probe.py, and write
{W18}/evidence/carrier-buildinfo.json `{{label: {{sha256, go_version, GOEXPERIMENT, build_settings}}}}`. Confirm
noswiss carriers record GOEXPERIMENT=noswissmap. Never execute a carrier.""", EX)
add("RealCarrierCensus", "executor", f"""
# Target
Find real (non-synthetic) Go 1.24.x/1.25.x ELF binaries on this host that are not r17 carriers ({W17}/predictions/carriers.tsv):
use {W17}/tools/carrier-census.py (read its --help) and/or buildinfo-probe.py over /usr/bin, /usr/lib, ~/.local/bin,
~/go/bin, ~/.cargo/bin, /opt. Write {W18}/evidence/real-carrier-census.json listing path, sha256, size, go
version, GOEXPERIMENT, owning package (`pacman -Qo`, read-only). Rank up to 3 candidates by size (<40 MB) and
whether they plausibly declare a named map type with methods (e.g. imports net/http → http.Header, net/url →
url.Values) using `go version -m` deps only. Never execute them.""", EX)

# ---------------- revengers ----------------
add("RevGhidraMapTypeRead", "revenger", f"""
# Target
Reverse the exact Ghidra 12.1.4 code path that reads a Go map type descriptor and its uncommon/method data:
GoType.getUncommonType / GoMapType / structure-size computation from the snapshot JSON / GoName reads, in
{SRCZIP}. Output: the algorithm as numbered steps with member:line anchors, the offset formula Ghidra uses for
the uncommon struct, and which BinaryReader call raises `Unable to read past EOF: A, B` and what A and B mean.""", RO)
add("RevAetherReplay", "revenger", f"""
# Target
Independently (without reading any new W18 tool) recompute from /usr/bin/aether's bytes the misread chain that
yields `Unable to read past EOF: 17645861, 111938854` (r17 log {W17}/runs/pro-aether/logs/*/ghidra.log:177).
Start from {W17}/w2/RevAetherEOF.md and verify or correct each step with your own byte reads (python3, xxd,
readelf). Name the map type descriptor address(es) involved and the field Ghidra misreads. This is the
independent cross-check for SwissMisreadTool.""", RO)
add("RevProducerRev", "revenger", f"""
# Target
R17-PRODUCER-REV ({SPOT}:139). Determine, from Git history and receipt bytes only, which lane revision's
carrier-run.py produced (a) the 8 first-pass receipts at da64646 and (b) the 8 second-pass receipts at {B}.
Use receipt key sets (e.g. `carrier.md5_pre`, `binding.md5_ok`), `orig_argv`, timestamps vs commit/push times
(`git log --format='%H %cI'`), and blob history of .ufo/waves/round-17/tools/carrier-run.py
(2711674, da64646, 95e34db, d0ab299). Output the two 40-hex producing revisions with the evidence chain and any
residual uncertainty (e.g. uncommitted working-tree bytes).""", RO)
add("RevNotesmdMaps", "revenger", f"""
# Target
For /home/vgpnk/.local/bin/notesmd-cli and the 8 synthetic carriers in {CARR}: enumerate runtime map type
descriptors (kind Map) and how many carry the uncommon tflag, by your own byte parsing of the type section via
moduledata/typelinks. r17 claimed notesmd-cli has 63 map types, none with method info ({KENTRY}:158-160).
Confirm or refute, and give counts per synthetic carrier (expected: methods variants have ≥1 uncommon map type,
nomethods variants report whether stdlib alone contributes any).""", RO)

# ---------------- scouts ----------------
add("ScoutGo124NotesSwiss", "scout", """
# Target
Open https://go.dev/doc/go1.24 and locate the runtime Swiss-table map section and the `GOEXPERIMENT=noswissmap`
opt-out. Record URL, access date, page sha256 (`curl -sL | sha256sum`, twice: is it stable?), exact heading/id
anchor and a ≤25-word contiguous quote. Draft a SOURCES row (11 cells, per /home/vgpnk/Projects/shokunin/CORPUS.md
SOURCES contract) scoped to "Go 1.24 default map implementation and its build-time opt-out".""", RO)
add("ScoutGo125MapsNotes", "scout", """
# Target
Determine from official Go sources whether Go 1.25 still supports GOEXPERIMENT=noswissmap: open
https://go.dev/doc/go1.25 (search for swiss/map) and the go1.25.0 tree's src/internal/buildcfg/exp.go and
src/runtime/map_noswiss.go build tags (raw.githubusercontent.com/golang/go/go1.25.0/...). Also check the installed
toolchain /home/vgpnk/.local/opt/go-1.25.0/src. Record exact anchors and ≤25-word quotes; draft a row if a new
source is needed.""", RO)
add("ScoutAbiSwissLayout", "scout", """
# Target
Open the go1.24.6 and go1.25.0 source of internal/abi map type definitions (/home/vgpnk/.local/opt/go-1.24.6/src/internal/abi/
and go-1.25.0; files map_swiss.go / map_noswiss.go or equivalents) and the upstream raw URLs. Record the field
lists and computed struct sizes of SwissMapType and OldMapType on amd64, file:line anchors, and file sha256.
Draft a code-kind SOURCES row scoped to "Go 1.24/1.25 amd64 map type descriptor layouts".""", RO)
add("ScoutAbiTypeUncommon", "scout", """
# Target
In /home/vgpnk/.local/opt/go-1.25.0/src/internal/abi/type.go, locate abi.Type, TFlagUncommon, UncommonType
and the function computing the uncommon offset per kind (Type.Uncommon). Record exact lines and how the offset
depends on the kind-specific struct size (map kind → which struct). ≤25-word quote with file:line; draft row
or say an existing S0xx row covers it.""", RO)
add("ScoutInstalledJsonMaps", "scout", f"""
# Target
In the installed Ghidra Go data {GODATA}: for go1.24.0.json and go1.25.0.json report `runtime.maptype` alias
target, the field list and total size of internal/abi.OldMapType and internal/abi.SwissMapType as the JSON
defines them, and which patch diffs exist for 1.24/1.25 (patchverdiffs/). Which snapshot does r16 selection
({LANE}/.ufo/waves/round-16/selection.py) pick for 1.24.6 and 1.25.0? Run it read-only and paste.""", RO)
add("ScoutGhidraGoStructMapping", "scout", f"""
# Target
In {SRCZIP}: how does Ghidra's Go structure mapping bind a Java class (GoMapType etc.) to the snapshot JSON
type `runtime.maptype`/`internal/abi.*MapType` (annotations, GoTypeManager registration)? Is there any
Swiss-map class or version switch in 12.1.4? List member:line anchors. Compare with the master change named by
S032 (PR #9348) only by reading the PR's files list (https://github.com/NationalSecurityAgency/ghidra/pull/9348/files).""", RO)
add("ScoutPr9348Reopen", "scout", """
# Target
R17-S032-DIGEST: re-open https://github.com/NationalSecurityAgency/ghidra/pull/9348 three times with curl and
compute sha256 each time (expect instability); also fetch the API JSON
https://api.github.com/repos/NationalSecurityAgency/ghidra/pulls/9348 and record title, state, merged, head sha,
updated_at. Draft the superseding row S033 whose teaches starts `supersedes S032 —` and whose anchor is title +
state + head sha with the page digest marked `fetch-time only`, plus a ≤25-word quote from the PR body.""", RO)
add("ScoutJjColocation", "scout", """
# Target
Open the jj 0.45 documentation on Git compatibility / colocated workspaces (https://jj-vcs.github.io/jj/latest/git-compatibility/
and the 0.45.x tagged docs if available; also /home/vgpnk/.local/bin/jj help -k? only `jj help` text is allowed
outside any repo cwd). Find the statement about Git HEAD being detached / pointing at the working-copy parent
in colocated repos. Record URL, version, anchor, ≤25-word quote; draft a docs-kind SOURCES row scoped to "jj
colocated repos: what Git HEAD names".""", RO)
add("ScoutJjRevsetsTrunk", "scout", """
# Target
Open the jj documentation for revsets/bookmarks (remote bookmarks `name@remote`, `trunk()`), the jj config
`snapshot.auto-track`, and the 1 MiB `snapshot.max-new-file-size` default. Record URLs, anchors, quotes; say
which, if any, deserve a SOURCES row for this round's C2 (branch-tip pinning) and which are leads only.""", RO)
add("ScoutGitRevParseDocs", "scout", """
# Target
Open the official git-rev-parse documentation (https://git-scm.com/docs/git-rev-parse) and gitrevisions
(https://git-scm.com/docs/gitrevisions): what `--verify`, `<rev>^{commit}`, `refs/heads/<name>` vs `HEAD`,
and `@{upstream}` require (attached branch). Record anchors and quotes; recommend whether a row is warranted.""", RO)
add("ScoutLaneGitSitesNow", "scout", f"""
# Target
Re-run the jj audit's sweep at the current baseline {B} (the audit used da64646): list every git argv in lane
tools under .ufo/gates, .ufo/rounds, .ufo/waves/round-14..17 (Git objects at {B}, `git grep -n` at {B}) and
diff against {AUDIT} section 3. Any new HEAD-keyed or upstream site added after da64646 (e.g. r17 final tools,
w2 seat tools)? This is the expected-count oracle for HeadRevLintTool.""", RO)
add("ScoutValidate16Sites", "scout", f"""
# Target
Find every lane text site at {B} claiming all 16 receipts validated (R17-VALIDATE16, {SPOT}:138): `git -C {LANE}
grep -n -I -E '16 receipts|all 16|16/16' {B} --` and read hits. Also the fleet report
/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/kaidoku.md. Classify each site: overstated / correct /
unrelated. List exact file:line.""", RO)
add("ScoutPinmapSites", "scout", f"""
# Target
Find every lane text site at {B} stating mid-run pin maps are retained (R17-PINMAP, {SPOT}:137): grep for
`pin map`, `pin_checks`, `maps are equal`, `pre/mid/post`, `each pin map`. Read {W17}/tools/carrier-run.py:470-500
for what is actually retained. Output exact file:line list with the overstated phrase, and the accurate
replacement wording.""", RO)
add("ScoutProducerRevSites", "scout", f"""
# Target
Find every lane text site at {B} citing a "measured source revision" or producing revision for the r17 runs
(R17-PRODUCER-REV, {SPOT}:139): SCORECARD round-17 section, LOG round-17, {KENTRY}, corpus/lessons/round-17.md,
SKILL.md r17 section. Exact file:line and what each says.""", RO)
add("ScoutRegistryFields", "scout", f"""
# Target
R17-REGISTRY ({SPOT}:144-146). Read the canonical registry-row field requirement in
/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md (search `Gate standard`, `write scope`,
`Pinned`) and quote it. For each of the 10 round-17 rows {LANE}/SKILL.md:537-546 plus citation-drift :448,
list which required field is missing, and what the row's tool actually writes and pins (read the tool). Output a
per-row table: missing field → proposed exact cell text.""", RO)
add("ScoutReaPin", "scout", """
# Target
Confirm the REA CLI used for carrier runs is still reproducible: `npx -y rea-agents@6.5.0 --version` and
`npx -y rea-agents@6.5.0 analyze --help` (no target), and `ls ~/.npm/_npx/*/node_modules/rea-agents/package.json`
versions. Never run analyze on a target. Report versions, paths and whether rea-agents 6.7.0 is also cached.""", RO)
add("ScoutSkillGoSection", "scout", f"""
# Target
Read {LANE}/SKILL.md:509-546 (r17 Go carrier section) and {KENTRY} and list exactly which rows/sentences a
confirmed or refuted Swiss-map replay (C3) would have to update or qualify (e.g. SKILL.md:528 INFERENCE row,
the corollary at {KENTRY}:161-166). Output a site list with the conditional new wording for both outcomes.""", RO)
add("ScoutCoverageMap", "scout", f"""
# Target
Read {LANE}/corpus/README.md (coverage map and `## Frontier`) and {LANE}/PROVINCE.md: is "Go map type
descriptor layout / Swiss maps under Ghidra" held ground, frontier, or unmapped? Cite lines. This decides whether
a C3 knowledge entry is expansion (uncovered ground) or deepening held ground.""", RO)
add("ScoutProtocolGate", "scout", """
# Target
Read /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md lines 300-544 and extract only
the rules binding a child-lane round's evidence (gate standard, two evidences, frozen re-run, registry rows,
red-before). Quote each with line numbers; flag any this round's plan (claims in
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/claims.json) could violate.""", RO)
add("ScoutOperatorLessons", "scout", f"""
# Target
List {LANE}/corpus/lessons/operator-*.md (if any) and every routed defect in earlier verifier spot-checks
(round-12..16-verifier-spotcheck.md) still open at {B}: for each, the routing line and whether a later lane
commit discharged it (`git log -S`). Output open items only, with evidence.""", RO)
add("ScoutMistakeSweep", "scout", f"""
# Target
Mine candidate mistakes for corpus/lessons/round-18.md `## Mistakes` from round 17: compare the r17 report
/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/kaidoku.md, {LANE}/corpus/lessons/round-17.md and the
outside check {SPOT}. For each disagreement give class (vocabulary in /home/vgpnk/Projects/shokunin/CORPUS.md:171-178),
evidence pointer, which QUALITY.md row should have caught it (captured-by) or `none`.""", RO)
add("ScoutMisrootFleet", "scout", """
# Target
Run `git -C /home/vgpnk/Projects/shokunin status --porcelain` and list untracked files at the fleet root whose
content names kaidoku or round-18 (grep -l). Read-only; never delete. Report exact paths.""", RO)
add("ScoutGoReSymSwiss", "scout", """
# Target
Does any other Go RE parser handle Swiss map types (GoReSym v3.4.1 release notes/changelog, redress, Ghidra
master after 12.1.4)? Open primary sources only (GitHub releases/commits); record anchors and quotes; propose at
most one SOURCES row or a lead line.""", RO)

# ---------------- connectors ----------------
add("ConnSiblingOverlap", "connector", """
# Target
Sibling-overlap scan: read every /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md and grep sibling corpora
for Go RTTI/Swiss map/Ghidra Go and for jj branch-tip tooling fixes. Report contested scope and who owns what;
nothing is absorbed.""", RO)
add("ConnDefectCriteria", "connector", f"""
# Target
Map each of the six R17 routed defects ({SPOT}:137-147) to the QUALITY.md row ({LANE}/corpus/QUALITY.md) that
should have caught it (captured-by) or `none`, and say whether a new criterion is warranted. Output a table usable
directly for `## Mistakes` rows.""", RO)
add("ConnJjRegistry", "connector", f"""
# Target
Connect {AUDIT} and {TRIAL} findings to the lane's SKILL.md registry rows (:445-546): which rows' entries or
recheck commands assume HEAD or a working-tree state, and which need a jj note (e.g. invocation-audit revision
scoping, auto-track none() making untracked files absent at REV). Output proposed row-cell text.""", RO)
add("ConnCorrectionPlacement", "connector", f"""
# Target
For each planned correction (R17-PINMAP, VALIDATE16, PRODUCER-REV, SUMS-RUNLOG; {SPOT}:137-143), decide the
append-only placement consistent with /home/vgpnk/Projects/shokunin/CORPUS.md:53-60 (corrections are new entries)
and PROTOCOL append-only rules: which files take an appended correction (LOG.md, SCORECARD.md r18 section,
{KENTRY} appended section) and which must never be rewritten. Output the exact placement list.""", RO)
add("ConnSourcesPaths", "connector", f"""
# Target
Propose the `## Paths` update in {LANE}/corpus/SOURCES.md for this round's likely new rows (Go 1.24 notes, abi
map layout source, jj colocation docs, S033 superseding S032): ordered study sequences with one-line why. Also
the search-log entry skeleton (identified/screened/included/excluded counts to be filled from scout reports).""", RO)
add("ConnMistakeTaxonomy", "connector", """
# Target
Read /home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w1/mistakes.md §5 and §8 and map this lane's recurring
mistake classes across rounds 14-17 lessons (/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-1[4-7].md
## Mistakes). Which classes recur after capture (fix not shown able to fail)?""", RO)
add("ConnFleetJjPractice", "connector", """
# Target
Read-only: how have other lanes this phase fixed HEAD-keyed revision pins under jj (grep sibling repos
/home/vgpnk/Projects/shokunin/*-shokunin for `refs/heads/`, `rev-parse HEAD`, `trunk()` in .py/.sh tools and
their LOG.md). Report patterns worth reusing and any pitfalls, with paths.""", RO)
add("ConnC3Prediction", "connector", f"""
# Target
Connect r17's aether inference ({KENTRY}:145-166) to the C3 design ({W18}/claims.json, {W18}/contract.md C3):
does the minimal pair actually separate the hypotheses (Swiss-layout misread vs patch fallback vs other)? Which
outcome pattern across the 8 carriers would confirm, refute, or leave it unresolved? Output a frozen-ready
outcome table.""", RO)

# ---------------- scribes ----------------
add("DraftS033Row", "scribe", """
# Target
Open https://github.com/NationalSecurityAgency/ghidra/pull/9348 yourself and draft S033 (11 cells, contract in
/home/vgpnk/Projects/shokunin/CORPUS.md:76-129): teaches opens `supersedes S032 —`; anchor = PR title, state, head
commit, accessed date, page sha256 marked `fetch-time only`; plus the lesson `## Gate` line (URL, access date,
≤25-word quote with location).""", DR)
add("DraftGoNotesRow", "scribe", """
# Target
Open https://go.dev/doc/go1.24 yourself and draft the SOURCES row for the Swiss-table maps section with its
GOEXPERIMENT=noswissmap opt-out (tier A docs), plus the `## Gate` quote line (≤25 words, located).""", DR)
add("DraftAbiRow", "scribe", """
# Target
Open the go1.25.0 internal/abi map type source (raw.githubusercontent.com/golang/go/go1.25.0/src/internal/abi/,
and /home/vgpnk/.local/opt/go-1.25.0/src/internal/abi/) yourself and draft one code-kind SOURCES row for the
SwissMapType/OldMapType descriptor layouts, plus the `## Gate` quote line.""", DR)
add("DraftJjRow", "scribe", """
# Target
Open the jj git-compatibility documentation (https://jj-vcs.github.io/jj/latest/git-compatibility/) yourself and
draft one docs-kind SOURCES row on colocated repos and Git HEAD, plus the `## Gate` quote line.""", DR)
add("DraftPinmapCorrection", "scribe", f"""
# Target
Draft the R17-PINMAP corrections ({SPOT}:137): (1) an appended `## Round-18 correction` section for {KENTRY}
naming lines 28-33 and stating "mid-run instants retain the comparator verdict against the retained pre map, not
the map" (must contain `R17-PINMAP` and `comparator verdict`); (2) one SCORECARD round-18 line correcting
SCORECARD.md:2374; (3) the forward fix sentence (carrier-run.py now retains each mid map with map_sha256).""", DR)
add("DraftQualityRow21", "scribe", f"""
# Target
Draft QUALITY.md admission row #21 from the partial outside disagreement ({SPOT}:108,137) — a retention claim
names each retained field; a comparator verdict is never described as the compared object. Why-cell cites
`corpus/lessons/round-17-verifier-spotcheck.md` R17-PINMAP and `corpus/lessons/round-18.md`; supersedes column
(`sharpens 19` or `—`). Follow the table shape at {LANE}/corpus/QUALITY.md:9-30 exactly (4 cells).""", DR)
add("DraftRegistryCells", "scribe", f"""
# Target
Draft replacement 5th cells (`Pinned values / write scope`) for SKILL.md rows go-route-compare, receipt-validate,
pins, go-buildinfo-probe ({LANE}/SKILL.md:540-545), each containing `Write scope:`, and the citation-drift row
kind change to `gate / kaidoku` with the probe-vs-strict sentence ({LANE}/SKILL.md:448). Read each tool to state
its true write scope and pinned values.""", DR)
add("DraftLessonSkeleton", "scribe", f"""
# Target
Draft corpus/lessons/round-18.md structure following {LANE}/corpus/lessons/round-17.md's shape: `## Gate`
(candidates/admitted/rejected/spot-check placeholder stated as pending non-author closure), `## Mistakes`
(class · evidence · captured-by · fix) with rows for R17-VALIDATE16 (number-drift), R17-PINMAP (overstatement),
R17-SUMS-RUNLOG (landing/reference-drift), using only facts in {SPOT}. Mark fields that need round results as
"filled at integration" (the L1 fills them).""", DR)
add("DraftSkillJjNote", "scribe", f"""
# Target
Draft a short SKILL.md subsection "Revision pins under jj (round 18)": a 3-row decision table (signal → decision
→ limit) on branch-tip vs HEAD, `--rev HEAD` refusal, custody repo-branch-tip, grounded in {AUDIT} F1/F2 and
{TRIAL} hazards 3-4, with path:line citations.""", DR)
add("DraftSwissTable", "scribe", f"""
# Target
Draft the SKILL.md decision-table rows for the Swiss-map replay in both outcomes (confirmed / refuted), in the
shape of {LANE}/SKILL.md:521-528 (Signal in a bound ghidra.log | Decision | Limit). Keep INFERENCE labels where
the replay cannot reach (silent size misread).""", DR)

# ---------------- reviewers ----------------
for name, d, what in [
    ("RevBasePinmap", "R17-PINMAP", f"{SPOT}:137 against {KENTRY}:28-33, SCORECARD.md:2374, {W17}/tools/carrier-run.py:470-500"),
    ("RevBaseValidate16", "R17-VALIDATE16", f"{SPOT}:138 against {W17}/verification.json (count receipt-validate-* commands and their revs)"),
    ("RevBaseProducerRev", "R17-PRODUCER-REV", f"{SPOT}:139 against receipt key sets at da64646 vs {B}"),
    ("RevBaseSumsRunlog", "R17-SUMS-RUNLOG", f"{SPOT}:140-143 against `git diff 2711674 {B} -- .ufo/waves/round-17/predictions/SHA256SUMS` and da64646 runs/run-log.txt"),
    ("RevBaseRegistry", "R17-REGISTRY", f"{SPOT}:144-146 against {LANE}/SKILL.md:448,537-546"),
    ("RevBaseS032", "R17-S032-DIGEST", f"{SPOT}:147 against {LANE}/corpus/SOURCES.md:38 (re-fetch the PR page twice)"),
]:
    add(name, "reviewer", f"""
# Target
Falsify the baseline premise of C1 for {d}: is the defect really open at {B}? Check {what}. Verdict: open /
already-closed / mis-stated, with the exact evidence. Also state the minimal objective test that distinguishes
open from closed (it will be compared with {W18}/contract.md routed-defects definitions — say if that definition
is too weak or too strong).""", RO)
for name, r, what in [
    ("RevBaseVerify59", "R1", f"{W17}/verify.py:55-60 and how source_revision feeds later commands"),
    ("RevBaseCitationRev", "R2", f"{LANE}/.ufo/gates/citation-drift/citation-drift-probe.py:100-110,260-280,470-490"),
    ("RevBaseCustodyHead", "R3", f"{LANE}/.ufo/gates/custody-pair/custody-pair.py:320-360"),
]:
    add(name, "reviewer", f"""
# Target
Falsify jj risk {r} from {AUDIT} at the current baseline {B}: re-read {what}; are the cited lines still those?
Is the risk real under the lane's current state (`/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state {LANE}`,
`git -C {LANE} rev-parse HEAD main origin/main`)? What minimal change fixes it without changing explicit-rev
behaviour? Compare with {W18}/contract.md.""", RO)
add("RevValidatorPaths", "reviewer", f"""
# Target
Read {W17}/tools/receipt-validate.py: does it read files via absolute paths recorded in the receipt? Predict the
result of validating the da64646 first-pass receipts (which lack carrier.md5_pre / binding.md5_ok per {SPOT}:139):
will the current validator exit 0, 1 or 2 on them, and why (cite lines)? This prediction is recorded before
Validate16Run's result is read.""", RO)
add("RevLogExtractScope", "reviewer", f"""
# Target
Read {W17}/tools/log-extract.py and the 16 retained r17 logs (8 under {W17}/runs, 8 at da64646): where exactly do
`Unable to read past EOF` and `Go analysis failure` appear (line numbers, levels, stack-trace format)? Is a
stack-trace line inside the polling-prefix capture guaranteed? Advise LogExtractEof on the parse rule.""", RO)
add("RevPinChecksCode", "reviewer", f"""
# Target
Read {W17}/tools/carrier-run.py pin_checks code and {W17}/tools/receipt-validate.py mid-run checks: list exact
lines to change for retaining mid maps with digests, and the backward-compatibility risk for the 16 retained
receipts. Advise CarrierRunMidMaps.""", RO)
add("RevClaimsSeparable", "reviewer", f"""
# Target
Review {W18}/claims.json: are C1/C2/C3 causally separable (each verifiable without the others), on distinct axes,
each with a falsifiable before→after and a counting command? Does C1 touch C3's tools (carrier-run.py edit) in a
way that couples them? Recommend concrete fixes.""", RO)
add("RevRunCarriersPlan", "reviewer", f"""
# Target
Review the plan to run 10 carriers (8 synthetic + aether + notesmd-cli recalibration) with {W17}/tools via a
{W18}/run-carriers.sh: env (REA_GHIDRA_STARTUP_TIMEOUT_MS), session dirs, pin list, timeouts from r17 receipts
({W17}/runs/*/receipt.json durations). Estimate wall time and failure modes; list preconditions the L1 must check.""", RO)
add("RevContractC3", "reviewer", f"""
# Target
Review {W18}/contract.md C3 `swiss-misread.py` spec against Ghidra source ({SRCZIP}) and Go abi: is the "true
layout" rule (Swiss iff Go ≥ 1.24 and GOEXPERIMENT lacks noswissmap) correct for 1.24.6 and 1.25.0? Is
predicted_failure well-defined? Name any source evidence that would make the emulator unfalsifiable.""", RO)

# ---------------- critics / sentinels ----------------
add("CriticC1", "critic", f"""
# Target
Attack C1 ({W18}/claims.json): is routed-defects.py a circular counter (corrections written to satisfy greps)?
For each of the six definitions in {W18}/contract.md, construct the cheapest text change that would flip it closed
without fixing the defect, and propose a stronger objective check. Judge whether "6 → 0" would be calibration
improvement or bookkeeping.""", RO)
add("CriticC2", "critic", f"""
# Target
Attack C2: is "3 live HEAD sites → 0" meaningful, or does head-rev-lint just stop seeing them (AST fixture
classification, shell scripts, f-strings, default arguments built at runtime)? Is the jj-red-before sandbox a
faithful model of the lane's jj state ({TRIAL} Step 4)? What would a non-author need to see to agree operability
improved?""", RO)
add("CriticC3", "critic", f"""
# Target
Attack C3: synthetic minimal-pair carriers vs real-world generality; emulator calibrated on aether then used to
predict the pair (is it overfit to one datum?); noswissmap control validity; whether any outcome would be called
a success (unfalsifiable framing). Propose the exact pre-registered decision rule (confirmed/refuted/unresolved)
to freeze with the predictions.""", RO)
add("CriticSourcedClaim", "critic", """
# Target
Attack the sourced-claim requirement (/home/vgpnk/Projects/shokunin/.ufo/prompts/kaidoku-round-18.md:73-74):
which planned row truly grounds which claim (S033 for C1, jj docs for C2, Go notes/abi for C3)? Is a superseding
digest row a real learning source or bookkeeping? Recommend which claim to file as the sourced one.""", RO)
add("CriticNoHarmPlan", "critic", f"""
# Target
Attack the no-harm plan: editing round-17 tools in place (carrier-run.py, receipt-validate.py, log-extract.py,
compare.py, verify.py) after their outputs were cited — does that harm reproducibility of r17 evidence or break
{W17}/controls.py frozen-blob checks? Should copies live under round-18 instead? Decide with evidence.""", RO)
add("CriticDiscernment", "critic", f"""
# Target
Attack the planned discernment verdict: the r17 outside check partially disagreed on the pin sentence ({SPOT}:108).
What would make round-18's QUALITY #21 a grounded criterion versus a criterion "with no lesson behind it"
(/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md:35)? Propose the red-before evidence.""", RO)
add("SentinelSandbox", "sentinel", f"""
# Target
Security/safety review of the planned jj-red-before sandbox ({W18}/contract.md) and the lane jj state: could any
step write {LANE} (jj discovery walking up from a mkdtemp under the lane, TMPDIR inside the lane, `git clone`
hardlinks, jj operation log)? Check `echo $TMPDIR`, `findmnt /tmp`. Recommend guards.""", RO)
add("SentinelReaEnv", "sentinel", f"""
# Target
Review REA run hygiene for the 10 planned carrier runs: {W17}/tools/carrier-run.py env allowlist, session.json
bridge-token exclusion, private TMPDIR, no carrier execution, toolchain tarball provenance (go1.24.6/go1.25.0 in
~/.local/opt verified against go.dev JSON). Report any leak path with line anchors.""", RO)

# ---------------- simplifiers ----------------
add("SimplifyRoutedDefects", "simplifier", f"""
# Target
YAGNI review of {W18}/contract.md C1/C2 tool specs: which outputs/flags/checks are not needed for the claims'
counting commands and can be dropped; which duplicate existing tools ({W17}/tools/*.py, {W17}/controls.py).""", RO)
add("SimplifyC3Tools", "simplifier", f"""
# Target
YAGNI review of C3: does swiss-misread.py need full moduledata parsing, or can typelinks + r17 buildinfo-probe.py
suffice? Can {W18}/run-carriers.sh be a thin parameterization of {W17}/run-carriers.sh instead of a copy?""", RO)

spec = {
    "wave": "kaidoku-r18-w1",
    "axes": ["calibration", "operability", "depth"],
    "reportDir": ".ufo/waves/round-18/w1",
    "maxLanes": 100,
    "context": (
        "# Goal\nKaidoku round 18 (hyaku phase 2), axes calibration + operability + depth. Claims: "
        f"{W18}/claims.json. Shared contract: {W18}/contract.md. L1 (KaidokuR18) holds the canonical planner seat; "
        "you are an author-side advisory seat, never an outside reviewer. REA CLI: `npx -y rea-agents@6.5.0 <command>` "
        "(the OMP rea MCP entry is disabled by operator authorization; never use xd://mcp__rea_* devices).\n"
        "# Contract\nLeaf: never delegate (executors may spawn at most one read-only labrat for a falsifiable hypothesis). "
        "Never run REA analyze/search/decompile or Ghidra/analyzeHeadless (the L1 runs every carrier analysis once, sequentially, "
        "after predictions are frozen). Never execute carrier binaries. Write ONLY your report and your explicitly assigned "
        f"file(s), at absolute paths under {LANE}. Never edit LOG/SCORECARD/QUALITY/SKILL/SHONEN/SOURCES/PROVINCE/README, "
        "knowledge, or committed lessons; the L1 integrates drafts. The lane is jj-colocated: never run `jj` or any git write "
        "(add/commit/stash/checkout/reset/rebase/push) in the lane; read-only git only; jj/git writes only inside a mkdtemp clone. "
        "Never write the fleet repo /home/vgpnk/Projects/shokunin outside the lane dir. Every `Report:` trailer path is "
        f"relative to {LANE} — write it at {LANE}/<that path>. Keep reports concise; cite exact path:line anchors; label "
        "observation vs inference; never fabricate output. Message only KaidokuR18 if blocked; never the orchestrator, never agent://all.\n"
        "# Host safety\nYou and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md "
        "first (official channels; record tool/version/channel/reason in your report). pacman guard: ALL pacman transactions are "
        "PAUSED host-wide (read-only `pacman -Q*` queries are fine); install via `uv tool`/`npx`/an official binary in ~/.local/bin "
        "instead, or report the need. When the pause lifts: before any `pacman -S` run `pacman -Sp --print-format '%n %v' <pkgs>` "
        "and proceed only if every listed package is not installed; never -Sy/-Syu/-U/-R, downgrade, or restart a host service. "
        "Never open/copy/query ~/.omp/agent/agent.db* or credential/auth files; never launch omp CLI processes; never modify "
        "client routing or host services. Prefer no installs."),
    "items": items,
}
with open(os.path.join(HERE, "wave1-spec.json"), "w") as f:
    json.dump(spec, f, indent=1, ensure_ascii=False)
from collections import Counter
print(len(items), dict(Counter(i["role"] for i in items)))
