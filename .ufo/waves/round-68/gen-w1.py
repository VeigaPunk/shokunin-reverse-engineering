#!/usr/bin/env python3
"""Generate the kaidoku round-68 wave-1 spec (one v1 build+attack wave, 13 seats).

R68, KaidokuR68.  Every absolute path is substituted at build time; the rendered
items must contain no unresolved `{...}` placeholders (checked before writing).
"""
import hashlib
import json
import pathlib
import re

GS = open('/home/vgpnk/.agents/skills/godspeed/directive.md').read().strip()
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
W1 = LANE + '/.ufo/waves/round-68/w1'
SCRATCH = '/fast/scratch/hyaku/kaidoku-r68'
CLAIMS = LANE + '/.ufo/waves/round-68/claims.json'
PLAN = LANE + '/plans/round-68-claims.md'
RC = LANE + '/tools/round-68/registry-conformance.py'
PE = LANE + '/tools/round-68/packed-elf.py'
CTL = LANE + '/tools/round-68/controls.py'
PRE = LANE + '/.ufo/waves/round-68/l1/pre'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
BASE = 'fcbe200f6739c38939e0dabf3f251de2cc6bd727'
FREEZE = '1eaf596e5f241762349fbd102c9e09ec1df18e3f'
SHA_RC = hashlib.sha256(pathlib.Path(RC).read_bytes()).hexdigest()
SHA_PE = hashlib.sha256(pathlib.Path(PE).read_bytes()).hexdigest()
SHA_CTL = hashlib.sha256(pathlib.Path(CTL).read_bytes()).hexdigest()

P1 = ("R68-C1 is verified iff the frozen registry-conformance census, run at the measured revision, "
      "reports mismatches 0 with scope_size 71 and registry_rows 77, while the same census run at the "
      "base revision fcbe200f6739c38939e0dabf3f251de2cc6bd727 reports mismatches 2 and names exactly "
      "tools/round-67/avm-le-counter.py and tools/round-67/mutation-battery.py as unregistered.")
P2 = ("R68-C2 is verified iff the frozen packed-ELF counter, run at the measured revision over its two "
      "pinned carriers, reports carriers_matched 2 of target 2 and control_ok true with every arm true "
      "on both carriers (detected, before_ok, identity_ok, recovery_ok, and refusal_ok on the carrier "
      "that pins an address), reports the packed bytes of both carriers at exactly 3 procedures, and "
      "reports the non-packed original as neither listed nor decompressible by the packer.")

CONTEXT = f"""# Target
kaidoku-shokunin round 68, attempt 1, wave w1 = the single v1 build+attack wave (13 seats; policy band
8-16; attack seats reviewer, critic, two mutation-testers = 4 of 13). Base {BASE}; operative freeze
{FREEZE}. Two declared claims (plan {PLAN}; container {CLAIMS}):
- R68-C1 (calibration, capability acquisition) — the registry-conformance census over the lane's own
  instrument inventory, repairing the four rows the round-67 outside closure found missing. Predicate,
  verbatim: "{P1}"
- R68-C2 (coverage, capability acquisition) — the packed-ELF triage route (detect UPX, unpack with sha
  identity, recover the original's REA inventory). Predicate, verbatim: "{P2}"

The L1 runs the after-arms and lands every file. A seat writes ONLY under its own
{W1}/<Name>/ directory and its own scratch dir; it never edits a tracked lane file, never the fleet
repo, never another lane, never the jj/git index, and never commits or pushes.

# Frozen inputs (read-only; NEVER edit)
- {RC} (sha256 {SHA_RC}) — the R68-C1 census. `--selftest` is 11 cases.
- {PE} (sha256 {SHA_PE}) — the R68-C2 route. `--selftest` is 13 cases.
- {CTL} (sha256 {SHA_CTL}) — the six control arms.
- Base receipts: {PRE}/c1-at-base.json (mismatches 2), {PRE}/c2-dryrun-at-base.json (route green at the
  base revision), {PRE}/controls-at-base.json (six arms).
- {CLAIMS} — the frozen container: pins, predicates, atoms A0-A9.
- {PLAN} — the declaration.
- REA package root for the CLI: {PKG} (version 6.5.0, package.json sha256 a5003023…). Invoke as
  `node {PKG}/scripts/rea.mjs <verb> …`; NEVER `npx -y` (it rewrites the npx cache lock — the
  round-67 M67-3 defect).

# Rules that bind every seat
- Scratch: your own dir under {SCRATCH}/<Name>/; create it, delete it before you yield
  (`trap 'rm -rf -- "$S" EXIT` or `finally: shutil.rmtree`), copy receipts into your wave dir first.
  Never /tmp for anything over 50 MB; never clone the lane.
- Absolute paths only: your tools start at the fleet root, so every path you write must be absolute
  under {LANE}. Every `Report:` trailer path is relative to {LANE} — write it at
  {LANE}/<that path>.
- Read-only git is fine (`git -C {LANE} log/show/diff/ls-tree/rev-parse`); NEVER `git add/commit/
  checkout/reset/push` and NEVER a mutating `jj` command anywhere.
- Tooling authorization (operator 2026-10-19): you may install or upgrade tools that help the task;
  read /home/vgpnk/.omp/agent/RULES.md first, use official channels only (uv tool / npx / an official
  release binary in ~/.local/bin), record tool, version, channel and reason in your report. **pacman
  transactions are PAUSED host-wide** — do not run any pacman transaction (`-S`, `-Sy`, `-Syu`, `-U`,
  `-R`); a needed package that only pacman could install is an L0 question in your report, not an
  install.
- You are a leaf: no subagent dispatch except one read-only `labrat` probe from an executor seat, and
  no swarm of your own.
- Label every conclusion observation / inference / unknown; an unrun check has not passed.
"""

ITEMS = [
    {
        "name": "ExecRegistry",
        "role": "executor",
        "task": f"""Independently re-derive the R68-C1 census — with your OWN extractor, not the instrument's.
Write under {W1}/ExecRegistry/ and scratch {SCRATCH}/ExecRegistry/.

1. Read {RC} and {CLAIMS} (atoms A0/A1/A4/A5) and {PLAN}.
2. From git objects at {BASE} (`git -C {LANE} show <rev>:<path>`, `ls-tree`), extract with grep/awk/python
   of your own: every `tools/round-N/….(py|sh|mjs)` named by `plans/round-N-claims.md` for its own round
   N >= 41 that exists at the revision; the SKILL.md registry rows between the two
   `instrument-registry v2` markers. Report: scope size, row count, unregistered set, duplicate set,
   absent-at-rev set, thin-verdict set, legacy (N<41) set, named-but-absent set. Compare every number to
   {PRE}/c1-at-base.json — the base must be scope 69, rows 73, mismatches 2 = the two round-67 paths.
3. Re-derive at the CURRENT lane tip (read it with `git -C {LANE} rev-parse main`): the round-68 plan now
   names two more instruments, so report the strict pre-repair reading (expected 4 unregistered) and the
   post-repair reading the L1 will land (expected 0 with scope 71 / rows 77). If the rows are not there
   yet, say so; do not add them.
4. Audit whether the regime declaration in the instrument's docstring and in atom A4 agree with what the
   code does (`plan_scope`, `census`), and whether a foreign-round citation is really excluded.
Report `report.md` with one table per revision, the exact commands, and any disagreement.""",
    },
    {
        "name": "ExecPacked",
        "role": "executor",
        "task": f"""Probe whether the R68-C2 route GENERALISES beyond its two pinned carriers, with your own
commands. Write under {W1}/ExecPacked/ and scratch {SCRATCH}/ExecPacked/.

1. Read {PE} (the arms and the carrier table) and {PRE}/c2-dryrun-at-base.json.
2. Pick a third host ELF of your choice (examples: /usr/bin/ls, /usr/bin/gzip, /usr/bin/file — pick one
   that `upx --best` accepts). Copy it into your scratch, `chmod +x`, record its sha256, then:
   `upx -l` on the copy (must refuse), `upx --best -q -o`, `upx -l` on the packed file (must list it),
   `readelf -SW` section count before/after, `upx -d -q -o`, sha256 of the unpacked file, and
   `node {PKG}/scripts/rea.mjs analyze --format json <file>` on the original, the packed file and the
   unpacked file — record `normalized_result` procedure/segment/string counts for each.
3. Also run the jq refusal leg: `node {PKG}/scripts/rea.mjs decompile <packed> 0x103fa0 --format json`
   and the same on an unpacked copy of /usr/bin/jq; record rc, error code, and the code length.
4. Verdict to report: does the route's rule (detect -> unpack identity -> inventory equality) hold on
   your third carrier? Name every arm that failed and why. This is a generalisation probe: it feeds the
   report, not the frozen predicate.
Report `report.md` with a per-file table, the argv of every command, and the counts.""",
    },
    {
        "name": "ExecControls",
        "role": "executor",
        "task": f"""Build and score two MORE shortcut controls this round did not commit, and re-derive the
six committed arms. Write under {W1}/ExecControls/ and scratch {SCRATCH}/ExecControls/.

1. Run `python3 -I -B {RC} --selftest` and `python3 -I -B {PE} --selftest`; record the case counts and
   confirm each prints `ok: true`. Confirm both variables print the registered inventory
   (`REGISTERED_CASES`) and that the executed names equal it (not just a count).
2. Run `python3 -I -B {CTL} --json-out <your dir>/controls-rerun.json` and compare field for field with
   {PRE}/controls-at-base.json.
3. New arm A (registry): plant a junk registry fixture in a scratch clone of the real inputs — a SKILL.md
   whose table has one row for a path that is NOT in scope plus a row with a thin verdict cell — and show
   the census's own functions (import the module) flag both. New arm B (packed): a synthetic carrier dict
   whose packed inventory equals the original's (a "detection from a packed count" shortcut) — show
   `fold`/`carrier_arms` refuse it. New arm C (all-false): every arm false -> not met.
4. For each new arm state what it would score if the counter were wrong (the false-green value) and why
   the committed counter cannot produce it.
Report `report.md` with the arm table and the receipts' paths under your wave dir.""",
    },
    {
        "name": "ReviewerGates",
        "role": "reviewer",
        "task": f"""Read-only clause-to-line review of both frozen instruments against both frozen predicates
(QUALITY #87: every clause traced to an implementing line).
Write under {W1}/ReviewerGates/.

1. Read {CLAIMS} (the two predicate strings, atoms A1/A4/A7/A9), {PLAN}, {RC}, {PE}, {CTL}.
2. For R68-C1, map each clause to the line that implements it: `mismatches 0`, `scope_size 71`,
   `registry_rows 77`, the base `mismatches 2` + the two named paths, the regime (own-round, N>=41,
   exists-at-rev), the four mismatch sets, and the `--selftest` inventory assertion. Name any clause the
   code cannot implement or implements differently.
3. For R68-C2, map: `carriers_matched 2 of 2`, `control_ok`, the five arms, `packed bytes at exactly 3
   procedures`, and the `neither listed nor decompressible` control clause. Check that `before_ok` uses
   the carrier floor and not the packed count itself; that `identity_ok` compares against the PIN, not
   against a value derived in-run; that `recovery_ok` compares unpacked to ORIGINAL counts.
4. Check the container's pins against the files: sha256 of each instrument vs `instruments`, and that
   {RC}/{PE}/{CTL} are byte-identical to the freeze commit (read-only git).
5. Verdict: blocking or advisory finding, each with file:line. Do not execute the counters beyond
   `--selftest`; do not edit anything.
Report `review.md`.""",
    },
    {
        "name": "CriticClaims",
        "role": "critic",
        "task": f"""Falsify the two claims by attack, not by re-reading. Scratch {SCRATCH}/CriticClaims/,
receipts under {W1}/CriticClaims/.

Attack R68-C1: (a) is the regime definition chosen to make the count small (N>=41, own-round only,
exists-at-rev)? Quantify what the claim would read under each widening (all rounds; foreign citations
counted; absent-at-rev counted) from your own extraction — report the numbers, not an opinion. (b) Does
`scope_size 71` follow necessarily from the two new plan entries plus the base 69, or can it pass with a
different tree? (c) Can a row that names a *different* file pass? Try a fixture where the row's cell-0
path is a superset/superset-with-suffix of the scope path. (d) Is `thin` grammar gameable by a cell that
merely contains "0", "1", "2" in prose?
Attack R68-C2: (a) identity is sha-equality with the pin — is that circular when the pinned original is
in the same run? Say exactly what it does establish (upx -d is byte-exact here) and what it does not.
(b) `recovery_ok` compares unpacked inventory to original inventory measured in the same run: is the arm
then a tautology given sha identity? (c) Is the `before` arm (3 procedures) a REA artifact of the
missing section header rather than evidence that the program is hidden? Test with a second reader
(`readelf -l`, `strings -n 8 | grep -c` or `rizin -N -q -c iI`) on the packed bytes.
Write `attack.md` with a verdict per sub-question: survived / falsified / unprovable, and the exact
command behind each number.""",
    },
    {
        "name": "MutRegistry",
        "role": "mutation-tester",
        "task": f"""Mutation-test {RC} in scratch copies only (never edit the instrument). Six mutants, each
a separate copy under {SCRATCH}/MutRegistry/mut/, each scored by `--selftest` and, where it can run
without the live tree, by a scoring call against a fixture root:
 M1 drop the own-round check -> a plan's foreign tool enters scope.
 M2 drop `thin` from `mismatches`.
 M3 drop the duplicate test.
 M4 `census` returns `mismatches: 0` unconditionally.
 M5 relax the verdict grammar to `re.search("0|1|2", cell)`.
 M6 `--selftest` executes 10 cases (drop one) but still prints the registered 11.
For each: does `--selftest` exit non-zero, and which case fires? A mutant that survives both detectors is
a finding, not a bug to fix here — name it and the case that would bind it (QUALITY #108: a survivor is
closed only by a case that feeds the mutated function a false input).
Write `mutants.md` with the mutant line, the score, the failing case set, and survivors named.""",
    },
    {
        "name": "MutPacked",
        "role": "mutation-tester",
        "task": f"""Mutation-test {PE} in scratch copies only. Five mutants under {SCRATCH}/MutPacked/mut/,
each scored by `--selftest` and by a `--skip-run` / fixture-root call where possible:
 M1 `identity_ok` returns True without comparing.
 M2 `recovery_ok` compares the unpacked counts to themselves.
 M3 `detected` uses only `upx -l` rc (no section-count clause).
 M4 `before_ok` compares the packed count to itself instead of the carrier floor.
 M5 the control arm (`upx -l` on the original) is dropped from `fold`.
For each: which detector fires, with which case name; if none fires, state what the green run would then
claim (a false green) and the case that would bind it.
Write `mutants.md` with the table and the survivors named.""",
    },
    {
        "name": "SentinelScope",
        "role": "sentinel",
        "task": f"""Scope, secret and provenance audit of the round's committed bytes: {BASE}..{FREEZE}
(plus the uncommitted wave dir if present). Read-only over the lane; receipts under {W1}/SentinelScope/.

Check and receipt: (1) every path the two commits touch is inside {LANE} and inside the round's write
scope; (2) no credential material (tokens, keys, cookies, private paths outside the lane) in any
committed byte of the round; (3) the instrument pins in {CLAIMS} match the blobs at the freeze
(`git -C {LANE} show {FREEZE}:<path> | sha256sum`); (4) no compiled cache (`__pycache__`, `.pyc`) or
scratch artifact is committed; (5) the receipts under {PRE}/ carry no absolute scratch path that is not
already public elsewhere, and every `rev` they name exists; (6) the fleet root is untouched by this
lane's seats (`git -C /home/vgpnk/Projects/shokunin status --porcelain` — report what you see, do not
clean anything).
Write `audit.md` with one line per check: PASS / FINDING (named), and the command behind it.""",
    },
    {
        "name": "ScoutSource",
        "role": "scout",
        "task": f"""Open the round's source and produce the SOURCES row evidence. Scratch
{SCRATCH}/ScoutSource/, evidence under {W1}/ScoutSource/.

The R68-C2 route needs a primary source for its identity rule: "a packed executable is restored by
unpacking to its original bytes; packing is reversible and the unpacked file is the original program,
not a reconstruction". Candidates, each opened this round with HTTP status, byte count, sha256 of the
fetched bytes and a LOCATED quote (file/line or section):
 (a) UPX official documentation — https://upx.github.io/ and the manual page it links
     (https://upx.github.io/upx-doc.html); look for the `-d`/`--decompress` description and any
     statement that unpacking restores the original file.
 (b) the UPX source repository's own docs (https://github.com/upx/upx — `doc/` or README) at a PINNED
     tag/commit; a raw.githubusercontent URL with the commit is the preferred locator (the S268
     precedent).
 (c) one candidate the lane should REJECT, with the reason (e.g., a man-page mirror with no revision,
     a wiki, a blog).
For each: quote <= 25 words, contiguous, from the fetched bytes; give the byte offset or line number.
Then write the exact `corpus/SOURCES.md` row (11 columns as the current registry's header defines:
read the header at {LANE}/corpus/SOURCES.md and the census schema in /home/vgpnk/Projects/shokunin/
CORPUS.md) with id S269 (confirm the highest id at the lane tip first), tier, kind docs, opened date
2026-11-03, recheck, status mined, used-by the round-68 entry. Do NOT append it; the L1 lands it.
Write `gate.md` (the table) and keep each fetched copy under your wave dir with its sha256.""",
    },
    {
        "name": "ConnectorCross",
        "role": "connector",
        "task": f"""Sibling-overlap scan for round 68's two surfaces. Read-only. Write under
{W1}/ConnectorCross/.

Question: does another shokunin lane already own (a) an instrument-registry or inventory-conformance
census (a gate comparing a declared table against the files a plan names), (b) a packed-executable /
UPX triage route, or (c) a sha256-identity "unpack restores the original" rule? Search the sibling lanes
under /home/vgpnk/Projects/shokunin/*-shokunin/ (their tools/, corpus/knowledge/, corpus/QUALITY.md,
SKILL.md) **read-only**, plus the fleet root's `merge/` and `considerthese/` directories if present.
For each hit: lane, path, what it does, and whether it is the same class as ours. Report the nearest
precedent even when it is not a duplicate (the class is what matters). Never edit, never import, never
run another lane's tool.
Write `overlap.md` with a hit table, a verdict per surface (duplicate / adjacent / unowned), and the
commands you ran.""",
    },
    {
        "name": "ScribeKnowledge",
        "role": "scribe",
        "task": f"""Draft the round's knowledge entry (prose only; the L1 lands it).
Path to draft: {W1}/ScribeKnowledge/entry.md — target repo path
`corpus/knowledge/2026-11-03-r68-packed-elf-route.md`.

Read: {PLAN} (R68-C2), {PE}, {PRE}/c2-dryrun-at-base.json, {W1}/ScribeSource/gate.md (the source row, if
it exists yet — otherwise the UPX page yourself and record what you opened), and an existing entry for
house style (`{LANE}/corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md`).

The entry must carry: the route (detect: `upx -l` + no section header; unpack: `upx -d`; identity:
sha256 equals the pin; recover: REA inventory equality), the measured numbers (packed 3 procedures vs
167/30/190 and 99/29/103; the refusal at 0x103fa0 on packed bytes and the code recovered after unpack),
the evidence pointers (instrument, receipts, carrier pins, packer pin), a provenance trio
(observation / inference / unknown), a `Limits` section naming what was NOT examined (no packed PE, no
packer other than UPX 5.2.0, no anti-UPX-modified stub, inventory equality is not semantic equality),
an explicit `[unknown]` list, and `source:` citing the round's new S-id first.
Add the coverage-map row text and the PROVINCE Core row text as separate fenced blocks for the L1.
Do not write outside your wave dir. `report.md` names what you drafted and what you could not verify.""",
    },
    {
        "name": "ScribeLesson",
        "role": "scribe",
        "task": f"""Draft the round-68 lesson (prose only; the L1 lands it) at
{W1}/ScribeLesson/lesson.md — target `corpus/lessons/round-68.md`.

Read: the round-67 verifier spot-check (`{LANE}/corpus/lessons/round-67-verifier-spotcheck.md`), the
round-67 lesson, {PLAN}, {CLAIMS}, {PRE}/c1-at-base.json and {PRE}/controls-at-base.json.

Required blocks: a `## Gate` table with at least one ADMIT and one REJECT from this round's source work
(see {W1}/ScribeSource/gate.md if it exists; otherwise open the UPX page and one reject candidate
yourself), each with locator, measured value, decision and flip condition; a `## Mistakes` table with
id | class | evidence pointer | captured-by | fix — mine at least three, and at least one must be the
defect the round-67 outside closure found in this lane's own self-assessment (registry rows absent while
the plan named the instruments), with `captured-by` naming the criterion that should have caught it; a
`## Outcome` section left as placeholders the L1 fills with the after-arm numbers (mark each line
`[L1]`); a `## Census` section with the start value from
{LANE}/.ufo/waves/round-68/l1/census-start.txt.
Do not claim a verdict; do not invent evidence. `report.md` lists the sources you opened.""",
    },
    {
        "name": "ExecLedger",
        "role": "executor",
        "task": f"""Close the round-67 closure's routed defects 3 and 4 on paper (the L1 lands the files).
Write under {W1}/ExecLedger/ and scratch {SCRATCH}/ExecLedger/.

1. Read `{LANE}/corpus/claim-freezes-corrections.tsv` and `{LANE}/corpus/claim-freezes-v2.tsv`.
   Defect 3 (QUALITY #100): the round-64 row's findings cell was rewritten in place at `451f3102`
   (`-INSTRUMENT_UNRESOLVED mkcache.js; …` -> `+INSTRUMENT_UNPINNED,INSTRUMENT_UNRESOLVED`), so a
   companion row is owed in the corrections ledger. Write the exact 8-column row
   (`correction-id`, `corrects`, `field`, `was`, `now`, `cause`, `receipt`, `utc`) with the values you
   can re-derive from `git -C {LANE} diff 8672cf40 451f3102 -- corpus/claim-freezes-v2.tsv`, receipt
   `451f3102`, and a correction-id that continues the ledger's own series (read the existing ids).
2. Defect 4: run the round-29 prefile gate and the round-24 freeze gate with `--disclosures` exactly as
   `{LANE}/tools/round-29/prefile-check.sh` and the freeze-gate scripts define them; paste the full
   output and exit codes into your report (the L1 commits the output as the round's prefile receipt).
   Then audit `corpus/claim-freezes.tsv`: count its data rows, name the rounds 53-67 it is missing and
   the stray `round-35` row, and propose the exact retirement erratum text (QUALITY #100: retire, never
   silently rewrite) — or argue with receipts why a different disposition is right.
3. Report the gate's verdicts for round 68 if a round-68 row exists; if not, say what the gate needs.
Write `report.md` with the exact TSV line, the gate outputs verbatim, and the counts.""",
    },
]

ITEMS = [{"name": it["name"], "role": it["role"],
          "prompt": "/skill:godspeed\n\n" + GS + "\n\n" + it["task"]} for it in ITEMS]

SPEC = {
    "wave": "r68-w1",
    "milestone": "r68-w1 build+attack: census re-derivation, third-carrier route probe, extra controls, clause review, claim attacks, eleven mutants, scope audit, source row, sibling scan, drafts, ledger repairs.",
    "reportDir": ".ufo/waves/round-68/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

rendered = json.dumps(SPEC)
assert "{W1}" not in rendered and "{LANE}" not in rendered
for it in ITEMS:
    assert it["prompt"].startswith("/skill:godspeed\n\nYou are a Godspeed-enabled subagent.")
    assert re.search(r"\{[A-Z_]{2,}\}", it["prompt"]) is None, it["name"]
pathlib.Path(LANE + '/.ufo/waves/round-68/r68-w1-spec.json').write_text(json.dumps(SPEC, indent=1))
print(json.dumps({"items": len(ITEMS), "roles": sorted({i["role"] for i in ITEMS}),
                  "spec": LANE + '/.ufo/waves/round-68/r68-w1-spec.json',
                  "sha_rc": SHA_RC[:12], "sha_pe": SHA_PE[:12], "sha_ctl": SHA_CTL[:12]}))
