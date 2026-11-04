#!/usr/bin/env python3
"""Generate the kaidoku round-66 wave-1 spec (one v1 build+attack wave, 12 seats). R66, KaidokuR66.

Interpolation discipline: LANE/W1 paths are substituted at build time; the rendered items must
contain no unresolved `{...}` placeholders (checked before the spec is written).
"""
import hashlib
import json
import pathlib
import re

GS = open('/home/vgpnk/.agents/skills/godspeed/directive.md').read().strip()
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
W1 = LANE + '/.ufo/waves/round-66/w1'
SCRATCH = '/fast/scratch/hyaku/kaidoku-r66'
TOOL1 = LANE + '/tools/round-66/closure-boundary.py'
TOOL2 = LANE + '/tools/round-66/coverage-selfcheck.py'
V1 = LANE + '/tools/round-65/jsc-closure-matrix.py'
R65C2 = LANE + '/tools/round-65/coverage-recipe.py'
CLAIMS = LANE + '/.ufo/waves/round-66/claims.json'
PLAN = LANE + '/plans/round-66-claims.md'
CONTROLS = LANE + '/.ufo/waves/round-66/l1/controls'
PRE = LANE + '/.ufo/waves/round-66/l1/pre'
ROOT = '/home/vgpnk/.local/share/kaidoku-jsc'
PROBE = LANE + '/.ufo/waves/round-64/inputs/probe-electron.jsc'
BASE = '311079d869f068bc083a8d180977e49634120fdf'
FREEZE = '7b63dd5d5199ed30bc3f213573d8594434a18eb6'
S1 = hashlib.sha256(pathlib.Path(TOOL1).read_bytes()).hexdigest()
S2 = hashlib.sha256(pathlib.Path(TOOL2).read_bytes()).hexdigest()

PREDICATE1 = ("R66-C1 is verified iff the repaired closure counter passes all five of its "
              "boundary arms: a1 the guarded fixture probe leaves closure.ok true with an "
              "empty cache; a2 the same probe without -B or the bytecode env makes "
              "closure.ok false and names a .pyc path; a3 the frozen 30-entry toolchain "
              "manifest verifies with count_ok true; a4 a manifest one entry short reports "
              "entries 29 != 30 and closure.ok false; a5 --skip-run emits no closure object "
              "claiming ok.")
PREDICATE2 = ("R66-C2 is verified iff the coverage self-check counter at the measured "
              "revision reports recipe_a_equivalent true, a non-empty recipe_a_hidden list, "
              "and mismatches 0 across its two self-assessment atoms, where at the base "
              "revision the same counter reports the cited fraction atom as a mismatch.")

CONTEXT = f"""# Target
kaidoku-shokunin round 66, attempt 1, wave w1 = the single v1 build+attack wave (12 seats; policy
band 8-16; attack seats reviewer, critic, two mutation-testers = 4 of 12). Base {BASE}; operative
freeze {FREEZE}. Two declared claims (plan {PLAN}; container {CLAIMS}):
- R66-C1 (depth, counter repair) executes the r65 closure's routed defect 2 (M65-5): the closure
  counter's post-probe cache check, the frozen count assertion and the `--skip-run` closure claim.
  Predicate, verbatim: "{PREDICATE1}"
- R66-C2 (calibration, counter repair) executes the r65 closure's routed defect 1 (M65-2/M65-4):
  recipe A verbatim, the hidden-file LIST, and the self-assessment atom mismatch count.
  Predicate, verbatim: "{PREDICATE2}"

# Frozen inputs (read-only; NEVER edit)
- {TOOL1} (sha256 {S1}) - R66-C1 counter. Loads {V1} by path under its sha256 pin
  (79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6) and re-hosts its CLOSURE,
  cache_entries and census in an ordered check. Modes: --verify, --manifest, --skip-run, --selftest.
- {TOOL2} (sha256 {S2}) - R66-C2 counter. Modes: --recipe a, --recipe stem, --equiv, --selfcheck,
  --selftest. `--equiv` extracts the SCORECARD recipe-A heredoc at --rev and re-runs it.
- {V1}, {R65C2} - the round-65 instruments, FROZEN: a defect is reported, never patched.
- Before-arm receipts: {CONTROLS}/c1-do-nothing.json (1 of 5 arms), {CONTROLS}/c2-do-nothing.json
  (0 of 3 conditions); pre-freeze dry runs {PRE}/dryrun-c1-verify.json (5 of 5) and
  {PRE}/dryrun-c2-selfcheck-at-base.json (equivalent true, hidden 3, mismatches 1).
- Toolchain root {ROOT} (read-only; copy with `cp -a --reflink=auto` if you need a mutable one):
  three d8 builds with snapshot_blob.bin and icudtl.dat, jsc2js-src/View8, venv (parse 1.22.4),
  inputs/atom.compiled.dist.jsc. Its dedicated interpreter is {ROOT}/venv/bin/python. The tree is
  cache-free; nothing may write into it.

# Shared rules (bind every seat)
- Scratch: every clone, copy, fixture and work tree lives under {SCRATCH}/<your-seat-name>/ created
  with mkdir -p and passed explicitly (TMPDIR, --work, --out). /tmp is for files under 50 MB only.
  Delete your scratch dir before you yield (trap 'rm -rf -- "$S"' EXIT in shell; shutil.rmtree in
  python). Check /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status before a heavy pass.
- Write only inside your own report directory {W1}/<your-seat-name>/ (absolute path). Every `Report:`
  trailer path is relative to {LANE} - write it at {LANE}/<that path>.
- Never run git/jj mutating commands (add, commit, stash, checkout, reset, pull, push, and no jj
  commit/new/describe/bookmark). Read-only git (log, show, diff, status, ls-files, rev-parse,
  ls-tree, ls-remote) is fine as `git -C {LANE} ...`. Never run git status inside {ROOT}/jsc2js-src.
- Never touch the fleet root, MANIFEST.json, .ufo/state/, .ufo/watchdog.log, sibling lane repos
  (read-only grep only), {ROOT} itself, or /home/vgpnk/Projects/shokuknow (read-only; never run its
  tools). Never message agent://all; the L1 reads the files you write.
- Network: only the URLs your task names. Never pipe a remote script into a shell. Official sources only.
- Tooling authorization (operator, 2026-10-19; /home/vgpnk/.omp/agent/RULES.md): you may install or
  upgrade tools that help your task through official channels, recording tool, version, channel and
  reason in your report. pacman is PAUSED host-wide: never run pacman, -Sy, -Syu, -U, -R or any
  partial upgrade; use uv tool / npx / an official binary in ~/.local/bin.
- Use absolute paths for every read, write and edit. Do not poll; run each command once, read its
  output, act. Keep your final yield short: findings with evidence pointers (path, command, exit
  code, sha256). Report only what you ran.
"""

ITEMS = [
    ("ExecClosure", "executor", f"""Run the frozen R66-C1 counter ONCE end to end and record its receipts. Do not edit it.
  S={SCRATCH}/ExecClosure; mkdir -p "$S" {W1}/ExecClosure
  sha256sum {TOOL1} > {W1}/ExecClosure/instrument-before.txt
  TMPDIR=$S timeout 2400 python3 -I -B {TOOL1} --verify --repo {LANE} \\
    --toolchain-root {ROOT} --probe {PROBE} --work "$S/work" \\
    --out {W1}/ExecClosure/verify.json > {W1}/ExecClosure/verify.stdout 2> {W1}/ExecClosure/verify.stderr; echo "exit=$?"
  TMPDIR=$S timeout 900 python3 -I -B {TOOL1} --manifest --repo {LANE} --toolchain-root {ROOT} \\
    --probe {PROBE} --out {W1}/ExecClosure/manifest.json > {W1}/ExecClosure/manifest.stdout 2>&1; echo "exit=$?"
  TMPDIR=$S python3 -I -B {TOOL1} --skip-run --repo {LANE} --out {W1}/ExecClosure/skiprun.json > /dev/null 2>&1; echo "exit=$?"
  sha256sum {TOOL1} > {W1}/ExecClosure/instrument-after.txt
  find {ROOT} -name '__pycache__' -o -name '*.pyc' | sort > {W1}/ExecClosure/toolchain-cache-after.txt; wc -l < {W1}/ExecClosure/toolchain-cache-after.txt
Write {W1}/ExecClosure/findings.md: the --verify exit, the per-arm table (arm, passed, the detail keys
that carry the decision), the manifest receipt's entries/count_ok/ok and probe message, the skip-run
receipt's closure and closure_claimed, the instrument sha256 before/after (must be equal), and the
toolchain cache line count (must be 0). Never re-run: if an exit is 2, record stderr and stop. Delete
{SCRATCH}/ExecClosure before you yield.""", "ExecClosure"),

    ("ExecCoverage", "executor", f"""Run the frozen R66-C2 counter arms ONCE and record them. Do not edit it.
  S={SCRATCH}/ExecCoverage; mkdir -p "$S" {W1}/ExecCoverage
  sha256sum {TOOL2} > {W1}/ExecCoverage/instrument-before.txt
  TMPDIR=$S T={W1}/ExecCoverage
  python3 -I -B {TOOL2} --selfcheck --root {LANE} --rev {FREEZE} --work "$S/w1" --out $T/selfcheck-at-freeze.json > $T/selfcheck-at-freeze.stdout 2>&1; echo "exit=$?"
  python3 -I -B {TOOL2} --selfcheck --root {LANE} --rev {BASE} --work "$S/w2" --out $T/selfcheck-at-base.json > $T/selfcheck-at-base.stdout 2>&1; echo "exit=$?"
  python3 -I -B {TOOL2} --recipe a --root {LANE} --rev {BASE} --work "$S/w3" --out $T/recipe-a-at-base.json > $T/recipe-a-at-base.stdout 2>&1; echo "exit=$?"
  python3 -I -B {TOOL2} --recipe stem --root {LANE} --rev {BASE} --work "$S/w4" --out $T/recipe-stem-at-base.json > $T/recipe-stem-at-base.stdout 2>&1; echo "exit=$?"
  python3 -I -B {TOOL2} --equiv --root {LANE} --rev {BASE} --work "$S/w5" --out $T/equiv-at-base.json > $T/equiv-at-base.stdout 2>&1; echo "exit=$?"
  sha256sum {TOOL2} > {W1}/ExecCoverage/instrument-after.txt
Independently re-derive three numbers from git objects at {BASE} and record the commands: the knowledge
file count (`git -C {LANE} ls-tree -r --name-only {BASE} -- corpus/knowledge | grep -c '\\.md$'`), the
recipe-A missing list (the three non-October names), and the coverage row's cited fraction (the first
'<n>/<n> knowledge files' in the '## Owned axes' coverage row). Write {W1}/ExecCoverage/findings.md:
each exit, the atoms with claimed vs observed, recipe_a_hidden, recipe_a_equivalent, the diffs object,
and whether the two independent counts equal the counter's. Delete {SCRATCH}/ExecCoverage before you yield.""", "ExecCoverage"),

    ("ExecControls", "executor", f"""Re-run BOTH committed do-nothing controls and add three fail-ability arms. Scratch
{SCRATCH}/ExecControls; receipts {W1}/ExecControls/.
 1. `TMPDIR=$S python3 -I -B {CONTROLS}/c1-do-nothing.py --repo {LANE} --out {W1}/ExecControls/c1-do-nothing.json; echo exit=$?`
    Compare its passed/arms_total with the committed {CONTROLS}/c1-do-nothing.json (expect 1/5, ok false).
 2. `TMPDIR=$S python3 -I -B {CONTROLS}/c2-do-nothing.py --repo {LANE} --rev {BASE} --out {W1}/ExecControls/c2-do-nothing.json; echo exit=$?`
    Compare with the committed receipt (expect 0/3, ok false).
 3. Arm-mutation A (the count assertion must be load-bearing): copy {TOOL1} into $S/m1.py, change
    `COUNT = 30` to `COUNT = 29`, keep the r65 pin load, and run `--verify` with the copy; record which
    arm flips and the exit code.
 4. Arm-mutation B (the ordering must be load-bearing): in a second copy $S/m2.py move the
    `post_cache = mod.cache_entries(root)` line to before the `probe_ok, probe_msg = probe_fn()` line
    and use the moved value in the `ok` expression; run `--verify` with the copy; record which arm flips.
 5. Arm-mutation C (skip-run must stay honest): in a third copy $S/m3.py make `skip_run_receipt`
    return `{{"closure": {{"ok": True, "entries": 30}}, "closure_claimed": True}}` plus the other keys;
    run `--skip-run` and `--verify` with the copy; record the a5 result.
Write {W1}/ExecControls/findings.md: each arm's command, exit, the flipped arm name and one-line verdict;
state plainly that a mutation which does NOT flip its arm is a counter defect to report, not to fix.
Delete {SCRATCH}/ExecControls before you yield.""".replace("{{", "{").replace("}}", "}"), "ExecControls"),

    ("ReviewerClosure", "reviewer", f"""Read-only code review of the two frozen counters against the two frozen predicates.
Read in full: {TOOL1}, {TOOL2}, {PLAN}, {CLAIMS}, and the receipts under {PRE}/ and {CONTROLS}/.
Deliver {W1}/ReviewerClosure/review.md with:
 1. A clause-to-line trace table per claim: every clause of the predicate (R66-C1 a1..a5; R66-C2
    recipe_a_equivalent, recipe_a_hidden non-empty, mismatches 0, the base arm) → the exact function
    and line range that evaluates it (QUALITY #87). Name any clause with no implementing line.
 2. Boundary hunt: can any arm pass without its defect present? Try to name a concrete input or a code
    path (fixture, manifest, revision) that satisfies the arm while the defect it guards is absent.
 3. QUALITY #68 check: is the predicate sentence byte-identical in the plan, the container, each
    counter's PREDICATE constant and the receipts? Quote the sha256 of each predicate site.
 4. QUALITY #83/#84 check: was the pre-freeze dry run the frozen counter itself on data of the frozen
    shape, and does every binding in the receipts name the field it reads?
 5. The r65 residuals the closure routed (A1/A3/A5 of its reviewer) — are they disposed of, or still open?
 6. Findings list F1..Fn with severity (blocking / advisory), each with a path:line pointer.
Do not edit the counters or any lane file outside your report dir. No scratch needed beyond $S.""", "ReviewerClosure"),

    ("CriticClaims", "critic", f"""Falsify the two claims by attack, not by re-reading. Read {PLAN}, {CLAIMS}, the two counters,
and the committed receipts. Try, each in scratch under {SCRATCH}/CriticClaims with its own receipt:
 A. C1 shortcut: build the cheapest counter that passes all five arms WITHOUT an ordered post-probe
    check — e.g. a counter whose a2 arm plants a `.pyc` after the probe instead of letting the probe
    write it. If the frozen arms cannot distinguish the two, say so with the diff.
 B. C1 escape: does any arm depend on a value the frozen counter itself writes rather than reads?
 C. C2 equivalence escape: can `recipe_a_equivalent` be true while `--recipe a` disagrees with the
    SCORECARD block in a key outside RECIPE_A_KEYS? Name the key and its consequence.
 D. C2 atom escape: can `mismatches == 0` be reached without repairing the self-assessment row — e.g.
    by a row shape the parser reads as equal? Construct the row text and score it with the counter.
 E. The base-arm honesty: run `--selfcheck --rev {BASE}` and confirm the A2 atom is false for the
    stated reason (claimed 142/142 vs observed 145/145), not for a parse failure.
Write {W1}/CriticClaims/attacks.md: one section per attack, each with the command, the exit, the
observed values and a verdict (counter holds / counter fails / could-not-evaluate). Report a failed
attack as evidence the claim holds; never soften a real escape. Scratch deleted before yield.""".replace("{BASE}", BASE), "CriticClaims"),

    ("MutClosure", "mutation-tester", f"""Mutation-test the R66-C1 counter. Work only in scratch copies under {SCRATCH}/MutClosure;
never edit {TOOL1}. Five mutants (each a separate copy under $S/mut/), scored by BOTH `--selftest` and
`--verify`:
 M1 move the post-probe `cache_entries` scan before the probe call (the C1-F1 defect reintroduced);
 M2 delete the `count_ok` term from the `ok` expression (the C1-F2 defect reintroduced);
 M3 make `skip_run_receipt` carry a synthetic `closure` with `ok: True` and `closure_claimed: True`;
 M4 force `fixture_probe` to always pass `-B` and the bytecode env (a2 becomes unreachable);
 M5 make `arm()` return `passed: True` unconditionally (the whole battery becomes vacuous).
For each: the mutant's file diff (unified, ≤40 lines), `--selftest` exit and the `SELFTEST` summary line,
`--verify` exit and the passed count, and the verdict killed / survived. A survivor is a finding: name
the line the selftest fails to bind. Write {W1}/MutClosure/mutants.md with the table plus one line per
mutant naming which arm or selftest case kills it. Delete {SCRATCH}/MutClosure before yield.""", "MutClosure"),

    ("MutCoverage", "mutation-tester", f"""Mutation-test the R66-C2 counter. Work only in scratch copies under {SCRATCH}/MutCoverage;
never edit {TOOL2}. Five mutants, scored by `--selftest` and by `--selfcheck --rev {BASE}`:
 M1 `recipe_hidden` returns `[]`; M2 `recipe_a_equivalence` returns true without running the block;
 M3 drop the A2 atom from the atoms list; M4 `parse_row` returns the observed fraction (a tautology);
 M5 `mismatches` computed as a constant 0.
For each: the diff, the selftest exit and summary line, the `--selfcheck` exit, mismatches and the
recipe_a_hidden count, and the verdict killed / survived. Name the arm or case that kills each mutant;
a survivor is a finding with the unbound line named. Write {W1}/MutCoverage/mutants.md. Delete
{SCRATCH}/MutCoverage before yield.""".replace("{BASE}", BASE), "MutCoverage"),

    ("SentinelScope", "sentinel", f"""Scope, secret and provenance audit of round 66's landed bytes so far. Read-only over the lane.
Check and receipt each into {W1}/SentinelScope/audit.md:
 1. Write scope: list every path the round's commits b5b02e1f, 78fa9666, 7b63dd5d add or change
    (`git -C {LANE} diff-tree --no-commit-id --name-status -r -z` per commit, or `git show --stat`).
    Flag any path outside {LANE}, and any path in the fleet root.
 2. Secret material: scan the round's new and changed files for credential shapes (private-key
    headers, `op://`, bearer/token assignments, cookie jars, 32+ char hex secrets that are NOT
    sha256 pins of named files). Name each hit with path:line; state the sweep command.
 3. Toolchain integrity: re-derive the closure manifest read-only with
    `TMPDIR=$S python3 -I -B {V1} --manifest --toolchain-root {ROOT} --probe {PROBE}` (expect exit 0,
    entries 30, cache empty) and count the toolchain files (`find {ROOT} -type f -not -path '*/.git/*' | wc -l`).
    Compare with the r65 freeze count 105 and explain any delta.
 4. Frozen-path integrity: for each path in `frozen_paths` of {CLAIMS}, confirm the blob at {FREEZE}
    equals the blob at the lane tip (`git -C {LANE} rev-parse {FREEZE}:<path>` vs `<branch>:<path>`).
 5. Registry rows: confirm the two SKILL.md rows for tools/round-66 exist at the tip, carry 7 cells and
    no escaped pipe (`grep -c '|' ` per row), and name a verdict map with 0/1/2.
Write the audit with a verdict line per item (clean / finding with reason). No lane edits. Delete $S.""".replace("{FREEZE}", FREEZE).replace("{BASE}", BASE), "SentinelScope"),

    ("ScoutSources", "scout", f"""Open the round's source and produce the SOURCES row evidence. Work in {SCRATCH}/ScoutSources;
write {W1}/ScoutSources/.
 1. Fetch https://docs.python.org/3/library/sys.html ONCE into $S/sys.html (`curl -fsSL -o`); record
    byte count, sha256, HTTP status and the UTC instant.
 2. Locate the `sys.dont_write_bytecode` entry: the nearest preceding <h1>-<h6> heading, the line
    number of the definition, and the sentence that names the PYTHONDONTWRITEBYTECODE environment
    variable. Quote it verbatim (record the word count; the row's Gate quote must be ≤25 words).
 3. Decide the row: kind `docs`, tier `A` or `B` with the CORPUS.md category named in one phrase, scope
    = exactly what the page states about the flag and the variable (never "the interpreter writes no
    bytecode"), teaches = one grounded learner benefit, recheck = a cadence.
 4. Draft the row in the registry's 11-column shape (pipe-free cells, no escaped pipes) as
    {W1}/ScoutSources/row.md, with the Gate block: URL, access date 2026-11-03, quote and locator.
 5. Second candidate + reject: find the page or section that documents `-B` (cmdline.html) and state
    why it is NOT the row for this scope (round 65 already holds S266 for the switch); record it as the
    rejected alternative with its flip condition.
 6. Measure the registry before-state: `grep -cE '^\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|' {LANE}/corpus/SOURCES.md`,
    the next free S-id, and `ls {LANE}/considerthese 2>&1` (expected absent). Also `ls /home/vgpnk/Projects/shokuknow/merge/kaidoku/`
    and quote MERGE-REPORT.md's heading list (read-only) so the report can state assimilation status.
Delete {SCRATCH}/ScoutSources before yield.""".replace("{{", "{").replace("}}", "}"), "ScoutSources"),

    ("ConnectorCross", "connector", f"""Sibling-overlap scan for round 66's two counter surfaces. Read-only.
Question: does another shokunin lane already own (a) a reproduction of a lane's superseded measurement
recipe, (b) a closure-count assertion gate, or (c) a self-assessment atom/mismatch counter?
 1. `grep -rIl --include='*.py' -e 'dont_write_bytecode' -e 'closure' -e 'count_ok' -e 'mismatches' /home/vgpnk/Projects/shokunin/*-shokunin/tools /home/vgpnk/Projects/shokunin/*-shokunin/scripts 2>/dev/null | sort`
    and narrow to the closest matches; read the top 3 hits' docstrings only.
 2. Check the lanes named in earlier kaidoku rounds: souji (coverage-agreement instrument), kumitate
    (registry/validator), tameshi (batteries). For each, one line: what it holds, whether round 66's
    counters duplicate, extend or merely neighbour it.
 3. Name the ownership boundary: which of the three surfaces is kaidoku's own, which is shared, and
    what should be reported to the owning lane rather than absorbed.
Write {W1}/ConnectorCross/overlap.md with the search commands, the hit list, and the boundary verdict.
Read-only: never edit a sibling repo. Delete $S.""", "ConnectorCross"),

    ("ScribeKnowledge", "scribe", f"""Draft the round's knowledge entry and its coverage-map row (prose only; the L1 lands them).
Read: {PLAN} clause A8, {TOOL1}, {TOOL2}, {PRE}/dryrun-c1-verify.json, {CONTROLS}/c1-do-nothing.json,
{W1}/ScoutSources/row.md when it exists (poll once with `ls`, do not loop), and
{LANE}/corpus/knowledge/2026-11-03-r65-jsc-closure-matrix.md for the house shape.
Write {W1}/ScribeKnowledge/entry.md: a `corpus/knowledge/2026-11-03-r66-closure-boundary.md` body with
 - the provenance trio first (`source:`, `verified-at:`, `recheck:`), the source citing the new S-row id
   as `S<nnn>` (take the id from the scout's row draft; if it is absent, write `S???` and say why);
 - what the two counters now decide, each claim clause mapped to the emitted field;
 - the five C1 arms and the three C2 conditions as two short tables;
 - the measured numbers at the base and at the freeze, each with its receipt path;
 - a `## Limits` list: what the counters do not check (fixture-only ordering proof, the stem recipe's
   bare-token limit, the `--equiv` subprocess cost).
Also write {W1}/ScribeKnowledge/map-row.md: the exact `corpus/README.md` coverage-map row text that adds
this entry (one table row, pipe-free, naming `2026-11-03-r66-closure-boundary`), and
{W1}/ScribeKnowledge/erratum.md: the r65 entry erratum the closure routed (its per-group table says
"venv identity 4" where the pinned map holds 5; the probe is counted under both artifacts and harness) —
appended-correction wording only, never a rewrite instruction. No scratch beyond $S.""", "ScribeKnowledge"),

    ("ScribeLesson", "scribe", f"""Draft the round lesson and the QUALITY rows (prose only; the L1 lands them).
Read {PLAN} (both claims and the frontier step), {CONTROLS}/c1-do-nothing.json, {CONTROLS}/c2-do-nothing.json,
{PRE}/dryrun-c2-selfcheck-at-base.json, and {LANE}/corpus/lessons/round-65.md for the house shape
(Gate table, `## Mistakes` table with class / evidence pointer / captured-by / fix, Outcome, Census).
Write {W1}/ScribeLesson/draft.md with:
 1. `## Gate` — candidates considered this round: (a) the sys.dont_write_bytecode page (admit, per the
    scout's row), (b) the cmdline.html `-B` section (reject as this round's row: S266 already holds it),
    (c) the r65 instrument's `--recipe date` mode as "recipe A" (reject: measured field difference),
    (d) a 30-vs-29 count fixture as evidence of the count assertion (reject: fixture, not a source).
    Each entry: row id or reason, flip condition for rejects.
 2. `## Mistakes` — at least three rows with the real classes and pointers:
    M66-1 the r65 counter's pre-probe cache order (class stale-premise/boundary; evidence
    {CONTROLS}/c1-do-nothing.json a2 block; captured-by QUALITY #87 plus the r65 closure's routed defect;
    fix = the ordered post-probe scan, shown red by the control and green by the a2 arm).
    M66-2 the integer-only "names" clause (class scope; evidence the r65 receipt and the new
    recipe_a_hidden list; captured-by QUALITY #87; fix = the emitted list).
    M66-3 (this round's own) the first C1 control run reused one fixture for both the arm and the
    r65-order emulation, so the pre-probe scan saw the cache the arm probe had just written and the
    control falsely "met" the a2 arm; class vacuous/control-contamination; captured-by the control's own
    detail dump showing `cache_present` before the probe; fix = two separate fixtures per arm, shown by
    the corrected control receipt (1/5).
    Add any further real mistake you can evidence.
 3. `## Outcome` — a factual paragraph per claim with its receipt path, and the honest statement that
    the outside non-author closure is still pending.
 4. Three QUALITY row drafts (#104..#106) in the lane's table style: (i) an ordered check's LAST step
    must be the one that proves no write happened; (ii) a frozen count must be asserted, not emitted;
    (iii) a control that reuses state between arms has scored nothing.
No scratch beyond $S.""".replace("{PRE}", PRE), "ScribeLesson"),
]


def build():
    tasks = []
    for name, role, body, _ in ITEMS:
        prompt = "/skill:godspeed\n\n" + GS + "\n\n" + body
        if re.search(r"\{[A-Za-z_][A-Za-z_0-9.]*\}", prompt):
            raise SystemExit(f"unresolved placeholder in {name}")
        tasks.append({"name": name, "role": role, "prompt": prompt})
    return {
        "wave": "r66-w1",
        "milestone": "r66-w1 build+attack: the two repaired frozen counters run end to end, their controls and mutants, the clause-to-line review and claim attacks, the source row and the prose drafts.",
        "reportDir": ".ufo/waves/round-66/w1",
        "context": CONTEXT,
        "items": tasks,
    }


if __name__ == '__main__':
    spec = build()
    out = pathlib.Path(LANE + '/.ufo/waves/round-66/r66-w1-spec.json')
    out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print('items', len(spec['items']), 'roles', sorted({i['role'] for i in spec['items']}))
    print('wrote', out)
