#!/usr/bin/env python3
"""Generate the kaidoku round-69 wave-1 spec (one v1 build+attack wave, 15 seats).

R69, KaidokuR69.  Every absolute path is substituted at build time; the rendered
items must contain no unresolved `{...}` placeholders (checked before writing).
"""
import hashlib
import json
import pathlib
import re

GS = open('/home/vgpnk/.agents/skills/godspeed/directive.md').read().strip()
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
W1 = LANE + '/.ufo/waves/round-69/w1'
L1 = LANE + '/.ufo/waves/round-69/l1'
SCRATCH = '/fast/scratch/hyaku/kaidoku-r69'
CLAIMS = LANE + '/.ufo/waves/round-69/claims.json'
PLAN = LANE + '/plans/round-69-claims.md'
PE = LANE + '/tools/round-69/packed-elf.py'
MC = LANE + '/tools/round-69/mutation-check.py'
CP = LANE + '/tools/round-69/contract-probe.py'
CTL = LANE + '/tools/round-69/controls.py'
PRE = L1 + '/pre'
BASE_RECEIPT = LANE + '/.ufo/waves/round-68/l1/scores/c2-at-landing.json'
R68 = LANE + '/tools/round-68/packed-elf.py'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
BASE = 'd7d9a62cc70935304e600ed0dee864fc4f1751f7'
FREEZE = 'f15998102f1ce3569e61faa2ac6f286bc414538e'

PINS = {str(pathlib.Path(p).name): hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
        for p in (PE, MC, CP, CTL)}

P1 = ("R69-C1 is verified iff the frozen mutation battery, run at the measured revision against "
      "tools/round-69/packed-elf.py with patch set r69, reports survivors [] with all five mutants "
      "killed and each kill's failed list naming its declared arm-false case, and pristine.cases 20 "
      "with pristine.ok true, while the same battery against tools/round-68/packed-elf.py at the base "
      "revision d7d9a62cc70935304e600ed0dee864fc4f1751f7 with patch set r68 reports exactly the five "
      "survivors M1_identity, M2_recovery, M3_detected, M4_before, M5_control and pristine.cases 13.")
P2 = ("R69-C2 is verified iff the frozen contract probe, run at the measured revision against "
      "tools/round-69/packed-elf.py with the measured run's receipt, reports arms_passed 6 of target 6 "
      "— A1_missing_node, A2_work_unusable, A3_packer_version, A4_packer_sha256, A5_carrier_record and "
      "A6_packer_pin each true — while the same probe against tools/round-68/packed-elf.py and its own "
      "round-68 landing receipt .ufo/waves/round-68/l1/scores/c2-at-landing.json at the base revision "
      "reports arms_passed 0 of 6 naming all six arms.")
P3 = ("R69-C3 is verified iff the frozen receipt checker, run at the measured revision over the "
      "instrument's three-carrier receipt, reports met true with target 3, carriers_matched 3, "
      "control_ok true, failing [], every carrier's before_ceiling_ratio at or below 0.75, and one "
      "carrier of kind shared-object (libz), while the same checker over the round-68 receipt "
      ".ufo/waves/round-68/l1/scores/c2-at-landing.json reports target 2 and no shared-object carrier.")

CONTEXT = f"""# Target
kaidoku-shokunin round 69, attempt 1, wave w1 = the single v1 build+attack wave (15 seats; policy band
8-16; attack seats reviewer x2, critic, mutation-tester x2 = 5 of 15 = 33%). Base {BASE}; operative
freeze {FREEZE} (the commit that first adds the claims container). Three declared claims (plan {PLAN};
container {CLAIMS}):
- R69-C1 (calibration, capability acquisition) — the packed route's five 2026-11-03 mutation
  survivors are killed by the instrument's own selftest through the `evaluate_carrier()` arm seam.
  Predicate, verbatim: "{P1}"
- R69-C2 (operability, capability acquisition) — the route's typed exit-2 contract, enforced UPX pin
  and per-carrier format/mode records. Predicate, verbatim: "{P2}"
- R69-C3 (coverage, capability acquisition) — a pinned packed shared-object carrier enters Core
  (/usr/lib/libz.so.1.3.2) beside the two executables. Predicate, verbatim: "{P3}"

The L1 runs the after-arms and lands every file. A seat writes ONLY under its own
{W1}/<Name>/ directory and its own scratch dir; it never edits a tracked lane file, never the fleet
repo, never another lane, never the jj/git index, and never commits or pushes. Seats return drafts and
findings; the L1 lands them.

# Frozen inputs (read-only; NEVER edit)
- {PE} (sha256 {PINS['packed-elf.py']}) — the round-69 route: 20-case selftest, typed preflight,
  enforced packer pin, three carriers including the shared object, `--check-receipt`.
- {MC} (sha256 {PINS['mutation-check.py']}) — the R69-C1 battery (patch sets r68 and r69).
- {CP} (sha256 {PINS['contract-probe.py']}) — the R69-C2 six-arm black-box probe.
- {CTL} (sha256 {PINS['controls.py']}) — the seven do-nothing/shortcut controls.
- {R68} — the round-68 route, kept byte-identical at its own round (48ef4c68…). Never edit it.
- Base receipts: {PRE}/c1-at-base.json (survivors 5, pristine.cases 13), {PRE}/c2-at-base.json
  (arms_passed 0 of 6), {PRE}/c3-at-base.json (target 2, exit 1), {PRE}/controls-at-base.json
  (seven arms, ok true). {BASE_RECEIPT} is the round-68 landing receipt (packer recorded, no pins).
- {CLAIMS} — the frozen container (pins, atoms A0-A9); {PLAN} — the declaration.
- REA package root: {PKG} (version 6.5.0, package.json sha256 a5003023…). Invoke as
  `node {PKG}/scripts/rea.mjs <verb> …`; NEVER `npx -y` (it rewrites the npx cache lock).

# Rules that bind every seat
- Scratch: your own dir under {SCRATCH}/<Name>/; create it, delete it before you yield
  (`trap 'rm -rf -- "$S"' EXIT` or `finally: shutil.rmtree`), copy receipts into your wave dir first.
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
- A claim is judged on the counter, kill rule and predicate frozen above: do not propose narrowing,
  widening or re-freezing one; attack it as written and report what you observe."""


def item(name, role, task):
    return {"name": name, "role": role,
            "prompt": "/skill:godspeed\n\n" + GS + "\n\n" + task}


ITEMS = [
    item("ExecC1", "executor", f"""Independently re-derive R69-C1 — with YOUR OWN patch applier, not
{MC}. Write under {W1}/ExecC1/ and scratch {SCRATCH}/ExecC1/.

1. Read {PLAN} (R69-C1), {CLAIMS}, {PRE}/c1-at-base.json and
   {LANE}/.ufo/waves/round-68/w1/MutPacked/mutants.md (the five original mutants).
2. `git -C {LANE} show {FREEZE}:tools/round-69/packed-elf.py` and the same for
   tools/round-68/packed-elf.py; write each to your scratch and confirm the sha256 against {CLAIMS}.
3. Apply the five r69 mutants YOURSELF (the same behavioural sites: identity_ok, recovery_ok,
   detected, before_ok, control_ok — find them in the source, patch the expression to a constant and
   record the exact old/new text). Run `python3 -I -B <copy> --selftest` and record rc + failed names.
   Then do the same to the r68 blob with its own five sites and record survivors.
4. Write `rederive.md`: the exact patches you used, the rc/failed per mutant, the survivor sets, and a
   verdict: does the frozen predicate's sentence hold at {FREEZE}? Name any mismatch with the
   battery's receipt (do not trust it)."""),

    item("ExecC2", "executor", f"""Attack R69-C2 with your OWN harness — do not run {CP}. Write under
{W1}/ExecC2/ and scratch {SCRATCH}/ExecC2/.

1. Read {PLAN} (R69-C2) and {LANE}/tools/round-69/packed-elf.py (the preflight and `--upx` seam).
2. Build your own fixtures: (a) a PATH dir with git/readelf/upx but no node; (b) a 0500 work dir;
   (c) a `upx` shell script printing `upx 5.1.0`; (d) a copy of /usr/bin/upx with one byte appended;
   (e) a `upx` script printing `upx 5.2.0` but whose sha256 differs (a different bytes shape from d).
   For each, run the instrument with `--root {LANE} --rev {FREEZE} --pkg {PKG} --work <scratch>` and
   record rc and the full stderr/stdout.
3. Check the exit-2 message is TYPED and names the class (node / work / packer version / packer sha).
   Also probe one shape the plan did not name (your choice) and say whether the contract holds or
   leaks a traceback.
4. Take the real three-carrier receipt the L1 leaves at {L1}/scores/c3-at-landing.json (if absent yet,
   wait for it or run the route yourself under your scratch) and re-derive the carrier `format` with
   your own `readelf -h` and the `packing_mode` from the receipt's own pack argv.
5. Write `rederive.md`: each arm's command, rc, typed class, and a verdict on the frozen predicate.""")
    ,

    item("ExecC3", "executor", f"""Independently verify R69-C3's carrier-class evidence. Write under
{W1}/ExecC3/ and scratch {SCRATCH}/ExecC3/.

1. Read {PLAN} (R69-C3), the CARRIERS table in {PE}, and {PRE}/c3-at-base.json.
2. With your own commands (upx, readelf, sha256sum), reproduce for /usr/lib/libz.so.1.3.2: the pin,
   the original format (`readelf -h`), the packed state (`upx -l`, zero sections), the pack and
   unpack round trip (`upx --best`, `upx -d`, sha256 equality), and the section/segment counts.
3. Repeat with a SECOND shared object you pick from /usr/lib (pin it, pack it, unpack it, check byte
   identity) — this is a generalisation probe, not claim input; name the carrier and every number.
4. Inspect {L1}/scores/c3-at-landing.json (or run the route yourself if absent) and say whether each
   carrier's recorded counts/format/ratio equal your own derivation. Flag any mismatch.
5. Write `verify.md` with the commands, the numbers, and a verdict on the frozen predicate (target 3,
   every arm, every ratio <= 0.75, one shared-object carrier)."""),

    item("ExecRepairs", "executor", f"""Prepare the R68-V4 repair for the L1 to land. Write under
{W1}/ExecRepairs/ and scratch {SCRATCH}/ExecRepairs/.

1. Read {LANE}/corpus/lessons/round-68-verifier-spotcheck.md §5 defect R68-V4 and
   {LANE}/tools/round-29/prefile-check.sh.
2. Measure each named defect with a command: (a) the comment says the legacy ledger "stops at round-52"
   — count its data rows and name the last round it carries and the rounds missing; (b) the comment
   says the gate "reported 20 exact of 36 on every round from 53 on" — run the round-24 gate if it can
   be run read-only, otherwise say why not and cite the ExecLedger seat's own receipt; (c) the failure
   branch's `${{got:-absent}}` is unreachable because `sha256sum` of empty stdin is `e3b0c442…` — show
   it with a command.
3. Write the exact replacement text for lines 31-35 of the script (comment + the failure branch), and
   the exact append-only LOG.md correction line (never rewrite a filed line). Do not edit the script.
4. Show red-before/green-after in a scratch copy: the script's defect statements vs the corrected
   text, and a `sh -n` syntax check of your proposed file.
5. Write `repair.md` with the patch text, the commands and their outputs."""),

    item("ExecLedger", "executor", f"""Prepare the R68-V1/V2/V5 repairs. Write under {W1}/ExecLedger/ and
scratch {SCRATCH}/ExecLedger/.

1. Read {LANE}/corpus/knowledge/2026-11-03-r68-packed-elf-route.md:1-12,
   {LANE}/corpus/README.md:110-125, {LANE}/corpus/SOURCES.md (row S269), and
   {LANE}/corpus/lessons/round-68-verifier-spotcheck.md §5 R68-V1/V2/V5.
2. V1: the entry opens with a bold `**Source:**` prose line and no `verified-at:`/`recheck:` lines.
   Write the exact append-only correction block (a `## Correction — round 69` section with
   `- source:` / `- verified-at:` / `- recheck:` list items plus the reason and pointer). Never rewrite
   the filed lines.
3. V2: the round-68 knowledge-index row sits above the table header/delimiter. Write the exact fix:
   the moved row line and the line numbers before/after in a scratch mirror (copy README to scratch,
   move the row, show the table parses: every row has the delimiter above it).
4. V5: the S269 row and the lesson say the quote is 11 words; count it (`printf '%s' '<quote>' | wc -w`).
   Write the exact new SOURCES row that supersedes S269 (CORPUS rule 2: `teaches` opens
   `supersedes S269 — `) with the correct count and the reason, plus the lesson note.
5. Write `repairs.md` with every exact line and the commands that produced it."""),

    item("ReviewerGates", "reviewer", f"""Review the four frozen round-69 instruments against the three
predicate sentences. Write under {W1}/ReviewerGates/ and scratch {SCRATCH}/ReviewerGates/.

1. Read {PLAN}, {CLAIMS}, then each of {PE}, {MC}, {CP}, {CTL} in full.
2. Clause map: for every clause of R69-C1, R69-C2 and R69-C3, name the exact code line/function that
   implements it, or mark it UNIMPLEMENTED. Check especially: the patch-set expectations; the
   `killed_wrong_case` path; `pristine.cases`; the six arm ids and their pass conditions; the
   `before_ceiling_ratio` comparison (`> 0.75` vs `<= 0.75`); the shared-object check; the
   `arms_passed`/`failed` consistency validators.
3. Freeze integrity: `git -C {LANE} show {FREEZE}:<tool> | sha256sum` for all four and compare to
   {CLAIMS} pins; `git -C {LANE} diff {FREEZE}..main -- tools/round-69` must be empty (report if not).
4. Attack the instruments as a reviewer: does any selftest case pass vacuously? Can `--check-receipt`
   pass a receipt with a false arm? Can the probe's A5 read a receipt from a different instrument?
   Does `preflight` order allow a short-circuit?
5. Write `review.md`: the clause map, each defect with severity (blocking / advisory), and a verdict."""),

    item("CriticClaims", "critic", f"""Falsify the three claims' predicates as written. Write under
{W1}/CriticClaims/ and scratch {SCRATCH}/CriticClaims/.

1. Read {PLAN} and {CLAIMS}. For each predicate, construct the cheapest fixture that satisfies the
   predicate SENTENCE while the claimed capability is absent — e.g. a receipt the checker passes with
   fabricated counts; a battery receipt that names the five cases without running them; a probe
   receipt with six arms whose observations are invented; a `target 3` receipt whose third carrier is
   a relabelled executable.
2. For each candidate fixture, run the frozen counter it attacks (`--check-receipt`, `--validate`,
   the probe's `--validate`) and record rc + output. If the fixture passes, that is a predicate gap:
   name it, state the counter or predicate change it would require, and mark it routed (never
   re-freeze this round).
3. Test the before-arms: are the base values reproducible from committed bytes at {BASE}? Does any
   after-target follow from a do-nothing control (re-read {PRE}/controls-at-base.json)?
4. Check the C3 arithmetic: 10/167, 10/99, 120/184 — does any carrier's ceiling exceed 0.75, and is
   the libz ceiling justified by the measured packed count (98) with headroom?
5. Write `attack.md`: each fixture, its command, its result, and a verdict sentence per claim."""),

    item("MutBattery", "mutation-tester", f"""Generate NEW mutants beyond the frozen five and score them.
Write under {W1}/MutBattery/ and scratch {SCRATCH}/MutBattery/.

1. Target {PE} at {FREEZE} (copy to scratch; NEVER edit the frozen file). Design at least eight
   mutants at behaviour-bearing sites the five do not cover, e.g.: `carrier_arms`'s control default;
   `fold`'s `bool(carriers)`/`control_ok`; `check_receipt`'s `ratio > 0.75`; `check_receipt`'s
   `"shared-object" not in kinds`; `elf_format`'s `len(found) == 4`; `preflight`'s node/before-git
   order; `section_count`'s "no sections" branch; the refusal arm's `len(code) > 200`.
2. For each: patch a scratch copy, run `--selftest` AND (where it applies) `--check-receipt` on both
   a passing and a failing synthetic receipt, and record which detector fires.
3. Report survivors with the exact false claim each would let through, and whether a cheap selftest
   case could kill it (route it; do not edit the frozen instrument).
4. Write `mutants.md`: the table (mutant, patch site, detectors, fires?, survivor?), the receipts, and
   the survivors named for the next freeze."""),

    item("MutSelftest", "mutation-tester", f"""Attack the COUNTERS themselves — can each fail? Write
under {W1}/MutSelftest/ and scratch {SCRATCH}/MutSelftest/.

1. Targets (copies only, never the frozen files): {MC}, {CP}, {CTL}.
2. For {MC}: (a) drop a mutant row from its PATCH_SETS — does the battery still report ok? (b) make it
   count a syntax-error kill as a kill (`killed_wrong_case` → `killed`) — does the predicate's wording
   stop it? (c) make `--validate` accept an empty mutant list.
3. For {CP}: (a) make A3 pass on any rc 2 (drop the `packer` substring check); (b) make A5 skip a
   carrier with missing `format`; (c) make `--validate` accept an arm with no observation.
4. For {CTL}: (a) flip one control's expected value so the do-nothing control would be "ok";
   (b) make `c3-loose-ceiling` expect 0.
5. Each mutated counter must be shown RED against the fixture it should reject; record the exact
   line, the mutation, and the observed false green or red. Write `counters.md` with the table and the
   survivors named for the next freeze."""),

    item("SentinelScope", "sentinel", f"""Scope and safety audit of the round so far. Write under
{W1}/SentinelScope/ and scratch {SCRATCH}/SentinelScope/.

1. `git -C {LANE} status --porcelain` and `git -C {LANE} diff --stat {BASE}..main`; every path the
   round touched must be inside {LANE} (tools/round-69, plans/round-69-claims.md, SKILL.md, .ufo/waves/
   round-69). Also check the fleet root `git -C /home/vgpnk/Projects/shokunin status --porcelain` for
   untracked files naming this lane/round (misroot candidates) — report, do not delete.
2. The `--upx` seam runs a caller-supplied binary as a subprocess. Enumerate what an untrusted `--upx`
   could do before the pin check (it is invoked for `--version`), and say whether the pin check makes
   the seam safe for the lane's use. Do not run anything malicious; reason from the code.
3. Credential material: grep the round's new files for tokens/keys/session ids; report any hit.
4. Scratch discipline: list what is under {SCRATCH} and whether seats cleaned up; no /tmp paths in
   committed tools (`grep -n '/tmp' {LANE}/tools/round-69/*.py`).
5. Write `audit.md` with each check, its command and its result, and a verdict."""),

    item("ScoutSource", "scout", f"""Open the packer-identity source for this round's sourced claim.
Write under {W1}/ScoutSource/ and scratch {SCRATCH}/ScoutSource/.

1. Fetch https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt (the pinned tag) with curl,
   record HTTP status, byte count and sha256. Locate the sections that ground a PACKER-IDENTITY row
   (not byte identity, which S269 already covers): the `--version`/`-V` description, the ELF format
   section, and any statement about the packer's version banner.
2. Also open two candidate rejections and record why each fails (e.g. the UPX front page for no
   revision identity; a distro man page rendering another version). Give URL, HTTP status, bytes,
   sha256, and the located quote or the reason it fails.
3. For every candidate: URL, access date (UTC), a ≤25-word LOCATED quote (line numbers in the fetched
   bytes) or the rejection reason + flip condition + tier (A/B/C) + kind.
4. Write `sources.md` and `fetches.json`; propose the exact SOURCES.md row (11 cells, no `|` inside)
   that the L1 will land, and the exact sentence R69-C2's A3/A4/A6 arms cite from it."""),

    item("ConnectorCross", "connector", f"""Sibling-overlap scan: does any other lane own this round's
ground? Write under {W1}/ConnectorCross/ and scratch {SCRATCH}/ConnectorCross/.

1. Read {LANE}/PROVINCE.md (Core/Frontier/Adjacent) and the fleet lanes' PROVINCE/SKILL headers
   read-only under /home/vgpnk/Projects/shokunin/*-shokunin/.
2. Search for lanes that own: mutation testing of gates, binary packer routes, shared-object triage,
   evidence-receipt contracts. Use grep over their PROVINCE.md/SKILL.md and corpus/README.md
   frontier lists; report every hit with path:line.
3. Decide: is any of R69-C1/C2/C3 cross-domain absorption? Name contested scope if any, and say what
   the lane should report rather than absorb. If none, say so with the sweep that showed it.
4. Write `overlap.md` with the sweep commands, hits, and the verdict."""),

    item("ScribeKnowledge", "scribe", f"""Draft the round-69 knowledge entry and its index rows. Write
under {W1}/ScribeKnowledge/ (drafts; the L1 lands them).

1. Read {PLAN}, {L1}/scores/ (the L1's after receipts, when present), {PRE}/c1-at-base.json,
   c2-at-base.json, c3-at-base.json, and {LANE}/corpus/knowledge/2026-11-03-r68-packed-elf-route.md
   (its shape and limits). Read {W1}/ScoutSource/sources.md if it exists for the S-row.
2. Draft `corpus/knowledge/2026-11-03-r69-packed-route-contract.md`: opens with `source:` (the S-row
   id + URL + anchor), `verified-at:` and `recheck:` lines; sections: the arm seam and the five
   mutations it kills; the typed contract table (exit-2 classes, the enforced pin, the carrier
   record); the shared-object carrier table (jq/xxd/libz with counts and ratios); Limits (UPX 5.2.0,
   linux/amd64, default packing mode, libz.so.1.3.2 only, REA 6.5.0); and a Corrections section only
   if needed.
3. Draft the PROVINCE.md `## Round-69 additions to Core` block and the corpus/README.md knowledge-index
   row (below the delimiter row) + coverage-map row.
4. Every number carries its receipt path; no claim beyond the receipts. Write `entry.md`, `province.md`,
   `readme-rows.md`."""),

    item("ScribeLesson", "scribe", f"""Draft `corpus/lessons/round-69.md`. Write under
{W1}/ScribeLesson/ (drafts; the L1 lands it).

1. Read {LANE}/corpus/lessons/round-68.md and round-68-verifier-spotcheck.md (the routed defects), the
   round-67 lesson, {PLAN}, {CLAIMS}, and the L1's after receipts under {L1}/scores/.
2. Required blocks: `## Gate` — at least one ADMIT and one REJECT from this round's source work (see
   {W1}/ScoutSource/sources.md; otherwise open the UPX doc and one reject candidate yourself), each
   with locator, measured value, decision, flip condition; `## Mistakes` — table id | class | evidence
   pointer | captured-by | fix, mining at least three, including the round-68 M68-6 class (a survivor
   is closed only by a case that feeds the mutated function a false input) and M68-4 (a rule
   generalised from one carrier family must name the family and the class it cannot see); `## Outcome`
   — placeholders the L1 fills with the after numbers, each line marked `[L1]`; `## Census` — the
   start value from {L1}/census-start.txt and a placeholder for the end value.
3. Do not claim a verdict; do not invent evidence. Write `lesson.md` and `sources-opened.md`
   (the list of sources you actually opened)."""),

    item("ReviewerRepairs", "reviewer", f"""Review the repairs drafts for append-only discipline. Write
under {W1}/ReviewerRepairs/ and scratch {SCRATCH}/ReviewerRepairs/.

1. Read the reparations drafts if they exist ({W1}/ExecRepairs/repair.md,
   {W1}/ExecLedger/repairs.md) and the defects they answer
   ({LANE}/corpus/lessons/round-68-verifier-spotcheck.md §5 R68-V1..V6).
2. Check each proposed change against CORPUS.md: corrections are new entries, never rewrites;
   SOURCES rows are append-only with `supersedes S0NN —`; LOG.md corrections are appended lines; the
   prefile script may be corrected (it is a tool, not a filed record) but the filed LOG line may not.
3. Verify each fix is shown able to fail (a red-before state) per CORPUS "a fix is shown able to fail
   before it counts"; name any fix with no red-before.
4. Check R68-V6 (the report erratum) is a report-only correction and needs no lane artifact.
5. Write `review.md`: per defect, ACCEPT / REVISE with the reason and the exact correction wording."""),
]

SPEC = {
    "wave": "r69-w1",
    "milestone": ("r69-w1 build+attack: three-claim verification, five independent re-derivations, "
                  "eight-plus new mutants, counter mutation, clause review, predicate attacks, scope "
                  "audit, sourced row, sibling scan, knowledge and lesson drafts, repairs."),
    "reportDir": ".ufo/waves/round-69/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

rendered = json.dumps(SPEC)
assert "{W1}" not in rendered and "{LANE}" not in rendered and "{SCRATCH}" not in rendered
for it in ITEMS:
    assert it["prompt"].startswith("/skill:godspeed\n\nYou are a Godspeed-enabled subagent.")
    assert re.search(r"\{[A-Z_]{2,}\}", it["prompt"]) is None, it["name"]
pathlib.Path(LANE + '/.ufo/waves/round-69/r69-w1-spec.json').write_text(json.dumps(SPEC, indent=1))
print(json.dumps({"items": len(ITEMS), "roles": sorted({i["role"] for i in ITEMS}),
                  "spec": LANE + '/.ufo/waves/round-69/r69-w1-spec.json',
                  "pins": PINS}))
