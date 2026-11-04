#!/usr/bin/env python3
"""Generate the round-80 wave-1 spec (r80-w1): 15 seats, one v1 wave."""
import json
import pathlib

WAVE = "r80-w1"
REPORT_DIR = ".ufo/waves/round-80/w1"
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
that lane's `.ufo/waves/round-80/w1/<your-seat-name>/`; a write anywhere else is a defect (never
write the fleet root, a sibling lane, a lane production path, or /tmp). Seat tools start at the
fleet root, so a relative path is wrong.
**You never edit a lane production file.** The L1 lands every lane edit. You deliver candidate
files, receipts and prose under your own evidence dir; a seat that writes `tools/`, `corpus/`,
`SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md` or `plans/` directly has failed its seat even
if the content was right.
Scratch: create ONE dir `/fast/scratch/hyaku/kaidoku-r80/<your-seat-name>/` (mkdir -p), pass it
explicitly (TMPDIR=... and any --work), and delete it with `trap 'rm -rf -- "$S"' EXIT` (or a
finally:) before you yield, after copying your receipts into your evidence dir. A tool that
hardcodes /tmp instead is a defect you must report.
Never run `git`/`jj` writes, never commit, push, stash or check out anywhere; read-only git
(`log`, `show`, `diff`, `status`, `ls-files`, `rev-parse`, `merge-base`, `cat-file`) is fine.
Never touch /home/vgpnk/Projects/shokunin/.ufo/state/, .ufo/watchdog.log, MANIFEST.json,
templates/, scripts/, or another lane. Never message agent://all - only your own L1 by id.
Any git fixture repo you create is `D=$(mktemp -d)` under your scratch root and every later call
names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first
commit, and never commit anywhere else.
Security: never write a raw environment dump or a config file's secret values into the lane. A
probe that must show an environment writes the KEY NAMES and the canary presence only. For the
client configs, record only the package pin, the key names and the file digest - never an `env`
block or a token. A pointer binder retains a pointed line's digest, never its bytes.
Tooling authorization (operator 2026-10-19): you may install or upgrade tools that help the task;
read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate, record
tool/version/channel/reason in your report). PACMAN IS PAUSED host-wide: no pacman transaction of
any kind; use uv tool / npx / an official binary in ~/.local/bin. No system-wide upgrades.
Every `Report:` trailer path a validator renders is relative to
/home/vgpnk/Projects/shokunin/kaidoku-shokunin - write it at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/<that path>. Your final answer is a short JSON:
files_written, findings, evidence, risks.
"""

FROZEN = """## Frozen state (round 80)
base `16dfa009bf143080dfcdfc5f9ec34bd359536d90` (the round-79 tip after the round-79 non-author
spot-check; lane tree clean and pushed). Declaration: the guard for `plans/round-80-claims.md`
(`git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log -1 --format=%H -- plans/round-80-claims.md`),
which freezes the three predicates, kill rules and controls, and the strictness fixture set
`.ufo/waves/round-80/l1/fixtures/strictness.json`.
Claims (frozen sentences in plans/round-80-claims.md):
R80-C1 calibration - `tools/round-80/strictness-battery.py` scores a candidate pointer binder and
  the round-79 control binder on four red fixtures (substring pin against a longer live token x2;
  a record declaring the same client cell twice x2) and two green controls. Target: cases 4,
  green_cases 2, candidate_false_greens 0, control_false_greens 4, candidate_green_refusals 0,
  control_green_refusals 0; live arm `tools/round-80/pointer-bind.py --rev <measured>` exits 0
  with checks_total 5, matched 5, mismatches 0, unparsed 0, duplicates [].
R80-C2 freshness - `tools/round-80/receipt-provenance.py --from-round 60 --to-round 79` requires
  every `l1/scores/*.json` receipt (excluding `/attacks/`) to carry an `instrument.sha256` that
  equals a COMMITTED blob of its `instrument.path`. Base: receipts 34, flagged 2,
  expected_control_flags 1 (`prov-forged-instrument.json`), unexpected 1
  (`.ufo/waves/round-79/l1/scores/c2-at-landing.json`). Target: flagged 1, unexpected 0.
R80-C3 depth - `tools/round-80/guard-battery.py --rev <measured>` binds each of the nine
  `defects.append` clauses of `tools/round-78/attack-gate.py`'s `validate_receipt()` to exactly
  one row of the round-80 SKILL decision-table block and one declared selftest case, and proves
  the case fails when the clause is deleted. Base: guards 9, rows 0, bound 0, survivors 9.
  Target: rows 9, bound 9, survivors 0, pristine.cases 37, pristine.failures 0,
  target_pin.matched true.
Frozen table-block contract (both the gate seat and the battery seat implement it): the block is
delimited by `<!-- round-80 receipt-guard table: begin -->` and
`<!-- round-80 receipt-guard table: end -->` in SKILL.md, and each row is exactly
`| G<NN>-<slug> | <exact trigger, prose> | <message prefix in backticks> | <case name in backticks> |`.
The nine clause prefixes, in source order: `duplicate fixture id`; `fixture ids`; `: fixture dir
mismatch`; `: base.accepted is not a bool`; `: refused without a reason`; `: refused by `;
`base_accepted does not re-derive`; `refused does not re-derive`; `instrument sha256 is not`.
"""

ROLE_TEXT = {
    "scout": "Read-only reconnaissance. Name what the surface holds and what it misses; run the "
             "commands you cite.",
    "connector": "Cross-lane pattern finding, read-only across sibling lanes; absorb nothing.",
    "executor": "Write and run code under your own evidence dir; never edit a lane file.",
    "reviewer": "Independent re-derivation. Re-run the counter yourself and check the bytes.",
    "critic": "Adversarial falsification. Your job is to find the claim false or the counter blind.",
    "mutation-tester": "Mutate copies in scratch and show each mutant killed by a named case.",
    "sentinel": "Adversarial security and scope review of the instruments and the wave bounds.",
    "scribe": "Draft prose/registry rows under your own evidence dir; the L1 lands them.",
}

L1 = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
W = f"{L1}/.ufo/waves/round-80/w1"

ITEMS = [
    {
        "name": "ScoutRecord",
        "role": "scout",
        "task": f"""## Target
Read-only recon of `PROVINCE.md`'s pointer cells under a strict exact-token rule.
Write only under {W}/ScoutRecord/.

## Change
1. From the base blob (`git -C {L1} show 16dfa009:PROVINCE.md`) print the five pointer cells with
   their 1-based line numbers: the three `(Devin|OMP|Kimi) `rea-agents@<pin>` (`<path>:<line>`)`
   cells, the Ghidra `application.properties:<n>` pointer with its `application.version=` value,
   and the `.bashrc:<a>-<b>` range. Quote each cell's text (paths and pins only, never a secret).
2. For each cell, print the pointed live line (`sed -n '<n>p' <path>`) and the exact token the
   binder will require on it. State for each whether the token stands as a WHOLE token there
   (delimited on both sides by end-of-line or a character outside `[A-Za-z0-9._-]`).
3. Sanity the strict rule against over-refusal: list every other `rea-agents@` occurrence in
   `PROVINCE.md` (there are several: lines 9, 12, 47) and say whether a delimited-token rule would
   newly refuse any of the five cells because of them - the answer must be grounded, not asserted.
4. Report the live byte offsets/lengths (`wc -l`) of the two client configs and `.bashrc` so the
   line ranges can be cross-checked, and the sha256 of each pointed line's text.

## Acceptance
Receipt JSON with `cells` (id, record_line, cell_text, pointed_line, token, whole_token,
line_sha256), `over_refusal_check`, `file_lengths`. Report at {W}/ScoutRecord.md.""",
    },
    {
        "name": "ScoutGate",
        "role": "scout",
        "task": f"""## Target
Read-only recon of the nine `validate_receipt()` refusal clauses in
`tools/round-78/attack-gate.py` at base `16dfa009`, and an independent deletion tally.
Write only under {W}/ScoutGate/.

## Change
1. Enumerate every `defects.append(...)` statement inside `validate_receipt()` in source order:
   the 1-based line, the exact message literal (or f-string prefix), the enclosing `if` condition,
   and the trigger that fires it. There are nine at base; report the count.
2. For each clause, grep the gate's `--selftest` cases (`case("...", validate_receipt(...)...)`)
   and name every case that currently reaches it. Distinguish "reached incidentally" from
   "pinned": a case pins a clause only when deleting the clause changes that case's verdict.
3. Independently reproduce the base deletion tally in your scratch: for each clause replace the
   `defects.append(...)` statement with `pass` in a COPY under your scratch, run
   `python3 -I -B <copy> --selftest`, and report exit, `SELFTEST cases/failures` and which cases
   failed. Expected shape: 9 clauses, 8 with no failing case (survivors), 1 killed
   (`: refused without a reason`). Report any deviation.
4. Report the pristine `python3 -I -B {L1}/tools/round-78/attack-gate.py --selftest` tally
   (cases, failures, exit) and the gate's sha256.

## Acceptance
Receipt JSON with `clauses` (line, prefix, condition, reaching_cases, pinned), `deletion_tally`
(per clause: failures, killed, failing_cases), `pristine`, `gate_sha256`. Report at
{W}/ScoutGate.md.""",
    },
    {
        "name": "ExecBinder",
        "role": "executor",
        "task": f"""## Target
Deliver a candidate `tools/round-80/pointer-bind.py` (round-79's binder with a strict match rule
and a duplicate-cell rule) under {W}/ExecBinder/. Round-79's source is
{L1}/tools/round-79/pointer-bind.py - read it whole first; your candidate keeps its CLI
(`--root --rev --json-out --battery --selftest --validate --control path-only`), its five check
ids (`devin-pin`, `omp-pin`, `kimi-pin`, `ghidra-version`, `bashrc-exports`), its `DECLARED` map,
its receipt schema conventions and its exit contract (0 bound / 1 defect / 2 unevaluable).

## Change
1. **Exact-token matching.** A declared token binds only when every occurrence in the pointed
   lines is delimited on both sides: the character before and after the match is missing
   (start/end of the pointed slice) or is outside `[A-Za-z0-9._-]`. `rea-agents@6.7.0` must NOT
   bind a line containing `rea-agents@6.7.05` or `rea-agents@6.7.00`; it MUST bind
   `"rea-agents@6.7.0",`. Give the refusal a distinct `reason` naming the longer token found.
2. **Duplicate cells.** `parse_record()` must count every declared cell (a second OMP cell makes
   `checks_total` 6, not 5) and return the duplicate ids; the receipt carries
   `duplicates: [<check_id>...]`, and `ok` is false when `duplicates` is non-empty. Each duplicate
   cell is still bound independently (no last-wins collapse).
3. **Selftest.** Keep all 21 existing cases green and add at least 6: red substring cases for both
   a longer live token and a longer argv token, a red duplicate-cell case for OMP and one for
   Devin, a green exact-token line, and a green two-line range whose token is on the second line.
   Also add `--validate` guards for the new fields (matched-without-delimiter evidence,
   duplicates present under `ok true`), each with a case.
4. **Receipt.** Record `instrument.sha256`, `checked_at`, a 40-hex `rev`, `duplicates`, and for
   every matched cell the pointed slice's digest only - never the slice bytes.

## Acceptance
`python3 -I -B {W}/ExecBinder/pointer-bind.py --selftest` exits 0 with `cases >= 27, failures 0`;
`--validate` on a self-produced receipt returns `defects []`; `--root {L1} --rev 16dfa009
--json-out <receipt>` reports `checks_total 5`, `matched 5`, `mismatches 0`, `unparsed 0`,
`duplicates []` (the live record must not regress). Deliver the candidate, its selftest log and
the live receipt; do not touch the lane copy.""",
    },
    {
        "name": "ExecProv",
        "role": "executor",
        "task": f"""## Target
Deliver `tools/round-80/receipt-provenance.py` under {W}/ExecProv/ - a sweep that decides whether
every landing-class receipt's `instrument.sha256` names a COMMITTED blob of its
`instrument.path`.

## Change
1. **Population.** Walk `.ufo/waves/round-<N>/l1/scores/*.json` for N from `--from-round` (default
   60) through `--to-round` (default 79) under `--root`; skip any path containing `/attacks/`;
   keep only JSON objects carrying `instrument.path` and a 64-hex `instrument.sha256`. Read the
   population from `--rev` (`git show <rev>:<path>`) so the count is revision-pinned, and skip a
   receipt that does not exist at `--rev`.
2. **Provenance.** For each receipt, the digest is committed iff it equals `git show
   <tip>:<instrument.path>` or `git show <r>:<instrument.path>` for some committed revision `r` of
   that path (`git rev-list --all -- <path>`). A digest matching only the working tree is NOT
   committed. A symbolic `rev` (`@HEAD@`, `main`, `HEAD`) is never treated as a committed
   revision. Reject an `instrument.path` containing `..` or starting with `/` with a named defect
   (never run git with it).
3. **Classification.** `expected_controls` is the declared basename list
   `["prov-forged-instrument.json"]`: a flagged receipt whose basename is in it counts as
   `expected_control_flags`; every other flag counts as `unexpected`. The receipt reports
   `receipts`, `flagged`, `expected_control_flags`, `unexpected`, `rows` (path, instrument, digest,
   verdict, matched_rev), `instrument.sha256`, `checked_at`, `rev`.
4. **Modes.** `--selftest` (at least 8 cases: uncommitted digest flagged; tip digest accepted;
   history digest accepted; working-tree-only digest flagged; `/attacks/` excluded; symbolic rev
   refused; path escape refused; a JSON without the instrument block skipped); `--validate`
   re-derives every count from `rows` and rejects `unexpected` that is not the difference;
   exit 0 when `unexpected == 0`, 1 when it is not, 2 when the population cannot be read.
5. **Base arms.** Run it at `--rev 16dfa009` and deliver that receipt. The expected base reading is
   `receipts 34`, `flagged 2`, `expected_control_flags 1`, `unexpected 1`; if your population rule
   yields a different count, report the exact difference and the receipts that cause it - do not
   tune the rule to hit 34.

## Acceptance
Selftest exits 0 with `cases >= 8, failures 0`; the base receipt is delivered with its rows; the
`--validate` on it is defect-free (a base receipt may be `ok false`, its internal consistency is
what `--validate` checks). Record the git commands you ran and their cost.""",
    },
    {
        "name": "ExecGuard",
        "role": "executor",
        "task": f"""## Target
Deliver `tools/round-80/guard-battery.py` under {W}/ExecGuard/ - the counter for R80-C3: it binds
each `validate_receipt()` clause of `tools/round-78/attack-gate.py` at a measured revision to one
row of the round-80 SKILL table block and one declared selftest case, then proves the case fails
when the clause is deleted.

## Change
1. **Clause enumeration.** From `git show <rev>:tools/round-78/attack-gate.py`, take the source of
   `validate_receipt()` and enumerate every `defects.append(...)` statement: emit `clause_id`
   (`G01`..`G09` in source order), 1-based line, the message literal, and a stable `message`
   prefix (the literal text before any interpolation). Report `guards`.
2. **Table parse.** From `git show <rev>:SKILL.md`, take the block between
   `<!-- round-80 receipt-guard table: begin -->` and `<!-- round-80 receipt-guard table: end -->`,
   split rows on unescaped `|`, and require exactly four cells: `G<NN>-<slug>`, trigger, a
   backticked message prefix, a backticked case name. Report `rows`. A malformed row, a duplicate
   clause id, an orphan row (no clause) and a clause with two rows are each named defects.
3. **Binding.** A clause is bound when its row's prefix is a prefix of the clause's message
   literal AND the case name appears as `case("<name>"` in the gate's selftest source. `bound` is
   the count of clauses bound. No clause may be bound to two rows.
4. **Mutation.** For each clause in source order: copy the gate blob to scratch, replace that
   `defects.append(...)` statement with `pass` (assert exactly one occurrence), compile it, run
   `python3 -I -B <copy> --selftest` under a four-key child environment
   (`HOME`, `LANG`, `PATH`, `TMPDIR`), and read the case JSON lines plus the
   `SELFTEST cases=<n> failures=<m>` summary. `killed` requires the declared case to be PRESENT in
   that output and to FAIL; a copy that does not compile or prints no summary is `inconclusive`,
   never a kill. `survivors` lists every clause not killed. Run the pristine gate the same way for
   `pristine.cases`/`pristine.failures` and re-derive `pristine.cases` from the copy's own
   summary - never from a hardcoded number.
5. **Receipt and modes.** `target_pin` = sha256 of the gate blob at `--rev` plus the expected
   landing digest passed as `--expect-sha256` (optional; `matched` false when it is absent or
   differs); receipt carries `guards`, `rows`, `bound`, `survivors`, `killed`, `pristine`,
   `target_pin`, `instrument.sha256`, `rev`, `checked_at`. `--selftest` at least 10 cases (unbound
   clause, orphan row, malformed row, duplicate id, absent declared case, case passing on the
   mutant, non-compiling mutant, empty clause set refused, summary-less copy inconclusive, a
   prefix that matches two clauses refused). `--validate` re-derives every count. Exit 0 when
   `guards>0`, `rows==guards`, `bound==guards`, `survivors==[]`, `pristine.failures==0`; 1
   otherwise; 2 unevaluable.
6. **Base arm.** Run at `--rev 16dfa009` and deliver the receipt. Expected shape: `guards 9`,
   `rows 0`, `bound 0`, `survivors 9`. If your reading differs, report the difference and the
   clause it comes from.

## Acceptance
Selftest exits 0 with `cases >= 10, failures 0`; `--validate` on your base receipt is
defect-free; the base receipt shows `guards 9`, `rows 0`, `survivors 9`; scratch dirs cleaned.""",
    },
    {
        "name": "ExecGate",
        "role": "executor",
        "task": f"""## Target
Deliver (a) a candidate revision of `tools/round-78/attack-gate.py` under {W}/ExecGate/ that adds
exactly EIGHT isolating selftest cases - one per clause that lacks one - and (b) a draft of the
round-80 decision-table block for SKILL.md. Read the gate whole first
({L1}/tools/round-78/attack-gate.py); it has 29 selftest cases at base and
`red-validate-refused-no-reason` already pins the `: refused without a reason` clause.

## Change
1. For each of the eight unbound clauses (all but `: refused without a reason`, in source order),
   write ONE `case("<name>", validate_receipt(<forged receipt>)["defects"], <expected>)` whose
   forged receipt trips that clause and whose assertion FAILS when the clause's `defects.append`
   is replaced by `pass`. Prefer asserting the exact defect list so a sibling clause's message
   cannot keep the case green. Case names (exact):
   `red-validate-duplicate-fixture-id`, `red-validate-fixture-id-set`,
   `red-validate-fixture-dir`, `red-validate-base-accepted-bool`,
   `red-validate-refused-other-rule`, `red-validate-base-accepted-count`,
   `red-validate-refused-count`, `red-validate-instrument-digest`.
   Build each forged receipt from the module's own `ATTACKS` table so it stays valid for a
   different attack set; do not hardcode a 10-item list.
2. Prove each case isolating in your scratch: nine mutants (one per clause, `defects.append` ->
   `pass`, exactly one occurrence each), each run's `--selftest` output, and the failing-case list.
   A case that stays green on its mutant is not acceptable - redesign it.
3. Draft the SKILL block in `guard-table-draft.md` with the exact contract from the frozen state:
   `<!-- round-80 receipt-guard table: begin -->`, nine rows
   `| G<NN>-<slug> | <trigger> | `<message prefix>` | `<case name>` |`, end marker. The prefix must
   be a literal prefix of the clause's message; the case name must be the one in your candidate.
4. Report the pristine tally of your candidate (`SELFTEST cases=37 failures=0`) and its sha256.

## Acceptance
Candidate gate exits 0 on `--selftest` with `cases 37, failures 0`; your nine mutant runs show
each declared case failing on its own mutant (paste the per-mutant table); the draft block parses
as nine four-cell rows. Deliver candidate, mutant table, draft block; never touch the lane copy.""",
    },
    {
        "name": "ScribeSources",
        "role": "scribe",
        "task": f"""## Target
Open and snapshot the two sources that ground R80-C1's rules, and one considered-but-rejected
candidate; draft registry rows for the lane. Draft only, the L1 appends under {L1}/corpus/SOURCES.md.

## Change
1. Open (fetch to your evidence dir, keep bytes) and locate a <=25-word quote in each:
   - RFC 8259 section 4 (the JSON object grammar) on duplicate names - the sentence stating names
     within an object SHOULD be unique; it grounds the duplicate-cell refusal. URL
     `https://www.rfc-editor.org/rfc/rfc8259.txt` (or the .html form; record which).
   - The Python `re` documentation on `\\b` (word boundary) - the sentence defining a word
     boundary; it grounds the exact-token (delimited) match. URL
     `https://docs.python.org/3/library/re.html`.
   Do not open a source you cannot snapshot; record HTTP status, bytes, sha256 and the located
   line number for each.
2. Duplicate check before drafting: `grep -n` `corpus/SOURCES.md` for both URLs and hosts
   (`rfc-editor.org`, `docs.python.org`). A URL already held is a refused reuse, not a row; a
   different anchor on a held host may be a row - say which and why.
3. Record ONE rejection with reason and flip condition (round-79 spot-check item 5): a
   non-authoritative treatment of duplicate JSON keys (a blog or Q&A page) that you actually
   opened; reason it is not a row here, and the exact condition that would flip it.
4. Draft two 11-column rows (`id | source | kind | tier | scope | anchor | teaches | status |
   opened | recheck | used-by`) with ids continuing the registry - read the highest id first
   (`grep -oE 'S[0-9]{3,}' corpus/SOURCES.md | sort -u | tail -3`). No cell may contain a literal
   or escaped `|`; rewrite a quoted fragment so the row parses as 11 cells. Draft only.

## Acceptance
Receipt JSON with `snapshots` (url, status, bytes, sha256, path), `quotes` (text, words, line),
`duplicate_check`, `rejection` (url, reason, flip), `next_ids`, `rows_draft`, `gate_block_draft`.
Report at {W}/ScribeSources.md.""",
    },
    {
        "name": "ScribeKnowledge",
        "role": "scribe",
        "task": f"""## Target
Draft the round-80 knowledge entry `corpus/knowledge/2026-11-04-r80-<slug>.md` (the L1 lands it)
and its coverage-map row. Read two recent entries for shape:
{L1}/corpus/knowledge/2026-11-04-r79-mutation-and-pointers.md and
{L1}/corpus/knowledge/2026-11-03-r68-packed-elf-route.md.

## Change
1. Content, in the lane's decision-table style: (a) the exact-token binding rule with its
   delimiter class, the two refusal signatures (`rea-agents@6.7.05` vs `@6.7.0`; `@6.7.00`) and
   the green controls; (b) the duplicate-cell rule and what a collapsing parser loses (the second
   cell, silently); (c) the receipt-provenance rule (digest must name a committed blob; working
   tree and symbolic revs are not committed); (d) the guard-table binding rule (one clause, one
   row, one isolating case; absent case = survivor). Cite the new `S###` rows from the sources
   seat and the receipts by path.
2. Every quantitative sentence must name the command that produces it and a receipt path under
   `.ufo/waves/round-80/`. Where the round has not measured a value yet, write the field as
   `pending the landing receipt` - never invent a count.
3. Draft the coverage-map row (read `corpus/README.md`'s `## Coverage map` and match the format),
   the `SOURCES.md` `used-by` values for the two rows, and the two `trust`/`scope` cells.
4. Name the coverage consequence honestly: this entry is on the lane's own instrument layer, not
   a new carrier class; say what the map should therefore record.

## Acceptance
Draft entry (full markdown), coverage-map row, `used_by` list. Receipt JSON with `title`,
`cites`, `commands`. Report at {W}/ScribeKnowledge.md.""",
    },
    {
        "name": "ScribeLesson",
        "role": "scribe",
        "task": f"""## Target
Draft `corpus/lessons/round-80.md` (the L1 lands it): `## Mistakes`, `## Gate`, `## Sources`.
Read {L1}/corpus/lessons/round-79.md and {L1}/corpus/lessons/round-79-verifier-spotcheck.md first.

## Change
1. **Mistakes**: at least three rows in the fleet shape (class, evidence pointer path:line,
   captured-by, fix), each fix shown able to fail. Candidates to weigh (ground each in bytes you
   read): the round-79 landing receipt naming an instrument digest that matches no committed blob
   (class: unrecoverable provenance; captured-by: none until R80-C2; fix: the sweep, which must
   flag the base population); a parser that collapses duplicate cells last-wins (class: silent
   information loss; captured-by: a count-based rule only counts unique ids); a selftest case that
   reaches a guard without pinning it (class: exercised-but-unpinned; captured-by: the deletion
   test); a substring token match (class: prefix acceptance; captured-by: none until R80-C1).
2. **Gate**: for every source row this round admits, the URL, access date and a <=25-word located
   quote; and at least ONE rejection with reason and flip condition. If the sources seat has not
   delivered yet, use your own opened source and say which.
3. **Sources**: the round's opening list as the lane records it, with the digest of the snapshot.
4. State each mistake's capture mechanism as a criterion the lane can now run (a command), not a
   sentiment.

## Acceptance
Draft lesson in full markdown with three tables; each mistake row has all four cells filled; the
Gate has >=1 admit and >=1 reject. Receipt JSON with `mistakes`, `gate_admits`, `gate_rejects`,
`commands`. Report at {W}/ScribeLesson.md.""",
    },
    {
        "name": "ReviewerC1",
        "role": "reviewer",
        "task": f"""## Target
Independent re-derivation of R80-C1. Do not import the executor's driver; write your own.
Evidence under {W}/ReviewerC1/.

## Change
1. From {L1}/.ufo/waves/round-80/l1/fixtures/strictness.json (frozen before data), implement your
   own scorer for the four red cases and two green controls: for `bind` cases call the loaded
   module's `bind(pointer, tokens, lines)`; for `record` cases create a fixture git repo in your
   scratch (`git init`, write `PROVINCE.md` = `record_template` + `append_cell`, commit it) and
   call the module's `battery(<repo>, "HEAD", None)`. Load a module by path with
   `importlib.util.spec_from_file_location`.
2. Score `tools/round-79/pointer-bind.py` (control) and the ExecBinder candidate if it exists at
   `{W}/ExecBinder/pointer-bind.py`; if it is not there yet, score the control only and use this
   seat to make the fixture set airtight: prove each red case really is accepted by the control
   for the reason stated in `why`, and each green control really is bound by it.
3. Attack the fixture set: can a degenerate implementation that refuses everything pass? (It must
   fail the two green controls.) Can a degenerate implementation that binds everything pass? (It
   must fail all four reds.) Is any red case red only because of an unrelated bug (e.g. the module
   raising instead of returning)? Report each.
4. Record, per case, the control's verdict with its `reason` string and a one-line judgement
   (`false-green` or `refused`).

## Acceptance
Receipt JSON with `cases` (id, kind, control_matched, control_reason, judgement),
`degenerate_checks` (bind-all, refuse-all, per-case), `flat_findings`. Report at
{W}/ReviewerC1.md.""",
    },
    {
        "name": "ReviewerC3",
        "role": "reviewer",
        "task": f"""## Target
Independent re-derivation of R80-C3: the nine-clause binding and its mutation proof.
Evidence under {W}/ReviewerC3/.

## Change
1. Write your own enumeration of `validate_receipt()`'s `defects.append` clauses at `16dfa009`
   (do not reuse the ExecGuard parser): source line, message literal, enclosing condition.
2. Write your own deletion driver: nine copies of the gate blob in your scratch, `defects.append`
   -> `pass`, `python3 -I -B <copy> --selftest` under a four-key child env, and the failing-case
   list from the case JSON lines. Confirm the base shape (8 survivors, 1 killed at
   `: refused without a reason`) or report the deviation.
3. If `{W}/ExecGate/` has a candidate gate and/or a draft table block, score them: does each of
   the nine declared cases exist, pass pristine, and fail on its own mutant? Does the draft block
   parse as nine four-cell rows with prefixes that match the clauses? Report every case that is
   not isolating and every row that does not bind.
4. Attack the binding rule: a table row whose prefix matches two clauses; a case that asserts a
   source literal rather than behaviour; a case that fails on everything (so it "kills" every
   mutant); a clause merged into one `defects.append` by a refactor. Say which of these the
   frozen predicate catches and which it misses.

## Acceptance
Receipt JSON with `clauses`, `deletion_tally`, `candidate_scoring` (per case: exists, pristine,
killed_by_its_mutant, isolating), `binding_attacks`. Report at {W}/ReviewerC3.md.""",
    },
    {
        "name": "CriticClaims",
        "role": "critic",
        "task": f"""## Target
Falsify the three round-80 predicates. Read {L1}/plans/round-80-claims.md first and attack the
sentences, not the work. Evidence under {W}/CriticClaims/.

## Change
1. **Do-nothing control reachability**, per claim: build the cheapest input that meets the
   predicate without the claimed work. C1: can a binder that refuses every token pass the
   predicate? (Check the green controls and the live 5/5 arm.) C2: can a sweep that flags nothing
   pass? (The control flag must be present.) C3: can a battery with zero guards or zero rows
   report `survivors 0`? Find every vacuous path and say whether the frozen predicate blocks it.
2. **Empty-set and population gaming**: a population with receipts removed instead of repaired;
   a `--from-round/--to-round` window narrowed to exclude the failing receipt; a table row whose
   case name is declared but not written; a case that asserts a constant.
3. **Axis labelling** (§9 of the round contract): is each claim named by the surface it changes,
   not the number it produces? Is `freshness` entering as an owned axis legitimate, and does the
   entry carry a measured baseline rather than an invented score? Is C3 depth or is it quality
   work on an existing instrument? Give a ruling and the sentence it rests on.
4. **Causal separability**: does any counter read another claim's file or receipt? List the file
   sets of the three claims and their intersection.
5. **Kill-rule completeness**: name a defect class the frozen kill rules miss, with the input that
   would exercise it.

## Acceptance
Receipt JSON with `reachability` (claim, vacuous_path, blocked_by), `gaming` (class, caught),
`axis_rulings`, `file_overlap`, `kill_rule_gaps`. Report at {W}/CriticClaims.md.""",
    },
    {
        "name": "MutInstruments",
        "role": "mutation-tester",
        "task": f"""## Target
Mutation-test the round-80 instruments' own selftests: for each of the three candidates the wave
delivers (`{W}/ExecBinder/pointer-bind.py`, `{W}/ExecProv/receipt-provenance.py`,
`{W}/ExecGuard/guard-battery.py`), does any conjunct survive a one-edit mutation with every
selftest case green? If a candidate is absent when you start, work on the ones present and say so;
score `{L1}/tools/round-79/pointer-bind.py` as a fourth target so the seat has work regardless.

## Change
1. For each target: copy the file to your scratch, record its sha256, run `--selftest` pristine
   and record `SELFTEST cases/failures`.
2. Cut at least four single-edit mutants per target (12+ total), each a one-hunk edit that keeps
   the file compiling: invert a comparison, drop a guard's `defects.append`, make a strict match
   bound unchecked, make a count read from a constant, make `--validate` ignore a field, make the
   provenance check accept the working tree. Assert each anchor occurs exactly once.
3. Run each mutant's `--selftest` under a four-key child env; `killed` = summary present and >=1
   failing case; a copy that does not compile or prints no summary is `inconclusive`. Record
   `killed_by` (the failing case names) and `sole_detector`.
4. For every survivor, prove the missing assertion: write a case in scratch and show it returns
   True on the pristine module and False on the mutant.

## Acceptance
Receipt JSON with `targets` (path, sha256, pristine), `mutants` (id, edit, exit, failures,
killed_by, survived), `survivors` (with the case that would kill each), `inconclusive`. Report at
{W}/MutInstruments.md.""",
    },
    {
        "name": "SentinelScope",
        "role": "sentinel",
        "task": f"""## Target
Adversarial security and scope review of the round-80 instruments and of this wave's bounds.
Evidence under {W}/SentinelScope/.

## Change
1. **Live-file reads.** The binder reads the three client configs, `.bashrc` and a Ghidra
   properties file. Verify from the candidate source that it retains only a digest of the pointed
   lines and never writes their bytes; check every receipt the wave produced for a raw token,
   `env` block or secret value (grep for `token`, `api_key`, `sk-`, `Bearer`, `password`). Report
   any leak with the file and line.
2. **Path handling.** Does the provenance sweep reject `..`/absolute `instrument.path` values
   before running git? Does the guard battery ever execute a lane file it did not copy to scratch?
   Does any instrument write outside `--json-out` and `--work`?
3. **Child environment.** The gate mutation and the provenance sweep spawn children: confirm each
   subprocess runs with an allowlist (`HOME`, `LANG`, `PATH`, `TMPDIR`) and `TMPDIR` under the
   seat's scratch, and that a run records the env it observed if it claims one.
4. **Wave bounds.** Check this wave's seats for writes outside `.ufo/waves/round-80/w1/` and for
   any `git`/`jj` write: `git -C {L1} status --porcelain` must show no lane-tree change by a
   seat; list any file a seat wrote outside its evidence dir.
5. **Forgery.** Can a hand-authored receipt pass `--validate`? State exactly which checks are
   internal consistency and which bind to an artefact; do not call consistency authenticity.

## Acceptance
Receipt JSON with `leaks`, `path_checks`, `child_env`, `wave_bounds`, `forgery_limit`. Report at
{W}/SentinelScope.md.""",
    },
    {
        "name": "ConnectorSibling",
        "role": "connector",
        "task": f"""## Target
Cross-lane, read-only: does any sibling lane already implement a receipt-provenance sweep, an
exact-token/word-boundary matcher or a clause-to-case binding, and what does this lane's version
add or miss? Evidence under {W}/ConnectorSibling/.

## Change
1. Search read-only across `/home/vgpnk/Projects/shokunin/*/tools/` and `/home/vgpnk/Projects/shokunin/*/scripts/`
   for `provenance`, `instrument.sha256`, `word boundary`, `duplicate key`, `sole_detector`,
   `guard`, `clause` (grep -l, then read the hits). List every sibling implementation with its
   path, its rule and its scope; absorb nothing, edit nothing.
2. Compare each against the three round-80 rules and name what this lane's version adds (e.g. the
   committed-blob requirement, the duplicate-cell count) and what it lacks that a sibling has.
3. `considerthese/`: state whether {L1}/considerthese/ exists. If it does, read the newest file and
   name at most one still-unimplemented proposal that fits this round's axes; if it does not,
   write the single line the report must carry.
4. Name any sibling lane whose round-80 work touches this lane's evidence surfaces (a shared
   instrument path, a shared receipt), so the L1 can route it.

## Acceptance
Receipt JSON with `sibling_impls` (path, rule, scope), `delta`, `considerthese`, `overlap`.
Report at {W}/ConnectorSibling.md.""",
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
        "milestone": ("r80-w1: strict pointer binding, receipt provenance and guard-table "
                      "binding frozen with base arms, attacked from four directions."),
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
