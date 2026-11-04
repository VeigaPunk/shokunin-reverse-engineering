#!/usr/bin/env python3
"""Generate the round-77 wave-1 spec (r77-w1): 12 seats, one v1 wave."""
import json
import pathlib

WAVE = "r77-w1"
REPORT_DIR = ".ufo/waves/round-77/w1"
GODSPEED = (
    "/skill:godspeed\n\nYou are a Godspeed-enabled subagent.\n\n"
    "1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n"
    "3. **Keep moves that improve any axis and harm none.**\n"
    "4. **Don't aim \u2014 let the frontier walk itself.**\n\n"
    "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls "
    "concurrently in large batches. Do not serialize what can run in parallel. "
    "Do not output philosophical reasoning or verbose plans. Act directly via "
    "tool calls.\n\n")

BOUNDS = """## Bounds (read first)
Lane repo: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Every path you write is absolute under
that lane; a write anywhere else is a defect (never write the fleet root, a sibling lane, or /tmp).
Work from /home/vgpnk/Projects/shokunin/kaidoku-shokunin; seat tools start at the fleet root, so
relative paths are wrong.
Scratch: create ONE dir `/fast/scratch/hyaku/kaidoku-r77/<your-seat-name>/` (mkdir -p), pass it
explicitly (TMPDIR=... and any --work), and delete it with `trap 'rm -rf -- "$S"' EXIT` (or a
finally:) before you yield; receipts first copied under
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/w1/<your-seat-name>/.
Never run `git`/`jj` writes, never commit, push, stash or check out anywhere; read-only git
(`log`, `show`, `diff`, `status`, `ls-files`, `rev-parse`) is fine. Never touch
/home/vgpnk/Projects/shokunin/.ufo/state/, .ufo/watchdog.log, MANIFEST.json, templates/,
scripts/, or another lane. Never message agent://all. Never edit production files:
the L1 lands every lane edit; you write only under your own evidence dir. Editing a lane file,
even to "fix" a defect you found, is a blocking defect of your seat.
Any git fixture repo you create is `D=$(mktemp -d)` under your scratch root and every later call
names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first
commit, and never commit anywhere else.
Security (round-72 incident, QUALITY row 128): never write a raw environment dump into the lane. A
probe that must show an environment writes the KEY NAMES and the canary presence only; values stay
out of every committed file.
Tooling authorization (operator 2026-10-19): you may install or upgrade tools that help the task;
read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate, record
tool/version/channel/reason in your report). PACMAN IS PAUSED host-wide: no pacman transaction of
any kind; use uv tool / npx / an official binary in ~/.local/bin. No system-wide upgrades.
Every `Report:` trailer path a validator renders is relative to
/home/vgpnk/Projects/shokunin/kaidoku-shokunin - write it at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/<that path>. Your final answer is a short JSON:
files_written, findings, evidence, risks.
"""

FROZEN = """## Frozen state (round 77)
base `188562d43e3cc58b217ad7aa763fb296c5b8a0b7` (the round-76 lane tip, after the round-76
non-author spot-check lesson); declaration `819cf30e2fc35d91a69df1b2a42a025741c7d0ef` (both
instruments, `plans/round-77-claims.md`, the two selftests, the two do-nothing controls, the
census-start and the three source snapshots - committed BEFORE any claim data); freeze
`6767a879c6a3f386a9c3fc9d332c794f2d9ea914` (`.ufo/waves/round-77/claims.json` with both frozen
predicates and instrument pins, plus the two base receipts; the round-29 gate audits it CLEAN,
findings [], three instrument paths).
Claims (frozen sentences in `plans/round-77-claims.md` and `.ufo/waves/round-77/claims.json`):
R77-C1 calibration - `tools/round-77/verdict-bind.py` re-derives a claimed verdict from the JSON
  receipt its evidence cell names; base 188562d4 exits 1 with `mismatch_count 4` naming the
  `capability-row binding` row and PROVINCE.md line 585 (`D24 true` vs `false`,
  `mismatch_count 0` vs `1`); the landing target is exit 0, `mismatch_count 0`,
  `bound_clauses >= 18`, `in_scope_rows >= 11`, `validate` defect-free; the selftest's 15 cases
  carry one red fixture per failure shape plus legitimate look-alikes.
R77-C2 operability - `tools/round-77/prefile-receipt.py` runs `tools/round-29/prefile-check.sh`
  under a four-key child environment and retains a receipt binding argv, rev, exit, verdict line
  and stdout digest; base 188562d4 exits 1 with `arms_ok 4 of 6` (filing receipt absent, three
  round-76 gate receipts without exit); the landing target is exit 0, `arms_ok 6 of 6`, `validate`
  defect-free; the selftest's 13 cases carry both red fixtures and their legitimate look-alikes.
Round-76 routed defects under repair (outside document, `corpus/lessons/round-76-verifier-spotcheck.md`
section 6): 1 the landing receipt cited as green in three files; 2 loose tip-receipt revision prose
in the filed report; 3 the gate-at-tip `exit 0` is not in its receipt; 4 the prefile check retains
no receipt; 5 D24 admits a false verdict written beside a resolving path.
"""

ROLE_TEXT = {
    "scout": "Read-only reconnaissance. Name what the surface holds and what it misses; run the "
             "commands you cite.",
    "connector": "Cross-lane pattern finding, read-only across sibling lanes; absorb nothing.",
    "executor": "Write and run code fixtures under your own evidence dir; never edit a lane file.",
    "reviewer": "Independent re-derivation. Re-run the counter yourself and check the bytes.",
    "critic": "Adversarial falsification. Your job is to find the claim false or the counter blind.",
    "mutation-tester": "Mutate copies in scratch and show each mutant killed by a named case.",
    "sentinel": "Adversarial security and scope review of the two instruments and the wave bounds.",
    "scribe": "Draft prose/registry rows under your own evidence dir; the L1 lands them.",
    "revenger": "Reverse-engineer the record's own behaviour and history from committed bytes.",
}

ITEMS = [
    {
        "name": "ScoutSurfaces",
        "role": "scout",
        "task": """## Target
Map the five round-76 routed defects onto the two round-77 instruments and the record cells they
bind. Work read-only; write only under
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/w1/ScoutSurfaces/.

## Change
1. Read `corpus/lessons/round-76-verifier-spotcheck.md` section 6 (the five defects) and the two
   instruments `tools/round-77/verdict-bind.py` and `tools/round-77/prefile-receipt.py` at the
   freeze `6767a879`.
2. Enumerate EVERY mention of the false landing-receipt annotation across the lane's tracked
   markdown: run, and paste, `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin grep -n` (or
   `grep -rn`) for the spellings `c1-at-landing`, `D24 true, mismatch_count 0`, `0 mismatches,
   nine atoms` across `SCORECARD.md`, `PROVINCE.md`, `LOG.md`, `corpus/lessons/round-76*.md`,
   `corpus/knowledge/*r76*`, `SKILL.md`, `corpus/README.md`. Classify each hit: in C1's frozen
   scope (SCORECARD `## Capabilities` row first-working round >= 73; PROVINCE `- **Core — `
   bullets) or outside it (a record correction the L1 must append).
3. Name what the instruments cannot see: for each instrument list at least two surfaces/classes
   its frozen scope excludes, with the command that shows the exclusion.
4. Check the C1 scope arithmetic yourself: from `SCORECARD.md` at `6767a879`, count the
   `## Capabilities` data rows, the rows whose 4th cell numeral is >= 73, and the bound clauses
   the instrument reports (`--rev 6767a879`), and say whether 9 in-scope rows / 21 bound clauses
   reproduce.

## Acceptance
A receipt JSON with: `mentions` (path:line, spelling, in_scope bool, for every hit), `blind_spots`
(two per instrument with the command and its output tail), `scope_arithmetic` (`rows`, `in_scope`,
`bound_clauses`, `reproduced` bool). Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/w1/ScoutSurfaces.md.""",
    },
    {
        "name": "ConnectorCross",
        "role": "connector",
        "task": """## Target
Sibling-overlap scan: does any other shokunin lane already hold a verdict-binding or
prefile/gate-receipt instrument that this round duplicates, and does any sibling hold a stronger
form of the same rule?

## Change
1. Read-only scan of /home/vgpnk/Projects/shokunin/*-shokunin/ (never write there): grep for
   `--check-receipt`, `prefile`, `freeze-gate`, `mismatch_count`, `verdict`, `evidence cell` in
   each lane's `tools/`, `plans/round-*-claims.md` and `corpus/QUALITY.md` (limit to the 12
   newest round dirs per lane if a lane is huge).
2. For every hit, name the lane, the path, the round, and what its rule binds (or does not).
3. State explicitly whether kaidoku's two instruments are novel, a weaker duplicate, or a stronger
   form, with the sibling path you read.
4. Absorb nothing; write no lane file outside your evidence dir.

## Acceptance
Receipt JSON with `siblings` (lane, path, round, binds), `novelty` (verdict per instrument plus
the sibling path), `contested_scope` (any cross-lane scope question, or `none`). Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/w1/ConnectorCross.md.""",
    },
    {
        "name": "ExecC1Grammar",
        "role": "executor",
        "task": """## Target
Attack `tools/round-77/verdict-bind.py`'s annotation grammar with constructions a token-presence
predicate would accept, and show the parser/binder rejects each (import the module in-process with
`python3 -I -B -c` or a scratch copy; never edit the lane file).

## Change
1. Fixtures to score (each against a synthetic receipt you build in scratch, and the real
   receipts where named):
   a. a cell that NEGATES the field (`no defects, mismatch_count 0` where the receipt is
      defective) - show which clause binds and whether the negation escapes as prose;
   b. a clause outside the parenthesised group;
   c. a second group whose path differs from the first;
   d. the same clause twice with contradictory values;
   e. nested parentheses;
   f. a bare path (no backticks) next to a backticked path;
   g. the PROVINCE continuation-line form (two lines, group on the second);
   h. a row whose first-working round is 72 (out of scope) carrying a false annotation;
   i. an unknown field (`survivor 1`) - must be unbound, never a pass;
   j. `mismatch_count true` against an integer 1 - must be a defect (typed comparison).
2. For each fixture say what a token-presence or substring predicate would do and what this
   grammar does; a fixture that passes when it should not is a BLOCKING defect with its input,
   the call and the output.
3. Run `--selftest` and paste its JSON; confirm 15 cases, 0 failures.
4. Run the counter at `--rev 6767a879` (the freeze) and paste `mismatch_count`, `bound_clauses`,
   `in_scope_rows` and the defect labels.

## Acceptance
Receipt JSON with `fixtures` (id, input, expected, observed, pass bool), `selftest`, `freeze_run`.
Report at /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/w1/ExecC1Grammar.md.""",
    },
    {
        "name": "ExecC2Receipt",
        "role": "executor",
        "task": """## Target
Forge prefile receipts and show `tools/round-77/prefile-receipt.py --check-receipt` refuses each,
while a genuine receipt is accepted.

## Change
1. Produce a genuine receipt: run the gate on a `git clone --shared` of the lane at `6767a879`
   into your scratch (`--work`), or use `.ufo/waves/round-77/pre/c2-at-base.json`'s `clone-run`
   detail if it already carries one; then doctor copies:
   a. `exit` removed;
   b. `exit` as the string "0";
   c. `exit` as `true`;
   d. `passed` flipped;
   e. `stdout` replaced while `stdout_sha256` kept;
   f. `rev` transplanted to a wrong 40-hex;
   g. `env_keys` cut to three keys;
   h. `argv` naming another script;
   i. `prefile_line` set to `prefile: FAIL` while exit is 0;
   j. `stdout` carrying `prefile: PASS` inside prose (not a verdict line).
2. For each doctor, run `--check-receipt` and paste the defect list; name which clause caught it.
3. Show the genuine receipt passes `--check-receipt` (the legitimate look-alike), and show a
   genuinely FAILING receipt (exit 1, verdict FAIL) also passes validation - a fail is a valid
   receipt.
4. Run `--selftest` and paste its JSON (13 cases, 0 failures).

## Acceptance
Receipt JSON with `forgeries` (id, doctor, defects, caught_by), `genuine`, `selftest`. Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/w1/ExecC2Receipt.md.""",
    },
    {
        "name": "ExecControls",
        "role": "executor",
        "task": """## Target
Score the do-nothing controls of both claims against the frozen targets, and show neither control
reaches them.

## Change
1. C1: regenerate the two controls with
   `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-77/gen-controls.py
   --root . --base 188562d43e3cc58b217ad7aa763fb296c5b8a0b7 --out-dir <your scratch>/controls`
   and run both control instruments at the base; paste `mismatch_count`, `bound_clauses` and
   `meets_target` for each. Then run round 76's own `tools/round-76/record-audit.py --rev 188562d4`
   and paste its verdict (the pointer-only control: D24 true, 0 mismatches, false annotation
   standing).
2. C2: run `prefile-check.sh` on a clean shared clone at the base exactly as round 76 did, paste
   its `prefile:` line and exit, and show the battery's `record-receipt` arm stays unmet because no
   receipt was retained. Then build a forged battery receipt (copy
   `.ufo/waves/round-77/pre/c2-at-base.json`, set `arms_ok` to 6 while an arm row says
   `met false`) and run `--validate-battery` on it; paste the defects.
3. State in one line per claim whether a do-nothing control can reach the frozen target.

## Acceptance
Receipt JSON with `c1_controls` (control, mismatch_count, bound_clauses, meets_target),
`pointer_only`, `c2_gate_alone`, `forged_arms_defects`, `targets_reachable_by_control` (bool).
Report at /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/w1/ExecControls.md.""",
    },
    {
        "name": "ReviewerC1",
        "role": "reviewer",
        "task": """## Target
Independently re-derive R77-C1 from committed bytes and check every defect the counter names.

## Change
1. Run the frozen counter yourself:
   `python3 -I -B tools/round-77/verdict-bind.py --root . --rev <rev> --json-out <scratch>/c1.json`
   at `188562d4` (base) and at `6767a879` (freeze). Paste both summaries.
2. For each of the four base defects, re-derive claimed vs actual by hand from the receipt bytes:
   `git -C . show 188562d4:.ufo/waves/round-76/l1/scores/c1-at-landing.json | python3 -m json.tool`
   and the `D24_capability_rows` atom; state whether the receipt really records `ok false` /
   `mismatch_count 1` / the two absent evidence paths.
3. Independently count the in-scope population: extract the `## Capabilities` table yourself
   (`awk`/`python`) and list the rows with first-working round >= 73; check the instrument's
   `in_scope_rows` and `bound_clauses` against your own count.
4. Read the instrument's scope and grammar code and name any clause it does not actually re-derive
   (a place where the printed verdict could still be false while the counter is green).
5. State what the landing target requires and whether the current record can reach it without the
   three-cell correction.

## Acceptance
Receipt JSON with `runs` (rev, exit, mismatch_count, bound_clauses, in_scope_rows),
`defects_reverified` (label, claimed, actual, agree bool), `population_check`, `blind_clauses`.
Report at /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/w1/ReviewerC1.md.""",
    },
    {
        "name": "ReviewerC2",
        "role": "reviewer",
        "task": """## Target
Independently re-derive R77-C2 and audit every arm's observation at the base.

## Change
1. Run the battery yourself with a fresh work dir:
   `python3 -I -B tools/round-77/prefile-receipt.py --root . --rev 188562d4 --work <scratch> --battery --json-out <scratch>/c2.json`
   and paste `arms_ok`, `arms_total`, and each arm's `met` with its `observed` text.
2. Verify arm by arm: (a) the clone run really ran the gate on a clean clone (show the clone's
   `git status --porcelain` empty and the receipt's `rev`); (b) the record receipt really is
   absent at 188562d4; (c) the gate receipts really lack `exit` - list them from
   `git ls-tree 188562d4 .ufo/waves/round-76/l1/scores` and paste each file's absence of an
   `exit` line; (d) each red fixture is refused for its declared reason.
3. Read `check_receipt` and name every clause it re-derives and every clause it takes on trust.
4. State what the landing target requires, and whether a filing receipt with exit 0 plus round-77's
   gate receipts carrying `exit` would satisfy it (given the newest-round-dir rule).

## Acceptance
Receipt JSON with `battery` (arms_ok, arms_total, arms), `clone_evidence`, `gate_receipts`
(path, carries_exit bool), `trusted_clauses`. Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/w1/ReviewerC2.md.""",
    },
    {
        "name": "CriticClaims",
        "role": "critic",
        "task": """## Target
Falsify both claims. Find a pass that is false or a target a do-nothing control reaches.

## Change
1. C1 over-set hunt: construct an annotation in C1's frozen scope that the grammar binds and the
   counter passes while the record is false (a field alias, an atom shorthand that matches the
   wrong atom, a group whose nearest preceding path is the wrong receipt, a qualifier that hides a
   contradiction, a `validate defect-free` on a receipt whose `validate` block is absent or
   non-defect-free). For each, say whether the frozen grammar accepts it and why.
2. C1 under-set hunt: an annotation whose falsehood the grammar cannot see but that a reader would
   read as a verdict (the scope floor boundary: a round-72 row; a PROVINCE bullet outside
   `- **Core — `; a claim-table cell). Name the surface left unbound and whether the frozen
   predicate claims it.
3. C2 hunt: an arm that can pass without its observation (empty gate set, a gate receipt with
   `exit=0` inside prose, a filing receipt measured at a different rev, a receipt whose stdout
   digest matches but whose `passed` is stale).
4. Coupling check: state whether C1 can pass with C2's work absent and vice versa, and show it by
   running C1 at `6767a879` (no round-77 gate receipts) and C2 with the false annotation still in
   the record.
5. Verdict per claim: SURVIVES or FALSIFIED, with the fixture path and output.

## Acceptance
Receipt JSON with `c1_over_set`, `c1_under_set`, `c2_attacks`, `coupling`, `verdicts`. Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/w1/CriticClaims.md.""",
    },
    {
        "name": "MutationTester",
        "role": "mutation-tester",
        "task": """## Target
Mutate both round-77 instruments and show each mutant is killed by a named selftest case.

## Change
1. In scratch, copy `tools/round-77/verdict-bind.py` and produce at least six mutants, each
   changing one decision: drop the typed check (`typed_equal` -> `==`); drop the atom lookup
   (always top-level field); make `--rev` resolution use the working tree instead of `show`;
   ignore the `_total` key in the `of` form; treat an unknown field as a pass; skip the
   `absent_receipt` defect (treat a missing receipt as clean).
2. For each mutant, run `--selftest` and record which case names fail. A mutant that still exits 0
   is a SURVIVOR: name it, with the exact code change and the selftest output.
3. Do the same for `tools/round-77/prefile-receipt.py` with at least four mutants: accept a
   non-integer `exit`; skip the stdout digest; accept a verdict line that disagrees with `exit`;
   skip the `env_keys` check.
4. Confirm the pristine instruments' selftests pass (15 and 13 cases, 0 failures) and that no
   mutant shares a survivor with another (sole-detector field per mutant).

## Acceptance
Receipt JSON with `mutants` (instrument, name, change, killed_by, survivors list), `pristine`
(c1, c2), `survivor_count`. Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/w1/MutationTester.md.""",
    },
    {
        "name": "SentinelScope",
        "role": "sentinel",
        "task": """## Target
Security and scope review of the two instruments and the wave's bounds.

## Change
1. Read both instruments at `6767a879`. Verify and cite line numbers for: no `shell=True`; no
   bare-name execution of a caller-supplied path; the four-key child environment and that no raw
   environment value is written; `cwd`/`TMPDIR` containment under the work root for every child;
   `git clone --shared` reads the lane but writes only the clone; no write outside `--root`,
   `--work`, `--json-out`; `--filing`'s output path; the receipt checker's inability to read
   outside the lane (or a named limit).
2. Probe the refusals: run the C1 counter with `--rev` absent (expect exit 2), with an unknown rev
   (expect exit 2 or a named unevaluable), and the C2 battery with `--work` absent (expect exit 2);
   paste the outputs.
3. Check the wave's own bounds: does any instruction in the spec let a seat write outside its
   evidence dir, or install a tool through pacman? Name the exact spec lines.
4. Name the bypasses the instruments do not cover (copying a receipt elsewhere, a receipt produced
   by another tool, a caller who edits the instrument before measuring) and say whether the claims
   overstate.

## Acceptance
Receipt JSON with `clauses` (line, property, evidence), `refusals`, `bounds_check`,
`uncovered_bypasses`, `overstatement` (bool + reason). Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/w1/SentinelScope.md.""",
    },
    {
        "name": "ScribeSources",
        "role": "scribe",
        "task": """## Target
Draft the round's three SOURCES rows and two knowledge entries under your evidence dir; the L1
lands them.

## Change
1. Open the three committed snapshots under
   /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/l1/sources/
   (`rfc8259.txt`, `page-721dd237.html` bash manual, `page-298eb5f5.html` ast docs) and verify the
   candidate quotes byte-exactly with `grep -n`/`sed -n`, recording line numbers:
   - RFC 8259 section 3 Values line 298: `A JSON value MUST be an object, array, number, or string, or one of`;
   - Bash 3.7.5 Exit Status line 4435: `Bash itself returns the exit status of the last command`;
   - ast `literal_eval` line 2760: `Evaluate an expression node or a string containing only a Python literal or`.
2. Draft three registry rows in the lane's 11-column schema (copy the exact header from
   `corpus/SOURCES.md` at the freeze: id, title — url, kind, tier, scope, anchor, teaches,
   status, opened, recheck, used-by). Rows: RFC 8259 section 3 (admit, `mined`, scope: JSON value
   types — booleans are literal names, not numbers; supports the typed comparison in
   `tools/round-77/verdict-bind.py`), bash manual (admit, `mined`, scope: a shell process's exit
   status is the last command's; supports `prefile-receipt.py`'s exit binding), ast docs (REJECT
   with reason and flip: the annotation grammar is not a Python literal grammar, and
   `literal_eval` would accept Python-only spellings the records do not use; flip when the grammar
   becomes a Python literal grammar). Every cell must contain no literal or escaped `|`.
3. Check the registry for id collisions with your proposed ids (use the next free S-numbers by
   reading `corpus/SOURCES.md`; do not assume a number) and for URL duplicates (the RFC and JSON
   URLs are already held - name the existing ids and the W04 warning class).
4. Draft two knowledge entries (one per admitted row) with a `## Gate` block carrying the URL, the
   access date 2026-11-04, the snapshot sha256 and the located quote with its line.
5. The reject row's Gate records the consumer search: run and paste
   `grep -c 'literal_eval' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-77/verdict-bind.py`
   (expected 0) and say the row is not needed.

## Acceptance
Files under your evidence dir: `sources-rows.md` (three rows), `knowledge-rfc8259-section3.md`,
`knowledge-bash-exit-status.md`, `receipt.json` with `quotes` (source, line, bytes-verified bool,
snapshot sha256), `ids` (proposed, collision check), `duplicate_urls`. Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/w1/ScribeSources.md.""",
    },
    {
        "name": "RevengerRecord",
        "role": "revenger",
        "task": """## Target
Reverse-engineer the record's correction history and propose the exact correction texts the L1
must land for routed defects 1 and 2, under the lane's traceability rules.

## Change
1. Read `corpus/lessons/round-76-verifier-spotcheck.md` section 6 defect 1 and 2, the round-76
   claim table in `SCORECARD.md`, the `capability-row binding` row in `## Capabilities`, the
   PROVINCE round-76 addition, and `corpus/lessons/round-76.md`.
2. Read `corpus/QUALITY.md` rows 34, 35, 36, 65 and 74 (reversal traceability, append-only,
   corrections sweep every mention) and say exactly what form the correction must take: which
   cells may be edited in place, what the appended correction section must contain, and what may
   never be rewritten (the filed round-76 report).
3. Extract, from committed bytes, the true values each citation should carry:
   `git show <rev>:.ufo/waves/round-76/l1/scores/c1-at-tip.json` (rev, exit, mismatch_count,
   atom count, D24 ok) and `c1-at-landing.json` (rev, exit, mismatch_count, D24 ok, and the
   evidence paths' first commit). Paste the jq/JSON output.
4. Propose the exact old -> new text for: (a) the R76-C1 before->after cell; (b) the
   `## Capabilities` row `capability-row binding` evidence cell; (c) the PROVINCE round-76
   evidence lines; (d) the LOG.md sentence(s) carrying the tip-receipt revision prose; and the
   appended correction section's bullets. Mark which are in-place edits and which are appended.
5. Name any hit your sweep finds that the spot-check did not name (other files citing the landing
   receipt as green).

## Acceptance
Receipt JSON with `true_values`, `corrections` (surface, old, new, mode in-place|append),
`extra_hits`, `rules_applied`. Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-77/w1/RevengerRecord.md.""",
    },
]


def main() -> None:
    items = []
    for item in ITEMS:
        items.append({
            "name": item["name"],
            "role": item["role"],
            "prompt": (GODSPEED + BOUNDS + FROZEN
                       + f"## Role\n{ROLE_TEXT[item['role']]}\n\n"
                       + item["task"]),
        })
    spec = {
        "wave": WAVE,
        "milestone": ("r77-w1: verdict binding and the prefile receipt become runnable, "
                      "red-fixtured instruments; independent re-derivation, forgery attacks, "
                      "mutation scoring, security review, source rows, record correction plan."),
        "reportDir": REPORT_DIR,
        "context": FROZEN + "\n" + BOUNDS,
        "items": items,
    }
    out = pathlib.Path(__file__).with_name(f"{WAVE}-spec.json")
    out.write_text(json.dumps(spec, indent=1) + "\n")
    print(json.dumps({"spec": str(out), "items": len(items),
                      "roles": sorted({i["role"] for i in items})}))


if __name__ == "__main__":
    main()
