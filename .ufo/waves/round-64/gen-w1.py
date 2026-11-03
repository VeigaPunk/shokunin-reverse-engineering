#!/usr/bin/env python3
"""Generate the kaidoku round-64 wave-1 spec (one v1 build+attack wave, 12 seats). R64, KaidokuR64.

Interpolation discipline: LANE/W1 paths are substituted at build time; the rendered items must
contain no unresolved `{...}` placeholders (checked below before the spec is written).
"""
import json, pathlib, re

GS = open('/home/vgpnk/.agents/skills/godspeed/directive.md').read().strip()
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
W1 = LANE + '/.ufo/waves/round-64/w1'
HOME = '/home/vgpnk/.local/share/kaidoku-jsc'
TOOL = LANE + '/tools/round-64/jsc-route-matrix.py'
CLAIMS = LANE + '/.ufo/waves/round-64/claims.json'
PLAN = LANE + '/plans/round-64-claims.md'
PROBE = LANE + '/.ufo/waves/round-64/inputs/probe-electron.jsc'
TYPORA = HOME + '/inputs/atom.compiled.dist.jsc'
PREFREEZE = LANE + '/.ufo/waves/round-64/l1/prefreeze-probe'
SCRATCH = '/fast/scratch/hyaku/kaidoku-r64'

CONTEXT = f"""# Target
kaidoku-shokunin round 64, attempt 1, wave w1 = the single v1 build+attack wave (12 seats; policy band 8-16,
attack seats reviewer, critic, mutation-tester = 4 of 12). One declared claim: R64-C1 (depth, capability
acquisition): the `.jsc` -> source route (jsc2js: patched d8 dump, then View8 reconstruction, then `node --check`)
run as a frozen 18-run outcome matrix. Frozen declaration {LANE}/plans/round-64-claims.md (declared at 3fd8468c),
operative freeze {CLAIMS} (landed at a35e5141). Predicate, verbatim from the frozen claims file:
"R64-C1 is verified iff all 18 runs reproduce the frozen predicted label of their cell (dump|view8|check), with
every input and binary sha256 equal to its pin."

# Frozen inputs (read-only; NEVER edit or re-predict)
- Instrument: {TOOL} (sha256 29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb). Its PREDICTED table and PINS
  are frozen. Do not edit the instrument or the claims file; a finding that needs an edit is reported, never made.
- Probe artifact: {PROBE} (sha256 a86f6ea0...), an Electron 42.2.0 code cache.
- Typora artifact: {TYPORA} (sha256 6a0cb7b3...), extracted from /usr/share/typora/resources/app.asar.
- Toolchain (persistent, outside scratch): {HOME}/d8-14.8.178.14, {HOME}/d8-14.8.178.1, {HOME}/d8-14.7.173
  (each with d8, snapshot_blob.bin and icudtl.dat), {HOME}/jsc2js-src (jsc2js at 01fc264d22055865a460b322399a15d84b71f5aa),
  {HOME}/venv/bin/python (parse 1.22.4). Read these; never write into them.
- Pre-freeze probe receipts (already committed): {PREFREEZE}.

# Shared rules (bind every seat)
- Scratch: every clone, copy, dump, work tree and fixture lives under {SCRATCH}/<your-seat-name>/ created with mkdir -p and
  passed explicitly (--work, TMPDIR). /tmp is for files under 50 MB only. Delete your scratch dir before you yield
  (trap 'rm -rf -- "$S"' EXIT in shell). Check `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` before a heavy pass.
- Write only inside your own report directory {W1}/<your-seat-name>/ (absolute path). Every `Report:` trailer path is
  relative to {LANE} — write it at {LANE}/<that path>.
- Never run git/jj mutating commands (add, commit, stash, checkout, reset, pull, push, jj commit/new/describe/bookmark). Read-only git
  (log, show, diff, status, ls-files, rev-parse, ls-remote) is fine with `git -C {LANE} ...`.
- Never touch the fleet root, MANIFEST.json, .ufo/state/, .ufo/watchdog.log, sibling lane repos (read-only grep only), or
  /home/vgpnk/Projects/shokuknow (read-only; never run its tools).
- Network: only the URLs your task names. Never pipe a remote script into a shell. Official sources only.
- Tooling authorization (operator, 2026-10-19; /home/vgpnk/.omp/agent/RULES.md): you may install or upgrade tools that
  help your task through official channels, recording tool, version, channel and reason. pacman is PAUSED host-wide:
  never run pacman, -Sy, -Syu or partial upgrades.
- Use absolute paths for every read, write and edit. Do not poll; run each command once, read its output, act.
- Keep your final yield short: findings with evidence pointers (paths, command, exit code, sha256). Report only what you ran.
"""

ITEMS = [
 ("ScoutJscRoute", "scout", f"""Read-only upstream recon for R64-C1. Bounded: at most 10 network calls in total.
1. `git ls-remote https://github.com/xqy2006/jsc2js refs/heads/main` -> record the commit; it must be 01fc264d22055865a460b322399a15d84b71f5aa or report the drift.
2. GitHub API `https://api.github.com/repos/xqy2006/jsc2js/releases/tags/<tag>` for tags 14.8.178.14, 14.8.178.1 and 14.7.173: record each linux asset's name, size and `digest` field. Compare the digests with the sha256 pins in {TOOL} (PINS: D1 bc70d3c0..., D2 4060ff2e..., D3 c240ffae...) — tarball digests, not binary digests; record both the API digest and `sha256sum` of the local tarball if you find one under {HOME}; otherwise state that the local tarball is not present and do not download d8 binaries (the executor owns that).
3. Count the upstream releases: page through `https://api.github.com/repos/xqy2006/jsc2js/releases?per_page=100&page=N` (N=1..7) and report the total and the distinct tag count. S129 claims 677.
4. Raw README at commit 01fc264d: `https://raw.githubusercontent.com/xqy2006/jsc2js/01fc264d22055865a460b322399a15d84b71f5aa/README.md`. Locate (line numbers) the sentence on matching d8 (the 'matching' / 'MUST' sentence) and the view8 invocation (`python view8.py --disassembled`). Quote each in <=25 words with its line number.
5. Confirm View8 path: `git -C {HOME}/jsc2js-src ls-tree 01fc264d22055865a460b322399a15d84b71f5aa View8/` lists view8.py.
Write findings with a table (claim | command | observed | verdict) to {W1}/ScoutJscRoute/findings.md. Delete your scratch dir.""", "ScoutJscRoute"),

 ("ExecMatrixRun", "executor", f"""Run the frozen R64-C1 instrument ONCE, end to end, with the counting command. Do not edit the instrument or claims.
Command (absolute paths; use `timeout 3600`):
  S={SCRATCH}/ExecMatrixRun; mkdir -p "$S" {W1}/ExecMatrixRun
  timeout 3600 python3 {TOOL} --probe {PROBE} --typora {TYPORA} \\
    --d8-match {HOME}/d8-14.8.178.14 --d8-neighbour {HOME}/d8-14.8.178.1 --d8-cross {HOME}/d8-14.7.173 \\
    --view8-dir {HOME}/jsc2js-src/View8 --python {HOME}/venv/bin/python --node node \\
    --work "$S/matrix" --out {W1}/ExecMatrixRun/matrix-run.json > {W1}/ExecMatrixRun/matrix-run.stdout 2> {W1}/ExecMatrixRun/matrix-run.stderr; echo "exit=$?"
Record: the exit code; runs_matching and runs_total; every mismatch (cell, rep, predicted, observed); the per-run receipts (artifact, build, rep, dump_rc, dump_bytes, view8_out_bytes, label). Also record `sha256sum` of {TOOL} before the run and after it (must be equal). Also keep the per-cell directories' dump.txt and reconstruction.js copies only if each is under 2 MB (cp them to {W1}/ExecMatrixRun/cells/<artifact>-<build>-r<rep>/).
If exit is 2 (pin or input refusal), record the stderr text and stop; do not patch anything. Never re-run the matrix a second time; if you need a second run for a diagnosis, say so in findings and wait for the L1 instead.
Write findings to {W1}/ExecMatrixRun/findings.md (exit, counts, mismatches, labels table, sha256 before/after). Delete the scratch dir {SCRATCH}/ExecMatrixRun before you yield.""", "ExecMatrixRun"),

 ("ExecControlArms", "executor", f"""Run the four control arms of R64-C1 (no d8 real run; the matrix is someone else's job). Scratch {SCRATCH}/ExecControlArms; receipts {W1}/ExecControlArms/.
Arm A — selftest: `python3 {TOOL} --selftest > {W1}/ExecControlArms/selftest.txt; echo exit=$?` (expect CLEAN, exit 0).
Arm B — do-nothing: `python3 {TOOL} --skip-run --out {W1}/ExecControlArms/donothing.json > /dev/null; echo exit=$?` (expect exit 1, runs_matching 0). Compare its bytes with {LANE}/.ufo/waves/round-64/l1/c1-before-donothing.json (cmp; report equal or not).
Arm C — pin refusal on the probe: copy {PROBE} to {SCRATCH}/ExecControlArms/flip.jsc, flip one byte at offset 100 (python: read, xor 0xFF on byte 100, write). Run the matrix with --probe flip.jsc (other arguments exactly as in the counting command, with --work {SCRATCH}/ExecControlArms/work-c and --out {W1}/ExecControlArms/armC.json). Expect exit 2 with 'pin mismatch probe' on stderr and no run created under the work dir (ls must show nothing). Record it.
Arm D — fake-green d8 refused by pin: create {SCRATCH}/ExecControlArms/fakeD1/d8 as an executable sh script that prints `[SharedFunctionInfo]` and exits 0; copy {HOME}/d8-14.8.178.14/snapshot_blob.bin and icudtl.dat into fakeD1; run the matrix with --d8-match {SCRATCH}/ExecControlArms/fakeD1 (other args as in the counting command; work dir {SCRATCH}/ExecControlArms/work-d). Expect exit 2 'pin mismatch d8 D1' on stderr. Record it.
Write {W1}/ExecControlArms/findings.md: arm, command, exit, observed stderr/stdout key line, verdict (as predicted or not). Delete {SCRATCH}/ExecControlArms before you yield.""", "ExecControlArms"),

 ("ExecHeaderTable", "executor", f"""Static, read-only comparison of the V8 code-cache headers of the two artifacts. No d8 execution.
Inputs: {PROBE} and {TYPORA} (sha256 pins a86f6ea0... and 6a0cb7b3...; verify first).
Python (struct, little-endian): for each file, print the first 24 bytes as hex and the six 32-bit words; the word at offset 0 must be 0xc0de06c3 for both. Build a table: word index | probe value | typora value | equal (yes/no). Also state the file sizes and the declared payload length (the word that equals size minus 32 for each file, if any). Mark any interpretation of a word's meaning [INFERENCE] unless you read its name from the V8 source; you have no network for V8 sources, so write only the observed table and the equalities.
Write {W1}/ExecHeaderTable/header-table.md. No scratch needed beyond the output file; if you create any, delete it before yielding.""", "ExecHeaderTable"),

 ("ReviewerMatrix", "reviewer", f"""Review the frozen instrument {TOOL} against the predicate and the plan. Read-only; do not run the matrix (the executor did). You may run `python3 {TOOL} --selftest` and `--skip-run` into your scratch dir.
Check, with line numbers: (1) the sha256 of the instrument is 29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb; (2) PREDICATE string equals the predicate in {CLAIMS} and in {PLAN}; (3) PREDICTED equals the table in {PLAN} ('Frozen predicted labels'); (4) classify_dump, classify_view8, classify_check and norm_rc handle signal deaths and empty output exactly as their docstrings say; (5) verdict() counts 18 cells and treats a missing cell as not-run; (6) check_pins verifies every input and binary before any run; (7) run_matrix never writes outside --work and --out; (8) emit() cannot print a verified verdict on an incomplete run; (9) any path that could report exit 0 without 18 matching runs. Classify each finding blocking or non-blocking, with its line numbers.
Write {W1}/ReviewerMatrix/review.md: findings table (id | line | class | blocking? | evidence), and a verdict line 'instrument-sound' or 'instrument-defective: <ids>'.""", "ReviewerMatrix"),

 ("CriticClaim", "critic", f"""Attack R64-C1 as declared. Read-only. Read {PLAN}, {CLAIMS}, {TOOL}, and the pre-freeze probe receipts in {PREFREEZE}.
Attack list (answer each with evidence): (a) Is the predicate falsifiable by the matrix as built, or can a partial route satisfy it? (b) Can a do-nothing, fake-green or unpinned route reach 18/18? (c) Do the pre-freeze receipts really show the four observed cells (dump-probe.txt: SharedFunctionInfo count; dump-probe-x7.txt: exit 139; dump-typora-x7.err: abort; dump-match.err: the typora abort)? Recount each with grep and report counts. (d) Is 'the route never runs the application' true of the command set? (e) Is the 'not claimed' list complete? Name the single strongest counter-argument to the claim and what observation would falsify it. (f) Is the sourced claim (S264, the jsc2js README, plan section 'Sourced claim') actually supported by the README wording that the plan names? Check the README at commit 01fc264d22055865a460b322399a15d84b71f5aa via `git -C {HOME}/jsc2js-src show 01fc264d22055865a460b322399a15d84b71f5aa:README.md | grep -n -i 'd8\\|matching'`.
Write {W1}/CriticClaim/critique.md: a findings table (id | attack | class | severity blocking/non-blocking | evidence path + command + output line) and a verdict line: 'claim-survives' or 'claim-defective: <ids>'.""", "CriticClaim"),

 ("MutCounter", "mutation-tester", f"""Mutation-test the instrument's classifiers and verdict. Work only on scratch copies: {SCRATCH}/MutCounter/. Never edit {TOOL}.
Create six mutants of {TOOL} (copy, then apply one textual change each, with python str.replace and an assert that the target text occurs exactly once):
 M1: classify_dump returns 'dump-ok' for code 134 (add `if code == 134: return "dump-ok"` before the exit check);
 M2: norm_rc returns rc unchanged (signal deaths reported as negative numbers);
 M3: verdict() accepts matches >= total-1 (ok = matches >= total - 1);
 M4: PREDICTED[('typora','D1')] changed to 'dump-ok|view8-ok|node-pass';
 M5: SFI_RE loosened to rb"SharedFunctionInfo" without brackets;
 M6: classify_check always returns 'node-pass'.
For each mutant run `python3 <mutant> --selftest` and record its exit code and the FAIL lines. A mutant whose selftest still exits 0 is a SURVIVOR (a gap in the instrument's self-test). Also run `python3 <mutant> --skip-run` to confirm the mutant still refuses the do-nothing arm (exit 1).
Write {W1}/MutCounter/mutants.md: table (mutant | change | selftest exit | survived? | do-nothing exit). Delete the scratch dir before yielding.""", "MutCounter"),

 ("MutPins", "mutation-tester", f"""Mutation-test the pin gate check_pins() of {TOOL}. Work only on scratch copies under {SCRATCH}/MutPins/. Never edit the instrument.
Create five mutants (copy, single textual change, assert the target text occurs exactly once):
 P1: remove the D1 snapshot_blob.bin check (the loop over ('snapshot_blob.bin','D1-snapshot') and ('icudtl.dat','D1-icudtl') -> only icudtl);
 P2: remove the view8.py check;
 P3: remove the D3 d8 check (drop 'D3' from the builds dict in check_pins);
 P4: compare only the first 8 hex digits of every pin (sha256_file(p)[:8] != PINS[name][:8] style);
 P5: remove the typora pin check (inputs loop only checks 'probe').
For each mutant, build fixture trees under {SCRATCH}/MutPins/fixtures-<mutant>/ that violate exactly the check the mutant removes (wrong bytes at that path, or the file absent), call check_pins() of the mutant module through importlib with an argparse.Namespace of the right attributes, and record the return value. A mutant that returns None (accepts) for a violated fixture is a SURVIVOR. Also confirm the unmutated instrument returns an error string for each fixture (control).
Write {W1}/MutPins/pins.md: table (mutant | violated fixture | unmutated result | mutant result | survived?). Delete the scratch dir before yielding.""", "MutPins"),

 ("SecDownloads", "sentinel", f"""Provenance and safety audit of the binaries the instrument consumes. Read-only except scratch.
1. Confirm the Electron zip sha256 is 9caeeb15dada37cb3a2d80bf0f5899d175db026a4def11560890bd2f19684909 — locate the zip only if present under ~/.cache/electron or {SCRATCH}/lead; if it is absent, state so and do not download it.
2. For tags 14.8.178.14, 14.8.178.1, 14.7.173: the instrument pins the d8 binaries, not the tarballs. List the contents of each installed tree under {HOME}/d8-<tag>/ (ls -la, file, sha256sum of d8, snapshot_blob.bin, icudtl.dat). Confirm that d8 is an ELF executable (`file`), and that no file is setuid or setgid (`stat -c %a`).
3. Confirm the view8 tree and its single pin: `git -C {HOME}/jsc2js-src ls-tree 01fc264d22055865a460b322399a15d84b71f5aa View8/view8.py` and `sha256sum {HOME}/jsc2js-src/View8/view8.py` (must be b3123e4a...).
4. Grep the instrument and the lane's round-64 tooling for remote-script execution (patterns: `curl` or `wget` piped to `sh`, `bash -c "$(curl`, `eval $(curl`). Report every hit or state zero hits with the command.
5. Confirm the instrument never invokes a shell with a network command: grep for subprocess/shell use in {TOOL}.
6. For the three tags, compare the GitHub API `digest` of the tarball (use `curl -fsS https://api.github.com/repos/xqy2006/jsc2js/releases/tags/<tag>`) with the sha256 of the local tarball only if the tarball is present under {SCRATCH}/lead or {HOME}; otherwise state that the tarball is not present locally.
Write {W1}/SecDownloads/audit.md: a table (check | command | observed | verdict) and a line 'provenance-clean' or 'provenance-open: <ids>'. Delete any scratch you made.""", "SecDownloads"),

 ("ConnectJscCross", "connector", f"""Cross-link and sibling-overlap scan for the `.jsc` / View8 / d8 surface. Read-only.
1. In {LANE}: grep -rn -i -E 'jsc|view8|d8 |bytenode|ignition|v8 ?bytecode|loadjsc' --include='*.md' --include='*.json' --include='*.py' . (exclude .git and .ufo/waves/round-6[0-3]) and report each hit as file:line with a class: own-lane-knowledge, own-lane-skill, own-lane-scorecard, own-lane-tooling, staged-elsewhere, other.
2. In the fleet root /home/vgpnk/Projects/shokunin: grep -rln -i -E 'jsc2js|view8|loadjsc|\\.jsc' --include='*.md' */corpus */SKILL.md */PROVINCE.md 2>/dev/null, excluding kaidoku-shokunin. List each sibling lane and file that touches the same surface, and say which lane owns it by its PROVINCE.md (one line each).
3. For each hit that the lane's PROVINCE.md or LOG says is out of scope (e.g. the 'Adjacent' section on malware/dynamic analysis, gdb, Frida), state the ruling the lane already holds, with file:line.
4. Identify cross-links the lane should add (knowledge entry to SCORECARD planned row, PROVINCE frontier bullet, SKILL capability row). List the exact file and anchor for each; do not edit anything.
Write {W1}/ConnectJscCross/overlap.md with the three tables (own-lane hits, sibling overlap, proposed cross-links) and the one-line verdict 'overlap-declared' or 'no-overlap'.""", "ConnectJscCross"),

 ("ScribeSources", "scribe", f"""Re-ground the two staged jsc2js sources in this round and draft their SOURCES rows. Read-only to the lane; write only your report dir.
Open (each once; record the access date as 2026-11-03, the fetch time, and sha256 of the bytes fetched):
 (a) S264 — jsc2js README at the pinned commit: https://raw.githubusercontent.com/xqy2006/jsc2js/01fc264d22055865a460b322399a15d84b71f5aa/README.md
 (b) S265 — jsc2js releases page (the inventory): https://github.com/xqy2006/jsc2js/releases (fetch with curl; record the byte count and sha256; do not download any release asset).
For each source: a located quote (exact text, <=25 words, with its line number in the fetched bytes and the nearest heading), and the claim it teaches. For S265 also count the release tags on the page or in the API pages (the API total is the instrument's number; cite the command).
Draft SOURCES rows in the 11-column registry schema of {LANE}/CORPUS.md: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`. ids S264 and S265; kind docs; tier A (the tool's own documentation and its own release record, scoped to the tool's contract and its inventory); status mined; opened 2026-11-03; recheck 90d; used-by 'corpus/knowledge/2026-11-03-r64-jsc-route-outcome-matrix.md' (the L1 writes that entry). No '|' inside any cell; use '/' or ';' instead.
Write {W1}/ScribeSources/rows.md (the two rows, verbatim), {W1}/ScribeSources/gate.md (for each source: URL, access date, fetch sha256, located quote, line, heading, decision and limits), and {W1}/ScribeSources/counts.txt (command and output for the release count). No scratch to keep; delete any temp file before yielding.""", "ScribeSources"),

 ("ScribeLesson", "scribe", f"""Draft the round-64 lesson's `## Mistakes` rows and a QUALITY candidate from the evidence already on disk. Read-only to the lane; write only your report dir.
Read: the staged package entry {"/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/jsc-mapper-cli-contract.md"} (read-only), {PREFREEZE}/probe-view8.js, {PREFREEZE}/view8-probe.log, {PREFREEZE}/dump-probe.txt, and {LANE}/corpus/QUALITY.md (last criteria, to find the next free number; the lane's criteria run to #74 at the r63 closure — confirm the highest number with grep -E '^\\| [0-9]+ ').
Mistakes to draft (format: id | class | evidence pointer | captured-by | fix), each evidence pointer resolvable by command:
 M64-1: the staged entry says the mapper output is "approximate JavaScript"; `node --check` rejects the View8 output of the probe (see view8-probe.log and the node-check command). class: stale-premise / scope. captured-by: none (no QUALITY criterion requires an output-validity check on reconstruction claims). fix: a QUALITY criterion (draft text below).
 M64-2: pre-freeze probes ran a d8 without its execute bit (exit 126) and without icudtl.dat (exit 1, ICU init failure) before the route ran; the instrument's pin check verifies bytes, not executability. class: process. captured-by: none. fix: record it; the instrument's selftest does not cover executability (draft a candidate selftest case, do not add it to the frozen instrument).
Draft the QUALITY candidate (next free number N, text in the lane's table style, one sentence, pipe-free): a reconstruction claim (decompiler, disassembler, or view8-class tool) must name its output's syntax class and show a parser verdict on one run.
Write {W1}/ScribeLesson/draft.md: the two mistake rows verbatim (pipe-free cells), the QUALITY candidate row with its number, and for each row the command that demonstrates the evidence pointer. No scratch.""", "ScribeLesson"),
]

def build():
    tasks = []
    for name, role, body, _ in ITEMS:
        prompt = "/skill:godspeed\n\n" + GS + "\n\n" + body
        for token in ("{", "}"):
            pass
        if re.search(r"\{[A-Za-z_][A-Za-z_0-9.]*\}", prompt):
            raise SystemExit(f"unresolved placeholder in {name}")
        tasks.append({"name": name, "role": role, "prompt": prompt})
    spec = {
        "wave": "r64-w1",
        "milestone": "r64-w1 build+attack: frozen R64-C1 matrix run, controls, pins, provenance, source re-grounding, lesson drafts; L1 integrates, re-runs the instrument only as the receipted landing check",
        "reportDir": ".ufo/waves/round-64/w1",
        "context": CONTEXT,
        "items": tasks,
    }
    return spec

if __name__ == '__main__':
    spec = build()
    out = pathlib.Path(LANE + '/.ufo/waves/round-64/r64-w1-spec.json')
    out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print('items', len(spec['items']), 'roles', sorted({i['role'] for i in spec['items']}))
    print('wrote', out)
