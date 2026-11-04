#!/usr/bin/env python3
"""Generate the kaidoku round-67 wave-1 spec (one v1 build+attack wave, 12 seats). R67, KaidokuR67.

Interpolation discipline: every absolute path is substituted at build time; the rendered items must
contain no unresolved `{...}` placeholders (checked before the spec is written).
"""
import hashlib
import json
import pathlib
import re

GS = open('/home/vgpnk/.agents/skills/godspeed/directive.md').read().strip()
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
W1 = LANE + '/.ufo/waves/round-67/w1'
SCRATCH = '/fast/scratch/hyaku/kaidoku-r67'
TOOL1 = LANE + '/tools/round-67/avm-le-counter.py'
TOOL2 = LANE + '/tools/round-67/mutation-battery.py'
RULE2 = LANE + '/tools/round-67/gap-rule-v2.json'
RUNSH = LANE + '/tools/round-67/c1-run.sh'
ENGINE = LANE + '/tools/round-50/c1-counter.py'
R66C = LANE + '/tools/round-66/closure-boundary.py'
R66V = LANE + '/tools/round-66/coverage-selfcheck.py'
RULE50 = LANE + '/tools/round-50/gap-rule.json'
CARRIERS = LANE + '/tools/round-50/carriers.json'
CLAIMS = LANE + '/.ufo/waves/round-67/claims.json'
PLAN = LANE + '/plans/round-67-claims.md'
PRE = LANE + '/.ufo/waves/round-67/l1/pre'
BASE = 'a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92'
FREEZE = '3663e6b21dccf4c4957f459301156664d8b151d6'
S1 = hashlib.sha256(pathlib.Path(TOOL1).read_bytes()).hexdigest()
S2 = hashlib.sha256(pathlib.Path(TOOL2).read_bytes()).hexdigest()
SR = hashlib.sha256(pathlib.Path(RULE2).read_bytes()).hexdigest()
SE = hashlib.sha256(pathlib.Path(ENGINE).read_bytes()).hexdigest()

PREDICATE1 = ("R67-C1 is verified iff the pinned round-50 scoring engine, run under the "
              "round-67 gap rule and the round-67 documentation bindings, reports "
              "carriers_matched 4 of 4 with met_target true and exit 0 at the measured "
              "revision, while the four frozen envelopes scored under the round-50 rule "
              "report gaps_ok on 2 of 4.")
PREDICATE2 = ("R67-C2 is verified iff the round-67 selftest battery kills both round-66 "
              "mutation survivors -- the closure counter whose arm() returns passed true "
              "unconditionally and the coverage counter whose recipe_a_equivalence returns "
              "equivalent without running the block -- while both pristine counters stay "
              "green, and the round-66 selftests alone leave both survivors alive (0 of 2).")

CONTEXT = f"""# Target
kaidoku-shokunin round 67, attempt 1, wave w1 = the single v1 build+attack wave (12 seats; policy
band 8-16; attack seats reviewer, critic, two mutation-testers = 4 of 12). Base {BASE}; operative
freeze {FREEZE}. Two declared claims (plan {PLAN}; container {CLAIMS}):
- R67-C1 (coverage, frontier -> core) re-freezes the round-50 LE-AVM measurement under a gap rule
  that classes char-device entries as not-publishable instead of per-row required. Predicate,
  verbatim: "{PREDICATE1}"
- R67-C2 (depth, counter repair) adds the selftest battery that binds the two round-66 mutation
  survivors. Predicate, verbatim: "{PREDICATE2}"

The L1 runs the four carrier data runs and the after-arms AFTER this wave; your job is the frozen
instruments, the before-arms, the attacks and the prose, not the data run. A seat that writes an
`after.json` into {LANE}/corpus/evidence/round-67/ has exceeded its scope.

# Frozen inputs (read-only; NEVER edit)
- {TOOL1} (sha256 {S1}) - R67-C1 counter. Loads {ENGINE} (sha256 {SE}) by path under ENGINE_PIN and
  calls its `measure()` after patching exactly the names listed in its docstring. Modes:
  `--score` (needs --root --rev --freeze --pkg65 --carrier-cache --work --out) and `--control`
  (needs --root --rev --work --out; the do-nothing rule control and three red fixtures).
- {RULE2} (sha256 {SR}) - the round-67 gap rule: `allowed`/`removed`/`structural` unchanged from
  {RULE50}, `required.char-device` false, a `class_disposition` block with the reason.
- {TOOL2} (sha256 {S2}) - R67-C2 battery. Loads {R66C} and {R66V} by path under their sha256 pins;
  `--selftest` (9 cases), `--score` (two mutants: killed_before/killed_after), `--control`
  (the r66 selftests only).
- {RUNSH} - the round-67 data-run harness (fork of tools/round-50/c1-run.sh; the delta is exactly
  `kaidoku-r50`->`kaidoku-r67`, `round-50`->`round-67`, `R50-C1`->`R67-C1`). The L1 runs it.
- {CARRIERS} - the four chain-pinned vendor carriers (bytes never committed, AVM licence).
- Before-arms already committed: {PRE}/control-dryrun.json (gaps_ok_round50 2, gaps_ok_round67 4),
  {PRE}/control-dryrun-c2.json (killed_before 0, survived_before 2), {PRE}/score-dryrun-at-base.json
  (killed_after 2), {PRE}/selftest-r50.txt (169 cases), {PRE}/selftest-c2.json (9 cases).

# Rules for every seat
- Write ONLY under {W1}/<YourSeatName>/ ; read anything under {LANE}. Never write
  {LANE}/tools/, {LANE}/corpus/, {LANE}/PROVINCE.md, {LANE}/SCORECARD.md, {LANE}/LOG.md,
  {LANE}/SKILL.md, {LANE}/corpus/evidence/, the fleet repo, or any sibling lane.
- NEVER run git/jj writes anywhere (no commit, add, stash, checkout, switch, reset, pull, push, jj
  mutation). Read-only `git -C {LANE} log/show/diff/ls-files/rev-parse/cat-file` is fine.
- Every `Report:` trailer path the validator renders is relative to {LANE} - write it at
  {LANE}/<that path>.
- Scratch: `S={SCRATCH}/<YourSeatName>`; `mkdir -p "$S"`; `trap 'rm -rf -- "$S"' EXIT` in shell and
  a `finally: shutil.rmtree` in Python; TMPDIR=$S for every subprocess; delete the tree before you
  yield. Nothing under /tmp is evidence.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the
  task; read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record
  tool/version/channel/reason). **pacman guard (orchestrator ruling 2026-10-20): all pacman
  transactions are PAUSED host-wide** - install via `uv tool`/`npx`/an official binary in
  `~/.local/bin`, or file an L0 question; never `-Sy`, `-Syu`, `-U`, `-R`, downgrade, or restart a
  host service. The host's sync DB is ~413 packages ahead, so naming an installed package is a
  forbidden partial upgrade.
- No `agent://all`. Findings go in your report; the L1 reads the wave dir.
- Do not commit, push, or edit another seat's directory. One writer per file.
- Honesty: an unrun check has not passed; report dead ends and limits, never fabricate a verdict.
"""

ITEMS = []


def item(name, role, body):
    ITEMS.append((name, role, body))


item("ExecPins", "executor", f"""Verify every frozen pin and the freeze order at {FREEZE}. Read {CLAIMS} and {PLAN}.
 1. For every path in `claims.json` `instruments`, `sha256sum` the committed blob
    (`git -C {LANE} show {FREEZE}:<path> | sha256sum`) and compare with the recorded pin.
 2. `git -C {LANE} log --diff-filter=A --format=%H -- .ufo/waves/round-67/claims.json` must print
    exactly one commit and it must be {FREEZE}; every instrument's add commit must be an ancestor
    of {FREEZE} (`git merge-base --is-ancestor <c> {FREEZE}`), and the carry-in `cf705c53` too.
 3. Run both instruments' selftests at the freeze:
    `TMPDIR=$S python3 -I -B {TOOL2} --selftest --root {LANE} --work $S/bat`
    and `TMPDIR=$S python3 -I -B {R66C} --selftest` / `{R66V} --selftest`.
 4. Re-run the R29 freeze gate: `python3 -I -B {LANE}/tools/round-29/freeze-gate.py --root {LANE}
    --rev {FREEZE}`; report the round-67 entry verbatim (verdict and findings).
Write {W1}/ExecPins/pins.json with every pin, the add commits, the ancestor results, the selftest
summaries and the gate entry. Report any mismatch as a blocking finding.""")

item("ExecGapAudit", "executor", f"""Independent re-derivation of the per-carrier gap accounting, WITHOUT the r67 wrapper.
Read {ENGINE}, {RULE50}, {RULE2}, {CARRIERS} and the four committed envelopes under
{LANE}/corpus/evidence/round-50/c1/<id>/after.json (ids g7581 g7582 c6490 c6430).
 1. Import the engine by path (`importlib.util.spec_from_file_location`), pin its sha256 to
    {SE}, and call its own `parse_nonregular`, `subject_root`, `diagnostics`, `gaps`,
    `gap_rule_model`, `disposition_check`, `published`, `nonregular_published`.
 2. For each carrier and each rule, record `gaps_ok` and, for the FALSE carriers, the FULL list of
    undispositioned oracle paths - do not accept the engine's 8-path truncation: recompute the
    missing list yourself from the rule model (required kinds, gaps resolved by `extract_rel`,
    removals) and print every path with its kind and detail.
 3. Census the non-regular kinds per carrier (count by kind) and prove the undispositioned set is
    exactly the char-device class (13/13/1/1) and that no symlink is undispositioned.
Write {W1}/ExecGapAudit/audit.json with per-carrier rule results, the full missing lists, the kind
census and a one-line verdict per carrier. A path you cannot explain is a blocking finding.""")

item("ExecRedControls", "executor", f"""Extend the red-control battery over the committed envelopes (the wrapper's own control covers two).
Work from {W1}/ExecRedControls. Using the engine's `disposition_check` / `nonregular_published`
directly (same import and pin as ExecPins):
 1. Reproduce the wrapper's control (`python3 -I -B {TOOL1} --control --root {LANE} --rev {BASE}
    --work $S/ctl --out $S/wrapper-control.json`) and confirm gaps_ok_round50 2 / round67 4.
 2. Three NEW red fixtures, each on its own root and each expected to fail under the round-67 rule:
    (a) a block-device oracle row whose gap is removed from the envelope (the class is not required,
        so this must NOT fail - record it as the class boundary and say so);
    (b) a FIFO oracle row whose `unpublished-entry` gap is removed (fifo is not required either -
        record the boundary);
    (c) a gap whose `kind` is not in `allowed` for its entry kind (e.g. a `depth-limited` gap that
        carries a path) - must fail;
    (d) a `MaliciousSymlinkRemoved` diagnostic naming a char-device entry - must fail
        (`removed.kinds` is symlink only).
 3. State which of (a)-(d) the round-67 rule is designed to admit and which it must reject, and
    whether the admitted ones can hide a real extraction failure.
Write {W1}/ExecRedControls/red.json + red.md. A red fixture that does not fire is a blocking
finding against the rule.""")

item("ReviewerClauses", "reviewer", f"""Read-only clause-to-line review of both frozen instruments against both frozen predicates.
Read in full: {TOOL1}, {TOOL2}, {RULE2}, {PLAN}, {CLAIMS}, and the committed pre-freeze receipts in
{PRE}. Check, for each predicate:
 1. Every clause traced to the line that evaluates it (the plan carries a trace table; verify it,
    do not trust it). Name any clause with no implementing line.
 2. The predicate sentence byte-identical in the plan, `claims.json`, the instrument's `PREDICATE`
    constant and the emitted receipts (`sha256sum` of the extracted sentence in each).
 3. The instruments read the predicate from the claims file and refuse on a mismatch (QUALITY #68).
 4. No arm can pass while the defect it names is absent: for C1, does `--score` reach 4/4 with a
    rule that waives symlinks? For C2, does the battery pass with a mutant that is merely broken
    (syntax error) rather than mutated?
 5. Advisory findings are allowed; blocking findings must say which clause they falsify.
Write {W1}/ReviewerClauses/review.md with the per-clause table, the sha256 evidence and the
blocking/advisory split.""")

item("CriticClaims", "critic", f"""Falsify the two claims by attack, not by re-reading. Scratch under {SCRATCH}/CriticClaims.
Read {PLAN}, {CLAIMS}, both instruments and the pre-freeze receipts. Try each, in isolated scratch
copies (never edit the lane files):
 A. Relabelled-carrier attack on C1: `CLAUSES` drops `carrier_fresh_ok`. Does the claim then count
    a carrier whose bytes were already scored in round 50? Show it with a receipt and state whether
    the predicate discloses it.
 B. Rule-scope attack on C1: build a rule that waives `symlink` as well and score it with
    `--score --gap-rule <that rule>` (use the r50 envelopes through a scratch copy of the engine
    call path, or the wrapper's `--control` code path). Does the claim's counter distinguish it
    without the red controls? State the exact detector that would catch it.
 C. False-kill attack on C2: construct a mutant that fails an UNRELATED selftest case and show
    whether `--score` reports it killed (it must not: `EXPECTED_CASE` names the case).
 D. False-survive attack on C2: can a mutant pass the battery while the defect it names is present?
    Try at least one concrete shape (e.g. `arm()` returning `passed: True` only when `detail` is
    empty, or an equivalence function that runs the block but ignores its output).
 E. A claim you cannot falsify after these: say so and name what would falsify it.
Write {W1}/CriticClaims/attacks.md with one section per attack and its receipt path. Every attack
names the predicate clause it attacks and its outcome (falsified / survives / needs data).""")

item("MutCounter", "mutation-tester", f"""Mutation-test the R67-C1 counter {TOOL1} in scratch copies only (never edit it).
Four mutants, each a separate copy under $S/mut/, each scored with `--control` and, where it can
run without the data, with `--score` against a scratch clone-free invocation using the r50 envelopes
(the wrapper's control path is enough for M2/M3):
 M1 `patch_engine` stops dropping `carrier_fresh_ok` (CLAUSES unchanged).
 M2 the rule's `required.char-device` back to true.
 M3 the `--control` `control_ok` expression forced true.
 M4 `PROV_BASE` left at the r50 prefix.
For each: the mutation diff, the sha256 of the mutant, the command, the exit code and the field
that changes. State which detector kills it (exit code vs receipt field vs control field) and any
mutant that survives. Write {W1}/MutCounter/mutants.md + the per-mutant diffs/receipts.""")

item("MutBattery", "mutation-tester", f"""Mutation-test the R67-C2 battery {TOOL2} in scratch copies only.
Five mutants under $S/mut/, each scored by `--score` and `--selftest`:
 N1 `EXPECTED_CASE` accepts any failing case name.
 N2 `killed_after` drops the case-name condition (`after_rc != 0` alone).
 N3 `control()` reports `survived_before` as killed (before/after swap).
 N4 `selftest()` drops the `equiv-doctored-diffs` case.
 N5 `score()` treats a missing `after_out` as a kill.
For each: diff, mutant sha256, the command, exit code, and whether the battery's own selftest or a
score run catches it. A mutant that survives is a disclosed gap, not a repaired one. Write
{W1}/MutBattery/mutants.md + receipts.""")

item("SentinelScope", "sentinel", f"""Scope, secret and provenance audit of round 67's committed bytes so far (base {BASE} -> {FREEZE}).
Read-only over the lane. Check and receipt into {W1}/SentinelScope/audit.md:
 1. Write scope: every path changed by the round-67 commits (`git -C {LANE} diff --name-status
    {BASE} {FREEZE}`) is lane-relative and inside the declared write scope (tools/round-67,
    .ufo/waves/round-67, plans, LOG.md, corpus/claim-freezes-v2.tsv).
 2. No vendor bytes committed: no blob under corpus/evidence/round-67/ exists yet, and the four
    carrier pins appear only as hashes; `git -C {LANE} ls-files | wc -l` delta vs the base.
 3. No credential material, no session/private URLs, no `op://`, no absolute HOME paths that name
    secrets; scan the round's added lines (`git -C {LANE} diff {BASE} {FREEZE}`) for
    `BEGIN .*PRIVATE KEY|token|cookie|password|secret|op://`.
 4. The rule file has no escaped pipe and parses as JSON; the instruments parse
    (`python3 -m py_compile`).
 5. Scratch hygiene: no committed path under /tmp or /fast/scratch.
Report every finding with its path and line; an empty finding list is a result, not a blank.""")

item("ScoutSource", "scout", f"""Open the round's source and produce the SOURCES row evidence. Work in {SCRATCH}/ScoutSource.
The C1 class rule needs a primary source for "a char-device entry is a device-node inode, not a
file payload, so a regular-file extractor cannot reproduce it".
 1. Fetch ONCE into $S: `curl -fsSL https://docs.kernel.org/filesystems/squashfs.html` (record HTTP
    status, byte count and sha256). If that URL 404s, try
    https://www.kernel.org/doc/html/latest/filesystems/squashfs.html and record which served.
 2. Locate the inode-type text: the "Basic device inode" (and, if present, "Extended device inode")
    description with major/minor, and the section heading that contains it. Quote ONE contiguous
    passage of at most 25 words, verbatim, with its line number in the fetched bytes.
 3. Check the lane's registry: `grep -n 'squashfs' {LANE}/corpus/SOURCES.md` - is this URL or a
    close duplicate already a row? If yes, name the row and say whether a new row is justified
    (different locator/scope) or must be rejected as a duplicate (CORPUS.md rule 2).
 4. Propose the row cells: source (title - URL), kind (docs), tier (A if primary/authoritative for
    the format), scope, anchor (section + fetched-bytes line), teaches (one grounded sentence),
    status queued, opened 2026-11-03, recheck 180d, used-by the planned entry path
    corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md.
Write {W1}/ScoutSource/row.md, gate.md (URL, access date, quote, locator) and fetch.json (status,
bytes, sha256). A quote you cannot find contiguously in the bytes is a rejection, not a paraphrase.""")

item("ConnectorCross", "connector", f"""Sibling-overlap scan for round 67's two surfaces. Read-only.
Question: does another shokunin lane already own (a) a SquashFS gap/class-accounting rule or a
device-node publication rule, (b) a mutation-score battery that binds a counter's own selftest, or
(c) a receipt-revision convention for gate receipts?
 1. `grep -rIl --include='*.py' --include='*.md' --include='*.json' -E 'char-device|block-device|
    nonregular|disposition' /home/vgpnk/Projects/shokunin/*-shokunin 2>/dev/null | grep -v kaidoku`
    then read the hits that are gates/counters (not prose).
 2. `grep -rIl -E 'mutation|mutant' /home/vgpnk/Projects/shokunin/*-shokunin 2>/dev/null | grep -v
    kaidoku` and classify each hit (a battery that scores mutants, or prose).
 3. For each overlap: name the lane, the path, and whether it is the same class (report, do not
    absorb) or a genuinely different scope.
Write {W1}/ConnectorCross/overlap.md with the commands, hit counts and the classification. A class
precedent is cited as a precedent, never claimed as novel.""")

item("ScribeKnowledge", "scribe", f"""Draft the round's knowledge entry (prose only; the L1 lands it).
Read {PLAN} clause R67-C1, {RULE2}, {LANE}/corpus/evidence/round-50/c1/<id>/after.json,
{LANE}/corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md and {LANE}/corpus/QUALITY.md.
Write {W1}/ScribeKnowledge/entry.md:
 1. The provenance trio first: `source:` citing the SOURCES row the ScoutSource seat opened
    (S-number unknown to you: write `S<scout-row>` and the L1 substitutes the admitted id) plus the
    URL and anchor; `verified-at:` 2026-11-03 with the landing commit to be filled by the L1;
    `recheck:` the fetch + counter command.
 2. What moved and only what moved: Frontier -> Core for `squashfs_v4_le` on LE AVM-marker
    (`hsqs`) members, the four carriers, and the class rule's exact scope (char-device is not
    publishable by design; symlinks stay per-row required; a gap naming a char device is still
    allowed).
 3. The class rule and its limits: what it does NOT prove (no new carrier, no LE AVM kernel image,
    no nested sub-image, no vendor-mangled body, the marker is re-stampable).
 4. Observation / inference / unknown labels on every claim (QUALITY #5).
No file outside $S and {W1}/ScribeKnowledge.""")

item("ScribeLesson", "scribe", f"""Draft the round lesson (prose only; the L1 lands it) at {W1}/ScribeLesson/lesson.md.
Read {PLAN}, {PRE}/control-dryrun.json, {PRE}/control-dryrun-c2.json, {PRE}/score-dryrun-at-base.json,
{LANE}/corpus/lessons/round-66.md and {LANE}/corpus/lessons/round-66-verifier-spotcheck.md.
 1. `## Gate` - candidates considered for the round's source row: the kernel SquashFS page (admit or
    reject with reason and flip), the round-50 entry's S243/S244/S245/S249 rows (re-opened? say
    which and why they do not need a new row), and at least one REJECT with a reason and flip.
    Record the access date and the located quote for every admit.
 2. `## Mistakes` - at least one real mistake from this round or an earlier one, one row per
    mistake: class / evidence pointer / captured-by (criterion or `none`) / fix. Candidates: the
    round-50 rule's over-wide `required.char-device` (class over-generalisation from one carrier
    family; captured-by none until QUALITY #107; fix = the class rule + count), and any real
    mistake you can evidence from this round's receipts.
 3. `## Outcome` - one factual paragraph per claim with its receipt path, and the honest statement
    that the outside non-author closure is pending.
 4. Two QUALITY row drafts in the lane's table style: (i) a rule generalised from one carrier
    family must name the family it was generalised from and the class it cannot see; (ii) a
    mutation survivor is closed only by a case that exercises the mutated function on a false input.
No file outside $S and {W1}/ScribeLesson.""")


def build():
    tasks = []
    for name, role, body in ITEMS:
        prompt = "/skill:godspeed\n\n" + GS + "\n\n" + body
        if re.search(r"\{[A-Za-z_][A-Za-z_0-9.]*\}", prompt):
            raise SystemExit(f"unresolved placeholder in {name}")
        tasks.append({"name": name, "role": role, "prompt": prompt})
    return {
        "wave": "r67-w1",
        "milestone": "r67-w1 build+attack: both frozen instruments pinned and selftested, the class-rule gap audit and red controls, the clause review and claim attacks, four plus five counter/battery mutants, the source row and the prose drafts.",
        "reportDir": ".ufo/waves/round-67/w1",
        "context": CONTEXT,
        "items": tasks,
    }


if __name__ == '__main__':
    spec = build()
    out = pathlib.Path(LANE + '/.ufo/waves/round-67/r67-w1-spec.json')
    out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print('items', len(spec['items']), 'roles', sorted({i['role'] for i in spec['items']}))
    print('wrote', out)
