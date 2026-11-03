#!/usr/bin/env python3
"""Generate the kaidoku round-65 wave-1 spec (one v1 build+attack wave, 12 seats). R65, KaidokuR65.

Interpolation discipline: LANE/W1 paths are substituted at build time; the rendered
items must contain no unresolved `{...}` placeholders (checked before the spec is written).
"""
import hashlib
import json
import pathlib
import re

GS = open('/home/vgpnk/.agents/skills/godspeed/directive.md').read().strip()
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
W1 = LANE + '/.ufo/waves/round-65/w1'
SCRATCH = '/fast/scratch/hyaku/kaidoku-r65'
TOOL1 = LANE + '/tools/round-65/jsc-closure-matrix.py'
TOOL2 = LANE + '/tools/round-65/coverage-recipe.py'
CLAIMS = LANE + '/.ufo/waves/round-65/claims.json'
PLAN = LANE + '/plans/round-65-claims.md'
ROOT = '/home/vgpnk/.local/share/kaidoku-jsc'
PROBE = LANE + '/.ufo/waves/round-64/inputs/probe-electron.jsc'
BASE = 'c99e907cb5576c13a7b22755d776b356fdfc1752'


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


S1 = sha(TOOL1)
S2 = sha(TOOL2)

PREDICATE1 = ("R65-C1 is verified iff (i) the frozen closure manifest matches every one of its "
              "entries (count and sha256) with no Python bytecode cache present before the first "
              "run, (ii) all 18 runs reproduce the frozen predicted label of their cell "
              "(dump|view8|check), and (iii) the after-run toolchain census equals the before-run census.")
PREDICATE2 = ("R65-C2 is verified iff the repaired stem-keyed recipe reports, over the repository at "
              "the measured revision, `mismatches == 0` with `mapped > 0`, while the superseded "
              "date-limited recipe on the same revision reports a non-zero `population_dropped` "
              "naming the files it hides.")

CONTEXT = f"""# Target
kaidoku-shokunin round 65, attempt 1, wave w1 = the single v1 build+attack wave (12 seats; policy band
8-16; attack seats reviewer, critic, two mutation-testers = 4 of 12). Base {BASE}. Two declared claims
(plan {PLAN}; container {CLAIMS}):
- R65-C1 (depth, capability acquisition) repairs round 64's honest stop: complete closure pins for the
  `.jsc` route matrix, cache-free start, bytecode writes disabled, census before/after, then the same
  18-run matrix. Predicate, verbatim: "{PREDICATE1}"
- R65-C2 (calibration, capability) repairs the coverage recipe that derived its denominator from the
  same date filter as its numerator. Predicate, verbatim: "{PREDICATE2}"

# Frozen inputs (read-only; NEVER edit)
- {TOOL1} (sha256 {S1}) - closure manifest CLOSURE (27 toolchain entries + probe + node + interpreter),
  PREDICTED labels (unchanged from round 64), census, verdict. Frozen bytes; a defect is reported, never patched.
- {TOOL2} (sha256 {S2}) - coverage recipes `stem` and `date`; frozen bytes.
- {PROBE} (sha256 a86f6ea0...) - the Electron 42.2.0 probe code cache.
- Toolchain root {ROOT} (read-only except scratch copies): three d8 builds with snapshot_blob.bin and
  icudtl.dat, jsc2js-src/View8, venv (parse 1.22.4), inputs/atom.compiled.dist.jsc.
  The tree was cleaned of round-64 `__pycache__` files before the freeze (prep receipt
  {LANE}/.ufo/waves/round-65/prep/precache-dirs.txt); it must stay cache-free.

# Shared rules (bind every seat)
- Scratch: every clone, copy, dump, work tree and fixture lives under {SCRATCH}/<your-seat-name>/ created
  with mkdir -p and passed explicitly (TMPDIR, --work). /tmp is for files under 50 MB only. Delete your
  scratch dir before you yield (trap 'rm -rf -- "$S"' EXIT in shell). Check
  /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status before a heavy pass.
- Write only inside your own report directory {W1}/<your-seat-name>/ (absolute path). Every `Report:`
  trailer path is relative to {LANE} - write it at {LANE}/<that path>.
- Never run git/jj mutating commands (add, commit, stash, checkout, reset, pull, push, jj commit/new/
  describe/bookmark). Read-only git (log, show, diff, status, ls-files, rev-parse, ls-remote, ls-tree) is fine
  with `git -C {LANE} ...`. Never run git status inside {ROOT}/jsc2js-src (it can refresh that repo's index,
  which the census excludes but the closure still treats as non-input).
- Never touch the fleet root, MANIFEST.json, .ufo/state/, .ufo/watchdog.log, sibling lane repos (read-only
  grep only), {ROOT} itself (read-only; write only under scratch copies you make), or
  /home/vgpnk/Projects/shokuknow (read-only; never run its tools).
- Network: only the URLs your task names. Never pipe a remote script into a shell. Official sources only.
- Tooling authorization (operator, 2026-10-19; /home/vgpnk/.omp/agent/RULES.md): you may install or upgrade
  tools that help your task through official channels, recording tool, version, channel and reason. pacman
  is PAUSED host-wide: never run pacman, -Sy, -Syu, -U, -R or a partial upgrade.
- Use absolute paths for every read, write and edit. Do not poll; run each command once, read its output, act.
- Never message agent://all; the L1 reads the files you write. Keep your final yield short: findings with
  evidence pointers (paths, command, exit code, sha256). Report only what you ran.
"""

ITEMS = [
    ("ExecMatrix", "executor", f"""Run the frozen R65-C1 instrument ONCE, end to end, with the counting command. Do not edit it.
Command:
  S={SCRATCH}/ExecMatrix; mkdir -p "$S" {W1}/ExecMatrix
  sha256sum {TOOL1} > {W1}/ExecMatrix/instrument-before.txt
  TMPDIR=$S timeout 3000 python3 -I -B {TOOL1} --probe {PROBE} --work "$S/cells" \\
    --out {W1}/ExecMatrix/matrix-run.json > {W1}/ExecMatrix/matrix-run.stdout 2> {W1}/ExecMatrix/matrix-run.stderr; echo "exit=$?"
  sha256sum {TOOL1} > {W1}/ExecMatrix/instrument-after.txt
  find {ROOT} -name '__pycache__' -o -name '*.pyc' | sort > {W1}/ExecMatrix/cache-after.txt; wc -l < {W1}/ExecMatrix/cache-after.txt
Record in {W1}/ExecMatrix/findings.md: the exit code; runs_matching/runs_total; every mismatch; closure entries
and findings; the census delta (added/removed/changed); the label histogram; the cache-after line count (must be 0);
instrument sha256 before/after (must be equal). Copy each cell's reconstruction.js and dump.txt into
{W1}/ExecMatrix/cells/<artifact>-<build>-r<rep>/ only if each is under 2 MB. Never re-run the matrix: if the exit
is 2, record stderr and stop. Delete the scratch dir {SCRATCH}/ExecMatrix before you yield.""", "ExecMatrix"),

    ("ExecControls", "executor", f"""Run the R65-C1 control arms (no full matrix run; the executor owns that). Scratch {SCRATCH}/ExecControls;
receipts {W1}/ExecControls/.
 A - selftest: `python3 -I -B {TOOL1} --selftest > {W1}/ExecControls/selftest.txt 2>&1; echo exit=$?` (expect CLEAN, exit 0, 34 cases).
 B - do-nothing: `python3 -I -B {TOOL1} --skip-run --out {W1}/ExecControls/donothing.json > /dev/null 2>&1; echo exit=$?`
     (expect exit 1, runs_matching 0). cmp its bytes with {LANE}/.ufo/waves/round-65/l1/c1-before-donothing.json and report equal/not.
 C - pin mutation: `cp -a --reflink=auto {ROOT} $S/tc` then flip one byte of `$S/tc/d8-14.8.178.1/snapshot_blob.bin`
     (`printf '\\x00' | dd of=... bs=1 seek=100 conv=notrunc`), then
     `python3 -I -B {TOOL1} --manifest --toolchain-root "$S/tc" --probe {PROBE} --node /home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin/node
      --python /home/vgpnk/.local/share/kaidoku-jsc/venv/bin/python > {W1}/ExecControls/pin-mutation.json 2>&1; echo exit=$?`
     (expect exit 2 naming `d8-14.8.178.1/snapshot_blob.bin`). Do NOT run the matrix on the mutated copy.
 D - cache control: in a second copy `$S/tc2`, create `$S/tc2/jsc2js-src/View8/__pycache__/x.pyc` (empty file) and run the
     same --manifest (expect exit 2 naming the cache). Remove it; re-run (expect exit 0).
 E - census arms: `python3 -I -B {TOOL1} --census {W1}/ExecControls/census-a.json --toolchain-root "$S/tc3"` on a small
     scratch tree you create with two files; census again to `census-b.json` (compare exit 0); add a file; census to
     `census-c.json`; `--compare census-a census-c` (expect exit 1 naming the added path).
Write {W1}/ExecControls/findings.md with each arm's command, exit and one-line verdict. Delete {SCRATCH}/ExecControls.""", "ExecControls"),

    ("ExecCoverage", "executor", f"""Run the R65-C2 before/after arms and controls with the frozen coverage instrument. Do not edit it.
Scratch {SCRATCH}/ExecCoverage; receipts {W1}/ExecCoverage/.
 1. selftest: `python3 -I -B {TOOL2} --selftest > {W1}/ExecCoverage/selftest.txt 2>&1; echo exit=$?` (expect CLEAN, exit 0, 28 cases).
 2. before arm at the base: `python3 -I -B {TOOL2} --root {LANE} --rev {BASE} --recipe date --out {W1}/ExecCoverage/c2-before-date.json`
    (expect exit 1: population_dropped 2, mismatches 2).
 3. after arm at the same base: `--recipe stem --out {W1}/ExecCoverage/c2-after-stem.json` (expect exit 0, mapped 144, mismatches 0).
 4. historical control at the r63 landing `df727606`: both recipes (expect both clean: the defect is invisible before
    the November names exist) - record both.
 5. red arm: a scratch clone `git clone --shared {LANE} $S/lane` at `--rev` = that clone's tip; delete one knowledge
    file's map token from the clone's README and commit it there (fixture repo rules: every git call names -C "$S/lane";
    author identity only inside the clone), then run `--recipe stem` against the clone (expect exit 1 naming the file).
    Never commit in {LANE}.
Write {W1}/ExecCoverage/findings.md: each command, exit, the JSON numbers (knowledge_files, population, mapped,
population_dropped, mismatches, missing/dangling lists). Delete {SCRATCH}/ExecCoverage.""", "ExecCoverage"),

    ("ReviewerClosure", "reviewer", f"""Read-only review of the R65-C1 closure against round 64's two blocking findings.
Read: {TOOL1} (all of it), {PLAN}, {CLAIMS}, the round-64 review F1/F2
({LANE}/.ufo/waves/round-64/w1/ReviewerMatrix/review.md), and the round-64 instrument
{LANE}/tools/round-64/jsc-route-matrix.py.
Answer each question with a file:line pointer and a verdict (closed / open / partial):
 Q1 does CLOSURE pin every file the matrix run reads and every executable it spawns? Derive the import
    closure yourself (`grep -rn '^import\\|^from' {ROOT}/jsc2js-src/View8`) and compare with the map; name any
    read file not pinned and any pinned file the run never reads.
 Q2 does the census cover every write the run could make (name the exclusion and whether it can hide a write
    the run could make)?
 Q3 does the cache-free clause fire on a contaminated tree (read `cache_entries` and the call site)?
 Q4 is the predicate sentence byte-identical in {PLAN}, {CLAIMS} and the instrument constant? Quote the three.
 Q5 is the do-nothing arm reachable and does it exit 1 (read `emit`)? Does `--skip-run` bypass the closure check
    (state whether that is a hole for the claim)?
 Q6 does any label class in `classify_*`/`compose` admit a value the predicate would count as matching while the run
    actually failed?
Write {W1}/ReviewerClosure/review.md: one row per question (question, pointer, verdict), then a short list of defects
with severity (blocking / advisory) and a final line `VERDICT: ...`. No scratch needed.""", "ReviewerClosure"),

    ("CriticClaims", "critic", f"""Attack both declared claims as written. Read-only.
Read {PLAN}, {CLAIMS}, {TOOL1}, {TOOL2}, and the base tree at {BASE} (use `git -C {LANE} show {BASE}:<path>`).
For each claim: (a) is the axis the surface it changes (depth / calibration) and not merely the number it produces?
(b) can a do-nothing control reach the target (state the cheapest such control and its score under the frozen counter)?
(c) trace EVERY clause of the predicate to the code line that implements it and name any clause the code never reads
    (QUALITY #87); (d) is the after-state one value a closure can re-derive with one command over committed bytes?
(e) is any universal clause ("all", "every", "complete") present, and does the counting command enumerate the full set?
(f) does either claim narrow a target after landing, or reuse r64's frozen predicate under a new name?
Then attack R65-C2's before-arm: is `population_dropped` a legitimate mismatch count, or a re-description of the
old recipe's behaviour that a do-nothing round (no change) would also print?
Write {W1}/CriticClaims/critic.md: one section per claim with findings (id, claim clause, evidence pointer,
severity), then `VERDICT:` lines for C1 and C2.""", "CriticClaims"),

    ("MutClosure", "mutation-tester", f"""Mutation-test the R65-C1 instrument. Work only on scratch copies under {SCRATCH}/MutClosure/.
Never edit {TOOL1}.
Create six mutants (copy, one textual change, assert the target line changed) and for each run the instrument's
`--selftest` plus one targeted CLI arm; score killed (some arm goes red) or survived:
 M1 remove one CLOSURE entry (e.g. the D2 snapshot pin) - a manifest arm on a tree missing that file must still refuse;
 M2 make `cache_entries` return [] always - the cache control arm must go red (selftest case must fail);
 M3 make `compare_censuses` return `{{"equal": True, ...}}` always - the census controls must go red;
 M4 drop `-B` from the view8 argv and PYTHONDONTWRITEBYTECODE from the env - does any selftest case catch it?
 M5 make `classify_dump` return "dump-ok" for any rc - the verdict fixtures must go red;
 M6 make `emit` force exit 0 when labels match but the census differs - the census clause must be unreachable-green.
Write {W1}/MutClosure/mutants.md: mutant id, diff line, command, exit, verdict (killed/survived). Name survivors as
defects, do not repair them. Delete {SCRATCH}/MutClosure.""", "MutClosure"),

    ("MutCoverage", "mutation-tester", f"""Mutation-test the R65-C2 instrument. Work only on scratch copies under {SCRATCH}/MutCoverage/.
Never edit {TOOL2}.
Create six mutants (copy, one textual change, assert the line changed) and run `--selftest` plus the before/after CLI
arms at {BASE} for each; score killed or survived:
 M1 under `stem`, filter the population by DATE_TOKEN_RE again (restores the defect);
 M2 force `missing` to [] ;
 M3 force `dangling` to [] ;
 M4 accept an empty population as clean (exit 0);
 M5 normalize tokens after the CLAIM_RE filter (restores the `knowledge/`-prefixed rejection);
 M6 make `population_dropped` always 0.
Write {W1}/MutCoverage/mutants.md: mutant id, diff line, command, exit, verdict (killed/survived). Survivors are
named defects. Delete {SCRATCH}/MutCoverage.""", "MutCoverage"),

    ("SentinelProvenance", "sentinel", f"""Provenance and safety audit of the R65-C1 closure. Read-only except scratch ({SCRATCH}/SentinelProvenance).
1. For each of the three d8 builds: record `sha256sum` of d8, snapshot_blob.bin, icudtl.dat; locate any local
   release tarball under {ROOT} or ~/.cache and record its sha256 if present; state the provenance class the lane's
   round-64 record claims (official jsc2js release assets) and whether this host still holds the bytes to prove it.
2. Record `sha256sum` and version for node (v24.21.0) and the venv interpreter; record `venv/pyvenv.cfg` and the
   `parse` dist-info METADATA/RECORD digests.
3. Audit the pre-freeze cleanup: read {LANE}/.ufo/waves/round-65/prep/precache-dirs.txt and report what it records;
   independently `find {ROOT} -name '__pycache__' -o -name '*.pyc'` and report the count (expect 0).
4. Check that no download or install ran for this round: `git -C {LANE} log --oneline {BASE}..HEAD` and
   `ls -lt {ROOT}/inputs` (mtimes), and that {ROOT} mtimes predate the freeze except the cleanup.
5. Report any secret material you encounter by path/mechanism only (never the value).
Write {W1}/SentinelProvenance/report.md with a table (artifact | sha256 | provenance class | verified this round?)
and a short risk list. No scratch kept.""", "SentinelProvenance"),

    ("ScoutFrontier", "scout", f"""Read-only data walk: (a) independently re-derive the R65-C1 manifest - for every entry in CLOSURE
in {TOOL1}, run `sha256sum` on the absolute path and compare; write the 30-row table to
{W1}/ScoutFrontier/manifest-recheck.md with a mismatch count; (b) run `find {ROOT} -name '__pycache__' -o -name '*.pyc'`
and `ls -la {ROOT}/venv/bin/python` and record the interpreter chain; (c) read the two `planned` fields in the
SCORECARD (search `### Round 63` / `## Round 64` sections, the lines beginning `**planned`) and the r63 planned
record-section sweep candidate: produce a bounded planning note (<= 400 words, no implementation) naming what a
section-scoped record sweep would enumerate, which bindings it needs from each section, and the cheapest control that
would show it unmoved - this feeds the NEXT round's plan, it is not a claim of this round. No writes outside
{W1}/ScoutFrontier/. No scratch needed.""", "ScoutFrontier"),

    ("ConnectorCross", "connector", f"""Sibling-overlap scan (read-only; write only {W1}/ConnectorCross/overlap.md).
1. Search the sibling lane repos under /home/vgpnk/Projects/shokunin/*-shokunin for a `.jsc`/View8/V8-bytecode route
   counter or a closure-pin manifest capability: `grep -rln -i -E 'jsc|view8|loadjsc|dont_write_bytecode' --include='*.md' --include='*.py'`
   over each lane's SKILL.md, PROVINCE.md, tools/ and corpus/ (read-only). Name every hit's lane and what it claims.
2. Search the same lanes for a coverage-recipe / knowledge-file completeness counter (grep for
   'coverage map', 'population_dropped', 'knowledge_files' in tools/ and corpus/) and report whether any sibling
   already owns that instrument class.
3. Inside this lane, check the two new instruments' overlap: both read corpus/README.md? Which paths can each write?
   Name any duplicated logic that should have been composed instead of re-implemented (the lane's composition rule).
4. Report contested scope: any ground a sibling claims that this round's claims touch.
Write a table (lane | path:line | what it claims | overlap class) and a short `VERDICT:` line.""", "ConnectorCross"),

    ("ScribeSources", "scribe", f"""Open one source this round and draft its SOURCES.md row. Read-only to the lane; write only {W1}/ScribeSources/.
Source S266 (next free id): the Python documentation for the interpreter bytecode-write switch - fetch ONE of:
  https://docs.python.org/3/using/cmdline.html   (the `-B` option)
  https://docs.python.org/3/library/sys.html     (sys.dont_write_bytecode)
Choose the page whose committed-style text carries the clearer located quote; record the URL you opened, the access
date (2026-11-03), the fetch time, the byte count and sha256 of the fetched bytes, the exact quote (<= 25 words, one
contiguous passage), its line number in the fetched bytes and the nearest heading that contains it.
Draft the 11-column registry row in the schema of {LANE}/CORPUS.md:
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`
with id S266, kind docs, tier A (official documentation, scoped to the switch's semantics), status mined, opened
2026-11-03, recheck 90d, used-by `corpus/knowledge/2026-11-03-r65-jsc-closure-matrix.md`. No `|` inside any cell.
Write {W1}/ScribeSources/row.md (the row verbatim), {W1}/ScribeSources/gate.md (URL, access date, fetch sha256,
quote, line, heading, admissibility reasoning, and the limit of what the page does NOT establish about View8 output),
and {W1}/ScribeSources/fetch.json (url, bytes, sha256, headers). No scratch kept.""", "ScribeSources"),

    ("ScribeLesson", "scribe", f"""Draft the round-65 lesson's `## Mistakes` rows and one QUALITY candidate from evidence already on disk.
Read-only to the lane; write only {W1}/ScribeLesson/draft.md.
Read: {LANE}/.ufo/waves/round-65/prep/precache-dirs.txt, `git -C {LANE} show {BASE}:corpus/lessons/round-64.md`,
`git -C {LANE} show {BASE}:SCORECARD.md` (search `## Round 64` for the named recipe defect), {LANE}/corpus/QUALITY.md
(highest criterion number is 93; the next free is 94), {LANE}/.ufo/waves/round-65/l1/probe/dryrun-matrix.json,
{LANE}/.ufo/waves/round-65/l1/c2-before-date.json (if present).
Draft two Mistakes rows (format: id | class | evidence pointer | captured-by | fix), each pointer resolvable by command:
 M65-1: the round-64 View8 runs wrote `__pycache__` files into the retained toolchain (the recorded count and dirs are
   in the prep receipt). class: process/scope. captured-by: none before this round (r64's predicate had no cache-free
   clause). fix: the r65 cache-free clause plus `-B`/PYTHONDONTWRITEBYTECODE, shown red by the ExecControls cache arm.
 M65-2: the r1-era coverage recipe derived its denominator from its own date filter (144 files -> 142 assessed).
   class: number-drift/stale-premise. captured-by: the r64 SCORECARD note (recorded, no criterion). fix: the repaired
   stem recipe plus QUALITY #94.
Draft the QUALITY row #94 in the lane's table style, one sentence, pipe-free: a measurement recipe's denominator is
the population it claims, never a filter of it; a recipe that cannot see a file must not be able to report it clean.
Write {W1}/ScribeLesson/draft.md: the two rows verbatim, the QUALITY row, and for each row the command that
demonstrates its evidence pointer. No scratch.""", "ScribeLesson"),
]


def build():
    tasks = []
    for name, role, body, _ in ITEMS:
        prompt = "/skill:godspeed\n\n" + GS + "\n\n" + body
        if re.search(r"\{[A-Za-z_][A-Za-z_0-9.]*\}", prompt):
            raise SystemExit(f"unresolved placeholder in {name}")
        tasks.append({"name": name, "role": role, "prompt": prompt})
    return {
        "wave": "r65-w1",
        "milestone": "r65-w1 build+attack: the frozen R65-C1 closure matrix, controls, mutation and closure review; the R65-C2 coverage arms and mutations; provenance, sources, lesson drafts.",
        "reportDir": ".ufo/waves/round-65/w1",
        "context": CONTEXT,
        "items": tasks,
    }


if __name__ == '__main__':
    spec = build()
    out = pathlib.Path(LANE + '/.ufo/waves/round-65/r65-w1-spec.json')
    out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print('items', len(spec['items']), 'roles', sorted({i['role'] for i in spec['items']}))
    print('wrote', out)
