#!/usr/bin/env python3
"""Generate the round-48 v2 wave spec, validated dispatch and ready file (L1 artifact)."""
import json
import os
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WAVE_DIR = os.path.join(ROOT, ".ufo/waves/round-48")
FREEZE = "dc73587a8b9c1a23ba5a91dc7707ac7381a8b873"
BASE = "61b87d742032e65fca9c38267d7d6ed7e555edad"
GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim \u2014 let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

"""
AXES = ["coverage", "depth", "calibration"]
MILE = ("Round 48: verify, attack and falsify the two frozen counters (meaning-bound verdict "
        "maps over the instrument registry; the record re-derived from committed bytes with a "
        "completeness floor) and draft the landing evidence before data")
REPORT = ".ufo/waves/round-48/w1"
W = REPORT + "/"
SCRATCH = "/fast/scratch/hyaku/kaidoku-r48/"

CTX = f"""# Target
kaidoku-shokunin round 48, ONE v2 wave = verification, drafting and attack of the round's two FROZEN claim instruments, BEFORE any landing. Lane root (absolute): {ROOT}. L1 = KaidokuR48 (integration owner; it holds the canonical section-3 planner seat — the validator rejects `planner` as a swarm role, so bounded planning data-walks ride scout/connector/revenger seats; recorded in the round report). Declared freeze `{FREEZE}` (`plans/round-48-claims.md` + `tools/round-48/`, directory pathspec, after disclosed amendment A1); base `{BASE}`.

# The two claims (the claims file is the rule — read it, not this prompt)
- **R48-C1 depth**: `SKILL.md` `## Queue-drain craft` rule block 25, marker `<!-- verdict-meaning-table v1 -->`, header `trigger | v1 hole | v2 arm | exit`, exactly two rows (one per `R46-CL7`, `R47-CL10`), arm cells exactly `meaning` / `floor` **keyed by routed id**, a `mutations_sha256` over each mutation's name+body, an `interpreter_sha256` pin, resolving citations incl. one `corpus/knowledge/` entry; plus the **instrument-registry section re-bound by meaning**: rows exactly `tools/round-48/census2.json`, every verdict map split into 0/1/2 segments carrying a success / not-met / unevaluable meaning class, the three distinct. Counter `tools/round-48/meanings.py` (profiles v3 default, v2 = ported round-46/47 semantics).
- **R48-C2 calibration**: `tools/round-48/record2.py` re-derives `SCORECARD.md` from committed bytes — the round-47 atom oracle executed from `--rev`, a completeness floor per round section (seat/path/rev atom or a re-derived seats correction, a claim id), every `## Record corrections — round 48` line re-derived (seats/window/path/rev/axes/quote), quoted receipt numbers bound to the receipt they cite, and the Owned-axes score cell bound to its fraction. 5-forgery battery.
Claims file: **`{ROOT}/plans/round-48-claims.md`**. Read it in full before your first command.

# Contract (binding on every seat)
- **Read-only on the lane tree.** Write ONLY inside `{ROOT}/{W}<YourSeatName>/` (create it). Never edit `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, `SHONEN.md`, `PROVINCE.md`, or the fleet repo. Never commit, push, stage, stash, or run any mutating git/jj command (`add/commit/checkout/reset/switch/pull/push`, `jj commit/new/describe/squash/rebase/abandon/bookmark`). Read-only git is fine: `log`, `show`, `diff`, `diff-tree`, `ls-tree`, `cat-file`, `rev-parse`, `status --porcelain`.
- **Frozen means read-only.** `tools/round-48/` and `plans/round-48-claims.md` are byte-frozen at `{FREEZE}`. Copy to scratch to mutate the copy; never mutate the originals. A finding that a FROZEN clause is vacuous or satisfiable by a forgery is the most valuable thing you can return: give the exact command, the differing value, and a fixture path.
- **Fixture repos**: `D=$(mktemp -d -p "$S") && git -C "$D" init -q`, and every later git call names `-C "$D"`. Verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit. Never run `git commit` with a throwaway identity anywhere else.
- **Scratch**: `S={SCRATCH}<YourSeatName>`; `mkdir -p "$S"`, `export TMPDIR="$S" HYAKU_SCRATCH="$S"`. Remove `$S` before you yield AFTER copying receipts into your report dir. Never write under `/tmp`; nothing under `/tmp` is citable evidence. Check `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` before a heavy pass.
- **Honest capture beats a pass.** Every receipt carries the exact command, exit code, stdout sha256 and UTC time. A check you did not run is not passed — say "not run".
- **Exit codes are semantic**: 0 met/clean, 1 not met/violation, 2 could-not-evaluate. A 2 never counts toward a target.
- **`Report:` trailer**: the `Report: .ufo/waves/...` path in your prompt is relative to `{ROOT}` — write it at `{ROOT}/<that path>`.
- **Tooling**: read `/home/vgpnk/.omp/agent/RULES.md` before installing anything. **All pacman transactions are PAUSED host-wide** — install via `uv tool`/`npx`/an official binary in `~/.local/bin`, or nothing. Record any install (tool, version, channel, reason) in your report.
- Never message `agent://all`; never touch a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`, or the fleet repo.

# What the L1 does with your output
It reads your report, reconciles disagreements, lands `SKILL.md` block 25 and the registry meaning repairs, appends `SCORECARD.md` `## Round 48` + `## Record corrections — round 48`, then re-measures both counters at the landing revision. Do not "fix" frozen bytes.
"""

T = []


def add(name, agent, task):
    T.append({"name": name, "agent": agent,
              "task": GODSPEED + task.replace("<ROOT>", ROOT).replace("<W>", W)
              .replace("<FREEZE>", FREEZE).replace("<BASE>", BASE)})


RUN1 = ("Run `HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/<SEAT> python3 -I -B "
        "<ROOT>/tools/round-48/meanings.py \\\n  --root <ROOT> --freeze <FREEZE> --rev <REV> "
        "--json-out <W><SEAT>/receipt.json`")
RUN2 = ("Run `HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/<SEAT> python3 -I -B "
        "<ROOT>/tools/round-48/record2.py \\\n  --root <ROOT> --freeze <FREEZE> --rev <REV> "
        "--json-out <W><SEAT>/receipt.json`")

# --- R48-C1 ---------------------------------------------------------------------

add("C1Struct", "executor",
    "R48-C1 clauses 1-2 at `--rev <FREEZE>` and at `--rev <BASE>`: marker occurrences, block "
    "count, block-is-last, title `25. `, exact header, exactly two 4-cell rows, exit cells in "
    "{0,1,2}. " + RUN1 + " and record every value. Write `<W><SEAT>/report.md` with a table "
    "and the exact failing lists.")
add("C1IdsArms", "executor",
    "R48-C1 clauses 3-4: each row names exactly one routed id, `{R46-CL7, R47-CL10}` once each, "
    "and the row's arm equals `EXPECTED_ARM[routed id]` (`meaning`, `floor`). Prove the "
    "permutation hole is closed: build a scratch copy of a two-row block with the arms swapped "
    "and show `--profile v3` red / `--profile v2` green. " + RUN1 +
    " Write `<W><SEAT>/report.md` + `fixtures/`.")
add("C1Pins", "executor",
    "R48-C1 clauses 5-6: `mutations_sha256` must equal sha256 over each mutation's NAME and its "
    "own source body (this closes R47-CL4's names-only pin), and `interpreter_sha256` must equal "
    "the bytes of `tools/round-48/meanings.py` at `--rev`. Demonstrate: (a) a block whose digest "
    "was computed from names only is red; (b) editing one mutation BODY in a scratch copy of the "
    "counter moves the digest (so a body edit is visible). " + RUN1 +
    " Write `<W><SEAT>/report.md` with both fixtures.")
add("C1Refs", "executor",
    "R48-C1 clause 7: every `corpus|plans|tools/round-48` citation in block 25 resolves with a "
    "line selector inside 1..line_count at `--rev`, the block cites `corpus/lessons/round-47.md` "
    "and at least one `corpus/knowledge/` entry (QUALITY row 77a). Enumerate the citations a "
    "draft block must carry and test a citation with an out-of-range selector. " + RUN1 +
    " Write `<W><SEAT>/report.md`.")
add("C1Meaning", "executor",
    "R48-C1 clause 8, the meaning classifier: run it over the registry section at `<FREEZE>` and "
    "list EVERY row that fails, with the reason per row (no success/not-met/unevaluable class, "
    "duplicate segment, placeholder). Also test the classifier's edges: a segment naming two "
    "classes, `not met` inside the exit-0 text, a meaning containing the word `met` only as part "
    "of `not met`, an exit-2 text that says `refusal`. " + RUN1 +
    " Write `<W><SEAT>/report.md` with a per-row table and edge table.")
add("C1Census", "executor",
    "R48-C1 clause 8, the census half: `tools/round-48/census2.json` must equal a fresh "
    "derivation of `census2.py`'s rule at `--rev`, and the registry path set must equal it "
    "exactly. Derive the diff (missing/extra/duplicate) at `<FREEZE>`, and prove the clause "
    "fails on a one-path census drift and on a duplicated row. Run "
    "`python3 -I -B <ROOT>/tools/round-48/census2.py --root <ROOT> --rev <REV>` and "
    + RUN1 + " Write `<W><SEAT>/report.md`.")
add("C1Battery", "mutation-tester",
    "Attack the R48-C1 battery (4 forgeries, `v2_green 4`, `v3_green 0`). Find: a forgery that is "
    "a no-op at the landing revision; a forgery that differs nowhere it claims to (QUALITY row "
    "78b); a way to make `--profile v3` green while the artefact does no work (R47-CL10 class); "
    "whether the battery gate is coupled to the profile (R47-CL9 class). " + RUN1 +
    " Write `<W><SEAT>/report.md` with one receipt per attack.")
add("C1Gold", "critic",
    "Gold-artefact attack on R48-C1: construct the cheapest block 25 + registry that satisfies "
    "every v3 clause while doing no work (e.g. two rows that restate the claim, a registry whose "
    "meaning classes are cosmetic, citations that resolve but say nothing). Score it; if it is "
    "green, the claim is satisfiable and must be reported as such with the fixture. " + RUN1 +
    " Write `<W><SEAT>/report.md`.")
add("C1V2", "executor",
    "Ported-profile control for R48-C1: score the LANDED artefact (once block 25 exists; until "
    "then use your best draft) with `--profile v2` and with `--profile v3`, and show every "
    "forgery green under v2 and red under v3, the genuine artefact green under both. Record the "
    "exact invocation as the control the L1 must commit as `ctl-c1-1-v2-profile.json`.")
add("C1RowsA", "scribe",
    "Draft the corrected verdict-map cells for the FIRST HALF (alphabetical by path) of the "
    "registry rows that `tools/round-48/meanings.py` scores as failing at `<FREEZE>`. For each: "
    "read the tool's own source at `<ROOT>` and its exit contract, then write a cell of the form "
    "`0=<success class>, …; 1=<not-met class>, …; 2=<unevaluable class>, …` that states the "
    "tool's ACTUAL meanings. Write `<W><SEAT>/cells.md` as a table path | old cell | new cell | "
    "source line proving the meaning.")
add("C1RowsB", "scribe",
    "Same as C1RowsA for the SECOND HALF of the failing rows. `<W><SEAT>/cells.md`.")
add("C1NewRows", "scribe",
    "Draft the two missing registry rows (`tools/round-48/meanings.py`, "
    "`tools/round-48/record2.py`) in the house 7-cell schema, meaning-bound verdict maps, "
    "self-test command, pinned-value path, write scope, owner. Read each tool's `--help` and its "
    "exit contract. Write `<W><SEAT>/rows.md`.")
add("C1Block", "scribe",
    "Draft the exact bytes of craft rule block 25: title `25. …`, marker "
    "`<!-- verdict-meaning-table v1 -->`, the two-row table (`R46-CL7` -> `meaning`, `R47-CL10` "
    "-> `floor`), both pins, and the `Refs:` line. Read blocks 23-24 for the house style and "
    "`plans/round-48-claims.md` for the frozen predicate. Write `<W><SEAT>/block.md`; the L1 "
    "lands it verbatim after re-deriving both pins.")
add("C1Semantic", "reviewer",
    "Review the drafted verdict-cell repairs against the tools' own sources: does each new cell "
    "state the meaning the tool's code actually implements (exit 0/1/2)? Flag every cell that "
    "asserts a meaning the source does not support, and every meaning class that hides a real "
    "third state. Read `<ROOT>/tools/round-4[1-8]/` directly.")
add("C1SelfTest", "executor",
    "Coverage review of `meanings.py --selftest` (16 cases): name the cases that must exist and "
    "do not (a body-edit digest case, a `not met` inside exit 0, a two-class segment, a "
    "placeholder in only one segment, a census duplicate). Run the selftest and record "
    "`cases`/`failures`; propose the missing cases as text, do not edit the frozen file.")

# --- R48-C2 ---------------------------------------------------------------------

add("C2Floor", "executor",
    "R48-C2 clause 2, the completeness floor: for each of the last two `## Round N` sections, "
    "require a seat atom (or a re-derived seats correction), a path atom, a rev atom and a claim "
    "id, ids unique. Show (a) which of the two sections fails at `<FREEZE>` and why; (b) that a "
    "tautological section keeping only seat/window atoms is red under v3 and green under v2. "
    + RUN2 + " Write `<W><SEAT>/report.md`.")
add("C2Quote", "executor",
    "R48-C2 clause 4: every quoted `atoms|exempted|corrections|mismatches N` in a round section "
    "must be backed by a receipt that section cites, or by a re-derived `quote` correction. "
    "Reproduce the round-47 `exempted 2` misquote (the receipt reads 1), then test a forged "
    "quote correction that corrects a value already right (must be red) and one that names a "
    "round outside the window (must be red). " + RUN2 + " Write `<W><SEAT>/report.md`.")
add("C2Corr", "executor",
    "R48-C2 clause 3: the corrections grammar now parses `seats|window|path|rev|axes|quote`. "
    "Prove `axes` corrections are no longer silently inert (R47-CL14): a correct "
    "`- corrects axes depth: 24/24 …` is accepted, a wrong `999/999` is red under v3 and green "
    "under v2. Also test a seats correction whose total disagrees with the dispatch file. "
    + RUN2 + " Write `<W><SEAT>/report.md`.")
add("C2Axes", "executor",
    "R48-C2 clause 5: the coverage/depth score cell's second number must equal "
    "`round(10*n/d,2)` for the first fraction in the row (R47-CL2). Reproduce the A1 defect "
    "(the parser read the evidence cell, so the clause scored nothing: "
    "`.ufo/waves/round-48/controls/ctl-c2-a1-before.json` shows `axis_score_cells {}`), then "
    "prove a stale score with a fresh fraction is red. " + RUN2 + " Write `<W><SEAT>/report.md`.")
add("C2Oracle", "executor",
    "R48-C2 clause 1, R47-CL1: the atom oracle must run from the bytes at `--rev`, never from "
    "the worktree. Prove it: copy the lane to scratch, replace `tools/round-47/record.py` in the "
    "COPY with a stub that prints a green receipt, run `record2.py --root <copy>` and show the "
    "verdict does not move. Then show what DOES still come from the worktree (the `gate` import) "
    "and bound it. " + RUN2 + " Write `<W><SEAT>/report.md`.")
add("C2OracleLimit", "reviewer",
    "Bound the oracle delegation: `record2.py` execs `tools/round-47/record.py` from committed "
    "bytes but imports `tools/round-46/gate.py` from the worktree, and calls the oracle's "
    "`collect`/`derive`/`corrects`. List every path that is still worktree-sourced, every way a "
    "tampered worktree can move a C2 verdict, and whether any of them can flip exit 0. Measure, "
    "do not speculate.")
add("C2Battery", "mutation-tester",
    "Attack the R48-C2 battery (5 forgeries, `v2_green 5`, `v3_green 0`): find a forgery that is "
    "a no-op at the landing revision, one that fails for a reason other than the clause it "
    "names, and one that stays green under v3. Also test the battery's own precondition: the "
    "battery only runs when the genuine card is green — what does that hide? " + RUN2 +
    " Write `<W><SEAT>/report.md`.")
add("C2Gold", "critic",
    "Gold-record attack on R48-C2: write the cheapest SCORECARD tail that satisfies every v3 "
    "clause with no real record (claims named in prose, a receipt quoted correctly, one real "
    "path, one resolvable rev, a seats correction). Score it. If green, report the fixture and "
    "the clause that should have caught it. " + RUN2 + " Write `<W><SEAT>/report.md`.")
add("C2Selftest", "executor",
    "`record2.py --selftest` is parser-only. Specify the case table the counter should carry "
    "(per clause: one green and one red card, plus the five forgeries) and run the existing "
    "selftest, recording its output. Do not edit the frozen file; the L1 routes the gap.")
add("C2LandingGate", "executor",
    "Write a read-only landing preflight under `<W><SEAT>/` (`preflight.py` or `.sh`) that the "
    "L1 can run in one command before committing: block 25 present with both pins matching the "
    "bytes, registry rows == census2 paths, 0 meaning failures, both counters exit 0 at `--rev`, "
    "and no uncommitted change under `tools/round-48/` or `plans/round-48-claims.md`. Test it at "
    "`<FREEZE>` (must report red) and record the exact command line.")

# --- cross-claim attack -----------------------------------------------------------

add("CritSeparability", "critic",
    "Causal separability of R48-C1 and R48-C2: does either counter read the other's surface? "
    "Read both sources and prove or refute by measurement (score each at a revision where only "
    "the other's artefact exists). Name every shared input.")
add("CritClaims", "critic",
    "Falsify the two claim statements themselves: does R48-C1 move depth (QUALITY row 75: the "
    "depth surface is the craft section and its counting recipe) and R48-C2 move calibration? "
    "Is either claim a re-scoring of work the lane already holds? Is the after-state one value "
    "a closure can re-derive with one command?")
add("CritAxis", "critic",
    "Axis-harm audit: name every axis the round touches and the command that would show harm. "
    "Coverage must not move (no knowledge entry, no coverage-map row, no PROVINCE change) — "
    "verify with `git diff` over `corpus/knowledge`, `corpus/README.md` and `PROVINCE.md` between "
    "`<BASE>` and the landing revision once it exists.")
add("ConnAxes", "connector",
    "Cross-axis pattern scan: map each of the six routed defects (R46-CL7, R47-CL10, R47-CL1, "
    "R47-CL2, R47-CL13, R47-CL14) to the clause that closes it, and name any routed defect the "
    "round leaves open with the reason. Also scan rounds 41-47 for the same defect class "
    "appearing in an instrument the round does NOT touch.")
add("ConnRouted", "connector",
    "Sibling-overlap scan across the lane's own counters: which of `tools/round-4[1-8]` share a "
    "clause vocabulary (`met_target`, `failing`, exit 2 semantics, `frozen_path_changed`) and "
    "which disagree with the round-48 predicates? Name every disagreement with file:line; do not "
    "edit.")
add("RevRecord", "revenger",
    "Reverse-engineer what the round-47 record section claims versus what its own receipts say "
    "(M47-9 class). Enumerate every number the last two round sections state that a receipt also "
    "states, and report each disagreement. This is the evidence the `quote` correction clause "
    "rests on.")
add("SentScope", "sentinel",
    "Write-scope audit of both counters: can `--json-out` write inside the graded bytes or "
    "outside the lane (gate.out_path)? Can a fixture repo be created outside scratch? Can a "
    "counter read or write a sibling lane or the fleet repo? Measure each answer with a "
    "command; report anything a seat could exploit.")
add("SimplC1", "simplifier",
    "YAGNI pass on `tools/round-48/meanings.py`: for every clause, function and flag, name the "
    "claim clause it serves or argue for deletion. Specifically: is the `v2` profile "
    "load-bearing, is `MUST_KNOW` checkable as written, and does `census_rederive` earn its "
    "cost? Write a keep/cut table.")
add("SimplC2", "simplifier",
    "YAGNI pass on `tools/round-48/record2.py`: same treatment. Specifically: the `quote` "
    "correction class, the `axes` clause, the floor's per-section granularity, and the oracle "
    "delegation.")
add("ReviewerC1", "reviewer",
    "Surgical correctness review of `tools/round-48/meanings.py`: off-by-one in segment "
    "splitting, a regex that can match across cells, `SEG` matching a digit inside a word, the "
    "`_segments` rstrip, `check_refs`'s SELF skip, the census exec sandbox. Name each defect "
    "with file:line and a reproducing input.")
add("ReviewerC2", "reviewer",
    "Surgical correctness review of `tools/round-48/record2.py`: `_round_sections` offsets after "
    "in-place mutation, `_split_corrections`, `quote_value` on bools/lists, the `quote_fixes` "
    "path, `axis_scores` cell indexing, and the oracle exec namespace. Name each defect with "
    "file:line and a reproducing input.")
add("ReviewerBlock", "reviewer",
    "Review the drafted block 25 text against the frozen predicate: every clause the counter "
    "checks must be stated in the block, no clause may be stated that the counter does not "
    "check, and every routed id must be named where its hole is described. Write "
    "`<W><SEAT>/report.md` with a clause-by-clause coverage table.")
add("ReviewerScore", "reviewer",
    "Review the drafted `## Round 48` section and `## Record corrections — round 48` against "
    "R48-C2's clauses: seat atom, path atom, rev atoms, claim ids, quoted numbers backed by "
    "receipts, corrections that re-derive. Name every clause the draft would fail.")
add("LabC1Meaning", "mutation-tester",
    "One falsifiable hypothesis: 'the meaning classifier accepts a verdict cell whose exit-0 "
    "segment names a success class but whose tool actually returns 2 for that condition'. Pick "
    "three real registry rows, read the tools' sources, and test whether the class label matches "
    "the code path. Report the mismatch list.")
add("LabC2Floor", "mutation-tester",
    "One falsifiable hypothesis: 'the floor can be satisfied without a real record' — build the "
    "cheapest two round sections that carry a claim id, a real path, a resolvable rev and a "
    "seat total, and nothing else, and score them. Report the exit and the residual gap.")
add("LabPins", "reviewer",
    "One falsifiable hypothesis: 'the mutation digest is stable across runs and Python "
    "versions'. Compute `meanings.MUT_DIGEST` twice in separate processes and with `-O`, and "
    "report whether `inspect.getsource` is affected by `__pycache__` or by running from a "
    "different cwd.")

# --- reconnaissance ---------------------------------------------------------------

add("ScoutSkill", "scout",
    "Map the craft section at `<FREEZE>`: number of rule blocks, where block 25 must go, the "
    "exact house style of blocks 23-24 (title, marker, pins, table, Refs), and the section's "
    "line span. Report line numbers and a template the scribe can follow.")
add("ScoutSources", "scout",
    "Source reconnaissance for the round's frontier step: find a PRIMARY source that grounds an "
    "exit-code meaning the registry claims (e.g. Python `argparse` documenting exit status 2 for "
    "usage errors, or a POSIX/BSD exit-status convention for 0/1/2). Open it, record the URL, "
    "access date and a <=25-word located quote, and propose one row to ADMIT and one to REJECT "
    "(with the flip condition). Read `corpus/SOURCES.md` for the 11-column schema and the "
    "census rule.")
add("ScoutLog", "scout",
    "Read `LOG.md`'s last three round entries and report the exact heading/format a round-48 "
    "entry must follow, plus the line number where it belongs. Read-only.")
add("ScoutQuality", "scout",
    "Read `corpus/QUALITY.md` and report: the highest row number, the two-column shape, and "
    "whether rows 75/77/78 already cover the round-48 defect classes (state which is new). "
    "Propose the text of one new row grounded in this round's own A1 defect.")
add("ScoutProvince", "scout",
    "Read `PROVINCE.md` and report whether the round's surface (an instrument registry, a record "
    "counter) falls inside the lane's declared province, and whether any PROVINCE line must "
    "change. Quote the lines you rely on. Read-only.")
add("ScoutWaves", "scout",
    "Read `.ufo/waves/round-47/` receipts and report the house shape of a round's score "
    "receipts: which files under `l1/scores/` the report cites, what each contains, and the "
    "minimum set round 48 must commit.")
add("ScoutShonen", "scout",
    "Read `SHONEN.md` and report the exact four boxes, their current markers and the evidence "
    "pointer style a `[~]` line must carry. Propose the round-48 update line for the box the "
    "round actually moves.")
add("ScoutAssim", "scout",
    "Assimilation census (read-only): compare `/home/vgpnk/Projects/shokuknow/merge/kaidoku/` "
    "(MERGE-REPORT.md, `knowledge/`, `SOURCES.append.md`) with the lane's own "
    "`corpus/knowledge/` and `corpus/SOURCES.md`. Report: how many staged knowledge entries "
    "already have a lane counterpart (by subject, not by filename), the id-collision count "
    "between staged ids and the lane registry (use the 0-3 leading space pattern), and whether "
    "adoption this round would be knowledge or padding. Do not write anything into shokuknow.")

# --- drafting ---------------------------------------------------------------------

add("ScribeBlock", "scribe",
    "Write the final block-25 candidate at `<W><SEAT>/block.md`: title, marker, prose naming "
    "both routed defects and the two arms, the table, both pins (re-derive "
    "`interpreter_sha256` from `<ROOT>/tools/round-48/meanings.py` and `mutations_sha256` by "
    "running the counter), and a `Refs:` line with resolving citations including one "
    "`corpus/knowledge/` entry. The L1 lands it verbatim.")
add("ScribeSources", "scribe",
    "Draft the round-48 SOURCES append: one admitted row and one rejected row in the 11-column "
    "schema, ids continuing the lane registry (read the last id), `used-by` naming this round's "
    "lesson, status `mined`, plus the lesson `## Gate` block (URL, access date, <=25-word located "
    "quote, admit/reject reason, flip condition). Write `<W><SEAT>/sources.md`.")
add("ScribeLesson", "scribe",
    "Draft `corpus/lessons/round-48.md`: `## Gate` (both source rows, admit and reject), "
    "`## Mistakes` (one mined mistake with class, evidence pointer, captured-by, fix — candidate: "
    "A1's vacuous axis-score clause, the same class as the round-47 A2/A5 no-op forgeries), "
    "`## Routed defects (for round 49)` from what the wave found, and the freeze-series "
    "disclosure. Write `<W><SEAT>/lesson.md`.")
add("ScribeScore", "scribe",
    "Draft the `## Round 48` section for `SCORECARD.md`: base/freeze/landing, both claims with "
    "before -> after, counting command, measured revision, owned scores (all three stay 10), "
    "learning trends, and the routed list. Every number must be one a receipt backs. Write "
    "`<W><SEAT>/score.md`.")
add("ScribeCorrections", "scribe",
    "Draft `## Record corrections — round 48` for `SCORECARD.md`: (a) a `seats` correction for "
    "round 47 stating `1 wave, 75 seats total` (the round-47 section states no seat total; "
    "`w1-dispatch.json` reports `counts.spawn 75`), (b) a `quote` correction for round 47's "
    "`exempted` cell (the section quotes 2, the receipt reads 1). Both must satisfy R48-C2's "
    "grammar exactly. Write `<W><SEAT>/corrections.md`.")
add("ScribeLog", "scribe",
    "Draft the round-48 `LOG.md` entry in the house format: claims, freeze, landing, what was "
    "measured, what was found and routed. Write `<W><SEAT>/log-entry.md`.")
add("ScribeReport", "scribe",
    "Draft the round report's `## Work performed` and `## Landed changes` bullets from the "
    "claims file and the wave's receipts (they land under `<W>`), each bullet carrying an "
    "evidence pointer. Write `<W><SEAT>/report-draft.md`.")
add("ScribeShonen", "scribe",
    "Draft the round's SHONEN update: one line per box, `[~]` with a resolvable evidence "
    "pointer, `[x]` only with a named non-author verifier. Write `<W><SEAT>/shonen.md`.")
add("ScribeQualityRow", "scribe",
    "Draft QUALITY.md row 79 (or the next free number): 'a clause that scores nothing is not a "
    "clause' — the A1 defect (a parser reading the wrong cell made the axis-score clause green "
    "over zero rows), with the red-before receipt pointer and the rule the next round should "
    "apply. Two sentences, house style.")
add("ScribeRowsC", "scribe",
    "Third pass over the failing registry verdict cells: for rows whose honest meaning is not "
    "one of the three classes (e.g. `1=never a verdict`), propose the class prefix that keeps "
    "the tool's real meaning AND satisfies the counter, or argue in `<W><SEAT>/report.md` that "
    "the counter's vocabulary is wrong for that tool (with the code line).")

# --- execution / evidence ---------------------------------------------------------

add("ExecControls", "executor",
    "Re-run and record the round's controls at the declared freeze `<FREEZE>`: "
    "`ctl-c1-0-do-nothing.json`, `ctl-c2-0-do-nothing.json`, `ctl-c2-1-v2-profile.json`. Verify "
    "the committed ones under `.ufo/waves/round-48/controls/` reproduce byte-identical JSON "
    "(modulo timestamps) and report any drift.")
add("ExecCensus", "executor",
    "Regenerate `tools/round-48/census2.json` from the worktree and from `<FREEZE>`; report "
    "whether the committed file equals both derivations, the path count, the per-claims-file "
    "counts, and the registry diff (missing/extra/duplicate).")
add("ExecMeasure", "executor",
    "Write and run the round's measurement harness under `<W><SEAT>/`: the exact before "
    "(`<BASE>`) and after (landing, or the freeze if no landing yet) invocations for both "
    "counters, capturing exit code, `met_target`, `failing`, `meaning_rows_failed`, `floor`, "
    "`quotes_bad`, `battery`. One JSON per invocation plus a `measure.sh` the L1 can re-run.")
add("ExecSelftest", "executor",
    "Run both counters' selftests at `<FREEZE>` and record `cases`/`failures` verbatim: "
    "`meanings.py --selftest` (16 cases) and `record2.py --selftest` (parser-only). Report what "
    "each selftest does NOT cover.")
add("ExecRegistryAudit", "executor",
    "Independent audit of the registry section at `<FREEZE>`: for every row, does the named "
    "self-test command exist and is it runnable (`--selftest` present in the tool's argparse)? "
    "Report rows whose self-test cell claims a case count the tool cannot produce. Do not run "
    "heavy selftests.")
add("ExecReportNums", "executor",
    "Build the round's number ledger: every number the report will state (seat count, wave "
    "size, role mix, atoms, meaning rows failed before/after, forgeries green) with the exact "
    "command that derives it and the receipt path. Write `<W><SEAT>/numbers.md`.")

add("ScoutKnowledge", "scout",
    "QUALITY row 77(a) requires a new craft block to cite a `corpus/knowledge/` entry with a "
    "line range. Read the lane's `corpus/knowledge/` index and pick the entry that actually "
    "grounds the round-48 rule (a registered class set can hold while the surface stays "
    "shortcut-reachable; a check must fail where it claims to bind). Report the path, the exact "
    "line range, and a one-sentence statement of what those lines say.")
add("ScribeRowsD", "scribe",
    "Third split of the failing verdict cells: take the rows assigned to neither C1RowsA nor "
    "C1RowsB (coordinate by reading their reports if they exist, otherwise take the last third "
    "alphabetically) and draft meaning-bound cells. `<W><SEAT>/cells.md`.")
add("ReviewerRegistry", "reviewer",
    "Attack the registry repair as a set: after the repairs, does any row's purpose cell now "
    "contradict its verdict map (a `gate` whose exit 2 means `usage` only)? Does any repaired "
    "row still name a meaning its tool does not implement? Sample 12 rows across rounds 41-48 "
    "and read the tools.")
add("ReviewerCorrections", "reviewer",
    "Review the drafted `## Record corrections — round 48` lines against R48-C2's grammar and "
    "the round-47 oracle's own `corrects()`: exact phrasing, the seats total against "
    "`w1-dispatch.json`, the quote correction against the cited receipt. Name every mismatch.")
add("MutC1Rows", "mutation-tester",
    "Attack the drafted verdict-cell repairs: can a purely cosmetic prefix (`0=met, ...`) pass "
    "the meaning classifier while the tool's exit 0 does NOT mean met? Find the cheapest cell "
    "that passes the counter and misstates the tool, and name the clause that should catch it.")
add("MutC2Corr", "mutation-tester",
    "Attack the corrections grammar: a correction line that re-derives but corrects nothing "
    "material, a `quote` correction whose section quotes a value the receipt never had, an "
    "`axes` correction for an axis the card does not own. Score each; report which are green.")
add("RevC1", "revenger",
    "Reverse-engineer the intended semantics of block 25's two arms (`meaning`, `floor`) from "
    "the counter's code and the routed defects: what did the author mean each arm to guarantee, "
    "and does the code guarantee it? Name every gap between intent and implementation.")
add("CritAssim", "critic",
    "Attack the round's assimilation decision: the merge package stages 77 knowledge entries "
    "and 132 rows; the lane already holds 138 knowledge files and 144 rows. Is refusing adoption "
    "as duplicate/padding defensible, or is there a subset that is genuinely new ground? Measure "
    "the overlap by subject (not filename) and rule.")
add("ExecGateRun", "executor",
    "Run the C2LandingGate preflight (from the C2LandingGate seat if it exists, else write your "
    "own read-only copy under `<W><SEAT>/`) at `<FREEZE>` and report its exit plus every red "
    "line; then state the exact command the L1 runs at the landing revision.")
add("ScribeReportNumbers", "scribe",
    "Draft the report's `## Before -> after measurements` and `## Trend verdicts` sections from "
    "the receipts under `<W>`: one row per claim with the counting command and the measured "
    "revision, and three trend verdicts with evidence. Every number must name its receipt.")


def main():
    items = [{"name": t["name"], "role": t["agent"], "prompt": t["task"], "axes": AXES}
             for t in T]
    spec = {"wave": "r48-w1", "milestone": MILE, "reportDir": REPORT,
            "context": CTX, "items": items}
    spec_path = os.path.join(WAVE_DIR, "w1-spec.json")
    with open(spec_path, "w") as f:
        json.dump(spec, f, indent=1)
    env = dict(os.environ, UFO_FLEET_ALLOW_EXTERNAL_TOOLS="1",
               UFO_CONFIG_PATH="/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy-v2.json",
               UFO_PROJECT_ROOT=ROOT)
    proc = subprocess.run(["node", os.path.expanduser("~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs"),
                           "plan", "--spec", spec_path],
                          capture_output=True, text=True, env=env, cwd=ROOT)
    if proc.returncode != 0 or not proc.stdout.strip().startswith("{"):
        raise SystemExit("validator failed: rc=%s %s %s"
                         % (proc.returncode, proc.stdout[:800], proc.stderr[:800]))
    plan = json.loads(proc.stdout)
    wave_tasks = plan["tasks"]
    members = {t["name"]: {"kind": "spawn", "agentId": None, "role": t["agent"],
                           "item": None, "axes": AXES, "milestone": MILE}
               for t in wave_tasks}
    dispatch = {
        "schema": "ufo-swarm-wave-dispatch-v1", "wave": "r48-w1",
        "policy": plan["policy"], "counts": plan["counts"],
        "registry": {"schema": "ufo-swarm-registry-v1",
                     "path": ".ufo/waves/round-48/w1/swarm-registry.json",
                     "reportDir": REPORT, "members": members},
        "compaction": plan.get("compaction", {"applied": False, "mechanism": None,
                                              "reason": None, "savedBytes": 0,
                                              "payloadBytesBefore": 0,
                                              "payloadBytesAfter": 0}),
        "taskCall": {"context": plan["context"], "tasks": wave_tasks},
        "resumeSends": [],
        "note": ("Issue exactly one batched task call with taskCall ({context, tasks}); never "
                 "split a wave into multiple task calls (one-swarm-per-wave)."),
    }
    with open(os.path.join(WAVE_DIR, "w1-dispatch.json"), "w") as f:
        json.dump(dispatch, f, indent=1)
    os.makedirs(os.path.join(WAVE_DIR, "w1"), exist_ok=True)
    with open(os.path.join(WAVE_DIR, "w1/swarm-registry.json"), "w") as f:
        json.dump({"schema": "ufo-swarm-registry-v1", "wave": "r48-w1",
                   "reportDir": REPORT, "members": members}, f, indent=1)
    if "--no-ready" in sys.argv:
        print("ready file NOT written (--no-ready)")
    else:
        with open(os.path.join(WAVE_DIR, "w1.ready"), "w") as f:
            json.dump({"lane": "kaidoku", "round": 48, "wave": "r48-w1",
                       "dispatch": os.path.join(WAVE_DIR, "w1-dispatch.json"),
                       "l1": "KaidokuR48"}, f)
        print("ready written:", os.path.join(WAVE_DIR, "w1.ready"))
    print(json.dumps({"items": len(items), "counts": plan["counts"],
                      "roles": {r: sum(1 for t in T if t["agent"] == r)
                                for r in sorted({t["agent"] for t in T})}}, indent=1))


if __name__ == "__main__":
    main()
