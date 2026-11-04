#!/usr/bin/env python3
"""Generate the round-75 wave-1 spec (r75-w1): 14 seats, one v1 wave."""
import json
import pathlib

WAVE = "r75-w1"
REPORT_DIR = ".ufo/waves/round-75/w1"
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
Scratch: create ONE dir `/fast/scratch/hyaku/kaidoku-r75/<your-seat-name>/` (mkdir -p), pass it explicitly
(TMPDIR=... and any --work), and delete it with `trap 'rm -rf -- "$S"' EXIT` (or a
finally:) before you yield; receipts first copied under
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-75/w1/<your-seat-name>/.
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

FROZEN = """## Frozen state (round 75)
base `3c15a156239af06114e1ece8d1044a0d8205379b` (the round-74 lane tip); declaration
`8dff07b9ac7dfc3f099c97d98ee97cc5f69efb3a` (five round-75 instruments + plans/round-75-claims.md
+ the census-start receipt, committed BEFORE any claim data); freeze
`ec149dc497b4de53ccb3e7a125baa226a66daaa7` (claims.json + the pre receipts; the round-29 gate
audits it CLEAN, no findings, four instrument paths).
Claims (frozen sentences in plans/round-75-claims.md and .ufo/waves/round-75/claims.json):
R75-C1 operability -- the extended A12 class set closes: battery patch set r75probe on
  tools/round-75/seam-probe.py scores survivor_count 0, every mutant killed by its declared
  case, and b-drop-canary-field is the SOLE detector of a12-kernel-canary-field (failed ==
  exactly that case), pristine 25 cases, target pinned before execution; while patch set
  r75base on tools/round-74/seam-probe.py names exactly four survivors
  (d-home-under-truthy, d-tmpdir-under-truthy, d-name-samples-last-wins, d-lie-clean-superset)
  and b-drop-canary-field is not sole.
R75-C2 calibration -- the round-75 record audit (eight atoms D16-D23 from the round-74
  spot-check's routed defects 1-8) reports mismatch_count 8 at base 3c15a156 and 0 at the
  landing revision, with a defect-free validate block and a committed --validate receipt.
Instruments (committed at the declaration; `python3 -I -B`):
 tools/round-75/seam-probe.py (71 KB route-instrument probe, A1-A12 arms + 25-case selftest),
 tools/round-75/probe-mutation.py (battery: patch sets r75probe/r75base, sole_detector,
 pin-before-execution), tools/round-75/record-audit.py (eight atoms + exact grammars),
 tools/round-75/freeze-pins.py (containment-hardened pin checker), tools/round-75/controls.py.
Pre receipts (committed at the freeze): .ufo/waves/round-75/pre/c1-base-arm.json (r75base: 4
survivors, canary cross-binding), c1-post-at-declaration.json (r75probe: 0 survivors, sole
true), c2-at-base.json (mismatch_count 8), c2-at-declaration.json (8), controls-at-declaration.json
(4 of 4 arms met), freeze-pins-before-freeze.json (8 rows, 0 mismatches).
Round-74 receipts the arms may read: .ufo/waves/round-74/l1/scores/*.json,
.ufo/waves/round-74/pre/*.json, .ufo/waves/round-74/w1/*.md.
The round-74 non-author spot-check (the atom population, an OUTSIDE document):
corpus/lessons/round-74-verifier-spotcheck.md sections 2-6.
Frozen source pages opened for this round: proc_pid_cmdline(5)
 https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html (admitted S283) and
 environ(7) https://man7.org/linux/man-pages/man7/environ.7.html (rejected S284).
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
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-75/w1/ExecProbeCases/
(your evidence dir). Do not edit lane files.

## Change
Independently re-derive the four survivors and the cross-binding of the CLAIM'S BEFORE WORLD,
without running tools/round-75/probe-mutation.py. On a scratch copy of the round-74 probe
(`git show 3c15a156:tools/round-74/seam-probe.py`), hand-apply each mutation and run
`python3 -I -B <copy> --selftest` with TMPDIR set and cwd the lane:
 1. `and s.get("home_under") is True` -> `and bool(s.get("home_under"))` (expect the selftest
    to stay GREEN: a survivor);
 2. `and s.get("tmpdir_under") is True` -> `and bool(s.get("tmpdir_under"))` (expect GREEN);
 3. `out.setdefault(name or "?", sample)` -> `out[name or "?"] = sample` (expect GREEN);
 4. `sorted(s.get("keys") or []) == allow and not s.get("canary_present")\n        for s in
    forged_shims.values())` -> a `set(...) >= set(allow)` superset test (expect GREEN);
 5. delete the sample dict's `"canary_present": "KAIDOKU_ENV_CANARY" in env,` line (expect RED,
    and record the FULL `failures` list -- the cross-binding claim is that BOTH
    `a12-kernel-multiple-samples` and `a12-kernel-canary-field` fail).
Record the pristine run too (expect 20 cases, failures []).

## Acceptance
Rows 1-4: rc 0 and `failures` []; row 5: rc 1 with exactly the two case names. Any other
outcome is a defect reported with its exact output. Receipt JSON at
.ufo/waves/round-75/w1/ExecProbeCases/receipt.json with `pristine`, `rows` (name, mutation,
rc, failures, verdict).

## Evidence
Write .ufo/waves/round-75/w1/ExecProbeCases.md plus the receipt.
""")

item("ExecBattery", "executor", """
## Target
tools/round-75/probe-mutation.py and .ufo/waves/round-75/w1/ExecBattery/.

## Change
Run the frozen battery twice at the declaration revision, from the lane root, with your own
--work:
 A) `--rev 8dff07b9ac7dfc3f099c97d98ee97cc5f69efb3a --tool tools/round-75/seam-probe.py
    --patch-set r75probe --expect-survivors 0 --expect-target-sha256
    1fc1c8fc6d08b8626ead431961f286753805a08893b73bdb2350261ad1ac410d
    --expect-sole b-drop-canary-field`
 B) `--rev 3c15a156239af06114e1ece8d1044a0d8205379b --tool tools/round-74/seam-probe.py
    --patch-set r75base --expect-survivors 4`
Then run `--validate` on each receipt and `--selftest`. Re-derive from the JSON: the pristine
case count, every mutant's verdict and `failed` list, `sole_detector`, `target_pin`, the runner
block (path sha256 must equal `git show 8dff07b9:tools/round-75/probe-mutation.py | sha256sum`).
Also verify the pin-before-execution clause: rerun A with a deliberately wrong
`--expect-target-sha256` and require exit 2 with NO mutant executed (no scratch mutation dir
written under the --work you pass).

## Acceptance
A: exit 0, survivor_count 0, 15 mutants all killed, b-drop-canary-field sole with failed
["a12-kernel-canary-field"], pristine 25, pin matched+pinned_before_exec. B: exit 0, exactly
four survivors named and b-drop-canary-field not sole. `--validate` exit 0 both, `--selftest`
exit 0. Wrong-pin run: exit 2 and no new directory under --work. Any deviation is a defect.
Receipt at .ufo/waves/round-75/w1/ExecBattery/receipt.json.

## Evidence
Write .ufo/waves/round-75/w1/ExecBattery.md plus the receipt.
""")

item("ExecAuditBase", "executor", """
## Target
tools/round-75/record-audit.py and .ufo/waves/round-75/w1/ExecAuditBase/.

## Change
Run the frozen audit at base `3c15a156`, at the declaration `8dff07b9`, and `--selftest`; run
`--validate` on the base receipt. For each of the eight atoms, read its `evidence` block and
state which routed defect (1-8 of corpus/lessons/round-74-verifier-spotcheck.md section 6) it
re-derives, and whether the atom is false at base for THAT reason (the artifact is absent or
the property fails) rather than a path typo, a wrong regex, or an exception. Check that D20's
grammar fixtures really reject the four cosmetic constructions and that D21's pin set is
exactly the plan's `tools/round-75/*.py` set.

## Acceptance
Base: exit 1, mismatch_count 8, atom ids exactly D16-D23, every atom `ok false` with the named
reason. Declaration: same eight mismatches (the record is not written yet). `--selftest` exit 0
with the ten grammar/receipt cases. `--validate` on the base receipt: defects []. Report any
atom that is false for a mechanical reason (wrong path/regex) as a defect. Receipt at
.ufo/waves/round-75/w1/ExecAuditBase/receipt.json.

## Evidence
Write .ufo/waves/round-75/w1/ExecAuditBase.md plus the receipt.
""")

item("ExecAuditGrammars", "executor", """
## Target
tools/round-75/record-audit.py (read-only) and .ufo/waves/round-75/w1/ExecAuditGrammars/.

## Change
Attack the four strengthened grammars by building COSMETIC fixtures that a token-presence
predicate would accept, and show the exact grammar rejects each:
 1. used-by: `corpus/knowledge/x.md, not corpus/knowledge/y.md` (negated second path);
 2. used-by: `x.md` (bare filename, no corpus root);
 3. search note: a line naming `round 75`, `Question:`, `Where searched:`, the four field
    words but NO integers;
 4. rejected row: `REJECTED: short` with no `flip:` clause, and a row with `flip:` but a
    one-word reason;
 5. census erratum: `census erratum: W04 lines 23 and 24 rows` while the measured row count
    is 25 (reversed/stale values).
Call the parsers directly in-process (import the module) AND through the committed `--selftest`
case names. Also probe two ACCEPT fixtures (a well-formed cell, a complete rejected row) to
show the grammar is not rejecting everything.

## Acceptance
Each cosmetic fixture returns at least one defect with a reason naming the failed shape; each
accept fixture returns none. Any cosmetic fixture that passes is a BLOCKING defect with its
input and output. Receipt at .ufo/waves/round-75/w1/ExecAuditGrammars/receipt.json.

## Evidence
Write .ufo/waves/round-75/w1/ExecAuditGrammars.md plus the receipt.
""")

item("ExecControls", "executor", """
## Target
tools/round-75/controls.py and .ufo/waves/round-75/w1/ExecControls/.

## Change
Run every control arm from the lane root with `--base-rev 3c15a156` and your own --work:
 `python3 -I -B tools/round-75/controls.py --root . --base-rev 3c15a156 --work <scratch>
  --json-out <your receipt>`.
Independently re-derive each arm from its own observed block: c1_base_world must name the four
survivors and a two-case canary failure; c1_no_declared_cases must show killed [] with at least
six killed_wrong_case; c2_do_nothing must show mismatch_count 8; c2_red_fixtures must show every
grammar case true. Then write a NEGATIVE control of your own: change one assertion (e.g. expect
3 survivors) in a scratch copy and show the arm goes red, so the control is shown able to fail.

## Acceptance
The frozen run: all four arms ok, exit 0. Your negative control: exit 1 naming the changed arm.
Report any arm whose observation is inconsistent with the frozen instruments' own output.
Receipt at .ufo/waves/round-75/w1/ExecControls/receipt.json.

## Evidence
Write .ufo/waves/round-75/w1/ExecControls.md plus the receipt.
""")

item("ScribeRows", "scribe", """
## Target
corpus/SOURCES.md (read-only), the frozen source pages, and
.ufo/waves/round-75/w1/ScribeRows/.

## Change
Verify the round-75 source rows before they enter the registry:
 1. Fetch https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html fresh; record HTTP
    status, byte count, sha256, and save the bytes under your evidence dir. Locate the
    sentence "Think of this file as the command line that the process wants you to see." and
    the surrounding mutability paragraph; report its line span. Confirm a ≤25-word quote exists
    that grounds treating argv as a process CLAIM (not ground truth).
 2. Fetch https://man7.org/linux/man-pages/man7/environ.7.html fresh; digest it; quote the
    sentence defining `environ` and report whether the page says anything about
    `/proc/<pid>/cmdline` (grep it) -- the rejection's flip condition depends on that.
 3. Draft the two registry rows in the exact CORPUS v1 shape (11 cells, no `|` inside a cell,
    `recheck` a valid cadence, `used-by` exactly the admitted entry that cites the row), with
    the S283 admit and S284 reject. Do NOT write corpus/SOURCES.md.

## Acceptance
A `rows.md` with: the two draft rows verbatim, the located quotes with line spans, the
digests, and a cell-count check (each row 11 cells under the census parser). Report any
evidence that would refuse the admit (e.g. the quote not present) as a defect.

## Evidence
Write .ufo/waves/round-75/w1/ScribeRows.md plus the drafts under ScribeRows/.
""")

item("ScribeLesson", "scribe", """
## Target
corpus/lessons/round-75.md (does not exist yet; read-only for you), the round-74 lesson and
spot-check, and .ufo/waves/round-75/w1/ScribeLesson/.

## Change
Draft the two blocks the record audit will read:
 1. `## Gate` table with one row per source decision (S283 admit, S284 reject), each carrying
    URL, access date, a ≤25-word located quote, and a digestion note; plus a row-opened
    convention line stating that `opened` is the date the source was first opened by this lane
    and that a retrospective row names its opening round in the search log.
 2. `## Mistakes` table (class · evidence pointer · captured-by · fix) for the round's mined
    mistake: a predicate that tests for the presence of a token instead of the shape the token
    must have (the canary cross-binding and the four cosmetic atom passes are one class).
 3. The S275 used-by old->new re-log line, verbatim old
    `corpus/knowledge/2026-11-04-r72-checker-env-capsule.md, .ufo/waves/round-72/w1/ScoutSource.md`
    and the new value appending `corpus/knowledge/2026-11-04-r73-kernel-witness-record.md`,
    naming `.ufo/waves/round-74/w1/ScribeRows.md` as the file that held the old value.
Verify against the actual files that every value you state is the committed one.

## Acceptance
A draft file .ufo/waves/round-75/w1/ScribeLesson/draft.md with the three blocks, each value
traceable to a committed path/line you name. Report any mismatch between the draft and the
committed bytes as a defect with both values.

## Evidence
Write .ufo/waves/round-75/w1/ScribeLesson.md plus the draft.
""")

item("ScoutSource", "scout", """
## Target
The two source pages, the lane's A12 code, and .ufo/waves/round-75/w1/ScoutSource/.

## Change
Bounded reconnaissance for R75-C1's sourced claim:
 1. Re-open both pages (proc_pid_cmdline(5), environ(7)) and locate every passage that bears on
    (a) argv as process-controlled/overridable, (b) a zombie/empty read, (c) NUL separation,
    (d) the environment's exec-boundary origin. Give line spans and ≤25-word quotes.
 2. State which of the round-75 claims each passage supports and which it does NOT (e.g. it
    cannot ground merges of duplicate samples or `is True` identity checks).
 3. Check whether `proc_pid_cmdline(5)` and S275's `proc_pid_environ(5)` are the same split
    family and whether the registry's S275 source cell already names the split.
 4. Report the exact `source:`/`verified-at:`/`recheck:` trio a knowledge entry citing S283
    must carry.

## Acceptance
A findings file with the quotes, line spans, and an explicit supported/unsupported table; at
least one passage that does NOT support a claim the lane might be tempted to make. Report any
page drift from round 74's digests as a freshness defect.

## Evidence
Write .ufo/waves/round-75/w1/ScoutSource.md plus snapshots/digests under ScoutSource/.
""")

item("ConnectorCross", "connector", """
## Target
The lane's own instruments and the fleet's shared scripts; evidence in
.ufo/waves/round-75/w1/ConnectorCross/.

## Change
Cross-surface scan (read-only):
 1. Does any other lane or the fleet's `scripts/sources-census.sh` already implement the exact
    grammars round 75 adds (used-by path list, search-note fields, rejected row, erratum
    binding)? Compare the two implementations clause by clause and report divergences that
    would make the lane's atom disagree with the census gate.
 2. Does the round's `sole_detector` concept overlap any existing instrument
    (`tools/round-*/probe-mutation.py`, `mutation-battery.py`)? Report duplicated or
    conflicting semantics.
 3. Does `corpus/QUALITY.md` already carry a criterion for "token presence instead of shape"
    (the mined mistake class)? Quote the nearest rows and say whether a new row is needed or a
    supersession.
 4. `considerthese/` and `/home/vgpnk/Projects/shokuknow/merge/kaidoku/`: state whether either
    serves this round's claims (assimilation line).

## Acceptance
A findings file with a clause-by-clause comparison, exact paths/lines, and a verdict per item:
owner lane, duplication, or new ground. Name any contested scope rather than absorbing it.

## Evidence
Write .ufo/waves/round-75/w1/ConnectorCross.md.
""")

item("ReviewerClaims", "reviewer", """
## Target
R75-C1's frozen predicate (plans/round-75-claims.md, .ufo/waves/round-75/claims.json) and the
committed evidence; .ufo/waves/round-75/w1/ReviewerClaims/.

## Change
Adversarial review of the claim as a CLAIM, not as code:
 1. Re-derive the r75 probe's sha256 at the declaration and compare with the pin the battery
    was told to expect. Re-derive the r74 blob's sha at base.
 2. Find any path by which a do-nothing round could score survivor_count 0 (e.g. a patch set
    whose anchors no longer apply; a pristine count lowered; a `sole` field that is true
    vacuously because `failed` is empty).
 3. Attack the base arm: could it be made to report four survivors while the four classes are
    actually bound (or vice versa)? Check the patch site uniqueness for every one of the
    fifteen classes.
 4. Check the SEMANTIC claim: does `sole_detector` mean what the claim says, and is
    `a12-kernel-multiple-samples` genuinely independent of `canary_present` (read the case code
    and the mutated text)?
 5. Run the two frozen commands yourself and compare counts with the committed receipts.

## Acceptance
A findings file with a verdict per item (agree/disagree + reason) and any BLOCKING defect with
its exact command output. Do not edit lane files.

## Evidence
Write .ufo/waves/round-75/w1/ReviewerClaims.md.
""")

item("ReviewerAudit", "reviewer", """
## Target
R75-C2's eight atoms and the round-74 routed defects; evidence in
.ufo/waves/round-75/w1/ReviewerAudit/.

## Change
Atom-by-atom adversarial review at base `3c15a156` and the declaration `8dff07b9`:
 1. For each routed defect (1-8) state which atom covers it and read the atom's code; name any
    routed item no atom covers (defect 8 is declared cosmetic -- confirm that is the only one).
 2. Find atoms that can pass WITHOUT the repair: e.g. D17 passes on a lesson line that quotes
    the values but contradicts them; D21 passes when `instruments` pins extra files the plan
    never names; D22 passes on a selftest receipt that names the cases but ran nothing.
 3. Check the grammars against the REAL registry text (S275, S282, the search log) -- do the
    parsers accept the well-formed committed rows? A parser that rejects valid data is as
    broken as one that accepts junk.
 4. Verify every atom is FALSE at base for its routed reason (read each evidence block).
 5. Run the audit `--selftest` and `--validate` on the base receipt.

## Acceptance
A findings file with a verdict per atom, any vacuously-passing atom named BLOCKING, and a
parser-vs-real-data table. Exact outputs for every claim.

## Evidence
Write .ufo/waves/round-75/w1/ReviewerAudit.md.
""")

item("CriticClaims", "critic", """
## Target
The round-75 probe blob and the fifteen-class patch set; evidence in
.ufo/waves/round-75/w1/CriticClaims/.

## Change
Falsify the closure claim by finding A12 defects OUTSIDE the declared fifteen classes. On a
scratch copy of `tools/round-75/seam-probe.py`, apply at least eight plausible mutations the
patch set does not contain and run `--selftest` on each. Candidates (verify, do not assume):
 1. `sorted(s.get("keys") or []) == allow` -> compare the list without sorting;
 2. `_samples` accepts only lists (drop the single-dict branch);
 3. `kernel_witness`'s `under()` -> a startswith test (sibling-prefix false green);
 4. `_name_samples` keys on `name or "git"`;
 5. `lie_clean` -> `not any(canary)` only;
 6. `genuine_ok`'s `{"git", "readelf"} <= set(...)` -> `bool(genuine_kernel)`;
 7. `forged_detected` -> `bool(forged_kernel) or bool(forged_shims)`;
 8. `_proc_env` -> swallow `PermissionError` only.
For each: rc, `failures`, verdict (killed by which case / SURVIVOR). Rank the survivors by
whether a case is genuinely missing or the mutation is semantically equivalent.

## Acceptance
A table of at least eight mutations with exact outputs; every SURVIVOR named with the missing
case it would need. A survivor is not a claim failure by itself (the patch set is fifteen
classes) but must be reported, with a semantic-equivalence judgment for each.

## Evidence
Write .ufo/waves/round-75/w1/CriticClaims.md plus a receipt JSON.
""")

item("MutationTester", "mutation-tester", """
## Target
The round-75 instruments' own guards: tools/round-75/probe-mutation.py `validate()`,
tools/round-75/freeze-pins.py containment, tools/round-75/record-audit.py `receipt_defects`.
Evidence in .ufo/waves/round-75/w1/MutationTester/.

## Change
Mutate RECEIPTS and CONTAINERS, not source, and show each guard catches it:
 1. Take .ufo/waves/round-75/pre/c1-post-at-declaration.json; cut `sole_detector`, then one
    `failed` list, then `target_pin.pinned_before_exec`; run `--validate` after each and record
    the defect lines.
 2. Make a scratch claims container whose `instruments` names an absolute path, then a `..`
    path, then a symlink that escapes the root; run `tools/round-75/freeze-pins.py` against
    each and require exit 2 with the containment clause.
 3. Take the base audit receipt; change `mismatch_count` and `ok` independently; run
    `record-audit.py --validate` and record the defects.
 4. Try one mutation that SHOULD survive (e.g. change `root` in the receipt) and report it as
    an honest coverage limit of the guards.

## Acceptance
Every listed mutation is caught with the named clause; the honest survivor is reported. Any
mutation that passes its guard is BLOCKING with the exact mutated field.

## Evidence
Write .ufo/waves/round-75/w1/MutationTester.md plus the mutated copies and outputs.
""")

item("SentinelScope", "sentinel", """
## Target
The five round-75 instruments (source review, no execution of hostile payloads); evidence in
.ufo/waves/round-75/w1/SentinelScope/.

## Change
Adversarial security review, focused on the round-74 SentinelScope SS74 items and the new code:
 1. SS74-1: verify `freeze-pins.py`'s containment (absolute, `..`, symlink escape, the claims
    container itself) is enforced before every open, and that the Git-object branch applies the
    same lexical rule. Try a symlink escape.
 2. SS74-2/SS74-5: verify probe-mutation compares a supplied pin BEFORE any generated copy
    executes, and that the timeout path kills the process group. Look for other pre-execution
    reads of caller-selected revisions.
 3. SS74-3: verify no receipt serialises raw environment values (`_parse_shims`, A11 shim rows,
    capsule paths). Grep every JSON write.
 4. SS74-4: verify the A11 shim is fixed-source + sidecar and that no scratch path reaches perl
    source; look for other interpolated code paths.
 5. New round-75 code: `_samples`/`_name_samples` type confusion, the `sole` computation, the
    audit's `grammar_cases` fixtures, and the audit's `subprocess` calls.
Report severity, the exact path:line, and whether the round's claim depends on it.

## Acceptance
A findings file with a verdict per SS74 item (fixed / not fixed / new variant), at least one
new observation about the round-75 code, and no exploit run. Read-only; do not edit lane files.

## Evidence
Write .ufo/waves/round-75/w1/SentinelScope.md.
""")


def main() -> None:
    spec = {
        "wave": WAVE,
        "milestone": "r75-w1: the A12 case set closes and becomes independent; the record audit's atom grammar becomes exact; independent re-derivation, mutation attack, security review, source row, sibling scan.",
        "reportDir": REPORT_DIR,
        "context": FROZEN,
        "items": ITEMS,
    }
    out = pathlib.Path(__file__).with_name(f"{WAVE}-spec.json")
    out.write_text(json.dumps(spec, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out} with {len(ITEMS)} items")


if __name__ == "__main__":
    main()
