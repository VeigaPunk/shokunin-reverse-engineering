#!/usr/bin/env python3
"""Generate the round-76 wave-1 spec (r76-w1): 14 seats, one v1 wave."""
import json
import pathlib

WAVE = "r76-w1"
REPORT_DIR = ".ufo/waves/round-76/w1"
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
Lane repo: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Every path you write is absolute under that lane; a write anywhere
else is a defect (never write the fleet root, a sibling lane, or /tmp). Work from
/home/vgpnk/Projects/shokunin/kaidoku-shokunin; seat tools start at the fleet root, so relative paths are wrong.
Scratch: create ONE dir `/fast/scratch/hyaku/kaidoku-r76/<your-seat-name>/` (mkdir -p), pass it explicitly
(TMPDIR=... and any --work), and delete it with `trap 'rm -rf -- "$S"' EXIT` (or a
finally:) before you yield; receipts first copied under
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-76/w1/<your-seat-name>/.
Never run `git`/`jj` writes, never commit, push, stash or check out anywhere; read-only
git (`log`, `show`, `diff`, `status`, `ls-files`, `rev-parse`) is fine. Never touch
/home/vgpnk/Projects/shokunin/.ufo/state/, .ufo/watchdog.log, MANIFEST.json, templates/,
scripts/, or another lane. Never message agent://all. Never edit production files:
the L1 lands every lane edit; you write only under your own evidence dir.
Any git fixture repo you create is `D=$(mktemp -d)` under your scratch root and every
later call names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D`
before the first commit, and never commit anywhere else.
Security (round-72 incident, QUALITY row 128): never write a raw environment dump into
the lane. A probe that must show an environment writes the KEY NAMES and the canary
presence only; values stay out of every committed file.
Tooling authorization (operator 2026-10-19): you may install or upgrade tools that help
the task; read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety
gate, record tool/version/channel/reason in your report). PACMAN IS PAUSED host-wide:
no pacman transaction of any kind; use uv tool / npx / an official binary in ~/.local/bin.
Every `Report:` trailer path a validator renders is relative to /home/vgpnk/Projects/shokunin/kaidoku-shokunin - write it at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/<that path>. Your final answer is a short JSON: files_changed, behavior, evidence,
risks.
"""

FROZEN = """## Frozen state (round 76)
base `5303a662d43aac52b0667f2776cce49dfc004fcf` (the round-75 lane tip); declaration
`be99e4f9b72fb2dbae75329c0d5c55002854cbed` (the two round-76 instruments, plans/round-76-claims.md,
the two fixtures and the census-start receipt, committed BEFORE any claim data); a pre-freeze
instrument revision `58316c9218e0345bcdc1ff43357c8ca815481f86` (C2's green arm made
executability-only so the claims stay separable; receipts carry their own exit); freeze
`5824d5d8e135194a59db3df1533b76ff479753bf` (claims.json + the base and declaration receipts;
the round-29 gate audits it CLEAN, findings [], two instrument paths).
Claims (frozen sentences in plans/round-76-claims.md and .ufo/waves/round-76/claims.json):
R76-C1 calibration -- the record audit's new atom D24_capability_rows re-derives the SCORECARD
  `## Capabilities` table against every round section that says "Capabilities rows appended":
  at base 5303a662 the audit exits 1 with mismatch_count 1 naming exactly D24 (defects name the
  two absent rows `A12 case-independence closure` and `exact-grammar record audit`); at the
  landing revision it exits 0 with mismatch_count 0 over nine atoms D16-D24 and a defect-free
  validate block; six red fixtures in the selftest, one per failure shape.
R76-C2 operability -- the printed counting command executes as printed:
  tools/round-76/plan-command.py --battery scores three arms (plan-c1: the plan's own
  counting-command block executes verbatim, rc 0 or 1, integer mismatch_count; r75-printed: the
  round-75 report's printed command refused with PLACEHOLDER_UNBOUND and nothing executed;
  r75-argv: the same command with the digest bound executes and fails rc 2 with
  `missing required arguments: work`); base 5303a662 arms_ok 0, landing arms_ok 3.
Instruments (committed before the freeze; `python3 -I -B`):
 tools/round-76/record-audit.py (the round-75 audit + D24 + six capability red fixtures; 17-case
 selftest), tools/round-76/plan-command.py (block extractor, static grammar, shlex/no-shell
 executor, four-key child env, counter reader, battery, three controls, 3-case selftest).
Pre receipts (committed at the freeze): .ufo/waves/round-76/pre/c1-at-base.json (mismatch 1,
D24 only), c1-at-declaration.json (1), c1-control-r75audit-at-base.json (the round-75 audit is
GREEN at base with both rows absent -- the do-nothing control), c2-at-base.json (arms_ok 0),
c2-at-declaration.json (arms_ok 3), controls-at-declaration.json (three C2 controls met, C1
selftest 17 cases, gate selftest 3 cases), control-prose-plan.json,
control-missing-required-arg.json, control-ellipsis-rev.json, r75-printed-exec.txt (the hand run
of the round-75 printed command: exit 2, `missing required arguments: work`), audit-selftest.json,
gate-selftest.json, and the two fixtures .ufo/waves/round-76/pre/fixtures/r75-printed.md /
r75-argv.md.
The outside document this round works from: corpus/lessons/round-75-verifier-spotcheck.md
sections 1-6 (eight routed defects; 1 and 2 -> R76-C1, 4 -> R76-C2, 3/5/6/7/8 -> unclaimed
record corrections).
Frozen source pages opened this round: shlex.split
 https://docs.python.org/3/library/shlex.html#shlex.split (candidate S286) and argparse
 https://docs.python.org/3/library/argparse.html (candidate S287); sh(1)
 https://man7.org/linux/man-pages/man1/sh.1.html (candidate reject S288).
Hyperfocus your assignment; never deviate. Return a short JSON
(files_changed, behavior, evidence, risks) and delete your scratch dir before you yield.
"""

ITEMS = []


def item(name, role, body):
    ITEMS.append({"name": name, "role": role,
                  "prompt": GODSPEED + BOUNDS + FROZEN + "\n## Assignment: " + name +
                            f" ({role})\n" + body.strip() + "\n"})


item("ExecCapGrammar", "executor", """
## Target
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-76/record-audit.py (read-only) and
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-76/w1/ExecCapGrammar/.

## Change
Attack D24's grammar with COSMETIC constructions a token-presence predicate would accept, and show
`capability_defects()` rejects each (import the module in-process with `python3 -I -B -c` or a
scratch copy; never edit the lane file):
 1. a claim line naming a row that does not exist in the table;
 2. a row whose evidence cell is `—` (no path);
 3. a row whose evidence path does not resolve (`exists` returns False);
 4. a row whose first-working-round cell names 74 while the claim sits in a round-75 section;
 5. a stub description of three words;
 6. a table with no data rows;
 7. a section with no claim line at all.
Also run the six committed `cap-*` selftest case names through `--selftest` and read the live
claim line at the freeze rev (`git show 5824d5d8:SCORECARD.md`, line 5868): it wraps across two
source lines and the backticked name `A12 case-independence\\nclosure` straddles the wrap -- show
that the paragraph-level parser recovers both names and that a line-level parser does not.
Probe two ACCEPT fixtures (a well-formed row; the two real names) to show the grammar is not
rejecting everything.

## Acceptance
Each cosmetic fixture returns at least one defect naming the failed shape; each accept fixture
returns none; the wrapped claim line yields exactly the two names. A cosmetic fixture that passes
is a BLOCKING defect with its input and output. Receipt at
.ufo/waves/round-76/w1/ExecCapGrammar/receipt.json.

## Evidence
Write .ufo/waves/round-76/w1/ExecCapGrammar.md plus the receipt.
""")

item("ExecPlanArms", "executor", """
## Target
tools/round-76/plan-command.py (read-only) and .ufo/waves/round-76/w1/ExecPlanArms/.

## Change
Independently reproduce C2's three arms WITHOUT using `--battery`:
 1. read `.ufo/waves/round-76/pre/fixtures/r75-printed.md` at the freeze rev, `shlex.split` its
    block after joining `\\`-continuations, and show (a) the Unicode ellipsis is present in the
    argv and (b) executing that argv with `subprocess.run(..., shell=False)` exits 2 with
    `missing required arguments: work` (the gate refuses it statically instead);
 2. the same for `r75-argv.md` (digest bound, no `--work`): it EXECUTES and exits 2;
 3. extract the plan's `counting-command: C1` block at the freeze rev, execute its argv verbatim
    with only `$REV`/`$OUT` substituted, and read the receipt's `mismatch_count` (at the freeze
    it is 1; at the landing it will be 0 -- the value is C1's business).
Then check the gate's own claims about itself: run `--battery`, `--selftest` and one `--control`;
confirm the receipt's `argv[0:3] == ["python3","-I","-B"]` and that no shell is ever spawned
(`strace -f -e trace=execve` if available, else argue from the source that `shell=True` appears
nowhere: `grep -c 'shell=True' tools/round-76/plan-command.py` must be 0).

## Acceptance
Rows 1-3 reproduce the declared rc and message; the gate's battery at the freeze rev reports
arms_ok 3; `grep -c 'shell=True'` 0; the receipt's argv is the four-part python3 -I -B form. Any
deviation is a defect with its exact output. Receipt at
.ufo/waves/round-76/w1/ExecPlanArms/receipt.json.

## Evidence
Write .ufo/waves/round-76/w1/ExecPlanArms.md plus the receipt.
""")

item("ExecBaseArms", "executor", """
## Target
both round-76 instruments and .ufo/waves/round-76/w1/ExecBaseArms/.

## Change
Re-run the four counter invocations and compare each with its committed pre receipt:
 A) `python3 -I -B tools/round-76/record-audit.py --root . --rev 5303a662 --json-out <yours>` ->
    expect exit 1, mismatch_count 1, mismatches == ["D24_capability_rows"], validate {atoms 9,
    defects []}, and D24's defects naming BOTH rows;
 B) the same at `5824d5d8` -> expect the same single mismatch;
 C) `python3 -I -B tools/round-76/plan-command.py --root . --rev 5303a662 --work <yours>
    --battery --json-out <yours>` -> expect exit 1, arms_ok 0, all three arms
    BLOCK_ABSENT/FIXTURE_ABSENT;
 D) the same at `5824d5d8` -> expect exit 0, arms_ok 3.
Also run `tools/round-75/record-audit.py --rev 5303a662` (the do-nothing control): it must report
mismatch_count 0 over eight atoms while the two rows are absent. Compare every field of your
receipts with the committed ones and report any difference (paths under `root` may differ; nothing
else may).

## Acceptance
A-D match their committed receipts field for field (except `root`); the round-75 audit is green at
base. Any drift is a defect with the differing field. Receipt at
.ufo/waves/round-76/w1/ExecBaseArms/receipt.json.

## Evidence
Write .ufo/waves/round-76/w1/ExecBaseArms.md plus the receipt.
""")

item("ExecAuditAtoms", "executor", """
## Target
tools/round-76/record-audit.py (read-only) and .ufo/waves/round-76/w1/ExecAuditAtoms/.

## Change
Show that the eight inherited atoms D16-D23 still hold at base `5303a662` and at the freeze, and
that D24 is the ONLY false atom at both: read each atom's `evidence` block from your own run and
state, for each, which committed artifact it re-derives (round-75 receipts, the round-75 lesson,
the round-75 claims container, the freeze ledger) and that the artifact is unchanged between the
base and the freeze (`git diff --stat 5303a662 5824d5d8 -- <each path>` must be empty). Then check
D24's own evidence is not vacuous: its `claims` block must name the round-75 line 5868 and both
row names, and its `table_rows` must be the real `## Capabilities` first cells (count them:
`awk` over the table at the freeze rev).

## Acceptance
Eight atoms true at both revisions, D24 false at both, every D16-D23 artifact byte-identical
between base and freeze, the `## Capabilities` row count equal to the table's actual data rows.
Any atom true for a mechanical reason (wrong path, wrong regex) is a defect. Receipt at
.ufo/waves/round-76/w1/ExecAuditAtoms/receipt.json.

## Evidence
Write .ufo/waves/round-76/w1/ExecAuditAtoms.md plus the receipt.
""")

item("ScribeRows", "scribe", """
## Target
the two SOURCES.md rows and .ufo/waves/round-76/w1/ScribeRows/.

## Change
Fetch each page once with `curl -sS -o <scratch>/<name>.html -w '%{http_code} %{size_download}\\n'`
and record the sha256:
 1. https://docs.python.org/3/library/shlex.html#shlex.split -- admit, docs, tier A, scope
    "argv tokenisation without a shell", status mined, used-by
    corpus/knowledge/2026-11-04-r76-plan-command-executability.md; quote (<=25 words, contiguous,
    located) from the `shlex.split` entry.
 2. https://docs.python.org/3/library/argparse.html -- admit, docs, tier A, scope "exit status 2
    on a parser error", status mined, same used-by; quote from `ArgumentParser.error` /
    `exit(status=0, message=None)` naming status 2.
 3. https://man7.org/linux/man-pages/man1/sh.1.html -- REJECT, docs, tier C, teaches
    `REJECTED: <reason>; flip: <condition>` (three words each minimum). Reason: the claim's whole
    point is the shell the gate refuses to invoke; record the consumer search
    `grep -c 'shell=True' tools/round-76/plan-command.py` (must be 0) in the Gate row.
Rows must be 11 cells, no `|` inside any cell, ids S286, S287, S288, `opened` 2026-11-04.
Draft them in your evidence dir; do not edit corpus/SOURCES.md.

## Acceptance
Three rows in the exact registry grammar (11 cells, no literal or escaped pipes), each quote
literal and located with its snapshot line, the reject carrying reason+flip and the consumer
search. Receipt at .ufo/waves/round-76/w1/ScribeRows/receipt.json with the snapshots' sha256 and
the quote-to-snapshot line mapping.

## Evidence
Write .ufo/waves/round-76/w1/ScribeRows/rows.md plus the receipt and the snapshots.
""")

item("ScribeLesson", "scribe", """
## Target
the round-76 lesson draft and .ufo/waves/round-76/w1/ScribeLesson/.

## Change
Draft `corpus/lessons/round-76.md` with three sections, from the committed receipts (do not edit
the lane file; write the draft to your evidence dir):
 1. `## Gate` -- a row per SOURCES decision (S286 admit, S287 admit, S288 reject with reason and
    flip), each with URL, access date, located quote and digest; plus the census before/after
    line (191 rows at round start, exit 0, 24 W04 warnings -- `.ufo/waves/round-76/l1/census-start.txt`).
 2. `## Mistakes` -- one row: class, evidence pointer, captured-by, fix. The class this round
    mines: *a self-assessment sentence written before its artifact existed, and a printed command
    never executed by its author* (round-75 routed defects 1 and 4). Captured-by: D24 and the
    plan-command gate, each with the receipt showing it can fail.
 3. `## Routed-defect disposition` -- one row per round-75 routed defect 1-8 with its disposition
    (1,2 -> R76-C1; 4 -> R76-C2; 3,5,6,7,8 -> unclaimed record corrections, each naming the
    correction this round appends).
Keep every number tied to a committed receipt path; no number without its command.

## Acceptance
The draft names a receipt for every claim; the mistake row carries all four fields; every routed
defect has a disposition. Receipt at .ufo/waves/round-76/w1/ScribeLesson/receipt.json.

## Evidence
Write .ufo/waves/round-76/w1/ScribeLesson/lesson-draft.md plus the receipt.
""")

item("ScoutSource", "scout", """
## Target
the three candidate pages and .ufo/waves/round-76/w1/ScoutSource/.

## Change
Per-surface reconnaissance on the source decisions:
 1. Open `shlex.split` and locate: the exact-match sentence, the `posix` default, the
    `comments=False` default, and whether the page says the split is shell-compatible. Report what
    the gate actually relies on and what it must NOT claim (e.g. that shlex implements a shell's
    grammar -- it does not).
 2. Open `argparse` and locate the status-2 statements (`ArgumentParser.error`, `exit`), and check
    whether the page documents `parse_args` exiting 2 on a missing required argument -- the
    before-arm's observed behaviour. Quote what the page actually says.
 3. Open `sh(1)` and locate what the gate must avoid (word splitting, globbing, command
    substitution, pipelines); state why the reject row is right and what would flip it.
 4. Check the lane's existing registry for near-duplicates of these three URLs
    (`grep -n 'shlex\\|argparse\\|man1/sh' corpus/SOURCES.md`), so the ids do not collide.

## Acceptance
A per-page finding file with located quotes (page + line), a statement of what the row may and may
not claim, and the near-duplicate scan output. Any claim the pages do not support is a BLOCKING
defect for the row. Read-only. Receipt at .ufo/waves/round-76/w1/ScoutSource/receipt.json.

## Evidence
Write .ufo/waves/round-76/w1/ScoutSource.md.
""")

item("ConnectorCross", "connector", """
## Target
sibling-overlap scan and .ufo/waves/round-76/w1/ConnectorCross/.

## Change
Scan the fleet for instruments that already do what this round's two instruments do, and name
owners and divergences:
 1. `grep -rl 'counting-command\\|plan-command\\|plan_command' /home/vgpnk/Projects/shokunin/*-shokunin --include='*.py' --include='*.md'`
    and the fleet census `scripts/sources-census.sh` if it has a relevant check; report which
    lanes have a printed-command or plan-command gate and how theirs differs.
 2. Which lanes have a capability-table atom or a record audit that reads their SCORECARD
    (search for `## Capabilities` readers in sibling `tools/`)?
 3. Confirm `considerthese/` is absent in this lane and that `merge/kaidoku/` does not serve these
    claims (read `MERGE-REPORT.md` headings only).
Report overlaps as "duplication with named divergences" or "no overlap"; never absorb another
lane's surface.

## Acceptance
A findings file naming, per question, the searched command, the hits and the divergence. Read-only;
do not edit any lane. Receipt at .ufo/waves/round-76/w1/ConnectorCross/receipt.json.

## Evidence
Write .ufo/waves/round-76/w1/ConnectorCross.md.
""")

item("ReviewerC1", "reviewer", """
## Target
R76-C1 end to end, and .ufo/waves/round-76/w1/ReviewerC1/.

## Change
Re-derive C1 from frozen revisions without trusting the receipts:
 1. Read the frozen predicate in `plans/round-76-claims.md` and `.ufo/waves/round-76/claims.json`
    (they must agree word for word on the atom set and counter).
 2. At base `5303a662`, confirm the SCORECARD `## Capabilities` table has no row whose first cell
    is `A12 case-independence closure` or `exact-grammar record audit`, and that line 5868 claims
    them (`git show 5303a662:SCORECARD.md`).
 3. Re-run the audit at base and at the freeze with your own `--work`; compare with the committed
    pre receipts.
 4. Read D24's code: does it parse (not substring-match) the claim, require a resolving pointer,
    require the claiming round, and refuse a stub description? Name any path by which a forged
    SCORECARD could pass.
 5. Check the six `cap-*` selftest cases are load-bearing (each fails if its check is removed --
    reason from the code, do not patch the lane file).

## Acceptance
A verdict line (verified / not verified) with the exact commands and outputs; every path by which a
forgery could pass named as a finding with severity. Receipt at
.ufo/waves/round-76/w1/ReviewerC1/receipt.json.

## Evidence
Write .ufo/waves/round-76/w1/ReviewerC1.md.
""")

item("ReviewerC2", "reviewer", """
## Target
R76-C2 end to end, and .ufo/waves/round-76/w1/ReviewerC2/.

## Change
Re-derive C2 from frozen revisions without trusting the receipts:
 1. Confirm the frozen predicate matches between plan and container, and that the plan's C2 block
    is exactly the battery command.
 2. Re-run the battery at base and at the freeze; compare with the committed receipts.
 3. Read `plan-command.py`: is the static grammar checked BEFORE any execution? Is `shlex.split`
    used with `shell=False` everywhere? Is the child env exactly four keys? Is containment applied
    to `$WORK`/`$OUT` before the run? Is the argv allowlist enforced before `subprocess.run`?
 4. Attack the executability arm: can a block that cannot run (wrong flag, nonexistent script,
    absolute path, `..`) still be scored `met`? Try each on a scratch copy of the plan and record
    the gate's verdict.
 5. Check the three controls are load-bearing (each fails if its check is removed -- reason from
    the code).

## Acceptance
A verdict line with commands and outputs; every false-met path named as a finding with severity.
Receipt at .ufo/waves/round-76/w1/ReviewerC2/receipt.json.

## Evidence
Write .ufo/waves/round-76/w1/ReviewerC2.md.
""")

item("CriticClaims", "critic", """
## Target
the claims' falsification, and .ufo/waves/round-76/w1/CriticClaims/.

## Change
Falsify both claims:
 1. Build a forged SCORECARD in scratch that makes D24 green while the lane record is wrong (a
    table row with a description that lies; a row whose evidence pointer resolves but does not
    support the capability; a claim line whose names are a superset of the rows). Score it with
    `capability_defects()` and report which forgeries pass -- each is a blocking finding.
 2. Build a forged plan in scratch whose `counting-command: C1` block carries an executable but
    meaningless command (e.g. `true`-like python that writes a receipt with `mismatch_count 0`).
    Does the battery's `plan-c1` arm accept it? If yes, is that within the claim (executability
    only) or a hole in the claim's wording? Say which, with the exact predicate sentence.
 3. Check the base arms cannot be met by a do-nothing round: what is the minimum edit that makes
    `arms_ok 3` at the base revision? If it is "commit the instruments and plan", say so and
    judge whether that is the claimed work.

## Acceptance
A findings file with a verdict per forgery (blocking / non-blocking / within claim) and the exact
predicate sentence it is judged against. Receipt at
.ufo/waves/round-76/w1/CriticClaims/receipt.json.

## Evidence
Write .ufo/waves/round-76/w1/CriticClaims.md.
""")

item("MutationTester", "mutation-tester", """
## Target
the two instruments' own checks, and .ufo/waves/round-76/w1/MutationTester/.

## Change
Mutate scratch copies (never the lane files) and score each mutant against the declared selftest
cases:
 D24 mutants: (a) accept a row absent from the table; (b) drop the evidence-pointer existence
 check; (c) drop the first-working-round check; (d) drop the stub-description check; (e) parse the
 claim at line level instead of paragraph level.
 Gate mutants: (f) skip the static placeholder scan; (g) accept `shell=True`; (h) drop the
 containment check on `$OUT`; (i) drop the argv allowlist.
For each: run `--selftest` on the mutant and record `failures` (a mutant is killed when at least
one declared case fails) and whether the failing case is the one that should catch it
(`sole_detector`).

## Acceptance
Nine mutants scored: each killed by its declared case or reported as a SURVIVOR with its class.
Receipt at .ufo/waves/round-76/w1/MutationTester/receipt.json with (mutant, rc, failures, verdict,
sole).

## Evidence
Write .ufo/waves/round-76/w1/MutationTester.md plus the receipt.
""")

item("SentinelScope", "sentinel", """
## Target
security review of the two instruments, and .ufo/waves/round-76/w1/SentinelScope/.

## Change
The round-76 gate EXECUTES a command read out of a committed document -- review that surface:
 1. Argv allowlist: can a plan block reach an arbitrary binary, an absolute path, a `..` path, a
    script outside `tools/`? Try each on a scratch plan.
 2. Environment: is the child env exactly `PATH/HOME/TMPDIR/LANG`? Is HOME/TMPDIR inside the work
    root? Can the child inherit the caller's secrets?
 3. Containment: `$WORK`/`$OUT` containment is checked with realpath+commonpath -- try a symlink
    escape, an absolute `$OUT`, `..`.
 4. Static grammar: `METACHARS` blocks the semicolon, pipe, ampersand, dollar-paren, backtick and the two redirect signs -- is the list complete for a no-shell executor?
    Is `shlex.split` on the raw block a bypass (e.g. a newline-separated second command)?
 5. D24: `show()` runs `git show` with the path from a table cell -- can a crafted cell escape the
    repo or read outside the lane (path traversal, `--` injection, rev injection)?
 6. Timeout: the child has 300 s -- what does a timed-out run leave behind?
Report severity, path:line and whether a claim depends on it. No exploit run against the host.

## Acceptance
A findings file with a verdict per item (fixed / open / new variant), at least one new observation,
and no exploit executed. Read-only. Receipt at .ufo/waves/round-76/w1/SentinelScope/receipt.json.

## Evidence
Write .ufo/waves/round-76/w1/SentinelScope.md.
""")

item("RevengerProbe", "revenger", """
## Target
one falsifiable hypothesis, and .ufo/waves/round-76/w1/LabratProbe/.

## Change
Hypothesis: *the round-75 printed command fails for exactly the two reasons the gate names, and no
third*. Probe it read-only:
 1. Run the printed argv with the ellipsis: record rc and the exact message (expect exit 2,
    `missing required arguments: work`).
 2. Run it with the digest bound: same rc and message.
 3. Run it with `--work` added and the digest bound: does it now start the battery (time it and
    stop after 20 s with SIGTERM; record what it printed)? This tells whether `--work` is the only
    missing piece or whether `--json-out`/`--rev` matter too.
 4. Run it with `--work` and the abbreviated digest: does the pin check refuse before execution?
Report the smallest set of additions that makes the printed command runnable, and whether the
gate's two named reasons are the complete set.

## Acceptance
A probe file with the four runs' argv, rc and message, and a one-line conclusion (complete /
incomplete with the missing item). Read-only. Receipt at
.ufo/waves/round-76/w1/LabratProbe/receipt.json.

## Evidence
Write .ufo/waves/round-76/w1/LabratProbe.md plus the receipt.
""")


def main() -> None:
    spec = {
        "wave": WAVE,
        "milestone": "r76-w1: the capability rows become a checked claim and a printed counting command becomes executable; independent re-derivation, forgery attack, mutation scoring, security review, source rows, sibling scan.",
        "reportDir": REPORT_DIR,
        "context": FROZEN,
        "items": ITEMS,
    }
    out = pathlib.Path(__file__).with_name(f"{WAVE}-spec.json")
    out.write_text(json.dumps(spec, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out} with {len(ITEMS)} items")


if __name__ == "__main__":
    main()
