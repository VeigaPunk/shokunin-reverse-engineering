#!/usr/bin/env python3
"""Generate the kaidoku round-53 wave-1 (build+attack, v1 policy band 16-32) spec. R53, KaidokuR53.

Interpolation discipline (M51-6 / CritBand F1/F2): this generator substitutes LANE/W1/BASE at
build time; the emitted item strings must contain no `{...}` placeholders. The dispatch is
independently re-checked for `{X}`, `{x}`, `<ANGLE>` and `{...}` forms before the ready file
is written (SentScope re-audits the rendered dispatch; r52 CritBand found the round-52 checker
blind to lowercase/single-char/angle forms).
"""
import json, pathlib

GS = open('/home/vgpnk/.agents/skills/godspeed/directive.md').read().strip()
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
W1 = LANE + '/.ufo/waves/round-53/w1'
BASE = '4cb12b41368c83ac6e04a0ae44788622dd26c79e'          # claims-draft commit (this wave's target)
LANEBASE = '6697518f0ad8e8399567ae4c9cd0207fc7c04d8b'      # round-start tip
ENVD = LANE + '/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes'

CONTEXT = f"""# Target
kaidoku-shokunin round 53, attempt 1, wave r53-w1 = the single v1 BUILD+ATTACK wave (32 seats,
policy band 32-48; the operator amended the run-13 band mid-run from 16-32 to 32-48 and this
round dispatches after the amendment, so the live policy governs). Two declared claims, both offline over committed bytes - no REA run, no
vendor fetch, no network beyond the URLs your own task names:
- **R53-C1 depth**: triage table v6 as SKILL.md rule block 27 + instrument
  {LANE}/tools/round-53/sqfs-triage-v6.py + frozen fixture-level reader census
  {LANE}/tools/round-53/reader-census.json + before-arm witness
  {LANE}/tools/round-53/v5-baseline-witness.py. Predicate (claims file is authoritative):
  v6 at the landing exits 0 with pair_mismatches 0, evaluator_missing 0,
  executability_violations 0, clean_residue 0; the witness at base {LANEBASE} exits 1 with
  executability_violations 1 naming dmg_Z3_v3ddwrt_inode_table and clean_residue 7.
- **R53-C2 calibration**: record oracle {LANE}/tools/round-53/r53-record.py, ten atoms T1-T10
  over the round's own record; at the freeze mismatches 8 (landing atoms red), at the landing
  mismatches 0.
Round base {LANEBASE}; claims draft (the round's rule - read it, not this prompt):
{LANE}/plans/round-53-claims.md at commit {BASE}. Wave findings that C1 must resolve, with
their full findings.md files: {LANE}/.ufo/waves/round-52/w1/CritTriV6/, MutTriV6/,
CritClaims/, CritBand/. Build on: triage v5 {LANE}/tools/round-50-c3/sqfs-triage-v5.py;
SKILL.md block 26 (marker `<!-- sqfs-triage-table v5 -->`); envelope corpus {ENVD} (126
envelopes, each an envelope.json REA evidence record - the fixture bytes live in scratch and
are gone, so everything scores from committed envelope/census bytes); reader-census lineage
{LANE}/corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md and
{LANE}/corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md (NOT promoted; S250/S251);
record-oracle port base {LANE}/tools/round-50/c2-record.py.

# Contract (binding on every seat)
- **Read-only on the lane tree.** Write ONLY inside {W1}/<YourSeatName>/ (create it) and your
  report file {W1}/<YourSeatName>.md. Drafts (instruments, census, rows, docs) go under
  {W1}/<YourSeatName>/ - never into the lane's tools/, plans/, corpus/, SKILL.md,
  PROVINCE.md, LOG.md, SCORECARD.md, SHONEN.md, nor the fleet repo. The L1 integrates drafts
  after the wave and may rewrite them. Never commit, push, stage, stash, or run any mutating
  git/jj command in the lane or fleet repo. Read-only git (log, show, diff, ls-tree,
  rev-parse, cat-file, merge-base) is fine.
- **status.json (routed defect 2):** before you yield, write
  {W1}/<YourSeatName>/status.json as an object {{"seat":"<YourSeatName>","role":"<role>",
  "status":"settled"|"failed"|"blocked","summary":"<=40 words","artifacts":["<relative paths
  under your seat dir>"]}} - the L1's wave accounting parses these files, not prose.
- **No REA runs this wave.** The L1 alone runs the counting commands after the wave (freeze,
controls, before-arms, landing, after-arms). Do not invoke `npx rea-agents`, `rea`, or the
package at /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents - READING its
source files is allowed where your task names it. Offline selftests and synthetic-fixture
probes (mksquashfs/unsquashfs/7z/sasquatch in your scratch) are allowed where your task
names them.
- **Downloads**: only where your task names a URL (at most the URLs your task names), into
your scratch only; never paste session cookies, tokens or Set-Cookie headers into any
receipt: strip headers before saving.
- **Fixture repos**: `D=$(mktemp -d -p "$S") && git -C "$D" init -q`; every later git call
names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first
commit; set `user.name`/`user.email` in that clone only. Never run `git commit` with a
throwaway identity anywhere else. Prefer `git clone --shared {LANE} "$S/clone"` +
`git -C "$S/clone" checkout --detach {BASE}` for a lane copy.
- **Scratch**: `S=/fast/scratch/hyaku/kaidoku-r53/w1-<YourSeatName>`; `mkdir -p "$S"`,
`export TMPDIR="$S"`. Remove `$S` before you yield AFTER copying receipts into
{W1}/<YourSeatName>/. Never write under /tmp; nothing under /tmp is citable. Check
/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status before a heavy pass.
- **Honest capture beats a pass.** Every receipt carries the exact command, exit code, stdout
sha256 and UTC time. A check you did not run is not passed - say "not run". Never fabricate
output. Exit codes are semantic: 0 met/clean, 1 not met/violation, 2 could-not-evaluate.
- **Absolute paths**: your tools start at the fleet root, not the lane. The `Report:` trailer
path in your prompt is relative to {LANE} - write it at {LANE}/<that path>
({W1}/<YourSeatName>.md). A file written at a relative path lands in the FLEET repo and is
a defect.
- **Tooling authorization (operator, 2026-10-19)**: you may install/upgrade tools that help
the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate;
record tool/version/channel/reason in your report). **pacman guard**: all pacman
transactions are PAUSED host-wide - install only via `uv tool`/`npx`/an official binary in
~/.local/bin, or nothing. Never `-Sy`, `-Syu`, `-U`, `-R`, downgrade, or restart a host
service.
- Never message `agent://all`; never touch a sibling lane, .ufo/state/, .ufo/watchdog.log,
/home/vgpnk/Projects/shokunin/.scratch/, or the fleet repo. Never write into
corpus/evidence/. An executor seat may spawn ONE read-only labrat probe for a falsifiable
hypothesis; no other seat spawns anything.
- Return a final message of at most 8 lines: your verdict, the 1-3 most important findings,
your report path.

# What the L1 does with your output
It reads every report + status.json, integrates the drafts (instruments, census, rows, entry,
lesson, registry rows), amends the claims file from attack findings, commits ONE freeze
(instruments + census + fixtures + amended claims), scores the pre-freeze controls, runs the
before-arms, lands SKILL block 27 + record sections, re-runs the counters at the landing,
commits, pushes, files the report. Drafts you write are inputs the L1 reviews and may
rewrite. Report; do not wait for others."""

def item(name, role, task):
    return {"name": name, "role": role, "prompt": f"/skill:godspeed\n\n{GS}\n\n{task}"}

items = [
# ---------------- executors (7) ----------------
item("ExecV6Port", "executor",
f"""Port the triage instrument to v6 as a complete draft {W1}/ExecV6Port/sqfs-triage-v6.py.
Read {LANE}/tools/round-50-c3/sqfs-triage-v5.py (port it; do not rewrite its scored
semantics), {LANE}/plans/round-53-claims.md (R53-C1, the v6 changes bullet is your spec),
{LANE}/.ufo/waves/round-52/w1/CritTriV6/findings.md and
{LANE}/.ufo/waves/round-52/w1/MutTriV6/battery.md. Changes exactly: (1) read the frozen
census {LANE}/tools/round-53/reader-census.json (a new --census arg, pinned in the claims
instruments map) as a binding input of routing AND the evaluator; (2) new row
legacy-body-refused -> preserve-unresolved (FAILED body, extractor-failure+, 0 published,
fixture census NO-READER) placed before legacy-body-failure; (3) legacy-body-failure narrowed
to reader-backed fixtures via the census condition; (4) the seven no-reader ddwrt clean
envelopes route clean-unverified/record-unverified (census condition on the clean row);
(5) first-match precedence: census-conditioned rows decide before family rows - state it in
the docstring; (6) the executability audit: for every FAILED-body envelope whose prescribed
action prescribes a cross-read, count a violation when the census marks those bytes NO-READER;
clean_residue counts clean-labelled envelopes whose census rows are NO-READER; (7) receipt
fields pair_mismatches, evaluator_missing, executability_violations, clean_residue; (8) port
the whole battery harness (--selftest, --emit-mutant, --controls), freeze-drift gating (exit 2
frozen_path_changed) and exit-code map from v5; (9) the claims-file predicate sentence in the
docstring verbatim; (10) the score-time reader census input is read from --census, never from
the worktree. Python 3 -I -B compatible; runnable with --selftest offline over fixture trees
in scratch. If the port exceeds your budget, deliver the complete hunk-level diff-spec -
never a broken file."""),
item("ExecWitness", "executor",
f"""Draft the before-arm witness {W1}/ExecWitness/v5-baseline-witness.py. Context: CritClaims F2
measured that the v5 instrument refuses a base-descending freeze (exit 2 at
tools/round-50-c3/sqfs-triage-v5.py:1261-1263) and MutTriV6 F1 measured that
tools/round-50-c3/ holds no table file (the v5 bytes live in SKILL.md at the marker
`<!-- sqfs-triage-table v5 -->`). So the witness is its own script: args --root --rev --freeze
--envelopes --census --json-out; it reads the v5 table block from `git show <rev>:SKILL.md`
(requiring rev == the declared base or a descendant, refusing rev newer than the freeze),
re-implements the v5 routing decision path self-contained (port the row application +
first-match order from the v5 source; cite the lines you ported), and scores the SAME
executability audit + clean_residue over the frozen census ({LANE}/tools/round-53/reader-census.json,
read from --census). Expected before receipt at the base: exit 1, executability_violations 1
naming dmg_Z3_v3ddwrt_inode_table, clean_residue 7 naming the seven envelopes. Include a
--selftest over fixture trees in scratch: one case proving the witness reads the BASE bytes
(mutate a synthetic base file's label -> witness verdict changes), one case proving the
ancestry refusal. Read {LANE}/.ufo/waves/round-52/w1/RevV5Gate/ for the r53 wave's gate
semantics findings if present. Python 3 -I -B compatible."""),
item("ExecCensus", "executor",
f"""Draft the frozen fixture-level reader census {W1}/ExecCensus/reader-census.json and its
lineage/recapture helper {W1}/ExecCensus/recapture-readers.sh. Source ground: the committed
reader evidence - {LANE}/corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md (the round-49
reader census incl. v3-readers.out pointers), the round-50 census tables under
{LANE}/tools/round-50/oracle/ and .ufo/waves/round-49,waves/round-50 wave evidence,
{LANE}/corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md (S250/S251 ground; NOT
promoted), and the envelope corpus {ENVD} (126 envelope.json records carrying handler names,
gap kinds, published counts). One row per ddwrt fixture (15 envelopes) plus every other
fixture your sources cover; fields: fixture id, family, reader outcomes where committed
evidence carries them (reader name, command, exit, UTC, evidence pointer) or
"lineage": [pointers] with "recaptured": false, and the expected triage-relevant kind
(reader-backed / no-reader). Explicitly mark the 7 ddwrt no-reader clean envelopes and the 1
ddwrt FAILED no-reader body. Fresh recapture ONLY where a committed mksquashfs recipe exists
(search .ufo/waves/round-42 and corpus for the fixture recipes; mksquashfs + unsquashfs + 7z
runs go in your scratch with receipts): a recapture that CONTRADICTS the lineage is a stop -
write contradiction.json and mark the census unusable (the claims kill rule fires). Rows
without committed per-row command/exit are declared-not-recaptured, never silently recaptured.
No new reader is claimed validated. Receipts for every command you run."""),
item("ExecRecord", "executor",
f"""Draft the round-53 record oracle {W1}/ExecRecord/r53-record.py. Port base:
{LANE}/tools/round-50/c2-record.py (port its structure: atom table, committed-bytes discipline,
--battery/--selftest). Spec: {LANE}/plans/round-53-claims.md R53-C2 (the ten atoms T1-T10 are
normative; the counter parses each atom's declared value from the committed SCORECARD round-53
section text and checks it against observed state at --rev - record-vs-reality). Args: --root
--rev --freeze --base --battery --selftest --json-out. Expected: at the freeze, exit 1 with
exactly mismatches 8 (T3-T10 red: landing atoms; T1/T2 green); at a landing REV, exit 0 with
mismatches 0. Every read resolves committed bytes via git show (never the worktree); helpers
loaded only from --rev bytes (the r48 C2OracleLimit lesson); scratch-respecting (TMPDIR/--work,
no hardcoded /tmp - the r53 routed defect). --selftest: git-fixture cases in scratch covering
at least: green landing fixture, red landing fixture (one wrong declared number), forged
receipt (rev mismatch), falsified wave line (seat-count wrong), frozen-path-drift case, plus
one case per atom. Also deliver battery.md listing >=10 record mutations, each naming the
atom it flips; no-op mutants are refused, not counted."""),
item("ExecControls", "executor",
f"""Draft the pre-freeze control suite {W1}/ExecControls/ (driver + fixtures + expected
receipts shape) for BOTH claims. Read {LANE}/plans/round-53-claims.md controls bullets (both
claims). For R53-C1: do-nothing (the witness at base over the real corpus -> red), junk table
(syntactically valid, wrong labels -> pair_mismatches>0 exit 1), audit-guard-deleted mutant
-> red, family-key mutant (v6 rows keyed on the bare family, ignoring the census) -> RED on
your synthetic reader-backed ddwrt FAILED-body witness (build it: mksquashfs recipe in your
scratch producing a ddwrt-style v3 body the census marks reader-backed; the mutant must route
it cross-read-legacy while the real v6 routes preserve-unresolved), swapped-action mutant
(preserve-unresolved <-> cross-read-legacy) -> red, clean-unverified-suppressed mutant ->
red. For R53-C2: the do-nothing run IS the freeze before-receipt (mismatches 8); junk record
(forged section, wrong numbers -> red), forged receipt (declared receipt whose rev differs ->
red), falsified wave line (seat count wrong) -> red. Deliver runnable drivers the L1 executes
post-freeze, each writing a receipt with command/exit/stdout sha256/UTC into
.ufo/waves/round-53/l1/controls/. Prove each control is able to fail: show the green twin
where applicable (the control harness catches a correct instrument as green, the broken
variant as red). Never execute against production paths; fixtures live in your scratch."""),
item("ExecSweep", "executor",
f"""Routed repair (r52 routed defect 5, carried from r51): draft the read-only misroot sweep
helper {W1}/ExecSweep/misroot-sweep.sh. It runs `git -C <fleet> status --porcelain` (fleet
path from --fleet, default /home/vgpnk/Projects/shokunin), classifies each untracked file by
content (does it name kaidoku/round-53? another lane? neither), prints a machine-readable
finding list, writes NOTHING, never deletes anything (classification only - the protocol's
copy+delete remediation stays the L1's manual act). Include a --selftest over a fixture repo
in your scratch (created as D=$(mktemp -d -p "$S") && git -C "$D" init -q with planted stray
files): one stray naming kaidoku round-53, one naming another lane, one neutral; assert the
classification and exit codes (0 no kaidoku strays, 1 kaidoku strays found). Also draft the
registry row text for it as a probe (not a gate).""",),
item("ExecCensusRegen", "executor",
f"""Routed repair (CritClaims F3 / CritTriV6 F1 follow-through): produce the documented
census3 regeneration flow {W1}/ExecCensusRegen/regen.md + regen.sh draft. After the round's
new instrument-registry rows land in SKILL.md, {LANE}/tools/round-51/census3.json must be
regenerated from the committed registry or `census3.py --check` goes red (census_outside).
Deliver: the exact command sequence (generate from a pinned REV, --check verification,
receipt placement under .ufo/waves/round-53/l1/), a dry-run proof on the CURRENT committed
bytes (no production write: run generate into your scratch copy and show --check green
against it), and the guard: what breaks if regen is skipped (cite the r52 findings). Read
{LANE}/tools/round-51/census3.py first. Receipts with exact commands/exits."""),
# ---------------- scribes (3) ----------------
item("ScribeSources", "scribe",
f"""Two deliverables under {W1}/ScribeSources/. (1) Draft SOURCES row S253 for the sasquatch
project (https://github.com/onekey-sec/sasquatch - README/usage docs): open the URL yourself
with a receipt (UTC, HTTP status, bytes, sha256), write the row in the exact 11-column
contract shape ({LANE}/corpus/SOURCES.md is the shape reference; no `|` inside any cell;
tier scoped, anchor = exact section + revision/date, teaches = one grounded learner benefit,
status queued, recheck cadence) - the row serves R53-C1's reader-refusal ground (claim_row:
S253). Provide a <=25-word contiguous located quote for the round lesson's Gate block, with
its section. (2) The W04 audit table: {LANE}/.ufo/waves/round-53/l1/census-start.txt lists 19
duplicate-URL W04 warnings; for each, read both rows in {LANE}/corpus/SOURCES.md and verdict:
true-duplicate-needs-supersedes / within-scope-legitimate (CORPUS.md rule 2: only status,
recheck, used-by change in place; a correction is a NEW row whose teaches opens
`supersedes S0NN -`). Propose the correction set ONLY if every proposed row is census-safe
(11 columns, no escaped pipes, valid enums); otherwise recommend keep-debt with reasons.
Read /home/vgpnk/Projects/shokunin/CORPUS.md SOURCES contract first."""),
item("ScribeLesson", "scribe",
f"""Draft {W1}/ScribeLesson/round-53.md - the round lesson skeleton the L1 finalizes. Sections:
header (round, authorship = lane), `## Gate` (candidates: S253 admit with URL/access
date/<=25-word located quote; the W04-correction decision as the >=1 reject slot or an
explicit held-open marker; spot-check = pending), `## Mistakes` with the two mined rows from
{LANE}/plans/round-53-claims.md Frontier step (mistake 1: r52 claims file quoted r51's retry
disposition with an invented qualifier "without proof able to fail" - class reference-drift,
evidence = the CritRetry findings file finding 1 ({LANE}/.ufo/waves/round-52/w1/CritRetry/findings.md)
vs the actual r51 text at {LANE}/plans/round-51-claims.md lines 351-352; captured-by: none - claims-file
citations are not Gate quotes (QUALITY 16/17/42 cover Gate quotes only); fix: verbatim
file:line citation rule, draft QUALITY row 100 text). Mistake 2: r51/r52 results handoffs
omitted per-seat id/status - class attribution, captured-by QUALITY 22, fix: per-seat
status.json + id/status results rows (this round's T3 atom demonstrates it). Cite every
claim: round + LOG entry or commit. Verify each evidence pointer resolves (open the files)
before writing it; a pointer that does not resolve is named, not smoothed."""),
item("ScribeKnowledge", "scribe",
f"""Draft the knowledge entry {W1}/ScribeKnowledge/2026-10-30-r53-ddwrt-reader-census.md (the
R53-C1 landing entry - DRAFT; the L1 lands it only after the counters pass). Provenance trio
first: `source:` cites SOURCES row S253 (sasquatch README, the claim_row) plus the committed
census lineage ({LANE}/corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md,
{LANE}/corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md, S250/S251); `verified-at:` =
the freeze commit (placeholder, resolved by the L1); `recheck:` = the counting command from
the claims file. Content: the fixture-level ddwrt reader census (15 envelopes; 6/7
NO-READER; the 1 reader-backed fixture; the FAILED body dmg_Z3_v3ddwrt_inode_table; the 7
clean residues), what table v6 changes (new row legacy-body-refused, narrowed
legacy-body-failure, clean-unverified moves, precedence, the audit), and the observation /
inference / unknown discipline (QUALITY 5/7): reader outcomes are observations with their
command receipts; routing prescriptions are the lane's rule; what was NOT examined (no new
reader validated, no REA run this round, corpus = the round-42 recon set). QUALITY criteria
4/6/8/10/11 apply. Mark every number with its counting command (CORPUS rule: a count carries
its command)."""),
# ---------------- scouts (3) ----------------
item("ScoutSasquatch", "scout",
f"""Open and receipt the round's new source candidate: https://github.com/onekey-sec/sasquatch
(README, usage docs, and the variant coverage notes - which SquashFS vendor mangles it
handles: DD-WRT/-nopad, Broadcom, AVM). Record: exact URL(s) fetched, UTC access time, HTTP
status, bytes + sha256 of what you kept, and a <=25-word CONTIGUOUS quote with its exact
section/heading (QUALITY 42: contiguous served bytes, location named; label composite if the
words cross tags). Assess tier (A/B/C) for the scope `ddwrt/no-pad SquashFS independent-reader
refusals and sasquatch's variant support` and what it teaches for R53-C1's census. Also check:
does the repo document WHICH sasquatch variant flag handles ddwrt v3 (e.g. -le/-be/-nopad
handling), and does it claim unsquashfs refuses such bodies? Keep fetched bytes in your
scratch, copy receipts + the kept excerpt into your seat dir."""),
item("ScoutCensus", "scout",
f"""Independently verify the ddwrt reader-census numbers from committed bytes only - this is
the per-fixture table R53-C1 freezes, so errors here are claim-killing. Read:
{LANE}/corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md (round-49 reader census,
v3-readers.out pointers), the round-50 oracle/census tables ({LANE}/tools/round-50/oracle/),
{LANE}/corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md, and the 15 ddwrt envelopes in
{ENVD} (grep for v3ddwrt in the envelope dirs; each envelope.json carries handler name, gap
kinds, published-file counts, subject name). Produce {W1}/ScoutCensus/census-verify.md: per
fixture - family, which readers refused/succeeded per the committed evidence (unsquashfs, 7z,
sasquatch), the FAILED-body list, the no-reader clean list (must come out at 7; if your count
differs, that is a finding that stops the freeze - say so loudly), and the 1 reader-backed
fixture. Also verify the claim `6/7 NO-READER` appears in or is derivable from committed
bytes, and name any fixture whose reader status the committed evidence does NOT determine
(those become declared-not-recaptured census rows). Receipts: exact commands, exits."""),
item("ScoutMerge", "scout",
f"""Scan the assimilation package /home/vgpnk/Projects/shokuknow/merge/kaidoku/ (READ-ONLY;
never write, never run campaign tools there): MERGE-REPORT.md (what was staged and why),
SOURCES.append.md (staged rows + id range), knowledge/ entries. Report
{W1}/ScoutMerge/scan.md: (1) does any staged theme fit THIS round's ground (fixture-level
reader census, SquashFS reader refusals, executability audits, record/calibration oracles)?
Name candidate entries with paths; (2) the staged id range vs the lane registry (lane now
holds 159 rows, S001..S253 with gaps - derive exactly); (3) feasibility of the adoption path
(id-collision scratch check, CORPUS-schema normalization, scratch mirror +
sources-census.sh validate --file) and its cost; (4) a clear recommend: adopt (which entries,
why they clear PROVINCE scope + QUALITY bar) or none this round (the honest default - mass
id drift + normalization cost vs round budget). Do not adopt anything; the L1 decides."""),
# ---------------- reviewers (3) ----------------
item("RevV6Port", "reviewer",
f"""Produce the port-fidelity checklist + test vectors the L1 applies when integrating
{W1}/ExecV6Port/sqfs-triage-v6.py. Read {LANE}/tools/round-50-c3/sqfs-triage-v5.py in full
(the port must preserve its scored semantics except the v6 changes) and
{LANE}/plans/round-53-claims.md R53-C1. Deliver {W1}/RevV6Port/checklist.md: (1) the exact
v5 behaviors that must survive byte-for-byte (row order, matching semantics per column,
published-count predicates, first-match, evaluator independence, exit-code map, receipt
fields); (2) the v6 deltas restated as testable assertions; (3) 8-12 concrete test vectors:
envelope -> expected v6 label+action+audit fields, drawn from the committed corpus
({ENVD}) including dmg_Z3_v3ddwrt_inode_table (must be legacy-body-refused /
preserve-unresolved, violation 0 after), one of the 7 clean residues (must be
clean-unverified / record-unverified), one reader-backed ddwrt clean (stays clean), and
non-ddwrt families (unchanged labels); (4) the precedence traps CritTriV6 F4 named
(legacy-body-refused vs no-reader-failure duplication - same action, narrower trigger: which
fires first and why it is not ambiguous). Every vector cites the envelope path it reads."""),
item("RevRecord", "reviewer",
f"""Produce the port-requirements list for {W1}/ExecRecord/r53-record.py from the PRIOR
oracle's found defects. Read {LANE}/tools/round-50/c2-record.py and its routed findings:
{LANE}/.ufo/waves/round-48/ (C2OracleLimit - worktree-sourced gate.py import; MutC1Rows -
lexical bypass), the round-49 lesson wave-2 counter misses, and
{LANE}/plans/round-53-claims.md R53-C2. Deliver {W1}/RevRecord/requirements.md: (1) each
historical defect as a named requirement (all helpers loaded from --rev bytes; no worktree
imports; semantic checks not lexical bags - T7's section parsing must bind declared values
to observed state, not shared words); (2) the exit-code map per the fleet gate standard
(0/1/2 semantics, undeclared nonzero = could-not-evaluate); (3) the selftest coverage bar
(outer-CLI invocation per QUALITY 61, git-fixture cases, expected exits + finding ids
committed); (4) attack surface: for each atom T1-T10, the cheapest forgery that would pass a
sloppy implementation and the check that refuses it. Cite file:line for every claim about
the r50 oracle."""),
item("RevClaims", "reviewer",
f"""Verify the round-53 declaration against the lane's own freeze-chain machinery BEFORE the
freeze. Read {LANE}/plans/round-53-claims.md at {BASE} and run the standing gates over it
(read-only; they run against committed bytes):
`python3 -I -B {LANE}/.ufo/waves/round-24/tools/freeze-gate.py` and
`python3 -I -B {LANE}/tools/round-29/freeze-gate.py --disclosures` (check their CLIs first
with --help or by reading them; if a gate needs a ledger state that only exists post-freeze,
say exactly what it will check and what the freeze commit must add to pass);
`python3 -I -B {LANE}/tools/round-31/freeze-integrity.py` against the claims file's
instruments map (it does not exist yet - verify the claims file's instrument-pin plan
satisfies its schema: top-level `instruments`, sha256 per file, QUALITY 68 container
shape). Deliver {W1}/RevClaims/conformance.md: (1) gate outputs (exact commands, exits);
(2) QUALITY 33/38/45/48/68 conformance of the declaration: instruments-before-claims
ordering plan, do-nothing controls before data, claim_row S253 binding, axis-fit fields,
predicate-sentence identity plan (same sentence in claims file / docstrings / receipt
labels - name the exact three locations per claim); (3) every gap the freeze commit must
close, as an ordered checklist; (4) anything in the claims file that violates fleet section
9 claim-sizing (universal clauses, do-nothing-reachable targets) with the fix. Receipts for
every command you run."""),
# ---------------- critics (3) ----------------
item("CritV6", "critic",
f"""Pre-freeze attack on R53-C1's design as declared at {BASE}
({LANE}/plans/round-53-claims.md). Read the r52 findings it claims to resolve
({LANE}/.ufo/waves/round-52/w1/CritTriV6/findings.md, MutTriV6/battery.md,
CritClaims/findings.md) and the v5 source {LANE}/tools/round-50-c3/sqfs-triage-v5.py. Attack:
(1) per resolved finding - is the resolution in the claims file actually closable as written,
or does it move the defect (e.g. does the census-conditioned clean row break the v5
evaluator's independence requirement? does witness-at-base + v6-at-landing actually measure
one variable?); (2) the pair-change arithmetic: v5 scored 126/126 pair_mismatches 0 at
1439dfe9 - enumerate exactly which envelopes change label under v6 (claim says 8) and verify
from committed bytes that the evaluator, implementing identical precedence over the same
census, agrees (pair_mismatches stays 0) - if the evaluator must ALSO change, is it still
independent?; (3) the census kill rule (recapture contradicts lineage -> stop): is
declared-not-recaptured load-bearing anywhere the audit needs a measured row?; (4) the
before-arm: can the witness at base be green for a reason other than the claimed defect
(with the v5 table at base, executability_violations 1 - verify from bytes, not the
claims text); (5) anything that makes the freeze's kill rule undecidable (the CritRuleDerive
F-3 class). Findings numbered with severity + smallest correction, receipts with
command/exit/sha256/UTC. This is attack, not judgment."""),
item("CritRecord", "critic",
f"""Pre-freeze attack on R53-C2's atom design ({LANE}/plans/round-53-claims.md R53-C2 at
{BASE}). Attack each atom T1-T10: (1) forgery paths - can the atom pass while reality
differs (e.g. T3 counts seat dirs: 25 empty dirs with valid status.json but no work? T4:
receipts whose rev field is edited post-hoc - does anything bind receipt bytes to a commit
time? T6: row counts that match while a row was swapped - cite QUALITY 74)?; (2) the freeze
expectation `mismatches 8` - is it exactly derivable (which atoms are green at freeze and
why: T1 true at freeze, T2 true at freeze - verify from the declaration commit {BASE} bytes
that T1/T2 DO hold there); (3) do-nothing-reachability - what is the cheapest sequence that
reaches mismatches 0 without doing the round's work (committing an honest-looking record
over no work: which atom stops it - if none, the claim is wrongly sized, say so); (4)
separability - does any atom actually read C1's artifacts such that C2 fails when C1 lands
nothing (T4 names C1 receipts? then the record must declare their absence honestly - check
the atom text supports that); (5) no-op mutants - which battery mutations would NOT flip
their atom (the MutRecord spec must know). Findings numbered, severity, smallest correction,
receipts."""),
item("CritBand", "critic",
f"""Attack the round-53 wave shape and dispatch machinery. Read
{LANE}/plans/round-53-claims.md (Wave shape section), the rendered dispatch
{LANE}/.ufo/waves/round-53/r53-w1-dispatch.json (it exists when you start), and the r52
findings {LANE}/.ufo/waves/round-52/w1/CritBand/findings.md (F1-F13). Attack: (1) the
dispatch interpolation check - re-run the r52-era check on THIS dispatch and then attack it
with the CritBand blind spots - the exact token forms are in the r52 findings F1/F2
(lowercase brace tokens, single-character brace tokens, angle-bracket ALL-CAPS forms);
reproduce them and report what passes that should not; (2) per-seat accounting: the status.json schema in
the wave context - is `blocked` distinguishable from `failed`? does the L1's planned
accounting (claims file atom T3) have a no-dir blind spot (CritBand F3: a seat with no
directory is invisible)? propose the exact accounting rule that closes it; (3) attack-share
arithmetic: verify 10/25 from the dispatch's role fields, and the strict 8/25; (4) results
id/status: does the wave context bind the orchestrator's results.json id/status fields into
T3 tightly enough (what if the handoff again omits ids - what does the honest record say?);
(5) seat counts: 25 seats within the 16-32 band; any role the route table cannot serve?
Findings numbered with severity + fix; receipts."""),
# ---------------- mutation-testers (2) ----------------
item("MutV6", "mutation-tester",
f"""Produce the v6 mutation battery spec {W1}/MutV6/battery.md (measured, not asserted - the
MutTriV6 standard). Read {LANE}/.ufo/waves/round-52/w1/MutTriV6/battery.md +
findings + probe/ (7 scripts), {LANE}/plans/round-53-claims.md R53-C1, and the v5 source.
Measure over the committed corpus {ENVD} with your own probe scripts in scratch: for each
candidate v6 mutation - (a) legacy-body-refused row deleted, (b) row moved after
legacy-body-failure (precedence break), (c) census condition dropped (family-key), (d)
swapped actions preserve-unresolved<->cross-read-legacy, (e) clean-unverified census
condition dropped, (f) audit counter inverted, (g) clean_residue counter inverted,
(h) evaluator census input redirected to a junk census, (i) label spelling mutated -
which envelopes flip, which receipt field changes, expected exit? Then the synthetic
fixtures: the reader-backed ddwrt FAILED body (which mutants it catches that the corpus
cannot - the corpus has exactly 1 ddwrt FAILED body and it is no-reader, so family-key and
precedence mutants are corpus-vacuous: your synthetic witness must be the red arm) and a
14th-fixture census mutation (census-tamper arm: census row flipped no-reader -> reader-backed
without evidence: the audit must go red on the corpus envelope, catching census tampering).
18 receipts minimum (command, exit, stdout sha256, UTC). Every corpus-vacuous mutant is
declared vacuous-in-corpus with its synthetic red arm - never claimed as corpus-measured."""),
item("MutRecord", "mutation-tester",
f"""Produce the record-oracle mutation battery spec {W1}/MutRecord/battery.md. Read
{LANE}/plans/round-53-claims.md R53-C2 (atoms T1-T10, battery bullet) and
{LANE}/tools/round-50/c2-record.py's battery shape. Deliver >=10 record mutations, each
naming: the mutated bytes (which file, which declared value), the atom it flips, the
expected exit + finding id, and how a no-op is detected (a mutation that changes nothing
must be refused by the battery harness, not counted as a flip). Measure what you can now:
the current record state (SCORECARD has no round-53 section yet; LOG has the declaration
entry at {BASE}) - so verify T2's green-at-freeze expectation from bytes (LOG entry present
at the base, no deletions) and T1's pin plan (the claims file has an instruments plan - what
exactly must the freeze add). Include the falsified-section control spec (a section whose
numbers are wrong in exactly one atom -> mismatches 1), the forged-receipt control (rev
mismatch), and the seat-count control (declared 25 vs 24 dirs). Probe scripts in scratch,
receipts with command/exit/sha256/UTC."""),
# ---------------- connectors (2) ----------------
item("ConnSiblings", "connector",
f"""Sibling-overlap scan for the round-53 landing. Read {LANE}/PROVINCE.md (Core/Frontier/
Adjacent), then the sibling provinces that could contest the ground R53-C1 lands: the ddwrt
SquashFS reader census, triage routing rules, executability audits, record/calibration
oracles. Check at least: /home/vgpnk/Projects/shokunin/revenger-shokunin/PROVINCE.md
(runtime debugging vs static routing?), tsukuroi-shokunin (update-safety: squashfs handling
of system images?), kasegi-shokunin (bounty/security research: firmware analysis overlap?),
souji-shokunin. Deliver {W1}/ConnSiblings/overlap.md: per sibling - does its province claim
any of this ground (cite the exact lines)? contested-scope risks for landing block 27 + the
census; the kaidoku/revenger runtime-arbitration open item (r23/r52 reports) - does v6 touch
it? (it must not: v6 is static routing only - verify the claims text says so). No verdicts;
findings for the L1's report."""),
item("ConnSources", "connector",
f"""Cross-source pattern scan feeding the W04 dedupe decision and the census lineage. Read
{LANE}/corpus/SOURCES.md (the 19 W04 duplicate-URL warnings are listed in
{LANE}/.ufo/waves/round-53/l1/census-start.txt) and CORPUS.md rule 2. Deliver
{W1}/ConnSources/patterns.md: (1) for each duplicate cluster (several rows share one URL
across scopes): are the scopes genuinely different (tier A for scope X, B for scope Y) or
drifted copies? name clusters where a supersedes row is warranted vs where the duplicate is
load-bearing for different claims; (2) the S253 candidate (sasquatch repo): do existing rows
already cover it (S112/S118/S120/S121/S122 name unblob/sasquatch paths - which rows cite
sasquatch and with what anchors)? would S253 duplicate them (W04 risk!) or genuinely add the
variant-coverage ground? (3) pattern across the corpus: rows whose recheck dates have passed
(they are freshness debt, not this round's duty - just count them). Findings only; no
registry edits."""),
# ---------------- sentinel (1) ----------------
item("SentScope", "sentinel",
f"""Scope and safety audit of this wave's own dispatch. Read the rendered dispatch
{LANE}/.ufo/waves/round-53/r53-w1-dispatch.json and the wave context inside it. Audit:
(1) interpolation: scan EVERY item string for unresolved placeholders in all forms - brace-delimited ALL-CAPS tokens, brace-delimited lowercase tokens, single-character brace tokens, and angle-bracket ALL-CAPS forms of three or more characters (like the words LANE, BASE, REV wrapped in angle brackets) - report exact item names + offsets; (2) scope: every path any item names must be inside
/home/vgpnk/Projects/shokunin/kaidoku-shokunin or the explicit read-only externals
(/home/vgpnk/Projects/shokuknow for ScoutMerge, /home/vgpnk/.omp/agent/RULES.md,
/home/vgpnk/.agents/skills/godspeed/directive.md, /home/vgpnk/Projects/shokunin/scripts/
+ .ufo read-only) - flag any write-intent path outside the lane; (3) forbidden verbs:
no git commit/push/stash/reset/checkout/switch by seats, no pacman, no rea runs, no
agent://all - check the context states them and no item contradicts it; (4) credential
hygiene: no item asks for cookies/tokens/headers; (5) the status.json schema is stated
per-seat. Deliver {W1}/SentScope/audit.md with findings + the exact audit commands
(re-runnable), receipts."""),
# ---------------- revenger (1) ----------------
item("RevV5Gate", "revenger",
f"""Reverse-engineer the v5 instrument's freeze-gate and table-loading behavior so the r53
witness avoids inheriting its defects. Target: {LANE}/tools/round-50-c3/sqfs-triage-v5.py
(read-only). Established facts to verify and extend: (a) CritClaims F2 - the --freeze gate
refuses a freeze not descending from the claims-draft base (resolved hash ancestry check,
around :1261-1263): state the EXACT check (which hashes, which git call, what makes
base-descending fail when freeze descends from round-start but not from the claims draft);
(b) MutTriV6 F1 - --table accepts only a file, not a directory, and tools/round-50-c3/
holds no table file: state exactly what --table expects and what the SKILL-marker extraction
(--print-v5-block?) actually emits; (c) how the instrument reads SKILL.md at --rev vs --skill
- which byte source wins and can they disagree. Deliver {W1}/RevV5Gate/gate-semantics.md:
the precise semantics, minimal witness design that reads the BASE bytes via git show while
refusing newer-than-freeze revs, and >=4 test vectors (fixture repos in your scratch:
base-descending freeze pass, non-descending refusal, mutated base byte detection,
table-file-vs-marker behavior) with receipts (command/exit/sha256/UTC). Also: anything else
in the v5 gate you find that the r53 instruments must not copy."""),
# ---------------- band-fill seats (operator amended the run-13 band 16-32 -> 32-48 mid-run) ----------------
item("ExecPredicate", "executor",
f"""Draft the predicate-identity checker {W1}/ExecPredicate/predicate-identity.py (the
QUALITY 68 instrument): args --root --rev --claims <plans/round-53-claims.md path> --json-out;
it extracts each claim's predicate sentence from the claims file and verifies the SAME
sentence appears byte-identical (modulo whitespace normalization ONLY where the claims file
wraps lines) in (1) the named instrument docstrings read from `git show REV:<path>` and
(2) the receipt-label constants in those instruments. It fails (exit 1) naming the first
location where the sentence diverges, and exit 2 on a missing file/rev. --selftest over
fixture trees in scratch: one green fixture (all three locations agree), one red (docstring
paraphrases the sentence), one red (receipt label differs), one exit-2 (missing instrument).
This becomes the freeze gate for predicate identity; the L1 runs it at the freeze and cites
the receipt. Read {LANE}/.ufo/waves/round-34/r34b/predicate-reconciliation.json for the
historical defect class it prevents."""),
item("ScribeBlock27", "scribe",
f"""Draft the SKILL.md rule block 27 text {W1}/ScribeBlock27/block-27.md: the prose paragraph +
the complete `<!-- sqfs-triage-table v6 -->` table in the exact SKILL table format (copy the
format from block 26's marker region: comment markers, sqfs-triage-actions vocabulary line -
extended only if the v6 row introduces no new action, the 13-column header, every row with
all cells filled including cause and source). Content per {LANE}/plans/round-53-claims.md
R53-C1: new row legacy-body-refused (action preserve-unresolved, census-conditioned),
legacy-body-failure narrowed (census condition in the row text + cause), the seven ddwrt
no-reader clean envelopes routing clean-unverified (census condition on the clean row - note
the row's handler cell must name the census condition honestly: the census is fixture-level,
so the row text says the census decides), precedence note, and the Status paragraph marked
NOT-YET-SCORED (the L1 replaces it with the scored status at landing). Keep block 26 as
history (dated supersession note at the top of block 27, exactly how block 26 superseded
block 21). Every source citation in row cells must resolve (check them)."""),
item("ScoutPrior", "scout",
f"""Produce the frozen-corpus manifest the instruments pin: {W1}/ScoutPrior/corpus-manifest.json
+ manifest.md. For the envelope corpus {ENVD}: count the envelope dirs (claim says 126),
verify each holds a parseable envelope.json, record per-envelope: name, subject digest from
the envelope bytes, operation, provider version; and the corpus sha256 manifest (sorted
path+sha256 list, whole-tree digest). Also: re-run the v5 instrument selftest OFFLINE in your
scratch ({W1}-clone of the lane at {LANEBASE}; `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py
--selftest` with TMPDIR in your scratch) and record its exit + case count - the v6 port must
match or exceed it, and the receipt proves the baseline instrument was green BEFORE the port.
Flag any envelope that fails to parse (that is a corpus-integrity finding that stops the
freeze). Receipts: exact commands, exits, sha256s."""),
item("RevControls", "reviewer",
f"""Review the control-suite design against the fleet's control discipline BEFORE the
instruments are integrated. Read {LANE}/plans/round-53-claims.md (controls bullets, both
claims), {LANE}/.ufo/waves/round-52/w1/ExecControls/ + ExecCounterV2/ (the r52 control drafts
and their critique), and QUALITY rows 48, 50, 58, 61, 67 in {LANE}/corpus/QUALITY.md.
Deliver {W1}/RevControls/control-review.md: (1) for EACH planned control (C1: do-nothing,
junk table, audit-guard-deleted, family-key + synthetic reader-backed witness, swapped-action,
clean-unverified-suppressed; C2: freeze do-nothing, junk record, forged receipt, falsified
wave line): is it scoreable pre-data with a frozen instrument, able to fail, and immune to
the QUALITY 50 class (a green sandbox fixture that breaks the intent)? (2) the missing
controls the r52 rounds should have had (e.g. an id-keyed shortcut control for T3: a
do-nothing fixture with 25 fake-but-valid seat dirs must NOT satisfy T3's work-existence
expectations); (3) the exact receipt file naming + location plan
(.ufo/waves/round-53/l1/controls/) and what each receipt must contain to be citable
(QUALITY 73: argv, reader digest, commit, UTC or caller_asserted). Cite file:line for
every claim."""),
item("CritCensus", "critic",
f"""Attack the evidentiary strength of the frozen reader census R53-C1 depends on
({LANE}/plans/round-53-claims.md, Frozen census bullet; {LANE}/.ufo/waves/round-52/w1/CritTriV6/findings.md
F3/F7). Questions to answer from committed bytes: (1) for EACH of the 15 ddwrt fixtures, does
committed evidence actually determine reader-backed vs no-reader, or does the claim rest on a
summary line ({LANE}/corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md and the round-50
tables - cite the exact row for each fixture)? (2) the 6/7 figure - count it yourself from the
committed census rows; if the committed evidence determines only N<15 fixtures, name the gap
and what the census's declared-not-recaptured rows would mean for the audit's verdicts (a
NO-READER declaration without a retained command receipt: can the audit's executability
violation for dmg_Z3_v3ddwrt_inode_table stand on lineage alone? QUALITY 73/30/24 apply);
(3) the recapture kill rule - what happens if a recipe exists but mksquashfs is not installed
(check `command -v mksquashfs unsquashfs 7z sasquatch`), or the regenerated bytes differ from
the lineage digests (is there a lineage digest to compare?); (4) S251's correction: the writer
flag is -nopad, and neither fact establishes DD-WRT independent-reader support - does any
census row overclaim sasquatch success as reader-BACKED (sasquatch is the extractor, not an
independent second reader - is the census's reader-backed/no-reader axis even defined per
reader? state the definition the census must freeze). Findings numbered, severity, smallest
correction; receipts."""),
item("MutWitness", "mutation-tester",
f"""Produce the witness mutation battery spec {W1}/MutWitness/battery.md (measured where
possible). The witness ({W1}/ExecWitness/v5-baseline-witness.py draft, and its spec in
{LANE}/plans/round-53-claims.md R53-C1 Before bullet) is itself a gate - attack it: mutants
(a) reads HEAD/worktree SKILL.md instead of git show REV:SKILL.md (the base-drift arm:
mutate the worktree SKILL.md, witness verdict must NOT change), (b) rev-newer-than-freeze
refusal removed, (c) executability_violations counter inverted, (d) clean_residue counter
dropped, (e) census input swapped for a junk census, (f) the named-envelope check hardcoded
to the expected name instead of derived (the forgery arm: a witness that always prints
violations 1 naming dmg_Z3... - what input exposes it? a synthetic base where the v5 table
does NOT produce the violation must go green/red correctly). For each: the fixture (git
fixture repo in your scratch per the context recipe), expected exit + finding, and whether
the corpus can witness it or a synthetic base is required (declare vacuous-in-corpus where
so). Probe scripts in scratch; receipts command/exit/sha256/UTC."""),
item("ConnFleet", "connector",
f"""Cross-lane pattern scan: how do sibling lanes build record/calibration oracles and
pre-freeze control batteries? Sample at most three sibling repos read-only: /home/vgpnk/
Projects/shokunin/souji-shokunin, tsukuroi-shokunin, kengaku-shokunin - grep their tools/
for record/atom/calibration counters and their corpus/claim-freezes ledgers. Deliver
{W1}/ConnFleet/patterns.md: (1) per lane: does it run record-oracle-style calibration claims,
and what do its counters check that kaidoku's T1-T10 do not (steal good checks - e.g.
append-only verification, timestamp ordering, freeze-gate integration); (2) named patterns
worth adopting THIS round (each with the sibling file:line as pointer); (3) anything kaidoku
does that siblings lack (for the report's cross-lane section). Read-only; no verdicts about
sibling quality - patterns only."""),
]

spec = {
    "wave": "r53-w1",
    "milestone": "r53-w1 build+attack: triage-v6 port, witness, reader census, record oracle, controls, sources/lesson/knowledge drafts, pre-freeze attacks and batteries; L1 freezes, scores controls, lands, re-counts",
    "reportDir": ".ufo/waves/round-53/w1",
    "context": CONTEXT,
    "items": items,
}

out = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-53/r53-w1-spec.json')
out.write_text(json.dumps(spec, indent=1))
print(f"wrote {out} items={len(items)}")
roles = {}
for it in items:
    roles[it['role']] = roles.get(it['role'], 0) + 1
print("roles:", roles)
attack = roles.get('reviewer',0)+roles.get('critic',0)+roles.get('mutation-tester',0)+roles.get('sentinel',0)+roles.get('revenger',0)
print(f"attack share (5-role): {attack}/{len(items)} = {100*attack/len(items):.2f}%")
strict = roles.get('reviewer',0)+roles.get('critic',0)+roles.get('mutation-tester',0)
print(f"strict attack share: {strict}/{len(items)} = {100*strict/len(items):.2f}%")
# interpolation self-check on emitted strings
import re
bad = []
def scan(s, where):
    for m in re.finditer(r'\{[A-Za-z_][A-Za-z0-9_]*\}|<[A-Z][A-Z0-9_]{2,}>', s):
        bad.append((where, m.group(0)))
scan(spec['context'], 'context')
for it in items:
    scan(it['prompt'], it['name'])
print("placeholder hits:", bad if bad else "none")
