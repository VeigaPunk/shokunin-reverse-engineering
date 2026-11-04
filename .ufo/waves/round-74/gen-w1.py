#!/usr/bin/env python3
"""Generate the round-74 wave-1 spec (r74-w1): 15 seats, one v1 wave."""
import json
import pathlib

WAVE = "r74-w1"
REPORT_DIR = ".ufo/waves/round-74/w1"
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
Scratch: create ONE dir `/fast/scratch/hyaku/kaidoku-r74/<your-seat-name>/` (mkdir -p), pass it explicitly
(TMPDIR=... and any --work), and delete it with `trap 'rm -rf -- "$S"' EXIT` (or a
finally:) before you yield; receipts first copied under
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/<your-seat-name>/.
Never run `git`/`jj` writes, never commit, push, stash or check out anywhere; read-only
git (`log`, `show`, `diff`, `status`, `ls-files`, `rev-parse`) is fine. Never touch
/home/vgpnk/Projects/shokunin/.ufo/state/, .ufo/watchdog.log, MANIFEST.json, templates/,
scripts/, or another lane. Never message agent://all.
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

FROZEN = """## Frozen state (round 74)
base `04fdc2c4dbedbe5ee50a069af14310068393233e` (the round-73 lane tip); declaration
`b3a7e28089582ce5fb002a1b88e5295caf696b9f` (five round-74 instruments + plans/round-74-claims.md
+ the census-start receipt, committed BEFORE any claim data); freeze
`021914c0e638454e507087accfe41af1ab69f185` (claims.json + the pre receipts; the round-29 gate
audits it CLEAN, no findings).
Claims (frozen sentences in plans/round-74-claims.md and .ufo/waves/round-74/claims.json):
R74-C1 operability -- the six A12 selftest survivors round-73's MutProbe reported are each
  killed by a declared case: battery patch set r74probe survivor_count 0 (10 mutants, pristine
  20 cases, target pinned) while patch set r73probe on the landed round-73 probe names exactly
  the six survivors.
R74-C2 calibration -- the round-74 record audit (16 atoms: D1-D7 retained, D7b and D8-D15 added
  from the round-73 spot-check's routed defects 1-8 and planned items b/d) reports
  mismatch_count 11 at base 04fdc2c4 and 0 at the landing revision.
Instruments (committed at the declaration; `python3 -I -B`):
 tools/round-74/seam-probe.py, tools/round-74/probe-mutation.py, tools/round-74/record-audit.py,
 tools/round-74/freeze-pins.py, tools/round-74/controls.py.
Pre receipts (committed at the freeze): .ufo/waves/round-74/pre/c1-base-arm.json (r73probe: 6
survivors), c1-post-at-declaration.json (r74probe: 0 survivors), c2-at-base.json (mismatch_count
11), controls-at-declaration.json (4 of 4 arms met), freeze-pins-before-freeze.json (9 rows, 0
mismatches).
Round-73 receipts the arms may read: .ufo/waves/round-73/l1/scores/*.json,
.ufo/waves/round-73/pre/*.json, .ufo/waves/round-73/w1/MutProbe/results.json.
REA 6.5.0 package root: /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
Pinned packer: /usr/bin/upx (upx 5.2.0, sha256
 cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969); make your own
 scratch copy for --expect-upx (it must NOT be the module default /usr/bin/upx).
Round-73 route receipt: .ufo/waves/round-73/pre/route-at-declaration.json (its nonce commitment
 is .ufo/waves/round-73/l1/nonce-commitment.txt); the round-73 landing probe receipt is
 .ufo/waves/round-73/l1/scores/c1-at-landing.json (12 of 12 arms).
Hyperfocus your assignment; never deviate. Return a short JSON
(files_changed, behavior, evidence, risks) and delete your scratch dir before you yield.
"""

ITEMS = []


def item(name, role, body):
    ITEMS.append({"name": name, "role": role,
                  "prompt": GODSPEED + BOUNDS + FROZEN + "\n## Assignment: " + name +
                            f" ({role})\n" + body.strip() + "\n"})


item("ExecProbeCases", "executor", """
## Target
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-74/seam-probe.py (read-only) and
.the/ufo/waves/round-74/w1/ExecProbeCases/ (your evidence dir). Do not edit lane files.

## Change
Independently re-derive that EACH of the six new selftest cases binds its conjunct, without
using tools/round-74/probe-mutation.py. For each of these six defect classes apply the hand
mutation to a scratch copy of the probe and run `--selftest` (TMPDIR set, cwd the lane):
 1. delete `and not s.get("canary_present")` from `a12_verdict`'s genuine_ok (expect
    `a12-genuine-canary-only` to fail);
 2. make `_proc_env`'s `except OSError` branch return `{}` instead of `None` (expect
    `a12-proc-environ-unreadable`);
 3. make `kernel_witness` return `list(seen.values())[:1]` (expect
    `a12-kernel-multiple-samples`);
 4. delete the `"canary_present": ...` entry from the sample dict (expect
    `a12-kernel-canary-field`);
 5. swap the two witness arguments in `assemble_arm`'s verdict call (expect `a12-arm-wiring`);
 6. make `forged_subrun` return `{"rc": [], "shims": {}, "kernel": {}}` before its first
    statement (expect `a12-arm-forged-executed`).
Also run the pristine selftest (expect 20 cases, no failures) and record, per mutation, the
exact `failures` list.

## Acceptance
Per mutation: rc 1 and the declared case name present in `failures`; no other declared case
fails for a mutation that is not its own (report any cross-binding); pristine rc 0 with
`cases 20`. Receipt JSON at .ufo/waves/round-74/w1/ExecProbeCases/receipt.json with a
`rows` array (variant, rc, failures, verdict) and a `pristine` object. Report anything that
does not hold as a defect with its exact output.

## Evidence
.report .ufo/waves/round-74/w1/ExecProbeCases.md plus the receipt.
""")

item("ExecBattery", "executor", """
## Target
tools/round-74/probe-mutation.py (read-only) and .ufo/waves/round-74/w1/ExecBattery/.

## Change
From the committed blobs at the freeze revision `021914c0e638454e507087accfe41af1ab69f185`:
 1. run patch set r73probe against tools/round-73/seam-probe.py with
    `--expect-survivors 6`; record survivor names;
 2. run patch set r74probe against tools/round-74/seam-probe.py with `--expect-survivors 0`
    and `--expect-target-sha256 $(git show <rev>:tools/round-74/seam-probe.py | sha256sum)`;
 3. run `--validate` on both receipts (expect no defects);
 4. tamper a copy of the r74probe receipt (set `survivor_count` to 1) and run `--validate`
    (expect a named defect);
 5. prove the battery refuses a mismatched pair: `--patch-set r74probe --tool
    tools/round-73/seam-probe.py` (expect exit 2, unevaluable).
Use `--work` under your scratch dir. Do not edit lane files.

## Acceptance
Both arms exit 0 with the frozen expectations; both validations behave as stated; every
command line, exit code and the two survivor lists are in the report. Any deviation is a defect
reported with raw output, never smoothed.

## Evidence
.report .ufo/waves/round-74/w1/ExecBattery.md plus receipts JSON copies under
.ufo/waves/round-74/w1/ExecBattery/.
""")

item("ExecAuditRun", "executor", """
## Target
tools/round-74/record-audit.py (read-only) and .ufo/waves/round-74/w1/ExecAuditRun/.

## Change
 1. Run the audit at base `04fdc2c4dbedbe5ee50a069af14310068393233e` (expect exit 1,
    mismatch_count 11, naming D3, D6, D7b, D8, D9, D10, D11, D12, D13, D14, D15) and at the
    freeze revision `021914c0e638454e507087accfe41af1ab69f185` (expect exit 1; report which
    atoms are still false and why).
 2. For each of the nine atoms added this round, state the exact committed byte that makes it
    true or false, and whether that reason is the routed defect the plan names.
 3. Run `--validate` on both receipts (expect no defect).
 4. Flip one atom's `ok` in a valid receipt without updating `mismatches` and run `--validate`
    (expect a named defect).
Do not edit lane files. Use `--json-out` under your evidence dir.

## Acceptance
Per-atom table with the committed evidence and the routed-defect mapping; the two exit codes
and mismatch counts; the validate behaviours. Any atom whose reason does not match its routed
defect is a defect of the atom, reported.

## Evidence
.report .ufo/waves/round-74/w1/ExecAuditRun.md plus the receipts.
""")

item("ExecArm", "executor", """
## Target
The full round-74 seam probe (A1-A12) run end-to-end, to show the round-74 refactor
(`kernel_witness` injectable readers, `forged_subrun`, `assemble_arm`) preserves the runtime
A12 verdict. Evidence dir .ufo/waves/round-74/w1/ExecArm/.

## Change
Run:
```
TMPDIR=<scratch> python3 -I -B tools/round-74/seam-probe.py --root . --rev <freeze-rev> \\
  --tool tools/round-73/packed-elf.py --battery tools/round-73/mutation-check.py \\
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \\
  --work <scratch> --receipt .ufo/waves/round-73/pre/route-at-declaration.json \\
  --receipt-rev <the revision that receipt names in its own `rev` field> \\
  --expect-upx <your scratch copy of /usr/bin/upx> \\
  --nonce-commitment "$(cat .ufo/waves/round-73/l1/nonce-commitment.txt)" \\
  --json-out <your evidence dir>/probe-at-freeze.json
```
Read `--receipt-rev` from the receipt's own `rev` field; never guess it. Compare your arm rows
with .ufo/waves/round-73/l1/scores/c1-at-landing.json: same arm ids, same pass/fail pattern,
`arms_passed 12` of `target 12` with `A12_kernel_witness` true (or report the exact divergence
with both receipts' rows). If the host refuses a carrier, say so with the typed refusal and
leave the arm's status unknown; do not fabricate.

## Acceptance
A row-by-row comparison table plus the raw probe receipt. A divergence is a defect of the
refactor and reported as one. Do not edit lane files.

## Evidence
.report .ufo/waves/round-74/w1/ExecArm.md plus the receipt.
""")

item("ExecRepairs", "executor", """
## Target
Three record files you own this round: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md,
corpus/README.md and PROVINCE.md. No other seat edits them; you edit nothing else.

## Change
 1. SCORECARD.md `## Capabilities` table: append three rows for the round-73 acquisitions
    (kernel-side environment witness bound by ancestry; the record-vs-receipt audit; the
    reader-seam selftest closure) and two rows for round 74 (the probe-mutation closure: the
    ten defect classes scored against declared cases with `probe-mutation.py`; the record-audit
    v2: sixteen atoms over the round-73 routed set with `record-audit.py`). Each row: capability
    | what it can now do | evidence pointer that RESOLVES at the freeze revision | first-working
    round (73 / 74). Keep the existing table format exactly.
 2. In the SCORECARD round-73 section, append (never rewrite filed bytes) a block beginning
    `**Before-arm selection (round 74 correction)**` naming R73-C1's before-arm receipt
    (`pre/c1-at-base-r72probe.json`, 11 arms) and the role of the other before run
    (`pre/c1-at-base.json`, 8 of 12: the route differential, not the before-arm).
 3. corpus/README.md: restore its trailing newline (it currently ends with `.`); change nothing
    else.
 4. PROVINCE.md: append a `## Round-74 additions to Core` section (one short table or bullet
    list) naming the selftest case closure for the kernel-witness arm as Core for
    tools/round-74/seam-probe.py, and what stays Frontier (a wrapper that never runs a sampled
    process, `PR_SET_MM_ENV_START` relocation, non-linux substrates, signed receipts).

## Acceptance
Every appended row's evidence pointer resolves with `git show <freeze-rev>:<path>`; the table's
row grammar is unchanged (pipe count per row equal to its header); README ends with `0a`; no
filed line is deleted. Report the exact diff hunks you made.

## Evidence
.report .ufo/waves/round-74/w1/ExecRepairs.md
""")

item("ScribeRows", "scribe", """
## Target
corpus/SOURCES.md (you own this file this round; no other seat edits it).

## Change
 1. Open `https://man7.org/linux/man-pages/man2/ptrace.2.html` (one GET), save the bytes under
    .ufo/waves/round-74/w1/ScribeRows/, record size + sha256, and register row **S278**: kind
    `docs`, tier A, scope = what `PTRACE_MODE_READ_FSCREDS` is and that `/proc/<pid>/environ`
    access is governed by that check; anchor = the located sentence; teaches = an unreadable
    environ is a permission outcome, so a reader must omit that process rather than read it as
    empty; status `mined`; opened 2026-11-04; recheck `on-release`; used-by =
    `corpus/knowledge/2026-11-04-r74-probe-mutation-closure.md`. Keep the row grammar: 11 cells,
    no literal or escaped `|` inside a cell, and a located quote of at most 25 words.
 2. S275 `used-by`: append `corpus/knowledge/2026-11-04-r73-kernel-witness-record.md` to the
    cell (routed defect 2); log the old value in your report.
 3. Register four `rejected` rows (S279-S282) for the pages opened and rejected in round 73:
    `proc.5.html` (31 125 B stub, 0 hits for "complete command line"), `proc_cmdline.5.html`
    (documents /proc/cmdline, kernel boot arguments), `proc_pid.5.html` and the man-pages
    section-5 index — each with the reason and a flip condition, per the registry contract.
 4. `## Search log`: add a round-73 note and a round-74 note, each in the established form
    (question, where searched, identified/screened/included/excluded, stop rationale).

## Acceptance
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
exits 0 after your edit (paste the output), 184 rows before, 189 after; every new row has a
located quote and the opened/sha256 record in your evidence dir; no filed row is deleted.

## Evidence
.report .ufo/waves/round-74/w1/ScribeRows.md plus the snapshot and its digest.
""")

item("ScribeKnowledge", "scribe", """
## Target
New file corpus/knowledge/2026-11-04-r74-probe-mutation-closure.md (you own it).

## Change
Write the knowledge entry for R74-C1: what the round-73 mutation probe found (the six A12
survivors on the landed round-73 probe: `a-drop-genuine-canary`, `b-unreadable-empty`,
`b-first-sample-only`, `b-drop-canary-field`, `c-swap-verdict-inputs`, `c-skip-forged-subrun`),
what each new case binds and which seam it needs (`kernel_witness` injectable readers and one
deterministic pass, `forged_subrun`, `assemble_arm`), the exact counts (pristine 14 -> 20 cases;
base arm 4 killed / 6 survived; r74 arm 10 killed / 0 survivors), and the limits: the battery
scores `--selftest` only, a live A12 run is separate evidence, a mutation survivor is a test
coverage finding and never permission to weaken the contract.
The entry opens with the provenance trio as the first three line-start fields:
`source:`, `verified-at:`, `recheck:` (QUALITY row 131), and it cites **S278** (ptrace(2),
`PTRACE_MODE_READ_FSCREDS`) for the unreadable-environ case and S275/S277 for the channel.
Quote at most 25 words from S278 and name the located anchor.

## Acceptance
The trio is line-start within the first 12 lines; every cited path resolves at the freeze
revision; every number in the entry re-derives from a committed receipt (name which receipt
per number); the Limits section names the selftest-only scope.

## Evidence
.report .ufo/waves/round-74/w1/ScribeKnowledge.md
""")

item("ScribeLesson", "scribe", """
## Target
New file corpus/lessons/round-74.md (you own it).

## Change
Write the round-74 lesson with its contract sections:
 1. `## Mistakes` — at least one mined mistake in the class|evidence|captured-by|fix table
    shape. Candidate: round 73 froze a before-arm comparator the instrument could not produce
    (the plan said 11 of 12; the round-72 probe reports 8 of 12) and pinned two producer
    digests that were not the blobs at the freeze commit — one class: a record value written
    from a plan rather than from bytes. Give the evidence pointers (the freeze container, the
    spot-check §6, the pre receipts), the criterion that should have caught it (the
    freeze-pin procedure; the before-arm selection block) and the fix.
 2. `## Gate` — the sources opened this round (S278 ptrace(2); the four round-73 rejected pages)
    with URL, access date, a ≤25-word located quote, and the digestion of each.
 3. A short `## What the wave found` section left for the L1 to complete.
Also draft, in your report (not in the lesson), the exact SCORECARD round-74 section text the
L1 can apply: the two claim rows with before->after numbers, the `lowest-axis: calibration`
line, the census erratum naming BOTH the reported 24 W04 lines and the measured 23, and the
three trend verdicts. Numbers must come from committed receipts.

## Acceptance
The lesson's Gate quotes are located and ≤25 words; every evidence pointer resolves; the
draft SCORECARD text carries re-derivable numbers and the erratum names both values.

## Evidence
.report .ufo/waves/round-74/w1/ScribeLesson.md
""")

item("ScoutSource", "scout", """
## Target
Independent source verification for the round's sourced claim. Evidence dir
.ufo/waves/round-74/w1/ScoutSource/ (own it).

## Change
 1. Fetch `https://man7.org/linux/man-pages/man2/ptrace.2.html` (one GET), keep the bytes,
    digest them, and locate the `PTRACE_MODE_READ_FSCREDS` description — quote it verbatim with
    its section anchor.
 2. Re-open `https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html` and confirm (or
    refute) that the page states the environ read is governed by that same check; quote the
    sentence.
 3. Check whether the man7 section-5 index and `proc(5)` still carry the text the round-73
    rejection claimed they lack (grep for "complete command line"); state the byte counts.
 4. Report whether a row as drafted (S278, 11 cells) would parse: pipe count, quote word count,
    anchor resolvability.

## Acceptance
A verdict per item with the located quotes and digests; a refutation is reported as one, never
softened. No lane edit.

## Evidence
.report .ufo/waves/round-74/w1/ScoutSource.md
""")

item("ReviewerClaims", "reviewer", """
## Target
Re-derive both claims from committed bytes. Do not run the lane's instruments as your primary
evidence: read receipts, blobs and `git show` only (you may run `--validate`).

## Change
 1. R74-C1: from `.ufo/waves/round-74/pre/c1-base-arm.json` and
    `pre/c1-post-at-declaration.json`, re-derive the survivor lists, the declared cases per
    mutant, the pristine case counts and the target pin; check the six names against
    `.ufo/waves/round-73/w1/MutProbe/results.json`. Confirm or refute the frozen predicate's
    clauses one by one.
 2. R74-C2: re-derive at least six of the nine new atoms independently (your own reads, not the
    audit's rows) at base `04fdc2c4` and at the freeze `021914c0`, and compare with the two
    committed receipts.
 3. Check that no instrument blob changed between the declaration and the freeze (git diff).
## Acceptance
A claim-by-claim table: clause, verdict, evidence. A disagreement with the audit's atom rows is
the most valuable finding; report it with exact bytes.

## Evidence
.report .ufo/waves/round-74/w1/ReviewerClaims.md
""")

item("ReviewerGates", "reviewer", """
## Target
The freeze and gate evidence of round 74.

## Change
 1. Run `python3 -I -B tools/round-29/freeze-gate.py --root . --rev 021914c0e638454e507087accfe41af1ab69f185 --require-clean round-74`; confirm the round-74 freeze is CLEAN and that the instrument list it reports is the five declared instruments' subset the claims name.
 2. Verify every pin in `.ufo/waves/round-74/claims.json` against the blob at the freeze commit (independently of `tools/round-74/freeze-pins.py` — write your own reader).
 3. Check the wave evidence contract: the spec, dispatch and registry under
    .ufo/waves/round-74/, the report trailer paths, and that no seat wrote outside the lane.
 4. Check `corpus/claim-freezes-v2.tsv` for the round-73 FLAGGED row and state whether the
    round-74 row is now required (it is written at record time, not at freeze).

## Acceptance
A row per check with the exact command and output; any mismatch is a defect named with both
values.

## Evidence
.report .ufo/waves/round-74/w1/ReviewerGates.md
""")

item("CriticClaims", "critic", """
## Target
Falsify the two frozen claims. Write nothing outside your evidence dir.

## Change
 1. Attack R74-C1's counting surface: propose and run at least four NEW defect classes that the
    frozen patch set does not contain (candidates: delete `is True` from a `home_under` conjunct;
    make `_name_samples` keep the last sample instead of the first; make `assemble_arm` call the
    forged producer twice; delete the `stale` `sorted(s.get("keys") or []) == allow` conjunct in
    `lie_clean`), score each against the r74 probe with your own harness (not the lane battery),
    and report survivors.
 2. Attack R74-C2's atoms: name at least three ways a cosmetic edit satisfies an atom without
    repairing the defect (e.g. D10's search-log note, D12's numbers, D9's used-by cell) and
    demonstrate one where cheap. Say which are real and which the atom's evidence block already
    bounds.
 3. Attack the controls: can `c1_no_declared_cases` be satisfied by a battery bug rather than by
    the case names?
## Acceptance
Per attack: mechanism, exact run, observed verdict, and whether it is a claim defect, a debt
item for the next round, or refuted. Survivors are named, never hidden.

## Evidence
.report .ufo/waves/round-74/w1/CriticClaims.md and your scratch copies' patches.
""")

item("MutationTester", "mutation-tester", """
## Target
Mutate the round-74 record audit's ATOMS in scratch copies and measure which mutations the
committed evidence catches. Do not edit lane files.

## Change
For each of D8, D9, D11, D13, D14, apply at least one semantic mutation in a scratch copy of
tools/round-74/record-audit.py and run it at base `04fdc2c4` and at the freeze revision:
 - D8: accept a capability row with a dangling evidence pointer (drop the resolve conjunct);
 - D9: accept a used-by cell that names the round-72 entry (substring match on the basename);
 - D11: accept a missing page (drop one page from the required set);
 - D13: accept a file without the trailing newline;
 - D14: accept a receipt with no runner binding.
For each, state whether the *base receipt* (`pre/c2-at-base.json`) and the audit's own
`--selftest` distinguish the mutant from the pristine instrument. A mutant both accept
identically is a survivor and becomes named debt with the exact case it needs next round.

## Acceptance
A table: mutant, rc/failures at base, selftest verdict, survivor or killed-by-named-case. No
claim is made about runtime behaviour.

## Evidence
.report .ufo/waves/round-74/w1/MutationTester.md
""")

item("SentinelScope", "sentinel", """
## Target
Security review of the five round-74 instruments (read-only).

## Change
 1. Path containment: can any receipt field, capability row or claim row make an instrument read
    or write outside the lane root? Check `record-audit.py`'s path tokens, `freeze-pins.py`'s
    worktree mode and `controls.py`'s imported-module loads.
 2. Environment: do any new code paths record environment VALUES (QUALITY row 128)? Check
    `seam-probe.py`'s sample dicts and the controls' receipts.
 3. Subprocess: which children do the instruments start, with which env, and can a caller-made
    path reach an exec? Check `probe-mutation.py`'s detector invocation and `controls.py`'s
    selftest copy.
 4. Scratch discipline: do the instruments honour TMPDIR/`--work`, or do any hardcode /tmp?
Grep for `/tmp` in the five files.
## Acceptance
A finding per check with file:line, severity and the fix; "no finding" is stated explicitly per
check. Blocking findings are named as blocking.

## Evidence
.report .ufo/waves/round-74/w1/SentinelScope.md
""")

item("ConnectorCross", "connector", """
## Target
Sibling-overlap scan for the round's two surfaces. Read-only.

## Change
 1. Name which live sibling lanes own adjacent surfaces for (a) a producer-independent
    observation channel (kernel record vs child claim) and (b) record-vs-receipt auditing /
    provenance binding. Check at least kama, chousa and mado's PROVINCE/SKILL where read access
    exists under /home/vgpnk/Projects/shokunin/; do not write outside your evidence dir.
 2. For each overlap: what this lane's instrument proves, what the sibling's does, and whether a
    crosswalk (shared vocabulary or a shared rule) is warranted. Absorb nothing.
 3. Propose at most two concrete cross-lane items for a later round, each with the lane and the
    exact artifact it would read.
## Acceptance
A table: lane, artifact, overlap, this lane's distinct claim, crosswalk? (yes/no); plus the two
proposals. No sibling file is modified.

## Evidence
.report .ufo/waves/round-74/w1/ConnectorCross.md
""")

spec = {
    "wave": WAVE,
    "milestone": ("r74-w1: the six A12 selftest survivors close by declared cases, the record "
                  "audit binds the round-73 routed set and its freeze pins; independent "
                  "re-derivation, mutation attack, security review, source row, sibling scan."),
    "reportDir": REPORT_DIR,
    "context": BOUNDS + FROZEN + """
## Wave
One v1 wave, 15 seats: 5 executor, 3 scribe, 2 reviewer, 1 critic, 1 mutation-tester, 1
sentinel, 1 scout, 1 connector. Attack roles (reviewer/critic/mutation-tester) 4/15 = 27%.
The L1 holds the planner seat. You are one seat: do your assignment, write only inside the lane,
return a short JSON (files_changed, behavior, evidence, risks), and delete your scratch dir
before you yield.
""",
    "items": ITEMS,
}

path = pathlib.Path(".ufo/waves/round-74/r74-w1-spec.json")
path.write_text(json.dumps(spec, indent=1) + "\n")
print(json.dumps({"items": len(ITEMS),
                  "roles": sorted({i["role"] for i in ITEMS}),
                  "counts": {r: sum(1 for i in ITEMS if i["role"] == r)
                             for r in sorted({i["role"] for i in ITEMS})}}, indent=1))
